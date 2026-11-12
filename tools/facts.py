"""Vypíše z cache stručné vety s faktami (čísla, roky, sídla) pre písanie otázok.
použitie: python facts.py slug [slug ...] [--max 3000] [--all]"""
import os, re, sys

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "zdroje-cache")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
MAX = 3000
ALL = "--all" in sys.argv
for a in sys.argv[1:]:
    if a.startswith("--max="):
        MAX = int(a[6:])

USED = {}
if "--unused" in sys.argv:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from qparse import load_all, norm
    for q in load_all()[0]:
        for sl, ev in q["src"]:
            for part in ev.split("..."):
                part = norm(part)
                if len(part) > 15:
                    USED.setdefault(sl, []).append(part)

for slug in args:
    t = open(os.path.join(CACHE, slug + ".txt"), encoding="utf-8").read()
    lines = t.split("\n")
    s = 0
    for i, l in enumerate(lines):
        if "stiahnuť dokument" in l:
            s = i + 1
            break
    e = len(lines)
    for i in range(s, len(lines)):
        if re.match(r"^\s*\d\d-\d{4}\s*$", lines[i]) or lines[i].startswith("Tento informačný list pripravil"):
            e = i
            break
    body = " ".join(x.strip() for x in lines[s:e] if x.strip())
    sents = re.split(r"(?<=[.;:])\s+(?=[A-ZÁČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ„])", body)
    out, n = [], 0
    for x in sents:
        x = x.strip()
        if len(x) < 25:
            continue
        if not ALL and (re.match(r"(Právny základ|Článok|Články|Nariadeni|Smernic|Rozhodnuti|Protokol|Hlava|Zmluva o)", x) or re.search(r"č\. ?\d+/\d+|\(EÚ\) \d{4}/\d+|Ú\. v\.", x)):
            continue
        if not ALL and not re.search(r"\d|sídl|založ|predsed|zriaden|nazýva|známy ako|tzv\.", x):
            continue
        if USED and any(u in norm(x) for u in USED.get(slug, [])):
            continue
        x = x if len(x) <= 330 else x[:330] + "…"
        n += len(x)
        if n > MAX:
            break
        out.append(x)
    print(f"##### {slug}")
    for x in out:
        print("-", x)
