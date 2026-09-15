# -*- coding: utf-8 -*-
"""Rimas tradicionales inglesas, primeras palabras y frases de uso diario
para Fun for Nordic. Escribe songs/tradicionales.json.

Todas las letras son de dominio público (rimas populares anteriores a 1900 o
folclore de patio sin autor). Las de autoría del siglo XX (The Wheels on the
Bus, I'm a Little Teapot) llevan sólo el título y el primer verso.

Las notas para el profesor (uso, nota, gramatica) van en INGLÉS porque se
leen en el portal, que está en inglés (rhymes.html).

Cada pieza sale etiquetada con las palabras que están en la lista oficial YLE
(nis-portal/yle/wordlist-2025.json) y con el nivel sugerido: el más bajo que
cubre 9 de cada 10 de esas palabras.

    python songs/tradicionales.py
"""
import json, re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SALIDA = AQUI / "tradicionales.json"
YLE = Path(r"C:\Projects\nis-portal\yle\wordlist-2025.json")

# ---------------------------------------------------------------- rimas ----
# tipo: contar (para elegir quién la lleva) · palmas · comba · gestos · nursery
RIMAS = [
  # ---- para contar ---------------------------------------------------------
  dict(id="eeny-meeny", tipo="contar", titulo="Eeny, meeny, miny, moe", edad="4+",
    letra="Eeny, meeny, miny, moe,\nCatch a tiger by the toe.\nIf he hollers, let him go,\nEeny, meeny, miny, moe.",
    coda="My mother told me to pick the very best one, and you are not it.",
    uso="Point at one child per word; the last one pointed at is 'it' (or is out).",
    gramatica="imperatives: catch, let him go"),
  dict(id="one-potato", tipo="contar", titulo="One potato, two potato", edad="4+",
    letra="One potato, two potato, three potato, four,\nFive potato, six potato, seven potato, more.",
    uso="Everyone holds out two fists ('spuds up!'). The counter taps one fist per word; the fist tapped on 'more' goes behind the back. The last fist left wins.",
    gramatica="numbers 1-7"),
  dict(id="ip-dip", tipo="contar", titulo="Ip dip", edad="4+",
    letra="Ip dip, sky blue,\nWho's it? Not you.",
    variante="Ip dip do, the cat's got the flu,\nthe dog's got the chicken pox,\nout goes you.",
    uso="British version. One child per word; whoever lands on 'you' is out.",
    gramatica="Who's it? / has got"),
  dict(id="bubble-gum", tipo="contar", titulo="Bubble gum, bubble gum", edad="5+",
    letra="Bubble gum, bubble gum, in a dish,\nHow many pieces do you wish?",
    uso="The child pointed at on 'wish' says a number; keep counting up to that number and that child is out.",
    gramatica="How many …?"),
  dict(id="engine-engine", tipo="contar", titulo="Engine, engine, number nine", edad="5+",
    letra="Engine, engine, number nine,\nGoing down Chicago line.\nIf the train should jump the track,\nDo you want your money back?",
    coda="Yes → Y-E-S spells yes, and you are not it. / No → N-O spells no, and you are not it.",
    uso="The child pointed at on 'back' answers yes or no; spell the answer out and keep counting.",
    gramatica="Do you want …? / spelling"),
  dict(id="inky-pinky", tipo="contar", titulo="Inky pinky ponky", edad="4+",
    letra="Inky pinky ponky,\nDaddy bought a donkey,\nDonkey died, Daddy cried,\nInky pinky ponky.",
    uso="One child per word; the last one is 'it'.",
    gramatica="past simple: bought, died, cried"),
  dict(id="tinker-tailor", tipo="contar", titulo="Tinker, tailor", edad="6+",
    letra="Tinker, tailor, soldier, sailor,\nRich man, poor man, beggar man, thief.",
    uso="Count buttons, seeds or petals: the word you land on says 'what you will be when you grow up'.",
    gramatica="jobs"),
  dict(id="fish-alive", tipo="contar", titulo="One, two, three, four, five", edad="4+",
    letra="One, two, three, four, five,\nOnce I caught a fish alive.\nSix, seven, eight, nine, ten,\nThen I let it go again.\n\nWhy did you let it go?\nBecause it bit my finger so.\nWhich finger did it bite?\nThis little finger on my right.",
    uso="Count on your fingers; at the end hold up the little finger of your right hand.",
    gramatica="numbers 1-10 · past simple · Why …? Because …"),
  dict(id="icka-bicka", tipo="contar", titulo="Icka bicka soda cracker", edad="4+",
    letra="Icka bicka soda cracker,\nIcka bicka boo.\nIcka bicka soda cracker,\nOut goes you!",
    uso="One child per word; whoever lands on 'you' is out."),
  dict(id="sky-blue", tipo="contar", titulo="One, two, sky blue", edad="4+",
    letra="One, two, sky blue,\nAll out but you!",
    uso="The shortest one: good for choosing quickly between two or three."),

  # ---- palmas --------------------------------------------------------------
  dict(id="miss-mary-mack", tipo="palmas", titulo="Miss Mary Mack", edad="6+",
    letra="Miss Mary Mack, Mack, Mack,\nAll dressed in black, black, black,\nWith silver buttons, buttons, buttons,\nAll down her back, back, back.\n\nShe asked her mother, mother, mother,\nFor fifty cents, cents, cents,\nTo see the elephants, elephants, elephants,\nJump over the fence, fence, fence.\n\nThey jumped so high, high, high,\nThey reached the sky, sky, sky,\nAnd they didn't come back, back, back,\nTill the Fourth of July, ly, ly.",
    uso="In pairs, face to face. Basic pattern: clap your own hands – cross-clap with your partner – own clap – both hands with your partner. Each word said three times gets three beats.",
    gramatica="past simple: asked, jumped, reached, didn't come"),
  dict(id="sailor-went-to-sea", tipo="palmas", titulo="A Sailor Went to Sea", edad="5+",
    letra="A sailor went to sea, sea, sea,\nTo see what he could see, see, see,\nBut all that he could see, see, see,\nWas the bottom of the deep blue sea, sea, sea.",
    uso="Clapping in pairs; on every 'sea' put a hand to your forehead as if looking far away. Variants: 'went to chop' (chopping gesture), 'went to knee' (touch knee), and finally 'sea, chop, knee' with all three gestures in a row.",
    gramatica="past simple: went, could see · homophones sea/see"),
  dict(id="pat-a-cake", tipo="palmas", titulo="Pat-a-cake", edad="3+",
    letra="Pat-a-cake, pat-a-cake, baker's man,\nBake me a cake as fast as you can;\nPat it and prick it and mark it with B,\nPut it in the oven for baby and me.",
    uso="Clap with an adult or a partner; mime 'pat', 'prick' and 'mark'; swap the letter for the child's initial.",
    gramatica="imperatives: bake, pat, prick, mark, put"),
  dict(id="double-double", tipo="palmas", titulo="Double, double", edad="5+",
    letra="Double, double, this, this,\nDouble, double, that, that,\nDouble this, double that,\nDouble, double, this, that.",
    uso="'Double' = fists against fists; 'this' = palms against palms; 'that' = backs of the hands together. Faster every round.",
    gramatica="this / that"),
  dict(id="down-down-baby", tipo="palmas", titulo="Down, down, baby", edad="6+",
    letra="Down, down, baby, down by the roller coaster,\nSweet, sweet baby, I'll never let you go.\nShimmy, shimmy, cocoa pop, shimmy, shimmy, pow!\nShimmy, shimmy, cocoa pop, shimmy, shimmy, pow!",
    nota="Playground rhyme with countless versions; this is the most common one. First block only.",
    uso="Clapping in pairs with a shoulder shake on 'shimmy'."),

  # ---- comba ---------------------------------------------------------------
  dict(id="teddy-bear", tipo="comba", titulo="Teddy Bear, Teddy Bear", edad="5+",
    letra="Teddy bear, teddy bear, turn around,\nTeddy bear, teddy bear, touch the ground,\nTeddy bear, teddy bear, show your shoe,\nTeddy bear, teddy bear, that will do.\n\nTeddy bear, teddy bear, go upstairs,\nTeddy bear, teddy bear, say your prayers,\nTeddy bear, teddy bear, turn out the light,\nTeddy bear, teddy bear, say good night!",
    uso="While skipping, do each command without stopping. Without a rope it works as an action rhyme (TPR).",
    gramatica="imperatives: turn around, touch, show, go, say"),
  dict(id="cinderella", tipo="comba", titulo="Cinderella, dressed in yella", edad="6+",
    letra="Cinderella, dressed in yella,\nWent upstairs to kiss a fella.\nMade a mistake and kissed a snake.\nHow many doctors did it take?\nOne, two, three, four …",
    uso="Count until the skipper trips on the rope: that number is her score.",
    gramatica="past simple · How many …?"),
  dict(id="i-like-coffee", tipo="comba", titulo="I like coffee, I like tea", edad="5+",
    letra="I like coffee, I like tea,\nI like [Freya] to jump with me!",
    uso="The skipper calls a classmate by name and that child jumps in with her. Great for learning everyone's names.",
    gramatica="I like … · to + infinitive"),

  # ---- gestos y dedos ------------------------------------------------------
  dict(id="head-shoulders", tipo="gestos", titulo="Head, Shoulders, Knees and Toes", edad="3+",
    letra="Head, shoulders, knees and toes, knees and toes,\nHead, shoulders, knees and toes, knees and toes,\nAnd eyes and ears and mouth and nose,\nHead, shoulders, knees and toes, knees and toes.",
    uso="Touch each part as you name it; faster every round; then leave words out one by one and only do the gesture.",
    gramatica="parts of the body"),
  dict(id="if-youre-happy", tipo="gestos", titulo="If You're Happy and You Know It", edad="3+",
    letra="If you're happy and you know it, clap your hands. (clap, clap)\nIf you're happy and you know it, clap your hands. (clap, clap)\nIf you're happy and you know it, and you really want to show it,\nIf you're happy and you know it, clap your hands. (clap, clap)",
    coda="… stamp your feet · nod your head · shout 'Hooray!' · do all four.",
    gramatica="If + present · imperatives"),
  dict(id="open-shut-them", tipo="gestos", titulo="Open, Shut Them", edad="3+",
    letra="Open, shut them, open, shut them,\nGive a little clap, clap, clap.\nOpen, shut them, open, shut them,\nPut them in your lap, lap, lap.",
    uso="Open and close both hands; a gentle way to ask for quiet and still hands on the carpet.",
    gramatica="imperatives"),
  dict(id="two-little-dickie-birds", tipo="gestos", titulo="Two Little Dickie Birds", edad="3+",
    letra="Two little dickie birds sitting on a wall,\nOne named Peter, one named Paul.\nFly away, Peter! Fly away, Paul!\nCome back, Peter! Come back, Paul!",
    uso="Both index fingers are the birds; hide them behind your back on 'fly away' and bring them back on 'come back'. Swap the names for children in the class.",
    gramatica="imperatives: fly away, come back"),
  dict(id="this-little-piggy", tipo="gestos", titulo="This Little Piggy", edad="2+",
    letra="This little piggy went to market,\nThis little piggy stayed home,\nThis little piggy had roast beef,\nThis little piggy had none,\nAnd this little piggy cried 'Wee, wee, wee!'\nAll the way home.",
    uso="One toe (or finger) per line; tickle on the last one.",
    gramatica="past simple: went, stayed, had, cried"),
  dict(id="round-the-garden", tipo="gestos", titulo="Round and Round the Garden", edad="2+",
    letra="Round and round the garden,\nLike a teddy bear;\nOne step, two step,\nTickle you under there!",
    uso="Circle a finger on the child's palm, two steps up the arm, and tickle under the arm."),
  dict(id="itsy-bitsy-spider", tipo="gestos", titulo="Itsy Bitsy Spider", edad="3+",
    letra="The itsy bitsy spider climbed up the water spout.\nDown came the rain and washed the spider out.\nOut came the sun and dried up all the rain,\nAnd the itsy bitsy spider climbed up the spout again.",
    nota="In the UK: Incy Wincy Spider.",
    uso="Fingers climb (thumb to index finger, alternating), rain falls with wiggling fingers, the sun is a circle with both arms.",
    gramatica="past simple: climbed, came, washed, dried"),
  dict(id="wind-the-bobbin", tipo="gestos", titulo="Wind the Bobbin Up", edad="3+",
    letra="Wind the bobbin up, wind the bobbin up,\nPull, pull, clap, clap, clap.\nWind it back again, wind it back again,\nPull, pull, clap, clap, clap.\n\nPoint to the ceiling, point to the floor,\nPoint to the window, point to the door.\nClap your hands together, one, two, three,\nPut your hands upon your knee.",
    uso="Roll your fists around each other, pull, clap; then point to each thing in the classroom.",
    gramatica="imperatives · ceiling, floor, window, door"),
  dict(id="five-little-ducks", tipo="gestos", titulo="Five Little Ducks", edad="4+",
    letra="Five little ducks went swimming one day,\nOver the hills and far away.\nMother duck said, 'Quack, quack, quack, quack!'\nBut only four little ducks came back.",
    coda="Repeat with four, three, two, one … 'But none of the five little ducks came back.' Last verse: 'Sad mother duck went out one day … and all of the five little ducks came back!'",
    uso="One hand is the ducklings (fold one finger down each round), the other is the mother duck.",
    gramatica="counting down · past simple: went, said, came"),
  dict(id="five-little-monkeys", tipo="gestos", titulo="Five Little Monkeys", edad="4+",
    letra="Five little monkeys jumping on the bed,\nOne fell off and bumped his head.\nMama called the doctor and the doctor said,\n'No more monkeys jumping on the bed!'",
    coda="Repeat with four, three, two, one. Ending: 'No little monkeys jumping on the bed, none fell off and bumped their head …'",
    uso="Five fingers jump on your palm; take one away each round; wag a finger on 'No more monkeys'.",
    gramatica="counting down · No more …!"),
  dict(id="ten-in-the-bed", tipo="gestos", titulo="Ten in the Bed", edad="4+",
    letra="There were ten in the bed and the little one said,\n'Roll over, roll over!'\nSo they all rolled over and one fell out.",
    coda="Repeat from nine down to one. Ending: 'There was one in the bed and the little one said, Good night!'",
    uso="Roll your arms on 'roll over'; show the number with your fingers.",
    gramatica="There were … · counting down"),

  # ---- nursery rhymes clásicas --------------------------------------------
  dict(id="twinkle-twinkle", tipo="nursery", titulo="Twinkle, Twinkle, Little Star", edad="2+",
    letra="Twinkle, twinkle, little star,\nHow I wonder what you are!\nUp above the world so high,\nLike a diamond in the sky.\nTwinkle, twinkle, little star,\nHow I wonder what you are!",
    nota="Jane Taylor, 1806. Same tune as the ABC song and Baa, Baa, Black Sheep."),
  dict(id="humpty-dumpty", tipo="nursery", titulo="Humpty Dumpty", edad="3+",
    letra="Humpty Dumpty sat on a wall,\nHumpty Dumpty had a great fall.\nAll the king's horses and all the king's men\nCouldn't put Humpty together again.",
    gramatica="past simple: sat, had, couldn't"),
  dict(id="hickory-dickory", tipo="nursery", titulo="Hickory Dickory Dock", edad="3+",
    letra="Hickory dickory dock,\nThe mouse ran up the clock.\nThe clock struck one,\nThe mouse ran down,\nHickory dickory dock.",
    coda="Carry on with two (the mouse said 'boo'), three (the mouse said 'whee') … up to twelve.",
    gramatica="telling the time · up / down"),
  dict(id="hey-diddle-diddle", tipo="nursery", titulo="Hey Diddle Diddle", edad="3+",
    letra="Hey diddle diddle,\nThe cat and the fiddle,\nThe cow jumped over the moon.\nThe little dog laughed to see such fun,\nAnd the dish ran away with the spoon.",
    gramatica="past simple: jumped, laughed, ran away"),
  dict(id="jack-and-jill", tipo="nursery", titulo="Jack and Jill", edad="3+",
    letra="Jack and Jill went up the hill\nTo fetch a pail of water.\nJack fell down and broke his crown,\nAnd Jill came tumbling after.",
    gramatica="past simple: went, fell, broke, came"),
  dict(id="little-miss-muffet", tipo="nursery", titulo="Little Miss Muffet", edad="3+",
    letra="Little Miss Muffet\nSat on a tuffet,\nEating her curds and whey.\nAlong came a spider,\nWho sat down beside her,\nAnd frightened Miss Muffet away."),
  dict(id="london-bridge", tipo="nursery", titulo="London Bridge Is Falling Down", edad="4+",
    letra="London Bridge is falling down,\nFalling down, falling down.\nLondon Bridge is falling down,\nMy fair lady.",
    coda="Build it up with wood and clay … / Wood and clay will wash away … / Build it up with iron bars … / Iron bars will bend and break … / Build it up with silver and gold …",
    uso="Two children make a bridge with their arms; the others file underneath and the bridge falls on whoever is passing at 'my fair lady'.",
    gramatica="present continuous: is falling"),
  dict(id="mary-had-a-little-lamb", tipo="nursery", titulo="Mary Had a Little Lamb", edad="3+",
    letra="Mary had a little lamb,\nLittle lamb, little lamb,\nMary had a little lamb,\nIts fleece was white as snow.\n\nAnd everywhere that Mary went,\nMary went, Mary went,\nEverywhere that Mary went,\nThe lamb was sure to go.",
    nota="Sarah Josepha Hale, 1830.",
    gramatica="past simple: had, was, went"),
  dict(id="row-your-boat", tipo="nursery", titulo="Row, Row, Row Your Boat", edad="3+",
    letra="Row, row, row your boat,\nGently down the stream.\nMerrily, merrily, merrily, merrily,\nLife is but a dream.",
    uso="In pairs, sitting face to face holding hands, rowing back and forth. Can be sung as a round.",
    gramatica="imperative: row"),
  dict(id="rain-rain", tipo="nursery", titulo="Rain, Rain, Go Away", edad="2+",
    letra="Rain, rain, go away,\nCome again another day.\nLittle [Nico] wants to play,\nRain, rain, go away.",
    uso="Put a child's name in the third line.",
    gramatica="imperatives · wants to play"),
  dict(id="buckle-my-shoe", tipo="nursery", titulo="One, Two, Buckle My Shoe", edad="3+",
    letra="One, two, buckle my shoe;\nThree, four, knock at the door;\nFive, six, pick up sticks;\nSeven, eight, lay them straight;\nNine, ten, a big fat hen.",
    gramatica="numbers 1-10 · rhyming sounds"),
  dict(id="baa-baa-black-sheep", tipo="nursery", titulo="Baa, Baa, Black Sheep", edad="2+",
    letra="Baa, baa, black sheep,\nHave you any wool?\nYes sir, yes sir,\nThree bags full.\nOne for the master,\nAnd one for the dame,\nAnd one for the little boy\nWho lives down the lane.",
    gramatica="Have you any …? / Yes, sir"),
  dict(id="three-blind-mice", tipo="nursery", titulo="Three Blind Mice", edad="4+",
    letra="Three blind mice, three blind mice,\nSee how they run, see how they run!\nThey all ran after the farmer's wife,\nWho cut off their tails with a carving knife.\nDid you ever see such a thing in your life\nAs three blind mice?",
    nota="Can be sung as a round."),
  dict(id="ring-a-ring", tipo="nursery", titulo="Ring a Ring o' Roses", edad="2+",
    letra="Ring-a-ring o' roses,\nA pocket full of posies,\nA-tishoo! A-tishoo!\nWe all fall down.",
    uso="Circle holding hands, walking round; everyone drops to the floor on 'fall down'."),
  dict(id="hot-cross-buns", tipo="nursery", titulo="Hot Cross Buns", edad="3+",
    letra="Hot cross buns! Hot cross buns!\nOne a penny, two a penny,\nHot cross buns!\nIf you have no daughters,\nGive them to your sons,\nOne a penny, two a penny,\nHot cross buns!"),
  dict(id="old-macdonald", tipo="nursery", titulo="Old MacDonald Had a Farm", edad="3+",
    letra="Old MacDonald had a farm, E-I-E-I-O!\nAnd on that farm he had a cow, E-I-E-I-O!\nWith a moo-moo here and a moo-moo there,\nHere a moo, there a moo, everywhere a moo-moo,\nOld MacDonald had a farm, E-I-E-I-O!",
    coda="Repeat with pig (oink), duck (quack), sheep (baa), horse (neigh), dog (woof), chicken (cluck) … adding up the sounds.",
    gramatica="farm animals · here / there / everywhere"),
  dict(id="little-bo-peep", tipo="nursery", titulo="Little Bo Peep", edad="4+",
    letra="Little Bo Peep has lost her sheep,\nAnd doesn't know where to find them.\nLeave them alone, and they'll come home,\nWagging their tails behind them.",
    gramatica="present perfect: has lost · they'll come"),
  dict(id="polly-kettle", tipo="nursery", titulo="Polly Put the Kettle On", edad="3+",
    letra="Polly put the kettle on,\nPolly put the kettle on,\nPolly put the kettle on,\nWe'll all have tea.\n\nSukey take it off again,\nSukey take it off again,\nSukey take it off again,\nThey've all gone away.",
    gramatica="put on / take off"),
  dict(id="pease-porridge", tipo="nursery", titulo="Pease Porridge Hot", edad="3+",
    letra="Pease porridge hot,\nPease porridge cold,\nPease porridge in the pot,\nNine days old.\n\nSome like it hot,\nSome like it cold,\nSome like it in the pot,\nNine days old.",
    uso="Also a clapping game: own hands – knees – partner's hands.",
    gramatica="hot / cold · Some like it …"),
  dict(id="star-light", tipo="nursery", titulo="Star Light, Star Bright", edad="3+",
    letra="Star light, star bright,\nFirst star I see tonight,\nI wish I may, I wish I might,\nHave the wish I wish tonight.",
    gramatica="I wish …"),
  dict(id="jack-be-nimble", tipo="nursery", titulo="Jack Be Nimble", edad="3+",
    letra="Jack be nimble,\nJack be quick,\nJack jump over\nThe candlestick.",
    uso="Jump over an object on the floor on 'jump over'.",
    gramatica="imperatives · adjectives"),
  dict(id="little-jack-horner", tipo="nursery", titulo="Little Jack Horner", edad="4+",
    letra="Little Jack Horner\nSat in the corner,\nEating a Christmas pie;\nHe put in his thumb,\nAnd pulled out a plum,\nAnd said, 'What a good boy am I!'"),
  dict(id="rub-a-dub-dub", tipo="nursery", titulo="Rub-a-dub-dub", edad="4+",
    letra="Rub-a-dub-dub,\nThree men in a tub,\nAnd who do you think they be?\nThe butcher, the baker,\nThe candlestick-maker,\nTurn them out, knaves all three.",
    gramatica="jobs"),
  dict(id="hush-little-baby", tipo="nursery", titulo="Hush, Little Baby", edad="2+",
    letra="Hush, little baby, don't say a word,\nMama's gonna buy you a mockingbird.\nAnd if that mockingbird won't sing,\nMama's gonna buy you a diamond ring.",
    nota="Traditional lullaby; it goes on as a chain (diamond ring → looking glass → billy goat …).",
    gramatica="going to · if … won't"),
  dict(id="rock-a-bye", tipo="nursery", titulo="Rock-a-bye Baby", edad="2+",
    letra="Rock-a-bye baby, on the tree top,\nWhen the wind blows, the cradle will rock.\nWhen the bough breaks, the cradle will fall,\nAnd down will come baby, cradle and all.",
    gramatica="When + present, will"),

  # ---- con autor del s. XX: sólo título y primer verso ----------------------
  dict(id="wheels-on-the-bus", tipo="gestos", titulo="The Wheels on the Bus", edad="3+",
    letra="The wheels on the bus go round and round …",
    nota="Verna Hills, 1939. Lyrics under copyright, not included. Pattern: wheels (round and round), wipers (swish), horn (beep), doors (open and shut), people (up and down), babies (wah), mummies (shh).",
    uso="Each verse has its gesture; the children suggest new parts of the bus."),
  dict(id="little-teapot", tipo="gestos", titulo="I'm a Little Teapot", edad="3+",
    letra="I'm a little teapot, short and stout …",
    nota="Kelley and Sanders, 1939. Lyrics under copyright, not included.",
    uso="One arm on the hip (the handle), the other is the spout; tip over on 'tip me over'."),
]

