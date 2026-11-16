v {xschem version=3.4.4 file_version=1.2
}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}
C {iopin.sym} 60 -60 0 0 {name=p1 lab=PAD}
C {iopin.sym} 60 -100 0 0 {name=p2 lab=VSSIO}
C {diode.sym} 200 100 0 0 {name=D1 model=diode_pw2nd_11v0 area=64 perim=32 spiceprefix=X}
C {lab_pin.sym} 200 130 0 0 {name=l1 lab=VSSIO}
C {lab_pin.sym} 200 70 0 0 {name=l2 lab=PAD}
C {nfet_g5v0d10v5_esd.sym} 420 100 0 0 {name=MESD L=0.55 W=21.5 nf=1 mult=4 ad=6.235 as=6.235 pd=43.58 ps=43.58 nrd=0.0135 nrs=0.0135 sa=0 sb=0 sd=0 model=esd_nfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 440 70 0 0 {name=l3 lab=PAD}
C {lab_pin.sym} 400 100 2 0 {name=l4 lab=VSSIO}
C {lab_pin.sym} 440 130 0 0 {name=l5 lab=VSSIO}
C {lab_pin.sym} 440 100 0 0 {name=l6 lab=VSSIO}
T {D1 junction sizing, issue #100.  UNITS: area is um^2, perim is um.} 60 220 0 0 0.2 0.2 {}
T {} 60 244 0 0 0.2 0.2 {}
T {UNIT CONVENTION.  The sky130 diode subckt pre-scales its model cj by} 60 268 0 0 0.2 0.2 {}
T {1e-12 (cj = 0.0008512*1e-12 F per unit of area), so one unit of area} 60 292 0 0 0.2 0.2 {}
T {is 1 um^2 and the implied areal capacitance is 0.851 fF/um^2 - the} 60 316 0 0 0.2 0.2 {}
T {same CJ DR-001 line 63 records for this device.  Confirmed by} 60 340 0 0 0.2 0.2 {}
T {measurement: area=1000 perim=130 gives 858 fF against 851 fF} 60 364 0 0 0.2 0.2 {}
T {predicted.  The previous area=4e14 perim=8e7 was therefore 4e14 um^2} 60 388 0 0 0.2 0.2 {}
T {= 400 m^2 of junction: it DC-shunted the pad with 107.4 mA at 1.25 V} 60 412 0 0 0.2 0.2 {}
T {and presented 0.25 F.  A raw magnitude error, not a unit subtlety.} 60 436 0 0 0.2 0.2 {}
T {} 60 460 0 0 0.2 0.2 {}
T {ARITHMETIC.  Drawn rectangle 8.0 um x 8.0 um:} 60 484 0 0 0.2 0.2 {}
T {  area  = 8.0 * 8.0       = 64 um^2} 60 508 0 0 0.2 0.2 {}
T {  perim = 2 * (8.0 + 8.0) = 32 um} 60 532 0 0 0.2 0.2 {}
T {} 60 556 0 0 0.2 0.2 {}
T {WHY THIS SIZE.  Capacitance binds, not leakage.  Reverse leakage is} 60 580 0 0 0.2 0.2 {}
T {<= 2.04 nA anywhere on the grid, ~6e-7 of the 3.5 mA nominal tail, so} 60 604 0 0 0.2 0.2 {}
T {it cannot discriminate between candidate sizes.  Spec row P1 allows} 60 628 0 0 0.2 0.2 {}
T {pad + ESD <= 1.2 pF, i.e. 139 fF over DR-001's 1.061 pF pad} 60 652 0 0 0.2 0.2 {}
T {reference.  Worst condition over the grid and over P1's 1.0-1.6 V} 60 676 0 0 0.2 0.2 {}
T {bias range is fs / 125 C / pad at 1.0 V (lowest bias => largest Cj):} 60 700 0 0 0.2 0.2 {}
T {  XMESD junctions (fixed by DR-001, out of scope)  60.5 fF} 60 724 0 0 0.2 0.2 {}
T {  D1 at 64 um^2                                    54.1 fF} 60 748 0 0 0.2 0.2 {}
T {  pad_cell total (measured, matches the grid)     114.6 fF} 60 772 0 0 0.2 0.2 {}
T {  reserve left of the 139 fF allocation            24.4 fF  (17.6 %)} 60 796 0 0 0.2 0.2 {}
T {That reserve covers the drawn network's interconnect, contacts and} 60 820 0 0 0.2 0.2 {}
T {guard ring, and is owed to extraction (P1's stated evidence).  Area} 60 844 0 0 0.2 0.2 {}
T {is maximised subject to keeping it, because P2 (HBM >= 2 kV, a} 60 868 0 0 0.2 0.2 {}
T {target, not a result - the PDK publishes no rating) improves with} 60 892 0 0 0.2 0.2 {}
T {junction area.  Measured alternatives at the same corner:} 60 916 0 0 0.2 0.2 {}
T {  9.0 x 9.0 um (81 um^2): total 128.5 fF, reserve 10.5 fF - rejected,} 60 940 0 0 0.2 0.2 {}
T {    too little left for the interconnect that is not yet drawn} 60 964 0 0 0.2 0.2 {}
T {  7.0 x 7.0 um (49 um^2): total 102.3 fF, reserve 36.7 fF - rejected,} 60 988 0 0 0.2 0.2 {}
T {    gives up HBM area for margin P1 does not require} 60 1012 0 0 0.2 0.2 {}
T {} 60 1036 0 0 0.2 0.2 {}
T {ORIENTATION unchanged and re-confirmed, not changed: port 1 (N) of} 60 1060 0 0 0.2 0.2 {}
T {the subckt is the anode (its body is D0 N P, and a SPICE D card is} 60 1084 0 0 0.2 0.2 {}
T {Dxxx anode cathode model), so XD1 VSSIO PAD is reverse-biased for a} 60 1108 0 0 0.2 0.2 {}
T {positive pad - DR-001's ESD-to-VSSIO orientation.  Do not flip it.} 60 1132 0 0 0.2 0.2 {}
T {The grid confirms the asymmetry: 1 pA reverse at +1.25 V against} 60 1156 0 0 0.2 0.2 {}
T {31.7-65.9 mA forward at -1.0 V.} 60 1180 0 0 0.2 0.2 {}
T {} 60 1204 0 0 0.2 0.2 {}
T {EVIDENCE: sim/pad-dc/ (request, deck, G75 report).  This also sets} 60 1228 0 0 0.2 0.2 {}
T {the target geometry the deferred D1 layout must match; see} 60 1252 0 0 0.2 0.2 {}
T {layout/README.md 'Not drawn yet (deferred)'.} 60 1276 0 0 0.2 0.2 {}
