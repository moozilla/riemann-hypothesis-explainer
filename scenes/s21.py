import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rh import *

PANEL_BG = "#111829"
PAGE_BG = "#161d2e"


# ---------------------------------------------------------------- helpers (local to this scene)
def pill(w, h, col, op=0.9):
    w = max(w, h)
    return RoundedRectangle(width=w, height=h, corner_radius=h / 2, stroke_width=0, fill_color=col, fill_opacity=op)


def code_rows(n, row_h, bar_h, max_w, seed, unit=0.42, indent_w=0.32):
    """Abstract 'code': rows of thin rounded bars (keywords LIFT, names ZERO, rest MUTED), left-aligned at x=0,
    first row at y=0 going down. Not readable text -- just the texture of source code."""
    rng = np.random.default_rng(seed)
    rows, ind = VGroup(), 0
    for i in range(n):
        ind = int(np.clip(ind + rng.choice([-1, 0, 0, 1], p=[0.25, 0.35, 0.15, 0.25]), 0, 3))
        if i == 0 or rng.random() < 0.12: ind = 0
        k = rng.choice([1, 2, 2, 3, 3, 4])
        bars, x = VGroup(), ind * indent_w
        for j in range(k):
            w = unit * rng.uniform(0.5, 2.6)
            if j == 0 and rng.random() < 0.4: col = LIFT
            elif rng.random() < 0.3: col = ZERO
            else: col = MUTED
            if x + w > max_w: w = max_w - x
            if w < bar_h * 2: break
            b = pill(w, bar_h, col, 0.85)
            b.move_to(RIGHT * (x + w / 2) + DOWN * row_h * i)
            b.base_col, b.base_op = ManimColor(col), 0.85
            bars.add(b)
            x += w + unit * 0.3
        if not len(bars):
            b = pill(unit, bar_h, MUTED, 0.85).move_to(RIGHT * unit / 2 + DOWN * row_h * i)
            b.base_col, b.base_op = ManimColor(MUTED), 0.85
            bars.add(b)
        rows.add(bars)
    return rows


def check_mark(size=0.3, color=GOOD, width=5):
    c = VMobject().set_points_as_corners([np.array([-0.5, 0.0, 0]), np.array([-0.15, -0.38, 0]), np.array([0.55, 0.45, 0])])
    return c.scale(size).set_stroke(color, width).set_fill(opacity=0)


def paper_page():
    """A paper: title, author line, paragraphs, one displayed formula. 16 'lines' (to match 16 code rows)."""
    page = RoundedRectangle(width=4.2, height=5.6, corner_radius=0.06, stroke_color=INK, stroke_width=2,
                            fill_color=PAGE_BG, fill_opacity=1)
    lines = VGroup()
    top = page.get_top()[1] - 0.55
    lines.add(pill(2.6, 0.13, INK, 0.95).move_to(UP * top))
    lines.add(pill(1.4, 0.07, MUTED, 0.9).move_to(UP * (top - 0.33)))
    y = top - 0.8
    widths = [3.3, 3.3, 3.3, 2.2, None, 3.3, 3.3, 3.3, 3.3, 1.7, None, 3.3, 3.3, 2.6]
    for w in widths:
        if w is None:
            lines.add(pill(1.6, 0.1, INK, 0.9).move_to(UP * (y - 0.08)))
            y -= 0.5
        else:
            lines.add(pill(w, 0.06, MUTED, 0.85).move_to(LEFT * (3.3 - w) / 2 + UP * y))
            y -= 0.27
    return VGroup(page, lines)


