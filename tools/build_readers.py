# -*- coding: utf-8 -*-
"""Los cuentos de Nordic Little Readers y sus ilustraciones.

La secuencia pide un libro por unidad, pero los titulos que nombra (The
Very Hungry Caterpillar, Dear Zoo, Flat Stanley, The BFG...) tienen
copyright vigente: no se pueden digitalizar ni adaptar. Siguen siendo
lectura de biblioteca en papel.

Estos cuentos son PROPIOS, con los personajes de Fun for Nordic, y cubren
el mismo objetivo de cada unidad: el alfabeto, las partes del cuerpo, los
animales de granja, la familia, la comida.

Estan escritos como se escriben los cuentos de esta edad — frase corta,
patron que se repite y algo que se acumula pagina a pagina — para que el
nino pueda leer la segunda pagina apoyandose en la primera.

Las ilustraciones se componen con los escenarios del campus y las figuras
3D que ya tiene el curso, con el mismo tratamiento de render que las
escenas de unidad.

Salida: readers/data/*.json  ·  readers/img/*.jpg  ·  readers/data/index.json

    python tools/build_readers.py
    python tools/build_readers.py g1-u3      solo uno
"""
import io, json, os, re, sys

from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONDOS = os.path.join(ROOT, "assets", "scenes")
VOCAB = os.path.join(ROOT, "assets", "vocab")
CHARS = os.path.join(ROOT, "assets", "characters")
DATA = os.path.join(ROOT, "readers", "data")
IMG = os.path.join(ROOT, "readers", "img")

W, H = 1200, 750


# ---------------------------------------------------------------- cuentos
# Cada pagina: la frase, el fondo, y quien o que sale y donde.
#   ("char:starters:freya:1", x, y, alto)   un personaje
#   ("ball", x, y, alto)                    un objeto del banco
from readers_flyers import CUENTOS_FLYERS
from readers_movers import CUENTOS_MOVERS
from readers_starters2 import CUENTOS_STARTERS2

