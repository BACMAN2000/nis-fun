/* Portada animada de cada nivel — Fun for Nordic.
 *
 * La portada es la primera pantalla del nivel y compite con los videos de
 * las mascotas, que llevan fondos ilustrados con profundidad. El faro plano
 * de formas geometricas no daba la talla: el mar eran rayas, la arena una
 * mancha lisa y los ninos, que son 3D, se veian pegados encima.
 *
 * Ahora la escena esta construida por planos, como una ilustracion:
 *   cielo con degradado y calima -> montanas del fiordo con nieve ->
 *   mar en bandas de profundidad con el rielar del astro -> isla de roca
 *   con hierba -> el faro con volumen -> playa -> primer plano de rocas.
 * Encima va el grano y el gradeado de color de la hora, que es lo que cose
 * a los personajes con el fondo, y cada nino lleva su sombra de contacto en
 * la arena.
 *
 * El mismo faro sirve para los tres niveles, con distinta hora del dia, que
 * es lo que los distingue de un vistazo:
 *   Starters  manana clara
 *   Movers    atardecer en el fiordo
 *   Flyers    noche con aurora
 *
 * Todo es SVG y CSS, sin imagenes de fondo: pesa nada y se adapta a
 * cualquier ancho. Con "reducir movimiento" activado se queda quieto.
 *
 * Si algun dia hay lamina ilustrada del faro (assets/scenes/lighthouse-
 * <nivel>.jpg, del mismo sitio que salen las escenas de las unidades), se
 * pinta encima y el SVG queda debajo de respaldo: ver LAMINA.
 *
 * Uso:  BANNER.html(idx, LEVEL)  ->  el HTML de la pantalla
 *       BANNER.vivo(el)          ->  engancha los saludos
 */
