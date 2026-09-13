"""
Zero Parameter Structure — Paper 2 Electron Execution

Version 1.1

No free parameters. No tuning. Only structure.
"""

from decimal import Decimal, getcontext
from fractions import Fraction

from core.structural_constants import StructuralConstants, q, q_sharp
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
    if Decimal(obs) == 0:
        raise ValueError("reference value must be nonzero")
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
    print(f"  abs diff    = {absolute_diff(theory, Decimal(str(obs.value))):+.9e}")
    print(
        "  rel diff    = "
        f"{relative_diff_percent(theory, Decimal(str(obs.value))):+.16f} %"
    )
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

    print("Structural Origin of Electromagnetic Coupling and Mass Hierarchy")
    print("Paper 2 — Version 1.1")
    print("===============================================================")
    print(f"q       = {q}")
    print(f"q_#     = {q_sharp}")
    print(
        f"R(q)    = {format_fraction(constants.R):>5}"
        f" = {fraction_to_decimal(constants.R):.12f}"
    )
    print(
        f"S(q^2)  = {format_fraction(constants.S):>5}"
        f" = {fraction_to_decimal(constants.S):.12f}"
    )
    print()

    print("Version 1.1 structural indices")
    print("------------------------------")
    print(f"C_e      = {format_fraction(psi.Ce)}")
    print(f"Psi_Gp   = {format_fraction(psi.psi_Gp)}")
    print()

    print(f"Psi_e0   = {format_fraction(psi.psi_e0)}")
    print(f"Psi_e*   = {format_fraction(psi.psi_e_star)}")
    print(f"Psi_e    = {fraction_to_decimal(psi.psi_e):.12f}")
    print()

    print(f"Psi_p0   = {format_fraction(psi.psi_p0)}")
    print(f"Psi_p*   = {format_fraction(psi.psi_p_star)}")
    print(f"Psi_p    = {fraction_to_decimal(psi.psi_p):.12f}")
    print()

    print(f"Psi_n0   = {format_fraction(psi.psi_n0)}")
    print(f"Psi_n*   = {format_fraction(psi.psi_n_star)}")
    print(f"Psi_n    = {fraction_to_decimal(psi.psi_n):.12f}")
    print()

    print(f"Psi_mu0  = {format_fraction(psi.psi_mu0)}")
    print(f"Psi_mu*  = {format_fraction(psi.psi_mu_star)}")
    print(f"Psi_mu   = {fraction_to_decimal(psi.psi_mu):.12f}")
    print(f"Psi_tau  = {format_fraction(psi.psi_tau)}")
    print()

    print("Version 1.1 exact closure checks")
    print("--------------------------------")
    print(f"Psi_me   = {format_fraction(theory.psi_me)}")
    print(f"Psi_me*  = {format_fraction(theory.psi_me_star)}")
    print(
        "Psi_Gp[e-n reconstruction] = "
        f"{format_fraction(theory.psi_Gp_from_en)}"
    )
    print()

    print("Theoretical values")
    print("------------------")
    print(f"alpha^-1      = {theory.alpha_inv:.18f}")
    print(f"m_p / m_e     = {theory.proton_ratio:.18f}")
    print(f"m_n / m_e     = {theory.neutron_ratio:.18f}")
    print(f"m_mu / m_e    = {theory.muon_ratio:.18f}")
    print(f"m_tau / m_mu  = {theory.tau_from_mu_ratio:.18f}")
    print(f"m_tau / m_e   = {theory.tau_from_e_ratio:.18f}")
    print(
        "m_e c^2       = "
        f"{fraction_to_decimal(theory.electron_mass_scale):.18f} eV"
    )
    print()

    me_c2_mev = (
        fraction_to_decimal(theory.electron_mass_scale)
        * Decimal("1e-6")
    )

    print("Comparison with observation")
    print("---------------------------")
    print_comparison("alpha^-1", theory.alpha_inv, OBSERVED["alpha_inv"])
    print_comparison("m_p / m_e", theory.proton_ratio, OBSERVED["proton_ratio"])
    print_comparison("m_n / m_e", theory.neutron_ratio, OBSERVED["neutron_ratio"])
    print_comparison("m_mu / m_e", theory.muon_ratio, OBSERVED["muon_ratio"])
    print_comparison(
        "m_tau / m_mu",
        theory.tau_from_mu_ratio,
        OBSERVED["tau-muon_mass_ratio"],
    )
    print_comparison(
        "m_tau / m_e",
        theory.tau_from_e_ratio,
        OBSERVED["tau-electron_mass_ratio"],
    )
    print_comparison(
        "m_e",
        me_c2_mev,
        OBSERVED["electron_rest_energy_mev"],
    )

    print("Derived masses")
    print("--------------")
    print(f"m_mu c^2      = {theory.muon_ratio * me_c2_mev:.18f} MeV")
    print(f"m_tau c^2     = {theory.tau_from_e_ratio * me_c2_mev:.18f} MeV")
    print(f"m_p c^2       = {theory.proton_ratio * me_c2_mev:.18f} MeV")
    print(f"m_n c^2       = {theory.neutron_ratio * me_c2_mev:.18f} MeV")
    print(f"m_e c^2       = {me_c2_mev:.18f} MeV")


if __name__ == "__main__":
    main()
