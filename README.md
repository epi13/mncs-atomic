# mncs-atomic

<!-- MNCS:generated:begin -->
## Project entry

Machine-native classical particle simulation for MNCS: atoms as Lennard-Jones particles in periodic boxes integrated with velocity-Verlet dynamics, expressed natively in mncs-language.

```bash
python3 scripts/run_tests.py
```

Declared capabilities (declarations do not establish execution health):

- `atomic-simulation/0.1` — mncs-library (experimental)

Semantic sources and ownership: `.mncs/projections.json`.
<!-- MNCS:generated:end -->

Machine-native classical particle simulation for MNCS: atoms as
Lennard-Jones particles in periodic boxes, integrated with
velocity-Verlet dynamics. **Not CPU atomic operations** (no
compare-and-swap, memory ordering, or lock-free primitives live
here) and **not quantum chemistry** (no wavefunctions,
orbitals, or electronic structure).

`mncs-atomic` is the canonical home of **atomic-scale particle
semantics** — species parameters, particle identity, periodic
state, pair potentials with cutoff policy, deterministic
integrators, and ensemble-adjacent derived quantities — expressed
natively in `mncs-language` (Profile 0.18). There is exactly one
canonical implementation: no `atomic-v1/v2`, no `native-atomic`,
no parallel reference/production forks, no compatibility layers.

## Ownership boundary

| Concern | Owner | Atomic relationship |
|---|---|---|
| Scalar ops, `fround`/`ffloor`/`fabs`/`fmin`/`fmax`, `approx` | `mncs-numerics` | Consumed; never duplicated |
| Generic matrices, solvers, complex numbers, autodiff | `mncs-math` | Not a dependency; generic needs recorded as pressure |
| Points/vectors/transforms (2D+) | `mncs-geometry` | Not a dependency of the 1D slice; 2D+ will consume it |
| Finite-element topology/assembly | `mncs-fem` | Untouched; nothing forced into it |
| Continuum fields/fluxes | `mncs-fluid` | Sibling domain; no shared code, no duplication either |
| Content hashes/signatures | `mncs-crypto` | Not needed; would be consumed, never re-implemented |
| Structured data / serialization | `mncs-data` | No trajectory storage in Atomic |
| Test declarations, assertions, runner policy | `mncs-test` | Consumed via `mncs test`; no private harness |
| Execution/admission/lifecycle | Forge/Fabric | Atomic schedules nothing |
| Persistence / provenance graphs | Store/Lineage | Atomic persists nothing |
| Species, ids, boxes, LJ pairs, VV steps, temperature, results | **`mncs-atomic`** | Canonical home |

## Current capability (foundation slice)

Two-body + three-body 1D Lennard-Jones workloads, fully native
except language float ops and consumed Numeric discipline:

- `src/atomic/species.mncs` — SI species validation, argon
  reference data with provenance, SI conversions, reduced units.
- `src/atomic/state1d.mncs` — periodic box, minimum image,
  wrapping, squared distances, id-distinctness invariants.
- `src/atomic/lj.mncs` — LJ pair from r² (no sqrt), truncated
  cutoff with `Neglected`/`BadInput` structure, Newton-III
  projection.
- `src/atomic/integrator.mncs` — velocity-Verlet pair step,
  three-lane accumulation, K/P/E bookkeeping, 32/256-step
  drift-tracking drivers.
- `src/atomic/derived.mncs` — kinetic temperature, drift
  predicate.
- `src/atomic/model1d.mncs` — static dimer at σ, 256-step dimer
  dynamics, static 3-chain.

## Verification

39 native `mncs test` declarations across 6 suites
(`scripts/run_tests.py`), exact `==` on dyadic values with
explicit `approx` where rounding genuinely occurs, plus the
independent oracle `tools/oracle_atomic.py` (exact rationals +
independent float reference trajectory, no shared code).
Bitwise momentum, bounded energy drift, genuine oscillation,
oracle-trajectory agreement, and degenerate-model rejection. See
`docs/VERIFICATION.md` and `evidence/atomic-capabilities.json`.

## Layout

- `src/atomic/` — the library (`.mncs` only, no host semantics)
- `tests/native/` — in-language contracts via `mncs test`
- `scripts/run_tests.py` — canonical runner (suites + oracle)
  with revision-bound JSON evidence
- `tools/oracle_atomic.py` — independent reference oracle
- `docs/ARCHITECTURE.md` — layers and milestone status
- `docs/ATOMIC_MODEL.md` — ownership boundary and RFC classification
- `docs/VERIFICATION.md` — reference evidence
- `docs/LANGUAGE_PRESSURES.md` — pressure ledger with reproducers
- `docs/rfcs/0001-foundation.md` — foundation RFC (implemented
  slice noted)

## Adding a new workload

1. Create `src/atomic/<name>.mncs` (`module mncs.atomic.<name>.v1`;
   the file path must mirror the module segments).
2. State units, potential/model, cutoff, boundary conditions,
   timestep, precision, and method in the header; map every math
   term to its implemented term.
3. Validate all inputs into data outcomes (no traps for bad models).
4. Add a native suite under `tests/native/` + runner entry, with
   known-answer, invariant, symmetry, and degenerate cases plus
   oracle cross-checks. Do not imply quantum accuracy from
   classical foundations.
