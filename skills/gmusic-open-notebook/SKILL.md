---
name: gmusic-open-notebook
description: Start, stop, check, and use the open-notebook research app on Eury (gaia.jgwill.com). Use when someone wants to run open-notebook, open the research notebook, ingest sources/PDFs/audio/video, query notes with an LLM, or asks how to bring open-notebook back up. It is STOPPED BY DEFAULT to save memory — this skill is how you wake it.
---

# gmusic-open-notebook

**open-notebook** is a self-hosted, privacy-first research notebook (a NotebookLM alternative). You feed it sources — PDFs, links, audio, video — it ingests/transcribes them, lets you chat and search across them with an LLM, and generates summaries and podcasts.

On Eury it runs as **one all-in-one container** (SurrealDB + REST API + worker + Next.js UI).

## Status: STOPPED BY DEFAULT
It is intentionally left stopped with restart policy `no` so it consumes no RAM and does **not** return on reboot. Wake it only when needed, and stop it again when done.

## Where it lives
- Project dir: `/home/gmusic/workspace/open-notebook`
- Compose file: `docker-compose.single.yml`
- Container name: `open-notebook-open_notebook_single-1`
- Repo: `github.com/Gerico1007/open-notebook`
- Data (bind mounts, persist across stop/start): `./notebook_data` and `./surreal_single_data`
- Ports when running: **8502** = Next.js UI · **5055** = REST API (`/docs` for API docs)

## Start it (wake)
```bash
cd /home/gmusic/workspace/open-notebook
docker compose -f docker-compose.single.yml up -d
# wait ~20-40s, then open http://localhost:8502  (API: http://localhost:5055/docs)
```

## Stop it (put back to sleep — the default state)
```bash
cd /home/gmusic/workspace/open-notebook
docker compose -f docker-compose.single.yml stop
# or: docker stop open-notebook-open_notebook_single-1
```

## Check status / logs
```bash
docker ps -a --filter name=open_notebook --format '{{.Names}}: {{.Status}}'
docker logs -f open-notebook-open_notebook_single-1
```

## Keep it alive across a reboot (only while actively using it)
Default policy is `no`. To make it survive a reboot during a work stretch:
```bash
docker update --restart=unless-stopped open-notebook-open_notebook_single-1
```
Return it to the default when done:
```bash
docker update --restart=no open-notebook-open_notebook_single-1
```

## Notes
- Data lives in the bind mounts above, so stopping/starting never loses notebooks.
- It binds `0.0.0.0` — reachable beyond localhost; stop it when idle.
- Memory footprint when running is small (~100 MiB idle), but the point of default-stopped is one less always-on process on a memory-pressured box.
