"""Helpers to generate Quartus Block Design Files (.bdf) and symbols (.bsf)."""
import os
import re

LIB = r"D:\quartus\quartus\libraries"

PRIM = {
    "dff": os.path.join(LIB, "primitives", "storage", "dff.bsf"),
    "and2": os.path.join(LIB, "primitives", "logic", "and2.bsf"),
    "and3": os.path.join(LIB, "primitives", "logic", "and3.bsf"),
    "or2": os.path.join(LIB, "primitives", "logic", "or2.bsf"),
    "not": os.path.join(LIB, "primitives", "logic", "not.bsf"),
    "vcc": os.path.join(LIB, "primitives", "other", "vcc.bsf"),
    "gnd": os.path.join(LIB, "primitives", "other", "gnd.bsf"),
    "7474": os.path.join(LIB, "others", "maxplus2", "7474.bsf"),
    "74112": os.path.join(LIB, "others", "maxplus2", "74112.bsf"),
}


def blocks(text):
    """Return (start, end, block) for every balanced parenthesis block."""
    out = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == "(":
            depth = 1
            j = i + 1
            while j < n and depth > 0:
                if text[j] == "(":
                    depth += 1
                elif text[j] == ")":
                    depth -= 1
                j += 1
            out.append((i, j, text[i:j]))
            i = j
        else:
            i += 1
    return out


def points(block):
    return [tuple(map(int, m.groups()))
            for m in re.finditer(r"\(pt (-?\d+) (-?\d+)\)", block)]


class Symbol:
    """A symbol loaded from a .bsf file, or synthesised for a HDL entity."""

    def __init__(self, name, width, height, ports, body):
        self.name = name
        self.width = width
        self.height = height
        # ports: list of (port_name, direction, (x, y))
        self.ports = ports
        self.body = body  # inner s-expression text (ports + drawing)

    def port(self, name):
        for pname, direction, pos in self.ports:
            if pname == name:
                return pos
        for pname, direction, pos in self.ports:
            if pname.split("[")[0] == name:
                return pos
        raise KeyError("%s has no port %r (has %s)" %
                       (self.name, name, [p[0] for p in self.ports]))

    def port_dir(self, name):
        for pname, direction, pos in self.ports:
            if pname == name:
                return direction
        raise KeyError(name)


