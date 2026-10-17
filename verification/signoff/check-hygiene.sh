#!/bin/sh
# Mechanical checks behind T1 item 10 (repo hygiene); run by
# `klt signoff --attest 10` from the repository root.
set -eu

fail=0

# The README must point at the spec issue (#2), not the stale #1.
if ! grep -q 'see issue #2' README.md; then
  echo "README.md: spec pointer must cite issue #2" >&2
  fail=1
fi
if grep -q 'see issue #1' README.md; then
  echo "README.md: stale spec pointer to issue #1" >&2
  fail=1
fi

# No package.json script may be a placeholder that prints and exits 0.
if grep -Eq "exit 0" package.json; then
  echo "package.json: a script exits 0 without running a check" >&2
  fail=1
fi

exit "$fail"
