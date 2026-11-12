"""Hľadá podobné otázky (rovnaký fakt položený dvakrát) naprieč všetkými súbormi.
Porovnáva množinu významových slov textu + správnu odpoveď."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qparse import load_all, norm

STOP = set("a aj ako ale alebo do na v vo z zo s so k ku o od po pri pre za ktorý ktorá ktoré ktorého ktorej ktorú ktorým koľko kedy kde kto čo je sa bol bola bolo boli sú má mal mala v roku roku rok eú eu".split())

def words(s):
    return {w for w in re.findall(r"\w+", norm(s)) if w not in STOP and len(w) > 2}

qs, _ = load_all()
items = []
for q in qs:
    items.append((q, words(q["text"]), norm(q["ok"])))

thr = float(sys.argv[1]) if len(sys.argv) > 1 else 0.6
found = 0
for i in range(len(items)):
    qi, wi, oi = items[i]
    for j in range(i + 1, len(items)):
        qj, wj, oj = items[j]
        if qi.get("file") == qj.get("file") and qi.get("file","").endswith(".json"):
            continue
        if oi != oj:
            continue
        if not wi or not wj:
            continue
        jac = len(wi & wj) / len(wi | wj)
        if jac >= thr:
            found += 1
            print(f"{jac:.2f} | {qi.get('file','?')}: {qi['text'][:90]}\n     | {qj.get('file','?')}: {qj['text'][:90]}\n     = {qi['ok'][:60]}")
print("Podobných párov:", found)
