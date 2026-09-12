"""
Zero Parameter Structure

Copyright (c) 2026 Yasuo Tanaka
Licensed under the MIT License.

Paper 1 cosmology structural relations.

The v1.0 construction does not assume a single cosmological ratio at the
start.  It generates the finite L1 candidate set

    R(1..4), S(1..4)

and applies the same exact square-root closure to every candidate.
"""

from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
from math import gcd, isqrt
from core.structural_constants import StructuralConstants, q, q_sharp, R, S


# =========================================================
# Structural density realization
# =========================================================

@dataclass(frozen=True)
class DensityResult:
    omega_L: Fraction
    omega_dm: Fraction
    omega_b: Fraction
    omega_m: Fraction


def compute_density_parameters(T: Fraction) -> DensityResult:
    """Return the exact normalized density realization for a positive T.

    The unnormalized hierarchy is

        Omega_L : Omega_b : Omega_m
        = 1 : 1/(3 T^2) : 1/T,

    and every realization satisfies exactly

        Omega_m^2 = 3 Omega_L Omega_b.
    """
    if T <= 0:
        raise ValueError("T must be positive")

    omega_L  = T / (1 + T)
    omega_m  = 1 / (1 + T)
    omega_b  = 1 / (3 * T * (1 + T))
    omega_dm = omega_m - omega_b

    assert omega_m**2 == 3 * omega_L * omega_b

    return DensityResult(
        omega_L=omega_L,
        omega_dm=omega_dm,
        omega_b=omega_b,
        omega_m=omega_m,
    )


# =========================================================
# Exact closure diagnostics
# =========================================================

def _lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)


def primitive_integer_vector(
    values: DensityResult,
) -> tuple[int, int, int, int]:
    ordered = (
        values.omega_L,
        values.omega_dm,
        values.omega_b,
        values.omega_m,
    )

    common_den = 1
    for value in ordered:
        common_den = _lcm(common_den, value.denominator)

    ints = [
        value.numerator * (common_den // value.denominator)
        for value in ordered
    ]
    common_gcd = reduce(gcd, (abs(x) for x in ints))
    return tuple(x // common_gcd for x in ints)


def Zc(values: DensityResult) -> Fraction:
    """Dimensionless square-root closure ratio."""
    return (
        values.omega_dm + values.omega_m
    ) / values.omega_L


def rational_sqrt(value: Fraction) -> Fraction | None:
    """Return the exact nonnegative rational square root, if it exists."""
    if value < 0:
        return None

    sn = isqrt(value.numerator)
    sd = isqrt(value.denominator)

    if (
        sn * sn == value.numerator
        and sd * sd == value.denominator
    ):
        return Fraction(sn, sd)

    return None


@dataclass(frozen=True)
class CandidateResult:
    label: str
    n: int
    T: Fraction
    densities: DensityResult
    primitive: tuple[int, int, int, int]
    zc: Fraction
    sqrt_zc: Fraction | None


def candidate_universes() -> tuple[CandidateResult, ...]:
    """Generate the eight pre-exception L1 candidate realizations."""
    rows = []

    for label, func in (("R", R), ("S", S)):
        for n in range(1, 5):
            T = func(n)
            densities = compute_density_parameters(T)
            zc = Zc(densities)
            rows.append(
                CandidateResult(
                    label=label,
                    n=n,
                    T=T,
                    densities=densities,
                    primitive=primitive_integer_vector(densities),
                    zc=zc,
                    sqrt_zc=rational_sqrt(zc),
                )
            )

    return tuple(rows)


def square_root_survivors() -> tuple[CandidateResult, ...]:
    """Return the exact 8 -> 2 square-root closure survivors."""
    survivors = tuple(
        row
        for row in candidate_universes()
        if row.sqrt_zc is not None
    )

    expected = (
        ("R", 2, Fraction(13, 6),  Fraction(12, 13)),
        ("S", 4, Fraction(31, 24), Fraction(36, 31)),
    )
    actual = tuple(
        (row.label, row.n, row.T, row.sqrt_zc)
        for row in survivors
    )
    assert actual == expected

    return survivors


# =========================================================
# R(q) Lorentz/light-cone factorization
# =========================================================

@dataclass(frozen=True)
class LorentzClosure:
    gamma: Fraction
    beta: Fraction
    gamma_beta: Fraction
    lambda_plus: Fraction
    lambda_minus: Fraction


def r_q_lorentz_closure() -> LorentzClosure:
    T = R(q)
    values = compute_density_parameters(T)
    root = rational_sqrt(Zc(values))

    assert root == Fraction(12, 13)

    beta = rational_sqrt(1 - Zc(values))
    assert beta == Fraction(5, 13)

    gamma = 1 / root
    gamma_beta   = gamma * beta
    lambda_plus  = gamma * (1 + beta)
    lambda_minus = gamma * (1 - beta)

    assert gamma        == Fraction(13, 12)
    assert gamma_beta   == Fraction(5, 12)
    assert lambda_plus  == Fraction(3, 2)
    assert lambda_minus == Fraction(2, 3)
    assert lambda_plus * lambda_minus == 1

    return LorentzClosure(
        gamma=gamma,
        beta=beta,
        gamma_beta=gamma_beta,
        lambda_plus=lambda_plus,
        lambda_minus=lambda_minus,
    )


# Public exact v1.0 survivors.
assert R(q)    == Fraction(13, 6)
assert S(q**2) == Fraction(31, 24)