class S21(NarratedScene):
    sid = "s21"

    def construct(self):
        ROW_H = 0.32
        # ============================================================ a: paper -> code -> kernel
        with self.beat("a") as d:
            paper = paper_page().move_to(UP * 0.1)
            self.play(FadeIn(paper[0], shift=UP * 0.3), LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in paper[1]], lag_ratio=0.06),
                      run_time=1.3)
            self.play(paper.animate.shift(UP * 0.08).rotate(0.015), run_time=self.cue("released as code") - 0.3 - self.now() + self._beat_start,
                      rate_func=smooth)

            # code panel on the left
            panel = RoundedRectangle(width=4.5, height=5.9, corner_radius=0.15, stroke_color=DIM, stroke_width=2,
                                     fill_color=PANEL_BG, fill_opacity=1).move_to(LEFT * 3.95 + DOWN * 0.15)
            rows = code_rows(16, ROW_H, 0.11, 3.8, seed=7)
            rows.move_to(panel.get_corner(UL) + RIGHT * 0.3 + DOWN * 0.38, aligned_edge=UL)
            lean = T("Lean", size=30, color=INK, weight=MEDIUM).next_to(panel, UP, buff=0.12).align_to(panel, LEFT).shift(RIGHT * 0.2)
            self.play(ReplacementTransform(paper[0], panel),
                      LaggedStart(*[ReplacementTransform(l, r) for l, r in zip(paper[1], rows)], lag_ratio=0.04),
                      run_time=1.6)
            self.at("Lean")
            self.play(FadeIn(lean, shift=DOWN * 0.15), run_time=0.5)

            # kernel
            self.at("every logical step", lead=0.6)
            kernel = RoundedRectangle(width=1.9, height=1.45, corner_radius=0.16, stroke_color=INK, stroke_width=4,
                                      fill_color=BG, fill_opacity=1).move_to(RIGHT * 0.55 + UP * 0.25)
            klabel = T("kernel", size=30, color=INK).next_to(kernel, DOWN, buff=0.22)
            self.play(GrowFromCenter(kernel), FadeIn(klabel, shift=UP * 0.1), run_time=0.6)

            # stream rows through the kernel
            N, dt, T1, T2, T3 = 10, 0.0, 0.55, 0.3, 0.6
            Tstream = self.left() - 0.25
            dt = (Tstream - (T1 + T2 + T3)) / (N - 1)
            kin = kernel.get_center()
            OUT_X, OUT_Y0 = 3.05, rows[0].get_center()[1]
            items, checks = VGroup(), VGroup()
            for k in range(N):
                it = rows[k].copy().set_z_index(5)
                it.src = rows[k].get_center(); it.w0 = it.width; it.cur = 1.0
                it.s_in = min(1.0, 1.45 / it.w0) * 0.95
                it.s_out = 0.8
                it.dst_y = OUT_Y0 - k * ROW_H
                it.set_opacity(0)
                items.add(it)
                ck = check_mark(0.3).move_to(RIGHT * (OUT_X - 0.35) + UP * it.dst_y).set_stroke(opacity=0)
                checks.add(ck)
            clk = ValueTracker(0.0)

            def upd(group):
                t = clk.get_value()
                flash = 0.0
                for k, it in enumerate(group):
                    s = t - k * dt
                    if s <= 0:
                        it.set_opacity(0); continue
                    if s < T1:
                        a = smooth(s / T1)
                        sc = interpolate(1.0, it.s_in, a)
                        pos = interpolate(it.src, kin, a)
                    elif s < T1 + T2:
                        sc, pos = it.s_in, kin
                        flash = max(flash, np.sin(PI * (s - T1) / T2))
                    else:
                        a = smooth(min(1.0, (s - T1 - T2) / T3))
                        sc = interpolate(it.s_in, it.s_out, a)
                        dst = np.array([OUT_X + it.w0 * it.s_out / 2, it.dst_y, 0])
                        pos = interpolate(kin, dst, a)
                        checks[k].set_stroke(opacity=a)
                    it.scale(sc / it.cur); it.cur = sc
                    it.move_to(pos)
                    for b in it: b.set_fill(opacity=b.base_op)
                    rows[k].set_opacity(0.25)
                kernel.set_stroke(interpolate_color(ManimColor(INK), ManimColor(GOOD), flash), width=4 + 3 * flash)

            items.add_updater(upd)
            self.add(items, checks)
            self.play(clk.animate.set_value(Tstream), run_time=Tstream, rate_func=linear)
            items.remove_updater(upd)
            kernel.set_stroke(INK, 4)

        # ============================================================ b: the wall, counters, checkers
        with self.beat("b") as d:
            WALL_L, WALL_R, WALL_T, WALL_B = -6.35, -1.6, 3.35, -2.55
            NW, WRH = 60, 0.1
            wall = code_rows(NW, WRH, 0.05, WALL_R - WALL_L, seed=11, unit=0.62, indent_w=0.3)
            wall.move_to(np.array([WALL_L, WALL_T - 0.05, 0]), aligned_edge=UL)
            wall_h = NW * WRH
            band = ValueTracker(99.0)

            def wall_upd(m, dt_):
                for r in m:
                    r.shift(UP * 0.35 * dt_)
                    if r.get_center()[1] > WALL_T:
                        r.shift(DOWN * wall_h)
                    y = r.get_center()[1]
                    edge = np.clip(min(WALL_T - y, y - (WALL_T - wall_h)) / 0.5, 0, 1)
                    g = np.clip(1 - abs(y - band.get_value()) / 0.45, 0, 1)
                    for b in r:
                        b.set_fill(interpolate_color(b.base_col, ManimColor(GOOD), g), opacity=b.base_op * edge)

            out_stuff = VGroup(kernel, klabel, items, checks, lean, panel)
            self.play(FadeOut(out_stuff), ReplacementTransform(rows, wall[:16]),
                      LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in wall[16:]], lag_ratio=0.02), run_time=1.0)
            wall.add_updater(wall_upd)

            # counters
            n_lines, n_files = ValueTracker(0), ValueTracker(0)

            def counter(tr, word, y):
                lab = T(word, size=40, color=MUTED).move_to(RIGHT * 4.95 + UP * y, aligned_edge=LEFT)
                num = T("0", size=80, color=WARM)
                anchor = np.array([4.7, y, 0])

                def u(m):
                    m.become(T(f"{int(round(tr.get_value())):,}", size=80, color=WARM))
                    m.move_to(anchor, aligned_edge=RIGHT).align_to(lab, DOWN)
                num.add_updater(u); u(num)
                return VGroup(num, lab)
            c1 = counter(n_lines, "lines", 0.85)
            c2 = counter(n_files, "files", -0.75)
            self.add(c1[0]); self.play(FadeIn(c1[1]), n_lines.animate.set_value(17374215), run_time=2.2, rate_func=rush_from)
            self.at("thousand files", lead=1.6)
            self.add(c2[0]); self.play(FadeIn(c2[1]), n_files.animate.set_value(175187), run_time=1.8, rate_func=rush_from)
            for c in (c1, c2): c[0].clear_updaters()

            # compact the counters beneath the wall; checkers appear on the right
            self.at("Within hours", lead=0.4)
            small = VGroup(*[VGroup(T(v, size=32, color=WARM), T(w, size=26, color=MUTED)) for v, w in (("17,374,215", "lines"), ("175,187", "files"))])
            for c in small: c[1].next_to(c[0], RIGHT, buff=0.14, aligned_edge=DOWN)
            small.arrange(RIGHT, buff=0.55, aligned_edge=DOWN).move_to(np.array([WALL_L, -3.12, 0]), aligned_edge=LEFT)
            names = ["Lean kernel", "nanoda", "con-leche", "con-agua", "Pestka", "nanoclo", "tenet"]
            ys = np.linspace(2.75, -2.35, len(names))
            rowsC, cables = VGroup(), VGroup()
            for nm, y in zip(names, ys):
                circ = Circle(radius=0.22, stroke_color=MUTED, stroke_width=3, fill_color=GOOD, fill_opacity=0).move_to(RIGHT * 1.15 + UP * y)
                lab = Text(nm, font=MONO, font_size=32, color=MUTED).next_to(circ, RIGHT, buff=0.35)
                rowsC.add(VGroup(circ, lab))
                cables.add(Line(np.array([WALL_R + 0.15, y, 0]), circ.get_left() + LEFT * 0.08).set_stroke(DIM, 2))
            self.play(Transform(c1, small[0]), Transform(c2, small[1]), run_time=0.9)
            band.set_value(WALL_T + 0.6)
            self.play(band.animate(rate_func=linear).set_value(WALL_T - wall_h - 0.6),
                      LaggedStart(*[AnimationGroup(Create(cb), FadeIn(r, shift=LEFT * 0.2)) for cb, r in zip(cables, rowsC)],
                                  lag_ratio=0.15, run_time=1.6), run_time=2.6)

            tick_marks = VGroup()

            def tick(i, rt):
                circ, lab = rowsC[i]
                ck = check_mark(0.33, color=BG, width=5).move_to(circ).set_z_index(4); tick_marks.add(ck)
                pulse = cables[i].copy().set_stroke(GOOD, 5)
                return Succession(ShowPassingFlash(pulse, time_width=0.6, run_time=rt * 0.5),
                                  AnimationGroup(circ.animate.set_fill(GOOD, 1).set_stroke(GOOD), lab.animate.set_color(INK),
                                                 cables[i].animate.set_stroke(GOOD, 2, opacity=0.5), Create(ck), run_time=rt * 0.5))
            self.at("It passed Lean", lead=0.1)
            self.play(tick(0, 0.9))
            self.at("one independent")
            rest = self.left() - 0.2
            self.play(LaggedStart(*[tick(i, 0.7) for i in range(1, 7)], lag_ratio=(rest - 0.7) / 5 / 0.7, run_time=rest))

        # ============================================================ c: the final statement
        with self.beat("c") as d:
            wall.remove_updater(wall_upd)
            src_row = min(wall, key=lambda r: abs(r.get_center()[1] - 0.2))
            card_txt = Text("theorem riemannHypothesis : RiemannHypothesis", font=MONO, font_size=34, color=INK,
                            t2c={"theorem": LIFT, ":": MUTED, "RiemannHypothesis": ZERO})
            card_txt.move_to(UP * 1.55)
            card = RoundedRectangle(width=card_txt.width + 0.9, height=card_txt.height + 0.8, corner_radius=0.16,
                                    stroke_color=MUTED, stroke_width=2, fill_color=PANEL_BG, fill_opacity=1).move_to(card_txt)
            stmt = card_txt[-17:]
            hl = src_row.copy()
            self.play(FadeOut(VGroup(rowsC, cables, c1, c2, tick_marks)), wall.animate.set_opacity(0.12),
                      hl.animate.set_fill(ZERO, 1).scale(1.4), run_time=0.8)
            self.play(ReplacementTransform(hl, card), run_time=0.7)
            self.play(AddTextLetterByLetter(card_txt, time_per_char=0.03), run_time=1.3)
            self.at("definition of the Riemann")
            ul = Line(stmt.get_corner(DL), stmt.get_corner(DR)).shift(DOWN * 0.12).set_stroke(ZERO, 3)
            self.play(Create(ul), Indicate(stmt, color=ZERO, scale_factor=1.04), run_time=0.7)

            # Mathlib box with a small shelf of 'definitions'; one spine is RiemannHypothesis
            self.at("already sitting", lead=0.5)
            rng = np.random.default_rng(3)
            spines = VGroup(*[pill(rng.uniform(0.55, 0.85), 0.16, [MUTED, LIFT, MUTED, ZERO][i % 4], 0.55).rotate(PI / 2) for i in range(13)])
            spines.arrange(RIGHT, buff=0.07, aligned_edge=DOWN)
            key = spines[10].set_fill(ZERO, 1).stretch_to_fit_height(0.95, about_edge=DOWN)
            words = VGroup(T("Mathlib", size=40, color=INK, weight=BOLD), T("the public library", size=30, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            inner = VGroup(words, spines).arrange(RIGHT, buff=0.9, aligned_edge=DOWN)
            box = RoundedRectangle(width=inner.width + 1.0, height=inner.height + 0.7, corner_radius=0.18,
                                   stroke_color=INK, stroke_width=3, fill_color=BG, fill_opacity=1)
            mbox = VGroup(box, inner)
            inner.move_to(box)
            # put the key spine straight under the statement
            mbox.move_to(DOWN * 1.75)
            mbox.shift(RIGHT * min(6.3 - mbox.get_right()[0], stmt.get_center()[0] - key.get_center()[0]))
            arrow = Arrow(ul.get_center() + DOWN * 0.1, key.get_top() + UP * 0.08, buff=0.0, stroke_width=4, color=ZERO,
                          max_tip_length_to_length_ratio=0.12)
            self.play(FadeIn(mbox, shift=UP * 0.2), run_time=0.7)
            self.play(GrowArrow(arrow), Indicate(key, color=ZERO, scale_factor=1.15), run_time=0.9)
            r = self.left() - 0.3
            if r > 0.6:
                self.play(ShowPassingFlash(arrow.copy().set_stroke(INK, 6), time_width=0.5),
                          stmt.animate(rate_func=there_and_back).set_color(INK), run_time=min(1.5, r))

        # ============================================================ d: the wall folds into a booklet
        with self.beat("d") as d:
            wall.set_opacity(0.12)
            for r in wall:
                for b in r: b.set_fill(b.base_col)
            self.play(FadeOut(VGroup(card, card_txt, ul, mbox, arrow)), run_time=0.7)
            frame = RoundedRectangle(width=WALL_R - WALL_L + 0.4, height=wall.height + 0.4, corner_radius=0.15,
                                     stroke_color=DIM, stroke_width=2, fill_color=PANEL_BG, fill_opacity=1).move_to(wall)
            target_c = ORIGIN + UP * 0.1
            self.play(FadeIn(frame), *[b.animate.set_fill(opacity=b.base_op) for r in wall for b in r], run_time=0.8)
            self.play(VGroup(frame, wall).animate.scale(1.12).move_to(target_c), run_time=1.0)

            # booklet: back page + front page with a handful of lines
            bw, bh = 2.3, 3.0
            back = RoundedRectangle(width=bw, height=bh, corner_radius=0.08, stroke_color=MUTED, stroke_width=2,
                                    fill_color=PAGE_BG, fill_opacity=1).move_to(target_c + RIGHT * 0.12 + DOWN * 0.1)
            front = RoundedRectangle(width=bw, height=bh, corner_radius=0.08, stroke_color=INK, stroke_width=3,
                                     fill_color=PAGE_BG, fill_opacity=1).move_to(target_c)
            spine = Line(front.get_corner(UL) + RIGHT * 0.18, front.get_corner(DL) + RIGHT * 0.18).set_stroke(MUTED, 2)
            blines = VGroup(pill(1.3, 0.1, INK, 0.95).move_to(front.get_top() + DOWN * 0.45 + RIGHT * 0.09))
            for i, w in enumerate([1.6, 1.6, 1.2, 1.6, 1.6, 0.9, 1.6, 1.3]):
                blines.add(pill(w, 0.05, MUTED, 0.85).move_to(front.get_top() + DOWN * (0.85 + 0.25 * i) + RIGHT * 0.09 + LEFT * (1.6 - w) / 2))
            BK = 1.3
            for m in (back, front, spine, blines): m.scale(BK, about_point=target_c)
            keep_idx = np.linspace(4, NW - 5, len(blines)).astype(int)
            order = sorted(range(NW), key=lambda i: -abs(wall[i].get_center()[1] - target_c[1]))
            keepers = [wall[i] for i in keep_idx]
            others = [wall[i] for i in order if i not in set(keep_idx)]
            self.at("Alpöge himself", lead=0.3)
            fold_t = min(4.0, self.left() - 2.5)
            self.play(LaggedStart(*[r.animate.move_to(np.array([target_c[0], np.clip(r.get_center()[1], -1.2, 1.4), 0])).stretch(0.25, 0).set_opacity(0)
                                    for r in others], lag_ratio=0.02),
                      *[ReplacementTransform(k, l) for k, l in zip(keepers, blines)],
                      ReplacementTransform(frame, front), FadeIn(back), Create(spine),
                      run_time=fold_t)
            booklet = VGroup(back, front, spine, blines)
            self.remove(*others)
            r = self.left() - 0.1
            self.play(booklet.animate.shift(UP * 0.12).rotate(-0.03), run_time=max(0.5, r), rate_func=there_and_back)
        self.play(FadeOut(booklet), run_time=0.5)
        self.finish()
