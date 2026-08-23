# -*- coding: utf-8 -*-
"""Genera los SVG de personajes de Fun for Nordic (estilo plano de la biblia).

Salida: assets/characters/<nivel>/<slug>/pose-NN.svg
Niños: lienzo 200x260, poses 01-10. Mascotas: 200x200, poses 01-06.
"""
import math, os

ROOT = os.path.join(os.path.dirname(__file__), "..", "assets", "characters")

KIDS = {
    # nivel, slug: hair_style, hair, skin, shirt, pants, accesorio
    ("starters", "freya"):    ("ponytail", "#E8C86A", "#F6D7B8", "#7FB6E0", "#3E5F8A", None),
    ("starters", "nico"):     ("spiky",    "#2A2320", "#C98E5A", "#E05C4B", "#4A6786", None),
    ("starters", "astrid"):   ("bob",      "#8A5A33", "#F6D7B8", "#58A87A", "#6B7686", None),
    ("starters", "tomas"):    ("short",    "#2A2320", "#C98E5A", "#E8B23A", "#3E5F8A", None),
    ("movers", "erik"):       ("short",    "#C97B3A", "#F6D7B8", "#E08A3C", "#6E5643", "glasses"),
    ("movers", "valentina"):  ("long",     "#2A2320", "#C98E5A", "#8A6FB5", "#6B7686", None),
    ("movers", "sofia"):      ("ponytail", "#8A5A33", "#C98E5A", "#4BA8A0", "#4A6786", None),
    ("movers", "mateo"):      ("curly",    "#2A2320", "#F6D7B8", "#58A87A", "#3E5F8A", None),
    ("flyers", "ingrid"):     ("long",     "#E8C86A", "#F6D7B8", "#2F5D9E", "#6B7686", None),
    ("flyers", "diego"):      ("short",    "#2A2320", "#C98E5A", "#E05C4B", "#3A3F47", None),
    ("flyers", "maya"):       ("bun",      "#6E4A2F", "#C98E5A", "#3E8E6B", "#8F8562", "glasses"),
    ("flyers", "oliver"):     ("spiky",    "#C9622E", "#F6D7B8", "#D9A13B", "#4A6786", None),
}

POSES = ["waving", "pointing", "talking", "thinking", "surprised",
         "sitting", "running", "holding", "back", "celebrating"]

HX, HY, HR = 100, 70, 48            # cabeza
SH_L, SH_R = (76, 130), (124, 130)  # hombros
ARM = 50
HIP_L, HIP_R = (87, 182), (113, 182)


def arm(shoulder, angle, shirt, skin):
    """Brazo = trazo desde el hombro, rotado; mano = círculo al final."""
    x, y = shoulder
    return (f'<g transform="rotate({angle} {x} {y})">'
            f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+ARM}" stroke="{shirt}" '
            f'stroke-width="15" stroke-linecap="round"/>'
            f'<circle cx="{x}" cy="{y+ARM}" r="9" fill="{skin}"/></g>')


def leg(hip, angle, pants):
    x, y = hip
    return (f'<g transform="rotate({angle} {x} {y})">'
            f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+48}" stroke="{pants}" '
            f'stroke-width="17" stroke-linecap="round"/>'
            f'<ellipse cx="{x}" cy="{y+52}" rx="13" ry="8" fill="#3A3F47"/></g>')


