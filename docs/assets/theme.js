/* Apply the saved palette before the stylesheet paints the page. */
(() => {
  'use strict';
  const storageKey = 'kc-portfolio-theme';
  const themes = ['light', 'dark', 'paper', 'midnight', 'terminal', 'system'];
  const systemDark = window.matchMedia('(prefers-color-scheme: dark)');
  let preference = 'light';
  try {
    const stored = localStorage.getItem(storageKey);
    if (themes.includes(stored)) preference = stored;
  } catch (_) { /* The selector still works when browser storage is unavailable. */ }

  function applyTheme() {
    document.documentElement.dataset.theme = preference === 'system'
      ? (systemDark.matches ? 'dark' : 'light')
      : preference;
  }
  applyTheme();

  systemDark.addEventListener('change', () => {
    if (preference === 'system') applyTheme();
  });

  document.addEventListener('DOMContentLoaded', () => {
    const picker = document.querySelector('[data-theme-picker]');
    const select = document.querySelector('#theme-choice');
    if (!picker || !select) return;
    select.value = preference;
    picker.hidden = false;
    select.addEventListener('change', () => {
      if (!themes.includes(select.value)) return;
      preference = select.value;
      applyTheme();
      try { localStorage.setItem(storageKey, preference); } catch (_) { /* Optional persistence. */ }
    });
    window.addEventListener('storage', (event) => {
      if (event.key !== storageKey && event.key !== null) return;
      preference = themes.includes(event.newValue) ? event.newValue : 'light';
      select.value = preference;
      applyTheme();
    });
  });
})();
