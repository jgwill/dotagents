#!/usr/bin/env bash
# selftest for herdr-fork — exits 0 clean, non-zero on drift.
#
# Tier A  structural, deterministic. Uses the HERDR_FORK_PANES_JSON test seam so
#         pane resolution is tested against a fixture, not against whatever herdr
#         happens to be running. These must always pass.
# Tier B  anchor, live. The two panes measured on eury 2026-08-16 that made this
#         tool trustworthy. If they are gone the tool is untested against reality
#         and this FAILS on purpose. Override with
#         HERDRFORK_SELFTEST_ALLOW_ANCHOR_DRIFT=1 to skip them knowingly.
#
# Nothing here launches, writes to a pane, sends keys, or forks. Every exit code
# is captured directly from the command — never through a pipe, because a
# pipeline's status is the LAST command's, which would silently pass.

set -uo pipefail

BIN="${HERDRFORK_BIN:-$HOME/.local/bin/herdr-fork}"
STATE_DIR="$HOME/.local/state/herdr-fork"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/herdr-fork-selftest.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT

pass=0; fail=0; skip=0

ok()   { pass=$((pass+1)); printf 'PASS  %s\n' "$1"; }
no()   { fail=$((fail+1)); printf 'FAIL  %s\n' "$1"; [ $# -gt 1 ] && printf '      %s\n' "$2"; }
sk()   { skip=$((skip+1)); printf 'SKIP  %s\n' "$1"; }
head_() { printf '\n== %s ==\n' "$1"; }

# expect_rc <want-rc> <name> -- <cmd...>
expect_rc() {
  local want="$1" name="$2"; shift 3
  local out rc
  out="$("$@" 2>&1)"; rc=$?          # rc captured directly, no pipe
  if [ "$rc" -eq "$want" ]; then ok "$name (rc=$rc)"
  else no "$name" "wanted rc=$want got rc=$rc :: $(printf '%s' "$out" | head -2 | tr '\n' ' ')"; fi
}

# expect_grep <needle> <name> -- <cmd...>
expect_grep() {
  local needle="$1" name="$2"; shift 3
  local out rc
  out="$("$@" 2>&1)"; rc=$?
  if [ "$rc" -ne 0 ]; then
    no "$name" "command exited $rc :: $(printf '%s' "$out" | head -2 | tr '\n' ' ')"
  elif printf '%s' "$out" | grep -qF -- "$needle"; then ok "$name"
  else no "$name" "output lacks: $needle"; fi
}

# ------------------------------------------------------------------ tier A --
head_ "Tier A — the tool itself"

if [ -f "$BIN" ]; then ok "exists: $BIN"; else no "exists: $BIN"; fi
if [ -x "$BIN" ]; then ok "executable"; else no "executable"; fi
expect_rc 0 "--help exits 0" -- "$BIN" --help
expect_rc 2 "no argument is a usage error" -- "$BIN"

head_ "Tier A — project dir encoding (measured against 88 real dirs)"
python3 - "$BIN" <<'PY'
import importlib.util, sys
spec = importlib.util.spec_from_loader("hf", None)
src = open(sys.argv[1]).read()
mod = type(sys)("hf"); mod.__dict__["__name__"] = "hf"
exec(compile(src, sys.argv[1], "exec"), mod.__dict__)
cases = {
    "/home/gmusic":                    "-home-gmusic",
    "/home/gmusic/compositions-jamai":  "-home-gmusic-compositions-jamai",
    "/home/gmusic/.agents":             "-home-gmusic--agents",
    "/a/src/_sessiondata":              "-a-src--sessiondata",
}
bad = [(k, v, mod.project_dir_name(k)) for k, v in cases.items()
       if mod.project_dir_name(k) != v]
for k, want, got in bad:
    print(f"FAIL  encode {k} -> {got} (wanted {want})")
for k, v in cases.items():
    if mod.project_dir_name(k) == v:
        print(f"PASS  encode {k} -> {v}")
sys.exit(1 if bad else 0)
PY
if [ $? -eq 0 ]; then pass=$((pass+4)); else fail=$((fail+1)); fi

# ------------------------------------- tier A — pane resolution via fixture --
head_ "Tier A — pane resolution (fixture, deterministic)"
cat > "$TMP/panes.json" <<'JSON'
{"result":{"panes":[
 {"pane_id":"wT:p1","label":"alpha","cwd":"/home/gmusic","agent":"claude"},
 {"pane_id":"wT:p2","label":"alpha-beta","cwd":"/home/gmusic","agent":"claude"},
 {"pane_id":"wT:p3","label":"prefix-alpha-suffix","cwd":"/tmp","agent":"claude"},
 {"pane_id":"wT:p4","label":"lonely-gamma","cwd":"/tmp","agent":"claude"},
 {"pane_id":"wT:p5","cwd":"/tmp"}
]}}
JSON
export HERDR_FORK_PANES_JSON="$TMP/panes.json"

expect_rc 3 "not found -> rc 3" -- "$BIN" no-such-pane-zzz --resolve-only
expect_rc 4 "ambiguous substring 'alpha-' -> rc 4" -- "$BIN" alpha- --resolve-only
expect_grep "wT:p1" "exact label beats 3 substring matches" -- \
  "$BIN" alpha --resolve-only
expect_grep "matched by exact pane_id" "exact pane id wins" -- \
  "$BIN" wT:p3 --resolve-only
expect_grep "wT:p4" "unique substring resolves" -- "$BIN" gamma --resolve-only

# ambiguity must PRINT the candidates, not pick one
out="$("$BIN" alpha- --resolve-only 2>&1)"; rc=$?
if [ "$rc" -eq 4 ] && printf '%s' "$out" | grep -qF "wT:p2" \
   && printf '%s' "$out" | grep -qF "wT:p3"; then
  ok "ambiguity lists every candidate"
else
  no "ambiguity lists every candidate" "rc=$rc"
fi
unset HERDR_FORK_PANES_JSON

expect_rc 2 "--workspace + --new-workspace rejected" -- \
  "$BIN" wT:p1 --workspace w1 --new-workspace
expect_rc 2 "malformed --session-id rejected" -- \
  "$BIN" wT:p1 --session-id not-a-uuid

# ------------------------------------------------------------------ tier B --
head_ "Tier B — live anchors measured on eury 2026-08-16"

ANCHOR1_PANE="${HERDRFORK_ANCHOR1_PANE:-w17:p6}"
ANCHOR1_SESSION="${HERDRFORK_ANCHOR1_SESSION:-1937aa47-767f-4543-8cdc-257364ae2c52}"
ANCHOR1_CWD="${HERDRFORK_ANCHOR1_CWD:-/home/gmusic}"
ANCHOR2_PANE="${HERDRFORK_ANCHOR2_PANE:-w17:p8}"
ANCHOR2_SESSION="${HERDRFORK_ANCHOR2_SESSION:-71bbe83b-8963-4635-b8a2-40bcffbb3aff}"
ANCHOR2_CWD="${HERDRFORK_ANCHOR2_CWD:-/home/gmusic/compositions-jamai}"

anchor() {  # anchor <pane> <session> <cwd> <why-it-matters>
  local pane="$1" sess="$2" cwd="$3" why="$4" out rc
  out="$("$BIN" "$pane" --dry-run 2>&1)"; rc=$?
  if [ "$rc" -ne 0 ]; then
    if [ "${HERDRFORK_SELFTEST_ALLOW_ANCHOR_DRIFT:-0}" = "1" ]; then
      sk "anchor $pane gone ($why) — drift allowed by env"
    else
      no "anchor $pane ($why)" \
         "dry-run rc=$rc :: $(printf '%s' "$out" | head -2 | tr '\n' ' ')"
    fi
    return
  fi
  if printf '%s' "$out" | grep -qF "origin session         $sess"; then
    ok "anchor $pane resolves $sess ($why)"
  else
    no "anchor $pane session" \
       "$(printf '%s' "$out" | grep -F 'origin session' | head -1)"
  fi
  if printf '%s' "$out" | grep -qF "launch cwd             $cwd"; then
    ok "anchor $pane launch cwd $cwd"
  else
    no "anchor $pane launch cwd" \
       "$(printf '%s' "$out" | grep -F 'launch cwd' | head -1)"
  fi
  if printf '%s' "$out" | grep -qF "CORROBORATION ONLY"; then
    ok "anchor $pane names newest-jsonl as corroboration only"
  else
    no "anchor $pane corroboration labelling"
  fi
}

anchor "$ANCHOR1_PANE" "$ANCHOR1_SESSION" "$ANCHOR1_CWD" \
       "bare claude — argv silent, descendant env is the only signal"
anchor "$ANCHOR2_PANE" "$ANCHOR2_SESSION" "$ANCHOR2_CWD" \
       "explicit flags — argv and env must agree"

# the pair must differ in project dir but share lineage
o1="$("$BIN" "$ANCHOR1_PANE" --dry-run 2>&1)"; r1=$?
o2="$("$BIN" "$ANCHOR2_PANE" --dry-run 2>&1)"; r2=$?
if [ "$r1" -eq 0 ] && [ "$r2" -eq 0 ]; then
  d1="$(printf '%s' "$o1" | grep -F 'fork project dir' | head -1)"
  d2="$(printf '%s' "$o2" | grep -F 'fork project dir' | head -1)"
  if [ "$d1" != "$d2" ]; then ok "parent/child pair land in different project dirs"
  else no "parent/child pair project dirs" "both: $d1"; fi
  if printf '%s' "$o2" | grep -qF "origin ancestry        $ANCHOR1_SESSION"; then
    ok "child reports its ancestry: forked from $ANCHOR1_SESSION"
  else
    no "child lineage" \
       "$(printf '%s' "$o2" | grep -F 'origin ancestry' | head -1)"
  fi
  if printf '%s' "$o1" | grep -qF "origin ancestry        none in argv"; then
    ok "parent reports itself as a root session"
  else
    no "parent ancestry" \
       "$(printf '%s' "$o1" | grep -F 'origin ancestry' | head -1)"
  fi
elif [ "${HERDRFORK_SELFTEST_ALLOW_ANCHOR_DRIFT:-0}" = "1" ]; then
  sk "parent/child pair checks — drift allowed by env"
else
  no "parent/child pair checks" "rc1=$r1 rc2=$r2"
fi

# ---------------------------------------------------- tier B — side effects --
head_ "Tier B — --dry-run writes nothing"
before="$(ls -1 "$STATE_DIR" 2>/dev/null | sort)"
"$BIN" "$ANCHOR1_PANE" --dry-run >/dev/null 2>&1; rc=$?
after="$(ls -1 "$STATE_DIR" 2>/dev/null | sort)"
if [ "$before" = "$after" ]; then ok "--dry-run left $STATE_DIR untouched"
else no "--dry-run wrote files" "$(diff <(printf '%s' "$before") <(printf '%s' "$after") | tr '\n' ' ')"; fi

head_ "Tier B — no credential ever reaches stdout or the generated script"
# A dry-run that dumps the environment is a credential leak with a friendly
# name. Compare the tool's FULL output against the live secret's real value.
secret="$(bash --noprofile --norc -c \
  '. /opt/binscripts/load.sh >/dev/null 2>&1; printf %s "${HONCHO_MCP_BEARER_TOKEN:-}"')"
if [ -z "$secret" ]; then
  no "leak check" "HONCHO_MCP_BEARER_TOKEN did not load — cannot test for a leak"
else
  leak=0
  for pane in "$ANCHOR1_PANE" "$ANCHOR2_PANE"; do
    o="$("$BIN" "$pane" --dry-run 2>&1)"; r=$?
    [ "$r" -ne 0 ] && continue
    printf '%s' "$o" | grep -qF -- "$secret" && leak=1
  done
  if [ "$leak" -eq 0 ]; then
    ok "no HONCHO_MCP_BEARER_TOKEN value in any --dry-run output"
  else
    no "CREDENTIAL LEAK" "the token value appears in --dry-run output"
  fi
  o="$("$BIN" "$ANCHOR2_PANE" --dry-run 2>&1)"
  if printf '%s' "$o" | grep -qF 'HONCHO_MCP_BEARER_TOKEN:?unset after sourcing'; then
    ok "generated script asserts the token by NAME, not by value"
  else
    sk "token name-assertion (anchor 2 has no honcho mcp-config)"
  fi
fi

head_ "Tier B — load.sh is necessary AND sufficient (measured, not inherited)"
o="$(env -i HOME="$HOME" PATH=/usr/bin:/bin bash --noprofile --norc -c \
  '. /opt/binscripts/load.sh >/dev/null 2>&1
   printf "%s|%s|%s" "${MWCV:-MISSING}" "${MIADI_CHRONICLE_MW_URL:-MISSING}" \
     "${HONCHO_MCP_BEARER_TOKEN:+SET}"')"; rc=$?
case "$o" in
  MISSING*|*\|MISSING\|*|*\|) no "load.sh supplies all three" "got: $o (rc=$rc)" ;;
  *) ok "load.sh alone supplies MWCV / MIADI_CHRONICLE_MW_URL / token: $o" ;;
