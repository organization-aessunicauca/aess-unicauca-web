#!/usr/bin/env python3
"""
Genera las 4 páginas de detalle de divisiones (pages/divisiones/*.html)
a partir de una sola tabla de datos, para que todas compartan estructura.

Uso, desde la raíz del repositorio:
    python3 tools/divisiones/generar.py

Para cambiar textos, líderes o proyectos, edita DIVISIONES y vuelve a
ejecutar el script. Solo se reemplaza el contenido entre
<div class="division-page"> y el cierre de .main-content; el <head>
(título, descripción y SEO) de cada página se conserva.
"""
from html import escape
from pathlib import Path
import re

RAIZ = Path(__file__).resolve().parents[2]
FORM_POSTULACION = "https://forms.gle/ge2w6SF74GaRevaz9"

DIVISIONES = [
    {
        "archivo": "astronomia",
        "ancla": "sec-astronomia",
        "num": "01",
        "corto": "Astronomía",
        "titulo": "Astronomía",
        "titulo_grad": "y divulgación del cielo",
        "intro": (
            "Observación astronómica, ciclos de conferencias y campañas de divulgación "
            "científica. La división representa al capítulo en competencias internacionales "
            "y acerca el cielo a la comunidad universitaria y regional."
        ),
        "imagen": "divasatro.jpeg",
        "badge": "Astronomía · Observación · Outreach",
        "lineas": [
            "Observación astronómica y jornadas prácticas",
            "Charlas, talleres y actividades de divulgación",
            "Participación en retos o iniciativas académicas",
            "Articulación con aliados y eventos regionales",
        ],
        "lideres": [
            ("Kevin Ferney Grisales Rodriguez", "Líder", "kevin.jpeg"),
            ("Danna Isabela Agredo Ruiz", "Colíder", "danna.jpeg"),
        ],
        "proyectos": [
            ("Investigación", "Búsqueda de Asteroides",
             "Participación en campañas internacionales de búsqueda de asteroides con el IASC."),
            ("Evento", "NASA Space Apps Challenge",
             "El capítulo es host oficial de la hackatón internacional anual en Popayán."),
            ("Divulgación", "Actividades de divulgación",
             "Talleres, conferencias, demostraciones tecnológicas y experiencias interactivas "
             "para instituciones educativas y público general."),
        ],
    },
    {
        "archivo": "sistemas-inteligentes",
        "ancla": "sec-sia",
        "num": "02",
        "corto": "Sistemas Inteligentes",
        "titulo": "Sistemas Inteligentes",
        "titulo_grad": "y Estratégicos",
        "intro": (
            "Investigación y desarrollo en inteligencia artificial, automatización y "
            "planeación estratégica aplicadas a los proyectos aeroespaciales del capítulo."
        ),
        "imagen": "div2.jpeg",
        "badge": "IA · Automatización · Estrategia",
        "lineas": [
            "Modelos de inteligencia artificial aplicada",
            "Automatización de procesos y toma de decisiones",
            "Análisis de datos técnicos y operativos",
            "Planeación y soporte estratégico para proyectos",
        ],
        "lideres": [
            ("Farid Santiago Carvajal Morales", "Líder", "farid.jpeg"),
        ],
        "proyectos": [
            ("Simulación", "Simulación PsyImmerse",
             "Desarrollo de simulaciones con el semillero PsyImmerse."),
            ("Drones", "Construcción de drones",
             "Diseño, armado y pruebas de drones construidos por la división."),
        ],
    },
    {
        "archivo": "control-navegacion",
        "ancla": "sec-syn",
        "num": "03",
        "corto": "Control y Navegación",
        "titulo": "Control y Navegación",
        "titulo_grad": "para sistemas aeroespaciales",
        "intro": (
            "Desarrollamos métodos de modelado, control y automatización de sistemas "
            "dinámicos que garantizan su estabilidad, precisión y operación autónoma."
        ),
        "imagen": "divisiones/control-navegacion/portada.webp",
        "galeria": [
            ("divisiones/control-navegacion/cnc.webp",
             "Integrante de la división operando el software de control de una máquina CNC",
             "Control de una máquina CNC"),
            ("divisiones/control-navegacion/curso-vision.webp",
             "Sesión del curso de visión por computadora con una presentación proyectada",
             "Curso de visión por computadora: una foto es una hoja cuadriculada"),
            ("divisiones/control-navegacion/deteccion-color.webp",
             "Portátil mostrando una práctica de detección por color con la cámara",
             "Práctica: detección por color en tiempo real"),
        ],
        "badge": "Control · Guiado · Navegación",
        "lineas": [
            "Diseño de controladores y estrategias de estabilidad",
            "Guiado, navegación y estimación de estado",
            "Integración con aviónica y sistemas embebidos",
            "Simulación, pruebas y validación experimental",
        ],
        "lideres": [
            ("Jesús Santiago Moyan Vidal", "Líder", "jesus_vidal.jpg"),
            ("Jhoan Sebastian Parada Beltran", "Colíder", "Sebastian.png"),
        ],
        "proyectos": [
            ("Formación", "Control inteligente y visión por computadora",
             "Los líderes de la división están realizando un curso de control inteligente y "
             "visión por computadora para aplicarlo en los proyectos del capítulo. Las "
             "sesiones se publican en YouTube."),
        ],
        # Lista de YouTube del curso. Si el video no carga, revisa que el ID esté
        # completo: se copia de la URL, lo que va después de "list=" y antes de "&".
        "youtube_lista": "PLF_58DZqI98M",
        "youtube_titulo": "Curso de control inteligente y visión por computadora",
        # Logo de la división (ruta dentro de assets/images/). None = no se muestra.
        "logo": None,
        "temas": [
            ("Navegación y posicionamiento",
             "Determinar posición, velocidad y orientación de un vehículo con GNSS, IMU y otros sensores."),
            ("Lógica difusa (fuzzy logic)",
             "Controladores basados en reglas lingüísticas para sistemas no lineales o con incertidumbre."),
            ("Fusión de sensores",
             "Combinar mediciones de varios sensores para obtener una estimación más confiable que la de cada uno."),
            ("Estimación de estados",
             "Reconstruir variables que no se miden directamente a partir de datos ruidosos: observadores y filtros de Kalman."),
            ("Sistemas de control",
             "Diseño de controladores clásicos y modernos: PID, espacio de estados y control óptimo."),
            ("Modelado y simulación",
             "Modelos matemáticos de sistemas dinámicos y su validación en simulación antes de construir."),
            ("Automatización",
             "Integrar sensores, actuadores y lógica para que un proceso opere de forma autónoma."),
            ("Control de vehículos aeroespaciales",
             "Guiado, navegación y control (GNC) de cohetes, drones y satélites."),
        ],
        # Integrantes (además de los líderes): (nombre, programa o rol, foto en assets/images/ o None)
        "integrantes": [],
    },
    {
        "archivo": "percepcion-sensores-comunicaciones",
        "ancla": "sec-cyc",
        "num": "04",
        "corto": "Percepción y Sensores",
        "titulo": "Percepción, Sensores",
        "titulo_grad": "y Comunicaciones",
        "intro": (
            "Desarrollo de sistemas de sensores, visión artificial y enlaces de comunicación "
            "para la telemetría y el monitoreo de los proyectos del capítulo."
        ),
        "imagen": "psc.jpeg",
        "badge": "Sensores · Visión · Enlaces",
        "lineas": [
            "Integración y calibración de sensores",
            "Visión artificial y percepción del entorno",
            "Telemetría, radioenlaces y comunicación",
            "Monitoreo de variables para proyectos aeroespaciales",
        ],
        "lideres": [
            ("Evelyn Karina Velasco", "Colíder", None),
        ],
        "proyectos": [
            ("Investigación", "Filtro de Kalman",
             "Construcción del marco teórico sobre el filtro de Kalman para la estimación y "
             "fusión de datos de sensores."),
        ],
    },
]


