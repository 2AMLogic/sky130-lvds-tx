v {xschem version=3.4.4 file_version=1.2
}
G {}
K {type=subcircuit
format="@name @pinlist @symname SCALE=@SCALE"
template="name=x1 SCALE=1"
}
V {}
S {}
E {}
C {ipin.sym} -140 -60 0 0 {name=p1 lab=GPA}
C {ipin.sym} -140 -100 0 0 {name=p2 lab=GPB}
C {ipin.sym} -140 -140 0 0 {name=p3 lab=GNA}
C {ipin.sym} -140 -180 0 0 {name=p4 lab=GNB}
C {ipin.sym} -140 -220 0 0 {name=p5 lab=PG}
C {ipin.sym} -140 -260 0 0 {name=p6 lab=NG}
C {iopin.sym} 60 -60 0 0 {name=p7 lab=OUTP}
C {iopin.sym} 60 -100 0 0 {name=p8 lab=OUTN}
C {iopin.sym} 60 -140 0 0 {name=p9 lab=VCCD}
C {iopin.sym} 60 -180 0 0 {name=p10 lab=VDDIO}
C {iopin.sym} 60 -220 0 0 {name=p11 lab=VSSIO}
C {pfet_g5v0d10v5.sym} 200 100 0 0 {name=MPS L=1 W=12.8 nf=2 mult="\{SCALE\}" ad=1.856 as=3.712 pd=13.38 ps=26.76 nrd=0.0227 nrs=0.0227 sa=0 sb=0 sd=0 model=pfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 220 130 0 0 {name=l1 lab=TOP}
C {lab_pin.sym} 180 100 2 0 {name=l2 lab=PG}
C {lab_pin.sym} 220 70 0 0 {name=l3 lab=VDDIO}
C {lab_pin.sym} 220 100 0 0 {name=l4 lab=VDDIO}
C {pfet_01v8.sym} 420 100 0 0 {name=MSPA L=0.15 W=3.6 nf=4 mult="\{SCALE\}" ad=0.522 as=0.783 pd=4.76 ps=7.14 nrd=0.0806 nrs=0.0806 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 440 130 0 0 {name=l5 lab=OUTP}
C {lab_pin.sym} 400 100 2 0 {name=l6 lab=GPA}
C {lab_pin.sym} 440 70 0 0 {name=l7 lab=TOP}
C {lab_pin.sym} 440 100 0 0 {name=l8 lab=WELL}
C {pfet_01v8.sym} 640 100 0 0 {name=MSPB L=0.15 W=3.6 nf=4 mult="\{SCALE\}" ad=0.522 as=0.783 pd=4.76 ps=7.14 nrd=0.0806 nrs=0.0806 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 660 130 0 0 {name=l9 lab=OUTN}
C {lab_pin.sym} 620 100 2 0 {name=l10 lab=GPB}
C {lab_pin.sym} 660 70 0 0 {name=l11 lab=TOP}
C {lab_pin.sym} 660 100 0 0 {name=l12 lab=WELL}
C {nfet_01v8.sym} 860 100 0 0 {name=MSNA L=0.15 W=2.7 nf=3 mult="\{SCALE\}" ad=0.522 as=0.522 pd=4.76 ps=4.76 nrd=0.1074 nrs=0.1074 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 880 70 0 0 {name=l13 lab=OUTP}
C {lab_pin.sym} 840 100 2 0 {name=l14 lab=GNA}
C {lab_pin.sym} 880 130 0 0 {name=l15 lab=BOT}
C {lab_pin.sym} 880 100 0 0 {name=l16 lab=VSSIO}
C {nfet_01v8.sym} 1080 100 0 0 {name=MSNB L=0.15 W=2.7 nf=3 mult="\{SCALE\}" ad=0.522 as=0.522 pd=4.76 ps=4.76 nrd=0.1074 nrs=0.1074 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1100 70 0 0 {name=l17 lab=OUTN}
C {lab_pin.sym} 1060 100 2 0 {name=l18 lab=GNB}
C {lab_pin.sym} 1100 130 0 0 {name=l19 lab=BOT}
C {lab_pin.sym} 1100 100 0 0 {name=l20 lab=VSSIO}
C {nfet_g5v0d10v5.sym} 1300 100 0 0 {name=MNS L=1 W=6 nf=1 mult="\{SCALE\}" ad=1.74 as=1.74 pd=12.58 ps=12.58 nrd=0.0483 nrs=0.0483 sa=0 sb=0 sd=0 model=nfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 1320 70 0 0 {name=l21 lab=BOT}
C {lab_pin.sym} 1280 100 2 0 {name=l22 lab=NG}
C {lab_pin.sym} 1320 130 0 0 {name=l23 lab=VSSIO}
C {lab_pin.sym} 1320 100 0 0 {name=l24 lab=VSSIO}
C {pfet_g5v0d10v5.sym} 200 270 0 0 {name=MWVA L=0.5 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=pfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 220 300 0 0 {name=l25 lab=WELL}
C {lab_pin.sym} 180 270 2 0 {name=l26 lab=OUTP}
C {lab_pin.sym} 220 240 0 0 {name=l27 lab=VCCD}
C {lab_pin.sym} 220 270 0 0 {name=l28 lab=WELL}
C {pfet_g5v0d10v5.sym} 420 270 0 0 {name=MWVB L=0.5 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=pfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 440 300 0 0 {name=l29 lab=WELL}
C {lab_pin.sym} 400 270 2 0 {name=l30 lab=OUTN}
C {lab_pin.sym} 440 240 0 0 {name=l31 lab=VCCD}
C {lab_pin.sym} 440 270 0 0 {name=l32 lab=WELL}
C {pfet_g5v0d10v5.sym} 640 270 0 0 {name=MWPA L=0.5 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=pfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 660 300 0 0 {name=l33 lab=WELL}
C {lab_pin.sym} 620 270 2 0 {name=l34 lab=VCCD}
C {lab_pin.sym} 660 240 0 0 {name=l35 lab=OUTP}
C {lab_pin.sym} 660 270 0 0 {name=l36 lab=WELL}
C {pfet_g5v0d10v5.sym} 860 270 0 0 {name=MWPB L=0.5 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=pfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 880 300 0 0 {name=l37 lab=WELL}
C {lab_pin.sym} 840 270 2 0 {name=l38 lab=VCCD}
C {lab_pin.sym} 880 240 0 0 {name=l39 lab=OUTN}
C {lab_pin.sym} 880 270 0 0 {name=l40 lab=WELL}
C {pfet_g5v0d10v5.sym} 1080 270 0 0 {name=MGTA L=0.5 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=pfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 1100 300 0 0 {name=l41 lab=GPA}
C {lab_pin.sym} 1060 270 2 0 {name=l42 lab=VCCD}
C {lab_pin.sym} 1100 240 0 0 {name=l43 lab=WELL}
C {lab_pin.sym} 1100 270 0 0 {name=l44 lab=WELL}
C {pfet_g5v0d10v5.sym} 1300 270 0 0 {name=MGTB L=0.5 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=pfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 1320 300 0 0 {name=l45 lab=GPB}
C {lab_pin.sym} 1280 270 2 0 {name=l46 lab=VCCD}
C {lab_pin.sym} 1320 240 0 0 {name=l47 lab=WELL}
C {lab_pin.sym} 1320 270 0 0 {name=l48 lab=WELL}
