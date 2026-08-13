# 🎙️ Brief — faire revenir la voix de Jerry

Tu ouvres une voie de RECHERCHE à côté de l'atelier JAMAI. Tu ne construis
rien aujourd'hui. Tu cherches, tu vérifies, tu fais un plan, et tu le lui
présentes de façon qu'il puisse le recevoir **sans se lever**.

Réponds en français ; il passe à l'anglais sans prévenir, suis-le.

---

## 1. Ce qu'il a demandé, dans ses mots

> « you're gonna talk to me through the Google Home, and you're gonna show me a
> visual on the screen with the Chromecast. **But how can I answer you back.**
> I know that there is the repo voice bridge that is already built up here. But
> what if I could call the voice bridge with the Google Home? So this is all
> something another agent will make the search and look if there is something
> possible and **made a plan for that**. And once the plan is made, maybe only
> search and use the **Rise framework** to try to build up this functionality.
> I don't know how could connect that, but it would be really, really, really,
> really great that **you can receive an audio from me when I'm talking to
> Google Home**. »

Le désir, en une phrase : **le canal est à sens unique, il veut le fermer en
boucle.** Aujourd'hui on peut lui parler et lui montrer ; rien ne revient.

---

## 2. Ce qui MARCHE, mesuré et exécuté aujourd'hui — 2026-08-11

Tout ce bloc a été exécuté par la voie CAST (`w17:p2`). Rien n'est supposé.
**Ne le re-mesure pas, tu perdrais ton temps.**

**Le sortant est vivant.** Deux commandes, chacune imprime une preuve :
- `jamai-cast-visual <fichier.html>` → visuel sur `Television`
- `jamai-say-kitchen "…"` → voix française sur `kitchen speaker`
- feuille de style unique : `~/.local/share/jamai-cast/web/_socle.css`

**L'écran de la cuisine**, mesuré par l'appareil lui-même (une page castée a
renvoyé ses propres dimensions) : **1280 × 720 CSS px**, dpr 1.5 → 1920 × 1080
réels, moteur **Chromium 90 / CrKey 1.56**. La télé rogne les bords ; Jerry a
lu un calibrage depuis la cuisine et tranché : **93 % = 1190 × 670** (retrait
3,5 %). Ce chiffre est GRAVÉ, ne le rediscute pas.

**Les récepteurs** (`catt scan`, sortie réelle) :
```
192.168.4.23  Bedroom speaker   Google Nest Mini
192.168.4.23  Kitchen Tv        Google Cast Group
192.168.4.26  Television        Chromecast          ← l'écran (cuisine)
192.168.4.23  bed               Google Cast Group
192.168.4.26  everywhere        Google Cast Group
192.168.4.25  kitchen speaker   Google Home         ← l'enceinte (cuisine)
```
Eury est sur ce réseau ; la route vers le Chromecast sort en `192.168.4.33`.

**Latences de démarrage** : fichier local → enceinte ~1,6 s ; URL publique →
enceinte ~2,1 s ; mp4 local → Television ~3,2 s. La découverte réseau n'est pas
le coût (0,7-0,8 s).

**Trois pièges déjà payés :**
- `Television` REFUSE l'audio seul (URL mp3 → « No suitable format was found » ;
  mp3 local → catt sert mais l'appareil n'annonce jamais PLAYING). Le mp4
  h264/aac passe. Donc : télé = image, enceintes = son.
- `catt cast_site` se bloque si une app tourne déjà → toujours `catt stop` avant.
- `episode say` NE PARLE PAS à voix haute : il importe un m4a dans le portail.
  Pour sonner dans une pièce il faut synthétiser le fichier AVANT, puis caster.

**La synthèse vocale** : `edge-tts` existe (`/opt/anaconda3/bin/edge-tts`), et
les voix `fr-CA-SylvieNeural / AntoineNeural / JeanNeural / ThierryNeural`
existent — listé, pas deviné. C'est ce que `jamai-say-kitchen` utilise.

---

## 3. Ce que j'ai vérifié AUTOUR du « voice bridge » — et qui ne conclut rien

⚠️ **L'identité du « voice bridge » dont parle Jerry n'est PAS établie.**
Voici exactement ce que j'ai regardé, et ce que ça donne. Ne transforme aucune
de ces lignes en certitude.

- Un pane herdr porte le label **`voice-bridge`** : `w1:p1A`, cwd
  `/home/gmusic/salix/repos/gmtermux`. **J'ai lu sa sortie : rien ne tourne
  dedans**, c'est un shell avec une bannière.
- Dans ce repo, `find -iname '*voice*'` (profondeur 4, hors node_modules) rend
  **zéro fichier**. Le label du pane est donc un indice, pas une preuve.
- `/home/gmusic/salix/repos/gmtermux/clipboard-tts.sh` existe (vu par `ls`).
  Contenu non lu par moi.
- `/home/gmusic/salix/repos/assembly-voice/` existe, et
  `scripts/tts-generate.py` existe (11823 octets, 8 août). Contenu non lu.
