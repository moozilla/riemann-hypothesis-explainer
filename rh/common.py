"""Shared style + narration-sync framework. Every scene subclasses NarratedScene."""
import os, json, functools
from contextlib import contextmanager
from manim import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["PATH"] = os.path.join(ROOT, "tools/TinyTeX/bin/universal-darwin") + os.pathsep + os.environ["PATH"]

# ---- palette (dark, 3b1b-like). Use these names, not raw hex, so the film is coherent.
BG = "#0b0f1a"
INK = "#edf2f4"       # default text / lines
MUTED = "#7d8799"     # secondary text, axes, composites
DIM = "#3a4256"       # very faint structure
PRIME = "#ffd166"     # primes are always gold
ZERO = "#4cc9f0"      # zeta zeros / critical line are always cyan
BAD = "#ef476f"       # forbidden / off-line / error
GOOD = "#06d6a0"      # proved / ok
LIFT = "#b388ff"      # theta lifts / symmetry / tower
WARM = "#ff9f1c"      # secondary accent (cost, size)
FONT = "Avenir Next"
MONO = "Menlo"

config.background_color = BG
Text.set_default(font=FONT, color=INK)
MathTex.set_default(color=INK)
Tex.set_default(color=INK)

DUR_PATH = os.path.join(ROOT, "build/durations.json")
AUDIO_DIR = os.path.join(ROOT, "build/audio")
NO_AUDIO = bool(os.environ.get("RH_NO_AUDIO"))


def T(s, size=36, color=INK, weight=NORMAL, **kw):
    """Plain text label in the house font."""
    return Text(s, font_size=size, color=color, weight=weight, **kw)


def M(*s, size=44, color=INK, **kw):
    """Math (LaTeX)."""
    return MathTex(*s, font_size=size, color=color, **kw)


class NarratedScene(Scene):
    """Subclass, set sid = 's05', and wrap each beat's animations in `with self.beat('a'):`.

    On leaving the block the scene waits until that beat's narration has finished (plus a short
    breath), so picture and voice stay locked no matter which voice is used. Animations inside a
    beat must total LESS than self.dur(letter); overruns are printed and logged to build/overruns.log.
    """
    sid = None
    breath = 0.35      # silence after each beat
    last_hold = 0.6    # extra hold at the end of the scene

    def setup(self):
        self.camera.background_color = BG
        self._durs = json.load(open(DUR_PATH))
        import sys
        if ROOT not in sys.path: sys.path.insert(0, ROOT)
        from script import beats
        self._texts = {k: b["text"] for k, _, b in beats()}

    def dur(self, letter):
        return self._durs[self.sid + letter]

    def now(self):
        return self.renderer.time

    @contextmanager
    def beat(self, letter, breath=None):
        key = self.sid + letter
        d = self._durs[key]
        start = self.now()
        if not NO_AUDIO:
            self.add_sound(os.path.join(AUDIO_DIR, key + ".wav"))
        self._beat_start, self._beat_dur = start, d
        self._beat_text = self._texts[key]
        yield d
        used = self.now() - start
        total = d + (self.breath if breath is None else breath)
        if used > d + 0.05:
            msg = f"OVERRUN {key}: animations {used:.2f}s > narration {d:.2f}s"
            print(msg)
            with open(os.path.join(ROOT, "build/overruns.log"), "a") as f:
                f.write(msg + "\n")
        if total - used > 1 / 30:
            self.wait(total - used)

    def left(self):
        """Seconds of narration left in the current beat (handy for 'fill the rest' animations)."""
        return max(0.0, self._beat_dur - (self.now() - self._beat_start))

    def wait_until(self, t):
        """Wait until t seconds after the start of the current beat (to hit a spoken word)."""
        dt = t - (self.now() - self._beat_start)
        if dt > 1 / 30:
            self.wait(dt)

    def cue(self, phrase):
        """Estimated time (seconds into the current beat) at which `phrase` is spoken.
        Linear in character position — good to about +-0.5s. phrase must occur in the beat text."""
        text = self._beat_text
        i = text.lower().find(phrase.lower())
        if i < 0:
            raise ValueError(f"cue {phrase!r} not in beat text: {text!r}")
        return self._beat_dur * i / max(1, len(text))

    def at(self, phrase, lead=0.25):
        """Wait until just before `phrase` is spoken in the current beat."""
        self.wait_until(self.cue(phrase) - lead)

    def finish(self):
        self.wait(self.last_hold)
