# -*- coding: utf-8 -*-
"""Repasa las unidades de Fun for Nordic buscando la misma clase de fallos que
salieron en los examenes YLE: preguntas con dos respuestas validas, claves que
no estan entre las opciones, respuestas que el audio no dice, y datos que el
motor pinta mal.

    python nis-fun/tools/audita_curso.py [carpeta]   (por defecto ../content)
"""
import io, json, os, re, sys, glob

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(AQUI), 'content')

GRAVE, MEDIO, LEVE = [], [], []
def apunta(nivel, u, act, msg):
    nivel.append('%-16s %-14s %s' % (u, act, msg))

def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', str(s).lower()).strip()

def pal(x):
    return re.compile(chr(92) + 'b' + re.escape(x) + chr(92) + 'b', re.I)


UNIDAD = {}
def revisa(unidad, a):
    t = a.get('type')
    d = a.get('data') or {}
    act = '%s/%s' % (a.get('code') or '-', t)

    # ---- opciones con indice: exam_task, reading ----
    for it in (d.get('items') or []) if t == 'exam_task' else (d.get('questions') or []) if t == 'reading' else []:
        ops = it.get('options') or []
        k = it.get('answer')
        enun = it.get('sentence') or it.get('q') or ''
        if not isinstance(k, int) or not (0 <= k < len(ops)):
            apunta(GRAVE, unidad, act, 'clave fuera de las opciones (%r de %d): %s' % (k, len(ops), enun[:50]))
            continue
        if len(ops) < 3:
            apunta(MEDIO, unidad, act, 'solo %d opciones: %s' % (len(ops), enun[:50]))
        vistas = [str(o).strip().lower() for o in ops]
        if len(set(vistas)) != len(vistas):
            apunta(GRAVE, unidad, act, 'dos opciones iguales %s: %s' % (ops, enun[:40]))
        citado = ('"' + str(ops[k]) + '"') in str(enun) or ('«' + str(ops[k]) + '»') in str(enun)
        if enun and not citado and pal(norm(ops[k])).search(norm(enun)) and len(norm(ops[k])) > 3:
            apunta(MEDIO, unidad, act, 'el enunciado ya dice la respuesta «%s»: %s' % (ops[k], enun[:50]))

    # ---- picture_mc: la clave es la palabra ----
    if t == 'picture_mc':
        for q in (d.get('questions') or []):
            opciones = q.get('options') or []
            # `v` es lo que responde la opcion; el resto describe el dibujo (palabra,
            # personaje y pose, o la hora del reloj)
            vals = [o.get('v', o.get('word')) if isinstance(o, dict) else o for o in opciones]
            dibujos = [tuple(sorted((kk, str(vv)) for kk, vv in o.items() if kk not in ('v', 'pie', 'propio')))
                       if isinstance(o, dict) else (o,) for o in opciones]
            k = q.get('answer')
            if k not in vals:
                apunta(GRAVE, unidad, act, 'la respuesta «%s» no esta entre las opciones %s' % (k, vals))
            if len(set(str(x).strip().lower() for x in vals)) != len(vals):
                apunta(GRAVE, unidad, act, 'dos opciones dicen lo mismo %s' % vals)
            if len(set(dibujos)) != len(dibujos):
                apunta(GRAVE, unidad, act, 'dos opciones con el mismo dibujo: %s' % vals)
            sc = (q.get('script') or '') + ' ' + (d.get('script') or '')
            NUM = {'0':'zero','1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven',
                   '8':'eight','9':'nine','10':'ten','11':'eleven','12':'twelve'}
            formas = [k] + ([NUM[str(k)]] if str(k) in NUM else [])
            if k and sc and not any(pal(str(x)).search(sc) for x in formas):
                apunta(MEDIO, unidad, act, 'el audio no dice la respuesta «%s»' % k)

    # ---- listening: hueco con respuesta ----
    if t == 'listening':
        sc = d.get('script') or ''
        for q in (d.get('questions') or []):
            r = q.get('answer')
            if not str(r or '').strip():
                apunta(GRAVE, unidad, act, 'pregunta sin respuesta: %s' % str(q.get('q'))[:50])
            elif sc and not pal(str(r)).search(sc):
                apunta(MEDIO, unidad, act, 'el audio no dice la respuesta «%s»' % r)

    # ---- match_words: dos significados iguales = dos respuestas validas ----
    if t == 'match_words':
        pares = d.get('pairs') or []
        izq = [norm(p.get('left')) for p in pares]
        der = [norm(p.get('right')) for p in pares]
        if len(set(izq)) != len(izq):
            apunta(GRAVE, unidad, act, 'la misma palabra dos veces: %s' % [x for x in izq if izq.count(x) > 1][:2])
        exactos = [str(p.get('right') or '').strip().lower() for p in pares]
        if len(set(exactos)) != len(exactos):
            apunta(GRAVE, unidad, act, 'el mismo significado, palabra por palabra, para dos entradas')
        elif len(set(der)) != len(der):
            apunta(MEDIO, unidad, act, 'dos significados que solo se distinguen por un signo: %s' % [x for x in der if der.count(x) > 1][:1])
        for p in pares:
            if not str(p.get('left') or '').strip() or not str(p.get('right') or '').strip():
                apunta(GRAVE, unidad, act, 'par incompleto: %s' % p)

    # ---- spot_diff: las diferencias marcadas tienen que ser las de verdad ----
    if t == 'spot_diff':
        A, B = d.get('sceneA') or [], d.get('sceneB') or []
        hay_fotos = os.path.exists(os.path.join(os.path.dirname(BASE), 'assets', 'spot-diff',
                                                '%s-%s-diffs.json' % (UNIDAD.get('level'), UNIDAD.get('number'))))
        if not A and not B:
            if not hay_fotos:
                apunta(GRAVE, unidad, act, 'ni fotos generadas ni rejilla de emoji: la actividad sale vacia')
        elif len(A) != len(B) or any(len(x) != len(y) for x, y in zip(A, B)):
            apunta(GRAVE, unidad, act, 'las dos rejillas no tienen la misma forma')
        else:
            reales = set((i, j) for i, fila in enumerate(A) for j, c in enumerate(fila) if c != B[i][j])
            dichas = set((x[0], x[1]) for x in (d.get('diffs') or []))
            if reales != dichas:
                falta = sorted(reales - dichas); sobra = sorted(dichas - reales)
                apunta(GRAVE, unidad, act, 'diferencias mal marcadas: %d de verdad, %d apuntadas%s%s' % (
                    len(reales), len(dichas),
                    ' · sin marcar ' + str(falta) if falta else '',
                    ' · marcada y no lo es ' + str(sobra) if sobra else ''))

    # ---- crossword: los cruces tienen que dar la misma letra ----
    if t == 'crossword':
        rejilla, choques = {}, []
        palabras = d.get('words') or []
        if len(set(w.get('word') for w in palabras)) != len(palabras):
            apunta(GRAVE, unidad, act, 'la misma palabra dos veces en el crucigrama')
        # sin row/col el motor los coloca solo (engine/crossword-layout.js, determinista
        # y compartido con el libro en papel); solo se revisa la rejilla escrita a mano
        manuales = [w for w in palabras if w.get('row') is not None]
        if manuales and len(manuales) != len(palabras):
            apunta(GRAVE, unidad, act, '%d palabras con posicion y %d sin ella: la rejilla saldra a medias' % (len(manuales), len(palabras) - len(manuales)))
        for w in (manuales if len(manuales) == len(palabras) else []):
            pw, r, c, dirr = str(w.get('word') or ''), w.get('row'), w.get('col'), w.get('dir')
            if dirr not in ('across', 'down'):
                apunta(GRAVE, unidad, act, 'palabra sin direccion: %s' % pw); continue
            for k, ch in enumerate(pw):
                pos = (r, c + k) if dirr == 'across' else (r + k, c)
                if pos in rejilla and rejilla[pos] != ch:
                    choques.append('%s en %s: %s vs %s' % (pw, pos, rejilla[pos], ch))
                rejilla[pos] = ch

        for w in palabras:
            pw = str(w.get('word') or '')
            if pw and str(w.get('clue') or '') and pal(pw).search(str(w.get('clue'))):
                apunta(MEDIO, unidad, act, 'la pista de «%s» dice la palabra' % pw)
        for x in choques[:3]:
            apunta(GRAVE, unidad, act, 'el crucigrama no cuadra: %s' % x)

    # ---- gap_text: huecos y respuestas ----
    if t == 'gap_text':
        txt = d.get('text') or ''
        huecos = [int(x) for x in re.findall(r'\{(\d+)\}', txt)]
        ans = d.get('answers') or []
        if sorted(huecos) != list(range(1, len(ans) + 1)):
            apunta(GRAVE, unidad, act, '%d huecos (%s) para %d respuestas' % (len(huecos), sorted(huecos), len(ans)))
        caja = [norm(x) for x in (d.get('box') or [])]
        if caja:
            for r in ans:
                if norm(r) not in caja:
                    apunta(GRAVE, unidad, act, 'la respuesta «%s» no esta en el banco de palabras' % r)

    # ---- label_people: tienen que sobrar nombres ----
    if t == 'label_people':
        gente = [p.get('name') for p in (d.get('people') or [])]
        names = d.get('names') or []
        faltan = [g for g in gente if g not in names]
        if faltan:
            apunta(GRAVE, unidad, act, 'personas que no estan en la lista de nombres: %s' % faltan)
        if len(set(names)) != len(names):
            apunta(GRAVE, unidad, act, 'un nombre repetido en la lista')
        if len(names) <= len(gente):
            apunta(MEDIO, unidad, act, '%d nombres para %d personas: no sobra ninguno' % (len(names), len(gente)))
        sc = d.get('script') or ''
        for p in (d.get('people') or []):
            if sc and p.get('name') and not pal(p['name']).search(sc):
                apunta(GRAVE, unidad, act, 'el audio no nombra a «%s»' % p['name'])

    # ---- match_pictures ----
    if t == 'match_pictures':
        ids = [p.get('id') for p in (d.get('pictures') or [])]
        ans = d.get('answers') or []
        vals = list(ans.values()) if isinstance(ans, dict) else ans
        for v in vals:
            if v not in ids:
                apunta(GRAVE, unidad, act, 'la respuesta «%s» no es ninguna imagen (%s)' % (v, ids))
        if len(set(map(str, vals))) != len(vals):
            apunta(GRAVE, unidad, act, 'dos personas con la misma imagen: %s' % vals)
        if len(ids) <= len(vals):
            apunta(MEDIO, unidad, act, '%d imagenes para %d personas: no sobra ninguna' % (len(ids), len(vals)))

    # ---- key_transform ----
    if t == 'key_transform':
        for it in (d.get('items') or []):
            for r in (it.get('answers') or []):
                if not (2 <= len(str(r).split()) <= 5):
                    apunta(GRAVE, unidad, act, 'la respuesta «%s» no cabe en dos a cinco palabras' % r)
            if it.get('key') and it.get('answers') and not any(pal(it['key']).search(str(r)) for r in it['answers']):
                apunta(MEDIO, unidad, act, 'la palabra clave «%s» no aparece en la respuesta' % it['key'])


def main():
    unidades = sorted(glob.glob(os.path.join(BASE, '*', 'unit-*.json')))
    for f in unidades:
        u = json.load(io.open(f, encoding='utf-8'))
        nombre = os.path.basename(os.path.dirname(f)) + '/' + os.path.basename(f).replace('.json', '').replace('unit-', 'u')
        UNIDAD.clear(); UNIDAD.update({'level': u.get('level'), 'number': u.get('number')})
        for a in (u.get('activities') or []):
            revisa(nombre, a)
    print('=' * 74)
    print('AUDITORIA DEL CURSO \u2014 %d unidades, %d avisos' % (len(unidades), len(GRAVE) + len(MEDIO) + len(LEVE)))
    for titulo, lista in (('GRAVE (rompe la actividad)', GRAVE), ('MEDIO (revisar)', MEDIO), ('LEVE', LEVE)):
        print('\n--- %s: %d' % (titulo, len(lista)))
        for x in lista[:60]:
            print('   ', x)
        if len(lista) > 60:
            print('    ... y %d mas' % (len(lista) - 60))


if __name__ == '__main__':
    main()
