"""Generate layout/sky130_lvds_tx_driver_pad.gds (T1 item 2, analog; issue #22).

Run from the repository root with the pinned PDK on the environment:

    PDK_ROOT=~/.ciel PDK=sky130A klayout -b -r layout/gen_driver_pad.py

Environment: PDK_ROOT (default ~/.ciel), PDK (default sky130A), KLT (default
`klt`), GEN_OUT (default layout/sky130_lvds_tx_driver_pad.gds).

Stages 1-3 (see layout/README.md): the pad-cell frame, the grounded-gate
ESD clamp, the `driver` (flattened from design/driver/driver.spice, placed and
routed, issue #48) and the placement-only `ddr_mux` and `predriver` cells
(design/<block>/<block>.spice).
The stock sky130_ef_io__analog_noesd_pad is read from the PDK
(DR-001), never redrawn. Output is byte-reproducible: fixed cell names, no
timestamps, and every generated cell comes from `klt gen`, which is itself
deterministic.
"""
import heapq
import json
import math
import os
import re
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

# The driver is built from design/driver/driver.spice: the netlist is flattened,
# one leaf cell per MOS/resistor, and the leaves are routed to their nets.
DRIVER_NETLIST = "design/driver/driver.spice"
DRIVER_TOP = "driver"
# Leaf-cell name prefix of each driver subcircuit (SCALE is appended for the slice).
SUB_TAGS = {"drv_sel": "drv_sel", "drv_slice": "drv_slice_s%(SCALE)d"}
# Stage 3 blocks, device lists parsed from the committed netlists.
NETLISTS = {"ddr_mux": "design/ddr_mux/ddr_mux.spice",
            "predriver": "design/predriver/predriver.spice"}
SHELF_WIDTH_UM = 150.0
BLOCK_START_GAP_UM = 20.0  # pair to first block: room for the spines and extensions
BLOCK_GAP_UM = 20.0        # between blocks: room for the gateway pads

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



# ---- driver: flatten the netlist, draw one leaf per device, route the nets ----
# Routing plan (layout/README.md, "Routing"): each leaf carries its own stubs and
# four met3 rails (S, D, G, bulk); the leaves sit on a PITCH grid in shelf rows
# with routing channels between them, and a maze router joins the rails of each
# net on met3 (horizontal) and met4 (vertical).
PITCH_UM = 0.68          # routing grid (met3/met4 width .34 + space .34 >= rule .30)
WIRE3_UM = 0.38          # met3 wire/pad: via3 enclosure 0.09 on two adjacent edges
WIRE4_UM = 0.34
CHANNEL_UM = 12.24       # gap between leaf rows (18 tracks)
LEAF_GAP_UM = 3.4        # gap between leaves in a row (5 tracks)
VIA_COST = 6
STUB_UM = 0.2
RAIL_MIN_UM = PITCH_UM + 0.4
# GDS layers (layer, datatype)
L_LICON, L_MCON, L_MET1, L_VIA1 = (66, 44), (67, 44), (68, 20), (68, 44)
L_MET2, L_VIA2, L_MET3, L_VIA3 = (69, 20), (69, 44), (70, 20), (70, 44)
L_MET4, L_MET3_LBL = (71, 20), (70, 5)

def spice_cards(path):
    """Logical SPICE cards of a file: comments dropped, '+' continuations joined."""
    cards = []
    for raw in open(path).read().splitlines():
        if raw.startswith("+") and cards:
            cards[-1] += " " + raw[1:].strip()
        elif raw.strip() and not raw.startswith("*"):
            cards.append(raw.strip())
    return cards

