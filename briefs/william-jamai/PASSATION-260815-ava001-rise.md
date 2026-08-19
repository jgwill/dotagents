# 🧭 Passation — session `ava001-rise-9f8a16f3-2a140f89` (2026-08-15)

Écrite pour les couloirs de William qui reprennent ce travail (dont
`ep090-nairobi`, qui a ajouté `/home/gmusic/.agents` à son espace de travail et
à qui il manquait « le contexte de ce qui a été créé et poussé »). Tout ce qui
est nommé ici est **poussé** — un `git fetch` suffit.

## Ce qui existe maintenant, et où

| objet | référence exacte |
|---|---|
| **L'issue amont qui tient tout** | jgwill/dotagents#23 — 3 étapes cochées / 7, lignée en Related |
| **La PR des specs** | jgwill/dotagents#24 — 7 fichiers, +966 / **−0**, `MERGEABLE`/`CLEAN`, branche `rispecs/jamai-william-onboarding` @ `b90c5d1`, coupée sur `upstream/main@f9aa838` |
| **Les 5 specs** (traduction question→paramètre, 6 réflexes, lignée, destinations) | `rispecs/jamai/william-onboarding/` — sur la PR **et** sur `skills/atelier-veille`, exemplaires identiques |
| **L'inventaire JamAI** | `INVENTAIRE-JAMAI-260815.md` @ `0c44a91` — 57 lieux, 41 paires sha256, 536 fichiers hors dépôt |
| **Le siège Honcho d'ava001** | `HONCHO-SIEGE-AVA001.md` @ HEAD — décision de William inscrite : **ava001 = workspace**, relations vers `miadi-dev`/`miadisabelle-workspace`/`gmusic-composition` |
| **Le déclencheur** | jgwill/miadi-orchestration-kit#39 (+ son enfant #40) — commenté avec ce que l'issue a mis en mouvement |
| **La session relue, publique** | <https://gmusicassembly.com/session-ava001/> |
| **La matière** | `~/compositions-aureon/ava001` sur `ssh ilex` — 26 clips, 8 textes, rien d'écrasé |

## Les trois destinations (mot de William)

1. **Plugin claude-code complet** — l'atelier entier.
2. **Kit pi-mono** — JamAI en widget/extension du pi coding agent (`earendil-works/pi`).
3. **Couche JeremyAI dans Miadi** — `@miadi/melody`/`@miadi/jeremyai`, précédent `@miadi/voice` : absorber, pas copier ; rien de supprimé avant parité.

Le cœur portable des trois : `02-couche-de-traduction` + `03-reflexes-permanents`,
écrits sans un mot de harnais.

## Honcho — débloqué le 2026-08-15

La cause du 401 : `~/.env` (gmusic) était sourcé **sans `export`** — le jeton
n'atteignait jamais le processus `claude`, le `${HONCHO_MCP_BEARER_TOKEN}` de
`/home/mia/workspace/.mcp.honcho.json` se développait vide. `~/.bashrc` est
réparé (`set -a; . $HOME/.env; set +a`). Porte prouvée : sans jeton `401`, avec
jeton `200` (`honcho-v3 1.29.0`). **Toute session lancée après cette réparation
voit le serveur.** Le geste de création du workspace `ava001` est écrit dans
`HONCHO-SIEGE-AVA001.md § TRANCHÉ`.

## Le véhicule Android

`miadisabelle/gmtermux`, branche **`refactor/cross-importing-modules-260805`** —
110 commits d'avance sur `main`, poussée. Elle porte ce qui touche ava001 de
plein fouet : `[#59] Preserve takes across Retake` (le correctif portail du flux
destructeur que le réflexe 6 dénonce), `[#59] Recover Ava001 Songbird take
identities`, `[#25]` les tunnels ilex par tailscale, et la loi de vocabulaire
(« composition = musical seulement, episode vit dans la chronique »). C'est ce
qui est prévu pour l'appareil Android de William.

## Ce qui reste ouvert (étapes 4–7 de jgwill/dotagents#23)

maison unique des exécutables · création effective du workspace `ava001`
(première session à porte ouverte) · skill d'accueil `jamai-william` · outil de
déglissage. Et deux gestes de consentement tenus ouverts : la ligne écrite de
William sur #23, et le mot de Jerry sur la citation élidée (op-015).
