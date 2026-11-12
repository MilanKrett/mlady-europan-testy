"""Generuje otázky o 27 členských štátoch z profilov krajín na europa.eu (zdroje-cache/eu-country-*.txt)
a z mapy eurozóny ECB. Výstup: tools/gen/staty.json. Každá otázka nesie doslovný úryvok zo zdroja."""
import os, re, json, random, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(os.path.dirname(os.path.dirname(HERE)), "zdroje-cache")
OUT = os.path.join(HERE, "gen")
R = random.Random(2026)

# kód: (nominatív, genitív, lokál s predložkou, región, „pasca“ – mesto, ktoré nie je hlavné)
C = {
    "austria": ("Rakúsko", "Rakúska", "v Rakúsku", "stred", "Salzburg"),
    "belgium": ("Belgicko", "Belgicka", "v Belgicku", "zapad", "Antverpy"),
    "bulgaria": ("Bulharsko", "Bulharska", "v Bulharsku", "juhovychod", "Plovdiv"),
    "croatia": ("Chorvátsko", "Chorvátska", "v Chorvátsku", "juh", "Split"),
    "cyprus": ("Cyprus", "Cypru", "na Cypre", "juh", "Limassol"),
    "czechia": ("Česko", "Česka", "v Česku", "stred", "Brno"),
    "denmark": ("Dánsko", "Dánska", "v Dánsku", "sever", "Aarhus"),
    "estonia": ("Estónsko", "Estónska", "v Estónsku", "sever", "Tartu"),
    "finland": ("Fínsko", "Fínska", "vo Fínsku", "sever", "Turku"),
    "france": ("Francúzsko", "Francúzska", "vo Francúzsku", "zapad", "Lyon"),
    "germany": ("Nemecko", "Nemecka", "v Nemecku", "stred", "Bonn"),
    "greece": ("Grécko", "Grécka", "v Grécku", "juhovychod", "Solún"),
    "hungary": ("Maďarsko", "Maďarska", "v Maďarsku", "stred", "Debrecín"),
    "ireland": ("Írsko", "Írska", "v Írsku", "zapad", "Cork"),
    "italy": ("Taliansko", "Talianska", "v Taliansku", "juh", "Miláno"),
    "latvia": ("Lotyšsko", "Lotyšska", "v Lotyšsku", "sever", "Daugavpils"),
    "lithuania": ("Litva", "Litvy", "v Litve", "sever", "Kaunas"),
    "luxembourg": ("Luxembursko", "Luxemburska", "v Luxembursku", "zapad", "Esch-sur-Alzette"),
    "malta": ("Malta", "Malty", "na Malte", "juh", "Mdina"),
    "netherlands": ("Holandsko", "Holandska", "v Holandsku", "zapad", "Haag"),
    "poland": ("Poľsko", "Poľska", "v Poľsku", "stred", "Krakov"),
    "portugal": ("Portugalsko", "Portugalska", "v Portugalsku", "juh", "Porto"),
    "romania": ("Rumunsko", "Rumunska", "v Rumunsku", "juhovychod", "Kluž-Napoka"),
    "slovakia": ("Slovensko", "Slovenska", "na Slovensku", "stred", "Košice"),
    "slovenia": ("Slovinsko", "Slovinska", "v Slovinsku", "stred", "Maribor"),
    "spain": ("Španielsko", "Španielska", "v Španielsku", "juh", "Barcelona"),
    "sweden": ("Švédsko", "Švédska", "vo Švédsku", "sever", "Göteborg"),
}
NUMW = {"šesť": 6, "sedem": 7, "osem": 8, "deväť": 9, "päť": 5, "desať": 10}
CAP_FIX = {"luxembourg": "Luxemburg"}  # stránka uvádza „Luxembursko“ – mesto sa volá Luxemburg
MONARCHIE = {"belgium", "denmark", "luxembourg", "netherlands", "spain", "sweden"}


def txt(slug):
    t = open(os.path.join(CACHE, slug + ".txt"), encoding="utf-8").read()
    return re.sub(r"[  -​  　]", " ", t)


def line_of(t, pat):
    m = re.search(pat, t)
    if not m:
        return None, None
    # celý riadok ako dôkaz
    s = t.rfind("\n", 0, m.start()) + 1
    e = t.find("\n", m.end())
    return m, t[s:e if e > 0 else None].strip()


