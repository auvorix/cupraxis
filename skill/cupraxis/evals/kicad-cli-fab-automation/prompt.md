---
tags: [cupraxis]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Quero automatizar a saída de fábrica de um projeto KiCad 10 no Windows (projeto em C:\pcb\sensor\sensor.kicad_pro, placa sensor.kicad_pcb, esquemático sensor.kicad_sch). Me escreve um script PowerShell que: roda ERC e DRC (com checagem de paridade esquemático x placa) gerando relatório JSON e para se tiver erro; gera gerbers, furação, arquivo de posição (CPL) e BOM no formato que a JLCPCB aceita; e compacta tudo num zip. Também me escreve um arquivo .kicad_dru com as regras mínimas da JLCPCB para 2 camadas e uma regra para o par diferencial USB de 90 ohms.
