# -*- coding: utf-8 -*-
"""Mete el panel de unidades por grado en el portal.

Tres cosas:
  1. el panel (panel_fun_access.js) antes de funLibros;
  2. la entrada de menu y el enrutado, en admin y en profesor;
  3. la tarjeta del alumno solo ofrece los niveles que su grado puede abrir.
"""
import io, os, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

P = r"C:\Projects\nis-portal\app.js"
PANEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "panel_fun_access.js")

ANCLA_PANEL = "/* Los libros en PDF de un nivel, en el idioma que sea."

# --- menu y enrutado -----------------------------------------------------
CAMBIOS = [
    # admin: en Ensenanza, pegado a los cursos que gobierna
    ("""      {key:'fr',label:'🇫🇷 Français'},
      {key:'materiales',label:'📄 Materiales de clase'},""",
     """      {key:'fr',label:'🇫🇷 Français'},
      {key:'funaccess',label:'🔐 Unidades por grado'},
      {key:'materiales',label:'📄 Materiales de clase'},"""),

    ("""  if(tab==='funyle') return $('#main').innerHTML = funYleBody('renderAdmin');""",
     """  if(tab==='funaccess') return funAccessPanel(GRADES);
  if(tab==='funyle') return $('#main').innerHTML = funYleBody('renderAdmin');"""),

    # profesor: mismo sitio, y solo con sus grados
    ("""  ensenanza.push({key:'fr',label:'🇫🇷 Français'});""",
     """  ensenanza.push({key:'fr',label:'🇫🇷 Français'});
  if(teacherAllowedGrades().length) ensenanza.push({key:'funaccess',label:'🔐 Unidades por grado'});"""),

    ("""  if(active==='funyle') return $('#main').innerHTML = funYleBody('renderTeacher');""",
     """  if(active==='funaccess') return funAccessPanel(teacherAllowedGrades());
  if(active==='funyle') return $('#main').innerHTML = funYleBody('renderTeacher');"""),
]


def main():
    s = io.open(P, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")

    if "function funAccessPanel(" not in t:
        panel = io.open(PANEL, encoding="utf-8", newline="").read().replace("\r\n", "\n")
        if t.count(ANCLA_PANEL) != 1:
            print("ANCLA FALLA: donde meter el panel (%d)" % t.count(ANCLA_PANEL))
            return 1
        t = t.replace(ANCLA_PANEL, panel.strip() + "\n\n" + ANCLA_PANEL)

    n = 0
    for v, x in CAMBIOS:
        if x in t:
            continue
        if t.count(v) != 1:
            print("ANCLA FALLA (%d): %r" % (t.count(v), v[:70]))
            return 1
        t = t.replace(v, x)
        n += 1

    io.open(P, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)
    print("app.js: panel + %d enganches de menu" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
