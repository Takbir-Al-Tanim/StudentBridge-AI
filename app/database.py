"""MySQL 8 persistence for StudentBridge AI.

The application requires DATABASE_URL=mysql+pymysql://...; SQLite is only used
by isolated, disposable automated tests. Financial reference data retains source
provenance; no rows are presented as verified live bank transfer quotes.
"""
from __future__ import annotations
import csv
import hashlib
import hmac
import json
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import (
    MetaData, Table, Column, String, Text, Integer, BigInteger, Numeric,
    ForeignKey, UniqueConstraint, create_engine, select, insert, update, text,
)
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1]/'.env', override=False)

metadata = MetaData()

plans = Table('plans', metadata,
    Column('id', String(40), primary_key=True),
    Column('created_at', String(40), nullable=False),
    Column('payload_json', Text, nullable=False),
    Column('result_json', Text, nullable=False),
    Column('decision_hash', String(64), nullable=False))
transactions = Table('transactions', metadata,
    Column('id', String(45), primary_key=True),
    Column('plan_id', String(40), ForeignKey('plans.id'), nullable=False),
    Column('quote_id', String(80), nullable=False),
    Column('created_at', String(40), nullable=False),
    Column('status', String(40), nullable=False),
    Column('approved_amount', Numeric(22, 4), nullable=False),
    Column('currency', String(3), nullable=False),
    Column('simulation_only', Integer, nullable=False),
    Column('idempotency_key', String(120), unique=True, nullable=False))
audit_events = Table('audit', metadata,
    Column('id', BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, autoincrement=True),
    Column('occurred_at', String(40), nullable=False),
    Column('event_type', String(90), nullable=False),
    Column('object_id', String(80), nullable=False),
    Column('event_json', Text, nullable=False),
    Column('previous_hash', String(64), nullable=False),
    Column('event_hash', String(64), nullable=False))
provider_events = Table('provider_events', metadata,
    Column('event_id', String(120), primary_key=True),
    Column('session_id', String(150), nullable=False),
    Column('event_type', String(100), nullable=False),
    Column('payment_status', String(30), nullable=False),
    Column('received_at', String(40), nullable=False))
audit_chain_state = Table('audit_chain_state', metadata,
    Column('state_id', Integer, primary_key=True),
    Column('last_hash', String(64), nullable=False))

countries = Table('countries', metadata,
    Column('country_code', String(2), primary_key=True),
    Column('country_name', String(100), nullable=False),
    Column('currency_code', String(3)), Column('currency_name', String(100)),
    Column('data_status', String(60), nullable=False), Column('notes', Text))
sources = Table('sources', metadata,
    Column('source_id', Integer, primary_key=True),
    Column('publisher', String(255), nullable=False),
    Column('title', String(500), nullable=False),
    Column('source_url', Text, nullable=False),
    Column('source_type', String(100), nullable=False),
    Column('published_or_updated_date', String(100)),
    Column('collection_date', String(30), nullable=False), Column('notes', Text))
financial_benchmarks = Table('financial_benchmarks', metadata,
    Column('benchmark_id', Integer, primary_key=True),
    Column('country_code', String(2), ForeignKey('countries.country_code'), nullable=False),
    Column('benchmark_type', String(150), nullable=False),
    Column('context', Text, nullable=False),
    Column('amount', Numeric(20, 4)), Column('currency_code', String(3)),
    Column('unit', String(100)), Column('period', String(100)),
    Column('geography', String(150)), Column('reference_date', String(100)),
    Column('source_id', Integer, ForeignKey('sources.source_id')),
    Column('verification_status', String(100), nullable=False), Column('notes', Text))
tuition_benchmarks = Table('tuition_benchmarks', metadata,
    Column('tuition_id', Integer, primary_key=True),
    Column('country_code', String(2), ForeignKey('countries.country_code'), nullable=False),
    Column('institution', String(255)), Column('program', String(500), nullable=False),
    Column('level', String(100)), Column('student_type', String(150)),
    Column('amount', Numeric(20, 4)), Column('currency_code', String(3)),
    Column('fee_basis', String(100)), Column('academic_year', String(100)),
    Column('source_id', Integer, ForeignKey('sources.source_id')),
    Column('verification_status', String(100), nullable=False), Column('notes', Text))
