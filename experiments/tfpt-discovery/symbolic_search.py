#!/usr/bin/env python3
"""
(b1) Self-contained symbolic-regression pipeline for TFPT closed forms.

This is the correct tool for matching a SINGLE constant to the TFPT grammar
(PySR fits y=f(X) over data; for one number an enumerative MDL search is
right). It enumerates expressions  base + coeff * atom^power  over the TFPT
grammar, scores by relative error, AND reports a "look-elsewhere"
significance: the expected number of chance hits given the search-space size
and the data precision. A small candidate set surviving the chance estimate
is the only honest output.

Usage:  python symbolic_search.py
Extend ATOMS/BASES/COEFFS/forms to widen the grammar.
"""
import mpmath as mp
import itertools
mp.mp.dps = 30
pi = mp.pi
c3   = 1/(8*pi)
phi0 = mp.mpf(4)/3*c3 + 48*c3**4
gamma = mp.mpf(5)/6
lamC = mp.sqrt(phi0*(1-phi0))
eg = mp.e**(-gamma)

# --- TFPT grammar -----------------------------------------------------------
ATOMS = {
    "phi0": phi0, "c3": c3, "lamC": lamC, "phi0*e^-g": phi0*eg,
    "sqrt(phi0)": mp.sqrt(phi0), "phi_base": mp.mpf(1)/(6*pi),
}
BASES = {"0": mp.mpf(0), "1/4": mp.mpf(1)/4, "1/3": mp.mpf(1)/3,
         "1/2": mp.mpf(1)/2, "3/8": mp.mpf(3)/8, "2/9": mp.mpf(2)/9}
COEFFS = sorted({mp.mpf(k)/d for d in (1,2,3,4,6,8) for k in range(-8,9) if k})
POWERS = (1, 2)

def enumerate_space():
    for bn, b in BASES.items():
        for an, a in ATOMS.items():
            for p in POWERS:
                ap = a**p
                for c in COEFFS:
                    yield (f"{bn} + ({c})*{an}^{p}", b + c*ap)

SPACE = list(enumerate_space())
N_EXPR = len(SPACE)

def search(name, target, data_prec, top=6):
    """data_prec = fractional precision to which the *target* is known."""
    t = mp.mpf(str(target))
    hits = sorted(((abs(v-t)/abs(t), e, v) for e, v in SPACE), key=lambda x: x[0])
    print(f"\n=== {name}: target {t} (known to ~{data_prec:.0e}) ===")
    # look-elsewhere: prob a random expr lands within 'rel' of target ~ 2*rel
    # (values are O(target)); expected chance hits = N * 2*rel.
    for rel, e, v in hits[:top]:
        exp_chance = N_EXPR * 2*float(rel)
        flag = "PLAUSIBLE" if (rel < data_prec and exp_chance < 1) else "chance-likely"
        print(f"  {e:34s} = {mp.nstr(v,8):12s} rel={float(rel):.2e}  "
              f"E[chance hits @this rel]={exp_chance:6.2f}  -> {flag}")
    print(f"  (search space N = {N_EXPR} expressions)")

if __name__ == "__main__":
    print(f"TFPT symbolic search; grammar size N = {N_EXPR}")
    # validation: rediscover a KNOWN decoder (should appear with rel~0)
    search("VALIDATION lambda_C (known sqrt(phi0(1-phi0)))", float(lamC), 1e-12)
    # the genuine gaps:
    search("sin^2 theta12 (NuFIT NO 0.303)", 0.303, 3e-2)   # data ~10% (range .27-.34)
    search("sin^2 theta12 (upper 0.307)",   0.307, 3e-2)
    search("sin^2 thetaW MSbar(MZ) 0.23116", 0.23116, 1e-3) # scheme-dependent!
    search("alpha_s(MZ) 0.11796", 0.11796, 1e-2)
    print("""
READING:
- 'PLAUSIBLE' requires (i) rel error below the data precision AND
  (ii) expected chance hits < 1 in the whole search space.
- A flat grammar of ~1800 expressions will hit any 1e-3 target by chance
  (E[hits] ~ 1800*2e-3 ~ 4), so theta_W/alpha_s 'matches' are chance-likely:
  NOT predictions. theta_12 candidates survive only because the DATA itself
  is loose (~10%); they remain conjectures needing a derivation.
- Honest output: the engine GENERATES hypotheses; the TFPT closure must then
  DERIVE or REJECT each one. Use it to prune, never to claim.
""")
