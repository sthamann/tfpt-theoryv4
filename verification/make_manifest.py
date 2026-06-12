"""Generate stable per-file content manifests (reviewer points A3/A5 + Lean).

Writes two manifests under the repo root:

  * manifest.sha256       -- the TeX/figures/verification bundle (the stable
                             content identity of the paper+script layer);
  * lean_manifest.sha256  -- the Lean archive (sources, lakefile, lake-manifest,
                             toolchain pin, audit script + transcript), so the
                             Lean layer has its own stable content identity
                             (Alessandro 5.0 review, point 2).

Neither is the Overleaf export zip hash (a container hash); these are the
content identities.

Run:    python make_manifest.py            # (re)generate both manifests
Check:  python make_manifest.py --check    # verify the SHIPPED manifests
                                           # against the working tree; exits
                                           # nonzero on any missing/stale row

The --check mode exists because of the v83 reviewer finding (Alessandro):
the exported package shipped one stale `status_ledger.csv` row because the
manifest had not been regenerated after a final ledger edit.  RELEASE RULE:
`make_manifest.py` is always the LAST step before export, and
`make_manifest.py --check` must pass on the exported tree.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SHIP_LEAN = "lean4-carrier-rigidity"              # canonical shipped path (what the package exports)


def _lean_read_dir():
    """Lean source dir, robust to both layouts (Alessandro v73 portability request):
    prefer the shipped path ``lean4-carrier-rigidity/`` when present, fall back to the
    source-repo path ``experiments/lean4-carrier-rigidity/``.  Never silently yields zero
    files when the Lean sources are present under either layout."""
    for cand in (SHIP_LEAN, "experiments/lean4-carrier-rigidity"):
        if os.path.isdir(os.path.join(ROOT, cand)):
            return cand
    return "experiments/lean4-carrier-rigidity"


LEAN_DIR = _lean_read_dir()                        # repo path (where the files actually live)

TEX = [
    "introduction.tex", "changelog.tex",
    # shared, imported fragments now live in tex-artefacts/
    # (the auto-generated tex-artefacts/version-auto.tex is gitignored and excluded)
    "tex-artefacts/tfpt_docset.tex", "tex-artefacts/tfpt_style.tex",
    "tex-artefacts/tfpt_status.tex", "tex-artefacts/tfpt_figures.tex",
    "tex-artefacts/verification.tex", "tex-artefacts/version.tex",
    "tex-artefacts/predictions.tex",
    "tfpt_1_architecture_e8.tex", "tfpt_2_standard_model.tex",
    "tfpt_3_e8_audit_bootstrap.tex", "tfpt_4_frontier.tex", "tfpt_5_redteam.tex",
    "tfpt_horizon_readouts.tex", "tfpt_research_contracts.tex",
    "origin_theory.tex",
]
FIG = ["figures/action_tower.pdf", "figures/alpha_ablation.pdf",
       "figures/mass_ladder.pdf", "figures/status_heatmap.pdf",
       "figures/coxeter_circle.pdf", "figures/attractor.pdf",
       "figures/sds_cover.pdf", "figures/nariai_entropy.pdf",
       "figures/cover_twins.pdf", "figures/orientation.pdf",
       "figures/seam_units.pdf", "figures/trisection.pdf"]


def collect():
    files = list(TEX) + list(FIG)
    vdir = os.path.join(ROOT, "verification")
    for f in sorted(os.listdir(vdir)):
        # .json covers the frozen blind-prediction registry (REG.FREEZE.01)
        if f.endswith((".py", ".csv", ".md", ".json")):
            files.append("verification/" + f)
    # Wolfram independent path (.wl / .wls + its README)
    wdir = os.path.join(vdir, "wolfram")
    if os.path.isdir(wdir):
        for f in sorted(os.listdir(wdir)):
            if f.endswith((".wl", ".wls", ".md")):
                files.append("verification/wolfram/" + f)
    # Red-team / stress-test layer (.py sources + README + generated summary table)
    rdir = os.path.join(vdir, "redteam")
    if os.path.isdir(rdir):
        for f in sorted(os.listdir(rdir)):
            if f.endswith((".py", ".md", ".txt")):
                files.append("verification/redteam/" + f)
    return files


def collect_lean():
    """Lean sources + build descriptors + toolchain pin + audit script/transcript.

    Excludes LaTeX build artefacts of the Lean note and any .lake/build cache;
    only the reviewer-relevant, version-controlled inputs are hashed.
    """
    base = os.path.join(ROOT, LEAN_DIR)
    if not os.path.isdir(base):
        return []
    keep_ext = (".lean",)
    keep_name = {"lakefile.lean", "lake-manifest.json", "lean-toolchain",
                 "AUDIT_TRANSCRIPT.txt", "README.md", "REVIEWER_USAGE.md", "audit.sh"}
    out = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d != ".lake"]   # skip build cache
        for fn in filenames:
            if fn.endswith(keep_ext) or fn in keep_name:
                rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace(os.sep, "/")
                # record under the CANONICAL SHIPPED path, but read from the repo path
                ship = rel.replace(LEAN_DIR, SHIP_LEAN, 1)
                out.append((ship, rel))
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def write_manifest(files, out_name, label):
    lines = []
    for item in files:
        # each item is either "rel" (read==record) or ("record_rel", "read_rel")
        record, readrel = item if isinstance(item, tuple) else (item, item)
        p = os.path.join(ROOT, readrel)
        if os.path.isfile(p):
            lines.append(f"{sha256(p)}  {record}")
    lines.sort(key=lambda s: s.split("  ", 1)[1])
    out = os.path.join(ROOT, out_name)
    with open(out, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    top = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    print(f"wrote {out} ({len(lines)} files)")
    print(f"  {label} digest (content id): {top}")
    return top


def check_manifest(name):
    """Verify a shipped manifest line-by-line against the working tree.
    Returns (missing, stale); prints every offending row."""
    path = os.path.join(ROOT, name)
    missing, stale = 0, 0
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            want, rel = line.split("  ", 1)
            # the Lean manifest records the canonical SHIPPED path; map it
            # back to the repo path when reading from a source checkout
            read = rel
            if rel.startswith(SHIP_LEAN + "/") and LEAN_DIR != SHIP_LEAN:
                read = rel.replace(SHIP_LEAN, LEAN_DIR, 1)
            p = os.path.join(ROOT, read)
            if not os.path.isfile(p):
                missing += 1
                print(f"  MISSING  {rel}")
            elif sha256(p) != want:
                stale += 1
                print(f"  STALE    {rel}")
    status = "OK" if missing == 0 and stale == 0 else "FAIL"
    print(f"{name}: missing {missing}, stale {stale}  [{status}]")
    return missing, stale


def main():
    if "--check" in sys.argv[1:]:
        m1, s1 = check_manifest("manifest.sha256")
        m2, s2 = check_manifest("lean_manifest.sha256")
        ok = (m1 + s1 + m2 + s2) == 0
        print("MANIFEST CHECK " + ("PASSED" if ok else "FAILED"
              + " -- rerun make_manifest.py as the LAST release step"))
        raise SystemExit(0 if ok else 1)
    write_manifest(collect(), "manifest.sha256", "manifest")
    write_manifest(collect_lean(), "lean_manifest.sha256", "lean manifest")


if __name__ == "__main__":
    main()
