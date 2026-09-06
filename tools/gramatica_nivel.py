# -*- coding: utf-8 -*-
"""Las cinco estructuras que el curso daba en el nivel equivocado.

La auditoria cruzo la Grammar and Structures List del Handbook 2024 con lo que
ensena cada unidad. Cinco estructuras estaban fuera de sitio, y se comprobo una
por una contra los sample papers oficiales (los dos volumenes, mirando en que
nivel cae cada pagina):

    would like        Cambridge: Starters   ·  en las muestras sale ya en
                      Starters ("Would you like to colour it pink?") y cinco
                      veces en Movers. El curso no la daba hasta Movers u17:
                      un nino de Starters se la encuentra sin haberla visto.
    relative clauses  Cambridge: Movers     ·  en las muestras sale en Movers
                      ("This person helps people who aren't well", "The man
                      who is riding the motorbike"), y en la clave del
                      Speaking de Movers. El curso solo la daba en Flyers u48.
    be going to       Cambridge: Flyers     ·  en las muestras, solo Flyers.
                      El curso la daba en Movers u02 y u36.
    should            Cambridge: Flyers     ·  no sale ni una vez como modal
                      en las muestras. El curso la daba en Movers u26.
    What time ...?    Cambridge: Flyers     ·  en las muestras, solo Flyers.
                      El curso la daba en Movers u33.

Y una que sobra: Flyers u47 ensenaba el first conditional, cuando la lista de
A2 solo pide el zero conditional.

Los dos huecos de verdad (would like y relative clauses) se tapan ensenandolas
donde tocan, con una caja de gramatica. Las tres adelantadas no se borran del
todo: dejan de ser la gramatica declarada de una unidad de Movers y de ser lo
que la unidad hace practicar, pero siguen sonando en el dialogo, que es entrada
y no objetivo. Eso queda escrito en el campo grammar_ahead, que el motor
ensena al alumno y el libro al profesor: mejor un desajuste documentado que uno
callado.

El guion del audio (la actividad C) no se toca en ninguna unidad: esos mp3 los
graba ElevenLabs y su cuota esta para otra cosa. Todo lo demas que cambia
—intro, bocadillo e instrucciones— se regraba gratis con Edge TTS.

    python tools/gramatica_nivel.py --check
    python tools/gramatica_nivel.py
"""
import io, json, os, sys

REPOS = [r'C:\Projects\nis-portal\nis-fun',   # la copia que sirve nis.cohasset.pe
         r'C:\Projects\nis-fun']              # el repo suelto, el que va a Pages

CAMB = 'Cambridge'


