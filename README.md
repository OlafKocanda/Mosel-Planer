# Mosel-Planer

Gemeinsame Planung der Moseltour in den NRW-Herbstferien 2027 (23.10.–6.11.) für Jonathan, Nicole und Alessa (Leverkusen), Dennis und Hanna (Herten) sowie Anni, Olaf und Thea (Kelkheim).

**App:** https://olafkocanda.github.io/Mosel-Planer/ · **Werbeseite:** https://olafkocanda.github.io/Mosel-Planer/werbung.html

## Inhalt

- `index.html`: die fertige App für GitHub Pages. 24 Moselorte und 28 Ausflüge swipen, Rangliste mit Anreise aus Leverkusen, Herten und Kelkheim, Karte, Terminfindung und Ferienhaus-Sammlung. Wird aus `src/` gebaut, nicht direkt bearbeiten.
- `database.rules.json`: Regeln für die Firebase Realtime Database im Projekt `mosel-planer`. In der Firebase-Konsole unter „Realtime Database → Regeln“ komplett einfügen und veröffentlichen.
- `werbung.html` und `werbung/`: Werbeseite für die Freundesgruppe als zwei Handy-Bildschirme, plus die fertigen Screenshots.
- `src/`: Quellen
  - `template.html`: Oberfläche, Stil und Logik der App
  - `store-firebase.js`: Speicher über Firebase (für `index.html`); `store-claude.js`: Speicher der Variante als Claude-Artefakt
  - `data/`: Koordinaten (`coords.json`), Fahrzeiten ab den Startorten (`drive.json`), Kartengeometrie (`mapdata.json`), Ausflugsziele (`aus.json`) und Fahrzeiten Ort → Ausflug (`at.json`)
  - `build.py`: baut `index.html` (mit `--artifact` die Artefakt-Variante nach `build/`)
  - `werbung/`: Vorlage, Kartenbilder und `build.py` für `werbung.html`

## Ändern

```
python3 src/build.py
python3 src/werbung/build.py
```

Dann `index.html` bzw. `werbung.html` committen und pushen, GitHub Pages veröffentlicht automatisch.

## Daten

Die Daten liegen im Firebase-Projekt `mosel-planer` (Realtime Database, Standort europe-west1) unter `mosel/`: `marks` (Stimmen und Gestrichenes je Ort/Ausflug), `avail` (freie Tage je Person), `houses` (Ferienhäuser) und `settings` (Gewichtung, Startorte, Nächte, festgelegter Termin, Ort und Haus).

## Quellen

Fahrzeiten mit OSRM auf OpenStreetMap-Daten (+12 % Puffer). Moselverlauf aus einer OSRM-Fahrradroute entlang des Moselradwegs (© OpenStreetMap-Mitwirkende, ODbL), Rhein, Saar und Sauer nach Natural Earth, Ländergrenzen nach DIVA-GIS (deutschlandGeoJSON), vereinfacht. Ausflugsinfos recherchiert am 26.10.2026, meist Stand 2026. Ferientermine laut veröffentlichter Ferienliste NRW.
