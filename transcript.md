# Transcript
Full narration of the video, scene by scene. Generated from [script.py](script.py).

## Prologue

### 01. Static, or music?

This is a list of the prime numbers. Two, three, five, seven, eleven. Numbers that can't be broken into smaller pieces.

They are the atoms of arithmetic. Every whole number is built by multiplying primes together, in exactly one way.

And yet nobody can tell you where the next one will be. They show up like static. No formula. No rhythm anyone can hear.

In eighteen fifty-nine, Bernhard Riemann guessed that there is a rhythm after all. That the static is actually music, and that every note is tuned in a very precise way. For a hundred and sixty-seven years, nobody could prove it.

In November twenty twenty-six, the mathematician Levent Alpöge, working with the AI model Claude, published a proof. Seventeen million lines of it, checked line by line by a computer. This video is about what the Riemann hypothesis says, and how that proof works.

## Act I · The primes

### 02. The sieve

Let's start from the ground. Write down the whole numbers. Cross out every multiple of two. Then every multiple of three. Then five. Then seven. Whatever survives is prime.

Look at the survivors. Sometimes two of them sit side by side, like eleven and thirteen. Sometimes there are long deserts with none at all. Up close, there's no pattern.

So let's stop asking where the primes are, and ask an easier question. How many are there?

### 03. Counting primes

Walk along the number line, and every time you step on a prime, climb one stair. Mathematicians call this staircase pi of x: the number of primes up to x.

Up close it's jagged. Now zoom out. To a thousand. To a million. The stairs melt into a smooth curve.

As a teenager, Gauss noticed what that curve is. Near a number x, about one in every natural log of x numbers is prime. Near a million, that's about one in fourteen. Near a trillion, one in twenty-eight. Primes thin out, slowly and predictably.

Add up those odds and you get a prediction for the staircase. In eighteen ninety-six this was proved: the prediction and the truth agree, in the long run. That's the prime number theorem.

### 04. The wobble

But 'in the long run' hides the interesting part. Subtract the prediction from the truth, and you're left with the error. A wobble.

How big can the wobble get? Here's a comparison. Flip a coin a million times. You expect half a million heads, but you'll miss by a bit. Typically by about a thousand, which is the square root of a million. Square-root-sized error is the signature of pure randomness.

The Riemann hypothesis says the primes behave exactly like that. Count the primes up to x, and the prediction is off by about the square root of x, and never much more. The primes are as orderly as a random thing can possibly be.

To see why anyone would believe that, we need one of the strangest objects in mathematics.

## Act II · The zeta function

### 05. One function that knows every prime

Take the whole numbers, raise each to some power s, flip them over, and add them all up. One, plus one over two to the s, plus one over three to the s, and on forever. This is the zeta function.

When s is two, the sum settles down to a famous value, pi squared over six. Different inputs s, different outputs.

On its face, this has nothing to do with primes. Then Euler found something astonishing. The very same function can be written as a product, with one factor for each prime, and nothing else.

Why? Because every whole number is a unique product of primes. Multiply these brackets out, and every number appears exactly once. So zeta is a single function that knows about all the primes at once. Whatever the primes are doing, it's encoded in here.

### 06. Numbers that spin

Riemann's leap was to feed this function a new kind of input: complex numbers. Don't let the name scare you. A complex number is just a point on a plane, instead of a point on a line. It has a left-right part, and an up-down part.

What does it mean to raise a number to a complex power? Picture an arrow. The left-right part of s sets the arrow's length. The up-down part sets its angle, how far it has been spun around.

So each term of zeta becomes a little arrow, and adding them means laying them tip to tail. The sum traces out a spiral, and where the spiral ends up, that's the value of zeta.

Change the input and the whole spiral changes shape. And for certain very special inputs, something remarkable happens.

### 07. The zeros and the line

The spiral curls back and lands exactly on zero. Every arrow cancelled by the others. An input like this is called a zero of the zeta function.

Where are they? There are some boring ones off to the left that everyone understands. The interesting ones all live in this narrow strip, between zero and one. The critical strip.

Riemann computed the first few. And they weren't scattered around the strip. They were lined up, dead center, on the line where the left-right part is exactly one half.

His guess: all of them are on that line. Every single one, forever. That's the Riemann hypothesis. Computers have since checked trillions of zeros. All on the line. But trillions is not all.

### 08. The music of the primes

Why should the position of these dots matter to anyone? Because Riemann found an exact formula connecting zeros to primes. Each zero contributes one wave to the prime staircase.

Start with the smooth prediction. Add the wave from the first zero. Then the second. Then ten of them. A hundred. The smooth curve grows stairs, and the stairs land exactly on the primes. The zeros are the notes, and the primes are the music.

Each zero's two coordinates do different jobs. Its height sets the pitch of the wave. Its left-right position sets the volume: how fast the wave grows as you move along the number line.

