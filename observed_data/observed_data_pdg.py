from dataclasses import dataclass
from typing import Optional


# =========================================================
# Observed reference values
# =========================================================

DATASET_NAME = "Particle Data Group and paper-level reference values"
DATASET_VERSION = "PDG 2025 / Paper 6 reference set"


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
        name="Delta m21^2",
        value=7.50e-5,
        uncertainty=0.19e-5,
        unit="eV^2",
        note="Representative neutrino-oscillation reference value",
    ),
    "neutrino_delta_m32": ObservedValue(
        name="Delta m32^2",
        value=2.451e-3,
        uncertainty=0.026e-3,
        unit="eV^2",
        note="Representative neutrino-oscillation reference value",
    ),

    # -----------------------------------------------------
    # Paper 6: Higgs, electroweak, and strong coupling
    # Central values follow the comparison table used in
    # the Paper 6 manuscript.
    # -----------------------------------------------------
    "higgs_mass_gev_pdg": ObservedValue(
        name="m_H",
        value=125.20,
        uncertainty=0.11,
        unit="GeV",
        note="Representative PDG Higgs-mass reference value",
    ),
    "electroweak_vev_gev": ObservedValue(
        name="v",
        value=246.2197,
        unit="GeV",
        note="Electroweak vacuum expectation value used in Paper 6",
    ),
    "electron_yukawa": ObservedValue(
        name="y_e",
        value=2.935028e-6,
        note="Electron Yukawa reference value used in Paper 6",
    ),
    "weak_mixing_on_shell": ObservedValue(
        name="sin^2(theta_W)",
        value=0.2232027,
        note="On-shell value derived from the listed W- and Z-boson masses",
    ),
    "w_mass_gev": ObservedValue(
        name="m_W",
        value=80.3692,
        unit="GeV",
        note="Representative W-boson mass reference value used in Paper 6",
    ),
    "z_mass_gev": ObservedValue(
        name="m_Z",
        value=91.1876,
        unit="GeV",
        note="Representative Z-boson mass reference value used in Paper 6",
    ),
    "alpha_s_mz": ObservedValue(
        name="alpha_s(m_Z)",
        value=0.1180,
        uncertainty=0.0009,
        note="Representative strong-coupling reference value at Q = m_Z",
    ),

    # -----------------------------------------------------
    # Quark masses
    # Values are stored in MeV for direct comparison with
    # structural quark-mass predictions.
    # -----------------------------------------------------
    "quark_u_mass_mev": ObservedValue(
        name="m_u",
        value=2.16,
        uncertainty=0.07,
        unit="MeV",
        note="PDG 2025; MSbar mass at mu = 2 GeV; CL = 90%",
    ),
    "quark_d_mass_mev": ObservedValue(
        name="m_d",
        value=4.70,
        uncertainty=0.07,
        unit="MeV",
        note="PDG 2025; MSbar mass at mu = 2 GeV; CL = 90%",
    ),
    "quark_s_mass_mev": ObservedValue(
        name="m_s",
        value=93.5,
        uncertainty=0.8,
        unit="MeV",
        note="PDG 2025; MSbar mass at mu = 2 GeV; CL = 90%",
    ),
    "quark_c_mass_mev": ObservedValue(
        name="m_c",
        value=1273.0,
        uncertainty=4.6,
        unit="MeV",
        note="PDG 2025; MSbar mass m(mu = m); CL = 90%",
    ),
    "quark_b_mass_mev": ObservedValue(
        name="m_b",
        value=4183.0,
        uncertainty=7.0,
        unit="MeV",
        note="PDG 2025; MSbar mass m(mu = m); CL = 90%",
    ),
    "quark_t_mass_mev_direct": ObservedValue(
        name="m_t direct",
        value=172560.0,
        uncertainty=310.0,
        unit="MeV",
        note="PDG 2025; direct measurements; top mass is scheme-dependent",
    ),
    "quark_t_mass_gev_direct": ObservedValue(
        name="m_t direct",
        value=172.56,
        uncertainty=0.31,
        unit="GeV",
        note="PDG 2025; direct measurements; top mass is scheme-dependent",
    ),
    "quark_t_mass_gev_pole": ObservedValue(
        name="m_t pole",
        value=172.4,
        uncertainty=0.7,
        unit="GeV",
        note="PDG 2025; pole mass from cross-section measurements",
    ),
}


# Illustrative reference values for the Appendix-level alpha_s(Q)
# scale-trend comparison in Paper 6. These are kept separate from
# PDG_OBSERVED because the table is not presented as one uniform
# high-order extraction with a single threshold convention.
PAPER6_ALPHA_S_REFERENCE = {
    "m_tau": 0.31740,
    "m_b": 0.22426,
    "5": 0.21291,
    "10": 0.17815,
    "20": 0.15341,
    "35": 0.13805,
    "m_W": 0.12030,
    "m_Z": 0.11800,
    "m_t": 0.10761,
    "200": 0.10572,
    "500": 0.09515,
    "1000": 0.08847,
}
