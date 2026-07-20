"""
End-to-end minimal example for Zero Parameter Structure.

This script shows that cosmological density ratios, electron-sector quantities,
gravity, quark masses, neutrino masses, and Higgs/electroweak/strong-coupling
scale relations can be computed from the same fixed structural definitions.

The file is organized into independent sections so that each section can later
be transferred to a separate Jupyter Notebook cell with minimal modification.

No free parameters. No tuning. Only structure.

For full theory-vs-observation comparisons, run:

    python -m code.paper1_cosmology
    python -m code.paper2_electron
    python -m code.paper3_gravity
    python -m code.paper4_quark_mass
    python -m code.paper5_neutrino
    python -m code.paper6_higgs_electroweak
"""

from fractions import Fraction
import math


# =========================================================
# Physical constants
# =========================================================

c = 299792458       # exact, m/s
h = 6.62607015e-34  # exact, J s
hbar = h / (2 * math.pi)


# =========================================================
# Common structural definitions
# =========================================================

P_MIN = 1 + 1
P_MAX = 3 + 4
P_MID = P_MAX - P_MIN

R = (Fraction(1) + Fraction(P_MIN, 24)) * 2
S =  Fraction(1) + Fraction(P_MAX, 24)


# =========================================================
# Shared helpers
# =========================================================

def alpha2_transfer(alpha_value: float, i: int, j: int) -> float:
    """Return alpha^2_[i->j] = alpha^(2(i-j))."""
    return alpha_value ** (2 * (i - j))


def print_rows(rows: list[tuple[str, float, str, str]]) -> None:
    """Print rows as name, formatted value, and optional unit."""
    for name, value, unit, number_format in rows:
        value_text = format(float(value), number_format)
        print(f"{name:<18} = {value_text:>20} {unit:<8}")


# =========================================================
# Cosmology
# =========================================================

Omega_b  = 1 / (3 * R**2 + 3 * R)
Omega_m  = 3 * R    * Omega_b
Omega_L  = 3 * R**2 * Omega_b
Omega_dm = Omega_m - Omega_b


# =========================================================
# Electromagnetic coupling and mass hierarchy
# =========================================================

core_13 = R * 6
core_31 = S * 24

# Structural backbone values Psi_0.
psi_e0   = Fraction(3, 2) * (core_13    * core_31**2 - P_MAX**2) / 3
psi_p0   = Fraction(3, 2) * (core_13**2 * core_31    + P_MAX**2) / 12
psi_n0   = Fraction(3, 2) * (core_13    * core_31    + P_MIN**2) * 12
psi_mu0  = Fraction(psi_p0, P_MIN**2)
psi_tau0 = psi_p0

# Residual structural fluctuations delta_psi.
delta_e   = Fraction(1, 2) + Fraction(1, P_MID**2)
delta_p   = Fraction(6**2) * Fraction(1, psi_e0 + 24 - Fraction(1, 2))
delta_n   = Fraction(2, 3) * Fraction(12*P_MAX - 1, 12*P_MAX + 3)
delta_mu  = Fraction(1, 2) - Fraction(1, P_MAX**2) + Fraction(1, (psi_mu0 * P_MAX**2))
delta_tau = Fraction(1, 1)

psi_e     = psi_e0   - delta_e
psi_p     = psi_p0   + delta_p
psi_n     = psi_n0   - delta_n
psi_mu    = psi_mu0  - delta_mu
psi_tau   = psi_tau0 + delta_tau

alpha_inv =         4*math.pi * (3*R**2 / S) * (1 + 1/psi_e)
mmu_me    = (3/2) * 4*math.pi * (3*R**2 / S) * (1 + 1/psi_mu)
mtau_mmu  = (3/4)             * (8*R    * S) * (1 + 1/psi_tau)
mp_me     =         alpha_inv * (8*R    / S) * (1 - 1/psi_p)
mn_me     =         alpha_inv * (8*R    / S) * (1 - 1/psi_n)
mtau_me   = mtau_mmu * mmu_me

alpha = alpha_inv**-1

# Electron rest energy in MeV.
# The expression is kept close to the structural form used in the paper code.
psi_me_star = 24 * (Fraction(3, 2) * (R * S) * (6 * 24) - 1)
psi_me      = 12 * psi_me_star + Fraction(psi_e0, 3)
me_ev       = Fraction(c, 10**3) ** 2 / (psi_me * (1 + psi_me_star**-2))
me_mev      = me_ev * 10**-6  # MeV
me_gev      = me_ev * 10**-9  # GeV


