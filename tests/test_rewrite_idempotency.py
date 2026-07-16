"""Idempotency: running 04_rewrite_refs twice must not change content."""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

FIXTURES = Path(__file__).parent / "fixtures" / "vault-fm-brackets"


def _load_rewrite():
    spec = importlib.util.spec_from_file_location(
        "rewrite04", ROOT / "scripts" / "migration" / "04_rewrite_refs.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_rewrite_frontmatter_twice_is_noop(tmp_path: Path) -> None:
    """After first FM rewrite adds related_id, second pass must not change FM."""
    mod = _load_rewrite()
    from lib.common import parse_frontmatter, dump_frontmatter

    src = FIXTURES / "01_simple_wrap.md"
    text = src.read_text(encoding="utf-8")
    index = {
        "docs/a.md": "mt-2026-07-17-aaa1",
        "docs/b.md": "mt-2026-07-17-bbb2",
        "notes/c.md": "nt-2026-07-17-ccc3",
    }
    # Make mini repo with targets
    (tmp_path / "docs").mkdir()
    shutil.copy(FIXTURES / "docs" / "a.md", tmp_path / "docs" / "a.md")
    note = tmp_path / "note.md"
    note.write_text(text, encoding="utf-8")

    fm1, _, body = parse_frontmatter(text)
    assert fm1 is not None
    broken1: list = []
    new_fm1, n1 = mod.rewrite_frontmatter(fm1, "note.md", tmp_path, index, broken1, text)
    assert n1 == 1
    assert broken1 == []
    text_after = dump_frontmatter(new_fm1) + (body if body.startswith("\n") else "\n" + body)

    fm2, _, body2 = parse_frontmatter(text_after)
    assert fm2 is not None
    broken2: list = []
    new_fm2, n2 = mod.rewrite_frontmatter(
        fm2, "note.md", tmp_path, index, broken2, text_after
    )
    assert n2 == 0
    assert broken2 == []
    assert new_fm2 == fm2


def test_full_file_rewrite_twice_unchanged(tmp_path: Path) -> None:
    """End-to-end: two rewrite_body+frontmatter passes leave text identical."""
    mod = _load_rewrite()
    from lib.common import parse_frontmatter, dump_frontmatter

    (tmp_path / "docs").mkdir()
    shutil.copy(FIXTURES / "docs" / "a.md", tmp_path / "docs" / "a.md")
    shutil.copy(FIXTURES / "docs" / "b.md", tmp_path / "docs" / "b.md")
    (tmp_path / "notes").mkdir()
    shutil.copy(FIXTURES / "notes" / "c.md", tmp_path / "notes" / "c.md")

    index = {
        "docs/a.md": "mt-2026-07-17-aaa1",
        "docs/b.md": "mt-2026-07-17-bbb2",
        "notes/c.md": "nt-2026-07-17-ccc3",
    }

    # Body already id-rewritten + FM wrap needing strip
    text0 = """---
title: twice
related:
  - "[[docs/a.md]]"
  - "[[docs/b.md]]"
---
# twice

See [[mt-2026-07-17-aaa1|A]] and more.
"""
    path = tmp_path / "twice.md"
    path.write_text(text0, encoding="utf-8")

    def apply_once(text: str) -> tuple[str, int, int, int]:
        fm, _, body = parse_frontmatter(text)
        broken: list = []
        new_body, md_n, wiki_n = mod.rewrite_body(body, "twice.md", tmp_path, index, broken)
        assert fm is not None
        new_fm, fm_n = mod.rewrite_frontmatter(fm, "twice.md", tmp_path, index, broken, text)
        out = dump_frontmatter(new_fm)
        if new_body:
            out += new_body if new_body.startswith("\n") else "\n" + new_body
        return out, md_n, wiki_n, fm_n

    once, md1, wiki1, fm1 = apply_once(text0)
    assert fm1 == 2
    assert md1 == 0 and wiki1 == 0  # body already id-form
    twice, md2, wiki2, fm2 = apply_once(once)
    assert (md2, wiki2, fm2) == (0, 0, 0)
    assert twice == once
