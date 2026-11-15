# Карта репозитория

- Бренд = `projects/<id>/brand.json` + `mark.svg` + `posts.json` (+ фото, если есть, путь относительно папки бренда).
- Шаблоны `kit/*.html` открываются как `kit/<страница>.html?p=projects/<id>` через локальный сервер (его поднимает `scripts/render.py`).
- Результат — `projects/<id>/dist/`: logo (PNG + SVG), posts, reels, highlights, stickers, print, `Брендбук.pdf`.
- `dist/` не коммитится в ученических репозиториях без желания владельца (тяжёлые файлы).
