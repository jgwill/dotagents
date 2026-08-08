# atelier-veille — la veille de `jamai`, paramétrée pour les six ateliers

Généralisation de `jamai-watch` / `jamai-on-drop`. Même motif, mêmes quatre
couches, même coût : **zéro token de modèle** jusqu'à la couche 4.

```
atelier-watch <atelier> [--as <instance>]     la boucle   (couche 1 — empreinte)
  └─ atelier-on-drop <atelier> <fichier>      le crochet  (couche 2 — mesure)
       └─ verdict.txt + verdict.env           l'aiguillage (couche 3)
            └─ ateliers/<atelier>/after-drop  l'action     (couche 4 — auto, ou réveil)
atelier-claim-unit <atelier> "<Titre>"        le numéro, sous verrou
atelier-claim-unit <atelier> --version-de …   une version, sans consommer de numéro
atelier-post-text  <atelier> <slug> <f>       une section, dans sa propre seconde
```

## Ce qui était propre à jamai, ce qui était général

Séparé ligne à ligne sur les cinq scripts.

| dans `jamai-watch` / `jamai-on-drop` | verdict | devenu |
|---|---|---|
| `episode watch jamai` | propre | `episode watch "$ATELIER"` |
| `EPISODE_STATE_DIR=…/watch-standalone` | propre à **une** veille | `…/veilles/<atelier>--<instance>` |
| `jamai-watch.log` / `.pid` / `jamai-mine.txt` | propre à **une** veille | dans le dossier de la veille |
| `sed …Recordings-jamai/…` | propre | dérivé de l'atelier (`main` = `~/Recordings`, sans suffixe) |
| `drops/$(basename)` | **à plat — défaut** | `drops/<atelier>/<basename>` |
| chemin du crochet en dur | propre | `--hook`, défaut à côté du script |
| bornes de cadence 60/600 | général | idem, `ATELIER_VEILLE_MIN/MAX` |
| *(absent — défaut)* attendre la fin de l'écriture | général | `pose()`, absorbé de la voie 1 |
| *(absent)* amorcer le repère sans déclencher | général | `--prime`, absorbé de la voie 1 |
| `PIXEL_RECORDER_URL` supposé | propre | exporté depuis la table ; rien si « - » |
| détection midi / audio / texte | général | inchangé |
| `jamai-midi.py`, `-measure.py`, `-chords.py` | **généraux** — ils prennent un fichier | référencés, **pas recopiés** |
| seuil grave < 50 % & centroïde > 350 Hz | général | inchangé, avec son avertissement |
| appel Whisper (Groq) | général | inchangé |
| forme de `verdict.txt` | général | inchangé, **plus** `verdict.env` |
| que faire du verdict | **propre — et absent** | `ateliers/<atelier>/after-drop` |

`jamai-morning` et `jamai-unread.py` ne sont pas dans le motif de veille : ils
servent la lecture du matin, pas la boucle. Non touchés.

## La forme, tranchée et nommée comme un choix

Question 5 de Jerry offrait trois formes : veille paramétrée · un crochet par
atelier · un crochet commun à règles.

**Choix : veille paramétrée + crochet commun à règles + une action par atelier.**
Trois pièces, pas deux.

- La **mesure** est identique partout — un fichier est de la parole ou de la
  musique quel que soit le dossier où il tombe. La dupliquer six fois, c'est
  garantir que le seuil du grave sera corrigé dans une copie et pas dans les
  cinq autres. Elle reste dans **un seul fichier**.
- L'**action** diffère vraiment — Jerry veut un agent interactif pour `jamai`
  et des actions automatiques ailleurs. Elle est donc **un fichier par atelier**,
  `ateliers/<atelier>/after-drop`, exécutable ou absent.
- Les **règles** (unité, portail, mode, destination, sortie, queue) sont des
  données, pas du code : `ateliers.conf`.

Ce que ça coûte : un saut de plus à lire quand on débogue. Ce que ça évite :
six copies du seuil.

## `verdict.env` — pourquoi il existe

`verdict.txt` est une phrase, lisible par un humain. L'aiguillage ne doit pas
relire une phrase : ça demanderait un modèle, et la couche 3 doit coûter zéro.
`verdict.env` porte la même chose en variables :

```sh
. "$DOSSIER/verdict.env"
[ "$KIND" = parole ] && [ "$MODE" = auto ] && …     # aiguillage : du bash, rien d'autre
```

## Les cinq défauts payés — état

