"""
Zero Parameter Structure

Copyright (c) 2026 Yasuo Tanaka
Licensed under the MIT License.

This work is presented as a translation of underlying physical structure.
No free parameters. No tuning. Only structure.
"""

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction

from core.structural_constants import StructuralConstants
from core.structural_electron import (
    alpha_inverse,
    compute_electron_mass_path,
    compute_psi_values,
)

getcontext().prec = 56


# =========================================================
# Helpers
# =========================================================


def fraction_to_decimal(value: Fraction) -> Decimal:
    """Convert an exact Fraction to a high-precision Decimal."""
    return Decimal(value.numerator) / Decimal(value.denominator)


def alpha2_transfer(alpha: Decimal, i: int, j: int) -> Decimal:
    r"""Return the structural-transfer factor

        alpha^2_[i->j] = alpha^(2(i-j)).
    """
    return alpha ** (2 * (i - j))


# =========================================================
# Structural formulas
# =========================================================


@dataclass(frozen=True)
class NeutrinoMassRatios:
    m1_over_me: Decimal
    m2_over_me: Decimal
    m3_over_me: Decimal


@dataclass(frozen=True)
class NeutrinoMasses:
    m1_ev: Decimal
    m2_ev: Decimal
    m3_ev: Decimal
    delta_m21_ev2: Decimal
    delta_m31_ev2: Decimal
    delta_m32_ev2: Decimal
    sum_mnu_ev: Decimal


def neutrino_branch_factors(
    constants: StructuralConstants,
) -> tuple[Decimal, Decimal, Decimal]:
    r"""Return the fixed neutrino branch factors

        Phi_0 = 1,
        Phi_1 = 1/(3R^2),
        Phi_2 = 1/R.
    """
    R = fraction_to_decimal(constants.R)

    return (
        Decimal(1),
        Decimal(1) / (Decimal(3) * R**2),
        Decimal(1) / R,
    )


def neutrino_base_mass_ratio(constants: StructuralConstants) -> Decimal:
    r"""Return the common neutrino base structure relative to the electron mass.

        B_nu = 12 S alpha^2_[2->0]
             = 12 S alpha^4.
    """
    psi_electron = compute_psi_values(constants)
    alpha = Decimal(1) / alpha_inverse(constants, psi_electron)
    S = fraction_to_decimal(constants.S)

    return Decimal(12) * S * alpha2_transfer(alpha, 2, 0)


def compute_neutrino_mass_ratios(constants: StructuralConstants) -> NeutrinoMassRatios:
    r"""Compute the three neutrino mass ratios from the unified relation

        m_nu,n / m_e = B_nu (n + Phi_n),    n = 0, 1, 2.

    The public field names m1, m2, and m3 are retained for compatibility;
    they correspond respectively to n = 0, 1, and 2.
    """
    B_nu = neutrino_base_mass_ratio(constants)
    phi = neutrino_branch_factors(constants)

    ratios = tuple(
        B_nu * (Decimal(n) + phi_n)
        for n, phi_n in enumerate(phi)
    )

    return NeutrinoMassRatios(
        m1_over_me=ratios[0],
        m2_over_me=ratios[1],
        m3_over_me=ratios[2],
    )


def compute_neutrino_masses(constants: StructuralConstants) -> NeutrinoMasses:
    """Convert the structural mass ratios to eV and compute mass splittings."""
    ratios = compute_neutrino_mass_ratios(constants)

    psi_electron = compute_psi_values(constants)
    electron_path = compute_electron_mass_path(constants, psi_electron)
    me_st = fraction_to_decimal(electron_path.mass_scale)

    m1 = ratios.m1_over_me * me_st
    m2 = ratios.m2_over_me * me_st
    m3 = ratios.m3_over_me * me_st

    dm21 = m2**2 - m1**2
    dm31 = m3**2 - m1**2
    dm32 = m3**2 - m2**2

    return NeutrinoMasses(
        m1_ev=m1,
        m2_ev=m2,
        m3_ev=m3,
        delta_m21_ev2=dm21,
        delta_m31_ev2=dm31,
        delta_m32_ev2=dm32,
        sum_mnu_ev=m1 + m2 + m3,
    )

