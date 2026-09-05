# -*- coding: utf-8 -*-
"""Junta las letras de un nivel, les pone estilo y comprueba que sirven.

Dos comprobaciones, ninguna de estilo:

  * que la letra USA el vocabulario de su unidad. Una cancion "de la unidad
    12" que no diga ninguna palabra de la unidad 12 no vale para nada, por
    bonita que sea.
  * que las canciones no suenan todas igual. Al principio habia UNA formula
    de estilo para las 45 unidades y el resultado fue exactamente lo que
    cabia esperar: ocho canciones seguidas con el mismo tempo, los mismos
    instrumentos y el mismo aire. Ahora cada unidad coge un groove del
    repertorio de abajo, elegido por su tema, y dos unidades seguidas nunca
    llevan el mismo.

El chant SI comparte formula, y es a proposito: es un drill de percusion y
voz, sin instrumentos melodicos. Ahi lo que tiene que variar es la letra.

    python songs/monta.py starters          # con _chunk*.json: monta de cero
    python songs/monta.py starters --estilo # sin chunks: solo re-estila
"""
import glob, io, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CONTENT = r"C:\Projects\nis-portal\nis-fun\content"

EDAD = {"starters": "6-year-old", "movers": "9-year-old", "flyers": "11-year-old"}

# Lo que no cambia nunca: a quien se le canta y que se le entienda.
ESPINA = ("bright warm lead voice with a small kids' chorus on the refrain, "
          "simple and nursery-friendly, very clear diction")

CHANT = ("playground chant for {edad} children, call and response, handclaps "
         "and foot stomps, one adult leader voice and a chorus of kids "
         "answering, spoken-sung not melodic, 96 BPM, no melody instruments, "
         "very clear diction")

# El repertorio. Cada entrada es tempo + instrumentos + aire; ninguno lleva
# bateria dura ni nada que tape la letra.
GROOVES = {
 "ukelele":  "happy children's pop, ukulele, acoustic guitar and handclaps, 104 BPM",
 "vals":     "gentle children's waltz in 3/4, accordion and soft acoustic strings, 92 BPM",
 "banda":    "cheerful marching band parade, snare drum, tuba and bright brass, 116 BPM",
 "electro":  "playful kids' electro-pop, bouncy synth bass, bleeps and claps, 110 BPM",
 "skiffle":  "skiffle shuffle, washboard, upright bass and strummed acoustic guitar, 118 BPM",
 "bossa":    "light bossa nova, nylon-string guitar, shakers and brushed drums, 100 BPM",
 "funk":     "clean kids' funk, clavinet, wah guitar and tight snappy drums, 104 BPM",
 "doowop":   "sweet 50s doo-wop, finger snaps, piano triplets and sha-la-la backing, 124 BPM",
 "campo":    "country hoedown, banjo, fiddle and foot stomps, 96 BPM",
 "calipso":  "sunny calypso, steel drums and shakers, 108 BPM",
 "reggae":   "easy children's reggae, offbeat guitar skank and warm bass, 88 BPM",
 "nana":     "soft lullaby, music box, celesta and gentle strings, 72 BPM",
 "rocanrol": "playful 12-bar rock and roll, boogie piano and clean electric guitar, 128 BPM",
 "polka":    "bouncy accordion polka, tuba oom-pah and tambourine, 120 BPM",
 "gospel":   "joyful gospel handclap, upright piano and a big children's choir, 96 BPM",
}

# El tema de la unidad manda: el ritmo refuerza lo que se esta aprendiendo.
# Un desfile para el zoo, un vals para la familia, funk para mover el cuerpo.
POR_TEMA = {
 "toys": "ukelele",        "family": "vals",         "animals": "banda",
 "numbers": "electro",     "school": "skiffle",      "colours": "bossa",
 "body": "funk",           "face": "doowop",         "clothes": "polka",
 "house": "vals",          "bedroom": "nana",        "food": "calipso",
 "fruit": "bossa",         "drinks": "calipso",      "pets": "campo",
 "farm": "campo",          "wild animals": "banda",  "sea": "reggae",
 "people": "doowop",       "friends": "doowop",      "adjectives": "polka",
 "feelings": "vals",       "can": "funk",            "action verbs": "funk",
 "in / on / under": "skiffle", "school actions": "skiffle",
 "sports": "banda",        "playground": "calipso",  "street": "skiffle",
 "beach": "reggae",        "weather": "reggae",      "days": "polka",
 "day parts": "nana",      "breakfast": "campo",     "lunch": "calipso",
 "birthday": "rocanrol",   "body actions": "funk",   "animals + can": "banda",
 "letters": "electro",     "spelling": "electro",    "he / she": "doowop",
 "this / that": "polka",   "review": "rocanrol",
 "review & celebration": "gospel",
}

