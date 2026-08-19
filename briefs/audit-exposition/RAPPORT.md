# 🔒 Ce que cette machine sert au monde — rapport de mesure

**Pour Jerry ⚡.** Mesuré le **2026-08-16 entre 18:58 et 19:12 EDT**, sur `eury`,
adresse publique `38.240.197.248`. Rien n'a été modifié : aucun pare-feu, aucun
service arrêté, aucun fichier de configuration touché. Toutes les sondes sont des
lectures (`GET`, poignée de main, bannière). **Aucun `POST`, aucun `DELETE`.**

Convention : **[M]** = mesuré ici · **[D]** = dit par le brief, revérifié par moi ·
**[S]** = supposé, non mesuré. Chaque affirmation porte sa commande.

---

## 1. La question du §2 est TRANCHÉE — et la réponse est : oui, les paquets arrivent

Le brief demandait un point de vue extérieur. Je n'ai eu besoin **ni du téléphone
de Jerry, ni d'un service tiers** : la machine garde elle-même la trace des
inconnus qui l'ont déjà touchée. Aucune adresse n'est sortie vers un tiers.

**Trois preuves indépendantes, sur trois ports différents :**

| preuve | ce qu'elle établit | commande |
|---|---|---|
| **55 122 échecs de connexion SSH** venant de **154 adresses publiques distinctes**, depuis le 3 août, la dernière **à 19:04 aujourd'hui** — soit une minute avant la mesure. Pires attaquants : `45.142.193.164` (20 676 tentatives), `202.181.177.61`, `185.217.1.246` | port **22** reçoit l'Internet ouvert | `sudo lastb -a` |
| **`178.238.231.185` s'est connecté au VNC du port 5900 à 19:03:29 aujourd'hui**, refusé uniquement par la liste `-allow` de x11vnc | port **5900** reçoit l'Internet ouvert | `sudo tail /var/log/x11vnc-mirror.log` |
| **13 connexions TCP établies en ce moment** sur le port 8080, venant de `45.79.115.59`, `45.79.207.252`, `45.33.14.5` (plages de scan Linode) | port **8080** reçoit l'Internet ouvert, **maintenant** | `sudo ss -tnp state established 'sport = :8080'` |

En prime : le serveur DLNA du port 8200 affiche lui-même ses clients récents —
`178.128.230.199` et `172.105.102.10`, deux adresses publiques
(`curl http://38.240.197.248:8200/`).

**Il n'y a donc ni pare-feu ni NAT en amont qui protège.** [M]

**Le reste d'ombre, nommé comme un trou :** ces preuves portent sur 22, 5900,
8080, 8200. Un fournisseur *pourrait* filtrer certains ports et pas d'autres —
je ne peux pas exclure formellement que 8828 soit filtré alors que 22 ne l'est
pas. C'est très improbable ([S] — le filtrage sélectif suppose une règle, et il
n'y en a aucune ici), mais ce n'est pas mesuré. **Le test qui ferme la question
définitivement reste le tien** : téléphone, wifi coupé, données cellulaires,
`https://38.240.197.248:8828/`.

**Et la bonne nouvelle, mesurée :** *aucune* connexion SSH **réussie** ne vient
d'une adresse publique. Les 825 connexions réussies viennent toutes du tailnet
(`100.x`), de la boucle locale ou du LAN (`sudo last -a`, `grep Accepted
/var/log/auth.log`). Rien n'indique une intrusion par SSH.

---

## 2. Port par port — les 26 du brief, **plus 7 que le brief n'avait pas comptés**

Tous ces ports acceptent une connexion TCP venue de `38.240.197.248`
(`bash -c 'exec 3<>/dev/tcp/38.240.197.248/<port>'`, un par un). Sauf mention,
la réponse est obtenue **sans aucun identifiant**.

### 🔴 Les cinq qui donnent le plus

