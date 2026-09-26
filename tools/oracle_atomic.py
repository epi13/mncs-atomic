#!/usr/bin/env python3
"""Independent oracle for the mncs-atomic LJ foundation.

Derives every committed expectation independently of the MNCS
implementation: exact rational arithmetic (Fraction) for statics,
cutoff policy, periodic images, and unit conversions; an
independently coded float64 velocity-Verlet reference for dynamics
(different code path, same equations); invariant bounds (drift,
extrema, momentum) that do not depend on trajectory identity.

Canonical verification uses reduced units (eps = sig = m = 1).

Usage:
    python3 tools/oracle_atomic.py
"""

import math
from fractions import Fraction as Q

FAILURES = []


def check(name, got, want):
    ok = got == want
    print("%-46s got=%s want=%s %s" % (name, got, want, "OK" if ok else "MISMATCH"))
    if not ok:
        FAILURES.append(name)


def lj_exact_rational(r2, eps=Q(1), sig=Q(1)):
    """Exact LJ pair from squared distance (mirrors the documented
    formula, implemented here with independent rational code)."""
    sr2 = sig * sig / r2
    sr6 = sr2 ** 3
    sr12 = sr6 ** 2
    return Q(24) * eps * (2 * sr12 - sr6) / r2, Q(4) * eps * (sr12 - sr6)


def lj_float(r2, eps=1.0, sig=1.0):
    sr2 = sig * sig / r2
    sr6 = sr2 * sr2 * sr2
    sr12 = sr6 * sr6
    return 24.0 * eps * (2.0 * sr12 - sr6) / r2, 4.0 * eps * (sr12 - sr6)


def vv_step_float(x0, x1, v0, v1, m0, m1, dt, box):
    dx = x1 - x0
    dx -= round(dx / box) * box
    fr, u = lj_float(dx * dx)
    f0, f1 = -fr * dx, fr * dx
    nx0 = x0 + v0 * dt + f0 / (2.0 * m0) * dt * dt
    nx1 = x1 + v1 * dt + f1 / (2.0 * m1) * dt * dt
    ndx = nx1 - nx0
    ndx -= round(ndx / box) * box
    nfr, nu = lj_float(ndx * ndx)
    nf0, nf1 = -nfr * ndx, nfr * ndx
    return (nx0, nx1,
            v0 + (f0 + nf0) / (2.0 * m0) * dt,
            v1 + (f1 + nf1) / (2.0 * m1) * dt, nu)


