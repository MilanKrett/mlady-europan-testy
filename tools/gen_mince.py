"""Národné strany euromincí krajín eurozóny (ECB: zdroje-cache/ecb-coins-XX). Výstup: tools/gen/mince.json"""
import os, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
R = random.Random(33)
Q = []


def add(kat, n, text, ok, bad, v, src):
    bad = [b for b in dict.fromkeys(bad) if b != ok][:2]
    assert len(bad) == 2, text
    Q.append({"kat": kat, "n": n, "text": text, "ok": ok, "bad": bad, "v": v, "src": [list(s) for s in src]})


ST = {"at": "Rakúsko", "be": "Belgicko", "bg": "Bulharsko", "cy": "Cyprus", "de": "Nemecko", "ee": "Estónsko",
      "es": "Španielsko", "fi": "Fínsko", "fr": "Francúzsko", "gr": "Grécko", "hr": "Chorvátsko", "ie": "Írsko",
      "it": "Taliansko", "lt": "Litva", "lu": "Luxembursko", "lv": "Lotyšsko", "mt": "Malta", "nl": "Holandsko",
      "pt": "Portugalsko", "si": "Slovinsko", "sk": "Slovensko"}
GEN = {"Rakúsko": "rakúskych", "Belgicko": "belgických", "Bulharsko": "bulharských", "Cyprus": "cyperských", "Nemecko": "nemeckých",
       "Estónsko": "estónskych", "Španielsko": "španielskych", "Fínsko": "fínskych", "Francúzsko": "francúzskych", "Grécko": "gréckych",
       "Chorvátsko": "chorvátskych", "Írsko": "írskych", "Taliansko": "talianskych", "Litva": "litovských", "Luxembursko": "luxemburských",
       "Lotyšsko": "lotyšských", "Malta": "maltských", "Holandsko": "holandských", "Portugalsko": "portugalských", "Slovinsko": "slovinských"}

