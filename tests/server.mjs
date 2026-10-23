import { fileURLToPath } from 'node:url';
// Local harness: static site + real /api handlers + mock Supabase (/sb) + mock Anthropic (/anthropic).
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { Readable } from 'node:stream';

const ROOT = fileURLToPath(new URL('..', import.meta.url)).replace(/\/$/, '');
const PORT = 8790;
const BASE = `http://localhost:${PORT}`;
Object.assign(process.env, {
  ANTHROPIC_API_KEY: 'test-key', ANTHROPIC_BASE_URL: `${BASE}/anthropic`,
  SUPABASE_URL: `${BASE}/sb`, SUPABASE_SERVICE_ROLE_KEY: 'service-key', SUPABASE_ANON_KEY: 'anon-key',
  LEMONSQUEEZY_WEBHOOK_SECRET: 'whsec', LEMONSQUEEZY_VARIANT_CREATOR: '111', LEMONSQUEEZY_VARIANT_PRO: '222',
  LEMONSQUEEZY_CHECKOUT_CREATOR: 'https://muse.lemonsqueezy.com/buy/creator-uuid', LEMONSQUEEZY_CHECKOUT_PRO: 'https://muse.lemonsqueezy.com/buy/pro-uuid',
});
export const log = [];
export const db = { users: {}, tokens: {}, profiles: {}, generations: [] };
export const anthropicRequests = [];

const generate = (await import(ROOT + '/api/generate.js')).default;
const webhook = await import(ROOT + '/api/webhook.js');
const config = await import(ROOT + '/api/config.js');
const profileApi = (await import(ROOT + '/api/profile.js')).default;

const types = { '.html':'text/html', '.css':'text/css', '.js':'text/javascript', '.svg':'image/svg+xml', '.png':'image/png', '.webmanifest':'application/manifest+json' };
const readBody = (req) => new Promise((r) => { let b=''; req.on('data', c => b += c); req.on('end', () => r(b)); });
const send = (res, code, obj, headers = {}) => { res.writeHead(code, { 'Content-Type': 'application/json', ...headers }); res.end(obj === undefined ? '' : JSON.stringify(obj)); };

function sbUserFromAuth(req) { const t = (req.headers.authorization || '').replace('Bearer ', ''); return db.tokens[t]; }
function session(user) {
  const token = 'tok_' + crypto.randomUUID(); db.tokens[token] = user.id;
  return { access_token: token, token_type: 'bearer', expires_in: 3600, expires_at: Math.floor(Date.now()/1000)+3600, refresh_token: 'r_' + token, user };
}
function filterRows(rows, params) {
  for (const [k, v] of params) { if (['select','order','limit'].includes(k)) continue; const [, val] = v.split('.'); rows = rows.filter(r => String(r[k]) === val); }
  return rows;
}

async function mockSupabase(req, res, url) {
  const p = url.pathname.replace('/sb', '');
  const body = ['POST','PATCH','PUT'].includes(req.method) ? JSON.parse((await readBody(req)) || '{}') : null;
  log.push(`SB ${req.method} ${p}${url.search}`);
  if (p === '/auth/v1/signup') {
    const id = crypto.randomUUID(); const user = { id, email: body.email, user_metadata: body.data || {}, aud: 'authenticated', role: 'authenticated' };
    db.users[id] = { ...user, password: body.password };
    db.profiles[id] = { id, email: body.email, full_name: body.data?.full_name ?? null, plan: 'free', credits: 10, credits_reset_at: new Date().toISOString(), subscription_id: null, subscription_status: null, customer_portal_url: null, brand: null };
    return send(res, 200, session(user));
  }
  if (p === '/auth/v1/token') {
    const u = Object.values(db.users).find(u => u.email === body.email && u.password === body.password);
    if (!u) return send(res, 400, { error: 'invalid_grant', error_description: 'Invalid login credentials', msg: 'Invalid login credentials', code: 'invalid_credentials' });
    const { password, ...user } = u; return send(res, 200, session(user));
  }
  if (p === '/auth/v1/user' && req.method === 'GET') {
    const id = sbUserFromAuth(req); if (!id) return send(res, 401, { msg: 'invalid JWT', code: 'bad_jwt' });
    const { password, ...user } = db.users[id]; return send(res, 200, user);
  }
  if (p === '/auth/v1/logout') return send(res, 204);
  if (p === '/auth/v1/recover') { log.push('RECOVER ' + body.email); return send(res, 200, {}); }
  if (p === '/auth/v1/user' && req.method === 'PUT') {
    const id = sbUserFromAuth(req); if (!id) return send(res, 401, { msg: 'invalid JWT' });
    if (body.password) db.users[id].password = body.password;
    const { password, ...user } = db.users[id]; return send(res, 200, user);
  }
  if (p.startsWith('/rest/v1/rpc/')) {
    if (req.headers.authorization !== 'Bearer service-key') return send(res, 403, { message: 'permission denied' });
    const fn = p.split('/').pop(); const prof = db.profiles[body?.uid];
    if (fn === 'use_credit') { if (!prof || prof.credits <= 0) return send(res, 200, -1); prof.credits -= 1; return send(res, 200, prof.credits); }
    if (fn === 'refund_credit') { prof.credits += 1; return send(res, 200, null); }
    if (fn === 'anon_hit') {
      db.anon ??= {}; const e = db.anon[body.k] ||= { count: 0 }; e.count += 1;
      return send(res, 200, e.count <= body.max_count);
    }
    if (fn === 'anon_cleanup') return send(res, 200, null);
  }
  const table = p.replace('/rest/v1/', '');
  const isService = req.headers.authorization === 'Bearer service-key';
  const uid = isService ? null : sbUserFromAuth(req);
  const wantsObject = (req.headers.accept || '').includes('vnd.pgrst.object');
  if (req.method === 'GET') {
    let rows = table === 'profiles' ? Object.values(db.profiles) : db.generations;
    if (!isService) rows = rows.filter(r => (r.user_id ?? r.id) === uid); // RLS
    rows = filterRows(rows, url.searchParams);
    if (table === 'generations') rows = [...rows].sort((a,b) => b.id - a.id).slice(0, Number(url.searchParams.get('limit') || 1000));
    if (wantsObject) return rows.length ? send(res, 200, rows[0]) : send(res, 406, { code: 'PGRST116', message: 'no rows' });
    return send(res, 200, rows);
  }
  if (req.method === 'POST' && table === 'generations') {
    if (!isService) return send(res, 403, { message: 'RLS' });
    const row = { id: db.generations.length + 1, created_at: new Date().toISOString(), ...body }; db.generations.push(row); return send(res, 201);
  }
  if (req.method === 'PATCH' && table === 'profiles') {
    if (!isService) return send(res, 403, { message: 'RLS' });
    filterRows(Object.values(db.profiles), url.searchParams).forEach(r => Object.assign(r, body)); return send(res, 204);
  }
  send(res, 404, { message: 'mock: unhandled ' + req.method + ' ' + p });
}

