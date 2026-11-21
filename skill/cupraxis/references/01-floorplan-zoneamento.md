# 01 — Floorplan, zoneamento e placement (posicionamento de componentes)

> Pesquisa de 2026-11-20 para a futura skill "especialista em PCB" (KiCad 10, JLCPCB; vale para qualquer PCB — produtos autônomos, RF/IoT, energia, periféricos, placas que encaixam em host).
> **Etiquetas:** **[FATO]** = conferido na fonte primária lida (PDF/página aberta nesta pesquisa). **[INFERÊNCIA — fonte secundária]** = número visto só em resumo de busca, fórum ou blog de terceiro, sem abrir a fonte primária; usar com cautela. **[INFERÊNCIA]** = dedução minha ou prática comum sem fonte primária.
> PDFs baixados: `pdfs\01-floorplan\` (licenças em `pdfs\01-floorplan\LICENSES.md`).

---

## Resumo executivo

1. **Placement antes de rotear**, na ordem: mecânica fixa (conectores, furos, antenas) → críticos (RF, cristal, laço quente da SMPS) → CIs → passivos de suporte nos pinos → resto (Altium, JLCPCB, Sierra).
2. **Zoneamento por função e fluxo:** entrada de energia → regulador → MCU → lento → analógico mais longe. RF na borda da antena. Ruidoso longe do sensível (TI SZZA009 §2.3).
3. **Um plano de GND só, particionado e sem cortes.** A separação vem do placement e de rotear com disciplina (TI SLYT512, Ott).
4. **Proximidade:** Cin e FET/diodo da SMPS "acap", sem via. Desacoplamento no pino. Ferrite no +V, do lado do ruído. TVS colado ao conector. Terminação série no driver e paralela no receptor.
5. **Cristal:** perto do pino, conforme o datasheet (Microchip ≤ 12 mm; ESP32-C5 chip-down ≥ 2,4 mm). Nada por baixo; indutores longe.
6. **JLCPCB:** corpo a ≥ 2,5 mm da borda; rails de 5 mm (obrigatórios no Standard); 3 fiduciais de 1 mm (máscara de 2 mm, ≥ 3,35 mm da borda); tooling holes de 1,152 mm.
7. **Espaçamento JLC entre encapsulamentos:** QFN↔qualquer 1,0 mm, QFP 1,25 mm, BGA 2,0 mm, chips 0,15–0,35 mm. Courtyard OK não basta.
8. **PCBA:** Economic só monta 1 lado (≥ 0402). Standard monta 2 lados, mas exige placa ≥ 70×70 mm (senão, painel ou rails).
9. **Térmico:** cerca de 15 cm²/W (2 lados, ar parado, ΔT 40 °C); vias a 1 mm sob o EP; plano sem cortes; sensíveis (eletrolítico, cristal, GNSS) longe do calor (TI SNVA419).
10. **Mecânica:** MLCC a ≥ 5 mm de V-cut ou borda, ou paralelo a ela (Vishay, Murata).
11. **Compactar** com 0402/0201, os dois lados, via-in-pad (automático na JLC a partir de 6 camadas) e módulos. **Não compactar** sem canais de roteamento, com calor concentrado ou onde se precisa de retrabalho e test points.
12. **DFT:** 1 ponto sondável por net crítica; pad de 0,5 mm; folga de 0,29 × h + 0,7 mm das peças altas (Sierra/SEICA).
13. **Principais conflitos com a casa:** conector flush × 2,5 mm de borda; placa pequena (< 70×70 mm, ex. `[FLIPPER]`: módulo externo de 67,34 mm) × mínimo do PCBA Standard; `spread.py` com GAP de 0,6 mm × tabela JLC; "hub elimina test pads" × DFT; faltam fiduciais e tooling holes.

---

## Regras acionáveis

### A. Ordem de placement (fluxo de trabalho)

1. **Importar o contorno (Edge.Cuts) e a mecânica oficial antes de tudo.** Depois vêm os itens de posição obrigatória: conectores, furos, chaves, displays, antenas. Travar (lock) essas peças. **Por quê:** a posição deles é ditada pelo sistema (carcaça, host) e eles condicionam todo o resto. **[FATO]** Altium ("Component locations for connectors must be exact"): https://resources.altium.com/p/where-do-they-all-go-pcb-layout-component-placement-guidelines · JLCPCB (passo 1: "connectors, mounting holes, displays, buttons, and antennas"): https://jlcpcb.com/blog/pcb-component-placement-guide-2026
2. **Depois, a circuitaria principal pelo floorplan; em seguida, os passivos de suporte encostados no CI que servem; por último, os periféricos.** **[FATO]** Altium (mesma URL). JLCPCB (ordem: mecânicos → CIs-chave e de potência → passivos de suporte → LEDs, test points, jumpers → revisão de zoneamento antes de rotear): https://jlcpcb.com/blog/pcb-component-placement-guide-2026 · Sierra (conectores na borda → CIs principais → auxiliares como cristal e desacoplamento → passivos série, pull-up, ESD): https://www.protoexpress.com/blog/component-placement-guidelines-pcb-design-assembly/
3. **Na SMPS, a ordem interna é: primeiro o capacitor de bypass de entrada (C_BYPASS) e o diodo de roda-livre/FET low-side, os dois "acap"; só depois o resto.** **Por quê:** é o laço com di/dt em degrau. As outras peças "podem ser posicionadas relativamente sem cuidado". **[FATO]** TI SNVA054 (AN-1229) §4, `pdfs\01-floorplan\TI_SNVA054_AN-1229_Simple_Switcher_PCB_Layout.pdf`, https://www.ti.com/lit/pdf/snva054
4. **No esquemático, desenhar os passivos ao lado do pino em que vão ficar na placa.** Isso facilita o placement por cross-probing. **[INFERÊNCIA — fonte secundária]** (página vista só em resumo de busca) Fedevel tip 081: https://www.fedevel.com/blog/tip-081-place-components-in-the-schematic-close-to-the-pins-where-they-should-be-located-on-pcb
5. **Trazer os grupos lógicos do esquemático para fora da placa, perto da área final, e arrumar cada grupo antes de encaixá-lo.** **[FATO]** Altium (mesma URL da regra 1).
6. **Não encher a placa de passivos cedo: reservar primeiro os canais de roteamento dos sinais-chave.** **[FATO]** JLCPCB placement guide (URL da regra 1). Isso confirma o achado da casa (§15): o autorouter falhava por falta de canal entre os pads.

### B. Zoneamento funcional (onde cada zona fica)

7. **Agrupar por função** (energia, digital, analógico, RF, comunicação) e por mesmo par VCC/GND. Não misturar. **[FATO]** TI SZZA009 §2.3 "Board Zoning": "placing like functions on a board in the same general area, as opposed to mixing them together", `pdfs\01-floorplan\TI_SZZA009_PCB_Design_Guidelines_Reduced_EMI.pdf`, https://www.ti.com/lit/pdf/szza009 · Sierra (URL da regra 2).
8. **Gradiente de ruído:** a lógica de alta velocidade (MCU) fica perto da fonte, as peças mais lentas mais longe e o analógico mais longe ainda. **Por quê:** a lógica rápida tem menos chance de contaminar os outros traços. **[FATO]** TI SZZA009 §2.3.
9. **MCU ao lado do regulador, e regulador ao lado de onde a alimentação entra na placa**, com GND largo e contínuo ligando os três. **[FATO]** TI SZZA009 §2.3 ("Locate the microcomputer next to the voltage regulator, and the voltage regulator next to where VBatt enters the board"). Isso confirma a regra da casa §14 (energia no quadrante do USB-C).
10. **O laço do cristal (tank) fica longe de circuitos analógicos, sinais lentos e conectores.** Não deixar cabo ou flat dobrar por cima do MCU ou do oscilador depois de montado. **[FATO]** TI SZZA009 §2.3.
11. **Um único plano de GND, particionado em seções analógica e digital.** Cada sinal é roteado só na sua seção, em todas as camadas. Não cortar o plano. Se o corte for inevitável, fazer uma "ponte" única por onde passam todos os sinais. **[FATO]** TI SLYT512 (Grounding in mixed-signal systems demystified, Part 1), `pdfs\01-floorplan\TI_SLYT512_Grounding_Mixed_Signal_Demystified_Part1.pdf`, https://www.ti.com/lit/pdf/slyt512 · H. Ott, "Partitioning and layout of a mixed-signal PCB", Printed Circuit Design, jun/2001 (citado pela TI; o original não foi lido).
12. **A energia entra pela partição digital e alimenta o digital direto; o analógico recebe essa energia já filtrada ou regulada.** **[FATO]** TI SLYT512.
13. **Peças sensíveis de alta velocidade ficam longe da borda, mais para o centro. Não rotear sinal ruidoso ou de alta velocidade na beira da placa.** **[FATO]** Sierra (URL da regra 2). TI SZZA009 §2.4.1 ("Never run noisy traces on the outside edge of the board"). JLCPCB placement guide.
14. **Ruidosos (DC-DC, drivers de motor, osciladores) longe de sensíveis (entradas de ADC, sensores, referências, receptores RF).** **[FATO]** JLCPCB placement guide.
15. **RF:** o módulo ou chip de RF fica na borda. Antena de PCB do módulo **para fora da placa-base**, com o ponto de GND da antena junto da borda. **Não** centralizar o módulo com recorte nos 4 lados. Na carcaça, deixar **≥ 15 mm livres** em volta da antena. Antena longe de cristais, clocks, porta USB, conversor USB-serial e linhas UART (incluindo test points e headers). **[FATO]** Espressif ESP32-C5 Hardware Design Guidelines, seção "Positioning a Module on a Base Board" e "RF", `pdfs\01-floorplan\Espressif_ESP32-C5_Hardware_Design_Guidelines.pdf`, https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c5/pcb-layout-design.html
16. **Pico W:** recorte de antena de 14 × 9 mm. Qualquer coisa perto da antena reduz o desempenho. O módulo deve ficar **na borda** e não pode ser fechado em metal. **[FATO]** Raspberry Pi, *Hardware design with RP2040*, nota da seção do Pico W, `pdfs\01-floorplan\RaspberryPi_Hardware_Design_with_RP2040.pdf`, https://datasheets.raspberrypi.com/rp2040/hardware-design-with-rp2040.pdf
17. **Zona de conectores e IO numa borda, com a proteção (TVS e filtros) colada a eles.** Assim a corrente de ESD e a de modo comum dos cabos não atravessa a placa. **[FATO]** TI SLVA680 (ver regra 26).
18. **Interface humana (botões, LEDs, conectores de cabo) na borda acessível**, longe das antenas. **[INFERÊNCIA]**, combinando a regra da casa §5 com a Espressif (UART, headers e test points longe da antena).

**Floorplan genérico de referência (placa com RF + MCU + bateria + USB)** — **[INFERÊNCIA]** que sintetiza as regras 7–18 e as regras da casa §2/§3/§5/§14. Adaptar ao produto: sem RF, a borda superior vira IO/interface; sem bateria, a zona de energia encolhe para entrada + regulador; em placa que encaixa num host (HAT, shield, módulo de expansão), a borda de encaixe segue o gabarito oficial:

```
 ┌──────────────── borda das antenas (SMA edge-mount, ~18 mm entre centros) ────────────────┐
 │  [RF sub-GHz + can]   cerca de vias   [GNSS RX, longe dos TX]   cerca   [Wi-Fi/BLE módulo]│
 │   matching colado         │              LNA/SAW colados          │       antena p/ fora  │
 │───────────────── GND contínuo L2 · zona "silenciosa" (sem SMPS, sem clocks) ──────────────│
 │  [MCU A] + cristal A + desacopl.          (canais de roteamento livres)    [MCU B] + ...  │
 │  hub USB, flash, microSD (borda lateral)                    QWIIC/expansão (borda lateral)│
 │─────────────────────────────── zona de energia (canto inferior) ──────────────────────────│
 │ [USB-C+TVS] → [carregador power-path] → [buck-boost + L + Cin "acap"]  [JST bateria]      │
 └──── borda de encaixe/montagem (se houver: conector p/ host, HAT, backplane) — sem cabos extras ┘
