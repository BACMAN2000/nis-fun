# Fun for Nordic — serie YLE propia de NIS

Preparación Cambridge Young Learners (Starters/Movers/Flyers) con personajes propios.
Arquitectura: https://claude.ai/code/artifact/5f302f83-b553-4a9e-903a-ebe157241fd0

## Estructura
- `characters/bible.md` — biblia de personajes (identidad, paletas, prompts). **Leerla antes de tocar assets.**
- `assets/characters/<nivel>/<slug>/pose-NN.svg` — 138 SVG planos provisionales. El arte final
  (3D estilo Pixar, generado con Canva AI usando los prompts de la biblia) reemplaza estos archivos
  con el mismo nombre; el motor y el libro no se tocan.
- `content/<nivel>/unit-NN.json` — **fuente única** de cada unidad. Cada actividad declara
  `outputs`: book / digital / quiz. **Flyers está COMPLETO: 55 unidades** (temario en su index.json);
  starters y movers tienen 3 unidades piloto cada uno.
  Reglas de contenido aprendidas: en `match_words` no repetir valores de izquierda ni de derecha,
  y sin comillas dobles dentro de los textos (rompen el atributo data-v). Las respuestas de
  listening deben aparecer textualmente en el script.
- `engine/crossword-layout.js` — auto-diagramación determinista: las unidades solo declaran
  `{word, clue}` y el layout se calcula igual en digital y en papel. (Las unidades 1-3 de cada
  nivel aún llevan row/col/dir explícitos; ambas formas conviven.)
- `engine/index.html` — curso digital. Portada de niveles: `engine/` · Hub de un nivel: `engine/?level=flyers` · Unidad: `engine/?level=flyers&unit=1`. Colores por nivel en el mapa `COLORS` (engine y book.html) y en `content/levels.json`.
  Renderers: crossword, match_words, listening (con fallback de voz del navegador si falta el mp3),
  exam_task. Progreso en localStorage (Supabase en fase posterior).
- `book-builder/book.html` — plantilla imprimible del Student's Book (portada + 1 página por unidad).
- `character-sheet.html` — hoja de contacto para revisar los 15 personajes.

## Tareas visuales del examen A2 Flyers (5.º grado)

El curso tenía todo el peso en texto. Los formatos del examen que se resuelven
**mirando** no existían, y son cuatro:

| Tipo | Parte del examen | Qué hace el alumno |
|------|------------------|--------------------|
| `label_people`   | Listening Part 1     | escribe el nombre debajo de cada persona de la lámina |
| `picture_mc`     | Listening Part 4     | escucha y marca 1 de 3 imágenes |
| `match_pictures` | Listening Part 3     | empareja a cada explorador con una letra A–H |
| `picture_story`  | R&W Part 7           | escribe la historia de tres viñetas en 20–25 palabras |

De Cambridge se copia el **tipo de tarea** (formato público que usan todas las
editoriales). El dibujo es nuestro: personajes de `characters/bible.md` sobre
escenarios de `assets/scenes`, y el vocabulario con `engine/vocab-art.js`. No
entra ninguna ilustración de *Fun for Flyers*: son de Cambridge University
Press & Assessment.

- `content/cast-flyers.json` — quién puede salir, con qué poses (las que hay en
  disco), cómo se le describe en el audio y en qué escenario. Aquí está también
  el reparto de las seis **funciones** de Cambridge (robot de gramática,
  marcador de tiempo, naturalista, rutinas, ortografía, guía adulto) entre
  nuestros personajes, y el único hueco que queda: **falta un adulto guía**.
- `tools/gen_visual_flyers.py` — el generador. Idempotente y determinista.
  También escribe `content/flyers/exam-map.json`, que es lo que lee el portal.
- `tools/check_visual_flyers.py` — la auditoría: poses que existen, escenas que
  existen, respuestas que están entre las opciones y que se oyen en el audio,
  y modelos de historia que caben en las 20–25 palabras que se piden.