def load_symbol(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    sym = next(b for b in blocks(text) if b[2].startswith("(symbol"))
    body = sym[2]
    rect = re.search(r"\(rect (-?\d+) (-?\d+) (-?\d+) (-?\d+)\)", body)
    x1, y1, x2, y2 = map(int, rect.groups())
    ports = []
    for start, end, blk in blocks(body[1:]):
        if not blk.startswith("(port"):
            continue
        name = re.findall(r'\(text "([^"]*)"', blk)[0]
        direction = "in" if "(input)" in blk else "out"
        pos = points(blk)[0]
        ports.append((name, direction, pos))
    name = re.findall(r'\(text "([^"]*)"', body)[0]
    return Symbol(name, x2 - x1, y2 - y1, ports, body)


class Design:
    def __init__(self, title="exp5 design"):
        self.title = title
        self.items = []          # emitted blocks, in order
        self.wires = []          # list of ((x1,y1),(x2,y2))
        self.extra_junctions = set()
        self.symbols = []

    # ---------- primitives ----------
    def sym(self, symbol, x, y, inst):
        assert x % 8 == 0 and y % 8 == 0, (x, y)
        body = symbol.body
        body = re.sub(r"\(rect -?\d+ -?\d+ -?\d+ -?\d+\)",
                      "(rect %d %d %d %d)" % (x, y, x + symbol.width, y + symbol.height),
                      body, count=1)
        # replace the instance label (2nd text of the symbol header, before any port)
        head_end = body.find("(port")
        if head_end < 0:
            head_end = body.find("(drawing")
        if head_end < 0:
            head_end = len(body)
        header = body[:head_end]
        labels = list(re.finditer(r'\(text "([^"]*)"', header))
        if len(labels) >= 2:
            m = labels[1]
            header = header[:m.start()] + '(text "%s"' % inst + header[m.end():]
        body = header + body[head_end:]
        self.items.append(body)
        self.symbols.append((inst, symbol, x, y))
        ports = {}
        for name, _, (px, py) in symbol.ports:
            ports[name] = (x + px, y + py)
            ports.setdefault(name.split("[")[0], (x + px, y + py))
        return ports

    def inst(self, key, x, y, label):
        return self.sym(load_symbol(PRIM[key]), x, y, label)

    def input_pin(self, name, x, y):
        block = (
            "(pin\n\t(input)\n\t(rect %d %d %d %d)\n"
            '\t(text "INPUT" (rect 125 0 153 10)(font "Arial" (font_size 6)))\n'
            '\t(text "%s" (rect 5 0 45 12)(font "Arial" ))\n'
            "\t(pt 168 8)\n\t(drawing\n"
            "\t\t(line (pt 84 12)(pt 109 12))\n"
            "\t\t(line (pt 84 4)(pt 109 4))\n"
            "\t\t(line (pt 113 8)(pt 168 8))\n"
            "\t\t(line (pt 84 12)(pt 84 4))\n"
            "\t\t(line (pt 109 4)(pt 113 8))\n"
            "\t\t(line (pt 109 12)(pt 113 8))\n"
            "\t)\n"
            '\t(text "VCC" (rect 128 7 148 17)(font "Arial" (font_size 6)))\n'
            ")" % (x, y, x + 168, y + 16, name))
        self.items.append(block)
        return (x + 168, y + 8)

    def output_pin(self, name, x, y):
        block = (
            "(pin\n\t(output)\n\t(rect %d %d %d %d)\n"
            '\t(text "OUTPUT" (rect 1 0 39 10)(font "Arial" (font_size 6)))\n'
            '\t(text "%s" (rect 90 0 130 17)(font "Arial" ))\n'
            "\t(pt 0 8)\n\t(drawing\n"
            "\t\t(line (pt 0 8)(pt 52 8))\n"
            "\t\t(line (pt 52 4)(pt 78 4))\n"
            "\t\t(line (pt 52 12)(pt 78 12))\n"
            "\t\t(line (pt 52 12)(pt 52 4))\n"
            "\t\t(line (pt 78 4)(pt 82 8))\n"
            "\t\t(line (pt 82 8)(pt 78 12))\n"
            "\t)\n"
            "\t(annotation_block (location)(rect %d %d %d %d))\n"
            ")" % (x, y, x + 176, y + 16, name, x + 176, y + 16, x + 240, y + 40))
        self.items.append(block)
        return (x, y + 8)

    # ---------- wiring ----------
    def wire(self, *pts, bus=False):
        for a, b in zip(pts, pts[1:]):
            assert (a[0] == b[0]) or (a[1] == b[1]), "not orthogonal: %s %s" % (a, b)
            self.wires.append((a, b, bus))

    def junction(self, *pts):
        for p in pts:
            self.extra_junctions.add(p)

    def _auto_junctions(self):
        ends = {}
        for a, b, bus in self.wires:
            ends.setdefault(a, 0)
            ends.setdefault(b, 0)
            ends[a] += 1
            ends[b] += 1
        js = set(self.extra_junctions)
        for p, n in ends.items():
            if n >= 3:
                js.add(p)
        return sorted(js)

    def text(self, kind, x, y, body):
        self.items.append('(text "%s" (rect %d %d %d %d)(font "Arial" (font_size 8)))'
                          % (body, x, y, x + 8 * len(body), y + 12))

    def save(self, path):
        js = self._auto_junctions()
        out = ['(header "graphic" (version "1.4"))']
        out += self.items
        for a, b, bus in self.wires:
            out.append("(connector\n\t(pt %d %d)\n\t(pt %d %d)\n%s)"
                       % (a[0], a[1], b[0], b[1], "\t(bus)\n" if bus else ""))
        for x, y in js:
            out.append("(junction (pt %d %d))" % (x, y))
        open(path, "w", encoding="utf-8", newline="\r\n").write("\r\n".join(out) + "\r\n")


def write_bsf(path, name, ports, title=None):
    """ports: list of (port_name, direction, width) with width 1 or >1."""
    width = 160
    rows = max(len(ports), 2)
    height = 32 + 16 * rows
    lines = ['(header "symbol" (version "1.1"))',
             '(symbol (rect 0 0 %d %d)' % (width, height),
             '\t(text "%s" (rect 6 0 %d 16)(font "Arial" (font_size 10)))'
             % (name, 6 + 9 * len(name)),
             '\t(text "inst" (rect 3 %d 30 %d)(font "Arial" (font_size 6)))'
             % (height - 12, height + 2)]
    left = [p for p in ports if p[1] == "in"]
    right = [p for p in ports if p[1] == "out"]
    for idx, (pname, direction, w) in enumerate(left):
        y = 16 + 16 * idx
        label = pname + ("[%d..0]" % (w - 1) if w > 1 else "")
        lines.append('\t(port (pt 0 %d)(input)(text "%s" (rect 6 %d %d %d)'
                     '(font "Arial" (font_size 8)))(text "%s" (rect 6 %d %d %d)'
                     '(font "Arial" (font_size 8)))\n\t\t(line (pt 0 %d)(pt 16 %d)(line_width 1)))'
                     % (y, label, y - 7, 6 + 8 * len(label), y + 7,
                        label, y - 7, 6 + 8 * len(label), y + 7, y, y))
    for idx, (pname, direction, w) in enumerate(right):
        y = 16 + 16 * idx
        label = pname + ("[%d..0]" % (w - 1) if w > 1 else "")
        lines.append('\t(port (pt %d %d)(output)(text "%s" (rect %d %d %d %d)'
                     '(font "Arial" (font_size 8)))(text "%s" (rect %d %d %d %d)'
                     '(font "Arial" (font_size 8)))\n\t\t(line (pt %d %d)(pt %d %d)(line_width 1)))'
                     % (width, y, label, width - 8 - 8 * len(label), y - 7,
                        width - 8, y + 7, label, width - 8 - 8 * len(label), y - 7,
                        width - 8, y + 7, width - 8, y, width, y))
    lines.append('\t(drawing (text "%s"(rect 20 %d 130 %d)(font "Arial" (font_size 8)))'
                 % (title or name.upper(), height - 26, height - 14))
    lines.append('\t\t(line (pt 16 16)(pt 16 %d)(line_width 1))' % (height - 16))
    lines.append('\t\t(line (pt %d 16)(pt %d %d)(line_width 1))'
                 % (width - 16, width - 16, height - 16))
    lines.append('\t\t(line (pt 16 16)(pt %d 16)(line_width 1))' % (width - 16))
    lines.append('\t\t(line (pt 16 %d)(pt %d %d)(line_width 1)))' % (height - 16, width - 16, height - 16))
    lines.append(")")
    open(path, "w", encoding="utf-8", newline="\r\n").write("\r\n".join(lines) + "\r\n")
