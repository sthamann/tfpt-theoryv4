/**
 * Tour facts — single sync point for /tour numbers and labels.
 *
 * Sources: verification/status_ledger.csv, predictions_frozen.json,
 * website/lib/suite.ts (SCRIPT_TOTAL), website/lib/predictions.ts,
 * public verification stack (Python / Wolfram / Lean).
 * Snapshot date: 2026-07-23. Do not invent values; refresh from ledger/suite.
 */

import { SCRIPT_TOTAL } from "@/lib/suite";

/** Display markers only — fine types live in the ledger. */
export const STATUS_MARKERS = ["[E]", "[C]", "[O]", "[X]"] as const;

export const AXIOMS = {
  c3: {
    symbol: "c₃",
    value: "1/(8π)",
    latex: "c_3 = 1/(8\\pi)",
    label: "seam constant",
  },
  gCar: {
    symbol: "g_car",
    value: "5",
    latex: "g_{\\mathrm{car}} = 5",
    label: "carrier grade",
  },
} as const;

export const COMPILER = {
  chain: "D5 ⊕ A3 + μ4 ⇒ E8 ⇒ SM readouts",
  plain:
    "Two axioms feed a discrete compiler. The carrier algebra D₅ ⊕ A₃ with the μ₄ clock closes into the E₈ audit hull; Standard-Model readouts are read off that closure.",
} as const;

export const ALPHA = {
  inverse: "137.0359992",
  sigmaToCodata: "1.9σ",
  label: "α⁻¹ (EM fine-structure inverse)",
} as const;

export const PREDICTIONS = {
  frozenCount: 27,
  examples: [
    {
      id: "alpha",
      title: "Fine-structure constant",
      value: "α⁻¹ = 137.0359992",
      note: "1.9σ vs CODATA — one line among many, not a fit target",
    },
    {
      id: "theta12",
      title: "Solar mixing angle",
      value: "sin²θ₁₂ = 0.3067",
      note: "frozen; decisive confrontation at JUNO",
    },
    {
      id: "r",
      title: "Tensor-to-scalar ratio",
      value: "r ≈ 0.004",
      note: "frozen band; CMB-S4 / next-gen B-modes",
    },
  ],
} as const;

export const VERIFICATION = {
  pythonModules: SCRIPT_TOTAL,
  runCommand: "python run_all.py",
  runPassLine: "ALL CHECKS PASSED",
  wolfram: "116/116 + 564/564",
  leanCarrier: "0 sorry",
  externalReplications: 0,
} as const;

export const SEAM = {
  marks: 4,
  temperature: "T_seam = 4c₃",
  temperatureNote: "Hawking normalisation — third independent leg of c₃ (v526)",
  clockMetaphor: "quarter-beat clock on a circle with four marks",
} as const;

export const INPUT_BIT = {
  failedDerivations: 10,
  definition: "twist-class choice",
  measurable: "in principle interferometrically readable",
  status: "[O]" as const,
  note: "Ten side-blind derivation attempts failed; the bit stays an input, now physically defined.",
} as const;

export const TOY_KILL = {
  id: "v529",
  name: "straddle law",
  status: "published, not buried",
  plain:
    "The first interacting toy model fails a preregistered kill test (straddle law). Banked openly — anti-numerology style.",
} as const;

export const EMPIRICAL_NULLS = {
  rxte: "RXTE — search target (null)",
  nicer: "NICER 0.75% / 0.93% rms — search targets, never upgraded to claims",
} as const;

export const OPEN = {
  seamEquiv: {
    id: "SEAM.EQUIV",
    marker: "[O]" as const,
    plain: "Unconditional seam equivalence remains open; ledger is source of truth.",
  },
  interactingSeam: {
    plain:
      "Woit bridge: α / β₁ / β₂ executed at the free level; the interacting seam stays open.",
  },
} as const;

