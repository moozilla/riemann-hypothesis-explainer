import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *
import bisect


def psi_minus_x(xs):
    """Chebyshev psi(x) - x, computed exactly from the primes."""
    top = int(max(xs)) + 1
    pp = []
    for p in primes_upto(top):
        q = p
        while q <= top:
            pp.append((q, np.log(p))); q *= p
    pp.sort()
    qs = [a for a, _ in pp]; cs = np.cumsum([b for _, b in pp])
    out = []
    for x in xs:
        i = bisect.bisect_right(qs, x)
        out.append((cs[i - 1] if i else 0.0) - x)
    return np.array(out)


def rig_scale(scale):
    """Beam tilts about the pivot, pans hang plumb (same rig as s14/s16). Returns the angle tracker."""
    scale.beam_group.remove(scale.left_pan, scale.right_pan)
    scale.add(scale.left_pan, scale.right_pan)
    P = scale.pivot.get_center()
    L = np.linalg.norm(scale.beam.get_end() - P)
    offL = scale.left_pan.get_center() - scale.beam.get_start()
    offR = scale.right_pan.get_center() - scale.beam.get_end()
    a = ValueTracker(0.0)

    def ends():
        p = scale.pivot.get_center(); v = L * np.array([np.cos(a.get_value()), np.sin(a.get_value()), 0])
        return p - v, p + v
    scale.beam.add_updater(lambda m: m.put_start_and_end_on(*ends()))
    scale.left_pan.add_updater(lambda m: m.move_to(ends()[0] + offL))
    scale.right_pan.add_updater(lambda m: m.move_to(ends()[1] + offR))
    return a


def glow_dot(p, color, r=0.07, layers=3):
    g = VGroup(*[Dot(p, radius=r * (1 + 0.9 * k), color=color, fill_opacity=0.16) for k in range(layers, 0, -1)])
    g.add(Dot(p, radius=r, color=color))
    return g


