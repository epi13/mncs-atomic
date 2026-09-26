# Atomic model and ownership boundary

## What "Atomic" means here

Classical atomic-scale particle simulation: atoms are point
masses carrying a species (LJ parameters + mass) and a distinct
identity, evolving in periodic boxes under pair potentials via
deterministic integrators. Concurrency atomics (CAS, memory
ordering) and quantum chemistry (wavefunctions, orbitals) are
explicitly NOT this repository — the README states both
exclusions first, and no code path suggests them.

## What Atomic owns

Particle-domain semantics, and only those:

- **Species** — `Species { mass, epsilon, sigma }` (SI),
  positivity validation as data, argon reference data with
  provenance, SI conversions, reduced-unit projections.
- **Identity** — particle ids (u64) with pairwise-distinctness
  invariants. Property equality never implies identity: two argon
  atoms share a `Species` value and remain distinct entities;
  duplicated ids are `Duplicated`/`BadInput` data.
- **Periodic state** — `Box`, minimum image (via consumed
  `fround`), wrapping (via consumed `ffloor`), squared distances.
- **Pair interaction** — LJ from r² (F/r + U), truncated cutoff
  with `Neglected` (legitimate) vs `BadInput` (singular/
  degenerate) kept distinct, Newton-III force projection.
- **Dynamics** — velocity-Verlet pair step, three-lane static
  accumulation, K/P/E bookkeeping, fixed-count drift-tracking
  drivers (32/256 steps).
- **Derived quantities** — kinetic temperature (explicit kB),
  drift-acceptance predicate.
- **Results** — `DimerStatic`/`DimerRun`/`Chain3` outcomes with
  provenance (t, steps, extrema, drift) and a single `BadInput`
  failure arm (no solver exists to fail distinctly).

## What Atomic does not own

- **Numeric** (`mncs-numerics`): rounding, `approx`, consumed
  verbatim. The r²-only LJ formulation deliberately avoids
  spending sqrt pressure.
- **Math** (`mncs-math`): no dependency yet; eigensolvers,
  complex numbers, and thermostat/ensemble algebra stay future
  pressures, not vendored code.
- **Geometry** (`mncs-geometry`): 1D lanes need no 2D
  primitives; 2D+ must consume Geometry.
- **FEM/Fluid**: untouched siblings; continuum and particle
  domains share no code and duplicate none.
- **Crypto/Data/Store/Lineage/Forge/Fabric/Test/Debug/Doctor**:
  consumed or interfaced per the README table; Atomic persists,
  schedules, hashes, and serializes nothing itself.

## Deliberately out of scope

Quantum chemistry, nuclear physics, molecular topology/bonds,
thermostats/barostats, neighbor/cell lists (all-pairs at this
scale; the irregular-list need is pressure P-ATOMIC-NEIGHBOR),
2D/3D, parallel/GPU execution, checkpoints/trajectories,
uncertainty propagation, private units systems.

## RFC scope classification (0001-foundation)

1. **Still-valid core** (implemented): explicit units/potentials/
   cutoffs/BCs; integrator timestep recorded with results; force/
   energy/conservation evidence before performance; classical MD
   only (quantum exclusion honored).
2. **Now owned elsewhere** (consumed): `fround`/`ffloor` rounding,
   `approx` discipline (Numerics); test execution (mncs-test).
3. **Redesigned for current strength**: neighbor-list semantics —
   RFC assumed lists up front; at N ≤ 3 all-pairs is exact and
   simpler, with rebuild policy deferred to a real N.
4. **Unnecessary scope** (cut): GPU/CUDA campaigns, large-N
   partitioning, async migration — correctly untouched until a
   verified dynamics exists whose contract they must preserve.
5. **Blocked, valuable** (pressures): irregular neighbor lists
   (P-ATOMIC-NEIGHBOR), dimensional analysis (P-ATOMIC-UNITS),
   many-body/thermostat algebra (P-ATOMIC-MATH).

## Historical note

The repository bootstrapped with architecture docs only (no host
MD code, no prior consumers). There was no legacy implementation
to port or remove: the foundation below is the first and only
canonical implementation, built directly against the current
language and the modernized Numeric/Test libraries.
