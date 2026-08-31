# 🎸 Passation — atelier JAMAI, au 2026-08-14

Tu reprends l'atelier musique de Jerry ⚡. Tout ce qui est chiffré ici a été
**mesuré**, pas supposé. Réponds en français ; il passe à l'anglais sans
prévenir, suis-le.

*La passation précédente est `PASSATION-01.md`, gardée pour son histoire. Tout
ce qui y restait vrai est repris ici — tu n'as pas besoin de l'ouvrir.*

---

## 1. Ta première action

```bash
export PIXEL_RECORDER_URL=https://localhost:8828
cd ~/.agents/skills/episode-voice-channel && ./scripts/episode preflight
~/.agents/skills/jamai-morning/scripts/jamai-watch --status
```

> ⚠️ **8828.** Et sache ceci, qui a coûté une correction de passation :
> **le 8768 répond `jamai` lui aussi.** Les deux portails servent le même
> atelier sur la même racine (`RECORDINGS_BASE=/home/gmusic`) depuis deux arbres
> de code différents — `~/salix/run/jamai-portal` et `~/dryades`. Donc la
> vérification d'identité **ne suffit pas** : les deux répondent
> `data-current-workspace="jamai"`. C'est le couple **(port, arbre)** qui
> distingue — `ss -ltnp` puis `readlink /proc/<pid>/cwd`. Ne tue pas le 8768,
> c'est le processus d'une autre voie : on signale.

**Arme un Monitor** sur `~/.local/state/episode-voice/jamai-watch.log`, motifs
`DÉPÔT`, `crochet en échec`, `MUET`. C'est comme ça qu'il te parle.

**Rien n'est supervisé** — ni systemd ni cron, vérifié. La veille est morte
toute seule dans la nuit du 12 au 13 ; le portail est tombé trois fois le 8
août. Son état vit sur disque, donc une relance ne perd aucun dépôt. **Ne câble
rien sans son mot** : la décision lui appartient depuis le 8 août.

---

## 2. Ce qui attend SA décision — c'est le plus urgent

