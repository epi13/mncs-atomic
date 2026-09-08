# Architecture

## Layers

1. **Particle model** — positions, velocities, masses/species, units, box/cell and simulation state.
2. **Spatial indexing** — periodic boundaries, cell lists, Verlet/neighbor lists and rebuild policy.
3. **Interactions** — pair potentials, force/energy kernels and cutoff semantics.
4. **Dynamics** — integrators, constraints and ensemble/temperature-control foundations.
5. **Parallel execution** — SoA/AoS layouts, SIMD, threading, force accumulation and CUDA kernels.
6. **Persistence** — checkpoints/trajectories with explicit reproducibility metadata.
7. **Verification** — force gradients, energy/momentum behavior, known configurations and cross-backend comparison.

## First milestones

1. Particle/box/unit foundation.
2. Lennard-Jones reference implementation.
3. Neighbor/cell lists plus periodic boundaries.
4. Velocity-Verlet integration and conservation corpus.
5. SIMD/threaded/CUDA kernels and deterministic/reproducible modes.
6. Large-particle and cross-CUDA-generation pressure campaigns.