- `tools/gen_audio_visual.py` — graba los diálogos con Edge TTS, una voz fija
  por personaje. Hace falta: el portátil del colegio solo tiene voces
  castellanas, así que la voz del navegador no sirve en clase.
- `tools/patch_engine_visual.py` — mete los renderers en `engine/index.html`
  **por ancla de texto, no copiando el archivo**. Hay dos copias del motor
  (este repo y `nis-portal/nis-fun/`) y no van a la par.

Cobertura: `label_people` y `picture_story` en las 55 unidades; `picture_mc` en
28 y `match_pictures` en 24. Las que faltan son unidades de gramática pura
(posesivos, preposiciones, meses, adverbios de frecuencia) donde no hay objeto
que dibujar; el generador **no** las rellena con dibujos falsos.

Cada actividad lleva un bloque `kpi` con el grado, la unidad del Scope &
Sequence de 5.º a la que sirve y el outcome que cubre. Eso es lo que permite
enseñarlas dentro de la clase (portal → 5.º → Cambridge Flyers) en vez de como
un curso de examen aparte.

## Correr en local
```
python -m http.server 9310 --directory C:/Projects/nis-fun
```
→ http://localhost:9310/engine/?level=flyers

## Libros (modos del book-builder)
`book.html?level=flyers&units=1,...,55` + `mode`:
- *(sin mode)* → Student's Book · `mode=wb` → Workbook (página de tarea por unidad, estilo Home
  booklet: copiar wordlist + homework + check yourself + firmas) · `mode=key` → Teacher's Key
  (todas las respuestas, compacto).
PDFs completos de Flyers ya compilados en book-builder/: `FunForNordic3-SB-full.pdf`,
`FunForNordic3-WB-full.pdf`, `FunForNordic3-TeachersKey.pdf`.

## Audio
`python tools/gen_audio.py` — genera los mp3 de las actividades C con ElevenLabs (una voz fija
por personaje, mapa VOICES dentro del script; key en el archivo de mocks-cambridge). Idempotente:
salta los que existen. El audio NO va por git.

## Compilar el Student's Book a PDF
Con el server corriendo:
```
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu ^
  --no-pdf-header-footer --virtual-time-budget=8000 ^
  --print-to-pdf="C:\Projects\nis-fun\book-builder\FunForNordic3-SB-pilot.pdf" ^
  "http://localhost:9310/book-builder/book.html?level=flyers&units=1,2,3"
```
(Notas: `--headless=new` falla en esta versión de Edge; usar `--headless` clásico. Si hay otro
Edge abierto, añadir `--user-data-dir="%TEMP%\edge-pdf-profile"` — sin eso sale exit 0 pero no
escribe el PDF.)

## Regenerar personajes SVG
```
python tools/gen_characters.py
```

## Audio (pendiente)
`audio/<nivel>/uNN-<actividad>.mp3` con ElevenLabs — 1 voz fija por personaje (anotarla en la
biblia al elegirla). El audio NO va por git. Mientras no exista el mp3, el motor usa la voz del
navegador como provisional.

## Arte 3D (Canva)
Instalado (PNG 3D con fallback SVG vía onerror en engine/book): **Flyers completo** (ingrid,
diego, maya, oliver, kili) + Movers erik, valentina, sofia. **Pendientes: mateo y luna** — la
cuota de IA de Canva se agotó; regenerar con los prompts de `characters/bible.md` y el pipeline:
generate-design → create-design-from-candidate → export-design `{"type":"png"}` (sin más
parámetros) → `tools/segment_sheet.py` → revisar con `tools/montage.py` → copiar a assets con la
numeración estándar. Starters se queda en SVG plano (decisión estilística para los pequeños).
Las hojas originales exportadas quedaron en los diseños Canva del usuario ("...Character Reference...").

## Pendientes de fase (ver artifact)
- Completar arte 3D: mateo y luna (cuando renueve la cuota de Canva).
- F1: 55 unidades Flyers + audio + Workbook PDF + quizzes en plataforma (tarjeta YLE separada,
  dentro: Starters/Movers/Flyers).
