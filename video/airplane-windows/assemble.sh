#!/bin/bash
# Concatenate shots, light grade, burn captions/titles, mix audio at -14 LUFS -> final.mp4 + cover.png
set -e; cd "$(dirname "$0")"
printf "file 'shots/%s.mp4'\n" A B C D E F G H I J K > list.txt
ffmpeg -v error -y -f concat -safe 0 -i list.txt -c copy video_only.mp4
ffmpeg -v error -y -i video_only.mp4 -i audio/mix_raw.wav -filter_complex \
 "[0:v]eq=saturation=1.25:contrast=1.06,ass=captions.ass,format=yuv420p[v];[1:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -profile:v high -crf 18 -preset medium -r 30 \
 -c:a aac -b:a 192k -ar 48000 -movflags +faststart -t 60.9 final.mp4
ffmpeg -v error -y -ss 1.2 -i final.mp4 -frames:v 1 cover.png
echo "final.mp4: $(ffprobe -v error -show_entries format=duration:stream=width,height -of csv=p=0 final.mp4 | tr '\n' ' ')"
