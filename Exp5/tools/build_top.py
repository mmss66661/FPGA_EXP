import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bdf_lib import Design, load_symbol

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def top():
    d = Design("key pulse counter")
    key0 = d.input_pin("KEY0", 32, 88)
    key1 = d.input_pin("KEY1", 32, 216)
    clk50 = d.input_pin("CLK_50M", 32, 328)

    keyin = d.sym(load_symbol(os.path.join(OUT, "keyin.bsf")), 216, 80, "inst")
    or2 = d.inst("or2", 440, 64, "inst11")
    n_key1 = d.inst("not", 216, 208, "inst12")
    red = d.sym(load_symbol(os.path.join(OUT, "rising_edge_detect.bsf")), 600, 48, "inst2")
    seg = d.sym(load_symbol(os.path.join(OUT, "seg_show.bsf")), 840, 32, "inst3")
    fen = d.sym(load_symbol(os.path.join(OUT, "fenpin.bsf")), 216, 320, "inst4")

    kd = d.output_pin("KD[15..0]", 776, 168)
    key_sig = d.output_pin("KEY_sig", 536, 112)
    hex0 = d.output_pin("HEX0[7..0]", 1120, 40)
    hex1 = d.output_pin("HEX1[7..0]", 1120, 56)
    hex2 = d.output_pin("HEX2[7..0]", 1120, 72)
    hex3 = d.output_pin("HEX3[7..0]", 1120, 88)
    o5m = d.output_pin("clk_5M", 440, 328)
    o10k = d.output_pin("clk_10k", 440, 360)
    o50 = d.output_pin("clk_50", 440, 408)

    d.wire(key0, keyin["k_in"])

    # KEY0 path -> OR
    d.wire(keyin["k_out"], (400, 96), (400, 80), or2["IN1"])
    # KEY1 is inverted, then -> OR
    d.wire(key1, n_key1["IN"])
    d.wire(n_key1["OUT"], (424, 224), (424, 96), or2["IN2"])

    d.wire(or2["OUT"], (536, 88), (536, 64), red["KEY_IN"])
    d.wire((536, 88), (536, 120))
    d.junction((536, 88))

    d.wire(red["D"], (776, 64), (776, 48), seg["Num"], bus=True)
    d.wire((776, 64), (776, 176), bus=True)
    d.junction((776, 64))

    d.wire(seg["HEX0"], hex0, bus=True)
    d.wire(seg["HEX1"], hex1, bus=True)
    d.wire(seg["HEX2"], hex2, bus=True)
    d.wire(seg["HEX3"], hex3, bus=True)

    d.wire(clk50, fen["clk_50M"])

    # 50 Hz clock drives the debounce module
    d.wire(fen["clk_50"], (392, 416), o50)
    d.wire((392, 416), (392, 240), (184, 240), (184, 112), keyin["clk"])
    d.junction((392, 416))

    d.wire(fen["clk_5M"], o5m)
    d.wire(fen["clk_10k"], o10k)

    d.save(os.path.join(OUT, "exp5_top.bdf"))


top()
print("top done")
