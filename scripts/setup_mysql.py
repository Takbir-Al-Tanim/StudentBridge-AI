"""Create MySQL tables and safely import the 15 Oct 2026 source-backed CSV research seed."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import database

if __name__ == '__main__':
    db_name=database.engine().dialect.name
    if db_name!='mysql':
        raise SystemExit('This script must use a MySQL DATABASE_URL, not a test database.')
    database.initialize()
    directory=Path(__file__).resolve().parents[1]/'data/research/corrected'
    counts=database.import_research_csv(directory)
    print('MySQL research data ready:',counts)
    print('IMPORTANT: Provider transfer quotes are unverified placeholders, not usable bank offers.')
