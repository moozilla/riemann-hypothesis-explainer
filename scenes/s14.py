import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *

# The balance scale + mystery token are shared with s16 — keep these placement numbers identical there.
SCALE_K, SCALE_POS = 1.4, DOWN * 0.9


def placed_scale():
    s = balance_scale()
    s.scale(SCALE_K).move_to(SCALE_POS)
    return s


def token_spot(scale):
    return scale.pivot.get_center() + UP * 0.95


def rig_scale(scale):
    """Make the beam tilt about the pivot with the pans hanging plumb. Returns a ValueTracker (angle, CCW = right end up).
    Call with the scale level and at its final size."""
    scale.beam_group.remove(scale.left_pan, scale.right_pan)  # pans hang, beam rotates
    scale.add(scale.left_pan, scale.right_pan)
    P = scale.pivot.get_center()
    L = np.linalg.norm(scale.beam.get_end() - P)
    anchor = lambda pan: pan[0][0].get_start()   # top of the strings = hook on the beam
    offL = anchor(scale.left_pan) - scale.beam.get_start()
    offR = anchor(scale.right_pan) - scale.beam.get_end()
    a = ValueTracker(0.0)

    def ends():
        p = scale.pivot.get_center(); v = L * np.array([np.cos(a.get_value()), np.sin(a.get_value()), 0])
        return p - v, p + v
    scale.beam.add_updater(lambda m: m.put_start_and_end_on(*ends()))
    scale.left_pan.add_updater(lambda m: m.shift(ends()[0] + offL - anchor(m)))
    scale.right_pan.add_updater(lambda m: m.shift(ends()[1] + offR - anchor(m)))
    return a


