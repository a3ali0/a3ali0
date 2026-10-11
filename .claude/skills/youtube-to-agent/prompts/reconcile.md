# Reconcile prompt (step 05)

Run after both `notes/claude-pass.md` and `notes/gemini-pass.md` exist. Output is `SPEC.md`.

```xml
<role>You are reconciling two independent readings of the same build tutorial into one spec. One reading came from frames and a transcript you saw yourself. The other came from Gemini reading the video natively. Neither is authoritative.</role>

<context>
Reading A: notes/claude-pass.md (yours)
Reading B: notes/gemini-pass.md (Gemini, two samples)
What I am building: [the skill or script you want at the end]
</context>

<task>Write SPEC.md. Every single line carries one of three labels.</task>

<process>
1. CONFIRMED. Both readings agree. Build on it without further checking.
2. SINGLE SOURCE. Only one reading has it. Keep it, label it, and tell me which reading it came from.
3. CONFLICT. The readings disagree. Do not average them and do not pick the more confident one. List both versions, then go back and look at the specific frames that settle it, and say what you saw.
</process>

<rules>
- Delete every timestamp, duration and count from both readings. Neither reader has a clock, both reconstruct timings, and both are routinely off by whole seconds.
- Keep exact strings. Commands, package names, config keys and error messages stay literal, never paraphrased.
- Flag the archetype trap. If a step reads like it came from documentation rather than from this specific video, it probably did. Both models describe what this KIND of tutorial usually contains, and the distinctive step is exactly what gets normalized away.
- End with an OPEN QUESTIONS list: everything neither reading could see, and everything still labelled CONFLICT.
</rules>
```
