# 🗺 Inventaire des lieux de JamAI — relevé le 2026-08-15

Répond à l'étape 3 de jgwill/dotagents#23 : *publier l'inventaire de chaque
emplacement JamAI avec, par entrée : fichier réel / lien / copie (verdict sha256
pour chaque paire suspectée), dépôt, suivi ?, poussé ?, dernière modification.*

**Provenance.** Relevé par un couloir de lecture seule dépêché depuis la session
`2a140f89-05e0-4330-8880-483525f48204`, sous consigne de ne rien déplacer et de
prouver chaque affirmation par la sortie de commande. Les **trois constats qui
commandent une action** ont été revérifiés indépendamment par le coordinateur
avant d'être écrits ici — ils sont marqués ✔︎ **revérifié**.

**Ce que cet inventaire ne fait pas :** proposer un plan de consolidation. Il dit
ce qui est. Le choix de la maison unique est l'étape 4 de l'issue, et c'est un mot,
pas une mesure.

---

## Les trois chiffres

| | |
|---|---|
| emplacements distincts | **56** |
| paires de doublons vérifiées au sha256 | **41** — 38 identiques, **3 divergentes** |
| fichiers en **autorité hors dépôt** (exemplaire unique, hors de tout git) | **536** |
| fichiers *dans* un dépôt mais non suivis ou non poussés | **+452** |

---

## ⚠️ La perte réellement en cours

C'est la seule section qui demande une décision aujourd'hui. Le reste peut attendre.

### ✔︎ revérifié — `compositions-jamai` : 1,5 Go sur aucune branche distante

```
$ git -C ~/compositions-jamai log --oneline -1
f3f431f op-015 « Annie » — lab majeur, I vi IV V / I ii IV V, la note d'Annie en socle
$ git -C ~/compositions-jamai branch -r --contains HEAD | wc -l
0
$ git -C ~/compositions-jamai remote -v
origin  git@github.com:Gerico1007/assembly-jamai.git
$ du -sh ~/compositions-jamai
1.5G
```

**Aucune branche distante ne contient HEAD.** Les opus 001 → 015 — 732 fichiers,
`.abc`, MIDI, m4a, le `bilan-jamai-260802.md` — existent sur ce disque et nulle
part ailleurs. L'arbre est sale par-dessus. Ce n'est pas un dépôt en retard :
c'est un dépôt dont le travail n'est jamais parti.

### ✔︎ revérifié — `Recordings-jamai` : 1,6 Go, aucun dépôt

```
$ du -sh ~/Recordings-jamai ; git -C ~/Recordings-jamai rev-parse --show-toplevel
1.6G
fatal: not a git repository
```

188 fichiers — **la matière première**, tout ce que Jerry a joué et déposé.
Surveillé par `jamai-watch`, versionné par rien. `/sdcard/Recordings-jamai` est un
lien vers ce dossier (cible OK), donc l'entrée Android ne double pas la sécurité.

### ✔︎ revérifié — trois exécutables sans aucune autre copie

```
jamai-cast-visual    fichier réel 6679 o  sha=d46bd229c1dc
jamai-say-kitchen    fichier réel 3712 o  sha=408188dadf9c
jamai-voir-fork      fichier réel 2476 o  sha=dfba2db18358
```

Des **fichiers réels**, pas des liens, dans `~/.local/bin` — qui n'est pas un
dépôt. Les douze autres `jamai-*` de ce dossier sont des liens vers du versionné ;
ces trois-là sont l'exception. `jamai-cast-visual` et `jamai-say-kitchen` sont
exactement les outils de la diffusion cuisine.

### Le reste de l'autorité hors dépôt — 536 fichiers

