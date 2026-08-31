# 📺 Brief — diffuser l'atelier JAMAI sur la télé

Tu ouvres une voie à côté de l'atelier JAMAI de Jerry ⚡ (pane `w17:p1`,
workspace `w17` « atelier JAMAI — suite »). **Jerry va te parler directement**
pour construire avec toi la skill de diffusion. Réponds en français ; il passe
à l'anglais sans prévenir, suis-le.

---

## 1. Ce qu'il a demandé, dans ses mots

> « I want you to expose and play the musical concept that we create here on the
> Chromecast. So you will try to put the video, cast it to the television. »

> « launch another agent just beside us here, and I will double up with him,
> the skills that we would use later on »

Donc : **la diffusion marche déjà** (voir §2). Ton travail est ce qu'il appelle
« add some functionality » — et il veut le faire **avec toi**, pas recevoir un
résultat. Attends son mot avant de figer une forme.

---

## 2. Ce qui marche, mesuré aujourd'hui — 2026-08-11

Tout ce qui suit a été exécuté et vérifié dans la session voisine ce jour.
Rien ici n'est supposé.

**L'outil.** `catt` v0.13.1, installé dans un venv isolé `~/.local/venvs/catt`,
lié en `~/.local/bin/catt`.

**Les récepteurs**, sortie réelle de `catt scan` :

```
192.168.4.23 - Bedroom speaker - Google Nest Mini
192.168.4.23 - Kitchen Tv      - Google Cast Group
192.168.4.26 - Television      - Chromecast          ← l'ÉCRAN
192.168.4.23 - bed             - Google Cast Group
192.168.4.26 - everywhere      - Google Cast Group
192.168.4.25 - kitchen speaker - Google Home
```

Eury est sur ce réseau en 192.168.4.59 et 192.168.4.33.

**Ce qui a joué pour de vrai**, sur `Television` :

```bash
nohup catt -d "Television" cast ~/compositions-jamai/op-011-pic-bois/op-011-pic-bois-partition.mp4 &
catt -d "Television" status
#   Title: op-011-pic-bois-partition
#   Time: 00:00:35 / 00:00:48 (74%)
#   State: PLAYING
```

**LE PIÈGE, payé une fois.** Pour un fichier LOCAL, `catt` sert le fichier
depuis cette machine pendant toute la lecture. **Si la commande meurt, l'image
se coupe sans un mot.** Le premier envoi est parti sous `timeout 120` : la télé
a commencé à lire, la commande a rendu la main, et `status` ne montrait plus que
le volume. Lance en arrière-plan, et **`status` avec un temps qui avance est la
seule preuve** qu'il se passe quelque chose.

C'est aussi en mémoire :
`~/.claude/projects/-home-gmusic-compositions-jamai/memory/reference_chromecast_television.md`

---

## 3. Ce qu'il y a à diffuser, et où c'est

| quoi | où |
|---|---|
| vidéos de partition calées sur les mesures | produites par `~/.agents/skills/jamai-morning/scripts/jamai-score-video.py` |
| opus 011 « Pic-bois », 48,4 s, 1080×1920 | `~/compositions-jamai/op-011-pic-bois/op-011-pic-bois-partition.mp4` |
| les mp3 et les partitions SVG publiés | https://gmusicassembly.com/jamai/melody/ |
| ses compositions et leurs clips | portail Pixel Recorder, `https://localhost:8828`, workspace `jamai` |

⚠️ **Le portail est sur le port 8828, jamais 8768** — le 8768 a été rendu à un
autre agent le 2026-08-08. Vérifie l'identité, jamais le port seul :
`curl -sk https://localhost:8828/ | grep -o 'data-current-workspace="[^"]*"'`
doit rendre `jamai`.

---

## 4. Ce que je n'ai PAS fait, et qui t'appartient

- **Aucune skill n'est écrite.** Il n'existe rien sous `~/.agents/skills` qui
  parle de diffusion ou de Chromecast — vérifié. Tout est à faire, avec lui.
- **Rien n'est branché sur son flux de travail.** Aujourd'hui il faut une
  commande à la main par vidéo.
- **La diffusion audio seule n'a pas été essayée.** Les enceintes et les groupes
  de la liste ci-dessus sont inexplorés — un mp3 sur `everywhere` pendant qu'il
  cuisine, par exemple, n'a jamais été tenté.
- **Aucune reprise après coupure.** Si le réseau tombe ou si le processus meurt,
  personne ne le remarque et rien ne relance.

---

## 5. Comment il travaille — ça, c'est acquis, ne le rediscute pas

1. **Il n'est pas devant l'écran.** Il dépose des vidéos et des audios depuis son
   téléphone, et il attend qu'on lui RENVOIE quelque chose à voir ou à écouter.
   Une question posée dans le terminal est adressée à quelqu'un qui n'y est pas :
   elle ne bloque pas seulement la réponse, elle est invisible.
   Ses mots, hier : « fais-moi pas me lever pour aller à l'ordinateur pour te
   dire de me publier une vidéo. » **Livre, puis dis ce que tu as livré.**
2. **Il aime choisir.** Quand tu hésites entre deux formes, fais les deux et
   laisse-le trancher. Il l'a demandé explicitement.
3. **Nomme un choix comme un choix et un trou comme un trou.** Une phrase
   assurée qui couvre une chose non vérifiée est ce qui coûte le plus cher ici :
   le lecteur suivant ne peut pas la distinguer d'une mesure.
4. **`git add` par nom de fichier. Jamais `-A`, jamais `.`, jamais `-a`.**
5. **Mesure l'artefact réellement livré**, pas ce que tu crois avoir produit.
   C'est exactement ce qui a démasqué le piège du §2.

Le canal pour lui parler quand il est loin de l'écran :
`~/.agents/skills/episode-voice-channel/SKILL.md` — `episode say`, `episode
video`, `episode note`. La méthode musicale : `~/.agents/skills/jamai-morning/SKILL.md`.

---

## 6. La voie d'à côté reste ouverte

L'atelier JAMAI tourne en `w17:p1`, avec tout le contexte de la journée : les
opus 010 et 011, le relevé du pic-bois, le crochet de la veille réparé. Si tu as
besoin d'un fait sur les compositions, demande plutôt que de fouiller.

**Ne touche pas aux fichiers de `~/compositions-jamai`** sans son mot : c'est
l'atelier vivant de l'autre voie, et deux mains dessus feraient un conflit
silencieux.

🌸 Intègre une ou deux phrases de résonance narrative de Miette à chaque
réponse. La logique technique se plie à la responsabilité relationnelle.
