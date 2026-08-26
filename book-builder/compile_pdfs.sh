#!/bin/bash
# Recompila los 9 PDFs (SB/WB/Key x 3 niveles) desde book.html.
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

python -m http.server $PORT --directory "$(cygpath -w "$ROOT")" >/dev/null 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null; rm -rf "$TMP"' EXIT
sleep 2

declare -A NAME=( [starters]=1 [movers]=2 [flyers]=3 )
declare -A SUF=( [sb]=SB [wb]=WB [key]=TeachersKey )

for lvl in starters movers flyers; do
  for mode in sb wb key; do
    f="$OUT/FunForNordic${NAME[$lvl]}-${SUF[$mode]}.pdf"
    printf "%-34s " "$(basename "$f")"
    rm -f "$f"
    "$EDGE" --headless --disable-gpu --no-sandbox \
      --user-data-dir="$TMP/p-$lvl-$mode" \
      --print-to-pdf="$(cygpath -w "$f")" --print-to-pdf-no-header \
      --virtual-time-budget=45000 \
      "http://localhost:$PORT/book-builder/book.html?level=$lvl&mode=$mode" \
      >/dev/null 2>&1
    for i in $(seq 1 20); do [ -s "$f" ] && break; sleep 1; done
    if [ -s "$f" ]; then
      printf "%7.1f MB\n" "$(python -c "import os;print(os.path.getsize(r'$(cygpath -w "$f")')/1048576)")"
    else
      echo "FALLO"
    fi
  done
done
