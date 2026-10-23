"""Builds the English inner pages: about, blog, articles, legal pages, 404 and the free tools.

The homepage in 7 languages is built by tools/build_landing.py; login.html, reset.html and app.html
are edited by hand. Run:  python3 tools/build_pages.py
"""
import os
import pathlib

OUT = str(pathlib.Path(__file__).resolve().parent.parent)

def head(title, desc, extra=''):
    return f'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#0b0d14">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://hozvoc-svg.github.io/-/assets/og-image.png">
  <meta name="twitter:card" content="summary_large_image">{extra}
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="manifest" href="site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <script>
    document.documentElement.classList.add('js');
    // Apply saved theme before paint to avoid a flash.
    try {{ const t = localStorage.getItem('theme'); if (t) document.documentElement.dataset.theme = t; }} catch (e) {{}}
  </script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
'''

def header(active=''):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == active else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''
  <header class="nav" id="nav">
    <div class="container nav__inner">
      <a href="index.html" class="logo" aria-label="Muse home">
        <img src="assets/favicon.svg" alt="" width="28" height="28">
        <span>Muse</span>
      </a>
      <nav class="nav__links" id="navLinks" aria-label="Primary">
        {a('index.html#features','Features','features')}
        {a('index.html#demo','Try it','demo')}
        {a('index.html#pricing','Pricing','pricing')}
        {a('blog.html','Blog','blog')}
        {a('about.html','About','about')}
        <a href="login.html" class="nav__login">Log in</a>
      </nav>
      <div class="nav__actions">
        <button class="icon-btn" id="themeToggle" aria-label="Toggle color theme">
          <svg class="i-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
          <svg class="i-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
        </button>
        <a href="login.html?mode=signup" class="btn btn--primary btn--sm nav__cta">Start free</a>
        <button class="icon-btn burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="navLinks">
          <span></span><span></span>
        </button>
      </div>
    </div>
  </header>
'''

FOOTER = '''
  <footer class="footer">
    <div class="container footer__inner">
      <div class="footer__brand">
        <a href="index.html" class="logo"><img src="assets/favicon.svg" alt="" width="24" height="24"><span>Muse</span></a>
        <p>Marketing copy in seconds.</p>
      </div>
      <div class="footer__cols">
        <div><h4>Product</h4><a href="index.html#features">Features</a><a href="index.html#pricing">Pricing</a><a href="index.html#faq">FAQ</a><a href="tools.html">Free tools</a><a href="login.html">Log in</a></div>
        <div><h4>Company</h4><a href="about.html">About</a><a href="blog.html">Blog</a><a href="about.html#contact">Contact</a></div>
        <div><h4>Legal</h4><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a></div>
      </div>
    </div>
    <div class="container footer__bottom">
      <p>© <span id="year"></span> Muse. All rights reserved.</p>
    </div>
  </footer>

  <script src="js/main.js" defer></script>
</body>
</html>
'''

AUTH_SCRIPTS = '''  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.117.0/dist/umd/supabase.js" defer></script>
  <script src="js/auth.js" defer></script>
'''

def page(name, title, desc, body, active='', footer=True, extra='', scripts=''):
    end = '  <script src="js/main.js" defer></script>\n</body>\n</html>\n'
    html = head(title, desc, extra) + header(active) + body + (FOOTER.replace(end, scripts + end) if footer else '\n' + scripts + end)
    open(os.path.join(OUT, name), 'w').write(html)

CONTACT = 'support@example.com'  # TODO: replace with the owner's support email

# ---------------- About ----------------
page('about.html', 'About — Muse', 'Muse is an AI copywriter that helps small businesses and creators write marketing content in seconds.', f'''
  <main id="main">
    <section class="page-hero">
      <div class="hero__glow" aria-hidden="true"></div>
      <div class="container">
        <span class="eyebrow reveal">About</span>
        <h1 class="reveal">Great copy shouldn't need a <span class="gradient-text">big budget</span></h1>
        <p class="reveal">Muse is an independent product that helps small businesses, creators and freelancers write marketing content in seconds.</p>
      </div>
    </section>

    <section class="section">
      <div class="container split">
        <div class="art art--5 reveal" role="img" aria-label="Abstract aurora artwork"></div>
        <div class="reveal">
          <span class="eyebrow">Why Muse</span>
          <h2>Write more. Spend less time on it.</h2>
          <p>Hiring a copywriter is expensive, and writing every post yourself takes hours. Muse gives you a first draft in seconds — in the right format, tone and language — so you can spend your time running your business.</p>
          <p>Muse is built on Claude by Anthropic, one of the most capable AI models for writing.</p>
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container">
        <div class="section__head reveal">
          <span class="eyebrow">Our principles</span>
          <h2>What we believe in</h2>
        </div>
        <div class="values">
          <article class="card reveal"><div class="card__icon">🎯</div><h3>Useful over flashy</h3><p>Every feature has to save you time on real marketing work.</p></article>
          <article class="card reveal"><div class="card__icon">🔐</div><h3>Your work is yours</h3><p>You own what you create. Your content is not used to train AI models.</p></article>
          <article class="card reveal"><div class="card__icon">💸</div><h3>Fair pricing</h3><p>A free plan to start, simple monthly plans, cancel anytime.</p></article>
        </div>
      </div>
    </section>

    <section class="section" id="contact">
      <div class="container newsletter reveal">
        <span class="eyebrow">Contact</span>
        <h2>Questions or feedback?</h2>
        <p style="color:var(--muted)">We read every message and usually reply within one business day.</p>
        <p><a class="btn btn--primary btn--lg" href="mailto:{CONTACT}">{CONTACT}</a></p>
      </div>
    </section>
  </main>
''', active='about')

