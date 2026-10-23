"""Builds the localized landing pages (index.html, uk.html, es.html, ...) from one template.

Edit the copy in LANG below, then run:  python3 tools/build_landing.py
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://hozvoc-svg.github.io/-/"  # public URL used for og:image and hreflang links

# Language list: code, file, native name, short label, extra Google font
LANGS = [
    ("en", "index.html", "English", "EN", None),
    ("zh", "zh.html", "中文", "中文", "Noto+Sans+SC:wght@400;500;700;900"),
    ("hi", "hi.html", "हिन्दी", "हिं", "Noto+Sans+Devanagari:wght@400;500;600;700;800"),
    ("es", "es.html", "Español", "ES", None),
    ("fr", "fr.html", "Français", "FR", None),
    ("ar", "ar.html", "العربية", "ع", "IBM+Plex+Sans+Arabic:wght@400;500;600;700"),
    ("uk", "uk.html", "Українська", "UA", None),
]

LANG = {}

LANG["en"] = dict(
    title="Muse — AI Copywriter for Ads, Posts &amp; Emails",
    desc="Muse writes ads, social posts, product descriptions and emails in your tone, in 11 languages, in seconds. Start free.",
    og_title="Muse — AI Copywriter", og_desc="Ads, social posts, product descriptions and emails in seconds. Start free.", og_locale="en_US",
    skip="Skip to content", home="Muse home", menu="Primary", n_features="Features", n_try="Try it", n_pricing="Pricing", n_faq="FAQ", n_blog="Blog", blog_href="blog.html",
    login="Log in", theme="Toggle color theme", open_menu="Open menu", lang_label="Language", cta_nav="Start free",
    pill_tag="Free", pill="10 generations every month", h1a="Marketing copy in seconds.", h1b="Just describe it.",
    sub="Muse writes ads, social posts, product descriptions and emails in the tone you choose — in 11 languages, ready to copy and publish.",
    cta1="Start writing free", cta2="Try it now", note="No credit card required · Cancel anytime",
    go="Generate", chips=["📣 Ad", "💬 Social post", "✉️ Email", "Tone: playful", "English"],
    channels_title="Write for every channel", channels=["Instagram", "LinkedIn", "Facebook Ads", "X / Twitter", "Shopify", "Etsy", "Email", "Blog"],
    f_eyebrow="Features", f_h2="Your always-on copywriter", f_p="Stop staring at a blank page. Describe what you need and get publish-ready copy in seconds.",
    f=[("✍️", "9 ready-made formats", "Ads, social posts, product descriptions, emails, blog outlines, slogans, video scripts, review replies and marketplace listings — each tuned with copywriting best practices."),
       ("🎚️", "Any tone", "Friendly, professional, playful, bold, luxury or minimal."),
       ("🌍", "11 languages", "English, Chinese, Hindi, Spanish, French, Arabic, Portuguese, German, Italian, Polish and Ukrainian."),
       ("🗂️", "Saved history", "Every result is saved to your account, so you can reuse it anytime."),
       ("💼", "Commercial use", "Use everything you write in ads, stores and client work."),
       ("🧠", "Powered by Claude", "Muse runs on Claude by Anthropic, one of the world's most capable AI models for writing — so your copy reads naturally, not like a robot wrote it.")],
    d_eyebrow="Try it", d_h2="See Muse in action", d_p="Browse examples, or write your own prompt — 3 free tries, no sign-up.",
    tabs=["📣 Instagram ad", "🛍️ Product description", "✉️ Cold email", "✦ Your prompt"], tabs_label="Demo prompts",
    d_input="Describe what you want Muse to write", d_ph="e.g. A LinkedIn post announcing our new eco-friendly sneaker line", d_go="Generate",
    d_prompt="Prompt", d_status="writing…",
    h_eyebrow="How it works", h_h2="From idea to published in a minute",
    steps=[("Pick a format", "Ad, social post, product description, email, video script, review reply and more."),
           ("Describe it", "A sentence or two about your product, audience and offer is enough."),
           ("Copy &amp; publish", "Get the result in seconds, tweak if you like, and post it.")],
    metrics=[("9", "Content formats"), ("11", "Languages"), ("6", "Tones of voice"), ("10", "Free generations / month")],
    p_eyebrow="Pricing", p_h2="Start free. Upgrade when you need more.", p_p="1 generation = 1 credit. Credits refill every month.", mo="/mo",
    free_desc="Try Muse at no cost.", free_btn="Start free", free_list=["10 generations / month", "All 9 formats", "All tones &amp; languages", "Saved history"],
    popular="Most popular", creator_desc="For creators, freelancers and small shops.", creator_btn="Get Creator",
    creator_list=["300 generations / month", "Everything in Free", "Commercial use", "Email support"],
    pro_desc="For agencies and busy marketing teams.", pro_btn="Get Pro", pro_list=["1,000 generations / month", "Everything in Creator", "Priority support"],
    q_eyebrow="FAQ", q_h2="Frequently asked questions",
    faq=[("Can I use the content commercially?", "Yes. You can use everything you generate in ads, online stores, social media and client work."),
         ("What is a credit?", "One generation uses one credit. Free accounts get 10 credits every month; paid plans refill on each billing date. If a generation fails, the credit is returned automatically."),
         ("Is my content private?", "Your prompts and results are visible only to you. Muse uses Anthropic's Claude API, and your content is not used to train AI models."),
         ("Can I cancel anytime?", "Yes. There are no contracts — cancel from “Manage billing” in your account and keep access until the end of the paid period."),
         ("Does Muse create images or videos?", "Not yet. Muse focuses on writing great text — including scripts for your videos and listings for your online store.")],
    c_h2="Your next post is one sentence away.", c_p="Create a free account and get 10 generations every month.", c_btn="Start writing free",
    ft_tag="Marketing copy in seconds.", ft_product="Product", ft_company="Company", ft_legal="Legal",
    ft_about="About", ft_blog="Blog", ft_contact="Contact", ft_privacy="Privacy", ft_terms="Terms", rights="All rights reserved.",
)

LANG["uk"] = dict(
    title="Muse — AI-копірайтер для реклами, постів і розсилок",
    desc="Muse пише рекламу, пости, описи товарів і email-листи українською та ще 10 мовами за секунди. 10 генерацій щомісяця безкоштовно.",
    og_title="Muse — AI-копірайтер українською", og_desc="Реклама, пости, описи товарів і листи за секунди. Почніть безкоштовно.", og_locale="uk_UA",
    skip="Перейти до змісту", home="Muse — головна", menu="Головне меню", n_features="Можливості", n_try="Спробувати", n_pricing="Ціни", n_faq="Питання", n_blog="Блог", blog_href="yak-napysaty-post-instagram.html",
    login="Увійти", theme="Змінити тему", open_menu="Відкрити меню", lang_label="Мова", cta_nav="Почати",
    pill_tag="Безкоштовно", pill="10 генерацій щомісяця", h1a="Тексти для бізнесу за секунди.", h1b="Просто опишіть.",
    sub="Muse пише рекламу, пости, описи товарів і email-листи потрібним тоном — українською та ще 10 мовами. Скопіювали й опублікували.",
    cta1="Почати безкоштовно", cta2="Спробувати зараз", note="Без банківської картки · Скасування будь-коли",
    go="Створити", chips=["📣 Реклама", "💬 Пост", "✉️ Лист", "Тон: грайливий", "Українська"],
    channels_title="Тексти для будь-якого каналу", channels=["Instagram", "Facebook", "TikTok", "Telegram", "Prom.ua", "Rozetka", "Email", "Блог"],
    f_eyebrow="Можливості", f_h2="Ваш копірайтер, що працює 24/7", f_p="Більше жодного «не знаю, що написати». Опишіть, що потрібно, — і отримайте готовий текст за секунди.",
    f=[("✍️", "9 готових форматів", "Реклама, пости, описи товарів, листи, плани статей, слогани, сценарії відео, відповіді на відгуки й картки для маркетплейсів — кожен налаштований за правилами копірайтингу."),
       ("🎚️", "Будь-який тон", "Дружній, діловий, грайливий, сміливий, преміальний або лаконічний."),
       ("🌍", "11 мов", "Українська, англійська, китайська, гінді, іспанська, французька, арабська, португальська, німецька, італійська й польська."),
       ("🗂️", "Історія", "Усі тексти зберігаються у вашому акаунті — повертайтеся до них будь-коли."),
       ("💼", "Для комерції", "Використовуйте тексти в рекламі, магазинах і роботі з клієнтами."),
       ("🧠", "Працює на Claude", "Muse використовує Claude від Anthropic — одну з найсильніших AI-моделей для текстів. Тому написане звучить природно, а не як від робота.")],
    d_eyebrow="Спробувати", d_h2="Подивіться, як це працює", d_p="Перегляньте приклади або напишіть власний запит — 3 спроби без реєстрації.",
    tabs=["📣 Реклама в Instagram", "🛍️ Опис товару", "✉️ Діловий лист", "✦ Ваш запит"], tabs_label="Приклади запитів",
    d_input="Опишіть, що має написати Muse", d_ph="Напр.: пост про відкриття нашої кав’ярні на Подолі, знижка −20% у перший тиждень", d_go="Створити",
    d_prompt="Запит", d_status="пишу…",
    h_eyebrow="Як це працює", h_h2="Від ідеї до публікації за хвилину",
    steps=[("Оберіть формат", "Реклама, пост, опис товару, лист, сценарій відео, відповідь на відгук та інші."),
           ("Опишіть", "Одного-двох речень про товар, аудиторію й пропозицію достатньо."),
           ("Скопіюйте й опублікуйте", "Отримайте текст за секунди, за бажанням підправте — і публікуйте.")],
    metrics=[("9", "Форматів"), ("11", "Мов"), ("6", "Тонів"), ("10", "Безкоштовно щомісяця")],
    p_eyebrow="Ціни", p_h2="Почніть безкоштовно. Розширюйтеся, коли знадобиться.", p_p="1 генерація = 1 кредит. Кредити поновлюються щомісяця. Оплата карткою в доларах.", mo="/міс",
    free_desc="Спробуйте без оплати.", free_btn="Почати", free_list=["10 генерацій на місяць", "Усі 9 форматів", "Усі тони й мови", "Історія текстів"],
    popular="Найпопулярніший", creator_desc="Для блогерів, фрилансерів і малих магазинів.", creator_btn="Обрати Creator",
    creator_list=["300 генерацій на місяць", "Усе з Free", "Комерційне використання", "Підтримка email"],
    pro_desc="Для агенцій і маркетингових команд.", pro_btn="Обрати Pro", pro_list=["1000 генерацій на місяць", "Усе з Creator", "Пріоритетна підтримка"],
    q_eyebrow="Питання", q_h2="Часті запитання",
    faq=[("Чи можна використовувати тексти в бізнесі?", "Так. Усе, що ви створюєте, можна використовувати в рекламі, інтернет-магазинах, соцмережах і роботі з клієнтами."),
         ("Що таке кредит?", "Одна генерація — один кредит. Безкоштовний акаунт отримує 10 кредитів щомісяця, платні тарифи — з кожною оплатою. Якщо генерація не вдалася, кредит повертається автоматично."),
         ("Чи бачить хтось мої тексти?", "Ваші запити й результати бачите лише ви. Muse працює через Claude API від Anthropic, і ваші тексти не використовуються для навчання AI."),
         ("Чи можна скасувати підписку?", "Так, будь-коли: «Manage billing» в акаунті. Доступ залишається до кінця оплаченого періоду."),
         ("Кабінет є українською?", "Так. Кабінет, вхід і всі повідомлення доступні 7 мовами, а самі тексти Muse пише 11 мовами — мову можна змінити будь-коли.")],
    c_h2="Ваш наступний пост — за одне речення.", c_p="Створіть безкоштовний акаунт і отримуйте 10 генерацій щомісяця.", c_btn="Почати безкоштовно",
    ft_tag="Тексти для бізнесу за секунди.", ft_product="Продукт", ft_company="Компанія", ft_legal="Документи",
    ft_about="Про нас", ft_blog="Блог", ft_contact="Контакти", ft_privacy="Конфіденційність", ft_terms="Умови", rights="Усі права захищено.",
)

LANG["es"] = dict(
    title="Muse — Redactor con IA para anuncios, posts y emails",
    desc="Muse escribe anuncios, posts, descripciones de productos y emails en tu tono y en 11 idiomas, en segundos. Empieza gratis.",
    og_title="Muse — Redactor publicitario con IA", og_desc="Anuncios, posts, descripciones y emails en segundos. Empieza gratis.", og_locale="es_ES",
    skip="Saltar al contenido", home="Inicio de Muse", menu="Menú principal", n_features="Funciones", n_try="Pruébalo", n_pricing="Precios", n_faq="Preguntas", n_blog="Blog", blog_href="blog.html",
    login="Iniciar sesión", theme="Cambiar tema", open_menu="Abrir menú", lang_label="Idioma", cta_nav="Empezar gratis",
    pill_tag="Gratis", pill="10 textos cada mes", h1a="Textos de marketing en segundos.", h1b="Solo descríbelo.",
    sub="Muse escribe anuncios, posts, descripciones de productos y emails con el tono que elijas, en 11 idiomas, listos para copiar y publicar.",
    cta1="Empieza gratis", cta2="Pruébalo ahora", note="Sin tarjeta de crédito · Cancela cuando quieras",
    go="Generar", chips=["📣 Anuncio", "💬 Post", "✉️ Email", "Tono: divertido", "Español"],
    channels_title="Escribe para cada canal", channels=["Instagram", "TikTok", "Facebook", "WhatsApp", "Shopify", "Mercado Libre", "Email", "Blog"],
    f_eyebrow="Funciones", f_h2="Tu redactor, siempre disponible", f_p="Olvídate de la página en blanco. Describe lo que necesitas y obtén textos listos para publicar en segundos.",
    f=[("✍️", "9 formatos listos", "Anuncios, posts, descripciones de productos, emails, esquemas de blog, eslóganes, guiones de vídeo, respuestas a reseñas y fichas de marketplace, cada uno con las mejores prácticas de copywriting."),
       ("🎚️", "Cualquier tono", "Cercano, profesional, divertido, atrevido, de lujo o minimalista."),
       ("🌍", "11 idiomas", "Español, inglés, chino, hindi, francés, árabe, portugués, alemán, italiano, polaco y ucraniano."),
       ("🗂️", "Historial guardado", "Todos tus textos se guardan en tu cuenta para reutilizarlos cuando quieras."),
       ("💼", "Uso comercial", "Usa todo lo que escribas en anuncios, tiendas y trabajos para clientes."),
       ("🧠", "Con la tecnología de Claude", "Muse funciona con Claude de Anthropic, uno de los modelos de IA más capaces para escribir, así que tus textos suenan naturales, no robóticos.")],
    d_eyebrow="Pruébalo", d_h2="Mira Muse en acción", d_p="Explora ejemplos o escribe tu propia petición: 3 intentos gratis, sin registro.",
    tabs=["📣 Anuncio de Instagram", "🛍️ Descripción de producto", "✉️ Email comercial", "✦ Tu petición"], tabs_label="Ejemplos",
    d_input="Describe lo que quieres que escriba Muse", d_ph="Ej.: un post de LinkedIn para anunciar nuestra nueva línea de zapatillas ecológicas", d_go="Generar",
    d_prompt="Petición", d_status="escribiendo…",
    h_eyebrow="Cómo funciona", h_h2="De la idea a la publicación en un minuto",
    steps=[("Elige un formato", "Anuncio, post, descripción de producto, email, guion de vídeo, respuesta a reseña y más."),
           ("Descríbelo", "Basta con una o dos frases sobre tu producto, tu público y tu oferta."),
           ("Copia y publica", "Obtén el resultado en segundos, ajústalo si quieres y publícalo.")],
    metrics=[("9", "Formatos"), ("11", "Idiomas"), ("6", "Tonos"), ("10", "Textos gratis al mes")],
    p_eyebrow="Precios", p_h2="Empieza gratis. Amplía cuando lo necesites.", p_p="1 texto = 1 crédito. Los créditos se renuevan cada mes.", mo="/mes",
    free_desc="Prueba Muse sin coste.", free_btn="Empezar gratis", free_list=["10 textos al mes", "Los 9 formatos", "Todos los tonos e idiomas", "Historial guardado"],
    popular="El más popular", creator_desc="Para creadores, freelancers y pequeñas tiendas.", creator_btn="Elegir Creator",
    creator_list=["300 textos al mes", "Todo lo de Free", "Uso comercial", "Soporte por email"],
    pro_desc="Para agencias y equipos de marketing.", pro_btn="Elegir Pro", pro_list=["1.000 textos al mes", "Todo lo de Creator", "Soporte prioritario"],
    q_eyebrow="Preguntas", q_h2="Preguntas frecuentes",
    faq=[("¿Puedo usar los textos con fines comerciales?", "Sí. Puedes usar todo lo que generes en anuncios, tiendas online, redes sociales y trabajos para clientes."),
         ("¿Qué es un crédito?", "Cada texto usa un crédito. Las cuentas gratuitas reciben 10 créditos al mes; los planes de pago se recargan en cada fecha de cobro. Si una generación falla, el crédito se devuelve automáticamente."),
         ("¿Mis textos son privados?", "Solo tú ves tus peticiones y resultados. Muse usa la API de Claude de Anthropic y tu contenido no se utiliza para entrenar modelos de IA."),
         ("¿Puedo cancelar cuando quiera?", "Sí, sin permanencia: cancela desde «Manage billing» en tu cuenta y mantén el acceso hasta el final del periodo pagado."),
         ("¿El panel está en español?", "Sí. El panel, el acceso y todos los mensajes están disponibles en 7 idiomas, y Muse escribe textos en 11 idiomas. Puedes cambiar el idioma cuando quieras.")],
    c_h2="Tu próximo post está a una frase de distancia.", c_p="Crea una cuenta gratis y obtén 10 textos cada mes.", c_btn="Empieza gratis",
    ft_tag="Textos de marketing en segundos.", ft_product="Producto", ft_company="Empresa", ft_legal="Legal",
    ft_about="Sobre nosotros", ft_blog="Blog", ft_contact="Contacto", ft_privacy="Privacidad", ft_terms="Términos", rights="Todos los derechos reservados.",
)

LANG["fr"] = dict(
    title="Muse — Rédacteur IA pour pubs, posts et emails",
    desc="Muse rédige vos pubs, posts, fiches produits et emails dans votre ton et en 11 langues, en quelques secondes. Commencez gratuitement.",
    og_title="Muse — Rédacteur publicitaire IA", og_desc="Pubs, posts, fiches produits et emails en quelques secondes. Commencez gratuitement.", og_locale="fr_FR",
    skip="Aller au contenu", home="Accueil Muse", menu="Menu principal", n_features="Fonctionnalités", n_try="Essayer", n_pricing="Tarifs", n_faq="FAQ", n_blog="Blog", blog_href="blog.html",
    login="Connexion", theme="Changer de thème", open_menu="Ouvrir le menu", lang_label="Langue", cta_nav="Commencer",
    pill_tag="Gratuit", pill="10 textes chaque mois", h1a="Vos textes marketing en quelques secondes.", h1b="Décrivez, c’est tout.",
    sub="Muse rédige pubs, posts, fiches produits et emails dans le ton de votre choix, en 11 langues, prêts à copier et publier.",
    cta1="Commencer gratuitement", cta2="Essayer maintenant", note="Sans carte bancaire · Résiliable à tout moment",
    go="Générer", chips=["📣 Pub", "💬 Post", "✉️ Email", "Ton : ludique", "Français"],
    channels_title="Des textes pour chaque canal", channels=["Instagram", "LinkedIn", "Facebook", "TikTok", "Shopify", "Etsy", "Email", "Blog"],
    f_eyebrow="Fonctionnalités", f_h2="Votre rédacteur, disponible 24 h/24", f_p="Fini la page blanche. Décrivez votre besoin et obtenez un texte prêt à publier en quelques secondes.",
    f=[("✍️", "9 formats prêts à l’emploi", "Pubs, posts, fiches produits, emails, plans d’articles, slogans, scripts vidéo, réponses aux avis et annonces marketplace, chacun optimisé selon les bonnes pratiques du copywriting."),
       ("🎚️", "Tous les tons", "Chaleureux, professionnel, ludique, audacieux, luxe ou minimaliste."),
       ("🌍", "11 langues", "Français, anglais, chinois, hindi, espagnol, arabe, portugais, allemand, italien, polonais et ukrainien."),
       ("🗂️", "Historique sauvegardé", "Tous vos textes sont enregistrés dans votre compte pour les réutiliser à tout moment."),
       ("💼", "Usage commercial", "Utilisez vos textes dans vos pubs, boutiques et missions clients."),
       ("🧠", "Propulsé par Claude", "Muse fonctionne avec Claude d’Anthropic, l’un des modèles d’IA les plus performants pour l’écriture : vos textes sonnent naturels, pas robotiques.")],
    d_eyebrow="Essayer", d_h2="Muse en action", d_p="Parcourez les exemples ou écrivez votre propre demande : 3 essais gratuits, sans inscription.",
    tabs=["📣 Pub Instagram", "🛍️ Fiche produit", "✉️ Email de prospection", "✦ Votre demande"], tabs_label="Exemples",
    d_input="Décrivez ce que Muse doit écrire", d_ph="Ex. : un post LinkedIn pour annoncer notre nouvelle gamme de baskets éco-responsables", d_go="Générer",
    d_prompt="Demande", d_status="rédaction…",
    h_eyebrow="Comment ça marche", h_h2="De l’idée à la publication en une minute",
    steps=[("Choisissez un format", "Pub, post, fiche produit, email, script vidéo, réponse à un avis et plus."),
           ("Décrivez", "Une ou deux phrases sur votre produit, votre cible et votre offre suffisent."),
           ("Copiez et publiez", "Obtenez le résultat en quelques secondes, ajustez si besoin et publiez.")],
    metrics=[("9", "Formats"), ("11", "Langues"), ("6", "Tons"), ("10", "Textes gratuits / mois")],
    p_eyebrow="Tarifs", p_h2="Commencez gratuitement. Passez à la vitesse supérieure quand vous voulez.", p_p="1 texte = 1 crédit. Les crédits se renouvellent chaque mois.", mo="/mois",
    free_desc="Essayez Muse sans frais.", free_btn="Commencer", free_list=["10 textes par mois", "Les 9 formats", "Tous les tons et langues", "Historique sauvegardé"],
    popular="Le plus populaire", creator_desc="Pour créateurs, freelances et petites boutiques.", creator_btn="Choisir Creator",
    creator_list=["300 textes par mois", "Tout le plan Free", "Usage commercial", "Support par email"],
    pro_desc="Pour agences et équipes marketing.", pro_btn="Choisir Pro", pro_list=["1 000 textes par mois", "Tout le plan Creator", "Support prioritaire"],
    q_eyebrow="FAQ", q_h2="Questions fréquentes",
    faq=[("Puis-je utiliser les textes à des fins commerciales ?", "Oui. Vous pouvez utiliser tout ce que vous générez dans vos pubs, boutiques en ligne, réseaux sociaux et missions clients."),
         ("Qu’est-ce qu’un crédit ?", "Chaque texte utilise un crédit. Les comptes gratuits reçoivent 10 crédits par mois ; les offres payantes sont rechargées à chaque échéance. Si une génération échoue, le crédit est rendu automatiquement."),
         ("Mes contenus sont-ils privés ?", "Vous seul voyez vos demandes et vos résultats. Muse utilise l’API Claude d’Anthropic, et vos contenus ne servent pas à entraîner des modèles d’IA."),
         ("Puis-je résilier à tout moment ?", "Oui, sans engagement : résiliez depuis « Manage billing » dans votre compte et gardez l’accès jusqu’à la fin de la période payée."),
         ("L’espace client est-il en français ?", "Oui. L’espace client, la connexion et tous les messages sont disponibles en 7 langues, et Muse rédige vos textes en 11 langues. Vous pouvez changer de langue à tout moment.")],
    c_h2="Votre prochain post tient en une phrase.", c_p="Créez un compte gratuit et obtenez 10 textes chaque mois.", c_btn="Commencer gratuitement",
    ft_tag="Vos textes marketing en quelques secondes.", ft_product="Produit", ft_company="Entreprise", ft_legal="Mentions",
    ft_about="À propos", ft_blog="Blog", ft_contact="Contact", ft_privacy="Confidentialité", ft_terms="Conditions", rights="Tous droits réservés.",
)

LANG["zh"] = dict(
    title="Muse — AI 营销文案助手：广告、帖子与邮件",
    desc="Muse 用你想要的语气，以 11 种语言在几秒内写出广告、社交帖子、产品描述和邮件。免费开始。",
    og_title="Muse — AI 文案助手", og_desc="几秒钟写好广告、帖子、产品描述和邮件。免费开始。", og_locale="zh_CN",
    skip="跳到正文", home="Muse 首页", menu="主菜单", n_features="功能", n_try="试用", n_pricing="价格", n_faq="常见问题", n_blog="博客", blog_href="blog.html",
    login="登录", theme="切换主题", open_menu="打开菜单", lang_label="语言", cta_nav="免费开始",
    pill_tag="免费", pill="每月 10 次生成", h1a="营销文案，几秒搞定。", h1b="描述一下就好。",
    sub="Muse 按你选择的语气撰写广告、社交帖子、产品描述和邮件，支持 11 种语言，复制即可发布。",
    cta1="免费开始写作", cta2="立即试用", note="无需信用卡 · 随时取消",
    go="生成", chips=["📣 广告", "💬 帖子", "✉️ 邮件", "语气：俏皮", "中文"],
    channels_title="适用于各种渠道", channels=["微信", "小红书", "抖音", "微博", "淘宝", "京东", "邮件", "博客"],
    f_eyebrow="功能", f_h2="全天候在线的文案助手", f_p="告别对着空白页发呆。描述你的需求，几秒钟就能得到可直接发布的文案。",
    f=[("✍️", "9 种现成格式", "广告、社交帖子、产品描述、邮件、博客大纲、口号、短视频脚本、评价回复和电商商品页，每种都融入了文案写作的最佳实践。"),
       ("🎚️", "任意语气", "亲切、专业、俏皮、大胆、高端或简约。"),
       ("🌍", "11 种语言", "中文、英语、印地语、西班牙语、法语、阿拉伯语、葡萄牙语、德语、意大利语、波兰语和乌克兰语。"),
       ("🗂️", "历史记录", "每条结果都会保存在你的账户中，随时可以再次使用。"),
       ("💼", "可商用", "生成的内容可用于广告、网店和客户项目。"),
       ("🧠", "由 Claude 驱动", "Muse 基于 Anthropic 的 Claude，这是全球最擅长写作的 AI 模型之一，所以文案读起来自然流畅，毫无机器感。")],
    d_eyebrow="试用", d_h2="看看 Muse 的实际效果", d_p="浏览示例，或输入你自己的需求：无需注册，可免费试用 3 次。",
    tabs=["📣 Instagram 广告", "🛍️ 产品描述", "✉️ 开发信", "✦ 你的需求"], tabs_label="示例",
    d_input="描述你希望 Muse 写什么", d_ph="例如：为我们新推出的环保运动鞋系列写一条 LinkedIn 帖子", d_go="生成",
    d_prompt="需求", d_status="写作中…",
    h_eyebrow="使用方法", h_h2="一分钟，从想法到发布",
    steps=[("选择格式", "广告、帖子、产品描述、邮件、短视频脚本、评价回复等。"),
           ("描述需求", "用一两句话介绍你的产品、受众和优惠就够了。"),
           ("复制并发布", "几秒钟得到结果，可按需微调，然后发布。")],
    metrics=[("9", "种格式"), ("11", "种语言"), ("6", "种语气"), ("10", "次免费 / 月")],
    p_eyebrow="价格", p_h2="免费开始，需要时再升级。", p_p="1 次生成 = 1 个积分。积分每月刷新。以美元计价。", mo="/月",
    free_desc="零成本体验 Muse。", free_btn="免费开始", free_list=["每月 10 次生成", "全部 9 种格式", "所有语气和语言", "历史记录"],
    popular="最受欢迎", creator_desc="适合创作者、自由职业者和小店铺。", creator_btn="选择 Creator",
    creator_list=["每月 300 次生成", "包含 Free 全部功能", "可商用", "邮件支持"],
    pro_desc="适合代理公司和营销团队。", pro_btn="选择 Pro", pro_list=["每月 1,000 次生成", "包含 Creator 全部功能", "优先支持"],
    q_eyebrow="常见问题", q_h2="常见问题",
    faq=[("生成的内容可以商用吗？", "可以。你生成的所有内容都可用于广告、网店、社交媒体和客户项目。"),
         ("什么是积分？", "每次生成消耗 1 个积分。免费账户每月获得 10 个积分；付费套餐在每个账单日自动补充。如果生成失败，积分会自动退回。"),
         ("我的内容是私密的吗？", "只有你能看到自己的需求和结果。Muse 使用 Anthropic 的 Claude API，你的内容不会被用于训练 AI 模型。"),
         ("可以随时取消吗？", "可以，没有合约限制：在账户的“Manage billing”中取消，已付费期间结束前仍可继续使用。"),
         ("工作台有中文界面吗？", "有。工作台、登录页和所有提示都支持 7 种界面语言，Muse 可用 11 种语言撰写文案，随时可以切换。")],
    c_h2="下一条爆款帖子，只差一句话。", c_p="创建免费账户，每月获得 10 次生成。", c_btn="免费开始写作",
    ft_tag="营销文案，几秒搞定。", ft_product="产品", ft_company="公司", ft_legal="法律",
    ft_about="关于我们", ft_blog="博客", ft_contact="联系我们", ft_privacy="隐私政策", ft_terms="服务条款", rights="保留所有权利。",
)

LANG["hi"] = dict(
    title="Muse — विज्ञापन, पोस्ट और ईमेल के लिए AI कॉपीराइटर",
    desc="Muse आपके चुने हुए टोन में, 11 भाषाओं में, सेकंडों में विज्ञापन, सोशल पोस्ट, प्रोडक्ट डिस्क्रिप्शन और ईमेल लिखता है। मुफ़्त शुरू करें।",
    og_title="Muse — AI कॉपीराइटर", og_desc="सेकंडों में विज्ञापन, पोस्ट, प्रोडक्ट डिस्क्रिप्शन और ईमेल। मुफ़्त शुरू करें।", og_locale="hi_IN",
    skip="मुख्य सामग्री पर जाएँ", home="Muse होम", menu="मुख्य मेनू", n_features="फ़ीचर", n_try="आज़माएँ", n_pricing="कीमतें", n_faq="सवाल", n_blog="ब्लॉग", blog_href="blog.html",
    login="लॉग इन", theme="थीम बदलें", open_menu="मेनू खोलें", lang_label="भाषा", cta_nav="मुफ़्त शुरू करें",
    pill_tag="मुफ़्त", pill="हर महीने 10 जनरेशन", h1a="मार्केटिंग कॉपी, सेकंडों में।", h1b="बस बताइए।",
    sub="Muse आपके चुने हुए टोन में विज्ञापन, सोशल पोस्ट, प्रोडक्ट डिस्क्रिप्शन और ईमेल लिखता है — 11 भाषाओं में, कॉपी करके तुरंत पब्लिश करने के लिए तैयार।",
    cta1="मुफ़्त में लिखना शुरू करें", cta2="अभी आज़माएँ", note="क्रेडिट कार्ड की ज़रूरत नहीं · कभी भी रद्द करें",
    go="बनाएँ", chips=["📣 विज्ञापन", "💬 पोस्ट", "✉️ ईमेल", "टोन: मज़ेदार", "हिन्दी"],
    channels_title="हर चैनल के लिए लिखें", channels=["Instagram", "YouTube", "WhatsApp", "Facebook", "Flipkart", "Amazon", "ईमेल", "ब्लॉग"],
    f_eyebrow="फ़ीचर", f_h2="आपका हमेशा तैयार कॉपीराइटर", f_p="खाली पन्ने को घूरना बंद करें। बताइए आपको क्या चाहिए और सेकंडों में पब्लिश के लिए तैयार कॉपी पाइए।",
    f=[("✍️", "9 तैयार फ़ॉर्मेट", "विज्ञापन, सोशल पोस्ट, प्रोडक्ट डिस्क्रिप्शन, ईमेल, ब्लॉग आउटलाइन, स्लोगन, वीडियो स्क्रिप्ट, रिव्यू के जवाब और मार्केटप्लेस लिस्टिंग — हर एक कॉपीराइटिंग के बेहतरीन तरीक़ों से तैयार।"),
       ("🎚️", "कोई भी टोन", "दोस्ताना, प्रोफ़ेशनल, मज़ेदार, बोल्ड, लग्ज़री या मिनिमल।"),
       ("🌍", "11 भाषाएँ", "हिन्दी, अंग्रेज़ी, चीनी, स्पैनिश, फ़्रेंच, अरबी, पुर्तगाली, जर्मन, इतालवी, पोलिश और यूक्रेनी।"),
       ("🗂️", "सेव हिस्ट्री", "हर नतीजा आपके अकाउंट में सेव होता है, ताकि आप उसे कभी भी दोबारा इस्तेमाल कर सकें।"),
       ("💼", "कमर्शियल इस्तेमाल", "जो भी लिखें, उसे विज्ञापनों, स्टोर और क्लाइंट के काम में इस्तेमाल करें।"),
       ("🧠", "Claude से संचालित", "Muse, Anthropic के Claude पर चलता है — लिखने के लिए दुनिया के सबसे सक्षम AI मॉडल्स में से एक। इसलिए आपकी कॉपी स्वाभाविक लगती है, रोबोट जैसी नहीं।")],
    d_eyebrow="आज़माएँ", d_h2="Muse को काम करते देखें", d_p="उदाहरण देखें या अपना अनुरोध लिखें — बिना साइन-अप के 3 मुफ़्त प्रयास।",
    tabs=["📣 Instagram विज्ञापन", "🛍️ प्रोडक्ट डिस्क्रिप्शन", "✉️ बिज़नेस ईमेल", "✦ आपका अनुरोध"], tabs_label="उदाहरण",
    d_input="बताइए Muse को क्या लिखना है", d_ph="जैसे: हमारी नई इको-फ़्रेंडली स्नीकर रेंज के लॉन्च पर LinkedIn पोस्ट", d_go="बनाएँ",
    d_prompt="अनुरोध", d_status="लिख रहा है…",
    h_eyebrow="यह कैसे काम करता है", h_h2="आइडिया से पब्लिश तक, एक मिनट में",
    steps=[("फ़ॉर्मेट चुनें", "विज्ञापन, पोस्ट, प्रोडक्ट डिस्क्रिप्शन, ईमेल, वीडियो स्क्रिप्ट, रिव्यू का जवाब और भी बहुत कुछ।"),
           ("बताइए", "अपने प्रोडक्ट, ऑडियंस और ऑफ़र के बारे में एक-दो वाक्य काफ़ी हैं।"),
           ("कॉपी करें और पब्लिश करें", "सेकंडों में नतीजा पाएँ, चाहें तो थोड़ा बदलें और पोस्ट करें।")],
    metrics=[("9", "फ़ॉर्मेट"), ("11", "भाषाएँ"), ("6", "टोन"), ("10", "मुफ़्त जनरेशन / माह")],
    p_eyebrow="कीमतें", p_h2="मुफ़्त शुरू करें। ज़रूरत हो तो अपग्रेड करें।", p_p="1 जनरेशन = 1 क्रेडिट। क्रेडिट हर महीने रिन्यू होते हैं। कीमतें अमेरिकी डॉलर में।", mo="/माह",
    free_desc="बिना किसी ख़र्च के Muse आज़माएँ।", free_btn="मुफ़्त शुरू करें", free_list=["हर महीने 10 जनरेशन", "सभी 9 फ़ॉर्मेट", "सभी टोन और भाषाएँ", "सेव हिस्ट्री"],
    popular="सबसे लोकप्रिय", creator_desc="क्रिएटर्स, फ़्रीलांसर्स और छोटी दुकानों के लिए।", creator_btn="Creator चुनें",
    creator_list=["हर महीने 300 जनरेशन", "Free की सभी सुविधाएँ", "कमर्शियल इस्तेमाल", "ईमेल सपोर्ट"],
    pro_desc="एजेंसियों और मार्केटिंग टीमों के लिए।", pro_btn="Pro चुनें", pro_list=["हर महीने 1,000 जनरेशन", "Creator की सभी सुविधाएँ", "प्राथमिकता सपोर्ट"],
    q_eyebrow="सवाल", q_h2="अक्सर पूछे जाने वाले सवाल",
    faq=[("क्या मैं कंटेंट का कमर्शियल इस्तेमाल कर सकता हूँ?", "हाँ। आप जो भी बनाते हैं, उसे विज्ञापनों, ऑनलाइन स्टोर, सोशल मीडिया और क्लाइंट के काम में इस्तेमाल कर सकते हैं।"),
         ("क्रेडिट क्या है?", "हर जनरेशन में एक क्रेडिट लगता है। मुफ़्त अकाउंट को हर महीने 10 क्रेडिट मिलते हैं; पेड प्लान हर बिलिंग तारीख़ पर रीफ़िल होते हैं। अगर जनरेशन फ़ेल हो जाए, तो क्रेडिट अपने आप वापस मिल जाता है।"),
         ("क्या मेरा कंटेंट प्राइवेट है?", "आपके अनुरोध और नतीजे सिर्फ़ आप देख सकते हैं। Muse, Anthropic के Claude API का इस्तेमाल करता है, और आपका कंटेंट AI मॉडल्स को ट्रेन करने के लिए इस्तेमाल नहीं होता।"),
         ("क्या मैं कभी भी रद्द कर सकता हूँ?", "हाँ, कोई कॉन्ट्रैक्ट नहीं: अपने अकाउंट में “Manage billing” से रद्द करें और भुगतान की गई अवधि के अंत तक एक्सेस बनाए रखें।"),
         ("क्या डैशबोर्ड हिन्दी में है?", "हाँ। डैशबोर्ड, लॉग इन और सभी संदेश 7 भाषाओं में उपलब्ध हैं, और Muse 11 भाषाओं में टेक्स्ट लिखता है। आप कभी भी भाषा बदल सकते हैं।")],
    c_h2="आपकी अगली पोस्ट बस एक वाक्य दूर है।", c_p="मुफ़्त अकाउंट बनाएँ और हर महीने 10 जनरेशन पाएँ।", c_btn="मुफ़्त में लिखना शुरू करें",
    ft_tag="मार्केटिंग कॉपी, सेकंडों में।", ft_product="प्रोडक्ट", ft_company="कंपनी", ft_legal="क़ानूनी",
    ft_about="हमारे बारे में", ft_blog="ब्लॉग", ft_contact="संपर्क", ft_privacy="प्राइवेसी", ft_terms="शर्तें", rights="सर्वाधिकार सुरक्षित।",
)

LANG["ar"] = dict(
    title="Muse — كاتب إعلانات بالذكاء الاصطناعي للإعلانات والمنشورات والبريد",
    desc="يكتب Muse الإعلانات والمنشورات وأوصاف المنتجات ورسائل البريد بالأسلوب الذي تختاره وبـ 11 لغة في ثوانٍ. ابدأ مجانًا.",
    og_title="Muse — كاتب محتوى بالذكاء الاصطناعي", og_desc="إعلانات ومنشورات وأوصاف منتجات ورسائل بريد في ثوانٍ. ابدأ مجانًا.", og_locale="ar_AR",
    skip="انتقل إلى المحتوى", home="الصفحة الرئيسية لـ Muse", menu="القائمة الرئيسية", n_features="المزايا", n_try="جرّبه", n_pricing="الأسعار", n_faq="الأسئلة", n_blog="المدونة", blog_href="blog.html",
    login="تسجيل الدخول", theme="تغيير المظهر", open_menu="فتح القائمة", lang_label="اللغة", cta_nav="ابدأ مجانًا",
    pill_tag="مجانًا", pill="10 نصوص كل شهر", h1a="نصوص تسويقية في ثوانٍ.", h1b="فقط صِف ما تريد.",
    sub="يكتب Muse الإعلانات والمنشورات وأوصاف المنتجات ورسائل البريد بالأسلوب الذي تختاره، بـ 11 لغة، جاهزة للنسخ والنشر.",
    cta1="ابدأ الكتابة مجانًا", cta2="جرّبه الآن", note="لا حاجة لبطاقة ائتمان · ألغِ في أي وقت",
    go="إنشاء", chips=["📣 إعلان", "💬 منشور", "✉️ بريد", "الأسلوب: مرح", "العربية"],
    channels_title="اكتب لكل قناة", channels=["Instagram", "TikTok", "Snapchat", "X", "Facebook", "Noon", "Email", "Blog"],
    f_eyebrow="المزايا", f_h2="كاتبك المتاح دائمًا", f_p="لا مزيد من الحيرة أمام الصفحة البيضاء. صِف ما تحتاجه واحصل على نص جاهز للنشر في ثوانٍ.",
    f=[("✍️", "9 قوالب جاهزة", "إعلانات ومنشورات وأوصاف منتجات ورسائل بريد ومخططات مقالات وشعارات وسيناريوهات فيديو وردود على التقييمات وصفحات منتجات للمتاجر، وكلها مبنية على أفضل ممارسات كتابة الإعلانات."),
       ("🎚️", "أي أسلوب", "ودود، احترافي، مرح، جريء، فاخر أو بسيط."),
       ("🌍", "11 لغة", "العربية والإنجليزية والصينية والهندية والإسبانية والفرنسية والبرتغالية والألمانية والإيطالية والبولندية والأوكرانية."),
       ("🗂️", "سجل محفوظ", "تُحفظ كل النتائج في حسابك لتعيد استخدامها في أي وقت."),
       ("💼", "استخدام تجاري", "استخدم كل ما تكتبه في الإعلانات والمتاجر وأعمال العملاء."),
       ("🧠", "مدعوم بـ Claude", "يعمل Muse بنموذج Claude من Anthropic، أحد أقوى نماذج الذكاء الاصطناعي في الكتابة، لذلك تبدو نصوصك طبيعية وليست آلية.")],
    d_eyebrow="جرّبه", d_h2="شاهد Muse أثناء العمل", d_p="تصفّح الأمثلة أو اكتب طلبك الخاص: 3 محاولات مجانية دون تسجيل.",
    tabs=["📣 إعلان إنستغرام", "🛍️ وصف منتج", "✉️ بريد تسويقي", "✦ طلبك"], tabs_label="أمثلة",
    d_input="صِف ما تريد أن يكتبه Muse", d_ph="مثال: منشور على LinkedIn للإعلان عن تشكيلتنا الجديدة من الأحذية الصديقة للبيئة", d_go="إنشاء",
    d_prompt="الطلب", d_status="جارٍ الكتابة…",
    h_eyebrow="كيف يعمل", h_h2="من الفكرة إلى النشر في دقيقة",
    steps=[("اختر القالب", "إعلان أو منشور أو وصف منتج أو بريد أو سيناريو فيديو أو رد على تقييم وغيرها."),
           ("صِف ما تريد", "تكفي جملة أو جملتان عن منتجك وجمهورك وعرضك."),
           ("انسخ وانشر", "احصل على النتيجة في ثوانٍ، وعدّلها إن شئت، ثم انشرها.")],
    metrics=[("9", "قوالب"), ("11", "لغة"), ("6", "أساليب"), ("10", "نصوص مجانية شهريًا")],
    p_eyebrow="الأسعار", p_h2="ابدأ مجانًا، وطوّر خطتك عند الحاجة.", p_p="نص واحد = رصيد واحد. يتجدد الرصيد كل شهر. الأسعار بالدولار الأمريكي.", mo="/شهر",
    free_desc="جرّب Muse دون أي تكلفة.", free_btn="ابدأ مجانًا", free_list=["10 نصوص شهريًا", "جميع القوالب التسعة", "كل الأساليب واللغات", "سجل محفوظ"],
    popular="الأكثر شيوعًا", creator_desc="لصنّاع المحتوى والمستقلين والمتاجر الصغيرة.", creator_btn="اختر Creator",
    creator_list=["300 نص شهريًا", "كل مزايا Free", "استخدام تجاري", "دعم عبر البريد"],
    pro_desc="للوكالات وفرق التسويق.", pro_btn="اختر Pro", pro_list=["1000 نص شهريًا", "كل مزايا Creator", "دعم ذو أولوية"],
    q_eyebrow="الأسئلة", q_h2="الأسئلة الشائعة",
    faq=[("هل يمكنني استخدام النصوص تجاريًا؟", "نعم. يمكنك استخدام كل ما تنشئه في الإعلانات والمتاجر الإلكترونية ووسائل التواصل وأعمال العملاء."),
         ("ما هو الرصيد؟", "كل نص يستهلك رصيدًا واحدًا. تحصل الحسابات المجانية على 10 أرصدة شهريًا، وتتجدد الخطط المدفوعة في كل موعد فوترة. إذا فشل الإنشاء، يُعاد الرصيد تلقائيًا."),
         ("هل محتواي خاص؟", "أنت وحدك ترى طلباتك ونتائجك. يستخدم Muse واجهة Claude البرمجية من Anthropic، ولا يُستخدم محتواك لتدريب نماذج الذكاء الاصطناعي."),
         ("هل يمكنني الإلغاء في أي وقت؟", "نعم، دون أي التزام: ألغِ من «Manage billing» في حسابك واحتفظ بالوصول حتى نهاية الفترة المدفوعة."),
         ("هل لوحة التحكم بالعربية؟", "نعم. لوحة التحكم وتسجيل الدخول وكل الرسائل متاحة بـ 7 لغات، ويكتب Muse النصوص بـ 11 لغة، ويمكنك تغيير اللغة في أي وقت.")],
    c_h2="منشورك القادم على بُعد جملة واحدة.", c_p="أنشئ حسابًا مجانيًا واحصل على 10 نصوص كل شهر.", c_btn="ابدأ الكتابة مجانًا",
    ft_tag="نصوص تسويقية في ثوانٍ.", ft_product="المنتج", ft_company="الشركة", ft_legal="قانوني",
    ft_about="من نحن", ft_blog="المدونة", ft_contact="اتصل بنا", ft_privacy="الخصوصية", ft_terms="الشروط", rights="جميع الحقوق محفوظة.",
)

SUN = '<svg class="i-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
MOON = '<svg class="i-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'


def build(code, fname, native, short, font):
    t = LANG[code]
    rtl = code == "ar"
    li = lambda items: "".join(f"<li>{i}</li>" for i in items)
    fonts = "family=Inter:wght@400;500;600;700;800" + (f"&family={font}" if font else "")
    alternates = "\n".join(f'  <link rel="alternate" hreflang="{c}" href="{SITE}{"" if f == "index.html" else f}">' for c, f, *_ in LANGS)
    alternates += f'\n  <link rel="alternate" hreflang="x-default" href="{SITE}">'
    switch = "\n".join(
        f'            <a href="{f}" lang="{c}"{" aria-current=\"true\"" if c == code else ""}>{n}</a>' for c, f, n, *_ in LANGS)
    jsonld = ""
    redirect = ""
    if code == "en":
        targets = ", ".join(f"{c}: '{f}'" for c, f, *_ in LANGS if c != "en")
        redirect = f"""    // First visit: open the page in the visitor's language (a choice made in the language menu wins).
    try {{
      const pages = {{ {targets} }};
      const saved = localStorage.getItem('muse-lang');
      const prefs = saved ? [saved] : (navigator.languages || [navigator.language || 'en']).map((l) => String(l).slice(0, 2).toLowerCase());
      const match = prefs.find((l) => l === 'en' || pages[l]);
      if (match && match !== 'en') location.replace(pages[match] + location.search + location.hash);
    }} catch (e) {{}}
