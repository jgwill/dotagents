#!/usr/bin/env python3
"""List the drops in an atelier that have not been worked on yet.

"Unread" is not "recent". A timestamp marker answers "was a session opened after
this file appeared?" — which is the wrong question, and it buries anything Jerry
drops in the evening the moment any session opens before he gets back to it.

The right question is "has this been worked on?", and disk can answer it: a file
that has been worked on is **attached to a composition**. So unread means: in the
recordings folder, not attached anywhere, and not our own voice.

Two consequences worth knowing:
  - nothing expires. A drop stays listed until it is used, however old.
  - reading consumes nothing, so this can run any number of times.

usage: jamai-unread.py <recordings-dir> <ledger> <portal-url> [since-iso-date]
"""
import datetime
import json
import os
import ssl
import sys
import urllib.request

KEEP = {".m4a", ".mp3", ".wav", ".opus", ".aac", ".amr", ".mid", ".midi"}


def attached_filenames(portal):
    """Every file already tied to a composition.

    The list endpoint returns `clipCount`, not `clips` — asking it alone reports
    zero attachments and marks everything unread. Each composition has to be
    fetched by slug.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    base = portal.rstrip("/") + "/api/compositions"
    seen = set()
    try:
        index = json.load(urllib.request.urlopen(base, timeout=15, context=ctx))
    except Exception:
        return seen, False          # portal down: say so rather than lie by omission
    for entry in index:
        slug = entry.get("slug")
        if not slug:
            continue
        try:
            comp = json.load(
                urllib.request.urlopen(f"{base}/{slug}", timeout=15, context=ctx))
        except Exception:
            continue
        for key in ("clips", "images"):
            seen |= {x["filename"] for x in comp.get(key, []) if x.get("filename")}
        for text in comp.get("texts", []):
            if text.get("source"):
                seen.add(text["source"])
    return seen, True


def main():
    rec = sys.argv[1]
    ledger = sys.argv[2]
    portal = sys.argv[3]
    since = sys.argv[4] if len(sys.argv) > 4 else ""

    ours = set()
    if os.path.exists(ledger):
        ours = {line.strip() for line in open(ledger) if line.strip()}

    attached, portal_ok = attached_filenames(portal)
    if not portal_ok:
        print("PORTAL_UNREACHABLE", file=sys.stderr)

    cut = 0.0
    if since:
        try:
            cut = datetime.datetime.fromisoformat(since).timestamp()
        except ValueError:
            print(f"date illisible, ignorée: {since}", file=sys.stderr)

    rows = []
    for name in os.listdir(rec):
        if name.startswith("."):
            continue
        if os.path.splitext(name)[1].lower() not in KEEP:
            continue
        if name in ours or name in attached:
            continue
        path = os.path.join(rec, name)
        mtime = os.path.getmtime(path)
        if mtime < cut:
            continue
        rows.append((mtime, path))

    for _, path in sorted(rows):
        print(path)


if __name__ == "__main__":
    main()
