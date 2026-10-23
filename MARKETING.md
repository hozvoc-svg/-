# Як привести перших клієнтів на Muse

> ⚠️ **Спочатку запуск, потім реклама.** Поки сайт не запущено на Vercel (див. `README.md`), реєстрація
> і генерація не працюють. Якщо привести людей раніше, вони побачать помилку й не повернуться.

## Сайт 7 мовами: давайте людям посилання їхньою мовою

| Аудиторія | Сторінка | Де шукати клієнтів |
|---|---|---|
| Україна | `uk.html` | Instagram, Facebook-групи, Telegram-чати підприємців |
| США, Велика Британія, світ | `index.html` | Reddit, Product Hunt, LinkedIn, каталоги AI |
| Іспанія, Латинська Америка | `es.html` | Instagram, TikTok, Facebook-групи emprendedores |
| Франція, Канада, Африка | `fr.html` | LinkedIn, Facebook-групи entrepreneurs |
| Індія | `hi.html` | Instagram, YouTube, WhatsApp-спільноти, LinkedIn |
| Близький Схід | `ar.html` | Instagram, TikTok, Snapchat, X |
| Китайськомовні продавці | `zh.html` | Китайськомовні спільноти продавців Amazon/Shopify |

Наприклад: `https://muse-ai.vercel.app/es.html`. Перемикач мов 🌐 є вгорі кожної сторінки.
Індія та Латинська Америка — величезні ринки малого бізнесу, і конкурентів, які пишуть їхньою мовою, там менше.

## 0. Красиве посилання (без «hozvoc»)

Безкоштовна адреса GitHub завжди містить ім'я акаунта (`hozvoc-svg.github.io`). Посилання без нього:

- **Vercel (безкоштовно, рекомендовано):** при запуску (README, крок 4) назвіть проєкт `muse-ai`.
  Адреса буде **https://muse-ai.vercel.app** (якщо назва зайнята, спробуйте `muse-copy`, `musewrite`, `muse-ua`).
  Змінити можна будь-коли: Vercel → Project → Settings → General → Project Name.
- **Власний домен (~$10–15/рік):** купіть, наприклад, `musewrite.com` на Namecheap або Cloudflare й
  підключіть у Vercel → Settings → Domains. Виглядає найпрофесійніше.

