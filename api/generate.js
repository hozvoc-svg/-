// Vercel serverless function: POST /api/generate  { prompt: string }
// Streams Claude's reply back as plain text. The API key stays on the server
// (set ANTHROPIC_API_KEY in your Vercel project settings).
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const MAX_PROMPT_CHARS = 600;
const RATE_LIMIT = 8; // requests per IP per window
const RATE_WINDOW_MS = 60 * 60 * 1000;
const hits = new Map(); // best-effort, per warm instance

const SYSTEM_PROMPT = `You are Muse, an AI copywriter shown in a live demo on a marketing website.
Write the piece of content the user asks for: ads, product descriptions, emails, social posts, slogans, short blog intros.
Keep it under 150 words, punchy and ready to publish. Plain text only, no Markdown headings; short paragraphs and simple bullet points with "•" are fine.
If the request is not a content-writing task, briefly say you are a content-writing demo and suggest a writing prompt instead.`;

function rateLimited(ip) {
  const now = Date.now();
  const entry = hits.get(ip);
  if (!entry || now - entry.start > RATE_WINDOW_MS) {
    hits.set(ip, { start: now, count: 1 });
    return false;
  }
  entry.count += 1;
  return entry.count > RATE_LIMIT;
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const prompt = typeof req.body?.prompt === "string" ? req.body.prompt.trim() : "";
  if (!prompt) return res.status(400).json({ error: "Please enter a prompt." });
  if (prompt.length > MAX_PROMPT_CHARS) {
    return res.status(400).json({ error: `Prompt is too long (max ${MAX_PROMPT_CHARS} characters).` });
  }

  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
  if (rateLimited(ip)) {
    return res.status(429).json({ error: "Demo limit reached. Sign up to keep creating!" });
  }
  if (!process.env.ANTHROPIC_API_KEY) {
    return res.status(500).json({ error: "Live demo is not configured: set ANTHROPIC_API_KEY on the server." });
  }

  try {
    const stream = client.beta.messages.stream({
      model: "claude-opus-5-5",
      max_tokens: 1024, // demo replies are deliberately short
      output_config: { effort: "low" },
      system: SYSTEM_PROMPT,
      messages: [{ role: "user", content: prompt }],
      // If a request is declined, the API retries it on a fallback model automatically.
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
    });

    // Send headers only once text arrives, so early API errors can still return JSON.
    for await (const event of stream) {
      if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
        if (!res.headersSent) {
          res.writeHead(200, { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" });
        }
        res.write(event.delta.text);
      }
    }
    if (!res.headersSent) {
      res.writeHead(200, { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" });
    }

    const message = await stream.finalMessage();
    if (message.stop_reason === "refusal") {
      res.write("\n\nSorry, Muse can't help with that request. Try a different prompt.");
    }
    return res.end();
  } catch (error) {
    console.error("generate failed:", error);
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
