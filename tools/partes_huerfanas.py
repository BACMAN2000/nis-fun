# -*- coding: utf-8 -*-
"""Las cuatro partes del examen de Starters que el curso no entrenaba nunca.

Cruzando el exam_focus de las 45 unidades con las nueve partes oficiales salia
esto: Listening 3 y Reading & Writing 3, 4 y 5 no aparecian en ninguna unidad
—15 de los 25 puntos del paper, y en el nivel de los mas pequenos—, mientras
que Listening 4 se llevaba veinte unidades ella sola.

Cuatro de esas veinte pasan a cubrir lo que faltaba, cada una en la unidad cuyo
tema encaja con la tarea:

    u03 At the zoo    -> Listening 3, escuchar y marcar el dibujo (picture_mc)
    u13 Fruit fun     -> R&W 3, ordenar las letras          (unscramble, nuevo)
    u18 The sea       -> R&W 4, elegir y copiar la palabra  (gap_text con banco)
    u30 The beach     -> R&W 5, la historia y una palabra   (story_qa, nuevo)

La actividad nueva se anade al final y con codigo libre, como manda la regla: el
progreso del alumno va por codigo y renumerar lo borraria. El exam_focus de la
unidad cambia, que es lo que hace que la parte deje de estar huerfana.

    python tools/partes_huerfanas.py --check
    python tools/partes_huerfanas.py
"""
import io, json, os, sys

REPOS = [r'C:\Projects\nis-portal\nis-fun', r'C:\Projects\nis-fun']

