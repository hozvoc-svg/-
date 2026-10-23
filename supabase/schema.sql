-- Muse database schema for Supabase.
-- Run once: Supabase dashboard → SQL Editor → paste this file → Run.

-- One row per user: plan, credits and billing state.
create table if not exists public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  email text,
  full_name text,
  plan text not null default 'free' check (plan in ('free', 'creator', 'pro')),
  credits integer not null default 10 check (credits >= 0),
  credits_reset_at timestamptz not null default now(),
  subscription_id text,
  subscription_status text,
  customer_portal_url text,
  created_at timestamptz not null default now()
);

-- Saved generations, shown in the user's history.
create table if not exists public.generations (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users (id) on delete cascade,
  template text not null,
  prompt text not null,
  output text not null,
  created_at timestamptz not null default now()
);
create index if not exists generations_user_created_idx on public.generations (user_id, created_at desc);

-- Added later: the user's saved business description (re-running this file is safe).
alter table public.profiles add column if not exists brand text check (char_length(brand) <= 500);

-- Row level security: users can read only their own rows.
-- All writes go through the server (service role) or the functions below.
alter table public.profiles enable row level security;
alter table public.generations enable row level security;

drop policy if exists "read own profile" on public.profiles;
create policy "read own profile" on public.profiles for select using (auth.uid() = id);

drop policy if exists "read own generations" on public.generations;
create policy "read own generations" on public.generations for select using (auth.uid() = user_id);

-- Create a profile automatically when someone signs up.
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, email, full_name)
  values (new.id, new.email, new.raw_user_meta_data ->> 'full_name')
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- Monthly credits per plan. Keep in sync with PLANS in api/_lib.js.
create or replace function public.plan_credits(p text)
returns integer language sql immutable as $$
  select case p when 'pro' then 1000 when 'creator' then 300 else 10 end;
$$;

-- Atomically spend one credit. Free plans refill every 30 days.
-- Returns the remaining credits, or -1 when the user has none left.
create or replace function public.use_credit(uid uuid)
returns integer language plpgsql security definer set search_path = public as $$
declare remaining integer;
begin
  update profiles
     set credits = plan_credits(plan), credits_reset_at = now()
   where id = uid and plan = 'free' and credits_reset_at < now() - interval '30 days';

  update profiles set credits = credits - 1
   where id = uid and credits > 0
   returning credits into remaining;

  return coalesce(remaining, -1);
end;
$$;

-- Give a credit back when a generation fails.
create or replace function public.refund_credit(uid uuid)
returns void language sql security definer set search_path = public as $$
  update profiles set credits = credits + 1 where id = uid;
$$;

-- Only the server may call the credit functions.
revoke execute on function public.use_credit(uuid) from public, anon, authenticated;
revoke execute on function public.refund_credit(uuid) from public, anon, authenticated;
