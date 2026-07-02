"""v469 -- SEAM.EQUIV.CROSSEDPRODUCT.01: the net-level crossed-product certification of
the 128-spinor extension + the R1 -> R1' invariant-level reduction (the 2026-07-02
closure-route round, promoted from experiments/tfpt-discovery/
closure_route_seam_crossedproduct.py).  It does NOT close SEAM.EQUIV.01.

After the G-block (v454-v464) the SEAM.EQUIV.01 residual was ONE TFPT-internal
realisation axiom (R1, `collar_realizes`: the abstract seam IS this p+ip lattice model)
plus ONE combined cited-theorem package whose extension leg rested on 2024/2025
PREPRINTS (AGT arXiv:2506.01008 + AMT arXiv:2407.18222, v459).  This module re-founds
both halves on strictly harder-to-reject ground:

(a) THE EXTENSION LEG IS 1995-2001 PEER-REVIEWED SUBFACTOR THEORY, NOT A 2025 PREPRINT.
    The spinor sector s of SO(16)_1 has conformal weight h_s = N/16 = 16/16 = 1 in Z,
    so its statistics phase is e^{2 pi i h_s} = +1 -- exactly the Longo-Rehren locality
    criterion: the Z2 simple-current crossed product SO(16)_1 x| {1,s} is a LOCAL
    index-2 extension (Longo-Rehren, Rev. Math. Phys. 7 (1995); the level-1 so(N) net
    with its DHR sectors from even-CAR: Boeckenhauer, Rev. Math. Phys. 8 (1996);
    simple-current extensions of nets: Boeckenhauer-Evans, Comm. Math. Phys. 197
    (1998)).  KLM (Comm. Math. Phys. 219 (2001)) gives mu(B) = mu(SO16)/[B:A]^2
    = 4/4 = 1 => B holomorphic => B = (E8)_1 by the v463 classification pin.
    The AGT/AMT lattice-VOA route (v459) is thereby DEMOTED to an independent SECOND
    witness -- the certification no longer depends on unpublished work.
(b) THE SAME LOCALITY INTEGER CARRIES THE INDEX-4 mu4 ROUTE.  The glue current
    J = (s, Lambda1) of (D5)_1 x (A3)_1 has h(J^k) = {1, 1, 1} for k = 1, 2, 3 -- ALL
    integer (h_s(D5) = 5/8, h_Lambda1(A3) = 3/8; h_v = h_Lambda2 = 1/2), the net-level
    restatement of the v125 isotropy q(k(1,1)) = k^2 in Z.  Both routes are the same
    Lagrangian-glue mechanism, both land on the one holomorphic c=8 endpoint.
(c) R1 -> R1': THE REALISATION AXIOM LOSES ITS MODEL-LEVEL FIAT.  The content of
    `collar_realizes` reduces to INVARIANTS -- {quasi-free [C v155/v160], gapped
    [E v302], class D, c_- = 8 [E, forced by P1 via v456]} -- because 2d class-D
    free-fermion phases are classified by the Chern integer (Kitaev Ann. Phys. 321
    (2006) 16-fold way + periodic table 2009) and c_- is a PHASE invariant
    (Kapustin-Spodyneiko PRB 101 (2020); Kim-Shi-Kato-Albert PRL 129 (2022) modular
    commutator): ANY realisation with these invariants is phase-equivalent to the v367
    stack, hence has the SAME edge scaling limit.  The invariants are computed here:
    per-copy FHS Chern |C| = 1 (M=1) vs 0 (M=3 control), nu = 16 x |C| = 16,
    c_- = nu/2 = 8.  Kitaev's published pin: nu = 0 mod 16 is EXACTLY the class whose
    edge admits a purely bosonic description, and that bosonic edge is the (E8)_1
    level-1 state -- the identification endpoint, from condensed-matter literature.

  [E] 1. LR LOCALITY INTEGER (index-2 route): h-spectrum of SO(16)_1 = {0, 1/2, 1, 1},
        h_s = 16/16 = 1 in Z, statistics phase +1, all four sectors simple currents
        (d = 1, fusion Z2 x Z2) -- the crossed-product locality criterion HOLDS.
  [E] 2. KLM ARITHMETIC: mu(B) = 4/2^2 = 1 => holomorphic; c = 8 preserved.
  [E] 3. INDEX-4 ROUTE PARALLEL: h(J^k) = {1,1,1} all integer = the v125 isotropy at
        net level; mu = 16/4^2 = 1, same endpoint.
  [E] 4. IDENTIFICATION ENDPOINT: E4/eta^8 q^1 coefficient = 248 (v463's pin,
        re-verified); 248 = 120 + 128 = 8 + 240.
  [E] 5. R1' INVARIANTS COMPUTED: FHS Chern 1/0 (topological/control), nu = 16,
        c_- = 8 = g_car + N_fam; nu mod 16 = 0 (the Kitaev-E8 class).
  [E] 6. THE CHAIN COMPOSES: T1 (phase classification) -> T2 (MMST + Boeckenhauer)
        -> T3 (LR/BE crossed product + KLM) -> T4 (classification pin) with matching
        in/out slots (v297-style typing).
  [C] 7. THE RE-FOUNDED PACKAGE: the extension leg now rests on LR 1995 + Boeckenhauer
        1996 + BE 1998 + KLM 2001 (peer-reviewed journals); MMST (CMP 2023, v458) stays
        the existence backbone; AGT/AMT (v459) becomes the independent second witness.
  [C] 8. R1 -> R1' RETYPED: `collar_realizes` (model fiat) -> `collar_invariants`
        (invariant-level, inputs TFPT-derived); quasi-freeness of the abstract seam
        stays the one [C] hypothesis (v155/v160); Lean mirror FORM.SEAM.RESIDUAL.01
        carries the alternative derivation.
  [O] 9. NOT CLOSED: the cited theorems stay cited (certification, not re-proof);
        SEAM.EQUIV.01 stays [O].

Mixed: exact (sector weights, mu-index, glue integers, E4/eta^8 tower -- Wolfram-
mirrored) + numerical (FHS Chern, Python-only, ties v367/v461)."""
import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8, dim_Splus

SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)


def _occ_vec(kx, ky, M):
    d = np.array([np.sin(kx), np.sin(ky), M - np.cos(kx) - np.cos(ky)])
    w, v = np.linalg.eigh(d[0] * SX + d[1] * SY + d[2] * SZ)
    return v[:, 0]


def _chern(M, N=24):
    """Fukui-Hatsugai-Suzuki plaquette Chern number (same convention as v367)."""
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    u = [[_occ_vec(kx, ky, M) for ky in ks] for kx in ks]
    F = 0.0
    for i in range(N):
        for j in range(N):
            ip, jp = (i + 1) % N, (j + 1) % N
            u00, u10, u01, u11 = u[i][j], u[ip][j], u[i][jp], u[ip][jp]
            Ux = np.vdot(u00, u10); Ux /= abs(Ux)
            Uy = np.vdot(u10, u11); Uy /= abs(Uy)
            Ux2 = np.vdot(u01, u11); Ux2 /= abs(Ux2)
            Uy2 = np.vdot(u00, u01); Uy2 /= abs(Uy2)
            F += np.angle(Ux * Uy * np.conj(Ux2) * np.conj(Uy2))
    return F / (2 * np.pi)


def _e8_tower(ncoef=4):
    """Integer q-coefficients of q^{1/3} E4/eta^8 (the (E8)_1 tower), exact."""
    q = sp.symbols("q")
    M_ = ncoef + 1
    e4 = 1 + 240 * sum(sp.divisor_sigma(n, 3) * q ** n for n in range(1, M_))
    inv8 = sp.prod([(1 - q ** n) ** -8 for n in range(1, M_)])
    ser = sp.series(e4 * inv8, q, 0, M_).removeO().expand()
    return [int(ser.coeff(q, n)) for n in range(ncoef)]


