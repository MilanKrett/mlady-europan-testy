"""Generuje otázky: komisári 2024 – 2029 (akt), vstup krajín do EÚ (his), predsedníctva Rady EÚ (ins).
Výstup: tools/gen/eu.json"""
import os, re, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(os.path.dirname(os.path.dirname(HERE)), "zdroje-cache")
R = random.Random(77)
D = json.load(open(os.path.join(HERE, "gen", "_staty_data.json"), encoding="utf-8"))
import sys; sys.path.insert(0, HERE)
from gen_staty import C  # noqa: E402  (tabuľka názvov krajín)

Q = []


def add(kat, n, text, ok, bad, v, src):
    bad = [str(b) for b in bad if str(b) != str(ok)][:2]
    assert len(bad) == 2, (text, ok, bad)
    Q.append({"kat": kat, "n": n, "text": text, "ok": str(ok), "bad": bad, "v": v, "src": [list(s) for s in src]})


# ---------- Komisia 2024 – 2029 (com-college) ----------
# (meno na stránke, krajina, žena?, oblasť – doslovne zo stránky, krátky opis do otázky)
KOM = [
    ("Teresa Riberová", "spain", 1, "čistá, spravodlivá a konkurencieschopná transformácia", "čistú, spravodlivú a konkurencieschopnú transformáciu", "výkonná podpredsedníčka"),
    ("Henna Virkkunenová", "finland", 1, "technologická suverenita, bezpečnosť a demokracia", "technologickú suverenitu, bezpečnosť a demokraciu", "výkonná podpredsedníčka"),
    ("Stéphane Séjourné", "france", 0, "prosperita a priemyselná stratégia", "prosperitu a priemyselnú stratégiu", "výkonný podpredseda"),
    ("Kaja Kallasová", "estonia", 1, "vysoká predstaviteľka Únie pre zahraničné veci a bezpečnostnú politiku", "zahraničné veci a bezpečnostnú politiku (ako vysoká predstaviteľka Únie)", "vysoká predstaviteľka a podpredsedníčka"),
    ("Roxana Mînzatuová", "romania", 1, "sociálne práva a zručnosti, kvalitné pracovné miesta a pripravenosť", "sociálne práva a zručnosti, kvalitné pracovné miesta a pripravenosť", "výkonná podpredsedníčka"),
    ("Raffaele Fitto", "italy", 0, "súdržnosť a reformy", "súdržnosť a reformy", "výkonný podpredseda"),
    ("Maroš Šefčovič", "slovakia", 0, "obchod a ekonomická bezpečnosť, medziinštitucionálne vzťahy a transparentnosť", "obchod a ekonomickú bezpečnosť, medziinštitucionálne vzťahy a transparentnosť", "komisár"),
    ("Valdis Dombrovskis", "latvia", 0, "hospodárstvo a produktivita, vykonávanie a zjednodušenie", "hospodárstvo a produktivitu, vykonávanie a zjednodušenie", "komisár"),
    ("Dubravka Šuicová", "croatia", 1, "Stredozemie", "Stredozemie", "komisárka"),
    ("Olivér Várhelyi", "hungary", 0, "zdravie a dobré životné podmienky zvierat", "zdravie a dobré životné podmienky zvierat", "komisár"),
    ("Wopke Hoekstra", "netherlands", 0, "klíma, nulová bilancia emisií a čistý rast", "klímu, nulovú bilanciu emisií a čistý rast", "komisár"),
    ("Andrius Kubilius", "lithuania", 0, "obrana a vesmírna agenda", "obranu a vesmírnu agendu", "komisár"),
    ("Marta Kosová", "slovenia", 1, "rozširovanie", "rozširovanie", "komisárka"),
    ("Jozef Síkela", "czechia", 0, "medzinárodné partnerstvá", "medzinárodné partnerstvá", "komisár"),
    ("Kostas Kadis", "cyprus", 0, "rybárstvo a oceány", "rybárstvo a oceány", "komisár"),
    ("Maria Luís Albuquerqueová", "portugal", 1, "finančné služby a únia úspor a investícií", "finančné služby a úniu úspor a investícií", "komisárka"),
    ("Hadja Lahbibová", "belgium", 1, "rovnosť, pripravenosť a krízové riadenie", "rovnosť, pripravenosť a krízové riadenie", "komisárka"),
    ("Magnus Brunner", "austria", 0, "vnútorné veci a migrácia", "vnútorné veci a migráciu", "komisár"),
    ("Jessika Roswallová", "sweden", 1, "životné prostredie, odolnosť v oblasti vody a konkurencieschopné obehové hospodárstvo", "životné prostredie, odolnosť v oblasti vody a obehové hospodárstvo", "komisárka"),
    ("Piotr Serafin", "poland", 0, "rozpočet, boj proti podvodom a verejná správa", "rozpočet, boj proti podvodom a verejnú správu", "komisár"),
    ("Dan Jørgensen", "denmark", 0, "energetika a bývanie", "energetiku a bývanie", "komisár"),
    ("Ekaterina Zacharievová", "bulgaria", 1, "startupy, výskum a inovácie", "startupy, výskum a inovácie", "komisárka"),
    ("Michael McGrath", "ireland", 0, "demokracia, spravodlivosť, právny štát a ochrana spotrebiteľa", "demokraciu, spravodlivosť, právny štát a ochranu spotrebiteľa", "komisár"),
    ("Apostolos Tzitzikostas", "greece", 0, "udržateľná doprava a cestovný ruch", "udržateľnú dopravu a cestovný ruch", "komisár"),
    ("Christophe Hansen", "luxembourg", 0, "poľnohospodárstvo a potraviny", "poľnohospodárstvo a potraviny", "komisár"),
    ("Glenn Micallef", "malta", 0, "medzigeneračná spravodlivosť, mládež, kultúra a šport", "medzigeneračnú spravodlivosť, mládež, kultúru a šport", "komisár"),
]
SHORT = {  # kratšie opisy oblastí do možností
    k[0]: k[4] for k in KOM
}
EASY = {"Maroš Šefčovič", "Kaja Kallasová", "Marta Kosová", "Andrius Kubilius", "Christophe Hansen"}
for i, (name, code, fem, port, port_acc, role) in enumerate(KOM):
    ev = f"{name} {port}"
    others = [k for k in KOM if k[0] != name]
    # 1) za čo zodpovedá
    b = R.sample(others, 2)
    rola = "komisárka" if fem else "komisár"
    if role.startswith("výkonn") or role.startswith("vysok"):
        rola = role
    add("akt", 2 if name in EASY else 3,
        f"Za ktorú oblasť zodpovedá v Európskej komisii 2024 – 2029 {rola} {name}?",
        port_acc, [SHORT[x[0]] for x in b],
        f"{name} ({C[code][0]}) má v Komisii Ursuly von der Leyenovej na starosti oblasť: {port}.",
        [("com-college", ev)])
    # 2) kto zodpovedá za oblasť
    b = R.sample(others, 2)
    add("akt", 2 if name in EASY else 3,
        f"Kto má v Európskej komisii 2024 – 2029 na starosti oblasť „{port}“?",
        name, [x[0] for x in b], f"Oblasť „{port}“ vedie {name} z krajiny {C[code][0]}.", [("com-college", ev)])
    # 3) odkiaľ pochádza
    kev = D[code].get("kom_ev")
    if kev:
        b = R.sample([k[1] for k in others], 2)
        add("akt", 1 if code == "slovakia" else 2,
            f"Ktorú krajinu reprezentuje v Európskej komisii 2024 – 2029 {('komisárka' if fem else 'komisár')} {name}?".replace("reprezentuje", "navrhla do"
            ) if False else f"Z ktorej krajiny pochádza člen Európskej komisie {name}?",
            C[code][0], [C[x][0] for x in b], kev, [(D[code]["slug"], kev)])

