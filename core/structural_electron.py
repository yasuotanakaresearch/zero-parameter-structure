"""
Zero Parameter Structure

Copyright (c) 2026 Yasuo Tanaka
Licensed under the MIT License.

This work is presented as a translation of underlying physical structure.
No free parameters. No tuning. Only structure.
"""

from dataclasses import dataclass
from fractions import Fraction
from decimal import Decimal, getcontext
from core.structural_constants import StructuralConstants, P_MIN, P_MAX, P_MID

getcontext().prec = 56

PI = Decimal("3.14159265358979323846264338327950288419716939937510")
c = 299_792_458  # exact speed of light in m/s


# =========================================================
# helpers
# =========================================================
def fraction_to_decimal(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


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
    delta_e: Fraction
    delta_p: Fraction
    delta_n: Fraction
    delta_mu: Fraction
    delta_tau: Fraction


def compute_psi_values(constants: StructuralConstants) -> PsiValues:
    """
    Construct the fixed structural Psi values for each particle sector.

    The backbone values follow the common integer-core representation
    used in the paper.  With

        6R = 13,  24S = 31,
        P_min = 2,  P_mid = 5,  P_max = 7,
        Psi_s = 72,

    the backbones are

        Psi_e0   = (3/2) * (13*31^2 - P_max^2) / 3
        Psi_p0   = (3/2) * (13^2*31 + P_max^2) / 12
        Psi_n0   = (3/2) * (13*31 + P_min^2) * 12
        Psi_mu0  = Psi_p0 / 4
        Psi_tau0 = Psi_p0

    The residual terms are stored separately.  Their signs are applied
    only when the observable formulas construct the effective indices:

        Psi_e_eff   = Psi_e0   - delta_e
        Psi_p_eff   = Psi_p0   + delta_p
        Psi_n_eff   = Psi_n0   - delta_n
        Psi_mu_eff  = Psi_mu0  - delta_mu
        Psi_tau_eff = Psi_tau0 + delta_tau
    """
    R = constants.R
    S = constants.S

    # Integer cores inherited from the fixed ratios.
    core_13 = R * 6
    core_31 = S * 24

    # Structural backbone values Psi_0.
    psi_e0   = Fraction(3, 2) * (core_13    * core_31**2 - P_MAX**2) / 3
    psi_p0   = Fraction(3, 2) * (core_13**2 * core_31    + P_MAX**2) / 12
    psi_n0   = Fraction(3, 2) * (core_13    * core_31    + P_MIN**2) * 12
    psi_mu0  = Fraction(psi_p0, P_MIN**2)
    psi_tau0 = psi_p0

    # Residual structural fluctuations delta_psi.
    # delta_e   = 1/2 + 1/P_mid^2
    # delta_p   = 6^2 * (Psi_p0 + 24 - 1/2)^(-1)
    # delta_n   = (3/2) * (12 * P_max - 1) * (12 * P_max + 3)^(-1)
    # delta_mu  = 1/2 - 1/P_max^2 + 1/(Psi_mu0*P_max^2)
    # delta_tau = 1
    delta_e   = Fraction(1, 2) + Fraction(1, P_MID**2)
    delta_p   = Fraction(6**2) * Fraction(1, psi_e0 + 24 - Fraction(1, 2))
    delta_n   = Fraction(2, 3) * Fraction(12*P_MAX - 1, 12*P_MAX + 3)
    delta_mu  = Fraction(1, 2) - Fraction(1, P_MAX**2) + Fraction(1, (psi_mu0 * P_MAX**2))
    delta_tau = Fraction(1, 1)

    return PsiValues(
        psi_e=psi_e0,
        psi_p=psi_p0,
        psi_n=psi_n0,
        psi_mu=psi_mu0,
        psi_tau=psi_tau0,
        delta_e=delta_e,
        delta_p=delta_p,
        delta_n=delta_n,
        delta_mu=delta_mu,
        delta_tau=delta_tau,
    )


# =========================================================
# Theory results
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
    electron_mass_scale: Fraction


# =========================================================
# Structural formulas
# =========================================================

def structural_term(
    constants: StructuralConstants,
    coefficient: Fraction,
    r_power: int,
    s_power: int,
) -> Fraction:
    """
    Common structural term:

        coefficient * R^r_power * S^s_power

    This is the exact rational structural part, before any π-dependent
    observational projection is applied.
    """
    return coefficient * (constants.R ** r_power) * (constants.S ** s_power)


def correction_term(
    sign: int,
    psi_value: Fraction,
    scale: Fraction = Fraction(1, 1),
) -> Fraction:
    """
    Residual correction term:

        1 + sign * scale / psi_value

    Examples
    --------
    correction_term(+1, psi) = 1 + 1/psi
    correction_term(-1, psi) = 1 - 1/psi
    """
    return 1 + sign * scale / psi_value


def projection_term(
    coefficient: Fraction,
    power: int = 1
) -> Decimal:
    """
    Observational projection term:

        (coefficient * π)^power

    This is the Decimal-valued projection layer, separated from the
    exact rational structural terms.
    """
    return (fraction_to_decimal(coefficient) * PI) ** power


def alpha_inverse(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """
    Compute the structural expression for alpha^{-1}.

    alpha^{-1} = 4π*(3R^2)/S * (1 + 1/psi_e)

    Structural meaning:
    - (3R^2)/S represents the secondary-binding sector after internal/external conversion.
    - 4*pi represents the external observational projection.
    - (1 + 1/psi_e) is the residual correction carried by the electron structure.

    Thus alpha^{-1} is interpreted as the externally observed form of
    the secondary-binding sector.
    """
    return projection_term(4) * fraction_to_decimal(
        structural_term(constants, Fraction(3, 1), 2, -1) * 
        correction_term(+1, psi.psi_e - psi.delta_e)
    )


def proton_mass_ratio(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """
    Compute the proton-to-electron mass ratio.

    m_p / m_e = alpha^{-1} * [(8R)/S * (1 - 1/psi_p)]

    Structural meaning:
    - alpha^{-1} supplies the outer observational normalization.
    - 2*(4R)/S represents the primary-binding sector after conversion.
    - (1 - 1/psi_p) is the proton residual correction.

    The proton mass is therefore interpreted as a primary-binding mass
    observed through the alpha-sector normalization.
    """
    return alpha_inverse(constants, psi) * fraction_to_decimal(
        structural_term(constants, Fraction(8, 1), 1, -1) *
        correction_term(-1, psi.psi_p + psi.delta_p)
    )


def neutron_mass_ratio(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """
    Compute the neutron-to-electron mass ratio.

    m_n / m_e = alpha^{-1} * [(8R)/S * (1 - 1/psi_n)]

    Structural meaning:
    - alpha^{-1} again provides the outer observational normalization.
    - 2*(4R)/S is the primary-binding base.
    - 1/psi_n is the neutron-specific residual shift.

    The neutron is interpreted as a neutral extension of the proton-side
    primary-binding structure.
    """
    return alpha_inverse(constants, psi) * fraction_to_decimal(
        structural_term(constants, Fraction(8, 1), 1, -1) *
        correction_term(-1, psi.psi_n - psi.delta_n)
    )


def muon_mass_ratio(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """
    Compute the muon-to-electron mass ratio.

    m_mu / m_e = (3/2) * 4π*(3R^2)/S * (1 + 1/psi_mu)

    Structural meaning:
    - (3/2) gives the leading structural scaling for the muon sector.
    - 4*pi*(3R^2)/S is the same secondary-binding observational channel
      that appears in alpha^{-1}.
    - (1 + R/psi_mu) is the muon residual correction.

    The muon is interpreted as an intermediate secondary-binding structure.
    """
    return projection_term(4) * fraction_to_decimal(
        structural_term(constants, Fraction(9, 2), 2, -1) *
        correction_term(+1, psi.psi_mu - psi.delta_mu)
    )

def tau_from_mu_ratio(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """
    Compute the tau-to-muon mass ratio.

    m_tau / m_mu = (3/4) * [(8R)*S * (1 + 1/psi_tau)]

    Structural meaning:
    - (3/4) gives the leading structural scaling for the tau sector.
    - (8R) represents the primary-binding pathway.
    - S here connects the internal pathway to the observed heavy-lepton sector.
    - (1 + 1/psi_tau) is the tau residual correction.

    The tau is interpreted as a fully extended heavy-lepton pathway.
    """
    return fraction_to_decimal(
        structural_term(constants, Fraction(8*3, 4), 1, 1) *
        correction_term(+1, psi.psi_tau + psi.delta_tau)
    )


def tau_from_e_ratio(constants: StructuralConstants, psi: PsiValues) -> Decimal:
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


# =========================================================
# Electron mass path structure
# =========================================================

@dataclass(frozen=True)
class ElectronMassPath:
    psi_me_star: Fraction
    psi_me: Fraction
    mass_scale: Fraction


def psi_me_star_value(
    constants: StructuralConstants,
    psi: PsiValues,
) -> Fraction:
    """
    Structural base path for the electron-mass sector.

    Structural form:
        Ψme* = 24 * [(3/2) * (R・S) * (6・24) - 1]

    Interpretation:
    - (3/2)RS :
        minimal coupled structural pathway

    - (6・24) :
        global expansion into the full structural layer

    - (-1) :
        residual exclusion offset

    - (*24) :
        final projection into the electron-mass sector

    Used as the residual suppression scale in:
        (1 + Ψme*^-2)

    Numerical value:
        Ψme* = 14484
    """
    R = constants.R
    S = constants.S

    psi_me_star = 24 * (Fraction(3, 2) * R * S * (6 * 24) - 1)

    return psi_me_star


def psi_me_value(
    psi: PsiValues,
    psi_me_star: Fraction,
) -> Fraction:
    """
    Full structural complexity of the electron mass.

    Structural form:
        Ψme = 12Ψme* + Ψe/3

    Interpretation:
    - 12Ψme* :
        dominant propagation pathway of the electron-mass structure

    - Ψe/3 :
        electromagnetic projection contribution

    Numerical value:
        Ψme = 175882
    """
    return 12 * psi_me_star + Fraction(psi.psi_e, 3)


def compute_electron_mass_path(
    constants: StructuralConstants,
    psi: PsiValues,
) -> ElectronMassPath:
    """
    Electron mass in structural form.

               (c * 10^-3)^2
    m_e = -----------------------
           Ψme * (1 + Ψme*^-2)

    Interpretation:
    - Ψme      : primary structural complexity
    - Ψme*     : residual correction path
    - c^2 term : propagation-scale origin

    The calculation is performed exactly using Fraction.
    """
    psi_me_star = psi_me_star_value(constants, psi)
    psi_me      = psi_me_value(psi, psi_me_star)

    mass_scale  = Fraction(c, 10**3)**2 / (psi_me * (1 + psi_me_star**-2))

    return ElectronMassPath(
        psi_me_star=psi_me_star,
        psi_me=psi_me,
        mass_scale=mass_scale,
    )


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
        electron_mass_scale=electron_path.mass_scale,
    )

