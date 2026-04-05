"""
Zero Parameter Structure — Paper 2 Electroweak Execution

No free parameters. No tuning. Only structure.
"""

from fractions import Fraction

from core.structural_constants import StructuralConstants
from core.structural_electroweak import compute_psi_values, compute_theory
from observed_data.observed_data_codata import OBSERVED, ObservedValue
from observed_data.observed_data_pdg import PDG_OBSERVED
from observed_data.observed_data_reference import REF_OBSERVED


# =========================================================
# Reporting helpers
# =========================================================

def format_fraction(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def absolute_diff(theory: float, obs: float) -> float:
    return theory - obs


def relative_diff_percent(theory: float, obs: float) -> float:
    return 100.0 * (theory - obs) / obs


def print_comparison(label: str, theory: float, obs: ObservedValue) -> None:
    print(label)
    print(f"  theory      = {theory:.12f}")
    print(f"  observation = {obs.value:.12f}")
    if obs.uncertainty is not None:
        print(f"  uncertainty = {obs.uncertainty:.12f}")
    print(f"  abs diff    = {absolute_diff(theory, obs.value):+.12e}")
    print(f"  rel diff    = {relative_diff_percent(theory, obs.value):+.9f} %")
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
    print(f"R = {format_fraction(constants.R):>5} = {float(constants.R):.12f}")
    print(f"Z = {format_fraction(constants.Z):>5} = {float(constants.Z):.12f}")
    print()

    print("Psi values")
    print("----------")
    print(f"Psi_e   = {format_fraction(psi.psi_e):>7} = {float(psi.psi_e):.1f}")
    print(f"Psi_p   = {format_fraction(psi.psi_p):>7} = {float(psi.psi_p):.1f}")
    print(f"Psi_n   = {format_fraction(psi.psi_n):>7} = {float(psi.psi_n):.1f}")
    print(f"Psi_mu  = {format_fraction(psi.psi_mu):>7} = {float(psi.psi_mu):.1f}")
    print(f"Psi_tau = {format_fraction(psi.psi_tau):>7} = {float(psi.psi_tau):.1f}")
    print()

    print("Theoretical values")
    print("------------------")
    print(f"alpha^-1      = {theory.alpha_inv:.12f}")
    print(f"m_p / m_e     = {theory.proton_ratio:.12f}")
    print(f"m_n / m_e     = {theory.neutron_ratio:.12f}")
    print(f"m_mu / m_e    = {theory.muon_ratio:.12f}")
    print(f"m_tau / m_mu  = {theory.tau_from_mu_ratio:.12f}")
    print(f"m_tau / m_e   = {theory.tau_from_e_ratio:.12f}")
    print(f"m_H / m_e     = {theory.higgs_value:.12f}")
    print(f"v_EW / m_e    = {theory.vev_value:.12f}")
    print(f"m_nu / m_e    = {theory.neutrino_ratio:.12e}")
    print()

    # Convert dimensionless ratios (normalized to m_e) into physical energy units (MeV → GeV/eV)
    me_c2     = OBSERVED["electron_rest_energy_mev"].value
    higgs_gev = theory.higgs_value * me_c2 / 1000.0
    vev_gev   = theory.vev_value * me_c2 / 1000.0
    m_nu_ev   = theory.neutrino_ratio * me_c2 * 1.0e6

    print("Comparison with observation")
    print("---------------------------")
    print_comparison("alpha^-1", theory.alpha_inv, OBSERVED["alpha_inv"])
    print_comparison("m_p / m_e", theory.proton_ratio, OBSERVED["proton_ratio"])
    print_comparison("m_n / m_e", theory.neutron_ratio, OBSERVED["neutron_ratio"])
    print_comparison("m_mu / m_e", theory.muon_ratio, OBSERVED["muon_ratio"])
    print_comparison("m_tau / m_mu", theory.tau_from_mu_ratio, PDG_OBSERVED["tau_from_mu_ratio"])
    print_comparison("m_tau / m_e", theory.tau_from_e_ratio, PDG_OBSERVED["tau_ratio"])
    print_comparison("m_H / m_e", higgs_gev, PDG_OBSERVED["higgs_mass_gev_repr"])
    print_comparison("v_EW / m_e", vev_gev, REF_OBSERVED["vev_gev"])

    print("Derived masses")
    print("--------------")
    print(f"m_e c^2 (Ref.) = {me_c2:.12f} MeV")
    print(f"m_mu c^2       = {theory.muon_ratio * me_c2:.12f} MeV")
    print(f"m_tau c^2      = {theory.tau_from_e_ratio * me_c2:.12f} MeV")
    print(f"m_p c^2        = {theory.proton_ratio * me_c2:.12f} MeV")
    print(f"m_n c^2        = {theory.neutron_ratio * me_c2:.12f} MeV")
    print(f"m_H c^2        = {higgs_gev:.12f} GeV")
    print(f"v_EW           = {vev_gev:.12f} GeV")
    print(f"m_nu c^2       = {m_nu_ev:.12f} eV")


if __name__ == "__main__":
    main()
