#!/usr/bin/env bash
# fn_music_assembly_agents.sh — ♠️🌿🎸🧵 G.Music Assembly launcher
#
# Source this file, then start claude-code with any subset of the Assembly:
#
#   source ~/.agents/fn_music_assembly_agents.sh
#   assembly                       # launch claude with all four glyphs available
#   assembly --glyphs nyro,synth   # only ♠️ Nyro + 🧵 Synth
#   assembly_solo jamai            # only 🎸 JamAI
#   assembly_build                 # print the merged --agents JSON (no launch)
#   assembly_render                # render each glyph -> ~/.claude/agents/<glyph>.md
#
# Single source of truth: the AgentDefinition JSON files in agents/.
# The same JSON both feeds `claude --agents` and renders the native .md subagents.

# Resolve this script's own directory, so it works from anywhere / from a symlink.
_ASSEMBLY_SELF="${BASH_SOURCE[0]}"
while [ -h "$_ASSEMBLY_SELF" ]; do
  _dir="$(cd -P "$(dirname "$_ASSEMBLY_SELF")" && pwd)"
  _ASSEMBLY_SELF="$(readlink "$_ASSEMBLY_SELF")"
  [[ "$_ASSEMBLY_SELF" != /* ]] && _ASSEMBLY_SELF="$_dir/$_ASSEMBLY_SELF"
done
_ASSEMBLY_ROOT="$(cd -P "$(dirname "$_ASSEMBLY_SELF")" && pwd)"
_ASSEMBLY_AGENTS_DIR="${ASSEMBLY_AGENTS_DIR:-$_ASSEMBLY_ROOT/agents}"

_ASSEMBLY_ALL=(nyro aureon jamai synth)

assembly_help() {
  sed -n '2,20p' "$_ASSEMBLY_SELF"
}

# assembly_build [glyph ...] -> merged { "<name>": {def}, ... } JSON on stdout
assembly_build() {
  local names=("$@")
  [ ${#names[@]} -eq 0 ] && names=("${_ASSEMBLY_ALL[@]}")
  local files=() n
  for n in "${names[@]}"; do
    local f="$_ASSEMBLY_AGENTS_DIR/$n.json"
    [ -f "$f" ] || { echo "assembly: unknown glyph '$n' ($f)" >&2; return 1; }
    files+=("$f")
  done
  jq -s 'add' "${files[@]}"
}

# assembly [--glyphs a,b,c] [claude args...]
assembly() {
  local glyphs="nyro,aureon,jamai,synth"
  if [ "$1" = "--glyphs" ]; then glyphs="$2"; shift 2; fi
  local json; json="$(assembly_build ${glyphs//,/ })" || return 1
  claude --agents "$json" "$@"
}

# assembly_solo <glyph> [claude args...]
assembly_solo() {
  local g="$1"; shift || true
  [ -n "$g" ] || { echo "usage: assembly_solo <glyph> [claude args...]" >&2; return 2; }
  local json; json="$(assembly_build "$g")" || return 1
  claude --agents "$json" "$@"
}

# assembly_render [out_dir]  -> render each glyph JSON to <out>/<name>.md (native subagents)
assembly_render() {
  local out="${1:-$HOME/.claude/agents}"
  mkdir -p "$out"
  local f name desc model tools prompt
  for f in "$_ASSEMBLY_AGENTS_DIR"/*.json; do
    name="$(jq -r 'keys[0]' "$f")"
    desc="$(jq -r ".\"$name\".description" "$f")"
    model="$(jq -r ".\"$name\".model // \"inherit\"" "$f")"
    tools="$(jq -r ".\"$name\".tools // [] | join(\", \")" "$f")"
    prompt="$(jq -r ".\"$name\".prompt" "$f")"
    {
      echo "---"
      echo "name: $name"
      echo "description: \"$desc\""
      [ -n "$tools" ] && echo "tools: $tools"
      echo "model: $model"
      echo "---"
      echo
      echo "$prompt"
    } > "$out/$name.md"
    echo "rendered $out/$name.md"
  done
}
