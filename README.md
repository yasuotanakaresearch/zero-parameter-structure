# Zero Parameter Structure

No free parameters. No tuning. Only structure.

---

## Can this really be computed from just a few lines?

```python
R = 13.0 / 6.0

Omega_b = 1 / (3 * R**2 + 3 * R)
Omega_m = 3 * R * Omega_b
Omega_L = 3 * R**2 * Omega_b
Omega_dm = Omega_m - Omega_b

print(Omega_L, Omega_m, Omega_dm, Omega_b)
```

```
0.68421 0.31579 0.26721 0.04858
```

No fitting.
No free parameters.
Only structure.

---

## Overview

This repository presents a minimal structural framework in which key physical quantities
emerge from fixed ratios rather than parameter fitting.

The framework is based on two constants:

- R = 13/6
- Z = 31/24

---

## Key Principle

Physical laws are not adjusted to data —
they are reconstructed from structure.

- No adjustable parameters
- No data fitting
- Fully reproducible relations

---

## Current Scope (Public)

- Cosmological density relations
- Reconstruction of ΩΛ, Ωm, Ωb
- Structural consistency checks

Example:

Ωm² = 3 ΩΛ Ωb

---

## Extended Scope (Preview)

Additional structural relations are under active development:

- Electromagnetic coupling structure
- Mass hierarchy (lepton sector)
- Gravity sector *(restricted release)*

Some results are intentionally not fully exposed
until independent verification is complete.

---

## Repository Structure

```
zero-parameter-structure/
├── core/
├── code/
├── observed_data/
└── README.md
```

---

## Papers

### Paper 1 — Cosmology

Structural Origin of Cosmological Density Ratios

- https://doi.org/10.5281/zenodo.19351666

Corresponding code:
```
python -m code.paper1_cosmology
```

---

### Paper 2 — Electroweak (in preparation)

Structural Origin of Electromagnetic Coupling and Mass Hierarchy

- https://doi.org/10.5281/zenodo.19426367

Corresponding code:
```
python -m code.paper2_electroweak
```

---

### Paper 3 — Gravity (restricted / under validation)

Structural Origin of Gravity

This sector is currently under validation.
Code and full implementation are not yet publicly released.

---

## Reproducibility

All public results can be reproduced with simple Python scripts.

No external fitting or optimization is required.

---

## Philosophy

- Structure first
- Ratios over parameters
- Direct comparison with observation

---

## Status

Work in progress.
Released incrementally alongside the paper series.

---

## License

MIT License
