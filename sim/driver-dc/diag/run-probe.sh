#!/usr/bin/env bash
# Run one of the raw one-corner diagnostic decks (probe-*.cir) without a
# machine-specific path baked into the deck.
#
#   sim/driver-dc/diag/run-probe.sh probe-fs125.cir
#   DRIVER_SPICE=/tmp/driver-pre-resize.spice sim/driver-dc/diag/run-probe.sh probe-ssm40.cir
#
# PDK_ROOT         PDK root holding sky130A/ (default: ~/.ciel, per docs/environment.md)
# DRIVER_SPICE     driver netlist to probe (default: design/driver/driver.spice, the
#                  CURRENT sizing). The numbers quoted in RECORD.md as "old sizing" are
#                  from the post-#177, pre-resize driver; reproduce them with:
#                    git show 7be1ca4:design/driver/driver.spice > /tmp/driver-pre-resize.spice
#                    DRIVER_SPICE=/tmp/driver-pre-resize.spice ...
# The deck is rendered into a temp dir; nothing is written into the repo.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
repo="$(cd "$here/../../.." && pwd -P)"
deck="${1:?usage: run-probe.sh <probe-deck.cir>}"
[ -f "$here/$deck" ] || deck="$(basename "$deck")"
lib="${PDK_ROOT:-$HOME/.ciel}/sky130A/libs.tech/ngspice/sky130.lib.spice"
[ -f "$lib" ] || { echo "run-probe.sh: PDK library not found: $lib (set PDK_ROOT)" >&2; exit 1; }
tmp="$(mktemp -d "${TMPDIR:-/tmp}/probe.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT
sed -e "s#__SKY130_LIB__#$lib#" \
    -e "s#__DRIVER_SPICE__#${DRIVER_SPICE:-$repo/design/driver/driver.spice}#" \
    -e "s#__PAD_CELL_SPICE__#$repo/design/pad_cell/pad_cell.spice#" \
    "$here/$deck" > "$tmp/$deck"
# wnflag must be set before the netlist is parsed (the bench does it through
# options.ngspice_init); a `set` inside .control is too late, and without it the
# sky130 BSIM4 cards abort with "Vsat ... is not positive".
printf 'set wnflag=1\nset num_threads=1\n' > "$tmp/.spiceinit"
cd "$tmp" && ngspice -b "$deck"
