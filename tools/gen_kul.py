"""Európske hlavné mestá kultúry, Sacharovova cena, Európske roky. Výstup: tools/gen/kul.json"""
import os, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
R = random.Random(77)
Q = []


def add(kat, n, text, ok, bad, v, src):
    bad = [str(b) for b in bad if str(b) != str(ok)]
    bad = list(dict.fromkeys(bad))[:2]
    assert len(bad) == 2, (text, ok, bad)
    Q.append({"kat": kat, "n": n, "text": text, "ok": str(ok), "bad": bad, "v": v, "src": [list(s) for s in src]})


# ---------- Európske hlavné mestá kultúry (EHMK) ----------
# rok: (riadok miest v zdroji, riadok krajín v zdroji, [(mesto SK, krajina SK, známe 0/1)])
E = {
    1985: ("Athens", "1985 European Capital of Culture in Greece", [("Atény", "Grécko", 1)]),
    1986: ("Florence", "1986 European Capital of Culture in Italy", [("Florencia", "Taliansko", 1)]),
    1987: ("Amsterdam", "1987 European Capital of Culture in the Netherlands", [("Amsterdam", "Holandsko", 1)]),
    1988: ("West Berlin", "1988 European Capital of Culture in Germany", [("Západný Berlín", "Nemecko", 1)]),
    1989: ("Paris", "1989 European Capital of Culture in France", [("Paríž", "Francúzsko", 1)]),
    1990: ("Glasgow", "1990 European Capital of Culture in the United Kingdom", [("Glasgow", "Spojené kráľovstvo", 0)]),
    1991: ("Dublin", "1991 European Capital of Culture in Ireland", [("Dublin", "Írsko", 1)]),
    1992: ("Madrid", "1992 European Capital of Culture in Spain", [("Madrid", "Španielsko", 1)]),
    1993: ("Antwerp", "1993 European Capital of Culture in Belgium", [("Antverpy", "Belgicko", 0)]),
    1994: ("Lisbon", "1994 European Capital of Culture in Portugal", [("Lisabon", "Portugalsko", 1)]),
    1995: ("Luxembourg", "1995 European Capital of Culture in Luxembourg", [("Luxemburg", "Luxembursko", 1)]),
    1996: ("Copenhagen", "1996 European Capital of Culture in Denmark", [("Kodaň", "Dánsko", 1)]),
    1997: ("Thessaloniki", "1997 European Capital of Culture in Greece", [("Solún", "Grécko", 0)]),
    1998: ("Stockholm", "1998 European Capital of Culture in Sweden", [("Štokholm", "Švédsko", 1)]),
    1999: ("Weimar", "1999 European Capital of Culture in Germany", [("Weimar", "Nemecko", 0)]),
    2000: ("Avignon, Bergen, Bologna, Brussels, Helsinki, Kraków, Prague, Reykjavík and Santiago de Compostela",
           "2000 European Capitals of Culture in France, Norway, Italy, Belgium, Finland, Poland, Czech Republic, Iceland and Spain",
           [("Avignon", "Francúzsko", 0), ("Bergen", "Nórsko", 0), ("Bologna", "Taliansko", 0), ("Brusel", "Belgicko", 1),
            ("Helsinki", "Fínsko", 1), ("Krakov", "Poľsko", 1), ("Praha", "Česko", 1), ("Reykjavík", "Island", 1),
            ("Santiago de Compostela", "Španielsko", 0)]),
    2001: ("Porto and Rotterdam", "2001 European Capitals of Culture in Portugal and the Netherlands", [("Porto", "Portugalsko", 0), ("Rotterdam", "Holandsko", 0)]),
    2002: ("Bruges and Salamanca", "2002 European Capitals of Culture in Belgium and Spain", [("Bruggy", "Belgicko", 0), ("Salamanca", "Španielsko", 0)]),
    2003: ("Graz", "2003 European Capital of Culture in Austria", [("Graz", "Rakúsko", 0)]),
    2004: ("Genoa and Lille", "2004 European Capitals of Culture in Italy and France", [("Janov", "Taliansko", 0), ("Lille", "Francúzsko", 0)]),
    2005: ("Cork", "2005 European Capital of Culture in Ireland", [("Cork", "Írsko", 0)]),
    2006: ("Patras", "2006 European Capital of Culture in Greece", [("Patra", "Grécko", 0)]),
    2007: ("Luxembourg and Sibiu", "2007 European Capitals of Culture in Luxembourg and Romania", [("Luxemburg", "Luxembursko", 1), ("Sibiu", "Rumunsko", 0)]),
    2008: ("Liverpool and Stavanger", "2008 European Capitals of Culture in the United Kingdom and Norway", [("Liverpool", "Spojené kráľovstvo", 0), ("Stavanger", "Nórsko", 0)]),
    2009: ("Linz and Vilnius", "2009 European Capitals of Culture in Austria and Lithuania", [("Linz", "Rakúsko", 0), ("Vilnius", "Litva", 1)]),
    2010: ("Essen, Pécs and Istanbul", "2010 European Capitals of Culture in Germany, Hungary and Turkey", [("Essen", "Nemecko", 0), ("Pécs", "Maďarsko", 0), ("Istanbul", "Turecko", 1)]),
    2011: ("Tallinn and Turku", "2011 European Capitals of Culture in Estonia and Finland", [("Tallinn", "Estónsko", 1), ("Turku", "Fínsko", 0)]),
    2012: ("Guimarães and Maribor", "2012 European Capitals of Culture in Portugal and Slovenia", [("Guimarães", "Portugalsko", 0), ("Maribor", "Slovinsko", 1)]),
    2013: ("Košice and Marseille-Provence", "2013 European Capitals of Culture in Slovakia and France", [("Košice", "Slovensko", 1), ("Marseille", "Francúzsko", 1)]),
    2014: ("Riga and Umeå", "2014 European Capitals of Culture in Latvia and Sweden", [("Riga", "Lotyšsko", 1), ("Umeå", "Švédsko", 0)]),
    2015: ("Mons and Plzeň", "2015 European Capitals of Culture in Belgium and the Czech Republic", [("Mons", "Belgicko", 0), ("Plzeň", "Česko", 1)]),
    2016: ("Donostia-San Sebastián and Wrocław", "2016 European Capitals of Culture in Spain and Poland", [("San Sebastián", "Španielsko", 0), ("Vroclav", "Poľsko", 1)]),
    2017: ("Aarhus and Pafos", "2017 European Capitals of Culture in Denmark and Cyprus", [("Aarhus", "Dánsko", 0), ("Pafos", "Cyprus", 0)]),
    2018: ("Leeuwarden and Valletta", "2018 European Capitals of Culture in the Netherlands and Malta", [("Leeuwarden", "Holandsko", 0), ("Valletta", "Malta", 1)]),
    2019: ("Matera and Plovdiv", "2019 European Capitals of Culture in Italy and Bulgaria", [("Matera", "Taliansko", 0), ("Plovdiv", "Bulharsko", 0)]),
    2020: ("Galway and Rijeka", "2020 European Capitals of Culture in Ireland and Croatia", [("Galway", "Írsko", 0), ("Rijeka", "Chorvátsko", 0)]),
    2022: ("Esch, Kaunas and Novi Sad", "2022 European Capitals of Culture in Luxembourg, Lithuania and Serbia", [("Esch-sur-Alzette", "Luxembursko", 0), ("Kaunas", "Litva", 0), ("Novi Sad", "Srbsko", 0)]),
    2023: ("Elefsina, Timișoara and Veszprém", None, [("Elefsina", None, 0), ("Temešvár", None, 0), ("Veszprém", None, 0)]),
    2024: ("Bad Ischl, Bodø and Tartu", "2024 European Capitals of Culture in Austria, Norway (EFTA/EEA country) and Estonia", [("Bad Ischl", "Rakúsko", 0), ("Bodø", "Nórsko", 0), ("Tartu", "Estónsko", 0)]),
    2025: ("Chemnitz and Nova Gorica", "2025 European Capitals of Culture in Germany and Slovenia", [("Chemnitz", "Nemecko", 0), ("Nova Gorica", "Slovinsko", 0)]),
    2026: ("Oulu and Trenčín", "2026 European Capitals of Culture in Finland and Slovakia", [("Oulu", "Fínsko", 1), ("Trenčín", "Slovensko", 1)]),
    2027: ("Liepāja and Évora", "2027 European Capitals of Culture in Latvia and Portugal", [("Liepāja", "Lotyšsko", 0), ("Évora", "Portugalsko", 0)]),
    2028: ("České Budějovice, Bourges and Skopje", "2028 European Capitals of Culture in Czechia, France and North Macedonia", [("České Budějovice", "Česko", 1), ("Bourges", "Francúzsko", 0), ("Skopje", "Severné Macedónsko", 0)]),
    2029: ("Lublin and Kiruna", "2029 European Capitals of Culture in Poland and Sweden", [("Lublin", "Poľsko", 0), ("Kiruna", "Švédsko", 0)]),
    2030: ("Leuven, Larnaka and Nikšić", "2030 European Capitals of Culture in Belgium, Cyprus and Montenegro", [("Leuven", "Belgicko", 0), ("Larnaka", "Cyprus", 0), ("Nikšić", "Čierna Hora", 0)]),
}
EC = "ecoc-node-335"
cities = [(y, c, k, f) for y, (_, _, L) in E.items() for (c, k, f) in L]
allc = sorted({c for _, c, _, _ in cities})
years = sorted(E)


