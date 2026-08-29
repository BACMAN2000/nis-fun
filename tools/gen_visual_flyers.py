# -*- coding: utf-8 -*-
"""Anade a cada unidad de Flyers las cuatro tareas VISUALES del examen A2.

El curso tenia todo el peso en texto: crossword, match_words, listening con
huecos, exam_task, pairwork y spot_diff. Los formatos del examen que se
resuelven MIRANDO no estaban:

    label_people    Listening Part 1   escribir el nombre debajo de cada persona
    picture_mc      Listening Part 4   escuchar y marcar 1 de 3 imagenes
    match_pictures  Listening Part 3   emparejar a cada explorador con A-H
    picture_story   R&W Part 7         escribir la historia de tres vinetas

De Cambridge se copia el TIPO de tarea, que es formato publico. El dibujo es
nuestro: los personajes de characters/bible.md, los escenarios de
assets/scenes y el arte de vocabulario de engine/vocab-art.js. Ninguna
ilustracion de Fun for Flyers entra aqui.

Reglas que no se rompen (si se editan las actividades a mano, respetarlas):

  - Solo entran personajes de content/cast-flyers.json, y solo con poses que
    existen en disco. Una pose inventada es un 404 y un hueco en la lamina.
  - Solo se dibujan palabras que tengan dibujo propio o emoji. Si una unidad
    no reune suficientes, la actividad NO se genera: media lamina en blanco
    ensena menos que no ponerla.
  - La respuesta aparece literalmente en el guion del audio.
  - Sin comillas dobles en los textos: viajan dentro de atributos data-.
  - El codigo de actividad se calcula, no se fija: hay unidades que ya llegan
    hasta la G o la H y las nuevas irian encima.

Idempotente y determinista (la semilla es el numero de unidad):

    python tools/gen_visual_flyers.py            # escribe
    python tools/gen_visual_flyers.py --dry      # solo informa
"""
import glob
import io
import json
import os
import random
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENIDO = os.path.join(RAIZ, "content", "flyers")
NUEVOS = ("label_people", "picture_mc", "match_pictures", "picture_story")

DRY = "--dry" in sys.argv


def lee(ruta):
    return json.load(io.open(ruta, encoding="utf-8"))


CAST = lee(os.path.join(RAIZ, "content", "cast-flyers.json"))
PERS = CAST["personajes"]
LUGARES = CAST["lugares"]
LUGAR_TEMA = CAST["lugar_por_tema"]


# ---------------------------------------------------------------------------
# Que palabras se pueden dibujar
#
# Tres fuentes, en este orden: SVG propio, PNG propio, emoji. Las dos primeras
# son arte de la escuela; el emoji es el respaldo que el motor ya usa en la
# pantalla de vocabulario, asi que una actividad con emoji no desentona.
# ---------------------------------------------------------------------------
def _claves_svg():
    t = io.open(os.path.join(RAIZ, "engine", "vocab-art.js"), encoding="utf-8").read()
    k = set(re.findall(r"A\.([a-z][a-z0-9_]*)\s*=", t))
    k |= set(re.findall(r'A\["([^"]+)"\]\s*=', t))
    k |= set(re.findall(r"A\['([^']+)'\]\s*=", t))
    return k


def _claves_png():
    return {os.path.splitext(os.path.basename(p))[0]
            for p in glob.glob(os.path.join(RAIZ, "assets", "vocab", "*.png"))}


def _claves_emoji():
    t = io.open(os.path.join(RAIZ, "engine", "emoji-map.js"), encoding="utf-8").read()
    m = {}
    for g in re.finditer(r"(?:'([^']+)'|\"([^\"]+)\"|([A-Za-z_][\w'-]*))\s*:\s*'([^']+)'", t):
        m[(g.group(1) or g.group(2) or g.group(3)).strip().lower()] = g.group(4)
    return m


SVG = _claves_svg()
PNG = _claves_png()
EMOJI = _claves_emoji()


def slug(w):
    return re.sub(r"[^a-z0-9]+", "-", str(w).lower().replace("'", "")).strip("-")


def limpia(w):
    return re.sub(r"^(a|an|the) ", "", str(w).strip().lower())


def hay_dibujo(w):
    k = limpia(w)
    return k in SVG or slug(k) in PNG or k in EMOJI


def arte_propio(w):
    k = limpia(w)
    return k in SVG or slug(k) in PNG