esac
o="$(env -i HOME="$HOME" PATH=/usr/bin:/bin bash -lc \
  'printf "%s" "${MWCV:-MISSING}"')"
if [ "$o" = "MISSING" ]; then
  ok "a login shell alone supplies NOTHING — #!/bin/bash -l is not a shortcut"
else
  no "login-shell premise" "bash -lc gave MWCV=$o; the preamble rationale drifted"
fi
o="$(env -i HOME="$HOME" PATH=/usr/bin:/bin bash --noprofile --norc -c \
  '. /opt/binscripts/load.sh >/dev/null 2>&1; printf "%s" "${MIADI_CHRONICLE_MW_URL:-}"')"
if [ "$o" = "http://127.0.0.1:8040" ]; then
  ok "chronicle wheel is the ilex tunnel $o"
else
  no "chronicle wheel drift" \
     "MIADI_CHRONICLE_MW_URL=$o (expected http://127.0.0.1:8040; the gaia wheel \
mw.tail3b11eb.ts.net has been OFFLINE since 2026-07-29)"
fi

head_ "Tier B — the generated script survives a hostile shell"
# Regression: an early preamble sourced load.sh under `set -e` with stderr
# redirected. load.sh aborts partway with -e active, so the script died with
# exit 1 and NOT ONE WORD printed — the silent-degrade failure this tool exists
# to prevent, reproduced inside the tool itself. CLAUDE_BIN is swapped for
# /bin/true so nothing launches; only the preamble and guards are exercised.
gen="$("$BIN" "$ANCHOR2_PANE" --no-launch --label selftest-scratch 2>&1)"; rc=$?
if [ "$rc" -ne 0 ]; then
  no "generate script for hostile-shell test" "rc=$rc"
