#!/usr/bin/env python3
"""jamai-tab.py — tablature guitare à six lignes, depuis un fichier ABC.

`abcm2ps` a bien une directive `%%tablature`, mais elle est faite pour les
instruments à VENT : elle dessine des doigtés de flûte, de galoubet, de txistu.
Elle ne sait pas placer une case sur un manche. Testé, refusé :
« error: Wrong values in %%tablature ». Il n'y a ni abctab2ps ni lilypond sur
cette machine. Donc on la dessine.

  jamai-tab.py piece.abc --voix 1 --out tab.png

Choix de corde : la position la plus BASSE jouable, en gardant la main dans un
empan de 4 cases autour des notes voisines. Une même hauteur existe à plusieurs
endroits sur un manche — mi3 est la corde de ré case 2, la corde de sol case
-3 (impossible), ou la corde de la case 7. Sans contrainte de main, une
tablature juste sur le papier devient injouable.
"""
import argparse, re, sys
from PIL import Image, ImageDraw, ImageFont

# Cordes à vide, de la 6ᵉ (grave) à la 1ʳᵉ (aiguë), en MIDI.
CORDES = [40, 45, 50, 55, 59, 64]          # mi2 la2 ré3 sol3 si3 mi4
NOMS_CORDES = ['E', 'A', 'D', 'G', 'B', 'e']
CASES_MAX = 15


def positions(midi):
    """Toutes les (corde, case) possibles pour une hauteur, 6ᵉ corde d'abord."""
    out = []
    for i, vide in enumerate(CORDES):
        c = midi - vide
        if 0 <= c <= CASES_MAX:
            out.append((i, c))
    return out


def choisir(suite):
    """Attribue une corde à chaque note en gardant la main groupée.

    On balaie les combinaisons possibles en pénalisant l'écart de case avec la
    note précédente et l'usage de deux fois la même corde d'affilée (physiquement
    impossible sans lever le doigt).
    """
    res = []
    precedent = None
    for m in suite:
        opts = positions(m)
        if not opts:
            res.append(None)
            continue
        def cout(o):
            corde, case = o
            c = case * 0.3                       # préférer le bas du manche
            if precedent:
                c += abs(case - precedent[1]) * 1.0
                if corde == precedent[0]:
                    c += 2.5                     # même corde deux fois de suite
            return c
        best = min(opts, key=cout)
        res.append(best)
        precedent = best
    return res


def lire_voix(chemin, voix):
    """Hauteurs MIDI de la voix demandée, dans l'ordre, depuis la source ABC."""
    LET = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    arm = 0
    notes = []
    for l in open(chemin):
        if l.startswith('K:'):
            arm = 1 if 'G' in l else 0            # sol majeur : fa dièse
        if not l.startswith(f'[V:{voix}]'):
            continue
        corps = re.sub(r'"[^"]*"', '', l.split(']', 1)[1])
        for tok in re.finditer(r'([\^_=]?)([A-Ga-g])([,\']*)(\d*)', corps):
            acc, let, oct_, dur = tok.groups()
            pc = LET[let.upper()]
            if acc == '^': pc += 1
            elif acc == '_': pc -= 1
            elif acc == '' and arm and let.upper() == 'F': pc += 1
            o = 5 if let.islower() else 4
            o += oct_.count("'") - oct_.count(',')
            notes.append((o + 1) * 12 + pc)
    return notes


def dessiner(paires, sortie, largeur=1400, par_ligne=16):
    n = len(paires)
    lignes = (n + par_ligne - 1) // par_ligne
    h_ligne = 130
    im = Image.new('RGB', (largeur, 40 + lignes * h_ligne), 'white')
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
        fp = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    except OSError:
        f = fp = ImageFont.load_default()
    for li in range(lignes):
        y0 = 30 + li * h_ligne
        ecart = 17
        for s in range(6):
            y = y0 + s * ecart
            d.line([(70, y), (largeur - 30, y)], fill='black', width=1)
            d.text((40, y - 9), NOMS_CORDES[5 - s], font=fp, fill='black')
        bloc = paires[li * par_ligne:(li + 1) * par_ligne]
        pas = (largeur - 110) / max(len(bloc), 1)
        for i, p in enumerate(bloc):
            if p is None:
                continue
            corde, case = p
            x = 80 + i * pas
            y = y0 + (5 - corde) * ecart
            t = str(case)
            bb = d.textbbox((0, 0), t, font=f)
            w = bb[2] - bb[0]
            d.rectangle([x - w / 2 - 3, y - 10, x + w / 2 + 3, y + 10], fill='white')
            d.text((x - w / 2, y - 9), t, font=f, fill='black')
    im.save(sortie)
    return im.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('abc')
    ap.add_argument('--voix', default='1')
    ap.add_argument('--out', required=True)
    ap.add_argument('--par-ligne', type=int, default=16)
    a = ap.parse_args()
    notes = lire_voix(a.abc, a.voix)
    if not notes:
        sys.exit(f"aucune note trouvée pour la voix {a.voix}")
    paires = choisir(notes)
    manquantes = sum(1 for p in paires if p is None)
    print(f"{len(notes)} notes · {manquantes} injouables sur un manche standard")
    for m, p in list(zip(notes, paires))[:12]:
        print(f"   midi {m:3d} → corde {NOMS_CORDES[p[0]] if p else '?'} case {p[1] if p else '—'}")
    print("taille :", dessiner(paires, a.out, par_ligne=a.par_ligne), "→", a.out)


if __name__ == '__main__':
    main()
