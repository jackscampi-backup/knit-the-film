#!/usr/bin/env python3
"""
Estrae i dati dai pattern v2 (con segmenti) per il sito web.
"""
import os
import re
import json

PATTERN_DIR = "../Pattern"
OUTPUT_JS = "films_data.js"
OUTPUT_JSON = "films.json"

def parse_pattern_file(filepath):
    """Estrae dati dal nuovo formato pattern v2"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Titolo
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if not title_match:
        return None
    title = title_match.group(1)

    # Slug dal nome file
    slug = os.path.basename(filepath).replace('.md', '')

    # Righe totali
    rows_match = re.search(r'\*\*Righe totali:\*\* (\d+)', content)
    total_rows = int(rows_match.group(1)) if rows_match else 1600

    # Estrai colori dalla tabella "Colori da preparare"
    # Pattern: | 1 | Nome | `#hex` | 123 | 10.5% |
    colors = []
    color_pattern = r'\|\s*\d+\s*\|[^|]+\|\s*`(#[0-9a-fA-F]{6})`\s*\|\s*(\d+)\s*\|\s*([\d.]+)%\s*\|'

    for match in re.finditer(color_pattern, content):
        hex_color = match.group(1).lower()
        rows = int(match.group(2))
        pct = float(match.group(3))
        colors.append({"hex": hex_color, "rows": rows, "pct": pct})

    if not colors:
        return None

    # Estrai segmenti dalla tabella "Pattern"
    # Pattern: | 1-56 | Nome | `#hex` | 56 | o | 1 | Nome | `#hex` | 1 |
    segments = []
    seg_pattern = r'\|\s*([\d-]+)\s*\|[^|]+\|\s*`(#[0-9a-fA-F]{6})`\s*\|\s*(\d+)\s*\|'

    # Trova la sezione Pattern
    pattern_section = re.search(r'## Pattern.*?\n\n(.*?)(?=\n---|\Z)', content, re.DOTALL)
    if pattern_section:
        for match in re.finditer(seg_pattern, pattern_section.group(1)):
            row_range = match.group(1)
            hex_color = match.group(2).lower()
            count = int(match.group(3))

            if '-' in row_range:
                start, end = row_range.split('-')
                start, end = int(start), int(end)
            else:
                start = end = int(row_range)

            segments.append({
                "start": start,
                "end": end,
                "hex": hex_color,
                "rows": count
            })

    return {
        "slug": slug,
        "title": title,
        "total_rows": total_rows,
        "colors": colors,
        "segments": segments
    }

def main():
    films = []

    for filename in sorted(os.listdir(PATTERN_DIR)):
        if filename.endswith('.md'):
            filepath = os.path.join(PATTERN_DIR, filename)
            data = parse_pattern_file(filepath)
            if data and data['colors']:
                films.append(data)
                print(f"✓ {data['title']} ({len(data['colors'])} colors, {len(data['segments'])} segments)")

    print(f"\nTotal: {len(films)} films")

    # Salva JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(films, f, indent=2)
    print(f"Saved {OUTPUT_JSON}")

    # Salva JS (compatto per velocità)
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write("const FILMS_DATA = ")
        json.dump(films, f, separators=(',', ':'))
        f.write(";\n")
    print(f"Saved {OUTPUT_JS}")

if __name__ == "__main__":
    main()
