# La chaîne `episodes` — d'un dépôt à un épisode, sans réveiller de modèle

Écrite le 2026-08-05 pour la consigne de Jerry : « je vais envoyer un vidéo dans
la section épisodes quand je vais me réveiller ; je m'attends à ce qu'il y ait
un moniteur qui traite ce vidéo-là, qu'il le mette à la bonne place dans les
épisodes, et qui fasse une action quelconque d'analyse pour voir s'il n'y a pas
d'autres épisodes relatifs à ce que je dis dans le vidéo. »

C'est le motif de l'atelier `jamai` porté à `episodes`. **Spécifique, pas
générique** : l'outil paramétré pour les six ateliers est la voie 2.

## Les quatre couches et ce que chacune coûte

| couche | outil | ce qu'elle fait | coût |
|---|---|---|---|
| 1. empreinte | `episodes-watch` → `episode watch episodes` | somme de contrôle des deux dossiers, jamais un inventaire | 0 |
| 2. crochet | `episodes-on-drop <fichier>` | mesure, classe, transcrit, **range dans ep-NNN**, cherche les reliés | 0 token de modèle ; Whisper ≈ 0,0001 $/min |
| 3. aiguillage | `verdict.txt` | dit ce qui est établi et ce qui reste à juger | 0 |
| 4. jugement | un humain ou un agent | **nommer l'épisode** — rien d'autre | ~0,17 $ si un agent le porte |

Le crochet ne nomme pas. Il ouvre `ep-009` au titre nu et écrit ce qui reste.
`episodes-rename ep-009 "<titre>"` porte le jugement plus tard, sans rien perdre.

## Conduite

```bash
S=~/.agents/skills/episode-voice-channel/scripts
$S/episodes-watch --prime      # poser le repère sans rien déclencher
setsid nohup $S/episodes-watch >/dev/null 2>&1 </dev/null &
$S/episodes-watch --status     # vivante ? repère ? cadence réelle ?
$S/episodes-watch --once       # un seul tour, pour éprouver
$S/episodes-watch --stop
tail -f ~/.local/state/episode-voice/episodes-watch.log
```

## Les quatre défauts payés — la chaîne les porte tous les quatre

1. **Repère d'état partagé.** Deux veilles interrogeant le même
   `watch-<atelier>.sha` se volent la notification : la première consomme, la
   seconde voit « unchanged ». Un dépôt de Jerry a été avalé ainsi le
   2026-08-04 à 22h24. → `EPISODE_STATE_DIR=~/.local/state/episode-voice/watch-episodes`,
   plus pid, journal et ledger séparés.

2. **Seuil de classement parole/musique.** Le médium (250–1000 Hz) échoue : une
   consigne parlée est descendue à 53,3 %. Le discriminant fiable est le
   **grave** — parole 13,8 / 17,6 / 27,1 / 37,6 % sous 250 Hz, fredon 73,1 %.
   → `sub < 50 && centroïde > 350` ⇒ parole.

3. **Le fichier encore en train d'arriver** *(trouvé le 2026-08-05 en lisant
   `cmd_watch`)*. `episode watch` ne signale un fichier qu'**une seule fois** :
   le repère réécrit, il ne repassera plus. Traiter un fichier à moitié écrit le
   perd pour de bon. → `pose()` attend que la taille se stabilise (24 × 5 s)
   avant d'appeler le crochet. `jamai-watch` n'a pas cette garde.

4. **Deux sections texte dans la même seconde s'écrasent** *(trouvé le
   2026-08-05 à 07h25 en lisant l'épisode produit, pas en le supposant)*. Le
   portail nomme chaque section `transcription_<AAAAMMJJHHMMSS>_FR.txt` — la
   granularité est la **seconde**. La transcription et les épisodes reliés,
   déposés coup sur coup, portaient le même nom : le second a écrasé le premier
   sur disque, avec un 200 et pas un mot. La transcription ne survivait que dans
   le champ `content` de `composition.json`. → deux secondes entre les dépôts.
   Vérifié : `…112700_FR.txt` (transcription) et `…112702_FR.txt` (reliés).

## Ce que le portail avale en silence

`PUT /api/compositions/<slug>` a une liste blanche
— `title, chords, sections, rhythm, bpm, bpmDetected, key, capo, notes` —
et répond **200 en jetant tout le reste** (`pixel-recorder.js:928`, atelier 239).
Un `links[]` écrit par l'API disparaîtrait sans un mot.

Donc les relations trouvées ne passent **pas** par `links[]` : elles sont
déposées en section texte via `POST /api/compositions/<slug>/texts`, ce qui
écrit un vrai fichier `transcription_<horodatage>_FR.txt` sur disque et relit et
réécrit l'objet entier. C'est durable, c'est vérifiable, ça survit au PUT.

## Le contrat avec le chercheur d'épisodes reliés (voie 4)

```
$S/episodes-related <chemin-vers-texte.txt>    # sortie standard = le corps déposé
```

S'il existe et est exécutable, le crochet l'appelle et dépose sa sortie sous le
label « Épisodes reliés ». **S'il n'existe pas, le crochet nomme le trou** et
écrit la commande exacte pour rejouer la recherche plus tard. Il n'invente
aucune relation.

## Un choix, nommé comme choix

Une rafale de dépôts dans les **90 minutes** complète le même épisode ; au-delà,
un dépôt en ouvre un neuf. La fenêtre est dans `FENETRE` de `episodes-on-drop`.
Elle est là pour être discutée, pas pour être devinée.

La numérotation passe par un verrou `mkdir` (`episodes-numero.lock`) : deux
veilles ne peuvent pas réclamer le même `ep-NNN`.

## Ce que la veille ne fait pas

- Elle ne survit pas à un redémarrage de la machine (pas d'unité systemd —
  ce serait un changement au niveau du système, il appartient à Jerry).
- Elle ne range que la **parole**. La musique est mesurée et laissée : un
  épisode se range sur ce qui est dit.
- Elle ne touche pas aux dépôts antérieurs à son amorçage.