# --------------------------------------------------------------- cajas nuevas
CAJAS = [
{
 'level': 'starters', 'unit': 14, 'code': 'G', 'id': 'would_like',
 'structure': 'Would like + noun or verb',
 'title': 'Grammar \u00b7 Would you like\u2026?',
 'instructions': 'Read the sentences. Then choose the right word.',
 'data': {
  'title': 'Would you like a drink?',
  'intro': 'You ask for something with <b>Can I have\u2026?</b> You <i>offer</i> something with <b>Would you like\u2026?</b> Both are polite, and the exam loves them.',
  'can': 'I can offer a drink with <b>Would you like\u2026?</b> and answer <b>Yes, please</b> or <b>No, thank you</b>.',
  'examples': [
   {'text': 'I would like some grapes. <b>Would you like</b> to colour that ball?', 'note': CAMB},
   {'text': '<b>Would you like</b> an apple? \u2014 Yes, please. Here you are.', 'note': CAMB},
   {'text': 'Astrid: <b>Would you like</b> some milk? \u2014 Nico: No, thank you. I would like water.'},
   {'text': "<b>Would you like</b> to play with my ball? \u2014 Yes, please!"},
  ],
  'rules': [
   '<b>Would you like</b> + a thing: <i>Would you like an apple?</i>',
   '<b>Would you like</b> + <b>to</b> + verb: <i>Would you like to play?</i>',
   'Two answers, and both are polite: <b>Yes, please.</b> / <b>No, thank you.</b>',
  ],
  'practice': {'instructions': 'Choose the right word.', 'items': [
   {'sentence': '___ you like some milk?', 'options': ['Are', 'Would', 'Do you'], 'answer': 1},
   {'sentence': 'Would you like ___ apple?', 'options': ['a', 'an', 'the'], 'answer': 1},
   {'sentence': 'Would you like ___ play with my ball?', 'options': ['to', 'for', 'and'], 'answer': 0},
   {'sentence': '\u2014 Would you like some cake? \u2014 ___', 'options': ['Yes, I would like.', 'Yes, please!', 'Yes, I do like.'], 'answer': 1},
   {'sentence': 'I ___ like some water, please.', 'options': ['am', 'would', 'do'], 'answer': 1},
  ]},
 },
},
{
 'level': 'movers', 'unit': 22, 'code': 'G', 'id': 'relative_clauses',
 'structure': 'Relative clauses (who, which, where)',
 'title': 'Grammar \u00b7 The girl who is riding a bike',
 'instructions': 'Read the sentences. Then choose the right word.',
 'data': {
  'title': 'One sentence, not two',
  'intro': 'Two short sentences about the same person? Join them with <b>who</b>. For a thing use <b>which</b>, for a place use <b>where</b>. In the Speaking test this is how you say which person you mean.',
  'can': 'I can join two sentences with <b>who</b>, <b>which</b> and <b>where</b> to say exactly which person, thing or place I mean.',
  'examples': [
   {'text': 'Vicky is the girl <b>who</b> is riding a bike.', 'note': CAMB},
   {'text': 'This person helps people <b>who</b> aren\u2019t well.', 'note': CAMB},
   {'text': 'My friend is the boy <b>who</b> has got curly hair and a green shirt.'},
   {'text': 'That\u2019s the shop <b>which</b> has the best bread, next to the park <b>where</b> we play.'},
  ],
  'rules': [
   '<b>who</b> for people \u00b7 <b>which</b> for things and animals \u00b7 <b>where</b> for places.',
   'The joining word comes straight after the person or thing: <i>the girl <b>who</b>\u2026</i>, not <i>the girl she\u2026</i>',
   'Do not say the person twice: never <i>the girl who she is riding a bike</i>.',
  ],
  'practice': {'instructions': 'Choose the right word.', 'items': [
   {'sentence': "Sofia is the girl ___ has got long black hair.", 'options': ['which', 'who', 'where'], 'answer': 1},
   {'sentence': 'That is the bike ___ my grandma gave me.', 'options': ['which', 'who', 'when'], 'answer': 0},
   {'sentence': 'This is the park ___ we play football on Saturdays.', 'options': ['who', 'which', 'where'], 'answer': 2},
   {'sentence': 'A doctor is a person ___ helps you when you are ill.', 'options': ['where', 'who', 'which'], 'answer': 1},
   {'sentence': 'Which one is right?', 'options': ['The boy who he is running.', 'The boy who is running.', 'The boy which is running.'], 'answer': 1},
  ]},
 },
},
{
 'level': 'flyers', 'unit': 47, 'code': 'L', 'id': 'if_zero',
 'structure': 'If clauses (zero conditional)',
 'title': 'Grammar \u00b7 If it\u2019s sunny, we go swimming',
 'instructions': 'Read the sentences. Then choose the right form.',
 'data': {
  'title': 'Two kinds of if',
  'intro': 'This unit is full of plans for <i>next</i> Saturday. But there is another <b>if</b>, the one for what is <b>always</b> true \u2014 and that is the one the Flyers exam asks for.',
  'can': 'I can tell the two kinds of <b>if</b> apart: what always happens, and what we will do this time.',
  'examples': [
   {'text': '<b>If it\u2019s sunny, we go swimming.</b> \u2014 always, every sunny day.', 'note': CAMB},
   {'text': 'If Kili smells biscuits, he <b>comes</b> to the window. It happens every time.'},
   {'text': 'If it rains on Saturday, we<b>\u2019ll</b> do the quiz inside. \u2014 just this Saturday.'},
   {'text': 'If you open the door, the light <b>comes</b> on. Try it!'},
  ],
  'rules': [
   'Always true \u2192 present in <b>both</b> halves: <i>If it\u2019s sunny, we <b>go</b> swimming.</i>',
   'A plan for one day \u2192 present + <b>will</b>: <i>If it rains, we<b>\u2019ll</b> stay inside.</i>',
   'Either way, <b>never put will after if</b>. The <i>will</i> goes in the other half.',
  ],
  'practice': {'instructions': 'Choose the right form.', 'items': [
   {'sentence': 'If you leave ice in the sun, it ___ into water. It always does.', 'options': ['will change', 'changes', 'changed'], 'answer': 1},
   {'sentence': 'If it ___ sunny, we go swimming. That is what we always do.', 'options': ['is', 'will be', 'was'], 'answer': 0},
   {'sentence': 'If it rains tomorrow, we ___ the picnic inside.', 'options': ['have', 'will have', 'had'], 'answer': 1},
   {'sentence': 'Which one is right?', 'options': ['If it will rain, we stay inside.', 'If it rains, we stay inside.', 'If it rain, we will stayed inside.'], 'answer': 1},
   {'sentence': 'Luna runs to the door if she ___ my bike. Every time!', 'options': ['hear', 'will hear', 'hears'], 'answer': 2},
  ]},
 },
},
]