def parse_hier(path):
    """{subckt: {ports, params, cards}} with each card a (name, nets, model, params)."""
    subs, cur = {}, None
    for card in spice_cards(path):
        tok = card.split()
        if tok[0].lower() == ".subckt":
            ports = [t for t in tok[2:] if "=" not in t]
            params = {t.split("=")[0]: float(t.split("=")[1]) for t in tok[2:] if "=" in t}
            cur = subs[tok[1]] = {"ports": ports, "params": params, "cards": []}
        elif tok[0].lower() == ".ends":
            cur = None
        elif cur is not None and tok[0][0] in "Xx":
            k = next((i for i, t in enumerate(tok) if "=" in t), len(tok))
            par = dict(t.split("=", 1) for t in tok[k:])
            cur["cards"].append((tok[0], tok[1:k - 1], tok[k - 1], par))
    return subs

def evaluate(expr, env):
    expr = expr.strip()
    if expr.startswith("{") and expr.endswith("}"):
        return env[expr[1:-1]]
    return float(expr)

def flatten_devices(subs, top, path=None, tag="drv"):
    """Flat leaf devices of subckt `top`: dicts with a stable cell name and flat nets."""
    path = path or DRIVER_NETLIST
    out = []
    def walk(name, netmap, env, prefix, tag):
        for card, nets, model, par in subs[name]["cards"]:
            flat = [netmap.get(n, prefix + n) for n in nets]
            if model in subs:
                sub = subs[model]
                senv = dict(sub["params"])
                senv.update({k: evaluate(v, env) for k, v in par.items()})
                nm = dict(zip(sub["ports"], flat))
                stag = SUB_TAGS[model] % {k: int(v) for k, v in senv.items()}
                walk(model, nm, senv, prefix + card + "/", stag)
                continue
            mm = re.match(r"sky130_fd_pr__(?:([np])fet_(01v8|g5v0d10v5)|(res_high_po_1p41))$", model)
            if not mm:
                die("%s: unsupported device model %s on %s" % (path, model, card))
            dev = {"path": prefix + card, "cell": "%s_%s" % (tag, card), "nets": flat}
            if mm.group(3):
                dev.update(kind="res", length=evaluate(par["L"], env), m=1)
            else:
                nf = int(evaluate(par["nf"], env))
                dev.update(kind=mm.group(1), thick=mm.group(2) == "g5v0d10v5", nf=nf,
                           m=int(evaluate(par.get("m", "1"), env)), l=evaluate(par["L"], env),
                           w=evaluate(par["W"], env) / nf)  # W on the card is the total width
            out.append(dev)
    top_sub = subs[top]
    walk(top, {p: p for p in top_sub["ports"]}, dict(top_sub["params"]), "", tag=tag)
    return out, top_sub["ports"]

def snap_up(v, step):
    return int(math.ceil(v / step - 1e-9)) * step

def snap_dn(v, step):
    return int(math.floor(v / step + 1e-9)) * step

def box(ly, cell, layer, x0, y0, x1, y1):
    idx = ly.layer(*layer)
    cell.shapes(idx).insert(pya.Box(int(round(x0 / ly.dbu)), int(round(y0 / ly.dbu)),
                                    int(round(x1 / ly.dbu)), int(round(y1 / ly.dbu))))

def square(ly, cell, layer, x, y, side):
    h = side / 2.0
    box(ly, cell, layer, x - h, y - h, x + h, y + h)

def stub(ly, cell, x, y, y_rail):
    """li1 pin -> mcon -> met1 -> via1 -> met2 stub -> via2 on the met3 rail at y_rail."""
    square(ly, cell, L_MCON, x, y, 0.17)
    square(ly, cell, L_MET1, x, y, 0.32)   # via1 enclosure 0.085 on every side
    square(ly, cell, L_VIA1, x, y, 0.15)
    square(ly, cell, L_MET2, x, y, 0.32)
    box(ly, cell, L_MET2, x - STUB_UM / 2, min(y, y_rail) - 0.185, x + STUB_UM / 2, max(y, y_rail) + 0.185)
    square(ly, cell, L_VIA2, x, y_rail, 0.2)
    square(ly, cell, L_MET2, x, y_rail, 0.37)

