# -*- coding: utf-8 -*-
"""Sube el nivel de Flyers metiendo un parrafo mas en la historia de cada unidad.

Por que: medido sobre el propio curso (tools/mide_progresion.py), el escalon de
Movers a Flyers era casi plano —la historia subia +1,17 palabras por oracion de
Starters a Movers y solo +0,64 de Movers a Flyers— y 132 palabras de la lista
oficial de Flyers no aparecian en ningun texto del curso. Los parrafos estan en
tools/flyers_nivel/intro-extra.json y llevan ese vocabulario y las subordinadas
del nivel.

Como escribe: NO reserializa el JSON. Busca el ancla dentro del archivo en
crudo e inserta el texto detras, asi el diff son las 55 lineas de las historias
y no las 20.000 del reformateo. Se aplica a las DOS copias del curso.

Antes de tocar el disco comprueba TODO (anclas, elenco, duplicados). Si algo
falla no escribe nada: mejor no aplicar que dejar la mitad.

    python tools/sube_flyers.py --probar    dice que haria
    python tools/sube_flyers.py             lo aplica a las dos copias
"""
import json, os, re, sys, argparse

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(ROOT, 'tools', 'flyers_nivel', 'intro-extra.json')
COPIAS = [
    os.path.join(ROOT, 'content', 'flyers'),
    os.path.join(os.path.dirname(ROOT), 'nis-portal', 'nis-fun', 'content', 'flyers'),
]

# Los cinco de Flyers en characters/bible.md. Quien no este aqui no sale.
ELENCO = {'Ingrid', 'Diego', 'Maya', 'Oliver', 'Kili'}
MAYUS = re.compile(r'\b([A-Z][a-z]{1,})\b')

# Una palabra con mayuscula no es un nombre propio: 'Today' o 'Another' solo
# estan empezando una frase. Se descartan las que existen en ingles, con el
# diccionario del lexicon (148.672 formas). Sin el, la comprobacion no vale y se
# avisa en vez de dar por bueno cualquier nombre. Mismo criterio que
# tools/aplica_historias.py.
DICC = os.path.join(os.path.dirname(ROOT), 'nis-portal', 'lexicon', 'words.txt')
INGLES = set()
if os.path.exists(DICC):
    INGLES = {l.strip().lower() for l in open(DICC, encoding='utf-8') if l.strip()}
MESES = {'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
         'september', 'october', 'november', 'december', 'monday', 'tuesday',
         'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}


def esc(s):
    """El mismo texto tal y como aparece dentro del JSON en crudo."""
    return json.dumps(s, ensure_ascii=False)[1:-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--probar', action='store_true')
    a = ap.parse_args()

    datos = json.load(open(DATOS, encoding='utf-8'))['unidades']
    problemas, plan = [], []
    if not INGLES:
        problemas.append('sin %s: no se puede distinguir nombre propio de '
                         'palabra comun, no se aplica nada' % DICC)

    for carpeta in COPIAS:
        if not os.path.isdir(carpeta):
            problemas.append('no existe la copia %s' % carpeta)
            continue
        for e in datos:
            f = os.path.join(carpeta, 'unit-%02d.json' % e['u'])
            if not os.path.exists(f):
                problemas.append('%s: no existe' % f)
                continue
            crudo = open(f, encoding='utf-8').read()
            d = json.loads(crudo)
            intro = (d.get('scene') or {}).get('intro') or ''
            if not intro:
                problemas.append('u%02d %s: sin scene.intro' % (e['u'], carpeta))
                continue
            if e['extra'] in intro:
                continue                      # ya aplicado: idempotente
            if intro.count(e['tras']) != 1:
                problemas.append('u%02d %s: el ancla aparece %d veces'
                                 % (e['u'], carpeta, intro.count(e['tras'])))
                continue
            # elenco: ningun nombre propio nuevo
            fuera = {w for w in MAYUS.findall(e['extra'])
                     if w not in ELENCO and w.lower() not in INGLES
                     and w.lower() not in MESES}
            if fuera:
                problemas.append('u%02d: nombres fuera de la biblia: %s'
                                 % (e['u'], ', '.join(sorted(fuera))))
                continue
            ta, ex = esc(e['tras']), esc(' ' + e['extra'])
            if crudo.count(ta) != 1:
                problemas.append('u%02d %s: el ancla no es unica en el archivo'
                                 % (e['u'], carpeta))
                continue
            plan.append((f, crudo.replace(ta, ta + ex, 1)))

    if problemas:
        print('NO SE ESCRIBE NADA. %d problema(s):' % len(problemas))
        for p in problemas:
            print('  -', p)
        sys.exit(1)

    if not plan:
        print('Nada que hacer: las dos copias ya lo tienen.')
        return

    print('%d archivo(s) a tocar%s' % (len(plan), ' (prueba)' if a.probar else ''))
    for f, nuevo in plan:
        print('  ', f)
        if not a.probar:
            with open(f, 'w', encoding='utf-8', newline='') as fh:
                fh.write(nuevo)
    if not a.probar:
        print('Hecho. Recuerda subir CONTENT_V en engine/index.html de las dos copias.')


if __name__ == '__main__':
    main()
