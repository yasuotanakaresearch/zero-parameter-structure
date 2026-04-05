"""
Zero Parameter Structure

Copyright (c) 2026 Yasuo Tanaka
Licensed under the MIT License.

This work is presented as a translation of underlying physical structure.
No free parameters. No tuning. Only structure.
"""

from dataclasses import dataclass
from fractions import Fraction

from core.structural_constants import StructuralConstants


# =========================================================
# Structural Density Relations
# =========================================================

@dataclass(frozen=True)
class DensityResult:
    """
    Exact structural density fractions derived from the common ratio R.

    The four components are expressed in exact rational form so that
    the closure structure and inter-component relations can be inspected
    without numerical rounding:
        ΩΛ  : dark-energy fraction
        Ωm  : total matter fraction
        Ωdm : dark-matter fraction
        Ωb  : baryon fraction
    """
    omega_lambda: Fraction
    omega_m: Fraction
    omega_dm: Fraction
    omega_b: Fraction


def compute_density_parameters(R: Fraction) -> DensityResult:
    """
    Compute the exact structural density fractions from the common ratio R.

    The normalized closure denominator is
        3R^2 + 3R,

    which yields the structural relations
        ΩΛ = 3R^2    / (3R^2 + 3R)
        Ωm = 3R       / (3R^2 + 3R)
        Ωdm = (3R - 1)/ (3R^2 + 3R)
        Ωb = 1        / (3R^2 + 3R)

    so that the exact ratio
        ΩΛ : Ωm : Ωb = 3R^2 : 3R : 1
    is preserved in rational form.
    """
    denom = 3 * R**2 + 3 * R

    omega_lambda =  3 * R**2   / denom
    omega_m      =  3 * R      / denom
    omega_dm     = (3 * R - 1) / denom
    omega_b      =  1          / denom

    return DensityResult(
        omega_lambda=omega_lambda,
        omega_m=omega_m,
        omega_dm=omega_dm,
        omega_b=omega_b,
    )

