# Guide de mise en place : profil GitHub d'Axel

Design repris de ton portfolio (`axeltadjounteu.vercel.app`) : Google Sans, bleu `#2563eb`, vert `#059669`, ciel `#38bdf8`, fond `#f0f4ff` / `#070b14`, grille, halos, cartes vitrées, monogramme ATN. Thème clair et sombre automatiques, en français et en anglais. 12 rubriques : À propos, Ma façon de construire, En ce moment, Atnyx, Projets, Boîte à outils, Labs, Certifications, Réalisations, Activité, Écrits & contenu, Contact.

## 1. Ce que contient le dossier

```
github-profile-axel/
├─ README.md               profil en anglais (affiché sur ta page GitHub)
├─ README.fr.md            profil en français (lien « Français » en haut du README)
├─ assets/light|dark/      160 SVG : bannière, en-têtes, principes, projets, outils, certifs, médailles, activité, boutons
├─ social/                 8 aperçus de dépôts en PNG 1280×640
├─ brand/avatar-atn.png    avatar 1024×1024 avec ton monogramme (alternative à ta photo)
├─ .github/workflows/      activity.yml : met à jour le tableau de bord d'activité chaque jour
├─ templates/              modèles de README pour un projet et pour un lab
├─ scripts/
│  ├─ content.py           TOUT le contenu et la configuration (le seul fichier à éditer)
│  ├─ build.py             génère les SVG, les PNG et les README
│  ├─ activity.py          récupère tes stats via l'API GitHub et dessine le tableau de bord
│  ├─ extract_logos.py     ajoute un nouveau logo (rarement utile)
│  ├─ logos.json           52 logos déjà extraits
│  └─ fonts/               Google Sans (licence OFL)
├─ GUIDE.md                ce fichier
└─ NOTICE.md               licences et crédits
```

## 2. Publier le profil

**a) Créer le dépôt du profil.** Sur GitHub : `+` → *New repository*. Le nom doit être **exactement ton pseudo GitHub** (par exemple `axel` pour `github.com/axel`). Coche *Public*. Ne coche pas « Add a README », tu as déjà le tien.

**b) Renseigner ton pseudo et tes liens.** Ouvre `scripts/content.py` et modifie en haut :

```python
USERNAME = "ton-pseudo"
LINKS = {
    "portfolio": "https://axeltadjounteu.vercel.app",
    "linkedin": "https://www.linkedin.com/in/ton-profil",
    "email": "mailto:ton.email@exemple.com",
    "tiktok": "https://www.tiktok.com/@ton-compte",
}
```

Relis aussi `PROJECTS`, `CERTS` et `TOOLBOX` : retire ce qui n'est pas vrai ou pas encore d'actualité.

**c) Générer les visuels** (Ubuntu) :

```bash
cd github-profile-axel
pip install -r scripts/requirements.txt
python3 scripts/build.py --readme
```

**d) Pousser sur GitHub :**

```bash
git init && git add . && git commit -m "feat: profile README"
git branch -M main
git remote add origin git@github.com:TON-PSEUDO/TON-PSEUDO.git
git push -u origin main
```

**e) Vérifier.** Ouvre `github.com/ton-pseudo`. Teste les deux thèmes dans *Settings → Appearance*, puis sur téléphone. Le lien « Français » en haut ouvre `README.fr.md`. Si tu préfères un profil français par défaut, échange les deux fichiers.

**f) Régler la colonne de gauche du profil** (*Edit profile*) :

| Champ | Suggestion |
|---|---|
| Nom | Axel Renaud Tadjounteu |
| Bio | `Cybersecurity · Cloud · Dev · Founder @ Atnyx` (160 caractères max) |
| Company | Atnyx |
| Location | Douala, Cameroon |
| Website | ton portfolio |
| Social accounts | LinkedIn (4 liens possibles) |
| Photo | carré, 500×500 px minimum, visage centré (GitHub le recadre en cercle) |

Active aussi *Contribution settings → « Private contributions »* (menu au-dessus du graphique de contributions sur ton profil) : ton activité sur les dépôts privés (NKUL, Branchline…) apparaît alors dans le graphique, sans exposer le code.

## 2 bis. Les rubriques de la page de profil GitHub

Ta page de profil mélange des parties **que tu dessines** (le README) et des parties **natives** que GitHub affiche à sa façon. Voici comment chacune est traitée, en reprenant les captures que tu m'avais envoyées.

