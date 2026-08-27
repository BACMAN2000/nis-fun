/* Escenas de apertura de unidad — Fun for Nordic.
 *
 * Las fotos del campus no pueden ilustrar una historia que pasa en el zoo o
 * en un museo. Estas escenas se dibujan a medida para cada unidad y, ademas,
 * se montan con los MISMOS dibujos del vocabulario (vocab-art.js): el alumno
 * reconoce en la ilustracion las palabras que acaba de aprender.
 *
 * Uso:  UNIT_SCENES.get('flyers', 1)  ->  SVG panoramico, o null si esa
 *       unidad todavia no tiene escena propia (el motor cae entonces a la
 *       foto del campus de sceneFor()).
 */
window.UNIT_SCENES = (function () {
  const W = 320, H = 180;

  const P = {
    cielo:'#cfe4f5', cieloGris:'#b9c8d6', sol:'#f2c14e',
    suelo:'#8ecfa8', suelo2:'#6fbf92', tierra:'#c9a06a',
    agua:'#7fb6dd', aguaOsc:'#4a8ec4', pared:'#f7ead6', paredOsc:'#e6d4b8',
    madera:'#a9713f', maderaOsc:'#6b4423', gris:'#8b98a5', grisOsc:'#5a6672',
    azul:'#4987c6', rojo:'#e0574a', verde:'#3fa06a', blanco:'#fff', negro:'#33373d'
  };

  // Coloca un dibujo del vocabulario dentro de la escena.
  // Los iconos vienen en lienzo 64x64, asi que basta trasladar y escalar.
  function pieza(word, x, y, s, rot) {
    const art = (window.VOCAB_ART && VOCAB_ART.get(word)) || null;
    if (!art) return '';
    const inner = art.replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '');
    const r = rot ? ` rotate(${rot} 32 32)` : '';
    return `<g transform="translate(${x} ${y}) scale(${s})${r}">${inner}</g>`;
  }

  const marco = (inner) =>
    `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" ` +
    `fill="none" stroke-linecap="round" stroke-linejoin="round" ` +
    `role="img">${inner}</svg>`;

  const S = {};

  // ---- STARTERS 1 · la caja de juguetes de Freya se vuelca --------------
  S['starters/1'] = marco(
    `<rect width="${W}" height="${H}" fill="#fdf6ea"/>` +
    `<rect y="118" width="${W}" height="62" fill="#e8d9c2"/>` +
    `<ellipse cx="160" cy="150" rx="128" ry="26" fill="#d9c3a5" opacity=".55"/>` +
    // caja volcada
    `<path d="M28 150 l6-44 h58 l6 44z" fill="${P.madera}"/>` +
    `<path d="M28 150 h70 v-8 h-70z" fill="${P.maderaOsc}"/>` +
    `<path d="M34 106 h58 l-8-16 h-42z" fill="#c08b52"/>` +
    `<text x="63" y="132" font-family="Baloo 2,system-ui" font-size="15" font-weight="800" ` +
    `fill="#fdf6ea" text-anchor="middle">TOYS</text>` +
    // los juguetes esparcidos
    pieza('ball', 96, 96, 0.95) +
    pieza('train', 140, 100, 1.0) +
    pieza('car', 196, 104, 0.85) +
    pieza('teddy', 240, 92, 1.05) +
    pieza('doll', 268, 102, 0.68) +
    pieza('kite', 176, 30, 0.9, 18) +
    `<path d="M186 88 q10 12 4 22" stroke="${P.grisOsc}" stroke-width="1.6"/>` +
    // manchas de color, que son las otras cuatro palabras
    `<circle cx="24" cy="34" r="11" fill="${P.rojo}" opacity=".85"/>` +
    `<circle cx="48" cy="24" r="9" fill="${P.azul}" opacity=".85"/>` +
    `<circle cx="70" cy="40" r="8" fill="${P.verde}" opacity=".85"/>` +
    `<circle cx="92" cy="26" r="10" fill="${P.sol}" opacity=".85"/>`);

  // ---- STARTERS 2 · Nico ensena la foto de su familia -------------------
  S['starters/2'] = marco(
    `<rect width="${W}" height="${H}" fill="#eef4fa"/>` +
    `<rect y="126" width="${W}" height="54" fill="#dfe8f2"/>` +
    // pizarra del aula al fondo
    `<rect x="14" y="18" width="86" height="60" rx="4" fill="#3d5a4a"/>` +
    `<rect x="14" y="18" width="86" height="60" rx="4" stroke="${P.madera}" stroke-width="5"/>` +
    `<path d="M26 42 h40 M26 54 h56 M26 66 h30" stroke="#fff" stroke-width="2.4" opacity=".65"/>` +
    // marco de la foto, grande y centrado
    `<rect x="118" y="16" width="186" height="126" rx="6" fill="${P.madera}"/>` +
    `<rect x="128" y="26" width="166" height="106" rx="3" fill="#fff"/>` +
    pieza('mother', 138, 40, 1.15) +
    pieza('father', 186, 40, 1.15) +
    pieza('sister', 236, 52, 1.0) +
    pieza('brother', 258, 54, 0.95) +
    pieza('baby', 208, 74, 0.85) +
    `<path d="M211 8 l16 10 l-16 10z" fill="${P.rojo}" opacity=".9"/>` +
    `<ellipse cx="211" cy="152" rx="96" ry="8" fill="#c9d6e4" opacity=".6"/>`);

  // ---- MOVERS 1 · el Club del Fiordo llega al zoo -----------------------
  S['movers/1'] = marco(
    `<rect width="${W}" height="${H}" fill="#d6ecf7"/>` +
    `<circle cx="272" cy="34" r="18" fill="${P.sol}"/>` +
    `<rect y="112" width="${W}" height="68" fill="${P.suelo}"/>` +
    `<path d="M0 112 q80-16 160 0 q80 16 160 0 v14 H0z" fill="${P.suelo2}"/>` +
    // arco de entrada del zoo
    `<path d="M18 112 v-52 q0-14 14-14 h28" stroke="${P.madera}" stroke-width="7"/>` +
    `<path d="M302 112 v-52 q0-14-14-14 h-28" stroke="${P.madera}" stroke-width="7"/>` +
    `<rect x="96" y="26" width="128" height="30" rx="6" fill="${P.verde}"/>` +
    `<text x="160" y="48" font-family="Baloo 2,system-ui" font-size="19" font-weight="800" ` +
    `fill="#fff" text-anchor="middle">ZOO</text>` +
    // vallas
    `<g stroke="${P.maderaOsc}" stroke-width="3" opacity=".55">` +
    `<path d="M0 112 h320 M40 100 v22 M120 100 v22 M200 100 v22 M280 100 v22"/></g>` +
    // los animales de la unidad
    pieza('panda', 26, 84, 1.05) +
    pieza('lion', 88, 82, 1.15) +
    pieza('kangaroo', 154, 80, 1.15) +
    pieza('penguin', 224, 90, 0.95) +
    pieza('parrot', 246, 66, 0.85) +
    `<path d="M262 76 q-10 4-18 2" stroke="${P.madera}" stroke-width="3"/>` +
    pieza('snail', 8, 128, 0.85));

  // ---- MOVERS 2 · sabado de lluvia y sol junto al fiordo ----------------
  S['movers/2'] = marco(
    `<defs><linearGradient id="us_cielo" x1="0" y1="0" x2="1" y2="0">` +
    `<stop offset="0" stop-color="#9fb3c4"/><stop offset="1" stop-color="#cfe4f5"/>` +
    `</linearGradient></defs>` +
    `<rect width="${W}" height="${H}" fill="url(#us_cielo)"/>` +
    // montanas del fiordo
    `<path d="M0 118 l52-56 l34 34 l40-44 l46 50 l38-30 l60 46z" fill="#8aa4b8"/>` +
    `<path d="M52 62 l14 15 h-28z M172 62 l12 14 h-24z" fill="#fff" opacity=".9"/>` +
    // agua
    `<rect y="118" width="${W}" height="62" fill="${P.agua}"/>` +
    `<path d="M0 132 q30 6 60 0 q30-6 60 0 q30 6 60 0 q30-6 60 0 q30 6 60 0" ` +
    `stroke="${P.aguaOsc}" stroke-width="2.4" opacity=".5"/>` +
    // orilla con el picnic
    `<path d="M0 152 q60-10 120-2 q60 8 120 0 q40-4 80 2 v28 H0z" fill="${P.suelo}"/>` +
    // el tiempo: lluvia a la izquierda, sol y arcoiris a la derecha
    pieza('rainy', 6, 8, 1.1) +
    pieza('windy', 62, 4, 0.95) +
    pieza('sunny', 250, 6, 1.15) +
    pieza('rainbow', 150, 46, 1.7) +
    pieza('umbrella', 24, 122, 0.85) +
    // manta de picnic
    `<path d="M196 168 l18-18 h44 l18 18z" fill="${P.rojo}" opacity=".85"/>` +
    `<path d="M206 158 h40 M214 150 l-8 18 M240 150 l8 18" stroke="#fff" stroke-width="2" opacity=".6"/>`);

  // ---- FLYERS 1 · maletas abiertas en la cocina del faro ----------------
  S['flyers/1'] = marco(
    `<rect width="${W}" height="${H}" fill="#f4efe6"/>` +
    // ventana con el faro al fondo
    `<rect x="212" y="14" width="92" height="66" rx="4" fill="#cfe4f5" stroke="${P.madera}" stroke-width="5"/>` +
    `<path d="M256 78 v-30 l6-14 l6 14 v30z" fill="#e7edf3"/>` +
    `<path d="M256 58 h12 M256 68 h12" stroke="${P.rojo}" stroke-width="4"/>` +
    `<circle cx="262" cy="36" r="5" fill="${P.sol}"/>` +
    `<path d="M212 66 q46-12 92 0 v14 h-92z" fill="${P.agua}"/>` +
    // mesa
    `<rect y="118" width="${W}" height="10" fill="${P.madera}"/>` +
    `<rect y="128" width="${W}" height="52" fill="#e8dcc8"/>` +
    // maleta abierta
    `<path d="M14 118 v-40 q0-6 6-6 h74 q6 0 6 6 v40z" fill="${P.maderaOsc}"/>` +
    `<rect x="20" y="80" width="74" height="38" fill="#d9c7a8"/>` +
    `<path d="M14 72 q-8-24 8-30 q10-4 14 4" stroke="${P.madera}" stroke-width="5"/>` +
    // la ropa de la unidad, dentro y alrededor
    pieza('uniform', 20, 74, 0.72) +
    pieza('scarf', 58, 74, 0.68) +
    pieza('gloves', 108, 76, 0.78) +
    pieza('sunhat', 152, 80, 0.78) +
    pieza('socks', 196, 84, 0.62) +
    pieza('suitcase', 232, 96, 0.8) +
    pieza('umbrella', 116, 22, 0.72) +
    pieza('belt', 156, 130, 0.7) +
    pieza('ring', 214, 136, 0.52));

  // ---- FLYERS 2 · el mapa de lugares de Diego y Maya --------------------
  S['flyers/2'] = marco(
    `<rect width="${W}" height="${H}" fill="#e4eff8"/>` +
    `<circle cx="34" cy="28" r="15" fill="${P.sol}"/>` +
    // rio que cruza la ciudad
    `<path d="M0 148 q60-12 120 0 q60 12 120 0 q40-8 80 2 v30 H0z" fill="${P.agua}"/>` +
    `<rect y="120" width="${W}" height="30" fill="#d3dfea"/>` +
    // los lugares de la unidad, como skyline
    pieza('museum', 8, 76, 1.0) +
    pieza('theatre', 66, 78, 0.95) +
    pieza('castle', 120, 66, 1.05) +
    pieza('stadium', 182, 80, 0.95) +
    pieza('restaurant', 240, 78, 0.85) +
    pieza('chemist\'s', 272, 86, 0.7) +
    pieza('bridge', 92, 108, 1.2) +
    pieza('airport', 224, 8, 0.85) +
    // calle
    `<path d="M0 120 h320" stroke="${P.grisOsc}" stroke-width="2.4" opacity=".45"/>` +
    `<path d="M8 134 h20 M44 134 h20 M80 134 h20 M228 134 h20 M264 134 h20 M300 134 h16" ` +
    `stroke="#fff" stroke-width="3" opacity=".8"/>`);

  return {
    get(level, unit) { return S[level + '/' + unit] || null; },
    has(level, unit) { return !!this.get(level, unit); },
    count: Object.keys(S).length
  };
})();
