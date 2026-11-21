import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *


# ---------------------------------------------------------------- modular tessellation (PSL2(Z) acting on the disk)
def _half_domains(Y=3000.0, n=40):
    """Left / right halves of the standard fundamental domain, as dense boundary samples in the upper half-plane."""
    s3 = np.sqrt(3) / 2
    ys = np.geomspace(s3, Y, n)
    yi = np.geomspace(1.0, Y, n)
    th = np.linspace(np.pi / 2, 2 * np.pi / 3, n // 2)
    left = np.concatenate([-0.5 + 1j * ys, np.linspace(-0.5, 0, 6) + 1j * Y, 1j * yi[::-1], np.exp(1j * th)])
    right = -np.conj(left)
    return left, right


@functools.lru_cache(None)
def modular_tiles(min_size=0.012):
    """BFS over PSL2(Z) words; returns list of (disk points (complex, unit disk), parity 0/1). Pruned by Euclidean size."""
    L, R = _half_domains()
    gens = [np.array([[1, 1], [0, 1]]), np.array([[1, -1], [0, 1]]), np.array([[0, -1], [1, 0]])]

    def key(g):
        g = g if (g[1, 0] > 0 or (g[1, 0] == 0 and g[1, 1] > 0)) else -g
        return tuple(int(x) for x in g.ravel())

    def image(g, z):
        a, b, c, d = g.ravel()
        w = (a * z + b) / (c * z + d)
        return (w - 1j) / (w + 1j)

    seen = {key(np.eye(2, dtype=int)): np.eye(2, dtype=int)}
    frontier = [np.eye(2, dtype=int)]
    tiles = []
    while frontier:
        nxt = []
        for g in frontier:
            pl, pr = image(g, L), image(g, R)
            size = max(np.ptp(pl.real), np.ptp(pl.imag))
            if size < min_size:
                continue
            tiles.append((pl, 0)); tiles.append((pr, 1))
            for h in gens:
                gh = g @ h
                k = key(gh)
                if k not in seen:
                    seen[k] = gh; nxt.append(gh)
        frontier = nxt
    return tiles


def tessellation(radius=3.2, center=ORIGIN, colors=(LIFT, BG), opac=(0.75, 1.0), stroke=1.2, min_size=0.016):
    g = VGroup()
    for pts, par in modular_tiles(min_size):
        v = VMobject().set_points_as_corners([center + radius * np.array([p.real, p.imag, 0]) for p in pts] + [center + radius * np.array([pts[0].real, pts[0].imag, 0])])
        v.set_fill(colors[par], opacity=opac[par]).set_stroke(INK, stroke, opacity=0.45)
        v.parity = par
        g.add(v)
    rim = Circle(radius=radius, color=INK, stroke_width=3).move_to(center)
    out = VGroup(g, rim); out.tiles, out.rim = g, rim
    return out


class S15(NarratedScene):
    sid = "s15"

    def construct(self):
        # ------------------------------------------------------------ a: lattice, expanding circle, theta series
        with self.beat("a") as d:
            sp = 0.66
            O = LEFT * 3.8 + DOWN * 0.25
            N = 4
            pts = {(i, j): Dot(O + sp * (i * RIGHT + j * UP), radius=0.07, color=INK) for i in range(-N, N + 1) for j in range(-N, N + 1) if i * i + j * j <= 18}
            lat = VGroup(*pts.values())
            self.play(LaggedStart(*[FadeIn(p, scale=0.3) for p in sorted(pts.values(), key=lambda m: np.linalg.norm(m.get_center() - O))],
                                  lag_ratio=0.01, run_time=1.6))
            r = ValueTracker(0.001)
            circ = always_redraw(lambda: Circle(radius=max(0.001, r.get_value() * sp), color=LIFT, stroke_width=3).move_to(O))
            self.add(circ)
            pts[(0, 0)].set_color(LIFT)
            # series layout on the right
            terms = [(0, 1), (1, 4), (2, 4), (4, 4), (5, 8), (8, 4), (9, 4), (10, 8)]
            def term_tex(n, c, first):
                if n == 0: return "1"
                q = "q" if n == 1 else f"q^{{{n}}}"
                return f"+\\,{c}{q}"
            head = M(r"\theta(q) =", size=46, color=LIFT)
            row1 = [M(term_tex(n, c, i == 0), size=46) for i, (n, c) in enumerate(terms[:5])]
            row2 = [M(term_tex(n, c, False), size=46) for (n, c) in terms[5:]] + [M(r"+\,\cdots", size=46)]
            line1 = VGroup(head, *row1).arrange(RIGHT, buff=0.18)
            line2 = VGroup(*row2).arrange(RIGHT, buff=0.18)
            line2.next_to(line1, DOWN, buff=0.45).align_to(row1[0], LEFT)
            series = VGroup(line1, line2)
            series.shift(RIGHT * (-0.2 - series.get_left()[0]) + UP * (0.2 - series.get_y()))
            line2.align_to(row1[0], LEFT)
            all_terms = row1 + row2[:3]
            spin = self.cue("A theta function") - (self.now() - self._beat_start) - 0.4
            if spin > 0.5:  # the grid turned a quarter turn lands on itself
                self.play(Rotate(lat, PI / 2, about_point=O), run_time=spin)
            self.at("A theta function")
            self.play(Write(head), run_time=0.8)
            self.at("fingerprint")
            t_left = self.left() - 1.0
            seg = t_left / len(terms)
            cur = 0.0
            for (n, c), tm in zip(terms, all_terms):
                hits = VGroup(*[p for (i, j), p in pts.items() if i * i + j * j == n])
                target = np.sqrt(n)
                if n > 0:
                    self.play(r.animate.set_value(target), run_time=seg * 0.45, rate_func=linear if cur > 0 else smooth)
                cur = target
                cnt = M(rf"\text{{distance}}^2 = {n}:\ \ {c}\text{{ points}}" if c > 1 else rf"\text{{distance}}^2 = 0:\ \ 1\text{{ point}}", size=40, color=LIFT).move_to(O + UP * 3.3)
                self.play(hits.animate.set_color(LIFT).scale(1.5), FadeIn(cnt, run_time=seg * 0.3), FadeIn(tm, shift=LEFT * 0.2), run_time=seg * 0.5)
                self.play(hits.animate.scale(1 / 1.5), FadeOut(cnt), run_time=seg * 0.05 + 0.001)
            self.play(FadeIn(row2[3]), r.animate.set_value(np.sqrt(10) + 0.25), run_time=0.5)

        # ------------------------------------------------------------ b: automorphic form — the modular tessellation
        with self.beat("b") as d:
            tess = tessellation(radius=3.3, center=RIGHT * 2.95 + DOWN * 0.05)
            self.play(FadeOut(lat), FadeOut(circ), series.animate.scale(0.62).to_corner(UL, buff=0.5), run_time=0.9)
            self.play(Create(tess.rim), LaggedStart(*[FadeIn(t) for t in sorted(tess.tiles, key=lambda m: -m.width)], lag_ratio=0.002), run_time=2.2)
            # a single tile and its images under the symmetries
            big = sorted([t for t in tess.tiles if t.parity == 0], key=lambda m: -m.width)
            hero = big[0]
            self.at("hidden symmetries")
            self.play(hero.animate.set_fill(PRIME, 0.95), run_time=0.5)
            others = big[1:40]
            self.play(LaggedStart(*[Succession(t.animate(run_time=0.3).set_fill(PRIME, 0.9), t.animate(run_time=0.5).set_fill(LIFT, 0.75)) for t in others],
                                  lag_ratio=0.08), run_time=2.6)
            self.at("automorphic forms")
            lab = T("automorphic form", size=44, color=LIFT, weight=MEDIUM).move_to(LEFT * 3.6 + DOWN * 1.2)
            self.play(Write(lab), run_time=1.0)
            # the disk turned half a turn lands exactly on itself (z -> -1/z)
            rest = self.left() - 0.1
            self.play(Rotate(tess, PI, about_point=tess.rim.get_center()), run_time=max(0.5, rest), rate_func=smooth)

        # ------------------------------------------------------------ c: the theta machine
        with self.beat("c") as d:
            box = RoundedRectangle(width=2.4, height=2.4, corner_radius=0.25, stroke_color=LIFT, stroke_width=4, fill_color=BG, fill_opacity=1)
            box.move_to(RIGHT * 0.1 + DOWN * 0.2)
            th = M(r"\theta", size=110, color=LIFT).move_to(box)
            machine = VGroup(box, th)
            # small symmetric object: a little square-lattice disc (4-fold symmetric)
            sc, sr = LEFT * 4.8 + DOWN * 0.2, 0.95
            small_disc = Circle(radius=sr, color=INK, stroke_width=3).move_to(sc)
            small_pts = VGroup(*[Dot(sc + 0.3 * (i * RIGHT + j * UP), radius=0.05, color=LIFT) for i in range(-3, 4) for j in range(-3, 4) if i * i + j * j <= 9])
            small = VGroup(small_disc, small_pts)
            a1 = Arrow(small.get_right(), box.get_left(), buff=0.2, stroke_width=4, color=MUTED)
            self.play(FadeOut(lab), FadeOut(series), tess.animate.scale(1.8 / 3.3).move_to(RIGHT * 4.45 + DOWN * 0.2).set_opacity(0.0),
                      FadeIn(machine, scale=0.8), run_time=0.9)
            self.remove(tess)
            tess2 = tessellation(radius=1.85, center=RIGHT * 4.45 + DOWN * 0.2, stroke=1.0, min_size=0.02)
            a2 = Arrow(box.get_right(), tess2.get_left(), buff=0.2, stroke_width=4, color=MUTED)
            self.play(FadeIn(small, shift=RIGHT * 0.4), run_time=0.7)
            self.at("Feed in")
            self.play(GrowArrow(a1), run_time=0.6)
            spin = self.cue("the machine returns") - (self.now() - self._beat_start) - 0.3
            if spin > 0.3:
                self.play(Rotate(small, PI / 2, about_point=sc), run_time=spin)
            self.at("the machine returns")
            ghost = small.copy()
            self.play(ghost.animate.scale(0.4).move_to(box).set_opacity(0), box.animate.set_fill(LIFT, 0.25), run_time=0.8)
            self.play(GrowArrow(a2), FadeIn(tess2, scale=0.3, shift=LEFT * 1.5), box.animate.set_fill(BG, 1), run_time=1.2)
            self.remove(ghost)
            sl = T("small space", size=28, color=MUTED).next_to(small, DOWN, buff=0.35)
            bl = T("bigger space", size=28, color=MUTED).next_to(tess2, DOWN, buff=0.2)
            self.play(FadeIn(sl), FadeIn(bl), run_time=0.6)
            self.at("theta lift")
            tl = T("theta lift", size=44, color=LIFT, weight=MEDIUM).next_to(box, UP, buff=0.45)
            self.play(Write(tl), run_time=0.8)
            rest = self.left() - 0.05
            if rest > 0.3:
                self.play(Rotate(tess2, PI, about_point=tess2.rim.get_center()), Rotate(small, PI / 2, about_point=sc), run_time=rest)
        self.finish()
