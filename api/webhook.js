// Vercel serverless function: POST /api/webhook
// Receives Lemon Squeezy subscription events and updates the user's plan and credits.
// Lemon Squeezy → Settings → Webhooks: URL https://<your-site>/api/webhook, events below, signing secret
// stored as LEMONSQUEEZY_WEBHOOK_SECRET. Checkout links must pass checkout[custom][user_id].
import crypto from "node:crypto";
import { PLANS, supabaseAdmin } from "./_lib.js";

function planForVariant(variantId) {
  const id = String(variantId);
  if (id === process.env.LEMONSQUEEZY_VARIANT_PRO) return "pro";
  if (id === process.env.LEMONSQUEEZY_VARIANT_CREATOR) return "creator";
  return null;
}

function validSignature(raw, signature, secret) {
  if (!signature || !secret) return false;
  const expected = crypto.createHmac("sha256", secret).update(raw).digest("hex");
  const a = Buffer.from(expected, "utf8");
  const b = Buffer.from(String(signature), "utf8");
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

export async function POST(request) {
  const raw = await request.text();
  if (!validSignature(raw, request.headers.get("x-signature"), process.env.LEMONSQUEEZY_WEBHOOK_SECRET)) {
    return json({ error: "Invalid signature" }, 401);
  }
  const db = supabaseAdmin();
  if (!db) return json({ error: "Supabase is not configured" }, 500);

  const event = JSON.parse(raw);
  const name = event.meta?.event_name;
  const userId = event.meta?.custom_data?.user_id;
  const attrs = event.data?.attributes || {};

  try {
    if (name === "subscription_payment_success") {
      // A renewal was paid: refill the monthly credits.
      const subscriptionId = String(attrs.subscription_id);
      const { data: profile } = await db.from("profiles").select("id, plan").eq("subscription_id", subscriptionId).maybeSingle();
      if (profile && PLANS[profile.plan]) {
        await db.from("profiles").update({ credits: PLANS[profile.plan], credits_reset_at: new Date().toISOString() }).eq("id", profile.id);
      }
      return json({ ok: true });
    }

    if (!name?.startsWith("subscription_")) return json({ ok: true, ignored: name });

    const subscriptionId = String(event.data.id);
    const plan = planForVariant(attrs.variant_id);
    const active = ["active", "on_trial", "past_due", "cancelled"].includes(attrs.status); // cancelled = active until period end
    const update = {
      subscription_id: subscriptionId,
      subscription_status: attrs.status,
      customer_portal_url: attrs.urls?.customer_portal ?? null,
    };

    let query;
    if (userId) query = db.from("profiles").select("id, plan, credits").eq("id", userId);
    else query = db.from("profiles").select("id, plan, credits").eq("subscription_id", subscriptionId);
    const { data: profile } = await query.maybeSingle();
    if (!profile) return json({ error: "Profile not found" }, 404);

    if (active && plan) {
      update.plan = plan;
      // New subscription or upgrade: top up to the plan's monthly credits.
      if (name === "subscription_created" || PLANS[plan] > PLANS[profile.plan]) {
        update.credits = Math.max(profile.credits, PLANS[plan]);
        update.credits_reset_at = new Date().toISOString();
      }
    } else if (!active) {
      // Expired or unpaid: back to the free plan.
      update.plan = "free";
      update.credits = Math.min(profile.credits, PLANS.free);
      update.credits_reset_at = new Date().toISOString();
    }

    const { error } = await db.from("profiles").update(update).eq("id", profile.id);
    if (error) throw error;
    return json({ ok: true });
  } catch (error) {
    console.error("webhook failed:", name, error);
    return json({ error: "Webhook processing failed" }, 500);
  }
}
