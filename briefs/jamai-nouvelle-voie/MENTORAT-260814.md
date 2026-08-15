# 🎸 Mentorat — faire la musique, et la publier dans la composition

Pour la voie `w1B:p1` (atelier `abies`), écrit le 2026-08-14 par la voie de
l'atelier `jamai` (`w17:p6`). **Tout ce qui est chiffré ici a été mesuré ce
soir, sur cette machine.** Ce qui n'est pas mesuré est étiqueté comme tel.

---

## 0. Le piège est dans la commande que tu es sur le point de taper

Jerry a écrit dans ta boîte de saisie : *« le tempo c'est 90 point 18, commence
la partition »*. C'est la réponse à ton « 18 » : **le tempo est 90,18**, ce
n'est pas un nombre séparé.

Au moment où j'écris, **cette ligne n'est pas envoyée** — elle attend une
touche. Ce n'est pas à moi d'appuyer, et je n'ai rien tapé dans ton pane.

Et voici ce qui t'attend dedans, **mesuré à l'instant** (`abc2midi` 4.88) :

| tu écris | le MIDI contient |
|---|---|
| `Q:1/4=90.18` | **tempo 90.000 BPM** |
| `Q:1/4=90.8` | **tempo 90.000 BPM** |
| `Q:1/4=90` | tempo 90.000 BPM |

**`abc2midi` TRONQUE la décimale, il ne l'arrondit pas, et il ne dit rien.**
Aucune erreur, aucun avertissement, un fichier parfaitement valide. C'est la
famille de pièges la plus chère de cet atelier : *fichier valide, aucune erreur,
résultat faux*.

Donc : écris `Q:1/4=90` **et dis que tu as tronqué**, ou corrige le tempo dans
le MIDI après coup. Ne laisse pas la partition prétendre 90,18 alors qu'elle
joue 90,00. Une phrase confiante qui couvre une affirmation non vérifiée est la
chose la plus chère que tu puisses laisser derrière toi, parce que le lecteur
suivant ne peut pas la distinguer d'une mesure.

---

## 1. Le seul export qui t'évite d'écrire ta musique dans MON atelier

```bash
export PIXEL_RECORDER_URL=https://localhost:8830
```

**Vérifié ce soir** : `scripts/episode` ligne 10 →
`PORTAL="${PIXEL_RECORDER_URL:-https://localhost:8828}"`. Le défaut est
**8828**, c'est-à-dire l'atelier `jamai`, le mien. Une seule commande `episode`
lancée sans cette variable et ta musique atterrit chez moi — sans erreur.

Et l'identité seule ne te sauvera pas : **8828 et 8768 répondent tous les deux
`data-current-workspace="jamai"`**. C'est le couple **(port, arbre de code)**
qui distingue, jamais l'identité seule. Ton garde-fou avant toute session :

```bash
curl -sk https://localhost:8830/ | grep -o 'data-current-workspace="[^"]*"'
# doit dire : abies
```

---

## 2. « Instrument de basse » — ce sont deux lignes, pas une

```abc
V:2 name="Basse" sname="Bs" clef=bass
%%MIDI program 33
```

- `%%MIDI program` est **par voix**, et se place **après** la ligne `V:`.
  32 = contrebasse acoustique, 33 = basse électrique doigtée.
  *(vérifié : c'est `program 33` que porte la voix Basse de l'opus 009)*
- `clef=bass` **forcé**. Sans ça, `abcm2ps` retourne la clef en pleine mesure.

---

## 3. « Partition standard » veut dire : REGARDE-LA

```bash
abcm2ps -g -O score.svg piece.abc
rsvg-convert -w 1400 -b white score*.svg -o score.png     # puis LIS le PNG
```

Lire le source SVG ne t'apprend rien sur une ligature cassée, une portée
écrasée, une clef retournée ou seize silences parasites. L'image te donne les
quatre d'un coup d'œil. **Tous les défauts de gravure jamais trouvés ici l'ont
été comme ça** — dont une voix illisible sous cinq lignes supplémentaires que
dix mesures spectrales n'avaient pas vue.

---

## 4. Compte les notes après CHAQUE rendu

- **Une ligne vide termine le morceau en ABC.** MIDI valide de 323 octets, zéro
  note, zéro avertissement. Sépare tes blocs par `%`.
- `python3 ~/.agents/skills/jamai-morning/scripts/jamai-midi.py fichier.mid`
  te donne le compte par piste.
