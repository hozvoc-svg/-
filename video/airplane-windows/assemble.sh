#!/bin/bash
# Concatenate shots, light grade, burn captions/titles, mix audio at -14 LUFS -> final.mp4 + cover.png
set -e; cd "$(dirname "$0")"
# hook pre-roll: 0.6 s flash of the square window cracking (frames from shot B)
ffmpeg -v error -y -framerate 30 -start_number 70 -i frames/B/%04d.png -frames:v 18 \
  -vf "scale=1188:2112,crop=1080:1920,eq=saturation=1.4:contrast=1.15" -c:v libx264 -crf 16 -pix_fmt yuv420p shots/PRE.mp4
printf "file 'shots/%s.mp4'\n" PRE A B C D E F G H I J K > list.txt
ffmpeg -v error -y -f concat -safe 0 -i list.txt -c copy video_only.mp4
ffmpeg -v error -y -i video_only.mp4 -i audio/mix_raw.wav -filter_complex \
 "[0:v]split[n][z];[z]scale=1188:2112,crop=1080:1920[zz];[n][zz]overlay=0:0:enable='between(t,9.6,11.2)+between(t,13.5,15.8)+between(t,22.8,24.6)+between(t,26.4,29.0)+between(t,35.0,37.7)+between(t,44.3,46.6)+between(t,48.8,50.9)+between(t,55.5,57.6)',setsar=1,eq=saturation=1.25:contrast=1.06,ass=captions.ass,format=yuv420p[v];[1:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -profile:v high -crf 18 -preset medium -r 30 \
 -c:a aac -b:a 192k -ar 48000 -movflags +faststart -t 61.5 final.mp4
ffmpeg -v error -y -ss 1.2 -i final.mp4 -frames:v 1 cover.png
echo "final.mp4: $(ffprobe -v error -show_entries format=duration:stream=width,height -of csv=p=0 final.mp4 | tr '\n' ' ')"
