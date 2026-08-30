#!/usr/bin/env python3
"""Exact checks for the finite-geometric and perfect-number realization.

The analytic proofs are given in the manuscript. This script provides
reproducibility checks for the finite search, the selected perfect-number
hierarchy, inclusion-exclusion cardinalities, finite flags, orbit-stabilizer
counts, and the derived X/Y structural-level coordinate table.

All decisive calculations use integers or fractions.
"""

from fractions import Fraction
from itertools import combinations, product
from math import comb, prod


def gl_order(a: int, q: int) -> int:
    return prod(q**a - q**i for i in range(a))


def agl_order(a: int, q: int) -> int:
    return q**a * gl_order(a, q)


def shell(q: int, b: int, c: int) -> int:
    return q**c - q**b


# ---------------------------------------------------------------------
# 1. Finite sanity check of the shell-symmetry uniqueness theorem
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

q, a, b, c = 2, 2, 3, 5


# ---------------------------------------------------------------------
# 2. Mersenne cores and the first three even perfect numbers
# ---------------------------------------------------------------------
def mersenne(p: int) -> int:
    return 2**p - 1


def even_perfect(p: int) -> int:
    return 2 ** (p - 1) * mersenne(p)


selected_exponents = (a, b, c)
selected_perfect = [(p, even_perfect(p)) for p in selected_exponents]
print("selected perfect numbers:", selected_perfect)
assert selected_perfect == [(2, 6), (3, 28), (5, 496)]

P1, P2, P3 = (value for _, value in selected_perfect)
M2, M3, M5 = mersenne(2), mersenne(3), mersenne(5)

assert (M2, M3, M5) == (3, 7, 31)
assert P1 == comb(2**2, 2)
assert P2 == comb(2**3, 2)
assert P3 == comb(2**5, 2)
assert M5 == M2 + 2**2 * M3
assert M3 == P1 + 1
assert P2 == q**2 * (P1 + 1)


# ---------------------------------------------------------------------
# 3. Unified support counts and inclusion-exclusion
# ---------------------------------------------------------------------
# A ~= F_2^2 and B ~= F_2^3. In A x B define
# calX = (A \\ {0}) x B and calY = A x (B \\ {0}).
# Only cardinalities are required for the paper's normalization.
calX_count = (q**a - 1) * q**b
calY_count = q**a * (q**b - 1)
union_count = q ** (a + b) - 1
intersection_count = (q**a - 1) * (q**b - 1)

print(
    f"support counts: calX={calX_count}, calY={calY_count}, "
    f"union={union_count}, intersection={intersection_count}"
)

assert a + b == c
assert c - b == a
assert calX_count == shell(q, b, c) == 24
assert calY_count == P2 == 28
assert union_count == M5 == 31
assert intersection_count == M2 * M3 == 21
assert calX_count + calY_count == union_count + intersection_count

R = Fraction(calX_count + calY_count, calX_count)
S = Fraction(union_count, calX_count)
R_minus_S = Fraction(intersection_count, calX_count)

assert R == S + R_minus_S
assert R == Fraction(13, 6)
assert S == Fraction(31, 24)
assert R_minus_S == Fraction(7, 8)

# Equivalent perfect-number closure forms used in the manuscript.
assert R == Fraction(q, 1) + Fraction(1, P1)
assert R_minus_S == Fraction(P2, q**5)
assert S == Fraction(P3, P1 * q**6)

print(f"perfect-number ratios: R={R}, R-S={R_minus_S}, S={S}")

# Structural decomposition: the apparently different perfect-number
# denominators reduce to the same q^3 normalization.
assert R_minus_S == Fraction(M3, q**3)
assert S == Fraction(M5, M2 * q**3)
assert R == Fraction(M2 * M3 + M5, M2 * q**3)

print(
    "common q^3 normalization: "
    f"R-S={Fraction(M3, q**3)}, S={Fraction(M5, M2 * q**3)}"
)


# ---------------------------------------------------------------------
# 4. Flag cardinalities in F_2^5
# ---------------------------------------------------------------------
def add(x, y):
    return tuple(u ^ v for u, v in zip(x, y))


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
# 5. GL(3,2), line stabilizer, and the 12 x 2 = 24 action
# ---------------------------------------------------------------------
def rank_mod2(matrix):
    mat = [list(row) for row in matrix]
    r = 0
    m, n = len(mat), len(mat[0])
    for col in range(n):
        pivot = next((i for i in range(r, m) if mat[i][col]), None)
        if pivot is None:
            continue
        mat[r], mat[pivot] = mat[pivot], mat[r]
        for i in range(m):
            if i != r and mat[i][col]:
                mat[i] = [x ^ y for x, y in zip(mat[i], mat[r])]
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


# ---------------------------------------------------------------------
# 6. Finite-geometric X/Y structural-level mapping
# ---------------------------------------------------------------------
def X_ZERO(n: int) -> int:
    if n < 1:
        raise ValueError("X structural level n must be >= 1")
    return 2**(n + 2) - 2**n


def X_MINUS(n: int) -> int:
    return X_ZERO(n) - 1


def X_PLUS(n: int) -> int:
    return X_ZERO(n) + 1


def Y(n: int) -> int:
    if n < 1:
        raise ValueError("Y structural level n must be >= 1")
    return 2**(n + 1) - 1


xy_table = [
    (n, X_MINUS(n), X_ZERO(n), X_PLUS(n), Y(n))
    for n in range(1, 5)
]
expected_xy_table = [
    (1, 5, 6, 7, 3),
    (2, 11, 12, 13, 7),
    (3, 23, 24, 25, 15),
    (4, 47, 48, 49, 31),
]

print("XY structural-level table:", xy_table)
assert xy_table == expected_xy_table

for n in range(1, 5):
    assert X_ZERO(n) == shell(2, n, n + 2)
    assert X_MINUS(n) == X_ZERO(n) - 1
    assert X_PLUS(n) == X_ZERO(n) + 1
    assert Y(n) == 2**(n + 1) - 1

for n in range(1, 4):
    assert X_ZERO(n + 1) == 2 * X_ZERO(n)
    assert X_MINUS(n + 1) == 2 * X_MINUS(n) + 1
    assert X_PLUS(n + 1) == 2 * X_PLUS(n) - 1
    assert Y(n + 1) == 2 * Y(n) + 1

assert X_ZERO(1) == 6
assert X_ZERO(2) == len(updates) == 12
assert X_ZERO(3) == shell(2, 3, 5) == 24
assert Y(4) == 2**5 - 1 == 31

# Coordinate representations of the already-derived fixed ratios.
assert Fraction(X_PLUS(2), X_ZERO(1)) == R
assert Fraction(Y(4), X_ZERO(3)) == S
assert Fraction(q, 1) / S == Fraction(X_ZERO(4), Y(4))

print("XY finite-geometric mapping checks passed")
print("all exact verification checks passed")
