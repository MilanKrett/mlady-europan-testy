"""Finančná gramotnosť: prepočty konverzných kurzov (ECB), inflácia (ECB), odškodnenie cestujúcich (Vaša Európa). Výstup: tools/gen/fin.json"""
import os, json, random
from decimal import Decimal as D

HERE = os.path.dirname(os.path.abspath(__file__))
R = random.Random(2009)
Q = []


def add(kat, n, text, ok, bad, v, src):
    bad = [str(b) for b in bad if str(b) != str(ok)]
    bad = list(dict.fromkeys(bad))[:2]
    assert len(bad) == 2, (text, ok, bad)
    Q.append({"kat": kat, "n": n, "text": text, "ok": str(ok), "bad": bad, "v": v, "src": [list(s) for s in src]})


def sk(x, dec=2):
    """formát čísla po slovensky: medzera ako oddeľovač tisícov, čiarka desatinná"""
    q = D(x).quantize(D(1) / (D(10) ** dec)) if dec else D(x).quantize(D(1))
    s = f"{q:,.{dec}f}" if dec else f"{q:,.0f}"
    return s.replace(",", " ").replace(".", ",")


# kód, kurz (text zo zdroja), genitív meny, krajina, skratka meny po slovensky
RATES = [
    ("BEF", "40,3399", "belgického franku", "Belgicko", "belgických frankov"),
    ("BGN", "1,95583", "bulharského leva", "Bulharsko", "bulharských leva"),
    ("DEM", "1,95583", "nemeckej marky", "Nemecko", "nemeckých mariek"),
    ("EEK", "15,6566", "estónskej koruny", "Estónsko", "estónskych korún"),
    ("IEP", "0,787564", "írskej libry", "Írsko", "írskych libier"),
    ("GRD", "340,750", "gréckej drachmy", "Grécko", "gréckych drachiem"),
    ("ESP", "166,386", "španielskej pesety", "Španielsko", "španielskych pesiet"),
    ("CYP", "0,585274", "cyperskej libry", "Cyprus", "cyperských libier"),
    ("FRF", "6,55957", "francúzskeho franku", "Francúzsko", "francúzskych frankov"),
    ("HRK", "7,53450", "chorvátskej kuny", "Chorvátsko", "chorvátskych kún"),
    ("ITL", "1936,27", "talianskej líry", "Taliansko", "talianskych lír"),
    ("LVL", "0,702804", "lotyšského latsu", "Lotyšsko", "lotyšských latov"),
    ("LTL", "3,45280", "litovského litasu", "Litva", "litovských litasov"),
    ("LUF", "40,3399", "luxemburského franku", "Luxembursko", "luxemburských frankov"),
    ("MTL", "0,429300", "maltskej líry", "Malta", "maltských lír"),
    ("NLG", "2,20371", "holandského guldenu", "Holandsko", "holandských guldenov"),
    ("ATS", "13,7603", "rakúskeho šilingu", "Rakúsko", "rakúskych šilingov"),
    ("PTE", "200,482", "portugalského escuda", "Portugalsko", "portugalských escúd"),
    ("SIT", "239,640", "slovinského tolara", "Slovinsko", "slovinských tolarov"),
    ("FIM", "5,94573", "fínskej marky", "Fínsko", "fínskych mariek"),
]
for code, rate, gen, cntry, plur in RATES:
    r = D(rate.replace(",", "."))
    ev = ("ecb-euro-map", f"{rate} {code} ({gen})")
    k = R.choice([10, 20, 50, 100, 200, 500, 1000])
    amount = r * k
    dec = 2 if amount < 100000 else 0
    amount_txt = sk(amount, dec)
    if amount_txt.endswith(",00"):
        amount_txt = amount_txt[:-3]
    if D(amount_txt.replace(" ", "").replace(",", ".")) != amount.quantize(D(1) / (D(10) ** dec)):
        continue
    add("fin", 2, f"Koľko eur zodpovedá sume {amount_txt} {code} ({plur}) podľa neodvolateľného konverzného kurzu eura?",
        f"{k} €", [f"{k * 10} €", f"{k // 10 if k >= 20 else k * 2} €", f"{k * 2} €"],
        f"Konverzný kurz bol 1 € = {rate} {code}. {amount_txt} : {rate} = {k} €.", [ev])
    # opačný prepočet
    k2 = R.choice([5, 10, 25, 40, 100])
    res = r * k2
    ok = sk(res, 2 if res < 1000 else 0) if (res * 100) % 1 == 0 or res >= 1000 else sk(res, 2)
    wrong1 = sk(r * k2 * 10, 2 if res < 100 else 0)
    wrong2 = sk((r * k2) / 10, 2)
    add("fin", 3, f"Koľko {plur} by ste dostali za {k2} € podľa neodvolateľného konverzného kurzu ({cntry})?",
        f"{ok} {code}", [f"{wrong1} {code}", f"{wrong2} {code}"],
        f"1 € = {rate} {code}, teda {k2} × {rate} = {ok} {code}.", [ev])

