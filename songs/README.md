# Canciones y chants por unidad

Dos piezas por unidad, sacadas del **vocabulario y la gramática de esa unidad**:
un **chant** (drill rítmico, call-and-response) y una **canción** (la misma
gramática dentro de una historia).

    piloto.json     la letra y el prompt de estilo de cada pieza
    audio/          los mp3 aprobados

## Cómo se hace una pieza

1. Escribir la letra en `piloto.json`, con su `estilo` (BPM, instrumentos,
   voces, idioma).
2. En Suno, modo **Advanced**: la letra en *Lyrics*, el estilo en *Styles*.
3. Generar **una sola vez** — cada Create da dos versiones. Comprobar la
   lista antes y después de pulsar; el CAPTCHA de Cloudflare puede aparecer
   encima y hacer creer que no se envió, cuando sí.
4. El usuario marca con el pulgar la versión buena. **Ese paso no lo puede
   hacer quien no oye el audio**, y es el que decide.
5. Descargar la marcada: menú «…» → Download → MP3 Audio.

## Trampas ya pisadas

- **El editor de letra solo acepta un evento `paste` de verdad.** Escribir
  con teclado simulado o `execCommand` no entra.
- **`Ctrl+A` en el campo de estilo deja una «a» pegada al principio**
  (`aupbeat children's…`) y esa «a» viaja al prompt. Borrarla con
  `Ctrl+Home` + `Supr`.
- **Chrome bloquea la segunda descarga seguida del mismo sitio**, en
  silencio. Hay que permitirlo en el icono de la barra de direcciones, y aun
  así conviene comprobar la carpeta después de cada una.
- El audio **no se puede sacar por URL**: `cdn1.suno.ai` da 403 y el `.m4a`
  de CloudFront viene cifrado. Solo sirve el botón de descarga.

## La referencia aprobada

El chant de `en/movers/03` (0:26) es la toma que aprobó el usuario. Su
prompt de estilo es la fórmula para los demás chants: si uno no suena bien,
se compara contra ese.
