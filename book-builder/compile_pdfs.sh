#!/bin/bash
# Recompila los PDFs (SB/WB/Key x 3 niveles) desde book.html.
#
#   ./compile_pdfs.sh          los 9 ingleses
#   ./compile_pdfs.sh fr       los 9 franceses (FunForNordicN-FR-*.pdf)
#   ./compile_pdfs.sh todo     los 18
#
# book.html carga los JSON con fetch, asi que necesita servidor: file:// lo
# bloquea por CORS. Edge tiene que ser --headless CLASICO (con --headless=new
# sale exit 0 sin escribir el PDF) y cada impresion necesita su propio
# --user-data-dir: reutilizar el perfil con un proceso colgado da el mismo
# fallo silencioso. La escritura es asincrona, de ahi la espera al final.
set -u
PORT=9350
ROOT="/c/Projects/nis-fun"
OUT="$ROOT/book-builder"
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
TMP=$(mktemp -d)
IDIOMAS="${1:-en}"
[ "$IDIOMAS" = "todo" ] && IDIOMAS="en fr"

python -m http.server $PORT --directory "$(cygpath -w "$ROOT")" >/dev/null 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null; rm -rf "$TMP"' EXIT
sleep 2

declare -A NAME=( [starters]=1 [movers]=2 [flyers]=3 )
declare -A SUF=( [sb]=SB [wb]=WB [key]=TeachersKey )

for lang in $IDIOMAS; do
  # El frances lleva -FR en el nombre para que los 18 convivan en la carpeta
  # y en el repo; el ingles conserva el nombre de siempre.
  if [ "$lang" = "fr" ]; then MARCA="-FR"; ARG="&lang=fr"; else MARCA=""; ARG=""; fi
  for lvl in starters movers flyers; do
    for mode in sb wb key; do
      f="$OUT/FunForNordic${NAME[$lvl]}${MARCA}-${SUF[$mode]}.pdf"
      printf "%-36s " "$(basename "$f")"
      rm -f "$f"
      "$EDGE" --headless --disable-gpu --no-sandbox \
        --user-data-dir="$TMP/p-$lang-$lvl-$mode" \
        --print-to-pdf="$(cygpath -w "$f")" --print-to-pdf-no-header \
        --virtual-time-budget=90000 \
        "http://localhost:$PORT/book-builder/book.html?level=$lvl&mode=$mode$ARG" \
        >/dev/null 2>&1
      for i in $(seq 1 30); do [ -s "$f" ] && break; sleep 1; done
      if [ -s "$f" ]; then
        printf "%7.1f MB  %s pp\n" \
          "$(python -c "import os;print(os.path.getsize(r'$(cygpath -w "$f")')/1048576)")" \
          "$(python -c "
try:
    from pypdf import PdfReader
    print(len(PdfReader(r'$(cygpath -w "$f")').pages))
except Exception:
    print('?')" 2>/dev/null)"
      else
        echo "FALLO"
      fi
    done
  done
done
