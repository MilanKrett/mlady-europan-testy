"""Načíta otázky z otazky/*.txt (+ generované z gen/*.json), overí dôkazy v zdroje-cache a zostaví data/otazky.json.

Formát bloku (bloky oddelené prázdnym riadkom):
    @ins 2                      (voliteľné: kategória a náročnosť 1-3; inak #kat/#n z hlavičky súboru)
    Text otázky (aj viac riadkov)
    + správna odpoveď
    - nesprávna odpoveď
    - nesprávna odpoveď
    = Vysvetlenie.
    > slug-zdroja | doslovný úryvok zo zdroja ... ďalší úryvok
    ! img/cesta/k/obrazku.jpg    (voliteľné)

Použitie: python -I -X utf8 qparse.py [--build]
"""
import os, re, sys, json, glob, hashlib, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(os.path.dirname(ROOT), "zdroje-cache")
QDIR = os.path.join(ROOT, "otazky")
GENDIR = os.path.join(ROOT, "tools", "gen")

KAT = {
    # kľúč: (názov, počet v teste, body za otázku) – podľa § 18 vyhlášky 9/2009 Z. z. (40 otázok, 100 bodov)
    "ins": ("Inštitúcie, právo a politiky EÚ", 8, 3),
    "akt": ("Aktuálne témy 2025 – 2026", 2, 3),
    "sta": ("Členské štáty a geografia", 8, 2),
    "obr": ("Obrázky: osobnosti, logá a pamiatky", 4, 4),
    "sym": ("Symboly, hodnoty a práva občanov", 1, 2),
    "svk": ("Slovensko v EÚ", 3, 2),
    "med": ("Mediálna a digitálna gramotnosť", 2, 1),
    "fin": ("Finančná gramotnosť a logika", 2, 1),
    "his": ("História EÚ a Európy", 8, 3),
    "kul": ("Kultúra, osobnosti a ocenenia", 2, 1),
}

_src_cache = {}
_index = None


def norm(s):
    s = unicodedata.normalize("NFC", s)
    s = s.replace("­", "").replace(" ", " ").replace(" ", " ")
    for ch in "„“”\"«»‚‘’'`´":
        s = s.replace(ch, "'")
    for ch in "–—‑−":
        s = s.replace(ch, "-")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def src_text(slug):
    if slug not in _src_cache:
        p = os.path.join(CACHE, slug + ".txt")
        if not os.path.exists(p):
            _src_cache[slug] = None
        else:
            _src_cache[slug] = norm(open(p, encoding="utf-8").read())
    return _src_cache[slug]


def src_url(slug):
    global _index
    if _index is None:
        _index = json.load(open(os.path.join(CACHE, "_index.json"), encoding="utf-8"))
    m = _index.get(slug)
    return m["url"] if m else None


def parse_file(path):
    txt = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    kat, n = None, 2
    out, errs = [], []
    for bi, block in enumerate(re.split(r"\n\s*\n", txt)):
        lines = [l.rstrip() for l in block.split("\n") if l.strip() and not l.lstrip().startswith("//")]
        if not lines:
            continue
        hdr = [l for l in lines if l.startswith("#")]
        for h in hdr:
            m = re.match(r"#kat\s+(\w+)", h)
            if m: kat = m.group(1)
            m = re.match(r"#n\s+(\d)", h)
            if m: n = int(m.group(1))
        lines = [l for l in lines if not l.startswith("#")]
        if not lines:
            continue
        q = {"kat": kat, "n": n, "text": [], "ok": None, "bad": [], "v": "", "src": [], "img": None,
             "file": os.path.basename(path), "blok": bi + 1}
        for l in lines:
            if l.startswith("@"):
                p = l[1:].split()
                q["kat"] = p[0]
                if len(p) > 1: q["n"] = int(p[1])
            elif l.startswith("+ "):
                q["ok"] = l[2:].strip()
            elif l.startswith("- "):
                q["bad"].append(l[2:].strip())
            elif l.startswith("= "):
                q["v"] += (" " if q["v"] else "") + l[2:].strip()
            elif l.startswith("> "):
                slug, _, ev = l[2:].partition("|")
                q["src"].append((slug.strip(), ev.strip()))
            elif l.startswith("! "):
                q["img"] = l[2:].strip()
            else:
                if q["ok"] is not None:
                    errs.append(f"{q['file']}#{bi+1}: text za odpoveďami: {l[:60]}")
                q["text"].append(l.strip())
        q["text"] = " ".join(q["text"])
        out.append(q)
    return out, errs


