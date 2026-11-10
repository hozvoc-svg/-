#!/bin/bash
# Render every clay shot (skips finished ones) and turn frames into shots/NN.mp4 at 12 fps.
cd "$(dirname "$0")/.."
PY=${BLENDER_PY:-python3}
mkdir -p shots
for s in 01 02 03 04 05 06 07 08; do
  [ -f shots/$s.mp4 ] && { echo "$s done"; continue; }
  rm -rf clay/frames/$s
  $PY clay/clay_scenes.py -- $s 2>&1 | grep -c Saved | xargs echo "shot $s frames:"
  ffmpeg -v error -y -framerate 12 -i clay/frames/$s/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p shots/$s.mp4 && echo "shot $s -> shots/$s.mp4"
done
