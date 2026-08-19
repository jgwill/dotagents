# 03 — Les onze lois, et ce que chacune a coûté

Chaque loi ci-dessous a été payée par une erreur commise le 16 août 2026, ou
par une mesure qui a contredit une supposition. Aucune n'est théorique.

---

## Loi 1 — Une unité non déclarée ne s'invente pas

**Coût.** J'ai écrit « m/s² » partout dans l'opus 017 comme si je le savais.

**Ce qui l'a défaite.** Son propre Landbase Movement Studio expose un registre
d'honnêteté par prise : le champ `channel semantic map` est **absent**, et sa
note dit ce qu'il *dirait* — « accel g ×3 · rotation rad/s ×3 · attitude rad
×3 ». Personne ne sait donc si c'est des g ou des m/s².

**La loi.** Écrire les nombres **sans unité** tant que la carte sémantique
n'existe pas. La musique n'en souffre pas : densité et nuances viennent de
**rapports**, pas de grandeurs absolues.

---

## Loi 2 — Le capteur est sur le ventre, pas sur le pied

**Coût.** J'ai écrit « le temps de ton corps qui avance », en pensant à la
marche.

**Ce qui l'a défaite.** Le même registre : `sensor placement` — « lives in
prose only: **phone worn on the belly** ».

**La loi.** Ce que le mouvement compte, c'est son souffle et son torse. Un
opus qui suit ce signal suit sa respiration, pas ses pas. Le dire ainsi.

---

## Loi 3 — Une cadence demandée n'est pas une cadence reçue

**Coût.** 28 attaques détectées, régulières, espacées de 120-133 ms.
Crédibles. **Fausses.**

**La mesure.** Prise à 100 Hz : 1627 paquets, dont **1232 répètent la valeur
précédente — 76 %**. Valeurs neuves : 395, soit **23,8 Hz réels**. Les 28
attaques traçaient l'escalier des valeurs tenues, pas le corps.
À 10 Hz, ses prises avaient **zéro** répétition : le capteur suivait.

**La loi.** Dégonfler avant d'analyser :
```python
neufs = [P[0]] + [P[i] for i in range(1,len(P)) if P[i]['values'] != P[i-1]['values']]
```
Et retenir le chiffre : **×10 de cadence = ×2,4 d'information**.
Une cadence tenue est invisible dans les statistiques par canal du
`summary.json` — min, max et moyenne sont identiques. Elle n'apparaît qu'en
comparant les vecteurs consécutifs.

---

## Loi 4 — Une tessiture mesurée hier ne prédit pas celle d'aujourd'hui

**Coût.** Le premier lit d'Ava 2 laissait vide **ré3-si3** (midi 50-59),
parce que la piste d'Ava 1, du 9 août, y passait 81,5 % du temps.

**La mesure.** Le 16 août, au parc, assis, enroulé dans sa couverture : sa
médiane est **do3**, et **53,7 %** de son temps tenu tombe dans **midi 46-49**
— les quatre demi-tons qui séparaient ma basse de la bande réservée.
**Il chantait pile dans l'interstice.**

**La loi.** Mesurer la bande à protéger sur la prise **la plus récente**. Et
se méfier autant du trou entre deux couches que d'une couche mal placée :
c'est exactement là qu'il est allé.

---

## Loi 5 — L'autocorrélation saute les octaves

**Coût.** J'ai annoncé que sa voix tenait un **si4** 10 % du temps, et j'ai
réservé le registre 69-73 pour lui.

**La mesure.** Sur les 1301 trames détectées vers 494 Hz, l'énergie à **f/4**
— son si2 — est **5,33 fois plus forte**, dans **86 %** des cas. Le si4
n'existe pas.

**La loi.** Replier les octaves avant de conclure, et vérifier une détection
haute en comparant l'énergie à f, f/2 et f/4. Après repli : **94,1 % de sa
voix entre la2 et mi3**, rien au-dessus.

---

## Loi 6 — Séparer le chant de la parole, sinon on mesure la parole

**Coût.** Une première mesure donnait 46,4 % de sa voix sous midi 49 — en
réalité surtout sa voix **parlée**.

**La loi.** Ne garder que les **notes tenues** : au moins 200 ms sans bouger
de plus d'un demi-ton, après lissage médian sur 5 trames. Sur 271 s de prise,
cela isole 74 s de chant. Vérifier la stabilité du résultat sur plusieurs
seuils (160 à 300 ms, ±60 à ±100 cents) avant de publier un chiffre.

