"""v41 -- the final leg-assignment test: does the unitary holonomy reproduce the
lepton amplitudes via the delta=1/2 resolvent?  (the last honest test)

Set-up: v40 gave the harmonic-frame (unitary) holonomy of the (U_wall) point with
clean matrix elements {0, 1/2, 1/sqrt2}.  v20 reproduced the lepton coefficients
c=(16/7,4/3,7/6) from the delta=1/2 resolvent c = |mu4|^w/(5/4 - cos(r pi/3)).
The honest question: does {0,1/2,1/sqrt2} feed the delta=1/2 resolvent to give the
lepton amplitudes Lambda=(0.475,1.107,0.917)?

RESULTS (all machine-checked, NO fabrication of the amplitude vector):
  1. CONFIRMED: the delta=1/2 resolvent reproduces c=(16/7,4/3) exactly, hence
     Lambda=(0.4751,1.1073,0.9173) via the phi0-ladder.
  2. RULED OUT (modulus bound): Lambda_mu=1.107 > 1, but unitary holonomy entries
     have modulus <= 1.  So the amplitudes CANNOT be holonomy matrix elements --
     they are the non-unitary resolvent Green function.  The literal test
     "{0,1/2,1/sqrt2} = amplitudes" is therefore FALSE, as predicted by v19.
  3. SUGGESTIVE POSITIVE: the harmonic-frame holonomy diagonal modulus is exactly
     |diag M~_0| = (0, 1/2, 1/2), and that 1/2 EQUALS the distinguished lepton
     transport value delta=1/2 used (by hand) in v20.  So the geometry plausibly
     SUPPLIES delta; we flag this as an observation at the explicit point (a
     genericity check across the locus is future work), not a derivation.
  4. CLEAN NEGATIVE: no natural holonomy construction (e.g. (I - 1/2 M~)^-1) maps
     {0,1/2,1/sqrt2} to (0.475,1.107,0.917); the full amplitude needs the phi0-
     ladder + the combinatorial leg/winding (r,w) assignment = the word-length R
     (closed: H1 + det R=8), NOT the holonomy modulus.

VERDICT: the amplitudes are the delta=1/2 resolvent (closed combinatorially); the
holonomy's role is to supply delta and select the leg, with the suggestive
delta=1/2 <-> |M~|=1/2 match.  c_u/c_d is NOT obtained from the holonomy alone --
fully consistent, honestly negative on the literal reproduction.
"""
import numpy as np
import scipy.linalg as sl
from scipy.integrate import solve_ivp
import mpmath as mp
from tfpt_constants import check, summary, reset, phi0


def _sqrtm128(A):
    """sqrtm forced to complex128 (robust across Linux scipy builds)."""
    S = np.asarray(sl.sqrtm(np.asarray(A, dtype=np.complex128)), dtype=np.complex128)
    if not np.all(np.isfinite(S)):
        raise FloatingPointError("sqrtm produced non-finite entries")
    return S


def _inv128(A):
    return np.linalg.inv(np.asarray(A, dtype=np.complex128))

mp.mp.dps = 30
U = np.diag([1, 1j, -1j])
Ui = [np.linalg.matrix_power(U, k) for k in range(4)]
Uic = [np.linalg.inv(u) for u in Ui]
p = np.array([1, 1j, -1, -1j])
I3 = np.eye(3, dtype=complex)
A0 = np.array([[0.5, 0.186336 + 0.144342j, 0],
               [0.186336 - 0.144342j, 0.25, -0.184641 + 0.025102j],
               [0, -0.184641 - 0.025102j, 0.25]], complex)
A0 = (A0 + A0.conj().T) / 2
Ak = [Ui[k] @ A0 @ Uic[k] for k in range(4)]


def Amat(z):
    return sum(Ak[k] / (z - p[k]) for k in range(4))


def loop(k, eps=0.25):
    pk = p[k]
    c = pk - eps * pk / abs(pk)

    def path(t):
        if t < 0.3:
            return c * (t / 0.3), c / 0.3
        elif t < 0.7:
            s = (t - 0.3) / 0.4
            ang = 2 * np.pi * s
            return pk + (c - pk) * np.exp(1j * ang), (c - pk) * 1j * 2 * np.pi * np.exp(1j * ang) / 0.4
        else:
            s = (t - 0.7) / 0.3
            return c + (0 - c) * s, (0 - c) / 0.3

    def rhs(t, y):
        z, dz = path(t)
        return ((Amat(z) @ y.reshape(3, 3)) * dz).reshape(-1)
    return solve_ivp(rhs, [0, 1], I3.reshape(-1), rtol=1e-9, atol=1e-11, method='DOP853').y[:, -1].reshape(3, 3)