| port | qui écoute (pid, user) | ce qu'il sert | auth ? | ce qu'un inconnu obtient |
|---|---|---|---|---|
| **5901** | `x11vnc` 1605286, **gmusic** — `-rfbauth ~/.vnc/passwd -forever -shared -noxdamage -scale 1872x953`, **aucun `-allow`** | bureau distant de l'écran `:0` — l'écran réel de Jerry | **un seul mot de passe VNC**, type de sécurité 2 offert et seul offert [M] | l'invite de mot de passe sur ton écran vivant. Le mot de passe VNC fait **8 caractères maximum** (fichier de 8 octets), le protocole est un défi DES, et x11vnc **ne limite pas les tentatives**. Un attaquant peut essayer sans fin. S'il passe : clavier, souris, écran, sessions ouvertes. |
| **8790** | `forest-conductor.js` 1123473, gmusic — `~/salix/repos/gmtermux` | pilote de la forêt : lit et **écrit dans les tmux** de tous les nœuds | **AUCUNE.** `grep -c "requireAuth\|basicAuth\|401\|token"` → **0** [M] | `GET /api/terminal/eury/sessions` → **200, la liste des 27 sessions tmux de cette machine, avec leurs noms** (`beta-mia`, `ep326-honcho`, `ava001-rise-…`…). `GET /api/terminal/nodes` → **200**, la carte du tailnet. Et la route `POST /api/terminal/:node/send` **tape des touches dans une de ces sessions** — je ne l'ai pas appelée. C'est de l'exécution de commandes à distance, sans mot de passe, depuis Internet. |
| **8828** + **8827** (→ redirige vers 8828) | `web/pixel-recorder.js` **644326**, gmusic — `~/salix/run/jamai-portal` — **l'atelier musique en train de tourner** | le portail : enregistrements, compositions, presse-papiers | **AUCUNE.** Les deux seules occurrences d'`Authorization` dans les 9 255 lignes sont `Bearer ${GROQ_API_KEY}`, sortantes [M] | `GET /` → 200 · `GET /api/compositions` → **200, 21 compositions** [D vérifié] · `GET /recordings` → **200, 181 fichiers listés** avec noms, tailles, dates · `GET /audio/260815220359.m4a` → **206, `Content-Range: bytes 0-99/617707`, `audio/mp4`** — le fichier se télécharge [D vérifié] · **`GET /api/clipboard/recent` → 200, 5 entrées du presse-papiers de cette machine** (je n'ai pas affiché le contenu). Et les routes d'écriture : `DELETE /recording/:filename`, `DELETE /api/compositions/:slug`, `POST /import`, `POST /start`, **`POST /api/app/pull`**, `POST /api/restart-portals`, `POST /transcribe/:filename` (qui dépense ta clé Groq). Non appelées. |
| **8768** + **8767** (→ 8768) | `pixel-recorder.js` **1402510**, gmusic — `~/dryades` | **le même dossier d'enregistrements** que 8828 | **AUCUNE** | `GET /recordings` → **200, les mêmes 181 fichiers** ; presse-papiers → 200, mêmes 5 entrées. **Fermer 8828 sans fermer 8768 ne fermerait rien.** [M] |
| **8830** + **8829** (→ 8830) | `pixel-recorder.js` **2254838**, gmusic — `~/salix/run/jamai-portal` (journal `abies.log`) | portail du nœud abies | **AUCUNE** | `GET /recordings` → **200, 54 fichiers** (jeu différent) ; presse-papiers → 200. |

**Le dossier derrière tout ça** : `~/Recordings-jamai` — **191 fichiers, 1,6 Go**
(`ls | wc -l`, `du -sh`) : 80 `.mp4`, 62 `.m4a`, 33 `.mov`, 10 `.json`, 6 `.mid`.
Ta guitare, ta voix, tes messages parlés, des vidéos de toi. [D vérifié]

### 🟠 Les portes d'entrée classiques

| port | qui écoute | ce qu'il sert | auth ? | ce qu'un inconnu obtient |
|---|---|---|---|---|
| **22** | `sshd` 1590, root | SSH | clé **et mot de passe** — `sudo sshd -T` donne **`passwordauthentication yes`**, `permitrootlogin without-password` [M] | une invite de mot de passe pour les comptes `gmusic`, `masso`, `paj`. **Aucun `fail2ban`** (`systemctl is-active fail2ban` → *inactive*, binaire absent). 55 122 tentatives déjà encaissées, personne n'est passé. |
| **5900** | `x11vnc` 1600770, **root** | miroir de l'écran physique | mot de passe **+ liste `-allow`** limitée à 8 adresses tailnet [M] | **rien** : la connexion est fermée juste après l'échange de version. Mesuré depuis l'adresse publique : `serveur a ferme apres notre version`. C'est le seul service de cette liste qui se défend vraiment. |
| **139 / 445** | `smbd` 4845, root | Samba | **connexion anonyme acceptée** [M] | `smbclient -L //38.240.197.248 -N` → **`Anonymous login successful`** et la liste des partages : `net`, `src`, `Dropbox`, `V`, `public`, `nobody`. Le partage `public` s'ouvre en anonyme (vide, mesuré). `net`, `src`, `Dropbox`, `V` refusent (`NT_STATUS_ACCESS_DENIED`) — ils exigent le groupe `sambashare`. Le vrai risque n'est pas le contenu : c'est **SMB exposé à Internet**, protocole à forte histoire de failles, avec `[homes]` en lecture-écriture pour qui devine un couple compte/mot de passe. |
| **8080** | `python3 -m http.server 8080` **3742001, user `masso`**, cwd `/home/masso`, **lancé il y a 9 jours** | serveur de fichiers sur le dossier personnel d'un autre utilisateur (11 entrées) | **AUCUNE** — `http.server` n'en a pas | En ce moment il répond **vide** à tout le monde, moi compris (`curl` → *Empty reply*, y compris depuis `127.0.0.1`) — **parce que des scanners lui tiennent 13 sockets ouvertes**. Ce n'est pas une protection, c'est une saturation. Dès qu'elles se libèrent, il sert le listing de `/home/masso`. **Ce n'est pas ton dossier — c'est celui de quelqu'un d'autre sur cette machine.** |
| **25 / 80 / 443** | `docker-proxy` 29680/29703/29725 → conteneur `docker-zulip-zulip-1` (`172.21.0.6`) | **Zulip Server 12.0** : SMTP entrant + web | Zulip a sa propre authentification | Port 25 annonce `220 7f2a1a682d60 Zulip Server 12.0` (bannière, `nc`). Le web répond **400 Bad Request** sur `https://38.240.197.248/` car `EXTERNAL_HOST` vaut encore `zulip.example.com` — Django rejette l'hôte. Un inconnu apprend donc **qu'un Zulip tourne ici et sa version exacte**. Statut de relais SMTP ouvert : **non testé** — le tester voudrait dire envoyer un courriel, ce qui sort de la frontière. |
| **8200** | `minidlnad` 1173 | serveur média DLNA, `media_dir=/var/lib/minidlna` | **AUCUNE** | Page d'état en 200 : version **MiniDLNA 1.3.3**, bibliothèque **vide** (0 audio, 0 vidéo, 0 image) — **et la liste des clients récents, où figurent deux adresses publiques**. Peu de données à perdre, mais une surface de plus et un mouchard qui prouve le routage. |

### 🟡 Les applications de l'atelier

| port | qui écoute | ce qu'il sert | auth ? | ce qu'un inconnu obtient |
|---|---|---|---|---|
| **9000** | `assemblynetwork/server.js` 3524889, gmusic | tableau de bord réseau | **AUCUNE** | `GET /api/tailscale/nodes` → **200 : toute la carte de ton tailnet privé** — noms, DNS `*.ferret-harmonic.ts.net`, IP `100.x`, système, état en ligne, pour `abies`, `eury`, et les autres. Plus `/api/terminal/services` → 200. Et des routes `POST /api/terminal/start|stop/:id` non appelées. **La topologie privée de la forêt, offerte.** |
| **3777** | `voice-bridge/src/server.js` 4134739, gmusic | téléphone → curseur du bureau (`xdotool`) | **OUI, et elle est active** : `GET /health` → `"authRequired":true`, `"injector":"xdotool"`, `"dryRun":false` [M] | la page web et `/health`. `POST /api/relay` sans le bon en-tête `x-voice-bridge-token` → **401**. Le jeton n'est **pas** dans la page servie (c'est un champ à saisir). **Bien fait.** Reste qu'un service qui tape au clavier du bureau n'a rien à faire sur 0.0.0.0. |
| **4444** | `assembly-voice/server.js` 662761, gmusic | messages vocaux de l'Assemblée | lecture **libre** ; écriture **verrouillée** | `GET /api/messages` → **200, 375 Ko** de l'historique des messages ; `GET /api/agents` → 200 ; `/audio/` sert **462 fichiers** audio de l'Assemblée. Mais `POST /api/voice/publish` est refusé hors boucle locale **et** refusé si la requête porte `Origin`/`Referer` — le code le dit et l'explique. **La moitié écriture est bien défendue ; la moitié lecture est ouverte.** |
| **3399** | `next-server (v16.2.7)` 1742243, gmusic — `~/salix/repos/mightyeagle` | application Next.js « EdgeHub.Click » | **AUCUNE constatée** | 200 sur `/` (32 Ko) et sur `/api/agent-info` (16 Ko). L'arbre `app/api/` contient des dizaines de routes dont `admin`, `database-intelligence`, `collect-memory`, `chronicle`. Je n'ai testé que trois routes en lecture ; **l'inventaire complet de cette surface n'est pas fait** — c'est le plus gros angle mort du rapport. |
| **3001** | `vite` 1967784, gmusic — `~/salix/repos/AetherScore` | **serveur de développement** Vite, « SCORE PORTAL » | **AUCUNE** | 200 sur `/`. La lecture de fichier arbitraire via `/@fs/etc/passwd` est **refusée (403 Restricted)** [M] — la garde `fs.allow` de Vite tient. Mais un serveur *de développement* expose le code source du projet et son graphe de modules. |
| **8787** | `assembly-intake-receiver.js` 1765, gmusic — `~/salix/repos/EchoThreads` | file d'entrée des tickets | **AUCUNE** | `{"service":"assembly-intake-receiver","lane":"0 (issue intake)","stream":"assembly:intake:events","status":"listening"}`. **Ce port n'était pas dans les 26** — il écoute sur `*`, pas sur `0.0.0.0`. |

