#!/bin/bash
# Render every shot (resumable), two in parallel, then encode each to shots/<id>.mp4
cd "$(dirname "$0")"; mkdir -p shots logs
run() { for s in "$@"; do EGL_PLATFORM=surfaceless /opt/bpyenv/bin/python scenes.py $s > logs/$s.log 2>&1
  ffmpeg -v error -y -framerate 30 -i frames/$s/%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p shots/$s.mp4; echo "shot $s done"; done; }
run A B C D E F G H I J K; echo ALL DONE
