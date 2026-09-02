# -*- coding: utf-8 -*-
"""Quita del auditor el ruido de codigo y arregla la consola de Windows.

El barrido de ">texto<" tambien pilla los "<" de un for(let c=0;c<n), y la
lista salia con medio JavaScript dentro. Un rotulo no tiene punto y coma,
ni parentesis, ni acentos graves: con eso basta para separarlos.
"""
import io

P = r"C:\Projects\nis-fun\tools\fr_motor.py"
s = io.open(P, encoding="utf-8").read()

VIEJO = """import io, os, re, sys
"""
NUEVO = """import io, os, re, sys

# La consola de Windows es cp1252 y se atraganta con los emojis del motor.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
"""
assert s.count(VIEJO) == 1
s = s.replace(VIEJO, NUEVO)

VIEJO2 = '''# Nombres propios y marcas: se escriben igual en los dos idiomas.'''
NUEVO2 = '''# Codigo, no rotulo. Una frase de interfaz no lleva punto y coma, ni
# parentesis, ni acentos graves; el barrido de ">texto<" si pilla el "<" de
# un for(let c=0;c<n) y hay que descartarlo.
CODIGO = re.compile(r"[`;={}()\\[\\]$|\\\\+*<>]|=>|\\bfunction\\b|\\breturn\\b")

# Nombres propios y marcas: se escriben igual en los dos idiomas.'''
assert s.count(VIEJO2) == 1
s = s.replace(VIEJO2, NUEVO2)

VIEJO3 = """        if t and t not in ya and t not in MARCAS and FRASE.search(t) \\
                and not NO_ES_TEXTO.match(t):
            fuera.add(t)"""
NUEVO3 = """        if t and t not in ya and t not in MARCAS and FRASE.search(t) \\
                and not NO_ES_TEXTO.match(t) and not CODIGO.search(t):
            fuera.add(t)"""
assert s.count(VIEJO3) == 1
s = s.replace(VIEJO3, NUEVO3)

VIEJO4 = """            if t and t not in ya and t not in MARCAS and PROSA.match(t) \\
                    and not NO_ES_TEXTO.match(t):
                fuera.add(t)"""
NUEVO4 = """            if t and t not in ya and t not in MARCAS and PROSA.match(t) \\
                    and not NO_ES_TEXTO.match(t) and not CODIGO.search(t):
                fuera.add(t)"""
assert s.count(VIEJO4) == 1
s = s.replace(VIEJO4, NUEVO4)

io.open(P, "w", encoding="utf-8").write(s)
print("auditor del motor: sin ruido de codigo")
