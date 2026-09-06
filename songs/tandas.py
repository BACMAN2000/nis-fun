# -*- coding: utf-8 -*-
"""
Genera songs/tandas.html: la hoja de trabajo para generar las 90 piezas en Suno.

Las letras y los estilos ya están escritos y revisados; lo que queda es el
trabajo manual en Suno, que no puede hacer quien no oye el audio: cada Create
da dos versiones y hay que elegir la buena con el pulgar.

Esta hoja quita de en medio todo lo demás: cada pieza trae su letra y su estilo
en un botón de copiar, en el orden de las tandas, con una casilla para marcar
lo hecho. Lo marcado se guarda en el navegador, así que se puede parar y seguir
otro día — y el cupo de descargas obliga a parar.
"""
import io, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

AQUI = os.path.dirname(os.path.abspath(__file__))
d = json.load(io.open(os.path.join(AQUI, 'starters.json'), encoding='utf-8'))
suno = json.load(io.open(os.path.join(AQUI, 'starters-suno.json'), encoding='utf-8'))
# «Hecha» = DESCARGADA. Las 90 ya están generadas en Suno y las 90 tienen su
# toma elegida por el usuario; lo único que falta es bajarlas, y el cupo de
# descargas de la cuenta Pro no da para las 90 de una sentada.
hechas, elegidas = set(), {}
for bloque in ('canciones', 'chants'):
    for u, v in (suno.get(bloque) or {}).items():
        if u.startswith('_'):
            continue
        clave = f'{u}-{"cancion" if bloque == "canciones" else "chant"}'
        elegidas[clave] = v.get('elegida')
        if v.get('descargada'):
            hechas.add(clave)

POR_TANDA = 25         # el cupo ronda las 27 descargas por ciclo
piezas = []
for u in sorted(d['unidades'], key=lambda x: int(x)):
    unidad = d['unidades'][u]
    for tipo in ('chant', 'cancion'):
        p = unidad.get(tipo)
        if not p:
            continue
        piezas.append({
            'id': f'{u}-{tipo}', 'unidad': u, 'tipo': tipo,
            'tema': unidad.get('titulo_unidad', ''),
            'gramatica': unidad.get('gramatica', ''),
            'titulo': p.get('titulo', ''),
            'letra': p.get('letra', ''),
            'estilo': p.get('estilo', ''),
            'hecha': f'{u}-{tipo}' in hechas,
            'elegida': elegidas.get(f'{u}-{tipo}'),
        })

def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

filas = []
for i, p in enumerate(piezas):
    tanda = i // POR_TANDA + 1
    filas.append(f'''<div class="pieza{' hecha' if p['hecha'] else ''}" data-id="{p['id']}" data-tanda="{tanda}">
  <label class="cab"><input type="checkbox" {'checked' if p['hecha'] else ''}>
    <b>U{p['unidad']} · {esc(p['tipo'])}</b>
    <span class="tit">{esc(p['titulo'])}</span>
    <span class="tema">{esc(p['tema'])} — {esc(p['gramatica'])}</span>
    <code class="id">{esc((p['elegida'] or '')[:8])}</code></label>
  <div class="cajas">
    <div><h4>Lyrics <button class="cp" data-t="l{i}">copiar</button></h4>
      <pre id="l{i}">{esc(p['letra'])}</pre></div>
    <div><h4>Styles <button class="cp" data-t="s{i}">copiar</button></h4>
      <pre id="s{i}">{esc(p['estilo'])}</pre></div>
  </div>
</div>''')

