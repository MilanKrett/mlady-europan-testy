"""Otázky o sídlach a úlohách agentúr a orgánov EÚ (profily na european-union.europa.eu). Výstup: tools/gen/agentury.json"""
import os, re, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(os.path.dirname(os.path.dirname(HERE)), "zdroje-cache")
R = random.Random(31)

# slug (bez eu-inst-), názov do otázky, mesto, krajina, krátka úloha do možností, záložný dôkaz sídla (ak nie je riadok „Sídlo:“), známe?
A = [
    ("agency-cooperation-energy-regulators-acer", "Agentúra pre spoluprácu regulačných orgánov v oblasti energetiky (ACER)", "Ľubľana", "Slovinsko", "spolupráca regulačných orgánov v oblasti energetiky", None, 0),
    ("agency-support-berec-berec-office", "Úrad BEREC", "Riga", "Lotyšsko", "podpora regulátorov elektronických komunikácií", None, 0),
    ("community-plant-variety-office-cpvo", "Úrad Spoločenstva pre odrody rastlín (CPVO)", "Angers", "Francúzsko", "právna ochrana nových odrôd rastlín", "49101 Angers", 0),
    ("eurofound", "Eurofound (Európska nadácia pre zlepšovanie životných a pracovných podmienok)", "Dublin", "Írsko", "výskum životných a pracovných podmienok", None, 0),
    ("eurojust", "Eurojust", "Haag", "Holandsko", "justičná spolupráca v trestných veciach", None, 1),
    ("european-agency-safety-and-health-work-eu-osha", "Európska agentúra pre bezpečnosť a ochranu zdravia pri práci (EU-OSHA)", "Bilbao", "Španielsko", "bezpečnosť a ochrana zdravia pri práci", None, 0),
    ("european-centre-development-vocational-training-cedefop", "Cedefop (Európske stredisko pre rozvoj odborného vzdelávania)", "Solún", "Grécko", "rozvoj odborného vzdelávania a prípravy", None, 0),
    ("european-centre-disease-prevention-and-control-ecdc", "Európske centrum pre prevenciu a kontrolu chorôb (ECDC)", "Štokholm", "Švédsko", "ochrana pred infekčnými chorobami", None, 1),
    ("european-chemicals-agency-echa", "Európska chemická agentúra (ECHA)", "Helsinki", "Fínsko", "bezpečnosť chemických látok", None, 0),
    ("european-cybersecurity-competence-centre-eccc", "Európske centrum kompetencií v oblasti kybernetickej bezpečnosti (ECCC)", "Bukurešť", "Rumunsko", "posilňovanie kapacít Európy v kybernetickej bezpečnosti", None, 0),
    ("european-environment-agency-eea", "Európska environmentálna agentúra (EEA)", "Kodaň", "Dánsko", "informácie o životnom prostredí a klíme", None, 0),
    ("european-fisheries-control-agency-efca", "Európska agentúra pre kontrolu rybárstva (EFCA)", "Vigo", "Španielsko", "dodržiavanie pravidiel spoločnej rybárskej politiky", None, 0),
    ("european-food-safety-authority-efsa", "Európsky úrad pre bezpečnosť potravín (EFSA)", "Parma", "Taliansko", "vedecké poradenstvo o rizikách v potravinovom reťazci", None, 1),
    ("european-institute-gender-equality-eige", "Európsky inštitút pre rodovú rovnosť (EIGE)", "Vilnius", "Litva", "rodová rovnosť", None, 0),
    ("european-institute-innovation-and-technology-eit", "Európsky inovačný a technologický inštitút (EIT)", "Budapešť", "Maďarsko", "podpora inovácií", None, 0),
    ("european-insurance-and-occupational-pensions-authority-eiopa", "Európsky orgán pre poisťovníctvo a dôchodkové poistenie zamestnancov (EIOPA)", "Frankfurt nad Mohanom", "Nemecko", "dohľad nad poisťovníctvom a dôchodkovým poistením", None, 0),
    ("european-investment-bank-eib", "Európska investičná banka (EIB)", "Luxemburg", "Luxembursko", "financovanie projektov, ktoré pomáhajú plniť ciele EÚ", None, 1),
    ("european-labour-authority-ela", "Európsky orgán práce (ELA)", "Bratislava", "Slovensko", "spolupráca krajín pri cezhraničnej mobilite pracovníkov", "811 09 Bratislava", 1),
    ("european-maritime-safety-agency-emsa", "Európska námorná bezpečnostná agentúra (EMSA)", "Lisabon", "Portugalsko", "námorná bezpečnosť a boj proti znečisťovaniu mora", None, 0),
    ("european-medicines-agency-ema", "Európska agentúra pre lieky (EMA)", "Amsterdam", "Holandsko", "vedecké hodnotenie a dohľad nad bezpečnosťou liekov", "1083 HS Amsterdam", 1),
    ("european-ombudsman", "Európsky ombudsman", "Štrasburg", "Francúzsko", "vyšetrovanie sťažností na nesprávny úradný postup inštitúcií EÚ", None, 1),
    ("european-public-prosecutors-office-eppo", "Európska prokuratúra (EPPO)", "Luxemburg", "Luxembursko", "stíhanie trestných činov poškodzujúcich financie EÚ", None, 1),
    ("european-securities-and-markets-authority-esma", "Európsky orgán pre cenné papiere a trhy (ESMA)", "Paríž", "Francúzsko", "ochrana investorov a stabilita finančných trhov", None, 0),
    ("european-training-foundation-etf", "Európska nadácia pre odborné vzdelávanie (ETF)", "Turín", "Taliansko", "rozvoj ľudského kapitálu v susedných krajinách EÚ", None, 0),
    ("european-union-agency-asylum-euaa", "Agentúra Európskej únie pre azyl (EUAA)", "Valletta", "Malta", "podpora krajín pri spoločnom európskom azylovom systéme", None, 0),
    ("european-union-agency-cybersecurity-enisa", "Agentúra Európskej únie pre kybernetickú bezpečnosť (ENISA)", "Atény", "Grécko", "vysoká úroveň kybernetickej bezpečnosti v Európe", None, 1),
    ("european-union-agency-fundamental-rights-fra", "Agentúra Európskej únie pre základné práva (FRA)", "Viedeň", "Rakúsko", "poradenstvo o základných právach", None, 1),
    ("european-union-agency-law-enforcement-training-cepol", "Agentúra EÚ pre odbornú prípravu v oblasti presadzovania práva (CEPOL)", "Budapešť", "Maďarsko", "odborná príprava príslušníkov polície a orgánov presadzovania práva", None, 0),
    ("european-union-agency-operational-management-large-scale-it-systems-area-freedom-security-and", "eu-LISA (agentúra na riadenie rozsiahlych informačných systémov)", "Tallinn", "Estónsko", "riadenie rozsiahlych informačných systémov v oblasti spravodlivosti a vnútra", None, 0),
    ("european-union-agency-railways-era", "Železničná agentúra Európskej únie (ERA)", "Valenciennes", "Francúzsko", "jednotný európsky železničný priestor", "59300 Valenciennes", 0),
    ("european-union-agency-space-programme-euspa", "Agentúra Európskej únie pre vesmírny program (EUSPA)", "Praha", "Česko", "satelitná navigácia Galileo a EGNOS", None, 1),
    ("european-union-aviation-safety-agency-easa", "Agentúra Európskej únie pre bezpečnosť letectva (EASA)", "Kolín", "Nemecko", "bezpečnosť civilného letectva", None, 0),
    ("european-union-drugs-agency-euda", "Agentúra Európskej únie pre drogy (EUDA)", "Lisabon", "Portugalsko", "informácie a varovania o drogách", None, 0),
    ("european-union-institute-security-studies-euiss", "Inštitút Európskej únie pre bezpečnostné štúdie (EUISS)", "Paríž", "Francúzsko", "analýzy zahraničnej, bezpečnostnej a obrannej politiky", None, 0),
    ("european-union-intellectual-property-office-euipo", "Úrad Európskej únie pre duševné vlastníctvo (EUIPO)", "Alicante", "Španielsko", "ochranné známky a dizajny EÚ", None, 0),
    ("european-union-satellite-centre-satcen", "Satelitné stredisko Európskej únie (SatCen)", "Torrejón de Ardoz", "Španielsko", "služby založené na vesmírnych údajoch pre zahraničnú a bezpečnostnú politiku", None, 0),
    ("europol", "Europol", "Haag", "Holandsko", "pomoc polícii v boji proti závažnej medzinárodnej trestnej činnosti a terorizmu", None, 1),
    ("frontex", "Frontex (Európska agentúra pre pohraničnú a pobrežnú stráž)", "Varšava", "Poľsko", "riadenie vonkajších hraníc EÚ", None, 1),
    ("fusion-energy-f4e", "Spoločný podnik Fusion for Energy (F4E)", "Barcelona", "Španielsko", "výskum jadrovej syntézy (projekt ITER)", None, 0),
    ("translation-centre-bodies-european-union-cdt", "Prekladateľské stredisko pre orgány Európskej únie (CdT)", "Luxemburg", "Luxembursko", "preklady pre agentúry a orgány EÚ", None, 0),
    ("single-resolution-board-srb", "Jednotná rada pre riešenie krízových situácií (SRB)", "Brusel", "Belgicko", "riešenie krízových situácií bánk v ťažkostiach", None, 0),
    ("european-defence-agency-eda", "Európska obranná agentúra (EDA)", "Brusel", "Belgicko", "spolupráca na európskych obranných projektoch", None, 0),
    ("publications-office-european-union-op", "Úrad pre vydávanie publikácií Európskej únie", "Luxemburg", "Luxembursko", "vydavateľské služby pre inštitúcie EÚ", None, 0),
    ("euratom-supply-agency-esa", "Zásobovacia agentúra Euratomu (ESA)", "Luxemburg", "Luxembursko", "bezpečné dodávky jadrového materiálu", None, 0),
    ("european-data-protection-supervisor-edps", "Európsky dozorný úradník pre ochranu údajov (EDPS)", "Brusel", "Belgicko", "ochrana osobných údajov v inštitúciách EÚ", None, 0),
    ("european-external-action-service-eeas", "Európska služba pre vonkajšiu činnosť (ESVČ)", "Brusel", "Belgicko", "diplomatické vzťahy EÚ a zahraničná politika", None, 1),
    ("european-personnel-selection-office-epso", "Európsky úrad pre výber pracovníkov (EPSO)", "Brusel", "Belgicko", "výberové konania na zamestnancov inštitúcií EÚ", None, 0),
]

