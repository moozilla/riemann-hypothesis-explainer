# How the proof works

A plain-language outline of Levent Alpöge's November 2026 proof of the Riemann Hypothesis, as described in his [remark](https://alpo.ge/remark.pdf) and in the reconstruction effort on the Lean Zulip linked from [Terence Tao's post](https://terrytao.wordpress.com/2026/11/20/unforced-euler-singularity-unforced-navier-stokes-singularity-and-the-generalized-riemann-hypothesis/). This is the same story the [video](assets/riemann_hypothesis_explainer.mp4) tells, without the pictures. It takes the proof as presented.

## 1. What the hypothesis says

The primes thin out in a predictable way: the number of primes below x is close to a smooth curve. What is left over is a wobble around that curve, and the Riemann Hypothesis is a statement about how big the wobble can get.

The zeta function packages every prime into one function. Its zeros, the inputs where it outputs exactly zero, each contribute one wave to the wobble. How far right a zero sits decides how loud its wave is. If every zero sits on the vertical line with real part 1/2, then every wave is as quiet as it can possibly be, and the prime count is off by only about √x. That is the size of error you get from flipping x coins.

So the hypothesis, "all the zeros are on the line", is the same statement as "the primes are as evenly spread as randomness allows".

The generalized version says the same thing for Dirichlet L-functions, the cousins of zeta that track primes by their remainders (primes ending in 1, 3, 7 or 9, for instance).

## 2. The destination: a ceiling

Weight each prime by its logarithm. Then the predicted total up to X is simply X.

The whole proof reduces to one inequality: this weighted count never overshoots X by more than about √X. Only one side is needed, a ceiling with no floor.

A ceiling is enough because of a classical argument going back to Landau. A zero to the right of the line would make a wave that swings up as well as down, and eventually it would break through the ceiling. So a ceiling means no zeros right of the line. The zeros come in mirror-image pairs across the line, so there are none on the left either.

## 3. The clue from a parallel universe

There is a setting where the analogue of the hypothesis has been a theorem for decades: counting points on curves over finite fields. Weil proved it in the 1940s.

In 1969 Stepanov found a much more elementary proof. Build a helper polynomial that vanishes at every point you are counting, and vanishes there to high multiplicity (the graph doesn't just cross zero, it flattens against it m times over). A polynomial of degree d has at most d zeros counted with multiplicity, so

    (number of points) × (multiplicity) ≤ degree.

Keep the degree low and the multiplicity high and you get the square-root bound.

## 4. Why it doesn't cross over

Multiplicity is defined with derivatives. Over the integers there is nothing to differentiate: a whole number is just a number. People have known for fifty years that an integer version of Stepanov's trick would be decisive, and nobody could find where the multiplicity would come from.

## 5. Divisibility versus size

The integer substitute for "few zeros" is an old idea from Chebyshev. Take 20 choose 10 = 184,756. Every prime between 10 and 20 divides it, because those primes appear on top of the fraction and nothing below can cancel them. But the number is also smaller than 4¹⁰. A non-zero whole number is at least as big as anything dividing it, so the product of those primes is trapped under a ceiling.

A fact about divisibility and a fact about size squeeze out a fact about primes. Chebyshev's version is crude. To reach √X you need a number that is divisible by far more while staying just as small.

## 6. Theta lifts supply the multiplicity

A theta function is a fingerprint of a lattice (a regular grid of points): it records how many grid points sit at each distance from the centre. Because lattices are so symmetric, theta functions are too. They are examples of automorphic forms.

Theta functions also work as machines. Feed in a symmetric object living on one space and you get back a symmetric object living on a bigger space. This is a theta lift.

The discovery at the heart of the proof is that **each theta lift gains one order of vanishing**. One lift behaves like one derivative. So instead of differentiating m times, you lift m times, climbing a tower of bigger and bigger symmetry groups (totally definite unitary groups, in the technical statement).

At the top of the tower you measure the final object and get a single number. Each lift along the way forced that number to be more divisible, while geometry keeps its size under control. That is Stepanov's argument rebuilt out of symmetry, feeding Chebyshev's squeeze.

## 7. How tall is the tower?

For primes up to X, with m lifts:

- one part of the error shrinks like X / m,
- another grows like m, because the spaces get bigger.

They balance at m ≈ √X, where both are about √X. That is exactly the ceiling.

Alpöge singles this step out in his remark. He had expected multiplicity to be nearly impossible to find, and it was Claude that proposed a chain of theta lifts of length about √X. For primes up to a trillion, that is a tower a million storeys tall. His comment: "And yet, what else could it be?"

## 8. The two-thirds wall

Done naively, the accounting stalls. If you pay the cost of each lift separately, the ceiling comes out at X^(2/3) instead of X^(1/2), which proves nothing.

The loss is waste. The chain is run many times, once per member of a large family of twists (Hecke characters). Think of each run as a column of numbers. Charged one at a time, every column pays its own toll.

The fix:

1. Put all the columns inside one shared integral lattice, so their divisibility is pooled.
2. Show the columns are nearly perpendicular to each other, so their sizes don't interfere.
3. Then the same quantity (the slope of the dual lattice) appears on both sides of the final comparison and cancels.

The technical tool for comparing divisibility with size here is Bost's slope inequality. With the waste gone, two-thirds becomes one-half.

## 9. The last leak

Pooling divisibility across the family only works if certain hidden obstructions vanish. These are Galois cohomology classes: objects that measure when something works one prime at a time yet fails globally.

Most can be killed by twisting. The stubborn ones need a statement related to Vandiver's conjecture, a century-old open problem. The proof doesn't need the full conjecture, only a weakened form, and it establishes that along the way. To do so it climbs an infinite tower of cyclotomic fields (Iwasawa theory) and uses Galois representations attached to automorphic forms, which is the Langlands correspondence at work.

This is why the proof is so large. It doesn't avoid modern number theory. It uses most of it.

## 10. The whole machine

1. Build a tower of about √X theta lifts. Each storey adds multiplicity.
2. At the top sits a number that is hugely divisible yet small.
3. Pool the divisibility on one shared lattice and plug the last leak.
4. Divisibility versus size gives the ceiling: the weighted prime count never overshoots by more than about √X.
5. Landau's argument turns the ceiling into "no zeros right of the line", and symmetry handles the left.
6. Run with twists, the same machine handles every Dirichlet L-function.

## 11. The proof as an object

The proof exists as Lean code: 17,374,215 lines in 175,187 files. It proves the statement named `RiemannHypothesis` in Mathlib, Lean's standard mathematics library, so there is no ambiguity about what was proved. It has been accepted by Lean's own kernel and by several independent checkers written by different people (nanoda among them).

Nobody has read all of it. What is written above is the outline that the author's remark and the people digging through the Lean source have pieced together so far.
