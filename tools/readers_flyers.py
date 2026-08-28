# -*- coding: utf-8 -*-
"""Los cuentos de Nordic Little Readers para 5.o de primaria (Flyers).

La estanteria solo tenia los seis de G1 y en Flyers no habia nada que leer.
Estos seis son para G5: mismos personajes que el curso de ese nivel —Ingrid,
Diego, Maya, Oliver y Kili—, y el hilo es el mismo que el del curso, la
Aurora Expedition.

Son mas largos que los de G1 y la frase ya no repite un patron fijo: a esta
edad el nino sostiene un parrafo corto y lo que engancha es que pase algo.
Cada cuento cubre el objetivo de su unidad (pasado, escribir una postal,
preguntar, comparar, aconsejar, planear) sin nombrarlo.

Se importan desde tools/build_readers.py, que es quien los dibuja y los
escribe a disco. Aqui solo esta el texto y que va en cada pagina.
"""

CUENTOS_FLYERS = [
{
 "id": "g5-u1", "grado": "G5", "tema": 1, "nivel": "A2",
 "titulo": "The Light in the Storm",
 "objetivo": "Past simple: telling what happened",
 "paginas": [
  {"t": "Last winter a big storm came to the fjord. The wind was so strong "
        "that the windows sang all night.",
   "clave": ["storm", "wind"], "fondo": "mirador",
   "piezas": [("char:flyers:ingrid:4", .30, .66, .50), ("windy", .74, .40, .30)]},
  {"t": "Ingrid was in the lighthouse kitchen with a cup of hot chocolate. "
        "Then the light went out.",
   "clave": ["kitchen", "light"], "fondo": "lighthouse-kitchen",
   "piezas": [("char:flyers:ingrid:6", .38, .70, .48), ("hot", .74, .68, .24)]},
  {"t": "Without the light, the boats could not find the harbour. Ingrid "
        "did not wait. She ran up the stairs.",
   "clave": ["boats", "ran"], "fondo": "lighthouse-kitchen",
   "piezas": [("char:flyers:ingrid:7", .48, .70, .52)]},
  {"t": "At the top she found the problem: the old lamp was cold and dark. "
        "Something inside it had broken.",
   "clave": ["lamp", "dark"], "fondo": "facade",
   "piezas": [("char:flyers:ingrid:2", .42, .66, .50), ("cold", .76, .62, .26)]},
  {"t": "Ingrid called her friends. Diego arrived first, with his "
        "microphone and no idea what to do with it.",
   "clave": ["called", "arrived"], "fondo": "entrance",
   "piezas": [("char:flyers:ingrid:3", .34, .68, .48),
              ("char:flyers:diego:4", .66, .68, .48)]},
  {"t": "Maya looked at the lamp for one minute. 'We do not need to fix "
        "it tonight,' she said. 'We need a light NOW.'",
   "clave": ["looked", "said"], "fondo": "facade",
   "piezas": [("char:flyers:maya:2", .38, .66, .48),
              ("char:flyers:ingrid:5", .68, .66, .48)]},
  {"t": "So they carried every torch in the school to the top of the "
        "lighthouse, and Oliver carried two.",
   "clave": ["carried", "torch"], "fondo": "main-building",
   "piezas": [("char:flyers:oliver:7", .34, .68, .48),
              ("char:flyers:maya:7", .62, .68, .46)]},
  {"t": "Kili flew above them in circles, because a condor always wants to "
        "know what the humans are doing.",
   "clave": ["flew", "above"], "fondo": "mirador",
   "piezas": [("char:flyers:kili:2", .52, .32, .22)]},
  {"t": "That night the boats saw a small yellow light on the rock, and "
        "they came home safely, one by one.",
   "clave": ["night", "safely"], "fondo": "mirador",
   "piezas": [("yellow", .30, .40, .24), ("char:flyers:ingrid:1", .64, .68, .48)]},
  {"t": "In the morning the storm stopped. 'We did it,' said Diego. 'And "
        "nobody recorded it,' said his microphone.",
   "clave": ["morning", "stopped"], "fondo": "entrance",
   "piezas": [("char:flyers:diego:1", .30, .68, .48),
              ("char:flyers:ingrid:1", .50, .68, .48),
              ("char:flyers:maya:1", .70, .68, .46),
              ("char:flyers:oliver:1", .88, .68, .46)]},
 ],
 "actividad": {"titulo": "What happened first?",
  "instruccion": "Tap the word you hear.",
  "items": [{"palabra": "storm", "img": "windy"},
            {"palabra": "cold", "img": "cold"},
            {"palabra": "night", "img": "cloudy"},
            {"palabra": "light", "img": "sunny"}]},
},
{
 "id": "g5-u2", "grado": "G5", "tema": 2, "nivel": "A2",
 "titulo": "Kili Delivers",
 "objetivo": "Writing a postcard",
 "paginas": [
  {"t": "Kili is the postbird of Nordic. He is solemn, he is enormous, and "
        "he lands like a falling suitcase.",
   "clave": ["postbird", "lands"], "fondo": "campus-hex",
   "piezas": [("char:flyers:kili:1", .50, .62, .30)]},
  {"t": "On Monday he brought a postcard from Sven, Ingrid's grandfather, "
        "who is travelling in the north.",
   "clave": ["postcard", "brought"], "fondo": "entrance",
   "piezas": [("char:flyers:kili:3", .32, .58, .26),
              ("char:flyers:ingrid:2", .66, .68, .48)]},
  {"t": "'Dear Ingrid,' it said. 'The sky here is green at night. Bring a "
        "warm scarf. Love, Grandpa.'",
   "clave": ["dear", "scarf"], "fondo": "library",
   "piezas": [("char:flyers:ingrid:6", .34, .68, .48), ("scarf", .72, .70, .26)]},
  {"t": "Ingrid wanted to answer, but a postcard is small. What do you "
        "write when you have only six lines?",
   "clave": ["answer", "write"], "fondo": "library",
   "piezas": [("char:flyers:ingrid:5", .50, .68, .50)]},
  {"t": "Diego said: 'Write the news!' Maya said: 'Write the weather!' "
        "Oliver said: 'Write a song about the weather.'",
   "clave": ["news", "weather"], "fondo": "classroom",
   "piezas": [("char:flyers:diego:3", .26, .68, .46),
              ("char:flyers:maya:3", .52, .68, .46),
              ("char:flyers:oliver:3", .78, .68, .46)]},
  {"t": "So Ingrid wrote all three, in very small letters, and then she "
        "could not read her own postcard.",
   "clave": ["wrote", "letters"], "fondo": "library",
   "piezas": [("char:flyers:ingrid:8", .50, .70, .48)]},
  {"t": "She started again. 'Dear Grandpa. We are all well. It rained for "
        "six days. I have the scarf. Come home soon.'",
   "clave": ["rained", "home"], "fondo": "library",
   "piezas": [("char:flyers:ingrid:6", .34, .68, .48), ("rainy", .74, .44, .28)]},
  {"t": "Kili took the postcard in his beak, looked at everybody, and "
        "waited. Nobody knew why.",
   "clave": ["took", "waited"], "fondo": "campus-hex",
   "piezas": [("char:flyers:kili:4", .50, .60, .30)]},
  {"t": "'He wants a biscuit,' said Maya. She was right. She usually is.",
   "clave": ["biscuit", "right"], "fondo": "picnic-garden",
   "piezas": [("char:flyers:maya:1", .34, .68, .46),
              ("char:flyers:kili:5", .70, .60, .28)]},
  {"t": "Then he flew north with the news of a rainy week, and the whole "
        "school watched him go.",
   "clave": ["flew", "north"], "fondo": "mirador",
   "piezas": [("char:flyers:kili:2", .56, .30, .24),
              ("char:flyers:ingrid:1", .28, .70, .44)]},
 ],
 "actividad": {"titulo": "On the postcard",
  "instruccion": "Tap the picture you hear.",
  "items": [{"palabra": "scarf", "img": "scarf"},
            {"palabra": "rainy", "img": "rainy"},
            {"palabra": "grandpa", "img": "grandpa"},
            {"palabra": "bird", "img": "bird"}]},
},
{
 "id": "g5-u3", "grado": "G5", "tema": 3, "nivel": "A2",
 "titulo": "Diego Asks Everyone",
 "objetivo": "Asking questions",
 "paginas": [
  {"t": "Diego had a new microphone and one very big problem: he had no "
        "story for Friday.",
   "clave": ["microphone", "story"], "fondo": "entrance",
   "piezas": [("char:flyers:diego:4", .50, .66, .52)]},
  {"t": "'Have you ever seen the aurora?' he asked the cook. 'Twice,' she "
        "said. 'And I was carrying soup both times.'",
   "clave": ["ever", "seen"], "fondo": "lighthouse-kitchen",
   "piezas": [("char:flyers:diego:3", .40, .70, .46)]},
  {"t": "'What is the best thing about winter?' he asked Oliver. Oliver "
        "played four notes and said: 'That.'",
   "clave": ["best", "winter"], "fondo": "amphitheater",
   "piezas": [("char:flyers:diego:3", .32, .68, .46),
              ("char:flyers:oliver:5", .66, .68, .48)]},
  {"t": "'How deep is the fjord?' he asked Maya. Maya opened a book, and "
        "Diego knew the answer would take a while.",
   "clave": ["deep", "answer"], "fondo": "library",
   "piezas": [("char:flyers:maya:6", .38, .68, .48),
              ("char:flyers:diego:2", .70, .68, .46)]},
  {"t": "'Why do you climb the lighthouse every morning?' he asked "
        "Ingrid. 'Because somebody has to,' she said.",
   "clave": ["why", "climb"], "fondo": "facade",
   "piezas": [("char:flyers:ingrid:2", .36, .68, .48),
              ("char:flyers:diego:3", .68, .68, .46)]},
  {"t": "'Where do you sleep?' he asked Kili. Kili said nothing, because "
        "condors do not give interviews.",
   "clave": ["where", "sleep"], "fondo": "campus-hex",
   "piezas": [("char:flyers:kili:6", .58, .60, .30),
              ("char:flyers:diego:4", .28, .68, .46)]},
  {"t": "On Thursday Diego had forty answers and still no story. He sat "
        "down on the steps and stopped asking.",
   "clave": ["answers", "stopped"], "fondo": "main-building",
   "piezas": [("char:flyers:diego:6", .50, .72, .46)]},
  {"t": "Then Maya sat next to him. 'You asked everyone a question,' she "
        "said. 'Nobody asked YOU one.'",
   "clave": ["question", "nobody"], "fondo": "main-building",
   "piezas": [("char:flyers:maya:6", .36, .72, .44),
              ("char:flyers:diego:6", .64, .72, .44)]},
  {"t": "'So: why do you always carry that microphone?' Diego thought for "
        "a long time. 'Because I want to remember all of this.'",
   "clave": ["carry", "remember"], "fondo": "main-building",
   "piezas": [("char:flyers:diego:1", .50, .70, .48)]},
  {"t": "On Friday the school newspaper had one line on the front page, "
        "and everybody read it twice.",
   "clave": ["newspaper", "read"], "fondo": "library",
   "piezas": [("char:flyers:diego:1", .32, .68, .46),
              ("char:flyers:maya:1", .58, .68, .46),
              ("char:flyers:ingrid:1", .82, .68, .46)]},
 ],
 "actividad": {"titulo": "Question words",
  "instruccion": "Tap the word you hear.",
  "items": [{"palabra": "where", "img": "museum"},
            {"palabra": "why", "img": "chemists"},
            {"palabra": "who", "img": "family"},
            {"palabra": "when", "img": "weather"}]},
},
{
 "id": "g5-u4", "grado": "G5", "tema": 4, "nivel": "A2",
 "titulo": "Maya and the River",
 "objetivo": "Comparing things",
 "paginas": [
  {"t": "Maya wanted to know one thing: is the river older than the "
        "school, or is the school older than the river?",
   "clave": ["older", "river"], "fondo": "garden",
   "piezas": [("char:flyers:maya:2", .50, .66, .52)]},
  {"t": "The school is a hundred years old. That sounded like a lot, until "
        "she looked at the rocks.",
   "clave": ["years", "rocks"], "fondo": "main-building-v2",
   "piezas": [("char:flyers:maya:6", .42, .68, .48)]},
  {"t": "The river is wider than the road and colder than the sea. In "
        "summer it is loud. In winter it is quiet.",
   "clave": ["wider", "colder"], "fondo": "mirador",
   "piezas": [("char:flyers:maya:2", .32, .68, .46), ("cold", .72, .60, .26)]},
  {"t": "Ingrid said the sea was bigger. Maya said bigger is not the same "
        "as older, and they argued happily for an hour.",
   "clave": ["bigger", "same"], "fondo": "mirador",
   "piezas": [("char:flyers:ingrid:3", .34, .68, .48),
              ("char:flyers:maya:3", .66, .68, .46)]},
  {"t": "A whale is bigger than a dolphin. A dolphin is faster than a "
        "boat. But none of them is older than the river.",
   "clave": ["bigger", "faster"], "fondo": "zoo",
   "piezas": [("whale", .30, .74, .24), ("dolphin", .66, .74, .22)]},
  {"t": "Maya measured the water every Monday for two months and wrote "
        "every number in a small green notebook.",
   "clave": ["measured", "wrote"], "fondo": "garden",
   "piezas": [("char:flyers:maya:6", .46, .70, .48), ("green", .78, .70, .20)]},
  {"t": "Oliver asked if the river had a song. Maya said no. Then she "
        "listened for a minute and said: 'Maybe.'",
   "clave": ["song", "listened"], "fondo": "garden",
   "piezas": [("char:flyers:oliver:5", .34, .68, .48),
              ("char:flyers:maya:2", .68, .68, .46)]},
  {"t": "In the library she found a map from 1840. The river was there. "
        "The school was not.",
   "clave": ["map", "library"], "fondo": "library",
   "piezas": [("char:flyers:maya:8", .50, .68, .50)]},
  {"t": "So the river is older. It was here before the school, before the "
        "town, and before anybody counted the years.",
   "clave": ["older", "before"], "fondo": "mirador",
   "piezas": [("char:flyers:maya:1", .40, .68, .48), ("bridge", .76, .64, .26)]},
  {"t": "'That is the best answer I have had all year,' said Diego, and "
        "for once he wrote it down instead of recording it.",
   "clave": ["best", "answer"], "fondo": "garden",
   "piezas": [("char:flyers:diego:1", .34, .68, .46),
              ("char:flyers:maya:1", .66, .68, .46)]},
 ],
 "actividad": {"titulo": "Which is bigger?",
  "instruccion": "Tap the animal you hear.",
  "items": [{"palabra": "whale", "img": "whale"},
            {"palabra": "dolphin", "img": "dolphin"},
            {"palabra": "shark", "img": "shark"},
            {"palabra": "fish", "img": "fish"}]},
},
{
 "id": "g5-u5", "grado": "G5", "tema": 5, "nivel": "A2",
 "titulo": "Oliver's Missing Song",
 "objetivo": "Giving advice",
 "paginas": [
  {"t": "The concert was on Friday and Oliver had written the best song of "
        "his life. On Wednesday he lost it.",
   "clave": ["concert", "lost"], "fondo": "amphitheater",
   "piezas": [("char:flyers:oliver:8", .50, .68, .52)]},
  {"t": "'You should look in your bag,' said Ingrid. He looked. The bag "
        "had two apples and a sock.",
   "clave": ["should", "bag"], "fondo": "classroom",
   "piezas": [("char:flyers:ingrid:3", .34, .68, .48),
              ("char:flyers:oliver:8", .68, .68, .48)]},
  {"t": "'You could ask the music room,' said Maya. The music room said "
        "nothing, because rooms do not talk.",
   "clave": ["could", "music"], "fondo": "classroom",
   "piezas": [("char:flyers:maya:3", .36, .68, .46),
              ("char:flyers:oliver:2", .68, .68, .48)]},
  {"t": "'Why don't you write it again?' asked Diego. 'Because I cannot "
        "remember it,' said Oliver. That was the whole problem.",
   "clave": ["write", "remember"], "fondo": "amphitheater",
   "piezas": [("char:flyers:diego:3", .34, .68, .46),
              ("char:flyers:oliver:6", .68, .70, .46)]},
  {"t": "They searched the library, the track, the garden and the kitchen. "
        "They found a hat, a ring and somebody's homework.",
   "clave": ["searched", "found"], "fondo": "track",
   "piezas": [("sunhat", .24, .72, .22), ("ring", .50, .76, .16),
              ("char:flyers:oliver:7", .78, .68, .46)]},
  {"t": "On Thursday night Oliver sat on the steps and hummed, because "
        "that is what he does when he is sad.",
   "clave": ["night", "sad"], "fondo": "main-building",
   "piezas": [("char:flyers:oliver:6", .50, .72, .48)]},
  {"t": "Kili landed next to him and hummed too. Badly. Very badly. But "
        "the four notes were the right ones.",
   "clave": ["landed", "notes"], "fondo": "main-building",
   "piezas": [("char:flyers:oliver:6", .38, .72, .46),
              ("char:flyers:kili:1", .70, .64, .26)]},
  {"t": "Oliver stood up so fast that he frightened the condor. 'That is "
        "my song! You have been listening all week!'",
   "clave": ["song", "listening"], "fondo": "main-building",
   "piezas": [("char:flyers:oliver:7", .40, .68, .50),
              ("char:flyers:kili:2", .74, .40, .24)]},
  {"t": "He wrote it down twice: one for the concert and one for the "
        "kitchen wall, where nothing ever gets lost.",
   "clave": ["wrote", "wall"], "fondo": "lighthouse-kitchen",
   "piezas": [("char:flyers:oliver:1", .46, .70, .48)]},
  {"t": "On Friday the whole school sang it, and one condor sat on the "
        "roof and sang it worse than everybody.",
   "clave": ["sang", "roof"], "fondo": "amphitheater",
   "piezas": [("char:flyers:oliver:1", .28, .68, .46),
              ("char:flyers:ingrid:1", .48, .68, .46),
              ("char:flyers:maya:1", .68, .68, .46),
              ("char:flyers:kili:1", .88, .60, .24)]},
 ],
 "actividad": {"titulo": "Good advice",
  "instruccion": "Tap the picture you hear.",
  "items": [{"palabra": "bag", "img": "suitcase"},
            {"palabra": "hat", "img": "sunhat"},
            {"palabra": "ring", "img": "ring"},
            {"palabra": "bird", "img": "bird"}]},
},
{
 "id": "g5-u6", "grado": "G5", "tema": 6, "nivel": "A2",
 "titulo": "The Night of the Aurora",
 "objetivo": "Making plans",
 "paginas": [
  {"t": "Maya read that the aurora would be visible on Saturday, and the "
        "whole school started planning at once.",
   "clave": ["aurora", "planning"], "fondo": "classroom",
   "piezas": [("char:flyers:maya:8", .50, .68, .50)]},
  {"t": "'We are going to walk to the mirador,' said Ingrid. 'We are going "
        "to leave at eight and we are NOT going to be late.'",
   "clave": ["going", "leave"], "fondo": "classroom",
   "piezas": [("char:flyers:ingrid:3", .40, .68, .50),
              ("char:flyers:maya:1", .70, .68, .46)]},
  {"t": "Oliver was going to bring the guitar. Diego was going to bring "
        "the microphone. Kili was going to bring himself.",
   "clave": ["bring", "guitar"], "fondo": "entrance",
   "piezas": [("char:flyers:oliver:5", .28, .68, .46),
              ("char:flyers:diego:4", .54, .68, .46),
              ("char:flyers:kili:1", .82, .60, .26)]},
  {"t": "They needed warm clothes, because at the top of the hill the wind "
        "never asks how you feel about it.",
   "clave": ["warm", "wind"], "fondo": "lighthouse-kitchen",
   "piezas": [("gloves", .26, .70, .20), ("scarf", .50, .68, .24),
              ("socks", .74, .72, .18)]},
  {"t": "On Saturday at eight they left. At eight fifteen Diego went back "
        "for the microphone he had left at home.",
   "clave": ["saturday", "left"], "fondo": "entrance",
   "piezas": [("char:flyers:diego:7", .50, .70, .48)]},
  {"t": "The walk was long and dark and cold, and nobody said one word "
        "about turning round.",
   "clave": ["walk", "dark"], "fondo": "labyrinth",
   "piezas": [("char:flyers:ingrid:7", .30, .68, .46),
              ("char:flyers:maya:7", .52, .68, .44),
              ("char:flyers:oliver:7", .74, .68, .44)]},
  {"t": "At the top they waited. Nothing happened. It was cold. Somebody "
        "said the word 'chocolate' and everybody agreed.",
   "clave": ["waited", "cold"], "fondo": "mirador",
   "piezas": [("cold", .26, .60, .24), ("char:flyers:ingrid:6", .62, .70, .46)]},
  {"t": "And then the sky turned green. Not a little green. All of it, "
        "from the sea to the mountain.",
   "clave": ["sky", "green"], "fondo": "mirador",
   "piezas": [("green", .34, .34, .26), ("rainbow", .70, .34, .30)]},
  {"t": "Diego did not record anything. He said afterwards that he forgot, "
        "but Maya says he chose to watch.",
   "clave": ["record", "watch"], "fondo": "mirador",
   "piezas": [("char:flyers:diego:1", .38, .70, .46),
              ("char:flyers:maya:1", .66, .70, .44)]},
  {"t": "They walked home very late and very happy, and on Monday nobody "
        "could explain it to the people who had stayed in bed.",
   "clave": ["home", "happy"], "fondo": "entrance",
   "piezas": [("char:flyers:ingrid:1", .24, .68, .46),
              ("char:flyers:diego:1", .44, .68, .46),
              ("char:flyers:maya:1", .64, .68, .46),
              ("char:flyers:oliver:1", .84, .68, .46)]},
 ],
 "actividad": {"titulo": "What do we take?",
  "instruccion": "Tap the picture you hear.",
  "items": [{"palabra": "gloves", "img": "gloves"},
            {"palabra": "scarf", "img": "scarf"},
            {"palabra": "socks", "img": "socks"},
            {"palabra": "umbrella", "img": "umbrella"}]},
},
]
