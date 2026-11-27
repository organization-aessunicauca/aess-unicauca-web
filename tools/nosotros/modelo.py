#!/usr/bin/env python3
"""
Genera el bloque HTML de la gráfica "Aceleración del conocimiento"
(Modelo Society) para pages/nosotros.html: un SVG animado para pantallas
anchas y una lista equivalente para móvil.

Uso, desde la raíz del repositorio:
    python3 tools/nosotros/modelo.py

Para cambiar textos o colores edita NODOS y vuelve a ejecutar. Solo se
reemplaza lo que está entre <!-- MODELO:INICIO --> y <!-- MODELO:FIN -->.
"""
from html import escape
from math import cos, sin, pi
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PAGINA = RAIZ / "pages" / "nosotros.html"

CENTRO = (430, 330)

# (clave, título, descripción, color, x, y, lado del texto, ícono)
NODOS = [
    ("educacion", "Educación", "El medio para transferir el conocimiento.", "#4ade80", 235, 190, "izq", "frasco"),
    ("competitividad", "Competitividad", "El valor para poner a prueba el saber.", "#5b5bf0", 235, 470, "izq", "engranaje"),
    ("investigacion", "Investigación", "El método para lograr nuevos conocimientos.", "#ef4444", 430, 560, "abajo", "microscopio"),
    ("organizacion", "Organización", "La forma de lograrlo juntos.", "#3ea2f5", 625, 470, "der", "red"),
    ("solidaridad", "Solidaridad", "El principio para inspirar una nueva cultura.", "#f5b301", 625, 190, "der", "manos"),
]
SALIDA = ("transformacion", "Transformación", "Cómo llegamos a la gente.", "#a23cf0", 845, 330, "der", "corazon")

ICONOS = {  # trazos en una caja de 24 × 24, centrados en (12, 12)
    "frasco": '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3"/><path d="M7.5 15h9"/>',
    "engranaje": '<circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>',
    "microscopio": '<path d="M6 21h12M9 21v-2a5 5 0 0 1 9-3"/><path d="M10 4l4 2-3 6-4-2z"/><path d="M12 9l2 1"/>',
    "red": '<circle cx="6" cy="17" r="2.4"/><circle cx="18" cy="17" r="2.4"/><circle cx="12" cy="6" r="2.4"/><path d="M7.4 15l3.4-6.8M16.6 15l-3.4-6.8M8.4 17h7.2"/>',
    "manos": '<circle cx="12" cy="7" r="2.6"/><path d="M8 13.5c1-1.4 2.4-2 4-2s3 .6 4 2"/><path d="M3 13l4 5h4M21 13l-4 5h-4"/>',
    "corazon": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
}


