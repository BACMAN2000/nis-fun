# -*- coding: utf-8 -*-
"""Alinea cada unidad de Fun for Nordic con lo que le pide la secuencia.

Con el reparto ya hecho (content/scope-map.json) cada unidad del curso sabe
a que grado y a que tema pertenece. Aqui se le escribe dentro lo que la
secuencia espera de ella:

    scope.grado        G1..G5
    scope.tema         el tema del ano al que pertenece
    scope.outcomes     que sabra hacer el alumno, por destreza (benchmarks)
    scope.vocabulario  las palabras que le tocan de ese tema
    scope.gramatica    los puntos de lengua que le tocan
    scope.pendiente    lo de arriba que todavia NO esta en la unidad

El vocabulario y la gramatica del tema se REPARTEN entre las unidades del
curso que lo trabajan, no se copian enteros en cada una: si el tema pide
doce palabras y tiene cuatro unidades, a cada una le tocan tres.

Lo que falta se anade como wordlist_extra, no dentro de wordlist. El
wordlist manda en los crucigramas, en las picture words, en los audios ya
grabados y en las escenas de las diferencias, que son deterministas: tocarlo
descuadra 300 imagenes y 1035 mp3. wordlist_extra es material de ampliacion
que el motor puede ensenar sin romper nada de eso.

    python tools/alinea_scope.py           escribe la alineacion
    python tools/alinea_scope.py --ver     la ensena sin tocar nada
"""
import glob, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
SCOPE = os.path.join(os.path.dirname(ROOT), "nis-portal", "scope", "scope-2026.json")
MAPA = os.path.join(CONTENT, "scope-map.json")

# Que destrezas trabaja cada tipo de actividad, para saber a que outcomes
# contribuye una unidad.
DESTREZA = {
    "listening": "listening",
    "pairwork": "speaking", "spot_diff": "speaking",
    "gap_text": "reading", "exam_task": "reading",
    "crossword": "lengua", "match_words": "lengua", "picture_words": "lengua",
}

META = re.compile(r"^\s*(▸|Bloom|ATL|Graduate Profile)", re.I)
# Lineas de vocabulario del tipo "Appearance: tall, short, thin": lo que
# interesa son las palabras de despues de los dos puntos.
# Puntos que la secuencia pide como "vocabulario" pero que estan escritos
# como una funcion de lengua ("Like/don't like: I like..., I don't like...")
# y no como una lista de palabras. El reparto automatico no los ve, y en el
# curso no los cubria ninguna unidad de ese grado: son huecos de verdad, no
# fallos del revisor. Se cierran aqui, con las palabras concretas, sobre la
# unidad del tema que les toca.
HUECOS = {
    ("G1", "Hello World!"):  ["numbers", "one", "two", "three", "four", "five",
                              "six", "seven", "eight", "nine", "ten"],
    ("G1", "Food & Fun"):    ["I like", "I don't like", "my favourite"],
    ("G2", "All About Me"):  ["age", "years old", "numbers", "ordinal numbers",
                              "first", "second", "third", "eleven", "twelve",
                              "twenty"],
    ("G2", "Food & Health"): ["healthy", "unhealthy", "fruit", "vegetables",
                              "sweets"],
    ("G4", "My Future"):     ["I want to be", "I'd like to", "future plans",
                              "I'm going to study", "next year",
                              "when I grow up"],
}


def palabras_de(punto):
    cuerpo = punto.split(":", 1)[1] if ":" in punto else punto
    fuera = re.split(r"[,/·]| and | or ", cuerpo)
    out = []
    for t in fuera:
        t = re.sub(r"\(.*?\)", "", t).strip(" .;")
        # una palabra o dos, en minusculas y sin numeros sueltos
        if not t or len(t) > 22 or not re.match(r"^[A-Za-z][A-Za-z '-]*$", t):
            continue
        if len(t.split()) > 2:
            continue
        out.append(t.lower())
    return out


def senas_unidad(d):
    """Con que se reconoce de que va una unidad del curso."""
    t = " ".join([d.get("title", ""), d.get("topic", ""), d.get("grammar", "")])
    voc = " ".join((w if isinstance(w, str) else w.get("w", ""))
                   for w in d.get("wordlist", []))
    return {w for w in re.findall(r"[a-z']+", (t + " " + voc).lower()) if len(w) > 2}


def reparte_grupos(grupos, unidades, senas):
    """Reparte por grupos, no palabra a palabra.

    El vocabulario viene agrupado en el Excel ("Family members: mum, dad,
    sister...") y esos grupos no se parten: se le dan enteros a la unidad
    del curso que mejor encaja, que para ese ejemplo es la de la familia.
    Lo que no encaja en ninguna se reparte por orden para que ninguna
    unidad se quede sin nada."""
    cajas = {n: [] for n in unidades}
    sueltos = []
    for etiqueta, palabras in grupos:
        marcas = {w for w in re.findall(r"[a-z']+", etiqueta.lower()) if len(w) > 2}
        marcas |= {w for p in palabras for w in p.split()}
        mejor, cuanto = None, 0
        for n in unidades:
            c = len(marcas & senas.get(n, set()))
            if c > cuanto:
                mejor, cuanto = n, c
        if mejor is not None and cuanto >= 2:
            cajas[mejor] += palabras
        else:
            sueltos.append((etiqueta, palabras))
    # los grupos sin dueno claro van a las unidades mas vacias
    for etiqueta, palabras in sueltos:
        n = min(unidades, key=lambda x: (len(cajas[x]), x))
        cajas[n] += palabras
    return cajas


