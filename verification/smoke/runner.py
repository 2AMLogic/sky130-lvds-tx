#!/usr/bin/env python3
"""Cold-start runner for the smoke bench; template for later benches.

Runs `test_smoke.py` under Icarus Verilog via cocotb's Python runner:

  - good leg: `smoke.v` must pass every test.
  - negative control: the *same, unmodified* test module against
    `negative_control/smoke_broken.v` must FAIL; a bench that has never
    failed is not known to be able to.

Writes a JSON result file (per-test pass/fail for both legs, seed, tool
versions, commit) and exits 0 only if both legs behave as expected.

    pip install -r requirements.txt
    python3 verification/smoke/runner.py [--out results/smoke.json]

Later benches reuse `run_bench()` rather than copying this file.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import random
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent


def _version(cmd: list[str]) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=False).stdout
        return out.splitlines()[0].strip() if out else "unknown"
    except OSError:
        return "unknown"


def _commit() -> str:
    try:
        r = subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=False,
        )
        return r.stdout.strip() or "unknown"
    except OSError:
        return "unknown"


def _tests(results_xml: Path) -> list[dict]:
    tests = []
    for case in ET.parse(results_xml).getroot().iter("testcase"):
        failed = case.find("failure") is not None or case.find("error") is not None
        tests.append({"name": case.get("name"), "passed": not failed})
    return tests


def run_leg(source: Path, build_dir: Path, toplevel: str, test_module: str,
            test_dir: Path, seed: int) -> list[dict]:
    from cocotb_tools.runner import get_runner

    runner = get_runner("icarus")
    runner.build(
        verilog_sources=[source],
        hdl_toplevel=toplevel,
        build_dir=build_dir,
        always=True,
        build_args=["-g2005"],  # Verilog-2005, no vendor extensions
        timescale=("1ns", "1ps"),
    )
    results_xml = runner.test(
        test_module=test_module,
        hdl_toplevel=toplevel,
        build_dir=build_dir,
        test_dir=test_dir,
        seed=seed,
    )
    return _tests(Path(results_xml))


def run_bench(*, bench_dir: Path, good: Path, broken: Path, toplevel: str,
              test_module: str, out: Path, good_only: bool = False,
              broken_only: bool = False) -> int:
    """Run both legs, write `out`, return the process exit status."""
    seed = int(os.environ.get("COCOTB_RANDOM_SEED", random.randrange(2**31)))
    result: dict = {
        "bench": bench_dir.name,
        "commit": _commit(),
        "seed": seed,
        "tools": {
            "python": platform.python_version(),
            "cocotb": _cocotb_version(),
            "iverilog": _version(["iverilog", "-V"]),
        },
        "legs": {},
    }
    ok = True
    if not broken_only:
        tests = run_leg(good, bench_dir / "sim_build" / "good", toplevel,
                        test_module, bench_dir, seed)
        passed = bool(tests) and all(t["passed"] for t in tests)
        result["legs"]["good"] = {"tests": tests, "as_expected": passed}
        print(f"good DUT: {sum(t['passed'] for t in tests)}/{len(tests)} passed")
        if not passed:
            print("FAIL: the real DUT must pass every test.")
            ok = False
    if not good_only:
        tests = run_leg(broken, bench_dir / "sim_build" / "broken", toplevel,
                        test_module, bench_dir, seed)
        failed = any(not t["passed"] for t in tests)
        result["legs"]["negative_control"] = {"tests": tests, "as_expected": failed}
        print(f"negative control: {sum(not t['passed'] for t in tests)}/{len(tests)} failed")
        if not failed:
            print("FAIL: negative control did not fail -- this bench is not known "
                  "to be able to fail.")
            ok = False
    result["overall"] = "PASS" if ok else "FAIL"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(f"result file: {out}")
    print("OVERALL:", result["overall"])
    return 0 if ok else 1


def _cocotb_version() -> str:
    import cocotb
    return cocotb.__version__


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--good-only", action="store_true")
    parser.add_argument("--broken-only", action="store_true")
    parser.add_argument("--out", type=Path, default=HERE / "results" / "smoke.json",
                        help="result JSON path (default: %(default)s, gitignored)")
    args = parser.parse_args()
    if args.good_only and args.broken_only:
        parser.error("--good-only and --broken-only are mutually exclusive")
    if shutil.which("iverilog") is None:
        print("error: iverilog not found on PATH (apt install iverilog)", file=sys.stderr)
        return 2
    try:
        import cocotb  # noqa: F401
    except ImportError:
        print("error: cocotb not installed (pip install -r requirements.txt)",
              file=sys.stderr)
        return 2
    return run_bench(
        bench_dir=HERE, good=HERE / "smoke.v",
        broken=HERE / "negative_control" / "smoke_broken.v",
        toplevel="smoke", test_module="test_smoke", out=args.out,
        good_only=args.good_only, broken_only=args.broken_only,
    )


if __name__ == "__main__":
    sys.exit(main())
