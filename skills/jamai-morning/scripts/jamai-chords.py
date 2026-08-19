#!/usr/bin/env python3
"""Identify the chord sounding on every beat of a MIDI file.

Naming chords by eye over a span is how a score ends up lying. A symbol written
once over a bar claims that chord holds for the bar — and Jerry's playing changes
inside the bar more often than not. On opus 001 a single `Gadd9` covered four
beats when the ninth sounded on one of them; the other three were `Gsus2`.

Run this on the source MIDI before writing any chord symbol, and place a new
symbol wherever the identification changes. Then run it again on the rendered
ABC and compare: same labels at the same beats, or the score is lying.

usage: jamai-chords.py <file.mid> [beats-per-bar]
"""
import sys

NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
FR = {'C': 'do', 'C#': 'do#', 'D': 'ré', 'D#': 'ré#', 'E': 'mi', 'F': 'fa',
      'F#': 'fa#', 'G': 'sol', 'G#': 'sol#', 'A': 'la', 'A#': 'la#', 'B': 'si'}

# Ordered by size: a smaller template wins ties, so a bare fifth is not reported
# as a coloured chord it does not contain.
TEMPLATES = [
    ('5',       (0, 7)),            ('sus2',    (0, 2, 7)),
    ('sus4',    (0, 5, 7)),         ('',        (0, 4, 7)),
    ('m',       (0, 3, 7)),         ('m(no3)',  (0, 7, 10)),
    ('7',       (0, 4, 7, 10)),     ('maj7',    (0, 4, 7, 11)),
    ('m7',      (0, 3, 7, 10)),     ('7sus4',   (0, 5, 7, 10)),
    ('add9',    (0, 2, 4, 7)),      ('madd9',   (0, 2, 3, 7)),
    ('6',       (0, 4, 7, 9)),      ('m6',      (0, 3, 7, 9)),
    ('69',      (0, 2, 4, 7, 9)),   ('m11',     (0, 3, 5, 7, 10)),
]


def read_midi(path):
    """Minimal SMF reader — mido is not installed on this box."""
    import struct
    data = open(path, 'rb').read()
    assert data[:4] == b'MThd', 'not a MIDI file'
    hlen = struct.unpack('>I', data[4:8])[0]
    _, _, div = struct.unpack('>HHH', data[8:14])
    pos = 8 + hlen
    events = []
    while pos < len(data) and data[pos:pos + 4] == b'MTrk':
        tlen = struct.unpack('>I', data[pos + 4:pos + 8])[0]
        track, i, now, running = data[pos + 8:pos + 8 + tlen], 0, 0, None
        pending = {}
        while i < len(track):
            delta = 0
            while True:
                byte = track[i]; i += 1
                delta = (delta << 7) | (byte & 0x7F)
                if not byte & 0x80:
                    break
            now += delta
            if i >= len(track):
                break
            status = track[i]
            if status & 0x80:
                i += 1; running = status
            else:
                status = running
            if status == 0xFF:
                i += 1
                length = 0
                while True:
                    byte = track[i]; i += 1
                    length = (length << 7) | (byte & 0x7F)
                    if not byte & 0x80:
                        break
                i += length
            elif status in (0xF0, 0xF7):
                length = 0
                while True:
                    byte = track[i]; i += 1
                    length = (length << 7) | (byte & 0x7F)
                    if not byte & 0x80:
                        break
                i += length
            else:
                high = status & 0xF0
                n = 1 if high in (0xC0, 0xD0) else 2
                payload = track[i:i + n]; i += n
                if high == 0x90 and payload[1] > 0:
                    pending.setdefault(payload[0], []).append(now)
                elif high == 0x80 or (high == 0x90 and payload[1] == 0):
                    if pending.get(payload[0]):
                        start = pending[payload[0]].pop(0)
                        events.append((start / div, now / div, payload[0]))
        pos += 8 + tlen
    return sorted(events)


def name_chord(pitches):
    """Best template match, preferring root position and the smallest fit."""
    classes = {p % 12 for p in pitches}
    bass = min(pitches) % 12
    best = None
    for root in range(12):
        intervals = frozenset((p - root) % 12 for p in classes)
        for suffix, template in TEMPLATES:
            if intervals == frozenset(template):
                rank = (0 if root == bass else 1, len(template))
                label = NAMES[root] + suffix + ('' if root == bass else '/' + NAMES[bass])
                if best is None or rank < best[0]:
                    best = (rank, label)
    return best[1] if best else '(non répertorié)'


def main():
    path = sys.argv[1]
    per_bar = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    events = read_midi(path)
    if not events:
        print('aucune note'); return
    last = max(e for _, e, _ in events)

    # Two different tolerances, and both were learned the hard way.
    #
    # ONSET (0.15 beat): abc2midi does not strike a chord's notes together — it
    # staggers them by about 0.021 beat each. A four-note chord therefore spans
    # 0.065 beat, and a window of 0.06 silently drops its last note and renames
    # the chord. Jerry's own recorded MIDI has no stagger, so the same file
    # compared against its own re-rendering disagreed with itself.
    #
    # OFFSET (0.02 beat): a note that ends exactly on the beat belongs to the
    # previous chord, not this one. Too tight a value here reported a phantom
    # "D5/A" by dropping a voice that started 0.010 beat late.
    ON_TOL, OFF_TOL = 0.15, 0.02
    rows = []
    for beat in range(int(last + 0.5)):
        sounding = [p for s, e, p in events
                    if s < beat + ON_TOL and e > beat + OFF_TOL]
        if not sounding:
            continue
        rows.append((beat, min(sounding) % 12, name_chord(sounding), sorted(set(sounding))))

    print(f"  {'temps':>5} {'mes.':>5}  {'basse':>5}  {'accord':16s}  notes")
    previous = None
    for beat, bass, chord, pitches in rows:
        mark = '  ←' if chord != previous else ''
        notes = ' '.join(FR[NAMES[p % 12]] for p in pitches)
        print(f"  {beat:5d} {beat // per_bar + 1:5d}  {FR[NAMES[bass]]:>5}  {chord:16s}  {notes}{mark}")
        previous = chord

    print('\nplacer un symbole à chaque ← :')
    previous = None
    for beat, _, chord, _ in rows:
        if chord != previous:
            print(f'   temps {beat:2d} (mesure {beat // per_bar + 1})  "{chord}"')
            previous = chord


if __name__ == '__main__':
    main()
