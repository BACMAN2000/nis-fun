/* Navegacion pantalla a pantalla — Fun for Nordic.
 *
 * El curso se veia como una pagina larga con todo apilado a la izquierda.
 * Ahora cada paso ocupa su propia pantalla, centrada, y se avanza con una
 * flecha a la derecha: portada del nivel, presentacion de la mascota, el
 * elenco, las unidades por tandas, y dentro de cada unidad la introduccion,
 * la historia, una actividad por pantalla y el repaso final.
 *
 * Uso:
 *   SCREENS.montar(app, [
 *     {id:'intro', titulo:'...', html:'<div>…</div>', alMostrar(el){}},
 *     ...
 *   ], {inicio: 0, alCambiar(i, total){}});
 */
window.SCREENS = (function () {

  let estado = null;

  function pinta() {
    if (!estado) return;
    const { cont, pantallas, i } = estado;
    const p = pantallas[i];

    // lo que estuviera sonando se corta aqui: la historia seguia oyendose
    // encima de la actividad siguiente
    if (window.SAY && SAY.parar) SAY.parar();
    if (window.speechSynthesis) { try { speechSynthesis.cancel(); } catch(e){} }
    cont.querySelectorAll('audio, video').forEach(m => { try { m.pause(); } catch(e){} });

    cont.querySelector('.scr-body').innerHTML = p.html;
    cont.querySelector('.scr-tit').textContent = p.titulo || '';

    // Los puntos explican adonde llevan. "Screen 5" no ayudaba a un
    // alumno (ni a un lector de pantalla) a distinguir la portada, los
    // cuentos o las unidades.
    cont.querySelector('.scr-dots').innerHTML = pantallas.map((_, k) =>
      `<button class="scr-dot${k === i ? ' on' : ''}" data-k="${k}"
         aria-label="Screen ${k + 1}: ${String(pantallas[k].titulo || 'Course content').replace(/"/g, '&quot;')}"
         title="${String(pantallas[k].titulo || 'Course content').replace(/"/g, '&quot;')}"
         ${k === i ? ' aria-current="step"' : ''}></button>`
    ).join('');

    const prev = cont.querySelector('.scr-prev');
    const next = cont.querySelector('.scr-next');
    prev.hidden = i === 0;
    next.hidden = i >= pantallas.length - 1;
    next.querySelector('.scr-lbl').textContent = p.etiquetaSiguiente || 'Next';

    cont.querySelector('.scr-cuenta').textContent = `${i + 1} / ${pantallas.length}`;

    if (typeof p.alMostrar === 'function') p.alMostrar(cont.querySelector('.scr-body'));
    if (estado.opts && typeof estado.opts.alCambiar === 'function')
      estado.opts.alCambiar(i, pantallas.length);

    cont.querySelector('.scr-body').scrollTop = 0;
    window.scrollTo(0, 0);
  }

  function ir(k) {
    if (!estado) return;
    const n = estado.pantallas.length;
    estado.i = Math.max(0, Math.min(n - 1, k));
    pinta();
  }

  /* La barra lleva las dos salidas en TODAS las pantallas: a la izquierda se
     sube un escalon del curso (unidad -> nivel -> portada) y a la derecha se
     sale al portal. Antes la vuelta iba escrita dentro del HTML de la
     primera pantalla, asi que en cuanto el alumno avanzaba se quedaba sin
     salida y tenia que retroceder con la flecha hasta el principio. */
  function salidas(opts) {
    return (opts.arriba
        ? `<a class="scr-salir" href="${opts.arriba.href}">‹ <span>${opts.arriba.texto}</span></a>`
        : '')
      + (opts.portal
        ? `<a class="scr-portal" href="${opts.portal}">🏫 <span>Portal</span></a>`
        : '');
  }

  function montar(app, pantallas, opts) {
    opts = opts || {};
    app.innerHTML = `
      <div class="scr">
        <div class="scr-top">${salidas(opts)}<h2 class="scr-tit"></h2>
          <span class="scr-cuenta"></span></div>
        <button class="scr-nav scr-prev" type="button" aria-label="Previous screen">
          <span class="scr-fl">‹</span></button>
        <div class="scr-body"></div>
        <button class="scr-nav scr-next" type="button" aria-label="Next screen">
          <span class="scr-lbl">Next</span><span class="scr-fl">›</span></button>
        <div class="scr-dots"></div>
      </div>`;
    const cont = app.querySelector('.scr');
    // ?scr=N abre directamente esa pantalla: sirve para enlazar un paso
    // concreto y para las capturas de pantalla.
    const pedida = parseInt(new URLSearchParams(location.search).get('scr'), 10);
    const arranque = Number.isFinite(pedida)
      ? Math.max(0, Math.min(pantallas.length - 1, pedida))
      : (opts.inicio || 0);
    estado = { cont, pantallas, i: arranque, opts };

    cont.querySelector('.scr-next').onclick = () => ir(estado.i + 1);
    cont.querySelector('.scr-prev').onclick = () => ir(estado.i - 1);
    cont.querySelector('.scr-dots').onclick = e => {
      const b = e.target.closest('.scr-dot');
      if (b) ir(+b.dataset.k);
    };
    // las flechas del teclado tambien pasan de pantalla, salvo mientras se
    // escribe en un ejercicio
    document.addEventListener('keydown', ev => {
      if (/^(INPUT|TEXTAREA|SELECT)$/.test((document.activeElement || {}).tagName)) return;
      if (ev.key === 'ArrowRight') ir(estado.i + 1);
      if (ev.key === 'ArrowLeft') ir(estado.i - 1);
    });
    pinta();
    return { ir, actual: () => estado.i };
  }

  return { montar, ir, actual: () => (estado ? estado.i : 0) };
})();
