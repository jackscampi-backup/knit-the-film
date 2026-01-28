#!/usr/bin/env python3
"""
Genera pattern per lavori tessili da palette cinematografiche.
Legge l'immagine riga per riga (1600 righe = 1600 righe del lavoro).
Raggruppa righe consecutive con colore simile.
"""
import os
import sys
from PIL import Image
from collections import Counter
import colorsys

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(c1, c2):
    """Distanza euclidea tra due colori RGB"""
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

def get_row_color(img, y):
    """Ottiene il colore dominante di una riga"""
    colors = []
    for x in range(img.width):
        pixel = img.getpixel((x, y))
        if len(pixel) == 4:  # RGBA
            r, g, b, a = pixel
        else:  # RGB
            r, g, b = pixel
        colors.append((r, g, b))

    # Colore medio della riga
    avg_r = sum(c[0] for c in colors) // len(colors)
    avg_g = sum(c[1] for c in colors) // len(colors)
    avg_b = sum(c[2] for c in colors) // len(colors)

    return (avg_r, avg_g, avg_b)

def get_color_name(hex_color):
    """Genera un nome descrittivo per il colore"""
    r, g, b = hex_to_rgb(hex_color)

    # Converti in HSL
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    h *= 360

    # Casi speciali
    if l < 0.12:
        return "Nero"
    if l > 0.88:
        return "Bianco"
    if s < 0.1:
        if l > 0.7:
            return "Grigio Chiaro"
        elif l < 0.3:
            return "Grigio Scuro"
        return "Grigio"

    # Determina tonalità
    hues = [
        (15, "Rosso"), (45, "Arancione"), (70, "Giallo"),
        (150, "Verde"), (200, "Ciano"), (260, "Blu"),
        (310, "Viola"), (345, "Rosa"), (360, "Rosso")
    ]

    hue_name = "Rosso"
    for deg, name in hues:
        if h < deg:
            hue_name = name
            break

    if l < 0.3:
        return f"{hue_name} Scuro"
    if l > 0.7:
        return f"{hue_name} Chiaro"
    return hue_name

def analyze_palette(image_path, tolerance=30):
    """
    Analizza l'immagine riga per riga.
    Raggruppa righe consecutive con colore simile (entro tolerance).
    """
    img = Image.open(image_path).convert('RGB')

    segments = []  # [(start_row, end_row, hex_color, rgb)]

    current_color = None
    current_start = 0

    for y in range(img.height):
        row_color = get_row_color(img, y)

        if current_color is None:
            current_color = row_color
            current_start = y
        elif color_distance(row_color, current_color) > tolerance:
            # Nuovo segmento
            segments.append({
                'start': current_start + 1,  # 1-indexed
                'end': y,  # 1-indexed
                'rows': y - current_start,
                'hex': rgb_to_hex(*current_color),
                'rgb': current_color
            })
            current_color = row_color
            current_start = y

    # Ultimo segmento
    segments.append({
        'start': current_start + 1,
        'end': img.height,
        'rows': img.height - current_start,
        'hex': rgb_to_hex(*current_color),
        'rgb': current_color
    })

    return segments, img.height

def merge_similar_colors(segments, color_tolerance=100):
    """
    Unisce segmenti che usano colori molto simili in un unico colore.
    Mantiene l'ordine dei segmenti ma usa lo stesso hex per colori simili.
    """
    # Trova colori unici e raggruppa simili
    unique_colors = []
    color_mapping = {}  # rgb -> hex del gruppo

    for seg in segments:
        rgb = seg['rgb']
        found = False
        for uc in unique_colors:
            if color_distance(rgb, uc['rgb']) < color_tolerance:
                color_mapping[rgb] = uc['hex']
                found = True
                break
        if not found:
            unique_colors.append({'rgb': rgb, 'hex': seg['hex']})
            color_mapping[rgb] = seg['hex']

    # Applica mapping
    for seg in segments:
        seg['hex'] = color_mapping[seg['rgb']]

    # Unisci segmenti consecutivi con stesso colore
    merged = []
    for seg in segments:
        if merged and merged[-1]['hex'] == seg['hex']:
            merged[-1]['end'] = seg['end']
            merged[-1]['rows'] += seg['rows']
        else:
            merged.append(seg.copy())

    return merged, unique_colors

