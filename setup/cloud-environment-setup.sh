# Video skills for every session, in any project
export PATH="$HOME/.local/bin:$PATH"
if command -v claude >/dev/null 2>&1; then
  claude plugin marketplace add hozvoc-svg/- || true
  claude plugin install video-studio@hozvoc-video || true
fi
# Code-rendered video: Blender as a Python module (+ numpy/scipy) in /opt/bpyenv
if [ ! -x /opt/bpyenv/bin/python ]; then
  if command -v uv >/dev/null 2>&1; then
    uv venv -q -p 3.13 /opt/bpyenv && uv pip install -q -p /opt/bpyenv/bin/python bpy numpy scipy || true
  else
    python3 -m venv /opt/bpyenv && /opt/bpyenv/bin/pip install -q bpy numpy scipy || true
  fi
fi
pip install -q numpy scipy 2>/dev/null || true
# Higgsfield prompt skills (AKCodez/higgsfield-claude-skills, pinned commit; text only)
HF_TMP=$(mktemp -d)
if git clone -q https://github.com/AKCodez/higgsfield-claude-skills.git "$HF_TMP/hf" && git -C "$HF_TMP/hf" checkout -q f6698ab7a87223b67a76ce748ca1b936a8b5d399; then
  for d in 01-cinematic 02-3d-cgi 03-cartoon 04-comic-to-video 05-fight-scenes 06-motion-design-ad 07-ecommerce-ad \
           08-anime-action 09-product-360 10-music-video 11-social-hook 12-brand-story 13-fashion-lookbook 14-food-beverage 15-real-estate; do
    mkdir -p "$HOME/.claude/skills/higgsfield-$d" && cp "$HF_TMP/hf/$d/SKILL.md" "$HOME/.claude/skills/higgsfield-$d/SKILL.md"
  done
fi
rm -rf "$HF_TMP"