# Palabras que no son objetos: un dibujo de "already" no existe, y
# "is holding an empty" no es ingles.
NO_OBJETO = re.compile(
    r"^(a|an|the|and|or|but|because|already|always|never|often|sometimes|"
    r"again|along|back|badly|best|better|worse|worst|both|each|every|few|"
    r"many|much|more|most|less|enough|quite|really|very|too|also|even|only|"
    r"just|still|yet|soon|later|early|late|then|now|today|tomorrow|yesterday|"
    r"here|there|where|when|why|how|who|which|what|whose|"
    r"january|february|march|april|may|june|july|august|september|october|"
    r"november|december|monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
    r"add|agree|answer|arrive|arrived|belong|bring|brought|carry|carried|"
    r"catch|caught|change|choose|chose|climb|close|come|came|cook|cry|cut|"
    r"dance|decide|die|do|draw|drew|drink|drank|drive|drove|drop|eat|ate|"
    r"fall|fell|feel|felt|find|found|finish|fly|flew|forget|forgot|get|got|"
    r"give|gave|go|went|grow|grew|happen|hate|have|had|hear|heard|help|hide|"
    r"hit|hold|held|hope|hurt|invite|join|jump|keep|kept|kick|know|knew|"
    r"laugh|learn|leave|left|let|like|listen|live|look|lose|lost|love|make|"
    r"made|mean|meet|met|miss|move|need|open|paint|pick|play|point|prefer|"
    r"pull|push|put|read|remember|ride|rode|ring|rang|run|ran|say|said|see|"
    r"saw|sell|sold|send|sent|show|sing|sang|sit|sat|sleep|slept|smile|speak|"
    r"spoke|spell|spend|stand|stood|start|stay|stop|swim|swam|take|took|talk|"
    r"teach|taught|tell|told|think|thought|throw|threw|try|turn|understand|"
    r"use|visit|wait|wake|walk|want|watch|wear|wore|win|won|work|worry|write|wrote|"
    r"afraid|angry|ancient|beautiful|big|biggest|boring|brave|busy|clean|clever|"
    r"cold|cool|dangerous|dark|deep|dear|dirty|dry|easy|empty|excited|exciting|"
    r"expensive|famous|fast|fat|favourite|free|friendly|frightened|full|funny|"
    r"good|great|happy|hard|healthy|heavy|high|hot|hungry|important|interesting|"
    r"kind|large|light|long|loud|lovely|lucky|new|next|nice|noisy|old|other|"
    r"poor|pretty|proud|quick|quiet|ready|rich|right|sad|safe|same|scared|"
    r"short|shy|sick|silly|slow|small|soft|sorry|special|strong|sure|sweet|"
    r"tall|terrible|thin|thirsty|tidy|tired|ugly|useful|warm|weak|well|wet|"
    r"wide|wild|wonderful|wrong|young)$"
)


# Incontables: no admiten "a/an" ni cuentan como una cosa que se dibuja
# sola. Se quedan fuera de los marcos ("a news" no existe).
INCONTABLES = {
    "news", "weather", "money", "information", "homework", "music", "water",
    "milk", "bread", "rice", "hair", "advice", "food", "fun", "help", "time",
    "work", "sugar", "salt", "snow", "rain", "traffic", "luggage", "furniture",
}


def dibujable(w):
    k = limpia(w)
    return (bool(k) and k not in INCONTABLES and not NO_OBJETO.match(k)
            and hay_dibujo(k) and len(k) <= 22)


def primero_lo_nuestro(lista):
    """Delante las palabras con dibujo PROPIO, detras las de emoji.

    Una lamina del examen no mezcla estilos. Si de ocho imagenes siete son
    nuestro arte 3D y la octava es un emoji del sistema, la octava canta. No
    siempre se puede evitar -- solo hay 69 palabras con dibujo propio de las
    511 de Flyers -- pero cuando hay donde elegir, se elige."""
    return sorted(lista, key=lambda w: not arte_propio(w))


def art_ref(w):
    """Como referenciar el dibujo. El motor resuelve en este orden."""
    k = limpia(w)
    return {"word": k, "propio": arte_propio(k)}


