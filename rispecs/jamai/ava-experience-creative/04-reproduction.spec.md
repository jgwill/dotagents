# 04 — Reproduire, et le système de retour

Sa demande exacte : *« make a plan to reproduce it and set up a feedback
system »*. Deux parties, dans cet ordre.

---

# A. Reproduire

## A.1 — Ce qu'il faut avoir avant de commencer

| pièce | pourquoi | vérification |
|---|---|---|
| ses studios joignables | c'est le canal, pas le terminal | `curl -sk https://ilex:8768/` déclare `data-current-workspace="aureon"` |
| une veille sur **les deux** | il dépose là où ça lui vient | voir `A.2` |
| un registre `mien.txt` | sinon mes propres dépôts me reviennent comme les siens | `~/.local/state/ilex-watch/mien.txt` |
| `abc2midi`, `abcm2ps`, `fluidsynth`, `ffmpeg`, `rubberband` | la chaîne complète | tous présents sur gaia |
| un python avec `numpy` | toute la mesure | `/opt/anaconda3/bin/python3` |

⚠️ `/usr/bin/python3` n'a pas `numpy` ici. Épingler l'interpréteur.

## A.2 — La veille, telle qu'elle doit être

Elle sonde toutes les **75 s**, sur `8768` et `4768` :

1. **`/recordings`** — un fichier n'est signalé que si **sa taille n'a pas
   bougé** depuis la sonde précédente (un `.m4a` en cours d'écriture n'a pas
   d'index `moov` et est illisible) ;
2. **`/api/compositions` puis chaque salle** — clips, textes, images, note.
   Sans ce second volet on rate ses photos et ses textes : ils ne passent pas
   par `/recordings`. C'est l'erreur qu'il a relevée lui-même — *« It's empty.
   It means you're not looking in the right place »* ;
3. **filtre `mien.txt`** — tout ce que j'importe y est inscrit à l'import.

Défaut latent connu, non corrigé : une liste vide et un hôte injoignable sont
traités pareil. Ne mord pas tant qu'un portail a des enregistrements.

## A.3 — Les six temps

Détaillés dans `02`. Résumé opérationnel :

```
1 DÉPÔT        il enregistre ; ne rien lui demander de musical
2 MESURE       avant la première note ; publier le chiffre
3 CONTRAINTE   une contrainte issue de SA mesure, tenue partout
4 VÉRIFICATION relire le MIDI/audio RENDU, jamais l'intention
5 PUBLICATION  dans sa salle, avec les trois blocs de provenance
6 SA RÉPONSE   la remesurer comme une donnée
```

## A.4 — Le gabarit d'une pièce

Chaque générateur est un fichier python autonome qui écrit de l'ABC, dont
l'en-tête porte, **dans cet ordre** :

```
CE QUI EST DE LUI            fichier source + chiffre mesuré
CE QUE LA MESURE IMPOSE      la forme qui en découle
CE QUE JE CHOISIS            « et que tu défais d'un mot »
CE QUI A ÉTÉ ESSAYÉ          les candidats écartés, avec leur mesure
   ET ÉCARTÉ
SA FRONTIÈRE                 ce qui n'est pas sorti, et ce qui a été effacé
```

Puis, systématiquement, après le rendu :

```python
# hauteurs présentes dans SA bande → doit être 0
len([x for x in notes if 45 <= x <= 53])
# hauteurs hors du mode → doit être 0
len([x for x in notes if x % 12 not in MODE])
# stridence : bande 2-5 kHz de la pièce entière
# énergie dans SA bande de chant (116-156 Hz)
```

## A.5 — L'ordre de départ, s'il faut recommencer à froid

1. mesurer sa prise chantée la **plus récente** → la bande à laisser vide ;
2. bâtir un lit qui la respecte, et le publier ;
3. attendre qu'il chante dessus ;
4. mesurer ce qu'il a chanté → sa cellule, son rythme, son mètre ;
5. lui rendre sa cellule dans une pièce ;
6. à partir de là, tout vient de lui.

Le pas 3 n'est pas facultatif. Sans lui, on compose *pour* quelqu'un au lieu
de composer *avec*.

---

# B. Le système de retour

Ce que « feedback system » veut dire ici : un moyen de savoir si la boucle
marche, sans le lui demander.

## B.1 — Les quatre indicateurs, tous mesurables sans lui poser de question

| indicateur | comment | ce qu'il vaut le 16 août |
|---|---|---|
| **motif / bourdon** | s de motif ÷ s de bourdon dans sa prise chantée | parc : 5 s de motif · marche : **101 s** |
| **notes dans le mode** | % des hauteurs de sa prise Songbird dans le champ | 70,3 % → **75,1 %** |
| **respect de sa propre bande** | % de sa prise dans midi 45-53 | **3,3 %** — il se laisse la place seul |
| **rappel de matière** | ses cellules reviennent-elles d'une prise à l'autre | `+3 -8 +5` × 3 ; si/do dans la voix ET les cris |

Les quatre montent quand la boucle tient. Aucun ne demande son avis.

## B.2 — Les signaux d'alarme

| signal | ce qu'il veut dire | ce qu'on fait |
|---|---|---|
| il conteste une mesure | elle est probablement fausse | **remesurer, ne pas défendre** |
| deux pièces partagent figure, instruments et mesure | on se copie soi-même | changer la **forme**, pas la tonalité |
| une pièce dépasse 13,12 % de stridence | l'oreille va la refuser | mesurer chaque timbre, y compris ceux qu'on croit innocents |
| un chiffre trop rond, trop régulier | c'est peut-être l'outil | dégonfler, replier les octaves, relire le rendu |
| il ne répond plus après une publication | il n'a pas trouvé la porte | lui poser une **voix**, pas un texte |

## B.3 — Ce qui a servi de retour aujourd'hui, en pratique

- **une voix d'index** de 2 min 50 quand il a dit « j'ai beaucoup à écouter » ;
- **une leçon parlée** de 2 min 41 sur ce que sa capture donne à la musique ;
- les **notes de composition** — mais elles ont atteint 42 000 caractères et
  ne sont plus lisibles sur un téléphone. **La voix est devenue la porte
  d'entrée, l'écrit est devenu l'archive.** C'est une leçon de canal, pas de
  contenu.

## B.4 — Le rythme de la boucle

Aujourd'hui : dépôt toutes les 10 à 30 minutes, réponse publiée en 5 à 20
minutes. Ce qui a rendu ça tenable :

- la veille signale, je n'ai pas à sonder ;
- chaque générateur est autonome et se relance en une commande ;
- la vérification est scriptée (`/tmp/v.py`, `/tmp/str.py`), pas refaite à la
  main ;
- rien n'attend une validation pour être publié — **publier est le canal**.

## B.5 — Ce qui reste à construire pour que ça tienne sans moi

1. un `verifier.py` unique remplaçant les scripts épars de vérification ;
2. la couche **rythme** de la base de motifs est écrite mais pas encore
   utilisée comme critère de regroupement ;
3. **l'attitude en couleur harmonique** — l'opus 020 utilise le cap pour
   choisir un accord ; rien n'utilise encore l'inclinaison (canaux 7-8) ;
4. le `.sf2` de son instrument — **retenu faute de son mot**, voir loi 11.

🌸 Reproduire ne veut pas dire refaire les mêmes pièces : ça veut dire tenir
la même boucle assez longtemps pour que quelqu'un s'y reconnaisse.
