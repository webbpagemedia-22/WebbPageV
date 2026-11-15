"""Build the Amazon KDP files for The Neuro Spicy Cookbook.

Usage (from this folder):  python3 build_kdp.py /path/to/output-folder
Writes: kdp-paperback-interior.pdf, kdp-paperback-cover.pdf, kdp-ebook.epub, kdp-ebook-cover.jpg
Keep the output folder OUTSIDE the website repo: these files are for uploading to KDP, not for the site.

Paperback spec: 5.5 x 8.5 in (139.7 x 215.9 mm), no bleed inside, premium colour, white paper.
Cover: full wrap with 3.2 mm bleed; spine = page count x 0.0596 mm (premium colour).
"""
import json, sys, html, segno, asyncio, io, os, re, zipfile, uuid, datetime

OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else sys.exit('Give an output folder outside the repo.')
os.makedirs(OUT, exist_ok=True)
BASE = 'https://webbpageventura.co.uk/neuro-spicy-cookbook/'
SITE = 'webbpageventura.co.uk/neuro-spicy-cookbook'
AUTHOR = 'David Page'
YEAR = '2026'
book = json.load(open('recipes.json'))
videos = json.load(open('videos.json'))
labels = json.load(open('labels.json'))
TITLE = book['title']
order = ['Basics', 'Breakfast', 'Sauces', 'Rice & Curries', 'Mince', 'Weekend']
R = sorted(book['recipes'], key=lambda r: order.index(r['category']))
_W = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split()
NUM_WORD = (_W[len(R)] if len(R) < len(_W) else str(len(R))).capitalize()
e = html.escape
IMG = os.path.abspath('..')
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;700&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&display=swap" rel="stylesheet">'
TILE = "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 56 56'><rect width='56' height='56' fill='%231C3F94'/><g fill='%23F7F7F4'><circle cx='28' cy='28' r='10'/><circle cx='0' cy='0' r='17'/><circle cx='56' cy='0' r='17'/><circle cx='0' cy='56' r='17'/><circle cx='56' cy='56' r='17'/></g><circle cx='28' cy='28' r='4.5' fill='%23E9A21B'/></svg>\")"


def qr(url):
    b = io.BytesIO()
    segno.make(url, error='m').save(b, kind='svg', scale=4, border=0, dark='#1C3F94', xmldecl=False, svgns=True, omitsize=True)
    return b.getvalue().decode()


