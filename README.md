# AESS Unicauca Web

Sitio web oficial del Capítulo Estudiantil IEEE AESS Unicauca — [aessunicauca.com](https://aessunicauca.com).

## Créditos

**Diseño, contenido y desarrollo principal:** Sarah Cabeza

Con aportes de:

- **Jhojan Orozco**: reorganización de carpetas y estructura del código (`shared/`, `styles/`), footer compartido y páginas de divisiones
- **Andrés Muñoz**: página 404 y ajustes de estilos y rutas
- **Juan Alejandro**: SEO, dominio propio y página de inicio en la raíz

Advisor IEEE AESS Unicauca: Hernán Tobar

Este proyecto está organizado como un sitio estático con HTML, CSS y JavaScript vanilla. Durante la reorganización reciente se centralizaron los estilos en `styles/` y los scripts reutilizables en `shared/` para que el proyecto sea más legible, escalable y fácil de mantener.

## Estructura del proyecto

```text
aess-unicauca-web/
├── assets/
│   ├── icons/
│   └── images/
│       ├── carruselvert/
│       ├── eventos/
│       ├── galeria/
│       ├── historia/
│       ├── lideres/
│       ├── logos/
│       ├── nasa/
│       ├── noticias/
│       └── proyectos/
├── pages/
│   ├── historia.html
│   ├── divisiones.html
│   ├── proyectos.html
│   ├── eventos.html
│   ├── noticias.html
│   ├── galeria.html
│   ├── nosotros.html
│   ├── nasa.html
│   ├── divisiones/
│   │   ├── astronomia.html
│   │   ├── control-navegacion.html
│   │   ├── percepcion-sensores-comunicaciones.html
│   │   └── sistemas-inteligentes.html
│   ├── galery/
│   │   ├── g2020.html
│   │   ├── g2021.html
│   │   ├── g2022.html
│   │   ├── g2023.html
│   │   ├── g2024.html
│   │   └── g2025.html
│   ├── history/
│   │   ├── 2020.html
│   │   ├── 2021.html
│   │   ├── 2022.html
│   │   ├── 2023.html
│   │   ├── 2024.html
│   │   └── 2025.html
│   └── nasaspace/
│       ├── nasa2021.html
│       ├── nasa2022.html
│       ├── nasa2023.html
│       ├── nasa2024.html
│       └── nasa2025.html
├── shared/
│   └── scripts/
│       ├── nav.js
│       ├── footer.js
│       ├── timeline.js
│       ├── board-slideshow.js
│       ├── memory-gallery.js
│       └── photo-gallery.js
├── styles/
│   ├── main.css
│   ├── core.css
│   └── pages/
│       ├── divisiones.css
│       ├── division-detail.css
│       ├── galeria.css
│       ├── history.css
│       ├── nasa.css
│       ├── noticias.css
│       ├── not-found.css
│       └── proyectos.css
├── index.html          ← página de inicio
├── 404.html
├── sitemap.xml, robots.txt, CNAME
└── README.md
```

## Cómo funciona la navegación

La página de inicio es `index.html`, en la raíz. `pages/index.html` solo existe para redirigir enlaces antiguos a la raíz.

Las páginas principales dentro de `pages/` usan un nav compartido renderizado por:

- `shared/scripts/nav.js`

Las páginas anidadas, como:

- `pages/galery/*.html`
- `pages/history/*.html`
- `pages/nasaspace/*.html`

también usan el mismo nav compartido, pero pasando `data-root="../"` para corregir rutas relativas.

## Organización de estilos

El proyecto ya no usa un único `style.css` gigante en la raíz. Ahora los estilos están centralizados así:

- `styles/main.css`: punto de entrada único
- `styles/core.css`: estilos compartidos globales
- `styles/pages/`: estilos por área o sección

### Convención actual

- Todo HTML debe enlazar únicamente `styles/main.css`
- Los estilos globales o reutilizables deben ir a `core.css`
- Los estilos propios de una sección deben ir a `styles/pages/*.css`
- Si un bloque crece demasiado o empieza a repetirse, conviene fragmentarlo en más módulos

## Organización de scripts compartidos

Los scripts reutilizables se movieron a `shared/scripts/`.

### Scripts actuales

- `nav.js`
  - renderiza el menú lateral
  - marca la página activa
  - dibuja los iconos de redes sociales
  - controla la apertura/cierre en móvil

- `timeline.js`
  - controla el comportamiento de la línea de tiempo donde aplica

- `memory-gallery.js`
  - construye el mosaico de galerías anuales en `pages/galery/`
  - agrupa fotos por actividad
  - rota imágenes con transición suave
  - abre lightbox

- `photo-gallery.js`
  - construye la galería tipo mosaico de páginas NASA
  - genera tarjetas, numeración y lightbox

## Cómo editar cada parte del sitio

### 1. Páginas principales

Archivos:

- `index.html` (inicio)
- `pages/historia.html`
- `pages/divisiones.html`
- `pages/proyectos.html`
- `pages/eventos.html`
- `pages/noticias.html`
- `pages/galeria.html`
- `pages/nosotros.html`
- `pages/nasa.html`

Aquí se edita el contenido general de cada sección.

### 2. Galerías por año

Archivos:

- `pages/galery/g2020.html`
- `pages/galery/g2021.html`
- `pages/galery/g2022.html`
- `pages/galery/g2023.html`
- `pages/galery/g2024.html`
- `pages/galery/g2025.html`

Cada una contiene:

- el contenido editorial del año
- un bloque de datos con las fotos

Ese bloque se ve así:

```html
<script id="memory-gallery-data" type="text/plain">
[
  { src: '../../assets/images/galeria/g2020/fund.jpeg', alt: '...', caption: '...', activity: '...', span: 'span-2x2' }
]
</script>
```

Importante:

- `src` debe apuntar a un archivo real en `assets/images/galeria/...`
- `span` es opcional
- `activity` se usa para agrupar fotos que rotan en una misma tarjeta

### 3. Galerías NASA

Archivos:

- `pages/nasaspace/nasa2021.html`
- `pages/nasaspace/nasa2022.html`
- `pages/nasaspace/nasa2023.html`
- `pages/nasaspace/nasa2024.html`
- `pages/nasaspace/nasa2025.html`

Estas páginas usan un bloque similar:

```html
<script id="photo-gallery-data" type="text/plain">
[
  { src: '../../assets/images/nasa/n2021/prin.jpeg', alt: '...', caption: '...' }
]
</script>
```

Ese bloque es procesado por `shared/scripts/photo-gallery.js`.

### 4. Historia anual

Archivos:

- `pages/history/2020.html`
- `pages/history/2021.html`
- `pages/history/2022.html`
- `pages/history/2023.html`
- `pages/history/2024.html`
- `pages/history/2025.html`

Comparten nav y estilos comunes, pero el contenido sigue siendo propio de cada año.

## Galería: detalles importantes

La galería fue una de las áreas más reorganizadas.

### Galería principal

Archivo:

- `pages/galeria.html`

Muestra las portadas por año usando tarjetas con `background-image`.

### Galerías anuales

Archivos:

- `pages/galery/g2020.html` a `g2025.html`

Usan:

- `memory-gallery.js`
- estilos en `styles/pages/galeria.css`

### Corrección aplicada recientemente

Se corrigió un bug donde las imágenes no aparecían porque el loader interpretaba mal el bloque de datos cuando empezaba con salto de línea. El parser compartido ahora evalúa el contenido correctamente envolviéndolo como expresión.

## Reglas de mantenimiento recomendadas

### CSS

- no volver a crear un `style.css` monolítico en raíz
- no duplicar `<link rel="stylesheet">` en una misma página
- si una regla solo aplica a una sección, moverla a `styles/pages/`

### JS

- si un script se repite en dos o más páginas, moverlo a `shared/scripts/`
- evitar lógica inline larga dentro del HTML
- preferir bloques de datos pequeños en HTML + loader compartido, en vez de duplicar lógica completa

### Assets

- usar nombres consistentes y evitar mezclar mayúsculas/minúsculas innecesariamente
- verificar que cada `src` o `background-image` apunte a un archivo existente
- si se reemplaza una imagen, mantener la ruta cuando sea posible para no romper referencias
- antes de subir fotos, reducirlas a un máximo de 1920 px de lado y guardarlas como JPG (calidad ~80). Una foto no debería pasar de ~500 KB. Usar PNG solo para logos o imágenes con transparencia

## Cómo probar cambios localmente

Como es un sitio estático, basta con abrir `index.html`. Para que las rutas se comporten igual que en el dominio, es mejor servir la carpeta:

```bash
python3 -m http.server 8000
```

y abrir `http://localhost:8000`.

Si haces cambios en CSS o JS:

- recarga con `Ctrl + F5`
- **antes de publicar, sube el número de versión** (`?v=AAAAMMDD`) que llevan
  `styles/main.css`, sus `@import` y los `<script>` de `shared/scripts/`. Si no
  se cambia, los navegadores de los visitantes pueden seguir usando el CSS
  viejo con el HTML nuevo y la página se ve desarmada. Para cambiarlo en
  todo el sitio:

```bash
V=$(date +%Y%m%d); grep -rlE '\?v=[0-9]+' --include=*.html --include=*.css . | xargs sed -i -E "s/\?v=[0-9]+/?v=$V/g"
```

Si una galería no aparece:

1. abrir la consola del navegador (F12): las fotos faltantes aparecen como aviso `[photo-gallery] Falta la foto`. Al visitante no se le muestra nada: la foto simplemente se oculta
2. revisar que el archivo exista en `assets/images/...`
3. revisar la ruta en el bloque `memory-gallery-data` o `photo-gallery-data`
4. revisar que el script compartido correspondiente siga enlazado

## Estado actual de la arquitectura

A fecha de miércoles 29 de julio de 2026, el proyecto quedó con esta base:

- estilos centralizados en `styles/`
- scripts compartidos centralizados en `shared/scripts/`
- navegación reutilizable
- galerías anuales con loader compartido
- galerías NASA con loader compartido

## Mejoras futuras recomendadas

Si se sigue escalando el sitio, los siguientes pasos recomendados son:

1. mover los datos de galerías a archivos dedicados dentro de `shared/data/`
2. separar aún más `core.css` en módulos como:
   - `base/`
   - `layout/`
   - `components/`
3. documentar una guía de nombres para imágenes y contenido anual
4. generar miniaturas para las galerías anuales: la de 2025 tiene 111 fotos y carga unos 19 MB
5. completar las crónicas NASA Space Apps 2022, 2023 y 2024 (hoy muestran "memoria en construcción") y el jurado y los ganadores de 2021

## Autoría en el historial de git

- `.mailmap` unifica las identidades con que se hicieron los commits. Por ejemplo, los commits firmados como "AESS Unicauca" desde los correos de Sarah aparecen como Sarah Cabeza en `git log`, `git shortlog` y `git blame`.
- `.git-blame-ignore-revs` lista los commits que solo movieron o renombraron archivos, para que `git blame` y la vista Blame de GitHub muestren a quien escribió cada línea y no a quien la movió. Para usarlo localmente:

```bash
git config blame.ignoreRevsFile .git-blame-ignore-revs
```
