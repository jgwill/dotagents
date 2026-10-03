---
name: miaco
description: Use miaco to decompose a prompt or a recorded artefact into a PDE, clarify it, enrich it with QMD and the medicine wheel's memory, turn it into Structural Thinking and a Structural Tension Chart, check it against the decomposition schema, package it for an executor, and continue or steer the engine session that made it.
license: MIT
compatibility: Requires the miaco CLI from the mia-co package.
metadata:
  author: Guillaume D. Isabelle
  version: "1.1.2"
allowed-tools: Bash(miaco:*)
---

# miaco - engineering perspective CLI

`miaco` is the engineering-perspective command surface inside the `mia-code` family. Use it when a request is large enough that acting on it directly would lose implicit intent: decompose it first, then work from the PDE.

## Status

!`miaco status 2>/dev/null || echo "Not installed: npm install -g mia-co"`

## Where a PDE lives

Each PDE is a folder `.pde/<YYMMDDHHmm>--<uuid>/` under the working directory (`-w, --workdir`). Every `--pde` and `--parent` flag accepts the bare UUID or that folder name.

- miaco refuses to write a PDE into `/tmp` or `/var/tmp`. When `-w` is omitted, the current directory must be inside a git working tree. Pass `-w <vessel>` to choose where the record is kept.
- `meta.json` records the engine, model, strategy, session id, `--add-dir` paths, and `origin`: user, host, miaco version, git commit, and whether a person or an agent ran it.

## Core Flow

1. Decompose:

```bash
miaco decompose run -p "Add a health endpoint that reports DB and Redis status" --json
miaco decompose run -P ./prompt.md -s iterative-refinement -w ./my-repo --json
```

2. Clarify the obvious ambiguities and placeholders. What it cannot settle goes under *Still Open*:

```bash
miaco clarify run --pde <pde-id>
```

3. Ask the medicine wheel's memory about every ambiguity, open action, expected output and *Still Open* item (needs `MW_API_URL`). Each comes back answered, inferred or open, with the wheel records it rests on. Run `clarify` again to fold the answers in:

```bash
miaco memory resolve --pde <pde-id> --within circle:<id>
miaco clarify run --pde <pde-id>
```

4. Enrich from QMD. `formulate` asks the PDE's own session for queries, using the clarifications, and `run` searches them:

```bash
miaco qmd-inquiry-decompose formulate --pde <pde-id>
miaco qmd-inquiry-decompose run --pde <pde-id>
```

5. Translate into Structural Thinking and a Structural Tension Chart:

```bash
miaco pde-to-st run --pde <pde-id>
miaco stc convert <pde-id>
```

6. Package it for the executor. The package carries the clarifications, QMD findings, memory resolution, Four Questions and chart when they exist:

```bash
miaco executor prepare --pde <pde-id> --status partial
```

7. Continue or steer the same engine session:

```bash
miaco continue --pde <pde-id>
miaco steer --pde <pde-id> -p "Implement the next verified step"
```

Clarify, QMD, Structural Thinking, STC and the executor package run as one chain with `continue --steps`, in the order given. `memory resolve` is not a step: run `clarify` and `memory resolve` first, and a chain that starts with `clarify` folds memory's answers in. `--no-interactive` stops after the chain instead of reopening the session:

```bash
miaco continue --pde <pde-id> --steps clarify,formulate-qmd-queries,qmd-inquiry-decompose,pde-to-st,stc,executor --no-interactive
miaco continue -p "<prompt>" --steps clarify,pde-to-st,executor   # create the PDE first
```

## What each step writes

| Step | File in the PDE folder |
|---|---|
| `decompose run` | `pde-<uuid>.json`, `pde-<uuid>.md`, `meta.json` |
| `clarify run` | `pde-clarifications.md` |
| `memory resolve` | `memory-resolution.md`, `memory-resolution.json` |
| `qmd-inquiry-decompose formulate` | `pde-qmd-queries.json`, `pde-qmd-queries.md` |
| `qmd-inquiry-decompose run` | `pde-inquiry-enrichment.md` |
| `pde-to-st run` | `pde-four-questions.md` (plus `.picture`, `.draft`, `.review` without `--fast`) |
| `executor prepare` | `executor-prompt.json`, `EXECUTOR-PROMPT.md` |
| `steer` | `steers/<timestamp>.md` unless `--no-persist` |

`stc convert` writes a coaia-narrative JSONL chart (`-o` to choose the path).

## Command Map

