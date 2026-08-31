# Généraliser le motif de veille de l'atelier jamai à tous les ateliers

*Consigne de Jerry ⚡, 2026-08-04 en fin de séance, transcrite et mise en forme
sans rien retirer de son intention. Les faits d'état sont vérifiés en date du
2026-08-05.*

---

## Ce qu'il demande, dans ses termes

> La session que nous faisons, elle est vraiment écœurante, je l'aime beaucoup.
> Et j'aimerais traduire ça dans tous les autres espaces de travail. […]
> J'aimerais que tu me lances une session Claude […] Tu vas avoir pour but de
> recréer un peu les scripts d'observation, d'état qu'on a fait pour JamAI,
> mais pour toutes les autres espaces de travail. […] Une nouvelle space herdr
> dans laquelle il va avoir plusieurs sessions Claude qui vont travailler sur
> la création de ces scripts-là pour toutes les espaces de travail du dépôt
> d'innovation gmtermux.
>
> On va pouvoir lancer des scripts qui va observer l'arrivée de contenu dans un
> dossier spécifique et qui va enclencher une suite d'actions d'observation de
> ce qui a été déposé, et l'observation de ce qui a été déposé va faire en
> sorte qu'une autre action va déclencher. Dans chacune des fenêtres, on va
> pouvoir choisir l'action à faire. Donc si on prend par exemple JamAI, il y a
> un agent interactif qui doit utiliser un moniteur parce qu'il y a des actions
> que je veux qu'il soit fait par une intelligence artificielle. Mais pour
> d'autres, ça pourrait être des actions automatisées qui republient quelque
> chose dans un épisode ou dans un autre lieu, tout dépendant comment qu'on
> appelle les lieux. Donc avec JamAI ce sont des opus, avec épisode ce sont des
> épisodes, et avec les autres ils auront un autre nom aussi.
>
> Le but, ce n'est pas de le faire ici, c'est vraiment de saisir l'idée ici en
> observant la session pour comprendre qu'est-ce qu'on a réussi à faire. Il y a
> comme des actions qui se font d'analyse du vidéo qui est déposé et qui crée
> un contenu pour générer d'autres contenus au fond. Donc c'est vraiment un
> processus extraordinaire qui ne coûte pas beaucoup de tokens.
>
> On va vouloir que ça commence par l'épisode. Actuellement on est rendu à
> **ep-009**. Moi je vais envoyer un vidéo dans la section épisodes quand je
> vais me réveiller demain. Puis je m'attends à ce qu'il y ait un moniteur qui
> traite ce vidéo-là, qu'il le mette à la bonne place dans les épisodes, et
> qui fasse une action quelconque d'analyse pour voir s'il n'y a pas d'autres
> épisodes relatifs à ce que je dis dans le vidéo.

---

## Le motif à généraliser, tel qu'il a réellement fonctionné

Construit dans la séance du 2026-08-03/04 sur l'atelier `jamai`. Quatre couches,
et le nerf de l'affaire est que **seul ce qui s'imprime coûte des tokens** :

| couche | outil réel | ce qu'elle fait | coût |
|---|---|---|---|
| 1. empreinte | `episode watch <atelier>` | somme de contrôle du dossier, jamais un inventaire ; recul progressif quand rien ne bouge | 0 |
| 2. crochet | `jamai-on-drop <fichier>` | mesure, transcrit, classe, range — bash + ffmpeg + python + Whisper | 0 token de modèle |
| 3. aiguillage | le `verdict.txt` du crochet | décide : action automatique, ou réveiller un agent | 0 |
| 4. agent | outil `Monitor` de la session | réveillé seulement quand il faut juger | ~0,17 $ par réveil |

Fichiers de référence, tous en place et éprouvés :

- `~/.agents/skills/jamai-morning/scripts/jamai-watch` — la boucle, avec
  `--stop` / `--status` / `--once`, journal, et un repère d'état **propre à
  chaque veille**
- `~/.agents/skills/jamai-morning/scripts/jamai-on-drop` — le crochet
- `~/.agents/skills/jamai-morning/scripts/jamai-midi.py` — parseur MIDI note à note
- `~/.agents/skills/jamai-morning/scripts/jamai-measure.py` — timbre, bandes, pouls
- `~/.agents/skills/jamai-morning/scripts/jamai-chords.py` — accords temps par temps
- `~/.agents/skills/episode-voice-channel/scripts/episode` — le pilote de portail

### Deux défauts payés cash, à ne pas refaire

