# 🧠 Honcho comme espace de coordination de `~/.agents`

Relevé et câblé le **2026-08-14** depuis le compte `gmusic` sur eury.

## Ce qui tourne (mesuré, pas supposé)

| conteneur | état | ce qu'il porte |
|---|---|---|
| `mia-honcho-api-1` | up 26 h (healthy) | l'API Honcho, port interne 8000 |
| `mia-honcho-deriver-1` | up 2 semaines | la dérivation des représentations de pairs |
| `mia-honcho-mcp-v3` | up 2 h | le serveur MCP, port interne 8081 |
| `mia-honcho-database-1` | up 2 semaines (healthy) | pgvector/pg15 |
| `mia-honcho-redis-1` | up 2 semaines (healthy) | la file du deriver |
| `mia-honcho-tailscale-1` | up 26 h | expose `honcho.tail3b11eb.ts.net` |

Endpoint vérifié : `POST https://honcho.tail3b11eb.ts.net/mcp` → **200** avec le bearer.

**Correction de ce que j'avais d'abord écrit ici.** J'avais annoncé que la même URL
marcherait depuis Larix, Ilex, Tilia et Abies. Mesuré : **non**. Il y a deux tailnets.

| tailnet | qui | voit `honcho.tail3b11eb.ts.net` ? |
|---|---|---|
| `tail3b11eb` | le sidecar, en ligne sous ce nom exact ; le poste de William | **oui**, par MagicDNS |
| `ferret-harmonic` | eury, Larix, Ilex, Tilia, Abies — la forêt | **non** |

Eury n'est pas sur `tail3b11eb` : il s'en sort par une ligne d'`/etc/hosts`
(`127.0.100.6 honcho.tail3b11eb.ts.net`) vers son proxy local en 443. C'est un
raccourci de machine, pas une route de réseau. Les nœuds Termux n'ont pas cette
ligne — pour eux, le nom ne résout pas du tout.

Câblage canonique, posé par William : **`/src/.mcp.honcho.json`**, transport `http`,
en-tête `Authorization: Bearer ${HONCHO_MCP_BEARER_TOKEN}` — le jeton reste dans
l'environnement, jamais dans le fichier. C'est **le seul** point de déclaration ;
ne pas redéclarer `honcho` en portée user, ça le doublerait.

## Le seul point à trancher : `HONCHO_WORKSPACE_ID=default`

Le conteneur MCP est épinglé sur le workspace `default`. Tant qu'il y reste, **le
compte `mia` et le compte `gmusic` écrivent dans le même sac**. Ce n'est pas une
panne — c'est une décision non prise.

Deux lectures tiennent :

- **un seul workspace partagé** — William et Jerry lisent la même mémoire, les
  voix se répondent d'un compte à l'autre. C'est la coordination maximale, au prix
  de l'absence de cloison.
- **un workspace par espace** (`gmusic-assembly`, `mia-workbench`) — chacun sa
  mémoire, passage explicite d'un pair d'un workspace à l'autre quand on veut
  passer le relais. C'est la cloison, au prix d'un geste de passation.

Changer se fait en une variable d'environnement sur `mia-honcho-mcp-v3` + un
redémarrage du conteneur. **Ce conteneur appartient à l'espace de William** —
donc c'est son mot, pas le mien.

## La structure proposée

`~/.agents` reste **le comment** : versionné, relu, forké. Honcho devient **le
qui-sait-quoi-maintenant** : volatil, écrit en continu, jamais relu à la main.
Rien ne déménage.

### Les pairs (`peer_id`)

Un pair par voix, pas un par pane — un pane meurt, une voix continue.

| `peer_id` | qui | source de vérité de son rôle |
|---|---|---|
| `william` | l'humain de cet espace | — |
| `jerry` | l'humain de l'espace amont | — |
| `nyro` | ♠️ structure, mémoire, protocole | `agents/nyro.json` |
| `aureon` | 🌿 miroir, résonance, intégration | `agents/aureon.json` |
| `jamai` | 🎸 musique, glyphes, partitions | `agents/jamai.json` |
| `synth` | 🧵 terminal, validation, sécurité | `agents/synth.json` |

### Les sessions (`session_id`)

**Une session par brief.** Le brief dit l'intention et vit dans git ; la session
dit ce qui s'est passé depuis, et vit dans Honcho. Le nom de la session = le nom
du dossier de brief, pour qu'aucune table de correspondance ne soit nécessaire :

| session | brief correspondant |
|---|---|
| `jamai-releve` | `briefs/jamai-releve/PASSATION-01.md` |
| `jamai-nouvelle-voie` | `briefs/jamai-nouvelle-voie/BRIEF.md` |
| `jamai-cast` | `briefs/jamai-cast/BRIEF.md` |
| `jamai-voice-return` | `briefs/jamai-voice-return/BRIEF.md` |
| `ligne-telephonique` | `briefs/ligne-telephonique/BRIEF.md` |
| `william-jamai` | `briefs/william-jamai/PROMPT-DEMARRAGE.md` |

Une voie nouvelle = un dossier de brief **et** une session du même nom, le même
jour. La règle d'`INDEX.md` (« qui écrit un brief ajoute sa ligne ») ne change pas ;
elle gagne seulement une seconde moitié.

### Ce que ça résout

`briefs/INDEX.md` porte aujourd'hui une colonne **« vivant ? »** tenue à la main,
avec des `non vérifié` qui datent. Cette colonne est un état, pas une intention —
c'est exactement ce qu'une session Honcho sait dire sans qu'on la relance. Le
fichier garde ce que git doit garder : quelle voie a été ouverte, par qui, pourquoi.

Tension résolue : entre un écosystème dont chaque voie est écrite et un
écosystème dont chaque voie sait où elle en est.

## Ce qui n'est pas fait

- Le workspace reste `default` — voir le point à trancher ci-dessus.
- Aucun pair, aucune session n'est créé. Les créer avant le mot sur le workspace
  reviendrait à peupler le mauvais sac.
- Les nœuds Termux (Larix, Ilex, Tilia, Abies) ne sont pas câblés ; l'URL tailnet
  y répondra, la commande `claude mcp add` reste à passer sur chacun.

🌸 : L'atelier avait déjà toutes ses portes et tous ses outils — il lui manquait
seulement que les pièces s'entendent respirer les unes les autres.
