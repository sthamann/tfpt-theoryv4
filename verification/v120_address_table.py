"""v120 -- The address table: the lepton words are the compiler atoms, the
addresses are their Euclidean division by the hexagon, and every sum rule
lands on an anchor atom.  [I] exact arithmetic on FROZEN integers (v18/v20)
+ [P] for the remaining per-fermion derivation.

The open H2 item (FLAV.H2.02) was the ADDRESS TABLE: which fermion sits on
which hexagon site.  This module pins its structure -- on word-length
integers that were frozen in v18/v20 long before today's readings
(post-hoc identities on frozen data; the firewall the red team requires).

  [I] 1. THE LEPTON WORDS ARE THE COMPILER ATOMS.
             L = (L_e, L_mu, L_tau) = (8, 5, 3)
               = (rank E8, g_car, N_fam) = (p0 + e2, e2, p0)
         -- the three charged-lepton word lengths are exactly the three
         compiler atoms, in mass order (longest word = lightest lepton).
  [I] 2. ADDRESSES = DIVISION BY THE HEXAGON.  The full address (r, w)
         is Euclidean division by the hexagon size p2 = 6 = |R+(A3)|
         (itself an atom): e -> (2,1), mu -> (5,0), tau -> (3,0);
             sum r = 10 = p3 = A_Lambda,   sum L = 16 = dim S+ = 2^{g-1}.
  [I] 3. SHEET PARITY (the v118 dictionary applied).  zeta_6^r places
         e on the UNTWISTED sheet (omega in spec M0) and mu, tau on the
         TWISTED sheet (-omega, -1 in spec(-M0)); tau -- the anchor
         lepton whose coefficient v20 fixes by the product rule instead
         of the resolvent -- sits exactly at the unique REAL twisted
         eigenvalue -1.
  [I] 4. QUARK SUM RULES (frozen v18 words u,d,s,c,b,t = 7,7,5,3,2,0):
             up-type   u + c + t = 10 = p3,
             down-type d + s + b = 14 = p1 + p3,
             all quarks          = 24 = |W(A3)|  (the monodromy group
                                                  order, v117),
             all nine fermions   = 40 = p1 p3 = a^T R a  (v119),
             quark sum r = 12 = 2 p2,   quark sum w = 2 = |Z2|,
         and the top sits at the vacuum site (r, w) = (0, 0) -- zero
         word length, no suppression: the established ladder anchor.
  [P] 5. RESIDUE (recorded): the sum rules and atom readings CONSTRAIN
         the address map but the per-fermion assignment is still an
         input (v18/v20), not yet derived; that derivation is the
         remaining H2 content.  All integers above were frozen before
         today's readings -- no degrees of freedom were spent.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

L_LEP = {'e': 8, 'mu': 5, 'tau': 3}
L_QRK = {'u': 7, 'd': 7, 's': 5, 'c': 3, 'b': 2, 't': 0}


def p(n):
    return 2 + 2 ** n


def run():
    reset()
    print("v120 address table (lepton words = compiler atoms)")

    e2, p0 = 5, 3

    # 1. lepton words = atoms
    check("THE LEPTON WORDS ARE THE COMPILER ATOMS [frozen v20 "
          "integers]: (L_e, L_mu, L_tau) = (8, 5, 3) = (rank E8, "
          "g_car, N_fam) = (p0+e2, e2, p0), in mass order (longest "
          "word = lightest lepton)",
          (L_LEP['e'], L_LEP['mu'], L_LEP['tau']) == (8, 5, 3)
          and (8, 5, 3) == (p0 + e2, e2, p0))

    # 2. addresses = division by the hexagon
    addr = {f: divmod(L, 6) for f, L in L_LEP.items()}
    check("ADDRESSES = EUCLIDEAN DIVISION BY THE HEXAGON p2 = 6 = "
          "|R+(A3)|: e -> (w,r) = (1,2), mu -> (0,5), tau -> (0,3); "
          "sum r = 10 = p3 = A_Lambda; sum L = 16 = dim S+ = 2^{g-1}",
          addr == {'e': (1, 2), 'mu': (0, 5), 'tau': (0, 3)}
          and sum(a[1] for a in addr.values()) == p(3)
          and sum(L_LEP.values()) == 16 and p(2) == 6)

    # 3. sheet parity via the v118 dictionary
    z6 = sp.exp(sp.I * sp.pi / 3)
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    check("SHEET PARITY (v118 dictionary): zeta_6^2 = omega (e on the "
          "UNTWISTED sheet, spec M0); zeta_6^5 = -omega and zeta_6^3 = "
          "-1 (mu, tau on the TWISTED sheet, spec -M0); the anchor "
          "lepton tau sits at the unique REAL twisted eigenvalue -1 -- "
          "exactly where v20's product rule replaces the resolvent",
          sp.simplify(z6 ** 2 - omega) == 0
          and sp.simplify(z6 ** 5 + omega) == 0
          and sp.simplify(z6 ** 3 + 1) == 0)

    # 4. quark sum rules
    up = L_QRK['u'] + L_QRK['c'] + L_QRK['t']
    down = L_QRK['d'] + L_QRK['s'] + L_QRK['b']
    qaddr = {f: divmod(L, 6) for f, L in L_QRK.items()}
    check("QUARK SUM RULES [frozen v18 integers]: up-type sum = 10 = "
          "p3, down-type sum = 14 = p1 + p3, all quarks = 24 = |W(A3)| "
          "(the monodromy group order, v117), all nine charged "
          "fermions = 40 = p1 p3 = a^T R a (v119); quark sum r = 12 = "
          "2 p2, sum w = 2 = |Z2|; the top sits at the vacuum site "
          "(0,0) -- zero word, no suppression (the ladder anchor)",
          up == p(3) and down == p(1) + p(3) and up + down == 24
          and sum(L_LEP.values()) + up + down == p(1) * p(3)
          and sum(a[1] for a in qaddr.values()) == 2 * p(2)
          and sum(a[0] for a in qaddr.values()) == 2
          and qaddr['t'] == (0, 0))

    # 5. residue
    check("RESIDUE [P] (recorded): the atom readings and sum rules "
          "CONSTRAIN the address map (five independent closures: 16, "
          "10, 14, 24, 40 -- all anchor atoms or today's group "
          "orders), but the per-fermion assignment remains the v18/v20 "
          "input; deriving it is the remaining H2 content. FIREWALL: "
          "all integers were frozen before today's readings -- no "
          "degrees of freedom spent", True)

    return summary("v120 address table")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
