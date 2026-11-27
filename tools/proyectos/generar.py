#!/usr/bin/env python3
"""
Genera el contenido de pages/proyectos.html a partir de tres tablas:

  CONVOCATORIAS  proyectos que están buscando integrantes
  COMPETENCIAS   equipos de competencia, agrupados por año
  LABS           proyectos de I+D (AESS Challenge Labs)

Uso, desde la raíz del repositorio:
    python3 tools/proyectos/generar.py

Solo se reemplaza el bloque <div class="proyectos-page"> ... </div>; el
<head> (título, SEO) de la página se conserva.
"""
from html import escape
from pathlib import Path
import re

RAIZ = Path(__file__).resolve().parents[2]
PAGINA = RAIZ / "pages" / "proyectos.html"
FORM_GENERAL = "https://forms.gle/ge2w6SF74GaRevaz9"

# ---------------------------------------------------------------------------
# CONVOCATORIAS ABIERTAS
# Cada una: titulo, division, descripcion, perfiles (lista), fecha_limite
# (texto libre o None) y enlace (None = formulario general).
# Lista vacía = se muestra un aviso de "próximas convocatorias".
# ---------------------------------------------------------------------------
CONVOCATORIAS = [
    # {
    #     "titulo": "Nombre del proyecto",
    #     "division": "Control y Navegación",
    #     "descripcion": "Qué se va a hacer y qué aprenderá quien entre.",
    #     "perfiles": ["Programación en Python", "Electrónica"],
    #     "fecha_limite": "15 de diciembre de 2026",
    #     "enlace": None,
    # },
]

