// Interface translations for login.html, reset.html and app.html.
// Language = saved choice (localStorage "muse-lang", also set by the landing page switcher)
// → browser language → English. Elements opt in with data-i18n / data-i18n-html / data-i18n-ph / data-i18n-aria.
window.MuseUI = (() => {
  const LANGS = {
    en: { name: 'English', output: 'English' },
    zh: { name: '中文', output: 'Chinese' },
    hi: { name: 'हिन्दी', output: 'Hindi' },
    es: { name: 'Español', output: 'Spanish' },
    fr: { name: 'Français', output: 'French' },
    ar: { name: 'العربية', output: 'Arabic', rtl: true },
    uk: { name: 'Українська', output: 'Ukrainian' },
  };

  const T = {
    en: {
      welcome: 'Welcome back', create: 'Create your account', login_sub: 'Log in to keep writing.', signup_sub: '10 free generations every month. No card required.',
      tab_login: 'Log in', tab_signup: 'Sign up', google: 'Continue with Google', or_email: 'or with email',
      name: 'Full name', email: 'Email', password: 'Password', btn_login: 'Log in', btn_signup: 'Create account', forgot: 'Forgot password?',
      agree: 'By signing up you agree to our {terms} and {privacy}.', terms: 'Terms', privacy: 'Privacy Policy',
      err_fill: 'Please fill in all fields correctly.', err_pw: 'Password must be at least 8 characters.', err_invalid: 'Wrong email or password.',
      err_exists: 'This email is already registered. Log in instead.', err_unconfirmed: 'Please confirm your email first — check your inbox.',
      confirm_email: '📬 Almost there! Check your email to confirm your account.', not_ready: 'Accounts are not available yet. Please try again later.',
      reset_sent: '📬 If an account exists for this email, we’ve sent a link to reset your password.', email_first: 'Enter your email above, then tap “Forgot password?”.',
      reset_title: 'Set a new password', reset_sub: 'Choose a new password for your account.', new_pw: 'New password', btn_save_pw: 'Save password',
      reset_ok: '✓ Password updated! Opening your studio…', reset_invalid: 'This link is invalid or has expired. Request a new one from the login page.', back_login: '← Back to log in',
      credits: 'credits', credits_title: 'Generations left this month', upgrade: 'Upgrade', account: 'Account menu', plan: 'Plan', manage_billing: 'Manage billing', logout: 'Log out', ui_lang: 'Interface language',
      title_new: 'What do you want to write?', types: 'Content type',
      tpl_ad: 'Ad', tpl_social: 'Social post', tpl_product: 'Product description', tpl_email: 'Email', tpl_blog: 'Blog outline', tpl_slogan: 'Slogans', tpl_tiktok: 'Video script', tpl_review: 'Review reply', tpl_listing: 'Marketplace listing',
      describe: 'Describe it', ph_prompt: 'e.g. Cold brew coffee brand for busy students. Key benefit: smooth taste, no bitterness. Offer: first can for $1.',
      brand: 'About your business', brand_hint: 'optional · saved and used in every text', brand_ph: 'e.g. Drift — cold brew coffee shop in Kyiv. Young audience, playful tone, eco-friendly cups.', brand_save: 'Save', brand_saved: 'Saved ✓',
      tone: 'Tone', out_lang: 'Text language',
      tone_friendly: 'Friendly', tone_professional: 'Professional', tone_playful: 'Playful', tone_bold: 'Bold', tone_luxury: 'Luxury', tone_minimal: 'Minimal',
      generate: '✦ Generate', one_credit: '· 1 credit', result: 'Result', copy: 'Copy', copied: 'Copied ✓', select_copy: 'Select & copy',
      again: '↻ Another version', shorter: 'Shorter', longer: 'Longer',
      empty: 'Your content will appear here. Pick a type, describe what you need and hit Generate.', recent: 'Recent', no_history: 'No generations yet.',
      writing: 'writing…', done: 'done ✓',
      upgrade_title: 'Upgrade your plan', upgrade_lead: 'Get more generations every month. Cancel anytime.', per_mo: '/mo', best_value: 'Best value',
      gens300: '300 generations / month', gens1000: '1,000 generations / month', all_formats: 'All formats & languages', commercial: 'Commercial use', priority: 'Priority support',
      choose_creator: 'Choose Creator', choose_pro: 'Choose Pro', close: 'Close',
      out_of_credits: 'You’re out of credits. Pick a plan to keep creating.', payments_not_ready: 'Payments are not available yet. Please try again later.',
      not_setup: 'The studio is not available yet. Please try again later.', thanks_paid: '🎉 Thanks! Your plan is being activated…',
      err_empty: 'Please describe what you want to write.', err_too_long: 'Your description is too long (max 1,000 characters).', err_no_credits: 'You’re out of credits.',
      err_auth: 'Your session has expired. Please log in again.', err_busy: 'Muse is busy right now. Try again in a moment.', err_refused: 'Muse can’t help with that request. Try a different prompt — no credit was used.',
      err_server: 'Something went wrong. Please try again.', err_demo_limit: 'Free tries used up. Create a free account to get 10 generations a month.',
    },
    uk: {
      welcome: 'З поверненням', create: 'Створіть акаунт', login_sub: 'Увійдіть, щоб продовжити.', signup_sub: '10 безкоштовних генерацій щомісяця. Без картки.',
      tab_login: 'Вхід', tab_signup: 'Реєстрація', google: 'Продовжити з Google', or_email: 'або через email',
      name: 'Ім’я', email: 'Email', password: 'Пароль', btn_login: 'Увійти', btn_signup: 'Створити акаунт', forgot: 'Забули пароль?',
      agree: 'Реєструючись, ви погоджуєтеся з {terms} та {privacy}.', terms: 'Умовами', privacy: 'Політикою конфіденційності',
      err_fill: 'Заповніть усі поля правильно.', err_pw: 'Пароль має містити щонайменше 8 символів.', err_invalid: 'Неправильний email або пароль.',
      err_exists: 'Цей email уже зареєстровано. Увійдіть.', err_unconfirmed: 'Спершу підтвердьте email — перевірте пошту.',
      confirm_email: '📬 Майже готово! Перевірте пошту, щоб підтвердити акаунт.', not_ready: 'Акаунти поки недоступні. Спробуйте пізніше.',
      reset_sent: '📬 Якщо акаунт із цим email існує, ми надіслали посилання для зміни пароля.', email_first: 'Введіть email вище й натисніть «Забули пароль?».',
      reset_title: 'Новий пароль', reset_sub: 'Придумайте новий пароль для акаунта.', new_pw: 'Новий пароль', btn_save_pw: 'Зберегти пароль',
      reset_ok: '✓ Пароль змінено! Відкриваємо студію…', reset_invalid: 'Посилання недійсне або застаріло. Запросіть нове на сторінці входу.', back_login: '← До входу',
      credits: 'кредитів', credits_title: 'Генерацій залишилось цього місяця', upgrade: 'Тарифи', account: 'Меню акаунта', plan: 'Тариф', manage_billing: 'Керування оплатою', logout: 'Вийти', ui_lang: 'Мова інтерфейсу',
      title_new: 'Що написати?', types: 'Тип тексту',
      tpl_ad: 'Реклама', tpl_social: 'Пост', tpl_product: 'Опис товару', tpl_email: 'Лист', tpl_blog: 'План статті', tpl_slogan: 'Слогани', tpl_tiktok: 'Сценарій відео', tpl_review: 'Відповідь на відгук', tpl_listing: 'Картка товару',
      describe: 'Опишіть завдання', ph_prompt: 'Напр.: кав’ярня з холодною кавою для студентів. Перевага: м’який смак без гіркоти. Акція: перша чашка за 30 грн.',
      brand: 'Про ваш бізнес', brand_hint: 'необов’язково · зберігається й використовується в кожному тексті', brand_ph: 'Напр.: Drift — кав’ярня з холодною кавою в Києві. Молода аудиторія, грайливий тон, еко-стаканчики.', brand_save: 'Зберегти', brand_saved: 'Збережено ✓',
      tone: 'Тон', out_lang: 'Мова тексту',
      tone_friendly: 'Дружній', tone_professional: 'Діловий', tone_playful: 'Грайливий', tone_bold: 'Сміливий', tone_luxury: 'Преміальний', tone_minimal: 'Лаконічний',
      generate: '✦ Створити', one_credit: '· 1 кредит', result: 'Результат', copy: 'Копіювати', copied: 'Скопійовано ✓', select_copy: 'Виділіть і скопіюйте',
      again: '↻ Інший варіант', shorter: 'Коротше', longer: 'Довше',
      empty: 'Тут з’явиться текст. Оберіть тип, опишіть завдання й натисніть «Створити».', recent: 'Нещодавні', no_history: 'Ще немає текстів.',
      writing: 'пишу…', done: 'готово ✓',
      upgrade_title: 'Оберіть тариф', upgrade_lead: 'Більше генерацій щомісяця. Скасування будь-коли.', per_mo: '/міс', best_value: 'Найвигідніший',
      gens300: '300 генерацій на місяць', gens1000: '1000 генерацій на місяць', all_formats: 'Усі формати й мови', commercial: 'Комерційне використання', priority: 'Пріоритетна підтримка',
      choose_creator: 'Обрати Creator', choose_pro: 'Обрати Pro', close: 'Закрити',
      out_of_credits: 'Кредити закінчилися. Оберіть тариф, щоб продовжити.', payments_not_ready: 'Оплата поки недоступна. Спробуйте пізніше.',
      not_setup: 'Студія поки недоступна. Спробуйте пізніше.', thanks_paid: '🎉 Дякуємо! Тариф активується…',
      err_empty: 'Опишіть, що потрібно написати.', err_too_long: 'Опис задовгий (максимум 1000 символів).', err_no_credits: 'Кредити закінчилися.',
      err_auth: 'Сесія завершилась. Увійдіть знову.', err_busy: 'Muse зараз перевантажений. Спробуйте за хвилину.', err_refused: 'Muse не може виконати цей запит. Спробуйте інший — кредит не списано.',
      err_server: 'Щось пішло не так. Спробуйте ще раз.', err_demo_limit: 'Безкоштовні спроби вичерпано. Створіть акаунт і отримуйте 10 генерацій щомісяця.',
    },
    es: {
      welcome: 'Hola de nuevo', create: 'Crea tu cuenta', login_sub: 'Inicia sesión para seguir escribiendo.', signup_sub: '10 textos gratis cada mes. Sin tarjeta.',
      tab_login: 'Entrar', tab_signup: 'Registrarse', google: 'Continuar con Google', or_email: 'o con tu email',
      name: 'Nombre', email: 'Email', password: 'Contraseña', btn_login: 'Entrar', btn_signup: 'Crear cuenta', forgot: '¿Olvidaste tu contraseña?',
      agree: 'Al registrarte aceptas nuestros {terms} y la {privacy}.', terms: 'Términos', privacy: 'Política de privacidad',
      err_fill: 'Completa todos los campos correctamente.', err_pw: 'La contraseña debe tener al menos 8 caracteres.', err_invalid: 'Email o contraseña incorrectos.',
      err_exists: 'Este email ya está registrado. Inicia sesión.', err_unconfirmed: 'Primero confirma tu email: revisa tu bandeja de entrada.',
      confirm_email: '📬 ¡Casi listo! Revisa tu email para confirmar la cuenta.', not_ready: 'Las cuentas aún no están disponibles. Inténtalo más tarde.',
      reset_sent: '📬 Si existe una cuenta con este email, te hemos enviado un enlace para cambiar la contraseña.', email_first: 'Escribe tu email arriba y pulsa «¿Olvidaste tu contraseña?».',
      reset_title: 'Nueva contraseña', reset_sub: 'Elige una nueva contraseña para tu cuenta.', new_pw: 'Nueva contraseña', btn_save_pw: 'Guardar contraseña',
      reset_ok: '✓ ¡Contraseña actualizada! Abriendo tu estudio…', reset_invalid: 'El enlace no es válido o ha caducado. Pide uno nuevo desde la página de acceso.', back_login: '← Volver a iniciar sesión',
      credits: 'créditos', credits_title: 'Textos restantes este mes', upgrade: 'Mejorar plan', account: 'Menú de la cuenta', plan: 'Plan', manage_billing: 'Gestionar pagos', logout: 'Cerrar sesión', ui_lang: 'Idioma de la interfaz',
      title_new: '¿Qué quieres escribir?', types: 'Tipo de texto',
      tpl_ad: 'Anuncio', tpl_social: 'Post', tpl_product: 'Descripción de producto', tpl_email: 'Email', tpl_blog: 'Esquema de blog', tpl_slogan: 'Eslóganes', tpl_tiktok: 'Guion de vídeo', tpl_review: 'Respuesta a reseña', tpl_listing: 'Ficha de marketplace',
      describe: 'Descríbelo', ph_prompt: 'Ej.: café frío para estudiantes con prisa. Ventaja: sabor suave, sin amargor. Oferta: primera lata a 1 €.',
      brand: 'Sobre tu negocio', brand_hint: 'opcional · se guarda y se usa en cada texto', brand_ph: 'Ej.: Drift, cafetería de café frío en Madrid. Público joven, tono divertido, vasos ecológicos.', brand_save: 'Guardar', brand_saved: 'Guardado ✓',
      tone: 'Tono', out_lang: 'Idioma del texto',
      tone_friendly: 'Cercano', tone_professional: 'Profesional', tone_playful: 'Divertido', tone_bold: 'Atrevido', tone_luxury: 'De lujo', tone_minimal: 'Minimalista',
      generate: '✦ Generar', one_credit: '· 1 crédito', result: 'Resultado', copy: 'Copiar', copied: 'Copiado ✓', select_copy: 'Selecciona y copia',
      again: '↻ Otra versión', shorter: 'Más corto', longer: 'Más largo',
      empty: 'Aquí aparecerá tu texto. Elige un tipo, describe lo que necesitas y pulsa Generar.', recent: 'Recientes', no_history: 'Aún no hay textos.',
      writing: 'escribiendo…', done: 'listo ✓',
      upgrade_title: 'Mejora tu plan', upgrade_lead: 'Más textos cada mes. Cancela cuando quieras.', per_mo: '/mes', best_value: 'Mejor precio',
      gens300: '300 textos al mes', gens1000: '1.000 textos al mes', all_formats: 'Todos los formatos e idiomas', commercial: 'Uso comercial', priority: 'Soporte prioritario',
      choose_creator: 'Elegir Creator', choose_pro: 'Elegir Pro', close: 'Cerrar',
      out_of_credits: 'Te has quedado sin créditos. Elige un plan para seguir.', payments_not_ready: 'Los pagos aún no están disponibles. Inténtalo más tarde.',
      not_setup: 'El estudio aún no está disponible. Inténtalo más tarde.', thanks_paid: '🎉 ¡Gracias! Estamos activando tu plan…',
      err_empty: 'Describe lo que quieres escribir.', err_too_long: 'La descripción es demasiado larga (máx. 1.000 caracteres).', err_no_credits: 'Te has quedado sin créditos.',
      err_auth: 'Tu sesión ha caducado. Inicia sesión de nuevo.', err_busy: 'Muse está ocupado ahora mismo. Inténtalo en un momento.', err_refused: 'Muse no puede ayudar con esa petición. Prueba otra: no se ha usado ningún crédito.',
      err_server: 'Algo ha fallado. Inténtalo de nuevo.', err_demo_limit: 'Has usado los intentos gratis. Crea una cuenta y obtén 10 textos al mes.',
    },
    fr: {
      welcome: 'Bon retour', create: 'Créez votre compte', login_sub: 'Connectez-vous pour continuer à écrire.', signup_sub: '10 textes gratuits chaque mois. Sans carte bancaire.',
      tab_login: 'Connexion', tab_signup: 'Inscription', google: 'Continuer avec Google', or_email: 'ou par email',
      name: 'Nom complet', email: 'Email', password: 'Mot de passe', btn_login: 'Se connecter', btn_signup: 'Créer un compte', forgot: 'Mot de passe oublié ?',
      agree: 'En vous inscrivant, vous acceptez nos {terms} et notre {privacy}.', terms: 'Conditions', privacy: 'Politique de confidentialité',
      err_fill: 'Veuillez remplir correctement tous les champs.', err_pw: 'Le mot de passe doit contenir au moins 8 caractères.', err_invalid: 'Email ou mot de passe incorrect.',
      err_exists: 'Cet email est déjà inscrit. Connectez-vous.', err_unconfirmed: 'Confirmez d’abord votre email : vérifiez votre boîte de réception.',
      confirm_email: '📬 Presque terminé ! Vérifiez vos emails pour confirmer votre compte.', not_ready: 'Les comptes ne sont pas encore disponibles. Réessayez plus tard.',
      reset_sent: '📬 Si un compte existe pour cet email, nous avons envoyé un lien pour réinitialiser le mot de passe.', email_first: 'Saisissez votre email ci-dessus, puis touchez « Mot de passe oublié ? ».',
      reset_title: 'Nouveau mot de passe', reset_sub: 'Choisissez un nouveau mot de passe pour votre compte.', new_pw: 'Nouveau mot de passe', btn_save_pw: 'Enregistrer',
      reset_ok: '✓ Mot de passe mis à jour ! Ouverture de votre studio…', reset_invalid: 'Ce lien est invalide ou a expiré. Demandez-en un nouveau depuis la page de connexion.', back_login: '← Retour à la connexion',
      credits: 'crédits', credits_title: 'Textes restants ce mois-ci', upgrade: 'Changer d’offre', account: 'Menu du compte', plan: 'Offre', manage_billing: 'Gérer la facturation', logout: 'Se déconnecter', ui_lang: 'Langue de l’interface',
      title_new: 'Que voulez-vous écrire ?', types: 'Type de texte',
      tpl_ad: 'Pub', tpl_social: 'Post', tpl_product: 'Fiche produit', tpl_email: 'Email', tpl_blog: 'Plan d’article', tpl_slogan: 'Slogans', tpl_tiktok: 'Script vidéo', tpl_review: 'Réponse à un avis', tpl_listing: 'Annonce marketplace',
      describe: 'Décrivez-le', ph_prompt: 'Ex. : café infusé à froid pour étudiants pressés. Atout : goût doux, sans amertume. Offre : 1re canette à 1 €.',
      brand: 'Votre entreprise', brand_hint: 'facultatif · enregistré et utilisé dans chaque texte', brand_ph: 'Ex. : Drift, café spécialisé en cold brew à Lyon. Public jeune, ton ludique, gobelets écologiques.', brand_save: 'Enregistrer', brand_saved: 'Enregistré ✓',
      tone: 'Ton', out_lang: 'Langue du texte',
      tone_friendly: 'Chaleureux', tone_professional: 'Professionnel', tone_playful: 'Ludique', tone_bold: 'Audacieux', tone_luxury: 'Luxe', tone_minimal: 'Minimaliste',
      generate: '✦ Générer', one_credit: '· 1 crédit', result: 'Résultat', copy: 'Copier', copied: 'Copié ✓', select_copy: 'Sélectionnez et copiez',
      again: '↻ Autre version', shorter: 'Plus court', longer: 'Plus long',
      empty: 'Votre texte apparaîtra ici. Choisissez un type, décrivez votre besoin et cliquez sur Générer.', recent: 'Récents', no_history: 'Aucun texte pour l’instant.',
      writing: 'rédaction…', done: 'terminé ✓',
      upgrade_title: 'Passez à l’offre supérieure', upgrade_lead: 'Plus de textes chaque mois. Résiliable à tout moment.', per_mo: '/mois', best_value: 'Meilleur rapport',
      gens300: '300 textes par mois', gens1000: '1 000 textes par mois', all_formats: 'Tous les formats et langues', commercial: 'Usage commercial', priority: 'Support prioritaire',
      choose_creator: 'Choisir Creator', choose_pro: 'Choisir Pro', close: 'Fermer',
      out_of_credits: 'Vous n’avez plus de crédits. Choisissez une offre pour continuer.', payments_not_ready: 'Les paiements ne sont pas encore disponibles. Réessayez plus tard.',
      not_setup: 'Le studio n’est pas encore disponible. Réessayez plus tard.', thanks_paid: '🎉 Merci ! Votre offre est en cours d’activation…',
      err_empty: 'Décrivez ce que vous voulez écrire.', err_too_long: 'La description est trop longue (1 000 caractères max).', err_no_credits: 'Vous n’avez plus de crédits.',
      err_auth: 'Votre session a expiré. Reconnectez-vous.', err_busy: 'Muse est très sollicité. Réessayez dans un instant.', err_refused: 'Muse ne peut pas traiter cette demande. Essayez autre chose : aucun crédit n’a été utilisé.',
      err_server: 'Une erreur s’est produite. Réessayez.', err_demo_limit: 'Essais gratuits épuisés. Créez un compte gratuit pour obtenir 10 textes par mois.',
    },
    zh: {
      welcome: '欢迎回来', create: '创建账户', login_sub: '登录后继续写作。', signup_sub: '每月免费 10 次生成，无需信用卡。',
      tab_login: '登录', tab_signup: '注册', google: '使用 Google 继续', or_email: '或使用邮箱',
      name: '姓名', email: '邮箱', password: '密码', btn_login: '登录', btn_signup: '创建账户', forgot: '忘记密码？',
      agree: '注册即表示你同意我们的{terms}和{privacy}。', terms: '服务条款', privacy: '隐私政策',
      err_fill: '请正确填写所有字段。', err_pw: '密码至少需要 8 个字符。', err_invalid: '邮箱或密码错误。',
      err_exists: '该邮箱已注册，请直接登录。', err_unconfirmed: '请先确认你的邮箱，查看收件箱。',
      confirm_email: '📬 快好了！请查看邮箱确认你的账户。', not_ready: '账户功能暂不可用，请稍后再试。',
      reset_sent: '📬 如果该邮箱已注册，我们已发送重置密码的链接。', email_first: '请先在上方输入邮箱，再点击“忘记密码？”。',
      reset_title: '设置新密码', reset_sub: '为你的账户设置一个新密码。', new_pw: '新密码', btn_save_pw: '保存密码',
      reset_ok: '✓ 密码已更新！正在打开工作台…', reset_invalid: '链接无效或已过期，请在登录页重新申请。', back_login: '← 返回登录',
      credits: '积分', credits_title: '本月剩余生成次数', upgrade: '升级', account: '账户菜单', plan: '套餐', manage_billing: '管理账单', logout: '退出登录', ui_lang: '界面语言',
      title_new: '你想写什么？', types: '内容类型',
      tpl_ad: '广告', tpl_social: '社交帖子', tpl_product: '产品描述', tpl_email: '邮件', tpl_blog: '博客大纲', tpl_slogan: '口号', tpl_tiktok: '短视频脚本', tpl_review: '评价回复', tpl_listing: '电商商品页',
      describe: '描述需求', ph_prompt: '例如：给忙碌学生的冷萃咖啡。卖点：口感顺滑、零苦涩。优惠：首罐 1 元。',
      brand: '你的业务简介', brand_hint: '可选 · 保存后会用于每条文案', brand_ph: '例如：Drift，上海的冷萃咖啡店。年轻客群，语气俏皮，环保杯。', brand_save: '保存', brand_saved: '已保存 ✓',
      tone: '语气', out_lang: '文案语言',
      tone_friendly: '亲切', tone_professional: '专业', tone_playful: '俏皮', tone_bold: '大胆', tone_luxury: '高端', tone_minimal: '简约',
      generate: '✦ 生成', one_credit: '· 1 积分', result: '结果', copy: '复制', copied: '已复制 ✓', select_copy: '请选中后复制',
      again: '↻ 换一版', shorter: '更短', longer: '更长',
      empty: '文案会显示在这里。选择类型、描述需求，然后点击“生成”。', recent: '最近', no_history: '还没有生成记录。',
      writing: '写作中…', done: '完成 ✓',
      upgrade_title: '升级套餐', upgrade_lead: '每月获得更多生成次数，随时可取消。', per_mo: '/月', best_value: '最划算',
      gens300: '每月 300 次生成', gens1000: '每月 1,000 次生成', all_formats: '全部格式和语言', commercial: '可商用', priority: '优先支持',
      choose_creator: '选择 Creator', choose_pro: '选择 Pro', close: '关闭',
      out_of_credits: '积分已用完，选择套餐继续创作。', payments_not_ready: '支付功能暂不可用，请稍后再试。',
      not_setup: '工作台暂不可用，请稍后再试。', thanks_paid: '🎉 感谢购买！正在激活你的套餐…',
      err_empty: '请描述你想写的内容。', err_too_long: '描述太长（最多 1,000 个字符）。', err_no_credits: '积分已用完。',
      err_auth: '登录已过期，请重新登录。', err_busy: 'Muse 当前繁忙，请稍后再试。', err_refused: 'Muse 无法处理此请求，请换个说法，未扣除积分。',
      err_server: '出了点问题，请重试。', err_demo_limit: '免费试用次数已用完。注册免费账户，每月可生成 10 次。',
    },
    hi: {
      welcome: 'फिर से स्वागत है', create: 'अपना अकाउंट बनाएँ', login_sub: 'लिखना जारी रखने के लिए लॉग इन करें।', signup_sub: 'हर महीने 10 मुफ़्त जनरेशन। कार्ड की ज़रूरत नहीं।',
      tab_login: 'लॉग इन', tab_signup: 'साइन अप', google: 'Google से जारी रखें', or_email: 'या ईमेल से',
      name: 'पूरा नाम', email: 'ईमेल', password: 'पासवर्ड', btn_login: 'लॉग इन करें', btn_signup: 'अकाउंट बनाएँ', forgot: 'पासवर्ड भूल गए?',
      agree: 'साइन अप करके आप हमारी {terms} और {privacy} से सहमत होते हैं।', terms: 'शर्तों', privacy: 'प्राइवेसी पॉलिसी',
      err_fill: 'कृपया सभी फ़ील्ड सही से भरें।', err_pw: 'पासवर्ड कम से कम 8 अक्षरों का होना चाहिए।', err_invalid: 'ईमेल या पासवर्ड गलत है।',
      err_exists: 'यह ईमेल पहले से रजिस्टर्ड है। लॉग इन करें।', err_unconfirmed: 'पहले अपना ईमेल कन्फ़र्म करें — इनबॉक्स देखें।',
      confirm_email: '📬 बस थोड़ा और! अकाउंट कन्फ़र्म करने के लिए अपना ईमेल देखें।', not_ready: 'अकाउंट अभी उपलब्ध नहीं हैं। बाद में कोशिश करें।',
      reset_sent: '📬 अगर इस ईमेल से अकाउंट है, तो हमने पासवर्ड बदलने का लिंक भेज दिया है।', email_first: 'ऊपर अपना ईमेल लिखें, फिर “पासवर्ड भूल गए?” दबाएँ।',
      reset_title: 'नया पासवर्ड सेट करें', reset_sub: 'अपने अकाउंट के लिए नया पासवर्ड चुनें।', new_pw: 'नया पासवर्ड', btn_save_pw: 'पासवर्ड सेव करें',
      reset_ok: '✓ पासवर्ड बदल गया! आपका स्टूडियो खुल रहा है…', reset_invalid: 'यह लिंक अमान्य है या इसकी समय-सीमा खत्म हो गई है। लॉग इन पेज से नया लिंक माँगें।', back_login: '← लॉग इन पर वापस',
      credits: 'क्रेडिट', credits_title: 'इस महीने बचे जनरेशन', upgrade: 'अपग्रेड', account: 'अकाउंट मेनू', plan: 'प्लान', manage_billing: 'बिलिंग मैनेज करें', logout: 'लॉग आउट', ui_lang: 'इंटरफ़ेस भाषा',
      title_new: 'आप क्या लिखना चाहते हैं?', types: 'कंटेंट का प्रकार',
      tpl_ad: 'विज्ञापन', tpl_social: 'सोशल पोस्ट', tpl_product: 'प्रोडक्ट डिस्क्रिप्शन', tpl_email: 'ईमेल', tpl_blog: 'ब्लॉग आउटलाइन', tpl_slogan: 'स्लोगन', tpl_tiktok: 'वीडियो स्क्रिप्ट', tpl_review: 'रिव्यू का जवाब', tpl_listing: 'मार्केटप्लेस लिस्टिंग',
      describe: 'बताइए', ph_prompt: 'जैसे: व्यस्त छात्रों के लिए कोल्ड कॉफ़ी। ख़ासियत: स्मूद स्वाद, बिना कड़वाहट। ऑफ़र: पहली कैन ₹49।',
      brand: 'आपके बिज़नेस के बारे में', brand_hint: 'वैकल्पिक · सेव होकर हर टेक्स्ट में इस्तेमाल होता है', brand_ph: 'जैसे: Drift — बेंगलुरु की कोल्ड ब्रू कॉफ़ी शॉप। युवा ग्राहक, मज़ेदार टोन, इको-फ़्रेंडली कप।', brand_save: 'सेव करें', brand_saved: 'सेव हो गया ✓',
      tone: 'टोन', out_lang: 'टेक्स्ट की भाषा',
      tone_friendly: 'दोस्ताना', tone_professional: 'प्रोफ़ेशनल', tone_playful: 'मज़ेदार', tone_bold: 'बोल्ड', tone_luxury: 'लग्ज़री', tone_minimal: 'मिनिमल',
      generate: '✦ बनाएँ', one_credit: '· 1 क्रेडिट', result: 'नतीजा', copy: 'कॉपी करें', copied: 'कॉपी हो गया ✓', select_copy: 'चुनकर कॉपी करें',
      again: '↻ दूसरा वर्ज़न', shorter: 'छोटा', longer: 'लंबा',
      empty: 'आपका टेक्स्ट यहाँ दिखेगा। प्रकार चुनें, ज़रूरत बताइए और “बनाएँ” दबाएँ।', recent: 'हाल के', no_history: 'अभी कोई टेक्स्ट नहीं।',
      writing: 'लिख रहा है…', done: 'तैयार ✓',
      upgrade_title: 'अपना प्लान अपग्रेड करें', upgrade_lead: 'हर महीने ज़्यादा जनरेशन। कभी भी रद्द करें।', per_mo: '/माह', best_value: 'सबसे फ़ायदेमंद',
      gens300: 'हर महीने 300 जनरेशन', gens1000: 'हर महीने 1,000 जनरेशन', all_formats: 'सभी फ़ॉर्मेट और भाषाएँ', commercial: 'कमर्शियल इस्तेमाल', priority: 'प्राथमिकता सपोर्ट',
      choose_creator: 'Creator चुनें', choose_pro: 'Pro चुनें', close: 'बंद करें',
      out_of_credits: 'आपके क्रेडिट खत्म हो गए। जारी रखने के लिए प्लान चुनें।', payments_not_ready: 'भुगतान अभी उपलब्ध नहीं है। बाद में कोशिश करें।',
      not_setup: 'स्टूडियो अभी उपलब्ध नहीं है। बाद में कोशिश करें।', thanks_paid: '🎉 धन्यवाद! आपका प्लान चालू हो रहा है…',
      err_empty: 'बताइए कि आप क्या लिखना चाहते हैं।', err_too_long: 'विवरण बहुत लंबा है (अधिकतम 1,000 अक्षर)।', err_no_credits: 'आपके क्रेडिट खत्म हो गए।',
      err_auth: 'आपका सेशन खत्म हो गया। फिर से लॉग इन करें।', err_busy: 'Muse अभी व्यस्त है। थोड़ी देर में कोशिश करें।', err_refused: 'Muse इस अनुरोध में मदद नहीं कर सकता। कुछ और आज़माएँ — कोई क्रेडिट नहीं कटा।',
      err_server: 'कुछ गड़बड़ हो गई। फिर से कोशिश करें।', err_demo_limit: 'मुफ़्त प्रयास खत्म। हर महीने 10 जनरेशन के लिए मुफ़्त अकाउंट बनाएँ।',
    },
    ar: {
      welcome: 'مرحبًا بعودتك', create: 'أنشئ حسابك', login_sub: 'سجّل الدخول لمتابعة الكتابة.', signup_sub: '10 نصوص مجانية كل شهر. دون بطاقة.',
      tab_login: 'تسجيل الدخول', tab_signup: 'إنشاء حساب', google: 'المتابعة باستخدام Google', or_email: 'أو بالبريد الإلكتروني',
      name: 'الاسم الكامل', email: 'البريد الإلكتروني', password: 'كلمة المرور', btn_login: 'تسجيل الدخول', btn_signup: 'إنشاء الحساب', forgot: 'نسيت كلمة المرور؟',
      agree: 'بالتسجيل، أنت توافق على {terms} و{privacy}.', terms: 'الشروط', privacy: 'سياسة الخصوصية',
      err_fill: 'يرجى ملء جميع الحقول بشكل صحيح.', err_pw: 'يجب أن تتكون كلمة المرور من 8 أحرف على الأقل.', err_invalid: 'البريد الإلكتروني أو كلمة المرور غير صحيحة.',
      err_exists: 'هذا البريد مسجّل بالفعل. سجّل الدخول.', err_unconfirmed: 'يرجى تأكيد بريدك أولًا، تحقق من صندوق الوارد.',
      confirm_email: '📬 اقتربنا! تحقق من بريدك لتأكيد حسابك.', not_ready: 'الحسابات غير متاحة بعد. حاول لاحقًا.',
      reset_sent: '📬 إذا كان هناك حساب بهذا البريد، فقد أرسلنا رابطًا لإعادة تعيين كلمة المرور.', email_first: 'أدخل بريدك في الأعلى، ثم اضغط «نسيت كلمة المرور؟».',
      reset_title: 'تعيين كلمة مرور جديدة', reset_sub: 'اختر كلمة مرور جديدة لحسابك.', new_pw: 'كلمة المرور الجديدة', btn_save_pw: 'حفظ كلمة المرور',
      reset_ok: '✓ تم تحديث كلمة المرور! جارٍ فتح الاستوديو…', reset_invalid: 'الرابط غير صالح أو انتهت صلاحيته. اطلب رابطًا جديدًا من صفحة تسجيل الدخول.', back_login: '→ العودة إلى تسجيل الدخول',
      credits: 'رصيد', credits_title: 'النصوص المتبقية هذا الشهر', upgrade: 'ترقية', account: 'قائمة الحساب', plan: 'الخطة', manage_billing: 'إدارة الفوترة', logout: 'تسجيل الخروج', ui_lang: 'لغة الواجهة',
      title_new: 'ماذا تريد أن تكتب؟', types: 'نوع المحتوى',
      tpl_ad: 'إعلان', tpl_social: 'منشور', tpl_product: 'وصف منتج', tpl_email: 'بريد', tpl_blog: 'مخطط مقال', tpl_slogan: 'شعارات', tpl_tiktok: 'سيناريو فيديو', tpl_review: 'رد على تقييم', tpl_listing: 'صفحة منتج في متجر',
      describe: 'صِف ما تريد', ph_prompt: 'مثال: قهوة باردة للطلاب المشغولين. الميزة: طعم ناعم بلا مرارة. العرض: العلبة الأولى بدولار.',
      brand: 'عن نشاطك التجاري', brand_hint: 'اختياري · يُحفظ ويُستخدم في كل نص', brand_ph: 'مثال: Drift، مقهى قهوة باردة في دبي. جمهور شاب، أسلوب مرح، أكواب صديقة للبيئة.', brand_save: 'حفظ', brand_saved: 'تم الحفظ ✓',
      tone: 'الأسلوب', out_lang: 'لغة النص',
      tone_friendly: 'ودود', tone_professional: 'احترافي', tone_playful: 'مرح', tone_bold: 'جريء', tone_luxury: 'فاخر', tone_minimal: 'بسيط',
      generate: '✦ إنشاء', one_credit: '· رصيد واحد', result: 'النتيجة', copy: 'نسخ', copied: 'تم النسخ ✓', select_copy: 'حدّد وانسخ',
      again: '↻ نسخة أخرى', shorter: 'أقصر', longer: 'أطول',
      empty: 'سيظهر نصك هنا. اختر النوع، وصِف ما تحتاجه، ثم اضغط «إنشاء».', recent: 'الأحدث', no_history: 'لا توجد نصوص بعد.',
      writing: 'جارٍ الكتابة…', done: 'تم ✓',
      upgrade_title: 'رقِّ خطتك', upgrade_lead: 'نصوص أكثر كل شهر. ألغِ في أي وقت.', per_mo: '/شهر', best_value: 'الأفضل قيمة',
      gens300: '300 نص شهريًا', gens1000: '1000 نص شهريًا', all_formats: 'كل القوالب واللغات', commercial: 'استخدام تجاري', priority: 'دعم ذو أولوية',
      choose_creator: 'اختر Creator', choose_pro: 'اختر Pro', close: 'إغلاق',
      out_of_credits: 'نفد رصيدك. اختر خطة للمتابعة.', payments_not_ready: 'الدفع غير متاح بعد. حاول لاحقًا.',
      not_setup: 'الاستوديو غير متاح بعد. حاول لاحقًا.', thanks_paid: '🎉 شكرًا لك! جارٍ تفعيل خطتك…',
      err_empty: 'صِف ما تريد كتابته.', err_too_long: 'الوصف طويل جدًا (1000 حرف كحد أقصى).', err_no_credits: 'نفد رصيدك.',
      err_auth: 'انتهت جلستك. سجّل الدخول مرة أخرى.', err_busy: 'Muse مشغول الآن. حاول بعد قليل.', err_refused: 'لا يستطيع Muse تنفيذ هذا الطلب. جرّب طلبًا آخر، لم يُخصم أي رصيد.',
      err_server: 'حدث خطأ ما. حاول مرة أخرى.', err_demo_limit: 'انتهت المحاولات المجانية. أنشئ حسابًا مجانيًا للحصول على 10 نصوص شهريًا.',
    },
  };

  const read = (k) => { try { return localStorage.getItem(k); } catch (e) { return null; } };
  const write = (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} };

  const fromUrl = new URLSearchParams(location.search).get('lang');
  if (fromUrl && LANGS[fromUrl]) write('muse-lang', fromUrl);
  const browser = (navigator.languages || [navigator.language || 'en']).map((l) => String(l).slice(0, 2).toLowerCase());
  const lang = [read('muse-lang'), ...browser].find((l) => LANGS[l]) || 'en';

  const t = (key, vars) => {
    let s = (T[lang] && T[lang][key]) ?? T.en[key] ?? key;
    if (vars) Object.entries(vars).forEach(([k, v]) => { s = s.split(`{${k}}`).join(v); });
    return s;
  };

  const apply = (root = document) => {
    document.documentElement.lang = lang;
    document.documentElement.dir = LANGS[lang].rtl ? 'rtl' : 'ltr';
    root.querySelectorAll('[data-i18n]').forEach((el) => { el.textContent = t(el.dataset.i18n); });
    root.querySelectorAll('[data-i18n-ph]').forEach((el) => { el.placeholder = t(el.dataset.i18nPh); });
    root.querySelectorAll('[data-i18n-aria]').forEach((el) => { el.setAttribute('aria-label', t(el.dataset.i18nAria)); });
    root.querySelectorAll('[data-i18n-title]').forEach((el) => { el.title = t(el.dataset.i18nTitle); });
    // Sentences with links: {terms}/{privacy} are replaced by the element's own <a data-slot> children.
    root.querySelectorAll('[data-i18n-slots]').forEach((el) => {
      const slots = Object.fromEntries([...el.querySelectorAll('[data-slot]')].map((a) => [a.dataset.slot, a]));
      Object.values(slots).forEach((a) => { a.textContent = t(a.dataset.slot); });
      el.replaceChildren(...t(el.dataset.i18nSlots).split(/(\{\w+\})/).map((part) => {
        const m = part.match(/^\{(\w+)\}$/);
        return m && slots[m[1]] ? slots[m[1]] : document.createTextNode(part);
      }));
    });
    // Language picker: <select data-lang-picker>
    root.querySelectorAll('select[data-lang-picker]').forEach((sel) => {
      sel.replaceChildren(...Object.entries(LANGS).map(([code, l]) => new Option(l.name, code, false, code === lang)));
      sel.addEventListener('change', () => { write('muse-lang', sel.value); location.reload(); });
    });
  };

  return { lang, t, apply, outputLanguage: LANGS[lang].output, languages: LANGS };
})();
