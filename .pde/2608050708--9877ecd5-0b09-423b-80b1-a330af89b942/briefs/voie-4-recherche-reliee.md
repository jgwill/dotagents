# Voie 4 — trouver les épisodes reliés

**Tu portes la question ouverte de Jerry** : « une action quelconque d'analyse
pour voir s'il n'y a pas d'autres épisodes relatifs à ce que je dis dans le
vidéo ».

## État désiré

Étant donné la transcription d'un dépôt, produire les unités déjà existantes
qui parlent de la même chose — avec un lien vérifiable, pas une impression.

## Étapes

1. Recense les corpus candidats et **mesure-les** : QMD (`mcp__qmd__*` s'il est
   enregistré, sinon la voie de repli documentée), le manifeste des
   compositions de chaque portail, les transcriptions déjà écrites dans les
   dossiers de compositions.
2. Tranche : quel corpus, quel index, quel coût par recherche. Si le coût est
   nul en tokens de modèle, dis-le et montre-le.
3. Décide la forme de la sortie : une entrée dans `links[]`, une section, une
   note. **Coordonne-toi avec `w1:pM`**, qui a déjà établi que la migration de
   schéma « ne déplace rien : ajouter `kind`, `links[]`, `documents[]` ».
4. Éprouve sur un cas réel : prends la transcription d'un dépôt existant et
   vérifie que ce qui remonte est vraiment relié.

## Tension

Entre une demande volontairement vague — « une action quelconque » — et
l'exigence qu'un lien proposé soit vérifiable. Préfère une recherche étroite
et juste à une large et bavarde.

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