window.BANNER = (function () {

  const HORA = {
    starters: {
      // del alto del cielo hacia el horizonte
      cielo: ['#4fb0e6', '#8fd2f0', '#cfeafa', '#f2fbfe'],
      calima: 'rgba(255,255,255,.62)',
      // del horizonte hacia la orilla: el agua aclara al perder fondo
      mar: ['#1b6b91', '#2a86ad', '#41a5c7', '#84cfe0'],
      monteLejos: '#a9c8da', monteMedio: '#87aec5', monteCerca: '#6d97b0',
      nieve: '#f8fcfe',
      roca: ['#a3907a', '#6d6052'], rocaLuz: '#c2ad92',
      hierba: ['#74b45f', '#3d7742'],
      arenaSeca: ['#f6e8c8', '#e7d2a6'], arenaMojada: '#d7c193',
      astroX: 706, astroY: 108, astroR: 40, astroHalo: 168,
      astro: '#fff8d0', astroLuz: 'rgba(255,238,175,.7)',
      nubeLuz: '#ffffff', nubeSombra: 'rgba(122,152,182,.42)',
      reflejo: 'rgba(255,240,190,.30)',
      haz: 'rgba(255,246,200,.50)',
      torre: ['#ffffff', '#efe9dd', '#c8bfae'],   // luz, medio, sombra
      texto: '#0f3149', sombraTexto: '0 2px 14px rgba(255,255,255,.75)',
      tinte: 'rgba(255,214,140,.10)', tinteModo: 'soft-light',
      ave: '#3f5568', aurora: false, estrellas: 0,
    },
    movers: {
      cielo: ['#3f6fa8', '#c98db0', '#f9c88f', '#fde3c4'],
      calima: 'rgba(255,214,168,.55)',
      mar: ['#123a5c', '#1f5b83', '#2f7ba2', '#5ba3b8'],
      monteLejos: '#9d86a8', monteMedio: '#7b6790', monteCerca: '#5b5175',
      nieve: '#ffe6d6',
      roca: ['#8a7360', '#54453c'], rocaLuz: '#b3937a',
      hierba: ['#5f9153', '#31603a'],
      arenaSeca: ['#f0d7ab', '#d8b787'], arenaMojada: '#c9a67d',
      // el sol de movers se hunde: el mar se pinta despues y lo parte
      astroX: 664, astroY: 238, astroR: 58, astroHalo: 250,
      astro: '#ffbe6e', astroLuz: 'rgba(255,150,80,.6)',
      nubeLuz: '#ffe2c6', nubeSombra: 'rgba(158,92,120,.45)',
      reflejo: 'rgba(255,168,96,.40)',
      haz: 'rgba(255,220,150,.55)',
      torre: ['#fbeede', '#e6d3bc', '#b79b83'],
      texto: '#3a1c0e', sombraTexto: '0 2px 14px rgba(255,238,210,.7)',
      tinte: 'rgba(255,146,66,.16)', tinteModo: 'soft-light',
      ave: '#4a3a45', aurora: false, estrellas: 0,
    },
    flyers: {
      cielo: ['#070f26', '#12224a', '#22375f', '#3a5578'],
      calima: 'rgba(150,190,230,.20)',
      mar: ['#0a1a2e', '#102841', '#173753', '#22506b'],
      monteLejos: '#2b3a5c', monteMedio: '#22304d', monteCerca: '#1a2740',
      nieve: '#cfe0f5',
      roca: ['#3b3f52', '#20222f'], rocaLuz: '#565b73',
      hierba: ['#2c5a48', '#173328'],
      arenaSeca: ['#5c6884', '#3c4661'], arenaMojada: '#333c54',
      astroX: 700, astroY: 96, astroR: 28, astroHalo: 126,
      astro: '#f4f8ff', astroLuz: 'rgba(205,225,255,.34)',
      nubeLuz: '#c6d8f0', nubeSombra: 'rgba(20,38,72,.55)',
      reflejo: 'rgba(200,225,255,.26)',
      haz: 'rgba(190,232,255,.55)',
      torre: ['#dfe7f2', '#b9c4d6', '#8592ab'],
      texto: '#eaf2ff', sombraTexto: '0 2px 16px rgba(6,14,32,.85)',
      tinte: 'rgba(56,96,168,.13)', tinteModo: 'multiply',
      ave: '#9fb6d6', aurora: true, estrellas: 64,
    },
  };

  // Quien lleva la voz cantante en la portada de cada nivel.
  const ANFITRION = { starters: 'freya', movers: 'valentina', flyers: 'ingrid' };

  // Cuando haya lamina ilustrada del faro para un nivel, se anade aqui y
  // pasa a pintarse encima del SVG. Vacio = nadie la pide, que es mejor que
  // pedirla y comerse un 404 en cada carga.
  const CON_LAMINA = new Set([]);
  const LAMINA = n => `../assets/scenes/lighthouse-${n}.jpg?v=${window.ART_V || ''}`;

  const CSS = `
  .lh{position:relative;width:100%;max-width:64rem;margin:0 auto;border-radius:20px;
    overflow:hidden;box-shadow:0 18px 44px rgba(16,38,66,.28);isolation:isolate}
  .lh svg{display:block;width:100%;height:auto}
  .lh-lamina{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
    display:block;z-index:1}
  /* vineta: cierra la escena por los bordes y centra la mirada */
  .lh::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:4;
    background:radial-gradient(120% 88% at 50% 42%,rgba(0,0,0,0) 52%,rgba(8,22,40,.30) 100%)}
  .lh-capa{position:absolute;inset:0;display:flex;flex-direction:column;
    justify-content:space-between;padding:4.4% 5% 0;pointer-events:none;z-index:3}
  .lh-tit{text-align:left;pointer-events:none;max-width:62%}
  .lh-tit h1{margin:0;font-family:"Baloo 2",sans-serif;font-size:clamp(1.05rem,2.8vw,2.05rem);
    line-height:1.1;letter-spacing:-.01em}
  .lh-cast{margin:.3rem 0 0;font-family:"Baloo 2",sans-serif;font-weight:800;
    font-size:clamp(.78rem,2vw,1.35rem);letter-spacing:.1em;text-transform:uppercase;
    opacity:.92}
  .lh-elenco{display:flex;align-items:flex-end;justify-content:center;gap:.4%;
    pointer-events:auto;padding-bottom:2.2%}
  .lh-nino{background:none;border:0;padding:0;cursor:pointer;position:relative;
    flex:0 1 auto;line-height:0;transition:transform .2s cubic-bezier(.2,.8,.3,1);
    transform:translateY(var(--fondo,0px))}
  /* la sombra de contacto: sin esto los ninos flotan sobre la arena */
  .lh-nino::before{content:"";position:absolute;left:50%;bottom:1%;
    width:76%;height:8%;transform:translateX(-50%);border-radius:50%;
    background:radial-gradient(50% 50% at 50% 50%,rgba(22,28,20,.45),rgba(22,28,20,0) 70%);
    pointer-events:none}
  .lh-nino img{height:calc(clamp(88px,19.5vw,200px) * var(--esc,1));width:auto;display:block;
    filter:drop-shadow(0 10px 12px rgba(12,26,44,.30)) saturate(var(--sat,1)) brightness(var(--bri,1))}
  .lh-nino:hover{transform:translateY(calc(var(--fondo,0px) - 7px))}
  .lh-nino.mascota img{height:calc(clamp(62px,13.5vw,138px) * var(--esc,1))}

  /* el bocadillo: el del anfitrion aparece solo, los demas al pulsar */
  .lh-globo{position:absolute;left:50%;bottom:calc(100% - 6px);transform:translateX(-50%) scale(.6);
    background:#fff;color:#1d3a52;border-radius:14px;padding:.3rem .7rem;white-space:nowrap;
    font-family:"Baloo 2",sans-serif;font-weight:800;font-size:clamp(.7rem,1.7vw,1.05rem);
    box-shadow:0 6px 16px rgba(20,40,70,.34);opacity:0;pointer-events:none}
  .lh-globo::after{content:"";position:absolute;top:100%;left:50%;transform:translateX(-50%);
    border:7px solid transparent;border-top-color:#fff}
  .lh-nino.saluda .lh-globo{animation:lhglobo 3.4s ease-in-out infinite}
  .lh-nino.dice .lh-globo{animation:lhpop .9s ease-out}

  @keyframes lhglobo{
    0%,58%{opacity:0;transform:translateX(-50%) scale(.6)}
    8%,46%{opacity:1;transform:translateX(-50%) scale(1)}
    52%{opacity:0;transform:translateX(-50%) scale(.9)} }
  @keyframes lhpop{
    0%{opacity:0;transform:translateX(-50%) scale(.6)}
    18%{opacity:1;transform:translateX(-50%) scale(1.06)}
    80%{opacity:1;transform:translateX(-50%) scale(1)}
    100%{opacity:0;transform:translateX(-50%) scale(.95)} }

  /* el mar: el dibujo de la espuma encaja consigo mismo al repetirse, asi
     el vaiven no tiene principio ni final visible */
  .lh-ola{animation:lhola linear infinite}
  @keyframes lhola{from{transform:translateX(0)}to{transform:translateX(-400px)}}
  .lh-luz{transform-origin:var(--fx) var(--fy);animation:lhgira 8s linear infinite}
  @keyframes lhgira{from{transform:rotate(0)}to{transform:rotate(360deg)}}
  .lh-foco{animation:lhbrilla 8s ease-in-out infinite}
  @keyframes lhbrilla{0%,100%{opacity:.5}20%{opacity:1}40%{opacity:.55}}
  .lh-nube{animation:lhnube linear infinite}
  @keyframes lhnube{from{transform:translateX(1320px)}to{transform:translateX(-420px)}}
  .lh-ave{animation:lhave 9s ease-in-out infinite}
  @keyframes lhave{0%,100%{transform:translate(0,0)}50%{transform:translate(30px,-14px)}}
  .lh-aurora{animation:lhaurora 14s ease-in-out infinite}
  @keyframes lhaurora{0%,100%{opacity:.6;transform:translateY(0) scaleY(1)}
    50%{opacity:1;transform:translateY(-14px) scaleY(1.1)}}
  .lh-titila{animation:lhtitila ease-in-out infinite}
  @keyframes lhtitila{0%,100%{opacity:.2}50%{opacity:1}}
  .lh-rielar{animation:lhrielar 6s ease-in-out infinite}
  @keyframes lhrielar{0%,100%{opacity:.8}50%{opacity:1}}

  @media (max-width:640px){
    .lh-capa{padding:3.4% 4% 0}
    .lh-elenco{gap:0}
    .lh-tit{max-width:72%}
  }
  @media (prefers-reduced-motion:reduce){
    .lh-ola,.lh-luz,.lh-foco,.lh-nube,.lh-ave,.lh-aurora,.lh-titila,.lh-rielar,
    .lh-nino.saluda .lh-globo{animation:none}
    .lh-nino.saluda .lh-globo{opacity:1;transform:translateX(-50%) scale(1)}
  }`;

  /* ---- piezas del dibujo ---------------------------------------------- */

  // Espuma de 400 de ancho que encaja consigo misma al repetirse.
  function espuma(y, alto) {
    let d = `M0 ${y}`;
    for (let x = 0; x < 1700; x += 200) d += ` q50 ${-alto} 100 0 t100 0`;
    return d;
  }

  // Cordillera del fiordo: dientes de sierra con las cimas nevadas. Las
  // medidas van escritas una a una para que no salgan dos picos iguales.
  //
  // La nieve no es un parche pegado encima: se calcula sobre las dos
  // aristas del propio pico y se cierra con un borde dentado, que es como
  // baja la nieve de verdad por las vaguadas.
  function sierra(base, picos, color, nieve, nivelNieve) {
    let d = `M-40 ${base}`, cimas = '', x = -40;
    picos.forEach(([ancho, alto]) => {
      const izq = x, der = x + ancho;
      const cx = izq + ancho / 2, cy = base - alto;
      const derY = base - alto * .18;               // la ladera derecha cae menos
      d += ` L${cx} ${cy} L${der} ${derY}`;
      if (nieve && alto > nivelNieve) {
        const t = .34;                              // hasta donde baja la nieve
        const ax = cx + (izq - cx) * t, ay = cy + (base - cy) * t;
        const bx = cx + (der - cx) * t, by = cy + (derY - cy) * t;
        const mx = (ax + bx) / 2, my = (ay + by) / 2;
        cimas += `<path d="M${cx.toFixed(1)} ${cy.toFixed(1)}
          L${bx.toFixed(1)} ${by.toFixed(1)}
          L${(mx + (bx - mx) * .45).toFixed(1)} ${(my - alto * .07).toFixed(1)}
          L${mx.toFixed(1)} ${(my + alto * .05).toFixed(1)}
          L${(mx + (ax - mx) * .5).toFixed(1)} ${(my - alto * .06).toFixed(1)}
          L${ax.toFixed(1)} ${ay.toFixed(1)} Z" fill="${nieve}" opacity=".92"/>`;
      }
      x += ancho;
    });
    d += ` L${x} ${base + 80} L-40 ${base + 80} Z`;
    return `<path d="${d}" fill="${color}"/>${cimas}`;
  }

  // Abeto: la conifera de tres cuerpos, con su lado en sombra. Es lo que
  // hace nordica la loma del faro.
  function abeto(x, y, alto, claro, oscuro) {
    const w = alto * .52;
    return `<g transform="translate(${x} ${y})">
      <rect x="${-alto * .045}" y="${-alto * .12}" width="${alto * .09}" height="${alto * .14}" fill="#5a4433"/>
      <path d="M0 ${-alto} L${w / 2} ${-alto * .58} L${-w / 2} ${-alto * .58} Z" fill="${claro}"/>
      <path d="M0 ${-alto * .78} L${w * .58} ${-alto * .33} L${-w * .58} ${-alto * .33} Z" fill="${claro}"/>
      <path d="M0 ${-alto * .54} L${w * .66} ${-alto * .08} L${-w * .66} ${-alto * .08} Z" fill="${claro}"/>
      <path d="M0 ${-alto} L${w / 2} ${-alto * .58} L0 ${-alto * .58} Z" fill="${oscuro}" opacity=".5"/>
      <path d="M0 ${-alto * .78} L${w * .58} ${-alto * .33} L0 ${-alto * .33} Z" fill="${oscuro}" opacity=".5"/>
      <path d="M0 ${-alto * .54} L${w * .66} ${-alto * .08} L0 ${-alto * .08} Z" fill="${oscuro}" opacity=".5"/>
    </g>`;
  }

  // Velero lejano: da escala al mar y dice que el sitio esta vivo.
  function velero(x, y, e, vela, casco) {
    return `<g transform="translate(${x} ${y}) scale(${e})" opacity=".9">
      <path d="M0 0 L0 -34 L22 -6 Z" fill="${vela}"/>
      <path d="M-2 -2 L-2 -28 L-18 -2 Z" fill="${vela}" opacity=".85"/>
      <path d="M-22 0 L24 0 L18 9 L-16 9 Z" fill="${casco}"/>
    </g>`;
  }

  // Nube con volumen: masa clara arriba y su propia sombra debajo, no tres
  // elipses blancas.
  function nube(y, e, op, luz, sombra) {
    return `<g transform="translate(0 ${y}) scale(${e})" opacity="${op}" filter="url(#suave)">
      <g fill="${sombra}">
        <ellipse cx="4" cy="13" rx="62" ry="17"/><ellipse cx="46" cy="16" rx="34" ry="13"/>
        <ellipse cx="-42" cy="16" rx="30" ry="12"/></g>
      <g fill="${luz}">
        <ellipse cx="0" cy="0" rx="44" ry="25"/><ellipse cx="38" cy="8" rx="33" ry="18"/>
        <ellipse cx="-36" cy="9" rx="28" ry="16"/><ellipse cx="14" cy="-14" rx="26" ry="17"/></g>
    </g>`;
  }

  // El faro. Un faro de verdad es esbelto —alto como tres o cuatro veces su
  // base—, asi que la torre va de la roca hasta media pantalla; el degradado
  // la redondea y las bandas rojas van curvadas para que sigan el cilindro.
  function faro(c, FX, FY, BASE) {
    const PIE = BASE - 18, TECHO = 152;            // el fuste, de abajo arriba
    const ANCHO_PIE = 68, ANCHO_TECHO = 46;
    // el fuste se estrecha con la altura: aqui se mide cuanto
    const ancho = y => ANCHO_TECHO + (ANCHO_PIE - ANCHO_TECHO) *
                       (y - TECHO) / (PIE - TECHO);
    const banda = (y, h) => {
      const w = ancho(y), x = FX - w / 2, cur = w * .13;
      return `<path d="M${x.toFixed(1)} ${y} q${(w / 2).toFixed(1)} ${cur.toFixed(1)} ${w.toFixed(1)} 0
        l0 ${h} q${(-w / 2).toFixed(1)} ${cur.toFixed(1)} ${(-w).toFixed(1)} 0 Z"
        fill="#d94f3d"/>`;
    };
    const wPie = ANCHO_PIE, wTecho = ANCHO_TECHO;
    return `
    <g>
      <!-- la sombra cae a la derecha, que es de donde no viene la luz -->
      <ellipse cx="${FX + 26}" cy="${BASE + 8}" rx="86" ry="17"
               fill="rgba(16,24,16,.32)" filter="url(#suave)"/>
      <!-- zocalo de piedra -->
      <path d="M${FX - 62} ${BASE + 6} q62 -16 124 0 l-14 -30 q-48 -12 -96 0 Z" fill="${c.roca[1]}"/>
      <path d="M${FX - 62} ${BASE + 6} q62 -16 124 0 l-14 -30 q-48 -12 -96 0 Z"
            fill="none" stroke="rgba(255,255,255,.18)" stroke-width="2"/>
      <!-- fuste troncoconico -->
      <path d="M${FX - wPie / 2} ${PIE} q${wPie / 2} ${wPie * .12} ${wPie} 0
               L${FX + wTecho / 2} ${TECHO} q${-wTecho / 2} ${-wTecho * .12} ${-wTecho} 0 Z"
            fill="url(#torre)"/>
      ${banda(PIE - 46, 28)}${banda(TECHO + 26, 24)}
      <!-- puerta arqueada y ventanas en linea -->
      <path d="M${FX - 10} ${PIE - 2} q10 -26 20 0 l0 24 q-10 4 -20 0 Z" fill="#4a3a2c" opacity=".8"/>
      <rect x="${FX - 6}" y="${PIE - 76}" width="12" height="18" rx="6" fill="#2c4256" opacity=".9"/>
      <rect x="${FX - 4}" y="${PIE - 74}" width="4" height="8" rx="2" fill="rgba(255,255,255,.55)"/>
      <rect x="${FX - 6}" y="${TECHO + 62}" width="12" height="18" rx="6" fill="#2c4256" opacity=".9"/>
      <rect x="${FX - 4}" y="${TECHO + 64}" width="4" height="8" rx="2" fill="rgba(255,255,255,.55)"/>
      <!-- galeria con su barandilla -->
      <path d="M${FX - 40} ${TECHO} q40 -9 80 0 l-7 -13 q-33 -7 -66 0 Z" fill="#33506b"/>
      <rect x="${FX - 44}" y="${TECHO - 20}" width="88" height="8" rx="4" fill="#3d5c78"/>
      <g stroke="#33506b" stroke-width="2.6">
        <path d="M${FX - 32} ${TECHO - 12} v-9"/><path d="M${FX - 16} ${TECHO - 13} v-9"/>
        <path d="M${FX} ${TECHO - 13} v-9"/><path d="M${FX + 16} ${TECHO - 13} v-9"/>
        <path d="M${FX + 32} ${TECHO - 12} v-9"/></g>
      <!-- linterna: cristal, foco y reflejo del vidrio -->
      <rect x="${FX - 25}" y="${FY - 22}" width="50" height="52" rx="6" fill="#2f4a63"/>
      <rect x="${FX - 20}" y="${FY - 17}" width="40" height="42" rx="3" fill="url(#cristal)"/>
      <circle class="lh-foco" cx="${FX}" cy="${FY}" r="16" fill="#fff8dc" filter="url(#glow)"/>
      <rect x="${FX - 19}" y="${FY - 17}" width="9" height="42" fill="rgba(255,255,255,.25)"/>
      <!-- cupula y veleta -->
      <path d="M${FX - 30} ${FY - 22} Q${FX} ${FY - 62} ${FX + 30} ${FY - 22} Z" fill="#33506b"/>
      <path d="M${FX - 30} ${FY - 22} Q${FX} ${FY - 62} ${FX} ${FY - 62} L${FX} ${FY - 22} Z"
            fill="rgba(255,255,255,.16)"/>
      <rect x="${FX - 3}" y="${FY - 80}" width="6" height="20" fill="#33506b"/>
      <circle cx="${FX}" cy="${FY - 83}" r="5" fill="#d94f3d"/>
    </g>`;
  }

  function fondo(nivel) {
    const c = HORA[nivel] || HORA.starters;
    const FX = 1002, FY = 104;          // el foco del faro
    const HOR = 248, ORILLA = 356;      // horizonte y linea de la orilla
    const BASE = 302;                   // donde se planta el faro en la roca

    const estrellas = c.estrellas ? Array.from({ length: c.estrellas }, (_, i) => {
      const x = (i * 137) % 1180 + 10, y = (i * 71) % 210 + 6;
      const r = i % 4 === 0 ? 1.9 : i % 3 === 0 ? 1.4 : 1;
      return `<circle class="lh-titila" cx="${x}" cy="${y}" r="${r}" fill="#fff"
        style="animation-duration:${2 + (i % 5) * .7}s;animation-delay:${(i % 7) * .4}s"/>`;
    }).join('') : '';

    // Aurora: tres cintas de distinto color y velocidad, onduladas con ruido
    // y difuminadas, que es lo que la separa de un trazo verde.
    const aurora = c.aurora ? `
      <g filter="url(#velo)">
        <!-- el resplandor de fondo: sin el, las cintas parecen pegatinas -->
        <ellipse cx="820" cy="150" rx="440" ry="150" fill="url(#auHalo)" opacity=".5"/>
        <g class="lh-aurora" style="animation-duration:13s">
          <path d="M120 146 Q400 26 700 104 T1260 46 L1260 -30 L120 -30 Z" fill="url(#au1)"/></g>
        <g class="lh-aurora" style="animation-duration:17s;animation-delay:-4s">
          <path d="M60 198 Q420 74 780 156 T1260 100 L1260 12 L60 12 Z" fill="url(#au2)"/></g>
        <g class="lh-aurora" style="animation-duration:21s;animation-delay:-9s">
          <path d="M180 232 Q520 140 880 204 T1260 152 L1260 66 L180 66 Z" fill="url(#au3)"/></g>
        <!-- los rayos verticales, que es lo que hace que parezca una aurora -->
        <g class="lh-aurora" style="animation-duration:11s;animation-delay:-2s" opacity=".6">
          <path d="M560 40 l16 0 l-8 176 Z" fill="#5cf0b8"/>
          <path d="M700 24 l18 0 l-9 190 Z" fill="#7ef0c8"/>
          <path d="M860 46 l14 0 l-7 164 Z" fill="#59d8e8"/>
          <path d="M980 30 l16 0 l-8 180 Z" fill="#8fd0f4"/>
          <path d="M1100 52 l14 0 l-7 150 Z" fill="#6ce0c0"/></g>
      </g>` : '';

    // El rielar del astro en el agua: trazos que se ensanchan al acercarse,
    // no una mancha.
    const rielar = Array.from({ length: 13 }, (_, i) => {
      const y = HOR + 5 + i * 8;
      const w = 10 + i * 5.4 + (i % 3) * 6;
      return `<rect x="${(c.astroX - w / 2).toFixed(1)}" y="${y}" width="${w.toFixed(1)}"
        height="${i < 4 ? 3 : 4}" rx="2" fill="${c.reflejo}" opacity="${(1 - i * .055).toFixed(2)}"/>`;
    }).join('');

    return `
    <svg viewBox="0 0 1200 520" role="img"
         aria-label="A lighthouse on the rocks by the sea, with the Nordic characters waving.">
      <defs>
        <linearGradient id="cielo" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="${c.cielo[0]}"/>
          <stop offset=".42" stop-color="${c.cielo[1]}"/>
          <stop offset=".76" stop-color="${c.cielo[2]}"/>
          <stop offset="1" stop-color="${c.cielo[3]}"/>
        </linearGradient>
        <linearGradient id="mar" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="${c.mar[0]}"/>
          <stop offset=".38" stop-color="${c.mar[1]}"/>
          <stop offset=".72" stop-color="${c.mar[2]}"/>
          <stop offset="1" stop-color="${c.mar[3]}"/>
        </linearGradient>
        <linearGradient id="arena" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="${c.arenaMojada}"/>
          <stop offset=".22" stop-color="${c.arenaSeca[0]}"/>
          <stop offset="1" stop-color="${c.arenaSeca[1]}"/>
        </linearGradient>
        <linearGradient id="torre" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="${c.torre[2]}"/>
          <stop offset=".16" stop-color="${c.torre[1]}"/>
          <stop offset=".44" stop-color="${c.torre[0]}"/>
          <stop offset=".80" stop-color="${c.torre[1]}"/>
          <stop offset="1" stop-color="${c.torre[2]}"/>
        </linearGradient>
        <linearGradient id="roca" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="${c.rocaLuz}"/>
          <stop offset="1" stop-color="${c.roca[1]}"/>
        </linearGradient>
        <linearGradient id="hierba" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="${c.hierba[0]}"/>
          <stop offset="1" stop-color="${c.hierba[1]}"/>
        </linearGradient>
        <linearGradient id="calima" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="${c.calima}" stop-opacity="0"/>
          <stop offset="1" stop-color="${c.calima}"/>
        </linearGradient>
        <linearGradient id="au1" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="#4be0b0" stop-opacity="0"/>
          <stop offset=".42" stop-color="#57f0b4" stop-opacity="1"/>
          <stop offset="1" stop-color="#7b8cf0" stop-opacity="0"/></linearGradient>
        <linearGradient id="au2" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="#8f6fe0" stop-opacity="0"/>
          <stop offset=".55" stop-color="#59c8e8" stop-opacity=".95"/>
          <stop offset="1" stop-color="#59c8e8" stop-opacity="0"/></linearGradient>
        <linearGradient id="au3" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="#c86fe0" stop-opacity="0"/>
          <stop offset=".62" stop-color="#a678f0" stop-opacity=".8"/>
          <stop offset="1" stop-color="#4be0b0" stop-opacity="0"/></linearGradient>
        <radialGradient id="auHalo">
          <stop offset="0" stop-color="#4be0b0" stop-opacity=".55"/>
          <stop offset=".6" stop-color="#3f9ad8" stop-opacity=".22"/>
          <stop offset="1" stop-color="#3f9ad8" stop-opacity="0"/></radialGradient>
        <radialGradient id="halo">
          <stop offset="0" stop-color="${c.astroLuz}"/>
          <stop offset=".45" stop-color="${c.astroLuz}" stop-opacity=".45"/>
          <stop offset="1" stop-color="${c.astroLuz}" stop-opacity="0"/></radialGradient>
        <radialGradient id="cristal" cx=".35" cy=".3">
          <stop offset="0" stop-color="#fffdf0"/><stop offset="1" stop-color="#ffdf8e"/></radialGradient>
        <linearGradient id="rayo" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="${c.haz}"/>
          <stop offset=".55" stop-color="${c.haz}" stop-opacity=".35"/>
          <stop offset="1" stop-color="${c.haz}" stop-opacity="0"/></linearGradient>

        <!-- lo que esta al fondo va ligeramente desenfocado -->
        <filter id="lejos" x="-6%" y="-40%" width="112%" height="200%">
          <feGaussianBlur stdDeviation="1.2"/></filter>
        <filter id="suave" x="-30%" y="-90%" width="160%" height="320%">
          <feGaussianBlur stdDeviation="3.4"/></filter>
        <filter id="velo" x="-15%" y="-80%" width="130%" height="320%">
          <feTurbulence type="fractalNoise" baseFrequency=".009 .022" numOctaves="3" seed="7"/>
          <feDisplacementMap in="SourceGraphic" scale="34" xChannelSelector="R" yChannelSelector="G"/>
          <feGaussianBlur stdDeviation="6"/></filter>
        <filter id="glow" x="-200%" y="-200%" width="500%" height="500%">
          <feGaussianBlur stdDeviation="9" result="b"/>
          <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        <!-- el grano le quita el plastico al vector -->
        <filter id="grano" x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="3" seed="4"/>
          <feColorMatrix type="saturate" values="0"/></filter>
        <filter id="agua" x="-4%" y="-30%" width="108%" height="160%">
          <feTurbulence type="fractalNoise" baseFrequency=".012 .06" numOctaves="2" seed="11"/>
          <feDisplacementMap in="SourceGraphic" scale="7" xChannelSelector="R" yChannelSelector="G"/></filter>
        <!-- la boca del fiordo: donde el astro esta bajo, las montanas se
             abren y el mar sigue hasta el horizonte, que es por donde se
             pone el sol -->
        <radialGradient id="bocaG" cx=".5" cy=".5">
          <stop offset="0" stop-color="#000"/><stop offset=".55" stop-color="#000"/>
          <stop offset="1" stop-color="#fff"/></radialGradient>
        <mask id="boca">
          <rect width="1200" height="520" fill="#fff"/>
          ${c.astroY > 170 ? `<ellipse cx="${c.astroX}" cy="${HOR}" rx="250" ry="150" fill="url(#bocaG)"/>` : ''}
        </mask>
        <clipPath id="recorte"><rect x="0" y="0" width="1200" height="520" rx="20"/></clipPath>
        <clipPath id="soloMar"><rect x="0" y="${HOR}" width="1200" height="${ORILLA - HOR + 34}"/></clipPath>
      </defs>

      <g clip-path="url(#recorte)">
        <rect width="1200" height="520" fill="url(#cielo)"/>
        ${estrellas}${aurora}

        <!-- el astro, a la izquierda del faro y por debajo del titulo -->
        <circle cx="${c.astroX}" cy="${c.astroY}" r="${c.astroHalo}" fill="url(#halo)"/>
        <circle cx="${c.astroX}" cy="${c.astroY}" r="${c.astroR}" fill="${c.astro}" filter="url(#glow)"/>

        <!-- el fiordo: tres cordilleras, cuanto mas lejos mas palida -->
        <g mask="url(#boca)">
          <g filter="url(#lejos)" opacity=".88">
            ${sierra(HOR + 2, [[210, 96], [170, 132], [240, 74], [190, 112], [200, 60], [230, 92]],
                     c.monteLejos, c.nieve, 88)}
          </g>
          <g opacity=".95">
            ${sierra(HOR + 3, [[260, 62], [200, 96], [300, 44], [240, 78], [320, 56]],
                     c.monteMedio, c.nieve, 74)}
          </g>
          ${sierra(HOR + 4, [[380, 34], [300, 52], [360, 26], [340, 44]], c.monteCerca, null, 999)}
        </g>

        <!-- calima: funde la base de las montanas con el agua -->
        <rect x="0" y="${HOR - 48}" width="1200" height="54" fill="url(#calima)"/>

        <!-- nubes, con su sombra propia -->
        <g class="lh-nube" style="animation-duration:78s;animation-delay:-24s">
          ${nube(96, 1, c.aurora ? .2 : .92, c.nubeLuz, c.nubeSombra)}</g>
        <g class="lh-nube" style="animation-duration:104s;animation-delay:-62s">
          ${nube(178, .62, c.aurora ? .14 : .78, c.nubeLuz, c.nubeSombra)}</g>
        <g class="lh-nube" style="animation-duration:88s;animation-delay:-80s">
          ${nube(52, .82, c.aurora ? .16 : .85, c.nubeLuz, c.nubeSombra)}</g>

        <!-- el haz sale por detras de la torre: se dibuja antes que ella -->
        <g class="lh-luz" style="--fx:${FX}px;--fy:${FY}px" opacity=".9">
          <path d="M${FX} ${FY} L${FX + 900} ${FY - 190} L${FX + 900} ${FY + 190} Z"
                fill="url(#rayo)" filter="url(#suave)"/>
          <path d="M${FX} ${FY} L${FX + 900} ${FY - 60} L${FX + 900} ${FY + 60} Z" fill="url(#rayo)"/>
        </g>

        <!-- el mar -->
        <rect x="0" y="${HOR}" width="1200" height="${520 - HOR}" fill="url(#mar)"/>
        <g clip-path="url(#soloMar)">
          <rect x="0" y="${HOR}" width="1200" height="3" fill="#fff" opacity=".26"/>
          ${c.aurora ? `<!-- la aurora se refleja en el agua, del reves y desvaida -->
          <g transform="translate(0 ${HOR * 2 + 40}) scale(1 -1)" opacity=".45" filter="url(#velo)">
            <path d="M120 146 Q400 26 700 104 T1260 46 L1260 -30 L120 -30 Z" fill="url(#au1)"/>
            <path d="M60 198 Q420 74 780 156 T1260 100 L1260 12 L60 12 Z" fill="url(#au2)"/>
          </g>` : ''}
          <g class="lh-rielar">${rielar}</g>
          <!-- islote con sus arboles: le da fondo al agua -->
          <g opacity=".92">
            <path d="M96 ${HOR + 16} q26 -20 58 -18 q34 2 56 18 Z" fill="${c.monteCerca}"/>
            ${abeto(124, HOR + 2, 24, c.monteCerca, '#0b1d16')}
            ${abeto(142, HOR + 4, 17, c.monteCerca, '#0b1d16')}
          </g>
          ${velero(196, HOR + 62, .92, c.aurora ? '#c8d8ee' : '#fdfaf2', c.aurora ? '#33405c' : '#8a5f3c')}
          <g filter="url(#agua)">
            <g class="lh-ola" style="animation-duration:13s" opacity=".55">
              <path d="${espuma(HOR + 18, 5)}" fill="none" stroke="#fff" stroke-opacity=".26" stroke-width="3"/>
              <path d="${espuma(HOR + 32, 5)}" fill="none" stroke="#fff" stroke-opacity=".2" stroke-width="3"/></g>
            <g class="lh-ola" style="animation-duration:9s" opacity=".8">
              <path d="${espuma(HOR + 54, 7)}" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="4"/>
              <path d="${espuma(HOR + 74, 8)}" fill="none" stroke="#fff" stroke-opacity=".24" stroke-width="4"/></g>
            <g class="lh-ola" style="animation-duration:6.5s">
              <path d="${espuma(HOR + 92, 10)}" fill="none" stroke="#fff" stroke-opacity=".4" stroke-width="5"/></g>
          </g>
        </g>

        <!-- la playa, de lado a lado: los ninos se paran aqui -->
        <path d="M0 ${ORILLA + 24} Q300 ${ORILLA - 14} 640 ${ORILLA + 14}
                 T1200 ${ORILLA + 2} L1200 520 L0 520 Z" fill="url(#arena)"/>
        <g class="lh-ola" style="animation-duration:11s">
          <path d="${espuma(ORILLA + 14, 9)}" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="7"/>
          <path d="${espuma(ORILLA + 26, 7)}" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="4"/></g>

        <!-- el promontorio de la derecha y el faro plantado encima: la
             hierba cubre casi toda la loma y la roca asoma en el acantilado,
             que es lo que la separa de ser una mancha de color -->
        <path d="M708 520 Q790 ${ORILLA + 26} 878 ${BASE + 30} Q940 ${BASE - 14} 1012 ${BASE - 16}
                 Q1116 ${BASE - 6} 1200 ${ORILLA - 16} L1200 520 Z" fill="url(#hierba)"/>
        <!-- el acantilado, por debajo de la linea de hierba -->
        <path d="M708 520 Q790 ${ORILLA + 26} 878 ${BASE + 30} Q900 ${BASE + 20} 918 ${BASE + 26}
                 Q900 ${BASE + 74} 872 ${ORILLA + 66} Q800 ${ORILLA + 76} 748 520 Z" fill="url(#roca)"/>
        <path d="M1200 ${ORILLA - 16} Q1150 ${BASE + 34} 1104 ${ORILLA + 40} Q1150 ${ORILLA + 54} 1200 ${ORILLA + 34} Z"
              fill="url(#roca)" opacity=".9"/>
        <!-- estratos de la roca -->
        <g stroke="rgba(0,0,0,.18)" stroke-width="2.5" fill="none">
          <path d="M786 ${ORILLA + 44} q46 -10 80 -4"/><path d="M770 ${ORILLA + 68} q54 -12 92 -6"/>
          <path d="M1128 ${ORILLA + 30} q34 -8 62 -14"/></g>
        <!-- filo iluminado de la loma -->
        <path d="M878 ${BASE + 30} Q940 ${BASE - 14} 1012 ${BASE - 16} Q1116 ${BASE - 6} 1200 ${ORILLA - 16}"
              fill="none" stroke="rgba(255,255,255,.26)" stroke-width="3"/>
        <!-- la ladera que mira al sur queda en sombra -->
        <path d="M1012 ${BASE - 16} Q1116 ${BASE - 6} 1200 ${ORILLA - 16} L1200 520
                 L1040 520 Q1030 ${ORILLA + 40} 1012 ${BASE - 16} Z"
              fill="rgba(12,32,18,.16)"/>
        <!-- matas de hierba, para que la loma tenga relieve -->
        <g fill="${c.hierba[0]}" opacity=".55">
          <ellipse cx="930" cy="${BASE + 26}" rx="26" ry="12"/>
          <ellipse cx="1092" cy="${BASE + 16}" rx="30" ry="13"/>
          <ellipse cx="1170" cy="${ORILLA - 2}" rx="24" ry="11"/>
          <ellipse cx="820" cy="${ORILLA + 44}" rx="28" ry="12"/></g>
        <g stroke="${c.hierba[1]}" stroke-width="2.6" fill="none" stroke-linecap="round" opacity=".7">
          <path d="M900 ${BASE + 30} q-4 -16 4 -22"/><path d="M912 ${BASE + 28} q2 -14 10 -20"/>
          <path d="M1140 ${ORILLA + 4} q-4 -16 4 -22"/></g>
        <!-- la casa del farero, detras de la torre -->
        <g>
          <ellipse cx="1104" cy="${BASE + 30}" rx="44" ry="9" fill="rgba(14,26,14,.26)" filter="url(#suave)"/>
          <path d="M1072 ${BASE + 26} L1072 ${BASE - 8} L1136 ${BASE - 8} L1136 ${BASE + 26} Z" fill="#e8d9c2"/>
          <path d="M1064 ${BASE - 8} L1104 ${BASE - 34} L1144 ${BASE - 8} Z" fill="#b0503f"/>
          <rect x="1080" y="${BASE + 2} " width="12" height="14" rx="2" fill="#3f5f7c"/>
          <rect x="1112" y="${BASE + 6}" width="14" height="20" rx="2" fill="#6b4a33"/>
          <rect x="1124" y="${BASE - 30}" width="7" height="14" fill="#8b7f6e"/>
        </g>
        <!-- abetos: dos grupos, a un lado y al otro de la torre -->
        ${abeto(892, BASE + 34, 62, c.hierba[1], '#0d2a1c')}
        ${abeto(920, BASE + 30, 44, c.hierba[1], '#0d2a1c')}
        ${abeto(1170, ORILLA + 4, 54, c.hierba[1], '#0d2a1c')}
        ${abeto(1196, ORILLA + 16, 40, c.hierba[1], '#0d2a1c')}

        ${faro(c, FX, FY, BASE)}

        <!-- textura de la arena: motas y guijarros sueltos, que es lo que
             evita que el suelo sea una mancha lisa -->
        <g fill="${c.arenaMojada}" opacity=".5">
          <ellipse cx="180" cy="470" rx="34" ry="6"/><ellipse cx="470" cy="492" rx="42" ry="7"/>
          <ellipse cx="720" cy="474" rx="30" ry="6"/><ellipse cx="330" cy="508" rx="46" ry="7"/>
          <ellipse cx="612" cy="452" rx="26" ry="5"/></g>
        <g fill="${c.roca[1]}" opacity=".28">
          <ellipse cx="286" cy="504" rx="11" ry="4"/><ellipse cx="352" cy="514" rx="8" ry="3"/>
          <ellipse cx="146" cy="488" rx="9" ry="3.5"/><ellipse cx="676" cy="500" rx="10" ry="4"/></g>
        <!-- hierba de duna en los bordes: enmarca sin taparlos a ellos -->
        <g stroke="${c.hierba[1]}" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7">
          <path d="M40 520 q-6 -36 6 -52"/><path d="M56 520 q2 -32 18 -46"/>
          <path d="M24 520 q-12 -28 -6 -46"/>
          <path d="M1176 520 q6 -34 -6 -50"/><path d="M1158 520 q-2 -30 -16 -44"/></g>

        <!-- gaviotas a dos distancias -->
        <g class="lh-ave" fill="none" stroke="${c.ave}" stroke-width="3.4"
           stroke-linecap="round" opacity=".7">
          <path d="M232 122 q15 -13 30 0"/><path d="M262 122 q15 -13 30 0"/></g>
        <g class="lh-ave" style="animation-duration:12s;animation-delay:-3s" fill="none"
           stroke="${c.ave}" stroke-width="2.2" stroke-linecap="round" opacity=".45">
          <path d="M448 168 q10 -9 20 0"/><path d="M468 168 q10 -9 20 0"/>
          <path d="M392 196 q8 -7 16 0"/></g>

        <!-- gradeado de la hora y grano, encima de todo -->
        <rect width="1200" height="520" fill="${c.tinte}" style="mix-blend-mode:${c.tinteModo}"/>
        <rect width="1200" height="520" filter="url(#grano)" opacity=".05"
              style="mix-blend-mode:overlay"/>
      </g>
    </svg>`;
  }

  /* ---- la pantalla ----------------------------------------------------- */

  function html(idx, nivel) {
    const c = HORA[nivel] || HORA.starters;
    const anfitrion = ANFITRION[nivel] || (idx.kids || [])[0];
    const kids = idx.kids || [];

    // Los ninos no van en fila plana: los del centro pisan mas adelante
    // (mas grandes y mas abajo) y los de los extremos quedan detras, algo
    // mas pequenos y apagados por la distancia.
    const plano = i => {
      const centro = (kids.length - 1) / 2;
      const d = Math.abs(i - centro) / (centro || 1);          // 0 centro, 1 extremo
      return `--esc:${(1.05 - d * .14).toFixed(3)};--fondo:${(d * 10).toFixed(1)}px;` +
             `--sat:${(1 - d * .12).toFixed(2)};--bri:${(1 - d * .07).toFixed(2)}`;
    };

    const ninos = kids.map((k, i) => `
      <button class="lh-nino${k === anfitrion ? ' saluda' : ''}" data-quien="${k}"
              type="button" style="${plano(i)}"
              aria-label="Listen to ${k[0].toUpperCase() + k.slice(1)}">
        <span class="lh-globo">${k === anfitrion ? 'Hello!!' : 'Hi!'}</span>
        <img src="../assets/characters/${nivel}/${k}/fullbody.png?v=${window.ART_V || ''}" alt=""
             onerror="this.onerror=null;this.src='../assets/characters/${nivel}/${k}/pose-01.png?v=${window.ART_V || ''}'">
      </button>`).join('');

    return `<style>${CSS}</style>
      <div class="lh" data-nivel="${nivel}">
        ${fondo(nivel)}
        ${CON_LAMINA.has(nivel) ? `<img class="lh-lamina" src="${LAMINA(nivel)}" alt=""
             onerror="this.remove()">` : ''}
        <div class="lh-capa" style="color:${c.texto}">
          <div class="lh-tit" style="text-shadow:${c.sombraTexto}">
            <h1>${idx.name}</h1>
            <p class="lh-cast">${idx.cast}</p>
          </div>
          <div class="lh-elenco">
            ${ninos}
            <button class="lh-nino mascota" data-quien="${idx.mascot}" type="button"
                    style="--esc:1;--fondo:6px"
                    aria-label="${idx.mascot[0].toUpperCase() + idx.mascot.slice(1)}">
              <span class="lh-globo">Hello!</span>
              <img src="../assets/characters/${nivel}/${idx.mascot}/fullbody.png?v=${window.ART_V || ''}" alt=""
                   onerror="this.onerror=null;this.src='../assets/characters/${nivel}/${idx.mascot}/pose-01.png?v=${window.ART_V || ''}'">
            </button>
          </div>
        </div>
      </div>`;
  }

  /* Cada nino se presenta con su voz al pulsarlo. */
  function vivo(el) {
    const caja = el.querySelector('.lh');
    if (!caja) return;
    const nivel = caja.dataset.nivel;
    let sonando = null;
    caja.querySelectorAll('.lh-nino').forEach(b => {
      b.onclick = () => {
        const quien = b.dataset.quien;
        b.classList.remove('dice');
        void b.offsetWidth;                       // reinicia la animacion
        b.classList.add('dice');
        if (sonando) { sonando.pause(); sonando = null; }
        const nombre = quien[0].toUpperCase() + quien.slice(1);
        const a = new Audio(`../audio/cast/${nivel}-${quien}.mp3`);
        const deRespaldo = () => {
          if (window.SAY) SAY.frase(`Hello! I am ${nombre}!`);
        };
        a.onerror = deRespaldo;
        a.play().catch(deRespaldo);
        sonando = a;
      };
    });
  }

  return { html, vivo };
})();
