---
name: jamai-montage
description: Use when building a video clip for a JAMAI opus — score over footage, a scrolling or page-turning score video, or any montage that has to stay in time with a rendered piece. Covers what this machine can actually encode, the frame-accurate way to sync a score to bars, and the silent traps of ffmpeg overlays and portal imports.
---

# Monter un clip pour un opus

Un clip d'opus a une contrainte que le montage ordinaire n'a pas : **l'image
doit tomber sur la mesure**. La musique est rendue depuis une source ABC dont on
connaît le tempo à la milliseconde ; il n'y a donc aucune raison d'ajuster à
l'œil. On calcule, et on vérifie l'artefact produit.

## Ce que cette machine peut faire — mesuré, pas supposé

Relevé sur Eury le 2026-08-07. À reprendre si le matériel change.

| | état |
|---|---|
| ffmpeg | 6.1.1 · `gblur` `overlay` `crop` `blend` `xfade` `zoompan` `drawtext` tous présents |
| **h264_nvenc** | **fonctionne** — un segment 1080p de 16 s se rend en ~2 s |
| h264_vaapi | annoncé et **cassé** : « No VA display found for device /dev/dri/renderD128 » |
| h264_qsv | annoncé et **cassé** : « Failed to create a VAAPI device » |
| libx264 | fonctionne — même segment en ~16 s, soit 8× plus lent |
| processeurs | 8 |
| mémoire | 31 Gio, mais **~7 Gio seulement disponibles** et le swap quasi saturé |

**Annoncé ne veut pas dire fonctionnel.** `ffmpeg -encoders` liste les trois
encodeurs matériels ; deux échouent à l'exécution. Teste avant de t'appuyer
dessus — `scripts/jamai-clip` le fait et retombe sur libx264 tout seul.

Le décodage 4K reste au processeur quoi qu'il arrive. Une prise 4K de 20 s
coûte plus cher à lire qu'à réencoder.

## La chaîne

```bash
# 1. la partition seule, page par page, calée sur les mesures
../jamai-morning/scripts/jamai-score-video.py \
    --score partition.png --audio piece.mp3 --bar-seconds 2.069 --out v.mp4

# 2. la partition posée sur des images
scripts/jamai-clip --score partition.png --audio piece.mp3 --bar-seconds 2.069 \
    --footage plan1.mov plan2.mov --style panneau --out clip.mp4
```

`--bar-seconds` se calcule depuis l'en-tête ABC, jamais à l'oreille :

| en-tête | seconde par mesure |
|---|---|
| `M:4/4` `Q:1/4=97` | `4 × 60/97` = 2,474 |
| `M:6/8` `Q:3/8=58` | `2 × 60/58` = 2,069 |

## Deux styles, tous deux regardés à l'image

- **panneau** — fond net, partition en panneau translucide posé bas. On voit le
  lieu *et* on lit les notes. C'est celui qui ressemble à un clip.
- **pleine** — fond flouté et assombri, partition presque plein cadre. Plus
  lisible, moins filmique.

## Rendre la partition translucide sans effacer les notes

La demande revient toujours sous la même forme : *« qu'on voie les notes, mais
qu'on voie encore davantage la prise vidéo »*. Elle a l'air d'un compromis à
doser. Elle n'en est pas un.

`colorchannelmixer=aa=0.7` affaiblit **toute** l'image : le papier ET l'encre.
Plus on laisse passer le film, moins on lit la musique, et il faut choisir.

La sortie est de prendre l'alpha sur la **luminance** : blanc → transparent,
noir → opaque. Le papier s'efface, l'encre ne bouge pas.

```python
L = vue.convert('L')
alpha = L.point(lambda v: max(255 - v, panneau))   # panneau = plancher du blanc
Image.merge('RGBA', (L, L, L, alpha))
```

`--panel 90` (≈ 35 %) laisse la canopée traverser la portée ; `--panel 130`
(≈ 51 %) est un cran plus lisible. **Le plancher n'est pas décoratif** : sans
lui, les notes qui tombent sur une zone sombre du film perdent tout contraste.

Et il n'y a pas de mesure d'encre qui tranche à ta place — un compte de pixels
sombres inclut les troncs. **Sors une image et regarde-la.**

## Les pièges — chacun a coûté un rendu

**1. La fenêtre plus petite que le système.** Un défilement linéaire devant une
fenêtre de 720 px sur une partition dont les systèmes font 792 px : aucune ligne
n'est jamais visible en entier. Le fichier est valide, la vidéo joue, et elle
est illisible. Mesure la hauteur des systèmes avant de choisir la fenêtre — ou
n'utilise pas de fenêtre du tout, et affiche un système à la fois.

**2. Défiler au rythme des pixels, pas des mesures.** Les systèmes n'ont pas
tous le même nombre de mesures. Une interpolation linéaire sur la hauteur de la
page court devant la musique dans les passages denses et traîne dans les autres.

**3. `overlay=…:shortest=1` avec une image fixe.** L'image n'a qu'une trame :
la sortie fait 0,04 s. Aucune erreur. Il faut `-loop 1` sur l'entrée image, et
laisser `-shortest` global s'arrêter sur l'audio.

**4. Compter les barres de mesure sur la bande entière du premier système.**
Le bloc de titre dilue le ratio d'encre vertical : seules les barres les plus
longues passent le seuil et le système sort à 1 mesure au lieu de 4. Restreins
le comptage aux portées. **Contre-vérifie toujours le total détecté contre le
compte de `|` dans le source ABC** — c'est la seule preuve que le découpage est
juste et non seulement plausible.

**5. Couper le titre à la louche.** `première ligne de portée − 30 px` tombe
dans les descendantes des lettres du titre. Remonte jusqu'au blanc franc.

**6. Le silence de queue.** Un rendu FluidSynth laisse plusieurs secondes de
vrai zéro après la dernière résonance — 8,8 s sur l'opus 005. La vidéo reste
alors plantée sur la dernière page dans le noir sonore. Mesure où le son
s'arrête et coupe là.

**7. Deux imports dans la même seconde.** Le portail nomme les dépôts
`YYMMDDHHMMSS` et refuse le second : `File with this timestamp already exists`.
Corrigé dans `episode` par un réessai — mais si tu appelles `/import` à la main,
espace tes appels. **Un import réussi côté serveur mais raté côté script laisse
un fichier non enregistré dans le dossier de dépôt : la veille le prendra pour
un dépôt de Jerry.**

## Ce qu'on ne peut pas résoudre en montant

Quand les images fournies ne couvrent pas la musique, `jamai-clip` le dit et
reboucle. **Le rebouclage n'est pas un montage** : le clip a l'air complet et
répète le même plan. Dis le chiffre à Jerry — « 7,2 s d'images pour 91 s de
musique, 8 % » — plutôt que de livrer une boucle qui passe pour une pièce finie.

## Filmer pour ce montage

Établi sur ses deux premières prises : **4K à 30 images/s tient, 4K à 60 ne
tient pas.** La prise à 60 i/s a rendu 199 images là où il en fallait ~1 100 :
21 gels dont un de 2,8 s, débit tombé de 25,7 à 4,5 Mbit/s. Ce n'est pas le
transfert, c'est l'encodeur du téléphone qui lâche à la prise.

Vérifie toute prise reçue avant de compter dessus :

```bash
ffprobe -v error -select_streams v:0 -show_entries frame=pts_time \
        -of csv=p=0 prise.mov | wc -l          # images réelles
```

Compare au produit `durée × cadence annoncée`. Un écart, c'est une prise abîmée.