# predsedníčka
add("akt", 1, "Kto je predsedom (predsedníčkou) Európskej komisie v rokoch 2024 – 2029?", "Ursula von der Leyenová",
    ["Roberta Metsolová", "Kaja Kallasová"], "Komisiu vedie Ursula von der Leyenová, ktorá je predsedníčkou od roku 2019 a v roku 2024 začala druhé funkčné obdobie.",
    [("com-college", "Predsedníčka Ursula von der Leyenová")])
add("akt", 2, "Koľko členov má kolégium Európskej komisie 2024 – 2029 vrátane predsedníčky?", 27, [26, 28],
    "Kolégium tvorí 27 členov, po jednom z každej krajiny EÚ.", [("com-college", "Kolégium sa skladá z komisárov z 27 krajín EÚ.")])
add("akt", 2, "Na aké funkčné obdobie je vymenované kolégium komisárov?", "na päť rokov", ["na štyri roky", "na dva a pol roka"],
    "Kolégium je vymenované ako politické vedenie Komisie na päťročné funkčné obdobie.",
    [("com-college", "na päťročné funkčné obdobie")])
add("akt", 3, "V ktorý deň v týždni sa kolégium komisárov zvyčajne schádza v Bruseli?", "v stredu", ["v pondelok", "v piatok"],
    "Kolégium zasadá raz týždenne, zvyčajne v stredu v Bruseli. Počas pléna v Štrasburgu zasadá v utorok.",
    [("com-college", "Zvyčajne sa stretáva každú stredu v Bruseli.")])
