# -*- coding: utf-8 -*-
"""Ensena a la auditoria a no marcar frances como ingles.

"match" y "but" son palabras de los dos idiomas —un match de futbol, marcar
un but— y hacian saltar dos guiones que estan perfectamente en frances.
Quitarlas de la lista no vale: "Match the words" tiene que seguir saltando.

La regla que si funciona es mirar las dos a la vez: una frase con palabras
inglesas y NINGUNA palabra francesa inequivoca es inglesa. Si tiene de las
dos, es francesa con una palabra que se escribe igual.
"""
import io

P = r"C:\Projects\nis-fun\tools\fr_audita.py"
s = io.open(P, encoding="utf-8").read()

VIEJO = '''def ingles(t, minimo=2):
    if not isinstance(t, str) or len(t) < 6:
        return False
    return len(re.findall(DELATORAS, t.lower())) >= minimo'''

NUEVO = '''# Y las de la otra orilla: si aparecen, la frase es francesa aunque lleve una
# palabra que tambien exista en ingles.
FRANCESAS = r"\\b(le|la|les|des|une|un|du|de|et|est|sont|avec|dans|pour|sur|" \\
            r"que|qui|quoi|ton|ta|tes|mon|ma|mes|son|sa|ses|nous|vous|ils|" \\
            r"elle|elles|tu|je|au|aux|chez|tres|tres|oui|non|puis|alors|" \\
            r"ecris|ecoute|regarde|touche|choisis|associe|colorie|dessine|" \\
            r"complete|entoure|coche|relie|trouve|lis|parle)\\b"


def ingles(t, minimo=2):
    if not isinstance(t, str) or len(t) < 6:
        return False
    b = t.lower()
    if len(re.findall(DELATORAS, b)) < minimo:
        return False
    # "Le grand match de la recre" lleva match, pero tambien le, la y de:
    # es frances con una palabra que se escribe igual en los dos idiomas.
    return not re.search(FRANCESAS, b)'''

assert s.count(VIEJO) == 1, "el ancla de ingles() no esta"
io.open(P, "w", encoding="utf-8").write(s.replace(VIEJO, NUEVO))
print("auditoria: ahora mira tambien si la frase es francesa")
