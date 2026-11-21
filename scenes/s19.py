import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *


def vessel():
    """The pooled lattice as a tank with holes along its floor."""
    w, h = 5.0, 3.4
    body = RoundedRectangle(width=w, height=h, corner_radius=0.35, stroke_color=INK, stroke_width=4,
                            fill_color=LIFT, fill_opacity=0.12)
    dots = VGroup(*[Dot([x, y, 0], radius=0.045, color=LIFT) for x in np.linspace(-2.1, 2.1, 10) for y in np.linspace(-1.2, 1.2, 6)])
    hx = [-1.9, -1.1, -0.35, 0.4, 1.15, 1.95]
    holes = VGroup(*[Dot([x, -h / 2, 0], radius=0.09, color=BAD).set_z_index(4) for x in hx])
    g = VGroup(body, dots, holes)
    g.body, g.dots, g.holes = body, dots, holes
    return g


def twist_icon(r=0.36):
    a = Arc(radius=r, start_angle=PI / 2, angle=1.6 * PI, stroke_color=LIFT, stroke_width=4)
    a.add_tip(tip_length=0.14, tip_width=0.14)
    return a


def spiral_piece(c, k, n=8, r0=1.2, rise=0.5, band=0.7, gap=0.03):
    t0, t1 = k / n, (k + 1) / n
    ths = np.linspace(t0 * TAU + gap, t1 * TAU - gap, 24)
    rr = lambda th: r0 + rise * th / TAU
    inner = [c + rr(th) * np.array([np.cos(th), np.sin(th), 0]) for th in ths]
    outer = [c + (rr(th) + band) * np.array([np.cos(th), np.sin(th), 0]) for th in ths[::-1]]
    return Polygon(*inner, *outer, stroke_color=INK, stroke_width=2.5, fill_color=LIFT, fill_opacity=0.35)


def root_level(center, n, w=4.6, h=1.05, color=INK, r=0.075):
    ell = Ellipse(width=w, height=h, stroke_color=MUTED, stroke_width=2.5).move_to(center)
    pts = VGroup(*[Dot(center + np.array([w / 2 * np.cos(TAU * k / n + PI / 2 * 0), h / 2 * np.sin(TAU * k / n), 0]), radius=r, color=color)
                   for k in range(n)])
    g = VGroup(ell, pts); g.ell, g.pts = ell, pts
    return g


