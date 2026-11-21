<div align="center">

# PCB Expert

**A Claude Code skill and an open, source-tagged knowledge base for designing printed circuit boards, from requirements to the factory.**

KiCad 10 · kicad-cli · Freerouting · KiCad-MCP · JLCPCB · PCBWay · Aisler · Eurocircuits · OSH Park

[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-lightgrey.svg)](LICENSE-docs)
[![KiCad 10](https://img.shields.io/badge/KiCad-10.0-314cb0.svg)](https://www.kicad.org/)
[![Claude Code skill](https://img.shields.io/badge/Claude%20Code-skill-d97757.svg)](https://docs.claude.com/en/docs/claude-code/skills)

[Português](#português) · [What it does](#what-it-does) · [Install](#install) · [Repository layout](#repository-layout) · [Evaluation](#evaluation) · [Sources and licensing](#sources-and-licensing)

</div>

---

## What it does

`pcb-expert` turns Claude into a hardware design reviewer and planner that thinks about what actually breaks boards in production: edge mechanics, assembly rules, RF, power integrity, EMC and sourcing. A DRC catches only part of that.

- **Floorplan by zones:** power, digital, analog, RF/antenna, connectors and human interface, with a placement order and proximity rules for every component type.
- **Power:** buck, boost and buck-boost hot loops, LDO vs LC filtering, ferrite resonance, LiPo/USB-C power paths, current-based trace and via sizing.
- **RF:** antenna keepouts, CPWG vs microstrip, matching networks, via fences at ≤ λ/20, coexistence, SMA/u.FL.
- **Grounding, SI and EMC:** return paths, stackups, USB 90 Ω pairs, crystals, ESD/TVS placement, and why the 20H and 3W rules are contested.
- **Component selection:** MLCC DC-bias derating, inductors (Isat vs Irms), crystals, connectors, lifecycle and MSL.
- **Board shape and DFM:** outlines from official DXF/STEP, mounting holes, panelization, silkscreen minimums, enclosure co-design.
- **Vendor-agnostic manufacturing:** a common-minimum rule set, per-vendor BOM/CPL formats, DRU files, and EU import rules (VAT, IOSS, the 2026 per-line duty).
- **Toolchain know-how, tested on KiCad 10.0.8:** `kicad-cli` recipes and their traps, `.kicad_dru` rules, the `pcbnew` API, Freerouting, and the KiCad-MCP limitations.
- **Scripts:** a read-only board audit for edge connectors, the 2.5 mm assembly rule, MLCC flex risk, silk minimums and thin power traces. Also included: rip-up, spread, GND stitching fixes, a JLC/LCSC parts query, and a BOM/CPL converter.

Every technical claim in the knowledge base carries a source URL and a **FATO** (verified in the source) or **INFERÊNCIA** (inference / common practice) tag.

## Install

**Claude Code (recommended)**

```bash
git clone https://github.com/auvorix/pcb-expert.git
# user-wide
cp -r pcb-expert/skill/pcb-expert ~/.claude/skills/
# or project-only
cp -r pcb-expert/skill/pcb-expert <your-project>/.claude/skills/
```

The skill triggers on PCB tasks such as "plan the floorplan of my board", "review this layout", "generate JLC fab files" or "which fab should I use?". You can also call it explicitly with `/pcb-expert`.

**Requirements for the scripts (optional):**
- KiCad 10. Run the `pcbnew` scripts with KiCad's own `python.exe` (`%LOCALAPPDATA%\Programs\KiCad\10.0\bin\python.exe` on Windows).
- Python 3.10+.
- For `jlc_query.py`: the JLCPCB parts database downloaded by [KiCAD-MCP-Server](https://github.com/mixelpixx/KiCAD-MCP-Server), or set `JLC_DB`.

```bash
python pcb_audit.py board.kicad_pcb --json audit.json        # read-only gate
python jlc_query.py "mfr_part like 'TPS63020%'"               # parts lookup
```

## Repository layout

```
skill/pcb-expert/           ← the installable skill
  SKILL.md                  workflow with gates, zoning map, proximity table, key numbers
  references/               00–10 topic files + house rules + host templates (RPi HAT, Flipper)
  scripts/                  pcb_audit, ripup, spread, gnd_fix, island_fix, jlc_query, kicad_to_jlc
  evals/                    test cases (claude plugin eval format)
research/                   the full research corpus in Markdown (source of the references)
  boas-praticas/            01 floorplan · 02 power · 03 RF · 04 GND/SI/EMC · 05 components
                            06 shape/DFM · 07 bibliography · 08 KiCad · 09 fab/MCP/CAD · 10 vendors
  hosts/                    host templates (tagged [FLIPPER] where Flipper-specific)
docs/
  pdf-catalog.md            every vendor PDF used, with its official download link
  evaluation.md             benchmark of the skill vs no skill
```

Placeholders used in the files: `<REFERENCIAS>` is this repo's `research/` folder. `%USERPROFILE%` is your home folder. `<BRANDING>` and `<DEVSHARED>` are the author's local folders and are not needed to use the skill.

## Evaluation

The skill was built with Anthropic's skill-creator loop. Each test prompt ran **with** and **without** the skill, and an independent grader checked every assertion against the outputs. See [docs/evaluation.md](docs/evaluation.md).

| Iteration | Assertions | With skill | Without skill |
|---|---|---|---|
| 1 | 47 | 100 % | 96 % |
| 2 (harder, accuracy-focused) | 64 | 98 % | 81 % |
| 3 (unseen motor-driver case + fixes) | 25 | 96 % | 84–87 % |

The baseline was competent but made factual errors that the skill avoided. Examples: wrong JLC minimums, the wrong Raspberry Pi HAT outline for the header type, a wrong Eurocircuits class, and missing assembly constraints (2.5 mm edge, 70×70 mm double-sided minimum, the HAT+ STANDBY state).

## Sources and licensing

- **Code** (`skill/pcb-expert/scripts`, etc.): [MIT](LICENSE).
- **Documentation and research text**: [CC BY 4.0](LICENSE-docs).
- **Third-party PDFs** (TI, ADI, ST, NXP, Espressif, u-blox, Murata, Würth, Vishay, JST, Raspberry Pi…) are **not redistributed**. [docs/pdf-catalog.md](docs/pdf-catalog.md) lists each one with its official link.
- Flipper Zero mechanical files are GPL-3.0 at [flipperdevices/flipperzero-3d-models](https://github.com/flipperdevices/flipperzero-3d-models). Flipper One docs have no declared license, so they are linked only.
- Vendor capabilities, prices and tax rules change. Every number carries its consultation date; check the vendor page before ordering.

---

## Português

**PCB Expert** é uma skill do Claude Code e uma base de conhecimento aberta, com fontes etiquetadas (FATO / INFERÊNCIA), para projetar placas do requisito à fábrica.

O que cobre:
- floorplan por zonas;
- energia e fontes chaveadas;
- RF e antenas;
- aterramento, integridade de sinal e EMC;
- escolha de componentes;
- formato, fabricabilidade e estética;
- fabricação com qualquer fornecedor (JLCPCB, PCBWay, Aisler, Eurocircuits…);
- a cadeia de ferramentas do KiCad 10, testada na prática.

Toda a pesquisa está em português em [`research/boas-praticas/`](research/boas-praticas/). Para instalar, copie `skill/pcb-expert` para `~/.claude/skills/`.

Maintained by [AUVORIX](https://github.com/auvorix).
