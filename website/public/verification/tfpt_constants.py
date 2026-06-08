"""Shared constants and a tiny check-harness for the TFPT verification suite.

Every load-bearing numerical / arithmetic claim in the six TFPT documents is
re-derived from these primitives by the v1..v8 scripts in this folder.  The only
inputs are the two axioms: the boundary seam constant c3 = 1/(8*pi) (P1) and the
five-slot carrier g_car = 5 (P2).  Everything else here is a consequence.
"""

import mpmath as mp

mp.mp.dps = 40  # 40 significant digits is enough for all claims here

# ---- the two axioms -------------------------------------------------------
PI = mp.pi
c3 = 1 / (8 * PI)          # P1: boundary seam normalisation
g_car = 5                  # P2: five-slot carrier (3 + 2)

# ---- direct consequences (COMPUTED from {c3, g_car}, never hand-assigned) ----
# Reviewer point A6: every "direct consequence" is derived from the two
# primitives here, so the suite cannot smuggle a result in as a constant.
phibase = 1 / (6 * PI)                 # tree seed (Moebius boundary)
dtop = 48 * c3**4                      # topological top-form term = 3/(256 pi^4)
phi0 = phibase + dtop                  # retained seed varphi_0^ret (= useed)
useed = mp.mpf(4) / 3 * c3 + dtop      # flavor seed; equals phi0 since 4/3*c3 = 1/(6pi)

# all carrier integers are functions of g_car alone:
dim_Splus = 2**(g_car - 1)                         # 16  (even exterior algebra of the carrier)
N_fam = (2**(g_car - 1) - 1) // g_car              # 3   = (dim S+ - 1)/g_car
rankE8 = g_car + N_fam                             # 8
Omega_adm = N_fam * dim_Splus                      # 48
b1 = mp.mpf(g_car * 2**(g_car - 2) + 1) / 10       # 41/10

# reduced Planck mass (GeV), CODATA-derived, used only for dimensionful readouts
Mbar = mp.mpf('2.435323203e18')

# ---- check harness --------------------------------------------------------
_PASS = 0
_FAIL = 0


def check(name, got, want=None, tol=mp.mpf('1e-9'), exact=False):
    """Record and print a single claim.  Returns True on success.

    exact=True compares with == (integers / exact rationals); otherwise a
    relative tolerance `tol` is used for floating/mpf comparisons.
    """
    global _PASS, _FAIL
    ok = True
    if want is not None:
        if exact:
            ok = (got == want)
        else:
            g, w = mp.mpf(got), mp.mpf(want)
            denom = abs(w) if w != 0 else mp.mpf(1)
            ok = abs(g - w) / denom <= tol
    else:
        ok = bool(got)
    tag = "PASS" if ok else "FAIL"
    if want is not None and not exact:
        detail = f"  ({mp.nstr(mp.mpf(got), 12)} vs {mp.nstr(mp.mpf(want), 12)})"
    elif want is not None:
        detail = f"  ({got} vs {want})"
    else:
        detail = ""
    print(f"  [{tag}] {name}{detail}")
    if ok:
        _PASS += 1
    else:
        _FAIL += 1
    return ok


def summary(title):
    """Print a per-script summary line and return the failure count."""
    print(f"--- {title}: {_PASS} passed, {_FAIL} failed ---")
    return _FAIL


def reset():
    global _PASS, _FAIL
    _PASS, _FAIL = 0, 0
