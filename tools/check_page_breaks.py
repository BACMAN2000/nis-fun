# -*- coding: utf-8 -*-
"""Detecta actividades partidas entre dos paginas de los PDF.

Una actividad empieza con su letra (A, B, C...) seguida del titulo. Si el
encabezado sale en una pagina y el cuerpo continua en la siguiente, el
alumno se encuentra el crucigrama cortado. Este script busca dos senales:

  1. Paginas que ACABAN con un encabezado de actividad y poco mas debajo
     (el titulo quedo huerfano al pie).
  2. Paginas que EMPIEZAN sin encabezado, cuando la anterior tenia una
     actividad abierta (el cuerpo se fue solo a la hoja siguiente).

    python tools/check_page_breaks.py
"""
import os, re, sys
from pypdf import PdfReader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBROS = ["FunForNordic1-SB", "FunForNordic2-SB", "FunForNordic3-SB",
          "FunForNordic1-WB", "FunForNordic2-WB", "FunForNordic3-WB"]

# "A Read the sentences..." al principio de linea
CABECERA = re.compile(r"^([A-G])\s+([A-Z][^\n]{4,60})$", re.M)
UNIDAD = re.compile(r"^\s*(\d{1,2})\s*$", re.M)
# el arranque de unidad sale como "1 Colours and toys"
INICIO_UNIDAD = re.compile(r"^\s*\d{1,2}\s+\S")


def revisa(nombre):
    ruta = os.path.join(ROOT, "book-builder", nombre + ".pdf")
    if not os.path.exists(ruta):
        return None
    r = PdfReader(ruta)
    partidas = []
    for i, pag in enumerate(r.pages):
        txt = (pag.extract_text() or "")
        lineas = [l.rstrip() for l in txt.splitlines() if l.strip()]
        if not lineas:
            continue
        # senal 1: la pagina termina justo en un encabezado de actividad
        cola = "\n".join(lineas[-3:])
        m = CABECERA.search(cola)
        if m and lineas[-1].startswith(m.group(1) + " "):
            partidas.append((i + 1, "titulo huerfano al pie: %s %s"
                             % (m.group(1), m.group(2)[:40])))

        # senal 2: la hoja empieza por el medio de algo. Cada pagina tiene
        # que arrancar en un sitio reconocible — una actividad, el numero de
        # la unidad, las picture words o los cierres. Si no, lo de arriba
        # viene cortado de la hoja anterior.
        if i == 0:
            continue                       # la portada no cuenta
        arranque = lineas[0].strip()
        bien = (CABECERA.match(arranque) or UNIDAD.match(arranque)
                or INICIO_UNIDAD.match(arranque)
                or arranque.startswith(("Picture words", "All about me", "Wordlist",
                                        "The story of this unit", "NORDIC",
                                        "Fun for Nordic", "Across", "Down"))
                or re.match(r"^[A-G]\s", arranque))
        if not bien:
            partidas.append((i + 1, "arranca por el medio: %s" % arranque[:52]))
    return len(r.pages), partidas


if __name__ == "__main__":
    total = 0
    for n in LIBROS:
        res = revisa(n)
        if res is None:
            print("  %-28s (no existe)" % n); continue
        pags, partidas = res
        total += len(partidas)
        estado = "OK" if not partidas else "%d sospechosas" % len(partidas)
        print("  %-28s %3d pags  %s" % (n, pags, estado))
        for p, motivo in partidas[:8]:
            print("        pag %3d  %s" % (p, motivo))
    print("\n%d avisos en total" % total)
