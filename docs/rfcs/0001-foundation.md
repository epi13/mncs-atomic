# RFC 0001: Molecular/particle simulation foundation

Status: Draft

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
