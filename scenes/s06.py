import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *
import mpmath

SC = WARM  # the input s

# ---------------------------------------------------------------- shared layout (also used by s07)
U = 2.4                              # output plane: screen units per 1
ORIG = np.array([-0.2, 0.1, 0.0])    # output plane origin on screen
NT = 150                             # terms drawn in the spiral
NA = 10                              # first NA terms drawn as real arrows, the rest as a thin trail
S_START = complex(1.2, 3.0)          # where the spiral is first built (plain series converges here)
S_MID = complex(0.5, 13.5)           # where s06 ends
S_ZERO = complex(0.5, 14.134725141734694)


ZOOM_U, ZOOM_O = 5.6, np.array([-1.6, 0.75, 0.0])   # close-up view used while the spiral is first built
B_U, B_O = 3.2, np.array([2.1, 0.0, 0.0])          # roomy view for the single arrow in s06b
# VIEW["t"]: a ValueTracker in 0..1 blending view "a" -> view "b"; None means the default (end-of-s06 / s07) view
VIEW = dict(t=None, a=(U, ORIG), b=(ZOOM_U, ZOOM_O))


def view():
    if VIEW["t"] is None:
        return U, ORIG
    v = min(1.0, max(0.0, VIEW["t"].get_value()))
    (ua, oa), (ub, ob) = VIEW["a"], VIEW["b"]
    return ua + (ub - ua) * v, oa + (ob - oa) * v


def origin():
    return view()[1].copy()


def out_pt(z):
    u, o = view()
    return o + u * np.array([z.real, z.imag, 0.0])


def s_path(tau):
    """tau in [0,1]: S_START -> S_MID (end of s06); tau in [1,2]: up the line to the first zero (s07)."""
    if tau <= 1:
        return S_START + (S_MID - S_START) * tau
    return S_MID + (S_ZERO - S_MID) * (tau - 1)


def make_panel():
    """The small s-plane on the left."""
    ax = Axes(x_range=[-0.5, 2.0, 0.5], y_range=[-1, 15, 1], x_length=3.4, y_length=6.2,
              axis_config=dict(color=MUTED, stroke_width=2, include_ticks=False),
              tips=False).move_to([-4.65, -0.35, 0])
    grid = VGroup()
    for x in np.arange(-0.5, 2.01, 0.5):
        grid.add(Line(ax.c2p(x, -1), ax.c2p(x, 15)))
    for y in range(0, 16, 5):
        grid.add(Line(ax.c2p(-0.5, y), ax.c2p(2.0, y)))
    grid.set_stroke(DIM, 1.5)
    nums = VGroup(*[M(lab, size=26, color=MUTED).next_to(ax.c2p(x, 0), DOWN, buff=0.12).shift(RIGHT * 0.12)
                    for x, lab in [(1, "1"), (2, "2")]],
                  *[M(str(y), size=26, color=MUTED).next_to(ax.c2p(0, y), LEFT, buff=0.1).shift(UP * 0.0)
                    for y in (5, 10)])
    frame = SurroundingRectangle(VGroup(ax, grid), buff=0.0, stroke_width=0)
    g = VGroup(grid, ax, nums)
    g.ax = ax
    return g


def make_out_axes():
    O = origin()
    h = Line([-2.2, O[1], 0], [6.6, O[1], 0], stroke_width=2, color=MUTED)
    v = Line([O[0], -3.55, 0], [O[0], 3.55, 0], stroke_width=2, color=MUTED)
    one = VGroup(Line(out_pt(1) + DOWN * 0.08, out_pt(1) + UP * 0.08, stroke_width=2, color=MUTED),
                 M("1", size=26, color=MUTED).next_to(out_pt(1), DOWN, buff=0.12).shift(RIGHT * 0.12))
    zero = M("0", size=26, color=MUTED).next_to(O, DL, buff=0.08)
    g = VGroup(h, v, one, zero)
    g.zero = zero
    return g


def terms(s, alt=0.0, n=NT):
    k = np.arange(1, n + 1)
    sign = np.where(k % 2 == 0, 1.0 - 2.0 * alt, 1.0)
    return sign * np.exp(-s * np.log(k))


@functools.lru_cache(maxsize=4096)
def _limit(sr, si, alt):
    s = mpmath.mpc(sr, si)
    if alt >= 1.0:
        return complex(mpmath.altzeta(s))
    return complex(mpmath.zeta(s) * (1 - 2 * alt * mpmath.power(2, -s)))