class S19(NarratedScene):
    sid = "s19"

    def construct(self):
        clock = ValueTracker(0)
        clock.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(clock)

        V = vessel().move_to([-3.35, 0.55, 0])
        vlab = T("the pooled lattice", size=28, color=MUTED).next_to(V, UP, buff=0.3)
        leak = [ValueTracker(0) for _ in V.holes]
        NDROP, FALL = 3, 1.9

        def drops():
            g = VGroup()
            t = clock.get_value()
            for i, hole in enumerate(V.holes):
                lv = leak[i].get_value()
                if lv <= 0.01:
                    continue
                for k in range(NDROP):
                    ph = ((t * 0.9 + k / NDROP + i * 0.37) % 1.0)
                    p = hole.get_center() + DOWN * (0.12 + FALL * ph ** 1.6)
                    g.add(Dot(p, radius=0.08 * (1 - 0.4 * ph), color=LIFT, fill_opacity=lv * (1 - ph)))
            return g
        drip = always_redraw(drops)

        # ---------------------------------------------------------------- a: leaks; local vs global
        with self.beat("a") as d:
            self.add(drip)
            self.play(DrawBorderThenFill(V.body), FadeIn(V.dots, lag_ratio=0.02), FadeIn(vlab), run_time=1.2)
            self.play(*[FadeIn(h, scale=2) for h in V.holes], *[l.animate.set_value(1) for l in leak], run_time=0.8)
            C = np.array([3.45, 0.3, 0])
            pieces = VGroup(*[spiral_piece(C, k) for k in range(8)])
            self.at("hidden obstructions")
            self.play(LaggedStart(*[Indicate(h, color=BAD, scale_factor=1.8) for h in V.holes], lag_ratio=0.12), run_time=1.0)
            t_avail = self.cue("fails globally") - (self.now() - self._beat_start) - 1.6
            rt = max(1.5, min(3.4, t_avail))
            seam_flashes = []
            self.play(LaggedStart(*[FadeIn(p, shift=(p.get_center() - C) * 0.25) for p in pieces], lag_ratio=0.35), run_time=rt)
            loc = T("fits neighbour to neighbour", size=28, color=GOOD).move_to([3.45, -2.85, 0])
            # seam ticks between consecutive pieces
            r_at = lambda th: 1.2 + 0.5 * th / TAU
            ticks = VGroup(*[Line(C + r_at(k / 8 * TAU) * np.array([np.cos(k / 8 * TAU), np.sin(k / 8 * TAU), 0]),
                                  C + (r_at(k / 8 * TAU) + 0.7) * np.array([np.cos(k / 8 * TAU), np.sin(k / 8 * TAU), 0])).set_stroke(GOOD, 4)
                             for k in range(1, 8)])
            self.play(LaggedStart(*[ShowPassingFlash(t.copy(), time_width=1.0) for t in ticks], lag_ratio=0.15), FadeIn(ticks),
                      FadeIn(loc), run_time=min(1.2, max(0.6, self.left() - 2.2)))
            # the global seam: start (radius 1.05) vs end (radius 1.45)
            seam_in = C + RIGHT * 1.2
            seam_out = C + RIGHT * (1.7 + 0.7)
            seam = Line(seam_in, seam_out).set_stroke(BAD, 5)
            glob = T("but the ring doesn't close", size=28, color=BAD).move_to([3.45, 3.2, 0])
            self.play(Create(seam), FadeIn(glob), pieces[0].animate.set_stroke(BAD), pieces[7].animate.set_stroke(BAD),
                      run_time=min(0.8, max(0.3, self.left() - 0.6)))
            if self.left() > 0.5:
                self.play(Wiggle(VGroup(pieces[0], pieces[7], seam), scale_value=1.05), run_time=min(1.0, self.left() - 0.1))

        # ---------------------------------------------------------------- b: twists, weak Vandiver plug
        with self.beat("b") as d:
            self.play(FadeOut(VGroup(pieces, ticks, seam, loc, glob)), FadeOut(vlab),
                      V.animate.scale(1.3).move_to([0, 0.7, 0]), run_time=0.9)
            twistable = [0, 1, 2, 5]
            stubborn = [3, 4]
            self.at("killed by twisting")
            icons = [twist_icon().move_to(V.holes[i].get_center() + DOWN * 0.7) for i in twistable]
            tl = T("twist", size=32, color=LIFT).next_to(icons[0], DOWN, buff=0.15)
            self.play(FadeIn(tl), run_time=0.4)
            for ic, i in zip(icons, twistable):
                self.play(FadeIn(ic, scale=0.5), tl.animate.next_to(ic, DOWN, buff=0.15), run_time=0.15)
                self.play(Rotate(ic, angle=-TAU, about_point=ic.get_center()), leak[i].animate.set_value(0),
                          V.holes[i].animate.set_color(LIFT).scale(0.5), run_time=0.55)
                self.play(FadeOut(ic, scale=0.5), run_time=0.15)
            self.play(FadeOut(tl), run_time=0.3)
            st = T("stubborn", size=32, color=BAD).move_to([0, -2.3, 0]).shift(RIGHT * ((V.holes[3].get_x() + V.holes[4].get_x()) / 2))
            self.play(*[Indicate(V.holes[i], color=BAD, scale_factor=2) for i in stubborn], FadeIn(st, shift=UP * 0.1), run_time=0.9)
            self.at("Not the full conjecture")
            hx = (V.holes[3].get_x() + V.holes[4].get_x()) / 2
            plug = RoundedRectangle(width=1.8, height=0.4, corner_radius=0.15, stroke_color=GOOD, stroke_width=3,
                                    fill_color=GOOD, fill_opacity=0.85).move_to([hx, V.holes[3].get_y() - 1.9, 0])
            plab = T("weak Vandiver", size=34, color=GOOD).next_to(plug, DOWN, buff=0.25)
            self.play(FadeOut(st), FadeIn(plug, shift=UP * 0.4), FadeIn(plab, shift=UP * 0.4), run_time=0.7)
            self.play(VGroup(plug, plab).animate.shift(UP * (1.9 - 0.08)), *[leak[i].animate.set_value(0) for i in stubborn],
                      run_time=1.0, rate_func=rush_into)
            self.play(V.body.animate.set_stroke(GOOD), Flash(plug.get_center(), color=GOOD, flash_radius=1.1, line_length=0.3), run_time=0.8)
            self.play(V.body.animate.set_stroke(INK), run_time=0.6)
            # gentle sloshing of the lattice dots until the beat ends
            if self.left() > 0.4:
                self.play(Wiggle(V.dots, scale_value=1.02, rotation_angle=0.01 * TAU, n_wiggles=2), run_time=self.left() - 0.1)

        # ---------------------------------------------------------------- c: cyclotomic tower; Langlands
        with self.beat("c") as d:
            self.remove(drip)
            self.play(FadeOut(VGroup(V, plug, plab), shift=DOWN * 0.5), run_time=0.5)
            ys = [-2.55, -0.85, 0.85]
            ns = [3, 9, 27]
            levels = [root_level(np.array([0, y, 0]), n) for y, n in zip(ys, ns)]
            for lvl, col in zip(levels, (INK, INK, INK)):
                pass
            nlabs = [M(tex, size=48, color=WARM).next_to(lvl.ell, RIGHT, buff=0.35) for tex, lvl in zip(("3", "9", "27"), levels)]
            ttl = T("finer and finer\nroots of 1", size=36, color=INK, line_spacing=0.9).move_to([-4.5, 0.0, 0])
            self.play(Create(levels[0].ell), LaggedStart(*[FadeIn(q, scale=3) for q in levels[0].pts], lag_ratio=0.3), FadeIn(nlabs[0]), FadeIn(ttl), run_time=1.0)
            supports = VGroup()
            for k in range(2):
                lo, hi = levels[k], levels[k + 1]
                vl = VGroup(*[DashedLine(p.get_center(), p.get_center() + UP * (ys[k + 1] - ys[k]), dash_length=0.06).set_stroke(DIM, 2)
                              for p in lo.pts])
                supports.add(vl)
                ghost = lo.copy()
                self.play(ghost.animate.move_to(hi), Create(vl), run_time=0.7)
                old = set(range(0, ns[k + 1], 3))
                new_pts = VGroup(*[hi.pts[j] for j in range(ns[k + 1]) if j not in old])
                new_pts.set_color(WARM)
                self.remove(ghost)
                self.add(hi.ell, *[hi.pts[j] for j in old])
                self.play(LaggedStart(*[FadeIn(q, scale=3) for q in new_pts], lag_ratio=0.06), FadeIn(nlabs[k + 1]), run_time=0.9)
                self.play(new_pts.animate.set_color(INK), run_time=0.3)
            faint = VGroup(*[Ellipse(width=4.6, height=1.05, stroke_color=MUTED, stroke_width=2, stroke_opacity=o).move_to([0, y, 0])
                             for y, o in ((2.2, 0.45),)])
            vd = M(r"\vdots", size=44, color=MUTED).move_to([0, 2.95, 0])
            self.play(FadeIn(faint, shift=UP * 0.2), FadeIn(vd, shift=UP * 0.2), run_time=0.6)
            tower = VGroup(*levels, *nlabs, supports, faint, vd)

            self.at("the deepest dictionary")
            right_icon_target = tower.copy().scale(0.5).move_to([4.0, 0.75, 0])
            lt = lift_tower(floors=5, width=1.6, gap=0.5, grow=0.12, labels=False).move_to([-4.0, 0.75, 0])
            hL = T("automorphic forms", size=36, color=LIFT).move_to([-4.0, -1.55, 0])
            sL = T("symmetric functions", size=26, color=MUTED).next_to(hL, DOWN, buff=0.2)
            hR = T("Galois representations", size=36, color=WARM).move_to([4.0, -1.55, 0])
            sR = T("symmetries of numbers", size=26, color=MUTED).next_to(hR, DOWN, buff=0.2)
            self.play(FadeOut(ttl), tower.animate.scale(0.42).move_to([4.0, 0.75, 0]),
                      LaggedStart(*[GrowFromCenter(f) for f in lt.floors], *[GrowArrow(a) for a in lt.arrows], lag_ratio=0.1),
                      FadeIn(hL, shift=UP * 0.2), FadeIn(sL, shift=UP * 0.2), run_time=1.3)
            self.play(FadeIn(hR, shift=UP * 0.2), FadeIn(sR, shift=UP * 0.2), run_time=0.7)
            self.at("Langlands")
            arc = ArcBetweenPoints(LEFT * 1.9 + UP * 0.3, RIGHT * 1.9 + UP * 0.3, angle=-PI / 2.2).set_stroke(INK, 4)
            pillars = VGroup(Line(LEFT * 1.9 + UP * 0.3, LEFT * 1.9 + DOWN * 0.55), Line(RIGHT * 1.9 + UP * 0.3, RIGHT * 1.9 + DOWN * 0.55)).set_stroke(MUTED, 4)
            deck = Line(LEFT * 2.1 + UP * 0.3, RIGHT * 2.1 + UP * 0.3).set_stroke(INK, 4)
            hangers = VGroup(*[Line(arc.point_from_proportion(a), [arc.point_from_proportion(a)[0], 0.3, 0]).set_stroke(MUTED, 2)
                               for a in np.linspace(0.15, 0.85, 7)])
            lang = T("Langlands", size=44, color=INK, weight=MEDIUM).next_to(arc, UP, buff=0.25)
            swap = VGroup(Arrow(LEFT * 0.7, RIGHT * 0.7, buff=0, stroke_width=4, color=WARM, tip_length=0.2).shift(DOWN * 0.15),
                          Arrow(RIGHT * 0.7, LEFT * 0.7, buff=0, stroke_width=4, color=LIFT, tip_length=0.2).shift(DOWN * 0.5))
            self.play(Create(arc), Create(deck), FadeIn(pillars), Create(hangers), Write(lang), FadeIn(swap), run_time=1.2)
            # tokens crossing both ways along the deck until the beat ends
            while self.left() > 1.4:
                a1 = Dot(LEFT * 2.0 + UP * 0.48, radius=0.09, color=LIFT)
                a2 = Dot(RIGHT * 2.0 + UP * 0.48, radius=0.09, color=WARM)
                self.play(a1.animate.move_to(RIGHT * 2.0 + UP * 0.48).set_color(WARM),
                          a2.animate.move_to(LEFT * 2.0 + UP * 0.48).set_color(LIFT), run_time=1.2, rate_func=smooth)
                self.remove(a1, a2)
            dict_grp = VGroup(lt, hL, sL, hR, sR, tower, arc, pillars, deck, hangers, lang, swap)

        # ---------------------------------------------------------------- d: constellation
        with self.beat("d") as d:
            names = ["theta lifts", "unitary groups", "trace formula", "Arakelov geometry", "Iwasawa theory",
                     "Galois representations", "CM theory", "étale cohomology", "Shimura varieties"]
            POS = [(0, 2.95), (3.4, 2.25), (4.75, 0.65), (4.35, -1.35), (2.5, -2.9), (-2.1, -2.9), (-4.6, -1.35), (-4.55, 0.65), (-3.35, 2.25)]
            hub = VGroup(Circle(radius=0.62, stroke_color=GOOD, stroke_width=4, fill_color=BG, fill_opacity=1),
                         T("GRH", size=36, color=GOOD, weight=BOLD)).set_z_index(3)
            nodes, links = VGroup(), VGroup()
            for nm, (x, y) in zip(names, POS):
                pos = np.array([x, y, 0])
                lab = T(nm, size=28, color=INK).move_to(pos)
                nodes.add(lab)
                v = pos
                sc = min((lab.width / 2 + 0.15) / max(abs(v[0]), 1e-6), (lab.height / 2 + 0.15) / max(abs(v[1]), 1e-6))
                end = pos - v * sc
                links.add(Line(v / np.linalg.norm(v) * 0.66, end).set_stroke(LIFT, 2.5))
            self.play(FadeOut(dict_grp), run_time=0.4)
            self.play(GrowFromCenter(hub), run_time=0.4)
            per = (min(d - 1.2, 4.4)) / 9
            for k in range(9):
                self.play(FadeIn(nodes[k], scale=0.7), Create(links[k]), run_time=per)
            self.play(hub[0].animate.set_fill(GOOD, opacity=0.25), Flash(hub, color=GOOD, flash_radius=0.9), run_time=min(0.6, self.left() - 0.05))
        self.finish()
