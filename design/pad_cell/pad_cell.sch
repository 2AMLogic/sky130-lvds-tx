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
C {diode.sym} 200 100 0 0 {name=D1 model=diode_pw2nd_11v0 area=4e14 perim=8e7 spiceprefix=X}
C {lab_pin.sym} 200 130 0 0 {name=l1 lab=VSSIO}
C {lab_pin.sym} 200 70 0 0 {name=l2 lab=PAD}
C {nfet_g5v0d10v5_esd.sym} 420 100 0 0 {name=MESD L=0.55 W=21.5 nf=1 mult=4 ad=6.235 as=6.235 pd=43.58 ps=43.58 nrd=0.0135 nrs=0.0135 sa=0 sb=0 sd=0 model=esd_nfet_g5v0d10v5 spiceprefix=X}
C {lab_pin.sym} 440 70 0 0 {name=l3 lab=PAD}
C {lab_pin.sym} 400 100 2 0 {name=l4 lab=VSSIO}
C {lab_pin.sym} 440 130 0 0 {name=l5 lab=VSSIO}
C {lab_pin.sym} 440 100 0 0 {name=l6 lab=VSSIO}
