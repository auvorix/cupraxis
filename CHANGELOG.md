# Changelog

## 1.2.1 — 2026-11-21
- **Real JLCPCB quote** (5 pcs, 100×100 mm, shipped to Ireland) in `references/10`:
  - 2 layers €3.64 and 4 layers €7.29;
  - ENIG +€16.12; 2 oz copper +€33.15; black mask at no extra cost;
  - specifying a stackup costs nothing extra;
  - DDP shipping €23.67.
- **New finding:** the JLC04161H-3313 stackup is "special" and does not support Economic PCBA, only Standard. This is recorded in the skill and in the house rules.


## 1.2.0 — 2026-11-21
- **Official JLCPCB impedance values** from the vendor calculator replace the estimates. Setup: 4 layers, 1.6 mm, 1 oz outer / 0.5 oz inner, signal on L1 over L2.
  - JLC04161H-7628: CPWG 50 Ω W 0.306 mm with a 0.20 mm gap; microstrip 50 Ω 0.359 mm; 90 Ω differential pair W 0.291 / S 0.203 mm.
  - JLC04161H-3313: CPWG 0.142 mm; microstrip 0.151 mm; 90 Ω pair W 0.154 / S 0.203 mm.
- **House-rule conflicts A1–A16 resolved** (`references/regras-da-casa.md` §17):
  - stackup default 7628 SIG/GND/GND/SIG; CPWG for RF;
  - rails/panel for edge connectors;
  - minimum test pads;
  - hand-route critical nets before the autorouter;
  - multiple vias per GND island;
  - assembly spacing table in the placement gate.
- **Skill description:** narrower scope, so it no longer fires on firmware-only, basic-electronics, SPICE-only or enclosure-only tasks; quoted YAML, 936 characters.
- **`spread.py`:** default gap 1.0 mm, matching the assembler spacing table.
- **References:** Ignion 2.4 GHz antenna manual and app note added to the PDF catalog.
- **Known issue:** the skill-creator trigger-optimization loop (`claude -p`) recorded 0 triggers for every query on this Windows setup, positives included. The run was discarded as a harness problem and the description was tuned by hand.


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
