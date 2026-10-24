#!/bin/bash
# Install the Google Fonts used by the channel art (from npm @fontsource, converted to TTF for cairo/fontconfig).
set -e
FONTS="cormorant-garamond playfair-display cinzel montserrat lora quicksand
cinzel-decorative cormorant eb-garamond libre-baskerville dm-serif-display marcellus philosopher
josefin-sans raleway poppins nunito comfortaa space-grotesk orbitron exo-2 audiowide michroma syncopate
great-vibes dancing-script satisfy parisienne caveat amatic-sc
bebas-neue oswald anton abril-fatface alegreya crimson-text spectral italiana tenor-sans julius-sans-one"
pip install -q fonttools brotli
TMP=$(mktemp -d)
cd "$TMP"
for f in $FONTS; do npm pack --silent "@fontsource/$f" > /dev/null 2>&1 || echo "skip $f"; done
mkdir -p x ~/.fonts/sleepy
for t in *.tgz; do tar xzf "$t" -C x --one-top-level="${t%.tgz}"; done
python3 - <<'PY'
import glob, os
from fontTools.ttLib import TTFont
n = 0
for p in glob.glob('x/*/package/files/*-latin-*.woff2'):
    if '-ext-' in p:
        continue
    f = TTFont(p); f.flavor = None
    f.save(os.path.expanduser('~/.fonts/sleepy/') + os.path.basename(p).replace('.woff2', '.ttf')); n += 1
print(n, "font files")
PY
fc-cache -f > /dev/null
echo "fonts installed"
