# 01 — Réalité actuelle : ce que la session a réellement produit

Toutes les valeurs chiffrées ici ont été mesurées pendant la session
`9f8a16f3-7151-4d35-a928-53f703ba9faa` (2026-08-08 → 08-10) sur la matière de
William, et rapportées dans la conversation au moment de la mesure.

## Coordonnées pour revenir

| | |
|---|---|
| herdr workspace | `w15` — « musique pour William par JamAI » (n° 7) |
| herdr pane | `w15:p1` · tab `w15:t1` · terminal `term_65893aea9491546` |
| session Claude | `9f8a16f3-7151-4d35-a928-53f703ba9faa` |
| transcript | `~/.claude/projects/-home-gmusic/9f8a16f3-7151-4d35-a928-53f703ba9faa/` |
| composition | `https://ilex.ferret-harmonic.ts.net:8768/compositions/ava001` (workspace `aureon`) |
| dossier | `~/compositions-aureon/ava001` sur `ilex.ferret-harmonic.ts.net:8022` |

## La matière de départ

304 notes issues de 4 prises Songbird (suivi de hauteur sur la voix, monophonique,
`hzMean` sur chaque note), 6 notes vocales parlées, 1 prise détruite par un flux
Retake destructif et jamais remplacée.

## Les six interventions, et ce que chacune a déplacé

### 1. « Les médias, des fois, pas le tempo réel »
**Dite avant toute mesure.** Vérifiée après : force d'autocorrélation du train
d'attaques **0,182** et **0,169** sur les deux grandes prises. Aucune pulsation
métrique. A évité d'imposer une grille à une matière en rubato.

### 2. « Un autre rythme, un autre timbre »
Deux axes de contraste nommés séparément. A produit : pad à **345 Hz** de
centroïde contre **585 Hz** pour la voix (bande distincte), et instruments à
**8 à 16×** le grain vocal. Sans cette phrase, l'accompagnement doublait la voix.

### 3. « Décide de la tonalité et garde la même tout du long »
A transformé une texture en pièce. La v1 était en K:C avec altérations
explicites — une façon élégante de ne pas choisir.

### 4. « Les demi-tons, c'est qu'on chante et on n'est pas pile sur la note »
**L'intervention la plus lourde.** Deux pièces entières étaient bâties sur un
motif qui était du bruit de captation.

Vérification : **46 % des notes à 0,092 s** (le quantum minimal du tracker) et
**50 % des enchaînements exactement à un demi-ton**. Une mélodie ne se déplace
pas d'un demi-ton une fois sur deux.

Après fusion des grappes voisines d'un demi-ton : **304 → 141 notes**, et la
tonalité change — Si♭ majeur (r=+0,621) devient **ré dorien** (couverture 70,9 %,
tonique confirmé à 0,635 contre 0,401 pour le suivant).

Jerry a couplé la conséquence dans la même phrase : « moins de doubles croches,
plus de croches ». Mesure après déglissage : IOI médian **0,186 s → 0,465 s**.
**Il a prédit l'effet rythmique d'un artefact de détection de hauteur.**

### 5. « Les croches, j'aimerais qu'elles soient liées » + « qu'est-ce qui fait ça ? »
Il lisait **la page**, pas l'audio : le MIDI avant/après ligature porte le même
SHA-256 `02cf8b7fcdead787…`. En ABC la ligature est décidée par les espaces de la
source. La demande de **cause** plutôt que de correctif a fait remonter que
l'information était déjà dans les skills de JamAI, non appliquée.

### 6. « Le marimba fait un peu trop exotique »
Formulé comme un goût, c'était un diagnostic. Mesure sur 13 candidats, sur sa
ligne réelle : marimba à **2,40 %** d'énergie dans le medium 0,5–2 kHz, **le plus
faible de tous**. JamAI attribuait depuis trois versions la couleur sombre au
registre choisi. Guitare jazz : **15,34 %**, soit 6,4×. Effet sur le mixage
complet : centroïde **428 → 606 Hz**, bande 1–2 kHz **0,45 % → 3,21 %**.

## Ce qui distingue ces six phrases

Elles ne portent presque jamais sur le résultat. Elles portent sur **ce que les
mesures veulent dire** — et deux fois sur **la façon dont l'instrument de mesure
ment**. C'est le seul endroit où JamAI est structurellement aveugle : il peut
tout compter, il ne peut pas savoir qu'un chiffre est un artefact de captation
si personne ne lui dit comment la captation échoue.

## Discipline établie dans la même session

- **Versions jamais écrasées** : v1 `52577c32…`, v2 `8326e238…`, v3 `03128ba4…`
  vérifiées inchangées après chaque dépôt.
- **`DELETE` du portail est destructif** : il efface le fichier du dossier de
  composition, réécrit `addedAt` et déplace le clip en fin de liste. Les
  étiquettes ont donc été posées **en place** dans `composition.json`, ordre et
  dates préservés.
- **La voix n'est pas archivée** : analysée sur autorisation, puis supprimée
  (`shred`), seuls les chiffres conservés.
