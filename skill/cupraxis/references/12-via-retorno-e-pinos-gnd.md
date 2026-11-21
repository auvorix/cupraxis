# 12: Via de retorno na troca de camada e pinos de GND em conectores e cabos

Pesquisa de 2026-11-21. Escopo: duas regras contestadas da skill e a conta de λ/20.

**Legenda das etiquetas:**
- **FATO:** li o texto na fonte primária (PDF extraído com pdftotext, página baixada com curl ou código-fonte).
- **FATO-sec:** li a fonte só por um resumo automático de página (WebFetch), sem o texto bruto. O conteúdo é confiável, mas a citação pode não ser literal.
- **INFERÊNCIA:** conta ou raciocínio meu.
- **não encontrado:** procurei e não achei fonte.

Os PDFs ficam em `pdfs/12-via-gnd/` (licenças em `pdfs/12-via-gnd/LICENSES.md`). Os da TI, Toradex e NXP já estavam em `pdfs/04-emc/`.

---

## Resumo executivo

**Tópico 1: via de retorno na troca de camada.**
- As duas fontes primárias com número convergem em **cerca de 5 mm como limite superior** numa placa de 1,6 mm:
  - TI SLLA414A/SPRAAR7J: "*within 200 mils (center-to-center, closer is better)*" (FATO).
  - Archambeault (IEEE EMCS): "*within five times the plane-to-plane distance*" (FATO). Com o núcleo L2–L3 da JLC, isso dá 5,3 mm (7628) e 6,3 mm (3313) (INFERÊNCIA).
- O "≤ 2h ou 1 mm" do kicad-happy (RP-001) **não tem fonte primária numérica.** Ele cita Ott Parte 6, mas Ott Parte 6 só diz "*immediately adjacent*", sem número (FATO, li o texto).
  - No código, h é a **primeira** camada dielétrica (o prepreg L1–L2). Por isso, em 4 camadas na JLC, o raio sai sempre 1,0 mm (FATO no código; INFERÊNCIA na consequência).
  - Fisicamente, o h que importa para a troca de referência é o da **cavidade entre os planos** que a corrente de retorno precisa atravessar (o núcleo), e não o prepreg (INFERÊNCIA, apoiada em Archambeault).
- A física dá um resultado contraintuitivo: a indutância do par via de sinal + via de retorno cresce só com o **logaritmo** da distância (INFERÊNCIA, cálculo abaixo).
  - No JLC04161H-7628 ela vai de ≈0,6 nH (vias coladas) a ≈0,8 nH (1 mm), ≈1,1 nH (2 mm) e ≈1,5 nH (5 mm).
  - Por isso a distância pesa pouco em sinais lentos e muito quando o tempo de subida cai abaixo de ~1 ns, ou quando **vários sinais compartilham a mesma via** (ruído de terra somado).
- **Regra recomendada:**
  - **Alvo** ≤ 1 mm entre centros (colada, o que o DRC deixar) para borda rápida.
  - **Limite** ≤ 5 mm para tudo, inclusive sinal lento.
  - **Uma via por sinal rápido** (ou 1–2 simétricas por par diferencial).
  - Troca **GND↔PWR** não se resolve com via: exige capacitor de costura colado, ou reroteamento.

**Tópico 2: razão sinal:GND em conectores e cabos.**
- A regra "1 GND para cada 9 sinais", atribuída à TI SZZA009, é uma **leitura errada.** O texto (FATO, SZZA009 §2.5.3, nov./1999) diz:
  - 1:9 é o **piso** ("*Never run less than one ground return for every nine signal lines, even if it is just the jumper cable to the front-panel display in a completely sealed metal box*").
  - Cabo **> 1 pé (30 cm)** deve ter **1:4**.
  - Em velocidades maiores a prática "*is moving toward 1:5*".
  - O **melhor** é **1:1, em par trançado**.
- O 1:4 do kicad-happy (IO-002) não cita fonte, mas coincide com a cláusula "> 1 pé" da SZZA009.
- Mais importante que a razão é a **posição**: todo sinal rápido precisa ter um GND **vizinho**.
  - No header Samtec de 2,54 mm (TSM/SSW), pôr um GND entre agressor e vítima derruba o NEXT de sinal simples de **16,25 % para 1,77 %** (tr = 100 ps) e de **6,29 % para 0,77 %** (tr = 500 ps) (FATO).
- **Regra recomendada:**
  - **≥ 1:4** como padrão (aviso abaixo disso); **< 1:9 é erro.**
  - **1:1 ou 2:1** (todo sinal encostado num GND) para clock, SPI/SDIO/QSPI rápidos e cabos longos.
  - **GSSG** para pares diferenciais.
  - Contar também os GND pela **corrente de retorno** da alimentação.

**Ponto lateral λ/20:**
- A 2,45 GHz: **3,37 mm** com εeff 3,3 e **2,92 mm** com εr 4,4. A 5,8 GHz: 1,42 mm e 1,23 mm (INFERÊNCIA, conta).
- Para cerca de vias e costura de borda vale o **εr do dielétrico** (2,9 mm / 1,2 mm), porque os modos de cavidade vivem dentro do FR-4 (INFERÊNCIA).
- Não achei fonte primária de fabricante para λ/20 (não encontrado). Um artigo IEEE (Fang/Hwang 2023) dá um ótimo próximo de λ₀/37,5 ≈ λg/18 num caso específico (FATO + INFERÊNCIA).

**Confiança:**
- Leitura da SZZA009: **alta.**
- Distância da via de retorno: **média.** Há duas heurísticas primárias que convergem, mas não achei estudo publicado de "erro × distância" para placas como as nossas.
- λ/20: **média-baixa** (sem fonte primária).
- Regras de razão S:G por caso: **média.**

---

## Tópico 1: via de retorno junto da via de sinal que troca de referência

### 1.1 Física