| Rubrique (sur les captures) | Statut | Ce qui est fait pour toi |
|---|---|---|
| Bannière du README, texte d'accueil | Dessinée | Bannière « AXEL » avec faux terminal, et « À propos » |
| Current focus | Dessinée | « En ce moment » |
| Certifications avec badges cliquables | Dessinée | 5 cartes de certifs ; ajoute la preuve Credly dans `CERT_PROOF` pour les rendre cliquables |
| Tech stack | Dessinée | 5 bandeaux de logos + plateformes d'apprentissage |
| Featured projects | Dessinée | 6 cartes projet avec statut ; liens dans `PROJECT_LINKS` |
| I also write | Dessinée | « Écrits & contenu » : cartes TikTok et LinkedIn |
| Achievements (pastilles dans la colonne de gauche) | **Native** : elles se gagnent (Pull Shark, YOLO…) et ne se dessinent pas | Rubrique « Réalisations » avec **tes propres médailles** : re/Start, Cloud Practitioner, fondateur d'Atnyx, pitch MTN YaMo, hackathon AWS, formation No-Code |
| Popular repositories | **Native** : ce sont tes 6 dépôts épinglés | Descriptions prêtes à coller (voir plus bas) |
| Graphique de contributions, Activity overview | **Native** : GitHub ne se laisse pas restyler | Rubrique « Activité » : ton propre tableau de bord, aux couleurs du portfolio, mis à jour chaque jour |
| Nouveau : Ma façon de construire | Dessinée | 4 principes (à adapter à ta façon de travailler) |

**Descriptions des dépôts épinglés** (une pastille affiche le nom, cette description et le langage principal détecté par GitHub) :

| Dépôt | Description à coller |
|---|---|
| `portfolio` | Personal portfolio: React, Vite, Tailwind, multilingual, with a contact form. |
| `cloud-labs` | Hands-on AWS and Google Cloud labs, from the CLI, with cleanup steps. |
| `network-security-labs` | Cisco Packet Tracer labs: VLAN, ACL, DMZ, IPsec VPN, with configs. |
| `certification-notes` | My study notes for AWS SAA-C03 and CompTIA Security+. |

**Activer le tableau de bord d'activité** (une seule fois, après le premier push) :

1. Onglet **Actions** du dépôt du profil : si GitHub demande d'activer les workflows, accepte.
2. Choisis **Refresh activity** puis **Run workflow**. Au bout d'une minute environ, un commit `chore: refresh activity` remplace les visuels « en attente » par tes vrais chiffres. Ensuite, il se relance chaque jour à 03h17 UTC.
3. Optionnel, pour compter aussi les contributions privées : crée un jeton personnel (*Settings → Developer settings → Personal access tokens*, scope `read:user`), puis enregistre-le dans *Settings → Secrets and variables → Actions* sous le nom `PROFILE_TOKEN`. Sans lui, seules tes contributions publiques sont comptées.
4. Sans GitHub Actions, en local : `GH_TOKEN=ton_jeton python3 scripts/activity.py --user ton-pseudo`, puis commit et push.

GitHub peut désactiver les workflows planifiés d'un dépôt public sans activité depuis 60 jours : dans ce cas, relance-le à la main avec *Run workflow*. Un aperçu avec de fausses données (sans rien écrire dans `assets/`) : `python3 scripts/activity.py --demo /tmp/apercu`.

**Avatar.** Ta photo reste le meilleur choix pour un profil personnel. Si tu veux une alternative de marque (ou un avatar pour l'organisation Atnyx), `brand/avatar-atn.png` reprend ton monogramme sur le fond du portfolio.

## 3. Modifier ensuite

| Je veux changer… | Où |
|---|---|
| Un texte, un projet, une certif, un lien | `scripts/content.py` puis `python3 scripts/build.py --readme` |
| Le paragraphe « À propos », la liste « En ce moment » | dictionnaire `COPY` dans `scripts/build.py` |
| Les couleurs | dictionnaire `THEMES` dans `scripts/build.py` |
| Rendre une carte projet ou une certif cliquable | `PROJECT_LINKS` et `CERT_PROOF` dans `content.py`, puis `--readme` |
| Les principes, les médailles, les chaînes (TikTok, LinkedIn…) | `PRINCIPLES`, `ACHIEVEMENTS`, `CHANNELS` dans `content.py` |
| Régénérer aussi l'activité par-dessus les vraies données | `python3 scripts/build.py --force-activity` (par défaut, `build.py` ne l'écrase jamais) |

Attention : `--readme` **écrase** les deux README. Si tu les modifies à la main, lance `python3 scripts/build.py` sans l'option pour ne régénérer que les images.

## 4. Ajouter ou retirer un outil (logos)

1. **Retirer** : supprime la ligne de l'outil dans `TOOLBOX` (`content.py`).
2. **Ajouter un logo déjà extrait** (52 disponibles, voir `LOGOS`) : ajoute `("cle", "Libellé")` dans la catégorie voulue.
3. **Ajouter un nouveau logo** :
   - trouve son *slug* sur https://simpleicons.org (ex. `nginx`) ou son chemin sur https://devicon.dev ;
   - ajoute `"nginx": ("si", "nginx")` dans `LOGOS`, puis la ligne dans `TOOLBOX` ;
   - lance `cd scripts && npm install --no-save simple-icons devicon && python3 extract_logos.py && cd .. && python3 scripts/build.py`.
