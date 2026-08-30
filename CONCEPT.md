# Research Concept

## Purpose

This project explores whether physical quantities from different domains
can be organized by a small set of fixed dimensionless ratios and common
structural relations.

The central aim is to examine whether dimensionless constants, mass
ratios, density ratios, and physical scales can be assigned a common
structural meaning through the same fixed inputs and generating rules.

## Core Idea

The foundational layer begins with a minimal causal-inheritance update
identity rather than with observed physical quantities or fitted
parameters.

Using the discrete unit shift

```math
A^\sharp:=A+1,
\qquad
A^\flat:=A-1,
```

the minimal nontrivial inheritance condition selects

```math
q=2,
\qquad
q^\sharp=q+1=3.
```

The derived pair generates

```math
X(n,s)=q^\sharp q^n+s,
\qquad
X(n):=X(n,0),
\qquad
Y(n)=q^{n+1}-1.
```

The normalized product map is

```math
P(n)=\frac{X(n)Y(n)}{q^\sharp},
```

with the distinguished values

```math
\bigl(P(1),P(q),P(q^2)\bigr)=(6,28,496).
```

The fixed structural ratios used by the sector-specific relations are
then extracted directly from the generated \(X/Y\) hierarchy:

```math
R
=
\frac{X(q)^\sharp}{X(1)}
=
\frac{13}{6},
\qquad
S
=
\frac{Y(q^2)}{X(q^\sharp)}
=
\frac{31}{24}.
```

Equivalently,

```math
\frac{q}{S}
=
\frac{X(q^2)}{Y(q^2)}
=
\frac{48}{31}.
```

The product-map expressions for \(R\), \(S\), and \(R-S\) are retained as
exact equivalent closure relations, not as the primary definitions of
the structural ratios.

The same \(R\)- and \(S\)-branches are then carried unchanged into
sector-specific relations in cosmology, particle masses,
electromagnetic coupling, gravity-sector quantities, and related
physical scales.

## Core Principles

### 1. Fixed inputs rather than fitting parameters

The relations presented in this project use fixed structural inputs
instead of observable-by-observable adjustable parameters.

The same ratios are used across multiple calculations, and the resulting
values are compared directly with observational or experimental reference
values.

### 2. Structural interpretation of dimensionless quantities

Dimensionless constants and ratios are treated not only as measured
numerical values, but also as possible expressions of an underlying
common structure.

The central question is whether several apparently independent
quantities can be related through the same fixed branches and generating
rules.

### 3. Minimal-axiom origin of the structural branches

The foundational construction is formulated at a pre-observational
structural layer, denoted \(L1\).

At this level, the derivation does not assume spacetime dimension,
physical time, particles, masses, coupling constants, finite geometry,
group theory, string theory, or cosmological observables.

The logical direction is

```math
\text{causal inheritance}
\longrightarrow
(q,q^\sharp)
\longrightarrow
(X,Y),
```

with the downstream constructions

```math
(X,Y)\longrightarrow P,
\qquad
(X,Y)\longrightarrow(R,S).
```

Finite geometry may be used afterward as an independent mathematical
consistency check, but it is not a premise used to generate \(q\),
\(q^\sharp\), \(X\), \(Y\), \(P\), \(R\), or \(S\).

### 4. Relations across physical domains

The project examines structural relations across several categories,
including:

- cosmological density ratios
- electromagnetic coupling
- charged-particle mass hierarchy
- gravitational quantities
- quark and neutrino masses
- electroweak and strong-interaction scales
- cosmological and local kinematic scales

The importance of an individual relation is therefore not determined
only by its numerical accuracy.

A stronger test is whether the same fixed structure remains consistent
across different physical domains and hierarchical scales.

### 5. Direct comparison and falsifiability

Each relation produces a definite numerical value.

This allows direct comparison with observational or experimental data
without parameter optimization.

A relation may therefore be rejected if its numerical prediction is
inconsistent with reliable measurements, or if the common structural
form fails when applied across multiple domains.

### 6. Reproducibility

The project is designed so that the numerical relations can be reproduced
by simple scripts using the same fixed inputs.

The code accompanying each paper reports the structural constants,
structural coefficients, theoretical values, reference values, absolute
differences, relative differences, and sigma-level comparisons where
uncertainties are available.

### 7. Scope of interpretation

The relations in this repository are presented as structural
correspondences between fixed dimensionless ratios and observed reference
quantities.

They are evaluated by how far a small number of fixed branches and
generating rules can be carried across different sectors without
observable-specific fitting.

The foundational \(L1\) construction is kept logically separate from
later mathematical consistency checks and from sector-specific physical
interpretations.

Where multiple physical descriptions reproduce the same observable
relations, the project focuses on the common dimensionless or causal
structure shared by those descriptions.

## Research Position

The position of this project can be summarized as follows:

> Physical quantities from different domains are examined through fixed
> structural branches generated from a minimal causal-inheritance
> construction, with emphasis on reproducibility, cross-domain
> consistency, and direct comparison with reference values.

The intended style is cautious in interpretation, explicit in
assumptions, and strict in numerical comparison.
