from pathlib import Path
import subprocess,sys
# Replace the floating-car green verse with the regenerated shot and lift the captions
# above the picture from that verse onward so the band never hides the car or the box.
w=Path('work'); out=Path('outputs')
def run(args): subprocess.run(['ffmpeg','-y','-v','error',*args],check=True)
src=Path(sys.argv[1]); a=float(sys.argv[2]); b=float(sys.argv[3])   # window of the new shot to use
GREEN=5.10                                                          # verse length in the original song
run(['-ss',str(a),'-t',str(b-a),'-i',str(src),'-an','-vf',f'setpts={GREEN/(b-a):.9f}*(PTS-STARTPTS),fps=24,scale=1280:720,tpad=stop_mode=clone:stop_duration=0.1','-t',str(GREEN),'-c:v','libx264','-preset','fast','-crf','18',str(w/'complete-part-3-v2.mp4')])
(w/'green-v2-concat.txt').write_text("file 'complete-part-0.mp4'\nfile 'complete-part-1.mp4'\nfile 'complete-part-2.mp4'\nfile 'complete-part-3-v2.mp4'\nfile 'complete-part-4.mp4'\n")
run(['-f','concat','-safe','0','-i',str(w/'green-v2-concat.txt'),'-an','-t','23.5','-c:v','libx264','-crf','18','-preset','fast',str(w/'closing-prefix-v2.mp4')])
(w/'final-v2-concat.txt').write_text("file 'closing-prefix-v2.mp4'\nfile 'closing-aligned.mp4'\n")
# Captions: bottom band for red/yellow/blue, top band from the green verse (15.125 s) to the end.
ass=w/'colour-final.ass'; lines=[]
for line in ass.read_text(encoding='utf-8').splitlines():
    if line.startswith('Dialogue:'):
        f=line.split(',',9); t=f[1].split(':'); start=int(t[1])*60+float(t[2])
        if start>=15.1 and not f[9].startswith('{\an8'): f[9]='{\an8\pos(640,28)}'+f[9]
        line=','.join(f)
    lines.append(line)
(w/'colour-final-v2.ass').write_text('\n'.join(lines),encoding='utf-8')
run(['-f','concat','-safe','0','-i',str(w/'final-v2-concat.txt'),'-i',str(w/'what-colour-is-it-original.mp3'),'-vf',"drawbox=x=0:y=610:w=1280:h=110:color=0x122436@0.78:t=fill:enable='lt(t,15.125)',drawbox=x=0:y=0:w=1280:h=92:color=0x122436@0.78:t=fill:enable='gte(t,15.125)',ass=work/colour-final-v2.ass,fade=t=out:st=29.05:d=0.25",'-af','apad','-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','256k','-t','29.30','-movflags','+faststart',str(out/'What-Colour-Is-It-final.mp4')])
print('ok')
