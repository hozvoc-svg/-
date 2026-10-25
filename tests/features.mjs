import { createRequire } from 'node:module';
import fs from 'node:fs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const H = await import('./server.mjs'); await H.start();
const B = H.BASE; let fails = 0; const errs = [];
const check = (name, cond, extra = '') => { console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? '  ' + extra : '')); if (!cond) fails++; };
const SB = fs.readFileSync(H.ROOT + '/node_modules/@supabase/supabase-js/dist/umd/supabase.js', 'utf8');
const browser = await chromium.launch();
const newCtx = async (opts = {}) => {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, ...opts });
  await ctx.route('https://cdn.jsdelivr.net/**', (r) => r.fulfill({ status: 200, contentType: 'text/javascript', body: SB }));
  await ctx.route('https://fonts.googleapis.com/**', (r) => r.fulfill({ status: 200, contentType: 'text/css', body: '' }));
  return ctx;
};
const watch = (p, tag) => { p.on('pageerror', (e) => errs.push(tag + ': ' + e.message)); };

// 1. Auto language on the landing page
let ctx = await newCtx({ locale: 'es-ES' });
let p = await ctx.newPage(); watch(p, 'auto-es');
await p.goto(B + '/index.html'); await p.waitForURL(/es\.html/, { timeout: 4000 }).catch(() => {});
check('Spanish browser is sent to es.html', p.url().endsWith('/es.html'), p.url());
await p.click('.langs summary'); await p.click('.langs__menu a[lang="en"]');
await p.waitForTimeout(500); await p.goto(B + '/index.html'); await p.waitForTimeout(500);
check('after choosing English, index stays English', p.url().endsWith('/index.html'), p.url());
await ctx.close();
ctx = await newCtx({ locale: 'en-US' }); p = await ctx.newPage();
await p.goto(B + '/index.html'); await p.waitForTimeout(500);
check('English browser stays on index.html', p.url().endsWith('/index.html'));
await ctx.close();

// 2. Translated login (Ukrainian via saved choice from landing)
ctx = await newCtx({ locale: 'en-US' }); p = await ctx.newPage(); watch(p, 'uk-login');
await p.goto(B + '/uk.html'); await p.click('.langs summary'); await p.click('.langs__menu a[lang="uk"]');
await p.goto(B + '/login.html?mode=signup');
check('login in Ukrainian', (await p.textContent('#authCard h1:not([hidden])')).includes('Створіть') && (await p.textContent('#authSubmit')) === 'Створити акаунт', await p.textContent('#authSubmit'));
check('terms sentence with links translated', /Умовами/.test(await p.textContent('.auth-note')) && (await p.$$('.auth-note a')).length === 2, await p.textContent('.auth-note'));
await p.fill('input[name=name]', 'Олена'); await p.fill('input[name=email]', 'olena@ua.test'); await p.fill('input[name=password]', '123');
await p.click('#authSubmit');
check('validation message in Ukrainian', /щонайменше 8/.test(await p.textContent('#authMsg')));
await p.fill('input[name=password]', 'password123'); await p.click('#authSubmit');
await p.waitForURL(/app\.html/, { timeout: 5000 }).catch(() => {});
await p.waitForFunction(() => document.querySelector('#creditsCount').textContent !== '–', null, { timeout: 5000 }).catch(() => {});
check('studio in Ukrainian', (await p.textContent('#newTitle')) === 'Що написати?' && (await p.textContent('[data-template="review"] b')) === 'Відповідь на відгук');
check('text language defaults to Ukrainian', (await p.inputValue('#language')) === 'Ukrainian');
check('9 formats shown', (await p.locator('.tpl').count()) === 9);

// 3. Business profile is saved and used
await p.click('#brandBox summary'); await p.fill('#brand', 'Кав’ярня Drift у Києві');
await p.click('#brandSave'); await p.waitForTimeout(500);
const uid = Object.values(H.db.users).find((u) => u.email === 'olena@ua.test').id;
check('brand saved via /api/profile', H.db.profiles[uid].brand === 'Кав’ярня Drift у Києві' && /Збережено/.test(await p.textContent('#brandMsg')));
await p.click('[data-template="tiktok"]'); await p.fill('#prompt', 'Відео про нову каву');
await p.click('#genBtn');
await p.waitForFunction(() => document.querySelector('#genStatus').textContent.includes('готово'), null, { timeout: 8000 }).catch(() => {});
let req = H.anthropicRequests.at(-1);
check('brand + template + language sent', req.body.messages[0].content.startsWith('About my business: Кав’ярня Drift') && /video script/.test(req.body.system) && /Ukrainian/.test(req.body.system));
check('refine buttons visible', await p.isVisible('#refine'));

// 4. Refine: shorter
const before = H.db.profiles[uid].credits;
await p.click('#refine [data-mode="shorter"]');
await p.waitForFunction(() => document.querySelector('#genStatus').textContent.includes('готово'), null, { timeout: 8000 }).catch(() => {});
req = H.anthropicRequests.at(-1);
check('shorter sends previous answer + instruction', req.body.messages.length === 3 && req.body.messages[1].role === 'assistant' && /half as long/.test(req.body.messages[2].content));
check('refine costs one credit', H.db.profiles[uid].credits === before - 1, `${before} -> ${H.db.profiles[uid].credits}`);
await p.click('#refine [data-mode="again"]');
await p.waitForFunction(() => document.querySelector('#genStatus').textContent.includes('готово'), null, { timeout: 8000 }).catch(() => {});
req = H.anthropicRequests.at(-1);
check('"another version" keeps original prompt', req.body.messages[0].content.endsWith('Відео про нову каву') && /different version/.test(req.body.messages[2].content));

