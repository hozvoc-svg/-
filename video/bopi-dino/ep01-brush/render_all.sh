#!/bin/bash
# Render every shot (resumable: finished frames are skipped) and encode shots/SN.mp4 at 12 fps.
cd "$(dirname "$0")"
PY=${BLENDER_PY:-/opt/bpyenv/bin/python}
mkdir -p shots
for s in S1 S2 S3 S4 S5 S6 S7 S8 S9; do
  [ -f shots/$s.mp4 ] && { echo "$s done"; continue; }
  $PY bopi_scenes.py -- $s 2>&1 | grep -c Saved | xargs echo "$(date +%T) shot $s frames:"
  ffmpeg -v error -y -framerate 12 -i frames/$s/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p shots/$s.mp4 && echo "shot $s -> shots/$s.mp4"
done
echo ALL DONE
