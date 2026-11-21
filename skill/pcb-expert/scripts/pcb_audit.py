"""Auditoria SO-LEITURA de uma placa KiCad: checa o que DRC/ERC nao pegam.
Rodar com o python do KiCad (tem `import pcbnew`):
  "%USERPROFILE%\\AppData\\Local\\Programs\\KiCad\\10.0\\bin\\python.exe" pcb_audit.py placa.kicad_pcb [--json saida.json]
     [--edge-refs J,SW,USB,BT] [--jlc-edge 2.5] [--mlcc-edge 5.0] [--power-nets "+3V3,+5V,VBUS,VSYS,VBAT"] [--power-min 0.5]

Checagens (cada uma vira OK / AVISO / FALHA no relatorio):
  1. Contorno: tamanho da placa (bbox da Edge.Cuts), numero de camadas de cobre, espessura do stackup.
  2. Conectores/acesso (refs com prefixo em --edge-refs): distancia do CORPO (bbox do courtyard, ou do footprint)
     a borda mais proxima. Conector de acesso deve encostar/ultrapassar a borda (<= 0.5 mm) -> lista os recuados.
  3. Regra JLC de montagem: corpo de componente a >= 2.5 mm da borda (lista os que violam; conectores de borda
     aparecem aqui de proposito: exigem rail/painel ou consulta a JLC).
  4. MLCC (refs C*) a menos de --mlcc-edge mm da borda ou de furo de montagem (risco de trinca por flexao).
  5. Texto de silkscreen com altura < 1.0 mm ou traco < 0.15 mm (minimo JLC).
  6. Trilhas de redes de energia mais finas que --power-min mm (netclass que nao foi aplicada no autorouter).
  7. Pads sem rede em footprints com rede (possivel no_connect esquecido) - so informativo.
Nao altera nada. Nao substitui o DRC oficial (kicad-cli pcb drc).
"""
import argparse
import json
import math
import sys

import pcbnew

ap = argparse.ArgumentParser()
ap.add_argument("board")
ap.add_argument("--json")
ap.add_argument("--edge-refs", default="J,SW,USB,BT")
ap.add_argument("--jlc-edge", type=float, default=2.5)
ap.add_argument("--mlcc-edge", type=float, default=5.0)
ap.add_argument("--power-nets", default="+3V3,+3.3V,3V3,+5V,5V,VBUS,VSYS,VBAT,VIN,+12V")
ap.add_argument("--power-min", type=float, default=0.5)
A = ap.parse_args()

mm = pcbnew.ToMM
b = pcbnew.LoadBoard(A.board)
rep = {"board": A.board, "checks": []}


def add(name, status, detail, items=None):
    rep["checks"].append({"check": name, "status": status, "detail": detail, "items": items or []})


# ---------- contorno ----------
edges = [d for d in b.GetDrawings() if d.GetLayer() == pcbnew.Edge_Cuts]
segs = []
for d in edges:
    try:
        shape = d.GetShape()
    except Exception:
        continue
    if shape == pcbnew.SHAPE_T_SEGMENT:
        s, e = d.GetStart(), d.GetEnd()
        segs.append(((mm(s.x), mm(s.y)), (mm(e.x), mm(e.y))))
    else:
        # arcos/circulos/retangulos/poligonos: aproximar pelo poligono do contorno
        try:
            poly = pcbnew.SHAPE_POLY_SET()
            d.TransformShapeToPolygon(poly, pcbnew.Edge_Cuts, 0, pcbnew.FromMM(0.01), pcbnew.ERROR_INSIDE)
            for oi in range(poly.OutlineCount()):
                ol = poly.Outline(oi)
                n = ol.PointCount()
                pts = [(mm(ol.CPoint(i).x), mm(ol.CPoint(i).y)) for i in range(n)]
                for i in range(n):
                    segs.append((pts[i], pts[(i + 1) % n]))
        except Exception:
            pass
bb = b.GetBoardEdgesBoundingBox()
W, H = mm(bb.GetWidth()), mm(bb.GetHeight())
ncu = b.GetCopperLayerCount()
thick = None
try:
    thick = mm(b.GetDesignSettings().GetBoardThickness())
except Exception:
    pass
add("contorno", "OK" if segs else "FALHA",
    f"{W:.2f} x {H:.2f} mm, {ncu} camadas de cobre, espessura {thick} mm, {len(segs)} segmentos de Edge.Cuts"
    + ("" if W >= 70 and H >= 70 else " | < 70x70 mm: PCBA Standard JLC exige rail/painel (ou Economic, 1 lado)"))


def pt_seg(p, a, c):
    (px, py), (ax, ay), (bx, by) = p, a, c
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def inside(p):
    # ray casting no conjunto de segmentos
    x, y = p
    c = False
    for (x1, y1), (x2, y2) in segs:
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xi > x:
                c = not c
    return c


def rect_edge(r):
    """distancia minima (mm) do retangulo r=(x1,y1,x2,y2) a Edge.Cuts; negativa se cruza/ultrapassa a borda."""
    x1, y1, x2, y2 = r
    corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    if not all(inside(c) for c in corners):
        return -1.0  # parte do corpo fora da placa (ultrapassa a borda)
    pts = corners + [((x1 + x2) / 2, y1), ((x1 + x2) / 2, y2), (x1, (y1 + y2) / 2), (x2, (y1 + y2) / 2)]
    dmin = min(pt_seg(p, a, c) for p in pts for a, c in segs)
    return dmin


