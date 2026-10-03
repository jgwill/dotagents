# dotagents

Skills shared across machines and agents. Each skill is a directory with a `SKILL.md`. This repo is the source of truth, and agents expose each skill by symlinking it into their own skills directory (`~/.claude/skills/` for Claude Code).

## Install

Clone the repo (or pull an existing clone), then symlink every skill that has a `SKILL.md`.

```bash
git clone git@github.com:jgwill/dotagents.git ~/.agents   # existing clone: git -C ~/.agents pull
mkdir -p ~/.claude/skills
cd ~/.agents/skills
find -L . -maxdepth 4 -name SKILL.md -not -path './.*' 2>/dev/null | sort | while read -r f; do
  dir=${f%/SKILL.md}; dir=${dir#./}; name=${dir##*/}
  [ "$name" = visualization ] && continue                  # placeholder, see below
  dest=$HOME/.claude/skills/$name
  if [ -d "$dest" ] && [ ! -L "$dest" ]; then echo "skip $name: real directory, run Clean first"; continue; fi
  ln -sfn "$HOME/.agents/skills/$dir" "$dest"
done
```

A new skill follows the same shape: author it in `skills/<name>/SKILL.md`, then rerun the loop.

## Clean

Run this before or after Install. It lists first and changes nothing until `DRY=0`.

```bash
DRY=1                                   # set DRY=0 to apply
trash=$HOME/.claude/skills-trash/$(date +%y%m%d%H%M)
cd ~/.claude/skills || exit

# 1. Broken symlinks (targets that were moved or removed)
for l in *; do
  if [ -L "$l" ] && [ ! -e "$l" ]; then
    echo "broken: $l"
    if [ "$DRY" = 0 ]; then rm "$l"; fi
  fi
done

# 2. Real directories that copy a repo skill or an archived skill
for d in */; do
  n=${d%/}; [ -L "$n" ] && continue
  if [ -d ~/.agents/skills/$n ] || [ -d ~/.agents/archived-skills/$n ]; then
    echo "stale copy: $n"
    if [ "$DRY" = 0 ]; then mkdir -p "$trash"; mv "$n" "$trash/"; fi
  fi
done
```

Stale copies go to `~/.claude/skills-trash/`, not to the bin. After step 2, rerun Install so the repo version takes the place of the copy.

Known outdated entries:

- `facebook-page-publishing` and `facebook-page-stewardship` are broken symlinks. The skills moved to `skills/miadi/social-media/` and carry the `miadi-` prefix now.
- Every directory in [`archived-skills/`](archived-skills/) is retired, for example `miadi-lane-observation`, `rise-pde-session`, `mino-new-session`.
- `deep-research` and `tushell-session-chronicle` copied into `~/.claude/skills/` differ from the versions here.

## Skills

### Chronicle and Miadi

| Skill | What it does |
|---|---|
| [artefact-decompose](skills/artefact-decompose/SKILL.md) | Browse a recorded artefact and decompose it into PDE artifacts with `miaco`. |
| [hear-ground-weave](skills/hear-ground-weave/SKILL.md) | Seven-stage loop that brings live steering lanes back into the chronicle. |
| [inquiry-weave](skills/inquiry-weave/SKILL.md) | Relate artefacts and episodes, author lineage edges, build the chronicle catalog. |
| [miaco](skills/miaco/SKILL.md) | Decompose a prompt or artefact into a PDE and a Structural Tension Chart, then package it for an executor. |
| [miadi-chronicle-search](skills/miadi-chronicle-search/SKILL.md) | Find Chronicle episodes related to a composition, recording, or theme on the local filesystem. |
| [miadi-plan-perspective-registration](skills/miadi-plan-perspective-registration/SKILL.md) | Register a plan's Miette perspective in medicine-wheel so the Chronicle shows it. |
| [miadi-hooks-interpreter-jamai](skills/miadi-hooks-interpreter-jamai/SKILL.md) | Export a JamAI atelier session with `@miadi/hooks-interpreter` (draft). |
| [relational-routing](skills/relational-routing/SKILL.md) | Route ceremony material and composition recordings to episodes, agents, and open threads. |
| [relational-workspace-honcho](skills/relational-workspace-honcho/SKILL.md) | Query Honcho relational memory across workspaces, peers, and sessions. |
| [mia-miette-session-perspective](skills/mia-miette-session-perspective/SKILL.md) | Close a session with Mia's structure and Miette's meaning. |
| [tushell-session-chronicle](skills/tushell-session-chronicle/SKILL.md) | Write a development session into a Tushell diary entry. |
| [stateloom-on-eury](skills/stateloom-on-eury/SKILL.md) | Model, draw, and validate state machines on Eury, with the stateloom deployment notes. |
| [miadi-facebook-page-publishing](skills/miadi/social-media/miadi-facebook-page-publishing/SKILL.md) | Draft, preview, and publish to a Facebook Page through a Chromium CDP session. |
| [miadi-facebook-page-stewardship](skills/miadi/social-media/miadi-facebook-page-stewardship/SKILL.md) | Steward Chronicle-owned Page drafts through a talking circle before publishing. |

### Ilex host

