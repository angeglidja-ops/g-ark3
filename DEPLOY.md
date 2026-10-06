# Mettre le site en ligne — pas à pas

Le site est **en ligne** : https://g-ark3.angeglidja.workers.dev

Ce document garde la marche à suivre complète, et explique surtout comment
passer du déploiement manuel au déploiement automatique.

Rien à configurer côté formulaire : le bouton « Préparer le message » ouvre
directement la messagerie du visiteur, avec le message déjà rédigé, adressé
à **glixart79@gmail.com**. Aucun service tiers, aucune clé, aucun compte.

---

## Étape 1 — Envoyer le code sur GitHub

### Créer le dépôt

1. Sur **https://github.com/new**
2. Repository name : **`g-ark3`**
3. Laisse-le en **Public** (ou Private, Cloudflare sait lire les deux)
4. **Ne coche rien** : pas de README, pas de .gitignore, pas de licence —
   le dossier en contient déjà
5. **Create repository**

### Envoyer les fichiers

Depuis un terminal, dans le dossier du site :

```bash
git remote add origin https://github.com/angeglidja-ops/g-ark3.git
git branch -M main
git push -u origin main
```

GitHub demandera ton identifiant : le mot de passe ne fonctionne plus, il
faut un **token**. Va sur https://github.com/settings/tokens → *Generate new
token (classic)* → coche la case **repo** → copie le token et colle-le à la
place du mot de passe.

> Pas à l'aise avec le terminal ? Installe **GitHub Desktop**
> (https://desktop.github.com) : *Add local repository* → choisis le dossier
> → *Publish repository*. Même résultat, en trois clics.

---

## Étape 2 — Cloudflare (déjà fait)

Le site tourne sur **Cloudflare Workers** (et non Pages — c'est l'option que
le tableau de bord propose maintenant par défaut, elle fait le même travail
pour un site statique).

> **Adresse publique : https://g-ark3.angeglidja.workers.dev**
> Dépôt relié : `angeglidja-ops/g-ark3`

### Passer du déploiement manuel au déploiement automatique

Le tableau de bord affiche « Déployé manuellement » : aujourd'hui, tes
`git push` ne mettent pas le site à jour tout seuls, il faut téléverser à la
main à chaque fois. Le fichier **`wrangler.jsonc`** à la racine du dépôt
corrige ça — il dit à Cloudflare quoi publier :

```jsonc
{
  "name": "g-ark3",
  "compatibility_date": "2025-09-01",
  "assets": { "directory": "./public" }
}
```

Pour l'activer, une fois ce fichier poussé sur GitHub :

1. Tableau de bord → **Workers & Pages** → **g-ark3**
2. **Settings** → **Build** (ou *Builds*) → **Connect** / **Set up builds**
3. Choisis le dépôt `angeglidja-ops/g-ark3`, branche **`main`**
4. **Build command** : *laisser vide* · **Deploy command** : `npx wrangler deploy`
5. Enregistre

À partir de là, chaque `git push` redéploie le site en une minute, sans
aucune manipulation.

## Mettre le site à jour plus tard

Tu modifies un fichier, puis :

```bash
git add -A
git commit -m "mise à jour des tarifs"
git push
```

Cloudflare détecte le push et redéploie en moins d'une minute. Pas de bouton
à cliquer. Si tu te trompes, l'onglet **Deployments** du tableau de bord
permet de revenir à la version précédente en un clic (*Rollback*).

---

## Modifier le contenu, concrètement

Le site est généré : on ne touche jamais `public/index.html` à la main,
il est écrasé à chaque build.

- **Le texte, les prix, les sections, l'adresse mail** → `src/template-c.html`
- **Les images** → `assets/imgs.json` (encodées en base64)

Après avoir modifié un template :

```bash
python3 build.py
```

Cela régénère `public/index.html` et les deux archives.

---

## Comment arrivent les demandes

Le visiteur remplit nom, cabinet, adresse, besoin et message, puis clique
« Préparer le message ». Son logiciel de messagerie s'ouvre avec un mail
déjà écrit, qu'il n'a plus qu'à envoyer :

```
À      : glixart79@gmail.com
Objet  : Demande — Marie Dupont (Atelier Nord)

[son message]

—
Marie Dupont — Atelier Nord
marie@ateliernord.fr
Besoin : Modélisation 3D
```

Tu reçois donc un vrai mail, depuis sa vraie adresse : tu réponds
normalement, la conversation existe déjà dans ta boîte.

Si son navigateur bloque l'ouverture — ça arrive sur certains postes, ou
quand aucun logiciel de mail n'est configuré — le site affiche un bouton
**Copier le message** : il copie le tout, adresse comprise, à coller dans
n'importe quel webmail.

**La limite, à connaître :** tu ne sauras jamais combien de personnes ont
rempli le formulaire sans aller au bout de l'envoi. Si un jour tu veux
mesurer ça, ou recevoir les demandes même quand le visiteur n'a pas de
logiciel de mail, dis-le-moi : on branche un service d'envoi en dix minutes,
sans rien changer d'autre au site.

---

## Plus tard : un vrai nom de domaine

`g-ark3.angeglidja.workers.dev` fait le travail, mais `g-ark.com` sur une carte de visite
n'a pas le même poids. Quand tu voudras :

1. Achète le domaine (Cloudflare Registrar le vend au prix coûtant, environ
   10 €/an, sans marge ni renouvellement piégeux)
2. Dans ton projet → **Settings → Domains & Routes** → **Add → Custom domain**
3. Si le domaine est chez Cloudflare, tout se configure seul. Sinon, il faut
   ajouter un enregistrement CNAME chez ton registrar — l'écran te donne la
   valeur exacte à copier.

Le certificat HTTPS est créé automatiquement, gratuitement, dans les deux cas.

Avec un domaine, tu pourras aussi créer **contact@g-ark.com** gratuitement
via *Email Routing* dans Cloudflare : les mails arrivent dans ta boîte Gmail
habituelle, mais l'adresse affichée fait professionnelle.

---

## Si ça ne marche pas

| Symptôme | Cause la plus probable |
|---|---|
| Page blanche | Le dossier publié n'est pas `public` — vérifie `wrangler.jsonc` |
| Rien ne s'ouvre au clic | Aucun logiciel de mail configuré sur le poste du visiteur — le bouton « Copier le message » est là pour ça |
| Le PDF ne se télécharge pas | Vérifie qu'il est bien dans `public/` et poussé sur GitHub |
| `git push` refusé | Token GitHub manquant ou expiré |
| Le site ne se met pas à jour | Soit tu as oublié `python3 build.py`, soit les builds automatiques ne sont pas encore connectés |

---

## Partager le site

L'adresse est affichée en haut du projet : **Workers & Pages → g-ark3 →
Visit site**. C'est **https://g-ark3.angeglidja.workers.dev**.

Il n'y a aucun réglage de partage à activer : le site est **public dès la
première seconde**. Tu copies l'adresse, tu la colles dans WhatsApp, un
mail, une bio Instagram, une signature. Rien d'autre à faire.

### L'aperçu du lien

Quand tu colles l'adresse dans WhatsApp ou LinkedIn, une vignette apparaît :
l'image `public/share.jpg` (le logo sur une photo d'atelier), le titre
« G.ARK — L'architecture en grand » et une phrase de description. C'est
souvent la seule chose que ton interlocuteur regarde avant de cliquer.

