# video-studio — скіли Claude для відео

П'ять скілів, які Claude використовує автоматично, коли мова йде про відео:

| Скіл | Що робить |
|---|---|
| `video-hooks` | Хуки на перші 1–3 с: кадр + звук + текст, 12 формул, оцінка 0–12 |
| `short-form-script` | Сценарій і розкадровка Shorts / Reels / TikTok / YouTube з таймінгами |
| `video-styles` | 17 візуальних стилів (кіно, 3D, аніме, клеймейшн, нуар, VHS, кіберпанк…) + промпти для AI-відео |
| `genre-playbooks` | Як монтувати 13 жанрів: хорор, комедія, освіта, реклама, сторітелінг, ASMR, геймінг… |
| `video-pipeline` | Повний цикл: vidIQ → сценарій → Higgsfield → ElevenLabs → ffmpeg (субтитри, звук, експорт) |

## Як увімкнути в інших проєктах

**Claude Code (термінал або claude.ai/code):** напишіть у чаті
```
/plugin marketplace add hozvoc-svg/-
/plugin install video-studio@hozvoc-video
```
Або скопіюйте файл `.claude/settings.json` з цього репозиторію в будь-який інший проєкт — плагін підключиться сам.

**Звичайний чат claude.ai:** Settings → Capabilities → Skills → Upload skill, і завантажте по одному ZIP-файлу з папки `zips/`.
