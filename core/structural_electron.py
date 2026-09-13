"""
Zero Parameter Structure

Copyright (c) 2026 Yasuo Tanaka
Licensed under the MIT License.

Paper 2 — Version 1.1 structural implementation.

This module follows the Version 1.1 construction based on the generated
q/X/Y/P hierarchy. No continuously fitted observable-specific parameter
is introduced.
"""

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction

from core.structural_constants import (
    P,
    P1,
    P2,
    P3,
    StructuralConstants,
    X,
    Y,
    q,
    q_sharp,
)

getcontext().prec = 56

PI = Decimal("3.14159265358979323846264338327950288419716939937510")
c = 299_792_458  # exact speed of light in m/s


# =========================================================
# Helpers
# =========================================================

def fraction_to_decimal(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def K(n: int, d: int | None = None, s: int = 1) -> Fraction:
    """
    Structural affine factor

        K(n; d, s) = n + s/d,

    with d=q when omitted.
    """
    if d is None:
        d = q
    return Fraction(n, 1) + Fraction(s, d)


def dot_product(weights, values):
    """Exact sparse contraction used by the Version 1.1 sector formulas."""
    return sum(w * x for w, x in zip(weights, values))


def correction_term(sign: int, psi_value: Fraction) -> Fraction:
    """Return 1 + sign/Psi."""
    return 1 + Fraction(sign, 1) / psi_value


# =========================================================
# Psi values
# =========================================================

@dataclass(frozen=True)
class PsiValues:
    Ce: Fraction
    CG: Fraction

    psi_Gp: Fraction
    psi_Gp_hat: Fraction

    psi_e0: Fraction
    psi_e_star: Fraction
    psi_e: Fraction

    psi_p0: Fraction
    psi_p_star: Fraction
    psi_p: Fraction

    psi_n0: Fraction
    psi_n_star: Fraction
    psi_n: Fraction

    psi_mu0: Fraction
    psi_mu_star: Fraction
    psi_mu: Fraction

    psi_tau: Fraction


def compute_psi_values(constants: StructuralConstants) -> PsiValues:
    """
    Construct the Version 1.1 structural indices.

    The common structural ratios are inherited from StructuralConstants,
    while the charged-sector backbones and corrections are evaluated from
    the q/X/Y/P hierarchy.

    Main precursor:
        Psi_Gp = (C_e - Y(0)) / X(q) = 67/2

    Electron:
        Psi_e* = X(q) / [Psi_Gp - 1/P(1)]

    Proton:
        widehat(Psi_Gp) = C_G + q - 1/Psi_Gp
        Psi_p* = q^3 / widehat(Psi_Gp)

    Neutron and muon corrections follow the Version 1.1 sparse
    contraction formulas.
    """
    # Exact consistency with the common branch definitions.
    assert constants.R == q * Fraction(X(q, +1), X(q))
    assert constants.S == q * Fraction(Y(q**2),  X(q**2))

    Ce = X(q,       +1) * Y(q**2)     # 13 * 31 = 403
    CG = X(q_sharp, -1) * Y(q_sharp)  # 23 * 15 = 345

    psi_Gp = Fraction(Ce - Y(0), X(q))

    kappa_e  = K(0)
    kappa_p  = K(1) / X(q)
    kappa_n  = K(1) * X(q)
    kappa_mu = K(1) / X(q**2)

    # Electron
    psi_e_star = Fraction(X(q), (psi_Gp - Fraction(1, P(1))))
    w_e0       = [Ce * Y(q**2), Y(q)**2]
    w_e        = [Ce * Y(q**2), Y(q)**2, psi_e_star]
    M_e0       = [1, -1]
    M_e        = [1, -1, -q_sharp]
    psi_e0     = kappa_e * dot_product(M_e0, w_e0)
    psi_e      = kappa_e * dot_product(M_e , w_e)

    # Proton
    psi_Gp_hat = CG + q - Fraction(1, psi_Gp)
    psi_p_star = Fraction(q**3, psi_Gp_hat)
    w_p0       = [Ce * X(q,1), Y(q)**2]
    w_p        = [Ce * X(q,1), Y(q)**2, psi_p_star]
    M_p0       = [1, 1]
    M_p        = [1, 1, q]
    psi_p0     = kappa_p * dot_product(M_p0, w_p0)
    psi_p      = kappa_p * dot_product(M_p , w_p)

    # Neutron
    det_ratio_n = Fraction(P(q) - Fraction(1, q_sharp), P(q) + 1)
    psi_n_star  = Fraction(det_ratio_n, q_sharp**4)
    w_n0        = [Ce, q**2]
    w_n         = [Ce, q**2, psi_n_star]
    M_n0        = [1, 1]
    M_n         = [1, 1, -q_sharp]
    psi_n0      = kappa_n * dot_product(M_n0, w_n0)
    psi_n       = kappa_n * dot_product(M_n , w_n)

    # Muon
    w_mu0       = [Ce * X(q,1), Y(q)**2]
    M_mu0       = [1, 1]
    psi_mu0     = kappa_mu * dot_product(M_mu0, w_mu0)
    psi_mu_star = q**4 * K(q) / Y(q)**2 * (psi_e0 - Y(q)) / psi_p0
    w_mu        = [Ce * X(q,1), Y(q)**2, psi_mu_star]
    M_mu        = [1, 1, -q]
    psi_mu      = kappa_mu * dot_product(M_mu, w_mu)

    # Tau
    psi_tau = Fraction(662, 1)

    # Version 1.1 exact regression identities.
    assert psi_Gp     == Fraction(67, 2)
    assert psi_e_star == Fraction(9, 25)
    assert psi_p_star == Fraction(536, 23247)

    assert psi_e  == Fraction(6222, 1) - Fraction(27, 50)        # 6221.46
    assert psi_p  == Fraction(661,  1) + Fraction(2 * 67, 23247) # 661.005764184626
    assert psi_n  == Fraction(7326, 1) - Fraction(166, 261)      # 7325.36398467433
    assert psi_mu == Fraction(661,  4) - Fraction(31075, 64778)  # 164.7702846645466

    return PsiValues(
        Ce=Ce,
        CG=CG,
        psi_Gp=psi_Gp,
        psi_Gp_hat=psi_Gp_hat,
        psi_e0=psi_e0,
        psi_e_star=psi_e_star,
        psi_e=psi_e,
        psi_p0=psi_p0,
        psi_p_star=psi_p_star,
        psi_p=psi_p,
        psi_n0=psi_n0,
        psi_n_star=psi_n_star,
        psi_n=psi_n,
        psi_mu0=psi_mu0,
        psi_mu_star=psi_mu_star,
        psi_mu=psi_mu,
        psi_tau=psi_tau,
    )


# =========================================================
# Observable formulas
# =========================================================

def alpha_inverse(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """alpha^{-1}(0) = 4 pi B_alpha (1 + 1/Psi_e)."""
    return (
        Decimal(4)
        * PI
        * fraction_to_decimal(constants.B_alpha)
        * fraction_to_decimal(correction_term(+1, psi.psi_e))
    )


def proton_mass_ratio(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """m_p/m_e = alpha^{-1}(0) A_d (1 - 1/Psi_p)."""
    return alpha_inverse(constants, psi) * fraction_to_decimal(
        constants.A_d * correction_term(-1, psi.psi_p)
    )


def neutron_mass_ratio(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """m_n/m_e = alpha^{-1}(0) A_d (1 - 1/Psi_n)."""
    return alpha_inverse(constants, psi) * fraction_to_decimal(
        constants.A_d * correction_term(-1, psi.psi_n)
    )


def muon_mass_ratio(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """m_mu/m_e = K(1) 4 pi B_alpha (1 + 1/Psi_mu)."""
    return (
        fraction_to_decimal(K(1))
        * Decimal(4)
        * PI
        * fraction_to_decimal(constants.B_alpha)
        * fraction_to_decimal(correction_term(+1, psi.psi_mu))
    )


def tau_from_mu_ratio(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """m_tau/m_mu = K(1;4,-1) A_tau (1 + 1/Psi_tau)."""
    return fraction_to_decimal(
        K(1, 4, -1)
        * constants.A_tau
        * correction_term(+1, psi.psi_tau)
    )


def tau_from_e_ratio(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """m_tau/m_e = (m_tau/m_mu)(m_mu/m_e)."""
    return tau_from_mu_ratio(constants, psi) * muon_mass_ratio(constants, psi)


# =========================================================
# Electron mass-energy normalization
# =========================================================

@dataclass(frozen=True)
class ElectronMassPath:
    psi_me: Fraction
    psi_me_star: Fraction

    psi_me_from_n: Fraction
    psi_me_star_from_e: Fraction
    psi_me_star_from_pn: Fraction
    psi_me_star_from_n: Fraction

    psi_Gp_from_en: Fraction
    mass_scale: Fraction


def psi_me_value(psi: PsiValues) -> Fraction:
    """
    Version 1.0 product-map representation retained in Version 1.1:

        Psi_me
          = q P(1)P(q)P(q^2)
          + q^{-1}P(q)Psi_p0
          - P(q).
    """
    x_me = [
        Fraction(P1 * P2 * P3, 1),
        Fraction(P2, 1) * psi.psi_p0,
        Fraction(P2, 1),
    ]
    w_me = [Fraction(q, 1), Fraction(1, q), Fraction(-1, 1)]
    return dot_product(w_me, x_me)


def psi_me_star_value(psi: PsiValues, psi_me: Fraction) -> Fraction:
    """
    Version 1.1 primary representation:

        Psi_me* = [Psi_me - Psi_e0/q_sharp] / X(q).
    """
    return (psi_me - psi.psi_e0 / q_sharp) / X(q)


def compute_electron_mass_path(
    constants: StructuralConstants,
    psi: PsiValues,
) -> ElectronMassPath:
    """
    Evaluate Psi_me, Psi_me*, their exact alternate representations,
    the e-n reconstruction of Psi_Gp, and the electron mass-energy scale.
    """
    del constants  # kept in the public signature for sector API consistency

    psi_me      = psi_me_value(psi)
    psi_me_star = psi_me_star_value(psi, psi_me)

    # Version 1.1 exact alternate representations.
    psi_me_from_n       = q * X(q) * psi.psi_n0 + q * P(q) + q
    psi_me_star_from_e  = Y(q) * psi.psi_e0 / q_sharp - P(q) - P(1)
    psi_me_star_from_pn = Y(q) * (q_sharp * psi.psi_p0 + P(q)) + psi.psi_n0 / (K(1) * X(q))
    psi_me_star_from_n  = q * psi.psi_n0 - P(q) * P(1) 
    psi_Gp_from_en      = (psi.psi_n0 -  psi.psi_e0 * Y(q) / P(1)) / q

    # Exact closure checks.
    assert psi_me         == 175882
    assert psi_me_star    == 14484
    assert psi_me         == psi_me_from_n
    assert psi_me_star    == psi_me_star_from_e == psi_me_star_from_pn == psi_me_star_from_n
    assert psi_Gp_from_en == psi.psi_Gp == Fraction(67, 2)

    # c_km^2 / [Psi_me (1 + Psi_me*^-2)] gives eV.
    c_km = Fraction(c, 10**3)
    mass_scale = c_km**2 / (psi_me * (1 + psi_me_star**-2))

    return ElectronMassPath(
        psi_me=psi_me,
        psi_me_star=psi_me_star,
        psi_me_from_n=psi_me_from_n,
        psi_me_star_from_e=psi_me_star_from_e,
        psi_me_star_from_pn=psi_me_star_from_pn,
        psi_me_star_from_n=psi_me_star_from_n,
        psi_Gp_from_en=psi_Gp_from_en,
        mass_scale=mass_scale,
    )


# =========================================================
# Theory result
# =========================================================

@dataclass(frozen=True)
class TheoryResult:
    alpha_inv: Decimal
    proton_ratio: Decimal
    neutron_ratio: Decimal
    muon_ratio: Decimal
    tau_from_mu_ratio: Decimal
    tau_from_e_ratio: Decimal

    psi_me: Fraction
    psi_me_star: Fraction
    psi_Gp_from_en: Fraction
    electron_mass_scale: Fraction


def compute_theory(constants: StructuralConstants, psi: PsiValues) -> TheoryResult:
    mu_ratio = muon_mass_ratio(constants, psi)
    tau_mu_ratio = tau_from_mu_ratio(constants, psi)
    electron_path = compute_electron_mass_path(constants, psi)

    return TheoryResult(
        alpha_inv=alpha_inverse(constants, psi),
        proton_ratio=proton_mass_ratio(constants, psi),
        neutron_ratio=neutron_mass_ratio(constants, psi),
        muon_ratio=mu_ratio,
        tau_from_mu_ratio=tau_mu_ratio,
        tau_from_e_ratio=tau_mu_ratio * mu_ratio,
        psi_me=electron_path.psi_me,
        psi_me_star=electron_path.psi_me_star,
        psi_Gp_from_en=electron_path.psi_Gp_from_en,
        electron_mass_scale=electron_path.mass_scale,
    )
