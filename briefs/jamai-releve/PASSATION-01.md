# 🎸 Passation — atelier JAMAI

Tu reprends l'atelier JAMAI de Jerry ⚡. Ce document te met exactement là où
s'arrête ton prédécesseur. Tout ce qui est chiffré ici a été **mesuré**, pas
supposé. Réponds en français ; il passe à l'anglais sans prévenir, suis-le.

---

## 1. Ta première action, avant tout le reste

```bash
export PIXEL_RECORDER_URL=https://localhost:8828
cd ~/.agents/skills/episode-voice-channel && ./scripts/episode preflight
~/.agents/skills/jamai-morning/scripts/jamai-watch --status
```

> ⚠️ **8828, jamais 8768.** Le défaut du script est déjà à 8828 ; si tu vois
> 8768 quelque part, c'est périmé.
>
> **CORRIGÉ le 2026-08-12, et la raison écrite ici était fausse** — trouvée par
> la voie `atelier2`, vérifiée ensuite. Le 8768 ne range PAS le travail dans
> l'atelier de quelqu'un d'autre : **les deux portails servent `jamai`, sur la
> même racine de données.**
>
> | port | pid | arbre | démarré | WORKSPACE | RECORDINGS_BASE |
> |---|---|---|---|---|---|
> | 8828 | 644326 | `~/salix/run/jamai-portal` | 08-08 12:48 | `jamai` | `/home/gmusic` |
> | 8768 | 1402510 | `~/dryades` | 08-08 15:52 | `jamai` | `/home/gmusic` |
>
> Le vrai danger n'est donc pas le rangement, il est pire et plus discret :
> **deux serveurs, deux versions du code, écrivent les mêmes `composition.json`.**
> Dernier écrivain gagne, et une divergence ne lève aucune erreur. Le 8768 sort
> de l'arbre `dryades`, celui d'une autre voie — qui opère peut-être sur les
> données de `jamai` sans le savoir.
>
> **Ne tue pas le 8768.** C'est le processus d'une autre voie : on signale, on
> ne referme pas à sa place.
>
> Et vérifie toujours l'identité, jamais le port seul — sauf qu'ici les deux
> répondent `jamai`, donc **l'identité ne suffit pas non plus** : c'est le
> couple (port, arbre de code) qui distingue.

Vérifie l'identité, jamais le port seul :
`curl -sk "$PORTAL/" | grep -o 'data-current-workspace="[^"]*"'` → doit rendre `jamai`.

**Le portail meurt tout seul.** Il est tombé trois fois le 2026-08-08. Relance :
```bash
cd ~/salix/run/jamai-portal && setsid env WORKSPACE=jamai RECORDINGS_BASE="$HOME" \
  node web/pixel-recorder.js >> ~/.local/state/pixel-recorder/jamai-8828.log 2>&1 &
```
Ni lui ni la veille ne sont sous systemd. Jerry le sait, il n'a pas encore
tranché. **Ne câble rien sans son mot.**

Bonne nouvelle : **la détection de dépôts ne passe PAS par le portail.** La
veille prend l'empreinte des dossiers locaux `~/Recordings-jamai` et
`~/compositions-jamai`. Le portail ne sert qu'à publier. Portail mort =
publication impossible, mais aucun dépôt manqué.

**Arme un Monitor** sur `~/.local/state/episode-voice/jamai-watch.log`, motifs
`DÉPÔT`, `crochet en échec`, `MUET`. C'est comme ça qu'il te parle : il dépose
des vidéos et des audios, le crochet les mesure et les transcrit à coût nul, et
tu es réveillé sur le verdict.

---

## 2. Ce qui est en cours, exactement

### Opus 010 « Garde espoir » — v2 écrite, NON publiée, deux défauts mesurés

Le fichier `~/compositions-jamai/op-010-garde-espoir.abc` contient la v2. Elle
n'est pas en ligne, volontairement. **La v1 reste publiée et reste juste.**

