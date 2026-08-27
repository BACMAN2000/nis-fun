# -*- coding: utf-8 -*-
"""Reparte las unidades de Fun for Nordic entre los temas del Scope & Sequence.

La secuencia da seis temas por grado; el curso tiene 45, 50 y 55 unidades.
Para poder alinear vocabulario y gramatica hay que saber antes que unidad
del curso trabaja que tema de que grado.

Cada nivel del curso da para dos cursos escolares y los dos grados que lo
comparten tienen temas DISTINTOS, asi que sus unidades se REPARTEN entre
ellos: ninguna unidad se da dos veces. Flyers va entero a G5.

El reparto se propone por afinidad — se compara el titulo, el tema y el
vocabulario de cada unidad con el tema y el vocabulario que la secuencia
pide — y se guarda en content/scope-map.json, que es un archivo normal y
se puede corregir a mano. Nada mas del curso depende de adivinar: a partir
de ahi todo lee ese mapa.

    python tools/mapea_scope.py            propone y escribe el mapa
    python tools/mapea_scope.py --ver      lo enseña sin tocar nada
"""
import glob, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
SCOPE = os.path.join(os.path.dirname(ROOT), "nis-portal", "scope", "scope-2026.json")
MAPA = os.path.join(CONTENT, "scope-map.json")

# Que grados se reparten cada nivel del curso.
# Cada nivel del curso da para dos cursos escolares: el primero lo
# construye y el segundo lo termina y se presenta al examen. Coincide con
# el pathway oficial, donde G1 es "Pre-Starters prep" y G3 "Pre-Movers
# prep" — los anos sin examen.
REPARTO = {
    "starters": ["G1", "G2"],
    "movers":   ["G3", "G4"],
    "flyers":   ["G5"],
}

PARA = set("""a an the and or of to in on at is are am was were be do does did have has
had will can could should must my your his her its our their this that these those with
for from by as it he she they we you not no yes new word words about into over under
simple short long first second third use using""".split())


def pal(t):
    return {w for w in re.findall(r"[a-z']+", (t or "").lower()) if len(w) > 2 and w not in PARA}


def unidades_curso(nivel):
    out = []
    for f in sorted(glob.glob(os.path.join(CONTENT, nivel, "unit-*.json"))):
        d = json.load(io.open(f, encoding="utf-8"))
        voc = set()
        for w in d.get("wordlist", []):
            voc |= pal(w if isinstance(w, str) else w.get("w", ""))
        out.append({
            "n": d["number"], "titulo": d.get("title", ""), "topic": d.get("topic", ""),
            "gram": d.get("grammar", ""),
            "senas": pal(d.get("title", "")) | pal(d.get("topic", "")) | voc | pal(d.get("grammar", "")),
        })
    return out