**1. Repère d'état partagé.** Chaque veille exporte `EPISODE_STATE_DIR` vers
`…/veilles/<atelier>--<instance>/`, jamais la racine où d'autres sessions
écrivent déjà. Deux veilles sur le même couple sont **refusées au démarrage** ;
pour en vouloir deux, il faut le dire : `--as <autre>`.

*Vérifié le 2026-08-05* : deux veilles `synth --as A` et `--as B`, un même
dépôt réel — **les deux l'ont vu**, aucune ne l'a volé à l'autre. Aucun
`watch-synth.sha` n'est né à la racine.

**2. Seuil de classement.** Le grave (`< 250 Hz`) est le discriminant ; le
médium n'apparaît plus que dans l'avertissement qui explique pourquoi il est
mort.

*Vérifié le 2026-08-05* : `260804222416.mov` — 37,58 % sous 250 Hz, médium à
53,31 %, le cas exact que l'ancien seuil ratait — classé **PAROLE**, transcrit.

**3. Fichier encore en cours d'écriture — trouvé par la voie 1, absorbé ici.**
`episode watch` ne signale un fichier qu'**une** fois : le repère réécrit, il ne
repassera plus. Traiter un dépôt qui grossit encore le perd **définitivement**.
`jamai-watch` n'avait pas cette garde. `pose()` attend que la taille se
stabilise, 24 × 5 s au plus, **avant** d'appeler le crochet.

*Vérifié le 2026-08-05* : un dépôt écrit par tranches sur 12 s — la veille a
attendu 16 s, et le crochet a mesuré les 1 770 416 octets complets (25,17 s
d'audio), pas le fragment. Classé MUSIQUE à 73,13 % sous 250 Hz — le chiffre du
fredon, l'autre côté du seuil.

**4. Numéros réclamés en double.** Paramétrer la veille autorise plusieurs
veilles ; `episode new` lit-le-max-puis-crée n'était sûr qu'à une. Deux pièges,
tous deux fermés :

- **Le verrou doit être le même pour tout le monde.** Un `flock` sur un fichier
  et un `mkdir` sur un dossier ne s'excluent pas — objets différents, chemins
  différents, et les deux allocateurs réclament `ep-009` ensemble. `atelier-claim-unit`
  emploie donc le `mkdir` de la voie 1, **au chemin exact** de sa chaîne vivante :
  `~/.local/state/episode-voice/<atelier>-numero.lock`.
- **Le motif de lecture ne doit pas exiger le tiret final.** La voie 1 crée des
  titres nus (`ep-009`, sans slug) ; un `ep-(\d+)-` les manquerait et rendrait
  `ep-009` une seconde fois.

Reste non résolu, et nommé : une unité créée à la main dans le portail pendant
la fenêtre échappe au verrou.

**5. Deux sections texte dans la même seconde — trouvé par la voie 1, absorbé
ici.** Le portail nomme lui-même chaque section `transcription_<AAAAMMJJHHMMSS>_FR.txt`
— granularité **seconde**, et le client n'a aucune prise dessus : il n'envoie
que le texte, la langue, le label et le clip source (vérifié dans `episode`,
l. 336–338). Deux dépôts dans la même seconde portent le même nom ; le second
écrase le premier **sur disque**, avec un 200 et pas un mot. Sur ep-009 la
transcription (265 o) avait disparu sous les reliés (621 o), survivant seulement
dans le `content` de `composition.json`.

`atelier-post-text` attend que la seconde courante ait **dépassé** celle du
dernier dépôt réussi, sous verrou. C'est déterministe là où un `sleep 2` est une
estimation : le `sleep` tient pour deux sections, et retombe dans le trou à la
troisième ou si le portail répond plus vite qu'on ne l'a supposé.

*Vérifié le 2026-08-05* : trois dépôts d'affilée → secondes 07:29:34, 35, 36.
Deux dépôts **simultanés** → 07:29:37 et 38, le verrou les ayant sérialisés.

Hypothèse nommée : le portail et nous partageons l'horloge — vrai tant qu'il
répond sur localhost, ce qui est le cas des deux portails vivants.

*Note :* la garde vit dans la bibliothèque (`av_seconde_distincte`) et sert les
sections texte du portail. Elle avait aussi servi à un identifiant purement
horodaté, forme abandonnée sur décision de Jerry — le numéro porte désormais
l'unicité, et `v{ts}` n'est plus qu'un départage.

## La chaîne `episodes` de la voie 1 — absorbée, pas doublée, pas basculée

`episodes-watch` / `episodes-on-drop` **tournent en ce moment** (pid 2917786,
vérifié) et attendent le dépôt de Jerry demain matin. **Je n'y ai pas touché.**
Elles n'entrent pas en conflit avec le générique : leur repère est
`…/watch-episodes/`, celui du générique `…/veilles/episodes--<instance>/`.

Ce qu'elles ont payé est absorbé ci-dessus (`pose()`, verrou `mkdir` au même
chemin, motif sans tiret final). Ce qui reste est une **migration**, pas un
doublon — le seam est net, relu ligne à ligne le 2026-08-05 :

