#!/bin/sh
# Render the signoff verdict and require it to be byte-identical to the
# committed record. Shared by CI (.github/workflows/signoff.yml) and the local
# `pnpm check:signoff`, so there is one comparison to maintain. Run from the
# repository root with `klt` on PATH (e.g. under `uvx --from klayout-tools==X klt`).
set -u

manifest=manifests/sky130-lvds-tx.json
record=manifests/sky130-lvds-tx.signoff.json
# Overridable so a negative control can compare against a scratch copy.
record=${SIGNOFF_RECORD:-$record}

fresh=$(mktemp) || exit 1
trap 'rm -f "$fresh" "$fresh.a" "$fresh.b"' EXIT
trap 'exit 1' HUP INT TERM

rc=0
klt signoff --manifest "$manifest" --format json > "$fresh" || rc=$?
# 0 = every T1 item met; 3 = grader ran clean, some item unmet.
# Anything else is a hard error.
if [ "$rc" -ne 0 ] && [ "$rc" -ne 3 ]; then
  echo "::error::klt signoff exited $rc (expected 0 or 3)"
  exit 1
fi

if ! cmp -s "$fresh" "$record"; then
  echo "::error::Fresh klt signoff output differs from $record - the committed verdict is stale."
  echo "Regenerate it in this PR (see manifests/README.md)."
  python3 -m json.tool "$fresh" > "$fresh.a" 2>/dev/null || cp "$fresh" "$fresh.a"
  python3 -m json.tool "$record" > "$fresh.b" 2>/dev/null || cp "$record" "$fresh.b"
  diff "$fresh.a" "$fresh.b"
  rm -f "$fresh.a" "$fresh.b"
  exit 1
fi
echo "Committed signoff record is fresh."
