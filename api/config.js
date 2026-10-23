// Vercel serverless function: GET /api/config
// Exposes the public settings the browser needs. Only public values belong here:
// the Supabase anon key is designed to be public (row level security protects the data).
export function GET() {
  const config = {
    supabaseUrl: process.env.SUPABASE_URL || "",
    supabaseAnonKey: process.env.SUPABASE_ANON_KEY || "",
    checkout: {
      creator: process.env.LEMONSQUEEZY_CHECKOUT_CREATOR || "",
      pro: process.env.LEMONSQUEEZY_CHECKOUT_PRO || "",
    },
  };
  return new Response(JSON.stringify(config), {
    headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=300" },
  });
}
