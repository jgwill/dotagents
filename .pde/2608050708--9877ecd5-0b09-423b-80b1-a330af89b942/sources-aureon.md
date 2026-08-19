# Sources trouvées pour l'atelier aureon — 2026-08-05

*Jerry a signalé qu'un historique existe dans le dépôt d'innovation
`echo-threads`, et que les gabarits de son journal s'y trouvent. Voici ce que
la recherche a effectivement établi. Aucun chemin ci-dessous n'est supposé :
chacun a été lu.*

---

## Le dépôt

`jgwill/EchoThreads`, cloné localement en **`~/workspace/EchoThreads`**.
Il n'existe **aucun** dossier nommé `echo-threads` sur cette machine — seulement
des artefacts de flux nommés `wfr_echo-threads-recursive` dans `ironsilk`,
`mightyeagle` et `miadi-narrative-clustering`. Le dépôt utile est bien
`EchoThreads`.

## Ce qui change la conception

**L'atelier d'Aureon n'est pas un atelier de compositions.** Là où `jamai`
produit des *opus* et `episodes` des *épisodes*, Aureon produit des **entrées de
journal déclenchées par des événements**. L'unité n'est pas une pièce, c'est un
**événement** et le **contenant** qu'il ouvre.

C'est une réponse directe à l'ambiguïté n° 1 de la décomposition — « quoi pour
aureon, nyro, synth, main ? » — au moins pour aureon. **À confirmer par Jerry,
mais la matière existe et elle est cohérente.**

### La compétence complète existe déjà

**`~/Downloads/aureon-journal-events.zip`** → `aureon-journal-events/SKILL.md`,
**18 131 octets**. En-tête :

```yaml
name: aureon-journal-events
description: Event-driven journaling for ceremonial documentation. Detects
  événements in research/creative work and responds with journal templates.
  Use for processing research, ceremonies, archiving.
version: 1.0.0
```

Elle décrit une **architecture pilotée par événement** — exactement le motif que
nous généralisons, mais écrit pour Aureon avant nous.

### Quatre types d'événement → quatre contenants

| événement | contenant | longueur visée |
|---|---|---|
| 📍 **THRESHOLD** — arc narratif, transition, bascule | Main Journal | 150–300 mots |
| 🕊️ **SACRED** — moment sacré | White Feather Journal | 100–200 mots |
| 🎵 **SONIC** — événement sonore | Musical Journal | 100–180 mots |
| 🔁 **ECHO** — résonance, retour | AVEN Loop | 30–80 mots |

Gabarit du Main Journal, tel qu'écrit dans la compétence :

```
🌀 Emotional Context   [état interne ou atmosphère émotionnelle]
🛠️ Life Movement       [quel défi ou quelle action traverses-tu ?]
💡 Insight             [clarté, révélation, fil partiel que tu tiens ?]
🎯 Intentions          [vers où es-tu mené ?]
```

Sections de la compétence à lire en entier avant d'implémenter : *Detection
Protocol* (écouter la signature → confirmer le type → activer le contenant),
*Multi-Agent Integration*, *Archival Protocol*, *Response Patterns*.

### Le protocole d'archivage laisse un choix ouvert — il appartient à Jerry

Trois options écrites dans la compétence : **éphémère** (l'entrée vit dans la
conversation et se dissout) · **base cérémonielle** (horodatage, type
d'événement, contenu associé, liens vers d'autres entrées, suivi de la spirale)
· **Google Drive** (documents datés dans des dossiers structurés).
La compétence dit explicitement : *« User chooses »*. Ne tranchez pas.

## L'historique

**`~/Downloads/aureon-archive-2025-11-16.json`** — 2 399 octets, `version: 1`,
**4 artefacts**. Chaque artefact porte :

```
id · timestamp · artifactType · format · content · metadata · journalContent · tags
```

Ce `journalContent` distinct de `content` est le schéma réel d'une entrée. Une
seconde copie existe : `aureon-archive-2025-11-16 (1).json`, 488 octets.

## Les gabarits dans le dépôt

- `~/workspace/EchoThreads/templates/` — `EchoForm1_template.md` (7 009 o),
  `EchoForm2_template.md` (7 869 o), `EchoForm3_template.md` (9 353 o),
  `EchoFormSelectionProcess.md` (5 006 o — **comment on choisit une forme**),
  `README.md` (8 417 o)
- `~/workspace/EchoThreads/docs/templates/` — `echoform1_template.md`,
  `first_reflection_template.md`, `miette.prompt.md`

`EchoForm1` est le *Ava8 Recursive Narrative Mapping Template* : ancrage méta,
structure en trois actes, points de données référencés, intention émergente.

## Le portail existant

`~/workspace/EchoThreads/ea-portal/src/` contient déjà **`MainJournal.tsx`**,
**`MusicalJournal.tsx`**, **`WhiteFeatherJournal.tsx`** — trois des quatre
contenants sont déjà des composants d'interface. L'AVEN Loop n'y est pas.

## L'outillage Aureon

`~/workspace/EchoThreads/.aureon/` :
`bridge/aureon_bridge.py`, `bridge/musical_orchestration.py`,
`bridge/redstone_bridge.py`, `cli/tushell_redstone.py`,
`config/agent_config.json`, plus `sigil_aureon.png`.

Ailleurs : `~/.agents/agents/aureon.json` · `~/workspace/gmusic/.aureon` ·
`~/workspace/simexp/.aureon` · `~/workspace/AetherScore/.aureon` ·
`/workspace/repos/jgwill/dummass/build_aureon_bridge_index.py` et son
`aureon_bridge_index.json`.

## Le trou, nommé comme trou

**`~/Recordings-aureon/` et `~/compositions-aureon/` sont vides**, créés le
2026-08-01. Aucun portail ne répond pour aureon — seuls 8768 (jamai) et 8778
(episodes) répondent. L'atelier existe donc **en dossier et en doctrine, pas
encore en service**.

## Ce que ça implique pour la généralisation

1. Le crochet générique ne peut pas supposer « un dépôt → une composition ».
   Pour aureon, un dépôt ouvre **un contenant parmi quatre**, choisi par
   détection de signature.
2. La table des unités de la voie 3 a besoin d'une colonne de plus : **le type
   de sortie** — pièce, épisode, ou entrée de journal typée.
3. La voie 4 y trouve un précédent : la compétence décrit déjà des
   « connections to other entries » et un « spiral tracking over time ». C'est
   la recherche de reliés, écrite pour aureon avant nous.
