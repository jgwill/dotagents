#!/usr/bin/env python3
"""partition-video.py — vidéo de partition qui suit la musique, système par système.

Le défilement linéaire de `episode video` fait glisser la page à vitesse constante
devant une fenêtre de 720 px. Deux défauts mesurés le 2026-08-07 sur l'opus 006 :

  1. la fenêtre (720 px) est PLUS PETITE qu'un système (792 px de moyenne) :
     aucune ligne de la partition n'est jamais visible en entier ;
  2. la page défile en proportion des PIXELS, pas des MESURES. Les systèmes
     n'ont pas tous le même nombre de mesures, donc l'image court devant la
     musique par endroits et traîne ailleurs.

Ici : on découpe la page en systèmes, on compte les barres de mesure de chacun,
et on affiche chaque système IMMOBILE pendant exactement la durée de ses mesures.
Le regard a le temps de lire, et la page tourne quand la musique tourne.

  partition-video.py --score p.png --audio p.mp3 --bar-seconds 2.069 --out v.mp4
"""
import argparse, os, subprocess, sys, tempfile
from PIL import Image


def systemes(im, ecart=25):
    """Bandes de lignes encrées, séparées par >=`ecart` lignes blanches.

    L'écart entre deux systèmes dépend du nombre de portées. Sur les huit
    portées de l'opus 006, 25 lignes blanches séparent bien les systèmes ; sur
    une grille à deux portées, l'écart réel tombe sous 18 et quatre systèmes
    fusionnent en un. AUCUNE constante ne convient aux deux — d'où `--bars`.
    """
    w, h = im.size
    px = im.load()
    prof = [sum(1 for x in range(0, w, 4) if px[x, y] < 200) for y in range(h)]
    blocs, debut, blanc = [], None, 0
    for y, v in enumerate(prof):
        if v > 0:
            if debut is None:
                debut = y
            blanc = 0
        elif debut is not None:
            blanc += 1
            if blanc >= ecart:
                blocs.append((debut, y - blanc))
                debut, blanc = None, 0
    if debut is not None:
        blocs.append((debut, h - 1))
    return [b for b in blocs if b[1] - b[0] > 60]


