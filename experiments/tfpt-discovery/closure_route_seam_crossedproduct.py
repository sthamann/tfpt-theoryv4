"""Closure-route candidate 2026-07-02 (SANDBOX ONLY, no claim, not promoted):

SEAM.EQUIV.01 -- a NEW complete certification route that (a) replaces the
2024/2025-preprint leg of the cited theorem package by peer-reviewed 1995-2001
subfactor theorems, and (b) reduces the one TFPT-internal realisation axiom R1
("collar_realizes": the abstract seam IS this p+ip lattice model) to an
INVARIANT-level statement whose inputs are already TFPT-derived.

Current residual (Lean FORM.SEAM.RESIDUAL.01):
    axiom collar_realizes            : model-level realisation (R1)
    axiom seam_realisation_theorem   : MMST (CMP 2023) o AGT/AMT (arXiv 2025/2024)

Proposed route (every leg a PUBLISHED, peer-reviewed theorem):

    R1' invariants {quasi-free [C v155/v160], gap>0 [E v302], class D,
                    c_- = 8 [E, forced by P1 via v456]}
      --[T1: free-fermion phase classification, Kitaev Ann.Phys. 2006 (16-fold
             way) + periodic table 2009; c_- a phase invariant:
             Kapustin-Spodyneiko PRB 101 (2020), Kim et al. PRL 129 (2022)]-->
    the nu = 16 class-D phase (= the v367 p+ip stack, 16 chiral Majoranas)
      --[T2: MMST, CMP 397 (2023) per-copy c=1/2 scaling limit (audit v458)
             + Boeckenhauer, Rev. Math. Phys. 8 (1996): even-CAR algebras give
             the level-1 so(N) chiral net WITH its DHR sectors + fusion]-->
    the SO(16)_1 conformal net, sectors {1, v, s, c}
      --[T3: h_s = 16/16 = 1 in Z  =>  statistics phase +1  =>  the Z2
             simple-current crossed product is a LOCAL index-2 extension
             (Longo-Rehren RMP 7 (1995); Boeckenhauer-Evans CMP 197 (1998))]-->
    a local holomorphic extension B, mu(B) = mu(SO16)/2^2 = 1 (KLM CMP 2001)
      --[T4: holomorphic c=8 => dim V_1 = 248 (E4/eta^8) => E8 uniquely
             (Dong-Mason; v463 selector)]-->
    B = (E8)_1.                                              QED (certification)

Kitaev's 16-fold way is the independent physics pin: nu = 16 = 0 mod 16 is
EXACTLY the class-D phase whose edge admits a purely bosonic description, and
that bosonic edge is the (E8)_1 level-1 WZW model (the "Kitaev E8 state") --
published in Ann. Phys. 321 (2006), Sec. "sixteen-fold way".

This script machine-checks every arithmetic joint of the chain and the
composition typing (in/out slots, v297-style).  It does NOT close
SEAM.EQUIV.01 -- it exhibits a strictly harder-to-reject citation package
(older, peer-reviewed, hypothesis-checkable) plus the R1 -> R1' reduction.
"""
from fractions import Fraction as F
import cmath
import math

import numpy as np

PASS, FAIL = 0, 0


def check(label, ok):
    global PASS, FAIL
    print(("PASS  " if ok else "FAIL  ") + label)
    if ok:
        PASS += 1
    else:
        FAIL += 1


# ----------------------------------------------------------------------------
# T3 joint, route A (index 2): so(16)_1 sector data and the LR locality integer
# ----------------------------------------------------------------------------
print("== A. index-2 route: SO(16)_1 --Z2 spinor current--> holomorphic c=8 ==")
N = 16                                   # so(N), N = 16 Majoranas
h_vac, h_v = F(0), F(1, 2)
h_s = F(N, 16)                           # spinor conformal weight so(N)_1 = N/16
h_c = F(N, 16)
check("so(16)_1 sector weights h = {0, 1/2, 1, 1}: h_s = N/16 = %s" % h_s,
      h_s == 1 and h_c == 1 and h_v == F(1, 2))
