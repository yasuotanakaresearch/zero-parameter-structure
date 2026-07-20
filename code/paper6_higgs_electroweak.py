"""
Zero Parameter Structure - Paper 6 Execution

Structural Origin of Higgs, Electroweak, and Strong-Coupling
Scale Relations

No free parameters. No tuning. Only structure.
"""

from decimal import Decimal, getcontext
from fractions import Fraction

from core.structural_constants import StructuralConstants
from core.structural_higgs_electroweak import (
    alpha_s_scale_table,
    compute_higgs_electroweak_values,
    compute_qcd_continuation,
)
from observed_data.observed_data_pdg import (
    ObservedValue,
    PAPER6_ALPHA_S_REFERENCE,
    PDG_OBSERVED,
)

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
    values = compute_higgs_electroweak_values(constants)
    continuation = compute_qcd_continuation(constants, values)

    print("Structural Origin of Higgs, Electroweak,")
    print("and Strong-Coupling Scale Relations")
    print("=" * 58)
    print(
        f"R = {format_fraction(constants.R):>5}"
        f" = {fraction_to_decimal(constants.R):.12f}"
    )
    print(
        f"S = {format_fraction(constants.S):>5}"
        f" = {fraction_to_decimal(constants.S):.12f}"
    )
    print(f"alpha^-1  = {values.alpha_inverse:.12f}")
    print()

    main_rows = (
        ("B_H", values.B_H, "", ".12f"),
        ("Psi_H", values.psi_H, "", ".0f"),
        ("Psi_v", values.psi_v, "", ".0f"),
        ("m_H / m_e", values.mH_over_me, "", ".12f"),
        ("v / m_e", values.v_over_me, "", ".12f"),
        ("m_H", values.mH_gev, "GeV", ".12f"),
        ("v", values.v_gev, "GeV", ".12f"),
        ("y_e", values.electron_yukawa, "", ".12e"),
        ("sin^2(theta_W)", values.sin2_theta_w, "", ".12f"),
        ("m_W", values.mW_gev, "GeV", ".12f"),
        ("m_Z", values.mZ_gev, "GeV", ".12f"),
        ("alpha_s(m_Z)", values.alpha_s_mZ, "", ".12f"),
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
        ("m_H", values.mH_gev, "higgs_mass_gev_pdg"),
        ("v", values.v_gev, "electroweak_vev_gev"),
        ("y_e", values.electron_yukawa, "electron_yukawa"),
        (
            "sin^2(theta_W)",
            values.sin2_theta_w,
            "weak_mixing_on_shell",
        ),
        ("m_W", values.mW_gev, "w_mass_gev"),
        ("m_Z", values.mZ_gev, "z_mass_gev"),
        ("alpha_s(m_Z)", values.alpha_s_mZ, "alpha_s_mz"),
    )
    for label, theory, key in comparisons:
        print_comparison(label, theory, PDG_OBSERVED[key])

    print("Continuation parameters")
    print("-" * 58)
    print(f"{'m_d / m_e':<13} = {continuation.md_over_me:.12g}")
    print(f"{'A_s':<13} = {continuation.A_s:.12g}")
    print(f"{'Lambda_*':<13} = {continuation.lambda_star_gev:.12g} GeV")
    print()

    scales = (
        ("m_tau", Decimal("1.77686")),
        ("m_b", Decimal("4.18484")),
        ("5", Decimal("5")),
        ("10", Decimal("10")),
        ("20", Decimal("20")),
        ("35", Decimal("35")),
        ("m_W", values.mW_gev),
        ("m_Z", values.mZ_gev),
        ("m_t", Decimal("173.013")),
        ("200", Decimal("200")),
        ("500", Decimal("500")),
        ("1000", Decimal("1000")),
    )
    rows = alpha_s_scale_table(scales, continuation)

    print("Illustrative alpha_s(Q) continuation")
    print("-" * 76)
    print(
        f"{'Scale':<10}"
        f" {'Q [GeV]':>14}"
        f" {'alpha_s(Q)':>16}"
        f" {'Reference':>14}"
        f" {'Rel. diff':>14}"
    )
    print("-" * 76)
    for label, Q_gev, theory in rows:
        reference = decimal_from_number(PAPER6_ALPHA_S_REFERENCE[label])
        rel_diff = relative_diff_percent(theory, reference)
        print(
            f"{label:<10}"
            f" {Q_gev:>14.6f}"
            f" {theory:>16.6f}"
            f" {reference:>14.5f}"
            f" {rel_diff:>+13.2f}%"
        )

    print()
    print("Note")
    print("----")
    print(
        "The alpha_s(Q) table is an illustrative scale-trend continuation "
        "from the structural boundary value at m_Z."
    )
    print(
        "It is not presented as a uniform high-order RGE determination "
        "with one threshold and scheme convention."
    )


if __name__ == "__main__":
    main()
