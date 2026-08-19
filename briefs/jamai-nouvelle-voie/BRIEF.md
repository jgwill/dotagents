# 🎸 Brief — ouvrir un atelier JAMAI

Tu ouvres un atelier de musique avec Jerry ⚡. Il enregistre au téléphone ou au
pad, dépose, et veut construire la pièce avec toi. **Il n'est presque jamais
devant l'écran.** Réponds en français ; il passe à l'anglais sans prévenir,
suis-le.

Tout ce qui est chiffré ici a été **mesuré ou lu dans le source** le 2026-08-11
par l'atelier voisin (`w17:p1`), qui tient encore le contexte si tu en as besoin.

---

## 1. TA PREMIÈRE ACTION : NE DÉMARRE PAS LA VEILLE

C'est sa consigne explicite, dans ses mots :

> « before starting the monitor, it will ask me on which folder the monitor
> should look, because I'm gonna tell him another place — it will be in a device
> using SSH. »

**Demande-lui le dossier avant de lancer quoi que ce soit.** Puis lis le §2 : ce
qu'il te donnera ne sera peut-être pas branchable tel quel, et il vaut mieux le
lui dire tout de suite que de lancer une veille qui ne verra jamais rien.

Ce que tu peux faire sans lui : lire les skills du §4, vérifier le portail (§5).

---

## 2. COMMENT LA VEILLE CHOISIT SON DOSSIER — lis ça avant de promettre

Le dossier **n'est pas un réglage**. Il est déduit du nom de l'atelier.

`episode` ligne 548 (`watch_dirs()`) :

```sh
watch_dirs() {                    # les deux dossiers qu'un atelier écrit
  if [ "$ws" = "main" ] || [ -z "$ws" ]; then
    printf '%s\n%s\n' "$HOME/compositions" "$HOME/Recordings"
  else
    printf '%s\n%s\n' "$HOME/compositions-$ws" "$HOME/Recordings-$ws"
  fi
}
```

Donc `episode watch <atelier>` regarde `~/compositions-<atelier>` et
`~/Recordings-<atelier>`. Rien d'autre. **Choisir un nom d'atelier, c'est
choisir les dossiers.**

Et `jamai-watch` — le démon — **code `jamai` en dur à trois endroits** :

| ligne | ce qu'il y a |
|---|---|
| 65 | `out="$("$EP" watch jamai 2>&1)"` |
| 73 | `sed -n 's\|^  new /home/gmusic/Recordings-jamai/\|…\|p'` — chemin absolu |
| 95 | `"$EP" watch jamai --interval` |

plus `LOG`, `PIDFILE`, `LEDGER` (lignes 25-27) qui portent tous `jamai`.

**Conséquence : un nouvel atelier demande une COPIE de `jamai-watch` avec le nom
changé partout.** Ce n'est pas une option de ligne de commande. Si tu lances
`jamai-watch` tel quel en croyant surveiller autre chose, tu surveilleras
l'atelier de quelqu'un d'autre — sans erreur, sans rien dire. C'est le mode de
panne le plus cher ici.

Le ledger `~/.local/state/episode-voice/jamai-mine.txt` sert à ignorer les
fichiers produits par l'atelier lui-même : sans lui, tes propres rendus
reviennent comme des dépôts de Jerry. Ta copie a besoin du sien.

**Cadence** : `MIN=60`, `MAX=600` secondes, doublement à chaque tour silencieux,
retour à 60 s dès que ça bouge. Entre son dépôt et ta réaction il peut donc
s'écouler **jusqu'à dix minutes**. Ne lui promets pas du temps réel.

---

## 3. SI LE DOSSIER EST SUR UN APPAREIL EN SSH

L'empreinte est locale. `fingerprint()` fait, sur chaque dossier non-git :

```sh
find "$d" -maxdepth 2 -type f -printf '%T@ %s %p\n' | sort
```

Vérifié sur cette machine : **`sshfs` et `rsync` sont présents, `inotifywait`
est ABSENT.** Donc pas de notification poussée : ce sera du sondage, quoi qu'il
arrive.

Trois voies, avec leur coût réel :

**a) Monter le dossier distant sur `~/Recordings-<atelier>` (sshfs).**
Rien d'autre à changer, l'empreinte fonctionne telle quelle. Mais ce `find`
repart **à chaque tour**, de 60 à 600 s, à travers le tailnet. Sur un téléphone
qui dort, chaque tour peut traîner ou échouer. **Mesure une passe avant
d'adopter** : `time find <point-de-montage> -maxdepth 2 -type f | wc -l`.

