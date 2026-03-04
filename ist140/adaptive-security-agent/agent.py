#!/usr/bin/env python3
"""
Adaptive Security Assessment Agent

Purpose:
- Run authorized, scoped security assessment commands from a configurable playbook.
- Learn strategy effectiveness over time and prioritize commands that work.
- Use internet troubleshooting plus archived conversation recall when runs fail.

This tool is intentionally scoped for defensive, authorized testing only.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import shlex
import sqlite3
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple
from urllib.parse import quote, urlencode, urlparse
from urllib.request import Request, urlopen


RISKY_TOKENS = [";", "&&", "||", "|", "`", "$("]
DEFAULT_BLOCKED_PREFIXES = [
    "rm ",
    "shutdown",
    "reboot",
    "mkfs",
    "dd ",
    "iptables",
    "route ",
]
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*$"
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_text(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def summarize_text(text: str, max_chars: int) -> str:
    compact = " ".join(text.split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3].rstrip() + "..."


def extract_keywords(text: str, max_keywords: int = 8) -> List[str]:
    words = [w for w in normalize_text(text).split() if len(w) >= 3]
    deduped: List[str] = []
    seen = set()
    for word in words:
        if word in seen:
            continue
        seen.add(word)
        deduped.append(word)
        if len(deduped) >= max_keywords:
            break
    return deduped


def is_valid_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def normalize_website_target(raw_value: str) -> str:
    text = raw_value.strip()
    if "://" not in text:
        text = f"https://{text}"
    parsed = urlparse(text)
    hostname = (parsed.hostname or "").strip().rstrip(".").lower()
    return hostname


def is_valid_hostname(value: str) -> bool:
    if value == "localhost":
        return True
    return bool(HOSTNAME_RE.fullmatch(value))


def prompt_user(prompt: str) -> str:
    return input(prompt).strip()


def collect_interactive_target() -> Tuple[str, str, List[str]]:
    while True:
        target_type = prompt_user("Target type [website/ip]: ").lower()
        if target_type in {"website", "web", "domain"}:
            while True:
                raw_value = prompt_user("Website/domain to test: ")
                target = normalize_website_target(raw_value)
                if not target:
                    print("Please enter a website/domain.")
                    continue
                if not is_valid_hostname(target):
                    print("Invalid website/domain format. Try again.")
                    continue
                scope_patterns = [target, f".{target}"]
                return "website", target, scope_patterns
        if target_type in {"ip", "address"}:
            while True:
                target = prompt_user("IP address to test: ")
                if not is_valid_ip(target):
                    print("Invalid IP format. Try again.")
                    continue
                scope_patterns = [target]
                return "ip", target, scope_patterns
        print("Please enter 'website' or 'ip'.")


@dataclass
class CommandResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration_seconds: float

    @property
    def success(self) -> bool:
        return self.exit_code == 0


class ConversationArchive:
    """
    Memory-efficient long-term conversation store.

    Stores compact summaries in SQLite and retrieves only relevant rows by keyword,
    avoiding loading full historical transcripts into memory.
    """

    def __init__(self, db_path: Path, summary_chars: int = 320) -> None:
        self.db_path = db_path
        self.summary_chars = summary_chars
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS conversation_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts TEXT NOT NULL,
                    source TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    search_blob TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_conversation_memory_ts
                    ON conversation_memory(ts);
                CREATE INDEX IF NOT EXISTS idx_conversation_memory_source
                    ON conversation_memory(source);
                """
            )

    def add_message(self, role: str, content: str, source: str = "runtime") -> None:
        content = content.strip()
        if not content:
            return

        summary = summarize_text(content, self.summary_chars)
        keywords = extract_keywords(content)
        search_blob = " ".join(sorted(set(keywords + extract_keywords(summary))))

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO conversation_memory (ts, source, role, content, summary, search_blob)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (utc_now_iso(), source, role, content, summary, search_blob),
            )

    def import_jsonl(self, path: Path, source: str = "import") -> int:
        imported = 0
        with path.open("r", encoding="utf-8") as handle:
            for raw in handle:
                line = raw.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    self.add_message(role="unknown", content=line, source=source)
                    imported += 1
                    continue

                role = str(payload.get("role", "unknown"))
                content = str(
                    payload.get("content")
                    or payload.get("message")
                    or payload.get("text")
                    or ""
                )
                if content:
                    self.add_message(role=role, content=content, source=source)
                    imported += 1
        return imported

    def import_text(self, path: Path, source: str = "import") -> int:
        imported = 0
        with path.open("r", encoding="utf-8") as handle:
            for raw in handle:
                line = raw.strip()
                if not line:
                    continue
                role = "unknown"
                content = line
                lowered = line.lower()
                if lowered.startswith("user:"):
                    role = "user"
                    content = line[5:].strip()
                elif lowered.startswith("assistant:"):
                    role = "assistant"
                    content = line[10:].strip()
                self.add_message(role=role, content=content, source=source)
                imported += 1
        return imported

    def search(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        keywords = extract_keywords(query)
        with self._connect() as conn:
            if not keywords:
                rows = conn.execute(
                    """
                    SELECT ts, role, summary, source
                    FROM conversation_memory
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
            else:
                clauses = ["search_blob LIKE ?" for _ in keywords]
                sql = (
                    "SELECT ts, role, summary, source "
                    "FROM conversation_memory "
                    f"WHERE {' OR '.join(clauses)} "
                    "ORDER BY id DESC LIMIT ?"
                )
                params: List[str | int] = [f"%{k}%" for k in keywords] + [limit]
                rows = conn.execute(sql, params).fetchall()

        return [
            {
                "ts": str(row["ts"]),
                "role": str(row["role"]),
                "summary": str(row["summary"]),
                "source": str(row["source"]),
            }
            for row in rows
        ]

    def count(self) -> int:
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS c FROM conversation_memory").fetchone()
            return int(row["c"])


class SafetyPolicy:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.scope_patterns = [p.strip() for p in config.get("scope_patterns", []) if p.strip()]
        self.allowlist = set(config.get("command_allowlist", []))
        self.network_tools = set(config.get("network_tools_require_scope", []))
        blocked = config.get("blocked_command_prefixes", DEFAULT_BLOCKED_PREFIXES)
        self.blocked_prefixes = tuple(blocked)

    def _contains_scope(self, command: str) -> bool:
        return any(pattern in command for pattern in self.scope_patterns)

    def validate_command(self, command: str) -> Tuple[bool, str]:
        if any(token in command for token in RISKY_TOKENS):
            return False, "Blocked shell control token detected"

        try:
            parts = shlex.split(command)
        except ValueError as exc:
            return False, f"Invalid command format: {exc}"

        if not parts:
            return False, "Empty command"

        tool = parts[0]
        if self.allowlist and tool not in self.allowlist:
            return False, f"Tool '{tool}' is not in command_allowlist"

        if self.blocked_prefixes and command.startswith(self.blocked_prefixes):
            return False, "Command matches blocked prefix"

        if tool in self.network_tools and not self._contains_scope(command):
            return False, "Network command must include an in-scope target/pattern"

        return True, "ok"


class TerminalExecutor:
    def __init__(self, timeout_seconds: int) -> None:
        self.timeout_seconds = timeout_seconds

    def run(self, command: str) -> CommandResult:
        start = time.time()
        parts = shlex.split(command)
        try:
            proc = subprocess.run(
                parts,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
            )
            return CommandResult(
                command=command,
                exit_code=proc.returncode,
                stdout=proc.stdout.strip(),
                stderr=proc.stderr.strip(),
                duration_seconds=round(time.time() - start, 3),
            )
        except subprocess.TimeoutExpired:
            return CommandResult(
                command=command,
                exit_code=124,
                stdout="",
                stderr=f"Timeout after {self.timeout_seconds}s",
                duration_seconds=round(time.time() - start, 3),
            )
        except FileNotFoundError:
            return CommandResult(
                command=command,
                exit_code=127,
                stdout="",
                stderr="Command not found",
                duration_seconds=round(time.time() - start, 3),
            )


class WebResearcher:
    """Uses DuckDuckGo Instant Answer API for quick troubleshooting context."""

    ENDPOINT = "https://api.duckduckgo.com/"

    def __init__(self, max_results: int = 5, timeout_seconds: int = 20) -> None:
        self.max_results = max_results
        self.timeout_seconds = timeout_seconds

    def search(self, query: str) -> List[Dict[str, str]]:
        params = {
            "q": query,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1",
            "no_redirect": "1",
        }
        url = f"{self.ENDPOINT}?{urlencode(params)}"
        req = Request(url, headers={"User-Agent": "AdaptiveSecurityAgent/1.0"})
        results: List[Dict[str, str]] = []

        try:
            with urlopen(req, timeout=self.timeout_seconds) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="replace"))
        except Exception:
            return results

        abstract_text = data.get("AbstractText", "").strip()
        abstract_url = data.get("AbstractURL", "").strip()
        if abstract_text and abstract_url:
            results.append({"title": abstract_text[:220], "url": abstract_url})

        for item in data.get("RelatedTopics", []):
            if isinstance(item, dict) and "Text" in item and "FirstURL" in item:
                results.append({"title": item["Text"][:220], "url": item["FirstURL"]})
            elif isinstance(item, dict) and "Topics" in item:
                for nested in item.get("Topics", []):
                    if "Text" in nested and "FirstURL" in nested:
                        results.append({"title": nested["Text"][:220], "url": nested["FirstURL"]})

            if len(results) >= self.max_results:
                break

        return results[: self.max_results]


class MatrixNotifier:
    """Optional Matrix.org/Matrix homeserver notifier for run events."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.enabled = bool(config.get("matrix_enabled", False))
        self.homeserver = str(
            config.get("matrix_homeserver", "https://matrix-client.matrix.org")
        ).rstrip("/")
        self.room_id = str(config.get("matrix_room_id", "")).strip()
        self.access_token = str(config.get("matrix_access_token", "")).strip()
        self.timeout_seconds = int(config.get("matrix_timeout_seconds", 15))
        self.last_error = ""

    def can_send(self) -> bool:
        return self.enabled and bool(self.homeserver and self.room_id and self.access_token)

    def send(self, message: str) -> bool:
        if not self.can_send():
            return False

        room_encoded = quote(self.room_id, safe="")
        txn_id = str(int(time.time() * 1000))
        url = (
            f"{self.homeserver}/_matrix/client/v3/rooms/"
            f"{room_encoded}/send/m.room.message/{txn_id}"
        )
        payload = {"msgtype": "m.text", "body": message}
        req = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            method="PUT",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "User-Agent": "AdaptiveSecurityAgent/1.0",
            },
        )

        try:
            with urlopen(req, timeout=self.timeout_seconds):
                return True
        except Exception as exc:
            self.last_error = str(exc)
            return False


