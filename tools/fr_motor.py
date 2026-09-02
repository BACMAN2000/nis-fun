# -*- coding: utf-8 -*-
"""Busca en el motor el texto que el alumno lee y que no pasa por T().

La primera version buscaba palabras inglesas, y por eso se le escapaban
"Start learning" o "Play with sound": no llevan ninguna palabra que solo
exista en ingles. El criterio bueno no es el idioma, es la cobertura: en un
motor bilingue TODA frase que ve el alumno tiene que salir de T(), asi que
lo que hay que listar es lo que no sale de ahi.

Para eso hay que leer las cadenas como las lee JavaScript, no a golpe de
expresion regular: 'Let\\'s look at the answers' lleva una comilla escapada
dentro, `${quedan} more tries` es una plantilla, y dentro de un ${...} puede
haber otra plantilla con mas texto. Las tres se escapaban del barrido
anterior y las tres las ve el alumno.

Y se mira POR SITIO, no por cadena: que 'Listen' este traducido en un boton
no quiere decir que lo este en los otros tres. Por eso lo que se descarta no
es "la cadena X ya aparece en un T()" sino "esta aparicion esta dentro de un
T()", que es lo unico que garantiza que se traduce.

    python tools/fr_motor.py                  el motor y el lector
    python tools/fr_motor.py <archivo>        otro archivo
"""
import io, os, re, subprocess, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_E = r"C:\Projects\nis-portal\nis-fun\engine"
ARCHIVOS = [os.path.join(_E, f) for f in
            ("index.html", "banner.js", "magicbox.js", "screens.js",
             "recorder.js", "orientacion.js", "backend.js")] + \
           [r"C:\Projects\nis-portal\nis-fun\readers\index.html"]

# Lo que deja un ${...} al quitarlo. Un caracter de uso privado y no "\u2026":
# el texto de verdad lleva puntos suspensivos y confundirlos borra rotulos.
HUECO = "\ue000"

# Lo que no es prosa: clases, ids, selectores, rutas, eventos, claves.
# Anclado por los dos lados a proposito: sin el $ del final, el "/" de
# "0 / 10 - well done!" valia como ruta y se tragaba el rotulo entero.
NO_ES_TEXTO = re.compile(
    r"^(?:[a-z0-9_-]+|[.#][\w-]+|https?:\S*|\.{0,2}/\S*|[\w-]+/\S*"
    r"|[\w-]+\.[a-z]{2,4}"
    # una clave de localStorage: nisfun-x-lastUnit. Un rotulo no se escribe
    # con guiones pegando palabras.
    r"|\w+(?:[-_]\w+)+)$")
# Una palabra de tres letras ya basta: hace falta para "${paper} Part ${n}",
# donde lo unico en ingles era ese "Part" suelto entre dos huecos.
FRASE = re.compile(r"[A-Za-z]{3,}")
# Codigo, no rotulo: una frase de interfaz no lleva punto y coma ni llaves.
CODIGO = re.compile(r"[`;={}()\[\]$|\\+*<>]|=>|\bfunction\b|\breturn\b")
# Una "d" de SVG no es texto: M120 146 Q400 26 700 104 T1260 46 L1260 -30 Z
SVG = re.compile(r"^[MmLlHhVvCcSsQqTtAaZz0-9 ,.+-]+$")
ENTIDAD = re.compile(r"&#?\w{1,8};")

# Nombres propios, marcas y cosas que no son idioma: fuentes, teclas y APIs
# del navegador. Se escriben igual en los dos idiomas o no las lee nadie.
MARCAS = {
    "Fun for Nordic", "Nordic", "Pip", "Nordic Little Readers",
    "Petits Lecteurs Nordic", "Portal", "Astrid", "Nico", "Freya",
    "· Nordic International School",     # el colegio se llama asi en frances
    "Baloo 2", "Source Sans 3", "SourceGraphic",
    "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Backspace",
    "Enter", "Escape", "IntersectionObserver", "ABC", "NFD",
    "#sdB- .sd-cell",                    # un selector, no un rotulo
    "Paolo Baca",                        # quien escribio los textos
}


