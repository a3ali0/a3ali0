# YouTube tutorial → agent skill

A two-reader pipeline that turns a build tutorial into a working Claude Code skill:
`/watch` reads frames + transcript, Gemini reads the video natively, and the two
readings are reconciled into a labelled `SPEC.md` (CONFIRMED / SINGLE SOURCE /
CONFLICT) that `skill-creator` builds from.

## Setup (once, ~15 min)

1. **Install `/watch`** (Brad Bonanno, MIT, github.com/bradautomates/claude-video)

   | Where you work | Install |
   | --- | --- |
   | Claude Code | `/plugin marketplace add bradautomates/claude-video` then `/plugin install watch@claude-video` |
   | Codex, Cursor, Copilot, Gemini CLI, … | `npx skills add bradautomates/claude-video -g` |
   | Claude on the web | Download `watch.skill` from the latest release → Settings › Capabilities › Skills › + (turn on *Code execution and file creation* first) |

   Smoke test: `/watch https://youtu.be/dQw4w9WgXcQ what happens at the 30 second mark?`

2. **Gemini key** (the only key in the pipeline, free tier is enough)

   ```bash
   export GEMINI_API_KEY="your-key-here"   # add to ~/.zshrc / ~/.bashrc
   pip install -r requirements.txt
   ```

   Always run `/watch` with `--no-whisper`. For caption-less videos, transcribe
   locally: `pip install faster-whisper && python3 scripts/local_transcribe.py audio.wav`.

3. **Install the skill globally** (optional; it already works inside this repo
   as a project skill):

   ```bash
   ./install.sh
   ```

## Per video (~4 min)

```
/youtube-to-agent <url> [what you want out of it]
```

Or by hand:

| Step | What | Prompt / command |
| --- | --- | --- |
| 03 | Claude pass → `notes/claude-pass.md` | `/watch <url> --detail balanced --no-whisper` + [`prompts/claude-pass.md`](.claude/skills/youtube-to-agent/prompts/claude-pass.md) |
| 04 | Gemini pass → `notes/gemini-pass.md` | `python3 scripts/gemini_review.py "<url>" --samples 2 --end 600 --focus "…" > notes/gemini-pass.md` |
| 05 | Reconcile → `SPEC.md` | [`prompts/reconcile.md`](.claude/skills/youtube-to-agent/prompts/reconcile.md) |
| 06 | Build + run once | [`prompts/build.md`](.claude/skills/youtube-to-agent/prompts/build.md) |

Write the Claude pass **before** reading Gemini's, or the second opinion stops being one.

## Picking `/watch --detail`

Measured on one 49-minute 720p screen recording; treat as orders of magnitude.

| Mode | Frames | Extraction | Image tokens | Use when |
| --- | --- | --- | --- | --- |
| `transcript` | 0 | ~4.5 s | 0 | Talking, not typing |
| `efficient` | 50 | ~0.5 s | ~9.8k | First look at a long screen recording |
| `balanced` | 100 | ~20.9 s | ~19.7k | Default, need to read the screen |
| `token-burner` | 116 | ~21.0 s | ~22.8k | High motion, 100 frames misses cuts |

`--resolution 1024` ≈ 4× image tokens per frame: pair it with `efficient` or a
narrow `--start/--end` window. Scope both readers to the same window
(`/watch --start 12:30 --end 18:00` ↔ `gemini_review.py --start 750 --end 1080`).

## Rules of thumb

- **Keep the nouns, throw away the numbers.** Names, commands and errors are evidence; timestamps, durations and counts are decoration.
- **Archetype trap.** Models report what this *kind* of video usually contains. The fluent, documentation-sounding line is the one to check first.
- **Readers disagree on everything?** The window was too wide. Narrow it and rerun both.
- **Public videos only.** Private/unlisted URLs fail for both readers.
- **Model names move.** If all four models in `MODEL_CHAIN` fail, check the current Gemini model list.

## Layout

```
.claude/skills/youtube-to-agent/
  SKILL.md                    the one-command pipeline
  prompts/                    claude-pass, reconcile, build
  scripts/gemini_review.py    Gemini second-opinion pass
  scripts/local_transcribe.py faster-whisper fallback
scripts/                      symlinks to the above
notes/                        per-run readings (git-ignored)
install.sh                    copy the skill into ~/.claude/skills
```

Credits: `/watch` by Brad Bonanno (MIT), built on yt-dlp and ffmpeg. `skill-creator` is Anthropic's (anthropics/skills).
