# 08 — Ferramentas: KiCad 10, kicad-cli, regras customizadas, Freerouting e ecossistema

> Pesquisa de 2026-11-21, feita na máquina do dono: Windows 11, **KiCad 10.0.8** em `%USERPROFILE%\AppData\Local\Programs\KiCad\10.0\bin`.
> **Etiquetas:**
> - **FATO**: conferido na fonte lida (URL ao lado) ou por teste local reproduzível.
> - **FATO (`--help` 10.0.8)**: sintaxe copiada da saída de `kicad-cli … --help` desta instalação em 2026-11-21. A referência oficial é <https://docs.kicad.org/10.0/en/cli/cli.html>.
> - **FATO (teste local)**: comando executado numa **cópia** do demo `stickhub` do KiCad, no scratchpad da sessão. Nenhum projeto do dono foi tocado.
> - **URL de referência dos testes locais:** comandos do CLI → <https://docs.kicad.org/10.0/en/cli/cli.html>; DSN/SES, regras e netclasses → <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html>; API Python → <https://dev-docs.kicad.org/en/apis-and-binding/pcbnew/>. Quando a linha diz só "FATO (teste local)", vale a URL do assunto correspondente.
> - **INFERÊNCIA**: dedução ou prática comum sem fonte primária lida.
> - **NÃO VERIFICADO**: visto só em resumo de busca, sem abrir a página.
>
> Ferramentas de terceiros (KiKit, Fabrication Toolkit, kicad-jlcpcb-tools, iBOM, StepUp, pcb2blender) **não foram executadas**: a sintaxe delas vem da documentação de cada uma. O Freerouting foi executado.

---

## Resumo

1. **Estado do KiCad 10 (lançado em 2026-03).** As novidades que mais pesam no layout são estas:
   - editor gráfico de regras de DRC (gera regras compatíveis com a linguagem de Custom Rules);
   - correções sugeridas para erros de DRC;
   - tuning de comprimento refeito, com **Tuning Profiles** por camada (impedância-alvo, largura e gap calculados pelo stackup) e **tuning no domínio do tempo** (atraso de propagação);
   - **Design Blocks** também no editor de PCB;
   - objetos em camadas internas dentro de footprints;
   - troca de pino/porta (pin/gate swap) com anotação nos dois sentidos;
   - **variantes de projeto**, com `--variant` em todos os exports de PCB;
   - importadores de Allegro, PADS e gEDA/Lepton.

   **FATO**: <https://www.kicad.org/blog/2026/03/Version-10.0.0-Released/>. Detalhes de tuning profiles e variantes: <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html>.
2. **O que veio antes, no KiCad 9 e ainda vale.** **FATO**: <https://www.kicad.org/blog/2025/02/Version-9.0.0-Released/>
   - jobsets;
   - IPC API;
   - gerenciador de zonas;
   - padstacks por camada;
   - component classes;
   - DRC de creepage;
   - export ODB++;
   - várias netclasses por net.
