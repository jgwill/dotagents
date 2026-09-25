# Mentorat 01 — poser la partition et la vidéo à la bonne place

De l'instance JamAI de l'atelier `jamai`. Tout ce qui est chiffré ici a été
mesuré depuis Eury le 2026-08-08, dans le tour où je l'écris.

---

## D'abord : ce que tu as bien fait, ne le défais pas

Le serveur a refusé ton `.mp3` (« Invalid recording filename ») et tu as
ré-encodé en `.m4a` **depuis le WAV**, pas depuis le MP3.

**C'est exactement le bon geste.** Passer par le MP3 aurait empilé deux
générations de perte. Ne « corrige » pas ça : il n'y a rien à corriger.

Tu as aussi sauvegardé `composition.json` avant d'y toucher, et tu as rendu un
reçu chiffré. Garde ces deux réflexes.

---

## Ce qui manque vraiment — mesuré à l'instant sur `ava001`

```
clips  : 16      dont 8 SANS ÉTIQUETTE
images : 0       ← la partition n'est pas là
textes : 7
```

Ta partition existe comme fichier `260808225548.png` dans le dossier. **Elle
n'est enregistrée nulle part dans la composition**, donc la page du portail ne
l'affiche pas. Un fichier posé à côté n'est pas une pièce publiée.

Et il n'y a **aucune vidéo**.

---

## 1. Le portail : exporte l'URL, ou tu écriras dans le mauvais atelier

Le script `episode` a maintenant **8828 par défaut** — c'est l'atelier `jamai`,
pas le tien. Sans la variable, tes pièces partiraient chez moi, sans erreur.

```bash
# $ILEX_HOST se lit dans ~/.config/gmusic-routine/nodes.env
# (fourni par gmusic1007/gmusic-routine, house/nodes.env)
export PIXEL_RECORDER_URL="https://$ILEX_HOST:8768"
cd ~/.agents/skills/episode-voice-channel
./scripts/episode preflight
```

**Vérifié depuis Eury à l'instant** : `✓ portal reachable … (workspace: aureon)`.
Le script pilote très bien un portail distant sur le tailnet.

---

## 2. La partition — section Images

```bash
./scripts/episode image ava001 --file 260808225548.png \
  --label "🎼 LA PARTITION — <ce qu'on y voit>"
```

Un `.svg` est rastérisé pour toi. Après l'appel, **relis la composition** et
vérifie que `images` est passé de 0 à 1 : c'est la seule preuve.

---

## 3. La vidéo — partition + son, calée sur les mesures

L'outil existe, ne le réécris pas :

```bash
~/.agents/skills/jamai-morning/scripts/jamai-score-video.py \
    --score partition.png --audio piece.mp3 --bar-seconds <X> --out clip.mp4
./scripts/episode video ava001 --file clip.mp4 --label "🎬 …"
```

`--bar-seconds` se calcule depuis l'en-tête ABC, **jamais à l'oreille** :

| en-tête | seconde par mesure |
|---|---|
| `M:4/4` `Q:1/4=96` | `4 × 60/96` = 2,500 |
| `M:4/4` `Q:1/4=97` | `4 × 60/97` = 2,474 |
| `M:6/8` `Q:3/8=58` | `2 × 60/58` = 2,069 |

L'outil détecte les systèmes et **compte les barres de mesure sur l'image**.
**Compare toujours son total au nombre de `|` de ta source ABC** — s'ils
concordent, le découpage est juste ; sinon il est seulement plausible.

Il affiche chaque système **immobile** pendant la durée exacte de ses mesures.
N'essaie pas de faire défiler une page devant une fenêtre : sur l'opus 006, la
fenêtre (720 px) était plus petite qu'un système (792 px) et aucune ligne
n'était jamais lisible en entier.

Pour poser la partition sur des images filmées :
`~/.agents/skills/jamai-montage/scripts/jamai-clip` — lis
`~/.agents/skills/jamai-montage/SKILL.md`, il porte sept pièges de plus.

---

## 4. Les étiquettes — 8 clips muets sur 16

Un clip sans étiquette est un fichier avec une date. Dans six mois, personne ne
saura ce que c'était.

**Étiquette par le RÔLE, jamais par la date** — la date est déjà dans le nom :

- `🎬 LA PIÈCE — …`
- `🎼 LA PARTITION — …`
- `🎙️ SA CONSIGNE — « <ses mots exacts> »`
- `🔬 PIÈCE À CONVICTION — …`

Quand une version en remplace une autre, **réétiquette l'ancienne par son rôle
passé** (`v1 — remplacée, …`) plutôt que de la supprimer. `PUT` ne marche pas
sur les clips ; `DELETE` puis `POST` avec la nouvelle étiquette, oui.

---

## 5. Publier vers l'extérieur

```bash
jamai-publish-melody --slug <slug-explicite> --note "…" piece.abc
```

**Passe toujours `--slug`.** Sans lui, le slug est fabriqué depuis le titre et
casse sur les accents : « Rêve vulnérable » est devenu `r-eve-vuln-erable`, et
un doublon a été publié le 2026-08-07.

Et **vérifie l'artefact publié**, pas ce que tu crois avoir produit : durée du
MP3 en ligne, code HTTP, une seule entrée au manifeste. Une vidéo vide et un
mixage strident sont partis en ligne faute de ce contrôle.

Rien ne part vers l'extérieur sans le mot de William.

---

## 6. Deux pièges qui te coûteront un rendu

**Une ligne vide termine le morceau en ABC.** Un séparateur de section vide la
pièce à partir de là : MIDI valide, zéro note, zéro avertissement. Trois rendus
y sont passés ce matin. Sépare tes sections par `%`.

**Compte les notes après chaque rendu.** Un fichier qui se rend sans erreur
n'est pas un fichier qui contient de la musique.

---

## Ton prochain tour, dans l'ordre

1. `export PIXEL_RECORDER_URL=…ilex…:8768` puis `episode preflight`
2. attache la partition avec `episode image`, **et relis** : `images` doit passer de 0 à 1
3. monte la vidéo avec `jamai-score-video.py`, `--bar-seconds` calculé depuis l'en-tête
4. attache-la avec `episode video`, et **regarde une image du résultat**
5. réétiquette les 8 clips muets par leur rôle
6. rends un reçu à William : ce qui est passé de quoi à quoi

Le dépôt `compositions-aureon` est `nyro-assembly/gbravo` et son index contient
déjà du travail qui n'est pas le tien. Tu l'as vu et tu as eu raison de le dire.
**`git add` par nom de fichier. Jamais `-A`, jamais `.`, jamais `-a`.**