// 5. Translated server error (no credits)
H.db.profiles[uid].credits = 0;
await p.fill('#prompt', 'ще'); await p.click('#genBtn');
await p.waitForSelector('#upgradeModal[open]', { timeout: 5000 }).catch(() => {});
check('no-credits modal in Ukrainian', /Кредити закінчилися/.test(await p.textContent('#upgradeLead')));
await p.keyboard.press('Escape');
await p.screenshot({ path: H.ROOT + '/tests/.output/app-uk.png' });

// 6. Interface language picker in the account menu
await p.click('.account summary'); await p.selectOption('.account__lang select', 'ar');
await p.waitForLoadState('load'); await p.waitForTimeout(800);
check('switching to Arabic flips layout', (await p.getAttribute('html', 'dir')) === 'rtl' && (await p.textContent('#newTitle')) === 'ماذا تريد أن تكتب؟');
await p.screenshot({ path: H.ROOT + '/tests/.output/app-ar.png' });
await ctx.close();

// 6b. Google button follows the Supabase setting
H.db.googleEnabled = false;
ctx = await newCtx({ locale: 'en-US' }); p = await ctx.newPage();
await p.goto(B + '/login.html'); await p.waitForTimeout(600);
check('Google button hidden when provider is off', await p.isHidden('#googleBtn') && await p.isHidden('.divider'));
H.db.googleEnabled = true;
await p.reload(); await p.waitForTimeout(600);
check('Google button shown when provider is on', await p.isVisible('#googleBtn'));
await ctx.close();

// 7. Forgot + reset password (English)
ctx = await newCtx({ locale: 'en-US' }); p = await ctx.newPage(); watch(p, 'reset');
await p.goto(B + '/login.html');
await p.click('#forgotBtn');
check('forgot without email asks for email', /Enter your email/.test(await p.textContent('#authMsg')));
await p.fill('input[name=email]', 'olena@ua.test'); await p.click('#forgotBtn'); await p.waitForTimeout(400);
check('reset email requested', H.log.includes('RECOVER olena@ua.test') && /sent a link/.test(await p.textContent('#authMsg')));
await p.goto(B + '/reset.html'); await p.waitForTimeout(600);
check('reset page without session shows invalid link', /invalid or has expired/.test(await p.textContent('#resetMsg')) && await p.isHidden('#resetForm'));
await p.goto(B + '/login.html'); await p.fill('input[name=email]', 'olena@ua.test'); await p.fill('input[name=password]', 'password123'); await p.click('#authSubmit');
await p.waitForURL(/app\.html/, { timeout: 5000 }).catch(() => {});
await p.goto(B + '/reset.html'); await p.waitForTimeout(600);
await p.fill('input[name=password]', 'newpassword9'); await p.click('#resetSubmit');
await p.waitForURL(/app\.html/, { timeout: 5000 }).catch(() => {});
check('password updated and redirected', H.db.users[uid].password === 'newpassword9' && p.url().includes('app.html'));
await ctx.close();

// 8. API: refine validation + profile auth
let r = await fetch(B + '/api/profile', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{"brand":"x"}' });
check('profile API requires login', r.status === 401);
r = await fetch(B + '/api/generate', { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-forwarded-for': '7.7.7.7' }, body: JSON.stringify({ prompt: 'x', mode: 'hack', previous: 'y' }) });
await r.text(); req = H.anthropicRequests.at(-1);
check('unknown refine mode ignored', req.body.messages.length === 1);
r = await fetch(B + '/api/generate', { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-forwarded-for': '7.7.7.8' }, body: JSON.stringify({ prompt: '' }) });
check('error has code', (await r.json()).code === 'empty');

// mobile
ctx = await newCtx({ viewport: { width: 390, height: 844 }, locale: 'hi-IN' }); p = await ctx.newPage(); watch(p, 'mobile');
await p.goto(B + '/login.html'); await p.waitForTimeout(500);
check('Hindi login from browser language', /फिर से स्वागत/.test(await p.textContent('#authCard h1:not([hidden])')));
check('mobile login no overflow', !(await p.evaluate(() => document.documentElement.scrollWidth > innerWidth)));
await p.fill('input[name=email]', 'olena@ua.test'); await p.fill('input[name=password]', 'newpassword9'); await p.click('#authSubmit');
await p.waitForURL(/app\.html/, { timeout: 5000 }).catch(() => {}); await p.waitForTimeout(800);
check('mobile app no overflow', !(await p.evaluate(() => document.documentElement.scrollWidth > innerWidth)));
await p.screenshot({ path: H.ROOT + '/tests/.output/app-hi-m.png', fullPage: true });

console.log('page errors:', errs);
console.log(fails ? `${fails} FAILED` : 'ALL PASSED');
await browser.close(); H.server.close(); process.exit(0);
