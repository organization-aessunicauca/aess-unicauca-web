/* ==========================================================
   GALERÍA DE DIVISIÓN
   Abre las fotos de .division-gallery en un visor (<dialog>) con
   anterior / siguiente, teclado (← → Esc) y cierre al tocar fuera.
   ========================================================== */
(function () {
  const galeria = document.querySelector('.division-gallery__grid');
  const visor = document.getElementById('division-lightbox');
  if (!galeria || !visor || typeof visor.showModal !== 'function') return;

  const fotos = [...galeria.querySelectorAll('.division-gallery__item')];
  const img = visor.querySelector('img');
  const pie = visor.querySelector('figcaption');
  let actual = 0;

  function mostrar(i) {
    actual = (i + fotos.length) % fotos.length;
    const f = fotos[actual];
    img.src = f.dataset.full;
    img.alt = f.querySelector('img').alt;
    pie.textContent = f.dataset.caption || '';
  }

  fotos.forEach((f, i) => f.addEventListener('click', () => { mostrar(i); visor.showModal(); }));
  visor.querySelector('[data-accion="cerrar"]').addEventListener('click', () => visor.close());
  visor.querySelector('[data-accion="anterior"]').addEventListener('click', () => mostrar(actual - 1));
  visor.querySelector('[data-accion="siguiente"]').addEventListener('click', () => mostrar(actual + 1));
  visor.addEventListener('click', (e) => { if (e.target === visor) visor.close(); });
  visor.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') mostrar(actual + 1);
    if (e.key === 'ArrowLeft') mostrar(actual - 1);
  });
})();