# ------------------------------------------------------------ vocabulario ----
PRIMERAS_100 = {
  "people_family":  "I you he she we they mom dad friend teacher".split(),
  "home_school":    "home school room door window chair table book pencil bag".split(),
  "food_drink":     "water milk bread apple banana rice egg soup juice cookie".split(),
  "animals":        "dog cat bird fish horse cow sheep duck lion rabbit".split(),
  "colours_size":   "red blue green yellow black white big small long short".split(),
  "actions":        "go come eat drink play read write draw run jump".split(),
  "feelings_needs": "happy sad tired hungry thirsty sick good bad please sorry".split(),
  "daily_routine":  "wake sleep wash brush dress open close sit stand listen".split(),
  "places_nature":  "park street car bus tree flower sun rain sky beach".split(),
  "function_words": "the a and or in on under with from to".split(),
}
DOLCH_PRE_PRIMER = ("a and away big blue can come down find for funny go help here I in is it "
  "jump little look make me my not one play red run said see the three to two up we where yellow you").split()
DOLCH_PRIMER = ("all am are at ate be black brown but came did do eat four get good have he into like "
  "must new no now on our out please pretty ran ride saw say she so soon that there they this too under "
  "want was well went what white who will with yes").split()

# ----------------------------------------------------------------- frases ----
FRASES = {
  "greetings": [
    "Hello! How are you?", "I'm fine, thank you. And you?", "My name is …. What's your name?",
    "Nice to meet you.", "Good morning! / Good afternoon!", "Goodbye! See you tomorrow.",
  ],
  "classroom": [
    "May I go to the bathroom?", "I don't understand.", "Can you repeat that, please?",
    "How do you say … in English?", "I forgot my pencil.", "I know the answer!",
    "Can I have a rubber, please?", "I've finished.", "Please open your book.", "Let's read aloud.",
  ],
  "playground": [
    "Do you want to play?", "Can I play too?", "Your turn!", "My turn!", "I'm it!",
    "Let's make a team.", "You're out!", "That's not fair.", "Good game!", "Let's play again.",
  ],
  "needs_feelings": [
    "I'm hungry.", "I'm thirsty.", "I want some water, please.", "I'm tired.", "I feel sick.",
    "Can I have …, please?", "Excuse me.", "I'm sorry.", "Thank you very much.", "You're welcome.",
  ],
  "home": [
    "It's time for bed.", "Wash your hands.", "Brush your teeth.", "Put on your shoes.",
    "Switch off the light.", "Shut the door, please.", "What's for lunch?", "Can I watch TV?",
  ],
}