def sin_comentarios(s):
    """Los comentarios se tapan con espacios: las posiciones no se mueven."""
    def tapa(m):
        return " " * (m.end() - m.start())
    s = re.sub(r"<!--.*?-->", tapa, s, flags=re.S)
    s = re.sub(r"/\*.*?\*/", tapa, s, flags=re.S)
    return re.sub(r"(?m)^\s*//.*$", tapa, s)


def sin_tablas_por_idioma(s):
    """Tapa las tablas que ya vienen duplicadas por idioma.

    La caja magica no se traduce con T(): tiene dos tablas, FAMILIAS y
    FAMILIAS_FR, porque no es el mismo contenido —"bigger/biggest" no
    existe en frances—. Pedirle T() a esas dos seria pedirle a la version
    francesa que dijera lo mismo, que es justo lo que no debe.

    Se reconocen solas: una tabla se salta si el archivo tiene su gemela
    con _FR. Una tercera tabla sin gemela seguiria saliendo en la lista.
    """
    for m in list(re.finditer(r"\bconst\s+([A-Z_][A-Z0-9_]*)\s*=\s*\[", s)):
        nombre = m.group(1)
        base = nombre[:-3] if nombre.endswith("_FR") else nombre
        if ("const %s_FR" % base) not in s or ("const %s " % base) not in s:
            continue
        i, nivel = m.end(), 1
        while i < len(s) and nivel:
            if s[i] == "[":
                nivel += 1
            elif s[i] == "]":
                nivel -= 1
            i += 1
        s = s[:m.end()] + " " * (i - m.end()) + s[i:]
    return s


def salta_expresion(s, i):
    """Desde el '{' de un ${, devuelve donde acaba (indice del '}')."""
    j, nivel = i + 1, 1
    while j < len(s) and nivel:
        if s[j] == "{":
            nivel += 1
        elif s[j] == "}":
            nivel -= 1
        j += 1
    return j - 1


def literales(s, base=0):
    """Cada cadena del archivo, leida como la leeria JavaScript.

    Devuelve (comilla, contenido, posicion). En las plantillas el ${...}
    viene sustituido por un hueco —"${n} more tries" tiene que quedar como
    una frase— y ademas se vuelve a mirar dentro, porque ahi hay mas texto:
    ${etiqueta || 'Listen'} pintaba un boton en ingles.
    """
    out, i, n, dentro = [], 0, len(s), []
    while i < n:
        c = s[i]
        if c not in "'\"`":
            i += 1
            continue
        j, cuerpo = i + 1, []
        while j < n:
            d = s[j]
            if d == "\\":
                cuerpo.append(s[j + 1:j + 2])
                j += 2
                continue
            if c == "`" and d == "$" and s[j + 1:j + 2] == "{":
                k = salta_expresion(s, j + 1)
                dentro.append((s[j + 2:k], base + j + 2))
                cuerpo.append(HUECO)
                j = k + 1
                continue
            if d == c:
                break
            if d == "\n" and c != "`":
                break                       # comilla sin cerrar: no era una
            cuerpo.append(d)
            j += 1
        if j < n and s[j] == c:
            out.append((c, "".join(cuerpo), base + i + 1))
        i = j + 1
    for texto, pos in dentro:
        out.extend(literales(texto, pos))
    return out


def sueltas(s):
    """Texto entre etiquetas, con cada ${...} sustituido por un hueco.

    Y luego lo mismo dentro de cada ${...}: ahi vive el HTML condicional
    —${extra ? `<p>Careful…</p>` : ''}— que tambien pinta frases.
    """
    plano, dentro, i, n = [], [], 0, len(s)
    while i < n:
        k = s.find("${", i)
        if k < 0:
            plano.append(s[i:])
            break
        plano.append(s[i:k])
        j = salta_expresion(s, k + 1)
        dentro.append(s[k + 2:j])
        plano.append(" " + HUECO + " ")
        i = j + 1
    out = [m.group(1) for m in re.finditer(r">([^<>{}]{4,120})<", "".join(plano))]
    for e in dentro:
        out.extend(sueltas(e))
    return out