CUENTOS = [
{
 "id": "g1-u1", "grado": "G1", "tema": 1, "nivel": "Pre-A1",
 "titulo": "Hello, Pip!",
 "objetivo": "Greetings and letters",
 "paginas": [
  {"t": "Hello! I am Freya.", "clave": ["hello"], "fondo": "entrance",
   "piezas": [("char:starters:freya:1", .50, .62, .56)]},
  {"t": "Hello! I am Nico.", "clave": ["hello"], "fondo": "entrance",
   "piezas": [("char:starters:nico:1", .50, .62, .56)]},
  {"t": "Look! A little bird.", "clave": ["bird"], "fondo": "garden",
   "piezas": [("char:starters:freya:2", .32, .64, .52),
              ("char:starters:pip:1", .68, .70, .30)]},
  {"t": "Hello, bird! What is your name?", "clave": ["name"], "fondo": "garden",
   "piezas": [("char:starters:freya:3", .34, .64, .52),
              ("char:starters:pip:3", .66, .70, .32)]},
  {"t": "My name is Pip. P - I - P!", "clave": ["name"], "fondo": "garden",
   "piezas": [("char:starters:pip:1", .50, .66, .40)]},
  {"t": "Hello, Pip! I am Astrid.", "clave": ["hello"], "fondo": "classroom",
   "piezas": [("char:starters:astrid:1", .34, .62, .54),
              ("char:starters:pip:2", .68, .70, .30)]},
  {"t": "Hello, Pip! I am Tomas.", "clave": ["hello"], "fondo": "classroom",
   "piezas": [("char:starters:tomas:1", .34, .62, .54),
              ("char:starters:pip:5", .68, .70, .30)]},
  {"t": "Hello, friends! Let's play!", "clave": ["friends"], "fondo": "labyrinth",
   "piezas": [("char:starters:freya:10", .20, .64, .50),
              ("char:starters:nico:10", .38, .65, .50),
              ("char:starters:astrid:10", .58, .64, .50),
              ("char:starters:tomas:10", .76, .65, .50),
              ("char:starters:pip:1", .92, .74, .26)]},
 ],
 "actividad": {"titulo": "Who is who?", "instruccion": "Tap the friend you hear.",
  "items": [{"palabra": "Freya", "img": "char:starters:freya:1"},
            {"palabra": "Nico", "img": "char:starters:nico:1"},
            {"palabra": "Astrid", "img": "char:starters:astrid:1"},
            {"palabra": "Pip", "img": "char:starters:pip:1"}]},
},
{
 "id": "g1-u2", "grado": "G1", "tema": 2, "nivel": "Pre-A1",
 "titulo": "Where Is My Bag?",
 "objetivo": "Classroom objects",
 "paginas": [
  {"t": "Nico is in the classroom.", "clave": ["classroom"], "fondo": "classroom",
   "piezas": [("char:starters:nico:4", .50, .62, .56)]},
  {"t": "Where is my bag?", "clave": ["bag"], "fondo": "classroom",
   "piezas": [("char:starters:nico:4", .36, .62, .54), ("suitcase", .72, .78, .22)]},
  {"t": "Is it a book? No!", "clave": ["book"], "fondo": "library",
   "piezas": [("char:starters:nico:2", .34, .62, .52), ("museum", .70, .74, .26)]},
  {"t": "Is it a ball? No!", "clave": ["ball"], "fondo": "classroom",
   "piezas": [("char:starters:nico:2", .34, .62, .52), ("ball", .70, .76, .24)]},
  {"t": "Is it a kite? No!", "clave": ["kite"], "fondo": "classroom",
   "piezas": [("char:starters:nico:5", .34, .62, .52), ("kite", .72, .40, .26)]},
  {"t": "Freya has my bag!", "clave": ["bag"], "fondo": "classroom",
   "piezas": [("char:starters:freya:8", .36, .62, .54), ("suitcase", .70, .74, .24)]},
  {"t": "Thank you, Freya!", "clave": ["thank"], "fondo": "classroom",
   "piezas": [("char:starters:nico:10", .36, .63, .54),
              ("char:starters:freya:1", .64, .63, .54)]},
  {"t": "Now we can read a book!", "clave": ["book", "read"], "fondo": "library",
   "piezas": [("char:starters:nico:6", .36, .66, .50),
              ("char:starters:freya:6", .64, .66, .50)]},
 ],
 "actividad": {"titulo": "Find the thing", "instruccion": "Tap the picture you hear.",
  "items": [{"palabra": "a ball", "img": "ball"}, {"palabra": "a kite", "img": "kite"},
            {"palabra": "a bag", "img": "suitcase"}, {"palabra": "a teddy", "img": "teddy"}]},
},
{
 "id": "g1-u3", "grado": "G1", "tema": 3, "nivel": "Pre-A1",
 "titulo": "Move Your Body!",
 "objetivo": "Body parts and actions",
 "paginas": [
  {"t": "This is my head.", "clave": ["head"], "fondo": "track",
   "piezas": [("char:starters:tomas:2", .50, .62, .58)]},
  {"t": "These are my arms.", "clave": ["arms"], "fondo": "track",
   "piezas": [("char:starters:tomas:1", .50, .62, .58)]},
  {"t": "These are my legs.", "clave": ["legs"], "fondo": "track",
   "piezas": [("char:starters:tomas:7", .50, .62, .58)]},
  {"t": "I can jump! One, two, three!", "clave": ["jump"], "fondo": "track",
   "piezas": [("char:starters:tomas:7", .34, .58, .56),
              ("char:starters:astrid:7", .66, .60, .54)]},
  {"t": "Pip can fly. Look at his wings!", "clave": ["fly"], "fondo": "mirador",
   "piezas": [("char:starters:pip:1", .50, .44, .34)]},
  {"t": "Can you run, Astrid? Yes, I can!", "clave": ["run"], "fondo": "track",
   "piezas": [("char:starters:astrid:7", .50, .62, .56)]},
  {"t": "My legs are tired now.", "clave": ["legs"], "fondo": "track",
   "piezas": [("char:starters:tomas:6", .50, .66, .50)]},
  {"t": "Clap your hands. Well done!", "clave": ["hands"], "fondo": "amphitheater",
   "piezas": [("char:starters:tomas:10", .30, .64, .52),
              ("char:starters:astrid:10", .52, .64, .52),
              ("char:starters:pip:1", .76, .72, .28)]},
 ],
 "actividad": {"titulo": "My body", "instruccion": "Tap the word you hear.",
  "items": [{"palabra": "head", "img": None}, {"palabra": "arms", "img": None},
            {"palabra": "legs", "img": None}, {"palabra": "hands", "img": None}]},
},
{
 "id": "g1-u4", "grado": "G1", "tema": 4, "nivel": "Pre-A1",
 "titulo": "The Noisy Farm",
 "objetivo": "Farm animals and their sounds",
 "paginas": [
  {"t": "Freya is at the farm.", "clave": ["farm"], "fondo": "garden",
   "piezas": [("char:starters:freya:1", .50, .62, .56)]},
  {"t": "A big animal says MOO.", "clave": ["animal"], "fondo": "garden",
   "piezas": [("char:starters:freya:5", .32, .62, .52), ("panda", .70, .72, .30)]},
  {"t": "A little animal says QUACK.", "clave": ["animal"], "fondo": "garden",
   "piezas": [("char:starters:freya:2", .32, .62, .52), ("penguin", .70, .74, .26)]},
  {"t": "Look! A parrot in the tree.", "clave": ["parrot"], "fondo": "garden",
   "piezas": [("char:starters:freya:2", .30, .64, .50), ("parrot", .70, .34, .24)]},
  {"t": "The parrot says HELLO!", "clave": ["parrot"], "fondo": "garden",
   "piezas": [("parrot", .50, .48, .34)]},
  {"t": "Hello! says Freya. Hello! says the parrot.", "clave": ["hello"], "fondo": "garden",
   "piezas": [("char:starters:freya:3", .32, .64, .52), ("parrot", .70, .42, .26)]},
  {"t": "Pip is not happy. That is MY word!", "clave": ["happy"], "fondo": "garden",
   "piezas": [("char:starters:pip:5", .50, .66, .38)]},
  {"t": "Hello, hello, hello! Everybody laughs.", "clave": ["hello"], "fondo": "garden",
   "piezas": [("char:starters:freya:10", .28, .64, .50), ("char:starters:pip:1", .52, .70, .30),
              ("parrot", .76, .44, .24)]},
 ],
 "actividad": {"titulo": "Farm animals", "instruccion": "Tap the animal you hear.",
  "items": [{"palabra": "a parrot", "img": "parrot"}, {"palabra": "a panda", "img": "panda"},
            {"palabra": "a penguin", "img": "penguin"}, {"palabra": "a lion", "img": "lion"}]},
},
{
 "id": "g1-u5", "grado": "G1", "tema": 5, "nivel": "Pre-A1",
 "titulo": "My Family Photo",
 "objetivo": "Family members",
 "paginas": [
  {"t": "This is my family photo.", "clave": ["family"], "fondo": "entrance",
   "piezas": [("char:starters:nico:8", .50, .62, .56)]},
  {"t": "This is my mum. She is kind.", "clave": ["mum"], "fondo": "entrance",
   "piezas": [("char:starters:nico:2", .30, .64, .50), ("mother", .68, .64, .48)]},
  {"t": "This is my dad. He is tall.", "clave": ["dad"], "fondo": "entrance",
   "piezas": [("char:starters:nico:2", .30, .64, .50), ("father", .68, .62, .52)]},
  {"t": "This is my sister. She is little.", "clave": ["sister"], "fondo": "entrance",
   "piezas": [("char:starters:nico:2", .30, .64, .50), ("sister", .68, .70, .40)]},
  {"t": "This is my grandma. She is happy.", "clave": ["grandma"], "fondo": "entrance",
   "piezas": [("char:starters:nico:2", .30, .64, .50), ("grandma", .68, .64, .46)]},
  {"t": "This is my grandpa. He is old.", "clave": ["grandpa"], "fondo": "entrance",
   "piezas": [("char:starters:nico:2", .30, .64, .50), ("grandpa", .68, .63, .48)]},
  {"t": "And this is my baby cousin!", "clave": ["baby"], "fondo": "entrance",
   "piezas": [("char:starters:nico:5", .30, .64, .50), ("baby", .68, .74, .32)]},
  {"t": "I love my family.", "clave": ["family"], "fondo": "entrance",
   "piezas": [("family", .50, .64, .52)]},
 ],
 "actividad": {"titulo": "My family", "instruccion": "Tap the person you hear.",
  "items": [{"palabra": "mum", "img": "mother"}, {"palabra": "dad", "img": "father"},
            {"palabra": "grandma", "img": "grandma"}, {"palabra": "baby", "img": "baby"}]},
},
{
 "id": "g1-u6", "grado": "G1", "tema": 6, "nivel": "Pre-A1",
 "titulo": "Pip Is Hungry",
 "objetivo": "Food words",
 "paginas": [
  {"t": "Pip is hungry.", "clave": ["hungry"], "fondo": "picnic-garden",
   "piezas": [("char:starters:pip:4", .50, .66, .40)]},
  {"t": "On Monday he eats one apple.", "clave": ["apple"], "fondo": "picnic-garden",
   "piezas": [("char:starters:pip:1", .34, .68, .34), ("red", .68, .74, .20)]},
  {"t": "On Tuesday he eats two bananas.", "clave": ["bananas"], "fondo": "picnic-garden",
   "piezas": [("char:starters:pip:1", .30, .68, .34), ("yellow", .62, .76, .18),
              ("yellow", .78, .74, .18)]},
  {"t": "On Wednesday he drinks milk.", "clave": ["milk"], "fondo": "picnic-garden",
   "piezas": [("char:starters:pip:3", .34, .68, .34), ("cold", .70, .72, .22)]},
  {"t": "But Pip is still hungry!", "clave": ["hungry"], "fondo": "picnic-garden",
   "piezas": [("char:starters:pip:5", .50, .66, .40)]},
  {"t": "On Friday the friends make a big cake.", "clave": ["cake"], "fondo": "picnic-garden",
   "piezas": [("char:starters:freya:8", .28, .64, .50), ("char:starters:astrid:8", .52, .64, .50),
              ("char:starters:pip:2", .78, .72, .30)]},
  {"t": "Pip eats the cake. Yum yum!", "clave": ["cake"], "fondo": "picnic-garden",
   "piezas": [("char:starters:pip:1", .50, .66, .42)]},
  {"t": "Now Pip is happy. Thank you, friends!", "clave": ["happy"], "fondo": "picnic-garden",
   "piezas": [("char:starters:freya:10", .26, .64, .50), ("char:starters:astrid:10", .50, .64, .50),
              ("char:starters:pip:6", .78, .72, .30)]},
 ],
 "actividad": {"titulo": "Food", "instruccion": "Tap the word you hear.",
  "items": [{"palabra": "an apple", "img": "red"}, {"palabra": "a banana", "img": "yellow"},
            {"palabra": "a cake", "img": None}, {"palabra": "milk", "img": "cold"}]},
},
]

