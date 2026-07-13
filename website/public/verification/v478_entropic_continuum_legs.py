"""v478 -- GRAV.ENTROPIC.LEGS.01: first computable steps on the TWO remaining
research legs of the entropic-action bridge (v473-v477 round): (A) the AP2
CONTINUUM leg -- the state-side modular Hamiltonian of the compressed critical
state flows to the CHM/Bisognano-Wichmann geometric form, i.e. exactly the
object TFPT's Einstein derivation consumes (v323/v358); and (B) the MEASURE
leg -- the v477 one-moment condition reduced to a single-scale corollary with
an exact closed form for the KMS time t0, and the nearby integer explicitly
DECLINED per the anti-numerology discipline (v354/v355).  Both legs stay [O];
nothing closes.

Leg A (AP2 continuum).  v476 forced the state-side reading: Delta_Sigma is
built FROM the compressed relative metric/covariance.  The continuum question
is whether that object is the GEOMETRIC modular operator (CHM/BW boost).  On
the exactly solvable critical chain (infinite-volume sinc kernel, high
precision) the answer is exhibited:

  [N] 1. CALABRESE-CARDY c = 1.  The compressed interval state has S(L) =
        (c/3) ln L + k with c_est = 1.00089, 1.00038, 1.00021 for the pairs
        (8,16), (12,24), (16,32) -- monotone convergence to the Dirac value
        c = 1 (= 2 Majoranas x 1/2, the v450 reading); a gapped control
        chain gives c_est ~ 2e-4 -> 6e-8 (area law).  The compressed state
        carries the conformal/BW structure, quantitatively.
  [N] 2. CHM PARABOLA.  The nearest-neighbour couplings of the Peschel
        modular Hamiltonian K = ln((1-C_A)/C_A) organise on the CHM weight
        beta(x) = x(L-x)/L with correlation 0.866 -> 0.967 -> 0.986
        (L = 8, 16, 24, monotone), and the rescaled mid-plateau drifts by
        shrinking steps -- the state-side Delta_Sigma flows to the geometric
        CHM/BW form in the continuum limit (constants deliberately NOT
        asserted: the lattice EH is only asymptotically local).
  [N] 3. QUASI-LOCALITY STRUCTURE.  At half filling the EVEN-range bands of
        K vanish identically (particle-hole structure; r = 2 band = 0 to
        precision) and the odd tails are small (mean |K_{i,i+3}| / mean
        |K_{i,i+1}| ~ 0.018) -- the modular Hamiltonian is quasi-local with
        a parabolic envelope, the lattice shadow of the local boost.
  Leg-A verdict [C]: the state-side reading (v476) meets TFPT's geometric
        modular input (CHM ball, v323/v358) in the continuum limit; the
        continuum AP2 statement itself stays [O].

Leg B (the measure).  v477 reduced the R^2 route to mu2/mu1^2 =
(72/17)(8 pi)^9.  The sharpest special case:

  [E] 4. SINGLE-SCALE COROLLARY.  For a single-scale measure dmu = delta(t -
        t0) dt the moments give mu2/mu1^2 = e^{t0} EXACTLY (symbolic), so
        the condition forces t0 = ln(72/17) + 9 ln(8 pi) = 30.461...: ONE
        dimensionless KMS time with an exact closed form.  DECLINED
        explicitly: t0 is NOT h(E8) = 30 (difference 0.461 -- the near-miss
        is recorded and rejected per the v354/v355 no-free-pattern rule); no
        TFPT atom equals t0; deriving the measure from the entropic
        structure stays OPEN.
  [C/O] 5. Scope: leg A is a lattice exhibit (not a continuum proof); leg B
        is a parametrisation (not a derivation).  No status marker moves.

NET TYPING: [N] the three lattice exhibits (high-precision mpmath, 50 digits);
[E] the single-scale corollary (symbolic); [C] the meeting-point reading; [O]
both legs.  Extends GRAV.ENTROPIC.COMPRESS.01 (v476) / .SCALEFLOW.01 (v477).
Numerical + one exact corollary; Python-only by nature (mpmath eigensolver),
the exact corollary flagged in the Wolfram README.
"""
import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset

mp.mp.dps = 50


def sinc_cov(L):
    """Infinite-volume half-filled critical covariance, compressed to L sites."""
    M = mp.matrix(L, L)
    for i in range(L):
        for j in range(L):
            if i == j:
                M[i, j] = mp.mpf('0.5')
            else:
                d = i - j
                M[i, j] = mp.sin(mp.pi * d / 2) / (mp.pi * d)
    return M


def entropy(C):
    w, _ = mp.eigsy(C)
    S = mp.mpf(0)
    for k in range(C.rows):
        lam = w[k]
        if 0 < lam < 1:
            S -= lam * mp.log(lam) + (1 - lam) * mp.log(1 - lam)
    return S


def modular_h(C):
    w, V = mp.eigsy(C)
    return V * mp.diag([mp.log((1 - w[k]) / w[k]) for k in range(C.rows)]) * V.T


def corr(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    vx = mp.sqrt(sum((x - mx) ** 2 for x in xs))
    vy = mp.sqrt(sum((y - my) ** 2 for y in ys))
    return cov / (vx * vy)


def run():
    reset()
    print("v478  GRAV.ENTROPIC.LEGS.01: the two remaining legs -- AP2 continuum exhibit + the measure corollary")

    # 1. Calabrese-Cardy c = 1 (critical) vs c = 0 (gapped control)
    S = {L: entropy(sinc_cov(L)) for L in (8, 12, 16, 24, 32)}
    c_est = [float(3 * (S[b] - S[a]) / mp.log(mp.mpf(b) / a))
             for a, b in ((8, 16), (12, 24), (16, 32))]
    import numpy as np
    Ng = 240
    h = np.zeros((Ng, Ng))
    for i in range(Ng - 1):
        h[i, i + 1] = h[i + 1, i] = -1.0
    for i in range(Ng):
        h[i, i] = (-1.0) ** i
    wg, vg = np.linalg.eigh(h)
    Cg = (vg[:, wg < 0] @ vg[:, wg < 0].T)

    def s_gap(L):
        off = (Ng - L) // 2
        lam = np.linalg.eigvalsh(Cg[off:off + L, off:off + L])
        lam = lam[(lam > 1e-12) & (lam < 1 - 1e-12)]
        return float(-(lam * np.log(lam) + (1 - lam) * np.log(1 - lam)).sum())

    c_gap = 3 * (s_gap(32) - s_gap(16)) / float(mp.log(2))
    check("CALABRESE-CARDY c = 1 [N] (leg A): the compressed critical interval has "
          "S(L) = (c/3) ln L + k with c_est = %s (pairs (8,16),(12,24),(16,32)) -- "
          "monotone convergence to the Dirac c = 1 (= 2 Majoranas x 1/2, the v450 "
          "reading); gapped control c_est = %.1e (area law) -- the compressed state "
          "carries the conformal/BW structure quantitatively"
          % (["%.5f" % c for c in c_est], c_gap),
          all(abs(c - 1) < 2e-3 for c in c_est) and
          abs(c_est[2] - 1) < abs(c_est[1] - 1) < abs(c_est[0] - 1) and
          abs(c_gap) < 1e-4)

    # 2. CHM parabola: NN couplings vs beta(x) = x(L-x)
    corrs, plateaus = [], []
    for L in (8, 16, 24):
        K = modular_h(sinc_cov(L))
        nn = [-K[i, i + 1] for i in range(L - 1)]
        xs = [i + mp.mpf('0.5') for i in range(L - 1)]
        par = [x * (L - x) for x in xs]
        corrs.append(float(corr(nn, par)))
        mid = (L - 1) // 2
        plateaus.append(float(nn[mid] * L / par[mid]))
    drift = [abs(plateaus[i + 1] - plateaus[i]) for i in range(2)]
    check("CHM PARABOLA [N] (leg A): the NN couplings of K = ln((1-C_A)/C_A) "
          "organise on the CHM weight beta(x) = x(L-x)/L with correlation %s "
          "(L = 8, 16, 24 -- monotone toward 1), mid-plateau %s with shrinking "
          "drift %s -- the state-side Delta_Sigma flows to the geometric CHM/BW "
          "form that TFPT's Einstein derivation consumes (v323/v358); constants "
          "deliberately not asserted (the lattice EH is only asymptotically local)"
          % (["%.4f" % c for c in corrs], ["%.4f" % p for p in plateaus],
             ["%.1e" % d for d in drift]),
          corrs[0] < corrs[1] < corrs[2] and corrs[2] > 0.98 and drift[1] < drift[0])

    # 3. quasi-locality: even bands vanish, odd tails small + parabolic
    L = 24
    K = modular_h(sinc_cov(L))
    band = {r: [K[i, i + r] for i in range(L - r)] for r in (1, 2, 3)}
    even_max = max(abs(v) for v in band[2])
    tail_ratio = (sum(abs(v) for v in band[3]) / len(band[3])) / \
                 (sum(abs(v) for v in band[1]) / len(band[1]))
    xs3 = [i + mp.mpf('1.5') for i in range(L - 3)]
    corr3 = float(corr([-v for v in band[3]], [x * (L - x) for x in xs3]))
    check("QUASI-LOCALITY [N] (leg A): at half filling the EVEN-range bands of K "
          "vanish identically (max |K_{i,i+2}| = %.1e, particle-hole structure), "
          "the odd tail is small (mean ratio r=3/r=1 = %.4f) and itself "
          "parabola-enveloped (corr %.3f) -- the modular Hamiltonian is quasi-local "
          "with the boost envelope, the lattice shadow of the local BW form"
          % (float(even_max), float(tail_ratio), corr3),
          float(even_max) < 1e-30 and float(tail_ratio) < 0.05 and corr3 > 0.9)

    # 4. single-scale corollary (leg B, exact)
    t0s, pi_s = sp.symbols('t0 pi_s', positive=True)
    mu1 = t0s * sp.exp(-t0s)
    mu2 = t0s ** 2 * sp.exp(-t0s)
    ratio = sp.simplify(mu2 / mu1 ** 2)
    target = sp.Rational(72, 17) * (8 * sp.pi) ** 9
    t0_val = sp.log(target)
    t0_num = float(t0_val)
    check("SINGLE-SCALE COROLLARY [E] (leg B): a single-scale measure dmu = "
          "delta(t - t0) dt has mu2/mu1^2 = %s = e^{t0} exactly, so the v477 "
          "moment condition forces t0 = ln(72/17) + 9 ln(8 pi) = %.6f -- ONE "
          "dimensionless KMS time, exact closed form; DECLINED: t0 is NOT "
          "h(E8) = 30 (difference %.3f; near-miss rejected per the v354/v355 "
          "no-free-pattern rule); no TFPT atom equals t0 -- deriving the measure "
          "from the entropic structure stays OPEN"
          % (ratio, t0_num, t0_num - 30),
          ratio == sp.exp(t0s) and
          sp.simplify(t0_val - sp.log(sp.Rational(72, 17)) - 9 * sp.log(8 * sp.pi)) == 0 and
          abs(t0_num - 30.4610) < 1e-3 and abs(t0_num - 30) > 0.4)

    # 5. scope
    check("SCOPE [C/O]: leg A is a lattice exhibit (the state-side modular data "
          "flows to the CHM/BW geometric form), NOT a continuum proof; leg B is a "
          "parametrisation (one exact KMS time), NOT a derivation. Both legs stay "
          "[O]; no status marker moves", True)

    return summary("v478 GRAV.ENTROPIC.LEGS.01: the two remaining legs, first computable "
                   "steps -- leg A (AP2 continuum): compressed critical state has c_est -> 1 "
                   "(1.0009/1.0004/1.0002; gapped control ~0), EH NN couplings on the CHM "
                   "parabola (corr 0.87 -> 0.99), even bands exactly zero, odd tails 2% -- the "
                   "state-side Delta_Sigma flows to the CHM/BW form TFPT's Einstein derivation "
                   "consumes; leg B (measure): single-scale corollary mu2/mu1^2 = e^{t0} forces "
                   "t0 = ln(72/17) + 9 ln(8pi) = 30.461 exactly, near-miss to 30 DECLINED; [C] "
                   "meeting point; [O] both legs open, no marker moves")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