---

## Loi 7 — Le rendu ment, et il ment en silence

**Coût.** Quatre fois en une journée.

| ce qui semblait juste | ce que le rendu disait |
|---|---|
| altérations ABC implicites | sa note la plus grave sortait à **42 au lieu de 41** |
| `%%MIDI beat` pour les nuances | vélocités **80-105** au lieu de 40-112 |
| `Q:1/4=136` posé seul dans le corps | **aucun changement de tempo** — il faut le champ EN LIGNE `[Q:...]` |
| `-c copy` vers un conteneur `.m4a` | fichier de **0 octet** : l'audio est en **opus**, refusé par le conteneur ipod |

**La loi.** Relire le MIDI et l'audio **rendus**. Pour une ligne chromatique,
écrire l'altération explicite sur **chaque** note, bécarre compris.

---

## Loi 8 — Le timbre se choisit sur mesure, et la source du brillant surprend

**Coût.** À 27,07 % de stridence sur l'opus 023, j'ai accusé le charley.

**La mesure.** Baisser la batterie à 55 : **28,52 %**. La retirer :
**28,73 %**. Ça monte. La source était la **dent de scie** du lead.
Neuf candidats mesurés, calliope retenue à **11,30 %**.

**La loi.** Mesurer la bande 2-5 kHz de la **pièce entière** pour chaque
candidat, et mesurer aussi l'énergie **dans sa bande de chant** — les deux
critères ne classent pas pareil. Exemple : la harpe est la plus douce
(2,28 %) et la pire chez lui (5,22 %).

Seuils hérités de Jerry : **> 13,12 % rejeté · ≤ 5,98 % accepté · ≤ 3 % doux.**
Un multi-voix atteint rarement 5,98 % ; le dire plutôt que de tricher.

---

## Loi 9 — Assembler demande de rogner et d'égaliser d'abord

**Coût.** La première couture de la chanson de dix minutes tombait dans un
silence de fin de rendu : rapport de niveau **141**.

**La loi.** Avant tout fondu enchaîné : rogner les silences (`silenceremove`
en tête et en queue), puis amener chaque pièce à un **RMS cible commun**
(0,030 ici), plafonné par la crête. Après quoi les cinq coutures tenaient
entre **1,02 et 1,27**.

---

## Loi 10 — Un nom d'hôte dans une URL ne prouve pas qu'on a atteint cet hôte

**Coût, deux fois.** `localhost:8768` sur gaia n'est pas `ilex:8768`. Puis
`https://ilex:8790` a répondu « Forest Conductor » — c'était le service de
**gaia**, lié sur `0.0.0.0:8790`, parce que le port 8790 n'était pas déclaré
dans `peers.conf` et que le nom résolvait vers la voie de bouclage.

**La loi.** L'identité fiable est le triplet **(hôte, port, arbre de code)**.
Pour tout port non déclaré dans la passerelle, vérifier **depuis la machine** :
`ssh ilex 'curl http://127.0.0.1:<port>/'`.

---

## Loi 11 — Ne pas transcrire, publier ni convertir sa voix sans son mot

**Ce qui l'a établie.** Ses deux frontières, posées par lui :

- 8 août — « I don't consent that my voice and my original recording goes
  outside of the boundary here. […] The actual MIDI […] file that was
  recorded. »
- 16 août — « it's really a great privilege to use this sound, **nobody is
  authorized to use it without my consent**. »

**La loi.** Le MIDI est la part offerte ; la voix ne l'est pas. Déclencher une
transcription envoie son audio à un service tiers : c'est son geste, pas le
mien, même s'il le fait lui-même dix fois par jour. **Un oui donné pour une
pièce n'est pas un oui pour la suivante.** Ramener une copie pour analyse est
permis ; l'effacer au `shred` après usage fait partie de la permission.

Ce qui a été **refusé de moi-même** faute de son mot : un SoundFont `.sf2` de
son instrument d'aigle — un format fait pour circuler — et toute publication
web.

---

🌸 Onze lois, onze erreurs. Ce n'est pas un catalogue de fautes : c'est ce
qu'il reste quand on choisit de remesurer au lieu de se défendre.
