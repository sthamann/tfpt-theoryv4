#!/usr/bin/env python3
"""The ONE sync audit: papers <-> suite <-> ledger <-> changelog <-> website.

Bundles every consistency check that previously lived as loose shell snippets
in the workflow rules, plus the reverse directions.  Prints NOTHING but the
final verdict when everything agrees; prints every violation and exits 1
otherwise.

    python3 verification/audit_sync.py          # full audit
    bash build.sh audit                          # same, via the build script

Checks (sections A-F):
  A  suite integrity   : files on disk == run_all.py registration;
                         script_registry.csv == run_all.py; generated
                         verification.tex / ScriptIndex.tsx / content maps fresh
  B  papers, forward   : every registered script is cited (\\veri) in a paper
                         BODY (the master index table alone does not count)
  B  papers, reverse   : every \\veri{...} / \\vref{vN} target in the active
                         docs is a registered script (catches stale citations)
  B  changelog         : every registered script's module id appears in
                         changelog.tex (minus the frozen grandfathered list);
                         dated subsections are newest-first (non-increasing)
  C  csv well-formed    : every machine CSV (ledger, registry, clusters, freeze)
                         parses to a constant column width (no unquoted commas)
  C  ledger            : registry <-> status_ledger.csv script column agree
  D  website mirror    : public/verification == verification (sha256);
                         public/papers == root PDFs (sha256); release.ts
                         bytes+sha match the served PDFs; every vN mentioned
                         anywhere in website code is a registered script;
                         every pdf path in papers.ts exists
  E  versions          : website/lib/version.ts == tex-artefacts/version.tex;
                         release.ts COMMON version mentions the same version
  F  wolfram + layout  : wolfram README count == ledger GATE.WOLFRAM.01 count;
                         no overfull hbox > 30pt and no overfull vbox in the
                         logs of the active docs

Exceptions live in verification/audit_baseline.json (frozen: entries may only
be REMOVED, never added for new work).

stdlib only.
"""
import csv
import json
import hashlib
import re
import sys
from pathlib import Path

import make_docs_map
import make_script_index

ROOT = Path(__file__).resolve().parent.parent
VERIF = ROOT / "verification"
WEB = ROOT / "website"

ACTIVE_DOCS = make_docs_map.DOCS                       # 9 papers
ALL_NOTES = ACTIVE_DOCS + ["changelog"]                # + standalone changelog

errors: list[str] = []


