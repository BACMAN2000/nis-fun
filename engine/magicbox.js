/* The Magic Box — la explicación sin explicación, Fun for Nordic.
 *
 * Antes de la actividad de examen el alumno se encontraba con "Choose the
 * correct word" sin que nadie le hubiera enseñado la regla. Y ponerle un
 * titulo de gramatica a un nino de siete anos no sirve de nada: no sabe
 * que es un comparativo, y saberlo tampoco le ayuda a decirlo.
 *
 * Aqui la mascota abre su caja magica y la regla se VE: tres cajas de
 * tamanos distintos y la palabra que va creciendo con ella, con la
 * terminacion que se le anade encendida. El alumno pulsa y la caja cambia.
 * No aparece la palabra "comparativo" en ninguna parte.
 *
 * Cada unidad cae en una familia segun lo que practica; hay 148 patrones
 * distintos en la serie y una ilustracion por familia los cubre casi
 * todos. Lo que no encaja no ensena una caja vacia: no sale.
 *
 * Uso:  MAGICBOX.para(ud)   -> {titulo, html, alMostrar} o null
 */
window.MAGICBOX = (function () {

  const CSS = `
  .mb{max-width:46rem;margin-inline:auto;width:100%}
  .mb-tira{display:flex;justify-content:center;align-items:flex-end;gap:1.4rem;
    flex-wrap:wrap;margin:.4rem 0 1rem}
  .mb-paso{background:var(--surface2);border:2px solid transparent;border-radius:18px;
    padding:1rem .9rem .8rem;cursor:pointer;text-align:center;min-width:8.5rem;
    transition:transform .18s,border-color .18s}
  .mb-paso:hover{transform:translateY(-4px)}
  .mb-paso.on{border-color:var(--accent);background:#fff}
  .mb-paso svg{display:block;margin:0 auto .5rem}
  .mb-pal{font-family:"Baloo 2",sans-serif;font-weight:800;font-size:1.35rem;
    color:var(--ink);line-height:1.1}
  .mb-fin{color:var(--accent);background:#fff2c9;border-radius:6px;padding:0 .15rem}
  .mb-frase{margin:.35rem 0 0;font-size:.92rem;color:var(--soft);min-height:1.2rem}
  .mb-pie{text-align:center;color:var(--soft);margin:.2rem 0 0}
  .mb-reto{margin-top:1rem;background:var(--surface2);border-radius:16px;padding:.9rem 1rem;
    text-align:center}
  .mb-reto p{margin:0 0 .6rem;font-weight:600}
  .mb-ops{display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap}
  .mb-op{background:#fff;border:1.5px solid var(--line);border-radius:999px;
    padding:.4rem 1rem;cursor:pointer;font-family:"Baloo 2",sans-serif;font-weight:700;
    color:var(--ink)}
  .mb-op.bien{background:var(--ok);color:#fff;border-color:var(--ok)}
  .mb-op.mal{background:var(--bad);color:#fff;border-color:var(--bad)}
  .mb-eco{margin:.55rem 0 0;font-weight:700;color:var(--ok);min-height:1.3rem}
  @media (max-width:560px){ .mb-paso{min-width:7rem} }`;

  /* ---------- dibujos ---------- */
  function caja(alto, color) {
    // una caja de carton de tres cuartos; el alto la hace mas o menos grande
    const w = Math.round(alto * 1.25), h = alto;
    return `<svg width="${w}" height="${h + 14}" viewBox="0 0 ${w} ${h + 14}" aria-hidden="true">
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
    let s = `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" aria-hidden="true">`;
    for (let i = 0; i < n; i++) {
      const x = 26 + i * 34, y = 44;
      s += `<ellipse cx="${x}" cy="${y + 20}" rx="14" ry="4" fill="rgba(20,30,45,.14)"/>
            <circle cx="${x}" cy="${y}" r="15" fill="#e05c4b" stroke="#b7453a" stroke-width="1.6"/>
            <path d="M${x - 15} ${y} a15 15 0 0 0 30 0" fill="#f4f1ec" opacity=".55"/>`;
    }
    return s + '</svg>';
  }

  function figura(cara, brazo) {
    // un monigote simple: sirve para "puede/no puede" y para "ahora/antes"
    const w = 96, h = 108;
    return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" aria-hidden="true">
      <ellipse cx="48" cy="102" rx="24" ry="5" fill="rgba(20,30,45,.14)"/>
      <circle cx="48" cy="26" r="19" fill="#f6d7b8" stroke="#d9ab86" stroke-width="1.6"/>
      <circle cx="41" cy="24" r="2.6" fill="#2a2320"/><circle cx="55" cy="24" r="2.6" fill="#2a2320"/>
      <path d="${cara === 'triste' ? 'M41 34 q7 -5 14 0' : 'M41 32 q7 6 14 0'}"
            stroke="#2a2320" stroke-width="2" fill="none" stroke-linecap="round"/>
      <rect x="34" y="46" width="28" height="34" rx="9" fill="#7fb6e0"/>
      <path d="${brazo === 'arriba' ? 'M34 52 L18 34' : 'M34 54 L20 68'}"
            stroke="#f6d7b8" stroke-width="7" stroke-linecap="round"/>
      <path d="M62 54 L76 68" stroke="#f6d7b8" stroke-width="7" stroke-linecap="round"/>
      <path d="M40 80 L38 98 M56 80 L58 98" stroke="#3e5f8a" stroke-width="7" stroke-linecap="round"/>
    </svg>`;
  }

  function cajaCon(donde) {
    // una pelota dentro, encima o debajo de una caja
    const pos = { in: [64, 62], on: [64, 26], under: [64, 88] }[donde] || [64, 62];
    return `<svg width="128" height="108" viewBox="0 0 128 108" aria-hidden="true">
      <ellipse cx="64" cy="100" rx="34" ry="5" fill="rgba(20,30,45,.14)"/>
      ${donde === 'under' ? '' : ''}
      <path d="M30 44 L98 44 L98 92 L30 92 Z" fill="${donde === 'in' ? 'none' : '#e8c49a'}"
            stroke="#a9743f" stroke-width="2"/>
      ${donde === 'in' ? '<path d="M30 44 L98 44 L98 92 L30 92 Z" fill="#e8c49a" opacity=".45" stroke="#a9743f" stroke-width="2"/>' : ''}
      <circle cx="${pos[0]}" cy="${pos[1]}" r="14" fill="#e05c4b" stroke="#b7453a" stroke-width="1.6"/>
    </svg>`;
  }

  function reloj(hora) {
    return `<svg width="96" height="96" viewBox="0 0 96 96" aria-hidden="true">
      <circle cx="48" cy="48" r="38" fill="#f7f4ee" stroke="#33506b" stroke-width="4"/>
      <circle cx="48" cy="48" r="3" fill="#33506b"/>
      <path d="M48 48 L48 26" stroke="#33506b" stroke-width="4" stroke-linecap="round"
            transform="rotate(${(hora % 12) * 30} 48 48)"/>
      <path d="M48 48 L68 48" stroke="#e05c4b" stroke-width="3" stroke-linecap="round"/>
    </svg>`;
  }

  /* ---------- las familias ----------
     Cada una: como se reconoce, que se ve y que se aprende. El texto no
     nombra ninguna categoria gramatical: solo ensena. */
  const FAMILIAS = [
    {
      id: 'grande',
      busca: /compar|superlat|-er|bigger|biggest|tall|short|big|small|long|old|adjective\s*\+\s*er/i,
      titulo: 'Three boxes, three words',
      pasos: [
        { arte: () => caja(64, '#e8c49a'),  pal: 'big',      fin: '',    frase: 'This box is big.' },
        { arte: () => caja(92, '#e0b784'),  pal: 'bigg',     fin: 'er',  frase: 'This box is bigger!' },
        { arte: () => caja(124, '#d8a96c'), pal: 'bigg',     fin: 'est', frase: 'This box is the biggest!' },
      ],
      pie: 'One more box, one more ending.',
      reto: { p: 'This box is the ___ of all three.',
              ops: ['tall', 'taller', 'tallest'], bien: 2 },
    },
    {
      id: 'puedo',
      busca: /\bcan\b|can't|cannot|ability/i,
      titulo: 'What can you do?',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'I can',    fin: ' swim', frase: 'Yes! I can do it.' },
        { arte: () => figura('triste', 'abajo'), pal: "I can't",  fin: ' fly',  frase: 'No, I cannot.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'Can you',  fin: ' sing?', frase: 'Ask a friend!' },
      ],
      pie: 'One little word for everything you can do.',
      reto: { p: 'A fish in the sea…', ops: ['can swim', "can't swim", 'can fly'], bien: 0 },
    },
    {
      id: 'muchos',
      busca: /plural|countable|uncountable|there is|there are|there was|there were|how many/i,
      titulo: 'One, or a lot?',
      pasos: [
        { arte: () => bolas(1), pal: 'one ball',    fin: '',  frase: 'There is one ball.' },
        { arte: () => bolas(2), pal: 'two ball',    fin: 's', frase: 'There are two balls.' },
        { arte: () => bolas(3), pal: 'three ball',  fin: 's', frase: 'There are three balls!' },
      ],
      pie: 'More than one? Add the little s.',
      reto: { p: 'I can see four…', ops: ['cat', 'cats', 'catses'], bien: 1 },
    },
    {
      id: 'donde',
      busca: /preposition|in \/ on|on \/ under|place|where is|behind|between|under/i,
      titulo: 'Where is the ball?',
      pasos: [
        { arte: () => cajaCon('in'),    pal: 'in',    fin: '',  frase: 'The ball is in the box.' },
        { arte: () => cajaCon('on'),    pal: 'on',    fin: '',  frase: 'The ball is on the box.' },
        { arte: () => cajaCon('under'), pal: 'under', fin: '',  frase: 'The ball is under the box.' },
      ],
      pie: 'The box does not move — the ball does.',
      reto: { p: 'The cat is sleeping ___ the bed.', ops: ['in', 'on', 'under'], bien: 1 },
    },
    {
      id: 'ahora',
      busca: /continuous|-ing|present continuous|right now|doing/i,
      titulo: 'Right now!',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'I run',       fin: '',     frase: 'Every day.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'I am runn',   fin: 'ing',  frase: 'Right now!' },
        { arte: () => figura('feliz', 'arriba'), pal: 'She is runn', fin: 'ing',  frase: 'Look at her!' },
      ],
      pie: 'Happening now? Add -ing.',
      reto: { p: 'Look! Pip ___ .', ops: ['fly', 'is flying', 'flies'], bien: 1 },
    },
    {
      id: 'tengo',
      busca: /have got|has got|possession|whose|possessive|mine|yours/i,
      titulo: 'Whose is it?',
      pasos: [
        { arte: () => caja(76, '#e8c49a'), pal: 'I have got',   fin: ' a box', frase: 'It is mine.' },
        { arte: () => caja(76, '#d8b0d0'), pal: 'She has got',  fin: ' a box', frase: 'It is her box.' },
        { arte: () => caja(76, '#a8d0e8'), pal: 'They have got', fin: ' boxes', frase: 'They are theirs.' },
      ],
      pie: 'One person, or more than one?',
      reto: { p: 'Nico ___ a red kite.', ops: ['have got', 'has got', 'got'], bien: 1 },
    },
    {
      id: 'ayer',
      busca: /past simple|past continuous|was \/ were|went|yesterday|last week|irregular/i,
      titulo: 'Today and yesterday',
      pasos: [
        { arte: () => reloj(9),  pal: 'I play',   fin: '',    frase: 'Today.' },
        { arte: () => reloj(5),  pal: 'I play',   fin: 'ed',  frase: 'Yesterday.' },
        { arte: () => reloj(3),  pal: 'I went',   fin: '',    frase: 'Some words change completely!' },
      ],
      pie: 'Yesterday words look different.',
      reto: { p: 'Yesterday we ___ to the zoo.', ops: ['go', 'goed', 'went'], bien: 2 },
    },
    {
      id: 'manana',
      busca: /will|won't|going to|future|tomorrow/i,
      titulo: 'Tomorrow!',
      pasos: [
        { arte: () => reloj(9),  pal: 'I am',      fin: ' here', frase: 'Now.' },
        { arte: () => reloj(12), pal: 'I will',    fin: ' go',   frase: 'Tomorrow.' },
        { arte: () => reloj(2),  pal: "I won't",   fin: ' go',   frase: 'Not tomorrow!' },
      ],
      pie: 'Has not happened yet? Use will.',
      reto: { p: 'Tomorrow it ___ rain.', ops: ['will', 'was', 'is'], bien: 0 },
    },
    {
      id: 'este',
      busca: /this \/ that|these \/ those|this|that|these|those|demonstrat/i,
      titulo: 'Near me, far from me',
      pasos: [
        { arte: () => bolas(1), pal: 'this',  fin: ' ball',  frase: 'Here, next to me.' },
        { arte: () => bolas(1), pal: 'that',  fin: ' ball',  frase: 'Over there!' },
        { arte: () => bolas(3), pal: 'these', fin: ' balls', frase: 'Here, and more than one.' },
      ],
      pie: 'Near or far? One or many?',
      reto: { p: '___ boxes here are mine.', ops: ['This', 'These', 'That'], bien: 1 },
    },
    {
      id: 'el-hace',
      busca: /third person|3rd person|present simple|likes \/ doesn|does \/ doesn|daily routine/i,
      titulo: 'He, she… and a little s',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'I play',   fin: '',  frase: 'I play every day.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'He play',  fin: 's', frase: 'He plays every day.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'She play', fin: 's', frase: 'She plays every day.' },
      ],
      pie: 'He, she or it? The verb gets an s.',
      reto: { p: 'Pip ___ in the sea every morning.', ops: ['swim', 'swims', 'swimming'], bien: 1 },
    },
    {
      id: 'la-hora',
      busca: /o'clock|quarter past|half past|quarter to|what time|telling the time|clock/i,
      titulo: 'What time is it?',
      pasos: [
        { arte: () => reloj(3),  pal: "three o'clock", fin: '',   frase: 'The big hand points up.' },
        { arte: () => reloj(3),  pal: 'half past',     fin: ' three', frase: 'The big hand points down.' },
        { arte: () => reloj(4),  pal: 'quarter to',    fin: ' four',  frase: 'Almost four!' },
      ],
      pie: 'Look at the big hand first.',
      reto: { p: 'The big hand points down. It is…', ops: ["four o'clock", 'half past four', 'quarter to four'], bien: 1 },
    },
    {
      id: 'cuando',
      busca: /in \+ month|on \+ date|on \+ day|at \+ time|prepositions of time|month|season|birthday|date|in the morning|at night|day parts/i,
      titulo: 'in, on, at — when?',
      pasos: [
        { arte: () => reloj(12), pal: 'in',  fin: ' July',    frase: 'A whole month.' },
        { arte: () => reloj(9),  pal: 'on',  fin: ' Monday',  frase: 'One day.' },
        { arte: () => reloj(7),  pal: 'at',  fin: ' 7 o\'clock', frase: 'One moment.' },
      ],
      pie: 'Big time, small time, tiny time.',
      reto: { p: 'My birthday is ___ May.', ops: ['in', 'on', 'at'], bien: 0 },
    },
    {
      id: 'ya',
      busca: /present perfect|just \/ already|already|yet|ever \/ never|have you ever/i,
      titulo: 'Already done!',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'I am eating',   fin: '',        frase: 'Now.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'I have just',   fin: ' eaten',  frase: 'A moment ago!' },
        { arte: () => figura('triste', 'abajo'), pal: "I haven't",     fin: ' eaten yet', frase: 'Not yet…' },
      ],
      pie: 'Finished? Then use have.',
      reto: { p: 'Kili ___ already brought the letters.', ops: ['has', 'have', 'is'], bien: 0 },
    },
    {
      id: 'mejor',
      busca: /should|shouldn't|must|have to|advice|rules/i,
      titulo: 'A good idea, a bad idea',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'You should',    fin: ' sleep', frase: 'Good idea!' },
        { arte: () => figura('triste', 'abajo'), pal: "You shouldn't", fin: ' shout', frase: 'Not a good idea.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'Should I',      fin: ' help?', frase: 'Ask for advice.' },
      ],
      pie: 'Good idea, or better not?',
      reto: { p: 'You are tired. You ___ go to bed.', ops: ['should', "shouldn't", 'can\'t'], bien: 0 },
    },
    {
      id: 'como-voy',
      busca: /transport|by \+ vehicle|how do you get|travel by|bus|train|bike/i,
      titulo: 'How do you get there?',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'by',   fin: ' bus',  frase: 'I go by bus.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'by',   fin: ' bike', frase: 'I go by bike.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'on',   fin: ' foot', frase: 'This one is different!' },
      ],
      pie: 'Always by… except on foot.',
      reto: { p: 'I walk to school. I go ___ .', ops: ['by foot', 'on foot', 'by walk'], bien: 1 },
    },
    {
      id: 'que-verbo',
      busca: /play \/ go \/ do|play \+ sport|go \+ -ing|sports?/i,
      titulo: 'play, go or do?',
      pasos: [
        { arte: () => bolas(1), pal: 'play',  fin: ' football', frase: 'Games with a ball.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'go',   fin: ' swimming', frase: 'Words ending in -ing.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'do',   fin: ' karate',   frase: 'The rest!' },
      ],
      pie: 'Ball? play. -ing? go. The rest? do.',
      reto: { p: 'On Saturday I ___ basketball.', ops: ['play', 'go', 'do'], bien: 0 },
    },
    {
      id: 'haz-esto',
      busca: /imperative|some \/ any|instructions|commands|let's|action words|directions|turns and steps/i,
      titulo: 'Do it!',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'Open',      fin: ' the box!', frase: 'Just the verb.' },
        { arte: () => figura('triste', 'abajo'), pal: "Don't open", fin: ' it!',     frase: 'Say no with a don\'t.' },
        { arte: () => figura('feliz', 'abajo'),  pal: "Let's open", fin: ' it!',     frase: 'You and me together.' },
      ],
      pie: 'No name in front — just the verb.',
      reto: { p: '___ run in the corridor!', ops: ["Don't", 'Not', 'No'], bien: 0 },
    },
    {
      id: 'como-es',
      busca: /adjective|describing|personality|what is .* like|appearance|hair|material|made of/i,
      titulo: 'What is it like?',
      pasos: [
        { arte: () => caja(70, '#e8c49a'), pal: 'a big',       fin: ' box', frase: 'The word goes first.' },
        { arte: () => caja(70, '#d8b0d0'), pal: 'a big purple', fin: ' box', frase: 'Two words? Size first.' },
        { arte: () => caja(70, '#a8d0e8'), pal: 'The box is',   fin: ' blue', frase: 'Or put it after is.' },
      ],
      pie: 'Before the thing, or after is.',
      reto: { p: 'Which one is right?', ops: ['a box red', 'a red box', 'red a box'], bien: 1 },
    },
    {
      id: 'es-un',
      busca: /it is a|it's sunny|it's rainy|what is it|what colour|what color|this is a|a \/ an|naming|alphabet|animal sounds|weather/i,
      titulo: 'What is it?',
      pasos: [
        { arte: () => bolas(1), pal: 'It is a',  fin: ' ball',   frase: 'One thing.' },
        { arte: () => bolas(1), pal: 'It is an', fin: ' apple',  frase: 'a, e, i, o, u → an!' },
        { arte: () => bolas(1), pal: 'It is',    fin: ' red',    frase: 'And what colour is it?' },
      ],
      pie: 'a before most words, an before a, e, i, o, u.',
      reto: { p: 'It is ___ elephant.', ops: ['a', 'an', 'the'], bien: 1 },
    },
    {
      id: 'me-gusta',
      busca: /i like|don't like|likes \/ doesn't like|favourite|favorite|feelings|i have|for breakfast|would you like/i,
      titulo: 'Yes please, no thank you',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'I like',       fin: ' cake',   frase: 'Yes! 😀' },
        { arte: () => figura('triste', 'abajo'), pal: "I don't like", fin: ' fish',   frase: 'No… 🙁' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'Do you like',  fin: ' cake?',  frase: 'Ask a friend!' },
      ],
      pie: "Say no with don't.",
      reto: { p: 'Luna ___ like cats.', ops: ["don't", "doesn't", 'not'], bien: 1 },
    },
    {
      id: 'llevo',
      busca: /wearing|wear \/ carry|clothes|put on|i am wearing/i,
      titulo: 'What are you wearing?',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'I am wearing',  fin: ' a hat',    frase: 'On me, right now.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'She is wearing', fin: ' a scarf', frase: 'On her, right now.' },
        { arte: () => caja(66, '#e8c49a'),       pal: 'I am carrying',  fin: ' a bag',   frase: 'In my hand, not on me!' },
      ],
      pie: 'On your body? wearing. In your hand? carrying.',
      reto: { p: 'Erik ___ a big blue bag.', ops: ['is wearing', 'is carrying', 'wears'], bien: 1 },
    },
    {
      id: 'soy',
      busca: /i am|are you|his name|her name|he is|she is|it is|man \/ woman|boy \/ girl|have you got|to be|introduc|spell/i,
      titulo: 'Who is who?',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'I am',   fin: ' Nico',  frase: 'Me.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'He is',  fin: ' Nico',  frase: 'A boy.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'She is', fin: ' Astrid', frase: 'A girl.' },
      ],
      pie: 'I, he, she — one little word changes everything.',
      reto: { p: '___ is my sister.', ops: ['He', 'She', 'It'], bien: 1 },
    },
    {
      id: 'porque',
      busca: /because|so \(|so \/ because|reason|result|cause/i,
      titulo: 'Why? and So?',
      pasos: [
        { arte: () => figura('triste', 'abajo'), pal: 'I am tired',   fin: '',           frase: 'What happened.' },
        { arte: () => figura('triste', 'abajo'), pal: 'because',      fin: ' I ran',     frase: 'The reason.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'so',           fin: ' I sat down', frase: 'What happened next.' },
      ],
      pie: 'because looks back. so looks forward.',
      reto: { p: 'It was raining, ___ we stayed at home.', ops: ['because', 'so', 'but'], bien: 1 },
    },
    {
      id: 'el-que',
      busca: /relative clause|who, which|which, where|defining|non-defining/i,
      titulo: 'One sentence, not two',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'the girl',   fin: ' who runs',    frase: 'who — for people.' },
        { arte: () => bolas(1),                  pal: 'the ball',   fin: ' which is red', frase: 'which — for things.' },
        { arte: () => caja(70, '#e8c49a'),       pal: 'the place',  fin: ' where I live', frase: 'where — for places.' },
      ],
      pie: 'People who, things which, places where.',
      reto: { p: 'This is the book ___ I read last week.', ops: ['who', 'which', 'where'], bien: 1 },
    },
    {
      id: 'como-lo-hace',
      busca: /adverbs of manner|-ly|well, fast|how \+ adverb|slowly|loudly/i,
      titulo: 'How do you do it?',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'slow',   fin: '',    frase: 'What it is like.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'slow',   fin: 'ly',  frase: 'How you do it.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'well',   fin: '',    frase: 'This one does not take -ly!' },
      ],
      pie: 'Add -ly to say HOW. But good becomes well.',
      reto: { p: 'She sings very ___ .', ops: ['good', 'well', 'goodly'], bien: 1 },
    },
    {
      id: 'hacer',
      busca: /collocation|make and do|make \/ do|make or do/i,
      titulo: 'make or do?',
      pasos: [
        { arte: () => caja(70, '#e8c49a'), pal: 'make',  fin: ' a cake',      frase: 'When something new appears.' },
        { arte: () => figura('feliz', 'abajo'), pal: 'do', fin: ' your homework', frase: 'When it is work or a task.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'make', fin: ' a mistake', frase: 'And some you just learn!' },
      ],
      pie: 'Make it and it exists. Do it and it is done.',
      reto: { p: 'Please ___ the washing-up.', ops: ['make', 'do', 'take'], bien: 1 },
    },
    {
      id: 'cuantos',
      busca: /numbers 11|numbers 20|numbers 1|counting|how many\?/i,
      titulo: 'Counting up',
      pasos: [
        { arte: () => bolas(1), pal: 'thir',  fin: 'teen', frase: '13 — the -teen family.' },
        { arte: () => bolas(2), pal: 'thir',  fin: 'ty',   frase: '30 — the -ty family.' },
        { arte: () => bolas(3), pal: 'thirty', fin: '-one', frase: '31 — put them together.' },
      ],
      pie: '-teen is small, -ty is big. Listen to the end!',
      reto: { p: 'Which one is 15?', ops: ['fifty', 'fifteen', 'five'], bien: 1 },
    },
  ];

  /* Las unidades de repaso y las de estrategia de examen no llevan caja a
     proposito: no ensenan ninguna regla nueva, repasan las que ya se
     dieron. Ponerles una seria decorado, y ademas se la quitaria a la
     unidad donde esa regla si se explica. */
  const SIN_CAJA = /review|revision|strategies|exam strategies|whole course|paper strategies/i;

  function familiaDe(ud) {
    const t = ((ud.grammar || '') + ' ' + (ud.topic || '') + ' ' + (ud.title || '')).toLowerCase();
    if (SIN_CAJA.test(t)) return null;
    return FAMILIAS.find(f => f.busca.test(t)) || null;
  }

  function para(ud) {
    const f = familiaDe(ud);
    if (!f) return null;                    // sin caja vacia: mejor nada

    const pasos = f.pasos.map((p, i) => `
      <button class="mb-paso${i === 0 ? ' on' : ''}" type="button" data-i="${i}">
        ${p.arte()}
        <span class="mb-pal">${p.pal}<span class="mb-fin">${p.fin}</span></span>
        <p class="mb-frase">${p.frase}</p>
      </button>`).join('');

    const reto = f.reto ? `
      <div class="mb-reto">
        <p>${f.reto.p}</p>
        <div class="mb-ops">${f.reto.ops.map((o, i) =>
          `<button class="mb-op" type="button" data-i="${i}">${o}</button>`).join('')}</div>
        <p class="mb-eco" role="status"></p>
      </div>` : '';

    return {
      titulo: '🎁 The Magic Box — ' + f.titulo,
      html: `<style>${CSS}</style><div class="mb">
        <div class="mb-tira">${pasos}</div>
        <p class="mb-pie">${f.pie}</p>
        ${reto}
      </div>`,
      alMostrar(el) {
        el.querySelectorAll('.mb-paso').forEach(b => b.onclick = () => {
          el.querySelectorAll('.mb-paso').forEach(o => o.classList.remove('on'));
          b.classList.add('on');
          const t = b.querySelector('.mb-pal').textContent;
          if (window.SAY) SAY.frase(t, b);
        });
        if (!f.reto) return;
        const eco = el.querySelector('.mb-eco');
        el.querySelectorAll('.mb-op').forEach(b => b.onclick = () => {
          const bien = +b.dataset.i === f.reto.bien;
          b.classList.add(bien ? 'bien' : 'mal');
          eco.textContent = bien ? 'Yes! ⭐' : 'Try another one…';
          eco.style.color = bien ? '' : 'var(--bad)';
          if (bien) el.querySelectorAll('.mb-op').forEach(o => o.disabled = true);
        });
      },
    };
  }

  return { para, familiaDe, FAMILIAS };
})();
