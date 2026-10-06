#!/usr/bin/env python3
"""Injecte les images (base64) dans les templates et produit les pages finales.

src/template-c.html  -> public/index.html            (site public G.ARK)
src/template.html    -> archives/proposition-a.html  (archive, non référencée)
src/template-b.html  -> archives/proposition-b.html  (archive, non référencée)
"""
import json, pathlib, re

# Adresse publique du site — à changer le jour où un vrai domaine est branché.
# Sert aux balises de partage (aperçu WhatsApp, LinkedIn, Facebook).
SITE_URL = "https://g-ark3.angeglidja.workers.dev"

ROOT = pathlib.Path(__file__).resolve().parent
imgs = json.load(open(ROOT / "assets" / "imgs.json", encoding="utf-8"))

TARGETS = {
    "template.html": "archives/proposition-a.html",
    "template-b.html": "archives/proposition-b.html",
    "template-c.html": "public/index.html",
}

for src, dst in TARGETS.items():
    path = ROOT / "src" / src
    if not path.exists():
        continue
    html = path.read_text(encoding="utf-8")
    html = html.replace("__SITE__", SITE_URL.rstrip("/"))
    for key, b64 in imgs.items():
        html = html.replace("__%s__" % key, b64)
    left = re.findall(r"__[A-Z0-9]+__", html)
    assert not left, "tokens non remplacés: %s" % set(left)
    out = ROOT / dst
    out.write_text(html, encoding="utf-8")
    print("OK  %-18s -> %-22s %4d KB" % (src, dst, len(html) // 1024))
