# MNCS language pressure ledger

Record workload, observed behavior, required semantic, reproducer, owner, workaround and closure verification.

## How to read this ledger

Each entry: ID, workload, observed behavior, smallest reproducer,
required semantic, candidate owner, workaround in this repo, status.
A fast dynamics is not enough to close a pressure item; validated
physical behavior must survive the change.

## P-ATOMIC-NEIGHBOR — irregular neighbor lists (blocking at scale)

- Workload: all-pairs force accumulation generalizes to cell/
  Verlet lists with rebuild policy (RFC core semantic).
- Observed: at N ≤ 3 all-pairs is exact and needs no list; the
  language has fixed-size arrays and bounded iteration but no
  compact variable-length neighbor-list abstraction with a
  rebuild rule the compiler understands.
- Required: variable-length (capped) adjacency with construction/
  rebuild as declared computation.
- Candidate owner: `mncs-language` (sequence semantics), not Atomic.
- Workaround: none needed yet — all-pairs direct, rebuild policy
  deferred to a real N rather than simulated with fixed arrays.
- Status: OPEN, non-blocking at N ≤ 3; blocking for any large-N
  or 2D workload.

## P-ATOMIC-UNITS — dimensional analysis (non-blocking)

- Workload: SI species data vs reduced-unit dynamics vs
  temperature/energy conversions.
- Observed: no reusable dimension/unit system. Units live as
  documented contracts; reduced units (the MD community's own
  answer) carry the verification load cleanly.
- Required: generic dimensional analysis (quantity kinds,
  coherent units, dimensionless markers).
- Candidate owner: generic Numeric/Math ecosystem owner.
- Workaround: SI-per-field docs + reduced-unit projections with
  `BadScale` guards; no private units system built.
- Status: OPEN, non-blocking (no unit confusion occurred).

## P-ATOMIC-MATH — many-body/ensemble algebra home (non-blocking)

- Workload: thermostats/barostats, virial pressure, 3+-body
  potentials, future 2D dynamics.
- Observed: `mncs-math` owns exact/integer/rational machinery
  but no f64 ensemble/thermostat layer; nothing needed it yet
  (kinetic temperature is two operations).
- Required: decision on where f64 statistical-mechanics helpers
  live when a thermostat workload arrives.
- Candidate owner: `mncs-math` (or future numerical component).
- Workaround: model-local bookkeeping only; virial pressure and
  thermostats deferred, not stubbed.
- Status: OPEN, non-blocking.

## P-ATOMIC-FIELD — shared length-generic limits (informational)

- Workload: per-size outcome enums (`DimerRun`, `Chain3`,
  `Force3Out`) duplicate shapes across particle counts.
- Observed: same root cause as fluid pressure P-FLUID-FIELD —
  outcome enums cannot carry `[f64; N]` for generic N
  (MNP051/053 probes during the fluid campaign). Atomic chose
  small concrete record/enum shapes instead of the split
  validation/bare-kernel pattern; both are the same workaround.
- Required: nameable length-generic nominal types.
- Candidate owner: `mncs-language` (one fix serves both repos).
- Status: OPEN, non-blocking at N ≤ 3; converges with
  P-FLUID-FIELD — deliberately not a second pressure with a
  second reproducer.

## Closed by discipline (guidance for the next workload)

- `over` is reserved (`iterate…over`): binding named `over`
  fails parsing (MNP050). Prefer positional names (`above`).
- Trailing commas are refused in enum payload declarations
  (MNP132: "expected payload field name"). No trailing commas
  in declarations (constructions were unaffected in this repo).
- Sequence literals cannot seed generic-fn inference (MNE183):
  bind arrays with annotations first (fluid precedent, reused).
- Test names must not shadow library functions (MNE132 arity):
  one rename required (`steady_rhs_value` precedent noted).
- `select` evaluates both arms eagerly: neighbor/force guards
  stay in `if`-branches (fluid P-FLUID-SELECT, reused without
  incident).
- Scientific notation (`1.38e-23`) parses and compares exactly;
  shortest-repr oracle literals round-trip bit-identically.

## Initial pressure targets (from foundation RFC — status)

- High-throughput particle arrays, SoA/AoS, layout control:
  OPEN (no large-N workload yet; SoA lanes used at N ≤ 3).
- Compact variable-length neighbor lists: OPEN
  (P-ATOMIC-NEIGHBOR).
- Spatial hashing/cell lists: OPEN, correctly deferred.
- Periodic-boundary vector ops: PROVEN 1D (minimum image,
  wrapping via consumed rounding).
- Vectorized force kernels: PROVEN scalar-pair form; SIMD OPEN.
- Parallel scatter/accumulation: NOT ATTEMPTED (Newton-III
  accumulation is order-independent by construction).
- Deterministic vs fast reduction modes: single deterministic
  mode PROVEN (bitwise momentum); fast mode nonexistent.
- CUDA/shared-memory/migration/multi-generation: NOT ATTEMPTED.
- Generic f32/f64 and higher precision: f64 only; pressure
  unspent (no workload needed more).
- Checkpoint/trajectory serialization with numeric metadata:
  OPEN (nothing persisted).
