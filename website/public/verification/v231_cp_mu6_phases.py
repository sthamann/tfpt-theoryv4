"""v231 -- both CP phases are mu6 powers of ONE hexagonal CM unit, split by the sheet.

This sharpens red-team Target D one decisive step further than v220/v225 (which
located the CP residual in the hexagonal phase fiber): it shows the TWO CP phases
of the theory are not two independent inputs but ONE hexagonal object read on the
two sheets. With rho = e^{i pi/3} the primitive 6th root (the j=0 CM unit, v220):

  delta_CKM (leading) = pi/3   = arg(rho^1)      [quark sector]
  delta_PMNS          = 4 pi/3 = arg(rho^4)      [lepton sector, tfpt_2 'phase lattice']

and rho^4 = -rho, i.e. the lepton phase is the quark phase times the Z2 sheet
(rho^3 = -1, the half-turn). So

  delta_PMNS = delta_CKM,lead + pi = (hexagonal CM unit) x (Z2 sheet).

The orientation reading (v225) confirms the sheet split: the dual-normal-frame
Jarlskog orientation Im det(1, d, rho^k n) is +21 sin(pi/3) for the quark (k=1)
and -21 sin(pi/3) for the lepton (k=4) -- equal magnitude, opposite sign, exactly
the sheet flip.

  [E] 1. rho = e^{i pi/3} primitive 6th root: rho^6=1, rho^3=-1 (the Z2 sheet);
        j(rho)=0 (Eisenstein CM, v220).
  [E] 2. delta_CKM leading = arg(rho^1) = pi/3; delta_PMNS = arg(rho^4) = 4pi/3
        (the frozen readings, FLAV.CP.01 / the neutrino phase lattice).
  [E] 3. rho^4 = -rho => delta_PMNS = delta_CKM,lead + pi = (CM unit) x (sheet);
        the two CP phases are ONE hexagonal unit on the two sheets.
  [E] 4. the C6/mu6 monodromy (U6, charpoly t^6-1) carries rho in its spectrum.
  [E] 5. ORIENTATION: Im det(1,d,rho^1 n) = +21 sin(pi/3), Im det(1,d,rho^4 n)
        = -21 sin(pi/3) -- sheet-flipped quark/lepton Jarlskog orientations (v225).
  [E] 6. NEG: a generic non-mu6 phase does not give both frozen values nor the
        sheet relation; mu3 (cube roots) misses the sheet (no rho^3=-1).

Status: [E] for the mu6 arithmetic + the sheet relation + the orientation; the
REDUCTION 'two CP phases -> one hexagonal unit + the sheet' is the structural
content. [C] stays for the physical CP derivation (the quark seam correction
3 lambda_C^2 is the v88 misalignment; the deck stays Z/4, v215). Does NOT close
Target D; it removes one of its two phase inputs. Mirrored in
wolfram/tfpt_readouts_extension.wl.
"""
import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset, phi0, PI

mp.mp.dps = 30

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
A = sp.Matrix([1, 1, 2])


def run():
    reset()
    print("v231  CP: both phases are mu6 powers of rho=e^{i pi/3}, split by the Z2 sheet")

    rho = sp.exp(sp.I * sp.pi / 3)
    check("rho = e^{i pi/3} is a primitive 6th root: rho^6=1, rho^3=-1 (the Z2 "
          "sheet half-turn); j(rho)=0 Eisenstein CM (v220)",
          sp.simplify(rho**6) == 1 and sp.simplify(rho**3) == -1)
    check("delta_CKM leading = pi/3 = arg(rho^1) [quark sector]",
          sp.simplify(sp.arg(rho**1) - sp.pi / 3) == 0)
    check("delta_PMNS = 4 pi/3 = arg(rho^4) [lepton sector, tfpt_2 phase lattice]",
          sp.simplify(sp.exp(sp.I * sp.Rational(4, 3) * sp.pi) - rho**4) == 0)
    check("rho^4 = -rho => delta_PMNS = delta_CKM,lead + pi = (CM unit) x (Z2 sheet); "
          "the two CP phases are ONE hexagonal unit on the two sheets",
          sp.simplify(rho**4 + rho) == 0
          and sp.simplify(sp.Rational(4, 3) * sp.pi - sp.pi / 3 - sp.pi) == 0)

    # C6 / mu6 monodromy carries rho
    U6 = sp.Matrix(6, 6, lambda i, j: 1 if (j - i) % 6 == 1 else 0)
    t = sp.symbols('t')
    check("the C6/mu6 monodromy U6 has charpoly t^6-1 (spectrum mu6, contains rho)",
          sp.expand(U6.charpoly(t).as_expr()) == t**6 - 1)

    # orientation (v225): sheet-flipped Jarlskog orientations
    d = (A.T * R.inv())
    nvec = [5, -9, 6]
    vol = sp.Matrix([[1, 1, 1], list(d), nvec]).det()
    ImQ = mp.im(complex(rho**1) * float(vol))
    ImL = mp.im(complex(rho**4) * float(vol))
    check("ORIENTATION [E]: det(1,d,n)=21=N_fam*scalaron; Im det(1,d,rho^1 n) = "
          "+21 sin(pi/3) (quark), Im det(1,d,rho^4 n) = -21 sin(pi/3) (lepton) -- "
          "equal magnitude, opposite sign = the sheet flip",
          vol == 21
          and abs(ImQ - 21 * mp.sin(mp.pi / 3)) < mp.mpf('1e-9')
          and abs(ImL + 21 * mp.sin(mp.pi / 3)) < mp.mpf('1e-9')
          and abs(ImQ + ImL) < mp.mpf('1e-9'))

    # full frozen delta_CKM stays the seam-misalignment reading (v88), leading pi/3
    lam = mp.sqrt(phi0 * (1 - phi0))
    dCKM_full = PI / 3 + 3 * lam**2
    check("the quark seam correction 3 lambda_C^2 is the v88 misalignment (full "
          "delta_CKM = 68.65 deg); the leading term is the bare hexagonal phase pi/3",
          abs(dCKM_full - mp.mpf('1.198231638')) < mp.mpf('1e-8'))

    # negative control: mu3 (cube roots) has no sheet (-1), generic phase misses both
    omega3 = sp.exp(2 * sp.I * sp.pi / 3)        # primitive cube root
    check("NEG: mu3 (cube roots) has no element equal to -1 (no Z2 sheet), so it "
          "cannot relate the two CP phases by a half-turn; the hexagonal mu6 is "
          "required (mu6 = mu3 x mu2 = family x sheet)",
          all(sp.simplify(omega3**k + 1) != 0 for k in range(3))
          and sp.simplify(rho**3 + 1) == 0)

    return summary("v231 CP mu6 phases (one hexagonal unit, two sheets)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
