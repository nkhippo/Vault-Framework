#!/usr/bin/env python3
# Source: Vault-Framework/scripts/migration/04_rewrite_refs.py @ <commit-sha will be filled by caller>
"""Rewrite path-based references to wikilink ID references."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from lib.common import (  # noqa: E402
    FM_PATH_KEYS,
    add_common_args,
    dump_frontmatter,
    ensure_parent_dir,
    iter_markdown_files,
    log,
    offset_in_code,
    parse_frontmatter,
    rel_posix,
    resolve_repo_root,
    split_fenced_regions,
    to_posix,
)

MD_LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+?\.md(?:#[^)]*)?)\)")
WIKILINK_PATH_RE = re.compile(
    r"\[\[([^\]|#]*\/[^\]|#]*)(#[^\]|]*)?(?:\|([^\]]*))?\]\]"
)


def _index_hit(candidate: Path | str, repo_root: Path, index: dict[str, str]) -> str | None:
    """Return index key if candidate resolves inside repo and exists in index."""
    try:
        resolved = to_posix(Path(os.path.normpath(Path(candidate).as_posix())))
        abs_candidate = (repo_root / resolved).resolve()
        if not str(abs_candidate).startswith(str(repo_root.resolve())):
            return None
    except Exception:  # noqa: BLE001
        return None
    if resolved in index:
        return resolved
    alt = resolved.lstrip("./")
    if alt in index:
        return alt
    return None


def resolve_target(
    source_rel: str,
    raw_target: str,
    repo_root: Path,
    index: dict[str, str],
) -> tuple[str | None, str | None]:
    """Resolve a path reference to an index key.

    Resolution order (first hit wins):
      1. absolute path (leading ``/``) from repo root
      2. vault-root style (repo-root join of the given path)
      3. file-relative from the source file's directory
      4. unique basename match across the index

    Returns (resolved_posix_path, error_reason).
    """
    target = raw_target.strip()
    if target.startswith(("http://", "https://", "mailto:")):
        return None, None  # not a path ref — caller should skip

    if "#" in target:
        target, _section = target.split("#", 1)

    if not target.lower().endswith(".md"):
        if "." not in Path(target).name:
            target = target + ".md"

    # 1. Absolute (leading /)
    if target.startswith("/"):
        hit = _index_hit(Path(target.lstrip("/")), repo_root, index)
        if hit is not None:
            return hit, None

    # 2. Vault-root style (repo-root join)
    if not target.startswith("/"):
        hit = _index_hit(Path(target), repo_root, index)
        if hit is not None:
            return hit, None

    # 3. File-relative
    source_dir = Path(source_rel).parent
    hit = _index_hit(source_dir / target.lstrip("/"), repo_root, index)
    if hit is not None:
        return hit, None

    # Reject paths that escape the repo via relative traversal
    try:
        abs_rel = (repo_root / source_dir / target.lstrip("/")).resolve()
        if not str(abs_rel).startswith(str(repo_root.resolve())):
            return None, "outside_repo"
    except Exception:  # noqa: BLE001
        return None, "outside_repo"

    # 4. Basename unique match
    base = Path(target).name
    matches = [k for k in index if Path(k).name == base]
    if len(matches) == 1:
        return matches[0], None
    if len(matches) > 1:
        return None, "ambiguous_target"

    return None, "target_not_found"


def line_number_for_offset(text: str, offset: int) -> int:
    """1-indexed line number for a character offset."""
    return text.count("\n", 0, offset) + 1


def rewrite_body(
    body: str,
    source_rel: str,
    repo_root: Path,
    index: dict[str, str],
    broken: list[dict[str, str]],
) -> tuple[str, int, int]:
    """Rewrite markdown links and path wikilinks in body.

    Returns (new_body, md_link_count, wikilink_count).
    """
    regions = split_fenced_regions(body)
    md_count = 0
    wiki_count = 0

    def repl_md(m: re.Match[str]) -> str:
        nonlocal md_count
        if offset_in_code(regions, m.start()):
            return m.group(0)
        text, raw = m.group(1), m.group(2)
        if raw.strip().startswith(("http://", "https://", "mailto:")):
            return m.group(0)
        path_part = raw.split("#", 1)[0]
        section = ""
        if "#" in raw:
            section = "#" + raw.split("#", 1)[1]
        resolved, reason = resolve_target(source_rel, path_part, repo_root, index)
        if reason:
            broken.append(
                {
                    "source_file": source_rel,
                    "line_number": str(line_number_for_offset(body, m.start())),
                    "referenced_path": raw,
                    "reason": reason,
                    "pattern_type": "markdown_link",
                }
            )
            return m.group(0)
        assert resolved is not None
        doc_id = index[resolved]
        md_count += 1
        if section:
            return f"[[{doc_id}{section}|{text}]]"
        return f"[[{doc_id}|{text}]]"

    def repl_wiki(m: re.Match[str]) -> str:
        nonlocal wiki_count
        if offset_in_code(regions, m.start()):
            return m.group(0)
        path_part = m.group(1)
        section = m.group(2) or ""
        alias = m.group(3)
        resolved, reason = resolve_target(source_rel, path_part, repo_root, index)
        if reason:
            broken.append(
                {
                    "source_file": source_rel,
                    "line_number": str(line_number_for_offset(body, m.start())),
                    "referenced_path": path_part + section,
                    "reason": reason,
                    "pattern_type": "wikilink",
                }
            )
            return m.group(0)
        assert resolved is not None
        doc_id = index[resolved]
        wiki_count += 1
        if alias is not None:
            return f"[[{doc_id}{section}|{alias}]]"
        return f"[[{doc_id}{section}]]"

    new_body = MD_LINK_RE.sub(repl_md, body)
    # rebuild regions after first pass? Use original regions on original offsets —
    # safer to run wiki on result with fresh regions
    regions = split_fenced_regions(new_body)
    new_body = WIKILINK_PATH_RE.sub(repl_wiki, new_body)
    return new_body, md_count, wiki_count


def looks_like_path(value: Any) -> bool:
    """True if value looks like a markdown path string (bare or ``[[...]]``)."""
    if not isinstance(value, str):
        return False
    v = value.strip()
    if v.startswith("[[") and v.endswith("]]"):
        return True
    return ".md" in v.lower()


def strip_wikilink_wrapping(value: str) -> str:
    """Strip Obsidian wikilink ``[[...]]`` wrapping; return a bare path.

    Handles alias (``|``), section (``#``), surrounding whitespace, and adds
    ``.md`` when the inner path has no extension.
    Bare paths are returned trimmed unchanged (extension not forced).
    """
    v = value.strip()
    if v.startswith("[[") and v.endswith("]]"):
        inner = v[2:-2]
        if "#" in inner:
            inner = inner.split("#", 1)[0]
        if "|" in inner:
            inner = inner.split("|", 1)[0]
        inner = inner.strip()
        if not inner.lower().endswith(".md"):
            if "." not in Path(inner).name:
                inner = inner + ".md"
        return inner
    return v


def rewrite_frontmatter(
    fm: dict[str, Any],
    source_rel: str,
    repo_root: Path,
    index: dict[str, str],
    broken: list[dict[str, str]],
    text: str,
) -> tuple[dict[str, Any], int]:
    """Add *_id / *_ids fields for legacy path keys. Keep legacy keys.

    Idempotent: if ``{key}_id`` or ``{key}_ids`` already exists, skip that key.
    Wikilink-wrapped FM values (``[[path.md]]``) are stripped before resolve.
    """
    fm = dict(fm)
    count = 0
    for key in FM_PATH_KEYS:
        if key not in fm:
            continue
        # Already migrated companion field — do not re-resolve / overwrite
        if f"{key}_id" in fm or f"{key}_ids" in fm:
            continue
        val = fm[key]
        line_no = "1"
        # best-effort line number
        for i, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith(f"{key}:"):
                line_no = str(i)
                break

        if isinstance(val, list):
            ids: list[str] = []
            for item in val:
                if not looks_like_path(item):
                    continue
                raw = strip_wikilink_wrapping(str(item))
                resolved, reason = resolve_target(source_rel, raw, repo_root, index)
                if reason or resolved is None:
                    broken.append(
                        {
                            "source_file": source_rel,
                            "line_number": line_no,
                            "referenced_path": str(item),
                            "reason": reason or "target_not_found",
                            "pattern_type": "frontmatter",
                        }
                    )
                    continue
                ids.append(index[resolved])
            if ids:
                fm[f"{key}_ids"] = ids
                count += len(ids)
        elif looks_like_path(val):
            raw = strip_wikilink_wrapping(str(val))
            resolved, reason = resolve_target(source_rel, raw, repo_root, index)
            if reason or resolved is None:
                broken.append(
                    {
                        "source_file": source_rel,
                        "line_number": line_no,
                        "referenced_path": str(val),
                        "reason": reason or "target_not_found",
                        "pattern_type": "frontmatter",
                    }
                )
            else:
                fm[f"{key}_id"] = index[resolved]
                count += 1
    return fm, count


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Rewrite path refs to wikilink IDs.")
    add_common_args(parser)
    parser.add_argument(
        "--index",
        type=Path,
        default=Path("migration/index.json"),
        help="Index JSON (default: migration/index.json)",
    )
    parser.add_argument(
        "--broken-refs",
        type=Path,
        default=Path("migration/broken-refs.csv"),
        help="Broken refs CSV output",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print diffs only")
    args = parser.parse_args(argv)

    try:
        repo_root = resolve_repo_root(args.repo_root)
        index_path = args.index if args.index.is_absolute() else repo_root / args.index
        if not index_path.is_file():
            print(f"error: index not found: {index_path}", file=sys.stderr)
            return 2
        index: dict[str, str] = json.loads(index_path.read_text(encoding="utf-8"))

        broken: list[dict[str, str]] = []
        totals = {"markdown_link": 0, "wikilink": 0, "frontmatter": 0}

        for abs_path in iter_markdown_files(repo_root):
            rel = rel_posix(repo_root, abs_path)
            text = abs_path.read_text(encoding="utf-8")
            try:
                fm, _, body = parse_frontmatter(text)
            except Exception as exc:  # noqa: BLE001
                print(f"warn: skip unreadable FM {rel}: {exc}", file=sys.stderr)
                continue

            new_body = body
            md_n = wiki_n = fm_n = 0
            if body:
                new_body, md_n, wiki_n = rewrite_body(
                    body, rel, repo_root, index, broken
                )
            new_fm = fm
            if fm is not None:
                new_fm, fm_n = rewrite_frontmatter(
                    fm, rel, repo_root, index, broken, text
                )

            totals["markdown_link"] += md_n
            totals["wikilink"] += wiki_n
            totals["frontmatter"] += fm_n

            if fm is None:
                new_text = new_body
            else:
                assert new_fm is not None
                new_text = dump_frontmatter(new_fm)
                if new_body:
                    new_text += (
                        new_body if new_body.startswith("\n") else "\n" + new_body
                    )

            if new_text == text:
                continue

            log(args.verbose, f"rewrite {rel} (md={md_n} wiki={wiki_n} fm={fm_n})")
            if args.dry_run:
                print(f"=== {rel} ===")
                print(f"changes: md_link={md_n} wikilink={wiki_n} frontmatter={fm_n}")
                continue

            abs_path.write_text(new_text, encoding="utf-8")

        if not args.dry_run:
            out = (
                args.broken_refs
                if args.broken_refs.is_absolute()
                else repo_root / args.broken_refs
            )
            ensure_parent_dir(out)
            with out.open("w", encoding="utf-8", newline="") as fh:
                writer = csv.DictWriter(
                    fh,
                    fieldnames=[
                        "source_file",
                        "line_number",
                        "referenced_path",
                        "reason",
                        "pattern_type",
                    ],
                )
                writer.writeheader()
                writer.writerows(broken)
            print(
                f"rewrote refs: {totals}; broken={len(broken)} -> {out.as_posix()}",
                file=sys.stderr,
            )
        else:
            print(f"dry-run totals: {totals}; broken={len(broken)}", file=sys.stderr)

        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
