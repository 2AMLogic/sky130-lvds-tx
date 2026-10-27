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
C {ipin.sym} -140 -60 0 0 {name=p1 lab=GPA}
C {ipin.sym} -140 -100 0 0 {name=p2 lab=GPB}
C {ipin.sym} -140 -140 0 0 {name=p3 lab=GNA}
C {ipin.sym} -140 -180 0 0 {name=p4 lab=GNB}
C {ipin.sym} -140 -220 0 0 {name=p5 lab=XPA}
C {ipin.sym} -140 -260 0 0 {name=p6 lab=XPB}
C {ipin.sym} -140 -300 0 0 {name=p7 lab=XNA}
C {ipin.sym} -140 -340 0 0 {name=p8 lab=XNB}
C {ipin.sym} -140 -380 0 0 {name=p9 lab=EN}
C {ipin.sym} -140 -420 0 0 {name=p10 lab=EM0}
C {ipin.sym} -140 -460 0 0 {name=p11 lab=EM1}
C {ipin.sym} -140 -500 0 0 {name=p12 lab=IREF}
C {ipin.sym} -140 -540 0 0 {name=p13 lab=VCMREF}
C {iopin.sym} 60 -60 0 0 {name=p14 lab=OUTP}
C {iopin.sym} 60 -100 0 0 {name=p15 lab=OUTN}
C {iopin.sym} 60 -140 0 0 {name=p16 lab=VCCD}
C {iopin.sym} 60 -180 0 0 {name=p17 lab=VDDIO}
C {iopin.sym} 60 -220 0 0 {name=p18 lab=VSSIO}
C {nfet_g5v0d10v5.sym} 200 100 0 0 {name=MNB1 L=1 W=2 nf=1 mult=1 ad=0.58 as=0.58 pd=4.58 ps=4.58 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=nfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 220 70 0 0 {name=l1 lab=IREF}
C {lab_pin.sym} 180 100 2 0 {name=l2 lab=IREF}
C {lab_pin.sym} 220 130 0 0 {name=l3 lab=VSSIO}
C {lab_pin.sym} 220 100 0 0 {name=l4 lab=VSSIO}
C {nfet_g5v0d10v5.sym} 420 100 0 0 {name=MNB2 L=1 W=2 nf=1 mult=1 ad=0.58 as=0.58 pd=4.58 ps=4.58 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=nfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 440 70 0 0 {name=l5 lab=BIASP}
C {lab_pin.sym} 400 100 2 0 {name=l6 lab=IREF}
C {lab_pin.sym} 440 130 0 0 {name=l7 lab=VSSIO}
C {lab_pin.sym} 440 100 0 0 {name=l8 lab=VSSIO}
C {pfet_g5v0d10v5.sym} 640 100 0 0 {name=MPB L=1 W=2 nf=1 mult=1 ad=0.58 as=0.58 pd=4.58 ps=4.58 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 660 130 0 0 {name=l9 lab=BIASP}
C {lab_pin.sym} 620 100 2 0 {name=l10 lab=BIASP}
C {lab_pin.sym} 660 70 0 0 {name=l11 lab=VDDIO}
C {lab_pin.sym} 660 100 0 0 {name=l12 lab=VDDIO}
C {nfet_g5v0d10v5.sym} 860 100 0 0 {name=MT L=1 W=4 nf=1 mult=1 ad=1.16 as=1.16 pd=8.58 ps=8.58 nrd=0.0725 nrs=0.0725 sa=0 sb=0 sd=0 model=nfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 880 70 0 0 {name=l13 lab=TAIL}
C {lab_pin.sym} 840 100 2 0 {name=l14 lab=IREF}
C {lab_pin.sym} 880 130 0 0 {name=l15 lab=VSSIO}
C {lab_pin.sym} 880 100 0 0 {name=l16 lab=VSSIO}
C {nfet_g5v0d10v5.sym} 1080 100 0 0 {name=M1 L=1 W=10 nf=1 mult=1 ad=2.9 as=2.9 pd=20.58 ps=20.58 nrd=0.029 nrs=0.029 sa=0 sb=0 sd=0 model=nfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 1100 70 0 0 {name=l17 lab=N1}
C {lab_pin.sym} 1060 100 2 0 {name=l18 lab=VCMS}
C {lab_pin.sym} 1100 130 0 0 {name=l19 lab=TAIL}
C {lab_pin.sym} 1100 100 0 0 {name=l20 lab=VSSIO}
C {nfet_g5v0d10v5.sym} 1300 100 0 0 {name=M2 L=1 W=10 nf=1 mult=1 ad=2.9 as=2.9 pd=20.58 ps=20.58 nrd=0.029 nrs=0.029 sa=0 sb=0 sd=0 model=nfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 1320 70 0 0 {name=l21 lab=VCMFB}
C {lab_pin.sym} 1280 100 2 0 {name=l22 lab=VCMREF}
C {lab_pin.sym} 1320 130 0 0 {name=l23 lab=TAIL}
C {lab_pin.sym} 1320 100 0 0 {name=l24 lab=VSSIO}
C {pfet_g5v0d10v5.sym} 200 270 0 0 {name=ML1 L=1 W=4 nf=1 mult=1 ad=1.16 as=1.16 pd=8.58 ps=8.58 nrd=0.0725 nrs=0.0725 sa=0 sb=0 sd=0 model=pfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 220 300 0 0 {name=l25 lab=N1}
C {lab_pin.sym} 180 270 2 0 {name=l26 lab=N1}
C {lab_pin.sym} 220 240 0 0 {name=l27 lab=VDDIO}
C {lab_pin.sym} 220 270 0 0 {name=l28 lab=VDDIO}
C {pfet_g5v0d10v5.sym} 420 270 0 0 {name=ML2 L=1 W=4 nf=1 mult=1 ad=1.16 as=1.16 pd=8.58 ps=8.58 nrd=0.0725 nrs=0.0725 sa=0 sb=0 sd=0 model=pfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 440 300 0 0 {name=l29 lab=VCMFB}
C {lab_pin.sym} 400 270 2 0 {name=l30 lab=N1}
C {lab_pin.sym} 440 240 0 0 {name=l31 lab=VDDIO}
C {lab_pin.sym} 440 270 0 0 {name=l32 lab=VDDIO}
C {nfet_g5v0d10v5.sym} 640 270 0 0 {name=CC L=2 W=20 nf=1 mult=1 ad=5.8 as=5.8 pd=40.58 ps=40.58 nrd=0.0145 nrs=0.0145 sa=0 sb=0 sd=0 model=nfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 660 240 0 0 {name=l33 lab=VSSIO}
C {lab_pin.sym} 620 270 2 0 {name=l34 lab=VCMFB}
C {lab_pin.sym} 660 300 0 0 {name=l35 lab=VSSIO}
C {lab_pin.sym} 660 270 0 0 {name=l36 lab=VSSIO}
C {res_high_po_1p41.sym} 860 270 0 0 {name=RS1 L=15 model=res_high_po_1p41 spiceprefix=X mult=1}
C {lab_pin.sym} 860 240 0 0 {name=l37 lab=OUTP}
C {lab_pin.sym} 860 300 0 0 {name=l38 lab=VCMS}
C {lab_pin.sym} 840 270 2 0 {name=l39 lab=VSSIO}
C {res_high_po_1p41.sym} 1080 270 0 0 {name=RS2 L=15 model=res_high_po_1p41 spiceprefix=X mult=1}
C {lab_pin.sym} 1080 240 0 0 {name=l40 lab=OUTN}
C {lab_pin.sym} 1080 300 0 0 {name=l41 lab=VCMS}
C {lab_pin.sym} 1060 270 2 0 {name=l42 lab=VSSIO}
C {drv_sel.sym} 1300 270 0 0 {name=xsel_en}
C {lab_pin.sym} 1240 210 2 0 {name=l43 lab=EN}
C {lab_pin.sym} 1360 210 0 0 {name=l44 lab=BIASP}
C {lab_pin.sym} 1360 230 0 0 {name=l45 lab=VCMFB}
C {lab_pin.sym} 1360 250 0 0 {name=l46 lab=PGM}
C {lab_pin.sym} 1360 270 0 0 {name=l47 lab=NGM}
C {lab_pin.sym} 1360 290 0 0 {name=l48 lab=VCCD}
C {lab_pin.sym} 1360 310 0 0 {name=l49 lab=VDDIO}
C {lab_pin.sym} 1360 330 0 0 {name=l50 lab=VSSIO}
C {drv_sel.sym} 200 440 0 0 {name=xsel_e0}
C {lab_pin.sym} 140 380 2 0 {name=l51 lab=EM0}
C {lab_pin.sym} 260 380 0 0 {name=l52 lab=BIASP}
C {lab_pin.sym} 260 400 0 0 {name=l53 lab=VCMFB}
C {lab_pin.sym} 260 420 0 0 {name=l54 lab=PGE0}
C {lab_pin.sym} 260 440 0 0 {name=l55 lab=NGE0}
C {lab_pin.sym} 260 460 0 0 {name=l56 lab=VCCD}
C {lab_pin.sym} 260 480 0 0 {name=l57 lab=VDDIO}
C {lab_pin.sym} 260 500 0 0 {name=l58 lab=VSSIO}
C {drv_sel.sym} 420 440 0 0 {name=xsel_e1}
C {lab_pin.sym} 360 380 2 0 {name=l59 lab=EM1}
C {lab_pin.sym} 480 380 0 0 {name=l60 lab=BIASP}
C {lab_pin.sym} 480 400 0 0 {name=l61 lab=VCMFB}
C {lab_pin.sym} 480 420 0 0 {name=l62 lab=PGE1}
C {lab_pin.sym} 480 440 0 0 {name=l63 lab=NGE1}
C {lab_pin.sym} 480 460 0 0 {name=l64 lab=VCCD}
C {lab_pin.sym} 480 480 0 0 {name=l65 lab=VDDIO}
C {lab_pin.sym} 480 500 0 0 {name=l66 lab=VSSIO}
C {drv_slice.sym} 640 440 0 0 {name=xsl_main SCALE=11}
C {lab_pin.sym} 580 390 2 0 {name=l67 lab=GPA}
C {lab_pin.sym} 580 410 2 0 {name=l68 lab=GPB}
C {lab_pin.sym} 580 430 2 0 {name=l69 lab=GNA}
C {lab_pin.sym} 580 450 2 0 {name=l70 lab=GNB}
C {lab_pin.sym} 580 470 2 0 {name=l71 lab=PGM}
C {lab_pin.sym} 580 490 2 0 {name=l72 lab=NGM}
C {lab_pin.sym} 700 390 0 0 {name=l73 lab=OUTP}
C {lab_pin.sym} 700 410 0 0 {name=l74 lab=OUTN}
C {lab_pin.sym} 700 430 0 0 {name=l75 lab=VCCD}
C {lab_pin.sym} 700 450 0 0 {name=l76 lab=VDDIO}
C {lab_pin.sym} 700 470 0 0 {name=l77 lab=VSSIO}
C {drv_slice.sym} 860 440 0 0 {name=xsl_e0 SCALE=1}
C {lab_pin.sym} 800 390 2 0 {name=l78 lab=XPA}
C {lab_pin.sym} 800 410 2 0 {name=l79 lab=XPB}
C {lab_pin.sym} 800 430 2 0 {name=l80 lab=XNA}
C {lab_pin.sym} 800 450 2 0 {name=l81 lab=XNB}
C {lab_pin.sym} 800 470 2 0 {name=l82 lab=PGE0}
C {lab_pin.sym} 800 490 2 0 {name=l83 lab=NGE0}
C {lab_pin.sym} 920 390 0 0 {name=l84 lab=OUTP}
C {lab_pin.sym} 920 410 0 0 {name=l85 lab=OUTN}
C {lab_pin.sym} 920 430 0 0 {name=l86 lab=VCCD}
C {lab_pin.sym} 920 450 0 0 {name=l87 lab=VDDIO}
C {lab_pin.sym} 920 470 0 0 {name=l88 lab=VSSIO}
C {drv_slice.sym} 1080 440 0 0 {name=xsl_e1a SCALE=1}
C {lab_pin.sym} 1020 390 2 0 {name=l89 lab=XPA}
C {lab_pin.sym} 1020 410 2 0 {name=l90 lab=XPB}
C {lab_pin.sym} 1020 430 2 0 {name=l91 lab=XNA}
C {lab_pin.sym} 1020 450 2 0 {name=l92 lab=XNB}
C {lab_pin.sym} 1020 470 2 0 {name=l93 lab=PGE1}
C {lab_pin.sym} 1020 490 2 0 {name=l94 lab=NGE1}
C {lab_pin.sym} 1140 390 0 0 {name=l95 lab=OUTP}
C {lab_pin.sym} 1140 410 0 0 {name=l96 lab=OUTN}
C {lab_pin.sym} 1140 430 0 0 {name=l97 lab=VCCD}
C {lab_pin.sym} 1140 450 0 0 {name=l98 lab=VDDIO}
C {lab_pin.sym} 1140 470 0 0 {name=l99 lab=VSSIO}
C {drv_slice.sym} 1300 440 0 0 {name=xsl_e1b SCALE=1}
C {lab_pin.sym} 1240 390 2 0 {name=l100 lab=XPA}
C {lab_pin.sym} 1240 410 2 0 {name=l101 lab=XPB}
C {lab_pin.sym} 1240 430 2 0 {name=l102 lab=XNA}
C {lab_pin.sym} 1240 450 2 0 {name=l103 lab=XNB}
C {lab_pin.sym} 1240 470 2 0 {name=l104 lab=PGE1}
C {lab_pin.sym} 1240 490 2 0 {name=l105 lab=NGE1}
C {lab_pin.sym} 1360 390 0 0 {name=l106 lab=OUTP}
C {lab_pin.sym} 1360 410 0 0 {name=l107 lab=OUTN}
C {lab_pin.sym} 1360 430 0 0 {name=l108 lab=VCCD}
C {lab_pin.sym} 1360 450 0 0 {name=l109 lab=VDDIO}
C {lab_pin.sym} 1360 470 0 0 {name=l110 lab=VSSIO}
