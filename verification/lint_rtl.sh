#!/usr/bin/env bash
# Lint rtl/*.v with Verilator. Vacuous (exit 0) while rtl/ has no .v files.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
shopt -s nullglob
files=("$root"/rtl/*.v)
if [ ${#files[@]} -eq 0 ]; then
  echo "lint_rtl: no RTL yet (rtl/ has no .v files); nothing to lint"
  exit 0
fi
command -v verilator >/dev/null || { echo "error: verilator not found on PATH" >&2; exit 2; }
verilator --lint-only -Wall "${files[@]}"
echo "lint_rtl: ${#files[@]} file(s) clean"
