"""
Zero Parameter Structure — Paper 1 Cosmology Execution

No free parameters. No tuning. Only structure.
"""

from fractions import Fraction

from core.structural_constants import StructuralConstants
from core.structural_cosmology import compute_density_parameters
from observed_data.observed_data_cosmology import PLANCK_2018


# =========================================================
# Helpers
# =========================================================

def as_percent(x: Fraction) -> str:
    return f"{float(x) * 100:.3f}%"


def to_fraction_str(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def diff_percent_points(theory: Fraction, obs: float) -> str:
    return f"{100 * (float(theory) - obs):+.3f} %-pt"


# =========================================================
# Main
# =========================================================

def main() -> None:
    constants = StructuralConstants()
    result = compute_density_parameters(constants.R)

    print("Structural Cosmology: Theory vs Observation")
    print("===========================================")
    print(f"R = {to_fraction_str(constants.R):>5} = {float(constants.R):.12f}")
    print()

    print("Theoretical density parameters")
    print("------------------------------")
    print(f"ΩΛ = {to_fraction_str(result.omega_lambda):>7} = {float(result.omega_lambda):.8f} = {as_percent(result.omega_lambda)}")
    print(f"Ωm  = {to_fraction_str(result.omega_m):>7} = {float(result.omega_m):.8f} = {as_percent(result.omega_m)}")
    print(f"Ωdm = {to_fraction_str(result.omega_dm):>7} = {float(result.omega_dm):.8f} = {as_percent(result.omega_dm)}")
    print(f"Ωb  = {to_fraction_str(result.omega_b):>7} = {float(result.omega_b):.8f} = {as_percent(result.omega_b)}")
    print()

    print("Structural ratios")
    print("-----------------")
    print("ΩΛ : Ωm : Ωb = 3R^2 : 3R : 1")
    print(f"Exact ratio = {to_fraction_str(3 * constants.R**2)} : {to_fraction_str(3 * constants.R)} : 1")
    print(f"Numeric     = {float(3 * constants.R**2):.3f} : {float(3 * constants.R):.3f} : 1.000")
    print()

    print("Comparison with Planck 2018")
    print("---------------------------")

    obs = PLANCK_2018

    print(f"Observed ΩΛ = {obs.omega_lambda:.8f}")
    print(f"Theory ΩΛ   = {float(result.omega_lambda):.8f}")
    print(f"Difference    = {diff_percent_points(result.omega_lambda, obs.omega_lambda)}")
    print()

    print(f"Observed Ωm  = {obs.omega_m:.8f}")
    print(f"Theory Ωm    = {float(result.omega_m):.8f}")
    print(f"Difference    = {diff_percent_points(result.omega_m, obs.omega_m)}")
    print()

    print(f"Observed Ωb  = {obs.omega_b:.8f}")
    print(f"Theory Ωb    = {float(result.omega_b):.8f}")
    print(f"Difference    = {diff_percent_points(result.omega_b, obs.omega_b)}")


if __name__ == "__main__":
    main()
