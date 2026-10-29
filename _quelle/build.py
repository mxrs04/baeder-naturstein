"""Erzeugt alle HTML-Seiten der Website aus einer Quelle.

Kopfzeile, Menü und Fußzeile stehen nur einmal hier drin und werden auf
jede Seite übernommen. Nach einer Änderung einfach ausführen:

    python3 _quelle/build.py

Die fertigen .html-Dateien landen im Hauptordner (eine Ebene höher).
Bitte die .html-Dateien nicht direkt bearbeiten – sie werden beim nächsten
Lauf überschrieben. Texte immer hier ändern.
"""
import os
import struct
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))

FIRMA = "Eberhard Bäder Natursteine und Glas GmbH &amp; Co. KG"
TEL = "+49 7153 8313-0"
TEL_LINK = "+49715383130"
FAX = "+49 7153 8313-20"
MAIL = "info@natursteinwerk-baeder.de"
YOUTUBE_ID = "hvYI4MGJVQc"


# ---------------------------------------------------------------- Hilfen

def img_size(path):
    """Breite/Höhe von JPG/PNG lesen (ohne Zusatzpakete)."""
    with open(path, "rb") as f:
        head = f.read(26)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", head[16:24])
        f.seek(2)
        while True:
            marker, = struct.unpack(">H", f.read(2))
            length, = struct.unpack(">H", f.read(2))
            if marker in (0xFFC0, 0xFFC1, 0xFFC2):
                f.read(1)
                h, w = struct.unpack(">HH", f.read(4))
                return w, h
            f.seek(length - 2, 1)


def img(name, alt="", cls="", lazy=True, folder="assets/img"):
    path = f"{folder}/{name}"
    w, h = img_size(os.path.join(ROOT, path))
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ""
    return f'<img src="{path}" width="{w}" height="{h}" alt="{escape(alt)}"{c}{l}>'


def photo(name, alt="", extra=""):
    return f'<div class="photo {extra}">{img(name, alt)}</div>'


def figure(name, cap="", alt=None, extra=""):
    alt = cap if alt is None else alt
    fc = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f'<figure>{photo(name, alt, extra)}{fc}</figure>'


def gallery(items, contain=False):
    """items: Liste aus (Datei, Bildunterschrift)."""
    out = []
    for name, cap in items:
        label = cap or "Bild vergrößern"
        out.append(
            f'<figure><a href="assets/img/{name}" data-zoom="{escape(cap)}" aria-label="{escape(label)}">'
            f'{photo(name, cap)}</a>{f"<figcaption>{cap}</figcaption>" if cap else ""}</figure>')
    cls = "gallery gallery--contain" if contain else "gallery"
    return f'<div class="{cls}">{"".join(out)}</div>'


def swatches(items, square=False):
    """items: Liste aus (Datei, 'B-110 Absolute White')."""
    out = []
    for name, label in items:
        code, _, rest = label.partition(" ")
        if rest and any(ch.isdigit() for ch in code):
            cap = f"<b>{code}</b>{rest}"
        else:
            cap = label
        out.append(f'<figure class="swatch{" swatch--square" if square else ""}">{img(name, label)}<figcaption>{cap}</figcaption></figure>')
    return f'<div class="swatches">{"".join(out)}</div>'


