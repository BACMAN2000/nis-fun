# -*- coding: utf-8 -*-
"""Genera la actividad de "encuentra las diferencias" para TODAS las unidades.

El generador a mano (build_spot_diff.py) lleva la escena escrita unidad por
unidad: sirve para las de muestra, pero no para 150. Aqui se compone sola a
partir de lo que ya sabemos de cada unidad: su tema elige el sitio del
campus, y encima se colocan los ninos del nivel y objetos del banco de
dibujos 3D.

Las diferencias no salen del vocabulario de la unidad a proposito. En el
examen YLE esta tarea se resuelve hablando de colores, cantidades, tamano y
posicion — "In A the ball is red, but in B it is blue" — que es lenguaje que
el alumno ya tiene. Asi cada unidad tiene su escena aunque su vocabulario
sea de verbos o de adjetivos, que no se pueden dibujar.

Salen entre diez y doce diferencias, de tipos distintos: color, cantidad
(una que falta y una que se repite), tamano, posicion y una volteada.

Todo es determinista: la misma unidad da siempre la misma escena, asi que
se puede volver a generar sin que cambie lo que ya vio un alumno.

Salida: assets/spot-diff/{nivel}-{n}-{A,B}.jpg y -diffs.json
        y la actividad F escrita en content/{nivel}/unit-NN.json

    python tools/build_spot_diff_auto.py              todas las que falten
    python tools/build_spot_diff_auto.py starters     solo un nivel
    python tools/build_spot_diff_auto.py starters/6   solo esa unidad
    python tools/build_spot_diff_auto.py --rehacer    tambien las ya hechas
"""
import io, json, glob, os, random, re, sys

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONDOS = os.path.join(ROOT, "assets", "scenes")
VOCAB = os.path.join(ROOT, "assets", "vocab")
CHARS = os.path.join(ROOT, "assets", "characters")
SALIDA = os.path.join(ROOT, "assets", "spot-diff")
CONTENT = os.path.join(ROOT, "content")

W, H = 900, 620
ANCHO_FINAL = 820          # a lo que se guardan, para no inflar el repo
NIVELES = ("starters", "movers", "flyers")

# Los ninos de cada nivel. La mascota (pip/luna/kili) se deja fuera: es la
# guia del curso y sale en todas las pantallas, no conviene de figurante.
ELENCO = {
    "starters": ["freya", "nico", "astrid", "tomas"],
    "movers":   ["erik", "valentina", "sofia", "mateo"],
    "flyers":   ["ingrid", "diego", "maya", "oliver"],
}


def slug(w):
    return re.sub(r"[^a-z0-9]+", "-", (w or "").lower().replace("'", "")).strip("-")


# ---------------------------------------------------------------- el sitio
# Mismo reparto que sceneFor() del motor, para que la escena de las
# diferencias pase en el mismo sitio que el resto de la unidad.
MAPA = [
    ("hockey",        "hockey sport football match team ball game of"),
    ("track",         "run athletic exercise race fit body face health hair tall strong"),
    ("library",       "librar book read stor writ letter spell alphabet biograph diary note"),
    ("classroom",     "school classroom lesson subject timetable homework study exam test "
                      "practice teacher pencil material"),
    ("mirador",       "beach sea ocean island boat fish swim sail geograph space sky star "
                      "planet world country weather season rain snow sunny cloud wind storm"),
    ("picnic-garden", "food fruit vegetable eat drink breakfast lunch dinner picnic meal "
                      "snack cook hungry thirst cake kitchen"),
    ("garden",        "garden plant flower tree farm countryside nature grow animal pet bird insect zoo"),
    ("chess-plaza",   "number count math quantit compar superlativ measure money price "
                      "how many how much more most less"),
    ("facade",        "town city place building street direction way map shop buy work job "
                      "travel transport holiday trip home house room bedroom furniture "
                      "chore clean live clothes wear"),
    ("entrance",      "hello welcome greet friend family people person name telephone phone "
                      "feel happy sad personal who"),
    ("amphitheater",  "review party celebrat music show concert birthday danc sing hobb free time screen"),
    # El laberinto es una vista aerea: un personaje de pie encima no pega.
    # Estas unidades van a las escaleras de "We are Nordic".
    ("mirador",       "game play toy prepos position where is behind between hide"),
    ("campus-hex",    "time clock hour day week month routine morning afternoon night often always frequen"),
]


def sitio(ud):
    t = " ".join(str(ud.get(k, "")) for k in ("topic", "title", "grammar")).lower()
    for escena, palabras in MAPA:
        if any(p in t for p in palabras.split()):
            return escena
    return "campus-hex"


