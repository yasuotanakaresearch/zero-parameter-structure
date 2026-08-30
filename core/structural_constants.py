"""
Zero Parameter Structure

Copyright (c) 2026 Yasuo Tanaka
Licensed under the MIT License.

Common fixed structural constants used in the ``Structural Origin of''
paper series.

Version 1.0 minimal-axiom foundation
------------------------------------
The foundational construction selects

    q = 2,
    q_sharp = q + 1 = 3,

and generates

    X(n,s) = q_sharp * q**n + s,
    Y(n)   = q**(n+1) - 1,

with the unit-normalized product map

    P(n) = X(n)Y(n) / q_sharp.

The distinguished values are

    P(1), P(q), P(q**2) = 6, 28, 496.

The common structural ratios are defined directly from the generated
X/Y hierarchy,

    R = X(q,+1) / X(1)         = 13/6,
    S = Y(q**2) / X(q_sharp)   = 31/24,

so that

    q/S = X(q**2) / Y(q**2) = 48/31.

The existing sector-level interface

    P_MIN, P_MID, P_MAX,
    StructuralConstants,
    STRUCTURAL_CONSTANTS,

and the derived branch properties

    B_alpha, B_q, A_d, A_tau

is retained unchanged.  The legacy labels P_MIN/P_MID/P_MAX are
downstream compatibility values and are distinct from the foundational
product-map values P1/P2/P3.
"""

from dataclasses import dataclass
from fractions import Fraction


# =========================================================
# Minimal axiomatic structure
# =========================================================

q = 2
q_sharp = q + 1


def X(n: int, s: int = 0) -> int:
    """Generated X-sequence: X(n,s) = q_sharp * q^n + s."""
    return q_sharp * q**n + s


def Y(n: int) -> int:
    """Generated Y-sequence: Y(n) = q^(n+1) - 1."""
    return q**(n + 1) - 1


def P(n: int) -> int:
    """Unit-normalized product map: P(n) = X(n)Y(n)/q_sharp."""
    numerator = X(n) * Y(n)
    assert numerator % q_sharp == 0
    return numerator // q_sharp


P1 = P(1)
P2 = P(q)
P3 = P(q**2)

assert (q, q_sharp) == (2, 3)
assert (P1, P2, P3) == (6, 28, 496)


# =========================================================
# Legacy downstream interface
# =========================================================

# Retained unchanged for compatibility with existing sector-level scripts.
# These are not the same objects as P1, P2, P3.
P_MIN = 2
P_MID = 5
P_MAX = 7

assert (P_MIN, P_MID, P_MAX) == (2, 5, 7)


# =========================================================
# Optional finite-geometric consistency metadata
# =========================================================

# Retained for compatibility with earlier verification code.  These
# quantities are not used to define q, X, Y, P, R, or S.
Q = q
DIM_A = 2
DIM_B = 3
DIM_C = 5

VACUUM              = 1
INNER_NONZERO       = Q**DIM_A - 1
OUTER_LAYER         = Q**DIM_B - Q**DIM_A
INNER_TOTAL_NONZERO = Q**DIM_B - 1
TOTAL_NONZERO       = Q**DIM_C - 1
OUTER_SHELL         = Q**DIM_C - Q**DIM_B


# =========================================================
# Common structural branches
# =========================================================

@dataclass(frozen=True)
class StructuralConstants:
    """
    Fixed structural branches of the framework.

    Version 1.0 X/Y forms
    ---------------------

    R and S are generated directly from the X/Y hierarchy,

        R = X(q,+1) / X(1)
          = 13 / 6,

        S = Y(q**2) / X(q_sharp)
          = 31 / 24.

    The terminal ratio is

        q / S = X(q**2) / Y(q**2)
              = 48 / 31.

    The product-map formulas are exact equivalent closure
    representations rather than the primary definitions.

    Common branch structure
    -----------------------

            [ B_alpha  B_q   ]   [ 3 R^2 ] [ S^(-1)  S ]
            [ A_d      A_tau ] = [ 8 R   ]

    Therefore,

        B_alpha = 3 R^2 / S,
        B_q     = 3 R^2 S,
        A_d     = 8 R / S,
        A_tau   = 8 R S.

    The branch coefficients are derived quantities, not additional
    independent structural inputs.
    """

    R: Fraction = Fraction(X(q, +1), X(1))
    S: Fraction = Fraction(Y(q**2), X(q_sharp))

    @property
    def B_alpha(self) -> Fraction:
        """Electromagnetic and kinematic common branch, 3 R^2 / S."""
        return 3 * self.R**2 / self.S

    @property
    def B_q(self) -> Fraction:
        """Quark-sector common branch, 3 R^2 S."""
        return 3 * self.R**2 * self.S

    @property
    def A_d(self) -> Fraction:
        """Inverse-S A-branch, 8 R / S."""
        return 8 * self.R / self.S

    @property
    def A_tau(self) -> Fraction:
        """S-weighted A-branch, 8 R S."""
        return 8 * self.R * self.S


# =========================================================
# Exact closure and backward-compatibility checks
# =========================================================

# Primary X/Y relation.
assert Fraction(q, 1) / StructuralConstants.S == Fraction(X(q**2), Y(q**2))
assert X(q**2) == q * X(q_sharp)

# Equivalent product-map closure.
assert StructuralConstants.R == Fraction(q, 1) + Fraction(1, P1)
assert StructuralConstants.S == Fraction(P3, P1 * q**P1)
assert StructuralConstants.R - StructuralConstants.S == Fraction(P2, q**(P1 - 1))

# Legacy downstream R/S expressions remain exact numerical identities.
_LEGACY_R = 2 * (Fraction(1) + Fraction(P_MIN, 24))
_LEGACY_S = Fraction(1) + Fraction(P_MAX, 24)

assert StructuralConstants.R == _LEGACY_R
assert StructuralConstants.S == _LEGACY_S


# Default instance used by other modules.
STRUCTURAL_CONSTANTS = StructuralConstants()


if __name__ == "__main__":
    c = STRUCTURAL_CONSTANTS

    print("Minimal axiomatic structure")
    print("---------------------------")
    print(f"q = {q}")
    print(f"q_sharp = {q_sharp}")
    print(f"P1, P2, P3 = {P1}, {P2}, {P3}")
    print(f"R = {c.R} = {float(c.R):.12f}")
    print(f"S = {c.S} = {float(c.S):.12f}")
    print(f"q/S = {Fraction(q, 1) / c.S} = {float(Fraction(q, 1) / c.S):.12f}")
    print()

    print("Legacy downstream interface")
    print("---------------------------")
    print(f"P_MIN = {P_MIN}")
    print(f"P_MID = {P_MID}")
    print(f"P_MAX = {P_MAX}")
    print()

    print("Derived common branches")
    print("-----------------------")
    print(f"B_alpha = {c.B_alpha} = {float(c.B_alpha):.12f}")
    print(f"B_q     = {c.B_q} = {float(c.B_q):.12f}")
    print(f"A_d     = {c.A_d} = {float(c.A_d):.12f}")
    print(f"A_tau   = {c.A_tau} = {float(c.A_tau):.12f}")