# (krajina, minca/mince, motív, dôkaz, náročnosť, skupina konfliktu)
M = [
    ("at", "2 €", "pacifistka Bertha von Suttnerová", "portrét pacifistky Berthy von Suttnerovej", 3, None),
    ("at", "1 €", "skladateľ Wolfgang Amadeus Mozart", "Portrét Wolfganga Amadea Mozarta", 2, None),
    ("at", "20 centov", "palác Belvedere", "Palác Belvedere zobrazený na tejto minci", 3, None),
    ("at", "10 centov", "katedrála sv. Štefana vo Viedni", "Námetom tejto mince je katedrála sv. Štefana", 3, None),
    ("at", "5 centov", "alpská prvosienka", "Alpská prvosienka znázornená na tejto minci", 3, "kvet"),
    ("at", "1 cent", "horec", "Horec znázornený na tejto minci", 3, "kvet"),
    ("be", "všetky mince (tretia séria, 2014)", "kráľ Philippe", "V roku 2014 Belgicko vydalo tretiu sériu mincí, na ktorých je zobrazený kráľ Philippe", 3, "panovnik"),
    ("bg", "2 €", "svätý Paisij Chilendarský", "Minca 2 € nesie portrét svätého Paisija Chilendarského", 3, None),
    ("bg", "1 €", "svätý Ivan Rilský", "Na minci 1 € je vyobrazený Ivan Rilský", 3, None),
    ("bg", "centových mincí", "Madarský jazdec (skalný reliéf z 8. storočia)", "skalný reliéf Madarského jazdca z 8. storočia", 3, None),
    ("cy", "1 € a 2 €", "modla v tvare kríža z doby medenej", "Mince 1 € a 2 € zobrazujú modlu v tvare kríža z doby medenej", 3, None),
    ("cy", "10, 20 a 50 centov", "kyrénska obchodná loď", "Na minciach 10, 20 a 50 centov sa nachádza kyrénska obchodná loď", 3, "lod"),
    ("cy", "1, 2 a 5 centov", "muflón", "Mince 1 cent, 2 centy a 5 centov nesú motív muflóna", 3, None),
    ("de", "1 € a 2 €", "orlica", "Na minciach 1 € a 2 € je zobrazená orlica, tradičný symbol nemeckej zvrchovanosti", 2, None),
    ("de", "10, 20 a 50 centov", "Brandenburská brána", "Na minciach 10, 20 a 50 centov je zobrazená Brandenburská brána", 2, None),
    ("de", "1, 2 a 5 centov", "dubová vetvička", "Na minciach 1 cent, 2 centy a 5 centov je zobrazená dubová vetvička", 3, None),
    ("ee", "všetkých mincí", "geografický motív (obrys) krajiny a slovo „Eesti“", "Znázorňuje geografický motív Estónska a slovo „Eesti“ (Estónsko).", 3, "mapa"),
    ("es", "1 € a 2 € (prvá a druhá séria)", "kráľ Juan Carlos I.", "Mince prvej a druhej série nesú portrét kráľa Juana Carlosa I.", 2, "panovnik"),
    ("es", "10, 20 a 50 centov", "spisovateľ Miguel de Cervantes", "portrét otca španielskej literatúry Miguela de Cervantesa", 2, None),
    ("es", "1, 2 a 5 centov", "katedrála v Santiago de Compostela", "Na minciach 1 cent, 2 centy a 5 centov je znázornená katedrála v Santiago de Compostela", 3, None),
    ("fi", "2 €", "plody a kvety moruše", "Plody a kvety moruše zobrazené na tejto minci", 3, None),
    ("fi", "1 €", "dve letiace labute", "Autorom motívu dvoch letiacich labutí na tejto minci je Pertti Mäkinen.", 3, None),
    ("fi", "centových mincí", "heraldický lev", "je zobrazený heraldický lev, ktorý je reprodukciou diela sochára Heikkiho Häiväoju", 3, None),
    ("fr", "1 € a 2 € (prvá séria)", "strom symbolizujúci život, kontinuitu a rast", "Mince zobrazujú strom, ktorý symbolizuje život, kontinuitu a rast.", 3, None),
    ("fr", "10, 20 a 50 centov (prvá séria)", "rozsievačka", "Znázorňujú rozsievačku – postavu často zobrazovanú na francúzskom franku.", 3, "rozsievac"),
    ("fr", "1, 2 a 5 centov", "mladá Marianne", "Mince 1 cent, 2 centy a 5 centov zobrazujú portrét mladej Marianne", 2, None),
    ("fr", "50 centov (nová séria 2024)", "vedkyňa Marie Curie Skłodowská", "Mince zobrazujú portrét nositeľky Nobelovej ceny za vedu Marie Curie Skłodowskej", 2, None),
    ("fr", "20 centov (druhá séria 2024)", "speváčka a tanečnica Josephine Bakerová", "Mince zobrazujú portrét Josephine Bakerovej, speváčky, tanečníčky a bojovníčky za občianske práva.", 3, None),
    ("gr", "2 €", "únos Európy Diom premeneným na býka", "na ktorej Zeus prevtelený do býka unáša Európu", 2, None),
    ("gr", "1 €", "sova zo starovekej aténskej tetradrachmy", "Sova zobrazená na tejto minci je prevzatá zo starovekej aténskej tetradrachmy", 2, None),
    ("gr", "50 centov", "politik Eleftherios Venizelos", "Portrét na tejto minci patrí Eleftheriosovi Venizelosovi", 3, None),
    ("gr", "20 centov", "diplomat Ioannis Capodistrias", "Táto minca je venovaná Ioannisovi Capodistriasovi", 3, None),
    ("gr", "10 centov", "osvietenec Rigas Fereos", "Rigas Fereos (Velestinlis) (1757 – 1798), zobrazený na tejto minci", 3, None),
    ("gr", "5 centov", "moderný tanker", "Na tejto minci je zobrazený moderný tanker", 3, "lod"),
    ("gr", "2 centy", "korveta z vojny za nezávislosť", "Korveta znázornená na tejto minci bola používaná počas gréckej vojny za nezávislosť", 3, "lod"),
    ("gr", "1 cent", "aténska triéra", "Tento motív zobrazuje model aténskej triéry", 3, "lod"),
    ("hr", "2 €", "mapa krajiny so šachovnicovým vzorom", "Na minci 2 € je zobrazená mapa Chorvátska so šachovnicovým vzorom na pozadí.", 3, "mapa"),
    ("hr", "1 €", "kuna (malý cicavec)", "Na minci 1 € je zobrazená kuna so šachovnicovým vzorom na pozadí.", 2, None),
    ("hr", "10, 20 a 50 centov", "vynálezca Nikola Tesla", "portrét vynálezcu a inžiniera Nikolu Teslu", 2, None),
    ("hr", "1, 2 a 5 centov", "písmená „HR“ v hlaholike", "sú vyobrazené písmená „HR“ napísané hranatým písmom v hlaholike", 3, None),
    ("ie", "všetkých mincí", "keltská harfa", "Je na nich keltská harfa ako tradičný národný symbol Írska.", 2, None),
    ("it", "2 €", "básnik Dante Alighieri", "Na tejto minci je portrét Danteho Alighieriho od Raphaëla", 2, None),
    ("it", "1 €", "kresba ideálnych proporcií ľudského tela od Leonarda da Vinciho", "Na minci je známa kresba od Leonarda da Vinciho zobrazujúca ideálne proporcie ľudského tela.", 2, None),
    ("it", "50 centov", "jazdecká socha cisára Marka Aurélia", "Na tejto minci je zobrazená socha cisára Marka Aurélia na koni.", 3, None),
    ("it", "10 centov", "Botticelliho Zrodenie Venuše", "„Zrodenie Venuše“ od Sandra Botticelliho", 3, None),
    ("it", "5 centov", "Koloseum (Fláviov amfiteáter)", "Na tejto minci je vyobrazený Fláviov amfiteáter (Koloseum).", 2, None),
    ("it", "2 centy", "veža Mole Antonelliana", "Na minci je zobrazená veža Mole Antonelliana", 3, None),
    ("it", "1 cent", "hrad Castel del Monte", "Na tejto minci je znázornený hrad Castel del Monte.", 3, None),
    ("lt", "všetkých mincí", "štátny znak Vytis (jazdec)", "je zobrazený štátny znak Litovskej republiky, Vytis", 3, "znak"),
    ("lu", "všetkých mincí", "veľkovojvoda Henri", "Všetky luxemburské mince nesú portrét Jeho kráľovského veličenstva veľkovojvodu Henriho.", 3, "panovnik"),
    ("lv", "1 € a 2 €", "lotyšské sedliacke dievča", "lotyšské sedliacke dievča", 3, None),
    ("mt", "1 € a 2 €", "osemcípy kríž – emblém Maltézskeho rádu", "Hlavným motívom mincí 1 € a 2 € je emblém Maltézskeho rádu.", 3, None),
    ("mt", "1, 2 a 5 centov", "oltár z prehistorického chrámu Mnajdra", "je zobrazený oltár z prehistorického chrámu Mnajdra", 3, None),
    ("nl", "všetky mince (druhá séria, 2014)", "kráľ Willem-Alexander", "Na minciach druhej série, uvedenej do obehu v roku 2014, je zobrazený kráľ Willem-Alexander", 3, "panovnik"),
    ("pt", "1 € a 2 €", "portugalské hrady a erby", "Na minciach 1 € a 2 € sú zobrazené portugalské hrady a erby, obklopené hviezdami EÚ.", 3, None),
    ("pt", "10, 20 a 50 centov", "kráľovská pečať z roku 1142", "V strede mincí 10, 20 a 50 centov je kráľovská pečať z roku 1142.", 3, None),
    ("si", "2 €", "básnik France Prešeren", "Na tejto minci je portrét básnika Franceho Prešerena", 3, None),
    ("si", "1 €", "Primož Trubar, autor prvej slovinskej knihy", "Na tejto minci je portrét Primoža Trubara, autora prvej knihy vydanej v slovinčine.", 3, None),
    ("si", "50 centov", "vrch Triglav", "Táto minca zobrazuje vrch Triglav.", 2, None),
    ("si", "20 centov", "lipicanské kone", "Táto minca zobrazuje lipicanské kone.", 3, None),
    ("si", "5 centov", "rozsievač", "Táto minca nesie motív rozsievača.", 3, "rozsievac"),
    ("si", "1 cent", "bocian", "Táto minca znázorňuje bociana.", 3, None),
]
EURO = [c for c in ST if c != "sk"]
for i, (c, nom, mot, ev, n, grp) in enumerate(M):
    st = ST[c]
    conflict = {x[0] for x in M if grp and x[5] == grp}
    pool = [ST[x] for x in EURO if x != c and x not in conflict]
    bad = R.sample(pool, 2)
    add("sta", n, f"Na národnej strane euromincí ktorej krajiny je motív „{mot}“ – {nom}?", st, bad,
        f"Na {GEN[st]} minciach – {nom} – je motív: {mot.rstrip('.')}. Zdroj: ECB.", [(f"ecb-coins-{c}", ev)])
    other = [x for x in M if x[0] != c and not (grp and x[5] == grp)]
    bads = [x[2] for x in R.sample(other, 2)]
    add("sta", 3, f"Čo je zobrazené na národnej strane {GEN[st]} euromincí – {nom}?", mot, bads,
        f"{st}: {nom} – {mot.rstrip('.')}. Ostatné možnosti sú motívy mincí iných krajín.", [(f"ecb-coins-{c}", ev)])