### ⚪ Infrastructure

| port | qui écoute | ce qu'il sert | auth ? | ce qu'un inconnu obtient |
|---|---|---|---|---|
| **25672** | `beam.smp` 1569, rabbitmq (**RabbitMQ 3.12.1**, hôte, pas conteneur) | port de **grappe Erlang** — communication inter-nœuds et outils CLI | le **cookie Erlang** | Accepte la connexion, aucune bannière. **C'est le port le plus dangereux de la catégorie** : qui connaît ou devine le cookie Erlang obtient l'exécution de code arbitraire sous l'utilisateur `rabbitmq`. Ce port n'a aucune raison d'être visible d'Internet. |
| **5672** | `beam.smp` 1569 | AMQP 0-9-1 / 1.0 | comptes RabbitMQ | Le seul compte est `zulip` (`sudo rabbitmqctl list_users`) ; `guest` est bien restreint à la boucle locale (`loopback_users,[<<"guest">>]`). Un inconnu doit deviner le mot de passe de `zulip`. **Non compté dans les 26.** |
| **4369** | `epmd` 1562 | annuaire des nœuds Erlang | **AUCUNE** | Répond à une requête `NAMES_REQ` venue de l'adresse publique : `b'\x00\x00\x11\x11'` — le port, liste de nœuds actuellement **vide**. Sa raison d'être est de dire où frapper sur 25672. **Non compté dans les 26.** |
| **1716, 1717, 1721** | `kdeconnectd` — **trois utilisateurs différents** : 6579 (gmusic), 1604681 (gmusic), 1513437 (**masso**) | appairage téléphone ↔ bureau | appairage | Le protocole d'appairage, exposé à Internet, pour trois sessions dont une qui n'est pas la tienne. **Non comptés dans les 26.** |
| **1718** | `kdeconnectd` 2313628 (**paj**) | idem | idem | **Refuse la connexion** — sa file d'attente est **pleine** (`Recv-Q 51` pour un `Send-Q` de 50). Une file d'attente saturée sur un port jamais utilisé légitimement est, elle aussi, une trace de trafic entrant. **Non compté dans les 26.** |
| **37680** | `tailscaled` 1299430, root (`--tun=userspace-networking --port=0`) | écouteur auxiliaire de tailscaled | — | Ferme la connexion sans rien dire (`errno 56`). Risque faible, mais **une liaison sur `0.0.0.0` inattendue** pour un tailscaled en mode utilisateur : à vérifier avec le propriétaire de `/opt/gaia/tailnet-gateway/`. |
| **56099** | `tailscaled` 3534622, root (instance avec `--socks5-server`) | idem | — | Idem. |