# ------------------------------------------------------------ los dibujos
def banco():
    """Objetos dibujables, sin los que son personas: esos van de figurante."""
    gente = {"mother", "father", "sister", "brother", "baby", "grandma", "grandpa",
             "boy", "girl", "man", "woman", "friend", "teacher", "family"}
    hay = sorted(f[:-4] for f in os.listdir(VOCAB) if f.endswith(".png"))
    return [w for w in hay if w not in gente], gente


def carga(ruta, alto_px):
    im = Image.open(ruta).convert("RGBA")
    r = alto_px / im.height
    return im.resize((max(1, int(im.width * r)), max(1, alto_px)), Image.LANCZOS)


def gira_tono(im, grados):
    """Cambia el color y respeta la forma. Vectorizado: se llama mucho."""
    a = np.asarray(im, dtype=np.float32) / 255.0
    rgb, alfa = a[..., :3], a[..., 3:]
    mx = rgb.max(-1); mn = rgb.min(-1); dif = mx - mn
    sat = np.where(mx > 0, dif / np.maximum(mx, 1e-6), 0)

    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    d = np.maximum(dif, 1e-6)
    h = np.zeros_like(mx)
    h = np.where(mx == r, ((g - b) / d) % 6, h)
    h = np.where(mx == g, (b - r) / d + 2, h)
    h = np.where(mx == b, (r - g) / d + 4, h)
    h = (h / 6.0 + grados / 360.0) % 1.0

    i = np.floor(h * 6).astype(int) % 6
    f = h * 6 - np.floor(h * 6)
    p = mx * (1 - sat); q = mx * (1 - f * sat); t = mx * (1 - (1 - f) * sat)
    out = np.stack([
        np.choose(i, [mx, q, p, p, t, mx]),
        np.choose(i, [t, mx, mx, q, p, p]),
        np.choose(i, [p, p, t, mx, mx, q]),
    ], -1)
    # el gris y el blanco no se tocan: si no, la escena entera se tine
    quieto = (sat < 0.18)[..., None]
    out = np.where(quieto, rgb, out)
    return Image.fromarray((np.concatenate([out, alfa], -1) * 255).astype(np.uint8), "RGBA")


