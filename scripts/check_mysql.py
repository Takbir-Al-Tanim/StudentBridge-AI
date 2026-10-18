"""Read-only smoke check against the *actual* MySQL server; no destructive actions."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import database

def main():
    if database.engine().dialect.name!='mysql':raise SystemExit('A MySQL DATABASE_URL is required')
    print('Connected:',database.check_health())
    print('Tables:',list(database.metadata.tables))
    print('Research counts:',database.research_counts())
    print('Audit check:',database.verify_audit_chain(__import__('os').environ.get('APP_SECRET','local-sandbox-only-change-before-deploy').encode()))
if __name__=='__main__':main()
