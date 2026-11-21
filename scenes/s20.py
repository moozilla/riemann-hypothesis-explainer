import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *
import math

RM_Y = -1.55
XS = np.linspace(-5.1, 5.1, 4)
ICON_Y = 1.25
CAP_Y = -0.7

# first zeros (imaginary parts) of Dirichlet L-functions on the critical line, computed with mpmath
L_ZEROS = {   # real characters mod 3, 4, 5, 7
    3: [8.04, 11.249, 15.705, 18.262, 20.456, 24.059, 26.578, 28.218, 30.745, 33.897, 35.608, 37.552, 39.485, 42.616],
    4: [6.021, 10.244, 12.988, 16.343, 18.292, 21.451, 23.278, 25.729, 28.36, 29.656, 32.592, 34.2, 36.143, 38.512, 40.323, 41.807],
    5: [6.648, 9.831, 11.959, 16.034, 17.567, 19.541, 22.227, 24.588, 26.776, 28.461, 29.708, 33.0, 34.729, 35.869, 38.129, 39.561, 41.842],
    7: [4.476, 6.845, 11.16, 12.49, 15.113, 16.803, 19.612, 21.9, 23.163, 24.499, 27.361, 29.179, 30.722, 32.476, 34.111, 35.312, 38.365, 39.483, 40.71, 42.305],
}


def strip_with(zeros, height, width, tmax):
    g = critical_strip(height=height, width=width, tmax=tmax, n_zeros=1, labels=False)
    g.remove(g.zeros)
    zs = VGroup(*[Dot(g.p2c(0.5, t), radius=0.06, color=ZERO).set_z_index(3) for t in zeros if t < tmax])
    g.add(zs); g.zeros = zs
    return g


def shade_halves(cs, opacity=0.4):
    s = cs.strip
    r = Rectangle(width=s.width / 2, height=s.height, stroke_width=0, fill_color=BAD, fill_opacity=opacity).align_to(s, RIGHT).align_to(s, DOWN)
    l = Rectangle(width=s.width / 2, height=s.height, stroke_width=0, fill_color=BAD, fill_opacity=opacity).align_to(s, LEFT).align_to(s, DOWN)
    return l, r


