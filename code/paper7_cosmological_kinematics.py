"""
Zero Parameter Structure - Paper 7 Execution

Structural Origin of Cosmological and Local Kinematic Scales

No free parameters. No tuning. Only structure.
"""

from decimal import Decimal, getcontext
from fractions import Fraction

from core.structural_constants import StructuralConstants
from core.structural_cosmological_kinematic import compute_cosmological_kinematic_values
from observed_data.observed_data_reference import ObservedValue, REF_OBSERVED

getcontext().prec = 56


# =========================================================
# Reporting helpers
# =========================================================

def fraction_to_decimal(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def format_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def decimal_from_number(value: float | int | Decimal) -> Decimal:
    """Convert through str to avoid importing binary-float artifacts."""
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def absolute_diff(theory: Decimal, observed: float | Decimal) -> Decimal:
    return theory - decimal_from_number(observed)


def relative_diff_percent(
    theory: Decimal,
    observed: float | Decimal,
) -> Decimal:
    obs = decimal_from_number(observed)
    return Decimal(100) * (theory - obs) / obs


def sigma_diff(theory: Decimal, observed: ObservedValue) -> Decimal | None:
    if observed.uncertainty is None or observed.uncertainty == 0.0:
        return None

    return (
        theory - decimal_from_number(observed.value)
    ) / decimal_from_number(observed.uncertainty)


def print_comparison(
    label: str,
    theory: Decimal,
    observed: ObservedValue,
    digits: int = 12,
) -> None:
    unit = f" {observed.unit}" if observed.unit else ""
    sigma = sigma_diff(theory, observed)

    print(label)
    print(f"  structural  = {theory:.{digits}g}{unit}")
    print(f"  reference   = {observed.value:.{digits}g}{unit}")
    print(f"  dataset     = {observed.name}")
    if observed.uncertainty is not None:
        print(f"  uncertainty = {observed.uncertainty:.{digits}g}{unit}")
    print(f"  abs diff    = {absolute_diff(theory, observed.value):+.9e}{unit}")
    print(
        "  rel diff    = "
        f"{relative_diff_percent(theory, observed.value):+.9f} %"
    )
    if sigma is not None:
        print(f"  sigma       = {sigma:+.6f}")
    print()


# =========================================================
# Main
# =========================================================

def main() -> None:
    constants = StructuralConstants()
    values = compute_cosmological_kinematic_values(constants)

    print("Cosmological and Local Kinematic Scales")
    print("=" * 58)
    print(
        f"R = {format_fraction(constants.R):>5}"
        f" = {fraction_to_decimal(constants.R):.12f}"
    )
    print(
        f"S = {format_fraction(constants.S):>5}"
        f" = {fraction_to_decimal(constants.S):.12f}"
    )
    print(f"Psi_e,eff = {values.psi_e_eff:.12f}")
    print()

    main_rows = (
        ("B_alpha", values.B_alpha, "", ".12f"),
        ("Omega_b,st", values.omega_b_st, "", ".12f"),
        ("omega_st", values.omega_st, "", ".12f"),
        ("H_st", values.H_st, "km s^-1 Mpc^-1", ".12f"),
        (
            "H_ladder,st",
            values.H_ladder_st,
            "km s^-1 Mpc^-1",
            ".12f",
        ),
        ("T_alpha,st", values.T_alpha_st, "s", ".12e"),
        ("a_st", values.a_st, "m s^-2", ".12e"),
        (
            "c_closure",
            values.c_closure_m_per_s / Decimal(1000),
            "km s^-1",
            ".12f",
        ),
        ("v_LS,st", values.v_LS_st_km_per_s, "km s^-1", ".12f"),
    )

    print("Main structural values")
    print("-" * 58)
    for name, value, unit, fmt in main_rows:
        value_str = format(value, fmt)
        print(f"{name:<14} = {value_str} {unit}")
    print()

    print("Comparison with reference values")
    print("-" * 58)
    comparisons = (
        ("H_st", values.H_st, "planck_2018_h0_best_fit"),
        (
            "H_ladder,st",
            values.H_ladder_st,
            "riess_2022_shoes_h0",
        ),
        ("a_st", values.a_st, "mcgaugh_2016_g_dagger"),
        (
            "v_LS,st",
            values.v_LS_st_km_per_s,
            "tully_2008_local_sheet_cmb_velocity",
        ),
    )
    for label, theory, key in comparisons:
        print_comparison(label, theory, REF_OBSERVED[key])

    c_exact_km_per_s = Decimal("299792.458")
    closure_diff = values.c_closure_m_per_s / Decimal(1000) - c_exact_km_per_s

    print("Internal closure check")
    print("-" * 58)
    print(f"c_closure = {values.c_closure_m_per_s / Decimal(1000):.12f} km s^-1")
    print(f"c_exact   = {c_exact_km_per_s:.12f} km s^-1")
    print(f"difference = {closure_diff:+.9e} km s^-1")


if __name__ == "__main__":
    main()
