import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bdf_lib import Design, write_bsf

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def keyin():
    d = Design("key debounce")
    k_in = d.input_pin("k_in", 40, 80)
    clk = d.input_pin("clk", 32, 200)

    n_in = d.inst("not", 216, 72, "inst3")
    ff0 = d.inst("dff", 320, 64, "inst")
    ff1 = d.inst("dff", 448, 64, "inst1")
    n_q2 = d.inst("not", 552, 72, "inst6")
    and3 = d.inst("and3", 640, 64, "inst5")
    n_clk = d.inst("not", 216, 192, "inst4")

    d.inst("vcc", 336, 0, "inst7")
    d.inst("vcc", 464, 0, "inst8")
    d.inst("vcc", 336, 144, "inst9")
    d.inst("vcc", 464, 144, "inst10")

    k_out = d.output_pin("k_out", 760, 80)
    d.output_pin("Q0", 744, 232)
    d.output_pin("Q1", 744, 256)
    d.output_pin("Q2", 744, 280)

    d.wire(k_in, n_in["IN"])
    d.wire(n_in["OUT"], (288, 88), ff0["D"])
    d.wire((288, 88), (288, 240), (744, 240))
    d.junction((288, 88))

    d.wire(ff0["Q"], (400, 88), ff1["D"])
    d.wire((400, 88), (400, 264), (744, 264))
    d.wire((400, 88), (400, 56), (620, 56), (620, 80), and3["IN1"])
    d.junction((400, 88))

    d.wire(ff1["Q"], (528, 88), n_q2["IN"])
    d.wire((528, 88), (528, 288), (744, 288))
    d.junction((528, 88))
    d.wire(n_q2["OUT"], and3["IN2"])

    d.wire(and3["OUT"], k_out)

    d.wire(clk, (208, 208), n_clk["IN"])
    d.wire(n_clk["OUT"], (272, 208), (272, 104), ff0["CLK"], ff1["CLK"])
    d.junction((320, 104))
    d.wire((208, 208), (208, 304), (656, 304), (656, 96), and3["IN3"])
    d.junction((208, 208))

    d.wire((352, 16), ff0["PRN"])
    d.wire((480, 16), ff1["PRN"])
    d.wire((352, 160), ff0["CLRN"])
    d.wire((480, 160), ff1["CLRN"])

    d.save(os.path.join(OUT, "keyin.bdf"))

    write_bsf(os.path.join(OUT, "keyin.bsf"), "keyin",
              [("k_in", "in", 1), ("clk", "in", 1),
               ("k_out", "out", 1), ("Q0", "out", 1), ("Q1", "out", 1), ("Q2", "out", 1)])
    write_bsf(os.path.join(OUT, "fenpin.bsf"), "fenpin",
              [("clk_50M", "in", 1),
               ("clk_5M", "out", 1), ("clk_500k", "out", 1), ("clk_10k", "out", 1),
               ("clk_5k", "out", 1), ("clk_500", "out", 1), ("clk_50", "out", 1),
               ("clk_1", "out", 1)])
    write_bsf(os.path.join(OUT, "rising_edge_detect.bsf"), "rising_edge_detect",
              [("KEY_IN", "in", 1), ("D", "out", 16)])
    write_bsf(os.path.join(OUT, "seg_show.bsf"), "seg_show",
              [("Num", "in", 16), ("HEX0", "out", 8), ("HEX1", "out", 8),
               ("HEX2", "out", 8), ("HEX3", "out", 8)])


keyin()
print("keyin + symbols done")
