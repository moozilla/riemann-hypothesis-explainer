import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *

X1, X2 = -5.2, 5.2          # x of exponent 1 and exponent 1/2
LINE_Y = 0.2


def ex2x(e):
    return X1 + (1 - e) / 0.5 * (X2 - X1)


def brick_wall(x, y0, rows=7, bw=0.46, bh=0.24):
    bricks = VGroup()
    for r in range(rows):
        off = 0 if r % 2 == 0 else bw / 2
        for c in range(-1, 2):
            cx = x + c * bw + off - bw / 4
            if abs(cx - x) > bw * 0.9:
                continue
            b = Rectangle(width=bw * 0.94, height=bh * 0.88, stroke_color=BAD, stroke_width=2,
                          fill_color=BAD, fill_opacity=0.35).move_to([cx, y0 + bh / 2 + r * bh, 0])
            bricks.add(b)
    return bricks


def coin():
    c = Ellipse(width=0.62, height=0.2, stroke_color="#c77700", stroke_width=2, fill_color=WARM, fill_opacity=1)
    return c


# three nearly perpendicular integer vectors: the matrix columns
VECS = [np.array([3, 1, 0]), np.array([-1, 3, 1]), np.array([0, -1, 3])]


class S18(NarratedScene):
    sid = "s18"

    def construct(self):
        # ---------------- exponent line
        base = Line([X1 - 0.3, LINE_Y, 0], [X2 + 0.3, LINE_Y, 0]).set_stroke(MUTED, 3)
        ticks = VGroup(*[Line(UP * 0.14, DOWN * 0.14).set_stroke(MUTED, 3).move_to([ex2x(e), LINE_Y, 0]) for e in (1, 5 / 6, 2 / 3, 1 / 2)])
        nums = VGroup(M("1", size=44, color=MUTED), M(r"5/6", size=36, color=DIM), M(r"2/3", size=44, color=BAD), M(r"1/2", size=44, color=GOOD))
        for n, e in zip(nums, (1, 5 / 6, 2 / 3, 1 / 2)):
            n.next_to([ex2x(e), LINE_Y, 0], DOWN, buff=0.3)
        trivial = T("trivial", size=26, color=MUTED).next_to(nums[0], DOWN, buff=0.15)
        goal = T("goal", size=26, color=GOOD).next_to(nums[3], DOWN, buff=0.15)
        head = T("size of the error:  X to the power", size=26, color=MUTED).move_to([0, 2.6, 0])
        pole = Line([X2, LINE_Y, 0], [X2, LINE_Y + 1.5, 0]).set_stroke(INK, 3)
        flag = Polygon([X2, LINE_Y + 1.5, 0], [X2 + 0.62, LINE_Y + 1.27, 0], [X2, LINE_Y + 1.04, 0],
                       stroke_width=0, fill_color=GOOD, fill_opacity=1)
        flagg = VGroup(pole, flag)
        wall = brick_wall(ex2x(2 / 3), LINE_Y - 0.1, rows=6)
        marker = Dot([ex2x(1), LINE_Y, 0], radius=0.16, color=WARM).set_z_index(5)
        mlab = M("X^{1}", size=50, color=WARM).next_to(marker, UP, buff=0.3).shift(LEFT * 0.45)
        exline = VGroup(base, ticks, nums, trivial, goal, flagg, wall, marker, mlab, head)

        with self.beat("a") as d:
            self.play(Create(base), FadeIn(ticks), run_time=0.9)
            self.play(FadeIn(nums[0]), FadeIn(trivial), FadeIn(nums[3]), FadeIn(goal), FadeIn(nums[1]),
                      GrowFromPoint(marker, marker.get_center()), FadeIn(mlab, shift=DOWN * 0.2), FadeIn(head), run_time=0.8)
            self.play(Create(pole), GrowFromEdge(flag, LEFT), run_time=0.7)
            self.at("Do the accounting")
            stop = ex2x(2 / 3) - 0.62
            slide = self.cue("stalls") - (self.now() - self._beat_start)
            slide = max(1.6, slide)
            self.play(marker.animate.move_to([stop, LINE_Y, 0]),
                      MaintainPositionRelativeTo(mlab, marker),
                      LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in wall], lag_ratio=0.05, run_time=slide * 0.8),
                      FadeIn(nums[2], run_time=slide * 0.8),
                      run_time=slide, rate_func=rush_into)
            # bump
            self.play(marker.animate.shift(LEFT * 0.12), MaintainPositionRelativeTo(mlab, marker), wall.animate.shift(RIGHT * 0.04),
                      run_time=0.18, rate_func=there_and_back)
            self.at("two thirds. Close")
            m23 = M("X^{2/3}", size=50, color=BAD).next_to(marker, UP, buff=0.3).align_to(mlab, RIGHT)
            self.play(Transform(mlab, m23), Indicate(nums[2], color=BAD, scale_factor=1.3), run_time=0.7)
            self.at("But two thirds")
            cmp = M("X^{2/3}", r"\;\neq\;", "X^{1/2}", size=80).move_to(DOWN * 2.4)
            cmp[0].set_color(BAD); cmp[2].set_color(GOOD)
            self.play(TransformFromCopy(mlab, cmp[0]), FadeIn(cmp[1]), TransformFromCopy(nums[3], cmp[2]), run_time=1.0)
            self.at("worthless")
            self.play(Wiggle(flagg, scale_value=1.15, rotation_angle=0.04 * TAU), Indicate(cmp[2], color=GOOD), run_time=1.2)
            # marker keeps butting against the wall
            while self.left() > 1.0:
                self.play(marker.animate.shift(LEFT * 0.1), MaintainPositionRelativeTo(mlab, marker), run_time=0.45, rate_func=there_and_back)
                if self.left() > 0.8:
                    self.wait(0.35)

        # ---------------- the toll: towers -> columns
        exline.save_state()
        with self.beat("b") as d:
            self.play(FadeOut(cmp, shift=DOWN * 0.3), FadeOut(head),
                      exline.animate.scale(0.55).move_to(UP * 3.05 + DOWN * 0.08), run_time=0.8)
            xs = [-3.6, -1.5, 0.6]
            towers = VGroup()
            for x in xs:
                t = lift_tower(floors=5, width=1.15, gap=0.5, grow=0.1, labels=False).move_to([x, -0.4, 0])
                towers.add(t)
            ghost = VGroup(*[lift_tower(floors=5, width=1.15, gap=0.5, grow=0.1, labels=False).move_to([x, -0.4, 0]).set_opacity(o)
                             for x, o in ((2.6, 0.35), (4.3, 0.15))])
            chis = VGroup(*[M(rf"\chi_{{{i + 1}}}", size=34, color=LIFT).next_to(t, DOWN, buff=0.3) for i, t in enumerate(towers)])
            dots = M(r"\cdots", size=50, color=MUTED).move_to([5.5, -0.4, 0])
            self.play(LaggedStart(*[LaggedStart(*[GrowFromCenter(f) for f in t.floors], *[GrowArrow(a) for a in t.arrows], lag_ratio=0.12)
                                    for t in towers], lag_ratio=0.25), run_time=2.0)
            self.play(FadeIn(ghost), FadeIn(dots), run_time=0.6)
            self.at("family of twists")
            tw = T("one run per twist", size=30, color=LIFT).move_to(DOWN * 2.85)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chis], lag_ratio=0.2), FadeIn(tw), run_time=0.9)

            # matrix
            colx = [-3.3, -2.1, -0.9]
            rows_y = [0.75, -0.05, -0.85]
            cols = VGroup()
            for j, v in enumerate(VECS):
                cols.add(VGroup(*[M(str(int(v[i])), size=50, color=LIFT).move_to([colx[j], rows_y[i], 0]) for i in range(3)]))
            h = 2.5; yc = -0.05
            def bracket(x, s):
                return VMobject().set_points_as_corners([[x + s * 0.22, yc + h / 2, 0], [x, yc + h / 2, 0], [x, yc - h / 2, 0], [x + s * 0.22, yc - h / 2, 0]]).set_stroke(INK, 3)
            brk = VGroup(bracket(colx[0] - 0.65, 1), bracket(colx[2] + 0.65, -1))
            self.at("column of numbers")
            self.play(*[ReplacementTransform(towers[j], cols[j]) for j in range(3)], FadeIn(brk),
                      FadeOut(ghost, shift=LEFT), FadeOut(dots), FadeOut(tw), FadeOut(chis), run_time=1.2)

            # toll gates and the coin pile
            gate_y = -1.85
            gates = VGroup()
            for x in colx:
                post = Line([x + 0.45, gate_y - 0.35, 0], [x + 0.45, gate_y + 0.15, 0]).set_stroke(MUTED, 4)
                arm = Line([x + 0.45, gate_y, 0], [x - 0.45, gate_y, 0]).set_stroke(WARM, 5)
                gates.add(VGroup(post, arm))
            pile_c = np.array([4.6, -2.9, 0])
            pile_lab = T("wasted", size=32, color=WARM).move_to(pile_c + UP * 1.6)
            floor = Line(pile_c + LEFT * 1.1, pile_c + RIGHT * 1.1).set_stroke(MUTED, 2).shift(DOWN * 0.12)
            self.play(FadeIn(gates), FadeIn(pile_lab), Create(floor), run_time=0.5)
            self.at("Charged one at a time")
            coins = VGroup()
            rng = np.random.default_rng(3)
            anims = []
            k = 0
            for j in range(3):
                for c in range(3):
                    cn = coin().move_to([colx[j], gate_y - 0.1, 0])
                    target = pile_c + UP * (0.13 * k) + RIGHT * rng.uniform(-0.12, 0.12)
                    coins.add(cn); cn.set_opacity(0)
                    anims.append((j, cn, target))
                    k += 1
            rt = min(3.2, self.left() - 0.15)
            for cn in coins: cn.set_fill(opacity=1).set_stroke(opacity=1)
            self.add(coins)
            per = rt / 3
            for j in range(3):
                group = [(cn, tg) for jj, cn, tg in anims if jj == j]
                self.play(Rotate(gates[j][1], angle=-PI / 2.4, about_point=gates[j][1].get_start(), rate_func=there_and_back),
                          cols[j].animate(rate_func=there_and_back).set_color(WARM),
                          LaggedStart(*[cn.animate(path_arc=-PI / 3).move_to(tg) for cn, tg in group], lag_ratio=0.3),
                          run_time=per)

        # ---------------- shared lattice
        theta = ValueTracker(0.55)
        phi = 0.42
        U = 0.62
        LC = np.array([0.9, -0.3, 0])
        CEN = np.array([1.0, 1.0, 1.0])

        def proj(p):
            th = theta.get_value()
            x, y, z = p - CEN
            x1 = x * np.cos(th) - y * np.sin(th)
            y1 = x * np.sin(th) + y * np.cos(th)
            return LC + U * np.array([x1, z * np.cos(phi) + y1 * np.sin(phi), 0]), y1 * np.cos(phi) - z * np.sin(phi)

        pts = [np.array([i, j, k]) for i in range(-1, 4) for j in range(-1, 4) for k in range(-1, 4)]

        def lattice():
            g = VGroup()
            for p in pts:
                q, dep = proj(p)
                o = np.interp(dep, [-2.5, 2.5], [0.95, 0.2])
                g.add(Dot(q, radius=0.045, color=MUTED, fill_opacity=o))
            return g

        noise = [np.array([0.45, -0.35, 0.3]), np.array([-0.3, 0.4, -0.45]), np.array([0.4, 0.35, -0.3])]
        offs = [ValueTracker(1.0) for _ in range(3)]

        def vec_arrow(j):
            tip3 = VECS[j] + offs[j].get_value() * noise[j]
            a, _ = proj(np.zeros(3)); b, _ = proj(tip3)
            return Arrow(a, b, buff=0, stroke_width=6, color=LIFT, tip_length=0.26, max_stroke_width_to_length_ratio=20)

        def ra_marker(i, j, s=0.55):
            u = VECS[i] / np.linalg.norm(VECS[i]) * s
            w = VECS[j] / np.linalg.norm(VECS[j]) * s
            P = [proj(np.zeros(3))[0], proj(u)[0], proj(u + w)[0], proj(w)[0]]
            return VMobject().set_points_as_corners([P[1], P[2], P[3]]).set_stroke(GOOD, 3)

        with self.beat("c") as d:
            lat = lattice()
            self.play(FadeOut(gates), FadeOut(floor), FadeOut(exline),
                      VGroup(cols, brk).animate.scale(0.8).move_to([-4.85, -0.4, 0]),
                      VGroup(coins, pile_lab).animate.set_opacity(0.5),
                      run_time=0.8)
            self.play(FadeIn(lat, scale=0.8, lag_ratio=0.01), run_time=1.3)
            self.remove(lat, *lat)
            lat = always_redraw(lattice)
            self.add(lat)
            theta.add_updater(lambda m, dt: m.increment_value(0.09 * dt))
            self.add(theta)
            self.at("one shared lattice")
            lab1 = T("one shared lattice", size=32, color=INK).move_to([0.9, 3.1, 0])
            self.play(FadeIn(lab1, shift=DOWN * 0.2), run_time=0.6)
            self.at("so that their divisibility")
            arrows = []
            for j in range(3):
                snap = vec_arrow(j)
                self.play(TransformFromCopy(cols[j], snap), run_time=0.55)
                self.remove(snap)
                ar = always_redraw(lambda j=j: vec_arrow(j))
                arrows.append(ar); self.add(ar)
            self.play(*[o.animate.set_value(0) for o in offs], run_time=0.5, rate_func=rush_into)
            tips = VGroup(*[Circle(radius=0.12, stroke_color=LIFT, stroke_width=3).move_to(proj(VECS[j])[0]) for j in range(3)])
            self.play(LaggedStart(*[ShowPassingFlash(t.copy().scale(2), time_width=0.6) for t in tips], lag_ratio=0.1),
                      *[Flash(proj(VECS[j])[0], color=LIFT, line_length=0.15, num_lines=8, flash_radius=0.2) for j in range(3)], run_time=0.6)
            self.at("nearly perpendicular")
            ras = [always_redraw(lambda i=i, j=j: ra_marker(i, j)) for i, j in ((0, 1), (1, 2), (0, 2))]
            lab2 = T("nearly perpendicular", size=32, color=GOOD).move_to([0.9, -3.4, 0])
            self.play(*[Create(r) for r in ras], FadeIn(lab2, shift=UP * 0.2), run_time=0.9)
            self.wait(max(0, self.left() - 0.1))

        # ---------------- cancellation, wall crumbles
        with self.beat("d") as d:
            theta.clear_updaters()
            for mob in [lat, *arrows, *ras]: mob.clear_updaters()
            self.play(FadeOut(VGroup(lat, *arrows, *ras, lab1, lab2, cols, brk)), run_time=0.5)
            blk = lambda: VGroup(RoundedRectangle(width=1.5, height=0.8, corner_radius=0.12, stroke_color=LIFT, stroke_width=3,
                                                  fill_color=LIFT, fill_opacity=0.45), M(r"\Delta", size=44, color=INK))
            L1 = T("size", size=44, color=WARM); P1 = M("+", size=56); B1 = blk()
            GE = M(r"\geq", size=60)
            R1 = T("divisibility", size=44, color=PRIME); P2 = M("+", size=56); B2 = blk()
            row = VGroup(L1, P1, B1, GE, R1, P2, B2).arrange(RIGHT, buff=0.35).move_to(UP * 0.6)
            self.play(FadeIn(VGroup(L1, P1, GE, R1, P2)), FadeIn(B1, scale=0.6), FadeIn(B2, scale=0.6), run_time=0.8)
            self.at("both sides")
            same = T("same on both sides", size=28, color=LIFT).next_to(row, UP, buff=0.55)
            self.play(Indicate(B1, color=LIFT, scale_factor=1.15), Indicate(B2, color=LIFT, scale_factor=1.15), FadeIn(same), run_time=0.9)
            self.at("and cancels")
            strikes = VGroup(*[Line(b.get_corner(DL) + DL * 0.1, b.get_corner(UR) + UR * 0.1).set_stroke(BAD, 6) for b in (B1, B2)])
            self.play(Create(strikes), run_time=0.45)
            new_row = VGroup(L1.copy(), GE.copy(), R1.copy()).arrange(RIGHT, buff=0.4).move_to(UP * 0.6)
            self.play(FadeOut(VGroup(B1, B2, P1, P2, strikes, same), scale=0.5),
                      L1.animate.move_to(new_row[0]), GE.animate.move_to(new_row[1]), R1.animate.move_to(new_row[2]), run_time=0.7)
            self.at("The waste is gone")
            self.play(LaggedStart(*[c.animate.shift(DOWN * 0.3).set_opacity(0) for c in coins[::-1]], lag_ratio=0.08),
                      FadeOut(pile_lab), run_time=0.8)
            # exponent line returns
            self.play(FadeOut(VGroup(L1, GE, R1), shift=UP * 0.4), Restore(exline), run_time=0.7)
            self.at("Two thirds becomes")
            rubble = []
            for b in wall:
                rubble.append(b.animate(rate_func=rate_functions.ease_in_quad).shift(DOWN * np.random.uniform(1.2, 2.2) + RIGHT * np.random.uniform(-0.4, 0.6))
                              .rotate(np.random.uniform(-1.5, 1.5)).set_opacity(0))
            self.play(LaggedStart(*rubble, lag_ratio=0.03), run_time=1.0)
            m12 = M("X^{1/2}", size=50, color=GOOD)
            rt = min(1.6, self.left() - 0.15)
            self.play(marker.animate.move_to([ex2x(0.5), LINE_Y, 0]).set_color(GOOD),
                      UpdateFromFunc(mlab, lambda m: m.next_to(marker, UP, buff=0.3).shift(LEFT * 0.45)), run_time=rt * 0.7, rate_func=smooth)
            m12.next_to(marker, UP, buff=0.3).shift(LEFT * 0.8)
            self.play(Transform(mlab, m12), Flash(marker, color=GOOD, flash_radius=0.4), run_time=rt * 0.3)
        self.finish()
