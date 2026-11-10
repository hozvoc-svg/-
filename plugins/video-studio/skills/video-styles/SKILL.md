---
name: video-styles
description: Library of visual styles and camera language for AI video and image generation (Higgsfield, Kling, Veo, Runway, Luma, Sora-type models) and for editing looks — cinematic, 3D animation, anime, claymation, stop-motion, documentary, noir, VHS, cyberpunk, watercolor, isometric, paper cut-out and more. Use when the user asks for a new стиль, look, "не 2D", prompts for video generation, consistent characters across shots, or colour grading / LUT ideas.
---

# Video styles & prompt library / Бібліотека стилів

## Prompt formula (write prompts in English)

```
[SHOT TYPE + CAMERA MOVE], [SUBJECT + ACTION], [SETTING], [STYLE KEYWORDS], [LIGHTING], [COLOUR / GRADE], [LENS / FILM], [MOOD], [MOTION DETAILS]
```
- One main action per clip (4–10 s). Describe motion explicitly: "slowly turns head", "dust drifts".
- For image→video: describe only the **motion and camera**, not the whole image again.
- Negative/avoid list (where supported): `text, watermark, extra fingers, warped faces, flicker`.
- Do not name living artists, studios, franchises or copyrighted characters; describe the look instead.

## Consistency across shots
- Write a **character sheet** once (age, face, hair, outfit, colours, one signature prop) and paste it verbatim into every prompt.
- Generate a reference image first, then use image→video for each shot.
- Lock a **style suffix** (style + lighting + grade + lens) and reuse it for the whole video.

## Camera vocabulary
static locked-off · slow push-in · pull-out reveal · dolly left/right · orbit 180° · crane up · drone fly-over · FPV dive · whip pan · crash zoom · rack focus · handheld shaky · Dutch angle · low-angle hero · top-down overhead · POV · over-the-shoulder · macro extreme close-up · tracking shot following subject · bullet-time freeze · dolly zoom (vertigo).

## Style library

| Style | Style suffix (copy into prompt) | Best for |
|---|---|---|
| **Cinematic realism** | `cinematic film still, anamorphic 35mm lens, shallow depth of field, soft volumetric light, teal and orange grade, subtle film grain` | Stories, ads, travel |
| **Stylized 3D animation** | `stylized 3D animated film look, soft subsurface skin, big expressive eyes, rounded shapes, global illumination, vibrant warm palette` | Kids, mascots, explainers |
| **Claymation** | `claymation stop-motion, handmade plasticine textures, visible fingerprints, slight frame jitter at 12fps, miniature set, soft studio light` | Comedy, brand, cozy |
| **Stop-motion paper cut-out** | `layered paper cut-out animation, construction paper texture, drop shadows between layers, choppy 8fps motion` | Explainers, storybook |
| **Anime cel** | `anime cel-shaded animation, clean line art, flat colour with hard shadows, painted background, dramatic speed lines, impact frames` | Action, drama, hooks |
| **Watercolor / storybook** | `hand-painted watercolor animation, soft bleeding edges, paper grain, pastel palette, gentle parallax` | Fairy tales, calm, kids |
| **Film noir** | `black and white film noir, hard key light, venetian blind shadows, rain, high contrast, 1940s 35mm grain` | Mystery, true crime |
| **VHS / found footage** | `1990s VHS camcorder footage, tracking lines, chroma bleed, timestamp overlay, low-light noise, handheld` | Horror, nostalgia |
| **Cyberpunk neon** | `neon-soaked cyberpunk city at night, wet reflective streets, magenta and cyan, holograms, haze, anamorphic flares` | Tech, gaming, music |
| **Documentary** | `observational documentary, natural light, handheld 24mm, muted realistic colours, candid` | Education, interviews |
| **Isometric 3D diorama** | `isometric miniature diorama, tilt-shift, toy-like materials, soft ambient occlusion, clean pastel background` | Process, business, maps |
| **Low-poly / game** | `low-poly 3D, flat-shaded facets, bright gradient sky, stylized game cinematic` | Gaming, explainers |
| **Retro 80s synthwave** | `1980s synthwave, sunset grid horizon, chrome text, magenta-purple gradient, scanlines` | Music, retro |
| **Macro / product** | `macro product shot, studio softbox, black seamless background, slow rotation, crisp reflections, 100mm macro` | Products, ASMR |
| **Surreal / dreamcore** | `surreal dreamlike scene, impossible architecture, soft haze, pastel light, slow floating camera` | Art, music, hooks |
| **Epic fantasy** | `epic high-fantasy matte painting, god rays, vast scale, golden hour, sweeping crane shot` | Story, gaming |
| **Motion graphics / kinetic type** | build in Remotion / After Effects rather than generate: bold sans type, beat-synced reveals | Lists, quotes, data |

## Colour grade quick picks
teal-orange (blockbuster) · bleach bypass (gritty war/thriller) · warm golden (nostalgia) · cold desaturated blue (horror/drama) · pastel lifted blacks (lifestyle) · high-contrast mono (noir) · neon split-tone (cyberpunk).

## Output
For each shot give: the full prompt, duration, aspect ratio, camera move, and what to cut on. Offer 3 alternative styles if the user hasn't chosen one, each with a one-line reason tied to their genre.
