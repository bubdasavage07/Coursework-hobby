# Authorized Testing Walkthrough (Website or IP)

This guide is for authorized security testing only (assets you own or have written permission to assess).

## 1. Prereqs

- Mac terminal access
- Ubuntu host reachable by SSH
- Project synced to Ubuntu at `/home/ubuntu/adaptive-security-agent`

## 2. Saved Ubuntu Machine Info

Saved on March 4, 2026:

- VM name: `ubuntu-agent`
- State: `Running`
- IPv4: `192.168.2.4`
- Release: `Ubuntu 24.04.4 LTS`
- SSH user: `ubuntu`
- SSH target: `ubuntu@192.168.2.4`
- Remote project dir: `/home/ubuntu/adaptive-security-agent`

## 3. Every Place You Enter Info (With Examples)

- Ubuntu IP (`UBUNTU_IP`):
  - `192.168.2.4` (current)
  - `192.168.2.15` (example)
- SSH user (`ubuntu` in `ubuntu@IP`):
  - `ubuntu` (default)
  - `ethan` (example custom user)
- Remote project path (`REMOTE_DIR`):
  - `/home/ubuntu/adaptive-security-agent`
  - `/home/ethan/adaptive-security-agent`
- Website target in `config.json`:
  - `example.com`
  - `api.example.com`
- IP target in `config.json`:
  - `192.168.1.50`
  - `10.0.0.25`
- Matrix room ID in `config.json`:
  - `!abcDefGhij12345:matrix.org`
- Matrix access token in `config.json`:
  - `syt_xxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## 4. Set Your Ubuntu Variables (Mac Terminal)

```bash
cd /Users/ethan/CyberSecurity_classes/Random-Shit/ist140/adaptive-security-agent
UBUNTU_IP=192.168.2.4
TARGET="ubuntu@$UBUNTU_IP"
REMOTE_DIR="/home/ubuntu/adaptive-security-agent"
```

If your username is not `ubuntu`:

```bash
TARGET="ethan@$UBUNTU_IP"
REMOTE_DIR="/home/ethan/adaptive-security-agent"
```

## 5. One-Time Ubuntu Bootstrap

```bash
./scripts/setup_ubuntu_remote.sh "$TARGET" "$REMOTE_DIR"
```

This sets up SSH hardening, dependencies, Python venv, and `adaptive-agent.service`.

## 6. Configure Website or IP Scope

```bash
ssh "$TARGET"
cd "$REMOTE_DIR"
nano config.json
```

### Website mode (`config.json`) examples

```json
"targets": ["example.com"],
"scope_patterns": ["example.com", ".example.com"]
```

```json
"targets": ["api.example.com"],
"scope_patterns": ["api.example.com", ".api.example.com"]
```

### IP mode (`config.json`) examples

```json
"targets": ["192.168.1.50"],
"scope_patterns": ["192.168.1.50"]
```

```json
"targets": ["10.0.0.25"],
"scope_patterns": ["10.0.0.25"]
```

## 7. Dry Run First

Set:

```json
"dry_run": true
```

Run:

```bash
./scripts/run_agent_remote.sh "$TARGET" "$REMOTE_DIR" run
```

## 8. Live Run

Set:

```json
"dry_run": false
```

Run:

```bash
./scripts/run_agent_remote.sh "$TARGET" "$REMOTE_DIR" run
```

Or restart service:

```bash
ssh "$TARGET" "sudo systemctl restart adaptive-agent.service"
```

## 9. Guided Mode (Interactive)

```bash
./scripts/run_agent_remote.sh "$TARGET" "$REMOTE_DIR" guided-run
```

Prompt examples:

- Prompt: `Target type [website/ip]:` -> Example answer: `website`
- Prompt: `Website/domain to test:` -> Example answer: `example.com`
- Prompt: `Run mode [dry/live] (default: live):` -> Example answer: `dry`

IP run example:

- `ip`
- `192.168.1.50`
- `live`

## 10. View Results

```bash
ssh "$TARGET" "cat $REMOTE_DIR/runs/report.md"
```

Logs:

```bash
ssh "$TARGET" "tail -n 80 $REMOTE_DIR/runs/session.jsonl"
ssh "$TARGET" "journalctl -u adaptive-agent.service -n 80 --no-pager"
```

## 11. Matrix.org Notifications (Optional)

Set in `config.json`:

```json
"matrix_enabled": true,
"matrix_homeserver": "https://matrix-client.matrix.org",
"matrix_room_id": "!abcDefGhij12345:matrix.org",
"matrix_access_token": "syt_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Restart service:

```bash
ssh "$TARGET" "sudo systemctl restart adaptive-agent.service"
```