def make_leaf(ly, dev):
    """Leaf cell for one device (cached by name). Returns (cell, rails)."""
    name = dev["cell"]
    if name in LEAVES:
        return LEAVES[name]
    if dev["kind"] == "res":
        params = {"length_um": dev["length"], "width_um": 1.41, "num": 1, "dummy": 0, "flavor": "high"}
        cell, ports = klt_gen(ly, "res_array", params, name)
        sig = {"S": [p for p in ports if p["name"].endswith("_A")],
               "D": [p for p in ports if p["name"].endswith("_B")], "G": [], "B": []}
    else:
        params = {"w_um": dev["w"], "l_um": dev["l"], "fingers": dev["nf"], "rows": 1,
                  "cols": dev["m"], "dummy": 0, "topology": "array",
                  "flavor": "nfet" if dev["kind"] == "n" else "pfet",
                  "voltage_flavor": "hvi" if dev["thick"] else "",
                  "gate_contact": True, "add_guard_ring": True}
        cell, ports = klt_gen(ly, "mos_array", params, name)
        sig = {t: [p for p in ports if p["name"][0] == "U" and p["name"].endswith("_" + t)] for t in "SDG"}
        sig["B"] = [p for p in ports if p["name"] == "TAP_W"]
    if dev["kind"] == "p" and dev["thick"]:
        # the ring's n-well touches hvi, so the 5 V mark must enclose all of it
        nw = pya.Region(cell.begin_shapes_rec(ly.layer(64, 20)))
        cell.shapes(ly.layer(75, 20)).insert(nw.bbox())
    label_ports(ly, cell, dev["path"].split("/")[-1], [p for p in ports if p["name"][0] == "U" or p["name"][0] == "R"])
    bb = cell.dbbox()

    def clash(sides):
        for ta in sig:
            for tb in sig:
                if ta < tb and sides[ta] == sides[tb]:
                    if any(abs(pa["x_um"] - pb["x_um"]) < 0.45 for pa in sig[ta] for pb in sig[tb]):
                        return True
        return False
    # S and bulk stubs run down, G up; D runs up unless that crowds a G stub (short L)
    sides = {"S": -1, "D": 1, "G": 1, "B": -1}
    if clash(sides):
        sides["D"] = -1
    if clash(sides):
        die("%s: stubs closer than 0.45 um on both sides" % name)
    # rail rows (one per terminal) on the PITCH grid, outward from the cell
    rows, lo, hi = {}, snap_dn(bb.bottom - 0.5, PITCH_UM), snap_up(bb.top + 0.5, PITCH_UM)
    for term in "SDBG":  # bottom side: S, then D if it runs down, then B; top: D, then G
        if not sig[term]:
            continue
        if sides[term] < 0:
            rows[term], lo = lo, lo - PITCH_UM
        else:
            rows[term], hi = hi, hi + PITCH_UM
    rails = {}
    for term, plist in sig.items():
        if not plist:
            continue
        for p in plist:
            stub(ly, cell, p["x_um"], p["y_um"], rows[term])
        xs = [p["x_um"] for p in plist]
        x0, x1 = min(xs) - 0.25, max(xs) + 0.25
        if x1 - x0 < RAIL_MIN_UM:
            mid = (x0 + x1) / 2.0
            x0, x1 = mid - RAIL_MIN_UM / 2, mid + RAIL_MIN_UM / 2
        box(ly, cell, L_MET3, x0, rows[term] - WIRE3_UM / 2, x1, rows[term] + WIRE3_UM / 2)
        rails[term] = (x0, x1, rows[term])
    LEAVES[name] = (cell, rails)
    return LEAVES[name]

LEAVES = {}

