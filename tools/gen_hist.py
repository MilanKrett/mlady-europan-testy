"""História: predsedovia Európskeho parlamentu (Historické archívy EP) a predsedovia Európskej komisie (oesterreich.gv.at).
Výstup: tools/gen/hist.json"""
import os, json, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "..", "zdroje-cache")
R = random.Random(77)
Q = []


def add(kat, n, text, ok, bad, v, src):
    bad = [b for b in dict.fromkeys(bad) if b != ok][:2]
    assert len(bad) == 2, text
    Q.append({"kat": kat, "n": n, "text": text, "ok": ok, "bad": bad, "v": v, "src": [list(s) for s in src]})


def lines(slug):
    return [l.strip() for l in open(os.path.join(CACHE, slug + ".txt"), encoding="utf-8").read().split("\n")]


def near(lst, i, k=3):
    """indexy susedov v čase (bez i), najbližšie prvé"""
    idx = [j for j in range(len(lst)) if j != i]
    idx.sort(key=lambda j: (abs(j - i), R.random()))
    return idx[:k]


# ---------------- predsedovia EP ----------------
SK = {  # meno v zdroji -> (slovenský tvar, žena?)
    "Emilio Colombo": ("Emilio Colombo", 0), "Simone Veil": ("Simone Veilová", 1), "Pieter Dankert": ("Piet Dankert", 0),
    "Pierre Pflimlin": ("Pierre Pflimlin", 0), "Lord Plumb": ("lord Henry Plumb", 0),
    "Enrique Barón Crespo": ("Enrique Barón Crespo", 0), "Egon A. Klepsch": ("Egon Klepsch", 0), "Klaus Hänsch": ("Klaus Hänsch", 0),
    "José María Gil-Robles Gil-Delgado": ("José María Gil-Robles", 0), "Nicole Fontaine": ("Nicole Fontaineová", 1),
    "Pat Cox": ("Pat Cox", 0), "Josep Borrell Fontelles": ("Josep Borrell", 0), "Hans-Gert Pöttering": ("Hans-Gert Pöttering", 0),
    "Jerzy Buzek": ("Jerzy Buzek", 0), "Martin Schulz": ("Martin Schulz", 0), "Antonio Tajani": ("Antonio Tajani", 0),
    "David Maria Sassoli": ("David Sassoli", 0), "Roberta Metsola": ("Roberta Metsolová", 1),
}
NAT = {  # pôvod podľa životopisu v Historických archívoch EP
    "Emilio Colombo": ("Taliansko", "eppres-emilio-colombo", "Emilio Colombo was born on the 11th of April 1920 in Potenza, Italy."),
    "Simone Veil": ("Francúzsko", "eppres-simone-veil", "Simone Veil was born on 13 July 1927 in Nice, Alpes-Maritimes, France."),
    "Pieter Dankert": ("Holandsko", "eppres-piet-dankert", "Pieter Dankert was a Dutch politician"),
    "Pierre Pflimlin": ("Francúzsko", "eppres-pierre-pflimlin", "Pierre Pflimlin was born on 5 February 1907 in Roubaix in the Nord department of France."),
    "Lord Plumb": ("Spojené kráľovstvo", "eppres-lord-plumb", "Charles Henry Plumb was born in Warwickshire, United Kingdom, on 27 March 1925."),
    "Enrique Barón Crespo": ("Španielsko", "eppres-enrique-baron-crespo", "Enrique Barón Crespo was born in Madrid, Spain, on the 27 March 1944."),
    "Nicole Fontaine": ("Francúzsko", "eppres-nicole-fontaine", "Nicole Fontaine was born in Normandy, France, on 16 January 1942."),
    "Pat Cox": ("Írsko", "eppres-pat-cox", "Pat Cox was born on 28th November 1952 in Dublin, Ireland."),
    "Josep Borrell Fontelles": ("Španielsko", "eppres-josep-borrell-fontelles", "Josep Borrell Fontelles is a Spanish national"),
    "Jerzy Buzek": ("Poľsko", "eppres-jerzy-buzek", "From 1997 to 2001, Buzek was Prime Minister of Poland."),
    "Martin Schulz": ("Nemecko", "eppres-martin-schulz", "Since 2017, he has been a member of the German Bundestag"),
    "Antonio Tajani": ("Taliansko", "eppres-antonio-tajani", "Antonio Tajani was born in Rome on 4 August 1953."),
    "David Maria Sassoli": ("Taliansko", "eppres-david-sassoli", "David Maria Sassoli was born in Florence on 30 May 1956."),
    "Roberta Metsola": ("Malta", "eppres-roberta-metsola", "Roberta Metsola was born on 18 January 1979 in St. Julians in Malta."),
}
COUNTRIES = ["Taliansko", "Francúzsko", "Holandsko", "Spojené kráľovstvo", "Španielsko", "Írsko", "Poľsko", "Nemecko", "Malta",
             "Belgicko", "Luxembursko", "Portugalsko", "Grécko", "Rakúsko"]
