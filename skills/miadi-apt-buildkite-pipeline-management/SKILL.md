---
name: miadi-apt-buildkite-pipeline-management
description: Use when a Buildkite Package Registry already exists for the account, and the need is to onboard another repo/pipeline into it, troubleshoot why a release didn't publish, catch up a missed release, or rotate the publish token. Not for first-time setup of the registry/GitHub connection itself (see miadi-apt-buildkite-pipeline-setup).
---

# Miadi Apt / Buildkite Pipeline — Onboarding & Maintenance

## Overview

Assumes the registry-level work is already done: a Buildkite org connected
via GitHub App, and at least one public Debian Package Registry. This skill
covers the *ongoing* work — adding another repo's pipeline into that same
registry (whether it's the second one or the tenth), and diagnosing/fixing
the failure mode that looks identical to "nothing went wrong yet." Companion
to **miadi-apt-buildkite-pipeline-setup**, which this does not repeat in
full — cross-reference it for exact click-paths.

**Provenance:** grounded in the same 2026-07-30 build-out as the setup skill,
one account. Where a claim below is phrased as "observed" or "in this
account," treat it as one data point to verify, not a guaranteed default.

## When to use which skill

- **No registry exists at all** → `miadi-apt-buildkite-pipeline-setup` (do
  all of it, including the pipeline for the first repo).
- **A registry already exists** — whether zero, one, or many pipelines
  currently publish to it — and the task is adding a repo, or fixing/
  maintaining an existing one → this skill.

## Onboarding another repo into the existing registry

Don't create a second registry unless there's a real reason to segment
audiences (different visibility, different team). One registry serves every
app's `.deb` — apt clients add the source once and get every onboarded app.

1. Do `miadi-apt-buildkite-pipeline-setup`'s steps **2, 3, 4, 5, and 7**
   (connect the repo, bootstrap pipeline, author `pipeline.yml`, turn on
   Build tags, verify) for the new repo — pointing the `curl` publish URL at
   the **same** registry slug the first repo uses
   (`.../registries/<same-registry-slug>/packages`). **Skip its step 6** (the
   cluster secret) — see next.
2. The cluster secret (`PACKAGES_API_TOKEN`) is already there — reuse it,
   don't create a per-repo secret, unless the org wants per-repo credential
   scoping (then name it distinctly and update that repo's `pipeline.yml`
   accordingly).
3. Still turn "Build tags" on for the new pipeline (setup's step 5, the
   toggle under Pipeline → Settings → GitHub → GitHub Settings) — this
   setting is per-pipeline, not inherited from the first one.
4. Still document, in the new repo's own `CLAUDE.md`/`AGENTS.md`, every
   release-related action that repo has (its own version-bump/ship scripts
   plus this Buildkite leg) — the same picture setup's step 8 describes for
   the first repo. It doesn't carry over automatically; each repo's docs are
   separate.

## Troubleshooting: "my release didn't show up in the registry"

Work through in order — don't skip to guessing, and don't stop at the first
plausible cause without confirming it:

1. **Confirm the tag actually reached GitHub:**
   `git tag -l 'vX.Y.Z'` and `git ls-remote origin` (or `gh api
   repos/<owner>/<repo>/tags`).
2. **Confirm GitHub delivered the webhook:**
   First find Buildkite's hook ID — `gh api repos/<owner>/<repo>/hooks` and
   pick the entry whose `config.url` contains `webhook.buildkite.com` (there
   may be other unrelated hooks on the same repo; don't assume there's only
   one). Then `gh api repos/<owner>/<repo>/hooks/<that-id>/deliveries` — look
   for `push` and `create` events near the tag's timestamp, `status: "OK"`.
   **A 200 here proves GitHub sent it. It proves nothing about whether
   Buildkite built anything from it.** (Needs a `gh` token with repo hook-read
   access — the same auth used to manage the repo normally covers this.)
3. **Confirm a build actually exists for that tag:**
   Buildkite pipeline → Builds (or "All branches" filter) — look for a build
   whose ref is the tag. If webhook delivery succeeded but no build exists,
   check, in order:
   - Pipeline → Settings → GitHub → GitHub Settings → the `push` group's
     **Build tags** checkbox (the single most common cause found in this
     account's testing — see `miadi-apt-buildkite-pipeline-setup`'s step 5,
     the Build-tags toggle, for why it's easy to miss). Turn it on, save,
     reload the page to confirm it stuck.
   - If that's already on: the pipeline's branch/tag **filter pattern**
     (same Settings page, "Branch Limiting") — a pattern that excludes the
     tag's name.
   - Any conditional/skip rule on the upload step itself (e.g. "Skip builds
     for existing commits").
4. **If a build exists but the publish step didn't run:** check whether it
   was a real tag-push build or a manually-created one ("New Build" with a
   tag name typed into the Branch field). In this account's testing, manual
   builds did not set `build.tag` — an `if: build.tag != null` step showed
   as silently skipped ("N skipped steps hidden" in the build view), not as
   a failure. Treat this as expected for manual builds rather than something
   to debug in the pipeline; if you observe a manual build's tag-gated step
   actually running, trust that observation over this note.
5. **If the secret lookup or curl failed:** open the build's job log for the
   publish step directly — `buildkite-agent secret get` returns a clear error
   if the secret is missing/misnamed, and `curl -sf` surfaces a non-2xx
   registry response instead of printing a false success.

## Catching up a release that was missed

If a version was already built and shipped elsewhere (e.g. to GitHub
Releases) before a trigger fix above, and the local `./release/` (or
equivalent build output directory) still has the matching artifact:

1. Generate a **short-lived** API Access Token yourself (scopes
   `read_packages` + `write_packages`), described as a one-off catch-up so
   its purpose is legible in the token list.
2. `curl -sf -X POST https://api.buildkite.com/v2/packages/organizations/<org>/registries/<registry-slug>/packages -H "Authorization: Bearer $TOKEN" -F "file=@<path-to-deb>"` —
   the same call the real pipeline makes (keep `-sf` so a failure doesn't
   print as a silent success).
3. **Revoke that token, then verify the revocation took** by reloading the
   API Access Tokens list and confirming it's gone — don't just say you
   revoked it. This is the one case where the agent generating/using a token
   itself is fine: it never becomes a standing credential, provided
   revocation is actually confirmed. Its value will still sit in your shell
   history/session transcript for as long as those persist — a real,
   accepted cost of this exception, not something the revocation erases.
4. If this is the **second** time this same pipeline has needed a catch-up,
   stop and fix the underlying trigger (see Troubleshooting above) instead
   of minting another token — a repeating catch-up means the automation
   still isn't actually automatic.
5. Don't try to force a manual Buildkite build to do this instead — see
   Troubleshooting step 4 above for why that path doesn't set `build.tag`.

## Rotating the publish token

1. Generate a new API Access Token (same scopes) — human does this step,
   generates it, and pastes the value into the cluster secret's edit screen
   themselves (Buildkite → Agents → cluster → Secrets → the secret → edit
   value). The agent names the exact field and exact destination and does
   not type the value in, even if asked to for convenience.
2. Once confirmed working (next release, or a manual catch-up per above),
   revoke the old token from User → API Access Tokens and confirm the list
   no longer shows it.

## Checking registry health

- **What's published:** Package Registries → registry → **Releases** tab
  lists every package/version currently hosted.
- **Client install snippet for a specific package:** that package's
  **Installation** tab — always use Buildkite's own generated snippet
  (GPG key URL + `sources.list` line + `apt install` line), don't compose
  one from memory; it stays correct even if the underlying URL shape changes.
- **Never used yet:** a cluster secret's "Last read" column stays "Never"
  until a real pipeline build actually calls `buildkite-agent secret get`
  for it — a useful early signal that no real tag-triggered build has run.

## Common Mistakes

- Creating a second registry per repo instead of reusing the one shared
  registry — fragments the apt source users have to add.
- Assuming "Build tags" carries over when onboarding a new repo — it's set
  per pipeline.
- Treating a 200 OK webhook delivery as proof a build ran, or stopping at
  the Build-tags toggle without checking branch filters/conditionals when
  that toggle turns out to already be on.
- Fighting manual-build semantics to reproduce a tag-triggered release —
  publish directly instead (see Catching up, above).
- Generating a long-lived rotation token and pasting it in yourself instead
  of directing the human to, even when they ask you to for speed.
- Asserting a catch-up token was revoked without reloading the tokens list
  to confirm.
- Letting catch-up publishing become a recurring habit instead of a signal
  to fix the trigger.
