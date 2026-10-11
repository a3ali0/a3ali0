# Claude pass prompt (step 03)

Send this after `/watch` has read the frames. Fill in the two bracketed lines.
Save the answer to `notes/claude-pass.md` and do NOT open Gemini's version first.

```xml
<role>You have just watched a build tutorial. You are now writing the spec another agent will build from. That agent cannot watch video, so your text is the only thing it gets.</role>

<context>
What I want out of this video: [the whole build / just the section on X / only whether the approach is sound]
What I am building it into: [e.g. a Claude Code skill, a script, a repo]
</context>

<task>Write the spec in exactly the six sections below, in this order.</task>

<process>
1. WHAT IS BEING BUILT. One paragraph, the actual outcome and not the pitch.
2. STACK AND PREREQUISITES. Every tool, package, model, service and account shown on screen or named out loud. Exact names and versions where visible. Mark anything that costs money.
3. COMMANDS AND CONFIG, VERBATIM. Every command typed, every file path, every env var, every config value you can actually read in a frame. Quote it exactly. Where a value is blurred, truncated or scrolled past, write UNREADABLE instead of guessing.
4. THE BUILD ORDER. The steps in the order performed, including anything undone or redone. Say plainly where the video cuts ahead to a finished state.
5. GOTCHAS. Every error hit on screen, every warning said out loud, every "make sure you" aside.
6. WHAT THE VIDEO DOES NOT SHOW. Setup done off camera, values pasted from nowhere, steps asserted but never demonstrated.
</process>

<rules>
- Describe only what is in THIS video. If something you would expect from a tutorial like this is missing, say it is missing rather than filling it in from what you already know.
- The exact string on screen always beats your paraphrase of it.
- Cite the frame timestamp for anything in section 3, so I can go back and look.
</rules>
```
