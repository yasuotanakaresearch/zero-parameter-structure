#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZERO-PARAMETER PARTICLE MASS & SCALE MAP — 2026 EDITION

Merged renderer based on the user's micro-adjusted pixel-aligned background.

Pipeline:
  1. Compute all displayed physical values from repository core/.
  2. Render the pixel-aligned Matplotlib background from those computed values.
  3. Crop and overlay characters using the finalized 2026 scales and positions.
  4. Draw zero-parameter structural-value boxes.
  5. Export the final 1536x1024 PNG.

NO generative image AI is used.

Usage:
    python particle_mass_map.py \
        --characters character_sheet.png \
        --output zero_parameter_particle_mass_scale_map_2026.png
"""

from __future__ import annotations

import argparse
import sys
from decimal import Decimal
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np



# ============================================================
# CORE INTEGRATION
# ============================================================
#
# This file is intended to live in tools/:
#
#   repository/
#   ├─ core/
#   │  ├─ structural_constants.py
#   │  ├─ structural_electron.py
#   │  ├─ structural_gravity.py
#   │  ├─ structural_higgs_electroweak.py
#   │  ├─ structural_neutrino.py
#   │  └─ structural_quark_mass.py
#   └─ tools/
#      └─ particle_mass_map.py
#
# The renderer contains no physical prediction constants.
# All displayed physics values are computed from core.
# ============================================================

def _find_repo_root() -> Path:
    """Find a directory containing core/structural_constants.py."""
    here = Path(__file__).resolve().parent

    candidates = [
        here,          # script placed at repository root
        here.parent,   # script placed in tools/
    ]

    for root in candidates:
        if (root / "core" / "structural_constants.py").exists():
            return root

    raise RuntimeError(
        "Could not locate repository core/. "
        "Place this script in the repository root or in tools/."
    )


REPO_ROOT = _find_repo_root()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from core.structural_constants import STRUCTURAL_CONSTANTS
from core.structural_electron import (
    compute_psi_values,
    compute_theory,
    fraction_to_decimal as electron_fraction_to_decimal,
)
from core.structural_gravity import compute_gravity
from core.structural_higgs_electroweak import compute_higgs_electroweak_values
from core.structural_neutrino import compute_neutrino_masses
from core.structural_quark_mass import compute_quark_masses


def compute_map_values() -> dict[str, Decimal]:
    """
    Compute every physical number used by the mass map from core.

    The plotting / image-processing layer does not define alternative
    physics formulas or fallback numerical values.
    """
    constants = STRUCTURAL_CONSTANTS

    # Electron / charged-particle sector
    psi = compute_psi_values(constants)
    electron = compute_theory(constants, psi)

    # structural_electron.electron_mass_scale is in eV.
    me_ev = electron_fraction_to_decimal(electron.electron_mass_scale)
    me_mev = me_ev / Decimal("1e6")

    proton_gev = electron.proton_ratio * me_mev / Decimal("1000")
    neutron_gev = electron.neutron_ratio * me_mev / Decimal("1000")
    muon_mev = electron.muon_ratio * me_mev
    tau_gev = electron.tau_from_e_ratio * me_mev / Decimal("1000")

    # Quark sector
    quark_result = compute_quark_masses(constants)
    quark_mev = {row.symbol: row.mass_mev for row in quark_result.rows}

    # Neutrino sector
    neutrino = compute_neutrino_masses(constants)

    # Higgs / electroweak sector
    ew = compute_higgs_electroweak_values(constants)

    # Gravity sector
    gravity = compute_gravity(constants, psi)

    return {
        # quarks
        "u_mev": quark_mev["u"],
        "d_mev": quark_mev["d"],
        "c_gev": quark_mev["c"] / Decimal("1000"),
        "s_mev": quark_mev["s"],
        "t_gev": quark_mev["t"] / Decimal("1000"),
        "b_gev": quark_mev["b"] / Decimal("1000"),

        # charged leptons / hadrons
        "e_mev": me_mev,
        "mu_mev": muon_mev,
        "tau_gev": tau_gev,
        "p_gev": proton_gev,
        "n_gev": neutron_gev,

        # neutrinos
        "nu1_ev": neutrino.m1_ev,
        "nu2_ev": neutrino.m2_ev,
        "nu3_ev": neutrino.m3_ev,

        # bosons / electroweak
        "W_gev": ew.mW_gev,
        "Z_gev": ew.mZ_gev,
        "H_gev": ew.mH_gev,
        "vev_gev": ew.v_gev,
        "electron_yukawa": ew.electron_yukawa,
        "sin2_theta_w": ew.sin2_theta_w,

        # fundamental / gravity
        "alpha_inv": electron.alpha_inv,
        "me_c2_mev": me_mev,
        "G": gravity.g_value,
        "planck_mass_kg": gravity.planck_mass,
    }


_SUPERSCRIPT = str.maketrans("-+0123456789", "⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹")


def format_sci_unicode(value: Decimal, mantissa_places: int = 12) -> str:
    """Format Decimal as 'a.b × 10⁻ⁿ' for the information boxes."""
    value = Decimal(value)
    if value == 0:
        return "0"

    s = f"{value:.{mantissa_places}E}"
    mantissa, exponent = s.split("E")
    exponent_i = int(exponent)
    return f"{mantissa} × 10{str(exponent_i).translate(_SUPERSCRIPT)}"


BASE_W = 1536
BASE_H = 1024

# High-resolution render multiplier.
# 1 = 1536x1024
# 2 = 3072x2048
# 4 = 6144x4096
RENDER_SCALE = 2

PX_W = BASE_W * RENDER_SCALE
PX_H = BASE_H * RENDER_SCALE

BASE_DPI = 100
DPI = BASE_DPI * RENDER_SCALE


# ============================================================
# USER'S MICRO-ADJUSTED PIXEL-ALIGNED BACKGROUND
# ============================================================

def render_background(output_path: Path, values: dict[str, Decimal]) -> None:

    # ============================================================
    # PARTICLE MASS MAP — pixel-aligned reference layout
    #
    # Canvas: 1536 x 1024
    #
    # Horizontal layout is expressed directly in reference-image
    # pixel coordinates.  This avoids cumulative drift from a
    # generic normalized slot model.
    #
    # Each 3-particle group follows:
    #
    #   3 * (BAR_W + BAR_TO_CHAR_GAP + CHAR_W + SLOT_TAIL)
    #   + GROUP_GAP
    #
    # Final output has NO CHAR frames.
    # ============================================================

    W, H = 1536, 1024

    # ------------------------------------------------------------
    # Figure / pixel helpers
    # ------------------------------------------------------------
    fig = plt.figure(figsize=(W/BASE_DPI, H/BASE_DPI), dpi=DPI, facecolor="black")

    def px_x(x):
        return x / W

    def px_y_from_top(y):
        return 1.0 - y / H

    def add_axes_px(left, top, right, bottom):
        """Axes rectangle specified in pixels from top-left."""
        return fig.add_axes([
            left / W,
            (H - bottom) / H,
            (right - left) / W,
            (bottom - top) / H
        ])

    # ------------------------------------------------------------
    # Plot rectangles measured from the supplied reference
    # ------------------------------------------------------------
    PLOT_LEFT  = 180
    PLOT_RIGHT = 1500

    ax_gev = add_axes_px(PLOT_LEFT, 148, PLOT_RIGHT, 356)
    ax_mev = add_axes_px(PLOT_LEFT, 449, PLOT_RIGHT, 650)
    ax_ev  = add_axes_px(PLOT_LEFT, 744, PLOT_RIGHT, 931)

    axes = (ax_gev, ax_mev, ax_ev)

    # Pixel-like x coordinates inside each axes.
    for ax in axes:
        ax.set_xlim(PLOT_LEFT, PLOT_RIGHT)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_linewidth(1.4)
        ax.spines["bottom"].set_color("#d8d8d8")
        ax.set_facecolor("black")
        ax.tick_params(axis="x", length=0)
        ax.tick_params(axis="y", length=0, labelsize=10, pad=8, colors="#e8e8e8")
        ax.grid(axis="y", color="#404040", linewidth=0.7)
        ax.set_axisbelow(True)
        ax.set_xticks([])

    # ------------------------------------------------------------
    # Unit scales — same linear bar heights as reference
    # ------------------------------------------------------------
    ax_gev.set_ylim(-2, 210)
    ax_gev.set_yticks([0, 50, 100, 150, 200])

    ax_mev.set_ylim(-1.3, 130)
    ax_mev.set_yticks([0, 20, 40, 60, 80, 100, 120])

    ax_ev.set_ylim(-0.0007, 0.07)
    ax_ev.set_yticks([0, 0.02, 0.04, 0.06])
    ax_ev.set_yticklabels(["0", "0.02", "0.04", "0.06"])

    # ------------------------------------------------------------
    # Horizontal slot model
    #
    # Reference-scale measurements:
    # bar ~20 px
    # reserved character zone ~70 px
    # slot pitch ~150/170 px depending on band in original.
    #
    # We deliberately reserve room to the RIGHT of every bar.
    # ------------------------------------------------------------
    # ------------------------------------------------------------
    # Equal-width group geometry
    #
    # Intended rule:
    #   GROUP_W = (BAR_W + CHAR_W) * 3
    #   next group begins after GROUP_GAP
    #
    # Proportions are inherited from the original background model:
    #   BAR_W : CHAR_W : GROUP_GAP = 0.18 : 0.72 : 0.34
    # ------------------------------------------------------------
    MODEL_BAR_W     = 0.18
    MODEL_CHAR_W    = 0.72
    MODEL_SLOT_W    = MODEL_BAR_W + MODEL_CHAR_W   # 0.90
    MODEL_GROUP_GAP = 0.34

    # Original model also had 0.30 left padding and 0.25 right padding.
    MODEL_LEFT_PAD  = 0.30
    MODEL_RIGHT_PAD = 0.25
    MODEL_XMAX = (
        MODEL_LEFT_PAD
        + 3 * MODEL_SLOT_W
        + MODEL_GROUP_GAP
        + 3 * MODEL_SLOT_W
        + MODEL_GROUP_GAP
        + 3 * MODEL_SLOT_W
        + MODEL_RIGHT_PAD
    )

    MODEL_TO_PX = (PLOT_RIGHT - PLOT_LEFT) / MODEL_XMAX

    BAR_W = MODEL_BAR_W * MODEL_TO_PX
    CHAR_W = MODEL_CHAR_W * MODEL_TO_PX
    SLOT_W = BAR_W + CHAR_W
    GROUP_GAP = MODEL_GROUP_GAP * MODEL_TO_PX
    LEFT_PAD = MODEL_LEFT_PAD * MODEL_TO_PX

    QUARK_X0 = PLOT_LEFT + LEFT_PAD
    LEPTON_X0 = QUARK_X0 + 3 * SLOT_W + GROUP_GAP
    BOSON_X0 = LEPTON_X0 + 3 * SLOT_W + GROUP_GAP

    def bar_left(group_x0, i):
        return group_x0 + i * SLOT_W

    def char_region(group_x0, i):
        bx = bar_left(group_x0, i)
        return bx + BAR_W, bx + SLOT_W

    # Separators sit in the middle of each inter-group gap.
    SEP_Q_L = QUARK_X0 + 3 * SLOT_W + GROUP_GAP / 2
    SEP_L_B = LEPTON_X0 + 3 * SLOT_W + GROUP_GAP / 2

    # Category separators are drawn once as continuous figure-level lines below.

    # ------------------------------------------------------------
    # Colors
    # ------------------------------------------------------------
    RED, RED_D = "#ff6666", "#c83f3f"
    BLUE, BLUE_D = "#72a7ff", "#72a7ff"
    GREEN, GREEN_D = "#61b578", "#2f8749"
    PURPLE, PURPLE_D = "#b49cff", "#b49cff"
    YELLOW, YELLOW_D = "#f2c94c", "#b58d13"
    HADRON, HADRON_D = "#ffb454", "#ffb454"

    # ------------------------------------------------------------
    # Explicit x positions — measured from supplied image
    #
    # This is intentional: the reference itself does NOT use one
    # single uniform pitch for all occupied rows.
    # ------------------------------------------------------------
    gev = [
        ("c", values["c_gev"], bar_left(QUARK_X0, 0), RED, RED_D, RED_D),
        ("b", values["b_gev"], bar_left(QUARK_X0, 1), BLUE, BLUE_D, BLUE_D),
        ("t", values["t_gev"], bar_left(QUARK_X0, 2) - 14, RED, RED_D, RED_D),

        # LEPTONS / HADRONS: p | n | τ
        ("p", values["p_gev"],   bar_left(LEPTON_X0, 0), HADRON, HADRON_D, HADRON_D),
        ("n", values["n_gev"],   bar_left(LEPTON_X0, 1), HADRON, HADRON_D, HADRON_D),
        ("τ", values["tau_gev"], bar_left(LEPTON_X0, 2), GREEN, GREEN_D, GREEN_D),

        ("W±", values["W_gev"], bar_left(BOSON_X0, 0), PURPLE, PURPLE_D, PURPLE_D),
        ("Z⁰", values["Z_gev"], bar_left(BOSON_X0, 1), PURPLE, PURPLE_D, PURPLE_D),
        ("H",  values["H_gev"], bar_left(BOSON_X0, 2), PURPLE, PURPLE_D, PURPLE_D),
    ]

    mev = [
        ("u", values["u_mev"],  bar_left(QUARK_X0, 0), RED, RED_D, RED_D),
        ("d", values["d_mev"],  bar_left(QUARK_X0, 1), BLUE, BLUE_D, BLUE_D),
        ("s", values["s_mev"],  bar_left(QUARK_X0, 2), BLUE, BLUE_D, BLUE_D),

        ("e", values["e_mev"],  bar_left(LEPTON_X0, 0), GREEN, GREEN_D, GREEN_D),
        ("μ", values["mu_mev"], bar_left(LEPTON_X0, 1), GREEN, GREEN_D, GREEN_D),
    ]

    ev = [
        ("ν₁", values["nu1_ev"], bar_left(LEPTON_X0, 0), YELLOW, YELLOW_D, GREEN_D),
        ("ν₂", values["nu2_ev"], bar_left(LEPTON_X0, 1), YELLOW, YELLOW_D, GREEN_D),
        ("ν₃", values["nu3_ev"], bar_left(LEPTON_X0, 2), YELLOW, YELLOW_D, GREEN_D),
    ]

    # ------------------------------------------------------------
    # Draw bars + text
    # ------------------------------------------------------------
    def value_text(value):
        value = float(value)
        if value >= 100:
            return f"{value:.3f}"
        if value >= 10:
            return f"{value:.4f}".rstrip("0").rstrip(".")
        if value >= 1:
            return f"{value:.5f}".rstrip("0").rstrip(".")
        return f"{value:.6f}"

    def draw_rows(ax, rows, number_offset, label_offset):
        for name, value, x, face, edge, label_color in rows:
            ax.bar(
                x, value,
                width=BAR_W,
                align="edge",
                color=face,
                edgecolor=edge,
                linewidth=1.0,
                zorder=3
            )

            ax.text(
                x + BAR_W/2,
                float(value) + number_offset,
                value_text(value),
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
                color="#f3f3f3"
            )

            ax.text(
                x + BAR_W/2,
                label_offset,
                name,
                ha="center",
                va="top",
                fontsize=12,
                fontweight="bold",
                color=label_color,
                clip_on=False
            )

    draw_rows(ax_gev, gev, 4.5, -12)
    draw_rows(ax_mev, mev, 3.0, -8)
    draw_rows(ax_ev,  ev, 0.0045, -0.0045)

    # ------------------------------------------------------------
    # Title / category headers / unit boxes
    # ------------------------------------------------------------
    overlay = fig.add_axes([0, 0, 1, 1], frameon=False)
    overlay.set_xlim(0, W)
    overlay.set_ylim(H, 0)  # pixel coordinates, origin top-left
    overlay.axis("off")

    # Continuous category separators measured from the reference.
    # They run through the gaps between GeV / MeV / eV bands.
    overlay.plot([SEP_Q_L, SEP_Q_L], [111, 956], color="#5f5f5f", linewidth=1.0, zorder=0)
    overlay.plot([SEP_L_B, SEP_L_B], [111, 956], color="#5f5f5f", linewidth=1.0, zorder=0)

    overlay.text(
        46, 49,
        "PARTICLE MASS MAP — exact linear bars + reserved character space",
        fontsize=18,
        fontweight="bold",
        color="#f5f5f5"
    )

    def rounded_header(x0, y0, x1, y1, title, color):
        patch = FancyBboxPatch(
            (x0, y0),
            x1-x0,
            y1-y0,
            boxstyle="round,pad=0.0,rounding_size=10",
            facecolor="black",
            edgecolor=color,
            linewidth=1.3
        )
        overlay.add_patch(patch)
        overlay.text(
            (x0+x1)/2,
            (y0+y1)/2 + 1,
            title,
            ha="center",
            va="center",
            fontsize=15,
            fontweight="bold",
            color=color
        )
    # Headers follow the exact same group geometry as the graph contents.
    GROUP_W = 3 * SLOT_W
    HEADER_INSET = 8
    rounded_header(QUARK_X0  + HEADER_INSET, 65,
                   QUARK_X0  + GROUP_W - HEADER_INSET, 106, "QUARKS", RED_D)
    rounded_header(LEPTON_X0 + HEADER_INSET, 65,
                   LEPTON_X0 + GROUP_W - HEADER_INSET, 106, "LEPTONS / HADRONS", GREEN_D)
    rounded_header(BOSON_X0  + HEADER_INSET, 65,
                   BOSON_X0  + GROUP_W - HEADER_INSET, 106, "BOSONS", PURPLE_D)
    rounded_header(LEPTON_X0 + HEADER_INSET, 695,
                   LEPTON_X0 + GROUP_W - HEADER_INSET, 736, "NEUTRINO", YELLOW_D)

    def unit_box(x0, y0, x1, y1, unit, subtitle, color):
        patch = FancyBboxPatch(
            (x0, y0),
            x1-x0,
            y1-y0,
            boxstyle="round,pad=0.0,rounding_size=10",
            facecolor="black",
            edgecolor=color,
            linewidth=1.2
        )
        overlay.add_patch(patch)

        overlay.text(
            (x0+x1)/2,
            y0+28,
            subtitle,
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=color
        )

        overlay.text(
            (x0+x1)/2,
            (y0+y1)/2,
            unit,
            ha="center",
            va="center",
            fontsize=21,
            fontweight="bold",
            color=color
        )

    unit_box(20, 120, 130, 390, "GeV", "linear GeV", "#5f9cff")
    unit_box(20, 416, 130, 686, "MeV", "linear MeV", "#2c8649")
    unit_box(20, 711, 130, 966, "eV",  "linear eV",  "#cc3e43")

    # ------------------------------------------------------------
    # Optional debug-only character boxes.
    # Final output must remain False.
    # ------------------------------------------------------------
    SHOW_RESERVED_CHARACTER_AREAS = False

    if SHOW_RESERVED_CHARACTER_AREAS:
        # Quark / lepton / boson 3-slot reference regions.
        debug_groups = [
            (220, [0, 1, 2]),
            (820, [0, 1, 2]),
            (1120, [0, 1, 2]),
        ]

        for gx, indices in debug_groups:
            for i in indices:
                left, right = char_region(gx, i)
                overlay.add_patch(Rectangle(
                    (left, 182),
                    right-left,
                    168,
                    fill=False,
                    linestyle="--",
                    linewidth=0.8,
                    edgecolor="#aaaaaa"
                ))

    # ------------------------------------------------------------
    # Footer
    # ------------------------------------------------------------
    overlay.text(
        W/2,
        997,
        "Bars are mathematically scaled within each unit band. "
        "Character space is reserved to the right of each bar.",
        ha="center",
        va="center",
        fontsize=10.5,
        color="#a8a8a8"
    )


    # The uploaded background script intentionally stops before save here
    # because this merged renderer owns the output path.
    plt.savefig(
        output_path,
        dpi=DPI,
        facecolor="black",
        bbox_inches=None,
        pad_inches=0,
    )
    plt.close(fig)


# ============================================================
# CHARACTER EXTRACTION / CLEANUP
# ============================================================

# Coordinates in the original 1536x1024 character sheet.
CHAR_CROPS = {
    "u":   (5,    85,  190,  350),
    "d":   (190,  75,  390,  350),
    "c":   (390,  55,  635,  350),
    "s":   (640,  25,  970,  360),
    "t":   (980,   5, 1270,  360),
    "b":   (1270, 40, 1535,  350),

    "e":   (5,   365,  205,  635),
    "mu":  (205, 360,  410,  635),
    "tau": (410, 360,  650,  645),
    "nu1": (670, 365,  915,  650),
    "nu2": (910, 365, 1165,  660),
    "nu3": (1180,345, 1535,  660),

    "H":   (5,   640,  345, 990),
    "W":   (345, 650,  665, 985),
    "Z":   (655, 640, 1000, 990),
    "p":   (995, 660, 1290, 995),
    "n":   (1280,660, 1535, 985),
}


def clean_character(sheet: Image.Image, box) -> Image.Image:
    """
    Black-background edition.

    IMPORTANT:
    - Do NOT make black pixels transparent.
    - Preserve eyebrows, outlines, pupils, hair details, etc.
    - Only crop the manually defined rectangle from the original
      black-background character sheet.

    Because the final canvas is also black, the crop background blends
    naturally into the chart background without alpha-keying artifacts.
    """
    return sheet.crop(box).convert("RGBA")


# ============================================================
# FINAL CHARACTER PLACEMENT
# ============================================================

# Vertical ranges from V5. Character scale is preserved independently of x-position.
Y_TARGETS = {
    "c":   (117, 352), "b":   (112, 352), "t":   (82, 352),
    "p":   (122, 352), "n":   (122, 352), "tau": (137, 352),
    "W":   (117, 352), "Z":   (107, 352), "H":   (102, 352),

    "u":   (446, 646), "d":   (436, 646), "s":   (401, 646),
    "e":   (481, 646), "mu":  (426, 646),

    "nu1": (772, 927), "nu2": (772, 927), "nu3": (717, 927),
}

# Original V5 target-box widths. These are used ONLY for scaling,
# so moving bars/groups cannot accidentally resize the characters.
CHAR_SCALE_BOX_W = {
    "c":   85, "b":  105, "t":   144,
    "p":  105, "n":  105, "tau":  95,
    "W":  105, "Z":  115, "H":   120,
    "u":   90, "d":  105, "s":   155,
    "e":   75, "mu": 165,
    "nu1": 90, "nu2": 90, "nu3": 130,
}

# Character centers are tied to the center of the reserved area to the RIGHT of each bar.
# Small dx values preserve the hand-tuned appearance without changing scale.
CHAR_ANCHOR = {
    "c": ("Q", 0), "b": ("Q", 1), "t": ("Q", 2),
    "u": ("Q", 0), "d": ("Q", 1), "s": ("Q", 2),

    "p": ("L", 0), "n": ("L", 1), "tau": ("L", 2),
    "e": ("L", 0), "mu": ("L", 1),
    "nu1": ("L", 0), "nu2": ("L", 1), "nu3": ("L", 2),

    "W": ("B", 0), "Z": ("B", 1), "H": ("B", 2),
}

CHAR_DX = {
    "c": -20, "b": -10, "t":   0,
    "u": -20, "d": -20, "s":   0,

    "p":   0, "n":   0, "tau": 0,
    "e":   0, "mu":  8,
    "nu1": 0, "nu2": 0, "nu3": 0,

    "W":   5, "Z":   0, "H":   7,
}

# Finalized nominal character widths (pixels) from the hand-tuned 2026 composition.
# Used only for scale reproduction; horizontal position remains bar-anchored.
CHAR_NOMINAL_WIDTH = {
    "c":   85, "b":  105, "t":   144,
    "p":  105, "n":  105, "tau":  95,
    "W":  105, "Z":  115, "H":   140,
    "u":   90, "d":  105, "s":   155,
    "e":   75, "mu": 165,
    "nu1": 90, "nu2": 90, "nu3": 130,
}

# Final relative scales.
# u/d are deliberately smaller; ν3 is deliberately larger than ν1/ν2.
SCALE_FACTORS = {
    "u":   0.84,
    "d":   0.84,
    "c":   0.80,
    "b":   0.80,

    "t":   1.10,
    "s":   1.00,

    "p":   0.60,
    "n":   0.55,
    "tau": 0.80,

    "e":   0.72,
    "mu":  0.80,

    "nu1": 0.82,
    "nu2": 0.90,
    "nu3": 1.20,

    "W":   1.05,
    "Z":   1.10,
    "H":   1.20,
}


def overlay_characters(
    background: Image.Image,
    character_sheet: Image.Image,
) -> Image.Image:
    canvas = background.convert("RGBA")

    sprites = {
        name: clean_character(character_sheet, crop)
        for name, crop in CHAR_CROPS.items()
    }

    # Mirror the exact horizontal formula used by render_background().
    plot_left       = 180
    plot_right      = 1500
    model_bar_w     = 0.18
    model_char_w    = 0.72
    model_slot_w    = model_bar_w + model_char_w
    model_group_gap = 0.34
    model_left_pad  = 0.30
    model_right_pad = 0.25
    model_xmax = (
        model_left_pad
        + 3 * model_slot_w + model_group_gap
        + 3 * model_slot_w + model_group_gap
        + 3 * model_slot_w
        + model_right_pad
    )
    k = (plot_right - plot_left) / model_xmax

    bar_w = model_bar_w * k
    char_w = model_char_w * k
    slot_w = bar_w + char_w
    group_gap = model_group_gap * k
    left_pad = model_left_pad * k

    group_x = {
        "Q": plot_left + left_pad,
    }
    group_x["L"] = group_x["Q"] + 3 * slot_w + group_gap
    group_x["B"] = group_x["L"] + 3 * slot_w + group_gap

    for name, (y0, y1) in Y_TARGETS.items():
        sprite = sprites[name]
        group_key, idx = CHAR_ANCHOR[name]

        bar_left_px = group_x[group_key] + idx * slot_w
        char_left_px = bar_left_px + bar_w
        char_right_px = bar_left_px + slot_w
        center_x = (char_left_px + char_right_px) / 2 + CHAR_DX[name]

        # IMPORTANT: scaling is based on the preserved V5 box width,
        # not on the newly computed slot width.
        target_w = CHAR_SCALE_BOX_W[name]
        target_h = y1 - y0
        factor = SCALE_FACTORS[name]

        # Scale logical placement geometry to the high-resolution canvas.
        target_w_px = target_w * RENDER_SCALE
        target_h_px = target_h * RENDER_SCALE

        scale = min(
            target_w_px * 0.97 * factor / sprite.width,
            target_h_px * 0.97 * factor / sprite.height,
        )

        new_w = max(1, round(sprite.width * scale))
        new_h = max(1, round(sprite.height * scale))
        sprite = sprite.resize((new_w, new_h), Image.Resampling.LANCZOS)

        px = round(center_x * RENDER_SCALE - new_w / 2)
        py = round(y1 * RENDER_SCALE - new_h)
        canvas.alpha_composite(sprite, (px, py))

    return canvas


# ============================================================
# ZERO-PARAMETER INFORMATION BOXES
# ============================================================

def find_font(bold=False):
    """
    Robust Unicode font lookup.

    Use Matplotlib's bundled DejaVu Sans rather than relying on
    OS-specific /usr/share/fonts paths. This preserves Greek letters,
    superscripts/subscripts, multiplication signs, etc. on Windows,
    macOS, Linux, Colab, and most Python environments.
    """
    family = "DejaVu Sans"
    weight = "bold" if bold else "normal"

    prop = font_manager.FontProperties(
        family=family,
        weight=weight,
    )
    path = font_manager.findfont(
        prop,
        fallback_to_default=True,
    )

    if not path or not Path(path).exists():
        raise RuntimeError(
            "Could not locate a Unicode-capable DejaVu Sans font "
            "through Matplotlib."
        )

    return path


def load_font(size: int, bold=False):
    return ImageFont.truetype(find_font(bold=bold), size)


def draw_information_boxes(image: Image.Image, values: dict[str, Decimal]) -> Image.Image:
    """
    Draw structural-value boxes using logical 1536x1024 coordinates,
    scaling all Pillow geometry by RENDER_SCALE.
    """
    img = image.convert("RGB")
    d = ImageDraw.Draw(img)

    def S(v):
        return int(round(v * RENDER_SCALE))

    title_font = load_font(S(17), bold=True)
    body_font = load_font(S(15), bold=False)
    body_bold = load_font(S(15), bold=True)
    small_font = load_font(S(12), bold=False)

    def draw_box(
        rect,
        heading,
        rows,
        outline,
        fill,
        value_x_offset=125,
        gap=29,
    ):
        x0, y0, x1, y1 = [S(v) for v in rect]

        d.rounded_rectangle(
            (x0, y0, x1, y1),
            radius=S(14),
            fill=fill,
            outline=outline,
            width=S(2),
        )

        d.text(
            ((x0 + x1) // 2, y0 + S(14)),
            heading,
            font=title_font,
            fill=(242, 242, 242),
            anchor="ma",
        )

        d.line(
            (x0 + S(18), y0 + S(42), x1 - S(18), y0 + S(42)),
            fill=outline,
            width=S(1),
        )

        y = y0 + S(56)

        for label, value in rows:
            d.text(
                (x0 + S(20), y),
                label,
                font=body_bold,
                fill=outline,
                anchor="la",
            )
            d.text(
                (x0 + S(value_x_offset), y),
                value,
                font=body_font,
                fill=(242, 242, 242),
                anchor="la",
            )
            y += S(gap)

    draw_box(
        (1085, 455, 1490, 640),
        "ZERO-PARAMETER VALUES",
        [
            ("α⁻¹",  f'{values["alpha_inv"]:.12f}'),
            ("mₑc²", f'{values["me_c2_mev"]:.15f} MeV'),
            ("G",    format_sci_unicode(values["G"], 12)),
            ("Mₚₗ",  f'{format_sci_unicode(values["planck_mass_kg"], 12)} kg'),
        ],
        outline=(95, 150, 255),
        fill=(10, 14, 22),
        value_x_offset=125,
        gap=29,
    )

    draw_box(
        (1085, 735, 1490, 880),
        "ELECTROWEAK SCALE",
        [
            ("VEV",     f'{values["vev_gev"]:.6f} GeV'),
            ("yₑ",      format_sci_unicode(values["electron_yukawa"], 10)),
            ("sin²θW",  f'{values["sin2_theta_w"]:.9f}'),
        ],
        outline=(188, 140, 255),
        fill=(16, 10, 22),
        value_x_offset=125,
        gap=27,
    )

    d.text(
        (S(1288), S(897)),
        "Zero-parameter structural values",
        font=small_font,
        fill=(170, 170, 170),
        anchor="ma",
    )

    return img



def draw_final_title(image: Image.Image) -> Image.Image:
    """Draw the finalized title/subtitle/2026 badge at any RENDER_SCALE."""
    img = image.convert("RGB")
    d = ImageDraw.Draw(img)

    def S(v):
        return int(round(v * RENDER_SCALE))

    d.rectangle((0, 0, S(1536), S(62)), fill=(0, 0, 0))

    title_font = load_font(S(27), bold=True)
    subtitle_font = load_font(S(12), bold=False)
    badge_font = load_font(S(12), bold=True)

    d.text(
        (S(768), S(15)),
        "ZERO-PARAMETER PARTICLE MASS & SCALE MAP",
        font=title_font,
        fill=(245, 245, 245),
        anchor="ma",
    )
    d.text(
        (S(768), S(48)),
        "Particle Masses · Fundamental Constants · Electroweak & Gravity Scales",
        font=subtitle_font,
        fill=(175, 175, 175),
        anchor="ma",
    )

    badge_text = "2026 EDITION"
    bbox = d.textbbox((0, 0), badge_text, font=badge_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    pad_x = S(9)
    pad_y = S(5)
    x1 = S(1510)
    y0 = S(12)
    x0 = x1 - (tw + 2 * pad_x)
    y1 = y0 + th + 2 * pad_y

    d.rounded_rectangle(
        (x0, y0, x1, y1),
        radius=S(8),
        fill=(18, 22, 28),
        outline=(120, 130, 145),
        width=S(1),
    )
    d.text(
        ((x0 + x1) // 2, (y0 + y1) // 2),
        badge_text,
        font=badge_font,
        fill=(235, 235, 235),
        anchor="mm",
    )

    return img


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Render the merged 2026 zero-parameter particle mass & scale map."
    )
    parser.add_argument(
        "--characters",
        default="character_sheet.png",
        help="Original 1536x1024 character sheet with black background.",
    )
    parser.add_argument(
        "--output",
        default="zero_parameter_particle_mass_scale_map_2026.png",
        help="Final PNG output path.",
    )
    parser.add_argument(
        "--keep-background",
        action="store_true",
        help="Keep the intermediate background-only PNG.",
    )
    args = parser.parse_args()

    character_path = Path(args.characters)
    output_path = Path(args.output)

    if not character_path.exists():
        raise FileNotFoundError(character_path)

    background_path = output_path.with_name(output_path.stem + "_background.png")

    values = compute_map_values()

    render_background(background_path, values)

    background = Image.open(background_path).convert("RGBA")
    character_sheet = Image.open(character_path).convert("RGBA")

    if background.size != (PX_W, PX_H):
        raise ValueError(f"Unexpected background size: {background.size}")
    if character_sheet.size != (1536, 1024):
        raise ValueError(
            "Finalized character crops expect a 1536x1024 sheet; "
            f"received {character_sheet.size}"
        )

    result = overlay_characters(background, character_sheet)
    result = draw_information_boxes(result, values)
    result = draw_final_title(result)
    result.save(output_path, format="PNG", optimize=False)

    if not args.keep_background:
        background_path.unlink(missing_ok=True)

    print(f"Saved: {output_path.resolve()}")
    print(f"Size : {result.size[0]} x {result.size[1]}")
    print(f"Render scale: {RENDER_SCALE}x")
    print("Physics values: computed from repository core/")


if __name__ == "__main__":
    main()
