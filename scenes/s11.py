import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *

# ---- "parallel universe" identity, same as s10 / s12: periwinkle tinted frame + clock icon in the corner.
PARA = "#8c9eff"


def clock_icon(r=0.2, color=PARA, n=7):
    c = Circle(radius=r).set_stroke(color, 2.5)
    ticks = VGroup(*[Line(UP * r * 0.68, UP * r).rotate(-TAU * k / n, about_point=ORIGIN) for k in range(n)]).set_stroke(color, 2)
    hand = Line(ORIGIN, UP * r * 0.62).rotate(-TAU * 2 / n, about_point=ORIGIN).set_stroke(color, 2.5)
    return VGroup(c, ticks, hand)


def full_frame():
    rect = RoundedRectangle(corner_radius=0.3, width=13.1, height=7.1).set_stroke(PARA, 3).set_fill(PARA, 0.05)
    icon = clock_icon(r=0.2).move_to(rect.get_corner(UL) + RIGHT * 0.45 + DOWN * 0.42)
    g = VGroup(rect, icon); g.rect, g.icon = rect, icon
    return g


def gear(r=1.0, teeth=10, color=MUTED, width=3):
    pts = []
    for k in range(teeth):
        a0 = TAU * k / teeth
        for da, rr in [(0.0, r), (0.18, r), (0.25, r * 1.22), (0.43, r * 1.22), (0.5, r)]:
            pts.append([rr * np.cos(a0 + da * TAU / teeth), rr * np.sin(a0 + da * TAU / teeth), 0])
    body = VMobject().set_points_as_corners(pts + [pts[0]]).set_stroke(color, width)
    hole = Circle(radius=r * 0.35).set_stroke(color, width)
    return VGroup(body, hole)


def cheb(n, u):
    return np.cos(n * np.arccos(np.clip(u, -1, 1)))


