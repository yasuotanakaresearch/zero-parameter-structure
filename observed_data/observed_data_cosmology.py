from dataclasses import dataclass


# =========================================================
# Observed cosmological reference values
# =========================================================

DATASET_NAME = "Observed cosmological reference values"
DATASET_VERSION = "Planck 2018 example"


@dataclass(frozen=True)
class ObservedCosmology:
    name: str
    omega_m: float
    omega_b: float
    omega_lambda: float
    h: float


PLANCK_2018 = ObservedCosmology(
    name="Planck 2018",
    h=0.674,
    omega_m=0.315,
    omega_b=0.0224 / 0.674**2,
    omega_lambda=1.0 - 0.315,
)
