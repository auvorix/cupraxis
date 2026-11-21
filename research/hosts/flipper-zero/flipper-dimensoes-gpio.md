# Flipper Zero: dimensoes, GPIO, esquematico da devboard Wi-Fi e circuito de auto-boot

> **`[FLIPPER]` — pesquisa baseada na documentação oficial da Flipper Devices.** Conteúdo específico do Flipper Zero; aplicar **somente** a placas que encaixam nesse aparelho. Não é regra geral de PCB (para isso: `../../PADROES-PROJETO-PCB.md` e `../../boas-praticas/`).


Pesquisa de 2026-11-19. Convencao: **FATO** = verificado em fonte/arquivo citado; **INFERENCIA** = deducao minha, validar. Nada de cota inventada: o que nao foi achado esta em "Lacunas".

Arquivos de referencia salvos em `docs/ref/` (todos < 6 MB):
- `flipper-zero-body-2d.pdf` (desenho oficial 2D do corpo; GPL-3.0, ver `flipper-3d-LICENSE-GPL3.txt`), `flipper-zero-drawing.png` (preview legivel do mesmo desenho), `flipper-zero-body-3d.stl` (2,1 MB, corpo SEM capa).
- `flipper-wifi-devboard-v1-schematic.pdf` (esquematico Flipper Devices "WI-FI Module V1", Rev V1, 22.01.2022, 4 folhas), `flipper-wifi-devboard-pinout.png` (pinagem oficial da devboard), `flipper-wifi-devboard-autoboot-crop.png` (recorte do circuito de BOOT/EN, folha 2).

## 1. Dimensoes do Flipper Zero

### Corpo (sem capa)
| Medida | Valor | Fonte |
|---|---|---|
| Comprimento | 100,3 mm | FATO: `flipper-zero-body-2d.pdf` (cota entre parenteses = de referencia) e docs.flipper.net/zero/development/hardware/tech-specs |
| Largura (altura de tela) | 40,1 mm | idem |
| Espessura | 25,6 mm | idem |
| Peso | 102 g | FATO: tech-specs (sem capa; a pagina nao diz se inclui bateria, e a bateria e de 2100 mAh LiPo) |
| Caixa do STL | 100,30 x 40,09 x 25,60 mm | FATO: medido por mim nos vertices de `flipper-zero-body-3d.stl` (binario, 43 386 triangulos); confere com o desenho |
| Temperatura de operacao | 0 a 40 C | FATO: tech-specs |

### Regiao do GPIO (aresta superior, vista do desenho 2D)
FATO (cotas de `flipper-zero-body-2d.pdf`):
- Duas fileiras de furos/soquetes de 1 linha cada, passo 2,54 mm: grupo de 8 (pinos 1-8) e grupo de 10 (pinos 9-18).
- Entre o centro do pino 8 e o centro do pino 9: 17,78 mm.
- Do centro do pino 18 ate a ponta (extremo) direita do corpo: 19,24 mm.
- Linha central dos pinos a 14,75 mm de uma das faces (a face "plana" do desenho lateral, a de cima da vista; **qual face e a frontal da tela nao esta rotulado na cota**, ver Lacunas).
- Espessura total 25,6 mm.

INFERENCIA (calculada a partir das cotas acima, consistente com o desenho do modulo externo):
- Pino 1 fica a 100,3 - 19,24 - 22,86 - 17,78 - 17,78 = **22,64 mm** da ponta esquerda (vista frontal, ponta biselada a esquerda). Pino 18 a 19,24 mm da ponta direita.
- A PCB do modulo (67,34 mm) fica com a borda esquerda a ~18,17 mm e a direita a ~85,51 mm da ponta esquerda: folga lateral ~18 mm de cada lado. Confere com o pino 1 em x = 4,47 mm da borda da PCB (gpio.md) e pino 18 a ~4,45 mm da borda direita.

