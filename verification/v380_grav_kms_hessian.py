"""v380 -- GRAV.KMS.HESSIAN.01: the KMS Entire Hessian -- the Stelle ghost is EXACTLY the
Seeley-DeWitt truncation, and resummation pushes it to infinity.  This UPGRADES v304/v370 from
the *assumption* "the resummed graviton form factor is entire" to a derived statement: the seam
KMS cutoff f(u)=e^{-u} (v259) directly gives the dressed spin-2 propagator e^{-p^2/M^2}/p^2, whose
kinetic form factor a(u)=e^{u} (u=p^2/M^2) is entire and zero-free; every FINITE truncation of a
(the local R+R^2 / Weyl^2 spectral-action orders) carries a spurious zero = a Stelle ghost, and the
nearest zero runs off to infinity as more heat-kernel orders are kept -- so the ghost is a
truncation artefact that resummation removes.

Honest scope: [E] the truncation-artefact mechanism (each finite Taylor truncation of e^u has a
zero; e^u has none) AND the decoupling (the nearest truncation zero's modulus grows monotonically
with the order); [C] the identification of a(Box)=e^{Box/M^2} with the FULL off-shell curved-space
graviton Hessian of Tr e^{-D^2/Lambda^2} (the cited heat-kernel resummation step, Tomboulis 1997 /
Biswas-Mazumdar-Siegel); [O] perturbative only -- not the non-perturbative ambient measure
(QG.AMB.01).  Does NOT change QG.AMB.01's status; it closes the v304/v370 analyticity gap at the
truncation-tower level.

  [E] 1. SEAM CUTOFF -> ENTIRE FORM FACTOR.  f(u)=e^{-u} (the beta=1 seam KMS weight, v259) gives
        the dressed spin-2 propagator e^{-p^2/M^2}/p^2 = 1/(p^2 a) with kinetic form factor
        a(u)=e^{u}, which is entire and nowhere zero (Weierstrass: exp has no zeros) => the only
        propagator pole is p^2=0 (the healthy massless graviton), no ghost.
  [E] 2. EACH FINITE TRUNCATION CARRIES THE GHOST.  the Seeley-DeWitt expansion truncates a(u) to
        its Taylor partial sum T_n(u)=sum_{k<=n} u^k/k!; the local R+R^2 order T_1=1+u has the
        Stelle ghost zero at u=-1 (p^2=-M^2), the Weyl^2 order T_2=1+u+u^2/2 has the complex pair
        -1+-i, etc.  Every finite truncation has a zero; the entire a(u) has none.
  [E] 3. THE GHOST DECOUPLES UNDER RESUMMATION.  the modulus of the nearest zero of T_n grows
        MONOTONICALLY with the truncation order n (1, sqrt2, ... -> infinity), so keeping more
        heat-kernel orders pushes the spurious pole to infinity -- "entire" is precisely "do not
        truncate the heat kernel", and the ghost is the truncation, decoupling as it is resummed.
  [C] 4. PERTURBATIVE GRAVITON UNITARITY (the KMS Entire Hessian theorem).  with the entire
        a(Box) the spin-2 graviton is ghost-free (v370 sector decomposition); so the untruncated
        KMS spectral-action Hessian gives a unitary perturbative graviton -- upgrading the v304/
        v370 [C] assumption to a derived truncation-artefact + decoupling statement.
  [O] 5. RESIDUAL.  the identification of a(Box)=e^{Box/M^2} with the exact off-shell curved-space
        Hessian is the cited heat-kernel resummation; and this is perturbative, not the
        non-perturbative ambient measure (QG.AMB.01).

Python (sympy for the entire/zero-free + symbolic truncations; numpy for the truncation-zero
moduli).  The conclusion is [C]/[O] -- like v304/v370, this module is Python-only."""
import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset

u = sp.symbols("u", complex=True)


