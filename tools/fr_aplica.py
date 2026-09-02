# -*- coding: utf-8 -*-
"""Reconstruye las unidades francesas desde el glosario.

Toma cada unidad inglesa, cambia SOLO el texto que lee el alumno por su
traduccion y deja intacto todo lo demas: identificadores, poses, escenas,
respuestas numericas, emojis de las diferencias. Lo que no es texto no se
toca, y por eso la version francesa nunca pierde un dibujo.

Una unidad se escribe SOLO si esta traducida entera. Media unidad en frances
y media en ingles es peor que no tenerla: el alumno no sabe si es un fallo o
es el ejercicio. Las que faltan simplemente no salen en el indice.

    python tools/fr_aplica.py                todas las que se puedan
    python tools/fr_aplica.py --estado       cuantas saldrian
"""
import glob, io, json, os, re, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
ROOT = r"C:\Projects\nis-portal\nis-fun"
CONTENT = os.path.join(ROOT, "content")
DESTINO = os.path.join(ROOT, "content-fr")
GLOSARIO = os.path.join(AQUI, "fr_glosario.json")

# Los nombres ingleses son los de los examenes YLE de Cambridge: en frances no
# significan nada. Los identificadores internos NO cambian (las carpetas de
# dibujos, de poses y de audio se llaman starters/movers/flyers), solo cambia
# lo que se lee.
NIVELES = {
    "starters": {"nombre": "Les Explorateurs", "orden": 1, "nivel": "Pré-A1 · débutants",
                 "cast": "Les Explorateurs du Phare"},
    "movers":   {"nombre": "Les Aventuriers", "orden": 2, "nivel": "A1 · en route",
                 "cast": "Le Club du Fjord"},
    "flyers":   {"nombre": "Les Navigateurs", "orden": 3, "nivel": "A2 · exploration",
                 "cast": "L'Expédition Aurore"},
}

NOTA_SCOPE = ("Equivalencia provisional del Scope & Sequence de ingles. El de "
              "Frances no esta cargado todavia: confirmar con el colegio antes "
              "de darlo por oficial.")


def sin_tildes(t):
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn")


def pon(obj, ruta, valor):
    """Escribe en la ruta 'activities[2].data.words[0].clue' de un dict."""
    partes = re.findall(r"[^.\[\]]+|\[\d+\]", ruta)
    cur = obj
    for i, p in enumerate(partes):
        ultimo = i == len(partes) - 1
        if p.startswith("["):
            idx = int(p[1:-1])
            if ultimo:
                cur[idx] = valor
            else:
                cur = cur[idx]
        else:
            if ultimo:
                cur[p] = valor
            else:
                cur = cur[p]


