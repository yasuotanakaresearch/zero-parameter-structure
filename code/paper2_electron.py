"""
Zero Parameter Structure — Paper 2 Electron Execution

No free parameters. No tuning. Only structure.
"""

from fractions import Fraction
from decimal import Decimal, getcontext

from core.structural_constants import StructuralConstants
from core.structural_electron import compute_psi_values, compute_theory
from observed_data.observed_data_codata import OBSERVED, ObservedValue

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
    psi = compute_psi_values(constants)
    theory = compute_theory(constants, psi)

    print("Structural Electroweak Relations: Theory vs Observation")
    print("===============================")
    print(f"R = {format_fraction(constants.R):>5} = {fraction_to_decimal(constants.R):.12f}")
    print(f"S = {format_fraction(constants.S):>5} = {fraction_to_decimal(constants.S):.12f}")
    print()

    print("Psi values")
    print("----------")
    print(f"Psi_e   = {fraction_to_decimal(psi.psi_e  ) - fraction_to_decimal(psi.delta_e  ):.12f}")
    print(f"Psi_p   = {fraction_to_decimal(psi.psi_p  ) + fraction_to_decimal(psi.delta_p  ):.12f}")
    print(f"Psi_n   = {fraction_to_decimal(psi.psi_n  ) - fraction_to_decimal(psi.delta_n  ):.12f}")
    print(f"Psi_mu  = {fraction_to_decimal(psi.psi_mu ) - fraction_to_decimal(psi.delta_mu ):.12f}")
    print(f"Psi_tau = {fraction_to_decimal(psi.psi_tau) + fraction_to_decimal(psi.delta_tau):.12f}")
    print(f"Psi_me* = {format_fraction(theory.psi_me_star):>7}")
    print(f"Psi_me  = {format_fraction(theory.psi_me):>7}")
    print()

    print("Theoretical values")
    print("------------------")
    print(f"alpha^-1      = {theory.alpha_inv:.18f}")
    print(f"m_p / m_e     = {theory.proton_ratio:.18f}")
    print(f"m_n / m_e     = {theory.neutron_ratio:.18f}")
    print(f"m_mu / m_e    = {theory.muon_ratio:.18f}")
    print(f"m_tau / m_mu  = {theory.tau_from_mu_ratio:.18f}")
    print(f"m_tau / m_e   = {theory.tau_from_e_ratio:.18f}")
    print(f"m_e c^2       = {fraction_to_decimal(theory.electron_mass_scale):.18f}")
    print()

    # Convert dimensionless ratios (normalized to m_e) into physical energy units (MeV → GeV/eV)
    me_c2_mev  = fraction_to_decimal(theory.electron_mass_scale) * Decimal(10**-6)

    print("Comparison with observation")
    print("---------------------------")
    print_comparison("alpha^-1", theory.alpha_inv, OBSERVED["alpha_inv"])
    print_comparison("m_p / m_e", theory.proton_ratio, OBSERVED["proton_ratio"])
    print_comparison("m_n / m_e", theory.neutron_ratio, OBSERVED["neutron_ratio"])
    print_comparison("m_mu / m_e", theory.muon_ratio, OBSERVED["muon_ratio"])
    print_comparison("m_tau / m_mu", theory.tau_from_mu_ratio, OBSERVED["tau-muon_mass_ratio"])
    print_comparison("m_tau / m_e", theory.tau_from_e_ratio, OBSERVED["tau-electron_mass_ratio"])
    print_comparison("m_e", me_c2_mev, OBSERVED["electron_rest_energy_mev"])

    print("\nDerived masses")
    print("--------------")
    print(f"m_mu c^2      = {theory.muon_ratio * me_c2_mev:.18f} MeV")
    print(f"m_tau c^2     = {theory.tau_from_e_ratio * me_c2_mev:.18f} MeV")
    print(f"m_p c^2       = {theory.proton_ratio * me_c2_mev:.18f} MeV")
    print(f"m_n c^2       = {theory.neutron_ratio * me_c2_mev:.18f} MeV")
    print(f"m_e c^2       = {me_c2_mev:.18f} MeV")


if __name__ == "__main__":
    main()