def hair_front(style, color):
    p = []
    if style in ("short", "spiky", "curly", "bun", "ponytail"):
        p.append(f'<path d="M {HX-HR} {HY} A {HR} {HR} 0 0 1 {HX+HR} {HY} '
                 f'L {HX+HR} {HY-6} A {HR} {HR} 0 0 0 {HX-HR} {HY-6} Z" fill="{color}"/>')
        p.append(f'<path d="M {HX-HR} {HY+2} A {HR} {HR} 0 0 1 {HX+HR} {HY+2} '
                 f'A {HR*1.02} {HR*0.65} 0 0 0 {HX-HR} {HY+2} Z" fill="{color}"/>')
    if style == "spiky":
        for i in range(5):
            x = HX - 34 + i * 17
            p.append(f'<path d="M {x} {HY-40} l 8 -16 l 8 16 Z" fill="{color}"/>')
    if style == "curly":
        for i in range(6):
            a = math.pi * (0.15 + 0.14 * i)
            x, y = HX - HR * math.cos(a), HY - HR * math.sin(a) + 2
            p.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="12" fill="{color}"/>')
    if style == "bun":
        p.append(f'<circle cx="{HX}" cy="{HY-HR-6}" r="14" fill="{color}"/>')
    if style == "ponytail":
        p.append(f'<circle cx="{HX+HR+2}" cy="{HY-18}" r="10" fill="{color}"/>')
        p.append(f'<path d="M {HX+HR+2} {HY-18} q 14 26 4 52 q -10 -6 -14 -20 Z" fill="{color}"/>')
    if style == "bob":
        p.append(f'<path d="M {HX-HR} {HY-4} A {HR} {HR} 0 0 1 {HX+HR} {HY-4} '
                 f'L {HX+HR+4} {HY+34} q -10 8 -18 2 L {HX+HR-14} {HY+2} '
                 f'A {HR-14} {HR-14} 0 0 0 {HX-HR+14} {HY+2} L {HX-HR+14} {HY+36} '
                 f'q -8 6 -18 -2 Z" fill="{color}"/>')
    if style == "long":
        p.append(f'<path d="M {HX-HR} {HY-4} A {HR} {HR} 0 0 1 {HX+HR} {HY-4} '
                 f'L {HX+HR+6} {HY+64} q -12 8 -20 0 L {HX+HR-14} {HY+4} '
                 f'A {HR-14} {HR-14} 0 0 0 {HX-HR+14} {HY+4} L {HX-HR+14} {HY+64} '
                 f'q -8 8 -20 0 Z" fill="{color}"/>')
    return "".join(p)


def hair_back(style, color):
    extra = ""
    if style == "bun":
        extra = f'<circle cx="{HX}" cy="{HY-HR-6}" r="14" fill="{color}"/>'
    if style == "ponytail":
        extra = (f'<circle cx="{HX}" cy="{HY-HR+4}" r="11" fill="{color}"/>'
                 f'<path d="M {HX} {HY-HR+4} q 12 40 0 78 q -12 -38 0 -78 Z" fill="{color}"/>')
    if style in ("bob", "long"):
        d = 40 if style == "bob" else 66
        extra = (f'<path d="M {HX-HR} {HY} L {HX-HR+4} {HY+d} q {HR-4} 14 {2*(HR-4)} 0 '
                 f'L {HX+HR} {HY} Z" fill="{color}"/>')
    if style == "spiky":
        extra = "".join(f'<path d="M {HX-34+i*17} {HY-40} l 8 -16 l 8 16 Z" fill="{color}"/>'
                        for i in range(5))
    return f'<circle cx="{HX}" cy="{HY}" r="{HR}" fill="{color}"/>' + extra


