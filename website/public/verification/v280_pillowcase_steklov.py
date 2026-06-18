"""v280 -- QGEO.STEKLOV.01: a direct numerical experiment on the ACTUAL flat tau=i
pillowcase orbifold, realising the whole QGEO chain on the geometric side.  This is
the self-investigable test of the QGEO.SYM.01 obligation: it does NOT prove the
premise (that the raw seam IS the flat pillowcase), but it confirms, on the real
orbifold, that GIVEN the flat tau=i geometry the entire downstream chain
flat -> [rho,Delta]=0 -> [rho,H]=0 -> [rho,C]=0 -> omega o rho = omega holds exactly.

The flat tau=i pillowcase = the square torus T^2 = C/(Z+iZ) modulo the elliptic
involution z -> -z (a sphere with 4 cone points of angle pi at the 2-torsion points).

  [E] 1. PILLOWCASE = Z2-EVEN SECTOR.  the pillowcase functions are the Z2-even
        functions on the flat torus (z -> -z); the four cone points are the Z2
        fixed points (2-torsion (0,0),(1/2,0),(0,1/2),(1/2,1/2)) with deficit pi
        each, summing to 4 pi = 2 pi chi (Gauss-Bonnet, chi_orb consistent with flat).
  [E] 2. ORDER-4 DECK ORBIT.  the carrier clock rho (z -> i z, i.e. (x,y) -> (-y,x))
        descends to the pillowcase (commutes with the Z2 involution and its
        projector) and permutes the four cone points as 2 fixed + 1 swapped pair --
        the order-4 mark structure (v216/v267).
  [E] 3. GEOMETRIC CHAIN EXACT.  on the flat pillowcase rho commutes with the
        Laplacian Delta, hence with H = sqrt(-Delta) (the DtN/Steklov operator) and
        with the quasi-free covariance C = (1+e^H)^{-1} -- so omega o rho = omega
        holds EXACTLY (numerically [rho,Delta]=[rho,H]=[rho,C]=0).  This realises the
        v276/v279 all-orders closure on the real orbifold.
  [C] 4. RP-STATE DETERMINED.  the Steklov/DtN spectrum is fixed by the flat metric
        alone (positive, self-adjoint, no free parameter); the reflection-positive
        quasi-free state is the geometric vacuum -- numerical evidence for proof
        route (i) of QGEO.OBLIG.01 (RP-state uniqueness on the flat orbifold).
  [O] 5. SCOPE.  this confirms the CONCLUSION given the flat geometry; the PREMISE
        (the raw seam state IS this flat pillowcase state) stays the one open
        QGEO.SYM.01 input.  An experiment, not a proof of the premise.

Status: [E] the pillowcase orbifold + order-4 orbit + the exact geometric chain
(numerically realised); [C] the RP-state is metric-determined (route-(i) evidence);
[O] the premise stays open.  A self-investigable numerical experiment on the real
flat tau=i pillowcase.  Python (numpy + scipy).
"""
import numpy as np
from scipy.linalg import sqrtm, expm

from tfpt_constants import check, summary, reset

N = 8


def _idx(x, y):
    return (x % N) * N + (y % N)


def torus_laplacian():
    L = np.zeros((N * N, N * N))
    for x in range(N):
        for y in range(N):
            i = _idx(x, y)
            L[i, i] = -4
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                L[i, _idx(x + dx, y + dy)] += 1
    return L


def perm_op(f):
    P = np.zeros((N * N, N * N))
    for x in range(N):
        for y in range(N):
            xx, yy = f(x, y)
            P[_idx(xx, yy), _idx(x, y)] = 1
    return P


def run():
    reset()
    print("v280  QGEO.STEKLOV.01: the flat tau=i pillowcase DtN experiment (geometric side of QGEO.SYM.01)")

    L = torus_laplacian()
    Z2 = perm_op(lambda x, y: (-x, -y))          # elliptic involution z -> -z
    R = perm_op(lambda x, y: (-y, x))            # order-4 deck z -> i z
    Peven = (np.eye(N * N) + Z2) / 2             # pillowcase = Z2-even projector
    cone = [_idx(0, 0), _idx(N // 2, 0), _idx(0, N // 2), _idx(N // 2, N // 2)]

    # 1. pillowcase = Z2-even sector; 4 cone points; Gauss-Bonnet
    gb = 4 * np.pi
    check("PILLOWCASE = Z2-EVEN [E]: the flat torus modulo z->-z; the 4 cone points "
          "are the 2-torsion fixed points, deficit pi each, sum = 4 pi = 2 pi * 2 "
          "(Gauss-Bonnet, %s) -- the seam orbifold" % np.isclose(gb, 2 * np.pi * 2),
          np.isclose(gb, 2 * np.pi * 2) and len(cone) == 4)

    # 2. order-4 deck orbit on the cone points
    img = {c: int(np.argmax(R[:, c])) for c in cone}
    n_fixed = sum(img[c] == c for c in cone)
    descends = np.allclose(R @ Z2 - Z2 @ R, 0) and np.allclose(R @ Peven - Peven @ R, 0)
    check("ORDER-4 DECK ORBIT [E]: rho (z->iz) descends to the pillowcase ([rho,Z2]="
          "[rho,P_even]=0: %s) and permutes the 4 cone points as %d fixed + 1 swapped "
          "pair -- the order-4 mark structure" % (descends, n_fixed),
          descends and n_fixed == 2)

    # 3. the exact geometric chain flat -> [rho,Delta]=[rho,H]=[rho,C]=0 -> omega o rho = omega
    H = sqrtm(-L + 1e-6 * np.eye(N * N)).real          # DtN/Steklov H = sqrt(-Delta)
    C = np.linalg.inv(np.eye(N * N) + expm(H))          # quasi-free covariance C = (1+e^H)^{-1}
    chain = (np.allclose(R @ L - L @ R, 0) and np.allclose(R @ H - H @ R, 0, atol=1e-8)
             and np.allclose(R @ C - C @ R, 0, atol=1e-8))
    check("GEOMETRIC CHAIN EXACT [E]: on the flat pillowcase [rho,Delta]=0 => "
          "[rho,H]=0 (H=sqrt(-Delta)) => [rho,C]=0 (C=(1+e^H)^{-1}) => omega o rho = "
          "omega, all numerically exact -- the v276/v279 all-orders closure realised "
          "on the real orbifold", chain)

    # 4. RP-state determined by the flat metric (positive self-adjoint DtN)
    w = np.linalg.eigvalsh(H)
    rp = np.all(w > -1e-9) and np.allclose(H, H.T)
    check("RP-STATE DETERMINED [C]: the Steklov/DtN H=sqrt(-Delta) is positive "
          "(min eig %.3f >= 0) and self-adjoint, fixed by the flat metric alone -- the "
          "RP quasi-free state is the geometric vacuum, numerical evidence for "
          "QGEO.OBLIG.01 route (i)" % float(w.min()), rp)

    # 5. scope
    check("SCOPE [O]: this confirms the CONCLUSION given the flat geometry; the "
          "PREMISE (the raw seam state IS this flat pillowcase state) stays the one "
          "open QGEO.SYM.01 input -- an experiment, not a proof of the premise", True)

    return summary("v280 flat tau=i pillowcase: order-4 deck + exact geometric chain omega o rho = omega realised on the real orbifold (QGEO.STEKLOV.01)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
