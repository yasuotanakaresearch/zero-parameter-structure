"""
Zero Parameter Structure — Paper 3 Gravity Execution

No free parameters. No tuning. Only structure.
"""

from fractions import Fraction

from core.structural_constants import StructuralConstants
from core.structural_electroweak import compute_psi_values, alpha_inverse, proton_mass_ratio
from core.structural_gravity import compute_psi_gravity, compute_gravity
from observed_data.observed_data_reference import REF_OBSERVED, ObservedValue


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


def sigma_diff(theory: float, obs: ObservedValue) -> float | None:
    if obs.uncertainty is None or obs.uncertainty == 0.0:
        return None
    return (theory - obs.value) / obs.uncertainty


def print_comparison(label: str, theory: float, obs: ObservedValue) -> None:
    print(label)
    print(f"  theory      = {theory:.12e}")
    print(f"  observation = {obs.value:.12e}")
    if obs.uncertainty is not None:
        print(f"  uncertainty = {obs.uncertainty:.12e}")
    print(f"  abs diff    = {absolute_diff(theory, obs.value):+.12e}")
    print(f"  rel diff    = {relative_diff_percent(theory, obs.value):+.9f} %")
    sigma = sigma_diff(theory, obs)
    if sigma is not None:
        print(f"  sigma       = {sigma:+.6f}")
    print()


# =========================================================
# Main
# =========================================================

def main() -> None:
    constants = StructuralConstants()
    psi_ew = compute_psi_values(constants)

    # Inputs inherited from the electroweak sector
    alpha_inv_val = alpha_inverse(constants, psi_ew)
    alpha_val = 1.0 / alpha_inv_val
    mp_over_me_val = proton_mass_ratio(constants, psi_ew)

    psi_g = compute_psi_gravity(constants)
    result = compute_gravity(constants, alpha_val, mp_over_me_val)

    print("Structural Gravity Relations: Theory vs Observation")
    print("====================================")
    print(f"R = {format_fraction(constants.R):>5} = {float(constants.R):.12f}")
    print(f"Z = {format_fraction(constants.Z):>5} = {float(constants.Z):.12f}")
    print()

    print("Psi values")
    print("----------")
    print(f"Psi_G = {format_fraction(psi_g.psi_g):>7} = {float(psi_g.psi_g):.2f}")
    print(f"Psi_d = {format_fraction(psi_g.psi_d):>7} = {float(psi_g.psi_d):.2f}")
    print()

    print("Theoretical values")
    print("------------------")
    print(f"alpha       = {alpha_val:.12e}")
    print(f"m_p / m_e   = {mp_over_me_val:.12f}")
    print(f"alpha_Gp    = {result.alpha_gp:.12e}")
    print(f"alpha_Ge    = {result.alpha_ge:.12e}")
    print(f"sqrt(G)     = {result.sqrt_g:.12e}")
    print(f"G           = {result.g_value:.12e}")
    print()

    print("Comparison with observation")
    print("---------------------------")
    print_comparison("alpha_Gp", result.alpha_gp, REF_OBSERVED["alpha_gp"])
    print_comparison("alpha_Ge", result.alpha_ge, REF_OBSERVED["alpha_ge"])
    print_comparison("sqrt(G)", result.sqrt_g, REF_OBSERVED["sqrt_gravitational_constant"])
    print_comparison("G", result.g_value, REF_OBSERVED["gravitational_constant"])


if __name__ == "__main__":
    main()