# ------------------------------------------------- lo que cambia en cada unidad
# (nivel, unidad) -> {campo: valor} para los campos sueltos, y CAMBIOS de texto
CAMPOS = {
 ('starters', 14): {'grammar': 'Can I have\u2026? / Would you like\u2026?'},
 ('movers', 22):   {'grammar': 'adjectives + have got \u00b7 the person who\u2026'},
 ('movers', 2):    {'grammar': 'What is the weather like? + weather words',
                    'grammar_ahead': {'structure': 'be going to', 'level': 'flyers', 'unit': 43,
                        'nota': 'Suena en el dialogo de Erik y Sofia, pero no se practica: es de A2 Flyers.'}},
 ('movers', 26):   {'grammar': "What's the matter? + must / mustn't (health advice)",
                    'grammar_ahead': {'structure': 'should / shouldn\u2019t', 'level': 'flyers', 'unit': 6,
                        'nota': 'Suena dos veces en el dialogo de la dentista, pero no se practica: es de A2 Flyers.'}},
 ('movers', 33):   {'grammar': "o'clock / half past \u00b7 When\u2026?",
                    'grammar_ahead': {'structure': 'What time does\u2026?', 'level': 'flyers', 'unit': 18,
                        'nota': 'Preguntar la hora de algo con «What time does\u2026?» es de A2 Flyers; aqui basta «When\u2026?».'}},
 ('movers', 36):   {'grammar': 'want to / would like to (plans and wishes)',
                    'topic': 'plans & wishes',
                    'title': 'The surprise party',
                    'grammar_ahead': {'structure': 'be going to', 'level': 'flyers', 'unit': 43,
                        'nota': 'Suena en el plan secreto de Erik y Valentina, pero no se practica: es de A2 Flyers.'}},
 ('flyers', 47):   {'grammar': 'if + present: zero conditional (always) \u00b7 first conditional (this time)',
                    'grammar_ahead': {'structure': 'first conditional (if + present, will)', 'level': 'b1',
                        'nota': 'La lista de A2 Flyers solo pide el zero conditional; el first conditional ya es B1. Se ensena porque el plan A / plan B lo necesita, pero el examen no lo exige.'}},
}

