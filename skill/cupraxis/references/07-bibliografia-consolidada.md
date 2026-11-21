# Bibliografia consolidada (gerada automaticamente das seções `## Bibliografia` dos temas 01–06, 2026-11-20)

> Cada bloco é cópia literal da seção do tema; edições/anos de livros marcados "de memória" nos temas devem ser conferidos antes de citar.


---

## Do tema `01-floorplan-zoneamento.md`

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

---

## Do tema `02-energia-smps.md`

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

---

## Do tema `03-rf-antenas.md`

**Livros** (só citar; não baixar)
- Bowick, C.; Ajluni, C.; Blyler, J. *RF Circuit Design*, 2ª ed., Newnes/Elsevier, 2008. Redes de casamento L/π/T e Smith chart, de forma prática. Base para entender a π da Espressif e da TI.
- Pozar, D. M. *Microwave Engineering*, 4ª ed., Wiley, 2011. Linhas de transmissão (microstrip, CPW), casamento e S-parameters; referência acadêmica padrão.
- Balanis, C. A. *Antenna Theory: Analysis and Design*, 4ª ed., Wiley, 2016. Teoria de monopolo/IFA, campo próximo e distante, polarização.
- Wadell, B. C. *Transmission Line Design Handbook*, Artech House, 1991. Fórmulas fechadas de CPWG e microstrip usadas na memória de cálculo.
- **Correção do brief:** "Trilogy of Wireless" da Würth é *Trilogy of Wireless Power Transfer* (transferência de energia sem fio), **não** trata de antenas de comunicação. Não incluído como fonte. https://www.we-online.com/catalog/en/TRILOGY_WIRELESSPOWER

**Normas** (só citar)
- IPC-2141A, *Design Guide for High-Speed Controlled Impedance Circuit Boards*. Não lido; norma paga.
- ETSI EN 300 328 (2,4 GHz), EN 300 220-2 (SRD sub-GHz), EN 301 893 (5 GHz RLAN), EN 303 413 (GNSS), EN 301 489-1/-17 (EMC rádio): https://www.etsi.org/standards (gratuitas no site do ETSI; não baixadas, porque são grandes e o tema principal é layout).
- Diretiva RED 2014/53/UE: https://eur-lex.europa.eu/eli/dir/2014/53/oj · Regulamento Delegado (UE) 2022/30: https://eur-lex.europa.eu/eli/reg_del/2022/30/oj · Lista de normas harmonizadas, Decisão de Execução (UE) 2022/2191 (consolidada): https://eur-lex.europa.eu/eli/dec_impl/2022/2191/oj

