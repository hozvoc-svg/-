// Vercel serverless function: POST /api/generate
// Body: { prompt, template?, tone?, language?, mode?: "again" | "shorter" | "longer", previous? }
// Signed-in users (Authorization: Bearer <Supabase token>) spend one credit per generation;
// their saved business profile is added to the task. Anonymous visitors get a few free tries
// (landing page demo and free tools).
// Streams Claude's reply back as plain text; remaining credits are sent in X-Credits-Remaining.
// Errors are JSON: { error, code } — the browser translates them by `code`.
import crypto from "node:crypto";
import Anthropic from "@anthropic-ai/sdk";
import {
  TEMPLATES, TONES, LANGUAGES, REFINE, MAX_PROMPT_CHARS,
  buildSystemPrompt, buildMessages, supabaseAdmin, getUser, clientIp,
} from "./_lib.js";

const client = new Anthropic();

const DEMO_LIMIT = 3; // free tries per visitor per hour (landing demo and free tools)
const DEMO_WINDOW_SECONDS = 60 * 60;
// Free tries for everyone together per day: caps what anonymous visitors can cost you.
// ~1–2 cents each, so 300/day ≈ $3–6/day at most. Override with the ANON_DAILY_LIMIT env variable.
const ANON_DAILY_LIMIT = Number(process.env.ANON_DAILY_LIMIT) || 300;
const hits = new Map(); // fallback when the database is not configured (per server instance only)

function memoryLimited(key, max, windowMs) {
  const now = Date.now();
  const entry = hits.get(key);
  if (!entry || now - entry.start > windowMs) {
    hits.set(key, { start: now, count: 1 });
    return false;
  }
  entry.count += 1;
  return entry.count > max;
}

// Returns "visitor" or "daily" when a free try is not allowed, otherwise null.
async function anonLimit(db, ip) {
  const salt = process.env.SUPABASE_SERVICE_ROLE_KEY || "muse";
  const visitor = "ip:" + crypto.createHash("sha256").update(salt + ip).digest("hex").slice(0, 32);
  const day = "day:" + new Date().toISOString().slice(0, 10);
  if (!db) {
    if (memoryLimited(visitor, DEMO_LIMIT, DEMO_WINDOW_SECONDS * 1000)) return "visitor";
    return memoryLimited(day, ANON_DAILY_LIMIT, 24 * 3600 * 1000) ? "daily" : null;
  }
  const { data: visitorOk, error } = await db.rpc("anon_hit", { k: visitor, max_count: DEMO_LIMIT, window_seconds: DEMO_WINDOW_SECONDS });
  if (error) {
    console.error("anon_hit failed:", error);
    return memoryLimited(visitor, DEMO_LIMIT, DEMO_WINDOW_SECONDS * 1000) ? "visitor" : null;
  }
  if (!visitorOk) return "visitor";
  const { data: dayOk } = await db.rpc("anon_hit", { k: day, max_count: ANON_DAILY_LIMIT, window_seconds: 24 * 3600 });
  if (Math.random() < 0.01) db.rpc("anon_cleanup").then(() => {}, () => {});
  return dayOk === false ? "daily" : null;
}

const fail = (res, status, code, error) => res.status(status).json({ error, code });

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const body = req.body || {};
  const prompt = typeof body.prompt === "string" ? body.prompt.trim() : "";
  const template = TEMPLATES[body.template] ? body.template : "ad";
  const tone = TONES.includes(body.tone) ? body.tone : "friendly";
  const language = LANGUAGES.includes(body.language) ? body.language : "English";
  const mode = REFINE[body.mode] ? body.mode : null;
  const previous = mode && typeof body.previous === "string" ? body.previous : "";

  if (!prompt) return fail(res, 400, "empty", "Please describe what you want to write.");
  if (prompt.length > MAX_PROMPT_CHARS) return fail(res, 400, "too_long", `Prompt is too long (max ${MAX_PROMPT_CHARS} characters).`);
  if (!process.env.ANTHROPIC_API_KEY) return fail(res, 500, "not_configured", "AI is not configured: set ANTHROPIC_API_KEY on the server.");

  const user = await getUser(req.headers.authorization);
  const db = supabaseAdmin();
  let remaining = null;
  let brand = "";

  if (user) {
    const { data, error } = await db.rpc("use_credit", { uid: user.id });
    if (error) {
      console.error("use_credit failed:", error);
      return fail(res, 500, "server", "Could not check your credits. Please try again.");
    }
    if (data < 0) return fail(res, 402, "no_credits", "You're out of credits. Upgrade your plan to keep creating.");
    remaining = data;
    const { data: profile } = await db.from("profiles").select("brand").eq("id", user.id).maybeSingle();
    brand = profile?.brand || "";
  } else {
    if (req.headers.authorization) return fail(res, 401, "auth", "Your session has expired. Please log in again.");
    if (mode) return fail(res, 401, "auth", "Log in to refine a result.");
    const limited = await anonLimit(db, clientIp(req.headers));
    if (limited) {
      return fail(res, 429, "demo_limit", "Free demo limit reached. Create a free account to get 10 generations a month.");
    }
  }

  const refund = async () => {
    if (!user) return;
    const { error } = await db.rpc("refund_credit", { uid: user.id });
    if (error) console.error("refund failed:", error);
  };
  const headers = { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" };
  if (remaining !== null) headers["X-Credits-Remaining"] = String(remaining);

  let output = "";
  try {
    const stream = client.beta.messages.stream({
      model: "claude-opus-5-5",
      max_tokens: 2048, // marketing copy is short; keeps cost per generation predictable
      output_config: { effort: "low" },
      system: buildSystemPrompt({ template, tone, language }),
      messages: buildMessages({ prompt, brand, mode, previous }),
      // If a request is declined, the API retries it on a fallback model automatically.
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
    });

    // Send headers only once text arrives, so early API errors can still return JSON.
    for await (const event of stream) {
      if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
        if (!res.headersSent) res.writeHead(200, headers);
        res.write(event.delta.text);
        output += event.delta.text;
      }
    }

    const message = await stream.finalMessage();
    if (message.stop_reason === "refusal" || !output) {
      await refund();
      if (res.headersSent) return res.end("\n\n[…]"); // declined mid-answer: credit refunded, nothing saved
      return fail(res, 422, "refused", "Muse can't help with that request. Try a different prompt. No credit was used.");
    }
    res.end();

    if (user) {
      const { error } = await db.from("generations").insert({ user_id: user.id, template, prompt, output });
      if (error) console.error("saving generation failed:", error);
    }
  } catch (error) {
    console.error("generate failed:", error);
    if (!output) await refund();
    if (res.headersSent) return res.end("\n\n[…]");
    if (error instanceof Anthropic.RateLimitError) return fail(res, 429, "busy", "Muse is busy right now. Try again in a moment.");
    if (error instanceof Anthropic.AuthenticationError) return fail(res, 500, "not_configured", "The server's ANTHROPIC_API_KEY is invalid.");
    if (error instanceof Anthropic.APIError) return fail(res, 502, "server", "The AI service returned an error. Please try again.");
    return fail(res, 500, "server", "Something went wrong. Please try again.");
  }
}
