#!/usr/bin/env python3
"""clip.py — vidéo clip : sa prise en fond, la partition fondue par-dessus.

Sa consigne du 14 août, en marchant : « un vidéo clip qui va passer en arrière
des partitions […] puis on voyait les partitions fondues par-dessus ».

Trois choses que ce script encode :

 1. LA PARTITION EST INVERSÉE avant d'être posée. Une partition normale est
    noire sur blanc : posée sur une vidéo, soit le blanc cache l'image, soit le
    noir disparaît dans les ombres. Inversée (blanc sur noir) et mélangée en
    mode « screen », le noir devient transparent et seules les notes s'allument
    sur l'image. C'est ce qui donne le fondu, sans masque ni découpe.

 2. SA PRISE EST VERTICALE (1080x1920, drapeau de rotation). Elle est agrandie
    à la largeur de la toile puis recadrée sur une bande horizontale choisie
    plus bas que le centre — c'est là que sont ses pieds.

 3. LE DÉFILEMENT EST LE MÊME QUE LES AUTRES VIDÉOS : par morceaux, mesure par
    mesure, avec la tête de lecture qui court jusqu'au bout. La détection des
    barres et le panoramique viennent de jamai-defile.py.

  clip.py <fond> <partition.png> <audio> <sortie.mp4> <s/mesure> <nb_mesures> [bande_y] [assombri] [partition.svg]
"""
import subprocess, sys
import numpy as np
from PIL import Image

fond, png, audio, sortie = sys.argv[1:5]
# Le 5e argument accepte soit un nombre — toutes les mesures durent pareil —
# soit une liste « 61x2.667,1x2.857,… ». La chanson finit sur un RALENTI :
# ses quatre dernières mesures durent 2,857 · 3,158 · 3,529 · 4,138 s au lieu
# de 2,667. Une seule valeur ferait dériver la tête de lecture de plusieurs
# secondes sur la fin — exactement là où il regarde.
def lire_durees(spec):
    if 'x' not in spec and ',' not in spec:
        return None, float(spec)
    out = []
    for bloc in spec.split(','):
        n, d = bloc.split('x'); out += [float(d)] * int(n)
    return out, out[0]
DUREES, SEC = lire_durees(sys.argv[5])
NB_ATTENDU = int(sys.argv[6])
# BANDE_Y : où couper dans sa prise VERTICALE une fois élargie à la toile.
# Ses prises sont filmées vers le bas en marchant ; ses pieds ne sont pas à la
# même hauteur d'une prise à l'autre, donc ça se règle prise par prise.
BANDE_Y = int(sys.argv[7]) if len(sys.argv) > 7 else 1000
# ASSOMBRI : de combien on baisse le fond pour que les notes restent lisibles.
ASSOMBRI = float(sys.argv[8]) if len(sys.argv) > 8 else 0.08
FEN_L, CANVAS_H = 1280, 720

src = Image.open(png)
im = np.array(src.convert('L') if src.mode != 'RGBA'
              else Image.fromarray(np.array(src)[...,3]))
h, w = im.shape

# ── LES POSITIONS DE MESURE VIENNENT DU SVG, PAS DES PIXELS ────────────────
# La détection au pixel marchait sur deux portées et a échoué sur trois : les
# barres ne traversent pas tout le système (plus long trait continu : 50 % de
# la hauteur seulement), et aucun seuil ne rendait 16 — 18, puis 11, puis 10.
# Le garde-fou a refusé de fabriquer la vidéo, ce qui était le bon réflexe.
#
# Mais abcm2ps écrit DÉJÀ les numéros de mesure dans le SVG, avec leur
# abscisse exacte (`%%measurenb 1`). On les lit : plus de seuil, plus de
# devinette, et ça marche quel que soit le nombre de portées.
import re
svg = sys.argv[9] if len(sys.argv) > 9 else None
if svg:
    t = open(svg).read()
    m = re.search(r'width="([\d.]+)px"\s+height="([\d.]+)', t)
    Wsvg = float(m[1])
    ech = w / Wsvg                       # le PNG est rendu à une autre échelle
    nums = sorted({int(n): float(x) for x, n in
                   re.findall(r'<text x="([\d.]+)" y="[\d.]+">(\d+)</text>', t)
                   if 1 < int(n) <= NB_ATTENDU}.items())
    if len(nums) != NB_ATTENDU - 1:
        sys.exit(f"  ✗ {len(nums)} numéros de mesure dans le SVG, {NB_ATTENDU-1} attendus")
    xs = [v * ech for _, v in nums]      # début des mesures 2..N
    pas = xs[1] - xs[0]
    X = [xs[0] - pas] + xs + [xs[-1] + (xs[-1] - xs[-2])]
    NB = len(X) - 1
    print(f"  partition {w}x{h} · {NB} mesures lues DANS LE SVG")
    if NB != NB_ATTENDU:
        sys.exit(f"  ✗ ARRÊT : {NB} mesures, {NB_ATTENDU} attendues.")
