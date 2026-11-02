import os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SOURCES = [
    "exp5_t1_7474.bdf",
    "exp5_t2_74112.bdf",
    "keyin.bdf",
    "exp5_t4_jk2d.bdf",
    "exp5_t4_jk2t.bdf",
    "exp5_top.bdf",
    "fenpin.vhd",
    "rising_edge_detect.vhd",
    "seg_show.vhd",
]

TASK12 = [
    ("clk1", "PIN_F15"), ("Sd1", "PIN_A7"), ("Rd1", "PIN_B8"),
    ("D1", "PIN_A14"), ("Q1", "PIN_A8"), ("Q1N", "PIN_A9"),
    ("J1", "PIN_C11"), ("K1", "PIN_C10"), ("T1", "PIN_C11"),
]

HEX = {
    "HEX0": ["C14", "E15", "C15", "C16", "E16", "D17", "C17", "D15"],
    "HEX1": ["C18", "D18", "E18", "B16", "A17", "A18", "B17", "A16"],
    "HEX2": ["B20", "A20", "B19", "A21", "B21", "C22", "B22", "A19"],
    "HEX3": ["F21", "E22", "E21", "C19", "C20", "D19", "E17", "D22"],
}

TASK3 = [("CLK_50M", "PIN_P11"), ("KEY0", "PIN_W5"), ("KEY1", "PIN_AA15")]


def build(top="exp5_top"):
    qsf = [
        "# Quartus Prime settings generated for experiment 5",
        'set_global_assignment -name FAMILY "MAX 10"',
        "set_global_assignment -name DEVICE 10M50DAF484C7G",
        "set_global_assignment -name TOP_LEVEL_ENTITY %s" % top,
        "set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files",
        "set_global_assignment -name MIN_CORE_JUNCTION_TEMP 0",
        "set_global_assignment -name MAX_CORE_JUNCTION_TEMP 85",
        "set_global_assignment -name ERROR_CHECK_FREQUENCY_DIVISOR 256",
        "set_global_assignment -name NUM_PARALLEL_PROCESSORS 4",
        'set_global_assignment -name RESERVE_ALL_UNUSED_PINS_WEAK_PULLUP "AS INPUT TRI-STATED"',
    ]
    for f in SOURCES:
        key = "VHDL_FILE" if f.endswith(".vhd") else "BDF_FILE"
        qsf.append("set_global_assignment -name %s %s" % (key, f))
    for name, pin in TASK12:
        qsf.append("set_location_assignment %s -to %s" % (pin, name))
    for name, pin in TASK3:
        qsf.append("set_location_assignment %s -to %s" % (pin, name))
    for hexname, pins in HEX.items():
        for bit, pin in enumerate(pins):
            qsf.append("set_location_assignment PIN_%s -to %s[%d]" % (pin, hexname, bit))
    open(os.path.join(OUT, "exp5.qsf"), "w", encoding="utf-8", newline="\r\n").write("\n".join(qsf) + "\n")


if __name__ == "__main__":
    build()
    print("exp5.qsf written")
