# -*- coding: utf-8 -*-
"""Los 18 chants de patio (contar, palmas, comba) de Rhymes & chants, con musica.

La rima va INTACTA en el centro; la entrada y el cierre los cantan los personajes
de Starters (biblia cerrada: Freya, Nico, Astrid, Tomas, Pip y los companeros
Lia, Bruno, Aiko, Samu, Iris, Tino). Si Suno rechaza la rima tal cual, se usa
'letra_nis': misma metrica, otra letra (ver songs/README.md, copyright).

    python songs/chants-tradicionales.py      -> songs/chants-tradicionales.json
"""
import json, os

LEADER_CONTAR = ("playground counting-out chant for 7-year-olds, call and response, "
                 "handclaps and foot stomps, a cheerful girl leader voice and a small chorus "
                 "of children answering, spoken-sung, {bpm} BPM, bouncy bass and light marimba "
                 "under the voices, very clear consonants, fun and lively")
PALMAS = ("children's hand-clapping game song, two girls and a boy singing, crisp handclap "
          "patterns on every beat, {bpm} BPM, ukulele and bass, playful, call and response, "
          "very clear diction, schoolyard energy")
COMBA = ("jump-rope skipping rhyme for children, rope swish and slap on the beat, kids "
         "chanting together with a girl leader, {bpm} BPM, funky bass and snare, claps, "
         "very clear diction, joyful playground energy")