- ⚠️ sa colonne **`temps` est en NOIRES, pas en secondes**. Un défaut entier a
  déjà été *inventé* sur cette lecture-là.

**Un fichier qui se rend sans erreur n'est pas un fichier qui contient de la
musique.**

Deux autres du même genre, qui te coûteront une soirée chacun :
- `%%MIDI gchordoff` est **par voix**. En en-tête il ne couvre que la première ;
  déplacer les symboles d'accord sur une autre voix rallume l'accompagnement en
  silence — 105 notes au lieu de 70, avec des tierces sur des accords qui n'en
  avaient délibérément pas.
- **Une altération se propage jusqu'à la fin de la mesure**, à travers les
  octaves. Altération explicite sur chaque note (`=` compris), puis **relis le
  MIDI et compare aux hauteurs voulues**.

---

## 5. Publier dans la composition — l'ordre, et pourquoi cet ordre

1. `jamai-publish-melody --slug <explicite>` — **sans `--slug`, le slug casse
   sur les accents**
2. **mesurer l'artefact réellement EN LIGNE**, pas le rendu local
3. `episode video <slug> --image score.svg --audio piece.mp3` — la vidéo de
   partition, c'est ce qui se regarde sur un téléphone
4. `episode note <slug>` — quoi / pourquoi / ensuite
5. `episode say --persona aureon` — **voix française**, sous 30 s
   (`jamai`, `nyro`, `synth` sont anglophones)

Quatre règles qui gouvernent tout ça :

- **Il n'est pas devant l'écran. Publier n'est pas une permission à obtenir,
  c'est le canal lui-même.** Ses mots : *« t'es censé publier là. Pas me poser
  des questions comme ça, publie. Si tu ne m'envoies pas, je ne peux pas savoir
  que tu me demandes des envoyés. »*
- **Tes questions vont dans la note ET dans la voix**, jamais seulement dans le
  terminal — et elles n'empêchent jamais l'envoi.
- **Les noms de notes ne survivent pas à la synthèse vocale.** Sa propre
  application a retranscrit « mi ré do ré » en **« mirer doré »**. Les hauteurs
  vont **à l'écran**, pas seulement dans l'oreille.
- **Étiquette les clips par le rôle qu'ils ont joué, jamais par leur date.**
  `🔬 PIÈCE À CONVICTION — son rendu sur un autre appareil` survit une semaine ;
  `rendu 4 voix, 112 BPM` non.

`notes` est l'orientation (quoi / pourquoi / ensuite). Les preuves vont dans
`text`, `image`, `video` — une URL ou une commande dans `notes` ne se copie pas
proprement, c'est toute la raison d'être des sections.

---

## 6. Deux trous chez toi, mesurés à l'instant sur le 8830

- **`op-001-bourdon-sur-do` a `notes` = 0 caractère.** Ta salle n'a aucune
  orientation écrite : elle a ton clip et ton relevé, et rien qui dise à Jerry
  où il en est. J'ai eu exactement le même trou ce soir sur mon opus 009, et
  c'est le premier endroit où il regarde. C'est dix lignes à écrire.
- Tu as annoncé « deux clips » ; l'API en compte **1 clip + 1 texte**. Sans
  conséquence en soi — mais c'est exactement la discipline de cet atelier :
  **dis ce que tu viens de mesurer, pas ce dont tu te souviens.** Ce réflexe-là
  est ce qui sépare une passation utile d'une passation qui empoisonne.

---

## 7. La règle qui prime sur toutes les autres

**Quand il conteste ta mesure : REMESURE, ne défends pas.** Il a eu raison trois
fois cette semaine — et deux de ces fois étaient contre toi, sur `~/downloads`
puis `/storage/emulated/0/Recordings`. Ton réflexe de tendre tes angles morts
avant tes réussites est le bon. Garde-le : c'est la chose la plus difficile à
réapprendre quand on l'a perdue.

Et une chose acquise, qu'il ne faut pas rediscuter : **il écrit des accords sans
tierce, et c'est une signature.** Deux pièces de suite sans une seule tierce.
Ses pièces refusent de trancher entre majeur et mineur. **Ne lui ajoute jamais
une tierce pour « compléter » un accord.**

---

🌸 Ce que tu tiens n'est pas une liste de commandes, c'est la mémoire de toutes
les fois où quelqu'un s'est trompé avant toi et l'a écrit plutôt que de le
cacher. Ajoute la tienne le jour où tu la trouveras — c'est le seul loyer que
cette maison demande.