def iniciales(nombre):
    partes = [p for p in nombre.split() if p]
    return (partes[0][0] + (partes[2][0] if len(partes) > 2 else partes[-1][0])).upper()


def tabs(activa):
    items = []
    for d in DIVISIONES:
        actual = ' aria-current="page"' if d is activa else ""
        items.append(
            f'<a href="{d["archivo"]}.html" class="division-tab"{actual}>'
            f'<span class="division-tab__num">{d["num"]}</span>'
            f'<span class="division-tab__name">{escape(d["corto"])}</span></a>'
        )
    return (
        '<div class="division-tabs" role="navigation" aria-label="Divisiones del capítulo">\n'
        + "\n".join("                    " + i for i in items)
        + "\n                </div>"
    )


def lider(nombre, rol, foto):
    if foto:
        avatar = (f'<img class="division-leader__photo" src="../../assets/images/lideres/{foto}" '
                  f'alt="{escape(nombre)}" loading="lazy">')
    else:
        avatar = f'<span class="division-leader__photo division-leader__photo--initials" aria-hidden="true">{iniciales(nombre)}</span>'
    return (f'<li class="division-leader">{avatar}'
            f'<span class="division-leader__name">{escape(nombre)}</span>'
            f'<span class="division-leader__role">{escape(rol)}</span></li>')


