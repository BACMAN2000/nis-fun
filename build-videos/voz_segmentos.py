# -*- coding: utf-8 -*-
"""Encuentra en que segundos habla alguien en cada video.

Los videos de Veo traen la voz y la musica en la misma pista, asi que no se
pueden separar. Pero si se puede saber CUANDO habla alguien: se filtra la
banda de la voz (300-3400 Hz), se mide la energia cada 100 ms y se juntan
los tramos que superan el umbral. Lo que queda entre medias es musica,
ambiente o la cortinilla de marca, y eso se conserva tal cual.

    python build-videos/voz_segmentos.py                 todos
    python build-videos/voz_segmentos.py pip-intro       uno
    python build-videos/voz_segmentos.py --fotos         y saca un fotograma
                                                         de cada frase
"""
import json, os, subprocess, sys

import numpy as np

VIDEOS = r"C:\Projects\nis-portal\nis-fun\assets\videos"
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz-fr")
NOMBRES = ["pip-intro", "luna-intro", "kili-intro",
           "starters-cast", "movers-cast", "flyers-cast"]

UMBRAL = 0.03        # RMS de la banda de voz por encima de la cual hay habla
MINIMO = 0.25        # frases mas cortas que esto son ruido
JUNTA = 0.60         # dos tramos a menos de esto son la misma frase


def envolvente(mp4):
    """RMS de la banda de voz, un valor cada 100 ms."""
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", mp4, "-af",
         "highpass=f=300,lowpass=f=3400,aresample=16000", "-ac", "1",
         "-f", "s16le", "-"], capture_output=True)
    a = np.frombuffer(r.stdout, dtype=np.int16).astype(np.float32) / 32768
    w = 1600
    if len(a) < w:
        return np.zeros(0)
    return np.sqrt(np.convolve(a * a, np.ones(w) / w, "same"))[::w]


def frases(env):
    bruto, ini = [], None
    for i, x in enumerate(env):
        if x > UMBRAL and ini is None:
            ini = i
        elif x <= UMBRAL and ini is not None:
            bruto.append((ini / 10, i / 10))
            ini = None
    if ini is not None:
        bruto.append((ini / 10, len(env) / 10))

    unidas = []
    for a, b in bruto:
        if unidas and a - unidas[-1][1] <= JUNTA:
            unidas[-1][1] = b
        else:
            unidas.append([a, b])
    return [(a, b) for a, b in unidas if b - a >= MINIMO]


def principal(nombres, fotos):
    os.makedirs(SALIDA, exist_ok=True)
    todo = {}
    for n in nombres:
        mp4 = os.path.join(VIDEOS, n + ".mp4")
        f = frases(envolvente(mp4))
        todo[n] = [{"desde": a, "hasta": b, "dura": round(b - a, 2)}
                   for a, b in f]
        print("%-14s %d frases: %s" % (
            n, len(f), "  ".join("%.1f-%.1f" % x for x in f)))
        if fotos:
            for k, (a, b) in enumerate(f, 1):
                subprocess.run(
                    ["ffmpeg", "-y", "-v", "error", "-ss", str((a + b) / 2),
                     "-i", mp4, "-frames:v", "1", "-vf", "scale=640:-1",
                     os.path.join(SALIDA, "%s-%02d.jpg" % (n, k))])
    with open(os.path.join(SALIDA, "frases.json"), "w", encoding="utf-8") as g:
        json.dump(todo, g, ensure_ascii=False, indent=1)
    return todo


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    principal(args or NOMBRES, "--fotos" in sys.argv)