export const BRIDGES = {
  celestial: {
    name: "Celestial / twistor route",
    steps: 30,
    measureChain: "derived at probe level",
    progressLabel: "thirty-step story; measure chain derived",
  },
  woit: {
    name: "Woit OS-twistor bridge",
    executed: ["α", "β₁", "β₂"] as const,
    open: "β₃ / interacting",
    contract: "[O]" as const,
  },
} as const;

export const LINKS = {
  verification: "/verification",
  verificationDag: "/verification#dag",
  falsification: "/falsification",
  replication: "/replication",
  review: "/review",
  orientation: "/orientation",
} as const;

export type TourStepId =
  | "two-numbers"
  | "compiler"
  | "outputs"
  | "not-numerology"
  | "seam"
  | "check-yourself"
  | "how-it-dies"
  | "still-open"
  | "two-bridges"
  | "join-in";

export interface TourStepMeta {
  id: TourStepId;
  n: number;
  short: string;
  title: string;
  plain: string;
}

export const TOUR_STEPS: readonly TourStepMeta[] = [
  {
    id: "two-numbers",
    n: 1,
    short: "Two numbers",
    title: "What if two numbers were enough?",
    plain:
      "Everything here starts from two axioms: c₃ = 1/(8π) and g_car = 5. No secret knobs behind the curtain.",
  },
  {
    id: "compiler",
    n: 2,
    short: "The compiler",
    title: "Axioms in → machine → readouts out",
    plain:
      "Think of TFPT as a discrete compiler: feed the two axioms, run the carrier algebra, audit against E₈, read off Standard-Model structure.",
  },
  {
    id: "outputs",
    n: 3,
    short: "What comes out",
    title: "Concrete numbers you can argue with",
    plain:
      "Among the outputs: α⁻¹, mass and mixing structure, and 27 frozen predictions — three examples below with the actual figures.",
  },
  {
    id: "not-numerology",
    n: 4,
    short: "Not numerology",
    title: "Why this is not AI slop or curve-fitting",
    plain:
      "Predictions were frozen before decisive data; null Monte Carlos and look-elsewhere discipline are enforced; every claim carries an honest [E]/[C]/[O]/[X] grade.",
  },
  {
    id: "seam",
    n: 5,
    short: "The seam",
    title: "A circle, four marks, a built-in temperature",
    plain:
      "The seam is the heart of the story: a quarter-beat clock on four marks — and it carries Hawking's temperature normalisation as a measured third leg of c₃.",
  },
  {
    id: "check-yourself",
    n: 6,
    short: "Check it",
    title: "You do not have to trust us",
    plain:
      "One command runs the suite. Or open the in-browser Pyodide DAG on /verification and re-derive a node yourself.",
  },
  {
    id: "how-it-dies",
    n: 7,
    short: "How it dies",
    title: "Committed kill tests — including one that already fired",
    plain:
      "JUNO, CMB-S4 and friends can kill published predictions. Separately, a toy-level kill (v529, straddle law) already fired — and we published it.",
  },
  {
    id: "still-open",
    n: 8,
    short: "Still open",
    title: "What we do not pretend to have closed",
    plain:
      "SEAM.EQUIV stays [O] unconditionally. One input bit survives ten failed derivations — that failure is the point. The interacting seam is still open.",
  },
  {
    id: "two-bridges",
    n: 9,
    short: "Two bridges",
    title: "Celestial measure chain · Woit free bridge",
    plain:
      "Two research bridges toward physics: a thirty-step celestial/twistor story with a derived measure chain, and a Woit OS route with α→β₂ executed (interacting still open).",
  },
  {
    id: "join-in",
    n: 10,
    short: "Join in",
    title: "Reproduce, review, falsify",
    plain:
      "Zero external replications yet. The invitation is concrete: clone the repo, run the suite, file a kill, or write a review.",
  },
] as const;

export const TOUR_AS_OF = "2026-07-23";
