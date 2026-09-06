# -*- coding: utf-8 -*-
"""Las once estructuras oficiales que el curso nunca llegaba a ensenar.

La auditoria de gramatica comparo la lista oficial (yle/grammar-2024.json,
sacada del Handbook 2024) con TODO el texto de las 150 unidades — no solo la
etiqueta «grammar», sino lo que el nino lee y oye de verdad. Once estructuras
no aparecian ni una vez:

    Starters  Have + object + infinitive · Me too! · So do I · Story about + ing
    Movers    Want/ask sb to do sth · Shall for offers · When clauses ·
              Go for a + noun · Be good at + noun
    Flyers    Tag questions · Before/after clauses

Cada una entra en la unidad donde ya encaja por tema (las ofertas con Shall,
en el picnic; «be good at», en el dia de deporte; las coletillas, en la unidad
de respuestas cortas), como una actividad nueva de tipo grammar_box.

Ese tipo ya existia en el motor —regla, ejemplos y practica corregida— pero no
lo usaba ninguna unidad: estaba escrito y con su CSS, sin estrenar.

La caja va al final del array y con un codigo libre (G, o K donde G ya esta
cogido). No se renombra ninguna actividad: el progreso del alumno y lo que
guarda activity-save.js van por codigo, y cambiar las letras borraria lo hecho.
El libro ordena por letra, asi que sale tambien la ultima: los dos coinciden.

Tampoco se toca el campo «grammar» de la unidad: MAGICBOX elige su familia con
una expresion regular sobre grammar+topic+title, y anadir texto ahi puede
cambiarle la caja magica a una unidad que ya la tenia bien.

    python tools/gramatica_faltante.py --check
    python tools/gramatica_faltante.py
"""
import io, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
# El curso vive dos veces: el repo suelto es el que va a GitHub Pages y el
# portal lleva una copia vendorizada, que es la que sirve nis.cohasset.pe.
# Las dos tienen que quedar con el mismo contenido.
REPOS = [r'C:\Projects\nis-portal\nis-fun',
         r'C:\Projects\nis-fun']

CAMB = 'Cambridge'   # marca del ejemplo que viene tal cual de la lista oficial


