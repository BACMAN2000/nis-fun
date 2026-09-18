/* The Magic Box — la clase de gramatica de Fun for Nordic, sin llamarse gramatica.
 *
 * Antes de la actividad de examen el alumno se encontraba con "Choose the
 * correct word" sin que nadie le hubiera ensenado la regla. Y ponerle un
 * titulo de gramatica a un nino de siete anos no sirve de nada: no sabe
 * que es un comparativo, y saberlo tampoco le ayuda a decirlo.
 *
 * Aqui la mascota abre su caja magica y DA LA CLASE como la daria una buena
 * profesora de primaria: un gancho, tres pasos que se ven y se oyen uno a
 * uno, la regla en una frase, un truco para acordarse y un mini-reto que
 * explica por que. Cada paso tiene su dibujo (la manzana es una manzana, el
 * bus es un bus, el reloj marca la hora que se dice) y lo que cambia en la
 * palabra aparece con rebote y brilla mientras la mascota lo dice.
 *
 * Movimiento a proposito: la caja se sacude y se abre, las tarjetas saltan
 * de dentro, la mascota se mueve al hablar y hay confeti al acertar. Es para
 * los ninos a los que hay que ganarles la atencion en los tres primeros
 * segundos. Con prefers-reduced-motion se queda todo quieto.
 *
 * Cada unidad cae en una familia segun lo que practica; hay 148 patrones
 * distintos en la serie y una clase por familia los cubre casi todos. Lo
 * que no encaja no ensena una caja vacia: no sale.
 *
 * Formato de un paso:
 *   di    la frase grande; lo que va entre [corchetes] es lo que se ensena
 *         y sale resaltado ("It is [an] apple"). Las familias viejas siguen
 *         con pal + fin y se convierten solas.
 *   nota  la linea corta bajo la frase.
 *   dice  lo que dice la profesora en ese paso (se oye y se lee en el
 *         bocadillo). Sin dice, lee la frase y la nota.
 *   arte  el dibujo, que tiene que ser LO QUE DICE LA FRASE.
 *
 * Uso:  MAGICBOX.para(ud)   -> {titulo, html, alMostrar} o null
 *       MAGICBOX.lineas()   -> todo lo que la profesora dice (para grabarlo)
 */
