// Accounts and billing helpers shared by login.html and app.html.
// Needs the Supabase library (loaded from a CDN before this file) and the /api/config endpoint.
window.Muse = (() => {
  let clientPromise;

  const loadConfig = async () => {
    const res = await fetch('/api/config');
    if (!res.ok) throw new Error('not-configured');
    const config = await res.json();
    if (!config.supabaseUrl || !config.supabaseAnonKey) throw new Error('not-configured');
    return config;
  };

  const init = () => {
    clientPromise ??= loadConfig().then((config) => ({
      config,
      sb: window.supabase.createClient(config.supabaseUrl, config.supabaseAnonKey),
    }));
    return clientPromise;
  };

  const session = async () => {
    const { sb } = await init();
    const { data } = await sb.auth.getSession();
    return data.session;
  };

  // Sends the visitor to the login page unless they are signed in.
  const requireSession = async () => {
    const s = await session();
    if (!s) {
      location.replace('login.html?next=' + encodeURIComponent(location.pathname.split('/').pop() + location.search));
      return new Promise(() => {}); // page is navigating away
    }
    return s;
  };

  const signIn = async (email, password) => {
    const { sb } = await init();
    const { error } = await sb.auth.signInWithPassword({ email, password });
    if (error) throw error;
  };

  const signUp = async (email, password, fullName) => {
    const { sb } = await init();
    const { data, error } = await sb.auth.signUp({
      email,
      password,
      options: { data: { full_name: fullName }, emailRedirectTo: new URL('app.html', location.href).href },
    });
    if (error) throw error;
    return { needsConfirmation: !data.session };
  };

  const signInWithGoogle = async (next = 'app.html') => {
    const { sb } = await init();
    const { error } = await sb.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: new URL(next, location.href).href },
    });
    if (error) throw error;
  };

  // Emails a password-reset link that opens reset.html.
  const resetPassword = async (email) => {
    const { sb } = await init();
    const { error } = await sb.auth.resetPasswordForEmail(email, { redirectTo: new URL('reset.html', location.href).href });
    if (error) throw error;
  };

  // On reset.html the link signs the user in; then the new password is saved here.
  const updatePassword = async (password) => {
    const { sb } = await init();
    const { error } = await sb.auth.updateUser({ password });
    if (error) throw error;
  };

  // Saves the business description used in every generation (see api/profile.js).
  const saveBrand = async (brand) => {
    const s = await session();
    const res = await fetch('/api/profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${s.access_token}` },
      body: JSON.stringify({ brand }),
    });
    if (!res.ok) throw new Error((await res.json().catch(() => ({}))).code || 'server');
  };

  const signOut = async () => {
    const { sb } = await init();
    await sb.auth.signOut();
    location.href = 'index.html';
  };

  const profile = async () => {
    const { sb } = await init();
    const { data, error } = await sb.from('profiles').select('*').maybeSingle();
    if (error) throw error;
    return data;
  };

  const history = async (limit = 20) => {
    const { sb } = await init();
    const { data, error } = await sb.from('generations')
      .select('id, template, prompt, output, created_at')
      .order('created_at', { ascending: false })
      .limit(limit);
    if (error) throw error;
    return data;
  };

  // Opens the Lemon Squeezy checkout for a plan, linked to the signed-in user.
  const checkoutUrl = async (plan) => {
    const { config } = await init();
    const s = await session();
    const base = config.checkout[plan];
    if (!base || !s) return null;
    const url = new URL(base);
    url.searchParams.set('checkout[custom][user_id]', s.user.id);
    url.searchParams.set('checkout[email]', s.user.email);
    return url.href;
  };

  return { init, session, requireSession, signIn, signUp, signInWithGoogle, signOut, resetPassword, updatePassword, saveBrand, profile, history, checkoutUrl };
})();
