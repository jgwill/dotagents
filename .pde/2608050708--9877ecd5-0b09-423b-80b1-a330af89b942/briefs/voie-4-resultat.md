# Voie 4 — résultat

Outil : `~/.agents/skills/jamai-morning/scripts/jamai-related.py` (nouveau, non commité).

## 1. Les corpus, mesurés

| corpus | taille | verdict |
|---|---|---|
| manifestes `composition.json` | **190 721 o**, 12 fichiers | retenu — le champ `notes` porte la substance |
| `transcription_*.txt` | **78 602 o**, 31 fichiers | retenu |
| QMD | `mcp__qmd__*` **non enregistré** sur cet hôte ; repli `/etc/claude-code/scripts/whispering_inquiry.sh` présent (mia:mia), `qmd` absent du PATH | **écarté** — corpus de William, distant, et il n'indexe pas les compositions de Jerry |

**Corpus retenu : 269 323 octets, 12 unités.** Il tient en mémoire.

## 2. Le coût, montré

Index BM25 reconstruit à chaque appel : **20–30 ms**. Les 31 transcriptions
passées chacune en requête : **2 757 ms au total, soit 86 ms l'unité.**
**Zéro token de modèle, zéro appel réseau.** Rien n'est persisté, donc rien ne
périme.

## 3. Ce qu'il a fallu corriger, et pourquoi

- **34,7 % du corpus est du code** (chemins, commandes, blocs collés dans
  `notes`). En BM25 brut, ep-005 remontait sur `head`, `home`, `env`, `git`,
  `bash`, `usr` — de la syntaxe shell, pas du sujet. Le code est retiré des
  deux côtés avant l'index.
- **Un mot partagé est une coïncidence, deux mots à la suite sont un sujet.**
  La preuve exigée est un bigramme rare partagé. Seuil mesuré, pas deviné :
  `2 → 52 liens, 6/31 muettes · 3 → 36, 12/31 · 4 → 28, 14/31 · 5 → 25 · 6 → 18`.
  Retenu **4** : 0,90 lien par dépôt, près d'une requête sur deux reste muette.

## 4. Le vrai positif validé

ep-005 → **ep-006**, 8 bigrammes : « capture musicale », « transcription midi »,
« telle chantée », « voix telle », « playground livré ». Les notes d'ep-005
disaient déjà à la main *« Suite du sujet → ep-006 Capture Musicale »*.
**L'outil a retrouvé seul un lien que l'humain avait écrit.**

## 5. Le trou, nommé — c'est le résultat qui compte

Passé **les mots de Jerry du 2026-08-04** en requête : **zéro bigramme partagé
avec quoi que ce soit**, alors que le classement met ep-004 (45,28) puis ep-007
(30,80) en tête — qui sont les bons épisodes.

La cause, mesurée :

| terme | Jerry | corpus |
|---|---|---|
| `atelier`/`ateliers` | **0** | **104** |
| `espaces de travail` | **3** | **0** |
| `moniteur` | **2** | **0** |
| `clip` | **0** | 75 |
| `épisode` | 7 | 30 |

**Jerry et le corpus ne parlent pas la même langue.** Il dit « espaces de
travail » et « moniteur » — introuvables dans le corpus. Le corpus dit
« atelier » 104 fois — un mot qu'il n'emploie jamais.

Conséquence, et c'est la frontière que la voie 3 doit placer :

- **le bash classe gratuitement** — 12 unités → 3 candidats en 30 ms ;
- **il ne peut pas prouver le lien quand la requête est de la parole.** Le
  jugement demande un modèle qui lit ~15 lignes de preuve, pas 270 Ko.
- Le vrai remède n'est pas un meilleur algorithme, **c'est un vocabulaire
  partagé** : que chaque unité porte quelques mots dans le registre de Jerry.
  À trancher avec `w1:pM` en même temps que `links[]` / `documents[]`.

## 6. Où écrire — pour `w1:pM`