# -------------------------------------------------------- etiquetado YLE ----
NIVELES = ["starters", "movers", "flyers"]

def carga_yle():
    d = json.load(open(YLE, encoding="utf-8"))
    nivel = {}
    for niv in NIVELES:            # el más bajo gana
        for entrada in d[niv]:
            e = re.sub(r"\(.*?\)", "", entrada).lower()
            for w in re.split(r"[/,]", e):
                w = w.strip().rstrip(".")
                if w and w not in nivel:
                    nivel[w] = niv
    return nivel

def tokens(texto):
    t = re.sub(r"[^a-z' ]+", " ", texto.lower().replace("\n", " "))
    return [w.strip("'") for w in t.split() if w.strip("'")]

def etiqueta(pieza, nivel):
    texto = " ".join(pieza.get(k, "") for k in ("letra", "coda", "variante"))
    vistas, yle = set(), []
    for w in tokens(texto):
        if w in nivel and w not in vistas:
            vistas.add(w); yle.append(w)
    # nivel sugerido: el más bajo que cubre 9 de cada 10 palabras YLE de la pieza
    cuenta = {n: sum(1 for w in yle if nivel[w] == n) for n in NIVELES}
    acumulado, sugerido = 0, "flyers"
    for n in NIVELES:
        acumulado += cuenta[n]
        if yle and acumulado >= 0.9 * len(yle):
            sugerido = n; break
    pieza["palabras_yle"] = yle
    pieza["yle_por_nivel"] = cuenta
    pieza["nivel_yle"] = sugerido
    return pieza

