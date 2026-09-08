# mncs-atomic

Machine-native molecular and particle simulation for MNCS.

`mncs-atomic` targets atomic-scale and classical particle simulation—not CPU atomic operations. It pressures `mncs-language` with massive particle sets, spatial partitioning, neighbor lists, force accumulation, periodic boundaries, numerical integration, deterministic parallelism and GPU-heavy execution.

## Initial scope

- particle/state and unit abstractions
- spatial cells, neighbor lists and periodic boundaries
- established pair-potential workloads such as Lennard-Jones
- force/energy evaluation
- time integrators and constraints
- temperature/ensemble-control foundations
- conservation and reference-case verification
- CPU/SIMD/CUDA execution and cross-generation reproducibility studies

## Repository layout

- `docs/ARCHITECTURE.md`
- `docs/rfcs/0001-foundation.md`
- `docs/LANGUAGE_PRESSURES.md`
- `AGENTS.md`