# ---------------------------------------------------------------------------
# EQUIPOS DE COMPETENCIA (fuente: páginas de Historia de cada año)
# resultado: número de puesto (1, 2, 3...) o None si fue participación.
# area: Satélites, Cohetería, Hidrocohetería, Rovers, Hackatón, Radio...
# ---------------------------------------------------------------------------
COMPETENCIAS = {
    # "estado": "preparacion" = equipo rumbo a esa competencia (no cuenta en las cifras)
    2027: [
        {"equipo": "SPACS", "competencia": "Mundial de Satélites Enlatados CanSat (UNAM)", "lugar": "Ciudad de México",
         "fecha": None, "resultado": None, "categoria": None, "area": "Satélites", "estado": "preparacion",
         "detalle": "Misión Fobos 1."},
        {"equipo": "TulcánSat", "competencia": "Mundial de Satélites Enlatados CanSat (UNAM)", "lugar": "Ciudad de México",
         "fecha": None, "resultado": None, "categoria": None, "area": "Satélites", "estado": "preparacion",
         "detalle": "Misión TulcánSat."},
        {"equipo": "Atlas X", "competencia": "Latin American Space Challenge (LASC)", "lugar": None,
         "fecha": None, "resultado": None, "categoria": None, "area": "Cohetería", "estado": "preparacion",
         "detalle": "Equipo campeón del HidroChallenge IPN 2025."},
    ],
    2025: [
        {"equipo": "Atlas X", "competencia": "HidroChallenge IPN", "lugar": "Ciudad de México",
         "fecha": "Octubre", "resultado": 1, "categoria": None, "area": "Hidrocohetería",
         "detalle": "Hidrocohete con carga útil tipo CanSat. Invitado especial con stand propio en la Feria Aeroespacial de Ticomán."},
        {"equipo": "Flylejon", "competencia": "HidroChallenge IPN", "lugar": "Ciudad de México",
         "fecha": "Octubre", "resultado": None, "categoria": None, "area": "Hidrocohetería",
         "detalle": "Equipo de hidrocohetería del capítulo."},
        {"equipo": "Tulcán-Sat", "competencia": "Mundial de CanSat", "lugar": "Ciudad de México",
         "fecha": "Mayo", "resultado": 8, "categoria": None, "area": "Satélites",
         "detalle": "Octavo lugar entre equipos de todo el mundo. También estuvo presente en ENMICE."},
        {"equipo": "AirSat", "competencia": "ENMICE", "lugar": "Guadalajara, México",
         "fecha": "Noviembre", "resultado": 1, "categoria": "Picosatélites", "area": "Satélites",
         "detalle": "Primer puesto en la categoría de picosatélites."},
        {"equipo": "Astrek", "competencia": "ENMICE", "lugar": "Guadalajara, México",
         "fecha": "Noviembre", "resultado": 2, "categoria": "Carga útil", "area": "Rovers",
         "detalle": "Rover que obtuvo el segundo puesto en la categoría de carga útil."},
        {"equipo": "Katari X", "competencia": "ENMICE", "lugar": "Guadalajara, México",
         "fecha": "Noviembre", "resultado": None, "categoria": None, "area": "Cohetería",
         "detalle": "Cohete experimental de motor sólido con carga útil tipo CanSat."},
    ],
    2024: [
        {"equipo": "Tres equipos CanSat", "competencia": "Mundial de CanSat (PEU-UNAM)", "lugar": "Ciudad de México",
         "fecha": None, "resultado": None, "categoria": None, "area": "Satélites",
         "detalle": "Tres equipos del capítulo en el diseño, integración y validación de sistemas CanSat."},
    ],
    2023: [
        {"equipo": "Katari", "competencia": "Latin American Space Challenge (LASC)", "lugar": "Tatuí, Brasil",
         "fecha": None, "resultado": None, "categoria": None, "area": "Cohetería",
         "detalle": "Debut del equipo: cohete de motor sólido para un apogeo de 1000 m con un CanSat como carga útil."},
    ],
    2022: [
        {"equipo": "Sentinel", "competencia": "Ala Zagi Race AESS", "lugar": None,
         "fecha": None, "resultado": None, "categoria": "Inteligencia artificial", "area": "UAV",
         "detalle": "Ala volante tipo Zagi en la categoría de inteligencia artificial."},
        {"equipo": "Alpha Team", "competencia": "Mundial de CanSat (UNAM)", "lugar": "Ciudad de México",
         "fecha": None, "resultado": None, "categoria": None, "area": "Satélites",
         "detalle": "Representó a Colombia; equipo conformado en alianza con CREATIC."},
    ],
    2021: [
        {"equipo": "Icarus", "competencia": "CanSat Latinoamérica", "lugar": None,
         "fecha": "Octubre", "resultado": 1, "categoria": "Águilas", "area": "Satélites",
         "detalle": "CanSat para reconocimiento y búsqueda de personas con sensores atmosféricos y cámara."},
        {"equipo": "Alpha", "competencia": "CanSat Latinoamérica", "lugar": None,
         "fecha": "Octubre", "resultado": 2, "categoria": "Águilas", "area": "Satélites",
         "detalle": "CanSat para atención prehospitalaria y entrega aérea de suministros médicos."},
        {"equipo": "IIXU", "competencia": "CanSat Latinoamérica", "lugar": None,
         "fecha": "Octubre", "resultado": 5, "categoria": "Cóndores", "area": "Satélites",
         "detalle": "Relación entre calidad del aire, material particulado, lluvia y COVID-19."},
        {"equipo": "Sentinel", "competencia": "Ala Zagi Race AESS", "lugar": None,
         "fecha": None, "resultado": None, "categoria": "RF", "area": "UAV",
         "detalle": "Ala volante tipo Zagi en la categoría de radiofrecuencia (RF)."},
        {"equipo": "Team Crow", "competencia": "Rover Agricultor Latinoamérica", "lugar": None,
         "fecha": "Noviembre", "resultado": 2, "categoria": None, "area": "Rovers",
         "detalle": "Subcampeón, con estudiantes de Unicauca y Unicomfacauca."},
    ],
    2020: [
        {"equipo": "FireGoApp", "competencia": "NASA Space Apps Challenge", "lugar": "Sede Cali",
         "fecha": "Octubre", "resultado": 1, "categoria": None, "area": "Hackatón",
         "detalle": "Primer lugar local; clasificó a la competencia global."},
        {"equipo": "Convid to Plant", "competencia": "NASA Space Apps Challenge", "lugar": "Foz do Iguaçu, Brasil",
         "fecha": "Octubre", "resultado": 2, "categoria": None, "area": "Hackatón",
         "detalle": "Segundo lugar; clasificó a la competencia global."},
        {"equipo": "CarboKillers", "competencia": "NASA Space Apps Challenge", "lugar": "Sede Popayán",
         "fecha": "Octubre", "resultado": 3, "categoria": None, "area": "Hackatón",
         "detalle": "Tercer lugar entre los ganadores locales."},
        {"equipo": "Nathalia Ceballos", "competencia": "Concurso Mundial de Radio Experimentación IEEE AESS", "lugar": None,
         "fecha": "Septiembre", "resultado": 1, "categoria": "Individual", "area": "Radio",
         "detalle": "Diseño de circuito y de antena en simulación."},
        {"equipo": "AESS Unicauca", "competencia": "World CanSat / Rocketry Championship", "lugar": None,
         "fecha": None, "resultado": None, "categoria": "Fase cero", "area": "Satélites",
         "detalle": "Primera participación del capítulo en un campeonato mundial de CanSat."},
    ],
}

