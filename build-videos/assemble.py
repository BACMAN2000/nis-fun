# -*- coding: utf-8 -*-
"""Ensambla el video final de un nivel a partir de 2 clips de dúo Veo.
Uso: python assemble.py <clip1> <clip2> <salida.mp4>
Concatena con crossfade de 0.4 s (video xfade + audio acrossfade), 1080p."""
import subprocess, json, sys

def dur(p):
    r = subprocess.run(['ffprobe','-v','quiet','-print_format','json','-show_format',p],
                       capture_output=True, text=True)
    return float(json.loads(r.stdout)['format']['duration'])

c1, c2, out = sys.argv[1], sys.argv[2], sys.argv[3]
d1 = dur(c1)
XF = 0.4
off = d1 - XF
f = (
    f"[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v0];"
    f"[1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v1];"
    f"[v0][v1]xfade=transition=fade:duration={XF}:offset={off}[vout];"
    f"[0:a]aresample=44100[a0];[1:a]aresample=44100[a1];"
    f"[a0][a1]acrossfade=d={XF}[aout]"
)
cmd = ['ffmpeg','-y','-v','error','-i',c1,'-i',c2,'-filter_complex',f,
       '-map','[vout]','-map','[aout]','-c:v','libx264','-pix_fmt','yuv420p',
       '-preset','medium','-crf','19','-c:a','aac','-b:a','160k',out]
r = subprocess.run(cmd, capture_output=True, text=True)
print('OK' if r.returncode==0 else 'ERROR:\n'+r.stderr[-800:], out)
