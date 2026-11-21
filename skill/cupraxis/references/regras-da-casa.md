# Padrões de projeto de PCB — programa 9-PCB

> Documento-mãe de **como projetamos placas**. É **universal**: vale para qualquer PCB — produto autônomo, placa com RF, IoT/bateria, periférico USB, shield/HAT/módulo que encaixa em outro aparelho (host), ferramenta de teste etc. Consolidado em 2026-11-19 a partir das decisões e correções do dono; os casos reais citados vêm do primeiro projeto do programa (AirScope, um módulo de RF para um host portátil) e aparecem só como **exemplo** — a regra é sempre a geral. Ler ANTES de iniciar o esquemático ou o layout de qualquer placa nova.
>
> **Etiqueta `[FLIPPER]`:** marca conteúdo que vem da documentação oficial da Flipper Devices (Flipper Zero/One) e só se aplica a placas que encaixam nesses aparelhos. Fora disso, vale a regra geral do parágrafo.
>
> Regras de entrega (DRC/nets/GND) e de infraestrutura (DevShared, Freerouting, saída) continuam nos documentos próprios; aqui ficam as regras de **projeto físico e elétrico**.

---

## 1. Camadas da placa (stackup)

- **Padrão de protótipo simples (sem RF crítico, sem energia própria):** 2 camadas.
- **Usar 4 camadas sempre que houver QUALQUER um destes:**
  - **RF que precisa funcionar de verdade** (trilha de antena, casamento 50 Ω). As 4 camadas dão plano de GND sólido imediatamente abaixo da trilha → microstrip 50 Ω real, não "50 Ω de olho".
  - **Distribuição de energia limpa** (bateria, buck, vários LDOs).
  - **Muitas ilhas de GND** que não fecham em 2 camadas — 4 camadas resolve de forma **estrutural** (plano contínuo), em vez de remendar ilha por ilha.
- **Regra prática:** o número de camadas é decidido pela **necessidade elétrica (RF + energia)**, NÃO pela bateria sozinha. Uma placa com RF sério vai a 4 camadas mesmo sem bateria.
- Stackup de referência JLCPCB para 4 camadas: `JLC04161H-7628` (confirmar na calculadora de impedância da fábrica a largura de trilha para 50 Ω no dielétrico real, antes de rotear o RF).

---

## 2. Posicionamento térmico e de desempenho

- **Espalhar os geradores de calor** (MCUs, reguladores, PA de rádio) pela placa — **não** amontoar. Ex.: com 2× ESP32-C5, colocar **um em cada metade** da placa. Dissipa calor e, no caso de rádios da mesma banda, reduz interferência mútua (ver §3).
- **Aproximar o que tem de ficar perto:**
  - Cristais/ressonadores **colados** ao pino do MCU/rádio, com os capacitores de carga ao lado.
  - Capacitores de desacoplamento **imediatamente** nos pinos de alimentação do chip.
  - Redes de casamento de RF **junto** à saída de antena do chip (trilha curtíssima).
- **Reguladores** perto da carga que servem, com os capacitores de entrada/saída ao lado.
- Deixar folga térmica/espaço de montagem — não encostar corpos de componentes nem invadir cortesia (courtyard).

---

## 3. RF e antenas (precauções obrigatórias)

- **Trilha de RF o mais curta e direta possível:** cada chip de rádio fica **imediatamente abaixo da sua antena**.
- **Impedância 50 Ω controlada** (microstrip sobre plano de GND sólido — exige 4 camadas, ver §1). Largura calculada no stackup real da fábrica.
- **Isolamento entre rádios:**
  - Rádios da **mesma faixa** (ex.: nRF24 e Wi-Fi, ambos 2,4 GHz) ficam **separados** ao longo da borda, nunca lado a lado → reduz dessensibilização.
  - Receptor sensível (GPS) **afastado** dos transmissores (Wi-Fi/sub-GHz).
  - Confirmar isolamento entre antenas adjacentes (parâmetro S21) e seguir a nota de aplicação de cada fabricante.
- **Shield cans (gaiolas de blindagem)** sobre chips de RF **nus** (ex.: CC1101, nRF24): moldura soldável + tampa, com anel de vias de GND no contorno. Módulos que **já vêm blindados de fábrica** (ESP32-WROOM, MAX-M10S) **não** precisam de can.
- **Antena ativa (GPS):** se for usar antena com LNA, prever **bias tee** (choke + capacitor de bloqueio DC) para alimentar a antena pela própria trilha. Antena passiva dispensa.
- **Redes de casamento:** usar sempre a rede **oficial do fabricante** (datasheet/reference design), salva em `referencias/rf-reference-designs/`. Nunca inventar valores sem instrumentação de RF.

---

## 4. Conectores de antena

- **Padrão: SMA fêmea edge-mount de 50 Ω** na borda — é o que dá a transição coaxial limpa e a cara de produto. **NÃO usar SMA vertical through-hole** (parafusa pra cima) a não ser em protótipo descartável.
  - Atenção à espessura: a maioria dos edge-mount é para placa de 1,6 mm. Se a placa for mais fina (1,0–1,2 mm), achar a variante correta OU ajustar a espessura da placa conscientemente. **Confirmar peça de catálogo (JLCPCB/LCSC) antes de fechar o layout.**
