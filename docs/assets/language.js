(() => {
  'use strict';
  const key = 'kc-portfolio-language';
  const root = new URL('../', document.currentScript.src);
  const path = window.location.pathname.slice(root.pathname.length);
  if (path === '' || path === 'index.html') {
    try {
      if (localStorage.getItem(key) === 'pl') {
        const target = new URL('pl/', root);
        target.hash = window.location.hash;
        target.search = window.location.search;
        window.location.replace(target.href);
      }
    } catch (_) { /* Direct language links also work without storage. */ }
  }
  document.addEventListener('DOMContentLoaded', () => {
    const links = [...document.querySelectorAll('[data-language-switch]')];
    function updateFragments() {
      links.forEach(link => {
        const target = new URL(link.href);
        target.hash = window.location.hash;
        link.href = target.href;
      });
    }
    updateFragments();
    window.addEventListener('hashchange', updateFragments);
    links.forEach(link => {
      link.addEventListener('click', event => {
        if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        try { localStorage.setItem(key, link.dataset.languageSwitch); } catch (_) { /* Optional preference. */ }
      });
    });
  });
})();
