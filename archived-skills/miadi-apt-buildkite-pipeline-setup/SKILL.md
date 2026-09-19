---
name: miadi-apt-buildkite-pipeline-setup
description: Use when a Buildkite Package Registry and pipeline for `apt install`-style .deb distribution do not exist yet for an account — first-time setup of the registry, GitHub App connection, pipeline, tag-build trigger, and cluster secret. Not for adding another repo to an already-working setup, or for troubleshooting an existing one (see miadi-apt-buildkite-pipeline-management for both).
---

# Miadi Apt / Buildkite Pipeline — First-Time Setup

## Overview

Buildkite Package Registries (formerly packagecloud, now folded into Buildkite
itself) can host a real Debian/Ubuntu apt repository, and Buildkite pipelines
can build and publish to it automatically on release. This skill is the
from-scratch path: no registry, no pipeline, no GitHub connection yet.

**Provenance:** built and verified end-to-end 2026-07-30 against one account
(miadisabelle, `mia-parallel-code` repo, `miadi-apt` registry — two versions
published, one caught up manually after fixing the gotcha in step 5). Treat
anything below phrased as "in this account" or "observed" as one data point,
not a guaranteed universal default — verify before relying on it if the
outcome matters. The concrete UI paths (menu names, checkbox labels, tab
names) are the durable part; specific defaults and plan behavior can drift.

**Before this skill:** confirm the app's built package can't be self-hosted
via plain git+GitHub Pages — GitHub hard-blocks any pushed blob over 100MB, so
Electron-sized `.deb` files (100MB+) need a real package host, not a hand-rolled
`dists/`+`pool/` repo in a git-backed Pages site. Buildkite Package Registries
has no such limit.

**Login gotcha:** log in to Buildkite via **"Sign in with GitHub"** using the
target GitHub account, not email/password or Google — Buildkite orgs are keyed
to how you authenticated, and a different login method can land you in an
unrelated personal org that only superficially looks right.

## Prerequisites likely already provided by the Buildkite org

The account this was built against already had a **"Default cluster"**
pre-stocked with **Hosted Agent queues** (`linux-small`, `linux-medium`,
`linux-large`, `macos-medium`, `macos-large`) — Buildkite-managed runners that
auto-scale on demand, needing no self-hosted agent install. Check **Agents**
in the org nav → the cluster's **Queues** tab before assuming you need to
provision anything: if hosted queues already exist, `agents: { queue:
"linux-medium" }` in a pipeline step just picks one by name (exact names
available can differ by plan — read them off the Queues tab, don't assume
this list). If no cluster/queues exist at all, provisioning an agent or
cluster is a separate concern this skill doesn't cover.

**Plan/billing gate:** Package Registries and hosted agents can be limited by
plan (evaluation trials show a countdown banner like "N days left on your
evaluation trial"). If registry creation or a build unexpectedly fails outside
anything this skill covers, check the org's plan/trial status before assuming
a configuration mistake.

## Workflow

### 1. Create the Package Registry
Buildkite → **Package Registries** → New Registry:
- Ecosystem: **Debian/Ubuntu (deb)**
- Teams: **Everyone** (or as scoped as the org needs)
- Name it for the *distribution*, not the app — one registry can (and should)
  host every app's `.deb` if there will be more than one, so a name like
  `<org>-apt` beats a per-app name.
- After creating, go to registry **Settings** → **Registry Management** →
  **Make registry public**. The confirmation dialog shows the exact slug in
  the dialog text itself (`please type the slug of this registry: <slug>`) —
  retype exactly what's displayed there, don't derive or guess it. This is
  required — `apt install` needs anonymous reads, and non-public registries
  only serve authenticated users.

### 2. Connect the GitHub repo to a new pipeline
Buildkite → **Pipelines** → **New Pipeline** → **Git scope** dropdown → if the
target GitHub account isn't listed, **Connect GitHub account**. This installs
Buildkite's **GitHub App** (not a classic per-repo "Add webhook" — the app
install itself registers the webhook, and the browser flow may auto-select the
repo you were about to add). **If the target account is a GitHub organization
(not a personal account), this install may need approval from an org owner**
before it completes — a human-gated step like step 6's token, not something
to work around. Confirm the repo is preselected, name the pipeline (matches
the repo name by convention).

