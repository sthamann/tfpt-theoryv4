"""make_script_atlas.py -- GENERATED VIEW (do not edit script_atlas.md by hand).

Fuses the existing single sources into one causal, grouped atlas so an agent (or a
reader) can see at a glance WHAT already exists, which theme/branch it touches,
what it depends on, and what it supersedes -- the antidote to duplicating work or
forgetting old results.  No new data: it only re-projects

    status_ledger.csv    (claim -> status, dependencies, script, supersedes)
    script_registry.csv  (script -> cluster, one-line description)
    script_clusters.csv  (cluster -> title, purpose)
    docs_map.csv         (script -> which paper sections cite it)

into verification/script_atlas.md.  Wire-in: `bash build.sh gen`.  stdlib only.
"""
import csv
import os
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "script_atlas.md")

MARKER_RE = re.compile(r"\[(E|C|O|X|I|L|N|F|A|P)\]")


def _read(name):
    p = os.path.join(HERE, name)
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def norm(s):
    """canonical script key (registry has no .py, ledger/docs-map have .py)."""
    return (s or "").strip().removesuffix(".py")


def script_id_num(script):
    m = re.match(r"v(\d+)_", script)
    return int(m.group(1)) if m else 10 ** 9


WORD_FOLD = [("identit", "E"), ("lattice", "E"), ("numerical", "E"),
             ("formal", "E"), ("axiom", "O"), ("open", "O"),
             ("physical", "C"), ("conditional", "C"), ("kill", "X")]


def short_markers(status, canonical):
    """collapse to the 4-class display tags present, e.g. {E,C,O}."""
    blob = (status + " " + canonical)
    tags = set(MARKER_RE.findall(blob))
    fold = {"I": "E", "L": "E", "N": "E", "F": "E", "A": "O", "P": "C"}
    tags = {fold.get(t, t) for t in tags}
    low = blob.lower()
    for word, tag in WORD_FOLD:          # fold fine status words too (early rows have no [..])
        if word in low:
            tags.add(tag)
    order = [t for t in ("E", "C", "O", "X") if t in tags]
    return "[" + "/".join(order) + "]" if order else "[-]"


