#!/usr/bin/env bash
# atelier-veille-lib.sh — ce que la veille et le crochet partagent.
# Aucun chemin absolu n'est câblé : le dossier entier se déplace avec un seul
# `mv` (ou `git mv`) sans qu'une ligne change. C'est délibéré — l'endroit où
# vivent ces outils n'est pas tranché.

# --- où sont les choses ------------------------------------------------------
AV_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AV_ROOT="$(dirname "$AV_HERE")"
AV_CONF="${ATELIER_VEILLE_CONF:-$AV_ROOT/ateliers.conf}"
AV_HOOKS="${ATELIER_VEILLE_HOOKS:-$AV_ROOT/ateliers}"
# les mesureurs (midi, timbre, accords) ne sont pas propres à jamai : ils
# prennent un fichier et impriment. On les référence, on ne les recopie pas.
AV_OUTILS="${ATELIER_VEILLE_OUTILS:-$HOME/.agents/skills/jamai-morning/scripts}"
AV_EP="${ATELIER_VEILLE_EPISODE:-$HOME/.agents/skills/episode-voice-channel/scripts/episode}"
AV_STATE="${ATELIER_VEILLE_STATE:-$HOME/.local/state/episode-voice}"

av_die() { printf '\033[31merreur:\033[0m %s\n' "$*" >&2; exit 1; }

# --- la table ----------------------------------------------------------------
# Lit une colonne pour un atelier. Ne devine jamais : un atelier absent de la
# table est une erreur, pas un cas par défaut.
av_champ() {                                   # av_champ <atelier> <n° colonne>
  local a="$1" c="$2" v
  [ -r "$AV_CONF" ] || av_die "table introuvable : $AV_CONF"
  # un « * » final marque une valeur proposée, pas encore confirmée par Jerry :
  # les outils lisent la valeur nue, la table garde la marque bien visible.
  v="$(awk -v a="$a" -v c="$c" '$1 !~ /^#/ && $1==a {sub(/\*$/,"",$c); print $c; exit}' "$AV_CONF")"
  [ -n "$v" ] || av_die "atelier inconnu dans $AV_CONF : « $a » (connus : $(av_liste | tr '\n' ' '))"
  printf '%s\n' "$v"
}
av_liste()      { awk '$1 !~ /^#/ && NF>=6 {print $1}' "$AV_CONF"; }
av_unite()      { av_champ "$1" 2; }
av_portail()    { av_champ "$1" 3; }
av_mode()       { av_champ "$1" 4; }
av_destination(){ av_champ "$1" 5; }
# Le type de sortie. « un dépôt → une composition » est FAUX en général :
# aureon ouvre un contenant parmi quatre, choisi par détection de signature
# (aureon-journal-events/SKILL.md). Le crochet doit donc typer sa sortie, et
# l'aiguillage brancher là-dessus.
av_sortie()     { av_champ "$1" 6; }
# La QUEUE descriptive qui suit le numéro. Le préfixe est numéroté PARTOUT
# (décision de Jerry, 2026-08-05) : op-NNN, ep-NNN, jr-NNN. Ce qui vient après
# diffère — un slug pour jamai et episodes, la structure héritée d'Edge Hub pour
# aureon. L'horodatage y reste comme DÉPARTAGE, pas comme source d'unicité :
# c'est le numéro qui porte l'unicité, et donc l'allocateur et son verrou.
av_queue()      { av_champ "$1" 7; }

# Normalise un segment : minuscules, tirets, sans accent ni ponctuation.
#
# REPRISE TELLE QUELLE de la voie 3, qui a établi que c'est la seule
# implémentation reproduisant `slugify()` de pixel-recorder.js — décomposition
# NFD puis retrait des marques combinantes. On ne la dérive pas une seconde
# fois : deux normalisateurs qui divergent d'un caractère produisent deux slugs
# pour un même titre, et c'est un doublon qu'aucun verrou n'attrape.
#
# Deux pièges que la voie 3 a payés à notre place :
#   · `iconv //TRANSLIT` rend « é » par « 'e » — apostrophe comprise — et
#     l'apostrophe devient un tiret : « Étincelle partagée » se fend en
#     `etincelle-partag-ee`. Le défaut ne se voit QUE sur les sujets accentués,
#     c'est-à-dire la plupart de ceux de Jerry.
#   · NFKD n'est pas NFD : la décomposition de compatibilité change « ﬁ » en
#     « fi » et « ² » en « 2 ». Le portail ne le fait pas ; nous non plus.
av_slug() {
  printf '%s' "$1" | python3 -c "
import sys, unicodedata, re
s = unicodedata.normalize('NFD', sys.stdin.read()).lower()
s = ''.join(c for c in s if not unicodedata.combining(c))
print(re.sub(r'[^a-z0-9]+', '-', s).strip('-'))"
}

