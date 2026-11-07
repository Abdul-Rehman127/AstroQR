# Asteroids in a QR Code

A complete, playable **Asteroids** game that fits entirely inside a **single QR code**. Scan it, and the game runs in your browser. Nothing is downloaded from any server, there is no app, and there is no backend. The ~2 KB of data in the code *is* the game.

## Play it

> **Status:** the game source (`src/asteroids.html`) and the generated `asteroids_qr.png` aren't committed to this repo yet — only the packing tool (`pack.py`) and the loader page (`docs/index.html`) are here so far. Follow "Build it yourself" below to generate your own QR code once you have a game file to pack.

## Controls
- **Phone:** tap the top of the screen to fire; the bottom row is left / thrust / right.
- **Keyboard:** arrow keys to turn and thrust, space to fire.

## How it works

```
asteroids.html ──gzip──►──base64──► put in URL #fragment ──► QR code (https link)
```

The QR code holds a normal `https://` link to a fixed, **game-agnostic 700-byte loader page** (`docs/index.html`, hosted free on GitHub Pages). The **entire game** is compressed into the link's `#fragment`. A browser never sends the fragment to the server, so the game still lives entirely inside the QR code; the hosted page is just a dumb player that inflates and runs whatever game it's handed, using the browser's built-in `DecompressionStream`.

A standard QR code holds at most **2,953 bytes**; this build uses **2,116**.

## Why an https link instead of raw HTML
A phone's **default camera only auto-opens http(s) links.** Point it at raw HTML or a `data:` URL and the phone just offers to web-search the text (this is the "it did a Google search" problem). Wrapping the game in a real https link that carries the game in its fragment makes it open on any phone camera, while keeping the game inside the code and nothing game-specific on the server.

## Build it yourself
```
pip install -r requirements.txt
python3 pack.py src/asteroids.html --base https://YOURNAME.github.io/qr-game/
```
Replace `YOURNAME` with your GitHub username. This regenerates `asteroids_qr.png`.

## Hosting the loader (one time, free)
1. Push this repo to GitHub.
2. Settings → Pages → serve from the `docs/` folder.
3. Your loader lives at `https://YOURNAME.github.io/qr-game/`. Use that as `--base`.

The page is uploaded once and never changes; every game is just a different QR with a different fragment.

## Fully-offline alternative
If you want *zero* hosting, a QR-scanner app that can open `data:` URLs will run a self-contained version with no server at all. The hosted-link version above is the one that "just works" on a default iPhone/Android camera, so it's the default for sharing with testers.

## Note on novelty
This isn't the first time anyone has put a program in a QR code. The goal here is a *clean, genuinely playable* game in the smallest space, with the method fully documented.

## Tech
Plain JavaScript + HTML Canvas, gzip compression, QR encoding with `segno`. No frameworks, no build step, no dependencies in the game itself.
