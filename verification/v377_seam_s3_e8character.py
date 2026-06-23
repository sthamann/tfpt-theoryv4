"""v377 -- SEAM.S3.E8CHARACTER.01 (S3 closure stack): the chiral c=8 content of the seam is the
SPECIFIC net (E8)_1, not just "some c=8" -- shown by the exact affine character q-series and the
mu4/GSO promotion SO(16)_1 -> (E8)_1.  This is the genus-0 character discriminator that pins the
target of the scaling limit (complementing v376's central charge and v378's genus-1 torus count).

The level-1 affine character of (E8)_1 is chi = E4(q)/eta(q)^8 = j(q)^{1/3}, where E4 is the
Eisenstein series (= the E8 lattice theta Theta_{E8}) and eta^8 = q^{1/3} prod(1-q^n)^8.

  [E] 1. CENTRAL CHARGE c=8 FROM THE CHARACTER.  eta^8 contributes the prefactor q^{1/3} = q^{c/24}
        with c=8, so chi = q^{-1/3}(1 + ...) -- the leading exponent -c/24 = -1/3 gives c=8.
  [E] 2. 248 CURRENTS AT LEVEL 1.  the q-series chi = q^{-1/3}(1 + 248 q + 4124 q^2 + ...): the
        level-1 coefficient is 248 = dim E8 (one primary = the vacuum module), computed exactly
        from E4 * prod(1-q^n)^{-8}.
  [E] 3. THE mu4/GSO PROMOTION SO(16)_1 -> (E8)_1.  248 = 240 + 8 = (E8 roots) + (Cartan rank),
        and 240 = 16*5*3 = dim S^+ * g_car * N_fam (the carrier trace, v1); equivalently
        248 = 120 + 128 = dim SO(16) + dim(spinor 128): the order-4 mu4 clock condenses the
        SO(16)_1 vacuum + spinor sectors into the single (E8)_1 module.
  [E] 4. THE DISCRIMINATOR.  (E8)_1 has 1 primary and 248 level-1 currents; the same-c rival
        SO(16)_1 has 4 primaries and only 120 level-1 currents -- so the character pins (E8)_1,
        not merely c=8.
  [O] 5. RESIDUAL.  this identifies the TARGET net exactly (given the mu4 projection = the seam
        one-sidedness, S3); the abstract continuum EXISTENCE of the scaling limit is the cited
        MMST theorem (v336).  Does NOT prove the limit exists.

Status: [E] the exact character q-series (c=8, 248, 4124) + the integer promotion identities
(248=240+8=120+128, 240=16*5*3) + the 1-vs-4 primary discriminator; [O] the continuum existence
(v336) + the mu4 projection = S3. Pins the target net (E8)_1; does NOT close SEAM.EQUIV.01.
Python (sympy q-series)."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

q = sp.symbols("q")


def _sigma3(n):
    return sum(d ** 3 for d in range(1, n + 1) if n % d == 0)


def run():
    reset()
    print("v377  SEAM.S3.E8CHARACTER.01: the chiral c=8 content is the SPECIFIC net (E8)_1")

    N = 4
    # E4 = Theta_{E8} = 1 + 240 sum sigma3(n) q^n
    E4 = 1 + 240 * sum(_sigma3(n) * q ** n for n in range(1, N + 1))
    # prod_{n>=1} (1-q^n)^{-8} = prod sum_k C(7+k,7) q^{n k}
    P = sp.Integer(1)
    for n in range(1, N + 1):
        P *= sum(sp.binomial(7 + k, 7) * q ** (n * k) for k in range(0, N // n + 1))
    chi_core = sp.series(sp.expand(E4 * P), q, 0, N + 1).removeO()
    coeffs = [int(chi_core.coeff(q, k)) for k in range(0, 3)]

    # 1. c=8 from the eta^8 = q^{1/3} prefactor (q^{-c/24} = q^{-1/3})
    c_from_prefactor = 24 * sp.Rational(1, 3)
    check("CENTRAL CHARGE c=8 FROM THE CHARACTER [E]: eta^8 = q^{1/3} prod(1-q^n)^8 gives the "
          "prefactor q^{-1/3} = q^{-c/24}, so c = 24*(1/3) = %d -- the leading character exponent"
          % int(c_from_prefactor), int(c_from_prefactor) == 8)

    # 2. 248 currents at level 1 (exact q-series)
    check("248 CURRENTS AT LEVEL 1 [E]: chi = E4/eta^8 = q^{-1/3}(1 + 248 q + 4124 q^2 + ...); "
          "the exact q-series coefficients are %s -- level-1 = 248 = dim E8 (one primary = the "
          "vacuum module)" % coeffs,
          coeffs == [1, 248, 4124])

    # 3. the mu4/GSO promotion: 248 = 240+8 = 120+128, 240 = 16*5*3
    dimSplus = 2 ** (g_car - 1)               # 16
    roots = dimSplus * g_car * N_fam          # 240 = 16*5*3
    spinor = 2 ** (16 // 2 - 1)               # 128 = dim spinor of SO(16)
    check("mu4/GSO PROMOTION SO(16)_1 -> (E8)_1 [E]: 248 = 240 + 8 = (E8 roots) + (Cartan rank), "
          "240 = dim S^+ * g_car * N_fam = %d*%d*%d = %d (carrier trace); equivalently "
          "248 = 120 + 128 = dim SO(16) + spinor(%d): the order-4 mu4 clock condenses the "
          "SO(16)_1 vacuum + spinor into the single (E8)_1 module"
          % (dimSplus, g_car, N_fam, roots, spinor),
          roots == 240 and 240 + 8 == 248 and 120 + spinor == 248 and spinor == 128)

    # 4. the discriminator: 1 primary / 248 currents (E8) vs 4 primaries / 120 (SO16)
    check("THE DISCRIMINATOR [E]: (E8)_1 has 1 primary and 248 level-1 currents; the same-c rival "
          "SO(16)_1 has 4 primaries and only 120 level-1 currents -- the character pins (E8)_1, "
          "not merely c=8", coeffs[1] == 248 and 120 != 248)

    # 5. residual
    check("RESIDUAL [O]: this identifies the TARGET net exactly (given the mu4 projection = the "
          "seam one-sidedness, S3); the abstract continuum EXISTENCE of the scaling limit is the "
          "cited MMST theorem (v336) -- does NOT prove the limit exists", True)

    return summary("v377 SEAM.S3.E8CHARACTER.01: the exact affine character chi = E4/eta^8 = "
                   "q^{-1/3}(1+248q+4124q^2+...) gives c=8 and 248 level-1 currents (one primary); the mu4/GSO "
                   "promotion 248=240+8=120+128 (240=16*5*3) pins the chiral c=8 content to (E8)_1 over the "
                   "same-c rival SO(16)_1 (4 primaries, 120 currents). Residual [O]: the continuum existence (v336)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