add("akt", 3, "Kedy zasadá kolégium komisárov počas plenárnych zasadnutí Európskeho parlamentu v Štrasburgu?", "v utorok",
    ["v stredu", "vo štvrtok"], "Počas plenárnych zasadnutí EP v Štrasburgu sa kolégium stretáva v utorok.",
    [("com-college", "Počas plenárnych zasadnutí Európskeho parlamentu v Štrasburgu sa zasadnutie kolégia koná v utorok.")])
add("akt", 2, "Ako prijíma kolégium komisárov rozhodnutia?", "spoločne, podľa zásady kolegiality",
    ["hlasom predsedníčky, ostatní iba radia", "každý komisár rozhoduje sám za svoju krajinu"],
    "Kolégium rozhoduje spoločne podľa zásady kolegiality. Hlas každého z 27 členov má rovnakú váhu.",
    [("com-college", "Rozhodnutia prijíma kolégium komisárov spoločne na základe zásady kolegiality.")])

# ---------- vstup do EÚ (his) ----------
def VERB(code):
    return {"cyprus": "vstúpil", "lithuania": "vstúpila", "malta": "vstúpila"}.get(code, "vstúpilo")


YEARS = [1958, 1973, 1981, 1986, 1995, 2004, 2007, 2013]
for code, d in D.items():
    y = d["join_y"]
    idx = YEARS.index(y)
    near = [YEARS[j] for j in (idx - 1, idx + 1, idx - 2, idx + 2) if 0 <= j < len(YEARS)]
    bad = near[:2]
    nom = C[code][0]
    if y == 1958:
        q = f"Odkedy je {nom} členom európskych spoločenstiev, z ktorých vznikla EÚ?"
        n = 1
    else:
        q = f"V ktorom roku vstúpila krajina {nom} do Európskej únie (resp. európskych spoločenstiev)?"
        n = 1 if code in ("slovakia", "croatia", "czechia", "poland", "hungary") else 2
        if code in ("greece", "finland", "austria", "sweden", "denmark", "ireland", "portugal", "spain"):
            n = 2
    add("his", n, q, y, bad, f"{nom} je členským štátom EÚ od {d['join']}.", [(d["slug"], d["join_ev"])])

GROUPS = {}
for code, d in D.items():
    GROUPS.setdefault(d["join_y"], []).append(code)
