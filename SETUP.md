# Установка (делает агент)

1. Проверить: `python3 --version` (3.9+), `node --version` (18+), Google Chrome установлен.
2. `pip3 install fonttools pillow` — проверка шрифтов и картинки выбора.
3. Проверка сборки на примере: `python3 scripts/render.py examples/kuralay --only posts` — должны появиться PNG в
   `examples/kuralay/dist/posts/`. Нет Chrome — поставить; нет интернета — шрифты не загрузятся.
4. Владельцу написать одной строкой: «окружение готово», и начать этап 1.
