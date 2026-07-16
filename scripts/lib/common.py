# Source: Vault-Framework/scripts/lib/common.py @ <commit-sha will be filled by caller>
"""Common helpers for migration and validate scripts."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Iterator

import yaml

EXCLUDE_DIRS: set[str] = {
    "node_modules",
    ".git",
    "dist",
    "build",
    ".next",
    "out",
    "coverage",
    "_site",
    ".vscode",
    ".idea",
    "__pycache__",
    ".venv",
    "venv",
    ".pytest_cache",
    "migration",
    "audit",
}

MD_SUFFIXES: set[str] = {".md", ".markdown"}

ID_RE = re.compile(r"^(pj|nt|kn|mt)-\d{4}-\d{2}-\d{2}-[0-9a-f]{4}$")

JST = timezone(timedelta(hours=9), name="Asia/Tokyo")

FM_PATH_KEYS: tuple[str, ...] = (
    "related",
    "derived_from",
    "source",
    "link",
    "ref",
    "parent",
)


def add_common_args(parser: argparse.ArgumentParser) -> None:
    """Attach CLI args shared by all scripts."""
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (default: cwd)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose logging",
    )


def resolve_repo_root(path: Path) -> Path:
    """Return absolute repo root."""
    return path.expanduser().resolve()


def to_posix(path: Path | str) -> str:
    """Normalize a path to POSIX forward-slash form."""
    return Path(path).as_posix()


def should_skip_dir(rel: Path) -> bool:
    """True if any path component is an excluded directory."""
    return any(part in EXCLUDE_DIRS for part in rel.parts)


def is_markdown(path: Path) -> bool:
    """True if file suffix looks like markdown (case-insensitive)."""
    return path.suffix.lower() in MD_SUFFIXES


def iter_markdown_files(repo_root: Path) -> Iterator[Path]:
    """Yield absolute paths of markdown files under repo_root."""
    for p in sorted(repo_root.rglob("*")):
        if not p.is_file():
            continue
        try:
            rel = p.relative_to(repo_root)
        except ValueError:
            continue
        if should_skip_dir(rel):
            continue
        if is_markdown(p):
            yield p


def rel_posix(repo_root: Path, abs_path: Path) -> str:
    """Repo-relative POSIX path."""
    return to_posix(abs_path.relative_to(repo_root))


def log(verbose: bool, msg: str) -> None:
    """Print verbose message to stderr."""
    if verbose:
        print(msg, file=sys.stderr)


def now_jst() -> datetime:
    """Current datetime in Asia/Tokyo."""
    return datetime.now(JST)


def today_jst() -> str:
    """Today as YYYY-MM-DD in JST."""
    return now_jst().strftime("%Y-%m-%d")


def iso_jst() -> str:
    """Current ISO8601 timestamp in JST."""
    return now_jst().isoformat(timespec="seconds")


def parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, int, str]:
    """Parse YAML front matter.

    Returns (fm_dict_or_None, body_start_line_1indexed, body_text).
    If no front matter, returns (None, 1, text).
    """
    if not text.startswith("---"):
        return None, 1, text
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, 1, text
    end_idx: int | None = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None, 1, text
    fm_text = "".join(lines[1:end_idx])
    try:
        loaded = yaml.safe_load(fm_text)
    except yaml.YAMLError:
        raise
    if loaded is None:
        loaded = {}
    if not isinstance(loaded, dict):
        raise ValueError("Front Matter is not a mapping")
    body = "".join(lines[end_idx + 1 :])
    body_start = end_idx + 2  # 1-indexed line after closing ---
    return loaded, body_start, body


def dump_frontmatter(fm: dict[str, Any]) -> str:
    """Serialize front matter dict to YAML block including --- fences."""
    dumped = yaml.safe_dump(
        fm,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    ).rstrip() + "\n"
    return f"---\n{dumped}---\n"


def first_h1(body: str) -> str | None:
    """Return first ATX H1 text, or None."""
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip() or None
    return None


def git_first_commit_date(repo_root: Path, rel_path: str) -> str | None:
    """Oldest author date (ISO) for path, or None if unavailable."""
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--diff-filter=A",
                "--format=%aI",
                "--follow",
                "--",
                rel_path,
            ],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    lines = [ln.strip() for ln in result.stdout.splitlines() if ln.strip()]
    if not lines:
        return None
    return lines[-1]


def to_jst_date(iso_or_none: str | None, fallback: str) -> str:
    """Convert ISO datetime to YYYY-MM-DD in JST, or fallback."""
    if not iso_or_none:
        return fallback
    try:
        raw = iso_or_none.replace("Z", "+00:00")
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=JST)
        return dt.astimezone(JST).strftime("%Y-%m-%d")
    except ValueError:
        return fallback


def infer_prefix(path: str, is_vault_repo: bool) -> str:
    """Infer ID prefix from path per docs/id-scheme.md Type Inference.

    Non-Vault repos always return ``pj-``.
    """
    if not is_vault_repo:
        return "pj"
    p = path.lstrip("./")
    if p.startswith("30_projects/"):
        return "pj"
    if p.startswith("20_notes/"):
        return "nt"
    if p.startswith("40_knowledge/") or p.startswith("10_chat_logs/"):
        return "kn"
    if p.startswith("50_self/") or p.startswith("00_meta/"):
        return "mt"
    return "mt"


def extract_repo_name(repo_root: Path, explicit: str | None) -> str:
    """Resolve repository name from CLI, git remote, or directory name."""
    if explicit:
        return explicit
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            url = result.stdout.strip().rstrip("/")
            name = url.rsplit("/", 1)[-1]
            if name.endswith(".git"):
                name = name[:-4]
            if name:
                return name
    except OSError:
        pass
    return repo_root.name


def is_vault_repo_name(repo_name: str) -> bool:
    """True if repo_name is exactly 'Vault' (case-insensitive)."""
    return repo_name.lower() == "vault"


def _fence_indent_ok(line: str) -> bool:
    """True if line has at most 3 leading spaces before a potential fence (CommonMark)."""
    i = 0
    while i < len(line) and line[i] == " ":
        i += 1
        if i > 3:
            return False
    return True


def _parse_opening_fence(line: str) -> tuple[str, int] | None:
    """Return (fence_char, fence_len) for an opening fence line, else None.

    Opening fences may include an info string (e.g. ```yaml). Tabs in indent
    are not treated as opening fences here (indent must be spaces only, ≤3).
    """
    if not _fence_indent_ok(line):
        return None
    stripped = line.lstrip(" ")
    if not stripped:
        return None
    ch = stripped[0]
    if ch not in ("`", "~"):
        return None
    n = 0
    for c in stripped:
        if c == ch:
            n += 1
        else:
            break
    if n < 3:
        return None
    # Info string follows; backticks cannot appear in info for backtick fences
    # (CommonMark). We only need to recognize an opening line.
    return ch, n


def _is_closing_fence(line: str, fence_char: str, fence_len: int) -> bool:
    """True if line closes a fence opened with fence_char * fence_len.

    Closing fence: ≤3 space indent, ≥fence_len of the same char, no info string.
    """
    if not _fence_indent_ok(line):
        return False
    stripped = line.lstrip(" ")
    if not stripped.startswith(fence_char * fence_len):
        return False
    n = 0
    for c in stripped:
        if c == fence_char:
            n += 1
        else:
            break
    if n < fence_len:
        return False
    # Remainder must be whitespace only (no info string)
    return stripped[n:].strip() == ""


def split_fenced_regions(text: str) -> list[tuple[int, int, bool]]:
    """Return list of (start_offset, end_offset, is_code) covering full text.

    Marks fenced ``` / ~~~ blocks as code using CommonMark-ish rules:
    - Opening: line with ≤3 space indent, ≥3 backticks/tildes, optional info
    - Closing: same character, length ≥ opening, no info string
    - Unclosed fence runs to EOF
    - Indented (4-space) code blocks are NOT treated as fences
    - Inline single-backtick code is NOT a fence
    """
    lines = text.splitlines(keepends=True)
    regions: list[tuple[int, int, bool]] = []
    offset = 0
    in_fence = False
    fence_char = ""
    fence_len = 0
    for line in lines:
        end = offset + len(line)
        if in_fence:
            regions.append((offset, end, True))
            if _is_closing_fence(line.rstrip("\n"), fence_char, fence_len):
                in_fence = False
                fence_char = ""
                fence_len = 0
        else:
            opened = _parse_opening_fence(line.rstrip("\n"))
            if opened is not None:
                fence_char, fence_len = opened
                in_fence = True
                regions.append((offset, end, True))
            else:
                regions.append((offset, end, False))
        offset = end
    return regions


def offset_in_code(regions: list[tuple[int, int, bool]], pos: int) -> bool:
    """True if character offset falls inside a code region."""
    for start, end, is_code in regions:
        if start <= pos < end:
            return is_code
    return False


def json_safe(obj: Any) -> Any:
    """Convert YAML-loaded values into JSON-serializable forms."""
    if isinstance(obj, dict):
        return {str(k): json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [json_safe(v) for v in obj]
    if isinstance(obj, datetime):
        return obj.isoformat()
    from datetime import date as date_cls

    if isinstance(obj, date_cls):
        return obj.isoformat()
    return obj


def ensure_parent_dir(path: Path) -> None:
    """Create parent directories for path if missing."""
    path.parent.mkdir(parents=True, exist_ok=True)
