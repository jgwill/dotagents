---
name: chronicle-episode
description: Create, adopt, attach captures to, register, work with Attention, verify, commit, or publish Miadi Chronicle episode vessels on William's Ilex Android/Termux host. Use for mkepisode/passages work, new Episode Recorder episode creation, Chronicle decisions/captures/transcripts, or closing an episode through disk, Git, Medicine Wheel, and receipt proofs.
metadata:
  compatibility: Ilex Android/Termux with passages mkepisode >=0.2.0 (0.3.1 current alignment floor), Chronicle worktree, Git, and Medicine Wheel on port 8040.
---

# Chronicle Episode

Use this skill for every write to the Miadi Chronicle. A vessel is not complete merely because its directory exists.

This is the Ilex host variant. `/etc/claude-code/skills/chronicle-episode` owns Gaia-specific paths and recovery history. Keep the lifecycle contract aligned, but never copy one host’s literal paths into the other.

## Authority and paths

Before acting, read completely:

- `/data/data/com.termux/files/srv/miadi/episodes/miadi-chronicle/AGENTS.md`
- `/data/data/com.termux/files/srv/miadi/episodes/miadi-chronicle/CLAUDE.md`
- `/data/data/com.termux/files/srv/miadi/episodes/CLAUDE.md`

Ilex paths and endpoints:

```text
Git root:       /data/data/com.termux/files/srv/miadi/episodes
Chronicle root: /data/data/com.termux/files/srv/miadi/episodes/miadi-chronicle
Medicine Wheel: http://127.0.0.1:8040
Forgewright:    http://127.0.0.1:8031
```

The retired local bare path is not the active origin. Measure `git remote -v`; do not restore stale pointers from old episode files.

## Tool readiness

`mkepisode` from npm `passages` is the tool of record. Presence is not capability:

```bash
command -v mkepisode
mkepisode --help | grep -- --adopt
npm view passages version
npm view @miadi/inquiry-weave version
npm ls -g --all passages @miadi/inquiry-weave @miadi/episodic-memory-schema
node - <<'NODE'
const { createRequire } = require('node:module')
const { execFileSync } = require('node:child_process')
const { realpathSync } = require('node:fs')
const executable = realpathSync(execFileSync('which', ['mkepisode'], { encoding: 'utf8' }).trim())
console.log({ executable, weave: createRequire(executable)('@miadi/inquiry-weave/package.json').version })
NODE
```

`passages@0.2.0` is the adoption capability floor; `passages@0.3.1` is the current alignment floor because its registry range reaches `@miadi/inquiry-weave` 0.8.x. A current top-level weave does not prove what `mkepisode` loads. On Ilex, install the reviewed release deliberately with:

```bash
npm install -g passages@<reviewed-version> --prefer-online
```

Never hand-create an episode directory when `mkepisode` can create it.

## Required birth fields

A new vessel requires all four human-authored inputs:

1. positive episode number;
2. non-empty title;
3. non-empty desired result / goal;
4. one or more ordered provenance references.

Date, slug, series, status, type, root, and Wheel URL are derived. Survey after fetching; never silently replace a colliding number with another.

## Safe preflight

The Chronicle is a shared, main-only worktree. Preserve all unrelated dirty files.

```bash
root=/data/data/com.termux/files/srv/miadi/episodes
chronicle="$root/miadi-chronicle"
git -C "$root" branch --show-current
git -C "$root" status --short --branch
git -C "$root" fetch origin main
git -C "$root" rev-list --left-right --count main...origin/main
```

Only fast-forward when Git proves it safe. Never stash, reset, clean, force-push, or automatically rebase shared `main`. If local and remote diverge, the index already contains work, or integration requires judgment, refuse and report the exact stage.

## Create and register

Always derive the tool boundary variable from the Chronicle-specific variable:

```bash
export MIADI_CHRONICLE_ROOT=/data/data/com.termux/files/srv/miadi/episodes/miadi-chronicle
export MIADI_CHRONICLE_MW_URL=http://127.0.0.1:8040
export MW_API_URL="$MIADI_CHRONICLE_MW_URL"
mkepisode \
  --chronicle-root "$MIADI_CHRONICLE_ROOT" \
  --register "$MW_API_URL" \
  -n <number> \
  -t '<title>' \
  -g '<desired-result>' \
  -r 'owner/repo#issue' \
  -r '<other-provenance>'
```

