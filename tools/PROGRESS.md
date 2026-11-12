# Stav práce – Mladý Európan testy (12. 11. 2026)

Overené otázky: 620 / 3000 (`python -I -X utf8 qparse.py`, 0 chýb)
- gen_staty.py → gen/staty.json (301 sta)
- gen_eu.py → gen/eu.json (187: komisári, predsedníctva, pristúpenia)
- gen_agentury.py → gen/agentury.json (132: sídla, úlohy, roky agentúr; ELA → svk)

Ďalej (v tomto poradí):
1. gen_ecoc.py z zdroje-cache/ecoc-node-335.txt (zoznam EHMK 1985–2031, Trenčín 2026 → svk/akt) → kul
2. Sacharovova cena (ep-sakharov-laureates), Európske roky (eu-symbol-european-years), symboly → kul/sym
3. Ručné otázky otazky/*.txt: his (eu-history-*, eu-pioneer-*, ep-fs-1..5, 11, 79), ins (ep-fs-6..29, politiky), svk, med (disinfo, dsa, ai-act, gdpr, edmo), fin (ecb-inflation, ecb-banknotes, nbs-euromince – prepočty kurzom 30,1260)
4. UNESCO pamiatky (sta + obr), obrázky z Wikimedia Commons (komisári, predsedovia inštitúcií, priekopníci, logá, vlajky) + stránka licencií
5. Aplikácia (index.html, app.js, style.css; 1000 testov, 30 min, 90/100, prehľad chýb), overenie v prehliadači
6. GitHub Pages (MilanKrett/mlady-europan-testy), potom notifikácia + e-mail s linkom
