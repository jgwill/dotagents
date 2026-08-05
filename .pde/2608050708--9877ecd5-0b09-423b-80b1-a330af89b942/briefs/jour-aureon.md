# Veille du jour — atelier AUREON (les journaux)

**Portail : `https://localhost:8798`** — ouvert ce matin, `workspace=aureon`, vérifie-le.
**Dépôts : `~/Recordings-aureon/`** · **actuellement vides, zéro composition.**

## Ce qui n'existe pas encore, et que tu dois bâtir

**Il n'y a aucune chaîne pour cet atelier.** Ni veille, ni crochet. Tu pars de
`atelier-veille`, le moteur paramétré :

```
~/.agents/skills/atelier-veille/
  ateliers.conf        la table — la ligne `aureon` porte déjà le portail 8798
  scripts/atelier-watch, atelier-on-drop, atelier-claim-unit, atelier-post-text
```

Lis `README.md` (20 Ko) avant de câbler.

## L'unité — décidée par Jerry, à la lettre

```
jr-NNN.{type}.{sujet}.v{yymmddhhmmss}

jr-001.main.etincelle-partagee.v260805114230
jr-002.white.gratitude-au-travail.v260805143012
```

- **Tout en minuscules**, sans accent ni ponctuation, comme les slugs existants.
- `{type}` ∈ **`main`** · **`white`** · **`aven`** · **`musc`** — désabrégés par
  Jerry ; `musc` est le seul qui reste court.
- `v` est la **version**, et la version est la date **à la seconde**. Deux
  versions d'une même entrée gardent la même tête et changent de `v`.

## D'où ça vient — lis-le avant de construire

`~/.agents/.pde/2608050708--9877ecd5-.../sources-aureon.md` et
`sources-aureon-issue-115.md`. En bref :

- Une compétence complète existe déjà : `~/Downloads/aureon-journal-events.zip`
  → `SKILL.md`, 18 131 octets. Quatre types d'événement ouvrent quatre
  contenants, avec protocole de détection.
- Les quatre journaux sont nés dans `jgwill/orpheus` — #587 Main, #704 White
  Feather, #784 Aven's Loop, #717 Gmusic Lyrics.
- Aureon **lie chaque entrée à une issue GitHub**.
- Flux rituel : **Réalisation → Brouillon → Revue → Publication.** La **Revue
  appartient à Jerry.**
- Orthographe **A-U-R-E-O-N**, jamais Orion ni Oreon.

## Ce qui reste ouvert et n'est pas à toi

Le protocole d'archivage laisse explicitement le choix à l'utilisateur —
éphémère, base cérémonielle, ou Drive. **Ne tranche pas.**

## Ta première action

Câble la veille et le crochet pour `aureon`, éprouve-les à vide, puis arme un
`Monitor`. Un dépôt de Jerry aujourd'hui doit produire une entrée de journal
correctement nommée, et te réveiller pour le seul jugement qui reste : quel
contenant, et quel sujet.

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
