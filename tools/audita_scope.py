# -*- coding: utf-8 -*-
"""Audita Fun for Nordic contra el Scope & Sequence 2026 de NIS.

La secuencia oficial dice que grado hace que examen y que tiene que saber
hacer el alumno al acabarlo. Fun for Nordic es el material con el que se
prepara. Esta herramienta cruza las dos cosas y responde a la pregunta que
importa: de todo lo que la secuencia pide para este grado, que esta ya en
el curso y que falta por hacer.

Reparto de grados (pathway oficial 2026, confirmado con el usuario):
    G2  Starters   Cambridge Starters
    G3  Starters   preparacion de Movers, consolida A1
    G4  Movers     Cambridge Movers
    G5  Flyers     Cambridge Flyers

Se mira destreza por destreza. Para cada bloque de la secuencia se busca si
el curso tiene con que trabajarlo:

    vocabulario   las palabras del bloque, en los wordlist del nivel
    gramatica     el punto, en el grammar de alguna unidad o en The Magic Box
    listening     actividades de tipo listening
    speaking      pairwork y las de comparar dos fotos
    reading       lecturas con hueco y tareas de examen
    writing       los deberes de escribir
    phonics       actividades de sonidos y letras

    python tools/audita_scope.py            los cuatro grados de primaria
    python tools/audita_scope.py G4         solo uno
    python tools/audita_scope.py --json     para el panel del portal
"""
import glob, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
SCOPE = os.path.join(os.path.dirname(ROOT), "nis-portal", "scope", "scope-2026.json")

GRADOS = {
    "G2": {"nivel": "starters", "nota": "Cambridge Starters"},
    "G3": {"nivel": "starters", "nota": "prep de Movers, consolida A1"},
    "G4": {"nivel": "movers",   "nota": "Cambridge Movers"},
    "G5": {"nivel": "flyers",   "nota": "Cambridge Flyers"},
}

# Lo que el portal ya tiene fuera de Fun for Nordic. Sin esto el informe
# daba por perdido el Phonics Studio, que lleva tiempo publicado y cubre
# justo los grados de primaria.
#   ruta      para comprobar que sigue ahi
#   grados    a cuales sirve de verdad, no a cuales dice servir
PORTAL = os.path.join(os.path.dirname(ROOT), "nis-portal")
RECURSOS = {
    "phonics": {
        "nombre": "Phonics Studio",
        "ruta": os.path.join(PORTAL, "phonics", "index.html"),
        "grados": {"G1", "G2", "G3", "G4", "G5"},
        "enlace": "/phonics/",
    },
    "readers": {
        "nombre": "Readers del portal",
        "ruta": os.path.join(PORTAL, "reader.html"),
        # los cinco readers empiezan en A2: valen para Flyers, no para los
        # grados de debajo
        "grados": {"G5"},
        "enlace": "/reader.html",
    },
    "pronunciacion": {
        "nombre": "Pronunciation Coach",
        "ruta": os.path.join(PORTAL, "pronunciation-coach", "index.html"),
        "grados": {"G1", "G2", "G3", "G4", "G5"},
        "enlace": "/pronunciation-coach/",
    },
    "escritura": {
        "nombre": "Virtual Writing Tutor",
        "ruta": os.path.join(PORTAL, "writing-tutor.html"),
        "grados": {"G4", "G5"},
        "enlace": "/writing-tutor.html",
    },
}


def recursos_de(grado):
    """Los recursos del portal que existen de verdad y sirven a ese grado."""
    out = {}
    for k, r in RECURSOS.items():
        if grado in r["grados"] and os.path.exists(r["ruta"]):
            out[k] = r
    return out


# Que tipo de actividad del curso cubre cada bloque de la secuencia.
CUBRE = {
    "Vocabulary Development": ("vocab", None),
    "Language Conventions (Writing)": ("gramatica", None),
    "Listening Skills": ("actividad", {"listening"}),
    "Speaking Skills": ("actividad", {"pairwork", "spot_diff"}),
    "Reading Skills": ("actividad", {"gap_text", "exam_task", "crossword", "match_words"}),
    "Textual Comprehension": ("actividad", {"gap_text", "exam_task"}),
    "Text Types (Writing)": ("deberes", None),
    "Idea Development & Process": ("deberes", None),
    "Phonics": ("actividad", {"phonics"}),
    "Reading Plan": ("reader", None),
    "Writing Reflection": ("selfcheck", None),
}

PARA = set("""a an the and or of to in on at is are am was were be been do does did
have has had will would can could should must my your his her its our their this that
these these those with for from by as it he she they we you i not no yes new
words word learn learning use using about into over under""".split())


# Lineas que no son contenido sino etiquetas del propio documento: la
# taxonomia de Bloom, el perfil del graduado y las competencias ATL.
META = re.compile(r"^\s*(▸|Bloom|ATL|Graduate Profile)", re.I)


def util(puntos):
    return [p for p in puntos if p.strip() and not META.match(p)]


def pal(t):
    return {w for w in re.findall(r"[a-z']+", (t or "").lower()) if len(w) > 2 and w not in PARA}


def carga_nivel(nivel):
    """Todo lo que el curso ofrece en ese nivel, ya masticado."""
    d = {"wordlist": set(), "grammar": set(), "tipos": set(),
         "deberes": 0, "unidades": 0, "topics": []}
    for f in sorted(glob.glob(os.path.join(CONTENT, nivel, "unit-*.json"))):
        u = json.load(io.open(f, encoding="utf-8"))
        d["unidades"] += 1
        d["topics"].append(u.get("topic", ""))
        for w in u.get("wordlist", []):
            d["wordlist"] |= pal(w if isinstance(w, str) else w.get("w", ""))
        d["grammar"] |= pal(u.get("grammar", ""))
        for a in u.get("activities", []):
            d["tipos"].add(a.get("type", ""))
        if u.get("homework"):
            d["deberes"] += 1
    return d


