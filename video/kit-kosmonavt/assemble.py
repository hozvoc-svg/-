"""Assemble the final 1080x1920 video. Uses shots/NN.mp4 when present,
otherwise a placeholder card (animatic). Run build_audio.py first."""
import json, os, subprocess
tl = json.load(open('timeline.json'))
labels = ["1 · Хук: кіт у шоломі-акваріумі, ракета трясеться", "2 · Ніч, кіт дивиться на Місяць", "3 · Будує ракету з коробки і скотчу",
          "4 · Скафандр з фольги, рибки проти", "5 · ПУСК! Ракета злітає", "6 · Невагомість у космосі",
          "7 · Місяць із сиру — кусає", "8 · Прокинувся в коробці, сир на вусах"]
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
os.makedirs('norm', exist_ok=True)
VF = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,format=yuv420p"
parts = []
for i, d in enumerate(tl['shots']):
    out = f'norm/{i+1:02d}.mp4'; src = f'shots/{i+1:02d}.mp4'
    if os.path.exists(src):
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
        speed = min(1.0, dur / d)  # stretch (slow down) short clips to fill the shot
        vf = f"setpts=PTS/{speed:.4f},{VF}" if speed < 1 else VF
        # punch-in zoom on the hook and the launch
        if i in (0, 4): vf += ",zoompan=z='min(1+0.004*on,1.18)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"
        cmd = ['ffmpeg', '-v', 'error', '-y', '-i', src, '-t', str(d), '-vf', vf, '-an', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', out]
    else:
        txt = labels[i].replace(':', '\\:').replace("'", '')
        vf = (f"drawtext=fontfile={FONT}:text='{txt}':fontcolor=white:fontsize=36:x=(w-tw)/2:y=h*0.32:box=1:boxcolor=black@0.4:boxborderw=24,"
              f"drawtext=fontfile={FONT}:text='ЧОРНОВИК · кадр буде згенеровано':fontcolor=0xFFD700:fontsize=34:x=(w-tw)/2:y=h*0.25")
        cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=c=0x{["2b3a67","1d2b4f","5a3e2b","3f5f6b","7a2e1f","0e0f2e","6b5a1f","4f3b2b"][i]}:s=1080x1920:r=30:d={d}',
               '-vf', vf + ',format=yuv420p', '-c:v', 'libx264', '-crf', '20', out]
    subprocess.run(cmd, check=True); parts.append(out)
open('list.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'video_only.mp4'], check=True)
final = 'kit-kosmonavt.mp4' if all(os.path.exists(f'shots/{i+1:02d}.mp4') for i in range(8)) else 'kit-kosmonavt_animatic.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'video_only.mp4', '-i', 'audio/mix_raw.wav',
                '-vf', 'ass=captions.ass', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-map', '0:v', '-map', '1:a',
                '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100',
                '-movflags', '+faststart', '-shortest', final], check=True)
print('wrote', final)
