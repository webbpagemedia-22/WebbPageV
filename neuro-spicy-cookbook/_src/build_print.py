import json, sys, html, segno, asyncio, io, os
review = '--public' not in sys.argv
BASE = 'https://webbpageventura.co.uk/neuro-spicy-cookbook/'
book = json.load(open('recipes.json'))
order = ['Basics','Breakfast','Sauces','Rice & Curries','Mince','Weekend']
R = sorted(book['recipes'], key=lambda r: order.index(r['category']))
e = html.escape

def qr(url):
    b = io.BytesIO()
    segno.make(url, error='m').save(b, kind='svg', scale=4, border=0, dark='#1C3F94', xmldecl=False, svgns=True, omitsize=True)
    return b.getvalue().decode()

css = """
@page{size:148mm 210mm;margin:13mm 12mm 14mm 14mm}
@page :first{margin:0}
*{box-sizing:border-box}
body{margin:0;font:400 9.6pt/1.5 Lexend,sans-serif;color:#232836;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{position:relative;page-break-after:always}
.tiles{background-image:url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 56 56'><rect width='56' height='56' fill='%231C3F94'/><g fill='%23F7F7F4'><circle cx='28' cy='28' r='10'/><circle cx='0' cy='0' r='17'/><circle cx='56' cy='0' r='17'/><circle cx='0' cy='56' r='17'/><circle cx='56' cy='56' r='17'/></g><circle cx='28' cy='28' r='4.5' fill='%23E9A21B'/></svg>\");background-size:12mm 12mm;background-repeat:repeat}
.cover{width:148mm;height:210mm;display:flex;flex-direction:column;background:#F7F7F4;overflow:hidden}
.cover .tiles{height:92mm}
.cover .t{padding:12mm 14mm}
.cover h1{font:800 46pt/.9 'Bricolage Grotesque';letter-spacing:-.03em;color:#1C3F94;margin:0 0 6mm}
.cover p{font-size:11pt;color:#5B6170;margin:0;max-width:95mm}
.cover .foot{margin-top:auto;padding:0 14mm 12mm;font-size:8.5pt;color:#5B6170}
h2.toc{font:800 22pt/1 'Bricolage Grotesque';color:#1C3F94;margin:0 0 6mm}
.howto{background:#fff;border-left:3pt solid #E9A21B;padding:3mm 4mm;margin:0 0 7mm;font-size:9pt}
.cat{font:700 10pt/1.2 'Bricolage Grotesque';color:#5E6B2A;margin:3mm 0 .5mm}
.toc ol,.tocl{list-style:none;margin:0;padding:0}
.tocl li{border-top:.5pt solid #DADCE3;padding:.8mm 0;font-size:9pt}
.strip{height:4mm;margin:0 0 5mm}
.rc{font:700 9pt 'Lexend';color:#5E6B2A;margin:0}
h1.rn{font:800 24pt/1 'Bricolage Grotesque';letter-spacing:-.02em;color:#1C3F94;margin:1mm 0 1.5mm}
.aka{font-style:italic;color:#5B6170;margin:0 0 1mm}
.blurb{margin:0 0 2.5mm;font-size:10pt}
.meta{display:flex;gap:6mm;font-size:8.5pt;color:#5B6170;margin-bottom:3mm}
.meta b{color:#232836}
.hero{display:block;width:100%;height:62mm;object-fit:cover;border-radius:2mm;margin:0 0 3mm}
.intro{background:#fff;border-left:3pt solid #5E6B2A;padding:2.5mm 3.5mm;margin:0 0 3mm;font-size:9pt}
h3{font:700 12pt 'Bricolage Grotesque';margin:3mm 0 1.5mm}
.ing{columns:2;column-gap:6mm;margin:0;padding:0;list-style:none;font-size:9pt}
.ing li{break-inside:avoid;padding:.6mm 0 .6mm 3.5mm;position:relative}
.ing li::before{content:"";position:absolute;left:0;top:2.6mm;width:1.4mm;height:1.4mm;border-radius:50%;background:#E9A21B}
.steps{list-style:none;margin:0;padding:0}
.st{display:grid;grid-template-columns:8mm 1fr 13mm;gap:2.5mm;align-items:start;padding:1.4mm 0;border-top:.5pt solid #DADCE3;break-inside:avoid}
.n{width:7.5mm;height:7.5mm;border-radius:50%;border:1.6pt solid #E9A21B;display:grid;place-items:center;font:800 10pt 'Bricolage Grotesque';color:#1C3F94;background:#fff}
.st p{margin:.6mm 0 0}
.q svg{width:13mm;height:13mm;display:block}
.chk{display:block;background:#FCEFD2;border-left:2pt solid #E9A21B;padding:1mm 2mm;margin-top:1mm;font-size:8pt}
.tips{background:#fff;border-left:3pt solid #1C3F94;padding:2.5mm 3.5mm;margin-top:3mm;font-size:9pt;break-inside:avoid}
.tips b{font-family:'Bricolage Grotesque'}
.pn{position:absolute;bottom:7mm;right:13mm;font-size:8pt;color:#5B6170}
"""

