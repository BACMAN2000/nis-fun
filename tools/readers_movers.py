# -*- coding: utf-8 -*-
"""Los cuentos de Nordic Little Readers para 3.o y 4.o de primaria (Movers).

Faltaban los dos grados enteros: la estanteria saltaba de G1 a G5. Estos
seis usan los personajes del curso de Movers —Erik, Valentina, Sofia, Mateo
y Luna— y estan repartidos tres para G3 y tres para G4, porque el curso
manda los dos grados al mismo nivel y cada uno tiene que encontrar algo
suyo al abrir la estanteria.

Nueve paginas y frase de A1: mas larga que la de G1, pero todavia una idea
por pagina. El objetivo de cada unidad va dentro de la historia y no se
nombra.

Se importan desde tools/build_readers.py, que es quien los dibuja.
"""

CUENTOS_MOVERS = [
{
 "id": "g3-u1", "grado": "G3", "tema": 1, "nivel": "A1",
 "titulo": "Erik's Weather Machine",
 "objetivo": "Talking about the weather",
 "paginas": [
  {"t": "Erik built a weather machine from an umbrella, two spoons and a "
        "bicycle bell.",
   "clave": ["weather", "machine"], "fondo": "garden",
   "piezas": [("char:movers:erik:5", .38, .66, .52), ("umbrella", .74, .68, .26)]},
  {"t": "'It can tell us if it is going to rain,' he said. Nobody believed "
        "him. Not even Luna.",
   "clave": ["rain"], "fondo": "garden",
   "piezas": [("char:movers:erik:3", .36, .66, .50),
              ("char:movers:luna:1", .70, .74, .28)]},
  {"t": "On Monday the machine rang the bell. It was sunny all day.",
   "clave": ["sunny"], "fondo": "picnic-garden",
   "piezas": [("sunny", .32, .38, .30), ("char:movers:erik:6", .70, .68, .48)]},
  {"t": "On Tuesday the machine said nothing. It rained for six hours.",
   "clave": ["rained"], "fondo": "mirador",
   "piezas": [("rainy", .34, .40, .30), ("char:movers:erik:8", .72, .68, .48)]},
  {"t": "'Your machine is wrong every time,' said Sofia. 'That is very "
        "difficult too,' said Erik.",
   "clave": ["wrong"], "fondo": "classroom",
   "piezas": [("char:movers:sofia:3", .34, .66, .50),
              ("char:movers:erik:2", .68, .66, .50)]},
  {"t": "On Saturday the Club wanted a picnic. Erik looked at his machine "
        "and said: 'Take your coats.'",
   "clave": ["picnic", "coats"], "fondo": "picnic-garden",
   "piezas": [("char:movers:erik:3", .30, .68, .48),
              ("char:movers:valentina:1", .58, .68, .48),
              ("cold", .86, .68, .22)]},
  {"t": "The sky was blue. Everybody laughed at Erik and left their coats "
        "at home.",
   "clave": ["blue", "laughed"], "fondo": "picnic-garden",
   "piezas": [("blue", .30, .38, .24), ("char:movers:erik:6", .68, .68, .48)]},
  {"t": "At four o'clock it snowed. It never snows in September. Everybody "
        "ran home very fast.",
   "clave": ["snowed"], "fondo": "picnic-garden",
   "piezas": [("snowy", .34, .40, .30), ("char:movers:mateo:7", .74, .68, .46)]},
  {"t": "Erik said nothing. He just rang his little bell, once, and put "
        "the machine back in his bag.",
   "clave": ["bell"], "fondo": "garden",
   "piezas": [("char:movers:erik:1", .50, .66, .52)]},
 ],
 "actividad": {"titulo": "What is the weather?",
  "instruccion": "Tap the picture you hear.",
  "items": [{"palabra": "sunny", "img": "sunny"},
            {"palabra": "rainy", "img": "rainy"},
            {"palabra": "snowy", "img": "snowy"},
            {"palabra": "windy", "img": "windy"}]},
},
{
 "id": "g3-u2", "grado": "G3", "tema": 2, "nivel": "A1",
 "titulo": "Luna Runs Away",
 "objetivo": "Pets and past actions",
 "paginas": [
  {"t": "Luna is a husky. She is loyal, she is loud, and on Thursday she "
        "opened the garden gate with her nose.",
   "clave": ["husky", "gate"], "fondo": "garden",
   "piezas": [("char:movers:luna:1", .50, .70, .34)]},
  {"t": "Valentina looked in the classroom. No Luna. Only a chair and "
        "somebody's sandwich.",
   "clave": ["classroom"], "fondo": "classroom",
   "piezas": [("char:movers:valentina:4", .50, .66, .52)]},
  {"t": "Mateo looked in the library. No Luna. But he found the book he "
        "lost last year.",
   "clave": ["library", "found"], "fondo": "library",
   "piezas": [("char:movers:mateo:2", .50, .66, .52)]},
  {"t": "Sofia looked at the map and asked one question: 'Where does Luna "
        "always want to go?'",
   "clave": ["map", "question"], "fondo": "chess-plaza",
   "piezas": [("char:movers:sofia:2", .50, .66, .52)]},
  {"t": "Everybody said it at the same time: 'THE FARM.' Luna loves the "
        "cows and the cows do not love Luna.",
   "clave": ["farm", "cows"], "fondo": "picnic-garden",
   # Luna se nombra pero todavia no aparece: la estan buscando y sale en la
   # pagina siguiente. Se declara para que el revisor no la pida aqui.
   "ausente": ["luna"],
   "piezas": [("cow", .34, .70, .26), ("char:movers:valentina:3", .72, .68, .48)]},
  {"t": "They ran down the hill. Erik ran last because he was carrying his "
        "machine, of course.",
   "clave": ["ran", "hill"], "fondo": "track",
   "piezas": [("char:movers:sofia:7", .30, .68, .46),
              ("char:movers:mateo:7", .52, .68, .46),
              ("char:movers:erik:7", .76, .68, .46)]},
  {"t": "Luna was sitting in the middle of the field. She was not lost. "
        "The cows were.",
   "clave": ["field", "lost"], "fondo": "picnic-garden",
   "piezas": [("char:movers:luna:2", .40, .72, .32), ("cow", .74, .70, .24)]},
  {"t": "She had walked all morning to bring three cows back to the right "
        "gate, and she was very tired.",
   "clave": ["walked", "tired"], "fondo": "picnic-garden",
   "piezas": [("char:movers:luna:4", .50, .72, .32)]},
  {"t": "That night Luna slept for eleven hours, and nobody asked her to "
        "do anything at all.",
   "clave": ["night", "slept"], "fondo": "garden",
   "piezas": [("char:movers:luna:5", .40, .72, .32),
              ("char:movers:valentina:1", .72, .68, .46)]},
 ],
 "actividad": {"titulo": "Farm and pets",
  "instruccion": "Tap the animal you hear.",
  "items": [{"palabra": "dog", "img": "dog"},
            {"palabra": "cow", "img": "cow"},
            {"palabra": "horse", "img": "horse"},
            {"palabra": "duck", "img": "duck"}]},
},
{
 "id": "g3-u3", "grado": "G3", "tema": 3, "nivel": "A1",
 "titulo": "The Longest Picnic",
 "objetivo": "Food and how much there is",
 "paginas": [
  {"t": "The Fjord Club planned a picnic. Everybody had to bring one "
        "thing. Only one.",
   "clave": ["picnic", "bring"], "fondo": "picnic-garden",
   "piezas": [("char:movers:sofia:3", .34, .66, .50),
              ("char:movers:erik:1", .68, .66, .50)]},
  {"t": "Valentina brought bread. Sofia brought cheese. That was a good "
        "start.",
   "clave": ["bread", "cheese"], "fondo": "picnic-garden",
   "piezas": [("char:movers:valentina:1", .34, .68, .48),
              ("char:movers:sofia:1", .68, .68, .48)]},
  {"t": "Mateo brought bread too, because he forgot the list at home.",
   "clave": ["bread", "forgot"], "fondo": "picnic-garden",
   "piezas": [("char:movers:mateo:8", .50, .68, .50)]},
  {"t": "Erik brought a machine that cuts bread. Now there was a lot of "
        "bread and a machine.",
   "clave": ["machine", "lot"], "fondo": "picnic-garden",
   "piezas": [("char:movers:erik:5", .50, .68, .50)]},
  {"t": "'How much water is there?' asked Sofia. There was no water. "
        "Nobody brought water.",
   "clave": ["water", "much"], "fondo": "picnic-garden",
   "piezas": [("char:movers:sofia:4", .50, .66, .50)]},
  {"t": "So they ate bread and cheese and told stories, and it was better "
        "than they expected.",
   "clave": ["ate", "stories"], "fondo": "picnic-garden",
   "piezas": [("char:movers:valentina:6", .30, .70, .46),
              ("char:movers:mateo:6", .54, .70, .46),
              ("char:movers:erik:6", .78, .70, .46)]},
  {"t": "Luna ate four sandwiches when nobody was looking. There were only "
        "six.",
   "clave": ["ate", "four"], "fondo": "picnic-garden",
   "piezas": [("char:movers:luna:3", .50, .72, .34)]},
  {"t": "Then Sofia found a tap behind the tree, and suddenly there was "
        "water for everybody.",
   "clave": ["water", "tree"], "fondo": "garden",
   "piezas": [("char:movers:sofia:2", .50, .68, .50)]},
  {"t": "They stayed until it was dark. It was the longest picnic of the "
        "year, and there was nothing left.",
   "clave": ["dark", "longest"], "fondo": "picnic-garden",
   "piezas": [("char:movers:sofia:1", .26, .68, .46),
              ("char:movers:valentina:1", .48, .68, .46),
              ("char:movers:erik:1", .70, .68, .46),
              ("char:movers:luna:1", .90, .74, .26)]},
 ],
 "actividad": {"titulo": "At the picnic",
  "instruccion": "Tap the picture you hear.",
  "items": [{"palabra": "family", "img": "family"},
            {"palabra": "dog", "img": "dog"},
            {"palabra": "restaurant", "img": "restaurant"},
            {"palabra": "ball", "img": "ball"}]},
},
{
 "id": "g4-u1", "grado": "G4", "tema": 1, "nivel": "A1",
 "titulo": "Valentina Tells a Story",
 "objetivo": "Putting a story in order",
 "paginas": [
  {"t": "Every Friday Valentina tells a story, and every Friday it starts "
        "the same way: 'Once upon a time...'",
   "clave": ["story", "friday"], "fondo": "library",
   "piezas": [("char:movers:valentina:2", .50, .66, .54)]},
  {"t": "This Friday she started, and then she stopped. She had forgotten "
        "the middle.",
   "clave": ["started", "stopped"], "fondo": "library",
   "piezas": [("char:movers:valentina:8", .50, .66, .52)]},
  {"t": "'First a girl found a door,' she said. 'And then... and then...'",
   "clave": ["first", "then"], "fondo": "library",
   "piezas": [("char:movers:valentina:4", .40, .66, .50),
              ("char:movers:mateo:2", .74, .68, .46)]},
  {"t": "'And then a dragon,' said Mateo. 'There is always a dragon.'",
   "clave": ["dragon"], "fondo": "library",
   "piezas": [("char:movers:mateo:3", .50, .68, .50)]},
  {"t": "'And then a castle,' said Sofia, who thinks every story needs a "
        "map and a castle.",
   "clave": ["castle"], "fondo": "library",
   "piezas": [("char:movers:sofia:3", .36, .68, .48), ("castle", .74, .66, .28)]},
  {"t": "'And then a machine,' said Erik. Everybody looked at Erik.",
   "clave": ["machine"], "fondo": "library",
   "piezas": [("char:movers:erik:3", .50, .68, .50)]},
  {"t": "Valentina wrote it all on the board: the door, the dragon, the "
        "castle and, yes, the machine.",
   "clave": ["wrote", "board"], "fondo": "classroom",
   "piezas": [("char:movers:valentina:5", .50, .66, .52)]},
  {"t": "'Now,' she said, 'what happens at the END?' Nobody knew. That is "
        "always the difficult part.",
   "clave": ["end", "difficult"], "fondo": "classroom",
   "piezas": [("char:movers:valentina:3", .34, .66, .50),
              ("char:movers:erik:2", .70, .66, .48)]},
  {"t": "So they finished it together, and the story was longer and much "
        "stranger than the one she forgot.",
   "clave": ["finished", "together"], "fondo": "library",
   "piezas": [("char:movers:valentina:1", .28, .68, .46),
              ("char:movers:sofia:1", .50, .68, .46),
              ("char:movers:mateo:1", .72, .68, .46),
              ("char:movers:erik:1", .92, .68, .46)]},
 ],
 "actividad": {"titulo": "In the story",
  "instruccion": "Tap the picture you hear.",
  "items": [{"palabra": "castle", "img": "castle"},
            {"palabra": "train", "img": "train"},
            {"palabra": "bridge", "img": "bridge"},
            {"palabra": "museum", "img": "museum"}]},
},
{
 "id": "g4-u2", "grado": "G4", "tema": 2, "nivel": "A1",
 "titulo": "Sofia's Map",
 "objetivo": "Places and directions",
 "paginas": [
  {"t": "Sofia draws a map of everything. Her room, the school, the way to "
        "the bakery. Everything.",
   "clave": ["map", "school"], "fondo": "chess-plaza",
   "piezas": [("char:movers:sofia:2", .50, .66, .54)]},
  {"t": "On Saturday she made a map of the town for a visitor who had "
        "never been there.",
   "clave": ["town", "visitor"], "fondo": "main-building-v2",
   "piezas": [("char:movers:sofia:5", .40, .66, .50), ("museum", .76, .68, .26)]},
  {"t": "'Go past the museum, turn left at the bridge, and the theatre is "
        "on your right.'",
   "clave": ["left", "right"], "fondo": "main-building-v2",
   "piezas": [("bridge", .30, .70, .26), ("theatre", .70, .68, .28)]},
  {"t": "'If you see the airport, you have gone too far. Everybody sees "
        "the airport at least once.'",
   "clave": ["airport", "far"], "fondo": "main-building-v2",
   "piezas": [("airport", .50, .68, .30)]},
  {"t": "Mateo used the map on Sunday. He arrived at the police station.",
   "clave": ["police", "arrived"], "fondo": "main-building",
   "piezas": [("char:movers:mateo:4", .34, .68, .48),
              ("police-station", .74, .68, .28)]},
  {"t": "'The map is perfect,' said Sofia. 'You turned left at the wrong "
        "bridge.' There are two bridges.",
   "clave": ["bridge", "wrong"], "fondo": "chess-plaza",
   "piezas": [("char:movers:sofia:3", .36, .66, .50),
              ("char:movers:mateo:2", .70, .68, .48)]},
  {"t": "So she made a second map, with the two bridges drawn very big and "
        "one of them crossed out.",
   "clave": ["second", "big"], "fondo": "classroom",
   "piezas": [("char:movers:sofia:5", .50, .66, .52)]},
  {"t": "Now the visitor finds the theatre, the museum and the restaurant, "
        "and nobody visits the police station by accident.",
   "clave": ["theatre", "restaurant"], "fondo": "main-building-v2",
   "piezas": [("restaurant", .30, .70, .26), ("theatre", .68, .68, .28)]},
  {"t": "Sofia keeps every old map in a box. She says a wrong map still "
        "tells you where somebody went.",
   "clave": ["old", "box"], "fondo": "library",
   "piezas": [("char:movers:sofia:1", .50, .68, .50)]},
 ],
 "actividad": {"titulo": "Places in town",
  "instruccion": "Tap the place you hear.",
  "items": [{"palabra": "museum", "img": "museum"},
            {"palabra": "theatre", "img": "theatre"},
            {"palabra": "restaurant", "img": "restaurant"},
            {"palabra": "airport", "img": "airport"}]},
},
{
 "id": "g4-u3", "grado": "G4", "tema": 3, "nivel": "A1",
 "titulo": "Mateo Loses Everything",
 "objetivo": "My things and where they are",
 "paginas": [
  {"t": "Mateo loses things. Not sometimes. Every single day, and usually "
        "before nine o'clock.",
   "clave": ["loses", "day"], "fondo": "entrance",
   "piezas": [("char:movers:mateo:8", .50, .66, .54)]},
  {"t": "On Monday he lost his gloves. They were in his pocket, which is "
        "where gloves live.",
   "clave": ["gloves", "pocket"], "fondo": "classroom",
   "piezas": [("char:movers:mateo:2", .36, .66, .50), ("gloves", .74, .70, .22)]},
  {"t": "On Tuesday he lost his scarf. Luna had it. Luna thought it was a "
        "present.",
   "clave": ["scarf"], "fondo": "garden",
   "piezas": [("char:movers:luna:1", .36, .72, .30), ("scarf", .70, .70, .24)]},
  {"t": "On Wednesday he lost his bag, with his homework, his lunch and "
        "somebody else's book inside.",
   "clave": ["bag", "homework"], "fondo": "library",
   "piezas": [("char:movers:mateo:4", .38, .66, .50), ("suitcase", .74, .72, .24)]},
  {"t": "'Where did you go this morning?' asked Sofia, who solves these "
        "things with questions, not with luck.",
   "clave": ["where", "morning"], "fondo": "chess-plaza",
   "piezas": [("char:movers:sofia:3", .34, .66, .50),
              ("char:movers:mateo:6", .70, .68, .48)]},
  {"t": "'The track, the library, the garden and the kitchen.' So they "
        "walked all four, in that order.",
   "clave": ["track", "garden"], "fondo": "track",
   "piezas": [("char:movers:sofia:7", .34, .68, .46),
              ("char:movers:mateo:7", .66, .68, .46)]},
  {"t": "The bag was under the bench at the track, exactly where he sat "
        "down to tie his shoe.",
   "clave": ["under", "bench"], "fondo": "track",
   "piezas": [("suitcase", .50, .74, .26)]},
  {"t": "'You do not lose things,' said Sofia. 'You put them down and walk "
        "away. That is different.'",
   "clave": ["lose", "different"], "fondo": "track",
   "piezas": [("char:movers:sofia:1", .36, .68, .48),
              ("char:movers:mateo:1", .68, .68, .48)]},
  {"t": "Now Mateo has a rule: before he stands up, he counts his things. "
        "It works on most days.",
   "clave": ["rule", "counts"], "fondo": "classroom",
   "piezas": [("char:movers:mateo:1", .50, .66, .52)]},
 ],
 "actividad": {"titulo": "My things",
  "instruccion": "Tap the picture you hear.",
  "items": [{"palabra": "gloves", "img": "gloves"},
            {"palabra": "scarf", "img": "scarf"},
            {"palabra": "bag", "img": "suitcase"},
            {"palabra": "socks", "img": "socks"}]},
},
]
