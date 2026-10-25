#!/bin/bash
# Replace Git LFS pointer stubs in the HyperFrames plugin with the real files (the git proxy does not serve LFS).
M=/root/.claude/plugins/marketplaces/hyperframes
B=$(git -C "$M" rev-parse HEAD)
for f in $(git -C "$M" lfs ls-files -n); do
  head -c 40 "$M/$f" | grep -q git-lfs.github.com/spec || continue
  curl -sSfL --retry 3 -o "$M/$f" "https://media.githubusercontent.com/media/heygen-com/hyperframes/$B/$f"
done
grep -rl git-lfs.github.com/spec /root/.claude/plugins/cache/hyperframes 2>/dev/null | while read -r f; do
  rel=$(echo "$f" | sed -E 's|^/root/.claude/plugins/cache/hyperframes/[^/]+/[^/]+/||'); cp "$M/$rel" "$f"
done