else
  script="$(printf '%s\n' "$gen" | grep -F 'wrote ' | awk '{print $2}')"
  if [ ! -x "$script" ]; then
    no "generated script is executable" "$script"
  else
    ok "generated script is executable ($(basename "$script"))"
    env -i CLAUDE_BIN=/bin/true HOME="$HOME" "$script" >/dev/null 2>&1; rc=$?
    if [ "$rc" -eq 0 ]; then ok "runs clean under env -i with no PATH, no profile"
    else no "env -i run" "rc=$rc — preamble or a \${VAR:?} guard failed"; fi
    CLAUDE_BIN=/bin/true sh -c "$script" >/dev/null 2>&1; rc=$?
    if [ "$rc" -eq 0 ]; then ok "runs clean under bare sh -c"
    else no "sh -c run" "rc=$rc"; fi
    if head -1 "$script" | grep -q '^#!'; then ok "has a shebang"
    else no "has a shebang"; fi
    # comments are stripped first: the header legitimately NAMES the alias trap
    # in prose. What must be alias-free is the executable body.
    if grep -v '^[[:space:]]*#' "$script" | grep -q 'claudeyolo'; then
      no "script body is alias-free" "an executable line invokes an alias"
    else ok "script body names no alias — plain claude, explicit flags"; fi
    if grep -v '^[[:space:]]*#' "$script" | grep -q 'exec "\$CLAUDE_BIN"'; then
      ok "script execs a resolved absolute claude binary"
    else no "script execs a resolved binary"; fi
    if grep -qF "cd '" "$script"; then ok "script cds explicitly"
    else no "script cds explicitly"; fi
    rm -f "$script"
  fi
fi

head_ "Tier B — the alias failure mode this tool exists to prevent"
env -i sh -c 'miaclaudeyolo --version' >/dev/null 2>&1; rc=$?
if [ "$rc" -eq 127 ]; then
  ok "miaclaudeyolo is unavailable to a non-interactive shell (rc=127) — proves \
the generated script must emit plain claude"
else
  no "alias premise" "expected rc=127 from env -i sh -c miaclaudeyolo, got $rc"
fi

# ------------------------------------------------------------------ verdict --
printf '\n== verdict ==\npass=%d fail=%d skip=%d\n' "$pass" "$fail" "$skip"
[ "$fail" -eq 0 ] || exit 1
exit 0
