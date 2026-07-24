"""EXPLORATION (experiments/ only -- NOT a suite module, NOT in the ledger/papers).

Deeper sequel to pi_signature_self_application_probe.py (user request): apply the
theory's CYCLIC structures (mu4 clock ticks), the FROZEN SEARCH SIGNATURES from
the experiments (DSI comb tones, static teeth, Moebius exponents), the FRACTAL
structures (DSI base 3/2), and the PRIME CHAIN (h(E8)=30 prime clock: atoms
{2,3,5} + live phases {7,11,13,17,19,23,29} = E8 exponents = totatives of 30,
see markov_modular_prime_clock_probe.py) to pi itself.

Test batteries:
  (1) mu4 clock on pi, EXACT: Euler identity as clock statement (pi = the sheet
      tick), quarter/eighth ticks, silver-ratio seam angle.
  (2) clock character x prime chain, EXACT: L(1,chi4) = pi/4 (Leibniz/Euler) --
      the mu4 character summed over the primes GENERATES pi; 30-clock truncation
      of the Euler products with smooth-cutoff kill-control; E8-exponent phase
      balance under chi4 / mod-6.
  (3) frozen comb detectors (recovery-comb-domains kernel, seed 41) on pi's OWN
      recursive structure: continued-fraction terms; Gauss-Kuzmin null; Levy
      constant (the universal CF ladder rate CONTAINS pi^2 -- typed as a.e.-
      universal, NOT pi-specific).
  (4) frozen combs on decimal-digit waiting gaps + base-30 digits vs the prime
      clock (do pi's base-30 digits prefer the E8-exponent residues? chi^2 +
      binomial; control constant: e).
  (5) fractal: beta-expansion of pi in the DSI base beta = 3/2 (exact mpmath
      orbit) vs an MC null of generic seeds.

Firewall: discovery sandbox; nothing here is a claim or scorecard row. Digit-
level tests are tests of pi's GENERICITY (normality/Gauss-Kuzmin) against the
TFPT-specific structures -- the honest expectation is NULL everywhere; any
p < 0.05 would only ever be an escalate-candidate for a preregistered rerun.
Exact identities are classical mathematics (Euler, Leibniz, Levy, Steinhaus)
re-read in TFPT language, typed [E]-grade arithmetic / prose, never physics.

Run:  cd experiments/tfpt-discovery && .venv/bin/python pi_clock_comb_prime_probe.py
"""
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np

sys.set_int_max_str_digits(300_000)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "recovery-comb-domains" / "src"))
from tfpt_combdomains.quake import _stacked_at, rate_curve  # noqa: E402

# frozen search tones (source: signature_coverage_audit.py 2026-07-13 + the
# S1/S4 tooth spacings from SIGNATURES.md, expressed as ln-periods -> omegas)
A = 6 * math.log(1.5)
B = 6 * math.log(3.0)
TONES = {
    "omega_1 2.583 (S2b)": 2 * math.pi / A,
    "omega_2 0.953": 2 * math.pi / B,
    "omega_3 1.511": 2 * math.pi / (B - A),
    "res 2.749": 2.749026,
    "res 3.796": 3.796156,
    "res 4.911": 4.911247,
    "res 5.559": 5.558893,
    "S1 teeth 15.50": 2 * math.pi / math.log(1.5),
    "S4 Moe3 5.166": 2 * math.pi / (3 * math.log(1.5)),
    "S4 Moe4 3.875": 2 * math.pi / (4 * math.log(1.5)),
    "S4 Moe12 1.292": 2 * math.pi / (12 * math.log(1.5)),
}

ATOMS = [2, 3, 5]
LIVE = [7, 11, 13, 17, 19, 23, 29]
E8_EXP = [1, 7, 11, 13, 17, 19, 23, 29]          # = totatives of h(E8)=30
PRIMES_30 = ATOMS + LIVE                          # the ten-prime chain


def sec(t):
    print("\n" + "=" * 76 + "\n" + t + "\n" + "=" * 76)


