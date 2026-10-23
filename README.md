# Muse — AI-копірайтер із підпискою

Справжній онлайн-сервіс: люди реєструються, пишуть рекламу, пости, описи товарів і email за допомогою AI
та платять щомісячну підписку.

- **Головна сторінка** (`index.html`) продає сервіс і має безкоштовне демо (3 спроби без реєстрації).
- **Кабінет** (`app.html`): 6 форматів текстів, 6 тонів, 8 мов, історія, кредити, оплата.
- **Вхід і реєстрація** (`login.html`): email + пароль або Google.
- **Оплата підписки** через Lemon Squeezy, тарифи вмикаються автоматично.

## Як це заробляє

| Тариф | Ціна | Генерацій на місяць | Ваші витрати на AI (макс.) | Ваш дохід* |
|---|---|---|---|---|
| Free | $0 | 10 | ~$0.20 | — |
| Creator | $19 | 300 | ~$6 | ~$11–13 |
| Pro | $49 | 1 000 | ~$20 | ~$24–27 |

\* Після комісії Lemon Squeezy (~5% + 50¢) і максимальних витрат на AI. Більшість людей використовує
не всі кредити, тож реальний дохід зазвичай вищий. Одна генерація коштує ~1–2 центи (Claude Opus 5.5).

Хостинг (Vercel), база (Supabase) і платежі (Lemon Squeezy) на старті **безкоштовні**. Ви платите
тільки за AI (Anthropic), і лише коли сервісом користуються.

## Запуск: 4 сервіси, ~1 година, один раз

Код уже готовий. Потрібно лише зареєструватися й вставити ключі. Усі ключі вставляються у Vercel
(крок 4), а не в код.

### Крок 1. Anthropic: AI, що пише тексти

