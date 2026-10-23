// Shared server code. Files starting with "_" are not exposed as API routes on Vercel.
import { createClient } from "@supabase/supabase-js";

// Monthly credits per plan. Keep in sync with plan_credits() in supabase/schema.sql.
export const PLANS = { free: 10, creator: 300, pro: 1000 };

export const TEMPLATES = {
  ad: "a short, high-converting social media ad with a hook, the key benefit and a clear call to action",
  social: "an engaging social media post (Instagram, LinkedIn or X) with a strong first line and relevant hashtags at the end",
  product: "a persuasive product description: a one-line headline, a short paragraph and 3 benefit bullet points",
  email: "a short marketing or outreach email with a subject line, friendly tone and one clear call to action",
  blog: "a blog post outline with a catchy title, an intro paragraph and 5-7 section headings with one-line summaries",
  slogan: "10 distinct slogan or tagline options, one per line, each under 10 words",
  tiktok: "a 30-45 second TikTok / Reels / Shorts video script: a hook for the first 3 seconds, 3-5 short scenes with what to show and what to say, and a closing call to action",
  review: "a reply to a customer review: thank them by name if given, address their specific points, apologise and offer a fix if the review is negative, and keep it warm and short",
  listing: "a marketplace listing (Etsy, Amazon, Shopify, Prom, Rozetka): a search-friendly title under 140 characters, 5 benefit bullet points and 13 comma-separated search tags",
  hashtags: "30 relevant hashtags grouped under three labels: popular, niche and local/branded; hashtags only, separated by spaces within each group",
  names: "15 creative brand or business name ideas, one per line, each followed by a dash and a one-line explanation",
};

// Refinements of a previous result (one credit each).
export const REFINE = {
  again: "Write a new, clearly different version of the same content.",
  shorter: "Rewrite it to be about half as long, keeping the key message and call to action.",
  longer: "Rewrite it to be more detailed and about 1.5 times longer, keeping the same tone.",
};

export const MAX_PROMPT_CHARS = 1000;
export const MAX_BRAND_CHARS = 500;
const MAX_PREVIOUS_CHARS = 6000;

// Builds the conversation: the task (with the saved business profile, if any) and optionally a refinement.
export function buildMessages({ prompt, brand, mode, previous }) {
  const task = brand ? `About my business: ${brand}\n\nTask: ${prompt}` : prompt;
  const messages = [{ role: "user", content: task }];
  if (REFINE[mode] && previous) {
    messages.push({ role: "assistant", content: previous.slice(0, MAX_PREVIOUS_CHARS) });
    messages.push({ role: "user", content: REFINE[mode] });
  }
  return messages;
}

export const TONES = ["friendly", "professional", "playful", "bold", "luxury", "minimal"];

export const LANGUAGES = [
  "English", "Chinese", "Hindi", "Spanish", "French", "Arabic",
  "Portuguese", "German", "Italian", "Polish", "Ukrainian",
];

export function buildSystemPrompt({ template, tone, language }) {
  return `You are Muse, an expert marketing copywriter.
Write ${TEMPLATES[template]}.
Tone: ${tone}. Write in ${language}.
Output only the finished content, ready to copy and publish. Plain text, no Markdown headings or bold markers; use "•" for bullet points.
If the request is not a content-writing task, briefly say Muse writes marketing content and suggest how to rephrase it.`;
}

let admin;
export function supabaseAdmin() {
  if (!process.env.SUPABASE_URL || !process.env.SUPABASE_SERVICE_ROLE_KEY) return null;
  admin ??= createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
  return admin;
}

// Returns the signed-in user from the "Authorization: Bearer <token>" header, or null.
export async function getUser(authorization) {
  const token = (authorization || "").replace(/^Bearer\s+/i, "");
  const db = supabaseAdmin();
  if (!token || !db) return null;
  const { data, error } = await db.auth.getUser(token);
  return error ? null : data.user;
}

export function clientIp(headers) {
  return (headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
}