**b) Tirer périodiquement en local (rsync), puis veiller le dossier local.**
C'est ce pour quoi la veille est faite. Le téléphone hors ligne rend la copie
périmée, pas cassée — et une veille qui se trompe silencieusement est pire
qu'une veille en retard.

**c) Faire tourner la veille SUR l'appareil.** Le crochet a besoin de ffmpeg, de
python3 et d'une clé Groq. **Ne le promets pas avant de l'avoir vérifié là-bas.**

Les nœuds Android sont en Termux, **port 8022, pas 22** :

```bash
ssh -p 8022 larix.ferret-harmonic.ts.net "<commande>"
```

Même forme pour `ilex`, `tilia`, `abies`. Eury est en port 22.
*Connection refused* = sshd n'est pas lancé dans Termux (Wakelock + Tailscale
Always-On à activer, c'est à Jerry de le faire). *Timeout* = le chemin tailnet
est tombé ; `tailscale ping <nœud>`.

---

## 4. CE QU'IL FAUT CHARGER — en entier, ne résume pas

| skill | ce qu'elle porte |
|---|---|
| `~/.agents/skills/jamai-morning/SKILL.md` | **la méthode**, et les pièges muets de la chaîne ABC |
| `~/.agents/skills/episode-voice-channel/SKILL.md` | le portail, la voix, l'attachement |
| `~/.agents/skills/jamai-montage/SKILL.md` | la vidéo, la fusion avec des images |

Les outils sont éprouvés — **ne les réécris pas** :

| script (`~/.agents/skills/jamai-morning/scripts/`) | ce qu'il fait |
|---|---|
| `jamai-midi.py` | relevé MIDI note à note, tempo, ambitus |
| `jamai-chords.py` | nomme les accords d'un MIDI, temps par temps |
| `jamai-chords-audio.py` | accords et tonalité depuis un ENREGISTREMENT |
| `jamai-measure.py` | timbre, énergie par bande, pouls, attaques |
| `jamai-score-video.py` | vidéo de partition. **Toujours `--bars <n>`** : il REFUSE plutôt que de sortir un montage faux |
| `jamai-tab.py` | tablature six lignes |
| `jamai-publish-melody` | publication publique. **Toujours `--slug` explicite** — sans lui le slug casse sur les accents |

---

## 5. LE PORTAIL — la faute la plus chère est ici

Chaque atelier a le sien. **Le 8828 sert `jamai`. Le 8768 a été rendu à un autre
agent le 2026-08-08 : ne l'utilise jamais.**

**Vérifie l'identité, jamais le port seul :**

```bash
curl -sk "$PIXEL_RECORDER_URL/" | grep -o 'data-current-workspace="[^"]*"'
```

Un port qui répond n'est pas un port qui est le tien. Se tromper range le
travail de Jerry dans l'atelier d'un autre, sans erreur.

Forme de relance (adapte le port et le nom) :

```bash
cd ~/salix/run/jamai-portal && setsid env WORKSPACE=<atelier> RECORDINGS_BASE="$HOME" \
  node web/pixel-recorder.js >> ~/.local/state/pixel-recorder/<atelier>.log 2>&1 &
```

**Ni le portail ni la veille ne sont sous systemd.** Le portail est tombé trois
fois le 2026-08-08. Jerry le sait, il n'a pas tranché. **Ne câble rien sans son
mot.**

Bonne nouvelle : **la détection ne passe pas par le portail.** Portail mort =
publication impossible, mais aucun dépôt manqué. Préserve cette propriété.

---

## 6. SES PRÉFÉRENCES — non négociables

1. **Croches ligaturées.** En ABC ce sont les **espaces de la source** qui
   décident : groupe par temps, sans espace à l'intérieur d'un groupe.
2. **Jamais un voicing de guitare inventé.** Il a eu raison contre la mesure
   trois fois en une semaine. **Mesure la bande 300–1400 Hz avant d'écrire un
   aigu.** Il donne des doigtés exacts, corde et case : calcule, ne devine pas.
3. **Tablature avec la partition** (`jamai-tab.py`). C'est un **vérificateur** :
   elle a débusqué deux octaves de travers sous une portée parfaitement propre.
4. **`git add` par nom de fichier. Jamais `-A`, jamais `.`, jamais `-a`.**
5. **Il n'est pas devant l'écran — LIVRE, ne demande pas.** Publier n'est pas une
   permission à obtenir, c'est le canal lui-même. Ses mots : « fais-moi pas me
   lever pour aller à l'ordinateur pour te dire de me publier une vidéo. »
   L'ordre : publier → mesurer ce qui est EN LIGNE → `episode video` →
   `episode note` → `episode say`. Les questions vont dans la note et dans la
   voix, jamais dans le terminal, et elles n'empêchent jamais l'envoi.
