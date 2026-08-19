# Voie 3 — la table des six ateliers

*Vérifié le 2026-08-05. Chaque chemin, port, compte et empreinte vient d'une
commande lue dans le même tour. Ce qui est proposé est marqué **proposition**.*

---

## Deux corrections au brief, avant la table

**1. `main` n'a pas de paire suffixée.** `~/Recordings-main` et
`~/compositions-main` **n'existent pas**. L'atelier `main` est le suffixe
**vide** : `~/Recordings` + `~/compositions`. Deux sources concordent :

- `episode` ligne 470-477 — `watch_dirs()` : `if [ "$ws" = "main" ] || [ -z "$ws" ]`
  → `$HOME/compositions` et `$HOME/Recordings`.
- `pixel-recorder.js` ligne 47 — `WORKSPACE_NAV_ORDER = ['', 'episodes', 'aureon', 'nyro', 'jamai', 'synth']`
  ; la clé `''` porte le label `Main`.

Conséquence directe : toute veille écrite en supposant `Recordings-main`
surveille un dossier inexistant et ne verra jamais rien. Silencieusement.

**2. Trois portails répondent, pas deux.** Le troisième est sur **8868** et sert
`main` — 23 compositions. Mais c'est
`/home/gmusic/salix/repos/gmtermux-244/web/.songbird-preview.js` (pid 3470965),
lancé par la session `wR:p4` *songbird-246-implement*. **C'est un aperçu de
travail, pas un portail d'atelier durable** — il disparaîtra avec sa session.
Ne pas l'inscrire comme le registre de `main`.

---

## La table

**La colonne qui manquait, et qui change la conception : le type de sortie.**
Un atelier ne produit pas forcément une *pièce*. `aureon` produit des **entrées
de journal typées** — la matière apportée par Jerry le 2026-08-05 l'établit, et
elle est vérifiée plus bas.

| atelier | dépôt (surveillé) | publié dans | portail | **type de sortie** | unité | identifiant | attribution |
|---|---|---|---|---|---|---|---|
| **main** | `~/Recordings` — 37 | `~/compositions` → `nyro-assembly/gbravo` | 8868 *(aperçu, transitoire)* | **pièce** | *proposition : chanson* | *`ch-NNN-slug`* | séquentielle — **collision possible** |
| **aureon** 🌿 | `~/Recordings-aureon` — 0 | `~/compositions-aureon` (vide) **+ `ea-portal`** | aucun | **entrée de journal typée** — 4 contenants | **journal** *(décidé)* | **`jr-NNN.{type}.{sujet}.v{yymmddhhmmss}`** | séquentielle — **collision possible**, départagée par l'horodatage de queue |
| **episodes** 🎙️ | `~/Recordings-episodes` — 40 | `~/compositions-episodes` → `Gerico1007/assembly-episode` | **8778** | **épisode** | **épisode** *(établi)* | **`ep-NNN-slug`** | séquentielle — **collision possible** |
| **jamai** 🎸 | `~/Recordings-jamai` — 44 | `~/compositions-jamai` → `Gerico1007/assembly-jamai` | **8768** | **pièce musicale** | **opus** *(établi)* | **`op-NNN-slug`** | séquentielle — **collision possible** |
| **nyro** ♠️ | `~/Recordings-nyro` — 1 | `~/compositions-nyro` — **pas un dépôt git** | aucun | inconnu | *proposition : rite* | *`ri-NNN-slug`* | séquentielle — **collision possible** |
| **synth** 🧵 | `~/Recordings-synth` — 0 | `~/compositions-synth` — **pas un dépôt git** | aucun | inconnu | *proposition : fil* | *`fl-NNN-slug`* | séquentielle — **collision possible** |

Les noms en italique sont des propositions et appartiennent à Jerry. Ils passent
le test que le script `episode` s'impose à lui-même — se dire à voix haute sans
ambiguïté : *« chanson douze », « rite un », « fil cinq »*.

**La ligne d'aureon n'est pas une proposition : elle est tranchée.** Jerry a
décidé le 2026-08-05 — on garde la **structure** d'`EN-Entries:` et on remplace
sa tête par un préfixe numéroté. La table est **homogène** : `op-NNN`, `ep-NNN`,
`jr-NNN`. Trois ateliers, un seul mécanisme.

> **Le trajet des propositions, laissé écrit.** *(a)* *miroir / `mr-NNN`* —
> tombée : aureon ne produit pas de pièces. *(b)* *quatre séries `jr` · `pb` ·
> `mu` · `av`* — tombée : la structure existait déjà et portait le contenant
> dans l'identifiant. *(c)* *garder `EN-Entries:` tel quel* — écarté par Jerry :
> c'est **l'ancien système Edge Hub**, on n'en garde que la forme.
> La décision retient `jr-` de *(b)* et la queue de *(c)*. Aucune des trois
> n'était juste seule ; l'écrire évite de croire qu'on y est arrivé d'un coup.

---

## Aureon — l'atelier qui n'est pas fait de compositions

