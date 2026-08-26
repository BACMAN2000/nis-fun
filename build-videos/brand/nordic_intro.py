#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bumper de marca Nordic (NIS) — replica la gramatica del splash de Cambridge
(Fun for Flyers 4e / Presentation Plus): marca sola -> destello -> giro 3D ->
se asienta en el lockup -> reposo -> salida.

Salida: secuencia PNG + wav, ensamblados luego por ffmpeg.
"""
import os, sys, math
import numpy as np
from PIL import Image

LOGO_DIR = "C:/Users/User/OneDrive/09_Instituciones/NORDIC/MARKETING/LOGO/PNG"

W, H = 1920, 1080
FPS = 30
DUR = 3.45
NFRAMES = int(round(DUR * FPS))

# --- paleta de marca (extraida de los SVG oficiales) ---
AZUL = (0x49, 0x87, 0xc6)
AZUL_CLARO = (0xd1, 0xd2, 0xea)
GRIS = (0x63, 0x64, 0x65)

# --- linea de tiempo (segundos) ---
T_ENTRY_A, T_ENTRY_B = 0.00, 0.52     # la N entra (escala + fade)
T_SHINE_A, T_SHINE_B = 0.60, 1.02     # destello que barre
T_FLIP_A,  T_FLIP_B  = 1.00, 1.66     # giro 3D (540 grados)
T_SET_A,   T_SET_B   = 1.66, 2.20     # se encoge y se corre a la izquierda
T_WORD_A,  T_WORD_B  = 1.92, 2.44     # el texto se revela con wipe
T_OUT_A,   T_OUT_B   = 3.10, 3.45     # fundido de salida

SPIN_TURNS = 1.0                       # vuelta completa: termina de frente


# ---------------------------------------------------------------- easings
def clamp01(x):
    return 0.0 if x < 0 else (1.0 if x > 1 else x)


def prog(t, a, b):
    return clamp01((t - a) / (b - a)) if b > a else (1.0 if t >= b else 0.0)


def ease_out_cubic(x):
    return 1 - (1 - x) ** 3


def ease_in_out_cubic(x):
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def ease_out_back(x, s=1.70158):
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


# ---------------------------------------------------------------- assets
def load_parts(negative=False):
    """Separa el lockup horizontal en marca (la N) y wordmark (el texto)."""
    name = "Nordic Logo H N.png" if negative else "Nordic Logo H.png"
    im = Image.open(os.path.join(LOGO_DIR, name)).convert("RGBA")
    a = np.array(im)[:, :, 3]
    cols = (a > 8).sum(axis=0)
    nz = np.where(cols > 0)[0]
    # primer hueco ancho = separacion entre la N y el texto
    run, gap = None, None
    for x in range(nz.min(), nz.max() + 1):
        if cols[x] == 0:
            if run is None:
                run = x
        else:
            if run is not None and x - run > 100:
                gap = (run, x)
                break
            run = None
    gx0, gx1 = gap
    mark = im.crop((nz.min(), 0, gx0, im.height))
    word = im.crop((gx1, 0, nz.max() + 1, im.height))
    return im, mark, word, (nz.min(), gx0, gx1, nz.max() + 1)


# ---------------------------------------------------------------- 3D flip
def persp_coeffs(dst, src):
    """Coeficientes para Image.transform(PERSPECTIVE): mapea dst -> src."""
    M, B = [], []
    for (dx, dy), (sx, sy) in zip(dst, src):
        M.append([dx, dy, 1, 0, 0, 0, -sx * dx, -sx * dy])
        M.append([0, 0, 0, dx, dy, 1, -sy * dx, -sy * dy])
        B.append(sx)
        B.append(sy)
    res = np.linalg.lstsq(np.array(M, dtype=float), np.array(B, dtype=float), rcond=None)[0]
    return res.tolist()


def flip_render(img, theta, pad=1.35):
    """Gira `img` sobre su eje Y con proyeccion en perspectiva real.
    Devuelve RGBA del mismo tamano que el lienzo acolchado."""
    w, h = img.size
    cw, ch = int(w * pad), int(h * pad)

    c = math.cos(theta)
    back = c < 0
    src = img.transpose(Image.FLIP_LEFT_RIGHT) if back else img

    # rectangulo plano rotado sobre Y, proyectado en perspectiva
    d = w * 2.4                      # distancia de camara
    f = d                            # focal
    hw, hh = w / 2.0, h / 2.0
    ac = abs(c)
    s = math.sin(theta)
    pts = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        x3 = sx * hw * ac
        z3 = -sx * hw * abs(s)       # profundidad: un borde se acerca, el otro se aleja
        y3 = sy * hh
        k = f / (d + z3)
        pts.append((cw / 2 + x3 * k, ch / 2 + y3 * k))

    if abs(c) < 0.012:               # de canto: practicamente invisible
        return Image.new("RGBA", (cw, ch), (0, 0, 0, 0)), back

    dst = [(0, 0), (src.width, 0), (src.width, src.height), (0, src.height)]
    coeffs = persp_coeffs(pts, dst)
    out = src.transform((cw, ch), Image.PERSPECTIVE, coeffs,
                        Image.BICUBIC, fillcolor=(0, 0, 0, 0))
    return out, back


# ---------------------------------------------------------------- capas
def vignette(negative):
    """Fondo de marca: blanco con halo azul (o azul con halo claro en negativo)."""
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.72)) ** 2)
    r = np.clip(r, 0, 1)
    if negative:
        base = np.array(AZUL, dtype=float)
        edge = np.array([0x2c, 0x5b, 0x8c], dtype=float)
    else:
        base = np.array([255, 255, 255], dtype=float)
        edge = np.array(AZUL_CLARO, dtype=float) * 0.55 + 255 * 0.45
    k = (r ** 1.6)[:, :, None]
    bg = base[None, None, :] * (1 - k) + edge[None, None, :] * k
    return bg


def apply_shine(layer, p):
    """Banda de luz diagonal que barre la marca (como el destello de Cambridge)."""
    if p <= 0 or p >= 1:
        return layer
    arr = np.array(layer, dtype=float)
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    # posicion de la banda, diagonal
    u = (xx / w) * 0.78 + (yy / h) * 0.22
    pos = p * 1.6 - 0.3
    band = np.exp(-((u - pos) ** 2) / (2 * 0.055 ** 2))
    alpha = arr[:, :, 3:4] / 255.0
    glow = (band[:, :, None] * alpha) * 255.0
    arr[:, :, :3] = np.clip(arr[:, :, :3] + glow * 0.95, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def composite(bg, layer, cx, cy, opacity=1.0):
    """Pega `layer` centrada en (cx, cy) sobre el array de fondo bg (float HxWx3)."""
    if opacity <= 0:
        return bg
    lw, lh = layer.size
    x0, y0 = int(round(cx - lw / 2)), int(round(cy - lh / 2))
    x1, y1 = x0 + lw, y0 + lh
    sx0, sy0 = max(0, -x0), max(0, -y0)
    dx0, dy0 = max(0, x0), max(0, y0)
    dx1, dy1 = min(W, x1), min(H, y1)
    if dx1 <= dx0 or dy1 <= dy0:
        return bg
    sub = np.array(layer, dtype=float)[sy0:sy0 + (dy1 - dy0), sx0:sx0 + (dx1 - dx0)]
    a = (sub[:, :, 3:4] / 255.0) * opacity
    bg[dy0:dy1, dx0:dx1] = bg[dy0:dy1, dx0:dx1] * (1 - a) + sub[:, :, :3] * a
    return bg


def shade(img, k):
    """Oscurece/aclara conservando el alfa (para el dorso del giro)."""
    if abs(k - 1.0) < 1e-3:
        return img
    arr = np.array(img, dtype=float)
    arr[:, :, :3] = np.clip(arr[:, :, :3] * k, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


# ---------------------------------------------------------------- frame
def build(negative=False, outdir="frames"):
    full, mark, word, bounds = load_parts(negative)
    x0, gx0, gx1, x1 = bounds
    total_w = x1 - x0

    LOCK_W = 1000.0                       # ancho del lockup final en el lienzo
    s_end = LOCK_W / total_w             # escala final
    MARK_H_BIG = 470.0                   # alto de la N cuando entra sola
    s_big = MARK_H_BIG / mark.height

    lock_x0 = (W - LOCK_W) / 2.0
    mark_w_end = mark.width * s_end
    cx_end = lock_x0 + mark_w_end / 2.0
    cy = H / 2.0
    cx_big = W / 2.0

    word_w_end = word.width * s_end
    word_h_end = word.height * s_end
    word_x0 = lock_x0 + (gx1 - x0) * s_end

    os.makedirs(outdir, exist_ok=True)
    bg0 = vignette(negative)

    for i in range(NFRAMES):
        t = i / FPS
        bg = bg0.copy()

        # ---- escala / posicion de la marca
        p_set = ease_in_out_cubic(prog(t, T_SET_A, T_SET_B))
        s_now = s_big + (s_end - s_big) * p_set
        cx_now = cx_big + (cx_end - cx_big) * p_set

        if t < T_ENTRY_B:                       # entrada
            pe = ease_out_cubic(prog(t, T_ENTRY_A, T_ENTRY_B))
            s_now *= 0.82 + 0.18 * pe
            op = clamp01(prog(t, T_ENTRY_A, T_ENTRY_A + 0.24))
        else:
            op = 1.0

        mw = max(2, int(round(mark.width * s_now)))
        mh = max(2, int(round(mark.height * s_now)))
        base_mark = mark.resize((mw, mh), Image.LANCZOS)

        # ---- destello
        p_shine = prog(t, T_SHINE_A, T_SHINE_B)
        if 0 < p_shine < 1:
            base_mark = apply_shine(base_mark, p_shine)

        # ---- giro 3D con motion blur
        p_flip_raw = prog(t, T_FLIP_A, T_FLIP_B)
        if 0 < p_flip_raw < 1:
            SUB = 16
            acc_rgb = acc_a = None
            for k in range(SUB):
                tt = (i + (k / SUB) - 0.5) / FPS
                pf = ease_in_out_cubic(prog(tt, T_FLIP_A, T_FLIP_B))
                th = pf * SPIN_TURNS * 2 * math.pi
                lay, back = flip_render(base_mark, th)
                lay = shade(lay, 0.86 if back else 1.0)
                a = np.array(lay, dtype=float)
                al = a[:, :, 3:4] / 255.0
                # promediar en premultiplicado: si no, los subframes
                # transparentes lavan el color y la marca sale gris
                pm = a[:, :, :3] * al
                if acc_rgb is None:
                    acc_rgb, acc_a = pm, al
                else:
                    acc_rgb += pm
                    acc_a += al
            acc_rgb /= SUB
            acc_a /= SUB
            rgb = np.divide(acc_rgb, np.maximum(acc_a, 1e-6))
            out = np.concatenate([np.clip(rgb, 0, 255), acc_a * 255.0], axis=2)
            layer = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")
            # chispazo al cruzar el perfil
            pf_c = ease_in_out_cubic(p_flip_raw)
            th_c = pf_c * SPIN_TURNS * 2 * math.pi
            edge = math.exp(-((math.cos(th_c)) ** 2) / (2 * 0.09 ** 2))
            if edge > 0.02:
                arr = np.array(layer, dtype=float)
                al = arr[:, :, 3:4] / 255.0
                arr[:, :, :3] = np.clip(arr[:, :, :3] + 255 * edge * 0.55 * al, 0, 255)
                layer = Image.fromarray(arr.astype(np.uint8), "RGBA")
        else:
            layer = base_mark

        bg = composite(bg, layer, cx_now, cy, op)

        # ---- wordmark con wipe de izquierda a derecha
        p_word = ease_out_cubic(prog(t, T_WORD_A, T_WORD_B))
        if p_word > 0:
            ww = max(2, int(round(word_w_end)))
            wh = max(2, int(round(word_h_end)))
            wimg = word.resize((ww, wh), Image.LANCZOS)
            arr = np.array(wimg, dtype=float)
            xx = np.arange(ww)[None, :]
            front = p_word * (ww + 160) - 80
            m = np.clip((front - xx) / 90.0, 0, 1)      # borde suave del wipe
            arr[:, :, 3] *= m
            wimg = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
            # entra deslizandose apenas
            dx = (1 - p_word) * 26
            bg = composite(bg, wimg, word_x0 + ww / 2.0 + dx, cy, 1.0)

        # ---- salida
        p_out = prog(t, T_OUT_A, T_OUT_B)
        if p_out > 0:
            tgt = np.array(AZUL if negative else (255, 255, 255), dtype=float)
            k = ease_in_out_cubic(p_out)
            bg = bg * (1 - k) + tgt[None, None, :] * k

        Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).save(
            os.path.join(outdir, "f%04d.png" % i))

    return NFRAMES


# ---------------------------------------------------------------- audio
def build_audio(path, sr=48000):
    n = int(DUR * sr)
    t = np.arange(n) / sr
    out = np.zeros(n)

    # whoosh del giro: ruido rosa filtrado, envolvente en campana
    seg = (t >= T_FLIP_A - 0.10) & (t <= T_FLIP_B + 0.12)
    if seg.any():
        idx = np.where(seg)[0]
        m = len(idx)
        rng = np.random.default_rng(7)
        noise = rng.normal(0, 1, m)
        # filtro pasa-bajos de un polo, con corte que sube y baja
        y = np.zeros(m)
        c = 0.0
        for j in range(m):
            u = j / m
            cut = 0.04 + 0.30 * math.sin(math.pi * u) ** 2
            c += cut * (noise[j] - c)
            y[j] = c
        env = np.sin(math.pi * np.linspace(0, 1, m)) ** 1.8
        out[idx] += y * env * 0.34

    # chime al asentar: triada limpia con decaimiento
    t0 = T_SET_B - 0.14
    idx = np.where(t >= t0)[0]
    if len(idx):
        tt = t[idx] - t0
        env = np.exp(-tt * 3.1)
        tone = (0.60 * np.sin(2 * math.pi * 587.33 * tt) +      # Re5
                0.42 * np.sin(2 * math.pi * 880.00 * tt) +      # La5
                0.26 * np.sin(2 * math.pi * 1174.66 * tt) +     # Re6
                0.12 * np.sin(2 * math.pi * 1760.00 * tt))
        out[idx] += tone * env * 0.30

    # golpe grave al aparecer la marca
    idx = np.where(t >= T_ENTRY_A)[0]
    tt = t[idx] - T_ENTRY_A
    out[idx] += np.sin(2 * math.pi * 70 * tt) * np.exp(-tt * 9.0) * 0.22

    # limitador suave + fades
    out = np.tanh(out * 1.25) * 0.86
    fi = int(0.010 * sr)
    out[:fi] *= np.linspace(0, 1, fi)
    fo = int(0.22 * sr)
    out[-fo:] *= np.linspace(1, 0, fo)

    pcm = (np.clip(out, -1, 1) * 32767).astype("<i2")
    stereo = np.repeat(pcm[:, None], 2, axis=1).tobytes()
    import struct
    with open(path, "wb") as f:
        f.write(b"RIFF" + struct.pack("<I", 36 + len(stereo)) + b"WAVE")
        f.write(b"fmt " + struct.pack("<IHHIIHH", 16, 1, 2, sr, sr * 4, 4, 16))
        f.write(b"data" + struct.pack("<I", len(stereo)) + stereo)


# ---------------------------------------------------------------- cierre
# El cierre va al FINAL de cada video: entra el lockup completo y se queda
# en pantalla hasta el ultimo fotograma (nunca termina en blanco vacio).
OUT_DUR = 2.60
O_IN_A, O_IN_B = 0.06, 0.70        # el lockup entra (escala + fundido)
O_SHINE_A, O_SHINE_B = 0.58, 1.20  # destello que barre el lockup entero


def build_outro(negative=False, outdir="frames_outro"):
    full, mark, word, bounds = load_parts(negative)
    x0, gx0, gx1, x1 = bounds
    lockup = full.crop((x0, 0, x1, full.height))

    LOCK_W = 1000.0
    lw = int(round(LOCK_W))
    lh = int(round(lockup.height * LOCK_W / lockup.width))
    base = lockup.resize((lw, lh), Image.LANCZOS)

    os.makedirs(outdir, exist_ok=True)
    bg0 = vignette(negative)
    n = int(round(OUT_DUR * FPS))

    for i in range(n):
        t = i / FPS
        bg = bg0.copy()

        p_in = ease_out_cubic(prog(t, O_IN_A, O_IN_B))
        s = 0.93 + 0.07 * p_in
        op = clamp01(prog(t, O_IN_A, O_IN_A + 0.30))

        layer = base.resize((max(2, int(lw * s)), max(2, int(lh * s))), Image.LANCZOS)
        p_sh = prog(t, O_SHINE_A, O_SHINE_B)
        if 0 < p_sh < 1:
            layer = apply_shine(layer, p_sh)

        bg = composite(bg, layer, W / 2.0, H / 2.0, op)
        Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).save(
            os.path.join(outdir, "f%04d.png" % i))
    return n


def build_outro_audio(path, sr=48000):
    """Chime de cierre, mas suave que el de la entrada."""
    n = int(OUT_DUR * sr)
    t = np.arange(n) / sr
    out = np.zeros(n)
    t0 = O_IN_A
    idx = np.where(t >= t0)[0]
    tt = t[idx] - t0
    env = np.exp(-tt * 2.2)
    out[idx] += (0.55 * np.sin(2 * math.pi * 587.33 * tt) +
                 0.38 * np.sin(2 * math.pi * 880.00 * tt) +
                 0.22 * np.sin(2 * math.pi * 1174.66 * tt)) * env * 0.26
    out = np.tanh(out * 1.15) * 0.8
    fi = int(0.012 * sr)
    out[:fi] *= np.linspace(0, 1, fi)
    fo = int(0.30 * sr)
    out[-fo:] *= np.linspace(1, 0, fo)
    pcm = (np.clip(out, -1, 1) * 32767).astype("<i2")
    stereo = np.repeat(pcm[:, None], 2, axis=1).tobytes()
    import struct
    with open(path, "wb") as f:
        f.write(b"RIFF" + struct.pack("<I", 36 + len(stereo)) + b"WAVE")
        f.write(b"fmt " + struct.pack("<IHHIIHH", 16, 1, 2, sr, sr * 4, 4, 16))
        f.write(b"data" + struct.pack("<I", len(stereo)) + stereo)


if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "light"
    outdir = sys.argv[2] if len(sys.argv) > 2 else "frames_" + variant
    here = os.path.dirname(outdir) or "."

    if variant == "outro":
        n = build_outro(negative=False, outdir=outdir)
        build_outro_audio(os.path.join(here, "nordic_outro.wav"))
        print("frames cierre:", n, "->", outdir)
    else:
        n = build(negative=(variant == "dark"), outdir=outdir)
        print("frames:", n, "->", outdir)
        if variant == "light":
            build_audio(os.path.join(here, "nordic_intro.wav"))
            print("audio ok")