### Altura util acima do topo
FATO: o desenho oficial do modulo (`flipper-external-module-drawing.pdf`) fixa a PCB em 67,34 x **20 mm** (entre parenteses), espessura recomendada 1,0 a 1,2 mm, furos a 3,84 mm da borda inferior, abas de 2,6 mm de profundidade, entalhe de 14,86 mm, comprimento de encaixe do pino ("pin match length") 6 mm, header angulo reto 8 pinos L=17,78 e 10 pinos L=22,86, corpo do header 2,54 mm, furos de 0,9 mm.
INFERENCIA: com a linha de furos alinhada a superficie do topo, a PCB sobressai ~20 - 3,84 = **16,2 mm** acima do topo do Flipper (medi ~15,4 mm direto na vista frontal do desenho; o arredondamento do grafico explica a diferenca). Tratar **~15-16 mm** como altura util da placa acima do Flipper, incluindo componentes que fiquem da face de fora. Os componentes ficam a uma espessura de placa de distancia do corpo: o desenho da secao A-A mostra a PCB dentro do contorno da capa, sem folga lateral para componentes altos.

### Com capa de silicone
- FATO (docs.flipper.net/zero/gpio-and-modules): com capa, inserir o modulo ate **nao haver vao no meio entre a capa e o modulo**; sem capa, encaixar tudo, sem vao entre Flipper e modulo (pode precisar de forca). Os pinos do modulo nao devem ficar visiveis depois de inserido.
- FATO: o desenho do modulo externo (secao B-B) mostra a capa de silicone envolvendo o topo, e o modulo apoiado sobre ela. Nao ha cota de espessura de parede da capa nele.
- Peso e medidas da capa oficial: **nao achei em fonte oficial**. So listagem de revendedor (Desertcart, part FLP-A-CASE-OR): 10,4 x 4,4 x 2,9 cm e 23 g (outra listagem diz 28 g). Baixa confianca. Se for usar, medir a capa real: INFERENCIA fraca de ~1,7 mm por lado (104-100,3)/2 e (44-40,1)/2, so como ordem de grandeza.

## 2. GPIO oficial

Fontes: docs.flipper.net/zero/gpio-and-modules (texto), imagens oficiais ja em `docs/ref/` (`flipper-gpio-pinout.jpg`, `flipper-gpio-schematic.jpg`), firmware `targets/f7/furi_hal/furi_hal_resources.c` (branch dev, flipperdevices/flipperzero-firmware).

### FATO: limites eletricos (texto da doc)
- 18 pinos no topo, divididos em alimentacao e I/O. I/O em **3,3 V**, e o MCU e o STM32WB55.
- I/O ligam ao MCU **por resistores de 51 ohm em serie** e todos os pinos tem **protecao ESD**.
- Cada pino I/O fornece ate **20 mA**. Consumo total dos pinos I/O: **max 5 W**; acima disso a bateria pode entrar em modo protecao e o Flipper desligar.
- **3,3 V (pino 9)**: habilitado por padrao, carga maxima **1,2 A**. A doc o descreve como a alimentacao do microSD e diz que ele e **desligado temporariamente durante atualizacao de firmware e ao montar o microSD**.
- **5 V (pino 1)**: carga maxima **1,2 A**. Com bateria fica **desligado** por padrao; liga em Main Menu > GPIO > "5V on GPIO" = ON. Com USB conectado, o pino 1 recebe o 5 V direto do USB (sem passo de habilitacao descrito). "Nunca exceder 1,2 A".
- Pino configurado como **entrada** e tolerante a 5 V; como **saida**, nao. Evitar periferico I/O 5 V.
- Carga capacitiva grande ligada com o Flipper ligado pode corromper o microSD: conectar so com ele desligado.
- Tech-specs: "13 pinos I/O para o usuario", nivel 3,3 V CMOS, entradas 5 V tolerantes, 20 mA por pino digital, carga USB max 1 A.
- A doc nao traz tabela de funcoes em texto (so imagem). A funcao por pino abaixo vem das imagens oficiais + firmware.

