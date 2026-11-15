#!/usr/bin/env python3
"""BRAND_GUIDE.md — инструкция для любого ИИ (ChatGPT, Claude, Gemini, Canva AI), собранная из brand.json.
    python3 scripts/guide.py projects/<id>     →  projects/<id>/BRAND_GUIDE.md"""
import json, os, re, sys
if len(sys.argv) < 2: sys.exit(__doc__)
d = sys.argv[1].rstrip('/'); b = json.load(open(os.path.join(d, 'brand.json'), encoding='utf-8'))
t = lambda s: re.sub(r'<[^>]+>', '', s or '')
C, F, I, E = b['colors'], b['fonts'], b.get('idea', {}), b.get('elements', {})
names = {k: (n, u) for k, n, u in b.get('color_names', [])}
L = [f"# Брендбук {b['name']} — инструкция для ИИ", '',
     '> Прикрепите этот файл к ChatGPT, Claude, Gemini или Canva AI и напишите: «Сделай карусель по моему брендбуку на тему …». Правила ниже соблюдать строго.', '',
     '## 1. Идея', '', f"**{t(I.get('title'))} {t(I.get('accent'))}** {t(I.get('text'))}", '',
     'Опоры: ' + ' · '.join(f"**{h}** — {x}" for h, x in I.get('pillars', [])), '',
     '## 2. Цвета (только эти)', '', '| Цвет | HEX | Где |', '|---|---|---|']
L += [f"| {names.get(k, (k, ''))[0]} | `{v}` | {names.get(k, ('', ''))[1]} |" for k, v in C.items()]
L += ['', t(b.get('color_ratio', '')), '', '## 3. Шрифты', '']
for role, label in [('display', 'заголовки'), ('body', 'текст'), ('mono', 'теги, номера, промпты'), ('script', 'только подписи')]:
    if role in F:
        x = F[role]; kk = f" (казахские буквы — из {x['kk']})" if x.get('kk') and x['kk'] != x['family'] else ''
        L.append(f"- **{x['family']}** — {label}{kk}")
L += ['', '## 4. Знак', ''] + [f"- **{h}** {t(x)}" for h, x in b.get('mark_story', [])] + [''] + [f"- {x}" for x in b.get('mark_rules', [])]
L += ['', '## 5. Фирменные элементы', ''] + [f"- **{h}** — {t(x)}" for h, x in b.get('signature', [])]
L += [f"- Узор фона: `{E.get('pattern', 'dots')}`; выделение слова: `{E.get('highlight', 'pill')}`; линия через карусель: {'да' if E.get('route') else 'нет'}", '',
      '## 6. Карусель 1080 × 1350', '',
      'Типы слайдов: cover (фото + заголовок), text, steps (шаги 01–04), stat (было → стало), pwin (фото в окне), chat (диалог), cards (карточки с ценой), pcode (промпт), cta (финал с кодовым словом).',
      f"Сверху тег и номер «02 / 07», снизу {b.get('handle', '')} и «{b.get('swipe', 'листай →')}». Финал — кодовое слово «{b.get('cta_word', '')}».", '',
      '## 7. Тексты', ''] + [f"- **{h}** {t(x)}" for h, x in b.get('voice', [])]
L += ['', '## 8. Чек-лист', ''] + [f"- [ ] {t(x)}" for x in b.get('checklist', [])]
L += ['', '## 9. CSS', '', '```css', ':root {'] + [f"  --{k.replace('_', '-')}: {v};" for k, v in C.items()]
L += [f"  --{r}: '{F[r]['family']}', '{F[r].get('kk', F[r]['family'])}';" for r in F] + ['}', '```', '']
open(os.path.join(d, 'BRAND_GUIDE.md'), 'w', encoding='utf-8').write('\n'.join(L))
print('→', os.path.join(d, 'BRAND_GUIDE.md'))