class AdaptiveMemory:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.state = {"tool_scores": {}, "attempts": [], "updated_at": None}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            self.state = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.state["updated_at"] = utc_now_iso()
        self.path.write_text(json.dumps(self.state, indent=2), encoding="utf-8")

    def score_for(self, command: str) -> float:
        try:
            tool = shlex.split(command)[0]
        except Exception:
            return 1.0
        return float(self.state["tool_scores"].get(tool, 1.0))

    def rank(self, commands: List[str]) -> List[str]:
        return sorted(commands, key=self.score_for, reverse=True)

    def update(self, result: CommandResult) -> None:
        tool = shlex.split(result.command)[0]
        current = float(self.state["tool_scores"].get(tool, 1.0))
        delta = 0.25 if result.success else -0.20
        self.state["tool_scores"][tool] = round(max(0.1, current + delta), 3)
        self.state["attempts"].append(
            {
                "ts": utc_now_iso(),
                "command": result.command,
                "success": result.success,
                "exit_code": result.exit_code,
                "stderr_sample": result.stderr[:200],
            }
        )
        if len(self.state["attempts"]) > 500:
            self.state["attempts"] = self.state["attempts"][-500:]


class Planner:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.targets = config.get("targets", [])
        self.templates = config.get(
            "command_templates",
            [
                "dig {target} +short",
                "nslookup {target}",
                "curl -sSIk https://{target}",
                "openssl s_client -connect {target}:443 -brief",
                "nmap -Pn -sV --top-ports 100 {target}",
            ],
        )

    def build_command_queue(self) -> List[str]:
        commands: List[str] = []
        for target in self.targets:
            for template in self.templates:
                commands.append(template.format(target=target))
        return commands


