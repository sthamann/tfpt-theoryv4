"""EXPLORATION (experiments/ only -- NOT a suite module, NOT in the ledger/papers).

Hypothesis under test: "pi itself contains the black hole's information and feeds
the compiler -- and how does that connect to E8?"

Honest verdict (see prints): pi DOES feed the compiler, but as exactly ONE real
constant -- the seam normalizer 1/(8 pi) (and its sibling 1/(6 pi) = (4/3)c3).
It is irreducible compiler fuel (dimensionless alpha^-1 genuinely shifts with pi),
NOT a removable unit. But pi does NOT "contain" the black-hole information in any
non-trivial sense: the information-recovery DYNAMICS are the discrete, pi-FREE
transfer operator (spec {1,(2/3)^6,(1/3)^6}); pi only carries the entropy
MAGNITUDE (area). pi and E8 are the CONTINUOUS and DISCRETE halves of the boundary
data, meeting at the seam 2-surface (c3*8pi = 1). The "pi is mystical / contains
everything" reading is the Library-of-Babel fallacy and is rejected.
"""
import mpmath as mp

mp.mp.dps = 40
PI = mp.pi
C3 = 1 / (8 * PI)
GCAR, NFAM, Z2, MU4, DIMSP = 5, 3, 2, 4, 16


def alpha_inv(piv):
    """alpha^-1 as the root of F_{U(1)}=0 with pi = piv (to test pi-dependence)."""
    cc = 1 / (8 * piv); pb = 1 / (6 * piv); dt = 48 * cc**4
    def ps(a):
        Q = dt * mp.e**(-2 * a)
        return pb + Q * (1 - Q)**(mp.mpf(-5) / 4)
    F = lambda a: a**3 - 2 * cc**3 * a**2 - (mp.mpf(4) / 5) * cc**6 * 41 * mp.log(1 / ps(a))
    return 1 / mp.findroot(F, mp.mpf("0.0073"))


def sec(t):
    print("\n" + "=" * 72 + "\n" + t + "\n" + "=" * 72)


def main():
    sec("(1) DOES pi FEED THE COMPILER?  YES -- as exactly ONE constant 1/(8 pi)")
    print(f"alpha^-1(pi)        = {float(alpha_inv(PI)):.10f}")
    print(f"alpha^-1(1.01*pi)   = {float(alpha_inv(PI * mp.mpf('1.01'))):.10f}")
    print("  -> the DIMENSIONLESS alpha^-1 shifts with pi, so pi is a GENUINE input")
    print("     (via c3=1/(8pi)), not a removable unit. But it enters ONLY as 1/(k pi):")
    print(f"     c3 = 1/(8 pi),  phi_base = 1/(6 pi) = (4/3)c3 = {float(mp.mpf(4)/3*C3):.6f}")
    print("  CONCLUSION: pi is the minimal continuous 'fuel' = the seam-area normalizer.")

    sec("(2) DOES pi 'CONTAIN' THE BLACK-HOLE INFORMATION?  NO (two honest reasons)")
    print("(a) Library of Babel: pi is (conjectured) normal -> its digits contain every")
    print("    finite string. But that is TRUE OF ALL normal numbers and is information-")
    print("    theoretically vacuous. The compiler reads pi as ONE real, not a digit oracle.")
    print("(b) What is real: BH entropy S = Area/4 = pi r^2 carries pi via the 2-sphere AREA")
    print("    -- the SAME geometric pi as c3=1/(8pi). So pi carries the entropy MAGNITUDE,")
    print("    but the information DYNAMICS (the Page recovery) are the discrete operator:")
    lam2 = (mp.mpf(2) / 3)**6
    print(f"    spec(T) = {{1, (2/3)^6, (1/3)^6}}, recovery rate (2/3)^6 = {float(lam2):.6f} -- pi-FREE.")
    print("  CONCLUSION: pi = entropy area-scale; the actual information lives in the")
    print("              discrete (E8/anchor) recovery operator, with no pi in it.")

    sec("(3) HOW IT CONNECTS TO E8  --  continuous & discrete halves meet at the seam")
    print("DISCRETE half: anchor a=(1,1,2) -> E8 (rank 8, 240 roots, 248), and the")
    print("               recovery dynamics (2/3)^6 -- all pi-FREE.")
    print("CONTINUOUS half: pi -> c3 = 1/(8 pi), the ONE seam-2-sphere normalizer.")
    print(f"They MEET at the seam 2-surface:  c3 * 8 pi = {float(C3 * 8 * PI):.1f}  (the seam action = 1).")
    print("Inside E8, pi appears ONLY as a continuous MEASURE on the discrete lattice:")
    print("  - modular nome q = exp(2 pi i tau); the (E8)_1 character is E4/eta^8 = 1+248q+...")
    pack = PI**4 / 384
    print(f"  - E8 sphere-packing density = pi^4/384 = {float(pack):.6f} (Viazovska, dim 8)")
    print(f"    [coincidence, NOT promoted: 384 = 2*dim S+ * |mu4| * N_fam = {2*DIMSP*MU4*NFAM};")
    print("     a small-integer factoring -- exactly the look-elsewhere trap v100 guards against]")
    print("  -> pi never STORES E8's information; it normalizes the surface E8 lives on.")

    sec("VERDICT (firewall)")
    print("The defensible, non-mystical core of the hypothesis:")
    print("  TFPT = ONE discrete program (anchor -> E8) + ONE continuous primitive (pi).")
    print("  pi is the minimal continuous fuel (one real: the seam-area normalizer 1/(8pi)),")
    print("  E8 is the discrete program. The black hole's INFORMATION is in the discrete")
    print("  recovery operator (E8 side); pi only sets the entropy's area scale.")
    print("  => pi does NOT 'contain' the information -- it supplies the single continuous")
    print("     normalization the discrete E8-compiler needs. The 'pi contains everything'")
    print("     reading is the Library-of-Babel fallacy and is rejected. Stays in experiments/.")


if __name__ == "__main__":
    main()
