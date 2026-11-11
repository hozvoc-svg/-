// Free tools: AI generators (anonymous, limited like the landing demo) and the character counter.
(() => {
  const $ = (s, el = document) => el.querySelector(s);

  // AI tools: <form data-tool="hashtags|names"> with inputs named in data-fields, an output and a status.
  document.querySelectorAll('form[data-tool]').forEach((form) => {
    const out = $('[data-tool-output]', form.parentElement);
    const status = $('[data-tool-status]', form.parentElement);
    const button = $('button[type="submit"]', form);
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(form));
      if (!String(data.topic || '').trim()) { $('[name="topic"]', form).focus(); return; }
      const prompt = form.dataset.prompt.replace(/\{(\w+)\}/g, (_, k) => String(data[k] || '').trim());
      button.disabled = true;
      out.textContent = '';
      out.classList.add('is-typing');
      status.textContent = 'writing…';
      try {
        const res = await fetch('/api/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt, template: form.dataset.tool, language: data.language || 'English' }),
        });
        if (!res.ok) {
          const err = await res.json().catch(() => ({}));
          throw new Error(err.code === 'demo_limit'
            ? 'You’ve used your free tries for this hour. Create a free account to get 10 generations every month.'
            : 'This tool is not available right now. Please try again later.');
        }
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        for (;;) {
          const { done, value } = await reader.read();
          if (done) break;
          out.textContent += decoder.decode(value, { stream: true });
        }
        status.textContent = 'done ✓';
        $('[data-tool-copy]', form.parentElement).hidden = false;
      } catch (err) {
        out.textContent = err instanceof TypeError ? 'This tool is not available right now. Please try again later.' : err.message;
        status.textContent = '';
      } finally {
        out.classList.remove('is-typing');
        button.disabled = false;
      }
    });
    const copy = $('[data-tool-copy]', form.parentElement);
    copy?.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(out.textContent); copy.textContent = 'Copied ✓'; } catch (e) { copy.textContent = 'Select & copy'; }
      setTimeout(() => { copy.textContent = 'Copy'; }, 1500);
    });
  });

  // Character counter
  const input = $('#counterInput');
  if (input) {
    const rows = [...document.querySelectorAll('[data-limit]')];
    const segmenter = 'Segmenter' in Intl ? new Intl.Segmenter(undefined, { granularity: 'grapheme' }) : null;
    const countChars = (s) => (segmenter ? [...segmenter.segment(s)].length : [...s].length);
    const update = () => {
      const text = input.value;
      const chars = countChars(text);
      $('#statChars').textContent = chars.toLocaleString();
      $('#statNoSpaces').textContent = countChars(text.replace(/\s/g, '')).toLocaleString();
      $('#statWords').textContent = (text.trim() ? text.trim().split(/\s+/).length : 0).toLocaleString();
      $('#statLines').textContent = (text ? text.split('\n').length : 0).toLocaleString();
      $('#statHashtags').textContent = (text.match(/#[\p{L}\p{N}_]+/gu) || []).length;
      rows.forEach((row) => {
        const limit = Number(row.dataset.limit);
        const pct = Math.min(100, (chars / limit) * 100);
        row.style.setProperty('--pct', `${pct}%`);
        row.classList.toggle('is-over', chars > limit);
        $('.limit__left', row).textContent = chars > limit ? `${(chars - limit).toLocaleString()} over` : `${(limit - chars).toLocaleString()} left`;
      });
    };
    input.addEventListener('input', update);
    update();
  }
})();