| dans `episodes-on-drop` | correspond à |
|---|---|
| §1 mesure · §2 transcription (l. 48–113) | déjà générique dans `atelier-on-drop` |
| §3 quel épisode reçoit · §4 attacher · §5 reliés · §6 ce qui reste (l. 115–219) | deviendrait `ateliers/episodes/after-drop`, lisant `verdict.env` au lieu de re-mesurer |

**Cette bascule ne se fait pas avant le réveil de Jerry.** Elle rejouerait la
mesure et l'appel Whisper une seconde fois tant qu'elle est à moitié faite, et
elle remplacerait une chaîne éprouvée par une chaîne non éprouvée à quelques
heures du seul dépôt qui compte. C'est un choix, pas un oubli.

## Ce qui est un trou, et reste un trou

`ateliers.conf` porte `?` pour ce qui n'est pas nommé. **Un outil qui tombe sur
un `?` s'arrête** au lieu d'inventer — vérifié : `atelier-claim-unit aureon`
refuse et dit pourquoi.

| atelier | unité | portail | mode | destination | sortie |
|---|---|---|---|---|---|
| jamai | `op` (op-004 libre) | 8768 ✓ | réveil | — | pièce |
| episodes | `ep` (ep-009 libre) | 8778 ✓ | auto | **?** | épisode |
| aureon | **?** | aucun | **?** | **?** | journal\* |
| nyro · synth · main | **?** | aucun | **?** | **?** | **?** |

Quatre ateliers sur six n'ont ni unité, ni portail, ni mode. La voie 3 remplit
les noms ; les portails et les modes appartiennent à Jerry.

### Un seul allocateur, numéroté partout — décision de Jerry, 2026-08-05

L'identifiant est partout `<unite>-NNN<queue>`. **Le numéro porte l'unicité**,
donc l'allocateur et sa règle anti-collision sont nécessaires dans les trois
ateliers. `EN-Entries:` était l'ancien système Edge Hub : on garde sa structure,
on remplace sa tête par un préfixe numéroté.

| atelier | identifiant | queue |
|---|---|---|
| jamai | `op-NNN-slug` | `-{slug}` — le portail slugifie le titre |
| episodes | `ep-NNN-slug` | `-{slug}` |
| aureon | `jr-NNN.{type}.{sujet}.v{yymmddhhmmss}` | `.{type}.{sujet}.v{ts}` |

Dans `aureon` c'est **toujours Aureon qui écrit** et Jerry qui possède le
journal : les segments `{user}` et `{author}` d'Edge Hub n'ont plus d'objet.
Restent le type de journal, le sujet, et la date **à la seconde — douze
chiffres**.

```
jr-001.main.etincelle-partagee.v260805115751
jr-002.white.gratitude-au-travail.v260805115751
jr-003.aven.souffle-avant-la-marche.v260805115752
jr-004.musc.fredon-en-fa-mineur.v260805115752
```

### Aucune majuscule — règle de Jerry, appliquée à toute la chaîne

**L'identifiant entier** est en minuscules, pas seulement le sujet. Un
identifiant est un nom de fichier ; il doit survivre à un système insensible à
la casse sans que deux entrées se confondent.

Les quatre types sont **désabrégés** — les abréviations d'Edge Hub tenaient à la
casse mixte et ne servaient plus en bas de casse :

| type | journal | issue d'origine |
|---|---|---|
| `main` | Main Journal — Jericho's Reflections | orpheus#587 |
| `white` | Spiritual Journal — White Feather | orpheus#704 |
| `aven` | Aven's Loops — Emotional Anchors | orpheus#784 |
| `musc` | Gmusic Lyrics — Spiritual Composition | orpheus#717 |

`musc` reste le seul abrégé, non nommé dans cette passe — `music` compléterait
la série.

La règle est appliquée par **normalisation, pas par refus** — un `--type Main`
ou `--type AVEN` donné en entrée retombe sur `main` et `aven`, et une tête
`jr-001.Main.…` passée à `--version-de` retombe sur `jr-001.main.…` plutôt que
d'ouvrir une entrée voisine.

