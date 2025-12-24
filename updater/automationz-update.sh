#!/usr/bin/env bash
set -euo pipefail

AUTOMATIONZ_DIR="${AUTOMATIONZ_DIR:-/opt/automationz}"
BRANCH="${AUTOMATIONZ_BRANCH:-main}"
LOG="/var/log/automationz-updater.log"

{
  echo "=== AutomationZ updater: $(date -Is) ==="
  if [[ ! -d "$AUTOMATIONZ_DIR/.git" ]]; then
    echo "ERROR: $AUTOMATIONZ_DIR is not a git repo. Skipping."
    exit 1
  fi

  git -C "$AUTOMATIONZ_DIR" fetch --all
  git -C "$AUTOMATIONZ_DIR" checkout "$BRANCH"
  git -C "$AUTOMATIONZ_DIR" pull --ff-only

  echo "OK: Updated AutomationZ."
} | tee -a "$LOG"