### FATO: mapa de pinos (firmware `furi_hal_resources.c`, campo `.number`)
| Pino | MCU | Observacao |
|---|---|---|
| 1 | 5V | OTG ligado pelo menu |
| 2 / 3 / 4 / 5 | PA7 / PA6 / PA4 / PB3 | GPIO livres (PA7 PWM TIM1, PA4 PWM LPTIM2; PA7/PA6/PA4 ADC); pinagem oficial os marca como SPI |
| 6 | PB2 | GPIO livre, sem ADC |
| 7 | PC3 | GPIO livre, ADC4 |
| 8, 11, 18 | GND | |
| 9 | 3V3 | |
| 10 | PA14 (SWCLK) | marcado debug no firmware |
| 12 | PA13 (SWDIO) | marcado debug |
| 13 | PB6 USART1 TX | |
| 14 | PB7 USART1 RX | |
| 15 | PC1 | ADC2; LPUART TX |
| 16 | PC0 | ADC1; LPUART RX |
| 17 | PB14 (iButton) | pull-up de 1 kohm a 5 V na placa (ja em gpio.md): nao ligar |

- **UART**: 13/14 = USART1 (TX no 13, RX no 14: cruzar com o dispositivo). 15/16 = LPUART (na devboard, esquematico folha 4: LPUART_TX no pino 15, LPUART_RX no 16). Confirma gpio.md.
- **I2C**: a devboard oficial liga os pinos 15 e 16 a SDA e SCL (pinagem oficial: pino 15 = IO18 SDA, pino 16 = IO17 SCL), com pull-ups de 10 kohm chaveados por MOSFET (folha 4, R6/R8/R9/R10/VT1/VT2). O Flipper nao tem pull-up de I2C no GPIO: o modulo deve te-los.
- **SPI**: pinos 2-5 (PA7 MOSI, PA6 MISO, PA4 CS, PB3 SCK, funcoes STM32 padrao). A figura da devboard rotula o pino 4 como SCK e o 5 como CS/SWO (invertido em relacao a funcao nativa dos pinos): INFERENCIA, conferir antes de depender de SPI; nao e usado no AirScope.
- **PB2 e PC3 NAO estao ligados a NFC nem ao botao OK**: FATO no firmware. O NFC usa PE4 (CS) e PA2 (IRQ/pull RFID); o botao OK e PH3; PB13/PB14/PA0/PB9 = RFID/iButton/IR. PB2 e PC3 sao GPIO livres expostos so no header. A suposicao de "PB2 com NFC / PC3 com botao OK" **nao se sustenta**.
- Uso real de PB2/PC3: no app **ESP Flasher** (0xchocolate/flipperzero-esp-flasher, `esp_flasher_worker.c`) PC3 = DTR e PB2 = RTS. Ver secao 3.

## 3. Esquematicos oficiais e o circuito de auto-boot

### De onde veio o PDF
- As paginas docs.flipper.net/zero/development/hardware/devboard-schematics (e a antiga docs.flipperzero.one/development/hardware/wifi-developer-board/schematics, hoje 404) listam 4 PDFs (Wi-Fi Module V1 Assembly, ESP32-S2-WROVER-N4R2 schematic, Power schematic, Connectors schematic). **Os links sao pre-assinados (S3/Archbee) e retornam 403/expirado**; nao os obtive da fonte.
- Usei o PDF unico de 4 folhas "WI-FI Module V1" (Flipper Devices Inc., Rev V1, 22.01.2022) espelhado em github.com/UberGuidoZ/Flipper/Wifi_DevBoard/Flipper_Zero_WI-FI_Module_V1_Schematic.PDF. O bloco de titulo e do fabricante e o conteudo (ESP32-S2-WROVER, folhas MCU/Power/Connectors) coincide com os 4 itens da doc. INFERENCIA: e o mesmo desenho; a devboard vendida hoje tem imagem de pinagem "updated" e pode ter pequenas revisoes.
- Os PDFs de esquematico do proprio Flipper (peripherals, power, NFC) nao foram baixados pelo mesmo motivo; o mapa de pinos veio do firmware.

