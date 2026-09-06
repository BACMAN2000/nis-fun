# -*- coding: utf-8 -*-
"""Ata el pairwork de cada unidad a la parte del Speaking que ensaya.

Las 150 unidades tienen pairwork, asi que hablar se habla. Lo que no existia era
el mapa: nada decia que el juego de las diferencias de la u08 de Movers es la
parte 1 del examen oral, ni que la entrevista de comida de la u12 de Starters es
la parte 3. El profesor no podia buscar «quiero ensayar la parte 2» y el alumno
no sabia que lo que estaba haciendo entraba en el examen.

Las partes no son las mismas en los tres niveles (specs.json):

    Starters  1 senalar en la escena y colocar tarjetas  2 preguntas sobre la
              escena  3 preguntas sobre las tarjetas  4 preguntas personales
    Movers    1 decir cuatro diferencias  2 describir la historia en imagenes
              3 el intruso y por que  4 preguntas personales
    Flyers    1 seis diferencias a partir de lo que dice el examinador
              2 intercambio de informacion con fichas  3 la historia en
              imagenes  4 preguntas personales

Se clasifica por la MECANICA del pairwork, no por el tema: quien describe y
quien dibuja, quien pregunta y quien contesta, si hay que contar una historia en
orden o si hay que hablar de uno mismo. Lo que la regla no acierta va en
MANUAL, unidad por unidad.

    python tools/pairwork_speaking.py --check
    python tools/pairwork_speaking.py --tabla     reparto por nivel y parte
    python tools/pairwork_speaking.py
"""
import glob, io, json, os, re, sys

REPOS = [r'C:\Projects\nis-portal\nis-fun', r'C:\Projects\nis-fun']

# nombre de cada parte, por nivel, para escribirlo en la unidad
PARTES = {
 'starters': {1: 'Scene picture and object cards', 2: 'Questions about the scene',
              3: 'Questions about object cards', 4: 'Personal questions'},
 'movers':   {1: 'Find four differences', 2: 'Describe the picture story',
              3: 'Odd one out, and why', 4: 'Personal questions'},
 'flyers':   {1: 'Find six differences', 2: 'Information exchange with cards',
              3: 'Describe the picture story', 4: 'Personal questions'},
}

# La parte que ensaya cada mecanica. El orden importa: gana la primera que casa.
REGLAS = [
 # contar una historia en orden -> la de la secuencia de imagenes
 (r'story chain|retell|tell the story|in exactly \d+ sentences|one sentence each|'
  r'what happens next|invent a story|make up a story|three pictures|picture story', 'historia'),
 # decir en que se diferencian dos cosas -> la de las diferencias
 (r'differen|partner draws|draws it|draw the same|spot the|compare (?:two|your)', 'diferencias'),
 # el intruso
 (r'odd one out|which one does not|doesn\u2019t belong|does not belong', 'intruso'),
 # adivinar y mimar es describir sin nombrar: va con la de describir
 (r'guess(?:es)?|mime|without saying', 'diferencias'),
 # preguntar y contestar con datos, fichas, encuestas -> intercambio / tarjetas
 (r'interview|survey|ask (?:your partner |three classmates |\d+ )?(?:\d+ )?questions|'
  r'yes/no questions|find out|swap|card', 'fichas'),
 # hablar de uno mismo
 (r'about you|your favourite|tell (?:the class|us) about your|your weekend|your family|'
  r'your day|your room|your house|your plan|what do you (?:like|do)|describe your', 'personal'),
 # senalar y describir lo que hay en una escena
 (r'point at|look around|in the classroom|where is|put the|place the|describe (?:it|the picture)', 'escena'),
]

# mecanica -> parte, segun el nivel
MAPA = {
 'starters': {'escena': 1, 'diferencias': 2, 'historia': 2, 'fichas': 3, 'intruso': 3, 'personal': 4},
 'movers':   {'diferencias': 1, 'historia': 2, 'intruso': 3, 'fichas': 3, 'escena': 1, 'personal': 4},
 'flyers':   {'diferencias': 1, 'fichas': 2, 'historia': 3, 'intruso': 2, 'escena': 1, 'personal': 4},
}

