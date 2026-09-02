# -*- coding: utf-8 -*-
"""Saca de las unidades inglesas TODO lo que hay que traducir, sin repetir.

La traduccion no se hace unidad por unidad copiando JSON: se saca la lista de
cadenas unicas, se traducen una vez, y fr_aplica.py reconstruye las unidades
francesas con la misma forma. Asi una frase que sale en veinte unidades se
traduce una vez y no queda distinta en cada sitio.

    python tools/fr_extrae.py                 escribe tools/fr_cadenas.json
    python tools/fr_extrae.py --nivel movers  solo un nivel
"""
import glob, io, json, os, re, sys

ROOT = r"C:\Projects\nis-portal\nis-fun"
CONTENT = os.path.join(ROOT, "content")
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fr_cadenas.json")

# Que se traduce de cada unidad. La ruta es "donde vive" dentro del JSON: se
# usa igual al extraer y al reconstruir, para que nada se quede por el camino.
CAMPOS_UNIDAD = ["title", "topic", "grammar"]
CAMPOS_ESCENA = ["bubble", "intro"]
CAMPOS_ACTIVIDAD = ["title", "instructions"]


# Lista BLANCA: solo estas claves llevan texto que lee el alumno. Al reves
# -excluyendo lo conocido- se cuelan los identificadores internos ('campus-hex',
# 'lighthouse-kitchen', 'pose', 'count'), y traducir uno de esos rompe la
# referencia a un dibujo sin que falle nada visible.
CLAVES_TEXTO = {"title", "clue", "prompt", "sentence", "text", "instructions",
                "left", "right", "q", "answer", "word", "left_label",
                "right_label", "options", "items", "script", "hint", "label",
                "question", "story", "tip", "goal", "description", "words",
                # descubiertas auditando: la frase modelo de las actividades de
                # produccion, lo que hace cada persona de la lamina, y las dos
                # lineas del KPI que ve el profesor
                "model", "action", "puede", "clase", "place", "extra",
                "grammar", "support", "topic", "note"}


def textos_de(o, ruta="", dentro=False):
    """Recorre un 'data' de actividad y devuelve (ruta, texto) de lo legible."""
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            r = f"{ruta}.{k}" if ruta else k
            if isinstance(v, str):
                if k in CLAVES_TEXTO and v.strip() and not re.fullmatch(r"[\d\W_]+", v):
                    out.append((r, v))
            else:
                out += textos_de(v, r, k in CLAVES_TEXTO)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            r = f"{ruta}[{i}]"
            if isinstance(v, str):
                if dentro and v.strip() and not re.fullmatch(r"[\d\W_]+", v):
                    out.append((r, v))
            else:
                out += textos_de(v, r, dentro)
    return out


def _viejo_textos_de(o, ruta=""):
    fuera = {"answer", "code", "type", "outputs", "audio", "row", "col", "dir",
             "voice_note", "diffs", "sceneA", "sceneB", "figura", "slug", "pose"}
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k in fuera:
                continue
            r = f"{ruta}.{k}" if ruta else k
            if isinstance(v, str):
                if v.strip() and not re.fullmatch(r"[\d\W_]+", v):
                    out.append((r, v))
            else:
                out += textos_de(v, r)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            r = f"{ruta}[{i}]"
            if isinstance(v, str):
                if v.strip() and not re.fullmatch(r"[\d\W_]+", v):
                    out.append((r, v))
            else:
                out += textos_de(v, r)
    return out


def recoge(nivel_filtro=None):
    cadenas = {}          # texto ingles -> [donde sale, para dar contexto]
    mapa = {}             # archivo -> [(ruta, texto)]
    for f in sorted(glob.glob(os.path.join(CONTENT, "*", "unit-*.json"))):
        nivel = os.path.basename(os.path.dirname(f))
        if nivel_filtro and nivel != nivel_filtro:
            continue
        d = json.load(io.open(f, encoding="utf-8"))
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
            # el KPI es hermano de data, no vive dentro: se le olvidaba
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

        mapa[os.path.relpath(f, CONTENT).replace("\\", "/")] = pares
        for _, t in pares:
            cadenas.setdefault(t, 0)
            cadenas[t] += 1
    return cadenas, mapa


if __name__ == "__main__":
    nivel = None
    if "--nivel" in sys.argv:
        nivel = sys.argv[sys.argv.index("--nivel") + 1]
    cadenas, mapa = recoge(nivel)
    io.open(SALIDA, "w", encoding="utf-8").write(json.dumps(
        {"cadenas": sorted(cadenas.items(), key=lambda x: -x[1]), "mapa": mapa},
        ensure_ascii=False, indent=1))
    pal = sum(len(t.split()) for t in cadenas)
    print(f"{len(mapa)} unidades | {sum(len(v) for v in mapa.values())} apariciones "
          f"| {len(cadenas)} cadenas unicas | ~{pal} palabras")
    print("escrito", SALIDA)
