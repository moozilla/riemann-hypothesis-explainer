import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *
from scenes.s14 import placed_scale, rig_scale, token_spot   # same scale + token placement as s14e


class S16(NarratedScene):
    sid = "s16"

    def construct(self):
        # ------------------------------------------------------------ a: one lift ≈ one order of multiplicity
        with self.beat("a") as d:
            ax = Axes(x_range=[-1.5, 1.5, 1], y_range=[-1.3, 1.7, 1], x_length=4.6, y_length=3.6, tips=False,
                      axis_config=dict(stroke_color=MUTED, stroke_width=2, include_ticks=False)).move_to(LEFT * 3.7 + DOWN * 0.15)
            s = ValueTracker(0.0)
            f = lambda x: ((1 - s.get_value()) * 0.9 * x + s.get_value() * 1.1 * x * x) * (1 + 0.3 * x)
            curve = always_redraw(lambda: ax.plot(f, x_range=[-1.3, 1.15], color=INK, stroke_width=4))
            root = Dot(ax.c2p(0, 0), radius=0.09, color=PRIME).set_z_index(3)
            mlab = VGroup(M("m", "=", size=48), M("1", size=48, color=PRIME))
            mlab[1].next_to(mlab[0], RIGHT, buff=0.15)
            mlab.next_to(ax, UP, buff=0.05).shift(RIGHT * 0.9)
            ltxt = T("one order of multiplicity", size=30, color=PRIME).next_to(ax, DOWN, buff=0.35)

            t2 = lift_tower(floors=2, width=2.2, gap=2.3, grow=0.25)
            t2.move_to(RIGHT * 3.7 + DOWN * 0.3)
            th = M(r"\theta", size=50, color=LIFT).next_to(t2.arrows[0], RIGHT, buff=0.2)
            rtxt = T("one lift", size=30, color=LIFT).match_y(ltxt).match_x(t2.floors)
            approx = M(r"\approx", size=110).move_to(DOWN * 0.15)

            self.play(Create(ax), Create(curve), FadeIn(root), FadeIn(mlab), FadeIn(t2.floors[0]), FadeIn(t2.labels[0]), run_time=1.0)
            self.play(GrowArrow(t2.arrows[0]), FadeIn(th), FadeIn(t2.floors[1], shift=UP * 0.3), FadeIn(t2.labels[1]), run_time=1.0)
            self.at("gains one extra")
            pulse = Dot(t2.arrows[0].get_start(), radius=0.1, color=LIFT).set_z_index(4)
            two = M("2", size=48, color=PRIME).move_to(mlab[1])
            gt = min(2.2, self.cue("One lift") - self.cue("gains one extra") - 0.2)
            self.play(MoveAlongPath(pulse, Line(t2.arrows[0].get_start(), t2.arrows[0].get_end())), s.animate.set_value(1.0),
                      Transform(mlab[1], two), run_time=gt)
            self.play(FadeOut(pulse, scale=2), Flash(root, color=PRIME, line_length=0.2), run_time=0.5)
            self.at("One lift")
            self.play(Write(approx), FadeIn(ltxt, shift=UP * 0.2), FadeIn(rtxt, shift=UP * 0.2), run_time=1.0)
            rest = self.left() - 0.05
            if rest > 0.3:
                self.play(Indicate(approx, color=LIFT, scale_factor=1.15), run_time=rest)

        # ------------------------------------------------------------ b: the tower
        with self.beat("b") as d:
            FL = 10
            tw = lift_tower(floors=FL, width=2.4, gap=0.72, grow=0.1)
            tw.labels[FL - 2].become(M(r"\vdots", size=30, color=LIFT).move_to(tw.labels[FL - 2]))
            tw.labels[FL - 1].become(M(r"U_{m}", size=30, color=LIFT).move_to(tw.labels[FL - 1]))
            tw.shift(LEFT * 1.6 + UP * (-3.0 - tw.floors[0].get_y()))
            self.play(FadeOut(VGroup(ax, curve, root, mlab, ltxt, rtxt, approx, th)),
                      ReplacementTransform(t2.floors[0], tw.floors[0]), ReplacementTransform(t2.floors[1], tw.floors[1]),
                      ReplacementTransform(t2.arrows[0], tw.arrows[0]), ReplacementTransform(t2.labels[0], tw.labels[0]),
                      ReplacementTransform(t2.labels[1], tw.labels[1]), run_time=1.0)
            # you can't differentiate 17 ... but you can lift
            dd = M(r"\frac{d}{d\,?}\,17", size=64).move_to(RIGHT * 3.8 + UP * 0.4)
            self.at("can't differentiate")
            self.play(FadeIn(dd, shift=LEFT * 0.2), run_time=0.6)
            cross = Cross(dd, stroke_color=BAD, stroke_width=6)
            self.play(Create(cross), run_time=0.5)
            # counter
            ctitle = T("multiplicity", size=34, color=PRIME).move_to(RIGHT * 3.8 + UP * 1.0)
            vals = [str(i) for i in range(FL - 2)] + [r"\cdots", "m"]
            cval = M("1", size=110, color=PRIME).next_to(ctitle, DOWN, buff=0.35)
            self.at("But you can lift")
            p = Dot(tw.arrows[0].get_start(), radius=0.09, color=LIFT)
            self.play(FadeOut(VGroup(dd, cross), shift=UP * 0.2), MoveAlongPath(p, Line(tw.arrows[0].get_start(), tw.arrows[0].get_end())),
                      FadeIn(ctitle), FadeIn(cval), run_time=0.9)
            self.remove(p)
            self.at("you build a chain")
            steps = FL - 2
            per = (self.left() - 0.2) / steps
            for i in range(2, FL):
                newval = M(vals[i], size=110, color=PRIME).move_to(cval)
                over = tw.floors[i].get_y() - 1.65
                shown = VGroup(*tw.floors[:i], *tw.arrows[:i - 1], *tw.labels[:i])
                hidden = VGroup(*tw.floors[i:], *tw.arrows[i - 1:], *tw.labels[i:])
                if over > 0:
                    hidden.shift(DOWN * over)
                anims = [GrowArrow(tw.arrows[i - 1]), FadeIn(tw.floors[i], shift=UP * 0.25), FadeIn(tw.labels[i]),
                         Transform(cval, newval)]
                if over > 0:
                    anims.append(shown.animate.shift(DOWN * over))
                self.play(*anims, run_time=per * 0.8)
                self.wait(per * 0.2)

        # ------------------------------------------------------------ c: the number at the top; two gauges
        with self.beat("c") as d:
            top = tw.floors[-1]
            tpos = top.get_center() + UP * 1.15
            beams = VGroup(*[Line(top.get_center() + RIGHT * x * top.width / 2, tpos).set_stroke(LIFT, 3, opacity=0.8) for x in np.linspace(-1, 1, 7)])
            tok = number_token("?").move_to(tpos)
            self.play(FadeOut(ctitle), FadeOut(cval), LaggedStart(*[Create(b) for b in beams], lag_ratio=0.08), run_time=1.0)
            self.at("out comes")
            self.play(FadeIn(tok, scale=0.2), beams.animate.set_stroke(opacity=0), run_time=0.9)
            self.remove(beams)
            # gauges
            H, W, by = 4.2, 0.8, -2.75
            def gauge(x, col, label):
                frame = Rectangle(width=W, height=H, stroke_color=MUTED, stroke_width=3).move_to([x, by + H / 2, 0])
                lab = T(label, size=28, color=col).next_to(frame, DOWN, buff=0.18)
                return frame, lab
            gx_d, gx_s = 3.4, 5.5
            fd, ld = gauge(gx_d, PRIME, "divisibility")
            fs, ls = gauge(gx_s, WARM, "size")
            vd, vs = ValueTracker(0.04), ValueTracker(0.12)
            bar_d = always_redraw(lambda: Rectangle(width=W - 0.16, height=max(0.01, (H - 0.16) * vd.get_value()), stroke_width=0, fill_color=PRIME, fill_opacity=0.9)
                                  .move_to([gx_d, by + 0.08, 0], aligned_edge=DOWN))
            bar_s = always_redraw(lambda: Rectangle(width=W - 0.16, height=max(0.01, (H - 0.16) * vs.get_value()), stroke_width=0, fill_color=WARM, fill_opacity=0.9)
                                  .move_to([gx_s, by + 0.08, 0], aligned_edge=DOWN))
            self.play(FadeIn(VGroup(fd, ld, fs, ls)), FadeIn(bar_d), FadeIn(bar_s), run_time=0.8)
            self.at("Each lift")
            # a pulse climbs the tower; each floor adds divisibility
            per = min(0.42, (self.cue("while geometry") - self.cue("Each lift")) / FL)
            for i in range(FL):
                fl = tw.floors[i]
                self.play(fl.animate.set_fill(PRIME), vd.animate.set_value(0.04 + 0.9 * (i + 1) / FL),
                          vs.animate.set_value(0.12 + 0.05 * np.sin(i * 1.7) ** 2), run_time=per * 0.6)
                self.play(fl.animate.set_fill(LIFT), run_time=per * 0.4)
            self.play(Indicate(tok, color=PRIME, scale_factor=1.15), run_time=0.6)
            self.at("geometry")
            cy = by + 0.08 + (H - 0.16) * 0.2
            jaw = VGroup(Line(LEFT * 0.62, RIGHT * 0.62).set_stroke(MUTED, 8),
                         Line(LEFT * 0.62, LEFT * 0.62 + DOWN * 0.3).set_stroke(MUTED, 6),
                         Line(RIGHT * 0.62, RIGHT * 0.62 + DOWN * 0.3).set_stroke(MUTED, 6))
            glab = T("geometry", size=30, color=INK).next_to(jaw, UP, buff=0.15)
            clamp = VGroup(jaw, glab).move_to([gx_s, cy + 0.25, 0])
            self.play(FadeIn(clamp, shift=DOWN * 1.2), run_time=0.7)
            rest = self.left() - 0.1
            if rest > 0.4:  # size tries to climb, the clamp holds it
                self.play(vs.animate.set_value(0.2), clamp.animate.shift(UP * 0.05), rate_func=there_and_back, run_time=rest)

        # ------------------------------------------------------------ d: back on the balance scale
        with self.beat("d") as d:
            scale = placed_scale()
            tilt = rig_scale(scale)
            self.add(tilt)
            self.play(FadeOut(VGroup(tw, fd, ld, fs, ls, clamp), shift=DOWN * 0.3), FadeOut(bar_d), FadeOut(bar_s),
                      FadeIn(scale, shift=UP * 0.3), tok.animate.move_to(token_spot(scale)), run_time=1.2)
            self.at("with multiplicity")
            xm = M(r"\times\, m", size=48, color=PRIME).next_to(scale.left_pan, DOWN, buff=0.2)
            xm.add_updater(lambda mm: mm.next_to(scale.left_pan, DOWN, buff=0.2))
            self.play(FadeIn(xm, shift=UP * 0.2), tilt.animate.set_value(0.08), run_time=0.8)
            self.play(tilt.animate.set_value(0.0), run_time=0.8)
            self.at("This is Stepanov")
            banner = T("Stepanov's multiplicity, rebuilt from theta lifts", size=38, weight=MEDIUM).move_to(UP * 3.05)
            banner[-10:].set_color(LIFT)
            self.play(Write(banner), run_time=min(1.6, max(0.4, self.left() - 0.3)))
            rest = self.left() - 0.05
            if rest > 0.3:
                self.play(Indicate(tok[2], color=PRIME, scale_factor=1.2), run_time=rest)
        self.finish()
