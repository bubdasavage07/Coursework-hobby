#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <user@ubuntu_ip> <remote_project_dir> [run|guided-run|memory-stats]"
  echo "Example: $0 ubuntu@192.168.1.50 /home/ubuntu/adaptive-security-agent run"
  exit 1
fi

TARGET="$1"
REMOTE_DIR="$2"
MODE="${3:-run}"

case "$MODE" in
  run)
    REMOTE_CMD="cd '$REMOTE_DIR' && .venv/bin/python agent.py run --config config.json"
    ;;
  guided-run)
    REMOTE_CMD="cd '$REMOTE_DIR' && .venv/bin/python agent.py guided-run --config config.json"
    ;;
  memory-stats)
    REMOTE_CMD="cd '$REMOTE_DIR' && .venv/bin/python agent.py memory-stats --config config.json"
    ;;
  *)
    echo "Unsupported mode: $MODE"
    exit 1
    ;;
esac

ssh "$TARGET" "$REMOTE_CMD"