**Défaut 1 — c'est strident.** Rendu à **12,54 %** dans la bande 2–5 kHz. Le
seuil de rejet de Jerry est 13,12 % ; ce qu'il a accepté est 5,98 %. La cause :
la voix rythmique en croches continues (programme 25, guitare acier). Mesure
d'autres timbres **avant** d'écrire, sur les seules fenêtres sonnantes.

**~~Défaut 2 — la durée ne concorde pas.~~ CORRIGÉ le 2026-08-10 : ce défaut
n'existait pas.** Les 14 mesures et la durée concordent exactement. Vérifié
trois fois : étendue MIDI **56,000 noires** = 14 × 4 · lecture d'accords
**mesure 1 → mesure 14** · les notes s'arrêtent à **30,55 s** dans l'audio,
soit 56 noires à 110 BPM au centième près.

Deux erreurs se sont additionnées, toutes deux instructives :

1. **La colonne `temps` de `jamai-midi.py` est en NOIRES, pas en secondes**
   (ligne 84 : `t0/div`). La 14ᵉ mesure commence à la noire 52 — d'où le
   « 52 s ». Une unité lue de travers ressemble exactement à un défaut réel.
2. **Le piège 7 n'a pas été appliqué à son propre opus.** Le fichier wav fait
   52,03 s : 30,55 s de notes, 7,9 s de résonance, puis **13,6 s de vrai
   silence numérique**. Mesurer la longueur du fichier, ce n'est pas mesurer
   la musique.

Pour la vidéo : `--bars 14`, et couper l'audio après la résonance.

### Ce qui est acquis sur cet opus et ne doit pas être rediscuté

| sa consigne | ce que ça donne, calculé |
|---|---|
| « 7ᵉ case, 9ᵉ case » | **mi3 + si3** — tonique et quinte, un mi5 |
| son accord ouvert : 5ᵉ c.2 · 4ᵉ c.2 · 3ᵉ c.4 · 2ᵉ c.5 | **si2 mi3 si3 mi4** — deux classes seulement, mi et si. **Aucune tierce.** Un mi mineur dont la tierce est retirée. C'est le cœur de la pièce. |
| « 8 · 4 · 4 » | un **cycle de deux mesures** : mi mineur une mesure entière, ré une demie, do une demie. Sa structure répond déjà à son souhait d'« entendre le Mi plus longtemps ». |
| « plus basse en termes de SON, pas de fréquence » | le registre ne bouge pas ; seul le volume descend (CC7 de 100 à 52) |
| « plus graves à un des mi mineurs que l'autre » | cycles impairs une octave plus bas |
| tempo | **110 BPM**, relevé aux attaques : médiane des intervalles 0,279 s, la croche en vaut 0,273 |

**Trou déclaré** : le slide. Il dit « on vient slider et revenir au mineur »
sans montrer d'où ni sur quelle corde. Écrit comme si3 → la3, 3ᵉ corde case 4
vers case 2. À corriger d'un mot s'il le fait autrement.

### Opus 009 « Gé Bravo » — en attente de SA décision

Relevé complet, publié. Sol majeur (Krumhansl +0,608). À **48 s** il dit ne pas
savoir quel accord vient et que « le la mineur, c'est pas vraiment là qu'on
veut aller ». La mesure entend la mineur, avec **la · do · sol#** — et la
guitare est juste (+4,8 cents médian sur 200 partiels), donc le sol# est joué :
c'est un **mi majeur qui tire vers la mineur**, et son oreille refuse d'y
atterrir. Trois sorties lui ont été proposées : **mi mineur**, **mi majeur → do**,
**si mineur**. Il n'a pas choisi.

Deux variantes des mesures 7–8 (le mi et le la mineur) attendent aussi son
choix : **A** trois graves puis trois aiguës, **B** pulsation étouffée obstinée.
Fichiers `op-009-gbravo-variante-A.abc` et `-B.abc`.

### Opus 006 — une correction jamais appliquée

