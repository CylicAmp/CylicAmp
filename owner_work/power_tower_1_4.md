# Power tower of x = 1/4 -- every direction

## The owner's request (owner_work #257, 2026-10-13)

"Do all that this algorithm can do in every direction allowed to go by numbers" -- with a
recursive-loop script and its output on x = 1/4 (the full message, code and output, is #257 in
owner_work/messages/2026-10-13.txt).

## Built: `power_tower.py` (exact, 80 digits; digits cut and TRUNCATED, never rounded)

```
python3 power_tower.py                 # x = 1/4
python3 power_tower.py 1/27            # any x
```

## The run, x = 1/4

```
POWER TOWER of x = 1/4   (exact, 80 digits; digits cut at 15, truncated)

1. UP THE TOWER
height           value (22 digits)  digits            sum root
     1                        0.25  250000000000000     7  7
     2    0.7071067811865475244008  707106781186547    68  5
     3    0.3752142272464817736731  375214227246481    58  4
     4    0.5944269971524200924813  594426997152420    69  6
     5    0.4386511651252167584245  438651165125216    56  2
     6    0.5443844148639168907358  544384414863916    70  7
     7    0.4701624317068808897322  470162431706880    57  3
     8    0.5211155233735903816839  521115523373590    52  7
     9    0.4855759768414804739448  485575976841480    81  9
    10    0.5100986000134083165053  510098600013408    45  9
    11    0.4930489534482800092827  493048953448280    71  8
    12    0.5048413871357765137547  504841387135776    69  6
    13    0.4966554423575199517724  496655442357519    75  3
    14    0.5023236533949581194402  502323653394958    67  4
    15    0.4983919575586891021593  498391957558689    96  6
    16    0.5011158533637317893259  501115853363731    52  7
    17    0.4992271473045155327099  499227147304515    63  9
    18    0.5005359877445836865822  500535987744583    73  1
    19    0.4996286195977644318119  499628619597764    92  2
    20    0.5002574875558131433604  500257487555813    65  2
    21     0.499821555076827680758  499821555076827    78  6
    22    0.5001237038955123651418  500123703895512    51  6
    23    0.4999142623453871857172  499914262345387    76  4
    24    0.5000594323454865067209  500059432345486    58  4
    25    0.4999588063343032656046  499958806334303    74  2
    26     0.500028554088539552468  500028554088539    62  8
    27    0.4999802082057608066673  499980208205760    69  6
    28    0.5000137188145775502952  500013718814577    57  3
    29    0.4999904909327784522191  499990490932778    89  8
    30    0.5000065912265782568455  500006591226578    56  2

2. TO THE LIMIT
  limit t = 0.5   (t = x^t: 0.0)
  contraction at t: t*ln(x) = ln(t) = -0.693147180559945309   (alternates above/below)
  error ratios, heights 30-34: -0.6931517492, -0.6931440138, -0.6931493756, -0.6931456591, -0.6931482352
  first height within 10^-15 of the limit: 92
  roots from that height on, at the 15-digit cut: [5, 4, 5, 4, 5, 4, 5]

3. ACROSS x: towers whose limit is t have x = t^(1/t); contraction = ln t; converge iff 1/e < t < e
  t = 1/2: x = t^(1/t) =             0.25   ln t = -0.69314718   tower converges to 0.5
  t =   2: x = t^(1/t) =  1.4142135623731   ln t =  0.69314718   tower converges to 2.0
  t = 1/3: x = t^(1/t) = 0.037037037037037   ln t =  -1.0986123   tower does not converge (2-cycle)
  t =   3: x = t^(1/t) =  1.4422495703074   ln t =   1.0986123   tower converges to 2.47805268029  (not to t = 3: that root repels, |ln t| > 1)
  t = 1/e: x = t^(1/t) = 0.065988035845313   ln t =        -1.0   tower converges to 0.367879441171  (on the edge: converges, slowly)
  t =   e: x = t^(1/t) =  1.4446678610098   ln t =         1.0   tower converges to 2.71828182846  (on the edge: converges, slowly)
```

## What the numbers do

- **Up:** height 1 = 1/4, height 2 = 1/sqrt2, height 3 = 2^-sqrt2 (exact); the heights swing
  above and below 1/2 -- odd heights below, even heights above.
- **To the limit:** the tower converges to t = 1/2 exactly (1/4^(1/2) = 1/2). Each step shrinks the
  distance to 1/2 by the factor ln(1/2) = -ln 2 = -0.6931... (the minus sign is the swinging).
  From height 92 on, every height agrees with 1/2 to 15 digits.
- **The digital roots never settle:** at a 15-digit cut they end up alternating 5 (even heights,
  0.5000...) and 4 (odd heights, 0.4999...) forever. They do not lock to 5.
- **Across x:** every converging tower has limit t with x = t^(1/t), and the shrink factor there is
  exactly ln t (general: d/dt x^t = t ln x = ln t at the limit). So towers converge exactly for
  e^-e <= x <= e^(1/e) (Euler). 1/4 and sqrt2 are a matched pair: limits 1/2 and 2, shrink
  factors -ln 2 and +ln 2. And 1/4 is the only (1/n)^n whose tower converges: it needs
  ln n <= 1, so n <= e, so n = 2.

## Corrections to the pasted output (checked exactly)

1. Height 2 printed root 5 in one table (digits 707106781186547, sum 68) and root 6 in another
   (sum 69): the same number. 68 -> 5 is right; 69 came from the computer rounding 0.25**0.25 up.
2. Height 3: the true 15 digits are 375214227246481 -> 58 -> 4. The printed list ended in a
   rounded 2 (...482 -> 59 -> 5).
3. The first "convergence check" started at t = 0.5, which is already the limit (0.25^0.5 = 0.5),
   so it could not show convergence; the tower run from 1/4 does.
4. "height 100: 0.500000000000000, root 5" is rounding: height 100 is 0.50000000000000004750...
   (root 5) but height 99 is 0.49999999999999993146... (root 4). The roots alternate 5, 4 forever.
5. "THE 7s, 9s, 12s, 21s": digital roots are 1-9, so 12 and 21 cannot occur; the list also marks
   6, 3 and 1.