class S14(NarratedScene):
    sid = "s14"

    def construct(self):
        # ------------------------------------------------------------ a: the scale
        with self.beat("a") as d:
            scale = placed_scale()
            tilt = rig_scale(scale)
            self.add(tilt)
            cap = T("Chebyshev, 1850", size=40, weight=MEDIUM).move_to(UP * 3.05)
            self.play(FadeIn(scale, shift=UP * 0.3), run_time=1.0)
            self.at("divisibility")
            self.play(tilt.animate.set_value(0.12), Circumscribe(scale.left_pan[2], color=PRIME, buff=0.12), run_time=0.9)
            self.at("its size")
            self.play(tilt.animate.set_value(-0.10), Circumscribe(scale.right_pan[2], color=WARM, buff=0.12), run_time=1.0)
            self.play(tilt.animate.set_value(0.0), run_time=0.9)
            self.at("Chebyshev")
            self.play(FadeIn(cap, shift=DOWN * 0.2), run_time=0.8)
            self.play(tilt.animate.set_value(0.05), run_time=self.left() * 0.5, rate_func=there_and_back)

        # ------------------------------------------------------------ b: C(20,10) and its factors
        with self.beat("b") as d:
            self.play(FadeOut(scale, shift=DOWN * 0.4), FadeOut(cap, shift=UP * 0.3), run_time=0.6)
            dots = VGroup(*[Dot(radius=0.13, color=DIM) for _ in range(20)]).arrange(RIGHT, buff=0.33).move_to(UP * 2.7)
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in dots], lag_ratio=0.04, run_time=0.8))
            rng = np.random.default_rng(3)
            self.at("pick ten")
            pick_t = self.cue("It equals") - self.cue("pick ten") - 0.2
            n_pick = 6
            for k in range(n_pick):
                chosen = set(rng.choice(20, 10, replace=False))
                self.play(*[x.animate.set_color(INK if i in chosen else DIM).scale_to_fit_width(0.34 if i in chosen else 0.26)
                            for i, x in enumerate(dots)], run_time=max(0.2, pick_t / n_pick))
            top = M(r"\binom{20}{10}", "=", "184{,}756", size=84).move_to(UP * 0.55)
            fac = M("=", "2^2", r"\cdot", "11", r"\cdot", "13", r"\cdot", "17", r"\cdot", "19", size=84)
            fac.next_to(top, DOWN, buff=0.55).align_to(top[1], LEFT)
            VGroup(top, fac).shift(LEFT * VGroup(top, fac).get_x())
            self.play(Write(top[0]), run_time=0.7)
            self.at("one hundred eighty")
            self.play(Write(top[1:]), run_time=1.2)
            self.at("factor it")
            self.play(TransformFromCopy(top[2], fac), run_time=1.0)
            self.at("Every prime")
            brace = Brace(fac[3:], DOWN, color=PRIME, buff=0.15)
            blab = T("every prime from 10 to 20", size=30, color=PRIME).next_to(brace, DOWN, buff=0.15)
            self.play(GrowFromCenter(brace), FadeIn(blab), run_time=0.7)
            for word, idx in zip(["eleven", "thirteen", "seventeen", "nineteen"], [3, 5, 7, 9]):
                self.at(word, lead=0.15)
                self.play(fac[idx].animate.set_color(PRIME).scale(1.15), run_time=0.35)
            self.play(FadeOut(dots), run_time=min(0.6, max(0.1, self.left() - 0.05)))

        # ------------------------------------------------------------ c: why — the fraction
        with self.beat("c") as d:
            head = VGroup(top, fac)
            self.play(FadeOut(brace), FadeOut(blab), head.animate.arrange(RIGHT, buff=0.25).scale(0.55).move_to(UP * 3.0), run_time=0.9)
            ns = [str(k) for k in range(20, 10, -1)]
            ds = [str(k) for k in range(10, 0, -1)]
            def prod(lst):
                parts = []
                for i, s in enumerate(lst):
                    if i: parts.append(r"\cdot")
                    parts.append(s)
                return M(*parts, size=60)
            num, den = prod(ns), prod(ds)
            bar = Line(LEFT, RIGHT).set_stroke(INK, 3)
            bar.set_width(num.width + 0.3)
            frac = VGroup(num, bar, den).arrange(DOWN, buff=0.22).move_to(UP * 0.75)
            nterm = {int(s): num[2 * i] for i, s in enumerate(ns)}
            dterm = {int(s): den[2 * i] for i, s in enumerate(ds)}
            self.play(FadeIn(num, shift=DOWN * 0.2), Create(bar), FadeIn(den, shift=UP * 0.2), run_time=1.0)
            self.at("Those primes")
            gold = [19, 17, 13, 11]
            rings = VGroup(*[SurroundingRectangle(nterm[p], color=PRIME, buff=0.1, corner_radius=0.1, stroke_width=3) for p in gold])
            self.play(*[nterm[p].animate.set_color(PRIME) for p in gold], LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2), run_time=1.0)
            self.at("can't be cancelled")
            pairs = [(10, 20), (9, 18), (8, 16), (7, 14), (6, 12), (5, 15)]
            links, strikes = VGroup(), VGroup()
            for b, t in pairs:
                links.add(Line(dterm[b].get_top(), nterm[t].get_bottom(), buff=0.06).set_stroke(MUTED, 2, opacity=0.8))
            for k in list(range(10, 0, -1)) + [20, 18, 16, 15, 14, 12]:
                mob = dterm[k] if k <= 10 else nterm[k]
                strikes.add(Line(mob.get_corner(DL), mob.get_corner(UR)).set_stroke(MUTED, 3))
            dim_targets = [dterm[k] for k in range(1, 11)] + [nterm[k] for k in (20, 18, 16, 15, 14, 12)]
            ct = min(2.4, self.cue("So the number") - self.cue("can't be cancelled") - 0.2)
            self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.2), run_time=ct * 0.45)
            self.play(LaggedStart(*[Create(s) for s in strikes], lag_ratio=0.06), *[m.animate.set_opacity(0.35) for m in dim_targets],
                      FadeOut(links), run_time=ct * 0.55)
            self.at("So the number")
            self.play(*[Indicate(nterm[p], color=PRIME, scale_factor=1.25) for p in gold], Indicate(fac[3:], color=PRIME, scale_factor=1.1), run_time=1.0)
            self.at("can't be very big")
            size = M("184{,}756", "<", "4^{10}", "=", "1{,}048{,}576", size=64).move_to(DOWN * 2.45)
            size[2:].set_color(WARM)
            self.play(FadeIn(size[0], shift=UP * 0.2), run_time=0.5)
            self.play(Write(size[1:]), run_time=min(1.4, max(0.3, self.left() - 0.1)))

        # ------------------------------------------------------------ d: the squeeze
        with self.beat("d") as d:
            self.play(FadeOut(VGroup(num, bar, den, rings, strikes, head)), size.animate.set_opacity(0.4), run_time=0.5)
            ineq = M(r"11", r"\cdot", "13", r"\cdot", "17", r"\cdot", "19", r"\;\le\;", r"\binom{20}{10}", r"\;<\;", r"4^{10}", size=76).move_to(UP * 2.0)
            for i in (0, 2, 4, 6): ineq[i].set_color(PRIME)
            ineq[10].set_color(WARM)
            self.play(*[TransformFromCopy(nterm[p], ineq[i]) for p, i in zip([11, 13, 17, 19], [0, 2, 4, 6])],
                      FadeIn(VGroup(ineq[1], ineq[3], ineq[5], ineq[7], ineq[8], ineq[9])),
                      TransformFromCopy(size[2], ineq[10]),
                      FadeOut(size), run_time=1.1)
            self.at("at least as big")
            nums = M("46{,}189", r"\;\le\;", "184{,}756", r"\;<\;", "1{,}048{,}576", size=60).next_to(ineq, DOWN, buff=0.6)
            nums[0].set_color(PRIME); nums[4].set_color(WARM)
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.2) for m in nums], lag_ratio=0.25), run_time=1.2)
            self.at("trapped under")
            gen = M(r"\prod_{n<p\le 2n} p", r"\;<\;", r"4^{n}", size=80).move_to(DOWN * 2.0)
            gen[0].set_color(PRIME); gen[2].set_color(WARM)
            self.play(FadeIn(gen, shift=UP * 0.2), run_time=0.9)
            # walls close in
            wl = VGroup(Line(UP * 0.95, DOWN * 0.95).set_stroke(PRIME, 6), T("divisibility", size=28, color=PRIME))
            wr = VGroup(Line(UP * 0.95, DOWN * 0.95).set_stroke(WARM, 6), T("size", size=28, color=WARM))
            wl[1].next_to(wl[0], UP, buff=0.12); wr[1].next_to(wr[0], UP, buff=0.12)
            wl.move_to(LEFT * 6.0 + DOWN * 2.15); wr.move_to(RIGHT * 6.0 + DOWN * 2.15)
            self.play(FadeIn(wl), FadeIn(wr), run_time=0.5)
            self.at("A fact about")
            tgtL = gen.get_left()[0] - 0.45; tgtR = gen.get_right()[0] + 0.45
            self.play(wl.animate.shift(RIGHT * (tgtL - wl[0].get_x())), wr.animate.shift(RIGHT * (tgtR - wr[0].get_x())),
                      run_time=min(2.2, self.cue("squeeze out") - self.cue("A fact about")), rate_func=rush_into)
            self.at("squeeze out")
            self.play(Indicate(gen[0], color=PRIME, scale_factor=1.15), wl.animate.shift(RIGHT * 0.12), wr.animate.shift(LEFT * 0.12),
                      run_time=min(1.0, max(0.3, self.left() - 0.1)))

        # ------------------------------------------------------------ e: the mystery number we need
        with self.beat("e") as d:
            scale2 = placed_scale()
            tilt2 = rig_scale(scale2)
            self.add(tilt2)
            crude = T("crude", size=30, color=MUTED).next_to(gen, RIGHT, buff=0.5)
            self.play(FadeIn(crude, shift=LEFT * 0.2), FadeOut(wl), FadeOut(wr), run_time=0.6)
            self.wait(0.6)
            self.play(FadeOut(VGroup(ineq, nums, gen, crude), shift=UP * 0.4),
                      FadeIn(scale2, shift=UP * 0.4), run_time=1.0)
            tok = number_token("?").move_to(token_spot(scale2))
            self.at("far more special")
            self.play(FadeIn(tok[1:], scale=0.3), LaggedStart(*[FadeIn(g, scale=0.6) for g in tok[0]], lag_ratio=0.3), run_time=1.0)
            hd = T("hugely divisible", size=30, color=PRIME).next_to(scale2.left_pan, DOWN, buff=0.25)
            ss = T("still small", size=30, color=WARM).next_to(scale2.right_pan, DOWN, buff=0.25)
            hd.add_updater(lambda m: m.next_to(scale2.left_pan, DOWN, buff=0.25))
            ss.add_updater(lambda m: m.next_to(scale2.right_pan, DOWN, buff=0.25))
            self.at("divisible by much")
            self.play(FadeIn(hd, shift=UP * 0.2), tilt2.animate.set_value(0.09), run_time=0.9)
            self.at("staying just as small")
            self.play(FadeIn(ss, shift=UP * 0.2), tilt2.animate.set_value(0.0), run_time=0.9)
            self.at("Building")
            self.play(tok[0].animate.scale(1.25).set_opacity(0.0), rate_func=there_and_back, run_time=1.2)
            self.play(Indicate(tok[2], color=PRIME, scale_factor=1.3), run_time=1.0)
            rest = self.left() - 0.05
            if rest > 0.2:
                self.play(tok.animate.shift(UP * 0.12), tilt2.animate.set_value(0.03), rate_func=there_and_back, run_time=rest)
        self.finish()
