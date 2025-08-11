# MATLAB Simulator for Wolfram's ECA and reversible ECA

## Overview

This MATLAB program simulates Wolfram's elementary cellular automata (ECA) using a hardcoded rule (e.g., Rule 37) on a grid of specified width (e.g., 2400 cells) over a set number of generations (e.g., 1799).

The program supports periodic boundary conditions (ECA on a cylinder). This is the choice that makes more sense for a finite grid. If you don't want to see periodic boundary condition effects, just make the width of the grid big enough.

The program includes user prompts for:

- Enabling reversible mode.
- Choosing forward or backward simulation (backward requires reversible mode).
- Loading the initial state from a file (`cells.txt`) or using a hardcoded array of live cell positions.

The simulation computes the evolution step by step, displays the result as an image (black for live cells, white for dead), saves the grid as a PNG file without borders or legends, and writes the final state(s) to `cells.txt` for future use. In reversible mode, it saves both the second-to-last and last states; otherwise, only the last state.

## Reversible Elementary Cellular Automata

Reversible ECA (ECAR), as explored in Stephen Wolfram's *A New Kind of Science* ([NKS](https://www.wolframscience.com/nks/)), extend standard ECA by making the evolution invertible through a second-order rule. This incorporates the state from two time steps prior, allowing the system to run backward deterministically without information loss. Reversible elementary cellular automata are indicated bby appending R to the corresponding elementary cellular automata.

Wolfram suggests that the reversible ECA 37R could be universal (like 110), that is, able to compute all that can be computed.

### Computation

For a given ECA rule _R_, the next state _a_<sub>t+1</sub>(_i_) at position _i_ and time _t_+1 is computed as:

_a_<sub>t+1</sub>(_i_) = _R_(_a_<sub>t</sub>(_i_-1), _a_<sub>t</sub>(_i_), _a_<sub>t</sub>(_i_+1)) XOR _a_<sub>t-1</sub>(_i_)

where XOR denotes the exclusive or operation, and _a_<sub>t-1</sub> is the state from the previous step (initially all zeros for the first step in forward simulation). Backward computation reverses this to recover earlier states.

## Development

I had previously written a Java version of this program but I decided to restart from scratch in MATLAB with AI assistance from Grok. Grok 4 did a great job and always interpreted my prompts correctly despite possible ambiguities. Of course I checked the results against those of my previous code. This has been my first experiment with vibe coding and I'm quite pleased.

## Examples

Images included in this repository (the one-dimensional space of cells runs horizontally and time runs vertically):

### run1.png

Run 1: reversible ECA 37R running in the forward direction on a grid 2400 cells wide, starting with the initial state hardcoded in the program and running for 1799 steps so that the final image is 2400 x 1800 pixels.

### run2.png

Run 2: backward run after Run 1, with the initial state loaded from `cells.txt`. If you flip Figure 2 vertically it is identical to Figure 1.

### run3.png

Run 3: Run 1 for 899 steps; Edit `cells.txt` to flip (add) cell 865; Run backward to the beginning with the initial state loaded from `cells.txt`. Run backward again (twice backward is forward) for 1799 steps with the initial state loaded from `cells.txt`.. Compare to Run 1. Note how the cell flip propagates gradually in both directions.

### run4.png

Run 4: Run 1 for 899 steps; Edit `cells.txt` to flip (remove) cell 873; Run backward to the beginning with the initial state loaded from `cells.txt`. Run backward again (twice backward is forward) for 1799 steps with the initial state loaded from `cells.txt`.. Compare to Run 1. Note how the cell flip propagates gradually in both directions.

## Metaphysical musings

I have these pictures in mind when I think about free will as outlined in my book [*Irrational mechanics*](https://www.turingchurch.com/p/irrational-mechanics). Excerpts:

> I have a little program that computes Wolfram’s elementary CA and their reversible extensions. I have spent many happy hours playing with these CA, and in particular with Rule 37R, a reversible extension of elementary Rule 37. Rule 37R seems complex like Rule 110, and Wolfram thinks that Rule 37R could be universal like Rule 110.
> 
> Watching the complex behavior of those bits as time goes downward is really something. Rule 37R is deterministic, reversible, complex, and (perhaps) universal. Like in Rule 110, in Rule 37R there are particle-like gliders that propagate and collide, in a way that reminds of the Feynman diagrams of particle physics.
> 
> This seems the simplest toy model for some aspects of the deterministic and reversible world of Laplacian determinism where information is conserved.
> 
> ...discussions on free will follow...
> 
> You may be thinking that this sounds very weird because it seems to imply that, by acting with free will now, you not only determine the future but also change the past. In fact, playing with Rule 37R in my little CA program, I find it fascinating to watch how changes in the present gradually propagate toward both the future and the past. I start my deterministic and reversible Rule 37R CA program with some initial conditions at time zero, and let the program run for a while. Then I stop the program, choose a set of bits to represent me, and flip one of those bits to represent my free will. Then I run the program in the reverse time direction until reaching time zero: the initial conditions have changed to be compatible with my free choice at a later time.

This little program is not our universe. But according to Wolfram’s principle of computational equivalence ([NKS](https://www.wolframscience.com/nks/), Chapter 12) - all sufficiently powerful computing systems are equivalent to each other in the sense that they can emulate each other - running this little program with a certain (huge) initial string of bits (cells) would eventually encode (likely in a very scrambled holographic format that mixes times and places) all that happened or will happen in our universe, including the fact that you are reading this page now.

If Rule 37R is universal and consciousness is computable, a big version of this program, starting with a certain inconceivably huge but finite string of initial bits, would eventually result in a complex universe inhabited by conscious beings.

Let’s think of those conscious beings. They are huge strings of bits (since their entire universe is a huger string of bits, they can’t be anything else). Imagine two 37R beings as huge and ultra-complex versions of the two main trunks in the images above. These two 37R beings interact by exchanging gliders.

Suppose the left trunk encodes me. I'm a conscious being endowed with free will. In Runs 3 and 4, I make a free choice.

The effects of this choice “take time,” so to speak, to propagate toward the future and the past. The bit flip in the left trunk doesn’t affect the right trunk until a certain time difference in the past or in the future. In fact, you can see that the change in the left trunk is propagating to the right trunk only near the top and the bottom of Runs 3 and 4.

Interestingly, my choice here and now changes me but doesn't change the rest of the world at this time. Change gradually propagates toward both the future and the past.

Of course my words can only be imprecise, because human languages presuppose our usual conception of time. I could as well say that, given the bit flip, the new past has always been the real past.
