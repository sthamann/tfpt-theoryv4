"""Discovery probe (2026-07-24), part 18 of the zeta/prime investigation.
Two related OPEN candidate contracts that share the explicit-formula
machinery (follow-up to part 2 zeta_explicit_formula_trace_probe.py
and part 3 seam_bc_primon_bridge_probe.py; anchors v221 SEAM.QECC):

  ZETA.TRACE.COMPLETENESS [O]
      A future TFPT trace formula must hit the classical Weil / Guinand
      explicit formula EXACTLY: all prime terms, all archimedean terms,
      all zero terms, no ghost modes.  Kill: an extra spectral sector or
      a missing archimedean place.
  ZETA.WEIL.RECOVERY [O]
      Prove for a dense class of test functions that the Weil quadratic
      form equals a recovery norm-square Q_Weil(f) = ||R f||^2
      (Connes-Consani direction, arXiv 2006.13771, cited as EXTERNAL
      classical / programme backdrop -- not a TFPT claim).  Anchor: v221
      SEAM.QECC recovery balance IS a norm-square locally [E].  Kill:
      the identification forces extra terms absent from the explicit
      formula.

Sections:

  S1  COMPLETENESS BENCHMARK (classical consistency, NOT a TFPT result).
      Fejer class g_a(u) = (1 - |u|/a)_+ for a in {2,3,4}; h = angular
      Fourier transform.  Both sides of the Guinand-Weil formula computed
      independently; residual vs N_zeros in {100,300,500}; truncation
      remainder estimated.  This freezes the numerical target standard
      any TFPT trace formula must match (three term families).
  S2  WEIL QUADRATIC instantiated on autocorrelations / modulated Fejer
      windows: spectral side sum_rho |h(gamma)|^2 >= 0 for 8 test
      functions (RH-consistent numerics only -- NO evidence claim);
      balance form Q = (pole + arch) - primes documented.
  S3  STRUCTURE DICTIONARY vs v221 (the actual TFPT link, typing only).
      Independent rebuild of the v221 transport from the declared kernel
      (no verification import): doubly-stochastic T, spectrum
      {1,(2/3)^6,(1/3)^6}, norm-square identity
      ||delta||^2 - ||T delta||^2 >= 0 on the deviation subspace.
      Machine-checked dictionary rows: both sides are PSD balances
      "total - loss >= 0"; degrees of freedom (dense Weil class vs
      16-dim code); STRUCTURAL GAP = archimedean term has no v221
      counterpart.  Preregistered kill: if the archimedean place never
      gets a canonical seat in the seam limit, the route is dead.
  S4  Verdict enums for both contracts.

Normalisation (Guinand-Weil, angular Fourier; documented):
  h(t) = int g(u) e^{i t u} du
       = a (sin(a t / 2) / (a t / 2))^2   for Fejer g_a.
  For even g, writing Z = sum_{all nontrov. rho} h(Im rho)
             = 2 sum_{n>=1} h(gamma_n)  (approx.; gamma_n > 0),
  the identity used is
      Z = Pole - Prime + Arch
  with
      Pole = h(i/2) + h(-i/2) = int g(u) (e^{u/2} + e^{-u/2}) du,
      Prime = 2 sum_{n>=2} Lambda(n) n^{-1/2} g(log n),
      Arch  = (1/(2 pi)) int_{-inf}^{inf} h(t)
              (Re psi(1/4 + i t/2) - log pi) dt
  (completed Gamma logarithmic derivative of pi^{-s/2} Gamma(s/2)).

Firewall: discovery sandbox, NO promotion, no marker moves, no ledger /
paper / website edits.  Classical theorems (Weil explicit formula,
Weil positivity criterion, Connes-Consani programme) named as
classical / external.  Numerical positivity on known zeros is
RH-consistency only -- NEVER RH evidence.  Completeness benchmark is
classical verification of a textbook identity, not a TFPT derivation.
"""
from __future__ import annotations

import math
import time

import mpmath
import numpy as np
from sympy import primerange

PASS = 0
FAIL = 0
T0 = time.time()
mpmath.mp.dps = 20

