#!/usr/bin/env python3
"""jamai-chords-audio.py — accords et tonalité depuis un ENREGISTREMENT, pas un MIDI.

`jamai-chords.py` lit un fichier MIDI, où chaque hauteur est certaine. Ici la
source est une prise réelle : une guitare, une voix par-dessus, une pièce. Il
n'y a pas de vérité exacte à en tirer, seulement une estimation — et le devoir
de dire à quel point elle est sûre.

Méthode : STFT → chromagramme pondéré par l'amplitude → appariement à des
gabarits d'accords, fenêtre par fenêtre. La tonalité vient de Krumhansl sur le
chroma cumulé.

  jamai-chords-audio.py prise.wav [--debut 0] [--fin 68] [--fenetre 1.0]

Ce que l'outil NE fait pas, et qu'il ne faut pas lui faire dire :
  - il n'entend pas la basse séparément : un G/B et un G sortiront pareils ;
  - une voix parlée par-dessus pollue le chroma — regarde la colonne « force » ;
  - les gabarits sont dans l'ordre de spécificité, donc un add9 gagne sur un
    majeur seulement s'il est nettement mieux expliqué.
"""
import argparse, math, sys, wave
import numpy as np

NOMS = ['do', 'do#', 'ré', 'ré#', 'mi', 'fa', 'fa#', 'sol', 'sol#', 'la', 'la#', 'si']
LAT  = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Gabarits, en demi-tons depuis la fondamentale. L'ordre compte : le premier qui
# gagne nettement l'emporte, sinon on garde le plus simple.
GABARITS = [
    ('',      [0, 4, 7]),
    ('m',     [0, 3, 7]),
    ('sus4',  [0, 5, 7]),
    ('sus2',  [0, 2, 7]),
    ('7',     [0, 4, 7, 10]),
    ('maj7',  [0, 4, 7, 11]),
    ('m7',    [0, 3, 7, 10]),
    ('add9',  [0, 2, 4, 7]),
    ('madd9', [0, 2, 3, 7]),
    ('6',     [0, 4, 7, 9]),
]

KRUM_MAJ = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88])
KRUM_MIN = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])


def lire(p):
    w = wave.open(p)
    n, sr, ch = w.getnframes(), w.getframerate(), w.getnchannels()
    d = np.frombuffer(w.readframes(n), dtype='<i2').astype(float) / 32768
    if ch == 2:
        d = d.reshape(-1, 2).mean(1)
    return d, sr


def chroma(seg, sr, N=8192):
    """Chroma pondéré par l'amplitude, 65–2000 Hz.

    On coupe sous 65 Hz (le ronflement et la marche du pied) et au-dessus de
    2000 Hz (les harmoniques hautes brouillent la classe de hauteur plus
    qu'elles ne l'aident). L'amplitude, pas la puissance : la puissance laisse
    une seule corde forte écraser l'accord.
    """
    c = np.zeros(12)
    h = N // 2
    for s in range(0, max(len(seg) - N, 1), h):
        fr = seg[s:s + N]
        if len(fr) < N:
            break
        if math.sqrt((fr * fr).mean()) < 0.005:
            continue
        sp = np.abs(np.fft.rfft(fr * np.hanning(N)))
        f = np.arange(len(sp)) * sr / N
        m = (f >= 65) & (f <= 2000)
        pc = np.round(12 * np.log2(f[m] / 440.0) + 69).astype(int) % 12
        np.add.at(c, pc, sp[m])
    return c


def accord(c):
    """Renvoie (nom, force). La force est l'écart relatif au deuxième candidat :
    au-dessous de ~0,08 l'outil hésite, et il faut le dire."""
    if c.sum() <= 0:
        return None, 0.0
    v = c / c.sum()
    res = []
    for r in range(12):
        for suf, iv in GABARITS:
            g = np.zeros(12)
            for i in iv:
                g[(r + i) % 12] = 1
            # Similarité cosinus : elle ne dépend PAS du nombre de notes du
            # gabarit. Un premier essai multipliait par len(iv), ce qui donnait
            # mécaniquement l'avantage aux accords à quatre sons — un sol majeur
            # de contrôle sortait « Gmaj7 », le fa# venant de la 3ᵉ harmonique
            # du si. Un gabarit plus riche doit gagner parce qu'il explique
            # mieux, jamais parce qu'il est plus gros.
            cos = float((v * g).sum() / (np.linalg.norm(v) * np.linalg.norm(g)))
            dehors = float(v[[i for i in range(12) if g[i] == 0]].sum())
            # Léger désavantage aux gabarits étendus, à égalité d'explication.
            res.append((cos - 0.35 * dehors - 0.01 * len(iv), f"{LAT[r]}{suf}"))
    res.sort(reverse=True)
    return res[0][1], res[0][0] - res[1][0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fichier')
    ap.add_argument('--debut', type=float, default=0)
    ap.add_argument('--fin', type=float, default=1e9)
    ap.add_argument('--fenetre', type=float, default=1.0)
    a = ap.parse_args()

    d, sr = lire(a.fichier)
    fin = min(a.fin, len(d) / sr)
    print(f"# {a.fichier} · {len(d)/sr:.1f} s · analyse de {a.debut:.1f} à {fin:.1f} s"
          f" · fenêtre {a.fenetre:.2f} s\n")

    total = np.zeros(12)
    print(" temps       accord    force   classes dominantes")
    t = a.debut
    while t < fin:
        seg = d[int(t * sr):int(min(t + a.fenetre, fin) * sr)]
        c = chroma(seg, sr)
        total += c
        nom, force = accord(c)
        if nom is None:
            print(f" {t:6.1f}s     —")
        else:
            top = ' '.join(NOMS[i] for i in np.argsort(-c)[:3])
            drapeau = '' if force > 0.08 else '   ← hésite'
            print(f" {t:6.1f}s   {nom:>7}   {force:5.3f}   {top}{drapeau}")
        t += a.fenetre

    v = total / total.sum()
    print("\nchroma cumulé :")
    for i in np.argsort(-v):
        print(f"   {NOMS[i]:4} {v[i]*100:5.1f} %  {'█'*int(v[i]*200)}")
    print("\ntonalité, corrélation de Krumhansl :")
    res = []
    for tr in range(12):
        for prof, lab in ((KRUM_MAJ, 'majeur'), (KRUM_MIN, 'mineur')):
            res.append((float(np.corrcoef(v, np.roll(prof, tr))[0, 1]), f"{NOMS[tr]} {lab}"))
    res.sort(reverse=True)
    for r, k in res[:4]:
        print(f"   {k:12} {r:+.3f}")
    ecart = res[0][0] - res[1][0]
    print(f"\n   écart au deuxième : {ecart:+.3f}"
          f"{'  — franc' if ecart > 0.05 else '  — SERRÉ, ne tranche pas seul'}")


if __name__ == '__main__':
    main()
