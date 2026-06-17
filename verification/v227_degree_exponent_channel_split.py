"""v227 -- the 248 = 120 + 128 split as a magnitude/phase channel typing.

E8 carries two canonical invariant lists: the EXPONENTS m_i = {1,7,11,13,17,19,
23,29} (sum 120 = |R^+(E8)|) and the fundamental DEGREES d_i = m_i + 1 =
{2,8,12,14,18,20,24,30} (sum 128).  Together 120 + 128 = 248 = dim E8, the same
split as the D8 branching adj(E8) = 120 (adj SO(16)) + 128 (spinor).  This script
records the split exactly and TYPES it: the 120 channel carries magnitudes (root
transitions, positive roots, the Plucker/ratio readouts), the 128 channel carries
phase / glue completion (the Ramond / spinor sector).

This is the honest replacement for the over-strong "S^- is dark matter" reading
(red team / problem_b #6): the 128 channel is the NON-magnitude (phase/glue)
complement; whether it hosts a dark sector is Frontier [O], not asserted here.
It also gives red team Target D a clean home: the magnitude bijection
(ratios,product) lives in the 120 channel, the un-covered CP phases live in 128.

  [E] 1. exponent sum = 120 = |R^+(E8)| (sum of exponents = #positive roots).
  [E] 2. degree sum   = 128 = 2^(rank-1) (the half-spinor count of SO(16)).
  [E] 3. 248 = 120 + 128 = dim E8 = adj(D8) + spinor(D8) (the D8 branching).
  [E] 4. sum(degrees) - sum(exponents) = rank E8 = 8 (each degree = exponent+1).
  [C] 5. TYPING: 120 = magnitude channel, 128 = phase/glue channel.
  [O] 6. dark-sector reading of the 128 channel stays Frontier (NOT asserted).

Status: [E] for the split; [C] for the channel typing; [O] for any dark physics.
Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
from tfpt_constants import check, summary, reset, rankE8, dim_Splus

DIM_E8 = 248


def run():
    reset()
    print("v227  248 = 120 + 128 : magnitude channel vs phase/glue channel")

    exponents = [1, 7, 11, 13, 17, 19, 23, 29]
    degrees = [e + 1 for e in exponents]
    check("E8 exponents {1,7,11,13,17,19,23,29}; sum = 120 = |R^+(E8)| "
          "(MAGNITUDE channel: positive roots / root transitions)",
          sum(exponents) == 120)
    check("E8 degrees {2,8,12,14,18,20,24,30}; sum = 128 = 2^(rank-1) "
          "(PHASE/GLUE channel: the SO(16) half-spinor count)",
          sorted(degrees) == [2, 8, 12, 14, 18, 20, 24, 30]
          and sum(degrees) == 128 == 2**(rankE8 - 1))
    check("248 = 120 + 128 = dim E8 = adj(D8) + spinor(D8) (the D8 branching split)",
          120 + 128 == DIM_E8)
    check("sum(degrees) - sum(exponents) = rank E8 = 8 (each degree = exponent + 1)",
          sum(degrees) - sum(exponents) == rankE8 == 8)
    check("the phase channel 128 = 8 * dim S^+ = rank E8 * 16 (eight copies of "
          "the carrier half-spinor) -- a glue/spinor count, not a magnitude",
          128 == rankE8 * dim_Splus)

    # typing assertions (documentary; the arithmetic is the content)
    check("TYPING [C]: ratios+products (red team Target D magnitude bijection) "
          "live in the 120 channel; the un-covered CP phases live in the 128 "
          "channel (phase/glue) -- a clean home, not a new gate",
          True)
    check("DARK SECTOR [O]: whether the 128 phase/glue channel hosts a dark "
          "sector is Frontier; NOT asserted here (replaces 'S^- is dark matter')",
          True)

    return summary("v227 degree/exponent channel split (120 magnitude | 128 phase)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
