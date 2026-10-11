---
name: youtube-to-agent
description: Turn a YouTube tutorial into a working Claude Code skill or agent. Watches the video with /watch, gets an independent second read from Gemini's native video understanding, reconciles the two into one build spec, then hands that spec to skill-creator. Use when the user pastes a YouTube tutorial link and says "build this", "turn this into a skill", or "make an agent out of this".
argument-hint: "<youtube-url> [what you want out of it]"
allowed-tools: Bash, Read, Write, Skill, AskUserQuestion
license: MIT
user-invocable: true
---

# youtube-to-agent

Two independent readers watch the same video. /watch gives you frames plus a
timestamped transcript inside your own context. Gemini reads the video natively
on Google's side and returns a written spec. They are wrong in different ways,
and the disagreement is the useful part.

Files bundled with this skill (paths relative to this SKILL.md's folder):

- `scripts/gemini_review.py`: the Gemini pass
- `scripts/local_transcribe.py`: local faster-whisper transcript for caption-less videos
- `prompts/claude-pass.md`, `prompts/reconcile.md`, `prompts/build.md`: the exact prompts for steps 2, 4 and 5

Work in a fresh folder per video (e.g. `builds/<slug>/`) with a `notes/` subfolder.

## Step 0: Preflight

- `/watch` must be installed (`/plugin marketplace add bradautomates/claude-video`
  then `/plugin install watch@claude-video`). If it is missing, stop and say so.
- `GEMINI_API_KEY` set and `python3 -c "import google.genai"` succeeds. If not,
  tell the user (free key: https://aistudio.google.com/apikey, `pip install google-genai`)
  and offer to continue Claude-only, marking everything SINGLE SOURCE.

## Step 1: Scope before spending anything

Ask what the user actually wants if they did not say. Check the duration first.
Anything over about 20 minutes gets scoped to a section unless they insist.
Use the same window for both readers.

## Step 2: The Claude pass

Run /watch. Pick the detail mode on purpose: `transcript` for talking heads,
`efficient` for a first look at a long screen recording, `balanced` when you need
to read the screen, `--resolution 1024` for terminal and code work. Use --start
and --end whenever a section was named. Always pass --no-whisper: transcription
runs locally in this pipeline, never through a paid API.

Read every frame path. Then answer the prompt in `prompts/claude-pass.md` and
write it to notes/claude-pass.md BEFORE looking at Gemini's answer, or you will
anchor to it.

## Step 3: The Gemini pass

    python3 <skill-dir>/scripts/gemini_review.py "<url>" --samples 2 \
      --start <seconds> --end <seconds> \
      --focus "<what the user asked for>" > notes/gemini-pass.md

Two samples on purpose. A claim in both samples is worth something. A claim in
one is the model guessing.

## Step 4: Reconcile into SPEC.md

Follow `prompts/reconcile.md`. Three labels on every line. CONFIRMED means both
agree, build on it. SINGLE SOURCE means one reader only, keep it and mark it.
CONFLICT means go look at the frames yourself and settle it, never average two
guesses.

Throw away every timestamp, duration and count. Keep exact strings. Watch for the
archetype trap: a step that reads like documentation rather than like this video
probably came from training data. The tell is fluency.

## Step 5: Build and verify

Hand SPEC.md to skill-creator with the text in `prompts/build.md`. Say plainly
that it came from a video and that SINGLE SOURCE lines are unverified. Then run
the new skill once on a real input and fix what breaks. A skill built from a
tutorial and never executed is a summary of a video, not a tool. Copy SPEC.md
and notes/ into the new skill's folder as provenance.

## Failure modes

- No captions: /watch returns frames only. Gemini still hears the audio, so the
  spoken content is covered. Say so in the spec, and run
  `scripts/local_transcribe.py` if you need the transcript on disk.
- Gemini 429s on every model: free tier quota is spent. Run the Claude pass alone
  and mark the whole spec SINGLE SOURCE.
- The two readers disagree about almost everything: the window was too wide.
  Narrow to a section and rerun both.
- Private or unlisted video: neither reader can reach it. Stop and say so.
