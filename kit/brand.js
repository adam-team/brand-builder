// Ядро бренда: из brand.json и знака mark.svg собирает логотипы, бейдж, узор фона и CSS-переменные.
// Один файл для страниц kit/*.html (браузер) и для выгрузки SVG (node scripts/export-svg.mjs).
// Знак mark.svg рисуется ОДНИМ цветом currentColor в viewBox 0 0 240 240: цвет подставляется здесь.
(function (root) {
  const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

  // Палитра с запасными значениями: если в brand.json чего-то нет, бренд всё равно собирается
  function palette(cfg) {
    const c = Object.assign({
      accent: '#C8102E', accent_on_dark: '#FF4D63', accent_deep: '#8E0B20',
      dark: '#0E0D0D', dark_surface: '#1F1C1B', light: '#F4F2EF', light_alt: '#F3EDE4',
      soft: '#E8D9C2', surface: '#FFFFFF', muted: '#A69D92', on_accent: '#FFFFFF',
    }, cfg.colors || {})
    return c
  }

  // Знак нужного цвета. bg — залитая иконка-аватар (скруглённый квадрат или круг)
  function mark(cfg, markSvg, { fg, bg = 'none', size = 240, shape = 'square' } = {}) {
    const C = palette(cfg)
    fg = fg || C.accent
    // Атрибуты корневого <svg> (fill="none", stroke="currentColor"…) переносим на группу, иначе знак зальётся чёрным
    const rootTag = (markSvg.match(/<svg([^>]*)>/) || ['', ''])[1]
    const keep = (rootTag.match(/\s(fill|stroke|stroke-[a-z]+)="[^"]*"/g) || []).join('')
    const inner = `<g${keep}>` + markSvg.replace(/<\?xml[^>]*>/, '').replace(/<!--[\s\S]*?-->/g, '').replace(/<svg[^>]*>/, '').replace(/<\/svg>\s*$/, '') + '</g>'
    const plate = bg === 'none' ? '' : shape === 'circle'
      ? `<circle cx="120" cy="120" r="120" fill="${bg}"/>`
      : `<rect x="0" y="0" width="240" height="240" rx="${Math.round((cfg.radius ?? 30) * 2)}" fill="${bg}"/>`
    const k = bg === 'none' ? '' : ' transform="translate(30 30) scale(.75)"'
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="${size}" height="${size}">${plate}<g color="${fg}" style="color:${fg}"${k}>${inner}</g></svg>`
  }

  // Горизонтальный логотип: знак + имя + подпись моно-шрифтом
  function lockup(cfg, markSvg, { fg, text, sub, size = 600 } = {}) {
    const C = palette(cfg), F = fonts(cfg)
    fg = fg || C.accent; text = text || C.dark; sub = sub || C.muted
    const name = esc(cfg.name), tag = esc(cfg.tagline || '')
    const w = Math.max(600, 170 + name.length * 24)
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} 140" width="${size}" height="${Math.round(size * 140 / w)}">
  <g transform="translate(10 14) scale(.475)">${mark(cfg, markSvg, { fg, size: 240 }).replace(/<\/?svg[^>]*>/g, '')}</g>
  <text x="150" y="70" font-family="${F.display.family}, ${F.display.kk}, Arial, sans-serif" font-weight="${F.display.weight}" font-size="38" letter-spacing="-0.5" fill="${text}">${name}</text>
  ${tag ? `<text x="152" y="106" font-family="${F.mono.family}, ${F.mono.kk}, monospace" font-weight="500" font-size="17" letter-spacing="1" fill="${sub}">// ${tag}</text>` : ''}
</svg>`
  }

  // Круглый бейдж: знак в центре, имя и подпись по кругу (стикер, упаковка, сертификат)
  function badge(cfg, markSvg, { fg, bg, size = 320 } = {}) {
    const C = palette(cfg), F = fonts(cfg)
    fg = fg || C.accent; bg = bg || C.surface
    const t = esc((cfg.badge_text || `${cfg.name} · ${cfg.tagline || ''} · `).toUpperCase())
    const id = 'bp' + Math.random().toString(36).slice(2, 7)
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 320" width="${size}" height="${size}">
  ${bg === 'none' ? '' : `<circle cx="160" cy="160" r="156" fill="${bg}"/>`}
  <circle cx="160" cy="160" r="150" fill="none" stroke="${fg}" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>
  <defs><path id="${id}" d="M160 160m-120 0a120 120 0 1 1 240 0a120 120 0 1 1 -240 0"/></defs>
  <text font-family="${F.mono.family}, ${F.mono.kk}, monospace" font-weight="700" font-size="17" fill="${fg}"><textPath href="#${id}" textLength="748" lengthAdjust="spacing">${t}</textPath></text>
  <g transform="translate(103 103) scale(.475)">${mark(cfg, markSvg, { fg }).replace(/<\/?svg[^>]*>/g, '')}</g>
</svg>`
  }

  // Узор фона: точки, клетка, линии или ничего (elements.pattern в brand.json)
  function pattern(cfg, { fg, opacity = 0.12, step = 36 } = {}) {
    const kind = (cfg.elements || {}).pattern || 'dots'
    fg = fg || palette(cfg).dark
    let body = ''
    if (kind === 'dots') body = `<circle cx="${step / 2}" cy="${step / 2}" r="1.6" fill="${fg}" fill-opacity="${opacity}"/>`
    else if (kind === 'grid') body = `<path d="M${step} 0V${step}H0" fill="none" stroke="${fg}" stroke-opacity="${opacity}" stroke-width="1"/>`
    else if (kind === 'lines') body = `<path d="M0 ${step - 1}H${step}" stroke="${fg}" stroke-opacity="${opacity}" stroke-width="1"/>`
    else if (kind === 'diag') body = `<path d="M0 ${step}L${step} 0" stroke="${fg}" stroke-opacity="${opacity}" stroke-width="1"/>`
    else return 'none'
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${step}" height="${step}">${body}</svg>`
    return 'url("data:image/svg+xml;utf8,' + encodeURIComponent(svg) + '")'
  }

  // Шрифты: основной + запасной для казахских букв (браузер сам берёт ә ғ қ ң ө ұ ү һ і из запасного)
  function fonts(cfg) {
    const f = cfg.fonts || {}
    const one = (x, def, kk) => Object.assign({ family: def, weight: 700, kk: kk }, x || {})
    return {
      display: one(f.display, 'Montserrat', 'Montserrat'),
      body: one(f.body, 'Inter', 'Inter'),
      mono: one(f.mono, 'IBM Plex Mono', 'IBM Plex Mono'),
      script: f.script ? one(f.script, 'Cormorant', 'Cormorant') : null,
    }
  }

  // Ссылка Google Fonts на все семейства бренда (и их казахские замены)
  function fontsHref(cfg) {
    const F = fonts(cfg), fam = new Map()
    const add = (name, ital) => { if (name && !fam.has(name)) fam.set(name, ital) }
    for (const k of ['display', 'body', 'mono']) { add(F[k].family); add(F[k].kk) }
    if (F.script) { add(F.script.family, F.script.italic); add(F.script.kk, F.script.italic) }
    const q = [...fam].map(([n, ital]) => 'family=' + n.replace(/ /g, '+') + (ital ? ':ital,wght@1,400;1,500' : ':wght@400;500;600;700;800'))
    return 'https://fonts.googleapis.com/css2?' + q.join('&') + '&display=swap'
  }

  // CSS-переменные для всех страниц kit/
  function cssVars(cfg) {
    const C = palette(cfg), F = fonts(cfg), r = cfg.radius ?? 30
    const stack = (x, gen) => `'${x.family}', '${x.kk}', ${gen}`
    return `:root{--accent:${C.accent};--accent-dark:${C.accent_on_dark};--accent-deep:${C.accent_deep};--on-accent:${C.on_accent};` +
      `--dark:${C.dark};--dark-surface:${C.dark_surface};--light:${C.light};--light-alt:${C.light_alt};--soft:${C.soft};--surface:${C.surface};--muted:${C.muted};` +
      `--display:${stack(F.display, 'sans-serif')};--body:${stack(F.body, 'sans-serif')};--mono:${stack(F.mono, 'monospace')};` +
      `--script:${F.script ? stack(F.script, 'serif') : 'var(--display)'};--dw:${F.display.weight};--track:${F.display.tracking ?? -0.03}em;` +
      `--case:${F.display.case || 'none'};--r:${r}px;--r2:${Math.round(r * 0.6)}px;}`
  }

  // Линия-маршрут через всю карусель (elements.route): волна в нижней полосе
  function routePath(n, W = 1080, y = 1170) {
    const pts = []
    for (let i = 0; i <= n * 4; i++) pts.push([40 + i * (W * n - 120) / (n * 4), y + Math.sin(i * 1.15) * 34])
    let d = `M${pts[0][0]} ${pts[0][1]}`
    for (let i = 1; i < pts.length; i++) {
      const [x0, y0] = pts[i - 1], [x1, y1] = pts[i], mx = (x0 + x1) / 2
      d += ` C${mx} ${y0} ${mx} ${y1} ${x1} ${y1}`
    }
    return { d, end: pts[pts.length - 1], y }
  }

  // Браузер: загрузить проект ?p=<id> (или examples/kuralay по умолчанию), применить стиль
  async function load() {
    const q = new URLSearchParams(location.search)
    const p = q.get('p') || 'examples/kuralay'
    const base = '../' + (p.includes('/') ? p : 'projects/' + p) + '/'
    const cfg = await (await fetch(base + 'brand.json')).json()
    const markSvg = await (await fetch(base + (cfg.mark || 'mark.svg'))).text()
    const link = document.createElement('link'); link.rel = 'stylesheet'; link.href = fontsHref(cfg); document.head.appendChild(link)
    const st = document.createElement('style'); st.textContent = cssVars(cfg); document.head.appendChild(st)
    let posts = null
    try { const r = await fetch(base + 'posts.json'); if (r.ok) posts = await r.json() } catch (e) {}
    const api = {
      cfg, base, posts, C: palette(cfg), F: fonts(cfg),
      mark: (o) => mark(cfg, markSvg, o), lockup: (o) => lockup(cfg, markSvg, o), badge: (o) => badge(cfg, markSvg, o),
      pattern: (o) => pattern(cfg, o), routePath, photo: (f) => f ? (/^https?:/.test(f) ? f : base + f) : '',
    }
    // Ждём сами шрифты (и кириллицу, и казахские буквы), иначе подгонка заголовков посчитает ширину по системному шрифту
    const F = api.F, probe = 'Аа Әә Ққ Aa 0'
    await Promise.all([F.display, F.body, F.mono, F.script].filter(Boolean).flatMap((x) => [x.family, x.kk])
      .map((fam) => document.fonts.load(`${F.display.weight} 40px "${fam}"`, probe).catch(() => null)))
    await document.fonts.ready
    return api
  }

  const lib = { palette, mark, lockup, badge, pattern, fonts, fontsHref, cssVars, routePath, esc, load }
  if (typeof module !== 'undefined' && module.exports) module.exports = lib
  else root.Brand = lib
})(this)
