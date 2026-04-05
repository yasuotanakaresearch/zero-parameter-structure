from dataclasses import dataclass
from typing import Optional


# =========================================================
# Observed reference values (PDG-based)
# =========================================================

DATASET_NAME = "Particle Data Group reference values"
DATASET_VERSION = "PDG 2024 / 2025 update"


@dataclass(frozen=True)
class ObservedValue:
    name: str
    value: float
    uncertainty: Optional[float] = None
    note: str = ""


PDG_OBSERVED = {
    "tau_mass_mev": ObservedValue(
        name="m_tau [MeV]",
        value=1776.93,
        uncertainty=0.09,
        note="PDG tau mass reference",
    ),
    "tau_ratio": ObservedValue(
        name="m_tau / m_e",
        value=1776.93 / 0.51099895069,
        uncertainty=None,
        note="Derived from PDG tau mass and CODATA 2022 electron rest energy",
    ),
    "tau_from_mu_ratio": ObservedValue(
        name="m_tau / m_mu",
        value=(1776.93 / 0.51099895069) / 206.7682827,
        uncertainty=None,
        note="Derived from tau/e and CODATA 2022 muon/e ratio",
    ),
    "higgs_mass_gev_repr": ObservedValue(
        name="m_H [GeV] (representative)",
        value=125.1,
        uncertainty=None,
        note="Representative value adopted for structural comparison",
    ),
    "higgs_mass_gev_pdg": ObservedValue(
        name="m_H [GeV] (PDG)",
        value=125.25,
        uncertainty=0.17,
        note="PDG experimental reference value",
    ),
}
