/*
 * The race of the owner's three twin chains, on the owner's walk (tools/owner_walk_fast.c, the same table and pair test).
 * Every twin pair 2n - 1, 2n + 1 after (3, 5) has n at place 3; the root of n picks the chain:
 *   root 3 -> (5, 7)     root 6 -> (2, 4)     root 9 -> (8, 1)
 * Pass 1 counts each chain per part; pass 2 walks each part again starting from the counts before it, so the lead
 * (the chain with the most pairs so far; on a tie the first of 3, 6, 9) is followed pair by pair, exactly.
 * Also counted: the middle 2n by 37.
 *
 * At each n: predict from n's place in 1 2 3 (place 3, or n = 2); act with the neighbours, behind + yourself = 2n - 1
 * and yourself + right = 2n + 1; verify that both are prime. As in tools/owner_walk_parallel.py, 2n - 1 is odd number
 * n - 1 and 2n + 1 is odd number n (the k-th odd number is 2k + 1): one table "is 2k + 1 prime?", read two neighbouring
 * entries at a time. Same pieces, same pattern for 3 5 7 11 13 17, same counts -- only the language is faster.
 *
 *   gcc -O3 -march=native -fopenmp -o owner_race_fast tools/owner_race_fast.c -lm
 *   ./owner_race_fast N [threads]          prints one JSON line
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

#define NCK 16

typedef struct {
    int pass;                                    /* 1 or 2 */
    u64 c[3];                                    /* chains: n -> 3, 6, 9 */
    u64 c37[37];                                 /* the middle 2n by 37 */
    u64 *pb; u64 nb;                             /* per billion of n, 3 chains */
    u64 ck[NCK][3]; const u64 *marks; int nmarks;
    long long cum[3]; int lead;                  /* pass 2 */
    u64 changes, last_change;
    u64 n2;                                      /* the pair at n = 2 */
} race_t;

static inline int argmax3(const long long *v) {
    int b = 0;
    if (v[1] > v[b]) b = 1;
    if (v[2] > v[b]) b = 2;
    return b;
}

static inline void on_pair(u64 n, race_t *r) {
    if (n <= 2) { if (r->pass == 1) r->n2++; return; }
    int m = (int)(n % 9);
    int idx = m == 3 ? 0 : (m == 6 ? 1 : 2);     /* n is a multiple of 3 here, so m is 3, 6 or 0 */
    if (r->pass == 1) {
        r->c[idx]++;
        r->c37[(2 * n) % 37]++;
        r->pb[((n - 1) / 1000000000ull) * 3 + idx]++;
        for (int q = 0; q < r->nmarks; q++) if (n <= r->marks[q]) r->ck[q][idx]++;
    } else {
        r->cum[idx]++;
        int l = argmax3(r->cum);
        if (r->lead < 0) r->lead = l;
        else if (l != r->lead) { r->changes++; r->last_change = n; r->lead = l; }
    }
}

