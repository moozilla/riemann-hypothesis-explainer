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


def full_frame():
    """Whole screen inside the parallel universe: tinted frame + clock icon in the corner."""
    rect = RoundedRectangle(corner_radius=0.3, width=13.1, height=7.1).set_stroke(PARA, 3).set_fill(PARA, 0.05)
    icon = clock_icon(r=0.2).move_to(rect.get_corner(UL) + RIGHT * 0.45 + DOWN * 0.42)
    g = VGroup(rect, icon); g.rect, g.icon = rect, icon
    return g


def check(color=GOOD, s=1.0, width=8):
    return VMobject().set_points_as_corners([LEFT * 0.38 + UP * 0.02, DOWN * 0.3 + LEFT * 0.08, RIGHT * 0.42 + UP * 0.4]).set_stroke(color, width).scale(s)


def curve_count(p):
    """#points on y^2 = x^3 + x + 1 over the p-hour clock, plus the point at infinity."""
    sq = [0] * p
    for y in range(p): sq[y * y % p] += 1
    return 1 + sum(sq[(x ** 3 + x + 1) % p] for x in range(p))


class S10(NarratedScene):
    sid = "s10"

    def construct(self):
        # ============================================================== a: timeline, then the split
        with self.beat("a") as d:
            y0, x0, x1 = 0.2, -5.4, 5.4
            yx = lambda yr: x0 + (x1 - x0) * (yr - 1859) / (2026 - 1859)
            base = Line([x0, y0, 0], [x1, y0, 0]).set_stroke(DIM, 4)
            t0 = Line(UP * 0.18, DOWN * 0.18).set_stroke(MUTED, 3).move_to([x0, y0, 0])
            t1 = t0.copy().move_to([x1, y0, 0])
            l0 = M("1859", size=40, color=MUTED).next_to(t0, DOWN, buff=0.25)
            l1 = M("2026", size=40, color=MUTED).next_to(t1, DOWN, buff=0.25)
            yr = ValueTracker(1859)
            trail = always_redraw(lambda: Line([x0, y0, 0], [yx(yr.get_value()) + 1e-3, y0, 0]).set_stroke(INK, 4))
            runner = always_redraw(lambda: Dot([yx(yr.get_value()), y0, 0], radius=0.1, color=INK))
            year = always_redraw(lambda: Integer(int(yr.get_value()), group_with_commas=False, font_size=34, color=INK)
                                 .next_to(runner, UP, buff=0.25))
            self.play(Create(base), FadeIn(t0, t1, l0, l1), run_time=0.6)
            self.add(trail, runner, year)
            # failed attempts: little red sparks that die out as the years go by
            att_years = [1885, 1901, 1914, 1932, 1949, 1962, 1975, 1989, 1998, 2004, 2015]
            run = 0.36 * d
            marks = VGroup()
            anims = [yr.animate(rate_func=linear, run_time=run).set_value(2026)]
            for k, ay in enumerate(att_years):
                h = 0.55 + 0.35 * ((k * 7) % 3)
                mk = VGroup(Line([yx(ay), y0, 0], [yx(ay), y0 - h, 0]).set_stroke(BAD, 3),
                            Dot([yx(ay), y0 - h, 0], radius=0.06, color=BAD))
                marks.add(mk)
                tt = run * (ay - 1859) / (2026 - 1859)
                anims.append(Succession(Wait(tt), Create(mk, run_time=0.2), mk.animate(run_time=0.6).set_color(DIM)))
            self.play(*anims)
            self.remove(year); trail.clear_updaters(); runner.clear_updaters()
            fin = Integer(2026, group_with_commas=False, font_size=34, color=INK).next_to(runner, UP, buff=0.25)
            self.add(fin)

            self.at("one clue", lead=0.4)
            tl = VGroup(base, t0, t1, l0, l1, trail, runner, fin, marks)
            L, R = universe_panel(-1), universe_panel(+1)
            self.play(tl.animate.scale(0.5).shift(UP * 4.5).set_opacity(0), run_time=0.7)
            self.remove(tl)
            self.play(Create(L.rect), Create(R.rect), FadeIn(L.head, shift=DOWN * 0.15), run_time=0.9)
            self.at("parallel universe", lead=0.3)
            self.play(FadeIn(R.head, shift=DOWN * 0.15), R.rect.animate.set_fill(PARA, 0.13), run_time=0.7)
            self.play(R.rect.animate.set_fill(PARA, 0.07), run_time=0.5)
            self.at("Riemann hypothesis is true", lead=0.1)
            rhL = M(r"\text{RH}", size=72, color=INK).move_to(L.rect.get_center() + LEFT * 0.6 + DOWN * 0.2)
            qL = M("?", size=90, color=MUTED).next_to(rhL, RIGHT, buff=0.4)
            rhR = M(r"\text{RH}", size=72, color=INK).move_to(R.rect.get_center() + LEFT * 0.6 + DOWN * 0.2)
            ck = check(s=1.3).next_to(rhR, RIGHT, buff=0.4)
            self.play(FadeIn(rhL), FadeIn(rhR), FadeIn(qL), run_time=0.6)
            self.play(Create(ck), run_time=0.5)

        # ============================================================== b: clock arithmetic, then points on a curve
        p = 13
        with self.beat("b") as d:
            F = full_frame()
            self.play(FadeOut(VGroup(L, rhL, qL), shift=LEFT * 1.5), FadeOut(VGroup(rhR, ck, R.lab)),
                      Transform(R.rect, F.rect), ReplacementTransform(R.icon, F.icon), run_time=0.9)
            frame_rect, corner = R.rect, F.icon

            # the whole numbers in a row...
            cy = -0.3
            nums = VGroup(*[M(str(k), size=40) for k in range(p)])
            xs = np.linspace(-5.4, 5.4, p)
            row_line = Line([-5.9, cy - 0.55, 0], [5.9, cy - 0.55, 0]).set_stroke(MUTED, 3)
            row_ticks = VGroup(*[Line(UP * 0.12, DOWN * 0.12).move_to([x, cy - 0.55, 0]) for x in xs]).set_stroke(MUTED, 3)
            for n, x in zip(nums, xs): n.move_to([x, cy, 0])
            self.play(Create(row_line), FadeIn(row_ticks), LaggedStart(*[FadeIn(n, shift=UP * 0.2) for n in nums], lag_ratio=0.06),
                      run_time=1.0)

            # ...curl up into a clock
            self.at("clock arithmetic", lead=0.5)
            C, Rr = np.array([-1.7, cy, 0]), 2.2
            ang = lambda k: PI / 2 - TAU * k / p
            dirv = lambda a: np.array([np.cos(a), np.sin(a), 0])
            circ = Circle(radius=Rr).move_to(C).set_stroke(MUTED, 3)
            cticks = VGroup(*[Line(C + dirv(ang(k)) * (Rr - 0.13), C + dirv(ang(k)) * (Rr + 0.13)) for k in range(p)]).set_stroke(MUTED, 3)
            self.play(Transform(row_line, circ), Transform(row_ticks, cticks),
                      *[n.animate.move_to(C + dirv(ang(k)) * (Rr + 0.48)) for k, n in enumerate(nums)], run_time=1.3)
            hub = Dot(C, radius=0.08, color=INK)

            # 9 + 6 = 2 : the hand walks forward and wraps past 0
            self.at("wrap around", lead=0.6)
            h = ValueTracker(9)
            hand = always_redraw(lambda: Line(C, C + dirv(ang(h.get_value())) * (Rr * 0.72)).set_stroke(INK, 6))
            arc = always_redraw(lambda: Arc(radius=Rr * 0.86, start_angle=ang(9), angle=-(h.get_value() - 9) * TAU / p + 1e-4,
                                            arc_center=C).set_stroke(PARA, 7))
            eq = M("9", "+", "6", "=", "2", size=72).move_to([3.7, cy + 0.6, 0])
            eq[4].set_color(PARA)
            self.play(FadeIn(hand), FadeIn(hub), nums[9].animate.set_color(PARA), FadeIn(eq[0:3]), run_time=0.5)
            self.add(arc)
            self.play(h.animate.set_value(15), nums[9].animate.set_color(INK), run_time=1.6, rate_func=smooth)
            self.play(nums[2].animate.set_color(PARA).scale(1.25), FadeIn(eq[3:]), run_time=0.5)

            self.at("prime number of hours", lead=0.2)
            hrs = T("13 hours", 40, t2c={"13": PRIME}).next_to(eq, DOWN, buff=0.6)
            self.play(FadeIn(hrs, shift=UP * 0.2), run_time=0.6)
            self.play(Indicate(hrs[0:2], color=PRIME, scale_factor=1.3), run_time=0.8)

            # points on a curve: a 13 x 13 grid of clock pairs
            self.at("count solutions", lead=0.4)
            clock = VGroup(row_line, row_ticks, nums, hand, arc, hub)
            arc.clear_updaters(); hand.clear_updaters()
            nums[2].scale(1 / 1.25)
            gs, gc = 0.4, np.array([1.3, -0.75, 0])
            g2p = lambda x, y: gc + np.array([(x - (p - 1) / 2) * gs, (y - (p - 1) / 2) * gs, 0])
            grid = VGroup(*[Dot(g2p(x, y), radius=0.04, color=DIM) for x in range(p) for y in range(p)])
            xl = VGroup(*[M(str(k), size=24, color=MUTED).next_to(g2p(k, 0), DOWN, buff=0.28) for k in range(p)])
            yl = VGroup(*[M(str(k), size=24, color=MUTED).next_to(g2p(0, k), LEFT, buff=0.28) for k in range(p)])
            xn = M("x", size=34, color=MUTED).next_to(xl, RIGHT, buff=0.3)
            yn = M("y", size=34, color=MUTED).next_to(yl, UP, buff=0.2)
            curve_eq = M("y^2", "=", "x^3 + x + 1", size=50).move_to([gc[0], 2.75, 0])
            self.play(FadeOut(VGroup(eq, hrs)), nums[2].animate.set_color(INK),
                      clock.animate.scale(0.5).move_to([-4.6, 0.3, 0]), run_time=0.8)
            self.play(FadeIn(grid, lag_ratio=0.004), FadeIn(xl), FadeIn(yl), FadeIn(xn), FadeIn(yn), Write(curve_eq), run_time=0.9)

            sols = [(x, y) for x in range(p) for y in range(p) if (y * y - (x ** 3 + x + 1)) % p == 0]
            sol_dots = VGroup(*[VGroup(Dot(g2p(x, y), radius=0.16, color=PARA).set_opacity(0.25), Dot(g2p(x, y), radius=0.085, color=PARA))
                                for x, y in sols])
            inf_pt = VGroup(Dot(radius=0.16, color=PARA).set_opacity(0.25), Dot(radius=0.085, color=PARA)).move_to(g2p(p - 1, p - 1) + UP * 0.75 + RIGHT * 1.0)
            inf_l = M(r"\infty", size=34, color=PARA).next_to(inf_pt, RIGHT, buff=0.12)
            n_total = len(sols) + 1
            assert n_total == curve_count(p)
            cnt = ValueTracker(0)
            counter = always_redraw(lambda: Integer(int(round(cnt.get_value())), font_size=80, color=PARA).move_to([5.45, -0.1, 0]))
            cnt_l = T("points", 30, PARA).move_to([5.45, -0.95, 0])
            self.add(counter)
            self.play(FadeIn(cnt_l), run_time=0.3)
            lit = max(0.6, min(2.2, self.left() - 0.9))
            self.play(LaggedStart(*[FadeIn(sd, scale=2.5) for sd in sol_dots], lag_ratio=0.12),
                      cnt.animate.set_value(len(sols)), run_time=lit, rate_func=linear)
            self.play(FadeIn(inf_pt, scale=2.5), FadeIn(inf_l), cnt.animate.set_value(n_total), run_time=0.4)
            counter.clear_updaters()

        # ============================================================== c: their zeta zeros, Weil, and the real counts
        with self.beat("c") as d:
            self.play(FadeOut(VGroup(clock, grid, xl, yl, xn, yn, curve_eq, sol_dots, inf_pt, inf_l, cnt_l)),
                      counter.animate.scale(0.55).move_to([4.9, 2.9, 0]).set_opacity(0), run_time=0.6)
            self.remove(counter)
            # the curve's own zeta function: zeros repeat periodically in height, all on the line (computed: a_p = p+1-#)
            strip = critical_strip(height=4.4, width=1.6, tmax=10.0, n_zeros=0, labels=True).move_to([-4.35, -0.55, 0])
            ap = p + 1 - n_total
            th = np.arccos(ap / (2 * np.sqrt(p)))
            per, off = TAU / np.log(p), th / np.log(p)
            ts = sorted([t for k in range(6) for t in (off + per * k, -off + per * (k + 1)) if 0.2 < t < 9.8])
            zdots = VGroup(*[Dot(strip.p2c(0.5, t), radius=0.08, color=ZERO).set_z_index(3) for t in ts])
            zl = M(r"\zeta_{\text{curve}}(s)", size=40, color=PARA).next_to(strip.strip, UP, buff=0.3)
            self.play(FadeIn(VGroup(strip.strip, strip.edges, strip.axis, strip.labels)), Write(zl), run_time=0.9)
            self.at("own zeros", lead=0.2)
            self.play(LaggedStart(*[FadeIn(z, shift=DOWN * 0.6) for z in zdots], lag_ratio=0.12), run_time=1.1)
            self.at("critical line", lead=0.2)
            self.play(Create(strip.line), run_time=0.7)

            self.at("Weil", lead=0.3)
            weil = T("Weil, 1940s", 32).next_to(strip.strip, UP, buff=0.3)
            wck = check(s=0.8).next_to(weil, RIGHT, buff=0.2)
            wg = VGroup(weil, wck).move_to([strip.strip.get_x(), weil.get_y(), 0])
            self.play(zl.animate.next_to(wg, UP, buff=0.25), FadeIn(weil), run_time=0.6)
            self.at("every one of those zeros", lead=0.2)
            self.play(LaggedStart(*[Indicate(z, color=ZERO, scale_factor=1.8) for z in zdots], lag_ratio=0.08),
                      Create(wck), strip.line.animate.set_stroke(width=5), run_time=1.2)

            # the real point counts for every prime up to 250
            ax = Axes(x_range=[0, 250, 50], y_range=[0, 300, 100], x_length=7.4, y_length=4.9, tips=False,
                      axis_config=dict(color=MUTED, stroke_width=2, font_size=24),
                      x_axis_config=dict(numbers_to_include=[50, 100, 150, 200, 250]),
                      y_axis_config=dict(numbers_to_include=[100, 200, 300])).move_to([2.55, -0.55, 0])
            for nm in ax.get_x_axis().numbers: nm.set_color(MUTED)
            for nm in ax.get_y_axis().numbers: nm.set_color(MUTED)
            xlab = M("p", size=38, color=PRIME).next_to(ax.x_axis.get_end(), UP, buff=0.2)
            ylab = T("points", 26, PARA).next_to(ax.y_axis.get_end(), RIGHT, buff=0.2)
            P = np.linspace(0, 250, 120)
            band = Polygon(*[ax.c2p(x, x + 1 + 2 * np.sqrt(x)) for x in P], *[ax.c2p(x, max(0, x + 1 - 2 * np.sqrt(x))) for x in P[::-1]],
                           stroke_width=0, fill_color=GOOD, fill_opacity=0.16)
            mid = ax.plot(lambda x: x + 1, x_range=[0, 250], color=INK, stroke_width=2.5)
            mid_l = M("p+1", size=32).next_to(ax.c2p(250, 251), UP, buff=0.12).shift(LEFT * 0.35)
            ps = [q for q in primes_upto(250) if q not in (2, 31)]   # 2 and 31: the curve degenerates there
            pdots = VGroup(*[Dot(ax.c2p(q, curve_count(q)), radius=0.05, color=PARA) for q in ps])
            self.at("every one of those zeros", lead=-1.4)
            self.play(Create(ax), FadeIn(xlab), FadeIn(ylab), run_time=0.8)
            self.play(Create(mid), FadeIn(mid_l), FadeIn(band), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(pd, scale=2) for pd in pdots], lag_ratio=0.05), run_time=2.0)
            self.at("within a square root", lead=0.6)
            cap = M(r"\big|\,\#\text{points} - (p+1)\,\big| \;\le\; 2\sqrt{p}", size=40).move_to([2.55, 2.85, 0])
            self.play(Write(cap), Flash(pdots[ps.index(13)], color=PARA, line_length=0.15), run_time=1.0)

        # ============================================================== d: back to the split; one side proved, one side not
        with self.beat("d") as d:
            L2, R2 = universe_panel(-1), universe_panel(+1)
            plot = VGroup(ax, band, mid, mid_l, pdots, xlab, ylab)
            plot_t = plot.copy().scale_to_fit_width(5.0).move_to(R2.rect.get_center() + DOWN * 0.45)
            self.play(Transform(frame_rect, R2.rect), ReplacementTransform(corner, R2.icon), FadeIn(R2.lab),
                      FadeOut(VGroup(strip.strip, strip.edges, strip.axis, strip.labels, strip.line, zdots, zl, weil, wck)),
                      FadeOut(cap), Transform(plot, plot_t), run_time=1.0)
            q = M("?", size=150, color=MUTED).move_to(L2.rect.get_center() + DOWN * 0.3)
            bigck = check(s=1.1).move_to(plot_t[0].c2p(75, 250))
            self.play(Create(L2.rect), FadeIn(L2.head), FadeIn(q, scale=0.7), Create(bigck), run_time=0.9)
            self.at("how to carry", lead=0.4)
            full = ArcBetweenPoints(RIGHT * 1.7 + UP * 1.1, LEFT * 1.7 + UP * 1.1, angle=PI / 2.2)
            part = VMobject().pointwise_become_partial(full, 0, 0.62)
            bridge = DashedVMobject(part, num_dashes=12, dashed_ratio=0.55).set_stroke(INK, 4)
            self.play(Create(bridge), run_time=min(2.0, self.left() - 1.2), rate_func=linear)
            stub = Dot(part.get_end(), radius=0.07, color=INK)
            self.play(FadeIn(stub), Wiggle(q, scale_value=1.12), run_time=0.8)
            self.wait(max(0, self.left() - 0.5))
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
        self.finish()
