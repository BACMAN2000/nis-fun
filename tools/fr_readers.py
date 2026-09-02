# -*- coding: utf-8 -*-
"""Genera los cuentos franceses de Nordic Little Readers.

Toma cada cuento ingles de readers/data/, le cambia el texto por el frances
de fr_readers.json y deja intactos los dibujos, los identificadores y el
grado. Los cuentos no son una traduccion literal: son la misma historia
contada en frances, con los mismos personajes y las mismas ilustraciones.

Las palabras resaltadas (clave) se recalculan: "hello" no aparece en una
frase francesa. Se buscan las palabras de la actividad dentro de la frase,
sin el articulo, y se marca la primera que este.

    python tools/fr_readers.py
"""
import io, json, os, re, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
ROOT = r"C:\Projects\nis-portal\nis-fun\readers"
ORIG = os.path.join(ROOT, "data")
DEST = os.path.join(ROOT, "data-fr")
FUENTE = os.path.join(AQUI, "fr_readers.json")

# Los nombres de nivel del MCER son los mismos; el grado tambien.
ARTICULOS = re.compile(r"^(un|une|le|la|les|des|du|de la|l')\s*", re.I)


def sin_tildes(t):
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn")


def claves(texto, palabras):
    """Las palabras de la actividad que aparecen de verdad en la frase."""
    bajo = sin_tildes(texto).lower()
    fuera = []
    for p in palabras:
        n = ARTICULOS.sub("", p).strip()
        if not n:
            continue
        raiz = sin_tildes(n).lower()
        if re.search(r"\b" + re.escape(raiz), bajo):
            fuera.append(n)
    return fuera[:2]


def principal():
    fr = json.load(io.open(FUENTE, encoding="utf-8"))
    os.makedirs(DEST, exist_ok=True)
    indice, faltan = [], []

    for cid in sorted(fr.keys()):
        src = os.path.join(ORIG, cid + ".json")
        if not os.path.exists(src):
            faltan.append(cid)
            continue
        d = json.load(io.open(src, encoding="utf-8"))
        t = fr[cid]

        if len(t["paginas"]) != len(d["paginas"]):
            faltan.append(f"{cid}: {len(t['paginas'])} paginas frances vs "
                          f"{len(d['paginas'])} inglesas")
            continue
        pals = t["actividad"]["palabras"]
        if len(pals) != len(d["actividad"]["items"]):
            faltan.append(f"{cid}: {len(pals)} palabras vs "
                          f"{len(d['actividad']['items'])} items")
            continue

        d["lang"] = "fr"
        d["titulo"] = t["titulo"]
        d["objetivo"] = t["objetivo"]
        for i, p in enumerate(d["paginas"]):
            p["texto"] = t["paginas"][i]
            p["clave"] = claves(p["texto"], pals)
        d["actividad"]["titulo"] = t["actividad"]["titulo"]
        d["actividad"]["instruccion"] = t["actividad"]["instruccion"]
        for i, it in enumerate(d["actividad"]["items"]):
            it["palabra"] = pals[i]

        io.open(os.path.join(DEST, cid + ".json"), "w", encoding="utf-8").write(
            json.dumps(d, ensure_ascii=False, indent=1) + "\n")
        indice.append({"id": d["id"], "grado": d["grado"], "tema": d["tema"],
                       "nivel": d["nivel"], "titulo": d["titulo"],
                       "objetivo": d["objetivo"], "paginas": len(d["paginas"]),
                       "portada": d["paginas"][0].get("img", "")})

    io.open(os.path.join(DEST, "index.json"), "w", encoding="utf-8").write(
        json.dumps({"lang": "fr", "libros": indice}, ensure_ascii=False,
                   indent=1) + "\n")
    print(f"cuentos franceses: {len(indice)}/{len(fr)}")
    for f in faltan:
        print("   FALTA", f)


if __name__ == "__main__":
    principal()
