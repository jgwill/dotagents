#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  honcho-mcp.sh health
  honcho-mcp.sh tools
  honcho-mcp.sh workspaces [page] [size]
  honcho-mcp.sh peers <workspace-id> [page] [size]
  honcho-mcp.sh sessions <workspace-id> [page] [size]
  honcho-mcp.sh search <query> [workspace-id] [limit]
  honcho-mcp.sh session-context <workspace-id> <session-id> [search-query] [tokens]
  honcho-mcp.sh messages <workspace-id> <session-id> [page] [size]
  honcho-mcp.sh peer-context <workspace-id> <peer-id> [target-peer] [search-query] [top-k]
  honcho-mcp.sh representation <workspace-id> <peer-id> [target-peer] [session-id] [search-query] [max-conclusions]
  honcho-mcp.sh chat <workspace-id> <peer-id> <query> [target-peer] [session-id]
  honcho-mcp.sh call <tool-name> [arguments-json]
  honcho-mcp.sh --allow-mutation call <tool-name> [arguments-json]
EOF
}

die() {
  printf 'honcho-mcp: %s\n' "$*" >&2
  exit 1
}

need_integer() {
  [[ $1 =~ ^[0-9]+$ ]] || die "expected a non-negative integer, got: $1"
}

allow_mutation=false
if [[ ${1:-} == --allow-mutation ]]; then
  allow_mutation=true
  shift
fi

command_name=${1:-}
[[ -n $command_name ]] || { usage >&2; exit 2; }
shift

for dependency in curl jq; do
  command -v "$dependency" >/dev/null 2>&1 || die "required command not found: $dependency"
done
if command -v python3 >/dev/null 2>&1; then
  python_bin=python3
elif command -v python >/dev/null 2>&1; then
  python_bin=python
else
  die 'required command not found: python3 or python'
fi

env_file=${HONCHO_ENV_FILE:-$HOME/.env}
[[ -f $env_file ]] || die "environment file not found: $env_file"
# The credential file is intentionally sourced, never inspected or printed.
# shellcheck disable=SC1090
. "$env_file" >/dev/null
[[ -n ${HONCHO_MCP_BEARER_TOKEN:-} ]] || die 'HONCHO_MCP_BEARER_TOKEN is not set after sourcing the environment file'

