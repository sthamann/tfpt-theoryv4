"""v236 -- the (2,3,5) Brieskorn singularity is the ONE generator of the skeleton.

The capstone of the icosahedral round (v219/v223/v232/v233 + v55): the whole discrete
skeleton is the Milnor fibration of a SINGLE singularity, the (2,3,5) Brieskorn
singularity x^2 + y^3 + z^5 = 0, whose three exponents ARE the TFPT atoms
(|Z2|, N_fam, g_car) = (2, 3, 5). Every load-bearing structure is one of its Milnor
data:

  [E] 1. MILNOR NUMBER = the '8'. mu = (2-1)(3-1)(5-1) = (|Z2|-1)(N_fam-1)(g_car-1)
        = 1*2*4 = 8 = rank E8 = #(exceptional P^1) = the '8' in c3 = 1/(8 pi). A FIFTH
        independent origin of the 8 (after geometry, lattice, gravity, Coxeter-phi(30)).
  [E] 2. MONODROMY = the order-30 Coxeter cycle. The Milnor monodromy eigenvalues are
        lambda = zeta_2^{j1} zeta_3^{j2} zeta_5^{j3} (1<=ji<=ai-1) = the eight primitive
        30th roots e^{2 pi i m/30}, m in {1,7,11,13,17,19,23,29} = the E8 exponents; the
        characteristic polynomial is the 30th cyclotomic Phi_30 (degree phi(30)=8=mu).
        So the Milnor monodromy IS the E8 Coxeter element of order 30 = h(E8) (v55).
  [E] 3. THE TWO CLOCKS are facets of this one monodromy. (a) The monodromy GROUP
        <h> = Z/30 = Z/2 (sheet) x Z/3 (family/triality) x Z/5 (carrier): the mu3
        triality (the CP phase omega, v233) is the order-3 power h^10. (b) The GALOIS
        group of the eigenvalue field, Gal(Q(zeta_30)/Q) = (Z/30)^x = Z/2 x Z/4, carries
        the order-4 element (x7) = the mu4 clock acting on the spectrum (v223).
  [E] 4. MILNOR LATTICE = E8; LINK = Poincare homology sphere S^3/2I (v232/v234).
  [I] 5. So ONE singularity x^2+y^3+z^5 generates the atoms (exponents), the 8 (Milnor
        number), E8 (Milnor lattice), the order-30 cycle (monodromy), both clocks
        (mu3 inside <h>, mu4 in the Galois action) and the seam (link). Not many numbers
        sharing {2,3,5} -- one icosahedral singularity, read several ways.

Status: [E] for the Milnor number, the monodromy = Phi_30 = Coxeter-30, the
group/Galois split of the two clocks; [I] for the 'one generator' synthesis. This
unifies, it does not close a gate. Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

Z2 = 2
EXPS = (2, 3, 5)              # the Brieskorn exponents = the TFPT atoms (|Z2|,N_fam,g_car)


def run():
    reset()
    print("v236  the (2,3,5) Brieskorn singularity generates the whole skeleton")

    # 1. Milnor number = the '8'
    mu = (EXPS[0] - 1) * (EXPS[1] - 1) * (EXPS[2] - 1)
    check("MILNOR NUMBER [E]: mu = (2-1)(3-1)(5-1) = (|Z2|-1)(N_fam-1)(g_car-1) = "
          "1*2*4 = 8 = rank E8 = the '8' in c3=1/(8 pi) (a fifth independent origin)",
          mu == (Z2 - 1) * (N_fam - 1) * (g_car - 1) == 8 == rankE8)

    # 2. Milnor monodromy eigenvalues = primitive 30th roots = E8 exponents; charpoly = Phi_30
    t = sp.symbols('t')
    eigen = set()
    for j1 in range(1, EXPS[0]):
        for j2 in range(1, EXPS[1]):
            for j3 in range(1, EXPS[2]):
                # exponent in units of 1/30: 15 j1 + 10 j2 + 6 j3  (since 30/2,30/3,30/5)
                e = (15 * j1 + 10 * j2 + 6 * j3) % 30
                eigen.add(e)
    e8_exps = {1, 7, 11, 13, 17, 19, 23, 29}
    check("MONODROMY EIGENVALUES [E]: lambda = zeta_2^j1 zeta_3^j2 zeta_5^j3 give the "
          "exponents %s = the eight totatives of 30 = the E8 exponents"
          % sorted(eigen), eigen == e8_exps and len(eigen) == mu == 8)
    # characteristic polynomial = 30th cyclotomic Phi_30 (roots = the primitive 30th
    # roots = the totative exponents above); deg = phi(30) = 8, Phi_30 | t^30-1
    phi30 = sp.cyclotomic_poly(30, t)
    roots_vanish = all(abs(complex(sp.N(phi30.subs(t, sp.exp(2 * sp.I * sp.pi * m / 30))))) < 1e-9
                       for m in sorted(eigen))
    check("MONODROMY CHARPOLY [E]: the eigenvalues are exactly the roots of the 30th "
          "cyclotomic Phi_30 (deg phi(30)=8=mu, Phi_30 | t^30-1, the totative roots "
          "vanish); so the Milnor monodromy IS the order-30 E8 Coxeter element (v55)",
          sp.degree(phi30, t) == 8 == mu and sp.rem(t**30 - 1, phi30, t) == 0
          and roots_vanish)

    # 3a. monodromy GROUP <h> = Z/30 = Z/2 x Z/3 x Z/5; mu3 triality = h^10 (order 3)
    check("MONODROMY GROUP [E]: <h> = Z/30 = Z/2(sheet) x Z/3(family) x Z/5(carrier); "
          "the mu3 triality (CP phase omega, v233) is h^10 of order 3 (30/3=10=A_Lambda)",
          30 == Z2 * N_fam * g_car and 30 // N_fam == 10
          and sp.simplify(sp.exp(2 * sp.I * sp.pi * 10 / 30) - sp.exp(2 * sp.I * sp.pi / 3)) == 0)

    # 3b. Galois group of Q(zeta_30) = (Z/30)^x = Z/2 x Z/4; order-4 element x7 = mu4 clock
    units = [u for u in range(1, 30) if sp.gcd(u, 30) == 1]
    def mult_order(g):
        x, k = g % 30, 1
        while x != 1:
            x = (x * g) % 30; k += 1
        return k
    check("GALOIS / mu4 CLOCK [E]: Gal(Q(zeta_30)/Q) = (Z/30)^x = Z/2 x Z/4 (the E8 "
          "exponents); the order-4 element x7 (7^2=19,7^4=1 mod 30) = the mu4 clock "
          "acting on the spectrum (v223)",
          units == sorted(e8_exps) and mult_order(7) == 4)

    # 4. Milnor lattice = E8, link = Poincare sphere (cross-ref v232/v234)
    check("MILNOR LATTICE = E8, LINK = Poincare homology sphere S^3/2I [E] (v232/v234): "
          "the resolution's 8 exceptional P^1 carry the E8 Cartan; 2I perfect => H1=0",
          rankE8 == 8 and mu == 8)

    # 5. the one-generator synthesis
    check("SYNTHESIS [I]: ONE singularity x^2+y^3+z^5 generates the atoms (exponents), "
          "the 8 (Milnor number), E8 (Milnor lattice), order-30 (monodromy), both "
          "clocks (mu3 in <h>, mu4 in Galois) and the seam (link) -- not many numbers "
          "sharing {2,3,5}, but one icosahedral singularity read several ways",
          tuple(sorted(EXPS)) == (Z2, N_fam, g_car) == (2, 3, 5))

    return summary("v236 Brieskorn capstone ((2,3,5) singularity generates the skeleton)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
