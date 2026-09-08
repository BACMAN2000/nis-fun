# -*- coding: utf-8 -*-
"""Mide la progresion de complejidad entre Starters, Movers y Flyers.

Se hizo porque el corpus general (out/progresion_por_nivel.csv) daba Flyers POR
DEBAJO de Movers (8,21 vs 10,18 palabras/oracion). Esa medida mezcla en el mismo
saco cosas que no son comparables (ver `--auditoria`), asi que aqui se mide solo
el curso, campo a campo, deduplicando y sin cruzar la frontera de la coma.

Uso:
    python tools/mide_progresion.py                 # la curva de los tres niveles
    python tools/mide_progresion.py --detalle       # + desglose por unidad
    python tools/mide_progresion.py --csv out.csv
"""
import json, os, re, sys, glob, argparse
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
NIVELES = ('starters', 'movers', 'flyers')
WORDLIST = [
    os.path.join(ROOT, '..', 'nis-portal', 'yle', 'wordlist-2025.json'),
    os.path.join(ROOT, 'yle', 'wordlist-2025.json'),
]

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z'’\-]*")
# Fin de oracion: . ! ? … seguidos de espacio o final. El guion largo de los
# guiones de audio (—) tambien separa turnos.
SENT_RE = re.compile(r'(?:[.!?…]+(?:\s|$)|\s—\s)')

# Marcas de subordinacion / union de oraciones que Flyers debe usar y Starters no.
SUBORD = {
    'because', 'when', 'while', 'if', 'so', 'but', 'and', 'after', 'before',
    'until', 'although', 'though', 'that', 'which', 'who', 'whose', 'where',
    'than', 'as', 'since', 'unless', 'whether',
}
SUBORD_FUERTE = {
    'because', 'when', 'while', 'if', 'after', 'before', 'until', 'although',
    'though', 'which', 'who', 'whose', 'where', 'since', 'unless', 'whether',
}

# ---------------------------------------------------------------- clasificacion
def bucket(path):
    """Agrupa la ruta de campo en las cuatro familias de texto del curso."""
    p = path
    if p in ('scene.intro', 'scene.bubble') or p.endswith('.text') or p == 'reading':
        return 'historia'
    if p.endswith('.script') or '.script' in p:
        return 'guion'
    if p == 'title' or p.endswith('.title') or p.endswith('instructions') or p.endswith('.prompt'):
        return 'instruccion'
    if (p.endswith('.sentence') or p.endswith('.q') or p.endswith('.clue')
            or p.endswith('.defs') or p.endswith('.left') or p.endswith('.right')
            or p.endswith('.a') or p.endswith('.b') or p.endswith('.question')
            or p.endswith('.action') or p.endswith('.statement')):
        return 'ejercicio'
    return None


SALTAR = re.compile(r'(^|\.)(scope|wordlist|wordlist_extra|characters|exam_focus|'
                    r'grammar|topic|level|id|number|pose|code|type|answer|answers|'
                    r'options|words|pics|es|ipa|voice|img|audio|word)($|\.)')