EDGE = [
    ("hr", "O LIJEPA O DRAGA O SLATKA SLOBODO („Ó, krásna, vzácna, sladká sloboda“)", "Nápis na hrane mince 2 €: „O LIJEPA O DRAGA O SLATKA SLOBODO”"),
    ("lt", "LAISVĖ * VIENYBĖ * GEROVĖ (Sloboda, Jednota, Blahobyt)", "Nápis na hrane mince 2 €: LAISVĖ * VIENYBĖ * GEROVĖ *"),
    ("nl", "GOD * ZIJ * MET * ONS (Boh s nami)", "Nápis na hrane mince 2 € oboch sérií: GOD * ZIJ * MET * ONS * (Boh s nami)."),
    ("fi", "SUOMI FINLAND", "Nápis na hrane mince 2 €: SUOMI FINLAND ***"),
]
for c, txt, ev in EDGE:
    st = ST[c]
    bad = R.sample([ST[x] for x in EURO if x != c], 2)
    add("sta", 3, f"Na hrane 2 € mince ktorej krajiny je nápis {txt}?", st, bad,
        f"Nápis {txt} je na hrane 2 € mince – {st}.", [(f"ecb-coins-{c}", ev)])

json.dump(Q, open(os.path.join(HERE, "gen", "mince.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(Q), "otázok")