*Vérifié le 2026-08-05 à partir de `sources-aureon.md`, en relisant chaque
chemin. Trois affirmations de cette fiche sont fausses ; elles sont corrigées
ci-dessous, et le fond tient.*

### Ce qui est confirmé

`~/Downloads/aureon-journal-events.zip` — 7 672 octets, deux entrées, dont
`aureon-journal-events/SKILL.md` de **18 131 octets** exactement. En-tête :
`name: aureon-journal-events`, `metadata.version: 1.0.0`. Les quatre types
d'événement sont aux lignes 40, 63, 87, 111 du SKILL, chacun titré
`ÉVÉNEMENT → contenant` :

| événement | contenant | longueur | `{template}` **canonique** |
|---|---|---|---|
| 📍 **THRESHOLD** — bascule, transition, arc | Main Journal | 150–300 mots | **`main`** |
| 🕊️ **SACRED** — moment sacré | White Feather Journal | 100–200 mots | **`white`** |
| 🎵 **SONIC** — événement sonore | Musical Journal | 100–180 mots | **`musc`** |
| 🔁 **ECHO** — résonance, retour | AVEN Loop | 30–80 mots | **`aven`** |

Ces quatre jetons ne sont pas de moi : ils viennent de `EchoThreads#115`, et
c'est ce que « le type de sortie » veut dire. L'unité d'aureon est une
**entrée** ; le type d'événement choisit le `{template}`, qui est **dans
l'identifiant**. Il n'y a rien à numéroter.

`SKILL.md:237-265` — le *Detection Protocol* en trois pas : écouter la
signature → confirmer le type → activer le contenant. Et **`SKILL.md:254`** :
*« Default to **Main Journal** if truly unclear »*. Cette ligne compte : elle
donne un repli déterministe, donc gratuit.

`SKILL.md:388-406` — le protocole d'archivage laisse trois options
(*Ephemeral Offerings* · *Ceremonial Database* · *Google Drive Integration*) et
se termine par **« User chooses »**. Ce n'est pas à trancher ici.

`~/Downloads/aureon-archive-2025-11-16.json` — 2 399 octets, `version: 1`,
`artifacts` : **4**. Une seconde copie de 488 octets existe.

### Trois corrections à `sources-aureon.md`

1. **Le dépôt canonique est `~/salix/repos/EchoThreads`, pas
   `~/workspace/EchoThreads`.** Les deux existent et portent le même distant
   `git@github.com:jgwill/EchoThreads.git`. Mais `CLAUDE.md` du projet est
   explicite : *« Canonical active repo root: `/home/gmusic/salix/repos/` […]
   Treat `/home/gmusic/workspace/*` as archival/reference only »*. Et c'est le
   bon sens factuel : `salix` est sur `fix/cypher-349-portable-runtime` (f61352f,
   fichiers de mai 2026), `workspace` sur `400-refactor-link2abc-namespace`
   (97341ab, fichiers de novembre 2025). C'est aussi la copie **en service** —
   le receveur d'intake sur le port 8787 tourne depuis
   `~/salix/repos/EchoThreads/music/packages/gmusic-assembly/bin/`.
2. **Les gabarits EchoForm ne sont pas dans `templates/`.** Ils sont dans
   **`docs/EchoForms/`**, et là les cinq tailles annoncées sont exactes :
   `EchoForm1_template.md` 7 009 · `EchoForm2_template.md` 7 869 ·
   `EchoForm3_template.md` 9 353 · `EchoFormSelectionProcess.md` 5 006 ·
   `README.md` 8 417. Ce que `templates/` contient réellement, c'est
   `echoform1_template.md` (2 606), `first_reflection_template.md` (333),
   `miette.prompt.md` (1 828) — et `docs/templates/` n'a qu'un `ECHOFORM1.md`
   de 493 octets. Les deux listes de la fiche sont interverties.
3. **L'artefact d'archive a neuf clés, pas huit** : `id · timestamp ·
   artifactType · format · content · metadata · journalContent · tags ·
   **thumbnail**`.

Et un fait que la fiche ne dit pas : **la compétence n'est pas installée.** Rien
sous `~/.agents/skills`, `~/.hermes/skills` ni `~/.claude/skills` ne porte
`aureon`. Elle n'existe qu'en zip dans `~/Downloads`, daté du 15 novembre 2025.
C'est une doctrine disponible, pas une doctrine en service.

### Ce que ça change pour le crochet générique

Le crochet ne peut plus supposer *« un dépôt → une composition »*. Pour aureon,
un dépôt ouvre **un contenant parmi quatre**. Mais la ligne
automatique/réveil se trace quand même, et plus bas qu'on ne croirait :

| ce que bash établit seul | ce qui réveille un modèle |
|---|---|
| le fichier *est* du son → **SONIC**, par le discriminant du grave qui fonctionne déjà dans `jamai-on-drop` | distinguer **THRESHOLD / SACRED / ECHO** — ce sont des significations, pas des mesures |
| le repli : **Main Journal**, prescrit par `SKILL.md:254` | rédiger l'entrée dans le gabarit du contenant |