for y, cs in GROUPS.items():
    if y == 1958:
        continue
    for c in cs:
        other = [x for x in D if D[x]["join_y"] != y]
        b = R.sample(other, 2)
        add("his", 2, f"Ktorá z týchto krajín vstúpila do EÚ (resp. európskych spoločenstiev) v roku {y}?", C[c][0],
            [C[x][0] for x in b], f"V roku {y} vstúpili: {', '.join(C[x][0] for x in cs)}. "
            + " ".join(f"{C[x][0]} " + ("patrí k zakladajúcim krajinám." if D[x]['join_y'] == 1958 else f"{VERB(x)} v roku {D[x]['join_y']}.") for x in b),
            [(D[c]["slug"], D[c]["join_ev"]), (D[b[0]]["slug"], D[b[0]]["join_ev"]), (D[b[1]]["slug"], D[b[1]]["join_ev"])])
# zakladajúce krajiny
F = GROUPS[1958]
for c in F:
    b = R.sample([x for x in D if x not in F], 2)
    add("his", 1, "Ktorá z týchto krajín patrí k šiestim zakladajúcim krajinám európskych spoločenstiev?", C[c][0],
        [C[x][0] for x in b], "Zakladajúcich krajín bolo šesť: Belgicko, Francúzsko, Nemecko, Taliansko, Luxembursko a Holandsko.",
        [("eu-facts", "Založenie: v roku 1951 po druhej svetovej vojne šiestimi krajinami (Belgicko, Francúzsko, Nemecko, Taliansko, Luxembursko a Holandsko).")])

# ---------- predsedníctvo Rady EÚ (ins) ----------
t = open(os.path.join(CACHE, "cons-presidency.txt"), encoding="utf-8").read()
P = re.findall(r"\n(\w+): (január – jún|júl – december) (\d{4}) \(v trojici (so|s) (\w+) a (\w+)\)", t)
assert len(P) >= 25, len(P)
names = [p[0] for p in P]
for i, (cn, half, y, prep, a, b) in enumerate(P):
    period = f"{half} {y}"
    ev = f"{cn}: {half} {y}"
    nb = R.sample([x for x in names if x != cn and abs(names.index(x) - i) <= 4], 2)
    tense = "predsedala" if int(y) < 2026 or (y == "2026" and half.startswith("jan")) else ("predsedá" if y == "2026" else "bude predsedať")
    n = 2 if 2024 <= int(y) <= 2027 else 3
    q = f"Ktorá krajina {tense} Rade Európskej únie v období {period}?"
    add("ins", n, q, cn, nb, f"V období {period} {tense} Rade EÚ krajina {cn} (v trojici {prep} {a} a {b}).",
        [("cons-presidency", ev)])
add("ins", 1, "Ako často sa krajiny EÚ striedajú v predsedníctve Rady Európskej únie?", "každých šesť mesiacov",
    ["každý rok", "každých dva a pol roka"], "Členské štáty sa vo vykonávaní predsedníctva Rady striedajú vždy po šiestich mesiacoch.",
    [("cons-presidency", "Členské štáty EÚ sa vo vykonávaní predsedníctva Rady Európskej únie striedajú vždy po šiestich mesiacoch.")])
add("ins", 2, "Koľko krajín tvorí tzv. trojicu predsedníctiev Rady EÚ?", 3, [2, 4],
    "Krajiny s po sebe idúcimi predsedníctvami spolupracujú v trojčlenných skupinách, tzv. trojici.",
    [("cons-presidency", "Členské štáty, ktoré vykonávajú po sebe idúce predsedníctva, úzko spolupracujú v rámci trojčlenných skupín označovaných ako „trojica“.")])
add("ins", 3, "Ktorá zmluva zaviedla systém trojice predsedníctiev Rady EÚ?", "Lisabonská zmluva", ["Zmluva z Nice", "Maastrichtská zmluva"],
    "Systém trojice predsedníctiev sa zaviedol Lisabonskou zmluvou v roku 2009.",
    [("cons-presidency", "Tento systém sa zaviedol Lisabonskou zmluvou v roku 2009.")])
