"""Ground isolated GND pads: for each pad listed as unconnected in the DRC json,
find a clearance-safe via spot and a clearance-safe straight F.Cu stub to it."""
import sys, json, math, re, io
import pcbnew

BOARD, DRCJSON = sys.argv[1], sys.argv[2]
DRY = len(sys.argv) > 3 and sys.argv[3] == "dry"
mm = pcbnew.ToMM
board = pcbnew.LoadBoard(BOARD)
gnd = board.FindNet("GND")
GNDC = gnd.GetNetCode()

FINE = len(sys.argv) > 4
CLR = 0.195 if FINE else 0.22          # copper clearance used (rule is 0.18)
VIA_R, VIA_DRILL = 0.30, 0.30
TW = 0.25           # stub width
F_CU, B_CU = pcbnew.F_Cu, pcbnew.B_Cu

# ---------------- geometry helpers ----------------
def pt_seg(px, py, ax, ay, bx, by):
    dx, dy = bx-ax, by-ay
    L2 = dx*dx+dy*dy
    if L2 < 1e-12: return math.hypot(px-ax, py-ay)
    t = max(0, min(1, ((px-ax)*dx+(py-ay)*dy)/L2))
    return math.hypot(px-(ax+t*dx), py-(ay+t*dy))

def seg_inter(a, b, c, d):
    def o(p, q, r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    o1, o2, o3, o4 = o(a,b,c), o(a,b,d), o(c,d,a), o(c,d,b)
    return (o1*o2 < 0) and (o3*o4 < 0)

def seg_seg(a, b, c, d):
    if seg_inter(a, b, c, d): return 0.0
    return min(pt_seg(a[0],a[1],c[0],c[1],d[0],d[1]), pt_seg(b[0],b[1],c[0],c[1],d[0],d[1]),
               pt_seg(c[0],c[1],a[0],a[1],b[0],b[1]), pt_seg(d[0],d[1],a[0],a[1],b[0],b[1]))

def pt_rect(px, py, r):
    x1, y1, x2, y2 = r
    dx = max(x1-px, 0, px-x2); dy = max(y1-py, 0, py-y2)
    return math.hypot(dx, dy)

def seg_rect(a, b, r):
    x1, y1, x2, y2 = r
    if pt_rect(a[0],a[1],r) == 0 or pt_rect(b[0],b[1],r) == 0: return 0.0
    cs = [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]
    return min(seg_seg(a, b, cs[i], cs[(i+1)%4]) for i in range(4))

# ---------------- obstacles ----------------
segs = []    # (ax,ay,bx,by,halfw,layer,net)
vias = []    # (x,y,r,net)
for t in board.GetTracks():
    if t.Type() == pcbnew.PCB_VIA_T:
        vias.append((mm(t.GetX()), mm(t.GetY()), mm(t.GetWidth(F_CU))/2, t.GetNetCode()))
    else:
        s, e = t.GetStart(), t.GetEnd()
        segs.append((mm(s.x), mm(s.y), mm(e.x), mm(e.y), mm(t.GetWidth())/2, t.GetLayer(), t.GetNetCode()))
pads = []    # (rect, net, onF, onB, ref, num)
padmap = {}
for fp in board.GetFootprints():
    for p in fp.Pads():
        bb = p.GetBoundingBox()
        r = (mm(bb.GetLeft()), mm(bb.GetTop()), mm(bb.GetRight()), mm(bb.GetBottom()))
        thru = p.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH)
        onF = thru or p.IsOnLayer(F_CU); onB = thru or p.IsOnLayer(B_CU)
        pads.append((r, p.GetNetCode(), onF, onB, fp.GetReference(), p.GetNumber()))
        padmap.setdefault((fp.GetReference(), p.GetNumber()), []).append(p)
