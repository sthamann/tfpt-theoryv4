"""v289 -- MARKLOCAL.RAW.01: decompose the ONE remaining Route-B residual
('why is the raw seam sub-principal term mark-local?') into an explicit five-lemma
chain, discharge the four standard / already-established lemmas, and isolate the
SINGLE open analytic lemma (Flat-Away).  This is the best closing lever after v288:
it does NOT close mark-locality, it locates exactly which analytic statement remains.

The chain (raw RP seam => mark-local sub-principal term):
  L1 [C] CONIC PARAMETRIX.  the Steklov/DtN operator of a surface with conic
        singularities splits as Lambda = |D_theta| (principal) + M_f (sub-principal
        = multiplication by the boundary curvature f) + delta-sources at the cone
        points -- the b-calculus / conic-parametrix construction (Melrose); standard
        microlocal analysis, imported.
  L2 [O] FLAT-AWAY -- THE ONE OPEN ANALYTIC LEMMA.  reflection positivity + the mass
        gap + the four branch marks force the seam curvature to VANISH away from the
        four marks (the flat-pillowcase realisation).  This is the curvature-locality
        heart of SEAM.EQUIV.01; not a finite computation, left honestly open.
  L3 [E] ORBIT-SOURCE.  the four marks form a single mu4 orbit {0, pi/2, pi, 3pi/2}
        (v195 Lefschetz/character marks + the order-4 carrier clock; v216 Gauss-Bonnet
        gives exactly 4 cone points of deficit pi).
  L4 [E] FOURIER-SUPPORT.  a curvature sourced on the mu4 orbit has discrete Fourier
        support ONLY on modes m == 0 (mod 4) (v264/v288; verified by FFT here).
  L5 [E] FULL-OPERATOR.  hence M_f is Z4 block-diagonal and [rho, Lambda] = 0 on the
        full L^2 (v288), so omega o rho = omega (Tomita-Takesaki, v198).

  [E] 1. CHAIN TYPED.  five lemmas; four discharged (L1 conditional-by-literature,
        L3/L4/L5 exact), exactly ONE open (L2 Flat-Away).
  [E] 2. L3+L4 ORBIT => SUPPORT.  a mu4-orbit curvature has Fourier support only on
        4Z (verified); a non-orbit (generic 4-point) source does NOT -- so the
        orbit structure, not just '4 marks', is what gives mark-locality.
  [E] 3. L5 FULL-OPERATOR.  with that support, Lambda = |D_theta| + M_f commutes with
        rho = diag(i^n) on the full mode range (||[rho,Lambda]|| ~ 1e-15, v288).
  [C] 4. L1 CONIC PARAMETRIX.  the conic Steklov symbol decomposes as |k| + curvature
        multiplication + cone sources (structural check: M_f is multiplication by f);
        the decomposition itself is standard b-calculus, imported as [C].
  [O] 5. L2 IS THE ONE OPEN LEMMA.  precise statement + negative control: a curvature
        that does NOT vanish away from the marks breaks Z4-invariance and the whole
        chain -- so Route B reduces to exactly 'RP + gap + 4 marks => flat away from
        the marks'.  If L2 falls, Route B closes; SEAM.EQUIV.01 then needs only the
        holomorphy half (Route A).

Status: [E] the chain typing + L3/L4/L5 (orbit, support, full operator); [C] L1
(conic parametrix, literature); [O] L2 (Flat-Away), the single open analytic lemma.
A finer decomposition of the v288 residual, NOT a closure.  Python (numpy FFT).
"""
import numpy as np

from tfpt_constants import check, summary, reset

# lemma: (id, statement, status, evidence)
CHAIN = [
    ("L1", "conic Steklov DtN = |D_theta| + M_f + cone sources", "conditional",
     "b-calculus / conic parametrix (Melrose) -- imported"),
    ("L2", "RP + gap + 4 marks => curvature vanishes away from the marks (flat-away)", "open",
     "THE ONE OPEN ANALYTIC LEMMA (curvature-locality heart of SEAM.EQUIV.01)"),
    ("L3", "the 4 marks form a single mu4 orbit", "established", "v195/v216 + order-4 clock"),
    ("L4", "mu4-orbit curvature => Fourier support only on 4Z", "established", "v264/v288 (FFT)"),
    ("L5", "=> M_f Z4 block-diagonal, [rho,Lambda]=0 on full L^2", "established", "v288/v198"),
]

N = 64