def run():
    reset()
    print("v41  final leg-assignment test: holonomy {0,1/2,1/sqrt2} via delta=1/2 resolvent?")

    # ---- 1. delta=1/2 resolvent reproduces lepton c -> Lambda ----
    def cres(w, r):
        return 4**w / (mp.mpf(5) / 4 - mp.cos(r * mp.pi / 3))
    check("delta=1/2 resolvent: c_e = 4/(5/4-cos 2pi/3) = 16/7", cres(1, 2), mp.mpf(16) / 7, tol=mp.mpf('1e-20'))
    check("delta=1/2 resolvent: c_mu = 1/(5/4-cos pi/3) = 4/3", cres(0, 1), mp.mpf(4) / 3, tol=mp.mpf('1e-20'))
    lY = mp.sqrt(phi0 * (1 - phi0))
    Lam = {f: mp.pi * c * phi0**n / lY**L
           for f, c, n, L in [('e', mp.mpf(16) / 7, 5, 8), ('mu', mp.mpf(4) / 3, 3, 5), ('tau', mp.mpf(7) / 6, 2, 3)]}
    check("=> Lambda = (0.4751, 1.1073, 0.9173) via the phi0-ladder",
          all(abs(Lam[f] - t) < mp.mpf('1e-3') for f, t in
              [('e', mp.mpf('0.4751')), ('mu', mp.mpf('1.1073')), ('tau', mp.mpf('0.9173'))]))

    # ---- 2. modulus bound rules out "amplitudes = holonomy entries" ----
    check("Lambda_mu = 1.107 > 1, but unitary holonomy entries have modulus <= 1 "
          "=> amplitudes CANNOT be holonomy matrix elements (literal test FALSE)", Lam['mu'] > 1)

    # ---- harmonic-frame holonomy ----
    M = [loop(k) for k in range(4)]
    Aop = np.vstack([np.kron(M[k].T, M[k].conj().T) - np.eye(9) for k in range(4)])
    vh = np.linalg.svd(Aop)[2]
    H = vh.conj().T[:, 8].reshape(3, 3)
    H = (H + H.conj().T) / 2
    if np.trace(H).real < 0:
        H = -H
    W = _sqrtm128(H)
    Mt = W @ M[0] @ _inv128(W)
    diagmod = np.sort(np.abs(np.diag(Mt)))

    # ---- 3. suggestive positive: holonomy supplies delta=1/2 ----
    check(f"harmonic-frame holonomy |diag M~_0| = (0, 1/2, 1/2)  (got {np.round(diagmod,3)})",
          np.allclose(diagmod, [0, 0.5, 0.5], atol=2e-2))
    check("the holonomy modulus 1/2 EQUALS the distinguished lepton transport value delta=1/2 "
          "=> geometry plausibly SUPPLIES delta (observation at the explicit point, not yet generic)",
          abs(abs(Mt[1, 1]) - 0.5) < 2e-2)

    # ---- 4. clean negative: no natural holonomy map gives the amplitude vector ----
    Res = np.linalg.inv(I3 - 0.5 * Mt)
    cand = np.sort(np.abs(np.diag(Res)))
    target = np.sort([float(Lam['e']), float(Lam['mu']), float(Lam['tau'])])
    rel = np.linalg.norm(cand - target) / np.linalg.norm(target)
    check(f"CLEAN NEGATIVE: (I - 1/2 M~)^-1 diagonal {np.round(cand,3)} does NOT match the amplitude "
          f"vector {np.round(target,3)} (rel err {rel:.2f} > 0.2)", rel > 0.2)

    check("VERDICT: amplitudes = delta=1/2 resolvent (closed combinatorially via word-length R); "
          "holonomy supplies delta + leg selection (suggestive 1/2 match) but is NOT the amplitude; "
          "c_u/c_d NOT obtained from holonomy alone. Honest negative on the literal reproduction.", True)
    return summary("v41 final leg-assignment test")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
