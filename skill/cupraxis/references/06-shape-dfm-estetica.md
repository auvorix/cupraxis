# 06 — Shape (contorno), DFM JLCPCB, co-design com carcaça e estética

> Pesquisa de 2026-11-20. Etiquetas: **FATO** = conferido na fonte lida (URL ao lado); **INFERÊNCIA** = dedução / prática comum sem fonte primária lida; **NÃO VERIFICADO** = número visto só em resumo de busca, sem abrir a página.
> Página de capacidades da JLCPCB consultada em **2026-11-20**: <https://jlcpcb.com/capabilities/pcb-capabilities>. Os números de JLC abaixo vêm dela, salvo indicação.

## Resumo executivo

1. **Contorno** em `Edge.Cuts` tem que ser **fechado** (pontas coincidindo exatamente). Formas fechadas internas viram recortes. DXF e SVG entram por *File → Import → Graphics*. Co-design com o CAD mecânico: **KiCad StepUp** (FreeCAD), que empurra e puxa o contorno e verifica colisão. FATO.
2. **Canto interno** nunca é vivo: a fresa é redonda. A página oficial da JLC **não traz o raio**. O suporte da JLC citou uma fresa de **raio 0,5 mm** (recorte interno ≥ 1,0 mm), e o slot NPTH (não metalizado) tem largura mínima de **1,0 mm**. Na prática: **raio interno ≥ 1,0 mm** (INFERÊNCIA prudente). Para canto vivo, ponha um furo NPTH no canto.
3. **Folgas de borda (JLC):** cobre a **≥ 0,2 mm** da borda fresada e **≥ 0,4 mm** do V-cut (o blog da JLC recomenda 1,0 mm). Para montagem (PCBA), o **corpo do componente fica a ≥ 2,5 mm da borda** (termos da montagem JLC). Esta regra **colide** com a regra da casa de conector rente à borda (ver Conflitos).
4. **MLCC racha com a flexão da placa**: afaste os MLCCs **≥ 5 mm** (Knowles, Vishay) ou **≥ 10 mm** (Murata) de borda, furo de parafuso e conector, com o eixo longo **paralelo** à linha de separação.
5. **Furos de montagem:** KiCad M2 / M2.5 / M3 = furo de 2,2 / 2,7 / 3,2 mm, com anel de 4,4 / 5,4 / 6,4 mm. A especificação do Raspberry Pi HAT pede **furo de 2,75 mm, NPTH de preferência**, área livre de 6,2 mm e **cantos com R = 3 mm**.
6. **Painelização:** use **V-cut** só em linha reta e de ponta a ponta do painel (painel ≥ 70×70 mm, placa ≥ 0,6 mm). Use **mouse bites** (furos de 0,5–0,8 mm) para formas irregulares. A ferramenta para isso é o **KiKit**. A JLC não aceita V-cut na montagem *Economic*.
7. **Mínimos JLC (1 oz):** trilha/espaço de 0,10/0,10 mm (2 camadas) ou 0,09/0,09 mm (4+). Via de 0,15/0,25 mm (furo/diâmetro); a preferida tem furo ≥ 0,2 mm, e furos abaixo de 0,3 mm custam a mais. Anel ≥ 0,15–0,25 mm conforme o caso. Silk: traço ≥ 0,15 mm e altura ≥ 1,0 mm (proporção 1:6).
8. **Acabamento:** **ENIG para passo ≤ 0,5 mm** (QFN/BGA) e para cobre exposto decorativo. HASL só para passo > 0,65 mm (JLC). Máscara **preta ou branca** pede ponte de **0,13 mm** (contra 0,10 mm nas outras cores), o que pesa em QFN de passo fino.
9. **Estética:** silk legível (≥ 1 mm), orientação consistente, pino 1 e polaridade visíveis **depois** de montado, peças em grade, trilhas a 45° ou em arco, lágrimas (teardrops, nativas no KiCad). Máscara preta ou branca é opaca e esconde o cobre; verde, azul e roxo são translúcidos. Arte com cobre exposto fica longe de áreas de solda.
10. **Render:** visor 3D do KiCad, exportação STEP e **pcb2blender** (KiCad 9 → Blender) para campanha.
11. **Carcaça FDM:** folga de **0,5 mm** em volta dos componentes, parede ≥ 2 mm, furo de passagem +0,25 mm (Hubs). Nunca prenda a placa por interferência.

## Regras acionáveis

### A. Contorno (Edge.Cuts) e técnicas de formato

1. **O contorno é uma forma contínua e fechada, sem sobreposição; formas fechadas internas são recortes.**
   *Por quê:* com contorno inválido, o visor 3D e várias checagens do DRC não funcionam. O comando *Heal Shapes* corrige pequenas folgas entre pontas. **FATO**: <https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html>
2. **Para importar o contorno do CAD mecânico, use DXF ou SVG por *File → Import → Graphics* (Ctrl+Shift+F) direto na camada `Edge.Cuts`.** Confira a **unidade padrão do DXF** e a escala.
   *Por quê:* DXF sem unidade é lido na unidade padrão escolhida no diálogo, e um erro aí multiplica a placa por 25,4. **FATO** (opções do diálogo): mesma URL.
3. **Para geometria de encaixe (HAT, shield, Feather, módulo de host, carcaça), parta do DXF/STEP oficial**, nunca de memória. Isso confirma o PADROES §9 e o erro 8.
   *Por quê:* mesma razão do erro histórico. **INFERÊNCIA** apoiada pela especificação HAT, que é um desenho cotado oficial.
4. **Co-design ECAD↔MCAD com KiCad StepUp (bancada do FreeCAD):** carrega a placa com as peças no FreeCAD, exporta STEP, desenha o contorno no Sketcher e o **empurra (push) para a placa KiCad**, ou puxa, edita e devolve. Também **verifica colisão** com a carcaça. Funciona com FreeCAD 0.19–1.0 e KiCad 5.1–10.x.
   **FATO**: <https://github.com/easyw/kicadStepUpMod>
