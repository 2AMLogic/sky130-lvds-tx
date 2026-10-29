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
C {ipin.sym} -140 -60 0 0 {name=p1 lab=Q}
C {ipin.sym} -140 -100 0 0 {name=p2 lab=QB}
C {ipin.sym} -140 -140 0 0 {name=p3 lab=PQ}
C {ipin.sym} -140 -180 0 0 {name=p4 lab=PQB}
C {ipin.sym} -140 -220 0 0 {name=p5 lab=EN}
C {opin.sym} -40 -60 0 0 {name=p6 lab=GPA}
C {opin.sym} -40 -100 0 0 {name=p7 lab=GNA}
C {opin.sym} -40 -140 0 0 {name=p8 lab=GPB}
C {opin.sym} -40 -180 0 0 {name=p9 lab=GNB}
C {opin.sym} -40 -220 0 0 {name=p10 lab=XPA}
C {opin.sym} -40 -260 0 0 {name=p11 lab=XNA}
C {opin.sym} -40 -300 0 0 {name=p12 lab=XPB}
C {opin.sym} -40 -340 0 0 {name=p13 lab=XNB}
C {iopin.sym} 60 -60 0 0 {name=p14 lab=VCCD}
C {iopin.sym} 60 -100 0 0 {name=p15 lab=VSSIO}
C {pfet_01v8.sym} 200 100 0 0 {name=MP_enb L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 220 130 0 0 {name=l1 lab=ENB}
C {lab_pin.sym} 180 100 2 0 {name=l2 lab=EN}
C {lab_pin.sym} 220 70 0 0 {name=l3 lab=VCCD}
C {lab_pin.sym} 220 100 0 0 {name=l4 lab=VCCD}
C {nfet_01v8.sym} 420 100 0 0 {name=MN_enb L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 440 70 0 0 {name=l5 lab=ENB}
C {lab_pin.sym} 400 100 2 0 {name=l6 lab=EN}
C {lab_pin.sym} 440 130 0 0 {name=l7 lab=VSSIO}
C {lab_pin.sym} 440 100 0 0 {name=l8 lab=VSSIO}
C {pfet_01v8.sym} 640 100 0 0 {name=MPA_gma L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 660 130 0 0 {name=l9 lab=g_ma}
C {lab_pin.sym} 620 100 2 0 {name=l10 lab=QB}
C {lab_pin.sym} 660 70 0 0 {name=l11 lab=VCCD}
C {lab_pin.sym} 660 100 0 0 {name=l12 lab=VCCD}
C {pfet_01v8.sym} 860 100 0 0 {name=MPB_gma L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 880 130 0 0 {name=l13 lab=g_ma}
C {lab_pin.sym} 840 100 2 0 {name=l14 lab=EN}
C {lab_pin.sym} 880 70 0 0 {name=l15 lab=VCCD}
C {lab_pin.sym} 880 100 0 0 {name=l16 lab=VCCD}
C {nfet_01v8.sym} 1080 100 0 0 {name=MNA_gma L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1100 70 0 0 {name=l17 lab=g_ma}
C {lab_pin.sym} 1060 100 2 0 {name=l18 lab=QB}
C {lab_pin.sym} 1100 130 0 0 {name=l19 lab=n_gma}
C {lab_pin.sym} 1100 100 0 0 {name=l20 lab=VSSIO}
C {nfet_01v8.sym} 1300 100 0 0 {name=MNB_gma L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1320 70 0 0 {name=l21 lab=n_gma}
C {lab_pin.sym} 1280 100 2 0 {name=l22 lab=EN}
C {lab_pin.sym} 1320 130 0 0 {name=l23 lab=VSSIO}
C {lab_pin.sym} 1320 100 0 0 {name=l24 lab=VSSIO}
C {pfet_01v8.sym} 200 270 0 0 {name=MP_1ma L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 220 300 0 0 {name=l25 lab=s1_ma}
C {lab_pin.sym} 180 270 2 0 {name=l26 lab=g_ma}
C {lab_pin.sym} 220 240 0 0 {name=l27 lab=VCCD}
C {lab_pin.sym} 220 270 0 0 {name=l28 lab=VCCD}
C {nfet_01v8.sym} 420 270 0 0 {name=MN_1ma L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 440 240 0 0 {name=l29 lab=s1_ma}
C {lab_pin.sym} 400 270 2 0 {name=l30 lab=g_ma}
C {lab_pin.sym} 440 300 0 0 {name=l31 lab=VSSIO}
C {lab_pin.sym} 440 270 0 0 {name=l32 lab=VSSIO}
C {pfet_01v8.sym} 640 270 0 0 {name=MP_2ma L=0.15 W=2 nf=1 mult=1 ad=0.58 as=0.58 pd=4.58 ps=4.58 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 660 300 0 0 {name=l33 lab=s2_ma}
C {lab_pin.sym} 620 270 2 0 {name=l34 lab=s1_ma}
C {lab_pin.sym} 660 240 0 0 {name=l35 lab=VCCD}
C {lab_pin.sym} 660 270 0 0 {name=l36 lab=VCCD}
C {nfet_01v8.sym} 860 270 0 0 {name=MN_2ma L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 880 240 0 0 {name=l37 lab=s2_ma}
C {lab_pin.sym} 840 270 2 0 {name=l38 lab=s1_ma}
C {lab_pin.sym} 880 300 0 0 {name=l39 lab=VSSIO}
C {lab_pin.sym} 880 270 0 0 {name=l40 lab=VSSIO}
C {pfet_01v8.sym} 1080 270 0 0 {name=MP_3pma L=0.15 W=11 nf=2 mult=1 ad=1.595 as=3.19 pd=11.58 ps=23.16 nrd=0.0264 nrs=0.0264 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1100 300 0 0 {name=l41 lab=GPA}
C {lab_pin.sym} 1060 270 2 0 {name=l42 lab=s2_ma}
C {lab_pin.sym} 1100 240 0 0 {name=l43 lab=VCCD}
C {lab_pin.sym} 1100 270 0 0 {name=l44 lab=VCCD}
C {nfet_01v8.sym} 1300 270 0 0 {name=MN_3pma L=0.15 W=5.5 nf=1 mult=1 ad=1.595 as=1.595 pd=11.58 ps=11.58 nrd=0.0527 nrs=0.0527 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1320 240 0 0 {name=l45 lab=GPA}
C {lab_pin.sym} 1280 270 2 0 {name=l46 lab=s2_ma}
C {lab_pin.sym} 1320 300 0 0 {name=l47 lab=VSSIO}
C {lab_pin.sym} 1320 270 0 0 {name=l48 lab=VSSIO}
C {pfet_01v8.sym} 200 440 0 0 {name=MP_3nma L=0.15 W=11 nf=2 mult=1 ad=1.595 as=3.19 pd=11.58 ps=23.16 nrd=0.0264 nrs=0.0264 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 220 470 0 0 {name=l49 lab=GNA}
C {lab_pin.sym} 180 440 2 0 {name=l50 lab=s2_ma}
C {lab_pin.sym} 220 410 0 0 {name=l51 lab=VCCD}
C {lab_pin.sym} 220 440 0 0 {name=l52 lab=VCCD}
C {nfet_01v8.sym} 420 440 0 0 {name=MN_3nma L=0.15 W=5.5 nf=1 mult=1 ad=1.595 as=1.595 pd=11.58 ps=11.58 nrd=0.0527 nrs=0.0527 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 440 410 0 0 {name=l53 lab=GNA}
C {lab_pin.sym} 400 440 2 0 {name=l54 lab=s2_ma}
C {lab_pin.sym} 440 470 0 0 {name=l55 lab=VSSIO}
C {lab_pin.sym} 440 440 0 0 {name=l56 lab=VSSIO}
C {pfet_01v8.sym} 640 440 0 0 {name=MPA_gmb L=0.15 W=2 nf=1 mult=1 ad=0.58 as=0.58 pd=4.58 ps=4.58 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 660 470 0 0 {name=l57 lab=n_gmb}
C {lab_pin.sym} 620 440 2 0 {name=l58 lab=Q}
C {lab_pin.sym} 660 410 0 0 {name=l59 lab=VCCD}
C {lab_pin.sym} 660 440 0 0 {name=l60 lab=VCCD}
C {pfet_01v8.sym} 860 440 0 0 {name=MPB_gmb L=0.15 W=2 nf=1 mult=1 ad=0.58 as=0.58 pd=4.58 ps=4.58 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 880 470 0 0 {name=l61 lab=g_mb}
C {lab_pin.sym} 840 440 2 0 {name=l62 lab=ENB}
C {lab_pin.sym} 880 410 0 0 {name=l63 lab=n_gmb}
C {lab_pin.sym} 880 440 0 0 {name=l64 lab=VCCD}
C {nfet_01v8.sym} 1080 440 0 0 {name=MNA_gmb L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1100 410 0 0 {name=l65 lab=g_mb}
C {lab_pin.sym} 1060 440 2 0 {name=l66 lab=Q}
C {lab_pin.sym} 1100 470 0 0 {name=l67 lab=VSSIO}
C {lab_pin.sym} 1100 440 0 0 {name=l68 lab=VSSIO}
C {nfet_01v8.sym} 1300 440 0 0 {name=MNB_gmb L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1320 410 0 0 {name=l69 lab=g_mb}
C {lab_pin.sym} 1280 440 2 0 {name=l70 lab=ENB}
C {lab_pin.sym} 1320 470 0 0 {name=l71 lab=VSSIO}
C {lab_pin.sym} 1320 440 0 0 {name=l72 lab=VSSIO}
C {pfet_01v8.sym} 200 610 0 0 {name=MP_1mb L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 220 640 0 0 {name=l73 lab=s1_mb}
C {lab_pin.sym} 180 610 2 0 {name=l74 lab=g_mb}
C {lab_pin.sym} 220 580 0 0 {name=l75 lab=VCCD}
C {lab_pin.sym} 220 610 0 0 {name=l76 lab=VCCD}
C {nfet_01v8.sym} 420 610 0 0 {name=MN_1mb L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 440 580 0 0 {name=l77 lab=s1_mb}
C {lab_pin.sym} 400 610 2 0 {name=l78 lab=g_mb}
C {lab_pin.sym} 440 640 0 0 {name=l79 lab=VSSIO}
C {lab_pin.sym} 440 610 0 0 {name=l80 lab=VSSIO}
C {pfet_01v8.sym} 640 610 0 0 {name=MP_2mb L=0.15 W=2 nf=1 mult=1 ad=0.58 as=0.58 pd=4.58 ps=4.58 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 660 640 0 0 {name=l81 lab=s2_mb}
C {lab_pin.sym} 620 610 2 0 {name=l82 lab=s1_mb}
C {lab_pin.sym} 660 580 0 0 {name=l83 lab=VCCD}
C {lab_pin.sym} 660 610 0 0 {name=l84 lab=VCCD}
C {nfet_01v8.sym} 860 610 0 0 {name=MN_2mb L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 880 580 0 0 {name=l85 lab=s2_mb}
C {lab_pin.sym} 840 610 2 0 {name=l86 lab=s1_mb}
C {lab_pin.sym} 880 640 0 0 {name=l87 lab=VSSIO}
C {lab_pin.sym} 880 610 0 0 {name=l88 lab=VSSIO}
C {pfet_01v8.sym} 1080 610 0 0 {name=MP_3pmb L=0.15 W=11 nf=2 mult=1 ad=1.595 as=3.19 pd=11.58 ps=23.16 nrd=0.0264 nrs=0.0264 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1100 640 0 0 {name=l89 lab=GPB}
C {lab_pin.sym} 1060 610 2 0 {name=l90 lab=s2_mb}
C {lab_pin.sym} 1100 580 0 0 {name=l91 lab=VCCD}
C {lab_pin.sym} 1100 610 0 0 {name=l92 lab=VCCD}
C {nfet_01v8.sym} 1300 610 0 0 {name=MN_3pmb L=0.15 W=5.5 nf=1 mult=1 ad=1.595 as=1.595 pd=11.58 ps=11.58 nrd=0.0527 nrs=0.0527 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1320 580 0 0 {name=l93 lab=GPB}
C {lab_pin.sym} 1280 610 2 0 {name=l94 lab=s2_mb}
C {lab_pin.sym} 1320 640 0 0 {name=l95 lab=VSSIO}
C {lab_pin.sym} 1320 610 0 0 {name=l96 lab=VSSIO}
C {pfet_01v8.sym} 200 780 0 0 {name=MP_3nmb L=0.15 W=11 nf=2 mult=1 ad=1.595 as=3.19 pd=11.58 ps=23.16 nrd=0.0264 nrs=0.0264 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 220 810 0 0 {name=l97 lab=GNB}
C {lab_pin.sym} 180 780 2 0 {name=l98 lab=s2_mb}
C {lab_pin.sym} 220 750 0 0 {name=l99 lab=VCCD}
C {lab_pin.sym} 220 780 0 0 {name=l100 lab=VCCD}
C {nfet_01v8.sym} 420 780 0 0 {name=MN_3nmb L=0.15 W=5.5 nf=1 mult=1 ad=1.595 as=1.595 pd=11.58 ps=11.58 nrd=0.0527 nrs=0.0527 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 440 750 0 0 {name=l101 lab=GNB}
C {lab_pin.sym} 400 780 2 0 {name=l102 lab=s2_mb}
C {lab_pin.sym} 440 810 0 0 {name=l103 lab=VSSIO}
C {lab_pin.sym} 440 780 0 0 {name=l104 lab=VSSIO}
C {pfet_01v8.sym} 640 780 0 0 {name=MPA_gea L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 660 810 0 0 {name=l105 lab=g_ea}
C {lab_pin.sym} 620 780 2 0 {name=l106 lab=PQB}
C {lab_pin.sym} 660 750 0 0 {name=l107 lab=VCCD}
C {lab_pin.sym} 660 780 0 0 {name=l108 lab=VCCD}
C {pfet_01v8.sym} 860 780 0 0 {name=MPB_gea L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 880 810 0 0 {name=l109 lab=g_ea}
C {lab_pin.sym} 840 780 2 0 {name=l110 lab=EN}
C {lab_pin.sym} 880 750 0 0 {name=l111 lab=VCCD}
C {lab_pin.sym} 880 780 0 0 {name=l112 lab=VCCD}
C {nfet_01v8.sym} 1080 780 0 0 {name=MNA_gea L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1100 750 0 0 {name=l113 lab=g_ea}
C {lab_pin.sym} 1060 780 2 0 {name=l114 lab=PQB}
C {lab_pin.sym} 1100 810 0 0 {name=l115 lab=n_gea}
C {lab_pin.sym} 1100 780 0 0 {name=l116 lab=VSSIO}
C {nfet_01v8.sym} 1300 780 0 0 {name=MNB_gea L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1320 750 0 0 {name=l117 lab=n_gea}
C {lab_pin.sym} 1280 780 2 0 {name=l118 lab=EN}
C {lab_pin.sym} 1320 810 0 0 {name=l119 lab=VSSIO}
C {lab_pin.sym} 1320 780 0 0 {name=l120 lab=VSSIO}
C {pfet_01v8.sym} 200 950 0 0 {name=MP_1ea L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 220 980 0 0 {name=l121 lab=s1_ea}
C {lab_pin.sym} 180 950 2 0 {name=l122 lab=g_ea}
C {lab_pin.sym} 220 920 0 0 {name=l123 lab=VCCD}
C {lab_pin.sym} 220 950 0 0 {name=l124 lab=VCCD}
C {nfet_01v8.sym} 420 950 0 0 {name=MN_1ea L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 440 920 0 0 {name=l125 lab=s1_ea}
C {lab_pin.sym} 400 950 2 0 {name=l126 lab=g_ea}
C {lab_pin.sym} 440 980 0 0 {name=l127 lab=VSSIO}
C {lab_pin.sym} 440 950 0 0 {name=l128 lab=VSSIO}
C {pfet_01v8.sym} 640 950 0 0 {name=MP_2ea L=0.15 W=2 nf=1 mult=1 ad=0.58 as=0.58 pd=4.58 ps=4.58 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 660 980 0 0 {name=l129 lab=s2_ea}
C {lab_pin.sym} 620 950 2 0 {name=l130 lab=s1_ea}
C {lab_pin.sym} 660 920 0 0 {name=l131 lab=VCCD}
C {lab_pin.sym} 660 950 0 0 {name=l132 lab=VCCD}
C {nfet_01v8.sym} 860 950 0 0 {name=MN_2ea L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 880 920 0 0 {name=l133 lab=s2_ea}
C {lab_pin.sym} 840 950 2 0 {name=l134 lab=s1_ea}
C {lab_pin.sym} 880 980 0 0 {name=l135 lab=VSSIO}
C {lab_pin.sym} 880 950 0 0 {name=l136 lab=VSSIO}
C {pfet_01v8.sym} 1080 950 0 0 {name=MP_3pea L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1100 980 0 0 {name=l137 lab=XPA}
C {lab_pin.sym} 1060 950 2 0 {name=l138 lab=s2_ea}
C {lab_pin.sym} 1100 920 0 0 {name=l139 lab=VCCD}
C {lab_pin.sym} 1100 950 0 0 {name=l140 lab=VCCD}
C {nfet_01v8.sym} 1300 950 0 0 {name=MN_3pea L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1320 920 0 0 {name=l141 lab=XPA}
C {lab_pin.sym} 1280 950 2 0 {name=l142 lab=s2_ea}
C {lab_pin.sym} 1320 980 0 0 {name=l143 lab=VSSIO}
C {lab_pin.sym} 1320 950 0 0 {name=l144 lab=VSSIO}
C {pfet_01v8.sym} 200 1120 0 0 {name=MP_3nea L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 220 1150 0 0 {name=l145 lab=XNA}
C {lab_pin.sym} 180 1120 2 0 {name=l146 lab=s2_ea}
C {lab_pin.sym} 220 1090 0 0 {name=l147 lab=VCCD}
C {lab_pin.sym} 220 1120 0 0 {name=l148 lab=VCCD}
C {nfet_01v8.sym} 420 1120 0 0 {name=MN_3nea L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 440 1090 0 0 {name=l149 lab=XNA}
C {lab_pin.sym} 400 1120 2 0 {name=l150 lab=s2_ea}
C {lab_pin.sym} 440 1150 0 0 {name=l151 lab=VSSIO}
C {lab_pin.sym} 440 1120 0 0 {name=l152 lab=VSSIO}
C {pfet_01v8.sym} 640 1120 0 0 {name=MPA_geb L=0.15 W=2 nf=1 mult=1 ad=0.58 as=0.58 pd=4.58 ps=4.58 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 660 1150 0 0 {name=l153 lab=n_geb}
C {lab_pin.sym} 620 1120 2 0 {name=l154 lab=PQ}
C {lab_pin.sym} 660 1090 0 0 {name=l155 lab=VCCD}
C {lab_pin.sym} 660 1120 0 0 {name=l156 lab=VCCD}
C {pfet_01v8.sym} 860 1120 0 0 {name=MPB_geb L=0.15 W=2 nf=1 mult=1 ad=0.58 as=0.58 pd=4.58 ps=4.58 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 880 1150 0 0 {name=l157 lab=g_eb}
C {lab_pin.sym} 840 1120 2 0 {name=l158 lab=ENB}
C {lab_pin.sym} 880 1090 0 0 {name=l159 lab=n_geb}
C {lab_pin.sym} 880 1120 0 0 {name=l160 lab=VCCD}
C {nfet_01v8.sym} 1080 1120 0 0 {name=MNA_geb L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1100 1090 0 0 {name=l161 lab=g_eb}
C {lab_pin.sym} 1060 1120 2 0 {name=l162 lab=PQ}
C {lab_pin.sym} 1100 1150 0 0 {name=l163 lab=VSSIO}
C {lab_pin.sym} 1100 1120 0 0 {name=l164 lab=VSSIO}
C {nfet_01v8.sym} 1300 1120 0 0 {name=MNB_geb L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1320 1090 0 0 {name=l165 lab=g_eb}
C {lab_pin.sym} 1280 1120 2 0 {name=l166 lab=ENB}
C {lab_pin.sym} 1320 1150 0 0 {name=l167 lab=VSSIO}
C {lab_pin.sym} 1320 1120 0 0 {name=l168 lab=VSSIO}
C {pfet_01v8.sym} 200 1290 0 0 {name=MP_1eb L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 220 1320 0 0 {name=l169 lab=s1_eb}
C {lab_pin.sym} 180 1290 2 0 {name=l170 lab=g_eb}
C {lab_pin.sym} 220 1260 0 0 {name=l171 lab=VCCD}
C {lab_pin.sym} 220 1290 0 0 {name=l172 lab=VCCD}
C {nfet_01v8.sym} 420 1290 0 0 {name=MN_1eb L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 440 1260 0 0 {name=l173 lab=s1_eb}
C {lab_pin.sym} 400 1290 2 0 {name=l174 lab=g_eb}
C {lab_pin.sym} 440 1320 0 0 {name=l175 lab=VSSIO}
C {lab_pin.sym} 440 1290 0 0 {name=l176 lab=VSSIO}
C {pfet_01v8.sym} 640 1290 0 0 {name=MP_2eb L=0.15 W=2 nf=1 mult=1 ad=0.58 as=0.58 pd=4.58 ps=4.58 nrd=0.145 nrs=0.145 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 660 1320 0 0 {name=l177 lab=s2_eb}
C {lab_pin.sym} 620 1290 2 0 {name=l178 lab=s1_eb}
C {lab_pin.sym} 660 1260 0 0 {name=l179 lab=VCCD}
C {lab_pin.sym} 660 1290 0 0 {name=l180 lab=VCCD}
C {nfet_01v8.sym} 860 1290 0 0 {name=MN_2eb L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 880 1260 0 0 {name=l181 lab=s2_eb}
C {lab_pin.sym} 840 1290 2 0 {name=l182 lab=s1_eb}
C {lab_pin.sym} 880 1320 0 0 {name=l183 lab=VSSIO}
C {lab_pin.sym} 880 1290 0 0 {name=l184 lab=VSSIO}
C {pfet_01v8.sym} 1080 1290 0 0 {name=MP_3peb L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1100 1320 0 0 {name=l185 lab=XPB}
C {lab_pin.sym} 1060 1290 2 0 {name=l186 lab=s2_eb}
C {lab_pin.sym} 1100 1260 0 0 {name=l187 lab=VCCD}
C {lab_pin.sym} 1100 1290 0 0 {name=l188 lab=VCCD}
C {nfet_01v8.sym} 1300 1290 0 0 {name=MN_3peb L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 1320 1260 0 0 {name=l189 lab=XPB}
C {lab_pin.sym} 1280 1290 2 0 {name=l190 lab=s2_eb}
C {lab_pin.sym} 1320 1320 0 0 {name=l191 lab=VSSIO}
C {lab_pin.sym} 1320 1290 0 0 {name=l192 lab=VSSIO}
C {pfet_01v8.sym} 200 1460 0 0 {name=MP_3neb L=0.15 W=1 nf=1 mult=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {lab_pin.sym} 220 1490 0 0 {name=l193 lab=XNB}
C {lab_pin.sym} 180 1460 2 0 {name=l194 lab=s2_eb}
C {lab_pin.sym} 220 1430 0 0 {name=l195 lab=VCCD}
C {lab_pin.sym} 220 1460 0 0 {name=l196 lab=VCCD}
C {nfet_01v8.sym} 420 1460 0 0 {name=MN_3neb L=0.15 W=0.5 nf=1 mult=1 ad=0.145 as=0.145 pd=1.58 ps=1.58 nrd=0.58 nrs=0.58 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {lab_pin.sym} 440 1430 0 0 {name=l197 lab=XNB}
C {lab_pin.sym} 400 1460 2 0 {name=l198 lab=s2_eb}
C {lab_pin.sym} 440 1490 0 0 {name=l199 lab=VSSIO}
C {lab_pin.sym} 440 1460 0 0 {name=l200 lab=VSSIO}