def bolo(y):
    return "bolo" if y < 2026 else ("je" if y == 2026 else "bude")


def kat_for(c, y):
    if c in ("Košice", "Trenčín"):
        return "svk"
    if y == 2026:
        return "akt"
    return "kul"


def ev(y):
    line, cl, _ = E[y]
    return f"{y} {line}" + (f" {cl}" if cl else "")


for y, c, k, f in cities:
    if y == 2000 and not f:
        continue
    same = {x for (yy, x, _, _) in cities if yy == y}
    bad = R.sample([x for x in allc if x not in same and x != c], 2)
    n = 1 if f and y >= 2010 else (2 if f else 3)
    add(kat_for(c, y), n, f"Ktoré z týchto miest {bolo(y)} Európskym hlavným mestom kultúry v roku {y}?", c, bad,
        f"V roku {y} {'boli' if len(E[y][2]) > 1 and y < 2026 else ('sú' if len(E[y][2]) > 1 and y == 2026 else ('budú' if len(E[y][2]) > 1 else bolo(y)))} Európskym hlavným mestom kultúry: {', '.join(x for x, _, _ in E[y][2])}.",
        [(EC, ev(y))])
    if c != "Luxemburg":
        i = years.index(y)
        near = [z for z in years[max(0, i - 4):i + 5] if z != y]
        b = R.sample(near, 2)
        add(kat_for(c, y), 2 if f else 3, f"V ktorom roku {bolo(y)} mesto {c} Európskym hlavným mestom kultúry?", y, b,
            f"Mesto {c} {bolo(y)} Európskym hlavným mestom kultúry v roku {y}.", [(EC, ev(y))])
    if k and not f:
        ks = sorted({kk for (_, _, kk, _) in cities if kk and kk != k})
        add(kat_for(c, y), 3, f"V ktorej krajine leží mesto {c}, Európske hlavné mesto kultúry v roku {y}?", k, R.sample(ks, 2),
            f"{c} ({k}) {bolo(y)} Európskym hlavným mestom kultúry v roku {y}.", [(EC, ev(y))])

