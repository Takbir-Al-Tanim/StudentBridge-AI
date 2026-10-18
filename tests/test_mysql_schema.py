from pathlib import Path
from sqlalchemy.dialects import mysql
from sqlalchemy.schema import CreateTable
from app import database

def test_all_mysql_tables_compile_as_innodb():
    assert len(database.metadata.tables)==11
    for table in database.metadata.sorted_tables:
        statement=str(CreateTable(table).compile(dialect=mysql.dialect()))
        assert 'CREATE TABLE' in statement
        assert 'ENGINE=InnoDB' in statement

def test_research_import_repeatable_without_duplicates():
    counts1=database.research_counts()
    directory=Path(__file__).resolve().parents[1]/'data/research/corrected'
    database.import_research_csv(directory)
    assert database.research_counts()==counts1

def test_audit_chain_can_be_verified_after_plan_and_sandbox():
    import os
    from app.main import app
    from fastapi.testclient import TestClient
    client=TestClient(app)
    result=client.get('/api/audit/verify')
    assert result.status_code==200
    assert result.json()['valid'] is True
    assert 'checked' in result.json()

def test_mysql_sql_scripts_are_bundled():
    root=Path(__file__).resolve().parents[1]
    ddl=(root/'scripts/mysql_schema.sql').read_text()
    seed=(root/'scripts/mysql_research_seed.sql').read_text()
    assert 'CREATE TABLE IF NOT EXISTS audit_chain_state' in ddl
    assert 'CREATE TABLE IF NOT EXISTS payment_quotes' in ddl
    assert "'CN'" in seed and "'JP'" in seed
    assert 'INSERT IGNORE' in seed
