---
tags: [pcb-expert]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Tô projetando uma placa controladora de 2 motores DC (12 V, até 3 A cada, picos de partida maiores) usando dois DRV8871, alimentada por bateria LiPo 3S, com um ESP32-S3-WROOM-1 (módulo com antena impressa) e um INA226 com shunt para medir a corrente total. A placa tem uns 80x50 mm. Me diz como organizar o layout: camadas e espessura de cobre, larguras de trilha, onde fica a parte de potência vs a lógica, cuidados térmicos, proteção da entrada e como não deixar o ruído dos motores derrubar o ESP32.