add("kul", 2, "Od ktorého roku existuje iniciatíva Európske hlavné mesto kultúry?", 1985, [1975, 1993],
    "Iniciatíva Európske hlavné mesto kultúry vznikla v roku 1985 (prvým mestom boli Atény).",
    [("ecoc", "The initiative was developed in 1985"), (EC, "1985 Athens 1985 European Capital of Culture in Greece")])
add("kul", 3, "Ako sa volá cena, ktorú môže Európska komisia vyplatiť úspešnému Európskemu hlavnému mestu kultúry?", "Cena Meliny Mercouriovej",
    ["Cena Altiera Spinelliho", "Cena Karola Veľkého"],
    "Ide o Cenu Meliny Mercouriovej (Melina Mercouri Prize), v súčasnosti 1,5 mil. eur z programu Kreatívna Európa.",
    [("ecoc", "Melina Mercouri Prize (currently €1.5m funded from the EU Creative Europe programme)")])
add("kul", 3, "Z ktorého programu EÚ sa financuje Cena Meliny Mercouriovej pre Európske hlavné mestá kultúry?", "Kreatívna Európa",
    ["Erasmus+", "Horizont Európa"], "Cena Meliny Mercouriovej (1,5 mil. eur) sa financuje z programu Kreatívna Európa.",
    [("ecoc", "Melina Mercouri Prize (currently €1.5m funded from the EU Creative Europe programme)")])
add("kul", 3, "Koľko rokov pred rokom, v ktorom mesto nesie titul, sa Európske hlavné mesto kultúry formálne určí?", "štyri roky",
    ["jeden rok", "desať rokov"], "Európske hlavné mestá kultúry sa formálne určujú štyri roky pred samotným rokom titulu.",
    [("ecoc", "European Capitals of Culture are formally designated four years before the actual title year")])
