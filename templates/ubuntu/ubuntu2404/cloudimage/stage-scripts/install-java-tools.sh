#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=l
export NEEDRESTART_SUSPEND=1
export HELPER_SCRIPTS=/imagegeneration/helpers
export INSTALLER_SCRIPT_FOLDER=/imagegeneration/toolsets

echo "==> Running install-java-tools.sh"
sudo env DEBIAN_FRONTEND="${DEBIAN_FRONTEND:-}" NEEDRESTART_MODE="${NEEDRESTART_MODE:-}" NEEDRESTART_SUSPEND="${NEEDRESTART_SUSPEND:-}" GH_API_TOKEN="${GH_API_TOKEN:-}" GH_API_MIN_REMAINING="${GH_API_MIN_REMAINING:-}" GH_API_WAIT_BUFFER_SECONDS="${GH_API_WAIT_BUFFER_SECONDS:-}" SSH_USERNAME="${SSH_USERNAME:-}" HELPER_SCRIPTS="${HELPER_SCRIPTS:-}" INSTALLER_SCRIPT_FOLDER="${INSTALLER_SCRIPT_FOLDER:-}" HOME=/root bash /imagegeneration/toolsets/install-java-tools.sh
echo "==> Done"
