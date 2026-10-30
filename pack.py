#!/usr/bin/env python3
"""Pack an HTML game into a single QR code that opens on any phone camera.

Usage:
  python3 pack.py src/asteroids.html --base https://YOURNAME.github.io/qr-game/

Why a base URL: a phone's default camera only auto-opens http(s) links, not raw
HTML or data: URLs (that's why a raw payload just triggers a web search). So the
QR holds a normal https link to a fixed, game-agnostic loader page (hosted once,
free, on GitHub Pages), with the ENTIRE game compressed into the URL's #fragment.
The fragment never leaves the phone / never hits the server, so the game still
lives inside the QR code; the page is just a dumb ~700-byte player.

Outputs asteroids_qr.png and a size report.
"""
import sys, gzip, base64, argparse, segno

CAP = 2953  # QR capacity in bytes (version 40, error-correction level L)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("game", nargs="?", default="src/asteroids.html")
    ap.add_argument("--base", default="https://YOURNAME.github.io/qr-game/",
                    help="URL of the hosted loader page (docs/index.html on GitHub Pages)")
    ap.add_argument("--out", default="asteroids_qr.png")
    a = ap.parse_args()

    html = open(a.game, "rb").read()
    payload = base64.b64encode(gzip.compress(html, 9)).decode()
    url = a.base.rstrip("/") + "/#" + payload

    # round-trip check
    assert gzip.decompress(base64.b64decode(url.split("#",1)[1])) == html, "round-trip mismatch!"

    size = len(url.encode())
    print(f"game HTML   : {len(html):>5} bytes")
    print(f"gzip'd      : {len(gzip.compress(html,9)):>5} bytes")
    print(f"QR URL      : {size:>5} bytes  ({'FITS' if size<=CAP else 'OVER'}, {CAP-size} spare of {CAP})")
    if size > CAP:
        sys.exit("Too big for one QR code. Golf the game smaller.")
    qr = segno.make(url, error="l")
    print(f"QR version  : {qr.version}  (lower = easier to scan)")
    qr.save(a.out, scale=12, border=4)
    print(f"saved       : {a.out}")
    print(f"opens       : {a.base.rstrip('/')}/#<game>")

if __name__ == "__main__":
    main()