def traduce_unidad(d, g, faltan):
    """Devuelve la unidad traducida, o None si le falta alguna cadena."""
    from fr_extrae import CAMPOS_UNIDAD, CAMPOS_ESCENA, CAMPOS_ACTIVIDAD, textos_de

    pares = []
    for c in CAMPOS_UNIDAD:
        if d.get(c):
            pares.append((c, d[c]))
    for c in CAMPOS_ESCENA:
        if (d.get("scene") or {}).get(c):
            pares.append(("scene." + c, d["scene"][c]))
    for i, a in enumerate(d.get("activities", [])):
        for c in CAMPOS_ACTIVIDAD:
            if a.get(c):
                pares.append((f"activities[{i}].{c}", a[c]))
        for r, t in textos_de(a.get("data") or {}):
            pares.append((f"activities[{i}].data.{r}", t))
        for r, t in textos_de(a.get("kpi") or {}):
            pares.append((f"activities[{i}].kpi.{r}", t))
    for i, h in enumerate(d.get("homework", [])):
        if h.get("prompt"):
            pares.append((f"homework[{i}].prompt", h["prompt"]))
    for c in ("wordlist", "wordlist_extra"):
        for i, w in enumerate(d.get(c) or []):
            pares.append((f"{c}[{i}]", w))
    ef = d.get("exam_focus") or {}
    for c in ("paper", "skill"):
        if ef.get(c):
            pares.append((f"exam_focus.{c}", ef[c]))
    sc = d.get("scope") or {}
    if sc.get("tema"):
        pares.append(("scope.tema", sc["tema"]))
    for i, o in enumerate(sc.get("outcomes") or []):
        for c in ("destreza", "puede"):
            if o.get(c):
                pares.append((f"scope.outcomes[{i}].{c}", o[c]))
    for c in ("vocabulario", "gramatica"):
        for i, v in enumerate(sc.get(c) or []):
            pares.append((f"scope.{c}[{i}]", v))

    sin = [t for _, t in pares if t not in g]
    if sin:
        for t in sin:
            faltan.setdefault(t, 0)
            faltan[t] += 1
        return None

    for ruta, texto in pares:
        pon(d, ruta, g[texto])

    # --- reglas de forma, no de idioma -------------------------------------
    nivel = d.get("level")
    d["lang"] = "fr"
    d["id"] = f"{nivel}-fr-{d.get('number', 0):02d}"

    for a in d.get("activities", []):
        if a.get("type") == "crossword":
            for w in ((a.get("data") or {}).get("words") or []):
                # La cuadricula la calcula el motor: las coordenadas inglesas no
                # valen porque BALL son 4 letras y BALLON son 6.
                w.pop("row", None)
                w.pop("col", None)
                w.pop("dir", None)
                w["word"] = re.sub(r"[^A-Z0-9]", "", sin_tildes(w["word"]).upper())
        # el audio se busca en audio/fr/: el motor ya antepone la carpeta
        if a.get("audio", "").startswith("fr/"):
            a["audio"] = a["audio"][3:]

    if d.get("scope"):
        d["scope"]["nota"] = NOTA_SCOPE
    return d


def principal(solo_estado):
    sys.path.insert(0, AQUI)
    g = json.load(io.open(GLOSARIO, encoding="utf-8")) if os.path.exists(GLOSARIO) else {}
    hechas, faltan, por_nivel = 0, {}, {}
    for f in sorted(glob.glob(os.path.join(CONTENT, "*", "unit-*.json"))):
        nivel = os.path.basename(os.path.dirname(f))
        d = json.load(io.open(f, encoding="utf-8"))
        t = traduce_unidad(d, g, faltan)
        if not t:
            continue
        hechas += 1
        por_nivel.setdefault(nivel, []).append(
            {"n": t["number"], "title": t["title"], "topic": t.get("topic", "")})
        if not solo_estado:
            dst = os.path.join(DESTINO, nivel, os.path.basename(f))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            io.open(dst, "w", encoding="utf-8").write(
                json.dumps(t, ensure_ascii=False, indent=1) + "\n")

    if not solo_estado:
        # indices: solo lo que existe de verdad
        niveles = []
        for nid, meta in sorted(NIVELES.items(), key=lambda x: x[1]["orden"]):
            uds = sorted(por_nivel.get(nid, []), key=lambda u: u["n"])
            if not uds:
                continue
            orig = json.load(io.open(os.path.join(CONTENT, nid, "index.json"),
                                     encoding="utf-8"))
            io.open(os.path.join(DESTINO, nid, "index.json"), "w",
                    encoding="utf-8").write(json.dumps({
                        "level": nid, "lang": "fr",
                        "name": f"{meta['nombre']} - Fun for Nordic {meta['orden']}",
                        "cast": meta["cast"], "color": orig["color"],
                        "mascot": orig["mascot"], "kids": orig["kids"],
                        "units": uds}, ensure_ascii=False, indent=1) + "\n")
            niveles.append({"id": nid, "name": meta["nombre"], "exam": meta["nivel"],
                            "cast": meta["cast"], "mascot": orig["mascot"],
                            "color": orig["color"]})
        io.open(os.path.join(DESTINO, "levels.json"), "w", encoding="utf-8").write(
            json.dumps({"levels": niveles}, ensure_ascii=False, indent=1) + "\n")

    print(f"unidades completas: {hechas}/150 | cadenas sin traducir: {len(faltan)}")
    for nid in ("starters", "movers", "flyers"):
        print(f"   {NIVELES[nid]['nombre']:18s} {len(por_nivel.get(nid, []))} unidades")
    return faltan


if __name__ == "__main__":
    principal("--estado" in sys.argv)