D = {}
for code in C:
    slug = "eu-country-" + code
    t = txt(slug)
    d = {"slug": slug}
    m, l = line_of(t, r"Hlavné mesto: ([^\n;]+)")
    d["cap"], d["cap_ev"] = CAP_FIX.get(code, m.group(1).strip()), l
    m, l = line_of(t, r"Úradn\w+ jazyk[^:\n]*EÚ: ([^\n]+)")
    d["lang"], d["lang_ev"] = [x.strip() for x in m.group(1).split(",")], l
    m, l = line_of(t, r"Členský štát EÚ: od ([^\n]+)")
    d["join"], d["join_ev"] = m.group(1).strip(), l
    d["join_y"] = int(re.search(r"(\d{4})", d["join"]).group(1))
    m, l = line_of(t, r"Mena: ([^\n]+)")
    d["cur"], d["cur_ev"] = m.group(1).strip(), l
    m, l = line_of(t, r"Schengenský priestor: ([^\n]+)")
    d["sch"], d["sch_ev"] = m.group(1).strip(), l
    m, l = line_of(t, r"Zemepisná rozloha: ([\d  ]+) km")
    d["area"], d["area_ev"] = int(re.sub(r"\D", "", m.group(1))), l
    m, l = line_of(t, r"Počet obyvateľov: ([\d  ]+)")
    d["pop"], d["pop_ev"] = int(re.sub(r"\D", "", m.group(1))), l
    m, l = line_of(t, r"má v Európskom parlamente (\S+) zástupcov")
    v = m.group(1)
    d["mep"], d["mep_ev"] = (int(v) if v.isdigit() else NUMW[v]), m.group(0)
    m, l = line_of(t, r"Politický systém\n([^\n]+)")
    d["pol"] = m.group(1).split(".")[0] + "." if m else None
    m2 = re.search(r"Dátumy predsedníctiev[^\n]*\n([^\n]+)", t)
    d["pres"] = [x.strip() for x in m2.group(1).split("|") if x.strip()] if m2 else []
    d["pres_ev"] = m2.group(1).strip() if m2 else None
    m = re.search(r"(\w+ (?:komisárom|komisárkou)) v Európskej (?:komisii|únii) je ([^,]+?),? (ktor\w+ je[^.\n]+)", t)
    if m:
        d["kom"], d["kom_ev"] = m.group(2).strip(), m.group(0).strip()
    D[code] = d

# eurozóna z mapy ECB
ecb = re.sub(r"\s+", " ", txt("ecb-euro-map"))
for code, d in D.items():
    m = re.search(re.escape(C[code][0] if code != "czechia" else "Česká republika") +
                  r" Členský štát EÚ (používajúci|nepoužívajúci) euro (?:Zakladajúci člen EÚ v roku \d{4}|Členom EÚ od roku \d{4})(?: Euro od roku (\d{4}))?", ecb)
    if m:
        d["euro"] = m.group(1) == "používajúci"
        d["euro_y"] = int(m.group(2)) if m.group(2) else None
        d["euro_ev"] = m.group(0)

Q = []


def add(kat, n, text, ok, bad, v, src):
    bad = [b for b in bad if b != ok][:2]
    assert len(bad) == 2, (text, ok, bad)
    Q.append({"kat": kat, "n": n, "text": text, "ok": str(ok), "bad": [str(b) for b in bad], "v": v,
              "src": [list(s) for s in src]})


codes = list(C)
REG = {}
for c in codes:
    REG.setdefault(C[c][3], []).append(c)


def same_region(c, k=2, exclude=()):
    pool = [x for x in REG[C[c][3]] if x != c and x not in exclude]
    if len(pool) < k:
        pool += [x for x in codes if x != c and x not in pool and x not in exclude]
    return R.sample(pool, k)