def recorre(obj, path=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from recorre(v, (path + '.' + k) if path else k)
    elif isinstance(obj, list):
        for v in obj:
            yield from recorre(v, path)
    elif isinstance(obj, str):
        yield path, obj


def toks(s):
    # el apostrofe tipografico y el recto son la misma palabra: la lista oficial
    # trae «you’re» y el curso escribe «you're». Si no se unifican, la cobertura
    # marca huecos que no existen.
    s = s.replace('’', "'")
    return [t.lower().strip("'-") for t in TOKEN_RE.findall(s) if t.strip("'-")]


def oraciones(txt):
    """Devuelve las oraciones del texto. NO parte por coma: una subordinada
    separada por coma es justo lo que estamos midiendo."""
    for p in SENT_RE.split(txt):
        p = p.strip(' —-–')
        if not p:
            continue
        # los guiones de audio traen 'Ingrid: ...' — el nombre no es parte de la frase
        p = re.sub(r'^[A-Z][a-z]+\s*:\s*', '', p)
        w = toks(p)
        if 3 <= len(w) <= 60:
            yield w


def carga_wordlist():
    for c in WORDLIST:
        if os.path.exists(c):
            wl = json.load(open(c, encoding='utf-8'))
            out = {}
            for lvl in NIVELES:
                s = set()
                for e in wl[lvl]:
                    base = re.sub(r'\(.*?\)', ' ', e).strip().lower()
                    for w in toks(base):
                        # «a.m.» y «p.m.» dejaban sueltas las letras m y p, que
                        # luego salian como palabras oficiales sin usar
                        if len(w) == 1 and w not in ('a', 'i'):
                            continue
                        s.add(w)
                out[lvl] = s
            return out
    return None


def mide(nivel, raiz):
    """Recoge los textos del nivel, deduplicados por (bucket, texto normalizado)."""
    datos = defaultdict(lambda: {'txt': [], 'vistos': set()})
    por_unidad = {}
    for f in sorted(glob.glob(os.path.join(raiz, 'content', nivel, 'unit-*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        u = d.get('number')
        loc = defaultdict(list)
        for path, s in recorre(d):
            if SALTAR.search(path):
                continue
            b = bucket(path)
            if not b:
                continue
            s = s.strip()
            if len(toks(s)) < 3:
                continue
            norm = re.sub(r'\s+', ' ', s.lower())
            if norm in datos[b]['vistos']:
                continue
            datos[b]['vistos'].add(norm)
            datos[b]['txt'].append(s)
            loc[b].append(s)
        por_unidad[u] = loc
    return datos, por_unidad


def nombres_propios(textos):
    """Tokens que salen casi siempre en mayuscula = nombres propios.

    Hace falta: el 33 % de las palabras largas de los guiones de Movers eran
    130 veces «Valentina». Contar nombres de personaje como lexico dificil
    hace que el nivel con la protagonista de nombre largo parezca mas dificil.
    """
    total, caps = Counter(), Counter()
    for t in textos:
        for w in TOKEN_RE.findall(t):
            k = w.lower().strip("'’-")
            if not k:
                continue
            total[k] += 1
            if w[:1].isupper():
                caps[k] += 1
    return {k for k, n in total.items() if caps[k] >= n * 0.6 and k not in ('i',)}


def resume(textos, sin_nombres=True):
    propios = nombres_propios(textos) if sin_nombres else set()
    sent_n = sent_w = 0
    largas = 0
    tk = 0
    letras = 0
    ocho = 0
    types = set()
    types_all = set()
    sub = 0
    subf = 0
    for t in textos:
        for w in oraciones(t):
            sent_n += 1
            sent_w += len(w)
            if len(w) >= 12:
                largas += 1
            if SUBORD & set(w):
                sub += 1
            if SUBORD_FUERTE & set(w):
                subf += 1
        types_all.update(toks(t))
        ws = [x for x in toks(t) if x not in propios]
        tk += len(ws)
        letras += sum(len(x) for x in ws)
        ocho += sum(1 for x in ws if len(x) >= 8)
        types.update(ws)
    if not sent_n:
        return None
    return {
        'oraciones': sent_n,
        'palabras': tk,
        'types': len(types),
        'pal_por_oracion': round(sent_w / sent_n, 2),
        'pct_oraciones_12+': round(100 * largas / sent_n, 1),
        'pct_con_subordinada': round(100 * subf / sent_n, 1),
        'pct_compuestas': round(100 * sub / sent_n, 1),
        'letras_por_palabra': round(letras / tk, 2) if tk else 0,
        'pct_palabras_8+': round(100 * ocho / tk, 1) if tk else 0,
        '_types': types,
        '_types_all': types_all,
    }


def variantes(w):
    """Formas que cuentan como «esta palabra aparece». Sin esto, «gloves» no
    cubre «glove» y la lista oficial parece tener huecos que no tiene."""
    v = {w, w + 's', w + 'es', w + 'ing', w + 'ed'}
    if w.endswith('e'):
        v |= {w[:-1] + 'ing', w + 'd'}
    if w.endswith('y'):
        v |= {w[:-1] + 'ies', w[:-1] + 'ied'}
    if w.endswith('s'):
        v.add(w[:-1])
    if w.endswith('f'):
        v.add(w[:-1] + 'ves')
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--detalle', action='store_true')
    ap.add_argument('--csv')
    ap.add_argument('--raiz', default=ROOT)
    ap.add_argument('--json')
    a = ap.parse_args()

    wl = carga_wordlist()
    filas = []
    todo = {}
    for nivel in NIVELES:
        datos, por_unidad = mide(nivel, a.raiz)
        todos = []
        for b in ('historia', 'guion', 'ejercicio', 'instruccion'):
            todos.extend(datos[b]['txt'])
        r = resume(todos)
        r['nivel'] = nivel
        r['por_bucket'] = {}
        for b in ('historia', 'guion', 'ejercicio', 'instruccion'):
            rb = resume(datos[b]['txt'])
            if rb:
                rb.pop('_types')
                rb.pop('_types_all')
                r['por_bucket'][b] = rb
        todo[nivel] = r
        filas.append(r)

    # cobertura de la lista oficial (acumulada: Flyers puede usar las tres listas)
    if wl:
        acum = set()
        for nivel in NIVELES:
            acum |= wl[nivel]
            propia = wl[nivel]
            # la cobertura se mide con TODAS las formas (los meses y los nombres
            # de la lista oficial van en mayuscula y el filtro de nombres propios
            # se los comia) y aceptando plural/-ing/-ed
            vistas = todo[nivel]['_types_all']
            falta_p = sorted(w for w in propia if not (variantes(w) & vistas))
            falta_a = sorted(w for w in acum if not (variantes(w) & vistas))
            todo[nivel]['cobertura_propia'] = round(100 * (len(propia) - len(falta_p)) / len(propia), 1)
            todo[nivel]['cobertura_acumulada'] = round(100 * (len(acum) - len(falta_a)) / len(acum), 1)
            todo[nivel]['lista_propia_n'] = len(propia)
            todo[nivel]['lista_propia_usadas'] = len(propia) - len(falta_p)
            todo[nivel]['lista_propia_sin_usar'] = falta_p

    print('\nCURVA DEL CURSO (Fun for Nordic) — solo texto del curso, deduplicado\n')
    cab = ('nivel', 'oracion', 'pal/or', '%or 12+', '%subord', 'types', 'letras', '%8+', 'cob.propia', 'cob.acum')
    print('{:<10}{:>9}{:>9}{:>9}{:>9}{:>8}{:>8}{:>7}{:>12}{:>10}'.format(*cab))
    for nivel in NIVELES:
        r = todo[nivel]
        print('{:<10}{:>9}{:>9}{:>9}{:>9}{:>8}{:>8}{:>7}{:>11}%{:>9}%'.format(
            nivel, r['oraciones'], r['pal_por_oracion'], r['pct_oraciones_12+'],
            r['pct_con_subordinada'], r['types'], r['letras_por_palabra'],
            r['pct_palabras_8+'], r.get('cobertura_propia', '-'),
            r.get('cobertura_acumulada', '-')))

    print('\nPOR TIPO DE TEXTO (palabras por oracion)\n')
    print('{:<12}{:>12}{:>12}{:>12}'.format('bucket', *NIVELES))
    for b in ('historia', 'guion', 'ejercicio', 'instruccion'):
        fila = [b]
        for nivel in NIVELES:
            rb = todo[nivel]['por_bucket'].get(b)
            fila.append(rb['pal_por_oracion'] if rb else '-')
        print('{:<12}{:>12}{:>12}{:>12}'.format(*fila))

    print('\nPOR TIPO DE TEXTO (% de oraciones con subordinada)\n')
    print('{:<12}{:>12}{:>12}{:>12}'.format('bucket', *NIVELES))
    for b in ('historia', 'guion', 'ejercicio', 'instruccion'):
        fila = [b]
        for nivel in NIVELES:
            rb = todo[nivel]['por_bucket'].get(b)
            fila.append(rb['pct_con_subordinada'] if rb else '-')
        print('{:<12}{:>12}{:>12}{:>12}'.format(*fila))

    # monotonia
    print('\nMONOTONIA (tiene que subir Starters < Movers < Flyers)\n')
    for m in ('pal_por_oracion', 'pct_oraciones_12+', 'pct_con_subordinada',
              'types', 'letras_por_palabra', 'pct_palabras_8+'):
        v = [todo[n][m] for n in NIVELES]
        ok = v[0] <= v[1] <= v[2]
        print('  {:<22} {:>8} {:>8} {:>8}   {}'.format(m, *v, 'OK' if ok else 'RETROCESO'))
    if wl:
        v = [todo[n]['cobertura_propia'] for n in NIVELES]
        print('  {:<22} {:>8} {:>8} {:>8}'.format('cobertura_propia', *v))

    if a.json:
        for n in NIVELES:
            todo[n].pop('_types', None); todo[n].pop('_types_all', None)
        json.dump(todo, open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print('\n->', a.json)


if __name__ == '__main__':
    main()
