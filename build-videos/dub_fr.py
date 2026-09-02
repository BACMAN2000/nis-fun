# -*- coding: utf-8 -*-
"""Dobla al frances los seis videos de mascotas y elenco.

Los videos son de Veo: la voz y la musica van en la MISMA pista y no se
pueden separar. Lo que si se puede es saber cuando habla alguien
(voz_segmentos.py mide la banda de la voz), y entonces:

  * se calla el original SOLO en esos huecos, con un desvanecido de 80 ms
    para que no se note el corte;
  * se mete ahi la frase francesa, ajustada al hueco con atempo;
  * todo lo demas -la cortinilla de marca, la musica, el ambiente, el
    cierre con el logo- se queda exactamente igual.

Los labios no cuadran, claro: los personajes fueron animados hablando
ingles. En las mascotas no se nota (un pico y un hocico no hacen fonemas) y
en el elenco los ninos salen de cuerpo entero y pequenos. Rehacer los
videos hablando frances significaria volver a generarlos con Veo.

    python build-videos/dub_fr.py                 los seis
    python build-videos/dub_fr.py pip-intro       uno
    python build-videos/dub_fr.py --solo-audio    deja los wav y no ensambla
"""
import asyncio, json, os, subprocess, sys

import edge_tts
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
VIDEOS = r"C:\Projects\nis-portal\nis-fun\assets\videos"
TRABAJO = os.path.join(AQUI, "voz-fr")
SR = 44100

# Voces. No hay voces infantiles en Edge TTS, asi que se suben de tono: las
# ninas sobre Eloise (que ya es joven) y los ninos sobre Henri, que necesita
# mucho mas para dejar de sonar a adulto.
NINA = "fr-FR-EloiseNeural"
NINO = "fr-FR-HenriNeural"
MASCOTA = "fr-FR-DeniseNeural"

# El guion. Cada frase va en el hueco que le toca (el orden es el de
# voz_segmentos.py, saltando la cortinilla de marca y el cierre del logo).
#
# No es una traduccion de lo que dicen en ingles -no hay transcripcion- sino
# la misma presentacion en frances: cada uno dice quien es y de que equipo.
GUION = {
    "pip-intro": [
        (3.5,  9.8,  MASCOTA, "+30Hz", "Salut ! Moi, c'est Pip. J'habite sur les rochers, près du phare."),
        (10.9, 13.5, MASCOTA, "+30Hz", "Je me cache dans chaque image. Tu me trouves ?"),
    ],
    "luna-intro": [
        (3.7,  12.1, MASCOTA, "+10Hz", "Bonjour ! Moi, c'est Luna. J'adore la neige, et je me souviens de tout ce qui se passe au Club du Fjord."),
        (12.9, 13.5, MASCOTA, "+10Hz", "À bientôt !"),
    ],
    "kili-intro": [
        (3.5,  11.9, MASCOTA, "-10Hz", "Bonjour ! Moi, c'est Kili, le facteur de l'école. J'apporte des lettres et des cartes postales de très loin."),
        (12.9, 13.5, MASCOTA, "-10Hz", "À bientôt !"),
    ],
    "starters-cast": [
        (5.2,  6.9,  NINA, "+18Hz", "Moi, c'est Freya !"),
        (7.8,  11.3, NINO, "+55Hz", "Et moi, c'est Nico. Nous sommes les Explorateurs du Phare !"),
        (14.6, 17.4, NINA, "+10Hz", "Bonjour ! Moi, c'est Astrid."),
        (18.0, 19.7, NINO, "+62Hz", "Et moi, c'est Tomás !"),
        (20.8, 23.1, NINA, "+14Hz", "Bienvenue à Fun for Nordic !"),
    ],
    "movers-cast": [
        (4.3,  5.0,  NINO, "+55Hz", "Salut !"),
        (6.0,  7.3,  NINO, "+55Hz", "Moi, c'est Erik."),
        (7.9,  11.3, NINA, "+16Hz", "Et moi, c'est Valentina. Voici le Club du Fjord !"),
        (14.4, 17.4, NINA, "+10Hz", "Bonjour ! Moi, c'est Sofía."),
        (18.0, 19.0, NINO, "+60Hz", "Viens jouer avec nous !"),
    ],
    "flyers-cast": [
        (5.5,  6.8,  NINA, "+12Hz", "Moi, c'est Ingrid !"),
        (7.6,  11.3, NINO, "+50Hz", "Et moi, c'est Diego. Nous sommes l'Expédition Aurore !"),
        (13.1, 13.6, NINA, "+16Hz", "Salut !"),
        (14.9, 16.0, NINA, "+8Hz",  "Moi, c'est Maya."),
        (17.2, 20.4, NINO, "+52Hz", "Et moi, c'est Oliver. Prêt pour l'aventure ?"),
    ],
}

MARGEN = 0.08        # el desvanecido con que se calla el original
# El hueco se calla un poco mas ancho de lo que mide el detector: la voz
# inglesa se apaga por debajo del umbral pero no de golpe, y esa cola se
# oiria debajo de la frase francesa.
HOLGURA = 0.12


def dura(p):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json",
                        "-show_format", p], capture_output=True, text=True)
    return float(json.loads(r.stdout)["format"]["duration"])


