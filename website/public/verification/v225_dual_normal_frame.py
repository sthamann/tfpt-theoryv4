"""v225 -- the dual normal frame (d, n): one boundary compass for flavor + horizon.

The horizon documents carry the dual anchor d = a^T R^{-1} = a^T L^{-1} =
(-1/2,-1/2,1), proportional to the Nariai traceless root (1,1,-2) (v103/v149),
and the torsion normal n = (5,-9,6), the first-generation selector with
n^T R = (8,0,0), n^T L = (20,0,0) (v136).  This script states the pair (d, n) as a
canonical NORMAL FRAME: flavor and horizon readouts are read through (d, n), not
through (R, L) directly, and the oriented volume det(1, d, n) is the natural seat
of orientation -- i.e. of CP.

  [E] 1. d = a^T R^{-1} = a^T L^{-1} = (-1/2,-1/2,1) (frame-independent across the
        mass and transport operators).
  [E] 2. d . 1 = 0 (kills the democratic direction), d . a = 1 (normalised on the
        anchor); d = -1/2 (1,1,-2) = -1/2 * Nariai traceless anchor (horizon normal).
  [E] 3. n = (5,-9,6): n^T R = (det R, 0,0) = (8,0,0), n^T L = (det L, 0,0) =
        (20,0,0) -- n annihilates the stable columns 2,3 and reads the determinant
        on the first-generation column (torsion / first-generation selector).
  [E] 4. ORIENTED VOLUME det(1, d, n) = 21 = N_fam * scalaron = 3 * 7 (the frame
        is non-degenerate; the two normals plus the democratic line span).
  [C] 5. CP AS ORIENTATION: rotating the frame by the hexagonal CM unit
        rho = e^{i pi/3} (v220) gives Im det(1, d, rho n) = 21 sin(pi/3) != 0 --
        a candidate Jarlskog/CP orientation object.  CP sits exactly where the
        magnitude logic fails (red team Target D): in the orientation of the
        normal frame, NOT in the magnitudes.  Typed [C], not a CP derivation.

Status: [E] for the normal frame; [C] for the CP-orientation reading.  Mirrored
(rational parts) in wolfram/tfpt_readouts_extension.wl.
"""
import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
L = K + Q
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])
SCALARON = 7


def run():
    reset()
    print("v225  dual normal frame (d, n): boundary compass for flavor + horizon")

    d = (A.T * R.inv())
    dL = (A.T * L.inv())
    check("d = a^T R^{-1} = (-1/2,-1/2,1)",
          list(d) == [sp.Rational(-1, 2), sp.Rational(-1, 2), 1])
    check("d = a^T L^{-1} = (-1/2,-1/2,1) too (frame-independent across R and L)",
          list(dL) == [sp.Rational(-1, 2), sp.Rational(-1, 2), 1])
    check("d . 1 = 0 (kills democratic direction)", (d * ONE)[0] == 0)
    check("d . a = 1 (normalised on the anchor)", (d * A)[0] == 1)
    check("d = -1/2 (1,1,-2) = -1/2 * Nariai traceless anchor (horizon normal)",
          d.T == sp.Rational(-1, 2) * sp.Matrix([1, 1, -2]))

    n = sp.Matrix([[5, -9, 6]])
    check("n = (5,-9,6): n^T R = (det R, 0, 0) = (8,0,0) (first-generation column = det R)",
          list(n * R) == [R.det(), 0, 0] == [8, 0, 0])
    check("n^T L = (det L, 0, 0) = (20,0,0); n annihilates the stable columns 2,3",
          list(n * L) == [L.det(), 0, 0] == [20, 0, 0])

    # oriented volume of the frame {1, d, n}
    frame = sp.Matrix([[1, 1, 1],
                       list(d),
                       [5, -9, 6]])
    vol = frame.det()
    check("ORIENTED VOLUME det(1, d, n) = 21 = N_fam * scalaron = 3 * 7 "
          "(non-degenerate frame)", vol == 21 == N_fam * SCALARON)

    # ---- [C] CP as orientation under the hexagonal CM rotation rho = e^{i pi/3} ----
    rho = mp.e**(1j * mp.pi / 3)
    # det(1, d, rho n) = rho * det(1,d,n) since rho scales the third row linearly
    im_part = mp.im(rho * float(vol))
    check("CP ORIENTATION [C]: Im det(1, d, rho*n) = 21 sin(pi/3) = %.4f != 0 "
          "(rho = e^{i pi/3}, the hexagonal CM unit, v220); CP lives in the "
          "orientation of the normal frame, where the magnitude bijection "
          "(Target D) fails -- candidate Jarlskog object, typed [C]"
          % float(im_part),
          abs(im_part - 21 * mp.sin(mp.pi / 3)) < mp.mpf('1e-9') and im_part > 0)

    return summary("v225 dual normal frame (d,n) + CP orientation")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
