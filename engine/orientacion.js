/* Hacia donde mira o senala cada pose.
 *
 * Los dibujos no son simetricos: la pose 2 de los ninos de Starters senala
 * con el dedo hacia NUESTRA izquierda, la 7 corre hacia la derecha, y Pip
 * esta girado a la izquierda en casi todas. Cuando el personaje se coloca a
 * la izquierda de lo que presenta —las actividades, un objeto de la lamina,
 * el bocadillo— acaba senalando fuera de la pantalla, que es justo lo
 * contrario de lo que la ilustracion tiene que hacer.
 *
 * Aqui se anota solo lo que se ve sin discusion. Lo que mira de frente no
 * entra: voltear una figura frontal no arregla nada y puede estropear una
 * asimetria buscada (una mochila, un objeto en una mano).
 *
 * Quien lo usa da vuelta la imagen con scaleX(-1) cuando la direccion no
 * apunta al contenido. No hay arte nuevo: es el mismo PNG reflejado.
 *
 * Comprobado mirando las hojas de contacto de los tres niveles el
 * 27-ago-2026. Si se anaden poses, se miran y se anotan aqui.
 */
window.ORIENTACION = {
  // Starters: los cuatro ninos comparten set de poses
  'starters/freya':  { 2: 'izq', 7: 'der' },
  'starters/nico':   { 2: 'izq', 7: 'der' },
  'starters/astrid': { 2: 'izq', 7: 'der' },
  'starters/tomas':  { 2: 'izq', 7: 'der' },
  // Pip esta girado a la izquierda en casi todas
  'starters/pip':    { 1: 'izq', 2: 'izq', 3: 'izq', 4: 'izq' },

  'movers/erik':      { 7: 'der' },
  'movers/valentina': { 7: 'der' },
  'movers/sofia':     { 7: 'der' },
  'movers/mateo':     { 2: 'izq', 7: 'der' },
  'movers/luna':      { 2: 'der' },

  'flyers/ingrid': { 4: 'der', 7: 'izq' },
  'flyers/maya':   { 7: 'izq' },
  'flyers/oliver': { 7: 'izq' },
  'flyers/kili':   { 2: 'izq' },
};

/* Devuelve el style que hay que ponerle a la imagen para que mire hacia
   `hacia` ('izq' o 'der'). Vacio si ya mira bien o si la pose es frontal. */
window.miraHacia = function (nivel, slug, pose, hacia) {
  const ficha = window.ORIENTACION[nivel + '/' + slug];
  const tiene = ficha && ficha[Number(pose)];
  return (tiene && tiene !== hacia) ? ' style="transform:scaleX(-1)"' : '';
};
