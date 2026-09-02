# -*- coding: utf-8 -*-
"""La lista de "lo que ya se hacer" y las mascotas, en frances.

Dos arreglos de forma, ademas de la traduccion:

  * las once frases del autoexamen se sacan a una tabla por tipo de
    actividad. Once ifs seguidos con la frase dentro no se pueden traducir
    sin repetir once veces la misma llamada.
  * lo que dice cada mascota deja de escribirse como 'a' + 'b'. Partida en
    dos trozos, la mitad se quedaba fuera de T() y volvia en ingles.
"""
import io, sys

P = r"C:\Projects\nis-portal\nis-fun\engine\index.html"

VIEJO_PUEDO = """  digital.forEach(a => {
    if (a.type === 'listening') puedo.push('I can listen and write the missing words.');
    if (a.type === 'crossword') puedo.push('I can read a clue and write the word.');
    if (a.type === 'match_words') puedo.push('I can match words that go together.');
    if (a.type === 'exam_task') puedo.push('I can choose the right answer in an exam task.');
    if (a.type === 'gap_text') puedo.push('I can read a text and fill in the gaps.');
    if (a.type === 'spot_diff') puedo.push('I can compare two pictures and say the differences.');
    if (a.type === 'pairwork') puedo.push('I can talk about this topic with a partner.');
    if (a.type === 'label_people') puedo.push('I can listen and write the right name under each person.');
    if (a.type === 'picture_mc') puedo.push('I can listen and choose the right picture.');
    if (a.type === 'match_pictures') puedo.push('I can listen and match each person to a picture.');
    if (a.type === 'picture_story') puedo.push('I can look at three pictures and write the story in 20-25 words.');
  });"""

NUEVO_PUEDO = """  // Una frase por tipo de actividad. En tabla y no en once ifs seguidos
  // porque cada una hay que decirla en los dos idiomas.
  const PUEDO_POR_TIPO = {
    listening:      T('I can listen and write the missing words.',
                      "Je sais écouter et écrire les mots qui manquent."),
    crossword:      T('I can read a clue and write the word.',
                      'Je sais lire une définition et écrire le mot.'),
    match_words:    T('I can match words that go together.',
                      'Je sais associer les mots qui vont ensemble.'),
    exam_task:      T('I can choose the right answer in an exam task.',
                      "Je sais choisir la bonne réponse dans un exercice d'examen."),
    gap_text:       T('I can read a text and fill in the gaps.',
                      'Je sais lire un texte et compléter les trous.'),
    spot_diff:      T('I can compare two pictures and say the differences.',
                      'Je sais comparer deux images et dire les différences.'),
    pairwork:       T('I can talk about this topic with a partner.',
                      'Je sais parler de ce sujet avec un camarade.'),
    label_people:   T('I can listen and write the right name under each person.',
                      'Je sais écouter et écrire le bon prénom sous chaque personne.'),
    picture_mc:     T('I can listen and choose the right picture.',
                      "Je sais écouter et choisir la bonne image."),
    match_pictures: T('I can listen and match each person to a picture.',
                      'Je sais écouter et associer chaque personne à une image.'),
    picture_story:  T('I can look at three pictures and write the story in 20-25 words.',
                      "Je sais regarder trois images et écrire l'histoire en 20-25 mots."),
  };
  digital.forEach(a => {
    const t = PUEDO_POR_TIPO[a.type];
    if (t) puedo.push(t);
  });"""

VIEJO_MASCOTA = """  pip:  { que: T('a little puffin', 'un petit macareux'),
          dice: T("I live on the rocks by the lighthouse. I am very shy, "
                  + "so I hide in every picture — can you find me?",
                  "J'habite sur les rochers, près du phare. Je suis très timide, "
                  + "alors je me cache dans chaque image — tu me trouves ?") },
  luna: { que: T('a husky', 'une husky'),
          dice: T("I love the snow and I remember everything that happened. "
                  + "I will tell you the stories!",
                  "J'adore la neige et je me souviens de tout ce qui s'est passé. "
                  + "C'est moi qui vais te raconter les histoires !") },
  kili: { que: T('an Andean condor', 'un condor des Andes'),
          dice: T("I am the postman of the school. I bring letters and "
                  + "postcards from far away — but I am not very good at landing!",
                  "Je suis le facteur de l'école. J'apporte des lettres et des "
                  + "cartes postales de très loin — mais je me pose très mal !") },"""

NUEVO_MASCOTA = """  pip:  { que: T('a little puffin', 'un petit macareux'),
          dice: T("I live on the rocks by the lighthouse. I am very shy, so I hide in every picture — can you find me?",
                  "J'habite sur les rochers, près du phare. Je suis très timide, alors je me cache dans chaque image — tu me trouves ?") },
  luna: { que: T('a husky', 'une husky'),
          dice: T("I love the snow and I remember everything that happened. I will tell you the stories!",
                  "J'adore la neige et je me souviens de tout ce qui s'est passé. C'est moi qui vais te raconter les histoires !") },
  kili: { que: T('an Andean condor', 'un condor des Andes'),
          dice: T("I am the postman of the school. I bring letters and postcards from far away — but I am not very good at landing!",
                  "Je suis le facteur de l'école. J'apporte des lettres et des cartes postales de très loin — mais je me pose très mal !") },"""


def main():
    s = io.open(P, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")
    for v, n in ((VIEJO_PUEDO, NUEVO_PUEDO), (VIEJO_MASCOTA, NUEVO_MASCOTA)):
        if n in t:
            continue
        if t.count(v) != 1:
            print("ANCLA FALLA (%d): %r" % (t.count(v), v[:70]))
            return 1
        t = t.replace(v, n)
    io.open(P, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)
    print("autoexamen y mascotas: en frances")
    return 0


if __name__ == "__main__":
    sys.exit(main())