window.MAGICBOX = (function () {

  const CSS = `
  .mb{max-width:46rem;margin-inline:auto;width:100%;position:relative}
  /* la caja que se abre */
  .mb-cabeza{display:flex;justify-content:center;align-items:flex-end;gap:1rem;
    margin:-.2rem 0 -.5rem;position:relative;z-index:0}
  .mb-cofre{width:150px;height:82px;overflow:visible}
  .mb-cofre svg{overflow:visible;display:block}
  .mb-tapa,.mb-chispa,.mb-cofre-svg{transform-box:fill-box;transform-origin:center}
  .mb-tapa{transform-origin:2% 100%}
  .mb-cofre-svg{transform-origin:50% 90%}
  .mb.abierta .mb-cofre-svg{animation:mb-sacude .55s ease-in-out}
  @keyframes mb-sacude{20%{transform:rotate(-5deg)}40%{transform:rotate(5deg)}60%{transform:rotate(-4deg)}80%{transform:rotate(3deg)}}
  .mb.abierta .mb-tapa{animation:mb-tapa .8s cubic-bezier(.34,1.56,.64,1) .5s forwards}
  @keyframes mb-tapa{to{transform:translate(-5px,-16px) rotate(-22deg)}}
  .mb-chispa{opacity:0}
  .mb.abierta .mb-chispa{animation:mb-chispa 1.15s ease-out .75s forwards}
  @keyframes mb-chispa{0%{opacity:0;transform:translate(0,0) scale(.2)}
    30%{opacity:1;transform:translate(calc(var(--dx)*.45),calc(var(--dy)*.45)) scale(1.15)}
    100%{opacity:0;transform:translate(var(--dx),var(--dy)) scale(.3)}}
  .mb-ver{background:var(--accent);color:#fff;border:0;border-radius:999px;padding:.4rem 1rem;
    font-family:"Baloo 2",sans-serif;font-weight:700;font-size:.95rem;cursor:pointer;
    display:inline-flex;gap:.35rem;align-items:center;margin-bottom:.7rem;
    box-shadow:0 3px 0 rgba(0,0,0,.12);transition:transform .15s}
  .mb-ver:hover{transform:translateY(-2px)}
  .mb-ver.on{background:var(--ok)}
  .mb-ver.pide{animation:mb-late 1s ease-in-out infinite}
  /* las tres tarjetas */
  .mb-tira{display:flex;justify-content:center;align-items:stretch;gap:1rem;
    flex-wrap:wrap;margin:.2rem 0 .9rem;position:relative;z-index:1}
  .mb-paso{background:var(--surface2);border:2px solid transparent;border-radius:18px;
    padding:1rem .8rem .7rem;cursor:pointer;text-align:center;min-width:9rem;max-width:12.5rem;
    flex:1 1 9rem;position:relative;opacity:0;transform:translateY(34px) scale(.85);
    transition:border-color .2s,box-shadow .2s,background .2s}
  .mb.abierta .mb-paso{animation:mb-salta .55s cubic-bezier(.34,1.56,.64,1) forwards}
  .mb.abierta .mb-paso:nth-child(1){animation-delay:.9s}
  .mb.abierta .mb-paso:nth-child(2){animation-delay:1.05s}
  .mb.abierta .mb-paso:nth-child(3){animation-delay:1.2s}
  @keyframes mb-salta{to{opacity:1;transform:none}}
  .mb-paso:hover{border-color:var(--line)}
  .mb-paso.on{border-color:var(--accent);background:#fff;
    box-shadow:0 0 0 5px rgba(59,111,181,.14),0 10px 22px rgba(20,30,45,.12)}
  .mb-num{position:absolute;top:-.65rem;left:-.45rem;width:1.7rem;height:1.7rem;border-radius:50%;
    background:var(--soft);color:#fff;font-family:"Baloo 2",sans-serif;font-weight:800;
    font-size:.95rem;display:grid;place-items:center;box-shadow:0 2px 6px rgba(0,0,0,.15)}
  .mb-paso.on .mb-num{background:var(--accent);animation:mb-late .5s}
  .mb-arte{display:block;margin:0 auto .45rem;height:108px;width:auto;max-width:100%}
  .mb-paso.on .mb-arte{animation:mb-bota 1s ease-in-out infinite alternate}
  @keyframes mb-bota{from{transform:translateY(0)}to{transform:translateY(-7px)}}
  .mb-pal{font-family:"Baloo 2",sans-serif;font-weight:800;font-size:1.28rem;
    color:var(--ink);line-height:1.15;display:block}
  .mb-fin{display:inline-block;color:#b8471b;background:#fff2c9;border-radius:6px;padding:0 .2rem}
  .mb-paso.on .mb-fin{animation:mb-pop .55s cubic-bezier(.34,1.56,.64,1),
    mb-brilla 1.2s ease-in-out .55s infinite alternate}
  @keyframes mb-pop{from{transform:scale(.2);opacity:0}to{transform:scale(1);opacity:1}}
  @keyframes mb-brilla{from{box-shadow:0 0 0 2px #ffe08a}to{box-shadow:0 0 0 7px rgba(255,224,138,.22)}}
  .mb-nota{margin:.35rem 0 0;font-size:.9rem;color:var(--soft);min-height:1.2rem}
  /* la regla y el truco */
  .mb-regla{text-align:center;margin:0 auto .7rem;font-family:"Baloo 2",sans-serif;font-weight:700;
    font-size:1.08rem;color:var(--ink);background:linear-gradient(transparent 58%,#fff2c9 58%);
    display:table;padding:.1rem .6rem;border-radius:6px;cursor:pointer;border:0}
  .mb-regla.on{animation:mb-late .6s ease-in-out 2}
  @keyframes mb-late{50%{transform:scale(1.07)}}
  .mb-truco{display:flex;gap:.6rem;align-items:center;background:#fff;border:1.5px dashed var(--accent);
    border-radius:14px;padding:.55rem .85rem;margin:0 auto .8rem;max-width:36rem;width:100%;
    font-size:.95rem;color:var(--ink);cursor:pointer;text-align:left;font-family:inherit;line-height:1.4}
  .mb-truco .ico{font-size:1.35rem;flex:none}
  .mb-truco.on{animation:mb-late .6s ease-in-out 2;border-style:solid;background:#fffbea}
  /* el reto */
  .mb-reto{margin-top:.2rem;background:var(--surface2);border-radius:16px;padding:.9rem 1rem;
    text-align:center;position:relative;overflow:hidden;transition:box-shadow .3s}
  .mb-reto.on{box-shadow:0 0 0 4px rgba(59,111,181,.18)}
  .mb-reto p{margin:0 0 .6rem;font-weight:600}
  .mb-ops{display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap}
  .mb-op{background:#fff;border:1.5px solid var(--line);border-radius:999px;
    padding:.4rem 1rem;cursor:pointer;font-family:"Baloo 2",sans-serif;font-weight:700;
    color:var(--ink);transition:transform .15s}
  .mb-op:hover{transform:translateY(-2px)}
  .mb-op.pide{animation:mb-late 1.1s ease-in-out 3}
  .mb-op.bien{background:var(--ok);color:#fff;border-color:var(--ok);animation:mb-late .5s}
  .mb-op.mal{background:var(--bad);color:#fff;border-color:var(--bad);animation:mb-tiembla .4s}
  @keyframes mb-tiembla{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
  .mb-eco{margin:.55rem 0 0;font-weight:700;color:var(--ok);min-height:1.3rem}
  .mb-conf{position:absolute;top:45%;left:50%;width:9px;height:9px;border-radius:2px;opacity:0;
    pointer-events:none;animation:mb-conf .95s ease-out forwards}
  @keyframes mb-conf{0%{opacity:1;transform:translate(0,0) rotate(0)}
    100%{opacity:0;transform:translate(var(--dx),var(--dy)) rotate(320deg)}}
  /* la mascota se mueve mientras habla (translate/rotate no pisan el
     transform con el que miraHacia la gira) */
  .mb-habla .guia-mascota{animation:mb-mascota .5s ease-in-out infinite alternate}
  @keyframes mb-mascota{from{translate:0 0;rotate:-2deg}to{translate:0 -5px;rotate:2deg}}
  @media (max-width:560px){ .mb-paso{min-width:7.5rem;flex-basis:7.5rem} .mb-arte{height:92px} }
  @media (prefers-reduced-motion:reduce){
    .mb *,.mb-habla .guia-mascota{animation:none!important;transition:none!important}
    .mb-paso{opacity:1;transform:none} .mb-tapa{transform:translate(-5px,-16px) rotate(-22deg)} }`;

  /* ---------- paleta (la misma de vocab-art.js) ---------- */
  const P = {
    rojo:'#e0574a', naranja:'#ef8a3c', amarillo:'#f2c14e', verde:'#3fa06a', verdeClaro:'#8ecfa8',
    azul:'#4987c6', azulClaro:'#a9c6e4', azulOsc:'#2f5f92', rosa:'#e58fa8', morado:'#8f7bc4',
    marron:'#a9713f', marronOsc:'#6b4423', gris:'#8b98a5', grisOsc:'#5a6672',
    blanco:'#ffffff', negro:'#33373d', piel:'#f3c9a0', pielOsc:'#d9a273', crema:'#f7ead6',
    agua:'#bfe0f5', sombra:'rgba(20,30,45,.14)'
  };
  const FONT = 'font-family="Baloo 2, sans-serif" font-weight="800"';

  /* ---------- lienzo y piezas ---------- */
  const W = 128, H = 108;
  function lienzo(inner, w, h) {
    w = w || W; h = h || H;
    return `<svg class="mb-arte" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" aria-hidden="true" fill="none" stroke-linecap="round" stroke-linejoin="round">${inner}</svg>`;
  }
  const sombra = (cx, cy, rx) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${Math.max(3, rx * .16)}" fill="${P.sombra}"/>`;
  const grupo = (inner, x, y, s) => `<g transform="translate(${x} ${y})${s && s !== 1 ? ` scale(${s})` : ''}">${inner}</g>`;
  const s64 = inner => `<svg viewBox="0 0 64 64" fill="none" stroke-linecap="round" stroke-linejoin="round">${inner}</svg>`;

  // Mete un svg entero (propio o de VOCAB_ART) dentro del lienzo, en x,y y
  // con ese tamano. Quita width/height propios para que no se dupliquen.
  function pon(s, x, y, size) {
    if (!s) return '';
    return s.replace(/^<svg\s([^>]*)>/, (m, at) =>
      `<svg x="${x}" y="${y}" width="${size}" height="${size}" ${at.replace(/\s(width|height)="[^"]*"/g, '')}>`);
  }

  /* dibujos propios en 64x64; lo que no esta aqui se pide a vocab-art.js */
  const D = {
    apple: () => s64(`
      <path d="M32 16 q1 -8 8 -10" stroke="${P.marronOsc}" stroke-width="3"/>
      <path d="M33 14 q12 -8 14 4 q-12 4 -14 -4z" fill="${P.verde}"/>
      <path d="M32 21 c-6 -7 -19 -3 -19 12 c0 12 8 23 15 23 c2 0 3 -1 4 -1 c1 0 2 1 4 1 c7 0 15 -11 15 -23 c0 -15 -13 -19 -19 -12z" fill="${P.rojo}"/>
      <path d="M21 28 q-3 4 -2 10" stroke="${P.blanco}" stroke-width="2.5" opacity=".6"/>`),
    cake: () => s64(`
      <rect x="10" y="36" width="44" height="18" rx="4" fill="${P.rosa}"/>
      <rect x="15" y="24" width="34" height="14" rx="4" fill="${P.crema}"/>
      <path d="M15 27 q4 7 8.5 0 q4 7 8.5 0 q4 7 8.5 0 q4 7 8.5 0 v-5 h-34z" fill="${P.rojo}"/>
      <path d="M10 39 q5 7 11 0 q5 7 11 0 q5 7 11 0 q5 7 11 0 v-4 h-44z" fill="${P.blanco}"/>
      <rect x="30" y="10" width="4" height="14" rx="1" fill="${P.azul}"/>
      <ellipse cx="32" cy="7" rx="2.6" ry="4" fill="${P.amarillo}"/>`),
    fish: () => s64(`
      <path d="M12 32 q16 -18 34 0 q-18 18 -34 0z" fill="${P.naranja}"/>
      <path d="M44 32 l14 -11 v22z" fill="${P.naranja}"/>
      <path d="M30 24 q6 8 0 16" stroke="${P.rojo}" stroke-width="2" opacity=".7"/>
      <circle cx="21" cy="30" r="2.6" fill="${P.negro}"/>
      <path d="M24 38 q6 2 10 -1" stroke="${P.rojo}" stroke-width="2" opacity=".7"/>`),
    bus: () => s64(`
      <rect x="6" y="14" width="52" height="32" rx="6" fill="${P.amarillo}"/>
      <rect x="10" y="19" width="9" height="10" rx="2" fill="${P.azulClaro}"/>
      <rect x="22" y="19" width="9" height="10" rx="2" fill="${P.azulClaro}"/>
      <rect x="34" y="19" width="9" height="10" rx="2" fill="${P.azulClaro}"/>
      <rect x="46" y="19" width="8" height="10" rx="2" fill="${P.azulClaro}"/>
      <rect x="6" y="34" width="52" height="4" fill="${P.naranja}"/>
      <circle cx="18" cy="48" r="5.5" fill="${P.negro}"/><circle cx="46" cy="48" r="5.5" fill="${P.negro}"/>
      <circle cx="18" cy="48" r="2" fill="${P.gris}"/><circle cx="46" cy="48" r="2" fill="${P.gris}"/>`),
    bike: () => s64(`
      <circle cx="15" cy="42" r="11" stroke="${P.negro}" stroke-width="3"/>
      <circle cx="49" cy="42" r="11" stroke="${P.negro}" stroke-width="3"/>
      <path d="M15 42 L27 24 L42 24 L49 42 L32 42 Z" stroke="${P.rojo}" stroke-width="3"/>
      <path d="M27 24 L24 17 M20 17 h8" stroke="${P.negro}" stroke-width="3"/>
      <path d="M42 24 L45 16 M40 16 h9" stroke="${P.negro}" stroke-width="3"/>
      <circle cx="32" cy="42" r="3" fill="${P.negro}"/>`),
    feet: () => s64(`
      <path d="M6 44 h26 q8 0 8 -6 q-8 0 -13 -9 h-14 q-7 0 -7 7z" fill="${P.azul}"/>
      <rect x="6" y="43" width="34" height="5" rx="2" fill="${P.blanco}" stroke="${P.gris}" stroke-width="1.5"/>
      <path d="M17 33 l5 3 M19 30 l5 3" stroke="${P.blanco}" stroke-width="2"/>
      <g transform="translate(20 -14)">
        <path d="M6 44 h26 q8 0 8 -6 q-8 0 -13 -9 h-14 q-7 0 -7 7z" fill="${P.rojo}"/>
        <rect x="6" y="43" width="34" height="5" rx="2" fill="${P.blanco}" stroke="${P.gris}" stroke-width="1.5"/>
        <path d="M17 33 l5 3 M19 30 l5 3" stroke="${P.blanco}" stroke-width="2"/>
      </g>`),
    bed: () => s64(`
      <rect x="4" y="16" width="5" height="36" rx="2" fill="${P.marron}"/>
      <rect x="55" y="28" width="5" height="24" rx="2" fill="${P.marron}"/>
      <rect x="8" y="30" width="48" height="14" rx="3" fill="${P.azul}"/>
      <rect x="9" y="22" width="18" height="10" rx="4" fill="${P.blanco}" stroke="${P.gris}" stroke-width="1.5"/>
      <rect x="8" y="44" width="48" height="6" fill="${P.marronOsc}"/>`),
    homework: () => s64(`
      <rect x="12" y="8" width="36" height="46" rx="3" fill="${P.blanco}" stroke="${P.gris}" stroke-width="2"/>
      <path d="M18 20 h24 M18 28 h24 M18 36 h16 M18 44 h20" stroke="${P.azulClaro}" stroke-width="2.5"/>
      <path d="M38 52 l16 -24" stroke="${P.amarillo}" stroke-width="6"/>
      <path d="M54 28 l3 -5 -7 -3z" fill="${P.piel}"/>
      <path d="M36 55 l2 -3 5 3z" fill="${P.rosa}"/>`),
    football: () => s64(`
      <circle cx="32" cy="34" r="21" fill="${P.blanco}" stroke="${P.negro}" stroke-width="2"/>
      <path d="M32 22 l10 7 -4 11 h-12 l-4 -11z" fill="${P.negro}"/>
      <path d="M32 22 v-9 M42 29 l9 -4 M38 40 l6 9 M26 40 l-6 9 M22 29 l-9 -4" stroke="${P.negro}" stroke-width="2"/>`),
    house: () => s64(`
      <path d="M8 30 L32 10 L56 30z" fill="${P.rojo}"/>
      <rect x="13" y="30" width="38" height="24" fill="${P.crema}" stroke="${P.marron}" stroke-width="2"/>
      <rect x="27" y="38" width="10" height="16" fill="${P.marron}"/>
      <rect x="17" y="35" width="7" height="7" fill="${P.azulClaro}"/>
      <rect x="40" y="35" width="7" height="7" fill="${P.azulClaro}"/>`),
    zoo: () => s64(`
      <rect x="29" y="30" width="6" height="26" fill="${P.marron}"/>
      <rect x="8" y="12" width="48" height="22" rx="5" fill="${P.verde}"/>
      <text x="32" y="29" text-anchor="middle" font-size="16" ${FONT} fill="${P.blanco}">ZOO</text>`),
    bowl: () => s64(`
      <path d="M6 28 q26 38 52 0z" fill="${P.amarillo}"/>
      <ellipse cx="32" cy="28" rx="26" ry="7" fill="${P.crema}" stroke="${P.naranja}" stroke-width="2"/>
      <path d="M38 26 l14 -18" stroke="${P.marronOsc}" stroke-width="4"/>
      <ellipse cx="53" cy="7" rx="4.5" ry="3.5" fill="${P.marronOsc}"/>`),
    plateFull: () => s64(`
      <ellipse cx="32" cy="36" rx="27" ry="12" fill="${P.blanco}" stroke="${P.gris}" stroke-width="2"/>
      <ellipse cx="28" cy="33" rx="9" ry="5" fill="${P.verde}"/>
      <ellipse cx="39" cy="36" rx="8" ry="4.5" fill="${P.naranja}"/>
      <circle cx="23" cy="39" r="3.5" fill="${P.rojo}"/>`),
    plateEmpty: () => s64(`
      <ellipse cx="32" cy="36" rx="27" ry="12" fill="${P.blanco}" stroke="${P.gris}" stroke-width="2"/>
      <ellipse cx="32" cy="36" rx="18" ry="7" stroke="${P.azulClaro}" stroke-width="1.5"/>`),
  };
  const dibujo = n => D[n] ? D[n]() : ((window.VOCAB_ART && VOCAB_ART.get(n)) || '');

  /* marcas que se ponen encima de una escena: si, no, me gusta, pregunta... */
  function marca(tipo, x, y) {
    x = x == null ? 104 : x; y = y == null ? 22 : y;
    const t = { x: `<circle cx="${x}" cy="${y}" r="14" fill="${P.rojo}"/><path d="M${x - 7} ${y - 7} l14 14 M${x + 7} ${y - 7} l-14 14" stroke="${P.blanco}" stroke-width="4"/>`,
      ok: `<circle cx="${x}" cy="${y}" r="14" fill="${P.verde}"/><path d="M${x - 8} ${y} l6 6 l11 -12" stroke="${P.blanco}" stroke-width="4"/>`,
      corazon: `<path d="M${x} ${y + 12} l-12 -12 a7 7 0 0 1 12 -9 a7 7 0 0 1 12 9z" fill="${P.rojo}"/>`,
      pregunta: `<circle cx="${x}" cy="${y}" r="14" fill="${P.amarillo}"/><text x="${x}" y="${y + 7}" text-anchor="middle" font-size="21" ${FONT} fill="${P.negro}">?</text>`,
      ahora: `<path d="M${x} ${y - 17} l4 10 10 -6 -4 11 11 3 -11 4 4 11 -10 -6 -4 10 -4 -10 -10 6 4 -11 -11 -4 11 -3 -4 -11 10 6z" fill="${P.amarillo}"/><text x="${x}" y="${y + 4}" text-anchor="middle" font-size="10" ${FONT} fill="${P.negro}">NOW</text>`,
      notas: `<path d="M${x - 6} ${y + 10} v-16 l12 -3 v16" stroke="${P.negro}" stroke-width="2.5"/><ellipse cx="${x - 9}" cy="${y + 11}" rx="4" ry="3" fill="${P.negro}"/><ellipse cx="${x + 3}" cy="${y + 8}" rx="4" ry="3" fill="${P.negro}"/>`,
      zzz: `<text x="${x - 12}" y="${y + 8}" font-size="12" ${FONT} fill="${P.azulOsc}">z</text><text x="${x - 2}" y="${y}" font-size="15" ${FONT} fill="${P.azulOsc}">z</text><text x="${x + 10}" y="${y - 9}" font-size="18" ${FONT} fill="${P.azulOsc}">z</text>`,
      sol: `<circle cx="${x}" cy="${y}" r="9" fill="${P.amarillo}"/><path d="M${x} ${y - 16} v5 M${x} ${y + 11} v5 M${x - 16} ${y} h5 M${x + 11} ${y} h5 M${x - 11} ${y - 11} l3 3 M${x + 8} ${y + 8} l3 3 M${x + 11} ${y - 11} l-3 3 M${x - 8} ${y + 8} l-3 3" stroke="${P.amarillo}" stroke-width="3"/>`,
      lluvia: `<path d="M${x - 14} ${y + 2} a8 8 0 0 1 6 -13 a10 10 0 0 1 19 3 a7 7 0 0 1 1 13z" fill="${P.gris}"/><path d="M${x - 9} ${y + 10} l-3 8 M${x} ${y + 10} l-3 8 M${x + 9} ${y + 10} l-3 8" stroke="${P.azul}" stroke-width="2.5"/>`,
      pajaros: `<path d="M${x - 14} ${y} q6 -8 12 0 q6 -8 12 0" stroke="${P.negro}" stroke-width="2"/><path d="M${x - 4} ${y - 12} q5 -7 10 0 q5 -7 10 0" stroke="${P.negro}" stroke-width="2"/>`,
    };
    return t[tipo] || '';
  }

  /* un nino de Nordic en 96x108, con pose y cara. Es el mismo monigote para
     todas las escenas, para que la tira lea como una sola clase. */
  function kid(o) {
    o = o || {};
    const ropa = o.ropa || P.azul, pelo = o.pelo || 'chico';
    const pose = o.pose || 'de-pie', cara = o.cara || 'feliz';
    const hx = 48, hy = 26, r = 19, PELO = pelo === 'chica' ? P.marronOsc : P.marron;
    let s = '';
    s += `<circle cx="${hx}" cy="${hy - 3}" r="${r + 1}" fill="${PELO}"/>`;
    if (pelo === 'chica') s += `<circle cx="${hx - r - 3}" cy="${hy + 8}" r="8" fill="${PELO}"/><circle cx="${hx + r + 3}" cy="${hy + 8}" r="8" fill="${PELO}"/>`;
    s += `<circle cx="${hx}" cy="${hy}" r="${r}" fill="${P.piel}" stroke="${P.pielOsc}" stroke-width="1.6"/>`;
    if (pelo === 'chica') s += `<circle cx="${hx - 11}" cy="${hy - 15}" r="3.5" fill="${P.rosa}"/>`;
    if (cara === 'dormido') s += `<path d="M${hx - 10} ${hy - 2} q3 4 6 0 M${hx + 4} ${hy - 2} q3 4 6 0" stroke="${P.negro}" stroke-width="2"/>`;
    else if (cara === 'cansado') s += `<path d="M${hx - 10} ${hy - 2} h6 M${hx + 4} ${hy - 2} h6" stroke="${P.negro}" stroke-width="2.4"/>`;
    else s += `<circle cx="${hx - 7}" cy="${hy - 2}" r="2.6" fill="${P.negro}"/><circle cx="${hx + 7}" cy="${hy - 2}" r="2.6" fill="${P.negro}"/>`;
    const bocas = {
      feliz:   `<path d="M${hx - 7} ${hy + 6} q7 6 14 0" stroke="${P.negro}" stroke-width="2"/>`,
      triste:  `<path d="M${hx - 7} ${hy + 9} q7 -5 14 0" stroke="${P.negro}" stroke-width="2"/>`,
      cansado: `<path d="M${hx - 6} ${hy + 8} h12" stroke="${P.negro}" stroke-width="2"/><path d="M${hx + 23} ${hy - 12} q4 6 0 8 q-4 -2 0 -8z" fill="${P.azulClaro}"/>`,
      canta:   `<ellipse cx="${hx}" cy="${hy + 8}" rx="4" ry="5" fill="${P.negro}"/>`,
      grita:   `<ellipse cx="${hx}" cy="${hy + 9}" rx="7" ry="7" fill="${P.negro}"/><ellipse cx="${hx}" cy="${hy + 12}" rx="4" ry="3" fill="${P.rojo}"/>`,
      dormido: `<path d="M${hx - 5} ${hy + 7} q5 3 10 0" stroke="${P.negro}" stroke-width="2"/>`,
    };
    s += bocas[cara] || bocas.feliz;
    s += `<rect x="34" y="46" width="28" height="34" rx="9" fill="${ropa}"${ropa === P.blanco ? ` stroke="${P.gris}" stroke-width="1.5"` : ''}/>`;
    if (pose === 'patada') s += `<rect x="34" y="66" width="28" height="5" fill="${P.negro}"/>`;
    const brazo = (x1, y1, e) => `<path d="M${x1} ${y1} L${e[0]} ${e[1]}" stroke="${P.piel}" stroke-width="7"/>`;
    const pierna = (x1, y1, e) => `<path d="M${x1} ${y1} L${e[0]} ${e[1]}" stroke="${P.azulOsc}" stroke-width="7"/>`;
    const POSES = {
      'de-pie':       { L: [20, 70], R: [76, 70] },
      saluda:         { L: [20, 70], R: [80, 30] },
      brazos:         { L: [16, 30], R: [80, 30] },
      corre:          { L: [20, 42], R: [78, 64], piernas: [[28, 98], [72, 94]],
                        extra: o.lineas === false ? '' : `<path d="M4 58 h10 M0 68 h12 M4 78 h10" stroke="${P.gris}" stroke-width="2.5"/>` },
      senala:         { L: [20, 70], R: [92, 52] },
      'senala-lejos': { L: [20, 70], R: [86, 22] },
      sostiene:       { L: [38, 88], R: [58, 88] },
      agarra:         { L: [20, 70], R: [78, 88] },
      cansado:        { L: [30, 86], R: [66, 86] },
      patada:         { L: [26, 44], R: [74, 40], piernas: [[38, 100], [88, 64]] },
      sentado:        { L: [26, 82], R: [70, 82], sentado: true,
                        antes: `<rect x="28" y="84" width="40" height="6" rx="2" fill="${P.marron}"/><rect x="30" y="90" width="5" height="14" fill="${P.marron}"/><rect x="61" y="90" width="5" height="14" fill="${P.marron}"/>` },
    };
    const p = POSES[pose] || POSES['de-pie'];
    if (p.antes) s = p.antes + s;
    s += brazo(34, 52, p.L) + brazo(62, 52, p.R);
    if (p.sentado) s += `<path d="M42 78 L66 81 L66 102" stroke="${P.azulOsc}" stroke-width="7"/><path d="M54 78 L66 81" stroke="${P.azulOsc}" stroke-width="7"/>`;
    else { const pi = p.piernas || [[38, 100], [58, 100]]; s += pierna(40, 80, pi[0]) + pierna(56, 80, pi[1]); }
    if (p.extra) s += p.extra;
    return s;
  }

  /* ---------- escenas ---------- */
  const nino   = (o, extra, antes) => lienzo((antes || '') + sombra(64, 103, 26) + grupo(kid(o), 16, 0) + (extra || ''));
  const objeto = (n, size, extra) => { size = size || 76;
    return lienzo(sombra(64, 100, size * .38) + pon(dibujo(n), 64 - size / 2, 100 - size + 2, size) + (extra || '')); };
  const dos    = (a, b, size) => { size = size || 60;
    return lienzo(sombra(36, 100, 22) + sombra(92, 100, 22) + pon(dibujo(a), 36 - size / 2, 100 - size + 2, size) + pon(dibujo(b), 92 - size / 2, 100 - size + 2, size)); };

  function nadando(o, extra) {
    // el agua tapa las piernas: cabeza, hombros y brazos fuera
    const k = grupo(kid(Object.assign({ pose: 'brazos' }, o || {})), 16, 16);
    const agua = `<rect x="0" y="70" width="128" height="38" rx="10" fill="${P.agua}"/>
      <path d="M0 73 q8 -6 16 0 t16 0 t16 0 t16 0 t16 0 t16 0 t16 0 t16 0" stroke="${P.azul}" stroke-width="2.5"/>
      <path d="M20 62 q3 -8 6 0 M102 62 q3 -8 6 0" stroke="${P.azul}" stroke-width="2"/>`;
    return lienzo(k + agua + (extra || ''));
  }
  function durmiendo(extra) {
    return lienzo(`
      ${sombra(64, 102, 52)}
      <rect x="6" y="28" width="9" height="56" rx="3" fill="${P.marron}"/>
      <rect x="113" y="46" width="9" height="38" rx="3" fill="${P.marron}"/>
      <rect x="14" y="60" width="100" height="22" rx="4" fill="${P.marronOsc}"/>
      <rect x="16" y="36" width="34" height="18" rx="7" fill="${P.blanco}" stroke="${P.gris}" stroke-width="1.5"/>
      <circle cx="32" cy="42" r="15" fill="${P.marron}"/>
      <circle cx="35" cy="44" r="14" fill="${P.piel}" stroke="${P.pielOsc}" stroke-width="1.5"/>
      <path d="M29 42 q3 4 6 0 M39 42 q3 4 6 0" stroke="${P.negro}" stroke-width="2"/>
      <path d="M33 50 q4 3 8 0" stroke="${P.negro}" stroke-width="2"/>
      <path d="M50 46 h60 q6 0 6 8 v8 h-70 v-12 q0 -4 4 -4z" fill="${P.azul}"/>
      ${marca('zzz', 74, 26)}${extra || ''}`);
  }
  function calendario(l1, l2, color) {
    const c = color || P.rojo, largo = Math.max(l1.length, (l2 || '').length);
    const fs = l2 ? 11 : Math.min(17, Math.round(58 / largo * 1.55));
    const tl = largo > 5 ? ' textLength="42" lengthAdjust="spacingAndGlyphs"' : '';
    const texto = l2
      ? `<text x="32" y="39" text-anchor="middle" font-size="${fs}" ${FONT} fill="${P.negro}"${tl}>${l1}</text><text x="32" y="51" text-anchor="middle" font-size="${fs}" ${FONT} fill="${P.negro}"${tl}>${l2}</text>`
      : `<text x="32" y="46" text-anchor="middle" font-size="${fs}" ${FONT} fill="${P.negro}"${tl}>${l1}</text>`;
    return s64(`
      <rect x="8" y="12" width="48" height="44" rx="5" fill="${P.blanco}" stroke="${P.gris}" stroke-width="2"/>
      <path d="M8 17 q0 -5 5 -5 h38 q5 0 5 5 v8 h-48z" fill="${c}"/>
      <rect x="17" y="7" width="4" height="11" rx="2" fill="${P.grisOsc}"/>
      <rect x="43" y="7" width="4" height="11" rx="2" fill="${P.grisOsc}"/>
      ${texto}`);
  }
  // el reloj marca de verdad la hora que dice la frase
  function reloj(hora, min) {
    min = min || 0;
    const ah = (hora % 12) * 30 + min * .5, am = min * 6;
    let marcas = '';
    for (let i = 0; i < 12; i++) marcas += `<path d="M48 13 v${i % 3 ? 3 : 6}" stroke="${P.azulOsc}" stroke-width="${i % 3 ? 2 : 3}" transform="rotate(${i * 30} 48 48)"/>`;
    return `<svg class="mb-arte" width="96" height="96" viewBox="0 0 96 96" aria-hidden="true">
      <circle cx="48" cy="48" r="40" fill="${P.crema}" stroke="${P.azulOsc}" stroke-width="4"/>
      ${marcas}
      <text x="48" y="27" text-anchor="middle" font-size="10" ${FONT} fill="${P.azulOsc}">12</text>
      <text x="72" y="52" text-anchor="middle" font-size="10" ${FONT} fill="${P.azulOsc}">3</text>
      <text x="48" y="76" text-anchor="middle" font-size="10" ${FONT} fill="${P.azulOsc}">6</text>
      <text x="24" y="52" text-anchor="middle" font-size="10" ${FONT} fill="${P.azulOsc}">9</text>
      <path d="M48 48 L48 30" stroke="${P.azulOsc}" stroke-width="5" stroke-linecap="round" transform="rotate(${ah} 48 48)"/>
      <path d="M48 48 L48 20" stroke="${P.rojo}" stroke-width="3.5" stroke-linecap="round" transform="rotate(${am} 48 48)"/>
      <circle cx="48" cy="48" r="3.5" fill="${P.azulOsc}"/>
    </svg>`;
  }
  // n puntos en rejilla: 13 se ve poco, 30 se ve mucho
  function puntos(n, colorExtra) {
    const cols = n <= 15 ? 5 : 6, filas = Math.ceil(n / cols);
    const celda = Math.min(112 / cols, 88 / filas), r = celda * .34;
    const x0 = 64 - (cols * celda) / 2 + celda / 2, y0 = 54 - (filas * celda) / 2 + celda / 2;
    let s = '';
    for (let i = 0; i < n; i++) {
      const c = i % cols, f = Math.floor(i / cols);
      const ultimo = colorExtra && i === n - 1;
      s += `<circle cx="${(x0 + c * celda).toFixed(1)}" cy="${(y0 + f * celda).toFixed(1)}" r="${r.toFixed(1)}" fill="${ultimo ? colorExtra : P.rojo}" stroke="${ultimo ? P.azulOsc : '#b7453a'}" stroke-width="1.2"/>`;
    }
    return lienzo(s);
  }
  function cajaAbierta(color) {
    return lienzo(`
      ${sombra(64, 100, 34)}
      <path d="M30 52 h68 v44 h-68z" fill="${color || '#e8c49a'}" stroke="#a9743f" stroke-width="2"/>
      <path d="M98 52 l14 -8 v44 l-14 8z" fill="#c99a63" stroke="#a9743f" stroke-width="2"/>
      <path d="M26 52 h76 l6 -22 h-76z" fill="#f0d5b0" stroke="#a9743f" stroke-width="2" transform="rotate(-32 26 52)"/>
      <path d="M60 30 l3 7 7 3 -7 3 -3 7 -3 -7 -7 -3 7 -3z" fill="${P.amarillo}"/>
      <path d="M82 18 l2 5 5 2 -5 2 -2 5 -2 -5 -5 -2 5 -2z" fill="${P.amarillo}"/>`);
  }
  const sombrero = `<ellipse cx="48" cy="9" rx="25" ry="5" fill="${P.rojo}"/><path d="M31 9 q0 -17 17 -17 q17 0 17 17z" fill="${P.rojo}"/>`;
  const bufanda  = `<path d="M33 45 q15 9 30 0 v7 q-15 9 -30 0z" fill="${P.verde}"/><path d="M58 50 l4 20" stroke="${P.verde}" stroke-width="7"/>`;
  const bolsa    = `<rect x="84" y="86" width="24" height="18" rx="4" fill="${P.naranja}"/><path d="M90 86 q6 -10 12 0" stroke="${P.marronOsc}" stroke-width="2.5"/>`;

  /* ---------- los dibujos de siempre (los usa la tabla francesa) ---------- */
  function caja(alto, color) {
    // una caja de carton de tres cuartos; el alto la hace mas o menos grande
    const w = Math.round(alto * 1.25), h = alto;
    return `<svg class="mb-arte" width="${w}" height="${h + 14}" viewBox="0 0 ${w} ${h + 14}" aria-hidden="true">
      <ellipse cx="${w / 2}" cy="${h + 8}" rx="${w * .42}" ry="5" fill="rgba(20,30,45,.14)"/>
      <path d="M${w * .10} ${h * .34} L${w * .70} ${h * .34} L${w * .70} ${h} L${w * .10} ${h} Z"
            fill="${color}" stroke="#a9743f" stroke-width="1.6"/>
      <path d="M${w * .70} ${h * .34} L${w * .95} ${h * .22} L${w * .95} ${h * .88} L${w * .70} ${h} Z"
            fill="#c99a63" stroke="#a9743f" stroke-width="1.6"/>
      <path d="M${w * .10} ${h * .34} L${w * .35} ${h * .22} L${w * .95} ${h * .22} L${w * .70} ${h * .34} Z"
            fill="#e8c49a" stroke="#a9743f" stroke-width="1.6"/>
      <rect x="${w * .10}" y="${h * .58}" width="${w * .60}" height="${h * .12}" fill="#e05c4b"/>
    </svg>`;
  }
  function bolas(n) {
    const w = 128, h = 74;
    let s = `<svg class="mb-arte" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" aria-hidden="true">`;
    for (let i = 0; i < n; i++) {
      const x = 26 + i * 34, y = 44;
      s += `<ellipse cx="${x}" cy="${y + 20}" rx="14" ry="4" fill="rgba(20,30,45,.14)"/>
            <circle cx="${x}" cy="${y}" r="15" fill="#e05c4b" stroke="#b7453a" stroke-width="1.6"/>
            <path d="M${x - 15} ${y} a15 15 0 0 0 30 0" fill="#f4f1ec" opacity=".55"/>`;
    }
    return s + '</svg>';
  }
  function figura(cara, brazo) {
    // el monigote antiguo: lo sigue usando la tabla francesa
    return `<svg class="mb-arte" width="96" height="108" viewBox="0 0 96 108" aria-hidden="true" fill="none" stroke-linecap="round" stroke-linejoin="round">
      ${sombra(48, 102, 24)}${kid({ cara: cara === 'triste' ? 'triste' : 'feliz', pose: brazo === 'arriba' ? 'saluda' : 'de-pie' })}
    </svg>`;
  }
  function cajaCon(donde) {
    // una pelota dentro, encima o debajo de una caja
    const pos = { in: [64, 62], on: [64, 26], under: [64, 88] }[donde] || [64, 62];
    return `<svg class="mb-arte" width="128" height="108" viewBox="0 0 128 108" aria-hidden="true">
      <ellipse cx="64" cy="100" rx="34" ry="5" fill="rgba(20,30,45,.14)"/>
      <path d="M30 44 L98 44 L98 92 L30 92 Z" fill="${donde === 'in' ? 'none' : '#e8c49a'}"
            stroke="#a9743f" stroke-width="2"/>
      ${donde === 'in' ? '<path d="M30 44 L98 44 L98 92 L30 92 Z" fill="#e8c49a" opacity=".45" stroke="#a9743f" stroke-width="2"/>' : ''}
      <circle cx="${pos[0]}" cy="${pos[1]}" r="14" fill="#e05c4b" stroke="#b7453a" stroke-width="1.6"/>
    </svg>`;
  }

  /* ---------- las familias ----------
     Como se reconoce la unidad (busca), y la clase: gancho, tres pasos con
     su dibujo y lo que dice la profesora, la regla (pie), el truco y el
     reto con su explicacion. Nada nombra una categoria gramatical: se
     ensena con "the little s", "the ending", "the helper word". */
  const FAMILIAS = [
    {
      id: 'grande',
      busca: /compar|superlat|-er|bigger|biggest|tall|short|big|small|long|old|adjective\s*\+\s*er/i,
      titulo: 'Three boxes, three words',
      gancho: 'Three boxes! Small, bigger, biggest. Watch the word grow with the box!',
      pasos: [
        { arte: () => caja(64, '#e8c49a'),  di: 'This box is [big]', nota: 'Just big.',
          dice: 'Look at this box. It is big. Just big. The word is short, like the box.' },
        { arte: () => caja(92, '#e0b784'),  di: 'This box is bigg[er]', nota: 'More than the first one.',
          dice: 'Now this one. It is bigger! Bigger than the first one. The word grows: we add E R. Big... bigger!' },
        { arte: () => caja(124, '#d8a96c'), di: 'This box is the bigg[est]', nota: 'The winner of all three!',
          dice: 'And this one? The biggest of all! The word grows again: E S T. Big, bigger, biggest! Say it with me!' },
      ],
      pie: 'One more box, one more ending: -er, then -est.',
      truco: 'Bigger is for two things. Biggest is the winner. Hear the T in biggest? T for Top!',
      reto: { p: 'This box is the ___ of all three.', ops: ['tall', 'taller', 'tallest'], bien: 2,
              explica: 'Tallest! Of all three, the winner gets E S T.',
              pista: 'Of all three... that is the winner. Which word has the T for Top?' },
    },
    {
      id: 'puedo',
      busca: /\bcan\b|can't|cannot|ability/i,
      titulo: 'What can you do?',
      gancho: 'Can you swim? Can you fly? One little word tells us what you can do: CAN!',
      pasos: [
        { arte: () => nadando({ cara: 'feliz' }), di: 'I [can] swim', nota: 'Yes! I can do it.',
          dice: 'Look, I am in the water. I can swim! Can means: yes, I know how to do it.' },
        { arte: () => nino({ pose: 'brazos', cara: 'triste' }, marca('x') + marca('pajaros', 24, 20)), di: "I [can't] fly", nota: 'No, I cannot.',
          dice: "But fly? The birds can fly. I have no wings! I can't fly. Can't means: no, I cannot." },
        { arte: () => nino({ pose: 'saluda', cara: 'canta' }, marca('pregunta') + marca('notas', 92, 60)), di: '[Can] you sing?', nota: 'Ask a friend!',
          dice: 'Now ask a friend! Put CAN first: Can you sing? Can you dance? Can you jump?' },
      ],
      pie: "can = yes, I can. can't = no, I cannot.",
      truco: 'The word after can never changes: can swim, can fly, can sing. No S, no I N G!',
      reto: { p: 'A fish in the sea…', ops: ['can swim', "can't swim", 'can fly'], bien: 0,
              explica: 'A fish can swim! Fish live in the water.',
              pista: 'A fish lives in the sea. What can a fish do in the water?' },
    },
    {
      id: 'muchos',
      busca: /plural|countable|uncountable|there is|there are|there was|there were|how many/i,
      titulo: 'One, or a lot?',
      gancho: 'One ball... two balls! Listen to the end of the word. Can you hear the little S?',
      pasos: [
        { arte: () => bolas(1), di: 'There is one ball', nota: 'Only one.',
          dice: 'One ball. Just one. The word is ball. No S.' },
        { arte: () => bolas(2), di: 'There are two ball[s]', nota: 'More than one → s',
          dice: 'Now two! Two balls. More than one? We add the little S at the end. Ballsss!' },
        { arte: () => bolas(3), di: 'There are three ball[s]', nota: 'Still s!',
          dice: 'Three balls! Ten balls! A hundred balls! Always the S. And look: there IS one, there ARE many.' },
      ],
      pie: 'More than one? Add the little s.',
      truco: 'Count on your fingers: one, no s. Two or more, sss, like a snake!',
      reto: { p: 'I can see four…', ops: ['cat', 'cats', 'catses'], bien: 1,
              explica: 'Four cats! More than one, so we add one S. Just one S!',
              pista: 'Four is more than one. Add the little s. Only one s!' },
    },
    {
      id: 'donde',
      busca: /preposition|in \/ on|on \/ under|place|where is|behind|between|under/i,
      titulo: 'Where is the ball?',
      gancho: 'Where is the ball? In the box? On the box? Under the box? Watch the ball move!',
      pasos: [
        { arte: () => cajaCon('in'),    di: 'The ball is [in] the box',    nota: 'Inside.',
          dice: 'The ball is IN the box. Inside! Can you see it? It is hiding in the box.' },
        { arte: () => cajaCon('on'),    di: 'The ball is [on] the box',    nota: 'On top.',
          dice: 'Now the ball is ON the box. On top! It sits on the box like a hat.' },
        { arte: () => cajaCon('under'), di: 'The ball is [under] the box', nota: 'Below.',
          dice: 'And now? The ball is UNDER the box. Below it! The box is over the ball.' },
      ],
      pie: 'The box does not move — the ball does.',
      truco: 'Put your hand in your pocket: IN. On your head: ON. Under your chair: UNDER. Try it!',
      reto: { p: 'The cat is sleeping ___ the bed.', ops: ['in', 'on', 'under'], bien: 1,
              explica: 'On the bed! The cat sleeps on top of the bed.',
              pista: 'Where do you sleep? On top of the bed, not inside it!' },
    },
    {
      id: 'ahora',
      busca: /continuous|-ing|present continuous|right now|doing/i,
      titulo: 'Right now!',
      gancho: 'Every day I run. But look, right now I am running! Watch what happens to the word.',
      pasos: [
        { arte: () => nino({ pose: 'corre', lineas: false }, pon(calendario('EVERY', 'DAY', P.azul), 84, 2, 42)), di: 'I run every day', nota: 'Every day. A habit.',
          dice: 'I run every day. Monday, Tuesday, every day. Just: I run.' },
        { arte: () => nino({ pose: 'corre' }, marca('ahora', 104, 22)), di: 'I [am] runn[ing]', nota: 'Right now!',
          dice: 'But look at me NOW! I am running! Right now! Two changes: AM before, I N G at the end.' },
        { arte: () => nino({ pose: 'corre', pelo: 'chica', ropa: P.rosa }, marca('ahora', 104, 22)), di: 'She [is] runn[ing]', nota: 'Look at her!',
          dice: 'Look at Astrid! She IS running! For he, she or it, we say IS. She is running!' },
      ],
      pie: 'Happening now? am / is / are + -ing.',
      truco: 'Point at a friend and say what they are doing: You are reading! He is jumping! Now, now, now: I N G!',
      reto: { p: 'Look! Pip ___ .', ops: ['fly', 'is flying', 'flies'], bien: 1,
              explica: 'Look! Right now! Pip IS flying. Is plus I N G.',
              pista: 'Look! means right now. We need two things: is... and I N G.' },
    },
    {
      id: 'tengo',
      busca: /have got|has got|possession|whose|possessive|mine|yours/i,
      titulo: 'Whose is it?',
      gancho: 'I have got a box. She has got a box. Have... has... Which one? Let\'s see!',
      pasos: [
        { arte: () => nino({ pose: 'sostiene' }, pon(caja(40, '#e8c49a'), 40, 70, 46)), di: 'I [have got] a box', nota: 'Mine!',
          dice: 'I have got a box. It is mine! For I, you, we and they: HAVE got.' },
        { arte: () => nino({ pose: 'sostiene', pelo: 'chica', ropa: P.rosa }, pon(caja(40, '#d8b0d0'), 40, 70, 46)), di: 'She [has got] a box', nota: 'Hers!',
          dice: 'Astrid has got a box too. HAS got. For he, she and it, have changes to HAS.' },
        { arte: () => lienzo(sombra(34, 103, 20) + sombra(94, 103, 20) + grupo(kid({ pose: 'sostiene' }), -2, 8, .72) + grupo(kid({ pose: 'sostiene', pelo: 'chica', ropa: P.rosa }), 58, 8, .72)
                      + pon(caja(40, '#e8c49a'), 18, 62, 34) + pon(caja(40, '#a8d0e8'), 78, 62, 34)), di: 'They [have got] boxes', nota: 'Theirs!',
          dice: 'Nico and Astrid? They have got boxes! Two people: HAVE got again.' },
      ],
      pie: 'he, she, it → has got. Everyone else → have got.',
      truco: 'HAS has an S, and so does SHE! She has, he has. Everyone else: have!',
      reto: { p: 'Nico ___ a red kite.', ops: ['have got', 'has got', 'got'], bien: 1,
              explica: 'Nico is a he. He has got a red kite!',
              pista: 'Nico is one boy, a he. Which one is for he?' },
    },
    {
      id: 'ayer',
      busca: /past simple|past continuous|was \/ were|went|yesterday|last week|irregular/i,
      titulo: 'Today and yesterday',
      gancho: 'Today I play. Yesterday I played. Listen to the end of the word: play... played!',
      pasos: [
        { arte: () => nino({ pose: 'de-pie' }, pon(dibujo('football'), 84, 66, 38) + pon(calendario('TODAY', null, P.verde), 2, 2, 42)), di: 'Today I play', nota: 'Now.',
          dice: 'Today. Right now. I play football. Just: play.' },
        { arte: () => lienzo(sombra(64, 103, 26) + `<g opacity=".55">${grupo(kid({ pose: 'de-pie' }), 16, 0)}${pon(dibujo('football'), 84, 66, 38)}</g>` + pon(calendario('YESTER', 'DAY'), 2, 2, 42) + marca('ok')), di: 'Yesterday I play[ed]', nota: 'Finished!',
          dice: 'Yesterday! It is finished. I played. We add E D at the end. Play... played!' },
        { arte: () => nino({ pose: 'corre' }, pon(dibujo('zoo'), 86, 24, 44) + pon(calendario('YESTER', 'DAY'), 2, 2, 38)), di: 'Yesterday I [went]', nota: 'Some words change completely!',
          dice: 'But careful! Some words are naughty. Not goed! We say WENT. I went to the zoo. Go... went!' },
      ],
      pie: 'Yesterday? Add -ed… but some words change completely.',
      truco: 'E D is for yesterday, like the End of the Day! Go, see and eat are naughty: went, saw, ate.',
      reto: { p: 'Yesterday we ___ to the zoo.', ops: ['go', 'goed', 'went'], bien: 2,
              explica: 'Went! Go is a naughty word. It changes completely.',
              pista: 'Go is one of the naughty words. It does not take E D!' },
    },
    {
      id: 'manana',
      busca: /will|won't|going to|future|tomorrow/i,
      titulo: 'Tomorrow!',
      gancho: 'Now I am here. Tomorrow? I will go! One little word for tomorrow: WILL.',
      pasos: [
        { arte: () => lienzo(sombra(64, 103, 40) + pon(dibujo('house'), 4, 40, 60) + grupo(kid({ pose: 'saluda' }), 40, 8, .9) + pon(calendario('TODAY', null, P.verde), 90, 2, 36)), di: 'Now I am here', nota: 'Now.',
          dice: 'Now, today, I am here. Right here, at home, with you.' },
        { arte: () => nino({ pose: 'corre' }, marca('sol', 18, 20) + pon(calendario('TO', 'MORROW'), 86, 2, 40)), di: 'Tomorrow I [will] go', nota: 'Later!',
          dice: 'Tomorrow, I will go to the beach! It has not happened yet. For later, we say WILL.' },
        { arte: () => nino({ pose: 'de-pie', cara: 'triste' }, marca('lluvia', 20, 18) + marca('x') + pon(calendario('TO', 'MORROW'), 86, 40, 36)), di: "Tomorrow I [won't] go", nota: 'Not tomorrow!',
          dice: "But if it rains? I won't go. Won't means will not. No beach tomorrow!" },
      ],
      pie: "Has not happened yet? Use will. No? won't.",
      truco: 'WILL is the same for everybody: I will, she will, they will. Easy!',
      reto: { p: 'Tomorrow it ___ rain.', ops: ['will', 'was', 'is'], bien: 0,
              explica: 'Tomorrow it will rain. Tomorrow, so: will!',
              pista: 'Tomorrow has not happened yet. Which word is for later?' },
    },
    {
      /* Las dos mitades de una frase con «if». La de siempre (zero
         conditional) es la que pide A2 Flyers; la del plan de este sabado
         (first conditional) ya es B1, y por eso van juntas y separadas. */
      id: 'si',
      busca: /conditional|if \+ present|if clause|if-clause/i,
      titulo: 'If…, then…',
      gancho: "If it's sunny, we go swimming. If it rains, we stay inside. Two halves, one sentence. Let's look!",
      pasos: [
        { arte: () => nadando({}, marca('sol', 18, 18)), di: "[If] it's sunny, we go swimming", nota: 'Always. Every sunny day.',
          dice: "If it's sunny, we go swimming. Every sunny day, always! The first half starts with IF." },
        { arte: () => objeto('house', 80, marca('lluvia', 22, 18)), di: "[If] it rains, we['ll] stay inside", nota: 'Only this Saturday.',
          dice: "If it rains this Saturday, we'll stay inside. One day, one plan. The WILL goes in the second half." },
        { arte: () => nino({ pose: 'de-pie' }, pon(reloj(4, 0), 84, 4, 42)), di: "If you're late, we['ll] wait", nota: 'A promise.',
          dice: "If you're late, we'll wait for you. That is a promise! IF first, WILL after." },
      ],
      pie: 'After if, never will. The will goes in the other half.',
      truco: 'IF and WILL never sit together! If it rains, we WILL stay. Will goes in the other half.',
      reto: { p: 'If it ___ tomorrow, we will stay at home.', ops: ['will rain', 'rains', 'rained'], bien: 1,
              explica: 'If it rains! After if, no will. The will is already in the other half.',
              pista: "Look: 'we will stay'. The will is already there. After if, keep it simple!" },
    },
    {
      id: 'este',
      busca: /this \/ that|these \/ those|this|that|these|those|demonstrat/i,
      titulo: 'Near me, far from me',
      gancho: 'This ball is here, in my hand. That ball is over there! Near or far? Let\'s see.',
      pasos: [
        { arte: () => nino({ pose: 'senala' }, pon(dibujo('ball'), 92, 40, 40)), di: '[This] ball', nota: 'Here, next to me.',
          dice: 'This ball. It is here, next to me. I can touch it. Near? THIS.' },
        { arte: () => nino({ pose: 'senala-lejos' }, pon(dibujo('ball'), 106, 2, 20)), di: '[That] ball', nota: 'Over there!',
          dice: 'That ball. It is far, over there! I point at it. Far? THAT.' },
        { arte: () => nino({ pose: 'senala' }, pon(dibujo('ball'), 86, 66, 26) + pon(dibujo('ball'), 104, 60, 26) + pon(dibujo('ball'), 95, 42, 26)), di: '[These] balls', nota: 'Here, and more than one.',
          dice: 'These balls! Near me, and more than one. This becomes THESE. And far and many? Those!' },
      ],
      pie: 'Near: this / these. Far: that / those.',
      truco: 'THIS is short, it is close to you! THAT: point your arm far away! Try it: this... that!',
      reto: { p: '___ boxes here are mine.', ops: ['This', 'These', 'That'], bien: 1,
              explica: 'These boxes! Here means near, and boxes means more than one.',
              pista: 'Boxes, more than one. And here, near. Which word is near AND many?' },
    },
    {
      id: 'el-hace',
      busca: /third person|3rd person|present simple|likes \/ doesn|does \/ doesn|daily routine/i,
      titulo: 'He, she… and a little s',
      gancho: 'I play. He plays. Do you hear it? A tiny S jumps onto the word! Let\'s find it.',
      pasos: [
        { arte: () => nino({ pose: 'saluda' }, pon(dibujo('football'), 84, 66, 38)), di: 'I play every day', nota: 'No s for I.',
          dice: 'I play football every day. For I, the word stays the same: play.' },
        { arte: () => nino({ pose: 'de-pie' }, pon(dibujo('football'), 84, 66, 38)), di: 'He play[s] every day', nota: 'He → s!',
          dice: 'But Nico? He plays. Listen: playsss. For HE, a little S jumps onto the end!' },
        { arte: () => nino({ pose: 'de-pie', pelo: 'chica', ropa: P.rosa }, pon(dibujo('football'), 84, 66, 38)), di: 'She play[s] every day', nota: 'She → s!',
          dice: 'And Astrid? She plays! For SHE too. He, she, it: the word gets an S.' },
      ],
      pie: 'He, she or it? The verb gets an s.',
      truco: 'HE, SHE, IT: the S club! Only for one person, and not you or me.',
      reto: { p: 'Pip ___ in the sea every morning.', ops: ['swim', 'swims', 'swimming'], bien: 1,
              explica: 'Pip swims! Pip is one, like he. Every morning, a habit. Swims with an S!',
              pista: 'Pip is one, like he or she. Every morning means a habit. Which one has the S?' },
    },
    {
      id: 'la-hora',
      busca: /o'clock|quarter past|half past|quarter to|what time|telling the time|clock/i,
      titulo: 'What time is it?',
      gancho: 'Tick tock! What time is it? Look at the big red hand first. Ready?',
      pasos: [
        { arte: () => reloj(3, 0),  di: "three [o'clock]", nota: 'Big hand up.',
          dice: 'The big hand points up, to the twelve. The small hand at three. Three o\'clock!' },
        { arte: () => reloj(3, 30), di: '[half past] three', nota: 'Big hand down.',
          dice: 'Now the big hand points down, to the six. Half of the clock! Half past three.' },
        { arte: () => reloj(3, 45), di: '[quarter to] four', nota: 'Almost four!',
          dice: 'The big hand at the nine. A quarter of the clock is left. Quarter to four. Almost four!' },
      ],
      pie: "Up: o'clock. Down: half past. Left: quarter to.",
      truco: 'Big hand up? o\'clock! Big hand down? half past! Big hand left? quarter to! Big hand right? quarter past!',
      reto: { p: 'The big hand points down. It is…', ops: ["four o'clock", 'half past four', 'quarter to four'], bien: 1,
              explica: 'Half past four! Big hand down means half past.',
              pista: 'Big hand down: that is the half of the clock. Half past...' },
    },
    {
      id: 'cuando',
      busca: /in \+ month|on \+ date|on \+ day|at \+ time|prepositions of time|month|season|birthday|date|in the morning|at night|day parts/i,
      titulo: 'in, on, at — when?',
      gancho: 'In July, on Monday, at seven o\'clock. Three tiny words for time. Big, small, tiny!',
      pasos: [
        { arte: () => objeto('julio', 84), di: '[in] July',       nota: 'A whole month.',
          dice: 'In July. A whole month, big time! IN for months, years and seasons: in July, in summer.' },
        { arte: () => objeto('lunes', 84), di: '[on] Monday',     nota: 'One day.',
          dice: 'On Monday. Just one day, smaller! ON for days and dates: on Monday, on my birthday.' },
        { arte: () => reloj(7, 0),         di: "[at] 7 o'clock", nota: 'One moment.',
          dice: 'At seven o\'clock. One little moment, tiny! AT for clock times: at seven, at night.' },
      ],
      pie: 'Big time: in. One day: on. One moment: at.',
      truco: 'Think of a box: IN the big box, the month. ON the day. AT the point of the clock!',
      reto: { p: 'My birthday is ___ May.', ops: ['in', 'on', 'at'], bien: 0,
              explica: 'In May! May is a month, big time, so: in.',
              pista: 'May is a whole month. Big time! Which word is for big time?' },
    },
    {
      id: 'ya',
      busca: /present perfect|just \/ already|already|yet|ever \/ never|have you ever/i,
      titulo: 'Already done!',
      gancho: 'I am eating... I have just eaten! Finished? Then we use HAVE. Watch!',
      pasos: [
        { arte: () => nino({ pose: 'sostiene' }, pon(dibujo('plateFull'), 40, 66, 46)), di: 'I am eating', nota: 'Now.',
          dice: 'Look. I am eating. Right now. Yummy! Not finished.' },
        { arte: () => nino({ pose: 'sostiene' }, pon(dibujo('plateEmpty'), 40, 66, 46) + marca('ok')), di: 'I [have] just eat[en]', nota: 'A moment ago!',
          dice: 'Now my plate is empty! I have just eaten. Finished, a moment ago. HAVE, plus the special word: eaten.' },
        { arte: () => nino({ pose: 'sostiene', cara: 'triste' }, pon(dibujo('plateFull'), 40, 66, 46) + marca('x')), di: "I [haven't] eaten [yet]", nota: 'Not yet…',
          dice: "And this plate is still full. I haven't eaten yet. Not yet, but soon!" },
      ],
      pie: "Finished? have + eaten. Not finished? haven't… yet.",
      truco: 'JUST means a moment ago. ALREADY means done! YET means not now, but soon. All of them with HAVE.',
      reto: { p: 'Kili ___ already brought the letters.', ops: ['has', 'have', 'is'], bien: 0,
              explica: 'Kili HAS already brought them! Kili is one, like he, so: has.',
              pista: 'Kili is one, like he or she. Have becomes...?' },
    },
    {
      id: 'mejor',
      busca: /should|shouldn't|must|have to|advice|rules/i,
      titulo: 'A good idea, a bad idea',
      gancho: 'You are tired? You should sleep! Good idea, or bad idea? SHOULD helps us!',
      pasos: [
        { arte: () => durmiendo(marca('ok', 108, 20)), di: 'You [should] sleep', nota: 'Good idea!',
          dice: 'You are tired. You should sleep! Should means: it is a good idea.' },
        { arte: () => nino({ pose: 'brazos', cara: 'grita' }, marca('x')), di: "You [shouldn't] shout", nota: 'Not a good idea.',
          dice: "In the library? You shouldn't shout! Shouldn't means: not a good idea. Shhh." },
        { arte: () => nino({ pose: 'saluda' }, marca('pregunta')), di: '[Should] I help?', nota: 'Ask for advice.',
          dice: 'Not sure? Ask! Should I help? Put SHOULD first to ask.' },
      ],
      pie: "Good idea? should. Bad idea? shouldn't.",
      truco: 'SHOULD is a friend giving advice, not a boss! And it is the same for everybody: I should, she should.',
      reto: { p: 'You are tired. You ___ go to bed.', ops: ['should', "shouldn't", "can't"], bien: 0,
              explica: 'You should go to bed! Tired? Good idea: sleep.',
              pista: 'Going to bed when you are tired... good idea or bad idea?' },
    },
    {
      id: 'como-voy',
      busca: /transport|by \+ vehicle|how do you get|travel by|bus|train|bike/i,
      titulo: 'How do you get there?',
      gancho: 'How do you get to school? By bus? By bike? On foot? Let\'s find out!',
      pasos: [
        { arte: () => objeto('bus', 84),  di: 'I go [by] bus',  nota: 'By + the vehicle.',
          dice: 'I go by bus. BY, and then the vehicle: by bus, by car, by train.' },
        { arte: () => objeto('bike', 84), di: 'I go [by] bike', nota: 'By again!',
          dice: 'I go by bike. By again! By bike, by boat, by plane. Always BY.' },
        { arte: () => objeto('feet', 84), di: 'I go [on foot]', nota: 'This one is different!',
          dice: 'But walking? Look at my feet. I go ON FOOT. Not by foot. On foot! The special one.' },
      ],
      pie: 'Always by… except on foot.',
      truco: 'Your feet are ON the ground: ON foot! Everything else: BY.',
      reto: { p: 'I walk to school. I go ___ .', ops: ['by foot', 'on foot', 'by walk'], bien: 1,
              explica: 'On foot! Walking is the special one.',
              pista: 'Walking is the special one. Your feet are ON the ground...' },
    },
    {
      id: 'que-verbo',
      busca: /play \/ go \/ do|play \+ sport|go \+ -ing|sports?/i,
      titulo: 'play, go or do?',
      gancho: 'Play football, go swimming, do karate. Three sports, three words. Which one goes where?',
      pasos: [
        { arte: () => objeto('football', 80), di: '[play] football', nota: 'Games with a ball.',
          dice: 'Play football, play tennis, play basketball. A ball? PLAY!' },
        { arte: () => nadando(), di: '[go] swimming', nota: 'Words ending in -ing.',
          dice: 'Go swimming, go skating, go fishing. Hear the I N G? GO!' },
        { arte: () => nino({ pose: 'patada', ropa: P.blanco }), di: '[do] karate', nota: 'The rest!',
          dice: 'Do karate, do judo, do gymnastics. No ball, no I N G? DO!' },
      ],
      pie: 'Ball? play. -ing? go. The rest? do.',
      truco: 'Ask two questions: Is there a ball? PLAY. Does it end in I N G? GO. No and no? DO!',
      reto: { p: 'On Saturday I ___ basketball.', ops: ['play', 'go', 'do'], bien: 0,
              explica: 'Play basketball! There is a ball, so: play.',
              pista: 'Basketball... is there a ball? Then which word?' },
    },
    {
      id: 'haz-esto',
      busca: /imperative|some \/ any|instructions|commands|let's|action words|directions|turns and steps/i,
      titulo: 'Do it!',
      gancho: 'Open the box! Don\'t open it! Let\'s open it! Three ways to say do it. Watch!',
      pasos: [
        { arte: () => cajaAbierta(), di: '[Open] the box!', nota: 'Just the verb.',
          dice: 'Open the box! No name in front. No I, no you. Just the verb: Open!' },
        { arte: () => lienzo(pon(caja(70, '#e8c49a'), 20, 14, 88) + marca('x')), di: "[Don't] open it!", nota: "Say no with don't.",
          dice: "Don't open it! To say no, put DON'T in front. Don't run! Don't shout!" },
        { arte: () => lienzo(sombra(30, 103, 18) + sombra(98, 103, 18) + grupo(kid({ pose: 'senala' }), -8, 8, .72) + grupo(kid({ pose: 'brazos', pelo: 'chica', ropa: P.rosa }), 62, 8, .72) + pon(caja(40, '#e8c49a'), 46, 62, 36)), di: "[Let's] open it!", nota: 'You and me together.',
          dice: "Let's open it! You and me, together. Let's play! Let's go!" },
      ],
      pie: "Just the verb. No: don't. Together: let's.",
      truco: 'Simon says: Jump! Don\'t jump! Let\'s jump! Play it with a friend.',
      reto: { p: '___ run in the corridor!', ops: ["Don't", 'Not', 'No'], bien: 0,
              explica: "Don't run! To say no before a verb, we use don't.",
              pista: "We need to say NO before the word 'run'. Which one goes before a verb?" },
    },
    {
      id: 'como-es',
      busca: /adjective|describing|personality|what is .* like|appearance|hair|material|made of/i,
      titulo: 'What is it like?',
      gancho: 'A big box. A big purple box. Where does the describing word go? Before or after? Let\'s see!',
      pasos: [
        { arte: () => caja(84, '#e8c49a'), di: 'a [big] box',        nota: 'The word goes first.',
          dice: 'A big box. Big goes BEFORE box. Not a box big. A big box!' },
        { arte: () => caja(84, '#c9a6dc'), di: 'a [big purple] box', nota: 'Size first, colour next.',
          dice: 'Two words? Size first, colour next: a big purple box. Big, purple, box!' },
        { arte: () => caja(66, '#a8d0e8'), di: 'The box [is] blue',  nota: 'Or put it after is.',
          dice: 'Or say it the other way: The box is blue. After IS, the colour comes last.' },
      ],
      pie: 'Before the thing, or after is.',
      truco: 'Size before colour: a big red ball, a small blue car. Big first, colour second!',
      reto: { p: 'Which one is right?', ops: ['a box red', 'a red box', 'red a box'], bien: 1,
              explica: 'A red box! The colour goes before the thing.',
              pista: 'The colour goes BEFORE the thing, like: a big box.' },
    },
    {
      id: 'es-un',
      busca: /it is a|it's sunny|it's rainy|what is it|what colour|what color|this is a|a \/ an|naming|alphabet|animal sounds|weather/i,
      titulo: 'What is it?',
      gancho: 'A ball. An apple. Two tiny words: A and AN. Why? Listen carefully!',
      pasos: [
        { arte: () => objeto('ball', 74),  di: 'It is [a] ball',   nota: 'One thing.',
          dice: 'It is a ball. One ball. Ball starts with B, so we say A. A ball!' },
        { arte: () => objeto('apple', 78), di: 'It is [an] apple', nota: 'a, e, i, o, u → an!',
          dice: 'It is an apple. Try: a apple... no! So we add an N: AN apple. Nice! For a, e, i, o, u we say AN.' },
        { arte: () => lienzo(sombra(40, 100, 26) + pon(dibujo('ball'), 8, 30, 68) + pon(dibujo('red'), 68, 30, 58)), di: 'It is [red]', nota: 'A colour needs no a.',
          dice: 'And the colour? It is red. No a, no an! Colours do not need a helper word.' },
      ],
      pie: 'a before most words, an before a, e, i, o, u.',
      truco: 'Say the word. Does it start with a, e, i, o or u? Then AN! An egg, an orange, an ice cream.',
      reto: { p: 'It is ___ elephant.', ops: ['a', 'an', 'the'], bien: 1,
              explica: 'An elephant! E is one of the five: a, e, i, o, u. So: an!',
              pista: 'E-lephant. Does it start with a, e, i, o or u? Then...' },
    },
    {
      /* Los planes y los deseos: es lo que pide «want to / would like to»,
         que en el curso estaba dado con «going to» — una estructura de A2
         Flyers dentro de una unidad de A1 Movers. */
      id: 'quiero',
      busca: /want to|wants to|would like to|ambition|wishes/i,
      titulo: 'What do you want?',
      gancho: 'I want a cake. I want to make it! Want... want to... What is the difference?',
      pasos: [
        { arte: () => objeto('cake', 80), di: 'I want [a cake]', nota: 'A thing? Just say it.',
          dice: 'I want a cake. A thing? Just say the thing: I want a cake, I want a dog.' },
        { arte: () => nino({ pose: 'sostiene' }, pon(dibujo('bowl'), 40, 66, 46)), di: 'I want [to] make it', nota: 'An action? Add to.',
          dice: 'I want to make it! An action? Put TO before the action: want to make, want to play.' },
        { arte: () => lienzo(sombra(30, 103, 18) + sombra(98, 103, 18) + grupo(kid({ pose: 'agarra' }), -8, 8, .72) + grupo(kid({ pose: 'saluda', pelo: 'chica', ropa: P.rosa }), 62, 8, .72) + pon(caja(40, '#e8c49a'), 40, 62, 36)), di: 'I [would like] to help you', nota: 'The polite one.',
          dice: 'I would like to help you. Would like is the polite way. Same TO!' },
      ],
      pie: "want + to + verb. Never 'I want make'.",
      truco: 'A thing? Want it. An action? Want TO do it. Polite? Would like TO.',
      reto: { p: 'I ___ to invite everybody.', ops: ['wanting', 'want', 'wants'], bien: 1,
              explica: 'I want to invite! For I, just want.',
              pista: 'It is I. No S, no I N G. Just...' },
    },
    {
      id: 'me-gusta',
      busca: /i like|don't like|likes \/ doesn't like|favourite|favorite|feelings|i have|for breakfast|would you like/i,
      titulo: 'Yes please, no thank you',
      gancho: 'Cake? Yes please! Fish? No thank you! Let\'s say what we like.',
      pasos: [
        { arte: () => objeto('cake', 78, marca('corazon')), di: 'I [like] cake',       nota: 'Yes!',
          dice: 'I like cake! Yes, I love it! I like: for the things you love.' },
        { arte: () => objeto('fish', 78, marca('x')),       di: "I [don't like] fish", nota: 'No…',
          dice: "I don't like fish. No, thank you! To say no: DON'T like." },
        { arte: () => objeto('cake', 78, marca('pregunta')), di: '[Do] you like cake?', nota: 'Ask a friend!',
          dice: 'Do you like cake? Put DO first to ask. Do you like fish? Do you like dogs?' },
      ],
      pie: "Yes: like. No: don't like. Ask: Do you like…?",
      truco: 'DO is the helper: Do you like...? I don\'t like... Saying yes? No helper needed!',
      reto: { p: 'Luna ___ like cats.', ops: ["don't", "doesn't", 'not'], bien: 1,
              explica: "Luna doesn't like cats. Luna is one, like she, so: doesn't.",
              pista: "Luna is a she. For he and she, don't becomes..." },
    },
    {
      id: 'llevo',
      busca: /wearing|wear \/ carry|clothes|put on|i am wearing/i,
      titulo: 'What are you wearing?',
      gancho: 'A hat on my head. A bag in my hand. Wearing or carrying? Look at where it is!',
      pasos: [
        { arte: () => nino({ pose: 'de-pie' }, grupo(sombrero, 16, 0)), di: 'I am [wearing] a hat', nota: 'On me, right now.',
          dice: 'I am wearing a hat. It is ON my body. Wearing, right now!' },
        { arte: () => nino({ pose: 'de-pie', pelo: 'chica', ropa: P.rosa }, grupo(bufanda, 16, 0)), di: 'She is [wearing] a scarf', nota: 'On her.',
          dice: 'Astrid is wearing a scarf. On her neck. Wearing!' },
        { arte: () => nino({ pose: 'agarra' }, bolsa), di: 'I am [carrying] a bag', nota: 'In my hand, not on me!',
          dice: 'But the bag? It is in my hand, not on me. I am carrying a bag. Carrying!' },
      ],
      pie: 'On your body? wearing. In your hand? carrying.',
      truco: 'Touch your T-shirt: wearing! Pick up your pencil: carrying!',
      reto: { p: 'Erik ___ a big blue bag.', ops: ['is wearing', 'is carrying', 'wears'], bien: 1,
              explica: 'Erik is carrying a bag. In his hand, not on his body.',
              pista: 'A bag goes in your hand. Which word is for the hand?' },
    },
    {
      id: 'soy',
      busca: /i am|are you|his name|her name|he is|she is|it is|man \/ woman|boy \/ girl|have you got|to be|introduc|spell/i,
      titulo: 'Who is who?',
      gancho: 'I am Pip. He is Nico. She is Astrid. Three tiny words: am, is, is. Let\'s meet everybody!',
      pasos: [
        { arte: () => nino({ pose: 'saluda' }), di: 'I [am] Nico',    nota: 'Me.',
          dice: 'I am Nico. Me, myself! For I, we say AM. I am!' },
        { arte: () => nino({ pose: 'de-pie' }), di: 'He [is] Nico',   nota: 'A boy.',
          dice: 'He is Nico. A boy, HE. For he, we say IS.' },
        { arte: () => nino({ pose: 'de-pie', pelo: 'chica', ropa: P.rosa }), di: 'She [is] Astrid', nota: 'A girl.',
          dice: 'She is Astrid. A girl, SHE. For she, we say IS too.' },
      ],
      pie: 'I am. He is. She is. It is.',
      truco: 'Point at yourself: I AM. Point at a boy: HE IS. Point at a girl: SHE IS. Point at a thing: IT IS!',
      reto: { p: '___ is my sister.', ops: ['He', 'She', 'It'], bien: 1,
              explica: 'She is my sister! A sister is a girl: she.',
              pista: 'A sister is a girl. Which word is for a girl?' },
    },
    {
      id: 'porque',
      busca: /because|so \(|so \/ because|reason|result|cause/i,
      titulo: 'Why? and So?',
      gancho: 'I am tired... because I ran! So I sat down. Because and so: one looks back, one looks forward.',
      pasos: [
        { arte: () => nino({ pose: 'cansado', cara: 'cansado' }), di: 'I am tired', nota: 'What happened.',
          dice: 'I am tired. Phew! That is what happened.' },
        { arte: () => nino({ pose: 'corre' }), di: 'I am tired [because] I ran', nota: 'The reason.',
          dice: 'Why am I tired? Because I ran! BECAUSE gives the reason. It looks back.' },
        { arte: () => nino({ pose: 'sentado', cara: 'cansado' }), di: 'I am tired, [so] I sat down', nota: 'What happened next.',
          dice: 'I am tired, so I sat down. SO tells us what happened next. It looks forward.' },
      ],
      pie: 'because looks back. so looks forward.',
      truco: 'BECAUSE answers WHY? SO answers AND THEN? Ask the question and you know!',
      reto: { p: 'It was raining, ___ we stayed at home.', ops: ['because', 'so', 'but'], bien: 1,
              explica: 'So we stayed at home! What happened next: so.',
              pista: 'Rain first, then staying at home. And then...? Which word looks forward?' },
    },
    {
      id: 'el-que',
      busca: /relative clause|who, which|which, where|defining|non-defining/i,
      titulo: 'One sentence, not two',
      gancho: 'The girl who runs. The ball which is red. The place where I live. Three little joining words!',
      pasos: [
        { arte: () => nino({ pose: 'corre', pelo: 'chica', ropa: P.rosa }), di: 'the girl [who] runs',   nota: 'who — for people.',
          dice: 'The girl who runs. A person? WHO. The boy who sings, the man who cooks.' },
        { arte: () => objeto('ball', 74),                                    di: 'the ball [which] is red', nota: 'which — for things.',
          dice: 'The ball which is red. A thing? WHICH. The book which I like.' },
        { arte: () => objeto('house', 80),                                   di: 'the place [where] I live', nota: 'where — for places.',
          dice: 'The place where I live. A place? WHERE. The school where we play.' },
      ],
      pie: 'People who, things which, places where.',
      truco: 'WHO is for a person. WHERE has HERE inside, a place! WHICH is for the rest.',
      reto: { p: 'This is the book ___ I read last week.', ops: ['who', 'which', 'where'], bien: 1,
              explica: 'The book which I read. A book is a thing: which.',
              pista: 'A book. Is it a person, a thing or a place?' },
    },
    {
      id: 'como-lo-hace',
      busca: /adverbs of manner|-ly|well, fast|how \+ adverb|slowly|loudly/i,
      titulo: 'How do you do it?',
      gancho: 'A slow snail... moves slowly. Slow... slowly! Add two letters and you say HOW.',
      pasos: [
        { arte: () => objeto('snail', 78), di: 'a [slow] snail', nota: 'What it is like.',
          dice: 'A slow snail. Slow tells us what the snail is like.' },
        { arte: () => objeto('snail', 78, `<path d="M8 96 q10 -4 20 0 t20 0" stroke="${P.gris}" stroke-width="2.5" stroke-dasharray="4 5"/>`), di: 'it moves slow[ly]', nota: 'How it does it.',
          dice: 'The snail moves slowly. Slow... slowly! Add L Y to say HOW it moves.' },
        { arte: () => nino({ pose: 'saluda', cara: 'canta', pelo: 'chica', ropa: P.rosa }, marca('notas', 100, 30)), di: 'she sings [well]', nota: 'No -ly for this one!',
          dice: 'But careful! Good becomes WELL, not goodly. She sings well. A naughty one!' },
      ],
      pie: 'Add -ly to say HOW. But good becomes well.',
      truco: 'Slowly, quickly, quietly, loudly: L Y at the end! Only GOOD is naughty: well.',
      reto: { p: 'She sings very ___ .', ops: ['good', 'well', 'goodly'], bien: 1,
              explica: 'She sings well! Good is naughty. It becomes well.',
              pista: 'Good is the naughty one. It does not take L Y. It becomes...' },
    },
    {
      id: 'hacer',
      busca: /collocation|make and do|make \/ do|make or do/i,
      titulo: 'make or do?',
      gancho: 'Make a cake. Do your homework. Make or do? Let\'s find the trick!',
      pasos: [
        { arte: () => objeto('cake', 80),     di: '[make] a cake',       nota: 'Something new appears.',
          dice: 'Make a cake. Before: nothing. After: a cake! Something new appears: MAKE.' },
        { arte: () => objeto('homework', 80), di: '[do] your homework',  nota: 'Work or a task.',
          dice: 'Do your homework. It is a job, a task. Work? DO. Do the washing-up, do exercise.' },
        { arte: () => objeto('homework', 80, marca('x')), di: '[make] a mistake', nota: 'Some you just learn!',
          dice: 'Make a mistake. Hmm, that one you just learn! Make a mistake, make a noise, make friends.' },
      ],
      pie: 'Make it and it exists. Do it and it is done.',
      truco: 'Can you hold it after? MAKE: a cake, a sandwich. Is it a job? DO: homework, the washing-up.',
      reto: { p: 'Please ___ the washing-up.', ops: ['make', 'do', 'take'], bien: 1,
              explica: 'Do the washing-up! It is a job: do.',
              pista: 'The washing-up is a job, a task. Which word is for jobs?' },
    },
    {
      id: 'cuantos',
      busca: /numbers 11|numbers 20|numbers 1|counting|how many\?/i,
      titulo: 'Counting up',
      gancho: 'Thirteen... thirty! They sound the same, but one is small and one is big. Listen to the end!',
      pasos: [
        { arte: () => puntos(13), di: 'thir[teen]',   nota: '13 — the -teen family.',
          dice: 'Thirteen. Thir-TEEN. Only thirteen dots. The TEEN family: thirteen, fourteen, fifteen.' },
        { arte: () => puntos(30), di: 'thir[ty]',     nota: '30 — the -ty family.',
          dice: 'Thirty! Thir-TY. Look how many dots! The TY family: twenty, thirty, forty.' },
        { arte: () => puntos(31, P.azul), di: 'thirty[-one]', nota: '31 — put them together.',
          dice: 'Thirty-one. Thirty, then one more. Thirty-two, thirty-three... Put them together!' },
      ],
      pie: '-teen is small, -ty is big. Listen to the end!',
      truco: 'TEEN is long, say it loud: thirTEEN! TY is short: thirty. Long sound, small number!',
      reto: { p: 'Which one is 15?', ops: ['fifty', 'fifteen', 'five'], bien: 1,
              explica: 'Fifteen! One, five: the TEEN family.',
              pista: '15 is small: one, five. Small numbers are the TEEN family.' },
    },
  ];
  // los calendarios de "in July" y "on Monday" se piden como dibujos
  D.julio = () => calendario('JULY');
  D.lunes = () => calendario('MON', null, P.azul);

  /* ---------- las familias, en frances ----------

     No es la traduccion de la tabla inglesa, y no puede serlo: "bigger,
     biggest" no existe en frances (es plus grand, le plus grand), la s de
     he plays no tiene equivalente y el -ly de slowly es -ment. Traducir la
     caja inglesa enseñaria gramatica inglesa con palabras francesas.

     Asi que es OTRA tabla, con las reglas que si son del frances: el genero
     de un/une, el acuerdo del adjetivo, el partitif du/de la/des, el passe
     compose con avoir o con etre. Los dibujos son los mismos porque una
     caja y una pelota no tienen idioma.

     El regex busca en el grammar/topic/title de la unidad FRANCESA, que ya
     esta en frances: por eso son palabras francesas y no las inglesas. */
  const FAMILIAS_FR = [
    {
      id: 'genero',
      busca: /c'est un|c'est une|de quelle couleur|l'alphabet|comment ça s'écrit|les cris des animaux|c'est \/ c'est/i,
      titulo: 'un ou une ?',
      pasos: [
        { arte: () => bolas(1), pal: 'un',  fin: ' ballon', frase: 'Le ballon : un.' },
        { arte: () => bolas(1), pal: 'une', fin: ' pomme',  frase: 'La pomme : une.' },
        { arte: () => bolas(2), pal: 'des', fin: ' ballons', frase: 'Plus d\'un : des.' },
      ],
      pie: 'Chaque mot a son un ou son une. On les apprend ensemble.',
      reto: { p: "C'est ___ maison.", ops: ['un', 'une', 'des'], bien: 1 },
    },
    {
      id: 'pluriel',
      busca: /le pluriel|combien|nombres 11|nombres 20|nombres 1|il y a \+/i,
      titulo: 'Un, ou beaucoup ?',
      pasos: [
        { arte: () => bolas(1), pal: 'un ballon',     fin: '',  frase: 'Il y a un ballon.' },
        { arte: () => bolas(2), pal: 'deux ballon',   fin: 's', frase: 'Il y a deux ballons.' },
        { arte: () => bolas(3), pal: 'trois ballon',  fin: 's', frase: 'Il y a trois ballons !' },
      ],
      pie: 'Plus d\'un ? On ajoute un s… mais on ne l\'entend pas.',
      reto: { p: 'Je vois quatre…', ops: ['chat', 'chats', 'chatses'], bien: 1 },
    },
    {
      id: 'ou',
      busca: /préposition.*lieu|dans, sur|où est|où…|où \?|derrière|entre|à côté de|indications|mouvement/i,
      titulo: 'Où est le ballon ?',
      pasos: [
        { arte: () => cajaCon('in'),    pal: 'dans', fin: '',  frase: 'Le ballon est dans la boîte.' },
        { arte: () => cajaCon('on'),    pal: 'sur',  fin: '',  frase: 'Le ballon est sur la boîte.' },
        { arte: () => cajaCon('under'), pal: 'sous', fin: '',  frase: 'Le ballon est sous la boîte.' },
      ],
      pie: 'La boîte ne bouge pas — le ballon, si.',
      reto: { p: 'Le chat dort ___ le lit.', ops: ['dans', 'sur', 'sous'], bien: 1 },
    },
    {
      id: 'savoir',
      busca: /savoir|je sais|il peut|pouvoir|je peux avoir/i,
      titulo: 'Qu\'est-ce que tu sais faire ?',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'Je sais',       fin: ' nager', frase: 'Oui ! Je sais le faire.' },
        { arte: () => figura('triste', 'abajo'), pal: 'Je ne sais pas', fin: ' voler', frase: 'Non, je ne sais pas.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'Tu sais',        fin: ' chanter ?', frase: 'Demande à un ami !' },
      ],
      pie: 'Pour dire non : ne… pas autour du verbe.',
      reto: { p: 'Un poisson dans la mer…', ops: ['sait nager', 'ne sait pas nager', 'sait voler'], bien: 0 },
    },
    {
      id: 'passe',
      busca: /passé composé|le passé|quand j'étais|imparfait|il y avait|biographies/i,
      titulo: 'Aujourd\'hui et hier',
      pasos: [
        { arte: () => reloj(9), pal: 'je joue',   fin: '',        frase: 'Aujourd\'hui.' },
        { arte: () => reloj(5), pal: 'j\'ai',     fin: ' joué',   frase: 'Hier : avoir + le participe.' },
        { arte: () => reloj(3), pal: 'je suis',   fin: ' allé',   frase: 'Aller, venir, partir : être !' },
      ],
      pie: 'Presque tous avec avoir. Aller et venir, avec être.',
      reto: { p: 'Hier nous ___ au zoo.', ops: ['allons', 'sommes allés', 'avons allé'], bien: 1 },
    },
    {
      id: 'futur',
      busca: /futur/i,
      titulo: 'Demain !',
      pasos: [
        { arte: () => reloj(9),  pal: 'je suis',   fin: ' ici',   frase: 'Maintenant.' },
        { arte: () => reloj(12), pal: 'je vais',   fin: ' partir', frase: 'Demain.' },
        { arte: () => reloj(2),  pal: 'je ne vais pas', fin: ' partir', frase: 'Pas demain !' },
      ],
      pie: 'aller + l\'infinitif : c\'est le futur proche.',
      reto: { p: 'Demain il ___ pleuvoir.', ops: ['va', 'était', 'allé'], bien: 0 },
    },
    {
      id: 'maintenant',
      busca: /en ce moment|maintenant|en train de|présent \(/i,
      titulo: 'En ce moment !',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'je cours',            fin: '',           frase: 'Tous les jours.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'je suis en train de', fin: ' courir',    frase: 'Juste maintenant !' },
        { arte: () => figura('feliz', 'arriba'), pal: 'elle est en train de', fin: ' courir',   frase: 'Regarde-la !' },
      ],
      pie: 'Le français dit le même verbe — être en train de, c\'est pour insister.',
      reto: { p: 'Regarde ! Pip ___ .', ops: ['vole', 'voler', 'volé'], bien: 0 },
    },
    {
      id: 'avoir',
      busca: /^avoir|avoir \/|avoir \+|possessif|à qui|le mien|tu as|j'ai|voici mon|il a \/|elle a|réponses courtes/i,
      titulo: 'C\'est à qui ?',
      pasos: [
        { arte: () => caja(76, '#e8c49a'), pal: 'j\'ai',      fin: ' une boîte',  frase: 'C\'est la mienne.' },
        { arte: () => caja(76, '#d8b0d0'), pal: 'elle a',     fin: ' une boîte',  frase: 'C\'est sa boîte.' },
        { arte: () => caja(76, '#a8d0e8'), pal: 'ils ont',    fin: ' des boîtes', frase: 'Ce sont les leurs.' },
      ],
      pie: 'j\'ai, tu as, il a, nous avons, vous avez, ils ont.',
      reto: { p: 'Nico ___ un cerf-volant rouge.', ops: ['ai', 'a', 'as'], bien: 1 },
    },
    {
      id: 'routine',
      busca: /3e personne|les routines|d'habitude|toujours|souvent|le présent|verbes d'action/i,
      titulo: 'je, tu, il… le verbe change',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'je jou',    fin: 'e',   frase: 'Je joue tous les jours.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'tu jou',    fin: 'es',  frase: 'Tu joues tous les jours.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'nous jou',  fin: 'ons', frase: 'Nous jouons tous les jours.' },
      ],
      pie: 'La fin du verbe suit la personne. On l\'écrit même si on ne l\'entend pas.',
      reto: { p: 'Pip ___ dans la mer chaque matin.', ops: ['nage', 'nages', 'nageons'], bien: 0 },
    },
    {
      id: 'hora',
      busca: /quelle heure|et quart|et demie|moins le quart|heures pile/i,
      titulo: 'Quelle heure est-il ?',
      pasos: [
        { arte: () => reloj(3, 0),  pal: 'trois heures',  fin: '',            frase: 'La grande aiguille est en haut.' },
        { arte: () => reloj(3, 30), pal: 'trois heures',  fin: ' et demie',   frase: 'La grande aiguille est en bas.' },
        { arte: () => reloj(3, 45), pal: 'quatre heures', fin: ' moins le quart', frase: 'Presque quatre heures !' },
      ],
      pie: 'Regarde d\'abord la grande aiguille.',
      reto: { p: 'La grande aiguille est en bas. Il est…', ops: ['quatre heures', 'quatre heures et demie', 'quatre heures moins le quart'], bien: 1 },
    },
    {
      id: 'cuando',
      busca: /en \+ mois|le \+ jour|les dates|saison|le matin \/ la nuit|quel âge|quand/i,
      titulo: 'en, le, à — quand ?',
      pasos: [
        { arte: () => reloj(12), pal: 'en', fin: ' juillet',   frase: 'Un mois entier.' },
        { arte: () => reloj(9),  pal: 'le', fin: ' lundi',     frase: 'Tous les lundis.' },
        { arte: () => reloj(7),  pal: 'à',  fin: ' sept heures', frase: 'Un moment précis.' },
      ],
      pie: 'Grande durée, jour, instant.',
      reto: { p: 'Mon anniversaire est ___ mai.', ops: ['en', 'le', 'à'], bien: 0 },
    },
    {
      id: 'deja',
      busca: /déjà|vient de|pas encore|ne… jamais|ne jamais/i,
      titulo: 'Déjà fait !',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'je mange',      fin: '',            frase: 'Maintenant.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'je viens de',   fin: ' manger',     frase: 'Il y a une minute !' },
        { arte: () => figura('triste', 'abajo'), pal: 'je n\'ai pas',  fin: ' encore mangé', frase: 'Pas encore…' },
      ],
      pie: 'venir de = ça vient de finir.',
      reto: { p: 'Kili ___ déjà apporté les lettres.', ops: ['a', 'est', 'va'], bien: 0 },
    },
    {
      id: 'consejo',
      busca: /devrait|devoir|il faut|la sécurité|les règles/i,
      titulo: 'Bonne idée, mauvaise idée',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'tu devrais',       fin: ' dormir', frase: 'Bonne idée !' },
        { arte: () => figura('triste', 'abajo'), pal: 'tu ne devrais pas', fin: ' crier',  frase: 'Pas une bonne idée.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'je dois',           fin: ' aider',  frase: 'Là, c\'est obligé.' },
      ],
      pie: 'devrais = un conseil. dois = une obligation.',
      reto: { p: 'Tu es fatigué. Tu ___ aller au lit.', ops: ['devrais', 'ne devrais pas', 'ne peux pas'], bien: 0 },
    },
    {
      id: 'transporte',
      busca: /transport|en \+ véhicule|comment tu vas/i,
      titulo: 'Comment tu y vas ?',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'en', fin: ' bus',   frase: 'J\'y vais en bus.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'à',  fin: ' vélo',  frase: 'J\'y vais à vélo.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'à',  fin: ' pied',  frase: 'Et à pied aussi !' },
      ],
      pie: 'Dedans : en. Dessus : à.',
      reto: { p: 'Je marche jusqu\'à l\'école. J\'y vais ___ .', ops: ['en pied', 'à pied', 'en marche'], bien: 1 },
    },
    {
      id: 'deporte',
      busca: /jouer à|faire de|sport/i,
      titulo: 'jouer à ou faire de ?',
      pasos: [
        { arte: () => bolas(1),                  pal: 'je joue au',      fin: ' football', frase: 'Les jeux avec un ballon.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'je fais de la',   fin: ' natation', frase: 'Les autres sports.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'je fais du',      fin: ' judo',     frase: 'du, de la, de l\' — comme le mot.' },
      ],
      pie: 'Un ballon ? jouer à. Sinon ? faire de.',
      reto: { p: 'Samedi je ___ basket.', ops: ['joue au', 'fais au', 'joue de'], bien: 0 },
    },
    {
      id: 'imperativo',
      busca: /impératif|allons|et si on|on pourrait|tu veux/i,
      titulo: 'Fais-le !',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'Ouvre',       fin: ' la boîte !', frase: 'Le verbe tout seul.' },
        { arte: () => figura('triste', 'abajo'), pal: 'N\'ouvre pas', fin: ' la boîte !', frase: 'Pour dire non : ne… pas.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'Ouvrons',     fin: '-la !',      frase: 'Toi et moi ensemble.' },
      ],
      pie: 'Pas de je ni de tu devant — juste le verbe.',
      reto: { p: '___ pas dans le couloir !', ops: ['Ne cours', 'Non cours', 'Pas cours'], bien: 0 },
    },
    {
      id: 'adjetivo',
      busca: /adjectif|décrire|description|personnalité|en \+ matière|quel \+ adjectif/i,
      titulo: 'Comment c\'est ?',
      pasos: [
        { arte: () => caja(70, '#e8c49a'), pal: 'une grande',    fin: ' boîte',  frase: 'Grand, petit, joli : devant.' },
        { arte: () => caja(70, '#a8d0e8'), pal: 'une boîte',     fin: ' bleue',  frase: 'Les couleurs : derrière.' },
        { arte: () => caja(70, '#d8b0d0'), pal: 'la boîte est',  fin: ' bleue',  frase: 'Une boîte : bleue, avec un e.' },
      ],
      pie: 'L\'adjectif s\'habille comme le mot : bleu, bleue, bleus, bleues.',
      reto: { p: 'Laquelle est correcte ?', ops: ['une boîte rouge', 'une rouge boîte', 'une boîte rouges'], bien: 0 },
    },
    {
      id: 'gustar',
      busca: /aimer|adorer|j'aime/i,
      titulo: 'Oui merci, non merci',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'j\'aime',       fin: ' le gâteau', frase: 'Oui ! 😀' },
        { arte: () => figura('triste', 'abajo'), pal: 'je n\'aime pas', fin: ' le poisson', frase: 'Non… 🙁' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'tu aimes',      fin: ' le gâteau ?', frase: 'Demande à un ami !' },
      ],
      pie: 'Pour dire non, le ne… pas entoure le verbe.',
      reto: { p: 'Luna ___ les chats.', ops: ['n\'aime pas', 'pas aime', 'non aime'], bien: 0 },
    },
    {
      id: 'llevar',
      busca: /porter|emporter|je porte|mettre|il fait \+ adjectif/i,
      titulo: 'Qu\'est-ce que tu portes ?',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'je porte',     fin: ' un chapeau', frase: 'Sur moi, maintenant.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'elle porte',   fin: ' une écharpe', frase: 'Sur elle, maintenant.' },
        { arte: () => caja(66, '#e8c49a'),       pal: 'j\'emporte',   fin: ' un sac',     frase: 'Dans la main, pas sur moi !' },
      ],
      pie: 'Sur le corps ? porter. Dans la main ? emporter.',
      reto: { p: 'Erik ___ un grand sac bleu.', ops: ['porte', 'emporte', 'met'], bien: 1 },
    },
    {
      id: 'soy',
      busca: /je suis|il est|elle est|il s'appelle|un homme|une femme|un garçon/i,
      titulo: 'Qui est qui ?',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'je suis',   fin: ' Nico',   frase: 'Moi.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'il est',    fin: ' Nico',   frase: 'Un garçon.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'elle est',  fin: ' Astrid', frase: 'Une fille.' },
      ],
      pie: 'je, il, elle — un petit mot change tout.',
      reto: { p: '___ est ma sœur.', ops: ['Il', 'Elle', 'On'], bien: 1 },
    },
    {
      id: 'porque',
      busca: /parce que|alors|la cause|le résultat/i,
      titulo: 'Pourquoi ? et Alors ?',
      pasos: [
        { arte: () => figura('triste', 'abajo'), pal: 'je suis fatigué', fin: '',              frase: 'Ce qui se passe.' },
        { arte: () => figura('triste', 'abajo'), pal: 'parce que',       fin: ' j\'ai couru',  frase: 'La raison.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'alors',           fin: ' je m\'assois', frase: 'Ce qui arrive après.' },
      ],
      pie: 'parce que regarde en arrière. alors regarde devant.',
      reto: { p: 'Il pleuvait, ___ nous sommes restés à la maison.', ops: ['parce que', 'alors', 'mais'], bien: 1 },
    },
    {
      id: 'relativos',
      busca: /pronoms relatifs|qui, que/i,
      titulo: 'Une phrase, pas deux',
      pasos: [
        { arte: () => figura('feliz', 'abajo'), pal: 'la fille',  fin: ' qui court',    frase: 'qui — celui qui fait.' },
        { arte: () => bolas(1),                 pal: 'le livre',  fin: ' que je lis',   frase: 'que — celui qu\'on fait.' },
        { arte: () => caja(70, '#e8c49a'),      pal: 'la ville',  fin: ' où j\'habite', frase: 'où — pour les lieux.' },
      ],
      pie: 'qui fait, que subit, où situe.',
      reto: { p: 'C\'est le livre ___ j\'ai lu la semaine dernière.', ops: ['qui', 'que', 'où'], bien: 1 },
    },
    {
      id: 'manera',
      busca: /adverbe|bien, vite|-ment/i,
      titulo: 'Comment tu le fais ?',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'lent',   fin: '',      frase: 'Comment c\'est.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'lente',  fin: 'ment',  frase: 'Comment on le fait.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'bien',   fin: '',      frase: 'Celui-là ne prend pas -ment !' },
      ],
      pie: 'On part du féminin : lente → lentement.',
      reto: { p: 'Elle chante très ___ .', ops: ['bon', 'bien', 'bonnement'], bien: 1 },
    },
    {
      id: 'faire',
      busca: /les expressions avec faire|il fait \+ météo|il fait soleil/i,
      titulo: 'Le verbe faire est partout',
      pasos: [
        { arte: () => reloj(12),                 pal: 'il fait',  fin: ' beau',       frase: 'Pour le temps qu\'il fait.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'je fais',  fin: ' mes devoirs', frase: 'Pour le travail.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'je fais',  fin: ' du vélo',    frase: 'Et pour les sports.' },
      ],
      pie: 'Le temps, le travail, le sport : faire.',
      reto: { p: '___ froid aujourd\'hui.', ops: ['Il fait', 'Il est', 'C\'est'], bien: 0 },
    },
    {
      id: 'partitivo',
      busca: /partitif|du \/ de la|beaucoup de|un peu de|quelques|je prends/i,
      titulo: 'du, de la, des',
      pasos: [
        { arte: () => caja(70, '#e8c49a'), pal: 'du',     fin: ' pain',  frase: 'Le pain : du.' },
        { arte: () => caja(70, '#d8b0d0'), pal: 'de la',  fin: ' soupe', frase: 'La soupe : de la.' },
        { arte: () => bolas(3),            pal: 'des',    fin: ' pommes', frase: 'Plusieurs : des.' },
      ],
      pie: 'Une partie, pas le tout : du, de la, des.',
      reto: { p: 'Je voudrais ___ eau.', ops: ['du', 'de l\'', 'des'], bien: 1 },
    },
    {
      id: 'comparativo',
      busca: /comparatif|superlatif|plus .* que|le plus|le meilleur/i,
      titulo: 'Trois boîtes, trois phrases',
      pasos: [
        { arte: () => caja(64, '#e8c49a'),  pal: 'grande',        fin: '',        frase: 'Cette boîte est grande.' },
        { arte: () => caja(92, '#e0b784'),  pal: 'plus',          fin: ' grande', frase: 'Celle-là est plus grande !' },
        { arte: () => caja(124, '#d8a96c'), pal: 'la plus',       fin: ' grande', frase: 'Et celle-là est la plus grande !' },
      ],
      pie: 'plus… que pour comparer, le plus… pour gagner.',
      reto: { p: 'Cette boîte est ___ des trois.', ops: ['grande', 'plus grande', 'la plus grande'], bien: 2 },
    },
    {
      id: 'si',
      busca: /si \+ présent|quand \+ présent|peut-être|la possibilité/i,
      titulo: 'Si… alors',
      pasos: [
        { arte: () => reloj(12), pal: 's\'il pleut',  fin: ', je reste',   frase: 'La condition d\'abord.' },
        { arte: () => reloj(3),  pal: 'quand il pleut', fin: ', je reste', frase: 'quand : ça arrive toujours.' },
        { arte: () => reloj(9),  pal: 'peut-être',    fin: ' qu\'il pleut', frase: 'Ça, c\'est moins sûr !' },
      ],
      pie: 'Après si, on garde le présent.',
      reto: { p: '___ il fait beau, on sort.', ops: ['Si', 'Alors', 'Mais'], bien: 0 },
    },
    {
      id: 'demasiado',
      busca: /trop \+|pas assez/i,
      titulo: 'Trop, ou pas assez ?',
      pasos: [
        { arte: () => caja(124, '#d8a96c'), pal: 'trop',        fin: ' grande', frase: 'Elle ne passe pas la porte !' },
        { arte: () => caja(64, '#e8c49a'),  pal: 'pas assez',   fin: ' grande', frase: 'Tout ne rentre pas dedans.' },
        { arte: () => caja(92, '#e0b784'),  pal: 'assez',       fin: ' grande', frase: 'Celle-là va très bien.' },
      ],
      pie: 'trop, c\'est en excès. pas assez, c\'est en manque.',
      reto: { p: 'Le sac est ___ lourd, je ne peux pas le porter.', ops: ['trop', 'assez', 'pas assez'], bien: 0 },
    },
    {
      id: 'hay',
      busca: /il y a/i,
      titulo: 'Il y a',
      pasos: [
        { arte: () => bolas(1), pal: 'il y a',       fin: ' un ballon',    frase: 'Un seul.' },
        { arte: () => bolas(3), pal: 'il y a',       fin: ' trois ballons', frase: 'Ça ne change pas au pluriel !' },
        { arte: () => bolas(1), pal: 'il n\'y a pas', fin: ' de ballon',   frase: 'Et au négatif : pas de.' },
      ],
      pie: 'il y a reste pareil — c\'est ce qui suit qui change.',
      reto: { p: 'Dans la boîte ___ deux pommes.', ops: ['il y a', 'ils y ont', 'il y ont'], bien: 0 },
    },
  ];


  /* Las de repaso y las de estrategia de examen no llevan caja, igual que
     en ingles: no ensenan ninguna regla nueva. */
  const SIN_CAJA_FR = /bilan|stratégie|strategies/i;

  /* Las unidades de repaso y las de estrategia de examen no llevan caja a
     proposito: no ensenan ninguna regla nueva, repasan las que ya se
     dieron. Ponerles una seria decorado, y ademas se la quitaria a la
     unidad donde esa regla si se explica. */
  const SIN_CAJA = /review|revision|strategies|exam strategies|whole course|paper strategies/i;

  function familiaDe(ud) {
    const fr = window.LANG === 'fr';
    const t = ((ud.grammar || '') + ' ' + (ud.topic || '') + ' ' + (ud.title || '')).toLowerCase();
    if ((fr ? SIN_CAJA_FR : SIN_CAJA).test(t)) return null;
    return (fr ? FAMILIAS_FR : FAMILIAS).find(f => f.busca.test(t)) || null;
  }

  /* ---------- texto ---------- */
  const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  // La frase grande de un paso: lo que va entre [corchetes] se resalta.
  // Las familias viejas (pal + fin) se convierten al mismo formato.
  function frase(p) {
    const t = p.di != null ? String(p.di) : String(p.pal || '') + (p.fin ? '[' + p.fin + ']' : '');
    return {
      html: esc(t).replace(/\[([^\]]*)\]/g, '<span class="mb-fin">$1</span>'),
      texto: t.replace(/[\[\]]/g, ''),
    };
  }
  const habla_de = p => p.dice || (frase(p).texto + (p.nota || p.frase ? '. ' + (p.nota || p.frase) : ''));

  // La clase entera, en orden: gancho, tres pasos, regla, truco y reto.
  function guion(f) {
    const g = [];
    if (f.gancho) g.push({ t: f.gancho, foco: 'cofre' });
    f.pasos.forEach((p, i) => g.push({ t: habla_de(p), foco: i }));
    if (f.pie) g.push({ t: f.pie, foco: 'regla' });
    if (f.truco) g.push({ t: f.truco, foco: 'truco' });
    if (f.reto) g.push({ t: T('Now you! Choose the right word.', 'À toi ! Choisis le bon mot.'), foco: 'reto' });
    return g;
  }

  /* Todo lo que la profesora dice en ingles, para grabarlo con Edge TTS
     (tools/gen_audio_edge.py magicbox). Lo que no tenga mp3 lo lee el
     navegador, pero en el portatil del colegio no hay voces inglesas. */
  function lineas() {
    const out = new Set();
    FAMILIAS.forEach(f => {
      guion(f).forEach(l => out.add(l.t));
      if (f.reto) { if (f.reto.explica) out.add(f.reto.explica); if (f.reto.pista) out.add(f.reto.pista); }
    });
    return [...out];
  }

  /* ---------- la caja que se abre ---------- */
  function cofreHTML() {
    const chispas = [[-46, -34], [-24, -52], [6, -58], [32, -50], [52, -30], [-8, -44]].map(([dx, dy], i) => {
      const x = 80 + dx * .25, y = 44 + dy * .25, s = i % 2 ? 6 : 8;
      return `<g class="mb-chispa" style="--dx:${dx}px;--dy:${dy}px"><path d="M${x} ${y - s} l${s * .35} ${s * .65} ${s * .65} ${s * .35} -${s * .65} ${s * .35} -${s * .35} ${s * .65} -${s * .35} -${s * .65} -${s * .65} -${s * .35} ${s * .65} -${s * .35}z" fill="${i % 3 ? P.amarillo : P.naranja}"/></g>`;
    }).join('');
    return `<div class="mb-cofre" aria-hidden="true"><svg class="mb-cofre-svg" viewBox="0 0 160 90" width="150" height="84">
      <ellipse cx="80" cy="85" rx="50" ry="5" fill="${P.sombra}"/>
      ${chispas}
      <path d="M36 46 h88 v38 h-88z" fill="#e8c49a" stroke="#a9743f" stroke-width="2"/>
      <path d="M124 46 l16 -9 v38 l-16 9z" fill="#c99a63" stroke="#a9743f" stroke-width="2"/>
      <rect x="74" y="46" width="12" height="38" fill="#e05c4b"/>
      <g class="mb-tapa">
        <rect x="30" y="34" width="100" height="13" rx="3" fill="#f0d5b0" stroke="#a9743f" stroke-width="2"/>
        <path d="M130 34 l16 -9 v13 l-16 9z" fill="#d9b58a" stroke="#a9743f" stroke-width="2"/>
        <rect x="74" y="34" width="12" height="13" fill="#e05c4b"/>
        <ellipse cx="71" cy="28" rx="9" ry="5.5" fill="#e05c4b" transform="rotate(-25 71 28)"/>
        <ellipse cx="89" cy="28" rx="9" ry="5.5" fill="#e05c4b" transform="rotate(25 89 28)"/>
        <circle cx="80" cy="30" r="4.5" fill="#b7453a"/>
      </g>
    </svg></div>`;
  }

  /* SAY es un const del script de index.html: se ve por su nombre desde
     aqui, pero NO existe window.SAY (por eso las tarjetas nunca sonaron).
     Se resuelve al usarlo, porque este archivo carga antes que ese script. */
  const say = () => (typeof SAY !== 'undefined' ? SAY : window.SAY) || null;

  /* ---------- hablar y esperar ----------
     SAY.frase no devuelve nada, asi que se espera a que el boton pierda
     la clase .saying (y a que la voz del navegador termine si fue ella).
     Aunque no suene nada, cada linea se queda en pantalla el tiempo de
     leerla: la clase funciona igual con el sonido apagado. */
  const espera = ms => new Promise(r => setTimeout(r, ms));
  function habla(t, btn, vivo) {
    return new Promise(res => {
      const t0 = Date.now(), minimo = t0 + 900 + t.length * 42;
      const S = say();
      if (!S || !btn) return setTimeout(res, minimo - t0);
      S.frase(t, btn, 'grammar');
      const tick = () => {
        if (vivo && !vivo()) { S.parar(); return res(); }   // cambio de pantalla a media frase
        const suena = btn.classList.contains('saying') || (window.speechSynthesis && speechSynthesis.speaking);
        if ((suena && Date.now() < t0 + 25000) || Date.now() < minimo) return setTimeout(tick, 120);
        res();
      };
      setTimeout(tick, 200);
    });
  }

  function confeti(cont) {
    const colores = [P.rojo, P.amarillo, P.verde, P.azul, P.rosa, P.morado, P.naranja];
    for (let i = 0; i < 16; i++) {
      const s = document.createElement('span');
      s.className = 'mb-conf';
      const a = (i / 16) * Math.PI * 2, d = 60 + Math.random() * 70;
      s.style.setProperty('--dx', Math.round(Math.cos(a) * d) + 'px');
      s.style.setProperty('--dy', Math.round(Math.sin(a) * d - 30) + 'px');
      s.style.background = colores[i % colores.length];
      s.style.animationDelay = (Math.random() * .15) + 's';
      cont.appendChild(s);
      setTimeout(() => s.remove(), 1200);
    }
  }

  function para(ud) {
    const f = familiaDe(ud);
    if (!f) return null;                    // sin caja vacia: mejor nada

    const pasos = f.pasos.map((p, i) => `
      <button class="mb-paso" type="button" data-i="${i}">
        <span class="mb-num">${i + 1}</span>
        ${p.arte()}
        <span class="mb-pal">${frase(p).html}</span>
        <p class="mb-nota">${esc(p.nota != null ? p.nota : p.frase)}</p>
      </button>`).join('');

    const reto = f.reto ? `
      <div class="mb-reto">
        <p>${esc(f.reto.p)}</p>
        <div class="mb-ops">${f.reto.ops.map((o, i) =>
          `<button class="mb-op" type="button" data-i="${i}">${esc(o)}</button>`).join('')}</div>
        <p class="mb-eco" role="status"></p>
      </div>` : '';

    const conClase = !!f.gancho;   // la tabla francesa todavia no tiene guion

    return {
      titulo: T('🎁 The Magic Box — ', '🎁 La Boîte Magique — ') + f.titulo,
      html: `<style>${CSS}</style><div class="mb">
        <div class="mb-cabeza">${cofreHTML()}${conClase ? `<button class="mb-ver" type="button">▶ ${T('Show me!', 'Montre-moi !')}</button>` : ''}</div>
        <div class="mb-tira">${pasos}</div>
        <button class="mb-regla" type="button">${esc(f.pie)}</button>
        ${f.truco ? `<button class="mb-truco" type="button"><span class="ico">💡</span><span>${esc(f.truco)}</span></button>` : ''}
        ${reto}
      </div>`,
      alMostrar(el) {
        const raiz = el.querySelector('.mb');
        if (!raiz) return;
        const guia = el.querySelector('.guia'), globo = el.querySelector('.guia-globo');
        const bocaP = globo && globo.querySelector('p'), bocaBtn = globo && globo.querySelector('.guia-say');
        const ver = raiz.querySelector('.mb-ver');
        const tarjetas = [...raiz.querySelectorAll('.mb-paso')];
        const regla = raiz.querySelector('.mb-regla'), truco = raiz.querySelector('.mb-truco'), retoEl = raiz.querySelector('.mb-reto');
        const vivo = () => document.body.contains(raiz);
        const estado = { viva: false, id: 0, respondido: false };

        // la mascota dice la linea: se lee en el bocadillo y Listen la repite
        const dice = t => {
          if (bocaP) bocaP.textContent = t;
          if (bocaBtn) bocaBtn.onclick = () => { parar(); if (say()) say().frase(t, bocaBtn, 'grammar'); };
        };
        const foco = k => {
          tarjetas.forEach((b, i) => b.classList.toggle('on', k === i));
          regla && regla.classList.toggle('on', k === 'regla');
          truco && truco.classList.toggle('on', k === 'truco');
          retoEl && retoEl.classList.toggle('on', k === 'reto');
        };
        const parar = () => {
          estado.viva = false; estado.id++;
          guia && guia.classList.remove('mb-habla');
          if (ver) { ver.classList.remove('on'); ver.textContent = '▶ ' + T('Show me!', 'Montre-moi !'); }
        };
        async function clase() {
          parar();
          const id = ++estado.id; estado.viva = true;
          if (ver) { ver.classList.add('on'); ver.classList.remove('pide'); ver.textContent = '■ ' + T('Stop', 'Stop'); }
          for (const linea of guion(f)) {
            if (!estado.viva || estado.id !== id || !vivo()) return;
            foco(linea.foco);
            dice(linea.t);
            guia && guia.classList.add('mb-habla');
            await habla(linea.t, bocaBtn, vivo);
            guia && guia.classList.remove('mb-habla');
            if (!estado.viva || estado.id !== id) return;
            const otro = document.querySelector('.saying');
            if (otro && otro !== bocaBtn) return parar();     // alguien pulso otra cosa
            await espera(420);
          }
          if (estado.id !== id) return;
          parar();
          // si nadie contesta en un rato, las opciones piden el clic
          setTimeout(() => { if (vivo() && !estado.respondido && !estado.viva) raiz.querySelectorAll('.mb-op').forEach(o => o.classList.add('pide')); }, 9000);
        }

        if (ver) ver.onclick = () => { if (estado.viva) { parar(); if (say()) say().parar(); } else clase(); };

        tarjetas.forEach(b => b.onclick = () => {
          parar();
          const i = +b.dataset.i, p = f.pasos[i], t = conClase ? habla_de(p) : frase(p).texto;
          foco(i); dice(t);
          if (say()) say().frase(t, bocaBtn || b, 'grammar');
        });
        if (regla) regla.onclick = () => { parar(); foco('regla'); dice(f.pie); if (say()) say().frase(f.pie, bocaBtn || regla, 'grammar'); };
        if (truco) truco.onclick = () => { parar(); foco('truco'); dice(f.truco); if (say()) say().frase(f.truco, bocaBtn || truco, 'grammar'); };

        if (f.reto) {
          const eco = raiz.querySelector('.mb-eco');
          raiz.querySelectorAll('.mb-op').forEach(b => b.onclick = () => {
            parar();
            const bien = +b.dataset.i === f.reto.bien;
            b.classList.remove('mal'); void b.offsetWidth;        // que tiemble otra vez
            b.classList.add(bien ? 'bien' : 'mal');
            raiz.querySelectorAll('.mb-op').forEach(o => o.classList.remove('pide'));
            const t = bien ? (f.reto.explica || '') : (f.reto.pista || '');
            eco.textContent = (bien ? T('Yes! ⭐', 'Oui ! ⭐') : T('Try another one…', 'Essaie encore…')) + (t ? ' ' + t : '');
            eco.style.color = bien ? '' : 'var(--bad)';
            if (t) { dice(t); if (say()) say().frase(t, bocaBtn || b, 'grammar'); }
            if (bien) { estado.respondido = true; raiz.querySelectorAll('.mb-op').forEach(o => o.disabled = true); confeti(retoEl); }
          });
        }

        // se abre la caja y, si hay clase, empieza sola: el movimiento y la
        // voz tienen que llegar antes de que el nino mire a otro lado
        requestAnimationFrame(() => raiz.classList.add('abierta'));
        if (conClase) setTimeout(() => { if (vivo() && !estado.viva && estado.id === 0) clase(); }, 1100);
      },
    };
  }

  return { para, familiaDe, FAMILIAS, FAMILIAS_FR, lineas };
})();
