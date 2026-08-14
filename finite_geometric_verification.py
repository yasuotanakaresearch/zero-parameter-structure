#!/usr/bin/env python3
"""Exact checks for the finite-geometric realization used in the paper.

The analytic proofs are given in the manuscript.  This script is a
reproducibility check for finite searches and structural cardinalities.
All decisive calculations use integers or fractions.
"""

from fractions import Fraction
from itertools import combinations, product
from math import prod


def gl_order(a: int, q: int) -> int:
    return prod(q**a - q**i for i in range(a))


def agl_order(a: int, q: int) -> int:
    return q**a * gl_order(a, q)


def shell(q: int, b: int, c: int) -> int:
    return q**c - q**b


def s_ratio(q: int, b: int, c: int) -> Fraction:
    return Fraction(q**c - 1, q**c - q**b)


def r_inc(q: int) -> Fraction:
    n = q*q + q + 1
    return Fraction(n + (n - 1), n - 1)


def r_act(q: int) -> Fraction:
    orbit = q*q * (q*q - 1)
    stabilizer = q * (q - 1)
    return Fraction(stabilizer, 1) * (1 + Fraction(1, orbit))


# ---------------------------------------------------------------------
# 1. Finite sanity check of the uniqueness theorem
# ---------------------------------------------------------------------
solutions = []
for q in range(2, 33):
    for a in range(1, 7):
        for b in range(a + 1, 22):
            for c in range(b + 1, 28):
                if shell(q, b, c) == agl_order(a, q):
                    solutions.append((q, a, b, c, shell(q, b, c)))

print("shell=symmetry solutions:", solutions)
assert solutions == [(2, 2, 3, 5, 24)]


# ---------------------------------------------------------------------
# 2. R and S uniqueness checks
# ---------------------------------------------------------------------
r_matches = [(q, r_inc(q)) for q in range(2, 101) if r_inc(q) == r_act(q)]
print("R-family intersections:", r_matches)
assert r_matches == [(2, Fraction(13, 6))]

s_matches = []
for q in range(2, 129):
    for b in range(1, 20):
        for c in range(b + 1, 30):
            if s_ratio(q, b, c) == Fraction(31, 24):
                s_matches.append((q, b, c))
print("S=31/24 solutions:", s_matches)
assert s_matches == [(2, 3, 5)]


# ---------------------------------------------------------------------
# 3. Flag cardinalities in F_2^5
# ---------------------------------------------------------------------
def add(x, y):
    return tuple(a ^ b for a, b in zip(x, y))


def span(vectors, n):
    out = {(0,) * n}
    for v in vectors:
        out |= {add(x, v) for x in list(out)}
    return frozenset(out)


def k_subspaces(n, k):
    nonzero = [v for v in product((0, 1), repeat=n) if any(v)]
    spaces = set()
    for basis in combinations(nonzero, k):
        s = span(basis, n)
        if len(s) == 2**k:
            spaces.add(s)
    return spaces


v5 = frozenset(product((0, 1), repeat=5))
sub3 = k_subspaces(5, 3)
profiles = set()
flag_count = 0
for u3 in sub3:
    nz = [v for v in u3 if any(v)]
    sub2 = set()
    for x, y in combinations(nz, 2):
        u2 = span((x, y), 5)
        if len(u2) == 4 and u2.issubset(u3):
            sub2.add(u2)
    for u2 in sub2:
        flag_count += 1
        profiles.add((len(u2) - 1, len(u3 - u2), len(v5 - u3)))

print("flags F2^2 < F2^3 < F2^5:", flag_count)
print("layer profiles:", sorted(profiles))
assert flag_count == 1085
assert profiles == {(3, 4, 24)}


# ---------------------------------------------------------------------
# 4. GL(3,2), line stabilizer, and the 12 x 2 = 24 action
# ---------------------------------------------------------------------
def rank_mod2(matrix):
    a = [list(row) for row in matrix]
    r = 0
    m, n = len(a), len(a[0])
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        for i in range(m):
            if i != r and a[i][c]:
                a[i] = [x ^ y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def mat_vec(matrix, vector):
    return tuple(
        sum(matrix[i][j] * vector[j] for j in range(len(vector))) % 2
        for i in range(len(matrix))
    )


def all_gl(n):
    mats = []
    for bits in product((0, 1), repeat=n*n):
        matrix = tuple(tuple(bits[i*n:(i+1)*n]) for i in range(n))
        if rank_mod2(matrix) == n:
            mats.append(matrix)
    return mats


gl3 = all_gl(3)
u2 = frozenset((x, y, 0) for x, y in product((0, 1), repeat=2))
u3 = frozenset(product((0, 1), repeat=3))
x_layer = frozenset(u3 - u2)
directions = frozenset(v for v in u2 if v != (0, 0, 0))
updates = tuple((x, d) for x in x_layer for d in directions)

line_stab = [
    m for m in gl3
    if frozenset(mat_vec(m, v) for v in u2) == u2
]

seed = updates[0]
orbit = {
    (mat_vec(m, seed[0]), mat_vec(m, seed[1]))
    for m in line_stab
}
stabilizer = [
    m for m in line_stab
    if (mat_vec(m, seed[0]), mat_vec(m, seed[1])) == seed
]

print("|GL(3,2)|:", len(gl3))
print("line stabilizer:", len(line_stab))
print("directed-update orbit:", len(orbit))
print("single-update stabilizer:", len(stabilizer))
assert len(gl3) == 168
assert len(line_stab) == 24
assert len(updates) == 12
assert len(orbit) == 12
assert len(stabilizer) == 2
assert len(line_stab) == len(orbit) * len(stabilizer)

print("all exact verification checks passed")
