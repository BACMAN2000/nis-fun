/* =========================================================================
 *  PaintLayer · pintar, trazar y escribir sobre una lámina
 * -------------------------------------------------------------------------
 *  Las láminas en blanco y negro de los Listening (Flyers Part 5 «colour and
 *  write», Starters Part 4 «colour», Movers Part 5) se veían pero no se
 *  podían pintar: el alumno escribía «pig pink» en una caja y ya. Este módulo
 *  pone un lienzo transparente encima de cualquier <img> con una barra de
 *  herramientas de niño: lápiz, pincel, rotulador, borrador y texto, con la
 *  paleta de colores de los exámenes YLE.
 *
 *  Uso:
 *     var api = PaintLayer.attach(imgEl, {
 *       tools:   ['pencil','brush','pen','eraser','text'],   // qué se ofrece
 *       colours: PaintLayer.YLE,                            // paleta
 *       initial: datosGuardados,                            // {v:1,w,h,ops:[…]}
 *       onChange: function(datos){ … }                     // cada trazo (con calma)
 *     });
 *     api.getData() / api.setData(d) / api.clear() / api.toDataURL() / api.destroy()
 *
 *  Lo que se guarda son los TRAZOS (no un PNG): pesan poco, se rehacen a
 *  cualquier tamaño y permiten deshacer. El pincel y el rotulador pintan en
 *  modo «multiply», así el negro del dibujo se sigue viendo debajo del color,
 *  como al colorear con lápices de verdad. El lápiz escribe encima (para
 *  trazar líneas y escribir palabras) y el borrador solo quita lo pintado,
 *  nunca la lámina.
 * ========================================================================= */
