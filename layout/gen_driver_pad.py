"""Generate layout/sky130_lvds_tx_driver_pad.gds (T1 item 2, analog; issue #22).

Run from the repository root with the pinned PDK on the environment:

    PDK_ROOT=~/.ciel PDK=sky130A klayout -b -r layout/gen_driver_pad.py

Environment: PDK_ROOT (default ~/.ciel), PDK (default sky130A), KLT (default
`klt`), GEN_OUT (default layout/sky130_lvds_tx_driver_pad.gds).

Stages 1 and 2 (see layout/README.md): the pad-cell frame, the grounded-gate
ESD clamp, and the placement-only `driver` cell (design/driver/driver.spice).
The stock sky130_ef_io__analog_noesd_pad is read from the PDK
(DR-001), never redrawn. Output is byte-reproducible: fixed cell names, no
timestamps, and every generated cell comes from `klt gen`, which is itself
deterministic.
"""
import json
import os
import subprocess
import sys
import tempfile

import pya

PDK_ROOT = os.path.expanduser(os.environ.get("PDK_ROOT", "~/.ciel"))
PDK = os.environ.get("PDK", "sky130A")
KLT = os.environ.get("KLT", "klt")
OUT = os.environ.get("GEN_OUT", "layout/sky130_lvds_tx_driver_pad.gds")

IO_GDS = os.path.join(PDK_ROOT, PDK, "libs.ref/sky130_fd_io/gds/sky130_ef_io__analog.gds")
FRAME = "sky130_ef_io__analog_noesd_pad"

# pad_cell.sch: XMESD, W=21.5 x m=4 = 86 um of L=0.55. klt gen caps a finger
# at 20 um, so the clamp is 5 fingers of 17.2 um: same total W, same L.
ESD_PARAMS = {"finger_width_um": 17.2, "l_um": 0.55, "fingers": 5, "add_guard_ring": True}
PAD_PITCH_UM = 75.0
SLOT_DEPTH_UM = 200.0
# Clamp origin inside the slot: below the met4/met5 bus rails, under the met3
# P_CORE stub (x 24.72-49.72), clear of the VCCHIB/VCCD rails at y < 12.
ESD_ORIGIN_UM = (34.0, 20.0)

# Driver devices, per design/driver/driver.spice. (name, kind, thick_oxide, W, L, nf)
# kind: n/p = MOS flavour; W is per finger (sky130 convention). Multiplicity m
# is applied at placement: SCALE for the drv_slice power devices, 1 elsewhere.
SLICE_SCALED = [
    ("XMPS", "p", True, 12.8, 1.0, 2),
    ("XMSPA", "p", False, 3.6, 0.15, 4),
    ("XMSPB", "p", False, 3.6, 0.15, 4),
    ("XMSNA", "n", False, 2.7, 0.15, 3),
    ("XMSNB", "n", False, 2.7, 0.15, 3),
    ("XMNS", "n", True, 6.0, 1.0, 1),
]
SLICE_FIXED = [
    ("XMWVA", "p", True, 0.5, 0.5, 1),
    ("XMWVB", "p", True, 0.5, 0.5, 1),
    ("XMWPA", "p", True, 0.5, 0.5, 1),
    ("XMWPB", "p", True, 0.5, 0.5, 1),
    ("XMGTA", "p", True, 0.5, 0.5, 1),
    ("XMGTB", "p", True, 0.5, 0.5, 1),
]
SEL = [
    ("XMP_sb", "p", False, 1.0, 0.15, 1),
    ("XMN_sb", "n", False, 0.5, 0.15, 1),
    ("XMLN1", "n", True, 1.0, 0.5, 1),
    ("XMLN2", "n", True, 1.0, 0.5, 1),
    ("XMLP1", "p", True, 0.5, 0.5, 1),
    ("XMLP2", "p", True, 0.5, 0.5, 1),
    ("XMPU", "p", True, 1.0, 0.5, 1),
    ("XMPP", "p", True, 4.0, 0.5, 2),
    ("XMND", "n", True, 1.0, 0.5, 1),
    ("XMNP", "n", True, 4.0, 0.5, 2),
]
BIAS = [
    ("XMNB1", "n", True, 2.0, 1.0, 1),
    ("XMNB2", "n", True, 2.0, 1.0, 1),
    ("XMPB", "p", True, 2.0, 1.0, 1),
    ("XMT", "n", True, 4.0, 1.0, 1),
    ("XM1", "n", True, 10.0, 1.0, 1),
    ("XM2", "n", True, 10.0, 1.0, 1),
    ("XML1", "p", True, 4.0, 1.0, 1),
    ("XML2", "p", True, 4.0, 1.0, 1),
    ("XCC", "n", True, 20.0, 2.0, 1),
]
# XRS1/2: res_high_po_1p41, L 15 (width 1.41 is the model's name).
SLICE_SCALES = {"xsl_main": 11, "xsl_e0": 1, "xsl_e1a": 1, "xsl_e1b": 1}
SEL_INSTANCES = ["xsel_en", "xsel_e0", "xsel_e1"]
SHELF_GAP_UM = 2.0
SHELF_WIDTH_UM = 150.0

