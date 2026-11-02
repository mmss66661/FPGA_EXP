import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bdf_lib import Design

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def common(d):
    sd = d.input_pin("Sd1", 40, 88)
    rd = d.input_pin("Rd1", 40, 136)
    clk = d.input_pin("clk1", 40, 152)
    ff = d.inst("74112", 392, 72, "inst")
    q1 = d.output_pin("Q1", 600, 136)
    q1n = d.output_pin("Q1N", 600, 152)
    d.wire(sd, ff["1PRN"])
    d.wire(rd, ff["1CLRN"])
    d.wire(clk, ff["1CLK"])
    d.wire(ff["1Q"], q1)
    d.wire(ff["1QN"], q1n)
    return ff


def jk2d():
    d = Design("JK to D")
    ff = common(d)
    d1 = d.input_pin("D1", 40, 104)
    n_d = d.inst("not", 272, 48, "inst1")
    d.wire(d1, (216, 112), ff["1J"])
    d.wire((216, 112), (216, 64), n_d["IN"])
    d.junction((216, 112))
    d.wire(n_d["OUT"], (360, 64), (360, 128), ff["1K"])
    d.save(os.path.join(OUT, "exp5_t4_jk2d.bdf"))


def jk2t():
    d = Design("JK to T")
    ff = common(d)
    t1 = d.input_pin("T1", 40, 104)
    d.wire(t1, (216, 112), ff["1J"])
    d.wire((216, 112), (216, 128), ff["1K"])
    d.junction((216, 112))
    d.save(os.path.join(OUT, "exp5_t4_jk2t.bdf"))


jk2d()
jk2t()
print("conversion circuits done")