EVI = ("ecb-inflation", "na úrovni 2 % v strednodobom horizonte")
# inflácia – výpočty
for price, pct in [(100, 2), (50, 4), (200, 3), (80, 5), (1000, 2), (250, 10), (40, 25), (300, 7)]:
    new = D(price) * (1 + D(pct) / 100)
    add("fin", 1 if pct in (2, 10) else 2, f"Košík tovarov stál pred rokom {price} €. Ročná miera inflácie bola {pct} %. Koľko stojí rovnaký košík dnes?",
        f"{sk(new)} €", [f"{sk(D(price) * (1 - D(pct) / 100))} €", f"{sk(D(price) + D(pct) * 10)} €", f"{sk(D(price) * (1 + D(pct) / 10))} €"],
        f"{price} € × (1 + {pct}/100) = {sk(new)} €. Ročnú mieru inflácie získame porovnaním ceny košíka s cenou v rovnakom mesiaci pred rokom.",
        [("ecb-inflation", "Porovnaním celkovej ceny koša v určitom mesiaci s jeho cenou v rovnakom mesiaci pred rokom získame ročnú mieru inflácie.")])
for old, new in [(100, 103), (50, 51), (200, 210), (40, 42), (500, 520), (80, 84)]:
    pct = (D(new) - D(old)) / D(old) * 100
    add("fin", 2, f"Cena košíka tovarov vzrástla za rok z {old} € na {new} €. Aká bola ročná miera inflácie?",
        f"{sk(pct, 0)} %", [f"{sk(D(new) - D(old), 0)} %", f"{sk(pct * 2, 0)} %", f"{sk(pct + 5, 0)} %", f"{sk(pct * 10, 0)} %"],
        f"({new} − {old}) : {old} × 100 = {sk(pct, 0)} %.",
        [("ecb-inflation", "Porovnaním celkovej ceny koša v určitom mesiaci s jeho cenou v rovnakom mesiaci pred rokom získame ročnú mieru inflácie.")])
add("fin", 2, "Ktorý z týchto výrokov o inflácii je správny?", "pri inflácii si za jedno euro kúpite menej ako predtým",
    ["pri inflácii si za jedno euro kúpite viac ako predtým", "inflácia znamená rast ceny jedného konkrétneho výrobku"],
    "Inflácia je všeobecný rast cien – za jedno euro sa dá kúpiť menej ako včera; inflácia znižuje hodnotu meny v čase.",
    [("ecb-inflation", "To znamená, že za jedno euro sa toho dá dnes kúpiť menej ako včera.")])
add("fin", 3, "Máte na účte 1 000 € s úrokom 1 % ročne a inflácia je 3 %. Čo sa stane s reálnou hodnotou vašich peňazí po roku?",
    "klesne – kúpite si za ne menej ako pred rokom", ["stúpne o 1 %", "nezmení sa"],
    "Úrok 1 % nevyrovná infláciu 3 %: na účte bude 1 010 €, ale ceny vzrastú o 3 %, takže reálna hodnota klesne (približne o 2 %).",
    [("ecb-inflation", "Inými slovami, inflácia znižuje hodnotu meny v priebehu času.")])

# odškodnenie cestujúcich v leteckej doprave
FL = [("1 500 km alebo menej", 250, 1200), ("od 1 500 km do 3 500 km", 400, 2800), ("viac ako 3 500 km", 600, 5000)]
EVA = ("ye-air", "Odškodnenie – odmietnutie nástupu do lietadla | Suma v EUR | Vzdialenosť | 250 | 1 500 km alebo menej | 400 | Nad 1 500 km v rámci EÚ a všetky ostatné lety od 1 500 km do 3 500 km | 600 | Viac ako 3 500 km")
for desc, amt, km in FL:
    add("fin", 2, f"Aké odškodnenie vám podľa pravidiel EÚ patrí, ak vám bol odmietnutý nástup na let dlhý {km} km (prišli ste včas a máte doklady)?",
        f"{amt} €", [f"{a} €" for _, a, _ in FL if a != amt] + ["1 000 €"],
        f"Pri odmietnutí nástupu je odškodnenie podľa vzdialenosti: 250 € (do 1 500 km), 400 € (1 500 – 3 500 km), 600 € (nad 3 500 km). Let {km} km → {amt} €.", [EVA])
    add("fin", 3, f"Rodina so 4 cestujúcimi nesmela nastúpiť na let dlhý {km} km. Aké celkové odškodnenie jej podľa pravidiel EÚ patrí?",
        f"{amt * 4} €", [f"{amt} €", f"{amt * 2} €", f"{(amt + 150) * 4} €"],
        f"Každý cestujúci má nárok na {amt} €, spolu 4 × {amt} = {amt * 4} €.", [EVA])
add("fin", 3, "O koľko percent môže letecká spoločnosť znížiť odškodnenie, ak vám ponúkne presmerovanie a priletíte len s malým meškaním?",
    "o 50 %", ["o 10 %", "o 100 %"], "Ak priletíte s meškaním po presmerovaní v stanovených limitoch, odškodnenie možno znížiť o 50 % (napr. 125 € namiesto 250 €).",
    [("ye-air", "možno vaše odškodnenie znížiť o 50 %")])

json.dump(Q, open(os.path.join(HERE, "gen", "fin.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("fin.json:", len(Q))
