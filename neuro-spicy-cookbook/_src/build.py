import json, glob, sys
review = '--public' not in sys.argv
book = json.load(open('recipes.json'))
labels = json.load(open('labels.json'))
videos = {}
videos.update(json.load(open('videos.json')))
for v in videos.values():
    v.setdefault('start', 0); v.setdefault('short', False)
t = open('template.html').read()
j = lambda o: json.dumps(o, ensure_ascii=False).replace('</', '<\\/')
t = (t.replace('/*BOOK*/null', j(book)).replace('/*VIDEOS*/{}', j(videos))
      .replace('/*LABELS*/{}', j(labels)).replace('/*REVIEW*/true', 'true' if review else 'false')
      .replace('<!--ROBOTS-->', '<meta name="robots" content="noindex">' if review else '<link rel="canonical" href="https://webbpageventura.co.uk/neuro-spicy-cookbook/">'))
out = '../index.html'
open(out, 'w').write(t)
missing = sorted({x for r in book['recipes'] for s in r['steps'] for x in s['tech'] if not (videos.get(x) or {}).get('id')})
print(out, '| videos:', len(videos), '| techniques without a video:', len(missing), missing[:10])
