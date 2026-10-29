# Website Bäder Natursteine und Glas

Statische Website (HTML + CSS, kein Framework). Wird über Vercel ausgeliefert.

## Texte oder Seiten ändern

Alle Seiten entstehen aus **einer** Datei: `_quelle/build.py`.
Dort stehen Menü, Kopf- und Fußzeile (nur einmal) und die Inhalte jeder Seite.

1. Text in `_quelle/build.py` ändern
2. Im Projektordner ausführen: `python3 _quelle/build.py`
3. Fertig – alle `.html`-Dateien sind neu erzeugt.

Die `.html`-Dateien bitte nicht direkt bearbeiten, sie werden beim nächsten Lauf überschrieben.

## Ordner

- `style.css` – Design für alle Seiten
- `main.js` – Menü, Bildbetrachter, Video, Schnelle Hilfe, Widerrufsformular
- `assets/img/` – Bilder der Seiten (Originalbilder, komprimiert)
- `assets/bilddatenbank/` – Natursteinbilder zum Herunterladen
- `assets/pdf/` – Broschüren
- `assets/fonts/` – Schriften lokal (keine Verbindung zu Google Fonts)

Hinweis: Alle Seiten haben `noindex` (nicht in Google), solange es eine Vorschau ist.
