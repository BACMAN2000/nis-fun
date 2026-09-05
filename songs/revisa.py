# -*- coding: utf-8 -*-
"""Dos comprobaciones que monta.py no hace y que salen caras si fallan.

1. **Quien sale en las letras.** La biblia de personajes es una lista cerrada
   (characters/bible.md). Si una cancion se inventa una prima o un vecino, el
   alumno se encuentra con alguien que no tiene cara, no tiene dibujo y no
   vuelve a aparecer.

2. **Si la letra cita una cancion infantil conocida.** Suno tiene un filtro de
   copyright que rechaza la generacion y NO deja rastro en la biblioteca: solo
   un aviso rojo un par de segundos sobre el boton Create. El chant de la
   unidad 4 se perdio tres veces por esto antes de que nadie mirase la
   pantalla en el momento justo. Lo que lo disparo fue recitar los numeros del
   uno al diez de corrido.

    python songs/revisa.py starters
"""
import io, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))

ELENCO = {"Freya", "Nico", "Astrid", "Tomás", "Pip",          # Starters
          "Erik", "Valentina", "Sofía", "Mateo", "Luna",      # Movers
          "Rosa", "Juan", "Lucía", "Beto", "Pablo", "Carmen", # familias
          "Ana", "Carla", "Pedro",
          "Lía", "Bruno", "Aiko", "Samu", "Iris", "Tino"}     # companeros

# Mayusculas que no son nombres de persona (inicio de verso, etiquetas,
# colores, numeros, gritos del chant).
NO_SON = set("""A B Z All Kids Leader Verse Chorus Bridge Blue Red Green Yellow
Orange Purple Pink Black White Brown TEN TWENTY STOP LOOK LISTEN HANDS UP BIG
UNDER THIS THAT Monday Tuesday Wednesday Thursday Friday Saturday Saturdays
Sunday One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve Thirteen
Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen Twenty Whee Shh Moo Neigh
Oink Quack Nod Wave Shake Stamp Open Close Slow Fast Cool Hot Sing Point Clap
Walk Touch Stand Sit Ready Steady Team Yes No Not Never Put Come Pick Start Say
Tell Take Feed Knock Good Great Every Past After And But The These Those Here
There Where What Who How Why When It He She We You I My His Her Our Their Do
Does Did Can Have Has Had Is Are Am Was Were Be Been Will Would Let Lets Now
Then Once Twice Both Even Just Only Very Too Also Well Down Almost Off On In At
To Of For With From By Up Out Over Above Below Between Behind Beside Beneath
Around Across Through Into Onto Raise Guess Blow Scary Team""".split())

# Temas conocidos que el filtro corta. La lista crece con cada rechazo.
MINAS = [r"old macdonald", r"e-?i-?e-?i-?o",
         r"if you're happy and you know it",
         r"rain,? rain,? go away",
         r"happy birthday to you",
         r"head,? shoulders,? knees and toes",
         r"twinkle,? twinkle",
         r"row,? row,? row your boat",
         r"baa,? baa,? black sheep",
         r"now i know my abc",
         r"once i caught a fish alive",
         r"the wheels on the bus",
         r"itsy bitsy|incy wincy",
         r"mary had a little lamb",
         r"london bridge is falling"]


def candidatos(letra):
    """Mayusculas que pueden ser un nombre de persona.

    La primera palabra de cada frase va en mayuscula por serlo, no por ser un
    nombre — y en un chant hay tres o cuatro frases por linea ("Grandma!
    Grandpa! And the baby too!"). Por eso se corta por frases y se tira la
    primera palabra de cada una: si no, medio diccionario sale como nombre.
    """
    for linea in letra.split("\n"):
        if linea.startswith("["):                 # [Leader], [Chorus]...
            continue
        for frase in re.split(r"[.!?:;]+\s*", linea):
            palabras = re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ']+", frase)
            for w in palabras[1:]:
                if re.match(r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}$", w):
                    yield w


def revisa(nivel):
    d = json.load(io.open(os.path.join(AQUI, nivel + ".json"),
                          encoding="utf-8"))["unidades"]
    fuera, citas = {}, []
    for n in sorted(d, key=int):
        for tipo in ("chant", "cancion"):
            t = d[n][tipo]["letra"]
            for w in candidatos(t):
                if w in NO_SON or w in ELENCO:
                    continue
                fuera.setdefault(w, []).append("%s/%s" % (n, tipo))
            b = t.lower()
            for m in MINAS:
                if re.search(m, b):
                    citas.append("%s/%s cita %r" % (n, tipo, m))

    print("%s: %d piezas" % (nivel, len(d) * 2))
    if fuera:
        print("\nnombres que no estan en la biblia:")
        for w, d_ in sorted(fuera.items()):
            print("   %-12s %s" % (w, ", ".join(d_[:6])))
    else:
        print("elenco: nadie fuera de la biblia")
    if citas:
        print("\nletras que citan un tema conocido (Suno las va a rechazar):")
        for c in citas:
            print("  ", c)
    else:
        print("copyright: ninguna letra cita un tema conocido")
    return len(fuera) + len(citas)


if __name__ == "__main__":
    sys.exit(1 if revisa(sys.argv[1] if len(sys.argv) > 1 else "starters") else 0)
