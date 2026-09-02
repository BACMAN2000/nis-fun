# -*- coding: utf-8 -*-
"""Los rotulos fijos del lector, traducidos en un solo sitio.

Igual que el splash del motor: la pagina tiene que decir algo antes de que
corra nada, asi que su texto va escrito en el HTML. Se reescribe al
arrancar; lo que cambia aqui es que se hace con T() y para los dos idiomas,
en vez de un if para el frances que dejaba el ingles sin pasar por ningun
sitio.
"""
import io, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

P = r"C:\Projects\nis-portal\nis-fun\readers\index.html"

VIEJO = (
    "if (LANG === 'fr'){\n"
    "  document.documentElement.lang = 'fr';\n"
    "  document.title = 'Petits Lecteurs Nordic';\n"
    "  document.getElementById('tit').textContent = 'Petits Lecteurs Nordic';\n"
    "  document.getElementById('volver').textContent = '\\u2039 La biblioth\u00e8que';\n"
    "  document.getElementById('home').textContent = 'Accueil \\u203a';\n"
    "  app.innerHTML = '<p class=\"muted\">Chargement\u2026</p>';\n"
    "}\n"
    "document.getElementById('volver').href = LANG === 'fr' ? './?lang=fr' : './';"
)

NUEVO = (
    "/* Los rotulos que van escritos en el HTML, para que la pagina diga algo\n"
    "   antes de que corra nada. Se reescriben aqui los cinco juntos: asi se\n"
    "   traducen en un solo sitio y la auditoria los ve pasar por T(). */\n"
    "document.documentElement.lang = LANG;\n"
    "document.title = T('Nordic Little Readers', 'Petits Lecteurs Nordic');\n"
    "document.getElementById('tit').textContent = T('Nordic Little Readers', 'Petits Lecteurs Nordic');\n"
    "document.getElementById('volver').textContent = T('\u2039 Bookshelf', '\u2039 La biblioth\u00e8que');\n"
    "document.getElementById('home').textContent = T('Home \u203a', 'Accueil \u203a');\n"
    "app.innerHTML = `<p class=\"muted\">${T('Loading\u2026', 'Chargement\u2026')}</p>`;\n"
    "document.getElementById('volver').href = LANG === 'fr' ? './?lang=fr' : './';"
)

s = io.open(P, encoding="utf-8", newline="").read()
crlf = "\r\n" in s
t = s.replace("\r\n", "\n")
if NUEVO not in t:
    if t.count(VIEJO) != 1:
        print("ANCLA FALLA (%d)" % t.count(VIEJO))
        sys.exit(1)
    t = t.replace(VIEJO, NUEVO)
io.open(P, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)
print("lector: rotulos fijos traducidos en un solo sitio")