class S20(NarratedScene):
    sid = "s20"

    def rm(self, active, done):
        return roadmap(active=active, done=done).shift(UP * RM_Y)

    def construct(self):
        rmap = self.rm(0, 0)

        # ------------------------------------------------ station 1: the tower
        with self.beat("a") as d:
            self.play(FadeIn(rmap.links), LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in rmap.stations], lag_ratio=0.15), run_time=1.0)
            tower = lift_tower(floors=6, width=1.45, gap=0.44, grow=0.1, labels=False).move_to([XS[0], ICON_Y + 0.15, 0])
            cap1 = M(r"m \approx \sqrt{X}", r"\text{ lifts}", size=38, color=LIFT).move_to([XS[0], CAP_Y, 0])
            self.at("tower of theta lifts")
            self.play(LaggedStart(*[GrowFromCenter(f) for f in tower.floors], lag_ratio=0.2), run_time=1.2)
            self.play(LaggedStart(*[GrowArrow(a) for a in tower.arrows], lag_ratio=0.2), run_time=0.8)
            self.at("square root")
            self.play(Write(cap1), run_time=0.9)
            self.at("Each story")
            mult = VGroup(*[Dot(radius=0.07, color=PRIME) for _ in range(6)])
            for f, dt in zip(tower.floors, mult):
                dt.move_to(f.get_right() + RIGHT * 0.25)
            rt = min(1.6, self.left() - 0.9)
            self.play(LaggedStart(*[AnimationGroup(Indicate(f, color=LIFT, scale_factor=1.08), FadeIn(dt, scale=2)) for f, dt in zip(tower.floors, mult)],
                                  lag_ratio=0.3), run_time=rt)
            self.play(Transform(rmap, self.rm(1, 1)), run_time=min(0.7, self.left() - 0.05))

        # ------------------------------------------------ station 2: token on the scale, lattice, plug
        with self.beat("b") as d:
            sc = balance_scale()
            sc.left_pan.remove(sc.left_pan[2]); sc.right_pan.remove(sc.right_pan[2])
            sc.scale(0.55).move_to([XS[1], ICON_Y - 0.15, 0])
            tok = number_token("?", r=0.42).scale(0.62)
            dish = sc.left_pan[1]
            tok.move_to(dish.get_bottom() + UP * (tok[1].height / 2 + 0.02))
            self.play(FadeIn(sc, shift=UP * 0.2), run_time=0.7)
            self.at("a number")
            self.play(FadeIn(tok, shift=DOWN * 0.8), run_time=0.6)
            self.play(Wiggle(VGroup(sc.beam_group, tok), scale_value=1.0, rotation_angle=0.02 * TAU, n_wiggles=3), run_time=0.9)
            # mini lattice + vectors and a plug, side by side above the scale
            lat = VGroup(*[Dot([i * 0.28, j * 0.28, 0], radius=0.035, color=MUTED) for i in range(4) for j in range(4)])
            vecs = VGroup(Arrow(ORIGIN, [0.84, 0.28, 0], buff=0, stroke_width=3, color=LIFT, tip_length=0.12),
                          Arrow(ORIGIN, [-0.0, 0.84, 0], buff=0, stroke_width=3, color=LIFT, tip_length=0.12))
            lat_icon = VGroup(lat, vecs.shift(lat[0].get_center())).move_to([XS[1] - 0.75, 2.9, 0])
            tank = VMobject().set_points_as_corners([[-0.5, 0.35, 0], [-0.5, -0.2, 0], [0.5, -0.2, 0], [0.5, 0.35, 0]]).set_stroke(INK, 3)
            plug = RoundedRectangle(width=0.42, height=0.2, corner_radius=0.08, stroke_width=0, fill_color=GOOD, fill_opacity=1).move_to([0.05, -0.2, 0])
            drop = Dot([0.05, -0.45, 0], radius=0.06, color=LIFT)
            plug_icon = VGroup(tank, plug, drop).move_to([XS[1] + 0.75, 2.9, 0])
            plug.shift(DOWN * 0.45)
            self.at("Pool the divisibility")
            self.play(FadeIn(lat, lag_ratio=0.05), GrowArrow(vecs[0]), GrowArrow(vecs[1]), run_time=0.8)
            self.at("plug the last leak")
            self.play(Create(tank), FadeIn(drop), FadeIn(plug), run_time=0.4)
            self.play(plug.animate.shift(UP * 0.45), drop.animate.set_opacity(0), run_time=0.5)
            self.play(Transform(rmap, self.rm(2, 2)), run_time=min(0.7, self.left() - 0.05))

        # ------------------------------------------------ station 3: wobble under the ceiling
        with self.beat("c") as d:
            ps = primes_upto(1200)
            ax = Axes(x_range=[0, 1000, 250], y_range=[-36, 40, 20], x_length=2.9, y_length=2.6,
                      axis_config=dict(stroke_color=MUTED, stroke_width=2, include_ticks=False, tip_length=0.12, tip_width=0.12)
                      ).move_to([XS[2], ICON_Y, 0])
            # Chebyshev psi(x) - x, really computed
            xs = np.arange(2, 1000, 2.0)
            pp = [(p, math.log(p)) for p in ps]
            pk = sorted({p ** k: lg for p, lg in pp for k in range(1, 12) if p ** k < 1000}.items())
            psi, j, vals = 0.0, 0, []
            for x in xs:
                while j < len(pk) and pk[j][0] <= x:
                    psi += pk[j][1]; j += 1
                vals.append(psi - x)
            wob = VMobject().set_points_as_corners([ax.c2p(x, v) for x, v in zip(xs, vals)]).set_stroke(PRIME, 2)
            ceil = ax.plot(lambda x: math.sqrt(x), x_range=[1, 1000], color=GOOD, stroke_width=4)
            forb = ax.get_area(ceil, x_range=[1, 1000], bounded_graph=ax.plot(lambda x: 40, x_range=[1, 1000]), color=BAD, opacity=0.22)
            cap3 = M(r"\text{overshoot} \le \sqrt{X}", size=36, color=GOOD).move_to([XS[2], CAP_Y, 0])
            self.play(Create(ax), run_time=0.6)
            self.play(Create(ceil), FadeIn(forb), run_time=0.8)
            self.at("weighted count")
            self.play(Create(wob), run_time=min(2.6, self.cue("square root") - (self.now() - self._beat_start)), rate_func=linear)
            self.at("square root")
            self.play(Write(cap3), Indicate(ceil, color=GOOD, scale_factor=1.0), run_time=0.9)
            self.play(Transform(rmap, self.rm(3, 3)), run_time=min(0.7, self.left() - 0.05))

        # ------------------------------------------------ station 4: zeros on the line; then every L-function
        with self.beat("d") as d:
            H, W, TM = 2.7, 1.15, 40
            cs = strip_with(zeta_zeros(8), H, W, TM).move_to([XS[3], ICON_Y + 0.1, 0])
            lsh, rsh = shade_halves(cs)
            self.play(FadeIn(cs), run_time=0.7)
            self.at("No zeros to the right")
            self.play(FadeIn(rsh), run_time=0.6)
            self.at("Symmetry")
            mirror = CurvedArrow(cs.p2c(0.85, 33), cs.p2c(0.15, 33), angle=-PI / 2.5, color=INK, stroke_width=3, tip_length=0.14)
            self.play(Create(mirror), run_time=0.5)
            self.play(FadeIn(lsh), FadeOut(mirror), run_time=0.6)
            glow = cs.line.copy().set_stroke(ZERO, 12, opacity=0.35)
            self.play(FadeIn(glow), Transform(rmap, self.rm(4, 4)), run_time=0.8)

            self.at("And the same machine")
            others = VGroup(tower, cap1, mult, sc, tok, lat_icon, plug_icon, ax, ceil, forb, wob, cap3)
            # five strips: zeta and four Dirichlet L-functions
            HH, WW = 4.0, 1.15
            sets = [zeta_zeros(14)] + [L_ZEROS[q] for q in (3, 4, 5, 7)]
            names = [r"\zeta(s)", r"L(s,\chi_3)", r"L(s,\chi_4)", r"L(s,\chi_5)", r"L(s,\chi_7)"]
            cx = np.linspace(-5.0, 5.0, 5)
            TM = 44
            strips = VGroup()
            for z, x in zip(sets, cx):
                s = strip_with(z, HH, WW, TM).move_to([x, 0.15, 0])
                l, r = shade_halves(s, opacity=0.2)
                g = s.line.copy().set_stroke(ZERO, 14, opacity=0.4)
                strips.add(VGroup(s, l, r, g))
            labs = VGroup(*[M(n, size=40, color=INK).next_to(strips[i][0].strip, DOWN, buff=0.55) for i, n in enumerate(names)])
            src = VGroup(cs, lsh, rsh, glow)
            self.play(FadeOut(others), FadeOut(rmap), run_time=0.6)
            self.play(LaggedStart(*[TransformFromCopy(src, st) for st in strips], lag_ratio=0.12), FadeOut(src), run_time=1.6)
            self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.15) for l in labs], lag_ratio=0.12), run_time=0.8)
            self.at("The generalized")
            title = T("Generalized Riemann Hypothesis", size=54, weight=MEDIUM)
            tomb = Square(side_length=0.36, stroke_width=0, fill_color=GOOD, fill_opacity=1)
            head = VGroup(title, tomb).arrange(RIGHT, buff=0.35, aligned_edge=DOWN).move_to(UP * 3.05)
            rt = min(1.3, self.left() - 0.6)
            self.play(Write(title), run_time=rt)
            self.play(FadeIn(tomb, scale=1.6), *[Indicate(st[3], color=ZERO, scale_factor=1.0) for st in strips], run_time=min(0.5, self.left()))
        self.finish()
