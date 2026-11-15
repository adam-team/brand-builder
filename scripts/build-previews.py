#!/usr/bin/env python3
"""Пересобрать картинки выбора стиля reference/style-previews/styles-A.jpg … styles-E.jpg из patterns/styles.json.
    python3 scripts/build-previews.py      (нужны Google Chrome и Pillow)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import serve, chrome, ROOT
from PIL import Image
port = serve()
for g in 'ABCDE':
    png = os.path.join(ROOT, f'reference/style-previews/styles-{g}.png')
    chrome(f'http://127.0.0.1:{port}/kit/styles.html?g={g}', ['--window-size=1880,1950', f'--screenshot={png}'], budget=12000)
    im = Image.open(png).convert('RGB'); bg = im.getpixel((5, im.height - 5))
    # обрезать пустой низ
    y = im.height - 1
    while y > 200 and all(im.getpixel((x, y)) == bg for x in range(0, im.width, 40)): y -= 1
    im.crop((0, 0, im.width, min(im.height, y + 40))).save(png[:-4] + '.jpg', quality=85); os.remove(png)
    print('styles-' + g + '.jpg')