Use argv-based process execution in applications; never concatenate browser input into a shell command. `--adopt` is only for one already-existing, manifest-less, unambiguous episode and never for ordinary birth.

For a governed birth, `mkepisode` writes the desired result and ordered provenance first. Do not substitute `inquiry-weave inquire --new-episode` or `promote --new-episode`; those relational commands can scaffold a compatibility vessel but do not own the required goal/reference contract. Relate or inquire against the created episode afterward.

## Name and work with the vessel

Creation, naming, relations, and human decisions have separate owners:

- `chronicle-episode` owns vessel birth and the five-stage proof.
- `chronicle-reference` owns the portable `miadi-chronicle:<number>[/artifact]` identity and resolves local, tailnet, public, wheel, and file destinations.
- `inquiry-weave` owns inquiry relations, lineage, and catalogs.
- `attention.json`, operated through passages/inquiry-weave, owns questions that wait for a human word.

Resolve the portable name before opening or linking:

```bash
inquiry-weave resolve 'miadi-chronicle:<number>' --json
inquiry-weave resolve 'miadi-chronicle:<number>' --verify --json
```

Use the Attention verbs instead of editing JSON for ordinary work:

```bash
passages attention add --episode 'miadi-chronicle:<number>' --id '<stable-id>' --question '<one decision>' --unlocks '<what answering releases>' --depth '<episode-local context ref>'
passages attention list --episode 'miadi-chronicle:<number>'
passages attention answer --episode 'miadi-chronicle:<number>' --id '<stable-id>' --answer '<the human word>'
passages attention sync --episode 'miadi-chronicle:<number>'
```

The episode room foregrounds open decisions, keeps answered decisions under **History**, and collapses to **Attention complete** when 0 remain open. Public visitors may read questions, context, answers, and history. Only loopback, an allowlisted Tailscale identity, or writer authority may answer. The same service is available to agents as `chronicle_attention_list`, `chronicle_attention_get`, and `chronicle_attention_answer` through `inquiry-weave-mcp`.

Never submit a guessed answer to test access. Read the HTTP capability response or the room’s rendered access mode, and preserve the human’s exact word when answering.

## Capture custody

A capture may be copied under `<episode>/captures/<take-stem>/`, but compressed raw media remains device-local and ignored by Chronicle Git. Never force-add `.m4a`, `.mp4`, `.mov`, or `.wav`.

Textual publication may include only named paths produced by the gesture, typically:

- `episode.yaml`;
- `.mw-registration.json`;
- `captures/<stem>/capture.json`;
- `captures/<stem>/transcription.json`;
- `captures/<stem>/transcription_<stem>_FR.txt`;
- `captures/<stem>/transcription_<stem>_EN.txt`.

A local copy, Wheel registration, Git commit, and Git push are separate stages. Preserve partial success and recovery paths.

## Git publication

Before staging, fetch again and require a clean index. Stage named textual files only; never `git add .`, `-A`, `commit -a`, or ignored media. Commit directly to `main` with an imperative subject, receipts in the body, `Ref: owner/repo#n`, and a truthful co-author/service trailer required by the Chronicle law. Fetch again before push; if the remote moved, stop rather than rewriting shared history. Push normally and never force.

## Five-stage proof

Report each stage independently:

1. **created** — `episode.yaml` exists;
2. **committed** — `git log -1 -- <episode-path>` names the intended commit;
3. **pushed** — `git rev-list --count origin/main..main` is `0` after fetch;
4. **registered** — `GET /api/nodes/chronicle:<episode-folder>` returns `200`;
5. **receipt-verified** — `.mw-registration.json` state and URL agree with the live read.

Then run `inquiry-weave resolve "miadi-chronicle:<episode-folder>" --verify --json` and require its Wheel leg to agree with the exact node API. Chronicle and Wheel page routes are client-routed and may return 200 for absent names; page status is never node-existence proof.

A pending receipt is debt, not success. A local save remains successful if later registration or publication refuses.

## Event-ready application boundary

Episode applications should emit privacy-bounded stage events through an injected sink. Events may carry correlation/idempotency keys, episode number/path, capture filename, relative textual artifact paths, hashes, commit SHA, and stage status. Never put transcript bodies, credentials, audio bytes, or absolute private media paths in an event payload. The event sink must not own the domain transaction; transport failure is its own receipt.
