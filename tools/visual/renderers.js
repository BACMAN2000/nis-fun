
/* ---------------------------------------------------------------------
   Tareas visuales del examen A2 Flyers (Listening 1, 3 y 4; R&W 7).
   Las genera tools/gen_visual_flyers.py y las dibuja con lo nuestro:
   personajes de content/cast-flyers.json sobre escenarios de assets/scenes.
   --------------------------------------------------------------------- */

/* Un dibujo de vocabulario, con los tres respaldos que ya usa la pantalla
   de palabras: PNG propio -> SVG propio -> emoji. Se devuelve HTML. */
function visDibujo(palabra){
  const k = String(palabra||'').toLowerCase().replace(/^(a|an|the) /,'');
  const art = (window.VOCAB_ART && VOCAB_ART.get(k)) || null;
  const plano = art || `<span class="emo">${EMOJI[k] || '✏️'}</span>`;
  const slug = k.replace(/'/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
  return `<img src="../assets/vocab/${slug}.png?v=${ART_V}" alt="${esc(k)}"
    onerror="this.replaceWith(...new DOMParser().parseFromString(this.dataset.fb,'text/html').body.childNodes)"
    data-fb="${esc(plano)}">`;
}

/* El escenario de fondo. Si la foto no esta, el bloque se queda con el
   color de fondo y los personajes siguen viendose: mejor eso que un icono
   de imagen rota encima de la escena. */
function visFondo(sitio){
  return `<img class="fondo" alt="" src="../assets/scenes/${sitio}.jpg?v=${ART_V}"
    onerror="this.onerror=null;this.src='../assets/scenes/${sitio}.png?v=${ART_V}';
             this.addEventListener('error',()=>this.remove(),{once:true})">`;
}

function visPersona(p){
  return `<img src="${CHAR(p.slug, p.pose||1)}" alt="${esc(p.name||p.slug)}" ${FB}>`;
}

/* La etiqueta de KPI. Es lo que convierte una tarea de examen suelta en
   una actividad de la clase de 5.o: dice de que unidad del Scope &
   Sequence sale y que outcome cubre. */
function visKpi(act){
  const k = act.kpi; if(!k) return '';
  const partes = [];
  if(k.examen_parte) partes.push(`${k.examen} · ${k.examen_parte.paper} Part ${k.examen_parte.part}`);
  if(k.tema && k.tema.nombre) partes.push(`${k.grado} · Unit ${k.tema.n}: ${k.tema.nombre}`);
  if(k.destreza) partes.push(k.destreza);
  return `<div class="vis-kpi">${partes.map(t=>`<span>${esc(t)}</span>`).join('')}</div>`;
}

/* Reproductor compartido de las tres tareas de listening.
   Misma logica que la actividad 'listening': si el mp3 no esta todavia,
   se lee el guion con la voz del navegador y se avisa de que es
   provisional, para que nadie crea que ese es el audio definitivo. */
function visAudio(el, act, guion){
  const caja = document.createElement('div');
  caja.className = 'lsn-mando';
  caja.innerHTML = `<button class="play" type="button">▶ Play</button>
    <button class="stop" type="button" disabled>⏹ Stop</button>
    <span class="provisional"></span>`;
  el.prepend(caja);

  const bPlay = caja.querySelector('.play'), bStop = caja.querySelector('.stop');
  const audio = act.audio ? new Audio(`../audio/${act.audio}`) : null;
  let modo = audio ? 'mp3' : 'tts', hablando = false;
  if (!audio) caja.querySelector('.provisional').textContent =
    '(temporary browser voice — the real audio is coming soon)';
  if (audio) audio.onerror = () => { modo = 'tts';
    caja.querySelector('.provisional').textContent =
      '(temporary browser voice — the real audio is coming soon)'; };

  const estado = son => { bStop.disabled = !son;
    bPlay.textContent = son ? '▶ Playing…' : '▶ Play'; bPlay.disabled = son; };
  if (audio) audio.onended = () => estado(false);

  bPlay.onclick = () => {
    if (modo === 'mp3' && audio && !audio.error){ audio.play(); estado(true); return; }
    const partes = String(guion||'').split('…');
    speechSynthesis.cancel();
    const voces = speechSynthesis.getVoices().filter(v => v.lang.startsWith('en'));
    partes.forEach((p, i) => {
      const u = new SpeechSynthesisUtterance(p.replace(/^[^:]+:/, '').trim());
      u.lang = 'en-GB'; u.rate = .92;
      if (voces.length) u.voice = voces[i % 2] || voces[0];
      if (i === partes.length - 1) u.onend = () => { hablando = false; estado(false); };
      speechSynthesis.speak(u);
    });
    hablando = true; estado(true);
  };
  bStop.onclick = () => {
    if (hablando){ speechSynthesis.cancel(); hablando = false; }
    if (audio){ audio.pause(); audio.currentTime = 0; }
    estado(false);
  };
}

const RENDER = {

/* ---- Listening Part 1: escribir el nombre debajo de cada persona ---- */
label_people(act, el){
  const d = act.data;
  el.innerHTML = `${visKpi(act)}
    <p class="vis-sitio">Everybody is in ${esc(d.place || 'the picture')}.</p>
    <div class="vis-escena">${visFondo(d.scene)}
      <div class="vis-fila">${d.people.map((p,i)=>`<div class="vis-quien">
        <span class="num">${i+1}</span>${visPersona(p)}
        <input data-i="${i}" autocomplete="off" spellcheck="false" aria-label="Name ${i+1}"></div>`).join('')}</div>
    </div>
    <div class="vis-banco">${d.names.map(n=>`<span data-n="${esc(n)}">${esc(n)}</span>`).join('')}</div>
    <div class="checkrow final"><button class="chk">Check</button>
      <button class="again" type="button" hidden>↻ Try again</button>
      <button class="reveal" type="button" hidden>👁 See the answers</button>
      <span class="score"></span><span class="tries"></span></div>`;

  visAudio(el, act, d.script);

  const entradas = () => [...el.querySelectorAll('.vis-quien input')];
  // el banco tacha los nombres ya escritos: son ocho para cinco huecos y
  // sin la marca el alumno pierde la cuenta de cuales le quedan
  const repinta = () => {
    const puestos = entradas().map(i => i.value.trim().toLowerCase());
    el.querySelectorAll('.vis-banco span').forEach(s =>
      s.classList.toggle('usado', puestos.includes(s.dataset.n.toLowerCase())));
  };
  el.addEventListener('input', repinta);
  el.querySelectorAll('.vis-banco span').forEach(s => s.onclick = () => {
    const libre = entradas().find(i => !i.value.trim() && !i.disabled);
    if (libre){ libre.value = s.dataset.n; repinta(); }
  });

  cicloIntentos(el, {
    entradas,
    corrige(){
      let bien = 0;
      entradas().forEach(inp => {
        const ok = inp.value.trim().toLowerCase() === d.people[+inp.dataset.i].name.toLowerCase();
        inp.className = ok ? 'ok' : 'bad';
        if (ok) bien++;
      });
      return { bien, total: d.people.length };
    },
    revela(){
      entradas().forEach(inp => {
        inp.value = d.people[+inp.dataset.i].name; inp.className = 'revelado';
      });
      repinta();
    },
    alAcertar(){ complete(act.code); },
  });
},

/* ---- Listening Part 4: escuchar y marcar una de tres imagenes ---- */
picture_mc(act, el){
  const d = act.data;
  const LET = 'ABC';
  el.innerHTML = `${visKpi(act)}
    ${d.questions.map((q,i)=>`<div class="vis-preg" data-q="${i}">
      <p>${i+1}. ${esc(q.q)}</p>
      <div class="vis-ops">${q.options.map((o,j)=>`<button class="vis-op" type="button"
          data-q="${i}" data-w="${esc(o.word)}" aria-label="Picture ${LET[j]}: ${esc(o.word)}">
          <span class="letra">${LET[j]}</span>
          <span class="dib">${visDibujo(o.word)}</span>
          <span class="pie">${esc(o.word)}</span></button>`).join('')}</div></div>`).join('')}
    <div class="checkrow final"><button class="chk">Check</button>
      <button class="again" type="button" hidden>↻ Try again</button>
      <button class="reveal" type="button" hidden>👁 See the answers</button>
      <span class="score"></span><span class="tries"></span></div>`;

  visAudio(el, act, d.script);

  el.querySelectorAll('.vis-op').forEach(b => b.onclick = () => {
    if (b.disabled) return;
    el.querySelectorAll(`.vis-op[data-q="${b.dataset.q}"]`)
      .forEach(x => x.classList.remove('sel'));
    b.classList.add('sel');
  });

  // cicloIntentos habla de inputs; aqui las respuestas son botones, asi que
  // se le pasa una lista de botones y se usa 'disabled' igual que alli
  const botones = () => [...el.querySelectorAll('.vis-op')];
  cicloIntentos(el, {
    entradas: botones,
    limpia(){ botones().forEach(b => b.className = 'vis-op'); },
    corrige(){
      let bien = 0;
      el.querySelectorAll('.vis-ops').forEach(o => o.classList.add('resuelto'));
      d.questions.forEach((q,i) => {
        const sel = el.querySelector(`.vis-op[data-q="${i}"].sel`);
        if (sel && sel.dataset.w === q.answer){ sel.classList.add('ok'); bien++; }
        else if (sel) sel.classList.add('bad');
      });
      return { bien, total: d.questions.length };
    },
    revela(){
      d.questions.forEach((q,i) => {
        el.querySelectorAll(`.vis-op[data-q="${i}"]`).forEach(b => {
          b.classList.remove('ok','bad','sel');
          if (b.dataset.w === q.answer) b.classList.add('marca');
        });
      });
    },
    alAcertar(){ complete(act.code); },
  });
},

/* ---- Listening Part 3: emparejar cada explorador con una letra A-H ---- */
match_pictures(act, el){
  const d = act.data;
  const letras = d.pictures.map(p => p.id);
  el.innerHTML = `${visKpi(act)}
    <div class="vis-galeria">${d.pictures.map(p=>`<div class="vis-foto" data-id="${p.id}">
      <span class="letra">${p.id}</span>
      <span class="dib">${visDibujo(p.word)}</span></div>`).join('')}</div>
    <div class="vis-gente">${d.people.map((p,i)=>`<div class="vis-quien">
      ${visPersona(p)}<b>${esc(p.name)}</b>
      <select data-i="${i}" aria-label="Picture for ${esc(p.name)}">
        <option value="">–</option>
        ${letras.map(l=>`<option value="${l}">${l}</option>`).join('')}
      </select></div>`).join('')}</div>
    <div class="checkrow final"><button class="chk">Check</button>
      <button class="again" type="button" hidden>↻ Try again</button>
      <button class="reveal" type="button" hidden>👁 See the answers</button>
      <span class="score"></span><span class="tries"></span></div>`;

  visAudio(el, act, d.script);

  const selects = () => [...el.querySelectorAll('.vis-gente select')];
  // marcar en verde las fotos ya repartidas: hay ocho y solo cinco valen,
  // asi se ve de un vistazo cuales quedan libres
  const repinta = () => {
    const puestas = selects().map(s => s.value).filter(Boolean);
    el.querySelectorAll('.vis-foto').forEach(f =>
      f.classList.toggle('usada', puestas.includes(f.dataset.id)));
  };
  el.addEventListener('change', repinta);

  cicloIntentos(el, {
    entradas: selects,
    corrige(){
      let bien = 0;
      selects().forEach(s => {
        const nombre = d.people[+s.dataset.i].name;
        const ok = s.value && s.value === d.answers[nombre];
        s.className = ok ? 'ok' : 'bad';
        if (ok) bien++;
      });
      return { bien, total: d.people.length };
    },
    revela(){
      selects().forEach(s => {
        s.value = d.answers[d.people[+s.dataset.i].name] || '';
        s.className = 'revelado';
      });
      repinta();
    },
    alAcertar(){ complete(act.code); },
  });
},

/* ---- Reading & Writing Part 7: la historia de tres vinetas ----
   El benchmark de 5.o la pide con estas palabras: "Writing Part 3: 20-25-word
   picture story". Por eso el contador de palabras va delante y no detras:
   quedarse corto es el error tipico y hay que verlo mientras se escribe. */
picture_story(act, el){
  const d = act.data;
  const min = d.min_words || 20, max = d.max_words || 25;
  el.innerHTML = `${visKpi(act)}
    <div class="vis-tira">${d.frames.map(f=>`<div class="vis-vineta">
      <div class="marco"><span class="nn">${f.n}</span>${visFondo(f.scene)}
        <div class="gente">${(f.people||[]).map(visPersona).join('')}</div></div>
      <div class="pista">${esc(f.hint)}</div></div>`).join('')}</div>
    ${d.support ? `<div class="vis-apoyo">
      ${d.support.grammar ? `<b>${esc(d.support.grammar)}</b>` : ''}
      ${(d.support.words||[]).map(w=>`<span>${esc(w)}</span>`).join('')}</div>` : ''}
    <div class="vis-historia">
      <textarea placeholder="Write the story here — ${min} to ${max} words."
        aria-label="Your story"></textarea>
      <div class="vis-contador">0 words</div>
    </div>
    <div class="checkrow"><button class="chk">I have finished</button>
      <button class="reveal" type="button">👁 See one possible story</button>
      <span class="score"></span></div>`;

  const ta = el.querySelector('textarea');
  const cnt = el.querySelector('.vis-contador');
  const cuenta = () => (ta.value.trim().match(/\S+/g) || []).length;
  ta.addEventListener('input', () => {
    const n = cuenta();
    cnt.textContent = `${n} word${n === 1 ? '' : 's'}` +
      (n < min ? ` — ${min - n} more to go` : (n > max ? ` — ${n - max} too many` : ' — just right'));
    cnt.classList.toggle('bien', n >= min && n <= max);
  });

  el.querySelector('.chk').onclick = () => {
    const n = cuenta();
    const s = el.querySelector('.score');
    if (!n){ s.textContent = 'Write your story first.'; s.className = 'score partial'; return; }
    // Escribir no se corrige solo: se da por hecha y complete() ya guarda el
    // texto para que lo lea el profesor. Poner una nota automatica a una
    // redaccion seria mentir.
    s.textContent = n >= min && n <= max ? 'Sent to your teacher ✓'
                                         : `Sent — but it is ${n} words, not ${min}-${max}.`;
    s.className = 'score ' + (n >= min && n <= max ? 'good' : 'partial');
    complete(act.code);
  };

  el.querySelector('.reveal').onclick = e => {
    e.target.hidden = true;
    const caja = document.createElement('div');
    caja.className = 'vis-modelo';
    caja.innerHTML = `<b>One way of telling it:</b><br>${esc(d.model)}`;
    el.querySelector('.vis-historia').appendChild(caja);
  };
},