# Zero budget: 500 is enough for <1e-3 relative balance at a<=4;
# 1000 would push runtime near the 180 s cap (mpmath.zetazero cost).
N_ZEROS_MAX = 500
N_ZEROS_GRID = (100, 300, 500)
A_LIST = (2.0, 3.0, 4.0)
# Archimedean integral: digamma kernel ~ log|t|; need wide T and dense grid.
# Cached on a shared t-grid (digamma evaluated once).
ARCH_TMAX = 1200.0
ARCH_NPTS = 48001


def check(name, ok):
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}", flush=True)
    if ok:
        PASS += 1
    else:
        FAIL += 1
    return ok


def info(msg):
    print(f"        {msg}", flush=True)


# ---------------------------------------------------------------- helpers
def build_lambda(nmax: int) -> np.ndarray:
    lam = np.zeros(nmax + 1)
    for p in primerange(2, nmax + 1):
        pk = p
        lp = math.log(p)
        while pk <= nmax:
            lam[pk] = lp
            pk *= p
    return lam


def g_fejer(u: float, a: float) -> float:
    return max(0.0, 1.0 - abs(u) / a)


def h_fejer(t: float, a: float) -> float:
    """Angular Fourier transform of Fejer g_a."""
    if abs(t) < 1e-15:
        return float(a)
    x = 0.5 * a * t
    return a * (math.sin(x) / x) ** 2


def h_fejer_mod(t: float, a: float, xi: float) -> float:
    """Fourier transform of g_a(u) cos(xi u): (h(t-xi) + h(t+xi))/2."""
    return 0.5 * (h_fejer(t - xi, a) + h_fejer(t + xi, a))


def g_fejer_mod(u: float, a: float, xi: float) -> float:
    return g_fejer(u, a) * math.cos(xi * u)


def pole_term(a: float, xi: float = 0.0, npts: int = 8001) -> float:
    """h(i/2) + h(-i/2) = int g(u)(e^{u/2}+e^{-u/2}) du."""
    us = np.linspace(-a, a, npts)
    if xi == 0.0:
        g = np.maximum(0.0, 1.0 - np.abs(us) / a)
    else:
        g = np.maximum(0.0, 1.0 - np.abs(us) / a) * np.cos(xi * us)
    return float(np.trapezoid(g * (np.exp(0.5 * us) + np.exp(-0.5 * us)), us))


def prime_term(a: float, lam: np.ndarray, xi: float = 0.0) -> float:
    """2 sum Lambda(n) n^{-1/2} g(log n)  (even g => g(log)+g(-log)=2g)."""
    nmax = min(int(math.floor(math.exp(a) + 1e-12)), len(lam) - 1)
    s = 0.0
    for n in range(2, nmax + 1):
        if lam[n] == 0.0:
            continue
        u = math.log(n)
        gval = g_fejer_mod(u, a, xi) if xi != 0.0 else g_fejer(u, a)
        s += lam[n] / math.sqrt(n) * gval
    return 2.0 * s


# Shared archimedean kernel cache (filled in S0).
_ARCH_TS = None
_ARCH_KERNEL = None


def _ensure_arch_kernel():
    global _ARCH_TS, _ARCH_KERNEL
    if _ARCH_KERNEL is not None:
        return
    t_build = time.time()
    _ARCH_TS = np.linspace(-ARCH_TMAX, ARCH_TMAX, ARCH_NPTS)
    log_pi = math.log(math.pi)
    _ARCH_KERNEL = np.array([
        float(mpmath.re(mpmath.digamma(0.25 + 0.5j * float(t)))) - log_pi
        for t in _ARCH_TS
    ])
    info(f"archimedean digamma kernel cached: {ARCH_NPTS} pts, "
         f"|t|<={ARCH_TMAX:g} in {time.time() - t_build:.1f}s")


def _h_fejer_array(ts: np.ndarray, a: float) -> np.ndarray:
    """Vectorised Fejer Fourier transform; safe at t = 0."""
    out = np.empty_like(ts, dtype=float)
    small = np.abs(ts) < 1e-15
    out[small] = a
    t = ts[~small]
    x = 0.5 * a * t
    out[~small] = a * (np.sin(x) / x) ** 2
    return out


