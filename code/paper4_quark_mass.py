"""
Zero Parameter Structure — Paper 4 Quark Mass Execution

No free parameters. No tuning. Only structure.
"""

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction
from core.structural_constants import StructuralConstants
from core.structural_quark_mass import QuarkMassResult, compute_quark_masses, propagation_factor
from observed_data.observed_data_pdg import PDG_OBSERVED

getcontext().prec = 56


# =========================================================
# Observed data
# =========================================================

@dataclass(frozen=True)
class ObservedValue:
    name: str
    value: Decimal
    uncertainty: Decimal | None = None
    unit: str = "MeV"


# Representative PDG-style quark masses.
# u, d, s are MSbar masses at 2 GeV.
# c and b are running masses at their own scale.
# t is a directly reconstructed mass scale.
OBSERVED_QUARKS = {
    "u": PDG_OBSERVED["quark_u_mass_mev"],
    "d": PDG_OBSERVED["quark_d_mass_mev"],
    "c": PDG_OBSERVED["quark_c_mass_mev"],
    "s": PDG_OBSERVED["quark_s_mass_mev"],
    "t": PDG_OBSERVED["quark_t_mass_mev_direct"],
    "b": PDG_OBSERVED["quark_b_mass_mev"],
}


# =========================================================
# Reporting helpers
# =========================================================

def fraction_to_decimal(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def format_fraction(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def absolute_diff(theory: Decimal, obs: Decimal) -> Decimal:
    return Decimal(theory) - Decimal(obs)


def relative_diff_percent(theory: Decimal, obs: Decimal) -> Decimal:
    return Decimal(100) * (Decimal(theory) - Decimal(obs)) / Decimal(obs)


def sigma_diff(theory: Decimal, obs: ObservedValue) -> Decimal | None:
    if obs.uncertainty is None or obs.uncertainty == 0:
        return None
    return (Decimal(theory) - Decimal(obs.value)) / Decimal(obs.uncertainty)


def print_comparison(label: str, theory: Decimal, obs: ObservedValue) -> None:
    print(label)
    print(f"  theory      = {theory:.12f} {obs.unit}")
    print(f"  observation = {obs.value:.12f} {obs.unit}")
    if obs.uncertainty is not None:
        print(f"  uncertainty = {obs.uncertainty:.12f} {obs.unit}")
    print(f"  abs diff    = {absolute_diff(theory, obs.value):+.12f} {obs.unit}")
    print(f"  rel diff    = {relative_diff_percent(theory, obs.value):+.12f} %")
    sigma = sigma_diff(theory, obs)
    if sigma is not None:
        print(f"  sigma       = {sigma:+.6f}")
    print()


def display_mass(result: QuarkMassResult) -> str:
    return f"{result.mass_display:.12f} {result.unit}"


# =========================================================
# Main
# =========================================================

def main() -> None:
    constants = StructuralConstants()
    result = compute_quark_masses(constants)

    print("Structural Quark Mass Relations: Theory vs Observation")
    print("=====================================================")
    print(f"R = {format_fraction(constants.R):>5} = {fraction_to_decimal(constants.R):.12f}")
    print(f"S = {format_fraction(constants.S):>5} = {fraction_to_decimal(constants.S):.12f}")
    print()

    print("Psi values")
    print("----------")
    print(f"Psi_u = {format_fraction(result.psi.psi_u):>5} = {fraction_to_decimal(result.psi.psi_u):.12f}")
    print(f"Psi_d = {format_fraction(result.psi.psi_d):>5} = {fraction_to_decimal(result.psi.psi_d):.12f}")
    print()

    print("Common structural components")
    print("----------------------------")
    print(f"3R^2 S        = {format_fraction(result.base_ratio):>7} = {fraction_to_decimal(result.base_ratio):.12f}")
    print(f"8 R / S       = {propagation_factor(constants, 0):.12f}")
    print(f"8 pi R^2 / S  = {propagation_factor(constants, 1):.12f}")
    print()

    print("Structural table")
    print("----------------")
    print("q   Kq     u   n   theory")
    print("--  -----  --  --  ----------------")
    for row in result.rows:
        print(
            f"{row.symbol:<2}  "
            f"{format_fraction(row.k_value):>5} "
            f"{row.u_selector:>2}  "
            f"{row.n_power:>2}   "
            f"{display_mass(row)}"
        )
    print()

    print("Comparison with observation")
    print("---------------------------")
    for row in result.rows:
        obs = OBSERVED_QUARKS[row.symbol]
        print_comparison(row.symbol, row.mass_display, obs)


if __name__ == "__main__":
    main()
