"""
Zero Parameter Structure

Copyright (c) 2026 Yasuo Tanaka
Licensed under the MIT License.

Common fixed structural constants used in the ``Structural Origin of''
paper series.

V3 finite-geometric realization
-------------------------------
The fixed ratios R and S are generated from the unique finite-geometric
solution

    (q, a, b, c) = (2, 2, 3, 5),

with the nested binary dimensions

    F_2^2 < F_2^3 < F_2^5.

The legacy public interface

    P_MIN, P_MID, P_MAX,
    StructuralConstants,
    STRUCTURAL_CONSTANTS,

and the derived branch properties

    B_alpha, B_q, A_d, A_tau

is retained unchanged for compatibility with the existing sector-level
scripts.

The path labels are now connected to the finite-geometric decomposition

    F_2^3 = {0}
            disjoint union (F_2^2 \\ {0})
            disjoint union (F_2^3 \\ F_2^2),

whose cardinalities are

    1 | 3 | 4.

Hence

    P_MIN = 1 + 1 = 2,
    P_MID = 1 + 4 = 5,
    P_MAX = 3 + 4 = 7.

The previous identity P_MID = P_MAX - P_MIN remains true, but is no
longer used as the defining relation.
"""

from dataclasses import dataclass
from fractions import Fraction


# =========================================================
# Finite-geometric realization
# =========================================================

# Unique finite-field / dimension solution selected by the
# shell-symmetry condition in the V3 paper.
Q = 2
DIM_A = 2
DIM_B = 3
DIM_C = 5

# F_2^3 decomposition:
#
#     {0} | (F_2^2 \ {0}) | (F_2^3 \ F_2^2)
#      1  |        3       |        4
#
VACUUM              = 1
INNER_NONZERO       = Q**DIM_A - 1         # 3
OUTER_LAYER         = Q**DIM_B - Q**DIM_A  # 4

# F_2^5 state counts.
INNER_TOTAL_NONZERO = Q**DIM_B - 1         # 7
TOTAL_NONZERO       = Q**DIM_C - 1         # 31
OUTER_SHELL         = Q**DIM_C - Q**DIM_B  # 24


# =========================================================
# Legacy public path interface
# =========================================================

# Retained names and values for compatibility with existing scripts.
#
# P_MIN:
#   binary two-class structure, retained in the legacy form 1 + 1.
#
# P_MID:
#   vacuum plus the four-state outer affine layer.
#
# P_MAX:
#   all seven nonzero states of F_2^3 = 3 + 4.
#
P_MIN = 1 + 1
P_MID = VACUUM + OUTER_LAYER
P_MAX = INNER_NONZERO + OUTER_LAYER

# Structural consistency checks.
assert P_MIN == 2
assert P_MID == 5
assert P_MAX == 7

assert P_MAX == INNER_TOTAL_NONZERO
assert P_MID == 1 + OUTER_LAYER

# The old relation remains numerically valid, but is now a consequence
# rather than the definition of P_MID.
assert P_MID == P_MAX - P_MIN


# =========================================================
# Common structural branches
# =========================================================

@dataclass(frozen=True)
class StructuralConstants:
    """
    Fixed structural branches of the framework.

    V3 finite-geometric forms
    -------------------------

    S is the total-to-outer-shell normalization,

        S = (q^c - 1) / (q^c - q^b)
          = 31 / 24.

    R is the common value selected by the compatible projective-incidence
    and affine-action normalizations at q = 2,

        R = 2 + 1 / [q(q + 1)]
          = 13 / 6.

    These are exactly equivalent to the legacy numerical forms

        R = 2 * (1 + P_MIN / 24),
        S = 1 + P_MAX / 24.

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

    # V3 definitions.
    R: Fraction = Fraction(2, 1) + Fraction(1, Q * (Q + 1))
    S: Fraction = Fraction(TOTAL_NONZERO, OUTER_SHELL)

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
# Backward-compatibility checks
# =========================================================

# Legacy R/S expressions are retained only as exact equivalence checks.
_LEGACY_R = 2 * (Fraction(1) + Fraction(P_MIN, OUTER_SHELL))
_LEGACY_S = Fraction(1) + Fraction(P_MAX, OUTER_SHELL)

assert StructuralConstants.R == _LEGACY_R
assert StructuralConstants.S == _LEGACY_S


# Default instance used by other modules.
STRUCTURAL_CONSTANTS = StructuralConstants()


if __name__ == "__main__":
    c = STRUCTURAL_CONSTANTS

    print("Finite-geometric realization")
    print("----------------------------")
    print(f"q = {Q}")
    print(f"(a, b, c) = ({DIM_A}, {DIM_B}, {DIM_C})")
    print(f"1 | 3 | 4 = {VACUUM} | {INNER_NONZERO} | {OUTER_LAYER}")
    print(f"outer shell = {OUTER_SHELL}")
    print(f"total nonzero = {TOTAL_NONZERO}")
    print()

    print("Legacy public interface")
    print("-----------------------")
    print(f"P_MIN = {P_MIN}")
    print(f"P_MID = {P_MID}")
    print(f"P_MAX = {P_MAX}")
    print()

    print("Structural constants")
    print("--------------------")
    print(f"R = {c.R} = {float(c.R):.12f}")
    print(f"S = {c.S} = {float(c.S):.12f}")
    print()

    print("Derived common branches")
    print("-----------------------")
    print(f"B_alpha = {c.B_alpha} = {float(c.B_alpha):.12f}")
    print(f"B_q     = {c.B_q} = {float(c.B_q):.12f}")
    print(f"A_d     = {c.A_d} = {float(c.A_d):.12f}")
    print(f"A_tau   = {c.A_tau} = {float(c.A_tau):.12f}")