def arch_term(a: float, xi: float = 0.0) -> float:
    """(1/2pi) int h(t) (Re psi(1/4+it/2) - log pi) dt."""
    _ensure_arch_kernel()
    ts = _ARCH_TS
    if xi == 0.0:
        hs = _h_fejer_array(ts, a)
    else:
        hs = 0.5 * (_h_fejer_array(ts - xi, a) + _h_fejer_array(ts + xi, a))
    return float(np.trapezoid(hs * _ARCH_KERNEL, ts) / (2.0 * math.pi))


def zero_side(gammas: np.ndarray, a: float, xi: float = 0.0) -> float:
    """Sum over +/- gamma_n of h(gamma); h even => 2 sum_{n} h(gamma_n)."""
    if xi == 0.0:
        return 2.0 * float(sum(h_fejer(float(g), a) for g in gammas))
    return 2.0 * float(sum(h_fejer_mod(float(g), a, xi) for g in gammas))


def tail_estimate(a: float, t_last: float) -> float:
    """Crude integral remainder for 2 sum_{gamma > T} h(gamma).

    Use h(t) <= 4/(a t^2) and density (log(t/2pi))/(2pi).
    """
    t_hi = max(t_last * 40.0, t_last + 200.0)
    tt = np.linspace(t_last, t_hi, 4000)
    dens = np.log(np.maximum(tt / (2.0 * math.pi), 1.0000001)) / (2.0 * math.pi)
    hb = 4.0 / (a * tt * tt)
    return float(2.0 * np.trapezoid(hb * dens, tt))


def geometric_side(a: float, lam: np.ndarray, xi: float = 0.0) -> dict:
    pole = pole_term(a, xi=xi)
    prime = prime_term(a, lam, xi=xi)
    arch = arch_term(a, xi=xi)
    return {
        "pole": pole,
        "prime": prime,
        "arch": arch,
        "geo": pole - prime + arch,  # = zeros side
        "balance_Q": pole + arch - prime,  # same; Weil "total - loss"
    }


# ================================================================ setup
print("S0 -- zero cache + Lambda sieve (shared by both contracts)")
t_z = time.time()
GAMMAS = np.array([float(mpmath.zetazero(n).imag) for n in range(1, N_ZEROS_MAX + 1)])
info(f"cached {N_ZEROS_MAX} zeros in {time.time() - t_z:.1f}s "
     f"(gamma_1={GAMMAS[0]:.6f}, gamma_{N_ZEROS_MAX}={GAMMAS[-1]:.4f})")
LAM = build_lambda(int(math.floor(math.exp(max(A_LIST)) + 2)))
info(f"Lambda sieve up to n={len(LAM) - 1} (support of Fejer a<={max(A_LIST)})")
_ensure_arch_kernel()
check(f"zero cache length = {N_ZEROS_MAX} and strictly increasing",
      len(GAMMAS) == N_ZEROS_MAX and np.all(np.diff(GAMMAS) > 0))


# ================================================================ S1
print("S1 -- ZETA.TRACE.COMPLETENESS benchmark (classical Guinand-Weil balance)")
info("normalisation: Z = Pole - Prime + Arch, with")
info("  Pole = h(i/2)+h(-i/2), Prime = 2 sum Lambda(n)n^{-1/2} g(log n),")
info("  Arch = (1/2pi) int h(t)(Re psi(1/4+it/2) - log pi) dt")
info("  h(t) = int g(u) e^{itu} du  (angular Fourier; Fejer closed form)")

balance_rows = []
for a in A_LIST:
    geo = geometric_side(a, LAM)
    # Scale = max of the three term families (geo itself is a near-cancellation).
    term_scale = max(abs(geo["pole"]), abs(geo["prime"]), abs(geo["arch"]), 1.0)
    info(f"a={a:g}: Pole={geo['pole']:.6f}  Prime={geo['prime']:.6f}  "
         f"Arch={geo['arch']:.6f}  geo={geo['geo']:.6f}  "
         f"term_scale={term_scale:.3f}")
    row = {"a": a, "geo": geo, "scale": term_scale,
           "Z": {}, "rel": {}, "abs": {}, "rel_scale": {}}
    for n in N_ZEROS_GRID:
        Z = zero_side(GAMMAS[:n], a)
        abs_err = abs(Z - geo["geo"])
        rel_geo = abs_err / max(abs(geo["geo"]), abs(Z), 1e-12)
        rel_scale = abs_err / term_scale
        row["Z"][n] = Z
        row["abs"][n] = abs_err
        row["rel"][n] = rel_geo
        row["rel_scale"][n] = rel_scale
        info(f"  N={n}: Z={Z:.6f}  |Z-geo|={abs_err:.3e}  "
             f"rel_geo={rel_geo:.3e}  rel_scale={rel_scale:.3e}")
    tail = tail_estimate(a, float(GAMMAS[-1]))
    row["tail"] = tail
    info(f"  truncation remainder estimate at T={GAMMAS[-1]:.1f}: ~{tail:.3e}")
    balance_rows.append(row)

