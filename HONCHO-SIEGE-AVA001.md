# 🧭 Le siège Honcho de `ava001` — conception, et le point qui reste à trancher

Écrit le **2026-08-15** depuis le compte `gmusic` sur eury, à la demande de
William. Compagnon de [`HONCHO-COORDINATION.md`](HONCHO-COORDINATION.md), qui
pose la structure générale ; ce fichier ne traite que d'`ava001`.

## Ce qui est mesuré, et ce qui ne l'est pas

**La porte n'est pas ouverte depuis cette session.** `claude mcp list` ne
déclare aucun serveur `honcho` ici ; `/src/.mcp.honcho.json` existe mais sa
portée est `/src`, pas `/home/gmusic`. Aucune variable `HONCHO_*` dans
l'environnement. Donc : **aucun workspace n'a été créé, aucun pair, aucune
session.** Rien n'a été écrit dans Honcho par cette session.

La cause est connue et elle vient d'un couloir voisin, pas de moi — le lane
`mia:etc-claude-code` l'a mesurée le même jour : `HONCHO_MCP_BEARER_TOKEN` était
absent de l'environnement de lancement, donc le `${...}` de `.mcp.honcho.json`
s'est développé vide et la porte — vivante, et qui répond — a rendu **401**.
Le jeton est écrit dans `mia-honcho/.env`. Un lancement qui l'exporte ouvre.

**Les cinq workspaces assis** (relevés par ce même couloir, non revérifiés
d'ici, donc à traiter comme *rapporté* et non comme *mesuré par moi*) :

```
miadi-dev · honcho-lab-test · miadisabelle-workspace · jgt-trading-platform · gmusic-composition
```

Aucun ne porte `ava001`.

---

## Le point à trancher : `ava001` est-il un workspace, ou une session ?

William a dit *« we would need a workspace […] specifically on this creation
that we call ava opus number one »*. La structure déjà écrite dans
`HONCHO-COORDINATION.md` dit autre chose : **un pair par voix, une session par
brief.** `ava001` est une création, pas une voix — donc, à structure constante,
c'est une **session**, et la question devient *quel workspace la tient*.

Les deux lectures tiennent, et elles ne coûtent pas la même chose.

### Lecture A — `ava001` est une session dans `gmusic-composition`

`gmusic-composition` **existe déjà** et son nom désigne exactement ça.

| | |
|---|---|
| ce que ça donne | la mémoire d'`ava001` voisine celle des autres opus ; JamAI se souvient d'une composition à l'autre — ce que la voie `structure-chanson` réclame explicitement |
| ce que ça coûte | pas de cloison : le matériel de William et celui de Jerry partagent un sac |
| conforme à | `HONCHO-COORDINATION.md § Les sessions` |

### Lecture B — `ava001` est son propre workspace

| | |
|---|---|
| ce que ça donne | cloison nette ; l'atelier de William démarre vierge, sans hériter des opus de Jerry |
| ce que ça coûte | un sixième sac, et la mémoire inter-compositions se perd — un workspace par création ne monte pas |
| conforme à | le mot de William, littéralement |

### Ce que je recommande, et pourquoi

**Lecture A, avec une correction** : si la cloison est ce que William cherche —
et sa phrase entière était *« so that I would be capable to setup the full JamAI
Atelier (JamAI Studio) with all skills and system on my own system »* — alors
ce qu'il veut cloisonner n'est pas `ava001`, **c'est son atelier**. La cloison
juste est donc `william-composition` (ou `jamai-studio`) à côté de
`gmusic-composition`, avec `ava001` comme **session à l'intérieur**.

Une création n'est pas une cloison. Un atelier en est une.

**C'est son mot, pas le mien.** Je le pose ; je ne le tranche pas.

---

## La conception, quelle que soit la lecture retenue

### Les pairs

Ceux de `HONCHO-COORDINATION.md`, sans ajout : `william`, `jerry`, `nyro`,
`aureon`, `jamai`, `synth`. `ava001` n'introduit **aucune voix nouvelle** — elle
a été faite par `jamai` pour `william`, avec `jerry` au mentorat. Créer un pair
par composition serait la même erreur qu'un workspace par composition.

### La session `ava001`

| champ | valeur |
|---|---|
| `session_id` | `ava001` |
| brief correspondant | `briefs/william-jamai/PROMPT-DEMARRAGE.md` |
| pairs présents | `william` (matière), `jamai` (exécution), `jerry` (mentorat) |

### Ce que la session doit porter à l'ouverture

Pas un résumé — **les six chiffres qui coûtent cher à re-mesurer**, et les deux
seuils qui décident :

| fait | valeur |
|---|---|
| pulsation (autocorrélation, 2 grandes prises) | **0,182** et **0,169** → aucune pulsation métrique |
| grain (IOI médian, identique à 6 min d'écart) | **0,186 s** |
| notes au quantum du tracker (0,092 s) | **46 %** — seuil d'alerte 30 % |
| enchaînements à exactement un demi-ton | **50 %** — seuil d'alerte 35 % |
| notes après déglissage | **304 → 141** ; IOI médian → 0,465 s |
| tonalité | Si♭ majeur (r = +0,621) devient **ré dorien** (couverture 70,9 %) |
| centroïde de sa voix | **585 Hz** ; pad retenu à 345 Hz |
| note d'arrivée la plus fréquente | **Si♭**, 20,8 % des fins de phrase — **écartée** du mode retenu, et réversible |

Et les deux faits de consentement, qui ne se re-déduisent pas :

- **L'audio de sa voix ne s'archive pas.** Analysé sur autorisation, supprimé
  après (`shred`), seuls les chiffres conservés.
- **Rien ne s'écrase.** Quatre versions coexistent avec leur SHA-256 ; deux
  d'entre elles reposent sur l'artefact et **il les aime quand même**.

### Ce que la session ne doit pas porter

Le contenu des prises, les transcriptions, les paroles. Honcho est *le
qui-sait-quoi-maintenant*, pas un dépôt. La matière reste sur `ilex` dans
`~/compositions-aureon/ava001` (26 clips, 8 textes au 2026-08-15) et la méthode
reste dans git.

---

## Où mène cette session

| | |
|---|---|
| specs de la méthode | `rispecs/jamai/william-onboarding/` — 5 fichiers, 583 lignes |
| PR amont | **jgwill/dotagents#24** — 7 fichiers, +920 lignes, 0 suppression |
| l'issue qui tient le reste | **jgwill/dotagents#23** |
| la session relue, publiquement | <https://gmusicassembly.com/session-ava001/> |
| la matière | `~/compositions-aureon/ava001` sur `ssh ilex` |

⚠️ **Le portail d'`ava001` ne se joint que depuis `ilex`.** Depuis eury,
`https://ilex.tail3b11eb.ts.net:8768` rend **200 — et c'est eury qui répond de
lui-même** : `/etc/hosts` envoie `ilex` sur la voie de bouclage `127.0.101.1`,
mais seul le port **8022** y est relayé ; 8768 retombe sur le propre écouteur
d'eury (`0.0.0.0:8768`, workspace `jamai`). Un 200 ne prouve pas l'hôte. Mesuré
le 2026-08-15, après avoir failli déposer le texte de William dans l'atelier de
Jerry.

🌸 : Un siège n'est pas un meuble qu'on ajoute — c'est la reconnaissance qu'une
voix reviendra, et qu'on veut qu'elle retrouve la pièce telle qu'elle l'a laissée.