# Los demas grados viven en su propio archivo: aqui dentro, con seis
# cuentos ya escritos, no se encontraba nada.
CUENTOS += CUENTOS_STARTERS2 + CUENTOS_MOVERS + CUENTOS_FLYERS



# ------------------------------------------------------------ ilustracion
def _orientaciones():
    """Hacia donde mira cada pose, leido de engine/orientacion.js.

    Es el mismo dato que usan el motor y las laminas de unidad: una sola
    lista, que si se copia acaba separandose."""
    import re
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


ORIENTACION = _orientaciones()


def mira_bien(im, quien, pose, x):
    """Voltea al personaje para que mire hacia dentro de la pagina.

    Freya decia "Look! A little bird" mirando al margen mientras Pip estaba
    al otro lado. En una ilustracion el que esta a la izquierda mira a la
    derecha, y al reves. Lo que esta de frente no se toca."""
    lado = ORIENTACION.get((quien, int(pose)))
    if not lado:
        return im
    hacia = "der" if x < .5 else "izq"
    return im.transpose(Image.FLIP_LEFT_RIGHT) if lado != hacia else im


def carga(nombre, alto):
    if nombre.startswith("char:"):
        _, lvl, quien, pose = nombre.split(":")
        for f in ("pose-%s.png" % pose.zfill(2), "fullbody.png", "pose-01.png"):
            r = os.path.join(CHARS, lvl, quien, f)
            if os.path.exists(r):
                im = Image.open(r).convert("RGBA")
                e = alto / im.height
                return im.resize((max(1, int(im.width * e)), alto), Image.LANCZOS)
        return None
    r = os.path.join(VOCAB, nombre + ".png")
    if not os.path.exists(r):
        return None
    im = Image.open(r).convert("RGBA")
    im.thumbnail((W, alto), Image.LANCZOS)
    return im


