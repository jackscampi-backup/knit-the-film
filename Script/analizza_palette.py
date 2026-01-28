#!/usr/bin/env python3
"""
Analizza un'immagine palette cinematografica ed estrae i colori con le loro proporzioni.
Raggruppa colori simili per renderli lavorabili a maglia/uncinetto.
"""

import sys
from pathlib import Path
from PIL import Image
from collections import OrderedDict
import colorsys
import json

def rgb_to_hex(r, g, b):
    """Converte RGB in HEX."""
    return f"#{r:02x}{g:02x}{b:02x}"

def hex_to_rgb(hex_color):
    """Converte HEX in RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(c1, c2):
    """Calcola la distanza euclidea tra due colori RGB."""
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

def get_color_name(hex_color):
    """Assegna un nome descrittivo al colore basato su HSL."""
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    h = h * 360

    # Determina luminosità
    if l < 0.15:
        lum = "Nero"
    elif l < 0.35:
        lum = "Scuro"
    elif l > 0.85:
        lum = "Bianco"
    elif l > 0.7:
        lum = "Chiaro"
    else:
        lum = ""

    # Se saturazione bassa, è un grigio
    if s < 0.15:
        if l < 0.15:
            return "Nero"
        elif l > 0.85:
            return "Bianco"
        elif l > 0.6:
            return "Grigio Chiaro"
        elif l < 0.4:
            return "Grigio Scuro"
        else:
            return "Grigio"

    # Determina tonalità
    if h < 15 or h >= 345:
        hue = "Rosso"
    elif h < 45:
        hue = "Arancione"
    elif h < 65:
        hue = "Giallo"
    elif h < 150:
        hue = "Verde"
    elif h < 190:
        hue = "Ciano"
    elif h < 260:
        hue = "Blu"
    elif h < 290:
        hue = "Viola"
    elif h < 345:
        hue = "Magenta"
    else:
        hue = "Rosso"

    if lum and lum not in ["Nero", "Bianco"]:
        return f"{hue} {lum}"
    elif lum in ["Nero", "Bianco"]:
        return lum
    return hue

def extract_stripes(image_path):
    """Estrae le strisce orizzontali dall'immagine palette."""
    img = Image.open(image_path).convert('RGB')
    width, height = img.size

    stripes = []
    current_color = None
    current_height = 0

    for y in range(height):
        # Prendi il colore dal centro della riga
        pixel = img.getpixel((width // 2, y))
        hex_color = rgb_to_hex(*pixel)

        if hex_color == current_color:
            current_height += 1
        else:
            if current_color is not None:
                stripes.append({
                    'hex': current_color,
                    'rgb': hex_to_rgb(current_color),
                    'height': current_height,
                    'name': get_color_name(current_color)
                })
            current_color = hex_color
            current_height = 1

    # Aggiungi l'ultima striscia
    if current_color is not None:
        stripes.append({
            'hex': current_color,
            'rgb': hex_to_rgb(current_color),
            'height': current_height,
            'name': get_color_name(current_color)
        })

    return stripes, width, height

def group_similar_colors(stripes, threshold=40, min_height=2):
    """
    Raggruppa colori simili e filtra strisce troppo piccole.
    threshold: distanza massima per considerare due colori simili
    min_height: altezza minima per includere una striscia
    """
    if not stripes:
        return []

    grouped = []
    current_group = {
        'colors': [stripes[0]['hex']],
        'total_height': stripes[0]['height'],
        'dominant_hex': stripes[0]['hex'],
        'dominant_rgb': stripes[0]['rgb']
    }

    for i in range(1, len(stripes)):
        stripe = stripes[i]

        # Calcola distanza dal colore dominante del gruppo
        dist = color_distance(stripe['rgb'], current_group['dominant_rgb'])

        if dist < threshold:
            # Aggiungi al gruppo corrente
            current_group['colors'].append(stripe['hex'])
            current_group['total_height'] += stripe['height']
            # Aggiorna colore dominante se questo ha più altezza
            if stripe['height'] > current_group['total_height'] / len(current_group['colors']):
                current_group['dominant_hex'] = stripe['hex']
                current_group['dominant_rgb'] = stripe['rgb']
        else:
            # Salva gruppo corrente e inizia nuovo
            if current_group['total_height'] >= min_height:
                grouped.append(current_group)
            current_group = {
                'colors': [stripe['hex']],
                'total_height': stripe['height'],
                'dominant_hex': stripe['hex'],
                'dominant_rgb': stripe['rgb']
            }

    # Aggiungi ultimo gruppo
    if current_group['total_height'] >= min_height:
        grouped.append(current_group)

    return grouped

def analyze_palette(image_path, group_threshold=40, min_height=2):
    """
    Analizza completa di una palette cinematografica.
    Restituisce dati grezzi e raggruppati.
    """
    stripes, width, height = extract_stripes(image_path)
    grouped = group_similar_colors(stripes, group_threshold, min_height)

    # Calcola statistiche
    total_grouped_height = sum(g['total_height'] for g in grouped)

    result = {
        'file': str(image_path),
        'dimensions': {'width': width, 'height': height},
        'aspect_ratio': round(width / height, 4),
        'total_stripes': len(stripes),
        'grouped_colors': len(grouped),
        'stripes': stripes,
        'groups': []
    }

    for i, group in enumerate(grouped, 1):
        result['groups'].append({
            'order': i,
            'hex': group['dominant_hex'],
            'name': get_color_name(group['dominant_hex']),
            'height_px': group['total_height'],
            'percentage': round(group['total_height'] / height * 100, 1),
            'unique_colors': len(set(group['colors']))
        })

    return result

def print_analysis(analysis):
    """Stampa l'analisi in formato leggibile."""
    print(f"\n{'='*60}")
    print(f"ANALISI PALETTE: {Path(analysis['file']).stem}")
    print(f"{'='*60}")
    print(f"Dimensioni: {analysis['dimensions']['width']}x{analysis['dimensions']['height']} px")
    print(f"Aspect Ratio: {analysis['aspect_ratio']}")
    print(f"Strisce totali: {analysis['total_stripes']}")
    print(f"Gruppi colore: {analysis['grouped_colors']}")
    print(f"\n{'─'*60}")
    print(f"{'#':>3} | {'Colore':<20} | {'HEX':<9} | {'Px':>4} | {'%':>5}")
    print(f"{'─'*60}")

    for g in analysis['groups']:
        print(f"{g['order']:>3} | {g['name']:<20} | {g['hex']:<9} | {g['height_px']:>4} | {g['percentage']:>5.1f}")

    print(f"{'─'*60}\n")

def main():
    if len(sys.argv) < 2:
        print("Uso: python analizza_palette.py <immagine_palette> [threshold] [min_height]")
        print("  threshold: soglia raggruppamento colori (default: 40)")
        print("  min_height: altezza minima striscia in px (default: 2)")
        sys.exit(1)

    image_path = Path(sys.argv[1])
    threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    min_height = int(sys.argv[3]) if len(sys.argv) > 3 else 2

    if not image_path.exists():
        print(f"Errore: File non trovato: {image_path}")
        sys.exit(1)

    analysis = analyze_palette(image_path, threshold, min_height)
    print_analysis(analysis)

    # Salva anche JSON
    json_path = image_path.with_suffix('.json')
    with open(json_path, 'w') as f:
        json.dump(analysis, f, indent=2)
    print(f"Analisi salvata in: {json_path}")

if __name__ == "__main__":
    main()
