export ANTHROPIC_AUTH_TOKEN="ollama"
export ANTHROPIC_API_KEY=""
export ANTHROPIC_BASE_URL="http://localhost:11434"


model=qwen2.5-coder:7b
model=devstral
claude --model $model --strict-mcp-config --bare