```

### C. Proximidade por tipo de componente

19. **Desacoplamento:** o capacitor fica no pino de alimentação, com via de GND junto do pad de GND do capacitor e laço mínimo. **[FATO]** Espressif (via de GND "close to each capacitor's ground pad"); RP2040 ("it is important to place decoupling close to the power pins"); TI SZZA009 §2.2 (laços de bypass "as small as possible in area and length").
20. **Capacitor de entrada de SMPS no VIN/GND do CI, sem passar por via.** Se a via for inevitável, usar várias em paralelo. **[FATO]** TI SNVA054 §4–5; TI SNVA021 (AN-1149) "Input capacitor ... as close to the VIN pin of the IC as possible", `pdfs\01-floorplan\TI_SNVA021_AN-1149_Layout_Switching_Power_Supplies.pdf`, https://www.ti.com/lit/pdf/snva021
21. **Laço de potência da SMPS:** indutor, capacitores de saída e diodo juntos. Os laços dos dois estados de chaveamento devem "girar no mesmo sentido". O traço de **feedback** fica longe do indutor e do nó SW (de preferência do outro lado da placa, sob o plano). Componentes de compensação perto do CI, longe do indutor. **[FATO]** TI SNVA021 §1–5.
22. **Indutor:** usar indutor blindado (núcleo fechado) quando houver circuito sensível perto. **[FATO]** TI SNVA021 §1. **Longe do cristal** ("do not place any magnetic components nearby"). **[FATO]** Espressif, seção "Crystal".
23. **Cristal:**
   - mesmo lado do MCU;
   - capacitores de carga ao lado do cristal, no mesmo lado;
   - GND em volta ligado ao GND do MCU;
   - nenhum traço de sinal ou de energia dentro da área de guarda nem embaixo do cristal no outro lado;
   - distância ao pino **≤ 12 mm** (Microchip).
   
   **[FATO]** Microchip, dsPIC33AK256MPS306 datasheet §2.8: https://onlinedocs.microchip.com/oxy/GUID-D6315DA4-4399-4D39-80F4-F1F66A173640-en-US-4/GUID-3E98C051-6338-42AE-A8E3-AF262F4C2760.html
   
   - **Exceção do ESP32-C5 chip-down:** cristal a **≥ 2,4 mm** do pino de clock do chip, para não interferir no próprio chip. Clock sem vias. Resistor série do lado do chip. Capacitores de carga nas duas pontas do cristal, com o GND deles perto do GND do cristal. Isso não se aplica a módulos WROOM, que já trazem o cristal. **[FATO]** Espressif, seção "Crystal".
   - **Nota histórica:** a TI SZZA009 (1999, §2.4.1) pede "nenhum componente não relacionado a menos de 1 polegada (25 mm) do cristal". Isso é inviável em placa densa. Tratar como meta de "afastar o resto", não como regra. **[FATO]** sobre o texto; **[INFERÊNCIA]** sobre a interpretação.
   - Traços do cristal curtos, porque a capacitância parasita entra na carga (10 pF no RP2040). **[FATO]** RP2040 §2.3.
24. **Ferrite bead** só no +V (nunca no GND), do lado da **fonte de ruído** (perto do chip ruidoso). Com isso só o lado "barulhento" irradia. **[FATO]** TI SZZA009 §2.2, Fig. 9 "Ferrite-Bead Placement Closest to the Noise Source".
25. **Filtros LC/CLC das alimentações de RF junto aos pinos.** No ESP32-C5: 10 µF por pino VDDA (1, 3, 40, 41) e CLC/LC perto dos pinos 40/41, em 0201. **[FATO]** Espressif, "Power Supply".
26. **TVS/ESD:**
   - o mais perto do conector que as regras permitirem;
   - o CI protegido **muito mais longe** do TVS do que o TVS está do conector (L4 ≫ L1);
   - sem stub entre a linha e o TVS, com a rota passando pelo pino do TVS;
   - sem via entre o conector e o TVS;
   - GND do TVS de baixíssima indutância (furo de chassi adjacente ao GND do TVS e à blindagem do conector);
   - não rotear linhas desprotegidas na região entre o conector e o TVS.
   
   **[FATO]** TI SLVA680 §2.1–2.4, `pdfs\01-floorplan\TI_SLVA680_ESD_Protection_Layout_Guide.pdf`, https://www.ti.com/lit/pdf/slva680 · ESD do power junto da porta de energia: **[FATO]** Espressif, "Power Supply".
27. **Resistores série e de terminação:**
   - terminação série junto do pino do **driver**;
   - terminação paralela junto do pino do **receptor**.
   
   **[FATO]** Sierra (URL da regra 2).
   
   Casos citados pelos fabricantes:
   - 27 Ω do USB do RP2040 perto do chip;
   - pull-up/R do QSPI_SS perto da flash;
   - série do U0TXD do ESP32-C5 do lado do chip, longe do cristal;
   - RC/LC do SPI junto dos pinos.
   
   **[FATO]** RP2040 §2.2 e §2.4; Espressif, "UART"/"SPI".
28. **Resistor série de I/O do MCU (50–100 Ω em saídas)** o mais perto possível do MCU, sobre o "GND do micro". **[FATO]** TI SZZA009 §2.2.5.
29. **Pull-ups e pull-downs de strapping e boot** perto do pino do MCU. Deixar pad reservado para capacitor de ajuste (o GPIO28 do ESP32-C5 tem pull-up e espaço para C não montado). **[FATO]** Espressif, "Strapping pins".
30. **Test points:**
   - pelo menos **um ponto sondável por net** (flying probe);
   - pad de flying probe com mínimo de 6 mil e **20 mil (0,5 mm) recomendado**;
   - espaçamento entre pontos ≥ 10–20 mil;
   - distância a componentes L = 0,29 × altura + 0,7 mm (peça de 4 mm dá 1,86 mm);
   - borda "não sondável" de cerca de 3 mm.
   
   No ICT: pad de 0,9 mm no topo e 0,7 mm embaixo; centro a centro de 2,1 mm (agulha de 2,54 mm) ou 1,25 mm (agulha de 1,27 mm); 0,9 mm da borda. **[FATO]** Sierra DFT (valores baseados em SEICA): https://www.protoexpress.com/blog/design-for-testing-guidelines-pcb-manufacturing/ · Guia ICT (pad de 0,05" = 1,27 mm; pad quadrado tem cerca de 27 % mais área): `pdfs\01-floorplan\SMTnet_Design_Guidelines_In-Circuit_Testability.pdf`
31. **LEDs e botões:** na borda acessível, agrupados com o chip ou a função que indicam (Feather: LED de usuário acima do USB e LED CHG abaixo; botão de reset obrigatório). **[FATO]** Adafruit Feather Specification: https://learn.adafruit.com/adafruit-feather/feather-specification · regra da casa §14 (botões por chip).

### D. Orientação, alinhamento e grade

32. **Peças semelhantes na mesma orientação.** Polarizados todos para o mesmo lado (capacitores "all face the same direction"). Pino 1 e polaridade marcados no footprint ("K" no cátodo, "+" no tântalo). Segundo a Sierra, falta de pino 1 ou de polaridade é o principal "show-stopper" na montagem. **[FATO]** Sierra DFA tips: https://www.protoexpress.com/blog/tips-pcb-design-for-assembly/ · JLCPCB placement guide.
33. **Orientação zero do IPC-7351:**
   - R/C/L com o pino 1 (positivo) à esquerda;
   - diodo com o cátodo à esquerda;
   - SOT/SOIC/QFP/BGA com o pino 1 no canto superior esquerdo.
   
   Girar só em múltiplos de 90°. **[FATO]** sobre a tabela (Sierra, IPC-7351): https://www.protoexpress.com/blog/features-of-ipc-7351-standards-to-design-pcb-component-footprint/ · **[INFERÊNCIA]** sobre "só 90°": é prática para o CPL e o pick-and-place, sem norma lida.
34. **Grade de placement:** **não encontrei número normativo** (a IPC-7351 não foi lida). A KLC exige courtyard numa grade de **0,01 mm** e linha de 0,05 mm. **[FATO]** KLC F5.3 (fonte: https://gitlab.com/kicad/libraries/klc/-/raw/master/content/footprint/F5/F5.3.adoc, página: https://klc.kicad.org/footprint/f5/f5.3/). Prática sugerida: grade de 0,5 mm para CIs e conectores e 0,1 mm ou 0,05 mm para passivos. **[INFERÊNCIA]**.

### E. DFA / montagem (JLCPCB e indústria)

35. **Courtyard da KLC:**
   - folga padrão de **0,25 mm**;
   - **0,15 mm** para peças com menos de 1,5 mm em qualquer dimensão;
   - conectores com **0,5 mm**, mais a folga de acoplamento do conector macho;
   - capacitores enlatados com **0,5 mm**;
   - cristais com **0,5 mm**;
   - BGA/WLCSP com **1,0 mm**.
   
   **[FATO]** KLC F5.3 (URL da regra 34).
   
   IPC-7351B, níveis de densidade: A (Most, cerca de 0,50 mm), B (Nominal, cerca de 0,25 mm), C (Least, cerca de 0,10 mm). A é para baixa densidade; C para alta densidade (celulares). **[INFERÊNCIA — fonte secundária]** (valores de fórum e glossário; os rótulos variam entre as fontes; a norma não foi lida): https://www.pcblibraries.com/forum/topic3372.html · definições A/B/C **[FATO]** via Sierra (URL da regra 33).
36. **Courtyard sem sobreposição não garante DFA.** A JLCPCB tem uma tabela própria de **espaçamento mínimo entre encapsulamentos** (mm). **[FATO]** https://jlcpcb.com/help/article/minimum-spacing-for-smd-components

   | | 0201/0402 | 0603/0805 | 1206 | QFN | QFP | SOP | SOT | BGA |
   |---|---|---|---|---|---|---|---|---|
   | chip 0201–0805 | 0,15–0,18 | 0,18 | 0,25 | **1,0** | 0,5 | 0,4 | 0,2 | **1,0** |
   | chip 1206 | 0,25 | 0,25 | 0,35 | 1,0 | 0,5 | 0,4 | 0,2 | 1,0 |
   | QFN | 1,0 | 1,0 | 1,0 | 1,0 | 1,0 | 1,0 | 1,0 | 1,5 |
   | QFP | 0,5 | 0,5 | 0,5 | 1,0 | 1,25 | 1,25 | 1,0 | 1,5 |
   | SOP/SOIC | 0,4 | 0,4 | 0,4 | 1,0 | 1,25 | 0,5 | 0,4 | 1,0 |
   | SOT | 0,2 | 0,2 | 0,2 | 1,0 | 1,0 | 0,4 | 0,4 | 1,0 |
   | BGA | 1,0 | 1,0 | 1,0 | 1,5 | 1,5 | 1,0 | 1,0 | **2,0** |

   **Por quê:** inspeção, retrabalho e ponte de solda. A Sierra pede ≥ 10 mil entre discretos e prefere **30 mil (0,76 mm)**. **[FATO]** Sierra DFA tips.
37. **Distância à borda:** o corpo de qualquer componente fica a **≥ 2,5 mm** da borda da placa. **[FATO]** JLCPCB Terms and Conditions of Assembly, seção 2 item 3: https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service · Cobre: ≥ 0,2 mm da borda fresada e ≥ 0,4 mm de V-cut. **[FATO]** https://jlcpcb.com/capabilities/pcb-capabilities
38. **Rails (process edges):** ≥ **5 mm**, obrigatórios no PCBA Standard. Servem para afastar as peças da borda. Se forem estreitos demais, as peças da borda batem nas guias da linha. **[FATO]** https://jlcpcb.com/help/article/how-to-add-edge-rails-fiducials-for-pcb-assembly-order · https://jlcpcb.com/help/article/specifications-for-adding-process-edges-and-positioning-holes · "Tooling holes, Edge rails and Fiducials are required for PCB assembly orders"; se faltarem, a JLC adiciona por padrão. **[FATO]** T&C seção 5 item 5.
39. **Fiduciais globais:**
   - **3** (mínimo de 2), em "L", o mais afastados possível;
   - pad de cobre de **1,0 mm** sem furo;
   - abertura de máscara e keep-out de cobre de **2,0 mm**;
   - a **≥ 3,35 mm** da borda (incluindo o keep-out);
   - num jogo por lado populado.
   
   **[FATO]** https://jlcpcb.com/blog/fiducial-marks · https://jlcpcb.com/help/article/how-to-add-edge-rails-fiducials-for-pcb-assembly-order · Em painel: fiducial de 1 mm a 3,85 mm da borda do painel. **[FATO]** process-edges.
40. **Fiduciais locais:** 2 em diagonal sobre o land pattern de BGA/QFP/QFN com **passo ≤ 0,5 mm**. **[FATO]** JLCPCB fiducial-marks.
41. **Furos de ferramenta (tooling):** 2–3 furos NPTH de **1,152 mm** em cantos opostos, em área livre e longe de trilhas. **[FATO]** https://jlcpcb.com/help/article/How-to-add-tooling-holes-for-PCB-assembly-order · No painel: 2 mm. **[FATO]** process-edges.
42. **Tamanho e lados no PCBA da JLC:**

   | | Economic | Standard |
   |---|---|---|
   | Placa | 10×10 a 470×500 mm | 70×70 a 460×500 mm |
   | Lados montados | **um** | **dois** |
   | Menor encapsulamento | 0402 | 01005 |
   | Passo mínimo de CI | 0,4 mm | 0,35 mm |
   | Passo mínimo de BGA | 0,5 mm | 0,3 mm |
   | Reflow | 255 ± 5 °C | 240 ± 5 °C |
   
   Painel recomendado: ≤ 250×250 mm. **[FATO]** https://jlcpcb.com/capabilities/pcb-assembly-capabilities
43. **Painel (JLC):**
   - lado do painel de 150–200 mm, com 2–6 placas;
   - espaço entre placas ≥ 2 mm;
   - mouse bites de 0,5–0,8 mm de diâmetro;
   - abas de ≥ 4–5 mm;
   - entre dois V-cuts, 2 mm (3 mm recomendado).
   
   **[FATO]** https://jlcpcb.com/help/article/Panelizing-your-PCB-for-Assembly · https://jlcpcb.com/capabilities/pcb-capabilities
44. **MLCC e flexão:** a prática exige cerca de **5 mm** entre a borda e o capacitor cerâmico, com orientação **paralela** à borda. Usar fresado (relief) na linha de quebra em vez de V-score ou quebra manual. **[FATO]** Vishay, documento 49088, `pdfs\01-floorplan\Vishay_49088_MLCC_Board_Flex_Technical_Paper.pdf`, https://www.vishay.com/docs/49088/49088_technicalpaper.pdf · A Murata classifica as posições junto à quebra e diz que "paralelo à linha de quebra" é o mais eficaz. Se não der para girar a peça, abrir uma fenda (slit). **[FATO]** https://article.murata.com/en-eu/article/layout-helps-prevent-chip-mlcc-from-cracking
45. **Tombstoning (peça que levanta de um lado):** a causa é o desequilíbrio de molhagem entre os dois pads (um pad ligado a plano ou trilha larga aquece mais devagar). Pads simétricos, trilhas de largura equivalente e thermal relief no plano. Peças pequenas (0402/0201) são mais sensíveis. **[FATO]** Nordson EFD *Tombstone Troubleshooting*, `pdfs\01-floorplan\Nordson_EFD_Tombstone_Troubleshooting.pdf`, https://www.smtnet.com/library/files/upload/EFD-Tombstone-Troubleshooting.pdf · Via a > 1 mm do pad ou espelhada nos dois lados **[INFERÊNCIA — fonte secundária]** (blog AllPCB): https://www.allpcb.com/blog/pcb-assembly/tombstoning-in-smd-components.html
46. **Vias térmicas sob o pad:** podem roubar calor no reflow e prejudicar a junta. Usar furo pequeno (0,3–0,33 mm) a passo de 1–1,2 mm, ou pôr as vias "perto, mas não sob" o terminal. **[FATO]** TI SNVA054 §6.3.
47. **Dois lados (reflow duplo):** o lado de baixo leva peças pequenas e leves, que são refundidas de cabeça para baixo na 2ª passada. As pesadas (transformador, conector grande) vão em solda seletiva ou manual. **[FATO]** Altium: https://resources.altium.com/p/best-design-practices-double-sided-pcb-soldering-smd-parts · Critério massa ÷ área de pad **< 30 g/in²** (Zarrow; cerca de 0,047 g/mm² com SAC305). É otimista para peças com um pad dominante (QFN, EP). **[INFERÊNCIA — fonte secundária]**. Método de candidatura por peso e área de pad com solda lead-free: Liu, Geiger & Shangguan, Materials Transactions 47(6), 2006, https://www.jstage.jst.go.jp/article/matertrans/47/6/47_6_1577/_article/-char/en A Espressif recomenda **não pôr componentes na camada de baixo** da placa do ESP32-C5. **[FATO]** Espressif 1.4.1.
48. **Solda por onda (quando houver THT no lado de baixo):** peças altas não ficam "antes" das baixas no sentido da onda, porque fazem sombra. CIs alinhados ao sentido da onda. Conectores de várias fileiras paralelos à onda fazem ponte. **[INFERÊNCIA — fonte secundária]** (blogs; resumo de busca): https://www.protoexpress.com/kb/wave-soldering-design-considerations/ · https://www.vse.com/blog/wave-soldering-placement-guidelines/ Na JLC, preferir THT montado por SMT ou à mão, e evitar SMD no lado da onda. **[INFERÊNCIA]**.
49. **Peças altas e test points:** manter folga para a sonda. A Sierra pede L = 0,29 × altura + 0,7 mm (regra 30). **[FATO]**.

### F. Térmico no placement

50. **Espalhar as fontes de calor e calcular a área.** Placa de 2 lados com cobre cheio, sem fluxo de ar: **≥ 15,29 cm² por watt para ΔT de 40 °C**. Com ventilação, a área cai até à metade. Fontes múltiplas somam por superposição ("almost works"). **[FATO]** TI SNVA419 (AN-2020) Regras 1 e 6, `pdfs\01-floorplan\TI_SNVA419_AN-2020_Thermal_Design_By_Insight.pdf`, https://www.ti.com/lit/pdf/snva419
51. **Vias térmicas:** uma via de 12 mil com 0,5 oz tem cerca de **261 °C/W**. Fazer uma matriz a **1 mm** de passo sob o EP, ligada a todos os planos de GND. **[FATO]** TI SNVA419 Regra 2.
52. **Não cortar o plano de cobre no caminho do calor.** Um corte perpendicular ao fluxo somou +5,5 °C no exemplo da TI. Trilhas que atravessam o "espalhador" devem correr radiais à fonte. Planos que chegam às bordas melhoram até 30 %. **[FATO]** TI SNVA419 Regras 1 e 4.
53. **Rendimento decrescente do cobre:** cerca de 1 in² com 1 oz já dá a maior parte do ganho. Até 3 in² (2 oz) ainda melhora; acima disso, só com dissipador. Plano do outro lado sem vias ajuda 10–20 %; **com vias térmicas, 50–70 %**. **[FATO]** TI SNVA054 §6.3.
54. **Na SMPS, cobre de dissipação no nó SW é antena.** Não exagerar o cobre do nó de chaveamento. **[FATO]** TI SNVA054 §6.3.
55. **Componentes sensíveis a calor longe dos quentes:**
   - eletrolítico: a vida dobra a cada −10 °C (regra de Arrhenius; Würth SN008, Rohm, KEMET) **[INFERÊNCIA — fonte secundária]** (o PDF da Würth não baixou; https://community.element14.com/products/manufacturers/wuerth-elektronik/b/blog/posts/sn008-expected-lifetime-of-aluminum-electrolytic-and-aluminum-polymer-capacitor);
   - cristal (deriva de frequência), sensores e referências longe dos reguladores, MOSFETs e PA **[FATO]** JLCPCB placement guide, que também os afasta de furos de fixação e bordas por estresse mecânico.
56. **Peças grandes distribuídas pela placa** para o aquecimento no reflow ser uniforme. **[FATO]** Sierra DFA tips.

### G. Compactação: como encolher e quando não encolher

57. **Ferramentas de compactação:**
   - encapsulamentos menores (0402 cabe no Economic; 0201 e 01005 só no Standard);
   - os dois lados (Standard);
   - via-in-pad;
   - módulos prontos (WROOM, MAX-M10S), que já resolvem RF e cristal;
   - mais camadas, para liberar canais.
   
   **[FATO]** sobre os limites JLC (regra 42). **[INFERÊNCIA]** sobre a estratégia.
58. **Via-in-pad (POFV, resina com tampa de cobre):** a JLC aplica automaticamente em placas de **6 camadas ou mais**. Furo típico de 0,15–0,3 mm (mínimo de 0,1 mm a laser ou 0,15 mm mecânico). **[FATO]** https://jlcpcb.com/help/article/via-in-pad-pofv-guide · Que seja "grátis" em 6–20 camadas **[INFERÊNCIA — fonte secundária]** (notícia JLC vista em busca: https://jlcpcb.com/news/free-via-in-pad-6-20-layer-pcbs-pofv). Em 4 camadas, via-in-pad não é processo padrão: evitar via aberta em pad (a solda escorre). **[INFERÊNCIA]**.
59. **O RP2040 mostra o custo de compactar pouco ou muito.** Na placa de 2 camadas com peças só em cima, os pinos 48 e 49 dividem um único capacitor. Mais desacoplamento exigiria peças menores ou 4 camadas com os dois lados. **[FATO]** RP2040 §2.1.2.
60. **Não compactar quando:**
   - faltar canal de roteamento entre CIs (o caso da casa §15);
   - houver calor concentrado (regra 50);
   - precisar de retrabalho (BGA/QFN pedem 1–2 mm, regra 36);
   - precisar de test points (regra 30);
   - houver peças altas que fazem sombra na sonda ou na inspeção;
   - a zona for de RF, onde é preciso afastar os domínios.
   
   **[FATO]** para os números citados; **[INFERÊNCIA]** para o conjunto.
61. **Densidade-alvo:** **não encontrei número com fonte primária.** Prática comum: começar com cerca de 50–60 % da área útil ocupada por courtyards e só apertar depois de o roteamento fechar. **[INFERÊNCIA]**. Caso real da casa: 150×80 mm para cerca de 130 peças (2 camadas densas).

### H. Exemplos de placas profissionais

62. **Adafruit Feather:**
   - formato fixo de 0,9" × 2,0" (22,9 × 50,8 mm), com furos nos 4 cantos;
   - USB centralizado numa ponta;
   - JST-PH da LiPo a 0,425" da borda esquerda;
   - LED de usuário e LED CHG ao lado do USB;
   - reset obrigatório;
   - para ganhar área, aumentar o comprimento ou usar os dois lados, nunca a largura (para manter a compatibilidade dos headers).
   
   **[FATO]** https://learn.adafruit.com/adafruit-feather/feather-specification
63. **RP2040 Minimal (Raspberry Pi):**
   - 2 camadas, peças só em cima (mais barato e mais fácil de montar);
   - desacoplamento colado aos pinos;
   - cristal com C de carga simétricos e traço curto;
   - flash junto do QSPI, com R1/R2 perto da flash;
   - R série do USB perto do chip.
   
   O próprio layout traz notas do tipo "Make sure C8 is close to pin 45". **[FATO]** RP2040 §2.
64. **Espressif (layout de referência do ESP32-C5):**
   - 4 camadas: L2 GND sem trilha, L3 energia sob GND sólido no RF e no cristal, L4 com poucas trilhas e **sem componentes**;
   - módulo na borda, com a antena para fora.
   
   **[FATO]** Espressif 1.4.1.
65. **Dev boards de referência (SparkFun, Adafruit, Espressif DevKit, devboard Wi-Fi do Flipper `[FLIPPER]`):** **não analisadas em detalhe nesta rodada** (pendência). Arquivos da devboard do Flipper estão em `referencias/flipper-zero/` como exemplo de placa que encaixa em host.

---

## Erros comuns

| Erro | Consequência | Correção |
|---|---|---|
| Rotear antes de fechar o placement | Retrabalho, ilhas de GND, trilhas fantasma (casa §13 nº 18/19) | Ordem: mecânica → críticos → CIs → suporte → resto → **só então** rotear (regras 1–6) |
| Cortar o plano de GND entre "analógico" e "digital" | Retorno contorna o corte: laço grande, EMI e ruído no analógico | Plano único particionado e roteamento disciplinado (regra 11) |
| SMPS no meio da placa ou sob o RF | Nó SW irradia nos front-ends; VBUS/VBAT atravessam a placa | Energia no canto da entrada; laço quente compacto (regras 9, 20, 21) |
| Cap de entrada da SMPS "perto" mas através de via | Indutância no laço quente: ringing e EMI | Cap e diodo/FET "acap", sem via (regra 20) |
| Feedback da SMPS passando ao lado do indutor | Ruído na malha de controle, instabilidade | Feedback do outro lado e longe do SW e do indutor (regra 21) |
| TVS longe do conector ou ligado por stub | A ESD entra no CI antes do TVS conduzir | TVS colado ao conector, sem stub e sem via; CI longe (regra 26) |
| Ferrite no GND ou do lado "limpo" | Filtro inútil; o lado ruidoso irradia | Ferrite só no +V, do lado do chip ruidoso (regra 24) |
| Sinal ou energia passando sob o cristal; indutor ao lado do cristal | Jitter, deriva, falha de partida | Área de guarda em GND; nada por baixo; magnéticos longe (regra 23) |
| Achar que courtyard OK = montável na JLC | Ponte, retrabalho impossível, peça rejeitada no DFM | Conferir a tabela de espaçamento JLC (QFN/QFP/BGA ≥ 1–2 mm) (regra 36) |
| Peça a < 2,5 mm da borda sem rails | A peça bate na guia da linha; peça faltando ou deslocada | Rails de 5 mm ou painel; corpo a ≥ 2,5 mm (regras 37–38) |
| Sem fiduciais / fiducial perto da borda ou sem abertura de máscara | Visão da máquina falha; deslocamento em fine-pitch | 3 globais de 1 mm / 2 mm, a ≥ 3,35 mm; locais em passo ≤ 0,5 mm (regras 39–40) |
| MLCC perpendicular e colado a V-cut ou furo de fixação | Trinca de flexão: curto latente | ≥ 5 mm, paralelo à borda, ou slit/fresado (regra 44) |
| Pads assimétricos em 0402 (um no plano, outro em trilha fina) | Tombstoning | Thermal relief e cobre equivalente (regra 45) |
| Polarizados em orientações aleatórias, sem marca de pino 1 | Montagem invertida (principal "show-stopper") | Mesma orientação; "K"/"+"/pino 1 no silk (regra 32) |
| Placa densa sem nenhum test point | Sem diagnóstico na produção nem flying probe | 1 ponto por net crítica; pad de 0,5 mm; folga das peças altas (regra 30) |
| Compactar ao máximo antes de rotear | Autorouter trava por falta de canal | Reservar canais; desdensificar 1–5 mm (regra 6, casa §15) |
| Componentes no verso de placa Economic | A JLC não monta (só um lado) | Tudo em cima, ou PCBA Standard (regra 42) |

---

## Checklist

**Floorplan**
- [ ] Contorno e mecânica tirados do arquivo oficial; conectores, furos, antenas e botões travados antes de qualquer outra peça.
- [ ] Zonas desenhadas (energia / digital / RF / analógico / IO / IHM) com o fluxo: entrada de energia → regulador → MCU → periféricos → analógico mais longe.
- [ ] Zona de energia no canto da entrada (USB-C/bateria), longe dos RF RX (GNSS, sub-GHz).
- [ ] RF na borda da antena; módulo com antena para fora; ≥ 15 mm livres na carcaça; UART, USB e test points longe da antena.
- [ ] Plano de GND único, sem cortes, com as zonas separadas por placement.
- [ ] Canais de roteamento reservados entre os CIs.

**Proximidade**
- [ ] Cap de entrada e diodo/FET da SMPS "acap", sem via; feedback longe do SW e do indutor; indutor blindado.
- [ ] Desacoplamento no pino, com via de GND junto ao pad do cap.
- [ ] Cristal no mesmo lado do MCU, Cs de carga simétricos, guarda em GND, nada por baixo, indutores longe (ESP32 chip-down: ≥ 2,4 mm do pino).
- [ ] Ferrite no +V, do lado da fonte de ruído; LC/CLC junto dos pinos de RF.
- [ ] TVS colado a cada conector externo (USB, SMA se aplicável, GPIO), sem stub nem via.
- [ ] Terminação série no driver e paralela no receptor; pull-ups de boot junto do MCU.

**DFA (JLCPCB)**
- [ ] Corpo das peças a ≥ 2,5 mm da borda **ou** rails de 5 mm / painel previstos (conectores flush: ver Conflitos).
- [ ] Espaçamento entre peças ≥ tabela JLC (QFN/QFP 1,0–1,25 mm; BGA 2,0 mm; chips 0,15–0,35 mm).
- [ ] 3 fiduciais globais (1 mm de cobre, 2 mm de máscara, ≥ 3,35 mm da borda) por lado populado; fiduciais locais em passo ≤ 0,5 mm.
- [ ] 2–3 tooling holes de 1,152 mm (ou deixar a JLC adicionar no rail).
- [ ] Placa ≥ 70×70 mm para Standard (ou painel); Economic = um lado só.
- [ ] Polarizados na mesma orientação; pino 1, "K" e "+" no silk; rotações em múltiplos de 90°.
- [ ] MLCCs a ≥ 5 mm de V-cut, furo de fixação e borda, ou paralelos a ela.
- [ ] Pads de 0402/0201 com cobre simétrico (thermal relief no plano).
- [ ] Test points: 1 por net crítica (energia, reset, boot, UART, I²C), pad de 0,5 mm, folga de 0,29 × h + 0,7 mm das peças altas.

**Térmico**
- [ ] Potência por fonte estimada; área ≥ 15 cm²/W (2 lados, ar parado, ΔT 40 °C); fontes espalhadas.
- [ ] Matriz de vias térmicas a 1 mm sob os EPs; plano sem cortes no caminho do calor.
- [ ] Eletrolíticos, cristais, sensores e GNSS longe de reguladores e PA.

**Fechamento**
- [ ] Revisão de zoneamento e de acesso aos conectores **antes** de rotear (casa §12).
- [ ] Courtyard e DRC zerados **e** conferência manual contra a tabela JLC e o gate de borda.

---

## Conflitos com PADROES-PROJETO-PCB.md

> Só listo; o dono decide. Seções lidas: §2, §5, §9, §12, §14, §15 (e §3, §6, §13 por contexto).

### Confirma
- **§12 (placement antes de rotear):** confirmado por Altium, JLCPCB e Sierra (regras 1–6). A ordem que a literatura dá é mais detalhada: mecânica → críticos → CIs → suporte → resto.
- **§14 (energia no quadrante da entrada USB-C):** confirmado pela TI SZZA009 §2.3 (regulador ao lado da entrada de energia, MCU ao lado do regulador).
- **§14 (SMPS longe do RF, num canto):** confirmado (TI SZZA009 zoneamento; JLCPCB, "ruidosos longe de sensíveis").
- **§2 (espalhar geradores de calor):** confirmado pela TI SNVA419 (área por watt; superposição de fontes).
- **§2/§14 (desacoplamento colado; cristal com caps simétricos e GND sólido abaixo):** confirmado (Espressif, RP2040, Microchip, TI).
- **§7 (ferrite + LC por rádio):** coerente com a TI SZZA009 (ferrite no +V, do lado da fonte de ruído) e com a Espressif (CLC por VDDA). A literatura acrescenta *em que lado* pôr a ferrite.
- **§9 (componentes alinhados e agrupados por função):** confirmado (Sierra: mesma orientação; TI: zoneamento).
- **§15 (falha por falta de canal; desdensificar abre canais):** confirmado pelo JLCPCB placement guide ("reservar espaço de roteamento antes de encher de passivos").

### Diverge / precisa de nuance
1. **§5 e §13 nº 1–3 ("conector flush na borda", SMA com pad a cerca de 1–1,5 mm da borda) × JLCPCB T&C (corpo a ≥ 2,5 mm da borda; rails obrigatórios no PCBA Standard).** As duas regras convivem se a placa for com **rails ou em painel**: o conector fica flush na borda *da placa*, e a borda que a linha de montagem vê é a do rail. Isso tem custo: rail destacável e pós-processamento. **Não encontrei** como a JLC trata um conector cujo corpo **ultrapassa** a borda (SMA edge-mount, USB-C mid-mount) quando há rail; consultar a JLC antes do pedido. Também **não encontrei** se os 2,5 mm valem com ou sem rail.
2. **Placas pequenas (< 70 mm em algum lado, ex. `[FLIPPER]`: módulo externo do Flipper Zero, 67,34 mm) × PCBA Standard mínimo de 70×70 mm.** Abaixo disso a JLC exige painel ou rail (T&C item 14). O Economic aceita a partir de 10×10 mm, mas **só um lado** e **só até 0402**.
3. **§15 (`spread.py` com GAP de 0,6 mm; "check_courtyard_overlaps = 0" como critério) × tabela JLC de espaçamento mínimo** (QFN↔qualquer 1,0 mm; QFP↔QFP 1,25 mm; BGA 2,0 mm). Um GAP de 0,6 mm entre courtyards pode **não** atender QFN↔QFN. Sugestão: o script ganharia uma tabela de folga por par de encapsulamentos.
4. **§2/§14 ("cristal colado ao pino") × Espressif ESP32-C5 chip-down (≥ 2,4 mm do pino de clock).** Para módulos (WROOM) a questão some, porque o cristal é interno. Nos chips nus (CC1101, nRF24, hub FE1.1s) vale o datasheet de cada um. A Microchip dá teto de 12 mm. A TI (1999) pede 25 mm livres de peças não relacionadas, o que é inviável. Ajuste sugerido: "cristal próximo e **conforme o datasheet do chip**", não "colado".
5. **§6 ("hub USB elimina os headers de flash avulsos **e os test pads**") × DFT (pelo menos 1 ponto sondável por net; pads de 0,5 mm).** Eliminar o header de flash está certo. Eliminar *todos* os test pads tira o diagnóstico e o flying probe. Sugestão: manter pads SMD pequenos (sem header) em 3V3, VBAT, VSYS, GND, EN/RESET, BOOT, UART TX/RX e I²C.
6. **§12 "zero overlaps/courtyard" usa os courtyards da KLC (0,25 mm padrão; 0,5 mm em conectores e cristais; 1,0 mm em BGA).** A KLC fica perto do nível B/Nominal da IPC. Não é falha, mas o critério de "montável" é a regra 36, não o DRC.

### Falta no PADROES (a literatura cobre e a casa não)
- **Fiduciais:** 3 globais por lado populado (1 mm / máscara de 2 mm / ≥ 3,35 mm da borda) e locais em passo ≤ 0,5 mm (CC1101 QFN-20 0,5 mm, hub em QFN).
- **Tooling holes** (1,152 mm, 2–3, cantos opostos) e plano de **rails/painel**.
- **MLCC a ≥ 5 mm de V-cut, furo ou borda, ou paralelo a ela** (flex crack). Atenção redobrada em placas aparafusadas ou que sofrem torque de alavanca num conector de encaixe (módulos plugáveis, HATs).
- **Restrições de lado na JLC:** Economic monta um lado só. A Espressif recomenda não pôr componentes no verso.
- **TVS/ESD colado a cada conector externo** (USB-C, conector de encaixe/expansão, SMA, terminais de cabo), com as regras de stub e via da TI SLVA680. A casa cita ESD só de passagem.
- **Lado da ferrite** (fonte de ruído) e **terminação série no driver / paralela no receptor**.
- **Regras térmicas numéricas:** 15 cm²/W, vias de 1 mm de passo, sem cortes no caminho do calor, eletrolítico longe do calor.
- **Polaridade e orientação uniformes** (pino 1, "K", "+" no silk; mesma direção).
- **Test points / DFT** (ver Diverge 5).
- **Tombstoning:** pads simétricos e thermal relief em passivos pequenos ligados a plano.

---

## Bibliografia

### Livros (não lidos nesta rodada — só citar; pagos, não baixar)
- **Henry W. Ott**, *Electromagnetic Compatibility Engineering*, Wiley, 2009. É a referência de partição, retorno de corrente e plano único. Base do artigo da TI SLYT512.
- **Douglas Brooks & Johannes Adam**, *PCB Design Guide to Via and Trace Currents and Temperatures*, Artech House, 2021. Térmico de trilhas e vias.
- **Mark I. Montrose**, *Printed Circuit Board Design Techniques for EMC Compliance*, 2ª ed., IEEE Press/Wiley, 2000. Zoneamento e partição para EMC.
- **Eric Bogatin**, *Signal and Power Integrity — Simplified*, 3ª ed., Prentice Hall, 2018. Laços de corrente e desacoplamento.
- *Printed Circuit Board Designer's Reference* (Christopher Robertson, Prentice Hall, 2004) e *Complete PCB Design Using OrCAD* (Mitzner, Newnes): sugeridos no pedido, mas **não avaliados**. São mais tutoriais de ferramenta do que de floorplan (**[INFERÊNCIA]**).

### Normas (só citar; não baixar)
- **IPC-7351B/C** (*Generic Requirements for Surface Mount Design and Land Pattern Standard*) e o sucessor **IPC-7352**: níveis de densidade A/B/C, courtyard, orientação zero.
- **IPC-2221** (*Generic Standard on Printed Board Design*): folgas e espaçamentos gerais.
- **IPC-A-610** (aceitabilidade de montagens) e **J-STD-001** (solda): critério de inspeção.

### App notes / guias de fabricante (baixados em `pdfs\01-floorplan\`)
| Arquivo | Fonte | Por que vale |
|---|---|---|
| TI_SZZA009_PCB_Design_Guidelines_Reduced_EMI.pdf | https://www.ti.com/lit/pdf/szza009 | Zoneamento, ferrite, cristal, GND do micro (clássico de 1999) |
| TI_SNVA054_AN-1229_Simple_Switcher_PCB_Layout.pdf | https://www.ti.com/lit/pdf/snva054 | Ordem "acap" na SMPS, vias térmicas, cobre × EMI |
| TI_SNVA021_AN-1149_Layout_Switching_Power_Supplies.pdf | https://www.ti.com/lit/pdf/snva021 | Indutor, feedback, laços de potência |
| TI_SNVA419_AN-2020_Thermal_Design_By_Insight.pdf | https://www.ti.com/lit/pdf/snva419 | Regras térmicas numéricas de placement |
| TI_SLVA680_ESD_Protection_Layout_Guide.pdf | https://www.ti.com/lit/pdf/slva680 | Posição do TVS, stubs, vias, GND de ESD |
| TI_SLYT512_Grounding_Mixed_Signal_Demystified_Part1.pdf | https://www.ti.com/lit/pdf/slyt512 | Plano único particionado × plano dividido |
| Espressif_ESP32-C5_Hardware_Design_Guidelines.pdf | https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c5/ | Placement do ESP32-C5: módulo, antena, cristal, energia |
| RaspberryPi_Hardware_Design_with_RP2040.pdf | https://datasheets.raspberrypi.com/rp2040/hardware-design-with-rp2040.pdf | Exemplo completo e comentado de placement mínimo (KiCad) |
| Vishay_49088_MLCC_Board_Flex_Technical_Paper.pdf | https://www.vishay.com/docs/49088/49088_technicalpaper.pdf | 5 mm da borda e orientação de MLCC |
| Nordson_EFD_Tombstone_Troubleshooting.pdf | https://www.smtnet.com/library/files/upload/EFD-Tombstone-Troubleshooting.pdf | Causas de tombstoning ligadas ao layout |
| SMTnet_Design_Guidelines_In-Circuit_Testability.pdf | https://www.smtnet.com/library/files/upload/Design_guidelines_for_in-circuit_testability.pdf | Pads de ICT, passo e acesso |

### Não baixados (consultar online)
- ST **AN2867**, *Oscillator design guide for STM8AF/AL/S and STM32* (o download deu timeout; conteúdo não lido): https://www.st.com/resource/en/application_note/an2867-oscillator-design-guide-for-stm8afals-and-stm32-microcontrollers-stmicroelectronics.pdf
- Microchip, dsPIC33AK datasheet §2.8 *External Oscillator Layout Guidance*: https://onlinedocs.microchip.com/oxy/GUID-D6315DA4-4399-4D39-80F4-F1F66A173640-en-US-4/GUID-3E98C051-6338-42AE-A8E3-AF262F4C2760.html
- Murata, *Layout helps prevent chip MLCC from cracking*: https://article.murata.com/en-eu/article/layout-helps-prevent-chip-mlcc-from-cracking

### JLCPCB (fábrica-alvo)
- Assembly capabilities: https://jlcpcb.com/capabilities/pcb-assembly-capabilities
- PCB capabilities (bordas, V-cut, painel): https://jlcpcb.com/capabilities/pcb-capabilities
- Minimum Spacing Requirements for SMD Components: https://jlcpcb.com/help/article/minimum-spacing-for-smd-components
- Edge rails & fiducials: https://jlcpcb.com/help/article/how-to-add-edge-rails-fiducials-for-pcb-assembly-order
- Process edges & positioning holes: https://jlcpcb.com/help/article/specifications-for-adding-process-edges-and-positioning-holes
- Tooling holes: https://jlcpcb.com/help/article/How-to-add-tooling-holes-for-PCB-assembly-order
- Panelizing for assembly: https://jlcpcb.com/help/article/Panelizing-your-PCB-for-Assembly
- Terms & Conditions of Assembly (2,5 mm da borda): https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service
- Fiducial marks guide: https://jlcpcb.com/blog/fiducial-marks
- PCB component placement guide: https://jlcpcb.com/blog/pcb-component-placement-guide-2026
- Via-in-pad POFV guide: https://jlcpcb.com/help/article/via-in-pad-pofv-guide

### Artigos / blogs técnicos
- Altium, *Where Do They All Go? PCB Layout Component Placement Guidelines*: https://resources.altium.com/p/where-do-they-all-go-pcb-layout-component-placement-guidelines
- Altium, *Best Design Practices for Double-Sided PCB Soldering with SMD Parts*: https://resources.altium.com/p/best-design-practices-double-sided-pcb-soldering-smd-parts
- Sierra Circuits, *Component placement guidelines*: https://www.protoexpress.com/blog/component-placement-guidelines-pcb-design-assembly/
- Sierra Circuits, *Tips for PCB design for assembly*: https://www.protoexpress.com/blog/tips-pcb-design-for-assembly/
- Sierra Circuits, *Design for testing guidelines*: https://www.protoexpress.com/blog/design-for-testing-guidelines-pcb-manufacturing/
- Sierra Circuits, *Features of IPC-7351*: https://www.protoexpress.com/blog/features-of-ipc-7351-standards-to-design-pcb-component-footprint/
- Sierra Circuits, *DFA Handbook* (e-book gratuito com cadastro; não baixado): https://www.protoexpress.com/pcb-design-guides/dfa-handbook/
- KiCad Library Conventions F5.3 (courtyard): https://klc.kicad.org/footprint/f5/f5.3/ (fonte: https://gitlab.com/kicad/libraries/klc/-/raw/master/content/footprint/F5/F5.3.adoc)
- PCB Libraries forum (courtyard IPC-7351, secundária): https://www.pcblibraries.com/forum/topic3372.html
- Adafruit, *Feather Specification*: https://learn.adafruit.com/adafruit-feather/feather-specification
- Fedevel (Robert Feranec), tip 081: https://www.fedevel.com/blog/tip-081-place-components-in-the-schematic-close-to-the-pins-where-they-should-be-located-on-pcb
- Würth SN008 (vida de eletrolíticos, via element14): https://community.element14.com/products/manufacturers/wuerth-elektronik/b/blog/posts/sn008-expected-lifetime-of-aluminum-electrolytic-and-aluminum-polymer-capacitor

### Cursos / vídeos
- **Rick Hartley**, *How to Achieve Proper Grounding* (Altium, cerca de 2h20; não assistido nesta rodada): https://resources.altium.com/p/us-how-to-achieve-proper-grounding-rick-hartley-expert-live-training
- **Robert Feranec / FEDEVEL Academy**: cursos de layout (tip 081 acima).

### Ferramentas
- Calculadora de impedância JLCPCB (stackup real): https://jlcpcb.com/pcb-impedance-calculator
- KiCad 10: DRC de courtyard, regras customizadas por par de footprints (dá para codificar a tabela JLC da regra 36 como regra de "courtyard clearance" condicional, **[INFERÊNCIA]**).

---

### Lacunas declaradas
- Grade de placement normativa, densidade-alvo e limiares de quando ir para dois lados ou HDI: **sem número de fonte primária**.
- Como a JLC trata um conector que ultrapassa a borda numa placa com rail, e se os 2,5 mm valem com rail: **não encontrado**.
- Texto da IPC-7351 (courtyard A/B/C) não lido: valores **secundários**.
- Dev boards de referência (SparkFun, Adafruit, Flipper Wi-Fi devboard) não analisadas; o vídeo do Rick Hartley e os livros não foram consumidos.
- O conteúdo da ST AN2867 não foi lido (timeout).
- Conferência de URLs (2026-11-20, `curl`): todas as URLs citadas responderam 200, com três exceções. `klc.kicad.org` deu 403, que é desafio do Cloudflare: o site existe e o conteúdo foi lido pelo espelho do GitLab. `st.com` (AN2867) e `community.element14.com` (SN008) deram timeout; as duas apareceram em resultados de busca, mas não foram abertas.