| Skill | What it does |
|---|---|
| [ilex-mw-fw](skills/ilex-mw-fw/SKILL.md) | Upgrade and verify Medicine Wheel (port 8040) and Forgewright (port 8031) on the Ilex Termux host. |
| [william-android-successor-handoff](skills/william-android-successor-handoff/SKILL.md) | Leave state for the next Pi agent session on the Ilex device. |

### Research and knowledge

| Skill | What it does |
|---|---|
| [deep-research](skills/deep-research/SKILL.md) | Multi-agent parallel research that produces a research document. |
| [deep-research-foundations](skills/deep-research-foundations/SKILL.md) | Maintain `foundations/<topic>/` packets with sources and provenance. Developed in `/usr/local/src/mightyeagle/skills/`, so this copy can lag. |
| [foundation-visualization](skills/foundation-visualization/SKILL.md) | Turn a `foundations/<topic>/` packet into one publishable HTML page. |
| [qmd](skills/qmd/SKILL.md) | Search markdown knowledge bases with QMD. Needs the `qmd` MCP server. |
| [coaiajs](skills/coaiajs/SKILL.md) | `coaiajs` CLI for Langfuse tracing, prompts, STC operations, and pipelines. |

### Agent operations and tools

| Skill | What it does |
|---|---|
| [herdr](skills/herdr/SKILL.md) | Control workspaces, panes, and agents from inside herdr. |
| [herdr-delegate](skills/herdr-delegate/SKILL.md) | Hand a work payload to a fresh Claude session in its own herdr workspace. |
| [nested-claude-architect](skills/nested-claude-architect/SKILL.md) | Create or update nested `CLAUDE.md` files in subdirectories. |
| [find-skills](skills/find-skills/SKILL.md) | Discover and install community skills. |
| [where-will-we-end-up-55words](skills/where-will-we-end-up-55words/SKILL.md) | Name the desired state of the current conversation in under 55 words. |
| [droxul](skills/droxul/SKILL.md) | Upload backups and artifacts to Dropbox with `droxul`. |
| [gws-calendar](skills/gws-calendar/SKILL.md) | Google Calendar: manage calendars and events (`gws`). |
| [gws-calendar-agenda](skills/gws-calendar-agenda/SKILL.md) | Google Calendar: show upcoming events. |
| [gws-calendar-insert](skills/gws-calendar-insert/SKILL.md) | Google Calendar: create an event. |

### Web and React (from Vercel)

| Skill | What it does |
|---|---|
| [vercel-react-best-practices](skills/vercel-react-best-practices/SKILL.md) | React and Next.js performance guidelines. |
| [vercel-composition-patterns](skills/vercel-composition-patterns/SKILL.md) | React composition patterns for component APIs. |
| [vercel-react-native-skills](skills/vercel-react-native-skills/SKILL.md) | React Native and Expo best practices. |
| [vercel-react-view-transitions](skills/vercel-react-view-transitions/SKILL.md) | Animations with React's View Transition API. |
| [web-design-guidelines](skills/web-design-guidelines/SKILL.md) | Review UI code against Web Interface Guidelines. |

### Placeholder

[visualization](skills/visualization/SKILL.md) is a stub waiting on the upstream family from `Gerico1007/dotagents`. The Install loop skips it.

## Skills hosted in other repos

These appear in `skills/` as local symlinks and are not tracked here. Install each from its source.

| Skill | Source |
|---|---|
| [chronicle-episode](https://docs.miadi-orchestration-kit.jgwill.com/skills/chronicle-episode/SKILL.html) | `jgwill/miadi-orchestration-kit`, install with its `scripts/install-chronicle-skill.sh` |
| [miadi-react](https://docs.miadi-orchestration-kit.jgwill.com/skills/miadi-react/SKILL.html) | `jgwill/miadi-orchestration-kit` |
| [proposal-visualization](https://docs.miadi-orchestration-kit.jgwill.com/skills/proposal-visualization/SKILL.html) | `jgwill/miadi-orchestration-kit` |
| [miadi-review](https://docs.miadi.jgwill.com/packages/review-service/skills/miadi-review/SKILL.html) | `jgwill/Miadi`, `packages/review-service/skills/miadi-review` |

Link one with `ln -sfn <checkout>/skills/<name> ~/.claude/skills/<name>`.

## mw-managed skills (not in this repo)

Medicine-wheel skills are distributed by the `mw` CLI, not stored here:

```bash
mw skill install   # installs to ~/.claude/skills/.mw/skills/
# then symlink up:
ln -s .mw/skills/<name> ~/.claude/skills/<name>
```

Current mw skills: `direction-inquiry`, `fire-keeper-check`, `wave-spec-generator`, `ceremony-guide`

MCP tool guidance is tracked at jgwill/medicine-wheel#73. Migration context: jgwill/dotagents#7

## Not skills

These sit under `skills/` or the repo root and are not installable. Install ignores them because they have no `SKILL.md`.

- `skills/AGENTS.md`: status notes per skill.
- `skills/jgt-skills/`: one shell script for the trading platform, no skill yet.
- `skills/miadi/`: parent folder of the two Facebook skills.
- `skills/output/`, `skills/.pde/`, `skills/.hch/`: session output and tooling state, per machine.
- `skills/.mw/`: target of `mw skill install`.
- `archived-skills/`: retired skills, kept for history.
- `agents/`, `commands/`: agent persona JSON and command prompts.