"""
        jsonld = """  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"SoftwareApplication","name":"Muse","applicationCategory":"BusinessApplication","operatingSystem":"Web",
   "description":"AI copywriter for ads, social posts, product descriptions and emails in 11 languages.",
   "offers":[{"@type":"Offer","name":"Free","price":"0","priceCurrency":"USD"},{"@type":"Offer","name":"Creator","price":"19","priceCurrency":"USD"},{"@type":"Offer","name":"Pro","price":"49","priceCurrency":"USD"}]}
  </script>
"""
    features = "\n".join(
        f'''          <article class="card{" card--wide" if i == 0 else " card--full" if i == 5 else ""} reveal">
            <div class="card__icon">{icon}</div>
            <h3>{h}</h3>
            <p>{p}</p>
          </article>''' for i, (icon, h, p) in enumerate(t["f"]))
    tabs = "\n".join(
        f'            <button class="demo__tab{" is-active" if i == 0 else ""}{" demo__tab--live" if i == 3 else ""}" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-demo="{key}">{label}</button>'
        for i, (key, label) in enumerate(zip(["ad", "product", "email", "custom"], t["tabs"])))
    steps = "\n".join(f'          <li class="step reveal"><span class="step__num">{i + 1}</span><h3>{h}</h3><p>{p}</p></li>' for i, (h, p) in enumerate(t["steps"]))
    metrics = "\n".join(f'          <div><strong data-count="{n}">0</strong><span>{l}</span></div>' for n, l in t["metrics"])
    faq = "\n".join(f'          <details class="reveal"{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(t["faq"]))
    chips = t["chips"]
    marquee = "".join(f"<span>{c}</span>" for c in t["channels"]) + "\n            " + "".join(f'<span aria-hidden="true">{c}</span>' for c in t["channels"])

    page = f'''<!doctype html>
<html lang="{code}"{' dir="rtl"' if rtl else ''} data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t["title"]}</title>
  <meta name="description" content="{t["desc"]}">
  <meta name="theme-color" content="#0b0d14">
  <meta property="og:title" content="{t["og_title"]}">
  <meta property="og:description" content="{t["og_desc"]}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{t["og_locale"]}">
  <meta property="og:image" content="{SITE}assets/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
{alternates}
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="manifest" href="site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?{fonts}&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
{jsonld}  <script>
{redirect}    document.documentElement.classList.add('js');
    // Apply saved theme before paint to avoid a flash.
    try {{ const t = localStorage.getItem('theme'); if (t) document.documentElement.dataset.theme = t; }} catch (e) {{}}
  </script>
</head>
<body>
  <!-- Generated by tools/build_landing.py — edit the copy there, not here. -->
  <a class="skip-link" href="#main">{t["skip"]}</a>

  <header class="nav" id="nav">
    <div class="container nav__inner">
      <a href="#" class="logo" aria-label="{t["home"]}">
        <img src="assets/favicon.svg" alt="" width="28" height="28">
        <span>Muse</span>
      </a>
      <nav class="nav__links" id="navLinks" aria-label="{t["menu"]}">
        <a href="#features">{t["n_features"]}</a>
        <a href="#demo">{t["n_try"]}</a>
        <a href="#pricing">{t["n_pricing"]}</a>
        <a href="#faq">{t["n_faq"]}</a>
        <a href="{t["blog_href"]}">{t["n_blog"]}</a>
        <a href="login.html" class="nav__login">{t["login"]}</a>
      </nav>
      <div class="nav__actions">
        <details class="langs">
          <summary class="icon-btn langs__btn" aria-label="{t["lang_label"]}"><span aria-hidden="true">🌐</span> {short}</summary>
          <div class="langs__menu">
{switch}
          </div>
        </details>
        <button class="icon-btn" id="themeToggle" aria-label="{t["theme"]}">
          {SUN}
          {MOON}
        </button>
        <a href="login.html?mode=signup" class="btn btn--primary btn--sm nav__cta">{t["cta_nav"]}</a>
        <button class="icon-btn burger" id="burger" aria-label="{t["open_menu"]}" aria-expanded="false" aria-controls="navLinks">
          <span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <main id="main">
    <!-- HERO -->
    <section class="hero">
      <div class="hero__glow" aria-hidden="true"></div>
      <div class="container hero__inner">
        <a href="#demo" class="pill reveal">
          <span class="pill__tag">{t["pill_tag"]}</span> {t["pill"]} <span aria-hidden="true">{"←" if rtl else "→"}</span>
        </a>
        <h1 class="hero__title reveal">{t["h1a"]}<br><span class="gradient-text">{t["h1b"]}</span></h1>
        <p class="hero__sub reveal">{t["sub"]}</p>
        <div class="hero__cta reveal">
          <a href="login.html?mode=signup" class="btn btn--primary btn--lg">{t["cta1"]}</a>
          <a href="#demo" class="btn btn--ghost btn--lg">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
            {t["cta2"]}
          </a>
        </div>
        <p class="hero__note reveal">{t["note"]}</p>

        <div class="mockup reveal" aria-hidden="true">
          <div class="mockup__bar"><i></i><i></i><i></i><span>muse · studio</span></div>
          <div class="studio">
            <div class="studio__prompt">
              <span class="spark">✦</span>
              <span class="typing" id="typing"></span>
              <span class="studio__go">{t["go"]}</span>
            </div>
            <div class="studio__chips" id="studioChips">
              <span class="chip is-active">{chips[0]}</span><span class="chip">{chips[1]}</span><span class="chip">{chips[2]}</span>
              <span class="chip chip--ghost">{chips[3]}</span><span class="chip chip--ghost">{chips[4]}</span>
            </div>
            <div class="studio__out" id="studioOut"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- USE CASES -->
    <section class="logos">
      <div class="container">
        <p class="logos__title">{t["channels_title"]}</p>
        <div class="marquee">
          <div class="marquee__track">
            {marquee}
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURES -->
    <section class="section" id="features">
      <div class="container">
        <div class="section__head reveal">
          <span class="eyebrow">{t["f_eyebrow"]}</span>
          <h2>{t["f_h2"]}</h2>
          <p>{t["f_p"]}</p>
        </div>
        <div class="bento">
{features}
        </div>
      </div>
    </section>

    <!-- INTERACTIVE DEMO -->
    <section class="section section--alt" id="demo">
      <div class="container">
        <div class="section__head reveal">
          <span class="eyebrow">{t["d_eyebrow"]}</span>
          <h2>{t["d_h2"]}</h2>
          <p>{t["d_p"]}</p>
        </div>
        <div class="demo reveal">
          <div class="demo__tabs" role="tablist" aria-label="{t["tabs_label"]}">
{tabs}
          </div>
          <form class="demo__form" id="demoForm" hidden>
            <label for="demoInput" class="sr-only">{t["d_input"]}</label>
            <textarea id="demoInput" dir="auto" rows="2" maxlength="600" placeholder="{t["d_ph"]}"></textarea>
            <button class="btn btn--primary" type="submit" id="demoSubmit">{t["d_go"]}</button>
          </form>
          <div class="demo__panel">
            <div class="demo__prompt"><span class="demo__label">{t["d_prompt"]}</span><p id="demoPrompt"></p></div>
            <div class="demo__output">
              <span class="demo__label">Muse <span class="demo__status" id="demoStatus">{t["d_status"]}</span></span>
              <p id="demoOutput" dir="auto" aria-live="polite"></p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- HOW IT WORKS -->
    <section class="section" id="how">
      <div class="container">
        <div class="section__head reveal">
          <span class="eyebrow">{t["h_eyebrow"]}</span>
          <h2>{t["h_h2"]}</h2>
        </div>
        <ol class="steps">
{steps}
        </ol>
        <div class="metrics reveal">
{metrics}
        </div>
      </div>
    </section>

    <!-- PRICING -->
    <section class="section section--alt" id="pricing">
      <div class="container">
        <div class="section__head reveal">
          <span class="eyebrow">{t["p_eyebrow"]}</span>
          <h2>{t["p_h2"]}</h2>
          <p>{t["p_p"]}</p>
        </div>
        <div class="pricing">
          <article class="plan reveal">
            <h3>Free</h3>
            <p class="plan__desc">{t["free_desc"]}</p>
            <p class="plan__price"><span class="price">$0</span><small>{t["mo"]}</small></p>
            <a href="login.html?mode=signup" class="btn btn--ghost btn--block">{t["free_btn"]}</a>
            <ul class="plan__list">{li(t["free_list"])}</ul>
          </article>
          <article class="plan plan--featured reveal">
            <span class="plan__badge">{t["popular"]}</span>
            <h3>Creator</h3>
            <p class="plan__desc">{t["creator_desc"]}</p>
            <p class="plan__price"><span class="price">$19</span><small>{t["mo"]}</small></p>
            <a href="login.html?mode=signup&amp;plan=creator" class="btn btn--primary btn--block">{t["creator_btn"]}</a>
            <ul class="plan__list">{li(t["creator_list"])}</ul>
          </article>
          <article class="plan reveal">
            <h3>Pro</h3>
            <p class="plan__desc">{t["pro_desc"]}</p>
            <p class="plan__price"><span class="price">$49</span><small>{t["mo"]}</small></p>
            <a href="login.html?mode=signup&amp;plan=pro" class="btn btn--ghost btn--block">{t["pro_btn"]}</a>
            <ul class="plan__list">{li(t["pro_list"])}</ul>
          </article>
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section class="section" id="faq">
      <div class="container container--narrow">
        <div class="section__head reveal">
          <span class="eyebrow">{t["q_eyebrow"]}</span>
          <h2>{t["q_h2"]}</h2>
        </div>
        <div class="faq">
{faq}
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="section" id="contact">
      <div class="container">
        <div class="cta reveal">
          <div>
            <h2>{t["c_h2"]}</h2>
            <p>{t["c_p"]}</p>
          </div>
          <div class="cta__form">
            <a href="login.html?mode=signup" class="btn btn--light btn--lg">{t["c_btn"]}</a>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container footer__inner">
      <div class="footer__brand">
        <a href="#" class="logo"><img src="assets/favicon.svg" alt="" width="24" height="24"><span>Muse</span></a>
        <p>{t["ft_tag"]}</p>
      </div>
      <div class="footer__cols">
        <div><h4>{t["ft_product"]}</h4><a href="#features">{t["n_features"]}</a><a href="#pricing">{t["n_pricing"]}</a><a href="#faq">{t["n_faq"]}</a><a href="login.html">{t["login"]}</a></div>
        <div><h4>{t["ft_company"]}</h4><a href="about.html">{t["ft_about"]}</a><a href="{t["blog_href"]}">{t["ft_blog"]}</a><a href="about.html#contact">{t["ft_contact"]}</a></div>
        <div><h4>{t["ft_legal"]}</h4><a href="privacy.html">{t["ft_privacy"]}</a><a href="terms.html">{t["ft_terms"]}</a></div>
      </div>
    </div>
    <div class="container footer__bottom">
      <p>© <span id="year"></span> Muse. {t["rights"]}</p>
    </div>
  </footer>

  <script src="js/i18n.js" defer></script>
  <script src="js/main.js" defer></script>
</body>
</html>
'''
    (ROOT / fname).write_text(page, encoding="utf-8")


def update_sitemap():
    path = ROOT / "sitemap.xml"
    xml = path.read_text(encoding="utf-8")
    for _, fname, *_ in LANGS:
        if fname == "index.html":
            continue
        loc = f"{SITE}{fname}"
        if f"<loc>{loc}</loc>" not in xml:
            xml = xml.replace("</urlset>", f"  <url><loc>{loc}</loc><lastmod>2026-10-23</lastmod></url>\n</urlset>")
    path.write_text(xml, encoding="utf-8")


if __name__ == "__main__":
    keys = set(LANG["en"])
    for code, *_ in LANGS:
        missing = keys - set(LANG[code])
        assert not missing, f"{code} is missing {sorted(missing)}"
    for args in LANGS:
        build(*args)
    update_sitemap()
    print("built:", ", ".join(f for _, f, *_ in LANGS))
