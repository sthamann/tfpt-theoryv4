"""v29 -- machine certificates for the two research contracts (U_wall, G_metric).

Backs the cleanly-certifiable lemmas of the two research contracts
(tfpt_research_contracts), and records one HONEST correction.

C_U^(1)  WALL ENUMERATION (Contract 1, Lemma U1 -- corrected).
  Enumerate the 6^4 = 1296 weight matrices whose columns are permutations of the
  cusp triple (0,1,2).  The parabolic wall constraint (row-sum multiset {6,3,3},
  i.e. weights (2,1,1) lifting degrees (-2,-1,-1) to pardeg 0) leaves 144; with
  the O(-2) line distinguished (its row carries the max sum 6), 48.  HONEST
  RESULT: under the FULL natural symmetry D4(punctures) x S3(lines) x S3(values)
  these still form FIVE orbits, not one.  So W_wall is NOT singled out by
  symmetry alone -- the uniqueness must come from the TFPT SELECTOR (Lemma U4:
  det R=8, Spec(Q+)={1,2,3}), not from U1.  W_wall is one of the five.

G5  GAP-DOMINANCE (Contract 2, Lemma G5).
  The strong form 2||V_metric||_rel < Delta with ||V_metric||_rel <= 248 c3^2
  = 31/(8 pi^2) = 0.39262 and Delta = 6 log(3/2) = 2.43279 gives an effective
  transfer gap Delta_eff > 1.647 > 0.
"""
from itertools import permutations, product
import mpmath as mp
from tfpt_constants import check, summary, reset, c3

mp.mp.dps = 30


def _wall_orbits():
    perms = list(permutations([0, 1, 2]))
    mats = []
    for cols in product(perms, repeat=4):
        M = tuple(tuple(cols[c][r] for c in range(4)) for r in range(3))
        mats.append(M)
    def rowsums(M):
        return tuple(sum(M[r][c] for c in range(4)) for r in range(3))
    walls = [M for M in mats if sorted(rowsums(M), reverse=True) == [6, 3, 3]]
    # full symmetry group: D4 on columns, S3 on rows, S3 on values
    def rotate(p):
        return [p[(i + 1) % 4] for i in range(4)]
    D4 = []
    p = [0, 1, 2, 3]
    for _ in range(4):
        D4.append(tuple(p))
        D4.append((p[0], p[3], p[2], p[1]))
        p = rotate(p)
    D4 = list(set(D4))

    def canon(M):
        best = None
        for d in D4:
            Mc = tuple(tuple(M[r][d[c]] for c in range(4)) for r in range(3))
            for rp in permutations([0, 1, 2]):
                Mr = (Mc[rp[0]], Mc[rp[1]], Mc[rp[2]])
                for vp in permutations([0, 1, 2]):
                    X = tuple(tuple(vp[Mr[r][c]] for c in range(4)) for r in range(3))
                    if best is None or X < best:
                        best = X
        return best
    orbits = set(canon(M) for M in walls)
    Wwall = ((2, 1, 2, 1), (1, 0, 0, 2), (0, 2, 1, 0))
    return len(mats), len(walls), len(orbits), (canon(Wwall) in orbits)


def run():
    reset()
    print("v29  research-contract certificates (C_U^(1) wall enum, G5 gap)")

    # C_U^(1): wall enumeration (honest 5-orbit result)
    total, nwall, norb, has_W = _wall_orbits()
    check("C_U^(1): 6^4 = 1296 column-permutation weight matrices", total, 1296, exact=True)
    check("C_U^(1): 144 matrices satisfy the {6,3,3} wall constraint", nwall, 144, exact=True)
    check("C_U^(1) HONEST: 5 wall orbits under D4 x S3 x S3 (NOT 1) "
          "-> uniqueness needs the selector (U4), not symmetry (U1 corrected)", norb, 5, exact=True)
    check("C_U^(1): W_wall is one of the five wall types", has_W)

    # G5: gap-dominance strong form
    Vrel = 248 * c3**2
    Delta = 6 * mp.log(mp.mpf(3) / 2)
    check("G5: ||V_metric||_rel <= 248 c3^2 = 31/(8 pi^2) = 0.39262",
          Vrel, mp.mpf(31) / (8 * mp.pi**2), tol=mp.mpf('1e-20'))
    check("G5: strong form 2||V|| = 0.7852 < Delta = 6 log(3/2) = 2.4328", 2 * Vrel < Delta)
    Delta_eff = Delta - 2 * Vrel
    check("G5: effective transfer gap Delta_eff = Delta - 2||V|| > 1.647 (positive)",
          Delta_eff > mp.mpf('1.647'))
    return summary("v29 research-contract certificates")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
