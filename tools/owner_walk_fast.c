/*
 * The owner's walk (tools/owner_engine.py) in C, for ten trillion and more.
 *
 * At each n: predict from n's place in 1 2 3 (place 3, or n = 2); act with the neighbours, behind + yourself = 2n - 1
 * and yourself + right = 2n + 1; verify that both are prime. As in tools/owner_walk_parallel.py, 2n - 1 is odd number
 * n - 1 and 2n + 1 is odd number n (the k-th odd number is 2k + 1): one table "is 2k + 1 prime?", read two neighbouring
 * entries at a time. Same pieces, same pattern for 3 5 7 11 13 17, same counts -- only the language is faster.
 *
 *   gcc -O3 -march=native -fopenmp -o owner_walk_fast tools/owner_walk_fast.c -lm
 *   ./owner_walk_fast N [threads]          prints one JSON line
 */
#include <math.h>
#include <omp.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SEG (1u << 23)               /* odd numbers per piece */
#define PERIOD 255255u               /* 3 x 5 x 7 x 11 x 13 x 17 */
#define NMARK 20
#define SUB (1u << 19)               /* sub-piece for the small primes: half the core's 1 MB cache */

typedef unsigned long long u64;

static u64 *base; static size_t nbase, nsmall;
static unsigned char *pat;           /* pat[k] = 0 when 2k + 1 is a multiple of 3..17 (repeats every PERIOD) */

static void make_base(u64 limit) {
    unsigned char *s = calloc(limit + 1, 1);
    nbase = 0; base = malloc(sizeof(u64) * (limit / 2 + 16));
    for (u64 i = 2; i <= limit; i++) {
        if (s[i]) continue;
        if (i > 17) base[nbase++] = i;
        for (u64 j = i * i; j <= limit; j += i) s[j] = 1;
    }
    free(s);
    nsmall = 0;
    while (nsmall < nbase && base[nsmall] < SUB) nsmall++;
}

static void make_pattern(void) {
    size_t len = SEG + PERIOD + 8;
    pat = malloc(len);
    memset(pat, 1, len);
    const unsigned small[6] = {3, 5, 7, 11, 13, 17};
    for (int t = 0; t < 6; t++)
        for (size_t k = (small[t] - 1) / 2; k < len; k += small[t]) pat[k] = 0;
}

typedef struct {
    u64 pairs, missed, last;
    u64 *per_billion; u64 nb;
    u64 upto[NMARK];
} result_t;

