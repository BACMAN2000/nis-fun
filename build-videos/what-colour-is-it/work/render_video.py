from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, subprocess, json, sys

ROOT=Path(__file__).resolve().parent.parent
WORK=ROOT/'work'; OUT=ROOT/'outputs'
W,H,FPS=1280,720,24
INK='#173D4B'; TEAL='#167C80'; CORAL='#EF795F'
def font(n): return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',n)
F={n:font(n) for n in [18,22,26,30,36,42,48,58,72]}
def text(d,xy,s,n=30,fill=INK,anchor='mm'):
    d.text(xy,s,font=F[n],fill=fill,anchor=anchor)
def duration(p):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)]))
SONGS=[('01',"Pip's Toy Box",'COLOURS & TOYS',94.480167),('35','Open the Lunchbox','FOOD & FRIENDSHIP',95.520979),('37','Wiggle and Wave','MOVE & PLAY',115.240167)]
ASSETS={}
for p in WORK.glob('*.png'):
    im=Image.open(p).convert('RGBA'); box=im.getbbox()
    if box: im=im.crop(box)
    ASSETS[p.stem]=im
SPRITES={}
for name in ['pip','freya','nico','astrid','tomas']:
    for pose in [1,2,3]:
        im=ASSETS[f'{name}-{pose}']; h=290 if name=='pip' else 365
        SPRITES[(name,pose)]=im.resize((int(im.width*h/im.height),h),Image.Resampling.LANCZOS)
PROPS={}
for name in ['ball','kite','train','car','teddy','doll']:
    im=ASSETS[name]; im.thumbnail((235,230),Image.Resampling.LANCZOS); PROPS[name]=im

def star(d,x,y,r,c):
    pts=[(x+math.sin(i*math.pi/5)*(r if i%2==0 else r*.43),y-math.cos(i*math.pi/5)*(r if i%2==0 else r*.43)) for i in range(10)]
    d.polygon(pts,fill=c)
def background(ch):
    im=Image.new('RGB',(W,H),['#EAF8F6','#FFF6E6','#EDF1FE'][ch]); d=ImageDraw.Draw(im)
    d.ellipse((-170,340,1450,1400),fill=['#CCE8D5','#E2ECCF','#DDE2F8'][ch])
    d.ellipse((-180,570,1460,1150),fill=['#B4DACE','#F0DEBB','#CAD7EA'][ch])
    # A small lighthouse anchors the school series visually.
    d.polygon([(1160,325),(1178,188),(1211,188),(1232,325)],fill='#FFFBEE')
    d.polygon([(1170,254),(1221,254),(1226,281),(1167,281)],fill=CORAL)
    d.rounded_rectangle((1170,174,1218,202),8,fill=TEAL)
    d.polygon([(1163,177),(1194,153),(1225,177)],fill=CORAL)
    d.rectangle((1183,180,1191,195),fill='#FFF1A2');d.rectangle((1197,180,1206,195),fill='#FFF1A2')
    d.ellipse((54,225,152,323),fill='#FFE5A4')
    for x,y in [(105,386),(1100,430),(335,242),(968,257)]: star(d,x,y,10,'#FFFFFF')
    return im
BACK=[background(i) for i in range(3)]
def character(im,name,x,y,t,phase=0,pose=None,active=True):
    if pose is None: pose=[1,3,2,1][int(t/6+phase)%4]
    s=SPRITES[(name,pose)]
    a=math.sin(t*2.8+phase)*2.0 if active else 0
    s=s.rotate(a,resample=Image.Resampling.BICUBIC,expand=True)
    bounce=abs(math.sin(t*3.1+phase))*9 if active else 0
    im.paste(s,(int(x-s.width/2),int(y-s.height-bounce)),s)
