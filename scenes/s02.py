import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *
import functools


@functools.lru_cache(None)
def pauses(key, min_gap=0.12):
    """Silences inside a narration clip, as (start, end) seconds — sentence/comma boundaries, used to
    hit spoken words more precisely than the linear `cue` estimate. Trailing silence is dropped."""
    import scipy.io.wavfile as wf
    sr, a = wf.read(os.path.join(AUDIO_DIR, key + ".wav"))
    a = a.astype(float)
    if a.ndim > 1: a = a.mean(1)
    hop = int(sr * 0.01)
    e = np.sqrt(np.convolve(a ** 2, np.ones(hop) / hop, "valid")[::hop])
    q = e < e.max() * 0.03
    out, i = [], 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if (j - i) / 100 >= min_gap and j < len(q) - 2: out.append((i / 100, j / 100))
            i = j
        else:
            i += 1
    return out


class S02(NarratedScene):
    sid = "s02"

    def construct(self):
        N, cols = 128, 16
        nums = VGroup(*[M(str(n), size=38) for n in range(1, N + 1)])
        xs, ys = np.linspace(-6.05, 6.05, cols), np.linspace(3.2, -2.75, N // cols)
        for i, m in enumerate(nums):
            m.move_to(RIGHT * xs[i % cols] + UP * ys[i // cols])
        ps = primes_upto(N)
        cell = lambda n: nums[n - 1]
        dead = set()

        # ---------------------------------------------------------------- a: the sieve
        with self.beat("a") as d:
            pz = pauses("s02a")
            if len(pz) >= 6:
                starts = [pz[k][1] for k in range(1, 5)] + [pz[5][1]]
            else:
                starts = [self.cue(w) for w in ("cross out", "then every", "then five", "then seven", "whatever")]
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.12) for m in nums], lag_ratio=0.025, run_time=min(2.4, starts[0] - 0.6)))
            self.play(cell(1).animate.set_opacity(0.25), run_time=0.3)
            dead.add(1)
            for i, p in enumerate([2, 3, 5, 7]):
                self.wait_until(starts[i])
                avail = starts[i + 1] - starts[i] - 0.12
                ring = Circle(radius=0.36, color=PRIME, stroke_width=3).move_to(cell(p))
                self.play(Create(ring), cell(p).animate.set_color(PRIME).scale(1.15), run_time=0.3)
                mult = [k for k in range(2 * p, N + 1, p) if k not in dead]
                dead.update(mult)
                sweep = min(1.35, avail - 0.3)
                # a fast travelling wave: each multiple flashes red, then sinks to a dim ghost
                self.play(LaggedStart(*[AnimationGroup(cell(k).animate.set_color(DIM),
                                                       FadeOut(cell(k).copy().set_color(BAD), scale=1.7))
                                        for k in mult], lag_ratio=min(0.12, 1.0 / max(1, len(mult))), run_time=sweep),
                          FadeOut(ring, run_time=sweep))
            self.wait_until(starts[4])
            glows = VGroup(*[Circle(radius=0.3, stroke_width=0, fill_color=PRIME, fill_opacity=0.14).move_to(cell(p)) for p in ps])
            rest = [p for p in ps if p > 7]
            # 121 = 11 x 11 is the one composite here that 2, 3, 5, 7 miss: 11 takes it out
            self.play(LaggedStart(*[cell(p).animate.set_color(PRIME).scale(1.15) for p in rest], lag_ratio=0.04, run_time=min(1.3, self.left() - 0.1)),
                      FadeIn(glows, run_time=1.0),
                      Succession(Wait(0.5), AnimationGroup(cell(121).animate.set_color(DIM), FadeOut(cell(121).copy().set_color(BAD), scale=1.7), run_time=0.4)))

        # ---------------------------------------------------------------- b: twins and deserts
        with self.beat("b") as d:
            pz = pauses("s02b")
            t_side = pz[0][1] if len(pz) >= 4 else self.cue("sometimes two")
            t_desert = pz[2][1] if len(pz) >= 4 else self.cue("sometimes there")
            t_close = pz[3][1] if len(pz) >= 4 else self.cue("up close")
            # "Look at the survivors": a gentle ripple across the primes
            self.play(LaggedStart(*[Indicate(cell(p), color=PRIME, scale_factor=1.25) for p in ps], lag_ratio=0.03, run_time=min(1.0, t_side - 0.1)))
            self.wait_until(t_side)
            twin = SurroundingRectangle(VGroup(cell(11), cell(13)), color=PRIME, buff=0.13, corner_radius=0.18, stroke_width=3)
            self.play(Create(twin), run_time=0.6)
            others = [(17, 19), (29, 31), (41, 43), (59, 61), (71, 73), (101, 103)]
            obox = VGroup(*[SurroundingRectangle(VGroup(cell(a), cell(b)), color=PRIME, buff=0.13, corner_radius=0.18, stroke_width=2).set_stroke(opacity=0.5)
                            for a, b in others])
            self.play(LaggedStart(*[Create(b) for b in obox], lag_ratio=0.25, run_time=1.4))
            self.wait_until(t_desert)
            desert = VGroup(*[cell(k) for k in range(114, 127)])
            box = SurroundingRectangle(desert, color=BAD, buff=0.13, corner_radius=0.18, stroke_width=3)
            box_l = M(r"113 \;\longrightarrow\; 127", size=38, color=BAD).next_to(box, DOWN, buff=0.14)
            box_bg = BackgroundRectangle(box_l, color=BG, fill_opacity=0.9, buff=0.08)
            self.play(FadeOut(twin), FadeOut(obox), Create(box), FadeIn(box_bg), FadeIn(box_l, shift=UP * 0.1), cell(113).animate.scale(1.2), cell(127).animate.scale(1.2), run_time=0.8)
            self.play(LaggedStart(*[c.animate(rate_func=there_and_back).set_color(BAD) for c in desert], lag_ratio=0.12, run_time=1.4))
            self.wait_until(t_close)
            self.play(FadeOut(box), FadeOut(box_l), FadeOut(box_bg), cell(113).animate.scale(1 / 1.2), cell(127).animate.scale(1 / 1.2), run_time=0.5)
            # no pattern: primes flicker in a scattered order
            order = list(ps); np.random.default_rng(3).shuffle(order)
            self.play(LaggedStart(*[Indicate(cell(p), color=INK, scale_factor=1.2) for p in order], lag_ratio=0.05, run_time=min(1.0, self.left() - 0.1)))

        # ---------------------------------------------------------------- c: line them up
        with self.beat("c") as d:
            pz = pauses("s02c")
            t_q = pz[1][1] if len(pz) >= 2 else self.cue("how many")
            line = NumberLine(x_range=[0, N, 10], length=12.6, color=MUTED, stroke_width=3, include_numbers=True, font_size=28,
                              numbers_to_include=range(0, N + 1, 20)).move_to(DOWN * 3.0)
            line.numbers.set_color(MUTED)
            comps = VGroup(*[cell(n) for n in range(1, N + 1) if n not in ps])
            dots = VGroup(*[Dot(line.n2p(p), radius=0.075, color=PRIME) for p in ps])
            pv = VGroup(*[cell(p) for p in ps])
            self.play(FadeOut(comps, run_time=0.6), FadeOut(glows, run_time=0.6), pv.animate(run_time=0.6).shift(UP * 0.35).set_color(PRIME))
            self.play(Create(line), run_time=0.6)
            self.play(LaggedStart(*[ReplacementTransform(cell(p), dot, path_arc=-0.4) for p, dot in zip(ps, dots)], lag_ratio=0.04, run_time=min(2.0, t_q - 1.5)))
            q = T("How many are there?", size=56, weight=MEDIUM).move_to(UP * 0.7)
            self.wait_until(t_q - 0.15)
            self.play(FadeIn(q, shift=UP * 0.15), LaggedStart(*[Indicate(dt, color=PRIME, scale_factor=1.8) for dt in dots], lag_ratio=0.05), run_time=min(1.2, self.left() - 0.05))
        self.finish()