CAJAS = [
# ---------------------------------------------------------------- STARTERS
{
 'level': 'starters', 'unit': 5, 'code': 'G', 'id': 'have_obj_inf',
 'structure': 'Have + object + infinitive',
 'title': 'Grammar \u00b7 I have a book to read.',
 'instructions': 'Read the sentences. Then choose the right word.',
 'data': {
  'title': 'I have a book to read.',
  'intro': 'First say <b>what you have</b>. Then say <b>what you do with it</b>. One little word joins them: <b>to</b>.',
  'can': 'I can say what I have and what I do with it: <b>a book to read</b>.',
  'examples': [
   {'text': 'Lucy has a book <b>to read</b>.', 'note': CAMB},
   {'text': 'Astrid has a pencil <b>to draw</b>.'},
   {'text': 'I have an apple <b>to eat</b>.'},
   {'text': 'Pip has a fish <b>to eat</b>. Look at him!'},
  ],
  'rules': [
   'have / has + a thing + <b>to</b> + do it.',
   'The verb after <b>to</b> never changes: to read, to eat, to draw.',
   'Now say one to your partner: "I have a ___ to ___."',
  ],
  'practice': {'instructions': 'Choose the right word.', 'items': [
   {'sentence': 'I have a book ___ read.', 'options': ['to', 'and', 'is'], 'answer': 0},
   {'sentence': 'Astrid has an apple to ___.', 'options': ['eats', 'eat', 'eating'], 'answer': 1},
   {'sentence': 'We have a song to ___.', 'options': ['sing', 'sings', 'singing'], 'answer': 0},
   {'sentence': 'Pip has a fish ___ eat.', 'options': ['at', 'for', 'to'], 'answer': 2},
   {'sentence': 'She ___ a nice book to read.', 'options': ['have', 'has', 'having'], 'answer': 1},
  ]},
 },
},
{
 'level': 'starters', 'unit': 12, 'code': 'G', 'id': 'me_too',
 'structure': 'Me too!',
 'title': 'Grammar \u00b7 Me too!',
 'instructions': 'Read the sentences. Then choose the right word.',
 'data': {
  'title': 'Me too!',
  'intro': 'Your friend says something and you feel the same. Two words and you are in: <b>Me too!</b>',
  'can': 'I can say <b>Me too!</b> when I like the same thing as my friend.',
  'examples': [
   {'text': 'I like football. <b>Me too.</b>', 'note': CAMB},
   {'text': 'Nico: I like pizza. \u2014 Tomas: <b>Me too!</b>'},
   {'text': 'Nico: I want some cake. \u2014 Tomas: <b>Me too!</b>'},
   {'text': 'Nico: I have got a red bag. \u2014 Tomas: <b>Me too!</b>'},
  ],
  'rules': [
   'Say <b>Me too!</b> when the same thing is true for you.',
   'It is very short. Say it quickly and smile!',
   'Now try it: tell your partner one food you like and wait for "Me too!"',
  ],
  'practice': {'instructions': 'Choose the right answer.', 'items': [
   {'sentence': '\u2014 I like cake. \u2014 ___!', 'options': ['Me too', 'I too', 'Too me'], 'answer': 0},
   {'sentence': "\u2014 I'm happy today. \u2014 Me ___!", 'options': ['to', 'two', 'too'], 'answer': 2},
   {'sentence': '\u2014 I like ice cream. \u2014 ___', 'options': ['You too!', 'Me too!', 'Too me!'], 'answer': 1},
   {'sentence': 'Tomas likes milk. Nico likes milk. Nico says: ___', 'options': ['Me too!', 'Me and!', 'Too!'], 'answer': 0},
   {'sentence': '\u2014 I have got a cat. \u2014 Me ___! Her name is Pip.', 'options': ['to', 'too', 'so'], 'answer': 1},
  ]},
 },
},
{
 'level': 'starters', 'unit': 27, 'code': 'G', 'id': 'so_do_i',
 'structure': 'So do I',
 'title': 'Grammar \u00b7 So do I!',
 'instructions': 'Read the sentences. Then choose the right word.',
 'data': {
  'title': 'So do I!',
  'intro': 'Another way to say <i>me too</i> \u2014 a bit bigger, and grown-ups love it: <b>So do I.</b>',
  'can': 'I can answer <b>So do I!</b> when my friend and I do the same thing.',
  'examples': [
   {'text': 'I love hippos. <b>So do I.</b>', 'note': CAMB},
   {'text': 'Tomas: I play football. \u2014 Nico: <b>So do I!</b>'},
   {'text': 'Tomas: I like swimming. \u2014 Nico: <b>So do I!</b>'},
   {'text': 'Tomas: I want a new ball. \u2014 Nico: <b>So do I!</b>'},
  ],
  'rules': [
   'After <b>I like\u2026</b>, <b>I play\u2026</b>, <b>I want\u2026</b> you answer: <b>So do I.</b>',
   'The words go in this order: <b>So \u2014 do \u2014 I</b>. Not "So I do".',
   'Say a sport you play and let your partner answer "So do I!"',
  ],
  'practice': {'instructions': 'Choose the right word.', 'items': [
   {'sentence': '\u2014 I play basketball. \u2014 So ___ I!', 'options': ['am', 'do', 'is'], 'answer': 1},
   {'sentence': '\u2014 I like swimming. \u2014 ___ do I!', 'options': ['Very', 'Too', 'So'], 'answer': 2},
   {'sentence': '\u2014 I want a ball. \u2014 So do ___!', 'options': ['I', 'me', 'my'], 'answer': 0},
   {'sentence': '\u2014 I go swimming on Fridays. \u2014 So ___ I!', 'options': ['am', 'go', 'do'], 'answer': 2},
   {'sentence': 'Which one is right?', 'options': ['So I do.', 'So am I do.', 'So do I.'], 'answer': 2},
  ]},
 },
},
{
 'level': 'starters', 'unit': 28, 'code': 'G', 'id': 'story_about_ing',
 'structure': 'Story about + ing',
 'title': 'Grammar \u00b7 A story about playing',
 'instructions': 'Read the sentences. Then choose the right word.',
 'data': {
  'title': 'A story about playing',
  'intro': 'What is the book about? What is the song about? Say the action with <b>-ing</b>.',
  'can': 'I can say what a story is about: <b>a story about playing in the park</b>.',
  'examples': [
   {'text': 'This is a story about <b>playing</b> football.', 'note': CAMB},
   {'text': 'This is a story about <b>playing</b> in the park.'},
   {'text': "It's a book about <b>swimming</b>."},
   {'text': "It's a song about <b>running</b> and <b>jumping</b>."},
  ],
  'rules': [
   'about + verb + <b>-ing</b>: about play<b>ing</b>, about sing<b>ing</b>, about eat<b>ing</b>.',
   'Never "a story about play". The verb always takes <b>-ing</b> here.',
   'Tell your partner: "My favourite book is about ___ing."',
  ],
  'practice': {'instructions': 'Choose the right word.', 'items': [
   {'sentence': 'This is a story about ___ in the park.', 'options': ['play', 'playing', 'plays'], 'answer': 1},
   {'sentence': "It's a book about ___.", 'options': ['swims', 'swimming', 'swim'], 'answer': 1},
   {'sentence': "It's a story about ___ a kite.", 'options': ['flying', 'fly', 'flies'], 'answer': 0},
   {'sentence': 'This is a song about ___ and jumping.', 'options': ['runs', 'run', 'running'], 'answer': 2},
   {'sentence': 'Which one is right?', 'options': ['a story about eat', 'a story about eats', 'a story about eating'], 'answer': 2},
  ]},
 },
},
# ------------------------------------------------------------------ MOVERS
{
 'level': 'movers', 'unit': 11, 'code': 'G', 'id': 'go_for_a',
 'structure': 'Go for a + noun',
 'title': 'Grammar \u00b7 Go for a swim!',
 'instructions': 'Read the sentences. Then choose the right word.',
 'data': {
  'title': "Let's go for a swim!",
  'intro': 'You can <b>go for a</b> walk, <b>a</b> swim, <b>a</b> ride or <b>a</b> picnic. The action turns into a thing you go for \u2014 and the little <b>a</b> is never missing.',
  'can': 'I can say <b>go for a walk / a swim / a ride</b> to talk about what we do outside.',
  'examples': [
   {'text': "Yesterday we <b>went for a drive</b> in my brother's new car.", 'note': CAMB},
   {'text': "Let's <b>go for a swim</b> in the lake!"},
   {'text': 'We <b>went for a walk</b> in the forest and saw a big rock.'},
   {'text': 'Erik <b>goes for a ride</b> on his bike every Saturday.'},
  ],
  'rules': [
   'go / goes / went + <b>for a</b> + walk, swim, ride, drive, picnic.',
   'Never "go for swim". The <b>a</b> always stays.',
   '<b>Go swimming</b> is also correct \u2014 but then there is no <i>for</i> and no <i>a</i>.',
  ],
  'practice': {'instructions': 'Choose the right word.', 'items': [
   {'sentence': "Let's go ___ a swim in the lake!", 'options': ['to', 'for', 'at'], 'answer': 1},
   {'sentence': 'Yesterday we went for a ___ in the forest.', 'options': ['walk', 'walked', 'walking'], 'answer': 0},
   {'sentence': 'Valentina ___ for a ride on her bike every Saturday.', 'options': ['go', 'going', 'goes'], 'answer': 2},
   {'sentence': "Shall we go for a ___ by the lake? I've got sandwiches.", 'options': ['cold', 'picnic', 'jump'], 'answer': 1},
   {'sentence': 'Which one is right?', 'options': ['We went for swim.', 'We went a swim.', 'We went for a swim.'], 'answer': 2},
  ]},
 },
},
{
 'level': 'movers', 'unit': 15, 'code': 'G', 'id': 'be_good_at',
 'structure': 'Be good at + noun',
 'title': "Grammar \u00b7 I'm good at running!",
 'instructions': 'Read the sentences. Then choose the right word.',
 'data': {
  'title': "I'm good at running!",
  'intro': 'What can you do well? Say <b>good at</b> and then the sport \u2014 or the verb with <b>-ing</b>.',
  'can': 'I can say what I am <b>good at</b>, and ask my friends what they are good at.',
  'examples': [
   {'text': "She's very <b>good at basketball</b>.", 'note': CAMB},
   {'text': 'Mateo is <b>good at running</b>. He is always the winner.'},
   {'text': "I'm not very <b>good at throwing</b>, but I can catch!"},
   {'text': 'Are you <b>good at football</b>, Sofia?'},
  ],
  'rules': [
   'am / is / are + <b>good at</b> + a sport, or a verb with <b>-ing</b>.',
   'Always <b>at</b>. Not "good in", not "good of".',
   'For the negative: <b>is not very good at</b>\u2026 It sounds kinder.',
  ],
  'practice': {'instructions': 'Choose the right word.', 'items': [
   {'sentence': 'Sofia is very good ___ tennis.', 'options': ['in', 'at', 'on'], 'answer': 1},
   {'sentence': "I'm good at ___.", 'options': ['swim', 'swims', 'swimming'], 'answer': 2},
   {'sentence': '___ you good at catching the ball?', 'options': ['Do', 'Are', 'Is'], 'answer': 1},
   {'sentence': "Mateo isn't very good ___ jumping.", 'options': ['at', 'to', 'for'], 'answer': 0},
   {'sentence': 'Which one is right?', 'options': ["He's good in football.", "He's good football.", "He's good at football."], 'answer': 2},
  ]},
 },
},
{
 'level': 'movers', 'unit': 17, 'code': 'G', 'id': 'shall_offers',
 'structure': 'Shall for offers',
 'title': 'Grammar \u00b7 Shall I help you?',
 'instructions': 'Read the sentences. Then choose the right word.',
 'data': {
  'title': 'Shall I help you?',
  'intro': 'You want to help somebody. Do not just do it \u2014 offer first. <b>Shall I\u2026?</b> is the polite way in.',
  'can': 'I can offer to help with <b>Shall I\u2026?</b> and answer an offer politely.',
  'examples': [
   {'text': '<b>Shall I help</b> you wash the car, Mum?', 'note': CAMB},
   {'text': "You're hungry? <b>Shall I get</b> you a sandwich?"},
   {'text': '<b>Shall I open</b> the bottle for you?'},
   {'text': "<b>Shall I carry</b> the blanket? \u2014 Yes, please!"},
  ],
  'rules': [
   '<b>Shall I</b> + verb, with no <i>to</i>: Shall I help? Shall I open it?',
   'The answer is short: <b>Yes, please!</b> or <b>No, thanks.</b>',
   '<b>Shall we\u2026?</b> is for both of you: "Shall we have the picnic here?"',
  ],
  'practice': {'instructions': 'Choose the right word.', 'items': [
   {'sentence': '___ I help you with the picnic?', 'options': ['Am', 'Shall', 'Do'], 'answer': 1},
   {'sentence': 'Shall I ___ the bottle for you?', 'options': ['open', 'opens', 'opening'], 'answer': 0},
   {'sentence': '\u2014 Shall I get you some water? \u2014 ___', 'options': ['Yes, I shall.', 'Yes, I do.', 'Yes, please!'], 'answer': 2},
   {'sentence': "Mum has got a lot of bags. Mateo says: '___ I carry one?'", 'options': ['Shall', 'Am', 'Do'], 'answer': 0},
   {'sentence': 'Which one is right?', 'options': ['Shall I to help you?', 'Shall I help you?', 'Shall I helping you?'], 'answer': 1},
  ]},
 },
},
{
 'level': 'movers', 'unit': 24, 'code': 'G', 'id': 'want_sb_to',
 'structure': 'Want / ask someone to do something',
 'title': 'Grammar \u00b7 Mum wants me to help',
 'instructions': 'Read the sentences. Then choose the right word.',
 'data': {
  'title': 'Mum wants me to help',
  'intro': 'You want something \u2014 but you want <b>somebody else</b> to do it. The person goes in the middle, between the verb and <b>to</b>.',
  'can': 'I can say who wants somebody to do something: <b>Mum wants me to wash the dishes.</b>',
  'examples': [
   {'text': 'He <b>wants the teacher to tell</b> a story.', 'note': CAMB},
   {'text': 'Mum <b>wants me to wash</b> the dishes.'},
   {'text': 'Erik <b>asked Mateo to feed</b> the cat.'},
   {'text': 'Do you <b>want me to help</b> you with the rubbish?'},
  ],
  'rules': [
   'want / ask + <b>somebody</b> + <b>to</b> + verb.',
   'The person in the middle is <b>me, you, him, her, us, them</b> \u2014 or a name.',
   'Never "She wants that I help". English puts the person straight after the verb.',
  ],
  'practice': {'instructions': 'Choose the right word.', 'items': [
   {'sentence': 'Mum wants ___ to clean my room.', 'options': ['I', 'me', 'my'], 'answer': 1},
   {'sentence': 'Erik asked Mateo ___ feed the dog.', 'options': ['to', 'for', 'that'], 'answer': 0},
   {'sentence': 'Do you want me ___ help you?', 'options': ['and', 'for', 'to'], 'answer': 2},
   {'sentence': 'The teacher wants ___ to be quiet.', 'options': ['we', 'us', 'our'], 'answer': 1},
   {'sentence': 'Which one is right?', 'options': ['She wants that I help.', 'She wants me to help.', 'She wants me help.'], 'answer': 1},
  ]},
 },
},
{
 'level': 'movers', 'unit': 29, 'code': 'G', 'id': 'when_clauses',
 'structure': 'When clauses (not with future meaning)',
 'title': 'Grammar \u00b7 When he got home\u2026',
 'instructions': 'Read the sentences. Then choose the right word.',
 'data': {
  'title': 'When he got home\u2026',
  'intro': 'Two things happened. <b>When</b> tells your reader which one came first \u2014 and it lets you put two short sentences into one good one.',
  'can': 'I can join two past sentences with <b>when</b> to tell a story in order.',
  'examples': [
   {'text': '<b>When he got home</b>, he had his dinner.', 'note': CAMB},
   {'text': "<b>When Sofia came home</b>, Luna wasn't there."},
   {'text': 'Mateo was very happy <b>when he saw the dog</b>.'},
   {'text': '<b>When they looked under the bench</b>, they found her!'},
  ],
  'rules': [
   '<b>When</b> + what happened first, then the other thing.',
   'Start with <b>When</b> and you need a comma. Put it in the middle and you do not.',
   'Both halves are in the past: <b>When he got\u2026, he had\u2026</b>',
  ],
  'practice': {'instructions': 'Choose the right word.', 'items': [
   {'sentence': "___ Sofia came home, the dog wasn't there.", 'options': ['When', 'What', 'Who'], 'answer': 0},
   {'sentence': 'When they ___ into the park, they called her name.', 'options': ['walk', 'walked', 'walking'], 'answer': 1},
   {'sentence': 'Mateo was very happy ___ he saw Luna again.', 'options': ['then', 'what', 'when'], 'answer': 2},
   {'sentence': 'When he got home, he ___ his dinner.', 'options': ['have', 'had', 'having'], 'answer': 1},
   {'sentence': 'Which one is right?', 'options': ['When he opened the door when the cat ran out.', 'He opened the door when.', 'When he opened the door, the cat ran out.'], 'answer': 2},
  ]},
 },
},
# ------------------------------------------------------------------ FLYERS
{
 'level': 'flyers', 'unit': 39, 'code': 'K', 'id': 'before_after',
 'structure': 'Before / after clauses (not with future reference)',
 'title': 'Grammar \u00b7 Before she sailed, after she returned',
 'instructions': 'Read the sentences. Then choose the right word.',
 'data': {
  'title': 'Before she sailed, after she returned',
  'intro': '<b>Before</b> and <b>after</b> put two past actions in order. Careful: the order of the <i>words</i> is not always the order of the <i>story</i>.',
  'can': 'I can put two past actions in order with <b>before</b> and <b>after</b>.',
  'examples': [
   {'text': 'I finished my homework <b>before I played</b> football.', 'note': CAMB},
   {'text': '<b>Before she sailed</b> to the pole, Ingrid studied the map for a year.'},
   {'text': '<b>After they climbed</b> the mountain, they wrote everything down.'},
   {'text': 'The explorers ate their breakfast <b>before they left</b> the ship.'},
  ],
  'rules': [
   '<b>before</b> / <b>after</b> + a whole clause: a person <i>and</i> a verb, not just a word.',
   'Both verbs are in the past simple: before she <b>sailed</b>, after they <b>climbed</b>.',
   'Read to the end before you decide what happened first \u2014 that is exactly what the exam asks you to do.',
  ],
  'practice': {'instructions': 'Choose the right word.', 'items': [
   {'sentence': 'First they climbed the mountain. Then they took a photo. So they took a photo ___ they climbed it.', 'options': ['before', 'after', 'while'], 'answer': 1},
   {'sentence': '___ they left the ship, the explorers looked at the map one last time.', 'options': ['Before', 'Then', 'So'], 'answer': 0},
   {'sentence': 'After she ___ home, she wrote a book about her journey.', 'options': ['come', 'came', 'coming'], 'answer': 1},
   {'sentence': 'He read the map carefully before he ___ the ship.', 'options': ['leave', 'leaving', 'left'], 'answer': 2},
   {'sentence': 'Which one is right?', 'options': ['Before the journey started, they got everything ready.', 'Before started the journey, they got everything ready.', 'Before, the journey started they got everything ready.'], 'answer': 0},
  ]},
 },
},
{
 'level': 'flyers', 'unit': 49, 'code': 'K', 'id': 'tag_questions',
 'structure': 'Tag questions',
 'title': "Grammar \u00b7 \u2026isn't it?",
 'instructions': 'Read the sentences. Then choose the right ending.',
 'data': {
  'title': "That's the answer, isn't it?",
  'intro': 'You are almost sure, and you want the other person to agree. Add a mini-question at the end \u2014 English does this all the time.',
  'can': 'I can add a tag question (<b>isn\u2019t it? don\u2019t you? did she?</b>) to check something I think is true.',
  'examples': [
   {'text': "That's John's book, <b>isn't it</b>?", 'note': CAMB},
   {'text': 'You know the answer, <b>don\u2019t you</b>?'},
   {'text': 'She won the last round, <b>didn\u2019t she</b>?'},
   {'text': "It isn't the correct answer, <b>is it</b>?"},
  ],
  'rules': [
   'Positive sentence \u2192 <b>negative</b> tag. Negative sentence \u2192 <b>positive</b> tag.',
   'Use the same helper verb: is \u2192 isn\u2019t \u00b7 can \u2192 can\u2019t \u00b7 has \u2192 hasn\u2019t \u00b7 was \u2192 wasn\u2019t.',
   'No helper verb in the sentence? Then use <b>do / does / did</b>: "You play tennis, <b>don\u2019t you</b>?"',
  ],
  'practice': {'instructions': 'Choose the right ending.', 'items': [
   {'sentence': "That's the correct answer, ___?", 'options': ['is it', "isn't it", "doesn't it"], 'answer': 1},
   {'sentence': 'You know the question, ___?', 'options': ["aren't you", "didn't you", "don't you"], 'answer': 2},
   {'sentence': 'She won the last round, ___?', 'options': ["wasn't she", "didn't she", "doesn't she"], 'answer': 1},
   {'sentence': "It isn't your turn, ___?", 'options': ['is it', "isn't it", 'does it'], 'answer': 0},
   {'sentence': "They can't hear the buzzer, ___?", 'options': ["can't they", 'do they', 'can they'], 'answer': 2},
  ]},
 },
},
]


