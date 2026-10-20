# DR-003: Serializer ratio and forwarded-clock framing (8:1 DDR vs 7:1)

- **Status**: proposed
- **Date**: 2026-10-17
- **Author**: builder agent (issue #2)
- **Ratifies against / input to**: issue #2; `spec/target-spec.md` rows S1–S4, C1–C6
- **Supersedes**: none

## Context

Open question from the issue: 8:1 or 7:1 serialization, and which receiver
framing the forwarded clock should follow. The receiver is out of scope, so
the framing is a stated interface, not a verified link.

| | 8:1, DDR forwarded clock | 7:1, word-rate clock |
|---|---|---|
| Parallel word | 8 bits at 125 MHz (1 Gb/s) | 7 bits at 142.86 MHz |
| Forwarded clock | 500 MHz, 50 % duty, both edges sample (a `10101010` bit pattern at the bit rate) | 142.86 MHz with a 7-bit pattern that also marks the word boundary |
| Clock the transmitter needs from the PLL | 500 MHz (bit rate / 2) | 1 GHz bit clock (or 500 MHz DDR) plus a ÷7 word clock |
| Word boundary at the receiver | not carried by the clock; needs a training pattern or frame marker at a protocol layer (out of scope) | carried by the clock pattern |
| Receiver clock recovery | none: source-synchronous sampling with a phase-shifted clock | receiver PLL or DLL needed to multiply the word clock |
| Counter/divider | ÷4 of the 500 MHz clock: power-of-two | ÷7: odd divider, duty fix-up |
| Duty-cycle sensitivity | high: clock duty error is a bit-time error | lower |

## Decision

**8:1 with a DDR forwarded clock**, as the README draft states. The clock lane
is driven through the same serializer and driver path as the data lanes with a
fixed `10101010` word, so clock and data share delay and edge shape. The word
boundary is a protocol-layer matter this block does not carry: the spec states
that a training pattern or frame marker is needed by whatever receiver is used.
7:1 is the **stretch option** only (README: "7:1 option"), not designed for.

Proposed; ratifies with the PR.

## Alternatives considered

- **7:1 framing**: self-framing and the clock is slower, but the receiver
  needs a clock multiplier, the transmitter needs an odd divider, and the
  PLL must still produce 1 GHz or a 7× word multiple the sibling does not
  offer. Not chosen for the target; kept as the stretch.
- **Clock at the bit rate (1 GHz, SDR)**: doubles the clock requirement on the
  sibling PLL (further from its draft band) and doubles the clock-lane switching
  speed. Rejected.
- **No forwarded clock (embedded clock)**: needs clock recovery, a receiver
  topic; out of scope.

## Consequences

- The clock requirement on the PLL is **500 MHz at 50 ± 2.5 % duty** with a
  jitter budget (spec rows C1–C4). The DDR choice makes duty cycle a
  first-class budget item.
- Serializer reduction runs at 500 MHz on one clock with a ÷4 word counter;
  one-mux-level arithmetic closes with 27 % slack at the slow Liberty
  corner (spec S3), but not at the 1.5 Gb/s stretch.
- The frame-marker gap is a limitation of the interface, stated in the spec.

## Status notes

Proposed. Receiver framing is unverified by construction.