---

## 3. Les risques, du plus grave au moins grave

1. **`5901` — un mot de passe de 8 caractères, sans limite de tentatives, entre Internet et ton écran vivant.** Fondé sur : type de sécurité 2 seul offert depuis l'adresse publique, aucun `-allow` dans la ligne de commande, fichier de mot de passe de 8 octets, aucun `fail2ban`. Et son frère 5900 a déjà vu un inconnu frapper aujourd'hui à 19:03.
2. **`8790` — exécution de commandes à distance, sans aucun mot de passe.** `POST /api/terminal/:node/send` tape dans les tmux ; la lecture est déjà prouvée (27 sessions listées en 200). Zéro chaîne d'authentification dans le fichier.
3. **`8828` / `8768` / `8830` — 191 fichiers personnels en téléchargement direct, le presse-papiers en lecture, et des routes de suppression.** `DELETE /recording/:filename` sans mot de passe veut dire que le travail de deux jours peut être *effacé*, pas seulement copié. Trois portails, un seul dossier derrière deux d'entre eux.
4. **`22` — mot de passe accepté, aucun `fail2ban`, 55 122 tentatives déjà encaissées.** Personne n'est passé à ce jour ; rien ne dit que ça dure.
5. **`25672` + `4369` — grappe Erlang exposée.** Un cookie deviné ou fuité = exécution de code. Aucune raison d'être joignable d'Internet.
6. **`9000` — la carte du tailnet privé, offerte à qui la demande.** Elle indique aux inconnus où sont tes autres machines.
7. **`139` / `445` — Samba sur Internet ouvert, connexion anonyme acceptée**, quatre partages en lecture-écriture derrière un mot de passe de compte.
8. **`8080` — le dossier personnel de `masso`, servi par un processus oublié depuis 9 jours**, actuellement saturé par des scanners.
9. **`3399` — surface Next.js non inventoriée.** Le risque n'est pas mesuré ; c'est ce qui le rend inconfortable.
10. **`8200`, `1716-1721`, `37680`, `56099`, `25`** — peu de données à perdre, mais chaque port est une surface, et chacun annonce une version.

