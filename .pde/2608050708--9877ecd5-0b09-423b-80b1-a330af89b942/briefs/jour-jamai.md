# Veille du jour — atelier JAMAI (les opus)

**Portail : `https://localhost:8768`** — vérifie `workspace=jamai` avant d'écrire.
**Dépôts : `~/Recordings-jamai/`** · **Unité : `op-NNN-slug`** · quatre opus existent.

## Ce qui existe

```
~/.agents/skills/jamai-morning/scripts/
  jamai-watch      la veille
  jamai-on-drop    le crochet : mesure, transcrit, parse le MIDI, range
  jamai-midi.py    parseur MIDI note à note
  jamai-measure.py timbre, bandes, pouls
  jamai-chords.py  l'accord de chaque temps — JAMAIS nommer un accord à l'œil
```

**Le crochet ne crée pas d'opus.** Il établit ce que contient le dépôt. La
musique, c'est toi.

## Ta première action

```bash
setsid ~/.agents/skills/jamai-morning/scripts/jamai-watch \
  > ~/.local/state/episode-voice/jamai-watch.log 2>&1 < /dev/null &
```

Puis arme un `Monitor` sur `~/.local/state/episode-voice/jamai-watch.log`.

## Ce que tu fais quand Jerry dépose

Lis la compétence `~/.agents/skills/jamai-morning/SKILL.md` en entier — elle
porte la méthode et les cinq pièges muets de la chaîne ABC. En résumé :

- **MIDI** : parse note à note, nomme les accords avec `jamai-chords.py`,
  jamais à l'œil.
- **Audio chanté ou fredonné** : passe-haut à 110 Hz puis produit spectral
  harmonique **indexé depuis 0 Hz** — l'indexer depuis une bande verrouille
  sur l'harmonique 3 et rend des notes deux octaves trop haut.
- **Parole** : c'est une consigne. Transcris et agis.

Puis : écris l'ABC, **rastérise la partition et REGARDE-LA**, rends le MP3,
monte la vidéo, attache, committe dans `~/compositions-jamai`.

**R11 : ne jamais republier une source sans avoir d'abord attaché le rendu de
la version sortante.** Ce rendu est sa dernière sauvegarde.

## La règle qui décide tout

**Seul ce qui s'imprime coûte.** Un tour de veille silencieux coûte zéro. Tout
ce qui peut être du bash doit être du bash ; on ne réveille un modèle que pour
ce qui demande un jugement. Un réveil coûte ~0,17 $.

## Cinq choses payées aujourd'hui — ne les refais pas

1. **Ne jamais hériter de `PIXEL_RECORDER_URL`.** Fixe-le au portail de TON
   atelier, et vérifie que le portail répond bien avec le bon `workspace`
   avant d'écrire quoi que ce soit. Le 2026-08-05, un crochet a hérité de 8768
   et fabriqué trois épisodes dans l'atelier jamai.
2. **Refuser net un fichier du registre `<atelier>-mine.txt`.** Ce que
   l'atelier produit lui-même n'est pas un dépôt. Sans ça, tes propres audios
   rouvrent des unités en boucle — deux épisodes fantômes créés ce matin.
3. **Ne pas classer parole/musique au spectre.** Mesuré sur sept dépôts réels :
   la consigne parlée de 8,7 s sort à 342 Hz et 42,6 % sous 250 Hz, le chant de
   7,6 s à 465 Hz et 38,8 %. Le chant est plus aigu que la parole. Transcris,
   et laisse le CONTENU décider.
4. **Un repère d'état par veille.** Deux veilles qui partagent
   `watch-<atelier>.sha` se volent les notifications ; un dépôt de Jerry a
   dormi douze heures ainsi. Exporte ton propre `EPISODE_STATE_DIR`.
5. **Établir avant de parler.** Ne décris jamais un dépôt sans l'avoir mesuré,
   ne nomme jamais un accord à l'œil, regarde la partition rastérisée. Nomme un
   choix comme choix et un trou comme trou.

## Jerry est parti marcher

Il déposera de l'audio ou de la vidéo dans la journée. **Il dit souvent la
destination dans l'enregistrement lui-même** — « mets ça dans l'épisode 9 »,
« encore dans l'Opus 3 ». Le lecteur est déjà écrit et éprouvé :

```
~/.agents/skills/episode-voice-channel/scripts/destination-du-depot <texte.txt>
  → unite ep-009  |  neuf ep  |  courant  |  autre op
```

Ne l'appelle jamais sur un fichier de ton registre : nos propres audios disent
« épisode 9 » parce que c'est nous qui l'avons écrit.

## Ce qui t'appartient, et ce qui lui appartient

**À toi** : mesurer, transcrire, ranger, attacher, committer.
**À lui** : nommer. Un titre est un jugement. Laisse le titre nu et dis-le.

Ne réponds jamais à une invite en attente dans un autre panneau : c'est une
question qui lui est adressée.
