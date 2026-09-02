# -*- coding: utf-8 -*-
"""Enlaza tambien los nueve libros ingleses.

`frLibros` pasa a ser `funLibros(nivel, lang, conClave)`: el mismo boton
para los dos idiomas, que solo cambian el sufijo del archivo y el nombre
del libro. Se enlazan en los mismos tres sitios que los franceses.

El corregido sigue fuera de la vista del alumno en los dos idiomas.
"""
import io, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

P = r"C:\Projects\nis-portal\app.js"

VIEJA = '''/* Los libros en PDF de un nivel frances.
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
    // se abre en una pestana en vez de descargarse: el libro del alumno
    // pesa 24 MB y casi siempre lo que se quiere es mirarlo o imprimirlo
    `<a class="btn" target="_blank" rel="noopener"
        href="nis-fun/book-builder/FunForNordic${n}-FR-${suf}.pdf"
        style="background:#fff;border:1px solid var(--line);color:var(--ink);text-decoration:none">${em} ${txt}</a>`;
  return libro('SB', '\\u{1F4D8}', "Livre de l'\\u00e9l\\u00e8ve")
       + libro('WB', '\\u{1F4DD}', "Cahier d'exercices")
       + (conClave ? libro('TeachersKey', '\\u{1F511}', 'Corrig\\u00e9 du professeur') : '');
}'''

NUEVA = '''/* Los libros en PDF de un nivel, en el idioma que sea.
 *
 * Los tres se generan del mismo contenido que ve el alumno en pantalla
 * (book-builder/book.html, con ?lang=fr para el frances), asi que dicen
 * exactamente lo mismo que el curso. Lo unico que cambia entre idiomas es
 * el sufijo del archivo y el nombre del libro.
 *
 * `conClave` en false deja fuera el corregido: al alumno no se le dan las
 * respuestas, ni en ingles ni en frances.
 */
const FUN_LIBROS_N = { starters: 1, movers: 2, flyers: 3 };
const FUN_LIBROS_TXT = {
  en: { marca: '',    sb: "Student's Book", wb: 'Workbook',           key: "Teacher's Key" },
  fr: { marca: '-FR', sb: "Livre de l'\\u00e9l\\u00e8ve", wb: "Cahier d'exercices",
        key: 'Corrig\\u00e9 du professeur' },
};
function funLibros(nivel, lang, conClave){
  const n = FUN_LIBROS_N[nivel];
  const t = FUN_LIBROS_TXT[lang] || FUN_LIBROS_TXT.en;
  if (!n) return '';
  const libro = (suf, em, txt) =>
    // se abre en una pestana en vez de descargarse: el libro del alumno
    // pesa 24 MB y casi siempre lo que se quiere es mirarlo o imprimirlo
    `<a class="btn" target="_blank" rel="noopener"
        href="nis-fun/book-builder/FunForNordic${n}${t.marca}-${suf}.pdf"
        style="background:#fff;border:1px solid var(--line);color:var(--ink);text-decoration:none">${em} ${txt}</a>`;
  return libro('SB', '\\u{1F4D8}', t.sb)
       + libro('WB', '\\u{1F4DD}', t.wb)
       + (conClave ? libro('TeachersKey', '\\u{1F511}', t.key) : '');
}'''

# --- las llamadas francesas, al nombre nuevo ----------------------------
LLAMADAS = [
    ("${frLibros(nivel, true)}", "${funLibros(nivel, 'fr', true)}"),
    ("${frLibros(n, true)}", "${funLibros(n, 'fr', true)}"),
    (".map(n => frLibros(n, false)).join('')",
     ".map(n => funLibros(n, 'fr', false)).join('')"),
]

# --- ingles: la pestana de cada nivel ------------------------------------
VIEJO_NIVEL = """    <a class="btn" href="${url}" target="_blank" rel="noopener" style="background:${c.color};text-decoration:none">${c.em} Abrir en pantalla completa ↗</a>
  </div>
  <iframe src="${url}" title="${esc(c.curso)}\""""
NUEVO_NIVEL = """    <a class="btn" href="${url}" target="_blank" rel="noopener" style="background:${c.color};text-decoration:none">${c.em} Abrir en pantalla completa ↗</a>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:12px">
    <span class="muted" style="font-size:.85rem">Para imprimir:</span>${funLibros(nivel, 'en', true)}
  </div>
  <iframe src="${url}" title="${esc(c.curso)}\""""

# --- ingles: el hub YLE ---------------------------------------------------
VIEJO_HUB = """    <div class="card" style="margin-top:16px">
      <h2 style="margin:0 0 4px;color:var(--blue-d)">✅ Corregir lo que entregan</h2>"""
NUEVO_HUB = """    <div class="card" style="margin-top:16px">
      <h2 style="margin:0 0 4px;color:var(--blue-d)">📚 Los libros en PDF</h2>
      <div class="muted" style="font-size:.88rem;margin-bottom:12px">El libro del alumno, el cuaderno de casa
        y el corregido de cada nivel. Salen del mismo contenido que el curso en pantalla, así que dicen
        exactamente lo mismo.</div>
      ${['starters','movers','flyers'].map(n => `<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:10px">
        <span style="min-width:150px;font-weight:600;color:${FUN_CURSOS[n].color}">${FUN_CURSOS[n].em} ${FUN_CURSOS[n].curso}</span>
        ${funLibros(n, 'en', true)}</div>`).join('')}
    </div>
    <div class="card" style="margin-top:16px">
      <h2 style="margin:0 0 4px;color:var(--blue-d)">✅ Corregir lo que entregan</h2>"""

# --- ingles: la tarjeta del alumno ---------------------------------------
VIEJO_ALUMNO = """        <a href="${_withBack('nis-fun/engine/?level=flyers','classes_primary')}" target="_blank" rel="noopener" class="btn" style="background:#3b6fb5;color:#fff;text-decoration:none">🦅 A2 · Flyers</a>
      </div>
    </div>` : '';"""
NUEVO_ALUMNO = """        <a href="${_withBack('nis-fun/engine/?level=flyers','classes_primary')}" target="_blank" rel="noopener" class="btn" style="background:#3b6fb5;color:#fff;text-decoration:none">🦅 A2 · Flyers</a>
      </div>
      <div class="muted" style="font-size:.85rem;margin:14px 0 6px">📚 Your books to print:</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">${
        ['starters','movers','flyers'].map(n => funLibros(n, 'en', false)).join('')
      }</div>
    </div>` : '';"""


def main():
    s = io.open(P, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")

    if "function funLibros(" not in t:
        if t.count(VIEJA) != 1:
            print("ANCLA FALLA: frLibros (%d)" % t.count(VIEJA))
            return 1
        t = t.replace(VIEJA, NUEVA)
    for v, n in LLAMADAS:
        t = t.replace(v, n)

    for v, n in ((VIEJO_NIVEL, NUEVO_NIVEL), (VIEJO_HUB, NUEVO_HUB),
                 (VIEJO_ALUMNO, NUEVO_ALUMNO)):
        if n in t:
            continue
        if t.count(v) != 1:
            print("ANCLA FALLA (%d): %r" % (t.count(v), v[:70]))
            return 1
        t = t.replace(v, n)

    if "frLibros" in t:
        print("queda alguna llamada vieja a frLibros")
        return 1
    io.open(P, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)
    print("app.js: los libros de los dos idiomas, con la misma funcion")
    return 0


if __name__ == "__main__":
    sys.exit(main())
