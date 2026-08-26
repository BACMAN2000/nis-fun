#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Genera el splash de marca del portal NIS a partir del SVG oficial del logo.

Separa el lockup en dos SVG (la N y el texto) y los monta en una animacion CSS
con la misma linea de tiempo que el bumper en video.
"""
import re, os

SVG = "C:/Users/User/OneDrive/09_Instituciones/NORDIC/MARKETING/LOGO/SVG/Nordic Logo H.svg"
OUT = os.path.dirname(os.path.abspath(__file__))

src = open(SVG, encoding="utf-8").read()

# --- gradiente de la N (va en el <defs> del svg de la marca)
grad = re.search(r"<linearGradient\b.*?</linearGradient>", src, re.S).group(0)

# --- paths por clase: cls-1 = la N, cls-2 = el texto
paths = re.findall(r"<path\b[^>]*?/>", src, re.S)
grad_id = re.search(r'<linearGradient[^>]*\bid="([^"]+)"', src).group(1)
txt_fill = re.search(r"\.cls-2\s*\{[^}]*fill:\s*(#[0-9a-fA-F]{3,8})", src).group(1)

# El SVG original pinta por clase (.cls-1 = gradiente, .cls-2 = gris) y esas
# reglas viven en un <style> interno del archivo; al trocear el logo en dos
# se pierden, asi que el relleno se fija como atributo en cada path.
mark_paths = [p.replace('class="cls-1"', 'fill="url(#%s)"' % grad_id)
              for p in paths if 'class="cls-1"' in p]
word_paths = [p.replace('class="cls-2"', 'fill="%s"' % txt_fill)
              for p in paths if 'class="cls-2"' in p]

# el logo mide 3000 px de ancho en PNG y 569.12 en unidades SVG
K = 569.12 / 3000.0
MARK_X1 = 839 * K          # la N termina aqui
WORD_X0 = 1036 * K         # el texto empieza aqui
WORD_X1 = 3000 * K
VH = 107.24                # alto del viewBox original

mark_vb = "0 0 %.3f %.3f" % (MARK_X1, VH)
word_vb = "%.3f 0 %.3f %.3f" % (WORD_X0, WORD_X1 - WORD_X0, VH)

# proporciones reales del lockup, en multiplos del alto
MARK_R = MARK_X1 / VH                    # ancho de la N / alto
GAP_R = (WORD_X0 - MARK_X1) / VH         # separacion / alto
WORD_R = (WORD_X1 - WORD_X0) / VH        # ancho del texto / alto
BIG = 2.83                               # cuanto mas grande entra la N

mark_svg = ('<svg class="nisMark" viewBox="%s" xmlns="http://www.w3.org/2000/svg" '
            'aria-hidden="true"><defs>%s</defs>%s</svg>'
            % (mark_vb, grad, "".join(mark_paths)))
word_svg = ('<svg class="nisWord" viewBox="%s" xmlns="http://www.w3.org/2000/svg" '
            'aria-hidden="true">%s</svg>' % (word_vb, "".join(word_paths)))

CSS = """
/* ============================================================
   Splash de marca Nordic — portal NIS
   Misma linea de tiempo que el bumper en video (3.45 s):
   la N entra -> destello -> giro 3D -> se asienta en el lockup.
   ============================================================ */
