# -*- coding: utf-8 -*-
"""Receptor local de imagenes, para saltarse el bloqueo de descargas de Chrome.

Chrome corta la segunda descarga seguida de un sitio, y el boton de Gemini
deja de funcionar sin avisar. En vez de pelearse con eso, la propia pagina
manda la imagen aqui por POST y el archivo aparece directamente donde hace
falta.

    python tools/recibe_imagen.py            # escucha en 9351
    -> desde la pestana:  POST http://localhost:9351/subir?nombre=hoja.jpg
"""
import os, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 9351
DESTINO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "build-videos", "hojas3d")


class H(BaseHTTPRequestHandler):
    def _cors(self):
        # la pagina que envia es gemini.google.com, otro origen
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_POST(self):
        q = parse_qs(urlparse(self.path).query)
        nombre = (q.get("nombre") or ["hoja.jpg"])[0]
        nombre = os.path.basename(nombre).replace("..", "")
        n = int(self.headers.get("Content-Length", 0))
        datos = self.rfile.read(n)
        os.makedirs(DESTINO, exist_ok=True)
        ruta = os.path.join(DESTINO, nombre)
        with open(ruta, "wb") as f:
            f.write(datos)
        print("recibido: %s  (%d KB)" % (ruta, len(datos) // 1024), flush=True)
        self.send_response(200); self._cors()
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(("OK %d" % len(datos)).encode())

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    os.makedirs(DESTINO, exist_ok=True)
    print("escuchando en http://localhost:%d/subir  ->  %s" % (PUERTO, DESTINO), flush=True)
    HTTPServer(("127.0.0.1", PUERTO), H).serve_forever()