A zero on the center line makes a wave that grows like the square root of x. That's the coin-flip size. A zero to the right of the line would be louder than that, a wave big enough to break the square-root rule. So 'all zeros on the line' and 'the primes have square-root error' are the same statement. That's the hypothesis, in two languages.

### 09. The generalized hypothesis

The proof actually establishes something bigger. Sort the primes by their last digit. Apart from two and five, every prime ends in one, three, seven, or nine. Do the four teams get an equal share?

In the long run, yes. But how evenly? To study that, you build cousins of the zeta function, called Dirichlet L-functions. Same sum, except each term gets a twist, a little rotation that depends on the number's remainder.

Each of these cousins has its own zeros, and its own critical line. The generalized Riemann hypothesis says: all of their zeros are on the line too. For every one of these functions, all at once. This is the statement that was proved.

## Act III · The clue

### 10. A parallel universe

For a century and a half, this problem defeated everyone who touched it. But there was one clue. A parallel universe where the Riemann hypothesis is true, and we know why.

In that universe, you swap the whole numbers for clock arithmetic. Numbers that wrap around, like hours on a clock with a prime number of hours. In this world, you count solutions to equations, points on curves, instead of counting primes.

These curves have their own zeta functions, with their own zeros and their own critical line. And in the nineteen forties, André Weil proved that every one of those zeros is on the line. The number of points on a curve is always within a square root of the prediction.

So the square-root law is real, somewhere. The question was always how to carry the proof across to the ordinary whole numbers.

### 11. Stepanov's trick

In nineteen sixty-nine, Sergei Stepanov found a new proof of Weil's theorem that needed almost no machinery. Just one humble fact: a polynomial of degree d can equal zero at most d times.

Here is the trick. Suppose you want to show a curve doesn't have too many points. Build a helper polynomial that equals zero at every one of those points. Then the number of points is at most its degree.

That alone is too weak. So Stepanov did something clever. He made the helper vanish at each point not once, but many times over. Not just touching zero, but flat there. Flat to order m. That's called multiplicity.

Now each point uses up m of the polynomial's zeros, instead of one. So the number of points, times m, is at most the degree. Crank up the multiplicity, and the bound gets sharper and sharper, all the way down to the square-root law.

### 12. Why it doesn't cross over

So why not just do that for the ordinary primes? Because of how you measure flatness. To check that a function is flat, you take its derivative. And in the clock-arithmetic world there are extra variables around to take derivatives with.

Over the whole numbers, there's nothing to differentiate. What would it even mean to take the derivative of seventeen? Multiplicity, the engine of Stepanov's proof, has nowhere to live.

Alpöge's proof is a descendant of Stepanov's. Its central achievement is finding a substitute for multiplicity over the integers. And it gets there by a long road. So let's start at the destination, and work backwards.

## Act IV · The proof

### 13. The destination: a ceiling

Here's the destination. Instead of counting each prime as one, weight each prime by its logarithm. With that weighting, the prediction becomes beautifully simple: the total up to X should be about X itself.

The whole proof boils down to one inequality. Show that this weighted count can't overshoot its prediction by more than about the square root of X. One side only. A ceiling, with no floor.

Why is a ceiling enough? Remember, a zero off the line makes a loud wave. And waves go up as well as down. A classical argument going back to Edmund Landau shows that if any zero sat to the right of the line, its wave would eventually punch through that ceiling.

So a ceiling means no zeros to the right of the line. And the zeros come in mirror-image pairs across the line, so none on the left either. Every zero is trapped on the line. Everything now rests on building that ceiling.

### 14. Divisibility versus size

The ceiling comes from a very old idea: play a number's divisibility against its size. Here's the classic example, from Chebyshev in eighteen fifty.

Take twenty choose ten: the number of ways to pick ten things out of twenty. It equals one hundred eighty-four thousand, seven hundred fifty-six. Now factor it. Every prime between ten and twenty shows up: eleven, thirteen, seventeen, nineteen.

That's no accident. Those primes appear on top of the fraction and can't be cancelled by anything below. So the number is divisible by all of them. But it also can't be very big, since it's less than four to the tenth power.

A whole number that isn't zero is at least as big as anything that divides it. So the product of all those primes is trapped under a ceiling. A fact about divisibility, and a fact about size, squeeze out a fact about primes.

Chebyshev's ceiling is crude. To reach the square root, you need a far more special number: one that is divisible by much, much more, while staying just as small. Building that number is what the rest of the proof is for.

### 15. Theta functions

The special number comes from objects called theta functions. Picture a perfectly regular grid of points, a lattice. A theta function is a kind of fingerprint of that lattice. It records how many grid points sit at each distance from the center.

Because the lattice is so symmetric, its fingerprint is too. It satisfies an enormous number of hidden symmetries. Functions like this are called automorphic forms, and they are the main characters of modern number theory.