Donc même ici, un dépôt non jugé n'est pas un dépôt perdu : il atterrit dans le
Main Journal, gratuitement, et un modèle l'affine s'il est réveillé.

### La destination de « republier ailleurs » — un candidat, pas un fait

`~/salix/repos/EchoThreads/ea-portal/src/` contient déjà **`MainJournal.tsx`**,
**`MusicalJournal.tsx`**, **`WhiteFeatherJournal.tsx`** — trois des quatre
contenants sont des composants d'interface existants. L'AVEN Loop n'en a pas.

Cela **ressemble** fortement au *« autre lieu »* que Jerry évoque. Je le laisse
marqué comme candidat et non comme fait : rien dans ce qu'il a dit ne nomme
`ea-portal`, et l'inférence est la mienne. La question lui revient.

---

## La convention d'aureon — tranchée par Jerry le 2026-08-05

```
jr-NNN.{type}.{sujet}.v{yymmddhhmmss}
```

```
jr-001.main.etincelle-partagee.v260805114230
jr-002.white.gratitude-au-travail.v260805143012
jr-003.aven.souffle-avant-la-marche.v260805220544
jr-004.musc.fredon-en-fa-mineur.v260806081127
```

**Aucune majuscule, nulle part.** La règle porte sur l'identifiant **entier**,
pas seulement sur le sujet — un identifiant est un nom de fichier, et il doit
survivre à un système de fichiers insensible à la casse sans que deux entrées
se confondent.

| segment | contenu | source |
|---|---|---|
| `jr-NNN` | numéro séquentiel, allocateur sous verrou comme `op-` et `ep-` | notre convention |
| `{type}` | `main` · `white` · `aven` · `musc` | Edge Hub, **en minuscules et désabrégé** |
| `{sujet}` | le sujet abordé, minuscules-tirets sans accent | **remplace `{user}` et `{author}`** |
| `v{yymmddhhmmss}` | horodatage UTC **à la seconde — 12 chiffres** | Edge Hub, résolu à la seconde |

**`{user}` et `{author}` disparaissent, et pour une raison de fond :** dans cet
atelier c'est **toujours Aureon qui écrit**, et le journal est **toujours** celui
de Jerry. Deux segments qui ne varient jamais ne portent aucune information —
ils occupent la place que le **sujet** méritait. La forme finale dit trois
choses, et chacune varie : *quel journal · de quoi ça parle · quand*.

**Une seule série par atelier**, comme `op-` et `ep-`. Le type n'est pas un
registre séparé : c'est un segment. Un `jr-004` en `musc` suit un `jr-003` en
`aven` — le compteur est celui de l'atelier, pas celui du journal.

Les quatre types, désabrégés, et leur journal d'origine tel que `#115` le
nomme :

| type | journal | issue d'origine |
|---|---|---|
| `main` | Main Journal — Jericho's Reflections | `orpheus#587` |
| `white` | Spiritual Journal — White Feather | `orpheus#704` |
| `aven` | Aven's Loops — Emotional Anchors | `orpheus#784` |
| `musc` | Gmusic Lyrics — Spiritual Composition | `orpheus#717` |

*Deux observations, aucune objection.* **(a)** `musc` reste le seul abrégé —
`music` compléterait la série, mais Jerry ne l'a pas nommé dans cette passe et
`musc` tient. **(b)** Le jeton `main` du type et l'atelier `main` portent
maintenant le même mot dans deux espaces de noms distincts. Aucune collision
technique — un type ne se lit qu'en deuxième segment d'un `jr-` — mais
`jr-001.main.…` dans l'atelier `aureon` se lira de travers un jour, par
quelqu'un qui n'aura pas cette table sous les yeux.

### La seconde, pas la minute — et pourquoi c'est une correction, pas un détail

La spécification d'Edge Hub annonce `v{yymmddhhmmss}` — douze chiffres — mais
**ses trois exemples n'en portent que dix** : `v2504121923` se lit
`25·04·12·19·23`, soit une précision à la **minute**. La source se contredit
elle-même. La décision de Jerry tranche pour la seconde, et le motif est
opérationnel : **une veille automatique peut produire deux versions dans la même
minute ; un humain, non.** À dix chiffres, ces deux versions portent le même
nom et la seconde écrase la première en silence.

### Ce que `v` sépare — les versions, pas les entrées

Deux versions de la même entrée gardent la même tête `jr-NNN.{type}.{sujet}` et
changent de `v`. Une entrée **différente** prend un numéro neuf.

La règle qui a coûté un schéma le 2026-08-04 — *ne jamais republier une source
sans garder d'abord la version sortante* — n'a donc plus besoin d'être appliquée
par discipline : **le nom la porte.** Republier, c'est écrire un `v` neuf à côté,
pas par-dessus.

### La normalisation s'applique par segment, jamais à la chaîne assemblée

`pixel-recorder.js:839-844` :