def limit(s, alt=0.0):
    """Where the (possibly sign-twisted) series really ends up: zeta(s)*(1-2*alt*2^-s); alt=1 is eta(s)."""
    return _limit(round(s.real, 6), round(s.imag, 6), round(alt, 4))


def seg(a, b, width, color=INK, opacity=1.0):
    L = np.linalg.norm(b - a)
    if L < 0.14:
        return Line(a, b + 1e-4 * RIGHT, stroke_width=width, color=color, stroke_opacity=opacity)
    tl = min(0.22, 0.38 * L)
    return Arrow(a, b, buff=0, stroke_width=width, color=color, tip_length=tl,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=20).set_opacity(opacity)


def build_spiral(s, alt=0.0, k=NT, show_end=True):
    """Arrows 1, ±1/2^s, 1/3^s, ... tip to tail; k (float) = how many are laid down so far."""
    tm = terms(s, alt)
    P = np.concatenate([[0], np.cumsum(tm)])
    g = VGroup()
    kk = int(np.floor(k))
    fr = k - kk
    trail = []
    for n in range(1, min(kk, NT) + 1):
        a, b = out_pt(P[n - 1]), out_pt(P[n])
        if n <= NA:
            w = 5.0 - 2.0 * (n - 1) / NA
            g.add(seg(a, b, w, INK, 1.0 - 0.35 * (n - 1) / NA))
        else:
            trail.append(b) if trail else trail.extend([a, b])
    if 0 < fr and kk < NT:
        n = kk + 1
        a = out_pt(P[n - 1]); b = out_pt(P[n - 1] + fr * tm[n - 1])
        if n <= NA:
            g.add(seg(a, b, 5.0 - 2.0 * (n - 1) / NA, INK, 1.0 - 0.35 * (n - 1) / NA))
        else:
            trail.append(b) if trail else trail.extend([a, b])
    if len(trail) >= 2:
        tr = VMobject().set_points_as_corners(trail).set_stroke(INK, 1.6, opacity=0.55 - 0.35 * alt)
        g.add(tr)
    if show_end and k >= NT:
        L = limit(s, alt)
        e = out_pt(L)
        # the tail still wiggles around the true end point: join it smoothly with the running averages
        # of consecutive partial sums (they settle much faster than the raw sums)
        A = P[NA:].copy()
        for _ in range(4):
            A = 0.5 * (A[1:] + A[:-1])
        g.add(VMobject().set_points_smoothly([out_pt(z) for z in A[::3]] + [e]).set_stroke(INK, 2.6, opacity=0.9))
    return g


def end_dot(s, alt=0.0, color=INK):
    e = out_pt(limit(s, alt))
    return VGroup(Dot(e, radius=0.16, color=color, fill_opacity=0.25), Dot(e, radius=0.08, color=color)).set_z_index(5)


def s_readout(get_s, color=SC):
    def mk():
        s = get_s()
        g = VGroup(M("s", "=", size=38, color=color),
                   DecimalNumber(s.real, num_decimal_places=2, font_size=38, color=color),
                   M("+", size=38, color=color),
                   DecimalNumber(s.imag, num_decimal_places=2, font_size=38, color=color),
                   M("i", size=38, color=color)).arrange(RIGHT, buff=0.12)
        g[-1].shift(LEFT * 0.04)
        return g.move_to([-4.65, 3.2, 0])
    return always_redraw(mk)


@functools.lru_cache(None)
def endpoint_trace_samples():
    taus = np.linspace(0, 2, 601)
    return taus, [limit(s_path(t), 1.0) for t in taus]


def endpoint_trace(tau):
    taus, Ls = endpoint_trace_samples()
    pts = [out_pt(L) for t, L in zip(taus, Ls) if t <= tau] + [out_pt(limit(s_path(tau), 1.0))]
    if len(pts) < 2:
        pts = pts + [pts[-1] + 1e-3 * RIGHT]
    return VMobject().set_points_smoothly(pts).set_stroke(SC, 2.0, opacity=0.35)