- **Alinhar todas as antenas** na mesma borda, com espaçamento regular (~18 mm entre centros é um bom alvo), respeitando o isolamento do §3.
- Outros conectores (u.FL, pigtail) só quando o **módulo obriga** — ex.: ESP32-C5-WROOM-1U só expõe a antena por u.FL, então o Wi-Fi vai ao SMA por **pigtail u.FL→SMA** (limite do módulo, não do layout).

---

## 5. Componentes de ação manual → sempre na BORDA

Tudo que o usuário **toca, encaixa ou conecta** precisa alcançar a borda da placa e estar **acessível de verdade** (a carcaça só leva recortes de borda):

- **USB-C, microSD, botões (RESET/BOOT), LEDs, SMA, conectores de fio/expansão.**
- **Face de inserção voltada para fora:** o slot do microSD e a boca do USB-C têm que ficar **na linha da borda**, não recuados — senão o cartão/cabo não entra (erro já cometido: "toco" de placa sobrando na frente do slot; placa foi aparada até a boca do conector).
- **USB-C não pode ficar no miolo da placa** — tem que chegar à borda para o cabo encaixar.
- Bateria, chips e passivos ficam **internos**; só o que precisa de acesso vai à borda.
- Posicionar os botões onde o dedo alcança sem desmontar nada.

---

## 6. USB-C e gravação de firmware (flash)

- **Gravar firmware por USB-C é regra — não pode faltar.** Nada de header UART solto no meio da placa para ligar adaptador serial à mão (gambiarra; foi o caso do `J15` na AirScope).
- **Mais de 1 MCU na mesma placa → hub USB** (ex.: FE1.1s / CH334) atrás de **1 único USB-C**, para **todos os MCUs flasharem pelo mesmo cabo**. Isso **elimina** os headers de flash avulsos e os test pads.
- Prever o circuito de **auto-boot** adequado ao MCU (ex.: MCU ligado por ponte USB-UART → circuito clássico de dois MOSFET-N cruzados DTR/RTS→EN/BOOT, como nas dev boards oficiais da Espressif e na devboard Wi-Fi oficial do Flipper `[FLIPPER]`; MCUs com USB nativo, como ESP32-C3/C5/S3, podem dispensá-lo — conferir o datasheet). Validar antes de fabricar.

---

## 7. Energia

- **Decidir cedo:** a placa roda pendurada em outra fonte (host, barramento, USB, fonte de bancada — ex. `[FLIPPER]`: 3V3 do GPIO do Flipper Zero, limite 1,2 A) ou precisa de energia própria?
- **Usar energia própria (bateria) quando houver QUALQUER um:**
  - A fonte externa **cai no meio da operação** (ex. `[FLIPPER]`: o Flipper Zero derruba o próprio 3V3 ao montar o microSD / atualizar firmware → a placa reinicia no meio da tarefa).
  - **Uso destacado** é um recurso de produto (logger portátil, uso sem o host).
  - O consumo de pico (vários rádios / 2 MCUs em TX) encosta no limite da fonte externa.
- **Cadeia de energia padrão com bateria 1S LiPo:** `USB-C (5V) → carregador com POWER-PATH (VSYS) ← bateria LiPo 1S (proteção/PCM + JST) → conversor BUCK-BOOST p/ 3,3 V (≥2A) → rail único 3,3 V`.
  - **Por que buck-boost e não buck:** a LiPo 1S varia de ~4,2 V (cheia, ACIMA de 3,3 V e acima do limite de 3,6 V do ESP32) a ~3,0 V (vazia, ABAIXO de 3,3 V). Só buck-boost mantém 3,3 V estável nessa faixa; buck simples perderia metade da descarga e boost não cobriria a bateria cheia.
  - **Por que power-path no carregador:** a placa opera ligada no USB (flash/uso) ao mesmo tempo em que carrega — sem power-path a terminação de carga se confunde. Conferir carregador com power-path/VSYS na LCSC antes de fechar (ex.: família BQ2407x / MCP73871).
  - **Isolamento de ruído entre rádios NÃO se faz com LDO em cima de rail igual** (LDO não tem headroom de 3,3→3,3). Faz-se com **ferrite bead + filtro LC (bead + capacitor local)** na entrada de alimentação de cada rádio, a partir do rail único de 3,3 V. Separa o ruído de chaveamento sem perda de headroom.
  - **Back-feed na fonte externa:** com bateria própria, o TX de UART do MCU pode energizar o host desligado pelo pino de RX. Proteger com resistor série na linha de UART (ou gating).
- Do host/fonte externa fica **só controle (ex.: UART + GND)** quando houver bateria.
- **Bateria:** preferir célula com proteção; lembrar da certificação **UN38.3** no transporte e do espaço dela na carcaça. Nada de bateria solta não certificada em produto vendido.

---

## 8. Conexões extra para futuro (sempre prever)

- **Sempre adicionar pontos de expansão** baratos em espaço, para aprimoramentos futuros, mesmo que não usados agora:
  - **Conector I²C QWIIC (JST-SH)** — padrão Adafruit/SparkFun, abre add-ons prontos.
  - **Header de expansão** (ex.: 1×6: 5V / 3V3 / GND / UART TX / RX / GPIO) — permite plugar outro módulo ou um host futuro (ex.: Raspberry).