def sombra(base, im, cx, cy):
    """Una sombra corta bajo la figura para que no parezca pegada."""
    s = Image.new("RGBA", (im.width, max(6, im.height // 9)), (0, 0, 0, 0))
    ImageDraw.Draw(s).ellipse([im.width * .12, 0, im.width * .88, s.height - 1],
                              fill=(28, 38, 52, 60))
    base.alpha_composite(s, (cx - s.width // 2, cy + im.height // 2 - s.height // 2))


# ------------------------------------------------------------- la escena
# Sitios fijos, en tres bandas de profundidad, para que las figuras no se
# pisen. Lo que puede volar va arriba y lo demas se queda en el suelo: una
# ballena en el cielo distrae, y ademas asi el alumno puede decir donde
# esta cada cosa ("the kite is in the sky, the ball is on the ground").
VUELAN = {"kite", "rainbow", "sunny", "cloudy", "rainy", "snowy", "windy",
          "parrot", "weather", "hot", "cold"}

HUECOS_CHAR = [(.17, .62, .40), (.35, .64, .38), (.66, .63, .39), (.84, .61, .41)]
HUECOS_AIRE = [(.14, .24, .13), (.33, .18, .12), (.52, .22, .14),
               (.70, .17, .12), (.88, .23, .13)]
HUECOS_SUELO = [(.08, .86, .15), (.25, .90, .14), (.44, .87, .16),
                (.61, .91, .13), (.78, .88, .15), (.93, .85, .14),
                (.16, .74, .12), (.52, .75, .12), (.88, .73, .12)]
# donde puede aparecer o mudarse algo en la foto B
DESTINO_AIRE = [(.42, .30, .12), (.62, .33, .12)]
DESTINO_SUELO = [(.36, .78, .13), (.70, .80, .13), (.20, .82, .12)]


def destino(p, az, libre_char=None):
    """Adonde puede irse o repetirse una figura, sin salirse de su banda.

    Un nino movido a la banda del suelo saldria gigante y encima de otro,
    asi que se le manda al hueco de personaje que quedo sin usar."""
    if p["clase"] == "char":
        return (libre_char or (.50, .58))[:2]
    if p.get("vuela"):
        return az.choice(DESTINO_AIRE)[:2]
    return az.choice(DESTINO_SUELO)[:2]


def receta(lvl, n, ud, objetos_banco):
    """Decide quien sale, donde, y que cambia en la foto B."""
    az = random.Random("%s-%02d-diffs" % (lvl, n))

    ninos = az.sample(ELENCO[lvl], 3)
    sitios_char = az.sample(HUECOS_CHAR, 4)
    libre_char = sitios_char[3]                 # el hueco que nadie ocupa
    piezas = []
    for nom, (x, y, s) in zip(ninos, sitios_char[:3]):
        piezas.append({"id": "c-" + nom, "clase": "char", "nombre": nom,
                       "lvl": lvl, "x": x, "y": y, "s": s})

    # los objetos de la unidad que tengan dibujo van primero; el resto se
    # completa del banco, rotando para que no salgan siempre los mismos
    propios = []
    for w in ud.get("wordlist", []):
        p = w if isinstance(w, str) else w.get("w", "")
        if slug(p) in objetos_banco and slug(p) not in propios:
            propios.append(slug(p))
    resto = [o for o in objetos_banco if o not in propios]
    az.shuffle(resto)
    elegidos = (propios + resto)[:7]
    # que el cielo nunca quede vacio: si no salio nada que vuele, se cambia
    # el ultimo elegido por algo que si pueda
    if not any(o in VUELAN for o in elegidos):
        vuela = [o for o in objetos_banco if o in VUELAN]
        if vuela:
            elegidos[-1] = az.choice(vuela)

    aire = az.sample(HUECOS_AIRE, len(HUECOS_AIRE))
    suelo = az.sample(HUECOS_SUELO, len(HUECOS_SUELO))
    for nom in elegidos:
        banda = aire if nom in VUELAN else suelo
        if not banda:
            banda = suelo or aire
        x, y, s_ = banda.pop()
        piezas.append({"id": "o-" + nom, "clase": "obj", "nombre": nom,
                       "vuela": nom in VUELAN, "x": x, "y": y, "s": s_})

    # Diez diferencias, repartidas por tipo para que den juego al hablar.
    # Cada pieza cambia como mucho una vez: dos cambios sobre la misma
    # figura se leen como uno solo y el alumno solo puede pulsar una vez.
    obj = [p for p in piezas if p["clase"] == "obj"]
    chr_ = [p for p in piezas if p["clase"] == "char"]
    az.shuffle(obj); az.shuffle(chr_)
    bolsa = obj + chr_

    plan, i = [], 0

    def toma():
        nonlocal i
        p = bolsa[i % len(bolsa)]
        i += 1
        return p

    for _ in range(3):                                    # color
        plan.append(("color", toma(), az.choice([70, 120, 160, 200, 250])))
    plan.append(("quitar", toma(), None))                 # algo que falta
    plan.append(("quitar", toma(), None))
    for _ in range(2):                                    # algo repetido
        p = toma()
        plan.append(("duplicar", p, destino(p, az, libre_char)))
    plan.append(("tamano", toma(), az.choice([1.5, 1.6, 0.62])))
    p = toma()                                            # cambia de sitio
    plan.append(("mover", p, destino(p, az, libre_char)))
    plan.append(("espejar", toma(), None))                # mira al otro lado

    return {"fondo": sitio(ud), "piezas": piezas, "plan": plan}


def ruta_de(p):
    if p["clase"] == "char":
        for f in ("fullbody.png", "pose-01.png"):
            r = os.path.join(CHARS, p["lvl"], p["nombre"], f)
            if os.path.exists(r):
                return r
        return None
    r = os.path.join(VOCAB, p["nombre"] + ".png")
    return r if os.path.exists(r) else None


def monta(cfg, con_cambios):
    f = Image.open(os.path.join(FONDOS, cfg["fondo"] + ".jpg")).convert("RGB")
    e = max(W / f.width, H / f.height)
    f = f.resize((int(f.width * e), int(f.height * e)), Image.LANCZOS)
    x0 = (f.width - W) // 2; y0 = (f.height - H) // 2
    base = f.crop((x0, y0, x0 + W, y0 + H))
    # se aclara el fondo para que las figuras se despeguen
    base = Image.blend(base, Image.new("RGB", (W, H), "white"), 0.20).convert("RGBA")

    cambios = {}
    if con_cambios:
        for tipo, p, val in cfg["plan"]:
            cambios[p["id"]] = (tipo, val)

    zonas, extras = [], []
    # de fondo a primer plano, para que las figuras de delante tapen
    for p in sorted(cfg["piezas"], key=lambda q: q["y"]):
        tipo, val = cambios.get(p["id"], (None, None))
        if tipo == "quitar":
            zonas.append((p["x"], p["y"], p["s"]))
            continue
        r = ruta_de(p)
        if not r:
            continue
        alto = int(H * p["s"] * (val if tipo == "tamano" else 1))
        im = carga(r, alto)
        x, y = p["x"], p["y"]
        if tipo == "color":
            im = gira_tono(im, val)
        elif tipo == "espejar":
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        elif tipo == "mover":
            x, y = val
        elif tipo == "duplicar":
            extras.append((r, val[0], val[1], p["s"]))
        cx, cy = int(W * x), int(H * y)
        sombra(base, im, cx, cy)
        base.alpha_composite(im, (cx - im.width // 2, cy - im.height // 2))
        if tipo:
            zonas.append((x, y, p["s"]))

    for r, x, y, s in extras:
        im = carga(r, int(H * s))
        cx, cy = int(W * x), int(H * y)
        sombra(base, im, cx, cy)
        base.alpha_composite(im, (cx - im.width // 2, cy - im.height // 2))
        zonas.append((x, y, s))

    return base.convert("RGB"), zonas


# --------------------------------------------------- la actividad del JSON
TITULOS = [
    "Spot the differences!", "Look at A and B. What is different?",
    "Two pictures, many differences!", "A and B are not the same. Find out why!",
]


def pon_actividad(fichero, lvl, n, cuantas):
    d = json.load(io.open(fichero, encoding="utf-8"))
    acts = d.setdefault("activities", [])
    for a in acts:
        if a.get("type") == "spot_diff":
            return False                       # ya la tiene, no se toca
    letras = sorted(a.get("code", "") for a in acts if a.get("code"))
    siguiente = chr(ord(letras[-1]) + 1) if letras else "A"
    az = random.Random("%s-%02d-titulo" % (lvl, n))
    acts.append({
        "code": siguiente,
        "type": "spot_diff",
        "title": az.choice(TITULOS),
        "outputs": ["book", "digital"],
        "instructions": ("Look at picture A and picture B. Find the %d differences "
                         "and tell your partner about them." % cuantas),
        "data": {},
    })
    # por letra: el motor y el libro las ordenan asi, y el JSON debe cuadrar
    acts.sort(key=lambda a: a.get("code", ""))
    io.open(fichero, "w", encoding="utf-8", newline="\n").write(
        json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    return True


def una(lvl, n, fichero, objetos, rehacer):
    destino_json = os.path.join(SALIDA, "%s-%d-diffs.json" % (lvl, n))
    ud = json.load(io.open(fichero, encoding="utf-8"))
    if os.path.exists(destino_json) and not rehacer:
        return "ya estaba", 0

    cfg = receta(lvl, n, ud, objetos)
    a, _ = monta(cfg, False)
    b, zonas = monta(cfg, True)
    for im, cual in ((a, "A"), (b, "B")):
        if im.width > ANCHO_FINAL:
            im = im.resize((ANCHO_FINAL, round(im.height * ANCHO_FINAL / im.width)),
                           Image.LANCZOS)
        im.save(os.path.join(SALIDA, "%s-%d-%s.jpg" % (lvl, n, cual)),
                quality=82, optimize=True, progressive=True)

    vistas, limpio = set(), []
    for x, y, s in zonas:
        k = (round(x, 2), round(y, 2))
        if k in vistas:
            continue
        vistas.add(k)
        limpio.append({"x": round(x, 3), "y": round(y, 3), "r": round(s / 2, 3)})
    io.open(destino_json, "w", encoding="utf-8", newline="\n").write(
        json.dumps({"escena": cfg["fondo"], "zonas": limpio},
                   ensure_ascii=False, indent=1) + "\n")

    nueva = pon_actividad(fichero, lvl, n, len(limpio))
    return ("hecha" + (" + actividad" if nueva else "")), len(limpio)


if __name__ == "__main__":
    args = list(sys.argv[1:])
    rehacer = "--rehacer" in args
    solo = [a for a in args if "/" in a]              # p.ej. starters/6
    pedidos = ([a for a in args if a in NIVELES]
               or sorted({a.split("/")[0] for a in solo})
               or list(NIVELES))
    os.makedirs(SALIDA, exist_ok=True)
    objetos, _ = banco()
    print("banco de objetos: %d dibujos" % len(objetos))

    total, hechas, pocas = 0, 0, []
    for lvl in pedidos:
        for f in sorted(glob.glob(os.path.join(CONTENT, lvl, "unit-*.json"))):
            n = int(re.search(r"unit-(\d+)", f).group(1))
            if solo and ("%s/%d" % (lvl, n)) not in solo:
                continue
            total += 1
            estado, cuantas = una(lvl, n, f, objetos, rehacer or bool(solo))
            if estado.startswith("hecha"):
                hechas += 1
                if cuantas < 8:
                    pocas.append("%s u%d (%d)" % (lvl, n, cuantas))
        if not solo:
            print("  %-9s listo" % lvl)
    print("")
    print("%d unidades revisadas, %d escenas nuevas" % (total, hechas))
    if pocas:
        print("con menos de 8 diferencias:", ", ".join(pocas))
