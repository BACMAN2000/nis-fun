/* Grabadora de voz para las actividades de hablar — Fun for Nordic.
 *
 * El alumno graba su comparacion de las dos fotos, se escucha, y la
 * grabacion queda guardada para que el profesor la evalue despues.
 *
 * Guarda en dos sitios:
 *   - en el navegador (IndexedDB), para que el alumno pueda volver a oirse
 *     aunque no haya red;
 *   - en el servidor, cuando hay sesion iniciada, para el profesor.
 *
 * Uso:  REC.montar(el, {nivel, unidad, codigo});
 */
window.REC = (function () {

  const DB = 'nisfun-rec', TIENDA = 'audios';

  function abrirDB() {
    return new Promise((ok, mal) => {
      const q = indexedDB.open(DB, 1);
      q.onupgradeneeded = () => {
        if (!q.result.objectStoreNames.contains(TIENDA))
          q.result.createObjectStore(TIENDA, { keyPath: 'id' });
      };
      q.onsuccess = () => ok(q.result);
      q.onerror = () => mal(q.error);
    });
  }

  async function guardarLocal(id, blob, meta) {
    try {
      const db = await abrirDB();
      await new Promise((ok, mal) => {
        const t = db.transaction(TIENDA, 'readwrite');
        t.objectStore(TIENDA).put(Object.assign({ id, blob, fecha: new Date().toISOString() }, meta));
        t.oncomplete = ok; t.onerror = () => mal(t.error);
      });
      return true;
    } catch (e) { return false; }
  }

  async function leerLocal(id) {
    try {
      const db = await abrirDB();
      return await new Promise(ok => {
        const q = db.transaction(TIENDA, 'readonly').objectStore(TIENDA).get(id);
        q.onsuccess = () => ok(q.result || null);
        q.onerror = () => ok(null);
      });
    } catch (e) { return null; }
  }

  function montar(el, info) {
    const id = `${info.nivel}-u${info.unidad}-${info.codigo}`;
    el.innerHTML = `
      <div class="rec">
        <div class="rec-fila">
          <button class="rec-btn rec-grabar" type="button">
            <span class="rec-punto"></span><span class="rec-txt">Record</span></button>
          <span class="rec-tiempo">0:00</span>
          <audio class="rec-audio" controls hidden></audio>
        </div>
        <p class="rec-nota">Record yourself comparing the two pictures. You can listen to it
          and record again. Your teacher will be able to hear it.</p>
        <p class="rec-estado" role="status"></p>
      </div>`;

    const bt = el.querySelector('.rec-grabar');
    const audio = el.querySelector('.rec-audio');
    const reloj = el.querySelector('.rec-tiempo');
    const estado = el.querySelector('.rec-estado');
    let mr = null, trozos = [], t0 = 0, tic = null;

    // si ya grabo antes, que pueda volver a oirse
    leerLocal(id).then(r => {
      if (r && r.blob) {
        audio.src = URL.createObjectURL(r.blob);
        audio.hidden = false;
        estado.textContent = 'Your last recording is saved.';
      }
    });

    function reloj0(){ reloj.textContent = '0:00'; }
    function pinta(seg){
      reloj.textContent = Math.floor(seg / 60) + ':' + String(seg % 60).padStart(2, '0');
    }

    async function arranca() {
      let flujo;
      try {
        flujo = await navigator.mediaDevices.getUserMedia({ audio: true });
      } catch (e) {
        estado.textContent = 'I could not use the microphone. Please allow it in your browser.';
        return;
      }
      trozos = [];
      mr = new MediaRecorder(flujo);
      mr.ondataavailable = ev => { if (ev.data && ev.data.size) trozos.push(ev.data); };
      mr.onstop = async () => {
        flujo.getTracks().forEach(t => t.stop());
        clearInterval(tic); tic = null;
        const blob = new Blob(trozos, { type: mr.mimeType || 'audio/webm' });
        audio.src = URL.createObjectURL(blob);
        audio.hidden = false;
        bt.classList.remove('on');
        bt.querySelector('.rec-txt').textContent = 'Record again';
        estado.textContent = 'Saved. Listen to yourself!';
        await guardarLocal(id, blob, info);
        // y al servidor, si hay a donde mandarlo
        if (window.REC_SUBIR) {
          try {
            await window.REC_SUBIR(blob, Object.assign({ id }, info));
            estado.textContent = 'Saved. Your teacher can hear it now.';
          } catch (e) {
            estado.textContent = 'Saved on this device. It will be sent when you are online.';
          }
        }
      };
      mr.start();
      t0 = Date.now();
      bt.classList.add('on');
      bt.querySelector('.rec-txt').textContent = 'Stop';
      estado.textContent = 'Recording…';
      tic = setInterval(() => {
        const s = Math.floor((Date.now() - t0) / 1000);
        pinta(s);
        if (s >= 120) para();            // tope de dos minutos
      }, 250);
    }

    function para(){ if (mr && mr.state === 'recording') mr.stop(); }

    bt.onclick = () => (mr && mr.state === 'recording') ? para() : (reloj0(), arranca());
    return { id };
  }

  return { montar, leerLocal };
})();
