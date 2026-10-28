"""Baut die Werbeseite werbung.html (zwei Handy-Bildschirme für Screenshots).

    python3 src/werbung/build.py
"""
import json, base64
from pathlib import Path

W = Path(__file__).resolve().parent
ROOT = W.parent.parent
md = json.loads((W.parent / "data" / "mapdata.json").read_text())["lines"]
P = lambda lat, lon: ((lon - 5.8) * 0.643 * 700, (52.2 - lat) * 700)
pts = {"Koblenz": (50.3597, 7.5978, "end", -18, -4), "Cochem": (50.1484, 7.1663, "end", -20, 12), "Trier": (49.7596, 6.6442, "start", 18, 12)}
dots = "".join(f'<circle cx="{P(a, b)[0]:.0f}" cy="{P(a, b)[1]:.0f}" r="12"/>' for a, b, *_ in pts.values())
labs = "".join(f'<text x="{P(a, b)[0] + dx:.0f}" y="{P(a, b)[1] + dy:.0f}" text-anchor="{anc}">{n}</text>' for n, (a, b, anc, dx, dy) in pts.items())
river = f'''<svg class="river" viewBox="340 1250 520 480" role="img" aria-label="Die Mosel zwischen Trier und Koblenz">
<style>.river .rv{{stroke-width:11px}}.river .rh{{stroke-width:9px}}.river circle{{stroke-width:6px}}.river text{{font-size:38px}}</style>
<path class="rh" d="{md['rhine']}"/><path class="rv" d="{md['mosel']}"/>{dots}{labs}</svg>'''
b64 = lambda f: "data:image/jpeg;base64," + base64.b64encode((W / f).read_bytes()).decode()
t = (W / "promo-template.html").read_text()
for k, v in {"{{RIVER}}": river, "{{ORT}}": b64("card-ort.jpg"), "{{AUS}}": b64("card-aus.jpg")}.items():
    assert t.count(k) == 1, k
    t = t.replace(k, v)
page = '<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="robots" content="noindex">\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}</style>\n</head>\n<body>\n' + t + "\n</body>\n</html>\n"
(ROOT / "werbung.html").write_text(page)
print("geschrieben:", ROOT / "werbung.html")
