/*
 * TFPT MACHINE — grounded data layer (v3: seam-as-source + recursion + plain language).
 *
 * Every number is taken from the TFPT repo (verification/tfpt_constants.py,
 * origin_theory.tex, website/lib/predictions.ts, the v62 scorecard / v307 watchdog).
 * Nothing is invented. Exposed as `TFPT_DATA`.
 *
 * Each station carries BOTH a plain-language label (`plain` + `sub`) for non-experts
 * and the technical name/formula (`title` + `tech`). `match` on the cards is the
 * confrontation with current data: green (≲1σ) / orange (~1–3σ) / red (excluded) /
 * slate (not yet decisive).
 */
(function () {
  "use strict";
  const PI = Math.PI;
  const c3 = 1 / (8 * PI);
  const g_car = 5;
  const phibase = 1 / (6 * PI);
  const dtop = 48 * Math.pow(c3, 4);
  const phi0 = phibase + dtop;

  // ===================== the machine graph =====================
  // x,y are fractions of the canvas. kinds: source | input | build | auditor |
  // stage | gear | assembler | output.
  const stations = [
    // ----- SYNTAX belt (the discrete compiler) -----
    { id: "seam", kind: "source", x: 0.045, y: 0.24, accent: "#a78bfa", icon: "\u25c8", belt: "syntax",
      plain: "THE SOURCE", sub: "the edge of reality — 4 marks",
      title: "The boundary seam", tech: "\u2119\u00b9 \\ \u03bc\u2084 = {1, i, \u22121, \u2212i}",
      atoms: ["four marks (\u03bc\u2084)", "the order-4 clock z \u21a6 i z", "one-sided Gauss\u2013Bonnet \u21d2 8\u03c0"],
      detail: "Everything starts from ONE object: a boundary with exactly four marks. The one-sided Gauss\u2013Bonnet of its normal S\u00b2 slice gives 8\u03c0 \u2014 i.e. the tempo c\u2083 = 1/(8\u03c0). The two 'axioms' are two readings of this one edge." },

    { id: "c3", kind: "input", x: 0.155, y: 0.10, accent: "#3fd0e0", icon: "\u23f1", belt: "syntax",
      plain: "TEMPO  c\u2083", sub: "Gauss\u2013Bonnet: 8\u03c0 = |\u2124\u2082|\u00b72\u03c0\u03c7(S\u00b2)",
      title: "Axiom P1 — seam constant", tech: "c\u2083 = 1/(8\u03c0) \u2248 0.0398",
      atoms: ["the boundary clock-rate", "8 = one-sided Gauss\u2013Bonnet = rank E\u2088 = \u03c6(30)", "read off the seam geometry"],
      detail: "The tempo c\u2083 = 1/(8\u03c0). The 8 is the one-sided Gauss\u2013Bonnet of the seam's normal S\u00b2 slice (|\u2124\u2082|\u00b72\u03c0\u03c7 = 8\u03c0) \u2014 and equals rank E\u2088, which the auditor forces. The only number with no cheaper origin is \u03c0." },
    { id: "gcar", kind: "input", x: 0.155, y: 0.30, accent: "#f0b429", icon: "\u25a4", belt: "syntax",
      plain: "WIDTH  g_car", sub: "5 slots (Pascal-forced)",
      title: "Axiom P2 — carrier rank", tech: "g_car = 5  (3 + 2)",
      atoms: ["the half-spinor slot count", "Pascal: 2\u1d4d = g\u00b2+g+2 \u21d2 g=5", "read off the seam carrier"],
      detail: "The width: 5 slots. The auditor forces g_car = 5 three independent ways (the bootstrap \u03bc\u00b2\u22125\u03bc+4=0, the Pascal closure 2\u1d4d=g\u00b2+g+2, the anchor data). Not a free dial." },

    { id: "families", kind: "build", x: 0.285, y: 0.10, accent: "#5b8cff", icon: "\u2462", belt: "syntax",
      plain: "3 FAMILIES (A\u2083)", sub: "loops around the marks",
      title: "Cycle side \u2192 A\u2083", tech: "rank H\u2081(\u2119\u00b9\\\u03bc\u2084) = 3 = N_fam",
      atoms: ["three generations (A\u2083)", "cusp weights {0, 1/3, 2/3}", "the \u03bc\u2083 family clock"],
      detail: "Counting the loops around the four marks gives exactly 3 \u2014 why matter comes in three generations. Not assumed: it's the topology of the edge." },
    { id: "carrier", kind: "build", x: 0.285, y: 0.30, accent: "#34d39a", icon: "\u25c6", belt: "syntax",
      plain: "CARRIER 16 (D\u2085)", sub: "one full particle set",
      title: "Function side \u2192 D\u2085", tech: "\u039b^even(\u2102\u2075) = 1+10+5 = 16",
      atoms: ["h\u2070 = 5 = g_car (Riemann\u2013Roch)", "16 = the SO(10) half-spinor", "= one anomaly-free generation"],
      detail: "The function reading gives a 16-piece building block \u2014 EXACTLY one complete generation of Standard-Model particles (all quarks and leptons, plus a right-handed neutrino)." },

    { id: "hypercharge", kind: "factory", x: 0.41, y: 0.10, accent: "#5b8cff", icon: "\u2295", belt: "syntax",
      plain: "HYPERCHARGE FACTORY", sub: "makes b\u2081 = 41/10 and \u03a9_adm = 48",
      title: "Hypercharge factory", tech: "y\u208b = \u22121/3, y\u208a = 1/2, b\u2081 = 41/10",
      atoms: ["y\u208b = \u22121/3,  y\u208a = 1/2", "\u03a9_adm = 48", "b\u2081 = 41/10 (budget 41 = 10 b\u2081)"],
      detail: "Out of the carrier's 16 the hypercharges fall out (y\u208b = \u22121/3, y\u208a = 1/2), giving the admissible occupancy \u03a9_adm = 48 and the abelian slope b\u2081 = 41/10 \u2014 the budget 41 the \u03b1 engine needs." },
    { id: "gate", kind: "gate", x: 0.41, y: 0.30, accent: "#fb7185", icon: "\u229e", belt: "syntax",
      plain: "GLUE GATE \u27e8CLACK\u27e9", sub: "the two discs must add to 2",
      title: "Glue gate", tech: "q(D\u2085) + q(A\u2083) = 5/4 + 3/4 = 2",
      atoms: ["disc(D\u2085) = disc(A\u2083) = \u2124\u2084", "glue index |\u03bc\u2084| = 4", "5/4 + 3/4 = 2 = E\u2088 root norm"],
      detail: "The two glue discriminants are both \u2124\u2084; their norms q(D\u2085) = 5/4 and q(A\u2083) = 3/4 sum to exactly 2 (the E\u2088 root norm). When they match, the lattice latches \u2014 CLACK \u2014 and only then can E\u2088 form." },

    { id: "glue", kind: "auditor", x: 0.565, y: 0.20, accent: "#fb7185", icon: "\u2713", belt: "syntax",
      plain: "THE AUDITOR", sub: "the rulebook — fits only ONE way",
      title: "E\u2088 audit core / type-check", tech: "D\u2085 \u2295 A\u2083 + \u03bc\u2084 \u21d2 E\u2088, det = 1",
      atoms: ["the unique \u03bc\u2084 closure", "248 = 240 + 8", "validates 7 routes, pins g_car=5 and the 8 in c\u2083"],
      detail: "E\u2088 is the auditor (not a gauge group, not the world): the one rulebook in which the pieces lock together as an even-unimodular object (det = 1) \u2014 and only for ONE tempo and width. So E\u2088 doesn't just accept the inputs, it PINS them. That is the recursion: the 'axioms' are outputs of the audit." },

    { id: "skeleton", kind: "rom", x: 0.725, y: 0.10, accent: "#5b8cff", icon: "\u25a5", belt: "syntax",
      plain: "ANCHOR ROM", sub: "hard-wired genome a = (1,1,2)",
      title: "Anchor microcode", tech: "a=(1,1,2) \u2192 e=(4,5,2), p=(4,6,10)",
      atoms: ["a = (1,1,2) \u2192 e = (4,5,2)", "power sums p = 4, 6, 10", "reads off 240, 248, 30, 41"],
      detail: "The anchor a = (1,1,2) is the machine's ROM chip: its symmetric data e = (4,5,2) = (|\u03bc\u2084|, g_car, |\u2124\u2082|) and power sums p = (4,6,10) read off 240 roots, 248 = dim E\u2088, 30 = h(E\u2088) and the budget 41 \u2014 all hard-wired." },
    { id: "flavor", kind: "engine", x: 0.725, y: 0.30, accent: "#34d39a", icon: "\u25eb", belt: "syntax",
      plain: "FLAVOR ENGINE", sub: "the residue matrices R, L, K, Q",
      title: "Flavor engine", tech: "det R = 8, \u03c7_R = t\u00b3\u22129t\u00b2+10t\u22128",
      atoms: ["R / L / K / Q + Sheet Diamond", "det R = 8 = h(D\u2085), minors (2,3,5)", "the \u03c6\u2080-ladder basis"],
      detail: "The flavor operators R, L, K, Q (and the Sheet Diamond) are forged here: det R = 8, principal minors (2,3,5), char-poly t\u00b3\u22129t\u00b2+10t\u22128 \u2014 the Standard-Model flavor structure and the \u03c6\u2080-ladder basis." },

    // ----- DYNAMICS belt (the transport layer) -----
    { id: "clock", kind: "gear", x: 0.50, y: 0.55, accent: "#3fd0e0", icon: "\u2699", belt: "dynamics",
      plain: "TRANSPORT (the clock)", sub: "gapped transport \u2192 ONE attractor (selected, not tuned)",
      title: "The transport / translation clock", tech: "T = {1, (2/3)\u2076, (1/3)\u2076}, gap 6 ln(3/2)",
      atoms: ["static gear 5 = g_car (golden \u221a5)", "dynamic gear 6 = 2N_fam", "T = {1, (2/3)\u2076, (1/3)\u2076}", "gap \u0394 = 6 ln(3/2) > 0", "Perron\u2013Frobenius: ONE fixed point"],
      detail: "The DYNAMICS layer \u2014 distinct from the discrete compiler (top belt) and the physical dressing (bottom belt). Two coprime gears (static 5 = carrier, dynamic 6 = families) make the order-30 transport, spectrum {1, (2/3)\u2076, (1/3)\u2076}, positive gap 6 ln(3/2). By Perron\u2013Frobenius: a UNIQUE attractor \u2014 the constants are SELECTED, not tuned. (v319/v56)" },

    // ----- PHYSICS belt (the dressed observables) -----
    { id: "em", kind: "engine", x: 0.35, y: 0.82, accent: "#5b8cff", icon: "\u26a1", belt: "physics",
      plain: "\u03b1 ENGINE (1/137)", sub: "click for the derivation",
      title: "EM engine", tech: "F_U(1)(\u03b1)=0, budget 41 \u2192 \u03b1\u207b\u00b9 = 137.036",
      atoms: ["41 = 10 b\u2081 (from the factory)", "unique positive root", "matches CODATA to 9 digits"],
      detail: "The electromagnetic coupling \u2014 the famous 1/137 \u2014 is the single solution of one cubic built from the audited numbers (budget 41). Measured to nine digits; nothing tuned. Turn the ablation dials: only (8, 5) lands here." },
    { id: "seed", kind: "decoder", x: 0.51, y: 0.82, accent: "#f0b429", icon: "\u2726", belt: "physics",
      plain: "SEED DECODER  \u03c6\u2080", sub: "one seed \u2192 four observables",
      title: "Retarded-seed decoder", tech: "\u03c6\u2080 = 1/(6\u03c0) + 3/(256\u03c0\u2074)",
      atoms: ["Cabibbo \u03bb_C", "reactor \u03b8\u2081\u2083", "baryon \u03a9_b", "birefringence \u03b2"],
      detail: "The retarded seed \u03c6\u2080 is decoded into four numbers at once: the Cabibbo angle, the reactor angle, the baryon fraction and the cosmic birefringence \u2014 one seed, four cables." },
    { id: "sm", kind: "assembler", x: 0.685, y: 0.82, accent: "#34d39a", icon: "\u269b", belt: "physics",
      plain: "MASS FACTORY", sub: "all the particles on one ladder",
      title: "Standard-Model mass factory", tech: "one \u03c6\u2080-ladder \u2192 9 masses, CKM, PMNS",
      atoms: ["9 fermion masses (one ladder)", "CKM + PMNS mixings", "SU(3)\u00d7SU(2)\u00d7U(1)"],
      detail: "The 16-block \u00d73 with the \u03c6\u2080-ladder and the flavor engine assembles the whole Standard Model: nine fermion masses on one ladder, the CKM and PMNS mixings. See the Standard-Model deck below." },
    { id: "cosmo", kind: "stage", x: 0.84, y: 0.63, accent: "#a78bfa", icon: "\u272a", belt: "physics",
      plain: "GRAVITY \u00b7 QFT \u00b7 COSMOS", sub: "the seam as a horizon \u2014 click",
      title: "Gravity / QFT / horizon", tech: "G_ab + \u039b g_ab = c\u2083\u207b\u00b9 T_ab  (\u03b4S = \u03b4\u27e8K\u27e9)",
      atoms: ["G_ab = c\u2083\u207b\u00b9 T_ab DERIVED from \u03b4S = \u03b4\u27e8K\u27e9 (parameter-free)", "c\u2083 triply over-determined: anchor \u00b7 geometry \u00b7 thermodynamics", "\u039b from \u03b1; R+R\u00b2 scalaron \u2014 full 4D QG measure stays OPEN"],
      detail: "The SAME edge, read as a horizon, gives gravity, an emergent quantum field theory and cosmology. As of the 2026-06 work, Einstein's equation is DERIVED parameter-free from entanglement equilibrium (\u03b4S = \u03b4\u27e8K\u27e9): G_ab + \u039b g_ab = c\u2083\u207b\u00b9 T_ab with 8\u03c0 = 1/c\u2083 (v358/v359) and \u039b from \u03b1 (v60). The spectral action adds R+R\u00b2 (the scalaron). The one thing still dimensionful is the single unit v_geo; the full nonperturbative 4D quantum-gravity measure is the honest open frontier." },

    { id: "out", kind: "output", x: 0.93, y: 0.82, accent: "#3fd0e0", icon: "\u25ce", belt: "physics",
      plain: "PREDICTIONS", sub: "23 to measure \u2014 click for the tally",
      title: "The readout board", tech: "23 typed predictions vs current data",
      atoms: ["coloured by data match", "9 match \u00b7 6 near \u00b7 0 miss \u00b7 8 pending", "tally: 0 dimensionless dials + 1 unit (v_geo) + \u03c0"],
      detail: "The machine's output: 23 forward predictions and falsifiers, each coloured by how it stacks up against current data. Click for the full tally \u2014 the whole Standard Model, the constants and the cosmos come from ZERO dimensionless dials, ONE unit (v_geo) and \u03c0." },
  ];

  // forward pipes (drive the flow + the step depth)
  const edges = [
    ["seam", "c3"], ["seam", "gcar"],
    ["c3", "families"], ["seam", "families"], ["gcar", "carrier"], ["seam", "carrier"],
    ["carrier", "hypercharge"],
    ["families", "gate"], ["carrier", "gate"], ["seam", "gate"],
    ["gate", "glue"], ["hypercharge", "glue"],
    ["glue", "skeleton"], ["glue", "flavor"], ["skeleton", "flavor"],
    ["glue", "clock"], ["flavor", "clock"],
    ["hypercharge", "em"], ["skeleton", "em"], ["clock", "em"],
    ["flavor", "seed"], ["clock", "seed"],
    ["flavor", "sm"], ["seed", "sm"], ["clock", "sm"],
    ["em", "cosmo"], ["clock", "cosmo"],
    ["em", "out"], ["sm", "out"], ["cosmo", "out"], ["seed", "out"],
  ];

  // feedback loops (drawn specially, NOT used for depth)
  const feedback = [
    { from: "glue", to: "c3", kind: "bootstrap" },
    { from: "glue", to: "gcar", kind: "bootstrap" },
    { from: "cosmo", to: "seam", kind: "horizon" },
  ];

  const steps = [
    { t: "The Source", d: "It all starts from ONE thing: a boundary \u2014 the edge of reality \u2014 with exactly four marks (\u03bc\u2084)." },
    { t: "Two readouts (not free!)", d: "The edge is read two ways: a tempo c\u2083=1/(8\u03c0) (Gauss\u2013Bonnet) and a width g_car=5. They look like inputs \u2014 step 4 shows they aren't." },
    { t: "Build the pieces", d: "Loops \u2192 3 families (A\u2083); functions \u2192 the 16-piece carrier (D\u2085) = one full particle set." },
    { t: "Hypercharge + glue gate", d: "The factory makes b\u2081 = 41/10; the glue gate checks q(D\u2085)+q(A\u2083) = 5/4+3/4 = 2 \u2014 only then can the lattice latch (CLACK)." },
    { t: "The E\u2088 Audit Core (recursion!)", d: "E\u2088 closes as an even-unimodular object for only ONE (tempo, width) \u2014 so it PINS the 'axioms'. They're forced, not chosen." },
    { t: "Anchor ROM", d: "The anchor a=(1,1,2) reads off the whole integer grid: 240, 248, 30, 41." },
    { t: "Flavor engine", d: "The residue matrices R/L/K/Q (det R = 8) forge the flavor structure and the \u03c6\u2080-ladder basis." },
    { t: "Transport (dynamics)", d: "The gapped transport T = {1,(2/3)\u2076,(1/3)\u2076} has a unique attractor \u2014 the constants are selected, not tuned." },
    { t: "Engines & seed decoder", d: "The \u03b1 engine returns 1/137; the seed \u03c6\u2080 decodes into Cabibbo, reactor, baryon and birefringence." },
    { t: "Standard Model & cosmos", d: "One \u03c6\u2080-ladder builds all nine masses + mixings; the horizon fixes \u039b, the scalaron and inflation." },
    { t: "Predictions", d: "23 testable numbers, coloured by how they match what we've actually measured." },
  ];

  // ===================== Standard-Model deck =====================
  // sec groups the deck by SM sector (gauge / matter / quark mass / lepton mass / mixing / Higgs).
  const sm = [
    // --- forces & gauge structure ---
    { sym: "SU(3)\u00d7SU(2)\u00d7U(1)", title: "The forces (gauge group)", tfpt: "from the 16-block", measured: "the SM forces", match: "green", cat: "Structure", sec: "gauge",
      note: "structural \u2014 the building block carries exactly the Standard-Model forces.",
      detail: "16 = 10 + 5\u0304 + 1 under SU(5) \u2282 SO(10) is one anomaly-free generation; the gauge group is the SM one. Structural, not a fit." },
    { sym: "b\u2081 = 41/10", title: "Hypercharge slope", tfpt: "41/10", measured: "41/10 (SM)", match: "green", cat: "Forces", sec: "gauge",
      note: "matches the SM one-loop U(1) running exactly.",
      detail: "The budget 41 = 10 b\u2081 also fixes the 1/137 constant; a fourth family would shift it." },
    { sym: "sin\u00b2\u03b8_W", title: "Weinberg angle (high scale)", tfpt: "3/8 (bare)", measured: "0.23122 (M_Z)", match: "red", cat: "Forces", sec: "gauge",
      note: "NO clean match: 3/8 is the bare GUT value; with SM content it does NOT run down to 0.231 \u2014 the known NCG/GUT tension (v246).",
      detail: "The spectral-action boundary condition sin\u00b2\u03b8_W = 3/8 is not met by the SM run \u2014 an honest open tension, not a closure." },
    // --- matter content ---
    { sym: "3 families", title: "Three generations", tfpt: "3", measured: "3 (no 4th seen)", match: "green", cat: "Structure", sec: "matter",
      note: "matches \u2014 the loop count of the 4-marked edge; no fourth family observed.",
      detail: "N_fam = rank A\u2083 = dim H\u2081(\u2119\u00b9\\\u03bc\u2084) = 3. A fourth chiral generation would break the lattice closure." },
    { sym: "one generation", title: "= the building block (16)", tfpt: "16 = 10+5\u0304+1", measured: "15 SM + \u03bd_R", match: "green", cat: "Structure", sec: "matter",
      note: "matches \u2014 the 16-block is exactly one anomaly-free generation.",
      detail: "Q, u\u1d9c, d\u1d9c, L, e\u1d9c, \u03bd\u1d9c \u2014 16 Weyl states, gauge-anomaly-free (\u03a3Y = \u03a3Y\u00b3 = 0)." },
    // --- quark masses (Yukawa ladder) ---
    { sym: "t, c, u", title: "Up-type quark masses", tfpt: "172.7 / 1.27 / 0.0022 GeV", measured: "172.7 / 1.27 / 0.0022 GeV (PDG)", match: "green", cat: "Masses", sec: "qmass",
      note: "t,c,u sit on one \u03c6\u2080-ladder (word-lengths L = 0,2,4); the RATIOS are the closed prediction and the overall scale is the single anchor v_geo \u2014 so the absolute masses are reproduced, not independently fit.",
      detail: "The nine charged-fermion masses sit on one \u03c6\u2080-ladder; ratios are closed (Pl\u00fccker), the scale is the single anchor v_geo." },
    { sym: "b, s, d", title: "Down-type quark masses", tfpt: "4.18 / 0.093 / 0.0047 GeV", measured: "4.18 / 0.093 / 0.0047 GeV (PDG)", match: "green", cat: "Masses", sec: "qmass",
      note: "b,s,d on the same \u03c6\u2080-ladder (L = 2,3,4); ratios closed, the absolute scale anchored to v_geo.",
      detail: "Down-type word lengths on the \u03c6\u2080-ladder; the quark ratios are exact integer readouts." },
    { sym: "quark ratios", title: "Quark mass ratios", tfpt: "m_c/m_s \u2248 13.6,  m_t/m_b \u2248 41", measured: "13.7,  41.3 (PDG)", match: "green", cat: "Masses", sec: "qmass",
      note: "the coefficient ratios c_u/c_d=55/117, c_c/c_s=34/47, c_t/c_b=3/26 times \u03c6\u2080-powers give the measured quark mass ratios \u2014 exact integer readouts, no flavor fit.",
      detail: "mass ratio = c-ratio \u00d7 \u03c6\u2080^\u0394k: (34/47)/\u03c6\u2080 = 13.6 = m_c/m_s, (3/26)/\u03c6\u2080\u00b2 = 40.8 = m_t/m_b. Stratum-constant Readout Rigidity." },
    // --- lepton masses & Koide ---
    { sym: "e, \u03bc, \u03c4", title: "Charged-lepton masses", tfpt: "1.7769 / 0.10566 / 0.000511 GeV", measured: "1.7769 / 0.10566 / 0.000511 GeV (PDG)", match: "green", cat: "Masses", sec: "lmass",
      note: "the \u03c4,\u03bc,e amplitudes are the exact rationals (16/7, 4/3, 7/6), product 32/9; Koide Q \u2248 0.666. Masses reproduced on the ladder, scale anchored.",
      detail: "The lepton amplitudes are exact \u03b4=1/2 resolvent values; product 2^g_car/N_fam\u00b2 = 32/9." },
    { sym: "Q_Koide", title: "Koide lepton relation", tfpt: "0.664 \u2192 2/3", measured: "0.66666", match: "orange", cat: "Masses", sec: "lmass",
      note: "near \u2014 source level 0.33% below the target 2/3.",
      detail: "The transfer to the exact 2/3 attractor is conjectural; a near-miss." },
    // --- mixing angles & CP phases ---
    { sym: "\u03bb_C", title: "Cabibbo angle (quark mixing)", tfpt: "0.22438", measured: "0.2245 \u00b1 0.0007", match: "green", cat: "Mixing", sec: "mixing",
      note: "\u2248 0.9\u03c3.",
      detail: "\u03bb_C = \u221a(\u03c6\u2080(1\u2212\u03c6\u2080)); the same seed \u03c6\u2080 as the reactor angle and birefringence." },
    { sym: "sin\u00b2\u03b8\u2081\u2082", title: "Solar neutrino angle", tfpt: "0.30675", measured: "0.307 \u00b1 0.012", match: "green", cat: "Mixing", sec: "mixing",
      note: "0.02\u03c3 \u2014 the sharpest hit.",
      detail: "1/3 minus the seam misalignment: sin\u00b2\u03b8\u2081\u2082 = 1/3 \u2212 \u03c6\u2080/2 = 0.306747 (prediction of record)." },
    { sym: "sin\u00b2\u03b8\u2081\u2083", title: "Reactor neutrino angle", tfpt: "0.0231", measured: "0.02195 \u00b1 0.00058", match: "orange", cat: "Mixing", sec: "mixing",
      note: "~2.0\u03c3 mild tension.",
      detail: "sin\u00b2\u03b8\u2081\u2083 = \u03c6\u2080 e^{\u22125/6}; the most-tensioned core prediction." },
    { sym: "sin\u00b2\u03b8\u2082\u2083", title: "Atmospheric angle", tfpt: "\u2248 1/2", measured: "octant unknown", match: "slate", cat: "Mixing", sec: "mixing",
      note: "near-maximal; octant not yet picked.",
      detail: "\u03bc\u03c4-symmetric limit 45\u00b0; NOvA/T2K/DUNE address the octant." },
    { sym: "\u03b4_CKM", title: "Quark CP phase", tfpt: "\u2248 69\u00b0", measured: "65.7\u00b0 (LHCb)", match: "orange", cat: "Mixing", sec: "mixing",
      note: "+1.45\u03c3 \u2014 a live tension feeding rare-kaon decays.",
      detail: "Leading term \u03c0/3, the hexagonal Eisenstein phase." },
    { sym: "\u03b4_PMNS", title: "Neutrino CP phase", tfpt: "240\u00b0", measured: "212\u00b0\u207a\u00b2\u2076\u208b\u2084\u2081", match: "orange", cat: "Mixing", sec: "mixing",
      note: "+1.08\u03c3 \u2014 locked to the quark phase (\u03b4_CKM + 180\u00b0); decisive at DUNE.",
      detail: "\u03b4_PMNS = 4\u03c0/3, the sheet flip of \u03b4_CKM \u2014 the two CP phases are not independent (v320)." },
    // --- Higgs & strong-CP ---
    { sym: "N_\u03a6 = 1", title: "Exactly one Higgs", tfpt: "1", measured: "1 (no 2nd)", match: "green", cat: "Structure", sec: "higgs",
      note: "matches \u2014 N_\u03a6 = g_car \u2212 |\u03bc\u2084| = 1, a structural ban.",
      detail: "The carrier index fixes exactly one weak doublet; the Higgs sits near criticality." },
    { sym: "\u03b8_eff = 0", title: "Strong-CP / neutron EDM", tfpt: "0", measured: "no EDM signal", match: "green", cat: "Structure", sec: "higgs",
      note: "matches \u2014 a topological null; PSI nEDM consistent.",
      detail: "\u03b8_eff = 0 from \u03b3\u2085-Hermiticity + sheet involution + reflection positivity \u2014 not a fit." },
  ];
  const smGroups = [
    { key: "gauge", label: "Forces & gauge structure", color: "#5b8cff", blurb: "the gauge group, hypercharge slope and Weinberg angle \u2014 straight off the 16-block" },
    { key: "matter", label: "Matter content", color: "#34d39a", blurb: "three generations, each one anomaly-free 16 (16 Weyl states)" },
    { key: "qmass", label: "Quark masses \u2014 the Yukawa ladder", color: "#f0b429", blurb: "all six quark masses on ONE \u03c6\u2080-ladder; ratios exact, the only scale is the anchor v_geo" },
    { key: "lmass", label: "Lepton masses & Koide", color: "#f0b429", blurb: "charged-lepton masses as exact ladder amplitudes; the Koide ratio heads to 2/3" },
    { key: "mixing", label: "Mixing angles & CP phases", color: "#a78bfa", blurb: "CKM + PMNS angles and the two CP phases from the \u03c6\u2080 seed and the residue R" },
    { key: "higgs", label: "Higgs & strong-CP", color: "#3fd0e0", blurb: "exactly one Higgs doublet; the strong-CP angle is a topological null" },
  ];

  // ===================== the 23 predictions =====================
  // horizon: settled | live | soon | next | structural  (drives the "when testable" timeline)
  const predictions = [
    { sym: "\u03b1\u207b\u00b9", title: "Fine-structure constant", tfpt: "137.0359992", measured: "137.035999177 (CODATA)", status: "E", match: "green", cat: "Couplings", stage: "em",
      formula: "unique root of F_U(1)(\u03b1)=0,  41 = 10 b\u2081", note: "matches to ~9 figures (1.9\u03c3 on the last digits).",
      kill: "a second admissible root, or a stable mismatch beyond the interface uncertainty.",
      detail: "Existence and uniqueness of the positive root are proved; lands 2.9\u00d710\u207b\u00b9\u2070 from CODATA-2022.",
      horizon: "settled", when: "Already pinned to 9 digits (CODATA 2022). Confirmed \u2014 only a stable interface-level mismatch could break it." },
    { sym: "\u03bb_C", title: "Cabibbo angle", tfpt: "0.22438", measured: "0.2245 \u00b1 0.0007 (PDG)", status: "E", match: "green", cat: "Flavor", stage: "sm",
      formula: "\u03bb_C = \u221a(\u03c6\u2080(1\u2212\u03c6\u2080))", note: "~0.9\u03c3.",
      kill: "stable CKM global-fit mismatch after the declared comparison map.",
      detail: "The carrier base of the \u03c6\u2080-ladder \u2014 the same seed as \u03b8\u2081\u2083 and birefringence.",
      horizon: "settled", when: "Matches the PDG CKM fit (~0.9\u03c3) today; tightens further with Belle II / LHCb." },
    { sym: "det R", title: "Flavor residue invariants", tfpt: "8, minors (2,3,5)", measured: "structural", status: "E", match: "slate", cat: "Flavor", stage: "sm",
      formula: "det R = 8 = h(D\u2085),  \u03c7_R = t\u00b3\u22129t\u00b2+10t\u22128", note: "structural identity \u2014 a constraint any fit must satisfy, not a single datum.",
      kill: "a CKM/PMNS fit not carriable by a det-8 residue matrix with minors (2,3,5).",
      detail: "The flavor matrix carries only compiler numbers; \u2016R\u2016\u00b2 = 78 = dim E\u2086.",
      horizon: "structural", when: "A structural identity any flavor fit must already satisfy \u2014 not a single dated measurement." },
    { sym: "Q", title: "Koide relation", tfpt: "0.664 \u2192 2/3", measured: "0.66666 (leptons)", status: "C", match: "orange", cat: "Flavor", stage: "sm",
      formula: "Q\u2605 = |\u2124\u2082|/N_fam = 2/3", note: "0.33% below the target 2/3 (near-miss).",
      kill: "a source\u2192pole transfer landing far from 2/3.",
      detail: "Source-level quotient 0.664; the transfer to the exact 2/3 attractor is conjectural.",
      horizon: "live", when: "The lepton value is already 0.66666; the exact 2/3 transfer stays conjectural (a near-miss, not a dated test)." },
    { sym: "sin\u00b2\u03b8\u2081\u2082", title: "Solar angle", tfpt: "0.306747", measured: "0.307 \u00b1 0.012 (NuFIT)", status: "E", match: "green", cat: "Neutrino", stage: "sm",
      formula: "sin\u00b2\u03b8\u2081\u2082 = 1/3 \u2212 \u03c6\u2080/2", note: "0.02\u03c3 vs NuFIT, \u22120.28\u03c3 vs JUNO \u2014 the sharpest hit.",
      kill: "a JUNO central value clearly away from 0.307 at high significance.",
      detail: "Tri-bimaximal 1/3 minus the seam misalignment; the frozen prediction of record.",
      horizon: "soon", when: "JUNO precision result (~2026\u20132028) is decisive; matches NuFIT today (0.02\u03c3)." },
    { sym: "sin\u00b2\u03b8\u2081\u2083", title: "Reactor angle", tfpt: "0.0231", measured: "0.02195 \u00b1 0.00058 (NuFIT)", status: "E", match: "orange", cat: "Neutrino", stage: "sm",
      formula: "sin\u00b2\u03b8\u2081\u2083 = \u03c6\u2080 e^{\u22125/6}", note: "~2.0\u03c3 \u2014 the most-tensioned core prediction.",
      kill: "robust normal-ordering global-fit exclusion.",
      detail: "The seed times the carrier-trace factor e^{\u22125/6} (\u03b3 = 5/6 = tr_E Y\u00b2).",
      horizon: "live", when: "~2\u03c3 now vs Daya Bay / RENO global fits \u2014 the most-tensioned core prediction, live." },
    { sym: "sin\u00b2\u03b8\u2082\u2083", title: "Atmospheric angle", tfpt: "\u2248 1/2", measured: "octant ambiguous", status: "C", match: "slate", cat: "Neutrino", stage: "sm",
      formula: "\u03b8\u2082\u2083 = 45\u00b0 (\u03bc\u03c4-symmetric limit)", note: "octant not yet determined.",
      kill: "a robust off-maximal octant determination by NOvA/T2K/DUNE.",
      detail: "Near-maximal; the octant is not selected by the present transport.",
      horizon: "next", when: "Octant from NOvA/T2K now, decisively settled at DUNE / Hyper-K (~2030s)." },
    { sym: "NO, m_\u03b2\u03b2", title: "Mass ordering & m_\u03b2\u03b2", tfpt: "normal, small m_\u03b2\u03b2", measured: "NO preferred (~2.5\u03c3)", status: "C", match: "slate", cat: "Neutrino", stage: "sm",
      formula: "\u03a3m_\u03bd \u2273 0.0586 eV (NO floor)", note: "consistent with NO; not yet decisive.",
      kill: "inverted ordering, a large m_\u03b2\u03b2, or \u03a3m_\u03bd below the NO floor.",
      detail: "Prefers normal ordering with a small effective mass; LEGEND/nEXO/DUNE/KATRIN compare.",
      horizon: "next", when: "Ordering ~2.5\u03c3 now; LEGEND-1000 / nEXO / KATRIN + DUNE through the late 2020s\u20132030s." },
    { sym: "\u03b8_eff", title: "Strong CP / EDM null", tfpt: "0", measured: "no EDM signal", status: "E", match: "green", cat: "QCD/EDM", stage: "sm",
      formula: "arg det M_u = arg det M_d = 0", note: "matches \u2014 no neutron/electron EDM observed.",
      kill: "a solid neutron-EDM signal above SM background.",
      detail: "A topological null theorem (Pfaffian reality in the 16-Majorana CAR model).",
      horizon: "live", when: "Ongoing neutron / electron-EDM nulls (PSI nEDM, ACME) \u2014 any robust signal kills it." },
    { sym: "m_p/m_e", title: "Proton/electron ratio", tfpt: "not forced", measured: "1836.152", status: "O", match: "slate", cat: "QCD/EDM", stage: "sm",
      formula: "QCD confinement / EW Yukawa \u2014 no clean \u03c6\u2080 power", note: "honest non-claim: a cross-sector ratio, not a compiler power.",
      kill: "only fails if mis-asserted as a compiler power.",
      detail: "Computable at scheme level but genuinely not a \u03c6\u2080 power; deliberately not forced.",
      horizon: "structural", when: "Deliberately NOT a compiler prediction \u2014 a cross-sector QCD/EW ratio; only fails if mis-asserted." },
    { sym: "n_s", title: "Scalar tilt (R\u00b2)", tfpt: "0.960\u20130.967", measured: "0.9649 (Planck)", status: "C", match: "orange", cat: "Cosmology", stage: "cosmo",
      formula: "n_s = 1 \u2212 2/N\u2605", note: "match vs Planck, ~2\u03c3 tension vs the DESI-combined value.",
      kill: "a robust n_s \u2265 0.967 kills the scalaron-reheating chain.",
      detail: "From the same R\u00b2 attractor that fixes the scalaron mass; band over N\u2605 \u2208 [50,60].",
      horizon: "live", when: "Matches Planck; ~2\u03c3 vs the DESI-combined value now; CMB-S4 will sharpen it." },
    { sym: "r", title: "Tensor-to-scalar ratio", tfpt: "0.0033\u20130.0048", measured: "< 0.036 (BK18)", status: "C", match: "slate", cat: "Cosmology", stage: "cosmo",
      formula: "r = 12/N\u2605\u00b2", note: "below the current bound \u2014 a clean CMB-S4 target (~2033).",
      kill: "any robust r \u2273 0.01.",
      detail: "The R\u00b2 scalaron tensor ratio; a ~9\u03c3 detection target at CMB-S4.",
      horizon: "next", when: "Below today's bound; CMB-S4 (~2033) is a ~9\u03c3 detection target." },
    { sym: "A_s", title: "Scalar amplitude", tfpt: "2.0\u00d710\u207b\u2079", measured: "2.10\u00d710\u207b\u2079 (Planck)", status: "C", match: "orange", cat: "Cosmology", stage: "cosmo",
      formula: "A_s = N\u2605\u00b2 c\u2083\u2077/(24\u03c0\u00b2)", note: "the slow-reheating point underpredicts A_s; A_s prefers near-instant reheating.",
      kill: "A_s incompatible with the seam-fixed scalaron mass on the R\u00b2 branch.",
      detail: "Parameter-free once the seam fixes the scalaron mass; arbitrates the reheating speed.",
      horizon: "live", when: "Fixed once the seam sets the scalaron mass; Planck data arbitrates the reheating speed now." },
    { sym: "M_scal", title: "Scalaron mass", tfpt: "3.06\u00d710\u00b9\u00b3 GeV", measured: "not measured", status: "E", match: "slate", cat: "Cosmology", stage: "cosmo",
      formula: "(M/M\u0304)\u00b2 = c\u2083\u2077,  7 = \u03a9_adm \u2212 10 b\u2081", note: "lands at the canonical Starobinsky value; not directly measurable.",
      kill: "a scalaron mass incompatible with the seam power c\u2083\u2077.",
      detail: "A former input is now an output, fixed by the seam.",
      horizon: "structural", when: "Not directly measurable (~10\u00b9\u00b3 GeV) \u2014 an internal output fixed by the seam." },
    { sym: "\u03a9_b", title: "Baryon density", tfpt: "0.04894", measured: "0.04930 (Planck)", status: "C", match: "green", cat: "Cosmology", stage: "cosmo",
      formula: "\u03a9_b = (4\u03c0 \u2212 1) \u03b2_rad", note: "0.1\u03c3 (FRB DM(z): 0.0483\u00b10.0072).",
      kill: "robust inconsistency under the declared Planck convention.",
      detail: "Reads off the determinant-line angle \u03b2_rad; \u03a9_b h\u00b2 = 0.0222.",
      horizon: "settled", when: "Matches Planck / FRB DM(z) today (0.1\u03c3). Confirmed." },
    { sym: "\u03b7_B", title: "Baryon asymmetry", tfpt: "6.1\u00d710\u207b\u00b9\u2070", measured: "6.1\u00d710\u207b\u00b9\u2070 (obs)", status: "C", match: "green", cat: "Cosmology", stage: "cosmo",
      formula: "\u03b7_B = 273.9\u00d710\u207b\u00b9\u2070 \u00b7 \u03a9_b h\u00b2", note: "the Boltzmann solve lands 1.07\u00d7 observed (no free dial).",
      kill: "robust exclusion under the declared cosmological pipeline.",
      detail: "Downstream readout; conditional on the leptogenesis coupling mechanism.",
      horizon: "live", when: "Lands 1.07\u00d7 the observed value; conditional on the leptogenesis mechanism." },
    { sym: "H\u2080 ~ \u221a\u039b", title: "One exponential engine", tfpt: "w = \u22121, 1:5:10", measured: "DESI hints w \u2260 \u22121", status: "C", match: "orange", cat: "Cosmology", stage: "cosmo",
      formula: "\u039b \u223c e^{\u22122\u03b1\u207b\u00b9},  v_EW \u223c e^{\u2212\u03b1\u207b\u00b9/5}", note: "DESI hints w \u2260 \u22121 (up to 4.4\u03c3 in one combo); watchdog armed, not triggered.",
      kill: "a robust w \u2260 \u22121 at \u2265 5\u03c3 in a single systematics-controlled combination.",
      detail: "EW scale, \u039b and Hubble are powers of one engine \u2014 the same \u03b1\u207b\u00b9 \u2248 137. The most dangerous front.",
      horizon: "live", when: "DESI hints w\u2260\u22121 (up to 4.4\u03c3 in one combo) \u2014 the most dangerous front; \u22655\u03c3 in a clean combo kills it." },
    { sym: "N_\u03a6 = 1", title: "No second light Higgs", tfpt: "1", measured: "1 (none found)", status: "E", match: "green", cat: "Higgs", stage: "sm",
      formula: "N_\u03a6 = g_car \u2212 |\u03bc\u2084| = 1", note: "matches \u2014 no second light doublet observed.",
      kill: "robust discovery of a second light seam-even Higgs doublet.",
      detail: "The carrier index fixes exactly one weak doublet \u2014 a structural prohibition.",
      horizon: "settled", when: "No second light Higgs at the LHC so far; HL-LHC keeps probing \u2014 confirmed to date." },
    { sym: "\u03b2_rad", title: "Cosmic birefringence", tfpt: "0.2424\u00b0", measured: "0.215\u00b0 \u00b1 0.074\u00b0 (ACT DR6)", status: "E", match: "green", cat: "Astro", stage: "cosmo",
      formula: "\u03b2_rad = \u03c6\u2080/(4\u03c0)", note: "0.37\u03c3.",
      kill: "an externally calibrated \u03b2 = 0 within tight error.",
      detail: "Determinant-line / Chern\u2013Simons response of the seam; the same seed \u03c6\u2080 as the Cabibbo angle.",
      horizon: "live", when: "ACT DR6: 0.215\u00b0\u00b10.074\u00b0 (0.37\u03c3) now; future CMB-polarization calibration is decisive." },
    { sym: "m_a", title: "Axion dark matter", tfpt: "23.8 \u00b5eV", measured: "window open", status: "C", match: "slate", cat: "Astro", stage: "cosmo",
      formula: "f_a = M_scal/128,  \u03b8_i = 3\u03c0/5", note: "spine angle gives \u03a9_a h\u00b2 \u2248 0.125 (robust); the band is not yet excluded.",
      kill: "exclusion of the determinant-line axion window at the coupled sensitivity.",
      detail: "The strong-CP determinant-line axion; a scenario, not a sharp prediction.",
      horizon: "next", when: "Determinant-line window (~24 \u00b5eV); haloscopes (ADMX & friends) scanning through the 2020s\u20132030s." },
    { sym: "BR(K\u2192\u03c0\u03bd\u03bd\u0304)", title: "Rare kaon decays", tfpt: "9.45\u00d710\u207b\u00b9\u00b9", measured: "13.0\u207a\u00b3\u00b7\u00b3\u208b\u2083\u00b7\u2080 (NA62)", status: "C", match: "orange", cat: "Flavor", stage: "sm",
      formula: "closed CKM point + external SD input", note: "BR(K\u207a) within ~1.2\u03c3; \u03b4_CKM ~2\u03c3 \u2014 a live falsifier.",
      kill: "a stable NA62 BR(K\u207a) outside [7,12]\u00d710\u207b\u00b9\u00b9.",
      detail: "The closed CKM point feeds the cleanest FCNC probe; the neutral mode probes \u03b4_CKM.",
      horizon: "live", when: "NA62 K\u207a within ~1.2\u03c3 now (live falsifier); KOTO probes the neutral mode." },
    { sym: "\u03b2_BH", title: "EHT achromatic intercept", tfpt: "16 c\u2083\u2074 = 1/(256\u03c0\u2074)", measured: "data-limited", status: "C", match: "slate", cat: "Astro", stage: "cosmo",
      formula: "\u03b2_BH(r) = 16 c\u2083\u2074 Q_e Q_m / r\u00b2", note: "coupling fixed exactly; the residual nulls are blocked on a GRMHD library.",
      kill: "a residual failing the frequency / 1/r\u00b2 / sign-flip nulls.",
      detail: "The horizon-collar sibling of cosmic birefringence; achromatic, 1/r\u00b2, sign-flipping.",
      horizon: "next", when: "Blocked on a GRMHD library; ngEHT-era polarization imaging is the test." },
    { sym: "N_fam = 3", title: "No fourth generation", tfpt: "3", measured: "3 (none found)", status: "E", match: "green", cat: "Flavor", stage: "glue",
      formula: "N_fam = rank A\u2083 = dim H\u2081(\u2119\u00b9\\\u03bc\u2084) = 3", note: "matches \u2014 no fourth chiral generation observed.",
      kill: "a fourth chiral generation breaks the lattice closure itself.",
      detail: "Three families is structural \u2014 the four-puncture homology, not a fit.",
      horizon: "settled", when: "No fourth chiral generation (LEP / LHC). Confirmed \u2014 and structural." },
  ];
  const predGroups = [
    { key: "Couplings", label: "Gauge couplings", color: "#5b8cff", blurb: "the fine-structure constant straight out of the compiler" },
    { key: "Flavor", label: "Flavor \u2014 quark sector", color: "#f0b429", blurb: "Cabibbo, residue invariants, Koide and the rare-kaon falsifier" },
    { key: "Neutrino", label: "Neutrinos", color: "#a78bfa", blurb: "mixing angles, the ordering and the effective mass" },
    { key: "QCD/EDM", label: "QCD, strong-CP & EDM", color: "#34d39a", blurb: "the strong-CP null and one honest non-claim" },
    { key: "Higgs", label: "Higgs sector", color: "#3fd0e0", blurb: "exactly one light doublet" },
    { key: "Cosmology", label: "Cosmology & gravity", color: "#a78bfa", blurb: "inflation, the scalaron, baryons and the dark-energy engine" },
    { key: "Astro", label: "Astrophysics & late-time", color: "#3fd0e0", blurb: "cosmic birefringence, the axion window and the black-hole collar" },
  ];
  const horizons = {
    settled: { label: "\u2713 already measured", color: "#34d39a" },
    live: { label: "\u25cf live test now", color: "#f59e42" },
    soon: { label: "\u25b7 this decade", color: "#5b8cff" },
    next: { label: "\u25b7 ~2030s", color: "#a78bfa" },
    structural: { label: "\u25c6 structural / not timed", color: "#7c8db0" },
  };

  // ===================== live EM ablation =====================
  function dtop_of(cc) { return 48 * Math.pow(cc, 4); }
  function phiSeam(a, cc) { const x = dtop_of(cc) * Math.exp(-2 * a); return phibase + x * Math.pow(1 - x, -5 / 4); }
  function Fem(a, cc, M) { return Math.pow(a, 3) - 2 * Math.pow(cc, 3) * a * a - (4 / 5) * Math.pow(cc, 6) * M * Math.log(1 / phiSeam(a, cc)); }
  function budgetM(g) { return g * Math.pow(2, g - 2) + 1; }
  function ainv(N, g) {
    const cc = 1 / (N * PI), M = budgetM(g); let a = 0.0073;
    for (let i = 0; i < 200; i++) {
      const f = Fem(a, cc, M), h = 1e-10, df = (Fem(a + h, cc, M) - f) / h;
      if (!isFinite(df) || df === 0) break;
      const an = a - f / df; if (!isFinite(an) || an <= 0) return NaN;
      if (Math.abs(an - a) < 1e-14) { a = an; break; } a = an;
    }
    return 1 / a;
  }

  // N_fam = (2^(g-1)-1)/g must be a whole number; only g=5 gives 3 (Pascal closure)
  function nfamOf(g) { const v = (Math.pow(2, g - 1) - 1) / g; return Number.isInteger(v) ? v : null; }
  // does a candidate universe (tempo N in c3=1/(Nπ), width g) CLOSE?
  // Honest: closes iff g=5 (Pascal/3 families) AND N=8 (rank E8 = 8 = the seam constant).
  function closure(N, g) {
    const nf = nfamOf(g), ai = ainv(N, g);
    const alphaOk = isFinite(ai) && Math.abs(ai - 137.035999) < 0.05;
    const closes = g === 5 && N === 8;
    let reason;
    if (g !== 5) reason = (nf === null)
      ? `width g=${g} fails Pascal 2\u1d4d=g\u00b2+g+2 \u2014 the carrier can't close`
      : `wrong matter: g=${g} \u21d2 ${nf} generation(s), not 3`;
    else if (N !== 8) reason = `rank E\u2088 \u2260 8: the seam constant is forced \u2014 tempo N=${N} bends \u03b1 to ${isFinite(ai) ? ai.toFixed(2) : "\u2014"}`;
    else reason = "E\u2088 closes \u2014 all constraints met";
    return { closes, reason, ainv: ai, nfam: nf, alphaOk };
  }

  // the seven maximal E8 slices = the audit routes (v170 slice compression / E8-audit doc)
  const e8slices = [
    { name: "D\u2085 \u00d7 A\u2083", role: "main split", what: "SM carrier (16) + family glue" },
    { name: "E\u2086 \u00d7 A\u2082", role: "flavor", what: "the residue matrix R \u2014 det 8, minors (2,3,5)" },
    { name: "E\u2087 \u00d7 A\u2081", role: "gravity", what: "the scalaron & inflation (R+R\u00b2)" },
    { name: "F\u2084 \u00d7 G\u2082", role: "occupancy", what: "occupancy & gauge content" },
    { name: "A\u2084 \u00d7 A\u2084", role: "action", what: "the 1 : 5 : 10 action ladder" },
    { name: "A\u2088", role: "rank", what: "the rank decuple" },
    { name: "D\u2088", role: "split", what: "120 + 128 (NS + Ramond)" },
  ];
  // which audit route validates each prediction (keyed by title)
  const e8routeMap = {
    "Fine-structure constant": "D\u2085\u00d7A\u2083 route + EM budget 41 = 10 b\u2081",
    "Cabibbo angle": "E\u2086\u00d7A\u2082 flavor residue (\u03c6\u2080 seed)",
    "Flavor residue invariants": "E\u2086\u00d7A\u2082 \u2014 the residue matrix R",
    "Koide relation": "E\u2086\u00d7A\u2082 residue (source\u2192pole transfer)",
    "Solar angle": "A\u2083 family + seam misalignment",
    "Reactor angle": "A\u2083 family \u00d7 carrier trace 5/6",
    "Atmospheric angle": "A\u2083 family (\u03bc\u03c4 symmetry)",
    "Mass ordering & m_\u03b2\u03b2": "A\u2083 family / Majorana texture",
    "Strong CP / EDM null": "D\u2088 sheet (120+128), Pfaffian reality",
    "Proton/electron ratio": "no compiler route \u2014 frontier (F_transfer)",
    "Scalar tilt (R\u00b2)": "E\u2087\u00d7A\u2081 scalaron / inflation",
    "Tensor-to-scalar ratio": "E\u2087\u00d7A\u2081 scalaron / inflation",
    "Scalar amplitude": "E\u2087\u00d7A\u2081 scalaron (seam power c\u2083\u2077)",
    "Scalaron mass": "E\u2087\u00d7A\u2081 scalaron (c\u2083^{7/2})",
    "Baryon density": "A\u2084\u00d7A\u2084 action ladder / determinant line",
    "Baryon asymmetry": "F_transfer (Boltzmann) over A\u2084\u00d7A\u2084",
    "One exponential engine": "A\u2084\u00d7A\u2084 action ladder 1:5:10",
    "No second light Higgs": "carrier index (g_car \u2212 |\u03bc\u2084|)",
    "Cosmic birefringence": "determinant line (\u03c6\u2080/4\u03c0)",
    "Axion dark matter": "F_transfer (strong-CP determinant line)",
    "Rare kaon decays": "E\u2086\u00d7A\u2082 residue (closed CKM) + external SD",
    "EHT achromatic intercept": "horizon / determinant line (16 c\u2083\u2074)",
    "No fourth generation": "A\u2083 family geometry (closure)",
  };
  const smRouteByCat = {
    Structure: "carrier/glue closure (D\u2085\u2295A\u2083+\u03bc\u2084)",
    Forces: "D\u2085\u00d7A\u2083 route + budget 41",
    Masses: "E\u2086\u00d7A\u2082 flavor residue / \u03c6\u2080 ladder",
    Mixing: "A\u2083 family / residue R",
  };

  // ---- "break it" scenarios (failed universes as a goal) ----
  const scenarios = [
    { label: "g_car = 4", kind: "dial", N: 8, g: 4 },
    { label: "g_car = 6", kind: "dial", N: 8, g: 6 },
    { label: "tempo N = 7", kind: "dial", N: 7, g: 5 },
    { label: "drop the \u03bc\u2084 glue", kind: "force", reason: "without the \u03bc\u2084 glue, D\u2085\u2295A\u2083 has det 16 \u2260 1 \u2014 E\u2088 never forms (no even-unimodular closure)" },
    { label: "wrong R branch", kind: "force", reason: "a residue matrix with det \u2260 8 or minors \u2260 (2,3,5) fails the E\u2086\u00d7A\u2082 audit \u2014 flavor doesn't close" },
    { label: "promote m_p/m_e", kind: "firewall", toast: "\uD83D\uDEAB Nice try \u2014 that was numerology. m_p/m_e is a QCD/EW cross-sector ratio, not a compiler power; the frontier firewall blocks it (it stays an honest F_transfer item)." },
  ];

  // ---- substrate (hypergraph X-ray) ----
  const substrate = {
    note: "Substrate view: a consistent typed hypergraph \u2014 NOT a proof that a bare graph alone derives everything (the family cusp-weight is injected, not graph-derived).",
    types: {
      builds: { color: "#5b8cff", label: "builds" },
      glues: { color: "#a78bfa", label: "glues" },
      audits: { color: "#34d39a", label: "audits" },
      projects: { color: "#3fd0e0", label: "projects" },
      transfers: { color: "#f59e42", label: "transfers" },
      dresses: { color: "#f0b429", label: "dresses" },
    },
    nodes: [
      { id: "c3", label: "c\u2083", x: 0.10, y: 0.30, k: "in" },
      { id: "gcar", label: "g_car", x: 0.10, y: 0.50, k: "in" },
      { id: "mu4", label: "\u03bc\u2084", x: 0.10, y: 0.70, k: "in" },
      { id: "D5", label: "D\u2085", x: 0.30, y: 0.38, k: "build" },
      { id: "A3", label: "A\u2083", x: 0.30, y: 0.66, k: "build" },
      { id: "E8", label: "E\u2088", x: 0.50, y: 0.50, k: "audit" },
      { id: "R", label: "R", x: 0.67, y: 0.32, k: "flavor" },
      { id: "phi0", label: "\u03c6\u2080", x: 0.67, y: 0.66, k: "seed" },
      { id: "alpha", label: "\u03b1\u207b\u00b9", x: 0.86, y: 0.20, k: "out" },
      { id: "th12", label: "\u03b8\u2081\u2082", x: 0.86, y: 0.42, k: "out" },
      { id: "koide", label: "Koide", x: 0.86, y: 0.62, k: "out" },
      { id: "Lam", label: "\u039b", x: 0.86, y: 0.82, k: "out" },
    ],
    edges: [
      ["mu4", "D5", "builds", "E"], ["gcar", "D5", "builds", "E"], ["mu4", "A3", "builds", "E"], ["c3", "phi0", "builds", "E"],
      ["D5", "E8", "glues", "E"], ["A3", "E8", "glues", "E"], ["mu4", "E8", "glues", "E"],
      ["E8", "R", "audits", "E"], ["E8", "D5", "audits", "E"], ["E8", "A3", "audits", "E"],
      ["R", "th12", "projects", "E"], ["phi0", "th12", "projects", "E"], ["c3", "alpha", "projects", "E"], ["gcar", "alpha", "projects", "E"],
      ["R", "koide", "transfers", "C"], ["c3", "Lam", "dresses", "C"], ["alpha", "Lam", "transfers", "C"],
    ],
  };

  window.TFPT_DATA = { constants: { PI, c3, g_car, phi0 }, stations, edges, feedback, steps, sm, smGroups, predictions, predGroups, horizons, e8slices, e8routeMap, smRouteByCat, scenarios, substrate, em: { ainv, budgetM, nfamOf, closure } };
})();
