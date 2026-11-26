# Work Log

Chronological record of merged PRs and closed issues. Maintained by the Guide role.

### 2026-11-19

- **PR #117**: docs(spec): state the decision-record placement rule semantically
- **Issue #103** (closed): spec/ has two decision-record directories under a rule its README states wrongly

### 2026-11-18

- **PR #160**: ci: add merge_group trigger to ci.yml and signoff.yml
- **Issue #159** (closed): Merge queue: add the merge_group trigger to the required-check workflow(s)

### 2026-11-17

- **PR #155**: chore(loom): resync installed Loom to v0.19.1306

### 2026-11-16

- **PR #95**: docs: roadmap as of 2026-11-13
- **PR #148**: chore(loom): resync installed Loom to v0.19.1302
- **PR #150**: fix: existence-check in_tree[].decision pointers in the reuse-lock gate
- **Issue #146** (closed): reuse.lock.json's in_tree[].decision pointers are not existence-checked by the new reuse-lock gate
- **PR #147**: fix(verification): bind item-3 DRC deck provenance to its envelopes
- **Issue #145** (closed): verification/README.md item-3 deck provenance: analog r3 hash mislabeled and 'released: false' stale
- **PR #144**: Re-close the digital physical flow against the r2 serializer netlist
- **Issue #119** (closed): Re-close the digital physical flow (routed GDS + items 2/3/4/11 digital) against #115's regenerated serializer netlist
- **PR #142**: ci: gate reuse.lock local_sha256 drift; refresh vendored setup-env hash; re-derive 0002 edit list
- **Issue #141** (closed): reuse.lock.json's local_sha256 for the vendored scripts/setup-env.sh is stale, and 0002's edit list no longer covers the file's divergences
- **PR #140**: env: provision a dedicated .venv-pnr for place-and-route on a klayout 0.30.13 pin
- **Issue #120** (closed): Module pin for the digital P&R re-closure (#119): split venv vs upstream vs full 0.30.x re-pin

### 2026-11-15

- **PR #137**: docs: scope sim provenance-correction clause to pinned vs addendum blocks
- **Issue #136** (closed): sim/README.md provenance convention: 'corrected by annotation, not rewrite' is stated unconditionally, but the current addendum block may be edited in place
- **PR #135**: docs(sim): correct unpowered-pad klayout provenance figures; state canonical-figure convention
- **PR #132**: sim(unpowered-pad): re-run the grid against the ESD-fixed pad cell (cd0c89a)
- **PR #131**: docs: state WORK_PLAN snapshot semantics in header, name generation-time recovery
- **PR #129**: sim(driver-dc): instantiate the corrected pad_cell and re-grade E1/E2 at the pad node
- **PR #127**: fix: remove unused SLOT_DEPTH_UM constant from pad generator
- **PR #126**: docs: cite klayout-tools#5780 cause beside #5798 in TMPDIR friction record
- **PR #123**: docs(signoff): re-record serializer P&R artifact digests and enforce the binding
- **PR #122**: docs: disclose klt TMPDIR-length yosys deadlock and inventory PATH-pin rationale in the verification record
- **PR #121**: fix(signoff): regenerate the serializer netlist under the pinned yosys; re-close item 1 digital as r2 (stacked on #112)
- **PR #118**: docs(layout): state the pad-seam deferral reason from live status, not issue #24
- **PR #107**: sim: add unpowered-pad DC bench for the fail-safe well biasing
- **PR #102**: sim: add driver DC bench recording V_OD and V_OS over the G75 grid
- **Issue #134** (closed): sim/unpowered-pad/RECORD.md: recorded klayout client version disagrees with the committed reports (both blocks)
- **Issue #128** (closed): WORK_PLAN.md's generated region carries no generated-at timestamp, so a stale snapshot reads as current truth
- **Issue #125** (closed): Re-run sim/unpowered-pad bench against the ESD-fixed pad cell (cd0c89a)
- **Issue #124** (closed): verification/README.md: cross-reference klayout-tools#5780 (traced cause) alongside #5798 for the TMPDIR-length yosys deadlock
- **Issue #116** (closed): driver-dc bench: re-run the G75 grid with the corrected pad_cell instantiated
- **Issue #115** (closed): Re-close the digital flow under the pinned toolchain (serializer_synth.v is not pin-reproducible; item-1 digital envelope cannot be regenerated under klt 0.9.1)
- **Issue #113** (closed): flow/serializer/PNR.md: restore the committed-artifact hash table — the routed SPEF is now pinned by nothing
- **Issue #110** (closed): layout: the pad-seam deferral row still cites closed #24 as its live reason
- **Issue #109** (closed): layout: SLOT_DEPTH_UM in gen_driver_pad.py is defined and never read
- **Issue #104** (closed): layout: the driver-pad GDS freshness gate fails because the klt pin is stale and the klayout binary is unpinned
- **Issue #97** (closed): sim: unpowered-pad DC bench for the fail-safe well biasing (spec rows P4, P4a, P4b; DR-008)
- **Issue #96** (closed): sim: driver DC bench for V_OD and V_OS (spec rows E1, E2) across the G75 grid

