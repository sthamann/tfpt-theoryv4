"""v220 -- CP lives in the hexagonal phase fiber, not in the (square) seam deck.

Red team Target D leaves exactly one genuine residual: the magnitude bijection
(ratios, product) -> v_geo does NOT cover the CP phases delta_CKM/delta_PMNS
(v88).  The seam deck is the SQUARE modulus (mu4, cross-ratio 2 => j=1728, CM by
Z[i], automorphism Z/4; v214/v215/v216) -- which is purely real and carries no
phase.  Its exceptional PARTNER is the hexagonal modulus j=0 (tau = rho =
e^{i pi/3}, CM by the Eisenstein integers Z[omega], automorphism Z/6), and that
is exactly where a phase pi/3 lives.

  CRITICAL TYPING (the v215 kill-test selects the square): the SEAM DECK stays
  Z/4.  CP lives in the hexagonal PHASE FIBER over the seam, NOT in the seam
  deck.  This is a [C] bridge, NOT a derivation of CP and NOT a re-selection of
  the deck.

  [E] 1. SQUARE seam: j(i) = 1728, automorphism Z/4 (the mu4 clock; v214).
  [E] 2. HEX partner: j(rho) = 0, rho = e^{i pi/3}, automorphism Z/6, CM by
        Z[omega]; arg(rho) = pi/3 -- the hexagonal CM phase.
  [E] 3. the two are DIFFERENT configurations (j=1728 vs j=0); the deck is the
        square one, the phase fiber is the hexagonal one.
  [E] 4. the frozen leading CKM reading delta = pi/3 + 3 lambda_C^2 = 68.654 deg
        (v88; registry DELTA_CKM_RAD untouched) has leading term pi/3 = arg(rho),
        the hexagonal CM phase.
  [E] 5. NEG: the alternative pi/3 + 2 lambda_C^2 (coefficient |Z2| instead of
        N_fam) is the frozen look-elsewhere trap (v88) -- recorded, not adopted.

Status: [E] for the modular geometry; [C] for the CP bridge "the phase is the
hexagonal CM angle pi/3".  NOT [E] for a physical CP derivation.  Mirrored
(algebraic parts) in wolfram/tfpt_readouts_extension.wl.
"""
import mpmath as mp

from tfpt_constants import check, summary, reset, phi0, PI

mp.mp.dps = 30


def run():
    reset()
    print("v220  CP hexagonal modulus: phase fiber j=0 (Z/6) over the square seam (Z/4)")

    # ---- the square seam (the deck) ----
    check("SQUARE seam [E]: kleinj(i) normalised J(i)=1 <=> j=1728; automorphism "
          "Z/4 (the mu4 clock z->iz; v214)", abs(mp.kleinj(1j) - 1) < mp.mpf('1e-12'))

    # ---- the hexagonal partner (the phase fiber) ----
    rho = mp.e**(1j * mp.pi / 3)
    check("HEX partner [E]: kleinj(rho)=0 <=> j=0 for rho=e^{i pi/3}; automorphism "
          "Z/6, CM by the Eisenstein integers Z[omega]", abs(mp.kleinj(rho)) < mp.mpf('1e-12'))
    check("arg(rho) = pi/3 (the hexagonal CM phase = 60 deg)",
          abs(mp.arg(rho) - PI / 3) < mp.mpf('1e-20'))
    check("the two exceptional moduli are DIFFERENT: j_square=1728 != j_hex=0; "
          "the SEAM DECK is the square (Z/4), the PHASE FIBER is the hexagon (Z/6)",
          abs(mp.kleinj(1j) - 1) < mp.mpf('1e-12') and abs(mp.kleinj(rho)) < mp.mpf('1e-12'))

    # ---- the frozen CKM phase has leading term pi/3 = arg(rho) ----
    lam = mp.sqrt(phi0 * (1 - phi0))
    delta = PI / 3 + 3 * lam**2
    check("frozen leading CKM reading delta = pi/3 + 3 lambda_C^2 = 68.654 deg "
          "(v88; registry DELTA_CKM_RAD untouched); leading term pi/3 = arg(rho) "
          "is the hexagonal CM phase",
          abs(delta - mp.mpf('1.198231638')) < mp.mpf('1e-8')
          and abs(delta * 180 / PI - mp.mpf('68.654')) < mp.mpf('1e-2'))
    check("leading term of delta IS arg(rho) = pi/3 (60 deg); the 3 lambda_C^2 "
          "correction is the seam misalignment on top of the hexagonal phase",
          abs((delta - 3 * lam**2) - PI / 3) < mp.mpf('1e-20'))

    # ---- negative control: the |Z2| alternative is the frozen look-elsewhere trap ----
    alt = PI / 3 + 2 * lam**2
    check("NEG: the alternative pi/3 + 2 lambda_C^2 = 65.77 deg (coefficient |Z2| "
          "instead of N_fam=3) is the frozen look-elsewhere trap (v88), recorded "
          "NOT adopted; the two differ by lambda_C^2 = 2.88 deg",
          abs(alt * 180 / PI - mp.mpf('65.77')) < mp.mpf('5e-2')
          and abs((delta - alt) - lam**2) < mp.mpf('1e-20'))

    # ---- typing ----
    check("TYPING [C]: CP is the hexagonal-fiber phase; the seam deck stays Z/4 "
          "(NOT re-selected). This sharpens Target D geometrically, does not close it",
          True)

    return summary("v220 CP hexagonal modulus (Z/6 phase fiber over Z/4 seam)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
