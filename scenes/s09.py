import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *
import bisect

# Imaginary parts (0 < t < 40) of the zeros of Dirichlet L-functions on Re s = 1/2,
# computed with mpmath.dirichlet + findroot (see report); zeta from the shared cache.
L_ZEROS = {
    "chi3": [8.0397, 11.2492, 15.7046, 18.262, 20.4558, 24.0594, 26.5779, 28.2182, 30.745, 33.8974, 35.6084, 37.5518, 39.4852],
    "chi4": [6.0209, 10.2438, 12.9881, 16.3426, 18.292, 21.4506, 23.2784, 25.7288, 28.3596, 29.6564, 32.5922, 34.2, 36.1429, 38.5119],
    "chi5": [6.1836, 8.4572, 12.6749, 14.825, 17.3378, 18.9986, 22.4876, 24.3653, 25.5312, 27.9828, 30.4636, 32.1952, 34.4572, 35.4909, 37.272],
    "chi7": [4.4757, 6.8455, 11.1602, 12.4896, 15.1129, 16.8029, 19.6119, 21.8999, 23.163, 24.4988, 27.3615, 29.1789, 30.7219, 32.4759, 34.1112, 35.3118, 38.3646, 39.4826],
}

DIGITS = [1, 3, 7, 9]
TEAM = {1: PRIME, 3: WARM, 7: LIFT, 9: GOOD}
CHI5 = {0: None, 1: 0.0, 2: PI / 2, 3: -PI / 2, 4: PI}   # chi mod 5: 1, i, -i, -1, 0


def dial(angle, r=0.4):
    c = Circle(radius=r, stroke_color=MUTED, stroke_width=2)
    cen = Dot(radius=0.035, color=LIFT)
    g = VGroup(c, cen)
    if angle is None:
        g.add(Dot(radius=0.07, color=MUTED))
        g.arrow = None
    else:
        a = Arrow(ORIGIN, RIGHT * r, buff=0, stroke_width=4, color=LIFT, tip_length=0.16, max_tip_length_to_length_ratio=0.45)
        a.rotate(angle, about_point=ORIGIN)
        g.add(a); g.arrow = a
    return g


