# -*- coding: utf-8 -*-
"""Revisa que las paginas de los cuentos cuenten lo que dice su texto.

Tres cosas, que son las que se han visto fallar de verdad:

  la conversacion   si una pagina responde a la pregunta de la anterior,
                    los dos que hablan tienen que seguir en el dibujo. En
                    "Hello, bird! What is your name?" contestaba "My name
                    is Pip" con Pip solo: un pajaro hablando al aire.

  quien se nombra   si el texto dice un nombre del elenco, ese personaje
                    tiene que estar en la pagina.

  a donde mira      quien senala necesita algo a ese lado. El volteo lo
                    hace build_readers.py; aqui se comprueba que ademas
                    haya algo hacia donde mirar.

    python tools/check_readers.py
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))


def orientaciones():
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


def quienes(piezas):
    return [p[0].split(":")[2] for p in piezas if p[0].startswith("char:")]


def revisa(cuentos, elenco):
    ori = orientaciones()
    avisos = []
    for c in cuentos:
        pags = c["paginas"]
        for i, p in enumerate(pags):
            gente = quienes(p["piezas"])
            texto = p["t"]

            # 1. la respuesta a una pregunta conserva a los dos que hablan
            if i and pags[i - 1]["t"].rstrip().endswith("?"):
                antes = quienes(pags[i - 1]["piezas"])
                se_fueron = [q for q in antes if q not in gente]
                if se_fueron and len(antes) > 1:
                    avisos.append((c["id"], i + 1,
                                   "responde a una pregunta y %s ya no esta"
                                   % ", ".join(se_fueron)))

            # 2. A quien nombra el texto tiene que verse, salvo cuando el
            #    propio texto dice que NO esta: "Where Is Pip?" es un juego
            #    de buscar y "Luna Runs Away" va de que se ha escapado.
            #    Dibujarlos ahi destriparia el cuento.
            bajo = texto.lower()
            for q in elenco:
                if q in gente or not re.search(r"\b" + q + r"\b", bajo):
                    continue
                se_busca = (q in (p.get("ausente") or [])
                            or "?" in texto
                            or re.search(r"\bno " + q + r"\b", bajo)
                            or re.search(r"\b" + q + r" (is gone|ran away)", bajo))
                if not se_busca:
                    avisos.append((c["id"], i + 1,
                                   "el texto nombra a %s y no sale" % q))

            # 3. quien senala necesita algo a ese lado
            for nombre, x, y, s in p["piezas"]:
                if not nombre.startswith("char:"):
                    continue
                _, _, quien, pose = nombre.split(":")
                if (quien, int(pose)) not in ori:
                    continue
                # con la figura sola en la pagina no hay nada a ningun lado:
                # no es que senale al vacio, es que no la acompana nadie
                if len(p["piezas"]) < 2:
                    continue
                hacia = "der" if x < .5 else "izq"
                hay = [n for n, xx, *_ in p["piezas"]
                       if n != nombre and ((xx > x + .04) if hacia == "der"
                                           else (xx < x - .04))]
                if not hay:
                    avisos.append((c["id"], i + 1,
                                   "%s senala a la %s y no hay nada a ese lado"
                                   % (quien, "derecha" if hacia == "der" else "izquierda")))
    return avisos


if __name__ == "__main__":
    import build_readers as B
    elenco = set()
    base = os.path.join(ROOT, "assets", "characters")
    for lvl in os.listdir(base):
        elenco |= set(os.listdir(os.path.join(base, lvl)))

    avisos = revisa(B.CUENTOS, elenco)
    if not avisos:
        print("  todo cuadra: cada pagina ensena lo que cuenta")
    else:
        print("  %d paginas que no cuadran con su texto:" % len(avisos))
        for cid, n, que in avisos:
            print("   %-8s pag %-3s %s" % (cid, n, que))
