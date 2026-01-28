# CLAUDE.md - Palette Cinematografiche

Questo progetto trasforma le palette di colori dei film in pattern per lavori tessili (maglia, uncinetto, tessitura).

---

## Struttura

```
Palette/
├── Movies/     # 257 palette originali (PNG da The Colors of Motion)
├── Pattern/    # 100 pattern pronti (MD con colori e proporzioni)
├── Script/     # genera_pattern.py
└── README.md   # Documentazione progetto
```

---

## Cosa c'è

- **257 palette** di film scaricate da thecolorsofmotion.com
- **100 pattern** già generati per i film più iconici
- **Script Python** per generare nuovi pattern

---

## Script disponibile

```bash
cd Script
source /Users/ct011099/Documents/AI_Terminal/TOOLKIT/.venv/bin/activate

# Genera pattern da una palette
python genera_pattern.py ../Movies/nome-film.png

# Con meno colori (default: 15)
python genera_pattern.py ../Movies/nome-film.png --colori 10
```

**Output**: file `.md` in `Pattern/` con:
- Lista colori in ordine (dall'inizio alla fine del film)
- Codici HEX
- Proporzioni percentuali

---

## Come funziona

1. Le immagini in `Movies/` sono "firme cromatiche" dei film
2. Ogni riga orizzontale = un fotogramma compresso in una striscia di colore
3. Dall'alto al basso = dall'inizio alla fine del film
4. Lo script estrae i colori dominanti e calcola le proporzioni
5. L'utente usa le proporzioni per creare oggetti tessili (sciarpe, coperte, etc.)

---

## Task tipici

### Generare pattern per un film specifico
```bash
python Script/genera_pattern.py Movies/nome-film.png
```

### Generare pattern per più film
```bash
for film in film1 film2 film3; do
  python Script/genera_pattern.py "Movies/${film}.png"
done
```

### Vedere quali film sono disponibili
```bash
ls Movies/ | sed 's/.png$//'
```

### Vedere quali pattern sono già pronti
```bash
ls Pattern/ | sed 's/.md$//'
```

---

## Note

- Il venv del TOOLKIT contiene tutte le dipendenze (PIL)
- I pattern usano 12-15 colori di default (lavorabile a mano)
- Le proporzioni sommano sempre a 100%
- L'utente decide le dimensioni totali, le proporzioni restano uguali
