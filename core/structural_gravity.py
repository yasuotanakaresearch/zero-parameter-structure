"""
Zero Parameter Structure

Copyright (c) 2026 Yasuo Tanaka
Licensed under the MIT License.

This work is presented as a translation of underlying physical structure.
No free parameters. No tuning. Only structure.
"""

from dataclasses import dataclass
from fractions import Fraction
from decimal import Decimal, getcontext

from core.structural_constants import StructuralConstants
from core.structural_electron import alpha_inverse, proton_mass_ratio

getcontext().prec = 56

PI = Decimal("3.14159265358979323846264338327950288419716939937510")

# Exact SI definitions
C = Decimal("299792458")
h = Decimal("6.62607015e-34")

# hbar = h / (2π)
HBAR = h / (Decimal(2) * PI)


# =========================================================
# helpers
# =========================================================
def fraction_to_decimal(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


# =========================================================
# Psi values
# =========================================================

@dataclass(frozen=True)
class PsiGravity:
    psi_g: Fraction
    psi_g_star: Fraction


def compute_psi_gravity(constants: StructuralConstants, psi_ew: Fraction) -> PsiGravity:
    """
    Construct the structural Psi values for the gravity sector.

    Interpretation:
    - psi_g      : global structural branching index for the gravity sector
    - psi_g_star : residual suppression index for the gravitational coupling sector
    """
    R = constants.R
    S = constants.S

    # Gravity:
    # global structural branching index for the gravity sector,
    # representing the full coupled pathway of secondary binding,
    # primary binding, and residual transfer across the fourfold base.
    #
    # Structure:
    #
    #     ΨG = [12 * (3R^2) * (4R) + 2R] / 4
    #
    # where:
    # - 3R^2 : secondary-binding structure
    # - 4R   : primary-binding structure
    # - 2R   : minimal propagation pathway
    # - /4   : normalization over the fourfold structural base
    psi_g = (12 * (3 * R**2) * (4 * R) + 2 * R) / 4

    # Gravitational residue:
    # residual suppression index for the gravity sector,
    # representing the small bridge residual remaining after
    # hierarchical reduction of the dominant gravity pathway.
    #
    # Structural bridge:
    #
    #     ΨG0 = R・S^2 * (12*24)
    #     ΨG* = 4ΨG - 3(1 + 1/ΨG0)
    #
    # Interpretation:
    # - 4ΨG :
    #     full fourfold propagation structure of the gravity sector
    #
    # - 3 :
    #     dominant reduction of the primary propagation layer
    #
    # - 1/ΨG0 :
    #     tiny residual bridge contribution inherited from
    #     the electron-sector structural hierarchy
    #
    # ΨG* acts as the residual suppression scale governing
    # the final correction channel of the gravitational coupling.
    psi_g_0    = R * S**2 * (12*24)
    psi_g_star = 4 * psi_g - 3 * (1 + 1 / psi_g_0)

    return PsiGravity(
        psi_g=Fraction(psi_g),
        psi_g_star=Fraction(psi_g_star),
    )


# =========================================================
# Theory results
# =========================================================

@dataclass(frozen=True)
class GravityResult:
    sqrt_g: Decimal
    g_value: Decimal
    alpha_gp: Decimal
    alpha_ge: Decimal
    planck_mass: Decimal
    mp_value: Decimal
    me_value: Decimal

# =========================================================
# Structural formulas
# =========================================================

def sqrt_g(constants: StructuralConstants, psi: PsiGravity, alpha: Decimal) -> Decimal:
    """
    Compute the structural expression for sqrt(G).

    sqrt(G) = alpha * S / (π * Psi_G)
    """
    S = fraction_to_decimal(constants.S)
    psi_g_val = fraction_to_decimal(psi.psi_g)
    return alpha * S / (PI * psi_g_val)


def g_value(constants: StructuralConstants, psi: PsiGravity, alpha: Decimal) -> Decimal:
    """
    Compute the structural expression for G.

    G = (sqrt(G))^2
    """
    s = sqrt_g(constants, psi, alpha)
    return s * s


def alpha_gp(mp_over_me: Decimal, psi: PsiGravity, alpha: Decimal) -> Decimal:
    """
    Compute the proton-side gravitational coupling.

    alpha_Gp = alpha^24 * (m_p / m_e)^4 / (1 + 1/Psi_g_star)
    """
    psi_g_star = fraction_to_decimal(psi.psi_g_star)
    return (alpha**24) * (mp_over_me**4) / (1 + 1 / psi_g_star)


def alpha_ge(mp_over_me: Decimal, psi: PsiGravity, alpha: Decimal) -> Decimal:
    """
    Compute the electron-side gravitational coupling.

    alpha_Ge = alpha^24 * (m_p / m_e)^2 / (1 + 1/Psi_g_star)
    """
    psi_g_star = fraction_to_decimal(psi.psi_g_star)
    return (alpha**24) * (mp_over_me**2) / (1 + 1 / psi_g_star)


# =========================================================
# Planck bridge
# =========================================================

def planck_mass(g_value: Decimal) -> Decimal:
    """
    Compute the Planck mass.

    M_Pl = sqrt(hbar * c / G)

    Interpretation
    --------------
    The Planck mass acts as a bridge between
    dimensionless structural hierarchy and
    observed SI mass scales.
    """
    return ((HBAR * C) / g_value).sqrt()


def mp_value(
    m_pl: Decimal,
    mp_over_me: Decimal,
    psi: PsiGravity,
    alpha: Decimal,
) -> Decimal:
    """
    Proton SI mass from the structural hierarchy.

    M_p = M_Pl * alpha^12 * (m_p / m_e)^2 * (1 + 1/Psi_g_star)^(-1/2)
    """
    g_correction = Decimal((1 + 1 / psi.psi_g_star) ** (-1/2))
    return (m_pl * (alpha ** 12) * (mp_over_me ** 2) * g_correction)


def me_value(
    m_pl: Decimal,
    mp_over_me: Decimal,
    psi: PsiGravity,
    alpha: Decimal,
) -> Decimal:
    """
    Electron SI mass from the structural hierarchy.

    M_e = M_Pl * alpha^12 * (m_p / m_e) * (1 + 1/Psi_g_star)^(-1/2)
    """
    g_correction = Decimal((1 + 1 / psi.psi_g_star) ** (-1/2))
    return (m_pl * (alpha ** 12) * mp_over_me * g_correction)


# =========================================================
# Main computation
# =========================================================

def compute_gravity(
    constants: StructuralConstants,
    psi_electron: Fraction,
) -> GravityResult:

    alpha = 1 / alpha_inverse(constants, psi_electron)
    mp_over_me = proton_mass_ratio(constants, psi_electron)

    psi_gravity = compute_psi_gravity(constants, psi_electron)

    g_sq = sqrt_g(constants, psi_gravity, alpha)
    g_val = g_sq ** 2

    alpha_gp_val = alpha_gp(mp_over_me, psi_gravity, alpha)
    alpha_ge_val = alpha_ge(mp_over_me, psi_gravity, alpha)

    m_pl = planck_mass(g_val)

    mp = mp_value(m_pl, mp_over_me, psi_gravity, alpha)
    me = me_value(m_pl, mp_over_me, psi_gravity, alpha)

    return GravityResult(
        sqrt_g=g_sq,
        g_value=g_val,
        alpha_gp=alpha_gp_val,
        alpha_ge=alpha_ge_val,
        planck_mass=m_pl,
        mp_value=mp,
        me_value=me,
    )

