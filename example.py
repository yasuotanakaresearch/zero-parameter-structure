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
"""

from fractions import Fraction
import math


# =========================================================
# Fixed structural constants
# =========================================================

C = 299_792_458  # exact speed of light in m/s

R = Fraction(13, 6)
S = Fraction(31, 24)


# =========================================================
# Cosmology
# =========================================================

Omega_b = 1 / (3 * R**2 + 3 * R)
Omega_m = 3 * R * Omega_b
Omega_L = 3 * R**2 * Omega_b
Omega_dm = Omega_m - Omega_b


# =========================================================
# Electron sector
# =========================================================

psi_e0 = Fraction((R * S**2) * (6 * 24**2) - 7**2, 2)
delta_e = Fraction(1, 2) + Fraction(1, 5**2)
psi_e = psi_e0 - delta_e

alpha_inv = 4 * math.pi * float(3 * R**2 / S) * (1 + float(1 / psi_e))
alpha = alpha_inv**-1

psi_me_star = 24 * (Fraction(3, 2) * (R * S) * (6 * 24) - 1)
psi_me = 12 * psi_me_star + Fraction(psi_e0, 3)

# Electron rest energy in MeV.
# The expression is kept close to the structural form used in the paper code.
me_c2 = float(
    Fraction(C, 10**3) ** 2
    / (psi_me * (1 + psi_me_star**-2))
    * 10**-6
)


# =========================================================
# Gravity
# =========================================================

psi_g = (12 * (3 * R**2) * (4 * R) + 2 * R) / 4
sqrt_G = (alpha * float(S)) / (math.pi * float(psi_g))
G = sqrt_G**2


# =========================================================
# Quark masses
# =========================================================

psi_d = Fraction(2, 1)
psi_u = 2 * R

K = {
    "u": 1 / psi_u,
    "d": 1 / psi_d,
    "c": 1 + 1 / psi_d,
    "s": 1 - 1 / (2 * psi_d),
    "t": 2 + 1 / psi_u,
    "b": 2 + 1 / psi_d,
}

M0 = float((3 * R**2) * S) * me_c2
A_u = (8 * math.pi * float(R**2)) / float(S)
A_d = (8 * float(R)) / float(S)

m_u = float(K["u"]) * M0
m_d = float(K["d"]) * M0
m_c = float(K["c"]) * M0 * A_u
m_s = float(K["s"]) * M0 * A_d
m_t = float(K["t"]) * M0 * A_u**2
m_b = float(K["b"]) * M0 * A_d**2


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
    print(f"Psi_e0       = {psi_e0}")
    print(f"Psi_e        = {float(psi_e):.12f}")
    print(f"alpha^-1     = {alpha_inv:.12f}")
    print(f"alpha        = {alpha:.12e}")
    print(f"Psi_me*      = {psi_me_star}")
    print(f"Psi_me       = {psi_me}")
    print(f"m_e c^2      = {me_c2:.12f} MeV")
    print()

    print("Gravity")
    print("-------")
    print(f"Psi_G        = {psi_g} = {float(psi_g):.12f}")
    print(f"sqrt(G)      = {sqrt_G:.12e}")
    print(f"G            = {G:.12e}")
    print()

    print("Quark masses")
    print("------------")
    print(f"Psi_u        = {psi_u} = {float(psi_u):.12f}")
    print(f"Psi_d        = {psi_d} = {float(psi_d):.12f}")
    print(f"M0           = {M0:.12f} MeV")
    print(f"A_u          = {A_u:.12f}")
    print(f"A_d          = {A_d:.12f}")
    print()
    print(f"m_u          = {m_u:.12f} MeV")
    print(f"m_d          = {m_d:.12f} MeV")
    print(f"m_c          = {m_c:.12f} MeV")
    print(f"m_s          = {m_s:.12f} MeV")
    print(f"m_t          = {m_t / 1000:.12f} GeV")
    print(f"m_b          = {m_b / 1000:.12f} GeV")
    print()

    print("Note")
    print("----")
    print("These values are computed directly from fixed structural relations.")
    print("For full theory-vs-observation comparisons, run the paper scripts.")


if __name__ == "__main__":
    main()