def hexagono(cx, cy, r):
    pts = [(cx + r * cos(pi / 180 * (60 * k - 30)), cy + r * sin(pi / 180 * (60 * k - 30))) for k in range(6)]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def texto(n):
    _, titulo, desc, _, x, y, lado, _ = n
    if lado == "izq":
        tx, anchor, ty = x - 70, "end", y - 8
    elif lado == "der":
        tx, anchor, ty = x + 70, "start", y - 8
    else:
        tx, anchor, ty = x + 70, "start", y - 8
    # parte la descripción en dos líneas de largo similar
    palabras = desc.split()
    mitad = max(1, len(palabras) // 2)
    l1, l2 = " ".join(palabras[:mitad]), " ".join(palabras[mitad:])
    return (f'<text class="mx-title" x="{tx}" y="{ty}" text-anchor="{anchor}">{escape(titulo)}</text>'
            f'<text class="mx-desc" x="{tx}" y="{ty + 24}" text-anchor="{anchor}">'
            f'<tspan x="{tx}" dy="0">{escape(l1)}</tspan><tspan x="{tx}" dy="19">{escape(l2)}</tspan></text>')


def nodo(n, i, salida=False):
    clave, _, _, color, x, y, _, icono = n
    return f'''
        <g class="mx-node{' mx-node--out' if salida else ''}" style="--i:{i};--c:{color}">
          <g class="mx-hex">
            <path class="mx-hex__ring" d="{hexagono(x, y, 50)}"/>
            <path class="mx-hex__fill" d="{hexagono(x, y, 41)}"/>
            <g class="mx-icon" transform="translate({x - 15} {y - 15}) scale(1.25)">{ICONOS[icono]}</g>
          </g>
          <g class="mx-label">{texto(n)}</g>
        </g>'''


def linea(n, i):
    _, _, _, color, x, y, _, _ = n
    cx, cy = CENTRO
    # espina: del borde del núcleo hacia el hexágono, dejando aire en ambos extremos
    dx, dy = x - cx, y - cy
    d = (dx ** 2 + dy ** 2) ** 0.5
    x1, y1 = cx + dx / d * 90, cy + dy / d * 90
    x2, y2 = x - dx / d * 58, y - dy / d * 58
    return f'<line class="mx-line" style="--i:{i};--c:{color}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>'


def svg():
    cx, cy = CENTRO
    lineas = "\n        ".join(linea(n, i) for i, n in enumerate(NODOS))
    nodos = "".join(nodo(n, i) for i, n in enumerate(NODOS))
    sx = SALIDA[4]
    return f'''<svg class="mx-svg" viewBox="-90 0 1250 660" role="img" aria-labelledby="mx-titulo mx-desc">
      <title id="mx-titulo">Aceleración del conocimiento · Modelo Society</title>
      <desc id="mx-desc">Educación, competitividad, investigación, organización y solidaridad convergen en la aceleración del conocimiento, que lleva a la transformación de la sociedad. La juventud es cómo seguimos mejorando.</desc>
      <defs>
        <radialGradient id="mx-core" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#ff5d8f" stop-opacity=".55"/>
          <stop offset="70%" stop-color="#7c2238" stop-opacity=".18"/>
          <stop offset="100%" stop-color="#7c2238" stop-opacity="0"/>
        </radialGradient>
        <marker id="mx-arrow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto">
          <path d="M0,0 L10,5 L0,10 z" fill="#f6f1ea"/>
        </marker>
      </defs>

      <ellipse class="mx-orbit" cx="520" cy="335" rx="500" ry="305"/>
      <g class="mx-orbit-dot"><circle r="6"/></g>
      <text class="mx-ring-label" x="905" y="78" text-anchor="middle">Sociedad</text>
      <text class="mx-ring-label mx-ring-label--sub" x="150" y="605" text-anchor="middle">Juventud</text>
      <text class="mx-desc" x="150" y="627" text-anchor="middle">Cómo seguimos mejorando</text>

      <g class="mx-lines">
        {lineas}
        <line class="mx-line mx-line--out" style="--i:5;--c:#f6f1ea" x1="{cx + 100}" y1="{cy}" x2="{sx - 62}" y2="{cy}" marker-end="url(#mx-arrow)"/>
      </g>

      <g class="mx-core">
        <circle class="mx-core__glow" cx="{cx}" cy="{cy}" r="96" fill="url(#mx-core)"/>
        <circle class="mx-core__ring" cx="{cx}" cy="{cy}" r="84"/>
        <text class="mx-core__text" x="{cx}" y="{cy - 14}" text-anchor="middle">Aceleración</text>
        <text class="mx-core__text" x="{cx}" y="{cy + 8}" text-anchor="middle">del</text>
        <text class="mx-core__text" x="{cx}" y="{cy + 30}" text-anchor="middle">conocimiento</text>
      </g>
      {nodos}{nodo(SALIDA, 6, salida=True)}
    </svg>'''


def lista():
    items = "".join(f'''
        <li class="mx-item" style="--i:{i};--c:{c}">
          <span class="mx-item__icon" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONOS[ic]}</svg></span>
          <div><h3>{escape(t)}</h3><p>{escape(d)}</p></div>
        </li>''' for i, (_, t, d, c, _, _, _, ic) in enumerate(NODOS))
    _, t, d, c, _, _, _, ic = SALIDA
    return f'''<ol class="mx-list">{items}
        <li class="mx-item mx-item--out" style="--i:5;--c:{c}">
          <span class="mx-item__icon" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONOS[ic]}</svg></span>
          <div><h3>{escape(t)}</h3><p>{escape(d)}</p></div>
        </li>
      </ol>'''


BLOQUE = f'''<!-- MODELO:INICIO -->
                <section class="modelo" aria-labelledby="modelo-titulo">
                    <div class="section-meta">Nuestro modelo</div>
                    <div class="modelo__head">
                        <h2 id="modelo-titulo">Aceleración del conocimiento</h2>
                        <p>El <strong>Modelo Society</strong> resume cómo trabajamos: cinco principios que convergen para acelerar el conocimiento y transformar a la sociedad, con la juventud como motor de mejora continua.</p>
                    </div>
                    <div class="modelo__fig" data-modelo>
    {svg()}
    {lista()}
                    </div>
                    <script src="../shared/scripts/modelo-society.js?v=VERSION" defer></script>
                </section>
                <!-- MODELO:FIN -->'''

if __name__ == "__main__":
    import re
    html = PAGINA.read_text(encoding="utf-8")
    v = (re.search(r'main\.css\?v=(\d+)', html) or [None, "1"])[1]
    bloque = BLOQUE.replace("VERSION", v)
    if "<!-- MODELO:INICIO -->" not in html:
        raise SystemExit("Falta el marcador <!-- MODELO:INICIO --> en pages/nosotros.html")
    html = re.sub(r"<!-- MODELO:INICIO -->.*?<!-- MODELO:FIN -->", lambda _m: bloque, html, flags=re.S)
    PAGINA.write_text(html, encoding="utf-8")
    print("actualizada", PAGINA.relative_to(RAIZ))