add("kul", 3, "Kto formálne určí mesto za Európske hlavné mesto kultúry v členskom štáte EÚ?", "príslušný orgán daného členského štátu na odporúčanie poroty",
    ["Európsky parlament hlasovaním v pléne", "Rada Európy"],
    "Nezávislá porota odporučí jedno mesto za každú hostiteľskú krajinu a príslušný orgán členského štátu ho formálne určí.",
    [("ecoc", "The relevant authority in the Member State concerned then formally designates the recommended city as European Capital of Culture")])
add("akt", 2, "Ktoré dve krajiny budú mať Európske hlavné mesto kultúry v roku 2031?", "Malta a Španielsko", ["Bulharsko a Dánsko", "Grécko a Írsko"],
    "V roku 2031 budú tento titul niesť mestá z Malty a zo Španielska; súťaže o rok 2032 prebiehajú v Bulharsku a Dánsku.",
    [(EC, "2031 European Capitals of Culture in Malta and Spain")])
add("akt", 3, "Ktoré dve krajiny budú mať Európske hlavné mesto kultúry v roku 2032?", "Bulharsko a Dánsko", ["Malta a Španielsko", "Slovensko a Fínsko"],
    "V roku 2032 budú mať Európske hlavné mesto kultúry Bulharsko a Dánsko (súťaže sa začali v decembri 2025).",
    [(EC, "one in Bulgaria: competition started in December 2025 one in Denmark: competition started in December 2025")])
add("akt", 3, "Kedy Európska komisia predložila návrh nového právneho rámca pre Európske hlavné mestá kultúry na roky 2034 – 2047?", "v septembri 2026",
    ["v januári 2024", "v máji 2025"], "Komisia predložila návrh nového právneho rámca na obdobie 2034 – 2047 v septembri 2026.",
    [("ecoc", "The European Commission put forward its proposal for the new legal framework for the period between 2034 and 2047 in September 2026")])
add("kul", 3, "Ktoré z týchto miest mimo EÚ získalo titul Európske hlavné mesto kultúry pre rok 2030?", "Nikšić (Čierna Hora)",
    ["Skopje (Severné Macedónsko)", "Novi Sad (Srbsko)"],
    "Pre rok 2030 je určené čiernohorské mesto Nikšić; Skopje má titul v roku 2028 a Novi Sad ho mal v roku 2022.",
    [(EC, "Nikšić in Montenegro"), (EC, "2030 Leuven, Larnaka and Nikšić")])