# ---------------- Blog post ----------------
page('blog-post.html', 'How to get great marketing copy from AI — Muse', 'Four habits that turn generic AI text into marketing copy your customers respond to.', '''
  <main id="main">
    <article>
      <header class="page-hero">
        <div class="hero__glow" aria-hidden="true"></div>
        <div class="container">
          <a class="tag reveal" href="blog.html" style="display:inline-block">← Back to blog</a>
          <h1 class="reveal">How to get great marketing copy from AI</h1>
          <div class="meta reveal">5 min read</div>
        </div>
      </header>
      <div class="container">
        <div class="prose reveal">
          <p><strong>AI can write a decent post in seconds. Getting a great one takes a little direction.</strong> These four habits make the biggest difference.</p>

          <h2>1. Start with the outcome, not the format</h2>
          <p>“Write an Instagram post” gives you something generic. “Write an Instagram post that gets new runners to sign up for our Saturday 5K” gives you something that works. Say who it's for and what you want them to do.</p>

          <div class="art art--1" role="img" aria-label="Abstract neon artwork"></div>

          <h2>2. Give one concrete detail</h2>
          <p>A price, a deadline, an ingredient, a customer problem. One specific fact makes copy feel real instead of salesy.</p>
          <blockquote>Weak: “Try our amazing coffee.” Strong: “18 hours steeped, zero bitterness — your first can is $1.”</blockquote>

          <h2>3. Pick the tone on purpose</h2>
          <p>A luxury brand and a student café shouldn't sound the same. Choose the tone that matches your audience, then generate a couple of versions and keep the best lines.</p>
          <ul>
            <li>Playful for social media and younger audiences</li>
            <li>Professional for B2B and LinkedIn</li>
            <li>Minimal for premium products</li>
          </ul>

          <h2>4. Keep a human in the loop</h2>
          <p>AI is a brilliant first draft and a tireless brainstorming partner. Read the result, adjust a word or two to sound like you, and check facts like prices and dates before you publish.</p>

          <h3>Ready to try it?</h3>
          <p>Muse gives you 10 free generations every month. <a href="login.html?mode=signup">Create your free account</a> or <a href="index.html#demo">try it without signing up</a>.</p>
        </div>
      </div>
    </article>

    <section class="section">
      <div class="container">
        <div class="cta reveal">
          <div>
            <h2>Your next post is one sentence away.</h2>
            <p>Create a free account and get 10 generations every month.</p>
          </div>
          <div class="cta__form">
            <a href="login.html?mode=signup" class="btn btn--light btn--lg">Start writing free</a>
          </div>
        </div>
      </div>
    </section>
  </main>
''', active='blog')

# ---------------- Legal ----------------
def legal(name, title, intro, sections):
    body = '\n'.join(f'          <h2>{h}</h2>\n          <p>{p}</p>' for h,p in sections)
    page(name, f'{title} — Muse', f'{title} for Muse.', f'''
  <main id="main">
    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">Legal</span>
        <h1>{title}</h1>
        <p>Last updated: October 23, 2026</p>
      </div>
    </section>
    <section class="section" style="padding-top: 0">
      <div class="container">
        <div class="prose">
          <p>{intro}</p>
{body}
          <h2>Contact</h2>
          <p>Questions? Email us at <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
        </div>
      </div>
    </section>
  </main>
''')

legal('privacy.html', 'Privacy Policy', 'This policy explains what information Muse collects, how we use it and the choices you have.', [
  ('Information we collect', 'Your account details (name, email and, if you use Google sign-in, your Google profile basics), the prompts you write and the content Muse generates for you, and basic technical data such as your IP address, which we use to prevent abuse.'),
  ('How we use information', 'To provide the service, save your history, manage your plan and credits, prevent abuse and answer support requests. We do not sell your personal information.'),
  ('Service providers', 'We rely on trusted providers to run Muse: Supabase (accounts and database), Anthropic (the Claude AI model that writes your content), Lemon Squeezy (payments and billing, acting as merchant of record) and Vercel (hosting). They process data only to provide their services to us.'),
  ('AI and your content', 'Your prompts are sent to Anthropic’s Claude API to generate your content. Your content is not used to train AI models.'),
  ('Payments', 'Payments are handled by Lemon Squeezy. We never see or store your full card details.'),
  ('Data retention and deletion', 'We keep your data while your account is active. To delete your account and data, email us and we will remove it within 30 days.'),
  ('Your rights', 'Depending on where you live, you may have the right to access, correct, delete or export your data, and to object to certain processing. Contact us to exercise these rights.'),
])
legal('terms.html', 'Terms of Service', 'These terms govern your use of Muse. By creating an account you agree to them.', [
  ('Your account', 'Provide accurate information and keep your login secure. You are responsible for activity under your account.'),
  ('Acceptable use', 'Do not use Muse to create illegal, harmful, deceptive or infringing content, to send spam, or to attempt to disrupt or abuse the service.'),
  ('Your content', 'You own the content you create with Muse and may use it commercially. You are responsible for reviewing it before publishing.'),
  ('Plans, credits and billing', 'Each generation uses one credit. Free accounts receive 10 credits every 30 days; paid plans receive their monthly credits on each billing date. Unused credits do not roll over. Subscriptions renew automatically until cancelled; you can cancel anytime and keep access until the end of the paid period. Payments are processed by Lemon Squeezy, our merchant of record.'),
  ('Refunds', 'If something went wrong with your purchase, contact us within 14 days and we will make it right.'),
  ('Disclaimers', 'AI-generated content can contain mistakes. Check facts such as prices, dates and claims before publishing. The service is provided “as is” to the extent permitted by law.'),
  ('Changes', 'We may update these terms. We will notify you of material changes by email or in the app.'),
])

# ---------------- 404 ----------------
page('404.html', 'Page not found — Muse', 'This page could not be found.', '''
  <main id="main" class="notfound">
    <div class="hero__glow" aria-hidden="true"></div>
    <div style="position:relative">
      <div class="code gradient-text">404</div>
      <h1>Even AI couldn't write this page</h1>
      <p>The page you're looking for doesn't exist or has moved.</p>
      <a href="index.html" class="btn btn--primary btn--lg">Back to home</a>
    </div>
  </main>
''', footer=False, extra='\n  <meta name="robots" content="noindex">')

# ================= Blog articles =================
CTA = '''
    <section class="section">
      <div class="container">
        <div class="cta reveal">
          <div>
            <h2>{h}</h2>
            <p>{p}</p>
          </div>
          <div class="cta__form">
            <a href="login.html?mode=signup" class="btn btn--light btn--lg">{b}</a>
          </div>
        </div>
      </div>
    </section>'''

def article(fname, title, desc, h1, minutes, art, body, cta=('Write your next post in seconds.', 'Muse gives you 10 free generations every month.', 'Start writing free'), lang='en', back='← Back to blog'):
    html_body = f'''
  <main id="main">
    <article>
      <header class="page-hero">
        <div class="hero__glow" aria-hidden="true"></div>
        <div class="container">
          <a class="tag reveal" href="blog.html" style="display:inline-block">{back}</a>
          <h1 class="reveal">{h1}</h1>
          <div class="meta reveal">{minutes}</div>
        </div>
      </header>
      <div class="container">
        <div class="prose reveal">
{body}
          <div class="art {art}" role="img" aria-label="Abstract artwork"></div>
        </div>
      </div>
    </article>
{CTA.format(h=cta[0], p=cta[1], b=cta[2])}
  </main>
'''
    page(fname, title, desc, html_body, active='blog')
    if lang != 'en':
        p = os.path.join(OUT, fname)
        s = open(p).read().replace('<html lang="en"', f'<html lang="{lang}"', 1)
        open(p, 'w').write(s)

def ul(items): return '          <ul>\n' + '\n'.join(f'            <li>{i}</li>' for i in items) + '\n          </ul>'
def ol(items): return '          <ol>\n' + '\n'.join(f'            <li>{i}</li>' for i in items) + '\n          </ol>'