def check(q):
    e = []
    w = f"{q['file']}#{q['blok']} [{q['text'][:50]}]"
    if q["kat"] not in KAT: e.append(f"{w}: zlá kategória {q['kat']}")
    if q["n"] not in (1, 2, 3): e.append(f"{w}: zlá náročnosť")
    if not q["text"]: e.append(f"{w}: chýba text")
    if not q["ok"]: e.append(f"{w}: chýba správna odpoveď")
    if len(q["bad"]) != 2: e.append(f"{w}: treba presne 2 nesprávne odpovede, je {len(q['bad'])}")
    opts = [q["ok"]] + q["bad"]
    if len(set(norm(o) for o in opts if o)) != len(opts): e.append(f"{w}: rovnaké odpovede")
    if not q["v"]: e.append(f"{w}: chýba vysvetlenie")
    if not q["src"]: e.append(f"{w}: chýba zdroj")
    for slug, ev in q["src"]:
        t = src_text(slug)
        if t is None:
            e.append(f"{w}: neznámy zdroj {slug}")
            continue
        if not ev:
            e.append(f"{w}: chýba dôkaz pre {slug}")
            continue
        for part in ev.split("..."):
            part = part.strip()
            if part and norm(part) not in t:
                e.append(f"{w}: dôkaz sa nenašiel v {slug}: «{part[:90]}»")
    if q["img"] and not os.path.exists(os.path.join(ROOT, q["img"])):
        e.append(f"{w}: chýba obrázok {q['img']}")
    return e


def load_all():
    qs, errs = [], []
    for p in sorted(glob.glob(os.path.join(QDIR, "*.txt"))):
        a, b = parse_file(p)
        qs += a; errs += b
    for p in sorted(x for x in glob.glob(os.path.join(GENDIR, "*.json")) if not os.path.basename(x).startswith("_")):
        for i, g in enumerate(json.load(open(p, encoding="utf-8"))):
            g.setdefault("file", os.path.basename(p)); g.setdefault("blok", i + 1); g.setdefault("img", None)
            g["src"] = [tuple(s) for s in g["src"]]
            qs.append(g)
    # varianty tej istej otázky s rovnakou správnou odpoveďou (líšia sa len nesprávnymi možnosťami) – necháme prvú
    seen, uniq = set(), []
    for q in qs:
        k = qid(q)
        if k not in seen:
            seen.add(k); uniq.append(q)
    return uniq, errs


def qid(q):
    return hashlib.sha1(norm(q["text"] + "|" + q["ok"] + "|" + (q.get("img") or "")).encode()).hexdigest()[:8]


def main():
    qs, errs = load_all()
    for q in qs:
        errs += check(q)
    seen = {}
    for q in qs:
        k = norm(q["text"]) + "|" + "|".join(sorted(norm(o or "") for o in [q["ok"]] + q["bad"])) + "|" + str(q.get("img"))
        if k in seen:
            errs.append(f"{q['file']}#{q['blok']}: duplicitná otázka s {seen[k]}: {q['text'][:60]}")
        seen[k] = f"{q['file']}#{q['blok']}"
    from collections import Counter
    c = Counter(q["kat"] for q in qs)
    nd = Counter((q["kat"], q["n"]) for q in qs)
    print("Spolu otázok:", len(qs))
    for k, (name, cnt, pts) in KAT.items():
        cil = 75 * cnt
        print(f"  {k} {name:40s} {c.get(k,0):5d} / {cil}   (n1 {nd.get((k,1),0)}, n2 {nd.get((k,2),0)}, n3 {nd.get((k,3),0)})")
    if errs:
        print(f"\nCHYBY ({len(errs)}):")
        for e in errs[:300]:
            print(" ", e)
    if "--build" in sys.argv:
        if errs:
            print("Build zrušený kvôli chybám."); sys.exit(1)
        build(qs)


