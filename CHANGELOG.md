# Changelog

## 1.1.0 — 2026-11-21
- **Review checklists (`references/13`)**, adapted with attribution from kicad-happy (MIT) and KiCAD-MCP-Server (MIT):
  - schematic review by part class, stacked tolerances, standard connector pinouts and GPIO mux audit;
  - measurable EMC/PDN layout thresholds: SW-node copper, hot-loop area, unshielded inductor distance, decoupling distance, TVS ground vias;
  - target impedance, battery sleep budget, EN 55032 pre-compliance, and golden-netlist diff for scripted schematic edits.
- **Return vias and connector ground pins (`references/12`)**, from new primary-source research:
  - return via ≤ 1 mm (fast signals) with a 5 mm hard limit;
  - ground pins: error below 1:9, warning below max(2, ⌈S/4⌉), G-S-G for clocks;
  - fixes a misreading of TI SZZA009, where 1:9 is a floor and not the rule.
- **λ/20 via fences** now computed in FR-4 (εr ≈ 4.4): 2.9 mm at 2.45 GHz, 1.2 mm at 5.8 GHz.
- **Scripts:**
  - `gnd_fix.py` and `island_fix.py` guard `.kicad_pro` against `pcbnew.SaveBoard` overwriting it (verified on KiCad 10.0.8);
  - `kicad_to_jlc.py` cross-checks BOM and CPL designators.
- `references/11`: analysis of related skills and tools (kicad-happy, KiCAD-MCP-Server, ESP32-AI-Agent-Skill).


## 1.0.0 — 2026-11-21
- First public release of the `cupraxis` skill (KiCad 10, vendor-agnostic).
- Research corpus 00–10: floorplan, power, RF, GND/SI/EMC/stackup, components and connectors, shape/DFM/aesthetics, bibliography, KiCad 10 toolchain, fab/MCP/CAD, PCB/PCBA vendors.
- Host templates: Raspberry Pi HAT/HAT+, Flipper Zero/One (`[FLIPPER]`).
- Scripts: `pcb_audit.py` (new, read-only gate), `ripup.py`, `spread.py` (parameterized), `gnd_fix.py`, `island_fix.py`, `jlc_query.py`, `kicad_to_jlc.py`, `sync_references.py`.
- Evaluation: 3 iterations, 6 test cases; see `docs/evaluation.md`.