def place_leaves(ly, parent, devs):
    """Shelf-pack leaf instances on the PITCH grid; returns [(dev, ox, oy, rails)] in um."""
    gap = LEAF_GAP_UM
    limit = SHELF_WIDTH_UM
    placed = []
    x = y = rowh = 0.0
    for dev in devs:
        cell, rails = make_leaf(ly, dev)
        bb = cell.dbbox()
        if x and x + bb.width() > limit:
            x, y, rowh = 0.0, y + rowh + CHANNEL_UM, 0.0
        ox = snap_up(x - bb.left, PITCH_UM)
        oy = snap_up(y - bb.bottom, PITCH_UM)
        parent.insert(pya.CellInstArray(cell.cell_index(),
                                        pya.Trans(int(round(ox / ly.dbu)), int(round(oy / ly.dbu)))))
        placed.append((dev, ox, oy, rails))
        x = ox + bb.right + gap
        rowh = max(rowh, oy + bb.top - y)
    return placed

def node(v):
    return int(round(v / PITCH_UM))

class Router:
    """Maze router on met3 (layer 0, horizontal) and met4 (layer 1, vertical)."""
    def __init__(self, bounds):
        self.i0, self.j0, self.i1, self.j1 = bounds
        self.owner = {}
        self.edges = {}

    def mark_rail(self, net, x0, x1, y):
        j = node(y)
        for i in range(int(math.ceil((x0 - 0.49) / PITCH_UM - 1e-9)), int(math.floor((x1 + 0.49) / PITCH_UM + 1e-9)) + 1):
            self.owner[(0, i, j)] = net

    @staticmethod
    def rail_nodes(x0, x1, y):
        """(i, j) nodes where a via3 fits on the rail."""
        lo = int(math.ceil((x0 + 0.19) / PITCH_UM - 1e-9))
        hi = int(math.floor((x1 - 0.19) / PITCH_UM + 1e-9))
        return [(0, i, node(y)) for i in range(lo, hi + 1)]

    def free(self, net, n):
        o = self.owner.get(n)
        return o is None or o == net

    def route(self, net, rails):
        """Connect every rail (list of node lists) of one net; returns False on failure."""
        tree = set(rails[0])
        pending = [set(r) for r in rails[1:]]
        while pending:
            targets = set().union(*pending)
            found = self.search(net, tree, targets)
            if found is None:
                return False
            path = found
            for a, b in zip(path, path[1:]):
                self.edges.setdefault(net, []).append((a, b))
            for n in path:
                self.owner[n] = net
                tree.add(n)
            hit = path[-1]
            pending = [r for r in pending if hit not in r]
            for r in rails:  # a joined rail contributes all of its nodes to the tree
                if hit in r:
                    tree.update(r)
        return True

    def search(self, net, sources, targets):
        heap = [(0, 0, s) for s in sorted(sources)]
        heapq.heapify(heap)
        dist = {s: 0 for s in sources}
        prev = {}
        seq = 0
        while heap:
            d, _, cur = heapq.heappop(heap)
            if d > dist.get(cur, 1 << 60):
                continue
            if cur in targets:
                path = [cur]
                while path[-1] in prev:
                    path.append(prev[path[-1]])
                return path[::-1]
            l, i, j = cur
            if l == 0:
                nbrs = [((0, i - 1, j), 1), ((0, i + 1, j), 1), ((1, i, j), VIA_COST)]
            else:
                nbrs = [((1, i, j - 1), 1), ((1, i, j + 1), 1), ((0, i, j), VIA_COST)]
            for nb, c in nbrs:
                _, ni, nj = nb
                if not (self.i0 <= ni <= self.i1 and self.j0 <= nj <= self.j1) or not self.free(net, nb):
                    continue
                # a via lands on both layers: both nodes must be usable
                if c == VIA_COST and not (self.free(net, (0, ni, nj)) and self.free(net, (1, ni, nj))):
                    continue
                nd = d + c
                if nd < dist.get(nb, 1 << 60):
                    dist[nb] = nd
                    prev[nb] = cur
                    seq += 1
                    heapq.heappush(heap, (nd, seq, nb))
        return None

