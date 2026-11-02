import os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Vwf:
    def __init__(self, duration, grid=10.0):
        self.duration = float(duration)
        self.grid = grid
        self.signals = []      # (name, direction, transitions, width, parent)

    def add(self, name, direction, transitions=None, width=1, parent=""):
        self.signals.append((name, direction, transitions, width, parent))

    def add_bus(self, name, direction, width):
        self.add(name, direction, width=width)
        for bit in range(width - 1, -1, -1):
            self.add("%s[%d]" % (name, bit), direction, parent=name)

    def save(self, path):
        out = [
            "/* Vector Waveform File for experiment 5 */",
            "HEADER",
            "{",
            "\tVERSION = 1;",
            "\tTIME_UNIT = ns;",
            "\tDATA_OFFSET = 0.0;",
            "\tDATA_DURATION = %.1f;" % self.duration,
            "\tSIMULATION_TIME = 0.0;",
            "\tGRID_PHASE = 0.0;",
            "\tGRID_PERIOD = %.1f;" % self.grid,
            "\tGRID_DUTY_CYCLE = 50;",
            "}",
            "",
        ]
        for name, direction, _, width, parent in self.signals:
            signal_type = "BUS" if width > 1 else "SINGLE_BIT"
            lsb_index = 0 if width > 1 else -1
            out += [
                'SIGNAL("%s")' % name,
                "{",
                "\tVALUE_TYPE = NINE_LEVEL_BIT;",
                "\tSIGNAL_TYPE = %s;" % signal_type,
                "\tWIDTH = %d;" % width,
                "\tLSB_INDEX = %d;" % lsb_index,
                "\tDIRECTION = %s;" % direction,
                '\tPARENT = "%s";' % parent,
                "}",
                "",
            ]
        for name, direction, transitions, width, parent in self.signals:
            if width > 1:
                continue
            out.append('TRANSITION_LIST("%s")' % name)
            out.append("{")
            if transitions is None:
                out += ["\tNODE", "\t{", "\t\tREPEAT = 1;",
                        "\t\tLEVEL X FOR %.1f;" % self.duration, "\t}"]
            elif isinstance(transitions, tuple) and transitions[0] == "clock":
                _, half, count = transitions
                out += ["\tNODE", "\t{", "\t\tREPEAT = 1;", "\t\tNODE", "\t\t{",
                        "\t\t\tREPEAT = %d;" % count,
                        "\t\t\tLEVEL 0 FOR %.1f;" % half,
                        "\t\t\tLEVEL 1 FOR %.1f;" % half,
                        "\t\t}", "\t}"]
            else:
                out.append("\tNODE")
                out.append("\t{")
                out.append("\t\tREPEAT = 1;")
                for level, duration in transitions:
                    out.append("\t\tLEVEL %s FOR %.1f;" % (level, duration))
                out.append("\t}")
            out.append("}")
            out.append("")
        for idx, (name, _, _, width, parent) in enumerate(self.signals):
            out += ['DISPLAY_LINE', '{', '\tCHANNEL = "%s";' % name,
                    "\tEXPAND_STATUS = COLLAPSED;", "\tRADIX = Binary;",
                    "\tTREE_INDEX = %d;" % idx,
                    "\tTREE_LEVEL = %d;" % (1 if parent else 0)]
            if width > 1:
                children = ", ".join(str(idx + n) for n in range(1, width + 1))
                out.append("\tCHILDREN = %s;" % children)
            out += ["}", ""]
        out += ["TIME_BAR", "{", "\tTIME = 0;", "\tMASTER = TRUE;", "}", ";", ""]
        open(path, "w", encoding="utf-8", newline="\r\n").write("\n".join(out))


def task1():
    v = Vwf(1000)
    v.add("clk1", "INPUT", ("clock", 20.0, 25))
    v.add("Sd1", "INPUT", [("1", 90), ("0", 80), ("1", 830)])
    v.add("Rd1", "INPUT", [("1", 250), ("0", 80), ("1", 670)])
    v.add("D1", "INPUT", [("0", 400), ("1", 200), ("0", 400)])
    v.add("Q1", "OUTPUT")
    v.add("Q1N", "OUTPUT")
    v.save(os.path.join(OUT, "exp5_t1_7474.vwf"))