def ilustra(fondo, piezas):
    f = Image.open(os.path.join(FONDOS, fondo + ".jpg")).convert("RGB")
    e = max(W / f.width, H / f.height)
    f = f.resize((int(f.width * e), int(f.height * e)), Image.LANCZOS)
    x0, y0 = (f.width - W) // 2, (f.height - H) // 2
    base = f.crop((x0, y0, x0 + W, y0 + H))

    # el fondo, un poco fuera de foco y aclarado: en un cuento el que manda
    # es el personaje, no el sitio
    suave = base.filter(ImageFilter.GaussianBlur(W / 300.0))
    mask = Image.new("L", (W, H))
    px = mask.load()
    for y in range(H):
        v = int(255 * max(0.0, min(1.0, 1.15 - 1.4 * (y / H))))
        for x in range(W):
            px[x, y] = v
    base = Image.composite(suave, base, mask)
    base = Image.blend(base, Image.new("RGB", (W, H), "white"), 0.16).convert("RGBA")

    for nombre, x, y, s in sorted(piezas, key=lambda p: p[2]):
        im = carga(nombre, int(H * s))
        if im is not None and nombre.startswith("char:"):
            _, _, quien, pose = nombre.split(":")
            im = mira_bien(im, quien, pose, x)
        if im is None:
            continue
        cx, cy = int(W * x), int(H * y)
        sombra = Image.new("RGBA", (int(im.width * 1.2), max(10, im.height // 5)), (0, 0, 0, 0))
        ImageDraw.Draw(sombra).ellipse([0, 0, sombra.width - 1, sombra.height - 1],
                                       fill=(26, 36, 52, 52))
        sombra = sombra.filter(ImageFilter.GaussianBlur(sombra.height / 2.5))
        base.alpha_composite(sombra, (cx - sombra.width // 2,
                                      cy + im.height // 2 - sombra.height // 2))
        base.alpha_composite(im, (cx - im.width // 2, cy - im.height // 2))
    return base.convert("RGB")


def recorte(nombre, lado=220):
    """El dibujo suelto que sale en la actividad final."""
    im = carga(nombre, lado)
    if im is None:
        return None
    lienzo = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    lienzo.alpha_composite(im, ((lado - im.width) // 2, (lado - im.height) // 2))
    return lienzo


if __name__ == "__main__":
    os.makedirs(DATA, exist_ok=True)
    os.makedirs(IMG, exist_ok=True)
    solo = [a for a in sys.argv[1:] if not a.startswith("-")]

    indice = []
    for c in CUENTOS:
        if solo and c["id"] not in solo:
            continue
        paginas = []
        for k, p in enumerate(c["paginas"], 1):
            nombre = "%s-p%02d.jpg" % (c["id"], k)
            ilustra(p["fondo"], p["piezas"]).save(
                os.path.join(IMG, nombre), quality=86, optimize=True, progressive=True)
            paginas.append({"texto": p["t"], "clave": p.get("clave", []),
                            "img": "img/" + nombre})

        act = dict(c["actividad"])
        items = []
        for it in act["items"]:
            img = None
            if it.get("img"):
                r = recorte(it["img"])
                if r:
                    nombre = "%s-a-%s.png" % (c["id"], re.sub(r"[^a-z0-9]+", "-",
                                                              it["palabra"].lower()).strip("-"))
                    r.save(os.path.join(IMG, nombre), optimize=True)
                    img = "img/" + nombre
            items.append({"palabra": it["palabra"], "img": img})
        act["items"] = items

        d = {k: c[k] for k in ("id", "grado", "tema", "nivel", "titulo", "objetivo")}
        d["paginas"] = paginas
        d["actividad"] = act
        io.open(os.path.join(DATA, c["id"] + ".json"), "w", encoding="utf-8",
                newline="\n").write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")

        indice.append({"id": c["id"], "grado": c["grado"], "tema": c["tema"],
                       "nivel": c["nivel"], "titulo": c["titulo"],
                       "objetivo": c["objetivo"], "paginas": len(paginas),
                       "portada": paginas[0]["img"]})
        print("  %-7s %-22s %d paginas" % (c["id"], c["titulo"][:22], len(paginas)))

    # el indice se rehace con lo que haya en disco, no solo con lo generado
    todos = {}
    p_idx = os.path.join(DATA, "index.json")
    if os.path.exists(p_idx):
        for l in json.load(io.open(p_idx, encoding="utf-8")).get("libros", []):
            todos[l["id"]] = l
    for l in indice:
        todos[l["id"]] = l
    io.open(p_idx, "w", encoding="utf-8", newline="\n").write(
        json.dumps({"libros": [todos[k] for k in sorted(todos)]},
                   ensure_ascii=False, indent=1) + "\n")
    print("\n  %d cuentos en la estanteria" % len(todos))
