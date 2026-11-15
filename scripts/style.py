#!/usr/bin/env python3
"""Заготовка brand.json из готового стиля библиотеки.

    python3 scripts/style.py list                      # все 24 стиля
    python3 scripts/style.py 7 > projects/<id>/brand.json
    python3 scripts/style.py 7 --name "Anna Smirnova" --handle @anna --tagline "english · speaking"
Дальше агент правит поля под бренд: идея, знак, голос, посты. Цвета и шрифты можно смешивать из разных стилей.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(os.path.join(ROOT, 'patterns/styles.json'), encoding='utf-8'))
a = sys.argv[1:]
if not a: sys.exit(__doc__)
if a[0] == 'list':
    for s in S: print(f"{s['n']:>2}  {s['group']}  {s['name']:<26} {s['mood']}")
    sys.exit()
s = next(x for x in S if x['n'] == int(a[0]))
opt = lambda k, d: a[a.index(k) + 1] if k in a else d
tpl = json.load(open(os.path.join(ROOT, 'projects/_template/brand.json'), encoding='utf-8'))
tpl.update({'name': opt('--name', tpl['name']), 'handle': opt('--handle', tpl['handle']), 'tagline': opt('--tagline', tpl['tagline']),
            'style': f"{s['n']} · {s['name']}", 'colors': s['colors'], 'fonts': s['fonts'], 'radius': s['radius'], 'elements': s['elements'],
            'signature': [[x, ''] for x in s['signature']]})
print(json.dumps(tpl, ensure_ascii=False, indent=2))