# Lo que distingue a cada tema de los otros cinco de su grado. Se compara
# con el titulo, el tema y el vocabulario de cada unidad del curso.
#
# Estan escritas a mano a proposito: sacarlas del propio vocabulario de la
# secuencia no funciona, porque un tema ancho como "Personal Identity"
# comparte palabras con casi todas las unidades y se las llevaba todas.
SENAS = {
 ("G1", 1): "hello goodbye name colour colours number numbers one two three alphabet "
            "letter letters greeting",
 ("G1", 2): "classroom school pencil book bag ruler chair table board desk teacher "
            "crayon rubber",
 ("G1", 3): "body head hand arm leg foot feet face eyes nose mouth ears hair fingers toes",
 ("G1", 4): "farm animal animals cow duck horse sheep pig hen cat dog rabbit sound sounds",
 ("G1", 5): "family mother father sister brother baby grandma grandpa home house people",
 ("G1", 6): "food fruit apple banana cake milk water juice eat drink toy toys game fun "
            "party birthday",

 ("G2", 1): "myself name age body face hair eyes head hand nose mouth colour colours "
            "number numbers alphabet letter letters spell spelling boy girl people person "
            "clothes wear shirt shoes hat",
 ("G2", 2): "family home house room bedroom kitchen mother father sister brother baby "
            "grandma grandpa cousin bed table chair door window furniture",
 ("G2", 3): "animal animals pet pets zoo farm cat dog bird fish horse cow duck rabbit "
            "lion elephant monkey wild sea dolphin whale shark",
 ("G2", 4): "town street park shop playground beach place places city road library market",
 ("G2", 5): "food fruit drink drinks breakfast lunch dinner cake apple banana milk water "
            "juice eating healthy hungry thirsty lunchbox",
 ("G2", 6): "toy toys play playing game games sport sports ball jump party birthday "
            "hobby friends",

 ("G3", 1): "school classroom subject subjects teacher lesson book books pencil bag "
            "ruler desk board homework study rules",
 ("G3", 2): "day days morning afternoon evening night routine time clock hour week "
            "monday weekend every always usually sometimes never",
 ("G3", 3): "weather rain rainy sun sunny snow snowy wind windy cloud cloudy season "
            "seasons spring summer autumn winter",
 ("G3", 4): "nature tree trees plant plants garden flower forest jungle ocean river "
            "mountain insect lake habitat",
 ("G3", 5): "feeling feelings happy sad angry tired scared health healthy sick doctor "
            "hurt medicine better",
 ("G3", 6): "community friend friends neighbour helper helpers job jobs work worker "
            "police nurse driver together",

 ("G4", 1): "town city street shop shops market place places building bank post office "
            "library museum cinema directions left right map transport",
 ("G4", 2): "school classroom subject subjects lesson teacher learning study homework "
            "timetable",
 ("G4", 3): "animal animals wild nature forest jungle farm garden tree plant lake river "
            "sea ocean bird insect habitat",
 ("G4", 4): "sport sports game team swim health healthy exercise strong tired hurt "
            "doctor body",
 ("G4", 5): "holiday holidays travel trip journey beach hotel suitcase plane train camp "
            "visit yesterday past went",
 ("G4", 6): "future going want dream job jobs older tomorrow next plan hope",

 ("G5", 1): "myself identity name age appearance body face hair eyes tall personality "
            "friendly funny kind clothes wear",
 ("G5", 2): "routine daily habit habits morning night time clock home house housework "
            "chores usually always often breakfast lunch dinner",
 ("G5", 3): "nature natural animal animals plant tree forest jungle ocean sea river "
            "mountain weather environment planet earth space",
 ("G5", 4): "people culture cultures country countries language city town festival "
            "traditional world flag community",
 ("G5", 5): "health healthy wellbeing doctor hospital hurt sick medicine exercise sport "
            "sleep diet feeling",
 ("G5", 6): "adventure adventures experience experiences travel trip holiday journey "
            "explore discover story past exciting camp",
}


def senas_de(grado, n, u):
    """Las palabras con las que se reconoce ese tema."""
    fijas = SENAS.get((grado, n))
    if fijas:
        return pal(fijas) | pal(u["tema"])
    # los grados sin senas escritas (secundaria) caen al metodo antiguo
    return senas_tema(u)


def senas_tema(u):
    """Con que palabras se reconoce un tema de la secuencia: su nombre y
    todo lo que pide de vocabulario y de gramatica."""
    s = pal(u["tema"])
    for b in u["bloques"]:
        if b["bloque"] in ("Vocabulary Development", "Language Conventions (Writing)",
                           "Unit Themes"):
            for p in b["puntos"]:
                s |= pal(p)
    return s