# 1) hlavné mestá
HARD_CAP = {"netherlands", "slovenia", "estonia", "latvia", "lithuania", "malta", "cyprus", "luxembourg", "bulgaria", "romania"}
for c in codes:
    d = D[c]
    nom = C[c][0]
    o = same_region(c, 1)
    bad = [C[c][4], D[o[0]]["cap"]]
    n = 2 if c in HARD_CAP else 1
    extra = ""
    if c == "netherlands":
        extra = " Parlament a vláda však sídlia v Haagu."
    if c == "luxembourg":
        extra = " Hlavné mesto má rovnaké meno ako krajina."
    add("sta", n, f"Ktoré mesto je hlavným mestom krajiny {nom}?", d["cap"], bad,
        f"Hlavným mestom krajiny {nom} je {d['cap']}.{extra}", [(d["slug"], d["cap_ev"])])
    o2 = same_region(c, 2)
    add("sta", n, f"Ktorej krajiny je {d['cap']} hlavným mestom?", nom, [C[x][0] for x in o2],
        f"{d['cap']} je hlavné mesto krajiny {nom}.{extra}", [(d["slug"], d["cap_ev"])])

# 2) jazyky
ALL_LANG = sorted({l for d in D.values() for l in d["lang"]})
for c in codes:
    d = D[c]
    nom = C[c][0]
    others = [l for l in ALL_LANG if l not in d["lang"]]
    # ber jazyky blízkych krajín ako nesprávne
    near = [l for x in REG[C[c][3]] if x != c for l in D[x]["lang"] if l not in d["lang"]]
    near = list(dict.fromkeys(near)) or others
    bad = R.sample(near, 2) if len(near) >= 2 else R.sample(others, 2)
    ok = d["lang"][0] if len(d["lang"]) == 1 else R.choice(d["lang"])
    if len(d["lang"]) == 1:
        add("sta", 1 if c not in ("estonia", "latvia", "lithuania", "malta") else 2,
            f"Ktorý jazyk je úradným jazykom EÚ v krajine {nom}?", ok, bad,
            f"Úradným jazykom EÚ {C[c][2]} je {ok}.", [(d["slug"], d["lang_ev"])])
    else:
        add("sta", 2, f"Ktorý z týchto jazykov je jedným z úradných jazykov EÚ v krajine {nom}?", ok, bad,
            f"Úradné jazyky EÚ {C[c][2]}: {', '.join(d['lang'])}.", [(d["slug"], d["lang_ev"])])
# opačne: v ktorej krajine je jazyk úradný
for lang in ALL_LANG:
    has = [c for c in codes if lang in D[c]["lang"]]
    for c in has:
        cand = [x for x in codes if lang not in D[x]["lang"]]
        near = [x for x in REG[C[c][3]] if x in cand] or cand
        bad = R.sample(near, 2) if len(near) >= 2 else R.sample(cand, 2)
        n = 1 if len(has) == 1 else 3
        txtq = f"V ktorej z týchto krajín je {lang} úradným jazykom EÚ?"
        if len(has) > 1:
            txtq = f"V ktorej z týchto krajín je {lang} jedným z úradných jazykov EÚ?"
        if len(has) > 1 and c != has[0]:
            txtq = txtq.replace("V ktorej z týchto krajín", "V ktorej z uvedených krajín")
        if len(has) > 2 and has.index(c) >= 2:
            txtq = txtq.replace("úradných jazykov EÚ?", "úradných jazykov Európskej únie?")
        add("sta", n, txtq, C[c][0], [C[x][0] for x in bad],
            f"{lang[0].upper() + lang[1:]} je úradným jazykom EÚ v týchto krajinách: {', '.join(C[x][0] for x in has)}.",
            [(D[c]["slug"], D[c]["lang_ev"])])

# 3) euro
EURO = [c for c in codes if D[c].get("euro")]
NOEURO = [c for c in codes if c not in EURO]
EYEARS = sorted({D[c]["euro_y"] for c in EURO})
for c in EURO:
    d = D[c]
    y = d["euro_y"]
    bad = R.sample([x for x in EYEARS + [2004, 2010, 2020] if x != y and abs(x - y) <= 12] or [x for x in EYEARS if x != y], 2)
    n = 2 if y in (1999,) else 3
    if c in ("bulgaria", "croatia", "slovakia"):
        n = 2
    add("sta", n, f"Od ktorého roku používa {C[c][0]} euro?", y, bad,
        f"{C[c][0]} používa euro od roku {y}" + (" (v hotovosti od roku 2002)." if y <= 2001 else "."),
        [("ecb-euro-map", d["euro_ev"])])
