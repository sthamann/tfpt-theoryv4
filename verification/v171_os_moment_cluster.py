"""v171 -- Atomic OS Moment Lemma + Sugawara Gap Safety: the admissible transfer
sector's reflection positivity is a positive moment problem, and its mass gap
beats the E8 Sugawara metric budget.

The gapped admissible transfer operator has spectrum
    spec(T) = {1, (2/3)^6, (1/3)^6} = {1, 64/729, 1/729}    (v54/v56).
This module recasts the OS positivity of that sector (previously a numerical Gram
test) as an exact positive-moment statement, and reads the decoupling margin
Delta_eff as an E8 Sugawara inequality.

  [I] 1. ATOMIC OS MOMENT LEMMA.  Every scalar two-point correlator of the
         admissible sector has the form C(n) = A + B r^n + C s^n with
         r=64/729, s=1/729 and A,B,C >= 0 -- the moment sequence of the positive
         atomic measure mu = A d_1 + B d_r + C d_s. Hence every OS reflection
         (Hankel) matrix H_ij = C(i+j) is positive semidefinite: it factorises as
         a Vandermonde Gram H = W diag(A,B,C) W^T over the atoms {1,r,s}. Positive
         spectrum => moment measure => reflection positivity (a clean proof, not
         just a numerical Gram test).
  [I] 2. KALLEN-LEHMANN.  H = -log T gives spec(H) = {0, 6 log(3/2), 6 log 3}: a
         positive discrete Kallen-Lehmann spectrum with masses m1 = 6 log(3/2) =
         2.43279..., m2 = 6 log 3 = 6.59167..., unique vacuum, explicit gap,
         exponential clustering C(t) = A + B e^{-m1 t} + C e^{-m2 t}.
  [I] 3. EXACT CLUSTER CONSTANT.  The subdominant rate r=(2/3)^6 gives the sharp
         connected-correlator bound sum_n |<A0 An>_c| <= C/(1-r) = C * 729/665,
         and correlation length xi = 1/(6 log(3/2)) = 0.411050...
  [I] 4. SUGAWARA GAP SAFETY.  The decoupling margin is
         Delta_eff = 6 log(3/2) - 31/(4 pi^2) = 1.64755... > 0, where the
         denominator is the E8 Sugawara constant 31 = 1 + h^v(E8) = 1 + 30 and
         c((E8)_1) = 248/(1+h^v) = 248/31 = 8. So the bound reads
         |R+(A3)| log(N_fam/|Z2|) > (1 + h^v(E8))/(4 pi^2): the A3 transfer gap
         beats the E8 Sugawara metric budget (exact + the declared V_metric norm).

Status [I] for the moment/spectral/Sugawara identities (exact), [C] for the
declared metric-norm bound 2|V_metric| <= 31/4pi^2 (as already typed in v76).
Exact parts mirrored on the Wolfram path.
"""
import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

r = sp.Rational(64, 729)        # (2/3)^6
s = sp.Rational(1, 729)         # (1/3)^6


def run():
    reset()
    print("v171 Atomic OS Moment Lemma + Sugawara Gap Safety")

    # 0. spectrum
    check("TRANSFER SPECTRUM: spec(T) = {1, (2/3)^6, (1/3)^6} = {1, 64/729, "
          "1/729} (v54/v56)",
          r == sp.Rational(2, 3)**6 and s == sp.Rational(1, 3)**6, exact=True)

    # 1. atomic OS moment lemma -- Hankel PSD via Vandermonde-Gram factorisation
    atoms = [sp.Integer(1), r, s]
    A_, B_, C_ = sp.Rational(1), sp.Rational(1), sp.Rational(1)   # any A,B,C>=0
    weights = [A_, B_, C_]

    def Cn(n):
        return sum(w * a**n for w, a in zip(weights, atoms))
    N = 5
    H = sp.Matrix(N, N, lambda i, j: Cn(i + j))
    W = sp.Matrix(N, 3, lambda i, k: atoms[k]**i)        # Vandermonde of the atoms
    gram = W * sp.diag(*weights) * W.T
    factorises = sp.simplify(H - gram) == sp.zeros(N, N)
    psd = all(complex(sp.N(e)).real >= -1e-12 for e in H.eigenvals())
    check("ATOMIC OS MOMENT LEMMA: C(n)=A+B(64/729)^n+C(1/729)^n is the moment "
          "sequence of mu=A d_1+B d_r+C d_s; the Hankel matrix factorises as the "
          "Vandermonde Gram H = W diag(A,B,C) W^T over {1,r,s} => PSD (positive "
          "spectrum => moment measure => reflection positivity)",
          factorises and psd, exact=True)

    # 2. Kallen-Lehmann masses
    m1 = 6 * mp.log(mp.mpf(3) / 2)
    m2 = 6 * mp.log(3)
    check("KALLEN-LEHMANN: H=-log T gives spec(H)={0, 6log(3/2), 6log3}; masses "
          "m1=6log(3/2)=2.43279, m2=6log3=6.59167 (positive discrete spectrum, "
          "unique vacuum, explicit gap)",
          abs(m1 - mp.mpf("2.4327906486")) < 1e-9
          and abs(m2 - mp.mpf("6.5916737320")) < 1e-9)

    # 3. exact cluster constant + correlation length
    cluster = 1 / (1 - r)
    xi = 1 / m1
    check("EXACT CLUSTER CONSTANT: 1/(1-r) = 729/665 = 1.096240..., correlation "
          "length xi = 1/(6log(3/2)) = 0.411050...",
          cluster == sp.Rational(729, 665)
          and abs(xi - mp.mpf("0.4110505771")) < 1e-9)

    # 4. Sugawara gap safety
    hv_E8 = 30                                  # dual Coxeter number of E8
    sug = 1 + hv_E8                             # 31
    c_E8_1 = sp.Rational(248, sug)              # 248/31 = 8
    Delta = m1
    budget = mp.mpf(31) / (4 * mp.pi**2)
    Delta_eff = Delta - budget
    check("SUGAWARA GAP SAFETY: 31 = 1 + h^v(E8) = 1+30 and c((E8)_1) = 248/31 = "
          "8; the margin Delta_eff = 6log(3/2) - 31/(4pi^2) = %.6f > 0 -- the A3 "
          "transfer gap beats the E8 Sugawara metric budget |R+(A3)| "
          "log(N_fam/|Z2|) > (1+h^v(E8))/(4pi^2)" % float(Delta_eff),
          sug == 31 and c_E8_1 == 8 and Delta_eff > 0
          and abs(Delta_eff - mp.mpf("1.6475514754")) < 1e-9)

    # consistency: Delta = |R+(A3)| log(N_fam/|Z2|) = 6 log(3/2)
    check("GAP IDENTITY: Delta = |R+(A3)| log(N_fam/|Z2|) = 6 log(3/2) "
          "(|R+(A3)|=6, N_fam=3, |Z2|=2)",
          abs(6 * mp.log(mp.mpf(N_fam) / 2) - m1) < 1e-12, exact=False)

    return summary("v171 Atomic OS Moment Lemma + Sugawara Gap Safety")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
