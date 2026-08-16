# 🗂 Les voies mentorées — index

**Ce fichier manquait.** Sept briefs existaient dans ce dossier sans qu'aucun ne
dise lesquels sont encore valides, ce que chacun a produit, ni si la voie qu'il
a ouverte respire encore. Il fallait un `find` pour le savoir. C'est ça qui
faisait dire à Jerry que l'écosystème « n'est pas complètement vivant ».

**Règle : qui écrit un brief ajoute sa ligne ici, le même jour.**

État relevé le **2026-08-14** (`herdr workspace list`, pidfiles de veille).

| brief | ce qu'il a ouvert | vivant ? | état |
|---|---|---|---|
| `jamai-releve/PASSATION.md` | l'atelier musique — opus 010 à 012 | **oui** — `w17:p6`, veille **supervisée** pid 4059578 | à jour, voir ⬇ |
| `jamai-nouvelle-voie/BRIEF.md` | atelier `abies` sur dossier distant | **oui** — `w1B:p1`, veille pid **2459175** (601260 est mort) | à jour |
| `jamai-nouvelle-voie/MENTORAT-260814.md` | mentorat de `w1B:p1` — faire la musique et la publier | **oui** — remis le 2026-08-14 | à jour |
| `structure-chanson/BRIEF.md` | apprendre à finir une chanson, pas seulement à la commencer | **oui** — `w1E:p1`, ouverte le 2026-08-14 | à jour |
| `structure-chanson/RELEVE-01-260814.md` | **sa réponse** : ce n'est pas l'harmonie, c'est l'écart dynamique — mesuré sur l'opus 014 et croisé avec ISMIR 2013 (6 462 sections Billboard). Balados + corpus vérifiés au `curl`. Page : `claude.ai/code/artifact/d4103a02` | **oui** — remis le 2026-08-14 | à jour |
| `jamai-cast/BRIEF.md` | diffusion télé et enceintes | **session morte, OUTILS VIVANTS** | à jour |
| `jamai-voice-return/BRIEF.md` | faire revenir la parole de Jerry | non vérifié | non vérifié |
| `ligne-telephonique/BRIEF.md` | la ligne téléphonique | non vérifié | non vérifié |
| `william-jamai/PROMPT-DEMARRAGE.md` | l'atelier de William | pane `w15` vide — **mais sa composition vit sur `ilex`**, pas ici | valide |
| `william-jamai/PASSATION-260815-ava001-rise.md` | tout ce que la session `ava001-rise` a créé et poussé — pour les couloirs de William (`ep090-nairobi` et suivants) : issue/PR amont, inventaire, siège Honcho tranché, déblocage du jeton, branche gmtermux | **oui** — écrite le 2026-08-15 | à jour |
| `william-jamai/MENTORAT-01-…md` | mentorat partition et vidéo | idem | non vérifié |

## ⬇ La veille `jamai` est passée sous supervision le 2026-08-14

Sur le mot donné au terminal à 00 h 45 : `~/.config/systemd/user/jamai-watch.service`,
`Restart=always`, activé au démarrage. **Prouvé au `kill -9`** : tuée pid 4057600,
relevée seule 24 s après en 4059578. La passation dit encore « rien n'est
supervisé » — c'était vrai jusqu'à cette nuit. Pour débrancher :
`systemctl --user disable --now jamai-watch.service`.

Deux choses épinglées dans l'unit, chacune mesurée avant d'être écrite : le
portail (**8828**, parce que le 8768 répond `jamai` lui aussi) et le `PATH`
(**`/opt/anaconda3/bin`**, parce que `/usr/bin/python3` n'a pas `scipy` et que
le crochet serait mort à chaque dépôt).

## ⚠️ Un port ne veut rien dire sans son HÔTE et son ARBRE DE CODE

**Correction de ma propre correction.** J'avais écrit ici que le brief de
William était « périmé » et son avertissement sur le 8768 « faux ». **C'était
une sur-correction**, trouvée par la voie du fork le 2026-08-14 et vérifiée :
son brief ne nomme **aucune machine**, il dit seulement de ne pas prendre 8768
par défaut sans qu'on te l'ait donné. J'avais généralisé une mesure faite sur
`localhost` à une phrase qui ne parlait pas de `localhost`.

Les deux faits tiennent ensemble, et c'est ça qui compte :

| hôte | port | atelier | ce qu'il porte |
|---|---|---|---|
| eury / localhost | **8768** | `jamai` | arbre `~/dryades` |
| eury / localhost | **8828** | `jamai` | arbre `~/salix/run/jamai-portal` |
| **`ilex`** | **8768** | **`aureon`** | la composition `ava001` de William |

**Le même numéro de port, sur deux machines, n'est pas le même atelier.** Et sur
une même machine, deux ports peuvent servir le même atelier depuis deux arbres
différents. Donc :

> **La seule identité fiable est le triplet (hôte, port, arbre de code).**
> `data-current-workspace` ne suffit pas — sur eury, 8768 et 8828 répondent
> tous les deux `jamai`.

Sur eury, la conséquence mesurée reste entière :

| port | pid | arbre | WORKSPACE | RECORDINGS_BASE |
|---|---|---|---|---|
| 8828 | 644326 | `~/salix/run/jamai-portal` | `jamai` | `/home/gmusic` |
| 8768 | 1402510 | `~/dryades` | `jamai` | `/home/gmusic` |

Les deux servent **le même atelier sur la même racine**. Écrire sur 8768 ne
range rien chez un inconnu : ça écrit **dans `jamai`**, c'est-à-dire par-dessus
le travail de l'atelier musique. Et comme les deux arbres de code diffèrent,
deux serveurs écrivent les mêmes `composition.json` — dernier écrivain gagne,
aucune erreur levée.

**Le contrôle, en deux commandes**, à faire avant d'écrire sur un portail :

```bash
ss -ltnp | grep :<port>            # quel processus écoute
readlink /proc/<pid>/cwd           # depuis quel arbre de code
```

Et si l'hôte n'est pas celui-ci, refais-les **là-bas** — le résultat d'eury ne
dit rien d'ilex.

*Le brief de William n'est pas réécrit : sa phrase est juste, elle est
seulement sous-spécifiée, et c'est la ligne de mentorat d'une autre voie. On
signale, on ne réécrit pas à sa place.*

## Ce qui n'est sous aucune surveillance

Vérifié le 2026-08-14 : **ni systemd utilisateur, ni cron.** Aucune veille,
aucun portail n'est supervisé. La veille `jamai` est morte toute seule dans la
nuit du 12 au 13 ; le portail est tombé trois fois le 8 août. Tout tient parce
que quelqu'un relance à la main. **Décision en attente chez Jerry depuis le
2026-08-08 — ne rien câbler sans son mot.**