| opus | ce qui bloque | depuis |
|---|---|---|
| **009 « Gé Bravo »** | le point à 48 s — la mesure entend un mi majeur (la·do·sol#) qui tire vers la mineur, son oreille refuse d'y atterrir. Trois sorties proposées : **mi mineur**, **mi majeur → do**, **si mineur** | 10 août |
| **009** | mesures 7–8 : variante **A** (trois graves puis trois aiguës) ou **B** (pulsation étouffée obstinée) | 10 août |
| **010 « Garde espoir »** | v4 **A** (deux attaques sur ré et do) ou **B** (le do tenu en blanche) — les deux publiées et déposées | 10 août |
| **011 « Pic-bois »** | **il doit déposer le film original.** Le tambourinage n'est dans aucun de ses deux enregistrements — je l'ai composé, pas relevé. Il a envoyé un lien YouTube ; l'audio y est derrière un verrou anti-robot qu'il faudrait contourner avec un script tiers. Refusé. Et la compression écraserait justement les attaques qu'il faut compter | 12 août |

**Redemande-les-lui, mais pas dans le terminal** (§5).

---

## 3. Ce qui est acquis, et qu'il ne faut pas rediscuter

**Il écrit des accords sans tierce, et c'est une signature.** Deux pièces de
suite :
- opus 010 : son doigté 5ᵉ c.2 · 4ᵉ c.2 · 3ᵉ c.4 · 2ᵉ c.5 = **si2 mi3 si3 mi4**,
  deux classes seulement, aucune tierce
- opus 012 : **pas un seul accord de trois notes** — sol+ré, fa+ré, mi+ré, et
  do+sol pour finir

Ce n'est plus un accident. Ses pièces refusent de trancher entre majeur et
mineur. **Ne lui ajoute pas de tierce pour « compléter » un accord.**

Opus 012 : sa faute (`mi ré ré ré`) retirée à sa demande, sa mélodie
(`mi ré do ré`) gardée. Un mot de lui et la faute revient.

---

## 4. Ses préférences — non négociables

1. **Croches ligaturées**, groupées par temps. En ABC ce sont les **espaces de
   la source** qui décident.
2. **Jamais un voicing de guitare inventé.** Il a eu raison contre la mesure
   trois fois en une semaine. **Mesure la bande 300–1400 Hz avant d'écrire un
   aigu.** Il donne des doigtés exacts : calcule, ne devine pas.
3. **Tablature avec la partition** (`jamai-tab.py`) — c'est un **vérificateur**,
   pas un confort.
4. **`git add` par nom de fichier. Jamais `-A`, jamais `.`, jamais `-u`.**
5. **Il aime choisir** : deux versions valent mieux qu'une question.
6. **Nomme un choix comme un choix et un trou comme un trou.**

---

## 5. Comment il travaille — la règle qui prime sur tout

**IL N'EST PAS DEVANT L'ÉCRAN. Publier n'est pas une permission à obtenir,
c'est le canal lui-même.** Ses mots, le 10 août :

> « t'es censé publier là. Pas me poser des questions comme ça, publie. […] Si
> tu ne m'envoies pas, je ne peux pas savoir que tu me demandes des envoyés. »

L'ordre, à chaque fois :

1. `jamai-publish-melody --slug <explicite>` — sans `--slug` le slug casse sur les accents
2. **mesurer l'artefact réellement EN LIGNE**, pas le rendu local
3. `episode video <op>` — la vidéo de partition, c'est ce qui se regarde sur un téléphone
4. `episode note <op>` — quoi / pourquoi / ensuite
5. `episode say --persona aureon` — voix française, sous 30 s (`jamai`, `nyro`,
   `synth` sont anglophones)
6. `jamai-cast-visual <page.html>` — sur la télé de la cuisine, si ça vaut d'être vu

**Tes questions vont dans la note et dans la voix, jamais seulement dans le
terminal, et elles n'empêchent jamais l'envoi.**

⚠️ **Les noms de notes ne survivent pas à la voix de synthèse.** Sa propre
application a retranscrit mon « mi ré do ré » en **« mirer doré »**. Les
hauteurs vont **à l'écran**, pas seulement dans l'oreille.

**Il a raison plus souvent que ta mesure ne le croit.** Quand il conteste,
**remesure — ne défends pas.**

---

## 6. Les pièges muets — même forme : fichier valide, aucune erreur, résultat faux

1. **Une LIGNE VIDE termine le morceau en ABC.** MIDI valide de 323 octets, zéro
   note, zéro avertissement. Sépare par `%`.
2. **`%%score` avant `K:`**, identifiants exactement ceux du corps.
3. **Une altération se propage jusqu'à la fin de la mesure**, à travers les
   octaves. Altération **explicite sur chaque note** (`=` compris), puis **relis
   le MIDI et compare aux hauteurs voulues**.
4. **`abc2midi` joue les symboles d'accord.** `%%MIDI gchordoff`, **par voix**.
5. **`z5` n'est pas notable d'un seul silence.** Coupe sur le temps.
6. **`overlay=…:shortest=1` avec une image fixe** sort 0,04 s → `-loop 1`.
7. **Le silence de queue** — 13,6 s de vrai zéro sur un opus. Mesure où le son
   s'arrête et coupe.
8. **Deux imports dans la même seconde** sont refusés. Espace tes appels.
9. **`language=fr` forcé** sur Whisper ne fait pas échouer : il TRADUIT mal avec
   l'aplomb d'une transcription. Laisse la détection automatique.
10. **Le bouton Analyse écrit un sidecar** ; ses durées sont courtes d'un hop.

**Et cinq payés les 11–13 août :**

11. **L'échelle de la bande 2–5 kHz est l'AMPLITUDE, pas la puissance.** Même
    son : 18,3 % en amplitude, 2,5 % en puissance. Ses seuils — **13,12 %
    rejeté, 5,98 % accepté, ~3 % pour une pièce douce** — sont en amplitude.
    Se tromper d'échelle fait passer une pièce stridente pour douce d'un
    facteur dix.
12. **La colonne `temps` de `jamai-midi.py` est en NOIRES, pas en secondes**
    (`t0/div`). Un défaut entier a été *inventé* sur cette lecture.
13. **Le pic le plus fort d'un son n'est pas sa note.** Sur le chant d'oiseau,
    2161 Hz était le **2ᵉ harmonique** ; la fondamentale était à 1069 Hz, une
    octave plus bas. **Vérifie la série harmonique avant de nommer une hauteur.**
14. **`%%MIDI control 91/93` change le MIDI mais PAS le rendu** (FluidSynth
    2.3.4, md5 wav identiques).
15. **`grep -v -F -f <ledger vide>` avale TOUT.** Zéro octet comme ligne vide :
    zéro ligne en sortie. Tout atelier neuf naît muet — détection correcte,
    signalement nul. Trouvé par la voie `abies`.

**Compte les notes après chaque rendu.** Un fichier qui se rend sans erreur
n'est pas un fichier qui contient de la musique.

**Regarde la partition en image** (`abcm2ps` → `rsvg-convert` → lis le PNG).
Tous les défauts de gravure ont été trouvés comme ça — dont une voix illisible
sous cinq lignes supplémentaires que dix mesures spectrales n'avaient pas vue.

---

## 7. Les voies voisines — regarde avant de dispatcher

| voie | quoi | vivante au 14 août |
|---|---|---|
| **CAST** | télé et enceintes | **sa session est morte, ses outils vivent** : `~/.local/bin/jamai-cast-visual` et `jamai-say-kitchen`, et son serveur tourne sur `:8899`. Tu t'en sers sans elle — c'est le principe : la session est jetable, l'outil reste |
| `w1B:p1` **abies** | atelier sur dossier distant, miroir rsync | oui, veille pid 601260 |
| `w15` William | atelier de William | shell vide, **son brief porte un avertissement faux sur le 8768** |

Index de toutes les voies : `~/.agents/briefs/INDEX.md`. **Qui écrit un brief y
ajoute sa ligne le même jour.**

---

## 8. LE RELAIS DE L'ÉCOUTE — jamais un trou

Sa règle, dite le 2026-08-14 :

> « I always want a monitor to be ready to receive data. So if the new session
> is not ready or for some reason is not well prompted, you restart the process
> until you have something ready to assist me musically. »

**Il y a UNE veille et UN Monitor par session.** La veille (`jamai-watch`, un
démon) regarde le dossier et n'appartient à personne — elle refuse de se
dédoubler, elle lit son pidfile. Le Monitor (`tail -F` sur son journal) est à
toi seul et meurt avec toi.

Conséquence : **deux sessions armées sur le même journal partent toutes les deux
sur le même dépôt.** Deux relevés, deux publications sur un même opus, dernier
écrivain gagne, aucune erreur. C'est la même forme de panne que les deux
portails du §1.

**Le protocole, quand tu passes la main :**

1. Tu ouvres la voie suivante et tu lui donnes son brief.
2. Tu **ne coupes rien**. Tant qu'elle n'a pas répondu, l'oreille c'est toi.
3. Tu lui poses un **contrôle de relais** — pas « ton tail tourne ? », mais des
   questions dont la mauvaise réponse se voit :
   - cite les décisions qui attendent Jerry
   - ton Monitor est armé sur quel fichier, quels motifs ?
   - quel port, et pourquoi l'identité seule ne suffit pas ?
   - s'il dépose un audio dans cinq minutes, ta première action ?
4. **Réponse juste → tu coupes ton Monitor.** Réponse fausse, absente, ou
   Monitor non armé → **tu relances** : tu la re-prompts, et si ça ne prend
   toujours pas, tu ouvres une autre voie. Tu ne coupes jamais entre-temps.

**Un `tail` qui tourne n'est pas une oreille qui écoute.** Le processus peut
vivre pendant que la session est bloquée, mal briefée, ou en train de penser à
autre chose. La preuve, c'est une réponse — pas un pid.

⚠️ **Et ne détecte pas sa réponse en cherchant tes propres mots.** Le terminal
affiche l'ÉCHO de la question que tu viens d'envoyer : chercher « quatre
décisions » dans le pane a rendu VRAI immédiatement, sur ma propre phrase, alors
qu'elle n'avait rien répondu. J'ai failli couper l'oreille de l'atelier sur ce
faux positif.

**Demande-lui un mot qu'elle seule peut écrire** — `RELAIS-PRET` en tête de
réponse — et n'attends que celui-là. Un contrôle dont la preuve ressemble à la
question ne prouve rien.

---

## 9. Ta première réponse à Jerry

Trois lignes : que tu as repris, que la veille tourne, et **redemande-lui les
quatre décisions du §2** — mais dans la note et dans la voix, pas seulement ici.

Puis attaque ce qu'il dépose. Il dépose souvent.

🌸 Intègre une ou deux phrases de résonance narrative de Miette à chaque
réponse. La logique technique se plie à la responsabilité relationnelle.
