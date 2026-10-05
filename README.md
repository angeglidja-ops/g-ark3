# G.ARK — site

Site vitrine d'Ulysse Glidja, assistant architecte à Cotonou.
Une seule page, sans dépendance, sans framework : tout est inliné dans un
unique fichier HTML (images comprises, en base64). Il s'ouvre hors ligne.

**Mise en ligne : voir [DEPLOY.md](DEPLOY.md).**

## Organisation

```
public/                     ← le seul dossier publié par Cloudflare
  index.html                  le site (généré — ne pas éditer à la main)
  portfolio-ulysse-glidja-2026.pdf
  CREDITS.md                  crédits photo
  robots.txt
  _headers                    en-têtes HTTP (cache, sécurité)
src/
  template-c.html             source du site — c'est ici qu'on écrit
  template.html               archive : proposition A (big.dk)
  template-b.html             archive : proposition B (planche technique)
assets/
  imgs.json                   images encodées en base64, injectées au build
  credits.json                métadonnées des photos
  brand/                      déclinaisons du logo G.ARK
  real/                       photos sources et versions noir & blanc
archives/                     anciennes propositions générées (non publiées)
build.py                      injecte les images dans les templates
```

## Build

```bash
python3 build.py
```

Remplace chaque jeton `__CLÉ__` des templates par la valeur correspondante
de `assets/imgs.json`, et refuse de produire un fichier s'il reste un jeton
non résolu. Aucune dépendance : Python 3 standard suffit.

## Aperçu local

```bash
python3 -m http.server 8080 --directory public
```

Puis http://localhost:8080

## Technique

- Thème clair/sombre, mémorisé — raccourci `T`
- Menu de commandes — `⌘K` / `Ctrl+K`
- Curseur personnalisé, vignettes au survol, révélations au défilement
- Estimateur de budget avec bascule FCFA / EUR (taux fixe 655,957)
- Formulaire de contact sans backend : il compose un `mailto:` pré-rempli et
  ouvre la messagerie du visiteur, avec repli « copier le message »
- `prefers-reduced-motion` respecté : toutes les animations se coupent

## Crédits photo

Sept photographies issues de Pexels, licence libre, converties en noir et
blanc. Détail complet dans [public/CREDITS.md](public/CREDITS.md).
