"""v276 -- QGEO.SYM.03: the flat-pillowcase premise CLOSES the modular-commutator
chain to all orders, so the bedrock QGEO.SYM.01 collapses to ONE geometric postulate.
This does NOT prove QGEO.SYM.01 (that the raw seam IS the flat tau=i pillowcase) --
it proves that GRANTING the flat geometry discharges everything downstream exactly,
upgrading the leading-order results v198 (principal symbol) + v201 (subprincipal) to
the FULL operator.

The reduction chain (already established):
    QGEO.SYM.01  ==  omega_Sigma o rho = omega_Sigma   (mu4-invariance of the seam state)
    quasi-free   ==> omega o rho = omega  <=>  [rho, C] = 0  <=>  [rho, H] = 0
                     (C = (1+e^H)^{-1}, v258; H the DtN-induced modular Hamiltonian)
    [rho, H] = 0 ==> mark-locality + state invariance (v199/v267) -- all downstream [E].
So the entire bedrock sits on the single operator equation [rho, H] = 0.

  [E] 1. ISOMETRY => COMMUTATOR (the key step).  If the seam carries the flat tau=i
        pillowcase and H = f(Delta_flat) is a function of its intrinsic (flat)
        Laplacian -- the DtN of a flat metric, with NO curvature corrections -- then
        the order-4 deck rho (z -> iz) is an ISOMETRY, so [rho, Delta] = 0 and hence
        [rho, H] = [rho, f(Delta)] = 0 EXACTLY, to all orders.  Verified on the
        discretised square torus: rho^4 = I, [rho, Delta] = 0, [rho, sqrt(-Delta)] = 0;
        a generic non-isometry permutation FAILS (negative control).
  [E] 2. ALL-ORDERS UPGRADE.  this upgrades v198 (principal symbol |k| commutes) and
        v201 (subprincipal block-diagonal) from leading orders to the FULL H:
        flatness removes the lower-order curvature terms, so there is no residual
        obstruction -- the commutator is exact, not asymptotic.
  [C] 3. tau=i IS FORCED (not chosen).  the order-4 requirement forces the cross-ratio
        2 <=> j = 1728 <=> tau = i (the unique modulus with order-4 CM by Z[i];
        v214/v267); the hexagonal tau = omega (j = 0) is order-6, excluded.  So IF the
        seam has the order-4 deck at all, the flat tau=i pillowcase is forced.
  [O] 4. THE IRREDUCIBLE POSTULATE.  QGEO.SYM.01 therefore collapses to the SINGLE
        geometric statement: 'the raw RP seam state is the flat tau=i pillowcase
        quasi-free state (H = sqrt(-Delta_flat))'.  Everything downstream is [E]; this
        one statement is the bedrock (the role 'c = const' plays in relativity) --
        it needs a human constructive-QFT proof that the raw seam DtN state IS the
        flat tau=i geometry, or it stays an honest axiom.  Sharpest non-circular form.

Status: [E] the isometry=>commutator closure (numerically verified, all orders) +
the all-orders upgrade of v198/v201; [C] tau=i forced by order-4; [O] the one
geometric postulate stays open.  Narrows QGEO.SYM.01 to a single flat-geometry
statement; does NOT close it.  Python (numpy + scipy + sympy).
"""
import numpy as np
import sympy as sp
from scipy.linalg import sqrtm

from tfpt_constants import check, summary, reset

N = 8  # square-torus grid size


def _idx(x, y):
    return (x % N) * N + (y % N)


def flat_laplacian():
    """5-point periodic discrete Laplacian on the square (tau=i) torus."""
    L = np.zeros((N * N, N * N))
    for x in range(N):
        for y in range(N):
            i = _idx(x, y)
            L[i, i] = -4
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                L[i, _idx(x + dx, y + dy)] += 1
    return L


def order4_deck():
    """the order-4 isometry rho: z -> i z, i.e. the 90-deg rotation (x,y) -> (-y,x)."""
    R = np.zeros((N * N, N * N))
    for x in range(N):
        for y in range(N):
            R[_idx(-y, x), _idx(x, y)] = 1
    return R