# ---------- paperback interior ----------
CSS = """
*{box-sizing:border-box}
body{margin:0;font:400 9.6pt/1.5 Lexend,sans-serif;color:#232836;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{position:relative;page-break-after:always}
.tiles{background-image:""" + TILE + """;background-size:12mm 12mm;background-repeat:repeat}
.tp{height:172mm;display:flex;flex-direction:column;justify-content:center}
.tp h1{font:800 44pt/.92 'Bricolage Grotesque';letter-spacing:-.03em;color:#1C3F94;margin:0 0 8mm}
.tp .sub{font-size:11.5pt;color:#5B6170;max-width:90mm;margin:0 0 14mm}
.tp .by{font:700 15pt 'Bricolage Grotesque';color:#5E6B2A;margin:0}
.cr{height:172mm;display:flex;flex-direction:column;justify-content:flex-end;font-size:8.5pt;color:#5B6170;max-width:95mm}
.cr p{margin:0 0 2.5mm}
h2.toc{font:800 22pt/1 'Bricolage Grotesque';color:#1C3F94;margin:0 0 6mm}
.fw{font-size:11.5pt;line-height:1.65;max-width:100mm;margin-top:8mm}
.fw p{margin:0 0 5mm}
.fwsign{font:800 15pt 'Bricolage Grotesque';color:#5E6B2A}
.howto{background:#F7F7F4;border-left:3pt solid #E9A21B;padding:3mm 4mm;margin:0 0 6mm;font-size:9pt}
.cat{font:700 10pt/1.2 'Bricolage Grotesque';color:#5E6B2A;margin:2.6mm 0 .5mm}
.tocl{list-style:none;margin:0;padding:0}
.tocl li{border-top:.5pt solid #DADCE3;padding:.7mm 0;font-size:9pt;display:flex;justify-content:space-between}
.strip{height:4mm;margin:0 0 5mm}
.rc{font:700 9pt 'Lexend';color:#5E6B2A;margin:0}
h1.rn{font:800 24pt/1 'Bricolage Grotesque';letter-spacing:-.02em;color:#1C3F94;margin:1mm 0 1.5mm}
.aka{font-style:italic;color:#5B6170;margin:0 0 1mm}
.blurb{margin:0 0 2.5mm;font-size:10pt}
.meta{display:flex;gap:6mm;font-size:8.5pt;color:#5B6170;margin-bottom:3mm}
.meta b{color:#232836}
.hero{display:block;width:100mm;height:66mm;object-fit:cover;border-radius:2mm;margin:0 0 3mm}
.intro{background:#F7F7F4;border-left:3pt solid #5E6B2A;padding:2.5mm 3.5mm;margin:0 0 3mm;font-size:9pt}
h3{font:700 12pt 'Bricolage Grotesque';margin:3mm 0 1.5mm}
.ing{columns:2;column-gap:6mm;margin:0;padding:0;list-style:none;font-size:9pt}
.ing li{break-inside:avoid;padding:.6mm 0 .6mm 3.5mm;position:relative}
.ing li::before{content:"";position:absolute;left:0;top:2.6mm;width:1.4mm;height:1.4mm;border-radius:50%;background:#E9A21B}
.steps{list-style:none;margin:0;padding:0}
.st{display:grid;grid-template-columns:8mm 1fr 13mm;gap:2.5mm;align-items:start;padding:1.4mm 0;border-top:.5pt solid #DADCE3;break-inside:avoid}
.n{width:7.5mm;height:7.5mm;border-radius:50%;border:1.6pt solid #E9A21B;display:grid;place-items:center;font:800 10pt 'Bricolage Grotesque';color:#1C3F94;background:#fff}
.st p{margin:.6mm 0 0}
.q svg{width:13mm;height:13mm;display:block}
.tips{background:#F7F7F4;border-left:3pt solid #1C3F94;padding:2.5mm 3.5mm;margin-top:3mm;font-size:9pt;break-inside:avoid}
.tips b{font-family:'Bricolage Grotesque'}
"""


def interior_html(pagenos=None):
    pagenos = pagenos or {}
    pages = []
    pages.append(f"""<section class="page"><div class="tp"><h1>The Neuro<br>Spicy<br>Cookbook</h1>
<p class="sub">Family recipes, written the way they're actually cooked at home, with a video for every step.</p><p class="by">{e(AUTHOR)}</p></div></section>""")
    pages.append(f"""<section class="page"><div class="cr"><p><b>{e(TITLE)}</b></p><p>Copyright © {YEAR} {e(AUTHOR)}. All rights reserved.</p>
<p>The videos linked from this book belong to their creators and play from YouTube. The links are kept up to date at {SITE}</p><p>First edition, {YEAR}.</p></div></section>""")
    fw = book.get('foreword')
    if fw:
        pages.append(f"""<section class="page"><h2 class="toc">{e(fw['title'])}</h2><div class="fw">{''.join(f'<p>{e(x)}</p>' for x in fw['paragraphs'])}<p class="fwsign">{e(fw['sign'])}</p></div></section>""")
    toc = ''
    for c in order:
        rs = [r for r in R if r['category'] == c]
        if rs:
            toc += f'<p class="cat">{e(c)}</p><ul class="tocl">' + ''.join(f'<li><span>{e(r["name"])}</span><span>{pagenos.get(r["id"], "")}</span></li>' for r in rs) + '</ul>'
    pages.append(f"""<section class="page"><h2 class="toc">What's cooking</h2>
<p class="howto"><b>How the codes work.</b> Point your phone camera at the square next to any step. It opens that step on The Neuro Spicy Cookbook website and plays a short video showing how it's done.</p>{toc}</section>""")
    for r in R:
        ing = ''.join(f'<li>{e(g)}</li>' for g in r['ingredients'])
        steps = ''
        for k, s in enumerate(r['steps'], 1):
            seename = next((x['name'] for x in R if x['id'] == s.get('see')), None)
            see = f' <b>See {e(seename)} in this book; the code opens it.</b>' if seename else ''
            target = f"{BASE}#/{s['see']}" if seename else f"{BASE}#/{r['id']}/{k}"
            steps += f'<li class="st"><span class="n">{k}</span><p>{e(s["text"])}{see}</p><span class="q">{qr(target)}</span></li>'
        meta = ''.join(f'<span>{k} <b>{e(r[f])}</b></span>' for k, f in [('Prep', 'prep'), ('Cook', 'cook'), ('Serves', 'serves')] if r.get(f))
        tips = '<div class="tips"><b>OG\'s tips</b><br>' + '<br>'.join(e(t) for t in r['tips']) + '</div>' if r.get('tips') else ''
        equip = f'<p style="font-size:8.5pt;color:#5B6170;margin:1.5mm 0 0">You\'ll need: {e(", ".join(r["equipment"]))}</p>' if r.get('equipment') else ''
        img = f'<img class="hero" src="file://{IMG}/{e(r["image"])}" alt="">' if r.get('image') else ''
        pages.append(f"""<section class="page"><div class="tiles strip"></div><p class="rc">{e(r['category'])}</p><h1 class="rn">{e(r['name'])}</h1>{f'<p class="aka">{e(r["aka"])}</p>' if r.get('aka') else ''}
<p class="blurb">{e(r['blurb'])}</p>{img}<div class="meta">{meta}</div>{f'<p class="intro">{e(r["intro"])}</p>' if r.get('intro') else ''}
<h3>Ingredients</h3><ul class="ing">{ing}</ul>{equip}<h3>Method</h3><ol class="steps">{steps}</ol>{tips}</section>""")
    return f'<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body>{"".join(pages)}</body></html>'


