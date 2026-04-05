from dataclasses import dataclass
from typing import Optional


# =========================================================
# Observed reference values
# =========================================================

DATASET_NAME = "Observed reference values"
DATASET_VERSION = "CODATA 2022 + adopted reference values"


@dataclass(frozen=True)
class ObservedValue:
    name: str
    value: float
    uncertainty: Optional[float] = None
    note: str = ""


# Reference constants (CODATA 2022)
G_VALUE = 6.67430e-11
G_UNC = 1.5e-15
HBAR = 1.054571817e-34
C = 299792458.0

M_P = 1.67262192595e-27
M_E = 9.1093837139e-31


REF_OBSERVED = {
    "vev_gev": ObservedValue(
        name="v [GeV]",
        value=246.22,
        uncertainty=None,
        note="Adopted electroweak vacuum expectation value reference",
    ),
    "gravitational_constant": ObservedValue(
        name="G",
        value=G_VALUE,
        uncertainty=G_UNC,
        note="Newtonian gravitational constant (CODATA 2022)",
    ),
    "sqrt_gravitational_constant": ObservedValue(
        name="sqrt(G)",
        value=G_VALUE ** 0.5,
        uncertainty=None,
        note="Derived from the reference value of G",
    ),
    "alpha_gp": ObservedValue(
        name="alpha_Gp",
        value=G_VALUE * M_P**2 / (HBAR * C),
        uncertainty=None,
        note="Reference proton-proton gravitational coupling derived from CODATA constants",
    ),
    "alpha_ge": ObservedValue(
        name="alpha_Ge",
        value=G_VALUE * M_E**2 / (HBAR * C),
        uncertainty=None,
        note="Reference electron-electron gravitational coupling derived from CODATA constants",
    ),
}
