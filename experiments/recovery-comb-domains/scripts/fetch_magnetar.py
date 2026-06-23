#!/usr/bin/env python3
"""Thin wrapper: fetch/normalise real magnetar light curves for the A1 recovery-comb channel.

All logic lives in ``tfpt_combdomains.fetch`` (so the CLI subcommand ``tfpt-combdomains
fetch-magnetar`` and this script share one implementation). Run from anywhere, e.g.::

    python scripts/fetch_magnetar.py --list
    python scripts/fetch_magnetar.py --swift
    python scripts/fetch_magnetar.py --normalize raw_lc.qdp --source Swift_J1822.3-1606 \
        --time-col 0 --flux-col 1 --err-col 2 --mjd
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tfpt_combdomains.fetch import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