# Sustantivos que acaban en -s y NO son plurales. Sin esta lista, "a glass"
# salia como "some glass".
FALSOS_PLURALES = {
    "glass", "dress", "bus", "class", "address", "grass", "chess", "press",
    "gas", "circus", "octopus", "christmas", "tennis", "gymnastics",
    "boss", "cross", "kiss", "mouse", "house", "horse", "nurse", "purse",
    "cheese", "nose", "police", "ice", "juice", "office", "face", "place",
}


def articulo(w):
    """a / an / some, por sonido y por numero.

    Tres cosas que se veian mal antes: "a umbrella" (se elige por sonido, no
    por letra), "an uniform" (uni- suena /ju/ y lleva 'a') y "a socks", que es
    la que mas chirriaba: la wordlist de Flyers esta llena de plurales."""
    k = limpia(w)
    if k.endswith("s") and not k.endswith("ss") and not k.endswith("us")             and k not in FALSOS_PLURALES:
        return "some"
    return "an" if k[:1] in "aeiou" and not k.startswith("uni") else "a"


# ---------------------------------------------------------------------------
# Reparto: quien sale en esta unidad
# ---------------------------------------------------------------------------
COMPANEROS = [s for s, p in PERS.items() if not p.get("principal") and p["tipo"] != "monstruo"]
PRINCIPALES = [s for s, p in PERS.items() if p.get("principal")]


def elenco(ud, rnd, cuantos):
    """Los de la unidad primero; el resto se completa con companeros.

    Un companero de clase no cambia la historia y da variedad de rostros,
    que es justo lo que Listening Part 1 necesita: cinco caras distintas
    que se puedan describir sin ambiguedad.
    """
    propios = [c for c in (ud.get("characters") or []) if c in PERS]
    if ud.get("number") == 24:
        propios += ["grum", "zog", "zip"]
    resto = [c for c in COMPANEROS + PRINCIPALES if c not in propios]
    rnd.shuffle(resto)
    fuera = set()
    for s, p in PERS.items():
        u = p.get("solo_unidades")
        if u and ud.get("number") not in u:
            fuera.add(s)
    orden = [c for c in propios + resto if c not in fuera or c in propios]
    return orden[:cuantos]


def pose(slug_p, rnd, prefiere=None):
    disp = PERS[slug_p]["poses"]
    for p in (prefiere or []):
        if p in disp:
            return p
    return rnd.choice(disp)


def en_el(sitio):
    """in the classroom, pero at the school entrance.

    La biblia de lugares ya marca cuales son interiores; sin esto salian
    frases como "in the school entrance", que no dice nadie."""
    return "%s %s" % ("in" if LUGARES[sitio].get("dentro") else "at", LUGARES[sitio]["en"])


def el_ella(slug_p):
    """he / she. "because Ingrid looks bored" repite el nombre tres veces
    en una historia de veinte palabras; con el pronombre se lee mejor."""
    return "she" if PERS[slug_p]["tipo"] == "nina" else "he"


def pronombre(w):
    """it / them. "Ingrid shows it to Bruno" con unos guantes chirria."""
    return "them" if articulo(w) == "some" else "it"


def lugar(ud, rnd):
    tema = str((ud.get("scope") or {}).get("temaN") or 1)
    opciones = LUGAR_TEMA.get(tema) or list(LUGARES)
    opciones = [l for l in opciones if l in LUGARES]
    return rnd.choice(opciones)


# ---------------------------------------------------------------------------
# KPI: a que clase de 5.º sirve cada actividad
#
# Sin esto la actividad es preparacion de examen suelta, que es exactamente
# lo que direccion no quiere. Con esto cada tarea dice de que unidad del
# Scope & Sequence de G5 sale y que outcome cubre.
# ---------------------------------------------------------------------------
CLASE = {
    "label_people":   ("Listening", "Flyers-style: listen and label the people in the picture"),
    "picture_mc":     ("Listening", "Flyers-style: listen and tick the right picture"),
    "match_pictures": ("Listening", "Flyers-style: listen and match each person to a picture"),
    "picture_story":  ("Writing",   "Flyers-style: 20-25-word picture story (Writing Part 3)"),
}
PARTE = {
    "label_people":   ("Listening", 1),
    "picture_mc":     ("Listening", 4),
    "match_pictures": ("Listening", 3),
    "picture_story":  ("Reading & Writing", 7),
}


