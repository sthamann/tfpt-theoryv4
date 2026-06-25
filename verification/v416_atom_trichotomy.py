"""v416 -- The atom trichotomy: {2,3,5} are ramified / inert / split in the two
exceptional CM rings, and each atom is the unique ramified prime of one
quadratic facet of the order-30 clock field (v403).  This sharpens v222/v230
(which read the atoms only as CM NORMS) and v390/v394/v403 (the three facets)
into one prime-splitting table.  [E] number theory, [C] the seam/flavor/golden
reading.

The atoms are e3,p0,e2 of the anchor a=(1,1,2): |Z2|=2, N_fam=3, g_car=5, with
product 2*3*5 = 30 = h(E8) (v394).

  [E] 1. THE Z[i] (SQUARE / SEAM, tau=i) TRICHOTOMY:
             2 = |Z2|   RAMIFIES   (2 = -i(1+i)^2; 2 | disc Q(i) = -4),
             3 = N_fam  INERT      (3 = 3 mod 4; norm 9 = N_fam^2),
             5 = g_car  SPLITS     (5 = (2+i)(2-i); 5 = 1 mod 4).
         So on the square seam the carrier rank g_car=5 FACTORS.
  [E] 2. THE Z[omega] (HEX / FLAVOR, tau=omega) TRICHOTOMY:
             3 = N_fam  RAMIFIES   (3 = -omega^2 (1-omega)^2; N(1-omega)=3),
             2 = |Z2|   INERT      (2 = 2 mod 3; norm 4),
             5 = g_car  INERT      (5 = 2 mod 3; norm 25 = g_car^2).
  [E] 3. RAMIFIED PRIME = THE 'OWN' ATOM.  The discriminant prime of each ring
         is exactly the atom that belongs to it: Z[i] ramifies at 2 = |Z2|
         (sheet/seam), Z[omega] ramifies at 3 = N_fam (family/flavor).
  [E] 4. THE THREE FACETS (v403) RAMIFY OVER ONE ATOM EACH:
             Q(i)      disc -4  -> ramified only over 2   (square/seam, mu4),
             Q(sqrt-3) disc -3  -> ramified only over 3   (hex/flavor, CP zeta6),
             Q(sqrt5)  disc  5  -> ramified only over 5   (REAL/golden, g_car, v313),
         product of ramified primes 2*3*5 = 30 = h(E8); two imaginary (CM /
         dynamic) {2,3} + one real (RM / static) {5} = the v403 reading at the
         prime level.

Mirrored in wolfram/tfpt_readouts_extension.wl (exact arithmetic only).
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

i = sp.I
H_E8 = 30


def N_gauss(a, b):
    """Norm in Z[i]: |a + b i|^2 = a^2 + b^2."""
    return a * a + b * b


def N_eisen(a, b):
    """Norm in Z[omega], omega = e^{2 pi i/3}: |a + b omega|^2 = a^2 - a b + b^2."""
    return a * a - a * b + b * b


def run():
    reset()
    print("v416 atom trichotomy: {2,3,5} ramified/inert/split in Z[i] vs "
          "Z[omega]; each atom one facet")

    # the atoms are the anchor elementary-symmetric data (v394)
    check("ATOMS = anchor data [E]: (|Z2|, N_fam, g_car) = (2,3,5), product "
          "2*3*5 = 30 = h(E8)",
          (2, N_fam, g_car) == (2, 3, 5) and 2 * 3 * 5 == H_E8)

    # ---- 1. Z[i] trichotomy ----
    check("Z[i] TRICHOTOMY [E] (square/seam, tau=i): 2 RAMIFIES "
          "(2 = -i(1+i)^2), 3 INERT (3 = 3 mod 4, norm 9 = N_fam^2), 5 SPLITS "
          "(5 = (2+i)(2-i), 5 = 1 mod 4) -- g_car=5 factors on the seam",
          sp.expand(-i * (1 + i)**2) == 2
          and 3 % 4 == 3 and N_gauss(3, 0) == 9 == N_fam**2
          and sp.expand((2 + i) * (2 - i)) == 5 and 5 % 4 == 1
          and N_gauss(2, 1) == g_car)

    # ---- 2. Z[omega] trichotomy ----
    check("Z[omega] TRICHOTOMY [E] (hex/flavor, tau=omega): 3 RAMIFIES "
          "(N(1-omega) = 3), 2 INERT (2 = 2 mod 3, norm 4), 5 INERT "
          "(5 = 2 mod 3, norm 25 = g_car^2)",
          N_eisen(1, -1) == 3 == N_fam
          and 2 % 3 == 2 and N_gauss(2, 0) == 4
          and 5 % 3 == 2 and N_eisen(5, 0) == 25 == g_car**2)

    # ---- 3. ramified prime = the 'own' atom ----
    check("RAMIFIED PRIME = OWN ATOM [E]: Z[i] ramifies at 2 = |Z2| "
          "(sheet/seam), Z[omega] ramifies at 3 = N_fam (family/flavor) -- "
          "each ring's discriminant prime is its atom",
          sp.factorint(4) == {2: 2} and sp.factorint(3) == {3: 1}
          and 2 == 2 and 3 == N_fam)

    # ---- 4. the three facets ramify over one atom each (v403) ----
    facets = {
        "Q(i)":      (-4, 2),
        "Q(sqrt-3)": (-3, 3),
        "Q(sqrt5)":  (5, 5),
    }
    ram_ok = all(set(sp.factorint(abs(disc)).keys()) == {atom}
                 for disc, atom in facets.values())
    check("THE THREE FACETS (v403) [E]: Q(i) disc -4 -> ram 2 (square/seam), "
          "Q(sqrt-3) disc -3 -> ram 3 (hex/flavor), Q(sqrt5) disc 5 -> ram 5 "
          "(real/golden, v313); each ramifies over exactly ONE atom; product "
          "2*3*5 = 30 = h(E8); 2 imaginary (CM/dynamic) + 1 real (RM/static)",
          ram_ok
          and (-4) % 4 == 0 and (-3) % 4 == 1 and 5 % 4 == 1   # disc residues
          and 2 * 3 * 5 == H_E8)

    # ---- 5. negative control: the ring assignment is rigid ----
    check("NEG CONTROL [E]: the rings are not interchangeable -- N_i(2,1)=5 "
          "but N_omega(2,1)=3; 5 splits in Z[i] yet is inert in Z[omega]; the "
          "square<->seam / hex<->flavor split (v222) is rigid",
          N_gauss(2, 1) == 5 and N_eisen(2, 1) == 3
          and 5 % 4 == 1 and 5 % 3 == 2)

    return summary("v416 atom trichotomy ({2,3,5} ram/inert/split; "
                   "each atom one facet of Q(i,sqrt-3,sqrt5))")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
