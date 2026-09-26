# Architecture

## Layers

1. **Particle model** — positions, velocities, masses/species, units, box/cell and simulation state.
2. **Spatial indexing** — periodic boundaries, cell lists, Verlet/neighbor lists and rebuild policy.
3. **Interactions** — pair potentials, force/energy kernels and cutoff semantics.
4. **Dynamics** — integrators, constraints and ensemble/temperature-control foundations.
5. **Parallel execution** — SoA/AoS layouts, SIMD, threading, force accumulation and CUDA kernels.
6. **Persistence** — checkpoints/trajectories with explicit reproducibility metadata.
7. **Verification** — force gradients, energy/momentum behavior, known configurations and cross-backend comparison.

## Status (first canonical implementation)

Layer coverage after the foundation slice (all MNCS-native,
Profile 0.18, except language float ops and consumed
`mncs-numerics` rounding/discipline):

- Particle model: SI species + argon reference data, distinct
  ids, 1D box state, reduced-unit projections. DONE (`species`,
  `state1d`).
- Spatial indexing: periodic minimum image + wrapping DONE;
  cell/Verlet lists DEFERRED to a real N (P-ATOMIC-NEIGHBOR).
- Interactions: LJ pair from r² with truncated-cutoff policy
  DONE (`lj`); 3-body/superposition accumulation DONE for statics.
- Dynamics: velocity-Verlet pair step + 32/256-step
  drift-tracking drivers DONE (`integrator`, `model1d`);
  constraints/thermostats DEFERRED (P-ATOMIC-MATH).
- Parallel: not attempted (Newton-III accumulation is
  order-independent by construction; correctness first).
- Persistence: nothing persisted (trajectories/checkpoints OPEN).
- Verification: 39 native tests + 26-check oracle; exact statics,
  bitwise momentum, bounded drift, genuine oscillation,
  oracle-trajectory agreement, degenerate rejection. DONE.

## First milestones

1. Particle/box/unit foundation. DONE.
2. Lennard-Jones reference implementation. DONE (r² kernel,
   exact + minimum + cutoff evidence).
3. Neighbor/cell lists plus periodic boundaries. HALF: periodic
   boundaries done; lists deferred to real N (all-pairs exact
   at N ≤ 3).
4. Velocity-Verlet integration and conservation corpus. DONE
   (momentum bitwise, energy drift bounded, oscillation proven).
5. SIMD/threaded/CUDA kernels and deterministic/reproducible
   modes. DEFERRED except the deterministic mode itself, which
   is the only mode (no fast mode exists to compare).
6. Large-particle and cross-CUDA-generation pressure campaigns.
   DEFERRED (no verified accelerated path to campaign over).