def main():
    nivel = carga_yle()
    rimas = [etiqueta(dict(p), nivel) for p in RIMAS]
    def con_nivel(lista):
        return [{"palabra": w, "yle": nivel.get(w.lower())} for w in lista]
    salida = {
      "_nota": ("Rimas tradicionales inglesas (dominio público), primeras palabras y frases de uso "
                "diario, para Fun for Nordic; las notas al profesor van en inglés porque se leen en "
                "el portal. 'palabras_yle' son las palabras de la pieza que están en la lista oficial "
                "YLE 2025 y 'nivel_yle' el nivel más bajo que cubre 9 de cada 10 de ellas. Los ids "
                "con nota de autoría del s. XX llevan sólo el primer verso."),
      "_fuente_yle": "nis-portal/yle/wordlist-2025.json",
      "tipos": {"contar": "Counting-out", "palmas": "Clapping", "comba": "Skipping",
                "gestos": "Actions & fingerplays", "nursery": "Nursery rhymes"},
      "rimas": rimas,
      "vocabulario": {
        "primeras_100": {k: con_nivel(v) for k, v in PRIMERAS_100.items()},
        "dolch_pre_primer": con_nivel(DOLCH_PRE_PRIMER),
        "dolch_primer": con_nivel(DOLCH_PRIMER),
      },
      "frases": FRASES,
    }
    texto = json.dumps(salida, ensure_ascii=False, indent=2).replace("\n", "\r\n")
    SALIDA.write_text(texto, encoding="utf-8", newline="")
    por_tipo = {}
    for r in rimas: por_tipo[r["tipo"]] = por_tipo.get(r["tipo"], 0) + 1
    por_niv = {}
    for r in rimas: por_niv[r["nivel_yle"]] = por_niv.get(r["nivel_yle"], 0) + 1
    print(f"{len(rimas)} rimas -> {SALIDA.name}  {por_tipo}  nivel: {por_niv}")

if __name__ == "__main__":
    main()
