#!/usr/bin/env python3
"""Hermetic check that reuse.lock.json still describes the vendored tree.

For every `mode: vendored` import entry the script re-computes sha256 of the
committed local file and compares it to the recorded `local_sha256`, and
verifies the entry's `diverged:` decision-record path exists. Exits non-zero
on any mismatch, naming the file and both hashes, so a vendored file can no
longer drift (or lose its justification record) without a CI signal.

Needs no network, no simulators, no third-party packages:

    python3 -I scripts/check_reuse_lock.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LOCK_PATH = REPO_ROOT / "reuse.lock.json"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if not LOCK_PATH.is_file():
        print(f"FATAL: {LOCK_PATH.relative_to(REPO_ROOT)} not found", file=sys.stderr)
        return 2
    try:
        lock = json.loads(LOCK_PATH.read_text())
    except json.JSONDecodeError as exc:
        print(f"FATAL: {LOCK_PATH.relative_to(REPO_ROOT)} is not valid JSON: {exc}", file=sys.stderr)
        return 2

    failures = 0
    checked = 0
    for imp in lock.get("imports", []):
        if imp.get("mode") != "vendored":
            continue
        for entry in imp.get("files", []):
            checked += 1
            local = entry.get("local")
            recorded = entry.get("local_sha256")
            diverged = entry.get("diverged")

            if local is None or recorded is None:
                failures += 1
                print(f"INVALID: vendored entry missing 'local' or 'local_sha256': {entry}")
                continue

            local_path = REPO_ROOT / local
            if not local_path.is_file():
                failures += 1
                print(f"MISSING: {local} (lock records it as a vendored local file)")
            else:
                computed = _sha256(local_path)
                if computed == recorded:
                    print(f"ok: {local}")
                else:
                    failures += 1
                    print(f"MISMATCH: {local}")
                    print(f"  expected local_sha256: {recorded}")
                    print(f"  computed (sha256 of committed file): {computed}")

            if diverged is None:
                failures += 1
                print(f"INVALID: {local} has no 'diverged' decision record in the lock")
            elif not (REPO_ROOT / diverged).is_file():
                failures += 1
                print(f"MISSING: {diverged} (diverged: pointer for {local})")

    # A gate that checks nothing must not look like one that passed: an
    # imports[] entry removed, or a mode flipped away from `vendored`, would
    # otherwise exit 0 vacuously.
    if checked == 0:
        failures += 1
        print("VACUOUS: no vendored entries found in reuse.lock.json - nothing was checked")

    print(f"reuse.lock: {checked} vendored entr{'y' if checked == 1 else 'ies'} checked, "
          f"{failures} failure{'s' if failures != 1 else ''}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