4. Un logo introuvable (les services AWS comme Lambda ou DynamoDB, par exemple) : mets-le comme texte dans `"chips"`, comme c'est déjà fait pour les services AWS.

Les logos sont recolorés automatiquement pour rester lisibles en thème clair et sombre.

## 5. Les dépôts à créer

Six dépôts épinglés donnent un profil solide. Deux idées valent mieux que tout le design : **peu de dépôts, mais chacun avec un vrai README**, et des labs reproductibles.

| Dépôt | Visibilité | Contenu |
|---|---|---|
| `ton-pseudo` (profil) | Public | Ce dossier. |
| `portfolio` | Public | Ton site. S'il existe déjà, ne le recrée pas : ajoute seulement description, topics et aperçu social. |
| `cloud-labs` | Public | `gcp/skills-boost/<lab>/`, `aws/<lab>/` : chaque dossier a un `README.md` (modèle `templates/LAB_README.md`), les commandes `gcloud`/`aws` dans un `commands.sh` et le nettoyage des ressources. |
| `network-security-labs` | Public | `packet-tracer/<lab>/` : `topology.png`, fichier `.pkt`, `config-<equipement>.txt`, `README.md` (VLAN, ACL, DMZ, VPN IPsec). |
| `certification-notes` | Public | Tes notes de révision SAA-C03 et plan Security+. **Jamais de questions d'examen** : uniquement tes notes et tes schémas. |
| `nkul`, `ecocamer`, `branchline`, `atnyx-platform` | Privé au départ | Le code reste privé. Pour la vitrine, crée une version « docs » publique (README, architecture, captures) sans secret ni donnée client, quand tu es prêt. |

Option utile : crée une **organisation GitHub `atnyx`** (gratuite) pour les dépôts de l'entreprise. Son profil se règle avec un fichier `profile/README.md` dans un dépôt `.github` de l'organisation, avec les mêmes visuels.

**Réglages de chaque dépôt** (page du dépôt, roue dentée *About* et *Settings*) :

| Réglage | Règle |
|---|---|
| Description | une phrase, 350 caractères maximum |
| Website | l'URL en ligne si elle existe (ex. le portfolio) |
| Topics | 3 à 8, en minuscules avec tirets : `aws`, `cloud`, `cybersecurity`, `packet-tracer`, `nextjs`… |
| Social preview | *Settings → General → Social preview → Edit → Upload an image* : prends `social/<nom>.png` |
| README | copie `templates/REPO_README.md` ou `LAB_README.md` |
| Licence | MIT pour les labs et notes ; pas de licence (ou propriétaire) pour les produits |
| `.gitignore` et `.env.example` | jamais de clé, mot de passe ou jeton dans l'historique Git |

Les aperçus fournis : `portfolio`, `cloud-labs`, `network-security-labs`, `certification-notes`, `nkul`, `ecocamer`, `branchline`, `atnyx-platform`. Pour un autre dépôt, ajoute une ligne dans `REPOS` (`content.py`) et relance `python3 scripts/build.py`.

**Épingler** (page du profil → *Customize your pins*) : `cloud-labs`, `network-security-labs`, `portfolio`, `certification-notes`, et deux projets docs si tu les publies.

## 6. Images : formats et tailles

| Image | Format | Taille | Où |
|---|---|---|---|
| Visuels du profil (bannière, cartes, outils) | SVG | déjà générés | dossier `assets/`, appelés par le README |
| Photo de profil | JPG/PNG | carré, 500×500 minimum | *Edit profile* |
| Aperçu social d'un dépôt | **PNG** (le SVG n'est pas accepté) | 1280×640, moins de 1 Mo | *Settings → Social preview* |
| Capture d'écran dans un README | PNG ou WebP | 1600 px de large max, moins de 500 Ko | `docs/` du dépôt |
| Schéma d'architecture | SVG ou PNG | libre | `docs/architecture.png` |

Le texte des SVG est converti en tracés : il s'affiche pareil partout sans installer Google Sans. Chaque page charge environ 670 Ko de SVG dans un seul thème et une seule langue, ce qui reste raisonnable sur une connexion mobile.

## 7. Checklist finale

- [ ] `USERNAME` et `LINKS` renseignés, `python3 scripts/build.py --readme` lancé sans erreur
- [ ] Aucun `TON-...` restant : `grep -rn "TON-" README*.md`
- [ ] Profil vérifié en thème clair, sombre, et sur mobile
- [ ] Bio, localisation, site, LinkedIn, photo renseignés
- [ ] Contributions privées activées
- [ ] 4 dépôts publics créés avec description, topics, aperçu social et README
- [ ] 6 dépôts épinglés, avec les descriptions de la section 2 bis
- [ ] Workflow **Refresh activity** lancé une fois (et `PROFILE_TOKEN` ajouté si tu veux les contributions privées)
- [ ] Aucun secret dans l'historique (`git log -p | grep -i "secret\|password\|api_key"`)
