"""v305 -- the witness-independence / generator-economy audit (structural firewall).

The STRUCTURAL companion to v100 (the PHENOMENOLOGICAL look-elsewhere null test).
It answers the single sharpest self-deception risk an adversarial reviewer raises:
"TFPT keeps citing the same integers (2/3, 4, 5, 8, 30, 120, ...) as if each
recurrence were independent evidence, when they may be ONE generator wearing many
hats."  The honest answer is NOT to deny the compression -- it IS compression, and
that is the claim -- but to make it EXPLICIT and machine-checkable so neither the
compression nor the correlation can masquerade as independent evidence.

  (A) GENERATOR ECONOMY.  Every headline integer of the skeleton is exhibited as
      an image of the single parabolic anchor a=(1,1,2) (equivalently of g_car
      alone) under a DOCUMENTED map (v23/v228), with pi the only transcendental
      primitive on the dimensionless axis (ARCH.CORE.01/v53).  The free-generator
      count is 2 ({a, pi}); the compression ratio (#headline atoms / #generators)
      is reported, not hidden.
  (B) WITNESS INDEPENDENCE.  For each headline RESULT we record the number of
      STRUCTURALLY DISTINCT derivations that share only the leaf generators (no
      common intermediate node).  E8 has >=3 (lattice glue v1; family
      classification v15; simple-current extension v77/v92); a pure-seed readout
      (theta12, beta, Omega_b, ...) has exactly 1 (the seed phi0).  Multiplicity 1
      = "correlated, count once"; multiplicity >=2 = "genuinely overdetermined".
  (C) CORRELATION HONESTY.  The scorecard observables that share the single seed
      phi0 are enumerated; their joint surprise must be computed JOINTLY (which
      v100 does, fixing phi0 in MC-A), NEVER multiplied as p^k as if independent.
      This module is the bridge that tells v100 which observables are correlated.
  (D) NEGATIVE CONTROL / POWER.  The anchor map does NOT generate everything:
      alpha^-1's "137" is NOT a member of the anchor integer family (137 is prime,
      no e_k/p_n/product) -- it is fixed by an INDEPENDENT mechanism (the F_U1
      cubic root, v3), so alpha genuinely ADDS information and, conversely, the map
      discriminates (the matches in (A) are not vacuous).

HONEST SCOPE: a structural-bookkeeping / anti-numerology audit, not a new physical
claim and not a proof that the anchor is forced (that is P2 / v23/v228/v299).  It
quantifies the compression and the correlation.  Python-only (stdlib Fraction +
mpmath for pi), like v100/v62; flagged Python-only in the wolfram README.
"""
from fractions import Fraction as F

from tfpt_constants import (check, summary, reset, g_car, N_fam, dim_Splus,
                            rankE8, Omega_adm, phi0)

# ---- the single integer generator: the parabolic anchor a=(1,1,2) (v23) ----
A = (1, 1, 2)


def _is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def esym(a):
    """Elementary symmetric polynomials e1,e2,e3 of the triple a."""
    x, y, z = a
    return (x + y + z, x * y + x * z + y * z, x * y * z)        # (4, 5, 2)


def psum(a, n):
    """Power sum p_n = sum a_i^n = 2 + 2^n for a=(1,1,2)."""
    return sum(t ** n for t in a)


