"""Voľby do Európskeho parlamentu podľa štátov (EP informačný list 1.3.4 = ep-fs-21). Výstup: tools/gen/volby.json"""
import os, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
R = random.Random(2024)
Q = []


def add(kat, n, text, ok, bad, v, src):
    bad = [b for b in dict.fromkeys(bad) if b != ok][:2]
    assert len(bad) == 2, text
    Q.append({"kat": kat, "n": n, "text": text, "ok": ok, "bad": bad, "v": v, "src": [list(s) for s in src]})


ALL = ["Belgicko", "Bulharsko", "Česko", "Dánsko", "Nemecko", "Estónsko", "Írsko", "Grécko", "Španielsko", "Francúzsko",
       "Chorvátsko", "Taliansko", "Cyprus", "Lotyšsko", "Litva", "Luxembursko", "Maďarsko", "Malta", "Holandsko", "Rakúsko",
       "Poľsko", "Portugalsko", "Rumunsko", "Slovinsko", "Slovensko", "Fínsko", "Švédsko"]
LOC = {"Belgicko": "v Belgicku", "Malta": "na Malte", "Nemecko": "v Nemecku", "Rakúsko": "v Rakúsku", "Grécko": "v Grécku",
       "Bulharsko": "v Bulharsku", "Luxembursko": "v Luxembursku", "Írsko": "v Írsku", "Taliansko": "v Taliansku", "Poľsko": "v Poľsku",
       "Slovensko": "na Slovensku", "Rumunsko": "v Rumunsku", "Cyprus": "na Cypre", "Švédsko": "vo Švédsku", "Francúzsko": "vo Francúzsku",
       "Česko": "v Česku", "Litva": "v Litve", "Lotyšsko": "v Lotyšsku", "Chorvátsko": "v Chorvátsku", "Maďarsko": "v Maďarsku",
       "Estónsko": "v Estónsku", "Holandsko": "v Holandsku", "Španielsko": "v Španielsku", "Dánsko": "v Dánsku", "Portugalsko": "v Portugalsku",
       "Fínsko": "vo Fínsku", "Slovinsko": "v Slovinsku"}

# volebný vek
EV_AGE = ("ep-fs-21", "Vo väčšine členských štátov môžu voliť občania, ktorí dosiahli vek 18 rokov, s výnimkou Belgicka, Malty, Nemecka a Rakúska, kde je táto hranica stanovená na 16 rokov, a Grécka s hranicou 17 rokov.")
V16 = ["Belgicko", "Malta", "Nemecko", "Rakúsko"]
V18 = [c for c in ALL if c not in V16 + ["Grécko"]]
for c in V16:
    add("sta", 2, "V ktorej z týchto krajín môžu vo voľbách do Európskeho parlamentu voliť už 16-roční?", c, R.sample(V18, 2),
        "Voliť od 16 rokov sa dá v Belgicku, na Malte, v Nemecku a Rakúsku; v Grécku od 17, inde od 18 rokov.", [EV_AGE])
    add("sta", 3, f"Od koľkých rokov môžu občania voliť vo voľbách do Európskeho parlamentu {LOC[c]}?", "od 16 rokov",
        ["od 18 rokov", "od 21 rokov", "od 17 rokov"], "Voliť od 16 rokov sa dá v Belgicku, na Malte, v Nemecku a Rakúsku.", [EV_AGE])
add("sta", 3, "Od koľkých rokov môžu občania voliť vo voľbách do Európskeho parlamentu v Grécku?", "od 17 rokov",
    ["od 16 rokov", "od 21 rokov"], "Grécko má pre eurovoľby hranicu 17 rokov; Belgicko, Malta, Nemecko a Rakúsko 16 rokov, ostatné štáty 18.", [EV_AGE])
add("svk", 1, "Od koľkých rokov sa môžu Slováci zúčastniť na voľbách do Európskeho parlamentu ako voliči?", "od 18 rokov",
    ["od 16 rokov", "od 21 rokov"], "Vo väčšine štátov vrátane Slovenska sa volí od 18 rokov.", [EV_AGE])

# povinná účasť
EV_POV = ("ep-fs-21", "Účasť na voľbách je povinná v štyroch členských štátoch (Belgicko, Bulharsko, Luxembursko a Grécko)")
POV = ["Belgicko", "Bulharsko", "Luxembursko", "Grécko"]
NPOV = [c for c in ALL if c not in POV]
for c in POV:
    add("sta", 2, "V ktorej z týchto krajín je účasť na voľbách do Európskeho parlamentu povinná?", c, R.sample(NPOV, 2),
        "Povinná účasť na eurovoľbách platí v Belgicku, Bulharsku, Luxembursku a Grécku.", [EV_POV])
add("sta", 2, "V koľkých členských štátoch je účasť na voľbách do Európskeho parlamentu povinná?", "v štyroch",
    ["v žiadnom", "vo všetkých"], "Povinná účasť platí v štyroch štátoch: Belgicko, Bulharsko, Luxembursko a Grécko.", [EV_POV])
