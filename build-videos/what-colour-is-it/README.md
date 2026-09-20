# What Colour Is It? — video del chant (unidad 01 Starters)

Producción del video animado del chant «What Colour Is It?» (Fun for Nordic,
unidad 01), generado con tomas de Gemini (Veo) y montado con ffmpeg al audio
original del curso (`starters-01-chant.mp3`, 28,92 s).

- **Entregable:** `outputs/What-Colour-Is-It-final.mp4` (29,30 s · 1280×720 · 24 fps)
- **Publicado en:** https://nis.cohasset.pe/nis-fun/assets/videos/starters-01-what-colour.mp4
  (copiado a `/opt/nis-media/videos/` en el servidor; los videos viven fuera del repo)
- **En el portal:** pantalla Canciones de la unidad 01 → botón «Watch the video»
  (soporte añadido en `engine/songs.js` del repo nis-portal, commit
  `pub-video-what-colour` — push pendiente de credenciales de escritura)
- **Póster del reproductor:** `posters/starters-01-what-colour.jpg`
  (en el servidor, en `/opt/nis-media/videos/posters/`)

## Estructura

- `outputs/` — entregables y documentos: video final, póster, subtítulos (SRT),
  guion, letra, notas de producción y estado.
- `work/` — material de montaje: clips generados en Gemini (irremplazables),
  transcripciones de Whisper (JSON), scripts de montaje en Python/ffmpeg,
  subtítulos ASS y frames de auditoría (`work/audit/`).

Los mp4/mp3 de esta carpeta están gitignored (convención de `build-videos/`):
se trackean los scripts, ASS, JSON y documentos. El audio fuente es
`work/what-colour-is-it-original.mp3` (copia del mp3 del curso).

## Reconstruir el montaje final

```
cd work
python fix_green_verse_tags.py      # regenera colour-final-v3.ass (tags \an8)
python build_recap.py               # concat + subtítulos quemados → ../outputs/...-final.mp4
```

Requiere ffmpeg 8.x en PATH. PITFALL: los tags ASS en Python siempre con
raw-strings (`r'{\an8…}'`) — sin ello `\a` se convierte en BEL y libass corta
el texto fuera de cuadro (fue el bug de la v2).

Historial: producción de 2026-09-19/20 (sesiones Codex + Gemini, auditoría y
cierre en ZCode). Consolidado aquí el 2026-09-20 desde
`Documents/Codex/2026-09-19/https-www-youtube-com-watch-v/`.