/* walk n = s .. e: odd numbers k = s - 1 .. e */
static void walk_chunk(u64 s, u64 e, race_t *r) {
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
                on_pair(n, r);
            }
        }
        u64 i = 0;
        for (; i + 9 <= len; i += 8) {
            u64 a, b; memcpy(&a, T + i, 8); memcpy(&b, T + i + 1, 8);
            if ((a & b) == 0) continue;
            for (int t = 0; t < 8; t++) if (T[i + t] && T[i + t + 1]) {
                u64 n = k0 + i + t + 1;
                if (n < s || n > e) continue;
                on_pair(n, r);
            }
        }
        for (; i + 1 < len; i++) if (T[i] && T[i + 1]) {
            u64 n = k0 + i + 1;
            if (n < s || n > e) continue;
                on_pair(n, r);
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
    u64 marks[NCK]; int nmarks = 0;
    for (u64 m = 1000000; m <= N && nmarks < NCK; m *= 10) marks[nmarks++] = m;
    u64 nb = (N - 1) / 1000000000ull + 1;
    int parts = threads * 16;
    race_t *res = calloc(parts, sizeof(race_t));
    double t0 = omp_get_wtime();
    #pragma omp parallel for schedule(dynamic, 1) num_threads(threads)
    for (int c = 0; c < parts; c++) {
        u64 s = 1 + (N / parts) * c, e = (c == parts - 1) ? N : (N / parts) * (c + 1);
        res[c].pass = 1; res[c].pb = calloc(nb * 3, sizeof(u64)); res[c].nb = nb;
        res[c].marks = marks; res[c].nmarks = nmarks;
        walk_chunk(s, e, &res[c]);
        fprintf(stderr, "pass 1: part %d of %d done, %.0f s\n", c + 1, parts, omp_get_wtime() - t0);
    }
    long long off[3] = {0, 0, 0};
    for (int c = 0; c < parts; c++) {
        for (int j = 0; j < 3; j++) res[c].cum[j] = off[j];
        res[c].lead = (off[0] + off[1] + off[2] == 0) ? -1 : argmax3(off);
        for (int j = 0; j < 3; j++) off[j] += (long long)res[c].c[j];
    }
    #pragma omp parallel for schedule(dynamic, 1) num_threads(threads)
    for (int c = 0; c < parts; c++) {
        u64 s = 1 + (N / parts) * c, e = (c == parts - 1) ? N : (N / parts) * (c + 1);
        res[c].pass = 2;
        walk_chunk(s, e, &res[c]);
        fprintf(stderr, "pass 2: part %d of %d done, %.0f s\n", c + 1, parts, omp_get_wtime() - t0);
    }
    u64 tot[3] = {0, 0, 0}, c37[37] = {0}, ck[NCK][3] = {{0}}, changes = 0, last_change = 0, n2 = 0;
    u64 *pb = calloc(nb * 3, sizeof(u64));
    for (int c = 0; c < parts; c++) {
        for (int j = 0; j < 3; j++) tot[j] += res[c].c[j];
        for (int j = 0; j < 37; j++) c37[j] += res[c].c37[j];
        for (u64 b = 0; b < nb * 3; b++) pb[b] += res[c].pb[b];
        for (int q = 0; q < nmarks; q++) for (int j = 0; j < 3; j++) ck[q][j] += res[c].ck[q][j];
        changes += res[c].changes; if (res[c].last_change > last_change) last_change = res[c].last_change;
        n2 += res[c].n2;
    }
    long long fin[3] = {(long long)tot[0], (long long)tot[1], (long long)tot[2]};
    const char *names[3] = {"root3 (5,7)", "root6 (2,4)", "root9 (8,1)"};
    printf("{\"N\": %llu, \"pair_at_2\": %llu, \"chains\": {\"root3\": %llu, \"root6\": %llu, \"root9\": %llu}, ",
           N, n2, tot[0], tot[1], tot[2]);
    printf("\"lead_changes\": %llu, \"last_change_n\": %llu, \"final_lead\": \"%s\", \"seconds\": %.1f, ",
           changes, last_change, names[argmax3(fin)], omp_get_wtime() - t0);
    printf("\"checkpoints\": {");
    for (int q = 0; q < nmarks; q++) printf("%s\"%llu\": [%llu, %llu, %llu]", q ? ", " : "", marks[q], ck[q][0], ck[q][1], ck[q][2]);
    printf("}, \"middle_by_37\": [");
    for (int j = 0; j < 37; j++) printf("%s%llu", j ? ", " : "", c37[j]);
    printf("], \"per_billion\": [");
    for (u64 b = 0; b < nb; b++) printf("%s[%llu, %llu, %llu]", b ? ", " : "", pb[3 * b], pb[3 * b + 1], pb[3 * b + 2]);
    printf("]}\n");
    return 0;
}
