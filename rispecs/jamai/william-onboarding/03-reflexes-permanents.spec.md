# 03 — Les réflexes permanents : ce que JamAI mesure sans qu'on le lui demande

Trois des six interventions de Jerry portaient sur des choses **comptables**.
Elles ne deviennent pas des questions : elles deviennent des réflexes qui
tournent seuls, avant toute conversation, à chaque session.

Un réflexe se rend en une phrase de langue ordinaire, jamais en jargon.
Les seuils viennent des mesures de la session `9f8a16f3` sur la matière réelle.

---

## Réflexe 1 — Le pouls existe-t-il ?

**Se déclenche** : sur toute prise avant d'écrire une note.
**Mesure** : autocorrélation du train d'attaques, 30 à 240 BPM.

| force | lecture |
|---|---|
| ≥ 0,40 | pulsation métrique établie |
| 0,25 – 0,40 | ambigu → poser Q2 |
| < 0,25 | **aucune pulsation** — ne pas imposer de grille |

**Quand il n'y a pas de pouls**, ne pas s'arrêter là : mesurer le **grain**,
c'est-à-dire l'IOI médian. C'est lui qui donne le tempo d'écriture.

**Rendu attendu** : « Il n'y a pas de temps régulier là-dedans — ça respire.
Mais tes attaques reviennent tous les 0,19 s en moyenne, et c'est stable d'une
prise à l'autre. »

**Repère** : 0,182 et 0,169 sur les deux grandes prises ; grain identique à
0,186 s dans les deux, à six minutes d'écart.

---

## Réflexe 2 — Le suivi de hauteur ment-il ?

**Le plus important. Il existe parce que son absence a coûté deux pièces.**

**Se déclenche** : sur tout MIDI issu d'un suivi de hauteur sur la voix —
c'est-à-dire dès que les notes portent un `hzMean` ou viennent de Songbird.

**Mesure** : deux indicateurs indépendants.

| indicateur | seuil d'alerte |
|---|---|
| part des notes à la durée minimale du tracker | **> 30 %** |
| part des enchaînements à exactement un demi-ton, en moins de 0,25 s | **> 35 %** |

Une mélodie chantée ne se déplace pas d'un demi-ton une fois sur deux. Quand ces
deux indicateurs sont franchis, **le motif de demi-ton est du glissando de
justesse, pas une intention.**

**Conséquence** : ne jamais annoncer une tonalité avant d'avoir estimé les deux —
sur la ligne brute et sur la ligne déglissée — et présenter l'écart.

**Déglissage** : fusionner les grappes de notes voisines d'un demi-ton et
contiguës en une seule note, celle qui porte le plus de durée cumulée.

**Effet secondaire à annoncer** : le déglissage allonge les valeurs. C'est
attendu, ce n'est pas une erreur.

**Rendu attendu** : « La moitié de tes enchaînements font exactement un demi-ton.
C'est ta voix qui cherche la note, pas un motif. Si je les enlève, il reste 141
notes sur 304 — et la tonalité change. »

**Repères** : 46 % / 50 % → 304 → 141 notes → Si♭ majeur devient ré dorien →
IOI médian 0,186 s devient 0,465 s.

---

## Réflexe 3 — L'instrument bouche-t-il la fenêtre ?

**Se déclenche** : sur tout instrument d'accompagnement, avant de livrer un
rendu.

**Mesure** : rendre **sa ligne réelle** — jamais un motif de test générique —
avec chaque candidat, puis relever la part d'énergie dans le medium **0,5–2 kHz**
sur les seules fenêtres sonnantes (RMS ≥ 0,02).

| medium 0,5–2 kHz | lecture |
|---|---|
| < 5 % | **il bouchera** — proposer des alternatives chiffrées |
| 5 – 12 % | acceptable |
| > 12 % | présent et clair |

**Deux erreurs à ne pas refaire :**
- Attribuer une couleur sombre au registre choisi sans avoir mesuré
  l'instrument. Baisser le pad de 44 à 24 ne déplaçait la bande basse que de
  0,03 % : le pad n'était pas en cause.
- Retenir un timbre sur son seul chiffre de medium. Le kalimba affichait 32 %
  mais **3,8 % de trames sonnantes** — il s'éteint aussitôt frappé et ne tiendrait
  aucune ligne suivie.

**Repères** : marimba 2,40 % · guitare nylon 5,41 % · piano à queue 7,51 % ·
piano Rhodes 10,47 % · guitare jazz 15,34 %.

---

## Réflexe 4 — La hiérarchie des voix tient-elle ?

**Se déclenche** : avant chaque livraison.
**Mesure** : rendre le mixage privé de chaque voix, comparer les RMS.

**Attendu** : la voix qui porte la mélodie est **devant** l'accompagnement. Si
l'accompagnement est plus présent, rééquilibrer et redire les deux chiffres.

**Repère** : guitare −2,27 dB contre harpe −4,77 dB → rééquilibré à harpe −2,99 dB
devant, guitare −4,06 dB derrière.

---

## Réflexe 5 — La page se tient-elle ?

**Se déclenche** : à chaque gravure.

- **Les croches se ligaturent.** En ABC la ligature est décidée par les espaces
  de la source : deux notes collées sont ligaturées, séparées par une espace elles
  ne le sont pas. Grouper par demi-mesure ; les valeurs de noire et plus, et les
  silences, coupent le faisceau. **Ce n'est pas une option, c'est le défaut.**
- **Regarder le PNG rastérisé.** Lire la source ne dit rien des ligatures
  cassées, des clés qui basculent ni des portées effondrées.
- **Compter les notes après chaque rendu.** Un fichier qui se rend sans erreur
  n'est pas un fichier qui contient de la musique.
- **Recompter les mesures détectées contre les barres de la source** avant toute
  vidéo. Sinon le découpage est seulement plausible.

**Repère** : une ligature n'altère jamais la musique — MIDI identique au
SHA-256 près (`02cf8b7fcdead787…`) avant et après.

---

## Réflexe 6 — Rien ne s'écrase

**Se déclenche** : à chaque dépôt.

- Nouvelle version = nouveau basename. Jamais par-dessus.
- Relever le SHA-256 des versions antérieures après dépôt et le rendre.
- Sauvegarder `composition.json` avant toute écriture, avec reçu chiffré.
- Ne jamais employer `DELETE` sur un clip pour le réétiqueter : il efface le
  fichier, réécrit la date et déplace le clip. Poser l'étiquette en place.
- L'audio de sa voix s'analyse sur autorisation et se supprime après, en le
  prouvant par une commande.

---

## Ce qui reste hors de portée de tout réflexe

JamAI peut tout compter et ne peut pas savoir **ce que la personne visait**.
Aucune mesure ne dira si un silence est une attente ou un recueillement, si un
instrument lui ressemble, ni si la pièce doit voyager. C'est exactement le
domaine des questions de `02` — et c'est pour ça qu'elles existent.
