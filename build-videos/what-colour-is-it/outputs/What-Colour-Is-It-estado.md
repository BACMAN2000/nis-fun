# What Colour Is It? — video final con letra sincronizada

Video: What-Colour-Is-It-final.mp4
Duración: 29,30 segundos; 1280 × 720; 24 fps; audio original íntegro de Fun for Nordic (starters-01-chant.mp3), sin cambios de velocidad.

## Contenido

Verso rojo (pelota), amarillo (cometa), azul (tren) y verde (coche), recap «Red ball, yellow kite! Blue train, green car!» con un corte por juguete en su palabra cantada, y cierre con la caja de juguetes. La banda de letra va abajo hasta el verso azul y arriba desde el verso verde (15,1 s) hasta el final, para no tapar coche ni caja.

## Correcciones aplicadas

1. Coche verde regenerado: rueda sobre el pavimento con las cuatro ruedas apoyadas; Nico lo sostiene y Freya lo detiene.
2. Recap por juguete: pelota roja (20,36) → cometa amarilla (21,04) → tren azul (21,70) → coche verde (22,32) → caja (23,60).
3. Subtítulos del verso verde reanchorados: un tag `\an8` roto (carácter BEL generado por `'{\an8…}'` sin raw-string en build_green_v2.py) dejaba «What colour is it?», «Green! Green!» y «The car is green!» cortadas en el borde superior. Corregido en work/colour-final-v3.ass (generado por work/fix_green_verse_tags.py) y rehecho el montaje final; las líneas inferiores no cambiaron.

## Verificación (2026-09-20)

Decodificación completa sin errores; 29,29 s de video y 29,30 s de audio. Letra comprobada por perfil de píxeles en las 20 líneas: banda inferior 652–684, banda superior 36–65, ninguna fuera de cuadro. Revisión visual del verso verde y del recap confirmada fotograma a fotograma.

Scripts de montaje: work/build_recap.py (montaje), work/fix_green_verse_tags.py (subtítulos). El SRT de referencia está en What-Colour-Is-It-subtitulos.srt.

## Publicación en el portal (2026-09-20)

El video está publicado como material del chant «What Colour Is It?» (unidad 01 de Starters) en el portal del curso:

- Video: https://nis.cohasset.pe/nis-fun/assets/videos/starters-01-what-colour.mp4 (copiado en el servidor a /opt/nis-media/videos/; los videos viven fuera del repo).
- Póster: posters/starters-01-what-colour.jpg (copia local en What-Colour-Is-It-poster-portal.jpg).
- La pantalla de Canciones del engine (nis-fun/engine/songs.js) ahora muestra un botón «Watch the video» cuando la pieza tiene campo `video` en songs-starters.json; el video se ve dentro de la pantalla y nunca suena a la vez que el audio. Cache-busting actualizado (CONTENT_V = 2026-09-20-what-colour-video, songs.js?v=b96c25cf).
- Verificado en vivo: JSON con campo video, songs.js nuevo servido, video 200/206 con rangos y reproducción real comprobada en navegador (29,3 s, 1280 px, frame del verso rojo correcto).

Pendiente (único paso): empujar el commit f52ef13c (rama pub-video-what-colour, worktree C:/Users/User/nis-portal-pub) a main de bacman2000/nis-portal. La deploy key del servidor es read-only y no hay credenciales de escritura en la máquina. Mientras tanto los 3 archivos cambiados viven sin commit en el working tree del servidor (/opt/nis-portal) y el auto-pull los descartará en el próximo push ajeno; hay un marcador en /opt/nis-media/DEPLOY-PENDIENTE-PUSH.md del servidor.
