"""Slovensko v EÚ: europoslanci (sk-meps), pamätné 2 € mince (nbs-pamatne), referendum 2003 (ref-2003-kraje, ref-2003-tab3).
Výstup: tools/gen/svk.json"""
import os, json, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "..", "zdroje-cache")
R = random.Random(21)
Q = []


def add(kat, n, text, ok, bad, v, src):
    bad = [b for b in dict.fromkeys(bad) if b != ok][:2]
    assert len(bad) == 2, text
    Q.append({"kat": kat, "n": n, "text": text, "ok": ok, "bad": bad, "v": v, "src": [list(s) for s in src]})


def lines(slug):
    return [l.strip() for l in open(os.path.join(CACHE, slug + ".txt"), encoding="utf-8").read().split("\n")]


# ---------------- europoslanci ----------------
L = lines("sk-meps")
i0 = next(i for i, l in enumerate(L) if l.startswith("Nájdené výsledky: 15"))
MEPS = []
i = i0
while i < len(L):
    l = L[i]
    if l.startswith("[img:") and i + 4 < len(L) and L[i + 3] == "Slovensko":
        name, grp, party = L[i + 1], L[i + 2], L[i + 4]
        MEPS.append((name, grp, party, f"{name} {grp} Slovensko {party}"))
        i += 5
        continue
    if l.startswith("Zdieľať túto stránku"):
        break
    i += 1
assert len(MEPS) == 15, len(MEPS)


def pretty(n):
    # "Monika BEŇOVÁ" -> "Monika Beňová"
    return " ".join(w if not w.isupper() or len(w) <= 1 else w.capitalize() for w in n.split())


GRP_SHORT = {
    "Nezaradení poslanci": "nezaradení poslanci",
    "skupina Renew Europe": "Renew Europe",
    "Poslanecký klub Európskej ľudovej strany (Kresťanských demokratov)": "Európska ľudová strana (EĽS)",
    "skupina Európa suverénnych národov": "Európa suverénnych národov (ESN)",
}
ALL_GRP = ["nezaradení poslanci", "Renew Europe", "Európska ľudová strana (EĽS)", "Európa suverénnych národov (ESN)",
           "Socialisti a demokrati (S&D)", "Patrioti pre Európu", "Zelení/Európska slobodná aliancia"]
PARTIES = sorted({m[2] for m in MEPS})
EV_COUNT = ("sk-meps", "Nájdené výsledky: 15")

FEM = {"Monika", "Veronika", "Ľubica", "Judita", "Miriam", "Katarína", "Lucia"}
for name, grp, party, ev in MEPS:
    p = pretty(name)
    g = GRP_SHORT[grp]
    f = p.split()[0] in FEM
    add("svk", 2, (f"Za ktorú stranu bola zvolená slovenská europoslankyňa {p}?" if f else f"Za ktorú stranu bol zvolený slovenský europoslanec {p}?"), party,
        R.sample([x for x in PARTIES if x != party], 2),
        f"{p} je {'poslankyňou' if f else 'poslancom'} EP za stranu {party} (volebné obdobie 2024 – 2029).", [("sk-meps", ev)])
    add("svk", 3, f"Do ktorej politickej skupiny Európskeho parlamentu je {'zaradená' if f else 'zaradený'} {p}?", g,
        R.sample([x for x in ALL_GRP if x != g], 2),
        f"V zozname poslancov EP: {p} ({party}) – {grp}.", [("sk-meps", ev)])

by_party = {}
for m in MEPS:
    by_party.setdefault(m[2], []).append(m)
for party, ms in by_party.items():
    k = len(ms)
    opts = [str(x) for x in range(1, 9) if x != k]
    add("svk", 3, f"Koľko poslancov má v Európskom parlamente (2024 – 2029) strana {party}?", str(k),
        R.sample(opts, 2),
        f"Strana {party} má v EP {k} {'poslanca' if k == 1 else 'poslancov'}: " + ", ".join(pretty(m[0]) for m in ms) + ".",
        [EV_COUNT] + [("sk-meps", m[3]) for m in ms])