Si tu changes de domaine plus tard, change aussi la ligne `SITE_URL` en haut
de `build.py`, puis relance `python3 build.py` : sans ça, l'aperçu ira
chercher l'image à l'ancienne adresse et n'affichera rien.

WhatsApp et Facebook gardent l'aperçu en mémoire environ 7 jours. Après une
modification, force la mise à jour sur
https://developers.facebook.com/tools/debug/ (colle l'URL, puis *Scrape
Again*) et https://www.linkedin.com/post-inspector/.

### Montrer une version avant de la publier

Chaque déploiement reçoit aussi une **adresse de prévisualisation unique**,
lisible dans l'onglet *Deployments* du projet. Pratique pour faire relire une
modification sans toucher au site en ligne. Une fois les builds connectés,
pousser sur une branche autre que `main` crée automatiquement sa propre
adresse de test.

### Réserver l'accès à certaines personnes

Pour un lien privé — montrer une version à un cabinet précis, pas au monde
entier : **Zero Trust → Access → Applications**, et vise le domaine du
Worker. Cloudflare demande alors un code reçu par mail avant d'ouvrir la
page. Gratuit jusqu'à 50 personnes.

### Le PDF, directement

`https://g-ark3.angeglidja.workers.dev/portfolio-ulysse-glidja-2026.pdf` télécharge le
portfolio sans passer par le site. Utile quand quelqu'un te demande juste
« tu peux m'envoyer ton book ? ».
