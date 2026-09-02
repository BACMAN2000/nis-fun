# -*- coding: utf-8 -*-
"""El curso respeta lo que el profesor autorizo por grado.

Dos sitios:
  * el hub: la unidad fuera del rango sale con candado y no se puede clicar.
    NO se esconde: el alumno tiene que ver a donde va a llegar, y esconderla
    haria pensar que el curso son ocho unidades. Es la misma decision que ya
    tomo el portal en "Activar unidades".
  * la unidad: si alguien escribe el numero en la URL, no se abre.

Si no hay sesion, no hay red, o el idioma no tiene reglas escritas, NO se
cierra nada. Un candado que aparece porque fallo una consulta es peor que no
tener candado: el alumno se queda fuera de su clase sin que nadie sepa por
que.
"""
import io, os, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

E = r"C:\Projects\nis-portal\nis-fun\engine"

# --- backend.js: preguntar que le toca a este alumno --------------------
BK_ANCLA = "  /* ---- respuestas escritas y repaso final ---- */"

BK_NUEVO = '''  /* ---- que unidades puede abrir este alumno ----
   *
   * Lo decide el profesor en el portal (tabla fun_access, una fila por
   * grado e idioma). Devuelve null cuando NO hay que cerrar nada: sin
   * sesion, sin red, o cuando ese idioma no tiene ninguna regla escrita.
   * Null es "abierto" a proposito — un candado por un fallo de red deja al
   * alumno fuera de su clase sin que nadie sepa por que.
   */
  let _permiso;
  async function permiso() {
    if (_permiso !== undefined) return _permiso;
    _permiso = null;
    await arranca();
    if (!sb || !alumno) return _permiso;
    try {
      const lang = window.LANG === 'fr' ? 'fr' : 'en';
      const { data: filas } = await sb.from('fun_access')
        .select('grade_id,level,desde,hasta,unlocked').eq('lang', lang);
      if (!filas || !filas.length) return _permiso;     // idioma sin reglas
      const { data: perfil } = await sb.from('profiles')
        .select('grade_id').eq('id', alumno.id).maybeSingle();
      const grado = perfil && perfil.grade_id;
      if (!grado) return _permiso;
      const mia = filas.find(f => f.grade_id === grado && f.unlocked &&
                                  f.level === (window.LEVEL_ACTUAL || ''));
      _permiso = mia ? { desde: mia.desde, hasta: mia.hasta }
                     : { desde: 0, hasta: -1 };          // su grado no hace este nivel
    } catch (e) { _permiso = null; }
    return _permiso;
  }

  function puedeAbrir(p, n) {
    return !p || (n >= p.desde && n <= p.hasta);
  }

  /* ---- respuestas escritas y repaso final ---- */'''

BK_EXPORTA = [
    ("""  return { arranca, hayAlumno, guardar, progreso, subirAudio,
           alumno: () => alumno };""",
     """  return { arranca, hayAlumno, guardar, progreso, subirAudio,
           permiso, puedeAbrir, alumno: () => alumno };"""),
]

# --- index.html --------------------------------------------------------
IDX = [
    # el nivel que se esta mirando, para que backend.js sepa cual es
    ("""const LPFX = LANG === 'fr' ? 'nisfun-fr' : 'nisfun';""",
     """const LPFX = LANG === 'fr' ? 'nisfun-fr' : 'nisfun';
window.LEVEL_ACTUAL = LEVEL;   // backend.js lo necesita para leer fun_access"""),

    # el hub: candado en lo que no toca
    ("""  const tarjeta = u => {
    const p = store.get(u.n);
    const hechas = Math.min(4, p.done ? Object.keys(p.done).length : 0);
    const pct = hechas * 25;
    return `<a class="ucard" href="${Q(`?level=${LEVEL}&unit=${u.n}`)}">""",
     """  const tarjeta = u => {
    const p = store.get(u.n);
    const hechas = Math.min(4, p.done ? Object.keys(p.done).length : 0);
    const pct = hechas * 25;
    /* Cerrada: se ve, pero no se abre. Esconderla haria pensar que el curso
       son doce unidades; asi el alumno sabe a donde va a llegar. */
    if (!window.BACKEND || !BACKEND.puedeAbrir(PERMISO, u.n))
      return `<span class="ucard cerrada" aria-disabled="true"
        title="${T('Your teacher opens this one later.','Ton professeur ouvrira celle-ci plus tard.')}">
      <span class="n">${u.n}</span> <b>${u.title}</b><br>
      <small>${u.topic}</small><br>
      <span class="candado" aria-hidden="true">🔒</span>
      <span class="sr-only">${T('Locked','Fermée')}</span></span>`;
    return `<a class="ucard" href="${Q(`?level=${LEVEL}&unit=${u.n}`)}">"""),

    # el estilo del candado
    ("""  a.ucard:hover{border-color:var(--accent)}""",
     """  a.ucard:hover{border-color:var(--accent)}
  /* La unidad que el profesor no ha abierto todavia: se ve entera, apagada
     y sin enlace. No se esconde a proposito. */
  .ucard.cerrada{display:block;background:var(--surface2);border:1px dashed var(--line);
    border-radius:14px;padding:1rem 1.2rem;color:var(--soft);opacity:.7;cursor:not-allowed}
  .ucard.cerrada .n{font-family:"Baloo 2";font-weight:800;font-size:1.3rem;color:var(--soft)}
  .ucard.cerrada .candado{font-size:1.05rem}"""),
]


def parchea(ruta, cambios):
    s = io.open(ruta, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")
    n = 0
    for v, x in cambios:
        if x in t:
            continue
        if t.count(v) != 1:
            print("ANCLA FALLA en %s (%d): %r"
                  % (os.path.basename(ruta), t.count(v), v[:70]))
            return None
        t = t.replace(v, x)
        n += 1
    io.open(ruta, "w", encoding="utf-8",
            newline="\r\n" if crlf else "\n").write(t)
    return n


def main():
    r = parchea(os.path.join(E, "backend.js"),
                [(BK_ANCLA, BK_NUEVO)] + BK_EXPORTA)
    if r is None:
        return 1
    print("  backend.js: %d" % r)
    r = parchea(os.path.join(E, "index.html"), IDX)
    if r is None:
        return 1
    print("  index.html: %d" % r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