# sustituciones de texto, unidad por unidad
TEXTO = {
 ('movers', 2): [
  ("We're going to have a picnic by the fjord on Saturday\u2026 if it doesn't rain!",
   "We've got a picnic by the fjord on Saturday\u2026 if the weather is good!"),
  ('Student A is the TV weather presenter: draw four weather symbols for Monday\u2013Thursday and present them: "On Monday it\u2019s going to be rainy\u2026" Student B chooses what to wear each day. Then swap.',
   'Student A is the TV weather presenter: draw four weather symbols for Monday\u2013Thursday. Student B asks "What\u2019s the weather like on Monday?" and Student A answers "It\u2019s rainy." Student B chooses what to wear each day. Then swap.'),
  ("Student A is the TV weather presenter: draw four weather symbols for Monday\u2013Thursday and present them: \"On Monday it's going to be rainy\u2026\" Student B chooses what to wear each day. Then swap.",
   'Student A is the TV weather presenter: draw four weather symbols for Monday\u2013Thursday. Student B asks "What\u2019s the weather like on Monday?" and Student A answers "It\u2019s rainy." Student B chooses what to wear each day. Then swap.'),
 ],
 ('movers', 26): [
  ('You should brush your teeth twice a day, and you shouldn\u2019t eat sweets every afternoon.',
   'You must brush your teeth twice a day, and you mustn\u2019t eat sweets every afternoon.'),
  ("You should brush your teeth twice a day, and you shouldn't eat sweets every afternoon.",
   "You must brush your teeth twice a day, and you mustn't eat sweets every afternoon."),
  ('What should we do to stay healthy? Ask the doctor!',
   "What's the matter? Ask the doctor, and do what she says!"),
  ('Quick check \u00b7 Choose should or shouldn\u2019t.', 'Quick check \u00b7 Choose must or mustn\u2019t.'),
  ("Quick check \u00b7 Choose should or shouldn't.", "Quick check \u00b7 Choose must or mustn't."),
  ('Health poster team: write 4 rules for a healthy life (2 should, 2 shouldn\u2019t) and draw one icon for each. Present it in 30 seconds.',
   'Health poster team: write 4 rules for a healthy life (2 with must, 2 with mustn\u2019t) and draw one icon for each. Present it in 30 seconds.'),
  ("Health poster team: write 4 rules for a healthy life (2 should, 2 shouldn't) and draw one icon for each. Present it in 30 seconds.",
   "Health poster team: write 4 rules for a healthy life (2 with must, 2 with mustn't) and draw one icon for each. Present it in 30 seconds."),
  ('Write your healthy day: 5 sentences with should/shouldn\u2019t about food, sleep and sport.',
   'Write your healthy day: 5 sentences with must/mustn\u2019t about food, sleep and sport.'),
  ("Write your healthy day: 5 sentences with should/shouldn't about food, sleep and sport.",
   "Write your healthy day: 5 sentences with must/mustn't about food, sleep and sport."),
 ],
 ('movers', 33): [
  ('What time is the film? At seven o\u2019clock in the evening.',
   'When is the film? At seven o\u2019clock in the evening.'),
  ("What time is the film? At seven o'clock in the evening.",
   "When is the film? At seven o'clock in the evening."),
  ('What time do you get up? Look at the clock and say it in English!',
   'When do you get up? Look at the clock and say it in English!'),
 ],
 ('flyers', 47): [
  # la ayuda que el alumno tiene delante al escribir la historia decia solo
  # first conditional, que es justo lo que el examen NO pide. Se ancla con la
  # clave para no tocar la misma cadena en grammar_ahead, que si debe decirlo.
  ('"grammar": "first conditional (if + present, will)"',
   '"grammar": "if + present: zero conditional for what always happens, will for this Saturday"'),
 ],
 ('movers', 36): [
  ("Top secret! Sof\u00eda's birthday is on Friday, so the Club is going to prepare a surprise. Valentina is going to make the cake, Erik is going to invent something that throws balloons, and Mateo is going to invite everybody \u2014 quietly. Next week they are going to remember this party for a long time. What are YOU going to do at the weekend? Make a plan!",
   "Top secret! Sof\u00eda's birthday is on Friday, and the Club wants to prepare a surprise. Valentina would like to make the cake, Erik wants to invent something that throws balloons, and Mateo wants to invite everybody \u2014 quietly. What do YOU want to do at the weekend? Make a plan!"),
  ("Top secret: Sof\u00eda's birthday is on Friday. We're going to prepare the BEST surprise party in club history!",
   "Top secret: Sof\u00eda's birthday is on Friday. We want to prepare the BEST surprise party in club history!"),
  ('Erik is going to', 'Erik wants to'),
  ('Valentina is going to', 'Valentina would like to'),
  ('Mateo is going to', 'Mateo wants to'),
  ('Grandma is going to', 'Grandma would like to'),
  ('Luna is going to', 'Luna wants to'),
  ('Everyone is going to', 'Everyone wants to'),
  ('Match the person with their party job.', 'Match the person with the job they want.'),
  ('Quick check \u00b7 Choose the correct going to form.', 'Quick check \u00b7 Choose the correct form.'),
  ('Plan a surprise party for an imaginary friend: 5 sentences with going to (who, where, food, music, surprise). Present your plan in 30 seconds!',
   'Plan a surprise party for an imaginary friend: 5 sentences with want to / would like to (who, where, food, music, surprise). Present your plan in 30 seconds!'),
  ("Write 5 plans for next weekend with going to: I'm going to\u2026 My family is going to\u2026",
   "Write 5 plans for next weekend with want to: I want to\u2026 My family would like to\u2026"),
 ],
}