Theta functions can also be used as machines. Feed in a symmetric object living in one space, and the machine returns a new symmetric object living in a bigger space. This is called a theta lift.

### 16. Multiplicity from symmetry

Here is the discovery at the heart of the proof. Each time you apply a theta lift, the result gains one extra order of vanishing. One lift behaves like one derivative.

That's the missing ingredient. You can't differentiate a whole number. But you can lift. So instead of asking for multiplicity m directly, you build a chain. Lift, then lift again, and again, m times, climbing through a tower of bigger and bigger symmetric spaces.

At the top of the tower, you measure the final object, and out comes a single number. And this is the special number we wanted. Each lift along the way forced it to be divisible by more and more, while geometry keeps its size under control.

Divisibility versus size, exactly as with Chebyshev. But now with multiplicity m built in. This is Stepanov's argument, rebuilt out of symmetry.

### 17. How tall is the tower?

How long should the chain be? Suppose we're studying primes up to X. Every lift sharpens the estimate. With m lifts, one part of the error shrinks like X divided by m.

But every lift also has a cost. The spaces get bigger, the bookkeeping gets heavier, and a second error grows in proportion to m.

One error falls, the other rises. The total is smallest where they cross, and that happens when m is the square root of X. There, both errors are the size of the square root of X. Exactly the ceiling we need.

In his announcement, Alpöge singles out this moment. He had expected multiplicity to be nearly impossible to find. It was Claude that proposed a chain of theta lifts, of length square root of X. To study primes up to a trillion, a tower a million stories tall. As he put it: and yet, what else could it be?

### 18. The two-thirds wall

It isn't that easy, of course. Do the accounting in the obvious way, paying the cost of each lift separately, and the argument stalls. The ceiling comes out at X to the power two thirds. Close. But two thirds is not one half, and the proof is worthless unless you reach one half.

The loss comes from waste. The chain is actually run many times over, once for each member of a large family of twists. Think of each run as a column of numbers. Charged one at a time, each column pays its own toll.

The fix is to stop treating the columns separately. The proof places all of them inside one shared lattice, a single grid of whole-number points, so that their divisibility can be pooled. Then it shows the columns are nearly perpendicular to each other, so their sizes don't interfere.

With everything on the same grid, the same quantity appears on both sides of the final comparison, and cancels. The waste is gone. Two thirds becomes one half.

### 19. The last leak

One leak remains. Pooling divisibility across the family only works if certain hidden obstructions vanish. They're subtle objects that measure when something works one prime at a time, and yet fails globally.

Most of them can be killed by twisting. For the stubborn ones, the proof needs a statement related to a hundred-year-old open problem called Vandiver's conjecture. Not the full conjecture, but a weakened form, which the proof establishes along the way.

To get it, the argument climbs an infinite tower of number systems, each built from finer and finer roots of one. And it uses the deepest dictionary in number theory, the Langlands correspondence, which translates symmetric functions, like our theta lifts, into the language of symmetries of numbers themselves.

This is why the proof is so enormous. It doesn't dodge modern number theory. It uses nearly all of it.

### 20. The whole machine

Let's put the machine together. Start with a tower of theta lifts, about square root of X stories high. Each story adds multiplicity.

At the top sits a number that is hugely divisible, yet small. Pool the divisibility on one shared lattice, and plug the last leak.

Divisibility against size gives the ceiling: the weighted count of primes never overshoots by more than about the square root of X.

Landau's argument turns the ceiling into a wall. No zeros to the right of the line. Symmetry takes care of the left. And the same machine, run with twists, handles every Dirichlet L-function. The generalized Riemann hypothesis.

## Act V · The proof as an object

### 21. Seventeen million lines

The proof wasn't released as a paper. It was released as code, in a language called Lean, where every logical step must be justified to a small, trusted checking program.

Seventeen million lines. A hundred and seventy-five thousand files. Within hours of the release, mathematicians around the world were compiling it. It passed Lean's own checker, and then one independent checker after another, each written by different people in different languages.

And the final statement it proves is not something the authors wrote themselves. It's the definition of the Riemann hypothesis that was already sitting in Lean's public mathematics library.

A human-readable account is still being written. Alpöge himself expects the argument to become far shorter and simpler. The first proof of a great theorem is rarely the last.

## Epilogue

### 22. In one breath

So here's the whole story in one breath. The primes look random. Their randomness is controlled by the zeros of the zeta function. Riemann guessed that the zeros all lie on one line, which would make the primes exactly as orderly as coin flips.

The proof takes an idea that worked in a parallel universe, Stepanov's multiplicity, and rebuilds it for the whole numbers out of towers of symmetric functions. A number too divisible to be small, and too small to be that divisible, unless the primes behave.

For a hundred and sixty-seven years, this was the question mathematicians most wanted answered. Now the work of understanding the answer begins.
