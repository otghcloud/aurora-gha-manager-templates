#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=l
export NEEDRESTART_SUSPEND=1
export IMAGE_VERSION=dev
export IMAGE_OS=ubuntu26
export HELPER_SCRIPTS=/imagegeneration/helpers

echo "==> Running configure-environment.sh"
sudo env DEBIAN_FRONTEND="${DEBIAN_FRONTEND:-}" NEEDRESTART_MODE="${NEEDRESTART_MODE:-}" NEEDRESTART_SUSPEND="${NEEDRESTART_SUSPEND:-}" GH_API_TOKEN="${GH_API_TOKEN:-}" GH_API_MIN_REMAINING="${GH_API_MIN_REMAINING:-}" GH_API_WAIT_BUFFER_SECONDS="${GH_API_WAIT_BUFFER_SECONDS:-}" GITHUB_TOKEN="${GITHUB_TOKEN:-}" SSH_USERNAME="${SSH_USERNAME:-}" IMAGE_VERSION="${IMAGE_VERSION:-}" IMAGE_OS="${IMAGE_OS:-}" HELPER_SCRIPTS="${HELPER_SCRIPTS:-}" HOME=/root bash /imagegeneration/toolsets/configure-environment.sh
echo "==> Done"
