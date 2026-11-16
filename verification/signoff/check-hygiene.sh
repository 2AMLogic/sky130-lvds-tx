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

# The routed serializer artifacts committed under flow/serializer/ must match
# the sha256 digests recorded in PNR.md's "Committed artifacts" table. That
# table is the only recorded binding of those bytes, so a perturbed or
# regenerated artifact must fail here rather than drift silently; a missing
# section, a missing row, or a malformed digest fails too.
pnr_doc=flow/serializer/PNR.md
if [ ! -f "$pnr_doc" ]; then
  echo "$pnr_doc: missing (cannot verify committed-artifact digests)" >&2
  exit 1
fi
for artifact in serializer_routed.gds serializer_routed.v serializer_routed.def serializer_routed.spef; do
  recorded=$(awk -v art="$artifact" '
    /^## Committed artifacts/ { insec = 1; next }
    insec && /^## / { insec = 0 }
    insec && /^[|]/ && index($0, "`" art "`") {
      n = split($0, cells, "|")
      for (i = 1; i <= n; i++) {
        h = cells[i]
        gsub(/[` ]/, "", h)
        if (h ~ /^[0-9a-f]+$/ && length(h) == 64) { print h; exit }
      }
    }' "$pnr_doc")
  if [ -z "$recorded" ]; then
    echo "$pnr_doc: no sha256 row for $artifact in ## Committed artifacts" >&2
    fail=1
    continue
  fi
  measured=$(sha256sum "flow/serializer/$artifact" 2>/dev/null | cut -d' ' -f1)
  if [ -z "$measured" ]; then
    echo "flow/serializer/$artifact: missing (recorded $recorded in $pnr_doc)" >&2
    fail=1
    continue
  fi
  if [ "$recorded" != "$measured" ]; then
    echo "flow/serializer/$artifact: sha256 $measured does not match the digest recorded in $pnr_doc ($recorded)" >&2
    fail=1
  fi
done

# The item-3 DRC deck provenance restated in verification/README.md's "Deck
# provenance" table must match the provenance.deck block of every committed
# item-3-drc-*.json envelope. The README restatement has drifted twice (#98's
# digital r2, #119's digital r3), so it is re-derived here rather than trusted:
# a missing section, a missing row, or a mismatched hash or released flag fails.
readme_doc=verification/README.md
if ! grep -q '^### Deck provenance' "$readme_doc"; then
  echo "$readme_doc: missing ### Deck provenance section (cannot verify item-3 DRC deck provenance)" >&2
  fail=1
else
  for envelope in verification/signoff/evidence/item-3-drc-*.json; do
    if [ ! -f "$envelope" ]; then
      echo "verification/signoff/evidence: no item-3-drc-*.json envelopes found" >&2
      fail=1
      continue
    fi
    report=$(basename "$envelope")
    row=$(awk -v rep='`'"$report"'`' '
      /^### Deck provenance/ { insec = 1; next }
      insec && /^#/ { insec = 0 }
      insec && /^[|]/ && index($0, rep) { print; exit }
    ' "$readme_doc")
    if [ -z "$row" ]; then
      echo "$readme_doc: no ### Deck provenance row for $report" >&2
      fail=1
      continue
    fi
    recorded_hash=$(printf '%s\n' "$row" | awk -F'|' '{
      for (i = 1; i <= NF; i++) {
        h = $i
        gsub(/[` ]/, "", h)
        sub(/^sha256:/, "", h)
        if (h ~ /^[0-9a-f]+$/ && length(h) == 64) { print h; exit }
      }
    }')
    recorded_released=$(printf '%s\n' "$row" | awk -F'|' '{
      for (i = 1; i <= NF; i++) {
        v = $i
        gsub(/[` ]/, "", v)
        if (v == "true" || v == "false") { print v; exit }
      }
    }')
    if [ -z "$recorded_hash" ]; then
      echo "$readme_doc: no deck sha256 cell in the ### Deck provenance row for $report" >&2
      fail=1
      continue
    fi
    if [ -z "$recorded_released" ]; then
      echo "$readme_doc: no released cell in the ### Deck provenance row for $report" >&2
      fail=1
      continue
    fi
    deck_hash=$(python3 -c '
import json, sys
try:
    with open(sys.argv[1]) as f:
        print(json.load(f)["provenance"]["deck"]["content_hash"])
except Exception:
    pass
' "$envelope" 2>/dev/null || true)
    deck_released=$(python3 -c '
import json, sys
try:
    with open(sys.argv[1]) as f:
        d = json.load(f)["provenance"]["deck"]["released"]
        print("true" if d else "false")
except Exception:
    pass
' "$envelope" 2>/dev/null || true)
    if [ -z "$deck_hash" ] || [ -z "$deck_released" ]; then
      echo "$envelope: unreadable provenance.deck content_hash/released" >&2
      fail=1
      continue
    fi
    deck_hash=${deck_hash#sha256:}
    if [ "$recorded_hash" != "$deck_hash" ]; then
      echo "$envelope: deck content_hash sha256:$deck_hash does not match the digest recorded in $readme_doc ($recorded_hash)" >&2
      fail=1
    fi
    if [ "$recorded_released" != "$deck_released" ]; then
      echo "$envelope: deck released $deck_released does not match the value recorded in $readme_doc ($recorded_released)" >&2
      fail=1
    fi
  done
fi

exit "$fail"