# ---------- Sacharovova cena ----------
S = [  # rok, laureát, krajina/None, dôkaz, známe
    (1988, "Nelson Mandela", "Južná Afrika", "Nelson Rolihlahla Mandela – 1988, Južná Afrika", 1),
    (1988, "Anatolij Marčenko", "Rusko", "Anatolij Marčenko (in memoriam) – 1988, Rusko", 0),
    (1989, "Alexander Dubček", "Slovensko", "Alexander Dubček – 1989, Slovensko", 1),
    (1990, "Aun Schan Su Ťij", "Mjanmarsko", "Aun Schan Su Ťij – 1990, Mjanmarsko", 1),
    (1991, "Adem Demaçi", "Kosovo", "Adem Demaçi – 1991, Kosovo", 0),
    (1992, "Las Madres de Plaza de Mayo (Matky z Májového námestia)", "Argentína", "Las Madres de Plaza de Mayo – 1992, Argentína", 0),
    (1993, "denník Oslobođenje", "Bosna a Hercegovina", "Oslobođenje – 1993, Bosna a Hercegovina", 0),
    (1994, "Taslima Nasrin", "Bangladéš", "Taslima Nasrin – 1994, Bangladéš", 0),
    (1995, "Leyla Zana", "Turecko", "Leyla Zana – 1995, Turecko", 0),
    (1996, "Wej Ťing-šeng", "Čína", "Wej Ťing-šeng – 1996, Čína", 0),
    (1997, "Salíma Ghazálí", "Alžírsko", "Salíma Ghazálí – 1997, Alžírsko", 0),
    (1998, "Ibrahim Rugova", "Kosovo", "Ibrahim Rugova – 1998, Kosovo", 0),
    (1999, "Xanana Gusmão", "Východný Timor", "Xanana Gusmão – 1999, Východný Timor", 0),
    (2000, "¡Basta Ya!", "Španielsko", "¡Basta Ya! – 2000, Španielsko", 0),
    (2001, "Dom Zacarias Kamwenho", "Angola", "Dom Zacarias Kamwenho – 2001, Angola", 0),
    (2002, "Oswaldo José Payá Sardiñas", "Kuba", "Oswaldo José Payá Sardiñas – 2002, Kuba", 0),
    (2003, "Kofi Annan a pracovníci Organizácie Spojených národov", None, "Kofi Annan a pracovníci Organizácie Spojených národov – 2003", 1),
    (2004, "Bieloruské združenie novinárov", "Bielorusko", "Bieloruské združenie novinárov – 2004, Bielorusko", 0),
    (2005, "Reportéri bez hraníc", None, "Reportéri bez hraníc – 2005, sídlo vo Francúzsku", 1),
    (2006, "Alexander Milinkievič", "Bielorusko", "Alexander Milinkievič – 2006, Bielorusko", 0),
    (2007, "Sálih Mahmúd Muhammad Usmán", "Sudán", "Sálih Mahmúd Muhammad Usmán – 2007, Sudán", 0),
    (2008, "Chu Ťia", "Čína", "Chu Ťia – 2008, Čína", 0),
    (2009, "Memorial", "Rusko", "Memorial – 2009, Rusko", 0),
    (2010, "Guillermo Fariñas", "Kuba", "Guillermo Fariñas – 2010, Kuba", 0),
    (2012, "Džaafar Panáhí", "Irán", "Džaafar Panáhí – 2012, Irán", 0),
    (2013, "Malála Júsafzaj", "Pakistan", "Malála Júsafzaj – 2013, Pakistan", 1),
    (2014, "Denis Mukwege", "Konžská demokratická republika", "Denis Mukwege – 2014, Konžská demokratická republika", 0),
    (2015, "Rá´if Badawí", "Saudská Arábia", "Rá´if Badawí – 2015, Saudská Arábia", 0),
    (2016, "Nádja Murád a Lamjá´ Hadží Bašár", "Irak", "Nádja Murád a Lamjá´ Hadží Bašár – 2016, Irak", 0),
    (2017, "demokratická opozícia vo Venezuele", None, "Demokratická opozícia vo Venezuele – 2017", 0),
    (2018, "Oleg Sencov", "Ukrajina", "Oleg Sencov – 2018, Ukrajina", 1),
    (2019, "Ilham Tohti", "Čína", "Ilham Tohti – 2019, Čína", 0),
    (2020, "demokratická opozícia v Bielorusku", None, "Demokratická opozícia v Bielorusku- 2020, Bielorusko", 0),
    (2021, "Alexej Navaľný", "Rusko", "Alexej Navaľný - 2021, Rusko", 1),
    (2022, "statočný ľud Ukrajiny", None, "Sacharovova cena EP za slobodu myslenia za rok 2022 sa udeľuje ukrajinskému ľudu", 1),
    (2023, "Žína Mahsa Amíní a hnutie Žena, život, sloboda", None, "Žína Mahsa Amíní a iránske hnutie Žena, život, sloboda – laureáti Sacharovovej ceny za rok 2023", 1),
    (2024, "María Corina Machado a Edmundo González Urrutia", None, "María Corina Machado a nový prezident Edmundo González Urrutia – laureáti Sacharovovej ceny za rok 2024", 1),
    (2025, "Andrzej Poczobut a Mzia Amaglobeli", None, "Andrzej Poczobut a Mzia Amaglobeli – laureáti Sacharovovej ceny za rok 2025", 1),
    (2026, "Medzinárodný trestný súd (ICC) a jeho predstavitelia", None, "International Criminal Court and its officials – 2026 Sakharov Prize laureate", 1),
]


def sslug(y):
    return "sak-1988-2000" if y <= 2000 else ("sak-2001-2010" if y <= 2010 else ("sak-2011-2020" if y <= 2020 else "sak-2021-2030"))


