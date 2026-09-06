# -*- coding: utf-8 -*-
"""
Mete en cada unidad la historia de apertura que le falta (scene.intro).

Solo 9 de las 150 unidades tenian historia escrita; las otras 141 abrian el
curso sin nada que leer ni escuchar. Los textos viven en tools/historias/*.json
—un archivo por nivel y tramo— para poder revisarlos sin abrir 141 unidades.

Antes de escribir nada comprueba tres cosas, y si falla alguna no toca el disco:
  - que la unidad existe y NO tiene ya intro (no se pisa lo escrito a mano)
  - que solo aparecen personajes de la biblia
  - que el texto tiene un largo razonable para su nivel

    python tools/aplica_historias.py --probar   dice que haria, sin escribir
    python tools/aplica_historias.py            lo aplica
"""
import io, json, glob, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, 'tools', 'historias')
CONTENT = os.path.join(ROOT, 'content')

# Los 15 de characters/bible.md. Quien no esta aqui, no sale: si un texto se
# inventa un companero, el alumno se encuentra con alguien que no tiene cara.
ELENCO = {'freya', 'nico', 'astrid', 'tomas', 'tomás', 'pip',
          'erik', 'valentina', 'sofia', 'sofía', 'mateo', 'luna',
          'ingrid', 'diego', 'maya', 'oliver', 'kili'}
# nombres que ya usaban las historias escritas a mano (familia de Nico, la
# amiga de Valentina y la dentista): estaban antes de esto y se respetan
TOLERADOS = {'rosa', 'juan', 'emma', 'ana', 'aurora', 'simon'}
LARGO = {'starters': (300, 430), 'movers': (330, 470), 'flyers': (350, 520)}
NOMBRE = re.compile(r'\b([A-Z][a-záéíóúñ]{2,})\b')

# Una palabra con mayuscula no es un nombre propio: 'Today', 'Report' o
# 'Certainly' solo estan empezando una frase. Se descartan las que existen en
# ingles, usando el diccionario del lexico (148.667 palabras). Si no esta a
# mano se avisa, porque sin el la comprobacion de elenco no vale nada.
DICC = r'C:/Projects/nis-portal/lexicon/words.txt'
INGLES = set()
if os.path.exists(DICC):
    INGLES = {l.strip() for l in io.open(DICC, encoding='utf-8') if l.strip()}
else:
    print('  [!] sin words.txt: no se puede distinguir nombre propio de palabra comun')
COMUNES = {'The','This','That','These','Those','What','Where','When','Who','Why','How',
           'And','But','Now','Then','Today','Yesterday','Tomorrow','Look','Come','Open',
           'Say','Tell','Count','Play','Put','Take','Find','Read','Write','Sit','Stand',
           'Every','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten',
           'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday',
           'January','February','March','April','May','June','July','August','September',
           'October','November','December','English','Club','Explorers','Fjord','Aurora',
           'Radio','Amazon','Nile','Round','Welcome','Question','Music','Science','Maths',
           'Art','History','Geography','Listening','Reading','Writing','Word','Games',
           'Sports','Farm','Zoo','Beach','Museum','Congratulations','Big','Nobody','Both',
           'Not','No','Yes','Atchoo','Goal','Surprise','Happy','Dear','Simon','Cafe','Café',
           'It','He','She','They','We','You','I','If','In','On','At','So','A','An','Is','Are',
           'Do','Does','Did','Has','Have','Can','Will','Would','Should','Shall','Let','PE',
           'Toy','Lunchbox','Street','Fruit','Pet','Colour','Action','Where','Which','Whose',
           'Seven','Forty','Fifty','Twenty','Thirty','Hundred','Northern','Kitchen'}

def revisa(nivel, texto):
    fallos = []
    lo, hi = LARGO[nivel]
    if not (lo <= len(texto) <= hi):
        fallos.append(f'largo {len(texto)} fuera de {lo}-{hi}')
    for m in NOMBRE.finditer(texto):
        n = m.group(1)
        if n in COMUNES or n.lower() in ELENCO or n.lower() in TOLERADOS:
            continue
        if n.lower() in INGLES:
            continue                 # palabra corriente empezando una frase
        fallos.append(f'nombre fuera de la biblia: {n}')
    return fallos

probar = '--probar' in sys.argv
puestas = saltadas = 0
problemas = []

for f in sorted(glob.glob(os.path.join(HIST, '*.json'))):
    nivel = os.path.basename(f).split('-')[0]
    textos = json.load(io.open(f, encoding='utf-8'))
    for num, texto in sorted(textos.items(), key=lambda x: int(x[0])):
        ruta = os.path.join(CONTENT, nivel, f'unit-{int(num):02d}.json')
        if not os.path.exists(ruta):
            problemas.append((nivel, num, 'no existe la unidad')); continue
        d = json.load(io.open(ruta, encoding='utf-8'))
        sc = d.get('scene')
        if not isinstance(sc, dict):
            problemas.append((nivel, num, 'la unidad no tiene scene')); continue
        if sc.get('intro'):
            saltadas += 1; continue          # escrita a mano: no se toca
        fallos = revisa(nivel, texto)
        if fallos:
            problemas.extend((nivel, num, x) for x in fallos); continue
        if not probar:
            sc['intro'] = texto
            io.open(ruta, 'w', encoding='utf-8', newline='').write(
                json.dumps(d, ensure_ascii=False, indent=1))
        puestas += 1

print(('SIMULACION — ' if probar else '') + f'historias puestas: {puestas}')
print(f'unidades que ya tenian una (intactas): {saltadas}')
print(f'problemas: {len(problemas)}')
for n, num, p in problemas[:12]:
    print(f'   {n} u{num}: {p}')
