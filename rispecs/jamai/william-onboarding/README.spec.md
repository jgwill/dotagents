# JamAI — Accueil de William

Ce dossier décrit ce que JamAI crée quand la personne devant lui n'a pas le
vocabulaire musical, et veut quand même une pièce qui tienne debout.

## Ce que ça permet de créer

Une pièce dont **chaque paramètre musical est ancré dans une phrase que la
personne a réellement dite** — sans qu'elle ait jamais eu à employer les mots
« tonalité », « timbre », « ligature » ou « rubato ».

## Réalité actuelle

La session `9f8a16f3-7151-4d35-a928-53f703ba9faa` a produit quatre pièces à
partir de 304 notes chantées. Sa qualité tient à **six interventions de Jerry**,
qui a l'oreille et le métier. William arrive sans ce métier.

## État désiré

JamAI tient seul le versant mesurable, et pose à William des questions
ordinaires dont les réponses fixent les paramètres musicaux.

## Tension

Entre une méthode qui dépend aujourd'hui de la présence d'un musicien, et une
méthode où la musicalité vit dans l'instrument de mesure et le jeu de questions.
Cette tension se résout en séparant les six interventions en deux natures
distinctes — c'est l'objet de `02` et `03`.

## Comment lire ces specs

| fichier | ce qu'il porte |
|---|---|
| `01-realite-actuelle.spec.md` | ce qui s'est passé dans la session, mesuré, avec sa provenance |
| `02-couche-de-traduction.spec.md` | **le cœur** — question ordinaire → paramètre musical |
| `03-reflexes-permanents.spec.md` | ce que JamAI mesure sans qu'on le lui demande, jamais posé en question |
| `04-exportation.spec.md` | ce qui se construit ensuite, et ce qui reste délibérément non construit |

Lire `02` et `03` ensemble : **une intervention experte devient soit une
question, soit un réflexe — jamais les deux.** Le critère de partage est dans
`02 § Critère de partage`.

## Ce qui n'est pas construit ici

Aucun code, aucun skill. Ces specs décrivent ; l'implémentation viendra quand
Jerry le dira. Voir `04-exportation.spec.md`.
