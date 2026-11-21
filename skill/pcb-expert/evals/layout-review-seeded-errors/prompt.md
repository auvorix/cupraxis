---
tags: [pcb-expert]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Revisa esse layout que eu fiz no KiCad (placa de 2 camadas, 1,6 mm, 60x45 mm, vai pra JLCPCB com montagem) e me diz o que está errado, por ordem de gravidade:
- Buck TPS62130 (5V->3V3, 2 A): o capacitor de entrada de 10 uF ficou no lado de baixo, a uns 6 mm do pino VIN, ligado por 2 vias. A trilha do FB passa por baixo do indutor.
- USB 2.0 do MCU: D+ e D- com 3 vias cada, diferença de comprimento de 4 mm entre eles, e no meio do caminho cruzam um corte que fiz no plano de GND para separar GND analógico do digital.
- Cristal de 16 MHz a 10 mm do MCU, e passei uma trilha de SPI por baixo dele no bottom.
- O TVS do USB ficou perto do MCU, a uns 30 mm do conector USB-C.
- No VBUS (5 V) usei um MLCC 22 uF X5R 6,3 V 0805 como bulk, encostado na linha do V-cut do painel.
- A antena chip de 2,4 GHz está no canto da placa, mas deixei o pour de GND por baixo dela no bottom.
- As referências do silk estão com 0,6 mm de altura pra caber.