def kpi(ud, tipo):
    sc = ud.get("scope") or {}
    destreza, clase = CLASE[tipo]
    puede = ""
    for o in sc.get("outcomes") or []:
        if o.get("destreza") == destreza:
            puede = o.get("puede", "")
            break
    paper, parte = PARTE[tipo]
    return {
        "grado": sc.get("grado", "G5"),
        "cefr": CAST["cefr"],
        "examen": CAST["examen"],
        "tema": {"n": sc.get("temaN"), "nombre": sc.get("tema")},
        "destreza": destreza,
        "puede": puede,
        "clase": clase,
        "examen_parte": {"paper": paper, "part": parte},
    }


# ---------------------------------------------------------------------------
# F. label_people  --  Listening Part 1
# ---------------------------------------------------------------------------
def label_people(ud, rnd):
    gente = elenco(ud, rnd, 5)
    if len(gente) < 4:
        return None
    sitio = lugar(ud, rnd)

    personas = []
    for s in gente:
        p = PERS[s]
        personas.append({
            "slug": s,
            "name": p["nombre"],
            "pose": pose(s, rnd, [7, 3, 1, 6]),
            "clue": p["rasgo"],
            "action": p["accion"],
        })

    # Tres nombres de mas. Cambridge siempre deja nombres sin usar: obliga a
    # escuchar entero en vez de repartir por eliminacion.
    sobran = [PERS[s]["nombre"] for s in PERS
              if s not in gente and PERS[s]["tipo"] != "monstruo"]
    rnd.shuffle(sobran)
    banco = sorted([p["name"] for p in personas] + sobran[:3])

    lineas = ["Look at the picture. Listen and write the names. There is one example."]
    ej = personas[0]
    lineas.append("Diego: Who is that in %s? %s" % (LUGARES[sitio]["en"], ej["clue"].capitalize() + "."))
    lineas.append("Maya: That is %s. %s %s." % (ej["name"], ej["name"], ej["action"]))
    for p in personas[1:]:
        lineas.append("Diego: And who is %s?" % p["clue"])
        # el nombre se dice dos veces a proposito: en el examen la respuesta
        # siempre se oye repetida, para que quepa escribirla
        lineas.append("Maya: That is %s. Look, %s %s." % (p["name"], p["name"], p["action"]))
    guion = " … ".join(lineas).replace('"', "")

    return {
        "type": "label_people",
        "title": "Listen and write the names.",
        "instructions": "Look at the picture. Listen and write the name under each person. Careful: there are three names you do not need.",
        "outputs": ["digital"],
        "kpi": kpi(ud, "label_people"),
        "audio": "flyers/u%02d-%s.mp3" % (ud["number"], "{code}"),
        "data": {
            "scene": sitio,
            "place": LUGARES[sitio]["en"],
            "people": personas,
            "names": banco,
            "script": guion,
            "voice_note": "Voces: Diego (nino, reportero) pregunta y Maya (nina, cientifica) responde.",
        },
    }


# ---------------------------------------------------------------------------
# G. picture_mc  --  Listening Part 4
# ---------------------------------------------------------------------------
# Marcos de pregunta.
#
# Todos tienen que funcionar con CUALQUIER sustantivo de la lista, porque el
# generador no sabe si la palabra es algo que se lleva encima. Con marcos de
# llevar o necesitar salian frases imposibles ("I need a pocket, please"): se
# quedan solo los de ver, senalar, decir y dibujar, que valen para todo.
MARCOS = [
    ("What can {n} see in the picture?", "{n}: I can see the {w}."),
    ("What is {n} pointing at?",         "{n}: I am pointing at the {w}."),
    ("What is {n} talking about?",       "{n}: I am talking about the {w}."),
    ("Which word is {n} learning today?", "{n}: Today I am learning the word {w}."),
    ("What has {n} drawn?",              "{n}: I have drawn {a} {w}."),
    ("Which picture is {n} looking at?", "{n}: I am looking at the {w}."),
]


