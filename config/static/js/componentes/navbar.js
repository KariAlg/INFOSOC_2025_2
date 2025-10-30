// static/js/componentes/navbar.js
(() => {
  const openBtn = document.getElementById('open-sidebar-button');
  const closeBtn = document.getElementById('close-sidebar-button');
  const overlay = document.getElementById('overlay');

  const open = () => { document.body.classList.add('nav-open'); openBtn?.setAttribute('aria-expanded','true'); };
  const close = () => { document.body.classList.remove('nav-open'); openBtn?.setAttribute('aria-expanded','false'); };

  openBtn?.addEventListener('click', (e)=>{ e.preventDefault(); open(); });
  closeBtn?.addEventListener('click', (e)=>{ e.preventDefault(); close(); });
  overlay?.addEventListener('click', close);

  // Cierra menú si cambias a desktop
  window.addEventListener('resize', () => { if (window.innerWidth >= 1024) close(); });
})();
