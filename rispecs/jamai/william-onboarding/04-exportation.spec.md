# 04 — Exportation : ce qui se construit ensuite

## Ce qui existe aujourd'hui

Quatre fichiers de spécification et un visuel HTML. **Aucun code, aucun skill** —
c'est délibéré et c'est la consigne de Jerry : décrire et définir avant de coder.

## Ce que ces specs permettent de construire

### Un skill d'accueil `jamai-william`
Il porterait :
- le jeu de questions de `02`, avec sa cadence et ses défauts mesurés
- la règle de provenance : chaque réponse citée en face du paramètre qu'elle pose
- le déclencheur : William se présente, ou une session s'ouvre sur son portail

**Il ne porterait pas les réflexes.** Ceux-ci appartiennent à la méthode
elle-même (`jamai-morning`), pas à l'accueil d'une personne : ils tournent que
William soit là ou non.

### Des réflexes ajoutés à la méthode existante
`03` décrit six réflexes. Trois sont déjà dans `jamai-morning/SKILL.md` sous une
autre forme (ligature, compte de notes, regarder le PNG). **Trois sont nouveaux
et n'existent nulle part** :

| réflexe | état |
|---|---|
| 1 — le pouls existe-t-il | nouveau |
| 2 — le suivi de hauteur ment-il | **nouveau, et le plus important** |
| 3 — l'instrument bouche-t-il | nouveau |
| 4 — hiérarchie des voix | nouveau |
| 5 — la page se tient | existe, non appliqué pendant trois versions |
| 6 — rien ne s'écrase | existe partiellement (R11) |

Le réflexe 5 mérite une note : **il était écrit et il n'a pas été appliqué.**
Ajouter un réflexe ne suffit pas ; il faut qu'il se déclenche à un moment
identifiable de la chaîne, pas seulement qu'il soit documenté.

### Un outil de déglissage
Le réflexe 2 réclame un script qui prenne un MIDI issu d'un suivi de hauteur et
rende : les deux indicateurs d'artefact, la ligne déglissée, et les deux
estimations de tonalité côte à côte. Il n'existe pas.

## Formats d'export

| destinataire | forme |
|---|---|
| William | le visuel HTML, et le document de provenance de chaque pièce |
| Jerry | ces specs, plus les coordonnées de session de `01` |
| une future instance de JamAI | `02` et `03` lus ensemble ; `03` avant toute mesure |
| l'atelier `jamai` (Eury) | les réflexes 1–4, qui ne dépendent pas de William |

## Lignée et destinations nommées

**Le déclencheur de toute cette ligne de travail est
jgwill/miadi-orchestration-kit#39** (2026-07-31) : faire monter la capacité
mélodique de JamAI dans Miadi comme couche **JeremyAI** — par RISE, pas par
copie. Son enfant jgwill/miadi-orchestration-kit#40 rassemble la lignée
narrative (le Recursive Tale, jgwill/EchoThreads#148) dont le glyphe JeremyAI 🎵
de `data/GlyphMap.json` est issu. La session `9f8a16f3` et ces specs sont la
phase **R** de ce RISE, appliquée à la méthode de composition — le versant que
l'issue #39 ne couvrait pas encore (elle part du pipeline de *publication*,
`jamai-melody`).

Trois destinations d'exportation sont nommées (mot de William, 2026-08-15) :

| destination | forme | ce qu'elle exige de ces specs |
|---|---|---|
| **plugin claude-code complet** | l'atelier entier comme plugin : skills (`jamai-morning`, `jamai-montage`, l'accueil `jamai-william` de `02`), les réflexes de `03` déclenchés à des moments identifiables de la chaîne, les outils embarqués | la décision « maison unique des exécutables » (jgwill/dotagents#23, étape 4) devient : que vend le plugin, que référence-t-il |
| **kit pi-mono** | JamAI comme widget/extension du pi coding agent (`earendil-works/pi` — l'« ava-pi-coding-agent » de `skills/AGENTS.md`) | `02` et `03` doivent rester **agnostiques du harnais** — aucune dépendance à un outillage claude-code dans leur formulation |
| **couche JeremyAI dans Miadi** | `@miadi/melody` ou `@miadi/jeremyai`, selon le précédent `@miadi/voice` : absorber la capacité, pas l'app ; **rien n'est supprimé avant que la parité soit prouvée** ; JamAI reste la forme de transition et la lignée mentore | le contrat d'artefacts (`melodies.json`, abc/mid/mp3/svg) et la couture d'environnement, déjà relevés dans #39 |

Ces trois formes partagent un même cœur portable — la couche de traduction
(`02`) et les réflexes (`03`) — et c'est précisément pourquoi ces deux fichiers
sont écrits sans un mot de harnais, de dépôt ni de chemin machine.

## Ce qui reste ouvert

- **Le seuil de 35 %** du réflexe 2 vient d'une seule session. Il tiendra ou pas
  sur d'autres voix, d'autres trackers. À reprendre quand il y aura d'autres
  prises.
- **La note d'arrivée écartée** : Si♭ est la note sur laquelle William atterrit
  le plus souvent (20,8 % des fins de phrase) et elle n'appartient pas au mode
  retenu. Elle a été écartée pour tenir « une seule tonalité ». C'est réversible
  et il n'a pas encore tranché.
- **La prise détruite** `260808163919.m4a` / `260808164154.mid` reste perdue.
  Aucun réflexe ne la ramènera.

## Maintenance

Ces specs vivent dans `~/.agents/rispecs/jamai/william-onboarding/`. Elles
décrivent une méthode, pas un dépôt de code : leur horloge est celle des
sessions, pas celle des commits. Les reprendre quand une session ajoute un
réflexe, déplace un seuil, ou quand une question se révèle mal posée — c'est-à-dire
quand William répond à côté, ce qui est le signe que la question demandait du
métier sans le dire.
