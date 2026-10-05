# Mettre le site en ligne — pas à pas

Deux étapes. Compte une vingtaine de minutes la première fois, puis chaque
mise à jour prendra trente secondes.

Rien à configurer côté formulaire : le bouton « Préparer le message » ouvre
directement la messagerie du visiteur, avec le message déjà rédigé, adressé
à **glixart79@gmail.com**. Aucun service tiers, aucune clé, aucun compte.

---

## Étape 1 — Envoyer le code sur GitHub (10 min)

### Créer le dépôt

1. Sur **https://github.com/new**
2. Repository name : **`gark-site`**
3. Laisse-le en **Public** (ou Private, Cloudflare sait lire les deux)
4. **Ne coche rien** : pas de README, pas de .gitignore, pas de licence —
   le dossier en contient déjà
5. **Create repository**

### Envoyer les fichiers

Depuis un terminal, dans le dossier du site :

```bash
git remote add origin https://github.com/TON-PSEUDO/gark-site.git
git branch -M main
git push -u origin main
```

Remplace `TON-PSEUDO` par ton nom d'utilisateur GitHub.
GitHub demandera ton identifiant : le mot de passe ne fonctionne plus, il
faut un **token**. Va sur https://github.com/settings/tokens → *Generate new
token (classic)* → coche la case **repo** → copie le token et colle-le à la
place du mot de passe.

> Pas à l'aise avec le terminal ? Installe **GitHub Desktop**
> (https://desktop.github.com) : *Add local repository* → choisis le dossier
> → *Publish repository*. Même résultat, en trois clics.

---

## Étape 2 — Brancher Cloudflare Pages (10 min)

1. Crée un compte sur **https://dash.cloudflare.com** (gratuit)
2. Menu de gauche : **Workers & Pages** → **Create** → onglet **Pages** →
   **Connect to Git**
3. Autorise Cloudflare à accéder à ton GitHub, puis choisis **`gark-site`**
4. Écran de configuration — **c'est le point important** :

| Champ | Valeur |
|---|---|
| Project name | `gark` |
| Production branch | `main` |
| Framework preset | **None** |
| Build command | *laisser vide* |
| Build output directory | **`public`** |

5. **Save and Deploy**

Une minute plus tard le site est en ligne sur **`https://gark.pages.dev`**.

Le dossier `public/` est le seul publié. Les templates, les photos sources
et les deux anciennes propositions restent dans le dépôt mais ne sont pas
accessibles depuis le web.

---

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

`gark.pages.dev` fait le travail, mais `g-ark.com` sur une carte de visite
n'a pas le même poids. Quand tu voudras :

1. Achète le domaine (Cloudflare Registrar le vend au prix coûtant, environ
   10 €/an, sans marge ni renouvellement piégeux)
2. Dans ton projet Pages → **Custom domains** → **Set up a domain**
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
| Page blanche sur `.pages.dev` | Build output directory ≠ `public` |
| Rien ne s'ouvre au clic | Aucun logiciel de mail configuré sur le poste du visiteur — le bouton « Copier le message » est là pour ça |
| Le PDF ne se télécharge pas | Vérifie qu'il est bien dans `public/` et poussé sur GitHub |
| `git push` refusé | Token GitHub manquant ou expiré |
| Le site ne se met pas à jour | Tu as modifié un template sans relancer `python3 build.py` |