def ul(items, cls="checks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def chips(items):
    return '<ul class="chips">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def acc(title, body, open_=False):
    return f'<details class="acc"{" open" if open_ else ""}><summary>{title}</summary><div class="acc-body">{body}</div></details>'


def section(inner, cls="", id_=None):
    i = f' id="{id_}"' if id_ else ""
    return f'<section class="section {cls}"{i}><div class="wrap">{inner}</div></section>'


def head(eyebrow, title, lead="", center=False, tag="h2"):
    e = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="head{" center" if center else ""}">{e}<{tag}>{title}</{tag}>{l}</div>'


def hero(image, eyebrow, title, lead="", buttons="", small=True, home=False):
    cls = "hero hero--home" if home else ("hero hero--small" if small else "hero")
    e = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return (f'<section class="{cls}">{img(image, "", "hero-bg", lazy=False)}'
            f'<div class="wrap">{e}<h1>{title}</h1>{l}{buttons}</div></section>')


def page_head(crumbs, title, lead=""):
    c = " / ".join(f'<a href="{h}">{t}</a>' if h else t for t, h in crumbs)
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<section class="page-head"><div class="wrap"><div class="crumbs">{c}</div><h1>{title}</h1>{l}</div></section>'


def btn(text, href, kind="", ext=False):
    k = f" btn--{kind}" if kind else ""
    t = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="btn{k}" href="{href}"{t}>{text}</a>'


def btns(*b):
    return f'<div class="btns">{"".join(b)}</div>'


def subnav(items, active):
    act = ' class="is-active" aria-current="page"'
    return '<nav class="subnav" aria-label="Unterseiten">' + "".join(
        f'<a href="{h}"{act if h == active else ""}>{t}</a>' for t, h in items) + "</nav>"


def tile(href, image, title, text, more="Mehr erfahren", banner=False):
    cls = "tile tile--banner" if banner else "tile"
    return (f'<a class="{cls}" href="{href}"><div class="photo">{img(image, "")}</div>'
            f'<div class="tile-body"><h3>{title}</h3><p>{text}</p><span class="link-arrow">{more}</span></div></a>')


def person(image, name, text):
    return f'<div class="card person">{img(image, name)}<div>{text}</div></div>'


def cta(title="Lassen Sie sich beraten", text="Besuchen Sie unsere Ausstellung in Altbach oder rufen Sie uns an – wir beraten Sie gerne persönlich."):
    return section(
        f'<div class="center narrow" style="margin:0 auto"><span class="eyebrow">Persönlich für Sie da</span><h2>{title}</h2>'
        f'<p class="lead">{text}</p>'
        + btns(btn(ICON_PHONE + "07153 8313-0 anrufen", f"tel:{TEL_LINK}", "light"),
               btn("Kontakt &amp; Anfahrt", "kontakt-anfahrt.html", "ghost").replace("btn--ghost", "btn--ghost btn--on-dark"))
        .replace('class="btns"', 'class="btns" style="justify-content:center"') + "</div>",
        "section--dark")


ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>'
ICON_CHEV = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
ICON_INFO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>'

GEWERBE_HINWEIS = (
    f'<div class="notice" role="note">{ICON_INFO}<div><strong>Wichtige Kundeninformation</strong>'
    '<p>Liebe Kunden, wir weisen Sie darauf hin, dass wir <b>ausschließlich an Gewerbekunden</b> und '
    '<b>nicht an Privatpersonen</b> verkaufen. Wir bitten Sie, dies zu berücksichtigen.</p></div></div>')


# ---------------------------------------------------------------- Menü

MENU = [
    ("Naturstein &amp; Keramik", [
        ("Naturstein", "naturstein.html"),
        ("Silestone", "silestone.html"),
        ("Lightstone", "lightstone.html"),
        ("Neolith Keramik", "neolith-keramik.html"),
        ("Dekton", "dekton.html"),
        ("Laminam", "laminam.html"),
    ]),
    ("Glas", [
        ("Vetroplan Glasrückfronten", "vetroplan-glasrueckfronten.html"),
        ("Basic Line", "vetroplan-basic-line.html", "sub"),
        ("Trend Line", "vetroplan-trend-line.html", "sub"),
        ("Steel Art Line", "vetroplan-steel-art-line.html", "sub"),
        ("Life Line", "vetroplan-life-line.html", "sub"),
        ("Digital Print Line", "vetroplan-digital-print-line.html", "sub"),
    ]),
    ("Unternehmen", [
        ("Über uns &amp; Chronik", "ueber-uns.html"),
        ("Unser Team", "team.html"),
        ("Unsere Räumlichkeiten", "raeumlichkeiten.html"),
        ("News und Mitteilungen", "news-und-mitteilungen.html"),
    ]),
    ("Downloads", [
        ("Downloadcenter", "downloads.html"),
        ("Bilddatenbank Naturstein", "downloads.html#bilddatenbank"),
        ("Preisliste 2025/26", "download-preislisten.html"),
    ]),
]


def nav(active):
    out = []
    for i, (label, items) in enumerate(MENU):
        hrefs = [it[1] for it in items]
        is_act = " is-active" if active in hrefs else ""
        links = []
        for it in items:
            t, h = it[0], it[1]
            sub = " sub" if len(it) > 2 else ""
            act = ' is-active" aria-current="page' if h == active else ""
            links.append(f'<li><a class="{sub.strip()}{act}" href="{h}">{t}</a></li>')
        out.append(
            f'<li><button class="nav-link{is_act}" type="button" aria-expanded="false" aria-controls="dd{i}">{label}{ICON_CHEV}</button>'
            f'<ul class="dropdown" id="dd{i}">{"".join(links)}</ul></li>')
    k_act = " is-active" if active == "kontakt-anfahrt.html" else ""
    out.append(f'<li><a class="nav-link{k_act}" href="kontakt-anfahrt.html">Kontakt &amp; Anfahrt</a></li>')
    out.append(f'<li><a class="btn" href="tel:{TEL_LINK}">{ICON_PHONE}Anrufen</a></li>')
    return '<ul class="nav" id="hauptmenue">' + "".join(out) + "</ul>"


def footer():
    return f'''<footer class="footer"><div class="wrap">
<div class="footer-grid">
  <div>
    <a class="footer-logo" href="index.html">{img("logo.png", "Bäder Natursteine und Glas", folder="assets")}</a>
    <p>{FIRMA}<br>In den Weiden 24<br>73776 Altbach</p>
    <p>Telefon <a href="tel:{TEL_LINK}">{TEL}</a><br>Fax {FAX}<br>E-Mail <a href="mailto:{MAIL}">{MAIL}</a></p>
  </div>
  <div>
    <h4>Öffnungszeiten</h4>
    <p>Montag bis Mittwoch und Freitag<br>8.00–12.20 Uhr und 13.00–17.00 Uhr</p>
    <p>Donnerstag<br>8.00–12.20 Uhr und 13.00–18.00 Uhr</p>
  </div>
  <div>
    <h4>Materialien</h4>
    <ul>
      <li><a href="naturstein.html">Naturstein</a></li>
      <li><a href="silestone.html">Silestone</a></li>
      <li><a href="lightstone.html">Lightstone</a></li>
      <li><a href="neolith-keramik.html">Neolith Keramik</a></li>
      <li><a href="dekton.html">Dekton</a></li>
      <li><a href="laminam.html">Laminam</a></li>
      <li><a href="vetroplan-glasrueckfronten.html">Vetroplan Glas</a></li>
    </ul>
  </div>
  <div>
    <h4>Unternehmen</h4>
    <ul>
      <li><a href="ueber-uns.html">Über uns</a></li>
      <li><a href="ueber-uns.html#chronik">Chronik</a></li>
      <li><a href="team.html">Unser Team</a></li>
      <li><a href="raeumlichkeiten.html">Räumlichkeiten</a></li>
      <li><a href="downloads.html">Downloads</a></li>
      <li><a href="kontakt-anfahrt.html">Kontakt &amp; Anfahrt</a></li>
    </ul>
  </div>
</div>
<div class="footer-bottom">
  <span>©2019 Alle Rechte vorbehalten.</span>
  <nav aria-label="Rechtliches">
    <a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a><a href="cookie-richtlinie.html">Cookie-Richtlinie</a><a href="sitemap.html">Sitemap</a><a href="gewaehrleistung.html">Gesetzliche Gewährleistung</a><a href="vertrag-widerrufen.html">Vertrag widerrufen</a>
  </nav>
</div>
</div></footer>'''


HELP = f'''<button class="help-btn" type="button" aria-expanded="false" aria-controls="hilfe"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg><span>Schnelle Hilfe</span></button>
<div class="help" id="hilfe" role="dialog" aria-label="Schnelle Hilfe">
  <div class="help-head"><div><b>Bäder Assistenz</b><small>Schnelle Antworten</small></div><button type="button" aria-label="Schließen">×</button></div>
  <div class="help-body"><div class="msg">Guten Tag! Willkommen bei Bäder Natursteine und Glas. Wobei können wir helfen? Tippen Sie auf ein Thema.</div></div>
  <div class="help-quick">
    <button type="button" data-q="zeiten">Öffnungszeiten</button>
    <button type="button" data-q="materialien">Materialien</button>
    <button type="button" data-q="preise">Preise</button>
    <button type="button" data-q="kontakt">Kontakt</button>
  </div>
</div>'''


def layout(slug, title, desc, body):
    full_title = title if slug == "index.html" else f"{title} | Bäder Natursteine und Glas"
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{full_title}</title>
<meta name="description" content="{escape(desc)}">
<meta name="theme-color" content="#2a2e31">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="manifest" href="manifest.json">
<link rel="preload" href="assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/cormorant.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="sr-skip" href="#inhalt" style="position:absolute;left:-9999px">Zum Inhalt springen</a>
<div class="topbar"><div class="wrap">
  <span class="hide-sm">Mo–Mi &amp; Fr 8.00–17.00 Uhr · Do bis 18.00 Uhr</span>
  <a href="tel:{TEL_LINK}">Tel. 07153 8313-0</a>
  <a class="hide-xs" href="mailto:{MAIL}">{MAIL}</a>
</div></div>
<header class="header"><div class="wrap">
  <a class="logo" href="index.html" aria-label="Startseite">{img("logo.png", "Bäder Natursteine und Glas", lazy=False, folder="assets")}</a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="hauptmenue"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg><span>Menü</span></button>
  <nav aria-label="Hauptmenü">{nav(slug)}</nav>
</div></header>
<main id="inhalt">
{body}
</main>
{footer()}
{HELP}
<script src="main.js" defer></script>
</body>
</html>
'''


PAGES = {}


def page(slug, title, desc):
    def deco(fn):
        PAGES[slug] = (title, desc, fn)
        return fn
    return deco


# ---------------------------------------------------------------- Gemeinsame Technik-Texte

AUSSCHNITTE = [
    "Viereck gesägt für Auflageteile; Viereck flächenbündige Teile; Viereck für Unterbauteile",
    "Softeck gesägt für Auflageteile; Softeck flächenbündige Teile; Softeck für Unterbauteile",
    "Rund gesägt für Auflageteile; Rund flächenbündige Teile; Rund für Unterbauteile",
    "Eckspülenausschnitt gesägt für Aufbauteile; Eckspülenausschnitt für flächenbündige Teile",
    "Ovalausschnitt gesägt für Auflageteile; Ovalausschnitt für Unterbauteile",
    "Ablaufrillen ca. 400 x 10 mm",
]
P5 = "<b>Profil 5:</b> Oberseite und Unterseite mit Fasen 3 mm und Unterseite 50 mm Tiefe geschliffen."
P6 = "<b>Profil 6:</b> Oberseite und Unterseite mit Rundung 3 mm und Unterseite 50 mm Tiefe geschliffen."
P9 = "<b>Profil 9:</b> Schürzenprofil auf Gehrung verklebt, oben und unten gefast oder gerundet."
PSTRATOS = "<b>Profil Stratos:</b> Oben und unten gefast und poliert, unten ist ein eloxiertes Aluprofil angeklebt."


def technik(profile, ausschnitte, sonstiges=None, title="Kantenprofile, Ausschnitte &amp; Sonstiges"):
    body = acc("Kantenprofile", ul(profile, ""), True) + acc("Mögliche Ausschnitte", ul(ausschnitte, ""))
    if sonstiges:
        body += acc("Sonstiges", f"<p>{sonstiges}</p>")
    return head("Technik", title) + body


MATERIALS = [
    ("naturstein.html", "naturstein-01.jpg", "Naturstein", "Granit, Marmor und mehr – über 70 Sorten aus aller Welt am Lager."),
    ("silestone.html", "silestone-01.jpg", "Silestone", "Quarzoberfläche mit bis zu 94 % Naturquarz und Hygieneschutz."),
    ("lightstone.html", "lightstone-10.jpg", "Lightstone", "Quarzkomposit in 12 mm – exklusiv bei uns in Altbach."),
    ("neolith-keramik.html", "neolith-keramik-03.jpg", "Neolith Keramik", "Hightech-Keramik: kratz-, hitze- und UV-beständig."),
    ("dekton.html", "dekton-01.jpg", "Dekton", "Ultrakompakte Oberfläche aus Glas, Keramik und Quarz."),
    ("laminam.html", "laminam-02.jpg", "Laminam", "Keramikplatten, bei denen jede Oberfläche ein Unikat ist."),
]


# ---------------------------------------------------------------- Startseite

@page("index.html", "Bäder Natursteine und Glas – Küchenarbeitsplatten aus Altbach bei Esslingen",
      "An unserem Standort in Altbach nahe Esslingen verarbeiten wir Glas und Naturstein zu hochwertigen Produkten für den Innen- und Außenbereich.")
def p_index():
    regions = [
        ("Natursteine, Steine und Glas nach", ["Heidelberg", "Schwetzingen", "Mannheim", "Wiesloch", "Mosbach", "Wertheim", "Schwäbisch Hall", "Bretten"]),
        ("oder Steine auch nach", ["Bretten", "Bietigheim", "Bruchsal", "Freudenstadt", "Nagold", "Heilbronn", "Neckarsulm", "Eppingen"]),
        ("oder unsere Natursteine nach", ["Bad Rappenau", "Pforzheim", "Sindelfingen", "Böblingen", "Fellbach", "Ludwigsburg", "Ellwangen", "Aalen", "Schwäbisch Gmünd"]),
        ("oder unsere Küchenarbeitsplatten nach", ["Reutlingen", "Tübingen", "Rottweil", "Göppingen", "Lörrach", "Singen", "Ravensburg"]),
    ]
    reg = "".join(f'<div class="card"><h4>{t}</h4>{chips(c)}</div>' for t, c in regions)
    return (
        hero("home-02.jpg", "Erleben Sie die Faszination Naturstein!", "Hochwertige Natursteinarbeiten aus Altbach",
             "Die Eberhard Bäder Natursteine und Glas GmbH ist Ihr Partner für Natursteinarbeiten in Altbach, Esslingen, Stuttgart und dem Baden-Württembergischen Raum.",
             btns(btn("Materialien ansehen", "#materialien", "light"), btn("Kontakt &amp; Anfahrt", "kontakt-anfahrt.html", "ghost").replace("btn--ghost", "btn--ghost btn--on-dark")),
             home=True)
        + f'<div class="wrap notice-bar">{GEWERBE_HINWEIS}</div>'
        + section(
            '<div class="split">'
            f'<div><span class="eyebrow">Stein, Keramik und Glas</span><h2>Natursteinarbeiten und Glasprodukte aus Altbach bei Esslingen</h2>'
            '<p class="lead">Überzeugen Sie sich und Ihre Familie von den faszinierenden Elementen Stein, Keramik und Glas – Sie werden sehen, dass Sie deren Schönheit und Komfort garantiert nicht mehr missen möchten!</p>'
            '<p>An unserem Standort in Altbach, ganz in der Nähe von Esslingen, verarbeiten wir sowohl <a href="naturstein.html">Natursteine</a> wie Granit, Quarzkomposit (<a href="silestone.html">Silestone</a>), Keramik, Marmor als auch Glas. Unsere Glas- und Natursteinarbeiten finden Anwendung in den unterschiedlichsten Innen- und Außenbereichen, zum Beispiel als:</p>'
            + ul(['<a href="neolith-keramik.html">Küchenarbeitsplatte</a> oder Tischplatte', "Waschtischplatte oder Duschtrennwand im Bad",
                  '<a href="vetroplan-glasrueckfronten.html">Wandverkleidung</a>', "Terrassenplatte", "Treppe und Bodenplatte", "Fenstersims"])
            + '</div>'
            f'<div>{photo("home-01.jpg", "Küche mit Natursteinarbeitsplatte", "photo--tall")}</div>'
            '</div>')
        + section(
            '<div class="split split--rev">'
            '<div><h2>Persönliche Beratung in unserem Haus</h2>'
            '<p>Egal, ob es um die Erneuerung Ihrer Küche durch eine Naturstein- oder Glasarbeitsplatte geht, um die Modernisierung Ihres Bades oder um eine Neugestaltung Ihrer Wohnräume – über die vielfältigen Einsatzmöglichkeiten von Naturstein und Glas beraten wir Sie gerne individuell in unserem Hause in Altbach bei Esslingen.</p>'
            '<p>In unserem <a href="raeumlichkeiten.html#ausstellung">Ausstellungsraum</a> erhalten Sie einen ersten Eindruck von unseren Natursteinarbeiten. Gerne können Sie sich von allen vorrätigen Materialien aus Stein, Glas, Silestone und Keramik ein passendes Muster für zu Hause mitnehmen und so vor Ort ausprobieren, ob das ausgewählte Material beispielsweise mit Ihrem Fußboden, Ihren Möbeln oder Wohn-Accessoires harmoniert.</p>'
            '<p>Schauen Sie gerne bei uns vorbei oder <a href="kontakt-anfahrt.html">kontaktieren Sie uns</a> für weitere Informationen!</p>'
            + btns(btn("Zur Ausstellung", "raeumlichkeiten.html#ausstellung"), btn("Kontakt aufnehmen", "kontakt-anfahrt.html", "ghost")) + '</div>'
            f'<div>{photo("home-03.jpg", "Kücheninsel aus Stein", "photo--tall")}</div>'
            '</div>', "section--white")
        + section(
            head("Unsere Materialien", "Für jeden Anspruch das passende Material", "Naturstein, Quarz, Keramik und Glas – alles aus einer Hand, gefertigt in Altbach.", True)
            + '<div class="grid grid-3">' + "".join(tile(*m) for m in MATERIALS) + '</div>', id_="materialien")
        + section(
            head("Direkt vom Hersteller", "Natur- oder Steinplatten direkt vom Hersteller!", center=True)
            + gallery([("home-04.jpg", "Unsere Ausstellung"), ("home-05.jpg", "Musterregale in der Ausstellung"),
                       ("home-06.jpg", "Küche mit Arbeitsplatte und Glasrückwand"), ("home-07.jpg", "Unser Steinlager")])
            + f'<div style="margin-top:28px" class="video">{img("home-07.jpg", "")}<button type="button" data-yt="{YOUTUBE_ID}">'
              '<span class="play"><svg width="34" height="34" viewBox="0 0 24 24" fill="#2a2e31" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span>Video abspielen'
              '<small>Beim Abspielen wird das Video von YouTube geladen. Dabei werden Daten an YouTube (Google) übertragen.</small></button></div>',
            "section--white")
        + section(
            head("Unsere Marken", "Erstklassige Glasprodukte aus Altbach", center=True)
            + '<div class="grid grid-2">'
            f'<div class="card"><div style="height:90px;display:flex;align-items:center">{img("home-08.png", "Vetroplan – Die Profis in Sachen Glas", "logo-img")}</div>'
            '<h3>Die Glas-Alternative: Die Individualität nahezu ohne Grenzen Ihrer Kreativität</h3>'
            '<p>VETROPLAN ist eine Marke aus unserem Hause und Ihr Partner für Nischenrückfronten aus Glas. Überzeugen Sie sich und Ihre Familie von dem faszinierenden Element Glas – Sie werden sehen, dass Sie auf dessen Schönheit und Komfort nicht mehr verzichten möchten.</p>'
            + btns(btn("Zu VETROPLAN", "https://www.vetroplan.com/", ext=True), btn("Glasrückfronten ansehen", "vetroplan-glasrueckfronten.html", "ghost")) + '</div>'
            f'<div class="card"><div style="height:90px;display:flex;align-items:center">{img("home-09.jpg", "Culina Luce", "logo-img")}</div>'
            '<h3>LED-Lichtfelder aus Glas für ein entspanntes Wohngefühl in Küche oder Bad</h3>'
            '<p>CULINA LUCE ist unsere Marke, wenn es um LED-Lichtfelder für unterschiedlichste Anwendungsbereiche geht. Von Küchenrückwänden über Wand- und Badfelder bis hin zu Küchenarbeitsplatten oder ganz individuellen Anfertigungen – beleuchtet oder unbeleuchtet.</p>'
            + btns(btn("Zu CULINA LUCE", "https://www.culina-luce.de/", ext=True)) + '</div>'
            '</div>')
        + section(
            head("Liefergebiete", "Wir liefern in folgende Regionen in Süddeutschland", center=True)
            + f'<div class="grid grid-2">{reg}</div>', "section--sand")
        + cta()
    )


# ---------------------------------------------------------------- Naturstein

@page("naturstein.html", "Natursteinplatten für innen und außen",
      "Von Terrassen und Treppen bis hin zu Arbeitsplatten und Waschtischen bieten unsere Natursteinplatten zahlreiche Gestaltungsmöglichkeiten.")
def p_naturstein():
    groups = [
        ("Dunkle Granitsteine", "#2b2b2b", "Angola Schwarz, Blue in the night, Brown Antic, China Impala, Coffee Imperiale, Emerald Pearl, Impala, Marinace, Marinace Gold, Matrix, Mystic Grey, Nero Assoluto, Nero India, Nero Marcos, Nordic Sunset, Padang Dunkel, Silver Black, Spectrolith, Star Galaxy, Steel Grey, Virginia Black"),
        ("Weiße Granitsteine", "#f4f2ee", "Azul Aran, Bethel White, Bianco Kristall, Bianco Sardo, Imperial White, Meera White, Monte Rosa, Serizzo, Viscont White"),
        ("Graue Granitsteine", "#9a9a98", "Azul California, Basaltino, Grigio Carnico, Onsernone, Padang hell, Padang Kristall, Padang Rosa, Quarzit Silber, Rosa Beta, Super Grey"),
        ("Grüne Granitsteine", "#56715a", "Ice Green, Kashmir White, Verde Maritaca, Verde Oliva, Verde Spluga, Tropic Brown, Verde Eucalyptus"),
        ("Cremefarbige Granitsteine", "#e8dcc0", "Jura Gelb-Kalkstein"),
        ("Rote Granitsteine", "#93463a", "Aurora India, Balmoral, Multicolor Rot, Rosa Porrinho, Rosa Sardo, Tan Brown"),
        ("Blaue Granitsteine", "#3d5873", "Azul Macaubas, Azul Noce, Azul Platino, Baltic Blau, Blue Eyes, Fantastic Blue, Labrador Antic, Labrador Blue Pearl, Labrador Hell, Orissa Blue, Vitzag Blue"),
        ("Braune Granitsteine", "#6b4a33", "Baltic Braun, Breccia Imperiale, Coffestone, Fox Brown, Giallo Venezia, Quarzit Brown, Teak Stone"),
        ("Bunte Granitsteine", "linear-gradient(135deg,#c79a5a,#7c5a8a,#4f7b6b)", "Belorizonte, Incas Gold, Ivory Brown, Juparana Colombo, Juparana India, Kinawa, Melur Melody, Padang Gelb, Paradiso, Pegasus"),
    ]
    g = "".join(f'<div class="color-group"><h4><span class="dot" style="background:{c}"></span>{t}</h4>{chips(n.split(", "))}</div>' for t, c, n in groups)
    return (
        hero("naturstein-09.jpg", "Naturstein", "Natursteinplatten für innen und außen",
             "Egal, ob im Innen- oder Außenbereich – Natursteinplatten überzeugen durch Langlebigkeit und eine individuelle, wandelbare Optik.")
        + section(
            '<div class="split">'
            '<div><p class="lead">Von Terrassen über Wege und Treppen bis hin zu <a href="lightstone.html">Arbeitsplatten</a> und Waschtischen bietet Naturstein zahlreiche Gestaltungsmöglichkeiten für Ihren Wohnraum.</p>'
            '<p>Ob Sie eine kühle, zeitlose Optik bevorzugen oder eine warme Atmosphäre schätzen, spielt dabei keine Rolle – je nach Material und Oberflächenbearbeitung können unsere Natursteinplatten unterschiedliche Wirkungen erzielen.</p>'
            '<p><b>Steigern Sie das Ambiente Ihres Wohnbereiches und lassen Sie sich bei uns in Altbach beraten!</b></p></div>'
            f'<div class="grid grid-2">{figure("naturstein-01.jpg", "", "Küche mit Granitarbeitsplatte")}{figure("naturstein-02.jpg", "", "Granitarbeitsplatte im Detail")}</div>'
            '</div>')
        + section(
            '<div class="split split--top">'
            '<div><h2>Wir bieten Ihnen Natursteinplatten aus aller Welt</h2>'
            '<p>Bei Eberhard Bäder Natursteine und Glas in der Nähe von Stuttgart erwarten Sie hochwertige Natursteinplatten für jeden Anspruch. Unsere Natursteine kommen aus aller Welt, insbesondere aus Indien, Afrika, Brasilien, Italien, Spanien und China. Nennen Sie uns Ihre Wünsche und Anforderungen – wir finden garantiert die passende Natursteinplatte für Sie!</p>'
            '<p>Natursteine bestechen durch ihren individuellen Charakter: Kein Stein gleicht dem anderen in Zusammensetzung, Maserung und Färbung. Unsere Platten sind hitzeunempfindlich, robust und pflegeleicht und werden nicht zuletzt aufgrund ihrer zahlreichen Gestaltungsmöglichkeiten von unseren Kunden geschätzt.</p>'
            '<p>Rufen Sie uns bei weiteren Fragen gerne an oder besuchen Sie unsere <a href="raeumlichkeiten.html#ausstellung">Ausstellung</a> in Altbach, ganz in der Nähe von Stuttgart!</p></div>'
            '<div class="facts">'
            '<div class="fact"><b>250–280 cm</b><span>Plattenlänge, in Ausnahmefällen bis zu 310 cm</span></div>'
            '<div class="fact"><b>20 und 30 mm</b><span>Lieferbare Plattenstärken</span></div>'
            '<div class="fact"><b>Poliert</b><span>oder in leathertouch, teilweise auch in forto (geflammt und gebürstet)</span></div>'
            '<div class="fact"><b>Weltweit</b><span>Indien, Afrika, Brasilien, Italien, Spanien und China</span></div>'
            '</div></div>', "section--white")
        + section(
            head("Fertigung in Altbach", "Vom Rohblock zur fertigen Platte")
            + gallery([("naturstein-03.jpg", ""), ("naturstein-04.jpg", ""), ("naturstein-05.jpg", ""),
                       ("naturstein-06.jpg", ""), ("naturstein-07.jpg", ""), ("naturstein-08.jpg", "")]))
        + section(
            '<div class="split split--top"><div>'
            + head("Sortiment", "Diese Materialien haben wir im Sortiment", "Alle Sorten können Sie vor Ort ansehen und reservieren. Bilder vieler Sorten finden Sie in unserer <a href=\"downloads.html#bilddatenbank\">Bilddatenbank</a>.")
            + g + '</div>'
            f'<div class="stack">{photo("naturstein-10.jpg", "Bearbeitung einer Natursteinplatte", "photo--tall")}{photo("naturstein-09.jpg", "Natursteinplatten im Lager", "photo--wide")}</div>'
            '</div>', "section--white")
        + section('<div class="narrow">' + technik(
            ["<b>Profil 1:</b> Oberseite 1/4 Rundung, unten Fasen und Unterseite 50 mm Tiefe geschliffen",
             "<b>Profil 2:</b> Vorderseite 1/2 Rundung, unten Fasen und Unterseite 50 mm Tiefe geschliffen",
             "<b>Profil 3:</b> Vorderseite Buchrückenform und Unterseite 50 mm Tiefe geschliffen",
             "<b>Profil 4:</b> Oberseite 10 mm Fasen, unten Fasen und Unterseite 50 mm geschliffen",
             P5, P6, P9, PSTRATOS],
            AUSSCHNITTE,
            "Wandabschlussprofile in einer Höhe von 30 bis 100 mm und einer Stärke von 12 mm nach Kundenwunsch.") + '</div>')
        + cta()
    )


# ---------------------------------------------------------------- Silestone

@page("silestone.html", "Silestone Natursteinplatten für Küche &amp; Bad",
      "Bei uns in Altbach nahe Esslingen erwarten Sie hochwertige Silestone Natursteinplatten, die außergewöhnlich stabil und belastbar sind.")
def p_silestone():
    sorts = ("Altair (poliert und suede), Aluminio Nube (poliert und suede), Amarillo Palmira (poliert und suede), Amazon (poliert, suede und volcano), "
             "Arden Blue (poliert, suede und volcano), Azul Ugarit (poliert und suede), Beige Daphne (poliert), Black Dragon (poliert), Blanco Capri (poliert, suede und volcano), "
             "Blanco Maple (poliert und suede), Blanco Norte (poliert und suede), Blanco River (poliert, suede und volcano), Blanco Stellar (poliert und suede), "
             "Blanco Zeus (poliert, suede und volcano), Brazilian Brown (poliert), Carbono (poliert und suede), Cemento SPA (poliert, suede und volcano), Chrome (poliert und suede), "
             "Crema Minerva (poliert und suede), Cygnus (poliert und suede), Daria (poliert und suede), Dinux (poliert und suede), Doratus (poliert und suede), Dreis (poliert und suede), "
             "Eros Stellar (poliert), Gedatsu (poliert und suede), Giallo Nova (poliert), Gris Expo (poliert, suede und volcano), Haiku (poliert, suede und volcano), Hallay (poliert), "
             "Helix (poliert und suede), Istmo (poliert und suede), Kensho (poliert, suede und volcano), Kimbler (poliert), Kona Beige (poliert und suede), Lagoon (poliert und suede), "
             "Lyra (poliert und suede), Magenta Energy (poliert), Marron Jupiter (poliert und suede), Merope (poliert und suede), Mont Blanc (poliert und suede), "
             "Negro Anubis (poliert und suede), Negro Stellar (poliert), Negro Tebas (poliert und suede), Pulsar (poliert und suede), Quasar (poliert), Ross Monza (poliert und suede), "
             "Seleno (poliert), Steel (poliert), Tao (poliert), Tigris Sand (poliert, suede und volcano), Unsui (poliert und suede), Vortium (poliert und suede), Verde Fun (poliert), "
             "Verde Ugarit (poliert und suede), White Platinum (poliert), Yukon (poliert und suede), Zirconium (poliert und suede)")
    items = []
    for s in sorts.split("), "):
        name, _, surf = s.rstrip(")").partition(" (")
        items.append(f"{name} <small>{surf}</small>")
    return (
        page_head([("Startseite", "index.html"), ("Naturstein &amp; Keramik", None)], "Silestone Natursteinplatten für Küche &amp; Bad")
        + section(
            '<div class="split split--top">'
            f'<div>{figure("silestone-01.jpg", "Blanco Zeus Arbeitsplatte", extra="photo--wide")}</div>'
            '<div><p class="lead">Für hochwertige Silestone Natursteinplatten ist die Eberhard Bäder Natursteine und Glas GmbH aus der Nähe von Esslingen Ihr zuverlässiger Ansprechpartner.</p>'
            '<p>Silestone ist ein innovatives Oberflächenmaterial, das aus bis zu 94 Prozent Naturquarz besteht. Diese Komponente ist es auch, die das Produkt so außergewöhnlich stabil und belastbar macht.</p>'
            '<p>Silestone ist die einzige Quarzoberfläche mit einem integrierten Hygieneschutzkomplex. Dank dieser Technologie verfügen die Natursteinplatten über hervorragende hygienische Eigenschaften, die sie zu einem idealen Produkt für Küche und Bad machen. Bei uns in Altbach nahe Esslingen erhalten Sie Silestone Natursteinplatten in vielen verschiedenen Farbtönen und drei unterschiedlichen Oberflächenausführungen.</p></div>'
            '</div>', "section--tight")
        + section(
            '<div class="split split--top"><div>'
            '<h2>Entdecken Sie die Gestaltungsmöglichkeiten mit Natursteinplatten</h2>'
            '<p>Silestone bietet Ihnen eine Vielzahl von Gestaltungsmöglichkeiten: von der Küchen- oder Badabdeckung über Boden- und Wandverkleidung bis hin zum Design einer kompletten Einrichtung.</p>'
            '<p>Durch die langlebigen Eigenschaften ist Silestone eine Investition in die Zukunft.</p></div>'
            '<div class="facts">'
            '<div class="fact"><b>300 x 138 cm</b><span>Tafelgröße</span></div>'
            '<div class="fact"><b>12, 20, 30 mm</b><span>Lieferbare Plattenstärken</span></div>'
            '<div class="fact"><b>3 Oberflächen</b><span>poliert, Suede (leathertouch) und Volcano</span></div>'
            '<div class="fact"><b>bis 94 %</b><span>Naturquarz</span></div>'
            '</div></div>', "section--white")
        + section(head("Sortiment", "Diese Materialien haben wir im Sortiment", "In Klammern: lieferbare Oberflächen.") + chips(items))
        + section('<div class="narrow">' + technik(
            [P5.replace("50 mm Tiefe", "50 mm"), P6, P9,
             "<b>Profil 10:</b> Vorderseite gebrochen, oben und unten gefast, Unterseite geschliffen.", PSTRATOS],
            AUSSCHNITTE,
            "Auch Wandabschlussprofile in 30 bis 100 mm Höhe und 10 bis 30 mm Stärke sind auf Kundenwunsch möglich.") + '</div>', "section--white")
        + cta("Sprechen Sie uns an!")
    )


# ---------------------------------------------------------------- Lightstone

@page("lightstone.html", "Lightstone Küchenarbeitsplatten",
      "Unsere Lightstone Arbeitsplatten sind umweltfreundlich, pflegeleicht, hygienisch und höchst resistent gegen Flecken des täglichen Gebrauchs.")
def p_lightstone():
    faq = [
        ("Wie dicht und säurebeständig ist das Material?", "Das porenlose und hochverdichtete Quarzkompositmaterial macht Lightstone höchst resistent gegen Flecken. So hält es auch Produkten des alltäglichen Gebrauchs wie Fett, Öl, Kaffee, Zitrussaft oder Essig stand."),
        ("Wie hygienisch sind die Küchenarbeitsplatten?", "Lightstone ist ein sicheres hygienisches Produkt. Aufgrund des kompakten Materials und der wasserabweisenden Oberfläche sind die Küchenarbeitsplatten, die Sie bei uns in der Nähe von Stuttgart kaufen können, optimal für die ganze Familie geeignet."),
        ("Wie pflegeleicht sind die Arbeitsplatten?", "Die Oberflächen sind von Haus aus sehr pflegeleicht und hygienisch. Dennoch benötigen sie immer mal wieder ein paar „Streicheleinheiten“. Zur täglichen Reinigung genügt das Abwischen mit einem normalen Tuch und einem geeigneten Reinigungsmittel. Bei stärkeren Verschmutzungen empfehlen wir einen nicht scheuernden Schwamm."),
        ("Welches System verfolgt Lightstone?", 'Durch die im Vergleich zu anderen Herstellern geringere <a href="#farben">Farbkollektion</a> ist es nur bei Lightstone möglich, dem Kunden ein Quarzkompositmaterial im Einstiegssegment anzubieten. Die Qualität und die einzelnen Anteile der Komponenten, zum Beispiel der Quarzanteil, ist die gleiche wie bei anderen Anbietern.'),
        ("Wie nachhaltig sind die Küchenarbeitsplatten?", "Lightstone Arbeitsplatten sind sehr umweltfreundlich. Sie bestehen zu einem sehr hohen Anteil aus Quarz und durchlaufen einen nachhaltigen Produktionsprozess mit zertifizierter Qualität, um die natürlichen Ressourcen optimal zu schützen."),
    ]
    f = "".join(acc(q, f"<p>{a}</p>", i == 0) for i, (q, a) in enumerate(faq))
    return (
        page_head([("Startseite", "index.html"), ("Naturstein &amp; Keramik", None)], "Küchenarbeitsplatten für Stuttgart und Umgebung")
        + section(
            '<div class="split">'
            f'<div>{img("lightstone-02.jpg", "Lightstone – The Lightning Solution", "logo-img")}<p class="lead" style="margin-top:24px">Lightstone ist ein qualitatives Quarzkompositmaterial, das zur Produktion von Küchenarbeitsplatten verwendet wird.</p>'
            '<p>Die Grundlage für dieses hochwertig hergestellte Material sind sorgfältig ausgewählte Rohstoffe, wie zum Beispiel Quarz oder natürliche Farbpigmente. Küchenarbeitsplatten aus Lightstone erhalten Sie <b>exklusiv bei uns in Altbach</b> nahe Stuttgart in 12 mm Materialstärke.</p></div>'
            f'<div>{figure("lightstone-10.jpg", "Arbeitsplattendekor Dalia Nube", extra="photo--wide")}</div>'
            '</div>', "section--tight")
        + section('<div class="split split--top"><div>'
                  + head("Gut zu wissen", "Was Sie über unsere Arbeitsplatten wissen sollten")
                  + '<p>In Altbach bei Stuttgart bieten wir Ihnen qualitätsvolle Küchenarbeitsplatten, die die aktuellsten Sicherheitsanforderungen erfüllen. Sehen Sie selbst!</p></div>'
                  f'<div>{f}</div></div>', "section--white")
        + section(head("Bilder", "Lightstone in der Küche")
                  + gallery([("lightstone-03.jpg", "Gebürstete Oberfläche im Material Corda Melia"), ("lightstone-04.jpg", "Detailbild Dalia Nube"),
                             ("lightstone-05.jpg", "Detailbild Dalia Nube"), ("lightstone-06.jpg", "Arbeitsplattendekor Bianco Dorata"),
                             ("lightstone-07.jpg", "Arbeitsplattendekor Corda Melia"), ("lightstone-08.jpg", "Detailbild Dalia Nube"),
                             ("lightstone-09.jpg", "Detailbild Dalia Nube"), ("lightstone-11.jpg", "Detailbild Bianco Dorata"),
                             ("lightstone-12.jpg", "Detailbild Bianco Dorata")]))
        + section(
            '<div class="split split--top"><div>'
            + head("Material", "Farben und Oberflächen")
            + '<p>Sie bekommen Lightstone Quarzsteinplatten in hochglänzenden oder gebürsteten Oberflächenveredelungen. Alle Materialien haben wir für Sie ständig am Lager. Sie können sich die Platten live vor Ort anschauen und reservieren lassen.</p>'
            '<ul class="spec-list"><li><b>Tafelgröße</b><span>305 x 140 cm</span></li><li><b>Plattenstärke</b><span>12 mm</span></li><li><b>Oberflächen</b><span>poliert und leathertouch</span></li></ul></div>'
            '<div>' + swatches([("lightstone-material-02.jpg", "Arco Venata"), ("lightstone-material-03.jpg", "Grigio Ouro"),
                                ("lightstone-material-04.jpg", "Bianco Dorata"), ("lightstone-material-05.jpg", "Avorio Luras"),
                                ("lightstone-material-06.jpg", "Corda Melia"), ("lightstone-material-07.jpg", "Dalia Nube")], square=True) + '</div>'
            '</div>', "section--white", "farben")
        + section(
            '<div class="split"><div><h2>Zertifizierte Sicherheit</h2><p>Lightstone Quarzarbeitsplatten erfüllen schon heute die modernsten und sicherheitsrelevantesten Anforderungen und haben dadurch folgende Zertifikate:</p></div>'
            f'<div class="grid grid-2"><div class="framed">{img("lightstone-14.jpg", "NSF-Zertifikat")}</div><div class="framed">{img("lightstone-15.jpg", "GREENGUARD Indoor Air Quality Certified")}</div></div></div>')
        + cta()
    )


# ---------------------------------------------------------------- Neolith

@page("neolith-keramik.html", "Neolith – Küchenarbeitsplatten aus Keramik",
      "Neolith eignet sich besonders für Küchenarbeitsplatten, da es hygienisch, leicht zu reinigen sowie absolut kratz-, hitze- und UV-beständig ist.")
def p_neolith():
    props = [
        ("leicht", "Die Stärke der keramischen Platten erleichtert den Transport und die Handhabung und reduziert gleichzeitig den Belastungsfaktor des Unterbaus."),
        ("wasserundurchlässig", "Neolith ist mit seinem Absorptionsgrad von nahezu Null undurchlässig für Wasser und unempfindlich gegen Flüssigkeiten."),
        ("einfach zu reinigen", "Widerstandsfähigkeit gegen alle chemischen Reinigungsmittel, wie Bleiche oder Ammoniak."),
        ("hygienisch", "Es setzt keine Schadstoffe frei und ist geeignet für den Kontakt mit Lebensmitteln."),
        ("temperaturbeständig", "Es verbrennt nicht beim Kontakt mit Feuer und setzt weder Rauch noch Giftstoffe frei, wenn es hohen Temperaturen ausgesetzt wird."),
        ("verschleißbeständig und abriebfest", "Seine harte Oberfläche macht Neolith kratzfest und abriebfest."),
        ("biegesteif", "Es ist somit widerstandsfähig gegen hohe Belastungen und Drücke."),
        ("umweltfreundlich", "Da es vollständig aus natürlichen Materialien besteht, setzt es keine umweltschädlichen Substanzen frei und ist vollständig recyclingfähig."),
    ]
    pr = "".join(f'<div class="card"><h4>… {t}.</h4><p class="muted" style="margin:0">{d}</p></div>' for t, d in props)
    sw = [(f"neolith-keramik-{i:02d}.jpg", "") for i in range(12, 26)]
    return (
        page_head([("Startseite", "index.html"), ("Naturstein &amp; Keramik", None)], "Küchenarbeitsplatten aus Keramik")
        + section(
            '<div class="split">'
            f'<div>{img("neolith-keramik-02.jpg", "Neolith by TheSize", "logo-img")}'
            '<p class="lead" style="margin-top:24px">Bei NEOLITH handelt es sich um die größte Hightech-Keramik-Platte weltweit.</p>'
            '<p>Besonders in Küche, Bad und Wohnraum geht der Trend immer mehr hin zu großformatigen Fliesen, was NEOLITH so beliebt bei unseren Kunden aus dem Raum Stuttgart macht.</p>'
            '<p>Hergestellt wird die Keramik aus natürlichen, sorgfältig ausgewählten Rohstoffen, wie zum Beispiel Quarzsand, Mineralien, Feldspat oder Tonerde.</p>'
            '<p>Besonders beliebt sind die Keramik-Platten auch aufgrund ihrer außergewöhnlich dünnen Plattenstärke von 3, 5 oder 12 mm. Vor allem bei Küchenarbeitsplatten erleichtert dies den Transport, die Handhabung und Lagerung.</p></div>'
            f'<div>{photo("neolith-keramik-03.jpg", "Neolith Arbeitsplatte mit Spüle", "photo--tall")}</div>'
            '</div>', "section--tight")
        + section(
            '<div class="split split--rev">'
            '<div><span class="eyebrow">Nachhaltig</span><h2>Neolith ist 100 % Natur.</h2>'
            '<p>Nachhaltig und umweltfreundlich, besteht vollständig aus natürlicher Tonerde, Feldspat, Quarzsand und Mineraloxiden.</p>'
            '<p>Unter wesentlich höherem Druck hergestellt als herkömmliche Keramik, erfüllt Neolith alle in Europa geltenden Umweltschutzstandards.</p>'
            '<p>Auch Entwicklung und Herstellung erfolgen unter Berücksichtigung von Nachhaltigkeitskriterien und leisten einen wertvollen Beitrag für Umwelt und Gesellschaft.</p></div>'
            f'<div>{photo("neolith-keramik-04.jpg", "Küche mit Neolith Arbeitsplatte", "photo--tall")}</div>'
            '</div>', "section--white")
        + section(
            '<div class="narrow"><h2>Beständige, hygienische Küchenarbeitsplatten kaufen</h2>'
            '<p>NEOLITH ist für die unterschiedlichsten Anwendungen im Innen- und Außenbereich geeignet. Dazu zählen unter anderem Wandverkleidungen, Fußböden, Fassaden und Küchenarbeitsplatten, die wir Ihnen in Altbach bei Stuttgart anbieten.</p>'
            '<p>Die Porzellan-Keramik, aus der die Küchenarbeitsplatten hergestellt sind, ist absolut lebensmittelecht, d. h. Bakterien und Verfettungen können nicht in die Oberfläche eindringen. Zudem ist das Material hygienisch, temperaturbeständig, leicht zu reinigen und setzt keine Schadstoffe frei. Ob als Küchenarbeitsplatte, als Nischenrückwand oder Waschtisch – die NEOLITH Keramik-Platten überzeugen durch absolute Kratz-, Hitze- und UV-Beständigkeit und sind damit der perfekte Partner auch bei stärkeren Beanspruchungen.</p>'
            '<p>Ebenso wie die <a href="lightstone.html">Küchenarbeitsplatten von Lightstone</a> erfüllen auch die NEOLITH Arbeitsplatten modernste sicherheitstechnische Anforderungen. Lassen Sie sich ausführlich in unseren <a href="raeumlichkeiten.html#ausstellung">Ausstellungsräumen</a> in der Nähe von Stuttgart beraten! Bei weiteren Fragen stehen wir Ihnen natürlich auch telefonisch oder per <a href="kontakt-anfahrt.html">E-Mail</a> zur Verfügung.</p></div>'
            '<div style="margin-top:40px">' + gallery([("neolith-keramik-05.jpg", ""), ("neolith-keramik-06.jpg", ""), ("neolith-keramik-07.jpg", ""),
                                                        ("neolith-keramik-08.jpg", ""), ("neolith-keramik-09.jpg", ""), ("neolith-keramik-10.jpg", "")]) + '</div>')
        + section(
            '<div class="split split--top">'
            f'<div>{head("Farbmuster", "Farbmuster")}{figure("neolith-keramik-11.jpg", "Musterbox")}</div>'
            f'<div>{swatches(sw, square=True)}</div></div>', "section--white")
        + section(head("Technische Eigenschaften", "Neolith ist …") + f'<div class="grid grid-4">{pr}</div>')
        + section(
            '<div class="split split--top">'
            '<div><h3>Tafelgrößen</h3><ul class="spec-list">'
            '<li><b>6+ mm</b><span>Das Tafelmaß der Rohtafeln aus Keramik bei 6+ mm Materialstärke beträgt 320 x 150 cm.</span></li>'
            '<li><b>12 mm</b><span>Das Tafelmaß der Rohtafeln aus Keramik bei 12 mm Materialstärke beträgt 320 x 150 cm.</span></li>'
            '<li><b>Oberfläche</b><span>Keramik-Oberflächen sind rau.</span></li></ul></div>'
            '<div><h3>Sicherheitszertifikate</h3><p>Wie auch Lightstone erfüllt Neolith Keramik heute schon die modernsten und sicherheitsrelevantesten Anforderungen und hat dadurch folgende Zertifikate:</p>'
            f'<div class="framed">{img("neolith-keramik-26.jpg", "U.S. Green Building Council Member und GREENGUARD Indoor Air Quality Certified")}</div></div>'
            '</div>', "section--white")
        + section('<div class="narrow">' + technik(
            [P5, P6, "<b>Profil 5:</b> Oberseite und Unterseite mit Fasen 3 mm.", P9],
            ["Viereck gesägt für Auflageteile; Viereck flächenbündige Teile; Viereck für Unterbauteile (nur 12 mm)",
             AUSSCHNITTE[1], AUSSCHNITTE[2], AUSSCHNITTE[3],
             "Ovalausschnitt gesägt für Auflageteile; Ovalausschnitt für Unterbauteile (nur 12 mm)",
             AUSSCHNITTE[5], "Stärke 3+3 mm nur in Verbindung mit Profil 9 (wegen Klebefuge)"],
            "Wandabschlussprofile in einer Höhe von 50 bis 100 mm") + '</div>')
        + section(
            '<div class="split">'
            f'<div style="max-width:360px">{img("neolith-keramik-27.jpg", "Titelseite der Neolith Easy Endkundenbroschüre", "plain-img")}</div>'
            '<div><span class="eyebrow">Download</span><h2>Unsere neue Endkundenbroschüre für Sie</h2>'
            '<p>Neolith Easy 2026 – alle Dekore und Informationen auf einen Blick.</p>'
            '<a class="file" href="assets/pdf/neolith-easy-endkundenbroschuere.pdf" download><span class="ico">PDF</span><span><b>Neolith Easy 2026</b><span>Endkundenbroschüre · PDF · 3,3 MB</span></span></a></div>'
            '</div>', "section--white")
        + cta()
    )


# ---------------------------------------------------------------- Dekton

@page("dekton.html", "Dekton", "Dekton ist ein ultrakompaktes Material aus Glas, Keramik und Quarz – erhältlich bei Bäder Natursteine und Glas in Altbach.")
def p_dekton():
    sort = ["Sirius", "Danae", "Sirocco", "Kadum", "Ananké", "Domoos", "Keranium", "Strato", "Ariane", "Halo", "Spectra", "Zenith", "Aura", "Naone"]
    return (
        hero("dekton-01.jpg", "Naturstein &amp; Keramik", "Dekton", "Ultrakompakt, langlebig – ein Material, das ein Leben lang hält.")
        + section(
            '<div class="split split--top">'
            '<div><h2>Was ist Dekton?</h2>'
            '<p class="lead">Dekton ist die neue Farbkollektion der Fa. Cosentino und wird in dem sogenannten „Particle Sintering Technology“-Verfahren hergestellt.</p>'
            '<p>Bei dieser Methode werden Mineralpartikel derart gesintert, dass sie sich untereinander verbinden, ihre innere Struktur ändern und verdichten. Seine Bestandteile sind Glas, Keramik und Quarz.</p>'
            '<p>Dekton ist ein ultrakompaktes Produkt (ähnlich wie Keramik), das ein Leben lang hält.</p></div>'
            '<div><h3>Tafelgrößen</h3><div class="facts">'
            '<div class="fact"><b>320 x 144 cm</b><span>Tafelgröße</span></div>'
            '<div class="fact"><b>8, 12, 20 mm</b><span>Erhältliche Plattenstärken</span></div></div>'
            f'<div style="margin-top:28px">{figure("dekton-01.jpg", "Ariane", extra="photo--wide")}</div></div>'
            '</div>', "section--white")
        + section('<div class="split"><div>' + head("Sortiment", "Diese Materialien haben wir im Sortiment") + chips(sort) + '</div>'
                  f'<div>{figure("dekton-02.jpg", "Keranium", extra="photo--wide")}</div></div>')
        + section('<div class="narrow">' + technik([P5.replace("50 mm Tiefe", "50 mm"), P6, P9], AUSSCHNITTE) + '</div>', "section--white")
        + cta()
    )


# ---------------------------------------------------------------- Laminam

LAMINAM_KOLL = [
    ("I-NATURALI", "i-naturali", ["laminam-i-naturali-01.jpg", "laminam-i-naturali-02.jpg"], ""),
    ("IN-SIDE", "in-side", ["laminam-in-side-01.jpg"],
     "<p><b>Makellose Optik und Kontinuität zwischen Materialkern und Oberfläche.</b></p><p>Die Steine der großen italienischen Architekturtraditionen wie Porphyr, Piasentina und Cardoso. Diese Materialien, die seit der Antike für ihre Festigkeit, Widerstandsfähigkeit und gleichzeitig große ästhetische Leistung bekannt sind, haben die IN-SIDE-Kollektion inspiriert.</p>"),
    ("OSSIDO", "ossido", ["laminam-ossido-01.jpg"], ""),
    ("CALCE", "calce", ["laminam-calce-01.jpg", "laminam-calce-02.jpg"], ""),
    ("DIAMOND", "diamond", ["laminam-diamond-01.jpg"], ""),
    ("FOKOS", "fokos", ["laminam-fokos-01.jpg"], ""),
]


@page("laminam.html", "Laminam – Keramikarbeitsplatten für Ihre Küche",
      "Keramikplatten von Laminam: jede Oberfläche ein Unikat, in 5, 12 und 20 mm Stärke. Kollektionen I-Naturali, In-Side, Ossido, Calce, Diamond und Fokos.")
def p_laminam():
    koll = ""
    for name, anchor, imgs, text in LAMINAM_KOLL:
        pics = "".join(f'<div class="framed" style="margin-bottom:14px">{img(i, "Laminam Kollektion " + name)}</div>' for i in imgs)
        koll += (f'<div id="{anchor}" class="card" style="scroll-margin-top:110px"><span class="eyebrow">Kollektion</span><h3>{name}</h3>{text}{pics}</div>')
    nav_k = '<nav class="subnav" aria-label="Kollektionen">' + "".join(f'<a href="#{a}">{n.title()}</a>' for n, a, _, _ in LAMINAM_KOLL) + '</nav>'
    return (
        page_head([("Startseite", "index.html"), ("Naturstein &amp; Keramik", None)], "Keramikarbeitsplatten für Ihre Küche")
        + section(
            '<div class="split">'
            f'<div>{img("laminam-01.jpg", "Laminam – Superior Natural Surfaces", "logo-img")}'
            '<p class="lead" style="margin-top:24px">Keramikplatten von Laminam sind kein Mainstream-Produkt. Hier ist jede Oberfläche ein Unikat!</p>'
            '<p>Die Dekore stehen in den Stärken 5 mm, 12 mm und 20 mm für Sie zur Auswahl.</p>'
            '<p>Die innovativen Oberflächen bieten für jeden Geschmack, jedes Interieur und jeden Kunden die passende Wahl. Die erhältlichen Kollektionen spiegeln die aktuellen Einrichtungstrends ebenso wider wie exklusive Klassiker.</p>'
            '<p>Laminam verleiht modernen Küchen einen besonderen Charme und viel Persönlichkeit.</p></div>'
            f'<div>{photo("laminam-02.jpg", "Küche mit Laminam Keramik", "photo--wide")}</div>'
            '</div>', "section--tight")
        + section(
            '<div class="split split--top">'
            f'<div class="grid grid-2">{photo("laminam-03.jpg", "Laminam Kücheninsel", "photo--tall")}{photo("laminam-04.jpg", "Laminam Küchenzeile", "photo--tall")}</div>'
            '<div><h2>Allgemeine Planungshinweise</h2>' + ul([
                "Sollten zu den Arbeitsplatten Rückwände hinzukommen, so werden diese in der gleichen Materialstärke bestellt und berechnet, um Farb- und Haptik-Unterschiede zu vermeiden.",
                "Kleinstmengen (bis 2 m²) aus Keramik für bspw. Fenstersimse o. ä. sind bestellbar, werden allerdings mit einem Zuschlag von 50 % berechnet.",
                "Ablaufrillen bei Unterbau-Becken sind bei Keramik erst ab 12 mm möglich.",
                "Tafelgröße 3240 x 1620 mm.",
                "Laminam ist in 5 mm, 12 mm und 20 mm Stärke lieferbar."]) + '</div>'
            '</div>', "section--white")
        + section(head("Kollektionen", "Die Laminam-Kollektionen", "Springen Sie direkt zu einer Kollektion:") + nav_k
                  + f'<div class="grid grid-2" style="margin-top:32px">{koll}</div>')
        + cta()
    )


# ---------------------------------------------------------------- Vetroplan

VP_LINES = [
    ("Übersicht", "vetroplan-glasrueckfronten.html"),
    ("Basic Line", "vetroplan-basic-line.html"),
    ("Trend Line", "vetroplan-trend-line.html"),
    ("Steel Art Line", "vetroplan-steel-art-line.html"),
    ("Life Line", "vetroplan-life-line.html"),
    ("Digital Print Line", "vetroplan-digital-print-line.html"),
]


def vp_head(slug, banner, title):
    return (page_head([("Startseite", "index.html"), ("Vetroplan Glasrückfronten", "vetroplan-glasrueckfronten.html")], title)
            .replace("</div></section>", f'<div style="margin-top:20px;max-width:420px">{img(banner, title)}</div>{subnav(VP_LINES, slug)}</div></section>'))


@page("vetroplan-glasrueckfronten.html", "Vetroplan Glasrückfronten – moderne Wandverkleidungen aus Glas",
      "Mit den modernen Glasrückfronten von Vetroplan verleihen Sie Ihrer Traumküche einen ganz besonderen Touch! Lassen Sie sich beraten.")
def p_vetroplan():
    lines = [
        ("vetroplan-basic-line.html", "vp-03.jpg", "Basic Line", "Die wichtigsten Grundfarben in 6 bis 12 mm und vielen Oberflächen."),
        ("vetroplan-trend-line.html", "vp-04.jpg", "Trend Line", "Junge, frische Farbtöne – abgestimmt auf die Küchentrends."),
        ("vetroplan-steel-art-line.html", "vp-05.jpg", "Steel Art Line", "Metallische Farbtöne passend zu Griffen und Blenden."),
        ("vetroplan-digital-print-line.html", "vp-06.jpg", "Digital Print Line", "Ihr Wunschmotiv – auf Glas gedruckt."),
        ("vetroplan-life-line.html", "vp-07.jpg", "Life Line", "Neu ab 2014: 6 Grundfarbtöne im Einstiegssegment."),
    ]
    return (
        hero("vp-08.jpg", "Glas", "Moderne Wandverkleidungen aus Glas von Vetroplan",
             "Sie lieben das Besondere und möchten Ihre Küche individuell nach Ihrem Geschmack gestalten?",
             f'<div style="margin-top:26px">{subnav(VP_LINES, "vetroplan-glasrueckfronten.html")}</div>', small=False)
        + section(
            '<div class="split">'
            f'<div>{img("vp-01.jpg", "Vetroplan – Die Profis in Sachen Glas", "logo-img")}'
            '<p class="lead" style="margin-top:24px">Mit den modernen Glasrückfronten von <a href="https://www.vetroplan.com/" target="_blank" rel="noopener">Vetroplan</a> verleihen Sie Ihrer Traumküche einen ganz speziellen Touch!</p>'
            '<p>Im Gegensatz zu herkömmlichen Fliesen wird das lackierte Glas an die vorhandenen Gegebenheiten angepasst. Das Ergebnis ist eine hochwertige, sehr hygienische Wandverkleidung aus angepassten großen Elementteilen. Unsere <a href="team.html">Experten</a> aus Altbach bei Stuttgart beraten Sie gerne persönlich!</p></div>'
            f'<div>{photo("vp-09.jpg", "Küche mit Vetroplan Glasrückwand", "photo--wide")}</div>'
            '</div>')
        + section(
            '<div class="split split--top">'
            '<div><h2>Wandverkleidungen aus Glas – Ihre Profis nahe Stuttgart</h2>'
            '<p>Die Vetroplan Glasprodukte können auf unterschiedlichste Art im Innenausbau verwendet werden, zum Beispiel für Glasrückfronten im Küchenbereich, Arbeitsplatten, Thekenkonstruktionen und vieles mehr. Dabei haben Sie die Möglichkeit, die Wandverkleidung individuell in Farbe, Glasstärke und Oberflächenstruktur anzupassen und Ihren Räumlichkeiten somit eine einzigartige Note zu verleihen.</p>'
            '<p>Die Glasrückfronten von Vetroplan sind die einzigen, die serienmäßig als ESG-Sicherheitsglas verarbeitet und somit als Nischenrückfronten im Küchenbereich eingebaut werden können. Denn nur das standardmäßige Sicherheitsglas hält den thermischen und mechanischen Ansprüchen einer Küche (heiße Kochtöpfe, Stöße etc.) stand. <b>Aufgrund unserer langjährigen Erfahrung empfehlen wir Ihnen daher, von nicht vorgespanntem Glas abzusehen!</b></p></div>'
            f'<div style="max-width:340px;margin:0 auto">{img("vp-02.jpg", "Qualität: serienmäßig ESG-Glas")}</div>'
            '</div>', "section--white")
        + section(head("Die Vetroplan-Linien", "Glasrückfronten – gerne auch nach Heidelberg",
                       "In der Nähe von Heidelberg bieten wir Ihnen die Rückfronten in verschiedenen Ausführungen an. Wählen Sie Ihren Favoriten und erleben Sie die zahlreichen kreativen Gestaltungsmöglichkeiten mit Vetroplan!")
                  + '<div class="grid grid-3">' + "".join(tile(h, i, t, d, "Farben ansehen", banner=True) for h, i, t, d in lines) + '</div>')
        + section(head("Inspiration", "Vetroplan in der Küche")
                  + gallery([("vp-08.jpg", ""), ("vp-09.jpg", ""), ("vp-10.jpg", ""), ("vp-11.jpg", "")]), "section--white")
        + cta()
    )


@page("vetroplan-basic-line.html", "Vetroplan Basic Line",
      "Die Vetroplan Basic Line enthält die wichtigsten Grundfarben sowie verschiedene Materialstärken und Oberflächenbearbeitungen.")
def p_basic():
    names = ["B-110 Absolute White", "B-111 Sensitive White", "B-112 Magnolia White", "B-113 Concept White", "B-114 Effect White",
             "B-120 Silent Beige", "B-121 Concept Beige", "B-122 Smooth Beige", "B-123 Deep Beige", "B-130 Silent Red", "B-131 Sensitive Red",
             "B-132 Effect Red", "B-133 Concept Red", "B-134 Mellow Red", "B-135 Intense Red", "B-140 Silent Green", "B-141 Vivid Green",
             "B-150 Silent Brown", "B-151 Concept Brown", "B-152 Vivid Brown", "B-153 Terra Brown", "B-154 Mellow Brown", "B-155 Intense Brown",
             "B-160 Silent Blue", "B-161 Intense Blue", "B-170 Smooth Grey", "B-171 Platin Grey", "B-172 Intense Grey", "B-180 Concept Black", "B-181 Absolute Black"]
    sw = [(f"vp-vetroplan-basic-line-{i + 11:02d}.jpg", n) for i, n in enumerate(names)]
    return (
        vp_head("vetroplan-basic-line.html", "vp-vetroplan-basic-line-01.jpg", "Vetroplan Basic Line")
        + section(
            '<div class="split">'
            '<div><p class="lead">Die Vetroplan Basic Line enthält die wichtigsten Grundfarben.</p>'
            '<p>Sie haben zudem die Möglichkeit, Ihren gewünschten Farbton auf unterschiedliche Materialstärken (6, 8, 10 und 12 mm) sowie unterschiedliche Oberflächenbearbeitungen (Klar, Satinato, Strukturglas, …) zu wählen.</p></div>'
            f'<div>{figure("vp-vetroplan-basic-line-10.jpg", "Vetroplan Musterbox Basic Line")}</div>'
            '</div>', "section--tight")
        + section(head("Farbtöne", "Alle Farben der Basic Line") + swatches(sw), "section--white")
        + section(head("Wirkung", "So wirken die Farben") + gallery([(f"vp-vetroplan-basic-line-{i:02d}.jpg", "") for i in range(2, 10)]))
        + cta()
    )


@page("vetroplan-trend-line.html", "Vetroplan Trend Line",
      "Die Vetroplan Trend Line zeichnet sich durch junge, frische und moderne Farbtöne aus, abgestimmt auf die neuesten Trends der Küchenhersteller.")
def p_trend():
    names = ["T-400 Timeless White", "T-410 Natural Green", "T-411 Concept Green", "T-420 Concept Yellow", "T-430 Natural Apricot",
             "T-440 Concept Orange", "T-450 Silent Petrol", "T-451 Intense Petrol", "T-460 Active Blue", "T-470 Silent Violett"]
    sw = [(f"vp-vetroplan-trend-line-{i + 7:02d}.jpg", n) for i, n in enumerate(names)]
    return (
        vp_head("vetroplan-trend-line.html", "vp-vetroplan-trend-line-01.jpg", "Vetroplan Trend Line")
        + section(
            '<div class="split">'
            '<div><p class="lead">Die Vetroplan Trend Line – das sind junge, frische und moderne Farbtöne, abgestimmt auf die neuesten Trends der Küchenhersteller.</p>'
            '<p>Sie erhalten die Vetroplan Trend Line wahlweise in Hochglanz oder Satinato, standardmäßig in unserem ESG-Glas.</p></div>'
            f'<div>{figure("vp-vetroplan-trend-line-06.jpg", "Vetroplan Musterbox Trend Line")}</div>'
            '</div>', "section--tight")
        + section(head("Farbtöne", "Alle Farben der Trend Line") + swatches(sw), "section--white")
        + section(head("Wirkung", "Trend Line in der Küche") + gallery([(f"vp-vetroplan-trend-line-{i:02d}.jpg", "") for i in range(2, 6)]))
        + cta()
    )


@page("vetroplan-steel-art-line.html", "Vetroplan Steel Art Line",
      "Die Vetroplan Steel Art Line steht für metallische Farbtöne, die Sie in Verbindung mit anderen metallischen Elementen verwenden können.")
def p_steel():
    names = ["S-210 Rich Silver", "S-211 Sensitive Silver", "S-220 Absolute Metallic", "S-221 Sensitive Metallic", "S-230 Rich Bronze", "S-231 Intense Bronze", "S-240 Bright Taupe"]
    sw = [(f"vp-vetroplan-steel-art-line-{i + 2:02d}.jpg", n) for i, n in enumerate(names)]
    return (
        vp_head("vetroplan-steel-art-line.html", "vp-vetroplan-steel-art-line-01.jpg", "Vetroplan Steel Art Line")
        + section(
            '<div class="narrow"><p class="lead">Die Vetroplan Steel Art Line – das sind metallische Farbtöne, die Sie in Verbindung mit anderen metallischen Elementen, wie z. B. Griffen oder Blenden, verwenden können.</p>'
            '<p>Sie haben zudem die Möglichkeit, Ihren gewünschten Farbton auf unterschiedliche Materialstärken (6, 8, 10 und 12 mm) zu wählen.</p>'
            '<p>Sie erhalten die Vetroplan Steel Art Line ausschließlich in Satinato-Oberflächen (matt), standardmäßig in unserem ESG-Glas.</p></div>', "section--tight")
        + section(head("Farbtöne", "Alle Farben der Steel Art Line") + swatches(sw, square=True), "section--white")
        + cta()
    )


@page("vetroplan-life-line.html", "Vetroplan Life Line",
      "Die Vetroplan Life Line bekommen Sie in sechs Grundfarbtönen auf Floatglasbasis. Besuchen Sie uns nahe Esslingen und Stuttgart!")
def p_life():
    names = ["L-510 White on Float", "L-511 Grey on Float", "L-520 Beige on Float", "L-521 Brown on Float", "L-530 Orange on Float", "T-531 Red on Float"]
    sw = [(f"vp-vetroplan-life-line-{i + 3:02d}.jpg", n) for i, n in enumerate(names)]
    return (
        vp_head("vetroplan-life-line.html", "vp-vetroplan-life-line-01.jpg", "Vetroplan Life Line")
        + section(
            '<div class="split">'
            '<div><span class="eyebrow">Neu ab 2014</span><p class="lead">Die Vetroplan Life Line: 6 Grundfarbtöne im Einstiegssegment auf Floatglasbasis.</p>'
            '<p>Sie bekommen die Vetroplan Life Line in Klarglas sowie in Satinato-Oberflächen – standardmäßig natürlich in unserem ESG-Glas.</p></div>'
            f'<div>{figure("vp-vetroplan-life-line-02.jpg", "Vetroplan Musterbox Life Line")}</div>'
            '</div>', "section--tight")
        + section(head("Farbtöne", "Alle Farben der Life Line") + swatches(sw), "section--white")
        + cta()
    )


@page("vetroplan-digital-print-line.html", "Vetroplan Digital Print Line",
      "Setzen Sie individuelle Akzente in Ihrer Küche und lassen Sie Ihre Küchenfront bei uns in Altbach mit Ihrem Wunschmotiv bedrucken!")
def p_digital():
    return (
        vp_head("vetroplan-digital-print-line.html", "vp-vetroplan-digital-print-line-01.jpg", "Vetroplan Digital Print Line")
        + section(
            '<div class="split split--top">'
            '<div><p class="lead">Auf Kundenwunsch bedrucken wir Ihre Glasrückfront mit Motiven Ihrer Wahl.</p>'
            '<p>Bei ausreichender Datenmenge kann jedes beliebige Motiv aufgebracht werden. Vorschläge finden Sie in unserem Vetroplan-Digiprintkatalog.</p>'
            '<p>Wie Ihr Motiv auf das Glas kommt, sehen Sie in unserer <a href="raeumlichkeiten.html#digitalprint">Digitalprint-Abteilung</a>.</p></div>'
            '<div><a class="file" href="assets/pdf/vetroplan-digital-print-broschuere.pdf" download><span class="ico">PDF</span><span><b>Digital Print Broschüre</b><span>Vetroplan-Digiprintkatalog · PDF · 16,2 MB</span></span></a></div>'
            '</div>', "section--tight")
        + section(head("Beispiele", "Vorher und nachher")
                  + gallery([("raum-digitalprint-01.jpg", "Vorher"), ("raum-digitalprint-02.jpg", "Nachher"), ("raum-digitalprint-03.jpg", "Nachher")]), "section--white")
        + cta()
    )


# ---------------------------------------------------------------- Unternehmen

@page("ueber-uns.html", "Über uns &amp; Chronik",
      "Das Natursteinwerk Bäder kann bereits auf eine lange Tradition zurückblicken. Bereits seit 1926 sind wir Ihr Ansprechpartner rund um Glas und Naturstein.")
def p_ueber():
    chron = [
        ("1926", "Schon im Mai 1926 wurde das Natursteinwerk Bäder durch Robert Diehm, den Großvater von Eberhard Bäder, gegründet. Er eröffnete in Altbach eine Steinmetzwerkstatt."),
        ("1947", "1947 übernahm dann dessen Schwiegersohn Walter Bäder das Geschäft. Er setzte die Grabsteinarbeiten fort und erweiterte das Geschäftsfeld in weiser Voraussicht um die damals populären Betonarbeiten."),
        ("1977", "1977 übernahm sein Sohn, Eberhard Bäder, den Betrieb. Seine erfolgreiche Idee war es, auf die Produktion von hochwertigen Küchen- und Badplatten aus edlem Naturstein zu setzen. Damit konnte sich das Unternehmen solide erweitern."),
        ("1995", "1995 zog das Natursteinwerk in das Industriegebiet Altbach in die Straße mit dem wohlklingenden Namen „In den Weiden“. Heute ist neben seiner Ehefrau, Gerda Bäder, auch der gemeinsame Sohn, David Bäder, im Betrieb beschäftigt, der ebenfalls mit seinen innovativen Ideen zum weiteren Erfolg des Unternehmens beiträgt."),
        ("2009", "2009 startet das Unternehmen die eigene Glasproduktion."),
        ("2010", "2010 – das Jahr der Produkteinführung von Vetroplan."),
        ("2012", "2012 steigt David Bäder in die Geschäftsleitung des Unternehmens Natursteinwerk Bäder ein. Ab diesem Zeitpunkt firmiert das Natursteinwerk Bäder in die „Eberhard Bäder Naturstein und Glas GmbH und Co. KG“ um. Im selben Jahr wird der große Anbau an das bestehende Gebäude verwirklicht."),
    ]
    tl = '<ol class="timeline">' + "".join(f'<li><span class="year">{y}</span><p style="margin:0">{t}</p></li>' for y, t in chron) + '</ol>'
    hist = [("uu-chronik-03.jpg", "Visitenkarte aus dem Jahr 1930"), ("uu-chronik-01.jpg", "Ein Messestand der Firma Bäder um das Jahr 1950"),
            ("uu-chronik-02.jpg", "Die damalige Werkstatt"), ("uu-chronik-06.jpg", "Die damalige Seilsäge zum Zuschneiden von Massivteilen"),
            ("uu-chronik-05.jpg", "Eberhard Bäder als Sieger im Bundesleistungswettbewerb beim Bundeskanzler Erhard"), ("uu-chronik-04.jpg", "Die Firma in den 1980er Jahren")]
    return (
        hero("uu-01.jpg", "Über uns", "Familienunternehmen seit 1926", "Firmenstandort in Altbach bei Esslingen")
        + section(
            '<div class="split">'
            f'<div>{figure("uu-02.jpg", "v. l. n. r.: Eberhard, David und Gerda Bäder †", "Eberhard, David und Gerda Bäder", "photo--wide")}</div>'
            '<div><span class="eyebrow">Die Firmengründer und Inhaber</span><h2>Naturstein und Glas aus einer Hand</h2>'
            '<p class="lead">Das Unternehmen Eberhard Bäder Natursteine und Glas GmbH und Co KG ist ein Produzent von Arbeitsplatten für Küchen sowie ein Verarbeiter von Glasnischenrückfronten (Vetroplan) für den Innenausbau.</p>'
            + btns(btn("Unser Team", "team.html"), btn("Unsere Räumlichkeiten", "raeumlichkeiten.html", "ghost")) + '</div>'
            '</div>', "section--white")
        + section('<div class="split split--top"><div>'
                  + head("Chronik", "Die Geschichte der Firma Bäder", "Das Natursteinwerk Bäder hat eine lange Geschichte.")
                  + tl + '</div><div><h3>Aus unserem Archiv</h3>' + gallery(hist) + '</div></div>', id_="chronik")
        + cta()
    )


TEAM = [
    ("Geschäftsleitung", [("David Bäder", ["07153 8313-19"], "david-baeder"), ("Eberhard Bäder", ["07153 8313-28"], "eberhard-baeder"), ("Gerda Bäder †", [], None)]),
    ("Außendienst", [("Gerd Hofmann", ["07153 8313-27", "Mobil 01520 5360590"], "gerd-hofmann"),
                     ("Willi Günthner", ["Mobil 0179 2430977"], None),
                     ("Severine Castaldi", ["07153 8313-28", "Mobil 0155 63411743"], None)]),
    ("Angebote", [("Silvija Ostric", ["07153 8313-15"], "silvija-ostric")]),
    ("Empfang", [("Petra Bendig", ["07153 8313-12"], "petra-bendig"), ("Ester Held", ["07153 8313-11"], "ester-held")]),
    ("Leitung Produktion, Social Media, Verwaltung", [("Emmanouil Taosanis", ["07153 8313-26"], None), ("Nina Bäder", ["07153 8313-16"], "nina-baeder")]),
    ("Technik Glas", [("Sabine Walsh", ["07153 8313-31"], "sabine-walsh"), ("Jeannine Reiser", ["07153 8313-38"], "jeannine-reiser"),
                      ("Ute Geretshauser", ["07153 8313-35"], "ute-geretshauser"), ("Susanna Miloradovic", ["07153 8313-32"], "susanna-miloradovic"),
                      ("Angela Haug", ["07153 8313-13"], "angela-haug")]),
    ("Technik Stein", [("Adam Swais", ["07153 8313-36"], "adam-swais"), ("Gislinde Sobeck", ["07153 8313-37"], "gislinde-sobeck")]),
    ("Disposition", [("Tim Semler", ["07153 8313-30"], "tim-semler")]),
    ("Aufmaß", [("Frank Diez", ["07153 8313-34", "Mobil 0157 53604261"], "frank-diez")]),
    ("Digitaldruck", [("Serafin Bethavas", ["07153 8313-26"], "serafin-bethavas")]),
    ("Buchhaltung", [("Ester Held", ["07153 8313-11"], "ester-held"), ("Karin Strobel", ["07153 8313-12"], "karin-strobel"),
                     ("Panagiota Passaporti", ["07153 8313-12"], "panagiota-passaporti")]),
]


def tel_link(num):
    label = num
    digits = "".join(ch for ch in num if ch.isdigit())
    return f'<a href="tel:+49{digits[1:]}">{label}</a>'


@page("team.html", "Unser Team",
      "Von der Produktion bis hin zum Außendienst sind unsere geschulten und erfahrenen Mitarbeiter gerne für Sie da. Wir freuen uns auf Ihren Auftrag!")
def p_team():
    groups = ""
    for g, people in TEAM:
        rows = ""
        for name, phones, mail in people:
            ph = "".join(f"<span>{tel_link(p)}</span>" for p in phones)
            m = f'<a href="mailto:{mail}@natursteinwerk-baeder.de">{mail}@natursteinwerk-baeder.de</a>' if mail else ""
            rows += f'<div class="contact-row"><b>{name}</b>{ph}{m}</div>'
        groups += f'<div class="card team-group"><h3>{g}</h3>{rows}</div>'
    return (
        page_head([("Startseite", "index.html"), ("Unternehmen", None)], "Unser Team ist gerne für Sie da.",
                  "Alle Ansprechpartner mit Telefonnummer und E-Mail-Adresse. Tippen Sie auf eine Nummer, um direkt anzurufen.")
        + section(
            '<div class="card" style="margin-bottom:28px;display:flex;flex-wrap:wrap;gap:20px 48px;align-items:center">'
            '<h3 style="margin:0">Zentrale</h3>'
            f'<div class="contact-row" style="margin:0"><b>Telefon</b><a href="tel:{TEL_LINK}">07153 8313-0</a></div>'
            '<div class="contact-row" style="margin:0"><b>Telefax</b><span>07153 8313-20</span></div>'
            f'<div class="contact-row" style="margin:0"><b>E-Mail</b><a href="mailto:{MAIL}">{MAIL}</a></div></div>'
            f'<div class="grid grid-3">{groups}</div>', "section--tight")
        + cta()
    )


@page("raeumlichkeiten.html", "Unsere Räumlichkeiten",
      "Unser Familienunternehmen verfügt über ein eigenes Steinlager, Produktionshallen, eine Digitalprint-Abteilung und einen Ausstellungsraum.")
def p_raum():
    cards = [("#steinlager", "raum-01.jpg", "Steinlager", "Über 70 Natursteinsorten zum Ansehen und Reservieren.", "Zum Steinlager"),
             ("#digitalprint", "raum-02.jpg", "Digitalprint", "Ihr eigenes Motiv auf der Glasrückfront.", "Zum Digitalprint"),
             ("#produktion", "raum-03.jpg", "Produktion", "Modernste Maschinen für millimetergenaue Arbeit.", "Zur Produktion"),
             ("#ausstellung", "raum-04.jpg", "Ausstellung", "Muster ansehen und mit nach Hause nehmen.", "Zur Ausstellung")]
    sec = lambda id_, inner, cls="": f'<section class="section {cls}" id="{id_}" style="scroll-margin-top:90px"><div class="wrap">{inner}</div></section>'
    return (
        page_head([("Startseite", "index.html"), ("Unternehmen", None)], "Unsere Räumlichkeiten", "Gerne stellen wir Ihnen unsere Abteilungen vor.")
        + section('<div class="grid grid-4">' + "".join(tile(*c) for c in cards) + '</div>', "section--tight")
        # Ausstellung
        + sec("ausstellung",
              '<div class="split">'
              '<div><span class="eyebrow">Abteilung</span><h2>Ausstellung</h2>'
              '<p class="lead">In unserem Ausstellungsraum können Sie sich ein Bild von den verschiedenen Verarbeitungsmöglichkeiten machen.</p>'
              '<p>Außerdem können Sie sich von allen vorrätigen Materialien aus Stein, Glas, Silestone und Keramik ein passendes Muster für zu Hause mitnehmen. Mit diesem Muster können Sie vor Ort ausprobieren, ob das ausgewählte Material beispielsweise mit Ihrem Fußboden, Ihren Möbeln oder Ihren Wohn-Accessoires harmoniert.</p></div>'
              f'<div>{photo("raum-ausstellung-01.jpg", "Ausstellungsraum", "photo--wide")}</div></div>'
              '<div style="margin-top:36px;max-width:760px">' + person("raum-ausstellung-02.jpg", "Issa Sabokrouh",
              '<h3>Ich bin Issa Sabokrouh, Ihr Kundenberater.</h3><p>Wenn Sie uns besuchen möchten, um Ihr Bauvorhaben zu besprechen, würde ich mich sehr freuen, Sie hier begrüßen zu dürfen. Gerne nehme ich mir Zeit für Sie und Ihr Anliegen.</p>'
              '<p style="margin:0">Um einen Termin zu vereinbaren, freue ich mich über Ihre Nachricht an <a href="mailto:issa-sabokrouh@natursteinwerk-baeder.de">issa-sabokrouh@natursteinwerk-baeder.de</a></p>') + '</div>',
              "section--white")
        # Steinlager
        + sec("steinlager",
              '<div class="split split--top">'
              '<div><span class="eyebrow">Abteilung</span><h2>Steinlager</h2>'
              '<p class="lead">An unserem Lagerplatz finden Sie über 70 unterschiedliche Natursteinsorten.</p>'
              '<p>Weil Natursteine in ihrer natürlichen Farbgebung und Struktur immer schwanken, haben Sie hier die Möglichkeit, das von Ihnen gewünschte Material anzuschauen und für Ihre Küchenarbeitsplatte zu reservieren.</p>'
              '<p>Falls Sie nicht die Möglichkeit haben, unser Lager zu besuchen, so können wir Ihnen vorab ein Bild der aktuellen Steincharge zukommen lassen.</p></div>'
              '<div>' + gallery([("raum-steinlager-01.jpg", "Unser Natursteinlager"), ("raum-steinlager-02.jpg", "Gerne erstellen wir Ihnen eine Einteilung über den Maserungsverlauf"),
                                 ("raum-steinlager-03.jpg", "Steinplatte aus Naturstein „Super Grey“"), ("raum-steinlager-04.jpg", "Steinplatte aus Naturstein „Topazio white“")]) + '</div>'
              '</div>')
        # Produktion
        + sec("produktion",
              head("Abteilung", "Produktion", "Die Eberhard Bäder Natursteine und Glas GmbH und Co KG ist in ihren Produktionshallen mit den modernsten Maschinen ausgerüstet.")
              + gallery([("raum-produktion-01.jpg", "Werkstatt Stein"), ("raum-produktion-02.jpg", "Oberflächenschleifmaschine"), ("raum-produktion-03.jpg", "Werkstatt Glas"),
                         ("raum-produktion-04.jpg", "CNC Produktion in der Steinwerkstatt"), ("raum-produktion-05.jpg", "ESG Ofen"), ("raum-produktion-06.jpg", "CNC Zuschnitt Glas"),
                         ("raum-produktion-08.jpg", "Zugeschnittene Werkstücke")])
              + '<div style="margin-top:36px;max-width:760px">' + person("raum-produktion-07.jpg", "Manfred Feichter",
              '<h3>Guten Tag. Mein Name ist Manfred Feichter.</h3><p style="margin:0">Ich leite die Produktion der Eberhard Bäder Natursteine und Glas GmbH &amp; Co. KG. Zusammen mit meinem Team machen wir im Jahr mit unseren 4 CNC-Fräsen und unserer Wasserstrahl-Schneideanlage ca. 1.600 Küchenarbeitsplatten und ca. 2.700 Glasrückfrontenkommissionen. Wir produzieren mit modernster Technik Granitküchenarbeitsplatten und Glasrückfronten millimetergenau.</p>') + '</div>'
              + '<div class="facts" style="margin-top:28px"><div class="fact"><b>4</b><span>CNC-Fräsen und eine Wasserstrahl-Schneideanlage</span></div>'
              '<div class="fact"><b>ca. 1.600</b><span>Küchenarbeitsplatten im Jahr</span></div><div class="fact"><b>ca. 2.700</b><span>Glasrückfrontenkommissionen im Jahr</span></div></div>',
              "section--white")
        # Digitalprint
        + sec("digitalprint",
              '<div class="split split--top">'
              '<div><span class="eyebrow">Abteilung</span><h2>Digitalprint</h2>'
              '<p class="lead">Durch die Möglichkeiten im Digitalprint entstehen völlig neue und kreative Wege, um Glas zu bedrucken.</p>'
              '<p>Sie möchten Ihre Nischenrückfront in keinem Standard-Uni-Farbton, sondern lieber mit einem individuellen Bild bedruckt? Dann finden Sie hier die richtige Auswahl. Wir können ein selbst gemachtes Bild von Ihnen verwenden oder ein Bild aus einer Bilddatenbank. Folgende Online-Agenturen können wir empfehlen: <a href="http://www.pitopia.de" target="_blank" rel="noopener">www.Pitopia.de</a>, <a href="http://www.shutterstock.com" target="_blank" rel="noopener">www.shutterstock.com</a></p>'
              '<div class="card" style="margin-top:24px"><h4>Mein Tipp:</h4><p>Laden Sie sich am besten unseren Entwurfskatalog herunter und lassen Sie sich inspirieren. Einfach auf den Link klicken und schon kann’s losgehen:</p>'
              + btns(btn("Zum Entwurfskatalog", "http://www.vetroplan.com/vetroplan-farben/digital-line", ext=True), btn("Broschüre als PDF", "assets/pdf/vetroplan-digital-print-broschuere.pdf", "ghost")) + '</div></div>'
              '<div>' + gallery([("raum-digitalprint-01.jpg", "Vorher"), ("raum-digitalprint-02.jpg", "Nachher"), ("raum-digitalprint-03.jpg", "Nachher"),
                                 ("raum-digitalprint-04.jpg", "Digitalprint"), ("raum-digitalprint-05.jpg", "Bildeinteilung")]) + '</div></div>'
              '<div style="margin-top:36px;max-width:760px">' + person("raum-digitalprint-06.jpg", "Gerd Hofmann",
              '<h3>Ich bin Gerd Hofmann</h3><p style="margin:0">und beantworte Ihnen gerne Fragen zum Digitalprint oder Ihre Anfrage. Schreiben Sie mir an <a href="mailto:gerd-hofmann@natursteinwerk-baeder.de">gerd-hofmann@natursteinwerk-baeder.de</a>. Gemeinsam mit Ihnen erarbeiten wir Ihre individuelle Digitalprint-Glasrückfront.</p>') + '</div>')
        + cta()
    )


@page("news-und-mitteilungen.html", "News und Mitteilungen", "Neuigkeiten, neue Produkte und Ankündigungen der Eberhard Bäder Natursteine und Glas GmbH.")
def p_news():
    return (
        page_head([("Startseite", "index.html"), ("Unternehmen", None)], "News und Mitteilungen",
                  "Willkommen bei den News und Mitteilungen der Eberhard Bäder Natursteine und Glas GmbH. Hier informieren wir Sie regelmäßig über neue Produkte, Materialinnovationen und aktuelle Ankündigungen unseres Hauses.")
        + section(
            '<div class="grid grid-2">'
            '<div class="card"><span class="eyebrow">Aktion 2026</span><h3>Neolith EASY Bonusaktion</h3>'
            '<p>500 € Gutschrift für fünf verkaufte Neolith-Keramikarbeitsplatten. Alle Details in unserer Preisübersicht.</p>'
            '<a class="link-arrow" href="download-preislisten.html">Zur Aktion</a></div>'
            '<div class="card"><span class="eyebrow">Download</span><h3>Neue Neolith Easy Endkundenbroschüre</h3>'
            '<p>Alle Dekore und Informationen zu Neolith Easy 2026 als PDF.</p>'
            '<a class="link-arrow" href="neolith-keramik.html">Zur Broschüre</a></div>'
            '</div>', "section--tight")
    )


# ---------------------------------------------------------------- Kontakt

@page("kontakt-anfahrt.html", "Kontakt &amp; Anfahrt",
      "Eberhard Bäder Natursteine und Glas GmbH & Co. KG, In den Weiden 24, 73776 Altbach, Telefonnummer: 07153 83130. Wir freuen uns auf Sie!")
def p_kontakt():
    maps = "https://www.google.com/maps/search/?api=1&query=In+den+Weiden+24%2C+73776+Altbach"
    return (
        page_head([("Startseite", "index.html")], "Kontakt &amp; Anfahrt", "Wir freuen uns auf Ihren Besuch oder Ihren Anruf.")
        + section(
            '<div class="grid grid-3">'
            '<div class="card"><h3>Adresse</h3><p>Eberhard Bäder Natursteine und Glas GmbH und Co KG<br>In den Weiden 24<br>73776 Altbach</p>'
            f'<a class="link-arrow" href="{maps}" target="_blank" rel="noopener">Route planen</a></div>'
            '<div class="card"><h3>Telefon &amp; E-Mail</h3>'
            f'<div class="contact-row"><b>Telefon</b><a href="tel:{TEL_LINK}">+49 7153 8313 0</a></div>'
            '<div class="contact-row"><b>Telefax</b><span>+49 7153 8313 20</span></div>'
            f'<div class="contact-row"><b>E-Mail</b><a href="mailto:{MAIL}">{MAIL}</a></div></div>'
            '<div class="card"><h3>Öffnungszeiten</h3>'
            '<div class="contact-row"><b>Montag bis Mittwoch und Freitag</b><span>8.00 bis 12.20 Uhr<br>und 13.00 bis 17.00 Uhr</span></div>'
            '<div class="contact-row"><b>Donnerstag</b><span>8.00 bis 12.20 Uhr<br>und 13.00 bis 18.00 Uhr</span></div></div>'
            '</div>'
            '<div class="card" style="margin-top:28px;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:16px">'
            '<p style="margin:0">Alle Ansprechpartner mit Telefonnummer und E-Mail-Adresse finden Sie auf unserer Team-Seite.</p>'
            + btn("Zur Team-Seite", "team.html") + '</div>', "section--tight")
        + section(
            '<div class="split">'
            '<div><span class="eyebrow">Anfahrt</span><h2>So finden Sie zu uns</h2>'
            '<p>Unser Firmengelände liegt im Industriegebiet Altbach, ganz in der Nähe von Esslingen und Stuttgart.</p>'
            '<p class="muted" style="font-size:.92rem">Die Karte öffnet sich bei Google Maps. Dabei werden Daten an Google übertragen – mehr dazu in der <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Datenschutzerklärung von Google</a>.</p>'
            + btns(btn("In Google Maps öffnen", maps, ext=True)) + '</div>'
            f'<div><a href="{maps}" target="_blank" rel="noopener" class="photo photo--wide" style="display:block">{img("anfahrt-map.jpg", "Luftbild des Firmenstandorts In den Weiden 24, Altbach", folder="assets")}</a></div>'
            '</div>', "section--white")
        + cta("Besuchen Sie uns in Altbach")
    )


# ---------------------------------------------------------------- Downloads

STONE_NAMES = {"Blue In The Night": "Blue in the Night", "Deepsea": "Deep Sea", "Baltic Green Granite": "Baltic Green Granite"}


def stone_db():
    folder = os.path.join(ROOT, "assets", "bilddatenbank")
    out = []
    for f in sorted(os.listdir(folder), key=str.lower):
        if not f.endswith(".jpg") or f.endswith("-vorschau.jpg"):
            continue
        slug = f[:-4]
        name = " ".join(w.capitalize() for w in slug.split("-"))
        name = STONE_NAMES.get(name, name)
        size = os.path.getsize(os.path.join(folder, f)) / 1024 / 1024
        out.append(f'<a class="stone" href="assets/bilddatenbank/{f}" download>'
                   f'{img(slug + "-vorschau.jpg", name, folder="assets/bilddatenbank")}<span><span>{name}<small>{size:.1f} MB</small></span></span></a>'.replace(f"{size:.1f} MB", f"{size:.1f} MB".replace(".", ",")))
    return f'<div class="stone-grid">{"".join(out)}</div>'


@page("downloads.html", "Downloadcenter",
      "Aktuelle Downloads: Broschüren, Preisliste und unsere Bilddatenbank Naturstein mit über 50 Natursteinsorten zum Herunterladen.")
def p_downloads():
    return (
        page_head([("Startseite", "index.html")], "Downloadcenter", "Hier stehen für Sie aktuelle Downloads zur Verfügung.")
        + section(
            '<div class="grid grid-3">'
            '<a class="file" href="assets/pdf/neolith-easy-endkundenbroschuere.pdf" download><span class="ico">PDF</span><span><b>Neolith Easy</b><span>Endkundenbroschüre · PDF · 3,3 MB</span></span></a>'
            '<a class="file" href="assets/pdf/vetroplan-digital-print-broschuere.pdf" download><span class="ico">PDF</span><span><b>Vetroplan Digital Print</b><span>Broschüre · PDF · 16,2 MB</span></span></a>'
            '<a class="file" href="download-preislisten.html"><span class="ico">€</span><span><b>Preisliste 2025/26</b><span>Tarife &amp; Richtpreise ansehen</span></span></a>'
            '</div>', "section--tight")
        + f'<section class="section section--white" id="bilddatenbank" style="scroll-margin-top:90px"><div class="wrap">'
        + head("Bilddatenbank", "Bilddatenbank Naturstein", "Bilder unserer Natursteinsorten in hoher Auflösung. Tippen Sie auf einen Stein, um das Bild herunterzuladen.")
        + stone_db() + '</div></section>'
    )


@page("download-preislisten.html", "Preisliste &amp; Übersicht 2025/2026",
      "Service-, Montage- und Liefertarife sowie Richtpreise für Naturstein, Vetroplan Glas und Keramik – für Gewerbekunden.")
def p_preise():
    def table(rows):
        r = "".join(f"<tr><td>{a}</td><td>{b}</td><td class=\"num\">{c}</td></tr>" for a, b, c in rows)
        return f'<div class="table-wrap"><table><thead><tr><th>Leistung</th><th>Fläche</th><th style="text-align:right">Preis netto</th></tr></thead><tbody>{r}</tbody></table></div>'

    def price_list(rows):
        r = "".join(f"<tr><td>{a}</td><td class=\"num\">{b}</td></tr>" for a, b in rows)
        return f'<div class="table-wrap"><table><tbody>{r}</tbody></table></div>'
    cats = [
        ("Kategorie 1", "Natursteinwerk", "Über 80 verschiedene Granite, Hartgesteine &amp; Kalksteine am Lager in 20 &amp; 30 mm Stärke.", "ab 247,00 €/m²", "z. B. Rosa Beta 247 €, Bianco Sardo 252 €, Angola Schwarz 393 €"),
        ("Kategorie 2", "Vetroplan Glas", "ESG-Sicherheitsglas, Satinato, Diamantglas (kratzfest), Digitalprints &amp; Leuchtfelder.", "ab 251,00 €/m²", "Life-Line 251 €, Basic-Line 281 €, Steel Art 348 €, Digitalprint 367 €"),
        ("Kategorie 3", "Keramik &amp; High-Tech", "Neolith, Dekton, SapienStone &amp; Laminam. Extrem hitzebeständig und kratzfest.", "ab 322,00 €/m²", "Laminam ab 322 €, Dekton ab 517 € (gesenkt!), Neolith EASY ab 748 €"),
    ]
    c = "".join(f'<div class="card"><span class="eyebrow">{k}</span><h3>{t}</h3><p>{d}</p><div class="fact" style="margin:14px 0"><span>Richtpreis</span><b>{p}</b></div><p class="muted" style="margin:0">{e}</p></div>' for k, t, d, p, e in cats)
    mailto = f"mailto:{MAIL}?subject=" + "Anfrage%20Preisliste%202025%2F26%20(PDF)"
    return (
        page_head([("Startseite", "index.html"), ("Downloads", "downloads.html")], "Preisliste &amp; Übersicht 2025/2026", "Produktkataloge &amp; Tarife")
        + f'<div class="wrap" style="margin-bottom:12px">{GEWERBE_HINWEIS}</div>'
        + section(
            '<div class="grid grid-2">'
            '<div class="card" style="background:var(--stone);color:#e9e6e1;border-color:var(--stone)"><span class="eyebrow" style="color:#b9cde0">Messe-Aktion 2026</span>'
            '<h3 style="color:#fff">Neolith EASY Bonusaktion – 500 € Gutschrift für Sie!</h3>'
            '<p>Verkaufen Sie fünf Neolith Keramikarbeitsplatten und erhalten Sie umgehend eine Gutschrift von 500 Euro netto! 50 % Rabatt auf Aktionsdekore wie Ama Black, Calacatta Roma, Calatorao &amp; Taj Mahal.</p>'
            '<p style="margin:0;font-weight:600;color:#fff">500 € Gutschrift pro 5 Platten</p></div>'
            '<div class="card"><h3>Offizielle Preisliste 2025/26 als PDF</h3><p>Enthält alle technischen Daten, Tafelmaße, Aufpreise und Farbmuster für Gewerbekunden.</p>'
            + btns(btn(ICON_MAIL + "Preisliste PDF anfragen", mailto)) + '</div>'
            '</div>', "section--tight")
        + section(
            head("Tarife", "Zentrale Service- &amp; Montagetarife")
            + '<div class="grid grid-2">'
            '<div><h3>Aufmaß &amp; CAD-Erstellung</h3><p class="muted">Mindestberechnung 2 m²</p>'
            + table([("Aufmaß &amp; CAD", "bis 3 m²", "110,00 €"), ("Aufmaß &amp; CAD", "bis 5 m²", "89,00 €"), ("Aufmaß &amp; CAD", "über 5 m²", "75,00 €"),
                     ("Nur CAD", "bis 3 m²", "44,00 €"), ("Nur CAD", "bis 5 m²", "42,00 €"), ("Nur CAD", "über 5 m²", "37,50 €")]) + '</div>'
            '<div><h3>Montageservice</h3><p class="muted">Durch bei Bäder geschultes Fachpersonal</p>'
            + table([("Montage Arbeitsplatten", "bis 3 m²", "226,00 €"), ("Montage Arbeitsplatten", "bis 5 m²", "194,50 €"), ("Montage Arbeitsplatten", "über 5 m²", "160,00 €"),
                     ("Glasrückwand Montage", "bis 3 m²", "144,50 €"), ("Glasrückwand Montage", "bis 5 m²", "127,00 €"), ("Glasrückwand Montage", "über 5 m²", "119,00 €")]) + '</div>'
            '<div><h3>Lieferkosten pro Auftrag</h3>'
            + price_list([("Regional durch Firma Bäder", "34,00 €"), ("Überregional durch Firma Bäder", "76,50 €"), ("Spedition (Auftragswert bis 250 €)", "102,00 €"),
                          ("Spedition (Auftragswert 250 bis 500 €)", "89,00 €"), ("Spedition (Auftragswert über 500 €)", "76,50 €")]) + '</div>'
            '<div><h3>Strom- &amp; Wasserinstallationen</h3>'
            + price_list([("Deinstallation / Installation je Steckdose", "20,50 €"), ("Installation Kochfeld Standard", "89,00 €"),
                          ("Installation Kochfeld mehrteilig", "129,50 €"), ("Spüle Wasseranschluss", "147,00 €")]) + '</div>'
            '</div>', "section--white")
        + section(head("Richtpreise", "Materialkategorien &amp; Richtpreise") + f'<div class="grid grid-3">{c}</div>')
    )


# ---------------------------------------------------------------- Rechtliches

def legal(slug_title, inner, crumbs_title=None):
    return page_head([("Startseite", "index.html")], slug_title) + section(f'<div class="narrow legal">{inner}</div>', "section--tight")


@page("impressum.html", "Impressum", "Impressum der Eberhard Bäder Natursteine und Glas GmbH & Co. KG aus Altbach nahe Stuttgart.")
def p_impressum():
    return legal("Impressum",
                 '<div class="grid grid-2">'
                 '<div class="card"><h3>Kontakt</h3><p>Eberhard Bäder Natursteine und Glas GmbH und Co KG<br>In den Weiden 24<br>73776 Altbach</p>'
                 f'<p style="margin:0">Telefon <a href="tel:{TEL_LINK}">+49 7153 8313-0</a><br>Fax +49 7153 831320<br>E-Mail <a href="mailto:{MAIL}">{MAIL}</a></p></div>'
                 '<div class="card"><ul class="spec-list"><li><b>Geschäftsführer</b><span>David Bäder</span></li><li><b>Registergericht</b><span>Amtsgericht Esslingen</span></li>'
                 '<li><b>USt-ID</b><span>DE465023755</span></li></ul></div></div>'
                 '<h2>Haftung</h2><p>Die Informationen auf dieser Homepage sind ein Service der Firma Bäder.</p>'
                 '<p>Wir haben diese Website mit der größtmöglichen Sorgfalt zusammengestellt. Trotzdem können wir für absolute Fehlerfreiheit nicht garantieren. Die Fa. Bäder schließt jede Haftung für Schäden aus, die direkt oder indirekt aus der Benutzung der Website entstehen.</p>'
                 '<p>Inhalte dieser Website sind geistiges Eigentum der Eberhard Bäder Natursteine &amp; Glas GmbH &amp; Co. KG. Kopieren und/oder Vermarktung der vorhandenen Daten ist nur durch unsere ausdrückliche Erlaubnis gestattet.</p>')


@page("datenschutz.html", "Datenschutzerklärung", "Datenschutzerklärung der Eberhard Bäder Natursteine und Glas GmbH & Co. KG.")
def p_datenschutz():
    with open(os.path.join(HERE, "datenschutz-text.html"), encoding="utf-8") as f:
        text = f.read()
    return legal("Datenschutzerklärung", text)


@page("cookie-richtlinie.html", "Cookie-Richtlinie", "Welche Cookies und externen Dienste diese Website verwendet.")
def p_cookies():
    return legal("Cookie-Richtlinie",
                 '<p class="lead">Diese Website setzt keine Cookies zur Analyse oder Werbung. Externe Inhalte werden erst geladen, wenn Sie dies ausdrücklich per Klick wünschen.</p>'
                 '<h2>Unbedingt erforderlich</h2><p>Unbedingt erforderliche Cookies ermöglichen grundlegende Funktionen und sind für die einwandfreie Funktion der Website erforderlich. Diese Art von Cookies wird ausschließlich von dem Betreiber der Website verwendet (First-Party-Cookie), und sämtliche Informationen, die in den Cookies gespeichert sind, werden nur an diese Website gesendet. Diese Website benötigt derzeit keine solchen Cookies.</p>'
                 '<h2>Funktionell</h2><p>Funktionelle Inhalte ermöglichen dieser Website, bestimmte Funktionen zur Verfügung zu stellen. Sie werden bei uns nur nach Ihrem Klick aktiviert:</p>'
                 '<h3>YouTube</h3><p>Erst wenn Sie auf „Video abspielen“ klicken, wird das Video von YouTube geladen. Wir verwenden dafür die erweiterte Datenschutz-Einbindung (youtube-nocookie.com). Zusätzliche Cookies werden vom Dienstanbieter YouTube gesetzt und Informationen gesammelt, wenn Sie in Ihrem Google-Konto eingeloggt sind. YouTube registriert anonyme statistische Daten, z. B. wie oft das Video angezeigt wird und welche Einstellungen für die Wiedergabe verwendet werden.</p>'
                 '<p>Anbieter: Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA oder Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland, wenn Sie Ihren Wohnsitz in der EU haben.<br>'
                 'Cookie-Richtlinie: <a href="https://policies.google.com/technologies/cookies" target="_blank" rel="noopener">policies.google.com/technologies/cookies</a><br>'
                 'Datenschutzrichtlinie: <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">policies.google.com/privacy</a></p>'
                 '<h3>Google Maps</h3><p>Die Anfahrtskarte ist auf dieser Website als Bild eingebunden. Erst wenn Sie auf „In Google Maps öffnen“ klicken, wird Google Maps in einem neuen Fenster geöffnet. Anbieter und Richtlinien wie bei YouTube (Google).</p>'
                 '<h2>Performance und Marketing</h2><p>Performance-Cookies sammeln Informationen darüber, wie eine Website genutzt wird. Marketing- bzw. Third-Party-Cookies stammen unter anderem von externen Werbeunternehmen. Diese Website verwendet keine solchen Cookies.</p>')


@page("gewaehrleistung.html", "Gesetzliche Gewährleistung", "Informationen zur gesetzlichen Gewährleistung für Waren, die in der Europäischen Union verkauft werden.")
def p_gewaehr():
    return legal("Gesetzliche Gewährleistung",
                 '<p class="lead">Mindestens zwei Jahre gesetzliche Gewährleistung der Vertragsmäßigkeit für Waren, die in der Europäischen Union verkauft werden.</p>'
                 '<p>Verbraucherinnen und Verbraucher können ihre Rechte im Rahmen des gesetzlichen Gewährleistungsrechts geltend machen, z. B. wenn die Waren</p>'
                 + ul(["nicht der Beschreibung entsprechen,", "nicht bestimmungsgemäß funktionieren."], "") +
                 '<p>Verkäufer haften für jede Vertragswidrigkeit, die zum Zeitpunkt der Lieferung der Waren bestand und innerhalb des Zeitraums der gesetzlichen Gewährleistung erkennbar wird. Verkäufer müssen in solchen Fällen Folgendes anbieten:</p>'
                 + ul(["kostenlose Nachbesserung oder kostenlose Ersatzlieferung,", "in bestimmten Fällen eine Preisminderung oder eine vollständige Erstattung des Kaufpreises."], "") +
                 '<p>In einigen Ländern gilt ein längerer Zeitraum für die gesetzliche Gewährleistung. Für gebrauchte Waren kann ein kürzerer Zeitraum gelten, jedoch nicht weniger als ein Jahr. Für weitere Informationen zu Ihren Rechten in einem bestimmten Land scannen Sie den nachstehenden QR-Code oder fragen Sie den Verkäufer: <a href="https://europa.eu/youreurope/garantien" target="_blank" rel="noopener">europa.eu/youreurope/garantien</a></p>'
                 '<h2>Was ist zu tun, wenn Sie vertragswidrige Waren erhalten?</h2>'
                 + ul(["Melden Sie dem Verkäufer das Problem so bald wie möglich.", "Legen Sie einen Kaufnachweis vor, z. B. die Quittung, Rechnung oder einen Kontoauszug."], "") +
                 '<p>Verkäufer und Hersteller können auch gewerbliche Garantien gewähren, die unabhängig von der gesetzlichen Gewährleistung gelten. Diese GARAN-Kennzeichnung zeigt beispielsweise, dass der Hersteller eine gewerbliche Haltbarkeitsgarantie ohne zusätzliche Kosten gewährt, die die gesamte Ware abdeckt.</p>'
                 '<div class="framed" style="margin-top:28px"><img src="assets/img/eu-gewaehrleistung.svg" alt="Harmonisierter EU-Hinweis zur gesetzlichen Gewährleistung mit QR-Code" loading="lazy" width="595" height="842"></div>')


@page("vertrag-widerrufen.html", "Vertrag widerrufen", "Online geschlossene Verträge können innerhalb von 14 Tagen widerrufen werden.")
def p_widerruf():
    return legal("Vertrag widerrufen",
                 '<p class="lead">Online geschlossene Verträge können innerhalb von 14 Tagen widerrufen werden. Bitte füllen Sie das untenstehende Formular aus.</p>'
                 '<p>Beim Absenden öffnet sich Ihr E-Mail-Programm mit einer fertigen Nachricht an uns. Bitte senden Sie diese ab. Eine Eingangsbestätigung erhalten Sie anschließend per E-Mail.</p>'
                 '<form class="form card" id="widerruf-form" style="margin-top:28px">'
                 '<div><label for="w-name">Name *</label><input id="w-name" name="name" required autocomplete="name"></div>'
                 '<div><label for="w-nr">Bestell- oder Buchungsnummer * <span class="hint">Diese ist in der Bestellbestätigung zu finden.</span></label><input id="w-nr" name="nummer" required></div>'
                 '<div><label for="w-mail">E-Mail-Adresse * <span class="hint">Die Eingangsbestätigung wird an diese Adresse gesendet.</span></label><input id="w-mail" name="email" type="email" required autocomplete="email"></div>'
                 '<div><label for="w-art">Welche Artikel sollen widerrufen werden? <span class="hint">Leer lassen, um den gesamten Vertrag zu widerrufen. Um nur einen Teil der Bestellung zu widerrufen, die Artikel hier angeben.</span></label><textarea id="w-art" name="artikel"></textarea></div>'
                 '<div><label for="w-grund">Grund des Widerrufs (optional)</label><textarea id="w-grund" name="grund"></textarea></div>'
                 '<p class="muted" style="margin:0">Ein Klick auf die Schaltfläche unten erklärt verbindlich den Widerruf des oben angegebenen Vertrags, sobald Sie die vorbereitete E-Mail absenden. Alle mit * markierten Felder sind Pflichtfelder.</p>'
                 '<div><button class="btn" type="submit">Vertrag widerrufen</button></div>'
                 '</form>')


@page("sitemap.html", "Sitemap", "Übersicht aller Seiten der Website.")
def p_sitemap():
    groups = [("Startseite", [("Startseite", "index.html"), ("Kontakt &amp; Anfahrt", "kontakt-anfahrt.html")])] + [(g, [(t, h) for t, h, *_ in items]) for g, items in MENU] + [
        ("Rechtliches", [("Impressum", "impressum.html"), ("Datenschutz", "datenschutz.html"), ("Cookie-Richtlinie", "cookie-richtlinie.html"),
                         ("Gesetzliche Gewährleistung", "gewaehrleistung.html"), ("Vertrag widerrufen", "vertrag-widerrufen.html")])]
    extra = {"laminam.html": [(n.title(), f"laminam.html#{a}") for n, a, _, _ in LAMINAM_KOLL],
             "raeumlichkeiten.html": [("Ausstellung", "raeumlichkeiten.html#ausstellung"), ("Digitalprint", "raeumlichkeiten.html#digitalprint"),
                                      ("Produktion", "raeumlichkeiten.html#produktion"), ("Steinlager", "raeumlichkeiten.html#steinlager")],
             "ueber-uns.html": [("Chronik", "ueber-uns.html#chronik")]}
    cards = ""
    for g, items in groups:
        lis = ""
        for t, h in items:
            sub = "".join(f'<li><a href="{sh}">{st}</a></li>' for st, sh in extra.get(h, []))
            lis += f'<li><a href="{h}">{t}</a>{f"<ul>{sub}</ul>" if sub else ""}</li>'
        cards += f'<div class="card"><h3>{g}</h3><ul>{lis}</ul></div>'
    return page_head([("Startseite", "index.html")], "Sitemap") + section(f'<div class="grid grid-3">{cards}</div>', "section--tight")


@page("404.html", "Seite nicht gefunden", "Diese Seite gibt es leider nicht.")
def p_404():
    return page_head([("Startseite", "index.html")], "Diese Seite gibt es leider nicht.", "Vielleicht hilft Ihnen einer dieser Wege weiter:") + section(
        btns(btn("Zur Startseite", "index.html"), btn("Sitemap", "sitemap.html", "ghost"), btn("Kontakt", "kontakt-anfahrt.html", "ghost")), "section--tight")


# ---------------------------------------------------------------- Ausgabe

def main():
    for slug, (title, desc, fn) in PAGES.items():
        html = layout(slug, title, desc, fn())
        with open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f:
            f.write(html)
    print(f"{len(PAGES)} Seiten erzeugt.")


if __name__ == "__main__":
    main()