def picture_mc(ud, rnd, otras_palabras):
    buenas = [w for w in (ud.get("wordlist") or []) if dibujable(w)]
    if len(buenas) < 3:
        return None
    rnd.shuffle(buenas)
    buenas = primero_lo_nuestro(buenas)[:5]

    gente = [s for s in elenco(ud, rnd, 6) if PERS[s]["tipo"] in ("nino", "nina")]
    if not gente:
        return None

    preguntas = []
    for i, w in enumerate(buenas):
        w = limpia(w)
        distractores = [d for d in otras_palabras if d != w and dibujable(d)]
        rnd.shuffle(distractores)
        # los del propio tema primero: distinguir umbrella de scarf ensena mas
        # que distinguir umbrella de elephant
        cerca = [d for d in (ud.get("wordlist") or []) if limpia(d) != w and dibujable(d)]
        rnd.shuffle(cerca)
        dos = primero_lo_nuestro(cerca + distractores)[:2]
        if len(dos) < 2:
            continue
        nombre = PERS[gente[i % len(gente)]]["nombre"]
        preg, resp = MARCOS[(ud["number"] + i) % len(MARCOS)]
        opciones = [art_ref(w)] + [art_ref(d) for d in dos]
        rnd.shuffle(opciones)
        preguntas.append({
            "q": preg.format(n=nombre),
            "answer": w,
            "options": opciones,
            "script": (preg.format(n=nombre) + " … "
                       + resp.format(n=nombre, a=articulo(w), w=w)).replace('"', ""),
        })
    if len(preguntas) < 3:
        return None

    guion = ("Listen and tick the box. There is one example. … "
             + " … ".join(q["script"] for q in preguntas))
    return {
        "type": "picture_mc",
        "title": "Listen and tick the box.",
        "instructions": "Listen to each question and click the picture that answers it.",
        "outputs": ["digital"],
        "kpi": kpi(ud, "picture_mc"),
        "audio": "flyers/u%02d-%s.mp3" % (ud["number"], "{code}"),
        "data": {"questions": preguntas, "script": guion,
                 "voice_note": "Una voz por pregunta; la respuesta se dice entera."},
    }


# ---------------------------------------------------------------------------
# H. match_pictures  --  Listening Part 3
# ---------------------------------------------------------------------------
LETRAS = "ABCDEFGH"


def match_pictures(ud, rnd, otras_palabras):
    buenas = [limpia(w) for w in (ud.get("wordlist") or []) if dibujable(w)]
    buenas = list(dict.fromkeys(buenas))
    if len(buenas) < 4:
        return None
    rnd.shuffle(buenas)
    usadas = primero_lo_nuestro(buenas)[:5]

    extra = [d for d in otras_palabras if d not in usadas and dibujable(d)]
    rnd.shuffle(extra)
    extra = primero_lo_nuestro(extra)[:8 - len(usadas)]
    if len(usadas) + len(extra) < 6:
        return None

    gente = [s for s in elenco(ud, rnd, 8) if PERS[s]["tipo"] in ("nino", "nina")][:len(usadas)]
    if len(gente) < len(usadas):
        usadas = usadas[:len(gente)]

    fotos = [art_ref(w) for w in usadas + extra]
    rnd.shuffle(fotos)
    for i, f in enumerate(fotos):
        f["id"] = LETRAS[i]
    donde = {f["word"]: f["id"] for f in fotos}

    personas, respuestas, lineas = [], {}, [
        "Listen and match each person to a picture. There is one example.",
    ]
    for s, w in zip(gente, usadas):
        p = PERS[s]
        personas.append({"slug": s, "name": p["nombre"], "pose": pose(s, rnd, [8, 3, 1])})
        respuestas[p["nombre"]] = donde[w]
        # "which picture did you choose" vale para cualquier sustantivo;
        # "I have got a pocket" no es una frase que nadie diga.
        lineas.append("Diego: %s, which picture did you choose? … %s: I chose the %s."
                      % (p["nombre"], p["nombre"], w))

    return {
        "type": "match_pictures",
        "title": "Listen and match each explorer to a picture.",
        "instructions": "Listen. Then choose the letter of the picture for each person. Careful: some pictures are extra.",
        "outputs": ["digital"],
        "kpi": kpi(ud, "match_pictures"),
        "audio": "flyers/u%02d-%s.mp3" % (ud["number"], "{code}"),
        "data": {
            "people": personas,
            "pictures": fotos,
            "answers": respuestas,
            "script": " … ".join(lineas).replace('"', ""),
            "voice_note": "Diego pregunta; cada explorador responde con su objeto.",
        },
    }


# ---------------------------------------------------------------------------
# I. picture_story  --  Reading & Writing Part 7
#
# El benchmark de G5 lo pide con estas palabras: "Writing Part 3: 20-25-word
# picture story". Tres vinetas, una frase por vineta, y el contador delante
# para que el alumno vea si se queda corto.
# ---------------------------------------------------------------------------
VERBOS = [
    ("find", "finds", "found"), ("take", "takes", "took"), ("carry", "carries", "carried"),
    ("show", "shows", "showed"), ("give", "gives", "gave"), ("bring", "brings", "brought"),
]

