import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *

NZ = 100
XMAX = 50


def prime_powers(n):
    """[(p^k, p)] for all prime powers <= n, sorted."""
    out = []
    for p in primes_upto(n):
        q = p
        while q <= n:
            out.append((q, p)); q *= p
    return sorted(out)


def staircase_points(axes, xmax, x0=0.0):
    """Corner points of Chebyshev's psi on [x0, xmax] (jumps of ln p at prime powers)."""
    pts, y = [axes.c2p(x0, 0)], 0.0
    for q, p in prime_powers(int(xmax)):
        if q < x0: y += np.log(p); continue
        pts.append(axes.c2p(q, y)); y += np.log(p); pts.append(axes.c2p(q, y))
    pts.append(axes.c2p(xmax, y))
    return pts


class S08(NarratedScene):
    sid = "s08"

    def construct(self):
        gam = np.array(zeta_zeros(NZ))
        rho = 0.5 + 1j * gam
        xs = np.linspace(2.0, XMAX, 2400)
        base = xs - np.log(2 * np.pi) - 0.5 * np.log(1 - xs ** -2.0)
        TERMS = np.real(xs[None, :] ** rho[:, None] / rho[:, None])  # Re x^rho / rho
        ks = np.arange(NZ)

        def psi_approx(N):
            w = np.clip(N - ks, 0, 1)
            return base - 2 * (w @ TERMS)

        # ------------------------------------------------------------------ layout
        ax = Axes(x_range=[0, XMAX, 10], y_range=[0, XMAX, 10], x_length=8.8, y_length=6.3, tips=False,
                  axis_config=dict(color=MUTED, stroke_width=2, include_ticks=True, tick_size=0.05)).move_to(RIGHT * 2.0 + UP * 0.15)
        xnums = VGroup(*[M(str(v), size=24, color=MUTED).next_to(ax.c2p(v, 0), DOWN, buff=0.22) for v in range(10, XMAX + 1, 10)])
        ynums = VGroup(*[M(str(v), size=24, color=MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v in range(10, XMAX + 1, 10)])
        ptick = VGroup(*[Line(ax.c2p(q, 0) + DOWN * (0.13 if q == p else 0.07), ax.c2p(q, 0) + UP * (0.13 if q == p else 0.07))
                         .set_stroke(PRIME, 4 if q == p else 2.5, opacity=1 if q == p else 0.5) for q, p in prime_powers(XMAX)])
        stair = VMobject().set_points_as_corners(staircase_points(ax, XMAX)).set_stroke(PRIME, 4, opacity=0.38)
        stair_lab = T("prime staircase", size=26, color=PRIME).move_to(ax.c2p(40, 30)).set_opacity(0.8)

        strip = critical_strip(height=6.0, width=1.8, tmax=52, n_zeros=10).move_to(LEFT * 4.75 + DOWN * 0.05)

        # ================================================================== a
        with self.beat("a") as d:
            self.play(FadeIn(VGroup(strip[:4], strip.labels)), LaggedStart(*[GrowFromCenter(z) for z in strip.zeros], lag_ratio=0.12), run_time=1.4)
            self.play(Create(ax, run_time=1.2), FadeIn(xnums), FadeIn(ynums))
            self.play(Create(stair), LaggedStart(*[GrowFromCenter(t) for t in ptick], lag_ratio=0.05), FadeIn(stair_lab), run_time=1.8)
            self.at("Each zero contributes")
            # three zeros each emit a wave packet that flies to the staircase
            packets, anims = [], []
            for i in range(3):
                z = strip.zeros[i]
                g = gam[i]
                w = ParametricFunction(lambda t, g=g: np.array([t, 0.22 * np.exp(-(t / 0.45) ** 2) * np.sin(g * t * 0.9), 0]),
                                       t_range=[-0.9, 0.9, 0.01]).set_stroke(ZERO, 3)
                w.move_to(z.get_center())
                y_val = ax.p2c(z.get_center())[1]
                target = ax.c2p(y_val, y_val)
                packets.append(w)
                anims.append(Succession(
                    AnimationGroup(Flash(z, color=ZERO, line_length=0.18, flash_radius=0.18, run_time=0.5), FadeIn(w, run_time=0.3)),
                    w.animate(run_time=1.6, rate_func=rate_functions.ease_in_out_sine).move_to(target),
                    AnimationGroup(FadeOut(w, scale=1.6, run_time=0.4), Flash(target, color=PRIME, flash_radius=0.3, run_time=0.5))))
            self.play(LaggedStart(*anims, lag_ratio=0.35), run_time=min(3.6, self.left() - 0.2))

        # ================================================================== b  (hero)
        thin = critical_strip(height=6.6, width=1.0, tmax=245, n_zeros=NZ, labels=False).move_to(LEFT * 4.75 + UP * 0.12)
        for z in thin.zeros: z.scale(0.55).set_color(DIM)
        N = ValueTracker(0.0)

        def curve():
            ys = np.clip(psi_approx(N.get_value()), -1, XMAX + 2)
            return VMobject().set_points_as_corners(ax.c2p(xs, ys).T).set_stroke(INK, 3.5)

        def light_zeros(m):
            n = N.get_value()
            for k, z in enumerate(m.zeros):
                a = float(np.clip(n - k, 0, 1))
                z.set_color(interpolate_color(ManimColor(DIM), ManimColor(ZERO), a))
            return m

        cnt_lab = T("zeros used:", size=30, color=ZERO)
        cnt = Integer(0, font_size=40, color=ZERO)
        counter = VGroup(cnt_lab, cnt).arrange(RIGHT, buff=0.2).move_to(ax.c2p(13, 46))
        cnt.add_updater(lambda m: m.set_value(int(np.floor(N.get_value() + 1e-6))))
        formula = M(r"\psi(x)\approx x", r"\;-\;", r"\sum_{\rho}", r"\frac{x^{\rho}}{\rho}", size=40)
        formula[2].set_color(ZERO); formula[3].set_color(ZERO)
        formula.move_to(ax.c2p(14, 37))

        with self.beat("b") as d:
            self.play(ReplacementTransform(VGroup(strip[:4], strip.zeros), VGroup(thin[:4], thin.zeros)), FadeOut(strip.labels),
                      FadeOut(stair_lab), stair.animate.set_stroke(opacity=0.3), run_time=0.9)
            self.add(thin); thin.add_updater(light_zeros)
            hero = always_redraw(curve)
            h0 = curve()
            self.play(Create(h0, run_time=1.0, rate_func=linear), FadeIn(formula[0]), FadeIn(counter))
            self.remove(h0); self.add(hero)
            self.at("Add the wave from the first")
            self.play(FadeIn(formula[1:], shift=LEFT * 0.2), N.animate.set_value(1), run_time=1.1)
            self.at("Then the second")
            self.play(N.animate.set_value(2), run_time=0.8)
            self.at("Then ten")
            self.play(N.animate.set_value(10), run_time=1.3, rate_func=rate_functions.ease_in_out_sine)
            self.at("A hundred")
            self.play(N.animate.set_value(100), run_time=2.6, rate_func=rate_functions.ease_in_out_sine)
            self.at("land exactly")
            drops = VGroup(*[DashedLine(ax.c2p(p, 0), ax.c2p(p, np.log(p) + sum(np.log(pp) for q, pp in prime_powers(p) if q < p)),
                                        dash_length=0.07).set_stroke(PRIME, 2.5) for p in primes_upto(XMAX)])
            self.play(LaggedStart(*[Create(l) for l in drops], lag_ratio=0.08), stair.animate.set_stroke(opacity=0.6), run_time=1.6)
            self.wait_until(d - 1.6)
            self.play(LaggedStart(*[Indicate(t, color=PRIME, scale_factor=1.6) for t in ptick if t.get_stroke_width() > 3], lag_ratio=0.06), run_time=1.4)

        # ================================================================== c   (one zero = one wave)
        thin.clear_updaters()
        ms = critical_strip(height=6.0, width=2.2, tmax=40, n_zeros=1).move_to(LEFT * 4.6 + DOWN * 0.05)
        others = VGroup(*[Dot(ms.p2c(0.5, g), radius=0.05, color=DIM) for g in gam[1:6]])
        sig, gm = ValueTracker(0.5), ValueTracker(gam[0])
        U = np.log(100)
        wax = Axes(x_range=[0, U, U / 2], y_range=[-3, 3, 1], x_length=8.6, y_length=5.4, tips=False,
                   axis_config=dict(color=MUTED, stroke_width=2, include_ticks=False)).move_to(RIGHT * 2.1 + DOWN * 0.15)
        wnums = VGroup(*[M(s, size=26, color=MUTED).next_to(wax.c2p(u, -3), DOWN, buff=0.15) for s, u in [("1", 0), ("10", U / 2), ("100", U)]])
        wxl = M("x", size=30, color=MUTED).next_to(wax.c2p(U, -3), RIGHT, buff=0.15)
        A = 1.15 / np.exp(0.5 * U)
        us = np.linspace(0, U, 1400)
        YC = 3.5

        def wave_pts(s, g, ph=0.0):
            ys = np.clip(A * np.exp(s * us) * np.cos(g * us + ph), -YC, YC)
            return wax.c2p(us, ys).T

        def wavef():
            return VMobject().set_points_as_corners(wave_pts(sig.get_value(), gm.get_value())).set_stroke(ZERO, 3)

        zdot = Dot(ms.p2c(0.5, gam[0]), radius=0.09, color=ZERO).set_z_index(4)
        zdot.add_updater(lambda m: m.move_to(ms.p2c(sig.get_value(), gm.get_value())))
        hl = T("height  →  pitch", size=32, color=ZERO).move_to(wax.get_top() + UP * 0.35 + LEFT * 2.2)
        vl = T("left-right  →  volume", size=32, color=WARM).move_to(wax.get_top() + UP * 0.35 + RIGHT * 2.0)
        env = always_redraw(lambda: VGroup(*[VMobject().set_points_as_corners(wax.c2p(us, sgn * A * np.exp(sig.get_value() * us)).T)
                                             .set_stroke(WARM, 2.5, opacity=0.9) for sgn in (1, -1)]))

        with self.beat("c") as d:
            self.remove(thin); self.add(*thin[:4], *thin.zeros)
            wave = always_redraw(wavef)
            self.play(FadeOut(VGroup(hero, stair, ptick, drops, formula, counter, ax, xnums, ynums), run_time=0.8),
                      ReplacementTransform(thin[:4], ms[:4]), FadeOut(thin.zeros[6:]),
                      ReplacementTransform(thin.zeros[1:6], others), ReplacementTransform(thin.zeros[0], zdot),
                      FadeIn(ms.labels), run_time=1.0)
            self.add(zdot)
            self.play(Create(wax), FadeIn(wnums), FadeIn(wxl), run_time=0.8)
            w0 = wavef()
            self.play(TransformFromCopy(zdot, w0), run_time=0.9)
            self.remove(w0); self.add(wave)
            self.at("Its height")
            self.play(FadeIn(hl, shift=DOWN * 0.2), run_time=0.5)
            self.play(gm.animate.set_value(30), run_time=1.6, rate_func=there_and_back_with_pause)
            self.at("Its left-right")
            self.play(FadeIn(vl, shift=DOWN * 0.2), FadeIn(env), run_time=0.5)
            self.play(sig.animate.set_value(0.72), run_time=1.4)
            self.play(sig.animate.set_value(0.5), run_time=min(1.2, self.left() - 0.1))

        # ================================================================== d   (sqrt envelope + ghost)
        with self.beat("d") as d:
            env.clear_updaters()
            band = VGroup(*[wax.plot(lambda u, s=s: s * A * np.exp(0.5 * u), x_range=[0, U, U / 300]).set_stroke(GOOD, 3.5) for s in (1, -1)])
            fill = VMobject().set_points_as_corners([*wax.c2p(us, A * np.exp(0.5 * us)).T, *wax.c2p(us[::-1], -A * np.exp(0.5 * us[::-1])).T])
            fill.set_stroke(width=0).set_fill(GOOD, 0.12)
            sq = M(r"\sqrt{x}", size=40, color=GOOD).next_to(band[0].get_end(), UP, buff=0.15).shift(LEFT * 0.3)
            coin = T("coin-flip size", size=28, color=GOOD).next_to(sq, LEFT, buff=0.3)
            self.play(FadeOut(VGroup(hl, vl)), ReplacementTransform(env, band), FadeIn(fill), run_time=1.0)
            self.play(Write(sq), FadeIn(coin), run_time=0.8)
            self.at("A zero to the right")
            gsig, gg = 0.8, 21.0
            ghost = Dot(ms.p2c(gsig, gg), radius=0.09, color=BAD).set_z_index(4)
            ghalo = Circle(radius=0.2, color=BAD, stroke_width=2).move_to(ghost).set_stroke(opacity=0.8)
            self.play(wave.animate.set_stroke(opacity=0.35), FadeIn(ghost, scale=2), Create(ghalo), FadeOut(coin), run_time=0.7)
            ys = A * np.exp(gsig * us) * np.cos(gg * us + 0.4)
            bad = VMobject().set_points_as_corners(wax.c2p(us, np.clip(ys, -YC, YC)).T).set_stroke(BAD, 3.5)
            self.play(Create(bad), run_time=2.4, rate_func=linear)
            outside = np.abs(ys) > 1.25 * A * np.exp(0.5 * us)
            crest = [i for i in range(1, len(us) - 1) if outside[i] and abs(ys[i]) >= abs(ys[i - 1]) and abs(ys[i]) >= abs(ys[i + 1]) and abs(ys[i]) < YC]
            bl = M(r"x^{0.8}", size=44, color=BAD).move_to(wax.c2p(U * 0.45, 2.6))
            self.play(LaggedStart(*[Flash(wax.c2p(us[i], ys[i]), color=BAD, flash_radius=0.25, line_length=0.2) for i in crest[-4:]], lag_ratio=0.25),
                      Write(bl), run_time=1.4)
            # end card: two languages
            self.at("So 'all zeros")
            left = T("all zeros on the line", size=40, color=ZERO)
            right = VGroup(T("prime error ≈", size=40, color=GOOD), M(r"\sqrt{x}", size=46, color=GOOD)).arrange(RIGHT, buff=0.18)
            arrow = M(r"\Longleftrightarrow", size=80, color=INK)
            card = VGroup(left, arrow, right).arrange(RIGHT, buff=0.55).move_to(DOWN * 2.3)
            icon_strip = VGroup(ms[:4], others, zdot)
            zdot.clear_updaters()
            icon_wave = VGroup(wax, wave, band, fill, sq)
            wave.clear_updaters()
            self.play(FadeOut(VGroup(bad, ghost, ghalo, bl, wnums, wxl, ms.labels)), run_time=0.6)
            self.play(icon_strip.animate.scale(0.6).next_to(left, UP, buff=0.5),
                      icon_wave.animate.scale(0.5).next_to(right, UP, buff=0.5),
                      FadeIn(left, shift=UP * 0.2), FadeIn(right, shift=UP * 0.2), run_time=1.3)
            self.play(GrowFromCenter(arrow), run_time=0.7)
            self.play(wave.animate.set_stroke(opacity=1), Indicate(left, color=ZERO, scale_factor=1.08),
                      ms.line.animate.set_stroke(width=6), run_time=1.2)
            self.play(Indicate(right, color=GOOD, scale_factor=1.08), ms.line.animate.set_stroke(width=3),
                      band.animate.set_stroke(width=5), run_time=1.2)
            self.at("in two languages")
            self.play(Indicate(arrow, color=PRIME), band.animate.set_stroke(width=3.5), run_time=min(1.2, self.left() - 0.1))
        self.finish()
