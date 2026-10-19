"""Isolation: unit/API tests use disposable SQLite, NEVER the configured MySQL DB.
Production code refuses SQLite unless STUDENTBRIDGE_TEST_MODE=1.
Real MySQL validation is a separate opt-in smoke-test script.
"""
import os,tempfile
from pathlib import Path
_TMP=Path(tempfile.mkdtemp(prefix='studentbridge_test_'))
os.environ['STUDENTBRIDGE_TEST_MODE']='1'
os.environ['DATABASE_URL']='sqlite+pysqlite:///'+str(_TMP/'test.db')
os.environ['APP_SECRET']='test_only_changing_key_does_not_authorize_real_payments'
from app import database
database.initialize()
database.import_research_csv(Path(__file__).resolve().parents[1]/'data/research/corrected')
