# Brand Builder

Репозиторий для **Claude Code** и **Codex**: агент опрашивает тебя по этапам и собирает **брендбук с нуля** —
идея, знак и логотип, цвета, шрифты (с проверкой казахских букв), фирменные элементы, карусели, обложки рилс,
актуальные, стикеры, визитка, сертификат, PDF-брендбук и инструкция для любого ИИ.

> **Агенту:** склонируй репозиторий, подготовь окружение по [`SETUP.md`](SETUP.md) и сразу начни опрос по
> [`docs/agent-contract/WORKFLOW.md`](docs/agent-contract/WORKFLOW.md). Один вопрос за раз, с вариантами ответа.
> Новичку: [`START.md`](START.md).

## Как это работает

1. **Бриф ⏸** — кто ты, для кого, что продаёшь, кто нравится и на кого не хочешь быть похожей.
2. **Идея ⏸** — 3 метафоры бренда на выбор (пример: «Проект — это маршрут. ИИ его ускоряет»).
3. **Стиль ⏸** — 24 готовых стиля (картинки `reference/style-previews/styles-A…E.jpg`) или 25 «свой».
4. **Знак ⏸** — 3 варианта `mark.svg`, выбор, история знака.
5. **Голос ⏸** — как пишем, кодовое слово.
6. **Сборка** — `python3 scripts/render.py projects/<id>`: всё в PNG, SVG и PDF.
7. **Сдача ⏸** — `BRAND_GUIDE.md` для ChatGPT/Claude/Canva AI.

Весь бренд живёт в **одном файле `brand.json`** + знак `mark.svg` + тексты постов `posts.json`.
Шаблоны в `kit/` общие для всех: меняешь `brand.json` — меняется весь брендбук.

## Библиотека стилей (24 + свой)

| Группа | Номера | Стили |
|---|---|---|
| A · Монохром | 1–4 | Чистый монохром, Графит и бумага, Ночной монохром, Газета |
| B · Дорогой | 5–9 | Старые деньги, Чёрное золото, Бургунди, Тихая роскошь, Сапфир |
| C · Тёплый | 10–13 | Терракота, Оливковая роща, Персик и кофе, Скандинавия |
| D · Яркий | 14–18 | Неон на чёрном, Поп-арт, Электрик, Фуксия, Спорт |
| E · Особенные | 19–24 | Медицина-чистота, Степь (казахский модерн), Академия, Y2K стекло, Бохо, ИИ + проекты (Куралай) |
| 25 | — | **Свой стиль** по скриншотам, ссылкам, фото |

Откуда берутся дизайны и как найти свои: [`docs/DESIGN-SOURCES.md`](docs/DESIGN-SOURCES.md).

## Примеры

| Папка | Что |
|---|---|
| `examples/kuralay/` | настоящий брендбук Куралай v2 (стиль 24): знак-маршрут, красный, Unbounded/Manrope/JetBrains Mono |
| `examples/demo-oldmoney/` | демо-бренд риелтора в стиле 5 «Старые деньги»: тот же код, другой бренд |

История, как делался брендбук Куралай (что отклонили и почему): [`docs/CASE-KURALAY.md`](docs/CASE-KURALAY.md).

## Что внутри

| Папка или файл | Что |
|---|---|
| `CLAUDE.md`, `AGENTS.md` | точки входа для Claude Code и Codex |
| `docs/agent-contract/` | `WORKFLOW.md` (этапы), `QUESTIONS.md` (вопросы с вариантами) |
| `knowledge/` | как делать идею, знак, цвет, шрифты, карусели |
| `kit/` | шаблоны: `brand.js` (ядро), `post.html`, `reels.html`, `stickers.html`, `print.html`, `logo.html`, `brandbook.html`, `styles.html` |
| `patterns/` | `styles.json` (24 стиля), `fonts.json` (38 шрифтов с проверкой казахского) |
| `projects/_template/` | заготовка бренда ученика |
| `scripts/` | `new-project.sh`, `style.py`, `render.py`, `export-svg.js`, `check-fonts.py`, `guide.py`, `build-previews.py` |

## Команды

```bash
bash scripts/new-project.sh anna                        # папка бренда
python3 scripts/style.py list                           # список стилей
python3 scripts/style.py 5 --name "Anna" > projects/anna/brand.json
python3 scripts/check-fonts.py projects/anna/brand.json # казахские буквы в шрифтах
python3 scripts/render.py projects/anna                 # весь брендбук → projects/anna/dist/
python3 scripts/render.py projects/anna --only posts    # только карусели
python3 scripts/guide.py projects/anna                  # BRAND_GUIDE.md для ИИ
```

Структура контракта (этапы с паузами, файлы-замки) адаптирована из
[reels-pipline-automotaj](https://github.com/saint4ai/reels-pipline-automotaj) (MIT) и `platform-builder`. См. [`NOTICE.md`](NOTICE.md).
