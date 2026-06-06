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
    unit: str = ""
    note: str = ""


# Fermi coupling constant
GF=1.1663787e-5


REF_OBSERVED = {
    "higgs_mass_gev_repr": ObservedValue(
        name="m_H [GeV] (representative)",
        value=125.1,
        uncertainty=None,
        unit="GeV",
        note="Representative value adopted for structural comparison",
    ),
    "vev_gev": ObservedValue(
        name="v [GeV]",
        value=(2.0**0.5 * GF) ** (-1/2),
        uncertainty=None,
        unit="GeV",
        note="Adopted electroweak vacuum expectation value reference",
    ),
    "sqrt_gravitational_constant": ObservedValue(
        name="sqrt(G)",
        value=6.67430e-11 ** 0.5,
        uncertainty=None,
        note="Derived from the reference value of G",
    ),
}
