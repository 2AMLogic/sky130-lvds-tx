#!/usr/bin/env python3
"""Runner for the serializer bench; reuses the smoke bench's `run_bench()`.

  - good leg: `rtl/serializer.v` must pass every test.
  - negative control: the same, unmodified test module against
    `negative_control/serializer_broken.v` (counter wraps one cycle late)
    must FAIL.

    pip install -r requirements.txt
    python3 verification/serializer/runner.py [--out results/serializer.json]
"""

from __future__ import annotations

import argparse
import importlib.util
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

_spec = importlib.util.spec_from_file_location(
    "smoke_runner", REPO / "verification" / "smoke" / "runner.py")
_smoke = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_smoke)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--good-only", action="store_true")
    parser.add_argument("--broken-only", action="store_true")
    parser.add_argument("--out", type=Path, default=HERE / "results" / "serializer.json",
                        help="result JSON path (default: %(default)s, gitignored)")
    args = parser.parse_args()
    if args.good_only and args.broken_only:
        parser.error("--good-only and --broken-only are mutually exclusive")
    if shutil.which("iverilog") is None:
        print("error: iverilog not found on PATH", file=sys.stderr)
        return 2
    return _smoke.run_bench(
        bench_dir=HERE, good=REPO / "rtl" / "serializer.v",
        broken=HERE / "negative_control" / "serializer_broken.v",
        toplevel="serializer", test_module="test_serializer", out=args.out,
        good_only=args.good_only, broken_only=args.broken_only,
    )


if __name__ == "__main__":
    sys.exit(main())
