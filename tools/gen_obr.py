"""Obrázkové otázky (kat obr): portréty predsedov EP a komisárov, slovenskí europoslanci, logá inštitúcií a agentúr,
mapy členských štátov s vlajkou, národné strany euromincí. Výstup: tools/gen/obr.json + img/kredity.json"""
import os, json, random, re, sys, unicodedata, contextlib, io

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(ROOT, "..", "zdroje-cache")
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):  # tieto moduly pri importe len pregenerujú svoje (deterministické) súbory
    from gen_staty import C
    from gen_eu import KOM
    from gen_agentury import A
    from gen_mince import M, ST
    from gen_hist import EP, NAT
    from gen_svk import MEPS, pretty, PARTIES, FEM as MEP_FEM

R = random.Random(404)
Q, CRED = [], {}
D = json.load(open(os.path.join(HERE, "gen", "_staty_data.json"), encoding="utf-8"))


def add(n, text, ok, bad, v, src, img):
    bad = [b for b in dict.fromkeys(bad) if b != ok][:2]
    assert len(bad) == 2, text
    assert os.path.exists(os.path.join(ROOT, img)), img
    Q.append({"kat": "obr", "n": n, "text": text, "ok": ok, "bad": bad, "v": v, "src": [list(s) for s in src], "img": img})


def cred(img, page, url, who):
    CRED[img] = {"stranka": page, "obrazok": url, "autor": who}


