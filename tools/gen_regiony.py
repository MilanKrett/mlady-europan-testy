"""Najvzdialenejšie regióny EÚ (EP informačný list 3.1.7 = ep-fs-100). Výstup: tools/gen/regiony.json"""
import os, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
R = random.Random(9)
Q = []


def add(kat, n, text, ok, bad, v, src):
    bad = [b for b in dict.fromkeys(bad) if b != ok][:2]
    assert len(bad) == 2, text
    Q.append({"kat": kat, "n": n, "text": text, "ok": ok, "bad": bad, "v": v, "src": [list(s) for s in src]})


EVF = ("ep-fs-100", "päť francúzskych zámorských departmánov – Martinik, Mayotte, Guadeloupe, Francúzska Guyana a Réunion")
EVSM = ("ep-fs-100", "jedno francúzske zámorské spoločenstvo – Svätý Martin")
EVP = ("ep-fs-100", "dva portugalské autonómne regióny – Madeira a Azory")
EVS = ("ep-fs-100", "jedno španielske autonómne spoločenstvo – Kanárske ostrovy")
# región, štát, dôkaz, vzdialenosť, rozloha, obyvatelia, HDP, riadok tabuľky
REG = [
    ("Azory", "Portugalsko", EVP, 1548, 2322, 236488, 67, "Azory | 1 548 | 2 322 | 236 488 | 67"),
    ("Kanárske ostrovy", "Španielsko", EVS, 1850, 7447, 2258866, 62, "Kanárske ostrovy | 1 850 (priemer za všetky ostrovy) | 7 447 | 2 258 866 | 62"),
    ("Guadeloupe", "Francúzsko", EVF, 7578, 1685, 413791, 69, "Guadeloupe | 7 578 | 1 685 | 413 791 | 69"),
    ("Francúzska Guyana", "Francúzsko", EVF, 7841, 83751, 291774, 46, "Francúzska Guyana | 7 841 | 83 751 | 291 774 | 46"),
    ("Madeira", "Portugalsko", EVP, 1041, 802, 259440, 69, "Madeira | 1 041 | 802 | 259 440 | 69"),
    ("Martinik", "Francúzsko", EVF, 7641, 1108, 359419, 76, "Martinik | 7 641 | 1 108 | 359 419 | 76"),
    ("Réunion", "Francúzsko", EVF, 9921, 2504, 892102, 68, "Réunion | 9 921 | 2 504 | 892 102 | 68"),
    ("Svätý Martin", "Francúzsko", EVSM, 6700, 86, 32358, None, "Svätý Martin | 6 700 | 86 (francúzska strana 53) | 32 358"),
    ("Mayotte", "Francúzsko", EVF, 8444, 367, 329208, 30, "Mayotte | 8 444 | 367 | 329 208 | 30"),
]
STATES = ["Francúzsko", "Portugalsko", "Španielsko", "Holandsko", "Dánsko", "Taliansko"]
NOT_OR = ["Grónsko", "Korzika", "Sicília", "Baleárske ostrovy", "Faerské ostrovy", "Kréta", "Sardínia", "Svätý Bartolomej"]
for reg, st, ev, *_ in REG:
    add("sta", 2, f"Ktorej krajine EÚ patrí najvzdialenejší región {reg}?", st, [s for s in STATES if s != st][:3],
        f"{reg} patrí krajine {st}. EÚ má deväť najvzdialenejších regiónov: šesť francúzskych, dva portugalské (Madeira, Azory) a jeden španielsky (Kanárske ostrovy).", [ev])
for i, (reg, st, ev, *_) in enumerate(REG):
    bad = R.sample(NOT_OR, 2)
    add("sta", 3, "Ktorý z týchto regiónov je najvzdialenejším regiónom EÚ (ultraperiférnym regiónom)?" + (" " * (i % 3)), reg, bad,
        f"{reg} je jedným z deviatich najvzdialenejších regiónov EÚ; {bad[0]} ani {bad[1]} medzi ne nepatria.",
        [ev, ("ep-fs-100", "V súčasnosti má EÚ deväť najvzdialenejších regiónov:")])
add("sta", 2, "Koľko najvzdialenejších regiónov má v súčasnosti EÚ?", "deväť", ["tri", "dvadsaťsedem"],
    "EÚ má deväť najvzdialenejších regiónov: Martinik, Mayotte, Guadeloupe, Francúzska Guyana, Réunion, Svätý Martin, Madeira, Azory a Kanárske ostrovy.",
    [("ep-fs-100", "V súčasnosti má EÚ deväť najvzdialenejších regiónov:")])