# ---------------------------------------------------------------------------
# CONFERENCIAS Y ENCUENTROS ACADÉMICOS en los que ha participado el capítulo
# (año, nombre, lugar o None, rol, detalle)
# ---------------------------------------------------------------------------
CONFERENCIAS = [
    (2024, "Summit Internacional de Presidentes IEEE AESS", None, "Organizadores",
     "Encuentro de líderes de capítulos estudiantiles IEEE AESS para compartir experiencias, proyectos y estrategias de crecimiento."),
    (2023, "Taller Nacional sobre Drones Inteligentes", "México", "Participantes",
     "Intercambio académico con el INAOE y el ITAM."),
    (2023, "Intercambio académico y tecnológico TICANOR", "Alemania", "Participantes",
     "Programa con Fraunhofer FKIE, CeADAR Ireland y la Universidad del Cauca."),
    (2020, "Congreso Internacional de TIC X-TECH", None, "Participantes",
     "El proyecto EXCELSO recibió mentorías de expertos en innovación."),
]

# ---------------------------------------------------------------------------
# AESS CHALLENGE LABS (I+D)
# ---------------------------------------------------------------------------
LABS = [
    ("Banco de pruebas de aviónica y gemelo digital", "proyectos/banco.jpg",
     "Plataforma de pruebas para sistemas de aviónica y su gemelo digital, con el Semillero de "
     "Ingeniería Aeroespacial (SIA) y el semillero ImmerseTech."),
    ("Sistema de Control Vectorial de Empuje (TVC)", "proyectos/control.jpeg",
     "Sistema TVC para cohetería experimental: tobera, actuadores, electrónica, instrumentación, "
     "algoritmos de control y validación experimental."),
    ("IA ligera para UAVs (Lightweight AI)", "proyectos/ialig.jpg",
     "Modelos de inferencia en tiempo real sobre plataformas embarcadas, optimizando memoria, "
     "procesamiento y consumo energético, con referencia al Challenge 2 de IEEE AESS."),
    ("Motores de propulsión tipo sólido", "proyectos/solido.jpeg",
     "Diseño y manufactura con simulación y validación experimental: desempeño, caracterización de "
     "materiales, fabricación, instrumentación y pruebas estáticas."),
]

ICONO_AREA = {
    "Satélites": "🛰️", "Cohetería": "🚀", "Hidrocohetería": "💧", "Rovers": "🤖",
    "Hackatón": "💻", "Radio": "📡", "UAV": "✈️",
}


def puesto(r, estado=None):
    if estado == "preparacion":
        return '<span class="comp-result comp-result--prep">En preparación</span>'
    if r is None:
        return '<span class="comp-result comp-result--part">Participación</span>'
    clase = {1: "gold", 2: "silver", 3: "bronze"}.get(r, "rank")
    texto = {1: "1.er lugar", 2: "2.º lugar", 3: "3.er lugar"}.get(r, f"{r}.º lugar")
    return f'<span class="comp-result comp-result--{clase}">{texto}</span>'


def tarjeta_competencia(c):
    meta = " · ".join(escape(x) for x in (c["lugar"], c["fecha"]) if x)
    cat = f'<span class="comp-card__cat">{escape(c["categoria"])}</span>' if c["categoria"] else ""
    icono = ICONO_AREA.get(c["area"], "⭐")
    clases = " is-podium" if c["resultado"] in (1, 2, 3) else ""
    if c.get("estado") == "preparacion":
        clases += " is-upcoming"
    return f'''                            <li class="comp-card{clases}">
                                <div class="comp-card__top">
                                    <span class="comp-card__area"><span aria-hidden="true">{icono}</span> {escape(c["area"])}</span>
                                    {puesto(c["resultado"], c.get("estado"))}
                                </div>
                                <h3>{escape(c["equipo"])}</h3>
                                <p class="comp-card__comp">{escape(c["competencia"])}{cat}</p>
                                {f'<p class="comp-card__meta">{meta}</p>' if meta else ''}
                                <p class="comp-card__detail">{escape(c["detalle"])}</p>
                            </li>'''