Les deux dangers signalés sont réels, **et ils ne sont pas de même nature.**
Vérifié en lisant `web/pixel-recorder.js` dans `~/salix/repos/gmtermux-193` :

- `PUT /api/compositions/:slug` → `updateComposition` (l. 885). L'allowlist
  (l. 889) est `title, chords, sections, rhythm, bpm, bpmDetected, key, capo,
  notes` — **`links` absente**. Mais la fonction relit le disque entier
  (`getComposition`, l. 858) et réécrit l'objet complet. Donc : on **ne peut pas
  écrire** `links[]` par cette route (200 et rien d'écrit), mais un `links[]`
  déjà sur disque y **survit**. Cette route préserve.
- `POST /api/forest/compositions/:slug` (l. 732) fait
  `fs.writeFileSync(json, JSON.stringify(req.body))` — sans fusion, sans
  authentification. **Elle efface tout ce que le client n'a pas envoyé.**
  C'est la seule route qui détruit un `links[]`.

**Le choix : on écrit sur le disque, jamais par l'API** — lecture, fusion sur
`(atelier, slug)`, réécriture entière, `os.replace` atomique. Éprouvé sur une
copie : les 15 clés d'origine survivent, `notes` intact (12 535 o), 15 clips.

**Le seul risque restant appartient à la migration de `w1:pM`** : tant qu'un
client ignorant `links` peut POSTer sur la route forest, il efface. Ce n'est pas
une clé à ajouter, c'est une route à faire fusionner.

## 7. Livré au contrat de la voie 1

`~/.agents/skills/episode-voice-channel/scripts/episodes-related <texte.txt>`,
exécutable, **76 ms**, sortie standard prête à déposer telle quelle en section
texte. Elle sépare deux rangs, parce que la mesure l'impose :

- **PROUVÉS** — ≥ 4 bigrammes rares partagés, chacun imprimé ;
- **À VÉRIFIER** — le classement tient, la preuve manque. C'est le rang où
  tombent les mots de Jerry, et la sortie le dit en toutes lettres.

La route `POST /api/compositions/<slug>/texts` choisie par la voie 1 est
**meilleure que mon `links[]` sur disque** — vérifié à la lecture :
`addTextToComposition` (l. 934) écrit un vrai `.txt` **et** relit-réécrit
l'objet entier. Elle ne dépend donc pas de la survie d'une clé face à la route
forest destructrice. Je m'y range ; le `--write links[]` reste disponible mais
n'est pas le chemin retenu pour `episodes`.

## 8. Ce que le précédent aureon a ajouté

`aureon-journal-events/SKILL.md`, section *Archival Protocol*, option 2 :
« *Connections to other entries* » — c'est mon `links[]`. Mais aussi
« **Spiral tracking over time** », que je n'avais pas : ma recherche était
intemporelle, elle disait « ces deux se ressemblent » et jamais « ceci revient
à cela ». Ajouté pour le prix d'une comparaison d'horodatage : une unité
antérieure de plus d'un jour est marquée **🔁 retour**, pas voisin. C'est le
type d'événement ECHO de la compétence, appliqué aux épisodes.

La compétence dit « **User chooses** » pour l'archivage. Non tranché — c'est à
Jerry.

## 9. Après le premier vrai tour (retour de la voie 1, 07:25:42)

**Le plancher a été essayé et rejeté sur mesure.** La voie 1 a vu
« proximité 0 » sur trois pistes d'un extrait de 52 mots. Trois discriminants
essayés, trois échecs :

| discriminant | résultat |
|---|---|
| score brut | grandit avec la longueur de la requête — inutilisable seul |
| score normalisé par mot | prouvés à 6 bigrammes : **0,46–0,70** · sans preuve : **0,27–0,49**. Ça se chevauche. L'extrait court donne 0,34, en plein milieu de la famille des 31 requêtes réelles (0,27–1,01) |
| compte de mots partagés | sature à l'affichage |

**Il n'existe pas de scalaire gratuit qui sépare relié de non-relié sur ce
corpus.** Seule la preuve par phrase sépare, et elle est muette entre registres.
Donc : le nombre est **retiré** de la sortie. Il se lisait comme une confiance
sans en être une. Restent les mots partagés — « mots communs : claude, scripts »
se voit maigre à l'œil nu, ce qu'aucun « proximité 0 » ne disait.

**Épreuve en long** (1 070 mots, en aveugle) : op-003 → boucle-de-minuit
(« classes hauteur », « au-dessus khz ») et op-001/op-002 (contrebasse, octaves,
spectre, la2). La grappe musicale se retrouve entière et juste. **La longueur
n'est pas le problème ; le registre l'est.**

**Défaut du portail signalé par la voie 1, pas le mien mais à porter** : les
sections texte sont nommées à la seconde près — deux dépôts dans la même
seconde portent le même nom et le second écrase le premier, **avec un 200
muet**. Contourné par un `sleep 2`. C'est le même motif que le repère d'état
partagé du 2026-08-04 à 22h24 : une collision silencieuse qui avale une écriture.

## 10. Le déclaré passe avant l'inféré — ce que l'issue #115 a renversé

**Les quatre issues Orpheus vérifiées le 2026-08-05**, toutes OPEN. Les titres
réels disent plus que le tableau : **c'est une hiérarchie, pas un ensemble plat.**

| issue | titre réel | |
|---|---|---|
| #587 | Jericho's Journal | 2025-02-18 · **97 comm.** |
| #704 | **Sub-Journal for Issue #587** — Focused on Issue #668 | 13 comm. |
| #784 | Aven's Entry Loops — **Sub-Journal of Issue #704** | 4 comm. |
| #717 | [Journal - gmusic1007] | 8 comm. |

Corpus : **126 798 octets**. Et le graphe y est **déjà déclaré** — #587 renvoie
à 673 704 711 717 759 784 · #704 → 587 668 · #784 → 704 · #717 → 587.
Pour aureon **il n'y a rien à inférer** : on lit le graphe, écrit à la main.

**Le même graphe dort chez nous.** Mesuré : **5 renvois `ep-NNN` déclarés dans
la prose des compositions, qu'aucun champ ne porte** — ep-003 → ep-001 ep-002 ·
ep-005 → ep-006 · ep-006 → ep-005 · ep-007 → ep-004. Deux d'entre eux sont
exactement mes cas les plus coûteux : ep-005↔ep-006 que le BM25 a redécouvert à
grands frais, et **ep-007 → ep-004, la paire que j'avais eue juste pour la
mauvaise raison** (« trois minutes », une coïncidence).

**Rang `DÉCLARÉS` ajouté, en tête**, et retiré des rangs inférés pour ne rien
redire. Vu tirer sur le seul texte de dépôt qui cite une unité par son nom.

**Ce que ça change pour `w1:pM`** : `links[]` ne doit pas d'abord porter de
l'inféré avec un score. Il doit porter le **déclaré** — exact, gratuit, écrit
par un humain. L'inférence n'est la réponse que pour ce que personne n'a
déclaré. Les notes d'ep-005 disaient déjà « Suite du sujet → ep-006 » : un lien
déclaré rangé dans un champ de prose faute d'un champ pour le tenir.

## 11. La décision de Jerry, appliquée — `jr-NNN` et la cible issue

Trois changements, tous dans le rang `DÉCLARÉS`, aucun dans l'inférence :

1. **`jr-NNN` reconnu** au même titre que `ep-NNN` / `op-NNN`. Le séparateur
   après le numéro est un **point** chez aureon (`jr-001.MainJ.…`) et un tiret
   ailleurs — le glob accepte les deux (`%s[-.]*`).
2. **La cible d'un lien aureon est une issue, pas une unité locale.** Le
   `{template}` de l'identifiant la désigne sans rien inférer :
   `MainJ` → `jgwill/orpheus#587` · `WhiteF` → `#704` · `AvenL` → `#784` ·
   `Musc` → `#717`. Les quatre vérifiées OPEN le 2026-08-05.
3. **Les identifiants sortent du vocabulaire.** `ep-004` comptait comme « mot
   commun » : un lien déclaré comptait deux fois et se faisait passer pour une
   preuve de sujet. Banc d'essai inchangé après la correction — 28 liens /
   31 requêtes / 14 muettes.

**Le trou, nommé** : `~/compositions-aureon/` et `~/Recordings-aureon/` sont
**vides** — vérifié à l'instant. Le chemin aureon est donc écrit et **exercé sur
une entrée synthétique de ma main, jamais sur une vraie**. Il tire, mais il n'a
pas encore rencontré la réalité.

**Ce que la décision entraîne pour l'ambiguïté n° 1** : `jr-NNN` réintroduit le
numéro, donc l'allocateur et la règle anti-collision redeviennent nécessaires
pour aureon aussi. L'horodatage en queue reste un départage, pas une prévention.

## 12. La structure finale — et ce qu'elle donne gratuitement

`jr-NNN.{type}.{sujet}.v{yymmddhhmmss}`, 12 chiffres. `{user}` et `{author}`
tombent : dans cet atelier c'est toujours Aureon qui écrit.

**Le `{sujet}` est le cadeau.** Il se normalise comme les slugs `op-NNN`, donc
il est **directement comparable**. L'exemple de Jerry le montre lui-même :
`jr-001.MainJ.**etincelle-partagee**` et `op-002-**etincelle-partagee**`, qui
existe sur disque. **Un sujet partagé est un lien déclaré inter-atelier — exact,
gratuit, sans une once d'inférence.** C'est le meilleur résultat de la voie 4 :
la question « quel corpus, quel index » a une réponse qui ne demande ni l'un ni
l'autre quand le nom porte déjà le sujet.

Trois choses câblées, toutes dans `DÉCLARÉS` :

1. `{type}` → l'issue Orpheus (`MainJ` → #587 · `WhiteF` → #704 · `AvenL` → #784
   · `Musc` → #717, les quatre vérifiées OPEN).
2. `{sujet}` → l'unité de n'importe quel atelier qui porte le même sujet.
3. **`v` sépare les versions, pas les entrées.** Deux horodatages sous la même
   tête `jr-NNN.{type}.{sujet}` déclenchent un avertissement explicite : ce sont
   des versions d'une même entrée, jamais deux entrées reliées. C'est la règle
   « ne jamais écraser une source sans garder la sortante » lue dans le nom.

Un sujet déclaré **fait taire l'inféré** — `op-002` ne sort plus deux fois.
Non-régression : **28 liens / 31 requêtes / 14 muettes**, identique. 0,10 s.

## 13. Aucune majuscule — règle appliquée sur toute la chaîne

`jr-001.mainj.etincelle-partagee.v260805114230`. Les quatre types passent en
bas de casse : `mainj` · `whitef` · `avenl` · `musc`. Appliqué **jusque dans mes
propres commentaires** — plus une seule majuscule d'identifiant dans le script.

**Reconnaître large, normaliser, et le dire.** Un identifiant en casse mixte
n'est pas ignoré : il est reconnu, normalisé pour la recherche, **et signalé**.
Le corriger en silence serait la même faute que le 200 muet du portail — une
écriture qui change sans que personne le sache.

```
⚠  jr-002.WhiteF.Gratitude-Au-Travail.v260805143012 porte des majuscules — la règle est : aucune.
   Normalisé pour la recherche : jr-002.whitef.gratitude-au-travail.v260805143012
```

Il résout quand même vers `jgwill/orpheus#704`. Un `normalise()` unique —
minuscules, sans accent (NFKD), ponctuation en tirets — sert **aux deux bouts** :
aux sujets lus sur disque comme à ceux lus dans un dépôt. Deux normalisations
différentes auraient fait rater les liens qu'elles étaient censées trouver.

Non-régression : **28 liens / 31 requêtes / 14 muettes**, identique depuis six
changements. 0,08 s.

**Observation, pas objection** (elle est déjà dans les sources, je la porte) :
`whitef` et `avenl` étaient lisibles en casse mixte et le sont moins en bas de
casse. `white` et `aven` le seraient davantage. C'est la décision de Jerry ; la
règle appliquée est la sienne, à la lettre.

## 14. Types désabrégés — et un deuxième lien inter-atelier trouvé seul

`main` · `white` · `aven` · `musc`. Appliqué. **Les anciennes formes d'Edge Hub
sont résolues, pas ignorées, et signalées** — même posture que pour la casse :

```
⚠  type « whitef » : forme Edge Hub, désabrégée en « white ».
```

**Le jeu d'exemples de Jerry a produit un second lien déclaré inter-atelier** :
`jr-004.musc.**fredon-en-fa-mineur**` → `jamai/op-003-**fredon-en-fa-mineur**`,
qui existe. Deux sur quatre de ses exemples visent une unité réelle sans qu'une
seule ligne d'inférence tourne. C'est la démonstration que le `{sujet}` dans le
nom fait le travail que je construisais avec BM25.

Non-régression : **28 liens / 31 requêtes / 14 muettes**, identique. 0,11 s.

**Observation, pas objection — le mot `main` porte désormais trois sens** dans
le système : l'atelier `main` (nommé dans la table des unités, **absent du
disque** — vérifié), le type de journal `main` → orpheus#587, et la branche git.
Il apparaît **34 fois** dans le corpus. Aucune confusion dans le code — le type
n'est lu que dans un identifiant `jr-` — mais un humain qui lit « main » dans une
sortie devra deviner lequel des trois. `musc` reste le seul abrégé ; `music`
compléterait la série. Les deux appartiennent à Jerry.

