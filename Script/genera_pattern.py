#!/usr/bin/env python3
"""
Estrae i colori in ordine da una palette cinematografica.
Output: lista colori con proporzioni relative.

Uso:
  python genera_pattern.py <immagine> [--colori 15]
"""

import sys
import argparse
from pathlib import Path
from PIL import Image
import colorsys

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

def get_color_name(hex_color):
    """Nome descrittivo del colore."""
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    h = h * 360

    if l < 0.12:
        return "Nero"
    if l > 0.88:
        return "Bianco"

    if s < 0.15:
        if l > 0.6:
            return "Grigio Chiaro"
        elif l < 0.4:
            return "Grigio Scuro"
        return "Grigio"

    # Tonalità
    if h < 15 or h >= 345:
        hue = "Rosso"
    elif h < 45:
        hue = "Arancione"
    elif h < 70:
        hue = "Giallo"
    elif h < 150:
        hue = "Verde"
    elif h < 200:
        hue = "Ciano"
    elif h < 260:
        hue = "Blu"
    elif h < 310:
        hue = "Viola"
    else:
        hue = "Rosa"

    if l < 0.35:
        return f"{hue} Scuro"
    elif l > 0.65:
        return f"{hue} Chiaro"
    return hue

def extract_colors(image_path, max_colors=15, threshold=35):
    """
    Estrae i colori dalla palette, raggruppati e in ordine.
    Restituisce lista di (hex, nome, proporzione).
    """
    img = Image.open(image_path).convert('RGB')
    width, height = img.size

    # Estrai strisce orizzontali
    stripes = []
    current_color = None
    current_height = 0

    for y in range(height):
        pixel = img.getpixel((width // 2, y))
        hex_color = rgb_to_hex(*pixel)

        if hex_color == current_color:
            current_height += 1
        else:
            if current_color:
                stripes.append({'hex': current_color, 'height': current_height})
            current_color = hex_color
            current_height = 1

    if current_color:
        stripes.append({'hex': current_color, 'height': current_height})

    # Raggruppa colori simili consecutivi
    grouped = []
    current = {'hex': stripes[0]['hex'], 'rgb': hex_to_rgb(stripes[0]['hex']), 'height': stripes[0]['height']}

    for s in stripes[1:]:
        rgb = hex_to_rgb(s['hex'])
        if color_distance(rgb, current['rgb']) < threshold:
            current['height'] += s['height']
        else:
            grouped.append(current)
            current = {'hex': s['hex'], 'rgb': rgb, 'height': s['height']}
    grouped.append(current)

    # Semplifica a max_colors
    if len(grouped) > max_colors:
        ratio = len(grouped) / max_colors
        simplified = []
        i = 0
        while i < len(grouped) and len(simplified) < max_colors:
            block_end = min(int(i + ratio), len(grouped))
            block = grouped[i:block_end] if block_end > i else [grouped[i]]

            total_h = sum(g['height'] for g in block)
            dominant = max(block, key=lambda x: x['height'])

            simplified.append({'hex': dominant['hex'], 'height': total_h})
            i = block_end if block_end > i else i + 1
        grouped = simplified

    # Calcola proporzioni (somma = 100)
    total = sum(g['height'] for g in grouped)
    colors = []
    for g in grouped:
        prop = round(g['height'] / total * 100, 1)
        colors.append({
            'hex': g['hex'],
            'nome': get_color_name(g['hex']),
            'proporzione': prop
        })

    return colors

def generate_output(colors, film_name, output_path):
    """Genera file Markdown con la lista colori."""

    md = f"""# {film_name}

## Colori (dall'alto al basso)

| # | Colore | HEX | % |
|:-:|--------|:---:|:-:|
"""
    for i, c in enumerate(colors, 1):
        md += f"| {i} | {c['nome']} | `{c['hex']}` | {c['proporzione']}% |\n"

    md += f"""
---

## Lista per acquisto filati

"""
    for i, c in enumerate(colors, 1):
        md += f"{i}. `{c['hex']}` — {c['nome']} ({c['proporzione']}%)\n"

    md += f"""
---

## Come usare

Le proporzioni indicano quanto spazio occupa ogni colore.

**Esempio pratico:**
- Se fai 100 righe totali → colore al 15% = 15 righe
- Se fai 200 righe totali → colore al 15% = 30 righe

Scegli tu le dimensioni, mantieni le proporzioni.
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)

def main():
    parser = argparse.ArgumentParser(description='Estrai colori da palette cinematografica')
    parser.add_argument('immagine', help='Percorso immagine palette')
    parser.add_argument('--colori', '-c', type=int, default=15, help='Numero colori (default: 15)')
    parser.add_argument('--threshold', '-t', type=int, default=35, help='Soglia raggruppamento (default: 35)')
    parser.add_argument('--output', '-o', help='File output (default: stesso nome .md)')

    args = parser.parse_args()
    image_path = Path(args.immagine)

    if not image_path.exists():
        print(f"File non trovato: {image_path}")
        sys.exit(1)

    # Estrai colori
    colors = extract_colors(image_path, args.colori, args.threshold)

    # Nome film
    film_name = image_path.stem.replace('-', ' ').title()

    # Stampa a console
    print(f"\n{'═'*50}")
    print(f"  {film_name}")
    print(f"{'═'*50}")
    print(f"{'#':>3}  {'Colore':<18} {'HEX':<10} {'%':>5}")
    print(f"{'─'*50}")
    for i, c in enumerate(colors, 1):
        print(f"{i:>3}  {c['nome']:<18} {c['hex']:<10} {c['proporzione']:>5}%")
    print(f"{'─'*50}\n")

    # Salva file
    output_path = Path(args.output) if args.output else image_path.parent.parent / 'Pattern' / f"{image_path.stem}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generate_output(colors, film_name, output_path)
    print(f"Salvato: {output_path}\n")

if __name__ == "__main__":
    main()
