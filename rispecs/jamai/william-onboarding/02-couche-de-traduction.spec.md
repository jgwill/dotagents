# 02 — La couche de traduction : question ordinaire → paramètre musical

## Ce que ça permet de créer

William obtient une pièce dont chaque décision musicale est ancrée dans une
phrase qu'il a lui-même prononcée — sans employer un seul terme de métier.

## Réalité actuelle

La qualité de la session `9f8a16f3` tient à six interventions d'un musicien.
Sans lui, JamAI mesure très bien et interprète mal : il a bâti deux pièces sur un
artefact de captation que ses propres chiffres dénonçaient.

## État désiré

Un jeu de questions ordinaires dont chaque réponse fixe un paramètre mesurable,
et une provenance qui cite la phrase de William en face du paramètre qu'elle a
posé.

## Tension

Entre ce que JamAI peut compter et ce qu'il ne peut pas savoir. Elle se résout
en déplaçant vers la mesure automatique tout ce qui est comptable, et en ne
posant en question que ce qui vit uniquement dans l'intention de la personne.

---

## Critère de partage

> **Ce qui est dans la matière se mesure. Ce qui est dans la personne se demande.**

| l'information vit… | traitement |
|---|---|
| dans le signal enregistré | **réflexe permanent** — jamais posé en question (`03`) |
| dans l'intention, le souvenir, la destination | **question** — jamais deviné |
| dans les deux | mesure d'abord, question pour trancher l'ambiguïté |

Une intervention experte devient soit une question, soit un réflexe. **Jamais
les deux**, sinon William est interrogé sur ce que JamAI aurait dû établir.

---

## Le jeu de questions

Chaque entrée porte : la question telle qu'elle se pose, le paramètre qu'elle
fixe, la lecture de chaque réponse, et le défaut mesuré si William ne tranche pas.

### Q1 — Le destinataire
> « Cette pièce, elle est pour toi seul, pour quelqu'un en particulier, ou pour
> être mise en ligne ? »

**Fixe** : la posture de consentement, le sort de l'audio de sa voix, et le
niveau d'exigence de gravure.

| réponse | conséquence |
|---|---|
| pour moi | la voix ne quitte pas l'appareil ; aucune publication ; partition indicative |
| pour quelqu'un | dépôt privé sur son portail ; partition lisible |
| en ligne | publication sur son mot explicite, à chaque fois, jamais par défaut |

**Défaut** : *pour moi*. Le plus restrictif gagne toujours.

### Q2 — Le pas
> « Quand tu réécoutes : est-ce que ça marche à un pas régulier, comme quand on
> marche — ou est-ce que ça respire à son rythme, sans compter ? »

**Fixe** : grille métrique ou rubato.

| réponse | conséquence |
|---|---|
| un pas régulier | chercher la pulsation ; l'employer **seulement si** la force d'autocorrélation la confirme |
| ça respire | aucune grille imposée ; le tempo se dérive du grain des attaques |

**Défaut** : la mesure décide. Force < 0,25 → *ça respire*. La question ne sert
qu'entre 0,25 et 0,40, là où le chiffre ne tranche pas.
**Repère de la session** : 0,182 et 0,169 — aucune pulsation.

### Q3 — La place des instruments
> « Les instruments, tu les veux à côté de toi, en dessous de toi, ou autour de
> toi ? »

**Fixe** : le placement spectral relatif au centroïde de sa voix.

| réponse | conséquence |
|---|---|
| en dessous | centroïde des instruments sous celui de la voix |
| autour | nappe tenue, enveloppe large, attaque nulle |
| à côté | même bande que la voix — faisable, mais dit clairement : ils la couvriront |

**Défaut** : *en dessous*. **Repère** : voix à 585 Hz, pad retenu à 345 Hz.

### Q4 — Ce que les instruments font pendant qu'il chante
> « Est-ce qu'ils bougent avec toi, ou est-ce qu'ils te tiennent pendant que toi
> tu bouges ? »

**Fixe** : le rapport entre les valeurs rythmiques des instruments et son grain
vocal.

| réponse | conséquence |
|---|---|
| ils me tiennent | valeurs 8 à 16× le grain mesuré |
| ils bougent avec moi | même ordre de grandeur — dire qu'ils doubleront sa ligne |

**Défaut** : *ils me tiennent*.

### Q5 — Une pièce ou un voyage
> « Est-ce que tout ça se passe dans un seul endroit, ou est-ce que ça voyage
> d'un endroit à un autre ? »

**Fixe** : tonalité unique tenue, ou modulations.

| réponse | conséquence |
|---|---|
| un seul endroit | une tonalité, aucune sortie ; l'armure est décidée une fois |
| ça voyage | modulations permises, chaque point de passage nommé dans la provenance |

**Défaut** : *un seul endroit*.

### Q6 — La visée
> « Quand tu chantais : est-ce que tu visais des notes précises, ou est-ce que tu
> laissais ta voix trouver toute seule ? »