def actividad(c):
    return {
        'code': c['code'],
        'type': 'grammar_box',
        'title': c['title'],
        'instructions': c['instructions'],
        'outputs': ['book', 'digital'],
        'structure': c['structure'],
        'data': c['data'],
    }


def main():
    check = '--check' in sys.argv
    for repo in REPOS:
        if not os.path.isdir(repo):
            print('!! no existe %s' % repo); continue
        print('\n== %s' % repo)
        for c in CAJAS:
            ruta = os.path.join(repo, 'content', c['level'], 'unit-%02d.json' % c['unit'])
            d = json.load(io.open(ruta, encoding='utf-8'))
            acts = d['activities']
            usados = [a['code'] for a in acts]
            if c['code'] in usados and not any(a['type'] == 'grammar_box' for a in acts):
                print('  !! %s u%02d: el codigo %s ya esta cogido' % (c['level'], c['unit'], c['code']))
                continue
            nueva = actividad(c)
            hecho = [i for i, a in enumerate(acts) if a['type'] == 'grammar_box']
            if hecho:
                acts[hecho[0]] = nueva; verbo = 'actualizada'
            else:
                acts.append(nueva); verbo = 'anadida'
            print('  %-8s u%02d  %s  %-45s (%s)' % (c['level'], c['unit'], c['code'], c['structure'], verbo))
            if not check:
                with io.open(ruta, 'w', encoding='utf-8', newline='') as f:
                    json.dump(d, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