### 3. Set the pipeline's initial steps to the bootstrap pattern
In the **YAML Steps editor** on that same New Pipeline screen, replace
whatever's there with:
```yaml
steps:
  - command: buildkite-agent pipeline upload
```
This makes the pipeline always re-read `.buildkite/pipeline.yml` fresh from
whatever commit it's building — never hand-edit the real steps in Buildkite's
UI, edit the file in the repo. Create the pipeline.

### 4. Author `.buildkite/pipeline.yml` in the target repo
Gate the actual work on `if: build.tag != null` so ordinary branch pushes are
a no-op and only real releases (tag pushes) build+publish. Read the token via
`buildkite-agent secret get` — never hardcode it, never pass it as a literal
pipeline env var. Example (adapt build commands to the app):
```yaml
steps:
  - label: ":debian: Publish .deb to <registry-slug>"
    if: build.tag != null
    command: |
      apt-get update -qq && apt-get install -y -qq python3 make g++ fakeroot >/dev/null
      npm ci
      npm run build
      deb=$(ls release/*.deb)
      token=$(buildkite-agent secret get PACKAGES_API_TOKEN)
      curl -sf -X POST "https://api.buildkite.com/v2/packages/organizations/<org>/registries/<registry-slug>/packages" \
        -H "Authorization: Bearer ${token}" \
        -F "file=@${deb}"
    agents:
      queue: "linux-medium"
```
The publish URL shape (`api.buildkite.com/v2/packages/organizations/<org>/registries/<slug>/packages`)
matched this account's own generated "Publish Instructions" page for the
registry (Package Registries → registry → **Publish Instructions** tab) as of
2026-07 — this product surface has already changed once (packagecloud →
Buildkite), so if this exact call ever 404s or rejects auth unexpectedly,
re-read that tab for the current form rather than assuming the pipeline.yml
is wrong. Commit and push this file to the repo's default branch before
relying on it — the pipeline can't read a file that isn't on GitHub yet.

### 5. Turn on "Build tags" — the gotcha most likely to silently no-op everything
Pipeline → **Settings** → **GitHub** → **GitHub Settings** → the `push`
trigger group has two checkboxes: **Build branches** and **Build tags**. In
the account this was tested against, **Build branches was on and Build tags
was off** by default — don't assume this without opening the page and
checking, but if the release trigger is a tag push (`npm version` +
`git push --follow-tags`, or any tag-based release script), **Build tags**
must be checked. After checking it, click **Save GitHub Settings**, then
reload the page and confirm the checkbox is still checked — don't treat the
click alone as confirmation.

**Why this is dangerous:** GitHub's webhook delivery log can show the tag's
`push` and `create` events delivered successfully (200 OK) even when Buildkite
never creates a build from them — this is the failure mode this step guards
against, but it is not the *only* possible cause of "webhook OK, no build."
A pipeline's branch/tag filter pattern (Settings → GitHub → **Branch
Limiting**) or a conditional/skip-build rule can produce the identical
symptom. If turning "Build tags" on doesn't resolve a missing build, check
those next — see `miadi-apt-buildkite-pipeline-management`'s troubleshooting
flow for the full order.

### 6. Create the cluster secret — human does this step, not the agent
Buildkite → **Agents** → the pipeline's cluster → **Secrets** → **New secret**,
key `PACKAGES_API_TOKEN`. The *value* is a Buildkite API Access Token
(User → API Access Tokens → New, scopes `read_packages` + `write_packages`,
org-scoped) that **the human generates and pastes in themselves** — don't
generate a long-lived credential and relay it through chat/tool calls, even
though the browser tooling could technically type it in, and **even if the
human offers or asks you to paste it for them to save time** — decline and
explain why: the point is keeping the value out of your own context and
logs, and that holds regardless of who's asking. If a human hand-off is
needed, build a plain step-by-step artifact naming the exact fields and
exact destination page rather than describing it in prose.