noVia = [z for z in board.Zones() if z.GetIsRuleArea() and z.GetDoNotAllowVias()]
noTrk = [z for z in board.Zones() if z.GetIsRuleArea() and z.GetDoNotAllowTracks()]
ebb = board.GetBoardEdgesBoundingBox()
EX1, EY1, EX2, EY2 = mm(ebb.GetLeft()), mm(ebb.GetTop()), mm(ebb.GetRight()), 80.0

def in_area(zs, x, y):
    v = pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))
    return any(z.Outline().Contains(v) for z in zs)

def via_ok(x, y):
    if not (EX1+0.7 < x < EX2-0.7 and EY1+0.7 < y < EY2-0.7): return False
    if in_area(noVia, x, y): return False
    for (ax,ay,bx,by,hw,ly,net) in segs:          # through via: every layer
        if net != GNDC and pt_seg(x,y,ax,ay,bx,by) < VIA_R+hw+CLR: return False
    for (vx,vy,vr,net) in vias:
        d = math.hypot(x-vx, y-vy)
        if net != GNDC and d < VIA_R+vr+CLR: return False
        if d < 0.75: return False                    # hole-to-hole / stacking
    for (r,net,onF,onB,ref,num) in pads:
        d = pt_rect(x, y, r)
        if net != GNDC:
            if d < VIA_R+CLR+(0.03 if FINE else 0.08): return False      # copper + mask margin
        elif d < VIA_R+0.10: return False            # keep out of GND pads too (no via-in-pad)
    return True

def stub_ok(a, b, TW=TW, CLR=CLR):
    for (ax,ay,bx,by,hw,ly,net) in segs:
        if ly == F_CU and net != GNDC and seg_seg(a,b,(ax,ay),(bx,by)) < TW/2+hw+CLR: return False
    for (vx,vy,vr,net) in vias:
        if net != GNDC and pt_seg(vx,vy,a[0],a[1],b[0],b[1]) < TW/2+vr+CLR: return False
    for (r,net,onF,onB,ref,num) in pads:
        if onF and net != GNDC and seg_rect(a,b,r) < TW/2+CLR: return False
    mx, my = (a[0]+b[0])/2, (a[1]+b[1])/2
    if in_area(noTrk, mx, my): return False
    return True

# ---------------- targets ----------------
targets = []
if DRCJSON.endswith(".txt"):
    targets = [tuple(l.split()) for l in io.open(DRCJSON, encoding="utf-8").read().splitlines() if l.strip()]
    viol = []
else:
    d = json.load(io.open(DRCJSON, encoding="utf-8"))
    viol = d if isinstance(d, list) else d.get("violations", d.get("items", []))
for x in viol:
    if x.get("type") != "unconnected_items": continue
    for it in x.get("items", []):
        m = re.search(r"Pad (\S+) \[GND\] of (\w+)", it.get("description", ""))
        if m and (m.group(2), m.group(1)) not in targets:
            targets.append((m.group(2), m.group(1)))

