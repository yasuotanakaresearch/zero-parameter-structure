from dataclasses import dataclass
from math import sqrt


# =========================================================
# Observational cosmology inputs used in Paper 1 Appendix A
# =========================================================

DATASET_NAME = "Observed cosmological reference values"
DATASET_VERSION = "Planck 2018 + DESI DR2 representative comparison"


@dataclass(frozen=True)
class ObservedCosmology:
    name: str
    H0: float
    omega_m: float
    omega_b_h2: float

    @property
    def h(self) -> float:
        return self.H0 / 100.0

    @property
    def omega_b(self) -> float:
        return self.omega_b_h2 / self.h**2

    @property
    def omega_L(self) -> float:
        return 1.0 - self.omega_m

    @property
    def omega_dm(self) -> float:
        return self.omega_m - self.omega_b

    @property
    def Q(self) -> float:
        return sqrt(
            self.omega_m**2
            / (3.0 * self.omega_L * self.omega_b)
        )


# =========================================================
# Representative comparison rows
# =========================================================

# Planck 2018 base-LambdaCDM Plik best-fit row.
PLANCK_2018_PLIK_BEST_FIT = ObservedCosmology(
    name="Planck 2018 Plik best fit",
    H0=67.32,
    omega_m=0.3158,
    omega_b_h2=0.022383,
)

# DESI DR2 w0waCDM rows with published H0 and Omega_m.
# Omega_b and Q are reconstructed using the common BBN value
# omega_b h^2 = 0.02218.
DESI_DR2_CMB_PANTHEON_PLUS = ObservedCosmology(
    name="DESI+CMB+Pantheon+",
    H0=67.51,
    omega_m=0.3114,
    omega_b_h2=0.02218,
)

DESI_DR2_CMB_DESY5 = ObservedCosmology(
    name="DESI+CMB+DESY5",
    H0=66.74,
    omega_m=0.3191,
    omega_b_h2=0.02218,
)


# Backward-compatible alias for scripts expecting PLANCK_2018.
PLANCK_2018 = PLANCK_2018_PLIK_BEST_FIT


# =========================================================
# Regression checks
# =========================================================

assert abs(PLANCK_2018_PLIK_BEST_FIT.omega_b - 0.049389) < 5e-7
assert abs(PLANCK_2018_PLIK_BEST_FIT.omega_dm - 0.266411) < 5e-7
assert abs(PLANCK_2018_PLIK_BEST_FIT.Q - 0.991848) < 5e-7

assert abs(DESI_DR2_CMB_PANTHEON_PLUS.omega_b - 0.048666) < 5e-7
assert abs(DESI_DR2_CMB_PANTHEON_PLUS.Q - 0.982114) < 5e-7

assert abs(DESI_DR2_CMB_DESY5.omega_b - 0.049795) < 5e-7
assert abs(DESI_DR2_CMB_DESY5.Q - 1.000530) < 5e-7
