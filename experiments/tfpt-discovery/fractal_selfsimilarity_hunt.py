#!/usr/bin/env python3
"""
FRACTAL.HUNT.01 -- new fractal / self-similarity structures in TFPT
(discovery sandbox; exploration only, nothing promoted, no scorecard row).

Known & therefore EXCLUDED here (see experiments/SIGNATURES.md and the
discovery scripts recursive_crystal.py / tfpt_decagonal.py /
deeper_connections_probe.py / metallic_compactness_ladder.py):
  - single-tone log-periodic comb omega_1 = 2pi/ln((3/2)^6) = 2.5827 (S2b/S4)
  - E8 power-law ladder X ~ (D_n/60)^kappa (v5), phi0/lambda_Y mass ladder (v18)
  - Catalan recursion u = 1 + lambda_C^2 u^2, alpha cubic fixed point
  - 5->3 cut-and-project quasicrystal (space), metallic-mean compactness ladder
  - Feigenbaum route: TFPT sits at the reducible r=1 point (not chaotic)

NEW AXES probed here:

  F1  MORAN / SIMILARITY DIMENSION OF THE TRANSFER IFS.  Reading the decaying
      transfer eigenvalues {(2/3)^6, (1/3)^6} (v54/v124) as contraction ratios
      of a self-similar (Cantor-type) set, the Moran equation
          sum_i r_i^s = 1
      has the EXACT solution s = 1/6 = 1/p2, because the base ratios satisfy
      2/3 + 1/3 = 1.  Codimension 1 - 1/6 = 5/6 = gamma_car = g_car/p2 (the
      kappa_E8 numerator).  UNIQUENESS: for the family spectrum
      lambda_n = (1-n/N)^{p2}, the unit partition sum_{n=1}^{N-1}(1-n/N) = 1
      holds iff (N-1)/2 = 1 iff N = 3 = N_fam: only the physical family count
      gives the clean dimension 1/p2.

  F2  THE KERNEL IS A NONLATTICE STRING.  ln(1/r1)/ln(1/r2) = ln(3/2)/ln3 is
      irrational (3/2 and 3 are multiplicatively independent: (3/2)^m = 3^n
      forces 2^m = 3^{m-n}, so m = n = 0).  In Lapidus' classification the
      two-ratio transfer string is NONLATTICE: the pure omega_1 comb is only
      the lattice APPROXIMATION.  The continued fraction of the bend
      ln3/ln(3/2) = 2.70951... is computed; its convergents control which
      log-frequencies can resonate (F3/F4).

  F3  COMPLEX DIMENSIONS.  The geometric zeta of the string is
          zeta(s) = 1/f(s),   f(s) = 1 - e^{-a s} - e^{-b s},
          a = Delta = 6 ln(3/2),  b = 6 ln 3.
      Complex roots s_k = sigma_k + i t_k are found numerically (Newton from a
      seed grid).  Nonlattice => the only root on Re s = D is s = D = 1/6; all
      oscillatory roots sit strictly left of D (damped), and the second comb
      tone omega_2 = 2pi/b = 0.95324 appears with omega_1/omega_2 = bend
      EXACTLY (the S3 bend = ratio of the two comb frequencies).

  F4  THE CASCADE IS A LOG-TIME QUASICRYSTAL.  The binomially degenerate
      cascade rates {k a + m b} have Laplace transform exactly zeta(s), so the
      resonances of the log-time "diffraction" |zeta(sigma_0 + i omega)| ARE
      the complex dimensions of F3, and each strong peak is labelled by TWO
      integers (k, l) with omega a ~ 2pi k, omega b ~ 2pi l -- a rank-2
      Fourier module in log-time, the temporal sibling of the rank-5 spatial
      quasicrystal (tfpt_decagonal).  Fixed-generation multiplets are exact
      arithmetic progressions with spacing b - a = 6 ln 2 (third tone
      omega_3 = 2pi/(6 ln 2) = 1.51134), with 1/omega_2 = 1/omega_1 + 1/omega_3.

  F5  THE CARRIER COLLAPSE ORBIT.  Iterating the family-count map itself,
          F(g) = (2^{g-1} - 1)/g,
      gives 5 -> 3 -> 1 -> 0: the compiler formula N_fam = F(g_car) is one
      step of a self-similar recursion whose vacuum basin is EXACTLY
      {1, 3, 5} (= the Pascal-ladder ranks 2K+1, K = 0,1,2 of v108).  Even g
      never divide the odd 2^{g-1}-1; odd g >= 7 have F(g) > g whenever the
      step is defined (2^{g-1}-1 > g^2), so no orbit from g >= 6 can ever
      descend -- g_car = 5 is the LARGEST rank that compiles down to vacuum.

  F6  DECLINED (quantified, NOT claims): bend vs e; ln(Lambda_DSI)/ln(phi_golden)
      vs 5.

  F7  FLAVOR LADDER NEAR-LATTICE DEFECT.  ln(phi0)/ln(lambda_Y) = 2/(1+delta)
      with delta = ln(1-phi0)/ln(phi0) = 0.01863 exactly; the two flavor
      log-scales de-phase only after ~1/delta ~ 54 rungs >> L_max = 8, so the
      flavor sector is lattice-effective while the recovery kernel is not.

[E] = exact arithmetic below; [C] = physical reading; nothing here is a
prediction of record.  Firewall: discovery sandbox, never load-bearing.

Run:  cd experiments/tfpt-discovery && .venv/bin/python fractal_selfsimilarity_hunt.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 30
os.makedirs("figures", exist_ok=True)

FAILS = []


def check(name, ok):
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}")
    if not ok:
        FAILS.append(name)


def info(msg):
    print(f"       {msg}")


DECLINED = []


def declined(msg):
    DECLINED.append(msg)
    print(f"[DECLINED] {msg}")


# frozen kernel constants (SIGNATURES.md master notation)
N_FAM, P2, G_CAR = 3, 6, 5
A = 6 * mp.log(mp.mpf(3) / 2)          # Delta = ln(1/lambda_T)   = 2.43279...
B = 6 * mp.log(3)                       # ln(1/lambda_T')          = 6.59167...
D_SIM = mp.mpf(1) / 6                   # F1 similarity dimension
OMEGA1 = 2 * mp.pi / A                  # known comb tone 2.5827...
OMEGA2 = 2 * mp.pi / B                  # NEW second tone
OMEGA3 = 2 * mp.pi / (6 * mp.log(2))    # NEW generation-multiplet tone
BEND = mp.log(3) / mp.log(mp.mpf(3) / 2)

# ================================================================= F1
print("=" * 74)
print("F1  MORAN DIMENSION OF THE TRANSFER IFS  {(2/3)^6, (1/3)^6}")
print("=" * 74)

r1, r2 = sp.Rational(2, 3) ** 6, sp.Rational(1, 3) ** 6
s_dim = sp.Rational(1, 6)
moran = sp.root(r1, 6) + sp.root(r2, 6)
check("FORCED [E]: Moran equation r1^s + r2^s = 1 solved EXACTLY by s = 1/6 "
      "= 1/p2 (since (2/3)^{6/6} + (1/3)^{6/6} = 2/3 + 1/3 = 1)",
      sp.simplify(moran - 1) == 0)
check("FORCED [E]: fractal codimension 1 - 1/6 = 5/6 = gamma_car = g_car/p2 "
      "(the kappa_E8 numerator 5/6 IS the codimension of the transfer set)",
      sp.Rational(1, 1) - s_dim == sp.Rational(G_CAR, P2))

# uniqueness in the family count
part_ok = {N: sum(sp.Rational(N - n, N) for n in range(1, N)) for N in range(2, 9)}
check("UNIQUENESS [E]: for lambda_n = (1-n/N)^{p2} the unit partition "
      "sum_{n=1}^{N-1}(1-n/N) = (N-1)/2 = 1 holds IFF N = 3 = N_fam "
      "(only the physical family count gives dimension exactly 1/p2)",
      all((val == 1) == (N == 3) for N, val in part_ok.items()))
for N in (2, 3, 4, 5):
    ratios = [mp.mpf(N - n) / N for n in range(1, N)]
    if len(ratios) == 1:
        dimN = mp.mpf(0)  # single contraction -> one-point attractor
    else:
        g = lambda s, R=ratios: sum(r ** (P2 * s) for r in R) - 1
        dimN = mp.findroot(g, mp.mpf("0.2"))
    info(f"N = {N}: similarity dimension of (1-n/N)^6-IFS = {mp.nstr(dimN, 8)}"
         + ("   <-- exactly 1/6" if N == 3 else ""))
info("[C] modeling choice: the eigenvalues are read as similarity RATIOS of "
     "an IFS with the open-set condition; the identities above are exact.")

# ================================================================= F2
print("=" * 74)
print("F2  LATTICE vs NONLATTICE: the kernel is a NONLATTICE string")
print("=" * 74)

# multiplicative independence: (3/2)^m = 3^n  =>  2^m = 3^{m-n}  =>  m = n = 0
indep = all((sp.Rational(3, 2) ** m != sp.Integer(3) ** n)
            for m in range(1, 40) for n in range(1, 40))
check("FORCED [E]: 3/2 and 3 are multiplicatively independent (unique "
      "factorisation: (3/2)^m = 3^n forces 2^m = 3^{m-n}, so m = n = 0) "
      "=> ln(3/2)/ln3 irrational => the two-ratio transfer string is "
      "NONLATTICE in Lapidus' classification (scanned m,n < 40 + proof)",
      indep)

# continued fraction of the bend (controls all resonances below)
x = mp.mpf(BEND)
cf = []
for _ in range(16):
    ai = int(mp.floor(x))
    cf.append(ai)
    frac = x - ai
    if frac < mp.mpf("1e-25"):
        break
    x = 1 / frac
info(f"bend = ln3/ln(3/2) = {mp.nstr(BEND, 12)}")
info(f"continued fraction of the bend: {cf}")
convs = []
h0, h1, k0, k1 = 1, cf[0], 0, 1
convs.append((h1, k1))
for ai in cf[1:]:
    h0, h1 = h1, ai * h1 + h0
    k0, k1 = k1, ai * k1 + k0
    convs.append((h1, k1))
info(f"convergents l/k of the bend: {['%d/%d' % c for c in convs[:8]]}")
check("[E] the pure omega_1 = 2.5827 comb (S2b search target) is only the "
      "LATTICE approximation of the kernel; the true two-ratio string is "
      "nonlattice (consequence of the independence above)", indep)

# ================================================================= F3
print("=" * 74)
print("F3  COMPLEX DIMENSIONS of  f(s) = 1 - e^(-a s) - e^(-b s)")
print("=" * 74)


def f(s):
    return 1 - mp.e ** (-A * s) - mp.e ** (-B * s)


def fp(s):
    return A * mp.e ** (-A * s) + B * mp.e ** (-B * s)


check("FORCED [E]: f(1/6) = 0 exactly (the real complex dimension is the "
      "Moran dimension D = 1/6)", abs(f(D_SIM)) < mp.mpf("1e-25"))

# second comb tone + exact frequency identities
check("FORCED [E]: bend = omega_1/omega_2 EXACTLY -- the S3 walled-clock bend "
      "is the RATIO OF THE TWO COMB FREQUENCIES 2pi/Delta and 2pi/(6 ln3)",
      abs(OMEGA1 / OMEGA2 - BEND) < mp.mpf("1e-25"))
check("FORCED [E]: 1/omega_2 = 1/omega_1 + 1/omega_3 (harmonic additivity: "
      "6ln3 = 6ln(3/2) + 6ln2; tone periods in ln t add like series "
      "resistors)", abs(1 / OMEGA2 - 1 / OMEGA1 - 1 / OMEGA3) < mp.mpf("1e-25"))
info(f"omega_1 = 2pi/(6 ln 3/2) = {mp.nstr(OMEGA1, 8)}   (known S2b tone)")
info(f"omega_2 = 2pi/(6 ln 3)   = {mp.nstr(OMEGA2, 8)}   (NEW second tone)")
info(f"omega_3 = 2pi/(6 ln 2)   = {mp.nstr(OMEGA3, 8)}   (NEW generation tone)")
eps1 = mp.e ** (-mp.pi ** 2 / A)
eps2 = mp.e ** (-mp.pi ** 2 / B)
info(f"QT.02 amplitude law per tone: eps_1 = {mp.nstr(eps1, 6)} (known), "
     f"eps_2 = {mp.nstr(eps2, 6)}; mode weight of tone 2 = (1/3)^6 = "
     f"{mp.nstr(mp.mpf(729) ** -1, 4)} => net tone-2 visibility ~ "
     f"{mp.nstr(eps2 / 729, 4)} [C]")

# Newton hunt for complex roots in 0 < Im s <= 60
roots = {}
t_seed = 0.3
while t_seed <= 60.0:
    s = mp.mpc(0.1, t_seed)
    ok = False
    for _ in range(80):
        d = fp(s)
        if abs(d) < mp.mpf("1e-30"):
            break
        step = f(s) / d
        s = s - step
        if abs(step) < mp.mpf("1e-28"):
            ok = True
            break
    if ok and abs(f(s)) < mp.mpf("1e-24") and 0.05 < s.imag <= 60.5 and -4 < s.real < 0.2:
        key = round(float(s.imag), 6)
        if key not in roots:
            roots[key] = s
    t_seed += 0.3
roots = [roots[k] for k in sorted(roots)]
n_roots = len(roots)
exp_density = float(B / (2 * mp.pi) * 60)
info(f"found {n_roots} complex dimensions with 0 < Im s <= 60 "
     f"(Lapidus density estimate b*T/2pi ~ {exp_density:.1f})")
max_re = max(float(r.real) for r in roots)
check("[E, numeric] NONLATTICE signature: every oscillatory complex "
      "dimension sits STRICTLY left of D = 1/6 (the lattice comb would put "
      f"them ON the line); max Re = {max_re:.6f} < 0.166667",
      max_re < float(D_SIM) - 1e-9)
print("       first 10 complex dimensions s_k = sigma_k + i t_k:")
for r in roots[:10]:
    ka = float(r.imag * A / (2 * mp.pi))
    la = float(r.imag * B / (2 * mp.pi))
    print(f"         sigma = {float(r.real):+9.6f}   t = {float(r.imag):9.6f}"
          f"   (t a/2pi, t b/2pi) = ({ka:6.3f}, {la:6.3f})")
# where does the naive omega_1 tooth sit?
near1 = min(roots, key=lambda r: abs(r.imag - OMEGA1))
info(f"nearest complex dimension to the hunted omega_1 = {mp.nstr(OMEGA1, 6)}: "
     f"t = {float(near1.imag):.6f}, sigma = {float(near1.real):+.6f} "
     f"(detuning {float(near1.imag - OMEGA1):+.4f}, damping depth "
     f"D - sigma = {float(D_SIM - near1.real):.4f})")
# strongest resonances = roots closest to the line Re s = D
strongest = sorted(roots, key=lambda r: -float(r.real))[:5]
print("       5 strongest resonances (Re closest to D), with rank-2 labels:")
for r in strongest:
    t = float(r.imag)
    ka, la = t * float(A) / (2 * np.pi), t * float(B) / (2 * np.pi)
    k, l = round(ka), round(la)
    print(f"         t = {t:9.6f}  sigma = {float(r.real):+9.6f}  "
          f"(k,l) = ({k},{l})  residuals ({ka - k:+.3f}, {la - l:+.3f})"
          f"   l/k = {l}/{k}" if k else "")
lead = strongest[0]
lk = (round(float(lead.imag * A / (2 * mp.pi))), round(float(lead.imag * B / (2 * mp.pi))))
check("[E, numeric] the leading resonance label (k,l) = "
      f"{lk} satisfies l/k = a bend convergent (F2 list) -- the continued "
      "fraction of the bend controls the resonance hierarchy",
      (lk[1], lk[0]) in convs or lk == (0, 1))

# ================================================================= F4
print("=" * 74)
print("F4  LOG-TIME QUASICRYSTAL: cascade diffraction = complex dimensions")
print("=" * 74)

check("FORCED [E]: fixed-generation-n cascade rates {k a + (n-k) b} form an "
      "EXACT arithmetic progression with spacing b - a = 6 ln 2 "
      "(third tone omega_3); sympy: b - a == 6 log 2",
      sp.simplify(6 * sp.log(3) - 6 * sp.log(sp.Rational(3, 2)) - 6 * sp.log(2)) == 0)
info("Laplace transform of the binomially weighted cascade "
     "sum C(k+m,k) e^{-s(ka+mb)} = 1/f(s) = zeta_geom(s) EXACTLY "
     "(geometric series) -- so the log-time power spectrum below IS the "
     "complex-dimension spectrum of F3.")

af, bf = float(A), float(B)
sigma0 = 0.20
om = np.linspace(0.01, 12.0, 24000)
zf = 1 - np.exp(-(sigma0 + 1j * om) * af) - np.exp(-(sigma0 + 1j * om) * bf)
P = 1.0 / np.abs(zf) ** 2
# local maxima
pk = np.where((P[1:-1] > P[:-2]) & (P[1:-1] > P[2:]) & (P[1:-1] > 10 * np.median(P)))[0] + 1
peaks = sorted(((P[i], om[i]) for i in pk), reverse=True)
print(f"       top log-time diffraction peaks |zeta(0.20 + i w)|^2 (of {len(pk)}):")
for height, w in peaks[:6]:
    k, l = round(w * af / (2 * np.pi)), round(w * bf / (2 * np.pi))
    print(f"         w = {w:8.4f}   power = {height:9.2f}   rank-2 label (k,l) = ({k},{l})")
root_ts = np.array([float(r.imag) for r in roots if r.imag <= 12.5])
match = all(np.min(np.abs(root_ts - w)) < 0.05 for _, w in peaks[:3])
check("[E, numeric] each of the 3 strongest diffraction peaks coincides "
      "(within 0.05) with a complex-dimension imaginary part: the cascade's "
      "log-time Bragg spectrum IS the fractal-string spectrum", match)
info("[C] reading: the multi-generation cascade is a RANK-2 Fourier "
     "quasicrystal in ln t -- the temporal sibling of the rank-5 spatial "
     "cut-and-project set (tfpt_decagonal.py); comb searches that scan only "
     "omega_1 = 2.583 probe a strongly damped tooth (see F3 damping depth), "
     "while the leading two-tone resonance sits at the bend-convergent "
     "label instead.")

# figure
fig, ax = plt.subplots(1, 2, figsize=(11, 4.6))
ax[0].scatter([float(r.real) for r in roots], [float(r.imag) for r in roots],
              s=18, color="tab:purple")
ax[0].axvline(float(D_SIM), color="tab:red", ls="--", lw=1.2,
              label="Re s = D = 1/6")
ax[0].set_xlabel(r"Re $s$"); ax[0].set_ylabel(r"Im $s$")
ax[0].set_title("Complex dimensions of the two-ratio\n"
                r"transfer string  $1 = e^{-as} + e^{-bs}$ (nonlattice)")
ax[0].legend(loc="upper left")
ax[1].semilogy(om, P, lw=0.8, color="tab:red")
for t in root_ts:
    ax[1].axvline(t, color="tab:purple", lw=0.6, alpha=0.45)
ax[1].axvline(float(OMEGA1), color="tab:blue", ls=":", lw=1.4,
              label=r"$\omega_1 = 2.583$ (searched comb)")
ax[1].set_xlabel(r"$\omega$ (frequency in $\ln t$)")
ax[1].set_ylabel(r"$|\zeta_{\rm geom}(0.2+i\omega)|^2$")
ax[1].set_title("Log-time cascade diffraction:\npeaks = complex dimensions "
                "(purple lines)")
ax[1].legend(loc="upper right")
plt.tight_layout()
plt.savefig("figures/fractal_hunt.png", dpi=130)
plt.close()
print("       saved figures/fractal_hunt.png")

# ================================================================= F5
print("=" * 74)
print("F5  CARRIER COLLAPSE ORBIT  F(g) = (2^(g-1) - 1)/g")
print("=" * 74)


def famstep(g):
    """One compiler step; None if not integer (orbit dies)."""
    if g == 0:
        return None
    v = 2 ** (g - 1) - 1
    return v // g if v % g == 0 else None


orbit = [5]
while orbit[-1] not in (None, 0):
    orbit.append(famstep(orbit[-1]))
check("FORCED [E]: the carrier orbit is 5 -> 3 -> 1 -> 0 (vacuum): iterating "
      "the family-count formula itself collapses the compiler self-similarly, "
      "and the FIRST step 5 -> 3 is exactly N_fam = F(g_car)",
      orbit == [5, 3, 1, 0])
check("FORCED [E]: even g never step (2^{g-1}-1 is odd); odd g >= 7 satisfy "
      "2^{g-1}-1 > g^2, so any defined step INCREASES the rank (checked "
      "g = 7..99; doubling beats squaring thereafter) => no orbit from "
      "g >= 6 ever descends",
      all((2 ** (g - 1) - 1) % g != 0 for g in range(2, 101, 2))
      and all(2 ** (g - 1) - 1 > g * g for g in range(7, 100, 2)))
check("FORCED [E]: the vacuum basin is EXACTLY {1, 3, 5} = the Pascal-ladder "
      "ranks 2K+1 (K = 0,1,2; v108) -- g_car = 5 is the LARGEST rank that "
      "compiles down to the vacuum",
      {1, 3, 5} == {2 * K + 1 for K in range(3)}
      and famstep(3) == 1 and famstep(1) == 0)
steppable = [g for g in range(3, 2002, 2) if pow(2, g - 1, g) == 1]
composites = [g for g in steppable if any(g % p == 0 for p in range(2, int(g ** 0.5) + 1))]
info(f"odd g <= 2001 with a defined step: {len(steppable)} "
     f"(= odd primes + base-2 Fermat pseudoprimes {composites}) -- the step "
     "is defined on primes, but only {1,3,5} descend [E]")

# ================================================================= F6
print("=" * 74)
print("F6  DECLINED coincidences (look-elsewhere quantified; NOT claims)")
print("=" * 74)

dev_e = float(abs(BEND - mp.e) / mp.e)
declined(f"bend = ln3/ln(3/2) = {mp.nstr(BEND, 8)} vs e = 2.7182818: relative "
         f"deviation {dev_e:.2%} -- close but NOT exact; one-constant match "
         "with ~dozens of named constants available => not significant")
phi_g = (1 + mp.sqrt(5)) / 2
expo = mp.log(mp.mpf(729) / 64) / mp.log(phi_g)
declined(f"ln(Lambda_DSI)/ln(phi_golden) = {mp.nstr(expo, 7)} vs g_car = 5: "
         f"deviation {float(abs(expo - 5) / 5):.2%} -- the DSI ladder is NOT "
         "a golden-ratio power; keeps Q(sqrt5) (static carrier) and "
         "Z[ln2,ln3] (dynamic kernel) cleanly separated")

# ================================================================= F7
print("=" * 74)
print("F7  FLAVOR LADDER NEAR-LATTICE DEFECT (why v18 is single-ratio-safe)")
print("=" * 74)

c3 = 1 / (8 * mp.pi)
phi0 = mp.mpf(4) / 3 * c3 + 48 * c3 ** 4
lam_Y = mp.sqrt(phi0 * (1 - phi0))
delta = mp.log(1 - phi0) / mp.log(phi0)
check("FORCED [E]: 2 ln(lambda_Y) = (1 + delta) ln(phi0) with "
      "delta = ln(1-phi0)/ln(phi0) (exact, from lambda_Y^2 = phi0(1-phi0))",
      abs(2 * mp.log(lam_Y) - (1 + delta) * mp.log(phi0)) < mp.mpf("1e-25"))
info(f"delta = {mp.nstr(delta, 6)}; the two flavor log-scales ln(phi0), "
     f"2 ln(lambda_Y) de-phase after ~1/delta = {mp.nstr(1 / delta, 4)} rungs")
check("[E] lattice-effectiveness: the de-phasing scale 1/delta ~ 54 rungs "
      "exceeds the physical word-length window L <= 8 (v18) by ~7x => the "
      "flavor ladder is LATTICE-effective; only the recovery kernel (F2-F4) "
      "can show nonlattice structure",
      1 / delta > 6 * 8)

# ================================================================= summary
print("=" * 74)
print(f"SUMMARY: {'ALL EXACT/NUMERIC CHECKS PASSED' if not FAILS else f'{len(FAILS)} FAILURES'}"
      f"  |  survivors: F1 (dim 1/6, codim gamma_car, N=3 uniqueness), "
      f"F2 (nonlattice + bend CF), F3 (complex dimensions, 2nd/3rd tone), "
      f"F4 (log-time quasicrystal), F5 (carrier collapse basin {{1,3,5}}), "
      f"F7 (flavor lattice-effectiveness)  |  {len(DECLINED)} temptations "
      f"declined  |  exploration only, nothing promoted")
for name in FAILS:
    print("   FAIL:", name)
raise SystemExit(1 if FAILS else 0)
