# 10 — Fabricantes de PCB e PCBA: comparação, formatos e projeto agnóstico

> Pesquisa de **2026-11-21**. Toda URL abaixo foi consultada nessa data, salvo indicação.
> Etiquetas: **FATO** = lido na página citada; **FATO-sec** = lido só no trecho que a busca mostrou da página (página inteira não abriu); **INFERÊNCIA** = dedução minha ou conta feita por mim a partir de números FATO.
> "não encontrado" = procurei e não achei fonte. Não inventei número.
> Material da JLCPCB já existe em `09-ferramentas-fabrica-mcp-cad.md` (R1, pedido JLC) e `06-shape-dfm-estetica.md` (DFM JLC). Aqui a JLC entra só para comparação; os números JLC vêm desses arquivos (consulta de 2026-11-20/21) e da página de capacidades relida hoje.
> Contexto do dono: mora na **Irlanda** (UE). Isso pesa na escolha por causa do IVA/alfândega.

## Resumo

1. **Não existe "mínimo universal" publicado.** Cada fabricante publica um conjunto próprio e, às vezes, contraditório entre páginas. O mínimo comum seguro, que passa em todos os fabricantes pesquisados no serviço padrão de 2 camadas (exceto a altura de silk da Multi-CB, 1,2 mm, e da Würth, 1,5 mm), é ditado pelos mais conservadores (Aisler HASL e Elecrow): **trilha/espaço 0,20/0,20 mm, via com furo 0,30 mm e anel 0,20 mm (pad 0,70 mm), cobre-borda 0,40 mm (0,50 com V-cut), silk 0,17 mm × 1,0 mm (1,5 mm de altura se incluir a Würth)**. Ver a seção "projeto agnóstico" (INFERÊNCIA a partir dos números FATO da tabela).
2. **BOM e CPL não têm padrão.** JLC quer `Comment, Designator, Footprint, LCSC/JLCPCB Part #` + `Designator, Mid X, Mid Y, Layer, Rotation`; PCBWay quer MPN + fabricante; MacroFab usa um único arquivo `.XYRS` separado por tabulação e **em mils**; Aisler, OSH Park e MacroFab leem o `.kicad_pcb` direto e montam o BOM sozinhos a partir dos campos `MPN`. Mantenha no esquemático os campos `MPN`, `Manufacturer` e `LCSC`, e gere o formato de cada um na saída (FATO, seção de formatos).
3. **Rotação é a armadilha nº 1 da montagem.** Ninguém publica a convenção de "0°" de forma completa; a JLC diz que o 0° dela pode diferir do seu. Sempre conferir a prévia/DFM do fabricante e usar campos de correção por peça (`JLCPCB_CORRECTION`, `PCBWAY_CORRECTION`, `FT Rotation Offset`) (FATO: KiKit, Fabrication Toolkit, FAQ JLC).
4. **UE desde 01/07/2026:** acabou a isenção de imposto de importação para remessas ≤ 150 €. Remessa B2C ≤ 150 € paga **3 € por linha de item (código HS)** de "temporary customs duty", o IOSS só cobre o IVA, e desde 01/11/2026 há a **Union Handling Fee de 2 € por linha** (FATO: FAQ JLC, aviso NextPCB). Fabricar **dentro da UE** (Aisler/DE, Eurocircuits/BE, Multi-CB e Würth/DE) evita alfândega por completo (INFERÊNCIA: mercado único, sem importação). Atenção: a Multi-CB vende só a empresas, e Multi-CB e WEdirekt não montam.
5. **Arquivo nativo do KiCad:** **Eurocircuits**, **Multi-CB**, **OSH Park** ("We accept `.kicad_pcb` board layout files directly", processa com KiCad 9.x), **Aisler** (upload nativo e plugin "AISLER Push for KiCad", KiCad 10 suportado) e **MacroFab** (importa `.kicad_pcb`) aceitam. **Cuidado com a versão:** a OSH Park processa com KiCad 9.x e a MacroFab cita KiCad 8; uma placa salva no KiCad 10 pode não abrir num parser mais antigo (INFERÊNCIA). Só a Aisler tem fonte confirmando suporte ao KiCad 10. Os chineses querem Gerber RS-274X + Excellon em zip. ODB++ é aceito pela Aisler como alternativa; na JLC não há confirmação (FATO, ver tabela).
6. **KiKit `kikit fab`** tem exatamente `jlcpcb`, `pcbway`, `oshpark`, `neodenyy1` e `openpnp` (FATO, código-fonte). **Não existe** `kikit fab neodenyy` (o nome é `neodenyy1`), nem `aisler`/`eurocircuits`.
7. **Regras DRU:** há `.kicad_dru` oficial da PCBWay (zip, 2023) e regras KiCad oficiais da Aisler no GitHub `AislerHQ/aisler-support/kicad/` (2/4/6/8 camadas, último commit 2026-01-20). Para JLC/PCBWay há os repositórios comunitários `labtroll/KiCad-DesignRules` (KiCad 7) e `Cimos/kicad-druid` (KiCad 8–10). OSH Park só publica instruções manuais (FATO).
8. **Escolha rápida (INFERÊNCIA):** protótipo barato com montagem → JLCPCB (ou PCBWay); UE rápido sem alfândega → Aisler; qualidade industrial UE, painel, PCBA e IMS → Eurocircuits / Würth; RF e flex com peças especiais → PCBWay; ENIG roxo nos EUA com stackup FR408HR publicado → OSH Park; PCBA nos EUA com upload do `.kicad_pcb` → MacroFab.

## Tabela comparativa

Valores do serviço **padrão/protótipo** de 2 camadas, 1 oz, salvo nota. Cada célula tem fonte na seção por fabricante abaixo. "n.e." = não encontrado.

| Fabricante (país) | Trilha/espaço mín. | Furo mín. / anel | Cobre-borda | Silk mín. (traço × altura) | Camadas | Impedância | PCBA | Arquivos | Prazo típico (fabricação) | UE (Irlanda) |
|---|---|---|---|---|---|---|---|---|---|---|
| **JLCPCB** (CN) | 0,10/0,10 mm (2L); 0,09/0,09 (4L+) | via 0,15/0,25 mm (furo/pad); furo preferido ≥ 0,2 | 0,2 fresado / 0,4 V-cut | 0,15 × 1,0 mm | até 32 | 4–32 camadas, ±10 % | Sim, biblioteca própria (LCSC Basic/Extended), global sourcing, consignado; 2 faces só no Standard | Gerber RS-274X + Excellon (ODB++ não confirmado) | 2L: 24 h; 4L: 2–5 d; PCBA +24–48 h | IOSS (≤150 € B2C) + DDP opcional; €3/linha + €2 UHF |
| **PCBWay** (CN) | 0,1 mm / 4 mil | 0,15 mm (CNC) / 0,15 mm | 0,25 mm (avançado, normal) | 0,15 × 0,8 mm (1:5) | 1–14 (padrão); até 24+ (avançado) | ±10 % (±5 Ω ≤ 50 Ω); camada mínima n.e. | Sim; consignado preferido, turnkey sem markup; 1 ou 2 faces; mín. 10×10 mm | Gerber RS-274X; ODB++ só no visualizador (pedido n.e.) | "24 h" (promo); PCBA 24 h a semanas | IOSS desde 2021 (≤150 €); política pós-07/2026 n.e. |
| **NextPCB** (CN) | 3/3 mil (0,08 mm) ext. 1 oz | 0,15 mm (placa ≤ 1,2 mm) / 3,5 mil (0,09) | 0,2 fresado / 0,4 V-cut | 5 mil × 30 mil (0,12 × 0,76 mm) | 1–32 | 4–20 camadas, ±10 % | Sim; BOM com MPN; coluna "Customer Supply" | Gerber RS-274X/X2 + Excellon | "24 h" (promo) | IOSS só B2C ≤150 €; €3/linha cobrado pela transportadora |
| **Seeed Fusion** (CN) | 4/4 mil (1 oz) | 0,2 mm / n.e. | 0,3 mm | n.e. | 2, 4 (padrão); mais no Advanced | n.e. | Sim; OPL (biblioteca própria) + compra por MPN; 1 ou 2 faces; mín. 1 pç; placa ≥ 10×10 mm | Gerber RS-274X + Excellon, zip/rar ≤ 20 MB | "a partir de 24 h"; PCBA com OPL ~7–15 d.ú. (fonte antiga) | n.e. |
| **ALLPCB** (CN) | 4/4 mil (0,1 mm) | 0,2 mm / 0,153 mm | 0,3 mm / 0,4 V-cut | 0,15 × 0,8 mm | 1–14 (padrão); até 32 | opção na linha avançada; tolerância n.e. | Sim; turnkey ou consignado; placa ≥ 50×50 mm (senão paineliza); 2 faces | Gerber RS-274X/X2, zip/rar < 10 MB | "from 24 hours"; PCBA proto 1–2 d | impostos por conta do cliente; "DDP" citado sem países |
| **Elecrow** (CN) | 6/6 mil (0,15 mm) | 0,3 mm / 0,15 mm (FATO-sec) | n.e. | 0,15 × 0,8 mm | 1–8 | n.e. (contatar) | Sim; consignado, turnkey (Digikey/Mouser/TME) ou combo; 2 faces | Gerber RS-274X | PCB n.e.; PCBA ~3 semanas | DAP (comprador é o importador) |
| **OSH Park** (EUA) | 6/6 mil (0,152 mm) | 10 mil (0,254 mm) / 5 mil (0,127) | 15 mil (0,381 mm) | 5 mil (3 mil em textos curtos); altura n.e. | 2, 4, 6 | stackup 4L FR408HR publicado (Dk 3,61); tabela em imagem | **Não** (só placa nua) | **`.kicad_pcb` nativo**, Gerber | 2L: envia em 9–12 dias corridos; Super Swift 4–5 d.ú. | Frete grátis sem rastreio (2–4 sem.); IVA/IOSS n.e. |
| **Aisler** (DE) | 0,20/0,15 mm (2L HASL 35 µm); 0,125/0,125 (ENIG) | via 0,30 mm (HASL) ou 0,25 (ENIG) / 0,175–0,20 mm | 0,30 mm | 0,15 × 0,8 mm | 2, 4, 6, 8 | stackup "variável" (sem Dk); impedância n.e. | Sim ("Amazing Assembly"); global sourcing; peça do cliente €15 por peça; 2 faces; até 0201; 1 pç | **`.kicad_pcb` nativo**, ODB++, Gerber; plugin Push | Blitz 2L HASL ≥ 2 d.ú.; PCBA 6–9 d.ú. | **Dentro da UE**: sem alfândega; frete padrão grátis |
| **Eurocircuits** (BE) | PCB proto: 0,150/0,150 mm (classe 6); pools até 0,090 (classe 9) | proto: PTH acabado 0,25 mm, pad = furo + 0,35 (anel 0,175) | 0,25 externo / 0,40 interno | 0,10 × 1,0 mm (página de legenda) vs. 0,17 mm (Marking Editor): conflito | proto 2/4; pool de impedância 4/6/8 | pool DEFINED IMPEDANCE 4/6/8 camadas IS400; ±10 % só em snippet | Sim, só em placas Eurocircuits; compra tudo por padrão, cliente supre o que faltar; 2 faces; 5×5 a 340×440 mm; borda ≥ 5 mm | **KiCad nativo**, Eagle, Gerber X3/X2/X, ODB++; Excellon/XNC (IPC-2581 não listado) | proto 2–3 d.ú.; impedância 5 d.ú.; PCBA +3/5/7/10 d.ú. | **Dentro da UE**; com VAT number: reverse charge |
| **Multi-CB** (DE) | 0,10/0,10 mm (sem custo extra); 0,075 (especial) | 0,20 mm / 0,10 mm (via-pad 0,4) | 0,20 fresado / 0,50 scoring | 150 µm a 1,2 mm de altura (outra página: 100 µm): conflito | 1–48 | ±10 % ou ±5 % com buildup próprio; buildup grátis sem impedância | **Não** (só placa e stencil) | **KiCad nativo**, Eagle, Altium etc.; ODB++ e Gerber estendido preferidos; IPC-2581 aceito | expresso "from 1 WD"; padrão 4 d.ú. | Dentro da UE; **vende só a empresas** (preço sem IVA) |
| **Würth WEdirekt** (DE) | 0,10/0,10 mm (35 µm); 0,085 (18 µm) | via ≥ 0,25 mm com pad ≥ 0,60; pad = furo + 0,35 | 0,25 fresado / 0,50 V-score | **0,08 × 1,50 mm** | 1–8 pool; até 16 non-pool | sem tolerância; se o pool não atinge, usa stackup padrão sem avisar | **Não** no WEdirekt | Gerber 274X, ODB++ v8, Excellon; KiCad/IPC-2581 não listados | expresso "from 72 hours"; rígida "from 5 working days" | Dentro da UE (Irlanda sob termos da Würth UK); VAT ID para isenção intra-UE |
| **MacroFab** (EUA) | 5/5 mil padrão; 3/3 mil "Extended" | 10 mil padrão / 4 mil; 4/3 mil Extended | 10 mil padrão; 3 mil Extended | 5 mil × 32 mil | 2–36 | "offered", sem valores | **Foco é PCBA**; 2 faces por padrão; House Parts + turnkey + consignado | **`.kicad_pcb` nativo**; Gerber; XYRS | opção de 10 dias (anúncio antigo) | n.e.; IVA 23 % (FATO, revenue.ie) + desembaraço (INFERÊNCIA) |

