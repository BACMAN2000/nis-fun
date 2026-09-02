/* Dibujos de vocabulario de Fun for Nordic — SVG propios.
 *
 * Sustituyen a los emoji del sistema, que se veian distintos en cada equipo
 * y no eran arte de la escuela. Todos comparten lienzo 64x64, paleta y
 * grosor de trazo, para que una fila de palabras lea como un conjunto.
 *
 * Uso:  VOCAB_ART.get('umbrella')  ->  string SVG, o null si no hay dibujo
 *       (el motor cae entonces al emoji de emoji-map.js).
 */
window.VOCAB_ART = (function () {

  // ---- paleta comun ------------------------------------------------------
  const C = {
    azul:'#4987c6', azulClaro:'#a9c6e4', azulOsc:'#2f5f92',
    rojo:'#e0574a', naranja:'#ef8a3c', amarillo:'#f2c14e',
    verde:'#3fa06a', verdeClaro:'#8ecfa8',
    rosa:'#e58fa8', morado:'#8f7bc4', marron:'#a9713f', marronOsc:'#6b4423',
    gris:'#8b98a5', grisOsc:'#5a6672', blanco:'#ffffff', negro:'#33373d',
    piel:'#f3c9a0', pielOsc:'#d9a273', crema:'#f7ead6'
  };

  const svg = (inner) =>
    '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" ' +
    'fill="none" stroke-linecap="round" stroke-linejoin="round">' + inner + '</svg>';

  // Figura humana reutilizable: cambia pelo, piel, ropa y estatura.
  // Con esto las ocho palabras de familia salen del mismo molde.
  function persona(o) {
    const cx = 32;
    const alto = o.alto || 0;                 // 0 adulto, 6 nino, 10 bebe
    const cy = 22 + alto * 0.5;               // centro de la cabeza
    const r  = 11 - alto * 0.25;              // radio de la cabeza
    const hombro = cy + r + 3;
    const pelo = o.pelo || C.marronOsc;
    const piel = o.piel || C.piel;
    const ropa = o.ropa || C.azul;
    let s = '';
    // pelo de fondo (melena) si toca
    if (o.melena)
      s += `<path d="M${cx-r-2} ${cy+2} q0-${r+6} ${r+2}-${r+6} q${r+2} 0 ${r+2} ${r+6} l0 ${r+3} q-2-4-4-5 l-${2*r-4} 0 q-2 1-4 5z" fill="${pelo}"/>`;
    s += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${piel}"/>`;
    // flequillo
    s += `<path d="M${cx-r} ${cy-2} a${r} ${r} 0 0 1 ${2*r} 0 q-${r*0.5} -4 -${r} -3 q-${r*0.5} -1 -${r} 3z" fill="${pelo}"/>`;
    if (o.canas)
      s += `<path d="M${cx-r} ${cy-2} a${r} ${r} 0 0 1 ${2*r} 0 q-${r*0.5} -4 -${r} -3 q-${r*0.5} -1 -${r} 3z" fill="#cfd6dd"/>`;
    // ojos y sonrisa
    s += `<circle cx="${cx-r*0.38}" cy="${cy+1}" r="1.5" fill="${C.negro}"/>`;
    s += `<circle cx="${cx+r*0.38}" cy="${cy+1}" r="1.5" fill="${C.negro}"/>`;
    s += `<path d="M${cx-3} ${cy+r*0.5} q3 3 6 0" stroke="${C.negro}" stroke-width="1.6"/>`;
    if (o.gafas) {
      s += `<circle cx="${cx-r*0.38}" cy="${cy+1}" r="3.2" stroke="${C.grisOsc}" stroke-width="1.4"/>`;
      s += `<circle cx="${cx+r*0.38}" cy="${cy+1}" r="3.2" stroke="${C.grisOsc}" stroke-width="1.4"/>`;
      s += `<path d="M${cx-r*0.38+3.2} ${cy+1} l${r*0.76-6.4} 0" stroke="${C.grisOsc}" stroke-width="1.4"/>`;
    }
    if (o.bigote)
      s += `<path d="M${cx-4} ${cy+r*0.28} q4 2 8 0" stroke="${C.grisOsc}" stroke-width="2"/>`;
    // cuerpo
    const ancho = 11 - alto * 0.3;
    s += `<path d="M${cx-ancho} 56 q0-${56-hombro} ${ancho}-${56-hombro} q${ancho} 0 ${ancho} ${56-hombro} z" fill="${ropa}"/>`;
    return s;
  }

  // Fachada reutilizable para los lugares de Flyers.
  function edificio(o) {
    const cuerpo = o.cuerpo || C.crema;
    let s = `<rect x="${o.x||12}" y="${o.y||26}" width="${o.w||40}" height="${o.h||28}" rx="2" fill="${cuerpo}"/>`;
    s += `<rect x="8" y="54" width="48" height="4" rx="1.5" fill="${C.grisOsc}"/>`;
    return s;
  }

  const A = {};

  // ================= STARTERS 1 · juguetes y colores =====================
  A.ball = svg(
    `<circle cx="32" cy="34" r="19" fill="${C.rojo}"/>` +
    `<path d="M13 34 q19-9 38 0" stroke="${C.blanco}" stroke-width="3"/>` +
    `<path d="M32 15 q-9 19 0 38" stroke="${C.blanco}" stroke-width="3"/>` +
    `<path d="M20 20 q12 14 0 28" stroke="${C.blanco}" stroke-width="2" opacity=".55"/>`);

  A.kite = svg(
    `<path d="M32 6 L52 28 L32 54 L12 28 Z" fill="${C.amarillo}"/>` +
    `<path d="M32 6 L32 54" stroke="${C.blanco}" stroke-width="2"/>` +
    `<path d="M12 28 L52 28" stroke="${C.blanco}" stroke-width="2"/>` +
    `<path d="M32 6 L52 28 L32 30 Z" fill="${C.rojo}"/>` +
    `<path d="M32 30 L12 28 L32 54 Z" fill="${C.verde}" opacity=".85"/>` +
    `<path d="M32 54 q6 4 0 8 q-6 4 0 6" stroke="${C.grisOsc}" stroke-width="2"/>`);

  A.train = svg(
    `<rect x="4" y="34" width="22" height="14" rx="3" fill="${C.amarillo}"/>` +
    `<rect x="8" y="38" width="6" height="6" rx="1" fill="${C.crema}"/>` +
    `<rect x="17" y="38" width="6" height="6" rx="1" fill="${C.crema}"/>` +
    `<path d="M30 48 v-18 q0-4 4-4 h12 q4 0 4 4 v18z" fill="${C.rojo}"/>` +
    `<rect x="34" y="30" width="12" height="8" rx="1.5" fill="${C.azulClaro}"/>` +
    `<rect x="48" y="36" width="10" height="12" rx="2" fill="${C.rojo}"/>` +
    `<rect x="36" y="18" width="7" height="10" rx="2" fill="${C.grisOsc}"/>` +
    `<rect x="2" y="47" width="58" height="4" rx="2" fill="${C.grisOsc}"/>` +
    `<g fill="${C.negro}"><circle cx="11" cy="52" r="4.5"/><circle cx="22" cy="52" r="4.5"/>` +
    `<circle cx="37" cy="52" r="4.5"/><circle cx="50" cy="52" r="4.5"/></g>` +
    `<g fill="${C.gris}"><circle cx="11" cy="52" r="1.8"/><circle cx="22" cy="52" r="1.8"/>` +
    `<circle cx="37" cy="52" r="1.8"/><circle cx="50" cy="52" r="1.8"/></g>` +
    `<circle cx="39" cy="13" r="3.5" fill="#dbe4ee" stroke="#b6c6d6" stroke-width="1.2"/>` +
    `<circle cx="45" cy="7" r="4.5" fill="#dbe4ee" stroke="#b6c6d6" stroke-width="1.2"/>`);

  A.car = svg(
    `<path d="M8 44 l2-10 q1-4 5-4 h34 q4 0 5 4 l2 10 z" fill="${C.verde}"/>` +
    `<path d="M17 30 l3-8 q1-3 4-3 h16 q3 0 4 3 l3 8 z" fill="${C.verdeClaro}"/>` +
    `<path d="M32 19 l0 11" stroke="${C.verde}" stroke-width="2"/>` +
    `<rect x="6" y="42" width="52" height="6" rx="3" fill="${C.verde}"/>` +
    `<circle cx="18" cy="49" r="6" fill="${C.negro}"/><circle cx="18" cy="49" r="2.4" fill="${C.gris}"/>` +
    `<circle cx="46" cy="49" r="6" fill="${C.negro}"/><circle cx="46" cy="49" r="2.4" fill="${C.gris}"/>`);

  A.teddy = svg(
    `<circle cx="17" cy="18" r="7" fill="${C.marron}"/><circle cx="47" cy="18" r="7" fill="${C.marron}"/>` +
    `<circle cx="17" cy="18" r="3.4" fill="${C.crema}"/><circle cx="47" cy="18" r="3.4" fill="${C.crema}"/>` +
    `<ellipse cx="32" cy="40" rx="15" ry="16" fill="${C.marron}"/>` +
    `<ellipse cx="32" cy="44" rx="9" ry="9" fill="${C.crema}"/>` +
    `<circle cx="32" cy="24" r="14" fill="${C.marron}"/>` +
    `<ellipse cx="32" cy="28" rx="7" ry="5.5" fill="${C.crema}"/>` +
    `<ellipse cx="32" cy="25.5" rx="2.6" ry="2" fill="${C.negro}"/>` +
    `<circle cx="26" cy="21" r="1.9" fill="${C.negro}"/><circle cx="38" cy="21" r="1.9" fill="${C.negro}"/>` +
    `<path d="M29 30 q3 2.5 6 0" stroke="${C.negro}" stroke-width="1.5"/>`);

  A.doll = svg(
    `<path d="M14 26 q0-16 18-16 q18 0 18 16 l0 4 q-4-3-8-3 l-20 0 q-4 0-8 3z" fill="${C.amarillo}"/>` +
    `<circle cx="32" cy="26" r="12" fill="${C.piel}"/>` +
    `<path d="M20 24 a12 12 0 0 1 24 0 q-6-5-12-4 q-6-1-12 4z" fill="${C.amarillo}"/>` +
    `<circle cx="27" cy="27" r="2" fill="${C.negro}"/><circle cx="37" cy="27" r="2" fill="${C.negro}"/>` +
    `<path d="M29 32 q3 3 6 0" stroke="${C.rojo}" stroke-width="1.8"/>` +
    `<circle cx="22" cy="28" r="2.4" fill="${C.rosa}" opacity=".7"/>` +
    `<circle cx="42" cy="28" r="2.4" fill="${C.rosa}" opacity=".7"/>` +
    `<path d="M18 56 q2-18 14-18 q12 0 14 18 z" fill="${C.rosa}"/>` +
    `<path d="M26 40 q6 4 12 0" stroke="${C.blanco}" stroke-width="2" opacity=".7"/>`);

  // Colores: un lapiz con la punta del color que nombra.
  const lapiz = (col) => svg(
    `<path d="M22 8 h20 v34 l-10 12 l-10-12 z" fill="${C.crema}"/>` +
    `<path d="M22 8 h20 v6 h-20 z" fill="${C.grisOsc}" opacity=".25"/>` +
    `<path d="M22 38 h20 v4 l-10 12 l-10-12 z" fill="${col}"/>` +
    `<path d="M28 50 l4 4 l4-4 z" fill="${C.negro}" opacity=".55"/>` +
    `<rect x="22" y="8" width="20" height="46" rx="2" stroke="${C.grisOsc}" stroke-width="1.6" opacity=".45"/>` +
    `<rect x="22" y="14" width="7" height="24" fill="${C.blanco}" opacity=".35"/>`);
  A.red = lapiz(C.rojo);
  A.blue = lapiz(C.azul);
  A.green = lapiz(C.verde);
  A.yellow = lapiz(C.amarillo);

  // ================= STARTERS 2 · la familia ============================
  A.mother  = svg(persona({melena:1, pelo:C.marronOsc, ropa:C.rosa}));
  A.father  = svg(persona({pelo:C.negro, ropa:C.azul}));
  A.sister  = svg(persona({melena:1, pelo:C.amarillo, ropa:C.morado, alto:5}));
  A.brother = svg(persona({pelo:C.naranja, ropa:C.verde, alto:5}));
  A.grandma = svg(persona({melena:1, pelo:'#cfd6dd', ropa:C.morado, gafas:1}));
  A.grandpa = svg(persona({pelo:'#cfd6dd', ropa:C.grisOsc, gafas:1, bigote:1}));
  A.baby    = svg(
    persona({pelo:C.amarillo, piel:C.piel, ropa:C.amarillo, alto:10}) +
    `<path d="M24 20 q2-5 8-5 q6 0 8 5" stroke="${C.azulClaro}" stroke-width="2.4"/>`);
  A.family  = svg(
    `<g transform="translate(-11 6) scale(0.62)">${persona({melena:1, pelo:C.marronOsc, ropa:C.rosa})}</g>` +
    `<g transform="translate(11 6) scale(0.62)">${persona({pelo:C.negro, ropa:C.azul})}</g>` +
    `<g transform="translate(0 24) scale(0.44)">${persona({pelo:C.naranja, ropa:C.verde})}</g>`);

  // ================= MOVERS 1 · animales ================================
  A.bat = svg(
    `<path d="M32 30 q-6-12-16-13 q3 5 0 8 q5-1 6 3 q-7 0-11 5 q6 1 8 5 q7 3 13-2z" fill="${C.morado}"/>` +
    `<path d="M32 30 q6-12 16-13 q-3 5 0 8 q-5-1-6 3 q7 0 11 5 q-6 1-8 5 q-7 3-13-2z" fill="${C.morado}"/>` +
    `<ellipse cx="32" cy="32" rx="8" ry="10" fill="#4a3f6b"/>` +
    `<path d="M26 24 l-2-8 l7 5z" fill="#4a3f6b"/>` +
    `<path d="M38 24 l2-8 l-7 5z" fill="#4a3f6b"/>` +
    `<circle cx="29" cy="30" r="2" fill="${C.amarillo}"/>` +
    `<circle cx="35" cy="30" r="2" fill="${C.amarillo}"/>` +
    `<path d="M29 37 l1.5 3 M35 37 l-1.5 3" stroke="${C.blanco}" stroke-width="1.8"/>`);

  A.dolphin = svg(
    `<path d="M8 40 q10-22 30-22 q14 0 18 10 q-8-2-14 2 q6 6 4 14 q-14 8-28 2 q-6-2-10-6z" fill="${C.azul}"/>` +
    `<path d="M30 18 q2-9 8-11 q-1 7 2 11z" fill="${C.azulOsc}"/>` +
    `<path d="M14 42 q10 6 22 4 q-8 6-16 4z" fill="${C.azulClaro}" opacity=".8"/>` +
    `<path d="M52 28 q7-4 8-9 q2 8-3 13z" fill="${C.azul}"/>` +
    `<circle cx="18" cy="32" r="1.9" fill="${C.negro}"/>` +
    `<path d="M9 37 q4 1 7 0" stroke="${C.azulOsc}" stroke-width="1.6"/>`);

  A.kangaroo = svg(
    `<path d="M46 52 q10-2 14-8 q-2 9-12 12 q-4 1-6-2z" fill="${C.marron}"/>` +
    `<path d="M20 54 q-6 0-6-3 q0-3 5-4 l6-1 q-3-8 0-16 q3-9 12-9 q9 0 11 8 q2 8-3 14 q6 4 6 11 h-31z" fill="${C.marron}"/>` +
    `<path d="M40 18 q0-9 3-12 q3 5 1 12z" fill="${C.marron}"/>` +
    `<path d="M34 18 q-2-9 1-12 q4 4 3 12z" fill="${C.marron}"/>` +
    `<path d="M40 19 q1-6 2-8 q1 4 0 8z" fill="${C.rosa}"/>` +
    `<ellipse cx="31" cy="40" rx="6" ry="7" fill="${C.crema}"/>` +
    `<circle cx="31" cy="41" r="3.2" fill="${C.marronOsc}" opacity=".55"/>` +
    `<circle cx="41" cy="24" r="1.9" fill="${C.negro}"/>` +
    `<ellipse cx="47" cy="27" rx="2.4" ry="1.8" fill="${C.negro}"/>` +
    `<path d="M22 50 q8 2 14 0" stroke="${C.marronOsc}" stroke-width="1.6" opacity=".5"/>`);

  A.lion = svg(
    `<circle cx="32" cy="32" r="22" fill="${C.naranja}"/>` +
    `<g fill="${C.marron}">` +
    Array.from({length:12}, (_, i) => {
      const a = (i / 12) * Math.PI * 2, x = 32 + Math.cos(a) * 22, y = 32 + Math.sin(a) * 22;
      return `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="6"/>`;
    }).join('') + '</g>' +
    `<circle cx="32" cy="32" r="15" fill="${C.amarillo}"/>` +
    `<ellipse cx="32" cy="36" rx="7" ry="5.5" fill="${C.crema}"/>` +
    `<path d="M29 34 h6 l-3 3z" fill="${C.negro}"/>` +
    `<path d="M32 37 q-3 3-5 1 M32 37 q3 3 5 1" stroke="${C.negro}" stroke-width="1.4"/>` +
    `<circle cx="26" cy="29" r="2" fill="${C.negro}"/><circle cx="38" cy="29" r="2" fill="${C.negro}"/>`);

  A.panda = svg(
    `<circle cx="17" cy="18" r="7" fill="${C.negro}"/><circle cx="47" cy="18" r="7" fill="${C.negro}"/>` +
    `<circle cx="32" cy="34" r="20" fill="${C.blanco}" stroke="${C.gris}" stroke-width="1.2"/>` +
    `<ellipse cx="23" cy="31" rx="6" ry="7.5" fill="${C.negro}" transform="rotate(-18 23 31)"/>` +
    `<ellipse cx="41" cy="31" rx="6" ry="7.5" fill="${C.negro}" transform="rotate(18 41 31)"/>` +
    `<circle cx="23.5" cy="31.5" r="2.2" fill="${C.blanco}"/><circle cx="40.5" cy="31.5" r="2.2" fill="${C.blanco}"/>` +
    `<ellipse cx="32" cy="41" rx="3.4" ry="2.6" fill="${C.negro}"/>` +
    `<path d="M32 44 q-4 3-6 1 M32 44 q4 3 6 1" stroke="${C.negro}" stroke-width="1.5"/>`);

  A.parrot = svg(
    `<path d="M34 52 q6 6 6 10 q-8-1-11-8z" fill="${C.azul}"/>` +
    `<path d="M30 50 q2 8 0 12 q-7-4-7-11z" fill="${C.amarillo}"/>` +
    `<path d="M36 10 q14 3 14 20 q0 18-14 24 q-14-4-14-22 q0-19 14-22z" fill="${C.verde}"/>` +
    `<path d="M36 28 q11 3 12 14 q-6 8-13 6z" fill="${C.rojo}"/>` +
    `<path d="M36 10 q10 2 12 8 q-7-2-12-2z" fill="${C.amarillo}"/>` +
    `<path d="M23 20 q-7 2-7 7 q0 5 7 4 q-3-5 0-11z" fill="${C.naranja}"/>` +
    `<path d="M23 24 q-4 2-3 5" stroke="${C.marron}" stroke-width="1.4"/>` +
    `<circle cx="30" cy="21" r="2.4" fill="${C.negro}"/>` +
    `<circle cx="30.8" cy="20.2" r="0.8" fill="${C.blanco}"/>`);

  A.penguin = svg(
    `<ellipse cx="32" cy="34" rx="17" ry="22" fill="${C.negro}"/>` +
    `<ellipse cx="32" cy="38" rx="11" ry="16" fill="${C.blanco}"/>` +
    `<ellipse cx="32" cy="20" rx="12" ry="12" fill="${C.negro}"/>` +
    `<path d="M22 20 q10-8 20 0 q-4 8-10 8 q-6 0-10-8z" fill="${C.blanco}"/>` +
    `<path d="M28 23 l8 0 l-4 5z" fill="${C.naranja}"/>` +
    `<circle cx="27" cy="19" r="1.8" fill="${C.negro}"/><circle cx="37" cy="19" r="1.8" fill="${C.negro}"/>` +
    `<path d="M22 54 q-6 3-8 2 q3-4 8-5z" fill="${C.naranja}"/>` +
    `<path d="M42 54 q6 3 8 2 q-3-4-8-5z" fill="${C.naranja}"/>`);

  A.shark = svg(
    `<path d="M4 38 q12-18 34-18 q14 0 22 12 q-10 10-24 12 q-16 2-32-6z" fill="${C.gris}"/>` +
    `<path d="M6 38 q12 4 28 3 q-2 6-10 7 q-12 0-18-10z" fill="${C.blanco}" opacity=".85"/>` +
    `<path d="M30 20 q2-12 8-14 q-1 8 2 14z" fill="${C.grisOsc}"/>` +
    `<path d="M4 38 q-3 6-2 12 q6-4 8-9z" fill="${C.gris}"/>` +
    `<path d="M44 34 q8 1 14 3 q-8 3-14 2z" fill="${C.blanco}"/>` +
    `<path d="M45 36 l3 3 M50 36 l3 3 M55 36 l2 2" stroke="${C.grisOsc}" stroke-width="1.2"/>` +
    `<circle cx="47" cy="28" r="1.9" fill="${C.negro}"/>`);

  A.snail = svg(
    `<path d="M8 52 q0-8 8-9 q6-1 9-4" stroke="${C.verdeClaro}" stroke-width="9" stroke-linecap="round"/>` +
    `<path d="M25 39 q-2-8 3-12 q6-5 12-1 q7 5 5 14 q-2 10-13 12 q-9 1-12-5" fill="${C.amarillo}" stroke="${C.marron}" stroke-width="2.4"/>` +
    `<path d="M31 38 q-1-5 3-7 q5-2 7 3 q2 6-4 8 q-5 1-6-4" fill="none" stroke="${C.marron}" stroke-width="2.2"/>` +
    `<path d="M12 45 l-2-8 M18 43 l1-8" stroke="${C.verde}" stroke-width="2.4"/>` +
    `<circle cx="10" cy="35" r="2.4" fill="${C.negro}"/>` +
    `<circle cx="19" cy="34" r="2.4" fill="${C.negro}"/>` +
    `<path d="M8 52 h18" stroke="${C.verde}" stroke-width="2" opacity=".5"/>`);

  A.whale = svg(
    `<path d="M6 36 q6-16 26-16 q22 0 26 14 q2 8-8 12 q-20 6-36-2 q-8-4-8-8z" fill="${C.azul}"/>` +
    `<path d="M8 40 q14 8 34 4 q-2 6-12 8 q-16 1-22-12z" fill="${C.azulClaro}"/>` +
    `<path d="M56 34 q6-8 6-16 q-10 4-12 12z" fill="${C.azul}"/>` +
    `<path d="M28 20 q0-8 2-12 q4 6 3 12z" fill="${C.azulClaro}" opacity=".9"/>` +
    `<path d="M24 8 q-4 4-3 8 M34 8 q4 4 3 8" stroke="${C.azulClaro}" stroke-width="2.4"/>` +
    `<circle cx="17" cy="32" r="2" fill="${C.negro}"/>` +
    `<path d="M8 38 q5 1 9 0" stroke="${C.azulOsc}" stroke-width="1.6"/>`);

  // ================= MOVERS 2 · el tiempo ===============================
  const sol = (cx, cy, r) =>
    `<g stroke="${C.amarillo}" stroke-width="3">` +
    Array.from({length:8}, (_, i) => {
      const a = (i/8)*Math.PI*2;
      return `<path d="M${(cx+Math.cos(a)*(r+3)).toFixed(1)} ${(cy+Math.sin(a)*(r+3)).toFixed(1)} L${(cx+Math.cos(a)*(r+8)).toFixed(1)} ${(cy+Math.sin(a)*(r+8)).toFixed(1)}"/>`;
    }).join('') + '</g>' +
    `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${C.amarillo}"/>`;

  // Las nubes no pueden ser blancas: el lienzo tambien lo es y desaparecen.
  // Van en gris azulado con borde, que ademas las separa entre si.
  const nube = (cx, cy, s, col) =>
    `<g transform="translate(${cx} ${cy}) scale(${s})" fill="${col||'#dbe4ee'}" ` +
    `stroke="#b6c6d6" stroke-width="${(1.6/s).toFixed(2)}">` +
    `<path d="M-18 11 a8 8 0 0 1 0-16 a11 11 0 0 1 18-8 a10 10 0 0 1 15 8 ` +
    `a8 8 0 0 1 3 16 z"/></g>`;

  A.weather = svg(
    sol(24, 22, 10) +
    nube(38, 36, 1.15) +
    `<path d="M28 50 l-3 8 M38 50 l-3 8 M48 50 l-3 8" stroke="${C.azul}" stroke-width="3.2"/>`);

  A.sunny = svg(sol(32, 32, 15));

  A.rainy = svg(
    nube(32, 26, 1.25, '#c9d4de') +
    `<path d="M20 44 l-3 9 M30 44 l-3 9 M40 44 l-3 9 M50 45 l-3 8" stroke="${C.azul}" stroke-width="3.4"/>`);

  A.cloudy = svg(
    nube(26, 24, 0.85, '#eef3f8') +
    nube(35, 37, 1.15) +
    `<path d="M18 52 h28" stroke="#b6c6d6" stroke-width="2.4" opacity=".55"/>`);

  A.windy = svg(
    nube(30, 22, 1.0, '#e3eaf1') +
    `<g stroke="${C.azul}" stroke-width="3.4" fill="none">` +
    `<path d="M10 38 h30 q7 0 7-5 q0-5-5-5"/>` +
    `<path d="M14 48 h26 q7 0 7 5 q0 5-5 5"/>` +
    `<path d="M18 43 h20"/></g>`);

  A.snowy = svg(
    nube(32, 26, 1.2) +
    `<g stroke="${C.azul}" stroke-width="2.4" opacity=".95">` +
    `<g transform="translate(20 49)"><path d="M0 -5 v10 M-4.3 -2.5 l8.6 5 M-4.3 2.5 l8.6 -5"/></g>` +
    `<g transform="translate(33 53)"><path d="M0 -5 v10 M-4.3 -2.5 l8.6 5 M-4.3 2.5 l8.6 -5"/></g>` +
    `<g transform="translate(46 48)"><path d="M0 -5 v10 M-4.3 -2.5 l8.6 5 M-4.3 2.5 l8.6 -5"/></g></g>`);

  A.hot = svg(
    `<rect x="26" y="8" width="12" height="34" rx="6" fill="${C.blanco}" stroke="${C.grisOsc}" stroke-width="2.2"/>` +
    `<rect x="29" y="20" width="6" height="22" fill="${C.rojo}"/>` +
    `<circle cx="32" cy="48" r="9" fill="${C.rojo}" stroke="${C.grisOsc}" stroke-width="2.2"/>` +
    `<path d="M42 14 h7 M42 22 h7 M42 30 h7" stroke="${C.grisOsc}" stroke-width="2"/>` +
    sol(13, 15, 6));

  A.cold = svg(
    `<rect x="26" y="8" width="12" height="34" rx="6" fill="${C.blanco}" stroke="${C.grisOsc}" stroke-width="2.2"/>` +
    `<rect x="29" y="34" width="6" height="8" fill="${C.azul}"/>` +
    `<circle cx="32" cy="48" r="9" fill="${C.azul}" stroke="${C.grisOsc}" stroke-width="2.2"/>` +
    `<path d="M42 14 h7 M42 22 h7 M42 30 h7" stroke="${C.grisOsc}" stroke-width="2"/>` +
    `<g stroke="${C.azulClaro}" stroke-width="2.4" transform="translate(13 16)">` +
    `<path d="M0 -7 v14 M-6 -3.5 l12 7 M-6 3.5 l12 -7"/></g>`);

  A.rainbow = svg(
    `<g fill="none" stroke-width="5">` +
    `<path d="M6 50 a26 26 0 0 1 52 0" stroke="${C.rojo}"/>` +
    `<path d="M11 50 a21 21 0 0 1 42 0" stroke="${C.naranja}"/>` +
    `<path d="M16 50 a16 16 0 0 1 32 0" stroke="${C.amarillo}"/>` +
    `<path d="M21 50 a11 11 0 0 1 22 0" stroke="${C.verde}"/>` +
    `<path d="M26 50 a6 6 0 0 1 12 0" stroke="${C.azul}"/></g>` +
    nube(10, 50, 0.62, C.blanco) + nube(54, 50, 0.62, C.blanco));

  // ================= FLYERS 1 · ropa y equipaje =========================
  A.umbrella = svg(
    `<path d="M6 34 q0-22 26-22 q26 0 26 22 q-7-6-13 0 q-6-6-13 0 q-7-6-13 0 q-6-6-13 0z" fill="${C.rojo}"/>` +
    `<path d="M32 12 q-8 6-8 22 M32 12 q8 6 8 22" stroke="${C.blanco}" stroke-width="1.8" opacity=".7"/>` +
    `<path d="M32 34 v16 q0 6-6 6 q-5 0-5-4" stroke="${C.grisOsc}" stroke-width="3"/>` +
    `<circle cx="32" cy="11" r="2.4" fill="${C.grisOsc}"/>`);

  A.gloves = svg(
    `<g fill="${C.azul}">` +
    `<path d="M12 54 q-4 0-4-4 l0-18 q0-4 4-4 q3 0 3 4 l0-10 q0-4 3-4 q3 0 3 4 l0 10 l0-8 q0-4 3-4 q3 0 3 4 l0 22 q0 8-8 8z"/>` +
    `<g transform="translate(30 0)">` +
    `<path d="M12 54 q-4 0-4-4 l0-18 q0-4 4-4 q3 0 3 4 l0-10 q0-4 3-4 q3 0 3 4 l0 10 l0-8 q0-4 3-4 q3 0 3 4 l0 22 q0 8-8 8z"/></g></g>` +
    `<rect x="7" y="46" width="20" height="6" rx="3" fill="${C.azulOsc}"/>` +
    `<rect x="37" y="46" width="20" height="6" rx="3" fill="${C.azulOsc}"/>`);

  A.belt = svg(
    `<rect x="4" y="26" width="56" height="13" rx="4" fill="${C.marronOsc}"/>` +
    `<rect x="24" y="22" width="19" height="21" rx="3" fill="${C.amarillo}" stroke="${C.marron}" stroke-width="1.6"/>` +
    `<rect x="29" y="27" width="9" height="11" rx="1.5" fill="${C.crema}"/>` +
    `<path d="M33 27 v11" stroke="${C.marron}" stroke-width="2.4"/>` +
    `<g fill="${C.marron}"><circle cx="12" cy="32.5" r="1.8"/><circle cx="18" cy="32.5" r="1.8"/></g>`);

  A.pocket = svg(
    `<path d="M8 6 h48 v52 h-48 z" fill="${C.azul}"/>` +
    `<path d="M8 6 h48 v6 h-48 z" fill="${C.azulOsc}"/>` +
    `<path d="M20 20 h24 v18 q0 10-12 12 q-12-2-12-12 z" fill="${C.azulOsc}"/>` +
    `<path d="M20 20 h24 v18 q0 10-12 12 q-12-2-12-12 z" fill="none" stroke="${C.amarillo}" stroke-width="1.8" stroke-dasharray="3 2.5"/>` +
    `<path d="M20 26 h24" stroke="${C.amarillo}" stroke-width="1.6" stroke-dasharray="3 2.5"/>` +
    `<path d="M24 32 q8 5 16 0" stroke="${C.azulClaro}" stroke-width="2" opacity=".7"/>` +
    `<circle cx="44" cy="22" r="2.2" fill="${C.amarillo}"/>`);

  A.uniform = svg(
    `<path d="M22 12 l-14 6 l4 12 l6-2 l0 28 h28 l0-28 l6 2 l4-12 l-14-6 z" fill="${C.azul}"/>` +
    `<path d="M22 12 l10 12 l10-12 l-6-2 l-4 4 l-4-4z" fill="${C.blanco}"/>` +
    `<path d="M32 24 v32" stroke="${C.azulOsc}" stroke-width="1.6"/>` +
    `<g fill="${C.amarillo}"><circle cx="32" cy="32" r="1.8"/><circle cx="32" cy="40" r="1.8"/><circle cx="32" cy="48" r="1.8"/></g>` +
    `<path d="M40 16 l8 4 l-3 6" stroke="${C.rojo}" stroke-width="2.4"/>`);

  A.suitcase = svg(
    `<rect x="8" y="22" width="48" height="32" rx="4" fill="${C.marron}"/>` +
    `<rect x="8" y="22" width="48" height="32" rx="4" stroke="${C.marronOsc}" stroke-width="2"/>` +
    `<path d="M24 22 v-6 q0-4 4-4 h8 q4 0 4 4 v6" stroke="${C.grisOsc}" stroke-width="3.4"/>` +
    `<rect x="8" y="32" width="48" height="6" fill="${C.crema}" opacity=".9"/>` +
    `<rect x="27" y="30" width="10" height="10" rx="2" fill="${C.amarillo}" stroke="${C.marronOsc}" stroke-width="1.4"/>` +
    `<path d="M18 54 v3 M46 54 v3" stroke="${C.grisOsc}" stroke-width="3"/>`);

  A.ring = svg(
    `<circle cx="32" cy="40" r="16" fill="none" stroke="${C.amarillo}" stroke-width="6"/>` +
    `<circle cx="32" cy="40" r="16" fill="none" stroke="${C.naranja}" stroke-width="2" opacity=".5"/>` +
    `<path d="M32 8 l9 10 l-9 10 l-9-10 z" fill="${C.azulClaro}"/>` +
    `<path d="M32 8 l9 10 l-9 10 z" fill="${C.azul}"/>` +
    `<path d="M23 18 h18" stroke="${C.blanco}" stroke-width="1.6" opacity=".8"/>`);

  A.sunhat = svg(
    `<ellipse cx="32" cy="42" rx="28" ry="9" fill="${C.amarillo}"/>` +
    `<path d="M14 42 q0-24 18-24 q18 0 18 24 z" fill="${C.crema}"/>` +
    `<path d="M14 38 q18 6 36 0 l0 5 q-18 6-36 0z" fill="${C.rojo}"/>` +
    `<ellipse cx="32" cy="42" rx="28" ry="9" fill="none" stroke="${C.naranja}" stroke-width="1.6" opacity=".6"/>`);

  A.scarf = svg(
    `<path d="M14 10 q18 12 36 0 l0 12 q-18 12-36 0z" fill="${C.rojo}"/>` +
    `<path d="M20 22 q6 4 12 3 l0 30 q0 4-6 4 q-6 0-6-4z" fill="${C.rojo}"/>` +
    `<path d="M20 48 h12 M20 42 h12" stroke="${C.blanco}" stroke-width="2.4" opacity=".85"/>` +
    `<path d="M14 16 q18 12 36 0" stroke="${C.blanco}" stroke-width="2.4" opacity=".6"/>` +
    `<path d="M20 56 l-2 5 M26 57 l0 5 M32 56 l2 5" stroke="${C.rojo}" stroke-width="2.4"/>`);

  A.socks = svg(
    `<path d="M14 8 h12 v26 q0 4 4 6 l6 4 q5 3 2 8 q-3 5-8 2 l-12-7 q-4-3-4-9z" fill="${C.azul}"/>` +
    `<path d="M14 8 h12 v7 h-12z" fill="${C.rojo}"/>` +
    `<g transform="translate(22 6)">` +
    `<path d="M14 8 h12 v26 q0 4 4 6 l6 4 q5 3 2 8 q-3 5-8 2 l-12-7 q-4-3-4-9z" fill="${C.azulClaro}"/>` +
    `<path d="M14 8 h12 v7 h-12z" fill="${C.rojo}"/></g>`);

  // ================= FLYERS 2 · lugares de la ciudad ====================
  A.museum = svg(
    `<path d="M6 24 l26-14 l26 14 z" fill="${C.rojo}"/>` +
    edificio({y:24, h:30, x:8, w:48, cuerpo:C.crema}) +
    `<g fill="${C.crema}" stroke="${C.gris}" stroke-width="1.2">` +
    `<rect x="13" y="28" width="6" height="24" rx="2"/><rect x="24" y="28" width="6" height="24" rx="2"/>` +
    `<rect x="35" y="28" width="6" height="24" rx="2"/><rect x="46" y="28" width="6" height="24" rx="2"/></g>` +
    `<rect x="6" y="24" width="52" height="4" fill="${C.grisOsc}" opacity=".25"/>`);

  A.theatre = svg(
    edificio({y:18, h:36, x:10, w:44, cuerpo:'#7c3b52'}) +
    `<path d="M14 22 q18-8 36 0 l0 6 q-18-8-36 0z" fill="${C.amarillo}"/>` +
    `<path d="M18 54 v-18 q14-8 28 0 v18z" fill="#5d2b3d"/>` +
    `<path d="M32 36 v18" stroke="${C.amarillo}" stroke-width="2"/>` +
    `<g fill="${C.amarillo}"><circle cx="21" cy="30" r="2"/><circle cx="32" cy="28" r="2"/><circle cx="43" cy="30" r="2"/></g>` +
    `<path d="M24 12 l3 5 l5 1 l-4 4 l1 5 l-5-3 l-5 3 l1-5 l-4-4 l5-1z" fill="${C.amarillo}"/>`);

  A.castle = svg(
    `<path d="M8 54 v-26 h6 v-6 h6 v6 h8 v-6 h6 v6 h8 v-6 h6 v6 h6 v26z" fill="${C.gris}"/>` +
    `<path d="M22 54 v-16 q10-8 20 0 v16z" fill="${C.grisOsc}"/>` +
    `<path d="M32 38 v16" stroke="${C.gris}" stroke-width="1.6"/>` +
    `<g fill="${C.azulClaro}"><rect x="14" y="34" width="6" height="8" rx="3"/><rect x="44" y="34" width="6" height="8" rx="3"/></g>` +
    `<path d="M50 22 v-12 l10 4 l-10 4" fill="${C.rojo}" stroke="${C.grisOsc}" stroke-width="1.4"/>` +
    `<rect x="6" y="52" width="52" height="4" rx="1.5" fill="${C.grisOsc}"/>`);

  A.stadium = svg(
    `<ellipse cx="32" cy="34" rx="27" ry="19" fill="${C.verde}"/>` +
    `<ellipse cx="32" cy="34" rx="19" ry="12" fill="none" stroke="${C.blanco}" stroke-width="2"/>` +
    `<path d="M32 22 v24" stroke="${C.blanco}" stroke-width="2"/>` +
    `<circle cx="32" cy="34" r="4" fill="none" stroke="${C.blanco}" stroke-width="2"/>` +
    `<path d="M5 34 a27 19 0 0 1 54 0 l0 8 a27 19 0 0 1-54 0z" fill="${C.azul}" opacity=".55"/>` +
    `<g stroke="${C.grisOsc}" stroke-width="2.4">` +
    `<path d="M10 18 v-8 M54 18 v-8"/></g>` +
    `<g fill="${C.amarillo}"><circle cx="10" cy="9" r="3"/><circle cx="54" cy="9" r="3"/></g>`);

  A.airport = svg(
    `<path d="M4 40 l14-4 l10-16 q2-4 6-2 q3 2 1 6 l-5 10 l14-4 l4-8 q2-3 5-1 q2 2 1 5 l-2 6 l10-3 q4-1 5 2 q1 3-3 5 l-42 16 q-4 1-6-2 l-8-8z" fill="${C.azul}"/>` +
    `<path d="M18 36 l-8-8 l4-1 l9 7z" fill="${C.azulOsc}"/>` +
    `<g fill="${C.blanco}"><circle cx="24" cy="40" r="1.6"/><circle cx="30" cy="38" r="1.6"/><circle cx="36" cy="36" r="1.6"/></g>` +
    `<path d="M8 54 h48" stroke="${C.grisOsc}" stroke-width="3" stroke-dasharray="7 5"/>`);

  A.funfair = svg(
    `<circle cx="32" cy="30" r="22" fill="none" stroke="${C.rojo}" stroke-width="3"/>` +
    `<circle cx="32" cy="30" r="6" fill="${C.amarillo}"/>` +
    `<g stroke="${C.azul}" stroke-width="2.4">` +
    Array.from({length:8}, (_, i) => {
      const a = (i/8)*Math.PI*2;
      return `<path d="M32 30 L${(32+Math.cos(a)*22).toFixed(1)} ${(30+Math.sin(a)*22).toFixed(1)}"/>`;
    }).join('') + '</g>' +
    `<g fill="${C.verde}">` +
    Array.from({length:8}, (_, i) => {
      const a = (i/8)*Math.PI*2;
      return `<circle cx="${(32+Math.cos(a)*22).toFixed(1)}" cy="${(30+Math.sin(a)*22).toFixed(1)}" r="4"/>`;
    }).join('') + '</g>' +
    `<path d="M20 56 l12-14 l12 14z" fill="${C.grisOsc}"/>`);

  A["chemist's"] = svg(
    edificio({y:20, h:34, x:10, w:44, cuerpo:C.blanco}) +
    `<rect x="10" y="20" width="44" height="9" fill="${C.verde}"/>` +
    `<path d="M27 33 h10 v8 h8 v10 h-8 v8 h-10 v-8 h-8 v-10 h8z" fill="${C.verde}"/>` +
    `<rect x="10" y="20" width="44" height="34" rx="2" fill="none" stroke="${C.gris}" stroke-width="1.4"/>`);

  A.bridge = svg(
    `<path d="M2 44 q14-26 30-26 q16 0 30 26" fill="none" stroke="${C.rojo}" stroke-width="4"/>` +
    `<rect x="2" y="42" width="60" height="6" rx="2" fill="${C.grisOsc}"/>` +
    `<g stroke="${C.rojo}" stroke-width="2">` +
    `<path d="M12 42 v-9 M22 42 v-15 M32 42 v-18 M42 42 v-15 M52 42 v-9"/></g>` +
    `<rect x="8" y="48" width="7" height="12" fill="${C.gris}"/>` +
    `<rect x="49" y="48" width="7" height="12" fill="${C.gris}"/>` +
    `<path d="M2 56 q16 5 30 0 q14-5 30 0" stroke="${C.azulClaro}" stroke-width="2.4" opacity=".8"/>`);

  A["police station"] = svg(
    edificio({y:22, h:32, x:8, w:48, cuerpo:'#3e5c80'}) +
    `<rect x="8" y="22" width="48" height="8" fill="${C.azulOsc}"/>` +
    `<path d="M32 32 l7 3 v8 q0 7-7 10 q-7-3-7-10 v-8z" fill="${C.amarillo}"/>` +
    `<path d="M32 36 l2 4 h-4z" fill="${C.azulOsc}"/>` +
    `<g fill="${C.azulClaro}"><rect x="13" y="36" width="7" height="7" rx="1.5"/><rect x="44" y="36" width="7" height="7" rx="1.5"/></g>` +
    `<circle cx="32" cy="18" r="4" fill="${C.rojo}"/>` +
    `<path d="M28 18 h8" stroke="${C.azulOsc}" stroke-width="2"/>`);

  A.restaurant = svg(
    `<path d="M14 8 v20 q0 5 5 6 l0 22 q0 4 4 4 q4 0 4-4 l0-22 q5-1 5-6 v-20" stroke="${C.grisOsc}" stroke-width="3"/>` +
    `<path d="M20 8 v14 M27 8 v14" stroke="${C.grisOsc}" stroke-width="2.4"/>` +
    `<path d="M46 8 q8 4 8 16 q0 8-5 10 l0 22 q0 4-3 4 q-3 0-3-4z" fill="${C.grisOsc}"/>` +
    `<ellipse cx="32" cy="58" rx="26" ry="4" fill="${C.crema}"/>`);

  /* Alias de otros idiomas. El dibujo NO cambia con el idioma: cambia la palabra
     que lo nombra. Asi la version francesa reutiliza el arte ingles sin duplicar
     un solo SVG, y una palabra sin alias simplemente no dibuja (como ya pasa en
     ingles con las que no tienen arte). */
  const ALIAS = {
    'ballon':'ball', 'cerf-volant':'kite', 'cerf volant':'kite', 'voiture':'car',
    'nounours':'teddy', 'ours en peluche':'teddy', 'poupee':'doll', 'poupée':'doll',
    'rouge':'red', 'bleu':'blue', 'bleue':'blue', 'vert':'green', 'verte':'green',
    'jaune':'yellow', 'orange':'orange', 'noir':'black', 'noire':'black',
    'marron':'brown', 'pomme':'apple', 'banane':'banana', 'grenouille':'frog',
    'carotte':'carrot', 'mer':'sea', 'nuit':'night',
    'bonjour':'hello', 'salut':'hello', 'au revoir':'goodbye', 'les nombres':'numbers',
    'un':'one', 'deux':'two', 'trois':'three', 'quatre':'four', 'cinq':'five',
    'six':'six', 'sept':'seven', 'huit':'eight', 'neuf':'nine', 'dix':'ten'
  };

  // ---- API ---------------------------------------------------------------
  return {
    get(word) {
      if (!word) return null;
      const k = String(word).toLowerCase().trim();
      return A[k] || A[ALIAS[k]] || null;
    },
    /* La clave inglesa con la que se archiva el dibujo. La usa el motor para
       pedir el PNG: los archivos se llaman en ingles y no se renombran por
       traducir el curso. */
    base(word) {
      const k = String(word || '').toLowerCase().trim();
      return ALIAS[k] || k;
    },
    has(word) { return !!this.get(word); },
    count: Object.keys(A).length
  };
})();
