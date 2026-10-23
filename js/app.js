// Muse studio (app.html): generate copy, track credits, history and upgrades.
(async () => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const PLAN_NAMES = { free: 'Free', creator: 'Creator', pro: 'Pro' };
  const TEMPLATE_NAMES = { ad: 'Ad', social: 'Social post', product: 'Product description', email: 'Email', blog: 'Blog outline', slogan: 'Slogans' };

  const output = $('#output');
  const status = $('#genStatus');
  const genBtn = $('#genBtn');
  const copyBtn = $('#copyBtn');
  const modal = $('#upgradeModal');
  let template = 'ad';
  let session;

  try {
    session = await window.Muse.requireSession();
  } catch (err) {
    output.innerHTML = '';
    const p = document.createElement('p');
    p.className = 'output__empty';
    p.textContent = 'The studio is not set up yet: the site owner needs to connect Supabase (see README).';
    output.append(p);
    genBtn.disabled = true;
    return;
  }

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
  };

  const loadProfile = async () => {
    const p = await window.Muse.profile();
    if (p) renderProfile(p);
    return p;
  };

  const renderHistory = (items) => {
    const list = $('#history');
    list.innerHTML = '';
    if (!items.length) {
      const li = document.createElement('li');
      li.className = 'output__empty';
      li.textContent = 'No generations yet.';
      list.append(li);
      return;
    }
    items.forEach((g) => {
      const li = document.createElement('li');
      const btn = document.createElement('button');
      btn.type = 'button';
      const tag = document.createElement('span');
      tag.className = 'tag';
      tag.textContent = TEMPLATE_NAMES[g.template] || g.template;
      const text = document.createElement('span');
      text.className = 'history__prompt';
      text.textContent = g.prompt;
      const time = document.createElement('small');
      time.textContent = new Date(g.created_at).toLocaleString();
      btn.append(tag, text, time);
      btn.addEventListener('click', () => {
        output.textContent = g.output;
        copyBtn.disabled = false;
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

  // Generate
  $('#genForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const prompt = $('#prompt').value.trim();
    if (!prompt) { $('#prompt').focus(); return; }
    genBtn.disabled = true;
    copyBtn.disabled = true;
    output.textContent = '';
    output.classList.add('is-typing');
    status.textContent = 'writing…';
    try {
      session = (await window.Muse.session()) || session; // picks up refreshed tokens
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${session.access_token}` },
        body: JSON.stringify({ prompt, template, tone: $('#tone').value, language: $('#language').value }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        if (err.code === 'no_credits') openUpgrade("You're out of credits. Pick a plan to keep creating.");
        if (err.code === 'auth') { window.Muse.signOut(); return; }
        throw new Error(err.error || 'Something went wrong. Please try again.');
      }
      const left = res.headers.get('X-Credits-Remaining');
      if (left !== null) setCredits(left);
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        output.textContent += decoder.decode(value, { stream: true });
      }
      status.textContent = 'done ✓';
      copyBtn.disabled = false;
      setTimeout(loadHistory, 800);
      loadProfile().catch(() => {});
    } catch (err) {
      output.textContent = err.message;
      status.textContent = '';
    } finally {
      output.classList.remove('is-typing');
      genBtn.disabled = false;
    }
  });
  $('#prompt').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) $('#genForm').requestSubmit();
  });

  copyBtn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(output.textContent);
      copyBtn.textContent = 'Copied ✓';
    } catch (e) {
      copyBtn.textContent = 'Select & copy';
    }
    setTimeout(() => { copyBtn.textContent = 'Copy'; }, 1500);
  });

  // Upgrade
  function openUpgrade(lead) {
    if (lead) $('#upgradeLead').textContent = lead;
    $('#upgradeMsg').textContent = '';
    modal.showModal();
  }
  $('#upgradeBtn').addEventListener('click', () => openUpgrade());
  $$('[data-plan]', modal).forEach((btn) => btn.addEventListener('click', async () => {
    const url = await window.Muse.checkoutUrl(btn.dataset.plan).catch(() => null);
    if (!url) { $('#upgradeMsg').textContent = 'Payments are not set up yet (see README → Lemon Squeezy).'; return; }
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
    status.textContent = '🎉 Thanks! Your plan is being activated…';
    setTimeout(() => loadProfile().catch(() => {}), 4000);
  }
})();
