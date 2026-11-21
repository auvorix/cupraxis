# Evaluation: `cupraxis` with the skill vs without it

Method: Anthropic's skill-creator loop.

- Each test prompt ran in two isolated sub-agents.
  - **with_skill** read `SKILL.md` and its references.
  - **without_skill** used general knowledge and web search, and was forbidden to read the skill or the research folder.
- An independent grader then checked each assertion against the written answer and quoted the evidence.
- Assertions about `.kicad_dru` files were also checked programmatically. The generated rules were run with `kicad-cli pcb drc` on a scratch copy of a KiCad demo board.
- Test cases live in [`skill/cupraxis/evals/`](../skill/cupraxis/evals/), in `claude plugin eval` format.

Model used for all runs: Claude Opus 5.5 (2026-11-21).

## Test cases

| Case | What it asks | What it tests |
|---|---|---|
| `iot-sensor-floorplan` | ESP32-C3 chip-down + chip antenna + LiPo/USB-C + BME280 in 40×30 mm, assembled at JLC | zoning, antenna keepout, stackup and 50 Ω, LiPo→3.3 V, sensor self-heating, assembly constraints, battery vs antenna |
| `layout-review-seeded-errors` | review of a described layout with 8 planted errors | buck hot loop, FB under the inductor, USB over a plane split, crystal, TVS placement, MLCC on VBUS near the V-cut, GND under the antenna, silk minimums |
| `kicad-cli-fab-automation` | PowerShell fab script + JLC `.kicad_dru` + 90 Ω USB rule | real `kicad-cli` 10 syntax, gates, BOM/CPL formats, known `kicad-cli` traps, DRU that actually loads |
| `rpi-hat-analog-adc` | Raspberry Pi 5 HAT with ADS1115, 0–10 V inputs | official HAT outline and holes, HAT+ ID EEPROM, STANDBY state, input conditioning, analog grounding |
| `multi-vendor-eu-order` | compare JLCPCB, PCBWay, Aisler and Eurocircuits for a 4-layer, double-sided board shipped to Ireland | vendor-agnostic design, BOM/CPL per vendor, EU import, impedance per stackup |
| `motor-driver-power-board` (unseen, iteration 3) | 2× DRV8871, 3S LiPo, ESP32-S3 module, INA226 | current-based widths, thermal, bulk/hot loop, power vs logic return paths, Kelvin shunt, input protection |

## Results

| Iteration | Change | Assertions | With skill | Without skill | Delta |
|---|---|---|---|---|---|
| 1 | first draft | 47 | **100 %** | 96 % | +4 pp |
| 2 | harder, accuracy-focused assertions; HAT host template; reading map; tested `kicad-cli` traps | 64 | **98 %** | 81 % | +17 pp |
| 3 | unseen motor case; rule to label unsourced numbers | 25 | **96 %** | 84–87 % | +10 pp |
| 4 (regression, v1.1.0) | review checklists (`13`), return-via/GND-pin research (`12`), λ/20 in FR-4 | 25 (with skill only) | **100 %** | — | no regressions vs iteration 3 |

Cost: the skill roughly doubles tokens and time, because it reads references and often checks datasheets. In iteration 1 it used about 172k tokens against 82k, and 562 s against 240 s. A selective-reading map added in iteration 2 cut the layout review from 134k to 106k tokens and from 213 s to 119 s.

## What the skill fixes (examples from the graded runs)

The baseline was a competent engineer. These are the things it got wrong or missed that the skill got right:

- **Fabrication numbers.** The baseline labeled 0.127 mm trace, 0.3 mm drill, 0.25 mm PTH ring and 0.3 mm copper-to-edge as "JLC minimums". The actual 2-layer values are 0.10 / 0.15 / 0.18 / 0.2 mm. It also gave Eurocircuits class 6 as 0.125 mm instead of 0.150 mm.
- **Assembly constraints.** Body ≥ 2.5 mm from the board edge, PCBA Standard needing ≥ 70×70 mm or rails, and Economic being single-sided were missing from the baseline answers.
- **Raspberry Pi HAT.** The baseline paired 65×56.5 mm with a through-hole header; the official drawing gives 56.0 mm for through-hole and 56.5 mm for SMD. It also missed the HAT+ STANDBY state, which leads to a back-feed bug.
- **USB.** The baseline said a 4 mm intra-pair mismatch "still fits the spec" for High-Speed. The guideline is about 1.27 mm.
- **KiCad 10 toolchain.** The skill knows these from tests on 10.0.8:
  - parity problems come out as *warnings*;
  - `pos` defaults to ASCII and inches;
  - the BOM collapses references into ranges unless `--ref-range-delimiter` is empty;
  - PowerShell 5.1 drops empty arguments;
  - a malformed `.kicad_dru` is ignored silently;
  - an unconditional `clearance` rule overrides netclasses.
- **Vendor files.** Fabs that accept native `.kicad_pcb` files may process them with KiCad 8/9.
- **Part ratings.** The skill flagged that a DRV8871's start-up peak trips its minimum 3.7 A over-current protection, and sized R_ILIM for the worst case. The baseline's R_ILIM could exceed it.

## Known limits

- One run per configuration per iteration, so the numbers carry run-to-run variance.
- The baseline is a strong general model. Many generic best-practice assertions do not discriminate; the gains concentrate on non-obvious facts and numeric accuracy.
- Vendor capabilities, prices and tax rules were consulted in November 2026 and will drift. The skill tells the model to confirm on the vendor's page.
