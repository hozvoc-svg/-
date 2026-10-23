// Runs every test file against a local mock of Supabase, Claude and Lemon Squeezy (tests/server.mjs).
// No real accounts or API keys are used. Needs Playwright with Chromium installed (globally is fine).
// Usage: npm test            (all)        node tests/run.mjs features   (one file)
import { execSync, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const dir = fileURLToPath(new URL('.', import.meta.url));
fs.mkdirSync(dir + '.output', { recursive: true });
let nodePath = process.env.NODE_PATH;
if (!nodePath) { try { nodePath = execSync('npm root -g').toString().trim(); } catch (e) { nodePath = ''; } }

const only = process.argv.slice(2);
const files = ['limits', 'test', 'features', 'tools', 'langs'].filter((f) => !only.length || only.includes(f));
let failed = 0;
for (const f of files) {
  console.log(`\n=== ${f}`);
  const r = spawnSync(process.execPath, [dir + f + '.mjs'], { env: { ...process.env, NODE_PATH: nodePath }, encoding: 'utf8', timeout: 300000 });
  const lines = (r.stdout || '').split('\n').filter((l) => /^(PASS|FAIL|ALL PASSED|\d+ FAILED|page errors|browser errors|errors)/.test(l));
  console.log(lines.join('\n'));
  if (r.status !== 0 || !/ALL PASSED/.test(r.stdout || '')) {
    failed++;
    if (r.stderr && !/ALL PASSED/.test(r.stdout || '')) console.log(r.stderr.split('\n').filter((l) => !/^\s+at /.test(l)).slice(-15).join('\n'));
  }
}
console.log(failed ? `\n${failed} test file(s) FAILED` : '\nAll test files passed');
process.exit(failed ? 1 : 0);
