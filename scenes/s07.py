import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *
# the spiral layout is shared with s06 so the cut s06 -> s07 is seamless
from scenes.s06 import (SC, NT, S_ZERO, make_panel, make_out_axes, build_spiral, end_dot, s_readout,
                        endpoint_trace, s_path, out_pt, origin, limit, terms, tint_s)

SH, TMAX0 = 6.4, 52.0          # critical strip height on screen, and the height (t) it shows at first


class S07(NarratedScene):
    sid = "s07"

    def construct(self):
        # ------------------------------------------------------------------ a: the spiral lands on 0
        with self.beat("a") as d:
            panel = make_panel(); pax = panel.ax
            tau = ValueTracker(1.0)
            S = lambda: s_path(tau.get_value())
            pdot = always_redraw(lambda: Dot(pax.c2p(S().real, S().imag), radius=0.11, color=SC).set_z_index(4))
            pv = always_redraw(lambda: DashedLine(pax.c2p(S().real, S().imag), pax.c2p(S().real, 0), dash_length=0.08, stroke_width=2.5, color=SC))
            ph = always_redraw(lambda: DashedLine(pax.c2p(S().real, S().imag), pax.c2p(0, S().imag), dash_length=0.08, stroke_width=2.5, color=INK))
            rd = s_readout(S)
            oax = make_out_axes()
            trace = always_redraw(lambda: endpoint_trace(tau.get_value()))
            spiral = always_redraw(lambda: build_spiral(S(), 1.0, NT, True))
            ed = always_redraw(lambda: end_dot(S(), 1.0))
            self.add(panel, pv, ph, pdot, rd, oax, trace, spiral, ed)
            # straight away: the last stretch up the line
            self.play(tau.animate.set_value(2.0), run_time=min(2.6, self.cue("lands") + 0.2), rate_func=rate_functions.ease_out_cubic)
            for m in (spiral, ed, trace, pdot, pv, ph, rd):
                m.clear_updaters()
            O = origin()
            ed2 = VGroup(Dot(O, radius=0.16, color=ZERO, fill_opacity=0.3), Dot(O, radius=0.08, color=ZERO)).set_z_index(6)
            self.play(ReplacementTransform(ed, ed2), Flash(O, color=ZERO, flash_radius=0.35, line_length=0.25, num_lines=14), run_time=0.7)
            pulse = Circle(radius=0.16, color=ZERO, stroke_width=4).move_to(O)
            self.play(pulse.animate.scale(4.5).set_stroke(opacity=0), run_time=0.9)
            # every arrow cancelled by the others: a glint runs down the whole chain
            self.at("Every arrow", lead=0.1)
            P = np.concatenate([[0], np.cumsum(terms(S_ZERO, 1.0))])
            path = VMobject().set_points_as_corners([out_pt(z) for z in P[:40]]).set_stroke(ZERO, 6)
            self.play(ShowPassingFlash(path, time_width=0.35), run_time=1.6, rate_func=linear)
            zlab = M(r"\zeta(s) = 0", size=48, color=ZERO).move_to(O + np.array([1.9, 1.9, 0]))
            lead = Line(O + np.array([0.15, 0.15, 0]), zlab.get_corner(DL) + np.array([-0.05, -0.05, 0]), stroke_width=2, color=ZERO)
            self.play(Write(zlab), Create(lead), run_time=0.8)
            # the input itself is "a zero"
            self.at("called a zero", lead=0.4)
            pz = pax.c2p(S_ZERO.real, S_ZERO.imag)
            pdot2 = Dot(pz, radius=0.11, color=ZERO).set_z_index(5)
            rd2 = s_readout(lambda: S_ZERO, color=ZERO); rd2.clear_updaters()
            zname = T("a zero", size=32, color=ZERO).next_to(pz, RIGHT, buff=0.25)
            self.play(ReplacementTransform(pdot, pdot2), ReplacementTransform(rd, rd2), FadeIn(zname, shift=LEFT * 0.15),
                      Flash(pz, color=ZERO, flash_radius=0.3), run_time=0.9)

        # ------------------------------------------------------------------ b: where are they? the strip
        with self.beat("b") as d:
            cs = critical_strip(height=SH, width=1.0, tmax=TMAX0, n_zeros=10)
            cs.shift(np.array([0.5, 0.2, 0]) - cs.strip.get_center())
            bottom = cs.strip.get_bottom()[1]
            x0 = cs.strip.get_left()[0]
            axis_long = Line([-6.5, bottom, 0], [3.2, bottom, 0], stroke_width=2, color=MUTED)
            z1 = Dot(cs.p2c(0.5, S_ZERO.imag), radius=0.07, color=ZERO).set_z_index(5)
            self.play(FadeOut(VGroup(oax, trace, spiral, ed2, zlab, lead, rd2, pv, ph, zname)),
                      FadeOut(panel, scale=0.9),
                      FadeIn(VGroup(cs.strip, cs.edges)), Create(axis_long),
                      ReplacementTransform(pdot2, z1), run_time=1.3)
            # the boring ones
            self.at("boring", lead=0.3)
            triv = VGroup(*[Dot([x0 - 1.0 * k, bottom, 0], radius=0.08, color=MUTED) for k in (2, 4, 6)])
            trl = VGroup(*[M(f"-{k}", size=28, color=MUTED).next_to(dt, DOWN, buff=0.15) for k, dt in zip((2, 4, 6), triv)])
            boring = T("boring", size=30, color=MUTED).next_to(triv, UP, buff=0.35)
            self.play(LaggedStart(*[FadeIn(t, scale=0.3) for t in triv], lag_ratio=0.25), FadeIn(trl), run_time=0.9)
            self.play(FadeIn(boring, shift=DOWN * 0.15), run_time=0.5)
            self.at("interesting ones", lead=0.2)
            self.play(Indicate(z1, color=ZERO, scale_factor=2.0), cs.strip.animate.set_fill(opacity=0.18), run_time=0.9)
            self.at("between zero and one", lead=0.2)
            l0, l1 = cs.labels[0], cs.labels[2]
            self.play(FadeIn(l0, shift=UP * 0.1), FadeIn(l1, shift=UP * 0.1), run_time=0.6)
            self.at("The critical strip", lead=0.2)
            cname = T("critical strip", size=36, color=INK).next_to(cs.strip, RIGHT, buff=0.4).shift(UP * 1.2)
            arr = Arrow(cname.get_left() + LEFT * 0.05, cs.strip.get_right() + UP * 0.9 + LEFT * 0.2, buff=0.1, stroke_width=3, color=INK, tip_length=0.18)
            self.play(Write(cname), GrowArrow(arr), cs.strip.animate.set_fill(opacity=0.10), run_time=1.0)

        # ------------------------------------------------------------------ c: the first zeros, on the line
        with self.beat("c") as d:
            cs2 = critical_strip(height=SH, width=2.4, tmax=TMAX0, n_zeros=10)
            cs2.shift(np.array([0.0, 0.2, 0]) - cs2.strip.get_center())
            zs = cs2.zeros
            self.play(FadeOut(VGroup(triv, trl, boring, cname, arr)),
                      ReplacementTransform(cs.strip, cs2.strip), ReplacementTransform(cs.edges, cs2.edges),
                      ReplacementTransform(axis_long, cs2.axis),
                      ReplacementTransform(l0, cs2.labels[0]), ReplacementTransform(l1, cs2.labels[2]),
                      ReplacementTransform(z1, zs[0]), run_time=1.0)
            hts = zeta_zeros(10)
            hl = VGroup(*[M(f"{h:.2f}" + r"\ldots", size=28, color=MUTED).next_to(cs2.p2c(1.0, h), RIGHT, buff=0.3) for h in hts[:3]])
            self.add(hl[0])
            self.play(FadeIn(hl[0]), run_time=0.3)
            # pop, pop, pop
            pops = []
            for i in range(1, len(zs)):
                anim = [FadeIn(zs[i], scale=3.0)]
                if i < 3:
                    anim.append(FadeIn(hl[i], shift=LEFT * 0.1))
                pops.append(AnimationGroup(*anim))
            self.play(LaggedStart(*pops, lag_ratio=0.45), run_time=2.8)
            self.at("lined up", lead=0.2)
            self.play(Create(cs2.line), run_time=1.2)
            self.at("exactly one half", lead=0.3)
            half = cs2.labels[1]
            self.play(FadeIn(half, shift=UP * 0.15), Indicate(cs2.line, color=ZERO, scale_factor=1.0), run_time=0.9)
            self.play(LaggedStart(*[Indicate(z, color=ZERO, scale_factor=1.8) for z in zs], lag_ratio=0.1), run_time=max(0.3, min(1.6, self.left() - 0.1)))

        # ------------------------------------------------------------------ d: zoom out: hundreds of zeros, all on the line
        with self.beat("d") as d:
            NZ = 700
            allz = np.array(zeta_zeros(NZ))
            g = VGroup(cs2.strip, cs2.edges, cs2.axis, cs2.line, cs2.labels)
            shift = np.array([-3.7, 0, 0])
            self.play(g.animate.shift(shift), zs.animate.shift(shift), FadeOut(hl), run_time=0.8)
            tm = ValueTracker(TMAX0)
            bottom = cs2.strip.get_bottom()[1]
            xl = cs2.line.get_center()[0]

            def dots():
                T_ = tm.get_value()
                r = float(np.clip(0.07 * (TMAX0 / T_) ** 0.45, 0.022, 0.07))
                vis = allz[allz < T_]
                return VGroup(*[Dot([xl, bottom + SH * t / T_, 0], radius=r, color=ZERO) for t in vis]).set_z_index(4)

            def ticks():
                T_ = tm.get_value()
                step = next(s_ for s_ in (10, 20, 50, 100, 200, 250, 500) if T_ / s_ <= 5.5)
                g_ = VGroup()
                xe = cs2.strip.get_left()[0]
                for v in np.arange(step, T_ + 1e-6, step):
                    y = bottom + SH * v / T_
                    if y > bottom + SH - 0.1:
                        continue
                    g_.add(Line([xe - 0.12, y, 0], [xe, y, 0], stroke_width=2, color=MUTED),
                           Text(f"{int(v)}", font=FONT, font_size=22, color=MUTED).next_to([xe - 0.12, y, 0], LEFT, buff=0.08))
                return g_
            zd = always_redraw(dots)
            tk = always_redraw(ticks)
            self.remove(zs)
            self.add(zd)
            self.play(FadeIn(tk), run_time=0.3)

            title = T("The Riemann Hypothesis", size=50, weight=BOLD)
            st1 = T("every zero in the strip", size=36)
            st2 = VGroup(T("lies on the line", size=36), M(r"\mathrm{Re}(s) = \tfrac12", size=44, color=ZERO)).arrange(RIGHT, buff=0.25)
            st = VGroup(st1, st2).arrange(DOWN, buff=0.22)
            block = VGroup(title, st).arrange(DOWN, buff=0.5).move_to([2.6, 1.3, 0])
            cnt_v = ValueTracker(0.0)
            cnt = always_redraw(lambda: VGroup(
                Integer(int(round(10 ** cnt_v.get_value())) if cnt_v.get_value() > 0 else 0, group_with_commas=True, font_size=52, color=GOOD),
                M("+", size=52, color=GOOD).set_opacity(1.0 if cnt_v.get_value() > 12.99 else 0.0)).arrange(RIGHT, buff=0.1)
                .move_to([2.6, -1.35, 0]))
            cnt_l = T("zeros checked: all on the line", size=28, color=MUTED).move_to([2.6, -2.15, 0]).set_opacity(0)

            # zoom out vertically the whole time; the words arrive on cue
            T_total = self.left() - 0.2
            zoom_anim = ApplyMethod(tm.set_value, 1000.0, run_time=T_total, rate_func=rate_functions.ease_in_quad)

            # we interleave: start zoom, then cue texts with self.wait timing via a Succession of waits
            el = self.now() - self._beat_start
            c = lambda ph: self.cue(ph) - 0.2 - el
            t_st = max(0.05, c("all of them"))
            t_title = max(t_st + 1.0, c("That's the Riemann"))
            t_cnt = max(t_title + 1.0, c("Computers have"))
            t_q = max(t_cnt + 2.2, c("But trillions"))
            cnt.suspend_updating()
            seq = Succession(
                Wait(t_st),
                FadeIn(st, shift=UP * 0.2, run_time=1.0),
                Wait(max(0.01, t_title - t_st - 1.0)),
                FadeIn(title, shift=DOWN * 0.2, run_time=0.9),
                Wait(max(0.01, t_cnt - t_title - 0.9)),
                AnimationGroup(FadeIn(cnt), cnt_l.animate.set_opacity(1), run_time=0.3),
                cnt_v.animate(rate_func=rate_functions.ease_out_cubic, run_time=2.0).set_value(13.0),
                Wait(max(0.01, t_q - t_cnt - 2.3)),
                Indicate(cnt_l, color=INK, scale_factor=1.08, run_time=1.0),
            )
            cnt.resume_updating()
            self.play(AnimationGroup(zoom_anim, seq))
        self.finish()