### FATO: circuito de BOOT/RESET da devboard (folha 2, recorte em `flipper-wifi-devboard-autoboot-crop.png`)
Nets: `FLP_GPIO_0` = **pino 6 do header = PB2**; `ESP_EN` = **pino 7 = PC3** (folha 4, CON1: "FLP_GPIO_0 -> 6 PB2", "ESP_EN -> 7 PC3"; a pinagem oficial da devboard rotula pino 6 = BOOT e pino 7 = EN, laranja "ESP32 boot ctrl").

Dois **N-MOSFET DMN2058UW-7** cruzados (nao sao os transistores bipolares classicos DTR/RTS):
| | Gate | Source | Drain |
|---|---|---|---|
| VT5 (reset) | `ESP_EN` (PC3) via **R15 150 ohm** | `FLP_GPIO_0` (PB2) | linha **EN** do ESP32-S2 |
| VT6 (boot) | `FLP_GPIO_0` (PB2) via **R16 150 ohm** | `ESP_EN` (PC3) | linha **GPIO0** do ESP32-S2 |

- Cada uma das duas linhas do Flipper (pino 6 e 7) tem um diodo ESD **ESD241B1W0201E6327XTSA1** para GND (VD10 e VD9), colocado no lado do Flipper, antes do R15/R16.
- Ao lado, folha 2: EN tem **R13 10 kohm a 3V3 + C8 1 uF a GND** e botao RESET SW1 (SKRPABE010) para GND; GPIO0 tem **R14 10 kohm a 3V3** e botao BOOT SW2 para GND. (O mesmo modulo ESP32-S2-WROVER tem o EN/IO0 nos pinos 41 e 3.)
- Logica (derivada do esquematico, FATO por analise do circuito):
  - PC3 = alto e PB2 = baixo: VT5 conduz, EN vai a ~0 V -> **RESET** (VT6 desligado).
  - PB2 = alto e PC3 = baixo: VT6 conduz, GPIO0 vai a ~0 V -> **BOOT** (VT5 desligado, EN solto pelo pull-up).
  - Ambos baixos (ou Hi-Z, o padrao do Flipper) ou ambos altos: nenhum conduz, ESP roda normal.
- Isto bate com o firmware do ESP Flasher (`loader_port_enter_bootloader`/`loader_port_reset_target`), FATO: pinos em saida push-pull com pull-down, idle = baixo. **Reset puro**: PC3 alto por um tempo, depois baixo. **Entrar no bootloader**: PC3 alto (EN baixo, reset), depois PB2 alto + PC3 baixo (solta EN com GPIO0 baixo), segura `SERIAL_FLASHER_BOOT_HOLD_TIME_MS`, depois PB2 baixo (solta GPIO0). Antes disso o app ainda ciclou OTG (5 V) e levou SWCLK a baixo para outras placas (Multi-fucc/Xeon): irrelevante para o AirScope.
- Alimentacao (folhas 2/3): entrada 5 V (USB_5V) ou ext_5V (pino 1) -> 5V por bloco "ideal diode" (PMOS DMP1045U + par PNP MMDT2907A + 2x 100 kohm); LDO **AZ1117H-3.3** (10 uF entrada, 22 uF saida) gera LDO_3V3; e o 3V3 final une ext_3V3 (pino 9) e LDO_3V3 por mais dois blocos iguais. Desacoplamento no modulo: C2 22 uF + C3 100 nF. Isso confirma o conceito "OR de 3V3 do Flipper com o LDO do USB-C" de gpio.md: ninguem alimenta o outro para tras. USB: conector 105450-0101 USB-C com resistores 5,1 kohm no CC e ESD230B1 na VBUS/D+/D-. Os pinos 5V do header e a ligacao ao 5V interno so entram pelo bloco de selecao.

