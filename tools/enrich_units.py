# -*- coding: utf-8 -*-
"""Enriquece las unidades 1-3 de cada nivel con los tipos nuevos
(gap_text, spot_diff, match con distractor), con contenido original."""
import json, os

ROOT = os.path.join(os.path.dirname(__file__), "..")

def load(p): return json.load(open(os.path.join(ROOT, p), encoding="utf8"))
def save(p, d): json.dump(d, open(os.path.join(ROOT, p), "w", encoding="utf8"), ensure_ascii=False, indent=2)

def insert_before_E(ud, acts):
    idx = next(i for i, a in enumerate(ud["activities"]) if a["code"] == "E")
    for j, a in enumerate(acts):
        ud["activities"].insert(idx + j, a)

def GT(code, title, box, text, answers):
    return {"code": code, "type": "gap_text", "title": title,
            "outputs": ["book", "digital", "quiz"],
            "data": {"box": box, "text": text, "answers": answers}}

def SD(code, title, A, B, diffs):
    return {"code": code, "type": "spot_diff", "title": title,
            "outputs": ["book", "digital"],
            "data": {"sceneA": A, "sceneB": B, "diffs": diffs}}

def QA(code, title, pairs, extra):
    return {"code": code, "type": "match_words", "title": title,
            "outputs": ["book", "digital", "quiz"],
            "data": {"left_label": "Question", "right_label": "Answer",
                     "pairs": pairs, "extra": extra}}

# ---------- FLYERS 1 ----------
p = "content/flyers/unit-01.json"; ud = load(p)
for a in ud["activities"]:
    if a["code"] == "D":
        a["data"]["items"] = [
            {"sentence": "You wear this soft, long thing round your neck when the weather is cold and windy.", "options": ["a belt", "a scarf", "a pocket"], "answer": 1},
            {"sentence": "People carry their clothes and other things in this when they travel to another city.", "options": ["a suitcase", "a uniform", "a ring"], "answer": 0},
            {"sentence": "You can wear this round thing on your head on a hot and sunny day at the beach.", "options": ["gloves", "a sunhat", "an umbrella"], "answer": 1},
            {"sentence": "You put these on your feet before your shoes, and they keep your feet warm in winter.", "options": ["socks", "belts", "scarves"], "answer": 0},
            {"sentence": "Some people wear this small, pretty thing on a finger. It is sometimes made of gold.", "options": ["a pocket", "a sock", "a ring"], "answer": 2}]
insert_before_E(ud, [
    GT("F", "Read the story about the picture. Write the missing words.",
       ["suitcase", "gloves", "uniform", "pocket", "scarf", "umbrella", "boots", "ring"],
       "Ingrid is packing for the expedition. First she puts her blue {1} at the bottom, because the school photo is on Monday. Then she packs her warm {2} and her thick {3} for the cold days on the boat. Her money is safe in the small {4} of her rucksack. She is not taking her {5} because it is too big — her yellow coat is better for the rain. At the end, her {6} is so full that Kili has to sit on it to close it!",
       ["uniform", "scarf", "gloves", "pocket", "umbrella", "suitcase"]),
    SD("G", "Look and find the differences in the clothes shop.",
       [["🧥", "👒", "🧤", "👗", "🧣"], ["👟", "🎩", "🧦", "👕", "👖"], ["🧳", "💍", "🥾", "🧢", "☂️"]],
       [["🧥", "👜", "🧤", "👗", "🧣"], ["👟", "🎩", "🧦", "🥼", "👖"], ["🎒", "💍", "🥾", "🧢", "🕶️"]],
       [[0, 1], [1, 3], [2, 0], [2, 4]])])
save(p, ud)

# ---------- FLYERS 2 ----------
p = "content/flyers/unit-02.json"; ud = load(p)
insert_before_E(ud, [
    QA("F", "Find the answer to each question. Careful — one answer is extra!",
       [{"left": "How do you travel to school every morning?", "right": "By tram, but I walk when it's sunny."},
        {"left": "What do you do when you go to the funfair?", "right": "I ride the big wheel three times!"},
        {"left": "Where do you buy medicine in your town?", "right": "At the chemist's next to the bank."},
        {"left": "What did you see at the museum last week?", "right": "Very old coins and a gold crown."},
        {"left": "Who do you sit with at the stadium?", "right": "With my dad and my little sister."},
        {"left": "When does the theatre open in the evening?", "right": "At half past six, one hour before the play."}],
       ["It's made of wood and glass."]),
    GT("G", "Read about Maya's weekend. Write the missing words.",
       ["museum", "bones", "bridge", "dragon", "stadium", "three", "funfair", "tickets"],
       "On Saturday morning, Maya and her aunt visited the city {1}, where they saw dinosaur {2} that are eighty million years old. At midday they ate rice and fish at a little restaurant next to the old stone {3}. In the afternoon they watched a play about a friendly {4} at the theatre. On Sunday, the whole family went to the {5} to watch the cousin's football match. After the game, they celebrated with the biggest ice creams in town — Maya chose {6} flavours: chocolate, lemon and mango!",
       ["museum", "bones", "bridge", "dragon", "stadium", "three"])])
save(p, ud)