**Preço do protótipo (5 placas, 2 camadas, 100×100 mm)**

| Fabricante | Valor | Etiqueta |
|---|---|---|
| JLCPCB | "a partir de US$ 2 / 5 pç"; a cobertura de 100×100 mm não foi verificada; reajuste de preço anunciado em 03/08/2026 sem números | FATO (anúncio) / NÃO VERIFICADO (tamanho), ver `06` regra 33 |
| PCBWay | "$ 5.00 10 pcs 1-2 layer Build Time: 24 hours"; o tamanho coberto não aparece | FATO (home) / tamanho n.e. |
| Aisler | 2L 1,6 mm HASL Budget: 12,00 € + 100 cm² × 0,067 €/cm² × **6** pç (múltiplos de 3) = **52,20 € líquido**; Blitz: 22 + 100 × 0,129 × 6 = **99,40 €**. Tabela de 2023, que diverge do exemplo da própria página | Fórmula e taxas FATO; conta INFERÊNCIA |
| OSH Park | US$ 5/pol² por conjunto de 3; 100×100 mm = 15,5 pol² → US$ 77,50 por 3; 5 placas exigem **6** = **US$ 155** | Taxa FATO; conta INFERÊNCIA |
| NextPCB, Seeed, ALLPCB, Elecrow, MacroFab | cotador dinâmico; preço fixo não publicado | não encontrado |
| Eurocircuits, Würth | calculador online; preço fixo não publicado | não encontrado |
| Multi-CB | 1 pç 80×100 mm 2L HAL: €35,00 (4 d.ú.) ou €14,80 (8 d.ú.), sem IVA; caso 5 pç 100×100 não encontrado | FATO via agente (<https://www.multi-circuit-boards.eu/en/support/faq.html>) |

## Fichas por fabricante

### JLCPCB (comparação; detalhes em `09` R1 e `06` §E)
- Mínimos 2L 0,10/0,10 mm, 4L 0,09/0,09 mm; via 0,15/0,25 mm; cobre-borda 0,2 mm fresado e 0,4 mm V-cut; silk 0,15 mm × 1,0 mm (1:6); até 32 camadas; alumínio e cobre (1 camada), Rogers/PTFE (2 camadas) e flex em página própria; rigid-flex não aparece. FATO: <https://jlcpcb.com/capabilities/pcb-capabilities>.
- Impedância 4–32 camadas, ±10 %; stackups publicados: <https://jlcpcb.com/help/article/multi-layer-pcb-standard-laminated-structures>. FATO-sec (em `09`).
- PCBA: corpo do componente **≥ 2,5 mm** da borda; trilhos ≥ 3 mm (5 mm para SMT); fiducial de 1 mm; Economic só uma face, passivo ≥ 0402. FATO/FATO-sec (em `06` regras 17, 23, 24 e `09` R1.7).
- Arquivos: Gerber RS-274X + Excellon. ODB++: só há uma pergunta de cliente sem resposta em <https://jlc3dp.com/help/answers/detail/197-Can-ODB++-files-be-used-to-order> (FATO); aceitação **não confirmada**.
- UE: ver "Envio para a UE" abaixo.

### PCBWay (China)
- **PCB padrão** (<https://www.pcbway.com/capabilities.html>, FATO): 1–14 camadas; trilha/espaço 0,1 mm / 4 mil; furo CNC 0,15 mm; anel 0,15 mm (6 mil); silk 0,15 mm de traço e 0,8 mm de altura (1:5); espessura 0,2–3,2 mm; acabamentos HASL (com e sem chumbo), immersion gold, OSP, hard gold, immersion silver, immersion tin, ENEPIG; impedância ±10 % e ±5 Ω para ≤ 50 Ω (camada mínima **não declarada**). Avançado: cobre-borda fresado 0,25 mm (normal), 0,20 (média dificuldade); até 24+ camadas.
- **Flex/rigid-flex** (<https://pcbway.com/FPC-Rigid-Flex-PCB.html>, FATO): 1–12 camadas (padrão), até 26 (avançado); 2/2 mil; furo 0,10 mm; impedância < 50 Ω ±5 Ω, ≥ 50 Ω ±10 %; rigid-flex 0,25–6,0 mm.
- **PCBA** (<https://www.pcbway.com/assembly-capabilities.html>, FATO): placa 10×10 a 250×500 mm (menor que isso, painel); até 01005; pitch fino 0,25 mm; BGA 0,3 mm (rígida); uma ou duas faces; **mínimo 5 pç**; prazo "24 Hours to a few weeks", contado só quando peças e arquivos estão completos; consignado (preferido), turnkey ("We do not mark up on the parts cost") e parcial. Placa não retangular vai em painel com trilhos nas duas bordas longas.
- **Painel para montagem** (<https://www.pcbway.com/pcb_prototype/Panel_Requirements_for_Assembly.html>, FATO): 3 fiduciais de 1,0 mm com abertura de máscara de 1,7 mm, no meio dos trilhos; 4 furos de ferramenta; painel 50×50 a 330×530 mm; V-score com espaço 0 ou 3 mm, contínuo; tab-route com espaço 1,6 mm, furos ≥ 0,45 mm (normal 0,55–0,6), 5–6 furos por aba, aba sólida ≥ 2 mm. Largura do trilho e distância componente-borda: **não declaradas**. Guia de design da PCBWay: fiducial ≥ 5 mm da borda (FATO-sec, <https://pcbway.com/helpcenter/design_instruction/PCB_Panelization__Breakaway_Rails__Fiducial_Marks__Tooling_Holes.html>).
- **Arquivos** (<https://www.pcbway.com/assembly-file-requirements.html>, FATO): Gerber RS-274X; BOM em xls/xlsx/csv; centroid só SMD. ODB++: aparece no visualizador <https://www.pcbway.com/tool/ElectronicDesignViewer> (FATO-sec), aceitação em pedido **não encontrada**.
- **Preço/prazo**: "$ 5.00 10 pcs 1-2 layer Build Time: 24 hours"; PCBA "$ 29 free shipping for 1-20pcs assembly" (FATO: <https://www.pcbway.com/>).
- **DRU oficial**: `KiCAD_Custom_DRC_Rules_for_PCBWay.zip` (arquivo de 15/09/2023; página atualizada em 29/05/2024; versão do KiCad e valores não declarados) — FATO: <https://www.pcbway.com/helpcenter/design_instruction/PCBWay_Custom_Design_Rules.html>.
- **UE**: IOSS para B2C ≤ 150 € desde 01/07/2021 (FATO: <https://www.pcbway.com/blog/help_center/EU_e_commerce_adjustment_on_IMPORT_ONE_STOP_SHOP__IOSS_.html>). Política após a reforma de 07/2026: **não encontrada**.

### NextPCB (China, grupo Huaqiu)
- **PCB padrão** (<https://www.nextpcb.com/pcb-capabilities>, FATO): 1–32 camadas; trilha/espaço externo 1 oz 3/3 mil (0,08 mm), interno 0,5 oz 2,5/3 mil, externo 2 oz 5,5/5,5 mil; furo mecânico 0,15 mm (só placa ≤ 1,2 mm), PTH ≥ 0,2 mm; anel 3,5 mil (1 oz) / 4,5 mil (2 oz); cobre-borda ≥ 0,2 mm (fresado) e ≥ 0,4 mm (V-cut); silk 5 mil × 30 mil (serigrafia) ou 3 × 24 mil (impressora); espessuras 0,6–3,2 mm; **impedância de 4 a 20 camadas, ±10 %**; placa mínima 10×10 mm. Acabamentos: a página não lista. **Atenção**: páginas de produto da NextPCB dão 3,5/3,5 mil como "finest available for standard" (FATO-sec, busca); usar 3,5 mil ou mais.
- **PCBA** (<https://support.nextpcb.com/portal/en/kb/articles/1-pcb-assembly-files-explanation>, FATO): BOM com `Manufacturer Part Number`, `Designator`, `Quantity` + coluna `Customer Supply` (Y para peça do cliente, DNP para não montar); centroid com designator, X, Y, rotação (graus, "reference only") e lado opcional (coluna ou dois arquivos); THT normalmente fora; unidade **não declarada**. Gerber RS-274X e X2 ("RS-274D is not recommended"), Excellon, tudo num zip/rar.
- **UE**: aviso de 29/06/2026 (FATO: <https://www.nextpcb.com/news/eu-customs-reform-2026>): IOSS só para B2C ≤ 150 €; €3 por linha HS cobrado pela transportadora, não pela NextPCB; empresa com VAT number entra como B2B; DDP não mencionado.
- **Plugins KiCad** no PCM oficial: `kicad-nextpcb-plugin` (envio e cotação, KiCad 7+), `kicad-hqdfm-plugin` (DFM, KiCad 9+) — FATO: <https://gitlab.com/kicad/addons/metadata/-/tree/main/packages>.

### Seeed Fusion (China)
- **PCB** (<https://wiki.seeedstudio.com/Service_for_Fusion_PCB/>, FATO): 2 e 4 camadas FR-4 no serviço padrão; 4/4 mil (1 oz), 10/10 (2 oz), 15/15 (3 oz); trilha interna 4L ≥ 6 mil; PTH 0,2–5,8 mm; castelado ≥ 0,5 mm; cobre-borda ≥ 0,3 mm; espessuras 0,6–3,0 mm; acabamentos HASL (com e sem chumbo), ENIG, OSP, hard gold; placa 10×10 a 500×500 mm; mínimo 5 pç; materiais alumínio, flex, Rogers RO4003C/RO4350B, base de cobre; rigid-flex no Advanced PCB. Anel, silk e impedância: **não declarados**. Gerber RS-274X + Excellon, zip/rar ≤ 20 MB.
- **PCBA**: mínimo 1 pç; SMT/THT, uma ou duas faces; até 0201, BGA 0,4 mm; BOM xls/xlsx/csv no template Fusion com designator, MPN **ou SKU Seeed**, quantidade; CPL com designator, X/Y, rotação, lado (FATO, mesma URL). Especificação: placa 10×10 a 500×500 mm (FATO: <https://support.seeed.cc/portal/en/kb/articles/fusion-pcba-specification>).
- **OPL (Open Parts Library)**: catálogo próprio de peças em estoque em Shenzhen; prazo ~7–15 d.ú. só com OPL contra ~20–25 d.ú. sem (FATO-sec, páginas de suporte antigas; <https://support.seeedstudio.com/knowledgebase/articles/457797-fusion-pcba-specification>). Tamanho atual do OPL: não confirmado.
- Prazo PCB: "as fast as 24 hours" (FATO: <https://www.seeedstudio.com/fusion_pcb.html>). UE: **não encontrado**.

### ALLPCB (China)
- **PCB padrão** (<https://www.allpcb.com/standard_pcb_manufacturing_capability.html>, FATO, via agente de pesquisa): 1–14 camadas; 4/4 mil (recomenda ≥ 6 mil para baixar custo); furo CNC 0,2–6,5 mm; anel ≥ 0,153 mm; cobre-contorno ≥ 0,3 mm, V-cut ≥ 0,4 mm; silk ≥ 0,15 × 0,8 mm; 0,4–3,2 mm; acabamentos HASL, imersão ouro/prata/estanho, OSP, ouro duro e mole, NiPdAu. Geral: FR4 até 32 camadas, Rogers, HDI 4–20 (<https://www.allpcb.com/pcb-capabilities.html>, FATO).
- **PCBA** (<https://www.allpcb.com/pcb_assembly_capability.html>, FATO): placa ≥ 50×50 mm (menor é painelizada), até 350×1200 mm; 01005; 2 faces; proto 1–2 dias. Pick-and-place em mm, formatos xls/xlsx/csv/txt/pos (FATO-sec: <https://www.allpcb.com/faq/372.html>). Colunas exatas: **não encontradas**.
- Arquivos: Gerber RS-274X/X2 em zip/rar < 10 MB (FATO-sec: <https://www.allpcb.com/online_pcb_quote_new.html>). Impostos "borne by customers" (FATO-sec: <https://www.allpcb.com/shipping-information.html>).

### Elecrow (China)
- **PCB** (<https://www.elecrow.com/pcb-manufacturing.html>, FATO, via agente): 1–8 camadas; 6/6 mil (recomenda ≥ 8 mil); furo 0,3 mm; espessuras 0,6–2,0 mm; silk 0,15 × 0,8 mm; castelado ≥ 0,6 mm; HASL, HASL sem chumbo, ENIG; máx. 550×550 mm. Anel 0,15 mm (FATO-sec, PDF antigo). Cobre-borda e impedância: **não encontrados**.
- **PCBA** (<https://www.elecrow.com/pcb-assembly.html>, FATO): BOM com MPN completo (ou link de compra); coordenadas com designator, X, Y, rotação, lado — nomes de coluna e unidade **não declarados**; consignado sem taxa, turnkey (Digikey, Mouser, TME, Element14) ou combo; 2 faces; "panelizes by default"; prazo geral "3 weeks".
- Envio DHL ~3–5 d.ú.; impostos não inclusos, comprador é o "importer of record" (FATO-sec: <https://www.elecrow.com/terms-and-condition>).
- KiCad: só por presets do plugin **Gerber Zipper 2** (FATO: <https://github.com/g200kg/kicad-gerberzipper2>).

### OSH Park (EUA)
- **2 camadas** (<https://docs.oshpark.com/services/two-layer/>, FATO): 6/6 mil; furo 10 mil; anel 5 mil; cobre-borda 15 mil (0,381 mm); silk 5 mil (3 mil em textos curtos); 1,6 mm; **ENIG** (IPC-4552); 1 oz; US$ 5/pol² com 3 cópias; envia em 9–12 dias corridos; fresa de contorno 1,72 mm e de recorte interno 1,01 mm.
- **4 camadas** (<https://docs.oshpark.com/services/four-layer/>, FATO): 5/5 mil; furo 10 mil; anel 4 mil; **stackup publicado**: 1 oz / prepreg FR408HR 2113 de 7,87 mil / 0,5 oz / núcleo de 39 mil / 0,5 oz / 7,87 mil / 1 oz; Dk 3,61 a 1 GHz; US$ 10/pol²; 9–14 dias. Mudança temporária de stackup citada no changelog de 28/01/2026.
- **Serviços** (<https://docs.oshpark.com/services/>, FATO): Super Swift 2L 4–5 d.ú. (US$ 10/pol²); 2 oz 0,8 mm; Flex (US$ 10/pol², **suspenso temporariamente**); After Dark; Medium Run US$ 1/pol² (mín. 100 pol²); 6 camadas US$ 15/pol² (furo 8 mil). Sem via cega/enterrada. **Montagem: não oferece** (a página não menciona).
- **KiCad** (<https://docs.oshpark.com/design-tools/kicad/>, FATO): aceita `.kicad_pcb` direto, processado com KiCad 9.x; **não re-preenche zonas** (preencher antes, tecla `b`); fontes: embutir (KiCad 9+) ou mandar Gerber. Regras DRU: só instruções manuais (<https://docs.oshpark.com/design-tools/kicad/kicad-design-rules/>, FATO via agente).
- **Envio** (<https://docs.oshpark.com/submitting-orders/shipping-information/>, FATO): International First Class grátis, sem rastreio, 2–4 semanas; UPS Express Saver ~US$ 25–40 e FedEx ~US$ 20–35 para a Europa, ~7 dias. IVA/IOSS: **não declarado**.

### Aisler (Alemanha, UE)
- **Produto** (<https://aisler.net/products/boards>, FATO): 2/4/6/8 camadas FR4; HASL e ENIG; Blitz 2L HASL a partir de 2 d.ú. de fabricação; pedidos em múltiplos de 3; "manufactured and delivered from Germany"; frete mundial grátis; teste elétrico em toda placa; ferramentas suportadas incluem KiCad.
- **Regras 2L 1,6 mm HASL 35 µm** (<https://community.aisler.net/t/2-layer-1-6mm-hasl-design-rules/3735>, FATO, atualizado em 07/07/2025): trilha 0,20 mm, espaço 0,15 mm; via 0,30 mm (máx. 0,45) com anel 0,20 mm preferido / 0,175 mm absoluto; PTH 0,5 mm com anel 0,30 mm; **cobre-borda 0,30 mm**; silk 0,15 mm × 0,8 mm; furo-furo 0,30 mm; ponte de máscara 0,10 mm; expansão de máscara 0,05 mm; slot NPTH ≥ 0,8 mm (≥ 1,8 mm preferido), slot PTH 0,7–2,6 mm.
- **Tabela por acabamento** (<https://community.aisler.net/t/pcb-design-rules/41>, FATO, post de 22/04/2026): furo HASL ≥ 0,3 mm, ENIG ≥ 0,25 mm; 35 µm HASL 200/150 µm, ENIG 125/125 µm (100/100 µm em 6L+); 70 µm HASL 225/225, ENIG 175/175; castelado só com ENIG. "If you use small drills, castellated edges or small trace width/spacing it is required to choose ENIG."
- **Stackup**: 2L 1,6 mm 35 µm é "variável" (núcleo e prepreg conforme estoque, o que muda espessura e impedância) (FATO: <https://community.aisler.net/t/2-layer-1-6mm-35-m/5571>, 25/03/2026). Impedância controlada: **não encontrada**.
- **Montagem** (<https://aisler.net/products/assembly>, FATO): dupla face, THT, SMD ou misto, até 0201; a partir de 1 pç; distribuidores globais; peça do cliente com taxa; prazo "6 business days" (Blitz) vs. "from 9 business days" na FAQ (divergência na própria página). BOM lido do projeto: campos `mpn`, `MPN`, `Mpn`, `AISLER_MPN`, senão o `Value`; "Smart Match" para R, C, LED, D (FATO: <https://community.aisler.net/t/documenting-parts/56>). Taxa de peça do cliente €15 por peça atribuída (FATO: <https://community.aisler.net/t/our-simple-pricing>).
- **Arquivos**: `.kicad_pcb` direto; **pré-release (RC/beta/alpha) falha**; fontes personalizadas não são processadas no upload direto → usar AISLER Push ou ODB++ (FATO: <https://community.aisler.net/t/known-pcb-design-tools-issues-and-limitations/2633>). Plugin `com.github.aislerhq.PushForKiCad` no PCM; KiCad 10 suportado (FATO-sec: <https://community.aisler.net/t/kicad-10-is-live-and-100-supported-by-aisler/5567>). Há também "AISLER Push for CLI" e um servidor MCP (títulos FATO em <https://community.aisler.net/c/knowledge-base/106>).
- **DRU oficial**: `AislerHQ/aisler-support/kicad/` com `aisler-2-layer-simple-drc`, `-2-layer-hd-drc`, `-4-layer-hd-drc`, `-6-layer-hd-drc`, `-8-layer-hd-drc`; último commit 2026-01-20 (FATO, API do GitHub: <https://github.com/AislerHQ/aisler-support/tree/master/kicad>). Templates antigos em <https://github.com/AislerHQ/kicad_templates> (KiCad 5, 2022).
- **Preço** (<https://community.aisler.net/t/our-simple-pricing>, FATO, post de 27/08/2023): preço = Job Fee + área × taxa × quantidade; líquido de IVA ("add respective attributable VAT where required (i.e. if you are a consumer)"). 2L HASL Budget 12 €/0,067 €/cm²; Blitz 22 €/0,129; 2L ENIG Budget 12 €/0,097; 4L ENIG Budget 14 €/0,13. O exemplo da própria página usa 0,051 €/cm², que não bate com a tabela → **usar o calculador ao vivo**. Página de produto: "starts at €14.20".
- **Envio UE** (<https://community.aisler.net/t/shipping-methods/672>, FATO): padrão grátis (Deutsche Post Großbrief / DHL Warenpost, sem rastreio, 4–14 d.ú.); pagos: DHL Parcel 2–10, UPS Standard 2–7, Expedited 2–5, Express 1–5 d.ú.

### Eurocircuits (Bélgica, UE)
- **Classes** (tabela oficial, versão 07/05/2024, lida da imagem <https://www.eurocircuits.com/content/uploads/2025/04/EC-classification-ENGLISH-5-2024-V3.png>, linkada em <https://www.eurocircuits.com/technical-guidelines/pcb-design-guidelines/classification/>; FATO via agente):
  - Classe de padrão (trilha = espaço externo, mm): 3 = 0,250; 4 = 0,200; 5 = 0,175; **6 = 0,150**; 7 = 0,125; 8 = 0,100; 9 = 0,090. Anel externo: 0,200 / 0,150 / 0,150 / 0,125 / 0,125 / 0,100 / 0,100. Classes 3–6 em todos os serviços; 7 em STANDARD pool, DEFINED IMPEDANCE, RF e SEMI-FLEX; 8–9 em STANDARD, DZ e RF.
  - Classe de furo (PTH acabado / ferramenta mínima, mm): A 0,50/0,60; B 0,35/0,45; C 0,25/0,35; D 0,15/0,25; E 0,10/0,20. Ferramenta = furo acabado + 0,10 mm (PTH). Aspecto 1:8. Espessura máxima: A/B 3,2; C 2,4; D 2,0; E 1,6 mm.
  - INFERÊNCIA: o pool IMS (alumínio) não aparece nas classes 7–9 nem nos furos B–E, logo fica limitado a classe ≤ 6 e furo A.
- **PCB proto** (<https://www.eurocircuits.com/services/pcb-proto/>, FATO via agente): 2 ou 4 camadas, 1,55 mm, FR-4, 18 µm externo / 35 µm interno; ENIG ou HAL (escolha da Eurocircuits); 0,150/0,150 mm; PTH acabado 0,250, NPTH 0,350; pad = furo + 0,350; cobre-borda 0,250 externo / 0,400 interno; placa 20×20 a 580×425 mm; 1–5 pç; **2 ou 3 dias úteis**; IPC classe 2.
- **Silk**: 0,10 mm de traço e 1,00 mm de altura (FATO-sec: <https://www.eurocircuits.com/technical-guidelines/pcb-design-guidelines/legend-print/>), mas o guia do Marking Editor diz que 0,17 mm é a linha mais fina imprimível: **conflito**. Usar ≥ 0,17 mm (INFERÊNCIA).
- **Impedância** (<https://www.eurocircuits.com/services/defined-impedance-pool/>, FATO via agente): 4/6/8 camadas Isola IS400; 1,55 mm (1,00 mm em 4L); 0,100 mm em pool; 5 d.ú. nua, 10 d.ú. montada; ~800 stackups pré-definidos no editor online (sem PDF). Tolerância ±10 %: só em snippet (NÃO VERIFICADO).
- **PCBA** (<https://www.eurocircuits.com/pcba-capabilities/>, FATO via agente): placa 5×5 a 340×440 mm; **"Minimum 5mm border and 2mm breakrouting"**; uma ou duas faces, SMT/THT; 0201, QFP 0,35 mm, BGA 0,35/0,40 mm; a Eurocircuits compra tudo por padrão e o cliente fornece o que ela não achar (biblioteca própria não mencionada); 3/5/7/10 d.ú. após a placa; **"Only assembly of boards produced by Eurocircuits"**.
- **BOM/CPL** (<https://www.eurocircuits.com/user-guides/visualizer-user-guides/upload-cpl-data-user-guide/>, FATO via agente): CPL com refdes, rotação, lado "Top or Bottom", X/Y do centro; Excel ou CSV (vírgula ou tab), cabeçalho na 1ª linha; nomes exatos de coluna, unidade e origem **não encontrados** (os exemplos são imagens). BOM com Description, MPN e SPN (código do fornecedor); o BOM não é lido do CAD nativo, mas o CPL é extraído do `.kicad_pcb` (<https://www.eurocircuits.com/blog/kicad-eurocircuits-reads-in-native-kicad-data/>).
- **Arquivos** (<https://www.eurocircuits.com/technical-guidelines/pcb-design-guidelines/input-data-formats/>, FATO via agente): Eagle BRD e **KiCad nativo**; Gerber X3, X2, X (RS-274X); ODB++; furação XNC, Excellon 1/2, Sieb&Meyer. IPC-2581 não listado.
- **IVA/frete** (FATO-sec: <https://www.eurocircuits.com/user-guides/customer-account-user-guide/finance-and-administration/value-added-tax-vat/>): com VAT number válido, reverse charge (sem IVA) só se a entrega for no país do VAT number; senão, IVA do destino. Courier expresso como padrão; preço para a Irlanda não encontrado.
- **KiCad**: upload nativo + PCB Visualizer / PCB Checker / Assembly Checker online; plugin oficial ou `.kicad_dru`: **não encontrado**.
- **Pontos fortes** (INFERÊNCIA): fabricação na UE, pools especializados (IMS, RF, semi-flex, impedância definida, BINDI), DFM online grátis, placa e montagem no mesmo lugar.

### Multi-CB e Würth Elektronik WEdirekt (Alemanha, UE)
**Multi-CB** (FATO via agente)
- Parâmetros (<https://www.multi-circuit-boards.eu/en/pcb-design-aid/design-parameters.html>, "exemplary for 35µm"): padrão 100/100 µm, furo de via 200 µm, anel 100 µm, aspecto 1:10; produção especial 75/75 µm, furo 150, anel 75; cobre-borda 200 µm (fresa) e 500 µm (scoring); ponte de máscara 100 µm; 1–48 camadas.
- Página KiCad (<https://www.multi-circuit-boards.eu/en/support/pcb-data/kicad.html>): sem custo extra com trilha/espaço 0,1 mm, anel 0,1 mm, furo 0,2 mm, via-pad 0,4 mm; aceita `.kicad_pcb` nativo (eles geram os Gerbers); guia "Getting Started in KiCad 9" em PDF (<https://www.multi-circuit-boards.eu/fileadmin/pdf/kicad/getting_started_in_kicad-9_en_www.multi-circuit-boards.eu.pdf>). `.kicad_dru`: **não encontrado** (regras digitadas no Board Setup).
- Protótipos (<https://www.multi-circuit-boards.eu/en/products/printed-circuit-boards/prototypes.html>): FR4 1,55 mm, 35 µm; HAL sem chumbo em 2/4L, ENIG em 6–10L; preço online para 1–10 camadas.
- Silk: altura de 1,2 mm com traço de 150 µm (FATO-sec, página de legenda) vs. 100 µm no PDF de regras básicas: conflito.
- Impedância: ±10 % ou ±5 % sob pedido, com buildup próprio; o buildup grátis "does not yet include impedance control" (FATO-sec). PDF de stackups com exemplos de 50/90/100 Ω: <https://www.multi-circuit-boards.eu/fileadmin/pdf/leiterplatten_lagenaufbau/Multi-CB_Definierter_Lagenaufbau_Impedanzen_en.pdf> (não aberto).
- **Não monta**: "Multi-CB provides the PCBs - an assembler takes over the procurement and soldering" (<https://www.multi-circuit-boards.eu/en/pcb-assembly.html>); faz stencil.
- Arquivos (<https://www.multi-circuit-boards.eu/en/support/faq.html>): prefere ODB++ e Gerber estendido; importa EAGLE, KiCad, Altium, OrCAD, Target, Sprint; IPC-2581 aceito (<https://www.multi-circuit-boards.eu/en/support/pcb-data/ipc-2581.html>).
- Prazo: expresso "from 1 WD"; padrão 4 d.ú.; pedido antes das 9:00 conta o dia. **Vende só a empresas e instituições públicas**, com preços sem IVA, então não serve para pessoa física.

**Würth Elektronik WEdirekt** (FATO via agente)
- Diretrizes (<https://www.wedirekt.com/en/content/technology/pcbs>): trilha externa ≥ 85 µm (18 µm Cu), ≥ 100 µm (35 µm), ≥ 150 µm (70 µm, espaço 192 µm); pad = furo acabado + 0,35 mm; cobre-borda 0,25 mm (fresado) e 0,50 mm (V-score, 1,55 mm); **silk com traço ≥ 80 µm e altura ≥ 1,50 mm**, ≥ 100 µm da abertura de máscara; ENIG, HAL sem chumbo, estanho químico, ouro duro; placa máx. 426×271 mm; impedância sem tolerância, e se o pool não atingir, a placa sai no stackup padrão **sem consulta**; stackup não escolhível na loja.
- Capacidades (<https://www.wedirekt.com/fr/content/technology/wedirekt-technical-capabilities>): rígida 1–8 camadas (pool), até 16 (non-pool); 0,50–2,40 mm; vias ≥ 0,25 mm com pad ≥ 0,60 (ou ≥ 0,10 com pad ≥ 0,45); HDI 4–8L, flex e rigid-flex; IPC-A-600 classe 2.
- Arquivos (<https://www.wedirekt.com/en/content/technology/data-formats>): Gerber 274/274X, ODB++ v8, Excellon/Sieb&Meyer, Altium ≤ 23.7, Target 3001; KiCad, Eagle e IPC-2581 **não listados**.
- Sem montagem no WEdirekt (só placas e stencils, <https://www.wedirekt.com/en/>). Prazo "Express deliveries from 72 hours", rígida "From 5 working days" (a FAQ sugere uma opção de 2 d.ú.: conflito). Irlanda sob os termos da Würth Electronics UK (FATO-sec); VAT ID para entrega intra-UE isenta. Plugin KiCad e DRU: não encontrados.

### MacroFab (EUA/México, PCBA)
- **Capacidades** (<https://www.macrofab.com/pcb-assembly/capabilities>, FATO, via agente): 2–36 camadas; 3/3 mil; furo 4 mil; anel 3 mil; cobre-borda 3 mil; silk 5 mil × 32 mil; 1,6 mm padrão (0,2–6,3 mm); ENIG padrão, ENIPIG, HASL, EHG; impedância "offered"; máx. 14,9×14,9 pol. **Atenção**: os valores de 3–4 mil são provavelmente o nível "Extended" (taxa por pedido); o padrão publicado em 2018 é 5/5 mil, anel 4 mil, borda 10 mil, furo 10 mil (FATO: <https://www.macrofab.com/blog/new-standard-drc-specifications-prototype-pcbs-with-smaller-features>).
- **PCBA**: 2 faces por padrão; turnkey, estoque do cliente, consignado; "House Part List" própria (FATO: <https://github.com/MacroFab/EDALibraries>).
- **Arquivos**: importa `.kicad_pcb` direto e recomenda esse caminho (KiCad 8 e anteriores citados; preencher zonas antes) (FATO: <https://macrofab.com/blog/improved-kicad>). Formato XYRS na seção de formatos.
- Ferramentas de terceiros: `snhobbs/kicad-xyrs` e `aqsnyder/kicad-fab-package` (KiCad 10) (FATO: <https://github.com/topics/macrofab>). Nenhuma oficial.
- Envio à UE: **não encontrado**.

### Envio para a UE (Irlanda): regras de 2026
- **01/07/2026**: fim da isenção de imposto de importação para remessas ≤ 150 €. B2C ≤ 150 €: **€3,00 por linha declarada** ("temporary customs duty"); B2C > 150 € e todo B2B: tarifa normal com despacho formal. O IOSS cobre **só o IVA**. Com DDP, a JLC calcula e cobra IVA, imposto temporário e taxa de adiantamento na compra. Taxa de adiantamento (disbursement): exemplo DHL Alemanha 2 %, mínimo 15 €. **Union Handling Fee de €2 por linha** a partir de 01/11/2026, não pagável por IOSS. Devolução do imposto temporário em B2C ≤ 150 €: em geral não reembolsável. FATO: <https://jlcpcb.com/help/article/eu-customs-reform-faq> (atualizado em 28/10/2026).
- NextPCB confirma: €3 por linha HS até 01/07/2028; imposto cobrado pela transportadora/correio, não pelo fabricante; VAT number no checkout = B2B (FATO: <https://www.nextpcb.com/news/eu-customs-reform-2026>).
- **IVA irlandês padrão de 23 %**, em vigor desde 01/01/2026 (FATO: <https://www.revenue.ie/en/vat/vat-rates/search-vat-rates/current-vat-rates.aspx>).
- **Consequência prática** (INFERÊNCIA): um pedido PCB + PCBA + stencil da China pode ter 3+ linhas HS (≈ 9 € + 6 € UHF) além do IVA; juntar pedidos num envio reduz o custo; para a Irlanda, fabricar na UE elimina esse custo e o atraso de desembaraço.

## Formatos de BOM e CPL por fabricante (cabeçalhos exatos)

| Fabricante | BOM (cabeçalho) | CPL / posição (cabeçalho) | Unidade / rotação / lado | Fonte e etiqueta |
|---|---|---|---|---|
| **JLCPCB** (guia oficial) | `Comment, Designator, Footprint, LCSC PN` (rótulo do código varia: "JLCPCB Part #", "LCSC Part #"; o importador deixa mapear) | `Designator, Mid X, Mid Y, Layer, Rotation` | mm; graus, positivo = anti-horário; Layer `T/B` ou `Top/Bottom`; topo e fundo no mesmo arquivo; ≤ 200 designators por linha; 0° da JLC = orientação na fita | FATO, `09` R1 (<https://jlcpcb.com/help/article/how-to-generate-bom-and-centroid-files-from-kicad-8>, <https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly>) |
| JLC via **KiKit** | `Comment, Designator, Footprint, LCSC` | `Designator, Mid X, Mid Y, Layer, Rotation` | correção `JLCPCB_CORRECTION = X;Y;Rot` (mm, graus anti-horário, eixo do footprint) | FATO: <https://raw.githubusercontent.com/yaqwsx/KiKit/master/kikit/fab/jlcpcb.py>, `common.py` |
| JLC via **Fabrication Toolkit** | `Designator, Footprint, Quantity, Value, LCSC Part #` | `Designator, Mid X, Mid Y, Rotation, Layer` | `FT Rotation Offset`, `FT Position Offset` ("x,y"), `FT Layer Override` | FATO: <https://raw.githubusercontent.com/bennymeg/Fabrication-Toolkit/master/plugins/process.py> |
| JLC via **kicad-jlcpcb-tools** | `Comment, Designator, Footprint, LCSC, Quantity` (+ `Manufacturer, MPN` opcionais) | `Designator, Val, Package, Mid X, Mid Y, Rotation, Layer` | gerenciador de rotação próprio | FATO: <https://raw.githubusercontent.com/Bouni/kicad-jlcpcb-tools/main/bom_csv.py>, `fabrication.py` |
| **PCBWay** (oficial) | consignado: `Line#, Quantity Per Part Number, Reference Designator, Part Number, Part Description, Package, Type`; turnkey acrescenta `Manufacturers Name, Manufacturers Part Number, Distributors Part Number` (nomes como estão na página; o template `Sample_BOM_PCBWay.xlsx` não foi aberto) | designator, X, Y, rotação, lado (Top/Bottom); só SMD; cabeçalho exato **não declarado** (exemplo `a-sample-of-PCBWay-Centroid-File.txt` não aberto) | unidade, rotação e origem **não declaradas** | FATO: <https://www.pcbway.com/assembly-file-requirements.html> |
| PCBWay via **KiKit** | `Item #, Designator, Qty, Manufacturer, Mfg Part #, Description / Value, Footprint, Type, Your Instructions / Notes` | mesmo cabeçalho comum do KiKit (INFERÊNCIA) | campos `Manufacturer`, `PartNumber` obrigatórios; `PCBWAY_CORRECTION` | FATO: <https://raw.githubusercontent.com/yaqwsx/KiKit/master/kikit/fab/pcbway.py> |
| **NextPCB** | `Manufacturer Part Number`, `Designator`, `Quantity` + `Customer Supply` (Y/DNP) | Designator, X, Y, Rotation, Side (opcional) — nomes descritos, não cabeçalho literal | rotação em graus, "reference only"; unidade não declarada; `.pos` do KiCad aceito | FATO: <https://support.nextpcb.com/portal/en/kb/articles/1-pcb-assembly-files-explanation> |
| **Seeed Fusion** | template Fusion: designator, MPN **ou SKU Seeed**, quantidade, link opcional | designator, X/Y, rotação, lado | não declarados | FATO: <https://wiki.seeedstudio.com/Service_for_Fusion_PCB/> |
| **ALLPCB** | quantidade, designators, fabricante, MPN | X/Y, rotação, designator | **mm**; formatos xls/xlsx/csv/txt/pos | FATO-sec: <https://www.allpcb.com/faq/372.html> |
| **Elecrow** | template próprio; MPN completo ou link | designator, X, Y, rotação, lado | não declarados | FATO: <https://www.elecrow.com/pcb-assembly.html> |
| **Aisler** | **sem arquivo**: BOM extraído do projeto/ODB++ pelos campos `mpn`/`MPN`/`Mpn`/`AISLER_MPN` | sem arquivo (extraído do projeto) | — | FATO: <https://community.aisler.net/t/documenting-parts/56> |
| **MacroFab** | arquivo único `.XYRS`, separado por **tabulação**: `Part, X, Y, Rotation, Side, Type, XSize, YSize, Value, Footprint, Populate, MPN`; linhas com `#` ignoradas | (mesmo arquivo) | X, Y e tamanhos em **mils**; graus; Side `1/T/top` ou `2/B/bot/bottom`; Type `1/SMT/SMD` ou `2` (PTH) | FATO-sec (artigos de ajuda <https://help.macrofab.com/knowledge/macrofab-required-design-files>; certificado do site falhou) |
| **OSH Park** | não monta | — | — | FATO |
| **Eurocircuits** | Description, MPN, SPN (código do fornecedor); não lido do CAD | refdes, rotação, lado `Top`/`Bottom`, X/Y do centro; CSV/Excel com cabeçalho; nomes exatos n.e.; extraível do `.kicad_pcb` | n.e. | FATO via agente (<https://www.eurocircuits.com/user-guides/visualizer-user-guides/upload-cpl-data-user-guide/>) |
| **Multi-CB, Würth WEdirekt** | não montam | — | — | FATO |

**Notas transversais**
- `kicad-cli pcb export pos` gera `Ref, Val, Package, PosX, PosY, Rot, Side`; basta renomear para o formato JLC (FATO, `09` R1.5).
- Para NeoDen YY1: `kikit fab neodenyy1` gera `top_pos.csv` e `bottom_pos.csv`, origem obrigatória no canto inferior esquerdo da borda (FATO: <https://yaqwsx.github.io/KiKit/latest/fabrication/neodenyy1/>).
- Origem das coordenadas: só a JLC (via guia KiCad) e o NeoDen documentam; nos demais **não declarada**. INFERÊNCIA: usar a origem do arquivo de furação/auxiliar (Drill/Place origin) no canto inferior esquerdo da placa e declarar isso no pedido.

## Como escrever um projeto agnóstico de fabricante

### 1. Projetar pelo mínimo comum (2 camadas, serviço padrão)
Regra: escolher o valor **mais folgado** entre os mínimos publicados dos fabricantes que você talvez use. Tabela a partir dos números FATO acima (a coluna "agnóstico" é INFERÊNCIA):

| Parâmetro | Mais apertado publicado | Mais folgado publicado | **Agnóstico recomendado** | Quem dita |
|---|---|---|---|---|
| Trilha | 0,08 mm (NextPCB) | 0,20 mm (Aisler HASL 35 µm) | **0,20 mm** (0,15 mm se excluir Aisler HASL e Elecrow) | Aisler HASL |
| Espaço | 0,08 mm (NextPCB) | 0,15 mm (Elecrow, OSH 0,152, Aisler HASL) | **0,20 mm** (folga sobre 0,15) | Elecrow / OSH Park |
| Furo de via | 0,15 mm (JLC, PCBWay) | 0,30 mm (Aisler HASL, Elecrow) | **0,30 mm** | Aisler HASL / Elecrow |
| Anel de via | 0,09 mm (NextPCB) | 0,20 mm (Aisler preferido) | **0,20 mm → pad 0,70 mm** | Aisler |
| Furo PTH (pino) | — | 0,5 mm com anel 0,30 mm (Aisler) | **anel ≥ 0,30 mm** | Aisler |
| Cobre-borda (fresado) | 0,2 mm (JLC, NextPCB, Multi-CB) | 0,40 mm (Eurocircuits, camada interna); 0,381 (OSH Park) | **0,40 mm** (0,50 mm se houver V-cut: Würth e Multi-CB pedem 0,50) | Eurocircuits / OSH Park / Würth |
| Silk traço × altura | 0,08 mm (Würth) / 0,76 mm (NextPCB) | 0,17 mm (Eurocircuits, Marking Editor) / 1,50 mm (Würth) | **0,17 × 1,0 mm**; **1,5 mm** de altura se a Würth estiver no páreo | JLC / Eurocircuits / Würth |
| Ponte de máscara | 0,10 mm | 0,13 mm (JLC preto/branco, Seeed outras cores) | **0,13 mm** se cor ≠ verde | JLC / Seeed |
| Slot NPTH | 0,8 mm (Aisler) | 1,0 mm (JLC) | **1,0 mm** | JLC |
| Espessura | — | — | **1,6 mm** (todos oferecem; OSH e Aisler têm 1,6 como padrão) | consenso |
| Acabamento | — | — | **ENIG** se passo ≤ 0,5 mm ou se quiser Aisler com regras finas; OSH Park só faz ENIG | JLC blog / Aisler / OSH |

- 4 camadas: OSH Park 5/5 mil, furo 10 mil, anel 4 mil; Aisler 4L só ENIG (FATO). Agnóstico 4L (INFERÊNCIA): **0,15/0,15 mm, via 0,30/0,70 mm** (no mínimo 0,65 mm: Eurocircuits e Würth pedem pad = furo + 0,35 mm), cobre-borda 0,40 mm.
- Montagem (PCBA): **corpo do componente ≥ 2,5 mm da borda** (JLC, o único que publica) e fiduciais de 1 mm com abertura de 1,7–2 mm (PCBWay 1,7 mm) ≥ 5 mm da borda do painel (PCBWay). Se precisar de conector rente à borda, prever **trilho/borda de processo** de ≥ 5 mm (JLC) — INFERÊNCIA consolidada de `06` regras 17, 23 e 24 e da PCBWay.
- Impedância controlada **não é portátil**: cada fabricante tem stackup próprio (JLC e OSH Park publicam; Aisler diz "variável"). Recalcular largura/gap para o stackup do fabricante escolhido e pedir impedância controlada quando a linha for crítica (INFERÊNCIA a partir das páginas citadas).

### 2. Dados do esquemático que servem a todos
Campos recomendados em cada símbolo montado (INFERÊNCIA a partir das exigências FATO de cada fabricante):
- `MPN` (Aisler lê `MPN`/`AISLER_MPN`; NextPCB, Seeed, Elecrow, ALLPCB, PCBWay turnkey, MacroFab exigem MPN; Fabrication Toolkit cai para `MPN` se não achar LCSC).
- `Manufacturer` (PCBWay via KiKit exige `Manufacturer` + `PartNumber`; PCBWay oficial pede "Manufacturers Name").
- `LCSC` (JLC; KiKit usa `LCSC` por padrão; Bouni e Fabrication Toolkit reconhecem `LCSC`).
- Opcional: `PartNumber` (= MPN, para o KiKit PCBWay), `Type` SMD/THT, correções por fabricante (`JLCPCB_CORRECTION`, `PCBWAY_CORRECTION`, `FT Rotation Offset`).
- DNP/“Exclude from BOM/position files” nativos do KiCad, que o Fabrication Toolkit respeita (FATO).

### 3. Saídas sempre geradas (pacote neutro)
- Gerber X2 (RS-274X compatível) + Excellon + mapa de furos; **ODB++** (`kicad-cli pcb export odb`, KiCad 9+) e **IPC-2581** (`kicad-cli pcb export ipc2581`, KiCad 8+) para quem aceita; netlist IPC-D-356 para teste elétrico (FATO: <https://docs.kicad.org/9.0/en/cli/cli.html>, <https://docs.kicad.org/8.0/en/cli/cli.html>; Fabrication Toolkit gera `netlist.ipc`).
- BOM "mestre" com todos os campos + CPL "mestre" em mm, com lado e rotação; converter para cada fabricante por script/KiKit (INFERÊNCIA).
- Desenho de montagem em PDF (Seeed pede quando falta designator no silk; FATO).
- Fontes embutidas na placa (KiCad 9+) para OSH Park/Aisler não trocarem a fonte (FATO, OSH Park e Aisler).

### 4. Quando e como trocar de fabricante
- **Gatilhos** (INFERÊNCIA): prazo/custo de alfândega para a UE subiu; peça indisponível na biblioteca do montador; precisa de material especial (Rogers, flex, IMS, ouro duro); precisa de qualidade/rastreabilidade industrial; precisa de impedância com stackup estável.
- **Checklist da troca** (INFERÊNCIA): (1) trocar o `.kicad_dru` e as regras do Board Setup pelas do novo fabricante e rodar o DRC; (2) refazer a calculadora de impedância no stackup novo; (3) reconferir cobre-borda, slot, castelado e acabamento (Aisler exige ENIG para castelado e furos pequenos, FATO); (4) regenerar BOM/CPL no formato novo e **reconferir as rotações na prévia do novo montador** (as correções da JLC não valem em outro lugar); (5) conferir regras de painel e trilhos; (6) conferir a política de impostos/frete do destino.

### 5. Regras DRU por fabricante

| Fabricante | Arquivo | Versão KiCad | Etiqueta |
|---|---|---|---|
| JLCPCB | `labtroll/KiCad-DesignRules` → `JLCPCB/JLCPCB.kicad_dru` (último push 2024-11-29) | 7 | FATO: <https://github.com/labtroll/KiCad-DesignRules> |
| JLCPCB, PCBWay, Genérico | `Cimos/kicad-druid` (variantes 2L-1oz, 4L-2oz, 6L-1oz; capacidades em `.toml`, gerador e linter) | sintaxe 8; roda em 8–10 | FATO: <https://github.com/Cimos/kicad-druid> |
| PCBWay | oficial `KiCAD_Custom_DRC_Rules_for_PCBWay.zip` (2023) e `labtroll/.../PCBWAY/PCBWay.kicad_dru` | não declarada / 7 | FATO |
| Aisler | oficial `AislerHQ/aisler-support/kicad/aisler-{2-layer-simple,2-layer-hd,4-layer-hd,6-layer-hd,8-layer-hd}-drc` | não verificada (commit 2026-01-20) | FATO |
| OSH Park | só instruções manuais | — | FATO |
| NextPCB | DFM pelo plugin HQ DFM (KiCad 9+); `.kicad_dru` não encontrado | 9+ | FATO (PCM) |
| Eurocircuits, Multi-CB, Würth | não encontrado (Multi-CB: regras digitadas à mão a partir da página KiCad) | — | FATO via agente |
| Seeed, ALLPCB, Elecrow, MacroFab | não encontrado | — | — |

Regra de uso (INFERÊNCIA, coerente com `06` regra 34): copiar o arquivo para `<projeto>.kicad_dru`, **conferir cada número contra a página de capacidades datada**, e manter um `.kicad_dru` "agnóstico" com os valores da seção 1 como padrão do projeto, trocando pelo do fabricante só quando ele estiver decidido.

### 6. Plugins e ferramentas KiCad por fabricante

| Fabricante | Ferramenta | O que faz | Etiqueta |
|---|---|---|---|
| JLCPCB | **Fabrication Toolkit** (bennymeg, PCM `com.github.bennymeg.JLC-Plugin-for-KiCad`) | pasta `production/` com `gerbers.zip`, `bom.csv`, `positions.csv`, `netlist.ipc`, `designators.csv`; CLI `python3 -m plugins.cli -p board.kicad_pcb` | FATO: <https://github.com/bennymeg/Fabrication-Toolkit> |
| JLCPCB | **kicad-jlcpcb-tools** (Bouni) | busca e atribui peças do catálogo JLC, gera Gerber/BOM/CPL e o arquivo de impedância `Required_impedance_control.xlsx`; KiCad 7–10 | FATO: <https://github.com/Bouni/kicad-jlcpcb-tools> |
| JLC, PCBWay, OSH Park, NeoDen YY1, OpenPnP | **KiKit** `kikit fab` com os subcomandos `jlcpcb`, `pcbway`, `oshpark`, `neodenyy1`, `openpnp`; presets de painel `jlcTooling`, `jlcVcuts` | ver formatos acima; `--no-drc`, `--nametemplate`, `--assembly --schematic` | FATO: <https://yaqwsx.github.io/KiKit/latest/fabrication/intro/>, <https://raw.githubusercontent.com/yaqwsx/KiKit/master/kikit/fab_ui.py> |
| PCBWay | **PCBWay Plug-in for KiCad** (envio direto ao carrinho; precisa do campo "Manufacture Part Number"; atualizado para KiCad 10) e **PCBWay Fabrication Toolkit** (exportação local) | | FATO: <https://github.com/pcbway/PCBWay-Plug-in-for-Kicad>, <https://github.com/pcbway/PCBWay-Fabrication-Toolkit-for-KiCad> |
| NextPCB | `kicad-nextpcb-plugin` (KiCad 7+), `kicad-hqdfm-plugin` (KiCad 9+) | envio/cotação; DFM | FATO (PCM) |
| Aisler | **AISLER Push for KiCad** (`com.github.aislerhq.PushForKiCad`), Push CLI, MCP | envia o projeto | FATO |
| Elecrow, Seeed, JLC, PCBWay, PCBGogo | **Gerber Zipper 2** (KiCad 9+, IPC API) com presets por fabricante | Gerber + zip + BOM + POS | FATO: <https://github.com/g200kg/kicad-gerberzipper2> |
| OSH Park | sem plugin; upload do `.kicad_pcb`; KiKit `oshpark` só faz `gerbers.zip` | | FATO |
| MacroFab | sem plugin oficial; terceiros `snhobbs/kicad-xyrs`, `aqsnyder/kicad-fab-package` | | FATO |
| Eurocircuits | upload nativo + PCB Visualizer/Checker online; plugin não encontrado | | FATO via agente |
| Multi-CB | upload nativo + guia KiCad 9 em PDF; plugin não encontrado | | FATO via agente |
| Würth WEdirekt | não encontrado (KiCad não listado) | | FATO via agente |
| ALLPCB | não encontrado | | — |

## Árvore de decisão "qual fabricante usar"

(INFERÊNCIA consolidada a partir das fichas; conferir preço e prazo ao vivo.)

```
1. Precisa de montagem (PCBA)?
   ├─ NÃO (placa nua)
   │   ├─ Precisa chegar rápido na Irlanda sem alfândega?      → Aisler (Blitz) ou Eurocircuits
   │   ├─ Menor preço, aceita 1–3 semanas e taxas de importação → JLCPCB / PCBWay / NextPCB
   │   ├─ Quer ENIG + stackup 4L publicado (FR408HR) e frete grátis → OSH Park (lento para a UE)
   │   └─ Material especial (Rogers, flex, rigid-flex, alumínio, ouro duro) → PCBWay (mais opções);
   │       JLC tem flex, alumínio e Rogers 2L; IMS na UE → Eurocircuits (pool IMS); flex/rigid-flex na UE → Würth ou Multi-CB
   └─ SIM
       ├─ Peças comuns que existem na biblioteca do montador?  → JLCPCB (LCSC Basic) ou Seeed (OPL)
       ├─ Peças ocidentais por MPN (Mouser/Digikey), protótipo rápido na UE → Aisler Amazing Assembly
       │   ou Eurocircuits (placa + montagem; borda ≥ 5 mm)
       ├─ Peças consignadas / mix                                → PCBWay (prefere consignado), Elecrow
       ├─ Montagem nos EUA (ITAR, cliente norte-americano)       → MacroFab
       └─ Volume / produção com qualidade industrial UE          → Eurocircuits (PCBA); placa nua industrial → Würth / Multi-CB (só empresas)
2. Linha de impedância crítica (USB, RF 50 Ω, DDR)?
   → escolher quem publica stackup e tolerância (JLC 4L+ ±10 %; NextPCB 4L+ ±10 %; PCBWay ±10 % / ±5 Ω;
     OSH Park stackup FR408HR); Aisler declara stackup 2L "variável" → evitar para impedância.
     Na UE: Eurocircuits DEFINED IMPEDANCE (4/6/8 camadas IS400) ou Multi-CB com buildup próprio (±10 %/±5 %);
     Würth pool pode ignorar a impedância sem avisar.
3. Furo < 0,25 mm, castelado, passo ≤ 0,5 mm?
   → ENIG obrigatório na Aisler; JLC recomenda ENIG; OSH Park já é ENIG.
```

## Armadilhas

| Armadilha | Consequência | Correção | Fonte |
|---|---|---|---|
| Projetar no mínimo da JLC (0,10/0,10, via 0,15) e depois mandar para Aisler/OSH/Elecrow | DRC do fabricante reprova ou cobra extra | Projetar no mínimo comum (0,20/0,20, via 0,30/0,70) | FATO (números) / INFERÊNCIA (regra) |
| Achar que `kikit fab neodenyy` existe | Comando falha | O nome é `neodenyy1` | FATO (fab_ui.py) |
| Reaproveitar o CPL da JLC em outro montador | Peças giradas; MacroFab lê **mils**, não mm | Gerar CPL por fabricante e conferir a prévia | FATO (MacroFab XYRS) / INFERÊNCIA |
| Correções de rotação feitas só para a JLC | Valem só para a orientação da fita da JLC | Usar campos por fabricante (`JLCPCB_CORRECTION`, `PCBWAY_CORRECTION`) | FATO (KiKit) |
| Subir `.kicad_pcb` com zonas não preenchidas na OSH Park | Placa sai com zonas velhas | Preencher zonas (tecla `b`) antes de salvar | FATO (OSH Park) |
| Subir `.kicad_pcb` feito em KiCad RC/beta na Aisler | Upload falha | Usar versão estável, Push ou ODB++ | FATO (Aisler) |
| Fonte personalizada no silk com upload nativo | Fonte trocada | Embutir fontes (KiCad 9+) ou mandar Gerber/ODB++ | FATO (OSH Park, Aisler) |
| Castelado ou furo < 0,3 mm na Aisler com HASL | Não é aceito | Escolher ENIG | FATO (Aisler) |
| Contar com impedância no 2L da Aisler | Stackup "variável" muda a impedância | Outro fabricante ou pedir stackup | FATO (Aisler) |
| Pedido B2C da China > 150 € ou com muitas linhas HS para a Irlanda | Imposto normal, €3/linha + €2 UHF por linha, taxa da transportadora | Comparar DDP × não DDP; consolidar; considerar fabricação na UE | FATO (FAQ JLC) |
| Contar com IOSS para cobrir tudo | IOSS cobre só IVA | Prever imposto temporário e UHF | FATO (JLC, NextPCB) |
| Pedir 5 placas na OSH Park ou Aisler | Cobra 6 (múltiplos de 3) | Pedir 3 ou 6 | FATO |
| Confiar no "a partir de US$ 2/US$ 5" | Tamanho, cor, acabamento e frete mudam o preço | Cotação instantânea com a configuração real | FATO (anúncios) / INFERÊNCIA |
| Usar o preço de tabela da Aisler (2023) | Valores divergem do próprio exemplo | Calculador ao vivo | FATO (divergência) |
| Conector na borda num pedido PCBA | JLC exige corpo ≥ 2,5 mm da borda | Trilho de processo ou solda manual | FATO (`06` regra 17) |
| Placa < 50×50 mm na ALLPCB PCBA ou < 10×10 mm na PCBWay/Seeed | Fabricante paineliza (custo/prazo) | Painelizar você mesmo com KiKit | FATO |
| OSH Park Flex | Serviço temporariamente suspenso | Outro fabricante para flex (PCBWay, JLC) | FATO |
| ODB++ para a JLC | Aceitação não confirmada | Mandar Gerber + Excellon | FATO (pergunta sem resposta) |
| Subir `.kicad_pcb` do KiCad 10 num fabricante cujo parser é mais antigo (OSH Park: KiCad 9.x; MacroFab: KiCad 8 citado) | Upload falha ou interpretação errada | Mandar Gerber X2 + Excellon (ou ODB++) ou confirmar o suporte antes; Aisler confirma KiCad 10 | FATO (versões) / INFERÊNCIA (risco) |
| Pedir impedância no pool da Würth WEdirekt | Se o pool não atinge, a placa sai no stackup padrão sem consulta | Usar non-pool, Eurocircuits DEFINED IMPEDANCE ou Multi-CB com buildup próprio | FATO via agente (WEdirekt) |
| Pessoa física pedir na Multi-CB | Vende só a empresas e instituições públicas | Aisler, Eurocircuits ou Würth | FATO via agente |
| Mandar placa de outra fábrica para a Eurocircuits montar | "Only assembly of boards produced by Eurocircuits" | Pedir placa e montagem juntas | FATO via agente |
| Silk de 1,0 mm numa placa da Würth | Abaixo do mínimo de 1,50 mm de altura | 1,5 mm de altura se a Würth for candidata | FATO via agente |

## Bibliografia

Todas consultadas em **2026-11-21**.

**JLCPCB**
- Capacidades PCB: https://jlcpcb.com/capabilities/pcb-capabilities
- Reforma alfandegária UE, FAQ (atualizado 28/10/2026): https://jlcpcb.com/help/article/eu-customs-reform-faq
- Pergunta sobre ODB++: https://jlc3dp.com/help/answers/detail/197-Can-ODB++-files-be-used-to-order
- Demais páginas da JLC: ver bibliografia de `09-ferramentas-fabrica-mcp-cad.md` e `06-shape-dfm-estetica.md`.

**PCBWay**
- Capacidades: https://www.pcbway.com/capabilities.html
- Arquivos de montagem: https://www.pcbway.com/assembly-file-requirements.html
- Capacidades de montagem: https://www.pcbway.com/assembly-capabilities.html
- Painel para montagem: https://www.pcbway.com/pcb_prototype/Panel_Requirements_for_Assembly.html
- Painelização, trilhos, fiduciais: https://pcbway.com/helpcenter/design_instruction/PCB_Panelization__Breakaway_Rails__Fiducial_Marks__Tooling_Holes.html
- Flex/rigid-flex: https://pcbway.com/FPC-Rigid-Flex-PCB.html
- Regras DRC personalizadas: https://www.pcbway.com/helpcenter/design_instruction/PCBWay_Custom_Design_Rules.html
- IOSS (2021): https://www.pcbway.com/blog/help_center/EU_e_commerce_adjustment_on_IMPORT_ONE_STOP_SHOP__IOSS_.html
- Home (promoções): https://www.pcbway.com/
- Plugin KiCad: https://github.com/pcbway/PCBWay-Plug-in-for-Kicad · Fabrication Toolkit: https://github.com/pcbway/PCBWay-Fabrication-Toolkit-for-KiCad

**NextPCB**
- Capacidades: https://www.nextpcb.com/pcb-capabilities
- Arquivos de montagem: https://support.nextpcb.com/portal/en/kb/articles/1-pcb-assembly-files-explanation
- Reforma alfandegária UE: https://www.nextpcb.com/news/eu-customs-reform-2026

**Seeed Fusion**
- Guia PCB/PCBA: https://wiki.seeedstudio.com/Service_for_Fusion_PCB/
- Documentos de fabricação: https://wiki.seeedstudio.com/service_for_fusion_manufacturing_documents/
- Especificação PCBA: https://support.seeed.cc/portal/en/kb/articles/fusion-pcba-specification
- Página de pedido: https://www.seeedstudio.com/fusion_pcb.html

**ALLPCB, Elecrow, MacroFab** (lidas pelo agente de pesquisa)
- https://www.allpcb.com/standard_pcb_manufacturing_capability.html · https://www.allpcb.com/pcb-capabilities.html · https://www.allpcb.com/pcb_assembly_capability.html · https://www.allpcb.com/faq/372.html · https://www.allpcb.com/shipping-information.html
- https://www.elecrow.com/pcb-manufacturing.html · https://www.elecrow.com/pcb-assembly.html · https://www.elecrow.com/terms-and-condition
- https://www.macrofab.com/pcb-assembly/capabilities · https://www.macrofab.com/blog/new-standard-drc-specifications-prototype-pcbs-with-smaller-features · https://macrofab.com/blog/improved-kicad · https://help.macrofab.com/knowledge/macrofab-required-design-files · https://github.com/MacroFab/EDALibraries

**OSH Park**
- 2 camadas: https://docs.oshpark.com/services/two-layer/ · 4 camadas: https://docs.oshpark.com/services/four-layer/ · Serviços: https://docs.oshpark.com/services/
- KiCad: https://docs.oshpark.com/design-tools/kicad/ · Regras KiCad: https://docs.oshpark.com/design-tools/kicad/kicad-design-rules/
- Envio: https://docs.oshpark.com/submitting-orders/shipping-information/

**Aisler**
- Placas: https://aisler.net/products/boards · Montagem: https://aisler.net/products/assembly
- Regras: https://community.aisler.net/t/pcb-design-rules/41 · https://community.aisler.net/t/2-layer-1-6mm-hasl-design-rules/3735
- Stackup 2L: https://community.aisler.net/t/2-layer-1-6mm-35-m/5571
- Limitações de ferramentas: https://community.aisler.net/t/known-pcb-design-tools-issues-and-limitations/2633
- Documentar peças: https://community.aisler.net/t/documenting-parts/56
- Preços (2023): https://community.aisler.net/t/our-simple-pricing · Envio: https://community.aisler.net/t/shipping-methods/672
- Base de conhecimento: https://community.aisler.net/c/knowledge-base/106
- Regras KiCad: https://github.com/AislerHQ/aisler-support/tree/master/kicad · Templates: https://github.com/AislerHQ/kicad_templates · Push: https://github.com/aislerhq/PushForKiCad

**Eurocircuits, Multi-CB, Würth WEdirekt** (lidas pelo agente de pesquisa)
- https://www.eurocircuits.com/technical-guidelines/pcb-design-guidelines/classification/ · tabela: https://www.eurocircuits.com/content/uploads/2025/04/EC-classification-ENGLISH-5-2024-V3.png
- https://www.eurocircuits.com/services/pcb-proto/ · https://www.eurocircuits.com/services/defined-impedance-pool/ · https://www.eurocircuits.com/pcba-capabilities/
- https://www.eurocircuits.com/user-guides/visualizer-user-guides/upload-cpl-data-user-guide/ · https://www.eurocircuits.com/technical-guidelines/pcb-design-guidelines/input-data-formats/ · https://www.eurocircuits.com/blog/kicad-eurocircuits-reads-in-native-kicad-data/
- https://www.eurocircuits.com/technical-guidelines/pcb-design-guidelines/legend-print/ · https://www.eurocircuits.com/user-guides/customer-account-user-guide/finance-and-administration/value-added-tax-vat/
- https://www.multi-circuit-boards.eu/en/pcb-design-aid/design-parameters.html · https://www.multi-circuit-boards.eu/en/support/pcb-data/kicad.html · https://www.multi-circuit-boards.eu/en/support/faq.html · https://www.multi-circuit-boards.eu/en/pcb-assembly.html · https://www.multi-circuit-boards.eu/en/products/printed-circuit-boards/prototypes.html · https://www.multi-circuit-boards.eu/en/pcb-express-service.html
- https://www.wedirekt.com/en/content/technology/pcbs · https://www.wedirekt.com/fr/content/technology/wedirekt-technical-capabilities · https://www.wedirekt.com/en/content/technology/data-formats · https://www.wedirekt.com/en/content/faq

**Impostos UE/Irlanda**
- Revenue (IVA da Irlanda): https://www.revenue.ie/en/vat/vat-rates/search-vat-rates/current-vat-rates.aspx
- JLCPCB, reforma UE: https://jlcpcb.com/help/article/eu-customs-reform-faq · NextPCB: https://www.nextpcb.com/news/eu-customs-reform-2026

**Ferramentas KiCad**
- KiKit fab: https://yaqwsx.github.io/KiKit/latest/fabrication/intro/ · código: https://github.com/yaqwsx/KiKit/tree/master/kikit/fab · presets: https://github.com/yaqwsx/KiKit/tree/master/kikit/resources/panelizePresets
- Fabrication Toolkit: https://github.com/bennymeg/Fabrication-Toolkit
- kicad-jlcpcb-tools: https://github.com/Bouni/kicad-jlcpcb-tools
- Gerber Zipper 2: https://github.com/g200kg/kicad-gerberzipper2
- PCM oficial (lista de pacotes): https://gitlab.com/kicad/addons/metadata/-/tree/main/packages
- DRU: https://github.com/labtroll/KiCad-DesignRules · https://github.com/Cimos/kicad-druid
- kicad-cli (ODB++ 9.0+, IPC-2581 8.0+): https://docs.kicad.org/9.0/en/cli/cli.html · https://docs.kicad.org/8.0/en/cli/cli.html · https://docs.kicad.org/10.0/en/cli/cli.html

## Cotação real JLCPCB (conta do dono, 2026-11-21, FATO; 5 placas 100×100 mm, FR-4 1,6 mm, verde, HASL, 1 oz, envio para a Irlanda)
| Config | Preço PCB | Produção | Frete |
|---|---|---|---|
| 2 camadas | **€3,64** (oferta) | 24 h (padrão do formulário) / 2 dias | UPS Express Saver **DDP €23,67**, 2–4 dias úteis, 0,29 kg |
| 4 camadas | **€7,29** (oferta; app desktop "a partir de €5,46") | 3–4 dias; 2–3 dias por **+€60,29** | idem |
- Armadilha vista: ao voltar de 4 para 2 camadas o formulário manteve "Via Covering" com custo de **€15,14** (opção de via tampada herdada). Confira o detalhamento antes de salvar no carrinho.
- Opções cotadas na mesma base (5 placas de 100×100 mm, 2026-11-21, FATO):

| Opção | 2 camadas | 4 camadas |
|---|---|---|
| Base (HASL com chumbo, verde, 1 oz) | €3,64 · 2 dias (24 h por +€6,92) · app desktop €1,82 | €7,29 · 3–4 dias (2–3 dias por +€60,29) · app desktop a partir de €5,46 |
| HASL sem chumbo | +€1,18 (total €4,83) | não cotado |
| **ENIG** (1 µ" de ouro) | +€16,12 (total €19,76) · prazo vai a 3 dias | +€16,12 (total €23,40) |
| Máscara **preta** | sem custo extra · prazo vai a 3 dias | não cotado |
| Cobre externo **2 oz** | +€33,15 (total €36,79) · 3 dias | não cotado |
| **Specify Stackup** = JLC04161H-3313 (impedância) | — | **sem custo extra** (total igual, €23,40 com ENIG) |
| Frete UPS Express Saver DDP para a Irlanda | €23,67 · 2–4 dias úteis · 0,29 kg | igual |

- **Achado importante:** ao escolher o stackup **JLC04161H-3313**, o site avisa *"This is a special stackup, and it doesn't support economic PCB assembly"*. Ou seja, 3313 obriga o **PCBA Standard**. O 7628 padrão não tem esse aviso.
- **Via covering:** em 4 camadas o padrão do formulário é "Plugged", e "Tented" fica desabilitado. Ao voltar para 2 camadas a escolha pode ficar herdada e custar +€15,14; confira o detalhamento.
- **Conclusões para orçamento de protótipo** (INFERÊNCIA a partir desses números):
  - Ir de 2 para 4 camadas custa ~€3,65 por lote de 5.
  - ENIG custa ~€16 por lote.
  - 2 oz custa ~€33 por lote.
  - O frete (~€24) costuma pesar mais que a placa.
  - Para RF e QFN de passo fino, 4 camadas + ENIG sai a ~€23 + frete.