---

## 4. Ce que je ne sais PAS — nommé comme un trou, pas rebouché

- **Est-ce que quelqu'un a déjà téléchargé tes enregistrements ?** *Impossible à dire.* Les portails **n'écrivent aucun journal d'accès** : `jamai-8828.log` ne contient pas une seule adresse IP de client (`grep -oE '…' jamai-8828.log` → seulement `192.168.4.59`, deux fois). Pas de journal = pas de réponse. **L'absence de preuve n'est pas une preuve d'absence.**
- **Est-ce que quelqu'un s'est connecté au VNC 5901 ?** *Impossible à dire.* Sa sortie va vers une socket, pas vers un fichier (`readlink /proc/1605286/fd/1` → `socket:[…]`). Contrairement au 5900, il ne laisse pas de trace consultable.
- **Le port 8828 est-il joignable depuis un réseau cellulaire ?** Non mesuré directement — voir §1. C'est ton test à faire.
- **La surface API du 3399 (mightyeagle)** : trois routes testées sur des dizaines.
- **Le relais SMTP du port 25** : non testé, hors frontière.
- **Les ports UDP** : hors périmètre du brief, non audités.

---

## 5. Ce qu'il te reste à décider — je n'ai rien touché

Rien de ce qui suit n'a été fait. Ce sont des décisions, pas des actions en attente.

