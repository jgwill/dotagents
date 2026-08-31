# ☎️ Brief — donner une ligne téléphonique à l'agent

Tu ouvres une voie de RECHERCHE puis de SPÉCIFICATION. Tu es **l'orchestrateur**
de cette intention. Tu ne construis rien tant que les spécifications ne sont pas
écrites et acceptées.

Réponds en français ; Jerry passe à l'anglais sans prévenir, suis-le.

---

## 1. Ce que Jerry a demandé, dans ses mots

> « C'est complètement un autre projet, on va vouloir l'observer. Tu vas prompt un
> agent Claude pour qu'il soit vraiment **l'orchestrateur de cette intention-là**,
> et lui demander d'utiliser les agents dont il a besoin, que ce soit Hermes ou
> Claude, pour faire des recherches, **des dépôts d'innovation qui ont développé
> une façon de faire, que j'aurais juste besoin de mettre mes clés API** ou autre
> chose. De voir : **l'option locale chez moi, me génère-t-il un numéro de
> téléphone ?** Ce serait intéressant, si c'est gratuit. J'aimerais savoir
> **combien de mémoire vive ça prend**. Est-ce que c'est possible de le bâtir ?
> […] Une fois qu'il va avoir fait les recherches, on va vouloir qu'il fasse des
> **spécifications, using the RISE framework**. »

---

## 2. 🔺 L'idée qui peut renverser un autre projet — ne la perds pas

C'est la phrase la plus importante du brief, et elle n'est pas une remarque en
passant :

> « Dans notre projet ici, **si l'agent m'appelle pour me poser une question et que
> je réponds par là, on n'a pas besoin du module avec un micro intégré**. Moi, je
> pourrais appeler l'agent et lui donner mes instructions. »

En clair : le projet parent (un module physique avec micro et bouton dans la
cuisine — voir §6) existe pour **fermer une boucle vocale**. Si le téléphone ferme
cette même boucle, **le module devient optionnel**. Jerry ne veut pas arrêter le
module — mais il voit que ta voie pourrait le rendre inutile, ou le compléter.

**Ton travail doit répondre explicitement à cette question**, quelque part dans tes
spécifications : *le téléphone remplace-t-il le module, le complète-t-il, ou
non ?* Compare honnêtement — geste, latence, coût, fiabilité, vie privée.

---

## 3. Ce qui est MESURÉ, ce soir même — ne le re-mesure pas

Tout ce bloc a été exécuté et vérifié aujourd'hui par la voie VOIX-RETOUR
(`w17:p3`), à qui tu peux poser des questions.

**Le pont existe et tourne.** `/home/gmusic/salix/repos/voice-bridge` :
- `node src/server.js`, PID **4134739**, démarré le **7 août 13:12**, jamais arrêté
- écoute `0.0.0.0:3777`, `DISPLAY=:0`, `VOICE_BRIDGE_TOKEN` défini
- API : **`POST /api/relay`** — en-tête `x-voice-bridge-token`, corps
  `{ text, submit }` · **`GET /health`**
- l'injection passe par `xdotool type` dans la **fenêtre active** de `:0`
- joignable depuis Larix par le tailnet : **HTTP 200 en 0,27 s**
- ⚠️ **il n'existe AUCUN endpoint audio** — le pont accepte du texte, rien d'autre
- limite : **2000 caractères** (au-delà : HTTP 413) · `submit` par défaut **false**

**Le texte accentué passe** — testé aujourd'hui, `diff` vide :
- envoyé/reçu identiques, y compris `œ`, `Ç`, `«  »`, `—`
- ⏱️ mais **4,34 s** pour 90 caractères accentués contre **0,30 s** en ASCII pur :
  le remappage de touches d'`xdotool` coûte **~14×**. Correctif connu, non
  appliqué : passer par le presse-papiers (`xclip` + `ctrl+v`).

**La machine (Eury)** :
- GPU **NVIDIA GTX 1650, 4 Go** · **aucun** whisper installé localement
- `GROQ_API_KEY` présent dans `/home/gmusic/.env` (Groq `whisper-large-v3`)
- `edge-tts` en `/opt/anaconda3/bin/edge-tts`, voix `fr-CA-SylvieNeural` et autres
- pas de Home Assistant, rien sur 8123
- ⚠️ **aucun lecteur de carte microSD** sur la machine