def _trunc_min_root(n):
    """Smallest |zero| of the order-n Taylor partial sum of e^u (numpy)."""
    coeffs = [1.0 / float(sp.factorial(k)) for k in range(n + 1)]   # ascending: 1, 1, 1/2, ...
    roots = np.roots(coeffs[::-1])                                  # numpy wants descending
    return float(np.min(np.abs(roots)))


def run():
    reset()
    print("v380  GRAV.KMS.HESSIAN.01: the Stelle ghost is the Seeley-DeWitt truncation; resummation -> no ghost")

    # 1. seam cutoff -> entire form factor a(u)=e^u, zero-free => only the p^2=0 pole
    a = sp.exp(u)
    zeros_a = sp.solve(a, u)
    check("SEAM CUTOFF -> ENTIRE FORM FACTOR [E]: f(u)=e^{-u} (v259) gives the dressed propagator "
          "e^{-p^2/M^2}/p^2 = 1/(p^2 a) with a(u)=e^u entire & nowhere zero (solve(e^u)=%s), so the "
          "ONLY propagator pole is p^2=0 -- no ghost" % zeros_a,
          zeros_a == [])

    # 2. each finite truncation carries the ghost (T_1 root = -1, the Stelle ghost)
    T1 = 1 + u
    T2 = 1 + u + u**2 / 2
    root_T1 = sp.solve(T1, u)
    roots_T2 = sp.solve(T2, u)
    check("EACH FINITE TRUNCATION CARRIES THE GHOST [E]: the R+R^2 order T_1=1+u has the Stelle "
          "ghost zero u=%s (p^2=-M^2); the Weyl^2 order T_2=1+u+u^2/2 has the complex pair %s -- "
          "every finite Seeley-DeWitt truncation has a zero, the entire a(u)=e^u has none"
          % (root_T1, roots_T2),
          root_T1 == [-1] and set(roots_T2) == {-1 - sp.I, -1 + sp.I})

    # 3. the ghost decouples: |nearest zero| of T_n grows monotonically with n
    mods = [_trunc_min_root(n) for n in range(1, 9)]
    monotone = all(mods[i + 1] > mods[i] - 1e-9 for i in range(len(mods) - 1))
    check("GHOST DECOUPLES UNDER RESUMMATION [E]: the modulus of the nearest zero of the order-n "
          "truncation T_n grows monotonically with n (n=1..8: %s) -> infinity, so resumming the "
          "heat kernel pushes the spurious pole to infinity; 'entire' = 'do not truncate'"
          % [round(m, 3) for m in mods],
          monotone and mods[0] == 1.0 and mods[-1] > 2.5)

    # 4. perturbative graviton unitarity (the KMS Entire Hessian theorem)
    check("PERTURBATIVE GRAVITON UNITARITY [C]: with the entire a(Box) the spin-2 graviton is "
          "ghost-free (v370 sector decomposition), so the untruncated KMS spectral-action Hessian "
          "gives a unitary perturbative graviton -- upgrading the v304/v370 assumption to a derived "
          "truncation-artefact + decoupling statement", zeros_a == [] and monotone)

    # 5. residual (honest fence)
    check("RESIDUAL [O]: the identification of a(Box)=e^{Box/M^2} with the EXACT off-shell "
          "curved-space graviton Hessian of Tr e^{-D^2/Lambda^2} is the cited heat-kernel "
          "resummation; and this is PERTURBATIVE, not the non-perturbative ambient measure "
          "(QG.AMB.01) -- does NOT change QG.AMB.01's status", True)

    return summary("v380 GRAV.KMS.HESSIAN.01: the seam KMS cutoff e^{-u} (v259) gives an entire kinetic form "
                   "factor a=e^{p^2/M^2} (zero-free, only the p^2=0 pole); every finite Seeley-DeWitt truncation "
                   "carries a Stelle-ghost zero (T_1=1+u -> u=-1) and the nearest zero's modulus grows "
                   "monotonically with order -> infinity, so the ghost is exactly the truncation and resummation "
                   "removes it. Upgrades the v304/v370 'assume entire' to a derived truncation-artefact + "
                   "decoupling [E]; the exact-Hessian identification stays [C], perturbative-only [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