add("ins", 3, "Na koľko mesiacov pripravuje trojica predsedníctiev spoločný program Rady?", 18, [12, 24],
    "Trojica pripravuje spoločný program na 18 mesiacov.",
    [("cons-presidency", "počas 18 mesiacov bude Rada venovať")])
add("ins", 3, "Zasadnutiam ktorého zloženia Rady nepredsedá rotujúce predsedníctvo?", "Rade pre zahraničné veci",
    ["Rade pre poľnohospodárstvo a rybárstvo", "Rade pre hospodárske a finančné veci"],
    "Predsedníctvo vedie zasadnutia Rady okrem Rady pre zahraničné veci, ktorej predsedá vysoký predstaviteľ.",
    [("cons-presidency", "Predsedníctvo plánuje, koordinuje a vedie zasadnutia Rady (okrem Rady pre zahraničné veci)")])
add("ins", 3, "Približne po koľkých rokoch sa krajina opäť dostane k predsedníctvu Rady EÚ?", "po 13,5 roku",
    ["po 6 rokoch", "po 27 rokoch"], "Pri 27 krajinách a šiestich mesiacoch sa krajiny striedajú po 13,5 roku.",
    [("cons-presidency", "sa bez ohľadu na svoju veľkosť striedajú vo výkone tejto funkcie po 13,5 roku")])
add("akt", 2, "Pod akým heslom predsedá Írsko Rade EÚ v druhom polroku 2026?", "Sila v jednote",
    ["Zjednotení v rozmanitosti", "Európa, ktorá chráni"], "Írsko predsedá Rade EÚ pod heslom „Sila v jednote“.",
    [("cons-presidency", "Írsko sa pod heslom „Sila v jednote“ zameria")])
add("akt", 2, "Koľkýkrát predsedá Írsko Rade EÚ v druhom polroku 2026?", "ôsmykrát", ["prvýkrát", "štvrtýkrát"],
    "Írsko vykonáva predsedníctvo Rady ôsmykrát.", [("cons-presidency", "V súčasnosti vykonáva rotujúce predsedníctvo Rady Írsko, a to ôsmykrát")])
add("akt", 2, "Ktoré krajiny tvoria trojicu predsedníctiev Rady EÚ od júla 2026 do decembra 2027?", "Írsko, Litva a Grécko",
    ["Poľsko, Dánsko a Cyprus", "Taliansko, Lotyšsko a Luxembursko"], "Súčasnú trojicu tvoria Írsko, Litva a Grécko.",
    [("cons-presidency", "Súčasnú trojicu predsedníctiev tvoria: Írsko Litva Grécko")])

# prvé predsedníctvo nových členov (z profilov krajín)
for code in ["slovakia", "czechia", "slovenia", "poland", "hungary", "lithuania", "latvia", "malta", "estonia", "bulgaria", "romania", "croatia", "cyprus"]:
    d = D[code]
    first = d["pres"][0]
    y = int(first[-4:])
    cands = sorted({int(D[x]["pres"][0][-4:]) for x in ["slovakia", "czechia", "slovenia", "poland", "hungary", "lithuania", "latvia", "malta", "estonia", "bulgaria", "romania", "croatia", "cyprus"]} - {y}, key=lambda v: abs(v - y))
    bad = R.sample(cands[:4], 2)
    add("svk" if code == "slovakia" else "ins", 1 if code == "slovakia" else 3,
        f"Kedy prvýkrát predsedala Rade EÚ krajina {C[code][0]}?", f"{first}".replace("až", "–"), [f"{('január – jún' if v % 2 else 'júl – december')} {v}" for v in bad],
        f"Predsedníctva krajiny {C[code][0]}: {d['pres_ev']}.", [(d["slug"], d["pres_ev"])])

json.dump(Q, open(os.path.join(HERE, "gen", "eu.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("eu:", len(Q))