fx_rates = Table('fx_rates', metadata,
    Column('fx_id', Integer, primary_key=True),
    Column('base_currency', String(3), nullable=False),
    Column('quote_currency', String(3), nullable=False),
    Column('rate', Numeric(24, 10)), Column('rate_date', String(20)),
    Column('rate_type', String(255)),
    Column('source_id', Integer, ForeignKey('sources.source_id')),
    Column('verification_status', String(100), nullable=False), Column('notes', Text))
payment_quotes = Table('payment_quotes', metadata,
    Column('quote_id', Integer, primary_key=True),
    Column('origin_country_code', String(2), ForeignKey('countries.country_code'), nullable=False),
    Column('destination_country_code', String(2), ForeignKey('countries.country_code'), nullable=False),
    Column('provider_name', String(255)),
    Column('origin_currency', String(3)), Column('destination_currency', String(3)),
    Column('send_amount', Numeric(22, 4)), Column('receive_amount', Numeric(22, 4)),
    Column('fee_amount', Numeric(22, 4)), Column('fee_currency', String(3)),
    Column('quoted_fx_rate', Numeric(24, 10)), Column('delivery_time', String(100)),
    Column('quote_timestamp', String(40)), Column('quote_expiry', String(40)),
    Column('source_url', Text), Column('verification_status', String(100), nullable=False),
    Column('notes', Text))

for _table in metadata.tables.values():
    _table.dialect_options['mysql']['engine']='InnoDB'

RESEARCH_TABLES = [countries, sources, financial_benchmarks, tuition_benchmarks, fx_rates, payment_quotes]

_engine = None

def engine():
    global _engine
    if _engine is None:
        url = os.getenv('DATABASE_URL', '').strip()
        if not url:
            raise RuntimeError('DATABASE_URL is required. Configure a MySQL 8 URL as documented in README.md.')
        if not (url.startswith('mysql+pymysql://') or
                (url.startswith('sqlite+pysqlite://') and os.getenv('STUDENTBRIDGE_TEST_MODE') == '1')):
            raise RuntimeError('Use mysql+pymysql:// for StudentBridge. SQLite is permitted only in isolated test mode.')
        if url.startswith('sqlite+'):
            _engine = create_engine(url, future=True)
        else:
            _engine = create_engine(url, future=True, pool_pre_ping=True, pool_recycle=1800,
                                    connect_args={'connect_timeout': 8})
    return _engine

def initialize():
    """Create required tables; never drop or overwrite an existing user database."""
    metadata.create_all(engine(), checkfirst=True)
    with engine().begin() as conn:
        if conn.execute(select(audit_chain_state.c.state_id).where(audit_chain_state.c.state_id == 1)).first() is None:
            conn.execute(insert(audit_chain_state).values(state_id=1, last_hash='GENESIS'))

def check_health():
    with engine().connect() as conn:
        conn.execute(text('SELECT 1'))
    return engine().dialect.name

def utcstamp():
    return datetime.now(timezone.utc).isoformat()

def _add_audit(conn, event_type: str, object_id: str, details: dict, secret: bytes):
    # Lock the singleton BEFORE reading/updating the audit chain. Concurrent
    # MySQL requests will serialize here and cannot fork the chain.
    query = select(audit_chain_state.c.last_hash).where(audit_chain_state.c.state_id == 1)
    if conn.dialect.name == 'mysql':
        query = query.with_for_update()
    previous = conn.execute(query).scalar_one()
    now = utcstamp()
    data = json.dumps(details, sort_keys=True, separators=(',', ':'))
    msg = '|'.join([previous, now, event_type, object_id, data])
    event_hash = hmac.new(secret, msg.encode(), hashlib.sha256).hexdigest()
    conn.execute(insert(audit_events).values(occurred_at=now, event_type=event_type,
        object_id=object_id, event_json=data, previous_hash=previous, event_hash=event_hash))
    conn.execute(update(audit_chain_state).where(audit_chain_state.c.state_id == 1).values(last_hash=event_hash))

