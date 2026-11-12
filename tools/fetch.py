"""Stiahne URL do zdroje-cache a uloží čistý text (.txt) na overovanie faktov.

Použitie: python -I fetch.py <slug> <url> [<slug> <url> ...]
"""
import sys, os, re, json, urllib.request, datetime
from html.parser import HTMLParser
from urllib.parse import urljoin

CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "zdroje-cache")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
NL = "\n"


class Txt(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "head"}
    BLOCK = {"p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "br", "section", "article",
             "td", "th", "dt", "dd", "table", "ul", "ol"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.links = [], 0, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.SKIP:
            self.skip += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in self.BLOCK:
            self.out.append(NL)
        if tag in ("td", "th"):
            self.out.append(" | ")
        if tag == "img" and a.get("alt"):
            self.out.append(f" [img: {a.get('alt')}] ")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        if tag in self.BLOCK:
            self.out.append(NL)

    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)


def strip_boiler(t):
    # europa.eu: hlavný obsah je za drobčekovou navigáciou a pred pätičkou
    for end in ("Túto stránku spravuje", "This page is managed by", NL + "Share this page", NL + "Zdieľať túto stránku"):
        i = t.find(end)
        if i > 500:
            t = t[:i]
    i = t.find("Domovská stránka" + NL + "…")
    if i < 0:
        i = t.find("Home" + NL + "…")
    if 0 <= i < len(t) // 2:
        t = t[i:]
    return t


def to_text(raw, ctype):
    enc = "utf-8"
    m = re.search(r"charset=([\w-]+)", ctype or "")
    if m:
        enc = m.group(1)
    s = raw.decode(enc, errors="replace")
    p = Txt()
    p.feed(s)
    t = "".join(p.out)
    t = re.sub(r"[ \t\r\f\v ]+", " ", t)
    t = re.sub(r"\n\s*\n+", NL, t)
    return strip_boiler(t.strip()).strip(), p.links


def fetch(slug, url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "sk,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
        ctype = r.headers.get("Content-Type", "")
        final = r.geturl()
    os.makedirs(CACHE, exist_ok=True)
    links = []
    if url.lower().endswith(".pdf") or "pdf" in ctype:
        path = os.path.join(CACHE, slug + ".pdf")
        open(path, "wb").write(raw)
        try:
            import pypdf
            rd = pypdf.PdfReader(path)
            text = NL.join((pg.extract_text() or "") for pg in rd.pages)
        except Exception as e:
            text = f"PDF extract error: {e}"
    else:
        text, links = to_text(raw, ctype)
    meta = {"slug": slug, "url": url, "final": final,
            "fetched": datetime.datetime.now().isoformat(timespec="seconds"), "chars": len(text)}
    if links:
        good = sorted(set(urljoin(final, h) for h in links if not h.startswith(("#", "mailto:", "javascript:", "tel:"))))
        with open(os.path.join(CACHE, slug + ".links"), "w", encoding="utf-8") as f:
            f.write(NL.join(good))
    with open(os.path.join(CACHE, slug + ".txt"), "w", encoding="utf-8") as f:
        f.write(f"URL: {url}{NL}FETCHED: {meta['fetched']}{NL}{NL}{text}")
    idx = os.path.join(CACHE, "_index.json")
    data = json.load(open(idx, encoding="utf-8")) if os.path.exists(idx) else {}
    data[slug] = meta
    json.dump(data, open(idx, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return meta


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--list":
        # súbor s riadkami "slug url"
        args = [x for line in open(args[1], encoding="utf-8") if line.strip() and not line.startswith("#") for x in line.split(None, 1)]
        args = [a.strip() for a in args]
    for i in range(0, len(args), 2):
        slug, url = args[i], args[i + 1]
        try:
            m = fetch(slug, url)
            flag = "" if m["chars"] > 400 else "  (MÁLO TEXTU)"
            print(f"OK  {slug}: {m['chars']}{flag}")
        except Exception as e:
            print(f"ERR {slug}: {e}")
