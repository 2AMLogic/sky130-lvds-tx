# Item 4 digital: `VNB` `power.inconsistent_pin_net` diagnosis (#49)

Inputs: `flow/serializer/serializer_routed.gds` (sha256 `6a123945...cb8ff`), `serializer_routed.def`,
`klt 0.8.1.dev230+gb2a85ab6d62f`, deck `sky130`. Single local extractions, no grid.

## Finding being explained
`item-4-lvs-digital.json`: `VNB` reaches `VSS` (246 instances), `VCCD` (`sky130_fd_sc_hd__a22o_1_1`)
and `word_clk` (`sky130_fd_sc_hd__a21oi_1_0`).

## Evidence
1. **PDN intent is correct.** `serializer_routed.def` `SPECIALNETS`: `VSS ( PIN VSS ) ( * VNB ) ( * VGND )`,
   `VCCD ( PIN VCCD ) ( * VPB ) ( * VPWR )`. `VNB` appears in no other net.
2. **Transistor-level extraction is clean.** `klt extract <gds> --top serializer --deck sky130`
   (no abstract cells): 359 NMOS, all bulk `VGND|VSS`; 360 PMOS, all bulk `VCCD|VPB|VPWR`.
3. **Mechanism.** LEF `VNB` is a `pwell`-layer box (`a21oi_1`: 0.020 0.105 1.835 1.015). The abstract
   extractor (`extract_abstract.py`, `_lef_port_access_points`) probes each LEF port box at its
   bbox centre; with no probe role for `pwell` it takes whatever parent-level conductor is there, and
   falls back to the substrate net (`VSS`) only if none. Transformed centres:
   - `a21oi_1_0`: (26.69, 34.80) um lies under parent met1 (68/20), the `word_clk` route.
   - `a22o_1_1`: (33.81, 30.48) um lies under parent met5 (72/20), the `VCCD` strap (y 29.12-30.72).
   Both are over-cell routing, not a connection to the cell's substrate.

## Conclusion
Tool gap (abstract-cell substrate pin resolution), not a PDN/routing defect. No flow change, so the
routed GDS/DEF/netlist are unchanged and item 2 digital evidence needs no re-citation.
Upstream: 2AMLogic/klayout-tools#4363 (open). The request already carries `layout.abstract_cells`
and the library LEF; `power_connectivity: match` is blocked on #4363, not waived.
