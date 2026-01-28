# Knit the Film

Transform film color palettes into knitting and crochet patterns.

**Live Demo:** https://jackscampi-backup.github.io/knit-the-film/

---

## What is this?

Every film has a unique "color signature" - the dominant colors that appear throughout the movie. This project transforms those colors into practical patterns for textile crafts: knitting, crochet, and weaving.

The result? Scarves, blankets, cushions, and other textile creations that visually "tell" a film through its colors.

---

## Features

- **257 film palettes** from [The Colors of Motion](https://thecolorsofmotion.com/)
- **Mobile-first web interface** with product selector (Scarf, Blanket, Mousepad, Cushion, Custom)
- **Automatic calculations** for rows, stitches, and yarn needed
- **Yarn ball estimates** (different for knitting vs crochet)
- **Pattern instructions** with segment-by-segment guidance
- **Custom dimensions** support

---

## How it works

1. Each film palette image (1000×1600 px) represents the entire movie
2. Each horizontal row = one frame, compressed to its average color
3. Top to bottom = start to end of the film
4. The script analyzes the image row by row, grouping similar colors
5. Output: 8-12 distinct colors with exact row counts

---

## Project Structure

```
Palette/
├── Movies/          # 257 original palette images (PNG)
├── Pattern/         # 257 pattern files (Markdown)
├── Script/          # Python scripts for pattern generation
├── Web/             # Web interface
│   ├── index.html   # Main app
│   ├── films_data.js # All film data
│   └── yarn-ball.png # Yarn ball texture
└── README.md
```

---

## Films Available

### Classics
12 Angry Men, 2001: A Space Odyssey, A Clockwork Orange, Apocalypse Now, Barry Lyndon, Blade Runner, Gone with the Wind, Manhattan, Taxi Driver, The Godfather, The Shining, The Wizard of Oz

### 80s-90s
Aliens, Back to the Future, Braveheart, Dirty Dancing, Fargo, Fight Club, Goodfellas, Grease, Heat, Jurassic Park, Pulp Fiction, Se7en, The Big Lebowski, The Matrix, The Shawshank Redemption, Titanic, Toy Story

### 2000s
Amélie, Avatar, Donnie Darko, Eternal Sunshine of the Spotless Mind, Finding Nemo, Gladiator, Her, Inception, Kill Bill, La La Land, Lost in Translation, Moonrise Kingdom, No Country for Old Men, Spirited Away, The Dark Knight, The Grand Budapest Hotel, The Lord of the Rings, There Will Be Blood, Wall-E

### Animation
Aladdin, Beauty and the Beast, Frozen, How to Train Your Dragon, Moana, Monsters Inc., Mulan, My Neighbor Totoro, Snow White, The Incredibles, The Lion King, The Little Mermaid, Up

### And 200+ more...

---

## Generate New Patterns

```bash
cd Script
source /path/to/venv/bin/activate

# Generate pattern from a palette image
python genera_pattern_v2.py ../Movies/film-name.png

# All patterns regenerated
for f in ../Movies/*.png; do python genera_pattern_v2.py "$f"; done
```

---

## Yarn Estimates

The app estimates yarn needed based on:

| Technique | Yarn per stitch |
|-----------|-----------------|
| Knitting  | ~1.3 cm |
| Crochet   | ~2.0 cm |

Standard ball: 50g = ~125 meters

---

## Credits

- Film palettes from [The Colors of Motion](https://thecolorsofmotion.com/)
- Built with Claude Code

---

*January 2026*