# ---------- 1. Instagram captions ----------
cap = {
 'Coffee shops &amp; cafés': ['Monday called. We answered with espresso. ☕', 'Your sign to take a 10-minute break is right here.', 'Fresh pastries, fresh start. Come say hi before 10am 🥐', 'Rain outside, cinnamon latte inside. Fair trade.', 'Tag the friend who owes you a coffee 👇'],
 'Beauty salons': ['New week, new nails. Who’s booking? 💅', 'Before ➡️ after. Swipe to see the glow-up.', 'Self-care isn’t selfish. Two spots left this Friday.', 'Your hair, but on its best day. Every day.', 'Booked, blessed and blow-dried. Link in bio to reserve.'],
 'Clothing &amp; fashion stores': ['Restocked and ready to sell out (again). 🛍️', 'One jacket, three looks. Which one is you?', 'Weekend plans: this outfit. That’s it, that’s the plan.', 'Comfort that doesn’t look like comfort.', 'Only 12 left in this color. Just saying 👀'],
 'Fitness &amp; gyms': ['You don’t have to be great to start. You have to start to be great.', 'Monday motivation, delivered at 7am sharp. See you there 💪', 'Progress, not perfection. Show us your first-week win 👇', 'Free trial class this Saturday. Bring a friend, bring water.', 'Sore today, strong tomorrow.'],
 'Restaurants &amp; food': ['Made from scratch. Eaten in seconds. 🍝', 'Your table is waiting (and so is dessert).', 'Date night, sorted. Reserve via the link in bio.', 'New on the menu — and already a staff favorite.', 'Comment your go-to order and we’ll guess your personality 😄'],
 'Online shops &amp; e-commerce': ['Free shipping ends at midnight. You know what to do. 🛒', 'Customer favorite for a reason: 4.9★ and counting.', 'Gift idea, solved. Wrapped and shipped in 24 hours.', 'Small business, big love. Every order is packed by hand. 💛', 'Back in stock — but not for long.'],
 'Any business': ['Behind the scenes of a very ordinary (very busy) Tuesday.', 'Meet the team that makes it happen 👋', 'You asked, we listened. Here’s what’s new.', 'Thank you for 1,000 followers! Giveaway details below 🎉', 'Save this post for later — you’ll thank us.'],
}
body = '''          <p><strong>Stuck on what to write under your next post?</strong> Here are 35 ready-to-use Instagram captions for small businesses, grouped by industry. Copy them, tweak a word or two, and post.</p>
          <p>Each one follows a simple rule that works on Instagram: a short, scroll-stopping first line, and a clear reason to comment, save or visit.</p>
'''
for k, v in cap.items():
    body += f'          <h2>{k}</h2>\n' + ul(v) + '\n'
body += '''          <h2>How to write your own captions that work</h2>
''' + ol(['<strong>Lead with the hook.</strong> Only the first line shows before “more”. Make it a question, a bold claim or a relatable feeling.', '<strong>Add one concrete detail.</strong> A time, a price, a flavor, a number. Specific beats generic.', '<strong>Ask for one action.</strong> Comment, save, tag a friend or tap the link — pick one, not all four.', '<strong>Keep hashtags at the end.</strong> 3–8 relevant hashtags are plenty.']) + '''
          <h2>Need captions for your exact product?</h2>
          <p>Lists are a great start, but captions written for your product, your offer and your audience work better. <a href="login.html?mode=signup">Muse</a> writes them in seconds: describe what you sell, choose “Social post” and a tone, and get a caption ready to publish — in 11 languages, from English and Spanish to Chinese, Hindi and Arabic.</p>
'''
article('instagram-caption-ideas.html', '35 Instagram Caption Ideas for Small Businesses (Copy &amp; Paste) — Muse', 'Ready-to-use Instagram captions for cafés, salons, shops, gyms and restaurants, plus a simple formula to write your own.', '35 Instagram caption ideas for small businesses', '6 min read', 'art--4', body, ('Get captions written for your business.', 'Describe your product and get a ready-to-post caption in seconds. 10 free every month.', 'Try Muse free'))

# ---------- 2. Product descriptions ----------
body = '''          <p><strong>A product description has one job: help the right customer decide to buy.</strong> Most descriptions fail because they list features nobody asked about. Here’s a simple structure that sells, with before-and-after examples.</p>

          <h2>The 4-part structure</h2>
''' + ol(['<strong>Headline with the main benefit.</strong> Not “Ceramic mug, 350 ml” but “The mug that keeps your coffee hot through your first meeting.”', '<strong>One short paragraph for the feeling.</strong> Who is it for, and how will their day be better?', '<strong>3 benefit bullets.</strong> Turn each feature into what it does for the customer.', '<strong>Remove the last doubt.</strong> Size, materials, shipping time, returns — whatever stops people from clicking “buy”.']) + '''

          <h2>Example: before and after</h2>
          <h3>Before</h3>
          <blockquote>Wireless earbuds. Bluetooth 5.3. 40h battery. Noise cancelling. Black.</blockquote>
          <h3>After</h3>
          <blockquote>Sound, distilled. Aura Buds strip away the noise so you can focus on what you’re listening to.<br>• 40-hour battery that outlasts your busiest week<br>• Noise cancelling for trains, cafés and open offices<br>• Feather-light fit you’ll forget you’re wearing<br>Free shipping and 30-day returns.</blockquote>

          <h2>Turn features into benefits</h2>
          <p>For every feature, ask “so what?” until you reach something the customer cares about:</p>
''' + ul(['“Stainless steel” → “won’t rust, even after years in the dishwasher”', '“1,000 mAh battery” → “charges your phone twice on one battery”', '“Organic cotton” → “soft on sensitive skin, no itchy tags”', '“Handmade” → “every piece is slightly different — yours is one of a kind”']) + '''

          <h2>Common mistakes</h2>
''' + ul(['Copying the manufacturer’s description (Google sees duplicate text, and so do customers).', 'Writing for everyone instead of one clear customer.', 'Walls of text — use short paragraphs and bullets.', 'Forgetting practical details: dimensions, care, delivery.']) + '''

          <h2>Write 50 descriptions in an afternoon</h2>
          <p>If you have a whole catalog to fill, <a href="login.html?mode=signup">Muse</a> uses exactly this structure. Choose “Product description”, paste the product name and a few facts, pick a tone — and get a headline, a paragraph and three benefit bullets in seconds.</p>
'''
article('product-description-guide.html', 'How to Write a Product Description That Sells (With Examples) — Muse', 'A simple 4-part structure for product descriptions that convert, with before-and-after examples and common mistakes to avoid.', 'How to write a product description that sells', '5 min read', 'art--3', body, ('Fill your store with descriptions that sell.', 'Muse writes them using this exact structure. 10 free every month.', 'Try Muse free'))

