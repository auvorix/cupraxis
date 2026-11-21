# referencias/ — índice (base da skill universal "especialista em PCB")

Atualizado em 2026-11-21. Esta pasta é **universal**: serve a qualquer PCB (produto autônomo, IoT/bateria, RF, energia, periférico USB, sensor/analógico, HAT/shield/módulo que encaixa em host). Projetos específicos aparecem só como **exemplo** ou como **gabarito de host** opcional. Cada linha diz **o que é** e **qual papel terá na skill**.

**Etiqueta `[FLIPPER]`:** marca o que vem da documentação **oficial** da Flipper Devices (Flipper Zero/One). Só se aplica a placas que encaixam nesses aparelhos; a skill carrega esse material apenas nesse caso.

## Camadas do conhecimento
1. **Regras da casa** (decisões do dono, prevalecem): `PADROES-PROJETO-PCB.md`.
2. **Boas práticas gerais** (literatura profissional, com fonte e etiqueta FATO/INFERÊNCIA): `boas-praticas/`.
3. **Reference designs de peças** (`rf-reference-designs/`) e **gabaritos de host** (exemplos de placa que encaixa em outro aparelho: `flipper-zero/`, `flipper-one/`; futuros: Raspberry Pi HAT, Arduino shield, Feather etc.). Gabaritos só se aplicam quando o projeto encaixa naquele host.
4. **Ferramentas** (scripts): `scripts-roteamento/`, `scripts-bom/`.

## Arquivos

| Caminho | Conteúdo | Papel na skill |
|---|---|---|
| `PADROES-PROJETO-PCB.md` | Regras de projeto da casa + erros já cometidos + receitas de roteamento/BOM | Núcleo do `SKILL.md` (regras obrigatórias, gates, checklist) |
| `boas-praticas/00-conflitos-e-lacunas.md` | Onde a literatura diverge do PADROES, regras que faltam, pendências | Lista de decisões para o dono **antes** de escrever a skill |
| `boas-praticas/01-floorplan-zoneamento.md` | Zonas/quadrantes, ordem de placement, proximidade por tipo de peça, compactação, térmico, DFA/JLC (espaçamentos, fiduciais, rails), floorplan ASCII genérico (RF + MCU + bateria + USB) | `references/placement.md` |
| `boas-praticas/02-energia-smps.md` | Hot loops de buck/boost/buck-boost, LDO × LC, desacoplamento, largura de trilha/via por corrente, ferrite, LiPo/power-path, USB-C VBUS, térmico | `references/energia.md` |
| `boas-praticas/03-rf-antenas.md` | Keepout de antenas/módulos, CPWG × microstrip com contas, redes de casamento, cercas de via λ/20, coexistência, SMA/u.FL, RED | `references/rf.md` |
| `boas-praticas/04-gnd-si-emc-stackup.md` | Caminho de retorno, plano único × split, stackups JLC 2/4/6, USB 90 Ω, cristais, microSD, ESD/TVS, EMC, regras contestadas (20H/3W) | `references/gnd-emc-stackup.md` |
| `boas-praticas/05-componentes-conexoes.md` | Escolha de passivos (encapsulamento, dielétrico, DC bias), indutores, cristais, ferrites, TVS, ciclo de vida/MSL/JLC Basic×Extended, conectores (JST, B2B, FPC, USB-C, microSD, Tag-Connect, QWIIC) | `references/componentes.md` |
| `boas-praticas/06-shape-dfm-estetica.md` | Contorno (DXF/StepUp), cantos, furos M2–M3, co-design com carcaça, painelização, capacidades JLC, silkscreen e estética, documentação de fab | `references/shape-dfm.md` |
| `boas-praticas/07-bibliografia-consolidada.md` | Livros, normas, app notes, calculadoras (cópia das bibliografias dos temas) | `references/bibliografia.md` |
| `boas-praticas/08-ferramentas-kicad.md` | KiCad 10, receitas `kicad-cli` testadas no 10.0.8, `.kicad_dru`, API `pcbnew`/IPC, Freerouting, plugins | `references/08-ferramentas-kicad.md` |
| `boas-praticas/09-ferramentas-fabrica-mcp-cad.md` | Pedido JLC (BOM/CPL), KiCad-MCP (ferramentas e armadilhas), FreeCAD/StepUp/OpenSCAD, simulação, render | `references/09-...` |
| `boas-praticas/10-fabricantes-pcb-pcba.md` | Comparação de fabricantes (JLC, PCBWay, NextPCB, Seeed, ALLPCB, Elecrow, OSH Park, Aisler, Eurocircuits, Multi-CB/Würth, MacroFab), formatos BOM/CPL, mínimo comum, UE/IVA | `references/10-...` |
| `boas-praticas/_BRIEF-PESQUISA.md` | Contrato usado pelos agentes de pesquisa | Reutilizar para novas rodadas de pesquisa |
| `boas-praticas/pdfs/<tema>/` | ~100 MB de app notes e guias **oficiais gratuitos** (TI, Espressif, u-blox, Kyocera AVX, Vishay, Murata, JST, Raspberry Pi, Altium…), cada pasta com `LICENSES.md` | Fonte primária para consulta; **não** copiar para dentro da skill (só citar caminho) |
| `flipper-zero/` | `[FLIPPER]` Gabarito de host — docs oficiais Flipper Devices: GPIO, desenho mecânico oficial do módulo externo (DXF/PDF), devboard Wi-Fi, dimensões | `references/hosts/flipper-zero.md` (carregado só se o projeto encaixa nele) |
| `flipper-one/` | `[FLIPPER]` Gabarito de host — docs oficiais Flipper Devices: docs oficiais (GPIO, M.2, energia), imagens | `references/hosts/flipper-one.md` (idem) |
| `rf-reference-designs/` | CC1101 (layout/esquema/BOM TI, DN017), MAX-M10S integration manual, nRF24L01 spec | Reference designs de RF citados pela skill |
| `scripts-roteamento/` | `ripup.py`, `spread.py`, `gnd_fix.py`, `island_fix.py` | `scripts/` da skill (parametrizar antes — ver 00 §F) |
| `scripts-bom/` | `jlc_query.py` e afins (SQL no banco JLC local) | `scripts/` da skill |

## Skill gerada
A skill está instalada em `~/.claude/skills/pcb-expert/` e foi publicada em https://github.com/auvorix/pcb-expert. Para atualizar as referências da skill depois de editar esta pasta: `python -I ~/.claude/skills/pcb-expert/scripts/sync_references.py`.

## Próximo passo
1. Dono decide os itens de `boas-praticas/00-conflitos-e-lacunas.md` (seções A e D).
2. Atualizar `PADROES-PROJETO-PCB.md` com as decisões.
3. Montar a skill com `skill-creator`: `SKILL.md` enxuto e universal (fluxo + gates + checklist) apontando para `references/` (temas 01–06), `references/hosts/` (gabaritos opcionais) e `scripts/`.
