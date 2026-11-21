"""Recurring visual motifs, shared so they look identical in every scene that uses them."""
import functools
import numpy as np
from manim import *
from .common import *


@functools.lru_cache(None)
def primes_upto(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return [int(p) for p in np.nonzero(s)[0]]


@functools.lru_cache(None)
def zeta_zeros(n):
    """Imaginary parts of the first n nontrivial zeros (cached on disk)."""
    import os, json
    path = os.path.join(ROOT, "build/zeros.json")
    z = json.load(open(path)) if os.path.exists(path) else []
    if len(z) < n:
        import mpmath
        z = z + [float(mpmath.zetazero(k).imag) for k in range(len(z) + 1, n + 1)]
        json.dump(z, open(path, "w"))
    return z[:n]


def critical_strip(height=6.0, width=2.2, tmax=52.0, n_zeros=10, labels=True):
    """The critical strip 0<Re<1 with the line Re=1/2 and the first zeros.
    Returns VGroup with attributes: .strip .line .zeros (VGroup of Dots) .axis .p2c(sigma,t)->point"""
    strip = Rectangle(width=width, height=height, stroke_width=0, fill_color=ZERO, fill_opacity=0.10)
    edges = VGroup(Line(strip.get_corner(DL), strip.get_corner(UL)), Line(strip.get_corner(DR), strip.get_corner(UR))).set_stroke(MUTED, 2)
    line = Line(strip.get_bottom(), strip.get_top()).set_stroke(ZERO, 3)
    axis = Line(strip.get_corner(DL) + LEFT * 0.9, strip.get_corner(DR) + RIGHT * 0.9).set_stroke(MUTED, 2)
    g = VGroup(strip, edges, axis, line)

    def p2c(sigma, t):
        return strip.get_corner(DL) + RIGHT * width * sigma + UP * height * t / tmax
    zeros = VGroup(*[Dot(p2c(0.5, t), radius=0.07, color=ZERO).set_z_index(3) for t in zeta_zeros(n_zeros) if t < tmax])
    g.add(zeros)
    if labels:
        labs = VGroup(M("0", size=30, color=MUTED).next_to(strip.get_corner(DL), DOWN, buff=0.12),
                      M(r"\tfrac12", size=30, color=ZERO).next_to(strip.get_bottom(), DOWN, buff=0.12),
                      M("1", size=30, color=MUTED).next_to(strip.get_corner(DR), DOWN, buff=0.12))
        g.add(labs); g.labels = labs
    g.strip, g.edges, g.line, g.zeros, g.axis, g.p2c = strip, edges, line, zeros, axis, p2c
    return g


def balance_scale(left_label="divisibility", right_label="size", tilt=0.0):
    """A two-pan balance. Returns VGroup with .beam_group (rotate about .pivot to tilt), .left_pan, .right_pan."""
    base = VGroup(Line(DOWN * 1.6, UP * 0.9).set_stroke(MUTED, 5), Line(LEFT * 0.7 + DOWN * 1.6, RIGHT * 0.7 + DOWN * 1.6).set_stroke(MUTED, 5))
    pivot = Dot(UP * 0.9, radius=0.08, color=INK)
    beam = Line(LEFT * 2.4 + UP * 0.9, RIGHT * 2.4 + UP * 0.9).set_stroke(INK, 5)

    def pan(x, color, label):
        top = np.array([x, 0.9, 0])
        strings = VGroup(Line(top, top + DOWN * 1.1 + LEFT * 0.6), Line(top, top + DOWN * 1.1 + RIGHT * 0.6)).set_stroke(MUTED, 2)
        dish = ArcBetweenPoints(top + DOWN * 1.1 + LEFT * 0.7, top + DOWN * 1.1 + RIGHT * 0.7, angle=PI / 2.2).set_stroke(color, 5)
        lab = T(label, size=26, color=color).next_to(dish, DOWN, buff=0.25)
        return VGroup(strings, dish, lab)
    lp, rp = pan(-2.4, PRIME, left_label), pan(2.4, WARM, right_label)
    beam_group = VGroup(beam, lp, rp)
    g = VGroup(base, beam_group, pivot)
    g.beam_group, g.left_pan, g.right_pan, g.pivot, g.beam = beam_group, lp, rp, pivot, beam
    if tilt: beam_group.rotate(tilt, about_point=pivot.get_center())
    return g


def lift_tower(floors=6, width=2.6, gap=0.62, grow=0.12, labels=True):
    """Tower of theta lifts: platforms U_0..U_m joined by theta arrows. .floors[i], .arrows[i], .labels[i]"""
    fl, ar, lb = VGroup(), VGroup(), VGroup()
    for i in range(floors):
        w = width * (1 + grow * i)
        p = RoundedRectangle(width=w, height=0.16, corner_radius=0.08, stroke_width=0, fill_color=LIFT, fill_opacity=0.35 + 0.5 * i / max(1, floors - 1)).move_to(UP * gap * i)
        fl.add(p)
        if labels: lb.add(M(rf"U_{{{i}}}", size=26, color=LIFT).next_to(p, LEFT, buff=0.2))
        if i:
            ar.add(Arrow(fl[i - 1].get_top(), p.get_bottom(), buff=0.04, stroke_width=3, color=INK, max_tip_length_to_length_ratio=0.35, tip_length=0.14))
    g = VGroup(fl, ar, lb)
    g.floors, g.arrows, g.labels = fl, ar, lb
    return g


ROADMAP_STATIONS = ["multiplicity\nfrom symmetry", "divisibility\nvs size", "a ceiling\non the primes", "zeros on\nthe line"]


def roadmap(active=-1, done=0):
    """Four-station roadmap of the proof (left = start, right = RH). Stations < done are GOOD, == active is highlighted.
    .stations[i] (VGroup(dot,label)), .links[i]"""
    xs = np.linspace(-5.1, 5.1, 4)
    st, ln = VGroup(), VGroup()
    for i, (x, name) in enumerate(zip(xs, ROADMAP_STATIONS)):
        col = GOOD if i < done else (PRIME if i == active else MUTED)
        dot = Circle(radius=0.2, stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.9 if i < done or i == active else 0.0).move_to(RIGHT * x)
        lab = Text(name, font=FONT, font_size=24, color=col, line_spacing=0.8).next_to(dot, DOWN, buff=0.3)
        st.add(VGroup(dot, lab))
        if i: ln.add(Arrow(st[i - 1][0].get_right(), dot.get_left(), buff=0.12, stroke_width=3, color=GOOD if i <= done - 1 else MUTED, tip_length=0.18))
    g = VGroup(ln, st)
    g.stations, g.links = st, ln
    return g


def number_token(label="?", color=PRIME, r=0.42):
    """The 'special number' — a glowing token."""
    glow = VGroup(*[Circle(radius=r * (1 + 0.25 * k), stroke_width=0, fill_color=color, fill_opacity=0.10) for k in range(1, 4)])
    core = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=BG, fill_opacity=1)
    t = M(label, size=40, color=color).move_to(core)
    g = VGroup(glow, core, t); g.label = t
    return g


def scene_title(text, act=None):
    """Small lower-left caption used at the start of a scene (optional)."""
    t = T(text, size=30, color=INK, weight=MEDIUM)
    g = VGroup(t)
    if act:
        a = T(act.upper(), size=18, color=MUTED); g = VGroup(a, t).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    return g.to_corner(DL, buff=0.5)
