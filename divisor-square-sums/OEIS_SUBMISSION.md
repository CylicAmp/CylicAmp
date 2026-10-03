# Draft OEIS submission (new sequence)

Submit at https://oeis.org/Submit.html after registering a free account at
https://oeis.org/wiki/Special:RequestAccount. Copy each field below into the
matching box on the form. Upload b_file_family_m.txt as the b-file.

NAME:
Even numbers m such that p = sigma_2(m)/m - m is a prime with p > m/2 and p not dividing m; then m*p is a term of A185584.

DATA:
60, 286650, 308700, 389844, 1441188, 36580068, 76698960, 826169400, 883146600, 3943157400, 5156436600, 8147739600, 8897460000, 20009220000, 26158532400, 65883636000, 112834965600, 243898340400, 286940530800, 377486756712, 526927170000, 611809800000

OFFSET:
1

COMMENTS:
For such m, the divisors of n = m*p that are <= m/2 are exactly the proper divisors of m (every divisor of n not dividing m is a multiple of p > m/2), so the sum of the squares of the first tau(m)-1 divisors of n is sigma_2(m) - m^2 = n. Hence m*p is in A185584.
There are exactly 587 terms <= 10^22 (exhaustive search; b-file). The corresponding n = m*p agree with every such term of A185584 listed up to 9335069854188787800.
Terms are divisible by 6, since sigma_2(m)/m^2 > 3/2 is required and the sum of 1/d^2 over divisors coprime to 2 or to 3 cannot exceed 3/2.

EXAMPLE:
m = 60: sigma_2(60) = 5460, 5460/60 - 60 = 31, which is prime, 31 > 30 and 31 does not divide 60. So 60*31 = 1860 = 1^2+2^2+3^2+4^2+5^2+6^2+10^2+12^2+15^2+20^2+30^2 is in A185584.

PROG:
(PARI) isok(m) = if(m%2 || sigma(m,2)%m, return(0)); my(p=sigma(m,2)/m-m); isprime(p) && 2*p>m && m%p

CROSSREFS:
Cf. A185584, A001157 (sigma_2).

KEYWORD:
nonn

AUTHOR:
Michael Song
