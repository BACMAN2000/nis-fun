# Escenarios del colegio — prompts de ilustración (cartoon original)

Ilustraciones ORIGINALES estilo cartoon del campus de Nordic International School,
para libros y app. Las fotos de referencia están en el catálogo de la sesión del
23-ago (sitio oficial nordic-school.edu.pe). NUNCA se insertan las fotos: solo las
ilustraciones generadas. Instalar como `assets/scenes/<slug>.png` (fondo blanco,
recortar con tools/segment_sheet.py si sale con márgenes).

Prompt base (anteponer a cada uno):
> Cheerful children's book illustration, bright flat cartoon style with soft
> outlines, for a kids English course. Friendly, warm, colorful, no people,
> no text, no labels. Wide landscape composition on white background.

| slug | Escena | Detalle del prompt |
|------|--------|--------------------|
| main-building | Edificio principal (aéreo) | A modern circular school building formed by a ring of tall slim white columns, with hexagonal cream-and-orange classroom pavilions inside the ring, seen from above at an angle; green gardens around, tiny trees, sunny sky with soft clouds and a small condor flying. |
| facade | Fachada circular | Front view of a round modern school building: a tall open ring of thin white columns like a crown, glass doors at the base, bushes and a green lawn in front, blue sky. |
| entrance | Entrada | A modern school entrance: low wide concrete building with warm wooden doors, a clean sign area on the wall (blank, no letters), a little path with plants, morning light. |
| campus-hex | Campus hexagonal | Aerial view of a school campus with clustered hexagonal pavilions with skylights, connected paths, round gardens and a little labyrinth of green hedges. |
| amphitheater | Anfiteatro | A small round outdoor stone amphitheater with curved steps for children, next to a circular building of white columns, plants around, soft afternoon sky. |
| library | Biblioteca | Cozy modern school library interior with two floors of warm wooden shelves full of colorful books, round reading rugs, little tree-shaped decorations, big windows with daylight. |
| garden | Huerto escolar | A cheerful school vegetable garden with little green rows of plants, small wooden signs (blank), a watering can, butterflies and a big leafy tree behind. |

## Integración al terminar
- Portada de niveles del engine: banner con `main-building` detrás de las tarjetas.
- Portadas de los 3 libros (book-builder cover): `facade` bajo el título.
- Openers temáticos: unidades de school → `library`/`entrance`; places/town → `facade`;
  countryside/garden → `garden`; celebración final → `amphitheater`.
- El panel `.op-art` de emoji puede reemplazarse por la escena cuando exista.
