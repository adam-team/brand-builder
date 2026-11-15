#!/usr/bin/env python3
"""Собрать весь брендбук бренда в PNG, SVG и PDF.

    python3 scripts/render.py examples/kuralay          # пример Куралай
    python3 scripts/render.py projects/<id>             # бренд ученика
    python3 scripts/render.py projects/<id> --only posts # только карусели (logo, posts, reels, stickers, print, book)

Нужны Google Chrome и Node.js. Шрифты грузятся из Google Fonts, поэтому нужен интернет.
Результат: <папка>/dist/{logo,posts,reels,highlights,stickers,print}/ и <папка>/dist/Брендбук.pdf
"""
import http.server, json, os, shutil, socketserver, subprocess, sys, tempfile, threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = next((p for p in [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    shutil.which('google-chrome') or '', shutil.which('chromium') or '', shutil.which('chrome') or '',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe'] if p and os.path.exists(p)), None)


def serve():
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    os.chdir(ROOT)
    srv = socketserver.TCPServer(('127.0.0.1', 0), Q)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv.server_address[1]


def chrome(url, args, budget=9000):
    ud = tempfile.mkdtemp()
    cmd = [CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--user-data-dir={ud}',
           '--force-device-scale-factor=1', f'--virtual-time-budget={budget}', *args, url]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    finally:
        shutil.rmtree(ud, ignore_errors=True)


def shot(port, page, q, out, w, h, bg=True):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    args = [f'--window-size={w},{h}', f'--screenshot={out}']
    if not bg: args.append('--default-background-color=00000000')
    chrome(f'http://127.0.0.1:{port}/kit/{page}?{q}', args)
    print('  ', os.path.relpath(out, ROOT) if os.path.exists(out) else f'НЕ ПОЛУЧИЛОСЬ: {out}')


def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    brand = sys.argv[1].rstrip('/')
    only = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
    bdir = os.path.join(ROOT, brand)
    cfg = json.load(open(os.path.join(bdir, 'brand.json'), encoding='utf-8'))
    if not CHROME: sys.exit('Не найден Google Chrome: установи его и запусти снова.')
    port, dist, p = serve(), os.path.join(bdir, 'dist'), f'p={brand}'
    want = lambda k: only in (None, k)

    if want('logo'):
        print('логотипы')
        if shutil.which('node'): subprocess.run(['node', 'scripts/export-svg.js', brand], cwd=ROOT)
        for k, w, h in [('mark_accent', 1200, 1200), ('mark_white', 1200, 1200), ('mark_dark', 1200, 1200), ('app_accent', 1200, 1200),
                        ('app_dark', 1200, 1200), ('avatar', 1080, 1080), ('badge', 1200, 1200), ('badge_on_accent', 1200, 1200),
                        ('lockup', 2400, 560), ('lockup_dark', 2400, 560)]:
            shot(port, 'logo.html', f'{p}&k={k}', os.path.join(dist, 'logo', f'{k}.png'), w, h, bg=False)
    if want('posts'):
        print('карусели')
        posts = json.load(open(os.path.join(bdir, 'posts.json'), encoding='utf-8')).get('carousels', []) if os.path.exists(os.path.join(bdir, 'posts.json')) else []
        for c in posts:
            for i in range(len(c['slides'])):
                shot(port, 'post.html', f"{p}&post={c['id']}&s=s{i + 1}", os.path.join(dist, 'posts', c['id'], f'{i + 1:02d}.png'), 1080, 1350)
    if want('reels'):
        print('рилс, сторис, актуальные')
        for k in ['r1', 'r2', 'r3', 'st']:
            shot(port, 'reels.html', f'{p}&s={k}', os.path.join(dist, 'reels', f'{k}.png'), 1080, 1920)
        for i in range(len(cfg.get('highlights') or [0] * 6)):
            shot(port, 'reels.html', f'{p}&s=hl{i + 1}', os.path.join(dist, 'highlights', f'hl{i + 1}.png'), 1080, 1080)
    if want('stickers'):
        print('стикеры')
        shot(port, 'stickers.html', p, os.path.join(dist, 'stickers', 'stickers.png'), 1680, 1300)
    if want('print'):
        print('печать')
        shot(port, 'print.html', f'{p}&s=cert', os.path.join(dist, 'print', 'cert.png'), 2480, 1754)
        shot(port, 'print.html', f'{p}&s=front', os.path.join(dist, 'print', 'card-front.png'), 1063, 591)
        shot(port, 'print.html', f'{p}&s=back', os.path.join(dist, 'print', 'card-back.png'), 1063, 591)
    if want('book'):
        print('брендбук PDF')
        out = os.path.join(dist, 'Брендбук.pdf')
        chrome(f'http://127.0.0.1:{port}/kit/brandbook.html?{p}', ['--no-pdf-header-footer', f'--print-to-pdf={out}'], budget=15000)
        print('  ', os.path.relpath(out, ROOT) if os.path.exists(out) else 'НЕ ПОЛУЧИЛОСЬ')
    print('готово:', os.path.relpath(dist, ROOT))


if __name__ == '__main__':
    main()