done, fail = [], []
for ref, num in targets:
    for p in padmap.get((ref, num), []):
        if p.GetNetCode() != GNDC or not p.IsOnLayer(F_CU): continue
        px, py = mm(p.GetPosition().x), mm(p.GetPosition().y)
        best = None
        for rr in [x/20.0 for x in range(13, 121, (1 if FINE else 4))]:
            for ang in range(0, 360, (3 if FINE else 10)):
                vx = px + rr*math.cos(math.radians(ang)); vy = py + rr*math.sin(math.radians(ang))
                if via_ok(vx, vy) and stub_ok((px, py), (vx, vy)):
                    best = (round(vx, 3), round(vy, 3)); break
            if best: break
        def add_track(a, b, w):
            segs.append((a[0], a[1], b[0], b[1], w/2, F_CU, GNDC))
            if not DRY:
                tr = pcbnew.PCB_TRACK(board)
                tr.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(a[0]), pcbnew.FromMM(a[1])))
                tr.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(b[0]), pcbnew.FromMM(b[1])))
                tr.SetWidth(pcbnew.FromMM(w)); tr.SetLayer(F_CU); tr.SetNetCode(GNDC); board.Add(tr)
        if not best:
            # Fallback A: straight 0.2 mm stub into a GND pad of the same part that is not itself a target (EP)
            okA = False
            for (r, net, onF, onB, r2, n2) in pads:
                if r2 != ref or net != GNDC or not onF or (r2, n2) in targets: continue
                tx = min(max(px, r[0]+0.15), r[2]-0.15); ty = min(max(py, r[1]+0.15), r[3]-0.15)
                if math.hypot(tx-px, ty-py) < 4 and stub_ok((px, py), (tx, ty), 0.2, 0.19):
                    add_track((px, py), (tx, ty), 0.2)
                    done.append("%s.%s -> EP/pad %s (%.1fmm)" % (ref, num, n2, math.hypot(tx-px, ty-py)))
                    okA = True; break
            if okA: continue
            # Fallback B: dog-leg (waypoint) to a via
            okB = False
            for r1 in [x/10.0 for x in range(4, 31, 2)]:
                for a1 in range(0, 360, 15):
                    wx = px + r1*math.cos(math.radians(a1)); wy = py + r1*math.sin(math.radians(a1))
                    if not stub_ok((px, py), (wx, wy), 0.2, 0.19): continue
                    for r2_ in [x/10.0 for x in range(8, 41, 4)]:
                        for a2 in range(0, 360, 15):
                            vx = wx + r2_*math.cos(math.radians(a2)); vy = wy + r2_*math.sin(math.radians(a2))
                            if via_ok(vx, vy) and stub_ok((wx, wy), (vx, vy), 0.2, 0.19):
                                okB = (round(wx,3), round(wy,3), round(vx,3), round(vy,3)); break
                        if okB: break
                    if okB: break
                if okB: break
            if not okB:
                fail.append("%s.%s @%.2f,%.2f" % (ref, num, px, py)); continue
            wx, wy, vx, vy = okB
            add_track((px, py), (wx, wy), 0.2); add_track((wx, wy), (vx, vy), 0.2)
            vias.append((vx, vy, VIA_R, GNDC))
            if not DRY:
                v = pcbnew.PCB_VIA(board)
                v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(vx), pcbnew.FromMM(vy)))
                v.SetWidth(F_CU, pcbnew.FromMM(2*VIA_R)); v.SetDrill(pcbnew.FromMM(VIA_DRILL))
                v.SetLayerPair(F_CU, B_CU); v.SetNetCode(GNDC); board.Add(v)
            done.append("%s.%s -> dogleg via %.2f,%.2f" % (ref, num, vx, vy))
            continue
        vx, vy = best
        done.append("%s.%s -> via %.2f,%.2f (%.1fmm)" % (ref, num, vx, vy, math.hypot(vx-px, vy-py)))
        vias.append((vx, vy, VIA_R, GNDC))
        segs.append((px, py, vx, vy, TW/2, F_CU, GNDC))
        if not DRY:
            v = pcbnew.PCB_VIA(board)
            v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(vx), pcbnew.FromMM(vy)))
            v.SetWidth(F_CU, pcbnew.FromMM(2*VIA_R)); v.SetDrill(pcbnew.FromMM(VIA_DRILL))
            v.SetLayerPair(F_CU, B_CU); v.SetNetCode(GNDC); board.Add(v)
            tr = pcbnew.PCB_TRACK(board)
            tr.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py)))
            tr.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(vx), pcbnew.FromMM(vy)))
            tr.SetWidth(pcbnew.FromMM(TW)); tr.SetLayer(F_CU); tr.SetNetCode(GNDC); board.Add(tr)

print("targets:", len(targets), " fixed:", len(done), " failed:", len(fail))
for s in done: print("  OK  ", s)
for s in fail: print("  FAIL", s)
if not DRY:
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(BOARD, board)
    print("saved + zones refilled")