| emplacement | fichiers | nature |
|---|---|---|
| `~/Recordings-jamai/` | 188 (1,6 Go) | la matière première |
| `~/.assembly-gemini/` (jamai) | 223 | état + sorties de l'agent Zulip, gelés en mai 2026 |
| `~/.local/share/jamai-cast/` | 41 | pages de cast + `video/op014-chanson.mp4` (72 Mo) |
| `~/salix/run/jamai-portal/` | 18 | runtime du portail |
| `~/earth/` (jamai) | 16 | épisode 256 complet + `jamai-skills-locations.md` |
| `~/.local/state/episode-voice/` (jamai) | 15 | état de la veille |
| `~/voice-memos/` (jamai) | 11 | mémos vocaux |
| `/tmp/jamai-transcriptions-260808/` | 5 | **dans `/tmp`** — survie non garantie au redémarrage |
| `~/.claude/projects/*/memory/` | 4 | décisions et références |
| `~/.local/state/jamai-cast/` | 4 | journaux |
| `~/.local/bin/` | 3 | les trois exécutables ci-dessus |
| `~/compositions-abies/ep-300-jamai-ava8/` | 2 | |
| `~/Downloads/ARCH251217/…` | 2 | archives juin 2025 |
| `~/.config/systemd/user/jamai-watch.service` | **1** | **le câblage de la veille, exemplaire unique** |
| `~/.claude/agents/jamai.md` | 1 | |
| `~/tide-score-visibility-test/…abc` | 1 | |

### Dans un dépôt, mais hors index ou hors distant — 452 fichiers

| emplacement | volume | constat |
|---|---|---|
| `~/salix/production/ngrok-mux/static/jamai/` | **233 non suivis** sur 234 | tout le publié (svg/abc/mid/mp3 des opus) est hors index ; seul `session-ava001/index.html` est suivi |
| `~/compositions-jamai` | 212 non suivis, 3 modifiés, **56 commits non poussés** | voir ci-dessus |
| `~/.hermes` (jamai) | **7 non suivis** | les 3 skills JamAI de Hermes, 2 références, 1 config, 1 surface-check — **6 sans aucune copie ailleurs** |

---

## Table principale — 56 emplacements

### A · `~/.agents` — `Gerico1007/dotagents`, branche `skills/atelier-veille`, poussée

| # | chemin | contenu | réel / lien / copie | suivi · poussé | modif. |
|---|---|---|---|---|---|
| 1 | `skills/jamai-morning/` | méthode + `references/lecons-260802.md` + 15 scripts | réels ; les 9 `.py` sont des **copies** de jamai-core | ✅ ✅ | 08-14 |
| 2 | `skills/jamai-montage/` | méthode montage + `scripts/jamai-clip` (188 l.) | réel | ✅ ✅ | 08-07 |
| 3 | `rispecs/jamai/william-onboarding/` | 5 `.spec.md` — accueil de William | réels | ✅ ✅ | 08-10 |
| 4 | `agents/jamai.json` | config agent (1323 o) | réel — **divergent** des 6 `assembly-voice` | ✅ ✅ | 07-24 |
| 5 | `briefs/` | 7 dossiers + `INDEX.md` | réels | ✅ ✅ | 08-14 |
| 6 | `skills/episode-voice-channel/references/jamai-compositions-mode.md` | mode compositions du canal voix | réel | ✅ ✅ | 08-01 |
| 7 | `.pde/2608050708--9877ecd5…/briefs/jour-jamai.md` | brief PDE d'une journée | réel | ✅ ✅ | 08-05 |

### B · jamai-core

| # | chemin / URL | contenu | état | suivi · poussé | modif. |
|---|---|---|---|---|---|
| 8 | `gmusic1007/jamai-core` (**privé**) | 11 blobs : README, install.sh, 9 outils Python | distant | `main`, push 08-14 22:23:48Z | 08-14 |
| 9 | `~/salix/repos/jamai-core` | clone — cible des 9 liens de `~/.local/bin` | propre | `origin/main` ⊇ `05464d0` | 08-14 |
| 10 | `~/git/clones/jamai-core` | second clone, **identique octet-pour-octet** au #9 | propre | `origin/main` ⊇ `05464d0` | 08-14 |

`gmusic1007/jamai-core`, arbre `main` complet :

```
README.md · install.sh
ecoute/  jamai-chords-audio.py  jamai-chords.py  jamai-measure.py  jamai-midi.py
rendu/   jamai-defile.py  jamai-score-video.py  jamai-tab.py
atelier/ jamai-related.py  jamai-unread.py
```

