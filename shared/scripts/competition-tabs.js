/* ==========================================================
   PESTAÑAS POR AÑO (equipos de competencia)
   Sin JavaScript se ven todos los años, uno debajo de otro.
   Con JavaScript se muestra un año a la vez; se navega con clic
   o con las flechas ← → / Inicio / Fin del teclado.
   ========================================================== */
(function () {
  const lista = document.querySelector('.comp-tabs[role="tablist"]');
  if (!lista) return;
  const tabs = [...lista.querySelectorAll('[role="tab"]')];
  const paneles = tabs.map((t) => document.getElementById(t.getAttribute('aria-controls')));
  if (!tabs.length || paneles.some((p) => !p)) return;

  document.querySelector('.competitions')?.classList.add('has-tabs');

  function activar(i, enfocar) {
    tabs.forEach((t, j) => {
      const activo = j === i;
      t.setAttribute('aria-selected', String(activo));
      t.tabIndex = activo ? 0 : -1;
      paneles[j].hidden = !activo;
    });
    if (enfocar) tabs[i].focus();
  }

  tabs.forEach((t, i) => {
    t.addEventListener('click', () => activar(i, false));
    t.addEventListener('keydown', (e) => {
      const n = tabs.length;
      const destino = { ArrowRight: (i + 1) % n, ArrowLeft: (i - 1 + n) % n, Home: 0, End: n - 1 }[e.key];
      if (destino === undefined) return;
      e.preventDefault();
      activar(destino, true);
    });
  });

  activar(0, false);
})();