def draw_route(ly, cell, router):
    for net in sorted(router.edges):
        for a, b in router.edges[net]:
            (la, ia, ja), (lb, ib, jb) = a, b
            xa, ya, xb, yb = ia * PITCH_UM, ja * PITCH_UM, ib * PITCH_UM, jb * PITCH_UM
            if la != lb:
                square(ly, cell, L_VIA3, xa, ya, 0.2)
                square(ly, cell, L_MET3, xa, ya, WIRE3_UM)
                square(ly, cell, L_MET4, xa, ya, WIRE4_UM)
            elif la == 0:
                box(ly, cell, L_MET3, min(xa, xb) - WIRE3_UM / 2, min(ya, yb) - WIRE3_UM / 2,
                    max(xa, xb) + WIRE3_UM / 2, max(ya, yb) + WIRE3_UM / 2)
            else:
                box(ly, cell, L_MET4, min(xa, xb) - WIRE4_UM / 2, min(ya, yb) - WIRE4_UM / 2,
                    max(xa, xb) + WIRE4_UM / 2, max(ya, yb) + WIRE4_UM / 2)

GATE_PAD_UM = 1.2        # met4 landing pad under a via4 (0.8 um cut + 0.19 enclosure)
GATE_SETBACK = 5         # gateway sits this many tracks left of the leftmost rail

def build_routed(ly, name, path, top, tag, gates, route_nets=None):
    """A block flattened from `path`, placed leaf by leaf and routed.

    `route_nets` limits routing to those nets (None = all). `gates` maps a supply
    net to the global y (um) of its gateway: a met4 landing pad left of the block
    that the top level strands to the met5 supply straps. The block sits at y = 0.
    Returns (cell, {net: (x_local_um, y_um)}).
    """
    subs = parse_hier(path)
    if top not in subs:
        die("%s has no subckt %s" % (path, top))
    devs, top_ports = flatten_devices(subs, top, path, tag)
    cell = ly.create_cell(name)
    placed = place_leaves(ly, cell, devs)

    # rails per net: nodes where a via3 fits (grid coordinates absolute)
    nets = {}
    for dev, ox, oy, rails in placed:
        if dev["kind"] == "res":  # card is "A B bulk": A on the S rail, B on the D rail
            by_term = {"S": dev["nets"][0], "D": dev["nets"][1]}
        else:                     # MOS cards are "D G S B"
            by_term = dict(zip("DGSB", dev["nets"]))
        for term, (x0, x1, y) in rails.items():
            nets.setdefault(by_term[term], []).append((ox + x0, ox + x1, oy + y))
    allx = [r[0] for rs in nets.values() for r in rs] + [r[1] for rs in nets.values() for r in rs]
    ally = [r[2] for rs in nets.values() for r in rs]
    margin = 8
    gi = node(min(allx)) - GATE_SETBACK
    gate_nodes = {n: (1, gi, int(round(y / PITCH_UM))) for n, y in gates.items()}
    for n in gate_nodes:
        if n not in nets:
            die("%s: gateway net %s has no device terminal" % (name, n))
    gj = [g[2] for g in gate_nodes.values()]
    router = Router((min(node(min(allx)) - margin, gi - 3), min([node(min(ally)) - margin] + [j - 3 for j in gj]),
                     node(max(allx)) + margin, max([node(max(ally)) + margin] + [j + 3 for j in gj])))
    ids = {n: k for k, n in enumerate(sorted(nets))}
    for n, rs in nets.items():
        for x0, x1, y in rs:
            router.mark_rail(ids[n], x0, x1, y)
    for n, (_, i, j) in gate_nodes.items():  # keep other nets clear of the met4 landing pad
        for di in range(-2, 3):
            for dj in range(-2, 3):
                router.owner[(1, i + di, j + dj)] = ids[n]
    # short nets first, the wide power nets last
    order = sorted(nets, key=lambda n: (len(nets[n]), n))
    failed = []
    for n in order:
        if route_nets is not None and n not in route_nets:
            continue
        rail_nodes = [Router.rail_nodes(*r) for r in nets[n]]
        if any(not r for r in rail_nodes):
            die("net %s: a rail has no via3 site" % n)
        if n in gate_nodes:
            rail_nodes.insert(0, [gate_nodes[n]])
        if len(rail_nodes) > 1 and not router.route(ids[n], rail_nodes):
            failed.append(n)
    if failed:
        die("%s: unrouted nets: %s" % (name, ", ".join(failed)))
    draw_route(ly, cell, router)
    out = {}
    for n, (_, i, j) in gate_nodes.items():
        square(ly, cell, L_MET4, i * PITCH_UM, j * PITCH_UM, GATE_PAD_UM)
        out[n] = (i * PITCH_UM, j * PITCH_UM)
    # top-level pin labels: on the first rail of each port net
    lbl = ly.layer(*L_MET3_LBL)
    for p in top_ports:
        if p not in nets:
            die("port %s has no device terminal" % p)
        x0, x1, y = nets[p][0]
        i = Router.rail_nodes(x0, x1, y)[0][1]
        cell.shapes(lbl).insert(pya.Text(p, int(round(i * PITCH_UM / ly.dbu)), int(round(y / ly.dbu))))
    return cell, out

