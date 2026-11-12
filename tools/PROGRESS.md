# Stav práce – Mladý Európan testy (12. 11. 2026)

HOTOVO a online: https://milankrett.github.io/mlady-europan-testy/
(repo MilanKrett/mlady-europan-testy, GitHub Pages z vetvy main, koreň)

- 3068 overených otázok (z toho 401 s obrázkom), 1000 pevných testov × 40 otázok, 30 min, 100 bodov, úspech od 90.
- Kontrola: `cd tools && python -I -X utf8 qparse.py` (0 chýb); zostavenie: `qparse.py --build` → data/otazky.json, data/testy.json.
- Obrázkové otázky: `gen_obr.py` → gen/obr.json + img/kredity.json (licencie zobrazené na stránke „Ako to funguje“).
- Zdrojové stránky (cache) sú mimo repa v Desktop\Mlady Europan\zdroje-cache.

Úprava a nasadenie: zmeniť otazky/*.txt alebo tools/gen_*.py → spustiť generátor → `qparse.py --build` → `git commit` a `git push` (Pages sa obnoví samy).
Pozor: zmena textu otázky mení jej id aj zloženie testov; staré výsledky v prehliadači potom ukazujú na iné otázky.
Pri zmene app.js/style.css zvýšiť verziu cache v sw.js (V = "me-testy-vN").