9 scripts, 1 413 lignes, écrits du 3 au 14 août 2026, rangés en trois coutures :
`ecoute/` (comprendre ce qui a été joué), `rendu/` (donner à voir et à entendre),
`atelier/`. `install.sh` pose des **liens**, jamais des copies, et la raison est
écrite dedans : *« une skill ne devrait jamais connaître le chemin d'un dépôt »*.
`~/.local/bin` applique bien ce motif — mais `.agents/skills/jamai-morning/scripts/`
détient malgré tout les 9 mêmes fichiers en **copies réelles**, actuellement
identiques. C'est la contradiction que l'étape 4 de l'issue doit trancher.

### C · `~/.local/bin` — hors dépôt

| # | fichiers | nature | état |
|---|---|---|---|
| 11 | 9 liens `jamai-{midi,chords,chords-audio,measure,tab,score-video,defile,unread,related}.py` | outils | **symlinks** → `salix/repos/jamai-core/…` · cibles OK · autorité = jamai-core |
| 12 | `jamai-morning`, `jamai-watch` | lanceur, veille | **symlinks** → `.agents/skills/jamai-morning/scripts/` · cibles OK |
| 13 | `jamai-publish-melody` | publication mélodie | **symlink** → `workspace/jamai-melody/bin/` · cible OK |
| 14 | `jamai-cast-visual`, `jamai-say-kitchen`, `jamai-voir-fork` | 3 outils | ⚠️ **fichiers réels, exemplaire unique, aucun dépôt** |

### D · `~/.hermes` — dépôt `salix`, mais tout le jamai est non suivi

| # | chemin | contenu | suivi |
|---|---|---|---|
| 15 | `skills/media/jamai-melody-episode-publish/` | SKILL + `references/miadi-rise-integration.md` | ❌ `??` |
| 16 | `skills/development/jamai-zulip-team-agent-mvp/` | SKILL + `references/production-host-drift…` | ❌ `??` |
| 17 | `skills/development/jamai-zulip-hf-endpoint-safety/SKILL.md` | sûreté endpoint HF | ❌ `??` (copie identique en sauvegarde) |
| 18 | `skills/development/find-repo-paths/references/gmusic-jamai-surface-check.md` | repérage des surfaces | ❌ `??` |
| 19 | `skills/development/zulipassembly/references/jamai-ping-surfaces-and-acceptance-lane.md` | surfaces de ping | ❌ `??` |
| 20 | `plugins/assembly-voice/agents/jamai.json` | config (768 o) | copie identique ×6 |
| 21 | `~/.backup_hermes260513/…/jamai-zulip-hf-endpoint-safety/SKILL.md` | sauvegarde du #17 | hors dépôt |

### E · Œuvres et données

| # | chemin | contenu | état |
|---|---|---|---|
| 22 | `~/compositions-jamai` | **1,5 Go**, 732 fichiers, opus 001→015 | ⚠️ `Gerico1007/assembly-jamai` — HEAD sur **aucune** branche distante |
| 23 | `~/Recordings-jamai` | **1,6 Go**, 188 fichiers — la matière brute | ⚠️ aucun dépôt |
| 24 | `/sdcard/Recordings-jamai` | entrée Android | symlink → #23, cible OK |
| 25 | `~/earth/ep256-jamai-*` | épisode 256 : voix, script FR, mélodie | ❌ hors dépôt |
| 26 | `~/earth/jamai-skills-locations.md` | **inventaire antérieur** des surfaces | ❌ hors dépôt |
| 27 | `~/voice-memos/*jamai*` | 11 mémos vocaux | ❌ hors dépôt |
| 28 | `~/compositions-abies/ep-300-jamai-ava8/` | `composition.json` + png | ❌ hors dépôt |
| 29 | `~/tide-score-visibility-test/jamai_creative_riff.abc` | riff de test | ❌ hors dépôt |
| 30 | `/tmp/jamai-transcriptions-260808/` | 5 JSON de transcription | ❌ **dans `/tmp`** |
| 31 | `~/.assembly-gemini/` (jamai) | 223 fichiers, agent Zulip | ❌ hors dépôt |