else:
    clair = im > 128
    longest = np.zeros(w, dtype=int)
    for x in range(w):
        c = clair[:, x]
        if not c.any(): continue
        best = cur = 0
        for v in c:
            cur = cur + 1 if v else 0
            if cur > best: best = cur
        longest[x] = best
    cand = np.where(longest >= int(0.25*h))[0]
    groups, cur = [], [cand[0]]
    for x in cand[1:]:
        if x - cur[-1] <= 4: cur.append(x)
        else: groups.append(int(np.mean(cur))); cur = [x]
    groups.append(int(np.mean(cur)))
    fusion = [groups[0]]
    for x in groups[1:]:
        if x - fusion[-1] < 30: fusion[-1] = x
        else: fusion.append(x)
    X = fusion; NB = len(X) - 1
    print(f"  partition {w}x{h} · {NB} mesures détectées au pixel")
    if NB != NB_ATTENDU:
        sys.exit(f"  ✗ ARRÊT : {NB} mesures détectées, {NB_ATTENDU} attendues.")

xmax = max(0, w - FEN_L)
durees = DUREES if DUREES else [SEC]*NB
if len(durees) != NB:
    sys.exit(f"  ✗ {len(durees)} durées pour {NB} mesures")
bornes = [0.0]
for d in durees: bornes.append(bornes[-1] + d)
print(f"  durée totale attendue : {bornes[-1]:.2f} s")
expr = f"{X[-1]}"
for b in range(NB-1, -1, -1):
    t0, t1 = bornes[b], bornes[b+1]
    seg = f"({X[b]}+({X[b+1]-X[b]})*(t-{t0:.3f})/{durees[b]:.3f})"
    expr = f"if(lt(t,{t1:.3f}),{seg},{expr})"
crop_x = f"clip({expr}-{FEN_L//2},0,{xmax})"
tete_x = f"({expr})-({crop_x})"
pad_y  = max(0, (CANVAS_H - h)//2)

vf = (
  # sa prise : élargie à la toile, recadrée sur la bande des pieds, assombrie
  # juste ce qu'il faut pour que les notes ressortent sans noyer l'image
  f"[0:v]scale={FEN_L}:-2,crop={FEN_L}:{CANVAS_H}:0:{BANDE_Y},"
  f"eq=brightness=-{ASSOMBRI}:saturation=1.05,format=yuv420p,setsar=1[bg];"
  # la partition : fenêtre glissante, posée sur fond noir pour le mélange
  f"[1:v]format=rgba,crop={FEN_L}:{h}:x='{crop_x}':y=0,"
  f"pad={FEN_L}:{CANVAS_H}:0:{pad_y}:color=black@0,setsar=1[sc];"
  # `overlay` compose l'alpha sans toucher aux couleurs du fond. `blend` en
  # mode screen, essayé d'abord, rendait toute l'image MAGENTA : les deux
  # entrées n'avaient pas le même espace colorimétrique et le mélange se
  # faisait canal par canal sur des plans qui ne correspondaient pas.
  f"[bg][sc]overlay=0:0[v0];"
  f"[v0][2:v]overlay=x='{tete_x}-1':y={pad_y}[v]"
)
cmd = ['ffmpeg','-v','error','-y',
       '-i', fond,
       '-loop','1','-i', png,
       '-f','lavfi','-i', f'color=red@0.8:s=3x{h},format=rgba',
       '-i', audio,
       '-filter_complex', vf, '-map','[v]', '-map','3:a',
       '-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-r','30',
       '-c:a','aac','-b:a','160k','-shortest', sortie]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode:
    print(r.stderr[-1800:]); sys.exit(1)
d = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
                    '-of','csv=p=0',sortie],capture_output=True,text=True).stdout.strip()
print(f"  → {sortie} · {d} s")
