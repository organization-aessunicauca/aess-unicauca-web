/* ==========================================================
   MODELO SOCIETY · animación al entrar en pantalla
   Agrega .is-visible a [data-modelo] la primera vez que se ve.
   El CSS se encarga de la secuencia (núcleo, líneas, hexágonos,
   flecha y Transformación). Sin JavaScript, o con "reducir
   movimiento", la gráfica se muestra completa y quieta.
   ========================================================== */
(function () {
  const fig = document.querySelector('[data-modelo]');
  if (!fig) return;

  const reducir = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reducir || !('IntersectionObserver' in window)) {
    fig.classList.add('is-visible', 'is-static');
    return;
  }

  fig.classList.add('is-ready');            // estado inicial oculto, solo con JS
  const io = new IntersectionObserver((entradas) => {
    entradas.forEach((e) => {
      if (!e.isIntersecting) return;
      fig.classList.add('is-visible');
      io.disconnect();
    });
  }, { threshold: 0.25 });
  io.observe(fig);
})();
