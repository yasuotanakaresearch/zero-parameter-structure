from dataclasses import dataclass
from typing import Optional


# =========================================================
# Published comparison values
# =========================================================

DATASET_NAME = "Published comparison values"
DATASET_VERSION = (
    "Planck Collaboration VI (2020) + Riess et al. (2022) + "
    "McGaugh et al. (2016) + Tully et al. (2008)"
)


@dataclass(frozen=True)
class ObservedValue:
    name: str
    value: float
    uncertainty: Optional[float] = None
    unit: str = ""
    note: str = ""
    reference: str = ""


REF_OBSERVED = {
    "planck_2018_h0_best_fit": ObservedValue(
        name="Planck 2018 base-LambdaCDM H0 (Plik best fit)",
        value=67.32,
        uncertainty=None,
        unit="km s^-1 Mpc^-1",
        note=(
            "Plik best-fit value from Planck TT,TE,EE+lowE+lensing. "
            "The corresponding marginalized result is 67.36 +/- 0.54 "
            "km s^-1 Mpc^-1."
        ),
        reference=(
            "Planck Collaboration VI (2020), "
            "Planck 2018 results. VI. Cosmological parameters, "
            "Astronomy & Astrophysics 641, A6, Table 1, "
            "doi:10.1051/0004-6361/201833910"
        ),
    ),
    "riess_2022_shoes_h0": ObservedValue(
        name="SH0ES Cepheid-SN Ia H0",
        value=73.04,
        uncertainty=1.04,
        unit="km s^-1 Mpc^-1",
        note=(
            "Baseline local-distance-ladder result including systematic "
            "uncertainties."
        ),
        reference=(
            "Riess et al. (2022), "
            "A Comprehensive Measurement of the Local Value of the "
            "Hubble Constant with 1 km s^-1 Mpc^-1 Uncertainty from the "
            "Hubble Space Telescope and the SH0ES Team, "
            "The Astrophysical Journal Letters 934, L7, "
            "doi:10.3847/2041-8213/ac5c5b"
        ),
    ),
    "mcgaugh_2016_g_dagger": ObservedValue(
        name="RAR characteristic acceleration g_dagger",
        value=1.20e-10,
        uncertainty=None,
        unit="m s^-2",
        note=(
            "Best-fit radial-acceleration-relation scale. The quoted "
            "uncertainties are +/-0.02 (random) and +/-0.24 (systematic), "
            "in units of 1e-10 m s^-2."
        ),
        reference=(
            "McGaugh, Lelli, and Schombert (2016), "
            "Radial Acceleration Relation in Rotationally Supported "
            "Galaxies, Physical Review Letters 117, 201101, "
            "doi:10.1103/PhysRevLett.117.201101"
        ),
    ),
    "tully_2008_local_sheet_cmb_velocity": ObservedValue(
        name="Local Sheet velocity relative to the CMB frame",
        value=631.0,
        uncertainty=20.0,
        unit="km s^-1",
        note=(
            "Magnitude of the Local Sheet motion relative to the CMB "
            "reference frame."
        ),
        reference=(
            "Tully et al. (2008), "
            "Our Peculiar Motion Away from the Local Void, "
            "The Astrophysical Journal 676, 184-205, "
            "doi:10.1086/527428"
        ),
    ),
}