async function mockAnthropic(req, res) {
  const body = JSON.parse(await readBody(req));
  anthropicRequests.push({ headers: req.headers, body });
  const text = body.messages[0].content.includes('FAIL') ? null : `Mock copy for: ${body.messages[0].content}`;
  if (!text) return send(res, 529, { type: 'error', error: { type: 'overloaded_error', message: 'Overloaded' } });
  res.writeHead(200, { 'Content-Type': 'text/event-stream' });
  const ev = (type, data) => res.write(`event: ${type}\ndata: ${JSON.stringify({ type, ...data })}\n\n`);
  ev('message_start', { message: { id: 'msg_1', type: 'message', role: 'assistant', model: body.model, content: [], stop_reason: null, stop_sequence: null, usage: { input_tokens: 10, output_tokens: 0 } } });
  ev('content_block_start', { index: 0, content_block: { type: 'text', text: '' } });
  for (const w of text.match(/.{1,8}/g)) { ev('content_block_delta', { index: 0, delta: { type: 'text_delta', text: w } }); await new Promise(r => setTimeout(r, 5)); }
  ev('content_block_stop', { index: 0 });
  ev('message_delta', { delta: { stop_reason: 'end_turn', stop_sequence: null }, usage: { output_tokens: 20 } });
  ev('message_stop', {});
  res.end();
}

function vercelRes(res) { res.status = (c) => { res.statusCode = c; return res; }; res.json = (o) => { if (!res.headersSent) res.setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(o)); }; return res; }
async function webHandler(fn, req, res) {
  const body = req.method === 'GET' ? undefined : await readBody(req);
  const request = new Request(BASE + req.url, { method: req.method, headers: req.headers, body });
  const response = await fn(request);
  res.writeHead(response.status, Object.fromEntries(response.headers)); res.end(await response.text());
}

export const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, BASE);
  try {
    if (url.pathname.startsWith('/sb/')) return mockSupabase(req, res, url);
    if (url.pathname.startsWith('/anthropic/')) return mockAnthropic(req, res);
    if (url.pathname === '/api/generate') { const raw = await readBody(req); req.body = raw ? JSON.parse(raw) : undefined; return generate(req, vercelRes(res)); }
    if (url.pathname === '/api/profile') { const raw = await readBody(req); req.body = raw ? JSON.parse(raw) : undefined; return profileApi(req, vercelRes(res)); }
    if (url.pathname === '/api/webhook') return webHandler(webhook[req.method], req, res);
    if (url.pathname === '/api/config') return webHandler(config.GET, req, res);
    if (url.pathname === '/cdn/supabase.js') { res.writeHead(200, { 'Content-Type': 'text/javascript' }); return res.end(fs.readFileSync(ROOT + '/node_modules/@supabase/supabase-js/dist/umd/supabase.js')); }
    const f = path.join(ROOT, url.pathname === '/' ? 'index.html' : url.pathname);
    if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('nf'); }
    res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); res.end(fs.readFileSync(f));
  } catch (e) { console.error('SERVER ERROR', e); if (!res.headersSent) send(res, 500, { error: String(e) }); else res.end(); }
});
export const start = () => new Promise(r => server.listen(PORT, r));
export { BASE, PORT, ROOT };