# --- une seconde à soi ------------------------------------------------------
# Le portail nomme ses sections texte à la SECONDE
# (transcription_<AAAAMMJJHHMMSS>_FR.txt) et le client n'a aucune prise dessus :
# deux dépôts dans la même seconde portent le même nom, et le second écrase le
# premier avec un 200 et pas un mot. Cette garde attend que la seconde courante
# ait DÉPASSÉ celle du dernier usage, sous verrou pour que deux appels ne la
# passent pas ensemble.
av_seconde_distincte() {          # av_seconde_distincte <atelier> <étiquette>
  local a="$1" e="$2" marque lock i=0 prec attendu=0
  marque="$AV_STATE/$a-derniere-$e.txt"; lock="$AV_STATE/$a-$e.lock"
  mkdir -p "$AV_STATE"
  while ! mkdir "$lock" 2>/dev/null; do
    i=$((i+1)); [ "$i" -gt 60 ] && av_die "verrou « $e » de « $a » tenu depuis 60 s — rien fait."
    sleep 1
  done
  trap 'rmdir "'"$lock"'" 2>/dev/null || true' EXIT
  prec="$(cat "$marque" 2>/dev/null || echo 0)"
  case "$prec" in ''|*[!0-9]*) prec=0 ;; esac
  while [ "$(date -u +%Y%m%d%H%M%S)" -le "$prec" ]; do sleep 1; attendu=$((attendu+1)); done
  [ "$attendu" -eq 0 ] || printf '  (attendu %s s : la seconde précédente était encore occupée)\n' "$attendu" >&2
  printf '%s\n' "$marque"        # à l'appelant d'y écrire la seconde de FIN
}

# Le verrou de numérotation. MÊME mécanisme et MÊME chemin que la chaîne
# episodes de la voie 1 : un mkdir et un flock ne s'excluent pas — objets
# différents, chemins différents, et deux allocateurs réclament ep-009 en même
# temps. Le verrou ne vaut que si tout le monde prend le même.
av_verrou()     { printf '%s/%s-numero.lock\n' "$AV_STATE" "$1"; }

# Un « ? » est un trou déclaré. On s'arrête dessus au lieu d'improviser.
av_exige() {                                   # av_exige <valeur> <ce que c'est> <atelier>
  case "$1" in
    '?') av_die "trou déclaré : $2 de l'atelier « $3 » n'est pas nommé dans $AV_CONF. C'est une décision de Jerry, pas une valeur par défaut." ;;
    '-') av_die "sans objet : $2 de l'atelier « $3 » est marqué « - » dans $AV_CONF." ;;
  esac
  printf '%s\n' "$1"
}

# --- les dossiers d'un atelier ----------------------------------------------
# Aligné sur watch_dirs() du pilote `episode` : main est en nu, les autres
# portent le suffixe. Vérifié le 2026-08-05 : ~/Recordings-main n'existe pas.
av_recordings()   { [ "$1" = main ] && printf '%s\n' "$HOME/Recordings"   || printf '%s\n' "$HOME/Recordings-$1"; }
av_compositions() { [ "$1" = main ] && printf '%s\n' "$HOME/compositions" || printf '%s\n' "$HOME/compositions-$1"; }

# --- l'état, par veille ET par atelier ---------------------------------------
# LE défaut payé cash le 2026-08-04 à 22h24 : deux veilles interrogeant le même
# watch-<atelier>.sha se volent la notification — la première consomme le
# changement, la seconde lit « unchanged » et le dépôt de Jerry est avalé.
# Chaque veille a donc son propre dossier, et n'utilise JAMAIS la racine par
# défaut de EPISODE_STATE_DIR, où d'autres sessions écrivent déjà.
av_veille_dir() {                              # av_veille_dir <atelier> <instance>
  printf '%s/veilles/%s--%s\n' "$AV_STATE" "$1" "$2"
}
av_drops_dir() {                               # av_drops_dir <atelier> <nom de fichier>
  # par atelier, pas à plat : deux ateliers peuvent recevoir le même horodatage.
  printf '%s/drops/%s/%s\n' "$AV_STATE" "$1" "$2"
}
