#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <user@ubuntu_ip> <remote_project_dir>"
  echo "Example: $0 ubuntu@192.168.1.50 /home/ubuntu/adaptive-security-agent"
  exit 1
fi

TARGET="$1"
REMOTE_DIR="$2"
LOCAL_PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCAL_PUBKEY="$HOME/.ssh/id_ed25519.pub"

if [[ ! -f "$LOCAL_PUBKEY" ]]; then
  mkdir -p "$HOME/.ssh"
  chmod 700 "$HOME/.ssh"
  ssh-keygen -t ed25519 -N "" -f "$HOME/.ssh/id_ed25519"
fi

chmod 700 "$HOME/.ssh"

echo "[1/6] Copying SSH key to $TARGET"
if ssh -o BatchMode=yes -o ConnectTimeout=5 "$TARGET" "true" >/dev/null 2>&1; then
  echo "SSH key auth already works for $TARGET, skipping ssh-copy-id."
else
  ssh-copy-id -i "$LOCAL_PUBKEY" "$TARGET"
fi

echo "[2/6] Preparing remote Ubuntu packages"
ssh "$TARGET" 'bash -s' <<'REMOTE_CMDS'
set -euo pipefail
sudo apt update
sudo apt install -y openssh-server python3 python3-venv python3-pip nmap dnsutils whois curl openssl rsync
sudo systemctl enable --now ssh
REMOTE_CMDS

echo "[3/6] Hardening SSH (no root login, no password auth)"
ssh "$TARGET" 'bash -s' <<'REMOTE_CMDS'
set -euo pipefail
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%s)
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart ssh
REMOTE_CMDS

echo "[4/6] Syncing project to remote: $REMOTE_DIR"
ssh "$TARGET" "mkdir -p '$REMOTE_DIR'"
rsync -az --delete --exclude '.venv' --exclude '__pycache__' --exclude 'runs' "$LOCAL_PROJECT_DIR/" "$TARGET:$REMOTE_DIR/"

echo "[5/6] Creating Python venv + config"
ssh "$TARGET" "bash -s" <<REMOTE_CMDS
set -euo pipefail
cd "$REMOTE_DIR"
python3 -m venv .venv
source .venv/bin/activate
if [[ ! -f config.json ]]; then
  cp config.example.json config.json
fi
mkdir -p runs
REMOTE_CMDS

echo "[6/6] Installing systemd service for continuous agent"
ssh "$TARGET" "bash -s" <<REMOTE_CMDS
set -euo pipefail
USER_NAME="\$(id -un)"
SERVICE_PATH="/etc/systemd/system/adaptive-agent.service"

sudo tee "\$SERVICE_PATH" >/dev/null <<SERVICE_EOF
[Unit]
Description=Adaptive Security Agent Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=\$USER_NAME
WorkingDirectory=$REMOTE_DIR
ExecStart=$REMOTE_DIR/.venv/bin/python $REMOTE_DIR/agent.py run --config $REMOTE_DIR/config.json --continuous
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
SERVICE_EOF

sudo systemctl daemon-reload
sudo systemctl enable --now adaptive-agent.service
sudo systemctl status adaptive-agent.service --no-pager
REMOTE_CMDS

echo "Setup complete."
echo "Remote checks:"
echo "  ssh $TARGET 'systemctl status ssh --no-pager'"
echo "  ssh $TARGET 'systemctl status adaptive-agent.service --no-pager'"