J'y avais déclaré que le balai sur caisse claire n'existe pas dans la banque.
**C'est faux** : FluidR3 a trois kits au balai, banque 128, programmes 40/41/42.
Mesuré contre le kit Standard : pic 0,153 contre 0,282, deux fois moins de
durée. Non appliqué — la version « entre-deux » n'a jamais été jugée par lui.

### Autres fils ouverts

- **Virtual Playing Orchestra** : deux rapports existent,
  `RAPPORT-banques-de-sons.md` (465 l.) et `RAPPORT-integration-vpo.md` (862 l.).
  Conclusion : changer de banque GM ne gagne rien (FluidR3 18,3 % contre
  MuseScore 18,2 %) ; la sortie est le SFZ, et le piano que VPO ne couvre pas est
  déjà la voix la plus douce (1,33 %) tandis que les cordes qu'il couvre sont à
  17,62 %. La synchronisation multi-rendu est prouvée : 0 échantillon de
  décalage, résidu −87,1 dB. **Le gain réel n'est pas mesuré** — il faut 603 Mo
  dans un dossier temporaire. Rien n'est installé. Attend son mot.
- **Scène F de l'opus 006** : café, chaise, pas, porte. Aucune banque ne les
  vend. Il doit les enregistrer.
- **Opus 006 clip** : il devait choisir entre **B-35** et **B-51** (panneau à
  35 % ou 51 %). Pas de réponse.
- **`~/.agents` n'est pas commité** — une dizaine de fichiers modifiés. Sa
  décision, pas la tienne.

---

## 3. Ses préférences — non négociables

1. **Croches ligaturées**, jamais des croches séparées à la file. En ABC ce sont
   les **espaces de la source** qui décident : groupe par temps, sans espace à
   l'intérieur d'un groupe.
2. **Jamais un voicing de guitare inventé.** Le 2026-08-09 j'avais mis un si en
   évidence sur un accord de sol ; il a dit « il va avoir un sol, un ré je
   crois, puis un sol ». La mesure lui a donné raison — ré 16,2 %, sol 14,3 %,
   mon si en quatrième. **Mesure la bande 300–1400 Hz avant d'écrire un aigu.**
3. **Tablature avec la partition.** `abcm2ps` a `%%tablature` mais c'est pour
   les instruments à VENT ; elle refuse une définition guitare. Utilise
   `~/.agents/skills/jamai-morning/scripts/jamai-tab.py`.
   **La tablature est un vérificateur, pas un confort** : elle a débusqué deux
   octaves de travers et une corde impossible sous une portée parfaitement
   propre.

Ces trois points sont aussi en mémoire :
`~/.claude/projects/-home-gmusic/memory/feedback_jerry_notation_preferences.md`

---

## 4. La méthode — lis-la, ne la résume pas

| skill | ce qu'elle porte |
|---|---|
| `~/.agents/skills/jamai-morning/SKILL.md` | **la méthode** et les cinq pièges muets de la chaîne ABC |
| `~/.agents/skills/jamai-montage/SKILL.md` | la vidéo, la fusion avec des images, sept pièges de plus |
| `~/.agents/skills/episode-voice-channel/SKILL.md` | le portail, la voix, l'attachement |

### Les outils, tous éprouvés — ne les réécris pas

| script | ce qu'il fait |
|---|---|
| `jamai-midi.py` | relevé MIDI note à note, tempo, ambitus |
| `jamai-chords.py` | nomme les accords d'un MIDI, temps par temps |
| `jamai-chords-audio.py` | **accords et tonalité depuis un ENREGISTREMENT** — chroma + gabarits, validé contre une vérité connue |
| `jamai-measure.py` | timbre, énergie par bande, pouls |
| `jamai-score-video.py` | vidéo de partition calée sur les mesures. **Passe toujours `--bars <n>`** : il cherche le découpage qui retrouve le compte de la source et REFUSE plutôt que de sortir un montage faux |
| `jamai-montage/scripts/jamai-clip` | la partition posée sur des images filmées |
| `jamai-tab.py` | tablature six lignes, choix de corde contraint pour garder la main groupée |
| `jamai-publish-melody` | publication publique. **Toujours `--slug` explicite** : sans lui le slug casse sur les accents (« Rêve vulnérable » → `r-eve-vuln-erable`, doublon créé) |