.nisSplash{
  --h: clamp(30px, 5.6vw, 104px);       /* alto del lockup ya asentado */
  --big: calc(var(--h) * %(BIG)s);      /* alto de la N cuando entra sola */
  --gap: calc(var(--h) * %(GAP_R).4f);
  --wordW: calc(var(--h) * %(WORD_R).4f);
  --dur: 3.45s;
  position: fixed; inset: 0; z-index: 9999;
  display: flex; align-items: center; justify-content: center;
  background:
    radial-gradient(120%% 120%% at 50%% 45%%, #fff 0%%, #fbfbfe 45%%, #eceef7 100%%);
  animation: nisOut var(--dur) linear forwards;
}
.nisSplash[hidden]{ display: none; }

.nisStage{
  display: flex; align-items: center; justify-content: center;
  perspective: 1400px;
}

/* --- la N ------------------------------------------------- */
.nisMarkBox{
  position: relative;
  height: var(--big);
  width: calc(var(--big) * %(MARK_R).4f);
  transform-style: preserve-3d;
  animation:
    nisMarkSize var(--dur) linear forwards,
    nisMarkIn   var(--dur) linear forwards,
    nisSpin     var(--dur) linear forwards;
}
.nisMark{ display: block; width: 100%%; height: 100%%; }

/* destello que barre la silueta de la N */
.nisShine{
  position: absolute; inset: 0; pointer-events: none;
  background: linear-gradient(100deg,
      transparent 38%%, rgba(255,255,255,.15) 45%%,
      #fff 50%%, rgba(255,255,255,.15) 55%%, transparent 62%%);
  background-size: 260%% 100%%;
  background-repeat: no-repeat;
  mix-blend-mode: screen;
  opacity: 0;
  -webkit-mask-image: var(--markMask); mask-image: var(--markMask);
  -webkit-mask-size: 100%% 100%%;  mask-size: 100%% 100%%;
  -webkit-mask-repeat: no-repeat;  mask-repeat: no-repeat;
  animation: nisShine var(--dur) linear forwards;
}

/* --- el texto, revelado con wipe -------------------------- */
.nisWordBox{
  height: var(--h);
  width: 0;
  overflow: hidden;
  padding-left: var(--gap);
  box-sizing: content-box;
  animation: nisWordWipe var(--dur) linear forwards;
}
.nisWord{ display: block; height: 100%%; width: var(--wordW); max-width: none; }

/* ---------------- keyframes (%% = fraccion de 3.45 s) ------- */
@keyframes nisMarkSize{
  0%%,    15.1%% { height: var(--big); width: calc(var(--big) * %(MARK_R).4f); }
  48.1%%        { height: var(--big); width: calc(var(--big) * %(MARK_R).4f);
                 animation-timing-function: cubic-bezier(.65,0,.35,1); }
  63.8%%, 100%% { height: var(--h);   width: calc(var(--h) * %(MARK_R).4f); }
}
@keyframes nisMarkIn{
  0%%   { opacity: 0; }
  7%%   { opacity: 1; }
  100%% { opacity: 1; }
}
@keyframes nisSpin{
  0%%, 29%%   { transform: rotateY(0deg); animation-timing-function: cubic-bezier(.65,0,.35,1); }
  48.1%%, 100%% { transform: rotateY(360deg); }
}
@keyframes nisShine{
  0%%, 17.4%% { opacity: 1; background-position: -130%% 0; }
  29.6%%      { opacity: 1; background-position: 230%% 0; }
  29.7%%, 100%% { opacity: 0; background-position: 230%% 0; }
}
@keyframes nisWordWipe{
  0%%, 55.7%% { width: 0; animation-timing-function: cubic-bezier(.22,1,.36,1); }
  70.7%%, 100%% { width: var(--wordW); }
}
@keyframes nisOut{
  0%%, 89.9%% { opacity: 1; }
  100%%       { opacity: 0; }
}

/* respeta a quien pidio menos movimiento: lockup fijo y salida corta */
@media (prefers-reduced-motion: reduce){
  .nisSplash{ --dur: 1.2s; }
  .nisMarkBox{ height: var(--h); width: calc(var(--h) * %(MARK_R).4f); animation: none; }
  .nisWordBox{ width: var(--wordW); animation: none; }
  .nisShine{ display: none; }
}
""" % {"BIG": BIG, "MARK_R": MARK_R, "GAP_R": GAP_R, "WORD_R": WORD_R}

JS = """
/* Monta el splash una sola vez por sesion y lo retira al terminar.
   Un clic lo salta, igual que el splash de Presentation Plus. */
(function () {
  var KEY = 'nis_splash_seen';
  try { if (sessionStorage.getItem(KEY)) return; } catch (e) {}

  function mount() {
    var el = document.querySelector('.nisSplash');
    if (!el) return;
    try { sessionStorage.setItem(KEY, '1'); } catch (e) {}

    var done = false;
    function close() {
      if (done) return;
      done = true;
      el.hidden = true;
      el.remove();
    }
    el.addEventListener('click', close);
    var ms = (parseFloat(getComputedStyle(el).getPropertyValue('--dur')) || 3.45) * 1000;
    setTimeout(close, ms + 60);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
"""

MARKUP = """<div class="nisSplash" role="presentation">
  <div class="nisStage">
    <div class="nisMarkBox">
      %(mark)s
      <div class="nisShine"></div>
    </div>
    <div class="nisWordBox">%(word)s</div>
  </div>
</div>""" % {"mark": mark_svg, "word": word_svg}

# la mascara del destello: la propia N como SVG en data-uri
import urllib.parse
mask_svg = ('<svg viewBox="%s" xmlns="http://www.w3.org/2000/svg">%s</svg>'
            % (mark_vb, "".join(re.sub(r'fill="[^"]*"', 'fill="#000"', p)
                                for p in mark_paths)))
mask_uri = "url(\"data:image/svg+xml,%s\")" % urllib.parse.quote(mask_svg, safe="")

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Splash Nordic — portal NIS</title>
<style>
  html,body{margin:0;height:100%%;font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
  body{background:#0f172a;color:#e2e8f0;display:grid;place-items:center}
  .demo{text-align:center;padding:2rem}
  .demo h1{font-weight:600;font-size:1.25rem;margin:0 0 .5rem}
  .demo p{opacity:.7;margin:.25rem 0 1.25rem;font-size:.9rem}
  .demo button{font:inherit;padding:.6rem 1.2rem;border-radius:8px;border:1px solid #334155;
    background:#1e293b;color:#e2e8f0;cursor:pointer}
  .demo button:hover{background:#334155}
  .nisMarkBox{--markMask:%(mask)s}
%(css)s
</style>
</head>
<body>
<div class="demo">
  <h1>Splash de marca — portal NIS</h1>
  <p>Detras iria el portal. Se muestra una vez por sesion; un clic lo salta.</p>
  <button id="again">Volver a reproducir</button>
</div>

%(markup)s

<script>
%(js)s
// modo revision: ?t=1.30 congela la animacion en ese segundo
(function(){
  var m = /[?&]t=([\d.]+)/.exec(location.search);
  if (!m) return;
  var t = parseFloat(m[1]) * 1000;
  function freeze(){
    document.getAnimations().forEach(function(a){ a.pause(); a.currentTime = t; });
  }
  freeze(); setTimeout(freeze, 60); setTimeout(freeze, 250);
})();
document.getElementById('again').addEventListener('click', function(){
  try { sessionStorage.removeItem('nis_splash_seen'); } catch(e){}
  location.reload();
});
</script>
</body>
</html>
"""  % {"css": CSS, "js": JS, "markup": MARKUP, "mask": mask_uri}

open(os.path.join(OUT, "nis-splash-demo.html"), "w", encoding="utf-8").write(PAGE)

# snippet suelto para integrar en el portal
SNIP = ("<!-- ===== Splash de marca Nordic — pegar al inicio del <body> ===== -->\n"
        "<style>\n.nisMarkBox{--markMask:%s}\n%s</style>\n\n%s\n\n<script>\n%s</script>\n"
        % (mask_uri, CSS, MARKUP, JS))
open(os.path.join(OUT, "nis-splash-snippet.html"), "w", encoding="utf-8").write(SNIP)

print("mark viewBox:", mark_vb, "| paths:", len(mark_paths))
print("word viewBox:", word_vb, "| paths:", len(word_paths))
print("proporciones -> markR %.4f  gapR %.4f  wordR %.4f" % (MARK_R, GAP_R, WORD_R))
for f in ("nis-splash-demo.html", "nis-splash-snippet.html"):
    print(f, os.path.getsize(os.path.join(OUT, f)) // 1024, "KB")