Після цього напишіть мені нову адресу, і я оновлю всі посилання на сайті (прев'ю, sitemap).

### Якщо хочете гарнішу адресу на GitHub (необов'язково)

Зараз адреса `hozvoc-svg.github.io/-/`, бо репозиторій називається «-». Щоб змінити:

1. Відкрийте https://github.com/hozvoc-svg/- → **Settings** (вгорі справа).
2. У полі **Repository name** напишіть `muse-ai` → **Rename**.
3. Нова адреса: **https://hozvoc-svg.github.io/muse-ai/**. Напишіть мені, і я оновлю посилання в sitemap
   та прев'ю для соцмереж.

На Vercel назвіть проєкт `muse-ai`, і основна адреса сервісу буде **https://muse-ai.vercel.app**
(якщо назва вільна). Власний домен на кшталт `musewrite.com` коштує ~$10–15 на рік, його можна
підключити у Vercel → Settings → Domains.

## 1. План на перші 2 тижні

| День | Що зробити | Час |
|---|---|---|
| 1 | Запустити сайт (README), зареєструватися самому, перевірити оплату в тестовому режимі | 1 год |
| 2 | Додати сайт у Google Search Console (нижче) | 10 хв |
| 2 | Додати Muse в каталоги AI-інструментів (список нижче) | 1 год |
| 3–7 | Щодня написати 5 особистих повідомлень малим бізнесам (шаблони нижче) | 30 хв/день |
| 3–7 | Опублікувати 1 пост або коротке відео на день (тексти нижче) | 20 хв/день |
| 8 | Пост на Reddit і Indie Hackers | 30 хв |
| 10 | Запуск на Product Hunt (у вівторок або середу) | 1 год |
| 14 | Подивитися, звідки прийшли люди, і робити більше того, що спрацювало | 30 хв |

Мета перших двох тижнів: **20 безкоштовних користувачів і 1–3 платних**. Це нормальний старт.

## 2. Google Search Console (щоб сайт знаходили в Google)

1. https://search.google.com/search-console → **Add property** → **URL prefix** → адреса вашого сайту.
2. Підтвердження: оберіть **HTML tag**, скопіюйте рядок `<meta name="google-site-verification" ...>` і
   надішліть мені, я додам його на сайт. Або вставте його самі в `index.html` перед `</head>`.
3. **Sitemaps** → введіть `sitemap.xml` → **Submit**.

У блозі вже є 5 статей, написаних під пошукові запити: «Instagram caption ideas», «product description»,
«email subject lines» та українською «як написати пост для Instagram». Google зазвичай починає показувати
нові сайти через 2–8 тижнів.

## 3. Каталоги AI-інструментів (безкоштовний трафік)

Люди шукають AI-сервіси саме там. Додайте Muse в кожен (деякі просять плату за швидке розміщення,
безкоштовного варіанта достатньо):

- **There's An AI For That**: theresanaiforthat.com (Submit)
- **Futurepedia**: futurepedia.io (Submit a tool)
- **Toolify**: toolify.ai (Submit AI)
- **SaaSHub**: saashub.com (Submit product)
- **AlternativeTo**: alternativeto.net (як альтернатива Jasper / Copy.ai)
- **BetaList**: betalist.com (для нових стартапів)

**Опис для каталогів (англійською):**

> **Muse — AI copywriter for small businesses.** Write ads, social media posts, product descriptions,
> emails, blog outlines and slogans in seconds. 6 tones of voice, 11 languages (including Chinese, Hindi, Arabic,
> Spanish, German and French), saved history, commercial use. Powered by Claude. Free plan with
> 10 generations a month; paid plans from $19/month.

Категорії: Copywriting, Marketing, Social Media, E-commerce.

## 4. Особисті повідомлення (найшвидший спосіб отримати перших клієнтів)

Пишіть **власникам малого бізнесу**, у яких бачите активний, але слабкий Instagram: кав'ярні, салони,
магазини одягу, кондитерські. **Правила:**
- Тільки особисті повідомлення, по 5–10 на день, кожне з деталлю саме про цей бізнес.
- Спочатку дайте користь (готовий текст), а не продавайте.
- Якщо людина не відповіла, не пишіть повторно більше одного разу. Масові розсилки = спам і блокування.

**Українською:**

> Добрий день! Я гортав(-ла) ваш Instagram, у вас дуже гарні фото [конкретний товар/страва].
> Я зробив(-ла) сервіс, який пише тексти для постів за кілька секунд, і для прикладу написав(-ла)
> підпис саме для вашого [товару]:
>
> «[вставте текст, згенерований у Muse]»
>
> Можете використати безкоштовно 🙂 Якщо сподобається, там є 10 безкоштовних генерацій щомісяця:
> [посилання]. Буду вдячний(-на) за будь-який відгук!

**English:**

> Hi [name]! Love what you're doing with [specific product/post]. I built a small tool that writes
> social posts in seconds, and made this caption for your [product] as an example:
>
> "[paste caption generated in Muse]"
>
> Feel free to use it! If it's helpful, Muse gives you 10 free posts a month: [link].
> Any feedback would mean a lot.

## 5. Готові пости для соцмереж

**Facebook / Instagram (українською):**

> Зробив(-ла) сервіс, який пише тексти для бізнесу за 10 секунд ✍️
>
> Реклама, пости, описи товарів, email-розсилки — просто опишіть, що продаєте, оберіть тон і мову.
> Працює українською та ще 10 мовами.
>
> 10 генерацій щомісяця безкоштовно, без картки. Буду радий(-а) відгукам 🙏
> 👉 [посилання]

**LinkedIn (English):**

> I just launched Muse: an AI copywriter for small businesses.
>
> Most small business owners don't have time (or budget) for a copywriter. Muse writes ads, social posts,
> product descriptions and emails in seconds, in the tone and language you choose.
>
> It's free to try (10 generations a month). I'd love your honest feedback 👇
> [link]

**Reddit r/SideProject, Indie Hackers (English):**

> **Title:** I built an AI copywriter for small businesses: feedback welcome
>
> Hi all! I built Muse, a simple tool that writes marketing copy (ads, social posts, product descriptions,
> emails, slogans) for small businesses. Pick a format, describe your product in a sentence, choose a tone
> and language, and get publish-ready text.
>
> Stack: plain HTML/JS, Vercel functions, Supabase, Lemon Squeezy, Claude API.
> Free tier: 10 generations/month. There's also a no-signup demo on the homepage.
>
> What would make this useful enough for you to pay for? [link]

(На Reddit пишіть як автор, що просить відгук, а не як реклама. Спершу прочитайте правила сабреддиту.)

**Product Hunt:**
- Name: Muse
- Tagline: *AI copywriter for small businesses: posts, ads and emails in seconds*
- Description: як для каталогів вище
- Перший коментар: коротко, чому ви це зробили і що буде далі

## 6. Ідеї для коротких відео (TikTok, Reels, Shorts)

Знімайте екран телефону або комп'ютера, 15–30 секунд, з текстом на екрані:

1. **«Реклама для кав'ярні за 10 секунд».** Вводите запит → натискаєте Generate → показуєте результат.
2. **«Пишу опис товару: до і після».** Сухий опис від виробника vs текст із Muse.
3. **«3 підписи для Instagram, коли немає ідей».** Генеруєте три варіанти для різних бізнесів.

У кінці кожного відео: «Посилання в профілі, 10 текстів на місяць безкоштовно».

## 7. Що відстежувати

- **Скільки реєстрацій** на день: Supabase → Authentication → Users.
- **Скільки генерацій**: Supabase → Table Editor → generations.
- **Скільки оплат**: Lemon Squeezy → Dashboard.
- **Витрати на AI**: console.anthropic.com → Usage.

Якщо люди реєструються, але не платять, напишіть кільком із них і спитайте чому.
Їхні відповіді — найцінніша інформація для покращення продукту.
