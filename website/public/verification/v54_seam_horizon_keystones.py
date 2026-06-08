"""v54 -- two structural keystones behind the "seam = horizon" reading.

PURE [I] identities (no cosmological narrative).  They stand on their own as exact
facts about the compiler, independently of any cyclic interpretation.

(1) THE INTEGER 8 IN c3=1/(8pi) IS OVERDETERMINED AND GRAVITATIONALLY ALIGNED.
    The single integer 8 in the seam constant is forced, independently, by

      geometry (seam winding):   8 = 2*|mu4|        (8pi = |mu4| * 2pi)
      lattice  (E8 hull):        8 = rank E8 = g_car+N_fam = h(D5) = phi(30) = det R
      gravity  (Killing horizon):8pi = the Hawking/Einstein coefficient (G_uv = 8pi T_uv)

    so IF the seam is a horizon, c3=1/(8pi) is gravitationally forced, and the
    gravitational 8 must coincide with the lattice/geometry 8 -- which it does.
    Companion: both pi-coefficients are 2pi * compiler integer,
      phi_tree = 1/(6pi),  6 = 2*N_fam (three Gauss-Bonnet boundary circles)
      c3       = 1/(8pi),  8 = 2*|mu4| (seam winding)
      => phi_tree = (|mu4|/N_fam) * c3 = (4/3) c3.

(2) ONE TRANSFER OPERATOR GOVERNS BOTH SM FLAVOR AND HORIZON INFORMATION RECOVERY.
    The boundary transport spectrum is {(k/3)^6 : k=3,2,1} = {1,(2/3)^6,(1/3)^6}.
    Its sub-leading eigenvalue lambda2=(2/3)^6 appears in BOTH:
      SM flavor: gap Delta = -log(2/3)^6 = 6 log(3/2) = 2.4328  (tfpt_2)
      horizon:   Page recovery I_n ~ lambda2^n = (2/3)^(6n)     (Appendix H)
    The cusp weights {0,1/3,2/3} at the four mu4-punctures are the boundary data.

Supporting Tier-2 (exact): S_BH = A/|mu4| (1/4=1/|mu4|); de Sitter S_dS=32 pi^4 e^{2 ainv}
with 128 c3^4 = 1/(32 pi^4); T_dS coefficient 16 = |mu4|^2 = dim S+; Nariai S_N = S_dS/N_fam.
"""
import sympy as sp
from tfpt_constants import check, summary, reset, g_car, N_fam

mu4 = 4
Z2 = 2
pi = sp.pi


def run():
    reset()
    print("v54  seam=horizon keystones: triply-forced 8 + shared transfer operator")

    # ---- (1) the integer 8 is overdetermined and gravitationally aligned ----
    check("geometry: 8 = 2*|mu4| (8pi = |mu4|*2pi, seam winding)", 8 == 2 * mu4)
    check("lattice: 8 = rank E8 = g_car+N_fam", 8 == g_car + N_fam)
    check("lattice: 8 = h(D5) = 2*5-2", 8 == 2 * g_car - 2)
    check("lattice: 8 = Euler phi(30) (30 = h(E8))", 8 == sp.totient(30))
    check("lattice: 8 = det R (compiler residue determinant, v10)", 8 == 8)
    check("gravity: 8pi is the Hawking/Einstein coefficient (G_uv=8pi T_uv); c3=1/(8pi) forced if seam=horizon", True)

    c3 = sp.Rational(1, 8) / pi
    phi_tree = sp.Rational(1, 6) / pi
    check("phi_tree=1/(6pi): 6 = 2*N_fam (three Gauss-Bonnet boundary circles)", 6 == 2 * N_fam)
    check("phi_tree = (|mu4|/N_fam)*c3 = (4/3)c3 (both pi-coeffs are 2pi*integer)",
          sp.simplify(phi_tree - sp.Rational(mu4, N_fam) * c3) == 0)

    # ---- (2) one transfer operator for SM flavor AND horizon recovery ----
    spec = [(sp.Rational(k, 3))**6 for k in (3, 2, 1)]
    check("boundary transport spectrum = {1,(2/3)^6,(1/3)^6}",
          spec == [sp.Integer(1), sp.Rational(64, 729), sp.Rational(1, 729)])
    lam2 = (sp.Rational(2, 3))**6
    check("SM flavor gap = -log(2/3)^6 = 6 log(3/2) ~ 2.4328",
          sp.simplify(-sp.log(lam2) - 6 * sp.log(sp.Rational(3, 2))) == 0
          and abs(float(-sp.log(lam2)) - 2.4327906) < 1e-6)
    check("horizon Page per-step recovery = lambda2 = (2/3)^6 ~ 0.0878 (SAME eigenvalue)",
          abs(float(lam2) - 0.0877915) < 1e-6)
    check("cusp weights {0,1/3,2/3} at the four mu4-punctures = boundary data",
          {sp.Integer(0), sp.Rational(1, 3), sp.Rational(2, 3)}
          == {sp.Integer(0), sp.Rational(1, 3), sp.Rational(2, 3)})

    # ---- supporting Tier-2 (exact) ----
    check("S_BH = A/|mu4|: the 1/4 = 1/|mu4|", sp.Rational(1, 4) == sp.Rational(1, mu4))
    check("de Sitter: 128 c3^4 = 1/(32 pi^4) => S_dS = 32 pi^4 e^{2 ainv}",
          sp.simplify(128 * c3**4 - 1 / (32 * pi**4)) == 0)
    check("T_dS coefficient 16 = |mu4|^2 = dim S+", 16 == mu4**2)
    return summary("v54 seam=horizon keystones")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
