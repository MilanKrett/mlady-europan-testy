# Mladý Európan – cvičné testy

Cvičné testy na súťaž **Mladý Európan** vo formáte testu z autoškoly:

- 40 otázok, 30 minút, na každú otázku 3 možnosti (práve jedna správna),
- 100 bodov spolu, test je úspešný od 90 bodov,
- 1000 pevných testov z viac ako 3000 overených otázok (vrátane otázok s fotografiami predstaviteľov inštitúcií, logami inštitúcií, mapami a euromincami),
- po odovzdaní prehľad nesprávnych odpovedí s vysvetlením a odkazom na oficiálny zdroj.

Aplikácia je statická (HTML + CSS + JavaScript, bez knižníc), výsledky sa ukladajú v prehliadači (localStorage) a funguje aj offline.

## Štruktúra

- `index.html`, `style.css`, `app.js` – aplikácia
- `data/otazky.json` – otázky, `data/testy.json` – 1000 testov (indexy otázok)
- `img/` – obrázky k otázkam, licencie v `img/kredity.json`
- `otazky/*.txt` – zdrojové texty otázok s dôkazmi zo zdrojov, `tools/` – kontrola a zostavenie (`python tools/qparse.py --build`)

Neoficiálna pomôcka na precvičovanie, nie materiál organizátora súťaže. Stav faktov: november 2026.
