#!/usr/bin/env bash
set -euo pipefail

# Creates/updates ~/.ssh/config host alias "ubuntu" by discovering a reachable SSH target.
# Usage:
#   ./scripts/setup_ubuntu_alias.sh [username]
# Example:
#   ./scripts/setup_ubuntu_alias.sh ubuntu

USER_NAME="${1:-ubuntu}"
SSH_PORT="${UBUNTU_SSH_PORT:-22}"
CONFIG_FILE="$HOME/.ssh/config"
EXTRA_CIDR="${EXTRA_SSH_CIDR:-}"

mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"

if [[ ! -f "$HOME/.ssh/id_ed25519.pub" ]]; then
  ssh-keygen -t ed25519 -N "" -f "$HOME/.ssh/id_ed25519" >/dev/null
fi

scan_ssh_hosts() {
  local cidr="$1"
  python3 - "$cidr" "$SSH_PORT" <<'PY'
import ipaddress, subprocess, sys
net = ipaddress.ip_network(sys.argv[1], strict=False)
port = sys.argv[2]
for host in net.hosts():
    h = str(host)
    p = subprocess.run(['nc','-G','1','-z',h,port], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if p.returncode == 0:
        print(h)
PY
}

ACTIVE_CIDR=""
if ifconfig en0 >/dev/null 2>&1; then
  ACTIVE_CIDR=$(python3 - <<'PY'
import re, ipaddress, subprocess
out = subprocess.check_output(['ifconfig','en0'], text=True)
m = re.search(r'\binet\s+(\d+\.\d+\.\d+\.\d+)\b', out)
if m:
    ip = m.group(1)
    print(ipaddress.ip_network(ip + '/24', strict=False))
PY
)
fi

CANDIDATES=()
if [[ -n "$ACTIVE_CIDR" ]]; then
  while IFS= read -r h; do [[ -n "$h" ]] && CANDIDATES+=("$h"); done < <(scan_ssh_hosts "$ACTIVE_CIDR")
fi
if [[ -n "$EXTRA_CIDR" ]]; then
  while IFS= read -r h; do [[ -n "$h" ]] && CANDIDATES+=("$h"); done < <(scan_ssh_hosts "$EXTRA_CIDR")
fi

UNIQ=()
for h in "${CANDIDATES[@]:-}"; do
  skip=0
  for u in "${UNIQ[@]:-}"; do
    [[ "$u" == "$h" ]] && skip=1 && break
  done
  [[ $skip -eq 0 ]] && UNIQ+=("$h")
done

if [[ ${#UNIQ[@]} -eq 0 ]]; then
  echo "No reachable SSH host found. Start Ubuntu networking + sshd first, then rerun."
  exit 1
fi

TARGET_IP="${UNIQ[0]}"
if [[ ${#UNIQ[@]} -gt 1 ]]; then
  echo "Multiple SSH hosts found: ${UNIQ[*]}"
  echo "Using first candidate: $TARGET_IP"
fi

TMP_FILE=$(mktemp)
if [[ -f "$CONFIG_FILE" ]]; then
  cp "$CONFIG_FILE" "$TMP_FILE"
fi

awk '
BEGIN {skip=0}
/^Host[[:space:]]+ubuntu$/ {skip=1; next}
/^Host[[:space:]]+/ {if (skip==1) {skip=0}}
{if (skip==0) print}
' "$TMP_FILE" > "$TMP_FILE.clean" || true

cat "$TMP_FILE.clean" > "$CONFIG_FILE"
cat >> "$CONFIG_FILE" <<CFG

Host ubuntu
  HostName $TARGET_IP
  User $USER_NAME
  Port $SSH_PORT
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
  ServerAliveInterval 30
  ServerAliveCountMax 6
CFG
chmod 600 "$CONFIG_FILE"

echo "Configured SSH alias: ubuntu -> $USER_NAME@$TARGET_IP:$SSH_PORT"
echo "Next: ssh-copy-id ubuntu && ssh ubuntu"
