# 13 — Checklists de revisão: esquemático, layout (EMC/PDN) e edição por MCP

> Consolidado em 2026-11-21 a partir de `11-analise-skills-relacionadas.md`.
> As heurísticas foram parafraseadas de:
> - **kicad-happy** (Andrew Klofas, MIT, commit `6b9767e1`, https://github.com/aklofas/kicad-happy);
> - **KiCAD-MCP-Server** (mixelpixx, MIT, v2.9.0).
>
> Cada número vem rotulado com a origem. "Heurística kicad-happy" é um limiar de revisão, não uma norma; quando a heurística cita uma fonte primária (TI, IEC), ela aparece entre parênteses.
>
> Os limiares servem para **triagem numa revisão**: o que passa do limite merece atenção e justificativa. Não substituem o datasheet do chip.

## Resumo
- **Esquemático:** o gate da etapa 3 não é só "ERC 0". Revise o circuito por classe de peça (§A), empilhe as tolerâncias (§B), confira pinagens padrão (§C) e audite o mux de GPIO (§D).
- **Layout:** os limiares numéricos de EMC (§E) e de rede de energia/PDN (§F) transformam "laço mínimo" e "perto do pino" em itens que dá para medir.
- **Bateria:** faça o orçamento de corrente em sono e calcule a tensão mínima sob pico (§G).
- **UE:** limites de emissão irradiada da EN 55032 e margem de projeto (§H).
- **Edição por script/MCP:** compare a netlist antes e depois, conheça as pegadinhas de símbolo e use as ferramentas de lint (§I).

---

## A. Revisão de esquemático por classe de peça
Fonte: heurística kicad-happy, `deep-review.md` e `schematic-analysis.md`.

| Classe | Conferir |
|---|---|
| Regulador | Vin de pior caso, com tolerância e transiente. Recalcule Vout pelo divisor de FB e confira contra o nome da rail. EN nunca flutuando: compare o limiar com a tensão que o aciona. Pull-up do PG no domínio certo. Capacitores de entrada e saída pelo valor **efetivo após DC bias**. Dissipação P = (Vin − Vout)·I e Tj = Ta + P·θJA |
| MCU | Cada par VDD/VSS com seu capacitor. VDDA com filtro próprio. Strapping no sentido do boot desejado. Nenhum pino alimentado por domínio mais alto que o seu, salvo se for 5 V tolerant |
| MOSFET | Rds(on) **na Vgs real** do circuito, não na condição de teste mínima do datasheet. Pull-down de gate |
| TVS | Tensão de trabalho ≥ nível alto normal da rail. Tensão de grampeamento ≤ máximo absoluto do pino protegido |
| Indutor | Isat ≥ 1,3 × corrente de pico (heurística kicad-happy). Irms pelo aquecimento (ver `05`) |
| Capacitor | Tensão nominal ≥ 1,5 × tensão aplicada (heurística kicad-happy). C0G em RF e cristal. DC bias em X5R/X7R (`05`) |
| Interface | VIH do receptor contra VOH do driver. Quem é dono do pull-up. Pull-ups em paralelo no mesmo barramento somam (ex.: I²C com dois módulos que trazem os seus) |

**Severidade sugerida para esquemático** (heurística kicad-happy):
- **Crítico:** máximo absoluto excedido, falta capacitor de saída do regulador, pino de alimentação flutuando, divisor de FB que gera sobretensão.
- **Aviso:** margem < 20 %, DC bias não considerado, falta ESD externo.
- **Sugestão / Info:** o resto.

## B. Tolerância empilhada (divisores, filtros, cristal)
Fonte: heurística kicad-happy, `schematic-analysis.md`.

- **Divisor de FB:**
  - Vout_max = VREF_max · (1 + Rt·(1+tol) / (Rb·(1−tol)))
  - Vout_min = VREF_min · (1 + Rt·(1−tol) / (Rb·(1+tol)))
  - Compare Vout_max com o máximo absoluto de quem está a jusante e Vout_min com o headroom do LDO seguinte.
  - Exemplo (deles): VREF 0,595 V ± 2,5 %, 820 k / 110 k a 1 % → 4,82–5,25 V.
- **Outros casos:** a mesma conta vale para divisor de ADC, filtro RC e capacitores de carga de cristal. Exemplo de RC: 10 k 5 % + 100 nF 10 % → f_c de 138 a 186 Hz.

## C. Pinagens padrão que mais causam erro
Fonte: heurística kicad-happy. **Confira no documento oficial do padrão antes de fechar.**

| Conector | Pinagem / cuidado |
|---|---|
| FTDI 6 pinos | O TX da placa vai ao RXD do cabo (pino 5) |
| SWD 10 pinos (1,27 mm) | 1 = VTref, 2 = SWDIO, 4 = SWCLK, 6 = SWO, 10 = nRST |
| Qwiic / STEMMA QT | 1 GND, 2 3V3, 3 SDA, 4 SCL. Qwiic é 3,3 V; STEMMA QT aceita 3–5 V (`05`) |
| CAN | Terminação de 120 Ω só nas duas pontas do barramento |
| RS-485 | A polaridade A/B varia por fabricante: documente no silk |
| USB Micro-B (device) | Pino ID desconectado |

## D. Auditoria de mux de GPIO
Fonte: procedimento da heurística kicad-happy. Os dados de pino vêm **do datasheet do chip usado**.

Para cada pino do MCU, confira:
1. A função atribuída existe naquele pino.
2. Não há dois periféricos no mesmo pino.
3. Nenhum canal de ADC está sendo usado como digital ao mesmo tempo.
4. Os pinos de JTAG/SWD não foram usados como GPIO sem querer, o que tira o debug.
5. Nenhum pino de strapping vai a um periférico que o puxe no boot. Exemplo: GPIO0 do ESP32 como CS de SPI.
6. Os pinos de flash/PSRAM internos estão livres.

ESP32: use o datasheet da variante exata (C3, C5, S3…). **Não** use tabelas genéricas de "ESP32": a skill ESP32-AI-Agent-Skill erra os pinos de variantes novas.

---

## E. Limiares de EMC para revisão de layout
Fonte: heurística kicad-happy, `pcb-emc-rules.md`, com a fonte primária citada nela.

| ID (deles) | Item | Aviso | Erro | Correção |
|---|---|---|---|---|
| SW-002 | Área total de cobre do nó SW/LX (pads + trilhas + zonas) (TI SLVA477) | ≥ 25 mm² | > 100 mm² | Nó SW mínimo, só o necessário para corrente e térmico |
| SW-003 | Área do hot loop **medida pelos pads**: Cin+ → VIN do CI → SW → indutor; GND do CI → Cin− | 25–100 mm² | > 100 mm² | Cin colado, mesmo lado, sem via |
| ML-001 | Indutor de conversor **não blindado** (ou de blindagem desconhecida) perto de ADC, amplificador operacional, cristal ou RF | < 15 mm | < 8 mm e sabidamente não blindado | Indutor blindado ou eixo perpendicular às trilhas sensíveis |
| DC-001 | Capacitor de desacoplamento até o pino de alimentação do CI | > 5 mm | > 8 mm | Aproximar; o menor valor mais perto |
| DC-003 | Capacitor de desacoplamento até a via de GND/alimentação mais próxima | > 3 mm | — | A indutância da via e da trilha domina (trilha sobre plano ≈ 0,3–0,8 nH/mm) |
| ES-001 | TVS até o conector (centro a centro) | > 15 mm | — | TVS no conector, antes de tudo (`04` D5) |
| ES-002 | Vias de GND a ≤ 3 mm do TVS | — | < 2 vias | 2 vias em paralelo: ~0,5 → ~0,25 nH, ~9 V a menos de clamp em 8 kV |
| TH-002 | Ferrite a ≤ 10 mm de regulador chaveado | info | — | A permeabilidade cai com a temperatura; a impedância pode cair 30–50 % acima de ~85 °C |
| EF-001 | Filtro EMI de entrada do SMPS | f_sw / f_corte < 5 | — | Baixar o corte (−40 dB/década) e amortecer (`02` §E) |
| CK-003 | Trilha de clock perto de conector externo | < 10 mm | — | Afastar; o cabo vira antena |

**Estimativas rápidas** (ordem de grandeza, ±10–20 dB; servem para dizer qual banda corre risco, não para prever aprovação):
- **Modo diferencial com plano:** E_DM ≈ 2,632×10⁻¹⁴ · f² · A · I / r.
- **Modo comum em cabo:** E_CM ≈ 1,257×10⁻⁶ · f · L · I_CM / r.
- **Escala:** dobrar a área do laço dá +6 dB; dobrar a frequência dá +12 dB em modo diferencial.
- **Ressonância da cavidade entre planos:** f_mn = c / (2√εr) · √((m/L)² + (n/W)²). Para 100 × 80 mm em FR-4, f₁₀ ≈ 714 MHz.
- **Fenda no plano:** ressoa em f ≈ c / (2L).
- **Indutância de via:** L ≈ 0,2 · h · [ln(4h/d) + 1] nH (h e d em mm).
- **Frequência de joelho:** f ≈ 0,35 / t_r (ou 0,5 / t_r).
- Referência: 5 µA de corrente de modo comum num cabo de 1 m a 100 MHz já estouram o limite FCC Classe B em ~3 dB. Cabos são o radiador principal.

**Shield can** (fonte: KiCad-MCP, prompt `emc_shield_review`):
- Uma lata com poucos clips ou vias deixa fendas que podem irradiar **mais** que nenhuma lata. Use cerca de vias contínua ≤ λ/20 sob o contorno da moldura (`03`).
- Supressão em dB = 20·log10(E_antes / E_depois), uma razão de campo, não de potência.

## F. Rede de distribuição de energia (PDN)
Fontes: KiCad-MCP (prompt `pdn_dc_review`) e heurística kicad-happy.

- **Impedância-alvo:** Z_target = ΔV_permitido / ΔI_degrau, onde ΔI é o degrau transitório e não a corrente DC.
  - O kicad-happy usa por padrão Z_target = 5 % · V / (0,5 · I_transitório) e confere anti-ressonâncias até ~200 MHz.
  - A capacitância nominal do esquemático não é a efetiva: aplique o DC bias.
- **Impedância no pino do CI:** Z_local ∥ (Z_regulador + R_trilha + jωL_trilha). Trilha longa e estreita até o regulador anula o desacoplamento distante.
- **Acoplamento entre rails:** um conversor a jusante puxa do rail a montante I_in ≈ V_out · I_out / (V_in · η), pulsado em f_sw. O rail de cima precisa de capacitância para esse ripple.
- **Plano contra trilha:**
  - Em plano, use a IPC-2152; a IPC-2221 é para trilha isolada e superestima a elevação de temperatura de um plano.
  - "525 mA/mm" (= 15 A/mm² em cobre de 35 µm) indica aglomeração de corrente num estrangulamento, não um limite térmico.
- **Nó SW:** pequeno e na **camada externa** sobre GND contínuo. Não o leve para camada interna: isso acrescenta vias e acoplamento capacitivo.

## G. Bateria: orçamento de sono e tensão mínima
Fonte: heurística kicad-happy.

- **Corrente de sono:** some o sono do MCU, os divisores sempre ligados (I = Vbat / (Rt + Rb)), o Iq dos reguladores, os pull-ups com caminho para GND, as fugas de TVS/FET/diodo e LEDs. **Sinalize qualquer item acima de 10 % do total.**
- **Tensão mínima da bateria:** V_bat_min = Vin_min do regulador + I_pico · R_interna + margem. Use o pico de TX do rádio (Wi-Fi pode passar de 300–500 mA; ver datasheet).
- **EN dos reguladores** com pull-down, para nascerem desligados no boot quando a sequência importa.

## H. Pré-conformidade de emissão irradiada (UE)
Fontes: heurística kicad-happy (`emc-standards.md`) e KiCad-MCP. **Confirme os limites no texto da norma antes de tratar como FATO.**

- **CISPR 32 / EN 55032, Classe B (residencial):**
  - a 10 m: 30 dBµV/m (30–230 MHz) e 37 dBµV/m (230–1000 MHz);
  - a 3 m: 40 e 47 dBµV/m;
  - conversão de 3 m para 10 m: −10,5 dB.
- **Margem de projeto ≥ 6 dB.** A incerteza de câmara fica em torno de ±3,6 dB RSS.
- **No teste:** desligue os cabos de debug e UART. Fechada a lata, o cabo vira o radiador que sobra.

## I. Edição de esquemático por script ou MCP
Fonte: KiCad-MCP (`HEADLESS_AUTHORING.md`, `TOOL_INVENTORY.md`, `DATASHEET_TOOLS_GUIDE.md`).

- **Netlist "golden":** antes e depois de qualquer edição em lote ou limpeza cosmética, rode `kicad-cli sch export netlist --format kicadxml` na folha raiz e compare os mapeamentos net → {REF.PIN}. Uma limpeza cosmética não pode mudar a netlist.
- **Pegadinhas de símbolo:**
  - **Símbolo com unidade de alimentação separada** (ex.: `74xx:74LS139`): pôr só a unidade A gera `missing_power_pin`; inclua a unidade de alimentação.
  - **Pad exposto de QFN/DFN tipado `power_input`:** dá erro de ERC até ser ligado, normalmente a GND.
  - **Símbolo apagado que foi ligado por `batch_add_and_connect`:** deixa labels órfãs; use `deleteAttachedLabels: true`.
  - **Espaçamento:** deixe ~12,7 mm entre peças, porque um global label ocupa ~7,6 mm.
- **Lint antes do ERC final** (ferramentas do KiCad-MCP):
  - `validate_schematic`: falha estrutural, com linha e coluna;
  - `find_orphaned_wires`, `find_wires_crossing_symbols`, `find_overlapping_elements`;
  - `find_duplicate_symbols`: sobra de Eagle/SnapEDA;
  - `lint_schematic_cosmetic` e `autoplace_schematic_fields`: passes que não mudam a netlist;
  - `digikey_check_library_availability`: obsoleto ou sem estoque;
  - `enrich_datasheets`: preenche o campo Datasheet com o link LCSC.
- **Campos de sourcing com nomes reconhecidos:** `MPN`, `Manufacturer`, `LCSC`, `DigiKey_PN`, `Mouser_PN` e os paramétricos `Voltage`, `Tolerance`, `Power`, `Dielectric`. Com tensão e dielétrico em campos, a revisão de DC bias e de margem de tensão fica mecânica.
- **`pcbnew.SaveBoard` regrava o `.kicad_pro`** com o modelo de projeto em memória, que pode estar desatualizado (KiCad-MCP `KNOWN_ISSUES.md` #5). **FATO, testado em 2026-11-21 no KiCad 10.0.8:** carregar e salvar o demo `stickhub` mudou o hash do `.kicad_pro`. Grave netclasses editando o JSON do `.kicad_pro` e compare o arquivo antes e depois de scripts que salvam a placa. `gnd_fix.py` e `island_fix.py` usam `safe_save()`, que restaura o `.kicad_pro` original se ele mudar (testado). O `kicad_to_jlc.py` cruza BOM × CPL e sai com erro se algum designator do BOM não tiver posição.

## O que NÃO foi adotado das fontes (contradiz as referências 00–10)
- **Dados JLC do kicad-happy (verificados em 2025-01, defasados):**
  - trilha mínima 0,127 mm, silk 0,8 mm e cobre-borda 0,3 mm;
  - "peças Basic grátis", sem separar Economic de Standard;
  - Economic aceitando 0201;
  - tabela fixa de offset de rotação.
  - Os valores atuais estão em `06`, `09` e `10`.
- **Distância à borda** de 1 mm (SMD) / 2 mm (THT): mais fraca que a regra JLC de corpo a 2,5 mm e de MLCC a ≥ 5 mm.
- **Via de retorno e pinos de GND em conector:** tratados em `12-via-retorno-e-pinos-gnd.md`, que traz pesquisa própria.
- **KiCad-MCP:**
  - "ground plane partitioning" genérico (`04` defende plano único);
  - o prompt que diz que `export_bom` exporta campos customizados (o código não exporta; ver `09`);
  - o prompt de footprint com "KiCad 9", furo mínimo de 0,5 mm e silk de 0,12 mm.
