"""
Zero Parameter Structure

Copyright (c) 2026 Yasuo Tanaka
Licensed under the MIT License.

Common fixed structural constants used in the ``Structural Origin of''
paper series.

The constants R and S are treated as fixed structural branches generated
from a common causal-path construction.  They are carried unchanged into
sector-specific relations and numerical comparisons.
"""

from dataclasses import dataclass
from fractions import Fraction


# =========================================================
# Causal-path counts
# =========================================================

# Minimal, maximal, and intermediate causal-path counts.
P_MIN = 1 + 1
P_MAX = 3 + 4

# P_MID is defined as the path span between P_MAX and P_MIN.
P_MID = P_MAX - P_MIN


# =========================================================
# Common structural branches
# =========================================================

@dataclass(frozen=True)
class StructuralConstants:
    """
    Fixed structural branches of the framework.

    R:
        The R-branch generated from the minimal causal-path count,

            R = 2 * (1 + P_MIN / 24) = 13 / 6.

        It is used as one of the common fixed structural inputs in the
        sector-specific relations.

    S:
        The S-branch generated from the maximal causal-path count,

            S = 1 + P_MAX / 24 = 31 / 24.

        It is used together with R as a common fixed structural input.

    Interpretation:
        The R- and S-branches are treated as fixed structural ratios
        associated with a causal-path interpretation consistent with the
        causal structure of general relativity.

        They are not adjusted separately for individual observables.
        Their role is to provide common fixed inputs for reproducible
        numerical comparisons across different physical sectors.
    """

    R: Fraction = 2 * (Fraction(1) + Fraction(P_MIN, 24))
    S: Fraction =      Fraction(1) + Fraction(P_MAX, 24)


# Default instance used by other modules.
STRUCTURAL_CONSTANTS = StructuralConstants()
