"""Consulta SQL no banco local de pecas JLCPCB (baixado pelo KiCAD-MCP: download_jlcpcb_database).
Uso: python -I jlc_query.py "<clausula WHERE>" [...]
Banco: variavel de ambiente JLC_DB, ou ~/.kicad-mcp/data/jlcpcb_parts.db
Ex.: python -I jlc_query.py "mfr_part like 'TPS63020%' order by (library_type='Basic') desc, stock desc"
Atencao: 'stock' e o estoque LCSC, NAO o do armazem de montagem JLC (confirmar na etapa BOM do pedido).
"""
import os
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")
DB = os.environ.get("JLC_DB", os.path.expanduser("~/.kicad-mcp/data/jlcpcb_parts.db"))
c = sqlite3.connect(DB)
COLS = "lcsc,library_type,mfr_part,package,stock,substr(description,1,95)"
for sql in sys.argv[1:]:
    print("##", sql[:110])
    for r in c.execute("select %s from components where %s" % (COLS, sql)).fetchall():
        print("  ", r)
