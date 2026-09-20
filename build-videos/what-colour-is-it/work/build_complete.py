from pathlib import Path
import json,re,subprocess
root=Path(__file__).resolve().parent.parent
w=root/'work'; out=root/'outputs'
words=json.loads((w/'what-colour-is-it-original.transcript.json').read_text())[0]['words']
# Phrase groups: question, question, repeated colour, object sentence.
groups=[]
for base in (0,14,28,42):
    for a,b in [(0,4),(4,8),(8,10),(10,14)]: groups.append(words[base+a:base+b])
groups += [words[56:60],words[60:64],words[64:68],words[68:72]]
colours={'red':'6060FF','yellow':'40E8FF','blue':'FFBF66','green':'83EF80'}
def stamp(t):
    cs=round(t*100); return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
def srtstamp(t):
    ms=round(t*1000); return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,46,&H00FFFFFF,&H00FFFFFF,&H00201810,&H90000000,-1,0,0,0,100,100,0,0,1,3,1,2,35,35,30,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
lines=[]; srts=[]
for i,g in enumerate(groups):
    start=g[0]['start']; end=min(g[-1]['end']+.12,groups[i+1][0]['start'] if i+1<len(groups) else 28.8)
    plain=' '.join(x['word'].strip() for x in g).replace('color','colour').replace(',','!').replace('.','!')
    if i in (16,17): plain=plain.replace('!',',').rstrip(',')+'!'
    # Highlight colour words and keep every word on one short readable line.
    decorated=re.sub(r'\b(red|yellow|blue|green)\b',lambda m:'{\\c&H'+colours[m.group().lower()]+'&}'+m.group()+'{\\c&HFFFFFF&}',plain,flags=re.I)
    lines.append(f'Dialogue: 0,{stamp(start)},{stamp(end)},Default,,0,0,0,,{decorated}')
    srts.append(f'{i+1}\n{srtstamp(start)} --> {srtstamp(end)}\n{plain}\n')
(w/'colour-complete.ass').write_text(header+'\n'.join(lines),encoding='utf-8')
(out/'What-Colour-Is-It-subtitulos.srt').write_text('\n'.join(srts),encoding='utf-8')
print('\n'.join(srts))
# Render all four verses to the unchanged original audio timeline.
source=w/'colour-four-generated.mp4'; finale=w/'colour-finale-generated.mp4'
segments=[(source,0,7.1,5.125),(source,10,17.2,5.0),(source,20,24.9,5.0),(source,25.05,29.95,5.10),(finale,20,29.95,8.695)]
parts=[]
for i,(src,a,b,duration) in enumerate(segments):
    dest=w/f'complete-part-{i}.mp4'; parts.append(dest)
    subprocess.run(['ffmpeg','-y','-v','error','-ss',str(a),'-t',str(b-a),'-i',str(src),'-an','-vf',f'setpts={(duration/(b-a)):.9f}*(PTS-STARTPTS),fps=24,tpad=stop_mode=clone:stop_duration=0.1','-t',str(duration),'-c:v','libx264','-preset','fast','-crf','18',str(dest)],check=True)
(w/'complete-concat.txt').write_text('\n'.join("file '"+p.name+"'" for p in parts))
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(w/'complete-concat.txt'),'-i',str(w/'what-colour-is-it-original.mp3'),'-vf','drawbox=x=0:y=610:w=1280:h=110:color=0x122436@0.78:t=fill,ass=work/colour-complete.ass','-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','18','-c:a','aac','-b:a','256k','-t','28.92','-movflags','+faststart',str(out/'What-Colour-Is-It-completa-ritmo-original.mp4')],check=True)
