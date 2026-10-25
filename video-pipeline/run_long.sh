#!/bin/bash
# Render + encode one long music episode, detached from the calling shell (survives task time limits).
# Usage: setsid nohup ./run_long.sh <episode> <crf> > /dev/null 2>&1 &
HERE="$(cd "$(dirname "$0")" && pwd)"
EP="$1"; CRF="${2:-30}"
LOG="$HERE/tmp/queue.log"
echo "$(date -u +%H:%M) start $EP" >> "$LOG"
until EPISODE="$EP" python3 "$HERE/build.py" long >> "$LOG" 2>&1; do
  echo "$(date -u +%H:%M) retry $EP" >> "$LOG"; sleep 20
done
echo "$(date -u +%H:%M) encode $EP crf$CRF" >> "$LOG"
ffmpeg -nostdin -v error -y -i "$HERE/out/${EP}_long.mp4" -c:v libx265 -preset medium -crf "$CRF" -tag:v hvc1 \
  -x265-params log-level=error -pix_fmt yuv420p -c:a copy -movflags +faststart "$HERE/out/${EP}_final.mp4" >> "$LOG" 2>&1 \
  && echo "$(date -u +%H:%M) done $EP $(du -h "$HERE/out/${EP}_final.mp4" | cut -f1)" >> "$LOG" \
  || echo "$(date -u +%H:%M) FAILED encode $EP" >> "$LOG"
