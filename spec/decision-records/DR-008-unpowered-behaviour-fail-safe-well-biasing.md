# DR-008: Unpowered behaviour (P4) is a joint pad-and-driver requirement, met by fail-safe well biasing

- **Status**: proposed; carries an **operator ruling** (below)
- **Date**: 2026-10-20
- **Author**: independent spec reviewer (PR #9), recording the operator's ruling
- **Ratifies against / input to**: `spec/target-spec.md` rows P4, P4a, P4b, D4, E8; amends `DR-001` (deciding observation) and `DR-002` (device list and consequences)
- **Supersedes**: none (amends `DR-001` and `DR-002`; neither is replaced)

## Context

`DR-001` rejects the stock `sky130_ef_io__analog_esd_pad` as the baseline
because its pad-to-VDDIO diode back-powers an unpowered chip when a partner
drives the pad (spec row P4). The independent review of PR #9 found that the
driver of `DR-002` carries the same path on its own: the top PMOS switches
(`pfet_01v8`) have their drains at the pad, and with VCCD = VDDIO = 0 V their
p+ drain-to-n-well junctions, wells tied to a 0 V rail, conduct from
V_pad ≈ 0.6 V exactly as the stock diode would. Removing the diode is
therefore necessary for P4 but not sufficient, and the review put the choice
to the operator:

- (a) keep P4 as a target and require a fail-safe driver, keeping the custom
  pad with its rationale intact;
- (b) move P4 to its fallback column and keep the custom pad for seam
  learning;
- (c) move P4 to its fallback column and take the stock pad as the baseline.

## Ruling

**Operator ruling (rjwalters, 2026-10-20, attended `/fleet:decide`, question
3, answer 2): keep P4** — no back-power while unpowered — **as a joint pad and
driver requirement, met with fail-safe well biasing, and then ratify.** The
`DR-001` custom-pad decision stands on its original argument; `DR-002` gains
the fail-safe mechanism below as part of the driver it specifies. Reviewer
calls 2–6 of the same review stay recommendations, recorded in
`target-spec.md` under *Open items*, not rulings.

## Decision (the mechanism, at spec level)

The pad-facing devices are the two top PMOS switches of each H-bridge (drains
at the pad) and, through them, the PMOS current source; the bottom NMOS
switches' n+ drains sit in the grounded p-substrate and are reverse-biased for
any positive pad voltage, so they need no measure beyond a gate held low.

1. **Floating n-well for the pad-facing PMOS switches.** The n-well of each
   top switch pair is not tied to a rail. It is tied to **max(VCCD, V_pad)**
   through two small well-switch PMOS devices: one from VCCD to the well,
   gated by the pad; one from the pad to the well, gated by VCCD. Powered,
   the well sits at VCCD (1.62–1.98 V) and the switch sees a body bias of at
   most a few hundred millivolts, inside the 1.8 V device's normal operating
   region. Unpowered, the well follows the pad, so the drain-to-well junction
   never forward-biases. The well-to-substrate junction is reverse-biased in
   both cases. The reference is VCCD rather than VDDIO on purpose: a well at
   3.3 V would put ~1.8 V of reverse body bias on thin-oxide devices in
   normal operation, which is outside what `DR-002`'s ≤ 1.98 V terminal rule
   intends for the switch devices. (A design record may choose another
   reference if it shows the body-bias stress is acceptable; the spec
   requirement is the behaviour in rows P4–P4b, not the reference node.)
2. **Gate tracking for the switch gates.** When VCCD = 0 V the predriver
   output is undefined and would otherwise leave a PMOS switch on with its
   gate at 0 V. A gate-tracking PMOS from the well to each top-switch gate,
   gated by VCCD, pulls the gate to the well potential when VCCD is absent,
   so the switch is off and the pad-to-source-node path is open. Powered,
   that device is off (its gate is at VCCD, above the well by at most the
   well-switch drop) and does not load the predriver.
3. **Device class of the auxiliary devices.** The well-switch and
   gate-tracking devices are `pfet_g5v0d10v5` (thick oxide): in the 2.4 V
   power-off test their gate-to-source voltage reaches 2.4 V, above the
   1.98 V thin-oxide limit of D4. They carry no signal current and can be
   minimum-size, so their speed does not matter.
4. **The current source needs no measure of its own.** Its drain is the
   switch source node, not the pad; with both switches off that node has no
   DC path from the pad, and the device's own n-well is at VDDIO = 0 V with
   its drain floating.
5. **The ESD network** stays as `DR-001` decides: to VSSIO only. Its reverse
   leakage (diode) and off-state leakage (snapback NMOS) are inside the P4
   limit, together with the well-switch and gate-tracking devices'
   subthreshold leakage and the thin-oxide switches' off leakage.
6. **Budget.** The well-switch drains add to the pad node; they count under
   P1's *LVDS driver drains ≤ 0.5 pF* allocation, not as new budget. The
   floating well is per switch pair, so each lane's two top switches share
   one well.

The technique is the standard fail-safe / "floating-well" I/O method
(Pelgrom and Dijkstra, "A 3/5 V compatible I/O buffer", IEEE J. Solid-State
Circuits, vol. 30, no. 7, 1995, is the public reference the reviewer knows
for it; cited from memory, not re-read for this record). The leakage limit's
public anchor is the SN65LVDS31 datasheet (TI SLLS261N §7.5): I_O(OFF) ±1 µA
(SN65) to ±4 µA (SN55) at VCC = 0 V, V_O = 2.4 V. Whether TIA/EIA-644 itself
sets a power-off limit was **not verified** (the standard's text is
licensed); the P4 figure of 20 µA is this repo's own, loose against the
datasheets by 5–20×.

## Verification (rows added to `target-spec.md`)

| Row | What | Limit | Conditions |
|---|---|---|---|
| P4 | Pad current, unpowered | ≤ ±20 µA per pad | VCCD = VDDIO = 0 V; both pads of a pair swept 0–2.4 V together and in the partner's differential pattern (one pad at 0.9–1.6 V, the other at its complement about 1.25 V); 125 °C and −40 °C; all five process corners; **driver and pad cell attached** |
| P4a | No forward-biased junction | every p+/n-well and n-well/p-substrate junction of the pad-facing devices (switches, well-switch, gate-tracking, ESD diode) at ≤ 0.3 V forward, i.e. reverse-biased or below conduction, reported per device | same sweep |
| P4b | Well and gate tracking | the floating well within 0.3 V of max(VCCD, V_pad) over the sweep; every top-switch gate within 0.3 V of its well when VCCD = 0 V; every thin-oxide terminal pair ≤ 1.98 V in the unpowered state; a 1 ms ramp of VCCD and VDDIO from 0 to nominal and back, with the pad held at 1.25 V, shows no pad-current excursion above ±1 mA | same corners, DC sweep plus one ramp transient |

These rows are measurable by DC and transient simulation of the driver with
the pad cell, then post-layout; silicon confirms them in `measurements/`. They
are **deterministic** over the process grid; no Monte Carlo is needed because
the limits are leakage bounds, not matching.

## Alternatives considered

- **Move P4 to the fallback column** (options b and c above): rejected by the
  ruling. The record keeps the reasoning that would have supported it — the
  custom pad's remaining argument without P4 is seam learning and capacitance
  margin — so that a later reversal is a decision, not a rediscovery.
- **Series isolation element** between pad and switch drains (a thick-oxide
  pass device): keeps the switches' wells grounded but adds series resistance
  and capacitance in the 1 Gb/s path and a second device class at the pad.
  Rejected for the baseline; allowed as the "equivalent the design justifies"
  if the floating well proves unworkable in layout.
- **Well tied to max(VDDIO, V_pad)**: the usual textbook form; rejected here
  because the pad-facing switches are 1.8 V devices and a 3.3 V well would
  reverse-bias their bodies by ~1.8 V in normal operation (item 1 above).
- **Thick-oxide switches, so the well may sit at VDDIO**: this is `DR-002`'s
  rejected "3.3 V switches with level shifters" alternative; speed, not
  stress, rules it out.

## Consequences

- `DR-002`'s device list gains the well-switch and gate-tracking
  `pfet_g5v0d10v5` devices; D4 names them; E8's disabled-state check and P4's
  unpowered check are both run on the same netlist.
- `DR-001`'s custom-pad decision keeps its deciding argument, now stated as
  one half of a joint requirement.
- The floating well's capacitance and the auxiliary devices' leakage become
  part of the T1 evidence (issue #6); a miss on P4–P4b is recorded as a miss,
  and a change to these rows is a new decision record.
- Nothing here touches the clock, serializer or low-swing records.

## Status notes

Proposed; records the operator's ruling of 2026-10-20 and ratifies with the
PR. The mechanism is specified by behaviour (rows P4–P4b) and a reference
implementation; the design records may substitute an equivalent that meets
the same rows, with the body-bias justification above.