def task2():
    v = Vwf(1200)
    v.add("clk1", "INPUT", ("clock", 20.0, 30))
    v.add("Sd1", "INPUT", [("1", 90), ("0", 80), ("1", 1030)])
    v.add("Rd1", "INPUT", [("1", 250), ("0", 80), ("1", 870)])
    v.add("J1", "INPUT", [("0", 410), ("1", 80), ("0", 80), ("1", 160), ("0", 470)])
    v.add("K1", "INPUT", [("0", 410), ("0", 80), ("1", 80), ("1", 160), ("0", 470)])
    v.add("Q1", "OUTPUT")
    v.add("Q1N", "OUTPUT")
    v.save(os.path.join(OUT, "exp5_t2_74112.vwf"))


def task4_jk2d():
    v = Vwf(1000)
    v.add("clk1", "INPUT", ("clock", 20.0, 25))
    v.add("Sd1", "INPUT", [("1", 90), ("0", 80), ("1", 830)])
    v.add("Rd1", "INPUT", [("1", 250), ("0", 80), ("1", 670)])
    v.add("D1", "INPUT", [("0", 450), ("1", 200), ("0", 200), ("1", 150)])
    v.add("Q1", "OUTPUT")
    v.add("Q1N", "OUTPUT")
    v.save(os.path.join(OUT, "exp5_t4_jk2d.vwf"))


def task4_jk2t():
    v = Vwf(1000)
    v.add("clk1", "INPUT", ("clock", 20.0, 25))
    v.add("Sd1", "INPUT", [("1", 90), ("0", 80), ("1", 830)])
    v.add("Rd1", "INPUT", [("1", 250), ("0", 80), ("1", 670)])
    v.add("T1", "INPUT", [("0", 410), ("1", 400), ("0", 190)])
    v.add("Q1", "OUTPUT")
    v.add("Q1N", "OUTPUT")
    v.save(os.path.join(OUT, "exp5_t4_jk2t.vwf"))


def _key_press():
    return [
        ("1", 40000000),
        ("0", 200000), ("1", 200000), ("0", 200000), ("1", 200000),
        ("0", 59200000),
        ("1", 200000), ("0", 200000), ("1", 200000), ("0", 200000),
        ("1", 59200000),
    ]


def top_key0():
    v = Vwf(160000000, grid=1000000.0)
    v.add("CLK_50M", "INPUT", ("clock", 10.0, 8000000))
    v.add("KEY0", "INPUT", _key_press())
    v.add("KEY1", "INPUT", [("1", 160000000)])
    v.add_bus("KD", "OUTPUT", 16)
    v.save(os.path.join(OUT, "exp5_top.vwf"))


def top_key1():
    v = Vwf(160000000, grid=1000000.0)
    v.add("CLK_50M", "INPUT", ("clock", 10.0, 8000000))
    v.add("KEY0", "INPUT", [("1", 160000000)])
    v.add("KEY1", "INPUT", _key_press())
    v.add_bus("KD", "OUTPUT", 16)
    v.save(os.path.join(OUT, "exp5_top_key1.vwf"))


def counter():
    v = Vwf(2000)
    v.add("KEY_IN", "INPUT", ("clock", 50.0, 20))
    v.add_bus("D", "OUTPUT", 16)
    v.save(os.path.join(OUT, "rising_edge_detect.vwf"))


def keyin():
    v = Vwf(4000)
    v.add("clk", "INPUT", ("clock", 100.0, 20))
    v.add("k_in", "INPUT", [("1", 400), ("0", 20), ("1", 20), ("0", 20), ("1", 20),
                            ("0", 1120), ("1", 20), ("0", 20), ("1", 2360)])
    v.add("k_out", "OUTPUT")
    v.add("Q0", "OUTPUT")
    v.add("Q1", "OUTPUT")
    v.add("Q2", "OUTPUT")
    v.save(os.path.join(OUT, "keyin.vwf"))


task1()
task2()
task4_jk2d()
task4_jk2t()
top_key0()
top_key1()
counter()
keyin()
print("vwf files written")
