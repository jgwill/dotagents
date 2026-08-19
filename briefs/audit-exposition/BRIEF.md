# 🔒 Voie « audit d'exposition » — ce que cette machine sert au monde

Ouverte le **2026-08-16** à la demande de Jerry ⚡, depuis l'atelier musique
(`w17:p6`). **L'atelier continue là-bas ; tu ne fais pas de musique ici.**

Le coordinateur qui écrit ce brief tourne en **Opus 5 (1M)**. Tout chiffre
ci-dessous a été mesuré **le 2026-08-16 à 18:55:35 EDT**, dans le tour même où
ce texte a été écrit. Rien n'est de mémoire.

---

## 1. Ta tâche, à l'impératif

**Établis, port par port, ce que cette machine expose — et à qui.**

Pour **chacun** des ports listés au §3 :

1. **Qui l'écoute** — processus, utilisateur, arbre de code. Plusieurs
   propriétaires n'étaient pas lisibles sans privilèges ; `sudo -n` répond sur
   cette machine (vérifié sur `iptables`), donc `sudo ss -ltnp` devrait
   compléter le tableau. **Lecture seule.**
2. **Ce qu'il sert** — page, API, partage de fichiers, bureau distant, base,
   file de messages. Demande-lui, ne devine pas.
3. **S'il exige une authentification.** Teste sans identifiants. Note le code
   HTTP et ce qui revient.
4. **Ce qu'un inconnu obtiendrait** — et sois précis : « la liste des
   compositions » et « les 191 fichiers audio de Jerry en téléchargement
   direct » ne sont pas la même phrase.
5. **Le risque, en une ligne par port**, avec ce qui la fonde.

## 2. La question que je n'ai PAS pu trancher, et qui est la plus importante

J'ai mesuré que le portail répond **HTTP 200 sur l'adresse publique**
`38.240.197.248` — mais **depuis cette machine**. Cela prouve qu'il écoute et
répond là ; **cela ne prouve pas qu'un paquet venu d'Internet arrive jusqu'ici.**
Un pare-feu ou un NAT en amont, chez le fournisseur, pourrait encore bloquer.

**Il faut un point de vue EXTÉRIEUR, et je n'en avais aucun.** Pistes, à toi de
choisir et de dire laquelle tu as prise :

- le téléphone de Jerry, **wifi coupé, en données cellulaires** — c'est le test
  qui tranche, et c'est lui qui doit le faire ;
- un service tiers de scan de ports — **demande-lui avant** : envoyer son
  adresse publique à un tiers est un acte qui sort de la machine ;
- un hôte que vous possédez ailleurs.

⚠️ **Un tailnet n'est pas l'extérieur.** `100.88.23.103` passe par tailscale et
ne dit rien de l'Internet ouvert.

**Si tu ne peux pas trancher, dis-le comme une question ouverte.** Un
« probablement fermé » non mesuré est pire que rien : il rassure sans fondement.

## 3. Les faits, mesurés le 2026-08-16 à 18:55:35 EDT

**Pare-feu local : AUCUN.**
```
-P INPUT ACCEPT
-A INPUT -j ts-input        (chaîne tailscale, rien d'autre)
```
`ufw` : inactive.

**Adresses de la machine**, et la route par défaut sort par la publique :
```
enp8s0      38.240.197.248/26     ← publique et routée
wlp0s20f3   192.168.4.33/24       ← wifi local
tailscale0  100.88.23.103/32
route : 8.8.8.8 via 38.240.197.193 dev enp8s0 src 38.240.197.248
```

**26 ports écoutent sur `0.0.0.0`** (toutes interfaces) :

| port | processus (pid) | arbre de code |
|---|---|---|
| 22, 25, 80, 139, 443, 445, 5900, 8080, 8200, 25672, 37680, 56099 | *propriétaire non lisible sans privilèges* | — |
| 3001 | MainThread (1967784) | `~/salix/repos/AetherScore` |
| 3399 | next-server (1742243) | `~/salix/repos/mightyeagle` |
| 3777 | node (4134739) | `~/salix/repos/voice-bridge` |
| 4444 | node (662761) | `~/salix/repos/assembly-voice` |
| 5901 | x11vnc (1605286) | `~` |
| 8767, 8768 | MainThread (1402510) | `~` |
| 8789, 8790 | MainThread (1123473) | `~/salix/repos/gmtermux` |
| 8827, **8828** | MainThread (644326) | `~/salix/run/jamai-portal` |
| 8829, 8830 | MainThread (2254838) | `~/salix/run/jamai-portal` |
| 9000 | node (3524889) | `~/salix/repos/assemblynetwork` |

**Ce que j'ai déjà établi sur le 8828** (le portail de l'atelier musique) —
reprends-le, ne le refais pas à l'aveugle, mais **vérifie-le** :