def make_tests(qs, count=1000, seed=2026):
    """1000 pevných testov: z každej kategórie presný počet otázok (KAT), otázky sa v rámci kategórie striedajú
    rovnomerne (každá príde na rad približne rovnako často), náročnosť je v každom teste premiešaná a v jednom
    teste nie sú dve otázky k rovnakému faktu (rovnaký dôkaz) ani s rovnakým obrázkom."""
    import random
    from collections import deque
    rnd = random.Random(seed)
    facts = [{(s, norm(e)) for s, e in q["src"]} for q in qs]
    pools = {}
    for k in KAT:
        lv = {n: [i for i, q in enumerate(qs) if q["kat"] == k and q["n"] == n] for n in (1, 2, 3)}
        for v in lv.values():
            rnd.shuffle(v)
        tot = sum(len(v) for v in lv.values())
        order, acc = [], {n: 0.0 for n in lv}
        # prekladanie úrovní v pomere ich veľkosti
        while len(order) < tot:
            for n in lv:
                acc[n] += len(lv[n]) / tot
            n = max((n for n in lv if lv[n]), key=lambda n: acc[n])
            acc[n] -= 1
            order.append(lv[n].pop())
        pools[k] = deque(order)
    tests = []
    for t in range(count):
        chosen, used_f, used_img = [], set(), set()
        for k, (_, cnt, _) in KAT.items():
            pool, skipped, got = pools[k], [], 0
            guard = 0
            while got < cnt and guard < 5 * len(pool) + 10:
                guard += 1
                i = pool.popleft()
                img = qs[i].get("img")
                if (facts[i] & used_f) or (img and img in used_img) or i in chosen:
                    skipped.append(i)
                    pool.append(i) if len(skipped) > len(pool) else None
                    continue
                chosen.append(i); used_f |= facts[i]; got += 1
                if img:
                    used_img.add(img)
                pool.append(i)  # na koniec radu – príde znova na rad až po ostatných
            for i in reversed(skipped):
                if i in pool:
                    pool.remove(i)
                pool.appendleft(i)
            assert got == cnt, (t, k)
        tests.append(chosen)
    return tests


def build(qs):
    out = []
    for q in qs:
        h = int(hashlib.sha1(norm(q["text"] + "|" + q["ok"] + "|" + (q.get("img") or "")).encode()).hexdigest(), 16)
        opts = [q["ok"]] + q["bad"]
        pos = h % 3  # pozícia správnej odpovede
        bad = q["bad"] if (h >> 4) % 2 == 0 else q["bad"][::-1]
        arr = bad[:]
        arr.insert(pos, q["ok"])
        srcs = []
        for slug, _ in q["src"]:
            u = src_url(slug)
            if u and u not in srcs: srcs.append(u)
        out.append({"id": qid(q), "k": q["kat"], "n": q["n"], "q": q["text"], "a": arr, "c": pos,
                    "v": q["v"], "z": srcs, **({"img": q["img"]} if q["img"] else {})})
    ids = [o["id"] for o in out]
    assert len(set(ids)) == len(ids), "duplicitné id"
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    tests = make_tests(qs)
    json.dump(tests, open(os.path.join(ROOT, "data", "testy.json"), "w", encoding="utf-8"), separators=(",", ":"))
    print("Zapísané data/testy.json:", len(tests), "testov")
    json.dump({"kat": {k: {"nazov": v[0], "pocet": v[1], "body": v[2]} for k, v in KAT.items()}, "otazky": out},
              open(os.path.join(ROOT, "data", "otazky.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("Zapísané data/otazky.json:", len(out))


if __name__ == "__main__":
    main()
