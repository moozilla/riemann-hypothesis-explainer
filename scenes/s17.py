import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *

X = 100.0          # plotted with X = 100, so sqrt(X) = 10
TOTAL_C = INK


class S17(NarratedScene):
    sid = "s17"
    last_hold = 1.4   # let the quote breathe before the cut

    def construct(self):
        ax = Axes(x_range=[0, 30, 10], y_range=[0, 40, 10], x_length=10.4, y_length=5.6, tips=True,
                  axis_config=dict(stroke_color=MUTED, stroke_width=3, include_ticks=False, tip_length=0.2, tip_width=0.2))
        ax.move_to(DOWN * 0.35 + LEFT * 0.4)
        xl = T("number of lifts  m", size=32, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.3).align_to(ax.x_axis, RIGHT)
        yl = T("error", size=32, color=MUTED).next_to(ax.y_axis, UP, buff=0.15).align_to(ax.y_axis, LEFT).shift(LEFT * 0.2)

        # ------------------------------------------------------------ a: X/m falls
        with self.beat("a") as d:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=1.0)
            px = M(r"\text{primes up to } X", size=40).to_corner(UR, buff=0.5)
            self.at("primes up to X")
            self.play(FadeIn(px, shift=LEFT * 0.2), run_time=0.7)
            self.at("With m lifts")
            fall = ax.plot(lambda m: X / m, x_range=[X / 40, 30], color=LIFT, stroke_width=5)
            fl = M(r"\frac{X}{m}", size=54, color=LIFT).move_to(ax.c2p(5.2, 30))
            self.play(Create(fall), run_time=min(2.4, self.left() * 0.6), rate_func=linear)
            self.play(FadeIn(fl, shift=LEFT * 0.2), run_time=0.6)

        # ------------------------------------------------------------ b: m rises
        with self.beat("b") as d:
            rise = ax.plot(lambda m: m, x_range=[0, 30], color=WARM, stroke_width=5)
            self.at("every lift also has a cost")
            self.play(Create(rise), run_time=min(2.5, d * 0.35), rate_func=linear)
            rl = M("m", size=54, color=WARM).next_to(ax.c2p(30, 30), RIGHT, buff=0.15)
            rt = T("cost of lifting", size=30, color=WARM).next_to(rl, DOWN, buff=0.12).align_to(rl, RIGHT).shift(RIGHT * 0.1)
            rt.move_to(ax.c2p(25.5, 22.5)).rotate(np.arctan2(ax.y_axis.unit_size, ax.x_axis.unit_size))
            self.play(FadeIn(rl), Write(rt), run_time=1.0)
            self.at("in proportion")
            dot = Dot(ax.c2p(4, 4), radius=0.09, color=WARM)
            self.play(MoveAlongPath(dot, ax.plot(lambda m: m, x_range=[4, 28])), run_time=max(0.4, self.left() - 0.35))
            self.play(FadeOut(dot), run_time=0.15)

        # ------------------------------------------------------------ c: the sum and its minimum
        with self.beat("c") as d:
            tot = ax.plot(lambda m: X / m + m, x_range=[X / 37.0, 30], color=TOTAL_C, stroke_width=6)
            tl = M(r"\frac{X}{m} + m", size=44, color=TOTAL_C).move_to(ax.c2p(19, 36))
            self.play(Create(tot), FadeIn(tl), run_time=1.6)
            t = ValueTracker(3.0)
            sl = always_redraw(lambda: Dot(ax.c2p(t.get_value(), X / t.get_value() + t.get_value()), radius=0.12, color=PRIME).set_z_index(5))
            self.play(FadeIn(sl), run_time=0.3)
            self.at("smallest")
            self.play(t.animate.set_value(10.0), run_time=min(2.4, self.cue("that happens") - self.cue("smallest") + 0.3), rate_func=smooth)
            self.at("that happens")
            cross = ax.c2p(10, 10)
            v1 = DashedLine(ax.c2p(10, 20), ax.c2p(10, 0), dash_length=0.1).set_stroke(INK, 2)
            h1 = DashedLine(cross, ax.c2p(0, 10), dash_length=0.1).set_stroke(INK, 2)
            cdot = Dot(cross, radius=0.1, color=INK)
            sx = M(r"\sqrt{X}", size=40).next_to(ax.c2p(10, 0), DOWN, buff=0.18)
            sy = M(r"\sqrt{X}", size=40).next_to(ax.c2p(0, 10), LEFT, buff=0.15)
            self.play(Create(v1), FadeIn(cdot), run_time=0.7)
            self.play(Write(sx), run_time=0.6)
            eq = M(r"\frac{X}{m} = m", r"\;\Rightarrow\;", r"m = \sqrt{X}", size=50)
            eq.scale(0.9).move_to(ax.c2p(23.5, 11.0))
            eq[2].set_color(PRIME)
            self.play(Write(eq), run_time=1.2)
            self.at("both errors")
            self.play(Create(h1), Write(sy), Indicate(cdot, color=PRIME), run_time=1.0)
            self.at("Exactly the ceiling")
            self.play(Indicate(sy, color=GOOD, scale_factor=1.3), Indicate(eq[2], color=PRIME), run_time=min(1.2, max(0.3, self.left() - 0.1)))

        # ------------------------------------------------------------ d: a million stories; the quote
        with self.beat("d") as d:
            plot = VGroup(ax, xl, yl, fall, fl, rise, rl, rt, tot, tl, v1, h1, cdot, sx, sy, sl)
            self.at("singles out")
            self.play(Flash(sl, color=PRIME, line_length=0.3, num_lines=12), run_time=0.8)
            self.play(Circumscribe(eq[2], color=PRIME, buff=0.12), run_time=1.4)
            self.at("He had expected")
            sl.clear_updaters()
            self.play(FadeOut(plot), FadeOut(px), eq.animate.scale(1.1).move_to(LEFT * 2.6 + UP * 0.6), run_time=1.2)

            # the tower: platforms rising out of the top of the frame
            tx = 4.7
            FL = 40
            tw = lift_tower(floors=FL, width=2.4, gap=0.5, grow=0.012, labels=False)
            tw.shift(RIGHT * tx + UP * (-2.55 - tw.floors[0].get_y()))
            u0 = M("U_0", size=30, color=LIFT).next_to(tw.floors[0], LEFT, buff=0.2)
            self.at("chain of theta lifts")
            vis = [i for i in range(FL) if tw.floors[i].get_y() < 4.2]
            self.play(LaggedStart(*[AnimationGroup(FadeIn(tw.floors[i], shift=UP * 0.2), *( [GrowArrow(tw.arrows[i - 1])] if i else [])) for i in vis],
                                  lag_ratio=0.25), FadeIn(u0), run_time=1.6)
            self.add(*[tw.floors[i] for i in range(FL)], *tw.arrows)
            # endless climb: slide the tower down continuously
            climb = VGroup(tw, u0)
            lab = M(r"X = 10^{12}", r"\;\longrightarrow\;", r"m \approx 10^{6}", r"\text{ lifts}", size=46)
            lab[0].set_color(INK); lab[2:].set_color(LIFT)
            lab.move_to(LEFT * 2.6 + DOWN * 1.0)
            self.add(climb)
            climb.add_updater(lambda m, dt: m.shift(DOWN * 0.9 * dt))
            self.at("a trillion")
            self.play(FadeIn(lab[0], shift=UP * 0.2), run_time=0.6)
            self.at("a million stories")
            self.play(FadeIn(lab[1:], shift=LEFT * 0.2), run_time=0.8)
            self.at("As he put it")
            # quote card
            q = T("“(And yet, what else could it be?)”", size=36, slant=ITALIC)
            who = T("— Levent Alpöge", size=30, color=MUTED)
            card_txt = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.3)
            card = VGroup(SurroundingRectangle(card_txt, buff=0.4, corner_radius=0.15, stroke_color=DIM, stroke_width=2,
                                               fill_color=BG, fill_opacity=0.92), card_txt)
            card.move_to(LEFT * 2.6 + UP * 0.6)
            if card.get_left()[0] < -6.5:
                card.shift(RIGHT * (-6.5 - card.get_left()[0]))
            lab_target = lab.copy().scale(0.85).next_to(card, DOWN, buff=0.5).match_x(card)
            self.play(FadeOut(eq, shift=UP * 0.3), run_time=0.35)
            self.play(FadeIn(card, shift=UP * 0.2), Transform(lab, lab_target), run_time=min(0.9, max(0.3, self.left() - 0.05)))
        self.finish()
