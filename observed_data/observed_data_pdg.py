from dataclasses import dataclass
from typing import Optional


# =========================================================
# Observed reference values (PDG-based)
# =========================================================

DATASET_NAME = "Particle Data Group reference values"
DATASET_VERSION = "PDG 2025"


@dataclass(frozen=True)
class ObservedValue:
    name: str
    value: float
    uncertainty: Optional[float] = None
    unit: str = ""
    note: str = ""


PDG_OBSERVED = {
    # -----------------------------------------------------
    # Neutrino sector
    # -----------------------------------------------------
    "neutrino_delta_m21": ObservedValue(
        name="Δm21^2 [eV^2]",
        value=7.50e-5,
        uncertainty=0.19e-5,
    ),
    "neutrino_delta_m32": ObservedValue(
        name="Δm32^2 [eV^2]",
        value=2.451e-3,
        uncertainty=0.026e-3,
    ),

    # -----------------------------------------------------
    # Higgs sector
    # -----------------------------------------------------
    "higgs_mass_gev_pdg": ObservedValue(
        name="m_H [GeV] (PDG)",
        value=125.22,
        uncertainty=0.11,
        note="PDG experimental reference value",
    ),

    # -----------------------------------------------------
    # Quark masses
    # Values are stored in MeV for direct comparison with
    # structural quark-mass predictions.
    # -----------------------------------------------------
    "quark_u_mass_mev": ObservedValue(
        name="m_u [MeV]",
        value=2.16,
        uncertainty=0.07,
        unit="MeV",
        note="PDG 2025; MSbar mass at μ = 2 GeV; CL = 90%",
    ),
    "quark_d_mass_mev": ObservedValue(
        name="m_d [MeV]",
        value=4.70,
        uncertainty=0.07,
        unit="MeV",
        note="PDG 2025; MSbar mass at μ = 2 GeV; CL = 90%",
    ),
    "quark_s_mass_mev": ObservedValue(
        name="m_s [MeV]",
        value=93.5,
        uncertainty=0.8,
        unit="MeV",
        note="PDG 2025; MSbar mass at μ = 2 GeV; CL = 90%",
    ),
    "quark_c_mass_mev": ObservedValue(
        name="m_c [MeV]",
        value=1273.0,
        uncertainty=4.6,
        unit="MeV",
        note="PDG 2025; MSbar mass m(μ = m); CL = 90%",
    ),
    "quark_b_mass_mev": ObservedValue(
        name="m_b [MeV]",
        value=4183.0,
        uncertainty=7.0,
        unit="MeV",
        note="PDG 2025; MSbar mass m(μ = m); CL = 90%",
    ),
    "quark_t_mass_mev_direct": ObservedValue(
        name="m_t [MeV] direct",
        value=172560.0,
        uncertainty=310.0,
        unit="MeV",
        note="PDG 2025; direct measurements; top mass is scheme-dependent",
    ),
    "quark_t_mass_gev_direct": ObservedValue(
        name="m_t [GeV] direct",
        value=172.56,
        uncertainty=0.31,
        unit="GeV",
        note="PDG 2025; direct measurements; top mass is scheme-dependent",
    ),
    "quark_t_mass_gev_pole": ObservedValue(
        name="m_t [GeV] pole",
        value=172.4,
        uncertainty=0.7,
        unit="GeV",
        note="PDG 2025; pole mass from cross-section measurements",
    ),
}