EASY = {"Simone Veil", "Roberta Metsola", "Martin Schulz", "David Maria Sassoli", "Antonio Tajani"}

L = lines("ep-hist-presidents")
EP = []
for i, l in enumerate(L[:-1]):
    m = re.match(r"President (from (\d{4})-(\d{4})|since (\d{4}))$", L[i + 1])
    if m and l in SK:
        span = f"{m.group(2)} – {m.group(3)}" if m.group(2) else f"od {m.group(4)}"
        EP.append((l, SK[l][0], SK[l][1], span, f"{l} {L[i + 1]}"))
assert len(EP) == 18, len(EP)

for i, (raw, nm, fem, span, ev) in enumerate(EP):
    n = 2 if raw in EASY else 3
    src = [("ep-hist-presidents", ev)]
    who = "predsedníčkou" if fem else "predsedom"
    if span.startswith("od"):
        pass  # otázka o súčasnej predsedníčke je už v ins-02
    else:
      if raw != "Nicole Fontaine":  # je už v his-02
        add("his", n, f"Kto bol predsedom alebo predsedníčkou Európskeho parlamentu v rokoch {span}?", nm,
            [EP[j][1] for j in near(EP, i)], f"{nm} bol{'a' if fem else ''} {who} Európskeho parlamentu v rokoch {span}.", src)
      if True:
        add("his", 3, f"V ktorých rokoch bol{'a' if fem else ''} {nm} {who} Európskeho parlamentu?", span,
            [EP[j][3] for j in near(EP, i) if not EP[j][3].startswith("od")],
            f"{nm} viedl{'a' if fem else ''} Európsky parlament v rokoch {span}.", src)
    if raw in NAT:
        c, sl, nev = NAT[raw]
        add("his", n, f"Z ktorého štátu pochádza{'' if span.startswith('od') else 'l'}{'a' if fem and not span.startswith('od') else ''} "
            f"{nm}, {'predsedníčka' if fem else 'predseda'} Európskeho parlamentu ({span})?",
            c, R.sample([x for x in COUNTRIES if x != c], 2),
            f"{nm} pochádza{'' if span.startswith('od') else ('la' if fem else 'l')} z krajiny: {c}.", src + [(sl, nev)])
    if i > 0:
        prev = EP[i - 1]
        others = [EP[j][1] for j in near(EP, i, 5) if j != i - 1]
        add("his", 3, f"Kto viedol Európsky parlament bezprostredne pred tým, ako sa {'jeho predsedníčkou stala' if fem else 'jeho predsedom stal'} "
            f"{nm} ({span})?", prev[1], others,
            f"Pred {nm} ({span}) viedol/viedla EP {prev[1]} ({prev[3]}).", [("ep-hist-presidents", prev[4])] + src)

# ---------------- predsedovia Európskej komisie ----------------
txt = re.sub(r"\s+", " ", open(os.path.join(CACHE, "at-kommissionen.txt"), encoding="utf-8").read())
DE = {"Belgien": "Belgicko", "Italien": "Taliansko", "Niederlande": "Holandsko", "Frankreich": "Francúzsko",
      "Großbritannien": "Spojené kráľovstvo", "Luxemburg": "Luxembursko", "Spanien": "Španielsko", "Portugal": "Portugalsko",
      "Deutschland": "Nemecko"}
NM = {"Jean Rey": "Jean Rey", "Franco-Maria Malfatti": "Franco Maria Malfatti", "Sicco Leendert Mansholt": "Sicco Mansholt",
      "François-Xavier Ortoli": "François-Xavier Ortoli", "Roy Jenkins": "Roy Jenkins", "Gaston Thorn": "Gaston Thorn",
      "Jacques Delors": "Jacques Delors", "Jacques Santer": "Jacques Santer", "Manuel Marín": "Manuel Marín",
      "Romano Prodi": "Romano Prodi", "José Manuel Durão Barroso": "José Manuel Barroso", "Jean-Claude Juncker": "Jean-Claude Juncker",
      "Ursula von der Leyen": "Ursula von der Leyenová"}
rows = re.findall(r"(\d+) \| (\d{4} - \d{4}|\d{4}|seit \d{4}) \| ([^|()]+?) \(([^)]+)\)", txt)
assert len(rows) == 17, rows
COM = []  # (meno raw, sk, krajina, od, do, [evidence])
for num, span, name, land in rows:
    base = re.sub(r" (I|II|III)$", "", name.strip())
    ev = f"{num} | {span} | {name} ({land})"
    a = int(span[-4:]) if span.startswith("seit") else int(span[:4])
    b = None if span.startswith("seit") else int(span[-4:])
    if COM and COM[-1][0] == base:
        COM[-1][4] = b
        COM[-1][5].append(ev)
        continue
    COM.append([base, NM[base], DE[land], a, b, [ev]])
