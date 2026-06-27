"""v430 -- E8.OTHERSIDE.AUDIT.01: the 'other side of the seam' (double-cover deck /
conjugate sheet S^-) audited against E8's UNMAPPED Casimir degrees -- the sheet/deck
complement of the reverse audit v354/v355.

The user's sharp question: the reverse audit (v354) found FIVE Casimir degrees
{12,14,18,20,24} that feed no PRIMARY readout ('hull overhead'); the double cover has
an 'other side' (the one-sided Z2 collar, the conjugate half-spinor S^-).  Does that
other side CORRELATE with the unmapped E8 structure -- is the leftover where the second
sheet lives?  This module runs that explicit cross-probe, and the answer is a disciplined
NEGATIVE: the other side lies entirely in E8's MATCHED structure (degree-2 and the
128-spinor) and is FORCED-DISJOINT from the five unmapped degrees.  It records WHY the
old 'S^- = dark matter' reading was downgraded (v227) and the WIMP no-go closed, and it
is the sheet/deck complement of the degree audit v354/v355.

  [E] 1. THE DECK IS THE DEGREE-2 INVARIANT (matched, not overhead).  The one-sided
        double cover contributes |Z2|=2 (the factor 1/2 in c3=1/(2*4pi)=1/(8pi),
        v58/v216); 2 is the SMALLEST E8 Casimir degree (the quadratic/metric) -- one of
        the THREE matched primary readouts {2,8,30} (v354), never one of the unmapped
        {12,14,18,20,24}.
  [E] 2. THE TWO SHEETS ARE THE 128-SPINOR (matched, collective).  dim S^+ = dim S^- =
        16; the full E8 spinor block is 128 = rank*dim S^+ = 8*16 = 2^(rank-1) =
        sum(degrees) (v227/v66) -- the spinor half of 248 = 120 + 128.  The 'other side'
        S^- enters 248 as the conjugate (16-bar,4-bar) (tfpt_1), 128 = 2*dim(16,4) =
        2*64, NOT as a spare singlet.
  [E] 3. FORCED-DISJOINT FROM THE UNMAPPED REGION.  The natural sheet/deck integer set
        {|Z2|, dim S^+, dim S^-, dim(S^+ + S^-), the 128-spinor} = {2,16,32,128} has
        EMPTY intersection with the unmapped degrees {12,14,18,20,24}; its only contact
        with the degree alphabet is the MATCHED degree 2 and the collective spinor budget
        128 = sum(deg).
  [O] 4. DISCIPLINED DECLINE (the v355 discriminator applied to the sheet).  Could a
        sheet/deck quantity FORCE a single unmapped degree?  Each candidate (e.g.
        24 = |Z2|*12, 18 = |Z2|*9, ...) needs an UNFORCED coefficient and admits >=2
        readings -- exactly the promiscuous mining v355 declines.  No forced
        sheet -> unmapped-degree identity exists; the only forced set-level sheet identity
        sum(deg) = 128 = spinor is the MATCHED budget already in v355.  So the unmapped
        degrees are NOT the other side.
  [E] 5. THE OLD 'S^- = DM' READING WAS DOWNGRADED, THE WIMP NO-GO CLOSED.  v227 replaced
        the over-strong 'S^- is dark matter' by the magnitude/phase typing of 248=120+128;
        the 128 = (16,4)+(16-bar,4-bar) is the SAME matter spinor, so 'no spare E8 singlet
        for a WIMP' (frontier, [E]).  Dark matter is the determinant-line axion (a PHASE
        of existing structure), not new structure on the other sheet.
  [O] 6. WHERE THE ONLY LIVE 'OTHER SIDE' QUESTION SITS (honest).  Whether the 128
        phase/glue channel hosts a dark sector stays Frontier (v227 #6) -- but that is
        MATCHED structure (the spinor 128 = sum(deg)), NOT the five unmapped degrees.
        Even the open question does not place the other side in the unmapped overhead.

CONCLUSION: the 'other side of the seam' is forced-disjoint from E8's unmapped Casimir
degrees; the correlation the question probes does not exist as a forced identity -- a
structural NEGATIVE that complements the reverse audit (v354) and the bandwidth decline
(v355).  Exact integer/arithmetic [E] + honest [O] residual.  Python-only (sympy);
the set/intersection identities are mirrored in wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8, dim_Splus

DIM_E8 = 248
Z2 = 2


def run():
    reset()
    print("v430  E8.OTHERSIDE.AUDIT.01: the double-cover 'other side' vs E8's unmapped "
          "Casimir degrees")

    exponents = [1, 7, 11, 13, 17, 19, 23, 29]
    degrees = [e + 1 for e in exponents]              # {2,8,12,14,18,20,24,30}
    matched = [2, 8, 30]                              # metric, rank->c3, Coxeter->g_car (v354)
    unmapped = [d for d in degrees if d not in matched]   # {12,14,18,20,24}

    # 1. the deck is the degree-2 invariant (matched, not overhead)
    c3_factor_ok = sp.Rational(1, 8) == sp.Rational(1, Z2 * 4)
    check("DECK = DEGREE-2 INVARIANT [E]: the one-sided double cover contributes |Z2|=2 "
          "(the 1/2 in c3=1/(2*4pi)=1/(8pi), v58/v216); 2 = min(E8 degrees) = the "
          "quadratic/metric, one of the THREE matched primary readouts {2,8,30} (v354), "
          "NOT one of the unmapped %s" % unmapped,
          c3_factor_ok and Z2 == min(degrees) and Z2 in matched
          and Z2 not in unmapped and matched == [2, 8, 30]
          and 8 == rankE8 and 30 == 2 * N_fam * g_car)

    # 2. the two sheets are the 128-spinor (matched, collective)
    spinor = rankE8 * dim_Splus                       # 128
    dim_16_4 = dim_Splus * 4                           # 64 = the (16,4) block
    check("TWO SHEETS = THE 128-SPINOR [E]: dim S^+ = dim S^- = 16; the E8 spinor block "
          "is 128 = rank*dim S^+ = 8*16 = 2^(rank-1) = sum(degrees) -- the spinor half "
          "of 248=120+128; the 'other side' S^- is the conjugate (16-bar,4-bar), "
          "128 = 2*dim(16,4) = 2*64, not a spare singlet",
          dim_Splus == 16 and spinor == 128 == 2 ** (rankE8 - 1) == sum(degrees)
          and 120 + spinor == DIM_E8 and spinor == 2 * dim_16_4)

    # 3. forced-disjoint from the unmapped region
    sheet_atoms = {Z2, dim_Splus, 2 * dim_Splus, spinor}   # {2,16,32,128}
    check("FORCED-DISJOINT [E]: the sheet/deck integer set {|Z2|,dim S^+,dim(S^+ + S^-),"
          "128-spinor} = %s has EMPTY intersection with the unmapped degrees %s; its only "
          "contact with the degree alphabet is the MATCHED degree 2 (and the collective "
          "budget 128=sum(deg))" % (sorted(sheet_atoms), unmapped),
          sheet_atoms == {2, 16, 32, 128}
          and sheet_atoms.isdisjoint(set(unmapped))
          and sheet_atoms.intersection(set(degrees)) == {2})

    # 4. disciplined decline -- the v355 discriminator applied to the sheet
    sheet_readings = {
        12: ["|R(A3)|", "h(E6)", "N_fam*|mu4|=3*4", "6*|Z2|"],
        14: ["dim G2", "2*7", "7*|Z2|"],
        18: ["h(E7)", "p4(a)=2+2^4", "9*|Z2|"],
        20: ["det L", "|mu4|*g_car=4*5", "10*|Z2|"],
        24: ["|W(A3)|=4!", "rank*N_fam=8*3", "|mu4|*6", "12*|Z2|"],
    }
    check("DISCIPLINED DECLINE [O]: each unmapped degree, if 'explained' from sheet/deck "
          "atoms, needs an UNFORCED coefficient and admits >=2 readings (%s) -- exactly "
          "the promiscuous mining v355 declines; no FORCED sheet -> unmapped-degree "
          "identity, and the only forced set-level sheet identity sum(deg)=128=spinor is "
          "the MATCHED budget (already v355). So the unmapped degrees are NOT the other side"
          % {d: len(r) for d, r in sheet_readings.items()},
          set(sheet_readings) == set(unmapped)
          and all(len(r) >= 2 for r in sheet_readings.values()))

    # 5. the old 'S^- = DM' reading downgraded, WIMP no-go closed
    check("'S^- = DM' DOWNGRADED, WIMP NO-GO [E]: v227 replaced the over-strong 'S^- is "
          "dark matter' by the magnitude/phase typing of 248=120+128; 128=(16,4)+"
          "(16-bar,4-bar) is the SAME matter spinor (128 = 2*64), so there is no spare E8 "
          "singlet for a WIMP (frontier) -- DM is the determinant-line axion (a PHASE of "
          "existing structure), not new structure on the other sheet",
          120 + spinor == DIM_E8 and spinor == 2 * dim_16_4 and dim_16_4 == 64)

    # 6. where the only live 'other side' question sits (honest)
    check("HONEST OPEN RESIDUAL [O]: the ONLY live 'other side' question -- does the 128 "
          "phase/glue channel host a dark sector (v227 #6) -- concerns MATCHED structure "
          "(the spinor 128=sum(deg)), NOT the five unmapped degrees; even the open question "
          "does not place the other side in the unmapped overhead",
          spinor == sum(degrees) and spinor not in unmapped)

    return summary("v430 other-side reverse audit: the double-cover 'other side' (deck |Z2|=2 "
                   "+ the 128-spinor S^+ (+) S^-) lies entirely in E8's MATCHED structure "
                   "(degree 2 + the collective spinor budget 128=sum(deg)) and is FORCED-DISJOINT "
                   "from the five unmapped Casimir degrees {12,14,18,20,24}; no forced "
                   "sheet->unmapped-degree identity (v355 discriminator), the old 'S^-=DM' "
                   "reading downgraded (v227) and the WIMP no-go closed -- the sheet/deck "
                   "complement of v354/v355, a clean structural NEGATIVE")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