```js
function slugify(title) {
  return title.toLowerCase()
    .normalize('NFD').replace(/[̀-ͯ]/g, '')  // strip accents
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}
```

C'est exactement la normalisation demandée — minuscules, accents retirés,
ponctuation en tirets — et c'est elle qui a produit `op-002-etincelle-partagee`.

**Mais il y a un piège, et il vient de la règle elle-même.** « Normalisation sur
toute la chaîne » veut dire *chaque segment est normalisé*, **pas** *on passe
l'identifiant assemblé dans `slugify`*. Les deux se disent pareil et ne font pas
la même chose : `slugify` remplace tout ce qui n'est pas `[a-z0-9]` par un
tiret — **y compris les points qui délimitent les segments**.

```
slugify("jr-001.main.etincelle-partagee.v260805114230")
  -> jr-001-main-etincelle-partagee-v260805114230     ← structure détruite
```

L'ordre correct est : **normaliser chaque segment, puis joindre par des points.**

```bash
id="jr-$(next).$(slug "$type").$(slug "$sujet").v$(date -u +%y%m%d%H%M%S)"
```

### Et `slug` ne doit pas être écrit avec `iconv` — mesuré, pas supposé

Le réflexe en bash est `iconv -t ASCII//TRANSLIT`. **Il produit un identifiant
faux**, et silencieusement :

```
« Étincelle partagée »
  iconv //TRANSLIT   -> etincelle-partag-ee      ← un tiret de trop
  NFD + strip        -> etincelle-partagee       ← ce que Jerry a écrit
```

`//TRANSLIT` rend `é` par `'e` — apostrophe comprise — et l'apostrophe devient
un tiret. Le mot se fend au milieu. Sur `souffle-avant-la-marche` et
`fredon-en-fa-mineur`, sans accent, les deux voies donnent le même résultat :
**le défaut ne se voit que sur les sujets accentués**, c'est-à-dire la plupart
de ceux de Jerry.

La seule implémentation qui reproduit `pixel-recorder.js:839` est la décomposition
NFD avec retrait des marques combinantes :

```bash
slug() { printf '%s' "$1" | python3 -c "
import sys, unicodedata, re
s = unicodedata.normalize('NFD', sys.stdin.read()).lower()
s = ''.join(c for c in s if not unicodedata.combining(c))
print(re.sub(r'[^a-z0-9]+', '-', s).strip('-'))"; }
```

Vérifié sur les quatre sujets d'exemple de Jerry : identique à sa graphie, dans
les quatre cas.

Ce que ça protège, dans l'autre sens : un point non filtré **dans le sujet**
fabriquerait un segment fantôme — `jr-005.main.ep.009-relu.v…` se lirait à cinq
segments au lieu de quatre, et le compteur comme le lecteur s'y tromperaient.
`slugify` transforme ce point en tiret. Le garde-fou est déjà écrit ; il faut
seulement l'appliquer au bon endroit.

*Observation retenue par Jerry le même jour* : en bas de casse, `whitef` et
`avenl` avaient perdu la lisibilité que la casse mixte leur donnait. Les trois
types sont désabrégés — `main`, `white`, `aven`. `musc` reste, non nommé dans
cette passe.

**Ce que la décision entraîne, et c'est le cœur de ma voie :** le numéro revient,
donc **l'allocateur et la règle anti-collision redeviennent nécessaires pour les
trois ateliers**. Ce n'est plus un choix ouvert. La section anti-collision
ci-dessous porte désormais sur `op-NNN`, `ep-NNN` **et** `jr-NNN`.

Mais la queue horodatée n'est pas décorative — elle **départage**. Deux `jr-004`
créés par deux veilles ne sont pas indistinguables comme le seraient `ep-009-a`
et `ep-009-b` : ils portent `v260805114331` et `v260805114332`, donc un ordre et
une réparation possible. **Le verrou empêche la collision ; l'horodatage la rend
survivable si le verrou manque.** C'est ce que la structure conservée apporte, et
c'est pourquoi la garder valait mieux que la refaire.

---

## D'où vient cette structure — `EN-Entries:`, l'ancien système Edge Hub

*Établi par `jgwill/EchoThreads#115`, « Aureon Journal Migration — Unified Entry
System », ouverte le 2025-04-04, neuf commentaires. Titre, date et nombre de
commentaires relus via `gh` le 2026-08-05 ; le format ci-dessous est recopié du
corps du commentaire, pas résumé.*

```
EN-Entries:.{template}.{user}.{author}.v{yymmddhhmmss}
```

Présenté dans l'issue comme *« the canonical naming convention for AI-generated
journaling entries across Raven, Aureon, and AVEN agents »*, clé
`ET.115.keyformatguide.v2504121927`. Exemples, tels quels :

```
EN-Entries:.WhiteF.Jericho.mix.v2504121923
EN-Entries:.AvenL.Jericho.rav.v2504122030
EN-Entries:.MainJ.Lian.aur.v2504121945
```

