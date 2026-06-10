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
from core.structural_electron import compute_psi_values, alpha_inverse, compute_electron_mass_path

getcontext().prec = 56


# =========================================================
# helpers
# =========================================================

def fraction_to_decimal(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


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


def neutrino_base_mass_ratio(constants: StructuralConstants) -> Decimal:
    """
    Base neutrino ratio relative to the electron mass.

        mν_base / me = 12 * S * alpha^4
    """
    psi_electron = compute_psi_values(constants)
    alpha = 1 / alpha_inverse(constants, psi_electron)

    return Decimal(12) * fraction_to_decimal(constants.S) * alpha**4


def compute_neutrino_mass_ratios(constants: StructuralConstants) -> NeutrinoMassRatios:
    """
    Three neutrino mass ratios relative to the electron mass.

        m1/me = 12 S alpha^4
        m2/me = m1/me * (1 + 1/(3R^2))
        m3/me = m1/me * (2 + 1/R)
    """
    R = fraction_to_decimal(constants.R)
    m1 = neutrino_base_mass_ratio(constants)
    m2 = m1 * (1 + 1 / (3 * R**2))
    m3 = m1 * (2 + 1 / R)

    return NeutrinoMassRatios(
        m1_over_me=m1,
        m2_over_me=m2,
        m3_over_me=m3,
    )


def compute_neutrino_masses(constants: StructuralConstants) -> NeutrinoMasses:
    ratios = compute_neutrino_mass_ratios(constants)

    psi_electron = compute_psi_values(constants)
    electron_path = compute_electron_mass_path(constants, psi_electron)
    me_c2 = fraction_to_decimal(electron_path.mass_scale)

    m1 = ratios.m1_over_me * me_c2
    m2 = ratios.m2_over_me * me_c2
    m3 = ratios.m3_over_me * me_c2

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