### 2026-11-14

- **PR #111**: fix(digital): close serializer setup timing at the in-spec ss corners
- **PR #108**: fix(pad_cell): size the ESD diode junction from the P1 budget, not 400 m²
- **PR #105**: refactor: generate the ESD clamp through the shared klt_gen wrapper
- **Issue #100** (closed): design: pad_cell ESD diode area is 400x the model default and shunts 107 mA at 1.25 V DC
- **Issue #99** (closed): Remove gen_esd(): klt_gen() is the same klt gen wrapper, generalised
- **Issue #98** (closed): Serializer S3: close setup timing at the 1.60 V and 1.76 V ss corners with 10 % clock uncertainty

### 2026-11-12

- **PR #91**: Bump Repo Skills 0.25.10 -> 0.26.1

### 2026-11-07

- **PR #87**: Bump Repo Skills 0.25.1 -> 0.25.10

### 2026-11-06

- **PR #85**: refactor(verification): fold run_bench into serializer runner and remove smoke dir
- **Issue #84** (closed): Relocate verification/smoke runner into the serializer bench and drop the importlib shim
- **PR #83**: docs: record post-route serializer STA at all hd corners (S3 not met)
- **Issue #82** (closed): Serializer spec S3: post-route klt sta at every sky130_fd_sc_hd corner with 10 % uncertainty

### 2026-11-02

- **PR #78**: feat: add analog ERC well/substrate ties and regenerate item 11 analog evidence
- **Issue #26** (closed): T1 item 11 (power delivery, structural): klt erc supply specs for VCCD/VDDIO/VSSIO across both partitions
- **Issue #74** (closed): Route VCCD/VDDIO/VSSIO across pad frame, driver and predriver in driver_pad layout
- **PR #75**: feat: strap supplies across pad frame, driver, ddr_mux and predriver
- **PR #73**: feat: add klt erc supply specs and item 11 evidence (digital met, analog unmet)
- **Issue #25** (closed): T1 item 4 (LVS clean): LVS of the analog cells against their schematics and of the serializer with power_connectivity
- **PR #72**: feat: cite klt lvs reports for T1 item 4 on both partitions
- **Issue #49** (closed): T1 item 4 prerequisite (digital): diagnose and fix the VNB power.inconsistent_pin_net finding in the routed serializer
- **PR #71**: docs: record digital LVS r2 report with power_connectivity match

### 2026-11-01

- **PR #69**: Bump Repo Skills 0.24.7 -> 0.25.1

### 2026-10-31

- **PR #67**: chore(verification): drop dead main() from shared run_bench() host
- **Issue #66** (closed): Trim dead main() and stale docstring from verification/smoke/runner.py
- **PR #64**: chore(verification): retire smoke placeholder bench, cold start runs serializer bench
- **Issue #30** (closed): Retire placeholder smoke bench and point pnpm test at the serializer bench
- **PR #61**: build: run serializer bench from pnpm test and drop duplicate check:all

### 2026-10-29

- **PR #32**: feat(signoff): attest T1 item 9 with a cold-start wrapper and pinned inventory
- **Issue #27** (closed): T1 item 9 (testbenches shipped): item 9 inventories and attestations for both partitions

### 2026-10-28

