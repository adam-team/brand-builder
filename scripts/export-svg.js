// Выгрузка логотипов в SVG (для печати, Canva, Figma): node scripts/export-svg.js <папка-бренда>
// Пример: node scripts/export-svg.js projects/anna  →  projects/anna/dist/logo/*.svg
const fs = require('fs'), path = require('path')
const B = require('../kit/brand.js')
const dir = process.argv[2]
if (!dir) { console.error('укажи папку бренда: node scripts/export-svg.js projects/<id>'); process.exit(1) }
const cfg = JSON.parse(fs.readFileSync(path.join(dir, 'brand.json'), 'utf8'))
const svg = fs.readFileSync(path.join(dir, cfg.mark || 'mark.svg'), 'utf8')
const C = B.palette(cfg), out = path.join(dir, 'dist', 'logo')
fs.mkdirSync(out, { recursive: true })
const files = {
  'mark-accent.svg': B.mark(cfg, svg, { fg: C.accent, size: 600 }),
  'mark-white.svg': B.mark(cfg, svg, { fg: '#FFFFFF', size: 600 }),
  'mark-light.svg': B.mark(cfg, svg, { fg: C.light_alt, size: 600 }),
  'mark-dark.svg': B.mark(cfg, svg, { fg: C.dark, size: 600 }),
  'app-accent.svg': B.mark(cfg, svg, { fg: C.on_accent, bg: C.accent, size: 600 }),
  'app-dark.svg': B.mark(cfg, svg, { fg: C.light_alt, bg: C.dark, size: 600 }),
  'badge.svg': B.badge(cfg, svg, { size: 800 }),
  'badge-on-accent.svg': B.badge(cfg, svg, { fg: C.on_accent, bg: C.accent, size: 800 }),
  'lockup.svg': B.lockup(cfg, svg, { size: 1200 }),
  'lockup-on-dark.svg': B.lockup(cfg, svg, { size: 1200, text: C.light_alt }),
}
for (const [n, s] of Object.entries(files)) fs.writeFileSync(path.join(out, n), s)
console.log(`SVG: ${Object.keys(files).length} файлов → ${out}`)
