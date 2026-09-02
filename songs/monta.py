# -*- coding: utf-8 -*-
"""Junta las letras de un nivel y comprueba que sirven para esa unidad.

La comprobacion no es de estilo, es de fondo: una cancion "de la unidad 12"
que no diga ninguna de las palabras de la unidad 12 no vale para nada, por
bonita que sea. Aqui se cuenta cuantas palabras del wordlist aparecen de
verdad en la letra, y se avisa de las que se quedan flojas.

El prompt de estilo NO se escribe a mano 45 veces: hay una formula por tipo
-la del chant es la que aprobo el usuario- y solo cambia la edad del nivel.

    python songs/monta.py starters
"""
import glob, io, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CONTENT = r"C:\Projects\nis-portal\nis-fun\content"

# La formula del chant es la de la toma aprobada (en/movers/03, 0:26). La de
# la cancion, la de "Yesterday at the Funfair" 1:35.
EDAD = {"starters": "6-year-old", "movers": "9-year-old", "flyers": "11-year-old"}

CHANT = ("playground chant for {edad} children, call and response, handclaps "
         "and foot stomps, one adult leader voice and a chorus of kids "
         "answering, spoken-sung not melodic, 96 BPM, no melody instruments, "
         "very clear diction")

CANCION = ("happy children's pop, ukulele, acoustic guitar and handclaps, "
           "bright warm voice with a small kids' chorus on the refrain, "
           "104 BPM, simple and nursery-friendly, no heavy drums, "
           "very clear diction")


def palabras_de(nivel, n):
    p = os.path.join(CONTENT, nivel, "unit-%02d.json" % int(n))
    d = json.load(io.open(p, encoding="utf-8"))
    return (d.get("wordlist") or []) + (d.get("wordlist_extra") or []), d


def cubre(letra, palabras):
    """Cuantas palabras de la unidad aparecen de verdad en la letra."""
    b = letra.lower()
    hay = [w for w in palabras
           if re.search(r"\b" + re.escape(w.lower().split()[0]), b)]
    return hay


def principal(nivel):
    datos = {}
    for f in sorted(glob.glob(os.path.join(AQUI, "_chunk*.json"))):
        datos.update(json.load(io.open(f, encoding="utf-8")))

    fuera, flojas = {}, []
    for n in sorted(datos, key=int):
        pal, ud = palabras_de(nivel, n)
        e = datos[n]
        edad = EDAD.get(nivel, "8-year-old")
        for tipo, formula in (("chant", CHANT), ("cancion", CANCION)):
            e[tipo]["estilo"] = formula.format(edad=edad)
            usa = cubre(e[tipo]["letra"], pal)
            e[tipo]["usa"] = len(usa)
            if len(usa) < 4:
                flojas.append("%s u%s %s: solo %d de %d palabras (%s)"
                              % (nivel, n, tipo, len(usa), len(pal),
                                 ", ".join(usa)))
        e["palabras"] = pal
        e["titulo_unidad"] = ud["title"]
        fuera[n] = e

    salida = os.path.join(AQUI, nivel + ".json")
    io.open(salida, "w", encoding="utf-8").write(
        json.dumps({"_nivel": nivel,
                    "_nota": "Una cancion y un chant por unidad, con la letra "
                             "sacada del vocabulario y la gramatica de esa "
                             "unidad. 'usa' dice cuantas palabras de la unidad "
                             "aparecen de verdad en la letra.",
                    "unidades": fuera}, ensure_ascii=False, indent=1) + "\n")

    total = sum(e[t]["usa"] for e in fuera.values() for t in ("chant", "cancion"))
    print("%s: %d unidades, %d piezas" % (nivel, len(fuera), len(fuera) * 2))
    print("palabras de la unidad usadas, de media: %.1f por pieza"
          % (total / (len(fuera) * 2)))
    if flojas:
        print("\nflojas (menos de 4 palabras de su unidad):")
        for x in flojas:
            print("  ", x)
    else:
        print("ninguna pieza baja de 4 palabras de su unidad")
    return len(flojas)


if __name__ == "__main__":
    sys.exit(1 if principal(sys.argv[1] if len(sys.argv) > 1 else "starters") else 0)