5. **Raio interno mínimo:** a página de capacidades da JLC **não publica** esse número (não encontrado em 2026-11-20). Em 2023 o suporte da JLC respondeu que usa fresa de **raio 0,5 mm**, ou seja, recorte interno de no mínimo **1,0 mm** de largura (**FATO de fonte secundária**: <https://techoverflow.net/2023/04/12/jlcpcb-which-milling-tool-radius-is-used-for-internal-cutouts>). O slot NPTH mínimo da JLC é **1,0 mm** (FATO, página de capacidades), o que é coerente com uma fresa de Ø 1,0 mm. Para comparação, a OSH Park usa fresa de **1,01 mm (0,040") nos recortes internos** e de **1,72 mm (0,068") no contorno** (FATO: <https://docs.oshpark.com/services/two-layer/>).
   **Regra da casa sugerida:** raio interno **≥ 1,0 mm** no contorno e nos recortes, o que cobre uma fresa de até Ø 2 mm (**INFERÊNCIA**).
   *Por quê:* a fresa redonda não alcança o canto vivo e deixa um raio igual ao dela. Quando o canto precisa ser vivo (encaixe), ponha **um furo NPTH no vértice** ("dog-bone"). A JLC lista furos no canto como solução (<https://jlcpcb.com/blog/how-to-avoid-incomplete-milling>, FATO qualitativo).
6. **Cantos externos arredondados** (R 1–3 mm): é o padrão de "cara de produto". O HAT exige **R = 3 mm** (FATO, `pdfs/06-dfm/rpi-hat-board-mechanical.pdf`). A JLC cobra **US$ 0,02/pç** para arredondar cantos e tirar rebarba em placas de 1,5–3 cm de lado, e **US$ 0,05/pç** abaixo de 1,5 cm (FATO: <https://jlcpcb.com/help/article/in-what-cases-will-there-be-charged-extra>). Desenhar o raio no próprio arquivo evita esse serviço (INFERÊNCIA).
7. **Slots (JLC):** slot metalizado com largura **≥ 0,5 mm** em 2 camadas e **≥ 0,35 mm** em multicamada; comprimento **≥ 2× a largura**. Slot NPTH **≥ 1,0 mm**. Tolerância: PTH +0,13/−0,08 mm; NPTH ±0,2 mm. **FATO** (capacidades). No KiCad, furo oval conta como **borda** para o DRC de clearance de borda (FATO, docs KiCad).
8. **Castellations (meio-furo, JLC):** furo **≥ 0,5 mm**, **≥ 1 mm** da borda, **≥ 0,5 mm** entre furos; placa **≥ 10×10 mm** e **≥ 0,6 mm** de espessura; **não aceita HASL**. Borda metalizada exige ≥ 3 pontos de quebra. **FATO** (capacidades).
9. **Tolerância do contorno (JLC):** fresado **±0,2 mm** (precisão ±0,1 mm só em placas ≥ 50×50 mm com 3 furos de ferramenta de 1,5 mm); depois do V-score, **±0,4 mm**. **FATO**.
   *Por quê:* em encaixe justo na carcaça, some esta tolerância à tolerância do FDM.
10. **Espessura (JLC FR-4):** 0,4 / 0,6 / 0,8 / 1,0 / 1,2 / 1,6 / 2,0 mm; tolerância ±10% (≥ 1,0 mm) ou ±0,1 mm (< 1,0 mm). A página diz 0,4–4,5 mm na faixa geral e 0,4–3,2 mm no FAQ (**conflito interno da página**). **FATO**. 1,6 mm é o padrão dos SMA edge-mount (PADROES §4) e dos HATs. Placa fina (≤ 0,8 mm) flexiona mais, o que é pior para MLCC e BGA, e **0,4 mm não aceita V-cut** (FATO, JLC Panelization). INFERÊNCIA: use 1,6 mm salvo restrição mecânica.

### B. Furos de montagem

11. **Diâmetros (biblioteca oficial do KiCad, `MountingHole.pretty`):**
    | Rosca | Furo | Pad (versão `_Pad`) | Courtyard |
    |---|---|---|---|
    | M2 | 2,2 mm | 4,4 mm | — |
    | M2.5 | 2,7 mm | 5,4 mm | Ø 5,9 mm |
    | M3 | 3,2 mm | 6,4 mm | — |
    **FATO**: <https://gitlab.com/kicad/libraries/kicad-footprints/-/tree/master/MountingHole.pretty> (arquivos `MountingHole_2.7mm_M2.5_Pad.kicad_mod` etc.). Os furos batem com a série *fine* (H12) da ISO 273: M2.5 = 2,7 e M3 = 3,2 mm (**NÃO VERIFICADO na norma**, visto em tabelas de terceiros; ISO 273 é paga, só citar).
12. **Keepout da cabeça do parafuso:** use o courtyard ou o círculo de comentário do footprint (Ø 5,4–5,9 mm no M2.5) como zona sem cobre de outra rede e sem componentes. Some a arruela ou o espaçador se forem maiores. **INFERÊNCIA** (o footprint desenha a cabeça em `Cmts.User`, Ø 5,4 mm, o que é FATO; tratar isso como keepout é inferência).
13. **NPTH ou anel de cobre:** a especificação do HAT diz que o furo **deve ser preferencialmente não metalizado**. Se for metalizado, o furo e o anel ficam **eletricamente isolados (não ligar ao GND)**, com área livre mínima de **6,2 mm** (cobre isolado ou máscara aberta), e o furo sai em **2,75 mm ±0,05**. **FATO**: `pdfs/06-dfm/rpi-hat-board-mechanical.pdf`.
    Em produto próprio com carcaça plástica, o anel ligado ao GND serve de aterramento ou blindagem quando há chassi metálico. Sem chassi, use NPTH (INFERÊNCIA). **Decida e registre no projeto.**
14. **NPTH mínimo da JLC = 0,50 mm**; anel de pad NPTH recomendado **≥ 0,45 mm**; trilha a **≥ 0,2 mm** do NPTH. **FATO** (capacidades).
15. **MLCC longe do parafuso:** ver a regra 35 (Murata recomenda ≥ 10 mm de furos de parafuso). FATO.

### C. Folgas de borda e de montagem (JLC)

16. **Cobre → borda fresada ≥ 0,2 mm; cobre → V-cut ≥ 0,4 mm.** **FATO** (capacidades). O blog da JLC sobre V-cut recomenda **1,0 mm** para cobre (FATO: <https://jlcpcb.com/blog/v-cut-panelization-standards>). Configure isso em *Board Setup → Constraints → Copper to edge clearance*; o DRC acusa *Board edge clearance violation* (FATO, docs KiCad). OSH Park: 0,381 mm (15 mil). PCBWay: 0,25 mm normal.
17. **Corpo do componente → borda ≥ 2,5 mm em pedido de montagem JLC.** Texto literal: *"The distance between the body of the components and the edge of the board must be equal or greater than 2.5mm."* **FATO**: <https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service>. Ver Conflitos (USB-C, SD e SMA na borda).
18. **Componentes altos ou sensíveis a estresse a ≥ 2,0 mm da linha de V-cut** (blog da JLC, FATO, mesma URL da regra 16). O guia da Altium diz **≥ 0,100" (2,54 mm)** entre SMT e a borda com V-groove (FATO: `pdfs/06-dfm/altium-dfm-guidebook.pdf`, cap. "Depanelization").
19. **Espaçamento entre componentes para montagem JLC (exemplos):** 0402↔0402 0,15 mm; 0603↔0603 0,18 mm; QFN↔passivo 1,0 mm; QFN↔QFN 1,0 mm; QFP↔QFP 1,25 mm; BGA↔BGA 2,0 mm. **FATO**: <https://jlcpcb.com/help/article/minimum-spacing-for-smd-components> (tabela completa lá).
20. **Silk → pad ≥ 0,15 mm** (JLC, FATO). O KiCad acusa *Silkscreen clipped by board edge* e permite exigir distância silk↔borda (FATO, docs).

### D. Painelização

21. **V-cut (JLC):** só linhas retas horizontais ou verticais que **atravessam o painel inteiro**; folga zero entre placas; ≥ 2 mm entre V-cuts paralelos (3 mm recomendado); ≤ 25 linhas por eixo; ângulo de 25°; alma restante ≈ 1/3 da espessura; placa ≥ 0,6 mm; painel de **70×70 a 475×475 mm**. Placa com lado < 15 mm paga extra. **FATO**: capacidades + <https://jlcpcb.com/help/article/PCB-Panelization> + blog V-cut.
22. **Forma irregular, arcos ou abas → tab-routing com mouse bites:** furos de **Ø 0,5–0,8 mm**, espaçados **0,2–0,3 mm**, aba de **≥ 5 mm** (≥ 4 mm sem mouse bite), **1,6–2 mm** entre placas. **FATO** (capacidades). O guia da Altium sugere furos de 20–30 mil a passo de 40–50 mil e **≥ 2 abas por lado** (FATO, Altium cap. Breakaway Tabs). Desloque os furos **para dentro** da placa se a carcaça for justa, para não sobrar rebarba (Altium, FATO).
23. **Trilhos (rails):** a JLC diz **≥ 3 mm** de borda de ferramenta, ou **5 mm para SMT**, com furos de ferramenta de **2 mm** e fiduciais de **1 mm** centrados a **3,85 mm** da borda do painel. O FAQ da mesma página recomenda **5–8 mm** (**conflito interno da JLC**; INFERÊNCIA: use 5 mm ou mais). **FATO**.
24. **Montagem JLC exige furos de ferramenta, trilhos e fiduciais.** Se faltarem, a JLC **adiciona por conta própria**. Placa < 70×70 mm ou sem trilho recebe mouse bite. Com "Panel by JLCPCB" os fiduciais vão nos trilhos, **não em cada placa**. **V-cut não é aceito na montagem Economic**, só na Standard. **FATO**: termos de montagem + página Panelization.
25. **KiKit** (`kikit panelize`): configuração em JSON ou CLI por seções `layout`, `source`, `tabs`, `cuts` (`mousebites`: drill/spacing/offset/prolong; `vcuts`), `framing` (`railstb`, `railslr`, `frame`), `tooling` (`3hole`/`4hole`), `fiducials` (`3fid`/`4fid`), `post` (`millradius`, "geralmente ≈ 1 mm"). Presets com `-p :vcuts`. **FATO**: <https://yaqwsx.github.io/KiKit/latest/panelization/cli/>. **Não encontrado** um preset "jlcTooling" na página lida. Para pacote JLC: `kikit fab jlcpcb --assembly --schematic ... BOARD OUTDIR` gera `gerbers.zip`, `bom.csv` e `pos.csv` (FATO: <https://yaqwsx.github.io/KiKit/latest/fabrication/jlcpcb/>).
   Use `post.millradius = 1mm` para o painel simular o raio da fresa (INFERÊNCIA a partir da documentação).

### E. DFM JLCPCB: capacidades (consulta em 2026-11-20)

26. **Trilha/espaço (1 oz):** 0,10/0,10 mm em 1–2 camadas; 0,09/0,09 mm em multicamada (0,075 só no fan-out de BGA). Com 2 oz: 0,16/0,16 (2 camadas) e 0,15/0,15 (multicamada). Tolerância de largura ±20%. **FATO**.
27. **Vias:** mínimo de 0,15 mm de furo / 0,25 mm de diâmetro; diâmetro da via ≥ furo + 0,1 mm (0,15 preferido), o que dá anel de ≈ 0,05–0,075 mm; **furo preferido ≥ 0,2 mm**; 0,1/0,2 só em placa ≤ 1 mm com ENIG/OSP e custo extra. **Furos < 0,3 mm têm cobrança extra.** Via↔via 0,2 mm. **FATO**: capacidades + página de cobranças extras.
   INFERÊNCIA: use **0,3/0,6 mm** como via padrão da casa e 0,2/0,4–0,45 mm onde a densidade exigir.
28. **Anel PTH:** 2 camadas 1 oz recomenda 0,25 mm (mínimo absoluto 0,18); multicamada 1 oz recomenda 0,20 mm (mínimo 0,15). PTH mínimo recomendado de 0,5 mm. **FATO**.
29. **Máscara:** expansão 1:1; abertura↔trilha ≥ 0,09 mm; **ponte de 0,10 mm** em verde, vermelho, amarelo, azul e roxo, e **0,13 mm em preto e branco** (1 oz). Vias tampadas com diâmetro ≤ 0,5 mm. **FATO**.
30. **Silkscreen:** traço **≥ 0,15 mm**, altura **≥ 1,0 mm** (40 mil), proporção largura:altura **1:6**, silk↔pad 0,15 mm. **FATO**. A PCBWay padrão aceita 0,15 mm de traço, 0,8 mm de altura e proporção 1:5 (FATO: <https://www.pcbway.com/capabilities.html>). Configure no KiCad em *Board Setup → Constraints → Minimum text height/thickness*; o DRC acusa *Text height/thickness out of range* (FATO, docs KiCad).
31. **Cores e acabamentos (JLC):** máscara verde, roxa, vermelha, amarela, azul, branca ou preta. Acabamentos HASL (com ou sem chumbo), ENIG e OSP; HASL não é aceito em 6+ camadas nem em placa ≤ 0,4 mm. Cobre externo de 1 ou 2 oz em multicamada; interno de 0,5 oz (padrão), 1 ou 2 oz. **FATO**.
32. **ENIG ou HASL:** *"Choose ENIG when your design has trace spacing or component pitch ≤ 0.5 mm"* e *"…pitch > 0.65 mm, HASL is usually sufficient"*. **FATO**: <https://jlcpcb.com/blog/how-to-resolve-short-circuit-hasl>. A JLC **cobra extra quando a área de ENIG passa de 30%** da placa (FATO, página de cobranças extras). INFERÊNCIA: em placas com QFN (ESP32-C5, CC1101, LNA) e RF, ENIG é o padrão.
33. **2 ou 4 camadas, custo:** a JLC anuncia "a partir de US$ 2 / 5 pç". Um resumo de busca indica que a promoção cobre 1–2 camadas até 100×100 mm, mas 4–8 camadas só até **50×50 mm** (**NÃO VERIFICADO**). Em 03/08/2026 a JLC anunciou um reajuste dos preços de FR-4 de 1, 2 e 4 camadas, sem números publicados (FATO: <https://jlcpcb.com/news/jlcpcb-fr4-pcb-price-adjustment-august2026>). **Use sempre a cotação instantânea.** Furação extra: 4 camadas paga mais por 10 mil furos que 2 camadas (NÃO VERIFICADO).
34. **DRC do fabricante no KiCad:** copie um `.kicad_dru` com as regras JLC para a pasta do projeto, renomeado para `<projeto>.kicad_dru`. Exemplo: <https://github.com/labtroll/KiCad-DesignRules> (FATO: escrito para o KiCad 7; **não testado no KiCad 10**). Alternativa citada: `Cimos/kicad-druid` (JLC e PCBWay, sintaxe do KiCad 8; NÃO VERIFICADO). INFERÊNCIA: **confira cada número contra a página de capacidades** antes de confiar no arquivo.

### F. MLCC, flexão e depanelização

35. **Distância de MLCC à borda, furo de parafuso e conector:** a Murata recomenda **≥ 10 mm** (exemplo de "distância apropriada") e diz que **fendas (slits) são melhores que perfurações** (FATO: <https://article.murata.com/article/strain-crack-mechanism-and-preventive-measures-for-mlcc>). A Vishay diz que normas costumam exigir **5 mm** borda↔MLCC e orientação **paralela à borda** (FATO: `pdfs/06-dfm/vishay-49088-mlcc-flex-cracking.pdf`). A Knowles situa a zona de estresse a **≈ 5 mm** da borda ou do ponto de fixação, desaconselha MLCC **no canto** e diz que uma fenda ao longo da borda de depanelização reduz o estresse (FATO: `pdfs/06-dfm/knowles-5mm-board-flex.pdf`).
36. **Orientação perto da linha de quebra:** os fabricantes de MLCC (Murata e Vishay, FATO; TDK, NÃO VERIFICADO, só via resumo de busca) mandam o eixo longo **paralelo** à linha de separação. O guia da Altium diz para orientar as peças **"90° to the board's edge"** perto das abas (FATO, Altium cap. Breakaway Tabs). **A literatura diverge.** Prevalece a fonte primária do componente: **paralelo** (INFERÊNCIA). Altium também pede **nada (componente, trilha, via, plano) a menos de 0,100" dos furos de quebra**.
37. **Placa grande e pesada:** evite BGA ou QFP grandes no centro de placas de 1,6 mm com mais de 25 pol² (≈ 161 cm²), por causa do empenamento (FATO, Altium).

### G. Co-design com a carcaça

38. **Folga FDM:** **0,5 mm** em volta dos componentes internos, parede **≥ 2 mm**, furo de passagem **+0,25 mm** no diâmetro (−0,25 mm para autoatarraxante), parede em volta do furo de boss **≥ 1 diâmetro**, recorte de porta com **2 mm a mais (1 mm por lado)**. **FATO**: <https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/>. Placa↔parede de 0,4–0,5 mm (prática comum; INFERÊNCIA). A placa nunca entra por interferência; use insertos de rosca a quente (heat-set) em vez de rosca impressa quando a carcaça for aberta mais vezes (INFERÊNCIA, consenso das fontes da busca).
39. **Soma das tolerâncias:** contorno da JLC ±0,2 mm (±0,4 mm no V-score) + FDM (~±0,2–0,25 mm) + posição do componente. Projete o recorte de USB-C e SMA com **≥ 0,5 mm por lado** (INFERÊNCIA a partir das regras 9 e 38).
40. **Zona de altura restrita:** desenhe no KiCad uma *rule area* (keepout) ou uma camada `User` com a altura máxima por região (sob a tampa, sob a bateria, sob o boss) e verifique em STEP. O KiCad StepUp **checa colisão** placa↔carcaça (FATO, regra 4). INFERÊNCIA quanto à técnica de camada.
41. **Botões, LEDs e light pipes:** o centro do LED deve estar no **eixo exato** do furo ou light pipe, com a ponta do pipe **o mais perto e paralela possível** da face do LED. Pipe rígido funciona bem até **≈ 75 mm** (NÃO VERIFICADO: visto só em resumo de busca de <https://resources.altium.com/p/light-pipes-explained> e do PDF VCC/Mouser <https://www.mouser.com/pdfDocs/WhatEngineersMustActuallyValidateBeforeDeployingLEDIndication.pdf>). **Valores numéricos de folga LED↔pipe não encontrados**; use o desenho do pipe escolhido.
42. **Exporte STEP da placa a cada revisão mecânica** (o KiCad gera STEP, GLB, BREP e XAO; a espessura vem do stackup) e confira a interferência no CAD. **FATO** (docs KiCad, introdução).

### H. Formatos padrão (proporção e furação de referência)

43. **Raspberry Pi HAT:** **65×56,5 mm** (56 mm com header PTH), **R = 3 mm** nos cantos, **4 furos M2.5 de 2,75 mm em retângulo de 58×49 mm** a 3,5 mm das bordas, recortes para flex de câmera (slot de 2×17 mm) e display. **FATO**: `pdfs/06-dfm/rpi-hat-board-mechanical.pdf` (desenho oficial lido). HAT+: pelo menos 1 furo alinhado ao Pi e espaçadores de **15 mm, sendo 16 mm o ideal** (FATO: `pdfs/06-dfm/rpi-hat-plus-specification.pdf`, cap. 7).
44. **Adafruit Feather:** **0,9" × 2,0" (22,86×50,8 mm)**, furos de 0,1" em cada canto (diâmetro não dado), header de 16 pinos e de 12 pinos com 0,8" entre as fileiras, USB à esquerda; **não mude a posição dos GPIO**. **FATO**: <https://learn.adafruit.com/adafruit-feather/feather-specification>.
45. **Qwiic:** conector JST SH de 4 pinos (SM04B-SRSS-TB), na ordem **GND / 3,3 V / SDA / SCL**, com cabo preto/vermelho/azul/amarelo. Qwiic Micro mede 19,05×7,62 mm. **Não há tamanho de placa padrão** publicado. **FATO**: <https://www.sparkfun.com/qwiic>.
46. **mikroBUS (Click):** tamanhos S/M/L de 25,4 × 28,6 / 42,9 / 57,15 mm, placa de 1,6 mm, furo de 35 mil (**NÃO VERIFICADO**: vem de cópia de terceiros da especificação v1; a página oficial da mikroe devolveu 403).

### I. Estética profissional

47. **Silk legível:** altura **≥ 1,0 mm** e traço **≥ 0,15 mm** (mínimo da JLC). INFERÊNCIA da casa: referências de **1,0 mm / 0,15 mm**, títulos de **1,5–2 mm / 0,25–0,3 mm** (o KiKit usa 1,5/0,3 mm como texto padrão do painel, FATO). Silk **nunca sobre pad nem sobre cobre exposto**: não adere ao cobre e é removido do pad (FATO: <https://hackaday.io/project/188607-make-your-own-pcb-art/details>; Altium: *"Always keep Silkscreen off pads"*).
48. **Todo contorno de componente com referência e indicador de polaridade**; o indicador tem que ficar **visível depois de montado** e fora do pad. O guia da Altium recomenda polarizados com o **+ para a direita ou para baixo** (orientação consistente) e desacoplamento colado ao pino. **FATO**: Altium DFM Guidebook, cap. 3–4. Referência secundária (NÃO VERIFICADO, só resumo de busca): JLC <https://jlcpcb.com/help/article/component-polarity-and-orientation-identification-guide>.
49. **Rotule** todo botão, LED, pino e conector de energia; tabela de pinout no silk junto do header; **vias tampadas** para não interromper o texto do silk. NÃO VERIFICADO: vem do resumo de busca do tutorial SparkFun "Better PCBs in Eagle", cuja URL (sparkfun.com/tutorials/115) devolveu 404 em 2026-11-20. Fica como INFERÊNCIA de boa prática.
50. **Orientação consistente do texto** (no máximo 2 direções de leitura, 0° e 90°), peças em **grade** (0,5 / 0,25 mm), passivos do mesmo grupo alinhados e com a mesma rotação. **INFERÊNCIA** (prática de mercado; o PADROES §11 já exige zero off-grid).
51. **Trilhas a 45° ou em arco**: o KiCad roteia com arcos (*each routing step will place either a straight segment, a single arc, or both*). **Lágrimas (teardrops)**: *Edit → Edit Teardrops* em massa, com padrões em *Board Setup → Teardrops* para pads redondos, retangulares e trilha↔trilha, e opção de bordas curvas. **FATO**: docs KiCad 9. Melhoram a robustez da junção trilha↔pad ou via (INFERÊNCIA comum) e a aparência.
52. **Cor da máscara:** **preto e branco são opacos** e não mostram o cobre embaixo; **verde, azul e roxo são translúcidos** e ficam "lavados" sobre plano de cobre; amarelo fica melhor sobre cobre; vermelho é vivo sobre cobre e discreto sobre FR-4 nu. **FATO**: <https://hackaday.io/project/188607-make-your-own-pcb-art/details> e <https://hackaday.com/2023/01/15/designing-aesthetically-pleasing-pcbs>. Lembre a ponte de máscara maior no preto e no branco (regra 29).
53. **Arte em cobre e máscara (board art):** combine 4 tons (máscara sobre cobre, máscara sobre FR-4, cobre exposto, silk). **Cobre exposto fica dourado em ENIG e prateado em HASL**; o autor recomenda **ENIG** para arte. Trilhas decorativas ficam ligadas só por uma ponta (ou isoladas) para não gerar erro de DRC, e **sem cobre exposto perto de pontos de solda** (risco de curto). Toda placa precisa de ≥ 1 furo e de cobre nas 2 faces, senão a fábrica estranha. **FATO**: mesmas URLs da regra 52.
   Atenção ao PADROES §11 (zero avisos): trilha decorativa em cobre gera aviso de net. INFERÊNCIA: desenhe a arte como **gráfico** em `F.Cu` mais a abertura em `F.Mask`, fora de qualquer net.
54. **Logo:** importe o SVG por *Import Graphics* em `F.Silkscreen`, com linha de traço ≥ 0,15 mm e detalhes ≥ 0,15 mm (INFERÊNCIA a partir do mínimo da JLC). Isso confirma o PADROES §10.
55. **Render para campanha:** use o visor 3D do KiCad para conferência e o **pcb2blender** (plugin do KiCad que exporta `.pcb3d` para importar no Blender 4.5 LTS/5.1, testado com KiCad 9, GPL-3.0) para render de produto. **FATO**: <https://github.com/30350n/pcb2blender>. **Não confirmado** se suporta o KiCad 10.
56. **Referências visuais** (Adafruit, Flipper, Teenage Engineering, badges da Hackaday): **não pesquisadas em detalhe nesta rodada** (lacuna). Fica apenas a referência ao guia Adafruit de arte em PCB: <https://learn.adafruit.com/making-wearable-badge-art-with-printed-circuit-boards?view=all> (camada vetorial → camada de PCB; NÃO VERIFICADO além do resumo).

### J. Documentação de fabricação e montagem

57. **Desenho mestre:** cotas a partir de **datums funcionais** (furos de montagem, não a borda), grade declarada, notas (material, espessura, acabamento, cor de máscara e silk, tolerâncias), tabela de furos. **FATO**: Altium DFM Guidebook, cap. 6–7 ("Avoid choosing datums at a board's edge"; ≥ 2 furos na grade).
58. **Camadas `F.Fab`/`B.Fab`** com contorno e referência de cada peça, para gerar o PDF de montagem; cotas em `User.Drawings`/`Dwgs.User`. INFERÊNCIA (convenção KiCad; a seção de camadas da documentação não foi lida em detalhe).
59. **BOM/CPL para a JLC:** confira a rotação no visualizador da JLC. Para corrigir peça girada ou deslocada, edite a coluna Rotation ou Mid X/Y do CPL e reenvie (FATO: <https://github.com/JLCPCB/JLCPCB-SMT-Assembly-Components-orientation-fix>). Para não editar à mão, use um **campo de correção por componente**: KiKit `JLCPCB_CORRECTION = "X;Y;Rot"` (mm, graus, rotação anti-horária, X/Y no referencial do footprint) (FATO: KiKit docs). No plugin bennymeg, os campos seriam `JLCPCB Rotation Offset` e `JLCPCB Position Offset` (NÃO VERIFICADO, visto só em resumo de busca: <https://github.com/bennymeg/Fabrication-Toolkit>).
60. **Fiduciais:** obrigatórios em toda arte SMT (Altium, FATO). A JLC põe os fiduciais no trilho, não em cada placa (regra 24). Se a placa vai sem trilho (montagem de placa única), ponha 2–3 fiduciais de **1 mm** de cobre com abertura de máscara de ~2 mm em cantos opostos (INFERÊNCIA; os 1 mm vêm do padrão de painel da JLC).

## Erros comuns

| Erro | Consequência | Correção |
|---|---|---|
| Contorno com pontas que não fecham ou que se sobrepõem | Visor 3D e DRC quebram; a fábrica interpreta errado | *Heal Shapes*; conferir o DRC de contorno (docs KiCad) |
| DXF importado na unidade errada | Placa 25,4× maior ou menor | Definir a unidade padrão do DXF no diálogo e medir uma cota conhecida |
| Canto interno vivo no contorno ou no encaixe | A fresa deixa raio e o encaixe não entra | Raio ≥ 1 mm ou furo NPTH no vértice (dog-bone) |
| Conector rente à borda num pedido PCBA JLC | Viola a regra de corpo ≥ 2,5 mm da borda; a JLC pode recusar ou exigir trilho | Trilho/borda de processo no painel, ou soldar o conector à mão (ver Conflitos) |
| MLCC (sobretudo ≥ 0805) junto à borda, aba, V-cut ou furo de parafuso | Trinca invisível que vira fuga ou curto em campo | ≥ 5–10 mm, eixo paralelo à linha de quebra, fenda de alívio |
| V-cut em placa com arco ou aba | A JLC não faz (só corta reto, de ponta a ponta) | Tab-routing com mouse bites (KiKit) |
| Cobre a < 0,4 mm do V-cut ou < 0,2 mm da borda | Cobre exposto, curto com o chassi | Constraint *copper to edge* no Board Setup |
| Silk com 0,1 mm de traço ou 0,8 mm de altura | Texto borrado ou ilegível na JLC | ≥ 0,15 mm e ≥ 1,0 mm; mínimos de texto no Board Setup |
| Silk sobre pad, via aberta ou cobre exposto | Texto cortado ou some | Tampar vias; afastar 0,15 mm do pad |
| Máscara preta em QFN de passo 0,4–0,5 mm | Ponte de máscara de 0,13 mm não cabe; solder bridge | Verde para a 1ª revisão, ou checar a ponte no DRC |
| HASL com QFN/BGA de passo ≤ 0,5 mm | Pad abaulado e curtos | ENIG |
| Furo de montagem metalizado ligado ao GND em padrão que pede isolado (HAT) | Viola a especificação e cria laço de terra pelo parafuso | NPTH, ou anel isolado ≥ 6,2 mm |
| Componente dentro do diâmetro da cabeça do parafuso | O parafuso esmaga a peça | Keepout = courtyard do furo (Ø 5,9 mm no M2.5) |
| Placa justa na carcaça impressa | Empena; trinca MLCC; não monta | Folga de 0,5 mm; furo +0,25 mm; não prender por interferência |
| Confiar num `.kicad_dru` de terceiros sem conferir | Regra desatualizada aprova algo que a fábrica recusa | Conferir o arquivo contra a página de capacidades (data) |
| CPL com rotação do KiCad ≠ da JLC | Peça girada (diodo, CI) | Conferir o visualizador da JLC; campo de correção por peça |
| Arte de cobre ligada à net ou perto de solda | Curto ou aviso de DRC (viola a regra de zero avisos) | Arte como gráfico fora de net, longe de pads |

## Checklist

- [ ] Contorno fechado em `Edge.Cuts`, sem sobreposição; recortes internos fechados.
- [ ] Geometria de encaixe tirada do DXF/STEP **oficial** e uma cota conhecida medida depois de importar.
- [ ] Cantos externos arredondados (R 1–3 mm); **todo canto interno com R ≥ 1,0 mm** ou furo NPTH no vértice.
- [ ] Slots: PTH ≥ 0,5 mm (2 camadas) ou ≥ 0,35 mm (multicamada); NPTH ≥ 1,0 mm; comprimento ≥ 2× a largura.
- [ ] Furos de montagem: M2.5 = furo de 2,7 mm (HAT: 2,75), decisão NPTH ou anel registrada, keepout de cabeça Ø ≥ 5,9 mm livre.
- [ ] Board Setup: *copper to edge* ≥ 0,2 mm (≥ 0,4 mm se houver V-cut); texto ≥ 1,0 mm e espessura ≥ 0,15 mm; trilha ≥ 0,10 mm; via ≥ 0,2/0,4 mm (padrão 0,3/0,6).
- [ ] `.kicad_dru` da JLC no projeto, conferido contra a página de capacidades (com data).
- [ ] Pedido PCBA: corpos a ≥ 2,5 mm da borda **ou** trilho/borda de processo definidos para os conectores de borda.
- [ ] MLCCs a ≥ 5 mm (ideal 10 mm) de borda, aba, V-cut, furo de parafuso e conector; eixo paralelo à linha de quebra; nada no canto.
- [ ] Painel: V-cut só reto e de ponta a ponta (painel ≥ 70×70 mm, placa ≥ 0,6 mm); senão mouse bites de 0,5–0,8 mm, abas ≥ 5 mm, 1,6–2 mm entre placas; trilhos ≥ 5 mm com fiduciais de 1 mm a 3,85 mm e furos de 2 mm.
- [ ] Montagem com V-cut → serviço Standard (não Economic).
- [ ] Acabamento: ENIG se houver passo ≤ 0,5 mm, RF ou cobre exposto decorativo; área de ENIG ≤ 30% ou custo aceito.
- [ ] Cor da máscara escolhida considerando a ponte (preto e branco = 0,13 mm) e a opacidade.
- [ ] Silk: referências legíveis, todas na mesma orientação (no máximo 2), pino 1 e polaridade visíveis depois de montado, nada sobre pad, vias tampadas.
- [ ] Peças em grade, grupos alinhados, rotação consistente; trilhas a 45° ou arco; teardrops aplicados.
- [ ] Logo (mono), nome, versão e pinout no silk; arte em cobre como gráfico fora de net.
- [ ] STEP exportado; interferência com a carcaça checada (StepUp/FreeCAD); zonas de altura respeitadas.
- [ ] Carcaça: folga de 0,5 mm, recortes de porta com ≥ 0,5–1 mm por lado, furos +0,25 mm, insertos heat-set.
- [ ] LEDs e botões no eixo dos furos ou light pipes da carcaça (medido no 3D).
- [ ] Documentação: `F.Fab` com referências, desenho com cotas a partir de datums nos furos, notas de material, espessura, acabamento e cores.
- [ ] BOM/CPL gerados; rotação conferida no visualizador da JLC; correções em campo por peça.
- [ ] Render (visor 3D / pcb2blender) conferido antes de fabricar.

## Conflitos com PADROES-PROJETO-PCB.md

| Item | PADROES | Literatura / fabricante | Situação |
|---|---|---|---|
| **Conector na borda × regra PCBA da JLC** | §5, §13 #1–4: USB-C, microSD e SMA **rentes à borda** (barril do SMA para fora) | Termos de montagem da JLC: **corpo do componente ≥ 2,5 mm da borda** (FATO) | **DIVERGE — decisão do dono.** Não verifiquei como a JLC trata conector que ultrapassa a borda num pedido PCBA. Saídas possíveis (INFERÊNCIA): (a) painel com **trilho/borda de processo** do lado dos conectores, retirado depois; (b) conectores de borda soldados à mão; (c) consultar o suporte da JLC antes do pedido. A regra da casa continua correta para a **mecânica**; falta a regra de **processo**. |
| **MLCC × furos M2.5 de canto e conectores de borda** | §9 (furos M2.5 nos cantos) e §5 (conectores na borda); nada sobre MLCC | Murata ≥ 10 mm; Vishay e Knowles ≈ 5 mm de borda, furo de parafuso e conector; nada no canto (FATO) | **FALTA.** Proposta: regra de afastar MLCC ≥ 5 mm (ideal 10 mm), com orientação paralela à linha de quebra. |
| Orientação perto da quebra | — | Altium: 90° à borda (FATO); Murata e Vishay: **paralelo** (FATO); TDK: paralelo (NÃO VERIFICADO); divergência interna da literatura | FALTA; o dono decide (sugestão: paralelo, fonte primária do componente). |
| Furos M2.5 | §9: M2.5 nos cantos | KiCad M2.5 = 2,7 mm, pad 5,4 mm; HAT: 2,75 mm, NPTH preferido, área livre de 6,2 mm (FATO) | **CONFIRMA**; **falta** decidir NPTH ou anel no GND e o keepout da cabeça (Ø ≥ 5,9 mm). |
| Cantos arredondados | §9: "cantos arredondados" sem número | HAT R = 3 mm (FATO); raio interno ≥ 1 mm (INFERÊNCIA) | CONFIRMA; **falta** o número do raio externo e do raio interno mínimo. |
| Mínimos de silk | §9 e §11: "silk legível", zero avisos | JLC: ≥ 1,0 mm de altura, ≥ 0,15 mm de traço, proporção 1:6 (FATO) | **FALTA** o número; sugerido no Board Setup e no gate. |
| Cobre → borda | não especificado | JLC: 0,2 mm fresado, 0,4 mm V-cut (1,0 recomendado) (FATO) | **FALTA**; é mensurável e entra no gate §12. |
| Acabamento | não especificado | ENIG para passo ≤ 0,5 mm (JLC, FATO) | **FALTA**; o padrão da casa com ESP32-C5/QFN deveria ser ENIG. |
| Cor da máscara | §10: escolher silk branco ou tinta "conforme a máscara" | Preto e branco: ponte de 0,13 mm e opacos; os outros são translúcidos (FATO) | **FALTA** o critério técnico (ponte de máscara em QFN). |
| Teardrops e trilha a 45° ou arco | não mencionado | KiCad nativo (FATO) | FALTA (estética e robustez). |
| Espessura × edge-mount | §4: maioria dos edge-mount é de 1,6 mm | JLC: 0,4–2,0 mm FR-4; 0,4 mm sem V-cut; castellation ≥ 0,6 mm (FATO) | CONFIRMA (1,6 mm como padrão). |
| Arte em cobre × "zero avisos" | §11: zero avisos | Trilha decorativa ligada por uma ponta gera aviso de DRC (FATO, Hackaday) | Compatível se a arte for gráfico fora de net (INFERÊNCIA); vale registrar como técnica. |
| Gate mecânico §12 | mede conector↔borda | Pode incluir: raio interno, cobre↔borda, MLCC↔borda e furo, keepout de parafuso, corpo↔borda (PCBA) | **Sugestão de ampliação** (não editei o PADROES). |
| Placa grande e vazia | §13 erro 10: dimensionar pelo conteúdo | Formatos padrão (HAT 65×56,5; Feather 22,86×50,8) servem de referência de proporção; placa compacta exige mais cuidado com MLCC↔borda e corpo↔borda (FATO das regras 17, 35, 43, 44) | **CONFIRMA**, com a ressalva de que encolher aproxima peças da borda. |
| Geometria oficial | §9 e erro 8: partir do DXF/STEP oficial | O HAT é um exemplo de desenho oficial cotado (FATO) | **CONFIRMA.** |
| Render 2D/3D antes de fabricar | §9 e §11 | StepUp (colisão), STEP, pcb2blender (FATO) | CONFIRMA; acrescenta a checagem de interferência com a carcaça. |

## Bibliografia

### Fabricantes de PCB: capacidades e guias (consultados em 2026-11-20)
- JLCPCB — PCB Capabilities: <https://jlcpcb.com/capabilities/pcb-capabilities> (fonte principal dos números JLC; contém conflitos internos sobre trilhos e espessura máxima).
- JLCPCB — PCB Panelization: <https://jlcpcb.com/help/article/PCB-Panelization>
- JLCPCB — V-Cut Panelization Standards (blog): <https://jlcpcb.com/blog/v-cut-panelization-standards>
- JLCPCB — Terms and conditions of assembly service (regra de 2,5 mm): <https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service>
- JLCPCB — Minimum spacing for SMD components: <https://jlcpcb.com/help/article/minimum-spacing-for-smd-components>
- JLCPCB — In what cases will there be charged extra: <https://jlcpcb.com/help/article/in-what-cases-will-there-be-charged-extra>
- JLCPCB — HASL short circuits / quando usar ENIG: <https://jlcpcb.com/blog/how-to-resolve-short-circuit-hasl>
- JLCPCB — Incomplete milling of internal corners: <https://jlcpcb.com/blog/how-to-avoid-incomplete-milling>
- JLCPCB — Polarity and orientation identification guide: <https://jlcpcb.com/help/article/component-polarity-and-orientation-identification-guide>
- JLCPCB — Price adjustment ago/2026: <https://jlcpcb.com/news/jlcpcb-fr4-pcb-price-adjustment-august2026>
- JLCPCB — Correção de orientação no CPL (GitHub oficial): <https://github.com/JLCPCB/JLCPCB-SMT-Assembly-Components-orientation-fix>
- TechOverflow — "JLCPCB: Which milling tool radius is used for internal cutouts?" (2023, resposta do suporte): <https://techoverflow.net/2023/04/12/jlcpcb-which-milling-tool-radius-is-used-for-internal-cutouts>
- OSH Park — 2-layer specs: <https://docs.oshpark.com/services/two-layer/>
- PCBWay — Capabilities: <https://www.pcbway.com/capabilities.html>
- Sierra Circuits — DFM Handbook (96 p., gratuito, **atrás de formulário**; não baixado): <https://www.protoexpress.com/pcb-design-guides/dfm-handbook/>

### E-books / app notes (PDFs em `pdfs/06-dfm/`)
- Altium — *Design for Manufacturing: A Practical Guide for "Right the First Time" PCB Design* (guia gratuito; painelização, abas, V-groove, silkscreen e polaridade, desenho mestre, documentação): <https://resources.altium.com/p/dfm-guidebook>
- Knowles — *Flexibility of Multilayer Ceramic Capacitors* (zona de 5 mm, canto, fenda): <https://www.knowlescapacitors.com/getattachment/Products/Capacitors/SMDCap/Technical-Article-5mm-Board-Flex-(002).pdf?lang=en-US>
- Vishay — *Coping with the Risk of Board Flexure Damage to MLCCs* (5 mm, paralelo à borda, JIS C 5101-1 com 2 mm de flexão em 90 mm): <https://www.vishay.com/docs/49088/49088_technicalpaper.pdf>
- Murata — *Strain crack mechanism and preventive measures for MLCC* (web, ≥ 10 mm, slits): <https://article.murata.com/article/strain-crack-mechanism-and-preventive-measures-for-mlcc>
- TDK — FlexCrack countermeasures (o PDF do Mouser não baixou; a página da TDK devolve 403 para acesso automático; conteúdo citado só via resumo de busca): <https://product.tdk.com/en/products/solutionguide/mlcc_flex-crack.html>
- Raspberry Pi — HAT board mechanical specification (desenho oficial): <https://github.com/raspberrypi/hats>
- Raspberry Pi — HAT+ specification (CC BY-ND 4.0): <https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf>

### Documentação de ferramentas
- KiCad 9 PCB Editor (Edge.Cuts, Import Graphics, Teardrops, DRC de borda e texto, STEP): <https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html>
- Biblioteca oficial de footprints KiCad, `MountingHole.pretty`: <https://gitlab.com/kicad/libraries/kicad-footprints/-/tree/master/MountingHole.pretty>
- KiCad StepUp (FreeCAD): <https://github.com/easyw/kicadStepUpMod>
- KiKit panelize CLI: <https://yaqwsx.github.io/KiKit/latest/panelization/cli/> · KiKit fab JLCPCB: <https://yaqwsx.github.io/KiKit/latest/fabrication/jlcpcb/>
- pcb2blender: <https://github.com/30350n/pcb2blender>
- Regras JLC em `.kicad_dru`: <https://github.com/labtroll/KiCad-DesignRules> (KiCad 7)
- Fabrication Toolkit (bennymeg; BOM/CPL com campos de offset): <https://github.com/bennymeg/Fabrication-Toolkit>

### Formatos padrão
- Adafruit Feather Specification: <https://learn.adafruit.com/adafruit-feather/feather-specification>
- SparkFun Qwiic: <https://www.sparkfun.com/qwiic>
- mikroBUS (página oficial; 403 para fetch automático): <https://www.mikroe.com/mikrobus>

### Carcaça e light pipes
- Hubs — Enclosure design for 3D printing: <https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/>
- Altium — Light Pipes Explained: <https://resources.altium.com/p/light-pipes-explained>
- VCC/Mouser — LED indication validation (PDF): <https://www.mouser.com/pdfDocs/WhatEngineersMustActuallyValidateBeforeDeployingLEDIndication.pdf>

### Estética e arte em PCB
- Hackaday — Designing Aesthetically-Pleasing PCBs (2023): <https://hackaday.com/2023/01/15/designing-aesthetically-pleasing-pcbs>
- Hackaday.io — Make your own PCB art (Ian Dunn): <https://hackaday.io/project/188607-make-your-own-pcb-art/details>
- Hackaday.io — Making a SAO with Inkscape and KiCad: <https://hackaday.io/project/202784-making-a-sao-with-inkscape-and-kicad>
- Adafruit — Making wearable badge art with PCBs: <https://learn.adafruit.com/making-wearable-badge-art-with-printed-circuit-boards?view=all>
- SparkFun — Better PCBs in Eagle: URL antiga sparkfun.com/tutorials/115 devolve **404** (2026-11-20); não lido.

### Normas (só citar; pagas, não baixar)
- ISO 273:1979 (confirmada em 2024) — furos de passagem para parafusos: <https://www.iso.org/standard/4183.html>
- IPC-2221 (projeto genérico de PCB), IPC-7351 (land patterns), IPC-A-610 (aceitabilidade de montagem), IPC-4552 (ENIG; a OSH Park declara conformidade).

### Livros (não baixar; referência)
- Peter Dalmaris, *KiCad Like a Pro* (Tech Explorations; várias edições): fluxo KiCad até a fabricação. Edição e conteúdo de painelização NÃO VERIFICADOS nesta rodada.
- No Starch Press, *Practical PCB Design* (capítulo de amostra 5 gratuito: <https://nostarch.com/download/samples/practical-pcb-design-chapter-5.pdf>). Autor, edição e conteúdo NÃO VERIFICADOS (apareceu só em resultado de busca).
- Nenhum livro foi lido nesta rodada; as regras acima vêm de fabricantes e da documentação das ferramentas.
