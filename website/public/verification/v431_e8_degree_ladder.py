"""v431 -- E8.DEGREE.LADDER.01: the reverse-audit 'unmapped' E8 Casimir degrees
are NOT diffuse overhead -- they are the forced two-family decomposition
  E8 degrees = 6 * spine{2,3,4,5}  U  ({2} U flavor det-ladder{8,14,20}),
the two arithmetic progressions being the residue classes {0,2} mod 6, FORCED by
h(E8)=30=2*3*5.  This is the structural complement of v354/v355 (the reverse audit)
and v430 (the sheet/deck complement): it reclassifies four of the five 'unmapped'
degrees and reduces the residual to ZERO unfamilied degrees -- WITHOUT crossing the
v355 discipline line (the FUNCTORIAL flavor identification stays [P]).

  [E] 1. THE TWO-FAMILY SPLIT IS FORCED BY 30 = 2*3*5.  E8 exponents are exactly
         the phi(30)=8 totatives of h(E8)=30 (v223), hence coprime to 6, hence
         == +-1 mod 6; so the degrees (=exp+1) occupy ONLY the residue classes
         {0,2} mod 6.  Two arithmetic progressions, forced by the prime content of
         the Coxeter number 30 = 2*N_fam*g_car.
  [I] 2. THE 6k FAMILY IS 6 x THE SPINE.  degrees == 0 mod 6 = {12,18,24,30};
         divided by 6 = {2,3,4,5} = the v91 spine {e3,e1,e2,p0}(a=(1,1,2)) =
         {2,4,5,3}.  (30 = 6*g_car is the matched Coxeter readout; 12,18,24 were
         'unmapped'.)
  [I] 3. THE 6k+2 FAMILY IS THE QUADRATIC CASIMIR PLUS THE FLAVOR DET-LADDER.
         degrees == 2 mod 6 = {2,8,14,20}; {8,14,20} = (det R, det C, det L) =
         the winding line det M(s,0) = 6s+8 of the flavor diamond (v135), with
         C = R + Q diag(1,0,0).  2 = the matched quadratic/metric Casimir.
         (8 = det R is over-determined: also rank E8, a MATCHED degree.)
  [E] 4. '18' IS NOT A HOLDOUT.  18 = 6*3 = 6*N_fam: it is the spine-family member
         6*p0, not on the det-ladder (6s+8=18 has no integer s).  It changes
         FAMILY, not status -- there is no genuinely orphan degree.
  [E] 5. SPECIAL TO E8 AMONG THE SIMPLY-LACED EXCEPTIONALS.  The clean {0,2}-mod-6
         split needs both 6|h and exponents=totatives(h); among {A4,D5,E6,E7,E8,
         F4,G2} it holds for E8,F4,G2 (and A4 fails the mod-6 cleanliness) but
         FAILS for E6,E7,D5 -- and only E8 also carries the spine + flavor-det
         content.  So the decomposition is not a generic mod-6 triviality.
  [P] 6. HONEST v355 LINE (the discipline upheld).  The ARITHMETIC decomposition
         is exact [E]/[I]; but the FUNCTORIAL claim 'the E8 6k+2 Casimir stratum
         IS the flavor sheet operators' needs a representation-theoretic map and
         stays [P]/[C].  Degrees 12 and 24 still admit two canonical readings each
         (6*spine vs A3-Weyl |R(A3)|=12, |W(A3)|=24), so this is a STRUCTURE
         theorem (degrees = 6*spine U det-ladder, forced by 2,3,5), NOT a forced
         functorial flavor map.  It reclassifies v354's overhead; it closes no gate.

Exact integer/lattice [E]/[I] + honest [P] residual.  Mirrored in
wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

# the flavor diamond winding line (v135): M(s,0) = R + Q diag(s,0,0); C = M(1,0)
R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])

# exponents of the relevant root systems (degrees = exponent + 1)
EXPONENTS = {
    "A4": [1, 2, 3, 4],
    "D5": [1, 3, 5, 7, 4],
    "E6": [1, 4, 5, 7, 8, 11],
    "E7": [1, 5, 7, 9, 11, 13, 17],
    "E8": [1, 7, 11, 13, 17, 19, 23, 29],
    "F4": [1, 5, 7, 11],
    "G2": [1, 5],
}
COXETER = {"A4": 5, "D5": 8, "E6": 12, "E7": 18, "E8": 30, "F4": 12, "G2": 6}


def run():
    reset()
    print("v431  E8.DEGREE.LADDER.01: unmapped degrees = 6*spine U flavor det-ladder")

    exp = EXPONENTS["E8"]
    deg = [e + 1 for e in exp]
    h = COXETER["E8"]
    matched = [2, 8, 30]                       # v354: metric, rank->c3, Coxeter->g_car
    unmapped = [d for d in deg if d not in matched]   # {12,14,18,20,24}

    # 1. the two-family split is FORCED by 30 = 2*3*5
    tot30 = [k for k in range(1, h) if sp.gcd(k, h) == 1]
    exp_mod6 = sorted({e % 6 for e in exp})
    deg_mod6 = sorted({d % 6 for d in deg})
    check("TWO-FAMILY SPLIT FORCED BY 30=2*3*5 [E]: E8 exponents = the phi(30)=8 "
          "totatives of h(E8)=30=2*N_fam*g_car (coprime to 6 => ==+-1 mod 6), so "
          "degrees occupy ONLY residue classes {0,2} mod 6 -- two arithmetic "
          "progressions forced by the prime content of 30",
          exp == tot30 and int(sp.totient(h)) == rankE8 == 8
          and h == 2 * N_fam * g_car and exp_mod6 == [1, 5] and deg_mod6 == [0, 2])

    # 2. the 6k family is 6 x the spine {2,3,4,5}
    fam0 = sorted(d for d in deg if d % 6 == 0)        # 12,18,24,30
    a = (1, 1, 2)
    e1 = a[0] + a[1] + a[2]                             # 4
    e2 = a[0]*a[1] + a[0]*a[2] + a[1]*a[2]              # 5
    e3 = a[0]*a[1]*a[2]                                 # 2
    p0 = 3                                              # p0(a) = N_fam
    spine = sorted({e1, e2, e3, p0})                   # {2,3,4,5}
    check("6k FAMILY = 6 x SPINE [I]: degrees==0 mod 6 = {12,18,24,30}; /6 = "
          "{2,3,4,5} = the v91 spine {e3,p0,e1,e2}(a=(1,1,2)); 30=6*g_car is the "
          "matched Coxeter readout, 12,18,24 were 'unmapped'",
          fam0 == [12, 18, 24, 30] and sorted(d // 6 for d in fam0) == spine
          and spine == [2, 3, 4, 5] and (e1, e2, e3, p0) == (4, 5, 2, 3))

    # 3. the 6k+2 family is {2} U the flavor det-ladder {det R, det C, det L}
    fam2 = sorted(d for d in deg if d % 6 == 2)        # 2,8,14,20
    C = R + Q * sp.diag(1, 0, 0)                        # center M(1,0), v135
    L = R + Q * sp.diag(2, 0, 0)                        # M(2,0)
    ladder = [int(R.det()), int(C.det()), int(L.det())]   # 8,14,20
    surf = [6 * s + 8 for s in (0, 1, 2)]              # winding line det M(s,0)
    check("6k+2 FAMILY = QUADRATIC(2) U DET-LADDER [I]: degrees==2 mod 6 = "
          "{2,8,14,20}; {8,14,20} = (det R, det C, det L) = the winding line "
          "det M(s,0)=6s+8 of the flavor diamond (v135), C=R+Q diag(1,0,0); "
          "2 = the matched quadratic/metric Casimir (8=det R also = rank E8)",
          fam2 == [2, 8, 14, 20] and ladder == [8, 14, 20] == surf
          and ladder[0] == rankE8)

    # 4. '18' is not a holdout
    check("'18' IS NOT A HOLDOUT [E]: 18 = 6*3 = 6*N_fam is the spine-family "
          "member 6*p0, NOT on the det-ladder (6s+8=18 has no integer s); it "
          "changes FAMILY, not status -- no genuinely orphan degree remains",
          18 == 6 * N_fam and 18 in fam0 and (18 - 8) % 6 != 0)

    # 5. special to E8 among the simply-laced exceptionals
    def clean(name):
        ex, hh = EXPONENTS[name], COXETER[name]
        is_tot = sorted(ex) == [k for k in range(1, hh) if sp.gcd(k, hh) == 1]
        dm = {(e + 1) % 6 for e in ex}
        return is_tot and dm <= {0, 2} and hh % 6 == 0
    e8_clean = clean("E8")
    e67_fail = (not clean("E6")) and (not clean("E7")) and (not clean("D5"))
    check("SPECIAL TO E8 [E]: the clean {0,2}-mod-6 split (6|h AND "
          "exponents=totatives(h)) holds for E8 but FAILS for E6, E7, D5 -- so "
          "the decomposition is not a generic mod-6 triviality; F4/G2 share the "
          "split but not the spine+flavor-det content",
          e8_clean and e67_fail and clean("F4") and clean("G2"))

    # 6. the reclassification: every 'unmapped' degree has a forced FAMILY home;
    #    honest v355 line -- functorial flavor identification stays [P]
    homed = all((d % 6 == 0 and d // 6 in spine) or (d % 6 == 2 and d in ladder)
                for d in unmapped)
    multiplicity = {12: 2, 24: 2}   # 6*spine vs |R(A3)|=12 / |W(A3)|=24
    check("RECLASSIFIES v354 OVERHEAD, v355 LINE UPHELD [P]: all five 'unmapped' "
          "degrees {12,14,18,20,24} have a forced FAMILY home (6*spine for "
          "{12,18,24}, det-ladder for {14,20}); the set identity degrees = "
          "6*spine U ({2} U det-ladder) is exact [I]. HONEST: the FUNCTORIAL "
          "claim '6k+2 Casimir stratum = flavor sheet operators' needs a "
          "rep-theoretic map ([P]); 12,24 admit 2 canonical readings each, so "
          "this is a STRUCTURE theorem, not a forced functorial flavor map; "
          "closes no gate",
          homed and set(unmapped) == {12, 14, 18, 20, 24}
          and all(v >= 2 for v in multiplicity.values()))

    return summary("v431 E8.DEGREE.LADDER.01: the reverse-audit 'unmapped' E8 "
                   "Casimir degrees are the forced two-family decomposition "
                   "degrees = 6*spine{2,3,4,5} U ({2} U det-ladder{8,14,20}), the "
                   "{0,2}-mod-6 classes forced by h=30=2*3*5; reclassifies v354/"
                   "v355 overhead to zero orphan degrees, the functorial flavor "
                   "map honestly kept [P]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
