import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *

# ---------------------------------------------------------------- "two universes" identity (shared look with s11, s12)
# our universe (whole numbers): plain thin white frame, number-line icon.
# parallel universe (clock arithmetic): periwinkle tinted frame, clock icon.
PARA = "#8c9eff"
PANEL_W, PANEL_H, PANEL_Y = 6.4, 6.9, -0.1


def clock_icon(r=0.2, color=PARA, n=7):
    c = Circle(radius=r).set_stroke(color, 2.5)
    ticks = VGroup(*[Line(UP * r * 0.68, UP * r).rotate(-TAU * k / n, about_point=ORIGIN) for k in range(n)]).set_stroke(color, 2)
    hand = Line(ORIGIN, UP * r * 0.62).rotate(-TAU * 2 / n, about_point=ORIGIN).set_stroke(color, 2.5)
    return VGroup(c, ticks, hand)


def ours_icon(color=INK):
    ln = Line(LEFT * 0.26, RIGHT * 0.3).set_stroke(color, 2.5)
    ticks = VGroup(*[Line(UP * 0.07, DOWN * 0.07).move_to(RIGHT * x) for x in (-0.2, -0.05, 0.1, 0.25)]).set_stroke(color, 2.5)
    return VGroup(ln, ticks)


def universe_panel(side):
    """side = -1: our universe (left), +1: parallel universe (right)."""
    rect = RoundedRectangle(corner_radius=0.25, width=PANEL_W, height=PANEL_H).move_to(RIGHT * 3.4 * side + UP * PANEL_Y)
    if side < 0:
        rect.set_stroke(INK, 2, opacity=0.45).set_fill(BG, 0)
        icon, lab = ours_icon(), T("our universe", 30, INK)
    else:
        rect.set_stroke(PARA, 3).set_fill(PARA, 0.07)
        icon, lab = clock_icon(), T("parallel universe", 30, PARA)
    head = VGroup(icon, lab).arrange(RIGHT, buff=0.22).move_to(rect.get_top() + DOWN * 0.45)
    g = VGroup(rect, head)
    g.rect, g.head, g.icon, g.lab = rect, head, icon, lab
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


