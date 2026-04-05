"""
Zero Parameter Structure

Copyright (c) 2026 Yasuo Tanaka
Licensed under the MIT License.

This work is presented as a translation of underlying physical structure.
No free parameters. No tuning. Only structure.
"""

from dataclasses import dataclass
from fractions import Fraction
from math import pi
from typing import Optional

from core.structural_constants import StructuralConstants


# =========================================================
# Psi values
# =========================================================

@dataclass(frozen=True)
class PsiValues:
    psi_e: Fraction
    psi_p: Fraction
    psi_n: Fraction
    psi_mu: Fraction
    psi_tau: Fraction


def compute_psi_values(constants: StructuralConstants) -> PsiValues:
    """
    Construct the structural Psi values for each particle sector.

    Each Psi is written as an exact structural expression in R,
    so that the particle hierarchy is represented by rational structure
    rather than floating-point fitting parameters.

    Interpretation:
    - psi_e   : electron structural mass index
    - psi_mu  : muon structural mass index
    - psi_n   : neutron structural mass index
    - psi_p   : proton structural mass index
    - psi_tau : tau structural mass index

    These quantities are kept as exact Fractions in order to preserve
    the structural form of the theory.
    """
    R = constants.R

    # Electron:
    # deepest nested structure among the charged sectors,
    # representing the most elaborate outer-to-inner linked pathway.
    psi_e   = (8  * (12 * (12 * (4 + 3 * R) + 3) + 7) + 3) / 2

    # Muon:
    # intermediate structural layer, simpler than the electron sector
    # but still carrying a nested binding hierarchy.
    psi_mu  = (8  * (8  *       (4 + 3 * R) + 5) + 2)      / 2

    # Neutron:
    # neutral composite extension of the proton-like sector,
    # with an added structural offset relative to the proton pathway.
    psi_n   = (8 *  (12 *       (4 + 3 * R) + 7) + 0)      / 2

    # Proton:
    # primary hadronic binding structure.
    psi_p   = (12 * (12 *        4 +          7) + 1)

    # Tau:
    # fully extended heavy charged-lepton pathway,
    # structurally close to a complete outer sequence.
    psi_tau = (12 * (12 *        4 +          7) + 7)

    return PsiValues(
        psi_e=Fraction(psi_e),
        psi_p=Fraction(psi_p),
        psi_n=Fraction(psi_n),
        psi_mu=Fraction(psi_mu),
        psi_tau=Fraction(psi_tau),
    )


# =========================================================
# Theory results
# =========================================================

@dataclass(frozen=True)
class TheoryResult:
    alpha_inv: float
    proton_ratio: float
    neutron_ratio: float
    muon_ratio: float
    tau_from_mu_ratio: float
    tau_from_e_ratio: float
    higgs_value: float
    vev_value: float
    neutrino_ratio: float


# =========================================================
# Structural formulas
# =========================================================

def alpha_inverse(constants: StructuralConstants, psi: PsiValues) -> float:
    """
    Compute the structural expression for alpha^{-1}.

    alpha^{-1} = 4*pi*(3R^2)/Z * (1 + 1/psi_e)

    Structural meaning:
    - (3R^2)/Z represents the secondary-binding sector after internal/external conversion.
    - 4*pi represents the external observational projection.
    - (1 + 1/psi_e) is the residual correction carried by the electron structure.

    Thus alpha^{-1} is interpreted as the externally observed form of
    the secondary-binding sector.
    """
    R = float(constants.R)
    Z = float(constants.Z)
    psi_e = float(psi.psi_e)
    return 4.0 * pi * (3.0 * R**2) / Z * (1.0 + 1.0 / psi_e)


def proton_mass_ratio(constants: StructuralConstants, psi: PsiValues) -> float:
    """
    Compute the proton-to-electron mass ratio.

    m_p / m_e = alpha^{-1} * [2*(4R)/Z * (1 - 1/psi_p)]

    Structural meaning:
    - alpha^{-1} supplies the outer observational normalization.
    - 2*(4R)/Z represents the primary-binding sector after conversion.
    - (1 - 1/psi_p) is the proton residual correction.

    The proton mass is therefore interpreted as a primary-binding mass
    observed through the alpha-sector normalization.
    """
    R = float(constants.R)
    Z = float(constants.Z)
    psi_p = float(psi.psi_p)
    alpha_inv = alpha_inverse(constants, psi)
    return alpha_inv * (2.0 * (4.0 * R) / Z * (1.0 - 1.0 / psi_p))


def neutron_mass_ratio(constants: StructuralConstants, psi: PsiValues) -> float:
    """
    Compute the neutron-to-electron mass ratio.

    m_n / m_e = alpha^{-1} * [2*(4R)/Z - 1/psi_n]

    Structural meaning:
    - alpha^{-1} again provides the outer observational normalization.
    - 2*(4R)/Z is the primary-binding base.
    - 1/psi_n is the neutron-specific residual shift.

    The neutron is interpreted as a neutral extension of the proton-side
    primary-binding structure.
    """
    R = float(constants.R)
    Z = float(constants.Z)
    psi_n = float(psi.psi_n)
    alpha_inv = alpha_inverse(constants, psi)
    return alpha_inv * (2.0 * (4.0 * R) / Z - 1.0 / psi_n)


