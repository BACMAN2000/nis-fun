from pathlib import Path
import subprocess
# "Red ball, yellow kite! Blue train, green car!": one cut per toy, each on its sung name,
# instead of the gathering shot that showed the toys in the opposite order.
w=Path('work'); out=Path('outputs')
def run(args): subprocess.run(['ffmpeg','-y','-v','error',*args],check=True)
cuts=[('colour-finale-generated.mp4',4.40,0.775),   # red ball, Nico points at it      20.225-21.00
      ('colour-finale-generated.mp4',12.50,0.68),   # yellow kite held up               21.00-21.68
      ('colour-four-generated.mp4',21.40,0.62),     # blue train in Freya's hands       21.68-22.30
      ('green-v2-generated.mp4',1.90,1.20)]         # green car held up by Nico         22.30-23.50
names=[]
for i,(src,a,d) in enumerate(cuts):
    dest=w/f'recap-{i}.mp4'; names.append(dest.name)
    run(['-ss',str(a),'-t',str(d),'-i',str(w/src),'-an','-vf','setpts=PTS-STARTPTS,fps=24,scale=1280:720','-t',str(d),'-c:v','libx264','-preset','fast','-crf','18',str(dest)])
(w/'final-v3-concat.txt').write_text('\n'.join("file '"+n+"'" for n in ['complete-part-0.mp4','complete-part-1.mp4','complete-part-2.mp4','complete-part-3-v2.mp4',*names,'closing-aligned.mp4'])+'\n')
run(['-f','concat','-safe','0','-i',str(w/'final-v3-concat.txt'),'-i',str(w/'what-colour-is-it-original.mp3'),'-vf',"drawbox=x=0:y=610:w=1280:h=110:color=0x122436@0.78:t=fill:enable='lt(t,15.125)',drawbox=x=0:y=0:w=1280:h=92:color=0x122436@0.78:t=fill:enable='gte(t,15.125)',ass=work/colour-final-v2.ass,fade=t=out:st=29.05:d=0.25",'-af','apad','-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','256k','-t','29.30','-movflags','+faststart',str(out/'What-Colour-Is-It-final.mp4')])
print('ok')