def err(section: str, msg: str) -> None:
    errors.append(f"[{section}] {msg}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalise_tex(text: str) -> str:
    return text.replace("\\allowbreak", "").replace("\\", "").replace(" ", "")


def module_id(script: str) -> str:
    return script.split("_")[0]


def changelog_entry_dates(text: str) -> list[tuple[int, int, str]]:
    """Return (date_sort_key, line_no, title) for each dated \\subsection*."""
    out: list[tuple[int, int, str]] = []
    for m in re.finditer(r"^\\subsection\*\{(20\d\d-\d\d-\d\d[^}]*)\}", text, re.M):
        title = m.group(1)
        dates = re.findall(r"20\d\d-\d\d-\d\d", title)
        if not dates:
            continue
        date_key = int(max(dates).replace("-", ""))
        line_no = text[: m.start()].count("\n") + 1
        out.append((date_key, line_no, title))
    return out


def load_baseline() -> dict:
    return json.loads((VERIF / "audit_baseline.json").read_text())


# -------------------------------------------------------------- A: suite
def check_suite(registered: list[str]) -> None:
    on_disk = {p.stem for p in VERIF.glob("v*.py") if re.match(r"v\d+_", p.name)}
    for s in sorted(on_disk - set(registered)):
        err("A.suite", f"{s}.py exists but is NOT registered in run_all.py")
    for s in sorted(set(registered) - on_disk):
        err("A.suite", f"{s} registered in run_all.py but file missing")

    # generated surfaces fresh?
    for target, content in make_script_index.build().items():
        if not target.exists() or target.read_text() != content:
            err("A.generated", f"{target.relative_to(ROOT)} stale -- run make_script_index.py")
    docs_csv, web_csv, sidecar = make_docs_map.build()
    for t, content in [
        (make_docs_map.DOCS_MAP, docs_csv),
        (make_docs_map.WEBSITE_MAP, web_csv),
        (make_docs_map.DATES_FILE, json.dumps(sidecar, indent=1) + "\n"),
    ]:
        if not t.exists() or t.read_text() != content:
            err("A.generated", f"{t.relative_to(ROOT)} stale -- run make_docs_map.py")


# -------------------------------------------------------------- B: papers
def check_papers(registered: list[str], baseline: dict) -> None:
    bodies = "".join((ROOT / f"{d}.tex").read_text() for d in ACTIVE_DOCS)
    bodies_norm = normalise_tex(bodies)
    body_exceptions = set(baseline.get("body_citation_exceptions", []))
    for s in registered:
        if s in body_exceptions:
            continue
        if s not in bodies_norm:
            err("B.forward", f"{s}.py is not cited in any paper body "
                             f"(master index alone does not count)")

    # reverse: every citation target must be a registered script
    all_tex = bodies + (ROOT / "changelog.tex").read_text()
    all_tex += "".join(p.read_text() for p in (ROOT / "tex-artefacts").glob("*.tex"))
    reg_set = set(registered)
    for m in re.finditer(r"\\veri\{([^}]*)\}", all_tex):
        target = normalise_tex(m.group(1))
        if target.endswith(".py"):
            target = target[:-3]
        if target.startswith("v") and target not in reg_set:
            err("B.reverse", f"\\veri{{{m.group(1)}}} cites unknown script '{target}'")
    mod_ids = {module_id(s) for s in registered}
    for m in re.finditer(r"\\vref\{(v\d+)[^}]*\}", all_tex):
        if m.group(1) not in mod_ids:
            err("B.reverse", f"\\vref{{{m.group(1)}}} references unknown module")

    # changelog: every non-grandfathered module id must appear
    chl = (ROOT / "changelog.tex").read_text()
    grandfathered = set(baseline.get("changelog_grandfathered", []))
    for s in registered:
        mid = module_id(s)
        if mid in grandfathered:
            continue
        if not re.search(r"\b" + mid + r"(?![0-9])", chl):
            err("B.changelog", f"{s}.py ({mid}) has no changelog.tex entry")

    entries = changelog_entry_dates(chl)
    for i in range(len(entries) - 1):
        cur_date, cur_line, cur_title = entries[i]
        nxt_date, nxt_line, nxt_title = entries[i + 1]
        if cur_date < nxt_date:
            err(
                "B.changelog",
                f"date order broken at line {cur_line}: {cur_title!r} (newer) "
                f"appears before line {nxt_line}: {nxt_title!r} (older) -- newest first",
            )


# -------------------------------------------------------------- C: ledger
def check_csv_wellformed() -> None:
    """Every machine-read CSV must parse to a constant column width -- guards the
    'single source of truth' against unquoted-comma corruption (a stray comma in
    a status/external field silently shifts every later column)."""
    for name in ("status_ledger.csv", "script_registry.csv",
                 "script_clusters.csv", "freeze_file.csv"):
        path = VERIF / name
        if not path.exists():
            continue
        with path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        if not rows:
            err("C.csv", f"{name} is empty")
            continue
        width = len(rows[0])
        for i, row in enumerate(rows, 1):
            if len(row) != width:
                first = row[0][:40] if row else ""
                err("C.csv", f"{name} line {i} has {len(row)} fields, expected "
                             f"{width} (unquoted comma in '{first}'? quote the field)")


def check_ledger(registered: list[str]) -> None:
    ledger_scripts = make_script_index.load_ledger_scripts()
    for s in sorted(set(registered) - ledger_scripts):
        err("C.ledger", f"{s}.py not referenced by any status_ledger.csv row")
    for s in sorted(ledger_scripts - set(registered)):
        err("C.ledger", f"ledger references unregistered script {s}.py")


# -------------------------------------------------------------- D: website
def check_website(registered: list[str]) -> None:
    # 1. verification mirror
    pub_v = WEB / "public" / "verification"
    want = {f"{s}.py" for s in registered} | {"tfpt_constants.py"}
    have = {p.name for p in pub_v.glob("*.py")}
    for name in sorted(want - have):
        err("D.verification", f"website/public/verification/{name} missing")
    for name in sorted(have - want):
        err("D.verification", f"website/public/verification/{name} is orphaned")
    for name in sorted(want & have) + ["predictions_frozen.json"]:
        if (VERIF / name).exists() and (pub_v / name).exists():
            if sha256(VERIF / name) != sha256(pub_v / name):
                err("D.verification", f"website/public/verification/{name} differs from verification/{name}")

    # 2. papers mirror
    pub_p = WEB / "public" / "papers"
    for doc in ALL_NOTES:
        root_pdf, web_pdf = ROOT / f"{doc}.pdf", pub_p / f"{doc}.pdf"
        if not root_pdf.exists():
            err("D.papers", f"{doc}.pdf missing at repo root (run build.sh notes)")
            continue
        if not web_pdf.exists():
            err("D.papers", f"website/public/papers/{doc}.pdf missing (run build.sh website)")
        elif sha256(root_pdf) != sha256(web_pdf):
            err("D.papers", f"website/public/papers/{doc}.pdf differs from root PDF (run build.sh website)")

    # 3. release.ts bytes + sha match the served PDFs
    release = (WEB / "lib" / "release.ts").read_text()
    entries = {
        m.group(1): (int(m.group(2)), m.group(3))
        for m in re.finditer(
            r'"(/papers/[^"]+\.pdf)":\s*\{[\s\S]*?bytes:\s*(\d+),\s*sha256:\s*\n?\s*"([0-9a-f]+)"',
            release,
        )
    }
    for pdf in sorted(pub_p.glob("*.pdf")):
        href = f"/papers/{pdf.name}"
        if href not in entries:
            err("D.release", f"{href} served but has no lib/release.ts entry")
            continue
        nbytes, sha = entries[href]
        if nbytes != pdf.stat().st_size or sha != sha256(pdf):
            err("D.release", f"{href}: release.ts bytes/sha stale (run npm run release:write)")

    # 4. scripts mentioned in website code must be registered
    reg_files = {f"{s}.py" for s in registered} | {"tfpt_constants.py"}
    for sub in ("app", "components", "lib"):
        for f in sorted((WEB / sub).rglob("*.ts*")):
            for name in set(re.findall(r"v\d+_[A-Za-z0-9_]+\.py", f.read_text())):
                if name not in reg_files:
                    err("D.code", f"{f.relative_to(ROOT)} references unknown script {name}")

    # 5. every pdf path referenced in papers.ts exists
    papers_ts = (WEB / "lib" / "papers.ts").read_text()
    for m in re.finditer(r'pdf:\s*"(/papers/[^"]+)"', papers_ts):
        if not (WEB / "public" / m.group(1).lstrip("/")).exists():
            err("D.papers_ts", f"papers.ts references missing file {m.group(1)}")


# -------------------------------------------------------------- E: versions
def tex_version() -> str:
    text = (ROOT / "tex-artefacts" / "version.tex").read_text()
    return re.search(r"\\def\\TFPTversion\{([^}]*)\}", text).group(1)


def check_versions() -> None:
    ver = tex_version()
    version_ts = WEB / "lib" / "version.ts"
    if not version_ts.exists():
        err("E.version", "website/lib/version.ts missing (run build.sh website)")
    else:
        m = re.search(r'SITE_VERSION = "([^"]+)"', version_ts.read_text())
        if not m or m.group(1) != ver:
            err("E.version", f"version.ts SITE_VERSION != TFPTversion ({ver}) -- run build.sh website")
    release = (WEB / "lib" / "release.ts").read_text()
    m = re.search(r'version:\s*"TFPT ([^"]+)"', release)
    if not m or m.group(1) != ver:
        err("E.version", f"release.ts COMMON version != TFPT {ver} -- run build.sh website")


# -------------------------------------------------------------- F: wolfram + layout
def check_wolfram() -> None:
    readme = (VERIF / "wolfram" / "README.md").read_text()
    m = re.search(r"Wolfram readouts: (\d+) passed", readme)
    ledger = (VERIF / "status_ledger.csv").read_text()
    m2 = re.search(r"\((\d+)/(\d+) pass", ledger)
    if not m or not m2:
        err("F.wolfram", "could not locate wolfram counts in README/ledger")
        return
    if not (m.group(1) == m2.group(1) == m2.group(2)):
        err("F.wolfram", f"wolfram counts disagree: README {m.group(1)} vs ledger "
                         f"{m2.group(1)}/{m2.group(2)} -- update both + re-run the .wl")
    # the website stats card must carry the same counts (base + extension)
    m3 = re.search(r"current total (\d+)/(\d+)", ledger)
    page = (WEB / "app" / "verification" / "page.tsx").read_text()
    base = m.group(1)
    if f"{base}/{base}" not in page:
        err("F.wolfram", f"website verification page misses the base count {base}/{base}")
    if m3 and f"{m3.group(1)}/{m3.group(2)}" not in page:
        err("F.wolfram", f"website verification page misses the extension count "
                         f"{m3.group(1)}/{m3.group(2)}")


def check_overfull() -> None:
    for doc in ALL_NOTES:
        log = ROOT / f"{doc}.log"
        if not log.exists():
            continue
        text = log.read_text(errors="replace")
        for m in re.finditer(r"Overfull \\hbox \((\d+(?:\.\d+)?)pt", text):
            if float(m.group(1)) > 30:
                err("F.layout", f"{doc}.log: overfull hbox {m.group(1)}pt (>30pt)")
        if "Overfull \\vbox" in text:
            err("F.layout", f"{doc}.log: overfull vbox")


# --------------------------------------------------------------
def main() -> None:
    registered = make_script_index.load_run_all_modules()
    baseline = load_baseline()
    check_suite(registered)
    check_papers(registered, baseline)
    check_csv_wellformed()
    check_ledger(registered)
    check_website(registered)
    check_versions()
    check_wolfram()
    check_overfull()
    if errors:
        for e in errors:
            print(e)
        print(f"\nAUDIT FAILED: {len(errors)} problem(s)")
        sys.exit(1)
    print(f"AUDIT OK ({len(registered)} scripts; papers, ledger, changelog and website in sync)")


if __name__ == "__main__":
    main()
