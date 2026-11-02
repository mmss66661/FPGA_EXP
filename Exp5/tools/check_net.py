"""Extract the connectivity of a .bdf file (pins, symbol ports, wires, junctions)."""
import re
import sys
from collections import defaultdict


def blocks(text):
    out = []
    i, n = 0, len(text)
    while i < n:
        if text[i] == "(":
            depth, j = 1, i + 1
            while j < n and depth:
                depth += {"(": 1, ")": -1}.get(text[j], 0)
                j += 1
            out.append(text[i:j])
            i = j
        else:
            i += 1
    return out


def head(b):
    m = re.match(r"\(([a-zA-Z_]+)", b)
    return m.group(1) if m else ""


def texts(b):
    return re.findall(r'\(text "([^"]*)"', b)


def rect(b):
    m = re.search(r"\(rect (-?\d+) (-?\d+) (-?\d+) (-?\d+)\)", b)
    return tuple(map(int, m.groups())) if m else None


def points(b):
    return [tuple(map(int, m.groups())) for m in re.finditer(r"\(pt (-?\d+) (-?\d+)\)", b)]


def analyse(path):
    txt = open(path, encoding="utf-8", newline="").read()
    syms, pins, segs, juncs = [], [], [], []
    for b in blocks(txt):
        h = head(b)
        if h == "symbol":
            r = rect(b)
            ts = texts(b)
            ports = []
            for ib in blocks(b[1:]):
                if head(ib) == "port":
                    name = texts(ib)[0]
                    ports.append((name, (r[0] + points(ib)[0][0], r[1] + points(ib)[0][1])))
            syms.append((ts[0], ts[1] if len(ts) > 1 else "", ports))
        elif h == "pin":
            ts, pts, r = texts(b), points(b), rect(b)
            pins.append((ts[1], (r[0] + pts[0][0], r[1] + pts[0][1])))
        elif h == "connector":
            p = points(b)
            if len(p) == 2:
                segs.append(tuple(p))
        elif h == "junction":
            p = points(b)
            if p:
                juncs.append(p[0])

    def on_seg(p, s):
        (x1, y1), (x2, y2) = s
        if x1 == x2:
            return p[0] == x1 and min(y1, y2) <= p[1] <= max(y1, y2)
        if y1 == y2:
            return p[1] == y1 and min(x1, x2) <= p[0] <= max(x1, x2)
        return False

    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for s in segs:
        union(s[0], s[1])
        for j in juncs:
            if on_seg(j, s):
                union(s[0], j)
        for _, p in pins:
            if on_seg(p, s):
                union(s[0], p)
        for _, _, ports in syms:
            for _, p in ports:
                if on_seg(p, s):
                    union(s[0], p)

    nets = defaultdict(list)
    for name, p in pins:
        nets[find(p)].append(name)
    for kind, inst, ports in syms:
        for name, p in ports:
            nets[find(p)].append("%s.%s" % (inst, name))

    print("==", path)
    print("  instances:", ["%s(%s)" % (i, k) for k, i, _ in syms])
    for members in sorted(nets.values(), key=len, reverse=True):
        if len(members) >= 2:
            print("  " + " -- ".join(sorted(set(members))))
    singles = [m[0] for m in nets.values() if len(m) == 1]
    if singles:
        print("  open:", ", ".join(sorted(singles)))


for f in sys.argv[1:]:
    analyse(f)
