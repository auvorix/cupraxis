"""KiCad BOM/POS CSV -> JLCPCB BOM (one line per LCSC code) + CPL.
Usage: python -I kicad_to_jlc.py bom_raw.csv pos_raw.csv out_bom.csv out_cpl.csv
bom_raw from: kicad-cli sch export bom --fields "Value,Reference,Footprint,LCSC" --labels "Comment,Designator,Footprint,LCSC Part #" --group-by "Value,Footprint,LCSC" --exclude-dnp --ref-range-delimiter ""
pos_raw from: kicad-cli pcb export pos --format csv --units mm --side both --exclude-dnp
JLC zeroes the qty of repeated LCSC codes on separate lines, so lines are merged by LCSC."""
import csv, collections, re, sys
bom_in, pos_in, bom_out, cpl_out = sys.argv[1:5]
rows = list(csv.reader(open(bom_in, encoding="utf-8")))
g = collections.OrderedDict()
for c, d, f, l in rows[1:]:
    f = f.split(":", 1)[-1]
    k = (l or c, f)
    if k not in g:
        g[k] = [c.split(" (")[0], [], f, l]
    g[k][1] += d.split(",")
nat = lambda r: (re.sub(r"\d+", "", r), int(re.sub(r"\D", "", r) or 0))
w = csv.writer(open(bom_out, "w", newline="", encoding="utf-8"))
w.writerow(rows[0])
for c, ds, f, l in g.values():
    w.writerow([c, ",".join(sorted(ds, key=nat)), f, l])
p = list(csv.DictReader(open(pos_in, encoding="utf-8")))
w = csv.writer(open(cpl_out, "w", newline="", encoding="utf-8"))
w.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
for r in p:
    w.writerow([r["Ref"], f'{float(r["PosX"]):.6f}mm', f'{float(r["PosY"]):.6f}mm', "Top" if r["Side"] == "top" else "Bottom", f'{float(r["Rot"]):.6f}'])
print("bom lines", len(g), "missing lcsc", sum(1 for v in g.values() if not v[3]), "cpl", len(p))
