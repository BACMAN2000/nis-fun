# -*- coding: utf-8 -*-
"""Reparte la posicion de la respuesta correcta en las unidades de Fun for Nordic.

El problema que arregla: la clave caia en la primera opcion el 81% de las veces
(en las lecturas, el 93%), con unidades enteras de KET y PET donde las quince
respuestas eran la A. El motor no baraja al pintar —`it.options.map` en orden y
corrige con `+b.dataset.k === it.answer`—, asi que la posicion del archivo es la
posicion de la pantalla y al alumno le basta pulsar siempre la primera.

    python nis-fun/tools/reparte_claves.py [--escribe] [carpeta ...]

Sin --escribe solo informa. Por defecto recorre content/ y content-fr/.

Mueve la OPCION ENTERA de sitio y actualiza el indice: la respuesta correcta
sigue siendo la misma cadena, solo cambia donde aparece. El reparto se lleva por
unidad, que es lo que hace un alumno de una sentada, y con semilla fija: dos
ejecuciones dan el mismo resultado.

No toca:
  - picture_mc, que guarda la clave como palabra y ya salia repartido (31/32/37);
  - las preguntas cuyas opciones llevan orden propio: cifras, horas, precios,
    dias, meses, ordinales y «all/none of the above».
"""
import io, json, os, re, sys, glob, zlib, collections

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
LET = 'ABCDEFGH'

# ---------------------------------------------------------------- orden propio
DIAS = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
        'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche'}
MESES = {'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
         'september', 'october', 'november', 'december',
         'janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout',
         'septembre', 'octobre', 'novembre', 'decembre'}
ORDINALES = re.compile(r'^(first|second|third|fourth|fifth|next|then|finally|last|'
                       r'premier|première|premiere|deuxième|deuxieme|troisième|troisieme|'
                       r'ensuite|enfin|dernier)\b', re.I)
CIFRA = re.compile(r'^[£$€]?\s*\d+([.,]\d+)?\s*(%|h|am|pm|:\d\d)?$', re.I)
HORA = re.compile(r'^\d{1,2}[:.h]\d{2}\s*(a\.?m\.?|p\.?m\.?)?$', re.I)


def sin_tildes(s):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


SEC_DIAS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
SEC_DIAS_FR = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
SEC_MESES = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
             'september', 'october', 'november', 'december']
SEC_MESES_FR = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout',
                'septembre', 'octobre', 'novembre', 'decembre']
SEC_ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth',
           'ninth', 'tenth', 'next', 'then', 'finally', 'last']


def _ordenada(pos):
    """True si la lista de posiciones va de menos a mas o de mas a menos.
    Vale para cifras, donde la convencion de examen es listarlas ordenadas."""
    if any(p is None for p in pos) or len(pos) < 2:
        return False
    return pos == sorted(pos) or pos == sorted(pos, reverse=True)


def _secuencia_regular(pos):
    """Mas estricto: ademas de ordenada, con paso constante. Hace falta para
    dias, meses y ordinales: con tres opciones, salir ordenadas por casualidad
    pasa una de cada tres veces, y «Sunday, Friday, Monday» no es una secuencia
    aunque sus posiciones bajen. «Monday, Tuesday, Wednesday» si lo es."""
    if any(p is None for p in pos) or len(pos) < 2:
        return False
    pasos = {pos[i + 1] - pos[i] for i in range(len(pos) - 1)}
    return len(pasos) == 1 and 0 not in pasos


def _posiciones(bajo, secuencia):
    return [secuencia.index(v) if v in secuencia else None for v in bajo]


def orden_propio(vals):
    """Devuelve el motivo por el que NO se debe barajar, o None.

    Ojo con la trampa: que las opciones sean dias, meses o cifras no basta. Lo
    que hace intocable una pregunta es que esten EN ORDEN — «Monday, Tuesday,
    Wednesday» se lee como una secuencia y barajarla desconcierta, pero
    «Wednesday, Monday, Friday» ya venia desordenado y ahi el orden no significa
    nada. Confundir las dos cosas dejaba sin repartir seis preguntas de
    starters/unit-32 que tenian cuatro de seis claves en la A."""
    t = [v.strip() for v in vals]
    bajo = [sin_tildes(v.lower()).strip(' .!?') for v in t]

    # estas dependen de la posicion pase lo que pase
    if any(re.search(r'\b(all|none|both|neither)\s+of\s+(the|these)\b', v, re.I) for v in t):
        return 'all/none of the above'
    if any(re.search(r'\b[A-D]\s+(and|&|or)\s+[A-D]\b', v) for v in t):
        return 'cita otras opciones'

    # numeros: intocables solo si van ordenados
    def num(v):
        m = re.match(r'^[£$€]?\s*(\d+([.,]\d+)?)', v)
        return float(m.group(1).replace(',', '.')) if m else None
    if all(CIFRA.match(v) or HORA.match(v) or re.match(r'^\d', v) for v in t):
        return 'cifras en orden' if _ordenada([num(v) for v in t]) else None

    for nombre, sec in (('dias de la semana', SEC_DIAS), ('dias de la semana', SEC_DIAS_FR),
                        ('meses', SEC_MESES), ('meses', SEC_MESES_FR),
                        ('secuencia first/next/then', SEC_ORD)):
        pos = _posiciones(bajo, sec)
        if all(p is not None for p in pos):
            return nombre + ' en orden' if _secuencia_regular(pos) else None
    return None


