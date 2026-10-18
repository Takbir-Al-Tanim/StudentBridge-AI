"""Original StudentBridge Journey Studio calculations. No LLM is allowed to approve payments.

All figures are preview calculations, not executable bank quotes.
"""
from __future__ import annotations
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
import re, hashlib
from typing import Any


def _dec(value: Any) -> Decimal:
    return Decimal(str(value))


def money(value: Decimal) -> float:
    return float(value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def deadline_check(due: date, delivery_days: int = 3, safety_days: int = 3) -> dict:
    today = date.today()
    remaining = (due - today).days
    latest = due - timedelta(days=delivery_days + safety_days)
    return {'days_left': remaining, 'latest_safe_start': latest.isoformat(),
            'estimated_delivery_days': delivery_days, 'safety_buffer_days': safety_days,
            'risk': 'overdue' if remaining < 0 else 'urgent' if remaining <= delivery_days + safety_days else 'on_track',
            'note': 'Planning buffer only. A provider must confirm transfer delivery times.'}


def planning_preview(*, amount: float, scholarship: float, available: float,
                     reserve: float, living_per_month: float, months: int,
                     reference_rate: float | None, reference_date: str | None,
                     origin_currency: str, destination_currency: str,
                     deadline: date) -> dict:
    due = _dec(amount) - _dec(scholarship)
    if due < 0:
        raise ValueError('Scholarship cannot exceed tuition.')
    living_dest = _dec(living_per_month) * months
    base = {
        'tuition_due': money(due), 'destination_currency': destination_currency,
        'available': available, 'origin_currency': origin_currency,
        'emergency_reserve': reserve, 'living_buffer_destination': money(living_dest),
        'living_months': months, 'deadline': deadline_check(deadline),
        'rate_basis': 'published reference rate, not a bank quote',
        'reference_date': reference_date,
        'not_a_payment_quote': True,
        'warnings': ['Reference conversions exclude intermediary fees, spreads, taxes and provider eligibility.',
                     'Review your real invoice and get a written provider quote before sending money.']
    }
    if reference_rate is None:
        base.update({'estimated_tuition_origin': None, 'estimated_living_origin': None,
                     'remaining_after_protection': None, 'protection_status': 'unknown',
                     'explanation': 'Current reference conversion unavailable. No rate was estimated or invented.'})
        return base
    if reference_rate <= 0:
        raise ValueError('Reference rate must be positive.')
    rate = _dec(reference_rate)
    required_tuition = due * rate
    required_living = living_dest * rate
    remaining = _dec(available) - _dec(reserve) - required_tuition - required_living
    base.update({'estimated_tuition_origin': money(required_tuition),
                 'estimated_living_origin': money(required_living),
                 'remaining_after_protection': money(remaining),
                 'protection_status': 'indicative_covered' if remaining >= 0 else 'indicative_shortfall',
                 'explanation': ('The reference-rate estimate leaves room for tuition, your selected living-cost buffer and emergency reserve, '
                                 'before any actual transfer fees.' if remaining >= 0 else
                                 'At the reference rate, your funds do not cover tuition, your selected living-cost buffer and emergency reserve. '
                                 'Review your budget and obtain a real bank quote.')})
    return base


def prepare_steps(*, invoice_ready: bool, quote_ready: bool, deadline: date,
                  protection_status: str) -> list[dict]:
    steps = [
        {'id': 'invoice', 'title': 'Confirm your university invoice',
         'detail': 'Check university, amount, currency and bank details on the official document.',
         'status': 'ready_to_review' if invoice_ready else 'needs_input', 'action': 'planner'},
        {'id': 'quote', 'title': 'Compare documented provider quotes',
         'detail': 'Verify provider support, exact fees, delivery time and reference URLs.',
         'status': 'ready_to_review' if quote_ready else 'needs_input', 'action': 'planner'},
        {'id': 'budget', 'title': 'Protect your study budget',
         'detail': 'Keep living expenses and emergency savings separate from tuition.',
         'status': protection_status, 'action': 'twin'},
        {'id': 'calendar', 'title': 'Add a deadline to your calendar',
         'detail': 'Create a downloadable reminder without sending an email or changing your calendar account.',
         'status': 'ready_to_review', 'action': 'download_calendar'},
        {'id': 'approve', 'title': 'Review before any payment',
         'detail': 'No financial transaction runs autonomously. Practice payments require an explicit approval.',
         'status': 'approval_required', 'action': 'pay'},
    ]
    if deadline < date.today():
        steps[3]['status'] = 'overdue'
    return steps


def safe_calendar_text(value: str) -> str:
    # Escape all ICS control characters and newlines to prevent calendar field injection.
    return re.sub(r'([,;\\])', r'\\\1', re.sub(r'[\r\n]+', ' ', value))[:160]


def _fold_ics(line: str, limit: int = 75) -> str:
    chunks=[];part='';length=0
    for char in line:
        size=len(char.encode('utf-8'))
        if length+size>limit and part:
            chunks.append(part);part=' ';length=1
        part+=char;length+=size
    chunks.append(part)
    return '\r\n'.join(chunks)


def calendar_bytes(due: date, name: str = 'University tuition payment', days_before: int = 7) -> bytes:
    if not 0 <= days_before <= 60:
        raise ValueError('Reminder days must be between 0 and 60.')
    event_day = due.strftime('%Y%m%d')
    end_day = (due + timedelta(days=1)).strftime('%Y%m%d')
    title_hash=hashlib.sha256(name.encode('utf-8')).hexdigest()[:12]
    uid = f'{event_day}-{days_before}-{title_hash}@studentbridge.local'
    summary = safe_calendar_text(name)
    now = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    parts = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//StudentBridge AI//Tuition Planner//EN',
             'CALSCALE:GREGORIAN', 'BEGIN:VEVENT', f'UID:{uid}', f'DTSTAMP:{now}',
             f'DTSTART;VALUE=DATE:{event_day}', f'DTEND;VALUE=DATE:{end_day}',
             f'SUMMARY:{summary}', 'DESCRIPTION:Verify the official invoice and provider delivery times. Planning reminder only.',
             'BEGIN:VALARM', 'ACTION:DISPLAY', 'DESCRIPTION:Tuition payment deadline is approaching',
             f'TRIGGER:-P{days_before}D', 'END:VALARM', 'END:VEVENT', 'END:VCALENDAR', '']
    return '\r\n'.join(_fold_ics(part) for part in parts).encode('utf-8')