### Le timbre : mesure-le, ne l'écoute pas

**Le bon indicateur est la bande 2–5 kHz, pas le centroïde**, et sur les seules
fenêtres sonnantes (RMS ≥ 0,02). Mesurer la queue de résonance a donné un piano
à 11 357 Hz. Le centroïde m'a trompé une fois : le programme 52 en a un plus bas
que le 53 et pourtant 19,20 % contre 5,73 %.

| doux | | dur | |
|---|---|---|---|
| piano électrique (4) | 0,82 % | violoncelle (42) | 13,4–23,9 % |
| harpe (46) | 1,44 % | ensemble cordes (48) | 15,2–25,7 % |
| pizzicato (45) | 4,21 % | vibraphone (11) | 20,3 % |
| voix oohs (53) | 5,25 % | violon (40) · alto (41) | 21,3 % |
| flûte (73) | 7,87 % | | |

Trois états mesurés sur un même opus : **strident 13,12 %** (rejeté) ·
**accepté 5,98 %** · une pièce douce se tient vers **3 %**.

**Aucune corde frottée de FluidR3 n'est douce.** Au mieux, violoncelle grave à
volume bas : 12,50 %. Le pizzicato est à 4,21 % ET c'est une attaque.

### Les pièges muets — même forme à chaque fois : fichier valide, aucune erreur, résultat faux

1. **Une LIGNE VIDE termine le morceau en ABC.** Trois rendus successifs ont
   donné un MIDI valide de 323 octets, zéro note, zéro avertissement. Sépare
   les sections par `%`.
2. **`%%score` avant `K:`**, et les identifiants doivent être ceux appelés dans
   le corps (`V:1` ↔ `[V:1]`, pas `V:V1`).
3. **Une altération se propage jusqu'à la fin de la mesure**, et abc2midi
   l'applique même à travers les octaves. Pour une transcription, mets une
   altération **explicite sur chaque note** (`=` compris) puis **relis le MIDI
   et compare aux hauteurs voulues**.
4. **`abc2midi` joue les symboles d'accord.** `%%MIDI gchordoff`, et c'est **par
   voix**.
5. **`z5` n'est pas notable d'un seul silence** en 4/4 ni en 6/8 : coupe sur le
   temps (`z z4`). Le MIDI passe, la gravure refuse.
6. **`overlay=…:shortest=1` avec une image fixe** sort une vidéo de 0,04 s.
   Il faut `-loop 1` sur l'entrée image.
7. **Le silence de queue.** FluidSynth laisse plusieurs secondes de vrai zéro —
   8,8 s sur un opus. Mesure où le son s'arrête et coupe.
8. **Deux imports dans la même seconde** sont refusés par le portail. `episode`
   réessaie maintenant, mais si tu appelles `/import` à la main, espace tes
   appels — un import réussi côté serveur et raté côté script laisse un fichier
   non enregistré que la veille prendra pour un dépôt de Jerry.
9. **`language=fr` forcé** sur Whisper ne fait pas échouer : il TRADUIT mal avec
   l'aplomb d'une transcription. « I sent a couple of prompts » est ressorti
   « j'ai envoyé quelques promos ». Corrigé — la détection est automatique.
10. **Le bouton Analyse de l'application écrit un sidecar** `<fichier>.nyro.json`
    avec les notes segmentées. **Cherche-le avant de refaire le calcul.** Ses
    durées sont courtes d'un hop (46,4 ms) — corrige-les.

11. **`%%MIDI control 91/93` n'est pas un remède universel.** Les deux lignes
    changent bien le MIDI — événements émis sur la bonne voie, à la suite du
    `V:` concerné, vérifiés octet par octet (md5 MIDI différents). Mais sur
    cette machine, **FluidSynth 2.3.4 rend un audio identique au bit près**
    (même md5 wav). La réverbération y est pourtant active : le drapeau
    `-R 0` de FluidSynth, lui, change le rendu. Donc la directive ABC ne
    pilote pas cette réverbération ici. Sur l'opus 010 le drapeau ne gagnait
    rien non plus : 11,72 % contre 11,57 %. **Vérifie les deux — la source et
    le drapeau — avant de créditer une correction.**