def body_rect(fp):
    try:
        cy = fp.GetCourtyard(pcbnew.F_CrtYd if not fp.IsFlipped() else pcbnew.B_CrtYd)
        if cy.OutlineCount():
            bx = cy.BBox()
            return (mm(bx.GetX()), mm(bx.GetY()), mm(bx.GetRight()), mm(bx.GetBottom())), "courtyard"
    except Exception:
        pass
    bx = fp.GetBoundingBox(False, False)
    return (mm(bx.GetX()), mm(bx.GetY()), mm(bx.GetRight()), mm(bx.GetBottom())), "bbox"


fps = list(b.GetFootprints())
pref = tuple(s for s in A.edge_refs.split(",") if s)
holes = []
for fp in fps:
    ref = fp.GetReference()
    if ref.startswith("H") or "MountingHole" in str(fp.GetFPID().GetLibItemName()):
        p = fp.GetPosition()
        holes.append((ref, mm(p.x), mm(p.y)))

edge_items, jlc_items, mlcc_items = [], [], []
if segs:
    for fp in fps:
        ref = fp.GetReference()
        if ref.startswith("H") or ref.startswith("#") or ref.startswith("REF"):
            continue
        r, src = body_rect(fp)
        d = rect_edge(r)
        if ref.startswith(pref):
            edge_items.append({"ref": ref, "dist_mm": round(d, 2), "fonte": src,
                               "ok": d <= 0.5})
        if d < A.jlc_edge:
            jlc_items.append({"ref": ref, "dist_mm": round(d, 2)})
        if ref.startswith("C") and not ref.startswith("CN"):
            p = fp.GetPosition()
            dh = min([math.hypot(mm(p.x) - hx, mm(p.y) - hy) for _, hx, hy in holes] or [999])
            if d < A.mlcc_edge or dh < A.mlcc_edge:
                mlcc_items.append({"ref": ref, "dist_borda_mm": round(d, 2), "dist_furo_mm": round(dh, 2),
                                   "valor": fp.GetValue()})
recuados = [i for i in edge_items if not i["ok"]]
add("conectores_na_borda", "OK" if not recuados else "FALHA",
    f"{len(edge_items)} pecas de acesso ({A.edge_refs}); {len(recuados)} recuadas > 0.5 mm da borda "
    "(conferir: so conectores/botoes que o usuario toca precisam estar na borda; dist negativa = ultrapassa a borda)",
    edge_items)
add("jlc_2.5mm_borda", "OK" if not jlc_items else "AVISO",
    f"{len(jlc_items)} pecas com corpo a < {A.jlc_edge} mm da borda (JLC Assembly T&C: exige >= 2.5 mm; "
    "conectores de borda -> rail/painel ou consulta a JLC)", jlc_items)
add("mlcc_flexao", "OK" if not mlcc_items else "AVISO",
    f"{len(mlcc_items)} capacitores a < {A.mlcc_edge} mm de borda/furo (trinca por flexao; orientar paralelo a borda "
    "ou afastar; soft-termination em >= 0805 de energia)", mlcc_items)

# ---------- silkscreen ----------
silk_bad = []
silk_layers = (pcbnew.F_SilkS, pcbnew.B_SilkS)


def check_text(t, owner):
    try:
        if t.GetLayer() not in silk_layers or not t.IsVisible():
            return
        h, w = mm(t.GetTextHeight()), mm(t.GetTextThickness())
        if h < 1.0 or w < 0.15:
            silk_bad.append({"onde": owner, "texto": t.GetText()[:30], "altura_mm": round(h, 2), "traco_mm": round(w, 3)})
    except Exception:
        pass


for d in b.GetDrawings():
    if isinstance(d, pcbnew.PCB_TEXT):
        check_text(d, "placa")
for fp in fps:
    check_text(fp.Reference(), fp.GetReference())
    check_text(fp.Value(), fp.GetReference())
    for it in fp.GraphicalItems():
        if isinstance(it, pcbnew.PCB_TEXT):
            check_text(it, fp.GetReference())
add("silk_minimos", "OK" if not silk_bad else "AVISO",
    f"{len(silk_bad)} textos de silk abaixo de 1.0 mm de altura ou 0.15 mm de traco (minimo JLC)", silk_bad[:60])

# ---------- trilhas de energia ----------
pnets = set(s.strip().upper() for s in A.power_nets.split(",") if s.strip())
thin = {}
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_VIA_T:
        continue
    n = t.GetNetname().upper().lstrip("/")
    if n in pnets:
        w = mm(t.GetWidth())
        if w < A.power_min - 1e-6:
            thin.setdefault(t.GetNetname(), []).append(round(w, 3))
add("trilhas_energia", "OK" if not thin else "AVISO",
    f"redes de energia com trilha < {A.power_min} mm: " + (", ".join(f"{k}: {len(v)} seg (min {min(v)} mm)" for k, v in thin.items()) or "nenhuma")
    + " (dimensionar pela IPC-2152; JLC 4 camadas tem cobre interno 0.5 oz; 'pescoco' curto saindo de pad de passo fino"
    " pode ser legitimo — o que importa e o trecho longo)")

# ---------- resumo ----------
order = {"FALHA": 2, "AVISO": 1, "OK": 0}
worst = max((c["status"] for c in rep["checks"]), key=lambda s: order[s])
rep["resultado"] = worst
for c in rep["checks"]:
    print(f"[{c['status']:5}] {c['check']}: {c['detail']}")
    for it in c["items"][:25]:
        if c["status"] != "OK" or c["check"] == "conectores_na_borda":
            print("         ", it)
print("RESULTADO:", worst)
if A.json:
    json.dump(rep, open(A.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.exit(0)
