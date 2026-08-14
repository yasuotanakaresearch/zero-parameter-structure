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
from core.structural_electron import compute_psi_values

getcontext().prec = 56

PI = Decimal("3.1415926535897932384626433832795028841971693993751")

# Exact SI definitions.
c = 299_792_458  # exact speed of light in m/s
AU_M = Decimal("149597870700")


# =========================================================
# Helpers
# =========================================================

def fraction_to_decimal(value: Fraction) -> Decimal:
    """Convert an exact Fraction to a high-precision Decimal."""
    return Decimal(value.numerator) / Decimal(value.denominator)


# =========================================================
# Structural values
# =========================================================

@dataclass(frozen=True)
class CosmologicalLocalKinematicValues:
    psi_e_eff: Decimal

    B_alpha: Decimal
    omega_b_st: Decimal
    omega_st: Decimal

    megaparsec_m: Decimal
    H_st: Decimal
    H_st_si: Decimal
    H_ladder_st: Decimal

    T_alpha_st: Decimal
    a_st: Decimal

    c_closure_m_per_s: Decimal
    v_LS_st_m_per_s: Decimal
    v_LS_st_km_per_s: Decimal


def compute_cosmological_kinematic_values(
    constants: StructuralConstants,
) -> CosmologicalLocalKinematicValues:
    r"""Compute the unified Paper 7 structural chain.

        B_alpha     = 3 R^2 / S

        Omega_b,st  = 1 / (3 R^2 + 3 R)
        omega_st    = 4 pi B_alpha / Psi_e,eff
        H_st        = 100 sqrt(omega_st / Omega_b,st)

        H_ladder,st = (R/2) H_st
        T_alpha,st  = B_alpha H_st^(-1)
        a_st        = 2 c T_alpha,st^(-1)

        c_closure   = (1/2) a_st B_alpha H_st^(-1)
        v_LS,st     = (1/8) a_st B_alpha^(-1) H_st^(-1)

    H_st is converted to SI before it enters the time, acceleration,
    closure, and velocity relations.
    """
    R            = fraction_to_decimal(constants.R)
    B_alpha      = fraction_to_decimal(constants.B_alpha)

    psi_electron = compute_psi_values(constants)
    psi_e_eff    = fraction_to_decimal(psi_electron.psi_e - psi_electron.delta_e)

    omega_b_st   = 1 / (3 * R**2 + 3 * R)
    omega_st     = 4 * PI * B_alpha / psi_e_eff
    H_st         = Decimal(100) * (omega_st / omega_b_st).sqrt()

    # 1 pc = (648000 / pi) au; 1 Mpc = 10^6 pc.
    megaparsec_m = AU_M * Decimal(648000) / PI * Decimal(10)**6
    H_st_si      = H_st * Decimal(1000) / megaparsec_m

    H_ladder_st  = (R / 2) * H_st
    T_alpha_st   = B_alpha / H_st_si
    a_st         = 2 * c / T_alpha_st

    c_closure_m_per_s = (Decimal(1) / 2) * a_st * B_alpha / H_st_si
    v_LS_st_m_per_s   = (Decimal(1) / 8) * a_st / B_alpha / H_st_si

    return CosmologicalLocalKinematicValues(
        psi_e_eff=psi_e_eff,
        B_alpha=B_alpha,
        omega_b_st=omega_b_st,
        omega_st=omega_st,
        megaparsec_m=megaparsec_m,
        H_st=H_st,
        H_st_si=H_st_si,
        H_ladder_st=H_ladder_st,
        T_alpha_st=T_alpha_st,
        a_st=a_st,
        c_closure_m_per_s=c_closure_m_per_s,
        v_LS_st_m_per_s=v_LS_st_m_per_s,
        v_LS_st_km_per_s=v_LS_st_m_per_s * Decimal(10)**-3,
    )
