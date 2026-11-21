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


def pz_or(key, n):
    p = pauses(key)
    return p if len(p) >= n else None


PR = np.array(primes_upto(1_000_000))


@functools.lru_cache(None)
def li_table():
    """Li(x) = integral_2^x dt/ln t, tabulated on a log grid (mpmath), for fast interpolation."""
    import mpmath
    xs = np.exp(np.linspace(np.log(2.0), np.log(2.0e6), 3000))
    return np.log(xs), np.array([float(mpmath.li(x, offset=True)) for x in xs])


def Li(x):
    lx, lv = li_table()
    x = np.maximum(np.asarray(x, dtype=float), 2.0)
    return np.interp(np.log(x), lx, lv)


def pi_of(x):
    return np.searchsorted(PR, np.asarray(x, dtype=float), side="right")


@functools.lru_cache(None)
def num_label(v):
    return Integer(int(v), font_size=30, color=MUTED, group_with_commas=True)


def nice_step(span, n=5):
    raw = span / n
    mag = 10 ** np.floor(np.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if m * mag >= raw: return m * mag
    return 10 * mag


# plot frame on screen
OX, OY, PW, PH = -5.3, -2.85, 11.5, 5.75


class Plot:
    """A pi(x) plot whose x-range is a tracker (X) — the axes relabel themselves as it zooms."""

    def __init__(self, X, walk=None):
        self.X, self.walk = X, walk

    def ymax(self, X=None):
        X = self.X.get_value() if X is None else X
        return 1.25 * X / np.log(X)

    def p(self, x, y):
        X = self.X.get_value()
        return np.array([OX + x / X * PW, OY + y / self.ymax() * PH, 0.0])

    def axes(self):
        ax = VGroup(Line([OX, OY, 0], [OX + PW + 0.25, OY, 0]), Line([OX, OY, 0], [OX, OY + PH + 0.2, 0])).set_stroke(MUTED, 3)
        return ax

    def ticks(self):
        X, Y = self.X.get_value(), self.ymax()
        g = VGroup()
        sx = nice_step(X)
        for k in np.arange(sx, X * 1.0001, sx):
            x = OX + k / X * PW
            g.add(Line([x, OY, 0], [x, OY - 0.12, 0]).set_stroke(MUTED, 2))
            g.add(num_label(int(round(k))).copy().move_to([x, OY - 0.38, 0]))
        sy = nice_step(Y, 4)
        for k in np.arange(sy, Y * 0.98, sy):
            y = OY + k / Y * PH
            g.add(Line([OX, y, 0], [OX - 0.12, y, 0]).set_stroke(MUTED, 2))
            g.add(num_label(int(round(k))).copy().next_to([OX - 0.14, y, 0], LEFT, buff=0.1))
        return g

    def stair(self):
        X = self.X.get_value()
        top = X if self.walk is None else min(X, self.walk.get_value())
        if X <= 4000:
            ps = PR[PR <= top]
            pts = [self.p(0, 0)]
            for i, q in enumerate(ps):
                pts += [self.p(q, i), self.p(q, i + 1)]
            pts.append(self.p(top, len(ps)))
        else:
            xs = np.linspace(0, top, 1200)
            pts = [self.p(x, y) for x, y in zip(xs, pi_of(xs))]
        return VMobject().set_points_as_corners(pts).set_stroke(PRIME, 4)

    def li(self, upto=None):
        X = self.X.get_value()
        xs = np.linspace(2, X if upto is None else upto, 400)
        return VMobject().set_points_smoothly([self.p(x, y) for x, y in zip(xs, Li(xs))]).set_stroke(INK, 7, opacity=0.6)


class S03(NarratedScene):
    sid = "s03"

    def construct(self):
        X = ValueTracker(30.0)
        walk = ValueTracker(0.0)
        P = Plot(X, walk)
        axes = P.axes()
        ticks = always_redraw(P.ticks)
        stair = always_redraw(P.stair)

        # ---------------------------------------------------------------- a: walk and climb
        with self.beat("a") as d:
            pz = pz_or("s03a", 4)
            t_name = pz[2][1] if pz else self.cue("mathematicians")
            t_def = pz[3][1] if pz else self.cue("the number of")
            walker = always_redraw(lambda: Dot(P.p(walk.get_value(), 0), radius=0.1, color=INK))
            climber = always_redraw(lambda: Dot(P.p(walk.get_value(), pi_of(walk.get_value())), radius=0.11, color=PRIME))
            def mk():
                Xv = X.get_value()
                if Xv > 96: return VGroup()
                return VGroup(*[Line(P.p(q, 0), P.p(q, 0) + UP * 0.22) for q in PR[PR <= min(walk.get_value(), Xv)]]).set_stroke(
                    PRIME, 4, opacity=float(np.clip(1.6 - Xv / 60, 0, 1)))
            marks = always_redraw(mk)
            self.play(Create(axes), FadeIn(ticks), run_time=0.6)
            self.add(marks, stair, walker, climber)
            self.play(walk.animate.set_value(30), run_time=t_name - 0.6, rate_func=linear)
            lab = M(r"\pi(x)", size=72, color=PRIME)
            lab_d = T("number of primes up to x", size=38, color=INK)
            hdr = VGroup(lab, lab_d).arrange(RIGHT, buff=0.4).move_to([OX + 0.6, 2.85, 0], aligned_edge=LEFT)
            hdr.shift(RIGHT * (OX + 0.5 - hdr.get_left()[0]))
            self.wait_until(t_name + 1.0)
            self.play(Write(lab), Indicate(stair, color=PRIME, scale_factor=1.0), run_time=0.9)
            self.wait_until(t_def - 0.1)
            self.play(FadeIn(lab_d, shift=LEFT * 0.2), run_time=0.7)

        # ---------------------------------------------------------------- b: zoom out 30 -> 100 -> 1,000 -> 1,000,000
        with self.beat("b") as d:
            pz = pz_or("s03b", 4)
            tz = [pz[k][1] for k in range(4)] if pz else [self.cue(w) for w in ("now zoom", "to a thousand", "to a million", "the stairs")]
            walk.set_value(1e9)
            self.remove(walker, climber)
            self.play(FadeOut(walker.copy()), FadeOut(climber.copy()), run_time=0.3)
            self.wait_until(tz[0])
            self.play(X.animate.set_value(100), run_time=tz[1] - tz[0] - 0.05, rate_func=smooth)
            self.play(X.animate.set_value(1000), run_time=tz[2] - tz[1] - 0.05, rate_func=smooth)
            self.play(X.animate.set_value(1_000_000), run_time=tz[3] - tz[2] + 0.2, rate_func=smooth)
            self.remove(marks)
            # "melts into a smooth curve": a glow runs along it
            g2 = P.stair().set_stroke(PRIME, 14, opacity=0.35)
            self.play(ShowPassingFlash(g2, time_width=0.4), run_time=min(1.4, self.left() - 0.05))

        # ---------------------------------------------------------------- c: Gauss: 1 in ln x
        with self.beat("c") as d:
            pz = pz_or("s03c", 5)
            t_near = pz[0][1] if pz else self.cue("near a number")
            t_mil = pz[1][1] if pz else self.cue("near a million")
            t_tri = pz[2][1] if pz else self.cue("near a trillion")
            t_thin = pz[3][1] if pz else self.cue("primes thin")
            gauss = T("Gauss", size=48, color=INK).move_to([3.4, -0.6, 0])
            curve_lab = M(r"\pi(x)", size=56, color=PRIME)
            self.play(FadeIn(gauss, shift=UP * 0.2), run_time=0.6)
            self.wait_until(t_near - 0.2)
            plot_all = VGroup(axes, ticks, stair, lab, lab_d, gauss)
            self.play(FadeOut(plot_all), run_time=0.6)
            ticks.clear_updaters(); stair.clear_updaters()
            chance = T("chance a number near x is prime", size=40)
            frac = M(r"\approx\ \frac{1}{\ln x}", size=64, color=PRIME)
            top = VGroup(chance, frac).arrange(RIGHT, buff=0.35).move_to(UP * 2.75)
            self.play(FadeIn(chance, shift=UP * 0.2), run_time=0.7)
            self.play(Write(frac), run_time=0.8)

            def strip(start, lit, y, n):
                dots = VGroup(*[Dot(radius=0.105, color=DIM) for _ in range(n)]).arrange(RIGHT, buff=0.235)
                dots.move_to([0, y, 0]).align_to([-6.0, 0, 0], LEFT)
                i = lit - start
                dots[i].set_color(PRIME).scale(1.4)
                halo = Circle(radius=0.3, stroke_width=0, fill_color=PRIME, fill_opacity=0.18).move_to(dots[i])
                tag = M(f"{lit:,}".replace(",", "{,}"), size=32, color=PRIME).next_to(dots[i], DOWN, buff=0.3)
                br = Brace(dots, UP, buff=0.12, color=MUTED)
                return dots, halo, tag, br

            d1, h1, tg1, b1 = strip(1_000_000, 1_000_003, 0.55, 14)
            l1 = VGroup(T("near a million:", size=36, color=MUTED), M(r"1 \text{ in } 14", size=46)).arrange(RIGHT, buff=0.3)
            l1.next_to(b1, UP, buff=0.15).align_to(d1, LEFT)
            T12 = 10 ** 12
            d2, h2, tg2, b2 = strip(T12 - 24, T12 - 11, -2.0, 28)
            l2 = VGroup(T("near a trillion:", size=36, color=MUTED), M(r"1 \text{ in } 28", size=46)).arrange(RIGHT, buff=0.3)
            l2.next_to(b2, UP, buff=0.15).align_to(d2, LEFT)
            self.wait_until(t_mil - 0.15)
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in d1], lag_ratio=0.06), GrowFromCenter(b1), FadeIn(l1[0]), run_time=1.0)
            self.play(FadeIn(h1, scale=0.3), FadeIn(tg1, shift=UP * 0.1), FadeIn(l1[1], shift=LEFT * 0.1), run_time=0.6)
            self.wait_until(t_tri - 0.15)
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in d2], lag_ratio=0.03), GrowFromCenter(b2), FadeIn(l2[0]), run_time=1.0)
            self.play(FadeIn(h2, scale=0.3), FadeIn(tg2, shift=UP * 0.1), FadeIn(l2[1], shift=LEFT * 0.1), run_time=0.6)
            self.wait_until(t_thin - 0.1)
            # thinning out: a gentle scan along each strip, the lone prime flaring as it passes
            self.play(LaggedStart(*[Indicate(x, color=MUTED, scale_factor=1.4) for x in d1], lag_ratio=0.1),
                      LaggedStart(*[Indicate(x, color=MUTED, scale_factor=1.4) for x in d2], lag_ratio=0.05),
                      run_time=min(2.2, self.left() - 0.05))
        c_stuff = VGroup(top, d1, h1, tg1, b1, l1, d2, h2, tg2, b2, l2)

        # ---------------------------------------------------------------- d: Li(x) hugs the staircase; PNT 1896
        with self.beat("d") as d:
            pz = pz_or("s03d", 4)
            t_1896 = pz[0][1] if pz else self.cue("in eighteen")
            t_agree = pz[1][1] if pz else self.cue("the prediction and")
            t_long = pz[2][1] if pz else self.cue("in the long")
            t_pnt = pz[3][1] if pz else self.cue("that's the")
            X.set_value(1000)
            ticks = always_redraw(P.ticks)
            stair = always_redraw(P.stair)
            self.play(FadeOut(c_stuff), FadeIn(axes), FadeIn(ticks), FadeIn(stair), run_time=0.7)
            upto = ValueTracker(2.0)
            li_c = always_redraw(lambda: P.li(max(2.5, upto.get_value())))
            self.add(li_c); self.bring_to_front(stair)
            self.play(upto.animate.set_value(1000), run_time=1.4, rate_func=smooth)
            li_c.clear_updaters(); self.remove(li_c)
            li_c = always_redraw(P.li)
            self.add(li_c); self.bring_to_front(stair)
            pred = always_redraw(lambda: T("prediction", size=36, color=INK).next_to(P.p(0.42 * X.get_value(), Li(0.42 * X.get_value())), UL, buff=0.25))
            truth = always_redraw(lambda: T("truth", size=36, color=PRIME).next_to(P.p(0.72 * X.get_value(), pi_of(0.72 * X.get_value())), DR, buff=0.25))
            self.play(FadeIn(pred), FadeIn(truth), run_time=0.6)
            self.wait_until(t_1896 - 0.1)
            cap = VGroup(T("Prime Number Theorem", size=44, weight=MEDIUM), M("1896", size=48, color=MUTED)).arrange(RIGHT, buff=0.35)
            cap.move_to([OX + 0.5, 2.85, 0], aligned_edge=LEFT)
            cap.shift(RIGHT * (OX + 0.5 - cap.get_left()[0]))
            self.play(FadeIn(cap, shift=DOWN * 0.15), run_time=0.8)
            self.wait_until(t_agree - 0.1)
            # in the long run: zoom out and the two become one
            self.play(X.animate.set_value(1_000_000), run_time=max(1.0, t_pnt - 0.2 - (self.now() - self._beat_start)), rate_func=smooth)
            ul = Line(cap[0].get_corner(DL), cap[0].get_corner(DR)).shift(DOWN * 0.12).set_stroke(PRIME, 3)
            self.play(Create(ul), run_time=min(0.8, self.left() - 0.05))
        self.finish()
