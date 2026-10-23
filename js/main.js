(() => {
  const root = document.documentElement;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const UK = root.lang === 'uk'; // Ukrainian landing page (uk.html)
  const t = (en, uk) => (UK ? uk : en);

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
    const scenes = UK ? [
      { chip: 0, prompt: 'Кава з собою для студентів, перша чашка 30 грн',
        out: "☕ Дедлайни не чекають. Твоя кава теж не мусить.\n\nМ’яка, без гіркоти, готова за хвилину. Перша чашка — лише 30 грн 👉 Заходь по дорозі на пари!" },
      { chip: 1, prompt: 'Пост: нам 1000 клієнтів',
        out: "1000 клієнтів! 🎉\n\nДва роки тому ми відправили перше замовлення з кухні. Сьогодні нам довіряє тисяча людей. Дякуємо за кожне замовлення, відгук та ідею 💛" },
      { chip: 2, prompt: 'Лист: −20% на зимову колекцію до неділі',
        out: "Тема: Ваші зимові улюбленці — тепер −20% ❄️\n\nДо неділі наші найзатишніші речі зі знижкою. Промокод WARM20 — і тепло стає доступнішим." },
    ] : [
      { chip: 0, prompt: 'Cold brew coffee for busy students, first can $1',
        out: "☕ Deadlines don't wait. Neither should your coffee.\n\nDrift Cold Brew: smooth, zero bitterness, ready when you are. Your first can is just $1 👉 Tap to try it." },
      { chip: 1, prompt: 'LinkedIn post: we just hit 1,000 customers',
        out: "1,000 customers. 🎉\n\nTwo years ago we shipped our first order from a kitchen table. Today, a thousand businesses trust us every week. Thank you for every order, review and idea.\n\n#milestone #smallbusiness" },
      { chip: 2, prompt: 'Email: 20% off winter collection, ends Sunday',
        out: "Subject: Your winter favorites, now 20% off ❄️\n\nHi there, our coziest pieces are on sale until Sunday. Use code WARM20 at checkout and stay snug for less." },
    ];
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
    const demosUk = {
      ad: {
        prompt: 'Напиши рекламу в Instagram для кав’ярні з холодною кавою. Грайливий тон, до 50 слів, із закликом до дії.',
        output: "☕ Ранок подзвонив — просить повернути йому іскру.\n\nХолодна кава Drift: 18 годин настоювання, нуль гіркоти, лише гарний настрій. Пий повільно або встигай усе — вибір за тобою.\n\n👉 Перша баночка всього за 30 грн!",
      },
      product: {
        prompt: 'Опис товару для мінімалістичних бездротових навушників. Преміально, 3 ключові переваги.',
        output: "Звук. Нічого зайвого.\n\nAura Buds прибирають усе непотрібне й досконало роблять головне:\n\n• 40 годин роботи — більше, ніж триває ваш найзавантаженіший тиждень\n• Адаптивне шумозаглушення, що підлаштовується під вас\n• Настільки легкі, що ви про них забудете\n\nЧистий звук. Нічого на заваді.",
      },
      email: {
        prompt: 'Короткий лист маркетинг-директору з пропозицією AI-контенту. Дружньо, без нав’язливості.',
        output: "Тема: 30 постів за один день?\n\nДобрий день, Олено!\n\nПомітив, що ви публікуєтеся в LinkedIn щодня — це вражає. Ми допомагаємо командам скоротити час на створення контенту на 70% без втрати власного стилю.\n\nЗнайдете 15 хвилин наступного тижня?\n\nЗ повагою,\nОлександр",
      },
    };
    const demosEn = {
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
    const demos = UK ? demosUk : demosEn;
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
      if (reduceMotion) { demoOutput.textContent = output; demoStatus.textContent = t('done ✓', 'готово ✓'); return; }
      demoStatus.textContent = t('writing…', 'пишу…');
      demoOutput.classList.add('is-typing');
      let i = 0;
      const step = () => {
        i = Math.min(i + 2, output.length);
        demoOutput.textContent = output.slice(0, i);
        if (i < output.length) { demoTimer = setTimeout(step, 18); return; }
        demoOutput.classList.remove('is-typing');
        demoStatus.textContent = t('done ✓', 'готово ✓');
      };
      step();
    };

    const openCustom = () => {
      stopAll();
      selectTab('custom');
      form.hidden = false;
      demoPrompt.textContent = t('Describe anything you want written — an ad, a post, an email, a slogan.', 'Опишіть, що потрібно написати: рекламу, пост, лист чи слоган.');
      demoOutput.textContent = t('Your result will appear here, written live by AI.', 'Тут з’явиться результат, написаний AI наживо.');
      demoStatus.textContent = t('live AI', 'живий AI');
      input.focus();
    };

    const generate = async (prompt) => {
      stopAll();
      controller = new AbortController();
      demoPrompt.textContent = prompt;
      demoOutput.textContent = '';
      demoOutput.classList.add('is-typing');
      demoStatus.textContent = t('writing…', 'пишу…');
      submit.disabled = true;
      try {
        const res = await fetch(API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(UK ? { prompt, language: 'Ukrainian' } : { prompt }),
          signal: controller.signal,
        });
        if (!res.ok) {
          let message = t('The live demo is not available right now. Please try again later.', 'Демо зараз недоступне. Спробуйте пізніше.');
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
        demoStatus.textContent = t('done ✓', 'готово ✓');
      } catch (err) {
        if (err.name === 'AbortError') return;
        demoOutput.textContent = err instanceof TypeError
          ? t('The live demo is not available right now. Create a free account to start writing.', 'Демо зараз недоступне. Створіть безкоштовний акаунт, щоб почати.')
          : err.message;
        demoStatus.textContent = t('unavailable', 'недоступно');
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
      submit.textContent = mode === 'signup' ? 'Create account' : 'Log in';
      msg.textContent = '';
    };
    $$('[data-auth-tab]', auth).forEach((t) => t.addEventListener('click', () => setMode(t.dataset.authTab)));
    setMode(params.get('mode') === 'signup' || plan ? 'signup' : 'login');

    const notReady = 'Accounts are not available yet: the site owner still needs to connect Supabase (see README).';
    const friendly = (err) => err.message === 'not-configured' ? notReady : err.message || 'Something went wrong. Please try again.';

    // Already signed in? Go straight to the app.
    window.Muse?.session().then((s) => { if (s) location.replace(next); }).catch(() => {});

    $('#googleBtn').addEventListener('click', async () => {
      try { await window.Muse.signInWithGoogle(next); } catch (err) { msg.textContent = friendly(err); }
    });

    $('#authForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const formEl = e.currentTarget;
      const visible = $$('input', formEl).filter((i) => !i.closest('[hidden]'));
      const invalid = visible.find((i) => !i.checkValidity());
      if (invalid) {
        msg.textContent = invalid.name === 'password' ? 'Password must be at least 8 characters.' : 'Please fill in all fields correctly.';
        invalid.focus();
        return;
      }
      const data = Object.fromEntries(new FormData(formEl));
      submit.disabled = true;
      msg.textContent = '';
      try {
        if (auth.dataset.mode === 'signup') {
          const { needsConfirmation } = await window.Muse.signUp(data.email, data.password, data.name);
          if (needsConfirmation) { msg.textContent = '📬 Almost there! Check your email to confirm your account.'; return; }
        } else {
          await window.Muse.signIn(data.email, data.password);
        }
        location.href = next;
      } catch (err) {
        msg.textContent = friendly(err);
      } finally {
        submit.disabled = false;
      }
    });
  }

  const year = $('#year');
  if (year) year.textContent = new Date().getFullYear();
})();
