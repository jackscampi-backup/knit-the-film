# Palette Cinematografiche in Tessuto

Crea sciarpe, coperte, pad mouse e altri oggetti tessili che rappresentano visivamente i colori di un film.

---

## L'idea

Ogni film ha una "firma cromatica" - i colori dominanti che appaiono nel corso della pellicola. The Matrix è verde, Blade Runner è ciano/arancio, Grand Budapest Hotel è rosa/rosso.

Le immagini nella cartella `Movies/` mostrano questa firma: ogni riga orizzontale è un fotogramma del film, compresso in una striscia di colore. Dall'alto al basso = dall'inizio alla fine del film.

**Questo progetto trasforma quelle strisce in istruzioni per lavori tessili**: maglia, uncinetto, tessitura. Il risultato è un oggetto che "racconta" visivamente il film attraverso i suoi colori.

---

## Pattern pronti (100 film)

Nella cartella `Pattern/` ci sono già 100 pattern pronti dei film più iconici:

- **Classici**: Godfather, 2001, Blade Runner, Shining, Taxi Driver, Apocalypse Now
- **Anni 90**: Pulp Fiction, Matrix, Fight Club, Fargo, Shawshank Redemption
- **Moderni**: Interstellar, Mad Max, La La Land, Joker, Arrival
- **Animazione**: Lion King, Spirited Away, Totoro, Wall-E, Finding Nemo
- **Wes Anderson**: Grand Budapest Hotel, Moonrise Kingdom, Royal Tenenbaums

Ogni pattern contiene:
- Lista colori **in ordine** (dall'inizio alla fine del film)
- Codici **HEX** (per comprare il filato giusto)
- **Proporzioni %** (quanto spazio occupa ogni colore)

---

## Come usare un pattern

Apri un file `.md` dalla cartella `Pattern/`, ad esempio `the-matrix-1999.md`:

```
| # | Colore | HEX | % |
|:-:|--------|:---:|:-:|
| 1 | Verde Scuro | #1f2f15 | 10.5% |
| 2 | Verde | #7ab473 | 5.8% |
| 3 | Verde Scuro | #21310d | 11.0% |
...
```

Le percentuali indicano la proporzione di ogni colore. Tu decidi le dimensioni totali:

| Progetto | Righe totali | Colore al 10% = |
|----------|--------------|-----------------|
| Pad mouse | 50 righe | 5 righe |
| Sciarpa | 150 righe | 15 righe |
| Coperta | 400 righe | 40 righe |

**Esempio**: vuoi fare una sciarpa di Matrix lunga 150 righe.
- Colore 1 (Verde Scuro, 10.5%) → 16 righe
- Colore 2 (Verde, 5.8%) → 9 righe
- Colore 3 (Verde Scuro, 11%) → 17 righe
- ...e così via

---

## Generare nuovi pattern

Se vuoi un film non incluso nei 100, puoi generarlo:

```bash
cd /Users/ct011099/Documents/AI_Terminal/TOOLKIT/Palette/Script
source ../../.venv/bin/activate

python genera_pattern.py ../Movies/nome-film.png
python genera_pattern.py ../Movies/nome-film.png --colori 10  # meno colori
```

---

## Struttura cartelle

```
Palette/
├── Movies/     # 257 palette originali (PNG)
├── Pattern/    # 100 pattern pronti (MD)
├── Script/     # genera_pattern.py
└── README.md
```

---

## Fonte

Le palette originali vengono da [The Colors of Motion](https://www.thecolorsofmotion.com/), un progetto che analizza i colori di ogni fotogramma dei film.

---

*Gennaio 2026*