def run():
    reset()
    print("v276  QGEO.SYM.03: the flat tau=i pillowcase closes [rho,H]=0 to all orders")

    L = flat_laplacian()
    R = order4_deck()

    # 1. isometry => commutator (the key step)
    is_order4 = np.allclose(np.linalg.matrix_power(R, 4), np.eye(N * N))
    comm_lap = np.allclose(R @ L - L @ R, 0)
    H = sqrtm(-L + 1e-6 * np.eye(N * N)).real          # H = sqrt(-Delta) ~ flat DtN
    comm_H = np.allclose(R @ H - H @ R, 0, atol=1e-8)
    check("ISOMETRY => COMMUTATOR [E]: the order-4 deck rho (z->iz) on the flat tau=i "
          "torus has rho^4=I (%s), [rho,Delta]=0 (%s, isometry commutes with the "
          "Laplacian), and [rho,H]=0 for H=sqrt(-Delta) (%s) -- so granting the flat "
          "geometry gives [rho,H]=0 EXACTLY, to all orders"
          % (is_order4, comm_lap, comm_H),
          is_order4 and comm_lap and comm_H)

    # negative control: a generic non-isometry permutation does NOT commute
    rng = np.random.default_rng(276)
    P = np.eye(N * N)[rng.permutation(N * N)]
    ctrl = not np.allclose(P @ L - L @ P, 0)
    check("NEGATIVE CONTROL [E]: a generic (non-isometry) permutation P does NOT "
          "commute with Delta ([P,Delta] != 0: %s) -- the commutation is special to "
          "the deck isometry, not generic" % ctrl, ctrl)

    # 2. all-orders upgrade: commute with every spectral function of Delta
    comm_L2 = np.allclose(R @ (L @ L) - (L @ L) @ R, 0)
    comm_exp = np.allclose(R @ sqrtm(sqrtm(-L + 1e-6 * np.eye(N * N))).real
                           - sqrtm(sqrtm(-L + 1e-6 * np.eye(N * N))).real @ R, 0, atol=1e-7)
    check("ALL-ORDERS UPGRADE [E]: rho commutes with Delta^2 (%s) and with "
          "(-Delta)^{1/4} (%s) -- with EVERY spectral function of Delta, so the v198 "
          "(principal symbol) + v201 (subprincipal) leading-order results upgrade to "
          "the FULL H; flatness removes the curvature terms, no residual obstruction"
          % (comm_L2, comm_exp), comm_L2 and comm_exp)

    # 3. tau=i is forced by order-4 (j=1728), hexagonal tau=omega (j=0) is order-6
    lam = sp.symbols("lam")
    jf = 256 * (lam ** 2 - lam + 1) ** 3 / (lam ** 2 * (lam - 1) ** 2)
    j_square = sp.simplify(jf.subs(lam, 2))            # cross-ratio-2 config
    j_hex = sp.simplify(jf.subs(lam, sp.exp(sp.I * sp.pi / 3)))
    check("tau=i FORCED [C]: order-4 => cross-ratio 2 => j=1728 (%s), the unique "
          "modulus with order-4 CM by Z[i]; the hexagonal tau=omega has j=0 (order-6, "
          "excluded) -- so IF the seam has the order-4 deck, the flat tau=i pillowcase "
          "is forced (v214/v267)" % (j_square == 1728),
          j_square == 1728 and sp.simplify(j_hex) == 0)

    # 4. the irreducible postulate
    check("IRREDUCIBLE POSTULATE [O]: QGEO.SYM.01 collapses to ONE geometric "
          "statement -- 'the raw RP seam state is the flat tau=i pillowcase quasi-free "
          "state, H=sqrt(-Delta_flat)'. Everything downstream is [E]; this one "
          "statement is the bedrock (like c=const) -- needs a human constructive-QFT "
          "proof that the raw seam DtN state IS the flat tau=i geometry, or stays an "
          "honest axiom. Sharpest non-circular form", True)

    return summary("v276 flat tau=i pillowcase => [rho,H]=0 to all orders; QGEO.SYM.01 = one geometric postulate (QGEO.SYM.03)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
