# Voie 1 — ce qui tourne au réveil de Jerry

*Écrit le 2026-08-05 vers 07h28. Chaque fait vient d'une commande lue dans le
tour où il a été écrit.*

## Ce qui tourne, maintenant

**La veille `episodes` est vivante — pid 2917786**, détachée (`setsid`), cadence
plafonnée à 300 s. Journal : `~/.local/state/episode-voice/episodes-watch.log`.

Trois outils, dans `~/.agents/skills/episode-voice-channel/scripts/` :

| outil | rôle |
|---|---|
| `episodes-watch` | la boucle — `--prime` / `--once` / `--status` / `--stop` |
| `episodes-on-drop` | le crochet — mesure, classe, transcrit, range, relie |
| `episodes-rename` | porte le jugement de nommage, après coup, sans rien perdre |

Le chercheur d'épisodes reliés, `episodes-related`, est **celui de la voie 4** —
posé à 07h23, exécuté pour de vrai à 07h25.

## Ce qui se passera quand tu déposeras ton vidéo

Dans les **cinq minutes** au plus :

1. la veille voit le fichier neuf et **attend qu'il ait fini d'arriver** ;
2. le crochet mesure — timbre, bandes, pouls — et classe **par le grave** ;
3. si c'est de la parole, Whisper transcrit (fr) ;
4. `ep-009` est ouvert **au titre nu**, ton clip attaché, la transcription
   déposée en section ;
5. le chercheur de la voie 4 tourne et dépose « Épisodes reliés » ;
6. le verdict dit ce qui reste : **te nommer l'épisode**.

Éprouvé trois fois ce matin, dont **une fois par le démon lui-même** — dépôt à
07:20:47, détecté à 07:25:39, épisode complet à 07:25:42. `ep-009` a été occupé,
lu, puis **rendu libre** : le portail en est à 8 compositions, prochain libre
`ep-009`. Ton dépôt aura bien le numéro que tu as annoncé.

## Ce que la répétition a fait sortir — deux défauts que personne n'avait payés

**Un fichier encore en train d'arriver était perdu pour de bon.** `episode
watch` ne signale un fichier qu'**une seule fois** : le repère réécrit, il ne
repasse plus. Un vidéo traité à moitié écrit ne revient jamais. La veille attend
maintenant que la taille se stabilise. `jamai-watch` n'a pas cette garde.

**Deux sections texte déposées dans la même seconde s'écrasaient.** Le portail
nomme chaque section à la seconde près. La transcription de `ep-009` avait
disparu du disque, remplacée par les reliés — avec un 200 et pas un mot. Elle ne
survivait que dans le champ `content` de `composition.json`. Corrigé, et vérifié
sur deux fichiers distincts.

Trouvés tous les deux en **lisant l'épisode produit**, pas en le supposant.

## Ce qui t'appartient — je n'ai rien tranché

1. **`w1:p2N` est bloquée sur une invite de permission** — la transcription Groq
   de `260804231226.mov`. Elle t'est adressée. Personne d'autre n'y répond.
2. **Ce dépôt du 2026-08-04 à 23h12** — 1 486 042 octets — **n'est rattaché à
   aucun épisode.** Il est antérieur à l'amorçage de la veille : elle ne le
   prendra pas. Le ranger ou le laisser est ton appel.
3. **`wQ:p1` porte ta consigne « corrige l'issue dotagents#5 » tapée, non
   envoyée.** Je ne l'envoie pas.
4. **La fenêtre de 90 minutes** — une rafale de dépôts complète un seul épisode,
   au-delà un dépôt en ouvre un neuf. C'est un choix, discutable.
5. **Nommer `ep-009`.** Le crochet ne nomme pas : nommer est le jugement.
   `episodes-rename ep-009 "<titre>"` le porte quand tu l'auras pris.

## Ce qui est reporté, et à qui

- **L'outil paramétré pour les six ateliers** — voie 2 (`wW:p2`), qui lit mes
  scripts pour les absorber plutôt que les doubler. Je lui ai transmis les
  quatre défauts et le verrou de numérotation.
- **La qualité du classement des reliés** — voie 4 (`wW:p4`). Son premier
  passage l'a dit lui-même : « Aucun lien PROUVÉ : le classement tient, la
  preuve manque. » C'est de l'honnêteté, pas une panne.
- **La survie de la veille à un redémarrage** — il faudrait une unité systemd.
  C'est un changement au niveau du système ; il t'appartient.

## Ce que la veille ne fera pas

Elle ne range que la **parole**. La musique est mesurée et laissée telle quelle :
un épisode se range sur ce qui est dit. Elle ne touche à aucun dépôt antérieur à
son amorçage. Elle ne committe rien — `~/compositions-episodes` est à toi, et je
l'ai laissé exactement comme je l'ai trouvé.

## Non committé

Ni les scripts, ni cette lecture, ni la référence
`~/.agents/skills/episode-voice-channel/references/chaine-episodes.md`.
Tu n'as pas demandé de commit.