Q = []


def add(kat, n, text, ok, bad, v, src):
    bad = [str(b) for b in bad if str(b) != str(ok)][:2]
    assert len(bad) == 2, (text, ok, bad)
    Q.append({"kat": kat, "n": n, "text": text, "ok": str(ok), "bad": bad, "v": v, "src": [list(s) for s in src]})


rows = []
for slug, name, city, cntry, role, fb, famous in A:
    t = open(os.path.join(CACHE, "eu-inst-" + slug + ".txt"), encoding="utf-8").read()
    t = re.sub(r"[  -​ ]", " ", t)
    m = re.search(r"Sídlo: [^\n]+", t)
    sev = fb if fb else m.group(0).strip()
    u = re.search(r"Úloha: ([^\n]+)", t)
    rok = re.search(r"Rok (?:vzniku|založenia): (\d{4})", t)
    rows.append(dict(slug="eu-inst-" + slug, name=name, city=city, cntry=cntry, role=role, sev=sev,
                     uev=u.group(0).strip() if u else None, rok=int(rok.group(1)) if rok else None,
                     rokev=rok.group(0) if rok else None, famous=famous))

CITIES = sorted({r["city"] for r in rows} | {"Viedeň", "Ľubľana", "Lyon", "Mníchov", "Kodaň"})
cnt = {}
for r in rows:
    cnt[r["city"]] = cnt.get(r["city"], 0) + 1

