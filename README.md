# Mosel-Planer

Gemeinsame Planung der Moseltour in den NRW-Herbstferien 2027 (23.10.–6.11.) für Jonathan, Nicole und Alessa (Leverkusen), Dennis und Hanna (Herten) sowie Anni, Olaf und Thea (Kelkheim).

- `index.html`: die komplette App (läuft über GitHub Pages). 24 Moselorte und 28 Ausflüge swipen, Rangliste mit Anreise aus Leverkusen, Herten und Kelkheim, Karte, Terminfindung und Ferienhaus-Sammlung.
- `database.rules.json`: Regeln für die Firebase Realtime Database des eigenen Projekts für den Mosel-Planer. In der Firebase-Konsole unter „Realtime Database → Regeln“ komplett einfügen und veröffentlichen.

Die Daten liegen in Firebase unter `mosel/`: `marks` (Stimmen und Gestrichenes je Ort/Ausflug), `avail` (freie Tage je Person), `houses` (Ferienhäuser) und `settings` (Gewichtung, Startorte, Nächte, festgelegter Termin, Ort und Haus). Ohne die Regeln zeigt die App „Datenbank-Regeln fehlen noch“ und speichert nichts.