(function(){
'use strict';
if(window.PaintLayer) return;

var YLE = [
  {n:'red',    c:'#e53935'}, {n:'blue',   c:'#1e88e5'}, {n:'green',  c:'#43a047'},
  {n:'yellow', c:'#fdd835'}, {n:'orange', c:'#fb8c00'}, {n:'pink',   c:'#f06292'},
  {n:'purple', c:'#8e24aa'}, {n:'brown',  c:'#795548'}, {n:'grey',   c:'#9e9e9e'},
  {n:'black',  c:'#212121'}
];
var TOOLS = {
  pencil: {label:'Pencil', icon:'✏️', size:3,  alpha:1,   mode:'source-over'},
  pen:    {label:'Colour pen', icon:'🖍️', size:9,  alpha:1,   mode:'multiply'},
  brush:  {label:'Brush',  icon:'🖌️', size:22, alpha:.55, mode:'multiply'},
  eraser: {label:'Eraser', icon:'🧽', size:24, alpha:1,   mode:'destination-out'},
  text:   {label:'Write',  icon:'🔤', size:0,  alpha:1,   mode:'source-over'}
};
var SIZES = {S:.6, M:1, L:1.8};
var MAXW = 1600;            // el lienzo interno no pasa de aquí: memoria en tablets
var CSS_ID = 'pl-css';

function css(){
  if(document.getElementById(CSS_ID)) return;
  var s = document.createElement('style'); s.id = CSS_ID;
  s.textContent = [
  '.pl-wrap{position:relative;display:block;width:100%;max-width:820px;margin:10px 0;user-select:none;-webkit-user-select:none}',
  '.pl-wrap img{display:block;width:100%;height:auto;margin:0!important;border-radius:14px}',
  '.pl-canvas{position:absolute;left:0;top:0;width:100%;height:100%;touch-action:none;cursor:crosshair;border-radius:14px}',
  '.pl-wrap.pl-text .pl-canvas{cursor:text}',
  '.pl-bar{display:flex;flex-wrap:wrap;align-items:center;gap:6px;padding:8px 10px;margin:8px 0 0;background:#f4f6fb;border:1px solid #d9deea;border-radius:12px;font-family:inherit}',
  '.pl-bar .pl-grp{display:flex;align-items:center;gap:4px;padding-right:8px;margin-right:2px;border-right:1px solid #d9deea}',
  '.pl-bar .pl-grp:last-child{border-right:0}',
  '.pl-bar button{border:1px solid #cfd6e4;background:#fff;border-radius:9px;min-width:38px;height:36px;padding:0 8px;font-size:1.05rem;cursor:pointer;line-height:1;color:#1e293b}',
  '.pl-bar button:hover{background:#eef2ff}',
  '.pl-bar button.on{background:#1e3a8a;color:#fff;border-color:#1e3a8a;box-shadow:0 0 0 2px #c7d2fe}',
  '.pl-bar button:disabled{opacity:.4;cursor:default}',
  '.pl-bar .pl-sw{width:28px;height:28px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 1px #b8c0d0;cursor:pointer;padding:0;min-width:0}',
  '.pl-bar .pl-sw.on{box-shadow:0 0 0 3px #1e3a8a;transform:scale(1.12)}',
  '.pl-bar .pl-sz{font-size:.8rem;font-weight:700;min-width:32px}',
  '.pl-bar .pl-hint{font-size:.78rem;color:#64748b;margin-left:auto}',
  '.pl-textbox{position:absolute;z-index:5;border:2px dashed #1e3a8a;background:rgba(255,255,255,.9);border-radius:6px;padding:2px 6px;font-weight:700;outline:none;min-width:60px}',
  '@media (max-width:600px){.pl-bar button{min-width:34px;height:34px;font-size:1rem}.pl-bar .pl-sw{width:24px;height:24px}}'
  ].join('\n');
  document.head.appendChild(s);
}

function attach(img, opts){
  opts = opts || {};
  css();
  if(img.__pl) return img.__pl;
  var tools = opts.tools || ['pencil','brush','pen','eraser','text'];
  var colours = opts.colours || YLE;
  var lang = opts.lang || 'en';
  var font = opts.font || '"Comic Sans MS","Segoe Print","Chalkboard SE",sans-serif';

  /* ---- DOM: envolver la imagen y poner el lienzo encima ---- */
  var wrap = document.createElement('div'); wrap.className = 'pl-wrap';
  img.parentNode.insertBefore(wrap, img); wrap.appendChild(img);
  var cv = document.createElement('canvas'); cv.className = 'pl-canvas';
  wrap.appendChild(cv);
  var ctx = cv.getContext('2d');
  var bar = document.createElement('div'); bar.className = 'pl-bar';
  wrap.parentNode.insertBefore(bar, wrap.nextSibling);

  /* ---- estado ---- */
  var ops = [];           // trazos y textos, en orden
  var redo = [];
  var tool = tools[0], colour = colours[colours.length-1].c, size = 'M';
  var drawing = null;     // trazo en curso
  var tChange = null;
  var W = 0, H = 0;       // tamaño interno del lienzo

  function medir(){
    var nw = img.naturalWidth || 1200, nh = img.naturalHeight || 700;
    var k = Math.min(1, MAXW / nw);
    W = Math.round(nw * k); H = Math.round(nh * k);
    cv.width = W; cv.height = H;
    repinta();
  }
  if(img.complete && img.naturalWidth) medir(); else img.addEventListener('load', medir);

  function trazo(o){
    if(o.t === 'text'){
      ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
      ctx.fillStyle = o.c; ctx.font = 'bold ' + Math.round(o.s) + 'px ' + font;
      ctx.textBaseline = 'middle';
      ctx.fillText(o.txt, o.x, o.y);
      return;
    }
    var T = TOOLS[o.t] || TOOLS.pencil;
    ctx.globalCompositeOperation = T.mode; ctx.globalAlpha = T.alpha;
    ctx.strokeStyle = o.c; ctx.lineWidth = o.s; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    var p = o.p;
    ctx.beginPath();
    if(p.length < 4){ ctx.arc(p[0], p[1], o.s/2, 0, Math.PI*2); ctx.fillStyle = o.c; ctx.fill(); return; }
    ctx.moveTo(p[0], p[1]);
    for(var i = 2; i < p.length; i += 2) ctx.lineTo(p[i], p[i+1]);
    ctx.stroke();
  }
  function repinta(){
    ctx.setTransform(1,0,0,1,0,0);
    ctx.clearRect(0,0,W,H);
    for(var i = 0; i < ops.length; i++) trazo(ops[i]);
    if(drawing) trazo(drawing);
    ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
  }
  function cambio(){
    botones();
    clearTimeout(tChange);
    tChange = setTimeout(function(){ if(opts.onChange) opts.onChange(getData()); }, 400);
  }

  /* ---- coordenadas: del puntero al lienzo interno ---- */
  function xy(e){
    var r = cv.getBoundingClientRect();
    return [ (e.clientX - r.left) * W / r.width, (e.clientY - r.top) * H / r.height ];
  }
  function grosor(){ return (TOOLS[tool].size * SIZES[size]) * (W / 1200); }

  /* ---- dibujar ---- */
  cv.addEventListener('pointerdown', function(e){
    if(e.button && e.button !== 0) return;
    // preventDefault también aquí: si no, el mousedown le quita el foco a la
    // caja de texto recién creada y se cierra vacía antes de poder escribir
    e.preventDefault();
    if(tool === 'text'){ caja(e); return; }
    try { cv.setPointerCapture(e.pointerId); } catch(err){}
    var q = xy(e);
    drawing = {t:tool, c:colour, s:Math.max(1, grosor()), p:[Math.round(q[0]), Math.round(q[1])]};
    repinta();
  });
  cv.addEventListener('pointermove', function(e){
    if(!drawing) return;
    e.preventDefault();
    var q = xy(e), p = drawing.p, n = p.length;
    var dx = q[0] - p[n-2], dy = q[1] - p[n-1];
    if(dx*dx + dy*dy < 4) return;         // puntos casi iguales: no engordan el guardado
    p.push(Math.round(q[0]), Math.round(q[1]));
    // solo el tramo nuevo, para no repintar todo en cada movimiento
    var T = TOOLS[drawing.t];
    ctx.globalCompositeOperation = T.mode; ctx.globalAlpha = T.alpha;
    ctx.strokeStyle = drawing.c; ctx.lineWidth = drawing.s; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    if(T.alpha < 1){ repinta(); return; }  // con transparencia los tramos se solapan: mejor entero
    ctx.beginPath(); ctx.moveTo(p[n-2], p[n-1]); ctx.lineTo(p[n], p[n+1]); ctx.stroke();
  });
  function suelta(e){
    if(!drawing) return;
    ops.push(drawing); drawing = null; redo = [];
    repinta(); cambio();
  }
  cv.addEventListener('pointerup', suelta);
  cv.addEventListener('pointercancel', suelta);
  cv.addEventListener('lostpointercapture', suelta);

  /* ---- escribir: una caja donde se pulsa; Enter la fija en el lienzo ---- */
  var box = null;
  function caja(e){
    if(box) fijar();
    var r = cv.getBoundingClientRect();
    var q = xy(e);
    box = document.createElement('input');
    box.className = 'pl-textbox'; box.type = 'text'; box.autocomplete = 'off'; box.spellcheck = false;
    box.placeholder = lang === 'es' ? 'escribe…' : 'type…';
    var px = 22 * SIZES[size] * (r.width / 820);
    box.style.left = Math.max(0, e.clientX - r.left - 4) + 'px';
    box.style.top = Math.max(0, e.clientY - r.top - px * .9) + 'px';
    box.style.font = 'bold ' + px + 'px ' + font; box.style.color = colour;
    box.__q = q;
    wrap.appendChild(box);
    setTimeout(function(){ if(box) box.focus(); }, 0);
    box.onkeydown = function(ev){
      if(ev.key === 'Enter'){ ev.preventDefault(); fijar(); }
      if(ev.key === 'Escape'){ ev.preventDefault(); box.remove(); box = null; }
    };
    box.onblur = function(){ setTimeout(function(){ if(box) fijar(); }, 150); };
  }
  function fijar(){
    if(!box) return;
    var v = box.value.trim(), q = box.__q;
    box.remove(); box = null;
    if(!v) return;
    ops.push({t:'text', c:colour, s:Math.round(30 * SIZES[size] * (W / 1200)), x:Math.round(q[0]), y:Math.round(q[1]), txt:v});
    redo = []; repinta(); cambio();
  }

  /* ---- barra ---- */
  var btns = {};
  function b(html, title, fn, cls){
    var e = document.createElement('button'); e.type = 'button'; e.innerHTML = html; e.title = title;
    if(cls) e.className = cls; e.onclick = fn; return e;
  }
  function grp(){ var g = document.createElement('div'); g.className = 'pl-grp'; bar.appendChild(g); return g; }
  var gT = grp();
  tools.forEach(function(k){
    var T = TOOLS[k]; if(!T) return;
    btns[k] = b(T.icon, T.label, function(){ tool = k; wrap.classList.toggle('pl-text', k === 'text'); botones(); });
    gT.appendChild(btns[k]);
  });
  var gC = grp(); var sws = [];
  colours.forEach(function(c){
    var e = b('', c.n, function(){ colour = c.c; if(tool === 'eraser') tool = tools[0]; botones(); }, 'pl-sw');
    e.style.background = c.c; e.dataset.c = c.c; sws.push(e); gC.appendChild(e);
  });
  var gS = grp(); var szb = {};
  ['S','M','L'].forEach(function(k){ szb[k] = b(k, {S:'Thin',M:'Medium',L:'Thick'}[k], function(){ size = k; botones(); }, 'pl-sz'); gS.appendChild(szb[k]); });
  var gU = grp();
  var bUndo = b('↶', 'Undo', function(){ if(!ops.length) return; redo.push(ops.pop()); repinta(); cambio(); });
  var bRedo = b('↷', 'Redo', function(){ if(!redo.length) return; ops.push(redo.pop()); repinta(); cambio(); });
  var bClear = b('🗑️', 'Clear everything', function(){
    if(!ops.length) return;
    if(!confirm(lang === 'es' ? '¿Borrar todo lo pintado?' : 'Clear everything you painted?')) return;
    redo = ops.slice(); ops = []; repinta(); cambio();
  });
  gU.appendChild(bUndo); gU.appendChild(bRedo); gU.appendChild(bClear);
  var hint = document.createElement('span'); hint.className = 'pl-hint'; bar.appendChild(hint);
  function botones(){
    Object.keys(btns).forEach(function(k){ btns[k].classList.toggle('on', k === tool); });
    sws.forEach(function(e){ e.classList.toggle('on', e.dataset.c === colour && tool !== 'eraser'); });
    Object.keys(szb).forEach(function(k){ szb[k].classList.toggle('on', k === size); });
    bUndo.disabled = !ops.length; bRedo.disabled = !redo.length; bClear.disabled = !ops.length;
    var T = TOOLS[tool];
    hint.textContent = tool === 'text' ? (lang === 'es' ? 'Toca la lámina y escribe · Enter para fijar' : 'Tap the picture and type · Enter to place')
                     : tool === 'eraser' ? (lang === 'es' ? 'Borra solo lo pintado' : 'Erases only your painting')
                     : (T.label + ' · ' + (colours.filter(function(c){ return c.c === colour; })[0] || {n:''}).n);
  }
  botones();

  /* ---- API ---- */
  function getData(){ return {v:1, w:W, h:H, ops:ops}; }
  function setData(d){
    ops = []; redo = [];
    if(d && d.ops && d.ops.length){
      // si el lienzo se midió con otro ancho, se escalan los trazos
      var k = (d.w && W) ? W / d.w : 1;
      ops = d.ops.map(function(o){
        if(k === 1) return o;
        var c = Object.assign({}, o);
        if(o.p) c.p = o.p.map(function(v){ return Math.round(v * k); });
        if(o.t === 'text'){ c.x = Math.round(o.x * k); c.y = Math.round(o.y * k); }
        c.s = o.s * k; return c;
      });
    }
    repinta(); botones();
  }
  var api = {
    getData: getData, setData: setData,
    clear: function(){ ops = []; redo = []; repinta(); cambio(); },
    isEmpty: function(){ return !ops.length; },
    count: function(){ return ops.length; },
    toDataURL: function(){        // lámina + pintura, para el profesor o para imprimir
      var out = document.createElement('canvas'); out.width = W; out.height = H;
      var c = out.getContext('2d');
      try { c.drawImage(img, 0, 0, W, H); } catch(e){}
      c.drawImage(cv, 0, 0);
      return out.toDataURL('image/png');
    },
    setTool: function(k){ if(TOOLS[k]){ tool = k; botones(); } },
    setColour: function(c){ colour = c; botones(); },
    destroy: function(){ bar.remove(); cv.remove(); wrap.parentNode.insertBefore(img, wrap); wrap.remove(); delete img.__pl; },
    el: wrap, bar: bar
  };
  if(opts.initial){
    if(W) setData(opts.initial); else img.addEventListener('load', function(){ setData(opts.initial); }, {once:true});
  }
  img.__pl = api;
  return api;
}

window.PaintLayer = { attach: attach, YLE: YLE, TOOLS: TOOLS };
})();
