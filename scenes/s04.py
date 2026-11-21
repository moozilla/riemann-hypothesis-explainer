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


PR = np.array(primes_upto(100_000))


@functools.lru_cache(None)
def li_table():
    import mpmath
    xs = np.exp(np.linspace(np.log(2.0), np.log(2.0e5), 2500))
    return np.log(xs), np.array([float(mpmath.li(x, offset=True)) for x in xs])


def Li(x):
    lx, lv = li_table()
    x = np.maximum(np.asarray(x, dtype=float), 2.0)
    return np.interp(np.log(x), lx, lv)


def pi_of(x):
    return np.searchsorted(PR, np.asarray(x, dtype=float), side="right")


def frame_map(ox, oy, w, h, X, Y0, Y1):
    """data (x, y) -> screen point, for a box with lower-left (ox, oy), size w x h, ranges [0,X] x [Y0,Y1]."""
    def p(x, y):
        return np.array([ox + x / X * w, oy + (y - Y0) / (Y1 - Y0) * h, 0.0])
    return p


def stair_pts(p, X):
    ps = PR[PR <= X]
    pts = [p(0, 0)]
    for i, q in enumerate(ps):
        pts += [p(q, i), p(q, i + 1)]
    pts.append(p(X, len(ps)))
    return pts


def err_pts(p, X, n=None):
    """pi(x) - Li(x) on [2, X]: exact jumps at primes, smooth decline in between."""
    xs = np.unique(np.concatenate([np.linspace(2, X, 700), PR[PR <= X] - 1e-6, PR[PR <= X]]))
    ys = pi_of(xs) - Li(xs)
    return [p(x, y) for x, y in zip(xs, ys)]