def reparte(cosas, cuantos):
    """Reparte una lista entre n, en orden y sin repetir."""
    if cuantos <= 0:
        return []
    cajas = [[] for _ in range(cuantos)]
    for i, c in enumerate(cosas):
        cajas[i % cuantos].append(c)
    return cajas


def outcomes_de(scope, grado, tipos):
    b = next((x for x in scope["benchmarks"] if x["grado"] == grado), {})
    tenemos = {DESTREZA[t] for t in tipos if t in DESTREZA}
    nombres = {"listening": "Listening", "speaking": "Speaking",
               "reading": "Reading", "writing": "Writing", "lengua": "Grammar & Vocabulary"}
    out = []
    for k in ("listening", "speaking", "reading", "writing", "lengua"):
        if k in tenemos and b.get(k):
            out.append({"destreza": nombres[k], "puede": b[k]})
    return out


def main(escribir):
    scope = json.load(io.open(SCOPE, encoding="utf-8"))
    reparto = json.load(io.open(MAPA, encoding="utf-8"))["reparto"]

    resumen = []
    for grado in sorted(reparto, key=lambda x: int(x[1:])):
        nivel = reparto[grado]["nivel"]
        g = next((x for x in scope["grados"] if x["grado"] == grado), None)
        if not g:
            continue
        n_voc = n_gram = n_und = 0

        for t in reparto[grado]["temas"]:
            tema = next((u for u in g["unidades"] if u["n"] == t["n"]), None)
            if not tema or not t["unidades"]:
                continue

            # lo que el tema pide, agrupado como viene en el Excel
            grupos, gram = [], []
            for b in tema["bloques"]:
                puntos = [p for p in b["puntos"] if not META.match(p)]
                if b["bloque"] == "Vocabulary Development":
                    for p in puntos:
                        ws = palabras_de(p)
                        if ws:
                            grupos.append((p.split(":", 1)[0], ws))
                elif b["bloque"] == "Language Conventions (Writing)":
                    gram += puntos
            gram = list(dict.fromkeys(gram))

            senas = {}
            for n in t["unidades"]:
                f = os.path.join(CONTENT, nivel, "unit-%02d.json" % n)
                if os.path.exists(f):
                    senas[n] = senas_unidad(json.load(io.open(f, encoding="utf-8")))
            cajas_v = reparte_grupos(grupos, t["unidades"], senas)
            cajas_g = reparte(gram, len(t["unidades"]))

            for k, n in enumerate(t["unidades"]):
                f = os.path.join(CONTENT, nivel, "unit-%02d.json" % n)
                if not os.path.exists(f):
                    continue
                d = json.load(io.open(f, encoding="utf-8"))
                tipos = {a.get("type", "") for a in d.get("activities", [])}
                if d.get("homework"):
                    tipos.add("__writing__")
                    DESTREZA["__writing__"] = "writing"

                ya = {(w if isinstance(w, str) else w.get("w", "")).lower()
                      for w in d.get("wordlist", [])}
                mios_v = list(dict.fromkeys(cajas_v.get(n, [])))
                mios_g = cajas_g[k] if k < len(cajas_g) else []
                faltan_v = [w for w in mios_v if w not in ya]

                d["scope"] = {
                    "grado": grado,
                    "temaN": t["n"],
                    "tema": t["tema"],
                    "outcomes": outcomes_de(scope, grado, tipos),
                    "vocabulario": mios_v,
                    "gramatica": mios_g,
                    "pendiente": {"vocabulario": faltan_v},
                }
                # ampliacion: lo que la secuencia pide y la unidad no tenia
                hueco = HUECOS.get((grado, t["tema"]), [])
                if hueco and k == 0:          # la primera unidad del tema
                    faltan_v = faltan_v + [w for w in hueco if w not in faltan_v]
                if faltan_v:
                    d["wordlist_extra"] = faltan_v
                elif "wordlist_extra" in d:
                    del d["wordlist_extra"]

                n_voc += len(faltan_v); n_gram += len(mios_g); n_und += 1
                if escribir:
                    io.open(f, "w", encoding="utf-8", newline="\n").write(
                        json.dumps(d, ensure_ascii=False, indent=1) + "\n")

        resumen.append((grado, nivel, n_und, n_voc, n_gram))

    print("  grado nivel      unidades  vocab nuevo  puntos de lengua")
    for grado, nivel, u, v, gr in resumen:
        print("   %-4s %-10s %6d %11d %14d" % (grado, nivel, u, v, gr))
    if escribir:
        print("\n  escrito el bloque scope en las unidades")
    else:
        print("\n  (nada modificado: quita --ver para escribir)")


if __name__ == "__main__":
    main("--ver" not in sys.argv)
