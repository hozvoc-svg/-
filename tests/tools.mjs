import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const H = await import('./server.mjs'); await H.start();
let fails = 0; const errs = [];
const check = (n, c, x = '') => { console.log((c ? 'PASS ' : 'FAIL ') + n + (x ? '  ' + x : '')); if (!c) fails++; };
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
await ctx.route('https://fonts.googleapis.com/**', (r) => r.fulfill({ status: 200, contentType: 'text/css', body: '' }));
const p = await ctx.newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.goto(H.BASE + '/hashtag-generator.html');
await p.fill('[name=topic]', 'Pumpkin latte at our cafe'); await p.selectOption('[name=platform]', 'TikTok'); await p.fill('[name=place]', 'Lisbon');
await p.click('button[type=submit]');
await p.waitForFunction(() => document.querySelector('[data-tool-status]').textContent.includes('done'), null, { timeout: 8000 }).catch(() => {});
let req = H.anthropicRequests.at(-1);
check('hashtag tool: template + prompt', /30 relevant hashtags/.test(req.body.system) && req.body.messages[0].content === 'Hashtags for a TikTok post. Post or business: Pumpkin latte at our cafe. Location (if any): Lisbon.', req.body.messages[0].content);
check('hashtag output shown + copy button', (await p.textContent('[data-tool-output]')).includes('Mock copy') && await p.isVisible('[data-tool-copy]'));
await p.screenshot({ path: H.ROOT + '/tests/.output/tool-hashtags.png', fullPage: true });
await p.goto(H.BASE + '/business-name-generator.html');
await p.fill('[name=topic]', 'Soy candles'); await p.selectOption('[name=language]', 'Spanish'); await p.click('button[type=submit]');
await p.waitForFunction(() => document.querySelector('[data-tool-status]').textContent.includes('done'), null, { timeout: 8000 }).catch(() => {});
req = H.anthropicRequests.at(-1);
check('name tool: template + language', /brand or business name ideas/.test(req.body.system) && /Spanish/.test(req.body.system));
await p.click('button[type=submit]'); await p.waitForTimeout(700);
await p.click('button[type=submit]'); await p.waitForTimeout(700);
check('demo limit message after 3 tries', /free tries/.test(await p.textContent('[data-tool-output]')), await p.textContent('[data-tool-output]'));
await p.goto(H.BASE + '/character-counter.html');
await p.fill('#counterInput', 'Hello world 👋 #coffee #latte\nsecond line');
check('counter stats', (await p.textContent('#statChars')) === '40' && (await p.textContent('#statWords')) === '7' && (await p.textContent('#statLines')) === '2' && (await p.textContent('#statHashtags')) === '2',
  [await p.textContent('#statChars'), await p.textContent('#statWords'), await p.textContent('#statLines'), await p.textContent('#statHashtags')].join(','));
await p.fill('#counterInput', 'x'.repeat(300));
check('X limit shows over', await p.evaluate(() => document.querySelector('[data-limit="280"]').classList.contains('is-over')) && /20 over/.test(await p.textContent('[data-limit="280"] .limit__left')));
await p.screenshot({ path: H.ROOT + '/tests/.output/tool-counter.png', fullPage: true });
for (const f of ['tools.html', 'hashtag-generator.html', 'character-counter.html', 'business-name-generator.html']) {
  const m = await ctx.newPage(); await m.setViewportSize({ width: 390, height: 844 }); await m.goto(H.BASE + '/' + f); await m.waitForTimeout(400);
  check('mobile no overflow ' + f, !(await m.evaluate(() => document.documentElement.scrollWidth > innerWidth))); await m.close();
}
console.log('errors:', errs); console.log(fails ? fails + ' FAILED' : 'ALL PASSED');
await b.close(); H.server.close(); process.exit(0);