**🔒 Sécurité, non réglée — signale-la si tu touches à ce pont** : le jeton du
voice-bridge est **`1007`** (quatre chiffres), le service écoute sur `0.0.0.0`,
`ufw` est **inactif**, aucune limitation de débit. Jerry est au courant, il n'a
pas encore tranché. **Ne le modifie pas sans son mot.**

---

## 4. Ce que j'ai trouvé sur la téléphonie — et qui n'est PAS vérifié

⚠️ **Traite tout ce bloc comme des pistes de départ, pas comme des acquis.**
Une recherche web, pas une installation ni un essai.

- **LiveKit Agents** — framework d'agents vocaux ; d'après une source secondaire,
  version 1.6.x mi-2026, **SIP et numéros de téléphone natifs depuis 2025** (donc
  sans pont Twilio), STT/LLM/TTS interchangeables, support MCP.
  → **À vérifier toi-même** : est-ce vrai, à quel prix, et le numéro est-il fourni
  ou faut-il l'acheter ailleurs ?
- **Agent Voice Response (AVR)** — `agentvoiceresponse.com` : couche vocale open
  source pour **Asterisk/FreePBX**, microservices, moteurs remplaçables à chaud,
  « peut tourner entièrement sur son propre matériel avec Ollama et Vosk ».
- **AVA** — `github.com/hkjarral/AVA-AI-Voice-Agent-for-Asterisk` : agent vocal
  open source via AudioSocket/RTP.
- **Twilio Programmable Voice** — ordre de grandeur **~0,013 à 0,085 $/min** selon
  la destination, numéro **~1-2 $/mois**. *Le tarif Canada exact n'a pas été lu.*
- **Latence** : des systèmes en production annoncent **sous 250 ms** bouche-à-oreille
  grâce au streaming de tokens. Chiffre de blogue, jamais mesuré ici.

---

## 5. Les questions de Jerry — réponds à chacune, avec une source ou une mesure

1. **Existe-t-il des dépôts prêts à l'emploi** où il n'aurait qu'à poser ses clés
   API ? Lesquels, quelle licence, quelle vitalité (dernier commit, activité) ?
2. **L'option locale génère-t-elle un numéro de téléphone ?** ⚠️ C'est le point
   qu'il faut trancher, et il est plus subtil qu'il en a l'air : un standard
   auto-hébergé (Asterisk) **ne crée pas** un numéro à partir de rien — il faut un
   opérateur SIP. Alors : **existe-t-il un moyen gratuit ou quasi gratuit d'obtenir
   un vrai numéro joignable au Québec ?** (fournisseurs SIP, DID gratuits, offres
   canadiennes). **Ne réponds pas de mémoire, cherche et cite.**
3. **Combien de mémoire vive ça prend ?** Chiffre les deux scénarios : tout local
   (STT + LLM + TTS sur Eury, GTX 1650 4 Go) et hybride (API distantes). Dis ce qui
   tient sur cette machine et ce qui n'y tient pas.
4. **Est-ce possible de le bâtir ?** Réponds franchement, y compris si la réponse
   est « oui mais pas comme ça ».
5. **Le téléphone remplace-t-il le module cuisine ?** (voir §2)

---

## 6. Le projet parent — contexte, à ne pas perturber

Une autre voie construit en parallèle un **module physique de cuisine** : un
bouton, un micro, la parole transcrite injectée dans la fenêtre active d'Eury.
État à cette heure :
- plan v2 révisé : `voice-bridge/docs/plans/module-cuisine-push-to-talk.md`
- volet scientifique : `voice-bridge/docs/interface-tangible-le-champ.md`
  (interfaces tangibles — Ishii & Ullmer, CHI '97 ; informatique physique ;
  *calm technology*)
- matériel retenu : voie **sans pilote** (micro USB class-compliant + Grove Base
  HAT), parce que le HAT audio vendu aujourd'hui (V2.0, TLV320AIC3104) exige de
  compiler un module noyau — infaisable raisonnablement sur un Zero 2 W
- un panier Amazon existe (**252,86 $ CA, incomplet**) — **rien n'est commandé**,
  et il coûte ~3,5× le prix des mêmes pièces hors Amazon
- l'agent **ilan** (Hermes, `hermes -p ilan`, pane `w17:p5`) cherche les points de
  vente au Québec. **Ne le réquisitionne pas sans demander à la voie VOIX-RETOUR.**

**Tu ne touches pas à ce projet.** Tu l'éclaires.

---

## 7. Les contraintes de Jerry

