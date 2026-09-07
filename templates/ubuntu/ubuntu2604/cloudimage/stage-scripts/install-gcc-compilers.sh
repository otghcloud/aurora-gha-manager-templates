#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=l
export NEEDRESTART_SUSPEND=1
export HELPER_SCRIPTS=/imagegeneration/helpers
export INSTALLER_SCRIPT_FOLDER=/imagegeneration/toolsets

echo "==> Running install-gcc-compilers.sh"
sudo -E env HOME=/root bash /imagegeneration/toolsets/install-gcc-compilers.sh
echo "==> Done"