3. **API Python: a SWIG `pcbnew` funciona no 10, mas está depreciada.** Ao importar, ela emite `DeprecationWarning: The SWIG-based Python interface to the PCB editor is deprecated and will be removed in a future version of KiCad.` (**FATO**, teste local). A remoção está planejada para o **KiCad 11.0** (**FATO**: <https://dev-docs.kicad.org/en/apis-and-binding/pcbnew/>).
   - **IPC API (pacote `kicad-python`, import `kipy`):** no 9 e no 10 só conversa com a **GUI aberta**, só existe no editor de PCB, e **não plota nem exporta**. Modo headless e export chegam no 11 (**FATO**: <https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/for-addon-developers/>).
   - O Python do KiCad 10.0.8 já traz `kicad-python 0.8.0` (**FATO**, `pip show` local).
   - **Conclusão para automação hoje:** `kicad-cli` para tudo que é export, DRC e ERC; SWIG `pcbnew` para edição em lote sem GUI (enquanto durar); `kipy` só para plugin com a GUI aberta. **INFERÊNCIA** a partir das três fontes.
4. **kicad-cli 10.0.8.** Subcomandos: `fp`, `jobset`, `pcb`, `sch`, `sym`, `version`.
   - `pcb export`: 3dpdf, brep, drill, dxf, gencad, gerbers, glb, ipc2581, ipcd356, odb, pdf, ply, pos, ps, stats, step, stl, stpz, svg, u3d, vrml, xao.
   - O **HPGL** do `pcb export` diz "No longer supported as of KiCad 10.0".
   - **Não existe export de Specctra DSN no kicad-cli.** Ele existe na GUI (File → Export → Specctra DSN) e na API SWIG (`pcbnew.ExportSpecctraDSN`).

   **FATO (`--help` 10.0.8)** + <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html> (seções "Specctra DSN" e "Importing Specctra session files").
5. **Regras customizadas (`.kicad_dru`):**
   - cabeçalho `(version 1)`; as regras são avaliadas **de baixo para cima** (a última que casa vence);
   - no KiCad 10, `insideArea()` e `insideCourtyard()` estão **depreciadas**: use `intersectsArea()` e `intersectsCourtyard()`;
   - há função nova `fromTo('U1-A5','U2-B3')` para restringir comprimento e skew a um trecho da net.

   **FATO**: <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html> (Custom design rules). O arquivo-exemplo JLC desta página foi **validado pelo DRC do 10.0.8** (FATO, teste local). **Cuidado:** um `.kicad_dru` com erro de sintaxe é **ignorado em silêncio** pelo `kicad-cli pcb drc` (FATO, teste local; armadilha 33).
6. **Freerouting v2.5.0 (2026-10-05):**
   - o round-trip DSN→SES funciona no KiCad 10.0.8 (FATO, teste local);
   - o DSN exportado **leva** zonas (como `plane`), keepouts de trilha/via (como `keepout`) e **todas as netclasses** com largura, isolação e via;
   - **não leva** as regras do `.kicad_dru`, o gap de par diferencial, nem o nome da rule area (FATO, teste local).
   - Os flags curtos `-mp`, `-mt`, `-inc` e `-dr` estão **depreciados** em favor de `--router.autorouter.*`. O `-help` embutido no jar ainda lista opções removidas.

   **FATO**: <https://github.com/freerouting/freerouting/blob/master/docs/command_line_arguments.md>, <https://github.com/freerouting/freerouting/releases/tag/v2.5.0>
7. **Ecossistema e KiCad 10:**

   | Ferramenta | Situação no KiCad 10 | Fonte (**FATO**) |
   |---|---|---|
   | KiKit 1.8.0+ | suporte declarado ao KiCad 10 | <https://github.com/yaqwsx/KiKit/releases/tag/v1.8.0> |
   | kicad-jlcpcb-tools | badge v10 e recursos de variantes | <https://github.com/Bouni/kicad-jlcpcb-tools> |
   | Fabrication Toolkit 5.3.1 | correções para o KiCad 10 | <https://github.com/bennymeg/Fabrication-Toolkit/releases/tag/5.3.1> |
   | iBOM 2.12.0 | QR/barcode e texto knockout do KiCad 10 | <https://github.com/openscopeproject/InteractiveHtmlBom/releases/tag/v2.12.0> |
   | KiCad StepUp | KiCad 10.x listado | <https://github.com/easyw/kicadStepUpMod> |
   | **pcb2blender** | **ainda sem release para o 10**: o último release é `v2.17.5-k9.0-b5.1` e o PR "Support KiCad 10" #140 está aberto | <https://github.com/30350n/pcb2blender/pull/140> |
8. **Mínimos da JLCPCB (2 camadas, 1 oz):**
   - trilha/espaço: 0,10/0,10 mm;
   - via: furo de 0,15 mm, diâmetro de 0,25 mm;
   - furo-a-furo: via 0,20 mm, pad 0,45 mm;
   - furo de via a trilha: 0,20 mm; PTH a trilha: 0,28 mm;
   - NPTH: ≥ 0,50 mm;
   - cobre à borda fresada: 0,20 mm (0,40 mm no V-cut);
   - silk: traço ≥ 0,15 mm, texto ≥ 1,0 mm, 0,15 mm do pad.

   **FATO**: <https://jlcpcb.com/capabilities/pcb-capabilities> (lida em 2026-11-21).

---

## Receitas prontas

> Todos os blocos usam o Git Bash do Windows com caminho completo, porque o `kicad-cli` **não está no PATH** desta máquina (FATO, `which kicad-cli` vazio). No PowerShell, troque por `& "%USERPROFILE%\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe" …`.

```bash
K="~/AppData/Local/Programs/KiCad/10.0/bin/kicad-cli.exe"
PY="~/AppData/Local/Programs/KiCad/10.0/bin/python.exe"   # tem import pcbnew e kipy
```

### 1. ERC e DRC em JSON (gate de entrega)
**FATO (`--help` 10.0.8)**; os dois comandos foram executados com sucesso (FATO, teste local).
```bash
"$K" sch erc --format json --severity-all --units mm --exit-code-violations -o saida/erc.json placa.kicad_sch
"$K" pcb drc --format json --severity-all --schematic-parity --units mm \
     --refill-zones --exit-code-violations -o saida/drc.json placa.kicad_pcb
```
- Com `--exit-code-violations`, a saída é **0** quando não há violação e **5** quando há (FATO: <https://docs.kicad.org/10.0/en/cli/cli.html>; FATO, teste local: `exit=5`).
- O JSON do DRC traz `violations`, `unconnected_items` e `schematic_parity`. O do ERC traz `sheets[].violations` (FATO, teste local).
- `--refill-zones` sozinho **não grava** a placa. Para gravar é preciso `--save-board`, que só vale junto com `--refill-zones` (FATO, `--help`).
- Outras opções do DRC: `--all-track-errors` e `--severity-exclusions` (FATO, `--help`).

Leitura rápida do resultado (Python comum):
```bash
python -c "import json;d=json.load(open('saida/drc.json'));print(len(d['violations']),len(d['unconnected_items']),len(d['schematic_parity']))"
```

### 2. Gerbers para fábrica (só as camadas que a fábrica usa)
**FATO (`--help` 10.0.8)**; executado (FATO, teste local).
```bash
"$K" pcb export gerbers --layers "F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts" \
     --subtract-soldermask --check-zones -o saida/fab/gerber/ placa.kicad_pcb
# 4 camadas: acrescente In1.Cu,In2.Cu em --layers
# Alternativa: usar o que está configurado no diálogo de plot da placa
"$K" pcb export gerbers --board-plot-params -o saida/fab/gerber/ placa.kicad_pcb
```
- Saem extensões Protel: `.gtl`, `.gbl`, `.gto`, `.gts`, `.gtp`, `Edge_Cuts.gm1`, e um `-job.gbrjob` (FATO, teste local).
- Se preferir as extensões do KiCad, use `--no-protel-ext`.
- Outras opções: `--precision 5|6` (padrão 6), `--no-x2`, `--no-netlist`, `--use-drill-file-origin` (FATO, `--help`).

### 3. Furação Excellon com PTH e NPTH separados
**FATO (`--help` 10.0.8)**; executado: gerou `-PTH.drl` e `-NPTH.drl` (FATO, teste local).
```bash
"$K" pcb export drill --format excellon --excellon-units mm --excellon-separate-th \
     --excellon-zeros-format decimal --excellon-oval-format alternate \
     --generate-map --map-format gerberx2 -o saida/fab/gerber/ placa.kicad_pcb
```
- Opções: `--drill-origin absolute|plot`, `--excellon-mirror-y`, `--excellon-min-header`, `--generate-report --report-path`, `--generate-tenting`, `--format gerber` (FATO, `--help`).

### 4. Arquivo de posição (CPL) em CSV e mm
**FATO (`--help` 10.0.8)**; executado (FATO, teste local).
```bash
"$K" pcb export pos --format csv --units mm --side both --exclude-dnp -o saida/fab/placa-pos.csv placa.kicad_pcb
```
- O cabeçalho gerado é `Ref,Val,Package,PosX,PosY,Rot,Side` (FATO, teste local). A JLC espera `Designator, Mid X, Mid Y, Rotation, Layer` em mm: renomeie Ref→Designator, PosX→Mid X, PosY→Mid Y, Rot→Rotation, Side→Layer (FATO: <https://jlcpcb.com/help/article/81-How-to-generate-the-BOM-and-Centroid-file-from-KiCAD>).
- **Rotação:** o export nativo **não corrige** a rotação para a JLC. Use as correções do kicad-jlcpcb-tools ou do Fabrication Toolkit, ou ajuste no visualizador da JLC (FATO, mesmo artigo).
- Outras opções: `--smd-only`, `--exclude-fp-th`, `--bottom-negate-x`, `--use-drill-file-origin`, `--variant` (FATO, `--help`).

### 5. BOM (formato JLC, sem faixas de referência)
**FATO (`--help` 10.0.8)**; executado (FATO, teste local).
```bash
"$K" sch export bom --fields 'Reference,Value,Footprint,${QUANTITY},LCSC' \
     --labels 'Designator,Comment,Footprint,Quantity,LCSC Part #' \
     --group-by 'Value,Footprint' --ref-range-delimiter '' --exclude-dnp \
     -o saida/fab/placa-bom.csv placa.kicad_sch
```
- Sem `--ref-range-delimiter ''`, o BOM agrupa em faixas (`C2,C5-C13`). Com ele, lista cada referência (`C2,C5,C6,…`) (FATO, teste local).
- Colunas mínimas da JLC: Comment, Designator, Footprint e "JLCPCB / LCSC Part #" (FATO: artigo 81 acima).
- Troque `LCSC` pelo nome real do campo no seu esquemático. INFERÊNCIA.
- Também há `--preset` e `--format-preset` para usar presets salvos no esquemático (FATO, `--help`).

### 6. IPC-2581 e ODB++
**FATO (`--help` 10.0.8)**; os dois foram executados (FATO, teste local).
```bash
"$K" pcb export ipc2581 --version C --units mm --compress \
     --bom-col-mfg-pn MPN --bom-col-dist-pn LCSC -o saida/fab/placa-ipc2581.xml placa.kicad_pcb
"$K" pcb export odb --units mm --compression zip --check-zones -o saida/fab/placa-odb.zip placa.kicad_pcb
```

### 7. STEP (carcaça), render 3D, PDF e SVG
**FATO (`--help` 10.0.8)**; todos executados (FATO, teste local).
```bash
"$K" pcb export step --subst-models --include-tracks --no-dnp -f -o saida/3d/placa.step placa.kicad_pcb
"$K" pcb render --side top --quality high --width 1920 --height 1080 -o saida/render/top.png placa.kicad_pcb
"$K" pcb render --rotate '-45,0,45' --perspective --floor -o saida/render/iso.png placa.kicad_pcb
"$K" pcb export pdf --layers "F.Cu,F.Silkscreen,Edge.Cuts" --mode-single -o saida/doc/top.pdf placa.kicad_pcb
"$K" pcb export svg --layers "F.Cu,Edge.Cuts" --mode-single --fit-page-to-board -o saida/doc/top.svg placa.kicad_pcb
"$K" sch export pdf -o saida/doc/esquematico.pdf placa.kicad_sch
```
- Opções do STEP: `--board-only`, `--no-components`, `--component-filter "J*,U1"`, `--include-zones`, `--include-silkscreen`, `--include-soldermask`, `--user-origin 0x0mm`, `--drill-origin`, `--grid-origin` (FATO, `--help`).
- Opções do render: `--side top|bottom|left|right|front|back`, `--background transparent|opaque`, `--quality basic|high|user|job_settings`, `--preset`, `--use-board-stackup-colors`, `--zoom`, `--pan`, `--pivot`, `--light-*` (FATO, `--help`).

### 8. Variáveis e variantes
**FATO (`--help` 10.0.8)** + <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html> (Command-line variant support).
```bash
# -D / --define-var KEY=VALUE: acrescenta ou sobrescreve variável de projeto (repetível)
"$K" pcb export gerbers -D REV=B -D DATA=2026-11-21 --layers "F.Cu,B.Cu,Edge.Cuts" -o saida/fab/gerber/ placa.kicad_pcb
# Variantes: --variant repetível; ${VARIANT} no caminho gera uma pasta por variante
"$K" pcb export gerbers --variant "WiFi-only" --variant "WiFi-BT" -o 'gerbers_${VARIANT}/' placa.kicad_pcb
```
- Quem aceita `-D`: drc, erc, gerbers, pdf, svg, step, ipc2581, odb, render e sch pdf.
- Quem **não** aceita: `pcb export drill`, `pcb export pos`, `sch export bom` e `sch export netlist` (FATO, `--help`).
- Em `.kicad_dru`, `${var}` é resolvido antes da avaliação, então dá para ter `(min ${hv_clearance})` (FATO: manual 10, Custom design rules).

### 9. Jobsets
**FATO (`--help` 10.0.8)** + <https://docs.kicad.org/10.0/en/cli/cli.html>
```bash
"$K" jobset run --file saida.kicad_jobset --stop-on-error placa.kicad_pro       # roda todas as destinations
"$K" jobset run --file saida.kicad_jobset --output "<descrição ou ID>" placa.kicad_pro
```
- O argumento posicional é o **projeto** (`.kicad_pro`).
- Sem `--output`, todas as destinations são geradas e os IDs delas são impressos.
- Sem `--stop-on-error`, a execução continua depois de uma falha.
- O jobset é criado na GUI do gerenciador de projetos (introduzido no KiCad 9: <https://www.kicad.org/blog/2025/02/Version-9.0.0-Released/>).
- **Não testado aqui:** nenhum `.kicad_jobset` existe nos demos instalados.
- Há relatos de segfault do `jobset run` pelo CLI no 10.0.3 (NÃO VERIFICADO: <https://gitlab.com/kicad/code/kicad/-/issues/24474>).
- **Recomendação:** um script com os comandos 1–7 é mais transparente que um jobset. INFERÊNCIA.

### 10. Python `pcbnew` (SWIG) no Windows — operações úteis
**FATO (teste local)**: todas estas chamadas rodaram no `python.exe` do KiCad 10.0.8. As assinaturas vêm das docstrings: `LoadBoard(wxString aFileName)`, `SaveBoard(wxString aFileName, BOARD aBoard, bool aSkipSettings=False)`, `ZONE_FILLER.Fill(ZONES aZones, bool aCheck=False, …)`, `ExportSpecctraDSN(BOARD, wxString)`, `ImportSpecctraSES(BOARD, wxString)`, `WriteDRCReport(BOARD, wxString, EDA_UNITS, bool)`. Doxygen: <https://docs.kicad.org/doxygen-python-10.0/namespaces.html>.
```python
# rodar com: "$PY" -I -W ignore script.py placa.kicad_pcb saida.kicad_pcb
import sys, pcbnew
src, dst = sys.argv[1], sys.argv[2]
b = pcbnew.LoadBoard(src)                       # lê também o .kicad_pro ao lado (netclasses)
print("pads", sum(1 for _ in b.GetPads()), "trilhas+vias", len(b.GetTracks()), "zonas", b.GetAreaCount())
for t in b.GetTracks():
    if isinstance(t, pcbnew.PCB_VIA):
        print("via", t.GetNetname(), pcbnew.ToMM(t.GetWidth()), pcbnew.ToMM(t.GetDrillValue()))
    else:
        print("trilha", t.GetNetname(), pcbnew.ToMM(t.GetWidth()))
fp = b.FindFootprintByReference("U1")
print("U1 em mm", pcbnew.ToMM(fp.GetPosition().x), pcbnew.ToMM(fp.GetPosition().y))
net = b.FindNet("+5V"); print("netclass", net.GetNetClassName())
# remover rota: use Delete (Remove dentro do loop gerou centenas de avisos 'memory leak' e o script não chegou a salvar)
# for t in list(b.GetTracks()): b.Delete(t)
pcbnew.ZONE_FILLER(b).Fill(b.Zones())           # refill antes de salvar/DRC
pcbnew.SaveBoard(dst, b)                        # grava também <dst>.kicad_pro e .kicad_prl
pcbnew.ExportSpecctraDSN(b, dst.replace(".kicad_pcb", ".dsn"))
```
- Unidades: a interna é **nanômetro** (inteiros). Converta com `pcbnew.FromMM(x)` e `pcbnew.ToMM(n)` (FATO, teste local). Nas regras customizadas, um número sem sufixo também é lido em nm (FATO: manual 10, Custom design rules).

### 11. IPC API (`kipy`): só com a GUI aberta
**FATO**: <https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/for-addon-developers/>. Métodos listados por `dir()` no `kipy` local (FATO, teste local). **Não executado** contra uma GUI aberta.
```python
from kipy import KiCad
k = KiCad()                 # conecta na instância aberta (KICAD_API_SOCKET/KICAD_API_TOKEN quando lançado pelo KiCad)
b = k.get_board()
print(len(b.get_footprints()), len(b.get_tracks()), len(b.get_vias()))
b.refill_zones(); b.save()
```
- Outros métodos de `Board`: `get_nets`, `get_items_by_net`, `get_items_by_netclass`, `get_stackup`, `get_zones`, `create_items`, `update_items`, `remove_items`, `begin_commit` e `push_commit` (FATO, teste local).

### 12. Freerouting (DSN → SES) sem GUI
**FATO (teste local)**: ciclo completo executado. Uma placa demo com a rota removida foi exportada para DSN (86 KB) e roteada com 5 passes em 34 s, gerando um SES de 43 KB. `ImportSpecctraSES` devolveu True e trouxe 525 trilhas/vias; refill e save funcionaram. A placa (a cópia do demo, no scratchpad) foi gravada com `SaveBoard` e conferida com `kicad-cli pcb drc`.
```bash
# Java: o jar 2.5.0 desta máquina roda com o JDK 25 (ver <DEVSHARED>\README.md)
J="/e/DevShared/jdk25/jdk-25.0.5+8/bin/java"
"$J" -jar ~/.kicad-mcp/freerouting.jar -de placa.dsn -do placa.ses \
     --router.autorouter.max_passes=50 --gui.enabled=false
# forma antiga (ainda aceita, depreciada): -de placa.dsn -do placa.ses -mp 50
# ignorar netclasses (ex.: planos roteados à mão):
#   --router.autorouter.ignore_net_classes=GND,Power      (antigo: -inc GND,Power)
# rodar só na 2ª camada: --router.layers.routable=false,true
# relatório de DRC em JSON (formato KiCad): -drc placa_fr_drc.json   (documentado, não testado; ausente do -help do jar)
```
Depois, de volta no KiCad: `pcbnew.ImportSpecctraSES(board, "placa.ses")`, depois `ZONE_FILLER` e `SaveBoard`, e por fim `kicad-cli pcb drc` (receita 1).
- Flags documentados: `-de` (aceita `dsn+rules` com `+`), `-do` (.dsn/.ses/.scr), `-drc`, `--router.max_threads`, `--router.optimizer.enabled`, `--router.optimizer.improvement_threshold`, `--router.optimizer.item_selection_strategy=sequential|prioritized`, `-l en|de|zh`, `--user_data_path=`, `--api_server.*` (FATO: <https://github.com/freerouting/freerouting/blob/master/docs/command_line_arguments.md>).

### 13. Exemplo de `.kicad_dru` com os mínimos da JLCPCB (2 camadas, 1 oz)
**FATO (teste local):** este arquivo, gravado como `<projeto>.kicad_dru` ao lado de uma cópia do demo, **foi aceito sem erro de sintaxe pelo DRC do 10.0.8**. As regras dispararam como esperado: texto de silk < 1,0 mm, traço < 0,15 mm e `track_width` da netclass Power. Os números vêm de <https://jlcpcb.com/capabilities/pcb-capabilities> (lida em 2026-11-21). As funções e restrições vêm de <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html> (Custom design rules).

**Vale só para 1–2 camadas e 1 oz.** Para multicamada a JLC dá 0,09/0,09 mm de trilha/espaço, anel PTH mínimo de 0,15 mm e fenda metalizada de 0,35 mm. Para 2 oz: trilha/espaço de 0,16 mm em 2 camadas e 0,15 mm em multicamada, anel de 0,254 mm.
```lisp
(version 1)
# JLCPCB 1-2 camadas, 1 oz. Avaliacao de baixo para cima: o mais especifico no fim.

(rule "JLC trilha minima"      (constraint track_width (min 0.10mm)))
(rule "JLC isolacao minima"    (constraint clearance (min 0.10mm)))

(rule "JLC furo minimo e maximo" (constraint hole_size (min 0.15mm) (max 6.3mm)))
(rule "JLC NPTH minimo"
    (condition "!A.isPlated()")
    (constraint hole_size (min 0.50mm)))
(rule "JLC fenda metalizada minima"
    (condition "A.isPlated() && A.Hole_Size_X != A.Hole_Size_Y")
    (constraint hole_size (min 0.50mm)))
(rule "JLC fenda nao metalizada minima"
    (condition "!A.isPlated() && A.Hole_Size_X != A.Hole_Size_Y")
    (constraint hole_size (min 1.0mm)))

(rule "JLC via diametro minimo"
    (condition "A.Type == 'Via'")
    (constraint via_diameter (min 0.25mm))
    (constraint annular_width (min 0.05mm)))
(rule "JLC anel de PTH (minimo absoluto 2L 1oz)"
    (condition "A.Type == 'Pad' && A.isPlated()")
    (constraint annular_width (min 0.18mm)))

(rule "JLC furo a furo com pad"
    (condition "A.Type == 'Pad' || B.Type == 'Pad'")
    (constraint hole_to_hole (min 0.45mm)))
(rule "JLC furo a furo via-via"
    (condition "A.Type == 'Via' && B.Type == 'Via'")
    (constraint hole_to_hole (min 0.20mm)))

(rule "JLC furo de via a cobre"
    (condition "A.Type == 'Via'")
    (constraint hole_clearance (min 0.20mm)))
(rule "JLC furo de PTH a cobre"
    (condition "A.Type == 'Pad' && A.isPlated()")
    (constraint hole_clearance (min 0.28mm)))
(rule "JLC NPTH a cobre"
    (condition "A.Pad_Type == 'NPTH, mechanical' && (B.Type == 'Track' || B.Type == 'Via' || B.Type == 'Zone')")
    (constraint physical_hole_clearance (min 0.20mm)))

# V-cut: usar 0.40mm
(rule "JLC cobre a borda" (constraint edge_clearance (min 0.20mm)))

(rule "JLC pad SMD a pad SMD"
    (severity warning)
    (condition "A.Pad_Type == 'SMD' && B.Pad_Type == 'SMD'")
    (constraint clearance (min 0.15mm)))

(rule "JLC texto de serigrafia"
    (layer "F.Silkscreen")
    (constraint text_height (min 1.0mm))
    (constraint text_thickness (min 0.15mm)))
(rule "JLC texto de serigrafia (verso)"
    (layer "B.Silkscreen")
    (constraint text_height (min 1.0mm))
    (constraint text_thickness (min 0.15mm)))
(rule "JLC serigrafia a pad"
    (condition "B.Type == 'Pad'")
    (constraint silk_clearance (min 0.15mm)))

# --- exemplos de condição (ajustar nomes ao projeto) ---
# A.NetClass casa qualquer netclass da lista da net; opt = largura padrao do roteador interativo
(rule "Potencia largura"
    (condition "A.NetClass == 'Power'")
    (constraint track_width (min 0.40mm) (opt 0.50mm)))
(rule "HV isolacao"
    (condition "A.hasNetclass('HV')")
    (constraint clearance (min 1.5mm)))
# insideArea() ainda existe, mas esta depreciada no 10
(rule "Area RF sem vias"
    (condition "A.intersectsArea('RF_KEEPOUT')")
    (constraint disallow via))
# opt do gap = usado pelo roteador de par diferencial
(rule "USB par diferencial"
    (condition "A.inDiffPair('/USB_D')")
    (constraint diff_pair_gap (min 0.10mm) (opt 0.15mm) (max 0.25mm))
    (constraint diff_pair_uncoupled (max 3mm)))
(rule "Pontos de teste afastados"
    (condition "A.Reference == 'TP*' && B.Reference == 'TP*'")
    (constraint courtyard_clearance (min 1.0mm)))
```
Notas sobre o arquivo:
- **Comentário só em linha própria.** O manual define comentário como "qualquer linha que começa com `#`" (FATO: manual 10). Teste local: com `#` no **fim** de uma linha de regra, o arquivo inteiro deixa de valer, e o `kicad-cli pcb drc` **não avisa**. Ele cai em silêncio nas regras de netclass (FATO, teste local; ver armadilha 33). Este bloco, exatamente como está aqui, foi revalidado depois da correção.
- **Origem das condições:** `A.Type == 'Via'`, `A.isPlated()`, `hole_to_hole`, `edge_clearance`, `courtyard_clearance`, `diff_pair_gap`, `A.NetClass`, `hasNetclass` e `intersectsArea` aparecem todos em exemplos do manual 10 (FATO).
  - O manual usa `(rule "Distance between Vias of Different Nets" (constraint hole_to_hole (min 0.254mm)) (condition "A.Type == 'Via' && B.Type == 'Via' && A.Net != B.Net"))` e `(rule "Plated through-hole size" (constraint hole_size (min 0.2mm) (max 6.35mm)) (condition "A.isPlated() && A.Hole_Size_X == A.Hole_Size_Y"))` (FATO).
- **Origem dos números JLC:**
  - via 0,15/0,25 mm, "Via diameter should be 0.1mm (0.15mm preferred) larger than Via hole size", donde o anel de 0,05 mm (FATO);
  - furo-a-furo de via 0,2 mm e de pad 0,45 mm (FATO);
  - via-trilha 0,2 mm, PTH-trilha 0,28 mm (0,35 recomendado) e NPTH-trilha 0,2 mm (FATO);
  - anel PTH em 2 camadas, 1 oz: "Recommended 0.25 mm or above; absolute minimum 0.18 mm" (FATO);
  - SMD pad-pad de redes diferentes 0,15 mm (FATO).

  Tudo em <https://jlcpcb.com/capabilities/pcb-capabilities>.
- **Fora da linguagem de regras:** a ponte de máscara (0,10 mm; 0,13 mm em preto/branco) não tem restrição própria nessa linguagem. Configure em Board Setup → Solder Mask/Paste. INFERÊNCIA (a lista oficial de restrições não traz "web" de máscara; ela traz `bridged_mask`, que é outra coisa).
- **Repositórios prontos de `.kicad_dru` para JLC:**
  - **Cimos/kicad-druid**: JLCPCB, PCBWay e Generic, cada um em variantes 2L-1oz, 4L-1oz, 4L-2oz e 6L-1oz. Declara funcionar no KiCad 8, 9 e 10 (FATO: <https://github.com/Cimos/kicad-druid>). O `JLCPCB-2L-1oz.kicad_dru` foi aceito pelo DRC do 10.0.8 (FATO, teste local).
  - **labtroll/KiCad-DesignRules**: feito para o KiCad 7, também aceito pelo 10.0.8 (FATO, teste local). Ainda assim, confira os números contra a página atual da JLC (<https://github.com/labtroll/KiCad-DesignRules>).
  - **krsche/kicad-template**: derivado do labtroll (NÃO VERIFICADO).

### 14. Ferramentas do ecossistema: comando principal

> Nenhuma destas foi executada. A sintaxe vem da documentação de cada uma.

| Ferramenta | KiCad 10 | Comando principal | Fonte |
|---|---|---|---|
| **KiKit** (painel, fab) | v1.8.0 trouxe suporte ao 10 e largou as versões < 9; a v1.8.1 corrige zonas no 10.0.5 (FATO) | Instalação no Windows: abrir o **KiCad Command Prompt** e rodar `pip install kikit`, depois `kikit --help`. Uso: `kikit fab jlcpcb [--assembly --schematic placa.kicad_sch --field LCSC --missingError --corrections JLCPCB_CORRECTION] placa.kicad_pcb saida/` → `gerbers.zip`, mais `bom.csv` e `pos.csv` com `--assembly` (FATO) | <https://github.com/yaqwsx/KiKit/releases/tag/v1.8.0>, <https://yaqwsx.github.io/KiKit/latest/installation/windows/>, <https://yaqwsx.github.io/KiKit/latest/fabrication/jlcpcb/> |
| **Fabrication Toolkit** (gerber + BOM + CPL no formato JLC) | 5.3.1 corrigiu footprint duplicado no 10 (FATO) | Plugin PCM. CLI no KiCad Command Prompt: `python -m plugins.cli -p placa.kicad_pcb [-t] [-f] [-e]` (`-t` traduz rotação/posição, `-f` refill, `-e` exclui DNP). Campos: `LCSC Part #` e variantes; `FT Rotation Offset`; `FT Position Offset` (FATO) | <https://github.com/bennymeg/Fabrication-Toolkit> |
| **kicad-jlcpcb-tools** (Bouni: busca LCSC, BOM/CPL, correções de rotação) | badge v7–v10; seção de variantes "(KiCad 10+)" (FATO) | Só GUI: no PCM, adicionar o repositório `https://raw.githubusercontent.com/Bouni/bouni-kicad-repository/main/repository.json`. Gera `GERBER-<proj>.zip`, `BOM-<proj>.csv` e `CPL-<proj>.csv`. **Sem modo CLI documentado** (FATO) | <https://github.com/Bouni/kicad-jlcpcb-tools> |
| **InteractiveHtmlBom** | 2.12.0 com recursos do 10 (FATO) | `"$PY" .../InteractiveHtmlBom/generate_interactive_bom.py --no-browser --dest-dir bom --extra-fields "LCSC" placa.kicad_pcb` (FATO; a combinação de flags é minha) | <https://github.com/openscopeproject/InteractiveHtmlBom/wiki/Usage> |
| **KiCad StepUp** (FreeCAD, co-design de carcaça) | lista KiCad 10.x; FreeCAD 0.19–1.0 (FATO) | Bancada do FreeCAD (Add-on Manager): carregar a placa, exportar STEP, **push/pull do contorno** pelo Sketcher, checar colisão (FATO) | <https://github.com/easyw/kicadStepUpMod> |
| **pcb2blender** (render em Blender) | **sem release para o 10**: último `v2.17.5-k9.0-b5.1` (KiCad 9, Blender 4.5/5.1); PR #140 "Support KiCad 10" aberto (FATO) | No pcbnew: botão "Export to Blender (.pcb3d)". No Blender: File → Import → PCB (.pcb3d) (FATO) | <https://github.com/30350n/pcb2blender>, <https://github.com/30350n/pcb2blender/pull/140> |
| **Freerouting** | v2.5.0 tem modo IPC para KiCad 10+, com fallback para DSN/SES; binários nativos (sem JRE) para Windows x64 (FATO) | Plugin pelo PCM (Ctrl+M → "Freerouting"). Ao terminar, o plugin dispara o `ZONE_FILLER` (FATO). CLI: receita 12 | <https://github.com/freerouting/freerouting/releases/tag/v2.5.0>, <https://github.com/freerouting/freerouting/blob/master/docs/integrations.md> |

### 15. Netclasses, impedância, stackup, pares diferenciais e tuning (KiCad 10)
- **Pares diferenciais:** são nets com o mesmo nome-base e sufixo **`+`/`-`** ou **`P`/`N`**: `USB+`/`USB-` ou `USB_P`/`USB_N`. Os estilos **não se misturam**: `USB+` com `USB_N` não forma par. Roteador de par: tecla **6**. O gap vem da netclass ou de `diff_pair_gap` em regra customizada. FATO: <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html> (Routing differential pairs).
- **`inDiffPair('/USB')` só é verdadeiro se existir a net de polaridade oposta.** FATO: manual 10 (Expression functions).
- **Tuning:** as ferramentas de tuning ficam nas teclas **7** (trilha única) e seguintes. Os padrões de tuning são objetos persistentes, editáveis depois. Regras `length`/`skew` sobrescrevem o alvo do padrão, a menos que "override custom rules" esteja marcado. O `skew (… within_diff_pairs)` mede o skew dentro de cada par. FATO: manual 10 (Length tuning; Constraint types).
- **Tuning Profiles (novo no 10):**
  - Ficam em Board Setup.
  - Têm impedância-alvo e uma tabela por camada (camada de sinal, referências, largura, gap e atraso). A largura e o gap são **calculados pelo stackup** (microstrip com 1 referência, stripline com 2).
  - O perfil é atribuído à netclass na coluna "Tuning Profile". Aí o roteador interativo usa a largura e o gap do perfil, e o DRC pode acusar "Tuning profile track geometries" se a severidade estiver em Warning/Error.

  FATO: manual 10 (Tuning profiles).
- **PCB Calculator → TransLine:** microstrip, coplanar (com e sem plano), microstrip acoplada (par), stripline, coaxial, par trançado. Track Width usa a **IPC-2221**. FATO: <https://docs.kicad.org/10.0/en/pcb_calculator/pcb_calculator.html>.
  - **INFERÊNCIA:** para pedido com impedância controlada na JLC, a palavra final é a calculadora da JLC com o stackup escolhido (ver tema 04).
- **Netclasses na prática:**
  - Ficam em Board Setup → Net Classes, gravadas no `.kicad_pro` em `net_settings.classes` e `netclass_patterns` (FATO, teste local).
  - Uma net pode ter várias netclasses (KiCad 9+, FATO: blog 9.0).
  - `A.NetClass == 'HV'` casa qualquer classe da lista; `hasExactNetclass()` exige a lista exata (FATO: manual 10).

---

## Armadilhas

| # | Armadilha | Consequência | Correção | Etiqueta / fonte |
|---|---|---|---|---|
| 1 | `pcb render -h …` achando que é ajuda | No `pcb render`, `-h` é **`--height`** | Use `--help` | FATO (`--help` 10.0.8) |
| 2 | `pcb export pos` sem opções | O padrão é **ascii e polegadas** (`--format ascii`, `--units in`) | Sempre `--format csv --units mm` | FATO (`--help` 10.0.8) |
| 3 | CPL do KiCad enviado direto à JLC | O cabeçalho `Ref,Val,Package,PosX,PosY,Rot,Side` não é o esperado, e a rotação sai sem correção | Renomeie as colunas (receita 4) ou use o Fabrication Toolkit / kicad-jlcpcb-tools | FATO (teste local) + <https://jlcpcb.com/help/article/81-How-to-generate-the-BOM-and-Centroid-file-from-KiCAD> |
| 4 | `pcb export gerbers` sem `--layers` | Exporta **todas** as camadas habilitadas: Fab, Courtyard, User_*, Adhesive, Margin | Passe `--layers` explícito ou `--board-plot-params` | FATO (teste local) |
| 5 | BOM com faixas `C5-C13` | Faixas confundem a importação na fábrica (INFERÊNCIA) | `--ref-range-delimiter ''` | FATO (teste local) |
| 6 | `drc --refill-zones --save-board` em placa aberta ou versionada | `--save-board` **reescreve** o `.kicad_pcb` | Use só `--refill-zones` no gate; grave por decisão explícita | FATO (`--help`); risco: INFERÊNCIA |
| 7 | DRC rodado sem refill depois de mudar regra ou rota | Zona velha gera falso `copper_edge_clearance` e falsas ilhas (no teste, sumiu com refill) | `--refill-zones` no DRC, ou `ZONE_FILLER` antes de salvar | FATO (teste local) |
| 8 | `physical_hole_clearance` sem filtro de B | Também mede contra **courtyard** e contra o próprio objeto Footprint (cuja Layer é F.Cu), gerando falso "actual 0.0000 mm" | Filtre `B.Type == 'Track' \|\| B.Type == 'Via' \|\| B.Type == 'Zone'` | FATO (teste local); o manual diz que physical_* inclui courtyard: <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html> |
| 9 | `silk_clearance` sem condição | Também vale contra `Edge.Cuts` (silk "clipped by board edge") | Condicione (`B.Type == 'Pad'`) ou aceite que vale para a borda | FATO (teste local) |
| 10 | Ordem das regras no `.kicad_dru` | **A última que casa vence.** Regra genérica no fim anula as específicas | O genérico vai no topo, o específico embaixo | FATO: manual 10 |
| 11 | `insideArea()` / `insideCourtyard()` / `memberOf()` | Depreciadas no 10 (ainda funcionam) | `intersectsArea()`, `intersectsCourtyard()`, `memberOfGroup()` | FATO: manual 10 |
| 12 | `(severity ignore)` achando que desliga a regra | A regra **continua sendo avaliada** e ainda sobrescreve regras anteriores | Apague a regra ou reescreva a condição | FATO: manual 10 |
| 13 | Editar o `.kicad_dru` com a placa aberta | O manual manda editar só pela página Custom Rules do Board Setup | Use o Board Setup e o "Check rule syntax". O manual diz que erro de sintaxe **impede o DRC de rodar**; isso vale para a GUI. No `kicad-cli` 10.0.8 o DRC **roda mesmo assim, sem as regras** (ver 33) | FATO: manual 10 <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html> + teste local |
| 14 | Esperar que o DSN leve as regras do `.kicad_dru` | O DSN só leva largura, isolação e via por netclass, mais `smd_smd` global. Ficam de fora: regras customizadas, gap de par diferencial e isolação furo-cobre | Depois do SES, sempre DRC do KiCad; regras críticas à mão | FATO (teste local); furo-cobre: <https://github.com/freerouting/freerouting/issues/191> |
| 15 | Achar que "o DSN não leva zonas nem keepouts" | **Leva:** zona → `(plane NET (polygon …))`; rule area de trilha/via → `(keepout "" …)`, **sem o nome** | Use keepout para bloquear o autorouter | FATO (teste local, 10.0.8); fluxo DSN/SES: <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html> (Specctra DSN) |
| 16 | Achar que a netclass não vai para o DSN | **Vai:** `(class Power +5V VIN (circuit (use_via …)) (rule (width 500) (clearance 200)))`. Depois do SES, a +5V voltou quase toda a 0,5 mm, com alguns trechos a **0,375 mm**. Mas a classe só existe se o `.kicad_pro` estiver ao lado da placa e com os `netclass_patterns` | Exporte a partir da placa **com** o projeto. Confira `grep "(class " placa.dsn` antes de rotear | FATO (teste local); <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html> (Specctra DSN; Net Classes); o caso do `.kicad_pro` ausente é INFERÊNCIA |
| 17 | Confiar no resultado do Freerouting sem DRC | No teste (5 passes), apareceram trilhas de **0,112 mm** (< 0,15 mm da placa), 10 pontes de máscara e 2 violações de isolação de netclass | DRC do KiCad depois de todo import de SES, e conferência das larguras de energia | FATO (teste local); <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html> (Importing Specctra session files) |
| 18 | Usar o `-help` do jar 2.5.0 como referência | Ele ainda lista `-us`, `-hr` e `-is random`, que as notas da 2.5.0 dizem removidos | Use `--router.autorouter.*` da doc oficial | FATO: saída local + <https://github.com/freerouting/freerouting/releases/tag/v2.5.0> |
| 19 | Rodar o Freerouting 2.5.0 no JRE 17 padrão | O README do DevShared registra que a 2.4+ precisa do JDK 25 (que roda o jar; FATO, teste local) | Use `<DEVSHARED>\jdk25\…\java` | FATO: `<DEVSHARED>\README.md` |
| 20 | Procurar export DSN no `kicad-cli` | Não existe | GUI ou `pcbnew.ExportSpecctraDSN(board, path)` | FATO (`--help` 10.0.8) |
| 21 | `board.Remove(t)` num loop sobre `GetTracks()` | Centenas de "swig/python detected a memory leak", e o script não chegou a salvar | `board.Delete(t)` em `list(board.GetTracks())` | FATO (teste local); API: <https://dev-docs.kicad.org/en/apis-and-binding/pcbnew/> |
| 22 | `SaveBoard(dst, b)` | Grava também `dst.kicad_pro` e `.kicad_prl` (`aSkipSettings=False` por padrão) | `SaveBoard(dst, b, True)` para gravar só a placa | FATO (teste local + docstring); <https://dev-docs.kicad.org/en/apis-and-binding/pcbnew/> |
| 23 | Salvar via `pcbnew` com a placa aberta na GUI | A GUI não recarrega sozinha, e um Save na GUI sobrescreve o que o script fez | Feche a placa na GUI antes, ou use `kipy` com a GUI aberta | INFERÊNCIA (não testado) |
| 24 | Unidades na API | Internamente tudo é **nm inteiro**; `GetWidth()` devolve 150000, não 0,15 | `pcbnew.FromMM()` e `pcbnew.ToMM()` | FATO (teste local) |
| 25 | Script SWIG para longo prazo | Remoção planejada no KiCad 11; já emite `DeprecationWarning` | Exports pelo `kicad-cli`; edição nova em `kipy` | FATO: <https://dev-docs.kicad.org/en/apis-and-binding/pcbnew/> |
| 26 | Esperar headless ou export do `kipy` no 10 | O IPC API do 9/10 exige GUI aberta e não plota nem exporta | `kicad-cli` | FATO: <https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/for-addon-developers/> |
| 27 | `python -I` e acentos/Ω no print (Windows) | `PYTHONIOENCODING` é ignorado com `-I` | `sys.stdout.reconfigure(encoding='utf-8')` | Registrado no PADROES §15 da casa (sem fonte externa) |
| 28 | `--variant` com nome inexistente | O export rodou **sem erro** (no teste, `--variant x`) | Confira o nome da variante. Não conte com o CLI para acusar | FATO (teste local); <https://docs.kicad.org/10.0/en/cli/cli.html> |
| 29 | `-D` em `export drill`/`pos` ou `sch export bom` | Esses comandos **não têm** `--define-var` | Defina a variável no projeto | FATO (`--help` 10.0.8) |
| 30 | pcb2blender no KiCad 10 | O release atual é para o KiCad 9 | Aguarde o release do PR #140, ou use `pcb render` / STEP | FATO: <https://github.com/30350n/pcb2blender/pull/140> |
| 31 | kicad-jlcpcb-tools e SWIG | O release 2026.04.03 passou o "forced DRC" para a **SWIG API**: risco quando a SWIG sair no 11 | Acompanhe os releases antes de migrar para o KiCad 11 | FATO: <https://github.com/Bouni/kicad-jlcpcb-tools/releases/tag/2026.04.03>; risco: INFERÊNCIA |
| 32 | `jobset run` no 10.0.x | Relatos de segfault (10.0.3) e de job antigo executado (10.0.4) | Prefira o script de comandos; teste em cópia | NÃO VERIFICADO: <https://gitlab.com/kicad/code/kicad/-/issues/24474>, <https://forum.kicad.info/t/kicad-10-jobsets-issue/70476> |
| 33 | `.kicad_dru` com erro de sintaxe (ex.: `#` no fim de uma linha de regra) | O `kicad-cli pcb drc` 10.0.8 **ignora o arquivo inteiro sem aviso** e roda só com netclass e Board Setup. No teste, as violações de silk sumiram e só sobraram as de netclass. Isso **diverge do manual**, que diz que o erro impede o DRC (comportamento da GUI) | Comentário só em linha própria; depois de editar, use o "Check rule syntax" do Board Setup (que ele pegue um `#` no fim de linha é INFERÊNCIA, não testado). No JSON, `grep "rule '" drc.json` mostra regras suas **só se alguma disparou**: em placa limpa, nada aparece tanto com as regras carregadas quanto com o arquivo ignorado, então isso não serve de prova | FATO (teste local, 10.0.8); manual: <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html> |

---

## Checklist de exportação para fábrica

- [ ] Placement concluído e travado antes de rotear (PADROES §12).
- [ ] O `.kicad_dru` da fábrica certa (camadas e oz) está no projeto, e "Check rule syntax" passou (receita 13).
- [ ] Netclasses conferidas em Board Setup. Pares nomeados `_P`/`_N` ou `+`/`-`, sem misturar.
- [ ] Se usar Freerouting: `grep "(class " placa.dsn` mostra as classes; sinais críticos (USB, RF, cristal) já roteados à mão e fixados; DRC do KiCad depois do SES.
- [ ] Zonas preenchidas: `--refill-zones` no DRC ou `--check-zones` nos exports.
- [ ] `kicad-cli sch erc --format json --severity-all --exit-code-violations` → **exit 0**.
- [ ] `kicad-cli pcb drc --format json --severity-all --schematic-parity --exit-code-violations` → **exit 0**, com 0 `unconnected_items` e 0 `schematic_parity`.
- [ ] Gerbers com `--layers` explícito (cobre, máscara, pasta, silk, `Edge.Cuts`) e `--subtract-soldermask`.
- [ ] Furação com `--excellon-separate-th --excellon-units mm`: PTH e NPTH separados, mapa gerado.
- [ ] Gerbers e furos abertos num visualizador antes de zipar (INFERÊNCIA: prática comum).
- [ ] CPL com `--format csv --units mm --exclude-dnp`; colunas renomeadas para Designator/Mid X/Mid Y/Rotation/Layer; rotações conferidas no visualizador da JLC.
- [ ] BOM com Designator/Comment/Footprint/LCSC Part #, `--ref-range-delimiter ''` e `--exclude-dnp`; todas as linhas com código LCSC.
- [ ] Opcional: IPC-2581 ou ODB++ (`--check-zones` no ODB).
- [ ] STEP (`--subst-models`) entregue para a checagem de carcaça (StepUp/FreeCAD), e render top/bottom conferido.
- [ ] Gate mecânico de borda (PADROES §12): o DRC não pega isso.
- [ ] Tudo em `saida/<plataforma>/` e `python "<BRANDING>\ferramentas\coletar_saida.py" .` rodado (regra global do dono).
- [ ] `LICENSES.md` atualizado (footprints, 3D e `.kicad_dru` de terceiros: kicad-druid e labtroll têm licença própria; conferir antes de copiar). A licença desses repositórios não foi conferida (NÃO VERIFICADO).

---

## Conflitos com PADROES-PROJETO-PCB.md

| Item da casa | O que o teste local e as fontes mostram | Sugestão |
|---|---|---|
| Erro nº 20: "o DSN não leva zonas" | No 10.0.8, o DSN **leva** as zonas como `(plane …)`. O log do Freerouting 2.5.0 diz "power plane / large copper pour … configured for plane routing" (FATO, teste local). A "consciência de copper pour/plano" é novidade da v2.5.0 (FATO: notas da 2.5.0). O sintoma antigo provavelmente vinha de versões anteriores do Freerouting (INFERÊNCIA) | Reescrever: "o DSN leva zonas como plane; até a v2.4 o Freerouting não as tratava bem". Manter a cautela com roteamento parcial |
| Erro nº 11 e §1/§7: "netclass Power não aplicou no DSN" | No 10.0.8, várias netclasses saem no DSN com largura, isolação e via, e o SES trouxe a +5V quase toda a 0,5 mm, com trechos a 0,375 mm; outras trilhas vieram a 0,112 mm, abaixo do mínimo da placa (FATO, teste local). Isso **reforça** a regra da casa de conferir largura depois de rotear. A causa provável do caso antigo: export sem o `.kicad_pro`/patterns, ou pelo backend do MCP (INFERÊNCIA) | Manter "conferir largura depois de rotear" e acrescentar: "antes de rotear, `grep '(class ' placa.dsn`" |
| §15 passo 4: `java -jar freerouting.jar … -mp 50` | `-mp` está depreciado e o equivalente é `--router.autorouter.max_passes=50`; o jar 2.5.0 pede JDK 25 (FATO) | Atualizar a linha do comando |
| §15 passo 7: `kicad-cli pcb drc --format json --severity-all --schematic-parity` | Confirmado pela sintaxe do 10.0.8. Falta `--exit-code-violations`, útil num gate automático (FATO) | Acrescentar o flag |
| Falta no PADROES | `pos` tem padrão em polegadas; `gerbers` sem `--layers` exporta tudo; BOM com faixas | Incluir as armadilhas 2–5 |

---

## O que não foi confirmado

- O formato do arquivo `.kicad_jobset`, e o `jobset run` na prática: não há jobset nos demos, e o comando não foi executado.
- Onde se liga o servidor do IPC API na GUI. A página oficial não cita "Preferences → Plugins"; não confirmado.
- O comportamento de `SaveBoard` com a mesma placa aberta na GUI (armadilha 23: INFERÊNCIA).
- Se keepouts que bloqueiam só zona, pad ou footprint vão para o DSN. Só o keepout de trilha+via foi testado.
- O mapa completo de layer types no DSN quando há camadas internas tipo "power". Uma issue antiga diz que o Freerouting só roteia em camadas "signal"; não testado no 10.
- Os comandos de KiKit, Fabrication Toolkit, iBOM, StepUp e pcb2blender: nenhum foi executado.
- A licença dos repositórios `.kicad_dru` (kicad-druid, labtroll).
- A teardrop no 10: o manual 10 documenta os parâmetros padrão em Board Setup → Teardrops e as propriedades em regras (`Enable_Teardrops`, `Max_Width` etc.), mas as notas do 10.0 não citam mudança. Não sei em que versão a teardrop nativa entrou (as notas do 8.0 lidas não a mencionam).

---

## Bibliografia/URLs

### KiCad: oficial
- KiCad 10.0.0, notas de lançamento: <https://www.kicad.org/blog/2026/03/Version-10.0.0-Released/>
- KiCad 9.0.0, notas: <https://www.kicad.org/blog/2025/02/Version-9.0.0-Released/>
- KiCad 8.0.0, notas: <https://www.kicad.org/blog/2024/02/Version-8.0.0-Released/>
- Manual do Editor de PCB 10.0: Custom design rules, Tuning profiles, Differential pairs, Length tuning, Specctra DSN/SES, Design variants. <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html>
- Manual do kicad-cli 10.0 (sintaxe conferida por `--help` no 10.0.8): <https://docs.kicad.org/10.0/en/cli/cli.html>
- PCB Calculator 10.0: <https://docs.kicad.org/10.0/en/pcb_calculator/pcb_calculator.html>
- Doxygen da API Python 10.0: <https://docs.kicad.org/doxygen-python-10.0/namespaces.html>
- Dev-docs, bindings SWIG `pcbnew` (deprecação; remoção planejada no 11.0): <https://dev-docs.kicad.org/en/apis-and-binding/pcbnew/>
- Dev-docs, IPC API para desenvolvedores de add-on: <https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/for-addon-developers/>
- Dev-docs, IPC API (visão geral): <https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/>
- Relatos de jobset no 10 (NÃO VERIFICADO): <https://gitlab.com/kicad/code/kicad/-/issues/24474>, <https://forum.kicad.info/t/kicad-10-jobsets-issue/70476>

### Fábrica
- JLCPCB PCB Capabilities (lida em 2026-11-21): <https://jlcpcb.com/capabilities/pcb-capabilities>
- JLCPCB, BOM e CPL a partir do KiCad (verificado pela JLC no KiCad 10.0.3): <https://jlcpcb.com/help/article/81-How-to-generate-the-BOM-and-Centroid-file-from-KiCAD>

### Regras `.kicad_dru` prontas
- Cimos/kicad-druid (JLCPCB, PCBWay, Generic; KiCad 8–10): <https://github.com/Cimos/kicad-druid>
- labtroll/KiCad-DesignRules (JLCPCB, KiCad 7): <https://github.com/labtroll/KiCad-DesignRules>
- krsche/kicad-template (derivado; NÃO VERIFICADO): <https://github.com/krsche/kicad-template>

### Freerouting
- Argumentos de linha de comando: <https://github.com/freerouting/freerouting/blob/master/docs/command_line_arguments.md>
- Release v2.5.0 (2026-10-05): <https://github.com/freerouting/freerouting/releases/tag/v2.5.0>
- Integrações (plugin KiCad): <https://github.com/freerouting/freerouting/blob/master/docs/integrations.md>
- Issue #191 (isolação furo-cobre fora do DSN): <https://github.com/freerouting/freerouting/issues/191>

### Ecossistema
- KiKit v1.8.0 (suporte ao KiCad 10): <https://github.com/yaqwsx/KiKit/releases/tag/v1.8.0>; v1.8.1: <https://github.com/yaqwsx/KiKit/releases/tag/v1.8.1>
- KiKit, fab JLCPCB: <https://yaqwsx.github.io/KiKit/latest/fabrication/jlcpcb/>; instalação no Windows: <https://yaqwsx.github.io/KiKit/latest/installation/windows/>
- Fabrication Toolkit: <https://github.com/bennymeg/Fabrication-Toolkit>; release 5.3.1: <https://github.com/bennymeg/Fabrication-Toolkit/releases/tag/5.3.1>
- kicad-jlcpcb-tools: <https://github.com/Bouni/kicad-jlcpcb-tools>; release 2026.04.03: <https://github.com/Bouni/kicad-jlcpcb-tools/releases/tag/2026.04.03>
- InteractiveHtmlBom, uso: <https://github.com/openscopeproject/InteractiveHtmlBom/wiki/Usage>; release v2.12.0: <https://github.com/openscopeproject/InteractiveHtmlBom/releases/tag/v2.12.0>
- KiCad StepUp (FreeCAD): <https://github.com/easyw/kicadStepUpMod>
- pcb2blender: <https://github.com/30350n/pcb2blender>; PR KiCad 10: <https://github.com/30350n/pcb2blender/pull/140>

### Ambiente local (não é fonte pública; registro do teste)
- `kicad-cli --version` → `10.0.8`. Help de: `pcb`, `sch`, `jobset run`, `pcb drc`, `sch erc`, `pcb render`, e dos exports gerbers, drill, pos, ipc2581, odb, step, pdf e svg, além de `sch export bom/pdf/netlist`, `pcb import` e `pcb upgrade`. Lidos em 2026-11-21.
- Python do KiCad: 3.11.5, `pcbnew` 10.0.8, `kicad-python` 0.8.0 (`kipy`), `kicad-skip` 0.2.5.
- Freerouting: `%USERPROFILE%\.kicad-mcp\freerouting.jar` v2.5.0 (build 2026-10-05), rodado com `<DEVSHARED>\jdk25\jdk-25.0.5+8\bin\java`.
- Testes feitos numa cópia de `share\kicad\demos\stickhub` no scratchpad da sessão. Nenhum arquivo de projeto do dono foi alterado.