class S11(NarratedScene):
    sid = "s11"

    def construct(self):
        F = full_frame()
        # ============================================================== a: degree d => at most d zeros
        with self.beat("a") as d:
            # Weil's proof: heavy clockwork, turning
            g1 = gear(1.0, 12).move_to([-1.0, -0.3, 0]); g2 = gear(0.62, 8).move_to([0.75, 0.45, 0]); g3 = gear(0.5, 7).move_to([0.55, -1.35, 0])
            g4 = gear(0.42, 6).move_to([-2.45, 0.85, 0])
            gears = VGroup(g1, g2, g3, g4)
            spin = [lambda m, dt: m.rotate(0.9 * dt), lambda m, dt: m.rotate(-1.5 * dt), lambda m, dt: m.rotate(-1.8 * dt),
                    lambda m, dt: m.rotate(-2.1 * dt)]
            for g, f in zip(gears, spin): g.add_updater(f)
            wl = T("Weil's proof", 32, MUTED).next_to(gears, DOWN, buff=0.45)
            self.play(FadeIn(F), FadeIn(gears, scale=0.8), FadeIn(wl), run_time=0.6)
            self.at("Stepanov", lead=0.2)
            title = T("Stepanov, 1969", 44, weight=MEDIUM).move_to(UP * 2.55)
            self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.7)
            # "almost no machinery": the clockwork is thrown away
            self.at("almost no machinery", lead=0.1)
            self.play(gears.animate.scale(0.05).set_opacity(0), FadeOut(wl), run_time=0.8)
            for g in gears: g.clear_updaters()
            self.remove(gears)

            # one humble fact: a real degree-5 polynomial
            self.at("one humble fact", lead=0.4)
            roots = [-2.6, -1.4, -0.1, 1.3, 2.5]
            f0 = lambda x: np.prod([x - r for r in roots])
            k = 1.7 / 11.65
            xs = np.linspace(-3.2, 3.2, 4001)
            ok = xs[np.abs([k * f0(x) for x in xs]) <= 2.3]
            x_lo, x_hi = ok.min(), ok.max()
            ax = Axes(x_range=[-3.2, 3.2, 1], y_range=[-2.4, 2.4, 1], x_length=12.0, y_length=4.4, tips=False,
                      axis_config=dict(color=MUTED, stroke_width=2, include_ticks=False)).move_to(DOWN * 0.75)
            ax.y_axis.set_opacity(0)
            poly = ax.plot(lambda x: k * f0(x), x_range=[x_lo, x_hi], color=INK, stroke_width=4)
            self.play(title.animate.set_opacity(0.0), Create(ax.x_axis), run_time=0.5)
            self.remove(title)
            self.play(Create(poly), run_time=1.4)

            self.at("degree d", lead=0.6)
            lab5 = T("degree 5", 40).move_to(UP * 2.55)
            self.play(FadeIn(lab5), run_time=0.4)
            rdots = VGroup(*[VGroup(Dot(ax.c2p(r, 0), radius=0.2, color=PARA).set_opacity(0.3), Dot(ax.c2p(r, 0), radius=0.1, color=PARA))
                             for r in roots])
            nums = VGroup(*[M(str(i + 1), size=40, color=PARA).next_to(ax.c2p(r, 0), DOWN if i % 2 == 0 else UP, buff=0.35).shift(RIGHT * 0.25)
                            for i, r in enumerate(roots)])
            # numbers sit on the side the curve is NOT on
            for i, r in enumerate(roots):
                slope = k * (f0(r + 1e-3) - f0(r - 1e-3))
                nums[i].next_to(ax.c2p(r, 0), DOWN if slope > 0 else UP, buff=0.3).shift(RIGHT * 0.32)
            tcount = min(1.8, self.left() - 1.6)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(rd, scale=2.5), FadeIn(n)) for rd, n in zip(rdots, nums)], lag_ratio=0.5),
                      run_time=tcount)
            labd = T("degree d   →   at most d zeros", 40, t2c={"d": WARM}).move_to(UP * 2.55)
            lab5b = T("degree 5   →   at most 5 zeros", 40).move_to(UP * 2.55)
            self.play(TransformMatchingShapes(lab5, lab5b), run_time=0.6)
            self.play(Transform(lab5b, labd), run_time=min(0.8, max(0.3, self.left() - 0.1)))

        # ============================================================== b: points -> helper polynomial
        a6 = 2.9
        P = lambda x: cheb(6, x / a6)         # Chebyshev T6: degree 6, all bumps the same height
        proots = [a6 * np.cos((2 * j - 1) * PI / 12) for j in range(6, 0, -1)]
        A = 1.7
        with self.beat("b") as d:
            self.play(FadeOut(VGroup(poly, rdots, nums)), lab5b.animate.set_opacity(0), run_time=0.6)
            self.remove(lab5b)
            pts = VGroup(*[VGroup(Dot(ax.c2p(r, 0), radius=0.2, color=PARA).set_opacity(0.3), Dot(ax.c2p(r, 0), radius=0.1, color=PARA))
                           for r in proots])
            self.at("too many points", lead=0.8)
            q = M(r"\#\,\text{points} = \,?", size=46, color=PARA).move_to(UP * 2.55)
            self.play(LaggedStart(*[FadeIn(pt, shift=DOWN * 1.2) for pt in pts], lag_ratio=0.2), FadeIn(q), run_time=1.3)
            self.at("helper polynomial", lead=0.5)
            mtr = ValueTracker(1.0)

            def helper_val(x, m):
                kk = int(np.floor(m)); t = m - kk
                if t < 1e-6: return A * P(x) ** kk
                return A * ((1 - t) * P(x) ** kk + t * P(x) ** (kk + 1))
            helper = always_redraw(lambda: ax.plot(lambda x: helper_val(x, mtr.get_value()), x_range=[-a6, a6], color=WARM, stroke_width=4)
                                   .set_z_index(-1))
            hl = T("helper", 32, WARM).move_to(ax.c2p(-a6, A) + RIGHT * 0.2 + UP * 0.35)
            h0 = helper.copy().clear_updaters()
            self.play(Create(h0), run_time=1.6)
            self.remove(h0); self.add(helper)
            self.play(FadeIn(hl), Indicate(pts, color=PARA, scale_factor=1.3), run_time=0.9)
            self.at("at most its degree", lead=0.6)
            ineq = M(r"\#\,\text{points}", r"\;\le\;", r"\text{degree}", size=50).move_to(UP * 2.55)
            ineq[0].set_color(PARA); ineq[2].set_color(WARM)
            self.play(TransformMatchingShapes(q, ineq), run_time=0.8)

        # ============================================================== c: multiplicity — flat at each point
        with self.beat("c") as d:
            self.play(ineq.animate.set_opacity(0.35), Wiggle(ineq, scale_value=1.05), run_time=0.9)
            self.at("something clever", lead=0.4)
            main = VGroup(ax, pts, hl)
            # shrink the stage to the left; open a magnifier on one point at the right
            self.play(FadeOut(ineq), FadeOut(hl), main.animate.scale(0.6).move_to([-2.65, -0.35, 0]), run_time=0.9)
            main.remove(hl)
            r0 = proots[3]
            focus = pts[3]
            lens_c, lens_r = np.array([4.1, -0.35, 0]), 2.0
            lens = Circle(radius=lens_r).move_to(lens_c).set_stroke(INK, 3).set_fill(BG, 1)
            ring = Circle(radius=0.38).move_to(focus.get_center()).set_stroke(INK, 3)
            conn = VGroup(Line(ring.get_top(), lens.get_top()), Line(ring.get_bottom(), lens.get_bottom())).set_stroke(INK, 1.5, opacity=0.5)
            lax = Line(lens_c + LEFT * lens_r, lens_c + RIGHT * lens_r).set_stroke(MUTED, 2)
            s_loc = np.sign(helper_val(r0 + 1e-3, 1) - helper_val(r0 - 1e-3, 1))

            def local(m):
                kk = int(np.floor(m)); t = m - kk
                fx = lambda u: (1 - t) * (s_loc * u) ** kk + t * (s_loc * u) ** (kk + 1) if t > 1e-6 else (s_loc * u) ** kk
                return ParametricFunction(lambda u: lens_c + np.array([u * 1.35, 1.35 * fx(u), 0]), t_range=[-1, 1],
                                          stroke_width=6, color=WARM)
            lcurve = always_redraw(lambda: local(mtr.get_value()))
            ldot = Dot(lens_c, radius=0.12, color=PARA).set_z_index(5)
            mlab = always_redraw(lambda: M(rf"m = {int(round(mtr.get_value()))}", size=48, color=PARA).next_to(lens, UP, buff=0.25))
            self.play(Create(ring), Create(conn), FadeIn(lens), run_time=0.6)
            self.add(lax, lcurve, ldot, mlab)
            self.play(FadeIn(VGroup(lax, ldot)), run_time=0.3)

            self.at("many times over", lead=0.3)
            self.play(mtr.animate.set_value(2), run_time=1.3)
            self.at("but flat there", lead=0.4)
            self.play(mtr.animate.set_value(3), run_time=1.2)
            self.at("Flat to order m", lead=0.3)
            self.play(mtr.animate.set_value(4), run_time=1.2)
            self.at("multiplicity", lead=0.3)
            mult = T("multiplicity", 40, PARA).next_to(lens, DOWN, buff=0.3)
            self.play(FadeIn(mult, shift=UP * 0.2), run_time=0.6)

        # ============================================================== d: the budget — #points x m <= degree
        with self.beat("d") as d:
            helper.clear_updaters(); lcurve.clear_updaters(); mlab.clear_updaters()
            m = 4
            # the (shrunk) helper moves up; the magnifier goes away
            self.play(FadeOut(VGroup(lens, lcurve, ldot, lax, ring, conn, mult)), mlab.animate.move_to([4.6, 2.25, 0]),
                      VGroup(main, helper).animate.scale(0.95).move_to([-1.4, 1.55, 0]), run_time=0.8)
            # budget bar: degree = 6 points x 4 = 24 slots
            n_slots, sw = 24, 0.48
            bar_y = -1.05
            slots = VGroup(*[Square(side_length=sw).set_stroke(WARM, 2).set_fill(WARM, 0.08) for _ in range(n_slots)]).arrange(RIGHT, buff=0)
            slots.move_to([0, bar_y, 0])
            blab = T("degree", 32, WARM).next_to(slots, UP, buff=0.22).align_to(slots, LEFT)
            self.play(FadeIn(slots, lag_ratio=0.03), FadeIn(blab), run_time=0.8)
            self.at("each point uses up", lead=0.1)
            blocks = VGroup()
            tb = max(0.25, min(0.45, (self.cue("So the number") - (self.now() - self._beat_start) - 0.2) / 6))
            for i, pt in enumerate(pts):
                blk = RoundedRectangle(corner_radius=0.06, width=sw * m - 0.08, height=sw - 0.04).move_to(slots[i * m:(i + 1) * m]).set_stroke(PARA, 3).set_fill(PARA, 0.55)
                fly = pt[1].copy()
                self.play(fly.animate.move_to(blk), run_time=tb * 0.5)
                self.play(ReplacementTransform(fly, blk), run_time=tb * 0.5)
                blocks.add(blk)
                if i == 0:
                    brace = Brace(blk, DOWN, buff=0.08, color=PARA)
                    bm = M("m", size=40, color=PARA).next_to(brace, DOWN, buff=0.08)
                    self.add(brace, bm)
            self.at("So the number", lead=0.2)
            ineq2 = M(r"\#\,\text{points}", r"\times", r"m", r"\;\le\;", r"\text{degree}", size=52).move_to([0, -2.75, 0])
            ineq2[0].set_color(PARA); ineq2[2].set_color(PARA); ineq2[4].set_color(WARM)
            self.play(FadeOut(VGroup(brace, bm)), Write(ineq2), run_time=1.0)

            # crank up m: the bound on #points comes down toward p+1, to within a square root
            self.at("Crank up", lead=0.4)
            ineq3 = M(r"\#\,\text{points}", r"\;\le\;", r"{\text{degree}", r"\over", r"m}", size=52)
            ineq3[0].set_color(PARA); ineq3[2].set_color(WARM); ineq3[4].set_color(PARA)
            ineq3.move_to([0, 2.45, 0])
            self.play(FadeOut(VGroup(main, helper, slots, blocks, blab)), mlab.animate.set_opacity(0),
                      TransformMatchingTex(ineq2, ineq3), run_time=0.9)
            self.remove(mlab)
            # dial for m
            dc, dr = np.array([-4.3, -0.6, 0]), 1.25
            mt = ValueTracker(1)
            arcbg = Arc(radius=dr, start_angle=PI * 1.25, angle=-PI * 1.5, arc_center=dc).set_stroke(DIM, 10)
            arcfg = always_redraw(lambda: Arc(radius=dr, start_angle=PI * 1.25, angle=-PI * 1.5 * (mt.get_value() - 1) / 19 - 1e-3,
                                              arc_center=dc).set_stroke(PARA, 10))
            needle = always_redraw(lambda: Line(dc, dc + dr * 0.8 * np.array([np.cos(PI * 1.25 - PI * 1.5 * (mt.get_value() - 1) / 19),
                                                                                 np.sin(PI * 1.25 - PI * 1.5 * (mt.get_value() - 1) / 19), 0])).set_stroke(INK, 5))
            hub = Dot(dc, radius=0.09, color=INK)
            mval = always_redraw(lambda: M(rf"m = {int(round(mt.get_value()))}", size=42, color=PARA).move_to(dc + DOWN * (dr + 0.15)))
            # gauge: possible #points
            gy, g0, g1 = -0.6, -1.7, 6.2
            gl = Line([g0, gy, 0], [g1, gy, 0]).set_stroke(MUTED, 3)
            xc, hw = 1.4, 0.9
            band = Rectangle(width=2 * hw, height=0.5).move_to([xc, gy, 0]).set_stroke(width=0).set_fill(GOOD, 0.3)
            ctick = Line(UP * 0.3, DOWN * 0.3).move_to([xc, gy, 0]).set_stroke(INK, 3)
            clab = M("p+1", size=36).next_to(ctick, DOWN, buff=0.35)
            glab = T("points", 28, PARA).next_to(gl, UP, buff=0.35).align_to(gl, LEFT)
            xb = lambda mm: min(g1, xc + hw + 6.5 / mm ** 1.1)
            bound = always_redraw(lambda: VGroup(Line([xb(mt.get_value()), gy + 0.55, 0], [xb(mt.get_value()), gy - 0.55, 0]).set_stroke(WARM, 5),
                                                 Triangle(fill_color=WARM, fill_opacity=1, stroke_width=0).scale(0.13).rotate(PI)
                                                 .move_to([xb(mt.get_value()), gy + 0.7, 0])))
            ruled = always_redraw(lambda: Rectangle(width=max(1e-3, g1 - xb(mt.get_value())), height=0.5).set_stroke(width=0)
                                  .set_fill(BAD, 0.22).move_to([(g1 + xb(mt.get_value())) / 2, gy, 0]))
            self.play(FadeIn(VGroup(arcbg, hub, gl, band, ctick, clab, glab)), run_time=0.6)
            self.add(arcfg, needle, mval, ruled, bound)
            tr = max(1.5, self.left() - 2.2)
            self.play(mt.animate.set_value(20), run_time=tr, rate_func=rate_functions.ease_in_out_sine)
            br = BraceBetweenPoints([xc - hw, gy + 0.3, 0], [xc, gy + 0.3, 0], UP, color=GOOD)
            brl = M(r"\approx\sqrt{p}", size=36, color=GOOD).next_to(br, UP, buff=0.1)
            self.play(FadeIn(br), FadeIn(brl), run_time=min(0.6, max(0.2, self.left() - 0.1)))
        self.finish()
