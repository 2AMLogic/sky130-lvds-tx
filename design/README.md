# design

Analog-partition design sources (T1 item 1, analog): xschem schematics and
symbols for the custom cells, and the SPICE netlists derived from them.
The synthesized serializer is the digital partition and lives under `rtl/`.

**Draft.** The spec is PROPOSED, not ratified (`spec/target-spec.md`). Every
device size and bias value here is provisional: the schematics fix topology,
device flavour (spec row D4) and pin names, not a design that meets E1–E9.
Sizing closure and the testbenches are separate work.

## Cells

| Directory | Cell | Contents |
|---|---|---|
| `ddr_mux/` | `ddr_mux` | 2:1 DDR retiming mux: two matched clocked-inverter muxes (`Q`, `QB`), `D0/D1` and complements, `CLK` |
| `predriver/` | `predriver` | enable gating (`EN`: holds one switch of each pair on, spec E8), then a four-stage chain per line; main (`GPA/GNA/GPB/GNB`) and pre-emphasis (`XPA/XNA/XPB/XNB`) gate drives |
| `driver/` | `driver` | current-steering H-bridge (D1): `drv_slice` ×4 (main, scale 11; pre-emphasis legs, scale 1, selected by `EM0`/`EM1`, 0–3 units), `drv_sel` ×3 (1.8 V select to 3.3 V source/sink gate bias, no level shifter in the data path), CMFB OTA on `VDDIO` sensing `OUTP/OUTN` against `VCMREF`, bias mirror from `IREF` |
| `driver/` | `drv_slice` | one bridge: `pfet_g5v0d10v5` source, `pfet_01v8`/`nfet_01v8` switch pairs, `nfet_g5v0d10v5` sink, floating-well switches and gate-tracking devices (DR-008) |
| `pad_cell/` | `pad_cell` | ESD to `VSSIO` only (DR-001): `diode_pw2nd_11v0` plus grounded-gate `esd_nfet_g5v0d10v5` on `PAD`. `PAD` is the net of both `P_PAD` and `P_CORE` of `analog_noesd_pad` (a direct metal path) |
| `.` | `lvds_tx_analog` | top: `ddr_mux` ×2 (the second, with its phases swapped, is the previous-bit tap), `predriver`, `driver`, `pad_cell` ×2 |

Grounds are `VSSIO` throughout; rails are `VCCD` (1.8 V) and `VDDIO` (3.3 V).
Pin names are the ones layout and LVS should use.

Known open points, not decided here: the previous-bit tap assumes the
serializer holds `D1` through the following `CLK`-high phase (the digital
interface to the mux is the serializer issue's); the tap polarity is set at the
top by swapping `PREV`/`PREVB`; the sense resistors, compensation and the
non-overlap of `CLK`/`CLKB` are unsized.

## Regenerate the netlists

`klt netlist` only (never raw `xschem`); `PDK_ROOT` must point at the pinned
install (`docs/environment.md`). Netlists are written with `--block` (an
includable `.subckt`); xschem's `** sch_path:` comments carry the checkout path,
which `--check` ignores.

```console
export PDK_ROOT=$HOME/.ciel PDK=sky130A
for c in ddr_mux/ddr_mux predriver/predriver driver/driver pad_cell/pad_cell lvds_tx_analog; do
  klt netlist design/$c.sch -o design/$c.spice --rcfile design/xschemrc --block --backend local
done
```

Freshness of one netlist: the same command with `--check` (exit 0 `match`,
3 `drifted`). Then re-attest and re-render the record (`manifests/README.md`):

```console
klt signoff --attest 1 --inventory verification/signoff/item-1-analog-inventory.json \
            -o verification/signoff/evidence/item-1-analog-design-sources.json
```

Unresolved symbols make xschem emit auto-named nets (`net1`, ...) with no
error: grep a regenerated netlist for `net[0-9]`; there must be none.
