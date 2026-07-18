"""
End-to-end minimal example for Zero Parameter Structure.

This script shows that cosmological density ratios, electron-sector quantities,
gravity, and quark masses can be computed from the same fixed structural
constants

    R = 13/6,  S = 31/24.

No free parameters. No tuning. Only structure.

For full theory-vs-observation comparisons, run the paper scripts:

    python -m code.paper1_cosmology
    python -m code.paper2_electron
    python -m code.paper3_gravity
    python -m code.paper4_quark_mass
    python -m code.paper5_neutrino
"""

from fractions import Fraction
import math


# =========================================================
# Fixed structural constants
# =========================================================

c = 299792458  # exact speed of light in m/s

P_MIN = 1 + 1
P_MAX = 3 + 4
P_MID = P_MAX - P_MIN

R = (Fraction(1) + Fraction(P_MIN, 24)) * 2
S =  Fraction(1) + Fraction(P_MAX, 24)


# =========================================================
# Cosmology
# =========================================================

Omega_b  = 1 / (3 * R**2 + 3 * R)
Omega_m  = 3 * R    * Omega_b
Omega_L  = 3 * R**2 * Omega_b
Omega_dm = Omega_m - Omega_b


# =========================================================
# Electron sector
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
tau_mu    = (3/4)             * (8*R    * S) * (1 + 1/psi_tau)
mp_me     =         alpha_inv * (8*R    / S) * (1 - 1/psi_p)
mn_me     =         alpha_inv * (8*R    / S) * (1 - 1/psi_n)
tau_me    = tau_mu * mmu_me

alpha = alpha_inv**-1

# Electron rest energy in MeV.
# The expression is kept close to the structural form used in the paper code.
psi_me_star = 24 * (Fraction(3, 2) * (R * S) * (6 * 24) - 1)
psi_me      = 12 * psi_me_star + Fraction(psi_e0, 3)
me_c2       = Fraction(c, 10**3) ** 2 / (psi_me * (1 + psi_me_star**-2)) * 10**-6


# =========================================================
# Gravity
# =========================================================

psi_g = (12 * (3 * R**2) * (4 * R) + 2 * R) / 4
sqrt_G = (alpha * S) / (math.pi * psi_g)
G = sqrt_G**2


# =========================================================
# Quark masses
# =========================================================

K = {
    "u": (    1 / (2 * R)),
    "d": (    1 /  2),
    "c": (1 + 1 /  2),
    "s": (1 - 1 /  4),
    "t": (2 + 1 / (2 * R)),
    "b": (2 + 1 /  2),
}

M0  = (3 * R**2) * S * me_c2
A_d = (8 * R) / S
A_u = math.pi * R * A_d

m_u = K["u"] * M0
m_d = K["d"] * M0
m_c = K["c"] * M0 * A_u
m_s = K["s"] * M0 * A_d
m_t = K["t"] * M0 * A_u**2
m_b = K["b"] * M0 * A_d**2

# =========================================================
# Neutrino masses
# =========================================================

m1_over_me = 12 * S * alpha**4
m2_over_me = m1_over_me * (1 + 1 / (3 * R**2))
m3_over_me = m1_over_me * (2 + 1 / R)

# Convert electron rest energy from MeV to eV.
me_c2_ev = me_c2 * 10**6

m_nu1 = m1_over_me * me_c2_ev
m_nu2 = m2_over_me * me_c2_ev
m_nu3 = m3_over_me * me_c2_ev

dm21 = m_nu2**2 - m_nu1**2
dm31 = m_nu3**2 - m_nu1**2
dm32 = m_nu3**2 - m_nu2**2

sum_mnu = m_nu1 + m_nu2 + m_nu3


# =========================================================
# Output
# =========================================================

def main() -> None:
    print("Zero Parameter Structure — Minimal End-to-End Example")
    print("=====================================================")
    print(f"R = {R} = {float(R):.12f}")
    print(f"S = {S} = {float(S):.12f}")
    print()

    print("Cosmology")
    print("---------")
    print(f"Omega_L  = {float(Omega_L):.12f} = {Omega_L}")
    print(f"Omega_m  = {float(Omega_m):.12f} = {Omega_m}")
    print(f"Omega_dm = {float(Omega_dm):.12f} = {Omega_dm}")
    print(f"Omega_b  = {float(Omega_b):.12f} = {Omega_b}")
    print()

    print("Electron sector")
    print("---------------")
    print(f"Psi_e        = {float(psi_e):.12f}")
    print(f"Psi_p        = {float(psi_p):.12f}")
    print(f"Psi_n        = {float(psi_n):.12f}")
    print(f"Psi_mu       = {float(psi_mu):.12f}")
    print(f"Psi_tau      = {float(psi_tau):.12f}")
    print(f"alpha^-1     = {alpha_inv:.12f}")
    print(f"alpha        = {alpha:.12e}")
    print(f"mp/me        = {mp_me:.12f}")
    print(f"mn/me        = {mn_me:.12f}")
    print(f"mmu/me       = {mmu_me:.12f}")
    print(f"tau/mmu      = {tau_mu:.12f}")
    print(f"tau/me       = {tau_me:.12f}")
    print(f"Psi_me*      = {psi_me_star}")
    print(f"Psi_me       = {psi_me}")
    print(f"m_e c^2      = {me_c2:.15f} MeV")
    print()

    print("Gravity")
    print("-------")
    print(f"Psi_G        = {psi_g} = {float(psi_g):.12f}")
    print(f"sqrt(G)      = {sqrt_G:.12e}")
    print(f"G            = {G:.12e}")
    print()

    print("Quark masses")
    print("------------")
    print(f"M0           = {M0:.12f} MeV")
    print(f"A_u          = {A_u:.12f}")
    print(f"A_d          = {float(A_d):.12f}")
    print()
    print(f"m_u          = {m_u:.12f} MeV")
    print(f"m_d          = {m_d:.12f} MeV")
    print(f"m_c          = {m_c:.12f} MeV")
    print(f"m_s          = {m_s:.12f} MeV")
    print(f"m_t          = {m_t / 1000:.12f} GeV")
    print(f"m_b          = {m_b / 1000:.12f} GeV")
    print()

    print("Neutrino masses")
    print("----------------")
    print(f"m1 / me      = {m1_over_me:.12e}")
    print(f"m2 / me      = {m2_over_me:.12e}")
    print(f"m3 / me      = {m3_over_me:.12e}")
    print()
    print(f"m1 c^2       = {m_nu1:.12f} eV")
    print(f"m2 c^2       = {m_nu2:.12f} eV")
    print(f"m3 c^2       = {m_nu3:.12f} eV")
    print(f"Sum mnu      = {sum_mnu:.12f} eV")
    print()
    print(f"Delta m21^2  = {dm21:.12e} eV^2")
    print(f"Delta m31^2  = {dm31:.12e} eV^2")
    print(f"Delta m32^2  = {dm32:.12e} eV^2")
    print()

    print("Note")
    print("----")
    print("These values are computed directly from fixed structural relations.")
    print("For full theory-vs-observation comparisons, run the paper scripts.")


if __name__ == "__main__":
    main()
