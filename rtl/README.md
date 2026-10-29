# rtl

- `serializer.v` — 8:1→2:1 serializer reduction on the 500 MHz clock with a ÷4
  word clock (spec S1/S2; micro-architecture per DR-004). Lint:
  `verification/lint_rtl.sh`; bench: `verification/serializer/`; synthesis:
  `flow/serializer/`.
