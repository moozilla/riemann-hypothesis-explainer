# riemann-hypothesis-explainer

An 18-minute animated explainer of the Riemann Hypothesis and of how Levent Alpöge's November 2026 Lean proof of it works, aimed at an educated layperson: no notation you have to decode, and every idea gets a picture.

**[Watch / download the video](assets/riemann_hypothesis_explainer.mp4)** (1080p, 17m50s, 79 MB)

- [explanation.md](explanation.md): the proof strategy in writing, about a five-minute read
- [transcript.md](transcript.md): the full narration, scene by scene

The whole thing was written, animated and narrated by Claude in one sitting, the day after the announcement. It is a best-effort reading of very fresh material, not an authoritative account. It takes the proof as presented and does not try to verify it.

## What it covers

| Act | Scenes | Content |
| --- | --- | --- |
| Prologue | 1 | Are the primes static, or music? |
| I · The primes | 2–4 | The sieve, counting primes, the leftover wobble |
| II · The zeta function | 5–9 | Euler's product, complex numbers that spin, the zeros and the critical line, primes as a sum of waves, Dirichlet L-functions |
| III · The clue | 10–12 | Curves over finite fields, Stepanov's multiplicity trick, why it doesn't carry over to the integers |
| IV · The proof | 13–20 | A one-sided √X ceiling and Landau's argument, divisibility versus size, theta lifts, the tower of √X lifts, the two-thirds wall, the weakened Vandiver statement |
| V · The proof as an object | 21 | 17 million lines of Lean and the independent checkers |
| Epilogue | 22 | The whole argument in one breath |

## Sources

- Levent Alpöge, [remark on the proof](https://alpo.ge/remark.pdf)
- Terence Tao, [blog post of 20 November 2026](https://terrytao.wordpress.com/2026/11/20/unforced-euler-singularity-unforced-navier-stokes-singularity-and-the-generalized-riemann-hypothesis/) and the Lean Zulip thread it links, where people are reconstructing the argument from the Lean source

## How it was made

- **Animation:** [Manim Community](https://www.manim.community/) 0.22.1 with LaTeX. The math on screen is computed, not drawn by hand: the prime staircase is rebuilt from actual zeta zeros (via `mpmath`), and the point counts on curves are real.
- **Narration:** [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M), voice `af_heart`, run locally. No paid services.
- **Sync:** the narration is generated first, one clip per beat. Each scene reads the clip lengths and times its animations to them.

## Layout

```
script.py        narration and visual notes for all 22 scenes (the source of truth)
scenes/          one Manim scene per file, s01.py … s22.py
rh/common.py     palette, text helpers, NarratedScene (audio-locked timing)
rh/motifs.py     shared visuals: critical strip, balance scale, lift tower, roadmap
scripts/tts.py   generate narration audio and build/durations.json
scripts/build.sh render every scene and assemble the final video
scripts/sheet.py contact sheets of a rendered scene, for checking frames
docs/            the brief the animator agents worked from
```

## Rebuilding

Developed on macOS (Apple silicon) with Python 3.12. You need `ffmpeg`, `espeak-ng`, and a LaTeX install with `dvisvgm` (TeX Live, MacTeX or TinyTeX).

```bash
brew install ffmpeg espeak-ng
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Generate the narration (downloads the Kokoro weights on first run), then render and assemble:

```bash
PYTORCH_ENABLE_MPS_FALLBACK=1 .venv/bin/python scripts/tts.py af_heart 1.0
scripts/build.sh
```

The result lands in `build/riemann_hypothesis_explainer.mp4`. A full render takes roughly 15 minutes.

Notes:

- `scripts/tts.py` points Kokoro at Homebrew's `espeak-ng` (`/opt/homebrew/...`). Change the two paths at the top on other systems.
- Text uses the Avenir Next and Menlo fonts, which ship with macOS. Change `FONT` and `MONO` in `rh/common.py` elsewhere.
- To re-render a single scene: `scripts/build.sh 3 s14`.
- To change the narration, edit `script.py`, re-run `tts.py` for the affected scene (`... tts.py af_heart 1.0 s14`), then re-render it.