def ascii_(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def url_of(slug):
    return open(os.path.join(CACHE, slug + ".txt"), encoding="utf-8").readline()[5:].strip()


def cache_has(slug, s):
    t = re.sub(r"\s+", " ", open(os.path.join(CACHE, slug + ".txt"), encoding="utf-8").read())
    return s in t


# ---------------- predsedovia Európskeho parlamentu ----------------
EPB = "https://historicalarchives.europarl.europa.eu/files/live/sites/historicalarchive/files/01_FONDS/01_Former%20Presidents/00_Presidents%20Portraits/"
EPIMG = {  # meno v zdroji -> (súbor, alt text na stránke)
    "Emilio Colombo": ("colombo", "Emilio Colombo"), "Simone Veil": ("veil", "Simone Veil"), "Pieter Dankert": ("dankert", "Piet Dankert"),
    "Pierre Pflimlin": ("pflimlin", "Pierre Pflimlin"), "Lord Plumb": ("lord_plumb", "Lord Henry Plumb"),
    "Enrique Barón Crespo": ("baron_crespo", "Enrique Baron Crespo"), "Egon A. Klepsch": ("klepsch", "Egon A. Klepsch"),
    "Klaus Hänsch": ("haensch", "Klaus Hänsch"), "José María Gil-Robles Gil-Delgado": ("gil-robles", "Jose Maria Gil-Robles"),
    "Nicole Fontaine": ("fontaine", "Nicole Fontaine"), "Pat Cox": ("cox", "Pat Cox"), "Josep Borrell Fontelles": ("borrell_fontelles", "Josep Borrell Fontelles"),
    "Hans-Gert Pöttering": ("poettering", "Hans-Gert Pöttering"), "Jerzy Buzek": ("buzek", "Jerzy Buzek"), "Martin Schulz": ("schulz", "Martin Schulz"),
    "Antonio Tajani": ("tajani", "Antonio Tajani"), "David Maria Sassoli": ("sassoli", "David Maria Sassoli"), "Roberta Metsola": ("metsola", "Roberta Metsola"),
}
EP_EASY = {"Roberta Metsola", "Simone Veil", "David Maria Sassoli", "Antonio Tajani", "Martin Schulz", "Josep Borrell Fontelles"}
for i, (raw, nm, fem, span, ev) in enumerate(EP):
    f, alt = EPIMG[raw]
    img = f"img/ep/{f}.jpg"
    cred(img, "https://historicalarchives.europarl.europa.eu/en/fonds/former-presidents", EPB + f"portrait_{f}.jpg",
         "© Európska únia – Európsky parlament (Historické archívy EP)")
    ev_img = f"European Parliament President {alt}"
    assert cache_has("ep-hist-presidents", ev_img), ev_img
    same = [e for e in EP if e[2] == fem and e[0] != raw]
    same.sort(key=lambda e: abs(EP.index(e) - i))
    bad = [e[1] for e in same[:4]]
    R.shuffle(bad)
    who = "predsedníčkou" if fem else "predsedom"
    add(1 if raw == "Roberta Metsola" else (2 if raw in EP_EASY else 3),
        "Kto je na fotografii? (predseda alebo predsedníčka Európskeho parlamentu)", nm, bad,
        f"Na fotografii je {nm}, {'predsedníčka' if fem else 'predseda'} Európskeho parlamentu ({span}).",
        [("ep-hist-presidents", ev_img), ("ep-hist-presidents", ev)], img)
    if not span.startswith("od"):
        bad = [e[3] for e in EP if e[0] != raw and not e[3].startswith("od")]
        bad.sort(key=lambda s: abs(int(s[:4]) - int(span[:4])))
        add(3, f"{'Žena' if fem else 'Muž'} na fotografii je {nm}. V ktorých rokoch bol{'a' if fem else ''} {who} Európskeho parlamentu?", span, bad[:2],
            f"{nm} bol{'a' if fem else ''} {who} EP v rokoch {span}.", [("ep-hist-presidents", ev)], img)
    else:
        add(1, "Žena na fotografii je Roberta Metsolová. Akú funkciu zastáva od roku 2022?", "predsedníčka Európskeho parlamentu",
            ["predsedníčka Európskej komisie", "vysoká predstaviteľka EÚ pre zahraničné veci"],
            "Roberta Metsolová je predsedníčkou Európskeho parlamentu od roku 2022.", [("ep-hist-presidents", ev)], img)

# ---------------- členovia Európskej komisie 2024 – 2029 ----------------
COMPAGE = "https://commission.europa.eu/about/organisation/college-commissioners_sk"
KFILE = {"Teresa Riberová": "teresa-ribera-rodriguez", "Henna Virkkunenová": "henna-virkkunen", "Stéphane Séjourné": "stephane-sejourne",
         "Kaja Kallasová": "kaja-kallas", "Roxana Mînzatuová": "roxana-minzatu", "Raffaele Fitto": "raffaele-fitto",
         "Maroš Šefčovič": "maros-sefcovic", "Valdis Dombrovskis": "valdis-dombrovskis", "Dubravka Šuicová": "dubravka-suica",
         "Olivér Várhelyi": "oliver-varhely", "Wopke Hoekstra": "wopke-hoekstra", "Andrius Kubilius": "kubilius", "Marta Kosová": "marta-kos",
         "Jozef Síkela": "jozef-sikela", "Kostas Kadis": "costas-kadis", "Maria Luís Albuquerqueová": "maria-luis-albuquerque",
         "Hadja Lahbibová": "hadja-lahbib", "Magnus Brunner": "magnus-brunner", "Jessika Roswallová": "jessika-roswall",
         "Piotr Serafin": "piotr-serafin", "Dan Jørgensen": "dan-jorgensen", "Ekaterina Zacharievová": "ekaterina-zaharieva",
         "Michael McGrath": "michael-mcgrath", "Apostolos Tzitzikostas": "apostolos-tzitzikostas", "Christophe Hansen": "christophe-hansen",
         "Glenn Micallef": "glenn-micallef"}
KM = []
for name, code, fem, port, port_acc, role in KOM:
    KM.append((name, code, fem, port, port_acc, role, f"img/kom/{KFILE[name]}.jpg"))
assert len({k[-1] for k in KM}) == len(KM) == 26
for k in KM:
    cred(k[-1], COMPAGE, COMPAGE, "© Európska únia, 2024 – 2026 (Európska komisia)")
cred("img/kom/president.jpg", COMPAGE, COMPAGE, "© Európska únia, 2024 – 2026 (Európska komisia)")
KEASY = {"Maroš Šefčovič", "Kaja Kallasová"}
for name, code, fem, port, port_acc, role, img in KM:
    ev = f"{name} {port}"
    same = [k for k in KM if k[2] == fem and k[0] != name]
    bad = [k[0] for k in R.sample(same, 2)]
    add(1 if name == "Maroš Šefčovič" else (2 if name in KEASY else 3),
        "Kto je na fotografii? (člen Európskej komisie 2024 – 2029)", name, bad,
        f"Na fotografii je {name} ({C[code][0]}) – v Komisii zodpovedá za oblasť: {port}.", [("com-college", ev)], img)
    others = [k for k in KM if k[0] != name]
    bad = [k[4] for k in R.sample(others, 2)]
    add(2 if name in KEASY else 3, f"Na fotografii je {name}. Za ktorú oblasť zodpovedá v Európskej komisii 2024 – 2029?", port_acc, bad,
        f"{name} má v Komisii Ursuly von der Leyenovej na starosti oblasť: {port}.", [("com-college", ev)], img)
add(1, "Kto je na fotografii? (predsedníčka Európskej komisie)", "Ursula von der Leyenová", ["Roberta Metsolová", "Kaja Kallasová"],
    "Na fotografii je Ursula von der Leyenová, predsedníčka Európskej komisie (od roku 2019, druhé obdobie od roku 2024).",
    [("com-college", "Predsedníčka Ursula von der Leyenová")], "img/kom/president.jpg")
add(1, "Žena na fotografii je Ursula von der Leyenová. Akú funkciu zastáva?", "predsedníčka Európskej komisie",
    ["predsedníčka Európskeho parlamentu", "prezidentka Európskej centrálnej banky"],
    "Ursula von der Leyenová vedie Európsku komisiu.", [("com-college", "Predsedníčka Ursula von der Leyenová")], "img/kom/president.jpg")

# ---------------- slovenskí poslanci EP ----------------
MEPPAGE = "https://www.europarl.europa.eu/meps/sk/search/advanced?countryCode=SK"
MEPID = {"BEŇOVÁ": 23868, "BLAHA": 257005, "CIFROVÁ": 257014, "HOJSÍK": 197770, "KALIŇÁK": 257007, "KARVAŠOVÁ": 257013,
         "LAŠŠÁKOVÁ": 198373, "LEXMANN": 204336, "MAZUREK": 249982, "ÓDOR": 257010, "ONDRUŠ": 257018, "ROTH": 96653,
         "UHRÍK": 197763, "WIEZIK": 197769, "YAR": 257011}
for name, grp, party, ev in MEPS:
    mid = next(v for k, v in MEPID.items() if k in name)
    img = f"img/mep/{mid}.jpg"
    cred(img, MEPPAGE, f"https://www.europarl.europa.eu/mepphoto/{mid}.jpg", "© Európska únia – Európsky parlament")
    p = pretty(name)
    fem = p.split()[0] in MEP_FEM
    same = [pretty(m[0]) for m in MEPS if (pretty(m[0]).split()[0] in MEP_FEM) == fem and m[0] != name]
    known = {"Erik Kaliňák", "Ľuboš Blaha", "Milan Uhrík", "Monika Beňová"}
    add(2 if p in known else 3, f"Kto je na fotografii? ({'slovenská poslankyňa' if fem else 'slovenský poslanec'} Európskeho parlamentu 2024 – 2029)",
        p, R.sample(same, 2), f"Na fotografii je {p} – {'poslankyňa' if fem else 'poslanec'} EP za stranu {party}.", [("sk-meps", ev)], img)
    add(2 if p in known else 3, f"Na fotografii je {'europoslankyňa' if fem else 'europoslanec'} {p}. Za ktorú stranu {'bola zvolená' if fem else 'bol zvolený'} "
        f"do Európskeho parlamentu?", party, R.sample([x for x in PARTIES if x != party], 2),
        f"{p} je {'poslankyňou' if fem else 'poslancom'} EP (2024 – 2029) za stranu {party}.", [("sk-meps", ev)], img)

# ---------------- logá inštitúcií, orgánov a agentúr ----------------
LG = json.load(open(os.path.join(HERE, "gen", "_logos.json"), encoding="utf-8"))
MAIN = {  # slug: (názov, krátka úloha, sídlo alebo None)
    "eu-inst-european-parliament": ("Európsky parlament", "priamo volený orgán s legislatívnou, kontrolnou a rozpočtovou zodpovednosťou", None),
    "eu-inst-council-european-union": ("Rada Európskej únie", "zastupuje vlády krajín EÚ, prijíma právne predpisy a koordinuje politiky", None),
    "eu-inst-european-commission": ("Európska komisia", "navrhuje a presadzuje právne predpisy, vykonáva politiky a rozpočet EÚ", None),
    "eu-inst-court-justice-european-union-cjeu": ("Súdny dvor Európskej únie", "zabezpečuje jednotný výklad a uplatňovanie práva EÚ", "Luxemburg"),
    "eu-inst-european-central-bank-ecb": ("Európska centrálna banka", "riadi euro a udržiava stabilné ceny", "Frankfurt nad Mohanom"),
    "eu-inst-european-court-auditors-eca": ("Európsky dvor audítorov", "kontroluje, či sa finančné prostriedky EÚ správne vyberajú a používajú", None),
    "eu-inst-european-economic-and-social-committee-eesc": ("Európsky hospodársky a sociálny výbor", "poradný orgán zástupcov zamestnávateľov, zamestnancov a záujmových skupín", None),
    "eu-inst-european-committee-regions-cor": ("Európsky výbor regiónov", "poradný orgán zástupcov regionálnych a miestnych orgánov", "Brusel"),
    "eu-inst-european-banking-authority-eba": ("Európsky orgán pre bankovníctvo (EBA)", "jednotný regulačný rámec a dohľad pre bankový sektor EÚ", None),
    "eu-inst-european-data-protection-board-edpb": ("Európsky výbor pre ochranu údajov (EDPB)", "jednotné uplatňovanie GDPR v krajinách EÚ", "Brusel"),
}
LOGOS = []  # (slug, názov, úloha, mesto, krajina, známe, hlavná inštitúcia?)
for slug, (nm, role, city) in MAIN.items():
    LOGOS.append((slug, nm, role, city, None, 1, True))
for s, nm, city, cntry, role, fb, famous in A:
    LOGOS.append(("eu-inst-" + s, nm, role, city, cntry, famous, False))
LOGOS = [l for l in LOGOS if l[0] in LG]
CITIES = sorted({l[3] for l in LOGOS if l[3]} | {"Viedeň", "Mníchov", "Lyon", "Kodaň", "Praha", "Ženeva"})
for slug, nm, role, city, cntry, famous, main in LOGOS:
    img = LG[slug]["img"]
    cred(img, url_of(slug), LG[slug]["url"], "Logo © príslušná inštitúcia, orgán alebo agentúra EÚ (portál european-union.europa.eu)")
    t = open(os.path.join(CACHE, slug + ".txt"), encoding="utf-8").read()
    t = re.sub(r"[  -​ ]", " ", t)
    ul = re.search(r"Úloha: ([^\n]+)", t)
    sd = re.search(r"Sídlo: [^\n]+", t)
    alt = re.search(r"\[img: ([^\]]*[Ll]ogo[^\]]*)\]", t)
    idev = (slug, alt.group(1).strip()) if alt else (slug, ul.group(0).strip()) if ul else None
    assert idev, slug
    pool = [l for l in LOGOS if l[6] == main and l[0] != slug] or LOGOS
    bad = [l[1] for l in R.sample(pool, 2)]
    add(1 if main and famous else 2, "Ktorej inštitúcii, orgánu alebo agentúre EÚ patrí logo na obrázku?", nm, bad,
        f"Na obrázku je logo: {nm}.", [idev], img)
    if city and sd:
        bad = R.sample([c for c in CITIES if c != city], 2)
        add(2 if famous else 3, f"Logo na obrázku patrí subjektu EÚ: {nm}. V ktorom meste sídli?", city, bad,
            f"{nm} sídli v meste {city}" + (f" ({cntry})." if cntry else "."), [(slug, sd.group(0).strip())], img)
    if main and ul:
        others = [l for l in LOGOS if l[6] and l[0] != slug]
        bad = [l[2] for l in R.sample(others, 2)]
        add(2, f"Logo na obrázku patrí subjektu EÚ: {nm}. Čím sa zaoberá?", role, bad,
            f"Podľa oficiálneho profilu: {ul.group(1).strip()}", [(slug, ul.group(0).strip())], img)

# ---------------- členské štáty: mapa s vlajkou ----------------
SI = json.load(open(os.path.join(HERE, "gen", "_staty_img.json"), encoding="utf-8"))
SIM = {"slovakia": ["czechia", "slovenia"], "slovenia": ["slovakia", "croatia"], "czechia": ["slovakia", "poland"], "austria": ["hungary", "slovenia"],
       "latvia": ["lithuania", "estonia"], "lithuania": ["latvia", "estonia"], "estonia": ["latvia", "finland"], "belgium": ["netherlands", "luxembourg"],
       "netherlands": ["belgium", "luxembourg"], "luxembourg": ["belgium", "netherlands"], "cyprus": ["malta", "greece"], "malta": ["cyprus", "italy"],
       "ireland": ["denmark", "portugal"], "denmark": ["sweden", "finland"], "sweden": ["finland", "denmark"], "finland": ["sweden", "estonia"],
       "spain": ["portugal", "france"], "portugal": ["spain", "italy"], "romania": ["bulgaria", "hungary"], "bulgaria": ["romania", "greece"],
       "croatia": ["slovenia", "hungary"], "hungary": ["austria", "romania"], "poland": ["czechia", "lithuania"], "germany": ["austria", "poland"],
       "france": ["belgium", "spain"], "italy": ["malta", "greece"], "greece": ["cyprus", "bulgaria"]}
for slug, info in SI.items():
    code = slug[11:]
    img = info["img"]
    cred(img, url_of(slug), info["url"], "© Európska únia (portál european-union.europa.eu)")
    d = D[code]
    nm = C[code][0]
    add(1 if code in ("slovakia", "germany", "france", "italy", "spain") else 2,
        "Ktorý členský štát EÚ je vyznačený na mape (vpravo hore je jeho vlajka)?", nm, [C[x][0] for x in SIM[code]],
        f"Na mape je vyznačené {nm}; vlajka v rohu je vlajka tohto štátu.", [(slug, info["alt"])], img)
    caps = [D[x]["cap"] for x in SIM[code]]
    add(2, "Aké je hlavné mesto členského štátu vyznačeného na mape?", d["cap"], caps,
        f"Na mape je {nm}, jeho hlavné mesto je {d['cap']}.", [(slug, info["alt"]), (slug, d["cap_ev"])], img)
    yrs = sorted({D[x]["join_y"] for x in D} - {d["join_y"]}, key=lambda y: abs(y - d["join_y"]))
    add(3, "V ktorom roku vstúpil do EÚ (resp. do Európskych spoločenstiev) štát vyznačený na mape?", str(d["join_y"]), [str(y) for y in yrs[:2]],
        f"{nm} je členským štátom EÚ od: {d['join']}.", [(slug, info["alt"]), (slug, d["join_ev"])], img)

# ---------------- národné strany euromincí ----------------
CM = json.load(open(os.path.join(HERE, "gen", "_coins_man.json"), encoding="utf-8"))
ECBP = {"ee": "et", "si": "sl"}
NEAR = {"at": ["de", "si"], "be": ["nl", "lu"], "bg": ["gr", "hr"], "cy": ["gr", "mt"], "de": ["at", "nl"], "ee": ["lv", "fi"],
        "es": ["pt", "it"], "fi": ["ee", "lv"], "fr": ["be", "lu"], "gr": ["cy", "bg"], "hr": ["si", "sk"], "ie": ["mt", "pt"],
        "it": ["mt", "es"], "lt": ["lv", "ee"], "lu": ["be", "nl"], "lv": ["lt", "ee"], "mt": ["cy", "it"], "nl": ["be", "de"],
        "pt": ["es", "ie"], "si": ["sk", "hr"], "sk": ["si", "hr"]}
DEN = {"2euro": "2 €", "1euro": "1 €", "50cent": "50 centov", "10cent": "10 centov", "1cent": "1 cent"}
SKM = {"2euro": ("dvojkríž na trojvrší zo štátneho znaku", "Na minciach hodnoty 1 € a 2 € je zobrazený dvojkríž na trojvrší, ktorý je v štátnom znaku Slovenskej republiky."),
       "1euro": ("dvojkríž na trojvrší zo štátneho znaku", "Na minciach hodnoty 1 € a 2 € je zobrazený dvojkríž na trojvrší, ktorý je v štátnom znaku Slovenskej republiky."),
       "50cent": ("Bratislavský hrad", "Mince v hodnote 10, 20 a 50 centov zobrazujú Bratislavský hrad a štátny znak Slovenskej republiky."),
       "10cent": ("Bratislavský hrad", "Mince v hodnote 10, 20 a 50 centov zobrazujú Bratislavský hrad a štátny znak Slovenskej republiky."),
       "1cent": ("tatranský štít Kriváň", "Na minciach hodnoty 1 cent, 2 centy a 5 centov je tatranský štít Kriváň, symbol zvrchovanosti slovenského národa, a štátny znak Slovenskej republiky.")}


def denoms(s):
    if "všetky" in s:
        return set(DEN)
    nums = re.findall(r"\d+", s)
    if "€" in s:
        return {n + "euro" for n in nums}
    if "cent" in s:
        return {n + "cent" for n in nums} if nums else {"50cent", "10cent", "1cent"}
    return set()


for key, info in CM.items():
    cc, dn = key.split("_")
    img = info["img"]
    cred(img, f"https://www.ecb.europa.eu/euro/coins/html/{ECBP.get(cc, cc)}.sk.html", info["url"], "© Európska centrálna banka (ECB)")
    nm = ST[cc]
    slug = "ecb-coins-" + cc
    if cc == "sk":
        motif, ev = SKM[dn]
        add(1, f"Ktorá krajina vydáva euromincu {DEN[dn]} s touto národnou stranou?", "Slovensko", [ST[x] for x in NEAR[cc]],
            f"Ide o slovenskú mincu {DEN[dn]}: {motif}.", [(slug, ev)], img)
        if dn in ("2euro", "50cent", "1cent"):
            add(1, f"Čo je zobrazené na národnej strane slovenskej euromince {DEN[dn]} na obrázku?", motif,
                [m for m in ("dvojkríž na trojvrší zo štátneho znaku", "Bratislavský hrad", "tatranský štít Kriváň", "Devín") if m != motif][:2] if dn != "1cent"
                else ["Bratislavský hrad", "Devín"], f"Na slovenských minciach: {ev}", [(slug, ev)], img)
        continue
    # krajiny s viacerými sériami (be, es, fr, nl): motív nemusí zodpovedať zvolenému obrázku -> bez motívu
    match = [m for m in M if m[0] == cc and dn in denoms(m[1])] if cc not in ("be", "es", "fr", "nl") else []
    anyev = next(m for m in M if m[0] == cc)
    m0 = match[0] if match else None
    add(2 if cc in ("de", "fr", "it", "es", "at") else 3, f"Ktorá krajina vydáva euromincu {DEN[dn]} s touto národnou stranou?", nm,
        [ST[x] for x in NEAR[cc]],
        f"Ide o národnú stranu mince {DEN[dn]}, ktorú vydáva {nm}" + (f" – motív: {m0[2]}." if m0 else "."),
        [(slug, (m0 or anyev)[3])], img)

# ---------------- zápis ----------------
json.dump(Q, open(os.path.join(HERE, "gen", "obr.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(CRED, open(os.path.join(ROOT, "img", "kredity.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(Q), "obrázkových otázok;", len(CRED), "obrázkov")