# Adjetivos de estado: los que se pueden poner detras de "is" y describen a
# una persona en una vineta. Sirven para las unidades de gramatica pura, que
# no tienen sustantivos que contar pero si sentimientos que dibujar.
ADJETIVOS = {
    "afraid", "angry", "bored", "brave", "busy", "careful", "clever", "excited",
    "friendly", "frightened", "funny", "happy", "hungry", "kind", "lazy", "lucky",
    "noisy", "proud", "quiet", "sad", "scared", "shy", "sick", "sorry", "strong",
    "surprised", "thirsty", "tired", "worried", "cold", "hot", "ready", "sure",
    "polite", "rude", "honest", "patient", "generous", "creative", "stubborn",
    "reliable", "ambitious", "fair", "gentle", "serious", "cheerful", "calm",
    "nervous", "curious", "helpful", "selfish", "hard-working", "well-behaved",
}

# Terminaciones que delatan un adjetivo. Sirven para las unidades de
# descripcion, donde la lista es toda de adjetivos y ninguno esta en la
# lista de arriba.
FIN_ADJETIVO = ("ful", "ous", "ive", "less", "able", "ible", "ish")


def es_adjetivo(w):
    return w in ADJETIVOS or w.endswith(FIN_ADJETIVO)


def picture_story(ud, rnd):
    """La imagen de cada vineta son NUESTROS personajes en NUESTRO escenario.

    Ojo con la tentacion de exigir que las palabras tengan dibujo: aqui no se
    dibuja el objeto, se dibuja la escena. La palabra va escrita debajo como
    pista para escribir. Por eso basta con que sean sustantivos (para las
    historias de objeto) o adjetivos de estado (para las de sentimiento), y
    asi entran tambien las unidades de gramatica pura.
    """
    palabras = [limpia(w) for w in (ud.get("wordlist") or [])]
    palabras = [w for w in dict.fromkeys(palabras) if w and len(w) <= 22]
    nombres = [w for w in palabras
               if dibujable(w) and not es_adjetivo(w)]
    sentires = [w for w in palabras if es_adjetivo(w)]

    gente = [s for s in elenco(ud, rnd, 9) if PERS[s]["tipo"] in ("nino", "nina")]
    if len(gente) < 2:
        return None
    a, b = gente[0], gente[1]
    sitios = LUGAR_TEMA.get(str((ud.get("scope") or {}).get("temaN") or 1), list(LUGARES))
    sitios = [s for s in sitios if s in LUGARES] or list(LUGARES)

    na, nb = PERS[a]["nombre"], PERS[b]["nombre"]
    # tres sitios DISTINTOS: con rnd.choice suelto salian las tres vinetas en
    # el mismo sitio, y entonces no hay historia que contar
    baraja = sitios[:]
    rnd.shuffle(baraja)
    while len(baraja) < 3:
        baraja += sitios
    sitio, s2, s3 = baraja[0], baraja[1], baraja[2]

    # Las tres plantillas caben en 20-25 palabras a proposito. El modelo que
    # ve el alumno tiene que ser una respuesta VALIDA a la consigna: con
    # frases de doce palabras salian historias de 34, o sea el ejemplo
    # contradecia lo que se le acababa de pedir.
    if len(nombres) >= 3:
        rnd.shuffle(nombres)
        tres = nombres[:3]
        v = VERBOS[ud["number"] % len(VERBOS)]
        marcos = [
            {"n": 1, "scene": sitio, "people": [{"slug": a, "pose": pose(a, rnd, [4, 3, 1])}],
             "word": tres[0],
             "hint": "%s / %s / %s %s" % (na, v[1], articulo(tres[0]), tres[0]),
             "model": "%s %s %s %s %s." % (na, v[1], articulo(tres[0]), tres[0], en_el(sitio))},
            {"n": 2, "scene": s2,
             "people": [{"slug": a, "pose": pose(a, rnd, [8, 3])},
                        {"slug": b, "pose": pose(b, rnd, [1, 3])}],
             "word": tres[1],
             "hint": "%s / bring / %s %s" % (nb, articulo(tres[1]), tres[1]),
             "model": "Then %s brings %s %s." % (nb, articulo(tres[1]), tres[1])},
            {"n": 3, "scene": s3,
             "people": [{"slug": b, "pose": pose(b, rnd, [10, 1, 3])},
                        {"slug": a, "pose": pose(a, rnd, [10, 1])}],
             "word": tres[2],
             "hint": "now / %s %s / happy" % (articulo(tres[2]), tres[2]),
             "model": "Now they have got %s %s too, and both are happy."
                      % (articulo(tres[2]), tres[2])},
        ]
    elif len(sentires) >= 3:
        rnd.shuffle(sentires)
        tres = sentires[:3]
        marcos = [
            {"n": 1, "scene": sitio, "people": [{"slug": a, "pose": pose(a, rnd, [4, 6, 1])}],
             "word": tres[0],
             "hint": "%s / be / %s" % (na, tres[0]),
             "model": "%s is %s %s." % (na, tres[0], en_el(sitio))},
            {"n": 2, "scene": s2,
             "people": [{"slug": b, "pose": pose(b, rnd, [3, 1])},
                        {"slug": a, "pose": pose(a, rnd, [6, 3])}],
             "word": tres[1],
             "hint": "%s / talk to / %s / %s" % (nb, na, tres[1]),
             "model": "%s talks to %s because %s looks %s."
                      % (nb, na, el_ella(a), tres[1])},
            {"n": 3, "scene": s3,
             "people": [{"slug": a, "pose": pose(a, rnd, [10, 7, 1])},
                        {"slug": b, "pose": pose(b, rnd, [1, 3])}],
             "word": tres[2],
             "hint": "now / both / %s" % tres[2],
             "model": "Now they are both %s and they smile." % tres[2]},
        ]
    else:
        # Tercera variante: la historia no necesita ninguna palabra de la
        # lista. Son dos personajes y tres sitios, que siempre los hay. Vale
        # para las unidades de gramatica pura (posesivos, preposiciones,
        # meses), donde no hay ni cosas que contar ni sentimientos que poner
        # en la cara, pero escribir 20-25 palabras sobre tres vinetas se
        # puede hacer igual. El lenguaje de la unidad va en 'support'.
        marcos = [
            {"n": 1, "scene": sitio, "people": [{"slug": a, "pose": pose(a, rnd, [4, 6, 1])}],
             "word": "",
             "hint": "%s / %s" % (na, en_el(sitio)),
             "model": "One morning %s is %s." % (na, en_el(sitio))},
            {"n": 2, "scene": s2,
             "people": [{"slug": a, "pose": pose(a, rnd, [3, 1])},
                        {"slug": b, "pose": pose(b, rnd, [3, 1])}],
             "word": "",
             "hint": "%s / meet / %s" % (na, nb),
             "model": "Then %s meets %s %s." % (na, nb, en_el(s2))},
            {"n": 3, "scene": s3,
             "people": [{"slug": a, "pose": pose(a, rnd, [10, 7, 1])},
                        {"slug": b, "pose": pose(b, rnd, [10, 1])}],
             "word": "",
             "hint": "%s / happy" % en_el(s3),
             # "They go at the picnic garden" era ademas incorrecto: en_el()
             # da la preposicion de estar, no la de ir
             "model": "%s they are very happy together." % en_el(s3).capitalize()},
        ]

    tres = [m.get("word") for m in marcos if m.get("word")]
    modelo = " ".join(m["model"] for m in marcos)
    return {
        "type": "picture_story",
        "title": "Look at the three pictures and write the story.",
        "instructions": "Look at the pictures. Write the story in 20-25 words. Use the words under each picture to help you.",
        "outputs": ["digital"],
        "kpi": kpi(ud, "picture_story"),
        "data": {
            "frames": marcos,
            "min_words": 20,
            "max_words": 25,
            "model": modelo,
            "words": tres,
            "support": {
                "grammar": ud.get("grammar", ""),
                "words": [limpia(w) for w in (ud.get("wordlist") or [])[:6]],
            },
        },
    }


