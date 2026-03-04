# Adaptive Security Agent (VSCodium Project)

This project gives you an adaptive, terminal-capable security assessment agent with:

- Authorized-scope policy checks before command execution
- Command allowlist and blocked-prefix safety controls
- Internet troubleshooting fallback for failed commands
- Long-term conversation recall using SQLite summaries (memory-efficient)
- Strategy adaptation based on historical command success/failure

## Important Use Constraint

Use this only on systems you own or have explicit written permission to test.

## Project Layout

- `agent.py`: main CLI app
- `config.example.json`: starting config
- `.vscode/tasks.json`: one-click run tasks in VSCodium
- `.vscode/launch.json`: debug launch profiles
- `runs/`: generated logs, reports, memory JSON, SQLite archive

## Quick Start

1. Open this folder in VSCodium.
2. Press the Run button.
   It now launches guided mode and asks:
   - website or IP
   - target address
   - dry/live mode
3. Copy the example config:

```bash
cp config.example.json config.json
```

4. Edit `config.json` targets/scope for assets you are authorized to test.
5. Dry-run first:

```bash
python3 agent.py run --config config.json
```

6. Set `"dry_run": false` in `config.json` when ready to execute.
   You can also keep `dry_run: true` and run once with `--live`.

```bash
python3 agent.py run --config config.json --live
```

## Conversation Memory (Low RAM)

The agent stores compact summaries in SQLite instead of loading full transcripts into process memory.

- Import old chat transcript (`.jsonl` or `.txt`):

```bash
python3 agent.py memory-import --config config.json --path old_chat.jsonl --source prior-session
```

- Search historical memory:

```bash
python3 agent.py memory-search --config config.json --query "nmap timeout"
```

- Show memory stats:

```bash
python3 agent.py memory-stats --config config.json
```

## Continuous Mode

```bash
python3 agent.py run --config config.json --continuous
```

Interval is controlled by `continuous_interval_seconds`.

## VSCodium Tasks

Open command palette -> `Tasks: Run Task`:

- `Agent: Dry Run`
- `Agent: Live Run`
- `Agent: Memory Stats`

## Remote Ubuntu From Mac Terminal

Use only your Mac terminal to control an Ubuntu host over SSH.

1. (Optional) Auto-discover and create an SSH alias named `ubuntu`:

```bash
./scripts/setup_ubuntu_alias.sh ubuntu
```

2. Bootstrap Ubuntu (SSH keys, SSH hardening, dependencies, venv, systemd service):

```bash
./scripts/setup_ubuntu_remote.sh ubuntu@<UBUNTU_IP> /home/ubuntu/adaptive-security-agent
```

3. Run agent on Ubuntu on-demand from your Mac terminal:

```bash
./scripts/run_agent_remote.sh ubuntu@<UBUNTU_IP> /home/ubuntu/adaptive-security-agent run
```

4. Check running service:

```bash
ssh ubuntu@<UBUNTU_IP> 'systemctl status adaptive-agent.service --no-pager'
```

## Matrix.org Notifications

The agent can send run updates to your Matrix.org app.

1. Open `config.json` and set:

- `"matrix_enabled": true`
- `"matrix_homeserver": "https://matrix-client.matrix.org"`
- `"matrix_room_id": "!yourRoomId:matrix.org"`
- `"matrix_access_token": "syt_..."`

2. Run the agent normally. It will notify on:

- start
- failed command events
- completion summary

## Full Walkthrough

- `WALKTHROUGH_AUTHORIZED_TESTING.md`
