# 02 — Energia: SMPS, LDO, desacoplamento, distribuição, bateria LiPo 1S e USB-C

> Corpus de referência para a skill "especialista em PCB" (KiCad 10 + JLCPCB, produtos com RF). Pesquisa feita em 2026-11-20.
> **Etiquetas:** **FATO** = conferido por mim no texto da fonte citada (PDF baixado ou página lida). **INFERÊNCIA** = dedução minha ou prática comum sem fonte primária lida. **SEC** = só vi em fonte secundária ou em resumo de busca, sem ler o original (tratar como "a confirmar").
> PDFs locais em `pdfs\02-energia\` (lista e licenças em `pdfs\02-energia\LICENSES.md`).

---

## Resumo executivo

1. O layout de uma fonte chaveada se resume a **minimizar o laço de alto di/dt (hot loop)**. No buck ele é C_in → chave alta → chave baixa → GND do C_in. No **buck-boost de 4 chaves há DOIS hot loops**: o de entrada (perna buck) e o de saída (perna boost). Com 3–5 A/ns, **2 nH de parasita geram 6 V de pico** (TI SLVAER0). FATO
2. **Ordem de posicionamento (TI SLYT614):** (1) C_in colado em VIN/PGND, sem vias no caminho; (2) indutor + nó SW mínimo; (3) C_out + pino de sensoriamento (VOS/FB); (4) componentes de sinal pequeno; (5) GND em ponto único (EP) e vias para o resto do sistema. FATO
3. **O nó SW deve ser pequeno.** Cobre de SW é uma placa de capacitor parasita que acopla ruído a tudo em volta: não "engordar" o SW por causa do calor. **FB curto, longe do indutor e do SW**, de preferência do outro lado da placa com GND entre eles. Não passar trilhas sob o indutor (Rohm). FATO
4. **O ferrite + capacitor por rádio pode PIORAR o ruído.** Bead + MLCC forma um LC de Q alto. No exemplo da ADI (bead de 100 Ω/0603 + 10 nF), há **pico de +10 dB em ~2,5 MHz**, e o conversor do exemplo chaveia a **2,4 MHz**: a mesma frequência do TPS63020 (buck-boost típico da casa). Saída: amortecer (**1 µF + 2 Ω em série** derivado à carga), usar o bead a **≤20 % da corrente nominal** (a 50 % a indutância cai até 90 %) e checar onde cai a ressonância. FATO
5. **Em modo de economia (PFM/PSM) a frequência de chaveamento cai** e pode ficar abaixo do corte do LC. O LDO filtra melhor nesse regime (TI SNVA871). Para placas com GNSS/receptores sensíveis, avaliar **PWM forçado** (TPS63020: PS/SYNC = alto). FATO + INFERÊNCIA
6. **LDO:** P = (Vin − Vout)·Io; a eficiência é ≈ Vout/Vin. Um LDO 3,3→3,3 V não regula (precisa de headroom maior que o dropout). O PSRR cai com a frequência: datasheets que só dão PSRR a 1 kHz não servem para pós-regular SMPS. FATO
7. **Desacoplamento:** a indutância de montagem (pad + trilha + via + distância até o plano) domina; com o plano a 10 mil vs 20 mil, um 0603 cai de 2,3 nH para 1,1 nH. Trilha até a via soma ~1 nH a cada 100 mil. **MLCC X5R/X7R perde capacitância com tensão DC**: dimensionar pela capacitância efetiva (Murata SimSurfing). FATO
8. **Largura de trilha:** as fontes divergem (0,38 mm/A em TI SNVA021, 1 mm/A a 1 oz em Rohm; ESP32-C5 pede ≥30 mil no 3V3 principal). Use a calculadora IPC-2152. **Na JLC, cobre interno de 4 camadas é 0,5 oz por padrão**: quem passar potência no interno precisa de trilhas mais largas ou pedir 1 oz. FATO
9. **Vias térmicas no EP:** furo ≤0,33 mm, sem thermal relief (conexão sólida), tentadas do lado do componente se não forem preenchidas (TI SLMA002); Rohm usa 0,3 mm em passo de 1,2 mm; ESP32-C5 pede ≥9 vias no pad. Na JLC, preenchimento epóxi + capa (POFV) é padrão/gratuito só a partir de 6 camadas. FATO
10. **Cadeia LiPo 1S:** carregador com power-path (ex.: BQ24074 = **linear**, P = (Vin−Vout)(Iout+Ibat) + (Vout−Vbat)·Ibat → esquenta; OVP 10,5 V; entrada tolera 28 V), NTC 10 k (103AT) no pack, proteção de célula (BQ2970/DW01 + FETs), proteção contra inversão (PMOS/ideal diode), USB-C sink com **Rd 5,1 kΩ independente em CC1 e CC2** e TVS/ESD na entrada (ESP32-C5 guide). FATO / SEC (Rd)

---

## Regras acionáveis

### A. Layout de conversor chaveado (buck, boost, buck-boost)

**A1. Identifique o(s) hot loop(s) ANTES de posicionar.**
- Buck: C_in ↔ chave alta ↔ chave baixa. Boost: chave baixa ↔ retificador ↔ C_out de alta frequência. Buck-boost de 4 chaves: **loop 1 (perna buck, com C_in)** e **loop 2 (perna boost, com C_out)**.
- **Por quê:** com di/dt de 3–5 A/ns, 2 nH de parasita = 6 V de spike. A corrente pulsada rica em harmônicos irradia proporcionalmente à área do laço. — FATO, TI SLVAER0 §2.1 https://www.ti.com/lit/pdf/slvaer0
- A indutância parasita **em série com o indutor principal é benigna**, porque a corrente ali é quase DC. — FATO, SLVAER0 §2.1

**A2. O capacitor de entrada é o componente mais importante: posicionar primeiro, logo depois do CI.**
- Rotear C_in a VIN/PGND **imediatamente**, com polígonos curtos e largos e **sem vias** entre C_in e o CI. As vias para o sistema ficam "fora" do circuito, não entre C_in e o CI. — FATO, TI SLYT614 passos 1, 3 e 5 https://www.ti.com/lit/an/slyt614/slyt614.pdf
- Ponha um MLCC pequeno (C_BYPASS) em paralelo ao C_in maior. **Não coloque o C_BYPASS no lado de baixo através de vias**: a indutância da via anula o efeito ("operates as a reverse effect"). Encurtar a ligação "mesmo que 1 mm" já ajuda. — FATO, Rohm 60AN066E §3 https://fscdn.rohm.com/en/products/databook/applinote/ic/power/switching_regulator/converter_pcb_layout_appli-e.pdf
- TPS63020: **10 µF X5R/X7R** em VIN–PGND, o mais perto possível; **3×22 µF** na saída; **0,1 µF** (máx. 0,22 µF) em VINA. Se a fonte estiver a "alguns polegadas", acrescente bulk de ~47 µF. — FATO, TPS63020 datasheet §8.2.2 https://www.ti.com/lit/ds/symlink/tps63020.pdf
- **Por quê:** a indutância entre C_in e o CI gera spikes (V = L·di/dt) que podem destruir o CI. — FATO, SLYT614

**A3. Nó de chaveamento (SW) mínimo.**
- O indutor fica perto do CI, mas não precisa estar tão perto quanto o C_in. Gire o indutor para encurtar o SW. **Não amplie o cobre do SW** por causa do calor: o cobre do SW é uma placa de capacitor parasita que acopla ruído e funciona como antena. — FATO, SLYT614 passo 2; Rohm §5; SLVAER0 §2.2 ("large SW copper helps thermal but causes severe radiated emissions")
- Snubber RC (se houver) com o laço mais curto possível entre SW e PGND. — FATO, SLYT614; Rohm fig. 3-g
- Em WCSP com SW entre VIN e PGND: passe o SW **por baixo do C_in** (trilha fina e curta) ou use via no SW, mas **nunca afaste o C_in**. Via no ramo SW→indutor é aceitável, porque fica em série com a indutância principal. — FATO, SLYT614 "Special considerations"

**A4. Nada sob o indutor; terminais do indutor afastados.**
- Rohm recomenda **não passar GND nem sinal diretamente sob o indutor**: correntes parasitas (eddy) reduzem L e o Q, e o ruído se propaga para as trilhas. Se for inevitável, use indutor blindado (circuito magnético fechado). Os terminais muito próximos acoplam o SW à saída pela capacitância parasita. — FATO, Rohm §5, figs. 6-c/6-d
- Prefira indutor blindado (ferrite fechado). Núcleo aberto ("stick") é o que mais emite. — FATO, TI SNVA021 §1 https://www.ti.com/lit/an/snva021c/snva021c.pdf
- *Nuance:* TI e ADI pedem um plano de GND contínuo na camada adjacente (ver A7). Com indutor blindado, manter o plano em L2 é a prática dominante; a recomendação de Rohm vale sobretudo para indutor sem blindagem. — INFERÊNCIA

**A5. Realimentação (FB/VOS) tipo Kelvin, longe do ruído.**
- Divisor FB **colado ao pino FB/AGND do CI**, nó FB o menor possível. Tome a tensão **depois do C_out** (ou nos terminais dele). Trilha longe do SW e do indutor, nunca sob ou paralela a eles. De preferência roteie no **lado oposto** ao indutor, com plano de GND entre os dois. — FATO, SNVA021 §2; Rohm §7 (a)–(d); SLYT614 passos 3–4; TPS63020 §10.1
- Trilha VOS curta e dedicada até o C_out; isolar as vias dela de outras redes. — FATO, SLYT614 passo 3

**A6. AGND/PGND: um único ponto de união.**
- Separe o "GND de potência" (C_in, C_out, PGND) do "GND quieto" (divisor FB, soft-start, compensação) e **una-os em um único ponto**, tipicamente no EP sob o CI, que também vai a GND. Não espalhe vias de GND do sistema nos componentes quietos: eles voltam ao pino AGND. — FATO, SLYT614 passo 5; TPS63020 §10.1; SLVAER0 §2.4 (net-tie em ponto único perto do GND do capacitor de VCC)
- Rohm: GND de C_in e de C_out a **1–2 cm** um do outro, porque o GND de entrada carrega ruído de "várias centenas de MHz". — FATO, Rohm §6
- *Em 4 camadas com plano de GND sólido* (padrão da casa), a "separação" é feita **pelo posicionamento e pelo caminho das correntes** no topo, não cortando o plano. — INFERÊNCIA (consistente com SLYT614 e SLVAER0)

**A7. Plano de GND adjacente e escudo.**
- Plano de GND dos dois lados / em camada interna separando a "camada de potência" da camada de sinais (FB, compensação). — FATO, SNVA021 §5
- Evite rotear sinais sensíveis sob a fonte. Se não der, ponha um plano de GND interno entre a camada da fonte e a de sinais. — SEC (AN-136, ADI; PDF não baixado) https://www.analog.com/en/resources/app-notes/an-136.html
- AN-139: plano sólido na camada adjacente reduz bastante a indutância do hot loop (">3× vs. 2 camadas de 1,5 mm; >14× vs. 1 camada"). — SEC (resumo de busca; PDF não lido) https://www.analog.com/en/resources/app-notes/an-139.html

**A8. Laços de corrente "girando no mesmo sentido".**
- Arranje os componentes para que os laços de corrente dos dois estados (chave ligada/desligada) circulem no mesmo sentido: isso evita inversão de campo e reduz a EMI irradiada. — FATO, SNVA021 §5

**A9. Buck-boost de 4 chaves: os dois loops + gate drive.**
- C_in junto à perna buck e C_out junto a VOUT/PGND do CI. Indutor entre as duas pernas, SW1 e SW2 pequenos. Capacitor de VCC e bootstrap colados (picos de ~1 A no laço de gate). Trilhas de gate e de retorno lado a lado. Sensores de corrente em par diferencial. — FATO, SLVAER0 §2.1–2.3
- Com controlador de 4 chaves, comparar um "single hot loop" com um "dual hot loop": a ADI mediu resultados quase iguais, com um pico 5 dBµV/m maior em ~90 MHz no dual. — SEC https://www.analog.com/en/analog-dialogue/articles/4-switch-buck-boost-controller-layout-for-low-emissions-single-hot-loop-vs-dual-hot-loop.html

**A10. Copie o layout do EVM/datasheet sempre que puder.** É a opção de menor risco. — FATO, SLYT614 introdução

**A11. Modo de operação e EMI em placas com rádio.**
- TPS63020: **2,4 MHz fixos em PWM**. O power save é selecionado pelo pino PS/SYNC (baixo = power save habilitado). Também aceita sincronização externa. — FATO, TPS63020 §7.4.4
- Em PSM a frequência "dobra para baixo" com a carga. O LC de pós-filtro, com corte em ~10 kHz no exemplo, deixa passar ou amplifica o ruído abaixo do corte. **O LDO é a melhor alternativa como pós-filtro quando se quer PSM.** — FATO, TI SNVA871 §3.1 https://www.ti.com/lit/pdf/snva871
- Recomendação: em placas com GNSS ou receptor sub-GHz sensível, **prever um jumper/GPIO em PS/SYNC** para testar PWM forçado vs PSM na bancada. — INFERÊNCIA

### B. LDO

**B1. Dissipação e eficiência.** P_LDO = (Vin − Vout)·Io; eficiência ≈ Io·Vo / [(Io+Iq)·Vi]. Exemplo TI: um LDO de 3,3 V com Vin de 4–4,5 V dá ≥73 %; com 3,6–4 V, 82,5 %. — FATO, TI SLVA079 §4 https://www.ti.com/lit/an/slva079a/slva079a.pdf

**B2. Dropout.** O LDO para de regular quando Vin − Vout < Vdo (ex.: TPS76733 ≈ 350 mV a 1 A). Logo, **um LDO 3,3 V alimentado por um rail de 3,3 V não regula**: só repassa o rail menos a queda. — FATO (definição, SLVA079 §1) + INFERÊNCIA (aplicação)

**B3. PSRR depende da frequência.** O PSRR costuma ser especificado entre 10 Hz e 1 MHz. Historicamente o LDO é fraco em alta frequência; há peças com >40 dB a 5 MHz. A curva tem 3 regiões: referência/filtro interno, ganho de malha aberta e parasitas + C_out. Aumentar headroom e C_out melhora o PSRR em alta frequência. — FATO (SNVA871 §3.2; TI SLAA414 https://www.ti.com/lit/pdf/slaa414 para "10 Hz–1 MHz" e ">40 dB a 5 MHz")

**B4. Quando LDO e quando buck/buck-boost.** — INFERÊNCIA, com base em B1–B3:
- **LDO:** Vin − Vout pequeno e corrente baixa (P < ~0,3–0,5 W num SOT-23-5/DFN sem cobre generoso); rail analógico ou de RF que precisa de PSRR alto; pós-regulação de SMPS (o ganho medido pela TI foi de ~12 dB no LDO e ~21 dB no total com LC parasita, SNVA871 §4.1 FATO).
- **Buck/buck-boost:** diferença de tensão grande ou corrente alta; bateria cuja faixa cruza a saída (LiPo 4,2→3,0 V com saída de 3,3 V → buck-boost).
- **LC vs LDO como pós-filtro:** o LC não perde headroom, mas ressoa (precisa de amortecimento) e não filtra em PSM. O LDO custa headroom e eficiência, mas filtra em PSM.

**B5. Capacitores do LDO.** Use o valor e a faixa de ESR do datasheet. O ESR do C_out influencia o transiente (SLVA079 §5). LDOs "cap-free/any-cap" dispensam ESR mínimo. — FATO (dependência do ESR, SLVA079) / INFERÊNCIA (generalização)

### C. Desacoplamento (decoupling) e PDN

**C1. A indutância de montagem domina, não o valor nominal.** Tabela de Archambeault (indutância de conexão; as linhas indicam a distância pad→via):

| Montagem | plano a 20 mil | plano a 10 mil |
|---|---|---|
| 0603 + 2×10 mil | 2,3 nH | 1,1 nH |
| 0603 + 2×100 mil | 3,3 nH | 2,1 nH |
| 0805 + 2×10 mil | 3,0 nH | 2,0 nH |
| 0805 + 2×160 mil | 5,1 nH | 3,5 nH |

— FATO, tabela "Typical connection decoupling capacitor inductance values" (PCD&F, B. Archambeault) https://www.pcdandf.com/pcdesign/images/stories/mag/0704/0704emc_table1.pdf
- Consequências: (a) **via colada ao pad** (≤10 mil de trilha); (b) **plano próximo**: no stackup JLC de 4 camadas, L1→L2 é um prepreg fino (confirmar a espessura na calculadora JLC), o que favorece GND em L2; (c) trocar 0805 por 0603 rende menos que encurtar trilha e aproximar o plano. — INFERÊNCIA a partir do FATO acima
- Exemplos medidos na LearnEMC: de **0,61 nH** (melhor caso) a **15,7 nH** com 1" de trilha (a trilha soma ~15 nH). — FATO https://learnemc.com/estimating-connection-inductance
- **0402 vs 0603:** não achei tabela primária com números de 0402 nesta pesquisa. Pela tendência da tabela acima, o encapsulamento menor tem laço menor, mas o ganho é secundário diante da via e do plano. — INFERÊNCIA; dado primário "não encontrado"

**C2. Ordem cap → pino → via.** O capacitor fica entre o pino e a via, ou com a via **no pad do capacitor**, sem trilha longa até o pino do CI. A ESP32-C5 pede vias de GND junto ao pad de GND do capacitor ("short return path"). — FATO (ESP32-C5 HW guide §1.4.2 https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c5/esp-hardware-design-guidelines-en-master-esp32c5.pdf) / INFERÊNCIA (generalização)

**C3. Valores típicos (exemplo ESP32-C5).** 10 µF na entrada principal de 3V3, junto com o diodo ESD; 1 µF em VDDPST1; 0,1 µF em VDDPST2/3; 10 µF em cada VDDA1/2/6/7 (pinos 1, 3, 40, 41) mais um capacitor extra nos pinos 1 e 3; **LC (CLC) em VDDA1/VDDA2 com indutor ≥500 mA**; componentes 0201 no filtro dos pinos 40/41. Fonte de 3,3 V com **≥600 mA** por chip. — FATO, ESP32-C5 HW guide §1.3.2 e §1.4.2

**C4. DC bias de MLCC X5R/X7R.** Dielétricos de alta constante (ferroelétricos de BaTiO₃) perdem capacitância com DC; o C0G praticamente não. Exemplo Murata: 100 µF/6,3 V X5R com 1,8 V DC → ~90 µF (−10 %); Y5V → −40 %. Medir/estimar **na tensão real do rail**. — FATO, Murata https://article.murata.com/article/voltage-characteristics-of-electrostatic-capacitance e FAQ https://www.murata.com/en-us/support/faqs/products/capacitor/mlcc/char/0005
- A perda cresce com a razão V_aplicada/V_nominal e com encapsulamentos pequenos de capacitância alta (ex.: 10 µF 0402 a 3,3 V pode cair bem mais da metade). — SEC/INFERÊNCIA (Nordic e Altium em busca; números de cada peça **só pela curva do fabricante**: Murata SimSurfing https://ds.murata.com/simsurfing/, TDK product center)
- A TI aumentou a capacitância dos filtros LC na bancada "em consideração ao derating a 3,3 V". — FATO, SNVA871 §4.1
- Regra prática: para rail de 3,3 V, use MLCC de **≥6,3 V (de preferência 10 V)** e **0603 para ≥10 µF**, e confira a capacitância efetiva. — INFERÊNCIA

**C5. Anti-ressonância ao paralelar valores diferentes (100 nF ‖ 1 µF ‖ 10 µF).** Entre as ressonâncias série de dois capacitores diferentes há um pico de impedância (anti-ressonância paralela). O pico cresce com ESR baixo e valores muito espaçados. ESR maior ou mais capacitores do mesmo valor achatam o pico. — SEC (Signal Integrity Journal https://www.signalintegrityjournal.com/articles/671-capacitor-coupling-for-minimum-impedance; Altium; não achei nota primária Murata/TDK/Novak lida). Para decisões: simule com modelos S-param/SPICE do fabricante (SimSurfing). — INFERÊNCIA

**C6. Capacitor perto da carga + bulk perto da entrada.** Se o capacitor grande não couber perto do CI, ponha um MLCC pequeno em paralelo colado aos pinos (TPS63020 §8.2.2.3). — FATO

### D. Distribuição de energia (planos, trilhas, vias, cobre)

**D1. Planos vs trilhas.** Em 4 camadas, rail de potência em polígono/plano (L3) ou trilhas largas cercadas de GND. A ESP32-C5 recomenda **4 camadas**, power nas internas (não na camada de GND), **≥2 vias** ao trocar de camada, trilha principal **≥30 mil (0,76 mm)**, VDDA de RF **≥20 mil**, demais **10 mil**, topologia **em estrela** a partir do 10 µF, e **separar os ramos de 2,4 GHz e 5 GHz**. — FATO, ESP32-C5 HW guide §1.4.2

**D2. Largura por corrente: as fontes divergem; use a calculadora IPC-2152.**
- TI SNVA021: **mínimo absoluto de 15 mil (0,381 mm) por ampère** "em placa padrão". — FATO
- Rohm: **1 mm/A em 1 oz (35 µm), 0,7 mm/A em 2 oz (70 µm)** com margem; 2 A em 35 µm com 0,53 mm → ΔT ≈ 20 °C. — FATO, Rohm §5
- Norma: **IPC-2152** (2009), que dimensiona condutores internos e externos por corrente e ΔT; ela mesma incentiva simulação. Não reproduzir tabelas: citar e usar calculadora. — FATO (sumário oficial https://www.ipc.org/TOC/IPC-2152.pdf); calculadora Saturn PCB Toolkit https://saturnpcb.com/saturn-pcb-toolkit/ (há relatos não verificados de divergência com os gráficos da norma, SEC)
- **JLC:** cobre **externo** multicamada 1 oz ou 2 oz; **interno 0,5 oz por padrão** (opções 1 e 2 oz). Trilha/espaço mínimos de 0,09/0,09 mm em 1 oz e 0,15/0,15 mm em 2 oz (multicamada). — FATO https://jlcpcb.com/capabilities/pcb-capabilities
- → A corrente em trilha **interna de 0,5 oz** exige ~2× a largura da externa de 1 oz para a mesma resistência, e a interna dissipa pior. — INFERÊNCIA (a resistência escala com a espessura; ΔT pela IPC-2152)

**D3. Vias por corrente: TI contradiz a si mesma; use calculadora.**
- TI SNVA021 (1999/2013): **1 via padrão a cada 200 mA**. — FATO
- TI SLYT614 (2015): **1 via por ampère, "mais é melhor se couber"**. — FATO
- A diferença vem de critérios distintos (queda/aquecimento vs indutância) e de "via padrão" não definida. Dimensione pela calculadora IPC-2152/Saturn com o furo e o plating reais (JLC: furo mínimo multicamada 0,15 mm / via 0,25 mm; furo preferido ≥0,2 mm). — INFERÊNCIA + FATO (JLC)

**D4. Queda de tensão.** Calcule R = ρ·L/(w·t) (cobre ρ ≈ 1,7×10⁻⁸ Ω·m; 1 oz ≈ 35 µm): uma trilha de 0,5 mm × 50 mm em 1 oz ≈ 49 mΩ → 49 mV/A. Em rail de 3,3 V com picos de TX de 2 rádios, isso pesa: alargue ou use plano. — INFERÊNCIA (física básica)
- **GNSS u-blox MAX-M10S:** "não adicionar resistência série **> 0,2 Ω**" na linha VCC/V_IO (ripple sob corrente dinâmica). — FATO, MAX-M10S Integration Manual UBX-20053088 **R01** §3.1 https://cdn.sparkfun.com/assets/5/c/a/0/b/MAX-M10S_IntegrationManual_UBX-20053088.pdf (revisão mais nova R04: https://www.mouser.lt/pdfDocs/MAX-M10S_IntegrationManual_UBX-20053088-2.pdf, não lida). **Isso inclui o RDC de qualquer ferrite/indutor série.**
- O MAX-M10S já alimenta o domínio de RF **por um ferrite interno**. — FATO, mesmo manual §3.1.1

### E. Filtros ferrite + capacitor por rail de rádio

**E1. Modelo e saturação.** O bead é R_DC + L_BEAD ‖ R_AC ‖ C_PAR. A corrente DC satura o núcleo: **a 50 % da corrente nominal, L cai até 90 %**; a 20 %, L fica em ~30 % (bead de 6 A) ou ~15 % (bead de 3 A). Ex.: TDK MPZ1608S101A, |Z|@100 MHz cai de 100 Ω para 10 Ω a 50 % de I_nom. **Operar a ~20 % da nominal**; a corrente nominal é limite térmico, não ponto de filtragem. — FATO, A. Limjoco (ADI) "Ferrite Beads Demystified" https://www.allaboutcircuits.com/industry-articles/ferrite-beads-demystified/ (republicação do Analog Dialogue/AN-1368 https://www.analog.com/en/resources/app-notes/an-1368.html)
- Ex.: ESP32-C5 com pico de TX de ~0,5 A num rail com bead → bead de **≥2,5 A** nominal para ficar em ~20 %. — INFERÊNCIA a partir do FATO

**E2. Ressonância: quando o ferrite piora.** Bead + MLCC de Q alto = LC subamortecido. Exemplo: MPZ1608S101A + 10 nF X7R → **pico de ~+10 dB em ~2,5 MHz**; o regulador do exemplo chaveava a **2,4 MHz**, então a fundamental é **amplificada**. Filtros não amortecidos chegam a 10–15 dB de pico, pior em carga leve. — FATO, Limjoco/ADI

**E3. Amortecimento.** (A) R série no capacitor: degrada o desacoplamento de alta frequência (pouco prático). (B) R em paralelo com o bead (10 Ω): baixa o crossover de 40,3 MHz para 3,8 MHz e perde atenuação de alta frequência. (C) **C_damp grande + R_damp em série, derivados à carga: 1 µF + 2 Ω reduziu a fundamental de 2,4 MHz em 5 dB**, "often an optimal solution". — FATO, Limjoco/ADI
- Para LC de pós-filtro com indutor: R de amortecimento **em paralelo com o indutor de 100–500 mΩ** (TI). Verifique a SRF do indutor: acima dela ele vira capacitor. — FATO, SNVA871 §3.1
- Filtro de entrada de SMPS (Middlebrook): ressonância **≥1 década abaixo de f_sw**; C_d ≥ 4·C_IN com ESR_d ≈ √(L_f/C_IN) para não desestabilizar o conversor. — FATO, TI SNVA489 §4.3–4.4 https://www.ti.com/lit/an/snva489c/snva489c.pdf

**E4. Procedimento por rail de rádio.** — INFERÊNCIA consolidada de E1–E3:
1. Comece pela rede do fabricante do rádio (ESP32-C5: LC/CLC em VDDA1/2; MAX-M10S: ferrite interno + ≤0,2 Ω série).
2. Escolha bead/indutor com corrente nominal ≥5× o pico DC e RDC compatível com a queda admissível.
3. Calcule f₀ = 1/(2π√(L·C)) com L **na corrente de operação** e C **efetiva** (DC bias). Se f₀ cair perto de f_sw (2,4 MHz) ou de suas harmônicas baixas, mude L/C ou amorteça (1 µF + ~1–2 Ω).
4. Meça na bancada com ponta de 1× / pigtail (SNVA871 §3.3), não com garra jacaré.

**E5. Bead de alta frequência e picos de corrente.** A Würth tem notas específicas (ANP045 sobre beads de alta frequência e DC bias; ANP041 sobre filtro de entrada à prova de pico com WE-MPSB; ANP025 sobre ringing). — SEC (existem segundo a busca; o servidor devolveu 403 ao robô) https://www.we-online.com/components/media/o190203v410%20ANP045b_Behind%20the%20Magic%20of%20High%20Frequency%20SMT%20Chip%20Bead%20Ferrites.pdf

### F. Bateria LiPo 1S, carregador, proteção, USB-C

**F1. Carregador com power-path (ex.: TI BQ24074).**
- Linear, 1 célula, até **1,5 A**; **DPPM**: alimenta o sistema e carrega a bateria de forma independente, permitindo terminar a carga corretamente e operar com bateria ausente ou defeituosa. Entrada de **28 V** sem dano; **OVP do BQ24074 = 10,5 V** (os outros membros da família: 6,6 V); **VOUT(REG) = 4,4 V**. — FATO, BQ2407x datasheet SLUS810N https://www.ti.com/lit/ds/symlink/bq24074.pdf
- **Dissipação (linear!):** P = (V_IN − V_OUT)·(I_OUT + I_BAT) + (V_OUT − V_BAT)·I_BAT. O pior caso é no início da carga (V_BAT baixa; a TI sugere 3,4 V como mínimo realista). Ex.: 5 V, 1 A de carga + 0,3 A de sistema, V_BAT = 3,4 V → (5−4,4)·1,3 + (4,4−3,4)·1 ≈ **1,8 W**: precisa de cobre e vias térmicas, ou de corrente de carga menor. — FATO (equação 11) + INFERÊNCIA (exemplo numérico)
- Layout: C de IN→GND e de OUT→GND colados ao CI; GND de sinal separado dos caminhos de alta corrente, em ponto único; trilhas IN/OUT dimensionadas para a corrente máxima; **EP soldado ao GND** (é a conexão térmica principal). — FATO, SLUS810N §12.1
- **NTC:** 10 kΩ (103AT) **no pack da bateria**, entrada TS. Janela de 0–50 °C com histerese de 3 °C. Sem NTC: resistor fixo de 10 kΩ em TS (desliga a proteção térmica da célula, então evite em produto). — FATO, SLUS810N (pinos/TS)

**F2. Proteção da célula (PCM).** Um CI de proteção 1S (ex.: TI BQ2970) faz OVP de sobrecarga, UVP de sobredescarga, OCC/OCD e curto, acionando FETs de CHG/DSG externos. Prefira **célula com PCM integrado** (exigência do PADROES §7). — FATO (funções, BQ2970 datasheet https://www.ti.com/lit/ds/symlink/bq2970.pdf) / casa

**F3. Inversão de polaridade da bateria.** Diodo série (simples, mas perde Vf; Schottky menos). **FET:** NMOS no retorno de GND ou **PMOS no caminho positivo**, com o diodo de corpo no sentido normal; queda = R_DS(on)·I. — FATO, TI SLVA139 https://www.ti.com/lit/pdf/slva139
- O PMOS "simples" não bloqueia corrente reversa (ex.: back-feed). Para isso, use controlador de diodo ideal. — FATO, TI SLVAE57 https://www.ti.com/lit/pdf/slvae57
- Com conector JST polarizado e célula com PCM, o PMOS ainda é barato e recomendado, porque cabos JST de terceiros vêm com polaridade invertida com frequência. — INFERÊNCIA (prática comum)

**F4. USB-C sink (UFP).**
- **Rd = 5,1 kΩ em CC1 E em CC2**, cada um com seu resistor (a orientação do cabo é desconhecida). — SEC (resumo de busca de Infineon/TI/ST; especificação USB-IF não lida) https://www.usb.org/document-library/usb-type-cr-cable-and-connector-specification-release-24 ; confirma o PADROES §14
- **ESD na entrada de energia + ≥10 µF**, com o diodo ESD **junto ao conector**. — FATO, ESP32-C5 HW guide §1.3.2 e §1.4.2
- **Sobretensão em VBUS:** fontes não conformes podem aplicar até 20 V sem negociação. A TI protege com uma chave OVP (TPD1S514) antes do CI de 5 V. — FATO, TI SLVAE35 https://www.ti.com/lit/pdf/slvae35. Para um sink só de 5 V com BQ24074 (entrada até 28 V, OVP 10,5 V), o próprio carregador aguenta. Se o VBUS também alimentar outra coisa diretamente (hub, 5 V do header), precisa de OVP/TVS próprio. — INFERÊNCIA
- TVS de VBUS deve ser do tipo **tolerante a DC em alta tensão**; escolha pela tensão de clamp após o transiente. — SEC (busca em documentos TI)

**F5. eFuse/load switch.** Load switch: liga/desliga o rail, com controle de inrush (pino CT: rampa linear) e sequenciamento. eFuse: acrescenta limite de corrente, OVP e bloqueio reverso. Útil para desligar rádios e o GNSS em modo de baixo consumo e para limitar o inrush de bancos grandes de MLCC. — FATO, TI SLVA927 https://www.ti.com/lit/pdf/slva927 ; SLVA652 https://www.ti.com/lit/pdf/slva652 (não lido em detalhe)

**F6. Posição da bateria e do carregador na placa.** Carregador/power-path, buck-boost, indutor e conector da bateria no mesmo quadrante do USB-C (PADROES §14), com trilhas VBUS/VSYS/VBAT curtas. NTC no pack ou, se a célula não tiver, termistor encostado na célula, e não no carregador (que esquenta sozinho). — INFERÊNCIA

### G. Térmico de reguladores

**G1. θJA não é constante.** θJA é medido numa placa de teste JEDEC (1s/2s2p). Entre 1s e 2s2p a variação chega a **50 %**. Usar θJA para prever Tj na sua placa é "má aplicação". Use Ψ_JT com a temperatura medida no topo do CI ou simulação. — FATO, TI SPRA953 https://www.ti.com/lit/an/spra953c/spra953c.pdf

**G2. Vias térmicas no exposed pad (EP).**
- Furo **≤0,33 mm (13 mil)** com 1 oz de plating; o retorno satura: para die pequeno, **5–9 vias** bastam. **Sem thermal relief** (raios) nas vias do pad: conexão sólida ao plano. Se a via não for preenchida, faça **tenting do lado do componente** com diâmetro de via + 0,1 mm; tenting do lado oposto aumenta voids. — FATO, TI SLMA002 §2.4 https://www.ti.com/lit/an/slma002h/slma002h.pdf
- Rohm (HTSOP-J8): vias de **0,3 mm de furo**, passo de **~1,2 mm**, sob o pad; vias extras em volta do CI se faltar. Pad em GND → cobre largo não aumenta EMI. — FATO, Rohm §4
- ESP32-C5: pad de GND com **≥9 vias** ao plano. — FATO, ESP32-C5 HW guide §1.4.2
- A JLC preenche via com epóxi + capa (POFV) **por padrão em ≥6 camadas**, para vias de 0,15–0,55 mm. Plugging/tenting só até **0,5 mm**. — FATO, JLC capabilities + via covering https://jlcpcb.com/help/article/pcb-via-covering . Em **4 camadas**, via-in-pad preenchida é opcional/paga, então use vias de **0,2–0,3 mm** abertas no pad (aceitar algum solder wicking) ou tented, e confira o stencil (janelas segmentadas). — INFERÊNCIA (sobre o FATO)

**G3. Área de cobre.** Os três caminhos térmicos (TPS63020 §10.3): melhorar a capacidade da PCB de dissipar, soldar o EP, fluxo de ar. O cobre do pad de GND pode ser grande; **o do SW, não** (A3). — FATO

---

## Erros comuns

| Erro | Consequência | Correção |
|---|---|---|
| C_in longe do CI ou ligado por vias | Spikes em SW, ringing, EMI, CI queimado | C_in colado a VIN/PGND na mesma face, sem vias (SLYT614, Rohm) |
| Esquecer o 2º hot loop do buck-boost (lado da saída) | Ringing em SW2, EMI | C_out colado a VOUT/PGND do CI (SLVAER0) |
| Polígono grande no SW "para dissipar" | Antena: acoplamento capacitivo e emissão irradiada | SW mínimo; dissipar pelo pad de GND (SLVAER0, SLYT614) |
| FB paralelo ao indutor ou sob o SW | Regulação ruim, jitter, instabilidade | FB curto, outra face, GND no meio (SNVA021, Rohm) |
| Trilha/sinal sob o indutor | Ruído induzido; L e Q menores | Keep-out sob indutor ou indutor blindado (Rohm) |
| Bead + 10 nF sem amortecimento num rail de 2,4 MHz | Ripple **amplificado** (~+10 dB) | 1 µF + 2 Ω de damping; checar f₀ (ADI) |
| Bead dimensionado pela corrente nominal | Satura, L cai até 90 %, filtro some | Operar a ≤20 % de I_nom (ADI) |
| Bead/indutor série no VCC do GNSS com RDC alto | Ripple sob corrente dinâmica, perda de sensibilidade | RDC total < 0,2 Ω (u-blox MAX-M10S) |
| MLCC 10 µF 0402 6,3 V em rail de 3,3 V contado como 10 µF | Capacitância real muito menor; instabilidade/ripple | Curva DC bias (SimSurfing); 0603/10 V |
| Capacitor ligado ao pino por trilha longa + via distante | +1 nH a cada ~100 mil; desacoplamento inútil em alta frequência | Via no pad ou colada; plano próximo (Archambeault) |
| Potência em camada interna de 0,5 oz (padrão JLC) com largura de 1 oz | Queda de tensão e aquecimento 2× maiores | Alargar ou pedir 1 oz interno; calcular IPC-2152 |
| Thermal relief nas vias do EP | Rth alta, CI quente | Conexão sólida (SLMA002) |
| Usar θJA do datasheet para "provar" Tj | Erro de até 50 % ou mais | Ψ_JT + medição/simulação (SPRA953) |
| Carregador linear 1,5 A sem cobre | Thermal foldback, carga lenta | Calcular P (eq. 11); cobre + vias; limitar I_chg |
| Um único Rd de 5,1 kΩ ligado aos dois CC (ou só em CC1) | Não carrega em uma das orientações ou com carregadores C-C | Dois Rd independentes |
| Medir ripple com garra jacaré | Ruído superestimado → filtro superdimensionado | Pigtail/ponta 1×, banda adequada (SNVA871) |
| LC de pós-filtro com PSM ligado | Ruído abaixo do corte passa ou é amplificado | PWM forçado ou LDO (SNVA871) |

---

## Checklist

**Conversor chaveado**
- [ ] Hot loop(s) identificado(s) no esquemático (buck-boost = 2 loops)
- [ ] C_in (MLCC) colado em VIN/PGND, mesma face, sem vias no laço
- [ ] C_out colado em VOUT/PGND (buck-boost) ou junto ao indutor (buck)
- [ ] SW com o menor cobre possível; indutor girado para encurtar o SW
- [ ] Sem trilhas sob o indutor; indutor blindado
- [ ] Divisor FB colado ao CI; sensoriamento depois do C_out; FB longe de SW/L, com GND entre eles
- [ ] AGND/PGND unidos em ponto único (EP), conforme o datasheet
- [ ] Layout comparado com o EVM/datasheet do CI
- [ ] Jumper/GPIO em PS/SYNC (ou equivalente) para testar PWM forçado vs PSM
- [ ] Vias de potência fora do laço C_in–CI, quantidade calculada pela corrente

**Filtros por rádio**
- [ ] Rede de alimentação do fabricante do rádio aplicada (ESP32-C5 LC em VDDA1/2 ≥500 mA)
- [ ] Bead/indutor com I_nom ≥5× o pico DC
- [ ] f₀ do LC calculada com L em carga e C efetiva; longe de f_sw e de harmônicas baixas
- [ ] Damping previsto (1 µF + 1–2 Ω) quando f₀ cai perto de f_sw
- [ ] RDC série no VCC do GNSS < 0,2 Ω no total

**Desacoplamento**
- [ ] 1 capacitor por pino de alimentação, via colada ao pad de GND
- [ ] Capacitância efetiva conferida (DC bias) para todos os ≥1 µF
- [ ] GND em L2 logo abaixo dos capacitores críticos

**Distribuição**
- [ ] Larguras pelo IPC-2152 (Saturn) com o cobre REAL de cada camada (JLC interno = 0,5 oz padrão)
- [ ] Main 3V3 ≥0,76 mm (ESP32-C5), ramos em estrela, 2,4 e 5 GHz separados
- [ ] ≥2 vias por troca de camada nos rails principais
- [ ] Larguras conferidas DEPOIS de rotear (PADROES §13 #11)

**Bateria/USB-C**
- [ ] Power-path com P do carregador calculada e cobre térmico
- [ ] NTC 10 k no pack ligado ao TS
- [ ] Célula com PCM; proteção contra inversão (PMOS/ideal diode) no conector
- [ ] Rd 5,1 kΩ independente em CC1 e CC2
- [ ] ESD + ≥10 µF na entrada VBUS, junto ao conector
- [ ] Back-feed do UART para o host protegido (PADROES §7)

**Térmico**
- [ ] EP com vias de 0,2–0,33 mm, sem thermal relief, ≥5–9 vias (ESP: ≥9)
- [ ] Decidido: via aberta / tented do lado do componente / POFV (só grátis em ≥6 camadas)
- [ ] Tj estimada com Ψ_JT ou simulação, não só θJA

---

## Conflitos com PADROES-PROJETO-PCB.md

> Só para o dono decidir. O PADROES **não foi editado**.

| Regra da casa | Veredito | Comentário e fonte |
|---|---|---|
| §7 "Buck-boost p/ 3,3 V" com LiPo 1S | **Confirma** | Faixa de 4,2 a 3,0 V cruza 3,3 V; TPS63020 (1,8–5,5 V, chaves de 4 A) é exemplo típico. FATO, datasheet |
| §7 "Isolamento entre rádios com ferrite + LC por rádio, sem LDO em rail igual" | **Confirma com ressalvas importantes (falta detalhe)** | (1) A ideia de LC por rail de RF é FATO (ESP32-C5 guide). (2) **Risco direto:** bead + MLCC ressoa, e o exemplo da ADI dá +10 dB justamente perto de 2,4 MHz = f_sw do TPS63020 → **acrescentar: bead a ≤20 % de I_nom, damping 1 µF + ~2 Ω, conferir f₀**. (3) Em **PSM** o LC não filtra (SNVA871) → prever PWM forçado em placas com GNSS. (4) No GNSS u-blox, o RDC série total precisa ser < 0,2 Ω (o módulo já tem ferrite interno no RF). (5) A justificativa "LDO não tem headroom 3,3→3,3" é correta (física de dropout). Mas **falta uma opção**: o SNVA871 mostra o LDO como melhor pós-filtro em PSM. Alternativa para o dono avaliar (não recomendação): buck-boost ajustado um pouco acima (ex.: 3,45–3,5 V) + LDO de baixo dropout/alto PSRR só no rail do GNSS/sub-GHz. É marginal porque o ESP32 tem máx. 3,6 V, então só para rails que não alimentam o ESP32. |
| §14 "SMPS num canto inferior, nunca sob CIs de RF" | **Parcialmente confirmado** | A literatura sustenta a física: hot loop e SW pequenos, nada sob o indutor (Rohm), plano de GND entre a fonte e os sinais (SNVA021; AN-136 SEC), indutor/antena perto degradam o RF (ESP32-C5 §1.4.10). **Nenhuma fonte prescreve "canto"**: o que importa é distância e blindagem pelo plano. "Canto inferior" é uma boa heurística da casa, não norma. |
| §2 "Reguladores perto da carga" vs §14 "energia agrupada no quadrante do USB-C" | **Tensão interna (falta regra de desempate)** | Para o buck-boost único de 3V3, §14 prevalece (trilhas de alta corrente curtas). "Perto da carga" vale para LDO/pós-filtro/LC local (SNVA871: LDO perto da carga). Sugestão: explicitar isso no PADROES. INFERÊNCIA |
| §14 "Netclass de energia 0,5–0,8 mm" | **Diverge parcialmente / falta** | Fontes: 0,38 mm/A (SNVA021), 1 mm/A a 1 oz (Rohm), ≥0,76 mm no main 3V3 (ESP32-C5). Para 2× ESP32 com picos de ~1 A, **0,5 mm é pouco pelo critério Rohm**. Calcular pelo IPC-2152. **Ponto cego:** o interno da JLC é **0,5 oz por padrão**, e a ESP32-C5 recomenda potência nas internas → conferir o cobre do JLC04161H-7628 e, se for 0,5 oz, dobrar a largura ou pedir 1 oz. |
| §14 "USB-C sink: dois 5,1 kΩ independentes" | **Confirma** | SEC (resumos de busca; spec USB-IF não lida). |
| §7 "Power-path (BQ2407x / MCP73871)" | **Confirma, com falta** | O DPPM é FATO. **Falta registrar que o BQ2407x é LINEAR** (dissipação de até ~2 W) → cobre/vias térmicas e limite de I_chg. BQ24074: OVP 10,5 V, VOUT(REG) 4,4 V (a entrada do buck-boost nunca passa de ~4,4 V). |
| §7 "Back-feed via UART" | Confirma (fora do escopo detalhado) | Load switch/eFuse com bloqueio reverso também resolve o back-feed de rail (SLVA927). |
| §14 "Desacoplamento colado aos pinos" | **Confirma** | Archambeault, LearnEMC, ESP32-C5. Falta explicitar: via no pad, plano próximo e DC bias. |
| — | **Falta no PADROES** | Vias térmicas no EP (≤0,33 mm, sem relief, ≥9 na ESP), POFV só grátis em ≥6 camadas na JLC; proteção contra inversão da bateria; NTC no pack; ESD + 10 µF no VBUS; regra "θJA ≠ sua placa". |
| — | **Contradição na literatura (não na casa)** | Vias por corrente: TI SNVA021 = 1 via/200 mA; TI SLYT614 = 1 via/A. Não reconciliado. Usar calculadora. |

---

## Bibliografia

### Livros (só citar; não baixar)
- **Steven M. Sandler**, *Power Integrity: Measuring, Optimizing, and Troubleshooting Power Related Parameters in Electronics Systems*, McGraw-Hill, 2014. Medição de PDN/ripple (ponta de 1×, injeção, impedância). INFERÊNCIA (dados bibliográficos de memória; conferir edição)
- **Larry D. Smith & Eric Bogatin**, *Principles of Power Integrity for PDN Design — Simplified*, Prentice Hall, 2017. Indutância de montagem, impedância-alvo, anti-ressonância. (idem)
- **Madhavan Swaminathan & A. Ege Engin**, *Power Integrity Modeling and Design for Semiconductors and Systems*, Prentice Hall, 2007. Modelagem de planos e PDN. (idem)
- **Sanjaya Maniktala**, *Switching Power Supplies A–Z*, 2ª ed., Newnes/Elsevier, 2012. Topologias, layout, EMI e filtros de entrada. (idem)
- **Istvan Novak & Jason R. Miller**, *Frequency-Domain Characterization of Power Distribution Networks*, Artech House, 2007. (idem)

### Normas (só citar)
- **IPC-2152** (2009) — *Standard for Determining Current Carrying Capacity in Printed Board Design*. Sumário: https://www.ipc.org/TOC/IPC-2152.pdf
- **USB Type-C Cable and Connector Specification** (USB-IF), Rd/Rp/CC: https://www.usb.org/document-library/usb-type-cr-cable-and-connector-specification-release-24
- JEDEC JESD51-x (placas de teste térmico), citadas em SPRA953.

### App notes / datasheets (baixados em `pdfs\02-energia\`)
- TI SNVA021C / AN-1149, *Layout Guidelines for Switching Power Supplies* — https://www.ti.com/lit/an/snva021c/snva021c.pdf
- TI SLYT614, C. Glaser, *Five steps to a great PCB layout for a step-down converter* (AAJ 1Q2015) — https://www.ti.com/lit/an/slyt614/slyt614.pdf
- TI SLVAER0C, *TPS55288 Layout Guideline* (buck-boost, 2 hot loops) — https://www.ti.com/lit/pdf/slvaer0
- TI SNVA489C / AN-2162, *Simple Success With Conducted EMI From DC-DC Converters* (filtro de entrada, damping) — https://www.ti.com/lit/an/snva489c/snva489c.pdf
- TI SNVA871, *Output Noise Filtering for DC/DC Power Modules* (LC vs LDO, PSM) — https://www.ti.com/lit/pdf/snva871
- TI SNVA571, S. Maniktala, *Fixing EMI Across the Board* — https://www.ti.com/lit/pdf/snva571 (baixado, não resumido)
- TI SLVA079, *Understanding the Terms and Definitions of LDO Voltage Regulators* — https://www.ti.com/lit/an/slva079a/slva079a.pdf
- TI SLAA414, *LDO PSRR Measurement Simplified* — https://www.ti.com/lit/pdf/slaa414
- TI SLMA002H, *PowerPAD Thermally Enhanced Package* (vias térmicas) — https://www.ti.com/lit/an/slma002h/slma002h.pdf
- TI SPRA953C, *Semiconductor and IC Package Thermal Metrics* — https://www.ti.com/lit/an/spra953c/spra953c.pdf
- TI TPS63020 datasheet (SLVS916I) — https://www.ti.com/lit/ds/symlink/tps63020.pdf
- TI BQ2407x datasheet (SLUS810N) — https://www.ti.com/lit/ds/symlink/bq24074.pdf
- TI BQ297xx datasheet (proteção 1S) — https://www.ti.com/lit/ds/symlink/bq2970.pdf
- TI SLVA139, J. Falin, *Reverse Current/Battery Protection Circuits* — https://www.ti.com/lit/pdf/slva139
- TI SLVAE57, *Basics of Ideal Diodes* — https://www.ti.com/lit/pdf/slvae57
- TI SLVAE35, *24 V-Tolerant USB-C port using TPS25810 and TPD1S514-1* — https://www.ti.com/lit/pdf/slvae35
- TI SLVA927, *Basics of Power Switches* (load switch, eFuse) — https://www.ti.com/lit/pdf/slva927
- ROHM 60AN066E Rev.004, *PCB Layout Techniques of Buck Converter* — https://fscdn.rohm.com/en/products/databook/applinote/ic/power/switching_regulator/converter_pcb_layout_appli-e.pdf
- Espressif, *ESP32-C5 Hardware Design Guidelines* — https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c5/esp-hardware-design-guidelines-en-master-esp32c5.pdf

### App notes NÃO baixadas (citadas)
- ADI AN-136, *PCB Layout Considerations for Non-Isolated Switching Power Supplies* (H. Zhang) — https://www.analog.com/en/resources/app-notes/an-136.html (site da ADI inacessível daqui por timeout; download pelo espelho bloqueado pela política de permissões)
- ADI AN-139, *Power Supply Layout and EMI* (C. Kueck) — https://www.analog.com/en/resources/app-notes/an-139.html
- ADI AN-1368 / Analog Dialogue, *Ferrite Beads Demystified* (A. Limjoco, J. Eco) — https://www.analog.com/en/resources/app-notes/an-1368.html ; conteúdo lido na republicação https://www.allaboutcircuits.com/industry-articles/ferrite-beads-demystified/
- ADI, *4-Switch Buck-Boost Controller Layout for Low Emissions — Single vs Dual Hot Loop* — https://www.analog.com/en/analog-dialogue/articles/4-switch-buck-boost-controller-layout-for-low-emissions-single-hot-loop-vs-dual-hot-loop.html
- ADI, *Layout for Power Designs #1: Hot Loops* — https://www.analog.com/en/resources/technical-articles/layout-for-power-designs-1-hot-loops.html
- TI SLVA652, *Basics of Load Switches* — https://www.ti.com/lit/pdf/slva652
- Würth ANP045b, *Behind the Magic of High Frequency SMT Chip Bead Ferrites* — URL na seção E5 (403 para robô)
- MPS, *Switch Node Layout Considerations for EMC* — https://www.monolithicpower.com/en/switch-node-layout-considerations-for-emc/ (a página exige JavaScript; não lida)
- u-blox MAX-M10S Integration Manual UBX-20053088 R01 — https://cdn.sparkfun.com/assets/5/c/a/0/b/MAX-M10S_IntegrationManual_UBX-20053088.pdf (R04: https://www.mouser.lt/pdfDocs/MAX-M10S_IntegrationManual_UBX-20053088-2.pdf)

### Artigos / tabelas
- B. Archambeault, tabela de indutância de conexão de capacitores (PCD&F 07/2004) — https://www.pcdandf.com/pcdesign/images/stories/mag/0704/0704emc_table1.pdf
- LearnEMC (Clemson), *Estimating the Connection Inductance of a Decoupling Capacitor* — https://learnemc.com/estimating-connection-inductance
- Murata, *Voltage characteristics of electrostatic capacitance* — https://article.murata.com/article/voltage-characteristics-of-electrostatic-capacitance ; FAQ DC bias — https://www.murata.com/en-us/support/faqs/products/capacitor/mlcc/char/0005
- Signal Integrity Journal, *Capacitor Coupling for Minimum Impedance* — https://www.signalintegrityjournal.com/articles/671-capacitor-coupling-for-minimum-impedance

### Ferramentas / calculadoras
- Saturn PCB Toolkit (IPC-2152, vias, queda de tensão) — https://saturnpcb.com/saturn-pcb-toolkit/
- Murata SimSurfing (curvas DC bias, impedância, S-param de MLCC e beads) — https://ds.murata.com/simsurfing/
- TDK product center / SEAT (curvas de MLCC e beads) — https://product.tdk.com/en/design-tools (403 para robô; existe)
- JLCPCB, capabilities (cobre, vias, POFV) — https://jlcpcb.com/capabilities/pcb-capabilities ; via covering — https://jlcpcb.com/help/article/pcb-via-covering ; impedância/stackup — https://jlcpcb.com/pcb-impedance-calculator ; POFV grátis ≥6 camadas — https://jlcpcb.com/blog/Free-Via-in-Pad-on-6-20-Layer-PCBs-with-POFV
- TI WEBENCH / datasheets com "Layout Example" — copiar o EVM sempre que possível (SLYT614).

---

## Lacunas (para próxima rodada)
- **ADI AN-136 / AN-139 / AN-1368 em PDF:** não baixados. O site analog.com deu timeout e o espelho `www-cce.cldnet.analog.com` foi **bloqueado pela política de permissões**. Precisa de autorização do dono ou de download manual. O AN-1368 está coberto como FATO via republicação.
- **Würth ANP045/ANP041/ANP025:** 403 ao robô. Baixar manualmente.
- **Anti-ressonância (Novak/Murata/TDK):** sem fonte primária lida.
- **Indutância de montagem de 0402:** número primário não encontrado.
- **Rd 5,1 kΩ e TVS de VBUS:** texto normativo da USB-IF não lido (só secundárias).
- **Notas de alimentação específicas do nRF24L01+ e do CC1101** (ripple admissível, filtros): ficam para o tema de RF.
- **POFV na JLC:** fontes divergem entre 6–20 e 6–32 camadas (SEC); a página de capabilities diz "≥6 camadas, padrão".
- Livros: dados bibliográficos a conferir (edição/ano) antes de publicar a skill.