def food(d,kind,x,y,s=1):
    # Simple original vector props; these are objects, not additions to the cast.
    def poly(p,c):d.polygon([(x+a*s,y+b*s) for a,b in p],fill=c)
    def ell(b,c):d.ellipse(tuple([x+b[0]*s,y+b[1]*s,x+b[2]*s,y+b[3]*s]),fill=c)
    if kind=='sandwich':
        poly([(-82,65),(85,65),(0,-85)],'#D19A51');poly([(-70,50),(72,50),(0,-69)],'#FFF0C5')
        poly([(-74,49),(75,49),(78,60),(-78,60)],'#76A357');poly([(-68,34),(66,34),(72,45),(-72,45)],'#EF795F')
    elif kind=='apple':
        ell((-68,-44,15,83),'#EC675C');ell((-13,-44,70,83),'#EC675C');poly([(-4,-33),(5,-33),(10,-83),(1,-83)],'#785643');ell((5,-83,52,-55),'#69986B')
    elif kind=='carrot':
        poly([(-40,-55),(47,-47),(-3,98)],'#F39246');poly([(-7,-54),(-48,-106),(-10,-83),(5,-115),(16,-80),(48,-100),(14,-49)],'#68A779')
        for yy in [-22,8,38]:d.line((x-18*s,y+yy*s,x+10*s,y+(yy+5)*s),fill='#D47136',width=4)
    elif kind=='cheese':
        poly([(-78,60),(79,60),(79,-35),(-2,-85),(-78,-8)],'#EDB741');poly([(-78,-8),(-2,-85),(79,-35),(0,16)],'#FFE485');poly([(-78,-8),(0,16),(0,60),(-78,60)],'#F8CE62')
        for xx,yy,r in [(29,9,13),(51,41,8),(-34,25,10)]:ell((xx-r,yy-r,xx+r,yy+r),'#D99C33')
    elif kind=='water':
        poly([(-44,-78),(45,-78),(33,82),(-32,82)],'#A2DAE5');poly([(-38,-34),(39,-34),(28,75),(-27,75)],'#60B9D6')
        d.line((x-26*s,y-58*s,x-20*s,y+49*s),fill='white',width=5)
    else:
        ell((-70,-70,70,70),'#DDA766')
        for xx,yy in [(-30,-27),(18,-35),(38,8),(-28,27),(8,40),(0,0)]:ell((xx-6,yy-6,xx+6,yy+6),'#916047')