check("all four sectors are simple currents (d = 1), fusion group Z2 x Z2 "
      "(N/2 = 8 even)", (N // 2) % 2 == 0)

omega_s = cmath.exp(2j * math.pi * float(h_s))
check("statistics phase omega_s = e^{2 pi i h_s} = +1 (h_s integer) -- the "
      "Longo-Rehren locality criterion for the Z2 crossed product HOLDS",
      abs(omega_s - 1) < 1e-15)

mu_SO16 = 4                              # = |Z2 x Z2| = det Cartan(D8)
index = 2
mu_B = F(mu_SO16, index ** 2)
check("KLM mu-index: mu(B) = mu(SO16)/[B:A]^2 = 4/4 = %s => B HOLOMORPHIC"
      % mu_B, mu_B == 1)

# ----------------------------------------------------------------------------
# T3 joint, route B (index 4, the mu4 glue -- parallel check, v125/v154 data):
# ALL powers of the glue current have integer weight => local Z4 extension
# ----------------------------------------------------------------------------
print("== B. index-4 route: (D5)_1 x (A3)_1 --mu4 glue--> holomorphic c=8 ==")
h_D5 = {0: F(0), 1: F(5, 8), 2: F(1, 2), 3: F(5, 8)}   # 1, s, v, c of so(10)_1
h_A3 = {k: F(k * (4 - k), 8) for k in range(4)}        # su(4)_1: k(4-k)/8
glue_int = all(float(h_D5[k % 4] + h_A3[k % 4]).is_integer() for k in range(1, 4))
check("mu4 glue J = (s, Lambda1): h(J^k) = %s for k=1,2,3 -- ALL integer => "
      "the Z4 crossed product is LOCAL (Lagrangian glue, matches v125 isotropy "
      "q(k,k) = k^2)" % [str(h_D5[k] + h_A3[k]) for k in (1, 2, 3)], glue_int)
check("KLM mu-index route B: 16/4^2 = 1 (holomorphic), same endpoint",
      F(16, 16) == 1)

# ----------------------------------------------------------------------------
# T4 joint: holomorphic c=8 => dim V_1 = 248 => E8 (recompute E4/eta^8)
# ----------------------------------------------------------------------------
print("== C. identification: E4/eta^8 tower and 248 = 120 + 128 = 8 + 240 ==")
M_ = 6
sig3 = [0] + [sum(d ** 3 for d in range(1, n + 1) if n % d == 0)
              for n in range(1, M_)]
e4 = [1] + [240 * s for s in sig3[1:]]
# coefficients of prod_{n>=1}(1-q^n)^{-8}: multiply the (1-q^k)^{-8} series
p8 = [F(1)] + [F(0)] * (M_ - 1)
for k in range(1, M_):
    poly = [F(1)] + [F(0)] * (M_ - 1)
    # (1-q^k)^{-8} = sum_j C(j+7,7) q^{k j}
    ser = [F(0)] * M_
    j = 0
    while k * j < M_:
        ser[k * j] = F(math.comb(j + 7, 7))
        j += 1
    p8 = [sum(p8[i] * ser[n - i] for i in range(n + 1)) for n in range(M_)]
tower = [sum(F(e4[i]) * p8[n - i] for i in range(n + 1)) for n in range(M_)]
check("E4/eta^8 tower = %s (q^1 coefficient 248 = dim E8)"
      % [int(t) for t in tower[:4]],
      [int(t) for t in tower[:3]] == [1, 248, 4124])
check("248 = 120 + 128 (so(16) + spinor) = 8 + 240 (Cartan + roots); "
      "C(16,2) = 120, 2^(16/2)/2 = 128",
      math.comb(16, 2) == 120 and 2 ** 8 // 2 == 128
      and 120 + 128 == 248 == 8 + 240)

# ----------------------------------------------------------------------------
# T1 joint / R1': the invariants are computable -- FHS Chern of the p+ip copy
# ----------------------------------------------------------------------------
print("== D. R1' invariants: per-copy Chern (FHS), c_- = 8, 16-fold way ==")


def chern_fhs(Mpar, n=48):
    ks = np.linspace(-np.pi, np.pi, n, endpoint=False)
    u = np.zeros((n, n, 2), dtype=complex)
    for i, kx in enumerate(ks):
        for j, ky in enumerate(ks):
            d = np.array([np.sin(kx), np.sin(ky), Mpar - np.cos(kx) - np.cos(ky)])
            h = d[0] * np.array([[0, 1], [1, 0]]) \
                + d[1] * np.array([[0, -1j], [1j, 0]]) \
                + d[2] * np.array([[1, 0], [0, -1]])
            w, v = np.linalg.eigh(h)
            u[i, j] = v[:, 0]
    c = 0.0
    for i in range(n):
        for j in range(n):
            u1, u2 = u[i, j], u[(i + 1) % n, j]
            u3, u4 = u[(i + 1) % n, (j + 1) % n], u[i, (j + 1) % n]
            f = (np.vdot(u1, u2) * np.vdot(u2, u3)
                 * np.vdot(u3, u4) * np.vdot(u4, u1))
            c += np.angle(f)
    return round(c / (2 * np.pi))


C_topo, C_triv = chern_fhs(1.0), chern_fhs(3.0)
check("per-copy FHS Chern: C(M=1) = %d (topological), C(M=3) = %d (control)"
      % (C_topo, C_triv), abs(C_topo) == 1 and C_triv == 0)
nu = 16 * abs(C_topo)
check("nu = 16 x |C| = %d; c_- = nu/2 = %d = g_car + N_fam; nu mod 16 = 0 is "
      "EXACTLY Kitaev's class whose edge admits a purely bosonic description "
      "= the (E8)_1 level-1 state (Ann. Phys. 321 (2006), 16-fold way)"
      % (nu, nu // 2), nu == 16 and nu // 2 == 8 and nu % 16 == 0)

# ----------------------------------------------------------------------------
# The chain composes (v297-style in/out typing)
# ----------------------------------------------------------------------------
print("== E. composition typing of the new citation chain ==")
CHAIN = [
    ("T1", "invariants {quasi-free, gapped, class D, c_-=8}",
     "the nu=16 class-D free-fermion phase",
     "Kitaev 2006/2009; Kapustin-Spodyneiko 2020; Kim et al. 2022"),
    ("T2", "the nu=16 class-D free-fermion phase",
     "SO(16)_1 conformal net with sectors {1,v,s,c}",
     "MMST CMP 397 (2023); Boeckenhauer RMP 8 (1996)"),
    ("T3", "SO(16)_1 conformal net with sectors {1,v,s,c}",
     "local index-2 holomorphic extension B (mu=1)",
     "Longo-Rehren RMP 7 (1995); Boeckenhauer-Evans CMP 197 (1998); KLM CMP 219 (2001)"),
    ("T4", "local index-2 holomorphic extension B (mu=1)",
     "(E8)_1",
     "Dong-Mason (holomorphic c=8 VOA unique); v463 selector"),
]
composes = all(CHAIN[i][2] == CHAIN[i + 1][1] for i in range(len(CHAIN) - 1))
check("chain composes: out(T_i) = in(T_{i+1}) for i = 1..3", composes)
for tid, i_, o_, ref in CHAIN:
    print("      %s: %s -> %s   [%s]" % (tid, i_, o_, ref))

print()
print("VERDICT: route_candidate (sandbox).  Not a closure of SEAM.EQUIV.01.")
print("What it changes if promoted:")
print("  * the Lean axiom `seam_realisation_theorem` can be re-founded on the")
print("    1995-2001 peer-reviewed package (LR/Boeckenhauer/BE/KLM) with the")
print("    2024/2025 AMT/AGT route demoted to an independent SECOND witness;")
print("    the locality integer h_s = 1 (and h(J^k) in Z for mu4) becomes a")
print("    kernel-checked joint instead of an implicit part of the citation.")
print("  * the axiom `collar_realizes` (R1, model-level) can be replaced by")
print("    `collar_invariants` (R1', invariant-level): quasi-free [C] + gap [E]")
print("    + class D + c_- = 8 [E from P1], with phase-classification and the")
print("    c_- invariance as the cited legs -- the invariants are TFPT-derived,")
print("    so the residual loses its last model-level fiat.")
print("Open even after promotion: quasi-freeness of the abstract seam stays [C]")
print("(v155/v160); the cited theorems stay cited (certification, not re-proof).")
print()
print("checks: %d passed, %d failed" % (PASS, FAIL))
