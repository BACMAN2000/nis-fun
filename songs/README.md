# Canciones y chants por unidad

Dos piezas por unidad, sacadas del **vocabulario y la gramática de esa unidad**:
un **chant** (drill rítmico, call-and-response) y una **canción** (la misma
gramática dentro de una historia).

    piloto.json         la letra y el estilo de las piezas de prueba
    starters.json       las 90 piezas de Starters (45 unidades x 2)
    starters-suno.json  que hay generado en Suno y a que unidad pertenece
    _lote*.json         las tandas en que se escribieron las letras
    monta.py            junta las letras, les pone estilo y mide vocabulario
    revisa.py           elenco y copyright
    audio/              los mp3 aprobados

Las tandas se escriben como `_chunkNN.json`; `monta.py` las **suma** a lo que
ya hay (no monta de cero, que borraria las unidades de las tandas anteriores).
En cuanto una tanda esta dentro se renombra a `_loteN.json` para que deje de
reaplicarse: si no, cualquier correccion hecha a mano en `starters.json` se
perderia la proxima vez que alguien ejecute el script.

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

## Cada unidad suena distinta

Las ocho primeras canciones salieron con **una sola formula de estilo** para
las 45 unidades, y sonaban todas igual: mismo tempo, mismos instrumentos,
mismo aire. Ahora `monta.py` tiene un repertorio de 15 grooves y le da a cada
unidad el que le pega por tema — desfile de banda para el zoo, vals para la
familia, funk para mover el cuerpo, doo-wop para las caras — con una regla
dura: **dos unidades seguidas nunca llevan el mismo**. El propio script lo
comprueba y lo dice al terminar.

    python songs/monta.py starters --estilo   # re-estila sin tocar las letras

El **chant si comparte formula**, y es a proposito: es un drill de percusion
y voz, sin instrumentos melodicos. Ahi lo que varia es la letra.

## Trampas ya pisadas

- **El editor de letra solo acepta un evento `paste` de verdad.** Escribir
  con teclado simulado o `execCommand` no entra. La caja de *Styles*, en
  cambio, es un `<textarea>` normal y no escucha ese evento: ahi hay que
  usar el setter nativo de `value` y disparar `input`.
- **La caja no se vacia con `execCommand('delete')`.** Si no se borra bien,
  la letra nueva se pega DETRAS de la anterior y sale un clip con dos
  unidades mezcladas — pasa desapercibido porque Suno genera algo. Se borra
  con el teclado (`Ctrl+A`, `Supr`) y se comprueba el LARGO de la caja antes
  de pulsar Create.
- **Leer la caja en la misma llamada que el pegado devuelve el valor viejo.**
  Hay que leerla en una llamada aparte, o esperar dentro del script.
- **El filtro de copyright de Suno corta en silencio.** El aviso («Your
  lyrics contain copyrighted material») solo sale un par de segundos encima
  del boton Create; en la biblioteca no queda ni rastro, asi que parece que
  el clic no llego. Hay que mirar la pantalla justo despues de pulsar. Lo
  que lo disparo fue recitar los numeros del uno al diez seguidos: se
  arreglo contando objetos («three red balls, six blue kites»), que ademas
  es mejor para ensenar a contar.
- **Suno renombra las piezas.** «Pip's Toy Box» aparece como «Toy Box Fun»,
  y dos piezas distintas pueden acabar con el mismo titulo. Por eso el
  nombre no vale para identificarlas: la correspondencia esta en
  `starters-suno.json`, con los ids.
- **`Ctrl+A` en el campo de estilo deja una «a» pegada al principio**
  (`aupbeat children's…`) y esa «a» viaja al prompt. Borrarla con
  `Ctrl+Home` + `Supr`.
- **Chrome bloquea la segunda descarga seguida del mismo sitio**, en
  silencio. Hay que permitirlo en el icono de la barra de direcciones, y aun
  así conviene comprobar la carpeta después de cada una.
- El audio **no se puede sacar por URL**: `cdn1.suno.ai` da 403 y el `.m4a`
  de CloudFront viene cifrado. Solo sirve el botón de descarga.

## Antes de mandar nada a Suno

    python songs/revisa.py starters

Comprueba dos cosas que `monta.py` no mira y que salen caras:

* **el elenco.** La biblia de personajes es una lista cerrada. Una cancion que
  se invente una prima deja al alumno con alguien que no tiene cara ni dibujo.
* **el copyright.** Suno rechaza la letra que se parece a una cancion infantil
  conocida, y lo hace en silencio. La lista de temas vigilados esta en el
  propio script y crece con cada rechazo: Old MacDonald, *If You're Happy*,
  *Rain Rain Go Away*, *Happy Birthday to You*, *Head, Shoulders...*, el
  abecedario cantado de corrido y el 1-a-10 de *Once I Caught a Fish Alive*.

## La referencia aprobada

El chant de `en/movers/03` (0:26) es la toma que aprobó el usuario. Su
prompt de estilo es la fórmula para los demás chants: si uno no suena bien,
se compara contra ese.