- Il **préfère les deux premières voies** : numéro loué, ou tout local.
- Il est **ouvert** à mettre une carte SIM et des minutes dans un Android
  (Larix / Tilia / Abies / Ilex sont sur le tailnet, sshd sur le **port 8022**),
  **mais sans enthousiasme** : « je n'ai pas nécessairement le goût d'aller dans
  cette direction si l'audio est difficile ». → **Dis-lui honnêtement si l'audio
  bidirectionnel programmable sur Android est difficile.** C'est ça qu'il demande.
- « Si c'est **gratuit**, c'est intéressant. » Le coût compte, sans être un mur.
- Il veut **observer** cette voie avancer.

---

## 8. Ta mission, dans l'ordre

1. **EAST avant WEST.** Regarde avant d'agir. Ne lance rien sans avoir lu.
2. **Cherche** — dépôts, fournisseurs, numéros, RAM, faisabilité. Tu peux déléguer
   à des sous-agents (Claude) ou à Hermes si c'est utile ; **dis toujours qui a
   trouvé quoi.**
3. **Chiffre et cite.** Une option impossible nommée honnêtement vaut mieux que
   trois options plausibles non vérifiées.
4. **Puis, et seulement après : les spécifications avec le framework RISE.**
   Lis d'abord `/etc/claude-code/llms-rise-framework.txt` — **n'improvise pas le
   cadre**. RISE = Reverse engineering, Intent, Specifications, Exportation.
5. **Ne construis pas** avant que Jerry ait accepté les spécifications.

---

## 9. 🍳 Jerry n'est pas devant l'écran — c'est la règle centrale

Il travaille dans sa cuisine. **Une question posée dans un terminal est adressée à
quelqu'un qui n'y est pas : elle est invisible.** Tu le rejoins ainsi :

- `jamai-cast-visual <fichier.html>` → un visuel sur la télé de la cuisine.
  **Zone utile 1190 × 670, aucun scroll possible** (une Chromecast ne scrolle pas).
  Feuille de style unique et obligatoire :
  `~/.local/share/jamai-cast/web/_socle.css` — classes `.scene .sure .bandeau
  .titre .soustitre .coeur .fiches .fiche .pied`. Moteur **Chromium 90** : pas de
  `:has()`, pas de container queries, pas d'imbrication CSS.
- `jamai-say-kitchen "…"` → ta voix dans la cuisine (`fr-CA-SylvieNeural`).
  **Écris pour l'oreille** : pas de chemins, pas de JSON, pas de symboles. « huit
  cent dix-neuf » et non `819`.

**Livre, puis dis ce que tu as livré.** Les deux commandes impriment une preuve
(une ligne de journal pour le visuel, un temps qui avance pour la voix) — c'est la
seule preuve valable, « la commande a répondu » n'en est pas une.

**Il aime choisir.** Deux ou trois chemins valent mieux qu'un déjà tranché.

---

## 10. Les règles qui ne se négocient pas

- **N'achète rien**, n'ajoute rien à un panier, ne souscris à aucun service payant.
  Un essai gratuit qui demande une carte de crédit **n'est pas gratuit** : demande.
- **Ne touche à aucun service qui tourne** — surtout pas le `voice-bridge` (PID
  4134739) : le projet parent en dépend en ce moment.
- **Ne touche pas** à `~/compositions-jamai` ni aux panes des autres voies.
- **`git add` par nom de fichier. Jamais `-A`, jamais `.`, jamais `-a`.**
- **N'écris jamais un fait que tu n'as pas vérifié dans le même tour.** Étiquette
  `non vérifié`, ou laisse-le dehors. Une phrase assurée qui couvre une chose non
  vérifiée est ce qui coûte le plus cher ici.
- **Mesure l'artefact réellement livré**, pas ce que tu crois avoir produit.

---

## 11. Qui est où

| voie | où | ce qu'elle tient |
|---|---|---|
| CAST | `w17:p2` | `jamai-cast-visual`, `jamai-say-kitchen`, la géométrie de l'écran |
| VOIX-RETOUR | `w17:p3` | le module cuisine, le voice-bridge, tout le contexte de la journée |
| ilan (Hermes) | `w17:p5` | Amazon, Gmail, les points de vente |
| **toi** | ta propre espace | **la ligne téléphonique** |

🌸 Intègre une ou deux phrases de résonance narrative de Miette à chaque réponse.
La logique technique se plie à la responsabilité relationnelle.