### INFERENCIA: como copiar para o ESP32-C5 (AirScope)
- O circuito e topologicamente neutro: basta mapear **drain VT5 -> EN (CHIP_PU)** e **drain VT6 -> pino de boot**. No C5, fonte Espressif (docs.espressif.com/projects/esptool/en/latest/esp32c5/advanced-topics/boot-mode-selection.html): "ESP32-C5 entra no bootloader serial com **GPIO28 em baixo** no reset", e o GPIO27 deve estar alto para entrar de forma confiavel; recomenda capacitor ~1-10 uF entre EN e GND (a devboard usa 1 uF + 10 kohm). **Ligar o drain de VT6 a GPIO28, nao a GPIO0** (que no C5 nao e o pino de boot). Conferir no esquematico do WROOM-1U do C5 que GPIO28 esta exposto e com pull-up e que GPIO27 fica alto.
- Pelo que o Flipper tem do lado do header (J1 pino 6 = PB2, pino 7 = PC3) o plano de gpio.md (RTS = pino 6 para boot, DTR = pino 7 para reset) esta **coerente** com o circuito oficial: PB2 -> gate do MOSFET de boot, PC3 -> gate do MOSFET de reset.
- Componentes copiaveis: 2x N-MOSFET (DMN2058UW-7 ou equivalente SOT-323 com Vgs(th) baixo, **conferir Vgs(th) vs. 3,3 V**), 2x 150 ohm nos gates, 2x ESD no lado Flipper (opcional), EN com 10 kohm + 1 uF, boot com 10 kohm. Em gpio.md essa parte e Q1/Q2 + R6-R9 DNP: o desenho oficial usa 2 MOSFET + 2 resistores + 2 ESD, mais simples que 4 resistores.
- Atencao: o circuito faz a mesma coisa que o par NPN classico (DTR/RTS), mas **depende de PB2 e PC3 serem baixos/Hi-Z no estado normal**. Qualquer app do Flipper que ponha PB2 e PC3 em niveis diferentes reinicia ou poe o ESP em boot: e o mesmo comportamento da devboard oficial.

## 4. Boas praticas e regras para modulos

- **Corrente 3,3 V**: limite da doc 1,2 A no pino 9 (FATO). Nao achei numero oficial de consumo da devboard Wi-Fi. INFERENCIA: dimensionar pelo pico de TX do ESP32-C5 (datasheet) com margem; e manter a opcao de alimentar tudo pelo USB-C do modulo, poupando a bateria do Flipper.
- **5 V ligado**: com bateria o pino 1 so tem tensao se o usuario ligar "5V on GPIO"; com USB no Flipper, o pino 1 tem 5 V direto do USB. FATO. Logo: **nao dependa do pino 1 sem testar e nao o ligue ao 5 V do USB-C do modulo** (a devboard isola com bloco ideal-diode). Se o modulo for alimentado so pelo 3V3 do Flipper, deixar o pino 1 desligado ou so com link DNP.
- **OTG**: o 5 V do pino 1 em bateria e o OTG do carregador (o ESP Flasher o desliga/liga no `loader_port_enter_bootloader`: FATO no codigo). Entrada em Hi-Z segura, nao exige nada do modulo.
- **3,3 V cai durante montagem do SD e atualizacao de firmware** (FATO, doc): o modulo precisa suportar reiniciar nesses momentos e nao pode manter uma tensao propria presa no 3V3 do Flipper (ideal diode). Capacitancia grande no 3V3 do pino 9: evitar (corrompe SD), usar so a necessaria (a devboard usa 22 uF + 100 nF no modulo ESP, 10 uF na entrada do LDO).
- **Capa de silicone**: ver secao 1. Sem cota oficial de folga: medir a capa real; projetar o modulo para encaixar com ou sem capa (a profundidade de encaixe muda; a doc exige sem vao).
- **Orientacao**: o modulo fica "em pe" sobre o topo, com a face frontal virada para o mesmo lado da tela (vista frontal: 8 pinos a esquerda). A orientacao do pino 1 dentro do grupo esta deduzida (ja registrada em gpio.md); confirmar no encaixe real.
- **Menor perfil**: nao ha tabela oficial que compare modulos. O gabarito oficial limita a PCB a 67,34 x 20 mm; qualquer placa menor/mais baixa que isso funciona. Nao achei medidas oficiais da devboard Wi-Fi.