# ---------- 3. Email subject lines ----------
subj = {
 'Sales &amp; promotions': ['Your 20% off ends tonight', 'We saved you something 👀', 'The sale you asked for is here', 'Last chance: 3 hours left', 'Free shipping, this weekend only'],
 'Product launches': ['It’s finally here', 'Meet the newest addition to the family', 'You’re first to see this', 'We made this because you asked', 'New: [product] (and why we love it)'],
 'Newsletters': ['3 things worth your time this week', 'What we learned this month', 'The one tip that changed how we work', 'Quick question for you', 'Behind the scenes at [brand]'],
 'Win-back &amp; reminders': ['We miss you (and here’s 15% off)', 'Still thinking about it?', 'You left something in your cart', 'Is this goodbye?', 'A small thank-you for being with us'],
 'Outreach &amp; B2B': ['Idea for [company]’s Instagram', '15 minutes next week?', 'Quick win for your [specific goal]', 'Saw your post about [topic]', '[Mutual contact] suggested I reach out'],
}
body = '''          <p><strong>Your email is only as good as its subject line</strong> — if it isn’t opened, nothing else matters. Here are 25 proven subject lines you can adapt, plus the rules behind them.</p>
'''
for k, v in subj.items():
    body += f'          <h2>{k}</h2>\n' + ul(v) + '\n'
body += '''          <h2>5 rules for subject lines that get opened</h2>
''' + ol(['<strong>Keep it under 45 characters</strong> so it isn’t cut off on phones.', '<strong>Create curiosity or urgency</strong> — but never lie. Misleading subjects destroy trust.', '<strong>Personalize</strong> with the reader’s name, company or last purchase when you can.', '<strong>Use one emoji at most.</strong> It can help in promotions; it hurts in B2B.', '<strong>Test two versions.</strong> Most email tools let you A/B test the subject on a small group first.']) + '''
          <h2>Write the whole email, not just the subject</h2>
          <p><a href="login.html?mode=signup">Muse</a> writes complete marketing and outreach emails — subject line, friendly body and a clear call to action. Pick “Email”, describe your offer and send it in minutes.</p>
'''
article('email-subject-lines.html', '25 Email Subject Lines That Get Opened (With Examples) — Muse', 'Proven email subject lines for sales, launches, newsletters, win-back and B2B outreach, plus 5 rules for writing your own.', '25 email subject lines that get opened', '4 min read', 'art--2', body, ('Write emails people actually open.', 'Subject line, body and call to action in seconds. 10 free every month.', 'Try Muse free'))

# ---------- 4. Ukrainian guide ----------
body = '''          <p><strong>Ідеї для постів закінчуються в найневдаліший момент.</strong> Ось простий спосіб написати пост для Instagram чи Facebook за хвилину — навіть якщо ви не копірайтер.</p>

          <h2>Формула поста з 4 частин</h2>
''' + ol(['<strong>Гачок у першому рядку.</strong> Питання, сміливе твердження або знайома ситуація: «Понеділок без кави — це не понеділок».', '<strong>Одна конкретна деталь.</strong> Ціна, час, смак, цифра: «Лате на вівсяному — 65 грн до 10:00».', '<strong>Користь для читача.</strong> Що він отримає: зекономить час, порадує себе, вирішить проблему.', '<strong>Один заклик до дії.</strong> «Напишіть у коментарях», «Збережіть пост» або «Запис за посиланням у профілі».']) + '''

          <h2>Приклади для різних бізнесів</h2>
          <h3>Кав’ярня</h3>
          <blockquote>☕ Понеділок без кави — це не понеділок. До 10:00 будь-яке лате — 65 грн. Заходьте по дорозі на роботу, ми вже на місці!</blockquote>
          <h3>Салон краси</h3>
          <blockquote>💅 Новий тиждень — новий манікюр. На п’ятницю залишилось два вільні віконця. Пишіть у Direct, щоб записатися.</blockquote>
          <h3>Інтернет-магазин</h3>
          <blockquote>🛍️ Повернулися в наявність! Улюблений світшот наших клієнток — тепер і в кольорі «мокко». Відправка в день замовлення.</blockquote>

          <h2>Типові помилки</h2>
''' + ul(['Довгий вступ замість гачка — до другого речення ніхто не дочитає.', 'Багато закликів одразу («лайк, коментар, репост, підписка») — оберіть один.', 'Загальні слова («якісно», «недорого») замість конкретики.', '20 хештегів — достатньо 3–8 доречних.']) + '''

          <h2>Пост за 10 секунд</h2>
          <p><a href="login.html?mode=signup">Muse</a> пише пости, рекламу й описи товарів українською (і ще 10 мовами). Оберіть «Пост», опишіть товар чи акцію одним реченням, виберіть тон — і отримайте готовий текст. 10 генерацій щомісяця безкоштовно.</p>
'''
article('yak-napysaty-post-instagram.html', 'Як написати пост для Instagram за 1 хвилину: формула і приклади — Muse', 'Проста формула поста з 4 частин, приклади для кав’ярні, салону краси й інтернет-магазину та типові помилки.', 'Як написати пост для Instagram за 1 хвилину', '4 хв читання', 'art--1', body, ('Пост для вашого бізнесу — за 10 секунд.', 'Muse пише українською. 10 генерацій щомісяця безкоштовно.', 'Спробувати безкоштовно'), lang='uk', back='← До блогу')

# ================= Free tools =================
SCRIPTS = '  <script src="js/tools.js" defer></script>\n'
LANG_OPTS = ''.join(f'<option>{l}</option>' for l in ['English','Spanish','French','German','Portuguese','Italian','Polish','Ukrainian','Chinese','Hindi','Arabic'])

def hero(eyebrow, h1, p):
    return f'''
    <section class="page-hero">
      <div class="hero__glow" aria-hidden="true"></div>
      <div class="container">
        <span class="eyebrow reveal">{eyebrow}</span>
        <h1 class="reveal">{h1}</h1>
        <p class="reveal">{p}</p>
      </div>
    </section>'''

TOOL_CTA = '''
    <section class="section">
      <div class="container">
        <div class="cta reveal">
          <div>
            <h2>{h}</h2>
            <p>{p}</p>
          </div>
          <div class="cta__form">
            <a href="login.html?mode=signup" class="btn btn--light btn--lg">Start writing free</a>
          </div>
        </div>
      </div>
    </section>'''

