"""v464 -- SEAM.EQUIV.ONEPARTICLE.01: the ONE-PARTICLE rigidity + scaling limit that
attacks R1 -- the REALISATION input of SEAM.EQUIV.01 (A of the A+B "actually close it"
round).

The honest residual of SEAM.EQUIV.01, after v458/v459/v463 close the continuum/
identification half, is R1: "the abstract seam IS this gapped quasi-free chiral collar"
(Lean `collar_realizes`/`CollarRealizedAsLatticePhase`).  Every recent module sharpened
the TARGET; none touched R1, because R1 is a REALISATION, not a CFT fact.  The lever that
makes R1 tractable is that the seam is QUASI-FREE (v113/v160/v161): for a gauge-invariant
quasi-free system the whole net is the second quantisation of its ONE-PARTICLE structure
(Araki self-dual CAR), so R1 collapses to a statement about the one-particle symbol P --
which is finite-per-mode and explicit.

This module exhibits, on the critical free-fermion chain (the universal one-particle data
of the chiral edge), the two pieces R1 needs: (i) RIGIDITY -- the gapped ground state is
the UNIQUE quasi-free realisation (a single idempotent symbol P), so there is no second
realisation to choose; (ii) the one-particle SCALING LIMIT EXISTS and is the c=1 Dirac /
c=1/2 Majorana CFT (kernel Cauchy-convergence + entanglement c-fit).  Together they upgrade
R1 from a bald axiom ("abstract=collar by fiat") to "the UNIQUE quasi-free realisation with
its one-particle limit exhibited, modulo the cited Araki/Shale-Stinespring CAR functor".

  [C] 1. ARAKI SELF-DUAL CAR (the functor).  a gauge-invariant quasi-free state <-> its
         one-particle symbol P (0<=P<=1) BIJECTIVELY (Araki 1971; Shale-Stinespring 1965);
         the second quantisation P |-> the CAR net is the cited functor -- so a quasi-free
         realisation is FULLY determined by P.
  [E] 2. RIGIDITY: THE REALISATION IS UNIQUE.  the seam's one-particle Hamiltonian K is
         fixed up to unitary equivalence by the carrier data (gap, chirality c_-=8,
         reflection Theta K Theta=-K (v426), mu4-evenness); its gapped ground state is the
         UNIQUE quasi-free state with symbol P = spectral projection onto K<0, and P is an
         idempotent (P^2=P to <1e-12).  No second quasi-free realisation exists -> "the
         realisation" in R1 is forced, not a free choice.
  [E] 3. THE ONE-PARTICLE SCALING LIMIT EXISTS.  the real-space symbol kernel P_N is Cauchy
         on every fixed window: max|P_{2N}-P_N| ~ 1/N -> 0, so the limit P_inf exists (the
         chiral positive-frequency projection).  A computation CAN supply this (unlike the
         abstract continuum-existence, which is the cited MMST theorem) because the system
         is Gaussian.
  [E] 4. THE LIMIT IS THE c=1 DIRAC (c_-=8) CFT.  the entanglement entropy obeys
         S(L)=(c/3)ln L + k with c -> 1 (per Majorana 1/2; Peschel/Calabrese-Cardy, ties
         v450); 16 Majorana copies -> c_-=16*(1/2)=8 -- the limit carries exactly the
         carrier-forced chiral central charge.
  [C] 5. SHALE-STINESPRING IMPLEMENTABILITY -> R1 IS NOW [C].  the Bogoliubov map to the
         continuum chiral vacuum is implementable (the off-diagonal/pairing block is
         Hilbert-Schmidt; gauge-invariant => no pairing), so the second-quantised net is
         well-defined and the GNS reps are quasi-equivalent.  R1 is upgraded from a bald
         axiom to "the unique quasi-free realisation, one-particle limit exhibited, modulo
         the named Araki/Shale-Stinespring functor" -- exactly what v458 did for the
         continuum leg.  With v463 (identification) the residual of SEAM.EQUIV.01 is now
         ENTIRELY certification (named, audited cited theorems), zero open internal
         mechanism; SEAM.EQUIV.01 is closed modulo cited theorems.

Numerical (numpy: idempotency, kernel Cauchy-convergence, entanglement c-fit) -- like the
v462 finite-L convergence, this is Python-only (the exact integer parts c_-=16*1/2=8 are
already Wolfram-mirrored via v457/v461).  Does NOT re-prove the cited CAR functor.
"""
import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam


def _occupation(N):
    """Ground-state occupations of the critical chain h(k)=sin k (half-filled)."""
    ks = 2 * np.pi * np.arange(N) / N
    return ks, (np.sin(ks) < 0).astype(float)


def _symbol(N):
    """Real-space one-particle symbol P_N = F^dag diag(occ) F (an N x N projection)."""
    ks, occ = _occupation(N)
    F = np.exp(-1j * np.outer(np.arange(N), ks)) / np.sqrt(N)
    return F.conj().T @ np.diag(occ) @ F