add("svk", 1, "Je účasť na voľbách do Európskeho parlamentu na Slovensku povinná?", "nie, povinná je len v Belgicku, Bulharsku, Luxembursku a Grécku",
    ["áno, pod hrozbou pokuty", "áno, ale len pre študentov"], "Povinná účasť platí iba v štyroch štátoch – Slovensko medzi nimi nie je.", [EV_POV])

# volebné prahy
EV_P5 = ("ep-fs-21", "Francúzsko, Belgicko, Litva, Poľsko, Slovensko, Česko, Rumunsko, Chorvátsko, Lotyšsko a Maďarsko (5 %)")
EV_P4 = ("ep-fs-21", "Rakúsko, Taliansko a Švédsko (4 %)")
EV_P3 = ("ep-fs-21", "Grécko (3 %)")
EV_P18 = ("ep-fs-21", "Cyprus (1,8 %)")
P = {"Slovensko": ("5 %", EV_P5), "Francúzsko": ("5 %", EV_P5), "Poľsko": ("5 %", EV_P5), "Česko": ("5 %", EV_P5),
     "Rakúsko": ("4 %", EV_P4), "Taliansko": ("4 %", EV_P4), "Švédsko": ("4 %", EV_P4), "Grécko": ("3 %", EV_P3), "Cyprus": ("1,8 %", EV_P18)}
for c, (p, ev) in P.items():
    add("svk" if c == "Slovensko" else "sta", 2 if c == "Slovensko" else 3,
        f"Aký volebný prah (minimálny podiel hlasov na získanie kresla) platí vo voľbách do Európskeho parlamentu {LOC[c]}?", p,
        ["5 %", "4 %", "3 %", "1,8 %", "10 %"], f"{c}: prah {p}. Prah 5 % majú napr. Francúzsko, Poľsko či Slovensko, 4 % Rakúsko, Taliansko a Švédsko.", [ev])
EV_NP = ("ep-fs-21", "Ostatné členské štáty neuplatňujú žiadne prahové hodnoty, hoci Nemecko sa o to usilovalo.")
add("sta", 3, "Ktorý súd vyhlásil v rokoch 2011 a 2014 volebné prahy pre eurovoľby vo svojej krajine za protiústavné?", "nemecký ústavný súd",
    ["Súdny dvor EÚ", "francúzska Ústavná rada"], "Nemecký ústavný súd vyhlásil prahy (najprv 5 %, potom 3 %) za protiústavné; v roku 2024 rozhodol, že prah podľa rozhodnutia 2018/994 protiústavný nebude.",
    [("ep-fs-21", "nemecký ústavný súd vyhlásil existujúce prahové hodnoty jednotlivých krajín pre voľby do EÚ (ktoré boli najprv 5 %, potom 3 %) za protiústavné")])
add("ins", 2, "Aký volebný systém musia všetky členské štáty použiť pri voľbách do Európskeho parlamentu?", "systém pomerného zastúpenia",
    ["väčšinový systém", "nepriame voľby v národných parlamentoch"], "Všetky členské štáty musia používať systém založený na pomernom zastúpení.",
    [("ep-fs-21", "Všetky členské štáty musia používať systém založený na pomernom zastúpení.")])

# volebné obvody
EV_OB = ("ep-fs-21", "Štyri členské štáty (Belgicko, Írsko, Taliansko a Poľsko) však rozdelili svoje štátne územie na viacero regionálnych volebných obvodov.")
OB = ["Belgicko", "Írsko", "Taliansko", "Poľsko"]
for c in OB:
    add("sta", 3, "Ktorý z týchto štátov má vo voľbách do Európskeho parlamentu viacero regionálnych volebných obvodov?", c,
        R.sample([x for x in ALL if x not in OB], 2), "Väčšina štátov tvorí jeden volebný obvod; viac regionálnych obvodov majú Belgicko, Írsko, Taliansko a Poľsko.", [EV_OB])
add("svk", 2, "Koľko volebných obvodov má Slovensko vo voľbách do Európskeho parlamentu?", "jeden – celé územie štátu",
    ["osem – podľa krajov", "štyri"], "Väčšina štátov vrátane Slovenska tvorí v eurovoľbách jediný volebný obvod; viac obvodov majú len Belgicko, Írsko, Taliansko a Poľsko.",
    [("ep-fs-21", "V európskych voľbách tvorí väčšina členských štátov jediný volebný obvod."), EV_OB])

# vek kandidáta
EV_K = ("ep-fs-21", "Výnimkou sú Belgicko, Bulharsko, Cyprus, Česko, Estónsko, Írsko, Litva, Lotyšsko, Poľsko a Slovensko (21 rokov), Rumunsko (23 rokov) a Taliansko a Grécko (25 rokov).")
add("svk", 2, "Koľko rokov musí mať najmenej kandidát vo voľbách do Európskeho parlamentu na Slovensku?", "21 rokov",
    ["18 rokov", "25 rokov"], "Minimálny vek kandidáta je vo väčšine štátov 18 rokov; na Slovensku (a napr. v Česku či Poľsku) 21 rokov.", [EV_K])
