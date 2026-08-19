# GUILLAUME.md - disc with jerry 260818

* RISE disc on commits and workflow

## Notes

* There's 4 scripts that it always run maybe after it generated ABC and those 4 scripts are :
{{ Jerry list scripts here }}

## pi-coding-agent extensions to have either on the android device Pi running with what is possible there

### `/workspace/repos/eleqtrizit/pi-chains`

* How is that one can be a source of inspiration ?

* my fork at `jgwill/agent-pi` has teams and chains, what is (or are) the chain(s) that JamAI did ?
* * all the steps of what I exported in `/srv/miadi/episodes/miadi-chronicle/2026-08-16-episode-333-the-fork-arrives-launched-not-handed-over/salix/songbird-71bbe83b/README.md` from my ava002 session could be used to create RISE framework of each chains.
* * Jerry can use the `@miadi/hooks-interpreter` with his session_id that can be read in `/home/gmusic/.agents/scripts/_env.sh` to create a similar folder as I did for my ava002 (2026-08-16-episode-333-the-fork-arrives-launched-not-handed-over/salix/songbird-71bbe83b).  I would expect that an independent RISE framework of each chains inside of his interpretation correlate semantically and logically a lot with mine which would lead to be ready to create the various 'pi-coding-agent' extensions foreach of the chains and see which one can run directly on the Android device and which one needs server/desktop system.

Jerry's origin session (`session_jerry_origin_id` = `1937aa47-767f-4543-8cdc-257364ae2c52`) was exported on 2026-08-19 to `/home/gmusic/atelier-jerry-origin-1937aa47` — same classified layout as songbird-71bbe83b (interpreter projection, generators, scores, rendered, captures, sessiondata). The motion is now a skill, so the next `session_id` can be dropped the same way without reconstructing the night: `/home/gmusic/.agents/skills/miadi-hooks-interpreter-jamai` (`scripts/export-jamai-session.py --session-id <id> --dest /home/gmusic/<name>`).

## Two halves — this time / next time

The two compositions came from a loop we should not lose, and that loop is not the next machine.

1. **[HOW WE DID IT THIS TIME](HOW-WE-DID-IT-THIS-TIME-260819.md)** — measured 2026-08-19. Claude-code sessions `1937aa47` (Jerry) and `71bbe83b` (William fork) still live in herdr `w17`. Three zero-token bash watches (`jamai-watch`, `ilex-watch`, `abies-watch`) plus `jamai-on-drop`. State in `~/.local/state/episode-voice/`. The phone is a tray. Eury does everything after capture.
2. **[HERE'S HOW WE WANT IT TO WORK NEXT TIME](DRAFT-PI-MONO-EXTENSIONS-260819.md)** — William's eight Pi extensions. Watch / voice / songbird / movement / abc / falsify / return must be able to live on Android. Only `jamai-render` stays desktop. Layout: `extensions/pi/jamai-*` beside `skills/`, shared code in `lib/`, proofs in `tests/`. Issue [Gerico1007/dotagents#32](https://github.com/Gerico1007/dotagents/issues/32).

`scripts/_env.sh` holds the session ids. Do not start from the leftover inline loop in `~/.local/state/ilex-watch/` — that is the model holding `while true`.

## Pi-mono extensions — draft 260819

The eight extensions that replace the Claude-code watch-and-wake loop (voice, Songbird, movement-score) are drafted in [`DRAFT-PI-MONO-EXTENSIONS-260819.md`](DRAFT-PI-MONO-EXTENSIONS-260819.md). Section 1 names each extension. Section 2 proposes `extensions/pi/jamai-*` beside `skills/`, with shared code in `lib/` and proofs in `tests/`. Every extension loads alone with `pi -e`. Only `jamai-render` needs host binaries. William opened [Gerico1007/dotagents#32](https://github.com/Gerico1007/dotagents/issues/32) and assigned it to Gerico1007 for review.

## Questions

### What is into `/home/gmusic/salix/repos/jamai-core` that is not in `/home/gmusic/.agents` this is needed ?  
* If any, it should be published and consumable by any of `/home/gmusic/.agents` and `/home/gmusic/salix/repos/miadi-orchestration-kit` that gets created for any agent type


## Android testing...

* given that `docker run -it termux/termux-docker` exist, there'S surely a sets of tests oand whatever could be conceived and deployed and attempt to make it work without the complicated need to test it on our Android device first...

## RELATED files

### jgwill/miadi-orchestration-kit#39 jgwill/miadi-orchestration-kit#40 jgwill/miadi-orchestration-kit#41 jgwill/miadi-orchestration-kit#42 jgwill/miadi-orchestration-kit#43

* I think they relate to an unfinished claude-code plugin that would orchestrate the experience we had.
* Jerry's agent has forked and created Issues/PR and locally cloned in `/home/gmusic/salix/repos/miadi-orchestration-kit`
* * I would target the /home/gmusic/salix/repos/miadi-orchestration-kit/pi/jamai-extensions as where to create these extensions of the various chains of actions JamAI takes...

### `/home/gmusic/.agents/scripts/_env.sh`
* jgwill/dotagents#27

## `/ep300-seven-fields-research-alignment-renaud-260815-220df92d-1bb2-465b-b07d-4ba103dbd71e/abstract-set-a.md`