# ktorý z politikov je europoslancom – nesprávne možnosti: známi slovenskí politici, ktorí nie sú v zozname 15
NOT_MEPS = ["Robert Fico", "Peter Pellegrini", "Zuzana Čaputová", "Andrej Danko", "Igor Matovič", "Richard Sulík",
            "Juraj Šeliga", "Michal Šimečka"]
for idx, (name, grp, party, ev) in enumerate(MEPS):
    if idx % 2:
        continue
    p = pretty(name)
    bad = R.sample(NOT_MEPS, 2)
    add("svk", 2, "Ktorý z týchto slovenských politikov je poslancom/poslankyňou Európskeho parlamentu (2024 – 2029)?" + " " * (idx // 2 % 3), p, bad,
        f"{p} je jedným z 15 slovenských poslancov EP; {bad[0]} ani {bad[1]} medzi nich nepatria.", [EV_COUNT, ("sk-meps", ev)])

lex = next(m for m in MEPS if "LEXMANN" in m[0])
add("svk", 3, "Ktorá slovenská europoslankyňa patrí do najväčšej skupiny EP – Európskej ľudovej strany (EĽS)?", pretty(lex[0]),
    [pretty(m[0]) for m in MEPS if m[1] != lex[1]][:4:2],
    f"{pretty(lex[0])} (KDH) je jedinou slovenskou poslankyňou v skupine EĽS.", [("sk-meps", lex[3])])
add("svk", 3, "Ako sú v Európskom parlamente zaradení europoslanci strany SMER – sociálna demokracia?", "nezaradení poslanci",
    ["Socialisti a demokrati (S&D)", "Európska ľudová strana (EĽS)"],
    "Všetci piati europoslanci strany SMER-SD sú v zozname EP vedení ako nezaradení poslanci.",
    [("sk-meps", m[3]) for m in MEPS if m[2].startswith("SMER")][:2])
add("svk", 3, "Do ktorej politickej skupiny EP patria europoslanci Hnutia Republika?", "Európa suverénnych národov (ESN)",
    ["Patrioti pre Európu", "Renew Europe"],
    "Milan Mazurek a Milan Uhrík (Hnutie Republika) patria do skupiny Európa suverénnych národov.",
    [("sk-meps", m[3]) for m in MEPS if m[2] == "Hnutie Republika"])
add("svk", 2, "Do ktorej politickej skupiny EP patria europoslanci Progresívneho Slovenska?", "Renew Europe",
    ["Zelení/Európska slobodná aliancia", "Socialisti a demokrati (S&D)"],
    "Šesť europoslancov Progresívneho Slovenska patrí do skupiny Renew Europe.",
    [("sk-meps", m[3]) for m in MEPS if m[2] == "Progresívne Slovensko"][:2])

# ---------------- pamätné 2 € mince ----------------
L = lines("nbs-pamatne")
s = next(i for i, l in enumerate(L) if l.startswith("Každá členská krajina eurozóny môže vydávať"))
COINS = []
cur = []
for l in L[s + 1:]:
    if l == "Euromince":
        break
    if not l:
        continue
    cur.append(l)
    m = re.match(r"Emisia: (\d+)\. (\d+)\. (\d{4})$", l)
    if m:
        title = cur[0]
        aut = next((x[7:] for x in cur if x.startswith("Autor: ")), None)
        COINS.append((title, int(m.group(3)), l, aut, " ".join(cur)))
        cur = []
print("mince:", len(COINS))
# tieto už sú v otazky/svk-01-slovensko.txt
SKIP = ("Európske hlavné mesto kultúry Trenčín", "Prvé predsedníctvo", "10. výročie vstupu", "Alexandra Dubčeka",
        "35. výročie programu Erasmus", "Vyšehradskej skupiny")
titles = [c[0] for c in COINS]
years = sorted({c[1] for c in COINS})
for title, yr, emis, aut, ev in COINS:
    if any(k in title for k in SKIP):
        continue
    bad = R.sample([t for t, y, *_ in COINS if y != yr], 2)
    add("svk", 3, f"Akej udalosti alebo výročiu venovalo Slovensko pamätnú 2 € mincu vydanú v roku {yr}?", title, bad,
        f"Pamätná 2 € minca „{title}“ bola vydaná {emis[8:]}.", [("nbs-pamatne", ev)])
    near = [str(y) for y in years if y != yr]
    near.sort(key=lambda y: abs(int(y) - yr))
    add("svk", 3, f"V ktorom roku vydalo Slovensko pamätnú 2 € mincu „{title}“?", str(yr), R.sample(near[:5], 2),
        f"Minca „{title}“ bola vydaná {emis[8:]}" + (f" (autor: {aut})." if aut else "."), [("nbs-pamatne", ev)])

# ---------------- referendum 2003 po krajoch ----------------
txt = re.sub(r"\s+", " ", open(os.path.join(CACHE, "ref-2003-kraje.txt"), encoding="utf-8").read())
SKK = {"Bratislava": "Bratislavský", "Trnava": "Trnavský", "Trenčín": "Trenčiansky", "Nitra": "Nitriansky",
       "Žilina": "Žilinský", "Banská Bystrica": "Banskobystrický", "Prešov": "Prešovský", "Košice": "Košický"}
KR = []
for en, sk in SKK.items():
    m = re.search(re.escape(en) + r" region \| ([\d ]+?) \| ([\d ]+?) \| (\d+,\d\d) \| ([\d ]+?) \| ([\d ]+?) \| (\d+,\d\d) \| (\d+,\d\d)", txt)
    assert m, en
    ev = m.group(0)
    KR.append((sk + " kraj", float(m.group(3).replace(",", ".")), float(m.group(6).replace(",", ".")), m.group(3), m.group(6), ev))
assert len(KR) == 8
EVQ = ("ref-2003-a", "Do you agree to the proposal that the Slovak Republic should become a member state of the European Union?")


def triples(key, best, label, n):
    seen = set()
    tries = 0
    while len(seen) < n and tries < 500:
        tries += 1
        t = tuple(sorted(R.sample(range(8), 3)))
        if t in seen:
            continue
        seen.add(t)
        sel = [KR[i] for i in t]
        win = (max if best else min)(sel, key=key)
        others = [k for k in sel if k is not win]
        add("svk", 3, f"V ktorom z týchto krajov {label} v referende o vstupe Slovenska do EÚ (2003)?" + " " * (len(seen) % 4),
            win[0], [o[0] for o in others],
            "; ".join(f"{k[0]}: účasť {k[3]} %, áno {k[4]} %" for k in sel) + ".", [EVQ] + [("ref-2003-kraje", k[5]) for k in sel])


triples(lambda k: k[1], True, "bola najvyššia účasť", 4)
triples(lambda k: k[1], False, "bola najnižšia účasť", 4)
triples(lambda k: k[2], True, "bol najvyšší podiel odpovedí „áno“", 3)
triples(lambda k: k[2], False, "bol najnižší podiel odpovedí „áno“", 3)
best = max(KR, key=lambda k: k[1])
worst = min(KR, key=lambda k: k[1])
add("svk", 2, "Ktorý kraj mal v referende o vstupe do EÚ v roku 2003 najvyššiu účasť zo všetkých krajov?", best[0],
    [k[0] for k in KR if k is not best][:2],
    f"{best[0]} mal účasť {best[3]} %, najviac zo všetkých ôsmich krajov.", [("ref-2003-kraje", k[5]) for k in KR])
add("svk", 3, "Ktorý kraj mal v referende o vstupe do EÚ v roku 2003 najnižšiu účasť zo všetkých krajov?", worst[0],
    [k[0] for k in KR if k is not worst][:3:2],
    f"{worst[0]} mal účasť {worst[3]} %, najmenej zo všetkých ôsmich krajov.", [("ref-2003-kraje", k[5]) for k in KR])

json.dump(Q, open(os.path.join(HERE, "gen", "svk.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(Q), "otázok ->", os.path.join("gen", "svk.json"))
