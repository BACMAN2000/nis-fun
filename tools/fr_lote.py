# -*- coding: utf-8 -*-
"""Reparte las cadenas pendientes en lotes y las integra al glosario.

El glosario (tools/fr_glosario.json) es {ingles: frances} y es la fuente de
la traduccion: se traduce cada cadena UNA vez, aunque salga en veinte
unidades. Asi la misma consigna no acaba dicha de tres maneras distintas.

    python tools/fr_lote.py 300            saca las 300 siguientes pendientes
    python tools/fr_lote.py --estado       cuantas faltan
    python tools/fr_lote.py --integra f    mete {indice: traduccion} al glosario
"""
import io, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CADENAS = os.path.join(AQUI, "fr_cadenas.json")
GLOSARIO = os.path.join(AQUI, "fr_glosario.json")
PENDIENTE = os.path.join(AQUI, "fr_lote_actual.json")


def carga_glosario():
    if os.path.exists(GLOSARIO):
        return json.load(io.open(GLOSARIO, encoding="utf-8"))
    return {}


def pendientes(nivel=None):
    d = json.load(io.open(CADENAS, encoding="utf-8"))
    g = carga_glosario()
    orden = [t for t, _ in d["cadenas"] if t not in g]
    if not nivel:
        # por frecuencia: lo que mas se repite primero, para que el vocabulario
        # comun quede fijado antes que las frases sueltas
        return orden, g
    # por nivel: una unidad solo se publica entera, asi que sale mas a cuenta
    # terminar un nivel que dejar las 150 a medias. Y dentro del nivel, primero
    # las unidades a las que les falta menos.
    falta_por_unidad = {}
    for arch, pares in d["mapa"].items():
        if not arch.startswith(nivel + "/"):
            continue
        falta = [t for _, t in pares if t not in g]
        if falta:
            falta_por_unidad[arch] = falta
    vistos, out = set(), []
    for arch in sorted(falta_por_unidad, key=lambda a: len(falta_por_unidad[a])):
        for t in falta_por_unidad[arch]:
            if t not in vistos:
                vistos.add(t)
                out.append(t)
    return out, g


if __name__ == "__main__":
    nivel = sys.argv[sys.argv.index("--nivel") + 1] if "--nivel" in sys.argv else None
    if "--estado" in sys.argv:
        p, g = pendientes(nivel)
        print(f"glosario: {len(g)} traducidas | pendientes: {len(p)}")
        sys.exit()

    if "--integra" in sys.argv:
        f = sys.argv[sys.argv.index("--integra") + 1]
        lote = json.load(io.open(PENDIENTE, encoding="utf-8"))
        nuevas = json.load(io.open(f, encoding="utf-8"))
        g = carga_glosario()
        n = 0
        for k, v in nuevas.items():
            i = int(k)
            if i < len(lote) and isinstance(v, str) and v.strip():
                g[lote[i]] = v.strip()
                n += 1
        io.open(GLOSARIO, "w", encoding="utf-8").write(
            json.dumps(g, ensure_ascii=False, indent=0, sort_keys=True))
        p, _ = pendientes()
        print(f"integradas {n} | glosario {len(g)} | pendientes {len(p)}")
        sys.exit()

    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 300
    p, g = pendientes(nivel)
    lote = p[:n]
    io.open(PENDIENTE, "w", encoding="utf-8").write(json.dumps(lote, ensure_ascii=False))
    for i, t in enumerate(lote):
        print(f"{i}\t{t}")
    print(f"\n--- {len(lote)} cadenas | quedan {len(p) - len(lote)} despues de este lote ---",
          file=sys.stderr)
