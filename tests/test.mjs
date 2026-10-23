import crypto from 'node:crypto';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const H = await import('./server.mjs');
await H.start();
const B = H.BASE;
let fails = 0;
const check = (name, cond, extra='') => { console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? '  ' + extra : '')); if (!cond) fails++; };
const gen = (body, token, ip='9.9.9.9') => fetch(B + '/api/generate', { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-forwarded-for': ip, ...(token ? { Authorization: 'Bearer ' + token } : {}) }, body: JSON.stringify(body) });
const sign = (obj) => { const raw = JSON.stringify(obj); return { raw, sig: crypto.createHmac('sha256', 'whsec').update(raw).digest('hex') }; };
const hook = (obj, sigOverride) => { const { raw, sig } = sign(obj); return fetch(B + '/api/webhook', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Signature': sigOverride ?? sig }, body: raw }); };

// ---- API: anonymous demo ----
let r = await gen({ prompt: 'Slogan for a bakery' });
check('anon generate 200', r.status === 200, await r.text());
await gen({ prompt: 'a' }); await gen({ prompt: 'b' });
r = await gen({ prompt: 'c' });
check('anon 4th request rate-limited 429', r.status === 429, JSON.stringify(await r.json()));
r = await gen({ prompt: '' }, null, '1.1.1.1'); check('empty prompt 400', r.status === 400);
r = await gen({ prompt: 'x' }, 'bogus-token', '1.1.1.2'); check('bad token 401', r.status === 401);

// ---- API: signed-in user ----
const su = await (await fetch(B + '/sb/auth/v1/signup', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: 'api@test.com', password: 'password1', data: { full_name: 'Api User' } }) })).json();
const uid = su.user.id, tok = su.access_token;
r = await gen({ prompt: 'Ad for running shoes', template: 'product', tone: 'bold', language: 'Ukrainian' }, tok);
const txt = await r.text();
check('user generate 200 + credits header 9', r.status === 200 && r.headers.get('x-credits-remaining') === '9', txt);
await new Promise(r => setTimeout(r, 200));
check('credit spent in DB', H.db.profiles[uid].credits === 9);
check('generation saved', H.db.generations.some(g => g.user_id === uid && g.template === 'product' && g.output.startsWith('Mock copy')));
const last = H.anthropicRequests.at(-1);
check('model claude-opus-5-5', last.body.model === 'claude-opus-5-5');
check('fallbacks default + beta header', last.body.fallbacks === 'default' && (last.headers['anthropic-beta'] || '').includes('server-side-fallback-2026-07-01'), last.headers['anthropic-beta']);
check('effort low, no temperature', last.body.output_config?.effort === 'low' && !('temperature' in last.body));
check('system prompt has template/tone/language', /product description/.test(last.body.system) && /bold/.test(last.body.system) && /Ukrainian/.test(last.body.system));
r = await gen({ prompt: 'x', template: 'evil', tone: 'ignore previous', language: 'Klingon; do X' }, tok);
await r.text();
const sys2 = H.anthropicRequests.at(-1).body.system;
check('unknown template/tone/language fall back to defaults', /social media ad/.test(sys2) && /friendly/.test(sys2) && /English/.test(sys2) && !/Klingon/.test(sys2));
const before = H.db.profiles[uid].credits;
r = await gen({ prompt: 'FAIL please' }, tok);
check('API failure -> 5xx', r.status >= 500, String(r.status));
await new Promise(r => setTimeout(r, 100));
check('credit refunded after failure', H.db.profiles[uid].credits === before, `${before} -> ${H.db.profiles[uid].credits}`);
H.db.profiles[uid].credits = 0;
r = await gen({ prompt: 'x' }, tok); const j = await r.json();
check('no credits -> 402 no_credits', r.status === 402 && j.code === 'no_credits');

// ---- API: config ----
const cfg = await (await fetch(B + '/api/config')).json();
check('config exposes only public values', cfg.supabaseAnonKey === 'anon-key' && !JSON.stringify(cfg).includes('service-key') && !JSON.stringify(cfg).includes('whsec'));

// ---- API: webhook ----
r = await hook({ meta: { event_name: 'subscription_created', custom_data: { user_id: uid } }, data: { id: '555', attributes: {} } }, 'deadbeef');
check('webhook bad signature 401', r.status === 401);
r = await hook({ meta: { event_name: 'subscription_created', custom_data: { user_id: uid } }, data: { id: '555', attributes: { status: 'active', variant_id: 111, urls: { customer_portal: 'https://portal.example/x' } } } });
check('subscription_created 200', r.status === 200, await r.text());
check('plan creator + 300 credits + portal', H.db.profiles[uid].plan === 'creator' && H.db.profiles[uid].credits === 300 && H.db.profiles[uid].customer_portal_url === 'https://portal.example/x', JSON.stringify(H.db.profiles[uid]));
H.db.profiles[uid].credits = 12;
r = await hook({ meta: { event_name: 'subscription_payment_success' }, data: { id: 'inv1', attributes: { subscription_id: 555 } } });
check('payment_success refills to 300', r.status === 200 && H.db.profiles[uid].credits === 300);
r = await hook({ meta: { event_name: 'subscription_updated' }, data: { id: '555', attributes: { status: 'active', variant_id: 222 } } });
check('upgrade to pro via update (lookup by subscription id)', H.db.profiles[uid].plan === 'pro' && H.db.profiles[uid].credits === 1000);
r = await hook({ meta: { event_name: 'subscription_cancelled' }, data: { id: '555', attributes: { status: 'cancelled', variant_id: 222 } } });
check('cancelled keeps pro until period end', H.db.profiles[uid].plan === 'pro');
r = await hook({ meta: { event_name: 'subscription_expired' }, data: { id: '555', attributes: { status: 'expired', variant_id: 222 } } });
check('expired -> free, credits capped at 10', H.db.profiles[uid].plan === 'free' && H.db.profiles[uid].credits === 10);
r = await hook({ meta: { event_name: 'order_created' }, data: { id: '1', attributes: {} } });
check('unrelated event ignored 200', r.status === 200);

// ---- Browser flow ----
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
await ctx.route('https://cdn.jsdelivr.net/**', (route) => route.fulfill({ status: 200, contentType: 'text/javascript', body: require('fs').readFileSync(H.ROOT + '/node_modules/@supabase/supabase-js/dist/umd/supabase.js', 'utf8') }));
let checkoutHit = null;
await ctx.route('https://muse.lemonsqueezy.com/**', (route) => { checkoutHit = route.request().url(); route.fulfill({ status: 200, contentType: 'text/html', body: '<h1>Checkout</h1>' }); });
const errs = [];
const page = await ctx.newPage();
page.on('pageerror', (e) => errs.push(e.message));
page.on('console', (m) => m.type() === 'error' && errs.push(m.text()));

await page.goto(B + '/login.html?mode=signup&plan=creator');
await page.fill('input[name=name]', 'Olena');
await page.fill('input[name=email]', 'olena@test.com');
await page.fill('input[name=password]', 'short');
await page.click('#authSubmit');
check('short password rejected', /at least 8/.test(await page.textContent('#authMsg')));
await page.fill('input[name=password]', 'longpassword');
await page.click('#authSubmit');
await page.waitForURL(/lemonsqueezy/, { timeout: 8000 }).catch(() => {});
const ck = checkoutHit ? new URL(checkoutHit) : null;
check('signup with plan -> checkout with user_id & email', ck && ck.pathname.endsWith('creator-uuid') && ck.searchParams.get('checkout[email]') === 'olena@test.com' && !!ck.searchParams.get('checkout[custom][user_id]'), checkoutHit);

await page.goto(B + '/app.html');
await page.waitForFunction(() => document.querySelector('#creditsCount').textContent !== '–');
check('app shows name & 10 credits', (await page.textContent('#creditsCount')) === '10' && (await page.textContent('#userName')) === 'Olena');
await page.click('[data-template="email"]');
await page.fill('#prompt', 'Winter sale 20% off');
await page.selectOption('#language', 'Ukrainian');
await page.click('#genBtn');
await page.waitForFunction(() => document.querySelector('#genStatus').textContent.includes('done'), null, { timeout: 8000 });
check('app output streamed', (await page.textContent('#output')).includes('Mock copy for: Winter sale'));
check('credits decreased to 9', (await page.textContent('#creditsCount')) === '9');
await page.waitForFunction(() => document.querySelectorAll('#history button').length === 1, null, { timeout: 5000 }).catch(() => {});
check('history shows item', (await page.locator('#history button').count()) === 1);
await page.screenshot({ path: H.ROOT + '/tests/.output/app-desktop.png' });
await page.click('#upgradeBtn');
check('upgrade modal opens', await page.isVisible('#upgradeModal'));
await page.screenshot({ path: H.ROOT + '/tests/.output/app-upgrade.png' });
await page.click('[data-plan="pro"]');
await page.waitForURL(/lemonsqueezy/, { timeout: 5000 }).catch(() => {});
check('pro checkout link', checkoutHit && checkoutHit.includes('pro-uuid'));

// out of credits -> modal
const oid = Object.values(H.db.users).find(u => u.email === 'olena@test.com').id;
H.db.profiles[oid].credits = 0;
await page.goto(B + '/app.html');
await page.waitForFunction(() => document.querySelector('#creditsCount').textContent === '0');
await page.fill('#prompt', 'anything'); await page.click('#genBtn');
await page.waitForSelector('#upgradeModal[open]', { timeout: 5000 }).catch(() => {});
check('no credits opens upgrade modal', await page.isVisible('#upgradeModal'));
await page.keyboard.press('Escape');

// logout -> app redirects to login
await page.click('.account summary'); await page.click('#signOutBtn');
await page.waitForURL(/index\.html/, { timeout: 5000 }).catch(() => {});
await page.goto(B + '/app.html');
await page.waitForURL(/login\.html/, { timeout: 5000 }).catch(() => {});
check('logged-out app redirects to login', page.url().includes('login.html'));
// log back in
await page.fill('input[name=email]', 'olena@test.com'); await page.fill('input[name=password]', 'wrongpass1'); await page.click('#authSubmit');
await page.waitForFunction(() => document.querySelector('#authMsg').textContent.length > 0);
check('wrong password shows error', /wrong email/i.test(await page.textContent('#authMsg')), await page.textContent('#authMsg'));
await page.fill('input[name=password]', 'longpassword'); await page.click('#authSubmit');
await page.waitForURL(/app\.html/, { timeout: 5000 }).catch(() => {});
check('login -> app', page.url().includes('app.html'));

// landing page + live demo (anonymous)
const p2 = await ctx.newPage(); p2.on('pageerror', (e) => errs.push(e.message));
await p2.goto(B + '/index.html#demo'); await p2.waitForTimeout(400);
await p2.click('[data-demo="custom"]'); await p2.fill('#demoInput', 'Tagline for a gym'); await p2.keyboard.press('Enter');
await p2.waitForFunction(() => document.querySelector('#demoStatus').textContent !== 'writing…', null, { timeout: 8000 });
check('landing demo works (or shows limit msg)', /Mock copy|limit/i.test(await p2.textContent('#demoOutput')), await p2.textContent('#demoOutput'));

// mobile app
const m = await browser.newPage({ viewport: { width: 390, height: 844 } });
await m.context().route('https://cdn.jsdelivr.net/**', (route) => route.fulfill({ status: 200, contentType: 'text/javascript', body: require('fs').readFileSync(H.ROOT + '/node_modules/@supabase/supabase-js/dist/umd/supabase.js', 'utf8') }));
await m.goto(B + '/login.html');
await m.fill('input[name=email]', 'olena@test.com'); await m.fill('input[name=password]', 'longpassword'); await m.click('#authSubmit');
await m.waitForURL(/app\.html/, { timeout: 5000 }).catch(() => {});
await m.waitForTimeout(800);
check('mobile app no horizontal overflow', !(await m.evaluate(() => document.documentElement.scrollWidth > innerWidth)));
await m.screenshot({ path: H.ROOT + '/tests/.output/app-mobile.png', fullPage: true });

console.log('browser errors:', errs.filter(e => !/Failed to load resource/.test(e)));
console.log(fails ? `\n${fails} FAILED` : '\nALL PASSED');
await browser.close(); H.server.close(); process.exit(0);
