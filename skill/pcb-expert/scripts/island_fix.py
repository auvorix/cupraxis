"""Aterra ILHAS do pour de GND: para cada regiao preenchida das zonas de GND sem via/pad passante de GND,
procura um ponto livre com folga e cria via(s) de costura. Ilhas pequenas demais vao para island_pads.txt
(passar ao gnd_fix.py). Rodar com o python.exe do KiCad. Uso: python island_fix.py placa.kicad_pcb x [dry]
Obs.: uma via por ilha e o minimo; em alta frequencia prefira varias vias ou remover ilhas pequenas."""
import sys, json, math, re, io
import pcbnew

BOARD, DRCJSON = sys.argv[1], sys.argv[2]
DRY = len(sys.argv) > 3 and sys.argv[3] == "dry"
mm = pcbnew.ToMM
board = pcbnew.LoadBoard(BOARD)
gnd = board.FindNet("GND")
GNDC = gnd.GetNetCode()

CLR = 0.22          # copper clearance used (rule is 0.18)
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

def via_ok(x, y, in_pad=False):
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
            if d < VIA_R+CLR+0.08: return False      # copper + mask margin
        elif d < VIA_R+0.10 and not in_pad: return False            # keep out of GND pads too (no via-in-pad)
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


# ---------------- islands ----------------
V = lambda x, y: pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))
added, padlist, report = 0, [], []
for z in board.Zones():
    if z.GetIsRuleArea() or z.GetNetCode() != GNDC: continue
    for layer in z.GetLayerSet().Seq():
        polys = z.GetFilledPolysList(layer)
        for i in range(polys.OutlineCount()):
            anchored = False
            for (vx, vy, vr, net) in vias:
                if net == GNDC and polys.Contains(V(vx, vy), i): anchored = True; break
            if not anchored:
                for (r, net, onF, onB, ref, num) in pads:
                    if net == GNDC and onF and onB and polys.Contains(V((r[0]+r[2])/2, (r[1]+r[3])/2), i):
                        anchored = True; break
            if anchored: continue
            bb = polys.Outline(i).BBox()
            x1, y1, x2, y2 = mm(bb.GetLeft()), mm(bb.GetTop()), mm(bb.GetRight()), mm(bb.GetBottom())
            spot = None
            for (r, net, onF, onB, ref, num) in pads:   # thermal via in the centre of a big GND pad (EP)
                cx, cy = (r[0]+r[2])/2, (r[1]+r[3])/2
                if net == GNDC and min(r[2]-r[0], r[3]-r[1]) >= 1.3 and polys.Contains(V(cx, cy), i) and via_ok(cx, cy, True):
                    spot = (round(cx, 3), round(cy, 3)); break
            y = y1 + 0.3
            while y < y2 and not spot:
                x = x1 + 0.3
                while x < x2:
                    if polys.Contains(V(x, y), i) and all(polys.Contains(V(x+0.42*math.cos(a), y+0.42*math.sin(a)), i)
                           for a in [k*math.pi/4 for k in range(8)]) and via_ok(x, y):
                        spot = (round(x, 3), round(y, 3)); break
                    x += 0.2
                y += 0.2
            inside = [(ref, num) for (r, net, onF, onB, ref, num) in pads if net == GNDC and
                      ((layer == F_CU and onF) or (layer == B_CU and onB)) and polys.Contains(V((r[0]+r[2])/2, (r[1]+r[3])/2), i)]
            name = board.GetLayerName(layer)
            if spot:
                vias.append((spot[0], spot[1], VIA_R, GNDC)); added += 1
                report.append("%s island %.1fx%.1f @%.1f,%.1f -> via %.2f,%.2f pads=%s" % (name, x2-x1, y2-y1, x1, y1, spot[0], spot[1], inside))
                if not DRY:
                    v = pcbnew.PCB_VIA(board); v.SetPosition(V(*spot))
                    v.SetWidth(F_CU, pcbnew.FromMM(2*VIA_R)); v.SetDrill(pcbnew.FromMM(VIA_DRILL))
                    v.SetLayerPair(F_CU, B_CU); v.SetNetCode(GNDC); board.Add(v)
            else:
                report.append("%s island %.1fx%.1f @%.1f,%.1f -> NO via spot, pads=%s" % (name, x2-x1, y2-y1, x1, y1, inside))
                padlist += inside
for s_ in report: print(s_)
io.open("island_pads.txt", "w", encoding="utf-8").write("\n".join("%s %s" % p for p in padlist))
print("vias added:", added, " pads needing stubs:", len(padlist))
if not DRY:
    pcbnew.ZONE_FILLER(board).Fill(board.Zones()); pcbnew.SaveBoard(BOARD, board); print("saved")
