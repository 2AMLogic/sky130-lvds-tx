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

exit "$fail"