assert len(COM) == 13, [c[0] for c in COM]
EV17 = ("at-kommissionen", "Seit 1967 wurden innerhalb der Europäischen Union (EU) und ihrer Vorgängerin, der Europäischen Gemeinschaft (EG), insgesamt 17 Kommissionen eingerichtet.")


def cspan(c):
    return f"od {c[3]}" if c[4] is None else f"{c[3]} – {c[4]}"


CM = [c for c in COM if c[0] != "Manuel Marín"]  # Marín viedol Komisiu len dočasne v roku 1999
CEASY = {"Jacques Delors", "Ursula von der Leyen", "Jean-Claude Juncker"}
for i, c in enumerate(CM):
    raw, nm, land, a, b, evs = c
    src = [("at-kommissionen", e) for e in evs]
    fem = nm.endswith("ová")
    n = 2 if raw in CEASY else 3
    if b is not None:
        add("his", n, f"Kto bol predsedom Európskej komisie v rokoch {a} – {b}?", nm, [CM[j][1] for j in near(CM, i)],
            f"{nm} ({land}) viedol Komisiu v rokoch {a} – {b}.", src)
        add("his", 3, f"V ktorých rokoch viedol Európsku komisiu {nm}?", cspan(c),
            [cspan(CM[j]) for j in near(CM, i) if CM[j][4] is not None],
            f"{nm} bol predsedom Komisie v rokoch {a} – {b}.", src)
    add("his", 2 if raw in CEASY else 3, f"Z ktorého štátu pochádza{'' if b is None else 'l'}{'a' if fem and b is not None else ''} "
        f"{'predsedníčka' if fem else 'predseda'} Európskej komisie {nm}?", land,
        R.sample([x for x in COUNTRIES if x != land], 2), f"{nm} pochádza{'' if b is None else ('la' if fem else 'l')} z krajiny: {land}.", src)
    others = [CM[j] for j in near(CM, i, 8) if CM[j][2] != land][:2]
    add("his", 3, f"Ktorý z týchto predsedov Európskej komisie pochádzal z krajiny {land}?" if b is not None
        else f"Kto z týchto ľudí vedie Európsku komisiu a pochádza z krajiny {land}?", nm, [o[1] for o in others],
        f"{nm} ({cspan(c)}) pochádza{'' if b is None else 'l'} z krajiny {land}; " + ", ".join(f"{o[1]} z krajiny {o[2]}" for o in others) + ".",
        src + [("at-kommissionen", o[5][0]) for o in others])
    if i > 0 and raw != "Romano Prodi":
        prev = CM[i - 1]
        add("his", 3, f"Kto viedol Európsku komisiu bezprostredne pred tým, ako ju {'prevzala' if fem else 'prevzal'} {nm}?", prev[1],
            [CM[j][1] for j in near(CM, i, 5) if j != i - 1],
            f"Pred {nm} viedol Komisiu {prev[1]} ({cspan(prev)}).", [("at-kommissionen", prev[5][-1])] + src)

dl = next(c for c in COM if c[0] == "Jacques Delors")
add("his", 3, "Koľko po sebe nasledujúcich komisií viedol Jacques Delors?", "tri (1985 – 1995)", ["dve (1985 – 1993)", "štyri (1981 – 1997)"],
    "Jacques Delors viedol tri komisie: Delors I (1985 – 1989), Delors II (1989 – 1993) a Delors III (1993 – 1995).",
    [("at-kommissionen", e) for e in dl[5]])
add("his", 3, "Koľko európskych komisií bolo zriadených od roku 1967 (vrátane súčasnej)?", "17", ["7", "27"],
    "Od roku 1967 bolo v EÚ a jej predchodkyni, Európskom spoločenstve, zriadených celkovo 17 komisií.", [EV17])
lux = [c for c in COM if c[2] == "Luxembursko"]
add("his", 3, "Koľko predsedov Európskej komisie (od roku 1967) pochádzalo z Luxemburska?", "traja – Thorn, Santer a Juncker",
    ["jeden – Juncker", "žiadny"], "Z Luxemburska pochádzali Gaston Thorn, Jacques Santer a Jean-Claude Juncker.",
    [("at-kommissionen", c[5][0]) for c in lux])

json.dump(Q, open(os.path.join(HERE, "gen", "hist.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(Q), "otázok ->", os.path.join("gen", "hist.json"))
