# Referencias tecnicas - Flipper One

> **`[FLIPPER]` — documentação oficial da Flipper Devices.** Conteúdo específico do Flipper One; aplicar **somente** a placas que encaixam nesse aparelho. Não é regra geral de PCB (para isso: `../PADROES-PROJETO-PCB.md` e `../boas-praticas/`).


Fonte: docs.flipper.net/one e o repositorio publico github.com/flipperdevices/flipperone-docs (branch public-release). Projeto em desenvolvimento aberto, SEM data de lancamento e SEM produto a venda (2026-11-19). Licenca do repo de docs nao declarada explicitamente no GitHub - tratar como referencia, nao redistribuir como se fosse nosso trabalho.

## O que e
Flipper One = "portable Linux multi-tool". SoC Rockchip RK3576 (ARM, roda Linux) + MCU RP2350 (controla tela, energia, boot, botoes/touchpad). Ainda sem especificacoes finais fechadas; hardware "pronto" segundo imprensa (CNX Software, mai/2026) mas software ainda em desenvolvimento.

## GPIO port (docs-md/GPIO-port.md)
- Conector de expansao para modulos externos (mecanica: ver gpio/flipper-one-gpio-module-*-mount.png - dois padroes de fixacao, por parafuso ou por tampa).
- Alimentacao: 3,3 V e 5 V, cada um protegido por EFUSE ate 2 A (bem mais corrente que o Flipper Zero, que e 1,2 A).
- USB 2.0 D+/D- da CPU disponivel no conector.
- Pinos mistos MCU (RP2350, 2 pinos: M40/M41 - ADC0, PWM8, PIO) e CPU (Rockchip, varios pinos multiplexados: I2C, UART, SPI, CAN, PWM, I2S, SPDIF, PIO) - ver tabela completa em docs-md/GPIO-port.md e a imagem gpio/gpio-port-pinout.jpg.
- Esquematico oficial: visualizador Altium 365 embutido na pagina (nao baixavel como arquivo; ver link em docs-md/GPIO-port.md).

## M.2 port (docs-md/M2-port.md) - NOVO, nao existe no Flipper Zero
- Slot interno (sob a tampa traseira), tipo **M.2 Key B**.
- Tamanhos suportados: 2230 (com extensor), 2242, 3042, 3052; espessura ate S3 (single-sided).
- Interfaces: PCIe 2.1 x1, USB 2.0, USB 3.1, SATA3, Serial Audio, UART, I2C, cartao SIM + eSIM.
- Usos previstos (docs-md/M2-Modules.md): modem celular, GNSS, SDR, SSD NVMe, aceleradores de IA, Wi-Fi.

## Modulos ja documentados pela propria Flipper
- Modulo GPIO walkie-talkie (SA828), ver GPIO-Modules.md.
- Modulo M.2 GNSS e modulo M.2 modem satelite, ver M2-gnss-receiver.md / M2-satellite-modem.md.
- Wi-Fi do proprio aparelho: modulo MT7921AU (ver imagens/flipper-one-wifi-*), citado em dev log, nao e um "modulo de expansao" e sim parte do hardware principal.

## Pendente (nao encontrado nesta pesquisa)
- Dimensoes externas do aparelho.
- Cotas mecanicas do conector GPIO (pitch, posicao) - os docs nao trazem um desenho tipo DXF como o do Flipper Zero.
- Licenca explicita do conteudo.

## Indice de arquivos
- `docs-md/` - paginas oficiais em Markdown (About-Hardware, GPIO-port, GPIO-Modules, M2-port, M2-Modules, M2-gnss-receiver, M2-satellite-modem, Power-subsystem, Power-meter, Debug-probe).
- `gpio/` - imagens do conector GPIO (pinout, montagem).
- `m2/` - imagens do slot M.2 (pinout, formato).
- `imagens/` - fotos gerais do hardware e do modulo Wi-Fi interno.

Pasta irma: `../flipper-zero/`.