def tarjeta_persona(nombre, detalle, foto):
    if foto:
        avatar = (f'<img class="division-member__photo" src="../../assets/images/{foto}" '
                  f'alt="{escape(nombre)}" loading="lazy">')
    else:
        avatar = f'<span class="division-member__photo division-member__photo--initials" aria-hidden="true">{iniciales(nombre)}</span>'
    det = f'<span class="division-member__detail">{escape(detalle)}</span>' if detalle else ""
    return f'<li class="division-member">{avatar}<span class="division-member__name">{escape(nombre)}</span>{det}</li>'


def version_assets(html):
    m = re.search(r'main\.css\?v=(\d+)', html)
    return m.group(1) if m else "1"


def pagina(d, v):
    i = DIVISIONES.index(d)
    ant, sig = DIVISIONES[i - 1], DIVISIONES[(i + 1) % len(DIVISIONES)]
    chips = "\n".join(f'                                <li>{escape(l)}</li>' for l in d["lineas"])
    lideres = "\n".join(f"                                {lider(*l)}" for l in d["lideres"])
    proyectos = "\n".join(
        f'''                    <a class="division-project" href="../proyectos.html">
                        <span class="division-project__tag">{escape(tag)}</span>
                        <h3>{escape(nombre)}</h3>
                        <p>{escape(texto)}</p>
                    </a>''' for tag, nombre, texto in d["proyectos"])
    video = ""
    if d.get("youtube_lista"):
        lista = escape(d["youtube_lista"])
        titulo_lista = escape(d["youtube_titulo"])
        video = f'''
                <section class="division-video">
                    <div class="section-meta">Videos del curso</div>
                    <div class="yt-playlist" data-youtube-list="{lista}" data-src="../../shared/data/youtube/{lista}.json">
                        <div class="yt-playlist__head">
                            <div>
                                <span class="yt-playlist__kicker">Lista de reproducción</span>
                                <h3>{titulo_lista}</h3>
                                <span class="yt-playlist__count"></span>
                            </div>
                            <a class="yt-playlist__more" href="https://www.youtube.com/playlist?list={lista}" target="_blank" rel="noopener">Ver en YouTube &rarr;</a>
                        </div>
                        <div class="yt-playlist__body">
                            <div class="yt-playlist__player">
                                <iframe src="https://www.youtube-nocookie.com/embed/videoseries?list={lista}&amp;rel=0"
                                        title="{titulo_lista}" loading="lazy"
                                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                                        referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
                            </div>
                            <div class="yt-playlist__side" hidden>
                                <ol class="yt-playlist__list"></ol>
                            </div>
                        </div>
                    </div>
                    <script src="../../shared/scripts/youtube-playlist.js?v={v}" defer></script>
                </section>
'''
    galeria = ""
    if d.get("galeria"):
        items = "\n".join(
            f'''                        <button type="button" class="division-gallery__item" data-full="../../assets/images/{foto}" data-caption="{escape(pie)}">
                            <img src="../../assets/images/{foto}" alt="{escape(alt)}" loading="lazy">
                            <span class="division-gallery__caption">{escape(pie)}</span>
                        </button>''' for foto, alt, pie in d["galeria"])
        galeria = f'''
                <section class="division-gallery">
                    <div class="section-meta">Galería de la división</div>
                    <div class="division-gallery__grid">
{items}
                    </div>
                    <dialog class="division-lightbox" id="division-lightbox" aria-label="Foto ampliada">
                        <button type="button" class="division-lightbox__btn division-lightbox__close" data-accion="cerrar" aria-label="Cerrar">&times;</button>
                        <button type="button" class="division-lightbox__btn division-lightbox__prev" data-accion="anterior" aria-label="Foto anterior">&larr;</button>
                        <figure>
                            <img src="" alt="">
                            <figcaption></figcaption>
                        </figure>
                        <button type="button" class="division-lightbox__btn division-lightbox__next" data-accion="siguiente" aria-label="Foto siguiente">&rarr;</button>
                    </dialog>
                    <script src="../../shared/scripts/division-gallery.js?v={v}" defer></script>
                </section>
'''
    temas = ""
    if d.get("temas"):
        cards = "\n".join(
            f'''                        <li class="division-topic">
                            <span class="division-topic__num">{i:02d}</span>
                            <h3>{escape(nombre)}</h3>
                            <p>{escape(texto)}</p>
                        </li>''' for i, (nombre, texto) in enumerate(d["temas"], 1))
        temas = f'''
                <section class="division-topics">
                    <div class="section-meta">Temas de interés</div>
                    <p class="division-topics__intro">Áreas que la división puede abordar en sus proyectos, cursos e investigación.</p>
                    <ul class="division-topic-grid">
{cards}
                    </ul>
                </section>
'''
    miembros = ""
    if "integrantes" in d:
        personas = [(n, r, f"lideres/{f}" if f else None) for n, r, f in d["lideres"]] + list(d["integrantes"])
        lis = "\n".join(f"                        {tarjeta_persona(*p)}" for p in personas)
        miembros = f'''
                <section class="division-members">
                    <div class="section-meta">Integrantes · {len(personas)}</div>
                    <ul class="division-member-grid">
{lis}
                    </ul>
                </section>
'''
    logo = ""
    if d.get("logo"):
        logo = f'<img class="division-page__logo" src="../../assets/images/{d["logo"]}" alt="Logo de la división {escape(d["titulo"])}">'
    titulo_lideres = "Quiénes la lideran" if len(d["lideres"]) > 1 else "Quién la lidera"
    titulo_proyectos = "En qué estamos trabajando"
    return f'''<div class="division-page">
                {tabs(d)}

                <div class="division-page__intro{' has-logo' if logo else ''}">
                    {logo}
                    <span class="eyebrow">División {d["num"]}</span>
                    <h1>{escape(d["titulo"])} <span class="grad">{escape(d["titulo_grad"])}</span></h1>
                    <p>{escape(d["intro"])}</p>
                </div>

                <div class="division-hero">
                    <div class="division-hero__media">
                        <div class="division-hero__img" style="background-image:url('../../assets/images/{d["imagen"]}')"></div>
                        <div class="division-hero__tint"></div>
                        <div class="division-hero__shade"></div>
                        <div class="division-hero__badge">{escape(d["badge"])}</div>
                    </div>

                    <div class="division-summary">
                        <section class="division-summary__block">
                            <h2>Líneas de trabajo</h2>
                            <ul class="division-lines">
{chips}
                            </ul>
                        </section>

                        <section class="division-summary__block">
                            <h2>{titulo_lideres}</h2>
                            <ul class="division-leaders">
{lideres}
                            </ul>
                        </section>
                    </div>
                </div>

                <section class="division-projects">
                    <div class="section-meta">{titulo_proyectos}</div>
                    <div class="division-project-grid">
{proyectos}
                    </div>
                </section>
{temas}{video}{galeria}{miembros}
                <section class="division-join">
                    <div>
                        <span class="eyebrow">Convocatorias abiertas</span>
                        <h2>¿Quieres sumarte a la división?</h2>
                        <p>Postúlate a nuestras convocatorias y participa en proyectos reales de investigación, desarrollo e innovación aeroespacial.</p>
                    </div>
                    <div class="division-cta">
                        <a href="{FORM_POSTULACION}" class="division-btn division-btn--primary" target="_blank" rel="noopener">Postularme &rarr;</a>
                        <a href="../proyectos.html" class="division-btn division-btn--secondary">Ver todos los proyectos</a>
                    </div>
                </section>

                <div class="division-pager" role="navigation" aria-label="Otras divisiones">
                    <a href="{ant["archivo"]}.html" class="division-pager__link">
                        <span>&larr; División {ant["num"]}</span>
                        <strong>{escape(ant["corto"])}</strong>
                    </a>
                    <a href="../divisiones.html#{d["ancla"]}" class="division-pager__all">Todas las divisiones</a>
                    <a href="{sig["archivo"]}.html" class="division-pager__link division-pager__link--next">
                        <span>División {sig["num"]} &rarr;</span>
                        <strong>{escape(sig["corto"])}</strong>
                    </a>
                </div>
            </div>
        </div>'''


PATRON = re.compile(r'<div class="division-page">.*?</div>\s*</div>\s*(?=</section>)', re.S)

for d in DIVISIONES:
    ruta = RAIZ / "pages" / "divisiones" / f'{d["archivo"]}.html'
    html = ruta.read_text(encoding="utf-8")
    v = version_assets(html)
    nuevo, n = PATRON.subn(lambda _m: pagina(d, v) + "\n    ", html, count=1)
    if n != 1:
        raise SystemExit(f"No encontré el bloque .division-page en {ruta}")
    ruta.write_text(nuevo, encoding="utf-8")
    print("actualizada", ruta.relative_to(RAIZ))
