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
    unit: str = ""
    note: str = ""


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
    "tau-muon_mass_ratio": ObservedValue(
        name="m_tau / m_mu",
        value=16.8170,
        uncertainty=0.0011,
    ),
    "tau-electron_mass_ratio": ObservedValue(
        name="m_tau / m_e",
        value=3477.23,
        uncertainty=0.23,
    ),
    "gravitational_constant": ObservedValue(
        name="G",
        value=6.67430e-11,
        uncertainty=1.5e-15,
    ),
    "planck_mass": ObservedValue(
        name="M_Pl",
        value=2.176434e-8,
        uncertainty=2.4e-13,
        unit="kg",
    ),
    "proton_mass": ObservedValue(
        name="M_P",
        value=1.67262192595e-27,
        uncertainty=5.2e-37,
        unit="kg",
    ),
    "electron_mass": ObservedValue(
        name="M_E",
        value=9.1093837139e-31,
        uncertainty=2.8e-40,
        unit="kg",
    ),
}