CURR = {"czechia": "česká koruna", "denmark": "dánska koruna", "hungary": "maďarský forint", "poland": "poľský zlotý",
        "romania": "rumunský lei", "sweden": "švédska koruna"}
for c in NOEURO:
    d = D[c]
    bad = R.sample([v for k, v in CURR.items() if k != c], 2)
    add("sta", 1 if c in ("czechia", "hungary", "poland") else 2, f"Akou menou sa platí v krajine {C[c][0]}?", CURR[c], bad,
        f"{C[c][0]} zatiaľ nepoužíva euro, platí sa tam menou {CURR[c]}.", [(d["slug"], d["cur_ev"])])
    add("sta", 2, f"Ktorej krajiny EÚ je menou {CURR[c]}?", C[c][0], [C[x][0] for x in R.sample([x for x in NOEURO if x != c], 2)],
        f"{CURR[c][0].upper() + CURR[c][1:]} je menou krajiny {C[c][0]}.", [(d["slug"], d["cur_ev"])])
# ktorá krajina nemá euro (1 bez eura + 2 s eurom)
for i, c in enumerate(NOEURO * 3):
    e2 = R.sample(EURO, 2)
    variant = i // len(NOEURO)
    q = ["Ktorá z týchto krajín EÚ nepoužíva euro?", "Ktorá z uvedených krajín nie je členom eurozóny?",
         "Ktorá z týchto krajín ešte neprijala euro?"][variant]
    add("sta", 2, q, C[c][0], [C[x][0] for x in e2],
        f"{C[c][0]} nepoužíva euro. {C[e2[0]][0]} a {C[e2[1]][0]} sú v eurozóne.",
        [(D[c]["slug"], D[c]["cur_ev"]), ("ecb-euro-map", D[e2[0]]["euro_ev"]), ("ecb-euro-map", D[e2[1]]["euro_ev"])])
for i, c in enumerate(R.sample(EURO, 12)):
    n2 = R.sample(NOEURO, 2)
    add("sta", 2, ["Ktorá z týchto krajín platí eurom?", "Ktorá z uvedených krajín je členom eurozóny?"][i % 2] + ("" if i < 6 else " "),
        C[c][0], [C[x][0] for x in n2], f"{C[c][0]} je v eurozóne, {C[n2[0]][0]} a {C[n2[1]][0]} nie.",
        [("ecb-euro-map", D[c]["euro_ev"]), (D[n2[0]]["slug"], D[n2[0]]["cur_ev"]), (D[n2[1]]["slug"], D[n2[1]]["cur_ev"])])

# 4) Schengen
SCH = {c: D[c] for c in codes if D[c]["sch"].startswith("člen od")}
for c, d in SCH.items():
    date = d["sch"].replace("člen od ", "").strip()
    y = int(date[-4:])
    years = sorted({int(x["sch"][-4:]) for x in SCH.values()})
    bad = R.sample([x for x in years if x != y], 2)
    add("sta", 3 if c not in ("slovakia", "bulgaria", "romania", "croatia") else 2,
        f"V ktorom roku sa {C[c][0]} stalo plnohodnotným členom schengenského priestoru?".replace("Litva sa stalo", "Litva sa stala").replace("Malta sa stalo", "Malta sa stala"),
        y, bad, f"{C[c][0]} je členom schengenského priestoru od {date}.", [(d["slug"], d["sch_ev"])])
