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
C {ipin.sym} -140 -60 0 0 {name=p1 lab=SEL}
C {iopin.sym} 60 -60 0 0 {name=p2 lab=BIASP}
C {iopin.sym} 60 -100 0 0 {name=p3 lab=VCMFB}
C {opin.sym} -40 -60 0 0 {name=p4 lab=PG}
C {opin.sym} -40 -100 0 0 {name=p5 lab=NG}
C {iopin.sym} 60 -140 0 0 {name=p6 lab=VCCD}
C {iopin.sym} 60 -180 0 0 {name=p7 lab=VDDIO}
C {iopin.sym} 60 -220 0 0 {name=p8 lab=VSSIO}
C {pfet_01v8.sym} 200 100 0 0 {name=MP_sb L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 220 130 0 0 {name=l1 lab=SELB}
C {lab_pin.sym} 180 100 2 0 {name=l2 lab=SEL}
C {lab_pin.sym} 220 70 0 0 {name=l3 lab=VCCD}
C {lab_pin.sym} 220 100 0 0 {name=l4 lab=VCCD}
C {nfet_01v8.sym} 420 100 0 0 {name=MN_sb L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 440 70 0 0 {name=l5 lab=SELB}
C {lab_pin.sym} 400 100 2 0 {name=l6 lab=SEL}
C {lab_pin.sym} 440 130 0 0 {name=l7 lab=VSSIO}
C {lab_pin.sym} 440 100 0 0 {name=l8 lab=VSSIO}
C {nfet_g5v0d10v5.sym} 640 100 0 0 {name=MLN1 L=0.5 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 660 70 0 0 {name=l9 lab=ENHB}
C {lab_pin.sym} 620 100 2 0 {name=l10 lab=SEL}
C {lab_pin.sym} 660 130 0 0 {name=l11 lab=VSSIO}
C {lab_pin.sym} 660 100 0 0 {name=l12 lab=VSSIO}
C {nfet_g5v0d10v5.sym} 860 100 0 0 {name=MLN2 L=0.5 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 880 70 0 0 {name=l13 lab=ENH}
C {lab_pin.sym} 840 100 2 0 {name=l14 lab=SELB}
C {lab_pin.sym} 880 130 0 0 {name=l15 lab=VSSIO}
C {lab_pin.sym} 880 100 0 0 {name=l16 lab=VSSIO}
C {pfet_g5v0d10v5.sym} 1080 100 0 0 {name=MLP1 L=0.5 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=pfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 1100 130 0 0 {name=l17 lab=ENHB}
C {lab_pin.sym} 1060 100 2 0 {name=l18 lab=ENH}
C {lab_pin.sym} 1100 70 0 0 {name=l19 lab=VDDIO}
C {lab_pin.sym} 1100 100 0 0 {name=l20 lab=VDDIO}
C {pfet_g5v0d10v5.sym} 1300 100 0 0 {name=MLP2 L=0.5 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=pfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 1320 130 0 0 {name=l21 lab=ENH}
C {lab_pin.sym} 1280 100 2 0 {name=l22 lab=ENHB}
C {lab_pin.sym} 1320 70 0 0 {name=l23 lab=VDDIO}
C {lab_pin.sym} 1320 100 0 0 {name=l24 lab=VDDIO}
C {pfet_g5v0d10v5.sym} 200 270 0 0 {name=MPU L=0.5 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 220 300 0 0 {name=l25 lab=PG}
C {lab_pin.sym} 180 270 2 0 {name=l26 lab=ENH}
C {lab_pin.sym} 220 240 0 0 {name=l27 lab=VDDIO}
C {lab_pin.sym} 220 270 0 0 {name=l28 lab=VDDIO}
C {pfet_g5v0d10v5.sym} 420 270 0 0 {name=MPP L=0.5 W=4 nf=2 mult=1 ad=0.58 as=1.16 pd=4.58 ps=9.16 nrd=0.0725 nrs=0.0725 sa=0 sb=0 sd=0 model=pfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 440 300 0 0 {name=l29 lab=PG}
C {lab_pin.sym} 400 270 2 0 {name=l30 lab=ENHB}
C {lab_pin.sym} 440 240 0 0 {name=l31 lab=BIASP}
C {lab_pin.sym} 440 270 0 0 {name=l32 lab=VDDIO}
C {nfet_g5v0d10v5.sym} 640 270 0 0 {name=MND L=0.5 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 660 240 0 0 {name=l33 lab=NG}
C {lab_pin.sym} 620 270 2 0 {name=l34 lab=ENHB}
C {lab_pin.sym} 660 300 0 0 {name=l35 lab=VSSIO}
C {lab_pin.sym} 660 270 0 0 {name=l36 lab=VSSIO}
C {nfet_g5v0d10v5.sym} 860 270 0 0 {name=MNP L=0.5 W=4 nf=2 mult=1 ad=0.58 as=1.16 pd=4.58 ps=9.16 nrd=0.0725 nrs=0.0725 sa=0 sb=0 sd=0 model=nfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 880 240 0 0 {name=l37 lab=NG}
C {lab_pin.sym} 840 270 2 0 {name=l38 lab=ENH}
C {lab_pin.sym} 880 300 0 0 {name=l39 lab=VCMFB}
C {lab_pin.sym} 880 270 0 0 {name=l40 lab=VSSIO}