RUEDA = ["ukelele", "banda", "bossa", "funk", "polka", "campo",
         "calipso", "doowop", "electro", "reggae", "skiffle", "vals"]


def groove_de(ud, previo, i):
    """El groove de esta unidad. Nunca el mismo que el de la anterior: dos
    canciones seguidas iguales es justo lo que se quiere evitar."""
    g = POR_TEMA.get((ud.get("topic") or "").strip())
    if g and g != previo:
        return g
    for k in range(len(RUEDA)):
        cand = RUEDA[(i + k) % len(RUEDA)]
        if cand != previo and cand != g:
            return cand
    return RUEDA[0]


def estilo_cancion(nivel, ud, previo, i):
    g = groove_de(ud, previo, i)
    return g, "%s, for %s children, %s" % (GROOVES[g], EDAD.get(nivel, "8-year-old"), ESPINA)


def palabras_de(nivel, n):
    p = os.path.join(CONTENT, nivel, "unit-%02d.json" % int(n))
    d = json.load(io.open(p, encoding="utf-8"))
    return (d.get("wordlist") or []) + (d.get("wordlist_extra") or []), d


def cubre(letra, palabras):
    """Cuantas palabras de la unidad aparecen de verdad en la letra."""
    b = letra.lower()
    return [w for w in palabras
            if re.search(r"\b" + re.escape(w.lower().split()[0]), b)]


def principal(nivel, solo_estilo=False):
    salida = os.path.join(AQUI, nivel + ".json")
    datos = {}
    if os.path.exists(salida):
        datos = json.load(io.open(salida, encoding="utf-8"))["unidades"]
    # Los chunks se SUMAN a lo que ya hay: se escriben por tandas y montar de
    # cero borraria las unidades que no estan en la tanda de hoy.
    if not solo_estilo:
        for f in sorted(glob.glob(os.path.join(AQUI, "_chunk*.json"))):
            datos.update(json.load(io.open(f, encoding="utf-8")))
    if not datos:
        raise SystemExit("no hay ni %s.json ni _chunk*.json" % nivel)

    fuera, flojas, previo = {}, [], None
    for i, n in enumerate(sorted(datos, key=int)):
        pal, ud = palabras_de(nivel, n)
        e = datos[n]
        e["chant"]["estilo"] = CHANT.format(edad=EDAD.get(nivel, "8-year-old"))
        previo, e["cancion"]["estilo"] = estilo_cancion(nivel, ud, previo, i)
        e["cancion"]["groove"] = previo
        for tipo in ("chant", "cancion"):
            usa = cubre(e[tipo]["letra"], pal)
            e[tipo]["usa"] = len(usa)
            if len(usa) < 4:
                flojas.append("%s u%s %s: solo %d de %d palabras (%s)"
                              % (nivel, n, tipo, len(usa), len(pal), ", ".join(usa)))
        e["palabras"] = pal
        e["titulo_unidad"] = ud["title"]
        fuera[n] = e

    io.open(salida, "w", encoding="utf-8").write(
        json.dumps({"_nivel": nivel,
                    "_nota": "Una cancion y un chant por unidad, con la letra "
                             "sacada del vocabulario y la gramatica de esa "
                             "unidad. 'usa' dice cuantas palabras de la unidad "
                             "aparecen de verdad en la letra; 'groove' es el "
                             "aire musical, y no se repite dos unidades "
                             "seguidas.",
                    "unidades": fuera}, ensure_ascii=False, indent=1) + "\n")

    total = sum(e[t]["usa"] for e in fuera.values() for t in ("chant", "cancion"))
    grooves = [e["cancion"]["groove"] for _, e in sorted(fuera.items(), key=lambda x: int(x[0]))]
    seguidos = sum(1 for a, b in zip(grooves, grooves[1:]) if a == b)
    print("%s: %d unidades, %d piezas" % (nivel, len(fuera), len(fuera) * 2))
    print("palabras de la unidad usadas, de media: %.1f por pieza"
          % (total / (len(fuera) * 2)))
    print("grooves distintos: %d de %d posibles; repetidos seguidos: %d"
          % (len(set(grooves)), len(GROOVES), seguidos))
    if flojas:
        print("\nflojas (menos de 4 palabras de su unidad):")
        for x in flojas:
            print("  ", x)
    else:
        print("ninguna pieza baja de 4 palabras de su unidad")
    return len(flojas) + seguidos


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    sys.exit(1 if principal(args[0] if args else "starters",
                            "--estilo" in sys.argv) else 0)