- **PR #59**: chore: re-run analog DRC on the routed GDS and cite it as 3.analog (r3)
- **Issue #58** (closed): T1 item 3 (DRC clean, analog): re-run klt drc on the routed driver/pad GDS — the cited report is bound to the pre-#48 stream
- **PR #57**: chore: retire superseded flow/pdk-smoke stand-in counter flow
- **Issue #39** (closed): Remove flow/pdk-smoke: superseded stand-in counter flow
- **Issue #24** (closed): T1 item 3 (DRC clean): klt drc on the driver/pad and serializer layouts with coverage disclosed

### 2026-10-27

- **PR #55**: build: pin klayout-tools to the 0.8.0 PyPI release
- **Issue #54** (closed): Bump klayout-tools pin dac2b5daceb6 → 0.8.0
- **PR #51**: feat: route the analog driver from its netlist so LVS compares topology
- **PR #50**: docs: diagnose VNB power finding as abstract-extraction tool gap
- **Issue #48** (closed): T1 item 4 prerequisite (analog): route the driver/pad layout so LVS compares topology
- **PR #43**: docs: record probe klt lvs reports for analog and digital partitions
- **PR #46**: docs: classify stock pad frame met4/met5 DRC findings and re-cite item 3 analog
- **PR #45**: feat: record klt drc reports per partition and cite them for T1 item 3
- **Issue #44** (closed): Analog pad frame reports 486 met4/met5 DRC violations under klt drc sky130 deck
- **PR #41**: feat: place ddr_mux and predriver in the layout generator and attest item 2 analog
- **PR #38**: feat: place driver, drv_sel and drv_slice devices in the layout generator
- **PR #36**: docs: sync manifests README verdict count and CI freshness list with signoff record
- **PR #35**: feat: generate pad-cell GDS with a grounded-gate ESD clamp (stage 1 of T1 item 2 analog)
- **PR #33**: feat: route serializer netlist with a VCCD power grid for T1 item 2
- **PR #28**: feat(design): analog schematics and derived netlists for T1 item 1
- **PR #29**: feat: add 8:1 serializer RTL, cocotb bench, netlist and item 1 digital attestation
- **Issue #22** (closed): T1 item 2 (layout, analog): driver and pad-cell layout in the 75 µm analog pad slot
- **Issue #34** (closed): manifests/README.md 'Current verdict' still says 4 of 22 items met after item 2 (digital) landed
- **Issue #23** (closed): T1 item 2 (layout, digital): place-and-route the serializer to a committed routed GDS with a PDN
- **Issue #20** (closed): T1 item 1 (design sources, analog): schematics and derived netlists for the DDR mux, predriver, current-steering driver and pad cell
- **Issue #21** (closed): T1 item 1 (design sources, digital): serializer RTL (8:1→2:1 reduction, ÷4 word counter) and its synthesized netlist

### 2026-10-24

- **PR #8**: ci: add T1 signoff manifest, item 10 attestation and freshness workflow
- **Issue #5** (closed): Signoff scaffolding: block manifest, committed klt signoff record, and CI (T1 item 10)

### 2026-10-21

- **PR #15**: Bump Repo Skills 0.24.3 -> 0.24.7
- **PR #14**: build: wire pnpm lint/test/check scripts to RTL lint and smoke bench
- **Issue #13** (closed): Wire package.json check:ci/check:all/test/lint to the real verification checks (currently vacuous exit-0 stubs)

### 2026-10-20

- **PR #9**: docs(spec): propose LVDS transmitter target spec and decision records
- **Issue #2** (closed): Draft and ratify the target spec

### 2026-10-17

- **PR #10**: feat: pin sky130 environment and commit analog and digital PDK smoke runs
- **PR #7**: feat(verification): cocotb/Icarus smoke harness with negative control, lint and CI
- **PR #1**: chore(loom): Install Loom 0.19.1180
- **Issue #4** (closed): Test harness skeleton: adopt-or-record gf180-tmds-tx's cocotb runner and negative-control pattern, plus RTL lint and CI (T1 item 9)
- **Issue #3** (closed): Pin the sky130 environment (adopt sky130-modexp's setup, include sky130_fd_io) and commit analog and digital smoke runs