| segment | contenu |
|---|---|
| `{template}` | le contenant — `WhiteF`, `AvenL`, `Musc`, `MainJ` |
| `{user}` | propriétaire du journal — `Jericho`, `Lian` |
| `{author}` | origine — `rav`, `aur`, `usr`, `mix` |
| `v{yymmddhhmmss}` | horodatage UTC **à la seconde** |

### Ce qui a été gardé, ce qui a été jeté

| segment Edge Hub | sort | pourquoi |
|---|---|---|
| `EN-Entries:` | **remplacé** par `jr-NNN` | ancien système Edge Hub ; le préfixe numéroté remet aureon en ligne avec `op-` et `ep-` |
| `{template}` | **gardé**, renommé `{type}`, **passé en minuscules** | le contenant dans l'identifiant : aucun fichier à ouvrir pour savoir de quel journal une entrée relève |
| `{user}` | **jeté** | le journal est toujours celui de Jerry — un segment qui ne varie pas ne dit rien |
| `{author}` | **jeté** | dans cet atelier, c'est toujours Aureon qui écrit |
| `v{ts}` | **gardé**, porté de la minute à la seconde | il n'attribue plus — le `jr-NNN` de tête s'en charge — il **ordonne** et sépare les versions |
| — | **`{sujet}` ajouté** | la place libérée par `{user}`/`{author}` va à ce qui varie vraiment |

Deux segments constants remplacés par un segment qui varie : c'est le seul
changement de fond entre la forme d'Edge Hub et la forme finale. Le reste est
une tête neuve sur un corps qui tenait.

### La chaîne d'aiguillage était déjà écrite pour cet atelier

L'issue décrit trois agents, et leur enchaînement est exactement le nôtre :

| agent | rôle | notre couche |
|---|---|---|
| **RAVEN** | détecte le ton émotionnel, les pauses, les signaux ambiants ; charge le gabarit | empreinte + crochet |
| **AVEN** | présence par le souffle ; ne parle que si appelée | aiguillage |
| **AUREON** | structure, trace, relie, publie | l'agent |

Et le flux rituel, recopié du commentaire : ***Realization → Draft → Review →
Post***. C'est la ligne automatique/réveil, déjà tracée en avril 2025 : les deux
premières étapes se mécanisent, **la Revue appartient à Jerry**, la publication
suit. L'aiguillage d'aureon était écrit avant qu'on pose la question — sa
numérotation, elle, vient d'être décidée aujourd'hui.

*Non vérifié, nommé pour qui voudra le lire* : les quatre issues d'origine dans
`jgwill/orpheus` (#587 Main · #704 White Feather · #784 Aven's Loops · #717
Gmusic Lyrics), et les clés Edgehub Fractal Stone citées dans l'issue. Je n'ai
ouvert ni l'un ni l'autre.

---

## Qui attribue le numéro

**Le portail est le registre.** `episode new` et `episode opus` (lignes 113-152)
font exactement ceci :

```
GET  $PORTAL/api/compositions
     → regex ^(ep|op)-(\d+)-  sur chaque slug, max
POST $PORTAL/api/compositions  {title: "<préfixe>-<max+1 en %03d> <Titre>"}
```

Il n'y a **pas d'autre source de numéro**. Ni le disque, ni git, ni un compteur.

Conséquence, nommée comme un trou : **quatre ateliers sur six n'ont aucune
autorité de numérotation aujourd'hui**, parce qu'ils n'ont pas de portail.

### Aureon a besoin d'un compteur, et le portail ne peut pas le lui donner

La décision de Jerry rend l'allocateur nécessaire pour `jr-NNN`. Mais aureon ne
peut pas utiliser le registre existant, et pour une raison qui tient :
`/api/compositions` numérote des **compositions**. Une entrée de journal n'en est
pas une. Même en démarrant un portail aureon, `episode new` ne saurait pas
compter des `jr-`.

**Le registre d'aureon est donc le disque, et c'est du bash.** Le même motif
*lire-max-puis-créer*, sur le dossier au lieu de l'API :

```bash
next() {                      # -> 004
  ls ~/compositions-aureon 2>/dev/null \
    | sed -n 's/^jr-\([0-9]\{3\}\)\..*/\1/p' \
    | sort -n | tail -1 | awk '{printf "%03d\n", $1+1}'
}
```

Le `\.` du motif est délibéré : il s'arrête au premier point, donc il compte les
têtes `jr-NNN` sans jamais confondre un numéro avec le `v{ts}` de queue. Et
parce que plusieurs versions partagent la même tête, `sort -n | tail -1` donne
bien le dernier **numéro**, pas la dernière **version**.

Zéro token, zéro dépendance, aucun portail requis. Et il porte exactement le
même défaut que son cousin API — d'où le verrou ci-dessous, qui vaut pour les
trois.