def die(msg):
    sys.stderr.write("gen_driver_pad: %s\n" % msg)
    sys.exit(1)

def load_frame(dst):
    if not os.path.isfile(IO_GDS):
        die("stock I/O GDS not found: %s (run scripts/setup-env.sh; set PDK_ROOT)" % IO_GDS)
    src = pya.Layout()
    src.read(IO_GDS)
    cell = src.cell(FRAME)
    if cell is None:
        die("%s has no cell %s" % (IO_GDS, FRAME))
    top = dst.create_cell(FRAME)
    top.copy_tree(cell)
    return top

def gen_esd(dst):
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "esd.gds")
        run = subprocess.run(
            [KLT, "gen", "esd_device", "--params", json.dumps(ESD_PARAMS), "--pdk", PDK,
             "--pdk-root", PDK_ROOT, "--cell-name", "lvds_esd_nfet", "-o", out,
             "--format", "json"], capture_output=True, text=True)
        if run.returncode != 0:
            die("klt gen esd_device failed:\n%s%s" % (run.stdout, run.stderr))
        src = pya.Layout()
        src.read(out)
        top = dst.create_cell("lvds_esd_nfet")
        top.copy_tree(src.cell("lvds_esd_nfet"))
    return top

def klt_gen(dst, generator, params, cell_name):
    """Run `klt gen`, copy the cell into dst, return (cell, ports)."""
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "g.gds")
        run = subprocess.run(
            [KLT, "gen", generator, "--params", json.dumps(params), "--pdk", PDK,
             "--pdk-root", PDK_ROOT, "--cell-name", cell_name, "-o", out,
             "--format", "json"], capture_output=True, text=True)
        if run.returncode != 0:
            die("klt gen %s (%s) failed:\n%s%s" % (generator, cell_name, run.stdout, run.stderr))
        report = json.loads(run.stdout)
        src = pya.Layout()
        src.read(out)
        cell = dst.create_cell(cell_name)
        cell.copy_tree(src.cell(cell_name))
    return cell, report["ports"]

def label_ports(ly, cell, dev, ports):
    for p in ports:
        lay = p["layer"]
        idx = ly.layer(lay["layer"], lay["datatype"])
        cell.shapes(idx).insert(pya.Text("%s.%s" % (dev, p["name"]),
                                         int(p["x_um"] / ly.dbu), int(p["y_um"] / ly.dbu)))

def gen_mos(ly, tag, dev, mult):
    name, kind, thick, w, l, nf = dev
    params = {"w_um": w, "l_um": l, "fingers": nf, "rows": 1, "cols": mult, "dummy": 0,
              "topology": "array", "flavor": "nfet" if kind == "n" else "pfet",
              "voltage_flavor": "hvi" if thick else ""}
    cell, ports = klt_gen(ly, "mos_array", params, "%s_%s" % (tag, name))
    label_ports(ly, cell, name, ports)
    return cell