def muon_mass_ratio(constants: StructuralConstants, psi: PsiValues) -> float:
    """
    Compute the muon-to-electron mass ratio.

    m_mu / m_e = (3/2) * 4*pi*(3R^2)/Z * (1 + R/psi_mu)

    Structural meaning:
    - (3/2) gives the leading structural scaling for the muon sector.
    - 4*pi*(3R^2)/Z is the same secondary-binding observational channel
      that appears in alpha^{-1}.
    - (1 + R/psi_mu) is the muon residual correction.

    The muon is interpreted as an intermediate secondary-binding structure.
    """
    R = float(constants.R)
    Z = float(constants.Z)
    psi_mu = float(psi.psi_mu)
    return (3.0 / 2.0) * 4.0 * pi * (3.0 * R**2) / Z * (1.0 + R / psi_mu)


def tau_from_mu_ratio(constants: StructuralConstants, psi: PsiValues) -> float:
    """
    Compute the tau-to-muon mass ratio.

    m_tau / m_mu = (3/2) * [(4R)*Z * (1 + 1/psi_tau)]

    Structural meaning:
    - (3/2) gives the leading structural scaling for the tau sector.
    - (4R) represents the primary-binding pathway.
    - Z here connects the internal pathway to the observed heavy-lepton sector.
    - (1 + 1/psi_tau) is the tau residual correction.

    The tau is interpreted as a fully extended heavy-lepton pathway.
    """
    R = float(constants.R)
    Z = float(constants.Z)
    psi_tau = float(psi.psi_tau)
    return (3.0 / 2.0) * ((4.0 * R) * Z * (1.0 + 1.0 / psi_tau))


def tau_from_e_ratio(constants: StructuralConstants, psi: PsiValues) -> float:
    """
    Compute the tau-to-electron mass ratio.

    This is obtained as:
        m_tau / m_e = (m_tau / m_mu) * (m_mu / m_e)

    Structural meaning:
    The tau/electron hierarchy is factorized into:
    - the muon/electron secondary-binding hierarchy
    - the tau/muon heavy-path extension
    """
    return tau_from_mu_ratio(constants, psi) * muon_mass_ratio(constants, psi)


def higgs_value(constants: StructuralConstants, psi: PsiValues) -> float:
    """
    Higgs = 13/alpha^2 + 8*(8*(4+3R) + R)

    Structural meaning:
    This term gives the mass scale associated with primary binding.

    Since alpha_inv = 1/alpha,
    1/alpha^2 = alpha_inv^2.
    """
    R = float(constants.R)
    alpha_inv = alpha_inverse(constants, psi)
    return 13.0 * alpha_inv**2 + 8.0 * (8.0 * (4.0 + 3.0 * R) + R)


def vev_value(constants: StructuralConstants, psi: PsiValues) -> float:
    """
    VEV = 26/alpha^2 - 3*12*12*((4+3R) + 2R)

    Structural meaning:
    This term gives the mass scale associated with secondary binding.

    Since alpha_inv = 1/alpha,
    1/alpha^2 = alpha_inv^2.
    """
    R = float(constants.R)
    alpha_inv = alpha_inverse(constants, psi)
    return 26.0 * alpha_inv**2 - 3.0 * 12.0 * 12.0 * ((4.0 + 3.0 * R) + 2.0 * R)


def neutrino_mass_ratio(constants: StructuralConstants, psi: PsiValues) -> float:
    """
    m_nu / m_e = (((8*alpha^2) * (12*alpha^2)) / 4) * Z

    Structural meaning:
    This term represents the decoupling of primary and secondary bindings.
    In this picture, the neutrino sector is interpreted not as a direct bound mass,
    but as a residual scale associated with the release of both first-order and
    second-order binding structures.

    Since the code uses alpha_inv = 1/alpha,
    alpha = 1 / alpha_inv.
    """
    Z = float(constants.Z)
    alpha_inv = alpha_inverse(constants, psi)
    alpha = 1.0 / alpha_inv
    return (((8.0 * alpha**2) * (12.0 * alpha**2)) / 4.0) * Z


def compute_theory(constants: StructuralConstants, psi: PsiValues) -> TheoryResult:
    mu_ratio = muon_mass_ratio(constants, psi)
    tau_mu_ratio = tau_from_mu_ratio(constants, psi)
    return TheoryResult(
        alpha_inv=alpha_inverse(constants, psi),
        proton_ratio=proton_mass_ratio(constants, psi),
        neutron_ratio=neutron_mass_ratio(constants, psi),
        muon_ratio=mu_ratio,
        tau_from_mu_ratio=tau_mu_ratio,
        tau_from_e_ratio=tau_mu_ratio * mu_ratio,
        higgs_value=higgs_value(constants, psi),
        vev_value=vev_value(constants, psi),
        neutrino_ratio=neutrino_mass_ratio(constants, psi),
    )