A short-lived token *you* generate solely to prove the publish call works
once is a different and acceptable exception, with conditions: (a) name it
descriptively (e.g. "one-off catch-up") so its purpose is legible in the
token list, (b) after using it, **revoke it and then verify the revocation
took** by reloading the API Access Tokens list and confirming it's gone —
don't just assert that you revoked it, (c) be aware the token value will sit
in cleartext in your own shell history / session transcript for as long as
those persist — this is a real, unavoidable cost of the exception, not a
clean workaround, and (d) if you find yourself reaching for this exception a
second time on the same pipeline, that's a signal to fix the underlying
trigger (see step 5) instead of minting another token — don't let repeated
"one-offs" become the normal path.

### 7. Verify end-to-end
Either wait for a real tag push, or prove the mechanism once with the
step-6 exception (a short-lived, immediately-revoked token) publishing an
already-built `.deb` directly via `curl`. In this account's testing, a
**Buildkite "New Build"** with a tag name typed into the Branch field did
**not** populate `build.tag` — the pipeline's `if: build.tag != null` step
showed as skipped even though the branch field read `v1.2.3`. This is
consistent with `build.tag` being populated from the actual webhook ref
rather than the Branch field, so treat manual builds as unsuitable for
validating the tag-triggered path — either push a real tag or publish
directly. If you see different behavior (the manual build's step actually
ran), trust what you observe over this note and update it.

### 8. Document the release picture in the repo
Most apps that get this far already have at least one other release action
(e.g. a version-bump script, a script that ships built artifacts to GitHub
Releases). Write into the repo's `CLAUDE.md`/`AGENTS.md` that this Buildkite
leg is an **additional, independent** one alongside whatever already exists:
it builds on Buildkite's own agent (not from any local build directory),
needs no trigger phrase, and fires purely off the tag reaching GitHub. Name
every release-related action the repo actually has (however many there are)
so a future agent doesn't assume any single one of them covers the others.

### 9. Hand over the client install snippet
Each published package's **Installation** tab (Package Registries → registry
→ a package) has Buildkite's own generated client instructions — GPG key URL,
`sources.list` line, and the `apt install` command. Use that generated
snippet verbatim rather than composing one from memory; it already has the
right `packages.buildkite.com/<org>/<registry>/...` paths, and stays correct
even if that URL shape changes in the future.

## Quick Reference

| Thing | Where |
|---|---|
| Registry create/settings | Package Registries → New Registry / registry Settings |
| Pipeline create | Pipelines → New Pipeline (Git scope → Connect GitHub account if needed) |
| Hosted agent queues | Agents → cluster → Queues tab (verify before assuming) |
| Bootstrap step | Pipeline's initial YAML: `buildkite-agent pipeline upload` |
| Real steps | `.buildkite/pipeline.yml` in the repo, gated `if: build.tag != null` |
| Build tags toggle | Pipeline → Settings → GitHub → GitHub Settings → `push` group |
| Publish token | Cluster → Secrets → `PACKAGES_API_TOKEN`, read via `buildkite-agent secret get` |
| Client install snippet | Package Registries → registry → a package → Installation tab |

## Common Mistakes

- Assuming a delivered (200 OK) webhook event means a build happened — check
  the pipeline's Builds list and the "Build tags" toggle (and, if that's not
  it, branch/tag filters and conditional rules), not just the delivery log.
- Hand-editing pipeline steps in the Buildkite UI instead of the repo's
  `.buildkite/pipeline.yml` — breaks the bootstrap pattern's whole point.
- Generating the long-lived publish token yourself and typing it into a
  form — direct the human to generate and paste it themselves, even if asked to do it for them.
- Asserting a token was revoked without reloading the tokens list to confirm
  it's actually gone.
- Letting a repeated "one-off catch-up" token become routine instead of
  fixing the underlying trigger it's compensating for.
- Trying to validate the tag-gated step via a manual "New Build" with a tag
  name in the Branch field — `build.tag` was observed to stay null there.
- Building a self-hosted apt repo on GitHub Pages for an app whose package
  exceeds 100MB — it will not push.

See **miadi-apt-buildkite-pipeline-management** for onboarding another repo
into an already-existing setup, and for troubleshooting/catch-up procedures.
