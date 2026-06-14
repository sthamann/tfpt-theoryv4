"""EXPLORATION (experiments/ only -- NOT a suite module, NOT in the ledger/papers).

Question: does the carrier rank g_car shift the induced Einstein-Hilbert
coefficient in the replica/heat-kernel reconstruction (a Sakharov-style field
multiplicity)?

Mechanism (v150, model level): the replica variation of a gapped 2d determinant
is of EH form,  Delta log det' = (ln m / 12 pi) Int sqrt(g) R, so the induced
coefficient is k = (ln m)/(12 pi), and the seam value k = c3/2 = 1/(16 pi) is
reached iff  ln m = 12 pi (c3/2) = 3/4 = q(A3)  (the A3 / FAMILY glue norm).

HONEST VERDICT (see prints): NO -- g_car does NOT shift the EH coefficient.
The coefficient selects the FAMILY norm q(A3)=3/4, and the CARRIER norm
q(D5)=5/4 (the g_car side) would give the WRONG Newton constant -- 5/3 too
strong (ratio q(D5)/q(A3) = g_car/N_fam). So TFPT gravity is "family-geometry
(A3) induced", not "carrier (D5/g_car) induced". This DISCONFIRMS the
carrier-gravity hypothesis -- which is the useful result. A Sakharov multiplicity
N>1 would need ln m = (3/4)/N, with no clean TFPT value emerging, so the repo's
single-effective-mode model (ln m = q(A3)) is what reproduces the seam value.
"""
import mpmath as mp

mp.mp.dps = 30
PI = mp.pi
C3 = 1 / (8 * PI)
GCAR, NFAM, MU4, DIMSP, CE8 = 5, 3, 4, 16, 8
Q_D5 = mp.mpf(GCAR) / MU4          # 5/4  carrier (D5) glue norm
Q_A3 = mp.mpf(NFAM) / MU4          # 3/4  family  (A3) glue norm
K_TARGET = C3 / 2                  # the seam EH coefficient 1/(16 pi)


def k_of(lnm, N=1):
    """induced EH coefficient k = N*(ln m)/(12 pi)."""
    return N * lnm / (12 * PI)


def sec(t):
    print("\n" + "=" * 72 + "\n" + t + "\n" + "=" * 72)


def main():
    sec("MECHANISM: k = (ln m)/(12 pi); seam target k = c3/2 = 1/(16 pi)")
    print(f"k_target = c3/2 = {float(K_TARGET):.8f} = 1/(16 pi)")
    print("v150 (model level): replica variation of a gapped 2d det IS the EH form,")
    print("k reached iff ln m = 12 pi (c3/2) = 3/4 = q(A3).")

    sec("THE TEST: which glue norm reproduces the seam EH coefficient?")
    for name, lnm in [("q(A3)=3/4  FAMILY (A3)", Q_A3),
                      ("q(D5)=5/4  CARRIER (D5/g_car)", Q_D5),
                      ("q(D5)+q(A3)=2  E8 root norm", Q_D5 + Q_A3)]:
        k = k_of(lnm)
        print(f"  ln m = {name:32s}: k = {float(k):.6f} = 1/({float(1/(k*PI)):.2f} pi)"
              f"  match c3/2? {mp.almosteq(k, K_TARGET)}")
    print()
    print(f"=> ONLY q(A3) (FAMILY) gives k = c3/2. The CARRIER norm q(D5) (the g_car")
    print(f"   side) gives 1/(9.6 pi) -- the WRONG G. Ratio q(D5)/q(A3) = {float(Q_D5/Q_A3):.4f}")
    print(f"   = g_car/N_fam = 5/3: carrier-induced gravity would be 5/3 too strong.")
    print("   PHYSICAL READING: gravity = the geometry channel, and A3 is the FAMILY")
    print("   GEOMETRY (mu4-punctured P^1 homology); D5 is the gauge CARRIER. Gravity")
    print("   couples to the geometry (A3), not the carrier (D5). g_car is the wrong knob.")

    sec("SAKHAROV MULTIPLICITY: k = N*(ln m)/(12 pi) -- what ln m for field count N?")
    for N, lbl in [(1, "single effective mode (v150)"), (GCAR, "g_car=5"),
                   (CE8, "c=8 (E8 central charge)"), (DIMSP, "dim S+ =16")]:
        lnm_req = 12 * PI * K_TARGET / N
        print(f"  N={N:2d} ({lbl:28s}): ln m = (3/4)/N = {float(lnm_req):.5f}")
    print()
    print("  No clean TFPT value emerges for N>1, so the repo's single-mode model")
    print("  (N=1, ln m = q(A3) = 3/4) is what reproduces the seam value. The full")
    print("  multiplicity (whether the seam gravity is induced by 1 or by c=8 modes)")
    print("  stays OPEN -- but it does NOT introduce a g_car factor.")

    sec("VERDICT (firewall)")
    print("The carrier-gravity hypothesis is DISCONFIRMED, cleanly:")
    print("  * the induced EH coefficient selects q(A3)=3/4 (FAMILY/A3 geometry);")
    print("  * the carrier norm q(D5)=5/4 (g_car side) would give G that is 5/3 too strong;")
    print("  * so g_car does NOT shift the EH coefficient -- gravity is family-geometry-induced.")
    print("This SHARPENS v150's 'ln m = q(A3)' into a falsifiable contrast (A3 not D5).")
    print("Still within the open SEAM.THEOREM.01 (model level, [P]/[A]) -- stays in experiments/.")


if __name__ == "__main__":
    main()