def frame(ch,t,total):
    im=BACK[ch].copy();d=ImageDraw.Draw(im)
    # Clouds drift without flashes or hard background changes.
    for i in range(4):
        x=((i*360+t*9)%1560)-140;y=200+i%2*35
        d.ellipse((x-44,y,x+58,y+30),fill='#FFFFFF');d.ellipse((x-14,y-18,x+30,y+24),fill='#FFFFFF')
    d.rounded_rectangle((34,24,303,67),radius=21,fill='white')
    text(d,(168,46),'FUN FOR NORDIC',22)
    text(d,(1234,46),f'{ch+1} / 3',22,anchor='rm')
    text(d,(640,96),SONGS[ch][2],18,TEAL)
    text(d,(640,150),SONGS[ch][1],48)
    if t<5:
        text(d,(640,215),'Listen. Sing. Play!',26,TEAL)
    # Cast remains stable across songs, with Pip as the guide.
    left=['freya','astrid','nico'][ch];right=['nico','tomas','freya'][ch]
    if ch<2:d.ellipse((226,308,510,639),fill='#FFFFFF')
    character(im,left,190,620,t,0)
    character(im,right,1090,620,t,2)
    d=ImageDraw.Draw(im)
    if ch==0:
        names=['ball','kite','train','car','teddy','doll']; idx=int(max(0,t-5)/7)%6
        name=names[idx]; p=PROPS[name]; py=int(355+math.sin(t*2)*12)
        d.ellipse((476,245,804,562),fill='#FFFFFF')
        # Object motion is distinct: the ball bounces and the train travels.
        px=640+int(math.sin(t*1.7)* (30 if name in ['train','car'] else 9))
        im.paste(p,(px-p.width//2,py-p.height//2),p)
        d=ImageDraw.Draw(im);text(d,(640,535),name.upper(),36)
        for i,n in enumerate(names):
            x=370+i*108; d.ellipse((x-8,588,x+8,604),fill=TEAL if i==idx else '#FFFFFF')
        character(im,'pip',365,624,t,1,pose=1)
    elif ch==1:
        foods=['sandwich','apple','carrot','cheese','water','biscuit'];idx=int(max(0,t-5)/7)%6
        d.rounded_rectangle((429,245,851,570),32,fill='#FFFFFF')
        # Opening lunchbox lid and dancing food.
        d.rounded_rectangle((457,457,823,541),20,fill='#ECAA64')
        d.rounded_rectangle((481,467,799,532),14,fill='#F8D8A9')
        food(d,foods[idx],640,363+int(math.sin(t*2.1)*12),1.05)
        text(d,(640,588),foods[idx].upper(),36)
        character(im,'pip',357,624,t,1,pose=2)
    else:
        d.ellipse((409,248,871,606),fill='#FFFFFF')
        character(im,'pip',640,569,t,1,pose=[1,3,1,2][int(t/4)%4])
        for i,label in enumerate(['SHAKE','NOD','WAVE']):
            x=464+i*176
            d.rounded_rectangle((x-76,598,x+76,645),23,fill=[TEAL,CORAL,'#6D80B9'][i])
            text(d,(x,622),label,22,'white')
        for i in range(8):
            a=i*math.pi/4+t*.35;x=640+math.cos(a)*221;y=426+math.sin(a)*165
            star(d,x,y,8+3*math.sin(t*2+i),['#E6B34D','#EF795F','#6DA69E'][i%3])
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((34,671,1246,699),14,fill='#FFFFFF')
    progress=max(.01,min(1,t/total))
    d.rounded_rectangle((34,671,34+1212*progress,699),14,fill=TEAL)
    # Gentle dip at chapter boundaries.
    fade=min(1,t/.7,(total-t)/.8)
    if fade<1:im=Image.blend(Image.new('RGB',(W,H),'#FFFCF4'),im,max(0,fade))
    return im

def render(ch):
    num,title,tag,total=SONGS[ch]
    frames=math.ceil(total*FPS)
    log=open(WORK/f'render-{num}.log','w')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(WORK/f'song{num}.mp3'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-af','afade=t=in:d=0.15,afade=t=out:st='+str(total-.5)+':d=0.5','-shortest','-movflags','+faststart',str(WORK/f'chapter-{num}.mp4')]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
    for n in range(frames):
        im=frame(ch,n/FPS,total)
        if n==FPS*12: im.save(OUT/f'preview-{num}.jpg',quality=92)
        p.stdin.write(im.tobytes())
        if n%(FPS*20)==0:print(f'{title}: {n//FPS}/{int(total)} sec',flush=True)
    p.stdin.close();p.wait();log.close()
    if p.returncode:raise RuntimeError((WORK/f'render-{num}.log').read_text())
if __name__=='__main__':
    if '--preview' in sys.argv:
        for ch in range(3): frame(ch,12,SONGS[ch][3]).save(OUT/f'preview-{SONGS[ch][0]}.jpg',quality=94)
    else:
        for ch in range(3):render(ch)
        (WORK/'concat.txt').write_text(''.join(f"file 'chapter-{s[0]}.mp4'\n" for s in SONGS))
        meta=';FFMETADATA1\ntitle=Fun for Nordic - Sing and Play\nartist=Nordic International School\n'
        start=0
        for num,title,tag,total in SONGS:
            meta+=f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={round(start*1000)}\nEND={round((start+total)*1000)}\ntitle={title}\n';start+=total
        (WORK/'chapters.txt').write_text(meta)
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(WORK/'concat.txt'),'-i',str(WORK/'chapters.txt'),'-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(OUT/'Fun-for-Nordic-Sing-and-Play.mp4')],check=True)
        print('COMPLETE',flush=True)