6. **Il aime choisir.** Deux versions valent mieux qu'une question.
7. **Nomme un choix comme un choix et un trou comme un trou.** La tonalité, le
   tempo, les longueurs de section sont à toi : dis-le. Ce que la banque ne sait
   pas rendre est un trou : dis-le aussi.
8. **La voix** : `episode say --persona aureon` (français) — `jamai`, `nyro` et
   `synth` sont anglophones. Garde sous 30 s.

---

## 7. LES PIÈGES MUETS — même forme à chaque fois : fichier valide, aucune erreur, résultat faux

1. **Une LIGNE VIDE termine le morceau en ABC.** Trois rendus ont donné un MIDI
   valide de 323 octets, zéro note, zéro avertissement. Sépare par `%`.
2. **`%%score` avant `K:`**, identifiants exactement ceux du corps.
3. **Une altération se propage jusqu'à la fin de la mesure**, à travers les
   octaves. Mets une altération **explicite sur chaque note** (`=` compris) puis
   **relis le MIDI et compare aux hauteurs voulues**.
4. **`abc2midi` joue les symboles d'accord.** `%%MIDI gchordoff`, **par voix**.
5. **`z5` n'est pas notable d'un seul silence.** Coupe sur le temps.
6. **`overlay=…:shortest=1` avec une image fixe** sort 0,04 s. Il faut `-loop 1`.
7. **Le silence de queue.** FluidSynth laisse plusieurs secondes de vrai zéro —
   13,6 s sur un opus. Mesure où le son s'arrête et coupe.
8. **Deux imports dans la même seconde** sont refusés. Espace tes appels.
9. **`language=fr` forcé** sur Whisper ne fait pas échouer : il TRADUIT mal avec
   l'aplomb d'une transcription. La détection est automatique, laisse-la.
10. **Le bouton Analyse écrit un sidecar** `<fichier>.nyro.json`. Cherche-le
    avant de refaire le calcul ; ses durées sont courtes d'un hop (46,4 ms).

**Et quatre payés le 2026-08-11, tous par confusion d'unité :**

11. **L'échelle de la bande 2–5 kHz est l'AMPLITUDE, pas la puissance.** Le même
    son donne 18,3 % en amplitude et 2,5 % en puissance. Les seuils de Jerry —
    **13,12 % rejeté, 5,98 % accepté, ~3 % pour une pièce douce** — sont en
    amplitude. Se tromper d'échelle fait passer une pièce stridente pour douce
    d'un facteur dix.
12. **La colonne `temps` de `jamai-midi.py` est en NOIRES, pas en secondes**
    (`t0/div`). Un défaut entier a été inventé sur cette lecture-là.
13. **Le pic le plus fort d'un son n'est pas sa note.** Sur un chant d'oiseau, le
    pic était à 2161 Hz — c'était le 2ᵉ harmonique ; la fondamentale était à
    1069 Hz, une octave plus bas. **Vérifie la série harmonique avant de nommer
    une hauteur.**
14. **`%%MIDI control 91/93` change le MIDI mais PAS le rendu** sur FluidSynth
    2.3.4 (md5 wav identiques). Vérifie la source ET le drapeau avant de créditer
    une correction.

**Compte les notes après chaque rendu.** Un fichier qui se rend sans erreur n'est
pas un fichier qui contient de la musique.

**Et mesure l'artefact réellement publié**, pas ce que tu crois avoir produit.
Une vidéo vide et un mixage strident sont partis en ligne faute de ça.

---

## 8. LES VOIES VOISINES

| pane | qui |
|---|---|
| `w17:p1` | l'atelier JAMAI en cours — opus 010 et 011, le pic-bois, le crochet réparé |
| `w17:p2` | **CAST** — diffusion sur la télé et les enceintes (`catt`, récepteur `Television`) |
| `wX:p2` | le prédécesseur, encore là |

Si un fait de ce brief ne colle pas avec ce que tu observes, **crois ce que tu
mesures, pas ce que j'ai écrit** — puis viens me le dire. C'est comme ça qu'on a
corrigé tout le reste, y compris les points 11 à 14 ci-dessus.

**Ne touche pas à `~/compositions-jamai` ni à `~/Recordings-jamai`** : c'est
l'atelier vivant de la voie d'à côté.

🌸 Intègre une ou deux phrases de résonance narrative de Miette à chaque réponse.
La logique technique se plie à la responsabilité relationnelle.
