"""Push-apart de componentes amontoados (abre canais de roteamento) com ancora na posicao original.
RODAR SO EM PLACA RIPADA (ripup.py antes) e com backup. Edita o .kicad_pcb em texto.
Uso: python -I spread.py placa.kicad_pcb --bounds XMIN XMAX YMIN YMAX [--fixed U1,U6] [--fixed-prefix J,H,X,SW]
     [--fixed-band "y<20"] [--gap 0.6] [--anchor 0.010] [--dry]
--bounds: area util (mm) onde as pecas moveis podem ficar (dentro da Edge.Cuts, com margem).
--fixed-band: expressao simples em x/y (mm) que congela uma faixa (ex.: regiao de RF junto as antenas)."""
import sys, io, re, math, argparse
ap = argparse.ArgumentParser()
ap.add_argument("board"); ap.add_argument("--bounds", nargs=4, type=float, required=True)
ap.add_argument("--fixed", default=""); ap.add_argument("--fixed-prefix", default="J,H,X,SW")
ap.add_argument("--fixed-band", default=""); ap.add_argument("--gap", type=float, default=1.0)  # folga extra entre raios; coerente com a tabela de montagem da fabrica (JLC: QFN >= 1,0 mm)
ap.add_argument("--anchor", type=float, default=0.010); ap.add_argument("--dry", action="store_true")
A = ap.parse_args()
board = A.board
FIXED = set(s for s in A.fixed.split(",") if s); PREF = tuple(s for s in A.fixed_prefix.split(",") if s)
t = io.open(board, encoding="utf-8").read()

# Split into footprint blocks
hdr = "\n\t(footprint "
idxs = [m.start() for m in re.finditer(re.escape(hdr), t)]
blocks = []
for i, s in enumerate(idxs):
    e = idxs[i+1] if i+1 < len(idxs) else t.find("\n\t(gr_", s)
    if e < 0: e = len(t)
    blocks.append((s, e))

def radius(name):
    n = name
    if "ESP32-C5-WROOM" in n: return 13.0
    if "microSD" in n: return 9.0
    if "USB_C" in n: return 7.0
    if "SMA" in n: return 6.0
    if "SSOP-28" in n or "TSSOP-28" in n: return 8.0
    if "ublox_MAX" in n: return 7.0
    if "SOIC-8" in n: return 5.5
    if "QFN" in n or "DFN" in n: return 5.5
    if "SOT-23" in n: return 3.4
    if "Crystal" in n: return 2.4
    if "SW_Slide" in n: return 7.0
    if "B3U-1000P" in n or "JS102011" in n: return 3.0
    if "0805" in n or "1210" in n: return 2.2
    if "0603" in n: return 1.8
    if "0402" in n: return 1.5
    if "PinHeader" in n or "JST" in n or "MountingHole" in n: return 5.0
    return 3.0

comps = []  # dict: ref,name,x,y,rot,atspan(local),radius,fixed
for (s,e) in blocks:
    blk = t[s:e]
    mname = re.search(r'\(footprint "([^"]+)"', blk)
    mref = re.search(r'\(property "Reference" "([^"]+)"', blk)
    mat = re.search(r'(?m)^\t\t\(at ([\-0-9.]+) ([\-0-9.]+)(?: ([\-0-9.]+))?\)', blk)
    if not (mname and mref and mat): continue
    name = mname.group(1); ref = mref.group(1)
    x = float(mat.group(1)); y = float(mat.group(2)); rot = mat.group(3)
    r = radius(name)
    band = bool(A.fixed_band) and eval(A.fixed_band, {"__builtins__": {}}, {"x": x, "y": y})
    fixed = ref.startswith(PREF) or ref in FIXED or band
    comps.append(dict(ref=ref,name=name,x=x,y=y,rot=rot,r=r,fixed=fixed,
                      s=s, at_s=s+mat.start(), at_e=s+mat.end(), ox=x, oy=y))

movable = [c for c in comps if not c["fixed"]]
print("total %d, movable %d, fixed %d" % (len(comps), len(movable), len(comps)-len(movable)))

GAP = A.gap
ANCHOR = A.anchor
XMIN,XMAX,YMIN,YMAX = A.bounds
for it in range(500):
    for m in movable:
        fx=fy=0.0
        for o in comps:
            if o is m: continue
            dx = m["x"]-o["x"]; dy = m["y"]-o["y"]
            d = math.hypot(dx,dy)
            need = m["r"]+o["r"]+GAP
            if d < need:
                if d < 1e-6:
                    dx,dy,d = 0.3,0.2,0.36
                push = (need-d)
                fx += push*dx/d; fy += push*dy/d
        # anchor to original
        fx += ANCHOR*(m["ox"]-m["x"]); fy += ANCHOR*(m["oy"]-m["y"])
        step = 0.5
        m["x"] += max(-1.5,min(1.5, fx*step))
        m["y"] += max(-1.5,min(1.5, fy*step))
        m["x"] = max(XMIN+m["r"], min(XMAX-m["r"], m["x"]))
        m["y"] = max(YMIN+m["r"], min(YMAX-m["r"], m["y"]))

# round to grid 0.05
for m in movable:
    m["x"] = round(m["x"]*20)/20.0
    m["y"] = round(m["y"]*20)/20.0

# report max displacement
disp = sorted(((math.hypot(m["x"]-m["ox"],m["y"]-m["oy"]),m["ref"]) for m in movable), reverse=True)
print("max disp:", [(round(d,1),r) for d,r in disp[:8]])

# write back (replace at spans from end to start to keep offsets)
edits = sorted(movable, key=lambda m:m["at_s"], reverse=True)
for m in edits:
    rotpart = (" %s" % m["rot"]) if m["rot"] is not None else ""
    newat = "\t\t(at %s %s%s)" % (("%g"%m["x"]),("%g"%m["y"]),rotpart)
    t = t[:m["at_s"]] + newat + t[m["at_e"]:]
if A.dry:
    print("dry run: nada gravado"); sys.exit(0)
io.open(board,"w",encoding="utf-8",newline="").write(t)
print("written. movable moved:", sum(1 for m in movable if abs(m["x"]-m["ox"])>0.05 or abs(m["y"]-m["oy"])>0.05))
