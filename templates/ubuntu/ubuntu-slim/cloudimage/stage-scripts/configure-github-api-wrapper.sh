#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=l
export NEEDRESTART_SUSPEND=1

sudo env DEBIAN_FRONTEND="${DEBIAN_FRONTEND:-}" NEEDRESTART_MODE="${NEEDRESTART_MODE:-}" NEEDRESTART_SUSPEND="${NEEDRESTART_SUSPEND:-}" GH_API_TOKEN="${GH_API_TOKEN:-}" GH_API_MIN_REMAINING="${GH_API_MIN_REMAINING:-}" GH_API_WAIT_BUFFER_SECONDS="${GH_API_WAIT_BUFFER_SECONDS:-}" GITHUB_TOKEN="${GITHUB_TOKEN:-}" SSH_USERNAME="${SSH_USERNAME:-}" HOME=/root bash <<'GHA_STAGE_EOF'
set -euo pipefail
install -m 0755 /tmp/github-api-curl-wrapper.sh /usr/local/bin/curl
printf 'GITHUB_API_MIN_REMAINING=%s\nGITHUB_API_WAIT_BUFFER_SECONDS=%s\n' "$GH_API_MIN_REMAINING" "$GH_API_WAIT_BUFFER_SECONDS" > /etc/github-api-rate-limit.conf
if [ -n "$GH_API_TOKEN" ]; then printf '%s' "$GH_API_TOKEN" > /etc/github-api-token; chmod 644 /etc/github-api-token; fi
GHA_STAGE_EOF
echo "==> Done"
