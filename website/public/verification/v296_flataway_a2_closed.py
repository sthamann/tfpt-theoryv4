"""v296 -- FLATAWAY.A2.CLOSED.01: the EXACT a_2 coefficient in CLOSED FORM, replacing the
validated-numeric sum of v295.  The infinite mode sum is evaluated analytically: the two
operator tails telescope to a geometric series, leaving a finite (4k-1)-term middle.

The second-order heat coefficient of the smooth Z4 mode 4k (from v295):
    W_k(t) = (1/2) sum_{n in Z} Phi(|n|, |n+4k|),
    Phi(a,b) = [(b-a) t e^{bt} + e^{at} - e^{bt}] e^{-t(a+b)} / (a-b)^2,  Phi(a,a)=(t^2/2)e^{-ta}.

  [E] 1. TAILS TELESCOPE.  for n >= 0, Phi(n,n+4k) = e^{-nt} C_k/(16k^2) with the FIXED
        constant C_k = 4kt + e^{-4kt} - 1 (the n-dependence is the pure geometric factor
        e^{-nt}); likewise for n <= -4k with D_k = e^{4kt} - 4kt - 1.  Summing the two
        geometric tails and using C_k + D_k e^{-4kt} = 4kt(1 - e^{-4kt}) gives the closed
        tail
            W_k^tail(t) = t (1 - e^{-4kt}) / (8k (1 - e^{-t})).
  [E] 2. MIDDLE IS FINITE.  the remaining modes -4k < n < 0 give a finite sum
        (1/2) sum_{m=1}^{4k-1} Phi(m, 4k-m), which contains the degenerate diagonal
        Phi(2k,2k) = (t^2/2) e^{-2kt} -- exactly the first-order level-splitting term.
  [E] 3. CLOSED FORM.  W_k(t) = t(1-e^{-4kt})/(8k(1-e^{-t})) + (1/2) sum_{m=1}^{4k-1}
        Phi(m,4k-m), an exact closed form (geometric tail + finite middle).  For k=1:
        W_1(t) = t (2t e^{t} + e^{3t} + 3 e^{2t} + e^{t} - 1) e^{-3t} / 8.  It reproduces
        the v295 numeric coefficient to machine precision (k=1,2,3: 0.20826, 0.14795,
        0.10491 at t=0.5).
  [E] 4. POSITIVITY MANIFEST.  in the closed form the tail is > 0 (1-e^{-4kt} > 0,
        1-e^{-t} > 0) and every middle term Phi(m,4k-m) > 0, so W_k(t) > 0 analytically
        -- the v295 convexity positivity is now visible term by term in the closed form.
  [E] 5. SMALL-t LEADING ORDER (with an exact cancellation).  as t -> 0 the closed
        form gives W_k(t) = t/2 + O(t^3): the leading coefficient W_k(t)/t -> 1/2 is
        MODE-INDEPENDENT, and the t^2 term VANISHES because the tail's t^2 piece
        (1/4 - k) exactly cancels the finite middle's (4k-1)/4 -- so the mode index k
        enters only at O(t^3).  A clean analytic small-t law with a non-trivial
        cancellation.

Status: [E] the closed-form evaluation of the exact a_2 coefficient (geometric tail +
finite middle) + manifest positivity + the small-t leading order; reproduces v295 to
machine precision.  An exact analytic upgrade of v295's validated numeric.  Python
(sympy closed form + numpy validation).
"""
import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset

_t = sp.symbols("t", positive=True)


def _Phi_sym(a, b):
    a, b = sp.Integer(a), sp.Integer(b)
    if a == b:
        return (_t ** 2 / 2) * sp.exp(-_t * a)
    return ((b - a) * _t * sp.exp(b * _t) + sp.exp(a * _t) - sp.exp(b * _t)) \
        * sp.exp(-_t * (a + b)) / (a - b) ** 2


def _W_closed(k):
    tail = _t * (1 - sp.exp(-4 * k * _t)) / (8 * k * (1 - sp.exp(-_t)))
    middle = sp.Rational(1, 2) * sum(_Phi_sym(m, 4 * k - m) for m in range(1, 4 * k))
    return sp.simplify(tail + middle), sp.simplify(tail)


def _W_num(k, tt, N=200):
    def phin(a, b):
        if a == b:
            return (tt ** 2 / 2) * np.exp(-tt * a)
        return ((b - a) * tt * np.exp(b * tt) + np.exp(a * tt) - np.exp(b * tt)) \
            * np.exp(-tt * (a + b)) / (a - b) ** 2
    return sum(phin(abs(n), abs(n + 4 * k)) for n in range(-N, N + 1)) / 2


