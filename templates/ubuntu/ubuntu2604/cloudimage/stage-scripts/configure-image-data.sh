#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=l
export NEEDRESTART_SUSPEND=1
export HELPER_SCRIPTS=/imagegeneration/helpers
export IMAGE_VERSION=dev
export IMAGEDATA_FILE=/imagegeneration/imagedata.json

echo "==> Running configure-image-data.sh"
sudo env DEBIAN_FRONTEND="${DEBIAN_FRONTEND:-}" NEEDRESTART_MODE="${NEEDRESTART_MODE:-}" NEEDRESTART_SUSPEND="${NEEDRESTART_SUSPEND:-}" GH_API_TOKEN="${GH_API_TOKEN:-}" GH_API_MIN_REMAINING="${GH_API_MIN_REMAINING:-}" GH_API_WAIT_BUFFER_SECONDS="${GH_API_WAIT_BUFFER_SECONDS:-}" GITHUB_TOKEN="${GITHUB_TOKEN:-}" SSH_USERNAME="${SSH_USERNAME:-}" HELPER_SCRIPTS="${HELPER_SCRIPTS:-}" IMAGE_VERSION="${IMAGE_VERSION:-}" IMAGEDATA_FILE="${IMAGEDATA_FILE:-}" HOME=/root bash /imagegeneration/toolsets/configure-image-data.sh
echo "==> Done"