| Command | Use |
|---|---|
| `miaco decompose run` | Persist a PDE from a prompt |
| `miaco decompose list`, `get <id>` | List recent PDEs, retrieve one |
| `miaco decompose artefact <dir>` | Read an artefact's transcriptions and route each to a form-matched decomposition; offline unless `--run`, `--dry-run` to preview (alias: `composition`) |
| `miaco clarify run` | Resolve obvious ambiguities inside an existing PDE |
| `miaco qmd search`, `qmd query` | BM25 keyword search, or semantic expansion with reranking |
| `miaco qmd-inquiry-decompose formulate`, `run` | Formulate QMD queries from the PDE, then add QMD findings to it |
| `miaco memory scope`, `resolve` | Show what the PDE's memory scope reaches (no engine), or resolve its open items from memory |
| `miaco pde-to-st run` | Structural Thinking Four Questions from the PDE (`--fast` for one pass) |
| `miaco stc convert`, `list`, `validate` | PDE to Structural Tension Chart JSONL (`-d` for deterministic, no LLM) |
| `miaco executor prepare` | Context, Intention, Unknowns / human gates, Provenance, Closure as one executor package |
| `miaco continue` | Run a step chain and reopen the interactive engine session |
| `miaco steer` | Send one non-interactive prompt into the PDE's session |
| `miaco schema parts`, `stages`, `show`, `validate <file>` | The decomposition contract: its seven parts, the stages that fill them, the JSON Schema, and whether a `.pde` artifact satisfies it |
| `miaco check` | Type-check the project with `tsc`, or refuse and say why |
| `miaco set` | Persist defaults: `default-engine`, `default-model`, `qmd-provider`, `qmd-collections` |
| `miaco chart`, `miaco trace` | COAIA chart operations and trace sessions |
| `miaco status`, `miaco examples`, `miaco skill` | Context, usage examples, this skill |

`miaco validate` is retired. Use `miaco schema validate` for a PDE and `miaco check` for code.

## Strategies

`-s` on `decompose run`, `continue`, and `decompose artefact`:

- `standard`: one call against the full schema (default).
- `iterative-refinement`: four calls, coarse, directions, actions, calibration, each against its own schema. Calibration returns to primary and secondary intent with what the middle stages found.
- `adversarial-consensus`: an optimistic and a critical reading, reconciled into one PDE.

`miaco schema stages` prints this from the code.

## Engine Selection

With no engine configured, miaco resolves to `claude` / `sonnet`. Engines: `copilot`, `claude`, `gemini`, `codex`, `pi`, `pva`, `hermes`, `ollama`, `opencode`.

```bash
miaco set default-engine claude
miaco set default-model sonnet
miaco set --list
MIACO_DEFAULT_ENGINE=pi miaco decompose run -p "Design the workspace setup"
miaco steer --pde <pde-id> -e codex -p "Review the implementation"
```

- `pva` runs pi with the `@avadisabelle/ava-pde` extension, and the decomposition comes back through its schema-bound `pde_submit` tool. `--pva-provider gh` selects GitHub Copilot, `oc` selects OpenAI Codex.
- `--add-dir <paths...>` gives the engine more directories and is kept in `meta.json`.
- `--yolo` on `continue` and `steer` passes each engine's permission bypass flag. Use it only when asked.
- `miaco --help` lists every environment variable with its current and default value.

## QMD Mode

Supported providers: `container`, `host`, `mcp-local`, `mcp-remote`. Host QMD works when the host has a `qmd` index. Use remote MCP when the index lives elsewhere:

```bash
MIACO_QMD_PROVIDER=mcp-remote \
MIACO_QMD_MCP_CONFIG=/path/to/your/mcp-config-qmd-remote.json \
MIACO_QMD_MCP_SERVER=qmd-remote \
miaco qmd-inquiry-decompose run --pde <pde-id>
```

`MIACO_QMD_MCP_CONFIG` is *your* stdio MCP config naming the remote QMD wrapper, and `MIACO_QMD_MCP_SERVER` names the entry inside it. Setting either `MIACO_QMD_MCP_CONFIG` or `MIACO_QMD_MCP_COMMAND` without a provider selects `mcp-remote`. Ask whoever maintains the index for the config. `--search-only` skips the slower semantic query.

## Memory Mode

A PDE can ask the medicine wheel's memory what has already been said about its ambiguities, open actions, expected outputs, and the *Still Open* items in `pde-clarifications.md`. miaco hands the engine the wheel's MCP server (`@medicine-wheel/mcp`, read tools only). The only setting is `MW_API_URL`. Engines: `claude`, `copilot`.

```bash
miaco memory scope --pde <pde-id> --within circle:<id>        # what the scope reaches, no engine
miaco memory resolve --pde <pde-id>                           # writes memory-resolution.md and .json
miaco steer --pde <pde-id> --memory -p "What did the circle decide about the release order?"
```

- **Scope:** the PDE's subject `pde:<root uuid>` plus what `--within` adds: a circle (`circle:…`), an episode (`YYYY-MM-DD-episode-…`), one person (`node:human:…`), a ceremony id, or another subject. `--within` works on `memory scope`, `memory resolve` and `steer`, and is kept in `meta.json`. The PDE's own opening ceremony is left out.
- **A new PDE** has nothing on the wheel yet, so without `--within` its scope reaches nothing. `memory scope` says so before any engine runs.
- **Verdicts:** `answered` when a wheel record says it, `inferred` when records point to it without saying it, `open` otherwise. Every answered or inferred item names its sources: the ceremony, the beat, who said it. What the engine knows from resuming the PDE's own session does not count as memory.
- **Downstream:** `clarify` treats answered items as resolved and inferred ones as still needing confirmation. `executor prepare` carries `memory-resolution.md` into the package.

## References

- `references/pde-workflow.md` for nesting, artefact decomposition, and the handoff.
- `references/install-and-environment.md` for install and environment variables.
