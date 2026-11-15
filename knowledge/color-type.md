# Цвет и шрифты

- Палитра бренда — 11 полей в brand.json: accent, accent_on_dark, accent_deep, on_accent, dark, dark_surface, light, light_alt, soft, surface, muted.
- Пропорция 60% светлых, 30% тёмного, 10% акцента. Акцент — для плашек, кнопок, цифр, финала, не для фона всей ленты.
- Контраст текста ≥ 4,5:1 (брендбук считает автоматически в разделе «Сочетания»).
- 3 роли шрифтов: display (заголовки), body (текст), mono (теги, цифры, промпты); опционально script (подписи).
- Казахский: проверка `python3 scripts/check-fonts.py "<Шрифт>"`. Нет букв — в поле `kk` указать замену с похожим характером
  (Unbounded → Geologica, Manrope → Onest, JetBrains Mono → IBM Plex Mono, Tenor Sans → Golos Text, Jost → Onest).
