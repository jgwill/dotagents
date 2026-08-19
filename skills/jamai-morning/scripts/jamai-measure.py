#!/usr/bin/env python3
"""Mesure d'un enregistrement : structure, tempo, hauteurs, timbre.
Pas de librosa sur cette machine — tout à la main avec numpy/scipy."""
import sys, wave, numpy as np
from scipy.signal import stft

path = sys.argv[1]
w = wave.open(path, 'rb')
sr = w.getframerate()
n = w.getnframes()
x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768.0
w.close()
dur = len(x) / sr
print(f"# {path}")
print(f"durée      : {dur:.2f} s   sr={sr}   échantillons={len(x)}")
print(f"pic        : {np.max(np.abs(x)):.4f}   RMS global : {np.sqrt(np.mean(x**2)):.5f}")

# ---- enveloppe RMS par 100 ms : où ça joue, où c'est silencieux
hop = sr // 10
env = np.array([np.sqrt(np.mean(x[i:i+hop]**2)) for i in range(0, len(x)-hop, hop)])
db = 20*np.log10(env + 1e-9)
floor = np.percentile(db, 10)
active = db > floor + 12
print(f"\n# enveloppe (100 ms/case), plancher={floor:.1f} dB")
# segments actifs
segs, on = [], None
for i, a in enumerate(active):
    if a and on is None: on = i
    elif not a and on is not None:
        if i - on >= 3: segs.append((on/10, i/10))
        on = None
if on is not None: segs.append((on/10, len(active)/10))
print(f"segments actifs (>0,3 s) : {len(segs)}")
for s, e in segs[:40]:
    print(f"   {s:6.1f} → {e:6.1f} s   ({e-s:.1f} s)")

# profil temporel compact
sym = ''.join('#' if a else '.' for a in active)
print("\n# carte temporelle, 1 caractère = 100 ms")
for i in range(0, len(sym), 100):
    print(f"  {i/10:6.1f}s |{sym[i:i+100]}|")

# ---- STFT
nper = 2048
f, t, Z = stft(x, fs=sr, nperseg=nper, noverlap=nper*3//4)
S = np.abs(Z)

# ---- centroïde spectral et bandes d'énergie
p = S**2
tot = p.sum() + 1e-12
cen = float((f[:, None] * p).sum() / tot)
bands = [(0, 250), (250, 1000), (1000, 4000), (4000, 8000), (8000, sr/2)]
print(f"\n# timbre\ncentroïde spectral : {cen:.0f} Hz")
for lo, hi in bands:
    m = (f >= lo) & (f < hi)
    print(f"   {lo:5.0f}–{hi:5.0f} Hz : {100*p[m].sum()/tot:5.2f} %")

# ---- profil de classes de hauteur (chroma), pondéré par l'énergie
# on ne garde que 80–2000 Hz : au-delà les harmoniques brouillent
chroma = np.zeros(12)
mask = (f > 80) & (f < 2000)
ff = f[mask]
midi = 69 + 12*np.log2(ff/440.0)
pc = np.round(midi).astype(int) % 12
en = p[mask].sum(axis=1)
for k in range(12):
    chroma[k] = en[pc == k].sum()
chroma /= chroma.sum() + 1e-12
names = ['do','do#','ré','ré#','mi','fa','fa#','sol','sol#','la','la#','si']
print("\n# profil de classes de hauteur (80–2000 Hz)")
order = np.argsort(-chroma)
for k in order:
    bar = '█' * int(chroma[k]*200)
    print(f"   {names[k]:4s} {100*chroma[k]:5.2f} %  {bar}")

# ---- tempo par autocorrélation du flux spectral
flux = np.maximum(0, np.diff(S.sum(axis=0)))
fps = sr / (nper // 4)
fl = flux - flux.mean()
ac = np.correlate(fl, fl, 'full')[len(fl)-1:]
ac /= ac[0] + 1e-12
lo_l, hi_l = int(fps*60/200), int(fps*60/50)   # 50–200 BPM
if hi_l < len(ac):
    seg = ac[lo_l:hi_l]
    best = lo_l + int(np.argmax(seg))
    print(f"\n# tempo (autocorrélation du flux spectral, fenêtre 50–200 BPM)")
    print(f"   pic à {best/fps:.3f} s  →  {60*fps/best:.1f} BPM   (force {ac[best]:.3f})")
    top = lo_l + np.argsort(-seg)[:6]
    for b in sorted(top):
        print(f"     {60*fps/b:6.1f} BPM   force {ac[b]:.3f}")

# ---- attaques
thr = np.percentile(flux, 92)
onsets = [i/fps for i in range(1, len(flux)-1)
          if flux[i] > thr and flux[i] >= flux[i-1] and flux[i] > flux[i+1]]
merged = [onsets[0]] if onsets else []
for o in onsets[1:]:
    if o - merged[-1] > 0.09: merged.append(o)
print(f"\n# attaques détectées : {len(merged)}")
if len(merged) > 1:
    d = np.diff(merged)
    print(f"   intervalle médian {np.median(d):.3f} s  →  {60/np.median(d):.1f} BPM si c'est le pouls")
print("   " + ' '.join(f"{o:.2f}" for o in merged[:60]))