class S04(NarratedScene):
    sid = "s04"

    def construct(self):
        X = 1000
        # top: the staircase and its prediction
        pt = frame_map(-5.6, 0.55, 11.6, 2.75, X, 0, 185)
        ax_t = VGroup(Line(pt(0, 0), pt(X, 0) + RIGHT * 0.2), Line(pt(0, 0), pt(0, 185) + UP * 0.1)).set_stroke(MUTED, 3)
        stair = VMobject().set_points_as_corners(stair_pts(pt, X)).set_stroke(PRIME, 4)
        xs = np.linspace(2, X, 300)
        li_c = VMobject().set_points_smoothly([pt(x, y) for x, y in zip(xs, Li(xs))]).set_stroke(INK, 4)
        truth = T("truth", size=32, color=PRIME).next_to(pt(700, pi_of(700)), DR, buff=0.2)
        pred = T("prediction", size=32, color=INK).next_to(pt(380, Li(380)), UL, buff=0.2)
        # bottom: the error, magnified
        E = 14
        pb = frame_map(-5.6, -3.35, 11.6, 3.0, X, -E, E)
        zero_b = Line(pb(0, 0), pb(X, 0) + RIGHT * 0.2).set_stroke(MUTED, 3)
        yax_b = Line(pb(0, -E), pb(0, E)).set_stroke(MUTED, 3)
        err = VMobject().set_points_as_corners(err_pts(pb, X)).set_stroke(WARM, 3.5)
        err_lab = T("truth − prediction", size=32, color=WARM).move_to(pb(0, E * 0.8), aligned_edge=LEFT).shift(RIGHT * 0.3)
        ticks_b = VGroup(*[M(s, size=28, color=MUTED).next_to(pb(0, v), LEFT, buff=0.12) for s, v in (("+10", 10), ("0", 0), ("-10", -10))])
        xnum = VGroup(*[Integer(v, font_size=28, color=MUTED, group_with_commas=True).next_to(pt(v, 0), DOWN, buff=0.12) for v in (500, 1000)])

        # ---------------------------------------------------------------- a: subtract -> the wobble
        with self.beat("a") as d:
            pz = pz_or("s04a", 3)
            t_sub = pz[0][1] if pz else self.cue("subtract")
            t_err = pz[1][1] if pz else self.cue("and you're")
            t_wob = pz[2][1] if pz else self.cue("a wobble")
            self.play(Create(ax_t), FadeIn(xnum), Create(stair), Create(li_c), run_time=1.2)
            self.play(FadeIn(truth), FadeIn(pred), run_time=0.5)
            # "hides the interesting part": a lens slides along the gap between the curves
            lens = Circle(radius=0.42, color=WARM, stroke_width=3).move_to(pt(150, (pi_of(150) + Li(150)) / 2))
            self.play(Create(lens), run_time=0.3)
            self.play(lens.animate.move_to(pt(850, (pi_of(850) + Li(850)) / 2)), run_time=max(0.4, t_sub - 0.15 - (self.now() - self._beat_start)))
            # subtract: the prediction flattens into the zero line, the truth into the error
            self.play(FadeOut(lens), Create(zero_b), Create(yax_b), FadeIn(ticks_b), run_time=0.5)
            zcopy = zero_b.copy()
            self.play(TransformFromCopy(li_c, zcopy), TransformFromCopy(stair, err), run_time=max(0.8, t_err - 0.1 - (self.now() - self._beat_start)))
            self.play(FadeIn(err_lab, shift=UP * 0.1), run_time=0.5)
            self.wait_until(t_wob - 0.15)
            flash = err.copy().set_stroke(WARM, 9, opacity=0.6)
            self.play(ShowPassingFlash(flash, time_width=0.35), run_time=min(1.1, self.left() - 0.05))

        # ---------------------------------------------------------------- b: coin flips and the sqrt(N) envelope
        N = 1_000_000
        K = 800                            # points per path
        ENV = 2.0                         # screen height of sqrt(N) at the right edge
        cx0, cy0, cw = -5.6, -0.55, 9.0

        def cp(t, s):                      # t in [0,1] (fraction of N), s in units of sqrt(N)
            return np.array([cx0 + t * cw, cy0 + s * ENV, 0.0])

        rng = np.random.default_rng(2026)
        paths = []
        tgrid = np.linspace(0, 1, K + 1)
        while len(paths) < 7:
            steps = rng.integers(0, 2, size=N, dtype=np.int8) * 2 - 1
            S = np.concatenate([[0], np.cumsum(steps, dtype=np.int64)])[(tgrid * N).astype(int)] / np.sqrt(N)
            ok = np.all(np.abs(S[8:]) <= 1.12 * np.sqrt(tgrid[8:])) and np.all(np.abs(S) <= 1.12)
            finals = [p[-1] for p in paths]
            if ok and all(abs(S[-1] - f) > 0.18 for f in finals):
                paths.append(S)
        paths.sort(key=lambda s: s[-1])
        prog = ValueTracker(0.0)

        def walk_mob(S, col, w):
            def f():
                k = max(2, int(prog.get_value() * K) + 1)
                return VMobject().set_points_as_corners([cp(t, s) for t, s in zip(tgrid[:k], S[:k])]).set_stroke(col, w, opacity=0.85)
            return always_redraw(f)

        cols = [MUTED, INK, MUTED, INK, MUTED, INK, MUTED]
        walks = [walk_mob(S, c, 2.5) for S, c in zip(paths, cols)]
        c_ax = VGroup(Line(cp(0, 0), cp(1, 0) + RIGHT * 0.25), Line(cp(0, -1.25), cp(0, 1.25))).set_stroke(MUTED, 3)
        env_t = np.linspace(0, 1, 200)
        env_up = VMobject().set_points_smoothly([cp(t, np.sqrt(t)) for t in env_t]).set_stroke(GOOD, 4)
        env_dn = VMobject().set_points_smoothly([cp(t, -np.sqrt(t)) for t in env_t]).set_stroke(GOOD, 4)
        band = VMobject().set_points_as_corners([cp(t, np.sqrt(t)) for t in env_t] + [cp(t, -np.sqrt(t)) for t in env_t[::-1]])
        band.set_stroke(width=0).set_fill(GOOD, 0.08)

        with self.beat("b") as d:
            pz = pz_or("s04b", 6)
            t_cmp = pz[0][1] if pz else self.cue("here's a")
            t_flip = pz[1][1] if pz else self.cue("flip a coin")
            t_exp = pz[2][1] if pz else self.cue("you expect")
            t_thou = pz[3][1] if pz else self.cue("typically")
            t_sqrt = pz[4][1] if pz else self.cue("which is")
            t_sig = pz[5][1] if pz else self.cue("square-root-sized")
            # how big can it get? amplitude arrows on the wobble
            arr = DoubleArrow(pb(640, 0), pb(640, -12), buff=0, color=WARM, stroke_width=3, tip_length=0.18)
            q = T("how big?", size=34, color=WARM).next_to(arr.get_bottom(), RIGHT, buff=0.2).shift(UP * 0.1)
            self.play(GrowFromCenter(arr), FadeIn(q), run_time=0.6)
            self.wait_until(t_cmp - 0.15)
            a_stuff = VGroup(ax_t, xnum, stair, li_c, truth, pred, zero_b, zcopy, yax_b, ticks_b, err, err_lab, arr, q)
            self.play(FadeOut(a_stuff, shift=UP * 0.3), run_time=0.6)
            # coin axes
            flips = VGroup(Integer(N, font_size=44, group_with_commas=True), T("flips", size=40, color=MUTED)).arrange(RIGHT, buff=0.22)
            flips.move_to([-5.6, 3.05, 0], aligned_edge=LEFT)
            flips.shift(RIGHT * (-5.6 - flips.get_left()[0]))
            ylab = T("heads − tails", size=30, color=MUTED).next_to(cp(0, 1.25), UP, buff=0.12).align_to([cx0 + 0.25, 0, 0], LEFT)
            nlab = Integer(N, font_size=30, color=MUTED, group_with_commas=True).move_to(cp(1, -1.25))
            self.play(Create(c_ax), FadeIn(ylab), run_time=0.6)
            self.wait_until(t_flip - 0.1)
            self.add(*walks)
            self.play(FadeIn(flips, shift=DOWN * 0.15), prog.animate.set_value(0.35), run_time=t_exp - t_flip - 0.05, rate_func=linear)
            exp = VGroup(T("expect", size=36, color=MUTED), Integer(500000, font_size=44, group_with_commas=True), T("heads", size=36, color=MUTED)).arrange(RIGHT, buff=0.2)
            exp.move_to([6.4, 3.05, 0], aligned_edge=RIGHT)
            exp.shift(RIGHT * (6.4 - exp.get_right()[0]))
            self.play(FadeIn(exp, shift=DOWN * 0.15), prog.animate.set_value(0.5), run_time=0.8, rate_func=linear)
            self.play(prog.animate.set_value(1.0), run_time=max(0.5, t_thou - 0.1 - (self.now() - self._beat_start)), rate_func=linear)
            # typically ~1,000 off
            br = Brace(Line(cp(1, 0), cp(1, 1)), RIGHT, buff=0.18, color=GOOD)
            thou = M(r"\approx 1{,}000", size=44, color=GOOD).next_to(br, RIGHT, buff=0.1)
            self.add(band)
            self.play(FadeIn(band), Create(env_up), Create(env_dn), GrowFromCenter(br), FadeIn(thou), run_time=1.2)
            self.wait_until(t_sqrt - 0.1)
            sq = M(r"=\sqrt{1{,}000{,}000}", size=44, color=GOOD).next_to(thou, DOWN, buff=0.2).align_to(thou, LEFT)
            # keep it on screen: shift the pair left if needed
            pair = VGroup(thou, sq)
            if pair.get_right()[0] > 6.6: pair.shift(LEFT * (pair.get_right()[0] - 6.6))
            self.play(Write(sq), run_time=0.8)
            self.wait_until(t_sig - 0.1)
            sqrtN = M(r"\sqrt{N}", size=56, color=GOOD).next_to(cp(0.62, np.sqrt(0.62)), UP, buff=0.3)
            self.play(FadeIn(sqrtN, shift=DOWN * 0.1), ShowPassingFlash(env_up.copy().set_stroke(GOOD, 10), time_width=0.5),
                      ShowPassingFlash(env_dn.copy().set_stroke(GOOD, 10), time_width=0.5), run_time=1.3)
            for w in walks: w.clear_updaters()
            self.play(*[Indicate(w, color=INK, scale_factor=1.0) for w in walks], run_time=min(1.5, self.left() - 0.05))

        # ---------------------------------------------------------------- c: the primes do exactly that
        with self.beat("c") as d:
            pz = pz_or("s04c", 4)
            t_count = pz[0][1] if pz else self.cue("count the")
            t_off = pz[1][1] if pz else self.cue("and the prediction")
            t_never = pz[2][1] if pz else self.cue("and never")
            t_ord = pz[3][1] if pz else self.cue("the primes are")
            Xp = 1000
            env_scale = ENV * 1.15                       # sqrt(Xp) at the right edge, on screen

            def ppt(x, e):
                return np.array([cx0 + x / Xp * cw, cy0 + e / np.sqrt(Xp) * env_scale, 0.0])

            # envelope widens a little (new units); coin walks recede
            new_up = VMobject().set_points_smoothly([ppt(t * Xp, np.sqrt(t * Xp)) for t in env_t]).set_stroke(GOOD, 4)
            new_dn = VMobject().set_points_smoothly([ppt(t * Xp, -np.sqrt(t * Xp)) for t in env_t]).set_stroke(GOOD, 4)
            new_band = VMobject().set_points_as_corners([ppt(t * Xp, np.sqrt(t * Xp)) for t in env_t] + [ppt(t * Xp, -np.sqrt(t * Xp)) for t in env_t[::-1]])
            new_band.set_stroke(width=0).set_fill(GOOD, 0.08)
            new_ax = VGroup(Line(cp(0, 0), cp(1, 0) + RIGHT * 0.25), Line(ppt(0, -1.5 * np.sqrt(Xp) / 1.45 * 1.4), ppt(0, 1.5 * np.sqrt(Xp) / 1.45 * 1.4))).set_stroke(MUTED, 3)
            new_ax[1].put_start_and_end_on(ppt(0, -1.2 * np.sqrt(Xp)), ppt(0, 1.2 * np.sqrt(Xp)))
            sqx = M(r"\sqrt{x}", size=56, color=GOOD).next_to(ppt(0.62 * Xp, np.sqrt(0.62 * Xp)), UP, buff=0.3)
            plab = T("primes up to x", size=40, color=MUTED)
            plab.move_to([-5.6, 3.05, 0], aligned_edge=LEFT).shift(RIGHT * (-5.6 - plab.get_left()[0]))
            ylab2 = T("truth − prediction", size=30, color=WARM).move_to(ylab).align_to([cx0 + 0.25, 0, 0], LEFT)
            nlab2 = VGroup(M("x", size=36, color=MUTED), M("=", size=36, color=MUTED), Integer(Xp, font_size=34, color=MUTED, group_with_commas=True)).arrange(RIGHT, buff=0.12).next_to(cp(1, 0) + RIGHT * 0.25, RIGHT, buff=0.15)
            walks_g = VGroup(*walks)
            self.play(walks_g.animate.set_stroke(opacity=0.12), FadeOut(VGroup(br, thou, sq, exp)),
                      Transform(env_up, new_up), Transform(env_dn, new_dn), Transform(band, new_band), Transform(c_ax, new_ax),
                      sqrtN.animate.move_to(sqx), run_time=1.4)
            self.wait_until(t_count - 0.35 if t_count > 2 else 1.6)
            self.play(ReplacementTransform(flips, plab), ReplacementTransform(ylab, ylab2), FadeIn(nlab2), ReplacementTransform(sqrtN, sqx), run_time=0.7)
            perr = VMobject().set_points_as_corners(err_pts(ppt, Xp)).set_stroke(WARM, 4)
            self.play(Create(perr), run_time=max(0.8, t_off - 0.05 - (self.now() - self._beat_start)), rate_func=linear)
            stmt = M(r"\big|\,", r"\text{truth}", r" - \text{prediction}", r"\,\big| \;\lesssim\; \sqrt{x}", size=48)
            stmt[1].set_color(PRIME); stmt[3][-3:].set_color(GOOD)
            stmt.move_to([6.4, 3.05, 0]).shift(RIGHT * (6.4 - stmt.get_right()[0]))
            self.play(FadeIn(stmt, shift=DOWN * 0.15), run_time=0.9)
            self.wait_until(t_never - 0.1)
            self.play(ShowPassingFlash(env_up.copy().set_stroke(GOOD, 10), time_width=0.5),
                      ShowPassingFlash(env_dn.copy().set_stroke(GOOD, 10), time_width=0.5), run_time=1.0)
            self.wait_until(t_ord - 0.1)
            # as orderly as randomness: the coin walks come back, sharing the same envelope as the primes
            self.play(walks_g.animate.set_stroke(opacity=0.45), ShowPassingFlash(perr.copy().set_stroke(WARM, 9), time_width=0.3),
                      run_time=1.6)
            self.play(walks_g.animate.set_stroke(opacity=0.2), run_time=min(1.4, self.left() - 0.05))

        # ---------------------------------------------------------------- d: zeta
        with self.beat("d") as d:
            pz = pz_or("s04d", 1)
            t_z = pz[0][1] if pz else self.cue("we need")
            everything = Group(*[m for m in self.mobjects])
            self.play(FadeOut(everything), run_time=0.9)
            self.wait_until(t_z - 0.2)
            zeta = M(r"\zeta", size=220, color=INK)
            halo = VGroup(*[Circle(radius=0.8 + 0.18 * k, stroke_width=0, fill_color=ZERO, fill_opacity=0.035) for k in range(9)])
            self.play(FadeIn(halo, scale=0.6), FadeIn(zeta, scale=0.85), run_time=1.0)
            self.play(halo.animate.scale(1.08), zeta.animate.scale(1.04), run_time=max(0.3, self.left() - 0.05), rate_func=there_and_back)
        self.finish()
