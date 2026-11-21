import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *
import functools


@functools.lru_cache(None)
def pauses(key, min_gap=0.12):
    """Silences inside a narration clip, as (start, end) seconds (sentence / comma boundaries).
    Used to land animations on spoken words more precisely than the linear `cue`. Trailing silence dropped."""
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


def pz_or(key, n, fallback):
    """Pause list if it has the expected shape, else None (caller falls back to cue())."""
    p = pauses(key)
    return p if len(p) >= n else None


X0, X1 = -6.3, 6.3          # number-line extent on screen
PR = np.array(primes_upto(20000))


def molecule(n, factors, center):
    """A composite drawn as a molecule of prime 'atoms' joined by bonds."""
    k = len(factors)
    if k == 2:
        pos = [LEFT * 0.55, RIGHT * 0.55]
    else:
        r = {3: 0.62, 4: 0.75, 5: 0.85, 6: 0.95}[k]
        pos = [r * np.array([np.cos(a), np.sin(a), 0]) for a in PI / 2 + TAU * np.arange(k) / k]
    atoms = VGroup()
    for p, q in zip(factors, pos):
        c = Circle(radius=0.33, stroke_color=PRIME, stroke_width=3, fill_color=BG, fill_opacity=1)
        glow = Circle(radius=0.45, stroke_width=0, fill_color=PRIME, fill_opacity=0.12)
        lab = M(str(p), size=38, color=PRIME)
        atoms.add(VGroup(glow, c, lab).move_to(center + q))
    bonds = VGroup()
    idx = [(0, 1)] if k == 2 else [(i, (i + 1) % k) for i in range(k)]
    for i, j in idx:
        a, b = atoms[i].get_center(), atoms[j].get_center()
        u = (b - a) / np.linalg.norm(b - a)
        bonds.add(Line(a + u * 0.33, b - u * 0.33).set_stroke(MUTED, 3))
    return atoms, bonds


