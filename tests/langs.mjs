import { createRequire } from 'node:module';
import fs from 'node:fs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const H = await import('./server.mjs'); await H.start();
const b = await chromium.launch(); const errs = []; let fails = 0;
const pages = { 'index.html': ['en', null], 'zh.html': ['zh', 'Chinese'], 'hi.html': ['hi', 'Hindi'], 'es.html': ['es', 'Spanish'], 'fr.html': ['fr', 'French'], 'ar.html': ['ar', 'Arabic'], 'uk.html': ['uk', 'Ukrainian'] };
for (const [file, [code, language]] of Object.entries(pages)) {
  for (const w of [1440, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.setExtraHTTPHeaders({ 'x-forwarded-for': '10.0.' + Math.floor(Math.random() * 250) + '.' + w % 250 });
    await p.route('https://fonts.googleapis.com/**', (r) => r.fulfill({ status: 200, contentType: 'text/css', body: '' }));
    p.on('pageerror', e => errs.push(file + ': ' + e.message));
    p.on('console', m => m.type() === 'error' && !/Failed to load/.test(m.text()) && errs.push(file + ': ' + m.text()));
    await p.goto(H.BASE + '/' + file);
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo({ top: y, behavior: 'instant' }); await new Promise(r => setTimeout(r, 30)); } window.scrollTo({ top: 0, behavior: 'instant' }); });
    await p.waitForTimeout(2200);
    const overflow = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    const typing = await p.textContent('#typing');
    if (overflow) { fails++; console.log('FAIL overflow', file, w); }
    if (w === 1440) {
      // hero text is in the page language
      const enHero = 'Cold brew coffee for busy students';
      const okHero = code === 'en' ? typing.startsWith('Cold') : !typing.includes(enHero.slice(0, 8)) && typing.length > 0;
      // language switcher has all 7 links that exist
      const links = await p.$$eval('.langs__menu a', as => as.map(a => a.getAttribute('href')));
      const okLinks = links.length === 7 && links.every(l => fs.existsSync(H.ROOT + '/' + l));
      // demo canned + live language
      await p.goto(H.BASE + '/' + file + '#demo'); await p.waitForTimeout(1200);
      const canned = await p.textContent('#demoOutput');
      await p.click('[data-demo="custom"]'); await p.fill('#demoInput', 'test ' + code); await p.keyboard.press('Enter');
      await p.waitForTimeout(1500);
      const req = H.anthropicRequests.at(-1);
      const sentLang = req && req.body.messages[0].content === 'test ' + code ? (req.body.system.match(/Write in (\w+)/) || [])[1] : 'NO REQUEST';
      const okLang = sentLang === (language || 'English');
      console.log(`${okHero && okLinks && okLang ? 'PASS' : 'FAIL'} ${file}: hero="${typing.slice(0, 28)}" canned="${canned.slice(0, 24).replace(/\n/g, ' ')}" demoLang=${sentLang} langLinks=${links.length}`);
      if (!(okHero && okLinks && okLang)) fails++;
      await p.goto(H.BASE + '/' + file); await p.waitForTimeout(1500);
      await p.screenshot({ path: `${H.ROOT}/tests/.output/lang-${code}.png` });
    } else {
      await p.screenshot({ path: `${H.ROOT}/tests/.output/lang-${code}-m.png` });
    }
    await p.close();
  }
}
// rate limiter: the demo allows 3/hour per IP; harness IP is the same for all -> later requests may be 429.
console.log('errors:', errs); console.log(fails ? fails + ' FAILED' : 'ALL PASSED');
await b.close(); H.server.close(); process.exit(0);