for i, c in enumerate(["ireland", "cyprus"] * 4):
    s2 = R.sample(list(SCH), 2)
    q = ["Ktorá z týchto krajín EÚ nie je súčasťou schengenského priestoru?",
         "Ktorá z uvedených krajín EÚ zatiaľ nepatrí do schengenského priestoru?",
         "Ktorá krajina EÚ z ponuky nie je v schengenskom priestore?",
         "Ktorá z týchto členských krajín EÚ stojí mimo schengenského priestoru?"][i // 2]
    add("sta", 2, q, C[c][0], [C[x][0] for x in s2],
        f"Z krajín EÚ nie sú v schengenskom priestore iba Írsko a Cyprus.",
        [(D[c]["slug"], D[c]["sch_ev"]), ("eu-facts", "Členmi schengenského priestoru sú všetky členské štáty EÚ okrem Cypru a Írska.")])

# 5) poslanci EP
MEPS = sorted({d["mep"] for d in D.values()})
for c in codes:
    d = D[c]
    m = d["mep"]
    near = sorted([x for x in MEPS if x != m], key=lambda x: abs(x - m))[:4]
    bad = R.sample(near, 2)
    n = 1 if c == "slovakia" else (2 if c in ("germany", "malta", "cyprus", "luxembourg") else 3)
    add("sta", n, f"Koľko poslancov volí {C[c][0]} do Európskeho parlamentu vo volebnom období 2024 – 2029?", m, bad,
        f"{C[c][0]} má v Európskom parlamente {m} poslancov.", [(d["slug"], d["mep_ev"])])

# 6) monarchie / republiky
REP = [c for c in codes if c not in MONARCHIE]
for i, c in enumerate(sorted(MONARCHIE) * 2):
    r2 = R.sample(REP, 2)
    q = ["Ktorá z týchto krajín EÚ je monarchiou?", "Na čele ktorej z týchto krajín stojí panovník (kráľ, kráľovná alebo veľkovojvoda)?"][i // len(MONARCHIE)]
    add("sta", 2, q, C[c][0], [C[x][0] for x in r2], f"{D[c]['pol']} {C[r2[0]][0]} a {C[r2[1]][0]} sú republiky.",
        [(D[c]["slug"], D[c]["pol"])])
for i, c in enumerate(R.sample(REP, 8)):
    m2 = R.sample(sorted(MONARCHIE), 2)
    add("sta", 2, ["Ktorá z týchto krajín je republikou?", "Ktorá z týchto krajín nemá na čele panovníka?"][i % 2], C[c][0],
        [C[x][0] for x in m2], f"{D[c]['pol']} {C[m2[0]][0]} a {C[m2[1]][0]} sú monarchie.", [(D[c]["slug"], D[c]["pol"])])
for c, kind in [("france", "poloprezidentská republika"), ("portugal", "poloprezidentská republika"),
                ("romania", "poloprezidentská republika"), ("cyprus", "prezidentská republika")]:
    add("sta", 3, f"Aké štátne zriadenie má {C[c][0]} podľa profilu krajiny na portáli EÚ?", kind,
        [x for x in ["parlamentná republika", "konštitučná monarchia", "poloprezidentská republika", "prezidentská republika"] if x != kind][:2],
        D[c]["pol"], [(D[c]["slug"], D[c]["pol"])])

# 7) porovnania rozlohy a obyvateľov
pairs = []
for reg, cs in REG.items():
    for tri in itertools.combinations(cs, 3):
        pairs.append(tri)
R.shuffle(pairs)
used, i = {}, -1
for tri in pairs:
    if len(used) and sum(used.values()) >= 40:
        break
    i += 1
    key = "pop" if i % 2 == 0 else "area"
    best = max(tri, key=lambda c: D[c][key])
    if i % 4 == 3:
        best = min(tri, key=lambda c: D[c][key])
    if used.get((key, i % 4 == 3, best), 0) >= 2:
        continue
    used[(key, i % 4 == 3, best)] = used.get((key, i % 4 == 3, best), 0) + 1
    if i % 4 == 3:
        q = "Ktorá z týchto krajín má najmenšiu rozlohu?" if key == "area" else "Ktorá z týchto krajín má najmenej obyvateľov?"
    else:
        q = "Ktorá z týchto krajín má najväčšiu rozlohu?" if key == "area" else "Ktorá z týchto krajín má najviac obyvateľov?"
    vals = "; ".join(f"{C[c][0]} {D[c][key]:,} {'km²' if key == 'area' else 'obyvateľov'}".replace(",", " ") for c in tri)
    add("sta", 2, q, C[best][0], [C[c][0] for c in tri if c != best],
        f"Podľa údajov Eurostatu za rok 2026: {vals}.", [(D[c]["slug"], D[c][key + "_ev"]) for c in tri])

os.makedirs(OUT, exist_ok=True)
json.dump(Q, open(os.path.join(OUT, "staty.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump(D, open(os.path.join(OUT, "_staty_data.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("staty:", len(Q))
