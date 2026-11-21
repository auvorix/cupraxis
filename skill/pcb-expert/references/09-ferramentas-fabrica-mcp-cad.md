# 09: Ferramentas, fábrica, KiCAD-MCP e CAD mecânico

> Corpus de referência para a skill universal "especialista em projeto de PCB" (KiCad 10, JLCPCB/PCBWay/Aisler, mercado UE). Pesquisa de 2026-11-21.
> Escopo: o pedido JLCPCB (PCB + PCBA), o KiCAD-MCP-Server instalado localmente, o co-design mecânico (FreeCAD/StepUp, OpenSCAD, impressão 3D), a simulação opcional e a visualização para campanha.
> **Etiquetas:**
> - **FATO**: conferido por mim na fonte primária. Pode ser a página web buscada (WebFetch), o arquivo local lido ou a saída de `--help` executada nesta máquina.
> - **FATO-sec**: tirado do resumo de uma busca (WebSearch) ou de uma fonte secundária. Não li a página primária inteira. Confirmar antes de usar como regra dura.
> - **INFERÊNCIA**: dedução minha ou prática comum, sem fonte primária.
>
> Caminhos locais citados:
> - `MCP\` = `%USERPROFILE%\AppData\Local\Programs\KiCAD-MCP-Server\` (v2.9.0, CHANGELOG de 2026-11-11).
> - `kicad-cli` = `%USERPROFILE%\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe` (`kicad-cli version` → **10.0.8**, FATO).
> - Nenhuma ferramenta MCP foi executada nesta pesquisa. Li arquivos, rodei `kicad-cli ... --help` e duas exportações do kicad-cli (BOM e pos) numa cópia descartável do demo `stickhub`, e li a versão de classe do `freerouting.jar`.

---

## Resumo

1. **O BOM da JLC tem as colunas `Comment, Designator, Footprint` e o código da peça** (o rótulo varia: "LCSC PN", "JLCPCB Part #"). O **CPL tem `Designator, Mid X, Mid Y, Layer, Rotation`**, em mm, com rotação positiva = anti-horária. Todo designator do BOM tem de existir, idêntico, no CPL (diferencia maiúsculas). Cada linha do BOM aceita no máximo 200 designators. ([KiCad 8 BOM/CPL](https://jlcpcb.com/help/article/how-to-generate-bom-and-centroid-files-from-kicad-8), [Pick & Place](https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly), [Recomendações BOM/CPL](https://jlcpcb.com/help/article/advice-for-bom-and-cpl-files-preparation); FATO.)
2. **Os exportadores do MCP não geram o formato JLC.**
   - `export_bom` grava só `value, footprint, quantity, references`. Não lê campo LCSC e não trata DNP (`MCP\python\commands\export.py:522-600`, FATO).
   - `export_position_file`/`export_pos` gravam o CSV do kicad-cli, cujo cabeçalho é `Ref,Val,Package,PosX,PosY,Rot,Side` (FATO: rodei o kicad-cli 10.0.8 numa cópia do demo `stickhub`). Precisa ser renomeado.
   - O caminho certo é `export_sch_bom` com `fields`/`labels`, ou o plugin **JLCPCB Fabrication Toolkit** (bennymeg), que a própria JLC recomenda.
3. **A rotação diverge porque o "0°" do footprint KiCad e o da JLC (orientação na fita) podem ser diferentes**, embora os dois usem o mesmo sentido de rotação. A correção:
   - offset por footprint (campo `FT Rotation Offset` no Fabrication Toolkit) ou edição da coluna Rotation;
   - conferir no **DFM/visualizador** da JLC, cuja prévia não é confiável para todas as peças.
   ([FAQ PCBA parte 2](https://jlcpcb.com/help/article/pcb-assembly-faqs-part-2), FATO-sec; [Fabrication-Toolkit](https://github.com/bennymeg/Fabrication-Toolkit), FATO.)
4. **Custos de PCBA (página de 22/10/2026), Economic × Standard:**

   | Item | Economic | Standard |
   |---|---|---|
   | Setup | US$ 8,18 | US$ 25,56 por face |
   | Stencil | US$ 1,53 | US$ 8,21 |
   | Feeder | US$ 3,07 só por **Extended** | US$ 1,53 por tipo, **Basic ou Extended** |

   "Basic = montagem grátis" vale só para Economic. A FAQ isenta as **Preferred Extended** da taxa de feeder na Economic. ([PCBA price](https://jlcpcb.com/help/article/pcb-assembly-price), [FAQ PCBA](https://jlcpcb.com/help/article/pcb-assembly-faqs); FATO.)
5. **A opção "remove order number" ficou obsoleta.** "Order Number is not available since May 2026." O padrão agora é **sem marca**. Não pôr mais `JLCJLCJLCJLC` no silk ([How to mark on PCB](https://jlcpcb.com/help/article/How-to-mark-on-PCB), atualizado em 22/05/2026, FATO).
6. **Prazos de fabricação da PCB** (≤ 100×100 mm, FR4 1,6 mm, HASL, máscara verde): 2 camadas com 5 pçs em **24 h**; 4 camadas em **2-5 dias**; 6 camadas em **6-7 dias**. A PCBA leva em geral **24-48 h** depois da placa ([produção](https://jlcpcb.com/help/article/pcb-fabrication-services-and-production-time), 10/11/2026; [FAQ PCBA](https://jlcpcb.com/help/article/pcb-assembly-faqs); FATO).
7. **No MCP, `route_trace`/`route_pad_to_pad` desenham UM segmento reto, sem checar colisão.** Uma rota assim atravessa pads e trilhas de outras redes. Usar só para ligações curtas e óbvias, e rodar `run_drc` depois de cada lote. O resto vai para `autoroute` (Freerouting) ou para o roteamento manual no KiCad (`MCP\python\commands\routing.py:474-700`, FATO).
8. **Todas as exportações por kicad-cli leem o `.kicad_pcb` SALVO** (`export_gerbers`, `export_drill`, `export_pos`, `export_3d_cli`). Rodar `save_board` antes de exportar (`MCP\src\tools\export.ts:334,404,605,944`, FATO).
9. **Mecânica:**
   - **KiCad StepUp NÃO está instalado** (o FreeCAD 1.1 local não tem pasta `Mod`) e declara suporte só até o FreeCAD 1.0.
   - O OpenSCAD local é **2021.01** e não importa STEP. Para ele, exportar DXF/SVG do Edge.Cuts ou STL/STEP→STL.
   - (FATO, `ls` local e [kicadStepUpMod](https://github.com/easyw/kicadStepUpMod).)
10. **Visualização:** o `kicad-cli pcb render` (KiCad 10.0.8) tem `--quality high`, `--floor`, `--perspective`, `--rotate`, `--background transparent` e luzes ajustáveis. Cuidado: **`-h` é ao mesmo tempo help e height**, então usar sempre `--height` (FATO, `--help` local).

---

## Receitas por etapa

### R1. Pedido JLCPCB: arquivos e formatos

**R1.1 Arquivos exigidos**
- PCB: Gerber RS-274X + Excellon (drill), num zip. PCBA: + **BOM** + **CPL**, em `.csv`, `.xls` ou `.xlsx` ([Pick & Place](https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly), FATO).
- Para o Gerber, a JLC recomenda o plugin **JLCPCB Fabrication Toolkit** (instalado pelo Plugin and Content Manager do KiCad). Ele gera o Gerber em zip, o BOM, o CPL e a netlist IPC ([KiCad 8 BOM/CPL](https://jlcpcb.com/help/article/how-to-generate-bom-and-centroid-files-from-kicad-8), [Fabrication-Toolkit](https://github.com/bennymeg/Fabrication-Toolkit); FATO).

**R1.2 BOM**

Colunas `Comment` (valor/especificação), `Designator`, `Footprint` e o código LCSC ([KiCad 8 BOM/CPL](https://jlcpcb.com/help/article/how-to-generate-bom-and-centroid-files-from-kicad-8), FATO).
- O rótulo da coluna do código aparece de formas diferentes: "LCSC PN" no guia do KiCad 8, "JLC Part #"/"LCSC Part #" no template citado pela busca. Não li o template oficial porque a seção de formato da página de recomendações é imagem (FATO-sec).
- Na prática o importador da JLC deixa mapear as colunas. **INFERÊNCIA:** usar `JLCPCB Part #` e conferir o mapeamento na tela de upload.
- Regras ([Recomendações BOM/CPL](https://jlcpcb.com/help/article/advice-for-bom-and-cpl-files-preparation), 09/09/2026, FATO):
  - designator único no BOM;
  - ≤ 200 designators por linha;
  - prefixo "C" para capacitor e "R" para resistor;
  - designators idênticos aos do CPL;
  - limpar os avisos (triângulos verdes) do Excel.

**R1.3 CPL**

Colunas `Designator, Mid X, Mid Y, Layer, Rotation`. Coordenadas em mm. Rotação em graus, positivo = anti-horário. Topo e fundo vão no mesmo arquivo, com Layer = `T/B` ou `Top/Bottom` ([Pick & Place](https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly), [Recomendações](https://jlcpcb.com/help/article/advice-for-bom-and-cpl-files-preparation); FATO).

**R1.4 Gerar o BOM JLC só com kicad-cli ou MCP** (sem plugin)
- O `kicad-cli sch export bom` aceita `--fields`, `--labels`, `--group-by`, `--exclude-dnp`, `--ref-delimiter` e `--ref-range-delimiter`. O padrão de `--ref-range-delimiter` é `"-"`, que produz faixas como `R1-R5` (FATO, `--help` local).
- **INFERÊNCIA:** a faixa `R1-R5` não casa com os designators do CPL. Desligar com `--ref-range-delimiter ""`.
- Comando testado (FATO: rodado no kicad-cli 10.0.8 sobre uma cópia do demo `stickhub`; o campo `LCSC` não existe no demo e saiu vazio):
  ```
  kicad-cli sch export bom proj.kicad_sch -o bom_jlc.csv \
    --fields "Value,Reference,Footprint,LCSC" \
    --labels "Comment,Designator,Footprint,JLCPCB Part #" \
    --group-by "Value,Footprint,LCSC" --ref-range-delimiter "" --exclude-dnp
  ```
- Saída real: cabeçalho `"Comment","Designator","Footprint","JLCPCB Part #"` e linhas como `"0.1uF","C2,C5,C6,C7,C8,C9,C10,C11,C12,C13","footprints:1005_C",""`. Com o delimitador padrão, o mesmo grupo sai como `"C2,C5-C13"`, o que confirma a armadilha da faixa (FATO, mesmo teste).
- O Footprint sai com o prefixo da biblioteca (`footprints:1005_C`). A JLC usa essa coluna só como referência (INFERÊNCIA).
- No MCP o equivalente é `export_sch_bom`, com os parâmetros `fields`, `labels`, `groupBy`, `excludeDnp`, `refDelimiter` e **`refRangeDelimiter`** ("blank disables ranges"). Passar `refRangeDelimiter: ""` (`MCP\src\tools\export.ts:1043-1099`, FATO).

**R1.5 Gerar o CPL**
- `kicad-cli pcb export pos --format csv --units mm --side both [--exclude-dnp] [--smd-only]`. Os padrões do kicad-cli são `--format ascii` e `--units in`, por isso é preciso passar os dois explicitamente (FATO, `--help` local).
- Saída real (FATO, kicad-cli 10.0.8, demo `stickhub`): cabeçalho `Ref,Val,Package,PosX,PosY,Rot,Side`; linha `"C1","1uF 10V","1005_C",156.022970,-94.994796,45.000000,bottom`. Side sai em **minúsculas** (`top`/`bottom`) e o Y sai **negativo** (eixo Y do KiCad para baixo).
- Renomear `Ref→Designator`, `PosX→Mid X`, `PosY→Mid Y`, `Rot→Rotation`, `Side→Layer`. A busca achou um guia da JLC que descreve esse mapeamento (FATO-sec, [JLC KiCad](https://jlcpcb.com/help/article/how-to-generate-the-bom-and-centroid-file-from-kicad)).
- **INFERÊNCIA:** a JLC aceita o Y negativo e `top/bottom` em minúsculas (é o formato que o guia descreve), mas conferir no visualizador. Se o sistema reclamar, trocar por `Top/Bottom`, a forma citada na página de recomendações.
- No MCP, `export_position_file` é um alias de `export_pos`. Ele mapeia `top/bottom/both → front/back/both`, usa mm por padrão e **recusa `mil`** (`MCP\src\tools\tool-aliases.ts:48-66`, FATO).

**R1.6 Rotação errada**
- **Causa:** "o 0° que você definiu pode ser diferente do nosso, mas usamos a mesma rotação". A referência da JLC é a orientação da peça na fita ([FAQ PCBA parte 2](https://jlcpcb.com/help/article/pcb-assembly-faqs-part-2), FATO-sec, citado no resumo da busca).
- **Correção:**
  1. Fabrication Toolkit: o banco `rotations.cf` corrige a maior parte. Para exceções, criar no footprint ou símbolo o campo `FT Rotation Offset` (graus, positivo = anti-horário) e, se preciso, `FT Position Offset` ("x,y" separados por vírgula; a página não dá a unidade, provavelmente mm = INFERÊNCIA). Um toque de seta no visualizador da JLC = 0,0635 mm ([Fabrication-Toolkit](https://github.com/bennymeg/Fabrication-Toolkit), FATO).
  2. Sem plugin: editar a coluna Rotation e subir de novo ([FAQ](https://jlcpcb.com/help/article/pcb-assembly-faqs-part-2), FATO-sec).
  3. **Sempre conferir no DFM/visualizador de montagem da JLC antes de pagar.** Relatos mostram que a prévia e o DFM divergem (ex.: conector USB que precisava de mais 180°) e que a prévia não mostra a orientação de todas as peças ([EasyEDA forum](https://easyeda.com/forum/topic/C10418-rotation-inconsistency-between-preview-and-DFM-analysis-1fd042a8ebde40d7b9e457f2d4660938), [KiCad forum](https://forum.kicad.info/t/jlcpcb-bom-and-pick-and-place/19016/11); FATO-sec).
  4. Garantir que o pino 1 está marcado no silk. A JLC finaliza a posição com base no CPL **e** nas marcas de silk ([after-sales FAQ](https://jlcpcb.com/help/article/common-pcba-after-sales-issues-and-faq), FATO-sec).
- Peças que mais erram, segundo a prática comum (INFERÊNCIA): SOT-23, diodos/LEDs polarizados, conectores USB-C/JST, QFN/QFP com pino 1 diferente, eletrolíticos.

**R1.7 Economic × Standard** ([PCBA price](https://jlcpcb.com/help/article/pcb-assembly-price) de 22/10/2026 e [FAQ](https://jlcpcb.com/help/article/pcb-assembly-faqs) de 09/09/2026, FATO)

| Item | Economic | Standard |
|---|---|---|
| Setup | US$ 8,18 | US$ 25,56 por face (US$ 51,12 nas duas) |
| Stencil | US$ 1,53 | US$ 8,21 por face |
| Feeder | US$ 3,07 por Extended; Basic isento (Preferred Extended isento, segundo a FAQ) | US$ 1,53 por feeder, Basic **e** Extended |
| Painel | mouse-bite (FAQ) | aceita V-cut |
| Solda manual | US$ 0,0164/junta + US$ 3,58/pedido | igual |

- Limites da Economic (FATO-sec, [capabilities PCBA](https://jlcpcb.com/capabilities/pcb-assembly-capabilities) via busca): 2-50 pçs; 2/4/6 camadas; montagem só numa face; passivo ≥ 0402; passo de CI ≥ 0,4 mm. A Standard vai até 01005 e passo 0,35 mm, com montagem nas duas faces.
- Uma peça "Standard only" força o pedido inteiro para a Standard (FATO-sec, [techoverflow](https://techoverflow.net/2024/04/10/jlcpcb-pcb-assembly-list-of-known-standard-only-parts/)).

**R1.8 Peças e estoque**
- **Basic:** já ficam carregadas na máquina. **Extended:** exigem montar o feeder à mão. **Preferred Extended:** eram Basic e foram reclassificadas como Extended (Preferred); são isentas de feeder na Economic ([FAQ PCBA](https://jlcpcb.com/help/article/pcb-assembly-faqs), FATO).
- **My Parts Lib / pré-compra** ([How to build your own parts library](https://jlcpcb.com/help/article/how-to-build-your-own-parts-library-in-jlcpcb), FATO-sec):
  - sem custo de inventário;
  - Extended em estoque sem quantidade mínima; Extended fora de estoque só por pré-pedido, com mínimo;
  - Basic só por pré-pedido com mínimo, e raramente é preciso;
  - as peças só servem para PCBA e não são enviadas avulsas;
  - se o My Parts tiver quantidade suficiente, o sistema usa ele primeiro; se faltar, completa com o estoque da JLC.
- **Global Sourcing:** a JLC compra de distribuidores. Prazo de **9-15 dias** ([termos](https://jlcpcb.com/help/article/global-sourcing-parts-order-terms-conditions), FATO-sec).
- **Consignadas:** você envia as peças e paga frete e alfândega; taxa de US$ 0,142/pç para manuseio manual ([termos](https://jlcpcb.com/help/article/consignment-part-terms-conditions), FATO-sec).
- **Regra de mistura:** para o MESMO part number, estoque JLC/pré-compra não se mistura com Global Sourcing/consignado (FATO-sec, mesmas páginas).

**R1.9 Opções do pedido da PCB** ([PCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities), FATO, sem data na página)

| Opção | O que a página diz |
|---|---|
| Espessura | 0,4/0,6/0,8/1,0/1,2/1,6/2,0 mm (≥ 2,5 mm só para 12+ camadas). Tolerância ±10 % (≥ 1 mm) ou ±0,1 mm (< 1 mm). |
| Acabamento | HASL (com ou sem chumbo), ENIG, OSP. Sem HASL em: 6+ camadas, ≤ 0,4 mm, alta frequência, base de cobre, flex. Borda metalizada e microvia 0,1 mm exigem ENIG/OSP. |
| Impedância | 4 a 32 camadas, ±10 % (±5 % sob pedido especial). Calculadora: 20-90 Ω single-ended, 50-150 Ω diferencial ([calculadora](https://jlcpcb.com/capabilities/impedance-calculator), FATO-sec). O stackup listado é o produzido, e a espessura do PP é a pós-laminação ([laminated structures](https://jlcpcb.com/help/article/multi-layer-pcb-standard-laminated-structures), FATO-sec). |
| Cobertura de via | Plugged com máscara (Ø ≤ 0,5 mm, nenhuma abertura); epoxy filled & capped (vias 0,15-0,55 mm, padrão em 6+ camadas); copper paste filled. "Tented" e "untented" **não aparecem** na página. |
| Cor | Verde, roxo, vermelho, amarelo, azul, branco, preto. Ponte mínima de máscara 0,10 mm (0,13 mm em preto/branco). A página não diz se a cor muda preço ou prazo. |
| Mínimos | 2 camadas: 0,10/0,10 mm, via 0,15/0,25 mm. 4 camadas: 0,09/0,09 mm. Furo preferido ≥ 0,2 mm. Furos de 0,1-0,15 mm (ou 0,2-0,25 mm com anel < 0,45 mm) custam mais. |
| Marca | Padrão sem marca. Opções: 2D barcode, número serial ou os dois. Order number indisponível desde 05/2026 ([How to mark](https://jlcpcb.com/help/article/How-to-mark-on-PCB), FATO). |

**R1.10 Comparação rápida com PCBWay e Aisler**

| Fábrica | O que encontrei | Etiqueta |
|---|---|---|
| **PCBWay** | BOM em xls/xlsx/csv. Consignado: Line #, quantidade, designator, part number, descrição, package, tipo. Turnkey: + fabricante, MPN, código do distribuidor. Centroid: designator, X, Y, rotação, face (Top/Bottom), só SMD. Montagem "de 24 h a algumas semanas", contada só quando peças e arquivos estão completos. Mínimo 5 pçs. Prefere consignado; turnkey "sem markup" nas peças. | FATO ([file req.](https://www.pcbway.com/assembly-file-requirements.html), [capabilities](https://www.pcbway.com/assembly-capabilities.html)) |
| **Aisler** | "Locally manufactured in Europe", "Manufactured and delivered from Germany". 2/4/6/8 camadas FR4, HASL ou ENIG. Blitz: 2 camadas HASL a partir de 2 dias úteis de fabricação (+ entrega). ENIG e 4 camadas demoram mais. Montagem "Amazing Assembly" em 6 dias úteis. Aceita o projeto KiCad nativo. A página se contradiz entre "one business day" e "two business days". | FATO ([boards](https://aisler.net/products/boards)) |
| Aisler × JLC para a UE | Fabricar na UE evita alfândega/IVA de importação e encurta a entrega, mas o preço unitário é maior. | INFERÊNCIA |

### R2. KiCAD-MCP-Server: ferramentas por etapa

Configuração e limitações gerais (FATO, `MCP\README.md` e `MCP\docs\KNOWN_ISSUES.md`):
- **Quantidade de ferramentas:** 253. Para não lotar o contexto, usar `KICAD_MCP_TOOLBOXES=core` ou uma lista (ex.: `schematic,drc,routing`). Para agentes de revisão, `KICAD_MCP_OPERATING_MODE=readonly` ou `manufacturing`.
- **Backends:** SWIG (edita o arquivo; a UI do KiCad só mostra depois de File > Revert) e IPC (experimental; KiCad aberto com Preferences > Plugins > Enable IPC API Server). Alguns comandos voltam para SWIG.
- **Depois de reiniciar o servidor**, sempre rodar `open_project`.
- **Dois parsers:**
  - O kicad-cli (`run_erc`, todos os `export_*`, netlist) é a verdade.
  - O kicad-skip (edição e inspeção do esquemático) é mais estrito e quebra com símbolos "flat" da SnapEDA/SamacSys. A correção é `repair_flat_symbols`.
  - (`MCP\docs\HEADLESS_AUTHORING.md` §1, §7a, FATO.)

**R2.1 Projeto e esquemático**

| Ferramenta | O que faz | Armadilhas (FATO, fonte) |
|---|---|---|
| `create_project`, `open_project`, `save_project`, `snapshot_project` | Ciclo de vida do projeto; snapshot cria um checkpoint nomeado | `close_project` com `save=false` descarta mudanças com aviso (CHANGELOG) |
| `create_schematic`, `batch_add_and_connect`, `batch_add_no_connects`, `add_schematic_component`, `connect_to_net` | Põe símbolos e liga pinos por nome de net | Origem dos símbolos na grade de **2,54 mm**. Um único ponto fora da grade de 1,27 mm estraga as junções da folha inteira; corrigir com `lint_offgrid fix:true` (HEADLESS_AUTHORING §2, §6) |
| `run_erc` | ERC via kicad-cli | Coordenadas do relatório vêm em **mm/100**. Em projeto hierárquico com global labels, rodar o ERC na **folha raiz**. `PWR_FLAG`: exatamente um por net de alimentação sem `power_output` (HEADLESS_AUTHORING §4-5) |
| `generate_netlist`, `export_netlist` | Netlist autoritativa | Não confiar em "connected N pin(s)". Validar com ERC + render + netlist (HEADLESS_AUTHORING §3) |
| `edit_schematic_component`, `set_schematic_component_property` | Grava campos MPN/LCSC no símbolo | Edições são **recusadas com o esquemático aberto no KiCad** (README v2.9) |

**R2.2 Sync para a placa**
- `sync_schematic_to_board` equivale ao F8. É **obrigatório** antes de posicionar ou rotear. Sem ele, a placa fica sem footprints e sem nets (`MCP\src\tools\schematic.ts:1652`, FATO).
- Desde a v2.9 as nets vêm do `kicad-cli sch export netlist`. Antes disso, numa placa real, **304 de 333 pads** ficaram com a net errada enquanto a ferramenta dizia "success". Conferir a versão instalada, que é a 2.9.0 (`MCP\CHANGELOG.md:207-215`, FATO).
- `create_board_from_schematic` cria o `.kicad_pcb` e já sincroniza (`schematic.ts:1713`, FATO).

**R2.3 Placement**

| Ferramenta | O que faz | Armadilhas |
|---|---|---|
| `place_component` | Põe footprint em x, y, rotação, layer | Para placa vinda do esquemático, preferir mover o que o sync criou a pôr peças novas (INFERÊNCIA) |
| `move_component`, `batch_move_components`, `rotate_component` | Reposiciona ou vira de face | Lote transacional (README) |
| `suggest_placement` | Força dirigida: aproxima peças ligadas, gira 0/90/180/270 para o vizinho, separa courtyards. Métrica: HPWL | O cabeçalho diz **"DRAFT — proposed new MCP capability"**. É **dry-run por padrão**. Usa o AABB combinado em footprints com vários courtyards, o que espaça demais. Não conhece RF, térmica nem conector na borda: **o floorplan humano vem primeiro** (`placement_optimizer.py:1-31`, FATO; última frase INFERÊNCIA) |
| `check_courtyard_overlaps` | Sobreposição de courtyards, inclusive com `positions` hipotéticas; opcionalmente courtyard fora do contorno | Caixa AABB por contorno de courtyard (cada contorno separado desde a #406). Não substitui o DRC (CHANGELOG:472-477, 1933-1934, FATO) |
| `check_placement_clearance` | Classifica o conflito: corpo, courtyard, keepout, silk/texto ou pad | Aproximação; conferir com `run_drc` (INFERÊNCIA) |
| `get_ratsnest`, `estimate_airwire_lengths` | Medem as conexões ainda não roteadas | — |

Fluxo previsto no código: `suggest_placement(dry)` → `check_courtyard_overlaps(positions=...)` → `apply=true` → `autoroute` → `run_drc` (`placement_optimizer.py:24-26`, FATO).

**R2.4 Roteamento**

| Ferramenta | O que faz | Armadilhas (FATO salvo indicação) |
|---|---|---|
| `route_trace` | Um segmento reto entre 2 pontos numa camada | **Não muda de camada.** **Não checa colisão.** Se o nome da net não existe, o código cria a trilha **sem net** e não dá erro (`routing.py:642-700`: `if nets_map.has_key(net)` sem `else`) |
| `route_pad_to_pad` | Liga pad a pad: acha as posições, pega a net do pad e põe via se as faces diferem | Também é **reta, sem checar obstáculos**. A via vai no **X do pad inicial e no Y médio**, também sem checar. A descrição TS diz "midpoint", o que não bate com o código (`routing.ts:597` × `routing.py:562-570`) |
| `route_differential_pair` | Dois segmentos paralelos e retos; o positivo fica à direita no sentido start→end; offset (gap+width)/2 | **Não termina nos pads**: é preciso ligar com `route_trace`. Não faz casamento de comprimento. Até a #407 o schema não batia e toda chamada falhava (ROUTING_TOOLS_REFERENCE, CHANGELOG:478-485) |
| `copy_routing_pattern` | Replica o roteamento entre blocos iguais | Os refs têm de estar na mesma ordem |
| `autoroute` | DSN → Freerouting CLI → SES. Opções: `attempts` (best-of-N), `targetNets`, `passSchedule`, `routeNets`/`excludeNets`, `signalLayers`, `layerTraceCosts`, `keepArtifacts` | Exige o Java **que o JAR pede** (21+; o 2.4.x exige 25) ou Docker/Podman. Num único passe, placas densas costumam ficar com 1-7 nets sem rota; usar `attempts` 3-5. Usar `excludeNets` para potência/RF roteadas à mão e `signalLayers` para manter trilhas fora do plano (`freerouting.ts:10-90`) |
| `export_dsn` / `import_ses` | Round-trip manual (GUI do Freerouting) | Furos redondos e recortes no Edge.Cuts saem como keepout com a folga cobre-borda. Referências `REF**` duplicadas viram `REF**_1`, `_2`, e o `import_ses` descarta essas entradas de placement (`placementSkipped`). **Um import que falha já removeu as trilhas não travadas da memória: reabrir do disco antes de salvar** (FREEROUTING_GUIDE) |
| `check_freerouting` | Diz o Java e a versão que o JAR exige (`java.required_version`) | Rodar antes do `autoroute` |

Ambiente local:
- O `<DEVSHARED>\README.md:38-40` registra o Freerouting **v2.5.0** em `%USERPROFILE%\.kicad-mcp\freerouting.jar`, com JDK 21 como padrão e JDK 25 em `<DEVSHARED>\jdk25\jdk-25.0.5+8` (FATO).
- **O JAR local exige Java 25:** a classe `app/freerouting/Freerouting.class` tem major version **69** = Java 25 (FATO: li os bytes 6-7 da classe dentro do JAR). Com o JDK 21 padrão, o `autoroute` cai em Docker/Podman ou falha. Apontar `JAVA_HOME` (no `env` do servidor MCP) para `<DEVSHARED>\jdk25\jdk-25.0.5+8` e conferir com `check_freerouting` (INFERÊNCIA: não testei se o servidor detecta esse Java).

**R2.5 Zonas**

| Ferramenta | O que faz | Armadilhas |
|---|---|---|
| `add_copper_pour` / `add_zone` | Zona por camada e net; sem `outline` ocupa a placa toda | Depois, preencher |
| `refill_zones` | Recalcula o preenchimento | **No backend SWIG pode dar segfault.** Preferir IPC (KiCad aberto) ou abrir no KiCad. O `run_drc` no KiCad 10 já preenche antes (KNOWN_ISSUES #2; CHANGELOG:329-340, FATO) |
| `add_gnd_stitching_vias` | Vias de GND com estratégia `grid`, `around_refs` ou `in_zones`. Checa colisão contra segmentos, vias e pads de outras nets em **todas** as camadas. Tem `dryRun` | Rodar com `dryRun` primeiro. Usar `in_zones` para a via costurar polígono real. Furo padrão 0,3 mm. Arcos eram tratados como corda até a #192 (`routing.ts:358`, CHANGELOG:1387, FATO) |
| `query_zones`, `summarize_net_copper`, `summarize_vias` | Inspeção sem listar milhares de itens | — |
| `audit_via_nets` | Compara a net de cada via com uma placa de referência ou revisão git | O KiCad pode mudar uma via de net ao salvar, e o DRC não percebe (README v2.9, FATO) |

**R2.6 Verificação**
- `run_drc`: DRC via kicad-cli. Desde a v2.9 inclui **itens não conectados** e **paridade com o esquemático**; antes, uma placa com nets sem rota podia sair "0 erros". No KiCad 10 preenche as zonas primeiro (CHANGELOG:329-340, FATO).
- `get_drc_violations`: lista por severidade e usa o `run_drc` por baixo (`design-rules.ts:295`, FATO).
- `set_voltage_clearance_rules`: grava regras de clearance/creepage por tensão no `.kicad_dru`. **A tabela de espaçamento vem da norma do usuário; a ferramenta não traz valores** (CHANGELOG 2.9.0, FATO).
- `get_stackup` / `set_stackup_layer`: lê e grava o stackup, com comparação contra uma receita (FATO, CHANGELOG 2.9.0).

**R2.7 Fabricação**

| Ferramenta | Uso | Armadilhas |
|---|---|---|
| `export_gerbers` | Gerber via kicad-cli, com todas as opções do diálogo Plot | Lê o arquivo **salvo**. Preferir ao `export_gerber` (SWIG), que até a #455 **não gravava arquivo** e dizia que sim (CHANGELOG:466-471) |
| `export_drill` | Excellon, com opções de PTH/NPTH separados, mapa etc. | Lê o arquivo salvo |
| `export_bom` | BOM a partir da placa | **Não serve para a JLC:** colunas fixas `value, footprint, quantity, references`; `includeAttributes` chama métodos `Get<attr>()` e por isso não lê o campo LCSC; ignora DNP; com 0 componentes, `components[0]` quebra (`export.py:522-600`, FATO). Usar `export_sch_bom` (R1.4) |
| `export_position_file` / `export_pos` | CPL via kicad-cli | Renomear cabeçalhos para a JLC. `mil` é recusado (R1.5) |
| `export_3d_cli` | STEP/GLB/STL/VRML para a mecânica | Lê o arquivo salvo |
| `export_pcb_dxf` | DXF para OpenSCAD/carcaça | — |

**R2.8 Banco JLCPCB**

| Ferramenta | O que faz | Armadilhas (FATO) |
|---|---|---|
| `download_jlcpcb_database` | SQLite local. Fontes: `cdfer` (padrão, **só itens em estoque**, ~480 mil peças, ~400 MB), `yaqwsx` (catálogo completo ~2,9 M, precisa de 7z), `official` (precisa de credenciais) | Os números de catálogo não batem entre os docs (2,5 M+ / ~600 mil / ~480 mil) (`jlcpcb-api.ts:13-25`; `JLCPCB_USAGE_GUIDE.md:28`) |
| `search_jlcpcb_parts` | Busca paramétrica, inclusive por `library_type` Basic/Extended/Preferred | O snapshot pode estar **dias a semanas atrasado** em preço e estoque (`JLCPCB_USAGE_GUIDE.md:36-38`) |
| `get_jlcpcb_part` | Detalhe por código LCSC; com `JLCPCB_APP_ID/API_KEY` vem ao vivo | Sem credenciais, usa o snapshot |
| `suggest_jlcpcb_alternatives` | Alternativas mais baratas, com mais estoque ou Basic | Conferir footprint e parâmetros: "Footprint mapping may need manual verification" (`JLCPCB_USAGE_GUIDE.md:340`) |

O texto dos docs do MCP ("Basic = free assembly; Extended US$ 3") só é verdade na **Economic**. Na Standard, até as Basic pagam feeder de US$ 1,53 (FATO, R1.7).

### R3. Co-design mecânico

**R3.1 FreeCAD + KiCad StepUp** ([kicadStepUpMod](https://github.com/easyw/kicadStepUpMod), FATO)
- **Funções:** carregar a placa e os modelos 3D do KiCad; exportar STEP/IGES; desenhar o contorno no Sketcher e fazer **push** para um `.kicad_pcb` existente, ou **pull** do contorno, editar e devolver; checar colisões entre carcaça e footprints.
- **Compatibilidade declarada:** FreeCAD 0.19 a 1.0 (não cita 1.1); KiCad 5.1 a 10.x. A instalação pelo Addon Manager pode falhar no Linux com FreeCAD ≥ 1.0.1.
- **Ambiente local (FATO, `ls`):** FreeCAD 1.1 em `%USERPROFILE%\AppData\Local\Programs\FreeCAD 1.1`, **sem pasta `Mod`** em `%APPDATA%\FreeCAD\v1-1`. Logo o StepUp **não está instalado**. Pendência para o dono: instalar pelo Addon Manager e testar no 1.1.
- **Receita (INFERÊNCIA):**
  1. `kicad-cli pcb export step` (ou `export_3d_cli format=step`) → importar no FreeCAD.
  2. Modelar a carcaça em volta.
  3. Checar interferência com Part > Check geometry ou com a ferramenta de colisão do StepUp.
  4. Se o contorno mudar na mecânica, devolver ao KiCad pelo push de sketch do StepUp.

**R3.2 OpenSCAD**
- O `import()` aceita **STL, OFF, 3MF (3D) e DXF, SVG (2D)**; OBJ só em snapshot de desenvolvimento. **STEP não está listado.** No DXF dá para escolher a `layer` ([manual](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Importing_Geometry), FATO).
- A versão local é a **2021.01** (`openscad.com --version`, FATO).
- **Receita (INFERÊNCIA):**
  1. `kicad-cli pcb export dxf --layers Edge.Cuts` (ou `export_pcb_dxf`) → `linear_extrude(1.6) import("placa.dxf")` para o volume da placa.
  2. Os furos de fixação saem do mesmo DXF.
  3. Os componentes altos entram como STL exportado do STEP (`kicad-cli pcb export stl`), só para checar folga.
  4. Gerar a carcaça com `offset(r=folga)` do contorno.

**R3.3 Tolerâncias FDM para carcaça de PCB** (valores iniciais; validar com corpo de prova na impressora)

| Item | Valor | Fonte |
|---|---|---|
| Folga placa-parede / componentes internos | ~0,5 mm | FATO ([Hubs](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)) |
| Folga de encaixe (peça-peça) | 0,1-0,2 mm conforme a impressora; 0 mm costuma travar | FATO-sec ([UAL wiki](https://wiki.cci.arts.ac.uk/books/digital-fabrication-lab/page/design-the-clearance-and-tolerance)) |
| Parede | ≥ 2 mm (Hubs). Mínimo FDM ≥ 0,8 mm ou 2× o bico (PCBWay). Conflito: usar 2 mm como padrão | FATO (Hubs) / FATO-sec ([PCBWay blog](https://www.pcbway.com/blog/PCB_Design_Layout/PCB_Enclosure_Design_Guide_Materials_IP_Ratings_and_DFM_Considerations_3349fb77.html)) |
| Furo passante para parafuso | Ø nominal + 0,25 mm | FATO (Hubs) |
| Furo para autoatarraxante | Ø nominal − 0,25 mm | FATO (Hubs) |
| Abertura de porta/conector | +2 mm no total (1 mm por lado) | FATO (Hubs) |
| Boss | parede em volta ≥ 1× o diâmetro do furo | FATO (Hubs) |
| Canto interno | o FDM arredonda o canto interno e ele colide com o canto vivo da PCB; prever alívio ou mais folga. A expansão térmica do plástico muda o ajuste | FATO-sec ([Aisler community](https://community.aisler.net/t/tolerance-management-between-pcb-and-3d-printing/5540)) |

**Insert de latão a quente (heat-set), M2/M2.5.** Não achei a tabela oficial da CNC Kitchen nem da Ruthex. As fontes divergem:

| Fonte | M2 | M2.5 | Etiqueta |
|---|---|---|---|
| McMaster | broca 3,2 mm (insert de 4 mm) | broca 4 mm (comprimento instalado 4 mm); furo máx. 4,1 mm (insert de 5,9 mm) | FATO-sec |
| Tabela Accu | 3,3 mm | 4,1 mm | FATO-sec ([Accu](https://accu-components.com/p/488-threaded-insert-hole-size-charts-for-3d-printing-pla-petg-resin)) |
| binkey (estilo CNC Kitchen) | — | 3,7 mm (insert M2.5×4) | FATO-sec, não verificado |
| Regra geral U. Wisconsin | Ø externo do insert − 0,3 mm | Ø externo do insert − 0,3 mm | FATO-sec ([UW](https://medesignlab.me.wisc.edu/?p=162)) |

- Profundidade do furo: comprimento do insert + ≥ 1 mm (FATO-sec, [Digi-Key/FreeCAD](https://www.digikey.com/es/maker/tutorials/2025/intro-to-freecad-part-4-how-to-use-heat-set-inserts)).
- Parede em volta do insert: 1,4 mm mínimo para M2 (Accu), 1,6 mm (Digi-Key) ou 2,0 mm (outra fonte). **Recomendo 2 mm** (INFERÊNCIA, pelo lado conservador).
- Mais perímetros (wall loops) aumentam a retenção (FATO-sec, UW).
- **Regra para a skill (INFERÊNCIA):** pegar o Ø do furo no desenho do fabricante do insert comprado. Sem desenho, começar em **M2 ≈ 3,2 mm** e **M2.5 ≈ 3,6-4,0 mm** e imprimir um corpo de prova com 3 diâmetros.

**R3.4 Light pipes e recortes**
- **Light pipe:** a ponta do pipe vai o mais perto possível do LED, sem tocar a lente. Um LED de ângulo estreito ajuda. Adaptadores que envolvem o LED eliminam vazamento de luz. Pipe rígido funciona até ~3" (FATO-sec, [Bivar FAQ](https://bivar.com/resources/light-pipe-faqs/?amp=1)). Dialight recomenda um LED específico por pipe e dá a altura PCB-centro da lente no desenho (FATO-sec). Não achei um gap numérico padrão: usar o datasheet do pipe.
- **USB-C:** a fonte numérica que achei é a de um usuário do fórum Digi-Key, que limita o overmold do plugue a ~12,5 mm de comprimento numa porta rebaixada. **Não é especificação** (FATO-sec, [Digi-Key forum](https://forum.digikey.com/t/overmold-size-of-the-usb-c-male-end/70874)). A fonte autoritativa é o desenho da USB-IF (não lido). **INFERÊNCIA:**
  - receptáculo rente à parede ou com no máximo ~0,5 mm de recuo;
  - abertura = contorno do receptáculo + 0,5-1 mm por lado (a regra da Hubs dá 1 mm por lado);
  - pensar no plugue moldado mais gordo dos cabos comuns.
- **SMA:** rosca 1/4-36 UNEF (≈ 6,35 mm). Recorte de painel de 6,35 ±0,05 mm (Würth bulkhead) a 6,4-6,55 mm (guias de fornecedor) (FATO-sec, [Würth datasheet](https://www.we-online.com/components/products/datasheet/60332042111504.pdf)). O SMA de borda (edge-launch) é especificado para a espessura da placa (0,8/1,6 mm): casar com a espessura pedida à JLC (FATO-sec, [Adafruit](https://www.adafruit.com/products/1865); casamento = INFERÊNCIA).
- **microSD:** não achei guia. **INFERÊNCIA:** usar o desenho do slot (push-push precisa de curso extra para ejetar); fenda = largura do cartão (11 mm) + ~1 mm, com um rebaixo para o dedo.

### R4. Simulação e verificação opcional (só gratuitas)

| Ferramenta | Para quê | Fonte |
|---|---|---|
| **ngspice no KiCad** | Simulação no editor de esquemático: OP, DC sweep, AC, transiente, ruído. Aceita modelos SPICE/LTspice/PSpice/HSpice. O `ngspice.dll` vem com o KiCad 10 local | FATO-sec ([kicad.org/discover/spice](https://kicad.org/discover/spice)); DLL = FATO (`ls` em `KiCad\10.0\bin`) |
| **openEMS** | FDTD 3D livre (GPLv3), scriptado em Octave/MATLAB/Python. Antena e transição de linha | FATO-sec ([docs.openems.de](https://docs.openems.de/intro.html)) |
| **Sonnet Lite** | EM planar grátis com registro. 64 MB de memória, até 6 portas, 2 níveis de condutor + GND. Última versão listada 18.53 (out/2021). A licença proíbe publicar comparações competitivas | FATO-sec ([Sonnet](https://sonnetsoftware.com/products/lite/download.html)) |
| **Qucs-S** | Circuito/RF; Qucsator embutido a partir da 24.2.0. **QucsStudio não é software livre** (é freeware) | FATO-sec ([openEMS/Qucs-S](https://openems.readthedocs.io/en/latest/concepts/postproc/qucs.html)) |
| **Saturn PCB Toolkit** | Calculadora freeware (impedância, corrente de trilha, via). Disponível no WinGet (`SaturnPCBDesign.SaturnPCBToolkit`, v8.47) | FATO-sec ([winget](https://winget.ragerworks.com/package/SaturnPCBDesign.SaturnPCBToolkit)) |
| **Broadcom AppCAD** | Calculadora RF grátis (linhas, casamento), parada na v4.0.0 há anos | FATO-sec ([broadcom.com/appcad](https://www.broadcom.com/appcad), [Hackaday](https://hackaday.com/2021/07/20/appcad-does-transmission-lines)) |
| **Calculadora de impedância da JLC** | Largura e gap para o stackup real da JLC | FATO-sec ([JLC](https://jlcpcb.com/capabilities/impedance-calculator)) |

Ordem sugerida (INFERÊNCIA): para linha de 50 Ω ou par USB 90 Ω, a calculadora da JLC com o stackup escolhido; depois Saturn para conferir. openEMS/Sonnet só para antena impressa ou transição crítica. Para antena de chip, seguir o layout de referência do fabricante, que vale mais que a simulação.

### R5. Visualização para campanha

**`kicad-cli pcb render`** (KiCad 10.0.8; FATO, `--help` local)
- Opções:
  - `--side top|bottom|left|right|front|back`;
  - `-w/--width` (1600) e `--height` (900). **`-h` está duplicado entre help e height: usar a forma longa**;
  - `--background default|transparent|opaque`;
  - `--quality basic|high|user|job_settings`;
  - `--preset`; `--use-board-stackup-colors`;
  - `--floor` (chão, sombras, pós-processamento);
  - `--perspective`; `--zoom`;
  - `--pan X,Y,Z`; `--pivot X,Y,Z` (cm); `--rotate X,Y,Z` (ex. `-45,0,45` = isométrico);
  - `--light-top/-bottom/-side/-camera` (0-1); `--light-side-elevation` (60°);
  - `--variant`; `-D var=valor`.
- Exemplo (INFERÊNCIA, montado a partir do help):
  ```
  kicad-cli pcb render placa.kicad_pcb -o hero.png --width 3840 --height 2160 \
    --quality high --floor --perspective --rotate "-35,0,30" --background transparent \
    --use-board-stackup-colors
  ```
- No MCP: `get_board_2d_view` gera a prévia 2D. **Na máquina local, a exportação de imagem que depende de `cairosvg` não funciona** (falta a DLL libcairo) (`<DEVSHARED>\README.md:38`, FATO).

**Outras ferramentas**
- **KiCad 3D viewer:** visualização interativa e raytracing no próprio KiCad. O `--quality high` do CLI usa o mesmo motor (INFERÊNCIA).
- **pcb2blender** (30350n, GPLv3): exportador no PCM do KiCad gera um `.pcb3d`, que o importador abre no Blender. A extensão do arquivo tem de ser `.pcb3d`. O Blender Extensions lista compatibilidade até o Blender 5.1. **Suporte ao KiCad 10 não confirmado** (FATO-sec, [github](https://github.com/30350n/pcb2blender), [Blender ext.](https://extensions.blender.org/add-ons/pcb3d-importer/)).
- **InteractiveHtmlBom** (openscopeproject, MIT): HTML autocontido e offline que liga a lista de peças à posição na placa, com destaque de nets opcional. CLI `generate_interactive_bom.py` para rodar sem interface. Serve para montagem manual e como material de campanha/documentação (FATO-sec, [wiki](https://github.com/openscopeproject/InteractiveHtmlBom/wiki/Usage), [PyPI](https://pypi.org/project/InteractiveHtmlBom/)).

---

## Armadilhas

| # | Armadilha | Consequência | Correção | Fonte / etiqueta |
|---|---|---|---|---|
| 1 | Usar `export_bom` do MCP para a JLC | BOM sem código LCSC e com cabeçalhos errados; a JLC não casa as peças | `export_sch_bom`/kicad-cli com `fields`/`labels`, ou o Fabrication Toolkit | `export.py:522-600`, FATO |
| 2 | Deixar o `--ref-range-delimiter` padrão (`-`) | Sai "C2,C5-C13"; a faixa não casa com o CPL e dá erro de designator | `--ref-range-delimiter ""` (MCP: `refRangeDelimiter: ""`) | Saída testada FATO; erro na JLC INFERÊNCIA |
| 3 | CPL do kicad-cli com padrão `ascii`/`in` | Coordenadas em polegada; peças fora do lugar | `--format csv --units mm` | `--help` FATO |
| 4 | Confiar na prévia de montagem da JLC | Peça polarizada girada 90/180° | Conferir o DFM, aplicar `FT Rotation Offset`, marcar pino 1 no silk | FATO-sec (FAQ/fóruns) |
| 5 | Achar que Basic é sempre grátis | Orçamento errado na Standard (US$ 1,53/feeder também nas Basic) | Ver a tabela R1.7 | FATO (price 22/10/2026) |
| 6 | Pôr `JLCJLCJLCJLC` no silk | Texto impresso à toa: a opção não existe desde 05/2026 | Não pôr; o padrão é sem marca | FATO (How to mark) |
| 7 | `route_trace`/`route_pad_to_pad` em placa cheia | Trilha reta atravessa pads e trilhas de outras redes (curto) | Só para ligações curtas e livres; `run_drc` a cada lote; o resto no `autoroute` ou à mão | `routing.py:474-700`, FATO |
| 8 | `route_trace` com nome de net digitado errado | Trilha sem net; DRC acusa e a conectividade engana | Rodar `get_nets_list` antes; sync primeiro | `routing.py:690-697`, FATO |
| 9 | Via automática do `route_pad_to_pad` | Via em cima de outra trilha ou pad | Conferir `via_position` no retorno e rodar DRC | `routing.py:562-570`, FATO |
| 10 | `route_differential_pair` achando que liga os pads | Par solto, sem casamento de comprimento | Ligar as pontas; casar comprimento no KiCad (tuning) | ROUTING_TOOLS_REFERENCE, FATO; tuning INFERÊNCIA |
| 11 | Exportar sem salvar | Gerber/CPL da versão anterior | `save_board` → exportar | `export.ts`, FATO |
| 12 | `export_gerber` (SWIG) em versão antiga | Nenhum arquivo, mas "sucesso" | Usar `export_gerbers` (kicad-cli) | CHANGELOG:466-471, FATO |
| 13 | `import_ses` falhou e o agente salvou | Trilhas não travadas perdidas | Reabrir do disco antes de salvar | FREEROUTING_GUIDE, FATO |
| 14 | `refill_zones` no backend SWIG | Segfault do worker | IPC ou abrir no KiCad; `run_drc` já preenche no KiCad 10 | KNOWN_ISSUES #2, FATO |
| 15 | Freerouting local (JAR em class major 69 = Java 25) com o JDK 21 padrão | `autoroute` cai em Docker ou falha | `JAVA_HOME` → `<DEVSHARED>\jdk25\...`; `check_freerouting` | FATO (FREEROUTING_GUIDE + bytes do JAR) |
| 16 | Snapshot `cdfer` do banco JLC | Só itens em estoque, e preço/estoque atrasados | Confirmar a peça no site ou com credenciais (`get_jlcpcb_part`) | `jlcpcb-api.ts`, FATO |
| 17 | Editar o esquemático com ele aberto no KiCad | O MCP recusa (ou o KiCad sobrescreve) | Fechar o esquemático no KiCad | README v2.9, FATO |
| 18 | Símbolo "flat" da SnapEDA/SamacSys | Todas as ferramentas skip falham na folha | `repair_flat_symbols` na lib **e** no `.kicad_sch` | HEADLESS_AUTHORING §7a, FATO |
| 19 | `suggest_placement` aplicado direto | Floorplan sem lógica de RF, borda ou térmica | Usar como sugestão (dry-run) depois do floorplan humano | `placement_optimizer.py` "DRAFT", FATO; resto INFERÊNCIA |
| 20 | Economic com peça "Standard only" ou 0201 | O pedido vira Standard (setup US$ 25,56+) | Filtrar peças compatíveis com Economic; passivo ≥ 0402 | FATO-sec |
| 21 | Misturar fontes para o mesmo part number | A JLC não aceita (estoque JLC × consignado/global) | Uma fonte por part number | FATO-sec |
| 22 | `kicad-cli pcb render -h 1080` | Mostra o help em vez de definir a altura | `--height 1080` | `--help` FATO |
| 23 | OpenSCAD 2021.01 com STEP | Não importa | DXF (Edge.Cuts) ou STL | FATO (manual + versão) |
| 24 | Contar com o StepUp no FreeCAD 1.1 local | Não está instalado; suporte declarado só até 1.0 | Instalar e testar; senão, STEP pelo kicad-cli e Part workbench | FATO (`ls`, README do StepUp) |
| 25 | Furo de insert copiado de uma tabela genérica | Insert solto ou parede rachada | Desenho do fabricante do insert + corpo de prova | FATO-sec (fontes divergem) |

---

## Checklist de pedido

**Antes de exportar**
- [ ] ERC na folha raiz com 0 erros; warnings triados (HEADLESS_AUTHORING §4).
- [ ] `sync_schematic_to_board` feito depois da última edição do esquemático.
- [ ] Todo símbolo montado tem o campo `LCSC` (ou `JLCPCB Part #`); DNP marcado.
- [ ] Peças conferidas no site da JLC (estoque ao vivo; Basic / Preferred / Extended), não só no snapshot local.
- [ ] Economic ou Standard decidido: só passivos ≥ 0402, montagem numa face, nenhuma peça "Standard only" (se Economic).
- [ ] Pino 1 / polaridade marcados no silk de toda peça polarizada.
- [ ] `run_drc` com 0 violações, 0 itens não conectados, 0 problemas de paridade (KiCad 10 já preenche as zonas).
- [ ] Se houve round-trip com Freerouting: `audit_via_nets` contra a revisão anterior.
- [ ] `save_board`.

**Exportar**
- [ ] Gerber + drill (`export_gerbers` + `export_drill`, ou Fabrication Toolkit) zipados; conferidos num visualizador de Gerber.
- [ ] BOM JLC: `Comment, Designator, Footprint, JLCPCB Part #`; sem faixas "R1-R5"; ≤ 200 designators por linha; sem DNP.
- [ ] CPL: `Designator, Mid X, Mid Y, Layer, Rotation`; mm; topo e fundo no mesmo arquivo; designators idênticos aos do BOM.
- [ ] **INFERÊNCIA (regra global do dono):** pacote de fabricação em `saida/<plataforma>/<projeto>-<versao>.<ext>`, seguido de `python "<BRANDING>\ferramentas\coletar_saida.py" .` (`%USERPROFILE%\.claude\CLAUDE.md`, seção "builds sempre em saida/"). Supõe que a regra também cobre o pacote Gerber/BOM/CPL.

**No site da JLC**
- [ ] Camadas, dimensões e quantidade conferidas com o Gerber detectado.
- [ ] Espessura (padrão 1,6 mm; casar com o SMA de borda e com o conector de host).
- [ ] Acabamento: ENIG para QFN/BGA fino, borda metalizada, ≤ 0,4 mm ou 6+ camadas; HASL sem chumbo para o resto (regras R1.9; escolha = INFERÊNCIA).
- [ ] Impedância controlada marcada, com o stackup escolhido igual ao usado no cálculo (4+ camadas).
- [ ] Cobertura de via escolhida (plugged / epoxy / padrão), coerente com via-in-pad.
- [ ] Cor (preto/branco: ponte de máscara mínima 0,13 mm).
- [ ] Marca: deixar "sem marca" (order number não existe mais desde 05/2026).
- [ ] PCBA: lado de montagem, Economic/Standard, quantidade montada.
- [ ] BOM/CPL enviados: nenhuma peça "unmatched"; cada rotação conferida no visualizador/DFM; offsets aplicados e reenviados se preciso.
- [ ] Peças My Parts Lib, pré-compra ou consignadas: selecionadas, sem misturar fontes no mesmo part number.
- [ ] Prazo esperado: PCB de 2 camadas em 24 h, 4 camadas em 2-5 dias; mais 24-48 h de PCBA; Global Sourcing soma 9-15 dias.

**Depois**
- [ ] Ao confirmar o pedido ou receber a placa: apagar os artefatos de `saida/` conforme a regra global de ciclo de vida (FATO: `%USERPROFILE%\.claude\CLAUDE.md`).

---

## Bibliografia/URLs

**JLCPCB (primárias; datas das páginas onde visíveis)**
- KiCad 8 BOM/CPL: https://jlcpcb.com/help/article/how-to-generate-bom-and-centroid-files-from-kicad-8
- Pick & Place (CPL), 09/09/2026: https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly
- Recomendações BOM/CPL, 09/09/2026: https://jlcpcb.com/help/article/advice-for-bom-and-cpl-files-preparation
- Preço PCBA, 22/10/2026: https://jlcpcb.com/help/article/pcb-assembly-price
- FAQ PCBA, 09/09/2026: https://jlcpcb.com/help/article/pcb-assembly-faqs
- FAQ PCBA parte 2 (rotação): https://jlcpcb.com/help/article/pcb-assembly-faqs-part-2
- After-sales FAQ: https://jlcpcb.com/help/article/common-pcba-after-sales-issues-and-faq
- Capacidades PCB: https://jlcpcb.com/capabilities/pcb-capabilities
- Capacidades PCBA: https://jlcpcb.com/capabilities/pcb-assembly-capabilities
- Prazo de fabricação, 10/11/2026: https://jlcpcb.com/help/article/pcb-fabrication-services-and-production-time
- Marcação (order number), 22/05/2026: https://jlcpcb.com/help/article/How-to-mark-on-PCB
- Biblioteca própria / pré-compra: https://jlcpcb.com/help/article/how-to-build-your-own-parts-library-in-jlcpcb
- Global Sourcing: https://jlcpcb.com/help/article/global-sourcing-parts-order-terms-conditions
- Consignadas: https://jlcpcb.com/help/article/consignment-part-terms-conditions
- Calculadora de impedância: https://jlcpcb.com/capabilities/impedance-calculator
- Stackups: https://jlcpcb.com/help/article/multi-layer-pcb-standard-laminated-structures
- Peças "Standard only" (terceiro): https://techoverflow.net/2024/04/10/jlcpcb-pcb-assembly-list-of-known-standard-only-parts/

**Plugins KiCad**
- JLCPCB Fabrication Toolkit (bennymeg): https://github.com/bennymeg/Fabrication-Toolkit
- InteractiveHtmlBom: https://github.com/openscopeproject/InteractiveHtmlBom/wiki/Usage
- pcb2blender: https://github.com/30350n/pcb2blender · https://extensions.blender.org/add-ons/pcb3d-importer/

**Outras fábricas**
- PCBWay, arquivos: https://www.pcbway.com/assembly-file-requirements.html
- PCBWay, capacidades: https://www.pcbway.com/assembly-capabilities.html
- Aisler, placas: https://aisler.net/products/boards

**KiCAD-MCP-Server (local)**
- `MCP\README.md` (v2.9.0; seções Toolboxes, Operating modes, Available Tools)
- `MCP\CHANGELOG.md` (linhas 7-105, 200-215, 325-340, 466-485, 1387, 1925-1937, 2600-2652)
- `MCP\docs\KNOWN_ISSUES.md`, `FREEROUTING_GUIDE.md`, `ROUTING_TOOLS_REFERENCE.md`, `HEADLESS_AUTHORING.md`, `JLCPCB_USAGE_GUIDE.md`, `JLCPCB_INTEGRATION.md`, `TOOL_INVENTORY.md` (inventário completo, não lido inteiro)
- `MCP\src\tools\routing.ts`, `freerouting.ts`, `component.ts`, `schematic.ts`, `design-rules.ts`, `export.ts`, `tool-aliases.ts`, `jlcpcb-api.ts`
- `MCP\python\commands\routing.py`, `export.py`, `placement_optimizer.py`
- `<DEVSHARED>\README.md` linhas 37-40 (KiCad 10.0.8, FreeCAD, OpenSCAD, MCP, Freerouting 2.5.0, JDK 25)
- Repositório upstream (citado no próprio README): https://github.com/mixelpixx/KiCAD-MCP-Server

**Mecânica**
- kicadStepUpMod: https://github.com/easyw/kicadStepUpMod
- OpenSCAD, importação: https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Importing_Geometry
- Hubs, carcaça impressa: https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/
- UAL, folgas: https://wiki.cci.arts.ac.uk/books/digital-fabrication-lab/page/design-the-clearance-and-tolerance
- Aisler community, tolerância PCB × 3D: https://community.aisler.net/t/tolerance-management-between-pcb-and-3d-printing/5540
- Inserts: https://medesignlab.me.wisc.edu/?p=162 · https://accu-components.com/p/488-threaded-insert-hole-size-charts-for-3d-printing-pla-petg-resin · https://www.digikey.com/es/maker/tutorials/2025/intro-to-freecad-part-4-how-to-use-heat-set-inserts
- Light pipe: https://bivar.com/resources/light-pipe-faqs/?amp=1 · https://resources.altium.com/p/light-pipes-explained
- USB-C overmold (fórum): https://forum.digikey.com/t/overmold-size-of-the-usb-c-male-end/70874
- SMA: https://www.we-online.com/components/products/datasheet/60332042111504.pdf · https://www.adafruit.com/products/1865

**Simulação**
- KiCad + ngspice: https://kicad.org/discover/spice
- openEMS: https://docs.openems.de/intro.html
- Qucs-S com openEMS: https://openems.readthedocs.io/en/latest/concepts/postproc/qucs.html
- Sonnet Lite: https://sonnetsoftware.com/products/lite/download.html
- Saturn PCB Toolkit: https://winget.ragerworks.com/package/SaturnPCBDesign.SaturnPCBToolkit
- AppCAD: https://www.broadcom.com/appcad · https://hackaday.com/2021/07/20/appcad-does-transmission-lines

**Lacunas desta pesquisa** (não preenchidas; precisam de fonte)
- Cabeçalho exato do template oficial de BOM/CPL da JLC: a seção está em imagem e eu não baixei o arquivo de exemplo.
- Via "tented/untented" como opção atual do pedido da JLC: a página de capacidades lista só plugged, epoxy e copper-filled.
- Stackup `JLC04161H-7628` e Dk atual: as fontes divergem (7628 = 4,4 ou 4,6).
- Se cor diferente de verde ou ENIG aumentam o prazo: não informado.
- Envelope de overmold USB-C pela USB-IF; guia de recorte para microSD push-push.
- Tabela oficial CNC Kitchen/Ruthex para inserts M2/M2.5.
- pcb2blender com KiCad 10 e StepUp com FreeCAD 1.1: sem confirmação.
- Se o importador da JLC aceita o Y negativo e o `bottom` minúsculo do CPL do kicad-cli.
