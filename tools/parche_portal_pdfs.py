# -*- coding: utf-8 -*-
"""Enlaza los libros franceses desde el portal.

Los nueve PDF estaban en el servidor pero no los enlazaba nadie: habia que
saberse la URL. Se enlazan en los tres sitios donde tienen sentido:

  * la pestana de cada nivel (profesor y admin): los tres libros de ese
    nivel, corregido incluido;
  * el hub de Francais: los nueve juntos, para imprimir de una vez;
  * la tarjeta del alumno de primaria: SOLO el libro y el cuaderno. El
    corregido lleva las respuestas.

Los enlaces se arman en una sola funcion, `frLibros(nivel, conClave)`, para
que el dia que cambie el nombre de un archivo no haya que buscarlo en tres
plantillas.
"""
import io, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

P = r"C:\Projects\nis-portal\app.js"

# --- la funcion nueva, justo antes de funFrCursoBody --------------------
ANCLA = "function funFrCursoBody(nivel){"

NUEVA = '''/* Los libros en PDF de un nivel frances.
 *
 * Los tres se generan del mismo contenido que ve el alumno en pantalla
 * (book-builder/book.html?lang=fr), asi que dicen exactamente lo mismo.
 * `conClave` en false deja fuera el corregido: al alumno no se le dan las
 * respuestas.
 */
const FR_LIBROS_N = { starters: 1, movers: 2, flyers: 3 };
function frLibros(nivel, conClave){
  const n = FR_LIBROS_N[nivel];
  if (!n) return '';
  const libro = (suf, em, txt) =>
    `<a class="btn" target="_blank" rel="noopener" download
        href="nis-fun/book-builder/FunForNordic${n}-FR-${suf}.pdf"
        style="background:#fff;border:1px solid var(--line);color:var(--ink);text-decoration:none">${em} ${txt}</a>`;
  return libro('SB', '\\u{1F4D8}', "Livre de l'\\u00e9l\\u00e8ve")
       + libro('WB', '\\u{1F4DD}', "Cahier d'exercices")
       + (conClave ? libro('TeachersKey', '\\u{1F511}', 'Corrig\\u00e9 du professeur') : '');
}

'''

# --- la pestana del nivel ------------------------------------------------
VIEJO_NIVEL = """    <a class="btn" href="${url}" target="_blank" rel="noopener" style="background:${c.color};text-decoration:none">${c.em} Abrir en pantalla completa \\u2197</a>
  </div>"""
NUEVO_NIVEL = """    <a class="btn" href="${url}" target="_blank" rel="noopener" style="background:${c.color};text-decoration:none">${c.em} Abrir en pantalla completa \\u2197</a>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:12px">
    <span class="muted" style="font-size:.85rem">Para imprimir:</span>${frLibros(nivel, true)}
  </div>"""

# --- el hub de Francais --------------------------------------------------
VIEJO_HUB = """    <div class="grid cols-3">
      ${tarjeta('starters','frstarters')}${tarjeta('movers','frmovers')}${tarjeta('flyers','frflyers')}
    </div>"""
NUEVO_HUB = """    <div class="grid cols-3">
      ${tarjeta('starters','frstarters')}${tarjeta('movers','frmovers')}${tarjeta('flyers','frflyers')}
    </div>
    <div class="card" style="margin-top:16px">
      <h2 style="margin:0 0 4px;color:var(--blue-d)">\\u{1F4DA} Los libros en PDF</h2>
      <div class="muted" style="font-size:.88rem;margin-bottom:12px">Los mismos tres libros de cada nivel que en
        ingl\\u00e9s, con la misma maqueta y los mismos dibujos. Salen del mismo contenido que el curso en pantalla,
        as\\u00ed que dicen exactamente lo mismo.</div>
      ${['starters','movers','flyers'].map(n => `<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:10px">
        <span style="min-width:150px;font-weight:600;color:${FUN_FR[n].color}">${FUN_FR[n].em} ${FUN_FR[n].curso}</span>
        ${frLibros(n, true)}</div>`).join('')}
    </div>"""

# --- la tarjeta del alumno -----------------------------------------------
VIEJO_ALUMNO = """      <div style="display:flex;gap:10px;flex-wrap:wrap">${botones}</div></div>`;"""
NUEVO_ALUMNO = """      <div style="display:flex;gap:10px;flex-wrap:wrap">${botones}</div>
      <div class="muted" style="font-size:.85rem;margin:14px 0 6px">\\u{1F4DA} Tes livres \\u00e0 imprimer :</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">${
        ['starters','movers','flyers'].filter(n => (idx[n]||0) > 0).map(n => frLibros(n, false)).join('')
      }</div></div>`;"""


def main():
    s = io.open(P, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")

    if "function frLibros(" not in t:
        if t.count(ANCLA) != 1:
            print("ANCLA FALLA: funFrCursoBody (%d)" % t.count(ANCLA))
            return 1
        t = t.replace(ANCLA, NUEVA + ANCLA)

    for v, n in ((VIEJO_NIVEL, NUEVO_NIVEL), (VIEJO_HUB, NUEVO_HUB),
                 (VIEJO_ALUMNO, NUEVO_ALUMNO)):
        if n in t:
            continue
        if t.count(v) != 1:
            print("ANCLA FALLA (%d): %r" % (t.count(v), v[:70]))
            return 1
        t = t.replace(v, n)

    io.open(P, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)
    print("app.js: los libros enlazados en los tres sitios")
    return 0


if __name__ == "__main__":
    sys.exit(main())
