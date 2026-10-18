# CLASS: AUDIT
"""
Audit of the pasted text on 4+9=13 and "a fourth primary colour" (owner_work #341, 2026-10-18). Another tool's text, relayed by the owner.

RIGHT:
  4+9=13   13=1+3=4   13=1x9+4   4=2x2 (even)   9=3x3 (odd)   13 is prime   4 is in the orbit C3 (3, 4, 30)   (the owner's 7x7=4+9=(1+3=4), #267)
WRONG:
  "digital root 4 = 2^2 (even square preserved under modulo reduction)": no square is "preserved". The roots of squares are only 1, 4, 7, 9; 13's root happens to be 4,
  and 14 gives 5. "C3 (k = 2, even square 2^2)": C3 is the three numbers 3, 4, 30; there is no k.
  "Belsten and Olshausen": the paper has three authors, Belsten, Frady and Olshausen ("Emergence of unique hues from sparse coding of color in natural scenes").
  "The human visual cortex uses sparse coding": the paper fits a sparse-coding model to 503 calibrated natural images; its six basis vectors are the four unique hues plus
  black and white, and opposite hues exclude each other. It is a theoretical study; testing on people is listed as future work.
  "12 percent of women carry ... a fourth cone": 12 percent is Mollon's projection, not a measurement. Fourth-cone carriers are confirmed in many women, but behavioural
  tetrachromacy has been reported in only a handful (one clear case, cDa29, Jordan 2007). "100 million colours" is a theoretical maximum.
I CAN'T CHECK: the Aug/Sept 2026 date and issue of the journal paper (an arXiv preprint, 2603.24293, is the same paper; a Berkeley Vision post says it is in the Journal of the
  Optical Society of America); "millions of pixels" (the dataset confirmed is 503 images); how a colour pole maps to the 41-state diamond (no mapping is given).
DONE: the rows 312 and 231 recoloured on the opponent ring. Red 0, yellow 90, green 180, blue 270 degrees; rows 1, 4, 7 (labels 1, 2, 3) are red, green, blue; rows 2 and 3 at 60 and
  120 degrees (orange-yellow, yellow-green: the way from red to green goes through yellow); rows 5 and 6 at 210 and 240 degrees (teal, azure). tools/draw_123_rows.py,
  reference/rotation_rows_123_seven_colours.png.
Sources: https://arxiv.org/pdf/2603.24293v1  https://vision.berkeley.edu/posts/colors-that-stand-alone  https://hyperallergic.com/187012/how-many-colors-can-most-of-us-actually-see/
FALSIFICATION: any assertion failing.
"""


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


assert 4 + 9 == 13 and 1 + 3 == 4 and 13 == 1 * 9 + 4 and 4 == 2 * 2 and 9 == 3 * 3 and 13 % 2 == 1 and all(13 % d for d in range(2, 13))
assert 4 % 37 == 4 and 4 in (3, 4, 30) and 7 * 7 == 49 and dr(49) == 4
squares = {dr(n * n) for n in range(1, 500)}
assert squares == {1, 4, 7, 9} and dr(13) == 4 and dr(14) == 5 and dr(14) not in squares
assert (3, 4, 30) == tuple(sorted({3, 26 * 3 % 37, 26 * 26 * 3 % 37}))
assert 12 / 100 == 0.12

if __name__ == "__main__":
    print("4+9=13=1+3=4 right; the square 'preserved', k = 2, cortex and 12 percent claims wrong; rows 312 and 231 recoloured on the red-yellow-green-blue ring")