# Page numbers must stay at least 0.25 in (6.4 mm) from the trim edge or KDP rejects the file; this keeps them about 0.45 in up.
FOOT = '<div style="width:100%;text-align:center;font-size:8px;color:#5B6170;font-family:Arial,sans-serif;margin-bottom:6.5mm"><span class="pageNumber"></span></div>'


async def render_interior(pg, path, pagenos=None):
    open(os.path.join(OUT, '_interior.html'), 'w').write(interior_html(pagenos))
    await pg.goto('file://' + os.path.join(OUT, '_interior.html')); await pg.wait_for_timeout(2500)
    await pg.pdf(path=path, width='139.7mm', height='215.9mm', print_background=True, display_header_footer=True,
                 header_template='<span></span>', footer_template=FOOT,
                 margin={'top': '13mm', 'bottom': '19mm', 'left': '14mm', 'right': '14mm'})


def start_pages(path):
    import pypdfium2 as pdfium
    d = pdfium.PdfDocument(path); found = {}
    for i in range(len(d)):
        head = ' '.join(d[i].get_textpage().get_text_range().split())[:160]
        for r in R:
            if r['id'] not in found and head.startswith(r['category'] + ' ' + r['name']):
                found[r['id']] = i + 1
    return found, len(d)


# ---------- paperback cover ----------
def cover_html(pages):
    spine = pages * 0.0596
    B, W, H = 3.2, 139.7, 215.9
    full_w, full_h = B + W + spine + W + B, B + H + B
    fx = B + W + spine  # left edge of the front panel
    band = B + 70
    photos = [r['image'] for r in R if r['id'] in ('roast-chicken', 'nasi-goreng', 'lasagne')]
    ph = ''.join(f'<img src="file://{IMG}/{p}" style="width:33mm;height:33mm;object-fit:cover;border-radius:2mm">' for p in photos)
    names = ', '.join(r['name'] for r in R[:-1]) + ' and ' + R[-1]['name']
    doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8">{FONTS}<style>