def generate_markdown(segments, unique_colors, total_rows, film_name, output_path):
    """Genera il file markdown con il pattern"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# {film_name}\n\n")

        f.write(f"**Righe totali:** {total_rows}\n\n")
        f.write(f"**Colori unici:** {len(unique_colors)}\n\n")

        f.write("---\n\n")
        f.write("## Colori da preparare\n\n")

        # Lista colori unici con quantità totali
        color_totals = {}
        for seg in segments:
            hex_color = seg['hex']
            color_totals[hex_color] = color_totals.get(hex_color, 0) + seg['rows']

        f.write("| # | Colore | HEX | Righe | % |\n")
        f.write("|:-:|--------|:---:|:-----:|:-:|\n")

        for i, (hex_color, rows) in enumerate(sorted(color_totals.items(), key=lambda x: -x[1]), 1):
            name = get_color_name(hex_color)
            pct = rows / total_rows * 100
            f.write(f"| {i} | {name} | `{hex_color}` | {rows} | {pct:.1f}% |\n")

        f.write("\n---\n\n")
        f.write("## Pattern (dall'alto al basso)\n\n")

        f.write("| Righe | Colore | HEX | Quante |\n")
        f.write("|:-----:|--------|:---:|:------:|\n")

        for seg in segments:
            name = get_color_name(seg['hex'])
            if seg['rows'] == 1:
                f.write(f"| {seg['start']} | {name} | `{seg['hex']}` | 1 |\n")
            else:
                f.write(f"| {seg['start']}-{seg['end']} | {name} | `{seg['hex']}` | {seg['rows']} |\n")

        f.write("\n---\n\n")
        f.write("## Come usare\n\n")
        f.write(f"Questo pattern ha **{total_rows} righe** (una per ogni riga di pixel dell'immagine).\n\n")
        f.write("Se vuoi ridurre le righe, dividi tutto per un fattore:\n")
        f.write(f"- ÷2 = {total_rows//2} righe\n")
        f.write(f"- ÷4 = {total_rows//4} righe\n")
        f.write(f"- ÷8 = {total_rows//8} righe\n")

def main():
    if len(sys.argv) < 2:
        print("Uso: python genera_pattern_v2.py <immagine.png> [tolerance]")
        print("  tolerance: quanto due colori devono essere diversi per essere separati (default: 30)")
        sys.exit(1)

    image_path = sys.argv[1]
    tolerance = int(sys.argv[2]) if len(sys.argv) > 2 else 30

    if not os.path.exists(image_path):
        print(f"File non trovato: {image_path}")
        sys.exit(1)

    # Nome film dal file
    basename = os.path.basename(image_path).replace('.png', '')
    film_name = basename.replace('-', ' ').title()

    print(f"Analisi: {film_name}")
    print(f"Tolerance: {tolerance}")

    # Analizza
    segments, total_rows = analyze_palette(image_path, tolerance=tolerance)
    print(f"Righe immagine: {total_rows}")
    print(f"Segmenti iniziali: {len(segments)}")

    # Unisci colori simili (tolerance alta per avere 8-12 colori)
    segments, unique_colors = merge_similar_colors(segments, color_tolerance=100)
    print(f"Dopo merge: {len(segments)} segmenti, {len(unique_colors)} colori unici")

    # Output
    output_dir = os.path.join(os.path.dirname(os.path.dirname(image_path)), 'Pattern')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{basename}.md")

    generate_markdown(segments, unique_colors, total_rows, film_name, output_path)
    print(f"Salvato: {output_path}")

if __name__ == "__main__":
    main()