# ---------------------------------------------------------------------------
def codigos_libres(ud, cuantos):
    usados = {a.get("code") for a in ud.get("activities", [])}
    libres = []
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if c not in usados:
            libres.append(c)
        if len(libres) == cuantos:
            break
    return libres


def escribe_mapa(unidades):
    """Resumen de que parte del examen practica cada unidad.

    El portal lo necesita para poder enseñar las tareas de Flyers DENTRO de
    la clase de 5.o, y cargar las 55 unidades enteras para averiguarlo seria
    absurdo. Se escribe siempre, aunque no se genere nada nuevo.
    """
    mapa = lee(os.path.join(RAIZ, "content", "scope-map.json"))
    temas = mapa["reparto"]["G5"]["temas"]
    salida = {
        "_leeme": "Generado por tools/gen_visual_flyers.py. No editar a mano.",
        "grado": "G5", "cefr": CAST["cefr"], "examen": CAST["examen"],
        "temas": [{"n": t["n"], "nombre": t["tema"], "unidades": t["unidades"]} for t in temas],
        "unidades": {},
    }
    for _, ud in unidades:
        partes = []
        for a in ud.get("activities", []):
            k = a.get("kpi") or {}
            if k.get("examen_parte"):
                partes.append({"paper": k["examen_parte"]["paper"],
                               "part": k["examen_parte"]["part"],
                               "tipo": a["type"], "code": a["code"],
                               "clase": k.get("clase", "")})
        ef = ud.get("exam_focus") or {}
        salida["unidades"][str(ud["number"])] = {
            "titulo": ud.get("title", ""),
            "foco": {"paper": ef.get("paper"), "part": ef.get("part")} if ef else None,
            "visuales": partes,
        }
    ruta = os.path.join(CONTENIDO, "exam-map.json")
    if not DRY:
        io.open(ruta, "w", encoding="utf-8").write(
            json.dumps(salida, ensure_ascii=False, indent=1) + chr(10))
    return sum(len(v["visuales"]) for v in salida["unidades"].values())