def audit(event_type, object_id, details, secret):
    with engine().begin() as conn:
        _add_audit(conn, event_type, object_id, details, secret)

def save_plan(plan_id: str, payload: dict, result: dict, decision_hash: str, secret: bytes):
    with engine().begin() as conn:
        conn.execute(insert(plans).values(id=plan_id, created_at=utcstamp(),
            payload_json=json.dumps(payload), result_json=json.dumps(result), decision_hash=decision_hash))
        _add_audit(conn, 'PLAN_CREATED', plan_id, {
            'corridor': f"{payload['origin']} -> {payload['destination']}",
            'quotes_count': len(result['quotes']),
            'recommended': result['recommended_quote_id'], 'decision_hash': decision_hash}, secret)

def load_plan(plan_id: str):
    with engine().connect() as conn:
        row = conn.execute(select(plans.c.result_json).where(plans.c.id == plan_id)).scalar_one_or_none()
    return json.loads(row) if row is not None else None

def get_tx_by_key(conn, key):
    return conn.execute(select(transactions).where(transactions.c.idempotency_key == key)).mappings().first()

def save_sandbox_payment(plan: dict, quote: dict, key: str, transaction_id: str, secret: bytes):
    """Single DB transaction for the simulated payment AND chained audit event."""
    try:
        with engine().begin() as conn:
            existing = get_tx_by_key(conn, key)
            if existing:
                if existing['plan_id'] != plan['plan_id'] or existing['quote_id'] != quote['quote_id']:
                    return {'conflict': True}
                return {'transaction_id': existing['id'], 'status': existing['status'],
                        'simulation_only': True, 'duplicate_prevented': True}
            conn.execute(insert(transactions).values(id=transaction_id, plan_id=plan['plan_id'],
                quote_id=quote['quote_id'], created_at=utcstamp(), status='SIMULATED_COMPLETED',
                approved_amount=quote['total'], currency=plan['origin_currency'],
                simulation_only=1, idempotency_key=key))
            _add_audit(conn, 'SANDBOX_EXECUTED', transaction_id, {
                'plan_id': plan['plan_id'], 'quote_id': quote['quote_id'],
                'amount': quote['total'], 'currency': plan['origin_currency'], 'no_real_money': True}, secret)
    except IntegrityError:
        # Idempotency keys are DB-unique. After a concurrent winning write,
        # safely return the existing transaction instead of duplicating it.
        with engine().connect() as conn:
            existing = get_tx_by_key(conn, key)
        if existing:
            if existing['plan_id'] != plan['plan_id'] or existing['quote_id'] != quote['quote_id']:
                return {'conflict': True}
            return {'transaction_id': existing['id'], 'status': existing['status'],
                    'simulation_only': True, 'duplicate_prevented': True}
        raise
    return {'transaction_id': transaction_id, 'status': 'SIMULATED_COMPLETED',
        'amount': quote['total'], 'currency': plan['origin_currency'], 'simulation_only': True,
        'notice': ('NO REAL MONEY MOVED. Example method and fees are fictional.' if quote.get('simulation_only') else 'NO BANK CONNECTION. NO REAL MONEY WAS MOVED. Provider quote was user entered.')}

def get_transaction(tx_id: str):
    with engine().connect() as conn:
        row=conn.execute(select(transactions).where(transactions.c.id==tx_id)).mappings().first()
    return dict(row) if row else None

def get_history(limit=30):
    with engine().connect() as conn:
        rows=conn.execute(select(transactions.c.id, transactions.c.plan_id,
           transactions.c.quote_id, transactions.c.created_at, transactions.c.status,
           transactions.c.approved_amount, transactions.c.currency, transactions.c.simulation_only)
           .order_by(transactions.c.created_at.desc()).limit(limit)).mappings().all()
    return [{**dict(r), 'approved_amount': float(r['approved_amount']),
             'simulation_only': bool(r['simulation_only'])} for r in rows]