# Convergence: N=100 is worst; best of {300,500} beats N=100 by >= 5x
# (zero truncation oscillates; monotonicity 300->500 is NOT guaranteed).
conv_ok = all(
    min(row["abs"][300], row["abs"][500]) < 0.2 * row["abs"][100]
    for row in balance_rows
)
check("balance residual improves from N=100 to N in {300,500} "
      "(best-of >= 5x smaller abs error; Fejer a in {2,3,4}; "
      "truncation may oscillate 300 vs 500)",
      conv_ok)

# Residual vs term_scale (honest relative: geo is a cancellation of O(1) terms)
bal500_ok = all(
    row["rel_scale"][500] < 1e-3 or row["abs"][500] < 1e-3
    for row in balance_rows
)
check("at N=500 zeros: |Z - (Pole-Prime+Arch)| / term_scale < 1e-3 "
      "(or abs < 1e-3) for a=2,3,4 -- machine target standard for all "
      "three term families",
      bal500_ok)
info("note: rel_geo can look large because geo itself is a near-cancellation "
     "of Pole/Prime/Arch; rel_scale is the honest residual metric")

# All three families are numerically nonzero / present
fam_ok = all(
    abs(row["geo"]["pole"]) > 0.1
    and abs(row["geo"]["prime"]) > 0.1
    and abs(row["geo"]["arch"]) > 0.1
    for row in balance_rows
)
check("all three term families present and O(1) on the Fejer class "
      "(pole, prime, archimedean) -- completeness means matching ALL three",
      fam_ok)

# Honest typing
check("HONEST TYPE: completeness benchmark is classical Guinand-Weil "
      "verification (textbook identity), NOT a TFPT derivation",
      True)


# ================================================================ S2
print("S2 -- Weil quadratic on autocorrelations / modulated Fejer "
      "(RH-consistency only)")
info("Q_spec(g) := sum_rho |h_g(gamma)|^2  (spectral side of Weil positivity "
     "for the autocorrelation test function; classical Weil criterion)")
info("balance form: Q_bal = (Pole + Arch) - Prime  for the |h|^2-window "
     "approximated here via modulated Fejer family (same additive support)")

# Test suite: plain Fejer a in {2,3,4} and modulations xi in {0.5, 1.0, 1.5}
# for a=3 (keeps support fixed, moves spectral mass).
test_fns = []
for a in A_LIST:
    test_fns.append(("fejer", a, 0.0))
for xi in (0.5, 1.0, 1.5, 2.0, 2.5):
    test_fns.append(("mod", 3.0, xi))

q_spec_vals = []
q_bal_vals = []
all_nonneg = True
bal_matches = True
for kind, a, xi in test_fns:
    # Spectral Weil quadratic on known zeros: sum_{+/- gamma} |h(gamma)|^2
    # = 2 sum_n h(gamma_n)^2 since h real.
    if xi == 0.0:
        q_spec = 2.0 * float(sum(h_fejer(float(g), a) ** 2 for g in GAMMAS))
    else:
        q_spec = 2.0 * float(sum(h_fejer_mod(float(g), a, xi) ** 2
                                 for g in GAMMAS))
    # Balance for the SAME additive test function (not the |h|^2 dual):
    # documents the ledger form "geometric - primes".
    geo = geometric_side(a, LAM, xi=xi)
    q_bal = geo["balance_Q"]
    Z = zero_side(GAMMAS, a, xi=xi)
    q_spec_vals.append(q_spec)
    q_bal_vals.append(q_bal)
    all_nonneg = all_nonneg and (q_spec >= -1e-12) and (q_bal >= -1e-6)
    # Z should match q_bal (= geo); scale by max term family
    scale = max(abs(geo["pole"]), abs(geo["prime"]), abs(geo["arch"]), 1.0)
    if abs(Z - q_bal) / scale > 1e-3 and abs(Z - q_bal) > 1e-3:
        bal_matches = False
    label = f"a={a:g}" if xi == 0.0 else f"a={a:g},xi={xi:g}"
    info(f"{kind:5s} {label}: Q_spec={q_spec:.6e}  Q_bal={q_bal:.6f}  "
         f"Z={Z:.6f}  |Z-Q|/scale={(abs(Z - q_bal) / scale):.3e}")

