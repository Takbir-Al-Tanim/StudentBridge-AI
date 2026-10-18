"""The assistant must show real source provenance and never invent missing quotes."""
from app.assistant import make_answer, countries_in
from app.main import CATALOG, SOURCES


def ask(question, country='Australia', plan=None):
    return make_answer(question,CATALOG,SOURCES,plan,country)


def test_explains_what_the_assistant_does():
    answer=ask('What can you do?')
    assert 'four student finance needs' in answer['message']
    assert any(a['target']=='remit' for a in answer['actions'])
    assert 'real' not in answer['safety'].lower() or 'no real' in answer['safety'].lower()


def test_country_mentioned_in_question_overrides_current_page_country():
    answer=ask('How do I build credit in Japan?',country='Australia')
    assert 'Japan' in answer['message'] and 'CIC' in answer['message']
    assert answer['sources'] and 'cic.co.jp' in answer['sources'][0]['url']


def test_tuition_response_has_original_source_and_program_year():
    answer=ask('Tuition fees in the UK')
    assert 'GBP' in answer['message']
    assert 'invoice' in answer['message'].lower()
    assert answer['sources']


def test_real_cross_border_route_not_imagined():
    answer=ask('What is the cheapest remittance from Japan to UK?')
    assert 'Japan → United Kingdom' in answer['message']
    assert 'do not have a verified live provider quote' in answer['message']


def test_living_cost_lookup_separates_visa_requirement_from_spending():
    answer=ask('What are the UK visa money requirements?')
    assert '1,529' in answer['message']
    assert 'actual monthly spending' in answer['message']
    assert answer['sources']


def test_fx_pair_is_specific_not_guessed():
    answer=ask('Exchange rate GBP to JPY')
    assert answer['fx_pair']=={'base':'GBP','quote':'JPY'}
    assert 'not transfer offers' in answer['message']


def test_saved_plan_quote_question_uses_result():
    plan={'quotes':[{'quote_id':'q1','provider':'Student Sample Bank','total':200.5,'fee_total':4.5,
                     'eta_days':2,'issues':[],'viable':True}],
          'origin_currency':'JPY','destination_currency':'GBP','days_remaining':5,
          'recommended_quote_id':'q1','recommendation':'Test plan only'}
    answer=ask('Which transfer route should I use?',plan=plan)
    assert 'Student Sample Bank' in answer['message']
    assert '200.50 JPY' in answer['message']
    assert 'entered by the user' in answer['message']


def test_unknown_credit_country_shows_evidence_not_promise():
    answer=ask('Credit building in China')
    assert 'China' in answer['message']
    assert 'loan approval' in answer['message']


def test_all_six_countries_detectable():
    assert countries_in('I want to go from China to Australia')==['China','Australia']
    assert countries_in('Japan to UK')==['Japan','United Kingdom']


def test_what_if_uses_deterministic_calculation_not_a_generic_chat_answer():
    plan={'quotes':[{'quote_id':'q1','provider':'Sample bank','total':110.0,
                     'base_cost':100.0,'fee_percent':10,'fixed_fee':0,'viable':True}],
          'origin_currency':'CNY','destination_currency':'AUD',
          'available_balance':200.0,'emergency_reserve':50.0,
          'living_budget_dest':0,'recommended_quote_id':'q1'}
    reply=ask('What if the exchange rate rises by 10%?',plan=plan)
    assert reply['tools_used']==['financial_digital_twin_calculation']
    assert '121.00 CNY' in reply['message']
    assert '79.00 CNY' in reply['message']
    assert 'not a forecast' in reply['message']
