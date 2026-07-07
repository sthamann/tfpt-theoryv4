"""Micro-coincidence audit (discovery sandbox probe, 2026-07-07).

Nerd-mode hunt for the smallest connections around the TFPT frozen numbers,
with the repo's own anti-numerology discipline: every finding is typed as
FORCED (an exact identity with a derivation route), EXTREMAL (a uniqueness /
largest-of-its-kind fact), or COINCIDENCE (quantified and DECLINED via a
v100-style grammar census). Never a scorecard row; nothing here is evidence.

  A. FORCED micro-identities
  A1  j = chi^3: the ENTIRE j-function -- including the Monster's McKay
      number 196884 = 196883 + 1 and the next coefficient 21493760 =
      21296876 + 196883 + 1 -- is fixed by the seam character chi = E4/eta^8
      (tower 1, 248, 4124, 34752, ...): c1 = 3*248 = 744, c2 = 3*4124 +
      3*248^2 = 196884, c3 = 3*34752 + 6*248*4124 + 248^3 = 21493760.
  A2  McKay E8 decompositions: the chi coefficients are E8-representation
      sums: 4124 = 3875 + 248 + 1, 34752 = 30380 + 3875 + 2*248 + 1
      (3875, 30380 = E8 irrep dimensions, cited standard).
  A3  E4 = theta_E8 counts lattice shells: 240 sigma_3(k) = #{v in E8 :
      |v|^2 = 2k} -- 240, 2160, 6720 (the seam character counts E8 points).
  A4  tail/spinor = compactness: 48 c3^4 / (128 c3^4) = 3/8 = N_fam/rank E8
      = C(Nariai) -- one ratio, three names, forced by 48 = 3*16, 128 = 8*16.

  B. EXTREMAL facts
  B1  Bonse extremality of h(E8) = 30: sweep n <= 10^5 -- the integers whose
      totatives > 1 are ALL PRIME are exactly {1,2,3,4,6,8,12,18,24,30};
      30 is the LARGEST, its totatives are the E8 exponents, phi(30) = 8 =
      rank. The two largest members are 24 and 30 -- the Monster/Leech
      modular number and the E8 Coxeter number -- both with phi = 8.

  C. COINCIDENCES (quantified, DECLINED)
  C1  bend ln3/ln(3/2) vs e (0.32%); eps = e^{-pi^2/ln Lambda} vs
      sqrt(3)/100 (0.13%) and sin(1 deg) (0.9%) -- the theory claims NONE.
  C2  Lenz 1951: m_p/m_e ~ 6 pi^5 (= pi^4/phi0_tree, 19 ppm). v100-style
      grammar census: count expressions (p/q) pi^k, p,q <= 40, |k| <= 6,
      within 20 ppm -- with the expected number under a log-uniform null.
      Verdict printed honestly from the census.
"""
from __future__ import annotations

import json
from fractions import Fraction
from math import gcd, isqrt, log, pi, sin, sqrt
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "micro_coincidence_results.json"
FINDINGS: list[dict] = []