for r in rows:
    bad = R.sample([c for c in CITIES if c != r["city"]], 2)
    kat = "svk" if r["city"] == "Bratislava" else "ins"
    add(kat, 1 if r["city"] == "Bratislava" else (2 if r["famous"] else 3), f"V ktorom meste sídli {r['name']}?", r["city"], bad,
        f"{r['name']} sídli v meste {r['city']} ({r['cntry']}).", [(r["slug"], r["sev"])])
    if cnt[r["city"]] == 1:
        others = [x for x in rows if x["city"] != r["city"]]
        b = R.sample(others, 2)
        add(kat, 1 if r["city"] == "Bratislava" else (2 if r["famous"] else 3),
            f"Ktorý orgán alebo agentúra EÚ sídli v meste {r['city']} ({r['cntry']})?", r["name"], [x["name"] for x in b],
            f"V meste {r['city']} sídli {r['name']}. {b[0]['name']} sídli v meste {b[0]['city']}, {b[1]['name']} v meste {b[1]['city']}.",
            [(r["slug"], r["sev"])])
    if r["uev"]:
        others = [x for x in rows if x["role"] != r["role"]]
        b = R.sample(others, 2)
        add(kat, 2 if r["famous"] else 3, f"Čím sa zaoberá {r['name']}?", r["role"], [x["role"] for x in b],
            f"Podľa oficiálneho profilu na portáli EÚ: {r['uev'][7:].strip()}", [(r["slug"], r["uev"])])
    if r["rok"] and r["famous"]:
        y = r["rok"]
        add(kat, 3, f"V ktorom roku vznikol {r['name']}?".replace("vznikol Európska", "vznikla Európska").replace("vznikol Agentúra", "vznikla Agentúra"),
            y, [y - 5, y + 4], f"{r['name']} – {r['rokev']} (oficiálny profil na portáli EÚ).", [(r["slug"], r["rokev"])])

json.dump(Q, open(os.path.join(HERE, "gen", "agentury.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("agentury:", len(Q))