# ------------------------------------------------------------------ generador
def generador(n, semilla):
    """Bloques [0..n-1] barajados: en cada ventana de n preguntas sale cada
    letra una vez, y nunca hay mas de dos claves iguales seguidas."""
    estado = [semilla & 0xFFFFFFFF]
    bolsa = []

    def rnd():
        estado[0] = (estado[0] * 1664525 + 1013904223) & 0xFFFFFFFF
        return estado[0] / 4294967296.0

    def siguiente():
        if not bolsa:
            b = list(range(n))
            for i in range(len(b) - 1, 0, -1):
                j = int(rnd() * (i + 1))
                b[i], b[j] = b[j], b[i]
            bolsa.extend(b)
        return bolsa.pop(0)
    return siguiente


# -------------------------------------------------------------------- recorrido
def preguntas_de(actividad):
    """Devuelve los dicts {options:[str], answer:int} de una actividad, en el
    orden en que el alumno los ve. picture_mc queda fuera a proposito."""
    fuera = []
    if actividad.get('type') == 'picture_mc':
        return fuera

    def anda(nodo):
        if isinstance(nodo, dict):
            ops = nodo.get('options')
            a = nodo.get('answer')
            if (isinstance(ops, list) and 2 <= len(ops) <= 8
                    and all(isinstance(x, str) for x in ops)
                    and isinstance(a, int) and not isinstance(a, bool)
                    and 0 <= a < len(ops)):
                fuera.append(nodo)
                return
            for v in nodo.values():
                anda(v)
        elif isinstance(nodo, list):
            for v in nodo:
                anda(v)
    anda(actividad)
    return fuera


def procesa(ruta, escribe, stats):
    crudo = io.open(ruta, 'rb').read()
    # El contenido esta mezclado: 156 unidades con CRLF y 174 con LF. Si se
    # escribe siempre LF, git marca el archivo entero como cambiado y el diff
    # real —dos lineas por pregunta— se pierde entre 400 lineas de ruido.
    fin = '\r\n' if b'\r\n' in crudo else '\n'
    raw = crudo.decode('utf-8').replace('\r\n', '\n')
    datos = json.loads(raw, object_pairs_hook=collections.OrderedDict)
    # Semilla estable por archivo. Con hash() no vale: Python lo aleatoriza en
    # cada proceso (PYTHONHASHSEED), asi que el reparto saldria distinto en cada
    # ejecucion y no habria forma de reproducirlo.
    semilla = 0x5EED + (zlib.crc32(os.path.basename(ruta).encode('utf-8')) & 0xFFFF)
    gens = {}
    antes, despues = [], []
    for act in (datos.get('activities') or []):
        for q in preguntas_de(act):
            ops, a = q['options'], q['answer']
            n = len(ops)
            antes.append((n, a))
            motivo = orden_propio(ops)
            if motivo:
                stats['saltadas'][motivo] += 1
                despues.append((n, a))
                continue
            if n not in gens:
                gens[n] = generador(n, semilla + n * 977)
            destino = gens[n]()
            despues.append((n, destino))
            if destino != a:
                ops[a], ops[destino] = ops[destino], ops[a]
                q['answer'] = destino
                stats['movidas'] += 1
            stats['tipos'][act.get('type', '?')] += 1
    for n, a in antes:
        stats['antes'][n][LET[a]] += 1
    for n, a in despues:
        stats['despues'][n][LET[a]] += 1
    stats['vistas'] += len(antes)

    if escribe and antes:
        salida = json.dumps(datos, ensure_ascii=False, indent=1)
        if raw.endswith('\n'):
            salida += '\n'
        io.open(ruta, 'wb').write(salida.replace('\n', fin).encode('utf-8'))


def main():
    args = [a for a in sys.argv[1:] if a != '--escribe']
    escribe = '--escribe' in sys.argv
    carpetas = args or [os.path.join(RAIZ, 'content'), os.path.join(RAIZ, 'content-fr')]
    stats = {'vistas': 0, 'movidas': 0,
             'antes': collections.defaultdict(collections.Counter),
             'despues': collections.defaultdict(collections.Counter),
             'saltadas': collections.Counter(), 'tipos': collections.Counter()}
    ficheros = []
    for c in carpetas:
        ficheros += sorted(glob.glob(os.path.join(c, '*', 'unit-*.json')))
    for f in ficheros:
        procesa(f, escribe, stats)

    print('unidades recorridas          : %d' % len(ficheros))
    print('preguntas de opcion multiple : %d' % stats['vistas'])
    print('claves movidas de sitio      : %d%s' % (stats['movidas'],
          '' if escribe else '   (simulacro: no se ha escrito nada)'))
    salt = ', '.join('%d %s' % (v, k) for k, v in stats['saltadas'].most_common())
    print('respetadas por orden propio  : %s' % (salt or 'ninguna'))
    print('por tipo de actividad        : %s' % ', '.join('%s %d' % (k, v) for k, v in stats['tipos'].most_common()))
    for n in sorted(stats['antes']):
        def p(c):
            t = sum(c.values()) or 1
            return ' · '.join('%s %.0f%%' % (k, 100.0 * c[k] / t) for k in sorted(c)) + '   (n=%d)' % t
        print('  %d opciones' % n)
        print('     antes   : %s' % p(stats['antes'][n]))
        print('     despues : %s' % p(stats['despues'][n]))


if __name__ == '__main__':
    main()