1. **Le repère partagé.** Deux veilles interrogeant le même `watch-jamai.sha`
   se volent la notification : la première consomme le changement, la seconde
   voit « unchanged ». Un dépôt de Jerry a été avalé ainsi le 2026-08-04 à
   22h24. Corrigé par un `EPISODE_STATE_DIR` distinct par veille.
2. **Le seuil de classement.** Distinguer parole et musique par le médium
   (250–1000 Hz) échoue : une consigne parlée est descendue à 53,3 %. Le
   discriminant fiable est le **grave** — parole 13,8 / 17,6 / 37,6 % sous
   250 Hz, fredon 73,1 %.

---

## L'état vérifié le 2026-08-05

**Six ateliers sur disque**, en paires `~/Recordings-<nom>` + `~/compositions-<nom>` :
`main`, `aureon`, `episodes`, `jamai`, `nyro`, `synth`.

**Deux portails répondent** : `8768` → atelier `jamai`, 4 compositions ·
`8778` → atelier `episodes`, 8 compositions.

**L'atelier episodes contient** : ep-001 artifact-container-vision (0 clips) ·
ep-002 gmtermux-141-r2-sync-explained (1) · ep-003 dotagents-1-episode-voice-channel-skill (4) ·
ep-004 deux-ateliers-un-seul-jerry (6) · ep-005 worktree-territory-map (15) ·
ep-006 capture-musicale (1) · ep-007 ce-que-coute-une-boucle (0) ·
ep-008 error-share-json (0). **ep-009 est donc bien le prochain libre.**

**Trois sessions Claude sont déjà en vol sur ce terrain** — à lire avant tout
travail, jamais à doubler :

- `w1:pM` — a **déjà produit l'étude de schéma** : « 14 des 23 compositions Main
  utilisent des accords, 0 des 4 épisodes » ; « la migration ne déplace rien :
  ajouter `kind`, `links[]`, `documents[]` » ; déposée dans `Gerico1007/dotagents#3`.
- `wQ:p1` — schéma des coûts de tokens, PR #20, consigne en attente.
- `w1:p2N` — **bloquée sur une invite de permission**, sur exactement notre
  question : *« Identify which workspace the new clip belongs to »*. Cette
  invite appartient à Jerry ; personne d'autre n'y répond.

---

## Ce que la décomposition doit trancher

1. **L'unité et sa numérotation** par atelier — `op-NNN` pour jamai, `ep-NNN`
   pour episodes, et quoi pour `aureon`, `nyro`, `synth`, `main` ? Qui attribue
   le numéro, et comment on évite deux veilles qui réclament le même.
2. **L'aiguillage à l'arrivée** — un fichier tombe dans *un* dossier. Comment
   décide-t-on de quel atelier il relève, et faut-il le déplacer ? C'est
   précisément là que `w1:p2N` est coincée.
3. **La frontière automatique / réveil**, atelier par atelier. Jerry veut un
   agent interactif pour `jamai`. Pour les autres, il évoque des actions
   automatisées qui republient ailleurs. Où passe la ligne, et qui la déplace.
4. **« D'autres épisodes reliés »** — sur quel corpus cherche-t-on, avec quel
   index ? QMD, le manifeste des compositions, les transcriptions déjà écrites ?
   Et que produit-on : un lien dans `links[]`, une section, une note ?
5. **La généralisation des outils** — `jamai-watch` et `jamai-on-drop` sont
   nommés et câblés pour un seul atelier. Faut-il un `atelier-watch <nom>`
   paramétré, un crochet par atelier, ou un crochet commun avec des règles ?
6. **La cible concrète de demain matin** : Jerry dépose une vidéo dans
   `episodes`. La chaîne doit la ranger dans `ep-009` et chercher les épisodes
   reliés à ce qu'il y dit. Qu'est-ce qui est indispensable pour que ça marche
   à son réveil, et qu'est-ce qui peut attendre.

---

## Contraintes de posture

- **Regarder avant de dépêcher.** Trois sessions en vol, une bloquée sur une
  question qui appartient à Jerry. On lit leur sortie récente avant d'écrire
  quoi que ce soit ; on ne répond jamais à une invite adressée à l'humain.
- **Aucun fait non vérifié dans un brief.** Chaque chemin, chaque numéro,
  chaque empreinte doit venir d'une commande lue dans le même tour.
- **Ce qui coûte, c'est ce qui s'imprime.** Toute action qui peut être du bash
  doit être du bash.
- **Nommer un choix comme choix et un trou comme trou.**
