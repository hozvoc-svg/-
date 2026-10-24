#!/bin/bash
# Build several episodes one after another, each followed by a delivery-size re-encode.
# Usage: ELEVENLABS=1 ./run_queue.sh ep1 ep2 ...   (waits for any build already running to finish first)
HERE="$(cd "$(dirname "$0")" && pwd)"
LOG="${QUEUE_LOG:-$HERE/tmp/queue.log}"
while pgrep -f "build.py long" > /dev/null || pgrep -f "_final.mp4" > /dev/null; do sleep 30; done
for ep in "$@"; do
  echo "$(date -u +%H:%M) start $ep" >> "$LOG"
  if EPISODE="$ep" python3 "$HERE/build.py" long >> "$LOG" 2>&1 &&
     ffmpeg -v error -y -i "$HERE/out/${ep}_long.mp4" -vf scale=2560:1440:flags=lanczos -c:v libx265 -preset medium -crf 21 -tag:v hvc1 \
       -x265-params log-level=error -pix_fmt yuv420p \
       -c:a copy -movflags +faststart "$HERE/out/${ep}_final.mp4" >> "$LOG" 2>&1; then
    echo "$(date -u +%H:%M) done $ep $(du -h "$HERE/out/${ep}_final.mp4" | cut -f1)" >> "$LOG"
  else
    echo "$(date -u +%H:%M) FAILED $ep" >> "$LOG"
  fi
done
echo "$(date -u +%H:%M) queue finished" >> "$LOG"
