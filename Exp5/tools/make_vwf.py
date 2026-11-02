import os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Vwf:
    def __init__(self, duration, grid=10.0):
        self.duration = float(duration)
        self.grid = grid
        self.signals = []      # (name, direction, transitions or None)

    def add(self, name, direction, transitions=None):
        self.signals.append((name, direction, transitions))

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
        for name, direction, _ in self.signals:
            out += [
                'SIGNAL("%s")' % name,
                "{",
                "\tVALUE_TYPE = NINE_LEVEL_BIT;",
                "\tSIGNAL_TYPE = SINGLE_BIT;",
                "\tWIDTH = 1;",
                "\tLSB_INDEX = -1;",
                "\tDIRECTION = %s;" % direction,
                '\tPARENT = "";',
                "}",
                "",
            ]
        for name, direction, transitions in self.signals:
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
        for idx, (name, _, _) in enumerate(self.signals):
            out += ['DISPLAY_LINE', '{', '\tCHANNEL = "%s";' % name,
                    "\tEXPAND_STATUS = COLLAPSED;", "\tRADIX = Binary;",
                    "\tTREE_INDEX = %d;" % idx, "\tTREE_LEVEL = 0;", "}", ""]
        out += ["TIME_BAR", "{", "\tTIME = 0;", "\tMASTER = TRUE;", "}", ";", ""]
        open(path, "w", encoding="utf-8", newline="\r\n").write("\n".join(out))


def task1():
    v = Vwf(1000)
    v.add("clk1", "INPUT", ("clock", 20.0, 25))
    v.add("Sd1", "INPUT", [("1", 80), ("0", 80), ("1", 840)])
    v.add("Rd1", "INPUT", [("1", 240), ("0", 80), ("1", 680)])
    v.add("D1", "INPUT", [("0", 400), ("1", 200), ("0", 200), ("1", 200)])
    v.add("Q1", "OUTPUT")
    v.add("Q1N", "OUTPUT")
    v.save(os.path.join(OUT, "exp5_t1_7474.vwf"))


def task2():
    v = Vwf(1200)
    v.add("clk1", "INPUT", ("clock", 20.0, 30))
    v.add("Sd1", "INPUT", [("1", 80), ("0", 80), ("1", 1040)])
    v.add("Rd1", "INPUT", [("1", 240), ("0", 80), ("1", 880)])
    v.add("J1", "INPUT", [("0", 400), ("1", 80), ("0", 80), ("1", 160), ("0", 480)])
    v.add("K1", "INPUT", [("0", 400), ("0", 80), ("1", 80), ("1", 160), ("0", 480)])
    v.add("Q1", "OUTPUT")
    v.add("Q1N", "OUTPUT")
    v.save(os.path.join(OUT, "exp5_t2_74112.vwf"))


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
keyin()
print("vwf files written")
