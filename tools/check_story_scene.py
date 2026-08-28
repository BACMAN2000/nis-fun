# -*- coding: utf-8 -*-
"""Comprueba que la ilustracion de una unidad ensena lo que cuenta su historia.

En Starters 1 la historia dice "three little cars" y en el dibujo habia un
solo coche. El alumno mira la imagen mientras lee, asi que cada cosa que
nombra el texto tiene que estar, y en la cantidad que dice.

Se leen las dos piezas de texto de la unidad:
  scene.intro    la historia de apertura
  scene.bubble   lo que dice el personaje en su bocadillo

De ahi se sacan tres cosas y se comparan con lo que el generador de escenas
coloca de verdad:

  los objetos   con cuantos ("a red ball" = 1, "three little cars" = 3)
  el sitio      si la historia pasa en la cocina del faro, el fondo no
                puede ser la fachada del colegio
  quien sale    los personajes que la historia nombra tienen que estar

El sitio y los personajes se anadieron el 27-ago-2026: Flyers 1 cuenta que
estan en la cocina del faro con las maletas abiertas y la lamina era la
fachada del colegio con la ropa flotando en fila. Solo mirando objetos eso
pasaba la revision.

Solo mira las unidades con texto escrito a mano: las demas llevan una
introduccion de plantilla que no nombra objetos concretos, asi que no puede
contradecir al dibujo.

    python tools/check_story_scene.py
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
sys.path.insert(0, os.path.join(ROOT, "tools"))

NUMEROS = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
           "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}

# plural -> singular, lo justo para el vocabulario de estos libros
def singular(p):
    if p.endswith("ies"):
        return p[:-3] + "y"
    if p.endswith("es") and p[:-2].endswith(("sh", "ch", "x", "s")):
        return p[:-2]
    if p.endswith("s") and not p.endswith("ss"):
        return p[:-1]
    return p


def menciones(texto, vocabulario):
    """{objeto: cuantos} segun lo que dice el texto."""
    pide = {}
    palabras = re.findall(r"[A-Za-z']+", texto.lower())
    for i, p in enumerate(palabras):
        base = singular(p)
        if base not in vocabulario:
            continue
        # el numero es la ultima palabra contable de las tres anteriores
        cuantos = 1
        for atras in palabras[max(0, i - 3):i][::-1]:
            if atras in NUMEROS:
                cuantos = NUMEROS[atras]
                break
        pide[base] = max(pide.get(base, 0), cuantos)
    return pide


# Que sitio ensena cada fondo. Si la historia nombra uno de estos sitios,
# el fondo de la escena tiene que ser de esa familia.
SITIOS = {
    "classroom":       ("classroom",),
    "library":         ("library",),
    "garden":          ("garden", "picnic-garden"),
    "picnic":          ("picnic-garden", "garden"),
    "playground":      ("chess-plaza", "campus-hex"),
    "track":           ("track",),
    "hockey":          ("hockey",),
    "zoo":             ("zoo",),
    "fjord":           ("picnic-garden", "garden", "mirador"),
    "lighthouse":      ("lighthouse-kitchen", "lighthouse"),
    "kitchen":         ("lighthouse-kitchen", "kitchen"),
    "funfair":         ("funfair",),
    "theatre":         ("theatre", "amphitheater"),
    "amphitheatre":    ("amphitheater",),
    "maze":            ("labyrinth",),
    # Estos no tienen fondo propio. Estan aqui solo para que una historia
    # que recorre varios sitios se reconozca como recorrido: Flyers 2 va
    # del museo al puente y al teatro, y no hay un fondo que sea los tres.
    "museum":          (),
    "bridge":          (),
    "airport":         (),
    "restaurant":      (),
    "stadium":         (),
    "castle":          (),
    "beach":           ("picnic-garden", "garden"),
    # el "mirador" del campus son escaleras: el mar solo se ve en estos
    "sea":             ("picnic-garden", "garden"),
}


def sitio_de(texto):
    """El sitio donde pasa la historia, si es uno solo.

    "Fjord Club" es el nombre del grupo, no un sitio, y se quita antes de
    mirar. Y si la historia nombra varios sitios no se exige ninguno: es
    un recorrido -Flyers 2 va del museo al puente y al teatro- y no hay
    un fondo que sea los tres."""
    t = texto.lower().replace("fjord club", "")
    if "lighthouse kitchen" in t or ("lighthouse" in t and "kitchen" in t):
        return "kitchen"
    vistos = [s for s in SITIOS if re.search(r"\b" + s + r"\b", t)]
    return vistos[0] if len(vistos) == 1 else None


def quien_sale(texto, personajes):
    """Los personajes del curso que la historia nombra."""
    t = texto.lower()
    return {q for q in personajes if re.search(r"\b" + re.escape(q) + r"\b", t)}


def elenco():
    """Los personajes que tienen dibujo, por su slug."""
    base = os.path.join(ROOT, "assets", "characters")
    fuera = set()
    for lvl in os.listdir(base):
        for quien in os.listdir(os.path.join(base, lvl)):
            fuera.add(quien)
    return fuera


def dibujables():
    """Lo que se puede poner en una escena: hay dibujo 3D para ello."""
    d = os.path.join(ROOT, "assets", "vocab")
    return {f[:-4] for f in os.listdir(d) if f.endswith(".png")}


# Palabras de la historia que piden que la lamina ensene ese tema. Si el
# texto habla del tiempo, el alumno tiene que ver el tiempo en el dibujo.
TEMAS_VISIBLES = {
    # "storm" fuera del patron: casi siempre es figurado -"a confetti storm",
    # "a stage, a storm and 500 people singing"- y llenaba el informe.
    "clima": (r"\b(weather|rain|rainy|sunny|snow|snowy|wind|windy|cloud|cloudy)\b",
              ("rainy", "sunny", "snowy", "windy", "cloudy", "weather", "rainbow",
               "umbrella", "hot", "cold")),
}


def orientaciones():
    """Hacia donde mira cada pose, del catalogo que usa todo el curso."""
    fuera = {}
    try:
        txt = io.open(os.path.join(ROOT, "engine", "orientacion.js"),
                      encoding="utf-8").read()
    except Exception:
        return fuera
    for m in re.finditer(r"'([a-z]+)/([a-z]+)':\s*\{([^}]*)\}", txt):
        for pose, lado in re.findall(r"(\d+)\s*:\s*'(izq|der)'", m.group(3)):
            fuera[(m.group(2), int(pose))] = lado
    return fuera


def senala_a_algo(piezas):
    """Quien senala tiene que tener algo a ese lado.

    Tras voltear, el personaje mira hacia dentro de la lamina; lo que este
    chequeo busca es que ahi haya efectivamente alguna pieza y no el vacio:
    senalar al aire se lee tan raro como senalar al margen."""
    ori = orientaciones()
    malos = []
    for nombre, px, py, ps in piezas:
        if not nombre.startswith("char:"):
            continue
        trozos = nombre.split(":")
        quien = trozos[1]
        # el formato es char:<quien>:<pose>; si viene otra cosa se deja pasar
        # en vez de romper el informe entero
        try:
            pose = int(trozos[2]) if len(trozos) > 2 else 1
        except ValueError:
            continue
        if (quien, pose) not in ori:
            continue                      # de frente: no senala a ningun lado
        hacia = "der" if px < .5 else "izq"
        hay = [n for n, x, *_ in piezas
               if n != nombre and ((x > px + .04) if hacia == "der" else (x < px - .04))]
        if not hay:
            malos.append("%s senala a la %s y no hay nada a ese lado"
                         % (quien, "derecha" if hacia == "der" else "izquierda"))
    return malos


TRAE_EL_FONDO = {}
NO_SALEN = {}


def revisa(escenas):
    """escenas = {'nivel/n': (fondo, [(objeto,x,y,s), ...])}"""
    problemas, sin_escena, decorado = [], [], []
    hay_dibujo = dibujables()
    hay_persona = elenco()
    for lvl in ("starters", "movers", "flyers"):
        carpeta = os.path.join(CONTENT, lvl)
        if not os.path.isdir(carpeta):
            continue
        for f in sorted(os.listdir(carpeta)):
            if not f.startswith("unit-"):
                continue
            d = json.load(io.open(os.path.join(carpeta, f), encoding="utf-8"))
            esc = d.get("scene") or {}
            texto = " ".join(x for x in (esc.get("intro"), esc.get("bubble")) if x)
            if not texto:
                continue
            vocab = set()
            for w in d.get("wordlist", []):
                vocab.add((w if isinstance(w, str) else w.get("w", "")).lower())
            # solo lo que se PUEDE dibujar: de los verbos y los adjetivos
            # del wordlist no hay figura, y no tiene sentido exigirlos
            pide = {k: v for k, v in menciones(texto, vocab).items() if k in hay_dibujo}
            clave = "%s/%d" % (lvl, d["number"])

            # El tema se mira SIEMPRE, aunque la historia no nombre ningun
            # objeto del banco: "black clouds over the sea, a big storm is
            # coming" no cita ninguna palabra dibujable y aun asi la lamina
            # tiene que ensenar el tiempo.
            for tema, (patron, dibujos) in TEMAS_VISIBLES.items():
                if not re.search(patron, texto.lower()):
                    continue
                if clave not in escenas:
                    decorado.append((clave, "habla del %s y la unidad no tiene "
                                            "lamina propia" % tema))
                else:
                    fondo_t, piezas_t = escenas[clave]
                    hay = {n for n, *_ in piezas_t} | set(TRAE_EL_FONDO.get(fondo_t, ()))
                    if not (hay & set(dibujos)):
                        decorado.append((clave, "habla del %s y el dibujo no "
                                                "ensena nada de eso" % tema))

            if not pide:
                continue

            # el sitio y el reparto se miran aunque la historia no nombre
            # ningun objeto dibujable
            if clave in escenas:
                fondo, piezas = escenas[clave]
                sitio = sitio_de(texto)
                if sitio and SITIOS[sitio] and fondo not in SITIOS[sitio]:
                    decorado.append((clave, "pasa en '%s' y el fondo es '%s'"
                                     % (sitio, fondo)))
                nombrados = quien_sale(texto, hay_persona)
                puestas = {n.split(":")[1] for n, *_ in piezas
                           if n.startswith("char:")}
                faltan = sorted(nombrados - puestas - set(NO_SALEN.get(clave, {})))
                if faltan:
                    decorado.append((clave, "la historia nombra a %s y no salen"
                                     % ", ".join(faltan)))

                # quien senala tiene que tener algo hacia donde senalar
                for aviso in senala_a_algo(piezas):
                    decorado.append((clave, aviso))


            if clave not in escenas:
                sin_escena.append((clave, sorted(pide)))
                continue
            puestos = {}
            for nombre, *_ in (escenas.get(clave) or ("", []))[1]:
                puestos[nombre] = puestos.get(nombre, 0) + 1
            # lo que el fondo ya trae dibujado cuenta como puesto
            for obj in TRAE_EL_FONDO.get(escenas[clave][0], ()):
                puestos[obj] = puestos.get(obj, 0) + 1

            # "the ducks" no dice cuantos: con dos en el dibujo la historia se
            # cumple. Solo se exige el numero exacto cuando el texto lo dice
            # ("three little cars").
            plural = {p_.rstrip("s") for p_ in re.findall(r"[A-Za-z]+s\b", texto.lower())}
            for obj, cuantos in sorted(pide.items()):
                hay = puestos.get(obj, 0)
                if hay == 0:
                    problemas.append((clave, obj, cuantos, 0, "no esta en el dibujo"))
                elif hay < cuantos:
                    problemas.append((clave, obj, cuantos, hay, "faltan"))
                elif hay > cuantos and obj not in plural:
                    problemas.append((clave, obj, cuantos, hay, "cantidad distinta"))
    return problemas, sin_escena, decorado


if __name__ == "__main__":
    import build_unit_scenes as B
    globals()["TRAE_EL_FONDO"] = B.TRAE_EL_FONDO
    globals()["NO_SALEN"] = B.NO_SALEN
    fallos, sin_escena, decorado = revisa(B.ESCENAS)
    if not fallos:
        print("  todo cuadra: lo que cuenta cada historia esta en su dibujo")
    else:
        print("  %d desajustes entre la historia y el dibujo:" % len(fallos))
        for clave, obj, pide, hay, que in fallos:
            print("   %-12s %-10s la historia dice %d, el dibujo tiene %d  (%s)"
                  % (clave, obj, pide, hay, que))
    if decorado:
        print("")
        print("  %d laminas que no cuadran con lo que cuenta la historia:"
              % len(decorado))
        for clave, que in decorado:
            print("   %-12s %s" % (clave, que))
    if sin_escena:
        print("")
        print("  %d unidades nombran cosas que si se pueden dibujar pero"
              " todavia no tienen escena propia:" % len(sin_escena))
        for clave, objs in sin_escena[:14]:
            print("   %-12s %s" % (clave, ", ".join(objs)))
        if len(sin_escena) > 14:
            print("   ... y %d mas" % (len(sin_escena) - 14))
    raise SystemExit(1 if fallos else 0)
