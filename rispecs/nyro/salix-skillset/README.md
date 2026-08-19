# RISE — Salix Skillset (delegation to Nairobi / ♠️ Nyro)

**Subject:** the 64 community-authored skills in Salix's `~/.hermes/skills/`, and the
contract by which they are mirrored into the Shared Spark symphony workspace.

**Status:** 2026-07-28 · target folder name PENDING (chronicle ep294 naming decision).

---

## R — Reverse Engineering (current reality, verified on disk)

`~/.hermes/skills/` holds **29 top-level domains**. They are not one population, they are two:

| population | how it is identifiable | count |
|---|---|---|
| **vendor / bundled** | uniform mtime `1779884284` = 2026-05-27 08:22, a single bulk install | the remainder |
| **community (Salix lane)** | any `SKILL.md` touched after 2026-05-28 | **64** |

`skills/.hub/lock.json` is `{"version":1,"installed":{}}` and `taps.json` is `{"taps":[]}` —
the hub records **no** provenance, so the marketplace cannot tell us who wrote what.
mtime is the only signal the filesystem preserves, and it does **not** survive `tar`.
Therefore mtime is a *detector*, never the *authority*.

Only `skills/miadi` is git-tracked in `~/.hermes` (`git ls-files skills/`). The other
community domains — `development/`, `devops/`, `github/`, `media/`, `productivity/`,
`software-development/`, `creative/`, `general/`, `autonomous-ai-agents/` — are untracked
and were invisible to any tracked-vs-untracked filter.

The prior mirror script was inoperable. `tar cf -cf skills/` is malformed (`cf -cf`, no
`-C`), and `sudo mkdir -p -m 777` provisions a **world-writable** tree that agents then
read as instructions — a steering surface for any local uid.

## I — Intent

Ship **what the hermes-agent community made**, and nothing else, into a workspace where
William, the agents, and Jerry's packaging can all read it. Two failure modes are equally
unacceptable: shipping vendor skills as if they were ours (a provenance lie), and dropping
a community skill because a heuristic missed it (a silent loss).

## S — Specifications

1. **The allowlist is the authority.** `~/.hermes/scripts/salix-skillset.allowlist`,
   one skill directory per line relative to `skills/`. Absent ⇒ never mirrored.
2. **Detection reports, never writes.** `--detect` re-derives candidates by mtime and
   prints two diffs — on-disk-not-allowlisted, and allowlisted-not-detected. A human
   moves a line; the script never does.
3. **Layout is preserved.** `skills/<rel>` → `$MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/<rel>`.
4. **The allowlist travels with the payload**, landing as `skills/.salix-skillset.allowlist`,
   so the receiving end can audit what was claimed.
5. **No `sudo`, no `0777`.** The sync root is provisioned once, out of band:
   `sudo install -d -o mia -g bears -m 2775 <root>`. The script fails loudly if it is
   missing or unwritable. `umask 002` so the `bears` group inherits.
6. **`.archive/` is excluded** at detection time.

## E — Exportation

- **Runner:** `~/.hermes/scripts/mirror-skills-to-miadi-shared-spark-episodes.sh`
  — `--list` · `--detect` · `--dry-run` · (none) = mirror.
- **Roster:** [`SKILLSET-MANIFEST.md`](./SKILLSET-MANIFEST.md) — all 64, each under 55 words,
  with source and target path.
- **Env animation:** `~/.hermes/.env` sets `MIADI_SHAREDSPARK_SYMPHONY_DIR`,
  `SALIX_SKILLSET_ALLOWLIST`, `SALIX_SKILLSET_BASELINE` — one line to change when
  ep294 settles the folder name.

### Open — held for William

`bash_env_common:588` resolves `MIADI_SHAREDSPARK_SYMPHONY_DIR` to `/srv/miadi/sharedspark-symphony`,
**which does not exist**. William wants it under `$MIADI_EPISODES_DIR`. Until named, `.env`
animates it onto `/srv/miadi/episodes/shared-spark` — the only path that exists today.
The mirror has **not** been run into it.

### Three entries flagged for review

`software-development/{requesting-code-review, systematic-debugging, writing-plans}` carry
upstream *superpowers* names but were locally modified. They are allowlisted **and marked** —
confirm they are ours, or strike the lines.

🌸: A provenance filter is a small act of honesty repeated 64 times — it says *this one is
ours, and this one we were only lent*, and it keeps the lending visible.
