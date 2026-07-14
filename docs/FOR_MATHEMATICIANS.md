# TFPT for mathematicians

> The load-bearing content is lattice/Lie theory, finite-group geometry, and (at the frontier)
> VOA / AQFT. Here is where to inspect the formal objects and certificates.

## The `E8` closure (the exact core)

The compiler's "audit hull" is the even unimodular `E8` lattice, built as a glue extension of the
carrier. Inspect [`v1_e8_glue.py`](../verification/v1_e8_glue.py):

- `A3` and `D5` share the discriminant group `ℤ4` (`|det Cartan| = 4` each).
- Their discriminant-form norms `q(A3) = 3/4` and `q(D5) = 5/4` sum to the `E8` root norm `2` (the
  even-glue condition).
- The glued rank-8 even lattice has **240 roots**, **dimension 248**, glue index
  `[E8 : D5 ⊕ A3] = √(4·4/1) = 4 = |μ₄|`.
- An **explicit lattice certificate**: all 240 roots are built in coordinates (norm² = 2), the
  Bourbaki simple-root basis is constructed, and the lattice is verified **even** (integer Gram,
  even diagonal) and **unimodular** (`det = 1`), with every root integral over the basis. This is
  the even unimodular `E8` lattice itself, not merely an arithmetic match.

The Wolfram second path ([`wolfram/`](../verification/wolfram/)) re-derives the exact
algebraic/identity/lattice results independently (`368/368` on the extension).

## The uniqueness / rigidity theorems

- **Pascal closure** (`v2`): `g_car = 5` is the *unique* solution of
  `2^(g−1) = C(g,0)+C(g,1)+C(g,2)`, and `N_fam`, `rank E8 = 8`, the occupancy `48`, and the abelian
  index `b₁ = 41/10` all follow from `g` alone.
- **Boundary carrier selection** (`v47`): `(D5 ⊕ A3) + μ4 ≅ E8` is the unique familyful glue;
  alternatives are excluded.
- **Rank-gap converse** (Lean `AnchorLadder.rankgap_uniqueness`): `p₄ − p₃ = 8` selects the anchor
  `(1,1,2)` up to permutation.

## The formal certificates (Lean 4)

[`experiments/lean4-carrier-rigidity/`](../experiments/lean4-carrier-rigidity/) is machine-formalised
and **audited by CI**: no `sorry`/`admit`, no domain-specific axioms, and `#print axioms` on every
headline theorem returns *only* the three standard kernel axioms (`propext`, `Classical.choice`,
`Quot.sound`). The seam-residual modules additionally declare their *named cited-theorem* axioms
explicitly (e.g. `SeamResidualAxiom.lean`). Run it:

```bash
cd experiments/lean4-carrier-rigidity && lake exe cache get && bash scripts/audit.sh
```

Formalised: the carrier algebra (hypercharge, anomaly-freedom, integer rigidity, Pascal/glue
uniqueness), the anchor ladder, the Möbius uniformisation normal form (`FORM.QGEO.02`), the
conditional DtN theorem (`FORM.QGEO.01`), the seam equivalence chain (`FORM.SEAMEQUIV.01`), and the
S3 continuum leg (`FORM.SEAM.MMST.01`: MMST hypotheses kernel-proved, scaling limit + OS
reconstruction as *named cited* axioms).

## The structural objects worth a look

- **Master cover** (`v85`): all anchor-block pencil covers are *one* double cover up to GL(2) Möbius
  reparametrisation (`disc = N_fam⁴·det(G)²`); Koide and the carrier are its two branch points.
- **Spine tetrahedron** (`v91`): `{2,3,4,5}` as one finite object — edges `{6,8,10,12,15,20}`,
  faces `{24,30,40,60}`, volume `120 = |R⁺(E8)|`; `240 = |μ₄|·|E(K₄)|·|E(K₅)|` (breaks at `K₆`).
- **Centered flavor diamond** (`v95`): four flavor operators as one center plus two axes.
- **Icosahedral / McKay bedrock** (`v219`): `E8` is the exceptional top of the McKay tower of finite
  `SU(2)` subgroups (`2I`, order `120`, Kac marks summing to `30 = h(E8)`) — choosing `E8` is
  choosing the icosahedron.

## The VOA / AQFT frontier

The single keystone `SEAM.EQUIV.01` reads as a simple-current extension
`(D₅)₁ ⊗ (A₃)₁ ⋊ ⟨(1,1)⟩ ≅ (E₈)₁` (index 4, `c = 8`, `μ = 1 ⇒` holomorphic `⇒ E8`, `v154`). The
`128`-spinor extension is the local `ℤ₂` simple-current crossed product with Longo–Rehren locality
integer `h_s = 16/16 = 1 ∈ ℤ`; holomorphy + Dong–Mason/Schellekens give the holomorphic `c = 8` VOA
uniquely `= V_{E8}` (`v463`). What stays `[O]` is the abstract continuum existence of the scaling
limit (cited MMST + OS-reconstruction theorems, not re-proved). See [`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md).

## Where to read

[`tfpt_1_architecture_e8.tex`](../tfpt_1_architecture_e8.tex) (the `D5 ⊕ A3 + μ4 ⇒ E8` construction),
[`tfpt_3_e8_audit_bootstrap.tex`](../tfpt_3_e8_audit_bootstrap.tex) (the seven `E8` slices, the
cascade bridge, the Möbius self-consistency loop), and the Lean project above.