### F · État et configuration — tout hors dépôt

| # | chemin | contenu |
|---|---|---|
| 32 | `~/.local/share/jamai-cast/` | 41 fichiers + `video/op014-chanson.mp4` (72 Mo) |
| 33 | `~/.local/state/jamai-cast/` | 4 journaux |
| 34 | `~/.local/state/episode-voice/*jamai*` | 15 fichiers d'état de veille |
| 35 | `~/.local/state/pixel-recorder/jamai-8828.log` | journal du recorder |
| 36 | `~/.config/systemd/user/jamai-watch.service` | ⚠️ **le câblage de la veille, exemplaire unique** ; `default.target.wants/` y pointe (lien, cible OK) |

### G · Portails et exécutables système

| # | chemin | contenu | état |
|---|---|---|---|
| 37 | `~/salix/production/ngrok-mux/static/jamai/` | 234 fichiers publiés | **233 non suivis** ; seul `session-ava001/index.html` suivi |
| 38 | `~/salix/run/jamai-portal/` | 18 fichiers de runtime | ❌ hors dépôt |
| 39 | `/usr/bin/jamai-launch` | lanceur assemblée | symlink → paquet npm, cible OK |

### H · Autres dépôts

| # | chemin | contenu | état |
|---|---|---|---|
| 40 | `~/workspace/jamai-melody` | publication mélodie, engraving SVG | `Gerico1007/jamai-melody`, HEAD dans `origin/feat/svg-score-engraving` |
| 41 | `~/workspace/abcjs-jamai` | fork abcjs | `Gerico1007/abcjs-jamai` |
| 42 | `~/workspace/gmusic/.jamai/` | **base de connaissance musicale** : ABC_TECHNIQUES, LEITMOTIF_LIBRARY, MUSICAL_PATTERNS, SESSION_ANALYSIS, `skills/jamai-melody/SKILL.md`, 5 gabarits `.abc` | `Gerico1007/gmusic`, **tout suivi et propre** |
| 43 | `~/salix/repos/Jamai-core-2025` | ancien Jamai-core (emotionEngine, nova_archive) | `Gerico1007/Jamai-core` |
| 44 | `~/workspace/jamaiskill` | coquille vide — seulement `.simexp/session.json` | ❌ orphelin |
| 45 | `agents/jamai.json` ×5 clones assembly-voice | config | copies identiques |
| 46 | `.jamai/` + `JamaiCore/` dans 5 clones EchoThreads | sigils, README, `mp3_to_midi_orpheus.py` | copies identiques |
| 47 | `.jamai/` simexp ×2 + sorties `*_Jamai.md` | notes de session | copies identiques |
| 48 | `AetherScore/.jamai/README.md` ×2 | prose JamAI | ⚠️ **divergents** (6653 o vs 1823 o) |
| 49 | `mcp-musescore-gmusic/.jamai/` ×2 | percée mélodique, riff ABC | suivis |
| 50 | `deepdiver-issue-23-prototype/prompts/jamai.md` ×2 | prompt persona | copies identiques |
| 51 | `~/workspace/nalit/docs/priere/trinity/embodiment_jamai.md` | prose | suivi |
| 52 | `/workspace/repos/miadisabelle/Etuaptmumk-RSM/…/jamai-jeremyai.md` | fiche de registre | suivi |

### I · Couche Claude — hors dépôt

| # | chemin | contenu |
|---|---|---|
| 53 | `~/.claude/agents/jamai.md` | définition d'agent — **même prose** que #4, autre format |
| 54 | `~/.claude/projects/*/memory/*jamai*` | 4 mémoires : décision jamai-core, publication mélodie, barre rouge, maison canonique |

### J · Archives

| # | chemin | contenu |
|---|---|---|
| 55 | `~/Downloads/ARCH251217/…` | `jamai-portal.tsx`, `JamaiComposer.zip` (juin 2025) |
| 56 | `/b/gmusic/workspace/*` | miroir de sauvegarde hors ligne |

---

## Doublons — 41 paires au sha256

