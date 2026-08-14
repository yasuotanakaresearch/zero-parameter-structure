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

        core_13 = 6R,  core_31 = 24S,
        P_min = 2,  P_mid = 5,  P_max = 7,

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

        alpha^{-1} = 4π B_alpha (1 + 1/Psi_e,eff)

    where the common branch value is inherited from StructuralConstants:

        B_alpha = 3R^2 / S.

    The 4π factor supplies the observational projection, while the
    effective electron index carries the residual structural correction.
    """
    psi_e_eff = psi.psi_e - psi.delta_e

    return projection_term(4) * fraction_to_decimal(
        constants.B_alpha * correction_term(+1, psi_e_eff)
    )


def proton_mass_ratio(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """
    Compute the proton-to-electron mass ratio.

        m_p / m_e = alpha^{-1} A_d (1 - 1/Psi_p,eff)

    where

        A_d = 8R / S

    is inherited as the common structural transfer factor from the
    electromagnetic kernel to the composite nucleon scale.  It does not
    count individual quark constituents.
    """
    psi_p_eff = psi.psi_p + psi.delta_p

    return alpha_inverse(constants, psi) * fraction_to_decimal(
        constants.A_d * correction_term(-1, psi_p_eff)
    )


def neutron_mass_ratio(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """
    Compute the neutron-to-electron mass ratio.

        m_n / m_e = alpha^{-1} A_d (1 - 1/Psi_n,eff)

    The same A_d branch used for the proton supplies the common composite
    nucleon scale.  The proton-neutron separation is introduced only by
    the corresponding effective structural index.
    """
    psi_n_eff = psi.psi_n - psi.delta_n

    return alpha_inverse(constants, psi) * fraction_to_decimal(
        constants.A_d * correction_term(-1, psi_n_eff)
    )


def muon_mass_ratio(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """
    Compute the muon-to-electron mass ratio.

        m_mu / m_e
            = (3/2) 4π B_alpha (1 + 1/Psi_mu,eff)

    The muon therefore inherits the same B_alpha branch that appears in
    alpha^{-1}, with the fixed leading coefficient 3/2 and its own
    effective structural index.
    """
    psi_mu_eff = psi.psi_mu - psi.delta_mu

    return projection_term(4) * fraction_to_decimal(
        Fraction(3, 2)
        * constants.B_alpha
        * correction_term(+1, psi_mu_eff)
    )

def tau_from_mu_ratio(constants: StructuralConstants, psi: PsiValues) -> Decimal:
    """
    Compute the tau-to-muon mass ratio.

        m_tau / m_mu
            = (3/4) A_tau (1 + 1/Psi_tau,eff)

    where the common branch value

        A_tau = 8RS

    is inherited from StructuralConstants.
    """
    psi_tau_eff = psi.psi_tau + psi.delta_tau

    return fraction_to_decimal(
        Fraction(3, 4)
        * constants.A_tau
        * correction_term(+1, psi_tau_eff)
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
# Appendix A: logarithmic sampling of alpha^{-1}(Q)
# =========================================================

@dataclass(frozen=True)
class AlphaRunningCoefficients:
    """Fixed rational coefficients used at the selected mass scales."""

    muon: Fraction
    tau: Fraction
    bottom: Fraction
    w_boson: Fraction
    z_boson: Fraction
    top: Fraction


@dataclass(frozen=True)
class AlphaRunningSample:
    """One discrete logarithmic sample of the inverse electromagnetic coupling."""

    label: str
    mass_gev: Decimal
    coefficient: Fraction
    delta_alpha_inv: Decimal
    alpha_inv: Decimal


def k_n(n: int) -> Fraction:
    """
    Discrete structural coefficient used in Appendix A:

        K_n = (1 + 1/n)^(-1) = n/(n + 1)

    The index n is a structural label, not a particle-generation number.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    return Fraction(n, n + 1)


def alpha_running_coefficients() -> AlphaRunningCoefficients:
    """
    Return the rational coefficients assigned to the characteristic scales:

        K_alpha,mu  = K_3 / 4
        K_alpha,tau = K_3 / 2
        K_alpha,b   = K_2 + K_3 - 1
        K_alpha,W   = K_2
        K_alpha,Z   = K_3
        K_alpha,t   = K_4
    """
    k2 = k_n(2)
    k3 = k_n(3)
    k4 = k_n(4)

    return AlphaRunningCoefficients(
        muon=k3 / 4,
        tau=k3 / 2,
        bottom=k2 + k3 - 1,
        w_boson=k2,
        z_boson=k3,
        top=k4,
    )


def logarithmic_alpha_shift(
    mass_gev: Decimal,
    electron_mass_gev: Decimal,
    coefficient: Fraction,
) -> Decimal:
    """
    Compute the discrete logarithmic shift in the inverse coupling:

        Delta_alpha,ln(m_i)
            = K_alpha,i * ln(m_i / m_e)

    Both masses must be expressed in the same unit.  GeV is used by the
    reference implementation so that the logarithm is dimensionless.
    """
    mass_gev = Decimal(mass_gev)
    electron_mass_gev = Decimal(electron_mass_gev)

    if mass_gev <= 0 or electron_mass_gev <= 0:
        raise ValueError("mass scales must be positive")

    return fraction_to_decimal(coefficient) * (mass_gev / electron_mass_gev).ln()


def compute_alpha_running_sample(
    label: str,
    mass_gev: Decimal,
    electron_mass_gev: Decimal,
    coefficient: Fraction,
    alpha_inv_zero: Decimal,
) -> AlphaRunningSample:
    """
    Evaluate one characteristic-scale sample:

        alpha_ln^{-1}(m_i)
            = alpha^{-1}(0) - Delta_alpha,ln(m_i)

    This is a discrete structural sampling formula.  It is not implemented
    as a continuous beta function and does not replace standard QED running.
    """
    delta = logarithmic_alpha_shift(
        mass_gev=mass_gev,
        electron_mass_gev=electron_mass_gev,
        coefficient=coefficient,
    )

    return AlphaRunningSample(
        label=label,
        mass_gev=Decimal(mass_gev),
        coefficient=coefficient,
        delta_alpha_inv=delta,
        alpha_inv=Decimal(alpha_inv_zero) - delta,
    )


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

