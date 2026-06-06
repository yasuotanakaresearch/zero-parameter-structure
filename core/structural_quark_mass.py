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
from core.structural_electron import compute_psi_values, compute_electron_mass_path

getcontext().prec = 56

PI = Decimal("3.14159265358979323846264338327950288419716939937510")


# =========================================================
# helpers
# =========================================================

def fraction_to_decimal(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


# =========================================================
# Psi values
# =========================================================

@dataclass(frozen=True)
class PsiQuark:
    psi_u: Fraction
    psi_d: Fraction


def compute_psi_quark(constants: StructuralConstants) -> PsiQuark:
    """
    Construct the structural Psi values for the quark sector.

    Interpretation:
    - psi_d : base down-type structural index
    - psi_u : up-type index obtained by propagation through R

    Structure:

        Ψd = 2
        Ψu = Ψd * R = 2R
    """
    R = constants.R

    psi_d = Fraction(2, 1)
    psi_u = psi_d * R

    return PsiQuark(
        psi_u=Fraction(psi_u),
        psi_d=Fraction(psi_d),
    )


# =========================================================
# Quark rows and results
# =========================================================

@dataclass(frozen=True)
class QuarkRow:
    symbol: str
    k_value: Fraction
    u_selector: int
    n_power: int
    unit: str = "MeV"


@dataclass(frozen=True)
class QuarkMassResult:
    symbol: str
    k_value: Fraction
    u_selector: int
    n_power: int
    mass_mev: Decimal
    mass_display: Decimal
    unit: str


@dataclass(frozen=True)
class QuarkMassResults:
    psi: PsiQuark
    base_ratio: Fraction
    rows: tuple[QuarkMassResult, ...]


# =========================================================
# Structural formulas
# =========================================================

def base_ratio(constants: StructuralConstants) -> Fraction:
    """
    Common quark-mass base ratio.

        M0 / me = 3R^2 S
    """
    R = constants.R
    S = constants.S
    return 3 * R**2 * S


def propagation_factor(
    constants: StructuralConstants,
    u_selector: int,
) -> Decimal:
    """
    Unified propagation/projection factor.

        F(u) = 8 π^u R^(u+1) / S

    where:
    - u = 0 gives the down-type factor 8R/S
    - u = 1 gives the up-type factor 8πR^2/S
    """
    R = fraction_to_decimal(constants.R)
    S = fraction_to_decimal(constants.S)
    u = int(u_selector)

    return Decimal(8) * (PI ** u) * (R ** (u + 1)) / S


def quark_mass_ratio(
    constants: StructuralConstants,
    row: QuarkRow,
) -> Decimal:
    """
    Unified structural quark-mass ratio.

        mq / me = Kq (3R^2 S) [8 π^u R^(u+1) / S]^n
    """
    k = fraction_to_decimal(row.k_value)
    base = fraction_to_decimal(base_ratio(constants))
    factor = propagation_factor(constants, row.u_selector)

    return k * base * (factor ** row.n_power)


def quark_mass_mev(
    constants: StructuralConstants,
    row: QuarkRow,
) -> Decimal:
    """
    Project the dimensionless quark-mass ratio onto MeV using me.
    """
    psi_electron = compute_psi_values(constants)
    electron_path = compute_electron_mass_path(constants, psi_electron)
    me_c2_mev = fraction_to_decimal(electron_path.mass_scale) * Decimal(10**-6)

    return quark_mass_ratio(constants, row) * me_c2_mev


def quark_rows(psi: PsiQuark) -> tuple[QuarkRow, ...]:
    """
    Construct the quark-sector structural table in the order
    (u, d, c, s, t, b).

    Kq values:
        Ku = 1/Ψu
        Kd = 1/Ψd
        Kc = 1 + 1/Ψd
        Ks = 1 - 1/(2Ψd)
        Kt = 2 + 1/Ψu
        Kb = 2 + 1/Ψd
    """
    psi_u = psi.psi_u
    psi_d = psi.psi_d

    return (
        QuarkRow("u", Fraction(1, 1) / psi_u, 0, 0, "MeV"),
        QuarkRow("d", Fraction(1, 1) / psi_d, 0, 0, "MeV"),
        QuarkRow("c", Fraction(1, 1) + Fraction(1, 1) / psi_d, 1, 1, "MeV"),
        QuarkRow("s", Fraction(1, 1) - Fraction(1, 1) / (2 * psi_d), 0, 1, "MeV"),
        QuarkRow("t", Fraction(2, 1) + Fraction(1, 1) / psi_u, 1, 2, "MeV"),
        QuarkRow("b", Fraction(2, 1) + Fraction(1, 1) / psi_d, 0, 2, "MeV"),
    )


def compute_quark_masses(
    constants: StructuralConstants,
) -> QuarkMassResults:
    psi = compute_psi_quark(constants)
    rows: list[QuarkMassResult] = []

    for row in quark_rows(psi):
        mass_mev = quark_mass_mev(constants, row)
        mass_display = mass_mev / Decimal(1000) if row.unit == "GeV" else mass_mev

        rows.append(
            QuarkMassResult(
                symbol=row.symbol,
                k_value=row.k_value,
                u_selector=row.u_selector,
                n_power=row.n_power,
                mass_mev=mass_mev,
                mass_display=mass_display,
                unit=row.unit,
            )
        )

    return QuarkMassResults(
        psi=psi,
        base_ratio=base_ratio(constants),
        rows=tuple(rows),
    )

