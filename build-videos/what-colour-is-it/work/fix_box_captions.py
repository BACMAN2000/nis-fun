from pathlib import Path
src=Path('work/colour-complete.ass').read_text()
lines=[]
for line in src.splitlines():
    if line.startswith('Dialogue:'):
        fields=line.split(',',9)
        if float(fields[1].split(':')[-1])>=20.3:
            fields[9]=r'{\an8\pos(640,28)}'+fields[9]
            line=','.join(fields)
    lines.append(line)
Path('work/colour-visible-box.ass').write_text('\n'.join(lines),encoding='utf-8')
