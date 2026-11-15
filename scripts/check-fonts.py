#!/usr/bin/env python3
"""Есть ли в шрифте казахские буквы (ә ғ қ ң ө ұ ү һ і), кириллица и латиница. Проверка по настоящему файлу шрифта с Google Fonts.

    python3 scripts/check-fonts.py "Unbounded" "Montserrat" "Inter Tight"
    python3 scripts/check-fonts.py projects/<id>/brand.json    # все шрифты бренда
Нужен пакет fontTools: pip3 install fonttools
"""
import io, json, re, sys, urllib.request
from fontTools.ttLib import TTFont
KK, RU, EN = 'ӘәҒғҚқҢңӨөҰұҮүҺһІі', 'АаБбЖжЩщЫыЭэЮюЯяЁё', 'AaBbQqWwZz'

def check(fam):
    css = urllib.request.urlopen(urllib.request.Request(
        'https://fonts.googleapis.com/css2?family=' + fam.replace(' ', '+'), headers={'User-Agent': 'Mozilla/4.0'})).read().decode()
    urls = re.findall(r'url\((https://[^)]+)\)', css)
    if not urls: return f'{fam}: нет на Google Fonts'
    cmap = set()
    for u in urls: cmap |= set(TTFont(io.BytesIO(urllib.request.urlopen(u).read())).getBestCmap())
    miss = lambda s: ''.join(c for c in s if ord(c) not in cmap)
    kk, ru = miss(KK), miss(RU)
    return f"{fam}: казахский {'✓' if not kk else '✕ нет ' + kk}, русский {'✓' if not ru else '✕'}, английский {'✓' if not miss(EN) else '✕'}"

args = sys.argv[1:]
if not args: sys.exit(__doc__)
if args[0].endswith('.json'):
    f = json.load(open(args[0], encoding='utf-8'))['fonts']
    args = sorted({x['family'] for x in f.values()} | {x.get('kk') for x in f.values() if x.get('kk')})
for a in args: print(check(a))
