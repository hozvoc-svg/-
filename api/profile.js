// Vercel serverless function: POST /api/profile  { brand }
// Saves the signed-in user's business description, which /api/generate adds to every task.
// Writes go through the server so users can never change their own plan or credits.
import { MAX_BRAND_CHARS, supabaseAdmin, getUser } from "./_lib.js";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }
  const user = await getUser(req.headers.authorization);
  if (!user) return res.status(401).json({ error: "Please log in again.", code: "auth" });

  const brand = typeof req.body?.brand === "string" ? req.body.brand.trim().slice(0, MAX_BRAND_CHARS) : "";
  const { error } = await supabaseAdmin().from("profiles").update({ brand: brand || null }).eq("id", user.id);
  if (error) {
    console.error("saving profile failed:", error);
    return res.status(500).json({ error: "Could not save. Please try again.", code: "server" });
  }
  return res.status(200).json({ ok: true, brand });
}
