"""Assemble ep01: shots/S1..S9.mp4 + audio/mix_norm.wav + karaoke lyrics + hook text -> out/bopi_ep01_brush.mp4 (1080x1920)
Run after render_all.sh and build_audio.py (+ loudnorm, see README)."""
import json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
FONTS = os.path.abspath(os.path.join(HERE, '..', 'fonts'))
d = json.load(open('song.json')); words = json.load(open('audio/words.json'))
B = 60 / d['bpm']; T0 = d['start']
def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f'{h}:{m:02d}:{s:05.2f}'
# ASS colours are &HAABBGGRR
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 0", "",
       "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Lyric,Fredoka,84,&H0032D7FF,&H00FFFFFF,&H00602A4A,&H64000000,-1,0,0,0,100,100,1,0,1,7,3,2,90,90,430,1",
       "Style: Hook,Fredoka,104,&H00FFFFFF,&H00FFFFFF,&H001E1EC8,&H64000000,-1,0,0,0,100,100,2,0,1,9,4,8,60,60,300,1",
       "Style: End,Fredoka,120,&H0032D7FF,&H00FFFFFF,&H00602A4A,&H64000000,-1,0,0,0,100,100,2,0,1,9,4,8,60,60,330,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
# hook text (different from the voice line "Oh no! Sugar bugs!")
ass.append(f"Dialogue: 1,{ts(0.15)},{ts(2.45)},Hook,,0,0,0,,{{\\fad(60,0)\\t(0,180,\\fscx112\\fscy112)\\t(180,320,\\fscx100\\fscy100)}}BOPI FORGOT\\NTO BRUSH!")
# karaoke lines: one per 4-beat line; split into two rows when long
i = 0
for li, L in enumerate(d['lines']):
    n = len(L['notes']); ws = words[i:i + n]; i += n
    start = T0 + li * 4 * B; end = start + 4 * B
    parts = []; lead = max(0, round((ws[0]['t'] - (start - 0.15)) * 100))
    txt = f"{{\\k{lead}}}"
    for w in ws:
        word = w['w'] + ('!' if w is ws[-1] else '')
        txt += f"{{\\k{round(w['d'] * 100)}}}{word} "
    ass.append(f"Dialogue: 0,{ts(start - 0.15)},{ts(end - 0.05)},Lyric,,0,0,0,,{{\\fad(80,60)}}{txt.strip()}")
END = T0 + 16 * 4 * B
ass.append(f"Dialogue: 1,{ts(END - 0.2)},{ts(END + 1.9)},End,,0,0,0,,{{\\fad(100,0)\\t(0,200,\\fscx115\\fscy115)\\t(200,350,\\fscx100\\fscy100)}}SHINY TEETH!")
open('captions.ass', 'w').write('\n'.join(ass) + '\n')

os.makedirs('out', exist_ok=True)
shots = [f'shots/S{k}.mp4' for k in range(1, 10)]
open('list.txt', 'w').write(''.join(f"file '{s}'\n" for s in shots))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'out/video_only.mp4'], check=True)
vf = f"scale=1080:1920:flags=lanczos,setsar=1,ass=captions.ass:fontsdir={FONTS}"
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'out/video_only.mp4', '-i', 'audio/mix_norm.wav', '-vf', vf,
                '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
                '-r', '24', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', 'out/bopi_ep01_brush.mp4'], check=True)
print('-> out/bopi_ep01_brush.mp4')
