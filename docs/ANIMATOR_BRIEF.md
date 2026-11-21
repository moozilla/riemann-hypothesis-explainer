# Animator brief — "The Riemann Hypothesis: what it says, and how the proof works"

You are animating part of a ~20 minute explainer in the style of 3Blue1Brown, for an educated layperson
(someone who has seen some college math but whose eyes glaze over at notation). The narration is
already written and recorded; your job is to make pictures that carry the idea so well the viewer could
almost follow with the sound off.

## Files
- `script.py` — the narration, the single source of truth. Each scene has beats; each beat has `text`
  (spoken verbatim) and `visual` (direction — treat it as intent, improve on it freely, but keep what the
  narration refers to on screen when it is said). Read the WHOLE script once so you know the arc and what
  comes before/after your scenes.
- `rh/common.py` — palette, fonts, `T()` text, `M()` math, and `NarratedScene` (audio sync). READ IT.
- `rh/motifs.py` — shared motifs (critical strip, balance scale, lift tower, roadmap, number token,
  primes, zeta zeros). If your scene shows one of these, USE the shared builder so the film is coherent.
  Do NOT edit files in `rh/`; if you need another helper put it in your own scene file.
- `scenes/s02.py` — a working example of the conventions (rough; it shows the mechanics, not the quality bar).
- `build/durations.json` — seconds of narration per beat key (e.g. `s05c`).

## Conventions (must follow)
- One file per scene: `scenes/sNN.py`, one class `SNN(NarratedScene)` with `sid = "sNN"`. Start the file with the
  same two import lines as `scenes/s02.py`.
- Every beat: `with self.beat("a") as d:` … animations …. On exit the framework waits for the narration
  to end. Animations inside a beat must total LESS than `d` seconds — an `OVERRUN` line is printed otherwise
  and you must fix it (compute run_times from `d`, don't hard-code long ones).
- Sync to the words: `self.at("phrase")` waits until just before that phrase is spoken in the current beat;
  `self.wait_until(seconds)`, `self.left()` (narration seconds remaining) are also available.
- End `construct` with `self.finish()`. Scenes are concatenated with hard cuts, so start from an empty
  screen and bring things in quickly (first motion within ~0.3s), and end clean (fade out the last ~0.5s is
  fine but not required).
- Colors: primes are always `PRIME` (gold); zeta zeros / the critical line always `ZERO` (cyan);
  forbidden/off-line/bad `BAD`; proved/ok `GOOD`; theta lifts/symmetry `LIFT`; cost/size `WARM`;
  secondary `MUTED`/`DIM`. Use the names from `rh.common`.
- Text: `T("…")` (Avenir Next) for words, `M(r"…")` for math (LaTeX works). Keep on-screen words FEW and
  large (font_size ≥ 24 at 1080p for anything meant to be read). No bullet lists, no paragraphs, no
  slide-like title+text layouts. Spoken numbers that matter should appear on screen.
- Frame is 14.2 × 8 units; keep everything inside ±6.6 × ±3.6. Use the frame — don't leave the picture
  small in the middle.

## Quality bar
- Motion carries meaning: prefer transforming one thing into the next over fade-out/fade-in. Use
  ValueTrackers / always_redraw / updaters for continuous change. Real math, really computed
  (numpy / mpmath / sympy are installed) — no fake squiggles where a true curve exists.
- Never leave the screen static for more than ~3 seconds: if the narration is long, stage the reveal across
  it, or add gentle purposeful motion (a tracker sweeping, a highlight travelling, slow camera-free drift).
- No overlapping text, nothing clipped at the frame edge, no leftover objects from an earlier beat
  cluttering a later one. Good spacing and alignment. Lines 2–4 px, consistent.
- Honest but not pedantic: the audience is lay; no caveats, no hedging text on screen.

## Workflow (do all of it)
Run everything from the project root (`rh-explainer/`). Use the venv: `.venv/bin/manim`.
1. Low-quality render with sound: `.venv/bin/manim -ql scenes/sNN.py SNN 2>&1 | grep -E "OVERRUN|Error|Traceback|line " `
   (`RH_NO_AUDIO=1` in front skips audio muxing if you only want pictures.)
2. Contact sheet: `.venv/bin/python scripts/sheet.py sNN 16` → `build/frames/sNN_sheet.png`; optional
   `t0 t1` args zoom into a time window (`sheet.py sNN 12 20 35`). LOOK at it with the Read tool. For a
   single full-res frame: `ffmpeg -v error -y -ss T -i media/videos/sNN/480p15/SNN.mp4 -frames:v 1 build/frames/sNN_T.png`.
3. Critique like a director: Is it clear? Beautiful? Anything overlapping, clipped, tiny, off-palette,
   static too long, or out of sync with the words? Fix and repeat. Expect at least 3 render→look→fix rounds
   per scene. Check transitions between beats specifically (sample frames just after each beat starts).
4. Finish with zero OVERRUN lines and a clean final `-ql` render of each scene. Do NOT run high-quality
   (`-qh`) renders — the director does the final renders. Do not touch other agents' scene files, `rh/`,
   `script.py`, or `build/audio`.
5. Final report (short): per scene, one line on what is on screen, plus anything you are unhappy with or
   that the director should double-check. No need to paste code.