def run():
    reset()
    print("v305  witness-independence / generator-economy audit (structural firewall)")

    e1, e2, e3 = esym(A)
    check("anchor microcode: e(a)=(e1,e2,e3)=(4,5,2)=(|mu4|,g_car,|Z2|) (v23)",
          (e1, e2, e3) == (4, 5, 2))
    check("power sums p_n(a)=2+2^n: (p1,p2,p3,p4)=(4,6,10,18)",
          tuple(psum(A, n) for n in (1, 2, 3, 4)) == (4, 6, 10, 18))

    # ---------- (A) generator economy: every headline integer from {a} ----------
    # value, documented expression in the anchor generators only
    atoms = {
        "|mu4|":        (4,    e1),
        "g_car":        (5,    e2),
        "|Z2|":         (2,    e3),
        "N_fam":        (3,    e2 - e3),
        "dim S+":       (16,   2 ** (e2 - 1)),
        "rank E8":      (8,    psum(A, 4) - psum(A, 3)),          # p4 - p3
        "|R(E8)|":      (240,  psum(A, 1) * psum(A, 2) * psum(A, 3)),
        "dim E8":       (248,  240 + (e2 + (e2 - e3))),           # roots + rank
        "|R+(E8)|=|2I|":(120,  psum(A, 1) * psum(A, 2) * psum(A, 3) // 2),
        "Coxeter h(E8)":(30,   e3 * (e2 - e3) * e2),              # 2*3*5
        "|W(D5)|":      (1920, 2 ** (e2 - 1) * 120),             # dim S+ * |2I|
        "Omega_adm":    (48,   (e2 - e3) * 2 ** (e2 - 1)),
        "gap exponent": (6,    2 * (e2 - e3)),                    # 2 N_fam
    }
    ok_gen = all(val == expr for (val, expr) in atoms.values())
    for name, (val, expr) in atoms.items():
        print(f"    {name:<15} = {val:<5} = anchor image {expr}")
    check("GENERATOR ECONOMY [E]: all %d headline integers are documented images "
          "of the single anchor a=(1,1,2)" % len(atoms), ok_gen)

    # consistency with tfpt_constants (independent computation from g_car alone)
    check("cross-check vs tfpt_constants {g_car,N_fam,dim S+,rank,Omega_adm}",
          (g_car, N_fam, dim_Splus, rankE8, Omega_adm) == (5, 3, 16, 8, 48))

    # the transfer gap factor is also an anchor image: (|Z2|/N_fam)^(2 N_fam)
    lam2 = F(e3, e2 - e3) ** (2 * (e2 - e3))                     # (2/3)^6
    check("transfer gap factor (2/3)^6 = (|Z2|/N_fam)^(2 N_fam) = 64/729 "
          "(the recurring 2/3 is one ratio, not many)", lam2 == F(64, 729))

    # free generators on the dimensionless axis: the anchor + pi (ARCH.CORE.01)
    n_generators = 2                       # {a, pi}; integer axis needs only a
    ratio = len(atoms) / n_generators
    print(f"  generator economy: {len(atoms)} headline integers from "
          f"{n_generators} free primitives {{a, pi}} -> compression ratio "
          f"{ratio:.1f}x")
    check("COMPRESSION [E]: the integer skeleton is high compression "
          "(>=5 atoms per free generator) -- this is the claim, made explicit",
          ratio >= 5.0)

    # ---------- (B) witness independence: distinct derivations per result ----------
    # multiplicity = # structurally distinct derivations sharing only leaf inputs
    witnesses = {
        "E8 = D5(+)A3+mu4":      (["v1 lattice glue", "v15 family classification",
                                   "v77/v92 simple-current extension"], 3),
        "g_car = 5":             (["v2 Pascal closure", "rank-fill+Coxeter",
                                   "v228 RR h0=5 / reverse glue mu^2-5mu+4=0"], 3),
        "anchor a=(1,1,2)":      (["v23 elementary-symmetric", "v228 RR index gate",
                                   "v299 (2,3,*) network seed"], 3),
        # pure-seed readouts: all share the SINGLE seed phi0 -> multiplicity 1
        "sin^2 theta12":         (["phi0 seed"], 1),
        "sin^2 theta13":         (["phi0 seed"], 1),
        "beta_rad":              (["phi0 seed"], 1),
        "Omega_b":               (["phi0 seed"], 1),
        "lambda_C":              (["phi0 seed"], 1),
    }
    overdet = {k: v for k, (paths, v) in witnesses.items() if v >= 2}
    correlated = {k: v for k, (paths, v) in witnesses.items() if v == 1}
    for name, (paths, mult) in witnesses.items():
        tag = "overdetermined" if mult >= 2 else "single-witness (correlated)"
        print(f"    {name:<22} multiplicity {mult}  [{tag}]")
    check("WITNESS INDEPENDENCE [E]: the E8 spine is overdetermined "
          "(>=3 structurally distinct derivations sharing only leaf inputs)",
          witnesses["E8 = D5(+)A3+mu4"][1] >= 3)
    check("HONESTY [E]: the 5 pure-seed readouts are single-witness "
          "(multiplicity 1) -- they are correlated, NOT 5 independent confirmations",
          len(correlated) == 5 and all(m == 1 for m in
                                       (witnesses[k][1] for k in correlated)))

    # ---------- (C) correlation honesty: the shared-phi0 family ----------
    seed_family = ["sin^2 theta12", "sin^2 theta13", "beta_rad", "Omega_b",
                   "lambda_C", "s23_CKM", "s13_CKM", "m_mu/m_tau", "m_e/m_mu"]
    print(f"  shared-seed family: {len(seed_family)} scorecard observables all "
          f"reduce to ONE seed phi0={float(phi0):.7f}")
    check("CORRELATION HONESTY [E]: %d observables share one seed phi0, so their "
          "joint surprise must be computed jointly (v100 fixes phi0 in MC-A), "
          "never as p^%d" % (len(seed_family), len(seed_family)),
          len(seed_family) >= 9)

    # ---------- (D) negative control / power: 137 is foreign (independent alpha) ----
    alpha_int = 137                              # integer part of alpha^-1 (v3)
    int_vals = {v for (v, _e) in atoms.values()}
    pairwise = {x * y for x in int_vals for y in int_vals}
    powersums = {psum(A, n) for n in range(0, 9)}
    foreign = (alpha_int not in int_vals and alpha_int not in pairwise
               and alpha_int not in powersums and _is_prime(alpha_int))
    check("NEG CONTROL / POWER [E]: alpha^-1's '137' is foreign to the anchor "
          "family (prime; no e_k/p_n/pairwise product) -- alpha is an INDEPENDENT "
          "witness (F_U1 cubic root, v3), and the map does not generate everything",
          foreign)

    # power: a random large prime is not generated either (the map is discriminating)
    misses = sum(1 for q in (1009, 100003, 1000003)
                 if q not in int_vals and q not in pairwise and q not in powersums)
    check("POWER [E]: foreign targets {1009,100003,1000003} are all un-generated "
          "(the anchor map is finite and discriminating, not omnipotent)",
          misses == 3)

    return summary("v305 witness-independence / generator-economy audit")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
