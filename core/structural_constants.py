"""
Zero Parameter Structure

Copyright (c) 2026 Yasuo Tanaka
Licensed under the MIT License.

This work is presented as a translation of underlying physical structure.
No free parameters. No tuning. Only structure.
"""

from dataclasses import dataclass
from fractions import Fraction


# =========================================================
# Common structural symbols
# =========================================================

@dataclass(frozen=True)
class StructuralConstants:
    """
    Fixed structural constants of the framework.

    R:
        Basic structural propagation ratio.
        This constant represents the reconstruction ratio of the full structure
        from the observable sector, and sets the scale for structural transmission.

    Z:
        Internal/external conversion factor.
        This constant bridges internal binding structure and externally observed structure,
        and appears when translating between structural propagation and light-observed quantities.

    In this interpretation:
    - light propagation corresponds to the externally observed transmission
    - structural propagation corresponds to the underlying update/transfer structure
    - Z mediates the conversion between internal binding and external observation
    """

    # Structural propagation ratio
    R: Fraction = Fraction(24 + 2, 12)

    # Internal/external conversion factor
    Z: Fraction = Fraction(24 + 7, 24)

