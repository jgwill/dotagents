#!/usr/bin/env python3
"""jamai-deglisse.py — le suivi de hauteur ment-il ? (réflexe 2 de la méthode)

Prend un MIDI issu d'un suivi de hauteur sur la voix (Songbird) et rend :
  1. les DEUX indicateurs d'artefact et leur verdict contre les seuils ;
  2. la ligne déglissée — grappes voisines d'un demi-ton et contiguës fusionnées
     en la note qui porte le plus de durée cumulée ;
  3. les DEUX estimations de tonalité côte à côte (brute / déglissée),
     par corrélation de Krumhansl-Schmuckler ET par couverture de gamme —
     parce qu'en ava001 les deux méthodes ne s'entendaient pas et que c'est
     la couverture qui avait raison (la sixte dorienne pénalisée par K-S) ;
  4. --segments : le verdict PAR SEGMENT chanté — l'enseignement inversé que
     William a demandé (2026-08-15, op002) : « I want to know what am I singing
     that transforms well into musical notes ». Un segment stable est matière ;
     un segment au quantum ou en bavardage de demi-tons est la voix qui cherche.

Existe parce que son absence a coûté deux pièces (session 9f8a16f3) :
46 % des notes au quantum du tracker et 50 % des enchaînements au demi-ton
avaient fait lire un « motif » là où il n'y avait que du glissando de justesse.
Seuils d'alerte : 30 % (quantum) et 35 % (demi-tons) — d'UNE session, à
reprendre quand d'autres prises existeront (04-exportation § Ce qui reste ouvert).

Le parseur MIDI vient de jamai-midi.py (mido n'est pas installé ici).

  jamai-deglisse.py prise.mid [--segments] [--json] [--gap 1.0]
"""
import sys, struct, json, math

# ---------------------------------------------------------------- parseur MIDI
def vlq(d, i):
    v = 0
    while True:
        b = d[i]; i += 1
        v = (v << 7) | (b & 0x7F)
        if not b & 0x80: return v, i

def notes_du_midi(path):
    d = open(path, 'rb').read()
    assert d[:4] == b'MThd', "pas un fichier MIDI"
    fmt, ntrk, div = struct.unpack('>HHH', d[8:14])
    i, tempo = 14, 500000
    notes = []                       # (debut_s, duree_s, midi)
    for _ in range(ntrk):
        assert d[i:i+4] == b'MTrk'
        ln = struct.unpack('>I', d[i+4:i+8])[0]
        j, end = i + 8, i + 8 + ln
        i = end
        t, run, on = 0, None, {}
        while j < end:
            dt, j = vlq(d, j); t += dt
            b = d[j]
            if b & 0x80: st = b; j += 1; run = st
            else: st = run
            hi = st & 0xF0
            if st == 0xFF:
                mt = d[j]; j += 1
                ml, j = vlq(d, j)
                if mt == 0x51: tempo = int.from_bytes(d[j:j+ml], 'big')
                j += ml
            elif st in (0xF0, 0xF7):
                ml, j = vlq(d, j); j += ml
            elif hi in (0x80, 0x90, 0xA0, 0xB0, 0xE0):
                p1, p2 = d[j], d[j+1]; j += 2
                s = t * tempo / (480 * 1_000_000) if False else t
                if hi == 0x90 and p2 > 0: on[p1] = t
                elif hi in (0x80, 0x90):
                    if p1 in on:
                        t0 = on.pop(p1)
                        notes.append((t0, t - t0, p1))
            elif hi in (0xC0, 0xD0): j += 1
    k = tempo / (div * 1_000_000)    # ticks -> secondes (tempo unique suffit ici)
    return sorted((t0 * k, du * k, n) for t0, du, n in notes)

# ------------------------------------------------------------------- mesures
def indicateurs(notes):
    if not notes: return None
    durees = [round(du, 3) for _, du, _ in notes]
    quantum = min(durees)
    au_quantum = sum(1 for du in durees if du <= quantum * 1.05)
    trans = demi = 0
    for (t0, du, n), (t1, _, m) in zip(notes, notes[1:]):
        if t1 - (t0 + du) < 0.25:
            trans += 1
            if abs(m - n) == 1: demi += 1
    return {
        "notes": len(notes), "quantum_s": quantum,
        "part_quantum": au_quantum / len(notes),
        "part_demi_tons": (demi / trans) if trans else 0.0,
        "transitions_serrees": trans,
    }

def deglisser(notes):
    """Fusionne les grappes chromatiques contiguës ; garde la note majoritaire."""
    if not notes: return []
    out, grappe = [], [notes[0]]
    for n in notes[1:]:
        t0p, dup, mp = grappe[-1]
        contigu = n[0] - (t0p + dup) < 0.25
        voisin = abs(n[2] - mp) <= 1
        if contigu and voisin: grappe.append(n)
        else:
            out.append(_fusion(grappe)); grappe = [n]
    out.append(_fusion(grappe))
    return out

def _fusion(grappe):
    poids = {}
    for _, du, m in grappe: poids[m] = poids.get(m, 0) + du
    m = max(poids, key=poids.get)
    t0 = grappe[0][0]
    fin = max(t + du for t, du, _ in grappe)
    return (t0, fin - t0, m)

