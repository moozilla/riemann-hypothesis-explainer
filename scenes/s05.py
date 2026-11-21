import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *

SC = WARM  # the input s is always the warm accent in Act II


def tint(m, idxs, color):
    g = m[0]
    for i in idxs:
        g[i if i >= 0 else len(g) + i].set_color(color)
    return m


def frac(n, size=52, prime=False):
    """1/n^s with s in the input colour (and n gold if prime)."""
    m = M(rf"\frac{{1}}{{{n}^{{s}}}}", size=size)
    tint(m, [-1], SC)
    if prime:
        tint(m, range(2, len(m[0]) - 1), PRIME)
    return m


def euler_factor(p, size=48):
    m = M(rf"\frac{{1}}{{1-{p}^{{-s}}}}", size=size)
    nd = len(str(p))
    tint(m, range(4, 4 + nd), PRIME)
    tint(m, [-1], SC)
    return m


class S05(NarratedScene):
    sid = "s05"

    def construct(self):
        # ------------------------------------------------------------------ a: build the series
        with self.beat("a") as d:
            nmax = 5
            finals = [M("1", size=52)] + [frac(n) for n in range(2, nmax + 1)]
            pluses = [M("+", size=52) for _ in range(nmax)]
            dots = M(r"\cdots", size=52)
            row = []
            for i, f in enumerate(finals):
                row += [f, pluses[i]]
            row.append(dots)
            series = VGroup(*row).arrange(RIGHT, buff=0.28).move_to(UP * 0.2)
            # intermediate forms at the same centres
            nums = [M(str(n), size=60).move_to(finals[n - 1]) for n in range(1, nmax + 1)]
            pows = [tint(M(f"{n}^{{s}}", size=60), [-1], SC).move_to(finals[n - 1]) for n in range(1, nmax + 1)]
            flips = [frac(n).move_to(finals[n - 1]) for n in range(1, nmax + 1)]
            ndots = M(r"\cdots", size=60).move_to(dots)

            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in nums + [ndots]], lag_ratio=0.12, run_time=1.2))
            self.at("raise each")
            self.play(LaggedStart(*[ReplacementTransform(a, b) for a, b in zip(nums, pows)], lag_ratio=0.1, run_time=1.2))
            self.at("flip them")
            self.play(LaggedStart(*[ReplacementTransform(a, b) for a, b in zip(pows, flips)], lag_ratio=0.08, run_time=1.0))
            self.at("add them")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pluses], lag_ratio=0.1, run_time=0.8),
                      ReplacementTransform(ndots, dots, run_time=0.8))
            self.at("One, plus")
            self.play(ReplacementTransform(flips[0], finals[0]), run_time=0.5)
            for f in flips[1:]:
                self.remove(f)
            self.add(*finals[1:])
            # read along: one over two to the s, one over three to the s, and on forever
            for i, cue in [(1, "over two"), (2, "over three")]:
                self.at(cue, lead=0.4)
                self.play(Indicate(finals[i], color=INK, scale_factor=1.25), run_time=0.8)
            self.at("on forever", lead=0.3)
            self.play(LaggedStart(*[Indicate(m, color=INK, scale_factor=1.15) for m in finals[3:] + [dots]], lag_ratio=0.25, run_time=1.2))

            lhs = M(r"\zeta(s)", "=", size=60)
            lhs[0][2].set_color(SC)
            full = VGroup(lhs.copy(), series.copy()).arrange(RIGHT, buff=0.3).move_to(UP * 0.2)
            self.at("This is the zeta", lead=0.5)
            lhs.move_to(full[0])
            self.play(series.animate.move_to(full[1]), FadeIn(lhs, shift=RIGHT * 0.4), run_time=0.8)
            knob = SurroundingRectangle(lhs[0][2], color=SC, buff=0.08, corner_radius=0.06, stroke_width=3)
            knob_l = T("input", size=30, color=SC).next_to(knob, DOWN, buff=0.2)
            self.play(Create(knob), FadeIn(knob_l, shift=UP * 0.1), run_time=min(0.6, self.left() - 0.05))

        # ------------------------------------------------------------------ b: s = 2 -> pi^2/6
        with self.beat("b") as d:
            top = VGroup(lhs, series)
            st = ValueTracker(2.0)   # the input s
            kt = ValueTracker(0.0)   # how many terms are stacked (continuous)
            H = 2.0                  # screen units per 1
            base_y = -3.2
            col_x = -2.6
            NB = 40

            def stack():
                s, k = st.get_value(), kt.get_value()
                g = VGroup()
                y = base_y
                for n in range(1, NB + 1):
                    f = min(1.0, max(0.0, k - (n - 1)))
                    if f <= 0:
                        break
                    h = H * n ** (-s) * f
                    r = Rectangle(width=1.5, height=max(h, 1e-3), stroke_width=1.2 if h > 0.04 else 0,
                                  stroke_color=BG, fill_color=INK if n % 2 else MUTED, fill_opacity=0.9)
                    r.move_to([col_x, y + h / 2, 0])
                    g.add(r)
                    y += h
                return g

            def psum():
                s, k = st.get_value(), kt.get_value()
                tot = 0.0
                for n in range(1, NB + 1):
                    f = min(1.0, max(0.0, k - (n - 1)))
                    if f <= 0:
                        break
                    tot += n ** (-s) * f
                if k >= NB:  # the visible stack is truncated: add the (tiny) remainder so the readout is honest
                    s_ = s
                    tot = sum(n ** (-s_) for n in range(1, 4000)) + 4000 ** (1 - s_) / (s_ - 1)
                return tot

            stk = always_redraw(stack)
            target = PI ** 2 / 6
            dash = DashedLine([col_x - 0.75, base_y + H * target, 0], [3.0, base_y + H * target, 0], dash_length=0.12, stroke_width=3, color=PRIME)
            dash_l = M(r"\frac{\pi^2}{6} = 1.6449\ldots", size=40, color=PRIME).next_to(dash, RIGHT, buff=0.2)
            ground = Line([col_x - 1.3, base_y, 0], [col_x + 1.3, base_y, 0], stroke_width=3, color=MUTED)
            def _ro():
                v = psum()
                g = VGroup(M(r"=", size=44), DecimalNumber(v, num_decimal_places=4, font_size=44)).arrange(RIGHT, buff=0.15)
                return g.move_to([col_x - 1.0, base_y + H * v, 0], aligned_edge=RIGHT)
            readout = always_redraw(_ro)
            # the input knob: a slider for s
            sl = NumberLine(x_range=[1.5, 4, 0.5], length=4.0, color=MUTED, include_numbers=True, font_size=30,
                            numbers_to_include=[2, 3, 4], decimal_number_config={"num_decimal_places": 0}).move_to([4.0, -2.4, 0])
            sl.numbers.set_color(MUTED)
            mark = always_redraw(lambda: Triangle(fill_color=SC, fill_opacity=1, stroke_width=0).scale(0.14).rotate(PI)
                                 .next_to(sl.n2p(st.get_value()), UP, buff=0.04))
            sval = always_redraw(lambda: VGroup(M("s", "=", size=40, color=SC), DecimalNumber(st.get_value(), num_decimal_places=1, font_size=40, color=SC))
                                 .arrange(RIGHT, buff=0.12).next_to(sl, UP, buff=0.55))

            self.play(top.animate.scale(0.8).to_edge(UP, buff=0.45), FadeOut(knob), FadeOut(knob_l),
                      Create(ground), Create(sl), FadeIn(mark), FadeIn(sval), run_time=0.9)
            self.add(stk, readout)
            self.at("settles")
            # first terms slowly, then the rest pile on
            self.play(kt.animate.set_value(3), run_time=1.3, rate_func=linear)
            self.play(kt.animate.set_value(NB), Create(dash), run_time=1.4, rate_func=rate_functions.ease_in_quad)
            self.at("pi squared", lead=0.2)
            self.play(FadeIn(dash_l, shift=LEFT * 0.2), run_time=0.6)
            self.at("Different inputs")
            self.play(st.animate.set_value(3.0), run_time=0.9)
            self.play(st.animate.set_value(1.7), run_time=1.0)
            self.play(st.animate.set_value(2.0), run_time=min(0.7, self.left() - 0.1))

        # ------------------------------------------------------------------ c: Euler's product
        with self.beat("c") as d:
            stk.clear_updaters(); readout.clear_updaters(); mark.clear_updaters(); sval.clear_updaters()
            ps = [2, 3, 5, 7]
            facs = [euler_factor(p) for p in ps]
            dots2 = M(r"\cdots", size=52)
            dots_ = [M(r"\cdot", size=52) for _ in ps]
            lhs2 = M(r"\zeta(s)", "=", size=60); lhs2[0][2].set_color(SC)
            prod_row = VGroup(lhs2)
            for f, dt in zip(facs, dots_):
                prod_row.add(f, dt)
            prod_row.remove(dots_[-1]); prod_row.add(dots2)
            prod_row.arrange(RIGHT, buff=0.22).move_to(DOWN * 1.1)
            top.generate_target(); top.target.scale(1 / 0.8).move_to(UP * 1.5)
            lhs2.align_to(top.target, LEFT)
            prod_row[1:].next_to(lhs2, RIGHT, buff=0.3)
            dx = -VGroup(top.target, prod_row).get_center()[0]
            top.target.shift(RIGHT * dx); prod_row.shift(RIGHT * dx)
            self.play(FadeOut(VGroup(stk, readout, dash, dash_l, ground, sl, mark, sval)), MoveToTarget(top), run_time=0.9)
            # "nothing to do with primes": the denominators are just 2, 3, 4, 5, ...
            self.at("nothing to do")
            self.play(LaggedStart(*[Indicate(series[2 * i], color=MUTED, scale_factor=1.12) for i in range(1, 5)], lag_ratio=0.15), run_time=1.2)
            self.at("astonishing", lead=0.1)
            self.play(TransformFromCopy(lhs, lhs2), run_time=0.8)
            self.at("very same", lead=0.1)
            self.play(FadeIn(facs[0], shift=DOWN * 0.3), run_time=0.7)
            self.at("as a product", lead=0.2)
            rest = []
            for i in range(1, 4):
                rest += [FadeIn(dots_[i - 1]), FadeIn(facs[i], shift=DOWN * 0.3)]
            self.play(LaggedStart(*rest, FadeIn(dots2), lag_ratio=0.25, run_time=1.6))
            # the primes glow
            pr = VGroup(*[f[0][4:4 + len(str(p))] for f, p in zip(facs, ps)])
            self.at("and nothing else", lead=0.1)
            self.play(LaggedStart(*[Flash(g, color=PRIME, line_length=0.18, flash_radius=0.3) for g in pr], lag_ratio=0.2),
                      LaggedStart(*[Indicate(g, color=PRIME, scale_factor=1.5) for g in pr], lag_ratio=0.2), run_time=min(1.4, self.left() - 0.1))

        # ------------------------------------------------------------------ d: why - unique factorisation
        with self.beat("d") as d:
            sz = 58

            def bracket(p):
                parts = [M("(", size=sz + 10), M("1", size=sz), M("+", size=sz)]
                terms = []
                for k in (1, 2):
                    t = frac(p ** k, size=sz)
                    tint(t, range(2, len(t[0]) - 1), PRIME)
                    terms.append(t); parts += [t, M("+", size=sz)]
                parts += [M(r"\cdots", size=sz), M(")", size=sz + 10)]
                g = VGroup(*parts).arrange(RIGHT, buff=0.12)
                g.terms = terms; g.one = parts[1]
                return g

            br = [bracket(2), bracket(3), bracket(5)]
            col = VGroup(*br).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
            vd = M(r"\vdots", size=sz)
            times = VGroup(*[M(r"\times", size=sz, color=MUTED) for _ in range(3)])
            colg = VGroup(col, vd).arrange(DOWN, buff=0.3).move_to([-3.0, 0.2, 0])
            vd.align_to(col, LEFT).shift(RIGHT * 1.6)
            for tm, b in zip(times, [br[1], br[2], vd]):
                tm.next_to(b, LEFT, buff=0.25)
            times[2].set_opacity(0)
            self.play(FadeOut(lhs2), FadeOut(top, shift=UP * 0.4),
                      *[ReplacementTransform(f, b) for f, b in zip(facs, br)],
                      ReplacementTransform(VGroup(facs[3], *dots_[:3], dots2), vd),
                      FadeIn(times[:2]), run_time=1.4)

            def pick(terms, color):
                rings = VGroup(*[SurroundingRectangle(t, color=color, buff=0.07, corner_radius=0.08, stroke_width=3) for t in terms])
                cps = [t.copy() for t in terms]
                prod = VGroup()
                for k, c in enumerate(cps):
                    prod.add(c.copy())
                    if k < len(cps) - 1:
                        prod.add(M(r"\cdot", size=sz))
                prod.arrange(RIGHT, buff=0.18).move_to([3.9, 1.0, 0])
                return rings, cps, prod

            # pick one term from each bracket: 1/4^s, 1/3^s, 1/5^s  ->  1/60^s
            self.at("Multiply these")
            rings, cps, prod = pick([br[0].terms[1], br[1].terms[0], br[2].terms[0]], PRIME)
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.3), run_time=0.8)
            self.play(*[TransformFromCopy(c, q) for c, q in zip(cps, prod[0::2])], FadeIn(prod[1::2]), run_time=0.9)
            res = VGroup(M("=", size=56), frac(60, size=72)).arrange(RIGHT, buff=0.25).next_to(prod, DOWN, buff=0.6)
            self.play(FadeIn(res, shift=DOWN * 0.2), run_time=0.6)
            # and another: 1/2^s * 1 * 1/5^s -> 1/10^s
            self.at("exactly once", lead=0.6)
            rings2, cps2, prod2 = pick([br[0].terms[0], br[1].one, br[2].terms[0]], INK)
            res2 = VGroup(M("=", size=56), frac(10, size=72)).arrange(RIGHT, buff=0.25).next_to(prod2, DOWN, buff=0.6)
            self.play(ReplacementTransform(rings, rings2), ReplacementTransform(prod, prod2), ReplacementTransform(res, res2), run_time=0.9)

            # the bridge: sum over integers <=> product over primes
            self.at("So zeta is", lead=0.1)
            L = M(r"\sum_{n} \frac{1}{n^s}", size=80); tint(L, [-1], SC)
            R = M(r"\prod_{p} \frac{1}{1-p^{-s}}", size=80); tint(R, [1, 6], PRIME); tint(R, [-1], SC)
            arr = M(r"\Longleftrightarrow", size=80)
            bridge = VGroup(L, arr, R).arrange(RIGHT, buff=0.8).move_to(DOWN * 0.1)
            Ll = T("every whole number", size=32, color=INK).next_to(L, DOWN, buff=0.5)
            Rl = T("every prime", size=32, color=PRIME).next_to(R, DOWN, buff=0.5)
            zt = M(r"\zeta(s)", size=72); zt[0][2].set_color(SC)
            zt.next_to(bridge, UP, buff=0.8)
            self.play(FadeOut(VGroup(rings2, prod2, res2, times[:2]), shift=RIGHT * 0.3),
                      ReplacementTransform(VGroup(*br, vd), R), FadeIn(L, shift=RIGHT * 0.4), run_time=1.2)
            self.play(GrowFromCenter(arr), FadeIn(Ll, shift=UP * 0.2), FadeIn(Rl, shift=UP * 0.2), FadeIn(zt, shift=DOWN * 0.2), run_time=0.9)
            self.at("Whatever the primes")
            glow = VGroup(R[0][1].copy(), R[0][6].copy())
            self.play(LaggedStart(*[Flash(g, color=PRIME, line_length=0.25, flash_radius=0.45, num_lines=12) for g in glow], lag_ratio=0.3),
                      Indicate(R, color=PRIME, scale_factor=1.06), run_time=1.6)
            self.play(Indicate(L, color=INK, scale_factor=1.06), run_time=1.2)
            self.play(Indicate(R, color=PRIME, scale_factor=1.04), run_time=max(0.2, min(1.4, self.left() - 0.1)))
        self.finish()
