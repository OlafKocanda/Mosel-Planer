"""Baut den Mosel-Planer aus src/ zusammen.

    python3 src/build.py              -> index.html (eigenständig, Firebase, für GitHub Pages)
    python3 src/build.py --artifact   -> build/artifact.html (Variante für das Claude-Artefakt)
"""
import json, re, sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
D = SRC / "data"

c = json.loads((D / "coords.json").read_text())
dr = json.loads((D / "drive.json").read_text())
md = json.loads((D / "mapdata.json").read_text())
aus = json.loads((D / "aus.json").read_text())
at = json.loads((D / "at.json").read_text())
orte = list(dr["drive"].keys())
ONAME = {"leverkusen":"Leverkusen","herten":"Herten","kelkheim":"Kelkheim","koeln":"Köln","bonn":"Bonn","duesseldorf":"Düsseldorf","aachen":"Aachen","essen":"Essen","dortmund":"Dortmund","muenster":"Münster","wuppertal":"Wuppertal","bielefeld":"Bielefeld","frankfurt":"Frankfurt","badsoden":"Bad Soden","mainz":"Mainz"}
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
states = {k: v for k, v in md["states"].items() if k != "Bayern"}
data = "\n".join([
    "// Startorte, Koordinaten [lat, lon], Fahrzeiten in Minuten (OSRM + 12 %)",
    f"const OKEYS = {J(dr['orig'])};",
    f"const ONAME = {J(ONAME)};",
    f"const OGEO = {J({k: c[k] for k in dr['orig']})};",
    f"const GEO = {J({k: c[k] for k in orte})};",
    f"const DRIVE = {J(dr['drive'])};",
    "// Ausflugsziele, recherchiert am 26.10.2026; until = vermutlich letzter Öffnungstag 2027 (nach Stand 2026)",
    "const AUS = [\n" + ",\n".join(J(a) for a in aus) + "\n];",
    "// Fahrzeit Ort → Ausflug in Minuten",
    f"const AT = {J(at)};",
    'const INFO_DATE = "26. Oktober 2026";',
    "// Kartengeometrie, projiziert: x = (lon-5.8)*0.643*700, y = (52.2-lat)*700",
    f"const MAP = {J({**md['lines'], 'states': states})};",
])
t = (SRC / "template.html").read_text()
assert "/*@DATA@*/" in t and "/*@STORE@*/" in t
t = t.replace("/*@DATA@*/", data)

if "--artifact" in sys.argv:
    out = ROOT / "build" / "artifact.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(t.replace("/*@STORE@*/", (SRC / "store-claude.js").read_text()))
    print("geschrieben:", out)
    sys.exit()

body = t.replace("/*@STORE@*/", (SRC / "store-firebase.js").read_text())
body = body.replace("<p><b>Karte:</b>", "<p><b>Daten:</b> Stimmen, Tage und Ferienhäuser liegen in einer Firebase-Datenbank, alle mit dem Link sehen dasselbe.</p>\n    <p><b>Karte:</b>", 1)
title = re.search(r"<title>.*?</title>", body).group(0)
body = body.replace(title, "", 1).replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "", 1)
head = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#1D5C68">
{title}
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
<script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-database-compat.js"></script>
</head>
<body>
"""
(ROOT / "index.html").write_text(head + body + "\n</body>\n</html>\n")
print("geschrieben:", ROOT / "index.html")