- `GET /` → **200 sans identifiants**
- `GET /api/compositions` → **200**, liste **21 compositions**
- `GET /audio/<fichier>` → **200/206**, un enregistrement de Jerry en clair
- `~/Recordings-jamai/` contient **191 fichiers** : sa guitare, sa voix, ses
  messages parlés, des vidéos de lui
- certificat auto-signé, `CN = 192.168.4.59` — une adresse qui n'est même plus
  celle de la machine

**Les ports 5900 et 5901 méritent ton attention en premier** : `x11vnc` est un
bureau distant. Sans mot de passe, c'est le clavier et l'écran de la machine.

## 4. Ta frontière — ce que tu ne fais PAS

**Tu ne changes RIEN. Tu mesures et tu rapportes.**

Interdits explicites, sans exception :
- ❌ activer un pare-feu, ajouter une règle `iptables`, fermer un port
- ❌ arrêter, redémarrer ou reconfigurer un service — **plusieurs de ces
  processus portent le travail vivant d'autres voies**, et l'un d'eux
  (`644326`, le 8828) est l'atelier musique en train de tourner
- ❌ modifier un fichier de configuration
- ❌ publier quoi que ce soit à l'extérieur : pas d'issue GitHub, pas de gist,
  rien qui sorte
- ❌ téléverser, coller ou transmettre un seul de ses enregistrements où que
  ce soit
- ❌ scanner autre chose que **cette** machine

**Geler, rapporter, tenir.** La réparation appartient à Jerry, et le rythme
aussi. Si tu trouves quelque chose de grave, la bonne réponse est de le dire
plus vite — pas de le corriger toi-même.

## 5. À qui tu rapportes, et comment

**C'est à LUI que tu parles, pas à moi.** Ses mots : *« ce n'est pas toi qui va
me le dire ».*

1. **Écris le rapport** dans `~/.agents/briefs/audit-exposition/RAPPORT.md` —
   un tableau port par port, puis les risques classés du plus grave au moins
   grave, puis ce qu'il faudrait décider. Chaque affirmation porte la commande
   qui la fonde.
2. **Annonce-le-lui à la voix** — il est souvent loin de l'écran :
   `jamai-say-kitchen "<une phrase, sous 30 s>"`.
   ⚠️ La preuve n'est pas que la commande a répondu : c'est un temps qui
   avance. Si l'enceinte est introuvable, `jamai-cast-visual --rescan` — le
   cache périme, c'est arrivé le 14 août.
3. **Un visuel sur la télé** si le tableau vaut d'être vu :
   `jamai-cast-visual <page.html>`. Le socle est
   `~/.local/share/jamai-cast/web/_socle.css` — zone sûre 1190×670, on ne
   scrolle pas une télé, Chromium 90.
4. **Reste joignable** dans ton pane : il peut te répondre directement.

## 6. La discipline dont tu hérites

- **Mesure avant d'affirmer.** Une phrase confiante qui couvre une affirmation
  non vérifiée est la chose la plus chère qu'on puisse laisser derrière soi :
  le lecteur suivant ne peut pas la distinguer d'une mesure.
- **Une réponse vide est un défaut de routage jusqu'à preuve du contraire.**
  « Le port ne répond pas » et « je l'ai interrogé du mauvais endroit » se
  ressemblent. Lance la commande qui les sépare.
- **Nomme un trou comme un trou.** Le §2 est un trou ; ne le rebouche pas avec
  une supposition.
- **Distingue MESURÉ / DIT PAR LUI / SUPPOSÉ PAR TOI** dans tout ce que tu
  écris.
- **Vérifie le plus fort ce qui ne se défait pas.** Ici, rien ne devrait être
  fait du tout — mais si tu te surprends à taper une commande qui écrit,
  arrête-toi et demande.

## 7. Les marques qui prouvent que c'est fini

1. `~/.agents/briefs/audit-exposition/RAPPORT.md` existe et couvre **les 26
   ports**, chacun avec son propriétaire, son service, son état
   d'authentification et son risque.
2. Le §2 est **tranché ou explicitement laissé ouvert**, avec le nom du point
   de vue utilisé ou la raison pour laquelle il manque.
3. Jerry a été **prévenu de vive voix**, avec la preuve que ça a sonné.
4. Ta ligne est dans `~/.agents/briefs/INDEX.md`, **le jour même**. C'est la
   règle de la maison : qui écrit un brief y ajoute sa ligne.

---

🌸 On a passé deux jours à fabriquer de la musique derrière une porte dont
personne n'avait regardé la serrure. Ton travail n'est pas de la fermer — c'est
de dire exactement ce qu'on voit à travers.