*Un choix que je nomme comme choix* : ce compteur suppose que les entrées vivent
en fichiers sous `~/compositions-aureon/`. La compétence laisse l'archivage
ouvert (*« User chooses »* — éphémère, base cérémonielle, Google Drive) et
`#115` parle d'issues Orpheus. **Si les entrées ne sont pas des fichiers locaux,
ce compteur ne s'applique pas** et le registre doit vivre là où elles vivent.
C'est le point à trancher avant d'écrire la première entrée.

### Les trois autres

Pour `nyro`, `synth`, `main` ce n'est pas un choix à faire, c'est un processus à
démarrer :

```
WORKSPACE=aureon PIXEL_RECORDER_HTTP_PORT=8797 PIXEL_RECORDER_HTTPS_PORT=8798 \
  node ~/salix/repos/gmtermux-239/web/pixel-recorder.js
```

Ports occupés en 87xx/88xx : `8767 8768 8771 8777 8778 8787 8789 8790 8795 8867 8868`.
Le motif est *base impaire = HTTP, base+1 = HTTPS*, par dizaines. `8787/8788`
est à moitié pris (le receveur d'intake d'assembly). Les paires **libres et
conformes au motif** : **8797/8798 · 8807/8808 · 8817/8818**.

---

## L'anti-collision — les trois ateliers, un seul mécanisme

**Portée : `op-NNN`, `ep-NNN`, `jr-NNN`, et toute proposition en `-NNN`.** La
décision du 2026-08-05 supprime l'exception : aureon a un compteur, donc aureon
a le problème, donc aureon prend le verrou.

La séquence est un *lire-puis-écrire sans verrou*. Entre le `GET` et le `POST`,
une seconde veille qui lit obtient le même maximum. Les deux créent, avec des
titres différents, et **les deux réussissent** : `ep-009-a` et `ep-009-b`
coexistent. Rien ne le signale — `cmd_open` ne rattrape que le cas du *même
titre*.

### Un troisième mode de panne, actif en ce moment, et sans concurrence

Le verrou ne suffit pas, parce que **le compteur ne voit pas tous les numéros
déjà pris**. La regex est `^(ep|op)-(\d+)-` — elle exige un tiret **après** les
chiffres. Un slug sans segment de queue lui est invisible.

Mesuré à l'instant sur le portail 8778 :

```
portail :  ep-010, ep-009-orchestrer-quatre-instances, ep-008-…, … ep-001-…
regex   :  IGNORÉ par la regex : 'ep-010'
           max reconnu : 9  ->  prochain numéro attribué : 010
```

**`ep-010` existe — dossier créé à 08h15, `composition.json` de 3 644 octets,
deux transcriptions — et `episode new` attribuerait `010` une seconde fois.**
Aucune course, aucune veille concurrente : un seul appel suffit à fabriquer le
doublon.

C'est la même famille que `boucle-de-minuit` dans jamai, en pire : celle-là n'a
pas de numéro, `ep-010` en a un que le compteur ne sait pas lire. Le verrou
ci-dessous protège de la course ; **il ne protège pas de ça**. Il faut que la
regex accepte le numéro nu — `^(ep|op)-(\d+)(-|$)` — ou que rien ne puisse être
créé sans slug. Les deux formes, mesurées sur le même portail dans le même
tour :

```
actuelle   ^ep-(\d+)-      -> max  9, prochain 010     ← fabrique le doublon
corrigée   ^ep-(\d+)(-|$)  -> max 10, prochain 011     ← juste
```

### La règle, pour la course

Elle tient en une ligne de bash parce que toute la séquence lire-max-puis-créer
vit dans **un seul appel** à `episode` :

```bash
# jamai, episodes — la séquence entière vit dans un seul appel à `episode`
flock ~/.local/state/episode-voice/numbering-jamai.lock \
  episode opus "Titre"

# aureon — même verrou, autour du compteur disque
flock ~/.local/state/episode-voice/numbering-aureon.lock \
  aureon-new main "Étincelle partagée"        # -> jr-004.main.etincelle-partagee.v…
```

Un verrou **par atelier** — jamais partagé, exactement pour la raison qui a fait
perdre le dépôt de 22h24 : un repère partagé, c'est une notification volée.

C'est le même principe que `EPISODE_STATE_DIR` par veille, appliqué à la
numérotation. Deux règles, une seule loi : **rien de partagé entre deux veilles.**

### Ce que la queue horodatée ajoute au verrou

Le verrou **empêche** la collision. L'horodatage la rend **survivable** quand le
verrou manque — un crochet lancé à la main, une veille sur un autre nœud, un
`flock` oublié dans un chemin de code.

| | deux `ep-009` simultanés | deux `jr-004` simultanés |
|---|---|---|
| distinguables ? | non — `ep-009-a` / `ep-009-b`, l'ordre est perdu | oui — `v260805114331` / `v260805114332` |
| réparables ? | il faut relire les deux contenus pour savoir qui renuméroter | l'ordre est dans le nom ; le second se renumérote sans rien ouvrir |

