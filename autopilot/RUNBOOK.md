# Autopilot for @neuronbites (Instagram, English psychology reels)

You run with nobody watching. Work end to end, never ask questions, never wait for a reply.
If a step is impossible, skip it, keep going where you can, and say clearly in your final message what failed and why.

Repository: `hozvoc-svg/-`, branch `claude/inspiring-heisenberg-7y05q5`. Everything you make is committed and pushed there.
Memory between runs: `autopilot/log.json` (every reel, its Instagram id and stats) and `autopilot/followers.json`.

## Setup (both jobs)
1. If the repository is not in the working directory, clone it: `git clone https://github.com/hozvoc-svg/- repo && cd repo`
   and `git checkout claude/inspiring-heisenberg-7y05q5`. If `git push` is refused, attach the repository with the
   `add_repo` tool (owner `hozvoc-svg`, repo `-`, access `push`) and push again.
2. `pip install -q pycairo numpy` if `python3 -c "import cairo"` fails.
3. `python3 autopilot/ig.py check`. If it fails with an auth error, the Instagram token is missing or expired: still do
   the rest of the job, and start the final message with «⚠️ Ключ Instagram не працює, онови його» and the error.

## Night job (≈02:00 Kyiv): research → make → publish
1. **Research.** `python3 autopilot/trends.py 7` lists English Shorts from the last 7 days that beat their channel size.
   Ignore anything that is not psychology/relationships/human behaviour (games, cars, K-pop edits, horoscopes,
   "your birth date reveals…" pseudo-science). Prefer topics with a high ratio (views ÷ subscribers) AND a named,
   real psychological effect behind them. Skip topics already in `autopilot/log.json`.
   Also read `autopilot/LESSONS.md` and the stats in `log.json`: lean towards what got the longest average watch time and the most shares.
2. **Facts.** Only say what research supports. Name the effect or study when there is one. If a viral claim is a myth
   ("laughing = genius", "sleeping position reveals personality"), either skip it or make the reel about why it's a myth.
3. **Script** (`reelNN/script.txt`, NN = next free number): 60–80 words, 20–26 s spoken.
   Structure that works for this channel: a relatable hook in the first sentence that opens a loop
   ("…psychology has a name for it"), the named effect, why it happens, one practical tip, and the last line
   "Send this to …" (a specific person: the friend who…, someone who…). Send-to-a-friend endings beat "Follow".
   The very first frame must already show the conflict/situation, not a title card.
4. **Voice:** `cd reelNN && python3 ../autopilot/voice.py script.txt "phrase" "phrase" …` (prints timings).
   If the result is over 27 s, cut words and regenerate.
5. **Animation:** write `reelNN/cartoonNN.py` in the channel style. Copy the structure of `reel11/cartoon11.py` or
   `reel10/cartoon10.py`: `engine.py` (characters, backgrounds, captions, transitions) plus `stamp`, `speech`,
   `phone` helpers imported from `reel07/cartoon7.py`. 5–6 scenes, one per sentence, a new visual event every 2–3 s,
   a final share scene with a phone and a tapping finger, and a small "Follow @neuronbites" pill.
6. **Check it with your own eyes.** Render a contact sheet: `PREVIEW_DIR=<scratchpad> python3 cartoonNN.py 0.8 3 5 …`
   (12 timestamps), glue into one image and look at it. Fix every overlap (text over faces, labels hidden under the
   title pill, objects off-screen, tiny unreadable text, stray lines). Repeat until clean. Never skip this.
7. **Render + sound:** `python3 cartoonNN.py`, then write `cues.json` (sfx at phrases: whoosh on scene changes,
   pop on labels, ding on reveals, buzz on bad moments) and `python3 ../autopilot/mix.py cues.json reelNN_<slug>.mp4`.
8. **Cover** `cover_reelNN.png` (see `reel11/cover11.py`): 3 lines of big text in the top third, the key scene below,
   readable when cropped to 3:4 in the profile grid.
9. **Caption** `reelNN/caption.txt`: hook line + one sentence with the named effect + "Send this to …" + 8 hashtags.
   Also `reelNN/POST.md` (Ukrainian): why this topic (the trend numbers), the psychology source, the caption.
10. **Commit and push** (`git add` only the reel's sources, voice, align.json, cover, final mp4, caption, POST.md;
    never bed.wav/sfx.wav/cartoon_video.mp4). Instagram downloads the files from GitHub, so push BEFORE publishing.
11. **Publish:** `python3 autopilot/ig.py publish reelNN/reelNN_<slug>.mp4 reelNN/cover_reelNN.png reelNN/caption.txt "<topic>"`
    then commit and push `autopilot/log.json`.
12. **Final message (Ukrainian, short):** the topic and why, the Instagram link, and anything that failed.

## Afternoon job (≈14:00 Kyiv): report
1. Setup as above, `git pull`.
2. `python3 autopilot/ig.py stats`, then commit and push `autopilot/log.json` and `autopilot/followers.json`.
3. Final message in Ukrainian, phone-friendly, under 120 words:
   - last night's reel: views, average watch time (s), shares, saves, likes, comments, new followers since yesterday;
   - comparison with the channel's average and the best reel so far;
   - one concrete conclusion for the next reel (what to repeat, what to change).
   Write the conclusion also into `autopilot/LESSONS.md` (append, dated) so the night job can use it.
