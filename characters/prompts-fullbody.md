# Regenerar los `fullbody.png`

El `fullbody.png` es la figura de cuerpo entero que usan la **portada de cada nivel**
(`engine/banner.js`) y los videos de Veo. La portada los pinta a 200 px CSS, que en una
pantalla retina son **400 px reales**, y para los videos hacen falta más todavía. Por eso
el mínimo sano es **800 px de alto**.

## Lo que hay que rehacer y por qué

| Personaje | Nivel | `fullbody.png` hoy | Qué pasa |
|---|---|---|---|
| freya | starters | 180×339 | se escala al doble en la portada: se ve blando |
| nico | starters | 184×344 | igual |
| astrid | starters | 182×340 | igual |
| tomas | starters | 180×340 | igual |
| mateo | movers | 179×340 | igual |
| **pip** | starters | **no existe** | la portada cae a `pose-01.png` (248×279) |
| **luna** | movers | **no existe** | cae a `pose-01.png` (265×305) |
| **kili** | flyers | **no existe** | cae a `pose-01.png` (734×619) — el único que aguanta |

El resto del elenco ya está bien (erik 704, sofía 641, valentina 744, ingrid 721, diego 644,
oliver 691, maya 430) y **no se toca**.

> Nota: en Starters, Mateo, Pip y Luna **todas** las poses están a ~340 px, no solo el
> fullbody: esa tanda entera se recortó pequeña. Las poses se ven a menos tamaño dentro de
> las unidades, así que no corre prisa; si algún día se rehacen, valen los mismos prompts
> cambiando la línea de la pose.

## Cómo se pide (esto es lo que hace que salga usable)

1. **Adjuntar siempre la referencia** del propio personaje (columna de abajo). Sin ella
   vuelve otro niño distinto — es la regla de oro de [bible.md](bible.md). La referencia es
   de baja resolución a propósito: sirve para la identidad, no para la calidad.
2. **Fondo blanco liso y sin sombra en el suelo.** La sombra proyectada se pega al recorte y
   deja un halo gris alrededor de los pies, que en la portada se ve contra el mar.
3. **Cuerpo entero, de pie, de frente y saludando** (pose 01): es la que usa la portada.
4. **Un solo personaje**, sin objetos, sin texto y sin marco.
5. **Encuadre vertical**, la figura de la cabeza a los pies con un margen pequeño y parejo:
   así todos quedan a la misma escala cuando el CSS los iguala.
6. **Bajar la imagen a tamaño completo** ("Descargar imagen a tamaño completo"). Copiar al
   portapapeles da 1024 px y con eso la figura se queda en ~900, justo pero válido; si
   Chrome bloquea la segunda descarga seguida, está `python tools/recibe_imagen.py`.

---

## Los ocho prompts

Cada uno se pega tal cual, adjuntando la referencia indicada.

### freya — starters · referencia: `assets/characters/starters/freya/fullbody.png`

> Use ONLY the character described below. Do NOT invent a new character, do NOT change the
> face, the hair or the clothes, and do NOT add other people to the image. This is an
> existing character from our school's own English course (our own IP); the attached image
> is the approved reference for identity and style — it is low-resolution, so keep the
> identity and render it sharp.
>
> **FREYA, a 7-year-old girl.** Hair: blonde, two long braids and a soft fringe. Skin: fair.
> Wearing a light blue short-sleeved t-shirt, blue jeans and white sneakers.
>
> 3D cartoon style, same proportions as the reference: big head (about 40% of total height),
> large friendly eyes, soft rounded shapes, soft studio lighting with a gentle rim light.
> Full body from head to feet, standing, facing the viewer, one hand raised waving, smiling.
> Plain pure white background. No shadow on the ground, no floor, no props, no text, no
> border. Vertical framing, the character fills the frame with a small even margin.
> High resolution, sharp details.

### nico — starters · referencia: `assets/characters/starters/nico/fullbody.png`

