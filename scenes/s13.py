import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *


def prime_powers(n):
    out = []
    for p in primes_upto(n):
        q = p
        while q <= n:
            out.append((q, p)); q *= p
    return sorted(out)


def psi_corners(xmax):
    """(x, y) corners of Chebyshev's psi on [0, xmax]."""
    pts, y = [(0.0, 0.0)], 0.0
    for q, p in prime_powers(int(xmax)):
        pts.append((q, y)); y += np.log(p); pts.append((q, y))
    pts.append((xmax, y))
    return np.array(pts)


def poly(ax, xy, **stroke):
    return VMobject().set_points_as_corners(ax.c2p(xy[:, 0], xy[:, 1]).T).set_stroke(**stroke)


def nums(ax, vals, axis, size=24, fmt=str):
    out = VGroup()
    for v in vals:
        if axis == "x":
            out.add(M(fmt(v), size=size, color=MUTED).next_to(ax.c2p(v, ax.y_range[0]), DOWN, buff=0.18))
        else:
            out.add(M(fmt(v), size=size, color=MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.15))
    return out


class S13(NarratedScene):
    sid = "s13"

    def construct(self):
        axcfg = dict(color=MUTED, stroke_width=2, include_ticks=True, tick_size=0.05)

        # ================================================================== a
        ax1 = Axes(x_range=[0, 30, 5], y_range=[0, 30, 5], x_length=11.2, y_length=6.2, tips=False, axis_config=axcfg).move_to(RIGHT * 0.3 + UP * 0.1)
        n1 = VGroup(nums(ax1, range(10, 31, 10), "x"), nums(ax1, range(10, 31, 10), "y"))
        st1 = poly(ax1, psi_corners(30), color=PRIME, width=4)
        tk1 = VGroup(*[Line(ax1.c2p(p, 0) + DOWN * 0.12, ax1.c2p(p, 0) + UP * 0.12).set_stroke(PRIME, 4) for p in primes_upto(30)])
        name = T("each prime p counts", size=32).to_corner(UL, buff=0.55).shift(RIGHT * 0.8)
        lnp = M(r"\ln p", size=44, color=PRIME).next_to(name, RIGHT, buff=0.2)

        def step_brace(p):
            y0 = sum(np.log(pp) for q, pp in prime_powers(p) if q < p)
            ln = Line(ax1.c2p(p, y0), ax1.c2p(p, y0 + np.log(p)))
            b = Brace(ln, RIGHT, buff=0.08, color=PRIME)
            lab = M(rf"\ln {p}", size=32, color=PRIME).next_to(b, RIGHT, buff=0.1)
            return VGroup(b, lab)

        with self.beat("a") as d:
            self.play(Create(ax1), FadeIn(n1), run_time=0.9)
            self.play(Create(st1, rate_func=linear), LaggedStart(*[GrowFromCenter(t) for t in tk1], lag_ratio=0.1), run_time=2.2)
            self.at("weight each prime")
            br = VGroup(step_brace(7), step_brace(23), step_brace(29))
            self.play(FadeIn(name), Write(lnp), LaggedStart(*[FadeIn(b, shift=LEFT * 0.1) for b in br], lag_ratio=0.3), run_time=1.4)
            self.at("the prediction becomes")
            diag1 = Line(ax1.c2p(0, 0), ax1.c2p(30, 30)).set_stroke(INK, 3)
            self.play(Create(diag1), FadeOut(br), run_time=1.0)
            # zoom out to 100
            ax2 = Axes(x_range=[0, 100, 10], y_range=[0, 100, 10], x_length=11.2, y_length=6.2, tips=False, axis_config=axcfg).move_to(ax1)
            n2 = VGroup(nums(ax2, range(20, 101, 20), "x"), nums(ax2, range(20, 101, 20), "y"))
            st2 = poly(ax2, psi_corners(100), color=PRIME, width=4)
            diag2 = Line(ax2.c2p(0, 0), ax2.c2p(100, 100)).set_stroke(INK, 3)
            tk2 = VGroup(*[Line(ax2.c2p(p, 0) + DOWN * 0.1, ax2.c2p(p, 0) + UP * 0.1).set_stroke(PRIME, 3) for p in primes_upto(100)])
            xl = M(r"y = X", size=44, color=INK).next_to(ax2.c2p(100, 100), DOWN + LEFT, buff=0.1).shift(LEFT * 0.6)
            self.at("the total up to X")
            self.play(ReplacementTransform(ax1, ax2), ReplacementTransform(n1, n2), ReplacementTransform(st1, st2),
                      ReplacementTransform(diag1, diag2), ReplacementTransform(tk1, tk2[:len(tk1)]), FadeIn(tk2[len(tk1):]), run_time=1.8)
            self.play(Write(xl), run_time=0.7)

        # ================================================================== b   (error, ceiling)
        XM = 10000
        ax3 = Axes(x_range=[0, XM, 2000], y_range=[-120, 160, 40], x_length=11.6, y_length=6.0, tips=False, axis_config=axcfg).move_to(RIGHT * 0.4 + DOWN * 0.35)
        n3 = nums(ax3, range(2000, XM + 1, 2000), "x", size=22, fmt=lambda v: f"{v:,}".replace(",", "{,}"))
        c = psi_corners(XM)
        err = c.copy(); err[:, 1] = c[:, 1] - c[:, 0]
        errc = poly(ax3, err, color=PRIME, width=2.5)
        zero_line = Line(ax3.c2p(0, 0), ax3.c2p(XM, 0)).set_stroke(INK, 2.5, opacity=0.7)
        xs = np.linspace(0, XM, 600)
        ceil = VMobject().set_points_smoothly(ax3.c2p(xs, np.sqrt(xs)).T).set_stroke(INK, 4)
        forb = VMobject().set_points_as_corners([*ax3.c2p(xs, np.sqrt(xs)).T, ax3.c2p(XM, 160), ax3.c2p(0, 160)]).set_stroke(width=0).set_fill(BAD, 0.18)
        forb_l = T("forbidden", size=36, color=BAD, weight=MEDIUM).move_to(ax3.c2p(2600, 128))
        sq = M(r"+\sqrt{X}", size=40, color=INK).next_to(ax3.c2p(XM, 100), DOWN, buff=0.2).shift(LEFT * 0.4)
        ylab = T("weighted count − X", size=30, color=PRIME).next_to(ax3.c2p(0, -120), UP, buff=0.0).align_to(ax3.c2p(250, 0), LEFT).shift(UP * 0.15)
        ineq = VGroup(T("weighted count", size=34), M(r"\le\; X + \sqrt{X}", size=44)).arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.25)
        nofloor = T("no floor", size=30, color=MUTED).move_to(ax3.c2p(7400, -95))

        with self.beat("b") as d:
            self.play(FadeOut(VGroup(name, lnp, xl, tk2)), run_time=0.5)
            self.play(ReplacementTransform(ax2, ax3), FadeOut(n2), FadeIn(n3), ReplacementTransform(st2, errc),
                      ReplacementTransform(diag2, zero_line), run_time=2.0)
            self.play(FadeIn(ylab), run_time=0.5)
            self.at("can't overshoot")
            self.play(Create(ceil), run_time=1.4)
            self.play(FadeIn(forb), FadeIn(forb_l), Write(sq), run_time=1.0)
            self.play(FadeIn(ineq, shift=DOWN * 0.2), run_time=0.8)
            self.at("One side only")
            self.play(Indicate(ceil, color=BAD, scale_factor=1.0), run_time=0.9)
            self.at("with no floor")
            self.play(FadeIn(nofloor, shift=UP * 0.2), run_time=0.6)

        # ================================================================== c   (Landau)
        big = critical_strip(height=6.4, width=4.4, tmax=40, n_zeros=6).move_to(UP * 0.25)
        small_pos = LEFT * 5.25 + UP * 0.6
        S = 0.42
        beta, g0 = 0.9, zeta_zeros(1)[0]
        ghost = Dot(big.p2c(beta, g0), radius=0.13, color=BAD).set_z_index(5)
        halo = Circle(radius=0.28, color=BAD, stroke_width=3).move_to(ghost)
        gg = VGroup(big, ghost, halo)
        gg_small = gg.copy().scale(S).move_to(small_pos)
        plot = VGroup(ax3, n3, errc, zero_line, ceil, forb, forb_l, sq, ylab, nofloor)
        # wave of the ghost zero: A x^beta cos(g ln x + phi), crests timed to break the ceiling
        A = 4000 ** -(beta - 0.5)
        phi = -g0 * np.log(6100)
        wx = np.concatenate([np.linspace(1, 300, 1500), np.linspace(300, XM, 1500)])
        wy = A * wx ** beta * np.cos(g0 * np.log(wx) + phi)

        with self.beat("c") as d:
            plot.remove(nofloor)
            self.play(FadeOut(ineq), FadeOut(nofloor), errc.animate.set_stroke(opacity=0.4), run_time=0.5)
            self.play(plot.animate.scale(0.82).move_to(RIGHT * 1.25 + DOWN * 0.35), run_time=0.9)
            self.play(FadeIn(gg_small[0]), run_time=0.6)
            self.at("a zero off the line")
            self.play(FadeIn(gg_small[1], scale=2), Create(gg_small[2]), run_time=0.6)
            wave = VMobject().set_points_as_corners(ax3.c2p(wx, np.clip(wy, -118, 158)).T).set_stroke(BAD, 3.5)
            self.at("waves go up")
            self.play(Create(wave, rate_func=linear), run_time=2.8)
            self.at("Edmund Landau")
            land = T("Landau", size=36, color=BAD, weight=MEDIUM).next_to(gg_small, DOWN, buff=0.35)
            self.play(FadeIn(land, shift=UP * 0.2), run_time=0.6)
            self.at("punch through")
            crest = [i for i in range(1, len(wx) - 1) if wy[i] > np.sqrt(wx[i]) * 1.08 and wy[i] >= wy[i - 1] and wy[i] >= wy[i + 1]]
            pts = [ax3.c2p(wx[i], wy[i]) for i in crest]
            self.play(LaggedStart(*[Flash(p, color=BAD, flash_radius=0.35, line_length=0.3, num_lines=12) for p in pts], lag_ratio=0.4), run_time=1.5)

        # ================================================================== d   (trap the zeros on the line)
        with self.beat("d") as d:
            gg_big = gg
            self.play(FadeOut(VGroup(plot, wave, land)), run_time=0.6)
            self.remove(gg_small); self.add(gg_small)
            self.play(Transform(gg_small, gg_big), run_time=1.0)
            W, H = big.strip.width, big.strip.height
            right = Rectangle(width=W / 2 - 0.05, height=H, stroke_width=0, fill_color=BAD, fill_opacity=0.28).move_to(big.strip.get_center() + RIGHT * (W / 4 + 0.025))
            left = right.copy().move_to(big.strip.get_center() + LEFT * (W / 4 + 0.025))
            no_r = T("no zeros", size=34, color=BAD, weight=MEDIUM).move_to(right).shift(DOWN * 1.9)
            no_l = no_r.copy().move_to(left).shift(DOWN * 1.9)
            cross = VGroup(Line(UL, DR), Line(UR, DL)).set_stroke(BAD, 6).scale(0.22).move_to(gg_small[1])
            self.play(FadeIn(right), FadeIn(no_r), Create(cross), run_time=1.0)
            self.play(FadeOut(VGroup(gg_small[1], gg_small[2], cross), scale=0.3), run_time=0.6)
            self.at("mirror-image")
            t0 = 24.0
            pl = Dot(big.p2c(0.2, t0), radius=0.12, color=BAD).set_z_index(5)
            pr = Dot(big.p2c(0.8, t0), radius=0.12, color=BAD).set_z_index(5)
            lab_l = M(r"\rho", size=40, color=BAD).next_to(pl, LEFT, buff=0.15)
            lab_r = M(r"1-\bar\rho", size=40, color=BAD).next_to(pr, RIGHT, buff=0.15)
            arc = DashedVMobject(ArcBetweenPoints(pl.get_center(), pr.get_center(), angle=-PI / 2.2), num_dashes=16).set_stroke(LIFT, 3)
            self.play(FadeIn(pl, scale=2), FadeIn(lab_l), run_time=0.5)
            self.play(Create(arc), TransformFromCopy(pl, pr), FadeIn(lab_r), run_time=1.1)
            self.play(Flash(pr, color=BAD, flash_radius=0.35), run_time=0.6)
            self.at("none on the left")
            self.play(FadeOut(VGroup(pl, pr, lab_l, lab_r, arc), scale=0.3), FadeIn(left), FadeIn(no_l), run_time=1.0)
            self.at("trapped")
            glow = big.line.copy().set_stroke(ZERO, 14, opacity=0.35)
            zs = gg_small[0].zeros
            self.play(FadeIn(glow), gg_small[0].line.animate.set_stroke(width=6),
                      *[z.animate(rate_func=there_and_back).scale(1.8) for z in zs], run_time=1.4)
            self.play(glow.animate.set_stroke(opacity=0.15), run_time=min(1.2, self.left() - 0.1))
            self.play(glow.animate.set_stroke(opacity=0.4), run_time=max(0.1, min(1.2, self.left() - 0.1)))
        self.finish()
