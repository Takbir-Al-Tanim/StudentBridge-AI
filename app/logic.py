"""Transparent deterministic financial calculations. Never assume reference FX = payment quote."""
from __future__ import annotations
from datetime import date, datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

D = lambda v: Decimal(str(v))

def cents(value: Decimal) -> float:
    return float(value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

def evaluate(payload: dict[str, Any], reference: dict | None = None) -> dict:
    origin = payload['origin']; destination = payload['destination']
    if origin == destination:
        raise ValueError('Choose different origin and destination countries.')
    tuition = D(payload['tuition_amount']); scholarship = D(payload.get('scholarship_amount',0))
    available = D(payload['available_balance']); reserve = D(payload.get('emergency_reserve',0))
    monthly = D(payload.get('monthly_living_cost',0)); months = int(payload.get('living_months',0))
    protect_living = bool(payload.get('protect_living_costs', False))
    if min(tuition,scholarship,available,reserve,monthly) < 0 or months < 0:
        raise ValueError('Amounts must be nonnegative.')
    if scholarship > tuition:
        raise ValueError('Scholarship cannot exceed tuition amount for this payment.')
    if reserve > available:
        raise ValueError('Emergency reserve exceeds available balance.')
    required = tuition - scholarship
    today = date.today(); due = date.fromisoformat(payload['deadline'])
    days = (due-today).days
    result=[]
    for idx,q in enumerate(payload.get('quotes',[])):
        # Quote values are USER INPUT even with URL. Do not imply platform verification.
        r=D(q['rate']); fixed=D(q.get('fixed_fee',0)); pct=D(q.get('fee_percent',0)); eta=int(q.get('eta_days',0))
        if r<=0 or fixed<0 or pct<0 or pct>100 or eta<0:
            raise ValueError('Quote rate, fees or delivery estimate are invalid.')
        base=required*r; fee=base*pct/Decimal('100')+fixed; total=base+fee
        protected_living_origin=(monthly*months*r) if protect_living else D(0)
        remaining=available-total; usable=available-reserve-protected_living_origin
        eligible=bool(q.get('eligible',False))
        deadline_ok=eta<=days and days>=0
        affordable=total<=usable
        issues=[]
        if not eligible: issues.append('Route eligibility not confirmed by user')
        if not deadline_ok: issues.append('Estimated delivery does not meet deadline')
        if not affordable: issues.append('Insufficient funds after protected emergency reserve and living-cost buffer' if protect_living else 'Insufficient funds after protected reserve')
        if not q.get('source_url') and not q.get('simulation_only'): issues.append('Missing quote evidence URL')
        exp=q.get('expires_on')
        if exp:
            try:
                if date.fromisoformat(exp)<today: issues.append('Quote expired')
            except ValueError: issues.append('Invalid quote expiry date')
        viable=eligible and deadline_ok and affordable and (bool(q.get('source_url')) or bool(q.get('simulation_only'))) and not any(x in issues for x in ['Quote expired','Invalid quote expiry date'])
        result.append({
          'quote_id':q.get('id') or f'quote-{idx+1}', 'provider':q['provider'][:100], 'rate':float(r),
          'fixed_fee':float(fixed),'fee_percent':float(pct),'eta_days':eta,
          'base_cost':cents(base),'fee_total':cents(fee),'total':cents(total),
          'remaining':cents(remaining),'reserve_maintained':affordable,'deadline_ok':deadline_ok,
          'protected_living_origin':cents(protected_living_origin),
          'viable':viable,'eligible_by_user':eligible, 'issues':issues,
          'source_url':q.get('source_url') or None,'expires_on':exp or None,
          'provenance':('ILLUSTRATIVE_SANDBOX_OPTION_NOT_A_REAL_PROVIDER' if q.get('simulation_only') else 'USER_ENTERED_QUOTE_NOT_INDEPENDENTLY_VERIFIED'), 'simulation_only':bool(q.get('simulation_only')), 
          'destination_received':cents(required)
        })
    result.sort(key=lambda x:(not x['viable'],x['total'],x['eta_days']))
    best=next((q for q in result if q['viable']),None)
    if best:
        statement=(f"{best['provider']} is the lowest-cost demo option that fits your entered budget and deadline. Fees, provider and delivery times are illustrative. No real transfer can occur." if best.get('simulation_only') else f"{best['provider']} is the lowest-cost quote among those that pass the entered deadline, budget, and eligibility checks. Verify it directly with the provider before transferring real funds.")
    elif result:
        statement='No entered quote meets every required condition. Review the issues; do not initiate a payment based on this plan.'
    else:
        statement='No provider quotes were entered. A reference FX estimate is informational only, not an executable transfer offer.'
    ref_estimate=cents(required*D(reference['rate'])) if reference and reference.get('rate') else None
    return {
      'origin':origin,'destination':destination,'origin_currency':payload['origin_currency'],
      'destination_currency':payload['destination_currency'],'university':payload.get('university',''),
      'tuition_amount':cents(tuition),'scholarship_amount':cents(scholarship),'required_tuition':cents(required),
      'available_balance':cents(available),'emergency_reserve':cents(reserve),
      'monthly_living_cost':cents(monthly),'living_months':months,'protect_living_costs':protect_living,
      'living_budget_dest':cents(monthly*months),'deadline':str(due),'days_remaining':days,
      'quotes':result,'recommended_quote_id':best['quote_id'] if best else None,
      'recommendation':statement,'reference_rate':reference,'reference_only_estimate':ref_estimate,
      'source_type':'REAL_REFERENCE_OR_USER_ENTERED_QUOTE',
      'generated_at':datetime.now(timezone.utc).isoformat(),
      'cautions':['No real-money payment functionality is connected.', 'Provider quotes are user-entered, not independently checked.',
                  'Reference FX does not include transaction charges or spread.','Country rules and recipient details must be independently confirmed.']
    }

def simulate(plan:dict, change_percent:float, extra_fee:float=0, living_cost_change:float=0)->dict:
    if not -80<=change_percent<=200 or not 0<=extra_fee<=1e9 or not -80<=living_cost_change<=200:
        raise ValueError('Scenario inputs outside permitted range.')
    quote=next((q for q in plan['quotes'] if q['quote_id']==plan['recommended_quote_id']),None)
    if not quote:
        return {'ready':False,'message':'Add a suitable provider quote to use the stress test.'}
    fx_mult=D(1)+D(change_percent)/100
    original_base=D(quote['base_cost']); fixed=D(quote['fixed_fee']); pct=D(quote['fee_percent'])
    adjusted_base=original_base*fx_mult
    adjusted_total=adjusted_base*(1+pct/100)+fixed+D(extra_fee)
    remain=D(plan['available_balance'])-adjusted_total
    living=D(plan['living_budget_dest'])*(1+D(living_cost_change)/100)
    return {'ready':True,'scenario_total':cents(adjusted_total),'baseline_total':quote['total'],
            'cost_change':cents(adjusted_total-D(quote['total'])),'remaining_origin_currency':cents(remain),
            'reserve_protected':remain>=D(plan['emergency_reserve']),
            'living_requirement_destination_currency':cents(living),
            'message':'Scenario only. No exchange-rate prediction, provider guarantee or real payment.'}
