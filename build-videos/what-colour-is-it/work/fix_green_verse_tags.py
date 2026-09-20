from pathlib import Path
# The green-verse captions in colour-final-v2.ass carry a broken anchor tag:
# build_green_v2.py prepended '{\an8\pos(640,28)}' from a non-raw string, so \a
# became BEL (0x07) and libass ignored the tag. With default alignment 2 the
# \pos anchor is the text BASELINE-bottom, so those lines drew with their feet
# at y=28 and the glyphs clipped above the frame. Rebuild every anchor tag.
w = Path('work')
TOP_FROM = 15.1
CLEAN = r'{\an8\pos(640,28)}'

def seconds(stamp):
    h, m, s = stamp.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

out = []
fixed = kept = 0
for line in (w / 'colour-final-v2.ass').read_text(encoding='utf-8').splitlines():
    if not line.startswith('Dialogue:'):
        out.append(line); continue
    f = line.split(',', 9)
    text = f[9].replace('\x07', '')  # BEL from the \a escape
    # strip leading anchor/position groups (broken or valid), keep colour spans
    while text.startswith('{'):
        end = text.find('}')
        grp = text[:end + 1]
        if 'pos(' in grp or '\\an' in grp:
            text = text[end + 1:]
        else:
            break
    if seconds(f[1]) >= TOP_FROM:
        f[9] = CLEAN + text
        fixed += 1
    else:
        f[9] = text
        kept += 1
    out.append(','.join(f))

dest = w / 'colour-final-v3.ass'
dest.write_text('\n'.join(out) + '\n', encoding='utf-8')
assert '\x07' not in dest.read_text(encoding='utf-8'), 'BEL still present'
print(f'ok: {fixed} lines anchored top, {kept} bottom, wrote {dest.name}')
