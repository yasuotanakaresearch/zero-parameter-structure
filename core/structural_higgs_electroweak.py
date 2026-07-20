"""
Zero Parameter Structure

Copyright (c) 2026 Yasuo Tanaka
Licensed under the MIT License.

Paper 6 structural formulas for the Higgs, electroweak,
Yukawa, and strong-coupling scale relations.

No free parameters. No tuning. Only structure.
"""

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction
from typing import Iterable

from core.structural_constants import StructuralConstants
from core.structural_electron import (
    alpha_inverse,
    compute_electron_mass_path,
    compute_psi_values,
)

getcontext().prec = 56

PI = Decimal("3.1415926535897932384626433832795028841971693993751")


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
# Structural values
# =========================================================

@dataclass(frozen=True)
class HiggsElectroweakValues:
    alpha_inverse: Decimal
    alpha: Decimal
    electron_mass_ev: Decimal

    B_H: Decimal
    psi_H: Decimal
    psi_v: Decimal

    mH_over_me: Decimal
    v_over_me: Decimal
    mH_gev: Decimal
    v_gev: Decimal

    electron_yukawa: Decimal
    sin2_theta_w: Decimal
    cos_theta_w: Decimal

    mW_over_me: Decimal
    mW_gev: Decimal
    mZ_gev: Decimal
    alpha_s_mZ: Decimal


@dataclass(frozen=True)
class QCDContinuation:
    md_over_me: Decimal
    A_s: Decimal
    lambda_star_gev: Decimal
    alpha_s_mZ: Decimal


def compute_higgs_electroweak_values(
    constants: StructuralConstants,
) -> HiggsElectroweakValues:
    r"""Compute the unified Paper 6 structural chain.

        B_H = 12 R alpha^2_[1->2] = 12 R alpha^(-2)

        m_H / m_e = (1/2) B_H + Psi_H
        v   / m_e = B_H - Psi_v
    """
    R = fraction_to_decimal(constants.R)

    psi_electron = compute_psi_values(constants)
    alpha_inv    = alpha_inverse(constants, psi_electron)
    alpha        = 1 / alpha_inv

    electron_path = compute_electron_mass_path(constants, psi_electron)
    me_st  = fraction_to_decimal(electron_path.mass_scale)
    me_gev = me_st * Decimal(10**-9)

    B_H   = 12 * R * alpha2_transfer(alpha, 1, 2)
    psi_H = 12 * (4 * (3 * R**2) + 3)
    psi_v = 3 ** 2 * psi_H

    mH_over_me = Decimal(2**-1) * B_H + psi_H
    v_over_me  = B_H - psi_v

    mH_gev = mH_over_me * me_gev
    v_gev  = v_over_me  * me_gev

    electron_yukawa = Decimal(2).sqrt() / v_over_me
    sin2_theta_w    = 2 * PI * alpha * R**2 * (1 + Decimal(3**-3))
    cos_theta_w     = (1 - sin2_theta_w).sqrt()

    mW_over_me = (electron_yukawa**-1) / R * (1 + psi_v**-1)
    mW_gev     = mW_over_me * me_gev
    mZ_gev     = mW_gev / cos_theta_w
    alpha_s_mZ = 1 - (mW_gev / mZ_gev)

    return HiggsElectroweakValues(
        alpha_inverse=alpha_inv,
        alpha=alpha,
        electron_mass_ev=me_st,
        B_H=B_H,
        psi_H=psi_H,
        psi_v=psi_v,
        mH_over_me=mH_over_me,
        v_over_me=v_over_me,
        mH_gev=mH_gev,
        v_gev=v_gev,
        electron_yukawa=electron_yukawa,
        sin2_theta_w=sin2_theta_w,
        cos_theta_w=cos_theta_w,
        mW_over_me=mW_over_me,
        mW_gev=mW_gev,
        mZ_gev=mZ_gev,
        alpha_s_mZ=alpha_s_mZ,
    )


def compute_qcd_continuation(
    constants: StructuralConstants,
    values: HiggsElectroweakValues | None = None,
) -> QCDContinuation:
    """Compute the Appendix-level effective alpha_s(Q) continuation."""
    if values is None:
        values = compute_higgs_electroweak_values(constants)

    R = fraction_to_decimal(constants.R)
    S = fraction_to_decimal(constants.S)

    md_over_me      = Decimal(2**-1) * (3 * R**2 * S)
    A_s             = 4 * PI / md_over_me
    exponent        = -1 / (A_s * values.alpha_s_mZ)
    lambda_star_gev = values.mZ_gev * exponent.exp()

    return QCDContinuation(
        md_over_me=md_over_me,
        A_s=A_s,
        lambda_star_gev=lambda_star_gev,
        alpha_s_mZ=values.alpha_s_mZ,
    )


def alpha_s_at_scale(Q_gev: Decimal, continuation: QCDContinuation) -> Decimal:
    r"""Return the illustrative effective continuation

        alpha_s(Q)
        = (8/9) alpha_s^(0)(Q) + (1/9) alpha_s(m_Z),

        alpha_s^(0)(Q)
        = 1 / [A_s ln(Q/Lambda_*)].
    """
    Q_gev = Decimal(Q_gev)
    if Q_gev <= continuation.lambda_star_gev:
        raise ValueError("Q_gev must be greater than Lambda_*.")

    alpha_s0 = (continuation.A_s * (Q_gev / continuation.lambda_star_gev).ln())**-1

    return (
        Decimal(8 / 9) * alpha_s0 +
        Decimal(9**-1) * continuation.alpha_s_mZ
    )


def alpha_s_scale_table(
    scales: Iterable[tuple[str, Decimal]],
    continuation: QCDContinuation,
) -> tuple[tuple[str, Decimal, Decimal], ...]:
    """Evaluate alpha_s(Q) for labeled scales."""
    return tuple(
        (label, Decimal(Q_gev), alpha_s_at_scale(Decimal(Q_gev), continuation))
        for label, Q_gev in scales
    )

