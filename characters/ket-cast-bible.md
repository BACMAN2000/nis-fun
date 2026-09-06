# Fun for Nordic · Cambridge KET (A2) — Teen Cast Bible

The A2 course reuses the Fun for Nordic engine but needs an **older, teen cast** (the primary cast — Pip, Luna, Kili, the young explorers — is for children). These are secondary students at **Nordic International School (Peru)**, around **11–12 years old**, in the world of the **"Inspiring Nordic — Trades"** project. Style: **clean flat coursebook illustration** (like Compact Key for Schools), friendly, modern, diverse; consistent character design across poses. Full body, plain/transparent background for the sheet.

## Master style prompt (for AI generation)
> Flat vector-style illustration for a teen English coursebook (A2 / Cambridge Key). A single character, full body, friendly and modern, clean bold outlines, soft cel shading, simple shapes, no background (transparent or plain white). Realistic teen proportions (about 11–12 years old, NOT a small child, NOT an adult). Coherent, warm colour palette. Neutral standing pose looking slightly to the right. High quality, centred, whole body visible with room around it.

## The four students
- **mateo** — boy, 12. Warm brown skin, short dark-brown wavy hair, friendly round face, small eyebrows. Wears a **navy hoodie**, jeans, trainers. Personality: curious, kind, a builder and chess player; the "narrator" of several blog texts. Often carries a small wooden box or a chess piece.
- **sofia** — girl, 12. Light-brown skin, long dark straight hair (sometimes a plait), a little shy but warm smile. Wears a **mustard-yellow jumper** and a skirt or jeans, carries a **book** (she's the reader; Charlotte's Web / Matilda). Personality: thoughtful, loves stories and writing.
- **liam** — boy, 11. Fair skin, short curly fair/light-brown hair, energetic open smile, freckles. Wears an **orange-and-white football/sports top**, shorts or joggers, trainers; often with a **football**. Personality: sporty, sociable, international family.
- **nadia** — girl, 12. Medium-brown skin, curly dark hair, **round glasses**. Wears a **teal/green shirt** with a paint-splash or art-club badge, holds a **pencil/sketchbook**. Personality: artistic, designs the project posters.

## The guide
- **nova** — a friendly older-student/mentor guide (not a childish mascot). Neutral, warm, encouraging. Currently a simple purple placeholder avatar (graduation cap) at `assets/characters/ket/nova/pose-01|03|10.svg`. Redesign as a teen-appropriate guide (a slightly older student or a small modern robot/star companion — "Nova"), in the course accent colour **#6d5bd0 (indigo/violet)**.

## Where the art goes (engine)
`assets/characters/ket/<slug>/pose-NN.png` — the engine's `CHAR(slug,pose)` builds this path (falls back .png → .svg). Minimum useful set for the coursebook: **pose-01** (neutral standing, used in scene + as byline avatar in the `reading` card), optionally pose-03 (talking, for the guide bubble) and pose-10 (celebration). A clean **portrait/half-body per student** is the priority (for reading bylines and the unit scene). Keep the same face/outfit across all poses of the same character.

## Integration plan
1. Generate one clean full-body + one portrait per student (mateo, sofia, liam, nadia) and refresh nova.
2. Save as pose PNGs under `assets/characters/ket/<slug>/`.
3. Show the author's avatar next to the `reading` byline (each unit's reading names an author: U1 Miss Vega's class, U2 Mateo, U3 Liam, U4 Nadia, U5 Sofía, U6 Mateo), and feature the cast in the unit `scene`.

See [[nis-fun-biblia-personajes]] (primary cast rules), [[nis-yle-upgrade-ruta-2026]] (Gemini download gotchas: use the "Desktop at home" Chrome that saves without a dialog).