class S01(NarratedScene):
    sid = "s01"

    def construct(self):
        # ---- the prime "barcode": one gold tick per prime, drawn from trackers so the same object can
        # be the 0..32 number line, a zoomed-out scrolling strip, and the source of the waves.
        W = ValueTracker(20.0)        # width of the visible window (in integers)
        off = ValueTracker(0.0)       # left end of the window
        reveal = ValueTracker(1.0)    # only primes <= reveal are drawn
        yc = ValueTracker(-0.3)       # vertical centre of the strip
        hh = ValueTracker(0.42)       # tick height
        op = ValueTracker(1.0)        # opacity

        def xmap(n):
            return X0 + (np.asarray(n, dtype=float) - off.get_value()) / W.get_value() * (X1 - X0)

        def barcode():
            w, o = W.get_value(), off.get_value()
            ps = PR[(PR >= o) & (PR <= o + w) & (PR <= reveal.get_value())]
            xs = xmap(ps)
            y, h = yc.get_value(), hh.get_value()
            sw = float(np.clip(4.5 - 2.0 * np.log10(w / 20 + 1e-9), 1.6, 4.5))
            g = VGroup(*[Line([x, y - h / 2, 0], [x, y + h / 2, 0]) for x in xs])
            return g.set_stroke(PRIME, sw, opacity=op.get_value())

        bars = always_redraw(barcode)
        axis = Line(LEFT * 6.6, RIGHT * 6.6).set_stroke(MUTED, 3)
        axis.add_updater(lambda m: m.move_to(UP * yc.get_value()).set_stroke(opacity=0.9 * op.get_value()))
        comps = [n for n in range(1, 21) if n not in set(PR[:20].tolist())]
        cdots = VGroup(*[Dot([float(xmap(n)), -0.3, 0], radius=0.065, color=MUTED) for n in comps])
        pnums = {p: M(str(p), size=56, color=PRIME).move_to([float(xmap(p)), 0.45, 0]) for p in PR[PR <= 20]}
        glows = {p: Circle(radius=0.26, stroke_width=0, fill_color=PRIME, fill_opacity=0.13).move_to(pnums[p]) for p in pnums}

        # ---------------------------------------------------------------- a: the primes appear
        with self.beat("a") as d:
            pz = pz_or("s01a", 3, None)
            t2 = pz[0][1] if pz else self.cue("two")
            t3 = pz[1][1] if pz else self.cue("three")
            t_rest = pz[2][0] if pz else self.cue("numbers that")
            self.add(bars)
            self.play(Create(axis), LaggedStart(*[FadeIn(c, scale=0.3) for c in cdots], lag_ratio=0.05), run_time=1.3)
            times = [t2, t3] + list(np.linspace(t3, t_rest - 0.25, 4)[1:])   # 2, 3, 5, 7, 11
            for p, t in zip([2, 3, 5, 7, 11], times):
                self.wait_until(t - 0.1)
                reveal.set_value(p)
                self.play(FadeIn(pnums[p], shift=UP * 0.2, scale=1.3), FadeIn(glows[p], scale=0.4), run_time=0.3)
            rest = [p for p in pnums if p > 11]
            self.play(LaggedStart(*[AnimationGroup(FadeIn(pnums[p], shift=UP * 0.2), FadeIn(glows[p])) for p in rest], lag_ratio=0.35),
                      reveal.animate.set_value(20), run_time=0.8, rate_func=linear)
            reveal.set_value(1e9)
            # "can't be broken into smaller pieces": a soft shimmer along the primes
            self.play(LaggedStart(*[Indicate(pnums[p], color=PRIME, scale_factor=1.18) for p in pnums], lag_ratio=0.12),
                      run_time=min(1.8, self.left() - 0.1))

        # ---------------------------------------------------------------- b: atoms of arithmetic
        line_grp = VGroup(cdots, *pnums.values(), *glows.values())
        with self.beat("b") as d:
            pz = pz_or("s01b", 2, None)
            t_every = pz[0][1] if pz else self.cue("every whole")
            t_one = pz[1][1] if pz else self.cue("in exactly")
            self.play(FadeOut(line_grp, shift=DOWN * 1.5), yc.animate.set_value(-3.05), op.animate.set_value(0.35), run_time=0.6)
            spec = [(12, [2, 2, 3]), (30, [2, 3, 5]), (91, [7, 13]), (360, [2, 2, 2, 3, 3, 5])]
            cx = [-4.9, -1.65, 1.65, 4.9]
            nums, mols = [], []
            for (n, f), x in zip(spec, cx):
                num = M(str(n), size=84).move_to([x, 1.0, 0])
                atoms, bonds = molecule(n, f, np.array([x, -0.3, 0]))
                prod = M(r"\cdot".join(str(p) for p in f), size=40, color=MUTED).move_to([x, -1.75, 0])
                nums.append(num); mols.append((atoms, bonds, prod))
            # 12 first, on "atoms of arithmetic"
            self.play(FadeIn(nums[0], scale=0.8), run_time=0.4)
            self.play(nums[0].animate.shift(UP * 0.9), TransformFromCopy(nums[0], mols[0][0]), run_time=0.8)
            self.play(Create(mols[0][1]), FadeIn(mols[0][2], shift=UP * 0.1), run_time=0.4)
            self.wait_until(t_every)
            self.play(LaggedStart(*[FadeIn(nums[i], scale=0.8) for i in (1, 2, 3)], lag_ratio=0.3), run_time=0.7)
            self.play(*[nums[i].animate.shift(UP * 0.9) for i in (1, 2, 3)],
                      LaggedStart(*[TransformFromCopy(nums[i], mols[i][0]) for i in (1, 2, 3)], lag_ratio=0.25), run_time=1.3)
            self.play(*[Create(mols[i][1]) for i in (1, 2, 3)], *[FadeIn(mols[i][2], shift=UP * 0.1) for i in (1, 2, 3)], run_time=0.5)
            # "in exactly one way": each molecule locks in
            self.wait_until(t_one)
            rings = VGroup(*[SurroundingRectangle(VGroup(nums[i], mols[i][0], mols[i][2]), color=GOOD, buff=0.18, corner_radius=0.2, stroke_width=2.5)
                             for i in range(4)])
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15), run_time=min(0.9, self.left() - 0.05))
        b_stuff = VGroup(*nums, *[VGroup(*m) for m in mols], rings)

        # ---------------------------------------------------------------- c: zoom out -> static
        with self.beat("c") as d:
            self.play(FadeOut(b_stuff, shift=UP * 0.3), yc.animate.set_value(0.1), op.animate.set_value(1.0), run_time=0.6)
            # the window widens 20 -> 1200 and the ticks grow into a barcode
            self.play(W.animate.set_value(1200), hh.animate.set_value(2.4), run_time=1.6, rate_func=smooth)
            # then it scrolls by, like static
            self.play(off.animate.set_value(off.get_value() + 3200), run_time=self.left() - 0.05, rate_func=linear)

        # ---------------------------------------------------------------- d: static -> music, 1859
        zs = zeta_zeros(5)
        ylev = [1.25, 0.5, -0.25, -1.0, -1.75]
        phase = ValueTracker(0.0)
        amp = ValueTracker(0.0)
        WX0, WX1 = -5.5, 6.3

        def wave(k):
            def f():
                u = np.linspace(0, 2.2, 360)
                xs = WX0 + u / 2.2 * (WX1 - WX0)
                ys = ylev[k] + amp.get_value() * 0.27 * np.cos(zs[k] * u - phase.get_value() * zs[k] / 14)
                return VMobject().set_points_smoothly([np.array([x, y, 0]) for x, y in zip(xs, ys)]).set_stroke(ZERO, 3)
            return always_redraw(f)

        with self.beat("d") as d:
            pz = pz_or("s01d", 5, None)
            t_riem = pz[0][1] if pz else self.cue("bernhard")
            t_music = pz[1][1] if pz else self.cue("that the static")
            t_note = pz[2][1] if pz else self.cue("and that every")
            t_years = pz[3][1] if pz else self.cue("for a hundred")
            t_nobody = pz[4][1] if pz else self.cue("nobody could")
            # timeline + 1859
            tl = Line([-5.5, -3.0, 0], [5.5, -3.0, 0]).set_stroke(MUTED, 3)
            y1859 = M("1859", size=40).next_to(tl.get_start(), DOWN, buff=0.18)
            tick0 = Line(UP * 0.15, DOWN * 0.15).set_stroke(INK, 3).move_to(tl.get_start())
            sc = off.get_value()
            self.play(off.animate.set_value(sc + 220), yc.animate.set_value(2.75), hh.animate.set_value(0.95), Create(tl), FadeIn(tick0),
                      FadeIn(y1859, shift=UP * 0.2), run_time=1.2, rate_func=smooth)
            self.wait_until(t_riem)
            # the strip "decomposes" into clean waves (frequencies = heights of the first five zeta zeros)
            waves = [wave(k) for k in range(5)]
            ghosts = [bars.copy().clear_updaters() for _ in range(5)]
            for g in ghosts: g.set_stroke(opacity=0.5)
            self.add(*waves)
            self.play(LaggedStart(*[g.animate.move_to([0.4, ylev[k], 0]).stretch_to_fit_height(0.1).set_stroke(ZERO, opacity=0)
                                    for k, g in enumerate(ghosts)], lag_ratio=0.18),
                      amp.animate.set_value(1.0), run_time=2.2)
            self.remove(*ghosts)
            # music: the waves start to travel
            self.play(phase.animate.set_value(1.2), run_time=max(0.5, t_music - self.now() + self._beat_start + 0.3), rate_func=linear)
            self.play(phase.animate.set_value(3.2), run_time=max(0.5, t_note - (self.now() - self._beat_start)), rate_func=linear)
            # every note tuned precisely: all five sit on one exact vertical line (the critical line, foreshadowed)
            notes = VGroup(*[Dot([-6.05, y, 0], radius=0.11, color=ZERO) for y in ylev])
            vline = DashedLine([-6.05, 1.75, 0], [-6.05, -2.25, 0], dash_length=0.1).set_stroke(ZERO, 3, opacity=0.9)
            self.play(Create(vline), LaggedStart(*[GrowFromCenter(n) for n in notes], lag_ratio=0.2), phase.animate.set_value(4.4),
                      run_time=1.3, rate_func=linear)
            self.play(phase.animate.set_value(7.0), run_time=max(0.3, t_years - 0.2 - (self.now() - self._beat_start)), rate_func=linear)
            # 167 years go by, unproved
            year = ValueTracker(1859)
            fill = always_redraw(lambda: Line(tl.get_start(), tl.point_from_proportion(max(1e-3, (year.get_value() - 1859) / 167)))
                                 .set_stroke(BAD, 6))
            ylab = always_redraw(lambda: Integer(int(year.get_value()), font_size=40, color=INK, group_with_commas=False)
                                 .next_to(fill.get_end(), DOWN, buff=0.18))
            self.add(fill, ylab)
            self.play(year.animate.set_value(2026), phase.animate.set_value(10.5),
                      run_time=max(0.8, t_nobody + 0.3 - (self.now() - self._beat_start)), rate_func=smooth)
            unp = T("unproved", size=36, color=BAD).next_to(tl, UP, buff=0.22)
            self.play(FadeIn(unp, shift=UP * 0.15), phase.animate.set_value(12.0), run_time=min(0.8, self.left() - 0.05), rate_func=linear)

        # ---------------------------------------------------------------- e: November 2026, 17 million lines, title
        with self.beat("e") as d:
            pz = pz_or("s01e", 7, None)
            t_name = pz[0][1] if pz else self.cue("the mathematician")
            t_claude = pz[1][1] if pz else self.cue("working with")
            t_pub = pz[2][1] if pz else self.cue("published")
            t_lines = pz[3][1] if pz else self.cue("seventeen million")
            t_check = pz[4][1] if pz else self.cue("checked line")
            t_title = pz[5][1] if pz else self.cue("this video")
            t_sub = pz[6][1] if pz else self.cue("and how")
            end = Dot(tl.get_end(), radius=0.12, color=GOOD)
            nov = M(r"\text{Nov }2026", size=40, color=GOOD).next_to(tl.get_end(), DOWN, buff=0.18).align_to(tl.get_end(), RIGHT).shift(RIGHT * 0.35)
            ylab.clear_updaters(); fill.clear_updaters()
            self.play(FadeIn(end, scale=2), ReplacementTransform(ylab, nov), phase.animate.set_value(13.0), run_time=0.8, rate_func=linear)
            self.wait_until(t_name - 0.1)
            # clear the music, bring in the names
            name1 = T("Levent Alpöge", size=56, weight=MEDIUM).move_to(UP * 0.9)
            name2 = T("+  Claude", size=56, weight=MEDIUM, color=LIFT).move_to(DOWN * 0.3)
            self.play(FadeOut(VGroup(*waves, notes, vline)), op.animate.set_value(0.0), FadeIn(name1, shift=UP * 0.2), run_time=0.8)
            self.remove(bars)
            self.wait_until(t_claude)
            self.play(FadeIn(name2, shift=UP * 0.2), run_time=0.6)
            self.wait_until(t_pub - 0.1)
            proof = T("proof", size=36, color=GOOD).move_to(unp)
            self.play(fill.animate.set_stroke(GOOD), ReplacementTransform(unp, proof), Flash(end, color=GOOD, line_length=0.25, flash_radius=0.3),
                      run_time=0.7)
            self.wait_until(t_lines - 0.15)

            # the wall of code: abstract rows of dashes, scrolling upward
            rng = np.random.default_rng(7)
            rows = VGroup()
            nrows, pitch = 34, 0.27
            for r in range(nrows):
                y = 4.3 - r * pitch
                x = -6.9 + 0.4 * rng.integers(0, 6)
                xend = rng.uniform(1.0, 6.9)
                row = VGroup()
                while True:
                    L = rng.uniform(0.25, 1.5)
                    if x + L > xend: break
                    col = rng.choice([MUTED, MUTED, MUTED, DIM, LIFT, ZERO, PRIME])
                    row.add(Line([x, y, 0], [x + L, y, 0]).set_stroke(col, 4, opacity=0.55))
                    x += L + rng.uniform(0.12, 0.3)
                rows.add(row)
            span = nrows * pitch

            def scroll(m, dt):
                m.shift(UP * 1.6 * dt)
                if m.get_y() > 4.45: m.shift(DOWN * span)
            for row in rows: row.add_updater(scroll)
            cnt = ValueTracker(0)
            counter = always_redraw(lambda: Integer(int(cnt.get_value()), font_size=110, color=INK, group_with_commas=True).move_to(UP * 0.35))
            lines_l = T("lines", size=44, color=MUTED).move_to(DOWN * 0.75)
            back = RoundedRectangle(width=7.6, height=2.9, corner_radius=0.25, stroke_width=0, fill_color=BG, fill_opacity=0.88).move_to(UP * 0.05)
            self.play(FadeOut(VGroup(name1, name2, tl, tick0, y1859, nov, end, fill, proof)),
                      LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.02), FadeIn(back), FadeIn(lines_l), run_time=0.8)
            self.add(counter)
            self.play(cnt.animate.set_value(17374215), run_time=max(1.0, t_check + 1.2 - (self.now() - self._beat_start)),
                      rate_func=rush_from)
            # checked line by line: a green scan passes down the wall, ticking rows off
            chk = M(r"\checkmark", size=60, color=GOOD).next_to(lines_l, RIGHT, buff=0.3)
            scan = Rectangle(width=14.4, height=0.35, stroke_width=0, fill_color=GOOD, fill_opacity=0.18).move_to(UP * 4.3)
            self.add(scan); self.bring_to_front(back, counter, lines_l)

            def tick(m):
                if m.get_y() > scan.get_y(): m.set_stroke(GOOD, opacity=0.6)
            for row in rows: row.add_updater(tick)
            t_rem = t_title - 0.2 - (self.now() - self._beat_start)
            self.play(scan.animate.move_to(DOWN * 4.3), FadeIn(chk, scale=1.5), run_time=max(0.8, t_rem), rate_func=linear)
            # title card
            title = T("The Riemann Hypothesis", size=80, weight=MEDIUM).move_to(UP * 0.45)
            sub = T("what it says, and how the proof works", size=38, color=MUTED).next_to(title, DOWN, buff=0.45)
            rule = Line(LEFT * 3.2, RIGHT * 3.2).set_stroke(PRIME, 3).next_to(title, UP, buff=0.4)
            counter.clear_updaters()
            self.play(FadeOut(VGroup(rows, scan, back, counter, lines_l, chk)), run_time=0.45)
            self.play(FadeIn(title, shift=UP * 0.2), Create(rule), run_time=0.7)
            for row in rows: row.clear_updaters()
            self.wait_until(t_sub - 0.2)
            self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.8)
            self.play(VGroup(title, sub, rule).animate.scale(1.03), run_time=max(0.3, self.left() - 0.05), rate_func=linear)
        self.finish()
