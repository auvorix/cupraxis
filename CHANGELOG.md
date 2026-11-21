# Changelog

## 1.0.0 — 2026-11-21
- First public release of the `cupraxis` skill (KiCad 10, vendor-agnostic).
- Research corpus 00–10: floorplan, power, RF, GND/SI/EMC/stackup, components and connectors, shape/DFM/aesthetics, bibliography, KiCad 10 toolchain, fab/MCP/CAD, PCB/PCBA vendors.
- Host templates: Raspberry Pi HAT/HAT+, Flipper Zero/One (`[FLIPPER]`).
- Scripts: `pcb_audit.py` (new, read-only gate), `ripup.py`, `spread.py` (parameterized), `gnd_fix.py`, `island_fix.py`, `jlc_query.py`, `kicad_to_jlc.py`, `sync_references.py`.
- Evaluation: 3 iterations, 6 test cases; see `docs/evaluation.md`.
