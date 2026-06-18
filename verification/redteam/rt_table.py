"""Aggregate the five Red Team targets into Alessandro's red-team table.

Columns (his spec):  claim | assumptions | test method | pass/fail | residual risk.

Running this module executes the five `rt_*` stress tests, collects each
module-level REPORT, prints the narrow per-target table, and writes a plain-text
artifact `redteam_table.txt` that the LaTeX note `tfpt_5_redteam.tex` mirrors.
"""
import os
import rt_A_e8net
import rt_B_pascal
import rt_C_kc3
import rt_D_upoint
import rt_E_vgeo
import rt_F_qft4d

MODULES = [rt_A_e8net, rt_B_pascal, rt_C_kc3, rt_D_upoint, rt_E_vgeo, rt_F_qft4d]
ARTIFACT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "redteam_table.txt")


def collect(run_first=True):
    """Run the targets (if asked) and return (reports, total_failed_checks)."""
    reports, fails = [], 0
    for m in MODULES:
        if run_first:
            fails += m.run()
            print()
        reports.append(m.REPORT)
    return reports, fails


def render(reports):
    lines = []
    bar = "=" * 78
    lines.append(bar)
    lines.append("  TFPT RED TEAM / STRESS TEST -- summary table")
    lines.append("  (purpose: try to BREAK the reductions; verdict carries the honest status)")
    lines.append(bar)
    for r in reports:
        lines.append("")
        lines.append(f"  Target {r['target']}   [STATUS: {r['status']}]")
        lines.append(f"    claim    : {r['claim']}")
        lines.append(f"    assume   : {r['assumptions']}")
        lines.append(f"    works    : {r['works']}")
        lines.append(f"    fails    : {r['fails']}")
        lines.append(f"    verdict  : {r['verdict']}")
        lines.append(f"    residual : {r['residual']}")
    lines.append("")
    lines.append(bar)
    lines.append("  STATUS MATRIX")
    for r in reports:
        lines.append(f"    {r['target']}  {r['status']:22s}  {r['claim']}")
    lines.append(bar)
    return "\n".join(lines)


def main():
    reports, fails = collect(run_first=True)
    table = render(reports)
    print(table)
    with open(ARTIFACT, "w", encoding="utf-8") as fh:
        fh.write(table + "\n")
    print(f"\n[wrote {os.path.relpath(ARTIFACT)}]")
    if fails:
        print(f"\n{fails} adversarial check(s) could not be confirmed -- investigate.")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