add("sta", 2, "Ktoré tri štáty EÚ majú najvzdialenejšie regióny?", "Francúzsko, Portugalsko a Španielsko",
    ["Dánsko, Holandsko a Francúzsko", "Taliansko, Grécko a Cyprus"], "Najvzdialenejšie regióny majú Francúzsko (6), Portugalsko (2) a Španielsko (1).", [EVF, EVP, EVS])

def ext(key, idx, lab, unit, hi=True):
    rows = [r for r in REG if r[idx] is not None]
    best = max(rows, key=lambda r: r[idx]) if hi else min(rows, key=lambda r: r[idx])
    others = R.sample([r for r in rows if r is not best], 2)
    vals = ", ".join(f"{r[0]} {r[idx]:,}".replace(",", " ") + unit for r in [best] + others)
    add("sta", 3, f"Ktorý z týchto najvzdialenejších regiónov EÚ {lab}?", best[0], [o[0] for o in others],
        f"Podľa údajov EP: {vals.rstrip('.')}.", [("ep-fs-100", best[7])] + [("ep-fs-100", o[7]) for o in others])

for k in range(3):
    ext("pop", 5, "má najviac obyvateľov", " obyv.")
    ext("area", 4, "má najväčšiu rozlohu", " km²")
    ext("dist", 3, "je najďalej od hlavného mesta svojho štátu v kontinentálnej Európe", " km")
add("sta", 3, "Ktorý najvzdialenejší región EÚ má najnižšie HDP na obyvateľa (30 % priemeru EÚ)?", "Mayotte", ["Azory", "Kanárske ostrovy"],
    "Mayotte má HDP na obyvateľa na úrovni 30 % priemeru EÚ, najmenej zo všetkých najvzdialenejších regiónov.", [("ep-fs-100", REG[8][7])])
add("sta", 3, "Ktorý región sa v roku 2014 rozhodnutím Európskej rady stal najvzdialenejším regiónom EÚ?", "Mayotte",
    ["Svätý Bartolomej", "Grónsko"], "Mayotte bolo zámorskou krajinou a územím až do roku 2014, keď sa stalo najvzdialenejším regiónom.",
    [("ep-fs-100", "K opačnej situácii došlo v prípade Mayotte, ktoré bolo zámorskou krajinou a územím až do roku 2014")])
add("sta", 3, "Ktoré územie prestalo byť v roku 2012 najvzdialenejším regiónom EÚ a stalo sa zámorskou krajinou a územím?", "Svätý Bartolomej",
    ["Mayotte", "Madeira"], "Do konca roka 2011 bol Svätý Bartolomej najvzdialenejším regiónom, v roku 2012 sa stal zámorskou krajinou a územím.",
    [("ep-fs-100", "Do konca roka 2011 bol napríklad Svätý Bartolomej najvzdialenejším regiónom EÚ, ale v roku 2012 sa stal zámorskou krajinou a územím.")])
add("sta", 3, "S ktorými štátmi EÚ majú ústavné väzby zámorské krajiny a územia (ZKÚ)?", "s Dánskom, Francúzskom a Holandskom",
    ["so Španielskom a Portugalskom", "s Talianskom a Gréckom"], "Existuje 13 zámorských krajín a území s ústavnými väzbami na Dánsko, Francúzsko a Holandsko.",
    [("ep-fs-100", "Existuje 13 zámorských krajín a území, ktoré majú ústavné väzby na Dánsko, Francúzsko a Holandsko.")])
add("sta", 3, "Sú zámorské krajiny a územia (napr. Grónsko) súčasťou jednotného trhu EÚ?", "nie, na rozdiel od najvzdialenejších regiónov",
    ["áno, rovnako ako najvzdialenejšie regióny", "áno, ale len v roku 2026"], "Zámorské krajiny a územia nie sú súčasťou jednotného trhu; najvzdialenejšie regióny sú integrálnou súčasťou EÚ.",
    [("ep-fs-100", "Zámorské krajiny a územia nie sú súčasťou jednotného trhu")])
add("sta", 3, "V ktorom najvzdialenejšom regióne bola v roku 2020 nezamestnanosť nižšia ako priemer EÚ?", "na Azorách",
    ["na Kanárskych ostrovoch", "na Mayotte"], "Len na Azorách bola miera nezamestnanosti nižšia ako priemer EÚ; na Kanárskych ostrovoch a Mayotte bola viac ako trojnásobná.",
    [("ep-fs-100", "Len na Azorách bola miera nezamestnanosti nižšia ako priemer EÚ")])

json.dump(Q, open(os.path.join(HERE, "gen", "regiony.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("regiony.json:", len(Q))
