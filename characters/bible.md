# Fun for Nordic — Biblia de personajes

Contrato de identidad de los 15 personajes de la serie. **Toda salida (digital, SB, WB, quizzes)
usa los mismos assets**: `assets/characters/<nivel>/<slug>/pose-NN.svg`. Si un personaje se
redibuja (p. ej. ilustración final en PNG), se reemplazan los archivos manteniendo nombre y
pose — el contenido nunca se toca.

## Poses estándar (todas las salidas las referencian por número)

| NN | Pose        | Uso típico |
|----|-------------|-----------|
| 01 | waving      | apertura de unidad, saludos |
| 02 | pointing    | señalar la actividad / instrucciones |
| 03 | talking     | diálogos, bocadillos de texto |
| 04 | thinking    | preguntas, "What do you think?" |
| 05 | surprised   | datos curiosos, respuestas inesperadas |
| 06 | sitting     | escenas de lectura / escritura |
| 07 | running     | verbos de acción, unidades de deporte |
| 08 | holding     | presentar objetos del wordlist |
| 09 | back        | escenas de viaje, mirar paisajes |
| 10 | celebrating | cierre de unidad, "Well done!" |

Las mascotas usan las poses 01–06 (01 saludo/ala, 02 señalar, 03 hablar, 04 pensar,
05 sorpresa, 06 dormir/descansar).

## Reglas de estilo (para regenerar sin que "cambien de cara")

- Estilo plano (flat), contornos suaves, paleta fija por personaje (abajo).
- Cabeza grande (~40 % de la altura), ojos de punto, cejas simples, sonrisa por defecto.
- Fondo siempre transparente. Lienzo 200×260 (niños), 200×200 (mascotas).
- La **voz ElevenLabs es parte de la identidad**: una voz fija por personaje, se elige una
  vez y se anota aquí (columna Voz, pendiente hasta generar el primer audio).

---

## Nivel 1 · Starters — Los Exploradores del Faro (Pre A1, 2.º–3.º)

| Slug     | Nombre | Edad | Rol pedagógico | Personalidad / frase | Paleta (pelo · piel · polo · pantalón) |
|----------|--------|------|----------------|----------------------|----------------------------------------|
| freya    | Freya  | 7 | Presenta vocabulario (siempre pregunta *What's this?*) | Curiosa, ojos enormes | rubio #E8C86A · claro #F6D7B8 · celeste #7FB6E0 · azul #3E5F8A |
| nico     | Nico   | 7 | Comete los errores que el alumno corrige | Bromista limeño, *Oops!* | negro #2A2320 · trigueño #C98E5A · rojo #E05C4B · jean #4A6786 |
| astrid   | Astrid | 8 | Da las instrucciones de cada actividad | Ordenada, lista de tareas | castaño #8A5A33 · claro #F6D7B8 · verde #58A87A · gris #6B7686 |
| tomas    | Tomás  | 7 | Protagoniza acciones y verbos | Deportista, nunca quieto | negro #2A2320 · trigueño #C98E5A · amarillo #E8B23A · azul #3E5F8A |
| pip      | Pip    | — | Mascota: frailecillo escondido en cada lámina (juego de búsqueda) | Tímido y silencioso | plumas #26313B blanco #F4F1EC · pico/patas #E88A2E |

## Nivel 2 · Movers — El Club del Fiordo (A1, 4.º–5.º)

| Slug      | Nombre    | Edad | Rol pedagógico | Personalidad / frase | Paleta |
|-----------|-----------|------|----------------|----------------------|--------|
| erik      | Erik      | 9  | Introduce la gramática nueva (sus inventos la demuestran) | Inventor, gafas | rubio rojizo #C97B3A · claro #F6D7B8 · naranja #E08A3C · marrón #6E5643 |
| valentina | Valentina | 9  | Narra las historias de secuencias (Reading Part 5) | Cuentacuentos, *Once upon a time…* | negro #2A2320 · trigueño #C98E5A · morado #8A6FB5 · gris #6B7686 |
| sofia     | Sofía     | 10 | Conecta con lugares y comparativos | Viajera, mapa en mano | castaño #8A5A33 · trigueño #C98E5A · turquesa #4BA8A0 · jean #4A6786 |
| mateo     | Mateo     | 9  | Sus olvidos generan los diálogos de Listening | Despistado, *Where's my…?* | negro #2A2320 · claro #F6D7B8 · verde #58A87A · azul #3E5F8A |
| luna      | Luna      | —  | Mascota: husky, protagoniza historias en pasado | Leal, aúlla en las canciones | pelaje #9AA7B5 blanco #F4F1EC · ojos #5FA8D9 |

## Nivel 3 · Flyers — La Expedición Aurora (A2, 6.º)

| Slug   | Nombre | Edad | Rol pedagógico | Personalidad / frase | Paleta |
|--------|--------|------|----------------|----------------------|--------|
| ingrid | Ingrid | 11 | Modela opinión y sugerencia (*How about…?*) | Capitana, decidida | rubio #E8C86A · claro #F6D7B8 · azul marino #2F5D9E · gris #6B7686 |
| diego  | Diego  | 11 | Sus entrevistas son la base de Listening y Speaking | Reportero, micrófono | negro #2A2320 · trigueño #C98E5A · rojo #E05C4B · negro #3A3F47 |
| maya   | Maya   | 12 | Presenta temas de mundo real (ríos, planetas, salud) | Científica, lupa | castaño #6E4A2F · trigueño #C98E5A · verde #3E8E6B · caqui #8F8562 |
| oliver | Oliver | 11 | Canciones y chants de cierre de módulo | Músico, tararea todo | pelirrojo #C9622E · claro #F6D7B8 · mostaza #D9A13B · jean #4A6786 |
| kili   | Kili   | —  | Mascota: cóndor "cartero" — trae postales y cartas (Writing) | Solemne pero torpe al aterrizar | plumas #2E2A33 collar #F4F1EC · cabeza #D98A6A |

---

## Prompts de regeneración (ilustración final)

Cuando se pase de SVG plano a ilustración, usar por personaje:

> Flat vector children's book character, full body, transparent background, big head
> (40% of height), dot eyes, soft outlines, friendly smile. [NOMBRE], [EDAD] years old,
> [pelo], [piel], wearing [polo] t-shirt and [pantalón] trousers. Pose: [POSE de la tabla].
> Consistent character sheet style, no shadows, 200×260.

Mascotas: mismo estilo, cuerpo compacto 200×200, rasgos de la paleta indicada.
