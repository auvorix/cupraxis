# 11 — Análise de skills relacionadas (KiCAD-MCP-Server, kicad-happy, ESP32-AI-Agent-Skill)

Data: 2026-11-21. Objetivo: listar o que vale incorporar na skill `cupraxis` sem duplicar o que ela já tem (SKILL.md, `references/01–10`, `regras-da-casa.md`, scripts). Nenhum arquivo da skill foi alterado. Os repositórios do GitHub foram clonados no scratchpad, lidos como dados (nenhum script executado, nada instalado) e apagados no fim.

Versões analisadas (para os links serem estáveis):
- **KiCAD-MCP-Server** local: `%USERPROFILE%\AppData\Local\Programs\KiCAD-MCP-Server`, commit `9dd467c` (2026-11-11), v2.9.0.
- **kicad-happy**: commit `6b9767e19979cdef91631573753b1547efdbeab9` (2026-11-15). Base dos links: `https://github.com/aklofas/kicad-happy/blob/6b9767e19979cdef91631573753b1547efdbeab9/` (abreviado **KH/** abaixo).
- **esp32-ai-agent-skill**: commit `124d298e4ccaa737dbf6d26bbae47722e17f3097` (2026-04-14). Base: `https://github.com/ezrover/esp32-ai-agent-skill/blob/124d298e4ccaa737dbf6d26bbae47722e17f3097/` (abreviado **ESP/**).
- Nos links para arquivos `.md` do GitHub, acrescente `?plain=1` antes de `#L…` para a âncora de linha funcionar (ex.: `…/pcb-emc-rules.md?plain=1#L84`). As IDs X1–X12 são as contradições; A–E são os itens a aproveitar.

---

## Resumo

- **kicad-happy é a fonte que mais agrega.** Traz um conjunto de regras de EMC de layout com **limiares numéricos e fonte** (Ott, Paul, Bogatin, Hubing, TI). Exemplos: cobre do nó SW de 25/100 mm², área do hot loop medida pelos pads de 25/100 mm², indutor não blindado a ≤ 15 mm de ADC/cristal/RF, TVS com ≥ 2 vias de GND a ≤ 3 mm, filtro de entrada com f_sw/f_c ≥ 5, Z_target do PDN. Traz também um **checklist de revisão de esquemático por classe de peça**. A cupraxis tem a física (04 D, 02 A), mas não tem esses limiares como critério de revisão, nem nenhuma checagem automática deles no `pcb_audit.py`. Também falta uma revisão de esquemático estruturada: o gate da etapa 3 hoje é "ERC 0; desacoplamento; ESD; pull-ups".
- **No KiCAD-MCP-Server, o que interessa são os prompts `pdn_dc_review` e `emc_shield_review`** (`src/prompts/design.ts`), com regras curtas e corretas (IPC-2152 × IPC-2221 em plano, 525 mA/mm como sinal de aglomeração, não limite térmico, Z_target, "desligue o cabo de debug no teste irradiado"). Também vale o restante do `HEADLESS_AUTHORING.md` que o `09` ainda não cobre (diff de netlist "golden", unidade de alimentação separada, pino EP tipado `power_input`). Os outros prompts (layout review, stackup, routing, component) são listas genéricas que a cupraxis já supera. Alguns até a contradizem ("Consider ground plane partitioning").
- **ESP32-AI-Agent-Skill tem pouco valor para PCB.** O foco é firmware e LVGL. Os dados de pinos são rasos e têm erros. O mais grave: o validador **não conhece o ESP32-C5** (o chip da casa) e cai em silêncio nos pinos do ESP32 clássico. Só vale a *lista de categorias* de checagem de pino (flash, strapping, USB, ADC2+Wi-Fi, input-only, PSRAM octal). Os números devem vir dos datasheets da Espressif.
- **Licenças:** as três são MIT. Parafrasear heurísticas com atribuição tem risco baixo. Portar código (por exemplo, lógica do `emc_rules.py` para o `pcb_audit.py`) exige levar o aviso MIT. A tabela IPC-2221A copiada no kicad-happy não vira MIT por estar lá: risco médio.
- **Achado interno da cupraxis:** o SKILL.md diz "λ/20 ≈ 3,4 mm a 2,45 GHz". O `04` D3 e o kicad-happy dão 2,9–3,0 mm (εr 4,4). Ver "O que NÃO aproveitar", item X10.

---

## Por fonte

### 1. KiCAD-MCP-Server (mixelpixx), MIT

- **O que é:** servidor MCP com 253 ferramentas para o KiCad (SWIG/IPC), mais 20 prompts MCP (`grep -c "server.prompt("`: design 7, component 6, routing 5, footprint 2) (templates de texto) em `src/prompts/*.ts` e documentação em `docs/`.
- **Licença:** MIT, "Copyright (c) 2024 mixelpixx" (`LICENSE`).
- **Qualidade e maturidade:** o código e o CHANGELOG são ativos e detalhados, e o `09` já documenta as armadilhas das ferramentas. Os prompts têm qualidade **desigual**:
  - `design.ts` `pdn_dc_review` (l. 353–404) e `emc_shield_review` (l. 409–463) são recentes, precisos e proíbem inventar números. São bons.
  - `pcb_layout_review`, `layer_stackup_planning`, `design_rule_development`, `component_selection_guidance` e `pcb_design_optimization` (design.ts l. 24–348), mais todos os de `routing.ts` e `component.ts`, são **listas genéricas de tópicos sem números**.
  - `footprint.ts` é desatualizado ("KiCAD 9", l. 36) e tem erro (l. 88).
  - `docs/PCB_DESIGN_WORKFLOW.md` está **defasado**: fala em "229 tools" (l. 308), mas são 253, e recomenda `export_gerber`, `export_bom` e `route_pad_to_pad` (l. 208, 216, 301), justamente as ferramentas que o `09` aponta como armadilha.
  - `HEADLESS_AUTHORING.md` e `KNOWN_ISSUES.md` são bons e vêm de campo.

### 2. kicad-happy (Andrew Klofas), MIT

- **O que é:** skills para Claude Code, Codex e outros agentes: `kicad` (análise de esquemático, PCB e Gerber), `emc`, `bom`, `datasheets`, `spice`, `jlcpcb`, `pcbway`, `lcsc`, `digikey`, `mouser` e `element14`. Os analisadores Python usam só a stdlib.
- **Licença:** MIT, "Copyright (c) 2025 Andrew Klofas" (`LICENSE`).
- **Qualidade e maturidade:** **alta.**
  - 1.716 estrelas, push em 2026-11-19, CI, cerca de 300 arquivos de teste.
  - `VALIDATION.md` diz que cada versão roda contra um corpus de 5.858 projetos KiCad abertos (KiCad 5 a 10).
  - As regras de EMC citam livro ou app note, dizem quando o limiar é heurístico e foram "verified April 2026".
  - **Ponto fraco:** os dados de fabricante (skill `jlcpcb`, tabela "Fab House Capabilities") foram "verified 2025-01" e estão defasados em relação à cupraxis (2026-11). Ver a seção "O que NÃO aproveitar".

### 3. ESP32-AI-Agent-Skill (ezrover / "Vibe Coder"), MIT

- **O que é:** skill de "engenheiro embarcado ESP32", com escolha de chip, mapa de GPIO, validador `validate_pinmap.py` e gerador de config. Mais da metade do repositório é referência de LVGL e de placas Waveshare.
- **Licença:** MIT, "Copyright (c) 2026 Vibe Coder" (`LICENSE`).
- **Qualidade e maturidade:** **baixa para hardware.**
  - 57 estrelas, último push em 2026-08-03.
  - As fichas por chip têm de 18 a 30 linhas. A do ESP32-C5 diz "GPIO Count: ~20-30 (refer to specific module datasheet)" e não traz strapping.
  - Inconsistências internas: no C6, a strapping é "8, 9, 15" em `esp32-pins.md:334` e `{4, 5, 8, 9, 15}` em `esp32.py:38`.
  - O validador não tem ramo para C5, C2, H2 ou P4 (`esp32.py:1029`, `1044`, `1060`: "Default to base ESP32 for unknown variants").

---

## O que aproveitar

Legenda de esforço: **baixo** = editar texto de uma referência; **médio** = seção nova ou checagem simples em script; **alto** = checagem geométrica nova no `pcb_audit.py`. Todo número vindo do kicad-happy deve entrar rotulado como "heurística kicad-happy (fonte primária X)", seguindo a regra "De onde vem cada número" do SKILL.md.

### A. EMC e layout (kicad-happy, `skills/emc/references/pcb-emc-rules.md`)

| # | Item (heurística literal) | Fonte | Por que agrega (o que falta na cupraxis) | Onde encaixar | Esforço | Risco de licença |
|---|---|---|---|---|---|---|
| A1 | **SW-002:** cobre total no nó SW/LX: warning ≥ 25 mm², error > 100 mm² (TI SLVA477) | KH/skills/emc/references/pcb-emc-rules.md#L84 | O `02` diz "nó SW mínimo", mas não dá número verificável numa revisão | `02` §A (regra nova) + linha na tabela "Proximidade/Revisão de placement"; depois checagem no `pcb_audit.py` (somar a área de pads, trilhas e zonas da net SW) | baixo (texto) / alto (script) | baixo (paráfrase, com atribuição) |
| A2 | **SW-003:** área do hot loop **medida pelos pads** (Cin+ → VIN do CI; SW do CI → pad SW do indutor; GND do CI → Cin−): warning 25–100 mm², error > 100 mm². Se só houver os centros das peças, o resultado é apenas "info" | KH/…/pcb-emc-rules.md#L91 | A cupraxis manda "laço mínimo" sem limiar e sem dizer como medir | `02` §A + checklist de revisão de layout | baixo / alto | baixo |
| A3 | **ML-001:** indutor de conversor **não blindado (ou de blindagem desconhecida)** a < 15 mm de ADC, op-amp, cristal (ou do CI que ele alimenta) ou peça de RF: warning; a < 8 mm e sabidamente não blindado: error. Correção: indutor blindado ou eixo perpendicular às trilhas sensíveis | KH/…/pcb-emc-rules.md#L374 | Não existe distância numérica indutor→sensível na cupraxis (grep "blindado" só acha recomendação qualitativa) | `01` tabela de proximidade + `02` §A | baixo | baixo |
| A4 | **DC-001/DC-003:** capacitor de desacoplamento a > 5 mm do CI = warning, > 8 mm = error; capacitor a > 3 mm da via mais próxima = warning (a indutância da via domina; trilha sobre plano ≈ 0,3–0,8 nH/mm, não "1 nH/mm") | KH/…/pcb-emc-rules.md#L38, #L50 | O SKILL.md diz "no pino, laço mínimo", mas não dá limite para auditar. O valor de nH/mm também falta (grep "nH/mm" = 0) | Tabela "Proximidade" do SKILL.md (coluna Regra) + `02` §C; checagem simples no `pcb_audit.py` (distância do C ao pino de alimentação do U na mesma net) | baixo / médio | baixo |
| A5 | **ES-001/ES-002:** TVS a > 15 mm (centro a centro) do conector = warning; **< 2 vias de GND a ≤ 3 mm do TVS** = error (duas vias em paralelo: ~0,5 → ~0,25 nH, ~9 V a menos de clamp) | KH/…/pcb-emc-rules.md#L335, #L342 | O `04` D5 tem a física (0,25 nH ≈ 10 V) e "sem via antes do TVS", mas não o critério "≥ 2 vias de GND junto ao TVS" | `04` D5 (acrescentar a regra das 2 vias) + checagem no `pcb_audit.py` | baixo / médio | baixo |
| A6 | **TH-002:** ferrite a ≤ 10 mm de regulador chaveado: info. A permeabilidade cai com a temperatura e a impedância pode cair 30–50 % acima de ~85 °C | KH/…/pcb-emc-rules.md#L357 | O `02` §E fala de ferrite por corrente (≤ 20 % de I nominal), mas não por temperatura | `02` §E | baixo | baixo |
| A7 | **EF-001:** filtro EMI de entrada do SMPS com f_sw / f_corte ≥ 5 (margem para a queda de −40 dB/década) | KH/…/pcb-emc-rules.md#L321 | O `02` §E manda amortecer o ferrite+C e conferir a ressonância, mas não dá a razão mínima | `02` §E | baixo | baixo |
| A8 | **CK-003 / BE-001:** trilha de clock a < 10 mm de conector externo = warning; sinal na camada externa a < 1× a altura do dielétrico da borda = warning/error | KH/…/pcb-emc-rules.md#L113, #L257 | O `04` C4 tem "par rápido ≥ 2,3 mm da borda do plano", que é **mais forte** que o BE-001. O CK-003 (clock perto de conector) é novo | `04` C4: acrescentar só o CK-003 e manter o C4 como está | baixo | baixo |
| A9 | **Fórmulas de estimativa** (para dizer "que banda corre risco", **não** para prever aprovação; precisão de ±10–20 dB): E_DM = 2,632×10⁻¹⁴·f²·A·I/r (com plano); E_CM = 1,257×10⁻⁶·f·L·I_CM/r; regras de escala (2× área = +6 dB; 2× f = +12 dB); ressonância de cavidade f_mn = c/(2√εr)·√((m/L)²+(n/W)²) (100×80 mm → f₁₀ ≈ 714,5 MHz); fenda f = c/2L; via L = 0,2·h·[ln(4h/d)+1] nH; joelho 0,35/t_r e 0,5/t_r | KH/…/pcb-emc-rules.md#L163, #L178–L221, #L365 | O `04` D1 cita só qualitativamente as três fontes de emissão. Sem fórmula não dá para priorizar | `04` §D, subseção nova "Estimativas rápidas (INFERÊNCIA/ordem de grandeza)" | baixo | baixo |
| A10 | **Pré-conformidade UE:** limites CISPR 32/EN 55032 Classe B a 10 m: 30 dBµV/m (30–230 MHz) e 37 dBµV/m (230–1000 MHz); a 3 m, 40/47. Conversão 3 m→10 m = −10,5 dB. **Margem de projeto ≥ 6 dB** (incerteza de câmara de ±3,6 dB RSS). 5 µA de corrente de modo comum num cabo de 1 m a 100 MHz já passam o limite FCC B em ~3 dB | KH/skills/emc/references/emc-standards.md#L29, #L74, #L80 | A cupraxis cita a EN 55032 (04 D7) sem nenhum número de limite. O produto da casa vende na UE | `04` D7 | baixo | baixo (dados de norma; conferir no texto da IEC antes de tratar como FATO) |
| A11 | **Prática de teste (MCP `emc_shield_review`):** "Unplug debug and UART cables for a radiated test. A cable can be the remaining radiator once the seam is closed"; "A fitted can is not shielding by itself. A few clips can leave a slot that is louder than no can"; supressão em dB = 20·log10(E_antigo/E_novo) (razão de campo, não de potência) | MCP `src/prompts/design.ts:450`, `:456`, `:444` | Falta na cupraxis (o `03` manda usar shield can, mas não fala de quantos clips/vias ele precisa) | `03` (shield can) + `04` D7 | baixo | baixo |

### B. Energia e PDN

| # | Item | Fonte | Por que agrega | Onde encaixar | Esforço | Risco de licença |
|---|---|---|---|---|---|---|
| B1 | "For a plane, use IPC-2152. IPC-2221 is for an isolated trace. Applied to a plane it overstates the temperature rise"; "525 mA/mm is 15 A/mm² in 35 µm copper. It marks crowding. It is not a thermal limit." | MCP `design.ts:389`, `:391` | A cupraxis manda usar IPC-2152 (Saturn), mas não diz por que a IPC-2221 erra em plano, nem dá o critério de aglomeração | `02` §D | baixo | baixo |
| B2 | **Z_target = ΔV_permitido / ΔI_degrau** (ΔI = degrau transitório, não a corrente DC); "Nominal microfarads on the schematic are not the effective capacitance". O kicad-happy usa por padrão Z_target = V·5 % / (0,5·I_transitório) e aceita picos de anti-ressonância até 200 MHz | MCP `design.ts:395`; KH/…/pcb-emc-rules.md#L276 (PD-001), #L287 (PD-003: Z no pino do CI = Z_local ∥ (Z_reg + R_trilha + jωL_trilha)) | grep "Z_target / impedância alvo" na cupraxis = 0 | `02` §C | baixo | baixo |
| B3 | **PD-004 acoplamento entre rails:** o conversor a jusante puxa I_in = V_out·I_out / (V_in·η·D) pulsado em f_sw do rail a montante | KH/…/pcb-emc-rules.md#L294 | Novo; relevante na árvore de energia (etapa 1) | `02` §C | baixo | baixo |
| B4 | "Keep [the switch node] small and on the outer layer over unbroken ground… Do not move the switch node onto an inner layer: that adds vias and capacitive coupling" | MCP `design.ts:397` | Complementa o `02` §A, que não fala de camada do nó SW | `02` §A | baixo | baixo |
| B5 | **Orçamento de corrente em sono (bateria):** somar o sono do MCU, divisores sempre ligados (I = Vbat/(Rt+Rb)), Iq dos reguladores, pull-ups com caminho, fuga de TVS/FET/diodo e LED; **sinalizar qualquer contribuinte > 10 % do total**. Tensão mínima de bateria = Vin_min do regulador + I_pico·R_interna + margem. Pinos de EN de reguladores com pull-down para ficarem desligados no boot | KH/skills/kicad/references/schematic-analysis.md#L741, #L759 | O `02` §F (LiPo) não tem método de orçamento de sono nem de V_bat mínima sob pico (TX Wi-Fi) | `02` §F | baixo | baixo |

### C. Revisão de esquemático (gate da etapa 3)

| # | Item | Fonte | Por que agrega | Onde encaixar | Esforço | Risco de licença |
|---|---|---|---|---|---|---|
| C1 | **Checklist por classe de peça**, com destaques: <br>• **Regulador:** Vin de pior caso (com tolerância e transiente); recalcular Vout pelo divisor FB e conferir contra o nome da rail; EN não flutuante (limiar × tensão que o aciona); pull-up do PG no domínio certo; C de entrada/saída com valor **efetivo após DC bias**; P = (Vin−Vout)·I e Tj. <br>• **MCU:** cada par VDD/VSS com seu capacitor; VDDA com filtro próprio; boot straps no sentido do boot desejado; nenhum pino alimentado por domínio mais alto que o seu (5 V tolerance). <br>• **MOSFET:** "Rds(on) at the actual Vgs, not the datasheet minimum test condition"; pull-down de gate. <br>• **TVS:** tensão de trabalho ≥ o nível alto normal da rail; tensão de clamp ≤ abs max do pino protegido. <br>• **Indutor:** Isat ≥ 1,3× pico. <br>• **Capacitor:** tensão ≥ 1,5× a aplicada. <br>• **Interface:** VIH do receptor × VOH do driver; dono do pull-up e pull-ups em paralelo no mesmo barramento. | KH/skills/kicad/references/deep-review.md#L18, #L73; schematic-analysis.md#L248, #L312, #L332, #L342, #L352 | O gate 3 hoje é "ERC 0; desacoplamento; ESD; pull-ups; jumpers". O `05` cobre bem a escolha de peça, mas não a **revisão do circuito ligado** | SKILL.md, gate da etapa 3 (1 linha apontando para o checklist) + seção nova "Checklist de revisão de esquemático" no `05`, ou um `references/11-revisao-esquematico.md` novo | médio | baixo |
| C2 | **Tolerância empilhada do divisor de FB:** Vout_max = VREF_max·(1 + Rt(1+tol)/(Rb(1−tol))); Vout_min análogo. Exemplo do texto: 0,595 V ±2,5 %, 820 k/110 k a 1 % → 4,82–5,25 V. Usar Vout_max contra o abs max a jusante e Vout_min contra o headroom de LDO. O mesmo vale para divisor de ADC, filtro RC (10 k 5 % + 100 nF 10 % → 138–186 Hz) e capacitor de carga de cristal | KH/…/schematic-analysis.md#L587, #L794 | Ausente na cupraxis | `02` §A (FB) + `05` §E (cristal) | baixo | baixo |
| C3 | **Tabela de pinagem de conectores padrão** (erros mais comuns): FTDI 6 pinos (TX da placa → RXD do cabo, pino 5); SWD 10 pinos (1 = VTref, 2 = SWDIO, 4 = SWCLK, 6 = SWO, 10 = nRST); Qwiic (1 GND, 2 3V3, 3 SDA, 4 SCL); CAN (terminação de 120 Ω); RS-485 (polaridade A/B varia por fabricante); Micro-B (ID em NC no device) | KH/…/schematic-analysis.md#L880 | Ausente (grep "FTDI" = 0) | `05` §M (programação e debug) e §K | baixo | baixo (fatos de padrões; conferir SWD e Qwiic no documento oficial) |
| C4 | **Auditoria de mux de GPIO:** para cada pino do MCU, conferir no datasheet que a função atribuída existe naquele pino; procurar dois periféricos no mesmo pino, ADC num pino usado como digital, JTAG/SWD usado como GPIO (perde o debug), strapping ligado a periférico que o puxa no boot (ex.: GPIO0 do ESP32 como CS de SPI) | KH/…/schematic-analysis.md#L840; ESP/references/platforms/esp32-pins.md (categorias) | A cupraxis tem strapping só como item de placement (`01` #29) e no eval do C3. Não existe procedimento de auditoria de pinos | Mesmo destino de C1. Para ESP32, puxar a strapping e os pinos de flash e PSRAM **do datasheet do chip usado** (C5: Espressif), nunca do repo ESP32 | médio | baixo |
| C5 | **Severidade de esquemático** (Crítico/Aviso/Sugestão/Info), com exemplos: Crítico = abs max excedido, falta capacitor de saída do regulador, pino de alimentação flutuante, divisor FB com sobretensão; Aviso = margem < 20 %, DC bias não considerado, falta ESD externo | KH/…/schematic-analysis.md#L658 | O formato de revisão do SKILL.md (Crítico/Alto/Médio/Baixo) só dá exemplos de layout | SKILL.md, "Formatos de resposta" (uma frase) ou C1 | baixo | baixo |

### D. KiCad / MCP / fabricação

| # | Item | Fonte | Por que agrega | Onde encaixar | Esforço | Risco de licença |
|---|---|---|---|---|---|---|
| D1 | **Paridade de designators BOM × CPL antes do upload:** cruzar os designators e listar os "órfãos" do CPL (furo, fiducial e test point são esperados; qualquer outro indica BOM/placa divergentes). O kicad-happy afirma que "JLCPCB's web upload UX silently rejects orphan-designator CPLs with an unhelpful error" (afirmação deles, não verificada) | KH/skills/jlcpcb/SKILL.md#L205, #L222 | O `scripts/kicad_to_jlc.py` hoje só imprime contagens (`bom lines`, `missing lcsc`, `cpl`). O `09` R1 já exige "todo designator do BOM tem de existir no CPL", mas nada confere isso. O grader `evals/kicad-cli-fab-automation/graders/16-bom-cpl-cruzado.md` espera o cruzamento | `scripts/kicad_to_jlc.py`: comparar os conjuntos de designators, imprimir a diferença e sair com código ≠ 0 se faltar posição para algum item do BOM | baixo | nenhum (implementação própria) |
| D2 | **Diff de netlist "golden"** para provar que uma limpeza cosmética ou edição em lote não mexeu na conectividade: `kicad-cli sch export netlist --format kicadxml` da folha raiz antes e depois, comparando net → {REF.PIN} | MCP `docs/HEADLESS_AUTHORING.md:216` | Ausente (grep "golden" = 0). Útil sempre que o agente edita esquemático por script ou MCP | `08` (receita nova) ou `09` R2.1 | baixo | baixo |
| D3 | **Pegadinhas de símbolo ainda não registradas no `09`:** (a) símbolo multi-unidade com **unidade de alimentação separada** (ex.: `74xx:74LS139`): pôr só a unidade A gera `missing_power_pin`, então ponha a unidade de alimentação; (b) pino de **EP de DFN/QFN tipado `power_input`** dá erro até ser ligado (normalmente a GND); (c) apagar símbolo ligado por `batch_add_and_connect` deixa labels órfãs: usar `deleteAttachedLabels: true`; (d) espaçar peças ~12,7 mm (um global label ocupa ~7,6 mm) | MCP `docs/HEADLESS_AUTHORING.md:153`, `:160`, `:171`, §2 | O `09` R2.1 já tem a grade de 2,54 mm, o ERC em mm/100, a folha raiz, o PWR_FLAG e o símbolo "flat". Estes quatro itens faltam | `09` R2.1 (tabela) | baixo | baixo |
| D4 | **Ferramentas de lint do MCP que o `09` não cita:** `validate_schematic` (falha estrutural com linha e coluna), `find_orphaned_wires`, `find_wires_crossing_symbols`, `find_overlapping_elements`, `find_duplicate_symbols` (sobra de Eagle/SnapEDA), `lint_schematic_cosmetic` + `autoplace_schematic_fields` (passes que não mudam a netlist), `digikey_check_library_availability` (obsoleto/sem estoque por símbolo), `enrich_datasheets` (preenche o Datasheet com `https://www.lcsc.com/datasheet/<LCSC>.pdf` sem rede) | MCP `docs/TOOL_INVENTORY.md:244–250`, `:300`, `:311`, `:346`, `:485`; `docs/DATASHEET_TOOLS_GUIDE.md` | grep na cupraxis = 0 para todas | `09` R2.1 (linha "lint antes do ERC final") | baixo | baixo |
| D5 | **Save pelo `pcbnew` pode regravar o `.kicad_pro`:** "pcbnew serializes a possibly stale in-memory project model over `.kicad_pro` on every `SaveBoard`/`BOARD.Save`". O MCP precisou de um guard que restaura `net_settings`. Netclass deve ser gravada por edição direta do JSON do `.kicad_pro` | MCP `docs/KNOWN_ISSUES.md:80–95` | `scripts/gnd_fix.py:193` e `scripts/island_fix.py:154` chamam `pcbnew.SaveBoard`, e o `08`:220 confirma que o SaveBoard "grava também `<dst>.kicad_pro`". Risco de perder netclasses editadas fora do pcbnew (INFERÊNCIA: não testado nos nossos scripts) | `08` §Armadilhas + nota nos dois scripts (comparar o `.kicad_pro` antes e depois, ou usar `SaveBoard(..., aSkipSettings=True)`, assinatura já listada no `08`:202) | baixo | nenhum |
| D6 | **Campos de sourcing com nomes que as ferramentas reconhecem:** `MPN`, `Manufacturer`, `LCSC`, `DigiKey_PN`, `Mouser_PN`, `Voltage`, `Tolerance`, `Power`, `Dielectric`. Os campos custom ficam ocultos por padrão | MCP `src/prompts/component.ts:234–246` | O SKILL.md fala só de `MPN`, `Manufacturer` e `LCSC`. Os campos paramétricos (Voltage, Dielectric) permitem conferir o DC bias e a tensão na revisão | SKILL.md, "Fabricante: projetar de forma agnóstica" (3º item) | baixo | baixo |

### E. Normas (opcional, com cuidado)

| # | Item | Fonte | Por que agrega | Onde encaixar | Esforço | Risco de licença |
|---|---|---|---|---|---|---|
| E1 | **Espaçamento por tensão IPC-2221A Tabela 6-1** (B1 interno, B2 externo sem coating, A6 montado sem coating etc.) e **IEC 60664-1** para circuitos ligados à rede | KH/skills/kicad/references/standards-compliance.md#L73 | O `09` diz que o `set_voltage_clearance_rules` "não traz valores: a tabela vem da norma do usuário". A cupraxis não tem a tabela | `06` ou `04` §E, **só depois de conferir no PDF da IPC**: a tabela copiada tem 5 colunas rotuladas no cabeçalho e 7 valores por linha (formatação quebrada) | médio | **médio** (tabela de norma IPC protegida por copyright; citar a norma e transcrever só os valores necessários) |

---

## O que NÃO aproveitar e por quê

### Contradições com as referências da cupraxis (sinalizar; não adotar)

| # | O que a fonte diz | O que a cupraxis diz | Veredito |
|---|---|---|---|
| X1 | **RP-001:** via de retorno a ≤ max(2·h, 1,0 mm) da via de sinal (KH/…/pcb-emc-rules.md#L303) | SKILL.md e `04` A6: ≤ 5 mm (200 mil, TI SLLA414), "quanto mais perto melhor" | Números diferentes para o mesmo critério. O kicad-happy é mais estrito e é heurística deles. Manter o SLLA414 como limite e, no máximo, citar o RP-001 como "alvo" no `04` A6. Avisar o dono |
| X2 | **IO-002:** pinos de GND do conector ≥ max(2, sinais/4) (KH/…#L65) | `04` D4: ≥ 1 retorno de GND para cada 9 sinais (TI SZZA009 §2.5.3) | Divergência de número (1:4 × 1:9). O kicad-happy não cita fonte primária para o 1:4. Não adotar. Registrar em `00-conflitos-e-lacunas.md` |
| X3 | **GP-005:** com vários domínios de GND, "verify domains connect at a single intentional point (e.g., near the ADC)" (KH/…#L30); prompts do MCP: "Consider ground plane partitioning" (`routing.ts:59`, `component.ts:89`) | `04` A1–A3: plano **único e contínuo**, particionado por posição. Divisão só se obrigatória, com ponte única | O kicad-happy é compatível com o A2 (split só se obrigatório). O texto do MCP contradiz o A1. Não adotar |
| X4 | Tabela de distância de peça à borda: "SMD 1 mm, THT 2 mm, BGA 3 mm, V-score 2 mm" (KH/skills/kicad/references/pcb-layout-analysis.md#L266) | JLC: corpo ≥ 2,5 mm da borda para montagem; MLCC ≥ 5 mm de borda, V-cut ou furo | Bem mais fraca que as regras da casa. Não adotar |
| X5 | **BE-001:** sinal a < 1× h da borda (KH/…#L257) | `04` C4: par rápido ≥ 2,3 mm da borda do plano | Métricas diferentes. O BE-001 é muito mais fraco (h = 0,1–0,2 mm). Manter o C4 |
| X6 | Capacidades JLC "verified 2025-01": trilha/espaço 0,127 mm, via 0,45/0,2 mm, anel 0,125 mm, silk mínimo **0,8 mm** de altura, cobre ≥ **0,3 mm** da borda (KH/skills/jlcpcb/SKILL.md#L86–L94, #L236–L237; standards-compliance.md#L607) | SKILL.md (consulta 2026-11): 0,10/0,10 mm, via 0,15/0,25 mm, anel 0,18 mm, silk ≥ 1,0 mm, cobre ≥ 0,2 mm fresada / 0,4 mm V-cut | Dados defasados. Não usar |
| X7 | JLC: "Basic parts: No extra fee" (KH/skills/jlcpcb/SKILL.md#L127); Economic aceita 0201 (#L112) | `09` R1.7: Basic só é grátis na Economic; na Standard paga feeder de US$ 1,53. Economic exige peças ≥ 0402 (SKILL.md) | Errado ou defasado. O kicad-happy também se contradiz no tamanho mínimo da placa: 6×6 mm (#L93) × 10 mm (standards-compliance.md#L622). Não usar |
| X8 | Tabela fixa de offset de rotação JLC: "SOT-23 +180°, SOIC +90° ou +270°, QFN +90°" (KH/skills/jlcpcb/SKILL.md#L129) | `09` armadilha 4: conferir no visualizador DFM do fabricante, aplicar o offset por footprint | O offset depende do footprint da biblioteca e da fita, não da família. Adotar como regra induz erro. Não usar |
| X9 | MCP `HEADLESS_AUTHORING.md:77`: "Benign warnings (don't chase these)" | SKILL.md: ERC/DRC com **0 erros e 0 avisos**; aviso inevitável fica documentado com fonte | Aproveitar só o **diagnóstico** (de onde vem o aviso) para corrigir ou justificar. Nunca como licença para ignorar |
| X10 | kicad-happy: λ/20 a 2,4 GHz = 3,0 mm (εr 4,4) (KH/…#L133) | **Inconsistência interna da cupraxis:** o SKILL.md diz "≈ 3,4 mm a 2,45 GHz", e o `04` D3 diz 2,9 mm | Não é item para importar. O dono deve alinhar o SKILL.md com o `04` D3 (2,9 mm com εr 4,4; 3,4 mm só com εr efetivo ≈ 3,3 de microstrip, e então dizer isso) |
| X11 | MCP `component.ts:229`: campos custom "are exported by export_bom" | `09` R2.7: o `export_bom` não lê o campo LCSC (`python/commands/export.py:561`: `getattr(module, f"Get{attr}")()`, conferido de novo neste commit) | O prompt do MCP está errado. O `09` continua correto |
| X12 | MCP `PCB_DESIGN_WORKFLOW.md:208/216/301`: usar `export_gerber`, `export_bom` e "route_pad_to_pad is faster and more reliable" | `09` R2.4/R2.7 e armadilhas 1, 7 e 12 | Doc defasado ("229 tools", l. 308). Não usar |

### Genérico ou duplicado

- **Prompts genéricos do MCP:** `pcb_layout_review`, `layer_stackup_planning`, `design_rule_development`, `component_selection_guidance`, `pcb_design_optimization` (design.ts l. 24–348) e todos os de `routing.ts` e `component.ts`. São listas de tópicos ("Consider…") sem números. A cupraxis já cobre tudo com números e fonte (01–06). "Avoid right-angle bends" (`routing.ts:50`) é mito para baixa frequência e não acrescenta nada.
- **`footprint.ts`:** fala em "KiCAD 9" (l. 36). A tabela de pads diz "0402 … min 0.5 mm drill" (l. 88), o que não faz sentido para SMD. A tabela de pads "de memória" contraria a regra do SKILL.md de escolher o footprint pelo desenho do fabricante. O silk de 0,12 mm (l. 69) fica abaixo do mínimo JLC de 0,15 mm. Só o critério "courtyard ≥ 0,25 mm dos pads" (l. 64) é correto, e é padrão KLC já conhecido.
- **kicad-happy, regras já cobertas:** GP-001/GP-002 (fenda e plano), VS-001 (λ/20, igual ao `04` D3), SU-001..003 (stackup, igual ao `04` B), DP-001 (USB HS 25 ps; a cupraxis usa ≤ 1,27 mm de SPRAAR7, mais estrito), XT-001 "3H" (o `04` C3 já discute 3h × 3W), TH-001 (DC bias, já no `05` e no SKILL.md), SH-001 (fenda de conector, só relevante com carcaça metálica).
- **Fórmula de corrente IPC-2152 do kicad-happy** (`A = (117.555·ΔT^-0.913 + 1.15)·I^(…)`): eles mesmos marcam "PARTIALLY VERIFIED — from secondary sources". A cupraxis já manda usar a calculadora Saturn. Não importar.
- **Scripts do kicad-happy** (`analyze_schematic.py`, `analyze_pcb.py`, `analyze_emc.py`): são maduros, mas grandes, com formato JSON próprio e dependência entre si. Portar é alto esforço. **Alternativa:** o dono pode decidir instalar o kicad-happy como skill complementar de *revisão* (MIT), em vez de copiar código. Fica como decisão do dono; nada foi instalado.

### ESP32-AI-Agent-Skill (inseguro como fonte de pinos)

- **Não conhece o ESP32-C5:** `_get_strapping_pin_set` e `_get_flash_pins` não têm ramo para C5, C2, H2 ou P4 e caem em silêncio nos pinos do ESP32 clássico, strapping {0, 2, 5, 12, 15} e flash GPIO6–11 (ESP/scripts/platforms/esp32.py#L1029, #L1044, #L1060). Num projeto C5 a validação sai errada sem aviso.
- **C5 "ADC/WiFi Conflict: None"** sem fonte (ESP/references/esp32-c5/specs.md#L17). A ficha do C5 tem 18 linhas e nenhuma strapping.
- **C3 "No ADC2/WiFi conflict — all ADC channels work"** (ESP/references/esp32-c3/specs.md#L21; esp32-pins.md#L326). A Espressif desaconselha o ADC2 do C3 por limitação de hardware (INFERÊNCIA de memória: conferir na errata do ESP32-C3 antes de citar).
- **C6:** strapping inconsistente dentro do repo, "8, 9, 15" (esp32-pins.md#L334) × {4, 5, 8, 9, 15} (esp32.py#L38).
- **Exageros:** GPIO45 do S2/S3 em alto "can damage 3.3V flash" (esp32.py#L974, #L982). O próprio repo diz em outro lugar que a 1,8 V o módulo "WILL FAIL TO BOOT" (esp32-specifics.md#L88), o que é coerente com subtensão e não com dano. "Total chip ~1200 mA" (electrical-constraints.md#L121) não tem fonte.
- **O que fica:** só a lista de categorias de checagem de pino (flash/PSRAM reservados, strapping no boot, pinos de USB nativo, ADC2 × Wi-Fi no ESP32/S2/S3, input-only 34–39 sem pull no ESP32 clássico, PSRAM octal no S3). Ela entra no item C4 com os números tirados do datasheet do chip. **Não preencher a strapping do C5 de memória.**

---

## Recomendação priorizada

1. **Limiares de EMC de layout no `02`/`04` e no checklist de revisão (A1–A5, A7).** Itens: cobre do nó SW de 25/100 mm²; hot loop pelos pads de 25/100 mm²; indutor não blindado a ≤ 15 mm de ADC/cristal/RF; desacoplamento a 5/8 mm do CI e a ≤ 3 mm da via; TVS com ≥ 2 vias de GND a ≤ 3 mm; f_sw/f_c ≥ 5. Rotular como "heurística kicad-happy (fonte primária)". Esforço baixo (texto). Fecha a maior lacuna: revisar layout com número, não com "mantenha curto".
2. **Checklist de revisão de esquemático no gate da etapa 3 (C1, C2, C3, C5).** Por classe de peça: regulador (Vout recalculado, EN, PG, C efetivo), MCU (VDDA, straps, domínios), MOSFET (Rds(on) no Vgs real), TVS (clamp × abs max), Isat ≥ 1,3× pico, C ≥ 1,5× V; mais tolerância empilhada do FB e tabela de pinagem (FTDI, SWD, Qwiic, CAN, RS-485). Esforço médio. Hoje o gate 3 só pede o ERC.
3. **PDN (B1, B2, B4):** Z_target = ΔV/ΔI_degrau; IPC-2152 em plano e não IPC-2221; 525 mA/mm = sinal de aglomeração, não limite térmico; nó SW na camada externa. Esforço baixo, no `02` §C/§D.
4. **Paridade BOM × CPL no `kicad_to_jlc.py` (D1).** Diferença de designators, com código de saída ≠ 0. Esforço baixo. Atende o grader 16 e a regra que o `09` R1 já escreveu e ninguém confere.
5. **Risco do `SaveBoard` regravar o `.kicad_pro` (D5).** Nota no `08` §Armadilhas e conferência (diff do `.kicad_pro`) em `gnd_fix.py`/`island_fix.py`, ou `aSkipSettings=True`. Esforço baixo. Evita perder netclasses sem perceber.
6. **Pré-conformidade UE e práticas de teste (A10, A11).** Limites EN 55032 Classe B (30/37 dBµV/m a 10 m), margem de 6 dB, 3 m→10 m = −10,5 dB; desligar os cabos de debug/UART no teste irradiado; shield can com poucos clips pode irradiar mais que sem can. Esforço baixo, no `04` D7 e no `03`.
7. **Complementos do `09` R2.1 (D2, D3, D4):** diff de netlist "golden"; unidade de alimentação separada; pino EP `power_input`; `deleteAttachedLabels`; ferramentas de lint (`validate_schematic`, `find_orphaned_wires`, `find_duplicate_symbols` etc.). Esforço baixo.
8. **Orçamento de sono e V_bat mínima (B5)** no `02` §F, mais auditoria de mux de GPIO (C4) com dados do datasheet Espressif do C5. Esforço baixo a médio.

Depois (alto esforço, decidir com o dono): portar A1–A5 como checagens geométricas no `pcb_audit.py` (com o aviso MIT, se a lógica vier do `emc_rules.py`), ou adotar o kicad-happy como skill complementar de revisão.

Pendências para o dono:
- Alinhar o λ/20 do SKILL.md (3,4 mm) com o `04` D3 (2,9 mm) (X10).
- Registrar em `00-conflitos-e-lacunas.md` as divergências X1 (via de retorno) e X2 (pinos de GND por sinal).