names = [s[1] for s in S]
used_years = set()
for y, name, k, evd, f in S:
    kat = "svk" if k == "Slovensko" else ("akt" if y >= 2025 else "kul")
    if y not in used_years:
        used_years.add(y)
        other = [x for (yy, x, _, _, _) in S if yy != y]
        add(kat, 1 if (f and y >= 2020) else (2 if f else 3), f"Komu udelil Európsky parlament Sacharovovu cenu za slobodu myslenia za rok {y}?", name,
            R.sample(other, 2), f"Sacharovovu cenu za rok {y} získal(i): {name}.", [(sslug(y), evd)])
    if f or y % 3 == 0:
        ys = sorted({s[0] for s in S})
        i = ys.index(y)
        b = R.sample([z for z in ys[max(0, i - 4):i + 5] if z != y], 2)
        add(kat, 2 if f else 3, f"Za ktorý rok získal(i) Sacharovovu cenu za slobodu myslenia: {name}?", y, b,
            f"{name} – Sacharovova cena za rok {y}.", [(sslug(y), evd)])
    if k and k != "Slovensko":
        ks = sorted({s[2] for s in S if s[2] and s[2] != k})
        add(kat, 2 if f else 3, f"S ktorou krajinou je spojený laureát Sacharovovej ceny {name} ({y})?", k, R.sample(ks, 2),
            f"{name} získal(a) Sacharovovu cenu v roku {y}; podľa EP: {k}.", [(sslug(y), evd)])

add("svk", 1, "Ktorý Slovák získal Sacharovovu cenu za slobodu myslenia?", "Alexander Dubček", ["Václav Havel", "Milan Rastislav Štefánik"],
    "Alexander Dubček, vedúca osobnosť Pražskej jari, získal Sacharovovu cenu v roku 1989.",
    [("sak-1988-2000", "Alexander Dubček – 1989, Slovensko ... Alexander Dubček, vedúca osobnosť Pražskej jari")])
add("svk", 2, "Akou udalosťou je známy laureát Sacharovovej ceny z roku 1989 Alexander Dubček?", "bol vedúcou osobnosťou Pražskej jari",
    ["bol prvým prezidentom Slovenskej republiky", "podpísal prístupovú zmluvu Slovenska k EÚ"],
    "Podľa EP sa Alexander Dubček ako vedúca osobnosť Pražskej jari usiloval o demokratické a hospodárske reformy.",
    [("sak-1988-2000", "Alexander Dubček, vedúca osobnosť Pražskej jari, sa usiloval presadiť demokratické a hospodárske reformy")])