# Lo que la regla no acierta. Se mira el pairwork y se decide a mano.
MANUAL = {
 # Starters: senalar/colocar (1), hablar de la escena (2), las tarjetas (3), uno mismo (4)
 ('starters', 1): 1, ('starters', 5): 1, ('starters', 7): 1, ('starters', 11): 1,
 ('starters', 21): 1, ('starters', 25): 1, ('starters', 29): 1, ('starters', 43): 1,
 ('starters', 9): 2, ('starters', 18): 2, ('starters', 19): 2, ('starters', 31): 2,
 ('starters', 2): 3, ('starters', 16): 3, ('starters', 20): 3, ('starters', 30): 3,
 ('starters', 38): 3, ('starters', 40): 3, ('starters', 42): 3,
 ('starters', 15): 4, ('starters', 22): 4, ('starters', 28): 4, ('starters', 33): 4,
 ('starters', 34): 4, ('starters', 35): 4, ('starters', 36): 4, ('starters', 44): 4,
 # Movers: diferencias (1), la historia en imagenes (2), el intruso (3), uno mismo (4)
 ('movers', 12): 1, ('movers', 21): 1, ('movers', 30): 1, ('movers', 31): 1, ('movers', 43): 1,
 ('movers', 20): 2, ('movers', 23): 2, ('movers', 28): 2, ('movers', 41): 2,
 ('movers', 42): 2, ('movers', 47): 2,
 ('movers', 48): 3,
 ('movers', 11): 4, ('movers', 14): 4, ('movers', 16): 4, ('movers', 24): 4,
 ('movers', 26): 4, ('movers', 34): 4, ('movers', 38): 4, ('movers', 44): 4,
 ('movers', 49): 4, ('movers', 50): 4,
 # Flyers: diferencias (1), intercambio con fichas (2), la historia (3), uno mismo (4)
 ('flyers', 9): 1, ('flyers', 45): 1,
 ('flyers', 7): 2, ('flyers', 8): 2, ('flyers', 10): 2, ('flyers', 13): 2,
 ('flyers', 16): 2, ('flyers', 18): 2, ('flyers', 22): 2, ('flyers', 26): 2, ('flyers', 33): 2,
 ('flyers', 19): 3, ('flyers', 23): 3, ('flyers', 28): 3, ('flyers', 32): 3,
 ('flyers', 39): 3, ('flyers', 47): 3, ('flyers', 55): 3,
 ('flyers', 38): 4, ('flyers', 42): 4, ('flyers', 51): 4, ('flyers', 54): 4,
}


def parte(level, n, texto):
    if (level, n) in MANUAL:
        return MANUAL[(level, n)]
    t = (texto or '').lower()
    for pat, mec in REGLAS:
        if re.search(pat, t):
            return MAPA[level][mec]
    return None


def recorre(repo):
    for level in ('starters', 'movers', 'flyers'):
        for f in sorted(glob.glob(os.path.join(repo, 'content', level, 'unit-*.json'))):
            d = json.load(io.open(f, encoding='utf-8'))
            pw = [a for a in d['activities'] if a['type'] == 'pairwork']
            yield f, d, level, (pw[0] if pw else None)


def main():
    check = '--check' in sys.argv
    if '--tabla' in sys.argv:
        for f, d, level, pw in recorre(REPOS[0]):
            pass
        import collections
        for level in ('starters', 'movers', 'flyers'):
            c = collections.Counter()
            sin = []
            for f, d, lv, pw in recorre(REPOS[0]):
                if lv != level: continue
                p = parte(lv, d['number'], (pw or {}).get('data', {}).get('text'))
                c[p] += 1
                if p is None: sin.append(d['number'])
            print('%-9s %s   sin clasificar: %s' % (level, dict(sorted(c.items(), key=lambda x: str(x[0]))), sin))
        return
    for repo in REPOS:
        if not os.path.isdir(repo):
            print('!! no existe %s' % repo); continue
        n = sin = 0
        for f, d, level, pw in recorre(repo):
            if not pw: continue
            p = parte(level, d['number'], pw['data'].get('text'))
            if p is None:
                sin += 1; continue
            nuevo = {'part': p, 'name': PARTES[level][p]}
            if pw.get('speaking') != nuevo:
                pw['speaking'] = nuevo
                n += 1
                if not check:
                    with io.open(f, 'w', encoding='utf-8', newline='') as fh:
                        json.dump(d, fh, ensure_ascii=False, indent=1)
        print('%s: %d pairwork atados%s' % (repo, n, ' · %d sin clasificar' % sin if sin else ''))


if __name__ == '__main__':
    main()