class S12(NarratedScene):
    sid = "s12"

    def construct(self):
        L, R = universe_panel(-1), universe_panel(+1)
        Lc, Rc = L.rect.get_center(), R.rect.get_center()
        # ============================================================== a: flatness is measured with a derivative
        with self.beat("a") as d:
            primes = T("2  3  5  7  11  13  …", 40, PRIME).move_to(Lc + UP * 0.2)
            speed = ValueTracker(1.6)
            eng = gear(0.75, 10, color=PARA, width=4).move_to(Rc + UP * 0.35)
            eng.add_updater(lambda m, dt: m.rotate(-speed.get_value() * dt))
            eng_l = T("multiplicity", 30, PARA).next_to(eng, DOWN, buff=0.4)
            self.play(Create(L.rect), Create(R.rect), FadeIn(L.head), FadeIn(R.head), run_time=0.7)
            self.play(FadeIn(primes, lag_ratio=0.1), FadeIn(eng, scale=0.7), FadeIn(eng_l), run_time=0.8)
            arc = ArcBetweenPoints(Rc + LEFT * 1.3 + UP * 1.2, Lc + RIGHT * 0.9 + UP * 0.9, angle=PI / 3)
            br = DashedVMobject(arc, num_dashes=16).set_stroke(INK, 3)
            qm = M("?", size=60, color=INK).next_to(arc.point_from_proportion(0.5), UP, buff=0.12)
            self.play(Create(br), run_time=1.0)
            self.play(FadeIn(qm, scale=1.4), run_time=0.4)

            # flatness: a tangent slides along a real curve until it lies flat
            self.at("how you measure flatness", lead=0.3)
            eng_small = VGroup(eng, eng_l)
            self.play(FadeOut(br), FadeOut(qm), eng.animate.scale(0.45).move_to(R.rect.get_corner(UR) + LEFT * 0.8 + DOWN * 1.1),
                      eng_l.animate.set_opacity(0), run_time=0.7)
            self.remove(eng_l)
            ax = Axes(x_range=[-2.5, 1.5, 1], y_range=[-0.4, 1.5, 1], x_length=5.0, y_length=2.4, tips=False,
                      axis_config=dict(color=MUTED, stroke_width=2, include_ticks=False)).move_to(Rc + UP * 0.75)
            ax.y_axis.set_opacity(0)
            f = lambda x: 0.32 * x * x * (x + 2.3)
            fp = lambda x: 0.32 * (3 * x * x + 4.6 * x)
            curve = ax.plot(f, x_range=[-2.3, 1.15], color=WARM, stroke_width=4)
            self.play(Create(ax.x_axis), Create(curve), run_time=0.8)
            xt = ValueTracker(-1.9)

            def tangent():
                x = xt.get_value(); s = fp(x)
                p0, p1 = ax.c2p(x - 0.8, f(x) - 0.8 * s), ax.c2p(x + 0.8, f(x) + 0.8 * s)
                return Line(p0, p1).set_stroke(INK, 4)
            tan = always_redraw(tangent)
            tdot = always_redraw(lambda: Dot(ax.c2p(xt.get_value(), f(xt.get_value())), radius=0.09, color=INK))
            slope = always_redraw(lambda: VGroup(T("slope", 28, MUTED), DecimalNumber(abs(fp(xt.get_value())) if abs(fp(xt.get_value())) < 5e-3 else fp(xt.get_value()),
                                                                                       num_decimal_places=2, font_size=36, include_sign=False))
                                  .arrange(RIGHT, buff=0.2).move_to(Rc + DOWN * 0.95))
            self.add(tan, tdot, slope)
            self.at("take its derivative", lead=1.4)
            self.play(xt.animate.set_value(0.0), run_time=1.8, rate_func=smooth)
            tan.clear_updaters(); tdot.clear_updaters(); slope.clear_updaters()
            flat = M(r"\text{flat}", r"\iff", r"\text{derivative} = 0", size=40).move_to(Rc + DOWN * 1.7)
            self.play(tan.animate.set_stroke(GOOD), tdot.animate.set_color(GOOD), slope[1].animate.set_color(GOOD), Write(flat), run_time=0.8)

            # in clock-arithmetic land there is an x to differentiate with
            self.at("extra variables", lead=0.3)
            poly = M(r"x^3 + x + 1", size=42).move_to(Rc + DOWN * 2.7)
            self.play(FadeIn(poly, shift=UP * 0.2), run_time=0.5)
            ddx = M(r"\frac{d}{dx}", size=42, color=PARA)
            dpoly = M(r"\frac{d}{dx}", r"\big(x^3 + x + 1\big)", r"=", r"3x^2 + 1", size=40).move_to(Rc + DOWN * 2.7)
            dpoly[0].set_color(PARA); dpoly[3].set_color(PARA)
            ddx.move_to(dpoly[0]).shift(UP * 0.6)
            self.play(FadeIn(ddx, shift=DOWN * 0.3), run_time=0.4)
            self.play(ReplacementTransform(ddx, dpoly[0]), ReplacementTransform(poly, dpoly[1]), run_time=0.5)
            self.play(Write(dpoly[2:]), run_time=min(0.8, max(0.3, self.left() - 0.1)))

        # ============================================================== b: d/d? of 17 bounces off
        with self.beat("b") as d:
            n17 = M("17", size=150, color=PRIME).move_to(Lc + DOWN * 0.3)
            self.play(FadeOut(primes, shift=UP * 0.3), FadeIn(n17, scale=0.8), run_time=0.7)
            self.at("derivative of seventeen", lead=0.9)
            dq = M(r"\frac{d}{d\,?}", size=60, color=PARA).move_to(dpoly[0].get_center())
            self.play(dq.animate.move_to(n17.get_top() + UP * 1.4 + LEFT * 0.1), run_time=0.7, path_arc=-PI / 3)
            for k in range(2):
                self.play(dq.animate.next_to(n17, UP, buff=0.0), run_time=0.25, rate_func=rate_functions.rush_into)
                self.play(dq.animate.move_to(n17.get_top() + UP * (1.35 - 0.15 * k) + RIGHT * (0.5 if k == 0 else -0.6)).rotate(0.35 * (1 - 2 * k)),
                          Wiggle(n17, scale_value=1.05, rotation_angle=0.03 * TAU, run_time=0.5), run_time=0.45,
                          rate_func=rate_functions.rush_from)
            qq = M("???", size=56, color=MUTED).next_to(n17, DOWN, buff=0.45)
            self.play(FadeIn(qq), dq.animate.set_opacity(0.4), run_time=0.4)

            # the engine is carried over... and stalls
            self.at("Multiplicity, the engine", lead=0.2)
            eng_l2 = T("multiplicity", 30, PARA).move_to(Lc + DOWN * 2.6)
            self.play(FadeOut(qq), FadeOut(dq), n17.animate.scale(0.6).move_to(Lc + UP * 1.35),
                      eng.animate.scale(1 / 0.45).move_to(Lc + DOWN * 0.6), FadeIn(eng_l2), run_time=1.0)
            self.play(speed.animate.set_value(0.25), eng.animate.set_color(MUTED), run_time=0.8, rate_func=rate_functions.there_and_back_with_pause)
            jit = lambda m, dt: m.rotate(0.12 * np.sin(self.renderer.time * 23) * dt * 20 * (1 if speed.get_value() > 0.05 else 0))
            eng.add_updater(jit)
            self.play(speed.animate.set_value(0.0), eng.animate.set_color(DIM), eng_l2.animate.set_color(DIM), run_time=min(1.6, max(0.5, self.left() - 0.3)))
            eng.clear_updaters()

        # ============================================================== c: a descendant, a substitute, and the road
        with self.beat("c") as d:
            lineage = VGroup(T("Stepanov, 1969", 34, PARA), Arrow(LEFT * 0.6, RIGHT * 0.6, buff=0, stroke_width=4, color=INK, tip_length=0.2),
                             T("Alpöge, 2026", 34, INK)).arrange(RIGHT, buff=0.35).move_to(UP * 2.55)
            others = VGroup(L, R, n17, ax.x_axis, curve, tan, tdot, slope, flat, dpoly)
            self.play(FadeOut(others), eng.animate.move_to(DOWN * 0.3), eng_l2.animate.move_to(DOWN * 2.1), run_time=0.8)
            self.play(FadeIn(lineage[0], shift=RIGHT * 0.2), GrowArrow(lineage[1]), FadeIn(lineage[2], shift=RIGHT * 0.2), run_time=0.9)
            self.at("a substitute", lead=0.3)
            sub = T("a substitute for multiplicity", 34, LIFT).move_to(eng_l2)
            spd = ValueTracker(0.0)
            eng.add_updater(lambda m, dt: m.rotate(-spd.get_value() * dt))
            self.play(eng.animate.set_color(LIFT), Transform(eng_l2, sub), spd.animate.set_value(1.6), run_time=1.0)
            ints = T("over the whole numbers", 28, INK).next_to(eng_l2, DOWN, buff=0.2)
            self.play(FadeIn(ints), run_time=0.4)

            # the roadmap, revealed from the destination backwards
            self.at("a long road", lead=0.4)
            rm = roadmap(active=3).shift(UP * 0.4)
            st, ln = rm.stations, rm.links
            self.play(FadeOut(VGroup(lineage, eng_l2, ints)), eng.animate.scale(0.0).set_opacity(0).move_to(st[0][0]), run_time=0.6)
            eng.clear_updaters(); self.remove(eng)
            order = [st[3], ln[2], st[2], ln[1], st[1], ln[0], st[0]]
            self.play(LaggedStart(*[FadeIn(o, shift=LEFT * 0.35) for o in order], lag_ratio=0.35), run_time=2.2)
            self.at("start at the destination", lead=0.3)
            ring = Circle(radius=0.42).move_to(st[3][0]).set_stroke(PRIME, 4)
            self.play(Create(ring), st[3][0].animate.scale(1.2), run_time=0.6)
            self.play(st[3][0].animate.scale(1 / 1.2), run_time=0.3)
            self.at("work backwards", lead=0.3)
            back = CurvedArrow(st[3][0].get_top() + UP * 0.15, st[2][0].get_top() + UP * 0.15, angle=PI / 2.5, color=PRIME, stroke_width=4,
                               tip_length=0.2)
            self.play(Create(back), st[2][0].animate.set_stroke(PRIME), st[2][1].animate.set_color(PRIME),
                      run_time=min(0.9, max(0.3, self.left() - 0.05)))
        self.finish()