def gen_res(ly, tag, name, length):
    params = {"length_um": length, "width_um": 1.41, "num": 1, "dummy": 0, "flavor": "high"}
    cell, ports = klt_gen(ly, "res_array", params, "%s_%s" % (tag, name))
    label_ports(ly, cell, name, ports)
    return cell

def shelf_place(ly, parent, cells):
    """Place cells left to right in rows (shelf packing); order is fixed."""
    gap = int(SHELF_GAP_UM / ly.dbu)
    limit = int(SHELF_WIDTH_UM / ly.dbu)
    x = y = rowh = 0
    for c in cells:
        bb = c.bbox()
        if x and x + bb.width() > limit:
            x, y, rowh = 0, y + rowh + gap, 0
        parent.insert(pya.CellInstArray(c.cell_index(), pya.Trans(x - bb.left, y - bb.bottom)))
        x += bb.width() + gap
        rowh = max(rowh, bb.height())

def build_slice(ly, scale):
    cell = ly.create_cell("drv_slice_s%d" % scale)
    tag = "drv_slice_s%d" % scale
    devs = [gen_mos(ly, tag, d, scale) for d in SLICE_SCALED]
    devs += [gen_mos(ly, tag, d, 1) for d in SLICE_FIXED]
    shelf_place(ly, cell, devs)
    return cell

def build_sel(ly):
    cell = ly.create_cell("drv_sel")
    shelf_place(ly, cell, [gen_mos(ly, "drv_sel", d, 1) for d in SEL])
    return cell

def build_driver(ly):
    """The `driver` subcircuit: bias/CMFB devices, 3 drv_sel, 4 drv_slice."""
    cell = ly.create_cell("sky130_lvds_tx_driver")
    parts = [gen_mos(ly, "drv", d, 1) for d in BIAS]
    parts += [gen_res(ly, "drv", "XRS1", 15.0), gen_res(ly, "drv", "XRS2", 15.0)]
    slices = {sc: build_slice(ly, sc) for sc in sorted(set(SLICE_SCALES.values()))}
    sel = build_sel(ly)
    for inst in SEL_INSTANCES:
        parts.append(sel)
    for inst, sc in SLICE_SCALES.items():
        parts.append(slices[sc])
    shelf_place(ly, cell, parts)
    return cell

def main():
    ly = pya.Layout()
    ly.dbu = 0.001
    frame = load_frame(ly)
    esd = gen_esd(ly)

    pad = ly.create_cell("sky130_lvds_tx_pad_cell")
    pad.insert(pya.CellInstArray(frame.cell_index(), pya.Trans()))
    ox, oy = ESD_ORIGIN_UM
    pad.insert(pya.CellInstArray(esd.cell_index(), pya.Trans(int(ox / ly.dbu), int(oy / ly.dbu))))

    pair = ly.create_cell("sky130_lvds_tx_pad_pair")
    pitch = int(PAD_PITCH_UM / ly.dbu)
    pair.insert(pya.CellInstArray(pad.cell_index(), pya.Trans(0, 0)))         # PADP
    pair.insert(pya.CellInstArray(pad.cell_index(), pya.Trans(pitch, 0)))     # PADN

    # Placement-only driver (stage 2). It sits beside the pad pair, outside the
    # 75 x 200 um slot: its area is reported by the check script, not hidden.
    drv = build_driver(ly)
    top = ly.create_cell("sky130_lvds_tx_driver_pad")
    top.insert(pya.CellInstArray(pair.cell_index(), pya.Trans(0, 0)))
    top.insert(pya.CellInstArray(drv.cell_index(), pya.Trans(2 * pitch + int(SHELF_GAP_UM * 5 / ly.dbu), 0)))

    opts = pya.SaveLayoutOptions()
    opts.format = "GDS2"
    opts.gds2_write_timestamps = False
    opts.gds2_write_file_properties = False
    ly.write(OUT, opts)
    print("wrote %s" % OUT)

main()