# los items que hay que reescribir enteros: (nivel, unidad, codigo) -> items
ITEMS = {
 ('movers', 26, 'B'): {
  'instructions': 'Complete each sentence.',
  'items': [
   {'sentence': 'You ___ brush your teeth twice a day.', 'options': ['must', "mustn't", "aren't"], 'answer': 0},
   {'sentence': 'You ___ eat sweets before bed.', 'options': ['must', "mustn't", "don't"], 'answer': 1},
   {'sentence': 'Children ___ sleep ten hours.', 'options': ['must', "mustn't", "can't"], 'answer': 0},
   {'sentence': 'You ___ watch TV all afternoon.', 'options': ['must', "mustn't", 'must to'], 'answer': 1},
   {'sentence': "\u2014 What's the ___ , Mateo? \u2014 I've got a toothache.", 'options': ['matter', 'medicine', 'morning'], 'answer': 0},
  ]},
 ('movers', 36, 'B'): {
  'instructions': 'Complete each sentence.',
  'items': [
   {'sentence': 'We ___ to have a party on Friday.', 'options': ['want', 'wants', 'wanting'], 'answer': 0},
   {'sentence': 'She would ___ to help with the cake.', 'options': ['like', 'likes', 'liking'], 'answer': 0},
   {'sentence': 'I want ___ make the birthday card.', 'options': ['to', 'for', 'at'], 'answer': 0},
   {'sentence': '___ you want to invite the whole class?', 'options': ['Do', 'Are', 'Is'], 'answer': 0},
   {'sentence': "They don't want to ___ anything to Sofia!", 'options': ['say', 'saying', 'said'], 'answer': 0},
  ]},
 ('movers', 36, 'D'): {
  'instructions': 'Choose the best answer.',
  'items': [
   {'sentence': '"What do you want to do tomorrow?"', 'options': ['I want to visit my cousins.', 'Yesterday morning.', "It's Luna's."], 'answer': 0},
   {'sentence': '"Would you like to come to the party?"', 'options': ['Yes, please!', "It's half past two.", 'Under the bed.'], 'answer': 0},
   {'sentence': '"Who wants to bring the music?"', 'options': ['Erik does.', 'Two soles.', 'In the kitchen.'], 'answer': 0},
   {'sentence': 'A party that nobody expects is a \u2026', 'options': ['surprise', 'secret list', 'plan B'], 'answer': 0},
   {'sentence': 'Before a party you ___ everything.', 'options': ['prepare', 'forget', 'close'], 'answer': 0},
  ]},
}


def actividad(c):
    return {'code': c['code'], 'type': 'grammar_box', 'title': c['title'],
            'instructions': c['instructions'], 'outputs': ['book', 'digital'],
            'structure': c['structure'], 'data': c['data']}


