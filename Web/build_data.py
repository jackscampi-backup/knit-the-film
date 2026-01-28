#!/usr/bin/env python3
"""
Estrae colori E percentuali dai pattern .md e genera films_data.js
"""
import os
import re
import json

PATTERN_DIR = "../Pattern"
OUTPUT_JS = "films_data.js"
OUTPUT_JSON = "films.json"

def parse_pattern_file(filepath):
    """Estrae slug, title, colors con percentuali da un file .md"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Estrai titolo dalla prima riga (# Title Year)
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if not title_match:
        return None
    title = title_match.group(1)

    # Slug dal nome file
    slug = os.path.basename(filepath).replace('.md', '')

    # Estrai colori e percentuali dalla tabella
    # Pattern: | 1 | Nome Colore | `#hex` | 10.5% |
    colors = []
    pattern = r'\|\s*\d+\s*\|[^|]+\|\s*`(#[0-9a-fA-F]{6})`\s*\|\s*([\d.]+)%\s*\|'

    for match in re.finditer(pattern, content):
        hex_color = match.group(1).lower()
        pct = float(match.group(2))
        colors.append({"hex": hex_color, "pct": pct})

    if not colors:
        return None

    return {
        "slug": slug,
        "title": title,
        "colors": colors
    }

def main():
    films = []

    # Leggi tutti i pattern
    for filename in sorted(os.listdir(PATTERN_DIR)):
        if filename.endswith('.md'):
            filepath = os.path.join(PATTERN_DIR, filename)
            data = parse_pattern_file(filepath)
            if data:
                films.append(data)
                print(f"✓ {data['title']} ({len(data['colors'])} colors)")

    print(f"\nTotal: {len(films)} films")

    # Salva JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(films, f, indent=2)
    print(f"Saved {OUTPUT_JSON}")

    # Salva JS
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write("const FILMS_DATA = ")
        json.dump(films, f)
        f.write(";\n")
    print(f"Saved {OUTPUT_JS}")

if __name__ == "__main__":
    main()