def seccion_convocatorias():
    if not CONVOCATORIAS:
        return f'''                <section class="calls" aria-labelledby="calls-title">
                    <div class="section-meta">Convocatorias abiertas</div>
                    <div class="calls-empty">
                        <div>
                            <span class="eyebrow">Próximas convocatorias</span>
                            <h2 id="calls-title">¿Quieres sumarte a un proyecto?</h2>
                            <p>Pronto abriremos convocatorias para los equipos y proyectos del capítulo. Déjanos tus datos y te avisamos cuando haya una que encaje con tu perfil.</p>
                        </div>
                        <a href="{FORM_GENERAL}" class="btn-solid" target="_blank" rel="noopener">Quiero participar &rarr;</a>
                    </div>
                </section>'''
    cards = []
    for c in CONVOCATORIAS:
        perfiles = "".join(f"<li>{escape(p)}</li>" for p in c.get("perfiles", []))
        fecha = (f'<p class="call-card__date">Cierra: <strong>{escape(c["fecha_limite"])}</strong></p>'
                 if c.get("fecha_limite") else "")
        cards.append(f'''                        <article class="call-card">
                            <span class="call-card__div">{escape(c.get("division") or "AESS Unicauca")}</span>
                            <h3>{escape(c["titulo"])}</h3>
                            <p>{escape(c["descripcion"])}</p>
                            {f'<p class="call-card__label">Buscamos</p><ul class="call-card__profiles">{perfiles}</ul>' if perfiles else ''}
                            {fecha}
                            <a href="{escape(c.get("enlace") or FORM_GENERAL)}" class="btn-solid" target="_blank" rel="noopener">Postularme &rarr;</a>
                        </article>''')
    return f'''                <section class="calls" aria-labelledby="calls-title">
                    <div class="section-meta">Convocatorias abiertas</div>
                    <h2 class="calls__title" id="calls-title">Proyectos que buscan integrantes</h2>
                    <div class="call-grid">
{chr(10).join(cards)}
                    </div>
                </section>'''


def nota_panel(anio):
    if all(c.get("estado") == "preparacion" for c in COMPETENCIAS[anio]):
        return (f'<p class="comp-panel__note"><span aria-hidden="true">🚀</span> Rumbo a {anio}: '
                f'equipos que ya se están preparando para competir.</p>')
    return ""


def seccion_conferencias():
    if not CONFERENCIAS:
        return ""
    items = "\n".join(f'''                        <li class="conf-item">
                            <span class="conf-item__year">{a}</span>
                            <div class="conf-item__body">
                                <h3>{escape(n)}</h3>
                                <p class="conf-item__meta">{" · ".join(escape(x) for x in (lugar, rol) if x)}</p>
                                <p>{escape(d)}</p>
                            </div>
                        </li>''' for a, n, lugar, rol, d in sorted(CONFERENCIAS, key=lambda x: -x[0]))
    return f'''                <section class="conferences" aria-labelledby="conf-title">
                    <div class="section-meta">Conferencias y encuentros</div>
                    <h2 class="conferences__title" id="conf-title">Conferencias en las que hemos participado</h2>
                    <ol class="conf-list">
{items}
                    </ol>
                </section>'''