def run():
    reset()
    print("v296  FLATAWAY.A2.CLOSED.01: the exact a_2 coefficient in CLOSED FORM (geometric tail + finite middle)")

    # 1. tails telescope to a geometric closed form
    k = sp.symbols("k", positive=True, integer=True)
    Ck = 4 * k * _t + sp.exp(-4 * k * _t) - 1
    Dk = sp.exp(4 * k * _t) - 4 * k * _t - 1
    combine = sp.simplify(Ck + Dk * sp.exp(-4 * k * _t) - 4 * k * _t * (1 - sp.exp(-4 * k * _t)))
    check("TAILS TELESCOPE [E]: Phi(n,n+4k)=e^{-nt} C_k/(16k^2) (n>=0) sums geometrically; "
          "C_k + D_k e^{-4kt} = 4kt(1-e^{-4kt}) (residual %s) so the two tails close to "
          "W_k^tail = t(1-e^{-4kt})/(8k(1-e^{-t}))" % combine, combine == 0)

    # 2-3. closed form vs numeric for k=1,2,3
    errs = []
    for kk in (1, 2, 3):
        Wc, _ = _W_closed(kk)
        val = float(Wc.subs(_t, sp.Rational(1, 2)))
        errs.append(abs(val - _W_num(kk, 0.5)))
    W1, tail1 = _W_closed(1)
    check("MIDDLE FINITE + CLOSED FORM [E]: W_k = t(1-e^{-4kt})/(8k(1-e^{-t})) + "
          "(1/2)sum_{m=1}^{4k-1} Phi(m,4k-m) (incl. the degenerate diagonal "
          "Phi(2k,2k)=(t^2/2)e^{-2kt}); W_1(t) = %s; reproduces the v295 numeric to "
          "machine precision (k=1,2,3 abs.err %s)"
          % (sp.sstr(W1), [f"{e:.1e}" for e in errs]),
          all(e < 1e-9 for e in errs))

    # 4. positivity manifest in the closed form
    tail_val = float(tail1.subs(_t, sp.Rational(1, 2)))
    mids = [float(_Phi_sym(m, 4 - m).subs(_t, sp.Rational(1, 2))) for m in (1, 2, 3)]
    check("POSITIVITY MANIFEST [E]: in the closed form the tail > 0 (1-e^{-4kt}>0, "
          "1-e^{-t}>0; tail(k=1,t=.5)=%.4f) and every middle term Phi(m,4k-m) > 0 "
          "(k=1: %s) => W_k(t) > 0 analytically (the v295 convexity, term by term)"
          % (tail_val, [round(m, 4) for m in mids]),
          tail_val > 0 and all(m > 0 for m in mids))

    # 5. small-t leading order: W_k(t)/t -> 1/2 (mode-independent), then (4k-1)t^2/4
    leads = []
    subs = []
    for kk in (1, 2, 3):
        Wc, _ = _W_closed(kk)
        leads.append(sp.nsimplify(sp.limit(Wc / _t, _t, 0)))
        subs.append(sp.nsimplify(sp.limit((Wc - _t / 2) / _t ** 2, _t, 0)))
    ok_lead = all(sp.simplify(l - sp.Rational(1, 2)) == 0 for l in leads)
    ok_sub = all(sp.simplify(s) == 0 for s in subs)   # t^2 coefficient vanishes
    check("SMALL-t LEADING ORDER [E]: W_k(t) = t/2 + O(t^3) as t->0 -- the leading "
          "coefficient W_k/t -> 1/2 is MODE-INDEPENDENT (k=1,2,3: %s) and the t^2 term "
          "VANISHES (tail's (1/4-k) cancels the middle's (4k-1)/4; (W_k-t/2)/t^2 -> %s), "
          "so k enters only at O(t^3)"
          % ([str(l) for l in leads], [str(s) for s in subs]),
          ok_lead and ok_sub)

    return summary("v296 FLATAWAY.A2.CLOSED.01: exact a_2 coefficient in closed form W_k(t)=t(1-e^{-4kt})/(8k(1-e^{-t}))+(1/2)Σ Phi(m,4k-m), manifestly positive, leading W_k~t/2 (t^2 term cancels); reproduces v295 exactly")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
