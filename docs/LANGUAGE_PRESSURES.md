# MNCS language pressure ledger

Record workload, observed behavior, required semantic, reproducer, owner, workaround and closure verification.

## Initial pressure targets

- high-throughput particle arrays and SoA/AoS layout control
- compact variable-length neighbor lists
- spatial hashing/cell-list construction
- periodic-boundary vector operations
- vectorized force kernels
- parallel scatter/force accumulation
- deterministic versus fast atomic/reduction modes
- CUDA kernel launch and shared/local memory ergonomics
- host/device ownership and asynchronous migration
- generic f32/f64 and future higher-precision kernels
- checkpoint/trajectory serialization without losing numeric metadata
- cross-GPU-generation reproducibility evidence

A pressure item is not resolved until the real particle workload remains scientifically valid and the relevant backend behavior is measured.