def seccion_competencias():
    anios = sorted(COMPETENCIAS, reverse=True)
    todos = [c for a in anios for c in COMPETENCIAS[a] if c.get("estado") != "preparacion"]
    anios_compitiendo = sorted({a for a in anios for c in COMPETENCIAS[a] if c.get("estado") != "preparacion"})
    podios = sum(1 for c in todos if c["resultado"] in (1, 2, 3))
    primeros = sum(1 for c in todos if c["resultado"] == 1)
    tabs = "\n".join(
        f'''                        <button type="button" role="tab" class="comp-tab" id="tab-{a}" aria-controls="panel-{a}"
                                aria-selected="{'true' if i == 0 else 'false'}" tabindex="{0 if i == 0 else -1}">{a}<span class="comp-tab__n">{len(COMPETENCIAS[a])}</span></button>'''
        for i, a in enumerate(anios))
    paneles = "\n".join(
        f'''                    <div class="comp-panel" role="tabpanel" id="panel-{a}" aria-labelledby="tab-{a}" tabindex="0">
                        <h3 class="comp-panel__year">{a}</h3>
                        {nota_panel(a)}
                        <ul class="comp-grid">
{chr(10).join(tarjeta_competencia(c) for c in COMPETENCIAS[a])}
                        </ul>
                    </div>''' for a in anios)
    return f'''                <section class="competitions" aria-labelledby="comp-title">
                    <div class="section-meta">Equipos de competencia</div>
                    <h2 class="competitions__title" id="comp-title">Nuestros equipos en competencias</h2>
                    <ul class="comp-stats">
                        <li><strong>{len(todos)}</strong><span>participaciones</span></li>
                        <li><strong>{podios}</strong><span>podios</span></li>
                        <li><strong>{primeros}</strong><span>primeros lugares</span></li>
                        <li><strong>{len(anios_compitiendo)}</strong><span>años compitiendo</span></li>
                    </ul>
                    <div class="comp-tabs" role="tablist" aria-label="Año de competencia">
{tabs}
                    </div>
{paneles}
                </section>'''


def seccion_labs():
    cards = "\n".join(f'''                    <article class="lab-card">
                        <div class="lab-card__media">
                            <span class="lab-card__badge">I+D · En desarrollo</span>
                            <img src="../assets/images/{img}" alt="{escape(t)}" loading="lazy">
                        </div>
                        <div class="lab-card__body">
                            <h3>{escape(t)}</h3>
                            <p>{escape(d)}</p>
                        </div>
                    </article>''' for t, img, d in LABS)
    return f'''                <section class="labs" aria-labelledby="labs-title">
                    <div class="section-meta">AESS Challenge Labs</div>
                    <h2 class="labs__title" id="labs-title">Proyectos de investigación y desarrollo</h2>
                    <p class="lead">Iniciativas de I+D del capítulo para fortalecer competencias técnicas en aviónica, propulsión, control e inteligencia artificial aplicada.</p>
                    <div class="labs-grid">
{cards}
                    </div>
                </section>'''


def version_assets(html):
    m = re.search(r'main\.css\?v=(\d+)', html)
    return m.group(1) if m else "1"


def contenido(v):
    return f'''<div class="proyectos-page">

                <span class="eyebrow">Innovación aeroespacial</span>
                <h1>Proyectos <span class="grad">y equipos</span></h1>
                <p class="lead">
                    Equipos de competencia, proyectos de investigación y convocatorias abiertas del
                    Capítulo Estudiantil IEEE AESS Unicauca: satélites, cohetería, rovers, drones e
                    inteligencia artificial hechos por estudiantes.
                </p>

{seccion_convocatorias()}

{seccion_competencias()}

{seccion_conferencias()}

{seccion_labs()}

                <div class="project-cta">
                    <span class="project-cta__tag">Participa</span>
                    <h3>¿Tienes una idea o quieres unirte a un equipo?</h3>
                    <p>
                        Escríbenos por el formulario y te contamos cómo vincularte a las divisiones,
                        los equipos de competencia y los proyectos de I+D del capítulo.
                    </p>
                    <div class="project-cta__actions">
                        <a href="{FORM_GENERAL}" class="btn-solid" target="_blank" rel="noopener">Postularme &rarr;</a>
                        <a href="../index.html#participa" class="btn-outline">Ver todas las formas de participar</a>
                    </div>
                </div>

                <script src="../shared/scripts/competition-tabs.js?v={v}" defer></script>
            </div>'''


html = PAGINA.read_text(encoding="utf-8")
PATRON = re.compile(r'<div class="proyectos-page">.*?</div>\s*(?=</div>\s*</section>)', re.S)
nuevo, n = PATRON.subn(lambda _m: contenido(version_assets(html)) + "\n\n        ", html, count=1)
if n != 1:
    raise SystemExit("No encontré el bloque .proyectos-page en pages/proyectos.html")
PAGINA.write_text(nuevo, encoding="utf-8")
print("actualizada", PAGINA.relative_to(RAIZ))
