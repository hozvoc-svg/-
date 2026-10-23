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
};

export const TONES = ["friendly", "professional", "playful", "bold", "luxury", "minimal"];

export const LANGUAGES = ["English", "Ukrainian", "Spanish", "German", "French", "Polish", "Portuguese", "Italian"];

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
