# RFC 0001: Molecular/particle simulation foundation

Status: Partially implemented (foundation slice, 2026-09-26).
Superseded statements are marked below; the principles stand.

Implemented: explicit units/potentials/cutoffs/BCs (`species`,
`lj`, `state1d`); integrator timestep recorded with results
(`DimerRun` carries dt/steps); force/energy/conservation
evidence before any performance claim (`VERIFICATION.md`);
deterministic force accumulation with Newton-III ordering
(`integrator`); classical MD only, quantum exclusion honored
(README disambiguation).

Deferred (deliberately): neighbor-list rebuild semantics (no
N exists yet that needs lists — all-pairs is exact at N ≤ 3);
parallel reduction-ordering modes (single deterministic mode
only); GPU layout/scheduling contracts (no accelerated path);
ensemble/temperature controls beyond kinetic temperature;
checkpoints/trajectories.

Pressure objectives status: periodic-boundary ops PROVEN 1D;
deterministic accumulation PROVEN (bitwise momentum);
structured drift evidence PROVEN. Large arrays, SoA/AoS
transforms, spatial hashing, cell/Verlet lists, GPU kernels,
parallel scatter, migration, multi-generation reproducibility:
OPEN, correctly untouched until a verified dynamics exists
whose contract they must preserve.

## Principles

- Physical units, potential definitions, cutoffs and boundary conditions are explicit.
- Neighbor-list construction/rebuild rules are part of simulation semantics.
- Integrator timestep and ensemble controls are recorded with results.
- Force, energy and conservation/reference evidence precede performance claims.
- Deterministic/reproducible modes define parallel force accumulation and reduction ordering.
- GPU acceleration may change physical layout/scheduling but must preserve the declared numerical contract.
- Initial scope is classical particle/molecular dynamics, not quantum chemistry.

## Pressure objectives

Large contiguous arrays, SoA/AoS transforms, spatial hashing/cell lists, irregular neighbor lists, GPU kernels, parallel scatter/force accumulation, deterministic atomics/reductions, generic precision, vector math, memory migration, checkpoints and multiple CUDA generations.
