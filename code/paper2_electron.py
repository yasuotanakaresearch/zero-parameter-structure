"""
Zero Parameter Structure — Paper 2 Electron Execution

No free parameters. No tuning. Only structure.
"""

from decimal import Decimal, getcontext
from fractions import Fraction

from core.structural_constants import StructuralConstants
from core.structural_electron import (
    alpha_running_coefficients,
    compute_alpha_running_sample,
    compute_psi_values,
    compute_theory,
    k_n,
)
from observed_data.observed_data_codata import OBSERVED, ObservedValue
from observed_data.observed_data_pdg import PAPER2_ALPHA_INV_RGE_REFERENCE

getcontext().prec = 56


# =========================================================
# Appendix A inputs: characteristic mass scales
# =========================================================
# The mass scales are comparison inputs, not adjustable parameters.
# The logarithmic denominator m_e is calculated from the Paper 2 theory.

APPENDIX_MASS_SCALES_GEV = {
    "m_mu": Decimal("0.105658"),
    "m_tau": Decimal("1.776860"),
    "m_b": Decimal("4.184843"),
    "m_W": Decimal("80.3692"),
    "m_Z": Decimal("91.1876"),
    "m_t": Decimal("173.0126"),
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


def print_alpha_running_table(alpha_inv_zero: Decimal, electron_mass_gev: Decimal) -> None:
    """Print the Appendix A discrete logarithmic comparison.

    The structural samples are compared with the separate PDG/RGE reference
    table.  This is a characteristic-scale comparison, not a replacement for
    the continuous QED beta-function evolution.
    """
    coefficients = alpha_running_coefficients()
    coefficient_map = {
        "m_mu": coefficients.muon,
        "m_tau": coefficients.tau,
        "m_b": coefficients.bottom,
        "m_W": coefficients.w_boson,
        "m_Z": coefficients.z_boson,
        "m_t": coefficients.top,
    }

    samples = [
        compute_alpha_running_sample(
            label=label,
            mass_gev=mass_gev,
            electron_mass_gev=electron_mass_gev,
            coefficient=coefficient_map[label],
            alpha_inv_zero=alpha_inv_zero,
        )
        for label, mass_gev in APPENDIX_MASS_SCALES_GEV.items()
    ]

    print("\nAppendix A: logarithmic sampling of alpha^-1(Q)")
    print("------------------------------------------------")
    print("K_n = (1 + 1/n)^-1 = n/(n + 1)")
    print(
        f"K_2 = {format_fraction(k_n(2))}, "
        f"K_3 = {format_fraction(k_n(3))}, "
        f"K_4 = {format_fraction(k_n(4))}"
    )
    print(f"alpha^-1(0) = {alpha_inv_zero:.18f}")
    print(f"m_e         = {electron_mass_gev:.18f} GeV")
    print()
    print(
        f"{'scale':<7} {'Q [GeV]':>12} {'K_alpha':>10} "
        f"{'Delta_st':>12} {'alpha^-1 st':>13} "
        f"{'PDG/RGE ref':>13} {'abs diff':>11} {'rel diff':>10}"
    )
    print("-" * 105)

    absolute_relative_differences: list[Decimal] = []

    for sample in samples:
        try:
            reference = Decimal(str(PAPER2_ALPHA_INV_RGE_REFERENCE[sample.label]))
        except KeyError as exc:
            raise KeyError(
                f"Missing Paper 2 alpha reference for {sample.label!r}"
            ) from exc

        difference = absolute_diff(sample.alpha_inv, reference)
        relative = relative_diff_percent(sample.alpha_inv, reference)
        absolute_relative_differences.append(abs(relative))

        print(
            f"{sample.label:<7} "
            f"{sample.mass_gev:>12.6f} "
            f"{format_fraction(sample.coefficient):>10} "
            f"{sample.delta_alpha_inv:>12.6f} "
            f"{sample.alpha_inv:>13.6f} "
            f"{reference:>13.6f} "
            f"{difference:>+11.6f} "
            f"{relative:>+9.4f}%"
        )

    mean_abs = (
        sum(absolute_relative_differences, Decimal(0))
        / Decimal(len(absolute_relative_differences))
    )
    max_abs = max(absolute_relative_differences)

    print()
    print(f"mean absolute relative difference = {mean_abs:.6f} %")
    print(f"maximum absolute relative difference = {max_abs:.6f} %")
    print(
        "Reference note: m_mu, m_tau, and m_Z are PDG-anchored MSbar values; "
        "m_b, m_W, and m_t are representative RGE continuations."
    )


# =========================================================
# Main
# =========================================================

def main() -> None:
    constants = StructuralConstants()
    psi = compute_psi_values(constants)
    theory = compute_theory(constants, psi)

    print("Structural Electroweak Relations: Theory vs Observation")
    print("=======================================================")
    print(f"R = {format_fraction(constants.R):>5} = {fraction_to_decimal(constants.R):.12f}")
    print(f"S = {format_fraction(constants.S):>5} = {fraction_to_decimal(constants.S):.12f}")
    print()

    print("Psi values")
    print("----------")
    print(f"Psi_e   = {fraction_to_decimal(psi.psi_e) - fraction_to_decimal(psi.delta_e):.12f}")
    print(f"Psi_p   = {fraction_to_decimal(psi.psi_p) + fraction_to_decimal(psi.delta_p):.12f}")
    print(f"Psi_n   = {fraction_to_decimal(psi.psi_n) - fraction_to_decimal(psi.delta_n):.12f}")
    print(f"Psi_mu  = {fraction_to_decimal(psi.psi_mu) - fraction_to_decimal(psi.delta_mu):.12f}")
    print(f"Psi_tau = {fraction_to_decimal(psi.psi_tau) + fraction_to_decimal(psi.delta_tau):.12f}")
    print(f"Psi_me* = {format_fraction(theory.psi_me_star):>6}")
    print(f"Psi_me  = {format_fraction(theory.psi_me):>6}")
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

    # Convert the structural electron energy scale into MeV and GeV.
    me_c2_mev = fraction_to_decimal(theory.electron_mass_scale) * Decimal("1e-6")
    me_c2_gev = me_c2_mev * Decimal("1e-3")

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
    print_comparison("m_e", me_c2_mev, OBSERVED["electron_rest_energy_mev"])

    print("\nDerived masses")
    print("--------------")
    print(f"m_mu c^2      = {theory.muon_ratio * me_c2_mev:.18f} MeV")
    print(f"m_tau c^2     = {theory.tau_from_e_ratio * me_c2_mev:.18f} MeV")
    print(f"m_p c^2       = {theory.proton_ratio * me_c2_mev:.18f} MeV")
    print(f"m_n c^2       = {theory.neutron_ratio * me_c2_mev:.18f} MeV")
    print(f"m_e c^2       = {me_c2_mev:.18f} MeV")

    print_alpha_running_table(theory.alpha_inv, me_c2_gev)


if __name__ == "__main__":
    main()
