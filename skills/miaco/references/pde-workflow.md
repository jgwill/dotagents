# miaco PDE Workflow

Use this sequence when a request is large enough that acting directly would lose implicit intent.

## 1. Read the prompt as a PDE

```bash
miaco decompose run -p "<prompt>" --json
miaco decompose run -P ./prompt.md -w ./my-repo --json
```

`-p @./prompt.md` also reads a file. `--json` prints the stored record, including the UUID and folder. Keep the UUID, or the `YYMMDDHHmm--<uuid>` folder name, for every later step.

Pick a strategy when one pass is not enough: `-s iterative-refinement` for four staged calls, `-s adversarial-consensus` for an optimistic and a critical reading reconciled.

## 2. Nest children when the work splits

```bash
miaco decompose run --parent <parent-id> --child-kind issue -p "<child prompt>" --json
```

| Kind | Use |
|---|---|
| `milestone` | A root scope. Takes no parent. |
| `issue` | Under a milestone |
| `sub-task` | Under an issue |
| `follow-up` | Work discovered along the way |
| `refinement` | A new reading of the same artifact. `--parent` is the prior version, and the new PDE gets its own UUID. |
| `sibling` | Beside the parent |

`--meta '<json>'` stores provenance in the child's `meta.json`. `--uuid` supplies a UUID the caller already owns. `--session-id` records a known engine session.

## 3. Decompose a recorded artefact

```bash
miaco decompose artefact ./captures/<capture>            # offline: forms, intents, routed strategies
miaco decompose artefact ./captures/<capture> --segments # read what each transcription says
miaco decompose artefact ./captures/<capture> --run --dry-run
miaco decompose artefact ./captures/<capture> --run -w ./my-repo --parent <pde-id>
```

It accepts a capture folder, an episode's `captures/` directory, or a legacy composition folder. `--run` writes one PDE per transcription. Name the vessel with `-w`: a recording folder cannot be its own vessel.

## 4. Clarify, remember, enrich

```bash
miaco clarify run --pde <pde-id>
miaco memory resolve --pde <pde-id> --within circle:<id>
miaco clarify run --pde <pde-id>   # again, to fold memory's answers in
miaco qmd-inquiry-decompose formulate --pde <pde-id>
miaco qmd-inquiry-decompose run --pde <pde-id>
```

`clarify` puts what it cannot settle under *Still Open*. `memory resolve` asks the wheel about those items along with the PDE's ambiguities, open actions and outputs, and marks each answered, inferred or open with its sources. Running `clarify` again folds the answers in, and `formulate` builds its QMD queries from the clarifications. `memory resolve` needs `MW_API_URL` and the `claude` or `copilot` engine. Enrich before planning when the repository, wiki, or notes probably hold context the prompt did not name.

## 5. Structural Thinking and the chart

```bash
miaco pde-to-st run --pde <pde-id>        # picture, draft, review, revise
miaco pde-to-st run --pde <pde-id> --fast # one pass
miaco stc convert <pde-id>
```

What the executor needs is the tension between the desired outcome and current reality, not only a task list.

## 6. Check the PDE against the contract

```bash
miaco schema validate .pde/<folder>/pde-<uuid>.json
miaco schema validate <file> --stage directions --strict
```

`miaco schema parts` names the seven parts and the stage that fills each.

## 7. Prepare the executor handoff

```bash
miaco executor prepare --pde <pde-id> --status partial --gate "Human approves the migration"
```

This writes `executor-prompt.json` and `EXECUTOR-PROMPT.md` beside the PDE. The package separates Context, Intention, Unknowns / human gates, Provenance, and Closure so a downstream agent does not receive one blended prompt.

## 8. Chain, continue, steer

```bash
miaco continue --pde <pde-id> --steps clarify,qmd,pde-to-st,stc,executor --fast-st --no-interactive
miaco continue --pde <pde-id>
miaco steer --pde <pde-id> -p "<next instruction>"
miaco steer --pde <pde-id> --memory -p "<question about what was already decided>"
```

Step aliases: `formulate` for `formulate-qmd-queries`, `qmd` or `enrich` for `qmd-inquiry-decompose`, `questions` for `pde-to-st`, `handoff` for `executor`. Use `steer` for one bounded non-interactive prompt. Use `continue` to resume the session interactively.
