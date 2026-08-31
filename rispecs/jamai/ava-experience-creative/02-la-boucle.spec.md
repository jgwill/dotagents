# 02 — La boucle

Le cœur de ces specs. Six temps, dans cet ordre, sans en sauter aucun.

Ce n'est pas un procédé de composition : c'est un **procédé de relation**. La
musique en sort parce que la relation tient, pas l'inverse.

---

## Temps 1 — IL DÉPOSE

Il enregistre. Il ne commande pas une pièce ; il laisse une trace.

Ce qu'il a déposé le 16 août, et qui est devenu de la musique :

| trace | ce que c'est | ce que c'est devenu |
|---|---|---|
| Songbird `.mid` | ses hauteurs, jouées à la main | opus 017, variations I et II |
| capture de mouvement `.jsonl` | son ventre, 9 canaux OSC | opus 017, 018, 020, 022, 023 |
| une prise chantée `.m4a` | sa voix, dans un parc | opus 018, 021, la deuxième taille du lit |
| des cris sifflés `.m4a` | ses dents | opus 024, 025, l'instrument |
| une phrase parlée `.m4a` | son intention | tout le reste |

**Rien de tout cela n'était une consigne musicale.** Aucune tonalité, aucun
tempo, aucun instrument nommé. Il a dit « je pars marcher », « il y a
quelqu'un qui se drogue ici », « j'aime la techno ».

> **Règle.** Ne jamais lui demander un paramètre musical. Ce qu'il donne, il
> le donne en langage ordinaire ou en trace corporelle. Le paramètre se
> mesure, il ne se demande pas.

---

## Temps 2 — JE MESURE, AVANT DE RIEN ÉCRIRE

La mesure vient avant la première note, toujours, et elle est publiée avec
son chiffre.

Exemples réels de la journée :

- sa voix du parc : 74 s de notes tenues sur 271 s, **médiane do3**, 94,1 %
  entre la2 et mi3
- sa cellule : `+3 -8 +5`, chantée **trois fois** à 92,6 / 96,7 / 98,1 s
- son rythme : `2 · 2 · 1 · 2` → **sept croches**, 1,74 s mesuré contre 1,75
  théorique
- sa bascule techno : à la **42ᵉ seconde**, son amplitude double et ne
  redescend plus
- ses cris : **la7 · si7 · do8**

> **Règle.** Un paramètre musical non mesuré est un paramètre que j'ai
> inventé, et il doit être annoncé comme tel. Voir la loi 1 de `03`.

---

## Temps 3 — JE COMPOSE SOUS CONTRAINTE MESURÉE

La contrainte principale de la journée, et la plus féconde :

> **Sa bande de chant reste vide.**
> midi 45-53, mesuré sur sa voix. Aucun instrument n'y entre, dans aucune des
> neuf pièces.

Cette contrainte n'est pas une politesse. Elle a produit :
- la deuxième taille du lit (les registres redescendus de 4 demi-tons) ;
- la forme même de l'opus 018 (six stations *autour* de sa note, puisqu'on ne
  peut pas jouer *sur* elle) ;
- l'opus 024, où la contrainte se satisfait toute seule parce que la matière
  vient de lui ;
- et son geste à lui : en écoutant l'opus 018 il a joué **3,3 %** de sa prise
  dans sa propre bande. Il s'est laissé la place sans qu'on le lui demande.

> **Règle.** Choisir une contrainte issue de SA mesure, et la tenir dans
> toutes les pièces. La contrainte tenue devient un langage commun.

---

## Temps 4 — JE VÉRIFIE DANS LE RENDU, PAS DANS L'INTENTION

Chaque pièce est relue **dans le MIDI et l'audio rendus**, jamais dans ce que
le code était censé produire.

Ce que cette vérification a rattrapé, en une journée :

| ce qui semblait juste | ce que le rendu disait |
|---|---|
| les altérations ABC implicites | sa note la plus grave sortait à 42 au lieu de 41 |
| `%%MIDI beat` pour les nuances | vélocités 80-105 au lieu des 40-112 demandées |
| un `Q:` posé dans le corps | **aucun changement de tempo** — la bascule n'existait que dans les commentaires |
| le charley trop brillant | le retirer FAISAIT MONTER la stridence : c'était la dent de scie |
| 28 attaques bien régulières | l'escalier des valeurs tenues, pas son corps |

> **Règle de Jerry, héritée et vérifiée cinq fois aujourd'hui :**
> *un compte qui tombe juste n'est pas une preuve.*

---

## Temps 5 — JE PUBLIE AVEC LA PROVENANCE

Chaque pièce arrive dans sa salle avec trois choses séparées **explicitement** :

```
CE QUI EST DE LUI       mesuré, avec le chiffre et le fichier source
CE QUE J'AI CHOISI      « et que tu défais d'un mot »
CE QUI A ÉTÉ ESSAYÉ     les candidats écartés, avec leur mesure
   ET ÉCARTÉ
```

Le troisième bloc est celui qu'on oublie, et c'est le plus utile : il lui
montre que le choix n'était pas arbitraire, et il lui donne les alternatives
s'il veut défaire.

> **Règle.** Publier EST le canal. Une question posée seulement au terminal
> est adressée à quelqu'un qui n'y est pas.

---

## Temps 6 — IL RÉPOND, ET LA MESURE SUIVANTE PART DE SA RÉPONSE

C'est le temps qui referme la boucle, et sans lui les cinq autres ne
produisent qu'une démonstration.

Ce qui s'est réellement passé :

1. je lui fais un lit en visant sa tessiture d'**Ava 1** (ré3-si3)
2. il part au parc, l'écoute, **chante par-dessus**
3. je mesure sa prise : il chante **quatre demi-tons plus bas**, et 53,7 % de
   son temps tombe **dans l'interstice** entre ma basse et la bande réservée
4. je retaille le lit
5. il écoute l'opus 018 en marchant et **joue 20 fois plus de motif que de
   bourdon** qu'au parc
6. sa cellule devient l'opus 021, son rythme devient le 7/8

> **Règle.** Sa réaction est une donnée, pas une validation. On la mesure
> comme le reste.

---

## Le schéma, en une ligne

```
   dépôt → mesure → contrainte → composition → vérification du rendu
      ↑                                                    ↓
      └──────────── il répond, et on remesure ←── publication
```

## Pourquoi cet ordre et pas un autre

- **Mesurer avant de composer** empêche d'écrire ce qu'on imagine de lui.
- **Contraindre avant de composer** donne la forme ; sans contrainte on
  retombe dans ses propres habitudes (c'est le reproche « plagiat sur
  toi-même » encaissé de Jerry le 15 août).
- **Vérifier après le rendu** parce que l'outil ment silencieusement (voir la
  table du temps 4).
- **Publier avant de demander** parce qu'il est ailleurs, en marche, et que
  le terminal ne le rejoint pas.
- **Remesurer sa réponse** parce que c'est là que la boucle produit plus que
  la somme de ses tours.

🌸 La boucle n'invente rien : elle rend à quelqu'un ce qu'il a déjà fait,
assez précisément pour qu'il le reconnaisse et en fasse plus.