# ---- supply distribution: stock pad-frame rails -> straps -> block gateways ----
# The stock analog pad cell carries each supply only as edge stubs on met4/met5
# (x 0-1.27 and 73.73-75 um), with no via4 between the two layers. Per rail band
# this stage adds: met5 straps across the pair; met4+met5 extensions beyond both
# free edges with via4 (the 1.27 um stubs are too narrow for a legal via4) and
# via4 at the pair joint; met5 spines joining a supply's two bands (VDDIO on the
# left, VSSIO on the right); and met5 runs east to each block's gateway.
# met5 only crosses the pad interior (the ESD clamp's met4 sits in the VSSIO band).
STRAP_HALF_UM = 2.225    # half height of a strap window inside the stub band
EXT_UM = 3.6             # met4/met5 extension beyond a free pair edge
SPINE_W_UM = 1.6
L_MET5, L_VIA4 = (72, 20), (71, 44)

def frame_bands(frame, ly):
    """{net: [y_um]} of the stock stub labels (met5, left edge) for the three supplies."""
    out = {}
    it = frame.begin_shapes_rec(ly.layer(72, 5))
    while not it.at_end():
        sh = it.shape()
        if sh.is_text() and sh.text_string in ("VCCD", "VDDIO", "VSSIO") and sh.text_trans.disp.x * ly.dbu < 1.0:
            out.setdefault(sh.text_string, []).append(sh.text_trans.disp.y * ly.dbu)
        it.next()
    for n in ("VCCD", "VDDIO", "VSSIO"):
        if n not in out:
            die("stock frame has no %s label on met5" % n)
        out[n].sort()
    return out

def build_supplies(ly, top, bands, gateways, pair_w):
    """Draw the supply straps in `top`; gateways = {net: [(x_um, y_um)]} (global)."""
    h = STRAP_HALF_UM
    xr = pair_w
    spine_l = (-EXT_UM - 1.8 - SPINE_W_UM, -EXT_UM - 1.8)           # VDDIO
    spine_r = (xr + EXT_UM + 1.8, xr + EXT_UM + 1.8 + SPINE_W_UM)   # VSSIO
    def via4s(x, yc):
        for dy in (-1.0, 1.0):
            square(ly, top, L_VIA4, x, yc + dy, 0.8)
    for net, ys in bands.items():
        east = max([g[0] for g in gateways.get(net, [])] + [xr + EXT_UM]) + 1.2
        for yc in ys:
            yc = round(yc / 0.005) * 0.005   # stock label y can be off the 5 nm manufacturing grid
            lo, hi = yc - h, yc + h
            x_left = spine_l[0] if net == "VDDIO" else -EXT_UM
            x_right = spine_r[1] if net == "VSSIO" else east
            if net == "VSSIO":
                x_right = max(x_right, east)
            if net == "VDDIO" and yc > 50:
                x_right = xr + EXT_UM            # upper VDDIO band stops at its extension
            box(ly, top, L_MET5, x_left, lo, x_right, hi)
            box(ly, top, L_MET4, -EXT_UM, lo, 0.6, hi)
            box(ly, top, L_MET4, xr - 0.6, lo, xr + EXT_UM, hi)
            via4s(-EXT_UM / 2, yc)
            via4s(xr + EXT_UM / 2, yc)
            via4s(xr / 2, yc)
            for gx, gy in gateways.get(net, []):
                if abs(gy - yc) < h:
                    square(ly, top, L_VIA4, gx, gy, 0.8)
        if net == "VDDIO":
            box(ly, top, L_MET5, spine_l[0], round(ys[0] / 0.005) * 0.005 - h, spine_l[1], round(ys[-1] / 0.005) * 0.005 + h)
        if net == "VSSIO":
            box(ly, top, L_MET5, spine_r[0], round(ys[0] / 0.005) * 0.005 - h, spine_r[1], round(ys[-1] / 0.005) * 0.005 + h)