def get_audit(limit=50):
    with engine().connect() as conn:
        rows=conn.execute(select(audit_events.c.occurred_at, audit_events.c.event_type,
           audit_events.c.object_id, audit_events.c.event_hash, audit_events.c.previous_hash)
           .order_by(audit_events.c.id.desc()).limit(limit)).mappings().all()
    return [dict(r) for r in rows]

def verify_audit_chain(secret: bytes):
    """Check stored HMAC chain; reports corruption, not external notarization."""
    with engine().connect() as conn:
        rows=conn.execute(select(audit_events).order_by(audit_events.c.id)).mappings().all()
        chain_head=conn.execute(select(audit_chain_state.c.last_hash).where(audit_chain_state.c.state_id == 1)).scalar_one()
    previous='GENESIS'
    for row in rows:
        msg='|'.join([previous, row['occurred_at'], row['event_type'], row['object_id'], row['event_json']])
        expected=hmac.new(secret, msg.encode(), hashlib.sha256).hexdigest()
        if row['previous_hash'] != previous or not hmac.compare_digest(expected, row['event_hash']):
            return {'valid': False, 'failed_event_id': row['id'], 'checked': len(rows)}
        previous=row['event_hash']
    return {'valid': previous == chain_head, 'checked': len(rows), 'last_hash': previous,
            'stored_head_matches': previous == chain_head}

def import_research_csv(data_dir: Path) -> dict:
    """Repeatable non-destructive update of publicly supplied research rows.
    Uses a SELECT+UPDATE/INSERT upsert to work consistently on MySQL and tests.
    Does not overwrite plans, transactions or audit records.
    """
    initialize()
    counts={}
    nullable_numeric={'amount','rate','send_amount','receive_amount','fee_amount','quoted_fx_rate'}
    for table in RESEARCH_TABLES:
        p=data_dir / f'{table.name}.csv'
        if not p.is_file():raise FileNotFoundError(p)
        with p.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        pk=list(table.primary_key.columns)[0].name
        with engine().begin() as conn:
            for raw in rows:
                unexpected=set(raw)-set(table.c.keys())
                if unexpected:raise ValueError(f'Unknown CSV fields for {table.name}: {unexpected}')
                row={k:(None if v == '' else v) for k,v in raw.items()}
                # Numeric SQLAlchemy fields bind None for missing data; never 0.
                key=row[pk]
                exists=conn.execute(select(table.c[pk]).where(table.c[pk] == key)).first()
                if exists:
                    conn.execute(update(table).where(table.c[pk] == key).values(**{k:v for k,v in row.items() if k != pk}))
                else:
                    conn.execute(insert(table).values(**row))
        counts[table.name]=len(rows)
    return counts

def research_counts():
    from sqlalchemy import func
    with engine().connect() as conn:
        return {table.name: conn.execute(select(func.count()).select_from(table)).scalar_one() for table in RESEARCH_TABLES}

def research_financial_benchmarks(country_code=None):
    stmt=select(financial_benchmarks, countries.c.country_name, sources.c.source_url).join(
        countries, financial_benchmarks.c.country_code == countries.c.country_code).outerjoin(
        sources, financial_benchmarks.c.source_id == sources.c.source_id)
    if country_code:stmt=stmt.where(financial_benchmarks.c.country_code == country_code)
    with engine().connect() as conn:
        rows=conn.execute(stmt.order_by(financial_benchmarks.c.benchmark_id)).mappings().all()
    return [{**dict(r), 'country': r['country_name'], 'amount': (float(r['amount']) if r['amount'] is not None else None)} for r in rows]


def record_gateway_event(event_id: str, session_id: str, event_type: str, status: str, secret: bytes):
    """Idempotent webhook: unique provider event + audit write in one transaction."""
    try:
        with engine().begin() as conn:
            exists=conn.execute(select(provider_events.c.event_id).where(provider_events.c.event_id==event_id)).first()
            if exists:return False
            conn.execute(insert(provider_events).values(event_id=event_id,session_id=session_id,
                event_type=event_type,payment_status=status,received_at=utcstamp()))
            _add_audit(conn,'PROVIDER_PAYMENT_CONFIRMED',session_id,
                       {'provider':'Stripe','provider_event_id':event_id,'status':status},secret)
        return True
    except IntegrityError:
        return False
