# Korrekturleitfaden

Tablet-Checkliste für die Korrektur schriftlicher Prüfungen (Klausuren und Abitur). Sie läuft neben dem Erwartungshorizont mit: Bereich antippen (Aufgabenbezug, AFB I–III, Darstellung, Gesamturteil), Notenbereich der Teilleistung wählen, dann erscheinen die passenden Gutachten-Bausteine, Schlüsselwörter, Leitfragen zum Beleg und Randkommentare.

Die App speichert keine Namen und keine Punkte, nur Haken und Auswahl im Browser des Geräts.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `src/app.html` | Die App: Inhalte, Gestaltung, Logik (einzige Quelle) |
| `assets/` | Sunny-Illustrationen und App-Icons |
| `scripts/build.py` | Baut `dist/` (installierbare PWA) und `korrekturleitfaden.html` (Einzeldatei) |
| `.github/workflows/pages.yml` | Baut und veröffentlicht `dist/` bei jedem Push auf `main` |

## Inhalte ändern

Texte stehen in `src/app.html` in den Konstanten `STAGES` (Schlüsselwörter), `AREAS` (Bausteine, Leitfragen, Randkommentare) und `ZG` (Korrekturzeichen). Nach dem Push baut GitHub die Seite neu; die installierte App lädt die neue Fassung beim nächsten Öffnen mit Netz.

Lokal testen:

```sh
python3 scripts/build.py
python3 -m http.server -d dist 8000
```

## Auf dem Tablet installieren

- iPad (Safari): Seite öffnen → Teilen → „Zum Home-Bildschirm“.
- Android (Chrome): Seite öffnen → Menü → „App installieren“.

Danach läuft die App auch ohne Netz.

## Rechtsgrundlagen

AV Prüfungen Nr. 10 und 20; VO-GO § 14 und 15; KMK-Oberstufenvereinbarung Ziff. 8.4.3; EPA Geographie § 2 und 3.5.