class S22(NarratedScene):
    sid = "s22"

    def construct(self):
        # ============================================================ a: barcode -> zeros emit waves -> error in sqrt envelope
        with self.beat("a") as d:
            # barcode of primes
            X0, X1 = -6.3, 6.3
            NMAX = 700
            bar_line = Line(LEFT * 6.3, RIGHT * 6.3).set_stroke(MUTED, 2).shift(UP * 0.2)
            ticks = VGroup(*[Line(DOWN * 0.7, UP * 0.7).set_stroke(PRIME, 2.5).move_to(
                np.array([X0 + (X1 - X0) * p / NMAX, 0.2, 0])) for p in primes_upto(NMAX)])
            self.play(Create(bar_line), LaggedStart(*[FadeIn(t, scale=0.3) for t in ticks], lag_ratio=0.01), run_time=2.2)
            self.at("Their randomness", lead=0.6)
            # barcode moves up as a thin strip; the critical strip arrives on the left
            bc = VGroup(bar_line, ticks)
            cs = critical_strip(height=5.4, width=1.3, tmax=40, n_zeros=6)
            cs.move_to(LEFT * 5.15 + DOWN * 0.45)
            self.play(bc.animate.stretch(0.35, 1).stretch((6.3 + 3.3) / 12.6, 0).move_to(RIGHT * 1.5 + UP * 3.2),
                      FadeIn(VGroup(cs.strip, cs.edges, cs.axis, cs.line, cs.labels)), run_time=1.0)
            self.play(LaggedStart(*[GrowFromCenter(z) for z in cs.zeros], lag_ratio=0.15), run_time=0.8)

            # each zero emits its real wave: -2 Re(x^rho / rho), on a log-x axis u = ln x
            U0, U1 = np.log(10), np.log(3000)
            WX0, WX1 = -3.45, 6.3
            u2x = lambda u: WX0 + (WX1 - WX0) * (u - U0) / (U1 - U0)
            us = np.linspace(U0, U1, 1400)
            gam = [float(z) for z in zeta_zeros(6)]
            waves = VGroup()
            for g, z in zip(gam, cs.zeros):
                rho = complex(0.5, g)
                val = np.array([(-2 * np.exp(rho * u) / rho).real for u in us]) / np.exp(us / 2) * abs(rho)
                y0 = z.get_center()[1]
                amp = 0.12 * np.exp((us - U1) / 2 * 0.9) + 0.03
                pts = [np.array([u2x(u), y0 + a * v / 2, 0]) for u, v, a in zip(us, val, amp)]
                w = VMobject().set_points_smoothly(pts[::2]).set_stroke(ZERO, 2.5, opacity=0.85)
                waves.add(w)
            self.wait_until(self.cue("controlled by the zeros"))
            rem = self.cue("Riemann guessed") - (self.now() - self._beat_start) - 0.2
            self.play(LaggedStart(*[AnimationGroup(Flash(z, color=ZERO, line_length=0.15, flash_radius=0.16), Create(w))
                                    for z, w in zip(cs.zeros, waves)], lag_ratio=0.2), run_time=max(1.0, rem))

            # Riemann's guess: the line glows
            self.at("Riemann guessed", lead=0.1)
            glow = cs.line.copy().set_stroke(ZERO, 12, opacity=0.35)
            self.play(FadeIn(glow), cs.line.animate.set_stroke(width=5),
                      LaggedStart(*[z.animate.scale(1.4) for z in cs.zeros], lag_ratio=0.1), run_time=1.0)
            self.play(FadeOut(glow), LaggedStart(*[z.animate.scale(1 / 1.4) for z in cs.zeros], lag_ratio=0.1), run_time=0.8)

            # the waves add up to the real error psi(x) - x, which lives inside +-sqrt(x)
            YC, YS = -0.55, 2.1 / np.sqrt(3000)   # sqrt(3000) -> 2.1 units
            xs = np.exp(np.linspace(U0, U1, 2600))
            err = psi_minus_x(xs)
            epts = [np.array([u2x(np.log(x)), YC + YS * e, 0]) for x, e in zip(xs, err)]
            ecurve = VMobject().set_points_as_corners(epts).set_stroke(PRIME, 2.5)
            env = VGroup(*[ParametricFunction(lambda u, s=s: np.array([u2x(u), YC + s * YS * np.exp(u / 2), 0]), t_range=[U0, U1])
                           .set_stroke(INK, 2.5) for s in (1, -1)])
            env = VGroup(*[DashedVMobject(e, num_dashes=40) for e in env])
            axis = Line(np.array([WX0, YC, 0]), np.array([WX1, YC, 0])).set_stroke(MUTED, 2)
            lab = M(r"\pm\sqrt{x}", size=38).next_to(env[0][-1].get_end(), LEFT, buff=0.15).shift(UP * 0.35)
            self.wait_until(self.cue("which would make") - 0.3)
            tg = [ecurve.copy() for _ in waves]
            self.play(FadeIn(axis), *[ReplacementTransform(w, t) for w, t in zip(waves, tg)], run_time=1.4)
            self.remove(*tg); self.add(ecurve)
            self.at("coin flips", lead=0.6)
            self.play(Create(env), FadeIn(lab), run_time=min(1.2, self.left() - 0.1))
            a_stuff = VGroup(bc, cs, ecurve, env, lab, axis)

        # ============================================================ b: multiplicity -> tower -> scale settles
        with self.beat("b") as d:
            # vignette 1: a curve flattening at its zero (x^m)
            ax = Axes(x_range=[-1.1, 1.1, 1], y_range=[-1.5, 1.5, 1], x_length=3.0, y_length=2.8,
                      tips=False, axis_config=dict(stroke_color=MUTED, stroke_width=2, include_ticks=False)).move_to(LEFT * 4.75 + DOWN * 0.1)
            curve_of = lambda m: ax.plot(lambda x: x ** m, x_range=[-min(1.1, 1.5 ** (1 / m)), min(1.1, 1.5 ** (1 / m))], color=INK, stroke_width=4)
            crv = curve_of(1)
            zdot = Dot(ax.c2p(0, 0), radius=0.08, color=WARM).set_z_index(3)
            mlab = VGroup(M("m", "=", size=40, color=INK), Integer(1, font_size=40, color=WARM))
            mlab.arrange(RIGHT, buff=0.15).next_to(ax, DOWN, buff=0.35)
            v1 = VGroup(ax, crv, zdot, mlab); c0 = v1.get_center()
            v1.scale(1.5).move_to(DOWN * 0.1)
            self.play(FadeOut(a_stuff, run_time=0.6), Create(ax, run_time=0.6), Create(crv, run_time=0.8), FadeIn(zdot), FadeIn(mlab))
            self.at("parallel universe", lead=0.3)
            for m in (2, 3, 4, 5):
                self.play(Transform(crv, curve_of(m)), mlab[1].animate.set_value(m), run_time=0.75)

            # vignette 2: the tower of lifts
            self.at("towers", lead=0.9)
            tw = lift_tower(floors=6, labels=False).scale(0.62)
            tw.move_to(LEFT * 0.55 + DOWN * 0.35)
            self.play(v1.animate.scale(1 / 1.5).move_to(c0).set_stroke(opacity=0.55),
                      LaggedStart(*[AnimationGroup(FadeIn(f, shift=UP * 0.2), *( [GrowArrow(tw.arrows[i - 1])] if i else []))
                                    for i, f in enumerate(tw.floors)], lag_ratio=0.45), run_time=1.8)

            # vignette 3: the number at the top, on the balance
            self.at("A number too", lead=0.6)
            sc = balance_scale().scale(0.8).move_to(RIGHT * 3.9 + DOWN * 0.45)
            tilt = rig_scale(sc)
            tok = number_token("?").scale(0.8).move_to(tw.floors[-1].get_top() + UP * 0.45)
            spot = sc.pivot.get_center() + UP * 0.95 * 0.8
            self.play(FadeIn(sc), FadeIn(tok, scale=0.4), tilt.animate.set_value(0.22), run_time=0.8)
            self.play(tok.animate(path_arc=-0.9).move_to(spot), tw.animate.set_opacity(0.45), run_time=1.0)
            # rocks, then settles level
            t_settle = max(1.5, self.cue("unless the primes behave") + 1.0 - (self.now() - self._beat_start))
            t_settle = min(t_settle, self.left() - 0.6)
            amp0 = tilt.get_value()
            self.play(UpdateFromAlphaFunc(tilt, lambda m, a: m.set_value(amp0 * np.cos(3 * PI * a) * (1 - a) ** 1.6)),
                      run_time=t_settle, rate_func=linear)
            tilt.set_value(0)
            self.play(Indicate(sc.beam, color=GOOD, scale_factor=1.0), tok[1].animate.set_stroke(GOOD), run_time=min(0.6, max(0.2, self.left() - 0.05)))
            b_stuff = VGroup(ax, crv, zdot, mlab, tw, sc, tok)

        # ============================================================ c: primes, and the horizon of zeros
        with self.beat("c") as d:
            for m in sc.get_family(): m.clear_updaters()
            NL_Y = -2.1
            nl = NumberLine(x_range=[0, 41, 1], length=12.6, color=MUTED, stroke_width=2, include_ticks=False).move_to(UP * NL_Y)
            comp = VGroup(*[Dot(nl.n2p(n), radius=0.035, color=DIM) for n in range(1, 41) if n not in primes_upto(40)])
            pr = primes_upto(40)
            pdots = VGroup(*[glow_dot(nl.n2p(p), PRIME, r=0.075) for p in pr])
            pnums = VGroup(*[M(str(p), size=30, color=PRIME).next_to(nl.n2p(p), DOWN, buff=0.22) for p in pr])
            self.play(FadeOut(b_stuff, run_time=0.5), Create(nl, run_time=0.9), FadeIn(comp, run_time=0.8),
                      LaggedStart(*[AnimationGroup(FadeIn(dp, scale=0.3), FadeIn(pn, shift=UP * 0.1)) for dp, pn in zip(pdots, pnums)],
                                  lag_ratio=0.12, run_time=2.0))

            # the critical line, lying on its side, rises like a horizon with its zeros
            HY = 1.15
            gams = [g for g in zeta_zeros(40) if g < 101]
            band = VGroup(*[Rectangle(width=14.4, height=0.25 * k, stroke_width=0, fill_color=ZERO, fill_opacity=0.05) for k in (1, 2, 4, 7)])
            hline = Line(LEFT * 7.2, RIGHT * 7.2).set_stroke(ZERO, 3)
            zdots = VGroup(*[glow_dot(np.array([-6.3 + 12.6 * g / 101, 0, 0]), ZERO, r=0.06) for g in gams])
            horizon = VGroup(band, hline, zdots).move_to(UP * HY)
            rise = max(1.2, self.cue("Now the work") - (self.now() - self._beat_start))
            self.play(FadeIn(horizon, shift=UP * (HY - NL_Y - 0.4)), run_time=rise, rate_func=smooth)
            # hold with a gentle shimmer travelling along the zeros
            hold = max(0.8, self.left() - 1.0)
            self.play(LaggedStart(*[Indicate(z, color=INK, scale_factor=1.5) for z in zdots], lag_ratio=0.08), run_time=hold)
            self.play(FadeOut(VGroup(nl, comp, pdots, pnums, horizon)), run_time=min(0.9, max(0.3, self.left())))

        # end credit on black
        c1 = T("Proof: Levent Alpöge with Claude (November 2026)", size=30, color=INK)
        c2 = T("Explainer made with Claude", size=24, color=MUTED)
        cred = VGroup(c1, c2).arrange(DOWN, buff=0.22).move_to(DOWN * 0.1)
        self.play(FadeIn(cred, shift=UP * 0.1), run_time=0.9)
        self.wait(2.6)
        self.play(FadeOut(cred), run_time=0.7)
        self.finish()
