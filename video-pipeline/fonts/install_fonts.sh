#!/bin/bash
# Install the Google Fonts used by the channel art (from npm @fontsource, converted to TTF for cairo/fontconfig).
set -e
pip install -q fonttools brotli
TMP=$(mktemp -d)
cd "$TMP"
for f in cormorant-garamond playfair-display cinzel montserrat lora quicksand; do npm pack --silent "@fontsource/$f" > /dev/null; done
mkdir -p x ~/.fonts/sleepy
for t in *.tgz; do tar xzf "$t" -C x --one-top-level="${t%.tgz}"; done
python3 - <<'PY'
import glob, os
from fontTools.ttLib import TTFont
for p in glob.glob('x/*/package/files/*-latin-*.woff2'):
    if '-ext-' in p:
        continue
    f = TTFont(p); f.flavor = None
    f.save(os.path.expanduser('~/.fonts/sleepy/') + os.path.basename(p).replace('.woff2', '.ttf'))
PY
fc-cache -f > /dev/null
echo "fonts installed"
