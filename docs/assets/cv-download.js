/* Only the explicit download link uses this; other CV links remain previews. */
document.addEventListener('DOMContentLoaded', () => {
  const link = document.querySelector('[data-cv-download]');
  const status = document.querySelector('[data-download-status]');
  if (!link || !status) return;
  let busy = false;
  link.addEventListener('click', async event => {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    if (busy) return;
    busy = true;
    link.setAttribute('aria-disabled', 'true');
    status.textContent = 'Preparing your download…';
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
      status.textContent = 'Download requested. Check your browser’s downloads.';
    } catch (_) {
      status.textContent = 'Could not download the CV. Please try again.';
    } finally {
      busy = false;
      link.removeAttribute('aria-disabled');
    }
  });
});