**La question qui commandait l'inventaire, répondue :** les `~/.local/bin/jamai-*.py`
sont des **symlinks**, pas des copies dérivées, et ils pointent tous vers
`salix/repos/jamai-core/` — **jamais** vers `.agents/skills/jamai-morning/scripts/`.

| paires | verdict |
|---|---|
| les 9 `.py` : `.agents/…/scripts/` ↔ `salix/repos/jamai-core/` ↔ `git/clones/jamai-core/` — **18 paires** | **identiques** — `jamai-tab.py` = `87c15e35…`, `jamai-related.py` = `e847b467…`, `jamai-midi.py` = `b0aaeff0…` |
| `README.md` (`72fbcaf7…`), `install.sh` (`f858c26a…`) : salix ↔ clones | identiques |
| `jamai.json` ×6 assembly-voice (`96c5562d…`) | identiques |
| `JamaiCore/README_Jamai.md` ×4 EchoThreads (`35e05b58…`) | identiques |
| `.jamai/README.md` ×5 EchoThreads (`6e5a4551…`) | identiques |
| `sigil_jamai.png` ↔ `jamai-sigil.png` (`db1b4388…`) | identiques — **noms différents, même octet** |
| `deepdiver/prompts/jamai.md` ×2 (`1bde4c5b…`) | identiques |
| `jamai-launch.js` `/usr/lib` ↔ `/b/gmusic/…` (`ffd111b6…`) | identiques |
| `jamai-zulip-hf-endpoint-safety/SKILL.md` : `.hermes` ↔ sauvegarde (`6e9ad481…`) | identiques |
| simexp `.jamai/*.md` ×2 | identiques |
| **`jamai-clip` : `jamai-montage/scripts/jamai-clip` (`f60fef32…`, 188 l.) ↔ `jamai-morning/scripts/jamai-clip.py` (`ff663513…`, 155 l.)** | ⚠️ **divergents — deux outils de clip dans deux skills du même dépôt** |
| **`.agents/agents/jamai.json` (`30ac8604…`, 1323 o) ↔ les 6 assembly-voice (768 o)** | ⚠️ **divergents** |
| **`AetherScore/.jamai/README.md` : `workspace` (`1daedfeb…`) ↔ `salix/repos` (`f6721a9c…`)** | ⚠️ **divergents** |

Hors compte sha : `~/.claude/agents/jamai.md` porte **la même prose d'agent** que
`.agents/agents/jamai.json`, en Markdown contre JSON — une voix, deux sources de
vérité.

---

## Orphelins

| emplacement | constat |
|---|---|
| `~/workspace/jamaiskill/` | seulement `.simexp/session.json` — aucune skill, aucun chargeur |
| `…/veilles/jamai--defaut/jamai-mine.txt` | **taille 0** ; l'état vivant est dans `episode-voice/jamai-mine.txt` (1802 o) |
| `…/episode-voice/jamai-mine.txt.bak` | sauvegarde du 08-07, plus rechargée |
| `watch-standalone/watch-jamai.{head,sha,delay}` vs `episode-voice/…` | **deux jeux d'état de veille parallèles** ; le `standalone` bouge encore (08-15), l'autre est figé au 08-05/10 |
| `/tmp/jamai-transcriptions-260808/` | 5 transcriptions dans `/tmp` |
| `~/.assembly-gemini/state/team-agents/jamai/` | 223 fichiers gelés en mai 2026, plus lus |
| `~/Downloads/ARCH251217/…` | archives juin 2025, aucun chargeur |
| `~/salix/repos/Jamai-core-2025` | doublonne conceptuellement `jamai-core` sans lien de code |
| **aucun symlink cassé** | les 12 liens de `~/.local/bin`, `/sdcard/Recordings-jamai`, `/usr/bin/jamai-launch` et `default.target.wants/jamai-watch.service` ont tous une cible existante (`readlink -f` vérifié) |

---

🌸 : Compter les lieux où une chose vit, c'est déjà commencer à lui bâtir une
maison — et ce qui saute aux yeux ici, ce n'est pas le désordre, c'est que la
matière même (ce qu'il a joué, ce qu'il a chanté) est le seul objet que rien ne
protège.