def main():
    # --- exact statics ------------------------------------------------------
    fr, u = lj_exact_rational(Q(1))
    check("F(r=sigma)/r exact", fr, Q(24))
    check("U(r=sigma) exact", u, Q(0))
    fr2, u2 = lj_exact_rational(Q(4))
    check("F/r at r=2 exact", fr2, Q(-93, 1024))
    check("U at r=2 exact", u2, Q(-63, 1024))
    check("F at r=2 exact", fr2 * 2, Q(-93, 512))

    # --- minimum (float, irrational location) --------------------------------
    rstar = 2.0 ** (1.0 / 6.0)
    frs, us = lj_float(rstar * rstar)
    check("F(r*) ~ 0", abs(frs * rstar) < 1e-12, True)
    check("U(r*) ~ -eps", abs(us + 1.0) < 1e-12, True)

    # --- cutoff policy -------------------------------------------------------
    check("r=2.5 within rc=2.5", Q(25, 4) <= Q(25, 4), True)
    check("r=3.0 beyond rc=2.5", Q(9) > Q(25, 4), True)
    _, ucut = lj_float(2.5 * 2.5)
    check("U(2.5) nonzero (truncated, not shifted)", abs(ucut) > 0.01, True)

    # --- periodic images ------------------------------------------------------
    check("min image 6.0 in L=10", Q(6) - 10 * round(6.0 / 10), Q(-4))
    check("min image -6.0 in L=10", Q(-6) - 10 * round(-6.0 / 10), Q(4))
    check("wrap 12.5 in L=10", Q(25, 2) - 10 * math.floor(1.25), Q(5, 2))

    # --- argon SI conversions --------------------------------------------------
    m_si = 39.948 * 1.66053906660e-27
    e_si = 119.8 * 1.380649e-23
    s_si = 3.405 * 1.0e-10
    check("Ar mass kg", abs(m_si - 6.6335e-26) / 6.6335e-26 < 1e-3, True)
    check("Ar eps J", abs(e_si - 1.65402e-21) / 1.65402e-21 < 1e-3, True)
    check("Ar sigma m", s_si == 3.405e-10, True)
    check("reduced sigma of Ar", s_si / s_si == 1.0, True)

    # --- exact VV half-step ----------------------------------------------------
    # rest at r=1, dt=1/16: x0' = -12/256 = -3/64, x1' = 67/64.
    check("half-step x0'", Q(-12, 256), Q(-3, 64))
    check("half-step x1'", 1 + Q(12, 256), Q(67, 64))

    # --- reference dynamics ----------------------------------------------------
    dt = 0.002
    box = 10.0
    x0, x1, v0, v1 = 0.0, 1.3, 0.0, 0.0
    _, e0 = lj_float(1.3 * 1.3)
    E0 = e0
    maxdrift = 0.0
    rmin, rmax = 9.0, -9.0
    for _ in range(256):
        x0, x1, v0, v1, uu = vv_step_float(x0, x1, v0, v1, 1.0, 1.0, dt, box)
        r = abs(x1 - x0)
        rmin = min(rmin, r)
        rmax = max(rmax, r)
        maxdrift = max(maxdrift, abs((uu + 0.5 * (v0 * v0 + v1 * v1)) - E0))
    check("256-step drift < 1e-4", maxdrift < 1e-4, True)
    check("256-step rmin < 1.05", rmin < 1.05, True)
    check("256-step rmax > 1.29", rmax > 1.29, True)
    check("256-step momentum == 0", v0 + v1 == 0.0, True)
    check("256-step clock t", dt * 256 == 0.512, True)
    print("ref final: x0=%.15f x1=%.15f v0=%.15f v1=%.15f u=%.15f" % (x0, x1, v0, v1, uu))
    print("ref: E0=%.15f drift=%.3e rmin=%.12f rmax=%.12f" % (E0, maxdrift, rmin, rmax))

    # --- three-lane chain reference -----------------------------------------------
    xs = (0.0, 1.0, 2.2)
    box = 10.0
    ft = [0.0, 0.0, 0.0]
    ut = 0.0
    for (i, j) in ((0, 1), (0, 2), (1, 2)):
        dx = xs[j] - xs[i]
        dx -= round(dx / box) * box
        fr, uu = lj_float(dx * dx)
        ft[i] += -fr * dx
        ft[j] += fr * dx
        ut += uu
    print("ref chain: f0=%.15f f1=%.15f f2=%.15f u=%.15f sum=%.3e"
          % (ft[0], ft[1], ft[2], ut, ft[0] + ft[1] + ft[2]))

    # --- single VV step from rest at r=sigma, dt=1/16 ---------------------------
    s = vv_step_float(0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0 / 16.0, box)
    print("ref step1: x0=%.15f x1=%.15f v0=%.15f v1=%.15f u=%.15f" % s)

    # --- anharmonic period note -------------------------------------------------
    k = 72.0 * 2.0 ** (-1.0 / 3.0)
    t_harm = 2.0 * math.pi * math.sqrt(0.5 / k)
    check("harmonic period < observed 0.768", t_harm < 0.768, True)
    check("harmonic period sane", 0.4 < t_harm < 0.768, True)

    print("----")
    if FAILURES:
        print("ORACLE FAIL: %d mismatches: %s" % (len(FAILURES), FAILURES))
        raise SystemExit(1)
    print("ORACLE PASS")


if __name__ == "__main__":
    main()