def main():
    rutas = sorted(glob.glob(os.path.join(CONTENIDO, "unit-*.json")))
    if not rutas:
        raise SystemExit("no encuentro content/flyers/unit-*.json")

    # banco de palabras de TODAS las unidades: los distractores vienen de
    # otros temas a proposito, que ademas es repaso espaciado
    banco = []
    unidades = []
    for r in rutas:
        u = lee(r)
        unidades.append((r, u))
        banco += [limpia(w) for w in (u.get("wordlist") or []) if dibujable(w)]
    banco = list(dict.fromkeys(banco))

    total = {t: 0 for t in NUEVOS}
    sin = {t: [] for t in NUEVOS}
    tocadas = 0

    for ruta, ud in unidades:
        ya = {a.get("type") for a in ud.get("activities", [])}
        pendientes = [t for t in NUEVOS if t not in ya]
        if not pendientes:
            continue
        rnd = random.Random(9000 + ud["number"])
        otras = [w for w in banco if w not in
                 {limpia(x) for x in (ud.get("wordlist") or [])}]

        hechas = []
        for tipo in pendientes:
            if tipo == "label_people":
                act = label_people(ud, rnd)
            elif tipo == "picture_mc":
                act = picture_mc(ud, rnd, otras)
            elif tipo == "match_pictures":
                act = match_pictures(ud, rnd, otras)
            else:
                act = picture_story(ud, rnd)
            if act is None:
                sin[tipo].append(ud["number"])
                continue
            hechas.append(act)
            total[tipo] += 1

        if not hechas:
            continue
        for c, act in zip(codigos_libres(ud, len(hechas)), hechas):
            act["code"] = c
            if "audio" in act:
                act["audio"] = act["audio"].replace("{code}", c.lower())
            ud["activities"].append(act)
        tocadas += 1
        if not DRY:
            io.open(ruta, "w", encoding="utf-8").write(
                json.dumps(ud, ensure_ascii=False, indent=1) + "\n")

    n_map = escribe_mapa([(r, lee(r)) for r, _ in unidades])
    print("content/flyers/exam-map.json: %d tareas visuales indexadas" % n_map)
    print("unidades tocadas: %d de %d%s" % (tocadas, len(unidades), "  (--dry)" if DRY else ""))
    for t in NUEVOS:
        falta = sin[t]
        print("  %-16s %3d generadas" % (t, total[t]), end="")
        if falta:
            print("   sin generar en %d: %s" % (len(falta), ", ".join("u%d" % n for n in falta[:14])
                                                + (" ..." if len(falta) > 14 else "")))
        else:
            print()
    print("\narte disponible: %d SVG propios, %d PNG propios, %d emoji" % (len(SVG), len(PNG), len(EMOJI)))


if __name__ == "__main__":
    main()