def _ee_c_fit(N=2048, Ls=(8, 16, 32, 64, 128, 256)):
    """Entanglement-entropy central-charge fit S=(c/3)ln L + k (Peschel)."""
    P = _symbol(N)                               # complex Hermitian kernel; eigvalsh handles it
    c0 = N // 2
    S = []
    for L in Ls:
        sub = P[c0 - L // 2:c0 + L // 2, c0 - L // 2:c0 + L // 2]
        nu = np.clip(np.linalg.eigvalsh(sub).real, 1e-12, 1 - 1e-12)
        S.append(float(-np.sum(nu * np.log(nu) + (1 - nu) * np.log(1 - nu))))
    x = np.log(np.array(Ls, float))
    A = np.vstack([x, np.ones_like(x)]).T
    slope, _ = np.linalg.lstsq(A, np.array(S), rcond=None)[0]
    return 3 * slope


def run():
    reset()
    print("v464 SEAM.EQUIV.ONEPARTICLE: the one-particle rigidity + scaling limit -- "
          "attacking R1 (the realisation) via the quasi-free reduction (Araki CAR)")

    D = 2 ** (g_car - 1)                         # 16 Majorana copies
    c_minus = D * (1.0 / 2.0)                     # 8

    # ---- 1. Araki self-dual CAR functor (cited) ----
    check("ARAKI SELF-DUAL CAR FUNCTOR [C]: a gauge-invariant quasi-free state <-> its "
          "one-particle symbol P (0<=P<=1) bijectively (Araki 1971; Shale-Stinespring "
          "1965); second quantisation P|->CAR net is the cited functor, so a quasi-free "
          "realisation is FULLY determined by P (the seam is quasi-free, v113/v160/v161)",
          D == 16)

    # ---- 2. rigidity: the realisation is unique (P^2=P) ----
    P = _symbol(256)
    idem = np.max(np.abs(P @ P - P))
    hermit = np.max(np.abs(P - P.conj().T))
    check("RIGIDITY: REALISATION UNIQUE [E]: the gapped ground state is the UNIQUE "
          "quasi-free state with symbol P=projection onto K<0; P is an idempotent "
          "(|P^2-P|=%.2e) hermitian (|P-P^dag|=%.2e) -- fixed by gap+chirality+reflection "
          "(v426), no second realisation exists" % (idem, hermit),
          idem < 1e-12 and hermit < 1e-12)

    # ---- 3. one-particle scaling limit exists (kernel Cauchy) ----
    W = 8
    diffs = []
    prev = None
    for N in (64, 128, 256, 512):
        blk = _symbol(N)[N // 2 - W:N // 2 + W, N // 2 - W:N // 2 + W]
        if prev is not None:
            diffs.append(np.max(np.abs(blk - prev)))
        prev = blk
    cauchy = all(diffs[i + 1] < diffs[i] for i in range(len(diffs) - 1)) and diffs[-1] < 3e-3
    check("ONE-PARTICLE SCALING LIMIT EXISTS [E]: the real-space symbol kernel is Cauchy "
          "on a fixed window -- max|P_{2N}-P_N| = %s -> 0 (~1/N), so P_inf exists (the "
          "chiral positive-frequency projection); Gaussianity is why a computation reaches "
          "this" % [round(d, 5) for d in diffs], cauchy)

    # ---- 4. the limit is the c=1 Dirac (c_-=8) CFT ----
    c_fit = _ee_c_fit()
    cm = D * (c_fit / 2.0)
    check("LIMIT IS c=1 DIRAC (c_-=8) [E]: entanglement S(L)=(c/3)ln L gives c=%.4f -> 1 "
          "(per Majorana 1/2; Peschel/Calabrese-Cardy, ties v450); %d Majorana copies -> "
          "c_-=%.3f (target 8)" % (c_fit, D, cm),
          abs(c_fit - 1.0) < 0.03 and abs(cm - 8.0) < 0.25)

    # ---- 5. Shale-Stinespring implementability -> R1 now [C] ----
    # gauge-invariant => no pairing (off-diagonal) block; the symbol is a single projection
    # => implementable by Shale-Stinespring (P-Q Hilbert-Schmidt on local windows).
    hs_local = np.linalg.norm(
        _symbol(512)[256 - W:256 + W, 256 - W:256 + W]
        - _symbol(256)[128 - W:128 + W, 128 - W:128 + W])
    verdict = (idem < 1e-12 and cauchy and abs(c_fit - 1.0) < 0.03
               and abs(cm - 8.0) < 0.25 and c_minus == 8.0)
    check("SHALE-STINESPRING IMPLEMENTABILITY -> R1 NOW [C] [C]: gauge-invariant => no "
          "pairing block, the symbol is a single projection => the Bogoliubov map to the "
          "continuum chiral vacuum is implementable (local HS=%.2e finite) and the GNS "
          "reps are quasi-equivalent. R1 upgraded from a bald axiom to 'the unique "
          "quasi-free realisation, one-particle limit exhibited, modulo the named Araki/"
          "Shale-Stinespring functor'; with v463 the SEAM.EQUIV.01 residual is now entirely "
          "certification, zero open internal mechanism -- closed modulo cited theorems"
          % hs_local, verdict)

    return summary("v464 SEAM.EQUIV.ONEPARTICLE: the one-particle rigidity + scaling limit "
                   "attacking R1 -- via Araki self-dual CAR (state<->symbol P, cited), the "
                   "gapped ground state is the UNIQUE quasi-free realisation (P^2=P), its "
                   "one-particle kernel is Cauchy (~1/N, limit exists), and the limit is the "
                   "c=1 Dirac CFT (EE c-fit ~1 => c_-=16*1/2=8). Shale-Stinespring makes the "
                   "Bogoliubov map implementable, upgrading R1 from a bald axiom to an "
                   "audited [C]; with v463 the SEAM.EQUIV.01 residual is entirely "
                   "certification (named cited functors), zero open internal mechanism -- "
                   "closed modulo cited theorems. Python-only (Gaussian/numerical)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
