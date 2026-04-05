"""
Zero Parameter Structure

Copyright (c) 2026 Yasuo Tanaka
Licensed under the MIT License.

This work is presented as a translation of underlying physical structure.
No free parameters. No tuning. Only structure.
"""

from dataclasses import dataclass
from fractions import Fraction
from math import pi

from core.structural_constants import StructuralConstants
from core.structural_electroweak import alpha_inverse


# =========================================================
# Psi values
# =========================================================

@dataclass(frozen=True)
class PsiGravity:
    psi_g: Fraction
    psi_d: Fraction


def compute_psi_gravity(constants: StructuralConstants) -> PsiGravity:
    """
    Construct the structural Psi values for the gravity sector.

    Interpretation:
    - psi_g : global structural branching index for the gravity sector
    - psi_d : residual suppression index for the gravitational coupling sector
    """
    R = constants.R

    # Gravity:
    # global structural branching index for the gravity sector,
    # representing the full coupled pathway of secondary binding,
    # primary binding, and residual transfer across the fourfold base.
    psi_g = (12 * (3 * R**2) * (4 * R) + 2 * R) / 4

    # Gravitational residue:
    # residual suppression index for the gravity sector,
    # representing the tiny leftover correction channel that remains
    # after the dominant binding structures are hierarchically reduced.
    psi_d = (3 * 12 * (8 * (4 + 3 * R) - 3) - 7) / 2

    return PsiGravity(
        psi_g=Fraction(psi_g),
        psi_d=Fraction(psi_d),
    )


# =========================================================
# Theory results
# =========================================================

@dataclass(frozen=True)
class GravityResult:
    sqrt_g: float
    g_value: float
    alpha_gp: float
    alpha_ge: float


# =========================================================
# Structural formulas
# =========================================================

def sqrt_g(constants: StructuralConstants, psi: PsiGravity, alpha: float) -> float:
    """
    Compute the structural expression for sqrt(G).

    sqrt(G) = alpha * Z / (pi * Psi_G)
    """
    Z = float(constants.Z)
    psi_g_val = float(psi.psi_g)
    return alpha * Z / (pi * psi_g_val)


def g_value(constants: StructuralConstants, psi: PsiGravity, alpha: float) -> float:
    """
    Compute the structural expression for G.

    G = (sqrt(G))^2
    """
    s = sqrt_g(constants, psi, alpha)
    return s * s


def alpha_gp(mp_over_me: float, psi: PsiGravity, alpha: float) -> float:
    """
    Compute the proton-side gravitational coupling.

    alpha_Gp = alpha^24 * (m_p / m_e)^4 / (1 + 1/Psi_d)
    """
    psi_d_val = float(psi.psi_d)
    return (alpha**24) * (mp_over_me**4) / (1.0 + 1.0 / psi_d_val)


def alpha_ge(mp_over_me: float, psi: PsiGravity, alpha: float) -> float:
    """
    Compute the electron-side gravitational coupling.

    alpha_Ge = alpha^24 * (m_p / m_e)^2 / (1 + 1/Psi_d)
    """
    psi_d_val = float(psi.psi_d)
    return (alpha**24) * (mp_over_me**2) / (1.0 + 1.0 / psi_d_val)


def compute_gravity(
    constants: StructuralConstants,
    alpha: float,
    mp_over_me: float,
) -> GravityResult:
    psi = compute_psi_gravity(constants)
    s = sqrt_g(constants, psi, alpha)

    return GravityResult(
        sqrt_g=s,
        g_value=s * s,
        alpha_gp=alpha_gp(mp_over_me, psi, alpha),
        alpha_ge=alpha_ge(mp_over_me, psi, alpha),
    )