/* walk n = s .. e: odd numbers k = s - 1 .. e */
static void walk_chunk(u64 s, u64 e, u64 N, result_t *r, const u64 *marks, int nmarks) {
    unsigned char *T = malloc(SEG + 16);
    u64 *next = malloc(sizeof(u64) * nbase);
    u64 kstart = s - 1, kend = e;                    /* inclusive */
    u64 top = 2 * kend + 1;
    size_t np = 0;
    for (size_t i = 0; i < nbase; i++) {
        u64 p = base[i];
        if (p * p > top) break;
        u64 lo = 2 * kstart + 1;
        u64 m = (lo + p - 1) / p * p;
        if (m < p * p) m = p * p;
        if (m % 2 == 0) m += p;
        next[i] = (m - 1) / 2;                       /* odd-number index of the first odd multiple */
        np = i + 1;
    }
    unsigned char prev = 0; int have_prev = 0;
    for (u64 k0 = kstart; k0 <= kend; k0 += SEG) {
        u64 len = kend - k0 + 1; if (len > SEG) len = SEG;
        memcpy(T, pat + (k0 % PERIOD), len);
        const unsigned small[6] = {3, 5, 7, 11, 13, 17};
        for (int t = 0; t < 6; t++) { u64 k = (small[t] - 1) / 2; if (k >= k0 && k < k0 + len) T[k - k0] = 1; }
        if (k0 == 0) T[0] = 0;                       /* 1 is not prime */
        u64 k1 = k0 + len;
        /* small primes sub-piece by sub-piece, so the piece being crossed out stays in the core's own cache */
        for (u64 b0 = k0; b0 < k1; b0 += SUB) {
            u64 b1 = b0 + SUB < k1 ? b0 + SUB : k1;
            for (size_t i = 0; i < nsmall && i < np; i++) {
                u64 p = base[i], j = next[i];
                for (; j < b1; j += p) T[j - k0] = 0;
                next[i] = j;
            }
        }
        for (size_t i = nsmall; i < np; i++) {
            u64 p = base[i], j = next[i];
            for (; j < k1; j += p) T[j - k0] = 0;
            next[i] = j;
        }
        /* pairs: n with entries n - 1 and n both prime; n runs over k0 + 1 .. k1 - 1 inside, n = k0 across the edge */
        if (have_prev && prev && T[0]) {
            u64 n = k0;
            if (n >= s && n <= e) {
                r->pairs++; if (n % 3 != 0 && n != 2) r->missed++; r->last = n;
                r->per_billion[(n - 1) / 1000000000ull]++;
                for (int q = 0; q < nmarks; q++) if (n <= marks[q]) r->upto[q]++;
            }
        }
        u64 i = 0;
        for (; i + 9 <= len; i += 8) {
            u64 a, b; memcpy(&a, T + i, 8); memcpy(&b, T + i + 1, 8);
            if ((a & b) == 0) continue;
            for (int t = 0; t < 8; t++) if (T[i + t] && T[i + t + 1]) {
                u64 n = k0 + i + t + 1;
                if (n < s || n > e) continue;
                r->pairs++; if (n % 3 != 0 && n != 2) r->missed++; r->last = n;
                r->per_billion[(n - 1) / 1000000000ull]++;
                for (int q = 0; q < nmarks; q++) if (n <= marks[q]) r->upto[q]++;
            }
        }
        for (; i + 1 < len; i++) if (T[i] && T[i + 1]) {
            u64 n = k0 + i + 1;
            if (n < s || n > e) continue;
            r->pairs++; if (n % 3 != 0 && n != 2) r->missed++; r->last = n;
            r->per_billion[(n - 1) / 1000000000ull]++;
            for (int q = 0; q < nmarks; q++) if (n <= marks[q]) r->upto[q]++;
        }
        prev = T[len - 1]; have_prev = 1;
    }
    free(T); free(next);
}

int main(int argc, char **argv) {
    u64 N = strtoull(argv[1], NULL, 10);
    int threads = argc > 2 ? atoi(argv[2]) : omp_get_max_threads();
    make_base((u64)sqrt((double)(2 * N + 1)) + 2);
    make_pattern();
    u64 marks[NMARK]; int nmarks = 0;
    for (u64 m = 5; m <= N && nmarks < NMARK; m *= 10) marks[nmarks++] = m;
    u64 nb = (N - 1) / 1000000000ull + 1;
    int parts = threads * 16;                         /* more parts than threads, so the threads finish together */
    result_t *res = calloc(parts, sizeof(result_t));
    double t0 = omp_get_wtime();
    #pragma omp parallel for schedule(dynamic, 1) num_threads(threads)
    for (int c = 0; c < parts; c++) {
        u64 s = 1 + (N / parts) * c, e = (c == parts - 1) ? N : (N / parts) * (c + 1);
        res[c].per_billion = calloc(nb, sizeof(u64)); res[c].nb = nb;
        walk_chunk(s, e, N, &res[c], marks, nmarks);
        fprintf(stderr, "part %d of %d done (n %llu .. %llu), %.0f s\n", c + 1, parts, s, e, omp_get_wtime() - t0);
    }
    u64 pairs = 0, missed = 0, last = 0, upto[NMARK] = {0};
    u64 *pb = calloc(nb, sizeof(u64));
    for (int c = 0; c < parts; c++) {
        pairs += res[c].pairs; missed += res[c].missed; if (res[c].last > last) last = res[c].last;
        for (u64 b = 0; b < nb; b++) pb[b] += res[c].per_billion[b];
        for (int q = 0; q < nmarks; q++) upto[q] += res[c].upto[q];
    }
    printf("{\"N\": %llu, \"pairs\": %llu, \"missed\": %llu, \"last_n\": %llu, \"seconds\": %.1f, \"threads\": %d, ",
           N, pairs, missed, last, omp_get_wtime() - t0, threads);
    printf("\"pairs_up_to\": {");
    for (int q = 0; q < nmarks; q++) printf("%s\"%llu\": %llu", q ? ", " : "", marks[q], upto[q]);
    printf("}, \"per_billion\": [");
    for (u64 b = 0; b < nb; b++) printf("%s%llu", b ? ", " : "", pb[b]);
    printf("]}\n");
    return 0;
}