**App notes e guias de fabricante** (baixados em `pdfs\03-rf\`, salvo indicação)
- Espressif, *ESP32-C5 / ESP32-S3 / ESP32-C3 Hardware Design Guidelines* (release master, baixados em 2026-11-20). https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c5/esp-hardware-design-guidelines-en-master-esp32c5.pdf (trocar `esp32c5` por `esp32s3`/`esp32c3`). Fonte principal de módulo, stackup, π, stub e keepout.
- TI AN058 *Antenna Selection Guide* (SWRA161B): https://www.ti.com/lit/an/swra161b/swra161b.pdf
- TI DN007 *2.4-GHz Inverted F Antenna* (SWRU120D): https://www.ti.com/lit/an/swru120d/swru120d.pdf
- TI AN043 *Small Size 2.4 GHz PCB antenna* (SWRA117D): https://www.ti.com/lit/an/swra117d/swra117d.pdf
- TI DN023 *868/915/955 MHz Inverted F Antenna* (SWRA228C): https://www.ti.com/lit/an/swra228c/swra228c.pdf
- TI AN074 *RemoTI Coexistence Testing* (SWRA285): https://www.ti.com/lit/an/swra285/swra285.pdf. Coexistência 802.15.4 × Wi-Fi em nível de protocolo; pouco valor para layout.
- u-blox *GNSS Antennas — RF design considerations* UBX-15030289 R03: https://content.u-blox.com/sites/default/files/products/documents/GNSS-Antennas_AppNote_%28UBX-15030289%29.pdf
- u-blox *GNSS interference* white paper: https://incremental-content.u-blox.com/sites/default/files/GNSS_Interference_white_paper_FINAL.PDF
- u-blox *NINA-B3 System Integration Manual* UBX-17056748 R15 (módulo nRF52840): https://content.u-blox.com/sites/default/files/NINA-B3_SIM_UBX-17056748.pdf
- Johanson Technology, *Chip Antenna Layout Considerations for 802.11 Applications* (2006): https://johansontechnology.com/docs/2/jti-antenna-mounting.pdf
- Kyocera AVX, *AppNote 1001013 Wi-Fi/Bluetooth PCB Antenna (On/Off Ground)*: https://www.kyocera-avx.com/docs/techinfo/ApplicationNotes/Antenna-AppNotes/AVX-E_AppNote-1001013.pdf
- ETSI EG 203 367 V1.1.1 (2016), RED para equipamentos multirrádio e combinados (módulos): https://www.etsi.org/deliver/etsi_eg/203300_203399/203367/01.01.01_60/eg_203367v010101p.pdf
- Já no acervo (não duplicado): TI DN017 e CC1101EM 434 MHz (`rf-reference-designs\cc1101-ti\`), u-blox MAX-M10S Integration Manual UBX-20053088 (`rf-reference-designs\max-m10s-ublox\`), Nordic nRF24L01 Product Spec v2.0 (`rf-reference-designs\nrf24l01-nordic\`).

**Fontes lidas on-line (não baixáveis ou HTML)**
- Silicon Labs, *Managed Coexistence* e *Unmanaged Coexistence*: https://docs.silabs.com/coexistence/latest/multiprotocol-wifi-coexistence-fundamentals/04-managed-coexistence · https://docs.silabs.com/coexistence/latest/multiprotocol-wifi-coexistence-fundamentals/03-unmanaged-coexistence
- Silicon Labs, *Z-Wave 800 Series Integration Guide — PCB Implementation*: https://docs.silabs.com/z-wave/8.0.0/z-wave-800-series-integration-guide/08-pcb-implementation
- Nordic DevZone, *General PCB design guidelines for nRF52 series* (página não mantida): https://devzone.nordicsemi.com/guides/hardware-design-test-and-measuring/b/nrf5x/posts/general-pcb-design-guidelines-for-nrf52-series
- Microchip, BM20/23 *Module Placement Rules*: https://onlinedocs.microchip.com/oxy/GUID-26060FFF-4EA0-483D-BCBB-39AF46A5A76C-en-US-6/GUID-3351AEE9-DDD5-4583-8492-53634B5FD77C.html
- Stavoli, Correia, Soubh, *Demystifying Edge Launch Connectors*, Signal Integrity Journal, 2019: https://www.signalintegrityjournal.com/articles/1094-demystifying-edge-launch-connectors
- JLCPCB: stackups de impedância https://jlcpcb.com/impedance · capacidades https://jlcpcb.com/capabilities/Capabilities · exemplo de calculadora (pergunta de usuário) https://jlcpcb.com/help/answers/detail/331-Coplanar-and-non-coplanar-Impedance-calculator
- Würth WE-SHC (catálogo): https://www.we-online.com/catalog/en/WE-SHC
- Espressif, certificados dos módulos (CE/RED, FCC etc.): https://www.espressif.com/en/support/documents/certificates

**Pedidas no brief, mas não acessíveis em 2026-11-20** (bloqueio a cliente automatizado; existem, conforme busca)
- Silicon Labs AN1088 *Designing with an Inverted-F 2.4 GHz PCB Antenna*: https://www.silabs.com/documents/public/application-notes/an1088-designing-with-pcb-antenna.pdf (403)
- Silicon Labs AN928.2 *EFR32 Series 2 Layout Design Guide*: https://www.silabs.com/documents/public/application-notes/an928.2-efr32-series2-layout-design-guide.pdf (403)
- Nordic nWP-017 *Antenna tuning* (v1.0, 2012) e nWP-008 *λ/4 printed monopole 2.45 GHz*: https://docs.nordicsemi.com/bundle/nwp_017/resource/nwp_017.pdf (Cloudflare); o endereço antigo infocenter redireciona para a página inicial.
- **AN2731 não é da Microchip:** é a *Compact Planar Antennas for 2.4 GHz Communication* da **NXP (ex-Freescale)**, Rev. 4, 11/2020. O link nxp.com (https://www.nxp.com/docs/en/application-note/AN2731.pdf) deu 404; espelhos não oficiais não foram usados.
- Würth ANR017 *GNSS Antenna Selection* (403); Ignion manuais mXTEND (Mouser 403); Hirose U.FL (403); Intel USB 3.0 RFI white paper (403).

**Ferramentas e calculadoras**
- JLCPCB Impedance Calculator: https://jlcpcb.com/pcb-impedance-calculator
- Saturn PCB Toolkit: https://saturnpcb.com/saturn-pcb-toolkit/
- Broadcom AppCAD: https://www.broadcom.com/info/wireless/appcad
- KiCad PCB Calculator (Transmission Lines): https://docs.kicad.org/9.0/en/pcb_calculator/pcb_calculator.html
- Cursos e vídeos: não pesquisados nesta rodada (lacuna).

---

## Do tema `04-gnd-si-emc-stackup.md`

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

---

## Do tema `05-componentes-conexoes.md`

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

---

## Do tema `06-shape-dfm-estetica.md`

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
