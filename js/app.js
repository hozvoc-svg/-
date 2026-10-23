// Muse studio (app.html): generate copy, refine it, track credits, history, business profile and upgrades.
// Interface text comes from js/ui-i18n.js (applied by js/main.js before this file runs).
(async () => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const UI = window.MuseUI;
  const t = (key) => UI.t(key);
  const PLAN_NAMES = { free: 'Free', creator: 'Creator', pro: 'Pro' };

  const output = $('#output');
  const status = $('#genStatus');
  const genBtn = $('#genBtn');
  const copyBtn = $('#copyBtn');
  const refine = $('#refine');
  const modal = $('#upgradeModal');
  const langSelect = $('#language');
  let template = 'ad';
  let last = null; // { prompt, template, tone, language, output } of the result on screen
  let session;

  const showEmpty = (key) => {
    const p = document.createElement('p');
    p.className = 'output__empty';
    p.textContent = t(key);
    output.replaceChildren(p);
  };

  try {
    session = await window.Muse.requireSession();
  } catch (err) {
    showEmpty('not_setup');
    genBtn.disabled = true;
    return;
  }

  // Text language: last choice, otherwise the interface language.
  try { langSelect.value = localStorage.getItem('muse-out-lang') || UI.outputLanguage; } catch (e) { langSelect.value = UI.outputLanguage; }
  langSelect.addEventListener('change', () => { try { localStorage.setItem('muse-out-lang', langSelect.value); } catch (e) {} });

  const setCredits = (n) => { $('#creditsCount').textContent = n; };

  const renderProfile = (p) => {
    const name = p.full_name || p.email.split('@')[0];
    $('#userName').textContent = name;
    $('#userEmail').textContent = p.email;
    $('#avatar').textContent = name.slice(0, 2).toUpperCase();
    $('#planName').textContent = PLAN_NAMES[p.plan] || p.plan;
    setCredits(p.credits);
    $('#upgradeBtn').hidden = p.plan === 'pro';
    const billing = $('#manageBilling');
    if (p.customer_portal_url) { billing.href = p.customer_portal_url; billing.hidden = false; }
    const brand = $('#brand');
    if (p.brand && !brand.value) { brand.value = p.brand; $('#brandBox').open = true; }
  };

  const loadProfile = async () => {
    const p = await window.Muse.profile();
    if (p) renderProfile(p);
    return p;
  };

  const tplName = (key) => t(`tpl_${key}`);

  const renderHistory = (items) => {
    const list = $('#history');
    list.replaceChildren();
    if (!items.length) {
      const li = document.createElement('li');
      li.className = 'output__empty';
      li.textContent = t('no_history');
      list.append(li);
      return;
    }
    items.forEach((g) => {
      const li = document.createElement('li');
      const btn = document.createElement('button');
      btn.type = 'button';
      const tag = document.createElement('span');
      tag.className = 'tag';
      tag.textContent = tplName(g.template);
      const text = document.createElement('span');
      text.className = 'history__prompt';
      text.dir = 'auto';
      text.textContent = g.prompt;
      const time = document.createElement('small');
      time.textContent = new Date(g.created_at).toLocaleString(UI.lang);
      btn.append(tag, text, time);
      btn.addEventListener('click', () => {
        output.textContent = g.output;
        last = { prompt: g.prompt, template: g.template, tone: $('#tone').value, language: langSelect.value, output: g.output };
        copyBtn.disabled = false;
        refine.hidden = false;
        status.textContent = '';
        output.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      });
      li.append(btn);
      list.append(li);
    });
  };

  const loadHistory = () => window.Muse.history().then(renderHistory).catch((e) => console.error(e));

  await loadProfile().catch((e) => console.error(e));
  loadHistory();

  // Template picker
  $$('.tpl').forEach((btn) => btn.addEventListener('click', () => {
    template = btn.dataset.template;
    $$('.tpl').forEach((b) => {
      const on = b === btn;
      b.classList.toggle('is-active', on);
      b.setAttribute('aria-checked', String(on));
    });
  }));

  // Business profile
  $('#brandSave').addEventListener('click', async () => {
    const msg = $('#brandMsg');
    try {
      await window.Muse.saveBrand($('#brand').value);
      msg.textContent = t('brand_saved');
    } catch (err) {
      msg.textContent = t(`err_${err.message}`);
    }
    setTimeout(() => { msg.textContent = ''; }, 2500);
  });

  // Generate (or refine the result on screen when `mode` is given)
  const run = async (request) => {
    genBtn.disabled = true;
    copyBtn.disabled = true;
    $$('button', refine).forEach((b) => { b.disabled = true; });
    output.textContent = '';
    output.classList.add('is-typing');
    status.textContent = t('writing');
    let text = '';
    try {
      session = (await window.Muse.session()) || session; // picks up refreshed tokens
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${session.access_token}` },
        body: JSON.stringify(request),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        if (err.code === 'no_credits') openUpgrade(t('out_of_credits'));
        if (err.code === 'auth') { window.Muse.signOut(); return; }
        throw new Error(t(`err_${err.code || 'server'}`));
      }
      const left = res.headers.get('X-Credits-Remaining');
      if (left !== null) setCredits(left);
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        text += decoder.decode(value, { stream: true });
        output.textContent = text;
      }
      last = { ...request, output: text };
      delete last.mode;
      delete last.previous;
      status.textContent = t('done');
      copyBtn.disabled = false;
      refine.hidden = false;
      setTimeout(loadHistory, 800);
      loadProfile().catch(() => {});
    } catch (err) {
      output.textContent = err.message;
      status.textContent = '';
    } finally {
      output.classList.remove('is-typing');
      genBtn.disabled = false;
      $$('button', refine).forEach((b) => { b.disabled = false; });
    }
  };

  $('#genForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const prompt = $('#prompt').value.trim();
    if (!prompt) { $('#prompt').focus(); return; }
    run({ prompt, template, tone: $('#tone').value, language: langSelect.value });
  });
  $('#prompt').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) $('#genForm').requestSubmit();
  });

  $$('button[data-mode]', refine).forEach((btn) => btn.addEventListener('click', () => {
    if (!last) return;
    const { output: previous, ...request } = last;
    run({ ...request, mode: btn.dataset.mode, previous });
  }));

  copyBtn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(output.textContent);
      copyBtn.textContent = t('copied');
    } catch (e) {
      copyBtn.textContent = t('select_copy');
    }
    setTimeout(() => { copyBtn.textContent = t('copy'); }, 1500);
  });

  // Upgrade
  function openUpgrade(lead) {
    $('#upgradeLead').textContent = lead || t('upgrade_lead');
    $('#upgradeMsg').textContent = '';
    modal.showModal();
  }
  $('#upgradeBtn').addEventListener('click', () => openUpgrade());
  $$('[data-plan]', modal).forEach((btn) => btn.addEventListener('click', async () => {
    const url = await window.Muse.checkoutUrl(btn.dataset.plan).catch(() => null);
    if (!url) { $('#upgradeMsg').textContent = t('payments_not_ready'); return; }
    location.href = url;
  }));

  $('#signOutBtn').addEventListener('click', () => window.Muse.signOut());

  // Came from a pricing button (login.html?plan=…) or back from checkout (?paid=1)
  const params = new URLSearchParams(location.search);
  if (params.get('plan') && params.get('plan') !== 'free') {
    const url = await window.Muse.checkoutUrl(params.get('plan')).catch(() => null);
    if (url) location.href = url; else openUpgrade();
  }
  if (params.get('paid')) {
    status.textContent = t('thanks_paid');
    setTimeout(() => loadProfile().catch(() => {}), 4000);
  }
})();