def main():
    ly = pya.Layout()
    ly.dbu = 0.001
    frame = load_frame(ly)
    esd = gen_esd(ly)
    bands = frame_bands(frame, ly)

    pad = ly.create_cell("sky130_lvds_tx_pad_cell")
    pad.insert(pya.CellInstArray(frame.cell_index(), pya.Trans()))
    ox, oy = ESD_ORIGIN_UM
    pad.insert(pya.CellInstArray(esd.cell_index(), pya.Trans(int(ox / ly.dbu), int(oy / ly.dbu))))

    pair = ly.create_cell("sky130_lvds_tx_pad_pair")
    pitch = int(PAD_PITCH_UM / ly.dbu)
    pair.insert(pya.CellInstArray(pad.cell_index(), pya.Trans(0, 0)))         # PADP
    pair.insert(pya.CellInstArray(pad.cell_index(), pya.Trans(pitch, 0)))     # PADN

    top = ly.create_cell("sky130_lvds_tx_driver_pad")
    top.insert(pya.CellInstArray(pair.cell_index(), pya.Trans(0, 0)))

    # The three blocks sit beside the pair, outside the 75 x 200 um slot: their
    # area is reported by the check script, not hidden. Each supply gateway lands
    # on the met5 strap of its band (global y), so the y of a gateway is the band
    # centre snapped to the routing grid.
    def gate_y(net):
        yc = bands[net][0]
        return round(yc / PITCH_UM) * PITCH_UM
    blocks = [
        ("sky130_lvds_tx_driver", DRIVER_NETLIST, DRIVER_TOP, "drv", ("VCCD", "VDDIO", "VSSIO"), None),
        ("sky130_lvds_tx_ddr_mux", NETLISTS["ddr_mux"], "ddr_mux", "ddr_mux", ("VCCD", "VSSIO"), {"VCCD", "VSSIO"}),
        ("sky130_lvds_tx_predriver", NETLISTS["predriver"], "predriver", "predriver", ("VCCD", "VSSIO"), {"VCCD", "VSSIO"}),
    ]
    x = 2 * pitch * ly.dbu + BLOCK_START_GAP_UM
    gateways = {}
    for name, path, topname, tag, supplies, route in blocks:
        cell, gate = build_routed(ly, name, path, topname, tag, {n: gate_y(n) for n in supplies}, route)
        dx = snap_up(x - cell.dbbox().left, PITCH_UM)
        top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans(int(round(dx / ly.dbu)), 0)))
        for n, (gx, gy) in gate.items():
            gateways.setdefault(n, []).append((dx + gx, gy))
        x = dx + cell.dbbox().right + BLOCK_GAP_UM
    build_supplies(ly, top, bands, gateways, 2 * PAD_PITCH_UM)

    opts = pya.SaveLayoutOptions()
    opts.format = "GDS2"
    opts.gds2_write_timestamps = False
    opts.gds2_write_file_properties = False
    ly.write(OUT, opts)
    print("wrote %s" % OUT)

main()
