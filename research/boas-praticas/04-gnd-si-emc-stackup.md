# 04 — Aterramento, caminho de retorno, integridade de sinal (SI), EMC e stackup

> Corpus de referência para a skill "especialista em PCB" (KiCad 10 + JLCPCB, produtos com RF vendidos na UE).
> Pesquisa: 2026-11-20. PDFs em `pdfs\04-emc\` (licenças em `pdfs\04-emc\LICENSES.md`).
> **Etiquetas:** **FATO** = conferido na fonte lida (PDF baixado ou página aberta nesta sessão). **INFERÊNCIA** = dedução minha, cálculo meu ou prática comum sem fonte primária lida. **SECUNDÁRIO** = só resumo de busca, blog ou abstract (fonte primária não lida).

---

## Resumo executivo

1. **A corrente de retorno em alta frequência corre no plano logo abaixo da trilha**, porque esse é o caminho de menor indutância, seja o plano de GND ou de alimentação. Fenda, divisão (split) ou troca de camada interrompe esse caminho, aumenta a área do laço, a irradiação e o crosstalk, e altera a impedância. (FATO: Ott, PCB Stack-Up parte 6; TI SLLA414 §3.4–3.5)
2. **Na maioria dos casos, plano de GND único e contínuo, com o layout particionado (analógico | digital | RF | potência) e disciplina de roteamento, ganha do split AGND/DGND.** O split só se justifica se nenhum sinal cruzar a divisão. Se cruzar, faça uma ponte única por onde passam todas as trilhas. (FATO: Ott, "Grounding of Mixed Signal PCBs"; Toradex §6.9)
3. **Ao trocar de camada, ponha uma via de GND colada à via de sinal**: até 200 mil (5 mm) de centro a centro segundo a TI, e quanto mais perto melhor. Se a referência muda entre GND e PWR, ponha um capacitor colado à via de sinal (Ott parte 6, sem valor). A Toradex usa 10 a 100 nF. Para cruzar fenda ou split, Ott pede 1 a 10 nF a menos de 0,1" (2,5 mm) da trilha. (FATO: SLLA414; Ott parte 6; Toradex §6.8)
4. **Stackup de 4 camadas:** a camada de sinal deve ficar colada ao plano. Ott pede menos de 0,010" (0,25 mm) e cita cerca de 10 dB a menos de irradiação com 0,005". Na JLC, o **JLC04161H-7628** tem prepreg de 0,21 mm e o **JLC04161H-3313** tem 0,099 mm. SIG/GND/GND/SIG, com a alimentação roteada como trilha larga, é uma das melhores opções de EMC para placas com um único rail de 3V3. (FATO: Ott partes 1 e 2; jlcpcb.com/impedance)
5. **4 camadas contra 2:** Ott cita como regra prática cerca de 15 dB a menos de irradiação com 4 camadas. A TI (SZZA009) diz que uma placa de 2 camadas bem feita (malha de GND, GND sob a alimentação, ilha de GND sob o MCU) chega a "95% da eficácia". Para RF de 2,4/5 GHz com microstrip de 50 Ω, as 4 camadas resolvem a geometria. Em 2 camadas, a trilha de 50 Ω em 1,6 mm teria cerca de 2,8 mm. (FATO + INFERÊNCIA)
6. **USB 2.0 HS:** 90 Ω diferencial ±15% (TI usa 81–99 Ω), descasamento dentro do par ≤50 mil (TI) ou ≤1,1 mm (Toradex), 0 stubs, 0 test points, ≤4 vias. Os pinos A6/B6 e A7/B7 do USB-C ficam em curto com stub ≤3,5 mm, e o TVS vai junto ao conector, no caminho da trilha. (FATO: SPRAAR7 Tab. A-1; Toradex Tab. 8; TUSB321 §10.1; SLVA680)
7. **ESD (IEC 61000-4-2):** em 8 kV, di/dt ≈ 4×10¹⁰ A/s, e **cada 0,25 nH acrescenta cerca de 10 V** no pino protegido. O TVS vai encostado no conector, ligado ao plano de GND por via curta, sem stub e sem via entre o conector e o TVS. Nenhuma trilha desprotegida passa perto desse trecho. (FATO: TI SLVA680)
8. **Vias de costura (stitching):** espaçamento ≤λ/20 na maior frequência de interesse nas bordas e cercas de RF, e ≤λ/10 no resto. Em FR-4 isso dá cerca de 2,9 mm em 2,45 GHz e **cerca de 1,2 mm em 5,8 GHz** (ESP32-C5 é dual-band). (SECUNDÁRIO para a regra; INFERÊNCIA para o cálculo)
9. **A regra 20H é controversa.** Hubing/LearnEMC dizem que ela pode piorar a irradiação, e Montrose (IEEE T-EMC 2005) diz que ajuda só em casos específicos. A regra 3W também é contestada: o crosstalk depende da relação espaçamento/altura até o plano, não da largura da trilha. (FATO: LearnEMC; SECUNDÁRIO: Montrose)
10. **Cristal:** colado ao pino (≤12 mm segundo a Microchip), com GND contínuo na camada adjacente, anel de guarda aterrado com várias vias, guarda entre XI e XO, e nenhuma trilha embaixo nem dentro do pour. A Arrow recomenda o contrário (sem GND sob o cristal), por causa da capacitância parasita. Siga o datasheet do chip. (FATO: Microchip dsPIC33AK §2.6; TI AM67 §8.3.1; SECUNDÁRIO: Arrow)
11. **JLC:** via mínima de 0,15/0,25 mm. Fica mais cara com furo de 0,15 mm, ou com furo de 0,2–0,25 mm e anel abaixo de 0,45 mm. O controle de impedância tem tolerância padrão de ±10%. Back-drill existe a partir de 4 camadas e 0,8 mm de espessura. (FATO: jlcpcb.com/capabilities) Daí, via econômica = **0,3/0,5–0,6 mm** ou **0,2/≥0,45 mm**. (INFERÊNCIA)

---

## Regras acionáveis

### A. Aterramento e caminho de retorno

**A1. Use um plano de GND único e contínuo. Particione a placa por função em vez de dividir o plano.**
- **Por quê:** a corrente de retorno de alta frequência "não tem vontade" de entrar na área analógica, porque ela corre sob a trilha. Ott: "*It is always better to have only a single reference plane for a system*". "*The key to a successful mixed signal PCB layout ... is proper partitioning and routing discipline, not a split ground plane.*" (FATO, Ott, archive 2022: https://web.archive.org/web/2022/https://www.hottconsultants.com/techtips/split-gnd-plane.html)
- Toradex apresenta o "Virtual Split Approach" (um plano só, com uma linha imaginária que nenhum sinal cruza) como alternativa equivalente ao split físico. (FATO, Toradex §6.9.1.2, https://docs.toradex.com/102492-layout-design-guide.pdf)

**A2. Se for obrigatório dividir o plano (AGND/DGND, terra de potência), faça uma ponte única. Todo sinal que cruza a divisão passa sobre essa ponte, e nenhum sinal digital corre sobre o plano analógico (nem o inverso).**
- **Por quê:** sem a ponte, a corrente de retorno contorna a fenda e forma um laço grande, que irradia e acrescenta indutância. (FATO, Ott split-gnd-plane; Toradex §6.9.1.1; TI SCAA082 §2: "*Connect split ground planes only at one point*", https://www.ti.com/lit/an/scaa082a/scaa082a.pdf)

**A3. Em conversor A/D ou D/A com pinos AGND e DGND, ligue os dois ao MESMO plano de baixa impedância, junto ao pino.**
- **Por quê:** ADI MT-031 e Analog Dialogue ("Grounding (Again)", RAQ 9) recomendam unir AGND e DGND no encapsulamento com conexão mínima. Ott cita a mesma frase dos fabricantes e conclui que a forma mais limpa de cumprir isso é ter um plano só. (FATO para Ott. SECUNDÁRIO para a ADI: o PDF não pôde ser baixado.)

**A4. Nenhuma trilha crítica (clock, USB, SPI rápido, RF, cristal) pode cruzar fenda ou void no plano de referência.**
- Se for inevitável, coloque capacitores de costura de 1 a 10 nF, um de cada lado da trilha, a no máximo 0,1" (2,5 mm) dela. Mesmo assim, o caminho acrescenta pelo menos 5 a 10 nH. (FATO, Ott parte 6: https://web.archive.org/web/2012/http://www.hottconsultants.com/techtips/pcb-stack-up-6.html)
- A TI aceita até 1 µF, "*as close as possible to the plane crossing*". (FATO, SLLA414 §3.5)
- Mantenha os pares diferenciais rápidos a pelo menos 1,5W de qualquer void no plano. (FATO, SLLA414 §4.2)

**A5. Ordem de preferência para trilhas críticas (Ott):**
1. Uma só camada, adjacente a um plano.
2. Duas camadas adjacentes ao MESMO plano. A via passa pelo antipad, e a corrente vai de uma face do plano para a outra pela borda do furo, sem descontinuidade.
3. Duas camadas com planos diferentes do mesmo tipo (GND/GND), com via GND–GND ao lado da via de sinal.
4. Planos de tipos diferentes (GND/PWR), com capacitor de costura ao lado da via.

(FATO, Ott parte 6)

**A6. Via de retorno junto à via de sinal: no máximo 200 mil (5,08 mm) de centro a centro, quanto mais perto melhor, simétrica nos pares diferenciais.**
- (FATO, TI SLLA414 §3.5: "*Place these stitching vias symmetrically within 200 mils (center-to-center, closer is better)*", https://www.ti.com/lit/an/slla414/slla414.pdf. Também SPRAAR7 Fig. 2-11.)
- Toradex: via de GND na origem E no destino do sinal. Quando a referência é PWR, capacitores de costura de **10 a 100 nF** (10 nF para USB/SD). (FATO, Toradex §6.8, Tab. 8 e 15)

**A7. Evite usar o plano de alimentação como referência de sinal rápido.**
- Se não houver como evitar, ponha capacitores de costura e vias de GND na origem e no destino. (FATO, SLLA414 §3.5: "*TI does not recommend high-speed signal references to power planes unless completely unavoidable*")

**A8. Em 2 camadas, imite o plano:**
- Malha de GND (grid).
- GND roteado logo abaixo da alimentação.
- Retorno de cada I/O do MCU sob a própria trilha.
- **Ilha de GND sólida sob o MCU, cerca de 1/4" (6 mm) além do contorno do chip**, ligada ao pino GND, aos capacitores de desacoplamento e ao laço do oscilador.

(FATO, TI SZZA009 §2.1.2–2.1.3, https://www.ti.com/lit/an/szza009/szza009.pdf)
- Na mesma nota: em 2 camadas, trilhas de alimentação e GND com relação comprimento/largura ≤3:1. (FATO)

**A9. Pour de GND nas camadas externas: costure-o ao plano principal com vias "em quantos pontos for possível". Ilha sem via é antena.**
- (FATO, Ott parte 3: "*any unused area on layers 1 and 6 should be provided with 'ground fill' and tied into the primary ground plane, with vias, at as many locations as possible*", https://web.archive.org/web/2012/http://www.hottconsultants.com/techtips/pcb-stack-up-3.html)
- No KiCad, use "Remove islands: Always" nas zonas, ou costure cada ilha. Não deixe cobre flutuante. (INFERÊNCIA)

**A10. Grounding vai além do 0 V: trata de segurança, blindagem e de onde está a energia (campos no dielétrico).**
- Essa é a tese da palestra de Rick Hartley, "How to Achieve Proper Grounding" (Altium Live, 2019). (SECUNDÁRIO: confirmei só a página, o conteúdo veio de resumos. https://resources.altium.com/p/us-how-to-achieve-proper-grounding-rick-hartley-expert-live-training)

### B. Stackup

**B1. Os cinco objetivos de Ott para placas multicamada:**
1. Toda camada de sinal adjacente a um plano.
2. Sinal colado ao plano.
3. PWR e GND colados entre si.
4. Sinais rápidos enterrados entre planos.
5. Vários planos de GND.

Só a partir de 8 camadas dá para atender aos cinco. Em 4 e 6 camadas é preciso escolher. (FATO, Ott parte 1: https://web.archive.org/web/2012/http://www.hottconsultants.com/techtips/pcb-stack-up-1.html)

**B2. Priorize o acoplamento sinal↔plano (objetivo 2) sobre o acoplamento PWR↔GND (objetivo 3).**
- **Por quê:** com construção normal, a capacitância entre os planos é insuficiente para desacoplar abaixo de cerca de 500 MHz. O desacoplamento fica por conta dos capacitores. (FATO, Ott parte 1)

**B3. Para 4 camadas, quatro opções:**
- **Opção 1, SIG/GND/PWR/SIG com prepreg fino (<0,010") e núcleo grosso (>0,040"):** o laço do sinal fica menor (≥10 dB a menos com 0,005"), a impedância do plano cai (menos irradiação de modo comum pelos cabos) e o crosstalk diminui. Ott: "*one of the simplest, least costly, and most overlooked method[s] of reducing radiation*". (FATO, Ott parte 2: https://web.archive.org/web/2016/http://www.hottconsultants.com/techtips/pcb-stack-up-2.html)
- **Opção 2, GND/SIG+PWR/SIG+PWR/GND (planos fora):** segundo Ott, "*the best stack-up possible with a four-layer PCB*" do ponto de vista de EMC. Forma uma gaiola de Faraday se os dois GND forem costurados na periferia. Os contras são retrabalho difícil, o plano picotado pelos pads e o fato de não servir para microstrip de RF na camada externa. (FATO)
- **Opção 3, SIG+PWR/GND/GND/SIG+PWR:** sem blindagem, mas com dois GND (baixa impedância) e retrabalho fácil. É a melhor opção para RF em microstrip com rail único. (FATO para a descrição de Ott; INFERÊNCIA para a aplicação a RF)
- **Com SIG/GND/PWR/SIG:** os sinais da camada 4 tomam o plano de PWR como referência. Rotear o que é rápido na camada 1 ou pôr capacitores de costura. (FATO, Toradex §3.1)

**B4. Stackups de 4 camadas da JLC (1,6 mm, cobre externo de 1 oz/0,035 mm, interno de 0,5 oz/0,0152 mm)**

Fonte: https://jlcpcb.com/impedance (FATO)

| Stackup | Dielétrico L1–L2 (= L3–L4) | Núcleo L2–L3 | εr do prepreg | Comentário |
|---|---|---|---|---|
| JLC04161H-7628 | 7628, 0,2104 mm (8,3 mil) | 1,065 mm | 4,4 | Padrão ("no requirement"). Atende <0,010" (Ott), mas não 0,005". |
| JLC04161H-3313 | 3313, 0,0994 mm (3,9 mil) | 1,265 mm | 4,1 | Bem próximo do ideal de Ott (0,005"). |
| JLC04161H-1080 | 1080, 0,0764 mm (3,0 mil) | 1,265 mm | 3,91 | O mais colado. A trilha de 50 Ω fica estreita. |
| JLC04161H-2116 | 2116, 0,1164 mm | 1,265 mm | 4,16 | Intermediário. |

Núcleo NP-155F com εr 4,6. Máscara de solda com εr 3,8. (FATO, mesma página e guia da calculadora: https://jlcpcb.com/help/article/User-Guide-to-the-JLCPCB-Impedance-Calculator)

**B5. Larguras ESTIMADAS (microstrip na camada externa, sem máscara, Hammerstad-Jensen). Confirme na calculadora da JLC (https://jlcpcb.com/pcb-impedance-calculator) antes de rotear.**

| Stackup | 50 Ω single-ended | 90 Ω diferencial (largura/espaço) |
|---|---|---|
| 7628 (h = 0,21 mm) | ≈0,37 mm | ≈0,25/0,127 · 0,27/0,15 · 0,30/0,20 mm |
| 3313 (h = 0,099 mm) | ≈0,175 mm | ≈0,16/0,127 · 0,17/0,15 · 0,19/0,20 mm |
| 1080 (h = 0,076 mm) | ≈0,14 mm | ≈0,14/0,127 · 0,14/0,15 mm |

- (INFERÊNCIA, cálculo meu.) Conferência cruzada: o guia da Toradex, com prepreg de 112 µm, dá 50 Ω com 180 µm e 90 Ω com 180/165 µm, o que bate com a linha do 3313. (FATO, Toradex Tab. 2)
- A máscara de solda (εr 3,8) baixa a impedância em alguns ohms, e a calculadora da JLC já considera isso.
- A diferença prática entre os dois stackups (INFERÊNCIA): com 7628, a trilha de RF de 50 Ω (~0,37 mm) casa melhor com pads 0402 e com o pino central do SMA. Com 3313, a referência fica mais colada (menos EMI e crosstalk), mas as trilhas são estreitas (~0,17 mm).

**B6. Controle de impedância na JLC: tolerância padrão de ±10%, e ±5% sob pedido especial.** (FATO, jlcpcb.com/capabilities/pcb-capabilities)

**B7. Em 2 camadas, microstrip de 50 Ω de verdade é inviável em 1,6 mm.**
- A trilha teria ≈2,8 mm (cálculo meu, INFERÊNCIA). O Altium cita cerca de 110 mil para εr 4,8. (SECUNDÁRIO)
- O caminho é CPWG (coplanar aterrada) com gap pequeno, ou placa mais fina. O par USB de 90 Ω em 2 camadas é viável como diferencial coplanar: o exemplo do Altium usa 9,5 mil de largura, 5 mil de gap e 5 mil até o GND. Sem controle de impedância, o Altium sugere trilhas com menos de 0,75". (SECUNDÁRIO, Z. Peterson: https://resources.altium.com/p/routing-requirements-usb-20-2-layer-pcb)

**B8. Quando sair de 2 para 4 camadas:**
- Ott: acima de cerca de 10–15 MHz, considere multicamada. "*a four-layer board will produce 15 dB less radiation than a two-layer board*" (regra prática). (FATO, Ott parte 1)
- Contraponto, TI SZZA009: "*A two-layer board can achieve 95% of the effectiveness of a four-layer board*", desde que se imite o plano (A8). (FATO)
- Custo na JLC: promoções e preços mudam. Houve um reajuste de preços FR-4 anunciado para agosto de 2026. Confira a cotação ao vivo. (SECUNDÁRIO: https://jlcpcb.com/news/jlcpcb-fr4-pcb-price-adjustment-august2026)
- Para os produtos da casa (RF 2,4/5 GHz + USB + buck-boost), 4 camadas é o padrão defensável. (INFERÊNCIA, coerente com o §1 do PADROES)

**B9. Para 6 camadas (Ott parte 3):**
- **Não usar** SIG/SIG/GND/PWR/SIG/SIG.
- A mais comum é "pads ou baixa frequência / GND / alta frequência / alta frequência / PWR / baixa frequência". Ela não acopla PWR com GND, então o desacoplamento exige cuidado.
- **SIG/GND/SIG/SIG/PWR/SIG**, com 0,005"/0,005"/0,040"/0,005"/0,005", mantém cada direção de roteamento sempre sobre o mesmo plano.
- **GND/SIG/GND/PWR/SIG/GND** atende aos cinco objetivos, mas só tem duas camadas de roteamento.

(FATO, Ott parte 3)
- Na JLC, o padrão de 6 camadas é o **JLC06161H-3313**: 3313 de 0,0994 mm / núcleo de 0,55 / 2116 / núcleo de 0,55 / 3313. Via-in-pad (POFV) vem por padrão a partir de 6 camadas. (FATO, jlcpcb.com/impedance e capabilities)
- A TI recomenda pelo menos 6 camadas para SoCs com interfaces rápidas e, em camadas de sinal adjacentes, roteamento a 90° uma da outra. (FATO, SPRAAR7 §3.12)

**B10. Stackup simétrico (balanceado), para a placa não empenar.** (FATO, Ott parte 1)

### C. Integridade de sinal (SI)

**C1. Tempo de subida e comprimento crítico (é aproximação, e há debate):**
- Em FR-4, o atraso de microstrip é de cerca de 6 a 7 ps/mm, ou 145 a 170 mm/ns. (INFERÊNCIA, de c/√εef com εef entre 3,1 e 4,2. A TI SCAA082 §1.3 tabela o atraso em ps/100 mm.)
- Regras correntes (SECUNDÁRIO): quando o atraso de ida passa de 1/4 a 1/6 de Tr, trate a trilha como linha de transmissão. A lista EDN diz "terminar se o comprimento em polegadas ≥ Tr em ns". Exemplo: Tr = 1 ns dá algo entre 25 e 40 mm.
- O debate: Z. Peterson (Altium) mostra que as fontes citam frações que vão de 1/2 a 1/20 e que o comprimento crítico depende de banda e da tolerância de impedância. "*Don't use the critical length rule on impedance controlled buses*". A regra só serve em barramentos push-pull sem especificação de impedância (SPI, GPIO), para decidir se vale pôr um resistor série. (FATO: https://resources.altium.com/p/can-we-all-stop-quoting-critical-length-rule)

**C2. Terminação série:**
- **Resistor perto do pino do driver**, com valor ≈ Z0 − R_saída. Na prática fica entre 22 e 33 Ω para CMOS de 3,3 V em linhas de 50 Ω. (INFERÊNCIA)
- Para EMC em MCU (pinos de I/O digital simples), a TI SZZA009 chega a sugerir **50–100 Ω em série em toda saída** e 35–50 Ω em toda entrada, com o resistor colado ao MCU. (FATO, SZZA009 §2.2.5: "*Put a 50-100-Ω resistor in series with every output pin, and 35-50-Ω resistor on every input pin*")
- Técnicas de terminação: série, paralela, Thevenin e AC. (FATO, SCAA082 §1.3.2)

**C3. Crosstalk:**
- TI SLLA414: entre pares diferenciais rápidos, **5W** (largura de 6 mil pede 30 mil de espaço). Para qualquer outro sinal, keep-out de **30 mil**. Para clock ou sinal periódico, **50 mil**. (FATO, SLLA414 §4.1)
- TI SCAA082: no mínimo 2× a largura da trilha entre trilhas paralelas. (FATO)
- Contraponto (LearnEMC): o 3W "*makes no sense*", porque o crosstalk depende do espaçamento em relação à **altura até o plano**. Ott: com espaçamento fixo, o crosstalk é proporcional ao quadrado da altura da trilha. Plano colado reduz mais o crosstalk do que afastar as trilhas. (FATO: https://www.learnemc.com/emc-design-myths; Ott parte 2)
- Na prática: com 3313 (h ≈ 0,1 mm), um espaçamento de 0,3 mm (3h) já é generoso. Com 7628 (h ≈ 0,21 mm), use 0,6 mm ou mais perto de clocks. (INFERÊNCIA)

**C4. Distância da borda e de obstáculos:** par diferencial rápido a **≥90 mil (2,3 mm) da borda do plano de referência**. Não passe trilha rápida sob ou perto de cristal, oscilador, regulador chaveado, furo de montagem ou magnético. (FATO, SLLA414 §4.2)

**C5. USB 2.0 High-Speed (480 Mb/s):**

| Parâmetro | Valor | Fonte |
|---|---|---|
| Impedância | 90 Ω ±15% diferencial, 45 Ω ±15% single-ended | FATO, SLLA414 §2.1 |
| Faixa usada pela TI (AM335x) | 81–90–99 Ω diferencial; 40,5–45–49,5 Ω modo comum | FATO, SPRAAR7 Tab. A-1 |
| Descasamento dentro do par | ≤50 mil (1,27 mm) | FATO, SPRAAR7 Tab. A-1 |
| Descasamento (Toradex) | <7,5 ps ≈ 1,1 mm | FATO, Toradex Tab. 8 |
| Comprimento | ≤12.000 mil (TI) / <200 mm na carrier (Toradex) | FATO |
| Stubs / test points | 0 / 0 | FATO, SPRAAR7 Tab. A-1 |
| Vias | ≤4 por trilha, o mínimo possível, sempre em número igual nas duas | FATO, SPRAAR7; Toradex §6.6 |
| Distância a clock / outros sinais | 50 mil / 30 mil | FATO, SPRAAR7 Tab. A-1 |
| Capacitor de acoplamento AC | proibido | FATO, SLLA414; Toradex |
| Inversão D+/D− | não permitida | FATO, Toradex §7.4 |

- Serpentina de casamento junto da ponta descasada. Escape do encapsulamento a menos de 0,25" do chip. Nada (componente ou via) entre as duas trilhas do par. (FATO, SLLA414 §3.3 e §4.3; Toradex Fig. 19)
- USB Full-Speed (12 Mb/s, como no ESP32 com USB-Serial/JTAG FS) tolera bem trilhas curtas sem impedância controlada. Mesmo assim, rotear como par de 90 Ω não custa nada. (INFERÊNCIA)

**C6. Layout do USB-C:**
- **Ponte A6↔B6 (D+) e A7↔B7 (D−) com stub ≤3,5 mm** no receptáculo. (FATO, TI TUSB321 §10.1: https://www.ti.com/document-viewer/TUSB321/datasheet/layout-guidelines-sllsen99514)
- Um descasamento só "fecha" para uma orientação do plugue. Mantenha o stub curto dos dois lados. (SECUNDÁRIO, fórum)
- Um resistor de 5,1 kΩ independente em CC1 e outro em CC2 já está no §14 do PADROES.

**C7. microSD (SPI ou SDIO):**
- Todas as linhas com o mesmo comprimento, sobre plano de GND, **≤2 vias por linha**.
- **Resistor série de 0 a 22 Ω pelo menos no CLK** quando a distância host↔slot for grande.
- **Pull-ups externos de 10 a 100 kΩ em CMD e DAT** (não confie no pull-up interno). Pull-down de 100 kΩ opcional no CLK, para ele não flutuar no boot.
- Não ponha capacitor só no CLK. Se usar, ≤4,7 pF e igual em todas as linhas.
- Na proteção ESD, prefira diodo rápido com resistor série a filtro RC.

(FATO, Swissbit AN2111, CC BY 4.0)
- Toradex: SD/SDIO 50 Ω ±15%, <100 mm, descasamento de dados contra clock <15 mm a 52 MHz e <3 mm em SDR104. (FATO, Toradex Tab. 15)
- TI (AM6x): resistor série de 0 Ω reservado no CLK, junto ao pino do processador, para ajuste. (SECUNDÁRIO, TI SPRADO2/SPRACU5, via busca)

**C8. I²C:**
- tr máximo de 1000 ns (Standard), 300 ns (Fast) e 120 ns (Fast+). **Cb ≤400 pF (Standard e Fast) e ≤550 pF (Fast+)**.
- Fórmulas: tr = 0,8473 × Rp × Cb, e Rp(mín) = (VCC − VOL)/IOL, com VOL = 0,4 V a 3 mA.

(FATO, TI SLVA689 Tab. 2-1, https://www.ti.com/lit/an/slva689/slva689.pdf)
- Toradex: SDA e SCL juntas, topologia livre (stub não importa), comprimento limitado pela capacitância, <450 mm (Standard). (FATO. Atenção: a Toradex lista 100 pF para Fast Mode, menos que a especificação I²C. Use a TI/NXP como referência.)
- No conector QWIIC/expansão: TVS e, se o cabo for longo, resistor série de 22 a 100 Ω. (INFERÊNCIA)

**C9. Cristais e osciladores:**
- No mesmo lado do chip, **≤12 mm (0,5") dos pinos**, com os capacitores de carga ao lado do cristal. Pour de GND em volta, ligado direto ao GND do MCU, **sem trilha de sinal ou alimentação dentro do pour**. Em placa de 2 lados, nenhuma trilha no lado oposto, sob o cristal. A guarda sempre aterrada. (FATO, Microchip dsPIC33AK §2.6: https://onlinedocs.microchip.com/oxy/GUID-04B5982F-17EC-4A6E-B7FE-72DF0A5463B9-en-US-3/GUID-AA04B64F-3C38-4E1C-8B51-49DE3CFE2419.html)
- GND contínuo na camada adjacente, sob todo o circuito do cristal. Guarda de GND em volta, costurada com várias vias para não deixar stub sem terminação. **Guarda entre XI e XO**: a TI a chama de "crítica", porque sem ela a capacitância shunt reduz o ganho e a partida do oscilador. (FATO, TI AM67 §8.3.1: https://www.ti.com/document-viewer/AM67/datasheet/GUID-FF5AB214-194B-49FD-B2E0-06CC5A7E6E25)
- Divergência: a Arrow recomenda "*Do not lay out the ground (GND) pattern under crystal unit*", por causa da capacitância parasita. Há relato de LSE de 32 kHz que não oscilava com plano embaixo. (SECUNDÁRIO) Conclusão: siga a nota de aplicação do fabricante do chip (ex.: Espressif para o ESP32) e a dos cristais de 32 kHz em particular.
- TI SZZA009: os capacitores do oscilador "deitados" sobre as trilhas, para minimizar a área do laço. (FATO)

### D. EMC

**D1. As fontes de emissão são três (INFERÊNCIA consolidada de Ott partes 1–2 e TI SZZA009 §1.4):**
1. **Laços de corrente** (modo diferencial): a irradiação cresce com a área até 1/4 de λ (λ/4 = 25 cm em 300 MHz). (FATO, SZZA009 §1.4.1)
2. **Cabos como antenas** (modo comum, por causa da queda de tensão no plano de GND): planos de baixa impedância e vários GND reduzem isso. (FATO, Ott partes 1–2)
3. **Bordas de plano e cavidades**: tratadas com via de costura na borda (D3).

**D2. A regra 20H é controversa. Não a aplique como dogma.**
- LearnEMC: "*there is no data that generally supports pulling the edge of the power plane away*" e "*Adhering to a 20-H rule is more likely to create a problem than it is to prevent one*". Mudar o tamanho do plano só desloca a ressonância. (FATO, https://www.learnemc.com/emc-design-myths)
- Montrose et al., IEEE T-EMC vol. 47 nº 2, p. 227–233, 2005 (DOI 10.1109/TEMC.2005.847383): há benefício "*only when implemented in certain applications*". Hubing e Shim (2001) mediram irradiação um pouco maior com 20H. (SECUNDÁRIO, abstracts)
- Na prática: plano de PWR recuado 1 a 2 mm por fabricabilidade, mais costura de GND na borda, rende mais do que 20H. (INFERÊNCIA)

**D3. Vias de costura na borda e cercas de RF:**
- Use ≤λ/20 na maior frequência de interesse nas bordas e cercas, e ≤λ/10 na costura geral. Dica prática da Cadence: a cada 2–5 mm, e nenhum vão maior que 2× o passo nominal. (SECUNDÁRIO: JLC blog https://jlcpcb.com/blog/via-stitching-in-pcb-design; Applied-EE https://applied-ee.github.io/ee-notebook/docs/radio-rf/rf-layout-and-pcb-design/via-placement-and-stitching)
- Cálculo para FR-4 com εr 4,4, λ = c/(f·√εr) (INFERÊNCIA):

| f | λ no FR-4 | λ/20 | λ/10 |
|---|---|---|---|
| 433 MHz | 330 mm | 16,5 mm | 33 mm |
| 868 MHz | 165 mm | 8,2 mm | 16,5 mm |
| 1575 MHz (GPS L1) | 91 mm | 4,5 mm | 9,1 mm |
| 2,45 GHz | 58 mm | 2,9 mm | 5,8 mm |
| 5,8 GHz | 24,6 mm | **1,2 mm** | 2,5 mm |

- Na JLC, o espaçamento furo-a-furo mínimo entre vias é de 0,2 mm. Com via de 0,3/0,5 mm, um passo de 1,2 mm é fabricável. (FATO para a regra, jlcpcb.com/capabilities; INFERÊNCIA para a conta)
- Ott: com GND nas duas camadas externas costurados na periferia, os sinais ficam dentro de uma gaiola de Faraday. (FATO, parte 2)

**D4. Filtros nos conectores:**
- Todo sinal que sai da placa passa por filtro ou proteção **junto ao conector**: ferrite ou choke de modo comum e TVS. Trilhas protegidas e não protegidas não correm juntas. (FATO, SPRAAR7 §3.14: "*Keep any unprotected traces away from protected traces*")
- Em USB, choke de modo comum (CMF) opcional com footprint de 0 Ω 0402 (componentes maiores perdem mais do que o próprio CMF). O conjunto ESD+CMF fica curto e colado ao conector. Void de 60% sob os pads do ESD/EMI em linhas rápidas. (FATO, SPRAAR7 §3.14)
- Em cabos e chicotes: pelo menos um retorno de GND para cada 9 sinais ("prática comum na indústria de computadores"). (FATO, TI SZZA009 §2.5.3)

**D5. ESD/TVS no ponto de entrada (TI SLVA680, https://www.ti.com/lit/an/slva680/slva680.pdf, FATO):**
- V_ESD = V_br + R_dyn·I + (L2+L3)·di/dt. Em 8 kV (IEC 61000-4-2), di/dt = 30 A/0,8 ns = 4×10¹⁰ A/s, então **0,25 nH já somam cerca de 10 V**.
- TVS **o mais perto possível do conector**, e o CI protegido bem mais longe (L4 ≫ L1, para a corrente preferir o TVS).
- **Sem stub** entre a linha e o TVS. A trilha vai do conector direto ao pino do TVS e só depois segue para o CI.
- **Nenhuma via entre o conector e o TVS.** Se houver via, que fique depois do TVS.
- A indutância TVS→GND (L3) é a maior vilã: via de GND curta e larga, direto ao plano.
- Trecho conector→TVS reto. Se precisar curvar, use raio grande ou no máximo 45°. Em 8 kV, um canto de 90° concentra pelo menos 7 kV e pode abrir arco para raios abaixo de cerca de 2,6 mm.
- Keep-out de trilhas desprotegidas nessa região, em todas as camadas por onde passam as vias.
- TI SLVA796 (porta USB): TVS junto ao conector, ligado sem vias. O choke de dados ajuda a passar do nível 4 (±8 kV contato, ±15 kV ar). (FATO)

**D6. Terra de chassi:**
- Separar o GND do TVS e do conector (chassi) por indutância protege muito bem, mas complica o roteamento rápido. Por isso a maioria dos projetos usa GND comum.
- Se houver chassi aterrado, ponha o parafuso ou furo metalizado **junto do GND do TVS e da blindagem do conector**. Sem chassi, use vários planos de GND bem acoplados.

(FATO, SLVA680 §1)
- Para o produto da casa (carcaça plástica, sem terra), use GND comum, blindagem do USB-C ligada ao GND por via curta (ou por RC/ferrite, conforme a nota do fabricante do conector) e TVS no conector. (INFERÊNCIA)

**D7. Pré-conformidade CE: o que cabe ao layout (INFERÊNCIA, detalhar no tema regulatório):**
- Produtos com rádio entram na **RED (2014/53/UE)**. A EMC normalmente segue a ETSI **EN 301 489-1/-17**, que referencia métodos da EN 55032/55035, e o rádio segue a EN 300 328 (2,4 GHz), entre outras. Produtos sem rádio seguem a EN 55032 (emissão, Classe B residencial) e a EN 55035 (imunidade). Confirme no tema regulatório.
- **IEC 61000-4-2**: nível 4 = ±8 kV contato e ±15 kV ar. (FATO, citado na TI SLVA796)
- Do lado do layout: stackup com plano colado (B3), retorno contínuo (A4–A6), filtros e TVS no conector (D4–D5), costura de borda (D3), clock com espectro espalhado (spread spectrum) quando o MCU tiver, resistor série nas saídas rápidas (C2), fonte chaveada longe dos cabos e com laço quente mínimo (tema de potência), e ensaio de pré-varredura com sonda de campo próximo antes do laboratório.

### E. Vias (JLCPCB)

FATO para todos os itens desta seção, salvo indicação: https://jlcpcb.com/capabilities/pcb-capabilities

**E1. Tamanhos:**
- Mínimo em 2 camadas e multicamada: **furo de 0,15 mm / anel de 0,25 mm**.
- 0,1/0,2 mm só em placas de até 1 mm de espessura, com ENIG ou OSP.
- O diâmetro deve ser pelo menos 0,1 mm maior que o furo (0,15 mm é o preferido). Furo mínimo preferido: **0,2 mm**.
- **Custam mais:** furo de 0,1 ou 0,15 mm com qualquer anel, e furo de 0,2 ou 0,25 mm com anel abaixo de 0,45 mm.
- Vias sem acréscimo: **0,3/0,5–0,6 mm** (padrão robusto) ou **0,2/≥0,45 mm** (denso). (INFERÊNCIA a partir da regra acima)

**E2. Espaçamento:** furo-a-furo de via ≥0,2 mm. Furo-a-furo de pad ≥0,45 mm. Anel anular em multicamada: 0,20 mm recomendado, 0,15 mm mínimo.

**E3. Tenting e cobertura:**
- A página lista "plugged" (via preenchida com máscara, acabamento opaco) e preenchimento com epóxi ou pasta de cobre seguido de metalização. Via preenchida não pode ter abertura de máscara em nenhum lado, precisa de ≥0,35 mm até outras aberturas, e o diâmetro máximo preenchido é 0,5 mm.
- **"Tented/untented" não aparece na página** (não encontrado).
- No KiCad: vias com tenting nos dois lados, exceto as de teste. (INFERÊNCIA)

**E4. Via-in-pad (POFV):** preenchida (epóxi ou pasta de cobre) e metalizada por cima. Padrão em 6 camadas ou mais. Aceita vias de 0,15 a 0,55 mm. **Via aberta em pad de BGA ou QFN fino sem POFV puxa a solda (INFERÊNCIA, prática comum).** A página não informa o custo do POFV em 4 camadas.

**E5. Back-drill (só citar):**
- Na JLC: FR-4 de 4 a 32 camadas, espessura ≥0,8 mm, furo de 0,2–0,5 mm, broca 0,2 mm maior, ≥0,15 mm até a camada interna adjacente.
- A TI recomenda stub de via <15 mil, e acima disso back-drill. Irrelevante para USB 2.0 e RF em microstrip de 4 camadas. (FATO, SLLA414 §4.5–4.6)

**E6. Corrente em vias:** pelo menos uma via por ampère, e o mesmo número de vias para o retorno de GND. (FATO, Toradex §6.1)

**E7. Antipad grande em vias de sinal rápido** (30 mil ajuda) e sem pads internos não funcionais. (FATO, SLLA414 §4.8; Toradex Fig. 17)

---

## Erros comuns

| Erro | Consequência | Correção |
|---|---|---|
| Dividir AGND/DGND "porque o datasheet desenha assim" e rotear sinais por cima da fenda | Laço de retorno enorme, irradiação, ruído no ADC | Plano único e particionado (A1). Se dividir, ponte única e nenhum sinal cruzando (A2) |
| Trilha de clock, USB ou SPI cruzando void (ex.: atrás de fileira de vias, recorte do conector) | Descontinuidade de impedância, EMI | Rotear em volta ou capacitor de costura a ≤2,5 mm (A4). Checar com o plano visível no KiCad |
| Trocar de camada sem via de GND ao lado | Retorno procura o capacitor mais próximo, laço grande | Via GND–GND a ≤5 mm, idealmente a ≤1 mm (A6) |
| Sinal rápido na camada 4 sobre plano de PWR, sem costura | Retorno interrompido | Rotear na camada 1 sobre GND, ou usar SIG/GND/GND/SIG (B3), ou capacitor de costura |
| Pour de GND com ilhas sem via (ou uma só via) | Ilha ressoa como antena, DRC "island" | Costurar "em quantos pontos for possível" (A9) ou remover ilhas |
| Usar a 20H como dogma (recuar o PWR 20× h) | Pode aumentar a irradiação | Costurar a borda com vias λ/20 (D2, D3) |
| Aplicar 3W cegamente e ignorar a altura até o plano | Crosstalk mal estimado | Plano colado (3313) mais espaçamento relativo a h (C3) |
| TVS longe do conector, ou com stub ou via entre o conector e o TVS | ESD chega ao CI: cada 0,25 nH soma cerca de 10 V | TVS no conector, linha passando pelo pino do TVS, via de GND curta (D5) |
| Trilha desprotegida correndo ao lado do trecho conector→TVS | Acoplamento do pulso ESD | Keep-out (D5) |
| D+/D− trocados, ou com via ou componente entre as trilhas do par | Não enumera, ou EMI | Inversão não permitida. Par simétrico, nada no meio (C5) |
| Ponte A6/B6 do USB-C longa | Stub, reflexão | ≤3,5 mm (C6) |
| Capacitor só no CLK do microSD "para EMC" | Atraso CLK contra DAT, erros com a temperatura | Nada, ou ≤4,7 pF igual em todas as linhas (C7) |
| Confiar nos pull-ups internos de CMD/DAT do SD | Falhas intermitentes | Externos de 10 a 100 kΩ (C7) |
| Trilha passando sob o cristal, ou cristal longe do pino | Partida lenta, jitter, irradiação | ≤12 mm, sem trilhas embaixo, guarda aterrada e guarda entre XI e XO (C9) |
| Largura de 50 Ω "de olho", ou calculada com εr genérico | Descasamento de RF ou USB | Calculadora da JLC no stackup escolhido (B5) |
| Autorouter rotear USB, RF e cristal junto com o resto | Pares desbalanceados, vias extras, stubs | Rotear à mão e travar ANTES do autorouter. A TI diz "*laid out early (preferably first)*" (SPRAAR7 §1.2) |
| Via de 0,2 mm com anel de 0,4 mm sem perceber | Acréscimo de custo na JLC | 0,2/≥0,45 ou 0,3/0,5–0,6 (E1) |

---

## Checklist

**Stackup e planos**
- [ ] Número de camadas justificado (RF, USB HS, fonte chaveada → 4 camadas). Se for 2 camadas, imitar plano (A8)
- [ ] Stackup JLC escolhido e anotado (7628 ou 3313), com larguras de 50 Ω e 90 Ω da calculadora da JLC registradas no projeto
- [ ] Camada 2 = GND sólido sem recortes sob RF, USB e cristal. Camada 3 = GND (rail único) ou PWR com costura
- [ ] Nenhuma trilha crítica cruza fenda ou void. Pares a ≥1,5W de voids e a ≥2,3 mm da borda do plano
- [ ] Toda troca de camada de sinal crítico tem via de GND a ≤5 mm, idealmente adjacente
- [ ] Pour externo costurado ao GND com várias vias. Zero ilhas flutuantes
- [ ] Borda costurada (≤λ/20 da maior frequência; 1,2 mm se houver 5 GHz) e cercas de RF no mesmo passo

**Sinais**
- [ ] USB: par 90 Ω, descasamento ≤1,1 mm, ≤4 vias (de preferência 0), 0 stubs, 0 test points, a 30 mil de outros sinais e 50 mil de clocks
- [ ] USB-C: pontes A6/B6 e A7/B7 ≤3,5 mm, 5,1 kΩ em CC1 e outro em CC2, blindagem ao GND
- [ ] TVS/ESD no conector (USB, SD, QWIIC, botões externos), sem stub, sem via antes do TVS, GND curto
- [ ] microSD: mesmo comprimento, ≤2 vias, série de 0 a 22 Ω no CLK (perto do host), pull-ups externos de 10 a 100 kΩ, opção de 100 kΩ no CLK
- [ ] I²C: Rp calculado (tr, Cb ≤400 pF)
- [ ] Saídas rápidas que vão longe com resistor série perto do driver
- [ ] Cristal ≤12 mm, sem trilhas embaixo nem no pour, guarda aterrada com vias, guarda entre XI e XO, capacitores de carga ao lado
- [ ] Rotas críticas (RF, USB, cristal) feitas à mão e travadas antes do autorouter

**Vias e fabricação**
- [ ] Vias 0,3/0,5–0,6 ou 0,2/≥0,45 (sem acréscimo). Furo-a-furo ≥0,2 mm
- [ ] Tenting definido. Via-in-pad só com POFV
- [ ] Netclasses com largura/espaço de impedância controlada e regra de par diferencial no KiCad

**EMC**
- [ ] Filtro (ferrite ou CMF) e TVS em toda entrada de cabo
- [ ] Fonte chaveada longe de conectores, cabos e RF
- [ ] Pré-varredura com sonda de campo próximo planejada. Normas (RED/EN 301 489, IEC 61000-4-2) definidas com o tema regulatório

---

## Conflitos com PADROES-PROJETO-PCB.md

Comparei as regras da casa (§1, §3, §11, §12, §14, §15) com a literatura. Não editei o PADROES. A decisão é do dono.

| # | Regra da casa | Literatura | Situação |
|---|---|---|---|
| 1 | §1: 4 camadas para RF, energia limpa e muitas ilhas de GND | Ott: 4 camadas ≈ 15 dB menos de irradiação e multicamada acima de 10–15 MHz. TI SZZA009: 2 camadas bem feitas chegam a "95%" | **Confirma.** Acrescentar o contraponto da TI para placas simples e as técnicas A8 quando ficar em 2 camadas |
| 2 | §1: stackup de referência **JLC04161H-7628** | Ott quer o sinal a <0,010" do plano e mostra cerca de 10 dB a mais com 0,005". O 7628 tem 0,21 mm (dentro de 0,010"). O **3313** tem 0,099 mm (≈0,004") | **Diverge parcialmente / falta.** O 7628 é aceitável e dá trilha de 50 Ω larga (~0,37 mm, melhor para pads 0402 e SMA, INFERÊNCIA). O 3313 dá menos EMI e crosstalk, com trilhas de ~0,17 mm. Avaliar o 3313 como alternativa e registrar o critério |
| 3 | §1: não define o uso da camada 3 | Ott: SIG/GND/GND/SIG (alimentação por trilhas largas) é muito bom com rail único. Com SIG/GND/PWR/SIG, os sinais da camada 4 exigem costura (Toradex, TI) | **Falta.** Com o rail único de 3V3 do §7, SIG+PWR/GND/GND/SIG+PWR é candidato natural |
| 4 | §3/§14: cercas de via separando domínios de RF, sem passo definido | ≤λ/20 nas cercas e bordas. Em 5,8 GHz ≈ 1,2 mm, em 2,4 GHz ≈ 2,9 mm (SECUNDÁRIO + cálculo) | **Falta.** Definir o passo pela maior frequência (ESP32-C5 dual-band → ~1,2 mm) |
| 5 | §14: capacitores de carga do cristal simétricos, com GND sólido contínuo logo abaixo | Microchip e TI AM67 confirmam. A TI acrescenta guarda entre XI e XO e guarda costurada. A Microchip pede ≤12 mm e nenhuma trilha no lado oposto. A Arrow diverge (sem GND sob o cristal) | **Confirma**, com acréscimos e um alerta para conferir o datasheet de cada chip |
| 6 | §15, passo 4: Freerouting na placa inteira | TI SPRAAR7/SLLA414: sinais rápidos "*must be laid out early (preferably first)*". O autorouter não garante simetria do par, número igual de vias nem ausência de stubs | **Diverge / falta.** Rotear à mão e travar USB D+/D−, RF de 50 Ω e cristal antes do Freerouting (pela ordem do §12, o placement continua vindo primeiro) |
| 7 | §15, passo 6 (`island_fix.py`): **uma** via por ilha do pour | Ott: ground fill ligado ao plano "*at as many locations as possible*" | **Diverge.** Uma via deixa a ilha quase flutuante em alta frequência. Costurar com várias vias (passo λ/10–λ/20) ou remover a ilha |
| 8 | §15, passo 5: via de GND de 0,6 mm junto a pinos | JLC: 0,3/0,5–0,6 mm não paga acréscimo. 0,2/0,45 mm também não. Furo-a-furo ≥0,2 mm | **Confirma**, com uma opção mais densa sem custo extra (0,2/0,45) para os casos apertados citados no §15 |
| 9 | §11: "ilhas de GND fechadas (idealmente plano contínuo de 4 camadas)" | Ott, TI e Toradex: plano contínuo é o ideal. Acrescentam que nenhum sinal crítico pode cruzar fenda ou void e que toda troca de camada precisa de via de retorno | **Confirma / falta.** Acrescentar ao §12 o item "verificação de caminho de retorno" (fendas, voids atrás de fileiras de vias, trocas de camada) |
| 10 | §6/§14: USB-C, 2× 5,1 kΩ, hub | Faltam regras de SI e ESD do USB: 90 Ω, descasamento ≤1,1 mm, 0 stubs, pontes A6/B6 e A7/B7 ≤3,5 mm, TVS no conector sem via antes | **Falta.** Incluir no §6 ou §12 |
| 11 | §7: ferrite + LC por rádio | Não é escopo deste tema (ver tema de energia). Nada contra | — |
| 12 | §12: checklist sem itens de EMC/ESD | TVS e filtro em toda entrada de cabo, costura de borda, resistor série no CLK do SD | **Falta** |

---

## Bibliografia

### Livros (só citar, não baixar)
- **Henry W. Ott — *Electromagnetic Compatibility Engineering*, Wiley, 2009 (ano de memória, a conferir).** A referência sobre aterramento, stackup e retorno. Os Tech Tips on-line (abaixo) são um resumo gratuito do autor.
- **Henry W. Ott — *Noise Reduction Techniques in Electronic Systems*, 2ª ed., Wiley, 1988 (edição e ano de memória, a conferir).** O clássico anterior (acoplamento por impedância comum).
- **Eric Bogatin — *Signal and Power Integrity – Simplified*, 3ª ed., Prentice Hall, 2018.** (Edição e ano de memória, a conferir.) Didático em retorno, indutância de laço e crosstalk.
- **Howard W. Johnson e Martin Graham — *High-Speed Digital Design: A Handbook of Black Magic*, Prentice Hall, 1993, ISBN 0-13-395724-1.** E *High-Speed Signal Propagation: Advanced Black Magic*, 2003. (FATO: citados na TI SPRAAR7 §4)
- **Mark I. Montrose — *Printed Circuit Board Design Techniques for EMC Compliance*, 2ª ed., IEEE Press/Wiley, 2000 (edição e ano de memória, a conferir).** Página da editora: https://www.wiley-vch.de/en/areas-interest/engineering/printed-circuit-board-design-techniques-for-emc-compliance-978-0-7803-5376-3
- **Keith Armstrong — *EMC for Printed Circuit Boards*.** Mais a série gratuita "Design Techniques for EMC" (EMC Journal, 1999, 6 partes; parte 5 = PCB) e "Advanced PCB design and layout for EMC" (2004). Site oficial (emcstandards.co.uk) não verificado nesta sessão. Só encontrei espelhos de terceiros, que não cito como fonte.
- **Würth Elektronik — *Trilogy of Magnetics*** (filtros, ferrites, EMC). Livro do fabricante, citar apenas.

### Normas (só citar)
- IPC-2141A (projeto de impedância controlada), IPC-2221/2222 (projeto de PCB), IPC-6012 (qualificação).
- IEC 61000-4-2 (ESD), EN 55032 (emissão de equipamento multimídia), EN 55035 (imunidade), ETSI EN 301 489-1/-17 (EMC de equipamento de rádio), EN 300 328 (2,4 GHz).

### Application notes e guias (com PDF baixado em `pdfs\04-emc\`)
- TI **SLLA414A** — High-Speed Layout Guidelines for Signal Conditioners and USB Hubs (2025/2026). Retorno, split, costura de 200 mil, 5W, 90 mil da borda, stubs. https://www.ti.com/lit/an/slla414/slla414.pdf
- TI **SPRAAR7J** — High-Speed Interface Layout Guidelines (2023). Tabelas de USB 2.0, ESD/EMI, stackups de 6 camadas ou mais. https://www.ti.com/lit/an/spraar7j/spraar7j.pdf
- TI **SZZA009** — PCB Design Guidelines for Reduced EMI (1999). Laços, 2 contra 4 camadas, malha de GND, resistor série. https://www.ti.com/lit/an/szza009/szza009.pdf
- TI **SLVA680A** — ESD Protection Layout Guide (2022). Indutância, posição do TVS, vias, chassi. https://www.ti.com/lit/an/slva680/slva680.pdf
- TI **SCAA082A** — High-Speed Layout Guidelines (2017). Linhas de transmissão, terminação, crosstalk, split. https://www.ti.com/lit/an/scaa082a/scaa082a.pdf
- TI **SLVA796** — Effective System ESD Protection Guidelines, TPS254x USB Charging Port (2016). https://www.ti.com/lit/an/slva796/slva796.pdf
- TI **SSZB130** — System-Level ESD Protection Guide (o arquivo baixado é a rev. E, 2025). Seleção de TVS por conector. https://www.ti.com/lit/sg/sszb130d/sszb130d.pdf
- TI **SLVA689A** — I2C Bus Pullup Resistor Calculation. https://www.ti.com/lit/an/slva689/slva689.pdf
- **Toradex** — Layout Design Guide. Stackups com larguras, USB, SD, I²C, split virtual, costura. https://docs.toradex.com/102492-layout-design-guide.pdf
- **Swissbit AN2111** — SD Memory Card Design-in (CC BY 4.0). https://www.swissbit.com/media/pages/support/application-notes/sd-memory-card-design-in/bb4ec98db1-1775746198/an2111en_sd_memory_card_design-in.pdf

### Application notes citadas, sem PDF (download bloqueado ou não lido; URL vista em resultado de busca)
> Verificação de URL (2026-11-20, curl): analog.com, st.com, arrow.com, microchip.com e we-online.com recusam acesso automatizado (código 000/403), então não deu para confirmar o HTTP 200 dessas. Elas vieram de resultados de busca. Todas as URLs da TI, Toradex, Swissbit, JLC, Altium, LearnEMC, colorado.edu, archive.org (Ott), Microchip onlinedocs e scholarsmine retornaram 200.
- ADI **MT-031** — Grounding Data Converters and Solving the Mystery of "AGND" and "DGND" (Kester, Bryant, Byrne, rev. A 2008). https://wcm-cce.cldnet.analog.com/media/en/training-seminars/tutorials/mt-031.pdf. Correlatos lidos só na busca: https://www.analog.com/en/resources/analog-dialogue/articles/grounding-again.html e https://www.analog.com/en/resources/analog-dialogue/raqs/raq-issue-9.html
- ADI **MT-101** — Decoupling Techniques. URL não verificada nesta sessão.
- ST **AN1709** — EMC design guide for STM8, STM32 and legacy MCUs (rev. 2022). https://st.com/resource/en/application_note/an1709-emc-design-guide-for-stm8-stm32-and-legacy-mcus-stmicroelectronics.pdf
- ST **AN5612** — ESD protection of STM32 MCUs and MPUs. https://www.st.com/resource/en/application_note/an5612-esd-protection-of-stm32-mcus-and-mpus-stmicroelectronics.pdf
- ST **AN2867** — Oscillator design guide for STM8/STM32. URL não confirmada (tempo esgotado).
- Microchip **AN1517** — PCB Layout Guide for USB 2.0 Hubs. https://microchip.com/en-us/application-notes/an1517. AN26.2: só espelhos encontrados.
- Microchip dsPIC33AK — §2.6 External Oscillator Layout Guidance (página lida). https://onlinedocs.microchip.com/oxy/GUID-04B5982F-17EC-4A6E-B7FE-72DF0A5463B9-en-US-3/GUID-AA04B64F-3C38-4E1C-8B51-49DE3CFE2419.html
- TI **AM67** — datasheet §8.3.1, layout do cristal (página lida). https://www.ti.com/document-viewer/AM67/datasheet/GUID-FF5AB214-194B-49FD-B2E0-06CC5A7E6E25
- TI **TUSB321** — datasheet §10.1, stub A6/B6 ≤3,5 mm (página lida). https://www.ti.com/document-viewer/TUSB321/datasheet/layout-guidelines-sllsen99514
- Würth **ANP044** — Impact of layout, components and filters on the EMC of DC/DC (mais útil no tema de energia). https://www.we-online.com/components/media/o109026v410%20ANP044d_Impact%20of%20the%20layout%2C%20components%2C%20and%20filters.pdf
- Arrow — Crystal and oscillator PCB design considerations (divergência sobre GND sob o cristal). https://www.arrow.com/en/research-and-events/articles/crystal-oscillator-printed-circuit-board-design-considerations

### Artigos do autor e páginas técnicas
- Henry Ott, Tech Tips. O site atual responde 403 e parte do domínio serve spam. Lidos em snapshots do archive.org:
  - Grounding of Mixed Signal PCBs (snapshot 2022): https://web.archive.org/web/2022/https://www.hottconsultants.com/techtips/split-gnd-plane.html
  - PCB Stack-Up parte 1, Introdução (snapshot 2012): https://web.archive.org/web/2012/http://www.hottconsultants.com/techtips/pcb-stack-up-1.html
  - Parte 2, 4 camadas (snapshot 2016): https://web.archive.org/web/2016/http://www.hottconsultants.com/techtips/pcb-stack-up-2.html
  - Parte 3, 6 camadas (snapshot 2012): https://web.archive.org/web/2012/http://www.hottconsultants.com/techtips/pcb-stack-up-3.html
  - Parte 6, descontinuidades de retorno (snapshot 2012): https://web.archive.org/web/2012/http://www.hottconsultants.com/techtips/pcb-stack-up-6.html
- LearnEMC (Hubing e colaboradores) — EMC Design Myths (20H, 3W, cantos de 90°, capacitores): https://www.learnemc.com/emc-design-myths. Também QOTW de 25/12/2023 sobre 20H: https://learnemc.com/qotw-231225 (SECUNDÁRIO)
- Montrose et al. — "Analysis on the effectiveness of the 20-H rule...", IEEE T-EMC 47(2):227–233, 2005, DOI 10.1109/TEMC.2005.847383. "20-H Rule Modeling and Measurements": https://scholarsmine.mst.edu/ele_comeng_facwork/5806 (SECUNDÁRIO, abstract)
- Eric Bogatin — Rules of Thumb (índice das colunas EDN: banda×Tr, stub, crosstalk, indutância de retorno): https://www.colorado.edu/faculty/bogatin/rules-thumb
- Zachariah Peterson (Altium) — "Can We All Stop Quoting the Critical Length Rule?": https://resources.altium.com/p/can-we-all-stop-quoting-critical-length-rule. E "Routing Requirements for a USB Interface on a 2-Layer PCB": https://resources.altium.com/p/routing-requirements-usb-20-2-layer-pcb
- Rick Hartley — "[LIVE] How to Achieve Proper Grounding" (Altium, 2019, cerca de 2h19): https://resources.altium.com/p/us-how-to-achieve-proper-grounding-rick-hartley-expert-live-training

### Ferramentas e calculadoras
- JLCPCB, calculadora de impedância: https://jlcpcb.com/pcb-impedance-calculator. Stackups: https://jlcpcb.com/impedance. Guia: https://jlcpcb.com/help/article/User-Guide-to-the-JLCPCB-Impedance-Calculator
- JLCPCB, capacidades (vias, POFV, back-drill, impedância): https://jlcpcb.com/capabilities/pcb-capabilities
- JLCPCB blog, via stitching (λ/10, λ/20): https://jlcpcb.com/blog/via-stitching-in-pcb-design (SECUNDÁRIO)
- KiCad PCB Calculator (aplicativo embutido: microstrip, coplanar, par acoplado) e Layer Stack Manager.

### Lacunas desta pesquisa
- PDFs de ADI, ST, NXP, Microchip, Silicon Labs e Würth não puderam ser baixados (bloqueio do servidor). Os números deles não foram lidos aqui.
- As larguras de impedância são estimativas minhas (B5). Falta rodar a calculadora da JLC para 7628 e 3313, para 50 Ω CPWG e 90 Ω diferencial.
- Não achei fonte primária lida para o passo λ/20 nem para a regra de comprimento crítico.
- O conteúdo da palestra de Hartley e dos artigos de Armstrong não foi verificado em primeira mão.
- Nota de cristal específica da Espressif (ESP32-C5) não verificada. Fica para o tema de RF ou MCU.
