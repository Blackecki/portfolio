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
    if (!picker) return;
    const summary = picker.querySelector('summary');
    const choices = [...picker.querySelectorAll('input[name="theme"]')];
    const currentName = picker.querySelector('[data-theme-name]');
    function syncControls() {
      choices.forEach(choice => { choice.checked = choice.value === preference; });
      currentName.textContent = preference.charAt(0).toUpperCase() + preference.slice(1);
    }
    function closePanel(restoreFocus = false) {
      picker.open = false;
      if (restoreFocus) summary.focus();
    }
    syncControls();
    picker.hidden = false;
    picker.addEventListener('change', (event) => {
      if (!choices.includes(event.target) || !themes.includes(event.target.value)) return;
      preference = event.target.value;
      applyTheme();
      syncControls();
      try { localStorage.setItem(storageKey, preference); } catch (_) { /* Optional persistence. */ }
    });
    picker.querySelector('[data-theme-close]').addEventListener('click', () => closePanel(true));
    document.addEventListener('pointerdown', event => {
      if (picker.open && !picker.contains(event.target)) closePanel();
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && picker.open) {
        event.preventDefault();
        closePanel(true);
      }
    });
    picker.addEventListener('focusout', event => {
      if (event.relatedTarget && !picker.contains(event.relatedTarget)) closePanel();
    });
    window.addEventListener('storage', (event) => {
      if (event.key !== storageKey && event.key !== null) return;
      preference = themes.includes(event.newValue) ? event.newValue : 'light';
      syncControls();
      applyTheme();
    });
  });
})();
