import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bdf_lib import Design, load_symbol, PRIM, write_bsf

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def task1():
    d = Design("74LS74 D flip-flop test")
    sd = d.input_pin("Sd1", 40, 88)
    d1 = d.input_pin("D1", 40, 104)
    rd = d.input_pin("Rd1", 40, 120)
    clk = d.input_pin("clk1", 40, 136)

    ff = d.inst("7474", 392, 72, "inst2")

    q1 = d.output_pin("Q1", 600, 120)
    q1n = d.output_pin("Q1N", 600, 136)

    d.wire(sd, ff["1PRN"])
    d.wire(d1, ff["1D"])
    d.wire(rd, ff["1CLRN"])
    d.wire(clk, ff["1CLK"])
    d.wire(ff["1Q"], q1)
    d.wire(ff["1QN"], q1n)
    d.save(os.path.join(OUT, "exp5_t1_7474.bdf"))


def task2():
    d = Design("74LS112 JK flip-flop test")
    sd = d.input_pin("Sd1", 40, 88)
    j1 = d.input_pin("J1", 40, 104)
    k1 = d.input_pin("K1", 40, 120)
    rd = d.input_pin("Rd1", 40, 136)
    clk = d.input_pin("clk1", 40, 152)

    ff = d.inst("74112", 392, 72, "inst2")

    q1 = d.output_pin("Q1", 600, 136)
    q1n = d.output_pin("Q1N", 600, 152)

    d.wire(sd, ff["1PRN"])
    d.wire(j1, ff["1J"])
    d.wire(k1, ff["1K"])
    d.wire(rd, ff["1CLRN"])
    d.wire(clk, ff["1CLK"])
    d.wire(ff["1Q"], q1)
    d.wire(ff["1QN"], q1n)
    d.save(os.path.join(OUT, "exp5_t2_74112.bdf"))


task1()
task2()
print("task1/task2 done")
