'use strict';
let catalog=null, activePlan=null, activeRef=null, quotesSerial=0;
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const fmt=(n,c)=>new Intl.NumberFormat('en-US',{maximumFractionDigits:2,minimumFractionDigits:2}).format(Number(n||0))+(c?' '+c:'');
const escapeHTML=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const toast=(msg,error=false)=>{const t=$('#toast');t.textContent=msg;t.classList.remove('hidden');t.classList.toggle('error',error);clearTimeout(window.__toastTimer);window.__toastTimer=setTimeout(()=>t.classList.add('hidden'),4400)};
async function api(url,opts={}){let r;try{r=await fetch(url,opts)}catch(e){throw new Error('Cannot reach the backend. Start the Python server first.')}const j=await r.json().catch(()=>({}));if(!r.ok)throw new Error(typeof j.detail==='string'?j.detail:JSON.stringify(j.detail||'Request failed'));return j}
const json=(obj)=>({method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(obj)});
const countryObj=name=>catalog.countries.find(c=>c.name===name);
const countryC=name=>countryObj(name)?.currency||'?';
const sourceById=id=>catalog.sources.find(s=>s.id===id);
function showView(name){$$('.view').forEach(x=>x.classList.toggle('active',x.id===name));$$('.nav-link').forEach(x=>x.classList.toggle('active',x.dataset.target===name));$('#breadcrumb-current').textContent=({overview:'Home',remit:'Send money',pay:'Tuition payments',planner:'Compare payment routes',currencies:'My currencies',twin:'My budget',credit:'Build credit',sources:'Our data',activity:'Payment history'})[name]||name;window.scrollTo({top:0,behavior:'smooth'});if(name==='activity')loadActivity()}
function countrySelect(id,selected){$(id).innerHTML=catalog.countries.map(c=>`<option value="${escapeHTML(c.name)}" ${selected===c.name?'selected':''}>${c.flag} ${c.name}</option>`).join('')}
function updateCountries(){const orig=$('#origin').value,dest=$('#destination').value;const corridor=orig+'|'+dest;if(window.__lastCorridor&&window.__lastCorridor!==corridor){$('#tuition').value='';$('#quote-list').innerHTML='';activePlan=null;$('#plan-placeholder').classList.remove('hidden');$('#plan-output').classList.add('hidden');$('#plan-status').textContent='NOT ANALYZED';$('#plan-message').classList.add('hidden');}window.__lastCorridor=corridor;$('#origin-currency-pill').textContent=countryC(orig);$('#dest-currency-pill').textContent=countryC(dest);$('#t-currency').textContent=countryC(dest);$('#living-currency').textContent=countryC(dest);$('#a-currency').textContent=countryC(orig);let options=catalog.tuition.filter(t=>t.country===dest);$('#university').innerHTML='<option value="">Choose university or enter manually</option>'+options.map(t=>`<option value="${escapeHTML(t.id)}">${escapeHTML(t.institution)} · ${escapeHTML(t.program)}</option>`).join('');activeRef=null;$('#ref-rate').textContent='Not loaded';$('#ref-date').textContent='Fetch published reference FX, not a bank quote.';$('#tuition-source-note').textContent='Choose a program to see its official evidence link and enter actual payable amount.';const fb=(catalog.financial_benchmarks||[]).filter(x=>x.country===dest && (x.category.includes('visa_') || x.category==='student_living_cost_estimate' || x.category==='student_living_cost_estimate_lower')).slice(0,3);$('#destination-research-note').innerHTML=fb.length?'<strong>Published '+escapeHTML(dest)+' references:</strong> '+fb.map(x=>`${escapeHTML(x.label)}: ${fmt(x.amount,x.currency)} (${escapeHTML(x.unit||'')}; ${escapeHTML(x.period||'published')})`).join(' · ')+'<br><small>Financial requirement ≠ actual living expense. See Data & sources for evidence.</small>':'No suitable published financial benchmark in the local research collection. Enter your real costs manually.';if(orig===dest)toast('Select two different countries.',true)}
function handleUni(){const t=catalog.tuition.find(t=>t.id===$('#university').value);if(!t)return;if(t.input_ready===false)$('#tuition').value='';else if(t.amount!==null)$('#tuition').value=t.amount;const s=sourceById(t.source_id);$('#tuition-source-note').innerHTML=t.amount!==null?`<strong>${escapeHTML(t.program)}:</strong> ${fmt(t.amount,t.currency)} for ${escapeHTML(t.period)} (${escapeHTML(t.year)}). <a href="${escapeHTML(s?.url||'#')}" target="_blank" rel="noopener">View official source ↗</a><br>Confirm the exact amount on your invoice.`:`${escapeHTML(t.note)} ${s?`<a href="${escapeHTML(s.url)}" target="_blank" rel="noopener">Official source ↗</a>`:''}`}
function createQuote(){quotesSerial++;let id='user-quote-'+quotesSerial;const el=document.createElement('div');el.className='quote-card';el.dataset.quoteId=id;el.innerHTML=`<button class="quote-remove" aria-label="Remove quote" title="Remove this quote">×</button><div class="quote-title">PROVIDER QUOTE ${quotesSerial} <span style="color:#a8b8a9;font-weight:500">· entered by you</span></div><div class="quote-grid"><div class="field"><label>PROVIDER NAME</label><input data-quote="provider" placeholder="Bank / payment service"></div><div class="field"><label>EXACT QUOTED RATE (${escapeHTML(countryC($('#origin').value))} PER ${escapeHTML(countryC($('#destination').value))})</label><input data-quote="rate" type="number" min=".00000001" step="any" placeholder="From provider quote"></div><div class="field"><label>FIXED FEE (${escapeHTML(countryC($('#origin').value))})</label><input data-quote="fixed_fee" type="number" min="0" step="any" value="0"></div><div class="field"><label>FEE AS % OF CONVERTED AMOUNT</label><input data-quote="fee_percent" type="number" min="0" max="100" step="any" value="0"></div><div class="field"><label>EST. DELIVERY (DAYS)</label><input data-quote="eta_days" type="number" min="0" value="3"></div><div class="field"><label>QUOTE EXPIRY (IF ANY)</label><input data-quote="expires_on" type="date"></div><div class="field" style="grid-column:1/-1"><label>HTTPS QUOTE / PROVIDER EVIDENCE URL</label><input data-quote="source_url" type="url" placeholder="https://... (required for shortlist)"></div></div><label class="check-line"><input type="checkbox" data-quote="eligible"> I checked with the provider that this exact country pair and purpose are eligible.</label>`;$('#quote-list').appendChild(el);el.querySelector('.quote-remove').onclick=()=>el.remove();return el}
function readQuotes(){return $$('.quote-card').map(el=>{const v=k=>el.querySelector(`[data-quote="${k}"]`).value;return {id:el.dataset.quoteId,provider:v('provider'),rate:Number(v('rate')),fixed_fee:Number(v('fixed_fee')),fee_percent:Number(v('fee_percent')),eta_days:Number(v('eta_days')),expires_on:v('expires_on')||null,source_url:v('source_url')||null,eligible:el.querySelector('[data-quote="eligible"]').checked}})}
async function fetchReference(){const b=countryC($('#destination').value),q=countryC($('#origin').value);$('#ref-rate').textContent='Fetching…';let result=await api(`/api/fx?base=${encodeURIComponent(b)}&quote=${encodeURIComponent(q)}`);if(result.available){activeRef=result;$('#ref-rate').textContent=`1 ${b} = ${fmt(result.rate,q)}`;$('#ref-date').textContent=`Observation: ${result.date||'latest published'} · Reference market rate, no transfer fees.`;toast('Reference FX loaded. Provider quotes must still be entered separately.')}else{activeRef=null;$('#ref-rate').textContent='Unavailable';$('#ref-date').textContent='Could not reach the API. No rate has been guessed.';toast('FX API unavailable; enter a documented provider quote for real planning.',true)}}
async function buildPlan(){let btn=$('#build-plan');btn.disabled=true;btn.textContent='Analyzing your plan…';try{const req={origin:$('#origin').value,destination:$('#destination').value,origin_currency:countryC($('#origin').value),destination_currency:countryC($('#destination').value),university:catalog.tuition.find(x=>x.id===$('#university').value)?.institution||'Student entered',tuition_amount:Number($('#tuition').value),scholarship_amount:Number($('#scholarship').value),available_balance:Number($('#available').value),emergency_reserve:Number($('#reserve').value),monthly_living_cost:Number($('#living').value||0),living_months:Number($('#months').value||0),deadline:$('#deadline').value,reference_rate:activeRef?.rate||null,reference_source:activeRef?'FRANKFURTER_LIVE':null,reference_date:activeRef?.date||null,reference_proof:activeRef?.proof||null,quotes:readQuotes()};if(!req.deadline)throw new Error('Please enter a tuition payment deadline.');if(req.tuition_amount<=0)throw new Error('Enter a tuition amount greater than zero.');if(!$('#available').value)throw new Error('Enter available funds, even if the available amount is zero.');activePlan=await api('/api/plans',json(req));renderPlan();$('#plan-message').classList.add('hidden');toast('Your comparison is ready. Ask Bridge AI to explain any option.')}catch(e){$('#plan-message').classList.remove('hidden');$('#plan-message').textContent=e.message;toast(e.message,true)}finally{btn.disabled=false;btn.innerHTML='Compare my options <span>→</span>'}}
function renderPlan(){let p=activePlan;$('#plan-placeholder').classList.add('hidden');$('#plan-output').classList.remove('hidden');$('#plan-status').textContent=p.recommended_quote_id?'CONDITIONALLY VIABLE':'REVIEW REQUIRED';$('#plan-required').textContent=fmt(p.required_tuition,p.destination_currency);$('#plan-corridor').textContent=p.origin+' → '+p.destination;$('#plan-days').textContent=p.days_remaining+' day(s)';$('#plan-reference').textContent=p.reference_only_estimate===null?'Not available':fmt(p.reference_only_estimate,p.origin_currency);$('#plan-recommendation').textContent=p.recommendation;$('#quote-results').innerHTML=p.quotes.length?p.quotes.map(q=>`<div class="quote-result"><div class="quote-top"><span>${escapeHTML(q.provider)}</span><span class="${q.viable?'status-good':'status-bad'}">${q.viable?'PASS CONDITIONS':'REVIEW'}</span></div><strong>${fmt(q.total,p.origin_currency)}</strong><small>Fees ${fmt(q.fee_total,p.origin_currency)} • ${q.eta_days} estimated days • user-supplied quote</small>${q.issues.length?`<small class="error">${escapeHTML(q.issues.join(' · '))}</small>`:''}</div>`).join(''):'<div class="result-inline">No provider quotes submitted. Real reference-rate conversion does not establish a payable total.</div>'}
function showModal(html){$('#modal-content').innerHTML=html;$('#modal-overlay').classList.remove('hidden')}
function closeModal(){$('#modal-overlay').classList.add('hidden')}
async function passport(){if(!activePlan){toast('Create a plan first',true);return}const p=await api('/api/passport/'+activePlan.plan_id);const rows=[['Plan ID',p.plan_id],['Goal',p.goal],['Recommended route',p.recommended_quote_id||'None suitable'],['Evidence',p.reference_rate?.classification||'No market reference'],['Generated',new Date(p.date).toLocaleString()],['SHA-256 digest',p.integrity_hash.slice(0,25)+'…']];showModal(`<div class="eyebrow">INNOVATION 03 / EXPLAINABILITY</div><h2>Decision Passport</h2><p>Each decision carries the information needed to review it. This is not proof that a bank or regulator has approved a transaction.</p>${rows.map(r=>`<div class="passport-row"><span>${escapeHTML(r[0])}</span><strong>${escapeHTML(r[1])}</strong></div>`).join('')}<div class="passport-caption">${escapeHTML(p.reasoning)}</div><p style="margin-top:16px">Cautions: ${escapeHTML(p.limitations.join(' · '))}</p><button class="btn primary full" id="download-passport">Download passport (JSON) ↓</button>`);$('#download-passport').onclick=()=>{const blob=new Blob([JSON.stringify(p,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=`studentbridge-passport-${p.plan_id}.json`;a.click();URL.revokeObjectURL(url)}}
function approvalModal(){if(!activePlan){toast('Build a plan first',true);return}const p=activePlan,q=p.quotes.find(q=>q.quote_id===p.recommended_quote_id);if(!q){toast('No quote meets the entered conditions. Simulation is blocked.',true);return}showModal(`<div class="eyebrow">SIMULATED EXECUTION / NO BANK CONNECTION</div><h2>Review your sandbox payment</h2><p>This will create a test transaction in your local audit ledger. <strong>No real money or account is involved.</strong> Even passing routes are based on unverified user-entered quotes.</p><div class="passport-row"><span>Sending</span><strong>${escapeHTML(p.origin)} → ${escapeHTML(p.destination)}</strong></div><div class="passport-row"><span>Provider (user entered)</span><strong>${escapeHTML(q.provider)}</strong></div><div class="passport-row"><span>Total sandbox debit</span><strong>${fmt(q.total,p.origin_currency)}</strong></div><div class="passport-row"><span>Recipient receives (assumed)</span><strong>${fmt(p.required_tuition,p.destination_currency)}</strong></div><label class="approval-box"><input type="checkbox" id="approval-check"><span>I reviewed the amount and chosen option. I understand this is a <strong>simulation only</strong> and confirm I want to execute this sandbox action.</span></label><button class="btn primary full" id="confirm-pay">Approve & execute simulation ↗</button>`);$('#confirm-pay').onclick=async()=>{if(!$('#approval-check').checked){toast('You must confirm the simulated transaction.',true);return}const b=$('#confirm-pay');b.disabled=true;b.textContent='Creating sandbox transaction…';try{const t=await api('/api/sandbox/execute',json({plan_id:p.plan_id,quote_id:q.quote_id,confirmed:true,approval_phrase:'APPROVE SANDBOX',idempotency_key:'SB-'+crypto.randomUUID()}));showModal(`<div class="eyebrow">SANDBOX EXECUTION COMPLETE</div><h2>Payment simulation created ✓</h2><div class="passport-caption">NO REAL MONEY MOVED. This is a test ledger transaction only.</div><div class="passport-row"><span>Transaction</span><strong>${escapeHTML(t.transaction_id)}</strong></div><div class="passport-row"><span>State</span><strong>${escapeHTML(t.status)}</strong></div><div class="passport-row"><span>Test amount</span><strong>${fmt(t.amount,t.currency)}</strong></div><button class="btn primary full" id="view-activity">View audit trail ↗</button>`);$('#view-activity').onclick=()=>{closeModal();showView('activity')}}catch(e){toast(e.message,true);b.disabled=false;b.textContent='Approve & execute simulation ↗'}}}
async function runScenario(){if(!activePlan){toast('Build a plan first',true);return}let values={plan_id:activePlan.plan_id,fx_change_percent:Number($('#fx-change').value),extra_fee:Number($('#extra-fee').value),living_cost_change_percent:Number($('#living-change').value)};try{const d=await api('/api/scenarios',json(values));if(!d.ready){toast(d.message,true);return}$('#twin-empty').classList.add('hidden');$('#twin-output').classList.remove('hidden');let cc=activePlan.origin_currency;$('#scenario-cost').textContent=fmt(d.scenario_total,cc);$('#scenario-change').textContent=(d.cost_change>=0?'+':'')+fmt(d.cost_change,cc)+' compared with baseline';$('#baseline-value').textContent=fmt(d.baseline_total,cc);$('#stress-value').textContent=fmt(d.scenario_total,cc);let m=Math.max(d.baseline_total,d.scenario_total,1);$('#baseline-bar').style.width=(100*d.baseline_total/m)+'%';$('#stress-bar').style.width=(100*d.scenario_total/m)+'%';$('#reserve-badge').textContent=d.reserve_protected?'✓ Protected reserve survives':'! Protected reserve is at risk';$('#scenario-remaining').textContent=`Remaining: ${fmt(d.remaining_origin_currency,cc)} · Living-cost scenario: ${fmt(d.living_requirement_destination_currency,activePlan.destination_currency)}. These assumptions are hypothetical.`;toast('Digital Twin scenario calculated.')}catch(e){toast(e.message,true)}}
function paintSources(){
 const list=[...catalog.sources].sort((a,b)=>a.country.localeCompare(b.country));
 $('#source-count').textContent=list.length;
 $('#sources-list').innerHTML=list.map(s=>`<article class="source-card"><div class="source-country">${escapeHTML(s.country)} · ${escapeHTML(s.category.toUpperCase().replaceAll('_',' '))}</div><h3>${escapeHTML(s.title)}</h3><p>${escapeHTML(s.notes||'')}</p><small>${escapeHTML(s.status||'SOURCE RECORDED')}</small><p><a href="${escapeHTML(s.url)}" target="_blank" rel="noopener noreferrer">View original source ↗</a></p></article>`).join('');
 let bench=catalog.financial_benchmarks||[];
 $('#research-benchmarks').innerHTML=bench.map(b=>`<article class="source-card"><div class="source-country">${escapeHTML(b.country)} · ${escapeHTML(b.category.replaceAll('_',' '))}</div><h3>${escapeHTML(b.label)}</h3><p><strong>${fmt(b.amount,b.currency)}</strong> ${escapeHTML(b.unit||'')} · ${escapeHTML(b.geography||'')}</p><p>${escapeHTML(b.note||'')} ${escapeHTML(b.period||'')}</p>${b.source_url?`<a href="${escapeHTML(b.source_url)}" target="_blank" rel="noopener noreferrer">Published source ↗</a>`:''}</article>`).join('');
 const hist=(catalog.historical_reference_fx||[]).filter(x=>x.rate!==null);
 $('#research-fx').innerHTML=hist.map(x=>`<article class="source-card"><div class="source-country">${escapeHTML(x.rate_date||'HISTORICAL')} · REFERENCE ONLY</div><h3>1 ${escapeHTML(x.base)} = ${fmt(x.rate,x.quote)}</h3><p>${escapeHTML(x.note||'Not an executable provider quote.')}</p>${x.source_url?`<a href="${escapeHTML(x.source_url)}" target="_blank" rel="noopener noreferrer">Original FX source ↗</a>`:''}</article>`).join('');
}
function creditCountry(country){const c=catalog.credit_guidance[country],s=sourceById(c.source_id);$('#credit-body').innerHTML=`<div class="eyebrow">${escapeHTML(country.toUpperCase())} · FINANCIAL READINESS</div><h3>${escapeHTML(c.title)}</h3><p>Learn the correct steps before applying for banking or credit products in a new country.</p><div class="credit-steps">${c.steps.map((step,i)=>`<div class="credit-step"><span>${String(i+1).padStart(2,'0')}</span>${escapeHTML(step)}</div>`).join('')}</div><div class="passport-caption">${escapeHTML(c.disclaimer)}</div><p style="margin-top:17px">${s?`<a href="${escapeHTML(s.url)}" target="_blank" rel="noopener">Official / primary reference ↗</a>`:'Specific eligibility must be checked at the source.'}</p>`;$$('.credit-tabs button').forEach(b=>b.classList.toggle('active',b.dataset.country===country))}
function initCredit(){const names=catalog.countries.map(c=>c.name);$('#credit-tabs').innerHTML=names.map(c=>`<button data-country="${escapeHTML(c)}">${countryObj(c).flag} ${escapeHTML(c)}</button>`).join('');$$('.credit-tabs button').forEach(b=>b.onclick=()=>creditCountry(b.dataset.country));creditCountry('Australia')}
async function loadActivity(){try{const [t,a]=await Promise.all([api('/api/sandbox/history'),api('/api/audit')]);$('#transactions-list').innerHTML=t.transactions.length?t.transactions.map(tx=>`<div class="activity-item"><span class="activity-dot"></span><div><strong>${escapeHTML(tx.id)}</strong><small>${escapeHTML(tx.status)} · ${fmt(tx.approved_amount,tx.currency)} · ${new Date(tx.created_at).toLocaleString()}</small><small>LOCAL SANDBOX • NO REAL MONEY</small></div></div>`).join(''):'<p class="muted">No sandbox transactions yet. Approve a viable test route in the planner to create an audit record.</p>';$('#audit-list').innerHTML=a.audit_events.length?a.audit_events.map(x=>`<div class="activity-item"><span class="activity-dot"></span><div><strong>${escapeHTML(x.event_type)}</strong><small>${escapeHTML(x.object_id)} · ${new Date(x.occurred_at).toLocaleString()}</small><small>Hash: ${escapeHTML(x.event_hash.slice(0,22))}…</small></div></div>`).join(''):'<p class="muted">No decisions recorded yet.</p>'}catch(e){toast(e.message,true)}}
async function invoiceUpload(file){if(!file)return;if(file.size>2500000){toast('Invoice must be smaller than 2.5 MB.',true);return}let fd=new FormData();fd.append('file',file);try{let r=await api('/api/invoices/analyze',{method:'POST',body:fd});let area=$('#invoice-result');area.classList.remove('hidden');let f=r.fields||{};area.innerHTML=`<strong>${r.text_found?'Possible invoice fields extracted':'No selectable invoice text'}</strong><br>${escapeHTML(r.warning)}${f.amount_candidates?`<br>Amounts to verify: ${escapeHTML(f.amount_candidates.join(', ')||'None detected')}`:''}${f.date_candidates?`<br>Dates to verify: ${escapeHTML(f.date_candidates.join(', ')||'None detected')}`:''}${r.has_suspicious_instructions?'<br><strong>⚠ Suspicious embedded instructions detected.</strong>':''}`;toast('Invoice inspected. Review values manually.')}catch(e){toast(e.message,true)}}
let chatBusy=false;
function addAssistantButton(actions, host){
  if(!Array.isArray(actions)||!actions.length)return;
  const container=document.createElement('div');container.className='agent-actions';
  const allowed=new Set(['overview','pay','planner','twin','credit','sources','activity']);
  for(const a of actions){
    if(!allowed.has(a.target))continue;
    const button=document.createElement('button');button.type='button';button.className='agent-action';
    button.textContent=a.label+' →';
    button.onclick=()=>{showView(a.target);if(a.target==='planner')$('#origin').focus()};
    container.appendChild(button);
  }
  host.appendChild(container);
}
function addAssistantSources(sources,host){
  if(!Array.isArray(sources)||!sources.length)return;
  const wrap=document.createElement('div');wrap.className='agent-sources';
  const headline=document.createElement('strong');headline.textContent='Check the original sources';wrap.appendChild(headline);
  for(const s of sources){
    if(!/^https:\/\/[^\s]+$/.test(s.url||''))continue;
    const a=document.createElement('a');a.href=s.url;a.textContent=(s.title||'View source')+' ↗';
    a.target='_blank';a.rel='noopener noreferrer';wrap.appendChild(a);
  }
  host.appendChild(wrap);
}
async function askChat(message){
  const msg=String(message||'').trim();if(!msg||chatBusy)return;
  chatBusy=true;
  const pane=$('#chat-messages');const send=$('#chat-form button[type="submit"]');
  send.disabled=true;send.setAttribute('aria-busy','true');
  const user=document.createElement('div');user.className='chat-user';user.textContent=msg;pane.appendChild(user);
  const thinking=document.createElement('div');thinking.className='chat-ai';
  const avatar=document.createElement('span');avatar.className='chat-avatar';avatar.textContent='✳';avatar.setAttribute('aria-hidden','true');
  const bubble=document.createElement('div');bubble.className='chat-bubble';bubble.textContent='Checking the available information…';
  const dots=document.createElement('span');dots.className='chat-loading-dots';dots.setAttribute('aria-hidden','true');
  dots.innerHTML='<i></i><i></i><i></i>';bubble.appendChild(dots);
  thinking.append(avatar,bubble);pane.appendChild(thinking);pane.scrollTop=pane.scrollHeight;
  try{
    const result=await api('/api/chat',json({message:msg,plan_id:activePlan?.plan_id||null,country:$('#destination').value}));
    bubble.textContent=result.message;
    addAssistantSources(result.sources,bubble);
    addAssistantButton(result.actions,bubble);
    if(result.ai_explanation){
      const expl=document.createElement('details');expl.className='agent-optional';
      const label=document.createElement('summary');label.textContent='Optional AI wording';
      const body=document.createElement('p');body.textContent=result.ai_explanation;
      expl.append(label,body);bubble.appendChild(expl);
    }
    const trace=document.createElement('div');trace.className='chat-trace';
    const names=(result.tools_used||[]).map(s=>s.replaceAll('_',' ')).join(', ');
    trace.textContent='Checked with: '+names+'.';bubble.appendChild(trace);
  }catch(e){bubble.textContent='I could not answer right now. '+e.message;}
  finally{chatBusy=false;send.disabled=false;send.removeAttribute('aria-busy');pane.scrollTop=pane.scrollHeight;}
}
function pair(origin,dest){$('#origin').value=origin;$('#destination').value=dest;updateCountries();showView('planner')}

/* V4 country-pair animation: preview only, not a live payment feed. */
function initVisibleRouteAnimation(){
  const hero=$('#studentbridge-animated-hero');
  if(!hero)return;
  const routes=[['China','Australia'],['Japan','United Kingdom'],['South Korea','Japan'],['Australia','China'],['Bangladesh','South Korea'],['United Kingdom','Bangladesh']];
  const label=$('#hero-route-name'),btn=$('#hero-motion-toggle'),use=$('#hero-route-try');
  const svg=hero.querySelector('.route-network');
  const prefersReduced=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let index=0,paused=!!prefersReduced,timer=null;
  function display(){const [a,b]=routes[index];label.textContent=a+' → '+b;use.setAttribute('aria-label','Plan from '+a+' to '+b);}
  function resetProgress(){const el=$('#hero-route-progress');el.style.animation='none';void el.offsetWidth;el.style.animation='';}
  function sync(){hero.classList.toggle('motion-paused',paused);btn.textContent=paused?'Play ▶':'Pause ◼';btn.setAttribute('aria-pressed',String(paused));btn.setAttribute('aria-label',paused?'Play country route animation':'Pause country route animation');if(svg){if(paused&&typeof svg.pauseAnimations==='function')svg.pauseAnimations();else if(!paused&&typeof svg.unpauseAnimations==='function')svg.unpauseAnimations()}if(timer)clearInterval(timer);timer=null;if(!paused){resetProgress();timer=setInterval(()=>{if(document.visibilityState!=='visible')return;index=(index+1)%routes.length;display();resetProgress();},4300);}}
  btn.addEventListener('click',()=>{paused=!paused;sync();});
  use.addEventListener('click',()=>{const [a,b]=routes[index];pair(a,b);});
  document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden'&&timer){clearInterval(timer);timer=null;}else if(document.visibilityState==='visible'&&!paused){sync();}});
  display();sync();
}


/* StudentBridge V5: Four-step sandbox payment checkout.
   Example fees/methods are labeled fictional; server validates amount, available
   balance, protected reserve, deadline, approval and duplicate submissions. */
let demoPlan=null,demoSelected=null,demoReference=null,demoReceipt=null,demoBusy=false;
const demoStep=n=>{$$('.demo-stage').forEach((el,i)=>el.classList.toggle('hidden',i!==n-1));$$('[data-demo-step]').forEach(el=>el.classList.toggle('current',Number(el.dataset.demoStep)===n));window.scrollTo({top:0,behavior:'smooth'})};
function openBridgeAI(){$('#assistant-panel').classList.remove('assistant-closed');$('#assistant-panel').classList.add('assistant-open');$('#chat-input').focus()}
function closeBridgeAI(){$('#assistant-panel').classList.add('assistant-closed');$('#assistant-panel').classList.remove('assistant-open')}
function demoCountryChange(){
 const orig=$('#demo-origin').value,dest=$('#demo-destination').value;
 $('#demo-origin-currency').textContent=countryC(orig);
 $('#demo-dest-currency').textContent=countryC(dest);
 $('#demo-rate-base').textContent=countryC(dest);
 $('#demo-rate-quote').textContent=countryC(orig);
 demoReference=null;$('#demo-rate').value='';
 $('#demo-fx-note').textContent='Get a published reference rate, or enter a rate labeled as a demo value. This is not a bank quote.';
}
async function demoFetchRate(){
 const button=$('#demo-fetch-rate');button.disabled=true;button.textContent='Loading…';
 try{const base=countryC($('#demo-destination').value),quote=countryC($('#demo-origin').value);
   const r=await api(`/api/fx?base=${encodeURIComponent(base)}&quote=${encodeURIComponent(quote)}`);
   if(r.available){demoReference=r;$('#demo-rate').value=r.rate;$('#demo-fx-note').textContent=`Published reference rate dated ${r.date||'date not supplied'} from Frankfurter. This is not a bank quote; the practice payment adds fictional fees.`;toast('Published reference rate loaded.');}
   else{demoReference=null;$('#demo-fx-note').textContent='Reference rate unavailable. Enter a sample rate to continue the practice payment; it will be labeled as user-entered.';toast('Live rate unavailable. You can use a clearly labeled practice rate.',true)}
 }catch(e){toast(e.message,true)}finally{button.disabled=false;button.textContent='Get published rate'}
}
async function demoCompare(){
 if(demoBusy)return;
 const origin=$('#demo-origin').value,destination=$('#demo-destination').value;
 const rate=Number($('#demo-rate').value),tuition=Number($('#demo-amount').value),balance=Number($('#demo-balance').value);
 const reserve=Number($('#demo-reserve').value),deadline=$('#demo-deadline').value;
 if(origin===destination){toast('Choose two different countries.',true);return}
 if(!tuition||tuition<=0||!balance||balance<=0||!rate||rate<=0||!deadline){toast('Enter tuition, available money, exchange rate and payment deadline.',true);return}
 if(reserve>balance){toast('Savings to keep cannot be larger than your available balance.',true);return}
 demoBusy=true;$('#demo-compare').disabled=true;
 try{
   const r=await api('/api/demo/prepare',json({origin,destination,tuition_amount:tuition,available_balance:balance,
    emergency_reserve:reserve,deadline,rate,university:$('#demo-university').value||'University (practice)',
    reference_date:demoReference&&Math.abs(Number(demoReference.rate)-rate)<1e-10?demoReference.date:null,
    reference_proof:demoReference&&Math.abs(Number(demoReference.rate)-rate)<1e-10?demoReference.proof:null}));
   demoPlan=r;demoSelected=r.recommended_quote_id;
   $('#demo-methods').innerHTML=r.quotes.map(q=>`<label class="demo-method ${q.viable?'':'is-disabled'}">
    <input type="radio" name="demo-method" value="${escapeHTML(q.quote_id)}" ${q.quote_id===demoSelected?'checked':''} ${!q.viable?'disabled':''}>
    <span class="demo-method-body"><strong>${escapeHTML(q.provider)}</strong><span>${q.eta_days} day(s) estimated · Sample fee ${q.fee_percent}%</span><b>${fmt(q.total,r.origin_currency)}</b><small>${q.viable?'Fits entered budget and deadline':escapeHTML(q.issues.join('. '))}</small></span></label>`).join('');
   demoStep(2);
   if(!r.recommended_quote_id)toast('No method fits your balance and deadline. Edit details and try again.',true);
 }catch(e){toast(e.message,true)}finally{demoBusy=false;$('#demo-compare').disabled=false}
}
function demoToReview(){
 if(!demoPlan){toast('Enter payment details first.',true);return}
 const selected=document.querySelector('input[name="demo-method"]:checked');if(!selected){toast('Choose an available practice payment method.',true);return}
 demoSelected=selected.value;const q=demoPlan.quotes.find(i=>i.quote_id===demoSelected);if(!q||!q.viable){toast('The selected method does not meet the checks.',true);return}
 const p=demoPlan;
 $('#demo-review-details').innerHTML=`<div class="demo-summary-row"><span>From / To</span><strong>${escapeHTML(p.origin)} → ${escapeHTML(p.destination)}</strong></div>
 <div class="demo-summary-row"><span>Recipient</span><strong>${escapeHTML(p.university)}</strong></div>
 <div class="demo-summary-row"><span>Student pays</span><strong>${fmt(q.total,p.origin_currency)}</strong></div>
 <div class="demo-summary-row"><span>Payment amount</span><strong>${fmt(p.required_tuition,p.destination_currency)}</strong></div>
 <div class="demo-summary-row"><span>Example service fee</span><strong>${fmt(q.fee_total,p.origin_currency)}</strong></div>
 <div class="demo-summary-row"><span>Payment option</span><strong>${escapeHTML(q.provider)}</strong></div>
 <div class="demo-summary-row"><span>Estimated time</span><strong>${q.eta_days} day(s) (illustrative)</strong></div>
 <div class="demo-summary-total"><span>Total test debit</span><strong>${fmt(q.total,p.origin_currency)}</strong></div>
 <p class="demo-warning">Sample fees and transfer times, not actual provider quotes. No real payment is possible here.</p>`;
 $('#demo-consent').checked=false;demoStep(3)
}
async function demoExecute(){
 if(demoBusy)return;
 if(!$('#demo-consent').checked){toast('Please check the simulation approval box.',true);return}
 const q=demoPlan.quotes.find(i=>i.quote_id===demoSelected);
 if(!q||!q.viable){toast('This test method is not eligible.',true);return}
 demoBusy=true;const btn=$('#demo-pay-now');btn.disabled=true;btn.textContent='Saving practice payment…';
 try{
   const idempotency=window.crypto?.randomUUID?.() || ('sb-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2));
   const t=await api('/api/sandbox/execute',json({plan_id:demoPlan.plan_id,quote_id:demoSelected,confirmed:true,
    approval_phrase:'APPROVE SANDBOX',idempotency_key:'DEMO-'+idempotency}));
   demoReceipt=await api('/api/sandbox/receipt/'+encodeURIComponent(t.transaction_id));
   const r=demoReceipt;
   $('#demo-receipt-details').innerHTML=`<div class="demo-summary-row"><span>Receipt number</span><strong>${escapeHTML(r.transaction_id)}</strong></div>
     <div class="demo-summary-row"><span>Status</span><strong>Practice complete</strong></div>
     <div class="demo-summary-row"><span>From / To</span><strong>${escapeHTML(r.origin)} → ${escapeHTML(r.destination)}</strong></div>
     <div class="demo-summary-row"><span>Method</span><strong>${escapeHTML(r.method)}</strong></div>
     <div class="demo-summary-row"><span>Recipient</span><strong>${escapeHTML(r.university)}</strong></div>
     <div class="demo-summary-row"><span>Tuition amount</span><strong>${fmt(r.receiving_amount,r.receiving_currency)}</strong></div>
     <div class="demo-summary-row"><span>Example fee</span><strong>${fmt(r.fee_amount,r.sending_currency)}</strong></div>
     <div class="demo-summary-total"><span>Test amount</span><strong>${fmt(r.sending_amount,r.sending_currency)}</strong></div>`;
   demoStep(4);toast('Test payment saved to MySQL.');
 }catch(e){toast(e.message,true)}finally{demoBusy=false;btn.disabled=false;btn.textContent='Approve test payment →'}
}
function demoDownloadReceipt(){
 if(!demoReceipt)return;
 const r=demoReceipt;const content=[
 'STUDENTBRIDGE AI — PRACTICE RECEIPT','NO REAL MONEY MOVED','',
 'Transaction: '+r.transaction_id,'Date: '+r.date,'Status: '+r.status,
 'From: '+r.origin,'To: '+r.destination,'Recipient: '+r.university,
 'Method: '+r.method,'Tuition: '+r.receiving_amount+' '+r.receiving_currency,
 'Example fee: '+r.fee_amount+' '+r.sending_currency,
 'Practice debit: '+r.sending_amount+' '+r.sending_currency,'',r.warning
 ].join('\n');
 const url=URL.createObjectURL(new Blob([content],{type:'text/plain;charset=utf-8'}));
 const a=document.createElement('a');a.href=url;a.download='StudentBridge_Practice_Receipt_'+r.transaction_id+'.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
function initDemoPayment(){
 countrySelect('#demo-origin','China');countrySelect('#demo-destination','Australia');demoCountryChange();
 const d=new Date();d.setDate(d.getDate()+20);$('#demo-deadline').value=d.toISOString().slice(0,10);
 $('#demo-origin').onchange=demoCountryChange;$('#demo-destination').onchange=demoCountryChange;
 $('#demo-fetch-rate').onclick=demoFetchRate;$('#demo-compare').onclick=demoCompare;
 $('#demo-to-review').onclick=demoToReview;$('#demo-pay-now').onclick=demoExecute;
 $('#demo-save-receipt').onclick=demoDownloadReceipt;
 $('#demo-history').onclick=()=>showView('activity');
 $('#demo-new').onclick=()=>{demoPlan=null;demoSelected=null;demoReceipt=null;$('#demo-consent').checked=false;demoStep(1)};
 $$('[data-demo-back]').forEach(b=>b.onclick=()=>demoStep(Number(b.dataset.demoBack)));
}


/* Topic C — real reference data, clear separation from provider quotes */
function supportedCountries(){return catalog.countries||[]}
function updateRemitCurrencies(){
 const a=$('#remit-from').value,b=$('#remit-to').value;
 $('#remit-currency-from').textContent=countryC(a);
 $('#remit-fee-currency').textContent=countryC(a);
}
async function calculateRemittance(){
 const from=$('#remit-from').value,to=$('#remit-to').value;
 const send=Number($('#remit-amount').value),fee=Number($('#remit-fee').value),mark=Number($('#remit-markup').value);
 const output=$('#remit-result');
 if(from===to){output.textContent='Please choose two different countries.';return}
 if(!Number.isFinite(send)||send<=0||!Number.isFinite(fee)||fee<0||!Number.isFinite(mark)||mark<0||mark>=100){output.textContent='Enter a positive amount and valid fee information.';return}
 output.textContent='Checking the published exchange rate…';
 const base=countryC(from),quote=countryC(to);
 try{
  const r=await api('/api/fx?base='+encodeURIComponent(base)+'&quote='+encodeURIComponent(quote));
  if(!r.available){output.innerHTML='<p class="topic-error">A reference exchange rate is not available right now. We will not guess a rate.</p>';return}
  const rate=Number(r.rate)*(1-mark/100),received=(send-fee)*rate;
  if(send<=fee){output.innerHTML='<p class="topic-error">The fee is greater than or equal to the amount sent.</p>';return}
  output.innerHTML=`<div class="topic-kpi-label">Estimated amount received</div><div class="topic-kpi">${fmt(received,quote)}</div>
   <div class="topic-line"><span>Amount you send</span><strong>${fmt(send,base)}</strong></div>
   <div class="topic-line"><span>Bank fee you entered</span><strong>${fmt(fee,base)}</strong></div>
   <div class="topic-line"><span>Markup you entered</span><strong>${mark.toFixed(2)}%</strong></div>
   <div class="topic-line"><span>Published reference FX</span><strong>1 ${base} = ${fmt(r.rate,quote)}</strong></div>
   <div class="topic-line"><span>Rate observation</span><strong>${escapeHTML(r.date||'Latest published')}</strong></div>
   <p class="topic-disclaimer">Illustrative estimate only. Actual rates, intermediary charges, transfer availability and arrival times are not verified.</p>
   <a href="${escapeHTML(r.source_url)}" target="_blank" rel="noopener noreferrer" class="topic-source">View reference FX source ↗</a>`;
 }catch(e){output.textContent='Could not load exchange-rate data. Please try again later.'}
}
function initRemittance(){
 countrySelect('#remit-from','China');countrySelect('#remit-to','Australia');updateRemitCurrencies();
 $('#remit-from').onchange=updateRemitCurrencies;$('#remit-to').onchange=updateRemitCurrencies;
 $('#remit-calculate').onclick=calculateRemittance;
}
function initCurrencies(){
 $('#currency-balances').innerHTML=supportedCountries().map(c=>`<label><span>${c.flag} ${escapeHTML(c.name)} (${escapeHTML(c.currency)})</span><input type="number" min="0" step="0.01" inputmode="decimal" data-balance="${escapeHTML(c.currency)}" placeholder="Enter amount"></label>`).join('');
 $('#currency-target').innerHTML=supportedCountries().map(c=>`<option value="${escapeHTML(c.currency)}">${c.flag} ${escapeHTML(c.currency)} - ${escapeHTML(c.name)}</option>`).join('');
 $('#currency-target').value='GBP';$('#currency-calculate').onclick=calculateCurrencies;
}
async function calculateCurrencies(){
 const target=$('#currency-target').value,rows=$$('[data-balance]').map(el=>({currency:el.dataset.balance,raw:el.value,amount:Number(el.value)})).filter(r=>r.raw.trim()!=='');
 const output=$('#currency-result');
 if(!rows.length){output.textContent='Enter at least one balance first.';return}
 if(rows.some(r=>!Number.isFinite(r.amount)||r.amount<0)){output.textContent='Balances must be zero or greater.';return}
 output.textContent='Loading current published reference rates…';
 const converted=await Promise.all(rows.map(async r=>{
  if(r.currency===target)return {...r,converted:r.amount,date:'Same currency',rate:1,source:null};
  try{const fx=await api('/api/fx?base='+encodeURIComponent(r.currency)+'&quote='+encodeURIComponent(target));
   return {...r,converted:fx.available?r.amount*Number(fx.rate):null,date:fx.date||'Not available',rate:fx.rate,source:fx.available?fx.source_url:null};
  }catch(e){return {...r,converted:null,date:'Not available',rate:null,source:null}}
 }));
 const available=converted.filter(r=>r.converted!==null),missing=converted.filter(r=>r.converted===null);
 let html='<div class="topic-kpi-label">'+(missing.length?'Subtotal with available rates':'Combined estimated value')+'</div>';
 html+='<div class="topic-kpi">'+fmt(available.reduce((a,b)=>a+b.converted,0),target)+'</div>';
 html+=converted.map(r=>`<div class="topic-line"><span>${escapeHTML(r.currency)} · ${fmt(r.amount)}</span><strong>${r.converted===null?'Rate unavailable':fmt(r.converted,target)}</strong></div>`).join('');
 html+='<p class="topic-disclaimer">'+(missing.length?'Some currencies could not be converted and are excluded from the subtotal. ':'')+'Values use published reference rates, not bank quotes. No bank balances are connected.</p>';
 html+=converted.filter(r=>r.source).map(r=>`<div class="topic-meta">${escapeHTML(r.currency)} → ${escapeHTML(target)}: ${escapeHTML(r.date)} · <a target="_blank" rel="noopener noreferrer" href="${escapeHTML(r.source)}">Source ↗</a></div>`).join('');
 output.innerHTML=html;
}
function initCreditChecklist(){
 const boxes=$$('.credit-check');
 boxes.forEach(b=>b.onchange=()=>{$('#credit-progress').textContent=boxes.filter(el=>el.checked).length+' of '+boxes.length+' steps checked'});
}

async function init(){initVisibleRouteAnimation();catalog=await api('/api/catalog');initRemittance();initCurrencies();initCreditChecklist();initDemoPayment();initSecureCardCheckout();$('#current-date').textContent=new Date().toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'});countrySelect('#origin','China');countrySelect('#destination','Australia');updateCountries();let deadline=new Date();deadline.setDate(deadline.getDate()+45);$('#deadline').value=deadline.toISOString().slice(0,10);paintSources();initCredit();$$('.nav-link').forEach(b=>b.onclick=()=>showView(b.dataset.target));$$('[data-go]').forEach(b=>b.onclick=()=>showView(b.dataset.go));$$('[data-pair]').forEach(b=>b.onclick=()=>pair(...b.dataset.pair.split('|')));$('#origin').onchange=updateCountries;$('#destination').onchange=updateCountries;$('#swap-countries').onclick=()=>{let a=$('#origin').value;$('#origin').value=$('#destination').value;$('#destination').value=a;updateCountries()};$('#university').onchange=handleUni;$('#add-quote').onclick=createQuote;$('#fetch-rate').onclick=fetchReference;$('#build-plan').onclick=buildPlan;$('#open-passport').onclick=passport;$('#sandbox-pay').onclick=approvalModal;$('#close-modal').onclick=closeModal;$('#modal-overlay').onclick=e=>{if(e.target.id==='modal-overlay')closeModal()};$('#run-scenario').onclick=runScenario;$('#refresh-history').onclick=loadActivity;$('#invoice-file').onchange=e=>invoiceUpload(e.target.files?.[0]);['fx-change','extra-fee','living-change'].forEach(id=>{$('#'+id).oninput=()=>{let a=Number($('#fx-change').value),b=Number($('#living-change').value);$('#fx-change-label').textContent=(a>0?'+':'')+a+'%';$('#extra-fee-label').textContent=fmt($('#extra-fee').value,activePlan?.origin_currency||countryC($('#origin').value));$('#living-change-label').textContent=(b>0?'+':'')+b+'%'}});$('#chat-form').onsubmit=e=>{e.preventDefault();let m=$('#chat-input').value.trim();if(!m||chatBusy)return;$('#chat-input').value='';askChat(m)};$('#chat-input').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();$('#chat-form').requestSubmit()}});$('#ask-agent-button').onclick=openBridgeAI;$('#open-assistant').onclick=openBridgeAI;$('#close-assistant').onclick=closeBridgeAI;$$('.prompt-chip').forEach(b=>b.onclick=()=>askChat(b.textContent));}
init().catch(e=>{console.error(e);toast('Backend could not load. Run python run.py and refresh.',true)});


/* Secure card checkout: card and billing address fields always live on
   the payment provider's hosted HTTPS page, never in StudentBridge. */
async function initSecureCardCheckout(){
 const btn=$('#secure-card-button'), status=$('#secure-checkout-status'),payee=$('#secure-checkout-payee');
 if(!btn)return;
 try{
   const d=await api('/api/card/availability');
   if(!d.enabled){status.textContent=d.reason||'Card payments are not available yet.';btn.disabled=true;}
   else{
     status.textContent=d.mode==='TEST'?'Test environment — use payment provider test cards only. No real charge.':'Live card checkout is available for the listed authorized invoice.';
     payee.textContent='Payee: '+d.payee+' · Invoice: '+d.invoice_reference;
     btn.disabled=false;
   }
 }catch(e){status.textContent='Payment availability could not be checked.';btn.disabled=true;}
 btn.onclick=async()=>{
   btn.disabled=true;btn.textContent='Opening secure payment…';
   try{const result=await api('/api/card/checkout',json({}));
       if(!result.checkout_url.startsWith('https://checkout.stripe.com/'))throw new Error('Unexpected payment provider');
       window.location.assign(result.checkout_url);
   }catch(e){toast(e.message,true);btn.disabled=false;btn.textContent='Continue to secure card payment ↗';}
 };
 const url=new URL(window.location.href),sessionId=url.searchParams.get('card_session_id');
 if(sessionId){showView('pay');try{
   const r=await api('/api/card/session/'+encodeURIComponent(sessionId));
   status.textContent=r.status==='paid'?(r.mode==='TEST'?'Test card payment confirmed by provider; no real charge.':'Payment confirmed by provider for '+r.payee+'.'):'Provider reports: '+r.status+'. Payment is not confirmed.';
   payee.textContent='Payment reference: '+r.invoice_reference;
 }catch(e){status.textContent='Payment status cannot yet be verified. Check your provider receipt.';}
 url.searchParams.delete('card_session_id');window.history.replaceState({},'',url.pathname+url.search);
 }else if(url.searchParams.get('card_checkout')==='cancelled'){
   showView('pay');status.textContent='Card checkout was cancelled. No payment was confirmed.';
   url.searchParams.delete('card_checkout');window.history.replaceState({},'',url.pathname+url.search);
 }
}