def face(expr, accessory):
    eyes_y = HY - 2
    parts = []
    if expr == "thinking":
        eyes_y -= 6
    parts.append(f'<circle cx="{HX-18}" cy="{eyes_y}" r="4.5" fill="#2A2320"/>')
    parts.append(f'<circle cx="{HX+18}" cy="{eyes_y}" r="4.5" fill="#2A2320"/>')
    by = HY - 16 if expr != "surprised" else HY - 22
    parts.append(f'<path d="M {HX-24} {by} q 6 -5 12 0" stroke="#2A2320" stroke-width="3" fill="none" stroke-linecap="round"/>')
    parts.append(f'<path d="M {HX+12} {by} q 6 -5 12 0" stroke="#2A2320" stroke-width="3" fill="none" stroke-linecap="round"/>')
    if expr in ("smile", "thinking"):
        w = 10 if expr == "thinking" else 16
        parts.append(f'<path d="M {HX-w} {HY+20} q {w} {12 if expr=="smile" else 4} {2*w} 0" '
                     f'stroke="#2A2320" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
    elif expr == "open":
        parts.append(f'<path d="M {HX-14} {HY+18} q 14 20 28 0 Z" fill="#7A3B33"/>')
    elif expr == "o":
        parts.append(f'<ellipse cx="{HX}" cy="{HY+24}" rx="9" ry="11" fill="#7A3B33"/>')
    if accessory == "glasses":
        parts.append(f'<g stroke="#2A2320" stroke-width="3" fill="none">'
                     f'<circle cx="{HX-18}" cy="{eyes_y}" r="12"/>'
                     f'<circle cx="{HX+18}" cy="{eyes_y}" r="12"/>'
                     f'<line x1="{HX-6}" y1="{eyes_y}" x2="{HX+6}" y2="{eyes_y}"/></g>')
    return "".join(parts)


def kid_svg(style, hair, skin, shirt, pants, accessory, pose):
    torso = f'<rect x="70" y="116" width="60" height="72" rx="20" fill="{shirt}"/>'
    head = f'<circle cx="{HX}" cy="{HY}" r="{HR}" fill="{skin}"/>'
    ears = (f'<circle cx="{HX-HR}" cy="{HY+4}" r="8" fill="{skin}"/>'
            f'<circle cx="{HX+HR}" cy="{HY+4}" r="8" fill="{skin}"/>')
    legs = leg(HIP_L, 0, pants) + leg(HIP_R, 0, pants)
    expr, extra, lean = "smile", "", 0

    if pose == "waving":
        arms = arm(SH_L, 15, shirt, skin) + arm(SH_R, -150, shirt, skin)
    elif pose == "pointing":
        arms = arm(SH_L, 8, shirt, skin) + arm(SH_R, -95, shirt, skin)
    elif pose == "talking":
        arms = arm(SH_L, 25, shirt, skin) + arm(SH_R, -50, shirt, skin)
        expr = "open"
    elif pose == "thinking":
        arms = arm(SH_L, 8, shirt, skin) + arm(SH_R, -168, shirt, skin)
        expr = "thinking"
    elif pose == "surprised":
        arms = arm(SH_L, 140, shirt, skin) + arm(SH_R, -140, shirt, skin)
        expr = "o"
    elif pose == "sitting":
        arms = arm(SH_L, 30, shirt, skin) + arm(SH_R, -30, shirt, skin)
        legs = (f'<line x1="87" y1="182" x2="60" y2="206" stroke="{pants}" stroke-width="17" stroke-linecap="round"/>'
                f'<line x1="60" y1="206" x2="66" y2="232" stroke="{pants}" stroke-width="15" stroke-linecap="round"/>'
                f'<ellipse cx="66" cy="238" rx="12" ry="8" fill="#3A3F47"/>'
                f'<line x1="113" y1="182" x2="140" y2="206" stroke="{pants}" stroke-width="17" stroke-linecap="round"/>'
                f'<line x1="140" y1="206" x2="134" y2="232" stroke="{pants}" stroke-width="15" stroke-linecap="round"/>'
                f'<ellipse cx="134" cy="238" rx="12" ry="8" fill="#3A3F47"/>')
    elif pose == "running":
        arms = arm(SH_L, 50, shirt, skin) + arm(SH_R, -130, shirt, skin)
        legs = leg(HIP_L, 35, pants) + leg(HIP_R, -35, pants)
        lean = -6
        expr = "open"
    elif pose == "holding":
        arms = arm(SH_L, 60, shirt, skin) + arm(SH_R, -60, shirt, skin)
        extra = '<rect x="76" y="164" width="48" height="36" rx="6" fill="#D9A13B" stroke="#8A5A33" stroke-width="3"/>'
    elif pose == "back":
        arms = arm(SH_L, 12, shirt, skin) + arm(SH_R, -12, shirt, skin)
        body = arms + legs + torso + hair_back(style, hair)
        return _wrap(260, f'<g>{body}</g>')
    elif pose == "celebrating":
        arms = arm(SH_L, 160, shirt, skin) + arm(SH_R, -160, shirt, skin)
        expr = "open"

    body = arms + legs + torso + ears + head + hair_front(style, hair) + face(expr, accessory) + extra
    g = f'<g transform="rotate({lean} 100 190)">{body}</g>' if lean else f'<g>{body}</g>'
    return _wrap(260, g)


def _wrap(h, inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 {h}" '
            f'width="200" height="{h}">{inner}</svg>')


# ---------------- Mascotas ----------------

def puffin(pose):
    """Pip: frailecillo #26313B/#F4F1EC, pico y patas #E88A2E."""
    dark, white, orange = "#26313B", "#F4F1EC", "#E88A2E"
    wing_a = {"waving": -120, "pointing": -90, "talking": 20, "thinking": 15,
              "surprised": -60, "sleeping": 25}[pose]
    eye = ('<line x1="86" y1="86" x2="100" y2="86" stroke="#2A2320" stroke-width="3" stroke-linecap="round"/>'
           if pose == "sleeping" else '<circle cx="93" cy="84" r="5" fill="#2A2320"/>')
    beak_open = ('<path d="M 118 96 L 148 88 L 122 104 Z" fill="{o}"/>'
                 '<path d="M 118 104 L 144 106 L 122 112 Z" fill="#C96E1E"/>').format(o=orange) \
        if pose in ("talking", "surprised") else \
        f'<path d="M 118 96 L 150 100 L 118 110 Z" fill="{orange}"/>'
    look_up = ' transform="rotate(-12 100 100)"' if pose == "thinking" else ""
    wings = (f'<g transform="rotate({wing_a} 70 118)"><ellipse cx="70" cy="140" rx="14" ry="26" fill="{dark}"/></g>')
    if pose == "surprised":
        wings += f'<g transform="rotate(60 130 118)"><ellipse cx="130" cy="140" rx="14" ry="26" fill="{dark}"/></g>'
    body = (f'<ellipse cx="100" cy="120" rx="46" ry="56" fill="{dark}"/>'
            f'<ellipse cx="100" cy="132" rx="32" ry="40" fill="{white}"/>'
            f'<circle cx="88" cy="84" r="16" fill="{white}"/>'
            f'{eye}{beak_open}'
            f'<line x1="86" y1="174" x2="86" y2="188" stroke="{orange}" stroke-width="6"/>'
            f'<line x1="114" y1="174" x2="114" y2="188" stroke="{orange}" stroke-width="6"/>'
            f'<path d="M 78 188 l 8 6 l 8 -6 Z" fill="{orange}"/>'
            f'<path d="M 106 188 l 8 6 l 8 -6 Z" fill="{orange}"/>')
    return _wrap(200, f'<g{look_up}>{body}{wings}</g>')


def husky(pose):
    """Luna: husky #9AA7B5/#F4F1EC, ojos #5FA8D9, sentada."""
    grey, white, blue = "#9AA7B5", "#F4F1EC", "#5FA8D9"
    ear_a = {"waving": -14, "pointing": -8, "talking": 0, "thinking": -20,
             "surprised": -26, "sleeping": 16}[pose]
    eye = ('<line x1="74" y1="84" x2="88" y2="84" stroke="#2A2320" stroke-width="3" stroke-linecap="round"/>'
           '<line x1="112" y1="84" x2="126" y2="84" stroke="#2A2320" stroke-width="3" stroke-linecap="round"/>'
           if pose == "sleeping" else
           f'<circle cx="81" cy="84" r="5" fill="{blue}"/><circle cx="119" cy="84" r="5" fill="{blue}"/>'
           f'<circle cx="81" cy="84" r="2.4" fill="#2A2320"/><circle cx="119" cy="84" r="2.4" fill="#2A2320"/>')
    mouth = ('<ellipse cx="100" cy="112" rx="8" ry="10" fill="#7A3B33"/>' if pose in ("talking", "surprised")
             else '<path d="M 92 112 q 8 8 16 0" stroke="#2A2320" stroke-width="3" fill="none" stroke-linecap="round"/>')
    tail_d = ("M 152 158 q 26 -8 22 -34" if pose in ("waving", "surprised", "talking")
              else "M 152 162 q 24 4 30 -14")
    paw = f'<g transform="rotate(-110 64 150)"><line x1="64" y1="150" x2="64" y2="186" stroke="{grey}" stroke-width="14" stroke-linecap="round"/></g>' \
        if pose == "pointing" else ""
    body = (f'<path d="{tail_d}" stroke="{grey}" stroke-width="13" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="100" cy="150" rx="52" ry="44" fill="{grey}"/>'
            f'<ellipse cx="100" cy="160" rx="34" ry="32" fill="{white}"/>'
            f'<g transform="rotate({ear_a} 66 44)"><path d="M 54 62 L 66 24 L 84 56 Z" fill="{grey}"/></g>'
            f'<g transform="rotate({-ear_a} 134 44)"><path d="M 146 62 L 134 24 L 116 56 Z" fill="{grey}"/></g>'
            f'<circle cx="100" cy="82" r="40" fill="{grey}"/>'
            f'<path d="M 100 58 q 26 0 30 30 q -12 22 -30 22 q -18 0 -30 -22 q 4 -30 30 -30 Z" fill="{white}"/>'
            f'{eye}<ellipse cx="100" cy="100" rx="7" ry="5" fill="#2A2320"/>{mouth}'
            f'<line x1="80" y1="176" x2="80" y2="192" stroke="{white}" stroke-width="12" stroke-linecap="round"/>'
            f'<line x1="120" y1="176" x2="120" y2="192" stroke="{white}" stroke-width="12" stroke-linecap="round"/>'
            f'{paw}')
    return _wrap(200, f'<g>{body}</g>')


def condor(pose):
    """Kili: cóndor #2E2A33, collar #F4F1EC, cabeza #D98A6A."""
    dark, white, headc = "#2E2A33", "#F4F1EC", "#D98A6A"
    wing_a = {"waving": -130, "pointing": -95, "talking": 15, "thinking": 10,
              "surprised": -70, "sleeping": 20}[pose]
    eye = ('<line x1="88" y1="66" x2="100" y2="66" stroke="#2A2320" stroke-width="3" stroke-linecap="round"/>'
           if pose == "sleeping" else '<circle cx="94" cy="66" r="4.5" fill="#2A2320"/>')
    beak = (f'<path d="M 112 70 q 22 0 20 14 l -20 -4 Z" fill="#C9A34B"/>')
    letter = ('<rect x="120" y="86" width="34" height="24" rx="3" fill="#F4F1EC" stroke="#8A5A33" stroke-width="2" transform="rotate(8 137 98)"/>'
              '<path d="M 121 88 l 16 12 l 16 -12" stroke="#8A5A33" stroke-width="2" fill="none" transform="rotate(8 137 98)"/>') \
        if pose == "pointing" else ""
    wings = f'<g transform="rotate({wing_a} 66 120)"><path d="M 66 108 q -30 26 -18 62 q 16 -10 30 -34 Z" fill="{dark}"/></g>'
    if pose == "surprised":
        wings += f'<g transform="rotate(70 134 120)"><path d="M 134 108 q 30 26 18 62 q -16 -10 -30 -34 Z" fill="{dark}"/></g>'
    body = (f'<ellipse cx="100" cy="130" rx="44" ry="54" fill="{dark}"/>'
            f'<path d="M 64 100 q 36 -22 72 0 q -8 18 -36 18 q -28 0 -36 -18 Z" fill="{white}"/>'
            f'<circle cx="98" cy="66" r="24" fill="{headc}"/>'
            f'{eye}{beak}'
            f'<line x1="86" y1="182" x2="86" y2="194" stroke="#C9A34B" stroke-width="6"/>'
            f'<line x1="114" y1="182" x2="114" y2="194" stroke="#C9A34B" stroke-width="6"/>'
            f'{letter}')
    return _wrap(200, f'<g>{body}{wings}</g>')


MASCOTS = {
    ("starters", "pip"): puffin,
    ("movers", "luna"): husky,
    ("flyers", "kili"): condor,
}
MASCOT_POSES = ["waving", "pointing", "talking", "thinking", "surprised", "sleeping"]


def main():
    n = 0
    for (level, slug), (style, hair, skin, shirt, pants, acc) in KIDS.items():
        d = os.path.join(ROOT, level, slug)
        os.makedirs(d, exist_ok=True)
        for i, pose in enumerate(POSES, 1):
            with open(os.path.join(d, f"pose-{i:02d}.svg"), "w", encoding="utf-8") as f:
                f.write(kid_svg(style, hair, skin, shirt, pants, acc, pose))
            n += 1
    for (level, slug), fn in MASCOTS.items():
        d = os.path.join(ROOT, level, slug)
        os.makedirs(d, exist_ok=True)
        for i, pose in enumerate(MASCOT_POSES, 1):
            with open(os.path.join(d, f"pose-{i:02d}.svg"), "w", encoding="utf-8") as f:
                f.write(fn(pose))
            n += 1
    print(f"{n} SVG generados en {os.path.abspath(ROOT)}")


if __name__ == "__main__":
    main()
