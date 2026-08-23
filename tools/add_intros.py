# -*- coding: utf-8 -*-
"""Textos de apertura personalizados (originales) para las unidades 1-3 de cada nivel."""
import json, os

ROOT = os.path.join(os.path.dirname(__file__), "..")
INTROS = {
    "content/flyers/unit-01.json":
        "It is the first morning of the Aurora Expedition, and the lighthouse kitchen is full of open suitcases! Ingrid checks her list twice: uniform for the school photo, gloves and a scarf for the cold sea wind, and a secret pocket for the expedition money. Kili flies from room to room carrying socks in his beak — some of them are even the right ones. What do explorers wear, and what do they carry? Open your eyes: this unit is all about it!",
    "content/flyers/unit-02.json":
        "Reporter Diego has a new mission: to make a map of every amazing place in town! On Saturday he follows Maya with his microphone — to the museum with the dinosaur bones, to the old bridge over the green river, and to the theatre where a dragon appears on the stage. Some places are noisy, some are quiet, and one of them hides the best ice cream in the city. Where do YOU go at the weekend? Let's find out how to talk about it!",
    "content/flyers/unit-03.json":
        "Ten minutes before the big concert, Oliver runs into the hall shouting: 'I've forgotten my guitar!' Ingrid has already checked the lights, Maya has just found a lucky coin, and the drummer hasn't arrived yet. Everything happens at the same time — and that is exactly what this unit is about: things that have JUST happened, things we have ALREADY done, and things that haven't happened YET. Take a deep breath, explorer: the show is about to begin!",
    "content/movers/unit-01.json":
        "The gates of the zoo open at nine, and the Fjord Club is first in line! Valentina wants to see the pandas eating their breakfast of bamboo, Erik brings a notebook to draw every animal, and Sofia has the map with all the paths. Which animal is bigger, a whale or a dolphin? Which one jumps higher, a kangaroo or a frog? Today we compare them all — and Luna waits at home, dreaming of a very big bone.",
    "content/movers/unit-02.json":
        "Erik's newest invention is a weather machine made from an umbrella, two spoons and a bicycle bell. Does it work? Nobody knows! But this Saturday the Club really needs it, because there is a picnic planned by the fjord. Will it be sunny or rainy? Should they take the kite or the board games? In this unit you will learn to talk about every kind of weather — and maybe, like Sofia, you will see a rainbow with both ends in the water.",
    "content/movers/unit-03.json":
        "Yesterday the funfair came to town, with its big wheel, its ring game and its mountain of popcorn! The Fjord Club went at ten o'clock and stayed all day. Mateo lost his ticket TWO times, Erik won a little green dragon, and everyone screamed on the big wheel. Today they can't stop talking about it — in the past! Went, saw, ate, rode, won: these are the words of a great story. Come and hear it!",
    "content/starters/unit-01.json":
        "Freya opens her big toy box and — surprise! — everything falls on the floor: a red ball, a yellow kite, three little cars and one sleepy puffin called Pip. Now it is time to put everything back, and that is a game too! Say the name of each toy, say its colour, and count them with Freya. How many toys can YOU find in this unit? Open the box and let's play!",
    "content/starters/unit-02.json":
        "Nico brings a special photo to school today: his family photo! Look — his mother Rosa with her big smile, his father Juan who is very tall, his little sister, and the baby cousin who is only one. But wait… who is that little black and white bird next to grandma? PIP! He flew into the photo! Who is in YOUR family? In this unit you will learn to say it in English.",
    "content/starters/unit-03.json":
        "Today the Explorers visit the zoo, and Tomás is running from one animal to the next! The monkeys are jumping, the big grey elephant is eating a banana, and the lion is sleeping — shhh! Pip flies up high to say hello to the zoo birds, because birds understand birds. Can you say the names of all the animals? Can you make their sounds? Woof, meow, roar… let's go in!",
}

for path, intro in INTROS.items():
    full = os.path.join(ROOT, path)
    ud = json.load(open(full, encoding="utf8"))
    ud["scene"]["intro"] = intro
    json.dump(ud, open(full, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("9 intros personalizadas")
