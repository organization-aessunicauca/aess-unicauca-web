/* ==========================================================
   LISTA DE REPRODUCCIÓN DE YOUTUBE
   Convierte cada .yt-playlist en un reproductor con la lista de
   videos al lado (miniatura, número, título y fecha).

   Los videos salen de shared/data/youtube/<ID>.json, que GitHub
   Actions actualiza a diario (tools/youtube/actualizar_listas.py).
   Si ese archivo todavía no existe, queda el reproductor de YouTube
   con su propia lista, sin romper nada.
   ========================================================== */
(function () {
  const fecha = new Intl.DateTimeFormat('es-CO', { day: 'numeric', month: 'short', year: 'numeric' });

  function embed(lista, video, autoplay) {
    const base = 'https://www.youtube-nocookie.com/embed/';
    const params = new URLSearchParams({ list: lista, rel: '0' });
    if (autoplay) params.set('autoplay', '1');
    return video ? `${base}${video}?${params}` : `${base}videoseries?${params}`;
  }

  function iniciar(widget) {
    const lista = widget.dataset.youtubeList;
    const iframe = widget.querySelector('iframe');
    const lado = widget.querySelector('.yt-playlist__side');
    const ol = widget.querySelector('.yt-playlist__list');
    const contador = widget.querySelector('.yt-playlist__count');
    if (!lista || !iframe || !lado || !ol) return;

    fetch(widget.dataset.src, { cache: 'no-cache' })
      .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
      .then((datos) => {
        const videos = (datos.videos || []).filter((v) => v.id);
        if (!videos.length) return;

        if (contador) contador.textContent = `${videos.length} ${videos.length === 1 ? 'video' : 'videos'}`;

        const botones = videos.map((v, i) => {
          const li = document.createElement('li');
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'yt-playlist__item';

          const thumb = document.createElement('span');
          thumb.className = 'yt-playlist__thumb';
          const img = document.createElement('img');
          img.src = `https://i.ytimg.com/vi/${encodeURIComponent(v.id)}/mqdefault.jpg`;
          img.alt = '';
          img.loading = 'lazy';
          const num = document.createElement('span');
          num.className = 'yt-playlist__num';
          num.textContent = String(i + 1).padStart(2, '0');
          thumb.append(img, num);

          const texto = document.createElement('span');
          texto.className = 'yt-playlist__text';
          const titulo = document.createElement('span');
          titulo.className = 'yt-playlist__title';
          titulo.textContent = v.titulo || `Video ${i + 1}`;
          texto.append(titulo);
          if (v.publicado) {
            const f = document.createElement('span');
            f.className = 'yt-playlist__date';
            f.textContent = fecha.format(new Date(`${v.publicado}T12:00:00`));
            texto.append(f);
          }

          btn.append(thumb, texto);
          btn.addEventListener('click', () => reproducir(i, true));
          li.append(btn);
          ol.append(li);
          return btn;
        });

        function reproducir(i, autoplay) {
          iframe.src = embed(lista, videos[i].id, autoplay);
          iframe.title = videos[i].titulo || iframe.title;
          botones.forEach((b, j) => {
            b.classList.toggle('is-active', j === i);
            if (j === i) b.setAttribute('aria-current', 'true');
            else b.removeAttribute('aria-current');
          });
        }

        reproducir(0, false);
        lado.hidden = false;
        widget.classList.add('has-list');
      })
      .catch(() => { /* sin datos: se queda el reproductor de YouTube */ });
  }

  document.querySelectorAll('.yt-playlist[data-youtube-list]').forEach(iniciar);
})();