@page{{size:{full_w:.2f}mm {full_h:.2f}mm;margin:0}}
*{{box-sizing:border-box}}body{{margin:0;-webkit-print-color-adjust:exact;print-color-adjust:exact;font-family:Lexend,sans-serif;color:#232836}}
.wrap{{position:relative;width:{full_w:.2f}mm;height:{full_h:.2f}mm;background:#F7F7F4;overflow:hidden}}
.band{{position:absolute;left:0;top:0;width:100%;height:{band}mm;background-image:{TILE};background-size:12mm 12mm}}
.front{{position:absolute;left:{fx + 14:.2f}mm;top:{band + 12}mm;width:{W - 28:.1f}mm}}
.front h1{{font:800 44pt/.9 'Bricolage Grotesque';letter-spacing:-.03em;color:#1C3F94;margin:0 0 6mm}}
.front p{{font-size:11.5pt;line-height:1.45;color:#5B6170;margin:0;max-width:100mm}}
.by{{position:absolute;left:{fx + 14:.2f}mm;top:{B + H - 24}mm;font:700 16pt 'Bricolage Grotesque';color:#5E6B2A}}
.back{{position:absolute;left:{B + 14}mm;top:{band + 9}mm;width:{W - 28:.1f}mm}}
.back h2{{font:800 17pt/1.1 'Bricolage Grotesque';color:#1C3F94;margin:0 0 3mm}}
.back p{{font-size:9.4pt;line-height:1.5;margin:0 0 2.6mm}}
.ph{{display:flex;gap:4.5mm;margin-top:3mm}}
.url{{position:absolute;left:{B + 14}mm;top:{B + H - 21}mm;font-size:8.5pt;color:#5B6170;line-height:1.4;max-width:60mm}}
/* KDP prints the barcode bottom-right of the back cover: 50.8 x 30.5 mm, 6.35 mm in from the spine fold and the bottom trim. Keep a plain white box there (3 mm bigger all round) with nothing on it. */
.barcode{{position:absolute;left:{B + W - 6.35 - 50.8 - 3:.2f}mm;top:{B + H - 6.35 - 30.5 - 3:.2f}mm;width:56.8mm;height:36.5mm;background:#fff}}
</style></head><body><div class="wrap"><div class="band"></div>
<div class="back"><h2>A recipe book for anyone who was never shown how.</h2>
<p>{NUM_WORD} family recipes, written the way they're actually cooked at home. Every step has a code. Scan it with your phone and a short video shows you exactly how that step is done.</p>
<p>Inside: {e(names)}.</p><div class="ph">{ph}</div></div>
<div class="url">{SITE.replace("/", "/<br>", 1)}</div><div class="barcode"></div>
<div class="front"><h1>The Neuro<br>Spicy<br>Cookbook</h1><p>Family recipes with a video for every step.</p></div>
<div class="by">{e(AUTHOR)}</div></div></body></html>"""
    return doc, full_w, full_h, spine


def ebook_cover_html():
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{FONTS}<style>
*{{box-sizing:border-box}}body{{margin:0;width:1600px;height:2560px;background:#F7F7F4;font-family:Lexend,sans-serif;position:relative;overflow:hidden}}
.band{{height:1120px;background-image:{TILE};background-size:160px 160px}}
h1{{font:800 236px/.9 'Bricolage Grotesque';letter-spacing:-.03em;color:#1C3F94;margin:130px 0 70px 130px}}
p{{font-size:62px;line-height:1.4;color:#5B6170;margin:0 130px;max-width:1200px}}
.by{{position:absolute;left:130px;bottom:150px;font:700 84px 'Bricolage Grotesque';color:#5E6B2A}}
</style></head><body><div class="band"></div><h1>The Neuro<br>Spicy<br>Cookbook</h1><p>Family recipes with a video for every step.</p><div class="by">{e(AUTHOR)}</div></body></html>"""


# ---------- Kindle eBook (EPUB 3) ----------
def x(body, title):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en-GB" xml:lang="en-GB"><head><meta charset="utf-8"/><title>{e(title)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head><body>{body}</body></html>"""


def build_epub(path, cover_jpg):
    uid = str(uuid.uuid5(uuid.NAMESPACE_URL, BASE))
    files, spine, manifest = {}, [], []
    def add(name, body, title, nav=False):
        files[name] = x(body, title)
        manifest.append(f'<item id="{name[:-6]}" href="{name}" media-type="application/xhtml+xml"{" properties=\"nav\"" if nav else ""}/>')
        spine.append(f'<itemref idref="{name[:-6]}"/>')
    add('title.xhtml', f'<section epub:type="titlepage"><h1 class="bt">{e(TITLE)}</h1><p class="sub">Family recipes, written the way they\'re actually cooked at home, with a video for every step.</p><p class="by">{e(AUTHOR)}</p><p class="small">Copyright © {YEAR} {e(AUTHOR)}. All rights reserved. The videos linked from this book belong to their creators and play from YouTube.</p></section>', TITLE)
    fw = book.get('foreword')
    if fw:
        add('foreword.xhtml', f'<section epub:type="foreword"><h1>{e(fw["title"])}</h1>{"".join(f"<p>{e(p)}</p>" for p in fw["paragraphs"])}<p class="by">{e(fw["sign"])}</p></section>', fw['title'])
    navli = '<li><a href="title.xhtml">Title page</a></li>' + ('<li><a href="foreword.xhtml">Foreword</a></li>' if fw else '')
    for c in order:
        rs = [r for r in R if r['category'] == c]
        if rs:
            navli += f'<li><span>{e(c)}</span><ol>' + ''.join(f'<li><a href="r-{r["id"]}.xhtml">{e(r["name"])}</a></li>' for r in rs) + '</ol></li>'
    add('nav.xhtml', f'<p>Tap “Watch” under any step to open a short video showing how it\'s done.</p><nav epub:type="toc" id="toc"><h1>What\'s cooking</h1><ol>{navli}</ol></nav>', 'Contents', nav=True)
    imgs = []
    for r in R:
        steps = ''
        for k, s in enumerate(r['steps'], 1):
            extra = ''
            if s.get('see'):
                nm = next(z['name'] for z in R if z['id'] == s['see'])
                extra = f'<br/><a href="r-{s["see"]}.xhtml">Open the {e(nm)} recipe</a>'
            else:
                t = next((t for t in s['tech'] if (videos.get(t) or {}).get('id')), None)
                if t:
                    extra = f'<br/><a class="w" href="{BASE}#/{r["id"]}/{k}">Watch: {e(labels.get(t, t))}</a>'
            steps += f'<li>{e(s["text"])}{extra}</li>'
        img = ''
        if r.get('image'):
            fn = os.path.basename(r['image']); imgs.append(fn)
            img = f'<div class="hero"><img src="images/{fn}" alt="{e(r.get("imageAlt", r["name"]))}"/></div>'
        meta = ' | '.join(f'{k}: {e(r[f])}' for k, f in [('Prep', 'prep'), ('Cook', 'cook'), ('Serves', 'serves')] if r.get(f))
        body = (f'<section><p class="cat">{e(r["category"])}</p><h1>{e(r["name"])}</h1>' + (f'<p class="aka">{e(r["aka"])}</p>' if r.get('aka') else '')
                + f'<p>{e(r["blurb"])}</p>{img}<p class="meta">{meta}</p>' + (f'<p class="intro">{e(r["intro"])}</p>' if r.get('intro') else '')
                + '<h2>Ingredients</h2><ul>' + ''.join(f'<li>{e(g)}</li>' for g in r['ingredients']) + '</ul>'
                + (f'<p class="meta">You\'ll need: {e(", ".join(r["equipment"]))}</p>' if r.get('equipment') else '')
                + f'<h2>Method</h2><ol>{steps}</ol>'
                + ('<h2>OG\'s tips</h2><ul>' + ''.join(f'<li>{e(t)}</li>' for t in r['tips']) + '</ul>' if r.get('tips') else '') + '</section>')
        add(f'r-{r["id"]}.xhtml', body, r['name'])
    css = """body{font-family:sans-serif;line-height:1.5}h1{color:#1C3F94;line-height:1.1;margin:.2em 0 .4em}h1.bt{font-size:2.6em;margin-top:1.5em}
h2{font-size:1.15em;margin:1.2em 0 .4em}.cat{color:#5E6B2A;font-weight:bold;margin:0}.aka{font-style:italic}.meta,.small{font-size:.9em;color:#555}
.sub{font-size:1.1em}.by{font-weight:bold;color:#5E6B2A;font-size:1.2em}.intro{border-left:.3em solid #5E6B2A;padding-left:.8em}
.hero{text-align:center;margin:.8em 0}.hero img{max-width:100%}ol li,ul li{margin-bottom:.6em}a.w{font-size:.95em}nav ol{list-style:none;padding-left:0}nav ol ol{padding-left:1.2em}nav span{font-weight:bold}"""
    man = '\n'.join(manifest) + '\n<item id="css" href="style.css" media-type="text/css"/>\n<item id="cover" href="cover.jpg" media-type="image/jpeg" properties="cover-image"/>\n' + '\n'.join(f'<item id="img{i}" href="images/{fn}" media-type="image/jpeg"/>' for i, fn in enumerate(imgs))
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="en-GB"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="uid">urn:uuid:{uid}</dc:identifier><dc:title>{e(TITLE)}</dc:title><dc:creator>{e(AUTHOR)}</dc:creator><dc:language>en-GB</dc:language>
<meta property="dcterms:modified">{now}</meta><meta name="cover" content="cover"/></metadata>
<manifest>{man}</manifest><spine>{''.join(spine)}</spine></package>"""
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr(zipfile.ZipInfo('mimetype'), 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml', '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>', zipfile.ZIP_DEFLATED)
        z.writestr('OEBPS/content.opf', opf, zipfile.ZIP_DEFLATED); z.writestr('OEBPS/style.css', css, zipfile.ZIP_DEFLATED)
        for n, c in files.items(): z.writestr('OEBPS/' + n, c, zipfile.ZIP_DEFLATED)
        z.write(cover_jpg, 'OEBPS/cover.jpg', zipfile.ZIP_DEFLATED)
        for fn in imgs: z.write(os.path.join(IMG, 'images', fn), 'OEBPS/images/' + fn, zipfile.ZIP_DEFLATED)


async def main():
    from playwright.async_api import async_playwright
    from PIL import Image
    interior = os.path.join(OUT, 'kdp-paperback-interior.pdf')
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await render_interior(pg, interior)
        nums, n1 = start_pages(interior)
        assert len(nums) == len(R), ('could not find every recipe start page', nums)
        await render_interior(pg, interior, nums)
        nums2, n2 = start_pages(interior)
        assert nums2 == nums and n1 == n2, 'page numbers moved between passes'
        pages = n2 + (n2 % 2)
        doc, w, h, spine = cover_html(pages)
        open(os.path.join(OUT, '_cover.html'), 'w').write(doc)
        await pg.goto('file://' + os.path.join(OUT, '_cover.html')); await pg.wait_for_timeout(2500)
        await pg.pdf(path=os.path.join(OUT, 'kdp-paperback-cover.pdf'), width=f'{w:.2f}mm', height=f'{h:.2f}mm', print_background=True, prefer_css_page_size=True)
        pg2 = await b.new_page(viewport={'width': 1600, 'height': 2560})
        open(os.path.join(OUT, '_ecover.html'), 'w').write(ebook_cover_html())
        await pg2.goto('file://' + os.path.join(OUT, '_ecover.html')); await pg2.wait_for_timeout(2500)
        await pg2.screenshot(path=os.path.join(OUT, '_ecover.png'))
        await b.close()
    # Chromium rounds page sizes up to whole points; set the exact trim and cover sizes KDP expects.
    from pypdf import PdfReader, PdfWriter
    for f, (pw, ph) in {interior: (5.5 * 72, 8.5 * 72), os.path.join(OUT, 'kdp-paperback-cover.pdf'): (w / 25.4 * 72, h / 25.4 * 72)}.items():
        rd = PdfReader(f); wr = PdfWriter()
        for page in rd.pages:
            top = float(page.mediabox.top)
            for box in (page.mediabox, page.cropbox, page.trimbox, page.bleedbox, page.artbox):
                box.lower_left = (0, top - ph); box.upper_right = (pw, top)
            wr.add_page(page)
        wr.write(f)
    cj = os.path.join(OUT, 'kdp-ebook-cover.jpg')
    Image.open(os.path.join(OUT, '_ecover.png')).convert('RGB').save(cj, quality=92)
    build_epub(os.path.join(OUT, 'kdp-ebook.epub'), cj)
    for f in ('_interior.html', '_cover.html', '_ecover.html', '_ecover.png'): os.remove(os.path.join(OUT, f))
    print(f'interior: {n2} pages (KDP counts {pages}) | cover: {w:.2f} x {h:.2f} mm, spine {spine:.2f} mm')

asyncio.run(main())