pages = []
pages.append(f"""<section class="page cover"><div class="tiles"></div><div class="t">
<h1>The Neuro<br>Spicy<br>Cookbook</h1><p>The family recipes, written the way OG actually cooks them. Every step has a code: scan it with your phone camera and the video for that step plays.</p></div>
<div class="foot">webbpageventura.co.uk/neuro-spicy-cookbook</div></section>""")

toc = []
for c in order:
    rs = [r for r in R if r['category'] == c]
    if rs:
        toc.append(f'<p class="cat">{e(c)}</p><ul class="tocl">' + ''.join(f'<li><span>{e(r["name"])}</span></li>' for r in rs) + '</ul>')
pages.append(f"""<section class="page"><h2 class="toc">What's cooking</h2>
<p class="howto"><b>How the codes work.</b> Point your phone camera at the square next to any step. It opens that step on the The Neuro Spicy Cookbook website and plays a short video showing how it's done.</p>
{''.join(toc)}</section>""")

for r in R:
    ic = r.get('ingredientChecks', {})
    ing = ''.join(f'<li>{e(g)}' + (f'<span class="chk">OG to check: {e(ic[g])}</span>' if review and g in ic else '') + '</li>' for g in r['ingredients'])
    steps = ''
    for k, s in enumerate(r['steps'], 1):
        chk = f'<span class="chk">OG to check: {e(s["check"])}</span>' if review and s.get('check') else ''
        steps += f'<li class="st"><span class="n">{k}</span><p>{e(s["text"])}{chk}</p><span class="q">{qr(f"{BASE}#/{r["id"]}/{k}")}</span></li>'
    meta = ''.join(f'<span>{k} <b>{e(r[f])}</b></span>' for k, f in [('Prep','prep'),('Cook','cook'),('Serves','serves')] if r.get(f))
    tips = f'<div class="tips"><b>OG\'s tips</b><br>' + '<br>'.join(e(t) for t in r['tips']) + '</div>' if r.get('tips') else ''
    equip = f'<p style="font-size:8.5pt;color:#5B6170;margin:1.5mm 0 0">You\'ll need: {e(", ".join(r["equipment"]))}</p>' if r.get('equipment') else ''
    pages.append(f"""<section class="page" style="min-height:auto"><div class="tiles strip"></div>
<p class="rc">{e(r['category'])}</p><h1 class="rn">{e(r['name'])}</h1>{f'<p class="aka">{e(r["aka"])}</p>' if r.get('aka') else ''}
<p class="blurb">{e(r['blurb'])}</p>{f'<img class="hero" src="../{e(r["image"])}" alt="">' if r.get('image') else ''}<div class="meta">{meta}</div>{f'<p class="intro">{e(r["intro"])}</p>' if r.get('intro') else ''}
<h3>Ingredients</h3><ul class="ing">{ing}</ul>{equip}
<h3>Method</h3><ol class="steps">{steps}</ol>{tips}</section>""")

doc = f"""<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;700&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&display=swap" rel="stylesheet">
<style>{css}</style></head><body>{''.join(pages)}</body></html>"""
open('print.html', 'w').write(doc)

async def pdf():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto('file://'+os.path.abspath('print.html')); await pg.wait_for_timeout(2500)
        out = '../the-neuro-spicy-cookbook' + ('-draft' if review else '') + '.pdf'
        await pg.pdf(path=out, width='148mm', height='210mm', print_background=True, prefer_css_page_size=True)
        await b.close(); print(out)
asyncio.run(pdf())