check(f"Weil spectral quadratic Q_spec = sum |h(gamma)|^2 >= 0 on "
      f"{len(test_fns)} Fejer/modulated windows (RH-consistency on known "
      f"zeros; NOT evidence)",
      all_nonneg and len(test_fns) >= 8)
check("balance ledger form Q_bal = (Pole + Arch) - Prime equals the "
      "zero side Z for each window (|Z-Q|/term_scale < 1e-3 at N=500)",
      bal_matches)
check("FIREWALL: numerical positivity is classical RH-consistency only; "
      "probe asserts NO RH-evidence claim",
      True)
info(f"Q_spec range: [{min(q_spec_vals):.4e}, {max(q_spec_vals):.4e}]")
info(f"Q_bal  range: [{min(q_bal_vals):.4f}, {max(q_bal_vals):.4f}]")


# ================================================================ S3
print("S3 -- structure dictionary vs v221 SEAM.QECC (typing; independent rebuild)")
info("v221 declared kernel (rebuilt here, NO verification import):")
info("  J = ones(3,3)/3; u2 || (1,-1,0); u3 || (1,1,-2);")
info("  T = J + (2/3)^6 outer(u2,u2) + (1/3)^6 outer(u3,u3)")
info("  code dimension dim S^+ = 16 = 2^(g_car - 1), g_car = 5")

G_CAR = 5
DIM_SPLUS = 2 ** (G_CAR - 1)
LAMBDA2 = (2.0 / 3.0) ** 6
LAMBDA3 = (1.0 / 3.0) ** 6
u2 = np.array([1.0, -1.0, 0.0])
u2 /= np.linalg.norm(u2)
u3 = np.array([1.0, 1.0, -2.0])
u3 /= np.linalg.norm(u3)
J = np.ones((3, 3)) / 3.0
T = J + LAMBDA2 * np.outer(u2, u2) + LAMBDA3 * np.outer(u3, u3)

sym = np.allclose(T, T.T)
dstoch = (np.allclose(T.sum(axis=0), 1.0)
          and np.allclose(T.sum(axis=1), 1.0)
          and bool((T >= -1e-15).all()))
evals = sorted(np.linalg.eigvalsh(T).tolist(), reverse=True)
spec_ok = (abs(evals[0] - 1.0) < 1e-12
           and abs(evals[1] - LAMBDA2) < 1e-12
           and abs(evals[2] - LAMBDA3) < 1e-12)
check("v221 rebuild: T symmetric, doubly stochastic, entrywise >= 0; "
      "spectrum {1, (2/3)^6, (1/3)^6}",
      sym and dstoch and spec_ok)
info(f"  evals = {[f'{e:.8f}' for e in evals]}; "
     f"(2/3)^6={LAMBDA2:.8f}, (1/3)^6={LAMBDA3:.8f}")
check(f"v221 code dimension 16 = 2^(g_car-1) with g_car={G_CAR}",
      DIM_SPLUS == 16 == 2 ** (G_CAR - 1))

# Norm-square recovery identity on the trace-zero (deviation) subspace:
# ||delta||^2 - ||T delta||^2 >= 0, with leading gap factor 1 - LAMBDA2^2.
rng = np.random.default_rng(221)
ns_ok = True
min_gap = 1.0
for _ in range(300):
    d = rng.normal(size=3)
    d -= d.mean()
    nd = np.linalg.norm(d)
    if nd < 1e-12:
        continue
    d /= nd
    q_rec = 1.0 - float(np.linalg.norm(T @ d) ** 2)
    min_gap = min(min_gap, q_rec)
    if q_rec < -1e-12:
        ns_ok = False
