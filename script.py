"""Narration script: single source of truth.

Each scene has an id, a title, and beats. Each beat has:
  text   - the narration (spoken verbatim by TTS)
  visual - direction for the animator (what should be on screen during this beat)
Beat key = scene id + beat letter, e.g. "s05c".
"""

SCENES = [
    # ------------------------------------------------------------------ ACT 0
    dict(id="s01", act="Prologue", title="Static, or music?", beats=[
        dict(text="This is a list of the prime numbers. Two, three, five, seven, eleven. Numbers that can't be broken into smaller pieces.",
             visual="Black screen. Primes appear one by one as glowing numerals along a number line; composites are dim dots between them."),
        dict(text="They are the atoms of arithmetic. Every whole number is built by multiplying primes together, in exactly one way.",
             visual="A few composites (12, 30, 91, 360) split apart into their prime factors like molecules into atoms, e.g. 360 -> 2·2·2·3·3·5."),
        dict(text="And yet nobody can tell you where the next one will be. They show up like static. No formula. No rhythm anyone can hear.",
             visual="Zoom way out on the number line: primes as irregular ticks, like a barcode / noise strip scrolling by. Gaps visibly erratic."),
        dict(text="In eighteen fifty-nine, Bernhard Riemann guessed that there is a rhythm after all. That the static is actually music, and that every note is tuned in a very precise way. For a hundred and sixty-seven years, nobody could prove it.",
             visual="The barcode strip decomposes into a stack of clean sine waves (foreshadowing s08). '1859' appears; a timeline bar runs 1859 -> 2026 with the label 'unproved'."),
        dict(text="In November twenty twenty-six, the mathematician Levent Alpöge, working with the AI model Claude, published a proof. Seventeen million lines of it, checked line by line by a computer. This video is about what the Riemann hypothesis says, and how that proof works.",
             visual="Timeline reaches Nov 2026. A wall of tiny scrolling code-like lines (abstract, not readable) with a counter ticking up to 17,374,215 lines. Then title card: 'The Riemann Hypothesis — what it says, and how the proof works'."),
    ]),
    # ------------------------------------------------------------------ ACT I
    dict(id="s02", act="Act I · The primes", title="The sieve", beats=[
        dict(text="Let's start from the ground. Write down the whole numbers. Cross out every multiple of two. Then every multiple of three. Then five. Then seven. Whatever survives is prime.",
             visual="Grid of 2..121 (or 1..100). Sieve of Eratosthenes: sweep colors for multiples of 2, 3, 5, 7 in turn, each fading out; survivors glow in the prime color. Time the four sweeps to the words."),
        dict(text="Look at the survivors. Sometimes two of them sit side by side, like eleven and thirteen. Sometimes there are long deserts with none at all. Up close, there's no pattern.",
             visual="Highlight the twin pair 11, 13 with a bracket. Then highlight the gap 89 -> 97 (or 113 -> 127 if the grid goes that far) as a 'desert'."),
        dict(text="So let's stop asking where the primes are, and ask an easier question. How many are there?",
             visual="The surviving primes drop out of the grid and line up on a number line at the bottom, setting up the staircase."),
    ]),
    dict(id="s03", act="Act I · The primes", title="Counting primes", beats=[
        dict(text="Walk along the number line, and every time you step on a prime, climb one stair. Mathematicians call this staircase pi of x: the number of primes up to x.",
             visual="Axes 0..30. A dot walks along x; staircase pi(x) is drawn as it goes, stepping at 2,3,5,7,... Label the curve with the formula pi(x)."),
        dict(text="Up close it's jagged. Now zoom out. To a thousand. To a million. The stairs melt into a smooth curve.",
             visual="Animated zoom of the axes range: 30 -> 100 -> 1,000 -> 1,000,000 (recompute staircase at each scale; show range labels). The curve visibly smooths."),
        dict(text="As a teenager, Gauss noticed what that curve is. Near a number x, about one in every natural log of x numbers is prime. Near a million, that's about one in fourteen. Near a trillion, one in twenty-eight. Primes thin out, slowly and predictably.",
             visual="Show 'chance that a number near x is prime ≈ 1 / ln x'. Two little strips of dots: 14 dots with one lit (near 10^6), 28 dots with one lit (near 10^12)."),
        dict(text="Add up those odds and you get a prediction for the staircase. In eighteen ninety-six this was proved: the prediction and the truth agree, in the long run. That's the prime number theorem.",
             visual="Smooth curve Li(x) (integral of 1/ln t) drawn over the staircase on 0..1000 — they hug each other. Label 'prediction' vs 'truth'. Caption: 'Prime Number Theorem, 1896'."),
    ]),
    dict(id="s04", act="Act I · The primes", title="The wobble", beats=[
        dict(text="But 'in the long run' hides the interesting part. Subtract the prediction from the truth, and you're left with the error. A wobble.",
             visual="Staircase minus Li(x): the two curves separate, and the difference is plotted on its own axes below as a jittery curve around zero."),
        dict(text="How big can the wobble get? Here's a comparison. Flip a coin a million times. You expect half a million heads, but you'll miss by a bit. Typically by about a thousand, which is the square root of a million. Square-root-sized error is the signature of pure randomness.",
             visual="Several random-walk paths (heads minus tails) fanning out from the origin, with a sqrt(N) envelope curve above and below that contains them. Show 'N = 1,000,000 flips -> off by ~1,000 = sqrt(N)'."),
        dict(text="The Riemann hypothesis says the primes behave exactly like that. Count the primes up to x, and the prediction is off by about the square root of x, and never much more. The primes are as orderly as a random thing can possibly be.",
             visual="Back to the prime error curve: overlay the sqrt(x) envelope (scaled appropriately, e.g. sqrt(x)·ln(x)/(8π)) and show the wobble staying inside. Statement on screen: '|truth − prediction| ≲ sqrt(x)'."),
        dict(text="To see why anyone would believe that, we need one of the strangest objects in mathematics.",
             visual="Everything fades except a single glowing zeta symbol ζ in the center."),
    ]),
    # ------------------------------------------------------------------ ACT II
    dict(id="s05", act="Act II · The zeta function", title="One function that knows every prime", beats=[
        dict(text="Take the whole numbers, raise each to some power s, flip them over, and add them all up. One, plus one over two to the s, plus one over three to the s, and on forever. This is the zeta function.",
             visual="Build the series term by term: ζ(s) = 1 + 1/2^s + 1/3^s + 1/4^s + ... Highlight 's' as the input knob."),
        dict(text="When s is two, the sum settles down to a famous value, pi squared over six. Different inputs s, different outputs.",
             visual="Set s=2: bars of height 1, 1/4, 1/9, ... stacking toward a dashed line at π²/6 ≈ 1.6449. Running partial sum counter."),
        dict(text="On its face, this has nothing to do with primes. Then Euler found something astonishing. The very same function can be written as a product, with one factor for each prime, and nothing else.",
             visual="The sum morphs into / is joined by the Euler product: ζ(s) = 1/(1−2^{-s}) · 1/(1−3^{-s}) · 1/(1−5^{-s}) · 1/(1−7^{-s}) ··· with the primes 2,3,5,7 colored in the prime color."),
        dict(text="Why? Because every whole number is a unique product of primes. Multiply these brackets out, and every number appears exactly once. So zeta is a single function that knows about all the primes at once. Whatever the primes are doing, it's encoded in here.",
             visual="Show brackets (1 + 1/2^s + 1/4^s + ...)(1 + 1/3^s + 1/9^s + ...)(1 + 1/5^s + ...). Pick one term from each bracket (1/4^s, 1/3^s, 1/5^s), draw lines converging to 1/60^s. Then a 'sum over integers' ⇔ 'product over primes' bridge graphic."),
    ]),
    dict(id="s06", act="Act II · The zeta function", title="Numbers that spin", beats=[
        dict(text="Riemann's leap was to feed this function a new kind of input: complex numbers. Don't let the name scare you. A complex number is just a point on a plane, instead of a point on a line. It has a left-right part, and an up-down part.",
             visual="Number line; then it opens up into a plane. A point s with dashed projections to both axes; labels 'left-right part' and 'up-down part' (small secondary labels Re, Im)."),
        dict(text="What does it mean to raise a number to a complex power? Picture an arrow. The left-right part of s sets the arrow's length. The up-down part sets its angle, how far it has been spun around.",
             visual="Split screen: left, the s-plane with a draggable point s; right, an arrow for 1/n^s (say n=2). Move s left-right: arrow length changes. Move s up-down: arrow rotates. Use real math: 1/n^s has length n^{-σ}, angle −t·ln n."),
        dict(text="So each term of zeta becomes a little arrow, and adding them means laying them tip to tail. The sum traces out a spiral, and where the spiral ends up, that's the value of zeta.",
             visual="For a fixed s (e.g. s = 1.5 + 6i so the plain series converges visibly), draw arrows 1, 1/2^s, 1/3^s, ... tip to tail forming a spiral that converges to a point, marked ζ(s)."),
        dict(text="Change the input and the whole spiral changes shape. And for certain very special inputs, something remarkable happens.",
             visual="Animate s moving (ValueTracker); the spiral reshapes continuously and its endpoint wanders. End with s heading toward 1/2 + 14.13i. (Inside the strip use the alternating/eta series trick so partial sums converge: ζ(s) = η(s)/(1−2^{1−s}); just draw the η arrows.)"),
    ]),
    dict(id="s07", act="Act II · The zeta function", title="The zeros and the line", beats=[
        dict(text="The spiral curls back and lands exactly on zero. Every arrow cancelled by the others. An input like this is called a zero of the zeta function.",
             visual="Arrow spiral for s = 1/2 + 14.1347i (eta series) ending precisely at the origin; origin pulses. Label 'ζ(s) = 0'."),
        dict(text="Where are they? There are some boring ones off to the left that everyone understands. The interesting ones all live in this narrow strip, between zero and one. The critical strip.",
             visual="The s-plane. Mark trivial zeros at −2, −4, −6 as dim dots ('boring'). Shade the vertical strip 0 < Re s < 1, label 'critical strip'."),
        dict(text="Riemann computed the first few. And they weren't scattered around the strip. They were lined up, dead center, on the line where the left-right part is exactly one half.",
             visual="Zeros pop in one by one at heights 14.13, 21.02, 25.01, 30.42, 32.94, ... (use mpmath.zetazero) all on Re = 1/2. Then draw the critical line through them; label '1/2'."),
        dict(text="His guess: all of them are on that line. Every single one, forever. That's the Riemann hypothesis. Computers have since checked trillions of zeros. All on the line. But trillions is not all.",
             visual="Camera/axes zoom out vertically: hundreds of zeros stream up the line. Title 'The Riemann Hypothesis: every zero in the strip has real part 1/2'. Counter '10,000,000,000,000+ checked'."),
    ]),
    dict(id="s08", act="Act II · The zeta function", title="The music of the primes", beats=[
        dict(text="Why should the position of these dots matter to anyone? Because Riemann found an exact formula connecting zeros to primes. Each zero contributes one wave to the prime staircase.",
             visual="Left: the critical line with zeros as dots. Right: axes for the prime-counting staircase. A zero dot emits a wave that travels over to the right panel."),
        dict(text="Start with the smooth prediction. Add the wave from the first zero. Then the second. Then ten of them. A hundred. The smooth curve grows stairs, and the stairs land exactly on the primes. The zeros are the notes, and the primes are the music.",
             visual="THE HERO SHOT. Use the explicit formula for Chebyshev psi: ψ(x) ≈ x − Σ_ρ x^ρ/ρ − ln(2π), i.e. x − 2·Re Σ_{k≤N} x^{ρ_k}/ρ_k, on x in [2, 50] (or Riemann's formula for π(x)). Animate N = 0, 1, 2, 10, 100 zeros: the smooth line develops steps located at primes/prime powers. Show the true staircase faintly behind; counter 'zeros used: N'. Precompute with mpmath."),
        dict(text="Each zero's two coordinates do different jobs. Its height sets the pitch of the wave. Its left-right position sets the volume: how fast the wave grows as you move along the number line.",
             visual="One zero dot with a single wave beside it. Slide the dot up: frequency increases. Slide the dot right: the wave's envelope x^β grows faster. Labels 'height → pitch', 'left-right → volume'."),
        dict(text="A zero on the center line makes a wave that grows like the square root of x. That's the coin-flip size. A zero to the right of the line would be louder than that, a wave big enough to break the square-root rule. So 'all zeros on the line' and 'the primes have square-root error' are the same statement. That's the hypothesis, in two languages.",
             visual="Zero on the line: wave within sqrt(x) envelope (green/ok). Hypothetical zero at Re = 0.8 (red ghost): wave envelope x^0.8 bursts through the sqrt envelope. End card with a two-way arrow: 'all zeros on the line' ⇔ 'prime error ≈ sqrt(x)'."),
    ]),
    dict(id="s09", act="Act II · The zeta function", title="The generalized hypothesis", beats=[
        dict(text="The proof actually establishes something bigger. Sort the primes by their last digit. Apart from two and five, every prime ends in one, three, seven, or nine. Do the four teams get an equal share?",
             visual="Primes stream in and get sorted into four bins labelled by last digit 1, 3, 7, 9 (each a color); a bar-chart race as counts grow (to, say, primes below 10,000)."),
        dict(text="In the long run, yes. But how evenly? To study that, you build cousins of the zeta function, called Dirichlet L-functions. Same sum, except each term gets a twist, a little rotation that depends on the number's remainder.",
             visual="Bars end nearly equal. Then: ζ(s) = Σ 1/n^s morphs to L(s, χ) = Σ χ(n)/n^s. Show χ as a small dial per remainder class (e.g. mod 5: χ(1)=1, χ(2)=i, χ(3)=−i, χ(4)=−1, χ(0)=0) — arrows on unit circles."),
        dict(text="Each of these cousins has its own zeros, and its own critical line. The generalized Riemann hypothesis says: all of their zeros are on the line too. For every one of these functions, all at once. This is the statement that was proved.",
             visual="Several side-by-side critical strips (one per L-function, different colors), each with zeros on its center line. Title: 'Generalized Riemann Hypothesis (Dirichlet L-functions)'. A check mark sweeps across them."),
    ]),
    # ------------------------------------------------------------------ ACT III
    dict(id="s10", act="Act III · The clue", title="A parallel universe", beats=[
        dict(text="For a century and a half, this problem defeated everyone who touched it. But there was one clue. A parallel universe where the Riemann hypothesis is true, and we know why.",
             visual="Timeline 1859–2026 with a long empty stretch. Then the screen splits in two: 'our universe: whole numbers' | 'parallel universe' (a mirrored, differently tinted panel)."),
        dict(text="In that universe, you swap the whole numbers for clock arithmetic. Numbers that wrap around, like hours on a clock with a prime number of hours. In this world, you count solutions to equations, points on curves, instead of counting primes.",
             visual="A clock with 7 hours (0..6); show 5 + 4 = 2 wrapping around. Then a 7×7 (or 11×11 / 13×13) grid of points with the solutions of y² = x³ + x + 1 (mod p) lit up — 'points on a curve'."),
        dict(text="These curves have their own zeta functions, with their own zeros and their own critical line. And in the nineteen forties, André Weil proved that every one of those zeros is on the line. The number of points on a curve is always within a square root of the prediction.",
             visual="For several primes p, plot the number of points on the curve vs p: points hugging the line p+1 inside the band p + 1 ± 2·sqrt(p). Caption 'Weil, 1940s: |#points − (p+1)| ≤ 2·sqrt(p)'. A check mark for this universe."),
        dict(text="So the square-root law is real, somewhere. The question was always how to carry the proof across to the ordinary whole numbers.",
             visual="Split screen again: right panel has a check mark; left panel a question mark. A dashed bridge arrow from right to left, incomplete."),
    ]),
    dict(id="s11", act="Act III · The clue", title="Stepanov's trick", beats=[
        dict(text="In nineteen sixty-nine, Sergei Stepanov found a new proof of Weil's theorem that needed almost no machinery. Just one humble fact: a polynomial of degree d can equal zero at most d times.",
             visual="A wiggly polynomial curve of degree 5 crossing the x-axis 5 times; the crossings light up and are counted. 'degree d ⇒ at most d zeros'."),
        dict(text="Here is the trick. Suppose you want to show a curve doesn't have too many points. Build a helper polynomial that equals zero at every one of those points. Then the number of points is at most its degree.",
             visual="Dots on the axis (the 'points to be counted', unknown number, shown with a '?' count). A helper curve is threaded through all of them. Inequality: '#points ≤ degree'."),
        dict(text="That alone is too weak. So Stepanov did something clever. He made the helper vanish at each point not once, but many times over. Not just touching zero, but flat there. Flat to order m. That's called multiplicity.",
             visual="Zoom on one zero: curve crosses like x (m=1), then touches like x² (m=2), then flatter x³, x⁴ ... Animate the local shape flattening as m increases; label 'multiplicity m'."),
        dict(text="Now each point uses up m of the polynomial's zeros, instead of one. So the number of points, times m, is at most the degree. Crank up the multiplicity, and the bound gets sharper and sharper, all the way down to the square-root law.",
             visual="Budget picture: a bar of length 'degree' being consumed by blocks of size m, one per point. Inequality: '#points × m ≤ degree' → '#points ≤ degree / m'. A dial for m turning up while the bound shrinks toward 'p + 1 + sqrt-sized'."),
    ]),
    dict(id="s12", act="Act III · The clue", title="Why it doesn't cross over", beats=[
        dict(text="So why not just do that for the ordinary primes? Because of how you measure flatness. To check that a function is flat, you take its derivative. And in the clock-arithmetic world there are extra variables around to take derivatives with.",
             visual="A curve with a tangent line sliding to flat: 'flat ⇔ derivative = 0'. In the parallel-universe panel, a polynomial in x with d/dx acting on it happily."),
        dict(text="Over the whole numbers, there's nothing to differentiate. What would it even mean to take the derivative of seventeen? Multiplicity, the engine of Stepanov's proof, has nowhere to live.",
             visual="In the whole-number panel: 'd/d? (17) = ???' — the derivative symbol bounces off the number 17. The 'multiplicity' engine graphic sputters/greys out."),
        dict(text="Alpöge's proof is a descendant of Stepanov's. Its central achievement is finding a substitute for multiplicity over the integers. And it gets there by a long road. So let's start at the destination, and work backwards.",
             visual="A roadmap graphic with four stations right-to-left: 'RH' ← 'a ceiling on the primes' ← 'divisibility vs size' ← 'multiplicity from symmetry (theta lifts)'. This roadmap is reused in s20 — keep it clean."),
    ]),
    # ------------------------------------------------------------------ ACT IV
    dict(id="s13", act="Act IV · The proof", title="The destination: a ceiling", beats=[
        dict(text="Here's the destination. Instead of counting each prime as one, weight each prime by its logarithm. With that weighting, the prediction becomes beautifully simple: the total up to X should be about X itself.",
             visual="Staircase where the step at prime p has height ln p (Chebyshev's function), drawn against the straight line y = x on [0, 100]: it hugs the diagonal."),
        dict(text="The whole proof boils down to one inequality. Show that this weighted count can't overshoot its prediction by more than about the square root of X. One side only. A ceiling, with no floor.",
             visual="Plot (weighted count − X). Draw a ceiling curve at +sqrt(X)-ish above it; region above the ceiling shaded 'forbidden'. No curve below. On-screen: 'weighted count ≤ X + (about) sqrt(X)'."),
        dict(text="Why is a ceiling enough? Remember, a zero off the line makes a loud wave. And waves go up as well as down. A classical argument going back to Edmund Landau shows that if any zero sat to the right of the line, its wave would eventually punch through that ceiling.",
             visual="A ghost zero to the right of the line (red). Its wave with growing envelope x^β: the crests rise faster than the ceiling and eventually break through it — flash at the break point. Caption 'Landau'."),
        dict(text="So a ceiling means no zeros to the right of the line. And the zeros come in mirror-image pairs across the line, so none on the left either. Every zero is trapped on the line. Everything now rests on building that ceiling.",
             visual="Critical strip: right half gets crossed out/shaded 'no zeros'. Mirror reflection across Re = 1/2 (show a pair ρ ↔ 1−ρ̄ reflecting): left half shaded too. Only the line remains glowing."),
    ]),
    dict(id="s14", act="Act IV · The proof", title="Divisibility versus size", beats=[
        dict(text="The ceiling comes from a very old idea: play a number's divisibility against its size. Here's the classic example, from Chebyshev in eighteen fifty.",
             visual="A balance scale: left pan 'divisibility', right pan 'size'. Caption 'Chebyshev, 1850'."),
        dict(text="Take twenty choose ten: the number of ways to pick ten things out of twenty. It equals one hundred eighty-four thousand, seven hundred fifty-six. Now factor it. Every prime between ten and twenty shows up: eleven, thirteen, seventeen, nineteen.",
             visual="C(20,10) = 184,756 = 2² · 11 · 13 · 17 · 19. The primes 11, 13, 17, 19 highlighted in the prime color."),
        dict(text="That's no accident. Those primes appear on top of the fraction and can't be cancelled by anything below. So the number is divisible by all of them. But it also can't be very big, since it's less than four to the tenth power.",
             visual="Write (20·19·18·…·11)/(10·9·…·1). Highlight 19, 17, 13, 11 on top; show the denominators cancelling other things but not these. Then '184,756 < 4^10 = 1,048,576'."),
        dict(text="A whole number that isn't zero is at least as big as anything that divides it. So the product of all those primes is trapped under a ceiling. A fact about divisibility, and a fact about size, squeeze out a fact about primes.",
             visual="'11 · 13 · 17 · 19 ≤ C(20,10) < 4^10'. Generalize: 'product of primes between n and 2n < 4^n'. Squeeze graphic: two walls closing in on the primes."),
        dict(text="Chebyshev's ceiling is crude. To reach the square root, you need a far more special number: one that is divisible by much, much more, while staying just as small. Building that number is what the rest of the proof is for.",
             visual="The scale again: we need a mystery number '?' — 'hugely divisible' on one side, 'still small' on the other. The '?' glows; it will be revealed in s16."),
    ]),
    dict(id="s15", act="Act IV · The proof", title="Theta functions", beats=[
        dict(text="The special number comes from objects called theta functions. Picture a perfectly regular grid of points, a lattice. A theta function is a kind of fingerprint of that lattice. It records how many grid points sit at each distance from the center.",
             visual="Square lattice Z². Expanding circle from the origin; each time it hits lattice points they flash and a tally is recorded: distance² 0:1, 1:4, 2:4, 4:4, 5:8, ... assembling θ = 1 + 4q + 4q² + 4q⁴ + 8q⁵ + ..."),
        dict(text="Because the lattice is so symmetric, its fingerprint is too. It satisfies an enormous number of hidden symmetries. Functions like this are called automorphic forms, and they are the main characters of modern number theory.",
             visual="A richly symmetric picture: a tessellation of the upper half-plane / Poincaré disk by the modular group (draw fundamental domains via Möbius images), gently animated to show the symmetry. Label 'automorphic form'."),
        dict(text="Theta functions can also be used as machines. Feed in a symmetric object living in one space, and the machine returns a new symmetric object living in a bigger space. This is called a theta lift.",
             visual="A machine box labelled θ. A small symmetric shape (on a small 'space' disc) enters; a bigger, richer symmetric shape on a larger disc comes out. Arrow label 'theta lift'."),
    ]),
    dict(id="s16", act="Act IV · The proof", title="Multiplicity from symmetry", beats=[
        dict(text="Here is the discovery at the heart of the proof. Each time you apply a theta lift, the result gains one extra order of vanishing. One lift behaves like one derivative.",
             visual="Side by side: left, Stepanov's flattening curve with multiplicity m ticking 1→2; right, one theta-lift arrow between two spaces. An equals-ish sign: 'one lift ≈ one order of multiplicity'."),
        dict(text="That's the missing ingredient. You can't differentiate a whole number. But you can lift. So instead of asking for multiplicity m directly, you build a chain. Lift, then lift again, and again, m times, climbing through a tower of bigger and bigger symmetric spaces.",
             visual="Tower builds upward: platforms U₀ → U₁ → U₂ → … → U_m connected by θ arrows, each platform slightly larger; a multiplicity counter increments with each floor. Camera pans up."),
        dict(text="At the top of the tower, you measure the final object, and out comes a single number. And this is the special number we wanted. Each lift along the way forced it to be divisible by more and more, while geometry keeps its size under control.",
             visual="At the top platform a beam condenses into one glowing number-token (the '?' from s14). Two gauges: 'divisibility' climbing with each floor; 'size' pinned low by a clamp labelled 'geometry'."),
        dict(text="Divisibility versus size, exactly as with Chebyshev. But now with multiplicity m built in. This is Stepanov's argument, rebuilt out of symmetry.",
             visual="The balance scale from s14 returns with the token on it. Banner: 'Stepanov's multiplicity, rebuilt from theta lifts'."),
    ]),
    dict(id="s17", act="Act IV · The proof", title="How tall is the tower?", beats=[
        dict(text="How long should the chain be? Suppose we're studying primes up to X. Every lift sharpens the estimate. With m lifts, one part of the error shrinks like X divided by m.",
             visual="Axes: horizontal 'number of lifts m', vertical 'error'. Draw the falling curve X/m (hyperbola), labelled."),
        dict(text="But every lift also has a cost. The spaces get bigger, the bookkeeping gets heavier, and a second error grows in proportion to m.",
             visual="Draw the rising line m on the same axes, labelled 'cost of lifting'."),
        dict(text="One error falls, the other rises. The total is smallest where they cross, and that happens when m is the square root of X. There, both errors are the size of the square root of X. Exactly the ceiling we need.",
             visual="Draw total = X/m + m; a dot slides to its minimum at m = sqrt(X); dashed lines to both axes labelled sqrt(X). 'X/m = m ⇒ m = sqrt(X)'."),
        dict(text="In his announcement, Alpöge singles out this moment. He had expected multiplicity to be nearly impossible to find. It was Claude that proposed a chain of theta lifts, of length square root of X. To study primes up to a trillion, a tower a million stories tall. As he put it: and yet, what else could it be?",
             visual="Quote card (paraphrase attribution, short quote only): “(And yet, what else could it be?)” — Levent Alpöge. Beside it the tower stretching up out of frame with label 'X = 10¹² → m ≈ 10⁶ lifts'."),
    ]),
    dict(id="s18", act="Act IV · The proof", title="The two-thirds wall", beats=[
        dict(text="It isn't that easy, of course. Do the accounting in the obvious way, paying the cost of each lift separately, and the argument stalls. The ceiling comes out at X to the power two thirds. Close. But two thirds is not one half, and the proof is worthless unless you reach one half.",
             visual="An exponent number line from 1 down to 1/2: marker slides from 1 (trivial) down and gets stuck at a wall at 2/3; the goal flag sits at 1/2. 'X^{2/3}' vs 'X^{1/2}'."),
        dict(text="The loss comes from waste. The chain is actually run many times over, once for each member of a large family of twists. Think of each run as a column of numbers. Charged one at a time, each column pays its own toll.",
             visual="Many towers side by side, shrinking into columns of a matrix (vertical vectors). Each column passes its own toll gate and a coin is deducted per column — a pile of wasted coins grows."),
        dict(text="The fix is to stop treating the columns separately. The proof places all of them inside one shared lattice, a single grid of whole-number points, so that their divisibility can be pooled. Then it shows the columns are nearly perpendicular to each other, so their sizes don't interfere.",
             visual="The columns become vectors drawn from a common origin on one shared lattice of dots; they snap to lattice points. Show the angles between vectors near 90° with small right-angle markers ('nearly perpendicular')."),
        dict(text="With everything on the same grid, the same quantity appears on both sides of the final comparison, and cancels. The waste is gone. Two thirds becomes one half.",
             visual="An inequality with a matching colored block on both sides ('same slope' term); the two blocks cancel with a strike-through. Back on the exponent line, the wall at 2/3 crumbles and the marker slides to 1/2."),
    ]),
    dict(id="s19", act="Act IV · The proof", title="The last leak", beats=[
        dict(text="One leak remains. Pooling divisibility across the family only works if certain hidden obstructions vanish. They're subtle objects that measure when something works one prime at a time, and yet fails globally.",
             visual="A pipe/vessel (the pooled lattice) with a few small leaks. Then a 'local vs global' picture: puzzle pieces that each fit their neighbours locally but the ring fails to close globally."),
        dict(text="Most of them can be killed by twisting. For the stubborn ones, the proof needs a statement related to a hundred-year-old open problem called Vandiver's conjecture. Not the full conjecture, but a weakened form, which the proof establishes along the way.",
             visual="Most leaks get plugged by a 'twist' motion. A few stubborn red ones remain, labelled; a plug labelled 'weak Vandiver' seals them."),
        dict(text="To get it, the argument climbs an infinite tower of number systems, each built from finer and finer roots of one. And it uses the deepest dictionary in number theory, the Langlands correspondence, which translates symmetric functions, like our theta lifts, into the language of symmetries of numbers themselves.",
             visual="First: unit circle with roots of unity — p points, then p² points, then p³ … stacked as a tower of circles (cyclotomic/Iwasawa tower). Then: a two-column dictionary, 'automorphic forms (symmetric functions)' ⇄ 'Galois representations (symmetries of numbers)', with a bridge labelled 'Langlands'."),
        dict(text="This is why the proof is so enormous. It doesn't dodge modern number theory. It uses nearly all of it.",
             visual="A constellation/map of named areas lighting up one after another and connecting to a center node 'GRH': theta lifts, unitary groups, trace formula, Arakelov geometry (slopes), Iwasawa theory, Galois representations, CM theory, étale cohomology, Shimura varieties."),
    ]),
    dict(id="s20", act="Act IV · The proof", title="The whole machine", beats=[
        dict(text="Let's put the machine together. Start with a tower of theta lifts, about square root of X stories high. Each story adds multiplicity.",
             visual="The roadmap from s12 returns, now filling in left to right. Station 1: compact tower icon with 'm ≈ sqrt(X) lifts'."),
        dict(text="At the top sits a number that is hugely divisible, yet small. Pool the divisibility on one shared lattice, and plug the last leak.",
             visual="Station 2: the glowing number token on the balance scale; small lattice icon and plug icon appear beneath."),
        dict(text="Divisibility against size gives the ceiling: the weighted count of primes never overshoots by more than about the square root of X.",
             visual="Station 3: mini plot of the prime wobble under a sqrt ceiling."),
        dict(text="Landau's argument turns the ceiling into a wall. No zeros to the right of the line. Symmetry takes care of the left. And the same machine, run with twists, handles every Dirichlet L-function. The generalized Riemann hypothesis.",
             visual="Station 4: critical strip with both halves shaded out and the line glowing; then it duplicates into several strips (the L-functions). Big title: 'Generalized Riemann Hypothesis ∎'."),
    ]),
    # ------------------------------------------------------------------ ACT V
    dict(id="s21", act="Act V · The proof as an object", title="Seventeen million lines", beats=[
        dict(text="The proof wasn't released as a paper. It was released as code, in a language called Lean, where every logical step must be justified to a small, trusted checking program.",
             visual="A page of a paper dissolves into code-like lines. A small box labelled 'kernel' with lines flowing through it one at a time, each stamped with a check."),
        dict(text="Seventeen million lines. A hundred and seventy-five thousand files. Within hours of the release, mathematicians around the world were compiling it. It passed Lean's own checker, and then one independent checker after another, each written by different people in different languages.",
             visual="Counters: '17,374,215 lines', '175,187 files'. Then a column of checker names getting check marks in turn: Lean kernel, nanoda, con-leche, con-agua, Pestka, nanoclo, tenet."),
        dict(text="And the final statement it proves is not something the authors wrote themselves. It's the definition of the Riemann hypothesis that was already sitting in Lean's public mathematics library.",
             visual="A code card (monospace) showing exactly:  theorem riemannHypothesis : RiemannHypothesis  — with 'RiemannHypothesis' linked by an arrow to a box labelled 'Mathlib (public library)'."),
        dict(text="A human-readable account is still being written. Alpöge himself expects the argument to become far shorter and simpler. The first proof of a great theorem is rarely the last.",
             visual="The huge wall of code slowly compresses/folds down into a slim booklet outline. Calm."),
    ]),
    dict(id="s22", act="Epilogue", title="In one breath", beats=[
        dict(text="So here's the whole story in one breath. The primes look random. Their randomness is controlled by the zeros of the zeta function. Riemann guessed that the zeros all lie on one line, which would make the primes exactly as orderly as coin flips.",
             visual="Fast visual recap, three vignettes in sequence: barcode of primes → zeros on the critical line emitting waves → error curve inside the sqrt envelope."),
        dict(text="The proof takes an idea that worked in a parallel universe, Stepanov's multiplicity, and rebuilds it for the whole numbers out of towers of symmetric functions. A number too divisible to be small, and too small to be that divisible, unless the primes behave.",
             visual="Vignettes: flattening curve (multiplicity) → tower of lifts → balance scale tipping level."),
        dict(text="For a hundred and sixty-seven years, this was the question mathematicians most wanted answered. Now the work of understanding the answer begins.",
             visual="Return to the opening number line of glowing primes; the critical line with its zeros fades in above it like a horizon. Hold, then fade to black. Small end credit: 'Proof: Levent Alpöge with Claude (Nov 2026). Explainer generated with Claude.'"),
    ]),
]


def beats():
    """Yield (key, scene, beat) for every beat, key like 's05c'."""
    for sc in SCENES:
        for i, b in enumerate(sc["beats"]):
            yield f'{sc["id"]}{chr(97 + i)}', sc, b


if __name__ == "__main__":
    import json, sys
    n = sum(len(b["text"].split()) for _, _, b in beats())
    print(f"{len(SCENES)} scenes, {sum(1 for _ in beats())} beats, {n} words (~{n/150:.1f} min)")
    if len(sys.argv) > 1:
        json.dump(SCENES, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
