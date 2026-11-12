"""Obrázky pre obrázkové otázky.
  python -I imgget.py list <url>                 – vypíše <img> (src, alt) zo stránky
  python -I imgget.py get <url> <cesta.jpg> [max] – stiahne obrázok, zmenší (max px, predvolene 480) a uloží ako JPG/PNG
Cesta je relatívna k testy-app/."""
import sys, os, io, re, urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "sk,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read(), r.headers.get("Content-Type", "")


class Imgs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("img", "source"):
            src = a.get("src") or a.get("data-src") or (a.get("srcset") or a.get("data-srcset") or "").split(" ")[0]
            if src:
                self.out.append((src, a.get("alt") or a.get("title") or ""))


def lst(url):
    html, _ = fetch(url)
    p = Imgs()
    p.feed(html.decode("utf-8", "replace"))
    for s, a in p.out:
        print(urljoin(url, s), "|", a)


def get(url, out, mx=480):
    from PIL import Image
    data, ct = fetch(url)
    path = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if "svg" in ct or url.lower().endswith(".svg"):
        raise SystemExit("SVG – treba PNG verziu: " + url)
    im = Image.open(io.BytesIO(data))
    im.thumbnail((mx, mx))
    if out.lower().endswith(".png"):
        im.save(path, optimize=True)
    else:
        if im.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            im = im.convert("RGBA")
            bg.paste(im, mask=im.split()[-1])
            im = bg
        im.convert("RGB").save(path, quality=82, optimize=True, progressive=True)
    print("OK", out, im.size, os.path.getsize(path))


if __name__ == "__main__":
    if sys.argv[1] == "list":
        lst(sys.argv[2])
    else:
        get(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 480)
