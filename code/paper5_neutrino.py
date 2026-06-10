"""
Zero Parameter Structure — Paper 5 Neutrino Mass Execution

No free parameters. No tuning. Only structure.
"""

from fractions import Fraction
from decimal import Decimal, getcontext

from core.structural_constants import StructuralConstants
from core.structural_neutrino import compute_neutrino_mass_ratios, compute_neutrino_masses
from observed_data.observed_data_pdg import PDG_OBSERVED, ObservedValue

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
    print(f"  theory      = {theory:.18f}")
    print(f"  observation = {obs.value:.12f}")
    if obs.uncertainty is not None:
        print(f"  uncertainty = {obs.uncertainty:.12f}")
    print(f"  abs diff    = {absolute_diff(theory, obs.value):+.9e}")
    print(f"  rel diff    = {relative_diff_percent(theory, obs.value):+.16f} %")
    sigma = sigma_diff(theory, obs)
    if sigma is not None:
        print(f"  sigma       = {sigma:+.6f}")
    print()


# =========================================================
# Main
# =========================================================

def main() -> None:
    constants = StructuralConstants()
    ratios = compute_neutrino_mass_ratios(constants)
    masses = compute_neutrino_masses(constants)

    print("Structural Origin of Neutrino Mass Relations")
    print("===============================")
    print(f"R = {format_fraction(constants.R):>5} = {fraction_to_decimal(constants.R):.12f}")
    print(f"S = {format_fraction(constants.S):>5} = {fraction_to_decimal(constants.S):.12f}")
    print()

    print("Neutrino mass ratios")
    print("--------------------")
    print(f"m1 / me = {ratios.m1_over_me:.18e}")
    print(f"m2 / me = {ratios.m2_over_me:.18e}")
    print(f"m3 / me = {ratios.m3_over_me:.18e}")
    print()

    print("Derived neutrino masses")
    print("-----------------------")
    print(f"m1 c^2 = {masses.m1_ev:.18f} eV")
    print(f"m2 c^2 = {masses.m2_ev:.18f} eV")
    print(f"m3 c^2 = {masses.m3_ev:.18f} eV")
    print(f"Sum mnu = {masses.sum_mnu_ev:.12f} eV")
    print()

    print("Neutrino mass-squared differences")
    print("----------------------------------")
    print(f"Delta m21^2 = {masses.delta_m21_ev2:.12e} eV^2")
    print(f"Delta m31^2 = {masses.delta_m31_ev2:.12e} eV^2")
    print(f"Delta m32^2 = {masses.delta_m32_ev2:.12e} eV^2")
    print()

    print("Comparison with observed data")
    print("-----------------------------")
    print_comparison("Delta m21^2", masses.delta_m21_ev2, PDG_OBSERVED["neutrino_delta_m21"])
    print_comparison("Delta m32^2", masses.delta_m32_ev2, PDG_OBSERVED["neutrino_delta_m32"])


if __name__ == "__main__":
    main()