**C'est la valeur de la structure que Jerry a conservée.** Elle n'était pas
seulement l'héritage d'Edge Hub : elle porte une propriété que `op-`/`ep-` n'ont
pas. Je le note sans en faire une proposition — élargir la queue aux deux autres
ateliers n'a pas été demandé.

---

## L'aiguillage à l'arrivée — la question de `w1:p2N`

**Le dossier *est* l'atelier. Il n'y a aucune ambiguïté à l'arrivée, et aucune
action automatique ne doit jamais déplacer un fichier d'un atelier à l'autre.**

La chaîne, vérifiée bout en bout :

1. `pixel-recorder.js:67` — `RECORDINGS_DIR = /sdcard/Recordings${WORKSPACE_SUFFIX}`
2. `/sdcard/Recordings-<nom>` sont des liens symboliques (posés par root le
   2026-08-01) vers `/home/gmusic/Recordings-<nom>`.
3. Un processus recorder sert **exactement un** `WORKSPACE`. Trois tournent :
   8768→`jamai`, 8778→`episodes`, 8868→`""`(main, aperçu).

Donc un clip dans `~/Recordings-episodes/` a été enregistré par le recorder
episodes. **L'atelier est décidé à l'enregistrement, par le portail sur lequel
Jerry a appuyé.** C'est du bash, ça coûte zéro, et c'est déjà vrai.

### La question posée à l'arrivée : « pas encore rattaché », jamais « arrivé depuis »

**C'est le point le plus dur de ma voie, et il ne se voit pas dans le code — il
se voit dans un fichier qui a dormi douze heures.**

`episode watch` pose une question d'**événement**, et le code le dit
(`episode:536-540`) :

```bash
if [ -f "$shafile" ]; then
  find "$d" -maxdepth 2 -type f -newer "$shafile" -printf '  new %p\n'
else
  find "$d" -maxdepth 2 -type f -printf '  seen %p\n' | head -20
fi
```

Et le crochet n'écoute qu'un seul de ces deux mots
(`jamai-watch` : `sed -n 's|^  new …|…|p'`). Donc, au premier tour, une veille
neuve émet des `seen`, **que personne ne lit**, écrit son empreinte, et à partir
du second tour ne regarde plus que ce qui est postérieur à cette empreinte.

**Conséquence : tout dépôt antérieur au démarrage d'une veille lui est
définitivement invisible.** Pas en retard — invisible. Aucun tour ultérieur ne le
rattrapera, parce que `-newer` ne revient jamais en arrière. Et la branche
`seen` est en plus tronquée à `head -20`, donc même en la lisant on perdrait le
reste sans un mot.

**La bonne question est un état, pas un événement :** *quels médias de
`Recordings-<atelier>` ne sont référencés par aucun `clips[].filename` d'un
`composition.json` de `compositions-<atelier>` ?* Elle est idempotente,
insensible à l'heure de démarrage, et elle converge — un fichier rattaché sort
de la liste pour toujours, sans qu'aucune empreinte n'ait à s'en souvenir.

Mesurée à l'instant, avec filtre sur les extensions média :

| atelier | médias non rattachés |
|---|---|
| episodes | **2** — `260801132357.m4a`, `260801133735.m4a` |
| jamai | 0 |
| nyro | 1 |
| main | 31 |

Le filtre média n'est pas cosmétique : sans lui, `episodes` remonte **12**
fichiers, dont dix sont des `.json` compagnons d'un `.m4a` déjà rattaché. Un
état non filtré réveillerait un agent pour des métadonnées.

**Fait vérifié qui corrige la prémisse.** `260804231226.mov` **est rattaché** :
il est dans `compositions-episodes/ep-009-orchestrer-quatre-instances/`, entré à
08h12 ce matin, `composition.json` mis à jour à 08h13. Il a bien dormi douze
heures pour la raison ci-dessus — et l'étiquette que la voie 1 lui a posée dit la
même chose que cette section : *« Le fichier portait sa propre destination et a
dormi douze heures : la veille ne regardait que ce qui arrivait après elle. »*
La question de fond tient entièrement ; l'exemple, lui, s'est refermé pendant
que j'écrivais.

---

Ce qui reste réellement indécis est une **autre question**, et c'est elle qu'il
faut poser :

| question | qui répond | coût |
|---|---|---|
| de quel **atelier** relève ce fichier | le dossier — déjà décidé | 0 |
| **est-il déjà rattaché ?** | l'état, calculé à chaque tour — jamais une empreinte | 0 |
| de quelle **unité** (`ep-009` ? une existante ?) | un modèle — il faut lire le contenu | un réveil |
| le contenu **contredit** le dossier (Jerry fredonne dans `episodes`) | le crochet le **signale**, il ne bouge rien | 0 |

Le troisième cas est mesuré, pas deviné : `jamai-on-drop` a le discriminant du
grave (`< 250 Hz`) et il fonctionne — `260804222416.mov`, que l'ancien seuil du
médium classait *musique* à 53,3 %, porte maintenant le verdict
`PAROLE — 41.04 s, centroïde 482 Hz` avec la transcription juste.