async def graba(texto, voz, tono, destino):
    com = edge_tts.Communicate(texto, voz, pitch=tono, rate="+0%")
    with open(destino, "wb") as f:
        async for t in com.stream():
            if t["type"] == "audio":
                f.write(t["data"])


# Edge TTS deja casi un segundo de silencio a cada lado. Sin quitarlo,
# "Salut !" dura 1,8 s y no cabe en ningun hueco: lo que se acelera despues
# seria el silencio, no la voz.
RECORTA = ("silenceremove=start_periods=1:start_silence=0.04:"
           "start_threshold=-45dB,areverse,"
           "silenceremove=start_periods=1:start_silence=0.04:"
           "start_threshold=-45dB,areverse")


def pcm(p, tempo=1.0):
    """El mp3 como float32 mono a 44100, sin silencios y al tempo pedido."""
    af = [RECORTA, "aresample=%d" % SR]
    # atempo solo acepta 0.5-2.0 por pasada; con uno basta en este rango
    if abs(tempo - 1.0) > 0.01:
        af.insert(1, "atempo=%.4f" % max(0.5, min(2.0, tempo)))
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-af", ",".join(af),
                        "-ac", "1", "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.float32)


def dura_util(p):
    """Lo que dura la frase de verdad, ya sin los silencios de los bordes."""
    return len(pcm(p)) / SR


def pista_de_voz(nombre, lineas, largo):
    """Un wav del largo del video con cada frase en su sitio."""
    out = np.zeros(int(largo * SR) + SR, dtype=np.float32)
    for k, (a, b, voz, tono, texto) in enumerate(lineas, 1):
        mp3 = os.path.join(TRABAJO, "%s-%02d.mp3" % (nombre, k))
        if not os.path.exists(mp3):
            asyncio.run(graba(texto, voz, tono, mp3))
        hueco = b - a
        d = dura_util(mp3)
        # Se acelera solo si no cabe, y con tope: por encima de 1.35 deja de
        # sonar a nino y empieza a sonar a dibujo animado acelerado.
        tempo = 1.0 if d <= hueco else min(1.35, d / hueco)
        x = pcm(mp3, tempo)
        # centrada en el hueco: si sobra sitio, mejor repartido que pegado
        ini = int((a + max(0.0, (hueco - len(x) / SR)) / 2) * SR)
        fin = min(len(out), ini + len(x))
        out[ini:fin] += x[:fin - ini] * 0.92
        print("    %-38s %4.1fs en un hueco de %4.1fs  x%.2f"
              % (texto[:38], d, hueco, tempo))
    return out


def envolvente_original(lineas, n):
    """Ganancia del audio original: 1, y 0 dentro de cada hueco de voz.

    La bajada y la subida son media onda de coseno de 80 ms. Un corte seco
    chasquea, y en un video de 15 segundos el chasquido se oye mas que la
    frase.
    """
    g = np.ones(n, dtype=np.float32)
    r = int(MARGEN * SR)
    rampa = (1 + np.cos(np.linspace(0, np.pi, r))) / 2      # 1 -> 0
    for a, b, *_ in lineas:
        i, j = int((a - HOLGURA) * SR), int((b + HOLGURA) * SR)
        if i >= r:
            g[i - r:i] = np.minimum(g[i - r:i], rampa)          # baja
        g[i:min(j, n)] = 0.0                                    # callado
        k = min(n, j + r)
        if k > j:
            g[j:k] = np.minimum(g[j:k], rampa[::-1][:k - j])    # sube
    return g


def audio_original(mp4):
    """El audio del video como float32 mono a 44100."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-af",
                        "aresample=%d" % SR, "-ac", "1", "-f", "f32le", "-"],
                       capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.float32).copy()


def dobla(nombre, solo_audio):
    lineas = GUION[nombre]
    src = os.path.join(VIDEOS, nombre + ".mp4")
    largo = dura(src)
    print("  %s (%.1fs, %d frases)" % (nombre, largo, len(lineas)))

    orig = audio_original(src)
    voz = pista_de_voz(nombre, lineas, largo)[:len(orig)]
    if len(voz) < len(orig):
        voz = np.pad(voz, (0, len(orig) - len(voz)))

    mezcla = orig * envolvente_original(lineas, len(orig)) + voz
    pico = float(np.max(np.abs(mezcla))) or 1.0
    if pico > 0.99:
        mezcla *= 0.99 / pico

    wav = os.path.join(TRABAJO, nombre + "-fr.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar",
                    str(SR), "-ac", "1", "-i", "-", wav],
                   input=mezcla.tobytes(), check=True)
    if solo_audio:
        return

    salida = os.path.join(TRABAJO, nombre + "-fr.mp4")
    r = subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", src, "-i", wav,
         "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "160k", "-shortest", salida],
        capture_output=True, text=True)
    print("    ->", os.path.basename(salida),
          "OK" if r.returncode == 0 else "ERROR\n" + r.stderr[-400:])


if __name__ == "__main__":
    os.makedirs(TRABAJO, exist_ok=True)
    quiere = [a for a in sys.argv[1:] if not a.startswith("--")] or list(GUION)
    for n in quiere:
        dobla(n, "--solo-audio" in sys.argv)