- Deixar **pads/jumpers de configuração** (0 Ω) para habilitar/desabilitar caminhos (ex.: "USB-only", separar alimentação) sem respin.
- Não exagerar: expansão é baixo custo em espaço, mas cada conector vai à borda (§5) e entra no plano da carcaça.

---

## 9. Shape (formato) e estética

- **Formato com cara de produto:** retângulo com **cantos arredondados**, proporção equilibrada, nada de placa "em pé" desproporcional.
- **Furos de montagem M2.5** nos cantos (padrão), alinhados.
- Respeitar o **gabarito mecânico** quando a placa encaixa em outro aparelho ou carcaça (formatos padrão como Raspberry Pi HAT, Arduino shield, Feather, mikroBUS; módulo de expansão de um host; gabinete comercial): furos, cotas, entalhes/degraus, folgas. O conector de encaixe (ex.: GPIO) fica **dentro do entalhe, colado à borda**, não recuado para dentro.
- **SEMPRE partir do arquivo OFICIAL do fabricante para geometria de encaixe — NUNCA inventar cotas de memória.** Procurar o DXF/STEP/KiCad oficial ANTES de desenhar o contorno/conector. Guardar o arquivo oficial em `referencias/<host-ou-padrão>/` e extrair dele contorno, furos e posição do conector.
  - `[FLIPPER]` *Exemplo (módulo externo do Flipper Zero, desenho oficial Flipper Devices):* `referencias/flipper-zero/gpio/flipper-external-module-pcb-outline.dxf` → largura **67,34 mm**, 2 abas (degrau), headers 8-pin + 10-pin a **38,1 mm** centro-a-centro, furos a 3,84 mm da ponta da aba, pitch 2,54. (Erro já cometido: inventar 35,55 mm e contorno sem degrau — reprovado.)
- Componentes alinhados e agrupados por função; silk organizado e legível; referências sem colidir com pad/silk vizinho.
- Conferir **visualmente** o resultado (render 2D + visor 3D) antes de fabricar.

---

## 10. Branding (logo na placa)