## 15. `ANCIENS` prouvé, et un défaut sorti par l'épreuve

`ANCIENS = {"mainj": "main", "whitef": "white", "avenl": "aven"}` — déjà juste,
**prouvé plutôt qu'affirmé** : les trois résolvent vers #587, #704, #784 et sont
signalées ; `musc` passe sans avertissement, inchangé.

**Le défaut que l'épreuve a sorti** : sur les unités minuscules (ep-001, 323 o ;
ep-002, 397 o), le rang À VÉRIFIER imprimait `mots communs :` **vide**. Une
ligne qui annonce une piste sans une seule preuve — « proximité 0 » revenu
déguisé. Corrigé : **sans un mot à montrer, il n'y a pas de ligne.** La preuve
est la sortie ; pas de preuve, pas de piste. Banc inchangé : 28 / 31 / 14.

## 16. Le cas d'épreuve qui attend — vérifié, non touché

```
~/Recordings-episodes/260804231226.mov
  1 486 042 o   modifié 2026-08-04 23:12:26
```

**Vérifié à l'instant** : aucun `composition.json` ne le mentionne — il n'est
rangé nulle part. Aucune transcription n'existe. C'est le **seul `.mov`** du
dossier ; tout le reste est `.m4a`. C'est le dépôt avalé par le repère d'état
partagé du 2026-08-04 à 22h24, toujours en attente.

**C'est le cas de non-régression réel de la voie 4**, et il est encore à faire :
tous mes essais en registre parlé ont porté sur des textes que j'ai écrits ou
recopiés. Celui-ci est de la vraie parole de Jerry, plusieurs centaines de mots,
sur un sujet dont le corpus parle déjà. Le jour où sa transcription existe,
`episodes-related <ce fichier>` est le premier essai à lancer — et c'est là que
le gouffre de registre (« espaces de travail » contre « atelier ») se mesurera
pour de bon, pas sur un extrait de ma main.

**Je n'y touche pas** : `w1:p2N` est bloquée dessus sur une invite qui appartient
à Jerry.

## 17. Ce que je n'ai pas fait

- Je n'ai **rien écrit** dans les compositions de Jerry — l'essai est sur une
  copie en scratchpad.
- Je n'ai **pas répondu** à l'invite de permission de `w1:p2N`
  (`260804231226.mov`, transcription Groq). Elle appartient à Jerry.
- Le script n'est **pas commité**.