*Vérifié le 2026-08-05* : quatre réclamations avec de la casse mixte et des
capitales en entrée → **aucune majuscule** dans les identifiants produits.

### La normalisation vient de la voie 3, reprise telle quelle

`av_slug` **n'est pas une implémentation de plus**. C'est celle de la voie 3,
copiée caractère pour caractère : la seule qui reproduit `slugify()` de
`pixel-recorder.js` — décomposition **NFD** puis retrait des marques
combinantes. Deux normalisateurs qui divergent d'un caractère produisent deux
slugs pour un même titre, et c'est un doublon qu'aucun verrou n'attrape.

J'en portais un deuxième, et il divergeait pour de vrai — j'avais écrit `NFKD`,
la décomposition de *compatibilité* :

```
« Œuvre ﬁnale »        NFD (le portail) → uvre-nale     NFKD (le mien) → uvre-finale
« Puissance 2² du son » NFD (le portail) → puissance-2-du-son   NFKD → puissance-22-du-son
```

Le résultat du portail est le moins joli des deux — et c'est celui qu'il faut :
l'objectif est de coïncider avec lui, pas de faire mieux que lui.

Les deux pièges que la voie 3 a payés, portés dans le commentaire du code :
`iconv //TRANSLIT` rend « é » par `'e`, apostrophe comprise, et fend
« Étincelle partagée » en `etincelle-partag-ee` — invisible sauf sur les sujets
accentués, c'est-à-dire la plupart. Et normaliser **chaque segment puis joindre
par des points**, jamais l'identifiant assemblé : `slugify` remplace les points
eux-mêmes et détruirait la structure.

*Vérifié le 2026-08-05* : identique aux **sept** slugs déjà sur disque et aux
**quatre** sujets d'exemple de Jerry ; un point placé dans un sujet
(`ep.009 relu` → `ep-009-relu`) ne fabrique aucun segment fantôme.

### Un type hors série avertit, mais ne bloque pas

La série bouge encore : bloquer figerait un choix qui appartient à Jerry. Mais
une faute de frappe muette produirait un `jr-005.mian.…` qui a l'air bon, et un
identifiant dont tout l'intérêt est de porter du sens ne doit pas mentir en
silence. D'où un **avertissement sur stderr**, et l'écriture quand même.

*Vérifié le 2026-08-05* : `--type mian` et `--type WhiteF` avertissent tous deux
(`hors de la série connue`) et produisent `jr-005.mian.…` / `jr-006.whitef.…`.
La série vit dans **une seule ligne** de `atelier-claim-unit` — la déplacer,
c'est un mot à changer.

*À noter, sans conséquence de chemin* : `main` est désormais à la fois un type
de journal d'aureon et un nom d'atelier dans la table. Les deux vivent dans des
espaces séparés — un atelier nomme des dossiers (`veilles/main--…`,
`drops/main/`), un type ne paraît que dans l'identifiant `jr-NNN.main.…`. Aucune
collision de chemin ; la ressemblance est à l'œil seulement.

### Deux versions d'une entrée, et ce que `v` sépare

`--version-de <tête>` reprend `jr-NNN.{type}.{sujet}` (ramenée en minuscules), change le `v`,
et **ne consomme aucun numéro** : une entrée différente prend un numéro neuf,
une version garde le sien. « Ne jamais écraser une source sans garder la
sortante » est portée par le nom.

**C'est le seul endroit où le `v` porte l'unicité** — la tête y est partagée par
construction, donc deux versions dans la même seconde porteraient le nom
identique, exactement l'écrasement que la règle interdit. `av_seconde_distincte`
s'applique donc là, et **seulement là** : une entrée neuve n'attend pas, son
numéro suffit.

*Vérifié le 2026-08-05* : trois versions d'affilée sans pause →
`v…114545 · 47 · 48` ; deux versions simultanées → `…114549` et `…114550` ;
trois **entrées neuves** d'affilée → `jr-005 · 006 · 007`, toutes à
`v260805114550`, **en zéro seconde d'attente**.

**Le trou que l'idée horodatée masquait : aureon n'a aucun portail.** Un
allocateur qui n'interroge qu'une API ne peut pas le servir. Il lit donc **trois
sources** et prend la plus haute : le portail *s'il est déclaré*, le disque
(`~/compositions-<atelier>/<préfixe>-NNN*`), et un registre local
(`$AV_STATE/<atelier>-unites.txt`) — sans ce dernier, deux appels d'affilée sur
un atelier sans portail rendraient `jr-001` deux fois.

