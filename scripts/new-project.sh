#!/bin/sh
# Новая папка бренда: bash scripts/new-project.sh <id>   (латиница, цифры, дефис)
set -e
id="$1"; [ -z "$id" ] && { echo "укажи id: bash scripts/new-project.sh anna-english"; exit 1; }
cd "$(dirname "$0")/.."
[ -e "projects/$id" ] && { echo "projects/$id уже есть"; exit 1; }
cp -R projects/_template "projects/$id"
echo "создано: projects/$id  (BRIEF.md, IDEA.md, DESIGN.md, LOGO.md, brand.json, mark.svg, posts.json)"
