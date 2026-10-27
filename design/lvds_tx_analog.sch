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
C {ipin.sym} -140 -260 0 0 {name=p6 lab=EN}
C {ipin.sym} -140 -300 0 0 {name=p7 lab=EM0}
C {ipin.sym} -140 -340 0 0 {name=p8 lab=EM1}
C {ipin.sym} -140 -380 0 0 {name=p9 lab=IREF}
C {ipin.sym} -140 -420 0 0 {name=p10 lab=VCMREF}
C {iopin.sym} 60 -60 0 0 {name=p11 lab=PADP}
C {iopin.sym} 60 -100 0 0 {name=p12 lab=PADN}
C {iopin.sym} 60 -140 0 0 {name=p13 lab=VCCD}
C {iopin.sym} 60 -180 0 0 {name=p14 lab=VDDIO}
C {iopin.sym} 60 -220 0 0 {name=p15 lab=VSSIO}
C {ddr_mux.sym} 200 100 0 0 {name=xmux}
C {lab_pin.sym} 140 60 2 0 {name=l1 lab=D0}
C {lab_pin.sym} 140 80 2 0 {name=l2 lab=D0B}
C {lab_pin.sym} 140 100 2 0 {name=l3 lab=D1}
C {lab_pin.sym} 140 120 2 0 {name=l4 lab=D1B}
C {lab_pin.sym} 140 140 2 0 {name=l5 lab=CLK}
C {lab_pin.sym} 260 60 0 0 {name=l6 lab=Q}
C {lab_pin.sym} 260 80 0 0 {name=l7 lab=QB}
C {lab_pin.sym} 260 100 0 0 {name=l8 lab=VCCD}
C {lab_pin.sym} 260 120 0 0 {name=l9 lab=VSSIO}
C {ddr_mux.sym} 420 100 0 0 {name=xmuxp}
C {lab_pin.sym} 360 60 2 0 {name=l10 lab=D1}
C {lab_pin.sym} 360 80 2 0 {name=l11 lab=D1B}
C {lab_pin.sym} 360 100 2 0 {name=l12 lab=D0}
C {lab_pin.sym} 360 120 2 0 {name=l13 lab=D0B}
C {lab_pin.sym} 360 140 2 0 {name=l14 lab=CLK}
C {lab_pin.sym} 480 60 0 0 {name=l15 lab=PREV}
C {lab_pin.sym} 480 80 0 0 {name=l16 lab=PREVB}
C {lab_pin.sym} 480 100 0 0 {name=l17 lab=VCCD}
C {lab_pin.sym} 480 120 0 0 {name=l18 lab=VSSIO}
C {predriver.sym} 640 100 0 0 {name=xpre}
C {lab_pin.sym} 580 10 2 0 {name=l19 lab=Q}
C {lab_pin.sym} 580 30 2 0 {name=l20 lab=QB}
C {lab_pin.sym} 580 50 2 0 {name=l21 lab=PREVB}
C {lab_pin.sym} 580 70 2 0 {name=l22 lab=PREV}
C {lab_pin.sym} 580 90 2 0 {name=l23 lab=EN}
C {lab_pin.sym} 700 10 0 0 {name=l24 lab=GPA}
C {lab_pin.sym} 700 30 0 0 {name=l25 lab=GNA}
C {lab_pin.sym} 700 50 0 0 {name=l26 lab=GPB}
C {lab_pin.sym} 700 70 0 0 {name=l27 lab=GNB}
C {lab_pin.sym} 700 90 0 0 {name=l28 lab=XPA}
C {lab_pin.sym} 700 110 0 0 {name=l29 lab=XNA}
C {lab_pin.sym} 700 130 0 0 {name=l30 lab=XPB}
C {lab_pin.sym} 700 150 0 0 {name=l31 lab=XNB}
C {lab_pin.sym} 700 170 0 0 {name=l32 lab=VCCD}
C {lab_pin.sym} 700 190 0 0 {name=l33 lab=VSSIO}
C {driver.sym} 860 100 0 0 {name=xdrv}
C {lab_pin.sym} 800 -20 2 0 {name=l34 lab=GPA}
C {lab_pin.sym} 800 0 2 0 {name=l35 lab=GPB}
C {lab_pin.sym} 800 20 2 0 {name=l36 lab=GNA}
C {lab_pin.sym} 800 40 2 0 {name=l37 lab=GNB}
C {lab_pin.sym} 800 60 2 0 {name=l38 lab=XPA}
C {lab_pin.sym} 800 80 2 0 {name=l39 lab=XPB}
C {lab_pin.sym} 800 100 2 0 {name=l40 lab=XNA}
C {lab_pin.sym} 800 120 2 0 {name=l41 lab=XNB}
C {lab_pin.sym} 800 140 2 0 {name=l42 lab=EN}
C {lab_pin.sym} 800 160 2 0 {name=l43 lab=EM0}
C {lab_pin.sym} 800 180 2 0 {name=l44 lab=EM1}
C {lab_pin.sym} 800 200 2 0 {name=l45 lab=IREF}
C {lab_pin.sym} 800 220 2 0 {name=l46 lab=VCMREF}
C {lab_pin.sym} 920 -20 0 0 {name=l47 lab=PADP}
C {lab_pin.sym} 920 0 0 0 {name=l48 lab=PADN}
C {lab_pin.sym} 920 20 0 0 {name=l49 lab=VCCD}
C {lab_pin.sym} 920 40 0 0 {name=l50 lab=VDDIO}
C {lab_pin.sym} 920 60 0 0 {name=l51 lab=VSSIO}
C {pad_cell.sym} 1080 100 0 0 {name=xpadp}
C {lab_pin.sym} 1140 90 0 0 {name=l52 lab=PADP}
C {lab_pin.sym} 1140 110 0 0 {name=l53 lab=VSSIO}
C {pad_cell.sym} 1300 100 0 0 {name=xpadn}
C {lab_pin.sym} 1360 90 0 0 {name=l54 lab=PADN}
C {lab_pin.sym} 1360 110 0 0 {name=l55 lab=VSSIO}