## 5. Pontos de risco

1. **GPIO28 vs GPIO0**: copiar o circuito "ao pe da letra" ligando o MOSFET de boot ao GPIO0 nao poe o C5 em bootloader. Validar com o esquematico do ESP32-C5-WROOM-1U antes de rotear.
2. **Vgs(th) do MOSFET a 3,3 V**: com PB2/PC3 a 3,3 V (apos os 51 ohm do Flipper), VT5/VT6 devem conduzir com Vgs ~3,3 V. Conferir no datasheet do DMN2058UW-7 ou escolher outro; sem esse check o auto-boot pode falhar.
3. **Esquematico oficial nao baixado do site**: usei espelho no GitHub. Se a devboard mudou de revisao, comparar com o PDF mais novo (links do docs.flipper.net precisam ser abertos pelo navegador).
4. **Header**: o lado do corpo (frente/tras da PCB) e o lado da face de 14,75 mm nao estao rotulados no desenho: errar isso inverte o modulo. Prototipo de teste de encaixe (so furos + header, sem componentes) antes de encomendar o lote.
5. **Pino 17 (PB14/iButton)**: pull-up de 1 kohm a 5 V: manter NC. Pino 10 (SWCLK): o ESP Flasher o aciona para outras placas: manter NC.
6. **Atualizacao/SD derruba o 3V3**: o ESP reinicia nesses momentos; nao e defeito. Tampouco ligar o pino 1 a rede 3V3 por engano.
7. **Capacitancia no 3V3 e inrush**: doc alerta corrupcao de microSD ao conectar carga capacitiva com o Flipper ligado.
8. **Altura da placa**: o `CLAUDE.md` do AirScope registra a PCB v0.1 com 67,34 x **36 mm**, mas o gabarito oficial do modulo e 67,34 x **20 mm**. Com os furos a 3,84 mm da borda de encaixe, 36 mm de altura da ~32 mm acima do topo do Flipper, contra ~16 mm do gabarito. Nao e erro de encaixe (o header e igual), mas foge do desenho oficial: decidir conscientemente (antena/USB-C/microSD precisam do espaco?) e ver se cabe em capa/bolso.
9. **Tolerancias do desenho oficial** (classe B): +/-0,05 mm para L<=3 mm ate +/-0,30 mm acima de 120 mm (tabela do `flipper-external-module-drawing.pdf`).

## Lacunas (nao achei, nao inventei)
- Qual face do Flipper (frontal/tras) e a referencia dos 14,75 mm.
- Espessura/dimensoes oficiais da capa de silicone.
- Consumo oficial da devboard Wi-Fi e suas dimensoes.
- PDFs oficiais do site (links assinados expirados); esquematicos do proprio Flipper (peripherals/power).
- Vgs(th) do DMN2058UW-7 (nao conferi no datasheet).

## Fontes
- docs.flipper.net/zero/gpio-and-modules
- docs.flipper.net/zero/development/hardware/tech-specs
- docs.flipper.net/zero/development/hardware/devboard-schematics
- github.com/flipperdevices/flipperzero-3d-models (master): `flipper-zero/body-2d`, `body-3d`, `external-module/*`, `preview/*`
- github.com/flipperdevices/flipperzero-firmware (dev): `targets/f7/furi_hal/furi_hal_resources.c`, `documentation/doxygen/dev_board.dox`
- github.com/0xchocolate/flipperzero-esp-flasher: `esp_flasher_worker.c`
- github.com/UberGuidoZ/Flipper/Wifi_DevBoard (espelho do esquematico)
- cdn.flipper.net/Flipper_Zero_wifi_devboard_pinout_updated.png
- docs.espressif.com/projects/esptool/en/latest/esp32c5/advanced-topics/boot-mode-selection.html
