from pathlib import Path
from html import escape
import mistune
from weasyprint import HTML

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
md=mistune.create_markdown(plugins=['table','strikethrough'])
STYLE='''
@page {size:A4; margin:21mm 17mm 19mm 17mm; @bottom-center { content: "STUDENTBRIDGE AI  |  " counter(page); color:#777; font-size:8pt; }}
*{box-sizing:border-box} body{font-family:Arial,DejaVu Sans,sans-serif;color:#111;font-size:9.5pt;line-height:1.48}
h1,h2,h3,h4{font-family:Arial,sans-serif;page-break-after:avoid;color:#111}
h1{font-size:23pt;letter-spacing:-.65px;line-height:1.15;margin:0 0 18pt}
h2{font-size:14pt;border-bottom:1px solid #888;margin-top:26pt;margin-bottom:9pt;padding-bottom:6pt}
h3{font-size:11pt;margin-top:17pt;margin-bottom:7pt}p{margin:7pt 0 11pt}
li{margin:4pt 0}ul,ol{padding-left:20pt}blockquote{border-left:2px solid #777;padding:8pt 12pt;margin-left:0;color:#444}
pre{background:#f5f5f5;border:1px solid #ddd;padding:10pt;white-space:pre-wrap;overflow-wrap:anywhere;font:7.5pt/1.4 'DejaVu Sans Mono',monospace}
code{font:8.5pt 'DejaVu Sans Mono',monospace;overflow-wrap:anywhere}table{border-collapse:collapse;width:100%;margin:10pt 0 14pt;table-layout:fixed;page-break-inside:auto;font-size:7.6pt}tr{page-break-inside:avoid;page-break-after:auto}td,th{border:1px solid #bbb;padding:6pt;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{background:#e9e9e9}a{text-decoration:underline;color:#222;overflow-wrap:anywhere}
.cover{min-height:185mm;display:flex;flex-direction:column;justify-content:center;break-after:page}.cover-label{font-size:9pt;letter-spacing:3px;text-transform:uppercase;border-top:2pt solid #111;width:max-content;padding-top:10pt}.cover h1{font-size:34pt;margin:23pt 0 13pt}.cover h2{font-size:17pt;border:0;margin:0 0 15pt;padding:0;font-weight:normal}.cover p{font-size:11pt;color:#444}.rule{border-top:1pt solid #aaa;width:55%;margin:25pt 0}.meta{font-size:9pt;color:#555;line-height:1.9}.label{font-size:8pt;letter-spacing:1.3px;text-transform:uppercase;color:#666}
''' 
def render(title:str, subtitle:str, sources:list[str], target:str, desc:str):
    content=''.join('<article>'+md((ROOT/x).read_text(encoding='utf-8'))+'</article>' for x in sources)
    cover=f'''<div class="cover"><div class="cover-label">2026 International FinTech Competition / Topic C</div><h1>{escape(title)}</h1><h2>{escape(subtitle)}</h2><div class="rule"></div><p>{escape(desc)}</p><div class="meta">StudentBridge AI · China · United Kingdom · Japan · South Korea · Australia · Bangladesh<br>Prepared 15 October 2026 · Demonstration system · Real references with conditional user-input quotes</div></div>'''
    html='<html><head><meta charset="utf-8"><style>'+STYLE+'</style></head><body>'+cover+content+'</body></html>'
    HTML(string=html,base_url=str(ROOT)).write_pdf(DOCS/target)
    print(target,(DOCS/target).stat().st_size)

render('StudentBridge AI','Full project guide and implementation manual',
       ['README.md','docs/MYSQL_SETUP.md','docs/DATA_COLLECTION_GUIDE.md','docs/COMPETITION_ALIGNMENT.md','docs/NEXT_STEPS_BEFORE_SUBMISSION.md'],
       'FULL_PROJECT_GUIDE.pdf','A complete six-country student-finance project, including verified sources, collection strategy, technical features, launch steps, competition requirements and final team tasks.')
render('Technical Documentation','Architecture, core algorithms, data provenance and evaluation',
       ['docs/SYSTEM_DESIGN.md','docs/DATA_COLLECTION_GUIDE.md','docs/COMPETITION_ALIGNMENT.md'],
       'TECHNICAL_DOCUMENTATION.pdf','Technical explanation of EduRoute decision logic, the Digital Twin, Decision Passport, grounded AI, reference FX API, 30 directional country combinations, and sandbox transaction controls.')
render('Security Self-Assessment','Permission levels, implemented controls and known risks',
       ['docs/SECURITY_SELF_ASSESSMENT.md'],
       'SECURITY_SELF_ASSESSMENT.pdf','Transparent statement of the limits of the current financial MVP: no real-money movement, unverified user-entered quotes, no authentication, and no automatic regulatory certification.')