> *(mismo encabezado y mismo cierre que Freya, cambiando solo la ficha)*
>
> **NICO, a 7-year-old boy.** Hair: black, short and spiky. Skin: light brown.
> Wearing a red short-sleeved t-shirt, blue jeans and white and grey sneakers.

### astrid — starters · referencia: `assets/characters/starters/astrid/fullbody.png`

> **ASTRID, an 8-year-old girl.** Hair: brown, straight, shoulder length, with a fringe.
> Skin: fair. Wearing a green short-sleeved t-shirt, grey trousers and white sneakers with
> green details.

### tomas — starters · referencia: `assets/characters/starters/tomas/fullbody.png`

> **TOMÁS, a 7-year-old boy.** Hair: black, short. Skin: light brown. Wearing a yellow
> short-sleeved t-shirt, blue shorts and blue and white sneakers.

### mateo — movers · referencia: `assets/characters/movers/mateo/fullbody.png`

> **MATEO, a 9-year-old boy.** Hair: black, short with a side parting. Skin: fair. Wearing a
> green short-sleeved t-shirt, blue jeans and grey sneakers.

### pip — starters (mascota) · referencia: `assets/characters/starters/pip/pose-01.png`

> Use ONLY the character described below. Do NOT invent a new character and do NOT change
> the colours or the shape of the beak. This is an existing mascot from our school's own
> English course (our own IP); the attached image is the approved reference for identity and
> style — it is low-resolution, so keep the identity and render it sharp.
>
> **PIP, a young Atlantic puffin**, the shy mascot of the course. Dark slate-blue almost
> black back and wings, white chest and white face, grey eye patch, big orange beak with
> darker stripes, orange feet.
>
> 3D cartoon style, same proportions as the reference: chubby rounded body, big friendly
> eyes, soft studio lighting with a gentle rim light. Full body, standing on both feet,
> facing the viewer, one wing raised waving, gentle smile. Plain pure white background. No
> shadow on the ground, no floor, no props, no text, no border. Vertical framing, the
> character fills the frame with a small even margin. High resolution, sharp details.

### luna — movers (mascota) · referencia: `assets/characters/movers/luna/pose-01.png`

> *(mismo encabezado y cierre que Pip)*
>
> **LUNA, a Siberian husky puppy**, the loyal mascot of the course. Grey and white coat with
> the typical husky face mask, light blue eyes, thick curled fluffy tail, pink nose.
> Standing on all four legs with one front paw raised waving, friendly open-mouth smile.

### kili — flyers (mascota) · referencia: `assets/characters/flyers/kili/pose-01.png`

> *(mismo encabezado y cierre que Pip)*
>
> **KILI, a young Andean condor**, the postman mascot of the course: solemn but clumsy.
> Black plumage, white feather collar around the neck, reddish-brown bare head and face with
> a small crest, hooked beak. Standing on both feet, facing the viewer, wings half open as if
> waving, friendly expression.

---

## Qué hacer con la imagen

```bash
python tools/recorta_fullbody.py <descarga.jpg> <nivel> <slug> --mira
```

Quita el fondo blanco desde fuera hacia dentro (el blanco de los ojos o de unas zapatillas
se queda, porque no toca el borde), recorta al contenido, avisa si viene con menos de 800 px
de alto y no escribe nada con `--mira`. Sin esa opción, guarda en
`assets/characters/<nivel>/<slug>/fullbody.png`.

Después:

```bash
python tools/check_elenco.py
```

Y para publicar, el flujo de siempre: commit y push en `nis-fun`, copiar los PNG a
`C:\Projects\nis-portal\nis-fun\assets\characters\...` (con `git pull` antes: otra sesión
trabaja en ese clon), commit y push en `nis-portal`, y en el servidor
`cd /opt/nis-portal && git pull --ff-only origin main`.

Los PNG no llevan `?v=`, así que si un navegador ya tiene el viejo en caché puede tardar en
verse; el `index.html` va con `no-cache`, de modo que basta con recargar.
