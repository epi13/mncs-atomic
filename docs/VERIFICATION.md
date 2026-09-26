# Verification

Canonical verification uses reduced units (eps = sig = m = 1,
box 10, rc = 2.5) unless SI is stated.

## Pair kernel (lj, 6 tests)

- r = σ: F/r = 24, U = 0 — exact `==` (oracle rationals).
- r = 2σ: F/r = −93/1024, U = −63/1024 — exact `==`.
- Well minimum r* = 2^{1/6}: F ≈ 0, U ≈ −1 (tol 1e-9).
- Cutoff: r = 2.5 inside (closed), r = 3 `Neglected`
  (legitimate, not error), rc ≤ 0 `BadInput`.
- Coincident lanes and non-positive eps/sigma: `BadInput`.
- Projection antisymmetry bitwise (f0 + f1 == 0).

## Periodic state (state1d, 5 tests)

- Minimum images incl. cross-boundary pairs and the half-box tie
  (half away from zero, closed boundary) — exact.
- Wrapping into [0, L), negative inputs — exact.
- Squared distances incl. across-boundary r² = 4 — exact.
- Id distinctness (dimer/trimer), duplicates rejected — identity
  vs property equality pinned.

## Species and units (species, 7 tests)

- Validation order mass → epsilon → sigma.
- Argon reference data pinned (39.948 u, 119.8 K, 3.405 Å).
- SI conversions vs oracle (mass 6.63352146325368e-26 kg,
  eps 1.654017502e-21 J agree to 1e-9 relative; sigma exact).
- Reduced projections + `BadScale` arms.

## Integrator (integrator, 9 tests)

- VV position half-step from rest at σ, dt = 1/16: x0' = −3/64,
  x1' = 67/64 — exact.
- Full step velocities/energy vs oracle floats (tol 1e-9).
- Momentum bitwise zero after stepping.
- Beyond-cutoff free drift: uniform motion exact, u = 0.
- Three-lane [0, 1, 2.2] forces/energy vs oracle (tol 1e-9);
  net force zero to 1e-12.
- 32-step smoke: bounded drift, inward motion, momentum held.
- Degenerate mass/dt/box rejected.

## Derived (derived, 4 tests)

- Reduced T* = 2K/dof exact; T = 0 at rest (valid, not
  degenerate); unphysical kb/KE/dof rejected; drift predicate
  with non-positive tolerance accepting nothing.

## End-to-end models (model1d, 8 tests)

- Static dimer at σ: F = ∓24, U = K = P = 0 — exact.
- 256-step oscillation (dt = 0.002, from [0, 1.3]):
  trajectory vs oracle floats (tol 1e-9 on all five state
  values); drift 4.2e-5 < 1e-4 bound; rmin 1.039 < 1.05 and
  rmax 1.300 > 1.29 prove genuine oscillation without phase
  knowledge; P == 0.0 bitwise; t = 0.512, steps = 256.
- Free-drift limiting case (start beyond cutoff): exactly
  stationary, zero drift — exact.
- Chain statics vs oracle (tol 1e-9).
- Degenerate species/box/ids/dt/rc rejected per path.

## Independent oracle

`tools/oracle_atomic.py`: 26 checks — exact LJ rationals,
irrational-minimum floats, cutoff comparisons, image/wrap
integers, SI conversions, exact half-step fractions, an
independently coded float64 VV reference (trajectory, drift,
extrema, momentum, clock), and the harmonic-vs-observed period
note (0.59 harmonic vs 0.77 observed: anharmonicity documented,
not hidden). No shared code with the MNCS implementation. Runs
inside `scripts/run_tests.py`; verdict joins the evidence JSON.

## Totals

39 native `mncs test` declarations across 6 suites + 26 oracle
checks. Full run ≈ 2m37s wall (per-suite toolchain invocations
dominate; the largest case is 256 steps × 2 particles).
Evidence: `target/test-evidence-*.json`
(schema `mncs-atomic.test-evidence/1`, revision-bound).

## What is NOT claimed

Quantum accuracy (classical LJ only); 2D/3D; thermostats/
ensembles beyond kinetic temperature; neighbor lists;
production MD performance; cross-backend bitwise identity
(single-backend determinism: reruns green, same outputs).
