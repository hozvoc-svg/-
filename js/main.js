(() => {
  const root = document.documentElement;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Theme toggle
  $('#themeToggle').addEventListener('click', () => {
    const current = root.dataset.theme ||
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    const next = current === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  // Sticky nav border
  const nav = $('#nav');
  const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 8);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile menu
  const burger = $('#burger');
  const links = $('#navLinks');
  const setMenu = (open) => {
    links.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
  };
  burger.addEventListener('click', () => setMenu(!links.classList.contains('is-open')));
  $$('a', links).forEach((a) => a.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });

  // Animated counters
  const animateCount = (el) => {
    const target = parseFloat(el.dataset.count);
    const decimals = parseInt(el.dataset.decimals || '0', 10);
    const prefix = el.dataset.prefix || '';
    const suffix = el.dataset.suffix || '';
    const format = (v) => prefix + v.toLocaleString('en-US', {
      minimumFractionDigits: decimals, maximumFractionDigits: decimals,
    }) + suffix;
    if (reduceMotion) { el.textContent = format(target); return; }
    const duration = 1600;
    const start = performance.now();
    const tick = (now) => {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = format(target * eased);
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };

  // Scroll reveal + counters
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      $$('[data-count]', entry.target).forEach(animateCount);
      io.unobserve(entry.target);
    });
  }, { threshold: 0.15 });
  $$('.reveal').forEach((el, i) => {
    el.style.transitionDelay = `${(i % 4) * 70}ms`;
    io.observe(el);
  });

  // Cursor glow on feature cards
  $$('.card').forEach((card) => {
    card.addEventListener('pointermove', (e) => {
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${e.clientX - r.left}px`);
      card.style.setProperty('--my', `${e.clientY - r.top}px`);
    });
  });

  // Hero studio: type a prompt, show a loading shimmer, then reveal new "images"
  const typing = $('#typing');
  const grid = $('#studioGrid');
  const arts = $$('.art', grid);
  const phrases = [
    'A neon jellyfish drifting through a midnight city',
    'Pastel desert sunrise, minimal, soft light',
    'Holographic sneaker product shot, studio lighting',
  ];
  const artSets = [[1, 5, 4, 6], [2, 6, 3, 1], [4, 3, 2, 5]];
  const showSet = (i) => arts.forEach((el, k) => { el.className = `art art--${artSets[i][k]}`; });
  if (reduceMotion) {
    typing.textContent = phrases[0];
  } else {
    let pi = 0, ci = 0, deleting = false;
    const loop = () => {
      const phrase = phrases[pi];
      ci += deleting ? -1 : 1;
      typing.textContent = phrase.slice(0, ci);
      let delay = deleting ? 18 : 45;
      if (!deleting && ci === phrase.length) {
        grid.classList.add('is-loading');
        setTimeout(() => { showSet(pi); grid.classList.remove('is-loading'); }, 1100);
        deleting = true; delay = 3200;
      } else if (deleting && ci === 0) {
        deleting = false; pi = (pi + 1) % phrases.length; delay = 400;
      }
      setTimeout(loop, delay);
    };
    setTimeout(loop, 800);
  }

  // Interactive demo: canned prompts with a streaming-style response
  const demos = {
    ad: {
      prompt: 'Write an Instagram ad for a cold-brew coffee brand. Playful tone, under 50 words, include a CTA.',
      output: "☕ Mornings called. They want their spark back.\n\nMeet Drift Cold Brew — 18 hours steeped, zero bitterness, all good vibes. Smooth enough to sip slow, bold enough to get things done.\n\n👉 Tap to grab your first can for $1.",
    },
    product: {
      prompt: 'Product description for minimalist wireless earbuds. Premium feel, 3 key benefits.',
      output: "Sound, distilled.\n\nAura Buds strip away everything you don't need and perfect everything you do:\n\n• 40-hour battery that outlasts your busiest week\n• Adaptive noise cancelling that learns your world\n• A feather-light fit you'll forget you're wearing\n\nPure audio. Nothing in the way.",
    },
    email: {
      prompt: 'Short cold email to a marketing director offering AI content services. Friendly, not salesy.',
      output: "Subject: 30 posts, one afternoon?\n\nHi Jordan,\n\nI noticed Northwind posts daily on LinkedIn — impressive consistency. We help teams like yours cut content production time by 70% with AI, without losing your voice.\n\nWorth a 15-minute chat next week?\n\nBest,\nAlex",
    },
  };
  const demoPrompt = $('#demoPrompt');
  const demoOutput = $('#demoOutput');
  const demoStatus = $('#demoStatus');
  const tabs = $$('.demo__tab');
  let demoTimer;
  const runDemo = (key) => {
    clearTimeout(demoTimer);
    const { prompt, output } = demos[key];
    demoPrompt.textContent = prompt;
    tabs.forEach((t) => {
      const on = t.dataset.demo === key;
      t.classList.toggle('is-active', on);
      t.setAttribute('aria-selected', String(on));
    });
    if (reduceMotion) { demoOutput.textContent = output; demoStatus.textContent = 'done ✓'; return; }
    demoStatus.textContent = 'writing…';
    demoOutput.classList.add('is-typing');
    let i = 0;
    const step = () => {
      i = Math.min(i + 2, output.length);
      demoOutput.textContent = output.slice(0, i);
      if (i < output.length) { demoTimer = setTimeout(step, 18); return; }
      demoOutput.classList.remove('is-typing');
      demoStatus.textContent = 'done ✓';
    };
    step();
  };
  tabs.forEach((t) => t.addEventListener('click', () => runDemo(t.dataset.demo)));
  const demoIO = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) { runDemo('ad'); demoIO.disconnect(); }
  }, { threshold: 0.3 });
  demoIO.observe($('.demo'));

  // Pricing toggle
  const billing = $('#billingSwitch');
  billing.addEventListener('click', () => {
    const yearly = billing.getAttribute('aria-checked') !== 'true';
    billing.setAttribute('aria-checked', String(yearly));
    $$('.price[data-month]').forEach((el) => {
      el.textContent = '$' + (yearly ? el.dataset.year : el.dataset.month);
    });
  });

  // CTA form (front-end only — wire to your email provider)
  const form = $('#ctaForm');
  const msg = $('#ctaMsg');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = $('#email', form);
    if (!email.checkValidity() || !email.value) {
      msg.textContent = 'Please enter a valid email address.';
      email.focus();
      return;
    }
    msg.textContent = "🎉 You're on the list! We'll be in touch soon.";
    form.reset();
  });

  $('#year').textContent = new Date().getFullYear();
})();
