"""Generate MySQL-8 CREATE TABLE SQL and idempotent research-data seed SQL.
Only official/collected values from the corrected CSVs are included; no fabricated quotes.
"""
from pathlib import Path
import csv,sys
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from app.database import metadata, RESEARCH_TABLES
from sqlalchemy.dialects.mysql import dialect
from sqlalchemy.schema import CreateTable

def quote(val):
    if val is None or val == '':return 'NULL'
    return "'"+str(val).replace('\\','\\\\').replace("'","''")+"'"

def main():
    path=root/'scripts/mysql_schema.sql'
    lines=['-- StudentBridge AI / MySQL 8.0 schema. Research AND sandbox tables.',
           'CREATE DATABASE IF NOT EXISTS studentbridge_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;',
           'USE studentbridge_ai;', 'SET NAMES utf8mb4;', '']
    for table in metadata.sorted_tables:
        compiled=str(CreateTable(table,if_not_exists=True).compile(dialect=dialect()))
        lines.append(compiled+';\n')
    lines.append("INSERT IGNORE INTO audit_chain_state(state_id,last_hash) VALUES (1,'GENESIS');\n")
    path.write_text('\n'.join(lines),encoding='utf-8')
    path=root/'scripts/mysql_research_seed.sql'
    lines=['-- Original research records imported from corrected CSVs.',
           '-- Missing/unverified values remain NULL, never 0.',
           'USE studentbridge_ai;', 'SET NAMES utf8mb4;', 'START TRANSACTION;', '']
    d=root/'data/research/corrected'
    for table in RESEARCH_TABLES:
        with (d/f'{table.name}.csv').open(encoding='utf-8-sig',newline='') as f:
            rows=list(csv.DictReader(f))
        if not rows:continue
        names=list(rows[0]);fields=','.join('`'+n+'`' for n in names)
        for row in rows:
            vals=','.join(quote(row[k]) for k in names)
            lines.append(f'INSERT IGNORE INTO `{table.name}` ({fields}) VALUES ({vals});')
        lines.append('')
    lines.append('COMMIT;')
    path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Created MySQL schema and research seed:',len(metadata.tables),'tables')
if __name__=='__main__':main()