# =========================================================
# Gravity
# =========================================================

psi_g      = (12 * (3 * R**2) * (4 * R) + 2 * R) / 4
psi_g0     = R * S**2 * (12 * 24)
psi_g_star = 4 * psi_g - 3 * (1 + 1 / psi_g0)

sqrt_G   = (alpha * S) / (math.pi * psi_g)
G        = sqrt_G**2
alpha_Gp = alpha**24 * mp_me**4 / (1 + 1 / psi_g_star)
alpha_Ge = alpha**24 * mp_me**2 / (1 + 1 / psi_g_star)

g_corr = (1 + 1 / psi_g_star)**(-1/2)
M_Pl   = math.sqrt(hbar * c / G)
M_P    = M_Pl * alpha**12 * mp_me**2 * g_corr
M_E    = M_Pl * alpha**12 * mp_me    * g_corr


# =========================================================
# Quark masses
# =========================================================

K_q = {
    "u": (    1 / (2 * R)),
    "d": (    1 /  2),
    "c": (1 + 1 /  2),
    "s": (1 - 1 /  4),
    "t": (2 + 1 / (2 * R)),
    "b": (2 + 1 /  2),
}

B_q = (3 * R**2) * S
A_d = (8 * R) / S
A_u = math.pi * R * A_d

m_u = me_mev * K_q["u"] * B_q
m_d = me_mev * K_q["d"] * B_q
m_c = me_mev * K_q["c"] * B_q * A_u
m_s = me_mev * K_q["s"] * B_q * A_d
m_t = me_gev * K_q["t"] * B_q * A_u**2
m_b = me_gev * K_q["b"] * B_q * A_d**2


# =========================================================
# Neutrino masses
# =========================================================

B_nu = 12 * S * alpha2_transfer(alpha, 2, 0)

phi_nu = (
    1,
    1 / (3 * R**2),
    1 / R,
)

# Dimensionless mass ratios m_nu,n / m_e for n = 0, 1, 2.
nu_mass_ratios = tuple(
    B_nu * (n + phi_nu[n])
    for n in range(3)
)

# Absolute neutrino masses in eV.
m_nu1_ev, m_nu2_ev, m_nu3_ev = tuple(
    ratio * me_ev
    for ratio in nu_mass_ratios
)

dm21 = m_nu2_ev**2 - m_nu1_ev**2
dm31 = m_nu3_ev**2 - m_nu1_ev**2
dm32 = m_nu3_ev**2 - m_nu2_ev**2
sum_mnu = m_nu1_ev + m_nu2_ev + m_nu3_ev


# =========================================================
# Higgs, electroweak, and strong-coupling scales
# =========================================================

# Higgs-sector base structure and fixed structural integers.
B_H   = 12 * R * alpha2_transfer(alpha, 1, 2)
Psi_H = 12 * (4 * (3 * R**2) + 3)
Psi_v = 3**2 * Psi_H

# Higgs and vacuum scales.
mH_over_me = (1 / 2.0) * B_H + Psi_H
v_over_me  = B_H - Psi_v
mH_GeV     = mH_over_me * me_gev
v_GeV      = v_over_me  * me_gev

# Electron Yukawa and weak-sector values.
ye = math.sqrt(2) / v_over_me
sin2_thetaW = 2 * math.pi * alpha * R**2 * (1 + 3**-3)
cos_thetaW  = math.sqrt(1 - sin2_thetaW)
mW_over_me  = (1 / ye) / R * (1 + 1 / Psi_v)
mW_GeV      = mW_over_me * me_gev
mZ_GeV      = mW_GeV / cos_thetaW
alpha_s_mZ  = 1 - mW_GeV / mZ_GeV


# =========================================================
# Output
# =========================================================