Le registre est écrit **avant** toute création : si le portail refuse ensuite,
on a brûlé un numéro, ce qui se répare à la main. L'inverse ne se répare pas —
deux entrées sous le même numéro se recouvrent en silence.

*Vérifié le 2026-08-05* : sept réclamations sur `aureon` (sans portail, disque
vide), dont **quatre lancées simultanément** → `jr-001` … `jr-007`, **sept
numéros distincts sur sept**.

### Le mode dit *où* tombe la ligne, pas seulement de quel côté

`mode` valait `auto` ou `reveil` — un binaire. Le flux rituel d'aureon
(**Réalisation → Brouillon → Revue → Publication**) montre que la ligne a une
position, pas juste un côté : les deux premières étapes se mécanisent, la
**Revue appartient à Jerry**, la publication suit. D'où une troisième valeur,
`revue`. `verdict.env` la porte, et l'action de l'atelier branche dessus.

### Le motif a seize mois d'avance sur nous

`EchoThreads#115`, commentaires 6 à 8, avril 2025 : **RAVEN** détecte le ton et
charge le gabarit → invoque **AVEN** qui ancre → **AUREON** structure, relie et
publie. C'est empreinte → crochet → aiguillage → agent, écrit avant nous pour
cet atelier. Et c'est un argument de plus pour l'action **par atelier** plutôt
qu'un crochet unique : à la couche 4, ils sont **trois agents**, pas un.

**La sixième colonne existe parce que « un dépôt → une composition » est faux.**
`aureon-journal-events/SKILL.md` (18 131 o) décrit quatre contenants — Main
Journal · White Feather · Musical · AVEN Loop — choisis par **détection de
signature**, pas une pièce numérotée de plus. La sortie du crochet est donc
**typée** : `verdict.env` porte `KIND` (ce qu'EST le fichier) *et* `TYPE_SORTIE`
(ce que le dépôt OUVRE ici). `atelier-claim-unit aureon` **refuse** et dit
pourquoi, au lieu d'inventer un `au-001`. Le `*` marque la valeur comme
proposée : la matière est lue, la confirmation est à Jerry.

Correction de fait au brief : **`main` n'a pas de paire `-main`**. `episode`
le mappe sur `~/Recordings` + `~/compositions` (37 fichiers · 29 entrées). Cinq
paires suffixées + `main` en nu.

## Où ça vit — proposé, pas décidé

Ici, `~/.agents/skills/atelier-veille/`, à titre **provisoire**. Aucun chemin
absolu n'est câblé : les scripts résolvent leur propre dossier, et quatre
variables couvrent le reste (`ATELIER_VEILLE_CONF`, `_HOOKS`, `_OUTILS`,
`_STATE`). **Le dossier entier se déplace avec un seul `mv`, sans qu'une ligne
change.**

Trois destinations possibles, à Jerry de trancher :

1. **`jamai-morning/scripts/`** — proche des mesureurs qu'il réutilise. Contre :
   le nom dit « jamai » alors que l'outil sert six ateliers.
2. **`atelier-veille/` en compétence propre** *(l'endroit actuel)* — le nom dit
   ce que c'est. Il manque un `SKILL.md` pour qu'elle se charge vraiment ; je ne
   l'ai pas écrit, parce que c'est décider qu'elle est une compétence.
3. **`gmtermux`** — c'est le dépôt d'innovation que Jerry a nommé, et le seul
   qui traverse les machines de la forêt. Contre : les mesureurs restent dans
   `~/.agents`, la paire serait coupée en deux.

## Usage

```sh
atelier-watch --list                        la table
atelier-watch episodes --prime              poser le repère sans rien déclencher
atelier-watch episodes &                    veiller
atelier-watch jamai --as matin &            une seconde veille, nommée
atelier-watch episodes --status | --stop
atelier-watch episodes --once               un tour, puis sortir
atelier-claim-unit episodes --peek          le prochain numéro, sans créer
atelier-claim-unit episodes "Titre"         le réclamer, sous verrou
atelier-claim-unit aureon --type main "Étincelle partagée"
atelier-claim-unit aureon --version-de jr-001.main.etincelle-partagee
atelier-post-text episodes <slug> t.txt     une section, sans en écraser une autre
atelier-post-text episodes <slug> t.txt --dry-run   la seconde qu'elle prendrait
```
