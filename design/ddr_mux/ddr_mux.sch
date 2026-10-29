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
C {ipin.sym} -140 -60 0 0 {name=p1 lab=D0}
C {ipin.sym} -140 -100 0 0 {name=p2 lab=D0B}
C {ipin.sym} -140 -140 0 0 {name=p3 lab=D1}
C {ipin.sym} -140 -180 0 0 {name=p4 lab=D1B}
C {ipin.sym} -140 -220 0 0 {name=p5 lab=CLK}
C {opin.sym} -40 -60 0 0 {name=p6 lab=Q}
C {opin.sym} -40 -100 0 0 {name=p7 lab=QB}
C {iopin.sym} 60 -60 0 0 {name=p8 lab=VCCD}
C {iopin.sym} 60 -100 0 0 {name=p9 lab=VSSIO}
C {pfet_01v8.sym} 200 100 0 0 {name=MP_ck L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 220 130 0 0 {name=l1 lab=CLKB}
C {lab_pin.sym} 180 100 2 0 {name=l2 lab=CLK}
C {lab_pin.sym} 220 70 0 0 {name=l3 lab=VCCD}
C {lab_pin.sym} 220 100 0 0 {name=l4 lab=VCCD}
C {nfet_01v8.sym} 420 100 0 0 {name=MN_ck L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 440 70 0 0 {name=l5 lab=CLKB}
C {lab_pin.sym} 400 100 2 0 {name=l6 lab=CLK}
C {lab_pin.sym} 440 130 0 0 {name=l7 lab=VSSIO}
C {lab_pin.sym} 440 100 0 0 {name=l8 lab=VSSIO}
C {pfet_01v8.sym} 640 100 0 0 {name=MPD_a0 L=0.15 W=2 nf=2 mult=1 ad=0.29 as=0.58 pd=2.58 ps=5.16 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 660 130 0 0 {name=l9 lab=pm_a0}
C {lab_pin.sym} 620 100 2 0 {name=l10 lab=D0}
C {lab_pin.sym} 660 70 0 0 {name=l11 lab=VCCD}
C {lab_pin.sym} 660 100 0 0 {name=l12 lab=VCCD}
C {pfet_01v8.sym} 860 100 0 0 {name=MPE_a0 L=0.15 W=2 nf=2 mult=1 ad=0.29 as=0.58 pd=2.58 ps=5.16 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 880 130 0 0 {name=l13 lab=QB}
C {lab_pin.sym} 840 100 2 0 {name=l14 lab=CLKB}
C {lab_pin.sym} 880 70 0 0 {name=l15 lab=pm_a0}
C {lab_pin.sym} 880 100 0 0 {name=l16 lab=VCCD}
C {nfet_01v8.sym} 1080 100 0 0 {name=MNE_a0 L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1100 70 0 0 {name=l17 lab=QB}
C {lab_pin.sym} 1060 100 2 0 {name=l18 lab=CLK}
C {lab_pin.sym} 1100 130 0 0 {name=l19 lab=nm_a0}
C {lab_pin.sym} 1100 100 0 0 {name=l20 lab=VSSIO}
C {nfet_01v8.sym} 1300 100 0 0 {name=MND_a0 L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1320 70 0 0 {name=l21 lab=nm_a0}
C {lab_pin.sym} 1280 100 2 0 {name=l22 lab=D0}
C {lab_pin.sym} 1320 130 0 0 {name=l23 lab=VSSIO}
C {lab_pin.sym} 1320 100 0 0 {name=l24 lab=VSSIO}
C {pfet_01v8.sym} 200 270 0 0 {name=MPD_a1 L=0.15 W=2 nf=2 mult=1 ad=0.29 as=0.58 pd=2.58 ps=5.16 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 220 300 0 0 {name=l25 lab=pm_a1}
C {lab_pin.sym} 180 270 2 0 {name=l26 lab=D1}
C {lab_pin.sym} 220 240 0 0 {name=l27 lab=VCCD}
C {lab_pin.sym} 220 270 0 0 {name=l28 lab=VCCD}
C {pfet_01v8.sym} 420 270 0 0 {name=MPE_a1 L=0.15 W=2 nf=2 mult=1 ad=0.29 as=0.58 pd=2.58 ps=5.16 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 440 300 0 0 {name=l29 lab=QB}
C {lab_pin.sym} 400 270 2 0 {name=l30 lab=CLK}
C {lab_pin.sym} 440 240 0 0 {name=l31 lab=pm_a1}
C {lab_pin.sym} 440 270 0 0 {name=l32 lab=VCCD}
C {nfet_01v8.sym} 640 270 0 0 {name=MNE_a1 L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 660 240 0 0 {name=l33 lab=QB}
C {lab_pin.sym} 620 270 2 0 {name=l34 lab=CLKB}
C {lab_pin.sym} 660 300 0 0 {name=l35 lab=nm_a1}
C {lab_pin.sym} 660 270 0 0 {name=l36 lab=VSSIO}
C {nfet_01v8.sym} 860 270 0 0 {name=MND_a1 L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 880 240 0 0 {name=l37 lab=nm_a1}
C {lab_pin.sym} 840 270 2 0 {name=l38 lab=D1}
C {lab_pin.sym} 880 300 0 0 {name=l39 lab=VSSIO}
C {lab_pin.sym} 880 270 0 0 {name=l40 lab=VSSIO}
C {pfet_01v8.sym} 1080 270 0 0 {name=MPD_b0 L=0.15 W=2 nf=2 mult=1 ad=0.29 as=0.58 pd=2.58 ps=5.16 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1100 300 0 0 {name=l41 lab=pm_b0}
C {lab_pin.sym} 1060 270 2 0 {name=l42 lab=D0B}
C {lab_pin.sym} 1100 240 0 0 {name=l43 lab=VCCD}
C {lab_pin.sym} 1100 270 0 0 {name=l44 lab=VCCD}
C {pfet_01v8.sym} 1300 270 0 0 {name=MPE_b0 L=0.15 W=2 nf=2 mult=1 ad=0.29 as=0.58 pd=2.58 ps=5.16 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1320 300 0 0 {name=l45 lab=Q}
C {lab_pin.sym} 1280 270 2 0 {name=l46 lab=CLKB}
C {lab_pin.sym} 1320 240 0 0 {name=l47 lab=pm_b0}
C {lab_pin.sym} 1320 270 0 0 {name=l48 lab=VCCD}
C {nfet_01v8.sym} 200 440 0 0 {name=MNE_b0 L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 220 410 0 0 {name=l49 lab=Q}
C {lab_pin.sym} 180 440 2 0 {name=l50 lab=CLK}
C {lab_pin.sym} 220 470 0 0 {name=l51 lab=nm_b0}
C {lab_pin.sym} 220 440 0 0 {name=l52 lab=VSSIO}
C {nfet_01v8.sym} 420 440 0 0 {name=MND_b0 L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 440 410 0 0 {name=l53 lab=nm_b0}
C {lab_pin.sym} 400 440 2 0 {name=l54 lab=D0B}
C {lab_pin.sym} 440 470 0 0 {name=l55 lab=VSSIO}
C {lab_pin.sym} 440 440 0 0 {name=l56 lab=VSSIO}
C {pfet_01v8.sym} 640 440 0 0 {name=MPD_b1 L=0.15 W=2 nf=2 mult=1 ad=0.29 as=0.58 pd=2.58 ps=5.16 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 660 470 0 0 {name=l57 lab=pm_b1}
C {lab_pin.sym} 620 440 2 0 {name=l58 lab=D1B}
C {lab_pin.sym} 660 410 0 0 {name=l59 lab=VCCD}
C {lab_pin.sym} 660 440 0 0 {name=l60 lab=VCCD}
C {pfet_01v8.sym} 860 440 0 0 {name=MPE_b1 L=0.15 W=2 nf=2 mult=1 ad=0.29 as=0.58 pd=2.58 ps=5.16 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 880 470 0 0 {name=l61 lab=Q}
C {lab_pin.sym} 840 440 2 0 {name=l62 lab=CLK}
C {lab_pin.sym} 880 410 0 0 {name=l63 lab=pm_b1}
C {lab_pin.sym} 880 440 0 0 {name=l64 lab=VCCD}
C {nfet_01v8.sym} 1080 440 0 0 {name=MNE_b1 L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1100 410 0 0 {name=l65 lab=Q}
C {lab_pin.sym} 1060 440 2 0 {name=l66 lab=CLKB}
C {lab_pin.sym} 1100 470 0 0 {name=l67 lab=nm_b1}
C {lab_pin.sym} 1100 440 0 0 {name=l68 lab=VSSIO}
C {nfet_01v8.sym} 1300 440 0 0 {name=MND_b1 L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1320 410 0 0 {name=l69 lab=nm_b1}
C {lab_pin.sym} 1280 440 2 0 {name=l70 lab=D1B}
C {lab_pin.sym} 1320 470 0 0 {name=l71 lab=VSSIO}
C {lab_pin.sym} 1320 440 0 0 {name=l72 lab=VSSIO}
