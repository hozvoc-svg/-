// Vercel serverless function: POST /api/generate
// Body: { prompt, template?, tone?, language? }
// Signed-in users (Authorization: Bearer <Supabase token>) spend one credit per generation.
// Anonymous visitors get a few free tries on the landing page demo.
// Streams Claude's reply back as plain text; remaining credits are sent in X-Credits-Remaining.
import Anthropic from "@anthropic-ai/sdk";
import { TEMPLATES, TONES, LANGUAGES, buildSystemPrompt, supabaseAdmin, getUser, clientIp } from "./_lib.js";

const client = new Anthropic();

const MAX_PROMPT_CHARS = 1000;
const DEMO_LIMIT = 3; // anonymous generations per IP per window
const DEMO_WINDOW_MS = 60 * 60 * 1000;
const hits = new Map(); // best-effort, per warm instance

function demoLimited(ip) {
  const now = Date.now();
  const entry = hits.get(ip);
  if (!entry || now - entry.start > DEMO_WINDOW_MS) {
    hits.set(ip, { start: now, count: 1 });
    return false;
  }
  entry.count += 1;
  return entry.count > DEMO_LIMIT;
}

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

  if (!prompt) return res.status(400).json({ error: "Please describe what you want to write." });
  if (prompt.length > MAX_PROMPT_CHARS) {
    return res.status(400).json({ error: `Prompt is too long (max ${MAX_PROMPT_CHARS} characters).` });
  }
  if (!process.env.ANTHROPIC_API_KEY) {
    return res.status(500).json({ error: "AI is not configured: set ANTHROPIC_API_KEY on the server." });
  }

  const user = await getUser(req.headers.authorization);
  const db = supabaseAdmin();
  let remaining = null;

  if (user) {
    const { data, error } = await db.rpc("use_credit", { uid: user.id });
    if (error) {
      console.error("use_credit failed:", error);
      return res.status(500).json({ error: "Could not check your credits. Please try again." });
    }
    if (data < 0) {
      return res.status(402).json({ error: "You're out of credits. Upgrade your plan to keep creating.", code: "no_credits" });
    }
    remaining = data;
  } else {
    if (req.headers.authorization) {
      return res.status(401).json({ error: "Your session has expired. Please log in again.", code: "auth" });
    }
    if (demoLimited(clientIp(req.headers))) {
      return res.status(429).json({ error: "Free demo limit reached. Create a free account to get 10 generations a month.", code: "demo_limit" });
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
      messages: [{ role: "user", content: prompt }],
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
    if (!res.headersSent) res.writeHead(200, headers);

    const message = await stream.finalMessage();
    if (message.stop_reason === "refusal" || !output) {
      await refund();
      res.write("\n\nSorry, Muse can't help with that request. Try a different prompt. (No credit was used.)");
      return res.end();
    }
    res.end();

    if (user) {
      const { error } = await db.from("generations").insert({ user_id: user.id, template, prompt, output });
      if (error) console.error("saving generation failed:", error);
    }
  } catch (error) {
    console.error("generate failed:", error);
    if (!output) await refund();
    if (res.headersSent) return res.end("\n\n[Generation interrupted. Please try again.]");
    if (error instanceof Anthropic.RateLimitError) {
      return res.status(429).json({ error: "Muse is busy right now. Try again in a moment." });
    }
    if (error instanceof Anthropic.AuthenticationError) {
      return res.status(500).json({ error: "The server's ANTHROPIC_API_KEY is invalid." });
    }
    if (error instanceof Anthropic.APIError) {
      return res.status(502).json({ error: "The AI service returned an error. Please try again." });
    }
    return res.status(500).json({ error: "Something went wrong. Please try again." });
  }
}