def mesures(im, bande):
    """Nombre de mesures d'un système = barres verticales traversantes − 1.

    Les colonnes fusionnées à moins de 12 px comptent pour une : une double
    barre finale « |] » en donne deux distantes de ~9 px et gonflerait le total.
    """
    w, _ = im.size
    px = im.load()
    y0, y1 = bande
    H = (y1 - y0) / 3
    ratios = [sum(1 for y in range(y0, y1, 3) if px[x, y] < 128) / H for x in range(w)]
    # Seuil RELATIF à la page, pas fixe. Une barre de mesure ne traverse pas la
    # même proportion de la bande selon le nombre de portées : sur les huit
    # portées de l'opus 006 elle frôle 1,0, sur les deux portées d'une grille
    # elle tombe à 0,67. Un seuil fixe à 0,75 rendait alors 1 mesure au lieu
    # de 11 — sans erreur, et la vidéo tenait 33 s sur un seul système.
    pic = max([r for x, r in enumerate(ratios) if x > 90] or [0])
    seuil = max(0.50, pic * 0.85)
    cand = [x for x in range(w) if x > 90 and ratios[x] >= seuil]
    groupes = []
    for x in cand:
        if groupes and x - groupes[-1][-1] <= 12:
            groupes[-1].append(x)
        else:
            groupes.append([x])
    xs = [sum(g) // len(g) for g in groupes]
    return max(len(xs) - 1, 1)


def debut_des_portees(im, bande):
    """Où commencent les portées dans un système — le titre n'en fait pas partie.

    Une ligne de portée traverse la page ; une ligne de titre non. Sans ça, le
    premier système est gonflé par le bloc de titre et doit être réduit pour
    tenir dans le cadre : les notes y seraient plus petites qu'ailleurs.
    """
    w, _ = im.size
    px = im.load()
    y0, y1 = bande
    ligne = None
    for y in range(y0, y1):
        if sum(1 for x in range(0, w, 4) if px[x, y] < 200) > w / 4 / 2:
            ligne = y                      # première ligne de portée : traverse la page
            break
    if ligne is None:
        return y0
    # Remonter jusqu'au blanc franc qui sépare le titre des portées. Un simple
    # « ligne − 30 » coupait DANS le bloc de titre : les descendantes des lettres
    # entraient en haut du cadre. Au-dessus de la portée il y a d'abord l'encre
    # des notes hautes et de l'indication de tempo, puis du vide, puis le titre.
    blanc = 0
    for y in range(ligne, y0, -1):
        if sum(1 for x in range(0, w, 4) if px[x, y] < 200) == 0:
            blanc += 1
            if blanc >= 10:
                return y + blanc // 2
        else:
            blanc = 0
    return y0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--score', required=True)
    ap.add_argument('--audio', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--bar-seconds', type=float, required=True)
    ap.add_argument('--w', type=int, default=1920)
    ap.add_argument('--h', type=int, default=1080)
    ap.add_argument('--bars', type=int,
                    help="nombre de mesures compté dans la source ABC. Donné, "
                         "l'outil cherche le découpage qui le retrouve et REFUSE "
                         "s'il n'y arrive pas, au lieu de sortir un montage faux.")
    a = ap.parse_args()

    im = Image.open(a.score).convert('RGB')
    gris = im.convert('L')            # la détection lit des niveaux, pas des triplets

    def decoupe(ec):
        b = systemes(gris, ec)
        p = [(debut_des_portees(gris, x), x[1]) for x in b]
        return b, p, [mesures(gris, x) for x in p]

    if a.bars:
        # Le compte de la source fait foi. On cherche l'écart qui le retrouve.
        trouve = None
        essais = []
        for ec in (25, 22, 20, 18, 16, 14, 12, 10):
            b, p, n = decoupe(ec)
            essais.append((ec, len(b), sum(n)))
            if sum(n) == a.bars:
                trouve = (ec, b, p, n)
                break
        if not trouve:
            print(f"REFUS : aucun découpage ne retrouve les {a.bars} mesures de la source.",
                  file=sys.stderr)
            for ec, ns, tot in essais:
                print(f"   écart {ec:2d} lignes → {ns} systèmes, {tot} mesures", file=sys.stderr)
            print("Un montage bâti sur un mauvais compte tient la page au mauvais",
                  "moment, sans erreur visible. Corrige la détection ou la source.",
                  file=sys.stderr)
            sys.exit(1)
        ec, bandes, portees, nb = trouve
        print(f"découpage vérifié : écart {ec} lignes retrouve les {a.bars} mesures de la source")
    else:
        bandes, portees, nb = decoupe(25)
        print("⚠ compte de mesures NON vérifié — passe --bars <n> depuis la source ABC")
    if not bandes:
        sys.exit('aucun système détecté')

    dur = float(subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'csv=p=0', a.audio], capture_output=True, text=True).stdout.strip())

    # Compter les barres SUR LES PORTÉES seulement. Le premier système porte le
    # bloc de titre : inclus dans la bande, il dilue le ratio d'encre vertical
    # et seules les barres les plus longues passent le seuil. L'opus 005 sortait
    # ainsi à 1 mesure au lieu de 4 — sans erreur, et le premier système aurait
    # été balayé en deux secondes.
    total = sum(nb)
    print(f"{len(bandes)} systèmes, {total} mesures, audio {dur:.1f} s "
          f"({a.bar_seconds:.3f} s/mesure → {total * a.bar_seconds:.1f} s de musique)")

    tmp = tempfile.mkdtemp()
    lignes, t = [], 0.0
    for i, (bande, n) in enumerate(zip(bandes, nb)):
        y0 = portees[i][0] if i == 0 else bande[0] - 20
        y1 = bande[1] + 20
        vue = im.crop((0, max(y0, 0), im.width, min(y1, im.height)))
        # Agrandir au maximum sans déborder, puis centrer sur fond blanc.
        k = min(a.w / vue.width, a.h / vue.height)
        vue = vue.resize((int(vue.width * k), int(vue.height * k)), Image.LANCZOS)
        cadre = Image.new('RGB', (a.w, a.h), 'white')
        cadre.paste(vue, ((a.w - vue.width) // 2, (a.h - vue.height) // 2))
        p = os.path.join(tmp, f's{i:02d}.png')
        cadre.save(p)

        d = n * a.bar_seconds
        # Le dernier système reste à l'écran pendant la queue de résonance :
        # sinon la vidéo se termine sur du noir alors que l'accord sonne encore.
        if i == len(bandes) - 1:
            d = max(dur - t, d)
        lignes.append(f"file '{p}'\nduration {d:.3f}")
        print(f"  système {i+1} : {n:2d} mesures · {t:6.2f} → {t+d:6.2f} s · "
              f"grossissement ×{k:.2f}")
        t += d
    lignes.append(f"file '{os.path.join(tmp, f's{len(bandes)-1:02d}.png')}'")

    liste = os.path.join(tmp, 'liste.txt')
    open(liste, 'w').write('\n'.join(lignes) + '\n')

    subprocess.run(
        ['ffmpeg', '-nostdin', '-y', '-loglevel', 'error',
         '-f', 'concat', '-safe', '0', '-i', liste, '-i', a.audio,
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
         '-pix_fmt', 'yuv420p', '-r', '25',
         '-c:a', 'aac', '-b:a', '192k', '-shortest', a.out], check=True)
    print('→', a.out)


if __name__ == '__main__':
    main()
