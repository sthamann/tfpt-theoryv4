"""Run the whole TFPT Red Team / Stress Test layer.

    $ cd verification/redteam && python run_redteam.py

Runs the five adversarial targets (A-E), prints each protocol, then the summary
table and writes `redteam_table.txt`.  Exit code = number of FAILED adversarial
checks: a non-zero exit means a stress test could not confirm its own
counterexample/firewall (a real problem to investigate), NOT that TFPT is
"wrong".  The honest per-target outcome lives in the STATUS column of the table
(SURVIVES / SURVIVES (narrowed) / REDUCED, not closed / BROKEN).
"""
import rt_table


def main():
    code = rt_table.main()
    print("\n" + "=" * 78)
    print("  RED TEAM COMPLETE -- read the STATUS column above for each target's verdict.")
    print("=" * 78)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
