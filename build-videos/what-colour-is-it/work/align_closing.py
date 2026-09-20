from pathlib import Path
import subprocess
w=Path('work'); out=Path('outputs')
def run(args): subprocess.run(['ffmpeg','-y','-v','error',*args],check=True)
# Align the generated mouth movements to each original sung word.
source=[.96,1.06,1.82,2,2.30,2.86,3.40,4.16,4.40,4.78,5.66,6.84]
target=[0,.10,.62,1.06,1.56,2.08,2.58,3.10,3.50,3.96,4.62,5.80]
expr='5.8'
for i in range(len(source)-2,-1,-1):
    a,b=source[i:i+2]; c,d=target[i:i+2]
    expr=f'if(lt(PTS*TB,{b}),{c}+(PTS*TB-{a})*{(d-c)/(b-a)},{expr})'
run(['-i',str(w/'closing-sung-final.mp4'),'-an','-vf',f"trim=start=0.96:end=6.84,setpts='{expr}/TB',fps=24,tpad=stop_mode=clone:stop_duration=0.2",'-t','5.8','-c:v','libx264','-crf','18','-preset','fast',str(w/'closing-aligned.mp4')])
(w/'closing-v2-concat.txt').write_text("file 'closing-prefix.mp4'\nfile 'closing-aligned.mp4'\n")
run(['-f','concat','-safe','0','-i',str(w/'closing-v2-concat.txt'),'-i',str(w/'what-colour-is-it-original.mp3'),'-vf',"drawbox=x=0:y=610:w=1280:h=110:color=0x122436@0.78:t=fill:enable='lt(t,20.25)',drawbox=x=0:y=0:w=1280:h=100:color=0x122436@0.78:t=fill:enable='gte(t,20.25)',ass=work/colour-visible-box.ass,fade=t=out:st=29.05:d=0.25",'-af','apad','-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','256k','-t','29.30','-movflags','+faststart',str(out/'What-Colour-Is-It-cierre-corregido.mp4')])