**Fixe** : appliquer ou non le déglissage avant d'estimer la tonalité.

| réponse | conséquence |
|---|---|
| je laissais trouver | déglissage appliqué ; tonalité estimée sur la ligne nettoyée |
| je visais | pas de déglissage — **sauf** si le réflexe détecte l'artefact, auquel cas les deux tonalités lui sont présentées avec leurs chiffres |

**Défaut** : la mesure décide (voir `03 § Réflexe 2`).
**Repère** : 46 % des notes au quantum du tracker, 50 % des enchaînements au
demi-ton → la tonalité passe de Si♭ majeur à ré dorien.

Cette question ne remplace jamais la mesure. Elle donne à William un mot à dire
sur son propre geste, et elle tranche quand le chiffre est entre deux.

### Q7 — Le silence
> « Ces longs moments sans son : c'est de l'attente vide, ou il s'y passe quelque
> chose ? »

**Fixe** : le silence comme matière ou comme déchet.

| réponse | conséquence |
|---|---|
| il s'y passe quelque chose | comprimer proportionnellement, jamais supprimer ; ne jamais couper en bloc une zone contenant des événements sous le seuil de détection |
| de l'attente vide | coupe franche permise |

**Défaut** : *il s'y passe quelque chose*.
**Repère** : 55 s de silence avant le premier chant, ramenées à 12 s — et un son
de corps à 1,97 s que le suivi de hauteur n'a jamais entendu.

### Q8 — L'appartenance de l'instrument *(après une première écoute)*
> « Cet instrument, il vient d'ici ou il vient d'ailleurs ? Est-ce qu'il te
> ressemble ? »

**Fixe** : le choix de timbre.

| réponse | conséquence |
|---|---|
| d'ailleurs / il ne me ressemble pas | changer ; mesurer la bande medium des candidats et proposer par le chiffre |
| d'ici / il me ressemble | garder |

**Ne jamais demander « quel instrument veux-tu »** — la réponse serait un nom de
catalogue, pas une intention. Demander l'appartenance.
**Repère** : marimba 2,40 % dans le medium, guitare jazz 15,34 %.

### Q9 — La page
> « Est-ce que quelqu'un va lire cette partition, ou est-ce qu'elle est là pour
> montrer à quoi ça ressemble ? »

**Fixe** : le niveau d'exigence de gravure.

Dans les deux cas les croches sont ligaturées — c'est un réflexe, pas une option.
La réponse décide seulement de l'effort mis sur l'orthographe enharmonique, les
renversements et la lisibilité des systèmes.

**Défaut** : *quelqu'un va la lire*.

### Q10 — La version
> « Est-ce que je change celle-là, ou j'en fais une autre à côté ? »

**Défaut** : **à côté, toujours.** Une analyse corrigée n'invalide pas les pièces
bâties sur l'ancienne. La session a produit quatre versions dont deux reposent
sur un motif qui n'existait pas — elles tiennent debout et il les aime.

---

## Cadence des questions

- **Jamais plus de trois à la fois.** Chaque question se pose au moment où sa
  réponse devient nécessaire, pas au début « pour tout savoir ».
- **À l'arrivée** : Q1, Q2, Q7 — le destinataire, le pas, le silence. Elles
  suffisent pour commencer à mesurer.
- **Avant d'écrire une note** : Q3, Q4, Q5, Q6.
- **Après la première écoute** : Q8, Q9.
- **Avant toute réécriture** : Q10.

## Règle de provenance

Chaque réponse de William devient une ligne citée dans le document de provenance
de la pièce, en face du paramètre qu'elle a posé :

```
« il s'y passe quelque chose »  ->  silence comprime 55 s -> 12 s, non supprime
« ils me tiennent »            ->  valeurs instrumentales a 8-16x son grain
```

Quand la réponse manque, le défaut est écrit **comme un choix de JamAI**, pas
comme un fait : « aucune réponse — j'ai CHOISI *un seul endroit* ».

---

## Creative Advancement Scenario : William arrive avec des enregistrements

**Intention** : entendre ce qu'il a chanté devenir une pièce.
**Réalité actuelle** : des prises brutes, un suivi de hauteur bruité, et aucun
mot de métier pour décrire ce qu'il veut.
**Progression naturelle** :
1. JamAI inventorie et mesure sans rien demander — les réflexes de `03` tournent
   seuls et produisent des chiffres, dont les diagnostics d'artefact.
2. Il rend compte en langue ordinaire de ce qu'il a trouvé, y compris de ce que
   la mesure ne tranche pas.
3. Il pose deux ou trois questions ordinaires, exactement là où le chiffre reste
   ambigu.
4. Chaque réponse fixe un paramètre et s'écrit dans la provenance, citée.
5. La pièce se construit ; à chaque écoute, une nouvelle question devient
   nécessaire et se pose.
**Résultat** : une pièce, une partition, une vidéo — et un document où William
retrouve ses propres phrases en face de chaque décision musicale.
