(() => {
  const root = document.documentElement;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Landing page copy for the hero animation and demo. Other languages live in js/i18n.js.
  const EN = {
    language: null, // output language requested from the live demo (null = English)
    scenes: [
      { chip: 0, prompt: 'Cold brew coffee for busy students, first can $1',
        out: "☕ Deadlines don't wait. Neither should your coffee.\n\nDrift Cold Brew: smooth, zero bitterness, ready when you are. Your first can is just $1 👉 Tap to try it." },
      { chip: 1, prompt: 'LinkedIn post: we just hit 1,000 customers',
        out: "1,000 customers. 🎉\n\nTwo years ago we shipped our first order from a kitchen table. Today, a thousand businesses trust us every week. Thank you for every order, review and idea.\n\n#milestone #smallbusiness" },
      { chip: 2, prompt: 'Email: 20% off winter collection, ends Sunday',
        out: "Subject: Your winter favorites, now 20% off ❄️\n\nHi there, our coziest pieces are on sale until Sunday. Use code WARM20 at checkout and stay snug for less." },
    ],
    demos: {
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
    },
    done: 'done ✓',
    writing: 'writing…',
    live: 'live AI',
    unavailable: 'unavailable',
    customPrompt: 'Describe anything you want written — an ad, a post, an email, a slogan.',
    customOutput: 'Your result will appear here, written live by AI.',
    errorLater: 'The live demo is not available right now. Please try again later.',
    errorSignup: 'The live demo is not available right now. Create a free account to start writing.',
  };
  const L = { ...EN, ...(window.MUSE_I18N || {})[root.lang] };

  // Endpoint of the live AI demo (see api/generate.js). Works when deployed on Vercel.
  const API_URL = '/api/generate';

  // Theme toggle
  $('#themeToggle')?.addEventListener('click', () => {
    const current = root.dataset.theme ||
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    const next = current === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  // Sticky nav border
  const nav = $('#nav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Mobile menu
  const burger = $('#burger');
  const links = $('#navLinks');
  if (burger && links) {
    const setMenu = (open) => {
      links.classList.toggle('is-open', open);
      burger.setAttribute('aria-expanded', String(open));
    };
    burger.addEventListener('click', () => setMenu(!links.classList.contains('is-open')));
    $$('a', links).forEach((a) => a.addEventListener('click', () => setMenu(false)));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });
  }

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

  // Hero studio: type a prompt, then stream the "generated" copy below it
  const typing = $('#typing');
  const studioOut = $('#studioOut');
  if (typing && studioOut) {
    const chips = $$('.chip:not(.chip--ghost)', $('#studioChips'));
    const scenes = L.scenes;
    const show = (scene) => chips.forEach((c, i) => c.classList.toggle('is-active', i === scene.chip));
    if (reduceMotion) {
      show(scenes[0]); typing.textContent = scenes[0].prompt; studioOut.textContent = scenes[0].out;
    } else {
      let si = 0;
      const typeInto = (el, text, speed, done) => {
        let i = 0;
        const step = () => {
          i = Math.min(i + (speed < 20 ? 3 : 1), text.length);
          el.textContent = text.slice(0, i);
          if (i < text.length) setTimeout(step, speed); else done();
        };
        step();
      };
      const run = () => {
        const scene = scenes[si];
        show(scene);
        studioOut.textContent = '';
        studioOut.classList.remove('is-typing');
        typeInto(typing, scene.prompt, 40, () => setTimeout(() => {
          studioOut.classList.add('is-typing');
          typeInto(studioOut, scene.out, 15, () => {
            studioOut.classList.remove('is-typing');
            si = (si + 1) % scenes.length;
            setTimeout(run, 3500);
          });
        }, 500));
      };
      setTimeout(run, 600);
    }
  }

  // Interactive demo: canned examples + a live tab that calls the AI endpoint
  const demo = $('.demo');
  if (demo) {
    const demos = L.demos;
    const demoPrompt = $('#demoPrompt');
    const demoOutput = $('#demoOutput');
    const demoStatus = $('#demoStatus');
    const form = $('#demoForm');
    const input = $('#demoInput');
    const submit = $('#demoSubmit');
    const tabs = $$('.demo__tab', demo);
    let demoTimer;
    let controller;

    const selectTab = (key) => tabs.forEach((t) => {
      const on = t.dataset.demo === key;
      t.classList.toggle('is-active', on);
      t.setAttribute('aria-selected', String(on));
    });

    const stopAll = () => {
      clearTimeout(demoTimer);
      controller?.abort();
      demoOutput.classList.remove('is-typing');
    };

    const runCanned = (key) => {
      stopAll();
      selectTab(key);
      form.hidden = true;
      const { prompt, output } = demos[key];
      demoPrompt.textContent = prompt;
      if (reduceMotion) { demoOutput.textContent = output; demoStatus.textContent = L.done; return; }
      demoStatus.textContent = L.writing;
      demoOutput.classList.add('is-typing');
      let i = 0;
      const step = () => {
        i = Math.min(i + 2, output.length);
        demoOutput.textContent = output.slice(0, i);
        if (i < output.length) { demoTimer = setTimeout(step, 18); return; }
        demoOutput.classList.remove('is-typing');
        demoStatus.textContent = L.done;
      };
      step();
    };

    const openCustom = () => {
      stopAll();
      selectTab('custom');
      form.hidden = false;
      demoPrompt.textContent = L.customPrompt;
      demoOutput.textContent = L.customOutput;
      demoStatus.textContent = L.live;
      input.focus();
    };

    const generate = async (prompt) => {
      stopAll();
      controller = new AbortController();
      demoPrompt.textContent = prompt;
      demoOutput.textContent = '';
      demoOutput.classList.add('is-typing');
      demoStatus.textContent = L.writing;
      submit.disabled = true;
      try {
        const res = await fetch(API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(L.language ? { prompt, language: L.language } : { prompt }),
          signal: controller.signal,
        });
        if (!res.ok) {
          let message = L.errorLater;
          try { message = (await res.json()).error || message; } catch (e) {}
          throw new Error(message);
        }
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        for (;;) {
          const { done, value } = await reader.read();
          if (done) break;
          demoOutput.textContent += decoder.decode(value, { stream: true });
        }
        demoStatus.textContent = L.done;
      } catch (err) {
        if (err.name === 'AbortError') return;
        demoOutput.textContent = err instanceof TypeError
          ? L.errorSignup
          : err.message;
        demoStatus.textContent = L.unavailable;
      } finally {
        demoOutput.classList.remove('is-typing');
        submit.disabled = false;
      }
    };

    tabs.forEach((t) => t.addEventListener('click', () => {
      if (t.dataset.demo === 'custom') openCustom(); else runCanned(t.dataset.demo);
    }));
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const prompt = input.value.trim();
      if (!prompt) { input.focus(); return; }
      generate(prompt);
    });
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
    });

    const demoIO = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) { runCanned('ad'); demoIO.disconnect(); }
    }, { threshold: 0.3 });
    demoIO.observe(demo);
  }

  // Pricing toggle
  const billing = $('#billingSwitch');
  billing?.addEventListener('click', () => {
    const yearly = billing.getAttribute('aria-checked') !== 'true';
    billing.setAttribute('aria-checked', String(yearly));
    $$('.price[data-month]').forEach((el) => {
      el.textContent = '$' + (yearly ? el.dataset.year : el.dataset.month);
    });
  });

  // Email sign-up forms (front-end only — wire to your email provider)
  $$('form[data-signup]').forEach((form) => {
    const msg = $('.form-msg', form);
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = $('input[type="email"]', form);
      if (!email.value || !email.checkValidity()) {
        msg.textContent = 'Please enter a valid email address.';
        email.focus();
        return;
      }
      msg.textContent = form.dataset.success || "🎉 You're on the list! We'll be in touch soon.";
      form.reset();
    });
  });

  // Remember the language picked on the landing page, so login and the studio open in it too.
  $$('.langs__menu a[lang]').forEach((a) => a.addEventListener('click', () => {
    try { localStorage.setItem('muse-lang', a.lang); } catch (e) {}
  }));

  // Interface translations for login, reset and the studio (js/ui-i18n.js).
  const UI = window.MuseUI;
  UI?.apply();
  const tr = (key) => (UI ? UI.t(key) : key);
  // Supabase error codes → translated messages.
  const authError = (err) => {
    if (err.message === 'not-configured') return tr('not_ready');
    const code = err.code || '';
    if (code === 'invalid_credentials' || /invalid login/i.test(err.message)) return tr('err_invalid');
    if (code === 'user_already_exists' || /already registered/i.test(err.message)) return tr('err_exists');
    if (code === 'email_not_confirmed' || /not confirmed/i.test(err.message)) return tr('err_unconfirmed');
    if (code === 'weak_password') return tr('err_pw');
    return err.message || tr('err_server');
  };

  // Auth page: log in / sign up through Supabase (see js/auth.js)
  const auth = $('#authCard');
  if (auth) {
    const params = new URLSearchParams(location.search);
    const plan = params.get('plan');
    const next = params.get('next') || (plan ? `app.html?plan=${encodeURIComponent(plan)}` : 'app.html');
    const msg = $('#authMsg');
    const submit = $('#authSubmit');
    const setMode = (mode) => {
      auth.dataset.mode = mode;
      $$('[data-auth-tab]', auth).forEach((t) => {
        const on = t.dataset.authTab === mode;
        t.classList.toggle('is-active', on);
        t.setAttribute('aria-selected', String(on));
      });
      $$('[data-only]', auth).forEach((el) => { el.hidden = el.dataset.only !== mode; });
      $('input[name="password"]', auth).autocomplete = mode === 'signup' ? 'new-password' : 'current-password';
      submit.textContent = tr(mode === 'signup' ? 'btn_signup' : 'btn_login');
      msg.textContent = '';
    };
    $$('[data-auth-tab]', auth).forEach((t) => t.addEventListener('click', () => setMode(t.dataset.authTab)));
    setMode(params.get('mode') === 'signup' || plan ? 'signup' : 'login');

    // Already signed in? Go straight to the app.
    window.Muse?.session().then((s) => { if (s) location.replace(next); }).catch(() => {});

    $('#googleBtn').addEventListener('click', async () => {
      try { await window.Muse.signInWithGoogle(next); } catch (err) { msg.textContent = authError(err); }
    });

    $('#forgotBtn').addEventListener('click', async () => {
      const email = $('input[name="email"]', auth);
      if (!email.value || !email.checkValidity()) { msg.textContent = tr('email_first'); email.focus(); return; }
      try {
        await window.Muse.resetPassword(email.value);
        msg.textContent = tr('reset_sent');
      } catch (err) {
        msg.textContent = authError(err);
      }
    });

    $('#authForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const formEl = e.currentTarget;
      const visible = $$('input', formEl).filter((i) => !i.closest('[hidden]'));
      const invalid = visible.find((i) => !i.checkValidity());
      if (invalid) {
        msg.textContent = tr(invalid.name === 'password' ? 'err_pw' : 'err_fill');
        invalid.focus();
        return;
      }
      const data = Object.fromEntries(new FormData(formEl));
      submit.disabled = true;
      msg.textContent = '';
      try {
        if (auth.dataset.mode === 'signup') {
          const { needsConfirmation } = await window.Muse.signUp(data.email, data.password, data.name);
          if (needsConfirmation) { msg.textContent = tr('confirm_email'); return; }
        } else {
          await window.Muse.signIn(data.email, data.password);
        }
        location.href = next;
      } catch (err) {
        msg.textContent = authError(err);
      } finally {
        submit.disabled = false;
      }
    });
  }

  // Reset page: the emailed link signs the user in, then they choose a new password.
  const resetCard = $('#resetCard');
  if (resetCard) {
    const form = $('#resetForm');
    const msg = $('#resetMsg');
    window.Muse.session()
      .then((s) => { if (s) form.hidden = false; else msg.textContent = tr('reset_invalid'); })
      .catch((err) => { msg.textContent = authError(err); });
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const pw = $('input[name="password"]', form);
      if (!pw.checkValidity()) { msg.textContent = tr('err_pw'); pw.focus(); return; }
      $('#resetSubmit').disabled = true;
      try {
        await window.Muse.updatePassword(pw.value);
        msg.textContent = tr('reset_ok');
        setTimeout(() => { location.href = 'app.html'; }, 1200);
      } catch (err) {
        msg.textContent = authError(err);
        $('#resetSubmit').disabled = false;
      }
    });
  }

  const year = $('#year');
  if (year) year.textContent = new Date().getFullYear();
})();