1. **A corrente de retorno de alta frequência anda no plano logo abaixo da trilha, seja ele GND ou PWR, e só na superfície do cobre.** Ott: "*the lowest impedance return path is in a plane directly underneath the signal trace (irrespective of whether this is a power or ground plane)*". Também: "*at high-frequency all currents in conductors are surface currents. This affect will occur at all frequencies above 30 MHz for 1 oz. copper layers*". Um plano é, portanto, "*really two conductors not one*". (FATO, Ott, *PCB Stack-Up Part 6*, https://web.archive.org/web/2012/http://www.hottconsultants.com/techtips/pcb-stack-up-6.html)

2. **Quando o sinal troca de camada e a referência troca de plano, o retorno precisa de um caminho de um plano para o outro.**
   - Sem via ou capacitor por perto, Ott diz que "*the interplane capacitance is not usually large enough to be effective, so the return current will have to flow through the nearest decoupling capacitor*". Também diz que a capacitância entre planos só ajuda "*in the case of frequencies considerably above 500 MHz*". (FATO, Ott Parte 6)
   - Ordem de grandeza (INFERÊNCIA, C/A = ε₀εr/d):
     - Núcleo de 1,065 mm (JLC04161H-7628, εr 4,4): ≈ 3,7 pF/cm².
     - Prepreg de 0,1 mm: ≈ 39 pF/cm².

3. **Corrente de deslocamento e cavidade.**
   - A via de sinal atravessa a cavidade formada pelos dois planos de referência. A parte do retorno que não acha uma via ou capacitor vira **corrente de deslocamento** entre os planos e excita a cavidade como um guia de placas paralelas.
   - Fang/Hwang (IEEE EMC+SIPI 2023): "*the through-hole signal via excites the electromagnetic waves between planes ... standing waves appear with multiple resonance frequencies inside the power/ground plane and make a high-impedance return current path. These resonance waves are responsible for the open edge radiation*". (FATO, `pdfs/12-via-gnd/nsf-par-10465871.pdf`, https://par.nsf.gov/servlets/purl/10465871)
   - No caso estudado (câmera de 6 camadas), os picos de potência irradiada coincidiram com as ressonâncias da cavidade PWR/GND. No pico de acoplamento, a corrente no plano de alimentação subiu **30 dB**. (FATO, mesma fonte)
   - Weir (IPBLOX, 2012): "*When a signal traverses any cavity, the entire signal energy is impressed across the local impedance of the cavity*". Também: "*Injected power adds linearly, while noise voltage increases as the square root of the number of signals. A few signals can be OK where many can be disastrous*". (FATO, texto lido em https://ewh.ieee.org/r6/scv/emc/archive/022012SteveWeir.pdf; cópia local apagada por aviso de direitos)
   - Bogatin: trocar o retorno entre planos de tensões diferentes "*run[s] the risk of launching high bandwidth return currents into the cavity ... a source of long-range crosstalk and potentially a source of radiated emissions noise*". A solução que ele indica é dielétrico fino entre PWR e GND. (FATO, Bogatin, *Seven Tips for Your Next Stackup Design*, Design007, fev./2021, https://iconnect007.com/article/126202/seven-tips-for-your-next-stackup-design/126205/pcb)

4. **Primeira ressonância de uma cavidade retangular** (INFERÊNCIA, f₁₀ = c/(2a√εr), εr 4,4, borda aberta):

   | Lado a | f₁₀ |
   |---|---|
   | 30 mm | 2,38 GHz |
   | 50 mm | 1,43 GHz |
   | 80 mm | 0,89 GHz |
   | 100 mm | 0,71 GHz |

   - Placas IoT de 30–80 mm têm ressonâncias de cavidade justamente em 0,9–2,4 GHz, na faixa de Wi-Fi, BLE e GNSS.
   - As vias de costura dividem a cavidade e empurram as ressonâncias para cima. Weir: "*Cavity planes joined by only one via exhibit stiff resonances at low frequencies. Increasing the number of tie points divides the geometry, pushing resonant frequency up and overall noise down*". (FATO, Weir 2012)
   - Hubing (Clemson): os planos de referência "*should be connected to each other (stitched) using vias at every opportunity to prevent cavity resonances between the planes*". (FATO, https://cecas.clemson.edu/cvel/emc/FAQ/question-pcbdes07.html)

5. **Indutância do caminho de retorno em função da distância** (INFERÊNCIA, modelo de duas hastes paralelas entre planos):
   - Fórmula: L = (μ₀·d/π)·arccosh(s/2r), com d = altura da cavidade atravessada, s = distância entre centros e r = raio do furo (0,15 mm, furo de 0,3 mm). μ₀/π = 0,4 nH/mm.
   - O modelo vale para a parte da via dentro da cavidade e ignora pads, antipads e o stub.

   | Cavidade atravessada pelo retorno | s = 0,65 mm (colada) | 1 mm | 2 mm | 3 mm | 5 mm | 10 mm |
   |---|---|---|---|---|---|---|
   | JLC04161H-7628, núcleo L2–L3 de 1,065 mm | 0,60 nH | 0,80 | 1,10 | 1,28 | 1,49 | 1,79 |
   | JLC04161H-3313, núcleo L2–L3 de 1,265 mm | 0,71 nH | 0,95 | 1,31 | 1,51 | 1,77 | 2,12 |
   | 2 camadas, 1,6 mm (pour de cima ↔ pour de baixo) | 0,90 nH | 1,20 | 1,65 | 1,92 | 2,24 | 2,69 |
   | Prepreg de 0,21 mm (só para comparação) | 0,12 nH | 0,16 | 0,22 | 0,25 | 0,30 | 0,35 |

   - **Leitura** (INFERÊNCIA):
     - Ir de "colada" para 5 mm só multiplica L por ~2,5. A indutância é logarítmica, e por isso a distância é uma alavanca fraca.
     - A alavanca forte é a **altura da cavidade** (linear em d).
     - **O 3313 é ligeiramente pior que o 7628 na troca L1↔L4**, porque o prepreg é mais fino mas o núcleo é mais grosso (1,265 contra 1,065 mm). Isso contraria a intuição de que "3313 é melhor em tudo".
     - O "2h" do kicad-happy, calculado sobre o prepreg, não descreve essa geometria.
   - Os dados de stackup da JLC são FATO (https://jlcpcb.com/impedance, já registrados em `04-gnd-si-emc-stackup.md`): 7628 com prepreg de 0,2104 mm e núcleo de 1,065 mm; 3313 com prepreg de 0,0994 mm e núcleo de 1,265 mm.

6. **Tempo de subida, banda e frequência de joelho.**
   - Bogatin, Rule of Thumb #1: BW ≈ 0,35/RT, com RT de 10–90 % (1 ns → 350 MHz). (FATO-sec, https://www.edn.com/electronics-blogs/bogatin-s-rules-of-thumb/4424573/rule-of-thumb--1--the-bandwidth-of-a-signal-from-its-rise-time)
   - O f_knee = 0,5/tr de Johnson aparece em fontes secundárias. Não li o livro (não encontrado na fonte primária).
   - Reatância da via de retorno no joelho (INFERÊNCIA, X = 2π·f·L, com f = 0,5/tr):

   | tr | f (0,5/tr) | L = 0,6 nH | 0,8 nH (1 mm) | 1,1 nH (2 mm) | 1,5 nH (5 mm) | 5 nH (capacitor, Ott) | 10 nH |
   |---|---|---|---|---|---|---|---|
   | 5 ns | 100 MHz | 0,4 Ω | 0,5 Ω | 0,7 Ω | 0,9 Ω | 3,1 Ω | 6,3 Ω |
   | 1 ns | 500 MHz | 1,9 Ω | 2,5 Ω | 3,5 Ω | 4,7 Ω | 15,7 Ω | 31 Ω |
   | 0,5 ns | 1 GHz | 3,8 Ω | 5,0 Ω | 6,9 Ω | 9,4 Ω | 31 Ω | 63 Ω |
   | 0,1 ns | 5 GHz | 19 Ω | 25 Ω | 35 Ω | 47 Ω | 157 Ω | 314 Ω |

   - Comparado com uma linha de 50 Ω: até ~5 Ω é desprezível. Com tr ≤ 0,5 ns, 5 mm (9 Ω) já pesa, e com 0,1 ns qualquer distância é significativa (INFERÊNCIA).
   - Weir chega a uma conta parecida: "*100ps TR = 3.5GHz FKNEE; 1nH = 22 Ohms @ 3.5GHz*". (FATO, Weir 2012)

7. **Ruído de terra quando vários sinais compartilham um retorno.**
   - Bogatin, Rule of Thumb #8: "*% ground bounce noise = 2% per signal per nH / RT[nsec]*". Exemplo dele: 3 sinais, 5 nH, 2 ns → 15 %, "*a bit more than most systems can tolerate*". Com 1 ns → 30 %, "*pathological*". (FATO-sec, https://www.edn.com/electronics-blogs/all-aboard-/4429476/how-to-estimate-ground-bounce-in-a-connector--rule-of-thumb--8)
   - Aplicando a regra a uma via de retorno compartilhada (INFERÊNCIA; a regra foi feita para conectores, aqui é extrapolada):

   | L da via comum | tr | N = 1 | N = 4 | N = 9 |
   |---|---|---|---|---|
   | 0,8 nH (1 mm) | 10 ns | 0,16 % | 0,6 % | 1,4 % |
   | 0,8 nH | 2 ns | 0,8 % | 3,2 % | 7,2 % |
   | 0,8 nH | 0,5 ns | 3,2 % | 12,8 % | 28,8 % |
   | 1,5 nH (5 mm) | 10 ns | 0,3 % | 1,2 % | 2,7 % |
   | 1,5 nH | 2 ns | 1,5 % | 6,0 % | 13,4 % |
   | 1,5 nH | 0,5 ns | 6,0 % | 24 % | 54 % |

   - Conclusão (INFERÊNCIA):
     - Sinais lentos (tr ≥ 2 ns) podem compartilhar uma via de retorno a até ~2–5 mm em grupos de até ~4.
     - Sinais com tr ≤ 1 ns precisam de **via própria e colada.**

### 1.2 O que as fontes dizem (com citações)

| Fonte | O que diz | Número | Etiqueta |
|---|---|---|---|
| **TI SLLA414A** (ago./2025, rev. jan./2026) §3 | "*The entirety of any high-speed signal trace must maintain the same GND reference from origination to termination. If unable to maintain the same GND reference, via-stitch both GND planes together ... Place these stitching vias symmetrically within 200 mils (center-to-center, closer is better) of the signal transition vias.*" | 200 mil = 5,08 mm, máximo | FATO, `pdfs/04-emc/TI-SLLA414-highspeed-layout-USB-hubs.pdf` |
| **TI SPRAAR7J** (2023) §2 | Texto igual. A figura 2-11 mostra "*200 mils (max)*" | 5,08 mm | FATO, `pdfs/04-emc/TI-SPRAAR7-highspeed-interface-layout.pdf` |
| **TI SLLA414A** | Referência em PWR: "*use AC coupling capacitors and ground vias to allow the return signal to have a path back*". Para cruzar split: capacitores "*1 µF or lower and placed as close as possible to the plane crossing*" | ≤ 1 µF | FATO |
| **TI SCAA082A** (2017) | "*add some ground vias around the signal via. This is a similar structure to a coaxial line*" e "*Use ground vias around the signal via to make sure that the return current can flow as close as possible to the signal*" | sem número | FATO, `pdfs/04-emc/TI-SCAA082-highspeed-layout.pdf` |
| **Archambeault**, IEEE EMCS Newsletter, outono/2007, "Design Tid-Bit" | "*Maintaining a return via that connects the two return planes within five times the plane-to-plane distance will help minimize the return current spread and, therefore, the EMI noise between the planes. The closer the return via is to the signal via, the lower the EMI noise created by this signal via.*" | ≤ 5 × (distância entre planos) | FATO, `pdfs/12-via-gnd/IEEE-EMCS-Archambeault-designtip-fall07.pdf` |
| **Ott**, Stack-Up Parte 6 | Planos do mesmo tipo: "*you can put a via (ground to ground or power to power) instead of a capacitor immediately adjacent to the signal via*". De PWR para GND: "*place an additional decoupling capacitor adjacent to the signal via ... This adds considerable additional inductance in the return path (typically 5 to 10 nH)*" | "imediatamente adjacente"; capacitor = 5–10 nH | FATO |
| **Ott**, Parte 6 (fenda/split) | Capacitores "*0.001 to 0.01 uF according to the frequency*", "*within 0.1" of the trace*" | 1–10 nF, ≤ 2,54 mm | FATO |
| **Ott**, Parte 6 (resumo) | Ordem de preferência: (1) uma camada só; (2) duas camadas adjacentes ao **mesmo** plano; (3) planos do mesmo tipo + vias "*wherever the signal changes planes*"; (4) planos de tipos diferentes + capacitores | — | FATO |
| **Bogatin**, Design007, fev./2021, dicas 5–7 | Via de retorno "*from the starting plane(s) to the final plane(s)*" dá "*the lowest crosstalk*", e isso "*is only possible if the return planes are the same voltage ... a strong motivation to only use ground planes as the return planes*". Com capacitor de bloqueio: "*can be as much as 5x higher impedance*", "*a poor approximation ... but the best we can do*" | capacitor ≤ 5× pior que via | FATO |
| **Toradex** Layout Design Guide §6.8 | Vias de GND na fonte **e** no destino. Em referência PWR: capacitor de costura "*between 10nF and 100nF*". Tabelas de USB/SD: 10 nF dos dois lados | 10–100 nF | FATO, `pdfs/04-emc/Toradex-Layout-Design-Guide.pdf` |
| **Fang, Hwang et al.**, IEEE EMC+SIPI 2023 (Missouri S&T + Tesla) | Com plano fendido, 3 vias de GND espalhadas ao longo da fenda a λ/37,5 (λ = 150 mm em 2 GHz, portanto ~4 mm) suprimiram a irradiação em **22 dB**, 9 dB mais que 3 vias coladas à via de sinal e 2 dB mais que 6 vias coladas | λ₀/37,5 | FATO. Atenção: o caso é fenda em 6 camadas, **não** generalizar para "espalhar é melhor que colar" |
| **Weir**, IPBLOX/IEEE SCV 2012 | Capacitor 0402 de costura: "*500pH + 20pH / mil to cavity center → 1.0 - 1.2nH to cavity in center of 0.062" PCB*". Um capacitor por transição reduziu o ruído na vítima em **38 %**, "*limited due to capacitor mounted inductance*". "*The easiest mitigation ... is to only traverse cavities with dense stitching vias*" | 1,0–1,2 nH; −38 % | FATO (texto lido; PDF não guardado) |
| **Chang Fei Yee** (Keysight), Design007, jun./2019 | Estudo de crosstalk com "*A stitching via is placed 20 mil off each signal via*" (geometria do estudo, não regra) | 0,5 mm | FATO-sec, https://iconnect007.com/article/117815/stitching-capacitor-crosstalk-mitigation-for-return-path-discontinuity/117818/pcb |
| **Hubing**, LearnEMC | "*Radiation is NOT proportional to loop area*" e "*Don't allow your most critical nets to make too many layer transitions*" | — | FATO, https://learnemc.com/the-most-important-emc-design-guidelines e https://learnemc.com/other-good-emc-design-guidelines |
| **kicad-happy RP-001** | "*Signal via transitions layers without a ground stitching via within max(2 × dielectric_height, 1.0 mm)*". O código usa a **primeira** camada core/prepreg do stackup (`_stitch_radius_mm`, padrão h = 0,2 mm). Cita "*Ott, PCB Stack-Up Part 6; Sierra Circuits*" | max(2h, 1 mm) | FATO (código, commit 6b9767e, `skills/emc/references/pcb-emc-rules.md` e `skills/emc/scripts/emc_rules.py`), https://github.com/aklofas/kicad-happy |
| **Bogatin**, SIJ "Rule of Thumb" sobre distância de via de retorno | — | — | **não encontrado** (as 33 colunas do índice não têm uma sobre vias: https://www.colorado.edu/faculty/bogatin/rules-thumb) |
| Ritchey, Johnson, Hartley, Beeker, Armstrong: número para distância de via de retorno | — | — | **não encontrado.** Beeker (NXP AMF-AUT-T3395, 2018) diz só: "*Signal traces must be one dielectric away from the return!*" (FATO) |
| Intel, AMD-Xilinx, Microchip: guias com distância de via de retorno | — | — | **não encontrado** nesta rodada; só blogs secundários (0,5 mm, 30–40 mil, 50–100 mil, 2–3 diâmetros), que não usei |

**Como as regras se encaixam (INFERÊNCIA):**

- **"≤ 2h ou 1 mm" (kicad-happy).**
  - Como está no código, vira **1 mm fixo** em qualquer 4 camadas da JLC e **3,2 mm** em 2 camadas (2 × 1,6 mm).
  - Como alvo para borda rápida, 1 mm é bom: dá ≈ 0,8 nH no 7628, e é praticamente o mínimo que o DRC da JLC permite, com via 0,3/0,6 mm e folga de 0,127 mm, ≈ 0,73 mm entre centros.
  - Como **limite de erro** para todo sinal, é rígido demais e não tem base primária.
  - O "h" está errado para a física da troca de referência: deveria ser a cavidade atravessada (núcleo), não o prepreg.
- **"≤ 200 mil / 5 mm" (TI).**
  - É um **teto**, dito com "*closer is better*".
  - Bate com Archambeault (5 × núcleo da JLC = 5,3–6,3 mm).
  - Vale como limite de projeto para qualquer sinal. Como alvo, é frouxo para tr ≤ 1 ns.
- **"O mais perto possível" e "λ/20".**
  - "O mais perto possível" é o que Ott, Archambeault, TI e Bogatin dizem em palavras.
  - λ/20 é critério de **espaçamento de cerca de costura**, não de distância via-a-via na transição. Mesmo assim, λg/20 na frequência máxima (2,9 mm a 2,45 GHz) é um teto razoável para RF.
- **"Uma via por via de sinal" contra "via compartilhada pelo grupo".**
  - A tabela de ruído de terra (§1.1.7) mostra que compartilhar é aceitável para tr ≥ 2 ns e N ≤ 4, e ruim para tr ≤ 1 ns.
  - A TI pede vias "*symmetrically*" para o par diferencial, ou seja, 1 ou 2 por par, e não uma por fio.

### 1.3 Quando a via de retorno NÃO é necessária (ou não resolve)

1. **O sinal referencia as duas faces do mesmo plano.** Ott: "*when a signal passes through a via and continues on the opposite side of the same plane a return current discontinuity does not exist*", porque o retorno passa pela parede do antipad. (FATO, Ott Parte 6)
   - Exemplo: em 6 camadas, L1 (referência L2, face de cima) → L3 (referência L2, face de baixo).
   - Na JLC de 4 camadas padrão isso **não** acontece na troca L1↔L4, porque L1 referencia L2 e L4 referencia L3.
2. **As duas referências são o mesmo net (GND–GND) com cavidade fina e costura densa.** A via adjacente continua sendo a melhor solução, mas a exigência cai.
   - Weir: "*Thin cavities exhibit low HF impedance*" (FATO).
   - Bogatin recomenda dielétrico fino entre planos (FATO).
   - Na prática, para sinal lento (tr ≥ 3 ns), uma via de costura de GND já existente a ≤ 5 mm basta (INFERÊNCIA).
3. **GND↔PWR (por exemplo SIG/GND/PWR/SIG, de L1 para L4).** Uma via de GND **não liga** os dois planos de referência. O que serve é um **capacitor de costura** (Ott, Toradex, TI, Bogatin; FATO).
   - **Valor:** 10–100 nF (Toradex). Ott usa 1–10 nF em fendas. A TI pede ≤ 1 µF.
     - Acima da autorressonância, o valor quase não importa; quem manda é a indutância de montagem.
     - Autorressonância (INFERÊNCIA): 10 nF com 1,1 nH → 48 MHz; 100 nF com 1,1 nH → 15 MHz; 10 nF com 5 nH → 22 MHz.
     - Ou seja, **em toda a banda de interesse de um sinal rápido o capacitor é um indutor de 1–10 nH.**
   - **Indutância:**
     - Ott: 5–10 nH típicos.
     - Weir: 1,0–1,2 nH para 0402 bem montado em placa de 1,6 mm.
     - Bogatin: até 5× a de uma via.
     - Use **0402 ou menor**, com via de cada pad colada ao pad.
   - **Distância:** "*adjacent to the signal via*" (Ott). O único número de Ott é 0,1" (2,54 mm), e é para fenda. Adotar ≤ 2,5 mm (INFERÊNCIA a partir de Ott).
   - **Limite:** pela tabela do §1.1.6, um capacitor de 5 nH dá 16 Ω a 500 MHz. Para tr ≤ 1 ns (USB HS, clocks), **não trocar de GND para PWR: rerotear** na camada sobre GND ou usar SIG/GND/GND/SIG (INFERÊNCIA, em linha com a ordem de preferência de Ott).
   - Se fonte e destino usam o mesmo trilho, o desacoplamento perto do ponto de entrada e saída pode servir de capacitor de costura (Toradex, FATO).

### 1.4 Tabela de decisão (INFERÊNCIA, montada com as fontes acima)

Classifique pelo **tempo de subida real do driver**, não pela taxa de dados. Um GPIO de MCU comutando a 1 MHz pode ter borda de ~1–3 ns; a própria SZZA009 diz que "velocidade" inclui "*harmonic content*" (FATO).

**Por borda ou frequência** (referências GND→GND):

| Classe | Exemplos | Distância via de sinal → via de GND (centro a centro) | Vias de retorno | Observação |
|---|---|---|---|---|
| tr ≥ 3 ns, f < 50 MHz | GPIO, I²C, UART, SPI lento, PWM | **≤ 5 mm** (teto TI/Archambeault). Via de costura existente serve | Pode compartilhar 1 via entre até ~4 sinais se ≤ 2 mm | Ruído de terra ≤ ~3 % (tabela §1.1.7) |
| tr ≈ 0,5–1,5 ns | USB 2.0 HS (480 Mb/s; tr mínimo de 500 ps visto só em trecho de busca do datasheet TI TUSB1210, **não verificado**), SPI/SDIO/QSPI 25–100 MHz, clocks de cristal com buffer | **alvo ≤ 1 mm** (colada), **máx. 2 mm**; erro acima de 5 mm | 1 por sinal simples; **1–2 simétricas por par diferencial** (TI) | Minimizar o número de trocas (Hubing). Vias em ambos os fios do par |
| tr ≈ 50–200 ps (1–5 GHz digital) | USB 3.x, PCIe, HDMI, MIPI | **o mais perto que o DRC permitir** (~0,7–1 mm) | **≥ 2 por par**, simétricas | Também stub, antipad e backdrill, fora do escopo |
| RF 2,4 / 5,8 GHz | Trilha de 50 Ω até a antena | Evitar trocar de camada. Se trocar: anel "coaxial" de **3–4 vias de GND** a ≤ 1 mm (TI SCAA082: "*similar structure to a coaxial line*") | 3–4 | Teto absoluto λg/20 (2,9 / 1,2 mm). Cercas a ≤ λg/20 (ver λ/20) |

**Por stackup:**

| Stackup | Cavidade que o retorno atravessa na troca L1↔Ln | Teto (5 × d, Archambeault) | L a 1 mm / 5 mm | O que fazer |
|---|---|---|---|---|
| 2 camadas, 1,6 mm | Pour de cima ↔ pour de baixo (1,6 mm) | 8 mm, mas usar 5 mm (TI) | 1,20 / 2,24 nH | Via de GND colada em toda troca de sinal rápido. Pours dos dois lados costurados. O kicad-happy usa raio de 3,2 mm aqui |
| 4 camadas SIG/GND/GND/SIG, JLC04161H-7628 (prepreg 0,21 mm) | Núcleo L2–L3 de 1,065 mm | 5,3 mm | 0,80 / 1,49 nH | Alvo ≤ 1 mm para borda rápida, teto 5 mm |
| 4 camadas SIG/GND/GND/SIG, JLC04161H-3313 (prepreg 0,099 mm) | Núcleo L2–L3 de 1,265 mm | 6,3 mm | 0,95 / 1,77 nH | Igual. A troca é ~18 % mais indutiva que no 7628 |
| 4 camadas SIG/GND/PWR/SIG (7628 ou 3313) | GND (L2) ↔ PWR (L3): **via de GND não resolve** | — | capacitor: 1–10 nH | Sinal rápido: **não trocar** (rotear em L1 sobre GND). Lento: capacitor de 10–100 nF, 0402, ≤ 2,5 mm, com via colada em cada pad |
| "0,1–0,2 mm de prepreg até L2" (qualquer) | O prepreg fino melhora o laço da **trilha** e o crosstalk (Ott: < 0,010") mas **não** muda a indutância da **troca**, que depende do núcleo | — | — | Não usar o h do prepreg para dimensionar a via de retorno |

### 1.5 Regra recomendada para a skill (Tópico 1)

1. **Toda via de sinal que troca de plano de referência GND→GND tem uma via de GND a ≤ 1 mm entre centros** (colada, o que o DRC permitir) quando o sinal tiver tr ≤ 1,5 ns: USB, clocks, SPI/SDIO/QSPI > 20 MHz, RF.
   - **Teto absoluto para qualquer sinal: 5 mm** (TI 200 mil; Archambeault 5 × núcleo).
   - Razão: as duas fontes primárias com número dão ≈ 5 mm como limite. A física mostra que perto de 1 mm se ganha ~2× em indutância, sem custo.
2. **Par diferencial:** 1 ou 2 vias de GND **simétricas** por par (TI). Vias nos dois fios.
3. **Sinal lento** (tr ≥ 3 ns): basta uma via de GND a ≤ 5 mm, e ela pode ser compartilhada por até 4 sinais se estiver a ≤ 2 mm de todos.
4. **GND↔PWR:** proibido para tr ≤ 1,5 ns. Para lentos: capacitor de 10–100 nF, 0402, ≤ 2,5 mm da via de sinal, com via de GND e via de PWR coladas aos pads.
5. **Não exigir** via quando o sinal passa para a outra face do **mesmo** plano (Ott).
6. **Dimensionar pela cavidade atravessada (núcleo), não pelo prepreg.** Num verificador: raio de erro = min(5 mm, 5 × h_cavidade); raio de aviso = 1 mm para redes rápidas.

---

## Tópico 2: número e posição dos pinos de GND em conectores e cabos

### 2.1 Física

1. **Crosstalk em conector é sobretudo indutivo, por retornos compartilhados.** Johnson: "*Crosstalk in most connectors results primarily from mutual inductance rather than parasitic capacitance*". Também: "*When several bus lines are forced to share power/ground pins, their current loops overlap*". Dar a cada sinal pinos próprios de alimentação e GND "*will reduce the intersignal coupling*". (FATO-sec, H. Johnson, "Mutual Understanding", EDN, jan./1998, https://www.sigcon.com/Pubs/edn/mutual_understanding.htm)
2. **Ruído de terra no conector:** 2 % por sinal por nH dividido por tr (ns) (Bogatin RoT #8, FATO-sec, ver §1.1.7).
   - Com N sinais por pino de GND, o ruído cresce **linearmente com N** e cai com tr mais lento (INFERÊNCIA a partir da fórmula).
   - Indutância por pino de header de 2,54 mm: **não encontrado** (o relatório Samtec não dá L).
3. **O cabo plano é uma linha de transmissão**, e a geometria dos GND define a impedância.
   - Em G S+ G S− G a impedância diferencial é exatamente 2Z. Em G S+ S− G ela fica abaixo de 2Z (~150 Ω para um cabo de 100 Ω de impedância de sinal simples).
   - S+ S− S+ S− sem GND: "*I don't recommend using that configuration for flat cables*", exceto em par trançado.
   - (FATO-sec, H. Johnson, "Ribbon Cable Impedance", https://sigcon.com/Pubs/news/3_10.htm)
4. **Capacitância mútua em cabo longo.** TI (C. Wells, 2013): dois sinais vizinhos em 3 pés de cabo plano tiveram "*over 50 pF*" entre si e corromperam dados. Com 2 fios de GND entre eles, "*around 10 pF*", e a comunicação funcionou. Valor típico: 10–50 pF/pé entre vizinhos. (FATO-sec, https://e2e.ti.com/blogs_/archives/b/precisionhub/posts/how-to-minimize-crosstalk-in-cable-designs)
5. **Irradiação de modo comum pelo cabo.**
   - SZZA009: "*Because usually there is only one ground wire between boards, that one inductive wire has to return all of the RF energy ... a portion of the RF energy does not return ... via the ground wire, but rather through a radiated path*". (FATO, `pdfs/04-emc/TI-SZZA009-PCB-design-reduced-EMI.pdf` §2.5)
   - Hubing (QOTW 16/11/2020):
     - Sair de microstrip para cabo plano com o retorno a 2 mm gera tensão de modo comum de ~metade do sinal.
     - Pôr um fio de retorno do outro lado do sinal reduz a tensão que excita o cabo em ~4–8 dB, mas fios de GND adicionais têm efeito decrescente.
     - Cabo com plano de retorno (flex de 2 camadas) produz muito pouco modo comum.
     - (FATO-sec, https://learnemc.com/qotw-201116)
   - LearnEMC lab 7: um segundo fio de retorno reduz o acoplamento por impedância comum em ~6 dB. (FATO-sec, https://www.learnemc.com/labs-07)

### 2.2 O que as fontes dizem (com citações)

**TI SZZA009, "PCB Design Guidelines For Reduced EMI", novembro de 1999, §2.5.3 "Number of Returns".** Texto completo (FATO, extraído do PDF):

> "It is common practice in the computer industry to have at least one ground for every nine other signal lines in a cable or harness. With higher speeds, this ratio is moving toward 1:5. These higher speeds are not limited to data rates, but also to harmonic content. Use these guidelines in designing signal and return lines:
> - The best practice is to have one ground return for each signal in the cable, as a twisted pair.
> - Never run less than one ground return for every nine signal lines, even if it is just the jumper cable to the front-panel display in a completely sealed metal box.
> - If the cable is over one foot long, it should have one ground return line for four signal lines.
> - When possible, there should be a solid metal bracket, used as a mechanical brace, soldered between the two boards, to serve as a mounting bracket and as a robust RF ground return."

- **Contexto:**
  - O texto fala de **cabos e chicotes entre placas** (§2.5 "Cables and Connectors"), escrito em 1999.
  - O §2.5.2 acrescenta: "*run clocking or other high-speed wires twisted with their own separate return. Crosstalk is a problem in cables over 2-meters long, and can be a problem in cables as short as 6 inches*" (FATO).
- **Leitura:** 1:9 é o **mínimo absoluto**, mesmo num jumper curto dentro de caixa metálica fechada. Não é uma recomendação.
  - A recomendação muda conforme o caso: 1:4 acima de 30 cm, 1:5 em velocidades altas e 1:1 trançado como ideal.
  - (FATO na citação; INFERÊNCIA na leitura, que é direta)

| Fonte | O que diz | Etiqueta |
|---|---|---|
| **NXP AN10897** (guia ESD/EMC) §3.1.4.3 | "*Ground pins should be evenly distributed across all connectors (board-to-board or board-to-cable). The number of connector ground pins should be determined prior to layout and should include the current capabilities of the connector as well as the current carrying capability of the cables*". Também: "*A minimum of one ground-return track should be routed adjacent to each eight lines of address and data lines ... You can increase the ratio to 1 : 5 for higher performance*" | FATO, `pdfs/04-emc/nxp-an10897-esd-emc-guide.pdf` |
| **Samtec**, relatórios de caracterização | "*Electrical performance can vary significantly depending upon the number and location of ground pins. In general, the more pins dedicated to ground, the better electrical performance will be. However, dedicating pins to ground reduces signal density*". Define SE1:1 (GSGSG) e SE2:1 (GSSG) | FATO, `pdfs/12-via-gnd/Samtec-*.pdf` |
| **Samtec TSM/SSW**, header de 2,54 mm, 13,59 mm de altura acoplada (2011), Tabela 5 | NEXT de sinal simples: **GAQG** (agressor e vítima vizinhos) 19,56 / 18,51 / **16,25** / 10,86 / **6,29 %** para tr = 30 / 50 / 100 / 250 / 500 ps. **GAGQG** (GND entre eles) 2,51 / 2,10 / **1,77** / 1,31 / **0,77 %**. FEXT GAQG 11,92 → 2,80 %; GAGQG 3,50 → 0,55 % | FATO, `pdfs/12-via-gnd/Samtec-time-data-summary_tsm-01_ssw-22_web.pdf` |
| **Samtec TSM/SSW**, Tabela 6 | NEXT diferencial: **GAAQQG** 6,27 → 2,05 %; **GAAGQQG** 0,55 → 0,12 % (30 → 500 ps) | FATO |
| **Samtec TSM/SSW**, velocidade | "*Single-Ended: 5.5GHz/ 11Gbps; Differential: 8.5GHz/ 17Gbps*" (ponto de −3 dB) | FATO |
| **Samtec** (caracterização) | O laboratório usa GSG/GSSG, mas um sistema real pode ter "*SSSS, or four adjacent single ended signals*". "*in most applications, performance can safely be considered equivalent*" | FATO |
| **Beeker** (NXP, 2018) | "*Signal traces must be one dielectric away from the return! Adjacent to planar copper; Adjacent to ground trace*". Fala de "*'Smart' connector pinout*" sem dar razão | FATO (PDF lido) |
| **kicad-happy IO-002** | "*Ground pins < max(2, signal_pins / 4) for connectors with >2 signal pins*". No código: "*Rule of thumb: at least 1 ground pin per 4 signal pins*". Severidade warning em USB, HDMI, Ethernet, PCIe, SATA e LVDS; info no resto. **Sem fonte citada** | FATO (código) |
| **Ott**, *EMC Engineering* §2.16 "Ribbon Cables" | Existe no livro (sumário), mas o texto não está livre | **não encontrado** (texto) |
| Hartley, Ritchey, Armstrong: razão S:G | — | **não encontrado** |

**Normas que prescrevem a posição dos GND** (FATO-sec: pinagens lidas na Wikipedia; as especificações normativas da SATA-IO, PCI-SIG e USB-IF não foram lidas):
- **SATA**, conector de dados de 7 pinos: G A+ A− G B− B+ G. Os GND são mais longos e acoplam primeiro. (https://en.wikipedia.org/wiki/SATA)
- **PCIe** (borda de cartão): REFCLK e cada par HSO/HSI ficam entre pinos de GND (por exemplo A12 GND, A13/A14 REFCLK±, A15 GND, A16/A17 HSI±, A18 GND), padrão GSSG. (https://en.wikipedia.org/wiki/PCI_Express)
- **USB-C:** A1 GND, A2/A3 TX1±, …, A10/A11 RX2±, A12 GND. Os pares SuperSpeed ficam entre GND e VBUS. (https://en.wikipedia.org/wiki/USB-C)
  - INFERÊNCIA: o VBUS, desacoplado, faz papel de retorno AC, e a blindagem completa o retorno.
- **PATA de 80 vias** (UDMA/66 em diante): 40 pinos e 80 fios, com GND entre todos os sinais, "*to reduce the effects of capacitive coupling*". Obrigatório em UDMA4/5/6. Cabo de até 18" (460 mm). (FATO-sec, https://en.wikipedia.org/wiki/Parallel_ATA)
  - INFERÊNCIA: é um exemplo de IDC 1:1 imposto por norma.

### 2.3 O que muda com borda, tipo de conector e comprimento

1. **Borda (tr).**
   - Os números Samtec caem quase 3× de 100 para 500 ps (GAQG 16 % → 6 %) (FATO).
   - Para tr de 2–5 ns, o NEXT em header de 2,54 mm sem GND entre sinais deve cair para ~1–2 % (INFERÊNCIA, extrapolação ~1/tr de um conector curto, atraso de 122 ps, FATO na Tabela 7; **não medido**).
   - Por isso GPIO lento tolera SSSS. Clock e borda < 1 ns não toleram.
2. **Tipo de conector** (INFERÊNCIA, com base nos dados acima):
   - **Header de 2,54 mm:** pino longo, sem blindagem. O GND vizinho é o que mais pesa (8–9× no NEXT).
   - **IDC / cabo plano:** o comprimento domina e o cabo vira linha de transmissão. Usar G S G S (1:1) para coisas rápidas (exemplo PATA-80).
   - **FPC:** se tiver plano de GND numa camada, o retorno fica sob todos os sinais e quase não há modo comum (Hubing, FATO-sec). Sem plano, tratar como cabo plano.
   - **Mezanino placa-placa:** seguir a pinagem que o fabricante caracterizou (Samtec SE1:1/SE2:1). Colocar GND nas pontas das fileiras.
   - **Card edge:** seguir a norma (GSSG).
3. **Comprimento.**
   - SZZA009: > 1 pé → 1:4 (FATO). Crosstalk "*can be a problem in cables as short as 6 inches*" e "*is a problem in cables over 2-meters*" (FATO).
   - TI E2E: 3 pés sem GND entre sinais = 50 pF e falha; com 2 GND entre eles, ~10 pF e OK (FATO-sec).

### 2.4 Recomendações práticas por caso (INFERÊNCIA, salvo indicação)

| Caso | Razão S:G | Posição | Observação |
|---|---|---|---|
| GPIO lento, I²C, UART (cabo ≤ 30 cm) | **≥ 1:4** (piso 1:9 da SZZA009 só como erro duro) | GND distribuído; pelo menos 1 em cada ponta do conector | I²C: SDA/SCL vizinhos de GND reduzem crosstalk SCL→SDA. Pull-ups e capacitância do cabo limitam o comprimento |
| Os mesmos, cabo > 30 cm | **1:4** (SZZA009, FATO) | Idem | Considerar par trançado com o GND |
| SPI 10–50 MHz | **2:1** no mínimo; **SCK com GND dos dois lados** (G SCK G) | MOSI/MISO/CS podem dividir um GND | SZZA009: clock "*with their own separate return*" (FATO). Resistor série na saída |
| SDIO / QSPI 50–100+ MHz | **1:1 a 2:1**, CLK isolado por GND | Cabo curto (≲ 10 cm) ou FPC com plano | Acima disso, preferir FPC com plano de GND (Hubing) |
| USB 2.0 / LVDS (diferencial) | **GSSG** (1 GND por par, no mínimo; ideal G entre pares) | D+/D− vizinhos, GND dos dois lados | Samtec: GND entre pares derruba o NEXT diferencial ~11–17× (FATO). Em cabo, par trançado blindado |
| Cabo plano / IDC | **1:1** (G S G S) para borda rápida ou cabo > 30 cm; **≥ 1:4** para lento e curto | Alternar | PATA-80 como precedente (FATO-sec) |
| Pinos de alimentação | GND ≥ número de pinos de alimentação que conduzem corrente, cada pino abaixo da corrente nominal derateada | Alimentação e GND vizinhos (laço pequeno) | NXP: contar GND pela corrente (FATO). Correntes por contato em `05-componentes-conexoes.md` (JST SH/GH 1 A, PH 2 A, XH 3 A; DF40 0,3 A). Esses GND **não** contam como retorno de sinal rápido se estiverem longe dos sinais |

### 2.5 Regra recomendada para a skill (Tópico 2)

1. **Erro:** menos de 1 GND para cada 9 sinais em qualquer conector ou cabo (piso da SZZA009).
2. **Aviso:** menos de max(2, ⌈S/4⌉) GND. É o 1:4 da SZZA009 para cabo > 30 cm, o mesmo limiar do kicad-happy IO-002. Vale como padrão porque raramente se sabe o comprimento do cabo na revisão do layout.
3. **Posição (mais importante que a contagem):** todo clock e todo sinal com tr ≤ 1,5 ns tem um pino de GND **vizinho**. Pares diferenciais em **GSSG**. Pelo menos um GND em cada extremidade do conector.
4. **Cabo plano rápido ou longo:** 1:1 alternado.
5. **Corrente:** os GND também levam o retorno da alimentação. Somar a corrente e respeitar a nominal por pino.

---

## λ/20: conta e qual εr usar

λ₀ = c/f, λg = λ₀/√ε (INFERÊNCIA, conta):

| f | λ₀ (ar) | λ₀/20 | λg/20 com εeff 3,3 (microstrip externa) | λg/20 com εr 4,1 (3313) | **λg/20 com εr 4,4** (7628, stripline, FR-4 em volume) |
|---|---|---|---|---|---|
| 480 MHz (USB HS, fundamental) | 624,6 mm | 31,2 mm | 17,2 mm | 15,4 mm | 14,9 mm |
| 1 GHz | 299,8 mm | 15,0 mm | 8,25 mm | 7,40 mm | 7,15 mm |
| **2,45 GHz** | 122,4 mm | 6,12 mm | **3,37 mm** | 3,02 mm | **2,92 mm** |
| 5,0 GHz | 60,0 mm | 3,00 mm | 1,65 mm | 1,48 mm | 1,43 mm |
| **5,8 GHz** | 51,7 mm | 2,58 mm | 1,42 mm | 1,28 mm | **1,23 mm** |

**Qual εr aplicar (INFERÊNCIA):**
- **Cerca de vias ao lado da CPWG ou microstrip e costura de borda entre planos:** a onda que essas vias precisam bloquear é a **de placas paralelas** entre o cobre de cima e L2, ou entre L2 e L3. Ela se propaga **inteira dentro do dielétrico**. Use **εr em volume (4,4 no 7628; 4,1 no 3313)**: **2,9 mm a 2,45 GHz** e **1,2 mm a 5,8 GHz**.
- **εeff ≈ 3,3** descreve só a onda guiada **na trilha** externa, com parte do campo no ar. Serve para comprimento elétrico de linha, não para passo de cerca.
- **Cruzamento com fonte primária:** Fang/Hwang obtiveram o ótimo em λ/37,5 com λ = 150 mm a 2 GHz, ou seja, λ no **ar**, ≈ 4 mm. Em εr 4,3 (o do artigo) isso dá λg = 72 mm, e 4 mm ≈ **λg/18**. É coerente com "λg/20 no dielétrico". O caso é específico (fenda em 6 camadas). (FATO no número do artigo; INFERÊNCIA na conversão)
- **Fonte primária de fabricante para "λ/20":** não encontrado. Só fontes secundárias (blogs de fabricantes de placa e fórum SI-list), que dão ~3 mm a 2,4 GHz e chamam a regra de conservadora.

---

## Conflitos com as regras atuais da skill

| # | Regra atual da skill ou do repositório | O que as fontes dizem | Veredito |
|---|---|---|---|
| C1 | "via de GND ≤ 5 mm de cada troca de camada" | TI: ≤ 200 mil, "*closer is better*" (FATO). Archambeault: ≤ 5 × distância entre planos (FATO). Ott/Bogatin: "*immediately adjacent*" (FATO) | **Manter 5 mm como teto** e **acrescentar alvo ≤ 1 mm para redes rápidas** (tr ≤ 1,5 ns), 1–2 vias simétricas por par diferencial, e as exceções: GND↔PWR exige capacitor (ou proibir para redes rápidas); mesmo plano nas duas faces não exige via |
| C2 | "1 GND para cada 9 sinais" (atribuída à SZZA009) | SZZA009 §2.5.3: 1:9 é o **mínimo absoluto**; 1:4 para cabo > 1 pé; 1:5 em velocidades altas; 1:1 trançado é o ideal (FATO) | **Leitura errada da fonte. Substituir:** erro < 1:9, aviso < 1:4, mais a regra de posição (GND vizinho de clock e rápidos, GSSG) |
| C3 | `04-gnd-si-emc-stackup.md` linha 242: "pelo menos um retorno de GND para cada 9 sinais ('prática comum na indústria de computadores')" | A mesma frase da SZZA009 continua com 1:5, 1:4 (> 1 pé) e 1:1 | **Corrigir o tema 04** para citar os quatro níveis |
| C4 | `03-rf-antenas.md`: λ/20 ≈ 3,4 mm a 2,45 GHz (εeff 3,3). `04-gnd-si-emc-stackup.md`: ≈ 2,9 mm (FR-4) | As duas contas estão certas, mas com ε diferentes | **Unificar em εr do dielétrico: 2,9 mm a 2,45 GHz, 1,2 mm a 5,8 GHz** para cercas e costura de borda (seção λ/20) |
| C5 | kicad-happy RP-001: max(2h, 1 mm), atribuído a "Ott Parte 6" | Ott Parte 6 não tem número (FATO). O h do código é o da primeira camada dielétrica (FATO no código) | Se a skill reaproveitar o RP-001: tratar 1 mm como **alvo/aviso**, não erro. Dimensionar o teto pela cavidade (núcleo) |
| C6 | kicad-happy IO-002: 1:4, sem fonte | Coincide com a cláusula "> 1 pé" da SZZA009 (FATO) | Compatível com a regra recomendada. Acrescentar a regra de posição, que o IO-002 não verifica |
| C7 | `04-gnd-si-emc-stackup.md` linha 302: "Via GND–GND a ≤5 mm, idealmente a ≤1 mm" | Coerente com este estudo | **Confirma** |
| C8 | Suposição implícita de que o 3313 é melhor em tudo que o 7628 | Na troca L1↔L4 em SIG/GND/GND/SIG o núcleo do 3313 é mais grosso, e a via de retorno é ~18 % mais indutiva (INFERÊNCIA) | Registrar a nuance. Não muda a escolha do stackup |

---

## Bibliografia

**Primárias lidas (FATO):**
- TI **SZZA009**, *PCB Design Guidelines For Reduced EMI*, nov./1999, §2.5. https://www.ti.com/lit/an/szza009/szza009.pdf (local: `pdfs/04-emc/TI-SZZA009-PCB-design-reduced-EMI.pdf`)
- TI **SLLA414A**, *High-Speed Layout Guidelines for Signal Conditioners and USB Hubs*, ago./2025, rev. jan./2026, §3. https://www.ti.com/lit/an/slla414/slla414.pdf (local: `pdfs/04-emc/`)
- TI **SPRAAR7J**, *High-Speed Interface Layout Guidelines*, rev. fev./2023, §2, fig. 2-11. https://www.ti.com/lit/an/spraar7/spraar7.pdf (local: `pdfs/04-emc/`)
- TI **SCAA082A**, *High-Speed Layout Guidelines*, rev. ago./2017. https://www.ti.com/lit/an/scaa082a/scaa082a.pdf (local: `pdfs/04-emc/`)
- **Toradex**, *Layout Design Guide*, §6.8 e tabelas 8 e 15 (local: `pdfs/04-emc/Toradex-Layout-Design-Guide.pdf`)
- **NXP AN10897**, guia ESD/EMC, §3.1.4.3 (local: `pdfs/04-emc/nxp-an10897-esd-emc-guide.pdf`)
- B. **Archambeault**, "Design Tid-Bit", *IEEE EMC Society Newsletter*, outono/2007, pp. 102–103. https://ewh.ieee.org/soc/emcs/acstrial/newsletters/fall07/pg102-103.pdf (local: `pdfs/12-via-gnd/`)
- X. **Fang**, C. **Hwang**, M. Liu, R. R. Navarrete, "Analysis of EMI Problems Caused by Split Reference Plane on High-Speed Multilayer Boards", IEEE EMC+SIPI 2023, DOI 10.1109/EMCSIPI50001.2023.10241478. https://par.nsf.gov/servlets/purl/10465871 (local: `pdfs/12-via-gnd/nsf-par-10465871.pdf`)
- H. **Ott**, *PCB Stack-Up Part 6: Return Path Discontinuities* (snapshot de 2012). https://web.archive.org/web/2012/http://www.hottconsultants.com/techtips/pcb-stack-up-6.html
- E. **Bogatin**, "Seven Tips for Your Next Stackup Design", Design007/I-Connect007, fev./2021. https://iconnect007.com/article/126202/seven-tips-for-your-next-stackup-design/126205/pcb
- S. **Weir** (IPBLOX), "How Bad is Bad? Cavity Signal Injection and Mitigation", IEEE SCV EMC, fev./2012. https://ewh.ieee.org/r6/scv/emc/archive/022012SteveWeir.pdf (não guardado: aviso de direitos)
- **Clemson CVEL** (T. Hubing), EMC FAQ, PCB Design Q7. https://cecas.clemson.edu/cvel/emc/FAQ/question-pcbdes07.html
- **LearnEMC** (T. Hubing), *The Most Important EMC Design Guidelines* e *Other Good EMC Design Guidelines*. https://learnemc.com/the-most-important-emc-design-guidelines · https://learnemc.com/other-good-emc-design-guidelines
- **Samtec**, *High Speed Characterization Report* TSM/SSW (2,54 mm, 13,59 mm), rev. 26/08/2011. https://suddendocs.samtec.com/testreports/hsc-report_tsm-01_ssw-22_web.pdf · https://suddendocs.samtec.com/testreports/time-data-summary_tsm-01_ssw-22_web.pdf
- **Samtec**, DPAM/DPAF Characterization Details (definições SE1:1 e SE2:1). https://suddendocs.samtec.com/testreports/characterization-details_dpam-dpaf-10mm_web.pdf
- D. **Beeker** (NXP), *Effective Printed Circuit Board Design*, AMF-AUT-T3395, out./2018. https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/tech-days/358/1/AMF-AUT-T3395.pdf
- **kicad-happy** (aklofas), commit 6b9767e: `skills/emc/references/pcb-emc-rules.md` (RP-001, IO-002) e `skills/emc/scripts/emc_rules.py` (`_stitch_radius_mm`, `check_layer_transition_stitching`, IO-002). https://github.com/aklofas/kicad-happy
- **JLCPCB**, stackups de impedância (JLC04161H-7628 e -3313). https://jlcpcb.com/impedance (dados já conferidos em `04-gnd-si-emc-stackup.md`)

**Lidas por resumo (FATO-sec):**
- E. Bogatin, Rule of Thumb #1 (banda × tr). https://www.edn.com/electronics-blogs/bogatin-s-rules-of-thumb/4424573/rule-of-thumb--1--the-bandwidth-of-a-signal-from-its-rise-time
- E. Bogatin, Rule of Thumb #8 (ruído de terra em conector). https://www.edn.com/electronics-blogs/all-aboard-/4429476/how-to-estimate-ground-bounce-in-a-connector--rule-of-thumb--8
- E. Bogatin, Rule of Thumb #16 (indutância de folha da cavidade: 32 pH por mil de dielétrico). https://www.edn.com/electronics-blogs/all-aboard-/4434907/sheet-inductance-of-a-cavity--rule-of-thumb--16
- E. Bogatin, índice das Rules of Thumb. https://www.colorado.edu/faculty/bogatin/rules-thumb
- H. Johnson, "Mutual Understanding", EDN, jan./1998. https://www.sigcon.com/Pubs/edn/mutual_understanding.htm
- H. Johnson, "Ribbon Cable Impedance". https://sigcon.com/Pubs/news/3_10.htm
- C. Wells (TI), "How to minimize crosstalk in cable designs", dez./2013. https://e2e.ti.com/blogs_/archives/b/precisionhub/posts/how-to-minimize-crosstalk-in-cable-designs
- T. Hubing, LearnEMC QOTW 16/11/2020. https://learnemc.com/qotw-201116 · LearnEMC lab 7 (impedância comum em cabo plano). https://www.learnemc.com/labs-07
- C. F. Yee (Keysight), "Stitching Capacitor Crosstalk Mitigation for Return Path Discontinuity", Design007, jun./2019. https://iconnect007.com/article/117815/stitching-capacitor-crosstalk-mitigation-for-return-path-discontinuity/117818/pcb
- Pinagens (secundárias): SATA https://en.wikipedia.org/wiki/SATA · PCIe https://en.wikipedia.org/wiki/PCI_Express · USB-C https://en.wikipedia.org/wiki/USB-C · PATA https://en.wikipedia.org/wiki/Parallel_ATA

**Procuradas e não encontradas (nesta rodada):**
- Coluna de Bogatin (SIJ ou EDN) com número para a distância da via de retorno.
- Artigo de Johnson sobre "return-current via".
- Números de Ritchey, Hartley, Armstrong e Beeker para a distância de via ou para a razão S:G.
- Guias Intel, AMD-Xilinx e Microchip com distância de via de retorno.
- Texto de Ott §2.16 (cabo plano).
- Textos normativos USB-IF, PCI-SIG, SATA-IO e JEDEC.
- Indutância por pino de header de 2,54 mm.
- Valor normativo de tr/tf do USB 2.0 HS (500 ps, 10–90 %): visto só em trecho de busca do datasheet TI TUSB1210 (https://ti.com/document-viewer/TUSB1210-Q1/datasheet/specifications); **não verificado**.
- Fonte primária de fabricante para "λ/20".