def main():
    ledger = _read("status_ledger.csv")
    registry = _read("script_registry.csv")
    clusters = _read("script_clusters.csv")
    docs = _read("docs_map.csv")

    # script -> cluster, one-liner
    reg = {r["script"]: r for r in registry}
    cluster_meta = {c["cluster"]: c for c in clusters}

    # claim -> row ; script -> [claims] ; claim -> script
    claim_row = {r["claim_id"]: r for r in ledger}
    script_claims = defaultdict(list)
    claim_to_script = {}
    for r in ledger:
        s = (r.get("script") or "").strip()
        if s and s.endswith(".py"):
            script_claims[norm(s)].append(r["claim_id"])
            claim_to_script.setdefault(r["claim_id"], norm(s))

    # script -> docs that cite it (from docs_map scripts column)
    script_docs = defaultdict(set)
    for d in docs:
        for s in (d.get("scripts") or "").split(";"):
            s = s.strip()
            if s:
                script_docs[norm(s)].add(d["doc"])

    # supersede map: old_claim -> (new_claim, new_script)
    supersedes = {}
    for r in ledger:
        sup = (r.get("supersedes") or "").strip()
        if sup and sup != "-":
            for old in re.split(r"[;,]", sup):
                old = old.strip()
                if old:
                    supersedes[old] = (r["claim_id"], (r.get("script") or "").strip())

    def deps_as_scripts(claim_ids):
        out = []
        seen = set()
        for cid in claim_ids:
            row = claim_row.get(cid)
            if not row:
                continue
            for dep in re.split(r"[;]", row.get("dependencies") or ""):
                dep = dep.strip()
                if not dep or dep == "-":
                    continue
                tgt = claim_to_script.get(dep, dep)  # script or bare claim id
                key = tgt
                if key not in seen:
                    seen.add(key)
                    out.append(tgt)
        return out

    lines = []
    A = lines.append
    n_scripts = len(reg)
    A("# TFPT verification atlas\n")
    A("> **Generated** by `make_script_atlas.py` (`bash build.sh gen`) from the "
      "ledger + registry + clusters + docs map. Do not edit by hand.\n")
    A(f"`{n_scripts}` registered scripts · `{len(ledger)}` ledger claims · "
      f"`{len(cluster_meta)}` clusters.\n")
    A("**How to read:** each script line is "
      "`vN_name  [markers]  CLAIM.IDs  — one-liner`; the sub-line shows "
      "`deps` (resolved to the scripts they come from), `supersedes`, and the "
      "papers that cite it. The four-class markers are `[E]` exact/proven, "
      "`[C]` conditional, `[O]` open/axiom, `[X]` kill-test.\n")

    # ---- clusters in a sensible reading order ----
    order = ["core", "em", "flavor", "masses", "neutrinos", "gravity",
             "horizon", "uwall", "frontier", "registry"]
    order += [c for c in cluster_meta if c not in order]

    by_cluster = defaultdict(list)
    for s, r in reg.items():
        by_cluster[r["cluster"]].append(s)

    A("## Clusters (themes / branches)\n")
    for cl in order:
        if cl not in cluster_meta:
            continue
        meta = cluster_meta[cl]
        scripts = sorted(by_cluster.get(cl, []), key=script_id_num)
        A(f"### `{cl}` — {meta['title']}  ({len(scripts)} scripts)")
        A(f"_{meta['purpose']}_\n")
        for s in scripts:
            claims = script_claims.get(s, [])
            mk = short_markers(
                " ".join(claim_row[c]["status"] for c in claims if c in claim_row),
                " ".join(claim_row[c].get("canonical_status", "") for c in claims if c in claim_row),
            )
            one = (reg[s].get("what_web") or "").strip()
            one = one.split(" — ", 1)[-1] if " — " in one else one
            one = re.sub(r"\s+", " ", one)[:180]
            cids = ", ".join(claims) if claims else "(no ledger claim)"
            A(f"- **{s.replace('.py','')}** {mk} `{cids}` — {one}")
            deps = deps_as_scripts(claims)
            sup_out = [f"{c}→{supersedes[c][0]}" for c in claims if c in
                       {old for old in supersedes}]  # this script's claims that ARE superseded
            sub = []
            if deps:
                sub.append("deps: " + ", ".join(
                    d.replace('.py', '') if d.endswith('.py') else d for d in deps[:8]))
            cited = sorted(script_docs.get(s, []))
            if cited:
                sub.append("cited: " + ", ".join(c.replace("tfpt_", "").replace("_", " ") for c in cited))
            if sub:
                A("  - " + " · ".join(sub))
        A("")

    # ---- supersede map ----
    A("## Supersede map — do NOT reuse the left-hand claim\n")
    if supersedes:
        for old in sorted(supersedes):
            new, ns = supersedes[old]
            A(f"- `{old}` → superseded by `{new}` ({ns.replace('.py','') if ns else '-'})")
    else:
        A("- (none recorded)")
    A("")

    # ---- dependency overview ----
    indeg = defaultdict(int)
    for r in ledger:
        for dep in re.split(r"[;]", r.get("dependencies") or ""):
            dep = dep.strip()
            if dep and dep != "-":
                indeg[dep] += 1
    roots = sorted(c for c in claim_row if not [d for d in
                   re.split(r"[;]", claim_row[c].get("dependencies") or "") if d.strip() and d.strip() != "-"])
    most = sorted(indeg.items(), key=lambda kv: -kv[1])[:15]
    A("## Dependency overview\n")
    A(f"**Most-depended-on claims** (the load-bearing roots): " +
      ", ".join(f"`{c}`×{n}" for c, n in most) + "\n")
    A(f"**Axiom/root claims with no dependencies:** {len(roots)} "
      f"(e.g. {', '.join('`'+c+'`' for c in roots[:12])} …)\n")

    # ---- frontier (highest ids) ----
    all_scripts = sorted(reg, key=script_id_num)
    A("## Current frontier (highest-id scripts)\n")
    for s in all_scripts[-12:]:
        claims = script_claims.get(s, [])
        cids = ", ".join(claims) if claims else "(no claim)"
        A(f"- **{s.replace('.py','')}** — `{cids}`")
    A("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {OUT} ({n_scripts} scripts, {len(cluster_meta)} clusters, "
          f"{len(supersedes)} supersede links)")


if __name__ == "__main__":
    main()