def tramos_de_T(s):
    """(inicio, fin) del contenido de cada argumento de cada T()."""
    def cadena(g):                       # la comilla de cierre es la suya
        return r"(['\"`])((?:\\.|(?!\%d)[^\\])*)\%d" % (g, g)
    fuera = []
    for m in re.finditer(r"\bT\(\s*" + cadena(1) + r"\s*,\s*" + cadena(3),
                         s, re.S):
        fuera.append((m.start(2), m.end(2)))
        fuera.append((m.start(4), m.end(4)))
    return fuera


def normaliza(t):
    t = ENTIDAD.sub(" ", t)                 # &#9654; Play  ->  " Play"
    t = t.replace(HUECO, " ")
    return re.sub(r"\s+", " ", t).strip(" .,:")


def como_ruta(t):
    """La misma cadena con el hueco pegado, para ver si es una ruta.

    `${CDIR}/${nivel}/index.json` con el hueco en blanco parece texto
    ("/ /index.json"); con el hueco pegado es lo que es: una ruta.
    """
    return normaliza(t.replace(HUECO, "x"))


def sospechosa(t, exige_mayuscula):
    ruta = como_ruta(t)
    t = normaliza(t)
    if not t or t in MARCAS:
        return None
    if exige_mayuscula and not re.match(r"[A-Z]", t):
        return None
    if not FRASE.search(t) or SVG.match(t) or CODIGO.search(t) \
            or NO_ES_TEXTO.match(t) or NO_ES_TEXTO.match(ruta):
        return None
    return t


def audita(ruta):
    s = sin_comentarios(io.open(ruta, encoding="utf-8", newline="").read())
    s = sin_tablas_por_idioma(s)
    tramos = tramos_de_T(s)
    traducida = lambda p: any(a <= p <= b for a, b in tramos)

    fuera = set()
    # el texto suelto entre etiquetas no lleva posicion; se compara por
    # contenido con lo que ya pasa por T()
    ya = set()
    for a, b in tramos:
        ya.add(normaliza(re.sub(r"\$\{[^{}]*\}", HUECO, s[a:b])))
    for t in sueltas(s):
        r = sospechosa(t, exige_mayuscula=False)
        if r and r not in ya:
            fuera.add(r)
    for comilla, t, pos in literales(s):
        if traducida(pos):
            continue
        r = sospechosa(t, exige_mayuscula=(comilla != "`"))
        if r:
            fuera.add(r)
    return sorted(fuera)


def sintaxis(ruta):
    """Que el archivo al menos cargue.

    Una traduccion mete apostrofes donde antes no habia —t’ecouter— y
    uno sin escapar cierra la cadena y tumba el archivo entero sin que la
    auditoria de idioma note nada: el rotulo estaba traducido, pero la
    grabadora no cargaba. Se comprueba aqui porque es el mismo paso.
    """
    if not ruta.endswith(".js"):
        return None
    try:
        r = subprocess.run(["node", "--check", ruta], capture_output=True,
                           text=True)
    except FileNotFoundError:
        return None                      # sin node no se puede comprobar
    return None if r.returncode == 0 else r.stderr.strip().split(chr(10))[0]


if __name__ == "__main__":
    objetivo = sys.argv[1:] or ARCHIVOS
    total = 0
    for f in objetivo:
        malas = audita(f)
        total += len(malas)
        roto = sintaxis(f)
        print("%s: %d sin T()%s" % (os.path.basename(f), len(malas),
                                    "  [NO CARGA]" if roto else ""))
        if roto:
            total += 1
            print("    ", roto)
        for t in malas:
            print("   ", t)
    sys.exit(1 if total else 0)
