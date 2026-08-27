/* Portada animada de cada nivel — Fun for Nordic.
 *
 * La portada era una foto quieta con el titulo al lado y media pantalla en
 * blanco. Ahora es el faro de la serie: el mar se mueve, la luz gira, pasan
 * nubes y gaviotas, y el equipo del nivel esta abajo saludando. Al pulsar a
 * un nino se presenta con su voz.
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
 * Uso:  BANNER.html(idx, LEVEL)  ->  el HTML de la pantalla
 *       BANNER.vivo(el)          ->  engancha los saludos
 */
window.BANNER = (function () {

  const HORA = {
    starters: {
      cielo: ['#bfe6f7', '#e8f6fb'], mar: ['#3f9dc4', '#2b6f96'],
      astro: '#ffd76a', astroLuz: 'rgba(255,225,140,.55)', tierra: '#5f9e57',
      arena: ['#f2e3c0', '#e3cfa4'],
      haz: 'rgba(255,238,170,.55)', texto: '#1d3a52', aurora: false, estrellas: 0,
    },
    movers: {
      cielo: ['#f6c98b', '#fbe7cd'], mar: ['#2f6f9e', '#1d4a70'],
      astro: '#ff9d5c', astroLuz: 'rgba(255,150,90,.5)', tierra: '#4e7f52',
      arena: ['#e8cfa6', '#cfae7f'],
      haz: 'rgba(255,214,140,.6)', texto: '#4a2a17', aurora: false, estrellas: 0,
    },
    flyers: {
      cielo: ['#1b2a52', '#31456f'], mar: ['#16304d', '#0d1f33'],
      astro: '#eef3ff', astroLuz: 'rgba(220,235,255,.35)', tierra: '#27503f',
      arena: ['#42506b', '#2c3950'],
      haz: 'rgba(190,230,255,.6)', texto: '#eaf1ff', aurora: true, estrellas: 46,
    },
  };

  // Quien lleva la voz cantante en la portada de cada nivel.
  const ANFITRION = { starters: 'freya', movers: 'valentina', flyers: 'ingrid' };

  const CSS = `
  .lh{position:relative;width:100%;max-width:64rem;margin:0 auto;border-radius:20px;
    overflow:hidden;box-shadow:0 10px 34px rgba(20,40,70,.18);isolation:isolate}
  .lh svg{display:block;width:100%;height:auto}
  .lh-capa{position:absolute;inset:0;display:flex;flex-direction:column;
    justify-content:space-between;padding:4% 5% 0;pointer-events:none}
  .lh-tit{text-align:left;pointer-events:none}
  .lh-tit h1{margin:0;font-family:"Baloo 2",sans-serif;font-size:clamp(1rem,2.6vw,1.9rem);
    line-height:1.15;text-shadow:0 2px 10px rgba(255,255,255,.45)}
  .lh-cast{margin:.25rem 0 0;font-family:"Baloo 2",sans-serif;font-weight:800;
    font-size:clamp(.8rem,2.1vw,1.45rem);letter-spacing:.08em;text-transform:uppercase}
  .lh-elenco{display:flex;align-items:flex-end;justify-content:center;gap:1%;
    pointer-events:auto;padding-bottom:2.5%}
  .lh-nino{background:none;border:0;padding:0;cursor:pointer;position:relative;
    flex:0 1 auto;line-height:0;transition:transform .18s}
  .lh-nino img{height:clamp(86px,19vw,196px);width:auto;display:block;
    filter:drop-shadow(0 6px 10px rgba(15,30,50,.34))}
  .lh-nino:hover{transform:translateY(-6px)}
  .lh-nino.mascota img{height:clamp(60px,13vw,132px)}

  /* el bocadillo: el del anfitrion aparece solo, los demas al pulsar */
  .lh-globo{position:absolute;left:50%;bottom:calc(100% - 6px);transform:translateX(-50%) scale(.6);
    background:#fff;color:#1d3a52;border-radius:14px;padding:.3rem .7rem;white-space:nowrap;
    font-family:"Baloo 2",sans-serif;font-weight:800;font-size:clamp(.7rem,1.7vw,1.05rem);
    box-shadow:0 4px 12px rgba(20,40,70,.28);opacity:0;pointer-events:none}
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

  /* el mar: dos copias del mismo dibujo, la segunda entra cuando sale la
     primera, asi el vaiven no tiene principio ni final visible */
  .lh-ola{animation:lhola linear infinite}
  @keyframes lhola{from{transform:translateX(0)}to{transform:translateX(-400px)}}
  .lh-luz{transform-origin:var(--fx) var(--fy);animation:lhgira 7s linear infinite}
  @keyframes lhgira{from{transform:rotate(0)}to{transform:rotate(360deg)}}
  .lh-foco{animation:lhbrilla 7s ease-in-out infinite}
  @keyframes lhbrilla{0%,100%{opacity:.55}22%{opacity:1}44%{opacity:.6}}
  .lh-nube{animation:lhnube linear infinite}
  @keyframes lhnube{from{transform:translateX(1260px)}to{transform:translateX(-320px)}}
  .lh-ave{animation:lhave 9s ease-in-out infinite}
  @keyframes lhave{0%,100%{transform:translate(0,0)}50%{transform:translate(26px,-12px)}}
  .lh-aurora{animation:lhaurora 9s ease-in-out infinite}
  @keyframes lhaurora{0%,100%{opacity:.28;transform:translateY(0)}50%{opacity:.6;transform:translateY(-10px)}}
  .lh-titila{animation:lhtitila ease-in-out infinite}
  @keyframes lhtitila{0%,100%{opacity:.25}50%{opacity:1}}

  @media (max-width:640px){
    .lh-capa{padding:3% 4% 0}
    .lh-elenco{gap:0}
  }
  @media (prefers-reduced-motion:reduce){
    .lh-ola,.lh-luz,.lh-foco,.lh-nube,.lh-ave,.lh-aurora,.lh-titila,
    .lh-nino.saluda .lh-globo{animation:none}
    .lh-nino.saluda .lh-globo{opacity:1;transform:translateX(-50%) scale(1)}
  }`;

  // Espuma de 400 de ancho que encaja consigo misma al repetirse, para que
  // el vaiven no tenga principio ni final visible.
  function espuma(y, alto) {
    let d = `M0 ${y}`;
    for (let x = 0; x < 1700; x += 200)
      d += ` q50 ${-alto} 100 0 t100 0`;
    return d;
  }

  function nube(x, y, e) {
    return `<g transform="translate(${x} ${y}) scale(${e})" fill="#fff" opacity=".8">
      <ellipse cx="0" cy="0" rx="38" ry="22"/><ellipse cx="34" cy="7" rx="30" ry="17"/>
      <ellipse cx="-32" cy="8" rx="26" ry="15"/></g>`;
  }

  function fondo(nivel) {
    const c = HORA[nivel] || HORA.starters;
    const FX = 1004, FY = 172;          // el foco del faro, arriba del todo
    const MAR = 262, ARENA = 366;       // donde empieza el agua y donde la playa

    const estrellas = c.estrellas ? Array.from({ length: c.estrellas }, (_, i) => {
      const x = (i * 137) % 1180 + 10, y = (i * 71) % 190 + 8, r = i % 3 === 0 ? 1.8 : 1.2;
      return `<circle class="lh-titila" cx="${x}" cy="${y}" r="${r}" fill="#fff"
        style="animation-duration:${2 + (i % 5) * .7}s;animation-delay:${(i % 7) * .4}s"/>`;
    }).join('') : '';

    const aurora = c.aurora ? `
      <g class="lh-aurora">
        <path d="M0 118 Q300 30 620 92 T1200 52 L1200 6 L0 6 Z" fill="url(#au1)"/>
        <path d="M0 154 Q340 74 700 128 T1200 96 L1200 34 L0 34 Z" fill="url(#au2)"/>
      </g>` : '';

    return `
    <svg viewBox="0 0 1200 520" role="img"
         aria-label="A lighthouse on the rocks by the sea, with the Nordic characters waving.">
      <defs>
        <linearGradient id="cielo" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="${c.cielo[0]}"/><stop offset="1" stop-color="${c.cielo[1]}"/>
        </linearGradient>
        <linearGradient id="mar" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="${c.mar[0]}"/><stop offset="1" stop-color="${c.mar[1]}"/>
        </linearGradient>
        <linearGradient id="au1" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="#4be0b0" stop-opacity="0"/>
          <stop offset=".45" stop-color="#4be0b0" stop-opacity=".8"/>
          <stop offset="1" stop-color="#7b8cf0" stop-opacity="0"/></linearGradient>
        <linearGradient id="au2" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="#8f6fe0" stop-opacity="0"/>
          <stop offset=".55" stop-color="#59c8e8" stop-opacity=".7"/>
          <stop offset="1" stop-color="#59c8e8" stop-opacity="0"/></linearGradient>
        <radialGradient id="halo"><stop offset="0" stop-color="${c.astroLuz}"/>
          <stop offset="1" stop-color="${c.astroLuz}" stop-opacity="0"/></radialGradient>
        <linearGradient id="rayo" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="${c.haz}"/>
          <stop offset="1" stop-color="${c.haz}" stop-opacity="0"/></linearGradient>
        <linearGradient id="arena" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="${c.arena[0]}"/><stop offset="1" stop-color="${c.arena[1]}"/>
        </linearGradient>
        <clipPath id="recorte"><rect x="0" y="0" width="1200" height="520" rx="20"/></clipPath>
      </defs>

      <g clip-path="url(#recorte)">
        <rect width="1200" height="520" fill="url(#cielo)"/>
        ${estrellas}${aurora}

        <!-- el sol, lejos del titulo, que va arriba a la izquierda -->
        <circle cx="632" cy="96" r="96" fill="url(#halo)"/>
        <circle cx="632" cy="96" r="38" fill="${c.astro}"/>

        <g class="lh-nube" style="animation-duration:70s;animation-delay:-20s">${nube(0, 88, 1)}</g>
        <g class="lh-nube" style="animation-duration:96s;animation-delay:-56s">${nube(0, 168, .66)}</g>
        <g class="lh-nube" style="animation-duration:82s;animation-delay:-74s">${nube(0, 52, .82)}</g>

        <!-- el haz sale por detras de la torre: se dibuja antes que ella -->
        <g class="lh-luz" style="--fx:${FX}px;--fy:${FY}px">
          <path d="M${FX} ${FY} L${FX + 820} ${FY - 140} L${FX + 820} ${FY + 140} Z" fill="url(#rayo)"/>
        </g>

        <!-- el mar, con la linea del horizonte recta -->
        <rect x="0" y="${MAR}" width="1200" height="${520 - MAR}" fill="url(#mar)"/>
        <g class="lh-ola" style="animation-duration:11s">
          <path d="${espuma(MAR + 22, 7)}" fill="none" stroke="#fff" stroke-opacity=".30" stroke-width="4"/>
          <path d="${espuma(MAR + 44, 6)}" fill="none" stroke="#fff" stroke-opacity=".20" stroke-width="3"/></g>
        <g class="lh-ola" style="animation-duration:7s">
          <path d="${espuma(MAR + 66, 9)}" fill="none" stroke="#fff" stroke-opacity=".34" stroke-width="5"/>
          <path d="${espuma(MAR + 88, 8)}" fill="none" stroke="#fff" stroke-opacity=".24" stroke-width="4"/></g>

        <!-- la playa, de lado a lado: los ninos se paran aqui -->
        <path d="M0 ${ARENA + 26} Q300 ${ARENA - 12} 640 ${ARENA + 16}
                 T1200 ${ARENA + 4} L1200 520 L0 520 Z" fill="url(#arena)"/>
        <g class="lh-ola" style="animation-duration:9s">
          <path d="${espuma(ARENA + 20, 8)}" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="6"/></g>

        <!-- el promontorio de la derecha y el faro plantado encima -->
        <path d="M742 520 Q812 ${ARENA + 34} 890 ${ARENA - 54} Q952 ${ARENA - 104} 1010 ${ARENA - 108}
                 Q1108 ${ARENA - 96} 1200 ${ARENA - 4} L1200 520 Z" fill="${c.tierra}"/>
        <path d="M742 520 Q812 ${ARENA + 34} 890 ${ARENA - 54} Q952 ${ARENA - 104} 1010 ${ARENA - 108}
                 Q1108 ${ARENA - 96} 1200 ${ARENA - 4}" fill="none"
              stroke="rgba(0,0,0,.13)" stroke-width="4"/>
        <g>
          <path d="M958 ${ARENA - 30} L1050 ${ARENA - 30} L1032 210 L976 210 Z" fill="#f7f4ee"/>
          <path d="M966 ${ARENA - 112} L1042 ${ARENA - 112} L1038 ${ARENA - 158} L970 ${ARENA - 158} Z" fill="#e05c4b"/>
          <path d="M974 262 L1034 262 L1031 226 L977 226 Z" fill="#e05c4b"/>
          <rect x="962" y="196" width="84" height="14" rx="5" fill="#33506b"/>
          <rect x="972" y="${FY - 34}" width="64" height="64" rx="6" fill="#33506b"/>
          <rect x="979" y="${FY - 27}" width="50" height="52" rx="4" fill="#ffe9a8"/>
          <circle class="lh-foco" cx="${FX}" cy="${FY}" r="17" fill="#fff8dc"/>
          <path d="M964 132 L1004 100 L1044 132 Z" fill="#33506b"/>
          <rect x="1001" y="82" width="6" height="20" fill="#33506b"/>
          <circle cx="1004" cy="80" r="5.5" fill="#e05c4b"/>
        </g>

        <g class="lh-ave" fill="none" stroke="${c.aurora ? '#cfe0ff' : '#41566b'}" stroke-width="3.4"
           stroke-linecap="round" opacity=".7">
          <path d="M262 116 q14 -12 28 0"/><path d="M290 116 q14 -12 28 0"/>
          <path d="M340 158 q12 -10 24 0"/>
        </g>
      </g>
    </svg>`;
  }

  function html(idx, nivel) {
    const c = HORA[nivel] || HORA.starters;
    const anfitrion = ANFITRION[nivel] || (idx.kids || [])[0];
    const ninos = (idx.kids || []).map(k => `
      <button class="lh-nino${k === anfitrion ? ' saluda' : ''}" data-quien="${k}"
              type="button" aria-label="Listen to ${k[0].toUpperCase() + k.slice(1)}">
        <span class="lh-globo">${k === anfitrion ? 'Hello!!' : 'Hi!'}</span>
        <img src="../assets/characters/${nivel}/${k}/fullbody.png" alt=""
             onerror="this.onerror=null;this.src='../assets/characters/${nivel}/${k}/pose-01.png'">
      </button>`).join('');

    return `<style>${CSS}</style>
      <div class="lh" data-nivel="${nivel}">
        ${fondo(nivel)}
        <div class="lh-capa" style="color:${c.texto}">
          <div class="lh-tit">
            <h1>${idx.name}</h1>
            <p class="lh-cast">${idx.cast}</p>
          </div>
          <div class="lh-elenco">
            ${ninos}
            <button class="lh-nino mascota" data-quien="${idx.mascot}" type="button"
                    aria-label="${idx.mascot[0].toUpperCase() + idx.mascot.slice(1)}">
              <span class="lh-globo">Hello!</span>
              <img src="../assets/characters/${nivel}/${idx.mascot}/fullbody.png" alt=""
                   onerror="this.onerror=null;this.src='../assets/characters/${nivel}/${idx.mascot}/pose-01.png'">
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
