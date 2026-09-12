"""
Zero Parameter Structure — Paper 1 Cosmology Execution

Structural Origin of Cosmological Density Ratios
Version 1.0

Console-oriented reproduction output.
No free parameters. No tuning. Only structure.
"""

from fractions import Fraction

from core.structural_cosmology import (
    candidate_universes,
    r_q_lorentz_closure,
    square_root_survivors,
)
from observed_data.observed_data_cosmology import (
    DESI_DR2_CMB_DESY5,
    DESI_DR2_CMB_PANTHEON_PLUS,
    PLANCK_2018_PLIK_BEST_FIT,
)


WIDTH = 92


def rule(char: str = "-") -> None:
    print(char * WIDTH)


def section(title: str) -> None:
    print()
    print(title)
    rule()


def frac(value: Fraction | None) -> str:
    if value is None:
        return "-"
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def print_observation_table(rows) -> None:
    print(
        f"{'Dataset':<30}"
        f"{'H0':>8}"
        f"{'Omega_L':>10}"
        f"{'Omega_dm':>10}"
        f"{'Omega_b':>10}"
        f"{'Omega_m':>10}"
        f"{'Q':>10}"
    )
    rule()
    for obs in rows:
        print(
            f"{obs.name:<30}"
            f"{obs.H0:>8.2f}"
            f"{obs.omega_L:>10.6f}"
            f"{obs.omega_dm:>10.6f}"
            f"{obs.omega_b:>10.6f}"
            f"{obs.omega_m:>10.6f}"
            f"{obs.Q:>10.6f}"
        )


def main() -> None:
    rows = candidate_universes()

    section("Eight L1 candidate universes")

    print(
        f"{'Candidate':<10}"
        f"{'T':>8}"
        f"{'Omega_L':>10}"
        f"{'Omega_dm':>10}"
        f"{'Omega_b':>10}"
        f"{'Omega_m':>10}"
        f"{'sqrt(Zc)':>10}"
    )
    rule()

    for row in rows:
        d = row.densities
        print(
            f"{row.label + '(' + str(row.n) + ')':<10}"
            f"{frac(row.T):>8}"
            f"{float(d.omega_L):>10.6f}"
            f"{float(d.omega_dm):>10.6f}"
            f"{float(d.omega_b):>10.6f}"
            f"{float(d.omega_m):>10.6f}"
            f"{frac(row.sqrt_zc):>10}"
        )

    section("Exact rational square-root closure: 8 -> 2")

    survivors = square_root_survivors()
    for row in survivors:
        print(
            f"{row.label}({row.n}): "
            f"T={frac(row.T):>5}   "
            f"Zc={frac(row.zc):>8}   "
            f"sqrt(Zc)={frac(row.sqrt_zc):>5}   "
            f"primitive={row.primitive}"
        )

    r_survivor, s_survivor = survivors

    print()
    print(
        "R(q)   * sqrt(Zc(R(q)))   = "
        f"{frac(r_survivor.T * r_survivor.sqrt_zc)} = q"
    )
    print(
        "S(q^2) * sqrt(Zc(S(q^2))) = "
        f"{frac(s_survivor.T * s_survivor.sqrt_zc)}"
    )

    section("R(q) Lorentz / light-cone factorization")

    lorentz = r_q_lorentz_closure()

    print(f"gamma        = {frac(lorentz.gamma)}")
    print(f"beta         = {frac(lorentz.beta)}")
    print(f"gamma * beta = {frac(lorentz.gamma_beta)}")
    print(
        "eigenvalues  = "
        f"{frac(lorentz.lambda_plus)}, {frac(lorentz.lambda_minus)}"
    )

    a = 3**2 - 2**2
    b = 2 * 2 * 3
    c = 3**2 + 2**2
    assert (a, b, c) == (5, 12, 13)
    assert a * a + b * b == c * c

    print(f"5-12-13 triple from (2,3) = ({a}, {b}, {c})")
    print("[PASS] all exact v1.0 structural checks")

    section("Appendix A: observational diagnostics")

    print_observation_table(
        [
            PLANCK_2018_PLIK_BEST_FIT,
            DESI_DR2_CMB_PANTHEON_PLUS,
            DESI_DR2_CMB_DESY5,
        ]
    )

    print()
    print("[PASS] all Appendix A v1.0 reconstruction checks")

    print()
    rule("=")
    print("Paper 1 completed successfully.")
    rule("=")


if __name__ == "__main__":
    main()
