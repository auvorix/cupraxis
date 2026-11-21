r"""Atualiza references/ da skill a partir da fonte da verdade (<REFERENCIAS>).
Uso: python -I sync_references.py [pasta_referencias]
A fonte e editada pelo dono; a skill leva uma copia para funcionar fora daquela maquina/pasta."""
import os, shutil, sys, pathlib
_here = pathlib.Path(__file__).resolve().parent
# ordem: argumento > env PCB_REFERENCIAS > pasta local do dono > research/ do repositorio publico
_cands = [sys.argv[1]] if len(sys.argv) > 1 else [
    os.environ.get("PCB_REFERENCIAS", ""),
    r"<REFERENCIAS>",
    str(_here.parent.parent.parent / "research"),
]
SRC = next((pathlib.Path(c) for c in _cands if c and (pathlib.Path(c) / "boas-praticas").is_dir()), None)
if SRC is None:
    sys.exit("pasta de referencias nao encontrada: passe o caminho como argumento ou defina PCB_REFERENCIAS")
DST = pathlib.Path(__file__).resolve().parent.parent / "references"
m = {
    "PADROES-PROJETO-PCB.md": "regras-da-casa.md",
    "boas-praticas/00-conflitos-e-lacunas.md": "00-conflitos-e-lacunas.md",
    "boas-praticas/01-floorplan-zoneamento.md": "01-floorplan-zoneamento.md",
    "boas-praticas/02-energia-smps.md": "02-energia-smps.md",
    "boas-praticas/03-rf-antenas.md": "03-rf-antenas.md",
    "boas-praticas/04-gnd-si-emc-stackup.md": "04-gnd-si-emc-stackup.md",
    "boas-praticas/05-componentes-conexoes.md": "05-componentes-conexoes.md",
    "boas-praticas/06-shape-dfm-estetica.md": "06-shape-dfm-estetica.md",
    "boas-praticas/07-bibliografia-consolidada.md": "07-bibliografia-consolidada.md",
    "boas-praticas/08-ferramentas-kicad.md": "08-ferramentas-kicad.md",
    "boas-praticas/09-ferramentas-fabrica-mcp-cad.md": "09-ferramentas-fabrica-mcp-cad.md",
    "boas-praticas/10-fabricantes-pcb-pcba.md": "10-fabricantes-pcb-pcba.md",
}
for s, d in m.items():
    p = SRC / s
    if p.exists():
        shutil.copy2(p, DST / d); print("ok ", d)
    else:
        print("-- faltando", s)