# ------------------------------------------------------------------ tonalité
KS_MAJ = [6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88]
KS_MIN = [6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17]
NOMS = ['do','do#','ré','ré#','mi','fa','fa#','sol','sol#','la','la#','si']
MODES = {                      # intervalles depuis la tonique
    'majeur':  {0,2,4,5,7,9,11}, 'mineur':  {0,2,3,5,7,8,10},
    'dorien':  {0,2,3,5,7,9,10}, 'mixolydien': {0,2,4,5,7,9,10},
}

def profil(notes):
    p = [0.0]*12
    for _, du, m in notes: p[m % 12] += du
    return p

def correlation(p, gabarit):
    n = 12
    mx, my = sum(p)/n, sum(gabarit)/n
    num = sum((p[i]-mx)*(gabarit[i]-my) for i in range(n))
    den = math.sqrt(sum((x-mx)**2 for x in p) * sum((y-my)**2 for y in gabarit))
    return num/den if den else 0.0

def tonalites(notes):
    p = profil(notes)
    ks = []
    for t in range(12):
        rot = p[t:] + p[:t]
        ks.append((correlation(rot, KS_MAJ), f"{NOMS[t]} majeur"))
        ks.append((correlation(rot, KS_MIN), f"{NOMS[t]} mineur"))
    ks.sort(reverse=True)
    total = sum(p) or 1
    couv = []
    for t in range(12):
        for mode, deg in MODES.items():
            dedans = sum(p[(t+d) % 12] for d in deg)
            tonique = p[t] / total
            couv.append((dedans/total, tonique, f"{NOMS[t]} {mode}"))
    couv.sort(key=lambda x: (round(x[0], 3), x[1]), reverse=True)
    return {"ks": [(round(v,3), n) for v, n in ks[:3]],
            "couverture": [(round(c,3), round(tq,3), n) for c, tq, n in couv[:3]]}

# ------------------------------------------------------------------ segments
def segments(notes, gap=1.0):
    """Coupe sur les silences ; verdict par segment pour l'enseignement inversé."""
    if not notes: return []
    grp, out = [notes[0]], []
    for n in notes[1:]:
        t0p, dup, _ = grp[-1]
        if n[0] - (t0p + dup) > gap: out.append(grp); grp = [n]
        else: grp.append(n)
    out.append(grp)
    res = []
    for g in out:
        ind = indicateurs(g)
        deb, fin = g[0][0], max(t+du for t, du, _ in g)
        stable = ind["part_quantum"] <= 0.30 and ind["part_demi_tons"] <= 0.35
        deg = deglisser(g)
        res.append({
            "debut_s": round(deb,2), "fin_s": round(fin,2),
            "notes": len(g), "notes_deglissees": len(deg),
            "part_quantum": round(ind["part_quantum"],2),
            "part_demi_tons": round(ind["part_demi_tons"],2),
            "verdict": "se transforme bien" if stable else "la voix cherche la note",
            "ligne": [NOMS[m%12]+str(m//12-1) for _,_,m in deg][:12],
        })
    return res

# ----------------------------------------------------------------------- cli
if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    opts = {a for a in sys.argv[1:] if a.startswith('--')}
    gap = 1.0
    for a in sys.argv[1:]:
        if a.startswith('--gap='): gap = float(a.split('=')[1])
    if not args:
        print(__doc__); sys.exit(1)
    notes = notes_du_midi(args[0])
    ind = indicateurs(notes)
    deg = deglisser(notes)
    rapport = {
        "fichier": args[0],
        "indicateurs": {**ind,
            "seuil_quantum": 0.30, "seuil_demi_tons": 0.35,
            "artefact": ind["part_quantum"] > 0.30 and ind["part_demi_tons"] > 0.35},
        "deglissage": {"avant": len(notes), "apres": len(deg)},
        "tonalite_brute": tonalites(notes),
        "tonalite_deglissee": tonalites(deg),
    }
    if '--segments' in opts:
        rapport["segments"] = segments(notes, gap)
    if '--json' in opts:
        print(json.dumps(rapport, ensure_ascii=False, indent=1)); sys.exit(0)
    i = rapport["indicateurs"]
    print(f"# {args[0]} — {i['notes']} notes, quantum {i['quantum_s']} s")
    print(f"au quantum      : {i['part_quantum']:.0%}  (seuil 30 %)")
    print(f"demi-tons serrés: {i['part_demi_tons']:.0%}  (seuil 35 %)")
    print(f"verdict         : {'ARTEFACT — le tracker ment, dégliser avant toute tonalité' if i['artefact'] else 'ligne saine'}")
    print(f"déglissage      : {len(notes)} -> {len(deg)} notes")
    print("tonalité brute      :", rapport['tonalite_brute'])
    print("tonalité déglissée  :", rapport['tonalite_deglissee'])
    if '--segments' in opts:
        print("\n## segments (enseignement inversé)")
        for s in rapport['segments']:
            print(f"  {s['debut_s']:>7.2f}–{s['fin_s']:<7.2f} {s['notes']:>3} notes  "
                  f"quantum {s['part_quantum']:.0%}  demi-tons {s['part_demi_tons']:.0%}  -> {s['verdict']}")
