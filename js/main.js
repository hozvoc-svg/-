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

  // Typing effect in the hero mockup
  const typing = $('#typing');
  const phrases = [
    'Why did revenue spike in March?',
    'Show weekly active users by country',
    'Which plan has the highest churn?',
  ];
  if (reduceMotion) {
    typing.textContent = phrases[0];
  } else {
    let pi = 0, ci = 0, deleting = false;
    const loop = () => {
      const phrase = phrases[pi];
      ci += deleting ? -1 : 1;
      typing.textContent = phrase.slice(0, ci);
      let delay = deleting ? 30 : 55;
      if (!deleting && ci === phrase.length) { deleting = true; delay = 1800; }
      else if (deleting && ci === 0) { deleting = false; pi = (pi + 1) % phrases.length; delay = 400; }
      setTimeout(loop, delay);
    };
    setTimeout(loop, 800);
  }

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
