# Gabarito de host: Raspberry Pi HAT / HAT+ (40 pinos)

> Carregar só para placas que encaixam no header de 40 pinos do Raspberry Pi (Pi 4, 5, etc.).
> Fontes oficiais (conferidas em 2026-11-21):
> - Desenho mecânico da HAT (Raspberry Pi 2014/2018): `<REFERENCIAS>\boas-praticas\pdfs\06-dfm\rpi-hat-board-mechanical.pdf` (https://github.com/raspberrypi/hats).
> - Especificação HAT+ (rev. 12/2024): `...\pdfs\06-dfm\rpi-hat-plus-specification.pdf` (https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf).

## Mecânica (desenho oficial, FATO)
- **Placa:** 65 × 56 mm (header THT) ou 65 × 56,5 mm (header SMD). O desenho diz: "56.5mm for SMT style GPIO header, otherwise 56.0mm for through hole header".
- **Cantos:** raio de 3 mm.
- **Furos:** 4 furos M2.5 nos cantos, de **2,75 ± 0,05 mm**, em retângulo de **58 × 49 mm**. Os centros ficam a 3,5 mm das bordas: (3,5; 3,5), (61,5; 3,5), (3,5; 52,5), (61,5; 52,5).
  - De preferência não metalizados.
  - Se forem metalizados, furo e anel ficam isolados, sem ligação ao GND.
  - Anel ou área livre mínima de Ø 6,2 mm.
- **Header de 40 pinos:** na borda longa, ao longo de 58 mm entre os centros dos furos. O centro do header fica a 29 mm do furo. Confirme o pino 1 no footprint oficial ou sobrepondo o modelo 3D do Pi.
- **Recortes recomendados (exemplos do desenho):**
  - Fenda para o flex da câmera: 2 × 17 mm, centrada a 45 mm, a 11,5 mm da borda.
  - Recorte para o flex do display: 5 × 17 mm na borda esquerda, raio interno de 1 mm, a 19,5 mm da borda inferior.
  - No Pi 5 as posições de FFC e PCIe mudam: confira o desenho mecânico do Pi 5.

## Elétrica HAT+ (especificação 12/2024, FATO)
- **EEPROM de ID obrigatória** em ID_SD/ID_SC (GPIO0/1, pinos 27/28), com pull-ups de **3,9 kΩ para 3,3 V**.
  - Nada mais pode ser ligado a ID_SC e ID_SD.
  - A EEPROM tem de ser 3,3 V, com endereçamento de 16 bits, pino WP que protege toda a memória, sem clock stretching e sem paginação de endereço.
  - Peça recomendada: **OnSemi CAT24C32**. Como ela tem pull-down interno no WP, use pull-up "duro" de 1 kΩ.
  - Endereço típico: 0x50.
- **Estado STANDBY:** a HAT+ precisa ser eletricamente compatível com o 5 V ligado e o 3,3 V desligado, que é o standby do Pi 4/5. Na prática:
  - Rails próprios derivados do 5 V são habilitados pelo 3V3 do Pi.
  - Nenhum pull-up para um rail próprio pode alimentar de volta (back-feed) os GPIOs do Pi.
- **Espaçadores:** com o Active Cooler, use **≥ 15 mm; 16 mm é o ideal**. Mais altos se houver componentes embaixo da HAT. Use header empilhável compatível com essa altura.
- **Power HAT+:** se a placa alimenta o Pi, precisa fornecer ≥ 3 A a 5,1 V (ver spec).
- **GPIO a 3,3 V:** o I²C do Pi tem pull-ups de 1,8 kΩ para 3,3 V nos GPIO2/3. Periféricos alimentados em 5 V precisam aceitar VIH de 3,3 V. Exemplo: ADS1115 em 5 V tem VIH = 0,7·VDD = 3,5 V → alimente-o em 3,3 V.
