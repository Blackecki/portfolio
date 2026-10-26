/* Only the explicit download link uses this; other CV links remain previews. */
document.addEventListener('DOMContentLoaded', () => {
  const link = document.querySelector('[data-cv-download]');
  const status = document.querySelector('[data-download-status]');
  const row = document.querySelector('[data-cv-download-row]');
  const indicator = document.querySelector('[data-download-indicator]');
  if (!link || !status || !row || !indicator) return;
  let busy = false;
  let resetTimer;
  function feedback(state, message, hint) {
    row.dataset.state = state;
    status.textContent = message;
    indicator.title = hint;
  }
  link.addEventListener('click', async event => {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    if (busy) return;
    busy = true;
    clearTimeout(resetTimer);
    link.setAttribute('aria-disabled', 'true');
    link.setAttribute('aria-busy', 'true');
    feedback('loading', 'Preparing your download…', 'Preparing download');
    try {
      const response = await fetch(link.href, { credentials: 'same-origin' });
      if (!response.ok) throw new Error('PDF unavailable');
      const bytes = await response.arrayBuffer();
      const signature = new Uint8Array(bytes, 0, Math.min(5, bytes.byteLength));
      if (String.fromCharCode(...signature) !== '%PDF-') throw new Error('Invalid PDF');
      // A binary blob avoids browsers routing the link into their PDF viewer.
      const url = URL.createObjectURL(new Blob([bytes], { type: 'application/octet-stream' }));
      const save = document.createElement('a');
      save.href = url;
      save.download = link.download;
      save.hidden = true;
      document.body.append(save);
      save.click();
      save.remove();
      setTimeout(() => URL.revokeObjectURL(url), 30000);
      feedback('success', 'Download requested. Check your browser’s downloads.', 'Download requested');
      resetTimer = setTimeout(() => feedback('idle', '', 'Download PDF'), 4000);
    } catch (_) {
      feedback('error', 'Could not download the CV. Please try again.', 'Download failed. Click the link to try again.');
    } finally {
      busy = false;
      link.removeAttribute('aria-disabled');
      link.removeAttribute('aria-busy');
    }
  });
});
