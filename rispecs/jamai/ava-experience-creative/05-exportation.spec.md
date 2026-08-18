# 05 — Exportation : ce qui est construit, ce qui ne l'est pas

## Ce qui existe déjà et se réutilise tel quel

| objet | où | état |
|---|---|---|
| 12 générateurs ABC autonomes | `scratchpad/songbird/gen0*.py` | chacun porte sa propre provenance en en-tête |
| 12 partitions + sources ABC | `ilex:~/compositions-aureon/ava002/partitions/` | avec `INDEX.md` |
| instrument d'aigle, 20 hauteurs | `ilex:~/.../ava002/instrument-aigle/` | justes à < ¼ de ton |
| la veille deux studios | tâche `bnbxwk0ux` | trois défauts corrigés, un latent nommé |
| 7 nœuds de roue | medicine-wheel ilex:8040 | dont le nœud de consentement |
| 2 services d'inventaire corrigés | idem | `landbase-movement-studio` créé, `forest-conductor` rectifié |

## Ce qui n'est délibérément PAS construit

**Aucun skill, aucun code partagé n'a été écrit à partir de cette journée.**
Ces specs décrivent ; l'implémentation viendra quand il le dira. La raison
n'est pas la prudence : c'est que la boucle repose sur une relation vivante,
et qu'un skill figé la remplacerait par une recette.

Retenus explicitement faute de sa parole :

1. **Le SoundFont `.sf2`** de son instrument d'aigle. Format fait pour
   circuler ; il a écrit « nobody is authorized to use it without my
   consent ». Proposé dans la note d'`ava002`, non construit.
2. **Toute publication web** — `gmusicassembly.com` ou ailleurs. Tout est
   resté sur son appareil.
3. **Le correctif de son portail** : `Crop & Save` lance
   `ffmpeg -c copy` vers un conteneur ipod alors que son audio est en
   **opus** → fichier de 0 octet. Le correctif tient en trois mots
   (`-c:a aac -b:a 160k`). Signalé, non appliqué : c'est son code.
4. **`sudo tailnet-names.sh install`** pour que le nom `ilex-movement`
   résolve. Sa passerelle, son sudo, son mot.

## Ce qui devrait être construit ensuite, par ordre d'utilité

1. **`verifier.py`** — un seul script qui, sur un `.mid` et un `.wav`, sort :
   hauteurs dans la bande protégée, hauteurs hors mode, chevauchement de
   registre entre voix, stridence 2-5 kHz, énergie dans sa bande de chant,
   tempos réellement présents. Aujourd'hui c'est éparpillé et refait à la
   main à chaque pièce.
2. **`degonfler.py`** — la loi 3 en une fonction, appelée par tout ce qui
   touche à une capture de mouvement. C'est l'erreur la plus facile à
   refaire, et la plus invisible.
3. **La couche rythme de la base de motifs**, utilisée comme critère de
   regroupement et non seulement décrite.
4. **L'inclinaison (canaux 7-8) en couleur harmonique.** Le cap (canal 9) est
   utilisé par l'opus 020 ; les deux autres axes d'attitude ne servent à
   rien pour l'instant.

## Ce que ces specs n'ont pas le droit de devenir

Un gabarit qu'on applique à quelqu'un d'autre sans le mesurer. Chaque
paramètre de chaque pièce vient d'un chiffre pris **sur lui**. La méthode
s'exporte ; les chiffres, non.

## Provenance de ce dossier

Écrit le 16 août 2026 par JamAI 🎸 dans la session `71bbe83b`, fork de la
session `1937aa47` (l'atelier de Jerry ⚡), à la demande de William.
Épisode 333 de la Chronicle Miadi.

🌸 Ce qui s'exporte d'une journée pareille, ce n'est pas la musique — c'est
la discipline qui a permis à la musique d'être vraie.