# ---------- FLYERS 3 ----------
p = "content/flyers/unit-03.json"; ud = load(p)
insert_before_E(ud, [
    GT("F", "Read about the concert. Write just, already, yet or a participle.",
       ["already", "just", "yet", "forgotten", "broken", "found", "never", "ever"],
       "Oliver has {1} arrived at the concert hall — he is still breathing fast from running! He has {2} his guitar at home, so Kili is flying there to bring it. Ingrid has {3} checked the lights and the microphones twice. The drummer hasn't arrived {4}, but his drums are waiting on the stage. Maya has {5} a lucky coin under the stage and she says it is a good sign. Five minutes later, Kili lands with the guitar — nothing is {6}, and the show can begin!",
       ["just", "forgotten", "already", "yet", "found", "broken"]),
    SD("G", "Look at the concert stage. Find the differences!",
       [["🎤", "🎸", "🥁", "🎹", "🎺"], ["🎵", "🎶", "🎼", "🎧", "📻"], ["🌟", "🎫", "👏", "🎪", "💡"]],
       [["🎤", "🎸", "🪕", "🎹", "🎺"], ["🎵", "🎶", "🎼", "🎧", "🔔"], ["🌙", "🎫", "👏", "🎭", "💡"]],
       [[0, 2], [1, 4], [2, 0], [2, 3]])])
save(p, ud)

# ---------- MOVERS 1 ----------
p = "content/movers/unit-01.json"; ud = load(p)
insert_before_E(ud, [
    SD("F", "Two pictures of the zoo. Find the differences!",
       [["🐼", "🦁", "🐧", "🐬", "🦘"], ["🌴", "🌳", "🍃", "🪨", "🌿"], ["🐍", "🦜", "🐒", "🐢", "🦩"]],
       [["🐼", "🐯", "🐧", "🐬", "🦘"], ["🌴", "🌳", "🍌", "🪨", "🌿"], ["🐊", "🦜", "🐒", "🐢", "🦚"]],
       [[0, 1], [1, 2], [2, 0], [2, 4]]),
    GT("G", "Read about the trip. Write the missing words.",
       ["pandas", "dolphins", "penguins", "bamboo", "bone", "zoo", "cats"],
       "Last Saturday the Fjord Club went to the {1}. First they saw the {2} — they were eating green {3} all the time! Then they watched the {4} jump higher than the fence. The {5} were swimming in very cold blue water. At home, Luna got a big {6} because she waited all day like a very good dog.",
       ["zoo", "pandas", "bamboo", "dolphins", "penguins", "bone"])])
save(p, ud)

# ---------- MOVERS 2 ----------
p = "content/movers/unit-02.json"; ud = load(p)
insert_before_E(ud, [
    GT("F", "Read Sofía's postcard. Write the missing words.",
       ["rainy", "sunny", "kite", "chocolate", "rainbow", "picnic", "snowy"],
       "Dear Grandma, Saturday was a crazy weather day! In the morning it was {1}, so we played board games at Erik's house. After lunch the sky changed: it was {2} and windy — perfect for my new orange {3}! We had our {4} by the fjord and Erik brought hot {5} because it was a bit cold. Best of all, after the rain we saw a huge {6} over the water. Love, Sofía.",
       ["rainy", "sunny", "kite", "picnic", "chocolate", "rainbow"])])
save(p, ud)

# ---------- MOVERS 3 ----------
p = "content/movers/unit-03.json"; ud = load(p)
insert_before_E(ud, [
    QA("F", "Match each question with its answer. One answer is extra!",
       [{"left": "What time did you go to the funfair?", "right": "At ten o'clock in the morning."},
        {"left": "Who lost his ticket in the bus?", "right": "Mateo — but the driver found it!"},
        {"left": "What did Erik win at the ring game?", "right": "A little green dragon."},
        {"left": "What did you eat at the funfair?", "right": "Popcorn and a big red ice cream."},
        {"left": "How many times did you ride the big wheel?", "right": "Three times — it was very high!"},
        {"left": "Why was everyone laughing at the door?", "right": "Because the ticket was in Mateo's pocket!"}],
       ["It's next to the police station."])])
save(p, ud)

# ---------- STARTERS 1 ----------
p = "content/starters/unit-01.json"; ud = load(p)
insert_before_E(ud, [
    SD("F", "Two toy boxes! Find the differences.",
       [["⚽", "🧸", "🚗", "🪁"], ["🎲", "🪆", "🚂", "🎈"], ["🖍️", "📚", "🥁", "🤖"]],
       [["🏀", "🧸", "🚗", "🪁"], ["🎲", "🪆", "🚂", "🎁"], ["🖍️", "📚", "🎺", "🤖"]],
       [[0, 0], [1, 3], [2, 2]])])
save(p, ud)

# ---------- STARTERS 2 ----------
p = "content/starters/unit-02.json"; ud = load(p)
insert_before_E(ud, [
    GT("F", "Read about the photo. Write the missing words.",
       ["mother", "father", "sister", "baby", "dog"],
       "This is my family photo! My {1} is Rosa and my {2} is Juan. My little {3} is five years old. The {4} is my cousin — he is one!",
       ["mother", "father", "sister", "baby"])])
save(p, ud)

# ---------- STARTERS 3 ----------
p = "content/starters/unit-03.json"; ud = load(p)
insert_before_E(ud, [
    SD("F", "Two pictures of the zoo! Find the differences.",
       [["🦁", "🐵", "🐘", "🦒"], ["🌴", "🌵", "🍃", "🪨"], ["🦆", "🐟", "🐢", "🦜"]],
       [["🦁", "🐻", "🐘", "🦒"], ["🌳", "🌵", "🍃", "🪨"], ["🦆", "🐟", "🐢", "🐧"]],
       [[0, 1], [1, 0], [2, 3]])])
save(p, ud)

print("9 unidades enriquecidas")