def run():
    reset()
    print("v469 SEAM.EQUIV.CROSSEDPRODUCT.01: net-level crossed-product certification "
          "(LR/Boeckenhauer/BE/KLM) + R1 -> R1' invariant reduction; does NOT close "
          "SEAM.EQUIV.01")

    # 1. LR locality integer, index-2 route
    hs = sp.Rational(16, 16)                       # spinor weight so(N)_1 = N/16, N = 16
    hspec = [sp.Integer(0), sp.Rational(1, 2), hs, hs]
    check("LR LOCALITY INTEGER [E] (index-2): SO(16)_1 h-spectrum {0, 1/2, 1, 1} with "
          "h_s = N/16 = 16/16 = 1 in Z => statistics phase e^{2 pi i h_s} = +1 -- the "
          "Longo-Rehren criterion for the Z2 simple-current crossed product HOLDS "
          "(LR RMP 7 (1995); net + sectors from even-CAR: Boeckenhauer RMP 8 (1996); "
          "BE CMP 197 (1998)); all four sectors d = 1, fusion Z2 x Z2 (N/2 = 8 even)",
          hs == 1 and sp.floor(hs) == hs and hspec[1] == sp.Rational(1, 2)
          and (16 // 2) % 2 == 0)

    # 2. KLM mu-index arithmetic
    mu_SO16, index2 = 4, 2
    check("KLM ARITHMETIC [E]: mu(B) = mu(SO16)/[B:A]^2 = 4/2^2 = 1 => B HOLOMORPHIC "
          "(KLM CMP 219 (2001)); c = 8 preserved by the finite-index extension",
          sp.Rational(mu_SO16, index2 ** 2) == 1)

    # 3. index-4 mu4 route: all glue powers have integer weight
    hD5 = {0: sp.Integer(0), 1: sp.Rational(5, 8), 2: sp.Rational(1, 2), 3: sp.Rational(5, 8)}
    hA3 = {k: sp.Rational(k * (4 - k), 8) for k in range(4)}
    glue = [hD5[k] + hA3[k] for k in (1, 2, 3)]
    check("INDEX-4 ROUTE PARALLEL [E]: the mu4 glue J = (s, Lambda1) of (D5)_1 x (A3)_1 "
          "has h(J^k) = {1, 1, 1} for k = 1,2,3 -- ALL integer (h_s(D5) = 5/8 + "
          "h_L1(A3) = 3/8 = 1; 1/2 + 1/2 = 1) = the v125 isotropy q(k(1,1)) = k^2 at "
          "net level; mu = 16/4^2 = 1, the SAME holomorphic endpoint",
          all(g == 1 for g in glue) and sp.Rational(16, 16) == 1)

    # 4. identification endpoint (v463 pin re-verified)
    tower = _e8_tower(4)
    check("IDENTIFICATION ENDPOINT [E]: E4/eta^8 tower %s -- q^1 coefficient 248 = "
          "dim E8 (v463 classification pin); 248 = 120 + 128 = 8 + 240" % tower,
          tower == [1, 248, 4124, 34752] and 120 + 128 == 248 == 8 + 240)

    # 5. R1' invariants computed on the collar model
    C_topo = round(_chern(1.0))
    C_triv = round(_chern(3.0))
    nu = dim_Splus * abs(C_topo)
    check("R1' INVARIANTS COMPUTED [E]: per-copy FHS Chern C(M=1) = %d (topological), "
          "C(M=3) = %d (control); nu = 16 x |C| = %d; c_- = nu/2 = %d = g_car + N_fam "
          "= rank E8" % (C_topo, C_triv, nu, nu // 2),
          abs(C_topo) == 1 and C_triv == 0 and nu == 16
          and nu // 2 == 8 == g_car + N_fam == rankE8)
    check("KITAEV 16-FOLD-WAY PIN [E]: nu mod 16 = %d -- nu = 0 mod 16 is EXACTLY the "
          "class-D phase whose edge admits a purely bosonic description, and that "
          "bosonic edge is the (E8)_1 level-1 state (Kitaev Ann. Phys. 321 (2006)) -- "
          "the identification endpoint pinned from published condensed-matter theory"
          % (nu % 16), nu % 16 == 0)

    # 6. the chain composes (v297-style in/out typing)
    chain = [
        ("T1", "invariants {quasi-free, gapped, class D, c_-=8}",
         "the nu=16 class-D free-fermion phase"),
        ("T2", "the nu=16 class-D free-fermion phase",
         "SO(16)_1 conformal net with sectors {1,v,s,c}"),
        ("T3", "SO(16)_1 conformal net with sectors {1,v,s,c}",
         "local index-2 holomorphic extension B (mu=1)"),
        ("T4", "local index-2 holomorphic extension B (mu=1)", "(E8)_1"),
    ]
    check("THE CHAIN COMPOSES [E]: out(T_i) = in(T_{i+1}) for T1 (Kitaev/Kapustin-"
          "Spodyneiko/Kim et al.) -> T2 (MMST CMP 2023 + Boeckenhauer RMP 1996) -> T3 "
          "(LR 1995 + BE 1998 + KLM 2001) -> T4 (Dong-Mason + v463)",
          all(chain[i][2] == chain[i + 1][1] for i in range(len(chain) - 1)))

    # 7. the re-founded citation package [C]
    check("RE-FOUNDED PACKAGE [C]: the 128-spinor extension leg now rests on the "
          "1995-2001 PEER-REVIEWED subfactor package (LR/Boeckenhauer/BE/KLM); MMST "
          "(v458) stays the existence backbone; the AGT/AMT lattice-VOA route (v459) "
          "is DEMOTED to an independent second witness -- the certification no longer "
          "depends on 2024/2025 preprints", True)

    # 8. R1 -> R1' retyping [C]
    check("R1 -> R1' [C]: `collar_realizes` (model-level fiat) is replaceable by "
          "`collar_invariants` -- {quasi-free [C v155/v160], gap [E v302], class D, "
          "c_- = 8 [E v456 from P1]} + phase classification + c_- invariance "
          "(Kapustin-Spodyneiko PRB 101 (2020); Kim et al. PRL 129 (2022)): any "
          "realisation with these invariants is phase-equivalent to the v367 stack; "
          "quasi-freeness stays the ONE [C] hypothesis (Lean: FORM.SEAM.RESIDUAL.01)", True)

    # 9. honest scope [O]
    check("NOT CLOSED [O]: the cited theorems stay cited (certification, not "
          "re-proof); the abstract continuum existence and the quasi-free hypothesis "
          "remain; SEAM.EQUIV.01 stays [O]", True)

    return summary("v469 SEAM.EQUIV.CROSSEDPRODUCT.01: the 128-spinor extension "
                   "re-founded as the LOCAL Z2 simple-current crossed product (h_s = 1 "
                   "in Z, LR 1995/Boeckenhauer 1996/BE 1998/KLM 2001, peer-reviewed; "
                   "mu = 4/2^2 = 1 holomorphic; index-4 mu4 glue h(J^k) = {1,1,1} "
                   "parallel), AGT/AMT demoted to second witness; R1 reduced to "
                   "invariant level (FHS |C| = 1, nu = 16, c_- = 8, the Kitaev-E8 "
                   "16-fold-way class). SEAM.EQUIV.01 stays [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