F = [
    ("Kto udeľuje Sacharovovu cenu za slobodu myslenia?", "Európsky parlament", ["Európska komisia", "Rada Európy"], 1,
     "Sacharovovu cenu udeľuje Európsky parlament.", ("sak-faq", "Európsky parlament udeľuje cenu tým, ktorí tak ako Sacharov zasvätili svoje životy nenásilnému boju za ľudské práva")),
    ("Po kom je pomenovaná Sacharovova cena?", "po sovietskom vedcovi a disidentovi Andrejovi Sacharovovi", ["po ruskom spisovateľovi Alexandrovi Solženicynovi", "po zakladateľovi Červeného kríža Henrim Dunantovi"], 1,
     "Cena nesie meno sovietskeho vedca, disidenta a laureáta Nobelovej ceny za mier Andreja Sacharova (1921 – 1989).", ("sak-faq", "Cena je pomenovaná po sovietskom vedcovi, disidentovi a laureátovi Nobelovej ceny za mier Andrejovi Sacharovovi (1921 - 1989)")),
    ("Aká vysoká je peňažná odmena spojená so Sacharovovou cenou?", "50 000 eur", ["10 000 eur", "1 milión eur"], 2,
     "Peňažná odmena Sacharovovej ceny je 50 000 eur.", ("sak-faq", "Peňažná odmena je 50 000 EUR.")),
    ("Koľko poslancov EP musí najmenej podporiť kandidáta na Sacharovovu cenu, ak ho nenavrhuje politická skupina?", "40", ["10", "100"], 3,
     "Kandidátov navrhujú politické skupiny alebo skupina minimálne 40 poslancov EP; poslanec môže podporiť iba jedného kandidáta.", ("sak-faq", "Kandidátov na Sacharovovu cenu navrhujú politické skupiny alebo skupina minimálne 40 poslancov EP")),
    ("Koľkých kandidátov na Sacharovovu cenu môže podporiť jeden poslanec EP?", "iba jedného", ["najviac troch", "neobmedzený počet"], 3,
     "Každý poslanec môže podporiť iba jedného kandidáta.", ("sak-faq", "Poslanec môže podporiť iba jedného kandidáta.")),
    ("V ktorom mesiaci sa laureát Sacharovovej ceny zvyčajne vyhlasuje?", "v októbri", ["v máji", "v januári"], 2,
     "Nominácie sa podávajú v septembri a víťaz sa zvyčajne vyhlasuje v októbri.", ("sak-how", "Víťaz sa zvyčajne vyhlasuje v októbri.")),
    ("Kto v Európskom parlamente rozhoduje v záverečnom hlasovaní o laureátovi Sacharovovej ceny?", "Konferencia predsedov", ["plénum všetkých 720 poslancov", "Výbor pre kultúru a vzdelávanie"], 3,
     "Výbor pre zahraničné veci a Výbor pre rozvoj zostavia užší výber troch kandidátov a laureáta vyberie Konferencia predsedov.", ("sak-how", "Ďalej sa zostaví užší výber troch kandidátov a predloží sa Konferencii predsedov na záverečné hlasovanie")),
    ("Ktoré výbory Európskeho parlamentu posudzujú nominácie na Sacharovovu cenu?", "Výbor pre zahraničné veci a Výbor pre rozvoj", ["Výbor pre právne veci a Výbor pre petície", "Výbor pre rozpočet a Výbor pre kontrolu rozpočtu"], 3,
     "Nominácie sa posudzujú na spoločnej schôdzi Výboru pre zahraničné veci a Výboru pre rozvoj.", ("sak-how", "posudzujú na spoločnej schôdzi Výboru pre zahraničné veci a Výboru pre rozvoj")),
    ("Ktorú cenu získal Andrej Sacharov v roku 1975?", "Nobelovu cenu za mier", ["Nobelovu cenu za fyziku", "Pulitzerovu cenu"], 2,
     "Ruský fyzik Andrej Sacharov získal v roku 1975 Nobelovu cenu za mier.", ("sak-andrei", "Ruský fyzik Andrej Dmitrijevič Sacharov (1921 - 1989), ktorý v roku 1975 získal Nobelovu cenu za mier")),
    ("Čím sa Andrej Sacharov najprv preslávil?", "ako tvorca sovietskej vodíkovej bomby", ["ako prvý človek vo vesmíre", "ako autor románu Súostrovie Gulag"], 3,
     "Andrej Sacharov sa najprv preslávil ako tvorca sovietskej vodíkovej bomby, neskôr sa stal obhajcom ľudských práv.", ("sak-andrei", "sa najprv preslávil ako tvorca sovietskej vodíkovej bomby")),
    ("Kam poslali sovietske orgány Andreja Sacharova do exilu?", "do Gorkého", ["na Sibír do Norilska", "do Kyjeva"], 3,
     "Sovietske orgány poslali Sacharova do exilu v Gorkom, aby obmedzili jeho kontakty s cudzincami.", ("sak-andrei", "Sovietske orgány poslali Andreja Sacharova do exilu v Gorkom")),
    ("Ktorá laureátka Sacharovovej ceny si ju mohla osobne prevziať až o 23 rokov neskôr, v roku 2013?", "Aun Schan Su Ťij", ["Malála Júsafzaj", "Leyla Zana"], 3,
     "Aun Schan Su Ťij bola v čase udelenia ceny (1990) v domácom väzení a cenu si prevzala až 22. októbra 2013.", ("sak-1988-2000", "Sacharovovu cenu si mohla prísť prevziať osobne až o 23 rokov neskôr – 22. októbra 2013")),
    ("Ktorého laureáta Sacharovovej ceny nominoval na cenu sám Andrej Sacharov?", "Anatolija Marčenka", ["Nelsona Mandelu", "Alexandra Dubčeka"], 3,
     "Anatolij Marčenko, sovietsky disident, dostal cenu in memoriam v roku 1988; nominoval ho sám Andrej Sacharov.", ("sak-1988-2000", "Na cenu ho nominoval sám Andrej Sacharov.")),
    ("Akú inštitúciu ocenil Európsky parlament Sacharovovou cenou za rok 2026?", "Medzinárodný trestný súd a jeho predstaviteľov", ["Medzinárodný súdny dvor OSN", "Európsky súd pre ľudské práva"], 1,
     "Sacharovova cena za rok 2026 bola udelená Medzinárodnému trestnému súdu (ICC) a jeho predstaviteľom so sídlom v Haagu.", ("sak-2021-2030", "the 2026 Sakharov Prize for Freedom of Thought to the International Criminal Court (ICC) and its officials")),
    ("Ktoré povolanie spája laureátov Sacharovovej ceny za rok 2025 Andrzeja Poczobuta a Mziu Amaglobeliovú?", "sú to uväznení novinári", ["sú to lekári v vojnových zónach", "sú to opoziční prezidentskí kandidáti"], 2,
     "Cenu za rok 2025 získali uväznení novinári Andrzej Poczobut z Bieloruska a Mzia Amaglobeli z Gruzínska.", ("sak-2021-2030", "udelená Andrzejovi Poczobutovi z Bieloruska a Mzii Amaglobeliovej z Gruzínska")),
    ("Z ktorých krajín pochádzajú laureáti Sacharovovej ceny za rok 2025?", "z Bieloruska a Gruzínska", ["z Ruska a Ukrajiny", "z Iránu a Afganistanu"], 2,
     "Andrzej Poczobut je z Bieloruska a Mzia Amaglobeli z Gruzínska.", ("sak-2021-2030", "udelená Andrzejovi Poczobutovi z Bieloruska a Mzii Amaglobeliovej z Gruzínska")),
]
for t, ok, bad, n, v, s in F:
    add("kul" if "2025" not in t and "2026" not in t else "akt", n, t, ok, bad, v, [s])
