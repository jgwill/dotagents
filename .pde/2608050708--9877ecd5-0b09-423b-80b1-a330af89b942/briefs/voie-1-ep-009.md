# Voie 1 — la chaîne episodes, prête au réveil de Jerry

**Tu portes l'échéance.** Jerry dépose une vidéo dans l'atelier `episodes` à son
réveil et attend qu'une veille la traite, la range dans **ep-009**, et cherche
les épisodes reliés à ce qu'il y dit.

## État vérifié

L'atelier `episodes` (portail 8778) contient huit compositions :
ep-001 artifact-container-vision (0 clips) · ep-002 gmtermux-141-r2-sync-explained (1) ·
ep-003 dotagents-1-episode-voice-channel-skill (4) · ep-004 deux-ateliers-un-seul-jerry (6) ·
ep-005 worktree-territory-map (15) · ep-006 capture-musicale (1) ·
ep-007 ce-que-coute-une-boucle (0) · ep-008 error-share-json (0).
**ep-009 est libre.**

## État désiré

Une vidéo tombe dans `~/Recordings-episodes/`. Sans qu'un modèle soit réveillé :
elle est mesurée, transcrite, classée, rangée ; `ep-009` est créé ou complété ;
la recherche d'épisodes reliés est lancée ; et **un agent n'est réveillé que
s'il reste un jugement à porter**.

## Étapes

1. Lis la décomposition, puis les trois panneaux en vol.
2. Rejoue la chaîne jamai de bout en bout sur un dépôt existant d'`episodes`
   pour voir où elle casse — `episode watch episodes` a-t-il déjà un repère,
   le crochet sait-il parler au portail 8778.
3. Câble : dépôt → mesure → transcription → `ep-009` → recherche reliée →
   `links[]`. Chaque maillon vérifié séparément.
4. Répète un vrai dépôt de bout en bout et **lis l'ep-009 produit**.
5. Écris ce qui tourne au réveil, ce qui est reporté, et ce qui reste à Jerry.

## Tension

Entre une chaîne éprouvée sur un seul atelier et une échéance sur un autre,
sans savoir l'heure du réveil. Livre d'abord le chemin le plus court qui marche
vraiment ; le générique est la voie 2.

## Ce qui appartient à Jerry — ne tranche pas seul

- L'analyse « pour voir s'il n'y a pas d'autres épisodes relatifs » n'est
  nommée que comme « une action quelconque ». Coordonne-toi avec la voie 4.
- Un dépôt mal rangé : le déplace-t-on ou le référence-t-on seulement ?

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
