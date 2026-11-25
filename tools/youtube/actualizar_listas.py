#!/usr/bin/env python3
"""
Descarga los videos de las listas de YouTube que usa el sitio y los guarda
como JSON en shared/data/youtube/<ID_DE_LISTA>.json.

Las listas se detectan solas: busca en las páginas HTML los elementos con
data-youtube-list="ID". No necesita clave de API: usa el feed RSS público
de YouTube (muestra hasta los 15 videos de la lista).

Lo ejecuta GitHub Actions una vez al día (.github/workflows/youtube.yml).
También se puede correr a mano desde la raíz del repositorio:
    python3 tools/youtube/actualizar_listas.py
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "shared" / "data" / "youtube"
FEED = "https://www.youtube.com/feeds/videos.xml?playlist_id={}"
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}
ID_VALIDO = re.compile(r"^[A-Za-z0-9_-]{10,64}$")


def listas_en_el_sitio():
    ids = set()
    for html in RAIZ.rglob("*.html"):
        if ".git" in html.parts:
            continue
        ids.update(re.findall(r'data-youtube-list="([^"]+)"', html.read_text(encoding="utf-8")))
    return sorted(i for i in ids if ID_VALIDO.match(i))


def descargar(lista):
    req = urllib.request.Request(FEED.format(lista), headers={"User-Agent": "aess-site-bot"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raiz = ET.fromstring(r.read())
    videos = []
    for e in raiz.findall("atom:entry", NS):
        vid = e.findtext("yt:videoId", default="", namespaces=NS)
        if not vid:
            continue
        videos.append({
            "id": vid,
            "titulo": e.findtext("atom:title", default="", namespaces=NS).strip(),
            "publicado": e.findtext("atom:published", default="", namespaces=NS)[:10],
        })
    return {
        "lista": lista,
        "titulo": raiz.findtext("atom:title", default="", namespaces=NS).strip(),
        "videos": videos,
    }


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    fallos = 0
    for lista in listas_en_el_sitio():
        try:
            datos = descargar(lista)
        except Exception as exc:  # una lista caída no debe borrar los datos que ya hay
            print(f"[aviso] no se pudo leer la lista {lista}: {exc}", file=sys.stderr)
            fallos += 1
            continue
        destino = SALIDA / f"{lista}.json"
        destino.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{lista}: {len(datos['videos'])} videos -> {destino.relative_to(RAIZ)}")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
