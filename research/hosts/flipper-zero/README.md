# Referencias tecnicas - Flipper Zero

> **`[FLIPPER]` — documentação oficial da Flipper Devices.** Conteúdo específico do Flipper Zero; aplicar **somente** a placas que encaixam nesse aparelho. Não é regra geral de PCB (para isso: `../PADROES-PROJETO-PCB.md` e `../boas-praticas/`).


Biblioteca compartilhada do programa 9-PCB para qualquer projeto que encaixe no GPIO do Flipper Zero (nao duplicar essas pesquisas por projeto). Pasta irma futura: `../flipper-one/` (quando o dono decidir atacar o Flipper One).

## Conteudo

- **gpio/** - pinagem oficial do conector de 18 pinos:
  - `flipper-gpio-pinout.jpg`, `flipper-gpio-schematic.jpg` - mapa completo de pino x periferico STM32 (EXTI, Timer, ADC, UART, SPI, SWD), fonte docs.flipper.net/zero/gpio-and-modules.
  - `flipper-external-module-pcb-outline.dxf/.pdf`, `flipper-external-module-drawing.pdf/.png` - desenho mecanico OFICIAL do gabarito de PCB de modulo externo (furos, cotas, encaixe com a capa de silicone). Fonte: github.com/flipperdevices/flipperzero-3d-models (GPL-3.0, ver LICENSE-GPL3-flipperzero-3d-models.txt).
- **wifi-devboard-oficial/** - foto e pinout detalhado (pino Flipper <-> GPIO do ESP32-S2) da Wi-Fi Developer Board oficial. Usar como referencia de layout (posicao de USB-C, botoes RESET/BOOT, modulo) e do circuito de auto-boot (pinos 6/7 = boot/reset via MOSFET). Fonte: developer.flipper.net/flipperzero/doxygen/dev_board.html.
- **dimensoes-corpo/flipper-dimensoes-gpio.md** - pesquisa com fatos/fontes: dimensoes do corpo do Flipper (100,3 x 40,1 x 25,6 mm sem capa), posicao do header, limites eletricos do GPIO, e o circuito oficial de auto-boot (dois MOSFET N cruzados; no ESP32-C5 o boot vai no GPIO28).

## Pinagem confirmada (resumo rapido)

| Pino | Funcao |
|---|---|
| 1 | 5V (so com "5V on GPIO" ativado no menu, 1,2 A) |
| 6 | Boot (controle, via PB2) |
| 7 | Reset/EN (controle, via PC3) |
| 8, 11, 18 | GND |
| 9 | 3,3 V (1,2 A) |
| 13 | TX do Flipper (USART1) -> RX do modulo |
| 14 | RX do Flipper (USART1) <- TX do modulo |
| 15/16 | UART alternativa (LPUART) / I2C (SDA/SCL) em alguns modulos oficiais |
| 10, 12 | SWCLK/SWDIO - nao usar |
| 17 | iButton, pull-up 1 kOhm para 5V - nunca ligar |

Detalhe completo e fontes em `dimensoes-corpo/flipper-dimensoes-gpio.md`.

Usado pela primeira vez no projeto `temporaria/airscope-5g` (2026-11-19).