class S06(NarratedScene):
    sid = "s06"

    def construct(self):
        # ------------------------------------------------------------------ a: the line opens into a plane
        with self.beat("a") as d:
            line = NumberLine(x_range=[-6, 6, 1], length=12, color=MUTED, include_numbers=True, font_size=28,
                              stroke_width=2.5)
            line.numbers.set_color(MUTED)
            sdot = Dot(line.n2p(2), radius=0.11, color=SC).set_z_index(4)
            slab = M("s", size=44, color=SC).next_to(sdot, UP, buff=0.18)
            self.play(Create(line), run_time=0.8)
            self.play(FadeIn(sdot, scale=0.4), FadeIn(slab, shift=DOWN * 0.15), run_time=0.5)
            # slide s along the line (the old, real inputs)
            self.play(sdot.animate.move_to(line.n2p(3)), slab.animate.next_to(line.n2p(3), UP, buff=0.29), run_time=1.0)
            self.play(sdot.animate.move_to(line.n2p(1.5)), slab.animate.next_to(line.n2p(1.5), UP, buff=0.29), run_time=1.0)
            self.at("complex numbers", lead=0.1)
            plane = NumberPlane(x_range=[-7, 7, 1], y_range=[-4, 4, 1],
                                background_line_style=dict(stroke_color=DIM, stroke_width=1.5, stroke_opacity=1),
                                axis_config=dict(stroke_color=MUTED, stroke_width=2.5))
            plane.save_state()
            plane.stretch(0.01, 1)
            self.add(plane, sdot, slab)
            self.bring_to_back(plane)
            self.play(Restore(plane), FadeOut(line.ticks), line.numbers.animate.set_opacity(0.0), run_time=1.6, rate_func=smooth)
            self.remove(line)
            vax_num = VGroup(*[M(f"{y}i" if y != 1 else "i", size=26, color=MUTED).next_to(plane.c2p(0, y), LEFT, buff=0.12)
                               for y in (-2, -1, 1, 2, 3) if True])
            hax_num = VGroup(*[M(str(x), size=26, color=MUTED).next_to(plane.c2p(x, 0), DOWN, buff=0.12)
                               for x in (-4, -2, 2, 4)])
            self.play(FadeIn(vax_num), FadeIn(hax_num), run_time=0.6)

            self.at("point on a plane", lead=0.3)
            sx, sy = ValueTracker(1.5), ValueTracker(0.0)
            sdot.add_updater(lambda m: m.move_to(plane.c2p(sx.get_value(), sy.get_value())))
            slab.add_updater(lambda m: m.next_to(sdot, UR, buff=0.05))
            self.play(sy.animate.set_value(2.0), run_time=1.2)
            # projections onto the two axes
            vproj = always_redraw(lambda: DashedLine(sdot.get_center(), plane.c2p(sx.get_value(), 0), dash_length=0.1, stroke_width=3, color=SC))
            hproj = always_redraw(lambda: DashedLine(sdot.get_center(), plane.c2p(0, sy.get_value()), dash_length=0.1, stroke_width=3, color=INK))
            self.at("left-right part", lead=0.4)
            lr = VGroup(T("left-right part", size=30, color=SC), M(r"\mathrm{Re}(s)", size=28, color=MUTED)).arrange(DOWN, buff=0.1)
            lr.add_updater(lambda m: m.next_to(plane.c2p(sx.get_value(), 0), DOWN, buff=0.45))
            self.play(Create(vproj), FadeIn(lr), hax_num.animate.set_opacity(0.25), run_time=0.6)
            self.play(sx.animate.set_value(1.9), run_time=0.6)
            self.at("up-down part", lead=0.4)
            ud = VGroup(T("up-down part", size=30, color=INK), M(r"\mathrm{Im}(s)", size=28, color=MUTED)).arrange(DOWN, buff=0.1)
            ud.add_updater(lambda m: m.next_to(plane.c2p(0, sy.get_value()), LEFT, buff=0.35))
            self.play(Create(hproj), FadeIn(ud), vax_num.animate.set_opacity(0.0), run_time=0.6)
            self.play(sy.animate.set_value(2.6), run_time=max(0.1, min(1.0, self.left() - 0.1)))

        # ------------------------------------------------------------------ b: one arrow, 1/2^s
        with self.beat("b") as d:
            panel = make_panel()
            pax = panel.ax
            vt = ValueTracker(0.0); VIEW.update(t=vt, a=(B_U, B_O), b=(ZOOM_U, ZOOM_O))
            sig, tt = ValueTracker(sx.get_value()), ValueTracker(sy.get_value())
            S = lambda: complex(sig.get_value(), tt.get_value())
            pdot_target = Dot(pax.c2p(sig.get_value(), tt.get_value()), radius=0.11, color=SC)
            for m in (sdot, slab, lr, ud, vproj, hproj):
                m.clear_updaters()
            self.wait(0.8)
            self.play(FadeOut(plane, scale=0.3, target_position=pax.get_center()), FadeIn(panel, scale=2.5), FadeOut(VGroup(vax_num, hax_num, lr, ud, vproj, hproj)),
                      sdot.animate.move_to(pdot_target), FadeOut(slab), run_time=1.2)
            pdot = always_redraw(lambda: Dot(pax.c2p(sig.get_value(), tt.get_value()), radius=0.11, color=SC).set_z_index(4))
            pv = always_redraw(lambda: DashedLine(pax.c2p(sig.get_value(), tt.get_value()), pax.c2p(sig.get_value(), 0), dash_length=0.08, stroke_width=2.5, color=SC))
            ph = always_redraw(lambda: DashedLine(pax.c2p(sig.get_value(), tt.get_value()), pax.c2p(0, tt.get_value()), dash_length=0.08, stroke_width=2.5, color=INK))
            self.remove(sdot)
            self.add(pv, ph, pdot)
            rd = s_readout(S)
            oax = always_redraw(make_out_axes)
            ucirc = DashedVMobject(Circle(radius=B_U, color=DIM, stroke_width=2).move_to(origin()), num_dashes=60)
            arrow = always_redraw(lambda: seg(origin(), out_pt(2 ** (-S())), 5.0, INK))
            alab = always_redraw(lambda: tint_s(M(r"\frac{1}{2^s}", size=40)).next_to(out_pt(2 ** (-S())), normalize(out_pt(2 ** (-S())) - origin() + 1e-6 * RIGHT), buff=0.2))
            self.play(FadeIn(rd), Create(oax), Create(ucirc), run_time=0.8)
            self.at("Picture an arrow", lead=0.2)
            self.play(GrowArrow(seg(origin(), out_pt(2 ** (-S())), 5.0, INK)), run_time=0.6)
            self.remove(*[m for m in self.mobjects if isinstance(m, Arrow) and m is not arrow])
            self.add(arrow, alab)
            # left-right part -> length
            self.at("left-right part", lead=0.3)
            def _lenlab():
                t_ = T("length", size=30, color=SC)
                e_ = out_pt(2 ** (-S())); o_ = origin()
                pp = rotate_vector(normalize(e_ - o_ + 1e-6 * RIGHT), PI / 2)
                if pp[0] < 0:
                    pp = -pp
                off = 0.25 + 0.5 * t_.width * abs(pp[0]) + 0.5 * t_.height * abs(pp[1])
                return t_.move_to((o_ + e_) / 2 + off * pp)
            lenlab = always_redraw(_lenlab)
            hl = always_redraw(lambda: Line(origin(), out_pt(2 ** (-S())), stroke_width=10, color=SC, stroke_opacity=0.35))
            self.add(hl)
            self.play(FadeIn(lenlab), run_time=0.4)
            self.play(sig.animate.set_value(0.3), run_time=1.1)
            self.play(sig.animate.set_value(1.0), run_time=1.0)
            # up-down part -> angle
            self.at("up-down part", lead=0.3)
            self.play(FadeOut(lenlab), FadeOut(hl), run_time=0.3)

            def ang_arc():
                z = 2 ** (-S())
                a = float(np.angle(z))
                tot = -tt.get_value() * np.log(2)  # the true accumulated angle
                arc = Arc(radius=0.55, start_angle=0, angle=tot if abs(tot) > 1e-3 else 1e-3, arc_center=origin(), color=INK, stroke_width=3)
                return arc
            arc = always_redraw(ang_arc)
            anglab = T("angle", size=30, color=INK).next_to(origin(), DR, buff=0.45)
            self.play(Create(arc), FadeIn(anglab), run_time=0.5)
            self.play(tt.animate.set_value(8.0), run_time=min(2.4, self.left() - 1.1), rate_func=smooth)
            self.play(tt.animate.set_value(4.0), run_time=max(0.3, self.left() - 0.1))

        # ------------------------------------------------------------------ c: tip to tail -> a spiral
        with self.beat("c") as d:
            self.play(FadeOut(arc), FadeOut(anglab), FadeOut(alab), FadeOut(ucirc), vt.animate.set_value(1.0),
                      sig.animate.set_value(S_START.real), tt.animate.set_value(S_START.imag), run_time=1.0)
            self.remove(arrow)
            a2 = seg(origin(), out_pt(2 ** (-S_START)), 5.0 - 2.0 / NA, INK, 1.0 - 0.35 / NA)
            a1 = seg(origin(), out_pt(1), 5.0, INK)
            self.add(a2)
            l1 = M("1", size=40).next_to(out_pt(0.5), DOWN, buff=0.2)
            l2 = tint_s(M(r"\frac{1}{2^s}", size=40))
            l3 = tint_s(M(r"\frac{1}{3^s}", size=40))
            P = np.concatenate([[0], np.cumsum(terms(S_START))])
            self.play(GrowArrow(a1), FadeIn(l1), a2.animate.shift(out_pt(1) - origin()), run_time=0.9)
            l2.next_to(out_pt((P[1] + P[2]) / 2), RIGHT, buff=0.15)
            l3.next_to(out_pt((P[2] + P[3]) / 2), LEFT, buff=0.15).shift(UP * 0.1)
            kt = ValueTracker(2.0)
            spiral = always_redraw(lambda: build_spiral(S(), 0.0, kt.get_value(), show_end=False))
            self.remove(a1, a2)
            self.add(spiral)
            self.play(FadeIn(l2), run_time=0.4)
            self.at("laying them", lead=0.2)
            self.play(kt.animate.set_value(3.0), FadeIn(l3), run_time=0.8)
            self.play(kt.animate.set_value(8.0), run_time=1.4, rate_func=linear)
            self.at("traces out", lead=0.3)
            self.play(kt.animate.set_value(NT), run_time=2.0, rate_func=rate_functions.ease_in_quad)
            spiral.become(build_spiral(S(), 0.0, NT, True))
            spiral.clear_updaters()
            spiral.add_updater(lambda m: m.become(build_spiral(S(), alt.get_value(), NT, True)))
            alt = ValueTracker(0.0)
            ed = always_redraw(lambda: end_dot(S(), alt.get_value()))
            e0 = out_pt(limit(S_START))
            zl = VGroup(tint_s(M(r"\zeta(s)", size=48)).move_to(e0 + np.array([1.7, 1.55, 0])))
            zl.add(Line(e0 + np.array([0.15, 0.15, 0]), zl[0].get_corner(DL) + np.array([-0.05, -0.05, 0]), stroke_width=2, color=INK)).set_z_index(6)
            self.at("where the spiral", lead=0.2)
            self.play(FadeIn(ed, scale=0.3), FadeOut(VGroup(l1, l2, l3)), run_time=0.6)
            self.at("value of zeta", lead=0.3)
            self.play(FadeIn(zl[0], shift=DOWN * 0.15), Create(zl[1]), Flash(out_pt(limit(S_START)), color=INK, flash_radius=0.3), run_time=0.8)

        # ------------------------------------------------------------------ d: move s, the spiral reshapes
        with self.beat("d") as d:
            # alternate the signs (+ - + - ...): the same picture, but it settles even inside the strip
            self.play(alt.animate.set_value(1.0), FadeOut(zl), run_time=0.9)
            zl.clear_updaters()
            tau = ValueTracker(0.0)
            sig.add_updater(lambda m: m.set_value(s_path(tau.get_value()).real))
            tt.add_updater(lambda m: m.set_value(s_path(tau.get_value()).imag))
            self.add(sig, tt)
            trace = always_redraw(lambda: endpoint_trace(tau.get_value()))
            self.add(trace)
            self.bring_to_front(spiral, ed)
            VIEW.update(a=(U, ORIG))
            T_ = self.left() - 0.15
            self.play(AnimationGroup(tau.animate(run_time=T_, rate_func=rate_functions.ease_in_out_sine).set_value(1.0),
                                     vt.animate(run_time=min(2.2, T_), rate_func=linear).set_value(0.0)))
        self.finish()


def tint_s(m, color=SC):
    """Colour every 's' glyph in a small formula (heuristic: the last glyph of the tex)."""
    m[0][-1].set_color(color) if m.tex_string.strip().endswith("s}") or m.tex_string.strip().endswith("s") else None
    if m.tex_string == r"\zeta(s)":
        m[0][2].set_color(color)
    return m
