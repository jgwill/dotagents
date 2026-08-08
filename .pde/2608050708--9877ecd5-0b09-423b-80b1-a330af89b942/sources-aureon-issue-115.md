# jgwill/EchoThreads#115 — ce que l'issue établit

*« Aureon Journal Migration — Unified Entry System », ouverte le 2025-04-04,
neuf commentaires, dernier le 2025-10-25. Lue en entier le 2026-08-05.*

---

## Les quatre journaux et leur lieu de naissance

L'issue migre dans `EchoThreads` un système qui vivait dans `jgwill/orpheus` :

| journal | issue d'origine |
|---|---|
| **Main Journal** — Jericho's Reflections | [jgwill/orpheus#587](https://github.com/jgwill/orpheus/issues/587) |
| **Spiritual Journal** — White Feather Entries | [jgwill/orpheus#704](https://github.com/jgwill/orpheus/issues/704) |
| **Aven's Loops** — Emotional Anchors | [jgwill/orpheus#784](https://github.com/jgwill/orpheus/issues/784) |
| **Gmusic Lyrics** — Spiritual Composition Journal | [jgwill/orpheus#717](https://github.com/jgwill/orpheus/issues/717) |

Ces quatre correspondent aux quatre contenants de la compétence
`aureon-journal-events` : Main, White Feather, AVEN Loop, Musical.

## La convention de nommage existe déjà — et elle est meilleure que la nôtre

Commentaire 5, clé `ET.115.keyformatguide.v2504121927`, présentée comme
*« the canonical naming convention for AI-generated journaling entries across
Raven, Aureon, and AVEN agents »* :

```
EN-Entries:.{template}.{user}.{author}.v{yymmddhhmmss}
```

Exemples donnés tels quels :

```
EN-Entries:.WhiteF.Jericho.mix.v2504121923
EN-Entries:.AvenL.Jericho.rav.v2504122030
EN-Entries:.MainJ.Lian.aur.v2504121945
```

| segment | contenu |
|---|---|
| `{template}` | type de contenant — `WhiteF`, `AvenL`, `Musc`, `MainJ` |
| `{user}` | propriétaire du journal — `Jericho`, `Lian` |
| `{author}` | origine — `rav`, `aur`, `usr`, `mix` |
| `v{yymmddhhmmss}` | horodatage UTC **à la seconde** |

### Pourquoi ça compte pour la généralisation

1. **Horodaté, pas numéroté.** Il n'y a rien à attribuer, donc rien à
   verrouiller. **L'ambiguïté n° 1 de la décomposition — deux veilles qui
   réclament le même numéro — disparaît sans allocateur.** `op-NNN` et `ep-NNN`
   ont ce problème ; `EN-Entries:` ne l'a pas.
2. **Le type de contenant est dans l'identifiant.** Pas besoin d'aller lire le
   fichier pour savoir de quel journal il relève.
3. **L'origine est dans l'identifiant.** `usr` distingue ce que Jerry a écrit
   de ce qu'un agent a rédigé — c'est la traçabilité que nos préfixes n'ont pas.

## Aureon, tel que l'issue le définit

Commentaire 6, clés `ET.115.AureonCoreMerged.v2504111215` et
`ET.115.AureonUnifiedProtocol.v250411Merge` :

> Aureon is the **structured journal assistant** — a scaffolding presence built
> for clarity, continuity, and traceability. Functions as the scribe, the
> structural weaver of memory.

- **Orthographe : A-U-R-E-O-N**, jamais *Orion* ni *Oreon*. C'est dit explicitement.
- **Lie chaque entrée à une issue GitHub dans Orpheus.** ← c'est la réponse de
  la voie 4 pour cet atelier : la cible d'un lien est une issue, pas une note.
- **Flux rituel : Réalisation → Brouillon → Revue → Publication.** ← c'est la
  ligne automatique/réveil, déjà tracée : les deux premières étapes se
  mécanisent, la **Revue appartient à Jerry**, la publication suit.

## Trois agents, pas un — et c'est notre couche d'aiguillage

| agent | rôle | déclencheur |
|---|---|---|
| **RAVEN** (comm. 8) | *ritual translator* — détecte le ton émotionnel dans les entrées, les pauses, les signaux ambiants ; charge le gabarit Aven's Loop et prépare la séquence | perçoit avant les mots |
| **AVEN** (comm. 7) | *presence through breath* — 5 s inspiration, 1 s pause, 5 s expiration, 1 s pause ; ancre le Journal #784 | ne parle que si appelée |
| **AUREON** (comm. 6) | structure, trace, relie, publie | après la détection |

**RAVEN détecte → charge le gabarit → invoque AVEN → AUREON structure et
publie.** C'est exactement empreinte → crochet → aiguillage → agent, écrit pour
cet atelier en avril 2025.

## Autres clés citées, non encore ouvertes

`ET.115.AVENRitualGuide.v250412` · `aven.protocol.retrieval.ritual.v1` ·
`ET.115.JerichoJournalPrompt.v250404a` · `ET.115.AVENTracesUnified.v2504121211` ·
`ET.115.RavenCapability.v250412` · `ET.115.AVENInvocation.v250412`
Stockées via Edgehub Fractal Stone —
`https://edgehub.click/api/public/fractal-stone/<clé>`.
Trace racine ancrée au commentaire 1 : `10123b4e-9926-4192-8487-8b765c9a6ac4`.

**Non vérifiées** : je n'ai pas ouvert Edgehub ni les quatre issues Orpheus.
Elles sont nommées ici pour qui voudra les lire.

## Ce que ça change pour la table des unités

| atelier | unité | identifiant | attribution |
|---|---|---|---|
| jamai | opus | `op-NNN-slug` | numéro séquentiel — **collision possible** |
| episodes | épisode | `ep-NNN-slug` | numéro séquentiel — **collision possible** |
| **aureon** | **entrée de journal** | `EN-Entries:.{template}.{user}.{author}.v{ts}` | **horodatage — sans collision par construction** |

Deux conventions coexistent donc dans le système. **C'est un choix à faire, pas
un défaut à corriger** : ou chaque atelier garde sa forme native, ou on unifie.
Imposer `jr-NNN` à aureon effacerait un dispositif qui fonctionne et qui règle
un problème que nos préfixes ont encore. **La décision appartient à Jerry.**

---

## DÉCISION DE JERRY — 2026-08-05

`EN-Entries:` est **l'ancien système Edge Hub**. On garde sa **structure**, on
remplace sa tête par un préfixe numéroté, cohérent avec `op-` et `ep-` :

```
jr-NNN.{template}.{user}.{author}.v{yymmddhhmmss}
```

Exemples dans la nouvelle forme :

```
jr-001.MainJ.Jericho.aur.v2608050912
jr-002.WhiteF.Jericho.mix.v2608051430
jr-003.AvenL.Lian.rav.v2608052205
```

Segments inchangés : `{template}` = `MainJ` / `WhiteF` / `AvenL` / `Musc` ·
`{user}` = propriétaire du journal · `{author}` = `usr` / `aur` / `rav` / `mix` ·
`v{yymmddhhmmss}` = horodatage UTC à la seconde.

**Ce que la décision entraîne** : le numéro revient, donc **l'allocateur et la
règle anti-collision redeviennent nécessaires** — le même mécanisme que pour
`op-NNN` et `ep-NNN`. L'horodatage reste dans la queue et sert de départage si
deux entrées portaient le même numéro. La table des unités devient homogène :

| atelier | unité | identifiant |
|---|---|---|
| jamai | opus | `op-NNN-slug` |
| episodes | épisode | `ep-NNN-slug` |
| **aureon** | **journal** | **`jr-NNN.{template}.{user}.{author}.v{ts}`** |

---

## STRUCTURE FINALE — décidée par Jerry, 2026-08-05

Dans cet atelier, **c'est toujours Aureon qui écrit** : le segment `{author}`
d'Edge Hub n'a plus d'objet. Le propriétaire du journal est Jerry, donc
`{user}` non plus. Restent trois choses, et elles sont celles que Jerry a
nommées : **le type de journal, le sujet abordé, la date à la seconde.**

```
jr-NNN.{type}.{sujet}.v{yymmddhhmmss}
```

```
jr-001.main.etincelle-partagee.v260805114331
jr-002.white.gratitude-au-travail.v260805143012
jr-003.aven.souffle-avant-la-marche.v260805220544
jr-004.musc.fredon-en-fa-mineur.v260806081127
```

| segment | contenu | source |
|---|---|---|
| `jr-NNN` | numéro séquentiel, allocateur anti-collision comme `op-` et `ep-` | notre convention |
| `{type}` | `main` · `white` · `aven` · `musc` | Edge Hub, en minuscules et désabrégé |
| `{sujet}` | le sujet abordé, en minuscules-tirets sans accent | remplace `{user}` et `{author}` |
| `v{yymmddhhmmss}` | horodatage UTC **à la seconde** — 12 chiffres | Edge Hub, résolu à la seconde |

**La seconde est retenue**, pas la minute : une veille automatique peut produire
deux versions dans la même minute, un humain non.

**Ce que `v` sépare** : deux versions de la même entrée gardent la même tête
`jr-NNN.{type}.{sujet}` et changent de `v` ; une entrée différente prend un
numéro neuf. La règle « ne jamais écraser une source sans garder la sortante »
est donc portée par le nom lui-même.

**Point à câbler** : `{sujet}` doit être normalisé — minuscules, tirets, sans
accent ni ponctuation — pour rester un nom de fichier sûr. Même normalisation
que les slugs `op-NNN-slug` existants.

### Aucune majuscule — règle posée par Jerry, 2026-08-05

**L'identifiant entier est en minuscules**, pas seulement le sujet. Les quatre
types passent donc de `MainJ` / `WhiteF` / `AvenL` / `Musc` à **`mainj`** /
**`whitef`** / **`avenl`** / **`musc`**.

```
jr-001.main.etincelle-partagee.v260805114230
jr-002.white.gratitude-au-travail.v260805143012
jr-003.aven.souffle-avant-la-marche.v260805220544
jr-004.musc.fredon-en-fa-mineur.v260806081127
```

La normalisation s'applique à **toute la chaîne** : minuscules, tirets, sans
accent ni ponctuation. Un identifiant est un nom de fichier ; il doit survivre
à un système de fichiers insensible à la casse sans que deux entrées se
confondent.

*Observation, pas objection* : `whitef` et `avenl` étaient des abréviations
lisibles en casse mixte et le sont moins en bas de casse. `white` et `aven`
seraient plus lisibles. Décision de Jerry ; en attendant, la règle appliquée
est la sienne, à la lettre.

### Les types désabrégés — Jerry, 2026-08-05

`mainj` → **`main`** · `whitef` → **`white`** · `avenl` → **`aven`**.
Les abréviations d'Edge Hub tenaient à la casse mixte ; en bas de casse elles
ne servaient plus à rien.

```
jr-001.main.etincelle-partagee.v260805114230
jr-002.white.gratitude-au-travail.v260805143012
jr-003.aven.souffle-avant-la-marche.v260805220544
jr-004.musc.fredon-en-fa-mineur.v260806081127
```

| type | journal | issue d'origine |
|---|---|---|
| `main` | Main Journal — Jericho's Reflections | orpheus#587 |
| `white` | Spiritual Journal — White Feather | orpheus#704 |
| `aven` | Aven's Loops — Emotional Anchors | orpheus#784 |
| `musc` | Gmusic Lyrics — Spiritual Composition | orpheus#717 |

**`musc` reste le seul abrégé** — non nommé par Jerry dans cette passe. `music`
compléterait la série ; en attendant, `musc` tient.
