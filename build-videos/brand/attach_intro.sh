#!/bin/bash
# Envuelve cada video de elenco/mascota con la marca Nordic:
#   bumper de entrada  ->  video  ->  cierre con el logo completo
# El cierre NO se funde a blanco: el ultimo fotograma es el lockup entero.
set -e
export PATH="$PATH:/c/Users/User/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.2-full_build/bin"

SP="/c/Users/User/AppData/Local/Temp/claude/C--Cohasset-Web/6c4a34eb-b633-4e59-ac35-72cd830109e2/scratchpad"
V="/c/Projects/nis-fun/assets/videos"
OUT="$SP/con-intro"
mkdir -p "$OUT"

XF=0.35
IDUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SP/nordic-intro.mp4")
ODUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SP/nordic-outro.mp4")
echo "entrada ${IDUR}s   cierre ${ODUR}s   cruce ${XF}s"

# versiones para los videos de mascota (1280x720 @ 24 fps)
for p in intro outro; do
  ffmpeg -y -v error -i "$SP/nordic-$p.mp4" \
    -vf "scale=1280:720:flags=lanczos,fps=24" \
    -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p \
    -c:a aac -b:a 192k "$SP/nordic-$p-720p24.mp4"
done

wrap () {                 # $1=video  $2=sufijo de los bumpers ("" o "-720p24")
  local f="$1" sfx="$2"
  local name=$(basename "$f")
  local intro="$SP/nordic-intro$sfx.mp4"
  local outro="$SP/nordic-outro$sfx.mp4"
  local vdur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  local off1=$(python -c "print(round($IDUR - $XF, 4))")
  local off2=$(python -c "print(round($IDUR + $vdur - 2*$XF, 4))")
  local has_a=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$f" | head -1)
  echo "  -> $name  (cruces en ${off1}s y ${off2}s)"

  if [ -n "$has_a" ]; then
    ffmpeg -y -v error -i "$intro" -i "$f" -i "$outro" -filter_complex \
      "[0:v][1:v]xfade=transition=fade:duration=$XF:offset=$off1[v1];\
       [v1][2:v]xfade=transition=fade:duration=$XF:offset=$off2[v];\
       [0:a][1:a]acrossfade=d=$XF[a1];[a1][2:a]acrossfade=d=$XF[a]" \
      -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
      -c:a aac -b:a 192k "$OUT/$name"
  else
    ffmpeg -y -v error -i "$intro" -i "$f" -i "$outro" -filter_complex \
      "[0:v][1:v]xfade=transition=fade:duration=$XF:offset=$off1[v1];\
       [v1][2:v]xfade=transition=fade:duration=$XF:offset=$off2[v];\
       [0:a][2:a]acrossfade=d=$XF[a]" \
      -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
      -c:a aac -b:a 192k "$OUT/$name"
  fi
}

echo "== elenco (1920x1080 @30) =="
for f in starters-cast movers-cast flyers-cast; do
  [ -e "$V/$f.mp4" ] && wrap "$V/$f.mp4" ""
done

echo "== mascotas (1280x720 @24) =="
for f in pip-intro luna-intro kili-intro; do
  [ -e "$V/$f.mp4" ] && wrap "$V/$f.mp4" "-720p24"
done

echo "== resultado =="
for f in "$OUT"/*.mp4; do
  n=$(basename "$f")
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  o=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V/$n")
  printf "%-20s %6.2fs (original %5.2fs)  %s\n" "$n" "$d" "$o" \
    "$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$f")"
done