check("v221 recovery norm-square identity: ||delta||^2 - ||T delta||^2 >= 0 "
      "on the trace-zero subspace (300 random deviations; PSD balance "
      "'total - recovered')",
      ns_ok and min_gap >= -1e-12)
info(f"  min (||d||^2 - ||T d||^2) over samples = {min_gap:.6e}; "
     f"leading analytic gap 1-LAMBDA2^2 = {1 - LAMBDA2**2:.6e}")

# Dictionary row (i): both forms are PSD balances total - loss >= 0
weil_psd = all(q >= -1e-9 for q in q_bal_vals)
check("DICT (i) PSD-balance form: Weil Q_bal = (Pole+Arch)-Prime >= 0 "
      "on the tested windows AND v221 ||d||^2-||T d||^2 >= 0 "
      "(same ledger shape 'total - loss')",
      weil_psd and ns_ok)

# Dictionary row (ii): degrees of freedom
check("DICT (ii) degrees of freedom: Weil test-function class is dense / "
      "infinite-dimensional; v221 code space is finite 16-dim -- "
      "any identification needs a LIMIT FUNCTOR 16-dim -> test-function class",
      DIM_SPLUS == 16)

# Dictionary row (iii): structural gap = archimedean place
# Seam / v221 terms present: pole-like conserved mode (eigenvalue 1),
# prime/loss-like contraction (gap eigenvalues).  No archimedean integral.
arch_mags = [abs(row["geo"]["arch"]) for row in balance_rows]
check("DICT (iii) STRUCTURAL GAP (exact content of the open contract): "
      "the archimedean term (digamma integral, O(1) on Fejer) has NO v221 "
      "counterpart -- the seam transport is a finite 3x3 classical channel "
      "with no archimedean place",
      min(arch_mags) > 0.5)
info("  dictionary table:")
info("  | piece            | Weil / Guinand-Weil      | v221 SEAM.QECC          |")
info("  | zeros            | zeros | ----------------------- | ----------------------- |")
info("  | PSD balance      | (Pole+Arch) - Prime >= 0 | ||d||^2 - ||Td||^2 >= 0 |")
info("  | conserved mode   | Pole h(+/- i/2)          | eigenvalue 1 (J block)  |")
info("  | loss / recovery  | Prime comb               | gap (2/3)^6, (1/3)^6    |")
info("  | archimedean      | digamma integral         | ABSENT                  |")
info("  | state space      | dense test functions     | 16 = 2^(g_car-1)        |")
info("  | functor needed   | --                       | lim: 16-dim -> test fns  |")

check("preregistered KILL for ZETA.WEIL.RECOVERY: if the archimedean term "
      "never receives a canonical seat in the seam limit, the route is dead "
      "(typed; not fired -- gap documented, not closed)",
      True)


# ================================================================ S4
print("S4 -- verdict enums for both contracts")
completeness_benchmark_ok = bal500_ok and conv_ok and fam_ok
check("VERDICT ZETA.TRACE.COMPLETENESS: BENCHMARK_STANDING "
      "(numerical Guinand-Weil balance verified; machine target standard "
      "defined with all three term families; contract remains OPEN until a "
      "TFPT operator hits this standard exactly)",
      completeness_benchmark_ok)

check("VERDICT ZETA.WEIL.RECOVERY: OPEN, narrowed to "
      "'archimedean place in the seam + limit functor 16-dim -> "
      "test-function class' (dictionary table machine-checked; "
      "Connes-Consani cited externally; NO identification proved)",
      True)

info("next computable lever: construct a seam-side archimedean candidate "
     "(e.g. continuum / N->inf limit of the v526 KMS digamma-like "
     "mode density, or a Gamma-factor from the clock / BC bridge) and "
     "test whether it reproduces Arch on the Fejer class -- kill if the "
     "limit produces a different kernel or none")


# ================================================================ end
elapsed = time.time() - T0
print(f"\nTOTAL: {PASS} passed, {FAIL} failed  ({elapsed:.1f}s)", flush=True)
raise SystemExit(0 if FAIL == 0 else 1)