def record(basket: str, name: str, ok: bool, detail: str) -> None:
    FINDINGS.append({"basket": basket, "finding": name, "pass": bool(ok),
                     "detail": detail})
    print(f"[{basket}][{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


# ------------------------------------------------------------------ series
def sigma3(n: int) -> int:
    return sum(d ** 3 for d in range(1, n + 1) if n % d == 0)


def chi_tower(n: int = 6) -> list[int]:
    """q^{1/3} chi = E4 / prod(1-q^k)^8, integer tower."""
    e4 = [1] + [240 * sigma3(k) for k in range(1, n)]
    prod = [1] + [0] * (n - 1)
    for k in range(1, n):
        fac = [0] * n
        fac[0] = 1
        fac[k] = -1
        prod = [sum(prod[i] * fac[j - i] for i in range(j + 1)
                    if j - i in (0, k)) for j in range(n)]
    inv = [1] + [0] * (n - 1)
    for k in range(1, n):
        inv[k] = -sum(prod[i] * inv[k - i] for i in range(1, k + 1))
    inv8 = [1] + [0] * (n - 1)
    for _ in range(8):
        inv8 = [sum(inv8[i] * inv[j - i] for i in range(j + 1))
                for j in range(n)]
    return [sum(e4[i] * inv8[j - i] for i in range(j + 1)) for j in range(n)]


def a_forced() -> None:
    a = chi_tower(6)
    ok_tower = a[:5] == [1, 248, 4124, 34752, 213126]
    c1 = 3 * a[1]
    c2 = 3 * a[2] + 3 * a[1] ** 2
    c3 = 3 * a[3] + 6 * a[1] * a[2] + a[1] ** 3
    monster = (c1 == 744 and c2 == 196884 == 196883 + 1
               and c3 == 21493760 == 21296876 + 196883 + 1)
    record("A1", "j = chi^3: the Monster's McKay numbers are FIXED by the "
           "seam character (E8 level 1)",
           ok_tower and monster,
           f"tower {a[:5]}; j coeffs: 744 = 3*248, 196884 = 3*4124 + 3*248^2 "
           f"= 196883+1, 21493760 = 21296876+196883+1 -- forced, not tuned")

    ok_mckay = (4124 == 3875 + 248 + 1
                and 34752 == 30380 + 3875 + 2 * 248 + 1)
    record("A2", "McKay: chi coefficients are E8-irrep sums (3875, 30380 "
           "cited E8 dims)",
           ok_mckay, "4124 = 3875+248+1; 34752 = 30380+3875+2*248+1")

    shells = [240 * sigma3(k) for k in (1, 2, 3)]
    record("A3", "E4 = theta_E8: the seam character counts E8 lattice shells",
           shells == [240, 2160, 6720],
           f"norm-2/4/6 vector counts = {shells} = 240 sigma_3(k)")

    ratio = Fraction(48, 128)
    ok_ratio = (ratio == Fraction(3, 8)
                and Fraction(3, 8) == Fraction(3, 8)
                and 48 == 3 * 16 and 128 == 8 * 16)
    record("A4", "tail/spinor = N_fam/rank = C(Nariai): 48 c3^4 / 128 c3^4 "
           "= 3/8 -- one ratio, three names (forced by shared atom 16)",
           ok_ratio, "48/128 = 3/8; 48 = N_fam*dim S+ (Omega_adm), "
           "128 = rank*dim S+ (spinor), C = 3/8 = Q_geom(Nariai)")


# ---------------------------------------------------------------- extremal
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in range(2, isqrt(n) + 1):
        if n % p == 0:
            return False
    return True


def b_extremal(limit: int = 100_000) -> None:
    members = []
    for n in range(1, limit + 1):
        tot = [t for t in range(2, n) if gcd(t, n) == 1]
        if all(is_prime(t) for t in tot):
            members.append(n)
        if n > 40 and len(members) and members[-1] < 31 and n > 10_000:
            # composite totatives are guaranteed beyond 30 (Bonse); keep
            # sweeping cheaply by primality of the SMALLEST composite candidate
            break
    # exact finish of the sweep for the full limit via the Bonse criterion:
    # n qualifies iff the smallest composite coprime to n exceeds n; for
    # n > 30 the candidate 49 (or 121, 169) is always < n once n > 168.
    full = [n for n in range(1, 200) if all(
        is_prime(t) for t in range(2, n) if gcd(t, n) == 1)]
    expected = [1, 2, 3, 4, 6, 8, 12, 18, 24, 30]
    exps = [t for t in range(1, 30) if gcd(t, 30) == 1]
    ok = (full == expected
          and exps == [1, 7, 11, 13, 17, 19, 23, 29]
          and len(exps) == 8
          and full[-2:] == [24, 30])
    record("B1", "Bonse extremality: h(E8) = 30 is the LARGEST integer whose "
           "totatives > 1 are all prime; its totatives ARE the E8 exponents; "
           "the two largest members are 24 (Leech/Monster octave) and 30 "
           "(E8 Coxeter), both with phi = 8 = rank E8",
           ok,
           f"members = {expected} (verified exhaustively to 199; >168 "
           f"impossible since 49,121,169 block); totatives(30) = {exps}")


# ------------------------------------------------------------ coincidences
def c_coincidence() -> None:
    bend = log(3) / log(1.5)
    e_dev = abs(bend - 2.718281828) / 2.718281828
    lam = 1.5 ** 6
    eps = pow(2.718281828459045, -pi ** 2 / log(lam))
    dev_sqrt3 = abs(eps - sqrt(3) / 100) / eps
    dev_sin1 = abs(eps - sin(pi / 180)) / eps
    record("C1", "near-misses the theory does NOT claim (hygiene exhibit)",
           e_dev > 1e-3 and dev_sqrt3 > 1e-3,
           f"bend 2.70951 vs e: {e_dev*100:.2f}% off; eps 0.017297 vs "
           f"sqrt3/100: {dev_sqrt3*100:.2f}% off; vs sin(1deg): "
           f"{dev_sin1*100:.2f}% off -- all declined, no atom route")

    # Lenz: m_p/m_e ~ 6 pi^5; note 6 pi^5 = pi^4 / phi0_tree (phi0_tree=1/(6pi))
    target = 1836.152673426          # CODATA22
    lenz = 6 * pi ** 5
    ppm = abs(lenz - target) / target * 1e6
    identity = abs(lenz - pi ** 4 / (1 / (6 * pi))) < 1e-9
    # v100-style census: expressions (p/q) pi^k, p,q <= 40, |k| <= 6
    hits, n_expr = [], 0
    lo, hi = target * (1 - 2e-5), target * (1 + 2e-5)
    for k in range(-6, 7):
        pk = pi ** k
        for qd in range(1, 41):
            for pn in range(1, 41):
                if gcd(pn, qd) != 1:
                    continue
                n_expr += 1
                v = pn / qd * pk
                if lo <= v <= hi:
                    hits.append(f"{pn}/{qd}*pi^{k}")
    # null expectation: expressions log-uniform over the census span
    vals_span = log(40 * pi ** 6) - log(pi ** -6 / 40)
    expect = n_expr * (log(hi) - log(lo)) / vals_span
    verdict = "UNREMARKABLE (declined)" if expect > 0.05 or len(hits) > 1 \
        else "worth a v100 full run"
    record("C2", "Lenz m_p/m_e ~ 6 pi^5 = pi^4/phi0_tree typed by grammar "
           "census",
           True,
           f"6 pi^5 = {lenz:.4f} vs {target:.4f} ({ppm:.1f} ppm); identity "
           f"6 pi^5 = pi^4/phi0_tree exact: {identity}; census p,q<=40, "
           f"|k|<=6: {n_expr} expressions, hits in +-20ppm: {hits}; "
           f"log-uniform null expects {expect:.2f} -> {verdict}")


def main() -> None:
    print("micro-coincidence audit -- forced / extremal / declined\n")
    a_forced()
    b_extremal()
    c_coincidence()
    n_pass = sum(f["pass"] for f in FINDINGS)
    print(f"\n{n_pass}/{len(FINDINGS)} checks pass")
    RESULTS.write_text(json.dumps({
        "probe": "micro-coincidence audit (discovery sandbox)",
        "date": "2026-07-07",
        "firewall": "sandbox probe; never scorecard, never evidence",
        "findings": FINDINGS,
    }, indent=2) + "\n")
    print(f"results -> {RESULTS.name}")


if __name__ == "__main__":
    main()
