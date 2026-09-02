# -*- coding: utf-8 -*-
"""Traduce lo que el motor pintaba en ingles con ?lang=fr.

Son los rotulos que el primer barrido no vio porque no llevan ninguna
palabra que solo exista en ingles ("Start learning") o porque viven fuera de
index.html (el banner, las pantallas de nivel, la caja magica).

Se parchea por ancla y se comprueba una a una: si alguna no esta, el script
para sin tocar el archivo.
"""
import io, os, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

E = r"C:\Projects\nis-portal\nis-fun\engine"

# (archivo, viejo, nuevo)
CAMBIOS = [
    # ---- index.html ----------------------------------------------------
    ("index.html",
     """    <div><h3>${totalHechas ? `Continue Unit ${siguiente.unit.n}` : 'Start your first unit'}</h3>
      <p>${terminadas} of ${unidades.length} units completed · ${porcentaje}% overall</p></div>""",
     """    <div><h3>${totalHechas ? T(`Continue Unit ${siguiente.unit.n}`, `Continuer l'unité ${siguiente.unit.n}`) : T('Start your first unit','Commence ta première unité')}</h3>
      <p>${T(`${terminadas} of ${unidades.length} units completed · ${porcentaje}% overall`, `${terminadas} unités sur ${unidades.length} terminées · ${porcentaje}% en tout`)}</p></div>"""),

    ("index.html",
     """      ${totalHechas ? 'Continue learning' : 'Start learning'} <span aria-hidden="true">›</span></a>""",
     """      ${totalHechas ? T('Continue learning','Continuer') : T('Start learning','Commencer')} <span aria-hidden="true">›</span></a>"""),

    ("index.html",
     """        <p class="scr-pie">Meet the characters in 3D, then continue with your guide.</p>""",
     """        <p class="scr-pie">${T('Meet the characters in 3D, then continue with your guide.','Rencontre les personnages en 3D, puis continue avec ton guide.')}</p>"""),

    # ---- banner.js -----------------------------------------------------
    ("banner.js",
     """                  aria-label="Play this video with sound">🔊 Play with sound</button>""",
     """                  aria-label="${T('Play this video with sound','Lire la vidéo avec le son')}">🔊 ${T('Play with sound','Activer le son')}</button>"""),

    ("banner.js",
     """      sonido.textContent = activar ? '🔇 Mute' : '🔊 Play with sound';""",
     """      sonido.textContent = activar ? T('🔇 Mute','🔇 Couper le son') : T('🔊 Play with sound','🔊 Activer le son');"""),

    # ---- screens.js ----------------------------------------------------
    ("screens.js",
     """Course content""",
     """${T('Course content','Contenu du cours')}"""),
]


def main():
    # el cargador comun, el primero de todos
    P = os.path.join(E, "index.html")
    s = io.open(P, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")
    ancla = '<script src="crossword-layout.js"></script>'
    if 'i18n.js' not in t:
        if t.count(ancla) != 1:
            print("no encuentro donde meter i18n.js")
            return 1
        t = t.replace(ancla, '<script src="i18n.js?v=1"></script>\n' + ancla)
        # LANG y T ya vienen de i18n.js: aqui solo se reusan
        t = t.replace(
            "const LANG = qs.get('lang') === 'fr' ? 'fr' : 'en';",
            "const LANG = window.LANG;   // lo calcula i18n.js, que carga antes que todos")
        t = t.replace(
            "const T = (en, fr) => (LANG === 'fr' ? fr : en);\nwindow.LANG = LANG;   "
            "// backend.js lo necesita para separar las entregas por idioma",
            "const T = window.T;   // el mismo que usan banner.js, screens.js y magicbox.js")
    io.open(P, "w", encoding="utf-8",
            newline="\r\n" if crlf else "\n").write(t)

    for archivo, viejo, nuevo in CAMBIOS:
        P = os.path.join(E, archivo)
        s = io.open(P, encoding="utf-8", newline="").read()
        crlf = "\r\n" in s
        t = s.replace("\r\n", "\n")
        v, n = viejo.replace("\r\n", "\n"), nuevo.replace("\r\n", "\n")
        if n in t:
            print("  %s: ya estaba" % archivo)
            continue
        if t.count(v) != 1:
            print(f"ANCLA FALLA en {archivo} ({t.count(v)}): {v[:60]!r}")
            return 1
        t = t.replace(v, n)
        io.open(P, "w", encoding="utf-8",
                newline="\r\n" if crlf else "\n").write(t)
        print(f"  {archivo}: {v.strip()[:52]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