def primes_below(n):
    sieve = np.ones(n, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    return [int(p) for p in np.nonzero(sieve)[0]]


def chi4(n):
    return {1: 1, 3: -1}.get(n % 4, 0)


def chi2_pvalue(chi2, dof):
    return float(mp.gammainc(mp.mpf(dof) / 2, mp.mpf(chi2) / 2, mp.inf,
                             regularized=True))


def comb_scan(name, vals):
    """Frozen distribution-channel scan (identical machinery to
    signature_coverage_audit.py part 2): equal-ln rate curve + stacked
    permutation comb test at every frozen tone, Bonferroni over gated tones."""
    vals = np.asarray([v for v in vals if v > 0], dtype=float)
    t, y = rate_curve(vals)
    span = float(np.log(vals.max() / vals.min()))
    print(f"\n### {name}: {len(vals)} events, ln-range {span:.2f}, {len(t)} bins")
    gated = []
    for label, om in TONES.items():
        r = _stacked_at([(t, y)], om, seed=41)
        status = ("range_blind" if r["n_used"] == 0
                  else ("ESCALATE_CANDIDATE" if r["p_value"] < 0.05 else "null"))
        if r["n_used"] > 0:
            gated.append((label, r["p_value"]))
        print(f"  {label:22s} n_used={r['n_used']}  p={r['p_value']:.4f}  {status}")
    if gated:
        m = len(gated)
        best = min(gated, key=lambda kv: kv[1])
        gp = min(1.0, best[1] * m)
        print(f"  -> Bonferroni over {m} gated tones: best {best[0]} "
              f"p={best[1]:.4f}, global p={gp:.3f}"
              + ("  <-- SURVIVES (escalate)" if gp < 0.05 else "  (null)"))
    return gated


def cf_terms_of(x_func, n_max=3000, dps=1700):
    """Continued-fraction terms with an exact q_n precision guard."""
    old = mp.mp.dps
    mp.mp.dps = dps
    x = x_func()
    terms = []
    q2, q1 = 0, 1
    limit = 10**(dps - 80)
    a0 = int(mp.floor(x))
    x = x - a0
    for _ in range(n_max):
        x = 1 / x
        a = int(mp.floor(x))
        terms.append(a)
        q2, q1 = q1, a * q1 + q2
        if q1 > limit:
            break
        x = x - a
    mp.mp.dps = old
    return terms, q1


def digits_of(x_func, n_dec):
    """First n_dec fractional decimal digits as a string."""
    old = mp.mp.dps
    mp.mp.dps = n_dec + 30
    s = mp.nstr(x_func(), n_dec + 20, strip_zeros=False)
    mp.mp.dps = old
    return s.split(".")[1][:n_dec]


def base30_digits(dec_digits, n_out):
    """First n_out base-30 fractional digits from a decimal digit string
    (blockwise exact integer conversion; needs len(dec) >= 1.5*n_out + guard)."""
    n_dec = len(dec_digits)
    M = int(dec_digits)
    TEN = 10**n_dec
    out = []
    block = 500
    mult = 30**block
    while len(out) < n_out:
        M *= mult
        d_block, M = divmod(M, TEN)
        blk = []
        for _ in range(block):
            d_block, d = divmod(d_block, 30)
            blk.append(d)
        out.extend(reversed(blk))
    return out[:n_out]


def main():
    mp.mp.dps = 40
    PI = mp.pi

    sec("(1) MU4 CLOCK on pi, EXACT: pi IS the sheet tick of the clock")
    e_ident = abs(mp.e**(1j * PI) + 1)
    print(f"|exp(i*pi) + 1| = {mp.nstr(e_ident, 5)}   (Euler; exact)")
    print("  -> in clock language: one HALF-turn of the mu4 clock (clock^2 = the")
    print("     Z2 sheet, i^2 = -1) costs exactly pi. pi is not something the")
    print("     clock 'finds' -- pi IS the angular price of the sheet involution.")
    print(f"quarter tick pi/2:  clock^4 = identity; recursion on pi-as-angle is")
    print(f"  exactly 4-periodic (pi -> 3pi/2 -> 2pi=0 -> pi/2 -> pi): nothing new.")
    silver = 1 / mp.tan(PI / 8) - (1 + mp.sqrt(2))
    print(f"eighth tick pi/8:  cot(pi/8) - (1+sqrt2) = {mp.nstr(silver, 5)}  (exact 0)")
    print("  -> the mu4/square seam half-angle carries the SILVER ratio 1+sqrt2 --")
    print("     the Pell branch of the Markov anchor tree (v527 silver clock,")
    print("     markov_modular_prime_clock_probe I). Exact, classical, [E]-grade.")

    sec("(2) CLOCK CHARACTER x PRIME CHAIN, EXACT: the mu4 character over the"
        " primes GENERATES pi")
    print("Leibniz/Euler: L(1,chi4) = pi/4, Euler product over ODD primes")
    print("  pi/4 = prod_p p/(p - chi4(p));  chi4 = the mu4 clock character mod 4:")
    print(f"  live phases sorted by clock phase: p=1 mod 4: {[p for p in LIVE if p % 4 == 1]}"
          f" | p=3 mod 4: {[p for p in LIVE if p % 4 == 3]} (+ atom 5 = 1, atom 3 = 3 mod 4)")
    print("30-clock truncation (the ten-prime chain) + smooth-cutoff kill-control:")
    print("  cutoff X | rel.err of prod_{odd p<X} p/(p-chi4(p)) vs pi/4 "
          "| rel.err of 6*prod_{p<X}(1-p^-2)^-1 vs pi^2")
    pi4 = float(PI) / 4
    pi2 = float(PI)**2
    for X in (10, 20, 30, 42, 60, 102, 1002, 10002):
        pl = 1.0
        pz = 1.0
        for p in primes_below(X):
            if p != 2:
                pl *= p / (p - chi4(p))
            pz *= 1 / (1 - p**-2)
        e1 = abs(pl - pi4) / pi4
        e2 = abs(6 * pz - pi2) / pi2
        mark = "  <-- the TFPT ten-prime chain" if X == 30 else ""
        print(f"  {X:6d}   | {e1:10.3e}                            | {e2:10.3e}{mark}")
    print("  -> convergence is SMOOTH in the cutoff; X=30 is NOT distinguished for")
    print("     pi. Direction is reversed: pi does not 'contain' the prime chain --")
    print("     the full prime set, summed with the mu4 clock phase, produces pi.")
    s4 = sum(chi4(e) for e in E8_EXP)
    s6 = sum(1 if e % 6 == 1 else -1 for e in E8_EXP)
    print(f"E8-exponent phase balance (exact): sum chi4(exponents) = {s4},"
          f" sum chi6(exponents) = {s6}")
    print(f"  ({[e % 4 for e in E8_EXP]} mod 4 -- four ticks on each clock phase;")
    print(f"   sum of exponents = {sum(E8_EXP)} = # positive roots of E8)")
    print("rewrite note (NOT a discovery, v100 caution): 1/c3 = 8 pi = 2^g_car *")
    print("  L(1,chi4) * 4 = 32*(pi/4) -- a factoring of the integer 8, kept as prose.")

    sec("(3) FROZEN SEARCH SIGNATURES on pi's OWN recursion: continued fraction")
    cf, q_last = cf_terms_of(lambda: +mp.pi)
    known = [7, 15, 1, 292, 1, 1, 1, 2, 1, 3]
    print(f"CF terms computed: {len(cf)} (precision-guarded, q_n ~ 10^"
          f"{len(str(q_last))})")
    print(f"  first 10 terms {cf[:10]} == literature {known}: "
          f"{'PASS' if cf[:10] == known else 'FAIL'}")
    top = sorted(range(len(cf)), key=lambda i: -cf[i])[:3]
    print("  largest terms: " + ", ".join(f"a_{i+1}={cf[i]}" for i in top))
    # Gauss-Kuzmin null: P(a=k) = log2(1 + 1/(k(k+2)))
    n = len(cf)
    obs = [sum(1 for a in cf if a == k) for k in range(1, 9)]
    pk = [math.log2(1 + 1 / (k * (k + 2))) for k in range(1, 9)]
    obs.append(n - sum(obs))
    pk.append(1 - sum(pk))
    chi2 = sum((o - n * p)**2 / (n * p) for o, p in zip(obs, pk))
    pv = chi2_pvalue(chi2, len(obs) - 1)
    print(f"  Gauss-Kuzmin chi^2 (9 cells) = {chi2:.2f}, p = {pv:.3f}"
          f"  -> {'consistent with a GENERIC real' if pv > 0.05 else 'DEVIATES'}")
    levy = math.exp(math.pi**2 / (12 * math.log(2)))
    q_rate = float(mp.mpf(len(str(q_last))) * mp.log(10) / len(cf))
    print(f"  Levy ladder rate: q_n^(1/n) -> {math.exp(q_rate):.4f} vs Levy const "
          f"e^(pi^2/(12 ln2)) = {levy:.4f} (dev {abs(math.exp(q_rate)-levy)/levy:.1%})")
    print("  -> the CF ladder (the ur-fractal recursion) of pi grows at the")
    print("     universal rate that itself CONTAINS pi^2 -- but this holds for")
    print("     a.e. real (Levy 1936): self-reference of the continuum, NOT of pi.")
    comb_scan("pi CF terms (size channel)", cf)

    sec("(4) FROZEN COMBS on digit gaps + BASE-30 digits vs the prime clock")
    dec = digits_of(lambda: +mp.pi, 100_000)
    pos = [i for i, c in enumerate(dec) if c == "0"]
    gaps = np.diff(np.array(pos))
    comb_scan("pi decimal digit-0 waiting gaps", gaps)
    print("\nbase-30 digits vs the prime clock (do pi's digits prefer the")
    print("E8-exponent residues = totatives of 30?):")
    dec32 = dec[:32_000]
    for label, digstr in (("pi", dec32), ("e (control)",
                                          digits_of(lambda: +mp.e, 32_000))):
        d30 = base30_digits(digstr, 20_000)
        nn = len(d30)
        hits = sum(1 for d in d30 if d in set(E8_EXP))
        p_hit = 8 / 30
        z = (hits - nn * p_hit) / math.sqrt(nn * p_hit * (1 - p_hit))
        p_bin = math.erfc(abs(z) / math.sqrt(2))
        counts = [d30.count(k) for k in range(30)]
        chi2u = sum((c - nn / 30)**2 / (nn / 30) for c in counts)
        pu = chi2_pvalue(chi2u, 29)
        print(f"  {label:12s} E8-residue hits {hits}/{nn} (exp {nn*p_hit:.0f}),"
              f" z = {z:+.2f}, p = {p_bin:.3f};  30-cell chi^2 = {chi2u:.1f},"
              f" p = {pu:.3f}")
    print("  -> pi's base-30 digits are uniform; no preference for the prime-chain")
    print("     residues, and pi behaves exactly like the control constant e.")

    sec("(5) FRACTAL: beta-expansion of pi in the DSI base beta = 3/2")
    n_dig = 5000
    mp.mp.dps = int(n_dig * math.log10(1.5)) + 60
    x = mp.pi - 3
    beta = mp.mpf(3) / 2
    ones_pi = 0
    one_pos = []
    for i in range(n_dig):
        x = beta * x
        d = int(mp.floor(x))
        if d:
            ones_pi += 1
            one_pos.append(i)
        x -= d
    mp.mp.dps = 40
    f_pi = ones_pi / n_dig
    rng = np.random.default_rng(41)
    xs = rng.random(2000)
    freqs = np.zeros(2000)
    for _ in range(n_dig):
        xs *= 1.5
        ds = np.floor(xs)
        freqs += ds
        xs -= ds
    freqs /= n_dig
    mu, sd = float(freqs.mean()), float(freqs.std())
    z = (f_pi - mu) / sd
    p_mc = float(np.mean(np.abs(freqs - mu) >= abs(f_pi - mu)))
    print(f"digit-1 frequency of pi in base 3/2 (exact orbit, {n_dig} digits):"
          f" {f_pi:.4f}")
    print(f"  MC null (2000 generic seeds, float64): {mu:.4f} +- {sd:.4f}"
          f"  -> z = {z:+.2f}, MC p = {p_mc:.3f}")
    g1 = np.diff(np.array(one_pos))
    comb_scan("pi base-3/2 digit-1 waiting gaps", g1)
    print("  -> pi's orbit under the DSI map T(x) = (3/2)x mod 1 is statistically")
    print("     GENERIC: the fractal signature base does not single out pi.")

    sec("VERDICT (honest, firewall)")
    print("CYCLIC (clock): exact and structural -- pi IS the mu4 clock's sheet tick")
    print("  (Euler), the eighth tick carries the silver/Pell seam ratio, and the")
    print("  clock's character chi4 summed over ALL primes generates pi (Leibniz).")
    print("  The 30-clock ten-prime truncation is NOT distinguished (smooth cutoff).")
    print("PRIME CHAIN: the E8 exponents are chi4-phase-balanced on the 30-wheel")
    print("  (exact 4+4); pi's base-30 digits show NO preference for the exponent")
    print("  residues (z consistent with 0; control constant e identical).")
    print("SEARCH SIGNATURES: the frozen comb detectors (11 tones incl. S1/S4")
    print("  spacings) on pi's CF terms and digit-gap distributions: NULL after")
    print("  Bonferroni; pi's CF statistics are Gauss-Kuzmin generic; its ladder")
    print("  rate is the universal Levy constant (which contains pi^2 for EVERY")
    print("  generic real -- continuum self-reference, not pi-specificity).")
    print("FRACTAL: pi is a generic point of the beta = 3/2 (DSI) map: digit")
    print("  frequency and gap structure indistinguishable from the MC null.")
    print("CONCLUSION: every EXACT connection between pi and the theory's cyclic/")
    print("  prime structures runs through classical identities (Euler, Leibniz,")
    print("  Levy) in the GENERATIVE direction (clock+primes -> pi); every")
    print("  STATISTICAL probe of pi's expansions with the frozen TFPT detectors")
    print("  is null. pi carries the theory's structures as their OUTPUT, not as")
    print("  hidden content. Consistent with the Library-of-Babel rejection and")
    print("  the one-pass-compiler verdict. No promotion candidate; stays here.")


if __name__ == "__main__":
    main()