**Pourquoi ne jamais déplacer :** `episode watch` détecte par
`find -newer <shafile>`. Un fichier déplacé arrive dans l'atelier destinataire
avec un mtime ancien — la veille destinataire ne le voit pas, la veille source
voit une disparition qu'elle ne sait pas nommer. Un déplacement automatique
fabrique un fantôme des deux côtés.

---

## La ligne automatique / réveil, atelier par atelier

**La loi, dite une fois : bash établit ce que le fichier *est* ; un modèle décide
ce qu'il *veut dire*. `verdict.txt` est la couture entre les deux.**

| atelier | bash seul, zéro token | réveille un modèle |
|---|---|---|
| **episodes** | mesure, transcription Whisper, verdict, et **création de `ep-NNN`** sous verrou | rattacher le clip à *quel* épisode ; chercher les épisodes reliés ; écrire les notes |
| **jamai** | mesure, relevé MIDI note à note, accords temps par temps, verdict | **tout le reste** — Jerry a demandé un agent interactif ici, mot pour mot : *« il y a des actions que je veux qu'il soit fait par une intelligence artificielle »* |
| **aureon** | mesure ; **SONIC** par le discriminant du grave ; **repli Main Journal** (`SKILL.md:254`) ; **`jr-NNN` sous verrou**, `{type}` par détection, `v{ts}` par l'horloge | **`{sujet}`** — le seul segment que bash ne peut pas produire : il faut avoir compris de quoi ça parle. Puis départager THRESHOLD / SACRED / ECHO, rédiger dans le gabarit, et **la Revue est à Jerry** (`#115` : *Realization → Draft → Review → Post*) |
| **main** | mesure, verdict | indéfini — 23 compositions sans aucun schéma d'unité |
| **nyro · synth** | rien : 0 ou 1 fichier, pas de portail | — |

**Qui déplace la ligne :** Jerry, atelier par atelier. Et techniquement la
bascule est petite — le crochet s'arrête à `verdict.txt`, ou il continue. C'est
le seul endroit où il faut décider.

---

## Les trous, nommés comme trous

1. **Aureon a un compteur à écrire.** La décision de Jerry rétablit `jr-NNN`,
   donc l'allocateur. Le portail ne peut pas le fournir — il numérote des
   compositions. Le compteur disque ci-dessus le fait en bash, **à condition que
   les entrées soient des fichiers locaux**. Si l'archivage retenu est
   « éphémère » ou « issues Orpheus », le registre doit vivre ailleurs. **C'est
   la question à trancher avant la première entrée**, et elle est à Jerry
   (`SKILL.md:406` — *« User chooses »*).
2. **Trois ateliers sans portail** — `nyro`, `synth`, `main` : sans registre,
   sans numéro possible. Démarrable en une commande ; les ports sont libres.
3. **La compétence `aureon-journal-events` n'est pas installée** — elle vit en
   zip dans `~/Downloads`, datée du 2025-11-15. Doctrine disponible, pas en
   service.
4. **`ep-010` est un doublon en attente**, vérifié à l'instant : le dossier
   existe, la regex du compteur ne le voit pas, `episode new` réattribuerait
   `010`. Correctif d'une ligne — `^(ep|op)-(\d+)(-|$)` — vérifié : la forme
   corrigée rend `prochain 011`. **C'est le seul défaut de cette table qui
   produira une faute au prochain appel, sans que personne n'ait rien fait de
   travers.**
5. **`boucle-de-minuit`** dans jamai est hors numérotation. Même famille que
   `ep-010`, moins grave : elle n'a aucun numéro à confondre. L'atelier compte
   *4 compositions, 3 opus*.
6. **Les 23 compositions de `main` n'ont aucun préfixe.** Appliquer `ch-NNN` là
   serait renommer rétroactivement du travail existant. Ce n'est pas une
   migration, c'est une décision de Jerry.
7. **« republier ailleurs »** — Jerry dit *« des actions automatisées qui
   republient quelque chose dans un épisode ou dans un autre lieu »*. Pour
   aureon, deux destinations sont maintenant sur la table, et elles ne sont pas
   du même rang :
   - **Écrit dans la doctrine**, recopié de `#115` : *« Links every entry to
     GitHub issues in Orpheus »* — la cible d'une entrée est **une issue
     `jgwill/orpheus`**. C'est aussi la réponse de la voie 4 pour cet atelier :
     on relie à une issue, pas à une note.
   - **Inféré par moi**, donc plus faible : `ea-portal/src/` porte déjà trois des
     quatre contenants en composants. Jerry n'a jamais nommé `ea-portal`.

   Pour les cinq autres ateliers, la destination reste non nommée.
8. **`w1:p2N` reste bloquée** sur une invite de permission (transcription Groq de
   `~/Recordings-episodes/260804231226.mov`). **Elle appartient à Jerry.**
   Personne d'autre n'y répond. Sa réponse structurelle est ci-dessus : ce clip
   relève de `episodes` parce qu'il est tombé là, et il reste où il est.