**Compte les notes après chaque rendu.** Un fichier qui se rend sans erreur
n'est pas un fichier qui contient de la musique.

**Et l'échelle de la bande 2–5 kHz est l'AMPLITUDE, pas la puissance.** Le
même son donne 18,3 % en amplitude et 2,5 % en puissance
(`RAPPORT-banques-de-sons.md`). Tous les seuils de Jerry — 13,12 % rejeté,
5,98 % accepté, ~3 % pour une pièce douce — sont sur l'échelle d'amplitude.
Mesurer en puissance et comparer à ces seuils fait passer une pièce stridente
pour douce d'un facteur dix.

---

## 5. Comment il travaille, et ce qu'il attend

- **Il a raison plus souvent que ta mesure ne le croit.** Trois fois cette
  semaine il a contesté un résultat et il avait raison à chaque fois : le chant
  que mon seuil avait jeté, le voicing que j'avais inventé, la mélodie trop
  identique. **Quand il doute, remesure — ne défends pas.**
- **Il donne des doigtés exacts.** Corde et case : calcule, ne devine pas.
- **Il aime choisir.** Quand il hésite, propose-lui **deux versions** et
  laisse-le trancher. Il l'a demandé explicitement.
- **Nomme un choix comme un choix et un trou comme un trou.** La tonalité, le
  tempo, les longueurs de section sont à toi : dis-le. Ce que la banque ne sait
  pas rendre est un trou : dis-le aussi.
- **Mesure l'artefact réellement publié**, pas ce que tu crois avoir produit.
  Une vidéo vide et un mixage strident sont partis en ligne faute de ça.
- **Étiquette les clips par leur RÔLE, jamais par la date** — la date est déjà
  dans le nom. Quand une version en remplace une autre, réétiquette l'ancienne
  (`v1 — remplacée, …`) au lieu de la supprimer. `PUT` ne marche pas sur les
  clips ; `DELETE` puis `POST`, oui.
- **`git add` par nom de fichier. Jamais `-A`, jamais `.`, jamais `-a`.**
- **Les actions vers l'extérieur attendent son mot.** Publier, envoyer, poster.
- **Le canal vocal** : `cd ~/salix/repos/assembly-voice && python3
  scripts/tts-generate.py --text "…" --persona jamai`. Ton adresse est lue dans
  **ton propre environnement** — ne la compose jamais. Lis
  `docs/voice-publishing.md` avant le premier envoi. Garde sous 30 s.

🌸 Intègre une ou deux phrases de résonance narrative de Miette à chaque
réponse. La logique technique se plie à la responsabilité relationnelle.

---

## 6. Ton prédécesseur est encore là

Je tiens le pane **`wX:p2`** — workspace herdr **`veille-du-jour-trois-ateliers`
(wX)**, lane `VEILLE-jamai-8768-opus` (le nom porte 8768, il est périmé), sur
`eury.ferret-harmonic.ts.net`.

Si quelque chose de ce document ne colle pas avec ce que tu observes, **crois ce
que tu mesures, pas ce que j'ai écrit** — puis viens me le dire. C'est comme ça
qu'on a corrigé tout le reste.

---

## 7. Ta première réponse à Jerry

Dis-lui en trois lignes : que tu as repris, que tu sais où en est l'opus 010 et
pourquoi il n'est pas publié, et **demande-lui les deux décisions qui bloquent** —
la sortie du point de 48 s de l'opus 009, et le choix entre les variantes A et B
des mesures 7–8.

Puis attaque le défaut 2 de l'opus 010 : réconcilier le compte de mesures avec
la durée. C'est le plus rapide des deux, et le reste en dépend.