1. Зареєструйтесь на [console.anthropic.com](https://console.anthropic.com).
2. **Billing**: додайте картку й поповніть баланс ($5–10 для старту).
3. **Limits**: поставте місячний ліміт витрат (наприклад, $20), щоб не було сюрпризів.
4. **API Keys → Create Key**. Збережіть ключ як `ANTHROPIC_API_KEY`.

### Крок 2. Supabase: акаунти користувачів і база

1. Зареєструйтесь на [supabase.com](https://supabase.com) → **New project** (регіон: Frankfurt).
2. **SQL Editor → New query**: вставте весь вміст файлу `supabase/schema.sql` → **Run**.
3. **Project Settings → API**: скопіюйте
   - `Project URL` → `SUPABASE_URL`
   - `anon public` → `SUPABASE_ANON_KEY`
   - `service_role` → `SUPABASE_SERVICE_ROLE_KEY` (секретний, нікому не показуйте!)
4. **Authentication → URL Configuration**: у `Site URL` вставте адресу сайту з Vercel (з'явиться в кроці 4),
   а в `Redirect URLs` додайте `https://<ваш-сайт>/app.html`.
5. (Необов'язково) **Authentication → Providers → Google**: щоб працювала кнопка «Continue with Google».

### Крок 3. Lemon Squeezy: приймання оплати

1. Зареєструйтесь на [lemonsqueezy.com](https://www.lemonsqueezy.com) і створіть магазин.
   **Перевірте, що для вашої країни доступні виплати** (Settings → Payouts). Якщо ні,
   альтернатива — [Paddle](https://www.paddle.com); тоді доведеться переписати `api/webhook.js` (я допоможу).
2. Пройдіть активацію магазину (перевірка особи). Без неї приймаються лише тестові платежі.
3. **Products → New product** «Muse», тип **Subscription**, два варіанти:
   - Creator — $19 / місяць
   - Pro — $49 / місяць
4. Для кожного варіанта:
   - **ID варіанта** → `LEMONSQUEEZY_VARIANT_CREATOR` і `LEMONSQUEEZY_VARIANT_PRO`
   - **Share → Checkout link** → `LEMONSQUEEZY_CHECKOUT_CREATOR` і `LEMONSQUEEZY_CHECKOUT_PRO`
5. У налаштуваннях продукту → **Confirmation modal / Redirect URL**: `https://<ваш-сайт>/app.html?paid=1`.
6. **Settings → Webhooks → +**:
   - URL: `https://<ваш-сайт>/api/webhook`
   - Signing secret: придумайте довгий випадковий рядок → `LEMONSQUEEZY_WEBHOOK_SECRET`
   - Події: `subscription_created`, `subscription_updated`, `subscription_cancelled`,
     `subscription_resumed`, `subscription_expired`, `subscription_payment_success`

### Крок 4. Vercel: сайт в інтернеті

1. Зареєструйтесь на [vercel.com](https://vercel.com) через GitHub.
2. **Add New → Project** → оберіть репозиторій `hozvoc-svg/-` → **Deploy**.
3. **Settings → Environment Variables**: додайте всі 9 змінних:

   | Назва | Звідки |
   |---|---|
   | `ANTHROPIC_API_KEY` | крок 1 |
   | `SUPABASE_URL` | крок 2 |
   | `SUPABASE_ANON_KEY` | крок 2 |
   | `SUPABASE_SERVICE_ROLE_KEY` | крок 2 |
   | `LEMONSQUEEZY_VARIANT_CREATOR` | крок 3 |
   | `LEMONSQUEEZY_VARIANT_PRO` | крок 3 |
   | `LEMONSQUEEZY_CHECKOUT_CREATOR` | крок 3 |
   | `LEMONSQUEEZY_CHECKOUT_PRO` | крок 3 |
   | `LEMONSQUEEZY_WEBHOOK_SECRET` | крок 3 |

4. **Deployments → Redeploy**. Адреса сайту буде на кшталт `https://muse-xxx.vercel.app`.
   Поверніться в кроки 2.4, 3.5 і 3.6 та вставте цю адресу.

### Крок 5. Перевірка

1. Зареєструйтесь на своєму сайті й згенеруйте текст: кредити мають зменшитись з 10 до 9.
2. У Lemon Squeezy увімкніть **Test mode**, купіть Creator тестовою карткою `4242 4242 4242 4242`.
   У кабінеті має з'явитися тариф Creator і 300 кредитів.
3. Замініть `support@example.com` на свою пошту в `about.html`, `privacy.html` і `terms.html`.

## Де шукати перших клієнтів

Сайт сам клієнтів не приведе. Перші 10 платних користувачів потрібно знайти вручну:

1. **Власники малого бізнесу в Instagram і Facebook** (кав'ярні, салони, магазини одягу).
   Напишіть 3–5 постів для них безкоштовно в Muse й надішліть із посиланням на сервіс.
2. **Групи й спільноти** для SMM-ників, фрилансерів і власників Etsy/Shopify-магазинів.
3. **Product Hunt, Reddit (r/SideProject, r/Entrepreneur), Indie Hackers**: розкажіть, що ви зробили.
4. **Короткі відео (TikTok, Reels, Shorts)**: «написав рекламу за 10 секунд» добре заходить.
5. **Блог** (`blog.html`): статті на кшталт «50 ідей для постів кав'ярні» з часом приводять трафік із Google.

Реалістично: перші продажі — за кілька тижнів активного просування. 50 платних користувачів
приносять приблизно $600–1 000 на місяць.

## Технічні деталі

```
index.html, about.html, blog*.html,   — публічні сторінки
privacy.html, terms.html, 404.html
login.html, app.html                  — вхід і кабінет
css/style.css                         — стилі (кольори в :root на початку)
js/main.js                            — анімації, демо, форма входу
js/auth.js                            — акаунти (Supabase) та посилання на оплату
js/app.js                             — логіка кабінету
api/generate.js                       — генерація через Claude, списання кредитів
api/webhook.js                        — оплати Lemon Squeezy → тарифи й кредити
api/config.js                         — публічні налаштування для браузера
api/_lib.js                           — тарифи, шаблони, спільний код
supabase/schema.sql                   — таблиці, захист даних, функції кредитів
```

- **AI**: Claude Opus 5.5 (`claude-opus-5-5`), `effort: low`. Увімкнено автоматичний резервний режим
  (`fallbacks: "default"`): якщо модель відхилить запит, API повторить його на іншій моделі.
  Щоб зменшити витрати приблизно в 40 разів, у `api/generate.js` можна поставити модель `claude-haiku-5-5`
  (тексти будуть трохи простіші).
- **Безпека**: секретні ключі лише на сервері; користувачі бачать тільки свої дані (Row Level Security);
  кредити списуються атомарно на сервері; невдала генерація повертає кредит; підпис вебхука перевіряється.
- **Ліміт демо** (3 запити на годину з IP) зберігається в пам'яті сервера, тож це захист «найкращий можливий».
- **Тарифи** задано у двох місцях: `PLANS` в `api/_lib.js` і `plan_credits()` у `supabase/schema.sql`.
- **GitHub Pages** (`https://hozvoc-svg.github.io/-/`) показує лише статичну версію: без входу й генерації.
  Після запуску на Vercel використовуйте адресу Vercel.
- Юридичні сторінки — базовий шаблон. Перед активним продажем бажано показати їх юристу.