def revisa_bloque(bloque, puntos, curso, recursos):
    """Devuelve (estado, detalle) para un bloque de la secuencia."""
    modo, tipos = CUBRE.get(bloque, (None, None))
    if modo is None:
        return "no aplica", ""

    if modo == "actividad":
        hay = sorted(tipos & curso["tipos"])
        if hay:
            return "cubierto", "en el curso: " + ", ".join(hay)
        # puede estar fuera del curso, en otro sitio del portal
        if "phonics" in tipos and "phonics" in recursos:
            return "en el portal", recursos["phonics"]["nombre"] + " (" + \
                   recursos["phonics"]["enlace"] + ")"
        return "FALTA", "no hay actividades de " + ", ".join(sorted(tipos))

    if modo == "deberes":
        extra = ""
        if "escritura" in recursos:
            extra = " · " + recursos["escritura"]["nombre"]
        if curso["deberes"]:
            return "cubierto", ("%d unidades con tarea de escribir" % curso["deberes"]) + extra
        return "FALTA", "ninguna unidad pide escribir"

    if modo == "selfcheck":
        return "cubierto", "cada unidad acaba con su self-check"

    if modo == "reader":
        if "readers" in recursos:
            return "en el portal", recursos["readers"]["nombre"] + " (" + \
                   recursos["readers"]["enlace"] + ")"
        return "FALTA", "los readers del portal empiezan en A2; este grado no llega"

    # vocabulario y gramatica: se mira punto por punto
    fuente = curso["wordlist"] if modo == "vocab" else curso["grammar"]
    puntos = util(puntos)
    if not puntos:
        return "no aplica", ""
    sueltos = []
    for p in puntos:
        ps = pal(p)
        if not ps:
            continue
        if not (ps & fuente):
            sueltos.append(p)
    if not sueltos:
        return "cubierto", "%d de %d puntos" % (len(puntos), len(puntos))
    if len(sueltos) < len(puntos):
        return "a medias", "sin cubrir: " + " · ".join(s[:44] for s in sueltos[:3])
    return "FALTA", "ninguno de los %d puntos" % len(puntos)


def audita(grado, scope):
    cfg = GRADOS[grado]
    curso = carga_nivel(cfg["nivel"])
    recursos = recursos_de(grado)
    g = next((x for x in scope["grados"] if x["grado"] == grado), None)
    if not g:
        return None
    via = next((x for x in scope["pathway"] if x["grado"] == grado), {})

    unidades = []
    for u in g["unidades"]:
        bloques = []
        for b in u["bloques"]:
            estado, detalle = revisa_bloque(b["bloque"], util(b["puntos"]), curso, recursos)
            if estado == "no aplica":
                continue
            bloques.append({"seccion": b["seccion"], "bloque": b["bloque"],
                            "puntos": util(b["puntos"]), "estado": estado,
                            "detalle": detalle})
        unidades.append({"n": u["n"], "tema": u["tema"], "bloques": bloques})

    todos = [b for u in unidades for b in u["bloques"]]
    resumen = {e: sum(1 for b in todos if b["estado"] == e)
               for e in ("cubierto", "en el portal", "a medias", "FALTA")}
    return {
        "grado": grado, "nivel": cfg["nivel"], "nota": cfg["nota"],
        "cefr": g["cefr"], "examen": via.get("examen", ""),
        "unidadesCurso": curso["unidades"], "tiposCurso": sorted(t for t in curso["tipos"] if t),
        "temas": [u["tema"] for u in g["unidades"]],
        "unidades": unidades, "resumen": resumen,
        "recursos": [{"nombre": r["nombre"], "enlace": r["enlace"]} for r in recursos.values()],
    }


if __name__ == "__main__":
    if not os.path.exists(SCOPE):
        raise SystemExit("falta el scope: " + SCOPE)
    scope = json.load(io.open(SCOPE, encoding="utf-8"))
    pedidos = [a for a in sys.argv[1:] if a in GRADOS] or list(GRADOS)
    salida = [audita(g, scope) for g in pedidos]
    salida = [s for s in salida if s]

    if "--json" in sys.argv:
        p = os.path.join(os.path.dirname(SCOPE), "auditoria-primaria.json")
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            json.dumps({"grados": salida}, ensure_ascii=False, indent=1) + "\n")
        print("  %s  (%d grados)" % (os.path.basename(p), len(salida)))
        raise SystemExit(0)

    for s in salida:
        print("=" * 78)
        print("%s · %s · %s   →  Fun for Nordic %s (%d unidades)"
              % (s["grado"], s["cefr"], s["examen"] or s["nota"],
                 s["nivel"], s["unidadesCurso"]))
        r = s["resumen"]
        print("   en el curso %d · en el portal %d · a medias %d · FALTA %d"
              % (r["cubierto"], r["en el portal"], r["a medias"], r["FALTA"]))
        if s["recursos"]:
            print("   apoyo del portal: " + ", ".join(x["nombre"] for x in s["recursos"]))
        for u in s["unidades"]:
            malos = [b for b in u["bloques"]
                     if b["estado"] not in ("cubierto", "en el portal")]
            if not malos:
                print("   U%d %-22s todo cubierto" % (u["n"], u["tema"][:22]))
                continue
            print("   U%d %-22s" % (u["n"], u["tema"][:22]))
            for b in malos:
                print("      %-9s %-30s %s" % (b["estado"], b["bloque"][:30], b["detalle"][:66]))
        print()
