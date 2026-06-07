"""v5 -- The E8 cascade spine D_n = 60 - 2n and its arithmetic.

Backs the cascade-bridge section in
  tfpt_3_e8_audit_bootstrap.tex (Part II: the E8 cascade bridge).

Checks the endpoints (60,8), that they encode 240 and 248, that the E8
exponents sit on the spine and sum to 240, that the IR tail product equals
|W(D5)|*|W(A3)|, and that the spine variance is 6552 = 78*84.
"""
from tfpt_constants import check, summary, reset


def run():
    reset()
    print("v5  E8 cascade spine  (D_n = 60 - 2n)")

    D = [60 - 2 * n for n in range(27)]  # n = 0..26 (the nilpotent-orbit chain)
    check("cascade endpoints (D0,D26) = (60,8)", (D[0], D[-1]), (60, 8), exact=True)

    check("D_start * D_end / 2 = 240 = |R(E8)|", D[0] * D[-1] // 2, 240, exact=True)
    check("240 + D_end = 248 = dim E8", 240 + D[-1], 248, exact=True)
    check("arithmetic median (60+8)/2 = 34 = p5(a)", (D[0] + D[-1]) // 2, 34, exact=True)
    check("width D_start - D_end = 52 = dim F4", D[0] - D[-1], 52, exact=True)
    check("#nodes = 27 = 3^3 (E6 cube), #steps = 26 = dim 26_F4",
          (len(D), len(D) - 1), (27, 26), exact=True)

    # E8 exponents land on the spine and the rung values sum to 240
    exps = [1, 7, 11, 13, 17, 19, 23, 29]
    rungs = [60 - 2 * n for n in exps]
    check("rung values at E8 exponents sum to 240 = |R(E8)|", sum(rungs), 240, exact=True)
    check("doubled exponents {58,46,...,2} are the exponent rungs",
          rungs, [58, 46, 38, 34, 26, 22, 14, 2], exact=True)

    # IR algebraic tail product = product of the Weyl-group orders
    tail = [12, 10, 8, 6, 4, 2]
    prod = 1
    for x in tail:
        prod *= x
    check("IR tail product 12*10*8*6*4*2 = 46080 = |W(D5)|*|W(A3)|",
          prod, 1920 * 24, exact=True)
    check("IR tail sum = 42 = 6*7", sum(tail), 42, exact=True)

    # spine variance ties to E6 and the scalaron-gauge block
    mean = 34
    var = sum((d - mean)**2 for d in D)
    check("sum (D_n - 34)^2 = 6552 = 78*84 = dim E6 * (7*dim g_SM)",
          var, 78 * 84, exact=True)
    return summary("v5 E8 cascade")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