add("sta", 3, "V ktorej krajine musí mať kandidát do Európskeho parlamentu najmenej 23 rokov?", "Rumunsko",
    ["Taliansko", "Slovensko"], "Rumunsko má hranicu 23 rokov, Taliansko a Grécko 25 rokov, Slovensko 21 rokov.", [EV_K])
for c in ["Taliansko", "Grécko"]:
    add("sta", 3, f"Aký je minimálny vek kandidáta vo voľbách do Európskeho parlamentu {LOC[c]}?", "25 rokov",
        ["18 rokov", "21 rokov"], "Taliansko a Grécko majú najvyššiu hranicu – 25 rokov.", [EV_K])
for c in ["Česko", "Poľsko", "Írsko", "Estónsko"]:
    add("sta", 3, f"Aký je minimálny vek kandidáta vo voľbách do Európskeho parlamentu {LOC[c]}?", "21 rokov",
        ["18 rokov", "25 rokov"], f"{c} patrí medzi štáty s hranicou 21 rokov (spolu so Slovenskom).", [EV_K])
add("ins", 3, "Môže občan kandidovať v tých istých voľbách do Európskeho parlamentu vo viac ako jednom členskom štáte?", "nie, nikto nesmie kandidovať vo viac než jednom štáte",
    ["áno, najviac v dvoch štátoch", "áno, bez obmedzenia"], "Nikto nesmie kandidovať v tých istých voľbách vo viac než jednom členskom štáte (smernica 93/109/ES).",
    [("ep-fs-21", "Nikto nesmie kandidovať v tých istých voľbách vo viac než jednom členskom štáte")])
add("his", 3, "V ktorých eurovoľbách prvýkrát kandidovali hlavní kandidáti (Spitzenkandidaten) na predsedu Komisie?", "v roku 2014",
    ["v roku 1979", "v roku 2004"], "Hlavní kandidáti prvýkrát kandidovali vo voľbách v roku 2014; Parlament potom zvolil Jeana-Clauda Junckera.",
    [("ep-fs-21", "vo voľbách v roku 2014 prvýkrát kandidovali hlavní kandidáti")])
add("his", 2, "Kto bol v roku 2014 ako prvý „hlavný kandidát“ zvolený za predsedu Komisie?", "Jean-Claude Juncker",
    ["José Manuel Barroso", "Ursula von der Leyenová"], "Európsky parlament 22. októbra 2014 zvolil za predsedu Komisie hlavného kandidáta Jeana-Clauda Junckera.",
    [("ep-fs-21", "Nakoniec Európsky parlament 22. októbra 2014 zvolil na základe výsledkov volieb z roku 2014 jedného z týchto kandidátov – Jeana-Clauda Junckera – za predsedu Komisie.")])
add("his", 2, "V ktorom roku sa konali prvé priame voľby do Európskeho parlamentu?", "v roku 1979",
    ["v roku 1957", "v roku 1992"], "Prvé priame voľby sa konali v roku 1979 na základe Aktu o voľbách z 20. septembra 1976.",
    [("ep-fs-21", "Toto ustanovenie implementovala Rada pred prvými priamymi voľbami v roku 1979")])
add("med", 3, "Kedy Komisia navrhla celoeurópsky Kódex postupov proti šíreniu dezinformácií?", "v apríli 2018",
    ["v roku 2004", "v roku 2025"], "V apríli 2018 Komisia vydala oznámenie Boj proti dezinformáciám na internete a navrhla Kódex postupov; v septembri 2018 ho podpísali tri online platformy.",
    [("ep-fs-21", "Komisia v apríli 2018 vydala oznámenie s názvom Boj proti dezinformáciám na internete: európsky prístup a navrhla celoeurópsky Kódex postupov proti šíreniu dezinformácií")])
add("med", 2, "Čo okrem iného žiadal od online platforiem akčný plán EÚ proti dezinformáciám z decembra 2018 pred eurovoľbami?", "vymazávať falošné účty a označovať správy od „botov“",
    ["zrušiť všetky politické reklamy na svete", "zverejniť heslá používateľov"], "Akčný plán vyzval platformy na vymazanie falošných účtov, označovanie správ od botov a spoluprácu s overovateľmi faktov.",
    [("ep-fs-21", "vrátane vymazania falošných účtov, označovania správ doručených prostredníctvom „botov“")])
add("akt", 3, "Kedy bol prijatý záverečný akt prepracovaného nariadenia o štatúte a financovaní európskych politických strán?", "26. novembra 2025",
    ["9. mája 2024", "1. januára 2027"], "Po dlhých rokovaniach bol záverečný akt prijatý 26. novembra 2025.",
    [("ep-fs-21", "záverečný akt bol prijatý 26. novembra 2025")])

json.dump(Q, open(os.path.join(HERE, "gen", "volby.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("volby.json:", len(Q))
