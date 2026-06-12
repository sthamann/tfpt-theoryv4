#!/usr/bin/env python3
"""Generate the two script-index surfaces from ONE source of truth.

Source : verification/script_registry.csv   (script, cluster, what_web, what_tex)
         verification/script_clusters.csv   (cluster, title, purpose, accent)
Targets: tex-artefacts/verification.tex     (master script->check table, \\input
         by introduction.tex)
         website/components/ScriptIndex.tsx (clustered website index)

Both targets are GENERATED -- never edit them by hand.  To add/change a script
description, edit script_registry.csv and re-run:

    python3 verification/make_script_index.py            # rewrite both targets
    python3 verification/make_script_index.py --check    # exit 1 if stale

Validations (hard failures):
  * registry scripts == run_all.py MODULES (both directions, no duplicates)
  * every registry cluster is defined in script_clusters.csv
  * every registry script appears in >=1 row of status_ledger.csv

stdlib only -- runnable without the venv (build.sh calls it with python3).
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERIF = ROOT / "verification"
TEX_TARGET = ROOT / "tex-artefacts" / "verification.tex"
TSX_TARGET = ROOT / "website" / "components" / "ScriptIndex.tsx"
SUITE_TARGET = ROOT / "website" / "lib" / "suite.ts"


def module_number(script: str) -> int:
    return int(re.match(r"v(\d+)_", script).group(1))


def load_run_all_modules() -> list[str]:
    text = (VERIF / "run_all.py").read_text()
    return re.findall(r'\("(v\d+_[A-Za-z0-9_]+)"', text)


def load_clusters() -> dict[str, dict]:
    clusters = {}
    with open(VERIF / "script_clusters.csv", newline="") as f:
        for row in csv.DictReader(f):
            clusters[row["cluster"]] = row
    return clusters


def load_registry() -> list[dict]:
    with open(VERIF / "script_registry.csv", newline="") as f:
        return list(csv.DictReader(f))


def load_ledger_scripts() -> set[str]:
    scripts = set()
    with open(VERIF / "status_ledger.csv", newline="") as f:
        for row in csv.DictReader(f):
            for s in (row.get("script") or "").split(";"):
                s = s.strip().removesuffix(".py")
                if re.match(r"v\d+_", s):
                    scripts.add(s)
    return scripts


def validate(registry: list[dict], clusters: dict[str, dict]) -> list[str]:
    errors = []
    reg_scripts = [r["script"] for r in registry]
    dupes = {s for s in reg_scripts if reg_scripts.count(s) > 1}
    if dupes:
        errors.append(f"duplicate registry rows: {sorted(dupes)}")
    reg_set, mod_set = set(reg_scripts), set(load_run_all_modules())
    if reg_set - mod_set:
        errors.append(f"in registry but NOT in run_all.py: {sorted(reg_set - mod_set)}")
    if mod_set - reg_set:
        errors.append(f"in run_all.py but NOT in registry: {sorted(mod_set - reg_set)}")
    for r in registry:
        if r["cluster"] not in clusters:
            errors.append(f"{r['script']}: unknown cluster '{r['cluster']}'")
        if not r["what_tex"].strip() or not r["what_web"].strip():
            errors.append(f"{r['script']}: empty what_tex/what_web description")
    ledger = load_ledger_scripts()
    missing_ledger = reg_set - ledger
    if missing_ledger:
        errors.append(f"not in status_ledger.csv: {sorted(missing_ledger)}")
    return errors


# --------------------------------------------------------------------------
# tex-artefacts/verification.tex
# --------------------------------------------------------------------------

TEX_HEADER = r"""% ---------------------------------------------------------------------
%  tex-artefacts/verification.tex -- THE master script->check index.
%  The long table mapping every verification/vN_*.py to the claim it
%  machine-checks.  \input near the end of introduction.tex (inside the
%  "computational verification" appendix).
%
%  GENERATED FILE -- DO NOT EDIT BY HAND.
%  Source: verification/script_registry.csv (column what_tex).
%  Regenerate with:  python3 verification/make_script_index.py
%
%  Requires: xltabular (loaded by the including document) and the Y
%  column type (\newcolumntype{Y}{>{\raggedright\arraybackslash}X}).
% ---------------------------------------------------------------------
{\small
\renewcommand{\arraystretch}{1.25}
\begin{xltabular}{\linewidth}{@{}p{3.5cm}Y@{}}
\toprule
\textbf{Script} & \textbf{What it machine-checks} \\
\midrule
\endfirsthead
\toprule
\textbf{Script} & \textbf{What it machine-checks \emph{(continued)}} \\
\midrule
\endhead
\midrule
\multicolumn{2}{r@{}}{\scriptsize\itshape continued on next page}\\
\endfoot
\bottomrule
\endlastfoot
"""

TEX_FOOTER = "\\end{xltabular}\n}\n"


def tex_script_name(script: str) -> str:
    # v10_projection_involution -> v10\_\allowbreak projection\_\allowbreak involution.py
    return script.replace("_", "\\_\\allowbreak ") + ".py"


def gen_tex(registry: list[dict]) -> str:
    rows = sorted(registry, key=lambda r: module_number(r["script"]))
    body = "".join(
        f"\\texttt{{{tex_script_name(r['script'])}}} & {r['what_tex']} \\\\\n"
        for r in rows
    )
    return TEX_HEADER + body + TEX_FOOTER


# --------------------------------------------------------------------------
# website/components/ScriptIndex.tsx
# --------------------------------------------------------------------------

TSX_HEADER = """\
// GENERATED FILE -- DO NOT EDIT THE CLUSTERS DATA BY HAND.
// Source: verification/script_registry.csv + script_clusters.csv.
// Regenerate with:  python3 verification/make_script_index.py
"use client";

import { motion } from "motion/react";
import { Play } from "lucide-react";
import { useReproducer } from "./Reproducer";

interface Script {
  file: string;
  what: string;
}

interface Cluster {
  title: string;
  purpose: string;
  accent: string;
  scripts: Script[];
}

const CLUSTERS: Cluster[] = [
"""

TSX_FOOTER = """];

const TOTAL = CLUSTERS.reduce((n, c) => n + c.scripts.length, 0);

export function ScriptIndex() {
  const { open } = useReproducer();
  return (
    <div>
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <p className="max-w-3xl text-sm leading-relaxed text-slate-400">
          The suite is organised by what it proves. Each script is one claim
          cluster, cited inline in the documents via{" "}
          <span className="font-mono text-slate-300">\\veri&#123;vN&#125;</span>{" "}
          and registered in <span className="font-mono text-slate-300">run_all.py</span>,
          which ends <span className="font-mono text-emerald-300">ALL CHECKS PASSED</span>.{" "}
          <span className="text-slate-300">Click any script to run it live in your browser.</span>
        </p>
        <span className="rounded-full bg-slate-800/60 px-3 py-1 text-[11px] font-mono uppercase tracking-widest text-slate-300 ring-1 ring-slate-700/40">
          {TOTAL} scripts
        </span>
      </div>

      <div className="grid gap-5 lg:grid-cols-2">
        {CLUSTERS.map((c, i) => (
          <motion.section
            key={c.title}
            initial={{ opacity: 0, y: 14 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.05 }}
            transition={{ duration: 0.5, delay: (i % 2) * 0.05 }}
            className="glass relative overflow-hidden rounded-2xl ring-1 ring-slate-700/40"
          >
            <div
              aria-hidden
              className={`absolute inset-x-0 top-0 h-px bg-gradient-to-r ${c.accent} opacity-70`}
            />
            <div className="p-5 sm:p-6">
              <div className="flex items-center justify-between gap-3">
                <h3 className="font-serif text-base font-semibold text-slate-50">
                  {c.title}
                </h3>
                <span className="rounded-full bg-slate-800/60 px-2 py-0.5 text-[10px] font-mono text-slate-400">
                  {c.scripts.length}
                </span>
              </div>
              <p className="mt-1.5 text-xs leading-relaxed text-slate-400">
                {c.purpose}
              </p>
              <ul className="mt-4 space-y-1">
                {c.scripts.map((s) => (
                  <li key={s.file}>
                    <button
                      type="button"
                      onClick={() => open(s.file)}
                      className="group flex w-full items-start gap-2 rounded-md px-2 py-1.5 text-left transition-colors hover:bg-blue-500/5"
                      title={`Run ${s.file} in your browser`}
                    >
                      <span className="mt-0.5 font-mono text-[11px] font-semibold text-blue-300 group-hover:text-blue-200">
                        {s.file.split("_")[0]}
                      </span>
                      <span className="flex-1 text-[11px] leading-snug text-slate-300">
                        {s.what}
                      </span>
                      <Play
                        size={12}
                        className="mt-0.5 flex-none text-slate-600 transition-colors group-hover:text-blue-300"
                        aria-hidden
                      />
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </motion.section>
        ))}
      </div>
    </div>
  );
}
"""


def js_string(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def gen_tsx(registry: list[dict], clusters: dict[str, dict]) -> str:
    by_cluster: dict[str, list[dict]] = {cid: [] for cid in clusters}
    for r in registry:
        by_cluster[r["cluster"]].append(r)
    blocks = []
    for cid, meta in clusters.items():
        lines = [
            "  {",
            f"    title: {js_string(meta['title'])},",
            f"    purpose: {js_string(meta['purpose'])},",
            f"    accent: {js_string(meta['accent'])},",
            "    scripts: [",
        ]
        for r in by_cluster[cid]:
            lines.append(
                f"      {{ file: {js_string(r['script'] + '.py')},"
                f" what: {js_string(r['what_web'])} }},"
            )
        lines += ["    ],", "  },"]
        blocks.append("\n".join(lines))
    return TSX_HEADER + "\n".join(blocks) + "\n" + TSX_FOOTER


# --------------------------------------------------------------------------


def gen_suite(registry: list[dict]) -> str:
    return (
        "// GENERATED by verification/make_script_index.py -- do not edit.\n"
        "// Server-safe suite stats (single source: verification/run_all.py).\n"
        f"export const SCRIPT_TOTAL = {len(registry)};\n"
    )


def build() -> dict[Path, str]:
    registry = load_registry()
    clusters = load_clusters()
    errors = validate(registry, clusters)
    if errors:
        for e in errors:
            print(f"REGISTRY ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    return {
        TEX_TARGET: gen_tex(registry),
        TSX_TARGET: gen_tsx(registry, clusters),
        SUITE_TARGET: gen_suite(registry),
    }


def main() -> None:
    check_only = "--check" in sys.argv
    stale = []
    for target, content in build().items():
        if not target.exists() or target.read_text() != content:
            if check_only:
                stale.append(target)
            else:
                target.write_text(content)
                print(f"wrote {target.relative_to(ROOT)}")
    if check_only:
        if stale:
            for t in stale:
                print(f"STALE (re-run make_script_index.py): {t.relative_to(ROOT)}")
            sys.exit(1)
        print("script index up to date")


if __name__ == "__main__":
    main()