class S09(NarratedScene):
    sid = "s09"

    def construct(self):
        P = primes_upto(10000)
        by = {k: [p for p in P if p % 10 == k] for k in DIGITS}
        xs = {1: -3.9, 3: -1.3, 7: 1.3, 9: 3.9}
        BASE, HMAX, BW = -2.55, 3.9, 1.5
        cnt = {k: ValueTracker(0) for k in DIGITS}

        def bar_h():
            m = max(max(cnt[k].get_value() for k in DIGITS), 5)
            return {k: HMAX * cnt[k].get_value() / m for k in DIGITS}

        def make_bar(k):
            def f():
                h = max(bar_h()[k], 0.001)
                return Rectangle(width=BW, height=h, stroke_width=0, fill_color=TEAM[k], fill_opacity=0.85).move_to(
                    [xs[k], BASE + h / 2, 0])
            return always_redraw(f)

        bars = {k: make_bar(k) for k in DIGITS}
        nums = {}
        for k in DIGITS:
            n = Integer(0, font_size=34, color=TEAM[k])
            n.add_updater(lambda m, k=k: m.set_value(int(round(cnt[k].get_value()))).next_to([xs[k], BASE + bar_h()[k], 0], UP, buff=0.12))
            nums[k] = n
        floor = Line([-5.3, BASE, 0], [5.3, BASE, 0]).set_stroke(MUTED, 2)
        labs = VGroup(*[M(r"\dots" + str(k), size=48, color=TEAM[k]).next_to([xs[k], BASE, 0], DOWN, buff=0.22) for k in DIGITS])

        with self.beat("a") as d:
            self.play(Create(floor), FadeIn(labs, shift=UP * 0.2), run_time=0.6)
            self.add(*bars.values(), *nums.values())
            first = [2, 3, 5, 7, 11, 13, 17, 19]
            toks = VGroup(*[M(str(p), size=46, color=PRIME) for p in first]).arrange(RIGHT, buff=0.55).move_to(UP * 3.0)
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.3) for t in toks], lag_ratio=0.12), run_time=1.0)
            self.at("Sort the primes")
            fly = []
            for p, t in zip(first, toks):
                if p in (2, 5): continue
                k = p % 10
                fly.append(Succession(t.animate(run_time=0.7).move_to([xs[k], BASE + 0.4, 0]).scale(0.7).set_color(TEAM[k]),
                                      AnimationGroup(FadeOut(t, run_time=0.2), cnt[k].animate(run_time=0.2).increment_value(1))))
            self.play(LaggedStart(*fly, lag_ratio=0.25), run_time=2.0)
            self.at("Apart from two")
            out = VGroup(toks[0], toks[2])
            self.play(out.animate.set_color(MUTED).arrange(RIGHT, buff=0.45).move_to([-5.7, 3.0, 0]), run_time=0.8)
            strike = VGroup(*[Line(t.get_corner(DL), t.get_corner(UR)).set_stroke(BAD, 3) for t in out])
            self.play(Create(strike), run_time=0.4)
            # the race: all primes up to 10,000
            done = {k: int(cnt[k].get_value()) for k in DIGITS}
            L = ValueTracker(np.log(20))
            for k in DIGITS:
                cnt[k].add_updater(lambda m, k=k: m.set_value(bisect.bisect_right(by[k], np.exp(L.get_value()))))
            upto = VGroup(T("primes below", size=30, color=MUTED), Integer(20, font_size=40, color=INK, group_with_commas=True)).arrange(RIGHT, buff=0.2)
            upto.move_to([3.6, 3.0, 0])
            upto[1].add_updater(lambda m: m.set_value(int(np.exp(L.get_value()))))
            self.play(FadeIn(upto), run_time=0.4)
            self.play(L.animate.set_value(np.log(10000)), run_time=self.cue("Do the four") - (self.now() - self._beat_start) + 0.6, rate_func=rate_functions.ease_in_out_sine)
            q = T("equal shares?", size=40, weight=MEDIUM).move_to([-2.6, 3.0, 0])
            self.play(FadeIn(q, shift=DOWN * 0.2), run_time=0.6)

        with self.beat("b") as d:
            for k in DIGITS: cnt[k].clear_updaters()
            eq_y = BASE + HMAX * 306 / max(len(by[k]) for k in DIGITS)
            eq = DashedLine([-5.0, BASE + HMAX * (len(P) - 2) / 4 / max(len(by[k]) for k in DIGITS), 0], [5.0, BASE + HMAX * (len(P) - 2) / 4 / max(len(by[k]) for k in DIGITS), 0],
                            dash_length=0.12).set_stroke(INK, 2.5)
            yes = T("yes", size=40, color=GOOD, weight=MEDIUM).move_to(q)
            self.play(Create(eq), ReplacementTransform(q, yes), run_time=1.0)
            self.at("But how evenly")
            self.play(Indicate(VGroup(*nums.values()), scale_factor=1.25, color=INK), run_time=1.0)
            self.at("you build cousins")
            race = VGroup(*bars.values(), *nums.values(), floor, labs, eq, yes, upto, out, strike)
            for m in race: m.clear_updaters()
            zeta = M(r"\zeta(s)", r"=", r"\sum", r"\frac{1}{n^s}", size=60).move_to(UP * 2.4)
            self.play(FadeOut(race, shift=DOWN * 0.5), FadeIn(zeta, shift=DOWN * 0.3), run_time=1.0)
            Lf = M(r"L(s,\chi)", r"=", r"\sum", r"\frac{\chi(n)}{n^s}", size=60).move_to(UP * 2.4)
            Lf[3][0:4].set_color(LIFT); Lf[0][4].set_color(LIFT)
            self.at("Dirichlet")
            self.play(TransformMatchingShapes(zeta, Lf), run_time=1.0)
            # the series with a dial on each term
            terms = VGroup()
            for n in range(1, 11):
                frac = M(r"\frac{1}{" + str(n) + "^s}", size=48)
                terms.add(frac)
            terms.arrange(RIGHT, buff=0.64).move_to(DOWN * 1.5)
            plus = VGroup(*[M("+", size=40, color=MUTED).move_to((terms[i].get_right() + terms[i + 1].get_left()) / 2) for i in range(9)])
            dots_ = M(r"\cdots", size=40, color=MUTED).next_to(terms, RIGHT, buff=0.25)
            dials = VGroup(*[dial(CHI5[n % 5]).next_to(terms[n - 1], UP, buff=0.5) for n in range(1, 11)])
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in terms], lag_ratio=0.08), FadeIn(plus), FadeIn(dots_), run_time=1.2)
            self.at("a twist")
            # arrows start pointing right and turn to chi(n)
            for n, g in zip(range(1, 11), dials):
                if g.arrow is not None:
                    g.arrow.rotate(-CHI5[n % 5], about_point=g[0].get_center())
            self.play(LaggedStart(*[Create(g[0]) for g in dials], lag_ratio=0.06), FadeIn(VGroup(*[VGroup(*g[1:]) for g in dials])), run_time=1.0)
            self.play(*[Rotate(g.arrow, CHI5[n % 5], about_point=g[0].get_center()) for n, g in zip(range(1, 11), dials) if g.arrow is not None and CHI5[n % 5] != 0],
                      run_time=1.4)
            vals = VGroup(*[M(s, size=36, color=LIFT if s != "0" else MUTED).next_to(g, UP, buff=0.15)
                            for s, g in zip(["1", "i", "-i", "-1", "0"] * 2, dials)])
            self.play(LaggedStart(*[FadeIn(v, shift=DOWN * 0.1) for v in vals], lag_ratio=0.06), run_time=0.9)
            self.at("remainder")
            boxes = VGroup(*[SurroundingRectangle(VGroup(dials[i:i + 5], terms[i:i + 5], vals[i:i + 5]), buff=0.1, corner_radius=0.12)
                             .set_stroke(LIFT, 2.5, opacity=0.8) for i in (0, 5)])
            self.play(Create(boxes[0]), run_time=0.6)
            self.play(TransformFromCopy(boxes[0], boxes[1]), run_time=min(0.8, self.left() - 0.1))

        with self.beat("c") as d:
            names = [r"\zeta(s)", r"L(s,\chi_3)", r"L(s,\chi_4)", r"L(s,\chi_5)", r"L(s,\chi_7)"]
            zs = [[t for t in zeta_zeros(12) if t < 40]] + [L_ZEROS[k] for k in ("chi3", "chi4", "chi5", "chi7")]
            tints = [ZERO, PRIME, WARM, LIFT, GOOD]
            strips, nlabs = VGroup(), VGroup()
            for i, (nm, zz, tint) in enumerate(zip(names, zs, tints)):
                s = critical_strip(height=4.8, width=1.3, tmax=40, n_zeros=0, labels=False).move_to([-5.0 + 2.5 * i, -0.3, 0])
                s.strip.set_fill(tint, 0.14)
                s.zeros.add(*[Dot(s.p2c(0.5, t), radius=0.06, color=ZERO).set_z_index(3) for t in zz])
                strips.add(s)
                nlabs.add(M(nm, size=36, color=INK).next_to(s.axis, DOWN, buff=0.3).set_x(s.line.get_x()))
            self.play(FadeOut(VGroup(terms, plus, dots_, dials, vals, boxes, Lf)), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(VGroup(s.strip, s.edges, s.axis, s.line), shift=UP * 0.2) for s in strips], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(l) for l in nlabs], lag_ratio=0.15), run_time=1.6)
            self.play(LaggedStart(*[LaggedStart(*[GrowFromCenter(z) for z in s.zeros], lag_ratio=0.08) for s in strips], lag_ratio=0.12), run_time=2.0)
            self.at("The generalized")
            title = T("Generalized Riemann Hypothesis", size=40, weight=MEDIUM).move_to(UP * 3.3)
            self.play(Write(title), run_time=1.3)
            self.at("all of their zeros")
            self.play(*[s.line.animate.set_stroke(width=6) for s in strips], *[z.animate(rate_func=there_and_back).scale(1.7) for s in strips for z in s.zeros], run_time=1.2)
            self.play(*[s.line.animate.set_stroke(width=3) for s in strips], run_time=0.5)
            self.at("This is the statement")
            sweep = Rectangle(width=0.5, height=5.6, stroke_width=0, fill_color=GOOD, fill_opacity=0.25).move_to([-6.6, -0.3, 0])
            checks = VGroup(*[M(r"\checkmark", size=56, color=GOOD).next_to(s.strip, UP, buff=0.18) for s in strips])
            self.play(sweep.animate.move_to([6.6, -0.3, 0]),
                      LaggedStart(*[AnimationGroup(FadeIn(c, scale=1.6), s.line.animate.set_color(GOOD)) for c, s in zip(checks, strips)], lag_ratio=0.2),
                      run_time=min(2.0, self.left() - 0.6), rate_func=linear)
            self.play(FadeOut(sweep), *[s.line.animate.set_color(ZERO) for s in strips], run_time=0.5)
        self.finish()
