"""
Zero Parameter Structure — Paper 3 Gravity Execution

No free parameters. No tuning. Only structure.
"""

from fractions import Fraction
from decimal import Decimal, getcontext

from core.structural_constants import StructuralConstants
from core.structural_electron import compute_psi_values
from core.structural_gravity import compute_psi_gravity, compute_gravity
from observed_data.observed_data_codata import OBSERVED, ObservedValue
from observed_data.observed_data_reference import REF_OBSERVED, ObservedValue

getcontext().prec = 56


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
    if obs.uncertainty is None or obs.uncertainty == 0.0:
        return None
    return (Decimal(theory) - Decimal(obs.value)) / Decimal(obs.uncertainty)


def print_comparison(label: str, theory: Decimal, obs: ObservedValue) -> None:
    print(label)
    print(f"  theory      = {theory:.12e}")
    print(f"  observation = {obs.value:.12e}")
    if obs.uncertainty is not None:
        print(f"  uncertainty = {obs.uncertainty:.12e}")
    print(f"  abs diff    = {absolute_diff(theory, obs.value):+.12e}")
    print(f"  rel diff    = {relative_diff_percent(theory, obs.value):+.12f} %")
    sigma = sigma_diff(theory, obs)
    if sigma is not None:
        print(f"  sigma       = {sigma:+.6f}")
    print()


# =========================================================
# Main
# =========================================================

def main() -> None:
    constants = StructuralConstants()
    psi_electron = compute_psi_values(constants)

    psi_g = compute_psi_gravity(constants, psi_electron)
    result = compute_gravity(constants, psi_electron)

    print("Structural Gravity Relations: Theory vs Observation")
    print("====================================")
    print(f"R = {format_fraction(constants.R):>5} = {fraction_to_decimal(constants.R):.12f}")
    print(f"S = {format_fraction(constants.S):>5} = {fraction_to_decimal(constants.S):.12f}")
    print()

    print("Psi values")
    print("----------")
    print(f"Psi_G  = {format_fraction(psi_g.psi_g):>7} = {fraction_to_decimal(psi_g.psi_g):.2f}")
    print(f"Psi_G* = {format_fraction(psi_g.psi_g_star):>7} = {fraction_to_decimal(psi_g.psi_g_star):.12f}")
    print()

    print("Theoretical values")
    print("------------------")
    print(f"alpha_Gp    = {result.alpha_gp:.12e}")
    print(f"alpha_Ge    = {result.alpha_ge:.12e}")
    print(f"sqrt(G)     = {result.sqrt_g:.12e}")
    print(f"G           = {result.g_value:.12e}")
    print(f"M_Pl        = {result.planck_mass:.12e} kg")
    print(f"M_P         = {result.mp_value:.12e} kg")
    print(f"M_E         = {result.me_value:.12e} kg")
    print()

    print("Comparison with observation")
    print("---------------------------")
    print_comparison("G", result.g_value, OBSERVED["gravitational_constant"])
    print_comparison("M_Pl", result.planck_mass, OBSERVED["planck_mass"])
    print_comparison("M_P", result.mp_value, OBSERVED["proton_mass"])
    print_comparison("M_E", result.me_value, OBSERVED["electron_mass"])


if __name__ == "__main__":
    main()