class Agent:
    def __init__(self, config: Dict[str, Any], config_path: Path) -> None:
        self.config = config
        self.config_path = config_path
        self.base_dir = config_path.parent

        self.policy = SafetyPolicy(config)
        self.executor = TerminalExecutor(timeout_seconds=int(config.get("timeout_seconds", 120)))
        self.web = WebResearcher(max_results=int(config.get("web_results_limit", 5)))
        self.matrix = MatrixNotifier(config)
        self.memory = AdaptiveMemory(self._resolve_path(config.get("memory_path", "runs/memory.json")))
        self.planner = Planner(config)

        self.log_path = self._resolve_path(config.get("log_path", "runs/session.jsonl"))
        self.report_path = self._resolve_path(config.get("report_path", "runs/report.md"))
        archive_db = self._resolve_path(
            config.get("conversation_db_path", "runs/conversation_archive.sqlite3")
        )
        self.archive = ConversationArchive(
            db_path=archive_db,
            summary_chars=int(config.get("conversation_summary_chars", 320)),
        )

        self.max_iterations = int(config.get("max_iterations", 20))
        self.dry_run = bool(config.get("dry_run", True))
        self.auto_web_research = bool(config.get("auto_web_research", True))
        self.archive_search_limit = int(config.get("archive_search_limit", 5))
        self.matrix_notify_start = bool(config.get("matrix_notify_start", True))
        self.matrix_notify_failures = bool(config.get("matrix_notify_failures", True))
        self.matrix_notify_finish = bool(config.get("matrix_notify_finish", True))

    def _resolve_path(self, path_like: str) -> Path:
        path = Path(path_like)
        return path if path.is_absolute() else self.base_dir / path

    def _write_log(self, event: Dict[str, Any]) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event) + "\n")

    def _notify_matrix(self, message: str) -> None:
        if not self.matrix.can_send():
            return
        sent = self.matrix.send(message)
        if not sent and self.matrix.last_error:
            self._write_log(
                {
                    "ts": utc_now_iso(),
                    "event": "matrix_notify_error",
                    "error": self.matrix.last_error,
                }
            )

    def import_conversation_file(self, path: Path, source: str = "import") -> int:
        if path.suffix.lower() == ".jsonl":
            return self.archive.import_jsonl(path=path, source=source)
        return self.archive.import_text(path=path, source=source)

    def _research_from_failure(self, result: CommandResult) -> Dict[str, List[Dict[str, str]]]:
        output: Dict[str, List[Dict[str, str]]] = {"archive": [], "web": []}

        if not result.stderr:
            return output

        first_line = result.stderr.splitlines()[0].strip()
        query = f"{shlex.split(result.command)[0]} error {first_line}"

        output["archive"] = self.archive.search(query=query, limit=self.archive_search_limit)
        output["web"] = self.web.search(query=query)
        return output

    def _build_report(
        self,
        all_results: List[CommandResult],
        tips: Dict[str, Dict[str, List[Dict[str, str]]]],
    ) -> None:
        self.report_path.parent.mkdir(parents=True, exist_ok=True)
        lines: List[str] = []
        lines.append("# Adaptive Security Agent Report")
        lines.append("")
        lines.append(f"- Agent: `{self.config.get('agent_name', 'adaptive-security-agent')}`")
        lines.append(f"- Objective: {self.config.get('objective', 'Not provided')}")
        lines.append(f"- Generated: {utc_now_iso()}")
        lines.append(f"- Conversation archive rows: {self.archive.count()}")
        lines.append("")

        success_count = sum(1 for result in all_results if result.success)
        lines.append("## Execution Summary")
        lines.append("")
        lines.append(f"- Total commands: {len(all_results)}")
        lines.append(f"- Successful: {success_count}")
        lines.append(f"- Failed: {len(all_results) - success_count}")
        lines.append("")

        lines.append("## Command Outcomes")
        lines.append("")
        for result in all_results:
            status = "OK" if result.success else f"FAIL ({result.exit_code})"
            lines.append(f"### `{result.command}`")
            lines.append(f"- Status: {status}")
            lines.append(f"- Duration: {result.duration_seconds}s")
            if result.stdout:
                lines.append(f"- Stdout sample: `{result.stdout[:220].replace('`', "'")}`")
            if result.stderr:
                lines.append(f"- Stderr sample: `{result.stderr[:220].replace('`', "'")}`")

            if result.command in tips:
                command_tips = tips[result.command]
                if command_tips.get("archive"):
                    lines.append("- Related historical memory:")
                    for item in command_tips["archive"]:
                        lines.append(
                            "  - "
                            + f"[{item['source']}] {item['ts']} {item['role']}: {item['summary']}"
                        )
                if command_tips.get("web"):
                    lines.append("- Web troubleshooting links:")
                    for item in command_tips["web"]:
                        lines.append(f"  - {item['title']} -> {item['url']}")
            lines.append("")

        lines.append("## Next Actions")
        lines.append("")
        lines.append("- Review failed commands and install missing tools if needed.")
        lines.append("- Tighten `scope_patterns` so all network operations stay authorized.")
        lines.append("- Keep importing old chat logs to improve historical recall quality.")
        lines.append("")

        self.report_path.write_text("\n".join(lines), encoding="utf-8")

    def run_once(self) -> None:
        run_started = utc_now_iso()
        self.archive.add_message(
            role="system",
            content=f"Run objective: {self.config.get('objective', '')}",
            source="runtime",
        )

        queue = self.planner.build_command_queue()
        queue = self.memory.rank(queue)
        queue = queue[: self.max_iterations]

        if self.matrix_notify_start:
            mode = "dry-run" if self.dry_run else "live"
            targets = ", ".join(self.config.get("targets", []))
            self._notify_matrix(
                f"[Adaptive Agent] Run started ({mode}) at {run_started}\n"
                f"Objective: {self.config.get('objective', '')}\n"
                f"Targets: {targets}\n"
                f"Max iterations: {self.max_iterations}"
            )

        all_results: List[CommandResult] = []
        tips: Dict[str, Dict[str, List[Dict[str, str]]]] = {}
        skipped = 0

        for command in queue:
            allowed, reason = self.policy.validate_command(command)
            if not allowed:
                skipped += 1
                self._write_log(
                    {
                        "ts": utc_now_iso(),
                        "command": command,
                        "skipped": True,
                        "reason": reason,
                    }
                )
                self.archive.add_message(
                    role="system",
                    content=f"Skipped command `{command}` because: {reason}",
                    source="runtime",
                )
                continue

            if self.dry_run:
                skipped += 1
                self._write_log(
                    {
                        "ts": utc_now_iso(),
                        "command": command,
                        "dry_run": True,
                        "note": "Skipped execution because dry_run=true",
                    }
                )
                continue

            result = self.executor.run(command)
            all_results.append(result)
            self.memory.update(result)

            self._write_log(
                {
                    "ts": utc_now_iso(),
                    "command": result.command,
                    "exit_code": result.exit_code,
                    "success": result.success,
                    "duration_seconds": result.duration_seconds,
                    "stdout_sample": result.stdout[:500],
                    "stderr_sample": result.stderr[:500],
                }
            )

            summary = (
                f"Command `{result.command}` exit={result.exit_code}. "
                f"stdout={summarize_text(result.stdout, 160)} "
                f"stderr={summarize_text(result.stderr, 160)}"
            )
            self.archive.add_message(role="assistant", content=summary, source="runtime")

            if not result.success and self.auto_web_research:
                result_tips = self._research_from_failure(result)
                tips[result.command] = result_tips
                if result_tips.get("archive") or result_tips.get("web"):
                    self._write_log(
                        {
                            "ts": utc_now_iso(),
                            "command": result.command,
                            "research": result_tips,
                        }
                    )
                if self.matrix_notify_failures:
                    self._notify_matrix(
                        f"[Adaptive Agent] Command failed: {result.command}\n"
                        f"Exit: {result.exit_code}\n"
                        f"Error: {summarize_text(result.stderr, 240)}"
                    )

        self.memory.save()
        self._build_report(all_results=all_results, tips=tips)
        if self.matrix_notify_finish:
            successful = sum(1 for item in all_results if item.success)
            failed = sum(1 for item in all_results if not item.success)
            self._notify_matrix(
                f"[Adaptive Agent] Run completed at {utc_now_iso()}\n"
                f"Executed: {len(all_results)} | Successful: {successful} | Failed: {failed}\n"
                f"Skipped/Dry: {skipped}\n"
                f"Report: {self.report_path}"
            )


def load_config(path: Path) -> Dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    if not config.get("targets"):
        raise ValueError("Config must include at least one target in 'targets'.")
    if not config.get("scope_patterns"):
        raise ValueError("Config must include 'scope_patterns' for authorization checks.")
    return config


def resolve_config_path(path_or_none: str | None) -> Path:
    if path_or_none:
        return Path(path_or_none)
    script_dir = Path(__file__).resolve().parent
    primary = script_dir / "config.json"
    if primary.exists():
        return primary
    fallback = script_dir / "config.example.json"
    if fallback.exists():
        return fallback
    raise FileNotFoundError(
        "No config path provided and no config.json/config.example.json found next to agent.py."
    )


def build_agent(config_path: Path) -> Agent:
    config = load_config(config_path)
    return Agent(config=config, config_path=config_path)


def run_cmd(args: argparse.Namespace) -> None:
    config_path = resolve_config_path(args.config)
    agent = build_agent(config_path)
    if args.live:
        agent.dry_run = False

    if args.import_chat:
        for import_path_raw in args.import_chat:
            import_path = Path(import_path_raw)
            imported = agent.import_conversation_file(
                path=import_path,
                source=f"chat-import:{import_path.name}",
            )
            print(f"Imported {imported} conversation entries from {import_path}")

    if not args.continuous:
        agent.run_once()
        print(f"Run complete. Report: {agent.report_path}")
        return

    interval = int(agent.config.get("continuous_interval_seconds", 300))
    print(f"Continuous mode enabled. Interval={interval}s")
    while True:
        agent.run_once()
        print(f"Run complete at {utc_now_iso()} -> {agent.report_path}")
        time.sleep(interval)


def guided_run_cmd(args: argparse.Namespace) -> None:
    config_path = resolve_config_path(args.config)
    base_config = load_config(config_path)

    target_type, target, scope_patterns = collect_interactive_target()
    print(f"Selected target: {target_type} -> {target}")
    print("Proceeding with guided run for the selected target.")

    mode = prompt_user("Run mode [dry/live] (default: live): ").lower() or "live"
    live_run = mode == "live"

    runtime_config = json.loads(json.dumps(base_config))
    runtime_config["targets"] = [target]
    runtime_config["scope_patterns"] = scope_patterns
    runtime_config["objective"] = (
        f"Assess authorized {target_type} target {target} for security posture."
    )

    runs_dir = config_path.parent / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    guided_config_path = runs_dir / "guided_last_config.json"
    guided_config_path.write_text(json.dumps(runtime_config, indent=2), encoding="utf-8")

    agent = Agent(config=runtime_config, config_path=config_path)
    agent.dry_run = not live_run
    agent.run_once()
    print(f"Run complete. Report: {agent.report_path}")
    print(f"Saved guided config: {guided_config_path}")


def memory_import_cmd(args: argparse.Namespace) -> None:
    config_path = resolve_config_path(args.config)
    agent = build_agent(config_path)
    import_path = Path(args.path)
    imported = agent.import_conversation_file(path=import_path, source=args.source)
    print(f"Imported {imported} entries into {agent.archive.db_path}")


def memory_search_cmd(args: argparse.Namespace) -> None:
    config_path = resolve_config_path(args.config)
    agent = build_agent(config_path)
    rows = agent.archive.search(query=args.query, limit=args.limit)
    print(json.dumps(rows, indent=2))


def memory_stats_cmd(args: argparse.Namespace) -> None:
    config_path = resolve_config_path(args.config)
    agent = build_agent(config_path)
    print(
        json.dumps(
            {
                "conversation_db": str(agent.archive.db_path),
                "rows": agent.archive.count(),
            },
            indent=2,
        )
    )


def build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Adaptive Security Assessment Agent")
    subparsers = parser.add_subparsers(dest="command", required=False)

    run_parser = subparsers.add_parser("run", help="Execute assessment playbook")
    run_parser.add_argument("--config", required=False, help="Path to JSON config file")
    run_parser.add_argument(
        "--continuous",
        action="store_true",
        help="Run continuously with interval from config",
    )
    run_parser.add_argument(
        "--live",
        action="store_true",
        help="Force live execution for this run (overrides config dry_run=true)",
    )
    run_parser.add_argument(
        "--import-chat",
        action="append",
        help="Optional path to .jsonl or .txt chat transcript (repeatable)",
    )
    run_parser.set_defaults(func=run_cmd)

    guided_parser = subparsers.add_parser(
        "guided-run",
        help="Interactive mode: choose website or IP, enter target, then run assessment",
    )
    guided_parser.add_argument("--config", required=False, help="Path to JSON config file")
    guided_parser.set_defaults(func=guided_run_cmd)

    import_parser = subparsers.add_parser(
        "memory-import", help="Import historical conversation file into archive"
    )
    import_parser.add_argument("--config", required=False, help="Path to JSON config file")
    import_parser.add_argument("--path", required=True, help="Path to .jsonl or .txt transcript")
    import_parser.add_argument("--source", default="manual-import", help="Source label")
    import_parser.set_defaults(func=memory_import_cmd)

    search_parser = subparsers.add_parser("memory-search", help="Search historical archive")
    search_parser.add_argument("--config", required=False, help="Path to JSON config file")
    search_parser.add_argument("--query", required=True, help="Search query")
    search_parser.add_argument("--limit", type=int, default=5, help="Number of rows to return")
    search_parser.set_defaults(func=memory_search_cmd)

    stats_parser = subparsers.add_parser("memory-stats", help="Show archive row count")
    stats_parser.add_argument("--config", required=False, help="Path to JSON config file")
    stats_parser.set_defaults(func=memory_stats_cmd)

    return parser


def main() -> None:
    parser = build_cli()
    args = parser.parse_args()
    if args.command is None:
        fallback_args = argparse.Namespace(
            command="guided-run",
            config=None,
            func=guided_run_cmd,
        )
        print("No command provided. Entering guided mode.")
        guided_run_cmd(fallback_args)
        return

    args.func(args)


if __name__ == "__main__":
    main()