def ai_tool(fname, title, desc, h1, sub, tool, prompt, fields, button, faq, cta):
    faq_html = '\n'.join(f'          <details class="reveal"{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(faq))
    body = f'''
  <main id="main">{hero('Free tool', h1, sub)}
    <section class="section" style="padding-top: 8px">
      <div class="container container--narrow">
        <div class="tool panel reveal">
          <form data-tool="{tool}" data-prompt="{prompt}" novalidate>
{fields}
            <button class="btn btn--primary btn--block btn--lg" type="submit">{button}</button>
            <p class="tool__note">Free, no sign-up · 3 tries per hour</p>
          </form>
          <div class="output__head tool__head"><b>Result</b><div class="output__actions"><span class="demo__status" data-tool-status></span><button type="button" class="btn btn--ghost btn--sm" data-tool-copy hidden>Copy</button></div></div>
          <div class="output" data-tool-output dir="auto" aria-live="polite"><p class="output__empty">Your results will appear here.</p></div>
        </div>
      </div>
    </section>

    <section class="section section--alt" id="faq">
      <div class="container container--narrow">
        <div class="section__head reveal"><h2>Questions</h2></div>
        <div class="faq">
{faq_html}
        </div>
      </div>
    </section>
{TOOL_CTA.format(h=cta[0], p=cta[1])}
  </main>
'''
    page(fname, title, desc, body, scripts=SCRIPTS)

ai_tool('hashtag-generator.html', 'Free AI Hashtag Generator for Instagram, TikTok &amp; LinkedIn — Muse',
  'Generate 30 relevant hashtags for your post in seconds: popular, niche and local tags. Free, no sign-up.',
  'Free AI hashtag generator', 'Describe your post and get 30 relevant hashtags — popular, niche and local — in seconds.',
  'hashtags', 'Hashtags for a {platform} post. Post or business: {topic}. Location (if any): {place}.',
  f'''            <label class="field"><span>What is your post or business about?</span><textarea name="topic" dir="auto" rows="3" maxlength="400" required placeholder="e.g. New autumn pumpkin latte at our cozy coffee shop"></textarea></label>
            <div class="field-row">
              <label class="field"><span>Platform</span><select name="platform"><option>Instagram</option><option>TikTok</option><option>LinkedIn</option><option>X / Twitter</option><option>YouTube</option></select></label>
              <label class="field"><span>Language</span><select name="language">{LANG_OPTS}</select></label>
            </div>
            <label class="field"><span>City or country <small>(optional)</small></span><input name="place" maxlength="60" placeholder="e.g. Lisbon"></label>''',
  '✦ Generate hashtags',
  [('How many hashtags should I use?', 'On Instagram, 3–10 well-chosen hashtags usually work better than 30 random ones. Mix a few popular tags with niche and local ones that describe exactly what you post.'),
   ('Do hashtags still matter?', 'Yes, but as a way to describe your content to the platform and to people searching a topic. Relevance matters more than volume.'),
   ('Is the tool really free?', 'Yes. You can generate hashtags a few times an hour without an account. A free Muse account gives you 10 full generations every month.')],
  ('Need the caption too?', 'Muse writes the whole post — caption, call to action and hashtags — in your brand’s tone.'))

ai_tool('business-name-generator.html', 'Free AI Business Name Generator — Muse',
  'Get 15 creative business and brand name ideas with explanations in seconds. Free AI name generator, no sign-up.',
  'Free AI business name generator', 'Describe your idea and get 15 creative name ideas, each with a short explanation.',
  'names', 'Business: {topic}. Style: {style}.',
  f'''            <label class="field"><span>Describe your business</span><textarea name="topic" dir="auto" rows="3" maxlength="400" required placeholder="e.g. Handmade soy candles with natural scents, sold online"></textarea></label>
            <div class="field-row">
              <label class="field"><span>Style</span><select name="style"><option>modern and short</option><option>playful</option><option>elegant and premium</option><option>descriptive</option><option>made-up word</option></select></label>
              <label class="field"><span>Language</span><select name="language">{LANG_OPTS}</select></label>
            </div>''',
  '✦ Generate names',
  [('How do I choose the right name?', 'Say it out loud, check that it is easy to spell, and make sure it still fits if your business grows. Short names are easier to remember.'),
   ('Is the name available?', 'The tool suggests ideas only. Before you decide, check that the domain, social media handles and trademark are free in your country.'),
   ('Is the tool really free?', 'Yes. You can generate names a few times an hour without an account.')],
  ('Got your name? Now write your first posts.', 'Muse writes ads, posts and product descriptions for your new brand in seconds.'))

# Character counter (no AI)
LIMITS = [('Instagram caption', 2200), ('X / Twitter post', 280), ('LinkedIn post', 3000), ('TikTok caption', 4000), ('Facebook ad primary text (recommended)', 125),
          ('Google Ads headline', 30), ('Google Ads description', 90), ('YouTube title', 100), ('Etsy listing title', 140), ('Meta description (SEO)', 160), ('SMS', 160)]
rows = '\n'.join(f'''            <li class="limit" data-limit="{n}"><span class="limit__name">{name}</span><span class="limit__max">{n:,}</span><span class="limit__bar" aria-hidden="true"></span><span class="limit__left"></span></li>''' for name, n in LIMITS)
body = f'''
  <main id="main">{hero('Free tool', 'Character counter for social media', 'Paste your text to count characters and words and see if it fits Instagram, X, LinkedIn, TikTok, Google Ads and more.')}
    <section class="section" style="padding-top: 8px">
      <div class="container container--narrow">
        <div class="tool panel reveal">
          <label class="field"><span>Your text</span><textarea id="counterInput" dir="auto" rows="8" placeholder="Paste or type your caption, ad or post here…"></textarea></label>
          <div class="stats">
            <div><strong id="statChars">0</strong><span>characters</span></div>
            <div><strong id="statNoSpaces">0</strong><span>without spaces</span></div>
            <div><strong id="statWords">0</strong><span>words</span></div>
            <div><strong id="statLines">0</strong><span>lines</span></div>
            <div><strong id="statHashtags">0</strong><span>hashtags</span></div>
          </div>
          <ul class="limits">
{rows}
          </ul>
          <p class="tool__note">Limits are typical maximums and can change. Emojis count as one character here; some platforms count them as two.</p>
        </div>
      </div>
    </section>
{TOOL_CTA.format(h='Too long? Let Muse shorten it.', p='Paste your text into Muse, choose “Shorter” and get a version that fits — in seconds.')}
  </main>
'''
page('character-counter.html', 'Character Counter for Instagram, X, LinkedIn &amp; Ads — Muse', 'Free character and word counter with limits for Instagram, X/Twitter, LinkedIn, TikTok, Google Ads, YouTube, Etsy and SEO.', body, scripts=SCRIPTS)

# Hub
cards = [('hashtag-generator.html', 'art--4', '#️⃣', 'Hashtag generator', '30 relevant hashtags for any post, in seconds.'),
         ('business-name-generator.html', 'art--2', '💡', 'Business name generator', '15 creative name ideas with explanations.'),
         ('character-counter.html', 'art--3', '🔢', 'Character counter', 'Check if your text fits every platform.')]
html_cards = '\n'.join(f'''          <a class="post-card reveal" href="{h}">
            <div class="art {a}" aria-hidden="true"></div>
            <div class="post-card__body"><span class="tag">{i} Free</span><h3>{t}</h3><p>{d}</p></div>
          </a>''' for h, a, i, t, d in cards)
body = f'''
  <main id="main">{hero('Free tools', 'Free marketing tools', 'Small helpers for busy business owners. No sign-up needed.')}
    <section class="section" style="padding-top: 8px">
      <div class="container">
        <div class="posts">
{html_cards}
        </div>
      </div>
    </section>
{TOOL_CTA.format(h='Want the whole post written for you?', p='Muse writes ads, social posts, product descriptions and emails in 11 languages. 10 free every month.')}
  </main>
'''
page('tools.html', 'Free Marketing Tools: Hashtags, Business Names, Character Counter — Muse', 'Free tools for small businesses: AI hashtag generator, business name generator and a character counter for social media.', body, scripts=SCRIPTS)

# ================= More articles =================

# 1. Review replies (English)
body = '''          <p><strong>Every review is a public conversation.</strong> Future customers read your replies as carefully as the reviews themselves. Here’s how to answer, with templates you can adapt.</p>

          <h2>The 4-step reply formula</h2>
''' + ol(['<strong>Thank them by name.</strong> It shows a real person read the review.', '<strong>Mention something specific</strong> they wrote, so it doesn’t sound copy-pasted.', '<strong>Fix or explain</strong> — for negative reviews, apologise once and say what you’re doing about it.', '<strong>Invite them back</strong> or offer to continue privately.']) + '''

          <h2>Templates for positive reviews</h2>
''' + ul(['“Thank you, Anna! We’re so happy you loved the cinnamon buns — we’ll save you one next time ☕”',
          '“Thanks for the kind words, Mark. Our team works hard on fast delivery, and it means a lot that you noticed.”',
          '“Five stars from a regular — that’s the best compliment! See you on Saturday?”',
          '“We really appreciate you taking the time to write this, Priya. Enjoy your new boots!”']) + '''

          <h2>Templates for negative reviews</h2>
''' + ul(['“Hi Tom, I’m sorry your order arrived late — that’s not the experience we want for you. I’ve sent you a direct message with a refund for the delivery cost.”',
          '“Thank you for the honest feedback, Lisa. You’re right that the wait was too long on Friday. We’ve added a second barista for weekends.”',
          '“I’m sorry the size didn’t fit, Carlos. Returns are free — reply to your order email and we’ll send a new size right away.”',
          '“We hear you, and we’re sorry. Could you email us at the address on our website so we can make this right?”']) + '''

          <h2>Mistakes to avoid</h2>
''' + ul(['Arguing with the customer in public — even when they’re wrong.', 'Replying weeks later. Aim for 24–48 hours.', 'The same generic reply under every review.', 'Sharing personal details or order numbers publicly.']) + '''

          <h2>Reply to 20 reviews in 5 minutes</h2>
          <p>In <a href="login.html?mode=signup">Muse</a>, choose “Review reply”, paste the review and get a warm, specific answer in your brand’s tone — positive or negative, in 11 languages.</p>
'''
article('review-reply-templates.html', 'How to Reply to Customer Reviews: Formula + 8 Templates — Muse', 'A simple 4-step formula for replying to positive and negative customer reviews, with ready-to-use templates.', 'How to reply to customer reviews (with templates)', '5 min read', 'art--6', body, ('Never stare at a review again.', 'Muse writes thoughtful review replies in seconds. 10 free every month.', 'Try Muse free'))

# 2. Etsy listing (English)
body = '''          <p><strong>On Etsy, your listing has two readers:</strong> the search engine and the shopper. A great listing works for both. Here’s a template that does.</p>

          <h2>1. The title: what it is, for whom, what makes it special</h2>
          <p>Lead with the words shoppers actually type, then add details. Keep it readable — Etsy titles can be up to 140 characters, but the first few words matter most.</p>
          <blockquote>Soy Candle — Lavender &amp; Cedar, Hand-Poured, 40-Hour Burn, Gift for Her</blockquote>

          <h2>2. The first two lines</h2>
          <p>Only the beginning of your description shows before “Read more”. Use it for the main benefit and the feeling, not for shipping policies.</p>

          <h2>3. Benefit bullets</h2>
''' + ul(['What it’s made of (and why that’s better)', 'Size, weight and what’s included', 'How long it lasts or how to care for it', 'Who it’s perfect for (gift ideas sell)', 'Personalisation options, if any']) + '''

          <h2>4. Tags</h2>
          <p>Etsy allows 13 tags. Use all of them, mix broad and specific phrases (“lavender candle”, “gift for mom”, “cozy home decor”), and don’t repeat your title word for word.</p>

          <h2>Listing template</h2>
          <blockquote>[Main benefit in one line]<br>[1–2 sentences: who it’s for and how it feels]<br>• Made from …<br>• Size …<br>• Lasts …<br>• Perfect for …<br>Ships in [X] days, gift wrapping available.</blockquote>

          <h2>Write every listing in seconds</h2>
          <p><a href="login.html?mode=signup">Muse</a> has a “Marketplace listing” format: it writes the title, five benefit bullets and 13 search tags for Etsy, Amazon or Shopify in one go.</p>
'''
article('etsy-listing-description.html', 'How to Write an Etsy Listing That Sells (Template + Example) — Muse', 'Write Etsy titles, descriptions and tags that rank and convert, with a copy-and-paste listing template.', 'How to write an Etsy listing that sells', '5 min read', 'art--2', body, ('List products faster.', 'Titles, bullets and tags for every product in seconds. 10 free every month.', 'Try Muse free'))

# 3. Spanish
body = '''          <p><strong>¿Te quedas sin ideas para Instagram?</strong> Aquí tienes 30 ideas de publicaciones para pequeños negocios, agrupadas por objetivo. Elige una al día y tendrás contenido para todo el mes.</p>

          <h2>Para que te conozcan</h2>
''' + ul(['Presenta al equipo: quién hay detrás del negocio', 'Un día normal entre bastidores', 'Cómo empezó tu negocio', 'Tu espacio de trabajo o tu tienda', 'Un error que cometiste y lo que aprendiste', 'Tu producto favorito y por qué']) + '''
          <h2>Para vender sin parecer pesado</h2>
''' + ul(['Antes y después de usar tu producto', 'Las preguntas que más te hacen (con respuestas)', 'Tres formas de usar un mismo producto', 'Una oferta con fecha límite', 'Un pack o regalo para una fecha especial', 'El producto más vendido del mes']) + '''
          <h2>Para generar comentarios</h2>
''' + ul(['«¿Cuál elegirías: A o B?»', 'Rellena la frase: «Mi café perfecto es…»', 'Encuesta en stories y resultado en el feed', 'Pide recomendaciones a tus seguidores', 'Un pequeño sorteo con una regla sencilla', 'Un dato curioso de tu sector']) + '''
          <h2>Para generar confianza</h2>
''' + ul(['La reseña de un cliente (con su permiso)', 'Cómo se fabrica o prepara tu producto', 'Tus valores: ingredientes, materiales, proveedores locales', 'Un hito: aniversario, cliente número 1.000', 'Respuesta a una crítica y lo que cambiaste', 'Un consejo útil de tu especialidad']) + '''
          <h2>Para el día a día</h2>
''' + ul(['Novedades de la semana', 'Horarios especiales y festivos', 'Colaboración con otro negocio local', 'Un meme o humor de tu sector', 'Agradecimiento a tus clientes', 'Lo que viene el mes que viene']) + '''

          <h2>Convierte cada idea en un post listo</h2>
          <p>Con <a href="login.html?mode=signup">Muse</a> eliges «Post», describes la idea en una frase y recibes el texto con llamada a la acción y hashtags, en español y en 10 idiomas más.</p>
'''
article('ideas-posts-instagram.html', '30 ideas de posts para Instagram para pequeños negocios — Muse', 'Ideas de publicaciones para Instagram organizadas por objetivo: darte a conocer, vender, generar comentarios y confianza.', '30 ideas de posts para Instagram para pequeños negocios', '5 min de lectura', 'art--4', body, ('Escribe tu próximo post en segundos.', 'Muse escribe en español y en 10 idiomas más. 10 textos gratis al mes.', 'Probar gratis'), lang='es', back='← Volver al blog')

# 4. French
body = '''          <p><strong>Une bonne fiche produit répond à une seule question :</strong> « Pourquoi est-ce que je l’achèterais ? ». Voici une structure simple, avec un exemple avant/après.</p>

          <h2>La structure en 4 parties</h2>
''' + ol(['<strong>Un titre avec le bénéfice principal.</strong> Pas « Mug en céramique 350 ml », mais « Le mug qui garde votre café chaud toute la réunion ».', '<strong>Un court paragraphe émotionnel</strong> : pour qui, et comment sa journée sera meilleure.', '<strong>Trois puces de bénéfices</strong> : transformez chaque caractéristique en avantage.', '<strong>Levez le dernier doute</strong> : taille, matière, délais de livraison, retours.']) + '''

          <h2>Exemple</h2>
          <h3>Avant</h3>
          <blockquote>Bougie parfumée. Cire de soja. 200 g. Parfum lavande.</blockquote>
          <h3>Après</h3>
          <blockquote>Votre moment de calme, en pot. Coulée à la main avec de la cire de soja et une lavande douce, elle transforme votre salon en refuge après une longue journée.<br>• 40 heures de combustion propre, sans fumée noire<br>• Cire 100 % végétale et mèche en coton<br>• Idée cadeau prête à offrir, emballage inclus<br>Expédiée sous 48 h.</blockquote>

          <h2>Les erreurs à éviter</h2>
''' + ul(['Copier la description du fabricant (Google et vos clients le remarquent).', 'Écrire pour tout le monde au lieu d’un client précis.', 'Des pavés de texte : préférez phrases courtes et puces.', 'Oublier les informations pratiques.']) + '''

          <h2>Rédigez tout votre catalogue en un après-midi</h2>
          <p><a href="login.html?mode=signup">Muse</a> utilise exactement cette structure : choisissez « Fiche produit », indiquez le produit et quelques détails, et obtenez un titre, un paragraphe et trois bénéfices en quelques secondes.</p>
'''
article('fiche-produit-qui-vend.html', 'Comment écrire une fiche produit qui vend (avec exemples) — Muse', 'Une structure simple en 4 parties pour des fiches produits qui convertissent, avec un exemple avant/après.', 'Comment écrire une fiche produit qui vend', '5 min de lecture', 'art--3', body, ('Des fiches produits qui vendent, en quelques secondes.', 'Muse écrit en français et en 10 autres langues. 10 textes gratuits par mois.', 'Essayer gratuitement'), lang='fr', back='← Retour au blog')

# 5. Hindi
body = '''          <p><strong>हर दिन क्या पोस्ट करें, यह सोचना मुश्किल है।</strong> यहाँ छोटे बिज़नेस के लिए 24 आसान Instagram पोस्ट आइडिया हैं, जिन्हें आप आज से इस्तेमाल कर सकते हैं।</p>

          <h2>लोगों से जुड़ने के लिए</h2>
''' + ul(['अपनी टीम से मिलवाएँ', 'आपका बिज़नेस कैसे शुरू हुआ', 'काम का एक आम दिन — बिहाइंड द सीन्स', 'आपकी दुकान या वर्कस्पेस की झलक', 'आपका पसंदीदा प्रोडक्ट और उसकी वजह', 'एक गलती और उससे मिली सीख']) + '''
          <h2>बिक्री बढ़ाने के लिए</h2>
''' + ul(['प्रोडक्ट इस्तेमाल करने से पहले और बाद', 'ग्राहकों के सबसे आम सवाल और जवाब', 'एक प्रोडक्ट के तीन इस्तेमाल', 'त्योहार का ख़ास ऑफ़र (दिवाली, होली, राखी)', 'गिफ़्ट कॉम्बो', 'महीने का बेस्टसेलर']) + '''
          <h2>कमेंट और बातचीत के लिए</h2>
''' + ul(['“आप कौन-सा चुनेंगे: A या B?”', 'वाक्य पूरा करें: “मेरी परफ़ेक्ट चाय है…”', 'स्टोरी में पोल, फ़ीड में नतीजा', 'आसान नियमों वाला छोटा गिवअवे', 'अपने फ़ील्ड से जुड़ा मज़ेदार तथ्य', 'फ़ॉलोअर्स से सुझाव माँगें']) + '''
          <h2>भरोसा बनाने के लिए</h2>
''' + ul(['ग्राहक का रिव्यू (उनकी अनुमति से)', 'प्रोडक्ट कैसे बनता है', 'आपकी क्वालिटी और लोकल सप्लायर्स', 'कोई उपलब्धि: सालगिरह या 1,000वाँ ग्राहक', 'आपके फ़ील्ड की एक काम की टिप', 'ग्राहकों को धन्यवाद']) + '''

          <h2>हर आइडिया से तैयार पोस्ट</h2>
          <p><a href="login.html?mode=signup">Muse</a> में “सोशल पोस्ट” चुनें, आइडिया एक वाक्य में लिखें और हिन्दी या अंग्रेज़ी में कॉल-टू-एक्शन और हैशटैग के साथ तैयार पोस्ट पाएँ। हर महीने 10 जनरेशन मुफ़्त।</p>
'''
article('instagram-post-ideas-hindi.html', 'छोटे बिज़नेस के लिए 24 Instagram पोस्ट आइडिया — Muse', 'छोटे बिज़नेस के लिए आसान Instagram पोस्ट आइडिया: लोगों से जुड़ने, बिक्री बढ़ाने, कमेंट पाने और भरोसा बनाने के लिए।', 'छोटे बिज़नेस के लिए 24 Instagram पोस्ट आइडिया', '4 मिनट', 'art--1', body, ('अपनी अगली पोस्ट सेकंडों में लिखें।', 'Muse हिन्दी और 10 और भाषाओं में लिखता है। हर महीने 10 मुफ़्त।', 'मुफ़्त आज़माएँ'), lang='hi', back='← ब्लॉग पर वापस')

# 6. Ukrainian
body = '''          <p><strong>Відгуки читають не лише ті, хто їх залишив.</strong> Майбутні клієнти дивляться, як ви відповідаєте, особливо на негатив. Ось проста формула й готові шаблони.</p>

          <h2>Формула відповіді з 4 кроків</h2>
''' + ol(['<strong>Подякуйте на ім’я.</strong> Так видно, що відповідає жива людина.', '<strong>Згадайте конкретну деталь</strong> з відгуку, щоб відповідь не виглядала шаблонною.', '<strong>Виправте або поясніть.</strong> На негатив — одне вибачення й конкретна дія.', '<strong>Запросіть повернутися</strong> або продовжити розмову в особистих повідомленнях.']) + '''

          <h2>Шаблони для позитивних відгуків</h2>
''' + ul(['«Дякуємо, Ірино! Дуже раді, що вам сподобалися круасани — наступного разу відкладемо для вас найсвіжіший ☕»',
          '«Дякуємо за теплі слова, Андрію! Ми дуже стараємося з доставкою, і приємно, що ви це помітили.»',
          '«П’ять зірок від постійної клієнтки — найкращий комплімент! Чекаємо в суботу?»',
          '«Дякуємо, що знайшли час написати! Нехай нова сумка радує щодня.»']) + '''

          <h2>Шаблони для негативних відгуків</h2>
''' + ul(['«Олено, перепрошуємо за затримку замовлення — це не той досвід, який ми хочемо вам дати. Написали вам в особисті, щоб компенсувати доставку.»',
          '«Дякуємо за чесний відгук. Ви праві: у п’ятницю довелося довго чекати. Ми додали другого бариста на вихідні.»',
          '«Шкода, що розмір не підійшов. Повернення безкоштовне — напишіть у відповідь на лист із замовленням, і ми одразу надішлемо інший розмір.»',
          '«Нам дуже прикро. Напишіть, будь ласка, нам у Direct — розберемося й усе виправимо.»']) + '''

          <h2>Чого не робити</h2>
''' + ul(['Сперечатися з клієнтом публічно, навіть якщо він не правий.', 'Відповідати через кілька тижнів — найкраще протягом 1–2 днів.', 'Ставити однакову відповідь під усіма відгуками.', 'Публікувати номер замовлення чи особисті дані.']) + '''

          <h2>20 відповідей за 5 хвилин</h2>
          <p>У <a href="login.html?mode=signup">Muse</a> оберіть «Відповідь на відгук», вставте текст відгуку — і отримайте теплу, конкретну відповідь вашим тоном, українською чи будь-якою з 11 мов.</p>
'''
article('yak-vidpovidaty-na-vidguky.html', 'Як відповідати на відгуки клієнтів: формула і 8 шаблонів — Muse', 'Проста формула відповіді на позитивні й негативні відгуки та готові шаблони для малого бізнесу.', 'Як відповідати на відгуки клієнтів', '5 хв читання', 'art--6', body, ('Більше ніяких мук над відгуками.', 'Muse пише відповіді на відгуки за секунди. 10 генерацій щомісяця безкоштовно.', 'Спробувати безкоштовно'), lang='uk', back='← До блогу')

# ================= Blog index =================
POSTS = [
    ('instagram-caption-ideas.html', 'art--4', 'Ideas', '35 Instagram caption ideas for small businesses', 'Copy-and-paste captions for cafés, salons, shops, gyms and restaurants.', 'en'),
    ('review-reply-templates.html', 'art--6', 'Templates', 'How to reply to customer reviews', 'A 4-step formula and 8 templates for positive and negative reviews.', 'en'),
    ('product-description-guide.html', 'art--3', 'Guide', 'How to write a product description that sells', 'A simple 4-part structure with before-and-after examples.', 'en'),
    ('etsy-listing-description.html', 'art--2', 'Guide', 'How to write an Etsy listing that sells', 'Titles, descriptions and tags that rank and convert.', 'en'),
    ('email-subject-lines.html', 'art--2', 'Ideas', '25 email subject lines that get opened', 'For sales, launches, newsletters, win-back and B2B outreach.', 'en'),
    ('ideas-posts-instagram.html', 'art--4', 'Español', '30 ideas de posts para Instagram', 'Ideas para pequeños negocios, organizadas por objetivo.', 'es'),
    ('fiche-produit-qui-vend.html', 'art--3', 'Français', 'Comment écrire une fiche produit qui vend', 'Une structure en 4 parties, avec un exemple avant/après.', 'fr'),
    ('instagram-post-ideas-hindi.html', 'art--1', 'हिन्दी', '24 Instagram पोस्ट आइडिया', 'छोटे बिज़नेस के लिए आसान पोस्ट आइडिया।', 'hi'),
    ('yak-napysaty-post-instagram.html', 'art--1', 'Українською', 'Як написати пост для Instagram за 1 хвилину', 'Проста формула з 4 частин і приклади для малого бізнесу.', 'uk'),
    ('yak-vidpovidaty-na-vidguky.html', 'art--6', 'Українською', 'Як відповідати на відгуки клієнтів', 'Формула відповіді й 8 готових шаблонів.', 'uk'),
]
cards = '\n'.join(f'''          <a class="post-card reveal" href="{h}" lang="{l}">
            <div class="art {a}" aria-hidden="true"></div>
            <div class="post-card__body"><span class="tag">{t}</span><h3>{ti}</h3><p>{d}</p></div>
          </a>''' for h, a, t, ti, d, l in POSTS)
page('blog.html', 'Blog — Muse', 'Practical guides on writing marketing content with AI.', f'''
  <main id="main">
    <section class="page-hero">
      <div class="hero__glow" aria-hidden="true"></div>
      <div class="container">
        <span class="eyebrow reveal">Blog</span>
        <h1 class="reveal">Write better marketing <span class="gradient-text">with AI</span></h1>
        <p class="reveal">Practical guides for small businesses and creators.</p>
      </div>
    </section>

    <section class="section" style="padding-top: 24px">
      <div class="container">
        <div class="posts posts--two">
          <a class="post-card post-card--featured reveal" href="blog-post.html">
            <div class="art art--5" aria-hidden="true"></div>
            <div class="post-card__body"><span class="tag">Guide</span><h3>How to get great marketing copy from AI</h3><p>Four habits that turn generic AI text into copy your customers actually respond to.</p><div class="meta" style="justify-content:flex-start">5 min read</div></div>
          </a>
{cards}
        </div>
      </div>
    </section>
  </main>
''', active='blog')

# ================= Sitemap =================
SITE = 'https://hozvoc-svg.github.io/-/'
PUBLIC = ['about.html', 'blog.html', 'blog-post.html', 'privacy.html', 'terms.html', 'tools.html', 'hashtag-generator.html',
          'business-name-generator.html', 'character-counter.html', 'email-subject-lines.html'] + [p[0] for p in POSTS]
sitemap_path = os.path.join(OUT, 'sitemap.xml')
xml = open(sitemap_path, encoding='utf-8').read()
for f in dict.fromkeys(PUBLIC):
    loc = f'{SITE}{f}'
    if f'<loc>{loc}</loc>' not in xml:
        xml = xml.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>2026-10-23</lastmod></url>\n</urlset>')
open(sitemap_path, 'w', encoding='utf-8').write(xml)
print('pages built')
