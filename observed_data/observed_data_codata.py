from dataclasses import dataclass
from typing import Optional


# =========================================================
# Observational data (CODATA 2022)
# =========================================================

DATASET_NAME = "Observed reference values"
DATASET_VERSION = "CODATA 2022"


@dataclass(frozen=True)
class ObservedValue:
    name: str
    value: float
    uncertainty: Optional[float] = None


OBSERVED = {
    "alpha_inv": ObservedValue(
        name="alpha^-1",
        value=137.035999177,
        uncertainty=0.000000021,
    ),
    "muon_ratio": ObservedValue(
        name="m_mu / m_e",
        value=206.7682827,
        uncertainty=0.0000046,
    ),
    "proton_ratio": ObservedValue(
        name="m_p / m_e",
        value=1836.152673426,
        uncertainty=0.000000032,
    ),
    "neutron_ratio": ObservedValue(
        name="m_n / m_e",
        value=1838.68366200,
        uncertainty=0.00000074,
    ),
    "electron_rest_energy_mev": ObservedValue(
        name="m_e c^2 [MeV]",
        value=0.51099895069,
        uncertainty=0.00000000016,
    ),
}
