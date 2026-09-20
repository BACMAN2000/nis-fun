from pathlib import Path
p=Path('work/colour-complete.ass')
s=p.read_text()
s=s.replace(',,the ', ',,The ')
for color in ('red','yellow','blue','green'):
    s=s.replace('&}'+color+'!', '&}'+color.capitalize()+'!')
p.write_text(s,encoding='utf-8')
p=Path('outputs/What-Colour-Is-It-subtitulos.srt');s=p.read_text()
s=s.replace('\nthe ','\nThe ').replace('\nblue train','\nBlue train')
for c in ('red','yellow','blue','green'): s=s.replace('! '+c+'!','! '+c.capitalize()+'!')
p.write_text(s,encoding='utf-8')