TAREAS = [
{
 'unit': 3, 'code': 'G', 'focus': {'paper': 'Listening', 'part': 3, 'skill': 'listening'},
 'act': {
  'code': 'G', 'type': 'picture_mc', 'outputs': ['digital'],
  'audio': 'starters/u03-g.mp3',
  'title': 'Exam part \u00b7 Listen and tick the right picture.',
  'instructions': 'Listen. Which one is right? Tick A, B or C.',
  'data': {
   'script': ('Listen and tick the box. There is one example. '
              '\u2026 Which animal can swim? \u2026 Nico: Look! The fish is swimming in the water. '
              '\u2026 Which animal is very big and grey? \u2026 Astrid: The elephant! It is very big and grey. '
              '\u2026 Which animal can fly? \u2026 Nico: The parrot can fly. It is green and red. '
              '\u2026 Which animal has got a long neck? \u2026 Astrid: The giraffe has got a very long neck. '
              '\u2026 Which animal is orange and black? \u2026 Nico: The tiger! It is orange and black.'),
   'questions': [
    {'q': 'Which animal can swim?', 'answer': 'fish',
     'options': [{'word': 'tiger'}, {'word': 'fish'}, {'word': 'giraffe'}]},
    {'q': 'Which animal is very big and grey?', 'answer': 'elephant',
     'options': [{'word': 'elephant'}, {'word': 'rabbit'}, {'word': 'bird'}]},
    {'q': 'Which animal can fly?', 'answer': 'parrot',
     'options': [{'word': 'snake'}, {'word': 'cow'}, {'word': 'parrot'}]},
    {'q': 'Which animal has got a long neck?', 'answer': 'giraffe',
     'options': [{'word': 'giraffe'}, {'word': 'mouse'}, {'word': 'frog'}]},
    {'q': 'Which animal is orange and black?', 'answer': 'tiger',
     'options': [{'word': 'panda'}, {'word': 'tiger'}, {'word': 'penguin'}]},
   ],
  },
 }
},
{
 'unit': 13, 'code': 'G', 'focus': {'paper': 'Reading & Writing', 'part': 3, 'skill': 'writing'},
 'act': {
  'code': 'G', 'type': 'unscramble', 'outputs': ['book', 'digital'],
  'title': 'Exam part \u00b7 Look at the picture. Write the word.',
  'instructions': 'The letters are not in order. Look at the picture and write the word.',
  'data': {'items': [
   {'letters': 'p p a l e', 'word': 'apple', 'e': '\U0001f34e'},
   {'letters': 'n a a n b a', 'word': 'banana', 'e': '\U0001f34c'},
   {'letters': 'g o n e r a', 'word': 'orange', 'e': '\U0001f34a'},
   {'letters': 'o l m e n', 'word': 'lemon', 'e': '\U0001f34b'},
   {'letters': 'r e p a', 'word': 'pear', 'e': '\U0001f350'},
  ]},
 },
},
{
 'unit': 18, 'code': 'G', 'focus': {'paper': 'Reading & Writing', 'part': 4, 'skill': 'reading'},
 'act': {
  'code': 'G', 'type': 'gap_text', 'outputs': ['book', 'digital'],
  'title': 'Exam part \u00b7 Choose the word and write it in the gap.',
  'instructions': 'Read about the sea. Choose a word from the box and write it in each gap.',
  'data': {
   'box': ['sea', 'fish', 'boat', 'sand', 'birds', 'water'],
   'text': 'The {1} is very big and blue. There are a lot of {2} in it. Some are small and some are very big. You can go on the {3} with your family. On the beach you can play with the {4}. Look up! Two white {5} are flying.',
   'answers': ['sea', 'fish', 'boat', 'sand', 'birds'],
  },
 },
},
{
 'unit': 30, 'code': 'G', 'focus': {'paper': 'Reading & Writing', 'part': 5, 'skill': 'reading'},
 'act': {
  'code': 'G', 'type': 'story_qa', 'outputs': ['book', 'digital'],
  'title': 'Exam part \u00b7 Read the story. Answer with one word.',
  'instructions': 'Read the story about the beach. Answer each question with ONE word.',
  'data': {
   'text': ("It is a hot day and Nico is at the beach with Freya.\n"
            "Nico is making a big castle with the sand. Freya is swimming in the sea.\n"
            "Pip is sleeping under a red hat. He is very happy.\n"
            "Then Freya sees a small fish. 'Come here, Nico!' she says. 'Look at this fish!'"),
   'questions': [
    {'q': 'Where are Nico and Freya?', 'a': ['beach', 'the beach', 'at the beach']},
    {'q': 'What is Nico making?', 'a': ['castle', 'a castle', 'sandcastle']},
    {'q': 'What colour is the hat?', 'a': ['red']},
    {'q': 'Who is sleeping?', 'a': ['pip']},
    {'q': 'What does Freya see in the sea?', 'a': ['fish', 'a fish', 'a small fish']},
   ],
  },
 },
},
]


def main():
    check = '--check' in sys.argv
    for repo in REPOS:
        if not os.path.isdir(repo):
            print('!! no existe %s' % repo); continue
        print('\n== %s' % repo)
        for t in TAREAS:
            ruta = os.path.join(repo, 'content', 'starters', 'unit-%02d.json' % t['unit'])
            d = json.load(io.open(ruta, encoding='utf-8'))
            acts = d['activities']
            hecho = [i for i, a in enumerate(acts) if a['type'] == t['act']['type']]
            if hecho:
                acts[hecho[0]] = t['act']; verbo = 'actualizada'
            elif t['code'] in [a['code'] for a in acts]:
                print('  !! u%02d: el codigo %s ya esta cogido' % (t['unit'], t['code'])); continue
            else:
                acts.append(t['act']); verbo = 'anadida'
            antes = d.get('exam_focus')
            d['exam_focus'] = t['focus']
            print('  u%02d %-22s %s %s %-11s  %s -> %s %s' % (
                t['unit'], d['title'][:22], t['act']['code'], t['act']['type'], '(' + verbo + ')',
                '%s %s' % ((antes or {}).get('paper'), (antes or {}).get('part')),
                t['focus']['paper'], t['focus']['part']))
            if not check:
                with io.open(ruta, 'w', encoding='utf-8', newline='') as f:
                    json.dump(d, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