def propone(scope):
    mapa = {}
    for nivel, grados in REPARTO.items():
        curso = unidades_curso(nivel)
        # los temas de todos los grados que comparten este nivel, juntos
        temas = []
        for g in grados:
            d = next((x for x in scope["grados"] if x["grado"] == g), None)
            if not d:
                continue
            for u in d["unidades"]:
                temas.append({"grado": g, "n": u["n"], "tema": u["tema"],
                              "senas": senas_de(g, u["n"], u)})
        if not temas:
            continue

        # Cada unidad va al tema con el que mas comparte. Con empate a
        # cero todas caian en el primero de la lista y "Hello World!" se
        # llevaba media clase, asi que solo se asigna por afinidad cuando
        # hay afinidad de verdad; el resto se reparte por el orden del
        # curso, que ya viene ordenado por dificultad.
        UMBRAL = 2
        sin_sitio = []
        for uc in curso:
            puntos = []
            for t in temas:
                comun = uc["senas"] & t["senas"]
                # el nombre del tema pesa mas que una palabra suelta del
                # vocabulario: es lo que de verdad dice de que va la unidad
                extra = len(pal(uc["topic"]) & pal(t["tema"])) * 3
                puntos.append((len(comun) + extra, t))
            puntos.sort(key=lambda x: -x[0])
            mejor_n, mejor = puntos[0]
            if mejor_n >= UMBRAL:
                uc["asignado"] = mejor
                uc["fuerza"] = mejor_n
            else:
                uc["asignado"] = None
                uc["fuerza"] = 0
                sin_sitio.append(uc)

        # las que no encajan en ningun tema se reparten por orden entre los
        # temas que menos unidades tienen, empezando por el grado que va
        # primero: asi los dos cursos escolares quedan parejos
        for uc in sin_sitio:
            t = min(temas, key=lambda x: (
                len([u for u in curso if u["asignado"] is x]),
                x["grado"], x["n"]))
            uc["asignado"] = t

        # y si aun asi un tema queda muy cargado, se le quitan las de
        # afinidad mas floja y se pasan al mas vacio
        objetivo = max(2, int(len(curso) / len(temas) * 1.7))
        for _ in range(len(curso)):
            cargados = sorted(temas, key=lambda x: -len([u for u in curso if u["asignado"] is x]))
            gordo, flaco = cargados[0], cargados[-1]
            n_gordo = len([u for u in curso if u["asignado"] is gordo])
            n_flaco = len([u for u in curso if u["asignado"] is flaco])
            # se para en cuanto el mas cargado baja del tope. Antes seguia
            # hasta igualarlos todos, y eso deshacia el trabajo de las
            # senas: acababa siendo un reparto por orden y nada mas.
            if n_gordo <= objetivo:
                break
            floja = min((u for u in curso if u["asignado"] is gordo),
                        key=lambda u: u["fuerza"])
            floja["asignado"] = flaco
            floja["fuerza"] = len(floja["senas"] & flaco["senas"])

        for g in grados:
            mapa.setdefault(g, {"nivel": nivel, "temas": []})
        for t in temas:
            suyas = sorted(u["n"] for u in curso if u["asignado"] is t)
            mapa[t["grado"]]["temas"].append({
                "n": t["n"], "tema": t["tema"], "unidades": suyas,
            })
    for g in mapa:
        mapa[g]["temas"].sort(key=lambda t: t["n"])
    return mapa


if __name__ == "__main__":
    scope = json.load(io.open(SCOPE, encoding="utf-8"))
    mapa = propone(scope)

    for g in sorted(mapa, key=lambda x: int(x[1:])):
        d = mapa[g]
        total = sum(len(t["unidades"]) for t in d["temas"])
        print("%-3s  Fun for Nordic %-9s %d unidades" % (g, d["nivel"], total))
        for t in d["temas"]:
            us = t["unidades"]
            print("   U%d %-26s %2d: %s" % (t["n"], t["tema"][:26], len(us),
                                            ", ".join(str(x) for x in us[:14])))
        print()

    if "--ver" not in sys.argv:
        io.open(MAPA, "w", encoding="utf-8", newline="\n").write(
            json.dumps({"reparto": mapa}, ensure_ascii=False, indent=1) + "\n")
        print("escrito: content/scope-map.json  (se puede corregir a mano)")