def main():
    check = '--check' in sys.argv
    for repo in REPOS:
        if not os.path.isdir(repo):
            print('!! no existe %s' % repo); continue
        print('\n== %s' % repo)
        tocadas = {}

        # 1. las cajas nuevas
        for c in CAJAS:
            ruta = os.path.join(repo, 'content', c['level'], 'unit-%02d.json' % c['unit'])
            d = tocadas.setdefault(ruta, json.load(io.open(ruta, encoding='utf-8')))
            acts = d['activities']
            hecho = [i for i, a in enumerate(acts) if a.get('structure') == c['structure']]
            if hecho: acts[hecho[0]] = actividad(c); verbo = 'actualizada'
            elif c['code'] in [a['code'] for a in acts]:
                print('  !! %s u%02d: el codigo %s ya esta cogido' % (c['level'], c['unit'], c['code'])); continue
            else: acts.append(actividad(c)); verbo = 'anadida'
            print('  caja  %-8s u%02d  %s  %-40s (%s)' % (c['level'], c['unit'], c['code'], c['structure'], verbo))

        # 2. las sustituciones de texto. Van ANTES de los campos: buscan por
        # cadena en todo el JSON, y si se dejan para el final se llevan por
        # delante lo que acaba de escribirse en grammar_ahead cuando dice lo
        # mismo (paso justo con el first conditional de Flyers u47).
        for (L, n), pares in TEXTO.items():
            ruta = os.path.join(repo, 'content', L, 'unit-%02d.json' % n)
            d = tocadas.setdefault(ruta, json.load(io.open(ruta, encoding='utf-8')))
            crudo = json.dumps(d, ensure_ascii=False)
            hechos = 0
            for viejo, nuevo in pares:
                # normal: el texto tal cual, escapado como lo escribe json.
                # Si el par ya viene con comillas es un trozo de JSON crudo,
                # con su clave delante, para acotar donde se sustituye.
                if viejo.startswith('"'):
                    a, b = viejo, nuevo
                else:
                    a = json.dumps(viejo, ensure_ascii=False)[1:-1]
                    b = json.dumps(nuevo, ensure_ascii=False)[1:-1]
                if a in crudo: crudo = crudo.replace(a, b); hechos += 1
            tocadas[ruta] = json.loads(crudo)
            print('  texto %-8s u%02d  %d/%d sustituciones' % (L, n, hechos, len(pares)))

        # 3. los campos sueltos
        for (L, n), campos in CAMPOS.items():
            ruta = os.path.join(repo, 'content', L, 'unit-%02d.json' % n)
            d = tocadas.setdefault(ruta, json.load(io.open(ruta, encoding='utf-8')))
            for k, v in campos.items():
                if d.get(k) != v:
                    print('  campo %-8s u%02d  %-14s %s' % (L, n, k, json.dumps(v, ensure_ascii=False)[:70]))
                    d[k] = v

        # 4. los items reescritos
        for (L, n, code), data in ITEMS.items():
            ruta = os.path.join(repo, 'content', L, 'unit-%02d.json' % n)
            d = tocadas.setdefault(ruta, json.load(io.open(ruta, encoding='utf-8')))
            a = [x for x in d['activities'] if x['code'] == code]
            if not a: print('  !! %s u%02d: no hay actividad %s' % (L, n, code)); continue
            if a[0]['data'] != data:
                a[0]['data'] = data
                print('  items %-8s u%02d  %s reescrita' % (L, n, code))

        # 5. el titulo de u36 tambien vive en el indice del nivel
        idx = os.path.join(repo, 'content', 'movers', 'index.json')
        di = json.load(io.open(idx, encoding='utf-8'))
        for u in di['units']:
            if u['n'] == 36 and (u['title'] != 'The surprise party' or u.get('topic') != 'plans & wishes'):
                u['title'] = 'The surprise party'; u['topic'] = 'plans & wishes'
                tocadas[idx] = di
                print('  indice  movers u36  titulo y topic')

        if not check:
            for ruta, d in tocadas.items():
                with io.open(ruta, 'w', encoding='utf-8', newline='') as f:
                    json.dump(d, f, ensure_ascii=False, indent=1)
            print('  -> %d ficheros escritos' % len(tocadas))


if __name__ == '__main__':
    main()