add("med", 2, "Ktorá medzinárodná mimovládna organizácia bojujúca za slobodu informácií získala Sacharovovu cenu v roku 2005?", "Reportéri bez hraníc",
    ["Amnesty International", "Lekári bez hraníc"], "Reportéri bez hraníc (RSF) bojujú za slobodu informácií a prejavu a podporujú prenasledovaných novinárov.",
    [("sak-2001-2010", "Reportéri bez hraníc – 2005, sídlo vo Francúzsku")])

# ---------- Európske roky ----------
Y = [("2023 – 2024", "Európsky rok zručností"), ("2022", "Európsky rok mládeže"), ("2021", "Európsky rok železníc"),
     ("2018", "Európsky rok kultúrneho dedičstva"), ("2015", "Európsky rok rozvoja"), ("2013 – 2014", "Európsky rok občanov")]
for yr, name in Y:
    b = R.sample([x for _, x in Y if x != name], 2)
    add("sym", 2 if yr in ("2022", "2021", "2023 – 2024") else 3, f"Aký Európsky rok vyhlásila EÚ na obdobie {yr}?", name, b,
        f"Obdobie {yr} bolo {name}.", [("eu-symbol-european-years", f"{yr} – {name}")])
add("sym", 3, "Od ktorého roku sa vyhlasujú Európske roky?", 1983, [1957, 1999], "Európske roky sa vyhlasujú od roku 1983 a nemusia sa vyhlasovať každý rok.",
    [("eu-symbol-european-years", "Európske roky sa vyhlasujú od roku 1983")])
add("sym", 3, "Kto navrhuje tému Európskeho roka?", "Európska komisia", ["Európsky parlament", "Výbor regiónov"],
    "Tému navrhuje Európska komisia a schvaľuje ju Európsky parlament a krajiny EÚ.",
    [("eu-symbol-european-years", "Tému konkrétneho Európskeho roka navrhuje Európska komisia a schvaľuje ju Európsky parlament a krajiny EÚ")])
add("sym", 2, "V ktorom Európskom roku sa mladí ľudia zúčastnili na viac ako 13 000 aktivitách v 67 krajinách?", "Európsky rok mládeže 2022",
    ["Európsky rok zručností 2023 – 2024", "Európsky rok občanov 2013 – 2014"], "Počas Európskeho roka mládeže 2022 sa mladí zúčastnili na viac ako 13 000 aktivitách v 67 krajinách.",
    [("eu-symbol-european-years", "2022 – Európsky rok mládeže Mladí ľudia sa zúčastnili na viac ako 13 000 aktivitách v 67 krajinách")])
add("sym", 3, "S akým cieľom EÚ spojila Európsky rok železníc 2021?", "upriamiť pozornosť na úlohu železníc pri dosahovaní klimatickej neutrality do roku 2050",
    ["osláviť 100 rokov od prvého vlaku cez Alpy", "zaviesť jednotný cestovný lístok platný v celej EÚ"],
    "Európsky rok železníc upriamil pozornosť na kľúčovú úlohu železníc pri dosahovaní klimatickej neutrality do roku 2050.",
    [("eu-symbol-european-years", "kľúčovú úlohu pri dosahovaní klimatickej neutrality do roku 2050")])

json.dump(Q, open(os.path.join(HERE, "gen", "kul.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
from collections import Counter
print("kul.json:", len(Q), Counter(q["kat"] for q in Q))
