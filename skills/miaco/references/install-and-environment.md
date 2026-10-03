# miaco Install And Environment

## Install

```bash
npm install -g mia-co
miaco --help
```

From the `mia-code` repository:

```bash
cd miaco
npm install
npm run build
npm link
```

## Packaged Skill

```bash
miaco skill show
miaco skill install
miaco skill install --global --yes
```

`--yes` creates a `.claude/skills/miaco` symlink. `--force` replaces an existing install or symlink. Reinstall after upgrading miaco so the skill matches the CLI.

## Key Environment Variables

`miaco --help` prints every variable with its current and default value. The ones most often set:

| Variable | Purpose |
|---|---|
| `MIACO_CONFIG` | Persistent config path used by `miaco set`; defaults to `~/.config/miaco/config.json` |
| `MIACO_DEFAULT_ENGINE` | Environment override for default engine; config fallback defaults to `claude` |
| `MIACO_MODEL` | Cross-engine model override |
| `MIACO_PI_PROVIDER`, `MIACO_PI_MODEL`, `MIACO_PI_THINKING` | pi engine; defaults `openai-codex`, `gpt-5.6`, `xhigh` |
| `MIACO_PVA_PROVIDER`, `MIACO_PVA_MODEL`, `MIACO_PVA_THINKING` | pva engine; defaults `openai-codex`, `gpt-5.6`, `high` |
| `MIACO_PVA_EXTENSION` | pi extension pva loads for the `pde_submit` tool; defaults to `@avadisabelle/ava-pde`, empty disables |
| `PVA_HOME` | pi agent directory for pva; defaults to `~/.pva/agent` |
| `MIACO_HERMES_PROVIDER` | Hermes Agent provider passthrough |
| `MIACO_OLLAMA_MODEL`, `MIACO_OPENCODE_MODEL` | Local model overrides for the ollama and opencode engines |
| `MIA_CODE_<ENGINE>_BIN` | Engine binary path, for `COPILOT`, `CLAUDE`, `GEMINI`, `CODEX`, `PI`, `PVA`, `HERMES`, `OLLAMA`, `OPENCODE` |
| `MW_API_URL` | Medicine wheel API for `miaco memory` and `steer --memory`, such as `http://127.0.0.1:8040` |
| `MIACO_QMD_PROVIDER` | QMD provider: `container`, `host`, `mcp-local`, or `mcp-remote`; host is valid when QMD is installed locally |
| `MIACO_QMD_CONTAINER_DISABLED` | Legacy host-local switch |
| `MIACO_QMD_BIN` | Explicit host-local `qmd` binary for permitted local environments |
| `MIACO_QMD_MCP_COMMAND` | Full MCP stdio command for `mcp-local` or `mcp-remote` providers |
| `MIACO_QMD_MCP_CONFIG` | MCP config JSON containing a stdio QMD server, such as `mia-qmd/etc/mcp-config-qmd-remote-eury.json` |
| `MIACO_QMD_MCP_SERVER` | Server key inside `MIACO_QMD_MCP_CONFIG`; defaults to `qmd-remote` for remote MCP |
| `MIACO_QMD_COLLECTIONS` | Comma-separated default collections passed to QMD providers |
| `MIACO_LLMS_ROOT` | Parent directory containing `llms/llms-structural-thinking.txt` and `llms/llms-st-four-questions.md` for `pde-to-st` when `.pde` workdir is outside the guidance tree |
| `MIACO_STRUCTURAL_THINKING_GUIDANCE_ROOT` | More specific guidance root override for `pde-to-st`; accepts the parent directory or the `llms` directory itself |