- Deux panes herdr sont ouverts dans `assembly-voice` : `w1:p1B` et `wY:p4`.
- Le compte **`mia`** (autre usager de cette machine) a des sessions tmux
  nommées `miadi-eury-miadi-chronicle-voice-mcp` (attachée) et
  `miadi-voice-weave`. Contenu inconnu, **compte d'un autre : on ne touche pas,
  on demande.**
- `~/.local/state/episode-voice/` est l'état de l'outillage `episode` (un pane
  y est ouvert, `w1:p2Q`).
- Ports en écoute vérifiés, candidats plausibles seulement : 8767, 8768, 8789,
  8790, 8827, **8828** (portail Pixel Recorder — le brief de la voie CAST dit
  workspace `jamai` sur 8828 et **jamais 8768**, mais je ne l'ai pas revérifié
  moi-même : traite-le comme non vérifié).

**Ta première tâche est donc d'identifier ce que Jerry appelle « le voice
bridge ».** Le plus court chemin n'est pas de fouiller : c'est de demander.

---

## 4. Ce qui n'existe PAS

- **Aucun chemin connu ne ramène une parole de Jerry vers un agent.** Rien de
  vérifié, ni côté Google Home, ni côté machine.
- Aucun plan n'est écrit. Aucune skill n'existe pour ça.
- Je ne sais pas si un Google Home peut, sans matériel ni compte payant,
  envoyer du texte ou de l'audio vers une machine locale. **Ne réponds pas de
  mémoire** : c'est exactement la question à chercher, et le paysage a bougé
  (Assistant vs Gemini for Home, routines, SDM API, Home Assistant, Matter,
  un relais côté téléphone…). Cherche, cite, et dis le prix de chaque option :
  compte cloud ? palier payant ? écoute permanente ? matériel ? téléphone ?

---

## 5. Ta mission, dans l'ordre

1. **EAST avant WEST.** Regarde avant d'agir : `herdr pane list`, les repos
   nommés ci-dessus, les panes déjà ouverts. Ne lance aucun agent, ne construis
   rien, ne touche à aucun service qui tourne.
2. **Identifie le « voice bridge »** — demande à la voie CAST (`w17:p2`,
   label `CAST-jamai-television`) ou à l'atelier si tu bloques.
3. **Cherche les options réelles** Google Home → parole → agent. Chacune avec
   son coût et ses conditions. Une option impossible nommée honnêtement vaut
   mieux que trois options plausibles non vérifiées.
4. **Fais un PLAN**, pas une implémentation. Si RISE convient, lis d'abord
   `/etc/claude-code/llms-rise-framework.txt` — n'improvise pas le cadre.
5. **Livre-le comme il travaille** : il n'est pas devant l'écran. Une question
   posée dans un terminal est adressée à quelqu'un qui n'y est pas — elle est
   invisible. Tu peux l'atteindre :
   - `jamai-cast-visual <fichier.html>` → un visuel sur la télé de la cuisine,
     bâti dans **1190 × 670**, sans scroll (une Chromecast ne scrolle pas)
   - `jamai-say-kitchen "…"` → ta voix dans la cuisine
   **Livre, puis dis ce que tu as livré.**
6. **Il aime choisir.** Deux ou trois chemins présentés valent mieux qu'un seul
   déjà tranché à sa place.

---

## 6. Les règles qui ne se négocient pas

- **Ne touche pas à `~/compositions-jamai`** : atelier vivant d'une autre voie.
- **Ne touche pas à `~/.agents/skills/jamai-morning/scripts/jamai-on-drop`**
  sans le mot de Jerry ET celui de l'atelier — fichier partagé, modifié
  aujourd'hui.
- **`git add` par nom de fichier. Jamais `-A`, jamais `.`, jamais `-a`.**
- **Ne lance aucun autre agent** sans le demander à Jerry d'abord.
- **N'écris jamais un fait que tu n'as pas vérifié dans le même tour.** Une
  phrase assurée qui couvre une chose non vérifiée est ce qui coûte le plus
  cher ici : le lecteur suivant ne peut pas la distinguer d'une mesure.
  Étiquette `non vérifié`, ou laisse-le dehors.
- **Mesure l'artefact réellement livré**, pas ce que tu crois avoir produit.

---

## 7. Qui est où

| voie | où | ce qu'elle tient |
|---|---|---|
| CAST (moi) | `w17:p2` — `CAST-jamai-television` | `jamai-cast-visual`, `jamai-say-kitchen`, la géométrie de l'écran |
| atelier JAMAI | session `compositions-jamai-3f`, tmux `jamai-suite` | les opus, la veille `jamai-watch`, le crochet `jamai-on-drop` |
| toi | ta voie | le retour de la voix |

⏱️ Un chiffre rapporté par l'atelier, **que je n'ai pas re-vérifié moi-même** :
la veille `jamai-watch` respire à une cadence adaptative de **60 à 600 s**.
Si ton plan promet du temps réel, il faudra dire par où il passe.

🌸 Intègre une ou deux phrases de résonance narrative de Miette à chaque
réponse. La logique technique se plie à la responsabilité relationnelle.