def main() -> None:
    print("Zero Parameter Structure - Minimal End-to-End Example")
    print("=====================================================")
    print(f"P_MIN = {P_MIN}")
    print(f"P_MAX = {P_MAX}")
    print(f"P_MID = {P_MID}")
    print(f"R     = {R} = {float(R):.12f}")
    print(f"S     = {S} = {float(S):.12f}")
    print()

    print("Cosmology")
    print("---------")
    print(f"Omega_L  = {float(Omega_L):.12f} = {Omega_L}")
    print(f"Omega_m  = {float(Omega_m):.12f} = {Omega_m}")
    print(f"Omega_dm = {float(Omega_dm):.12f} = {Omega_dm}")
    print(f"Omega_b  = {float(Omega_b):.12f} = {Omega_b}")
    print()

    print("Electromagnetic coupling and mass hierarchy")
    print("--------------------------------------------")
    print_rows([
        ("Psi_e", psi_e, "", ".12f"),
        ("Psi_p", psi_p, "", ".12f"),
        ("Psi_n", psi_n, "", ".12f"),
        ("Psi_mu", psi_mu, "", ".12f"),
        ("Psi_tau", psi_tau, "", ".12f"),
        ("alpha^-1", alpha_inv, "", ".12f"),
        ("alpha", alpha, "", ".12e"),
        ("m_p / m_e", mp_me, "", ".12f"),
        ("m_n / m_e", mn_me, "", ".12f"),
        ("m_mu / m_e", mmu_me, "", ".12f"),
        ("m_tau / m_mu", mtau_mmu, "", ".12f"),
        ("m_tau / m_e", mtau_me, "", ".12f"),
        ("Psi_me*", psi_me_star, "", ".12f"),
        ("Psi_me", psi_me, "", ".12f"),
        ("m_e c^2", me_ev, "eV", ".9f"),
        ("m_e c^2", me_mev, "MeV", ".15f"),
        ("m_e c^2", me_gev, "GeV", ".14e"),
    ])
    print()

    print("Gravity")
    print("-------")
    print_rows([
        ("Psi_G", psi_g, "", ".12f"),
        ("Psi_G*", psi_g_star, "", ".12f"),
        ("sqrt(G)", sqrt_G, "", ".12e"),
        ("G", G, "", ".12e"),
        ("alpha_Gp", alpha_Gp, "", ".12e"),
        ("alpha_Ge", alpha_Ge, "", ".12e"),
        ("M_Pl", M_Pl, "kg", ".12e"),
        ("M_P", M_P, "kg", ".12e"),
        ("M_E", M_E, "kg", ".12e"),
    ])
    print()

    print("Quark masses")
    print("------------")
    print_rows([
        ("B_q", B_q, "", ".12f"),
        ("A_u", A_u, "", ".12f"),
        ("A_d", A_d, "", ".12f"),
        ("m_u", m_u, "MeV", ".12f"),
        ("m_d", m_d, "MeV", ".12f"),
        ("m_c", m_c, "MeV", ".12f"),
        ("m_s", m_s, "MeV", ".12f"),
        ("m_t", m_t, "GeV", ".12f"),
        ("m_b", m_b, "GeV", ".12f"),
    ])
    print()

    print("Neutrino masses")
    print("----------------")
    print_rows([
        ("m1 / m_e", nu_mass_ratios[0], "", ".12e"),
        ("m2 / m_e", nu_mass_ratios[1], "", ".12e"),
        ("m3 / m_e", nu_mass_ratios[2], "", ".12e"),
        ("m1 c^2", m_nu1_ev, "eV", ".12f"),
        ("m2 c^2", m_nu2_ev, "eV", ".12f"),
        ("m3 c^2", m_nu3_ev, "eV", ".12f"),
        ("Sum m_nu", sum_mnu, "eV", ".12f"),
        ("Delta m21^2", dm21, "eV^2", ".12e"),
        ("Delta m31^2", dm31, "eV^2", ".12e"),
        ("Delta m32^2", dm32, "eV^2", ".12e"),
    ])
    print()

    print("Higgs, electroweak, and strong-coupling scales")
    print("----------------------------------------------")
    print_rows([
        ("B_H", B_H, "", ".12f"),
        ("Psi_H", Psi_H, "", ".0f"),
        ("Psi_v", Psi_v, "", ".0f"),
        ("m_H / m_e", mH_over_me, "", ".12f"),
        ("v / m_e", v_over_me, "", ".12f"),
        ("m_H", mH_GeV, "GeV", ".12f"),
        ("v", v_GeV, "GeV", ".12f"),
        ("y_e", ye, "", ".12e"),
        ("sin^2(theta_W)", sin2_thetaW, "", ".12f"),
        ("m_W / m_e", mW_over_me, "", ".12f"),
        ("m_W", mW_GeV, "GeV", ".12f"),
        ("m_Z", mZ_GeV, "GeV", ".12f"),
        ("alpha_s(m_Z)", alpha_s_mZ, "", ".12f"),
    ])
    print()

    print("Note")
    print("----")
    print("Each section is arranged for later conversion into a Jupyter cell.")
    print("For full theory-vs-observation comparisons, run the paper scripts.")


if __name__ == "__main__":
    main()