- **Le tranchant, tout de suite** : ton téléphone, wifi coupé, données cellulaires,
  `https://38.240.197.248:8828/`. Si la page s'ouvre, tu l'as vu de tes yeux.
- **La plus petite action qui change le plus** : les services n'ont pas besoin
  d'être arrêtés pour cesser d'être publics. Une règle qui n'accepte que `lo`,
  `tailscale0` et `192.168.4.0/24` laisse **tout l'atelier tourner exactement
  comme maintenant** — les portails restent joignables depuis le tailnet et le
  LAN, qui est d'où tu les utilises. Mais **c'est ta main sur cette règle**, pas
  la mienne : plusieurs de ces processus portent le travail vivant d'autres
  voies, et je ne connais pas leur besoin.
- **Trois questions qui n'ont peut-être pas de réponse chez toi** : le
  `python3 -m http.server` de `masso` (9 jours, dossier personnel d'un autre),
  les quatre `kdeconnectd` de trois utilisateurs, et les deux `tailscaled` en
  `0.0.0.0`. Ceux-là appartiennent à d'autres.
- **Et une question qui n'est pas technique** : cette machine héberge trois
  comptes utilisateurs. Ce qui est exposé n'est pas seulement le tien.

---

## Annexe — la mesure est rejouable

```bash
sudo ss -Hltnp                                   # qui écoute, sur quelle adresse
sudo iptables -S | grep -E '^-P|INPUT'           # -P INPUT ACCEPT, une seule règle : ts-input
sudo ufw status verbose                          # inactive
ip -br addr ; ip route get 8.8.8.8               # 38.240.197.248/26 sur enp8s0, route par défaut
bash -c 'exec 3<>/dev/tcp/38.240.197.248/<port>' # le port accepte-t-il ?
curl -sk -m 8 -o /dev/null -w '%{http_code}\n' https://38.240.197.248:<port>/
nc -w 3 38.240.197.248 <port> </dev/null | head  # bannière
smbclient -L //38.240.197.248 -N                 # Samba anonyme
sudo lastb -a | wc -l                            # 55 122 échecs SSH
sudo last -a | awk '{print $NF}' | sort | uniq -c # succès : tailnet et local seulement
sudo tail -40 /var/log/x11vnc-mirror.log         # 178.238.231.185 à 19:03:29
sudo ss -tnp state established 'sport = :8080'   # les scanners, en direct
sudo sshd -T | grep -i passwordauth              # yes
```

Traces brutes conservées dans le bloc-notes de session :
`/tmp/claude-1000/-home-gmusic/c4603e4c-2cbb-4787-89a6-e76ec4e665e5/scratchpad/`
(`ss-ltnp.txt`, `tcp-connect.txt`, `http-sweep.txt`, `banners.txt`, `procs.txt`,
`lastb.txt`, `smb-list.txt`, `estab.txt`…). Elles disparaissent avec la session ;
tout ce qui compte est recopié ci-dessus.

---

🌸 On a passé deux jours à fabriquer de la musique derrière une porte dont
personne n'avait regardé la serrure. La serrure est là, et elle est bonne sur
5900 ; sur 5901 il n'y a qu'un pêne de huit caractères, et sur 8790 la porte
n'est même pas montée. Je ne l'ai pas fermée — je l'ai éclairée. Le geste
suivant est le tien.