mcp_url=${HONCHO_MCP_URL:-https://honcho.tail3b11eb.ts.net/mcp}
protocol_version=${HONCHO_MCP_PROTOCOL_VERSION:-2025-06-18}
tmp_parent=${TMPDIR:-${PREFIX:-/tmp}/tmp}
mkdir -p "$tmp_parent"
tmp_dir=$(mktemp -d "$tmp_parent/honcho-mcp.XXXXXX")
chmod 700 "$tmp_dir"
trap 'rm -rf "$tmp_dir"' EXIT INT TERM

auth_file=$tmp_dir/auth.headers
umask 077
printf 'Authorization: Bearer %s\n' "$HONCHO_MCP_BEARER_TOKEN" > "$auth_file"
unset HONCHO_MCP_BEARER_TOKEN

post_json() {
  local payload_file=$1 output_file=$2 headers_file=$3 session_id=${4:-}
  local -a request=(
    curl -sS --connect-timeout 15 --max-time 90
    -X POST "$mcp_url"
    -H "@$auth_file"
    -H 'Content-Type: application/json'
    -H 'Accept: application/json, text/event-stream'
    -H "MCP-Protocol-Version: $protocol_version"
    -D "$headers_file"
    -o "$output_file"
    -w '%{http_code}'
    --data-binary "@$payload_file"
  )
  if [[ -n $session_id ]]; then
    request+=( -H "Mcp-Session-Id: $session_id" )
  fi

  local status
  status=$("${request[@]}") || die 'HTTP request failed'
  [[ $status =~ ^2[0-9][0-9]$ ]] || {
    printf 'honcho-mcp: HTTP %s\n' "$status" >&2
    "$python_bin" - "$output_file" <<'PY' >&2
from pathlib import Path
import sys
print(Path(sys.argv[1]).read_text(errors="replace")[:2000])
PY
    exit 1
  }
}

extract_response() {
  "$python_bin" - "$1" <<'PY'
import json
import sys
from pathlib import Path

raw = Path(sys.argv[1]).read_text(errors="replace")
messages = []
if raw.lstrip().startswith("{"):
    messages.append(json.loads(raw))
else:
    data_lines = []
    for line in raw.splitlines():
        if line.startswith("data:"):
            data_lines.append(line[5:].lstrip())
    for line in data_lines:
        if line and line != "[DONE]":
            messages.append(json.loads(line))

if not messages:
    raise SystemExit("honcho-mcp: response contained no JSON-RPC message")
message = messages[-1]
if "error" in message:
    print(json.dumps(message["error"], indent=2, ensure_ascii=False), file=sys.stderr)
    raise SystemExit(1)

result = message.get("result", {})
if result.get("isError"):
    print(json.dumps(result, indent=2, ensure_ascii=False), file=sys.stderr)
    raise SystemExit(1)

content = result.get("content")
if isinstance(content, list) and len(content) == 1 and content[0].get("type") == "text":
    text = content[0].get("text", "")
    try:
        print(json.dumps(json.loads(text), indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print(text)
else:
    print(json.dumps(result, indent=2, ensure_ascii=False))
PY
}

readonly_tool() {
  case "$1" in
    honcho_health|list_workspaces|search|chat|get_peer_context|get_representation|list_peers|list_sessions|get_session_context|get_session_messages)
      return 0 ;;
    *) return 1 ;;
  esac
}

tool_name=
arguments='{}'
request_method=tools/call

case "$command_name" in
  tools)
    request_method=tools/list
    ;;
  health)
    tool_name=honcho_health
    ;;
  workspaces)
    page=${1:-1}; size=${2:-50}; need_integer "$page"; need_integer "$size"
    tool_name=list_workspaces
    arguments=$(jq -cn --argjson page "$page" --argjson size "$size" '{page:$page,size:$size}')
    ;;
  peers)
    [[ $# -ge 1 ]] || die 'peers requires <workspace-id>'
    workspace=$1; page=${2:-1}; size=${3:-50}; need_integer "$page"; need_integer "$size"
    tool_name=list_peers
    arguments=$(jq -cn --arg workspace "$workspace" --argjson page "$page" --argjson size "$size" '{workspace_id:$workspace,page:$page,size:$size}')
    ;;
  sessions)
    [[ $# -ge 1 ]] || die 'sessions requires <workspace-id>'
    workspace=$1; page=${2:-1}; size=${3:-50}; need_integer "$page"; need_integer "$size"
    tool_name=list_sessions
    arguments=$(jq -cn --arg workspace "$workspace" --argjson page "$page" --argjson size "$size" '{workspace_id:$workspace,page:$page,size:$size}')
    ;;
  search)
    [[ $# -ge 1 ]] || die 'search requires <query>'
    query=$1; workspace=${2:-}; limit=${3:-10}; need_integer "$limit"
    tool_name=search
    arguments=$(jq -cn --arg query "$query" --arg workspace "$workspace" --argjson limit "$limit" '{query:$query,workspace_id:$workspace,limit:$limit}')
    ;;
  session-context)
    [[ $# -ge 2 ]] || die 'session-context requires <workspace-id> <session-id>'
    workspace=$1; session=$2; search_query=${3:-}; tokens=${4:-0}; need_integer "$tokens"
    tool_name=get_session_context
    arguments=$(jq -cn --arg workspace "$workspace" --arg session "$session" --arg query "$search_query" --argjson tokens "$tokens" '{workspace_id:$workspace,session_id:$session,search_query:$query,tokens:$tokens,summary:true}')
    ;;
  messages)
    [[ $# -ge 2 ]] || die 'messages requires <workspace-id> <session-id>'
    workspace=$1; session=$2; page=${3:-1}; size=${4:-50}; need_integer "$page"; need_integer "$size"
    tool_name=get_session_messages
    arguments=$(jq -cn --arg workspace "$workspace" --arg session "$session" --argjson page "$page" --argjson size "$size" '{workspace_id:$workspace,session_id:$session,page:$page,size:$size}')
    ;;
  peer-context)
    [[ $# -ge 2 ]] || die 'peer-context requires <workspace-id> <peer-id>'
    workspace=$1; peer=$2; target=${3:-}; search_query=${4:-}; top_k=${5:-0}; need_integer "$top_k"
    tool_name=get_peer_context
    arguments=$(jq -cn --arg workspace "$workspace" --arg peer "$peer" --arg target "$target" --arg query "$search_query" --argjson topk "$top_k" '{workspace_id:$workspace,peer_id:$peer,target:$target,search_query:$query,search_top_k:$topk}')
    ;;
  representation)
    [[ $# -ge 2 ]] || die 'representation requires <workspace-id> <peer-id>'
    workspace=$1; peer=$2; target=${3:-}; session=${4:-}; search_query=${5:-}; maximum=${6:-0}; need_integer "$maximum"
    tool_name=get_representation
    arguments=$(jq -cn --arg workspace "$workspace" --arg peer "$peer" --arg target "$target" --arg session "$session" --arg query "$search_query" --argjson maximum "$maximum" '{workspace_id:$workspace,peer_id:$peer,target:$target,session_id:$session,search_query:$query,max_conclusions:$maximum}')
    ;;
  chat)
    [[ $# -ge 3 ]] || die 'chat requires <workspace-id> <peer-id> <query>'
    workspace=$1; peer=$2; query=$3; target=${4:-}; session=${5:-}
    tool_name=chat
    arguments=$(jq -cn --arg workspace "$workspace" --arg peer "$peer" --arg query "$query" --arg target "$target" --arg session "$session" '{workspace_id:$workspace,peer_id:$peer,query:$query,target:$target,session_id:$session}')
    ;;
  call)
    [[ $# -ge 1 ]] || die 'call requires <tool-name>'
    tool_name=$1
    if [[ $# -ge 2 ]]; then arguments=$2; else arguments='{}'; fi
    jq -e 'type == "object"' >/dev/null <<<"$arguments" || die 'arguments-json must be a JSON object'
    if ! readonly_tool "$tool_name" && [[ $allow_mutation != true ]]; then
      die "tool '$tool_name' is not on the read-only allowlist; explicit user authorization and --allow-mutation are required"
    fi
    ;;
  -h|--help|help)
    usage
    exit 0
    ;;
  *)
    usage >&2
    die "unknown command: $command_name"
    ;;
esac

initialize_payload=$tmp_dir/initialize.json
jq -cn --arg protocol "$protocol_version" '{jsonrpc:"2.0",id:1,method:"initialize",params:{protocolVersion:$protocol,capabilities:{},clientInfo:{name:"relational-workspace-honcho",version:"1.0.0"}}}' > "$initialize_payload"
post_json "$initialize_payload" "$tmp_dir/initialize.body" "$tmp_dir/initialize.headers"

session_id=$(awk 'BEGIN{IGNORECASE=1} /^mcp-session-id:/{sub(/\r$/,""); print substr($0,index($0,":")+2)}' "$tmp_dir/initialize.headers" | tail -1)
[[ -n $session_id ]] || die 'server did not return Mcp-Session-Id'

initialized_payload=$tmp_dir/initialized.json
printf '%s\n' '{"jsonrpc":"2.0","method":"notifications/initialized"}' > "$initialized_payload"
post_json "$initialized_payload" "$tmp_dir/initialized.body" "$tmp_dir/initialized.headers" "$session_id"

request_payload=$tmp_dir/request.json
if [[ $request_method == tools/list ]]; then
  jq -cn '{jsonrpc:"2.0",id:2,method:"tools/list",params:{}}' > "$request_payload"
else
  jq -cn --arg name "$tool_name" --argjson arguments "$arguments" '{jsonrpc:"2.0",id:2,method:"tools/call",params:{name:$name,arguments:$arguments}}' > "$request_payload"
fi
post_json "$request_payload" "$tmp_dir/response.body" "$tmp_dir/response.headers" "$session_id"
extract_response "$tmp_dir/response.body"

# Best-effort session cleanup. Authentication stays in the temporary header file.
curl -sS --connect-timeout 5 --max-time 15 -X DELETE "$mcp_url" \
  -H "@$auth_file" -H "Mcp-Session-Id: $session_id" \
  -H "MCP-Protocol-Version: $protocol_version" >/dev/null 2>&1 || true