html = f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Suno · las 90 piezas de Starters</title>
<style>
 body{{font:15px/1.5 system-ui,sans-serif;margin:0;background:#f4f6fb;color:#1f2430}}
 .wrap{{max-width:1000px;margin:0 auto;padding:18px}}
 h1{{font-size:20px;margin:0 0 4px}}
 .sub{{color:#5b6b8c;font-size:13px;margin:0 0 14px}}
 .barra{{position:sticky;top:0;background:#f4f6fb;padding:10px 0;border-bottom:1px solid #dde3f0;z-index:5}}
 .pieza{{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:10px 12px;margin:10px 0}}
 .pieza.hecha{{opacity:.5}}
 .cab{{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;cursor:pointer}}
 .tit{{font-weight:600}}
 .tema{{color:#64748b;font-size:12.5px}}
 .cajas{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px}}
 @media(max-width:820px){{.cajas{{grid-template-columns:1fr}}}}
 h4{{margin:0 0 4px;font-size:12px;color:#5b6b8c;display:flex;gap:8px;align-items:center}}
 pre{{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:8px;margin:0;
      white-space:pre-wrap;font:12.5px/1.5 ui-monospace,Consolas,monospace;max-height:230px;overflow:auto}}
 button{{font:600 11px system-ui;border:1px solid #93b4dd;background:#fff;color:#24507a;
         border-radius:99px;padding:2px 9px;cursor:pointer}}
 button:hover{{background:#e8f0fb}}
 .id{{color:#94a3b8;font-size:11px}}
 .tanda{{margin:22px 0 6px;font-weight:700;color:#24507a;border-top:2px solid #dde3f0;padding-top:10px}}
</style></head><body><div class="wrap">
<h1>Descargar las 90 piezas de Starters</h1>
<p class="sub"><b>Ya están generadas en Suno y las 90 tienen su toma elegida.</b> Lo único
que queda es bajarlas: menú «…» → Download → MP3 Audio, y guardarlas en
<code>songs/audio/</code> como <code>en-starters-NN-cancion.mp3</code> o
<code>-chant.mp3</code>. El código corto es el id de la toma marcada, para no
descargar la otra por error. El cupo de la cuenta ronda las 27 por ciclo, así que
las tandas son de 25. Lo que marques se guarda en este navegador.</p>
<div class="barra"><b id="cuenta"></b> &nbsp;·&nbsp; tandas de {POR_TANDA} piezas
 &nbsp;·&nbsp; <button id="limpiar">desmarcar todo</button></div>
{''.join(f'<div class="tanda">Tanda {t}</div>' + ''.join(f for f in filas[(t-1)*POR_TANDA:t*POR_TANDA]) for t in range(1, (len(filas)+POR_TANDA-1)//POR_TANDA + 1))}
</div>
<script>
 const K='suno_starters_hechas';
 const guardado=new Set(JSON.parse(localStorage.getItem(K)||'[]'));
 document.querySelectorAll('.pieza').forEach(p=>{{
   const cb=p.querySelector('input');
   if(guardado.has(p.dataset.id)){{ cb.checked=true; p.classList.add('hecha'); }}
   cb.onchange=()=>{{
     p.classList.toggle('hecha', cb.checked);
     cb.checked ? guardado.add(p.dataset.id) : guardado.delete(p.dataset.id);
     localStorage.setItem(K, JSON.stringify([...guardado]));
     cuenta();
   }};
 }});
 document.querySelectorAll('.cp').forEach(b=>{{
   b.onclick=e=>{{ e.preventDefault();
     navigator.clipboard.writeText(document.getElementById(b.dataset.t).textContent);
     const t=b.textContent; b.textContent='copiado'; setTimeout(()=>b.textContent=t,900); }};
 }});
 function cuenta(){{
   const n=document.querySelectorAll('.pieza.hecha').length;
   const tot=document.querySelectorAll('.pieza').length;
   document.getElementById('cuenta').textContent=n+' de '+tot+' hechas';
 }}
 document.getElementById('limpiar').onclick=()=>{{
   guardado.clear(); localStorage.setItem(K,'[]');
   document.querySelectorAll('.pieza').forEach(p=>{{p.classList.remove('hecha');p.querySelector('input').checked=false;}});
   cuenta();
 }};
 cuenta();
</script></body></html>'''

destino = os.path.join(AQUI, 'tandas.html')
io.open(destino, 'w', encoding='utf-8', newline='').write(html)
print(f'{len(piezas)} piezas ({sum(1 for p in piezas if p["hecha"])} ya hechas) '
      f'en {(len(piezas)+POR_TANDA-1)//POR_TANDA} tandas de {POR_TANDA}')
print('->', destino)
