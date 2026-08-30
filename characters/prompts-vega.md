# Mr Vega — la hoja 3D que falta

Mr Vega es el **guía adulto** del reparto de Flyers: el hueco que Cambridge cubre
con Mr Jones (transporte y lugares) y que hasta el 29-ago-2026 tapaba Diego, que
es alumno.

**Hoy funciona sin arte propio.** Usa la figura del banco `assets/vocab/father.png`,
que es como la biblia dibuja a los adultos del pueblo desde el principio (Pedro el
taxista, los tíos, los abuelos). Con eso sale en las láminas de *label_people* — 18
de las 55 — y el reparto queda completo.

**Lo que no puede hacer sin hoja propia:** posar. Una figura del banco solo está de
pie, así que Vega no entra en las tareas que piden una acción (`pose`), ni puede
señalar el camino, que es justo su función. Para eso hace falta esta hoja.

---

## El prompt

Sigue el prompt maestro de [bible.md](bible.md), con su ficha puesta. Se genera con
una imagen de referencia adjunta — usa `assets/characters/flyers/diego/pose-01.png`,
que fija el estilo — y **una sola hoja** con las nueve poses.

> Use ONLY the character described below. Do NOT invent a new character, do NOT change
> the face, the hair or the clothes, and do NOT add other people to the image.
> This is an existing character from our school's own English course (our own IP), and
> the attached image is the approved reference for the style.
>
> **Mr Vega**, 45 years old, the school caretaker. Hair: short dark brown with grey at
> the temples `#4A3728`. Skin: `#C98E5A`. Wearing a navy blue work polo shirt
> `#2F5D9E`, grey work trousers `#6B7686`, brown boots, a navy cap and a bunch of keys
> clipped to his belt.
> 3D cartoon style, full body, transparent background, big head, big friendly eyes,
> soft rounded shapes, ADULT proportions — clearly taller than the children in the
> reference, but the same drawing style.
> Lay the SAME character out on a 3x3 grid on a plain white background, one pose per
> cell, in this order:
> waving · pointing the way · talking · thinking · surprised · sitting ·
> walking · holding a box · giving a thumbs up.

## Después de generar

```bash
python tools/cut_3d_sheet.py hoja-vega.jpg 3 3 \
  vega-01 vega-02 vega-03 vega-04 vega-05 vega-06 vega-07 vega-08 vega-10
```

El script corta la rejilla, recorta cada figura a su contenido y quita el blanco.
Las salidas van a `assets/vocab/`, así que hay que moverlas a
`assets/characters/flyers/vega/pose-NN.png` con los nombres de la tabla de poses.

Luego, en `content/cast-flyers.json`:

- borrar `"figura": "father"` de la ficha de `vega`,
- poner sus `poses` reales,
- y regenerar: `python tools/gen_visual_flyers.py --rehacer label_people`

La auditoría avisa si alguna pose declarada no está en disco, así que no hace falta
comprobarlo a mano: `python tools/check_visual_flyers.py`.

## Por qué la cara importa aquí más que en otros

`father.png` la comparten Juan, Tom, Leo y Pedro, que salen en los **textos** del
curso. Vega sale en las **láminas**, donde el alumno tiene que distinguir a quién
señala el audio. Mientras solo esté de pie y la pista sea «the man in the blue
shirt» no hay confusión, porque es el único adulto de la escena. En cuanto haya dos
adultos en una lámina, esto deja de bastar.
