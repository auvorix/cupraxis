# 05: Componentes e conexões (escolha, sourcing, conectores, programação)

> Corpus de referência para a futura skill "especialista em projeto de PCB" (KiCad 10, JLCPCB; vale para qualquer PCB — produtos autônomos, RF/IoT, energia, periféricos, placas que encaixam em host).
> Pesquisa de 2026-11-20. PDFs locais em `pdfs\05-componentes\` (licenças em `pdfs\05-componentes\LICENSES.md`).
> **Etiquetas:**
> - **FATO**: conferido por mim na fonte primária, lida inteira ou no trecho citado.
> - **FATO-sec**: número tirado de uma fonte secundária ou de um resumo de busca. Não li o documento primário inteiro porque ele bloqueou robôs ou deu timeout. Confirmar antes de usar como regra dura.
> - **INFERÊNCIA**: dedução minha ou prática comum, sem fonte primária.

---

## Resumo executivo

1. **MLCC classe 2 (X5R/X7R) perde capacitância com tensão DC.** Na tabela da Nordic com dados Murata, um 0402 X7R de 6,3 V e 1 µF perde **40 %** a 3 V. Um 0402 X5R de 10 V e 4,7 µF perde **30 %**. Um de 100 nF perde só 3 %. Em rail de 3V3, escolher corpo maior e/ou tensão nominal maior e conferir a curva no SimSurfing ou no K-SIM. C0G/NP0 não sofre DC bias nem envelhecimento.
2. **MLCC trinca por flexão da placa.** Vishay: manter **≥ 5 mm da borda**, de preferência **paralelo à borda**, e longe de V-cut, furo de parafuso e conector THT. A trinca nasce na terminação e pode virar curto.
3. **Tântalo MnO₂ falha em curto e pode pegar fogo** com surto de baixa impedância. Usar a **50 % da tensão nominal** (Kyocera-AVX) ou trocar por polímero, alumínio-polímero ou MLCC. Na prática: em rail de 5 V/VBUS, tântalo MnO₂ não.
4. **Indutor de SMPS:** **Isat** (queda de L, definida em 10/20/30 % conforme o fabricante) limita o **pico**. **Irms** (aquecimento de +15 °C em indutor de chip e +40 °C em indutor de potência, na Coilcraft) limita a corrente **média/eficaz**. Conferir os dois com o pico real (I_out + ΔI/2) na temperatura máxima.
5. **Ferrite bead perde impedância com corrente DC.** Exemplo da ADI (FATO-sec): a 50 % da corrente nominal, uma bead de 100 Ω cai para 10 Ω em 100 MHz. Regra prática: operar em torno de **20 % da corrente nominal**.
6. **Cristal:** CL = C1·C2/(C1+C2) + Cs, com Cs ≈ **2–5 pF** (Microchip AN826) ou **2–3 pF** (ST). Margem de ganho gm/gm_crit **> 5** (ST AN2867, FATO-sec). Negative resistance **≥ 5–10× ESR** (Abracon). CI com capacitores de carga internos não leva os externos (erro 14 da casa).
7. **USB 2.0 HS:** proteção ESD com **< 4 pF** em D+/D− (TI). Para ter margem real no olho, **~0,5–1 pF** (onsemi: 6 pF já é inaceitável).
8. **Conectores:** escolher pela corrente por pino, pelos ciclos e pela retenção.
   - JST SH tem 1,0 mm de passo e 1 A. PH tem 2,0 mm e 2 A. GH tem 1,25 mm, 1 A e trava positiva. XH tem 2,5 mm e 3 A (JST).
   - Hirose DF40 faz só **30 ciclos**.
   - USB-C GCT USB4105: VBUS 5 A no total, demais pinos 0,25 A, 20 000 ciclos e **pernas THT na carcaça**.
9. **JLCPCB:** a FAQ lista **698** tipos de peça Basic. Na Economic, cada Extended paga **US$ 3,07** de feeder e a "Preferred Extended" é isenta. Na Standard é **US$ 1,53** por tipo, Basic ou Extended (página de 22/10/2026). Economic monta **≥ 0402**, passo de CI ≥ 0,4 mm e BGA ≥ 0,5 mm. Standard vai até 01005, passo 0,35 mm e BGA 0,3 mm.
10. **Ciclo de vida:** NRND ainda é vendável, mas é o primeiro sinal de EOL. Não projetar com NRND, LTB ou Obsolete. MSL 3 = **168 h** fora do saco a ≤ 30 °C/60 % UR; depois disso, bake.
11. **ESP32-C5 tem USB-Serial/JTAG nativo** (D+ = GPIO14, D− = GPIO13) que **entra em download sozinho**. O circuito de auto-boot com dois transistores (DTR/RTS) só é necessário atrás de uma ponte USB-UART.

---

## Regras acionáveis

### A. Encapsulamento de passivos (0201 / 0402 / 0603 / 0805)

1. **O padrão do programa é 0402 para sinal e desacoplamento até ~1 µF. Usar 0603/0805 para bulk (≥ 4,7 µF) e para potência ou tensão.**
   - Por quê: Economic PCBA da JLC só monta **≥ 0402**; 0201 e 01005 exigem Standard PCBA ([JLCPCB PCBA capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), FATO). Além disso, bulk em 0402 sofre muito DC bias (regra 9).
   - Retrabalho manual de 0201 é difícil (INFERÊNCIA, prática comum).
2. **A potência e a tensão máximas do resistor dependem da série, não só do tamanho. Ler o datasheet.**
   - Vishay CRCW e3 (thick film): **0402 = 0,10 W / 75 V; 0603 = 0,125 W / 75 V; 0805 = 0,25 W / 150 V; 1206 = 0,25 W / 200 V** (P70, a 70 °C). Tolerância ±1 % ou ±5 %. TCR ±100 ou ±200 ppm/K ([Vishay D/CRCW e3, doc 20035](https://www.vishay.com/docs/20035/dcrcwe3.pdf), FATO; PDF local).
   - Séries genéricas costumam ter valores menores: 0402 = 1/16 W e 0603 = 1/10 W (INFERÊNCIA; não verifiquei a Yageo RC porque o download falhou).
   - **Derating de projeto: dissipar ≤ 50 % do P70 na temperatura interna do produto** (INFERÊNCIA, prática comum). Acima de 70 °C a curva de derating do datasheet reduz a potência permitida.
3. **A tensão limite (Umax) conta tanto quanto a potência.** Divisor de alta tensão ou resistor de bleeder: somar a tensão sobre cada resistor e, se passar de ~50 % do Umax, colocar resistores em série.
   - Fonte: tabela Vishay acima (FATO). O critério de 50 % é INFERÊNCIA.
4. **Thin film versus thick film.**
   - Thin film: tolerância 0,1 %, TCR 25 ppm/K e menos ruído. Usar em referência de ADC, divisor de medição e ganho de amp-op.
   - Thick film: mais barato e mais robusto a pulso. Serve para todo o resto.
   - INFERÊNCIA (prática comum). O datasheet thin-film da Vishay não foi lido nesta rodada; está nas lacunas.
5. **Resistor que recebe pulso** (inrush, descarga de capacitor, snubber, sense de surto): usar série "pulse-proof" ou anti-surge e conferir a curva de energia de pulso do datasheet. INFERÊNCIA; não encontrei fonte primária lida.

### B. Capacitores cerâmicos (MLCC)

6. **Dielétrico por função:**
   - **C0G/NP0** em RF, casamento, carga de cristal, filtros, temporização e PLL.
   - **X7R** (−55 a +125 °C) ou **X5R** (−55 a +85 °C) em desacoplamento e bulk.
   - **Nunca Y5V/Z5U** em produto.
   - Por quê: C0G não tem DC bias nem envelhecimento ([Murata FAQ DC bias](https://www.murata.com/en-us/support/faqs/products/capacitor/mlcc/char/0005), FATO; [Würth SN011c](https://www.we-online.com/components/media/o189880v410%20SN011c%20EN.pdf), FATO, tabela "Aging: None" para classe 1).
   - Y5V: INFERÊNCIA (variação de +22/−82 % pela norma EIA). Não li a fonte nesta rodada.
7. **Envelhecimento da classe 2:** cerca de **2,5 %/década de horas para X7R** e **cerca de 6 %/década para X5R**. O reflow (> ~125 °C, a temperatura de Curie do BaTiO₃) **zera o envelhecimento**. Em projeto, o DC bias e a temperatura pesam mais que o envelhecimento ([Würth SN011c](https://www.we-online.com/components/media/o189880v410%20SN011c%20EN.pdf), FATO; PDF local).
8. **DC bias: consultar a curva SEMPRE que o capacitor for X5R/X7R ≥ 1 µF.** Dados Murata a 3 V de bias ([Nordic, Power Supply Decoupling Capacitor › DC bias](https://docs.nordicsemi.com/r/2Lg_vjNdr~1Jhm_V3QaJKQ/nANZT1UP6eq4Wxm0dBHTDA), FATO):

   | Peça Murata | Valor | Pacote | Diel. | V nom. | Perda a 3 V |
   |---|---|---|---|---|---|
   | GRM155R61A104KA01 | 100 nF | 0402 | X5R | 10 V | −3 % |
   | GRM155R61A105KE15 | 1 µF | 0402 | X5R | 10 V | −20 % |
   | GRM155R61A475MEAA | 4,7 µF | 0402 | X5R | 10 V | −30 % |
   | GRM155R70J105KA12 | 1 µF | 0402 | X7R | 6,3 V | **−40 %** |

   - Ferramentas: [Murata SimSurfing](https://ds.murata.com/simsurfing/) (as curvas são medidas com 50 % da tensão nominal durante 60 s, segundo o [PDF de condições de medida](https://ds.murata.com/simsurfing_data/pdf/en-us/mlcc/sim_mlcc_measuringcond_e.pdf), FATO), TDK SEAT/K-SIM e Samsung Electro-Mechanics Component Library.
   - Os links das ferramentas da TDK e da Samsung ficaram sem verificação de página.
9. **Regra prática para o rail de 3V3:** desacoplamento de 100 nF em 0402 X7R de 10–16 V está bem. **Bulk de 10–22 µF em 0603/0805 de 10 V ou mais**; nada de 10 µF em 0402 de 6,3 V. A capacitância efetiva tem de atender ao que o datasheet do regulador pede (ex.: "C_eff ≥ X µF").
   - INFERÊNCIA derivada da tabela acima.
10. **Trinca por flexão (flex cracking):**
    - Posicionar MLCC **a ≥ 5 mm da borda da placa** e **paralelo à borda**, com alívio fresado nas linhas de separação. Evitar quebrar painel à mão ([Vishay, "Coping with the Risk of Board Flexure Damage to MLCCs", doc 49088](https://www.vishay.com/docs/49088/49088_technicalpaper.pdf), FATO; PDF local).
    - A norma JIS C 5101-1 testa **2 mm de flexão num vão de 90 mm** (mesma fonte, FATO).
    - Manter MLCC longe de parafusos e de conectores THT (KEMET, FATO-sec, via resumo de busca do "Technical Overview of Flex Mitigation Solutions").
    - Em placa que leva parafuso, sofre torque de conector ou fica perto de um conector de encaixe (módulo plugável, HAT): usar **terminação flexível ou soft-termination**, ou **open-mode/floating electrode**, nos MLCC grandes (≥ 0805) de rails de energia (Vishay 49088, FATO, descreve as três abordagens).
    - Pads pequenos, com menos solda e filete menor, reduzem o estresse (Vishay 49088, FATO; KEMET, FATO-sec).
11. **MLCC grande (1206 ou maior) diretamente em VBUS/bateria sem fusível** cria risco de curto se trincar. Preferir dois capacitores menores, ou um open-mode, ou colocar um fusível/PTC antes (INFERÊNCIA, consequência da regra 10).

### C. Eletrolíticos, polímero e tântalo

12. **Tântalo MnO₂:** usar a **≤ 50 % da tensão nominal**. Por exemplo, um capacitor de 10 V só serve em rail de até 5 V.
    - Por quê: o modo de falha é curto. Sem limitação de corrente, o dielétrico rompe mais rápido do que o "self-healing" consegue isolar o defeito, e a peça vira um curto catastrófico ([Kyocera-AVX, rmtant.pdf](https://www.kyocera-avx.com/docs/techinfo/Tantalum-NiobiumCapacitors/rmtant.pdf), FATO; PDF local).
    - Na mesma fonte, um derating de 30 % dá ganho de cerca de 10× em confiabilidade (FATO).
    - "The voltage derating rules of 50 % should still be [followed]" ([Kyocera-AVX, Increasing reliability of SMD tantalum caps in low impedance apps](https://www.kyocera-avx.com/docs/techinfo/Tantalum-NiobiumCapacitors/increasing-reliability-SMD-tantalum-caps-low-impedance-apps.pdf), FATO; PDF local).
13. **Resistência série para tântalo:** a recomendação atual da Kyocera-AVX é **≥ 0,1 Ω por volt de trabalho** em regime. A regra antiga de 3 Ω/V é histórica (AVX "increasing reliability", FATO).
    - Rail de bateria ou VBUS com hot-plug não tem essa resistência. **Conclusão: tântalo MnO₂ fica proibido em VBUS, VBAT e entradas hot-plug** (INFERÊNCIA).
14. **Tântalo-polímero:** o derating é menor. Segundo a KEMET, é **10 % para ≤ 10 V e 20 % para > 10 V**; o MnO₂ continua com 50 % (FATO-sec, tutorial KEMET/DigiKey e artigo KEMET; páginas não abertas).
    - Pode falhar em curto, mas sem ignição (INFERÊNCIA).
15. **Eletrolítico de alumínio:** a vida dobra a cada 10 °C abaixo da temperatura nominal (regra de Arrhenius usada pelos fabricantes). Usar 105 °C e longe da SMPS. INFERÊNCIA; não li uma fonte primária nesta rodada.
16. **Escolha padrão em produto portátil 3V3/5V:** MLCC para quase tudo. Alumínio-polímero ou tântalo-polímero só quando for preciso bulk ≥ 100 µF com ESR baixo (INFERÊNCIA).

### D. Indutores (SMPS) e ferrites

17. **Indutor de potência:** escolher pelos dois números.
    - **Isat ≥ I_pico × 1,2–1,3** na temperatura máxima, com I_pico = I_out + ΔI_L/2.
    - **Irms ≥ I_out_rms.**
    - Definições da Coilcraft: Isat é a corrente em que L cai de uma porcentagem especificada. Irms é a corrente DC que eleva a temperatura em **15 °C (chip) ou 40 °C (potência)** acima de 25 °C. **Em alguns indutores Isat < Irms**, e então quem limita é o Isat ([Coilcraft Doc361](https://coilcraft.com/pdfs/Doc361_Current_Temp.pdf), FATO; PDF local).
    - O Doc469 mostra uma tabela com "Inductance drop = 30 % typ. at Isat" e definições de 10–20 % em outros casos ([Coilcraft Doc469](https://www.coilcraft.com/getmedia/d4009ece-69be-49a6-9185-9cbacb65e3aa/Doc469_selecting_inductors.pdf), FATO). **Comparar fabricantes só com o mesmo critério de queda.**
    - A margem de 1,2–1,3× é INFERÊNCIA.
18. **Indutor blindado ou semiblindado (molded/composite) é o padrão perto de RF.** O não blindado irradia campo do nó de chaveamento. Composite tem saturação "suave" (INFERÊNCIA; a Coilcraft só cita a opção "magnetically shielded for high density circuits", Doc469, FATO). Usar a série que o datasheet do regulador recomenda.
19. **Ferrite bead perde impedância com corrente DC.** Exemplo da ADI ("Ferrite Beads Demystified", Burket, Analog Dialogue 50-1, 2016; FATO-sec, o site deu timeout): a 50 % da corrente nominal, a impedância em 100 MHz cai de **100 Ω para 10 Ω** (TDK MPZ1608S101A, 3 A, 0603) e de **70 Ω para 15 Ω** (Würth 742 792 510, 6 A).
    - Diretriz da mesma fonte: usar a bead a **cerca de 20 % da corrente nominal**.
    - A corrente nominal é um limite térmico, não um ponto de operação para filtragem.
    - Fonte: [ADI Analog Dialogue](https://www.analog.com/en/resources/analog-dialogue/articles/ferrite-beads-demystified.html).
20. **Bead + capacitor forma um LC que pode ressoar e amplificar ruído** perto de f0 = 1/(2π√(LC)). Simular com o modelo SPICE do fabricante e, se precisar, amortecer com capacitor de ESR maior ou resistor série (ADI, mesma fonte, FATO-sec).
    - Vale para a regra da casa §7 de "bead + capacitor local por rádio".

### E. Cristais

21. **Carga do cristal:** CL = (C1·C2)/(C1+C2) + Cs ([Microchip AN826](https://ww1.microchip.com/downloads/en/AppNotes/00826a.pdf), FATO, PDF local; [Abracon, Quartz Crystal Glossary / Appendix A](https://abracon.com/Support/appendix-a.pdf), FATO, PDF local).
    - Cs (parasita de trilha + pino) fica entre **2 e 5 pF** segundo o AN826 (FATO). O artigo da ST põe **2–3 pF** e lembra que o C_IO de 5 pF do datasheet é pior caso ([ST KB "How to select a compatible crystal and load capacitors for STM32"](https://community.st.com/t5/stm32-mcus/how-to-select-a-compatible-crystal-and-load-capacitors-for-stm32/ta-p/780236), FATO).
    - **Com C1 = C2 = C: C = 2·(CL − Cs).** Exemplo: CL = 8 pF e Cs = 3 pF dão C = 10 pF (é o exemplo da ST: "Standard capacitor value in this case is 10 pF", FATO).
22. **Margem de oscilação (ST AN2867):**
    - gm_crit = 4·ESR·(2πF)²·(C0+CL)², calculado com os valores máximos do datasheet do cristal.
    - **Margem de ganho = gm_osc/gm_crit > 5.** Quando o datasheet do MCU traz "Gm_crit_max", vale gm_min = 5 × Gm_crit_max.
    - Fonte: [ST AN2867](https://www.st.com/resource/en/application_note/an2867-guidelines-for-oscillator-design-on-stm8afals-and-stm32-mcusmpus-stmicroelectronics.pdf), FATO-sec. O PDF da ST deu timeout e bloqueia curl; a relação 5× está confirmada no artigo da ST citado acima (FATO).
    - Exemplo (INFERÊNCIA, cálculo): 40 MHz, ESR 60 Ω, C0 2 pF e CL 10 pF dão gm_crit ≈ 2,2 mA/V. O oscilador precisa de ≥ 11 mA/V. **Cristal de ESR menor ou frequência menor melhora a margem.**
23. **Negative resistance:** medir colocando um resistor em série até a oscilação parar; −R = Ri + R1. **Recomendado −R ≥ 5 a 10× o ESR** ([Abracon Appendix A](https://abracon.com/Support/appendix-a.pdf), FATO).
24. **Drive level:** não exceder o máximo do datasheet do cristal. Excesso causa deriva e envelhecimento (AN826 e Abracon, FATO). Em 32,768 kHz, respeitar o modo de drive do RTC.
25. **CI com capacitores de carga internos** (FE1.1s, vários SoC de RF): **não colocar os externos**, ou usar só o valor de ajuste que o fabricante indicar. Somar os internos no cálculo da regra 21 (INFERÊNCIA, consistente com o erro 14 da casa).
26. **Layout:** capacitores de carga colados e simétricos, plano de GND contínuo embaixo, nenhuma trilha de sinal sob o cristal, trilhas curtas.
    - INFERÊNCIA, prática consolidada; o AN2867 traz isso, mas não consegui ler.
    - Cristal de 4 pads: eletrodos em 1/3 e GND em 2/4 (erro 12 da casa).

### F. LEDs, TVS/ESD e MOSFETs

27. **Resistor do LED:** R = (V_rail − V_F)/I_F. Por exemplo, (3,3 − 2,0)/5 mA = 260 Ω, que vira **270 Ω**. Para LED azul ou branco (V_F de ~2,8–3,2 V) em 3V3 a corrente fica instável. Usar 1–2 mA, que já basta para LED indicador moderno, ou alimentar por 5 V com transistor (INFERÊNCIA, lei de Ohm + V_F típico).
    - Ver a cor no esquemático **e** no campo LCSC.
28. **ESD em USB 2.0 High-Speed (480 Mbps):** diodo com **< 4 pF** em D+/D− ([TI SLVAF82B, §3.2](https://www.ti.com/document-viewer/lit/html/SLVAF82B/GUID-D4587727-15C3-460F-AF1D-D739F2DC3BE2), FATO).
    - No teste de olho da onsemi, 0,5 pF não altera o olho, **6 pF degrada demais** e 65 pF viola a máscara ([onsemi AND8319](https://www.onsemi.com/pub/Collateral/AND8319-D.PDF), FATO; PDF local).
    - **Alvo do programa: ≤ 1 pF** (ex.: classe TI ESD321/ESD401, 0,85–0,9 pF; FATO-sec). O diodo fica junto do conector, antes de qualquer outro componente (INFERÊNCIA).
    - Para VBUS, usar um TVS com tensão de trabalho ≥ 5,5 V (INFERÊNCIA).
29. **MOSFET acionado por GPIO de 3,3 V:** o critério é **R_DS(on) especificado em V_GS = 2,5 V (ou 1,8 V)**, não V_GS(th). O V_GS(th) é o ponto em que começa a conduzir (~250 µA), não o ponto de chaveamento pleno. Conferir também a SOA e o diodo de corpo (INFERÊNCIA, leitura padrão de datasheet). Não levantei nota de aplicação nesta rodada.

### G. CIs: encapsulamento para protótipo na JLC

30. **Preferir QFN/QFP/SOIC/SSOP. BGA só se não houver alternativa.**
    - JLC Economic aceita passo de CI **≥ 0,4 mm** e BGA **≥ 0,5 mm**. Standard aceita 0,35 mm e 0,3 mm ([JLCPCB PCBA capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), FATO).
    - QFN com pad exposto precisa de vias térmicas e de abertura de pasta segmentada. BGA não se retrabalha nem se inspeciona sem raio-X (INFERÊNCIA).
31. **Antes de rotear, conferir corpo, passo e largura entre pontas do terminal com o desenho mecânico do datasheet.** Na JLC, "SSOP-28" pode ser 150 mil ou 208 mil (erro 20 da casa).
    - **Pin 1:** o desenho do fabricante tem vista de cima ("top view") e land pattern recomendado; às vezes o land pattern vem em vista de baixo ("bottom view"). Espelhar errado troca a pinagem (INFERÊNCIA, causa clássica).
32. **Land pattern pela IPC-7351:** densidade A (most), B (nominal) e C (least). Para produto, o nível **B (nominal)** é o padrão. O C fica para densidade alta, e dificulta montagem e retrabalho ([JLCPCB blog Solder Pad Design](https://jlcpcb.com/blog/solder-pad-design-explained), FATO-sec; norma IPC-7351B/IPC-7352 só citada).
    - Quando o datasheet traz "recommended land pattern", ele vence a fórmula genérica (INFERÊNCIA).
33. **Modelo 3D STEP** de toda peça mecânica (conectores, botões, SMA, microSD, bateria) baixado do fabricante e alinhado ao footprint. Ele é usado no gate mecânico de borda (casa §12, erros 1–4) (INFERÊNCIA).

### H. Ciclo de vida e sourcing

34. **Status:**
    - **Active**: em produção.
    - **NRND**: em produção, sem data de obsolescência, mas não recomendado para projeto novo.
    - **Last Time Buy**: estoque limitado e final.
    - **Obsolete**: não se fabrica mais.
    - Fonte: [DigiKey, "Part Status: Obsolescence Process Explained"](https://forum.digikey.com/t/part-status-obsolescence-process-explained/10614), FATO.
    - **Projeto novo só com Active** (INFERÊNCIA). A JEDEC J-STD-048 prevê ≥ 6 meses do aviso até o LTB e ≥ 12 meses até a última entrega (FATO-sec, resumo de busca; norma só citada).
35. **Second source:** todo CI crítico (regulador, carregador, hub USB, LDO) com um equivalente pino-a-pino identificado no BOM, ou um footprint que aceite os dois. Passivos sempre por especificação, nunca por marca (INFERÊNCIA).
36. **JLCPCB Basic, Preferred Extended e Extended:**
    - A FAQ lista **698 tipos de Basic**: "frequently used parts like chip resistors, chip capacitors" ([JLCPCB PCB assembly FAQs](https://jlcpcb.com/help/article/pcb-assembly-faqs), FATO).
    - **Preferred Extended** são isentas da taxa de feeder na Economic (mesma fonte, FATO).
    - Tabela de preço de 22/10/2026: Economic **US$ 3,07 por tipo Extended**; Standard **US$ 1,53 por tipo**, Basic ou Extended ([JLCPCB PCB assembly price](https://jlcpcb.com/help/article/pcb-assembly-price), FATO). **Os valores mudam; conferir no pedido.**
    - A JLC aceita peças consignadas pelo cliente ("consign their own parts to our stock"; FAQ, FATO).
37. **MSL:** tempo máximo fora do saco seco a ≤ 30 °C, pela tabela J-STD-033 ([TI SPRABY1, Tabela 2-1](https://ti.com/lit/spraby1), FATO, conferida na página renderizada; PDF local):

    | MSL | 1 | 2 | 2a | 3 | 4 | 5 | 5a | 6 |
    |---|---|---|---|---|---|---|---|---|
    | Vida em fábrica | ilimitada (85 % UR) | 1 ano | 4 semanas | **168 h** | 72 h | 48 h | 24 h | bake antes e solda dentro do prazo do rótulo |

    - Estourou o prazo: **bake** conforme a J-STD-033, pela espessura do encapsulamento e pelo nível. O bake a 125 °C não serve para fita/bobina comum; a 40 °C leva cerca de 192 h ([JLCPCB MSL baking guide](https://jlcpcb.com/blog/moisture-sensitivity-level-msl-baking-guide), FATO).
    - Retrabalho de CI MSL ≥ 3 em placa montada: fazer bake antes (INFERÊNCIA).
38. **RoHS/REACH (produto na UE):** toda peça com declaração RoHS (2011/65/UE + 2015/863) e sem SVHC REACH acima de 0,1 % m/m. Guardar as declarações dos fabricantes no dossiê técnico da marcação CE (INFERÊNCIA; normas não lidas nesta rodada, ver lacunas).

### I. Conectores fio-placa (wire-to-board)

39. **Escolher pela tabela JST** (catálogos oficiais, FATO, PDFs locais):

    | Série | Passo | Corrente | Tensão | Fio | Temp. | Trava |
    |---|---|---|---|---|---|---|
    | **SH** | 1,0 mm | 1,0 A (AWG 28) | 50 V | AWG 32–28 | −25 a +85 °C | por atrito (INFERÊNCIA) |
    | **GH** | 1,25 mm | 1,0 A (AWG 26) | 50 V | AWG 30–26 | −40 a +105 °C | **trava positiva** ("secure lock", "large outer latch") |
    | **PH** | 2,0 mm | 2 A (AWG 24) | 100 V | AWG 32–24 | −40 a +105 °C | por atrito (INFERÊNCIA) |
    | **XH** | 2,5 mm | 3 A (AWG 22) | 250 V | AWG 30–22 | −25 a +85 °C | por atrito (INFERÊNCIA) |

    - Fontes: [JST SH](https://www.jst-mfg.com/product/pdf/eng/eSH.pdf), [JST GH](https://www.jst-mfg.com/product/pdf/eng/eGH.pdf), [JST PH](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf), [JST XH](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf).
    - **Produto que sofre vibração ou queda: GH (ou Molex PicoBlade/Pico-Lock) em vez de SH/PH** (INFERÊNCIA).
40. **Bateria LiPo com JST PH:** **a polaridade não é padronizada entre fornecedores de bateria.** Marcar "+" e "−" no silk, conferir com a bateria comprada e documentar o part number da bateria (INFERÊNCIA, problema notório em placas Adafruit/SparkFun; não achei fonte primária).
41. **Molex PicoBlade (1,25 mm):** cerca de 1 A por contato e **30 ciclos** (FATO-sec; datasheet da Molex não baixou). Micro-Fit 3.0 (3,0 mm, potência): corrente por circuito **não verificada** nesta rodada; ver o datasheet.
42. **Reduzir a corrente por pino** quando muitos pinos vizinhos conduzem ao mesmo tempo e quando o fio é mais fino que o do ensaio. A corrente do catálogo vale para o AWG indicado (o JST cita "AWG #24" etc., FATO). Para energia, usar ≥ 2 pinos em paralelo ou subir de série (INFERÊNCIA).

### J. Placa-placa (board-to-board), FPC e módulos

43. **Mezanino fino (Hirose DF40, 0,4 mm):** **0,3 A por contato, 30 V, só 30 ciclos de acoplamento** e 90 mΩ máx. depois do ensaio ([Hirose DF40C, catálogo 11/2013, cópia hospedada pela Adafruit](https://cdn-shop.adafruit.com/product-files/2227/ed_DF40_20140305-337786.pdf), FATO; PDF local). Catálogos mais novos da Hirose (FATO-sec) mantêm 0,3 A e 30 ciclos; a tensão varia entre 30 e 50 V conforme a edição.
    - **Não usar como conector de usuário.** Serve só para montagem fixa (INFERÊNCIA).
44. **Header de 2,54 mm** (expansão e protótipo) é robusto e THT. O de 1,27 mm economiza área, mas tem menos corrente e menos robustez. Header right-angle na borda segue o erro 7 da casa (direção do pino × pino 1) (INFERÊNCIA).
45. **FPC/FFC com ZIF:** lado dos contatos (top/bottom contact) **casado com o cabo**, atuador no lado acessível e pinagem espelhada conferida. Os ciclos costumam ser poucos (~20); ver o datasheet (INFERÊNCIA; nenhum datasheet ZIF lido).
46. **Castellated holes (módulo soldável) na JLC:**
    - Furo mínimo de **0,6 mm** (recomendado 0,8–1,0 mm). Espaço entre bordas de furos ≥ 0,6 mm (recomendado ≥ 0,8 mm).
    - Pad até a borda ≥ 1,0 mm. Furo até o canto da placa ≥ 3,0 mm (recomendado ≥ 5 mm).
    - Anel anular de 0,25 mm (mínimo absoluto 0,18 mm). Pad avançando ≥ 0,5 mm para dentro.
    - **ENIG recomendado** (obrigatório com slot ≥ 5 mm). Placa ≥ 10 × 10 mm; abaixo de 20 mm, panelizar.
    - Fonte: [JLCPCB blog, Castellated PCBs: Design Requirements](https://jlcpcb.com/blog/castellated-pcbs-introduction-and-design-requirements), FATO.
47. **Edge connector (gold fingers) na JLC:**
    - Chanfro de **30° ou 45°**; 30° é o recomendado. Não há chanfro em placa menor que 5 × 5 cm. Placa ou painel com gold fingers precisa ter ≥ 50 mm de lado. Área sem máscara. Ouro só com ENIG/ouro; HASL dá estanho.
    - Fonte: [JLCPCB help, Gold fingers](https://jlcpcb.com/help/article/jlcpcb-gold-fingers), FATO.
    - Profundidade do chanfro: L = (D/2 − T/2)/tan α (FATO-sec, resumo de outra página da JLC).
    - Para conector M.2, ver a especificação PCI-SIG/M.2 (só citar; não lida).

### K. USB-C, microSD, terminais e expansão

48. **Receptáculo USB-C só USB 2.0: usar o de 16 pinos.** O de 24 pinos só faz sentido com SuperSpeed ([Espressif, USB Type-C Hardware Design Guide](https://docs.espressif.com/projects/esp-iot-solution/en/latest/usb/usb_overview/usb_typec_hardware_guide.html), FATO).
    - Ligar A6 com B6 (D+) e A7 com B7 (D−) (Espressif, FATO).
    - **CC1 e CC2, cada um com seu 5,1 kΩ para GND** (sink/UFP). Não unir os CC nem omitir resistor, senão só uma orientação funciona ([Hackaday, "All About USB-C: Introduction For Hackers"](https://hackaday.com/2022/12/06/usb-c-introduction-for-hackers), FATO; Espressif, FATO).
    - Usar resistor de 1 % (Hackaday, FATO).
49. **Robustez mecânica do USB-C:** escolher um receptáculo com **pernas da carcaça THT** (shell stakes), não só SMD. Exemplo GCT USB4105:
    - Stakes de 0,60, 0,95 ou 1,20 mm conforme a espessura da placa.
    - Força de acoplamento de 5–20 N e durabilidade de **20 000 ciclos**.
    - **VBUS 5 A no total, GND 6,25 A, CC 1,25 A e 0,25 A nos demais pinos.**
    - Fonte: [GCT USB4105 drawing](https://gct.co/files/drawings/usb4105.pdf), FATO; PDF local, desenho marcado "confidential", não redistribuir.
    - Mid-mount (corpo afundado num recorte) reduz a altura, mas exige recorte em `Edge.Cuts` exatamente conforme o desenho (INFERÊNCIA).
    - **A boca do conector fica na linha da borda** (casa §5, erro 3).
50. **microSD:**
    - **Push-push** (ejeção por mola) é prático para o usuário, mas o mecanismo é complexo e pode "cuspir" ou prender o cartão.
    - **Hinge** (tampa articulada) segura melhor sob vibração e choque, porém costuma vir sem chave de detecção.
    - **Push-pull** é o mais simples e baixo.
    - Fonte: [Molex, "Smooth Operation for microSD Connectors"](https://experience.molex.com/smooth-operation-for-microsd-connectors), FATO-sec via resumo de busca; [DigiKey, memory card connectors](https://www.digikey.be/nl/articles/all-designers-need-to-know-about-memory-card-connectors), FATO.
    - **Para produto de bolso com carcaça: push-push com card-detect, boca na borda** (casa §5, erro 4) (INFERÊNCIA).
51. **Terminais de parafuso:** só para fio de campo (alimentação externa, sensores industriais). Passo 3,5/5,0/5,08 mm conforme a tensão e a corrente; pinos THT (INFERÊNCIA; nenhum datasheet lido).
52. **QWIIC / STEMMA QT:**
    - **JST SH de 4 pinos** (placa SM04B-SRSS-TB, cabo SHR-04V-S). Pinagem **GND, 3,3 V, SDA, SCL** (preto, vermelho, azul, amarelo). Qwiic exige que "Boards must be 3.3V" ([SparkFun Qwiic](https://www.sparkfun.com/qwiic), FATO).
    - O STEMMA QT da Adafruit segue a mesma pinagem, mas aceita **V+ de 3–5 V** e espera os **pull-ups no dispositivo** ([Adafruit STEMMA QT, Technical specs](https://learn.adafruit.com/introducing-adafruit-stemma-qt/technical-specs), FATO).
    - **Na placa host do programa: 3,3 V no pino 2, pull-ups de 2,2–4,7 kΩ com jumper/0 Ω para desabilitar**, e proteção contra curto no 3V3 do conector (INFERÊNCIA).

### L. Regras mecânicas gerais de conector

53. **Retenção:** todo conector que recebe força do usuário (USB-C, microSD, header de expansão, terminal, conector de bateria) precisa de **pinos ou abas THT ou abas SMD de ancoragem largas**. SMD puro arranca o pad (INFERÊNCIA; reforçada pela existência dos stakes no USB4105, FATO).
54. **Ciclos de inserção** acima do uso previsto, com margem de 2×. Exemplos: DF40 = 30 (só montagem fixa); USB-C ≥ 10 000 (INFERÊNCIA para o requisito; o USB4105 declara 20 000, FATO).
55. **Polarização (keying):** conector com carcaça polarizada (PH, GH, SH, XH e header box). Header sem trava com risco de inversão: pino de alimentação protegido contra inversão ou pino "chave" removido (INFERÊNCIA).
56. **Alívio de tensão do fio:** cabo preso na carcaça (abraçadeira, canal ou cola), nunca segurado só pela crimpagem (INFERÊNCIA).

### M. Programação e debug

57. **MCU com USB nativo (ESP32-C3/C5/S3):** o USB-Serial/JTAG põe o chip **em download automaticamente**, sem circuito DTR/RTS ([Espressif ESP-IDF, USB Serial/JTAG, ESP32-C5](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c5/api-guides/usb-serial-jtag-console.html), FATO). No C5, **D+ = GPIO14 e D− = GPIO13** (FATO).
    - **Manter o botão BOOT** (strap) e o RESET. Se a aplicação reconfigurar os pinos USB, o dispositivo some e a recuperação é manual. Em deep sleep ele também desconecta ([Espressif, mesma página para o C3](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-guides/usb-serial-jtag-console.html), FATO).
58. **MCU atrás de ponte USB-UART (CH340/CP210x) ou flashado por UART:** usar o auto-reset com dois transistores cruzados em DTR/RTS (EN↔RTS, GPIO0/boot↔DTR) e um **capacitor de 1–10 µF entre EN e GND** ([esptool, Boot mode selection](https://docs.espressif.com/projects/esptool/en/latest/esp32/advanced-topics/boot-mode-selection.html), FATO).
59. **MCU só SWD (STM32, nRF):** footprint **Tag-Connect TC2030** de 6 pads.
    - Desenho oficial da versão **NL (no legs)**: 6 pads condutores de **Ø 0,031″ (0,787 mm)** em passo de **0,050″ (1,27 mm)**, mais **3 furos de alinhamento não metalizados de Ø 0,039″ (0,991 mm)**.
    - Regras do mesmo desenho:
      - Nenhuma trilha ou via na área "KEEP OUT".
      - **Nenhum outro sinal a menos de 0,020″** de um pad.
      - **Sem pasta de solda nos pads**: não pode haver abertura no stencil. Se não der para evitar, fazer os pads THT com furo acabado ≤ 0,008″.
      - Marcar **DNL** no BOM.
      - O TC2030-CLIP prende o cabo pelos pinos de alinhamento, por baixo da placa.
    - Fonte: [Tag-Connect TC2030-IDC-NL Datasheet Rev B](https://www.tag-connect.com/wp-content/uploads/bsk-pdf-manager/2019/12/TC2030-IDC-NL-Datasheet-Rev-B.pdf), FATO; PDF local.
    - A versão com pernas (auto-retenção) tem furos extras de trava: [TC2030-IDC Datasheet Rev B](https://www.tag-connect.com/wp-content/uploads/bsk-pdf-manager/2019/12/TC2030-IDC-Datasheet-Rev-B.pdf), PDF local. **Decidir cedo, porque os footprints são diferentes.**
    - Os dois cabos têm a mesma área de ~0,02 pol², parecida com a de um 0805 (Microchip/Tag-Connect, FATO-sec).
    - Alternativa: header de debug Cortex de 10 pinos e 1,27 mm (INFERÊNCIA).
    - Ver o conflito com a casa §6 abaixo.

---

## Erros comuns

| Erro | Consequência | Correção |
|---|---|---|
| Bulk de 10 µF em 0402 de 6,3 V no rail de 3V3 | Capacitância efetiva cai 40–60 % (DC bias). Regulador instável ou ripple alto | Consultar a curva SimSurfing. Usar 0603/0805 de ≥ 10 V e conferir o C_eff exigido pelo regulador |
| X7R/Y5V em capacitor de carga de cristal ou de casamento RF | Frequência deriva com temperatura e tensão; casamento sai do lugar | Só C0G/NP0 |
| MLCC grande perto da borda, de V-cut, de furo de parafuso ou de conector de encaixe | Trinca por flexão: curto ou circuito aberto intermitente | ≥ 5 mm da borda, paralelo a ela. Soft-termination nos ≥ 0805 de potência |
| Tântalo MnO₂ em VBUS ou bateria hot-plug, ou com derating < 50 % | Curto e, eventualmente, ignição | Polímero (10–20 % de derating), alumínio-polímero ou MLCC |
| Indutor escolhido só pelo Irms (ou Isat de critério diferente entre marcas) | Satura no pico, a corrente dispara e o regulador entra em limite ou esquenta | Isat ≥ 1,2–1,3 × I_pico na temperatura máxima. Comparar com o mesmo % de queda |
| Ferrite bead escolhida pela impedância "100 Ω @ 100 MHz" com corrente próxima da nominal | Filtragem quase nula (100 → 10 Ω a 50 % de I_nom) | Corrente de trabalho ≈ 20 % da nominal. Usar a curva com bias |
| Cristal com C de carga = CL do datasheet (sem considerar Cs) ou com load caps externos em CI que já os tem | Frequência fora da tolerância; Wi-Fi/BLE/USB falham | C = 2(CL − Cs). Somar os capacitores internos (erro 14 da casa) |
| Cristal 2 pads em footprint de 4 pads (pinagem trocada) | Não oscila | Footprint 4-pin com GND em 2/4 (erro 12 da casa) |
| TVS genérico (≥ 6 pF) em D+/D− | Olho USB fecha; enumeração instável em HS | ESD ≤ 1 pF (máx. 4 pF) junto ao conector |
| Footprint escolhido pelo nome do pacote | O chip não assenta (SSOP-28 150 vs 208 mil) | Comparar com o desenho mecânico do datasheet ao gravar o LCSC (erro 20 da casa) |
| Pin 1 tirado de desenho em "bottom view" sem espelhar | Pinagem invertida | Conferir a vista indicada no desenho e o 3D |
| Projetar com peça NRND/LTB ou com estoque LCSC ≠ estoque JLC | Respin ou pedido travado | Só Active. Estoque confirmado na etapa de BOM do pedido (erro 21 da casa) |
| CI MSL 3 aberto por semanas e soldado sem bake | Popcorning e delaminação | Controlar as 168 h; bake conforme J-STD-033 |
| USB-C com um único 5,1 kΩ ou com CC1 e CC2 unidos | Só funciona numa orientação, ou o carregador não libera 5 V | Dois 5,1 kΩ independentes |
| USB-C ou microSD só SMD, sem perna THT | Pad arranca com o uso | Receptáculo com shell stakes THT |
| JST SH/PH sem trava num produto que cai ou vibra | Desconexão em campo | GH (trava positiva) ou fixar o cabo |
| Bateria JST PH de outro fornecedor com polaridade invertida | Carregador ou placa queimam | Silk +/−, conferir com a bateria real, documentar o part number |
| DF40 usado como conector de usuário | Contato degrada depois de 30 ciclos | Só montagem fixa; para o usuário, conector de ≥ 1 000 ciclos |
| Circuito de auto-boot DTR/RTS em ESP32 com USB nativo | Área e custo à toa | Usar o USB-Serial/JTAG. Manter só o botão BOOT/RESET |

---

## Checklist

**Passivos**
- [ ] Todo resistor com P_dissipada ≤ 50 % do P70 da série escolhida e tensão ≤ Umax
- [ ] Resistores de precisão (ADC, referência, divisor de medição) em thin film / 0,1 %
- [ ] RF, cristal e filtros: só C0G/NP0
- [ ] Todo X5R/X7R ≥ 1 µF com C_eff conferido na curva DC bias (SimSurfing/K-SIM) na tensão do rail
- [ ] Nenhum Y5V/Z5U no BOM
- [ ] MLCC ≥ 5 mm da borda e paralelo a ela. Soft-termination nos MLCC de potência ≥ 0805 em área de flexão
- [ ] Nenhum tântalo MnO₂ em VBUS/VBAT/entrada hot-plug; derating de 50 % (MnO₂) ou de 10–20 % (polímero)
- [ ] Indutor: Isat ≥ 1,2–1,3 × I_pico na temperatura máxima, Irms ≥ I_rms, blindado perto de RF
- [ ] Ferrite bead com I_trabalho ≈ 20 % de I_nominal; ressonância LC simulada ou amortecida

**Cristal**
- [ ] CL do cristal × C1/C2 calculados com Cs de 2–5 pF (e capacitores internos do CI)
- [ ] Margem de ganho gm/gm_crit > 5 (ST) ou −R ≥ 5–10× ESR (Abracon)
- [ ] Drive level dentro do máximo do cristal
- [ ] Footprint de 4 pads com GND correto; plano de GND sob o cristal, sem trilhas

**Semicondutores**
- [ ] LED com resistor calculado (I_F e V_F da cor real)
- [ ] ESD USB D+/D− ≤ 1 pF (máx. 4 pF), colado ao conector; TVS em VBUS
- [ ] MOSFET acionado por 3,3 V com R_DS(on) especificado em V_GS ≤ 2,5 V
- [ ] CIs em QFN/QFP/SOIC quando possível; passo ≥ 0,4 mm e BGA ≥ 0,5 mm (Economic) ou Standard PCBA decidida

**Footprint e modelo**
- [ ] Cada footprint conferido com o desenho mecânico do datasheet: corpo, passo, largura entre pontas, pin 1, vista
- [ ] Land pattern IPC-7351 nível B ou o recomendado pelo fabricante
- [ ] STEP de toda peça mecânica alinhado e conferido no 3D

**Sourcing**
- [ ] Todas as peças Active (sem NRND/LTB/Obsolete)
- [ ] Second source identificado para os CIs críticos
- [ ] Basic preferido; Extended contadas e custo de feeder avisado (Economic US$ 3,07 por tipo; Standard US$ 1,53 por tipo; conferir no pedido)
- [ ] Estoque de montagem confirmado no site da JLC (não no banco local)
- [ ] MSL de cada CI anotado; plano de bake se a montagem for manual
- [ ] Declarações RoHS/REACH arquivadas para o dossiê CE

**Conectores**
- [ ] Corrente por pino com margem (catálogo × AWG real × pinos simultâneos)
- [ ] Ciclos de inserção ≥ 2× o uso previsto
- [ ] Retenção THT/aba em todo conector manuseado pelo usuário
- [ ] Polarização ou keying; bateria com +/− no silk e conferida contra a bateria real
- [ ] USB-C de 16 pinos com shell stakes THT, dois 5,1 kΩ, D+/D− unidos, boca na borda
- [ ] microSD push-push com card-detect, boca na borda
- [ ] QWIIC: JST SH de 4 pinos, GND/3V3/SDA/SCL, pull-ups com jumper
- [ ] Castellated (se módulo): furo ≥ 0,6 mm (ideal 0,8–1,0), ≥ 3 mm do canto, ENIG
- [ ] Gold fingers (se houver): chanfro de 30°, placa ≥ 50 mm, ENIG

**Programação**
- [ ] MCU com USB nativo: USB-Serial/JTAG ligado ao hub/USB-C, botão BOOT e RESET acessíveis
- [ ] MCU atrás de ponte UART: auto-reset DTR/RTS + capacitor de 1–10 µF em EN
- [ ] MCU só SWD: footprint TC2030 (NL ou com pernas, decidido) conferido contra o PDF oficial

---

## Conflitos com PADROES-PROJETO-PCB.md

| Seção da casa | Situação | Detalhe |
|---|---|---|
| **§6, auto-boot** ("prever o circuito de auto-boot... dois MOSFET-N cruzados") | **Diverge parcialmente** | O ESP32-C5 tem USB-Serial/JTAG nativo (D+ GPIO14 / D− GPIO13) que **entra em download sozinho** (Espressif, FATO). Se o C5 for ligado pelo USB nativo ao hub, **o circuito de dois transistores é desnecessário**. Ele só é necessário com ponte USB-UART ou flash pelo UART de um host. Manter o botão BOOT (recuperação manual se o app reconfigurar os pinos USB; deep sleep derruba a USB). |
| **§6, "elimina headers e test pads"** | **Diverge para MCU sem USB** | Em MCU só SWD (STM32 e nRF sem USB) a prática profissional é um **footprint Tag-Connect TC2030-NL** (~0,02 pol², sem conector montado). Não é "gambiarra". Decisão do dono: admitir TC2030 como exceção para MCU sem USB. |
| **§16, "cada Extended custa ~US$ 3"** | **Confirma com nuance** | A página atual (22/10/2026) traz Economic **US$ 3,07 por tipo Extended** e Standard **US$ 1,53 por tipo, Basic ou Extended**. A casa não menciona as **"Preferred Extended"**, isentas da taxa na Economic. A FAQ lista **698** tipos Basic. Também: a Economic **não monta 0201** (mínimo 0402). |
| **§16, "CL ≈ C/2 + ~2–3 pF"** | **Confirma** | ST KB: 2–3 pF. AN826: 2–5 pF. Acrescentar: somar a capacitância de pino/interna do CI (Abracon e Microchip) e conferir a margem gm/gm_crit > 5 (AN2867) ou −R ≥ 5–10× ESR. |
| **§16, "RF só C0G/NP0"** | **Confirma** | Murata e Würth: C0G sem DC bias e sem envelhecimento. |
| **§14, USB-C com dois 5,1 kΩ independentes** | **Confirma** | Hackaday e Espressif. Acrescentar: resistor de 1 %, receptáculo de 16 pinos, D+/D− A6-B6/A7-B7 unidos, **shell stakes THT**. |
| **§13 erros 12–14, cristal** | **Confirma** | AN826 e Abracon. Erro 14 (load caps internos): consistente com a fórmula, porque o interno já entra no CL. |
| **§13 erro 20, footprint pelo nome** | **Confirma e amplia** | Acrescentar pin 1 em vista de cima × de baixo, land pattern IPC-7351 nível B e STEP do fabricante. |
| **§13 erro 21, estoque LCSC × JLC** | **Confirma** | Não há fonte contrária. Acrescentar: peças consignadas ("consign") e Global Sourcing como alternativa oficial (FAQ JLC). |
| **§8, QWIIC (JST-SH)** | **Confirma com nuance** | Qwiic exige 3,3 V; STEMMA QT aceita 3–5 V e espera pull-ups no dispositivo. Definir o 3V3 no pino 2 e pull-ups com jumper (a casa não especifica). |
| **§7, "ferrite bead + capacitor local por rádio"** | **Confirma com alerta** | A bead perde impedância com DC (ADI: 100 → 10 Ω a 50 % de I_nom) e o LC pode ressoar. **Falta na casa:** dimensionar a bead para cerca de 20 % de I_nom e checar ou amortecer a ressonância. |
| **§5, borda** | **Confirma** | Datasheets de USB-C e microSD definem a posição pela `PCB Edge`. |
| **Falta na casa** | **Falta** | (a) MLCC a ≥ 5 mm da borda e paralelo (Vishay). (b) DC bias em X5R/X7R ≥ 1 µF. (c) Proibir tântalo MnO₂ em VBUS/VBAT. (d) Isat × Irms do indutor do buck-boost. (e) ESD USB ≤ 1 pF (máx. 4 pF). (f) Polaridade da bateria JST PH. (g) Só peças Active e second source. (h) MSL e bake em montagem manual. (i) Retenção THT e ciclos de inserção dos conectores. (j) DF40 só para montagem fixa. |

---

## Bibliografia

### Livros (só citar)
- Horowitz, P.; Hill, W. **The Art of Electronics**, 3ª ed., Cambridge University Press, 2015. Capítulo 1 e apêndices sobre componentes passivos reais (tolerância, tipos de capacitor, indutores, cristais). É a referência prática de escolha de componente. Não baixar; comprar.
- Ott, H. W. **Electromagnetic Compatibility Engineering**, Wiley, 2009. Comportamento real de capacitores, ferrites e desacoplamento. Só citar.

### Normas (só citar, não baixar)
- IPC-7351B / IPC-7352: land patterns (níveis de densidade A/B/C).
- IPC/JEDEC J-STD-020 (classificação MSL) e J-STD-033 (manuseio, armazenamento, bake).
- JEDEC J-STD-048: notificação de descontinuação (PCN/LTB).
- JIS C 5101-1: ensaio de flexão de MLCC (2 mm em 90 mm).
- USB Type-C Cable and Connector Specification R2.x (usb.org).
- EIA-198 / IEC 60384: códigos de dielétrico (X7R, C0G...).
- Diretivas UE 2011/65/UE + 2015/863 (RoHS) e Regulamento 1907/2006 (REACH).

### App notes, datasheets e catálogos (✓ = PDF local em `pdfs\05-componentes\`)
- ✓ Microchip **AN826**, Crystal Oscillator Basics and Crystal Selection for rfPIC and PICmicro Devices: https://ww1.microchip.com/downloads/en/AppNotes/00826a.pdf
- ✓ Abracon, **Quartz Crystal Glossary of Terms / Appendix A** (CL, −R ≥ 5–10× ESR): https://abracon.com/Support/appendix-a.pdf
- ST **AN2867**, Guidelines for oscillator design on STM8/STM32: https://www.st.com/resource/en/application_note/an2867-guidelines-for-oscillator-design-on-stm8afals-and-stm32-mcusmpus-stmicroelectronics.pdf (não baixou: bloqueia curl e deu timeout; baixar pelo navegador)
- ST Community KB, How to select a compatible crystal and load capacitors for STM32: https://community.st.com/t5/stm32-mcus/how-to-select-a-compatible-crystal-and-load-capacitors-for-stm32/ta-p/780236
- ✓ Vishay **doc 49088**, Coping with the Risk of Board Flexure Damage to MLCCs: https://www.vishay.com/docs/49088/49088_technicalpaper.pdf
- ✓ Vishay **D/CRCW e3**, Standard Thick Film Chip Resistors (doc 20035): https://www.vishay.com/docs/20035/dcrcwe3.pdf
- ✓ Würth Elektronik **SN011c**, Why does the capacitance of MLCCs change? Aging: https://www.we-online.com/components/media/o189880v410%20SN011c%20EN.pdf
- ✓ Murata, SimSurfing MLCC measuring conditions: https://ds.murata.com/simsurfing_data/pdf/en-us/mlcc/sim_mlcc_measuringcond_e.pdf
- Murata FAQ, DC bias characteristics: https://www.murata.com/en-us/support/faqs/products/capacitor/mlcc/char/0005
- Nordic, Power Supply Decoupling Capacitor › DC bias (tabela Murata): https://docs.nordicsemi.com/r/2Lg_vjNdr~1Jhm_V3QaJKQ/nANZT1UP6eq4Wxm0dBHTDA
- KEMET (Yageo), Technical Overview of Flex Mitigation Solutions (hospedado na Mouser): https://www.mouser.com/pdfdocs/TechnicalOverviewofFlexMitigationSolutions.pdf (não baixou: Mouser bloqueia curl)
- ✓ Kyocera-AVX, **Reliability of tantalum capacitors** (rmtant): https://www.kyocera-avx.com/docs/techinfo/Tantalum-NiobiumCapacitors/rmtant.pdf
- ✓ Kyocera-AVX, **Increasing reliability of SMD tantalum capacitors in low impedance applications**: https://www.kyocera-avx.com/docs/techinfo/Tantalum-NiobiumCapacitors/increasing-reliability-SMD-tantalum-caps-low-impedance-apps.pdf
- KEMET, 2004 CARTS Europe, Derating Differences (MnO₂ 50 %, polímero 20 %): https://www.kemet.com/content/dam/kemet/lightning/obsolete/technical-archive/2004-CARTS-Europe-Derating-Differences.pdf (**404 em 2026-11-20**: a KEMET migrou para yageogroup.com; o link veio da busca e não existe mais. Procurar o documento no site da Yageo)
- ✓ Coilcraft **Doc361**, Current and Temperature Ratings: https://coilcraft.com/pdfs/Doc361_Current_Temp.pdf
- ✓ Coilcraft **Doc469**, Selecting the Best Inductor for Your DC-DC Converter: https://www.coilcraft.com/getmedia/d4009ece-69be-49a6-9185-9cbacb65e3aa/Doc469_selecting_inductors.pdf
- ADI Analog Dialogue, **Ferrite Beads Demystified** (C. Burket, 2016): https://www.analog.com/en/resources/analog-dialogue/articles/ferrite-beads-demystified.html (não baixou: timeout)
- TI **SLVAF82B**, ESD para USB 2.0 (< 4 pF): https://www.ti.com/document-viewer/lit/html/SLVAF82B/GUID-D4587727-15C3-460F-AF1D-D739F2DC3BE2
- ✓ onsemi **AND8319**, ESD protection for USB 2.0, signal integrity (olho com 0,5 / 6 / 65 pF): https://www.onsemi.com/pub/Collateral/AND8319-D.PDF
- ✓ TI **SPRABY1B**, MSL Ratings and Reflow Profiles: https://ti.com/lit/spraby1
- ✓ JST, catálogos **SH** (https://www.jst-mfg.com/product/pdf/eng/eSH.pdf), **GH** (https://www.jst-mfg.com/product/pdf/eng/eGH.pdf), **PH** (https://www.jst-mfg.com/product/pdf/eng/ePH.pdf), **XH** (https://www.jst-mfg.com/product/pdf/eng/eXH.pdf)
- ✓ Hirose **DF40C** (catálogo 11/2013, cópia hospedada pela Adafruit): https://cdn-shop.adafruit.com/product-files/2227/ed_DF40_20140305-337786.pdf. Página oficial: https://www.hirose.com/product/series/DF40?lang=en (bloqueia robôs)
- ✓ GCT **USB4105**, USB Type-C receptacle USB 2.0, desenho: https://gct.co/files/drawings/usb4105.pdf
- ✓ Tag-Connect, **TC2030-IDC-NL Datasheet Rev B** (footprint sem pernas): https://www.tag-connect.com/wp-content/uploads/bsk-pdf-manager/2019/12/TC2030-IDC-NL-Datasheet-Rev-B.pdf
- ✓ Tag-Connect, **TC2030-IDC Datasheet Rev B** (footprint com pernas): https://www.tag-connect.com/wp-content/uploads/bsk-pdf-manager/2019/12/TC2030-IDC-Datasheet-Rev-B.pdf. Índice de documentos: https://www.tag-connect.com/technical
- Espressif, USB Type-C Hardware Design Guide: https://docs.espressif.com/projects/esp-iot-solution/en/latest/usb/usb_overview/usb_typec_hardware_guide.html
- Espressif, USB Serial/JTAG console (ESP32-C5): https://docs.espressif.com/projects/esp-idf/en/latest/esp32c5/api-guides/usb-serial-jtag-console.html e (ESP32-C3): https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-guides/usb-serial-jtag-console.html
- Espressif esptool, Boot mode selection: https://docs.espressif.com/projects/esptool/en/latest/esp32/advanced-topics/boot-mode-selection.html

### Fabricante (JLCPCB)
- PCBA capabilities: https://jlcpcb.com/capabilities/pcb-assembly-capabilities
- PCB assembly FAQs (Basic, Preferred Extended, Extended, consignação): https://jlcpcb.com/help/article/pcb-assembly-faqs
- PCB assembly price (taxa de feeder): https://jlcpcb.com/help/article/pcb-assembly-price
- Castellated PCBs, design requirements: https://jlcpcb.com/blog/castellated-pcbs-introduction-and-design-requirements
- Gold fingers: https://jlcpcb.com/help/article/jlcpcb-gold-fingers
- MSL baking guide: https://jlcpcb.com/blog/moisture-sensitivity-level-msl-baking-guide
- Solder pad design (IPC-7351): https://jlcpcb.com/blog/solder-pad-design-explained

### Guias de comunidade e distribuidores
- Hackaday, All About USB-C: Introduction For Hackers (2022): https://hackaday.com/2022/12/06/usb-c-introduction-for-hackers
- SparkFun Qwiic: https://www.sparkfun.com/qwiic
- Adafruit STEMMA QT, Technical specs: https://learn.adafruit.com/introducing-adafruit-stemma-qt/technical-specs
- DigiKey, Part Status, Obsolescence Process Explained: https://forum.digikey.com/t/part-status-obsolescence-process-explained/10614
- DigiKey, All Designers Need to Know About Memory Card Connectors: https://www.digikey.be/nl/articles/all-designers-need-to-know-about-memory-card-connectors
- Molex, Smooth Operation for microSD Connectors: https://experience.molex.com/smooth-operation-for-microsd-connectors

### Ferramentas e calculadoras
- Murata SimSurfing (curvas DC bias e impedância de MLCC e ferrites): https://ds.murata.com/simsurfing/
- Würth REDEXPERT (indutores, ferrites, MLCC): https://redexpert.we-online.com/
- Banco local da JLC (casa §16): `%USERPROFILE%\.kicad-mcp\data\jlcpcb_parts.db` + `referencias\scripts-bom\jlc_query.py`

### Lacunas (não pesquisadas a fundo ou sem fonte primária lida nesta rodada)
- Y5V/Z5U (números exatos); thin film × thick film com datasheet Vishay/Susumu; resistores anti-pulso (curva de energia).
- MOSFET para 3,3 V (nota de aplicação Nexperia/Infineon); LED (datasheet de LED 0603 da LCSC).
- FPC/ZIF (ciclos, contato top/bottom), pogo pins, M.2 (especificação), Micro-Fit 3.0 (corrente por circuito), terminais de parafuso.
- STEP: fontes oficiais por fabricante. RoHS/REACH: texto das diretivas.
- ST AN2867, ADI Ferrite Beads e KEMET flex/tantalum existem, mas bloquearam o download. **Baixar manualmente** para `pdfs\05-componentes\`.
- Verificação de URLs (2026-11-20, curl):
  - **200 em todas**, com estas exceções:
    - Bloqueiam robôs, mas a página existe: Nordic docs (403), DigiKey.be (403), Würth SN011c (403 no curl; o conteúdo foi lido via WebFetch).
    - Timeout: analog.com e st.com.
    - 301 (redireciona): Molex experience.
    - **404 (morta):** KEMET 2004 CARTS.
- Samsung Electro-Mechanics e TDK (ferramentas DC bias): links das ferramentas não conferidos.
