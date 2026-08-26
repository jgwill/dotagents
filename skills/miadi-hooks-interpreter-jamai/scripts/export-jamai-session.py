#!/usr/bin/env python3
"""Classify a JamAI atelier session off /tmp, the songbird / 1937aa47 way.

Reads:
  - @miadi/hooks-interpreter projection of <session-id>
  - the live scratchpad under /tmp/claude-*/<cwd-slug>/<id>/scratchpad

Writes:
  <dest>/{00-interpreter,01-generators,02-scores,03-rendered,
          04-captures,06-analysis,07-surface,08-session-writes,
          09-sessiondata,MANIFEST.tsv}

Does not write README.md — that is a judgment, see the skill.
Refuses to overwrite dest. Needs to be able to read the scratchpad
(sudo this script if the agent is not the session owner).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_SESSIONDATA_ROOT = Path(
    os.environ.get("MIADI_SESSIONDATA_ROOT", "/a/src/_sessiondata")
)
DEFAULT_OWNER = (1000, 1000)  # gmusic:gmusic on Eury
INTERPRETER = os.environ.get("MIADI_HOOKS_INTERPRET", "miadi-hooks-interpret")


def classify(rel: Path) -> str:
    parts = rel.parts
    name = rel.name

    # Device drops — Pixel Recorder / Songbird timestamp names (YYMMDDHHMMSS),
    # wherever they sit. A folder named ilex/ or larix/ is a node, not an owner:
    # classify the timestamped files as captures, leave the rest to extension rules.
    stem = name.rsplit(".", 1)[0]
    if len(stem) >= 12 and stem[:12].isdigit() and name.endswith((".m4a", ".mid", ".jsonl")):
        return "04-captures"
    if len(parts) >= 2 and parts[0] in {"ilex", "larix", "tilia", "iriko", "ginkgo"}:
        if parts[1] in {"ava1", "ava2"} and name.endswith((".mid", ".m4a")):
            return "04-captures"

    if name.endswith(".py"):
        return "01-generators"
    if name.endswith(".abc"):
        return "02-scores"
    if name.endswith(".mid"):
        return "03-rendered/midi"
    if name.endswith((".wav", ".mp3", ".m4a")):
        return "03-rendered/audio"
    if name.endswith(".mp4"):
        return "03-rendered/video"
    if name.endswith((".png", ".svg")):
        return "03-rendered/scores"
    if name.endswith(".html"):
        return "07-surface"
    return "06-analysis"


def sha256(path: Path, buf: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(buf)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def copy_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def chown_tree(root: Path, owner: tuple[int, int]) -> None:
    uid, gid = owner
    for dirpath, _dirnames, filenames in os.walk(root):
        os.chown(dirpath, uid, gid)
        os.chmod(dirpath, 0o775)
        for name in filenames:
            p = Path(dirpath) / name
            os.chown(p, uid, gid)
            mode = p.stat().st_mode
            os.chmod(p, mode | stat.S_IRGRP | stat.S_IWGRP)


def run_interpreter(session_id: str, root: Path, dest_dir: Path) -> dict:
    dest_dir.mkdir(parents=True, exist_ok=True)
    for cmd in ("session", "aspects", "agents", "ceremony"):
        base = [INTERPRETER, cmd, session_id, "--root", str(root)]
        txt = subprocess.check_output(base, text=True)
        js = subprocess.check_output(base + ["--json"], text=True)
        (dest_dir / f"{cmd}.txt").write_text(txt, encoding="utf-8")
        (dest_dir / f"{cmd}.json").write_text(js, encoding="utf-8")
    (dest_dir / "SOURCE.txt").write_text(
        "\n".join(
            [
                f"session_id={session_id}",
                f"tool=@miadi/hooks-interpreter",
                f"cli={INTERPRETER}",
                f"root={root}",
                f"observed_at={datetime.utcnow().strftime('%Y-%m-%d')}",
                "",
                "Replay:",
                f"  {INTERPRETER} session  {session_id} --root {root}",
                f"  {INTERPRETER} aspects  {session_id} --root {root}",
                f"  {INTERPRETER} agents   {session_id} --root {root}",
                f"  {INTERPRETER} ceremony {session_id} --root {root}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return json.loads((dest_dir / "session.json").read_text(encoding="utf-8"))


def find_scratchpad(session_id: str, projection: dict) -> Path | None:
    for item in projection.get("creations") or []:
        path = Path(item.get("path") or "")
        if "scratchpad" in path.parts:
            for parent in [path, *path.parents]:
                if parent.name == "scratchpad" and parent.is_dir():
                    return parent
    # last-ditch: common cwd slugs on this host
    for slug in ("-home-gmusic", "-home-gmusic-compositions-jamai"):
        for claude in Path("/tmp").glob("claude-*"):
            candidate = claude / slug / session_id / "scratchpad"
            if candidate.is_dir():
                return candidate
    return None


def home_rel(path: Path) -> Path:
    try:
        return path.relative_to("/home/gmusic")
    except ValueError:
        return Path("abs") / path.as_posix().lstrip("/")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--session-id", required=True)
    ap.add_argument("--dest", required=True, type=Path)
    ap.add_argument("--sessiondata-root", type=Path, default=DEFAULT_SESSIONDATA_ROOT)
    ap.add_argument("--scratchpad", type=Path, default=None)
    ap.add_argument("--owner", default="1000:1000", help="uid:gid for the dest tree")
    ap.add_argument("--skip-rendered-audio-video", action="store_true",
                    help="copy generators/scores/captures/interpreter only")
    args = ap.parse_args()

    dest: Path = args.dest
    if dest.exists():
        print(f"refusing to overwrite existing {dest}", file=sys.stderr)
        return 2

    session_dir = args.sessiondata_root / args.session_id
    if not session_dir.is_dir():
        print(f"sessiondata missing: {session_dir}", file=sys.stderr)
        return 2

    uid_s, gid_s = args.owner.split(":", 1)
    owner = (int(uid_s), int(gid_s))

    dest.mkdir(parents=True)
    rows: list[tuple[str, str, int, str, str]] = []

    projection = run_interpreter(args.session_id, args.sessiondata_root, dest / "00-interpreter")

    scratch = args.scratchpad
    if scratch is None:
        scratch = find_scratchpad(args.session_id, projection)
    if scratch is None or not scratch.is_dir():
        print(
            f"scratchpad not readable or missing (looked at projection + /tmp/claude-*). "
            f"Interpreter-only drop will be written. Pass --scratchpad if you can see it.",
            file=sys.stderr,
        )
        scratch = None
    else:
        for src in sorted(scratch.rglob("*")):
            if not src.is_file():
                continue
            rel = src.relative_to(scratch)
            klass = classify(rel)
            if args.skip_rendered_audio_video and klass in (
                "03-rendered/audio",
                "03-rendered/video",
            ):
                continue
            dest_file = dest / klass / rel
            copy_file(src, dest_file)
            st = src.stat()
            mtime = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            rows.append(
                (klass.split("/")[0], f"{klass}/{rel.as_posix()}", st.st_size, mtime, sha256(src))
            )

    writes_dir = dest / "08-session-writes"
    writes_dir.mkdir(exist_ok=True)
    missing: list[str] = []
    for item in projection.get("creations") or []:
        src = Path(item.get("path") or "")
        if not src.as_posix() or "scratchpad" in src.parts:
            continue
        if not src.is_file():
            missing.append(str(src))
            continue
        if src.suffix == ".html":
            dest_file = dest / "07-surface" / src.name
            klass = "07-surface"
            rel_out = f"07-surface/{src.name}"
        else:
            rel = home_rel(src)
            dest_file = writes_dir / rel
            klass = "08-session-writes"
            rel_out = f"08-session-writes/{rel.as_posix()}"
        copy_file(src, dest_file)
        st = src.stat()
        mtime = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        rows.append((klass, rel_out, st.st_size, mtime, sha256(src)))

    (writes_dir / "MISSING.txt").write_text(
        ("\n".join(missing) + "\n") if missing else "none\n", encoding="utf-8"
    )
    (writes_dir / "ORIGIN.txt").write_text(
        "Snapshots of living files the interpreter listed as Write/Edit.\n"
        "These are current-on-disk copies, not the bytes at first write.\n",
        encoding="utf-8",
    )

    sess_dest = dest / "09-sessiondata" / args.session_id
    sess_dest.mkdir(parents=True)
    for src in sorted(session_dir.rglob("*")):
        if not src.is_file() or src.name.startswith("last_"):
            continue
        rel = src.relative_to(session_dir)
        copy_file(src, sess_dest / rel)
        st = src.stat()
        mtime = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        rows.append(
            (
                "09-sessiondata",
                f"09-sessiondata/{args.session_id}/{rel.as_posix()}",
                st.st_size,
                mtime,
                sha256(src),
            )
        )

    replay = dest / "00-interpreter" / "SOURCE.txt"
    replay.write_text(
        replay.read_text(encoding="utf-8")
        + "Self-contained replay from this drop:\n"
        + f"  {INTERPRETER} session  {args.session_id} --root {dest / '09-sessiondata'}\n"
        + f"  {INTERPRETER} aspects  {args.session_id} --root {dest / '09-sessiondata'}\n",
        encoding="utf-8",
    )

    rows.sort(key=lambda r: (r[0], r[1]))
    with (dest / "MANIFEST.tsv").open("w", encoding="utf-8") as f:
        f.write("class\tpath\tbytes\tmtime\tsha256\n")
        for row in rows:
            f.write("\t".join(str(x) for x in row) + "\n")

    try:
        chown_tree(dest, owner)
    except PermissionError:
        print("could not chown dest (not root?) — tree is still usable", file=sys.stderr)

    counts: dict[str, list[int]] = {}
    for klass, _path, size, _mtime, _h in rows:
        bucket = counts.setdefault(klass, [0, 0])
        bucket[0] += 1
        bucket[1] += size
    summary = {
        "dest": str(dest),
        "session_id": args.session_id,
        "scratchpad": str(scratch) if scratch else None,
        "files": len(rows),
        "bytes": sum(r[2] for r in rows),
        "counts": {k: {"files": v[0], "bytes": v[1]} for k, v in sorted(counts.items())},
        "missing_session_writes": missing,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