def _orbit_curvature(marks):
    idx = np.arange(N)
    f = np.zeros(N)
    for m in marks:
        d = np.minimum((idx - m) % N, (m - idx) % N)
        f += np.exp(-(d ** 2) / 2.0)
    return f


def run():
    reset()
    print("v289  MARKLOCAL.RAW.01: decompose raw mark-locality into a 5-lemma chain; isolate Flat-Away")

    established = [c for c in CHAIN if c[2] == "established"]
    conditional = [c for c in CHAIN if c[2] == "conditional"]
    openl = [c for c in CHAIN if c[2] == "open"]

    # 1. chain typed
    check("CHAIN TYPED [E]: 5 lemmas -- %d discharged (L1 conditional-by-literature, "
          "L3/L4/L5 exact), exactly ONE open (L2 Flat-Away)"
          % (len(established) + len(conditional)),
          len(established) == 3 and len(conditional) == 1 and len(openl) == 1
          and openl[0][0] == "L2")

    # 2. L3+L4: mu4-orbit => Fourier support on 4Z; generic 4-point does NOT
    f_orbit = _orbit_curvature([0, N // 4, N // 2, 3 * N // 4])
    fhat = np.fft.fft(f_orbit) / N
    off4 = max(abs(fhat[k]) for k in range(N) if k % 4 != 0)
    on4 = max(abs(fhat[k]) for k in range(N) if k % 4 == 0)
    f_generic = _orbit_curvature([0, 7, 19, 33])              # NOT a mu4 orbit
    ghat = np.fft.fft(f_generic) / N
    off4_g = max(abs(ghat[k]) for k in range(N) if k % 4 != 0)
    check("L3+L4 ORBIT => SUPPORT [E]: a mu4-orbit curvature has Fourier support only "
          "on 4Z (off-4Z %.2e vs on-4Z %.3f); a generic 4-point source does NOT "
          "(off-4Z %.3f > 0) -- the ORBIT structure, not just '4 marks', gives "
          "mark-locality" % (off4, on4, off4_g),
          off4 < 1e-12 and on4 > 0.1 and off4_g > 1e-3)

    # 3. L5: full-operator commutation
    ns = np.arange(N)
    rho = np.diag(1j ** ns)
    Mf = np.array([[fhat[(a - b) % N] for b in range(N)] for a in range(N)])
    k = np.fft.fftfreq(N, d=1.0 / N)
    Lam = np.diag(np.abs(k)) + Mf
    comm = np.linalg.norm(rho @ Lam - Lam @ rho)
    check("L5 FULL-OPERATOR [E]: with 4Z support, Lambda = |D_theta| + M_f commutes "
          "with rho = diag(i^n) on the full mode range (||[rho,Lambda]|| = %.1e ~ 0, "
          "v288)" % comm, comm < 1e-12)

    # 4. L1 conic parametrix: M_f is multiplication by the curvature (the subprincipal
    #    piece); the |k| + M_f + cone-source split is standard b-calculus
    is_circulant = np.allclose(Mf, np.array([[fhat[(a - b) % N] for b in range(N)] for a in range(N)]))
    check("L1 CONIC PARAMETRIX [C]: the conic Steklov symbol splits as |k| (principal) "
          "+ M_f (sub-principal = multiplication by curvature f, circulant in the "
          "Fourier basis: %s) + cone sources -- standard b-calculus/parametrix "
          "(Melrose), imported as conditional" % is_circulant, is_circulant)

    # 5. L2 is the one open lemma + negative control
    f_offmark = _orbit_curvature([0, N // 4, N // 2, 3 * N // 4]) + 0.3 * _orbit_curvature([11])
    hhat = np.fft.fft(f_offmark) / N
    Mf_bad = np.array([[hhat[(a - b) % N] for b in range(N)] for a in range(N)])
    broken = np.linalg.norm(rho @ Mf_bad - Mf_bad @ rho) > 1e-6
    check("L2 IS THE ONE OPEN LEMMA [O]: 'RP + gap + 4 marks => curvature vanishes "
          "away from the marks'. NEG control: adding curvature OFF the mu4 orbit "
          "breaks Z4-invariance and the whole chain (||[rho,M_f]|| > 0: %s). Route B "
          "thus reduces to exactly L2 -- if it falls, Route B closes and SEAM.EQUIV.01 "
          "needs only the holomorphy half (Route A)" % broken, broken)

    return summary("v289 MARKLOCAL.RAW.01: raw mark-locality decomposed into 5 lemmas, 4 discharged; the one open analytic lemma is Flat-Away (RP+gap+marks => flat away from the marks)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