- Colocar o **logo AUVORIX** no silkscreen (F.Silkscreen) de toda placa.
- Fonte dos assets: `<BRANDING>\logo\svg\`.
- **Silkscreen é cor única** → usar os arquivos **mono**:
  - Símbolo: `auvorix-simbolo-mono-branco.svg` (ou `-mono-tinta.svg`).
  - Wordmark: `auvorix-wordmark-mono-branco.svg` (ou `-mono-preto.svg`).
  - Lockup horizontal single-color: `auvorix-lockup-horizontal-branco.svg`.
- Escolher branco/tinta conforme a cor da máscara de solda. Importar via `import_svg_logo` no KiCad.
- Incluir também: nome do produto, versão da placa e, se couber, um pequeno aviso de uso legal (em ferramentas de pentest).
- O logo é marca própria do dono — sem questão de licença; assets de terceiros (footprints/símbolos/3D) continuam registrados em `LICENSES.md` do projeto.

---

## 11. Qualidade de entrega (resumo — detalhe nos docs próprios)

Antes de anunciar qualquer placa como pronta:
- **Rodar TODOS os testes** sem exceção: ERC (esquemático), DRC (placa), e as verificações de higiene (courtyard/overlap, off-grid, paridade esquemático↔placa, silk). Não pular nenhum.
- **Zero erros E zero avisos de QUALQUER tipo — inclusive os cosméticos/estéticos** (sobreposição de silk, referência colidindo com pad, texto fora da placa, off-grid). Nenhum erro pode ficar sem resolução; "é só cosmético" NÃO é desculpa para deixar passar. Se um aviso for genuinamente impossível de limpar, documentar o porquê com fonte — não apenas ignorar.
- **DRC zero** (0 erros, 0 avisos).
- **Nets 100% roteadas** (0 unrouted).
- **Ilhas de GND fechadas** (idealmente plano contínuo de 4 camadas).
- **USB de flash presente** (§6).
- Fabricação em `saida/fab/`, BOM/CPL gerados, render conferido, `LICENSES.md` atualizado.
- Nada genérico/improvisado: asset profissional ou deixar de fora e registrar pendência.

---

## 12. Checklist rápido de layout

> **REGRA DE ORDEM — obrigatória (ordem do dono, 2026-11-19):** **SEMPRE organizar/posicionar bem os componentes ANTES de rotear.** Primeiro o *placement* (floorplan por função, clusters colados aos seus chips, conectores na borda, térmico/RF separados, gate mecânico de borda, zero overlaps/courtyard) e **só então** rotear (Freerouting/manual). Nunca rotear sobre um placement provisório: mover peça em placa já roteada quebra trilhas, cria ilhas de GND e vira retrabalho (já aconteceu ao mover J4/J17). Toda mudança que adiciona/move peça recomeça pelo placement.

- [ ] **Placement revisado e aprovado ANTES de rotear** (floorplan limpo por função, clusters nos chips, conectores na borda, sem overlaps/courtyard, gate mecânico OK) — rotear é a ÚLTIMA etapa.
- [ ] Camadas decididas pela necessidade de RF/energia (não só bateria).
- [ ] Geradores de calor espalhados; rádios da mesma banda separados.
- [ ] Cristais, desacoplamento e redes de casamento colados aos chips.
- [ ] Trilha de RF curta, 50 Ω, sobre GND sólido; shield can nos chips de RF nus.
- [ ] Antenas alinhadas na borda, SMA edge-mount, espaçamento/isolamento OK.
- [ ] USB-C, microSD, botões, SMA, expansão → todos na BORDA, face voltada pra fora.
- [ ] Flash por USB-C; hub USB se houver >1 MCU; sem header serial solto.
- [ ] Energia: fonte externa aguenta? Se não → bateria + power-path + **buck-boost** (não buck+LDO) + ferrite/LC por rádio (§7).
- [ ] **Geometria de encaixe tirada do arquivo OFICIAL do fabricante (DXF/STEP), não inventada** (§9).
- [ ] Pontos de expansão previstos (QWIIC + header + jumpers de config).
- [ ] Shape arredondado, furos M2.5, gabarito mecânico respeitado, conector de encaixe no entalhe/borda.
- [ ] Logo AUVORIX (mono) + nome + versão no silk.
- [ ] TODOS os testes rodados (ERC, DRC, courtyard, off-grid, paridade, silk); **zero erros e zero avisos, inclusive cosméticos**.
- [ ] DRC zero, nets 100%, GND fechado, render conferido.
- [ ] **Conferência MECÂNICA de borda (gate obrigatório — DRC/ERC NÃO pegam isso):** medir numericamente a distância de cada conector de acesso (SMA, USB-C, microSD, conector de encaixe/expansão) à `Edge.Cuts`. SMA edge-mount com barril PRA FORA (não recuado/enterrado); USB-C/microSD com a boca NA borda; conector de encaixe nas posições/abas do gabarito oficial. (Erro já cometido: SMA 15 mm dentro, USB-C/SD recuados, conector de encaixe sem o degrau do gabarito — tudo passou no DRC.)

---

## 13. Erros já cometidos e correções — NÃO repetir

> Catálogo de erros reais (cometidos no projeto AirScope) e a regra **geral** que impede a repetição em qualquer placa. Ler antes de iniciar/entregar qualquer placa.

### Mecânica de borda e encaixe (o que mais deu erro — DRC/ERC NÃO pegam)
| # | Erro cometido | Correção / regra permanente |
|---|---|---|
| 1 | **SMA fêmea 15 mm DENTRO** da placa (pads longe da borda) | Edge-mount com pads **na borda**; medir distância pad→`Edge.Cuts`. §4, §12 |
| 2 | **SMA "enterrado"/plantado** na placa (recuado ~3 mm → barril sobra sobre o cobre) | Puxar o conector **flush na borda** (pad ~1–1,5 mm da borda) → barril sai pra fora; conferir em 3D (vista da borda). §4 |
| 3 | **USB-C recuado 2,3 mm** da borda (cabo não encaixa) | Boca do USB-C **na linha da borda** (frente do corpo em cima da `Edge.Cuts`). §5 |
| 4 | **microSD** desalinhado da borda | Boca do slot **na borda**; card entra pela borda. §5 |
| 5 | **Conector de encaixe sem o degrau/entalhe do gabarito** (placa virou retângulo liso ao refazer) | Contorno sempre do DXF oficial do host/padrão (no caso `[FLIPPER]`: as 2 abas do módulo externo). §9 |
| 6 | **Espaçamento de conector inventado** (35,55 mm) | Cota tirada do desenho oficial (no caso `[FLIPPER]`: 38,1 mm centro-a-centro). §9 |
| 7 | **Header right-angle com pinos apontando PRA DENTRO** da placa | Header right-angle: a direção do pino é acoplada à ordem dos pads. Inverter p/ pino pra fora (muda o lado do pino 1 — conferir contra o pino 1 do host) **ou** montar o header no lado de baixo (B.Cu, de frente pro host). §9 |
| 8 | **Inventar cotas de memória** em vez de usar o arquivo do fabricante | **SEMPRE** partir do DXF/STEP/KiCad oficial (ex. `[FLIPPER]`: `referencias/flipper-zero/gpio/…dxf`). §9 |

### Processo e verificação
| # | Erro cometido | Correção / regra permanente |
|---|---|---|
| 9 | **Declarar "pronto" confiando só em DRC/ERC/courtyard** | DRC/ERC **não checam mecânica** (borda, encaixe, acesso). Rodar o **gate mecânico de borda** (§12) + conferir 3D antes de entregar. |
| 10 | **Placa enorme e vazia** (220×100 p/ ~130 peças) | Dimensionar pelo conteúdo; encolher (ex.: AirScope foi p/ 150×80). §9 |
| 11 | **Netclass Power não aplicou no DSN** (+3V3 roteado em 0,2 mm) | Conferir larguras das trilhas de energia **depois de rotear**; alargar rails de pico (2 ESP). §1/§7 |
| 18 | **Rotear antes de organizar os componentes** (e depois mover peça em placa roteada) | **Placement primeiro, rotear por último** (regra de ordem §12). Mover peça roteada quebra trilhas/ilhas → retrabalho. Toda adição/mudança de peça recomeça pelo placement. |
| 19 | **Mover/espalhar componentes numa placa ainda ROTEADA sem ripar as trilhas ANTES** (AirScope v4, des-densificação) | As 1467 trilhas antigas ficaram apontando pros lugares velhos dos pads → **curtos/violações fantasma** (194 no Freerouting), que pareciam ser da nova disposição mas eram lixo de trilha. **Regra: rip-up TOTAL de trilhas/vias ANTES de qualquer movimentação de peça** (ripar → mover → re-rotear). **Como detectar:** `grep -c "(segment" placa.kicad_pcb` nos backups — se a placa "des-densificada/sem rota" ainda acusa segmentos, as trilhas NÃO foram removidas (a densa e a espalhada tinham ambas 1467). |
| 20 | **Footprint escolhido pelo NOME do encapsulamento, sem conferir o desenho do fabricante** (AirScope v4, hub FE1.1S U12) | "SSOP-28" foi posto como `SSOP-28_5.3x10.2mm_P0.65mm`, mas a peça real (LCSC C9359) é **SSOP-28 150 mil (3,9×9,9 mm, passo 0,635)** — o chip não assentaria; só foi pego na hora de montar a BOM, **depois** da placa roteada e com DRC 0. **Regra: ao gravar o código LCSC de cada CI, abrir o datasheet e comparar corpo, passo e largura entre pontas dos terminais com o footprint** (o campo `package` da JLC já denuncia: "SSOP-28-150mil"). Troca pós-rota = desvios locais verificados; **não** usar Freerouting parcial (o DSN não leva zonas → redes de plano aparecem "abertas" e ele faz lixo). |
| 21 | **Ler o `stock` da base local (`jlcpcb_parts.db`) como estoque de MONTAGEM da JLC** | O campo é o estoque da **LCSC** (comprável), não o do armazém de montagem. Base atualizada no mesmo dia ainda dizia ESP32-C5 = 473, mas no pedido a JLC mostrava **0** e travou. **Regra: o estoque de montagem só se confirma no site (etapa BOM do pedido). Peça com estoque LCSC e 0 na JLC = pré-comprar para o "My Inventory" antes.** Atualizar a base: `download_jlcpcb_database(force=true)` (fonte cdfer, ~400 MB). |

### Esquemático / componentes (1ª rodada AirScope)
| # | Erro cometido | Correção / regra permanente |
|---|---|---|
| 12 | **Cristal 2-pin em footprint de 4 pads** (pad 2 = case/GND) → não oscilaria | Usar `Device:Crystal_GND24` + footprint 4-pin (ex.: `Crystal_SMD_3225-4Pin`); eletrodos 1,3 / GND 2,4. |
| 13 | **Pino de teste do hub (FE1.1s TESTJ) ligado a GND** → modo de teste, não enumera | Ler o datasheet do pino: TESTJ é active-low c/ pull-up → **pull-up p/ 3V3**, não GND. |
| 14 | **Load caps externos no cristal do hub** | FE1.1s tem load caps **integrados** → remover os externos (detunam). |
| 15 | **SMA vertical** em vez de edge-mount | Regra: **SMA edge-mount** (§4). |
| 16 | **Header UART solto (J15) no meio da placa** p/ flash manual | Flash por USB-C + **hub** (§6); sem header serial avulso. |
| 17 | `no_connect` órfãos → falso "NC conectado" no ERC | Remover no_connects que sobraram após editar o esquemático. |

### Regras de entrega (reforço)
- **Zero erros E zero avisos** em TODOS os testes (ERC, DRC, courtyard, off-grid, paridade, silk) — inclusive cosméticos (§11, §12).
- **Nada vai à fábrica sem ordem expressa do dono** e sem a conferência física/visual dele.

---

## 14. Correções técnicas de arquitetura e roteamento (origem: AirScope v2; valem para qualquer placa)

> Boas práticas elétricas/de layout que corrigimos no re-placement v2. Aplicar como regra em todas as placas.

### Energia e corrente
- **Agrupar a energia no mesmo quadrante da entrada USB-C.** Carregador (power-path), buck-boost, indutor e conector de bateria juntos, perto do USB-C — para as trilhas de **alta corrente (VBUS / VSYS / VBAT) serem curtas** e não cruzarem a placa por baixo de áreas sensíveis.
- **Fonte chaveada (SMPS) longe dos front-ends de RF.** O nó de chaveamento do indutor do buck-boost irradia: colocar a seção chaveada **num canto inferior**, nunca sob os CIs de RF (CC1101/GPS/nRF24).
- **Netclass de energia com trilha larga** (ex.: 0,5–0,8 mm; o +3V3 precisa aguentar o pico dos 2 ESP). **Conferir a largura DEPOIS de rotear** — a netclass pode não ser aplicada no DSN/Freerouting (já aconteceu: +3V3 saiu em 0,2 mm).
- **USB-C como sink/UFP: dois resistores de 5,1 kΩ independentes** (CC1 e CC2) — conformidade. Conferir que existem os dois (não um só).

### RF
- **CIs de RF próximos da borda/antena** → trilha de 50 Ω mais curta, menos perda de inserção.
- **Rede de casamento compacta, colada ao pino de RF do chip, com saída ÚNICA** em linha coplanar aterrada (**CPWG) de 50 Ω** direta até o SMA. Não fragmentar/espalhar a rede. Largura de 50 Ω calculada no stackup real (calculadora JLCPCB).
- **Cercas de via (via stitching fences) separando os domínios de RF** quando há várias antenas paralelas — isola os canais; GND contínuo na camada logo abaixo. (Shield cans: só lata SMT montável — senão fica p/ versão validada.)
- **u.FL do módulo (ex.: ESP32-C5-WROOM-1U) virado para a sua antena/SMA**, com raio de curvatura do pigtail adequado (não forçar o conector).

### Cristais e desacoplamento
- **Caps de carga do cristal simétricos e colados** aos pads, com plano de GND sólido contínuo imediatamente abaixo.
- **Desacoplamento colado aos pinos de alimentação** de cada CI (não alinhado longe).

### Conectores e mecânica
- **Conectores de acesso (bateria, expansão QWIIC/header) FORA da borda de encaixe no host.** Na mesma borda do conector que pluga no host, o cabo colide com a carcaça do host → mover para outro quadrante ou **rotacionar 90° (saída lateral)**. (A bateria é interna: o cabo fica dentro da carcaça, mas ainda assim não deve ocupar a região do dock.)
- **Botões agrupados por função/por chip** (cada ESP com seu BOOT/RESET perto dele); acionamento acidental resolve-se **rebaixando/recuando na carcaça**, não reorganizando a eletrônica.
- **Compactar a área ociosa**: subir a RF e consolidar digital/energia na base reduz a altura do PCB (menos torque de alavanca sobre os pinos do conector de encaixe) — sem apertar o espaço de roteamento.

---

## 15. Técnica de roteamento que FUNCIONOU (validada na AirScope v4, 2026-11-20) — receita para qualquer placa

> Levou a placa de "96% e travada" para **100% roteada, DRC 0 violações / 0 não-conectados / 0 paridade**. Scripts salvos em `referencias/scripts-roteamento/` (genéricos: recebem o `.kicad_pcb` por argumento).

### Receita, na ordem
1. **Backup** do `.kicad_pcb` antes de cada etapa (`.bak-<etapa>`).
2. **Ripar TUDO primeiro** — `ripup.py placa.kicad_pcb` (remove segmentos/vias/arcos de nível superior). Nunca mover peça com trilha na placa (erro nº 19 do §13). Conferir: `grep -c "(segment" placa.kicad_pcb` deve dar **0**.
3. **Des-densificar** — `spread.py placa.kicad_pcb`: afasta componentes amontoados (push-apart com âncora na posição original). **Ficam fixos**: conectores (`J*`), furos (`H*`), chaves (`SW*`), cristais (`X*`), chips de RF e tudo na faixa de RF junto às antenas. Parâmetros: `GAP`, `ANCHOR`, raios por footprint. Na AirScope: raios ampliados, GAP 0,6, ANCHOR 0,010 → 70 peças movidas 1–5 mm. Depois: `check_courtyard_overlaps` = 0.
   - *Por que funciona:* o autorouter não falhava por largura de trilha, e sim por **falta de canal** entre pads de CIs vizinhos. Poucos milímetros de folga abrem os canais.
4. **Autoroutear** — `export_dsn` → Freerouting em background (`java -jar freerouting.jar -de x.dsn -do x.ses -mp 50`) → `import_ses`. **Sinal de DSN saudável:** tamanho igual ao de uma placa sem rota (AirScope: ~104 KB; o DSN "sujo" com trilha velha tinha 241 KB). Resultado: score 1000, 0 unrouted.
   - Não reexportar DSN de placa já roteada pelo backend (round-trip infiel). Sempre a partir de placa ripada.
5. **Aterrar os pads de GND isolados** — `gnd_fix.py placa.kicad_pcb relatorio_drc.json` (rodar com o Python do KiCad: `KiCad\10.0\bin\python.exe`, que tem `import pcbnew`). Para cada pad de GND listado como não-conectado:
   - procura em anéis um ponto de **via** com folga contra trilhas/vias/pads de outras redes em **todas as camadas** (via passante), fora de keepouts e sem cair em cima de pad;
   - liga pad→via com **trilha reta curta verificada** em F.Cu;
   - se não achar: liga o pino ao **EP do próprio CI** (entrada perpendicular); se ainda não, rota em **"L"** (ponto intermediário);
   - modo fino (4º argumento) para casos apertados; aceita também lista `REF NUM` em `.txt`.
   - *Por que os atalhos falham:* via 0,6 mm centrada em pino de passo 0,5 mm encosta no vizinho; `route_pad_to_pad`/`route_trace` do backend são **retos** e cruzam pads; grade de stitching cai no pour principal e não na ilha do pino.
6. **Aterrar ilhas do pour** — `island_fix.py placa.kicad_pcb x`: percorre cada região preenchida das zonas de GND; a que não tiver via/pad passante de GND dentro recebe uma via num ponto livre (via térmica no centro quando for EP grande). As pequenas demais saem em `island_pads.txt` → passar para o `gnd_fix.py`. Atenção: **EP também pode ser ilha** — ligar pino ao EP só resolve se o EP tiver caminho ao plano.
7. **Refill + salvar** pela API (`pcbnew.ZONE_FILLER(board).Fill(board.Zones())`, `SaveBoard`) e **DRC oficial**: `kicad-cli pcb drc --format json --severity-all --schematic-parity`. Repetir 5–7 até 0 não-conectados.
8. **Cosméticos por script** (API pcbnew): espelhar texto do verso, reposicionar referências de silk (respeitar altura mínima de texto da placa), salvar footprints customizados na lib do projeto e reapontar o FPID (some o `lib_footprint_mismatch`), marcar furos de montagem como *board only*, sincronizar campos com o esquemático.
9. **Gate mecânico de borda** (bbox de cada conector vs Edge.Cuts) + render/3D → só então gerar fab.

### Regras que saíram disso
- **Automação geométrica > clique por screenshot.** Com a API do KiCad dá para checar folga de verdade antes de criar cobre; operar o roteador interativo por imagem numa placa densa não converge.
- **Ensaio a seco primeiro** (`dry`): o script lista o que conseguiria fazer sem gravar nada.
- **DRC oficial depois de cada passo**; se piorar, voltar ao backup em vez de remendar.
- **BOM não é detalhe:** conferir códigos LCSC cedo — na AirScope a placa ficou limpa e a montagem continuou bloqueada por 143 peças sem LCSC.

---

## 16. Sourcing pelo banco local da JLCPCB (validado na AirScope v4, 2026-11-20)

> Em vez de pesquisar peça por peça, consultar **direto por SQL** o banco que o KiCAD-MCP baixa. Levantou ~90 linhas de BOM em minutos. Scripts em `referencias/scripts-bom/`.

### Onde está e como é
- Arquivo: `%USERPROFILE%\.kicad-mcp\data\jlcpcb_parts.db` (SQLite, ~556 mil peças; atualizar com `download_jlcpcb_database` do MCP).
- Tabela `components`: `lcsc` (chave), `category`, `subcategory`, `mfr_part`, `package`, `manufacturer`, `library_type` (`Basic`/`Extended`), `description`, `stock`, `price_json`. Há também `components_fts` (busca de texto).
- É um **snapshot**: estoque, preço e Basic/Extended podem ter mudado → **conferir no site antes de encomendar**.

### Como consultar
- `jlc_query.py "<cláusula WHERE>" ...` — imprime LCSC, classe, peça, encapsulamento, estoque e descrição. Aceita várias consultas de uma vez.
- Ordenação padrão para escolher: `order by (library_type='Basic') desc, stock desc` (Basic primeiro, depois maior estoque).
- **Python no Windows:** com `python -I` a variável `PYTHONIOENCODING` é ignorada e o `℃`/`Ω` das descrições quebra o print → pôr `sys.stdout.reconfigure(encoding='utf-8')` no script.

### Padrões de consulta que funcionaram
| Peça | WHERE |
|---|---|
| CI / conector por código do fabricante | `mfr_part like 'TPS63020%'` |
| Conferir códigos já conhecidos | `lcsc in ('C15464','C15483')` |
| Resistor 0402 1% | `category like '%Resistor%' and package='0402' and description like '% 10kΩ %' and description like '%±1%'` |
| Capacitor por dielétrico | `category like '%Capacitor%' and package='0402' and description like '100nF %' and description like '%X7R%'` |
| Capacitor de RF | idem com `(description like '%C0G%' or description like '%NP0%')` |
| Indutor de RF | `category like '%Inductor%' and package='0402' and description like '%27nH%' and (mfr_part like 'LQG15%' or mfr_part like 'LQW15%')` |
| Cristal | `category like '%Crystal%' and package like '%3225%' and description like '%26MHz%'` (a carga em pF aparece na descrição) |
| LED por cor | `package='0603' and (category like '%LED%' or category like '%Opto%') and description like '%Green%'` |

Armadilhas: a ordem dos campos na descrição varia (ex.: `50V 8.2pF` e não `8.2pF 50V`) → se `like '8.2pF %'` não achar, usar `like '%8.2pF%'`; nomes de categoria se repetem com grafias diferentes → usar `like '%Resistor%'`.

### Regras de escolha
- **Basic primeiro** (sem taxa); cada tipo Extended custa ~US$3 de setup por pedido — somar e avisar o dono.
- **RF:** só C0G/NP0 nos capacitores de casamento e de carga de cristal; indutor da série da referência do fabricante (Murata LQG15HS/LQW15A).
- **Cristal:** escolher a carga (CL) pelos capacitores que já estão na placa: CL ≈ C/2 + ~2–3 pF de parasitas; conferir ESR máximo do CI.
- **Conector/eletromecânico:** se o `mfr_part` do footprint **não existe** na base (aconteceu com o USB-C GCT USB4105 e o SMA Amphenol 132289), **não assumir equivalente**: ou troca-se o footprint para a peça que a JLC tem, ou a peça vem por fora. Decisão do dono.
- **Estoque baixo** (ex.: MAX-M10S com 68) → sinalizar para lote maior.
- Entregar a proposta em tabela (`docs/bom-lcsc-proposta-<versão>.md`) e **só gravar no esquemático depois da aprovação**; aí regenerar BOM/CPL e conferir rotações no visualizador da JLC.
- **Fazer isso cedo**, junto com a escolha de footprints — não depois de rotear.

---

## 17. Resolução dos conflitos com a literatura (2026-11-21, ordem do dono: "corrija as pendências")

> Fecha os itens A1–A16 de `boas-praticas/00-conflitos-e-lacunas.md`. **Onde este parágrafo diverge das seções anteriores, ele prevalece.** As fontes estão nos temas indicados entre colchetes.

| # | Regra adotada |
|---|---|
| A1 | **Conectores de acesso continuam rentes à borda** (§5). Para montagem na JLC, que exige corpo a ≥ 2,5 mm da borda: placa com **rails/painel**, porque a borda que a máquina vê é a do rail. **Antes de cada pedido**, confirmar com a JLC como ela trata conector que ultrapassa a borda; se não aceitar, esses conectores vão para solda manual. [01, 06] |
| A2 | Placa com algum lado < 70 mm: **painel ou rails no PCBA Standard**, ou PCBA Economic com todas as peças num lado só (≥ 0402). [01, 10] |
| A3 | **~18 mm entre SMA vale só entre bandas diferentes.** Antenas da mesma banda ficam no máximo de afastamento possível ao longo da borda, e a coexistência se resolve também no firmware (tempo, canal, potência). [03] |
| A4 | Linha de RF: **CPWG sobre GND sólido em L2** (o §3, que diz "microstrip", fica corrigido). Larguras da calculadora oficial JLC no §17-A11. [03] |
| A5 | Ferrite + LC por rádio, **com**: ferrite a ≤ 20 % da corrente nominal, amortecimento (ex.: 1 µF + 2 Ω), frequência de ressonância longe de f_sw, f_sw/f_corte ≥ 5 e jumper para PWM forçado. GNSS: ≤ 0,2 Ω em série no VCC. Opção registrada: buck-boost ajustado um pouco acima de 3,3 V + LDO só no GNSS/sub-GHz, respeitando o limite de 3,6 V do ESP32. [02, 13] |
| A5b | Energia: **mínimo de 0,76 mm** no tronco do +3V3 (Espressif) e largura pela IPC-2152 (Saturn), lembrando que o cobre interno JLC é 0,5 oz. Conferir as larguras **depois** de rotear (`pcb_audit.py`). [02] |
| A6 | Antes do Freerouting, **rotear à mão e travar**: RF 50 Ω, USB 90 Ω, cristal, hot loop do SMPS e troncos de energia. [04] |
| A7 | Ilhas de GND: **várias vias por ilha**, ou remover a ilha. Uma via só é o mínimo, não a meta. [04] |
| A8 | Gate de placement: além de courtyard = 0, a **tabela de espaçamento de montagem da fábrica** (JLC: QFN ≥ 1,0 mm de qualquer peça, QFP–QFP 1,25 mm, BGA 2,0 mm). `spread.py` com GAP coerente com essa tabela. [01] |
| A9 | Sem header de flash solto (§6 continua), mas **com test pads mínimos**: um ponto sondável por rail e por sinal crítico. Para SWD, Tag-Connect TC2030-NL. [01, 05] |
| A10 | Auto-boot: MCU com USB nativo (ESP32-C3/C5/S3) **dispensa os 2 MOSFETs**; o circuito só entra atrás de ponte USB-UART ou com flash pela UART de um host. O botão BOOT continua. [05] |
| A11 | **Stackup padrão de 4 camadas: JLC04161H-7628, SIG / GND / GND / SIG**, com energia por pour e trilhas largas em L1/L4. O 7628 dá trilha de 50 Ω de ≈ 0,31 mm, melhor para pads 0402 e SMA. Usar **3313** (L1 a 0,099 mm de L2, melhor EMC) quando EMC for o fator limitante e a geometria aceitar trilhas de ≈ 0,14–0,15 mm. Valores da calculadora oficial (2026-11-21):<br>• **7628:** CPWG 50 Ω W 0,306 mm com gap 0,20 mm; microstrip 0,359 mm; par 90 Ω W 0,291 / S 0,203 mm.<br>• **3313:** CPWG 50 Ω W 0,142 mm; microstrip 0,151 mm; par 90 Ω W 0,154 / S 0,203 mm. [03, 04] |
| A12 | Cristal "**perto, conforme o datasheet do chip**" (ex.: ESP32-C5 chip-down pede ≥ 2,4 mm do pino), com GND sólido embaixo e nenhuma trilha sob ele. [01] |
| A13 | Desempate de posicionamento: **buck/buck-boost no quadrante da entrada** (§14); **LDOs e filtros locais junto da carga** (§2). [02] |
| A14 | DSN do KiCad 10: leva zonas, keepouts e netclasses; **não** leva `.kicad_dru` nem gap de par diferencial. Depois de importar o SES, **sempre DRC e conferência de larguras** (o erro 20 fica com essa justificativa). [08] |
| A15 | **Via de retorno:** alvo ≤ 1 mm para sinal rápido (t_r ≤ 1,5 ns); limite de 5 mm para qualquer sinal. Par diferencial: 1–2 vias simétricas. Troca GND↔PWR: re-rotear ou capacitor de costura. [12] |
| A16 | **Pinos de GND em conector/cabo:** erro abaixo de 1:9; aviso abaixo de max(2, ⌈S/4⌉); clock e sinais rápidos com GND adjacente (G-S-G), par diferencial em GSSG; cabo flat rápido ou > 30 cm alterna 1:1. [12] |
