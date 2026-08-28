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

---

# Regla de oro: la biblia es la lista cerrada

**Quien no está en este documento, no sale en Fun for Nordic.**

Cuando un texto se inventa un compañero o un tío nuevo, el alumno se encuentra con
alguien que no tiene cara, no tiene dibujo y no vuelve a aparecer nunca más. Y cuando
se le pide arte a una IA sin decirle a quién, devuelve un niño distinto cada vez: al
cabo de tres unidades el colegio está lleno de desconocidos.

Por eso:

1. **Antes de escribir** una unidad, se elige a los personajes de las tablas de abajo.
   Si de verdad hace falta alguien nuevo, primero se le da ficha aquí.
2. **Antes de pedir arte a una IA**, se copia la ficha del personaje en el prompt —
   nombre, edad, pelo, piel, ropa y paleta— y se adjunta una imagen suya ya aprobada
   como referencia de estilo. Nunca se pide "un niño"; se pide *ese* niño.
3. **`python tools/check_elenco.py`** comprueba las dos cosas: que los nombres que
   usan los textos estén aquí, y que el arte de `assets/characters/` se corresponda
   con las fichas. Sale con error si aparece un intruso.

## Prompt maestro (pegar tal cual, cambiando solo la ficha)

Para las figuras de cuerpo entero que usan la portada de nivel y los videos, los ocho
prompts pendientes ya están escritos con su ficha puesta, junto con la herramienta de
recorte: [prompts-fullbody.md](prompts-fullbody.md).

> Use ONLY the character described below. Do NOT invent a new character, do NOT change
> the face, the hair or the clothes, and do NOT add other people to the image.
> This is an existing character from our school's own English course (our own IP), and
> the attached image is the approved reference for the style.
>
> **[NOMBRE]**, [EDAD] years old. Hair: [pelo]. Skin: [piel]. Wearing [ropa].
> 3D cartoon style, full body, transparent background, big head, big friendly eyes,
> soft rounded shapes, same proportions as the reference.
> Pose: [pose de la tabla de poses].

---

# Familias de los protagonistas

Estas personas **ya aparecen en los textos del curso**. Se dibujan con las figuras 3D
del banco (`assets/vocab/`), que es de donde salen las madres, padres y abuelos de las
escenas — no tienen carpeta propia en `assets/characters/`.

| slug | Nombre | De quién es | Figura del banco | Dónde sale |
|------|--------|-------------|------------------|------------|
| rosa | Rosa | Madre de Nico | `mother.png` | Starters 2, Flyers 2 |
| juan | Juan | Padre de Nico | `father.png` | Starters 2 |
| lucia | Lucía | Hermana pequeña de Nico, 5 años | `sister.png` | Starters 2 |
| beto | Beto | Primo bebé de Nico, 1 año | `baby.png` | Starters 2 |
| pablo | Pablo | Abuelo de Sofía; tiene la granja | `grandpa.png` | Movers 10 |
| carmen | Carmen | Tía de Valentina | `mother.png` | Movers 22 |
| sven | Sven | Abuelo de Ingrid, noruego | `grandpa.png` | Flyers 32 |
| nora | Nora | Tía de Ingrid, viajera | `mother.png` | Flyers 32 |
| tom | Tom | Tío de Ingrid | `father.png` | Flyers 32 |
| leo | Leo | Tío de Maya | `father.png` | Flyers 30 |

# Secundarios del pueblo

| slug | Nombre | Quién es | Figura del banco | Dónde sale |
|------|--------|----------|------------------|------------|
| pedro | Pedro | El taxista | `father.png` | Flyers (viajes) |
| ana | Ana | Compañera de otra clase | `sister.png` | Starters 20 |
| carla | Carla | Compañera de otra clase | `sister.png` | Flyers 51 |

# La familia monstruo

Solo para las unidades de describir personas, donde el chiste es que cada uno tiene un
número distinto de ojos, brazos y dientes. **No se mezclan con los niños.**

| slug | Nombre | Quién es | Rasgo que lo distingue | Dónde sale |
|------|--------|----------|------------------------|------------|
| grum | Grum | El abuelo monstruo | Verde, tres ojos, muy peludo | Flyers 24 |
| zog | Zog | El tío monstruo | Morado, un ojo, dos brazos largos | Flyers 24 |
| zip | Zip | El primo monstruo, pequeño | Naranja, cuatro ojos, redondo | Flyers 24 |

## Qué archivos tiene que tener cada personaje

`pose-01.png` como mínimo y **siempre** `fullbody.png`. El banner y la portada del nivel
piden el segundo y, si falta, caen a `pose-01` con un `onerror`: se ve bien, pero cada
carga deja un 404. Cuando no hay una figura de cuerpo entero propia —dibujada aparte y
más grande, como la de Ingrid— vale la copia de `pose-01`, que es lo que el navegador
acababa mostrando; Freya está así desde el principio.

`python tools/asegura_fullbody.py --arregla` lo comprueba y lo copia donde falte.

# Compañeros de clase

Los cuatro niños de cada nivel son los protagonistas, pero en el patio, en los pasillos
y en el aula hacen falta más caras. Estas seis fichas están **cerradas y aprobadas**, y
desde el 27-ago-2026 **tienen arte**: viven en los tres niveles a la vez
(`assets/characters/{starters,movers,flyers}/<slug>/`), porque el motor arma la ruta con
el nivel y un compañero que solo existiera en starters no se podría usar en el patio de
flyers, que es justo donde salen.

**No vale recolorear a un protagonista.** Se probó y lo que sale es Freya con otra
camiseta: la cara es la misma y el alumno lo nota. Un compañero es un dibujo nuevo, con
la ficha de abajo y el prompt maestro de arriba.

| slug | Nombre | Edad | Pelo · piel · ropa | Qué hace en las escenas |
|------|--------|------|--------------------|-------------------------|
| lia | Lía | 8 | trenzas negras #1F1A17 · trigueña #C98E5A · polo lila #9B7BC4, falda gris | Salta a la comba en el patio |
| bruno | Bruno | 8 | rizos castaños #6E4A2F · claro #F6D7B8 · polo verde agua #4BA8A0, short beige | Corre detrás de la pelota |
| aiko | Aiko | 9 | melena lisa negra #22201F · claro #F6D7B8 · polo coral #E87F6A, jeans | Lee sentada en el pasillo |
| samu | Samu | 9 | pelo corto rubio oscuro #B99457 · claro #F6D7B8 · polo azul marino #2F5D9E | Lleva la mochila y saluda |
| iris | Iris | 10 | coleta pelirroja #C9622E · pecas · polo mostaza #D9A13B, jeans | Dibuja con tiza en el suelo |
| tino | Tino | 10 | rapado castaño oscuro #4A3728 · trigueño #C98E5A · polo blanco y verde | Juega al hockey en la cancha |

Poses que hacen falta para cada uno, por orden de utilidad:
**01 waving**, **07 running**, **06 sitting**, **03 talking**. De momento las cuatro
apuntan a la misma figura de pie: mejor el mismo dibujo repetido que una casilla rota en
la lámina. Cuando haya poses de verdad se sustituyen una a una.