CHANTS = [
 # ---------------- COUNTING-OUT ----------------
 dict(id="eeny-meeny", estilo_v2='old-school hip-hop for kids, boom bap drums, vinyl scratches, a confident boy rapper leads and a kids crew answers, 90 BPM, deep bass, playful, very clear diction', titulo_nis='Who Is It?', letra_nis="""[Intro]
[Freya] Hello, friends! Who is it today? Let's count!

[Verse]
Nico, Freya, Astrid, Pip,
Round the circle, hop and skip.
Point your finger, round we go,
Who is it? We want to know!
One, two, three, it's not you,
Not you, not you, and not you!

[Break]
[Kids] Not you, Astrid! Not you, Tomás!

[Verse]
Nico, Freya, Astrid, Pip,
Round the circle, hop and skip.
Point your finger, round we go,
Who is it? We want to know!

[Outro]
[Freya] It's you, Nico!
[Nico] Oops!""", estilo=LEADER_CONTAR.format(bpm=96), personajes=["freya","nico","astrid","tomas"], escena="classroom",
  letra="""[Intro]
[Freya] Hello, friends! Who is it today? Let's count!

[Verse]
Eeny, meeny, miny, moe,
Catch a tiger by the toe.
If he hollers, let him go,
Eeny, meeny, miny, moe.
My mother told me to pick the very best one,
and you are not it!

[Break]
[Kids] Not you, Astrid! Not you, Tomás!

[Verse]
Eeny, meeny, miny, moe,
Catch a tiger by the toe.
If he hollers, let him go,
Eeny, meeny, miny, moe.

[Outro]
[Freya] It's you, Nico!
[Nico] Oops!"""),
 dict(id="one-potato", estilo_v2='sea shanty for children, accordion, fiddle and big foot stomps, a hearty adult male captain voice and a kids choir answering, 108 BPM, swinging 6/8 feel, very clear diction', titulo_nis='One Puffin, Two Puffin', letra_nis="""[Intro]
[Tomás] Fists in! Ready? Let's go!

[Verse]
One puffin, two puffins, on the rocks,
Three puffins, four puffins, in red socks!
Five puffins, six puffins, in the sea,
Seven puffins, eight puffins, look at me!

[Break]
[Kids] Count again! Count again!

[Verse]
One puffin, two puffins, on the rocks,
Three puffins, four puffins, in red socks!
Five puffins, six puffins, in the sea,
Seven puffins, eight puffins, look at me!

[Outro]
[Tomás] Eight! You're out, Freya!""", estilo=LEADER_CONTAR.format(bpm=100), personajes=["tomas","freya","nico","astrid"], escena="picnic-garden",
  letra="""[Intro]
[Tomás] Fists in! Ready? Let's go!

[Verse]
One potato, two potato, three potato, four,
Five potato, six potato, seven potato, more!

[Verse]
One potato, two potato, three potato, four,
Five potato, six potato, seven potato, more!

[Break]
[Kids] Count again! Count again!

[Verse]
One potato, two potato, three potato, four,
Five potato, six potato, seven potato, more!

[Outro]
[Tomás] More! You're out, Freya!"""),
 dict(id="ip-dip", estilo_v2="children's reggae, one-drop rhythm, offbeat guitar skank, warm bass, laid-back girl voice with kids echoing, 76 BPM, sunny and relaxed, very clear diction", estilo=LEADER_CONTAR.format(bpm=92), personajes=["astrid","lia","bruno","nico"], escena="track",
  letra="""[Intro]
[Astrid] Stand in a circle. One finger out!

[Verse]
Ip dip, sky blue,
Who's it? Not you!
[Kids] Not you, Lía!

Ip dip, sky blue,
Who's it? Not you!
[Kids] Not you, Bruno!

Ip dip, sky blue,
Who's it? Not you!
[Kids] Not you, Astrid!

[Outro]
[Astrid] Nico, you're it!
[Nico] Oops!"""),
 dict(id="bubble-gum", estilo_v2='1950s rock and roll doo-wop for kids, walking upright bass, piano boogie, handclaps, a girl lead with doo-wop backing kids, 150 BPM, bright and bouncy, very clear diction', titulo_nis='Cookies on a Plate', letra_nis="""[Intro]
[Freya] Yum, yum! Cookie time!

[Verse]
Cookies on a yellow plate,
Take some, Aiko! Don't be late!
[Aiko] Three!
[Kids] One, two, three!

[Verse]
Cookies on a yellow plate,
Take some, Samu! Don't be late!
[Samu] Five!
[Kids] One, two, three, four, five!

[Outro]
[Freya] Crunch! You're out!""", estilo=LEADER_CONTAR.format(bpm=98), personajes=["freya","aiko","samu"], escena="funfair",
  letra="""[Intro]
[Freya] Pop, pop! Bubble gum time!

[Verse]
Bubble gum, bubble gum, in a dish,
How many pieces do you wish?
[Aiko] Three!
[Kids] One, two, three!

[Verse]
Bubble gum, bubble gum, in a dish,
How many pieces do you wish?
[Samu] Five!
[Kids] One, two, three, four, five!

[Outro]
[Freya] Pop! You're out!"""),
 dict(id="engine-engine", estilo_v2='country hoedown train song for kids, chugging snare, banjo, fiddle, harmonica train whistle, a cowboy-style boy lead and kids shouting answers, 140 BPM, very clear diction', estilo=LEADER_CONTAR.format(bpm=104) + ", train whistle", personajes=["tomas","nico","iris"], escena="entrance",
  letra="""[Intro]
[Tomás] Choo choo! All aboard!

[Verse]
Engine, engine, number nine,
Going down Chicago line.
If the train should jump the track,
Do you want your money back?
[Nico] Yes!
[Kids] Y-E-S spells yes, and you are not it!

[Verse]
Engine, engine, number nine,
Going down Chicago line.
If the train should jump the track,
Do you want your money back?
[Iris] No!
[Kids] N-O spells no, and you are not it!

[Outro]
[Tomás] Choo choo!"""),
 dict(id="inky-pinky", estilo_v2='Andean huayno for children, charango, quena flute, bombo drum, a cheerful girl lead and kids chorus, 120 BPM, festive, very clear diction', estilo=LEADER_CONTAR.format(bpm=94), personajes=["nico","tino","freya"], escena="zoo",
  letra="""[Intro]
[Nico] Inky pinky! Say it with me!

[Verse]
Inky pinky ponky,
Daddy bought a donkey,
Donkey died, Daddy cried,
Inky pinky ponky.

[Verse]
Inky pinky ponky,
Daddy bought a donkey,
Donkey died, Daddy cried,
Inky pinky ponky.

[Outro]
[Kids] Ponky! Ponky! You're it, Tino!"""),
 dict(id="tinker-tailor", estilo_v2='school marching band, brass, glockenspiel and snare drum cadence, a bossy girl drum-major voice and kids chorus, 116 BPM, proud and bright, very clear diction', titulo_nis='Teacher, Doctor', letra_nis="""[Intro]
[Astrid] Count the buttons on your coat! What will you be?

[Verse]
Teacher, doctor, farmer, pilot,
Driver, dancer, singer, cook!

[Verse]
Teacher, doctor, farmer, pilot,
Driver, dancer, singer, cook!

[Break]
[Freya] One more time, Bruno!

[Verse]
Teacher, doctor, farmer, pilot,
Driver, dancer, singer, cook!

[Outro]
[Kids] Pilot! Bruno is a pilot!""", estilo=LEADER_CONTAR.format(bpm=96), personajes=["astrid","freya","bruno"], escena="library",
  letra="""[Intro]
[Astrid] Count the buttons on your coat!

[Verse]
Tinker, tailor, soldier, sailor,
Rich man, poor man, beggar man, thief.

[Verse]
Tinker, tailor, soldier, sailor,
Rich man, poor man, beggar man, thief.

[Break]
[Freya] One more time, Bruno!

[Verse]
Tinker, tailor, soldier, sailor,
Rich man, poor man, beggar man, thief.

[Outro]
[Kids] Sailor! Bruno is a sailor!"""),
 dict(id="fish-alive", estilo_v2='Caribbean calypso for kids, steel drums, shakers, congas, a smiling boy lead and kids chorus, 104 BPM, tropical seaside, very clear diction', estilo=LEADER_CONTAR.format(bpm=96) + ", ocean waves", personajes=["pip","freya","nico"], escena="mirador", solo_nis=True,
  letra="""[Intro]
[Freya] Where is Pip? He's at the sea!

[Verse]
One, two, three, four, five,
Pip the puffin takes a dive.
Six, seven, eight, nine, ten,
Up he comes with a fish again!

[Verse]
Why does Pip go down so deep?
Fish for dinner, then he'll sleep.
Which fish did Pip bring back?
A little silver one. Snap, snap, snap!

[Outro]
[Nico] Snap, snap! Good job, Pip!"""),
 dict(id="icka-bicka", estilo_v2='upbeat ska for children, offbeat guitar, trumpet and trombone stabs, fast hi-hats, a cheeky boy lead and kids shouting, 160 BPM, energetic, very clear diction', estilo=LEADER_CONTAR.format(bpm=100), personajes=["freya","samu","iris","nico"], escena="campus-hex",
  letra="""[Intro]
[Freya] Feet in the circle! Ready?

[Verse]
Icka bicka soda cracker,
Icka bicka boo.
Icka bicka soda cracker,
Out goes you!
[Kids] Bye, Samu!

[Verse]
Icka bicka soda cracker,
Icka bicka boo.
Icka bicka soda cracker,
Out goes you!
[Kids] Bye, Iris!

[Outro]
[Nico] Me? Oops!"""),
 dict(id="sky-blue", estilo_v2='gentle bossa nova for children, nylon guitar, soft brushes, light flute, a soft dreamy girl voice with kids humming, 88 BPM, calm and airy, very clear diction', estilo=LEADER_CONTAR.format(bpm=92), personajes=["astrid","aiko","tomas","freya"], escena="garden",
  letra="""[Intro]
[Astrid] Look up! What colour is the sky?

[Verse]
One, two, sky blue,
All out but you!
[Kids] Aiko!

One, two, sky blue,
All out but you!
[Kids] Tomás!

One, two, sky blue,
All out but you!
[Kids] Freya!

[Outro]
[Astrid] Blue, blue, sky blue!"""),
 # ---------------- CLAPPING ----------------
 dict(id="miss-mary-mack", estilo_v2='bubblegum K-pop for kids, bright synths, punchy claps, catchy hook, two girls and a boy trading lines, 124 BPM, sparkly and fun, very clear diction', titulo_nis='Little Pip, Pip, Pip', letra_nis="""[Intro]
[Freya] Clap with me, Astrid! Clap, clap!

[Verse 1]
Little Pip, Pip, Pip,
Went on a trip, trip, trip,
He took his hat, hat, hat,
And his yellow map, map, map.

[Verse 2]
He flew so far, far, far,
Over a car, car, car,
Over the school, school, school,
And the swimming pool, pool, pool.

[Verse 3]
He saw the moon, moon, moon,
He came back soon, soon, soon,
And he said hello, lo, lo,
To the kids below, low, low!

[Outro]
[Nico] Hello, Pip! Oops, he's gone!""", estilo=PALMAS.format(bpm=104), personajes=["freya","astrid","nico"], escena="amphitheater",
  letra="""[Intro]
[Freya] Clap with me, Astrid! Clap, clap!

[Verse 1]
Miss Mary Mack, Mack, Mack,
All dressed in black, black, black,
With silver buttons, buttons, buttons,
All down her back, back, back.

[Verse 2]
She asked her mother, mother, mother,
For fifty cents, cents, cents,
To see the elephants, elephants, elephants,
Jump over the fence, fence, fence.

[Verse 3]
They jumped so high, high, high,
They reached the sky, sky, sky,
And they didn't come back, back, back,
Till the Fourth of July, ly, ly.

[Outro]
[Nico] Elephants can't jump! Oops!"""),
 dict(id="sailor-went-to-sea", estilo_v2='surf rock for children, reverb twangy guitar, tom-tom drums, ocean waves, a boy and girl duet with kids shouting sea sea sea, 150 BPM, very clear diction', estilo=PALMAS.format(bpm=108) + ", ocean waves", personajes=["freya","nico","pip"], escena="mirador",
  letra="""[Intro]
[Freya] Look at the sea! Clap with me!

[Verse]
A sailor went to sea, sea, sea,
To see what he could see, see, see,
But all that he could see, see, see,
Was the bottom of the deep blue sea, sea, sea.

[Verse]
A sailor went to sea, sea, sea,
To see what he could see, see, see,
But all that he could see, see, see,
Was the bottom of the deep blue sea, sea, sea.

[Outro]
[Nico] And Pip! He saw Pip!"""),
 dict(id="pat-a-cake", estilo_v2='Italian tarantella for kids, mandolin, accordion, tambourine, getting faster and faster, a jolly boy lead and kids clapping, 130 BPM rising, very clear diction', titulo_nis='Roll the Pizza', letra_nis="""[Intro]
[Tomás] Let's make a pizza! Clap, clap!

[Verse]
Roll it, roll it, round and flat,
Make a pizza, just like that!
Cheese on top and tomatoes red,
Into the oven, Tomás said!

[Verse]
Roll it, roll it, round and flat,
Make a pizza, just like that!
Cheese on top and green beans too,
Pizza for Freya, and pizza for you!

[Outro]
[Freya] Mmm! Yummy pizza!""", estilo=PALMAS.format(bpm=100), personajes=["tomas","freya"], escena="lighthouse-kitchen",
  letra="""[Intro]
[Tomás] Let's make a cake! Clap, clap!

[Verse]
Pat-a-cake, pat-a-cake, baker's man,
Bake me a cake as fast as you can;
Pat it and prick it and mark it with B,
Put it in the oven for baby and me.

[Verse]
Pat-a-cake, pat-a-cake, baker's man,
Bake me a cake as fast as you can;
Pat it and prick it and mark it with T,
Put it in the oven for Tomás and me!

[Outro]
[Freya] Mmm! Yummy cake!"""),
 dict(id="double-double", estilo_v2='Peruvian cumbia for kids, guiro, timbales, electric guitar melody, two girls clapping and singing, 100 BPM, joyful dance groove, very clear diction', estilo=PALMAS.format(bpm=112), personajes=["astrid","bruno"], escena="chess-plaza",
  letra="""[Intro]
[Astrid] Double clap! Faster and faster!

[Verse]
Double, double, this, this,
Double, double, that, that,
Double this, double that,
Double, double, this, that.

[Verse]
Double, double, this, this,
Double, double, that, that,
Double this, double that,
Double, double, this, that.

[Outro]
[Bruno] Faster! This, that, this, that!"""),
 dict(id="down-down-baby", estilo_v2='Motown soul for children, tambourine, horn section, groovy bass, a girl lead with kids backing vocals, 108 BPM, warm and groovy, very clear diction', estilo=PALMAS.format(bpm=106), personajes=["freya","iris","tomas"], escena="funfair",
  letra="""[Intro]
[Iris] Freya, clap with me!

[Verse]
Down, down, baby, down by the roller coaster,
Sweet, sweet baby, I'll never let you go.
Shimmy, shimmy, cocoa pop, shimmy, shimmy, pow!
Shimmy, shimmy, cocoa pop, shimmy, shimmy, pow!

[Verse]
Down, down, baby, down by the roller coaster,
Sweet, sweet baby, I'll never let you go.
Shimmy, shimmy, cocoa pop, shimmy, shimmy, pow!
Shimmy, shimmy, cocoa pop, shimmy, shimmy, pow!

[Outro]
[Tomás] Pow!"""),
 # ---------------- SKIPPING ----------------
 dict(id="teddy-bear", estilo_v2='Afrobeat for kids, talking drum, shekere, bright guitar riffs, horns, a girl caller and kids response, 112 BPM, jumping energy, very clear diction', titulo_nis='Jump, Tomás, Jump', letra_nis="""[Intro]
[Freya] Turn the rope! Jump in, Tomás!

[Verse 1]
Jump, Tomás, jump, Tomás, clap your hands,
Jump, Tomás, jump, Tomás, now you stand,
Jump, Tomás, touch your nose,
Jump, Tomás, touch your toes.

[Verse 2]
Jump, Tomás, jump, Tomás, turn and spin,
Jump, Tomás, jump, Tomás, smile and grin,
Jump, Tomás, one, two, three,
Jump out now and come to me!

[Outro]
[Astrid] Well done, Tomás!""", estilo=COMBA.format(bpm=100), personajes=["freya","tomas","astrid"], escena="track",
  letra="""[Intro]
[Freya] Turn the rope! Jump in, Tomás!

[Verse 1]
Teddy bear, teddy bear, turn around,
Teddy bear, teddy bear, touch the ground,
Teddy bear, teddy bear, show your shoe,
Teddy bear, teddy bear, that will do.

[Verse 2]
Teddy bear, teddy bear, go upstairs,
Teddy bear, teddy bear, say your prayers,
Teddy bear, teddy bear, turn out the light,
Teddy bear, teddy bear, say good night!

[Outro]
[Astrid] Good night, Tomás!"""),
 dict(id="cinderella", estilo_v2='Brazilian samba batucada for children, surdo, tamborim, whistles, jungle animal sounds, a girl lead and kids chorus, 124 BPM, carnival fun, very clear diction', titulo_nis='Freya at the Zoo', letra_nis="""[Intro]
[Astrid] Jump in, Aiko! Ready, go!

[Verse]
Freya, Freya, at the zoo,
Saw a monkey and a kangaroo.
The monkey jumped and lost his shoe.
How many jumps can Aiko do?
[Kids] One, two, three, four, five, six, seven, eight, nine, ten!

[Outro]
[Nico] Ten jumps! Wow!""", estilo=COMBA.format(bpm=104), personajes=["astrid","aiko","nico"], escena="hockey",
  letra="""[Intro]
[Astrid] Jump in, Aiko! Ready, go!

[Verse]
Cinderella, dressed in yella,
Went upstairs to kiss a fella.
Made a mistake and kissed a snake.
How many doctors did it take?
[Kids] One, two, three, four, five, six, seven, eight, nine, ten!

[Outro]
[Nico] Ten doctors! Oops!"""),
 dict(id="i-like-coffee", estilo_v2='electro swing for kids, swing brass, upright bass, four-on-the-floor beat, a jazzy boy lead and kids chorus, 122 BPM, playful, very clear diction', titulo_nis='Apple, Orange, Pear', letra_nis="""[Intro]
[Freya] Jump with me! Who's next?

[Verse]
Apple, apple, orange, pear,
Jump in, Tomás, if you dare!

Apple, apple, orange, pear,
Jump in, Astrid, with your hair!

Apple, apple, orange, pear,
Jump in, Nico, over there!

[Outro]
[Nico] Jump, jump! Oops!""", estilo=COMBA.format(bpm=98), personajes=["freya","tomas","astrid","nico"], escena="track",
  letra="""[Intro]
[Freya] Jump with me! Who's next?

[Verse]
I like coffee, I like tea,
I like Tomás to jump with me!

I like coffee, I like tea,
I like Astrid to jump with me!

I like coffee, I like tea,
I like Nico to jump with me!

[Outro]
[Nico] Jump, jump! Oops!"""),
]

if __name__ == "__main__":
    aqui = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(aqui, "chants-tradicionales.json")
    json.dump({"_nota": __doc__.strip().splitlines()[0], "chants": CHANTS}, open(out, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(len(CHANTS), "->", out)
