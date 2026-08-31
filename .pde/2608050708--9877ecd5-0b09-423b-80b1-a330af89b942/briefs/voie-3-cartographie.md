# Voie 3 — la carte des ateliers

**Tu portes le vocabulaire.** Les deux autres voies dépendent de toi.

## État désiré

Une table, vérifiée atelier par atelier : nom de l'unité, préfixe, qui attribue
le numéro, règle anti-collision, portail, dossier de dépôt, et où passe la
ligne entre action automatique et réveil d'un agent.

## Ce qui est établi

`jamai` → **opus**, préfixe `op-NNN`. `episodes` → **épisode**, préfixe `ep-NNN`.
`main`, `aureon`, `nyro`, `synth` → **nom d'unité inconnu**.

## Étapes

1. Inventorie chaque atelier : ce que contient son dossier de compositions, si
   un portail répond, quel préfixe est déjà employé.
2. Propose un nom d'unité et un préfixe pour les quatre sans nom — **propose**,
   ils appartiennent à Jerry.
3. Établis l'attribution des numéros et la règle qui empêche deux veilles
   concurrentes de réclamer le même.
4. Trace la ligne automatique / réveil par atelier. Jerry veut un agent
   interactif pour `jamai` ; pour d'autres il évoque des actions automatisées
   qui republient ailleurs — la destination n'est pas dite.
5. Résous l'aiguillage à l'arrivée : un fichier tombe dans un dossier, comment
   sait-on de quel atelier il relève. **Lis d'abord `w1:p2N`, elle est coincée
   exactement là.**

## Tension

Entre six ateliers réels et un vocabulaire dont Jerry dit lui-même qu'il n'est
pas fixé — « tout dépendant comment qu'on appelle les lieux ».

## Avant tout — ce qui est déjà en vol

Trois sessions Claude travaillent déjà sur ce terrain. **Lis leur sortie récente
avant d'écrire une ligne** (`herdr pane read <id> --source recent --lines 60`).
Si l'une couvre ton sujet, **envoie-lui un message** — ne double jamais une voie :

- `w1:pM` — a **déjà produit l'étude de schéma** : « 14 des 23 compositions Main
  utilisent des accords, 0 des 4 épisodes » ; « la migration ne déplace rien :
  ajouter `kind`, `links[]`, `documents[]` ». Déposée dans `Gerico1007/dotagents#3`.
- `wQ:p1` — schéma des coûts de tokens, PR #20.
- `w1:p2N` — **bloquée sur une invite de permission qui appartient à Jerry**.
  Ne réponds pas à sa place. Sa question est la nôtre :
  « Identify which workspace the new clip belongs to ».

## Les deux défauts déjà payés — ne les refais pas

1. **Repère d'état partagé.** Deux veilles interrogeant le même
   `watch-<atelier>.sha` se volent la notification : la première consomme, la
   seconde voit « unchanged ». Un dépôt de Jerry a été avalé ainsi le
   2026-08-04 à 22h24. **Chaque veille exporte son propre `EPISODE_STATE_DIR`.**
2. **Seuil de classement parole/musique.** Le médium (250–1000 Hz) échoue : une
   consigne parlée est descendue à 53,3 %. Le discriminant fiable est le
   **grave** — parole 13,8 / 17,6 / 37,6 % sous 250 Hz, fredon 73,1 %.

## Posture

- **Ce qui coûte, c'est ce qui s'imprime.** Un tour de veille silencieux coûte
  zéro. Tout ce qui peut être du bash doit être du bash ; on ne réveille un
  modèle que pour ce qui demande un jugement.
- **Aucun fait non vérifié dans une sortie.** Chemin, numéro, empreinte,
  commit : chacun doit venir d'une commande lue dans le même tour.
- **Nommer un choix comme choix et un trou comme trou.**
- **Regarde la sortie, ne la suppose pas** — c'est ainsi que les deux défauts
  ci-dessus ont été trouvés.

## L'état vérifié le 2026-08-05

Six ateliers en paires `~/Recordings-<nom>` + `~/compositions-<nom>` :
`main`, `aureon`, `episodes`, `jamai`, `nyro`, `synth`.
Deux portails répondent : **8768 → jamai** (4 compositions) · **8778 → episodes** (8).

Outils de référence, éprouvés, dans `~/.agents/skills/jamai-morning/scripts/` :
`jamai-watch` (boucle, `--stop/--status/--once`), `jamai-on-drop` (crochet),
`jamai-midi.py`, `jamai-measure.py`, `jamai-chords.py`.
Le pilote de portail : `~/.agents/skills/episode-voice-channel/scripts/episode`.

**La décomposition complète est dans `~/.agents/.pde/2608050708--9877ecd5-.../`**
— lis `pde-*.md` (20 actions, 10 ambiguïtés) et `input-prompt.md` (la consigne
de Jerry mot pour mot) avant de commencer.
