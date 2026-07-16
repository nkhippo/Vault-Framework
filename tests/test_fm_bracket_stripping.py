"""Failing/unit tests for FM wikilink-bracket stripping in 04_rewrite_refs."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

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


INDEX = {
    "docs/a.md": "mt-2026-07-17-aaa1",
    "docs/b.md": "mt-2026-07-17-bbb2",
    "notes/c.md": "nt-2026-07-17-ccc3",
}


def test_strip_simple_wrap() -> None:
    mod = _load_rewrite()
    assert hasattr(mod, "strip_wikilink_wrapping")
    assert mod.strip_wikilink_wrapping("[[docs/a.md]]") == "docs/a.md"


def test_strip_alias() -> None:
    mod = _load_rewrite()
    assert mod.strip_wikilink_wrapping("[[docs/a.md|Display A]]") == "docs/a.md"


def test_strip_section() -> None:
    mod = _load_rewrite()
    assert mod.strip_wikilink_wrapping("[[docs/a.md#Summary]]") == "docs/a.md"


def test_strip_section_and_alias() -> None:
    mod = _load_rewrite()
    assert (
        mod.strip_wikilink_wrapping("[[docs/a.md#Summary|Display]]") == "docs/a.md"
    )


def test_strip_whitespace() -> None:
    mod = _load_rewrite()
    assert mod.strip_wikilink_wrapping("  [[docs/a.md]]  ") == "docs/a.md"


def test_strip_adds_md_extension() -> None:
    mod = _load_rewrite()
    assert mod.strip_wikilink_wrapping("[[docs/a]]") == "docs/a.md"


def test_strip_passthrough_bare_path() -> None:
    mod = _load_rewrite()
    assert mod.strip_wikilink_wrapping("docs/a.md") == "docs/a.md"


def test_resolve_wrapped_fm_value() -> None:
    """Wrapped FM value must resolve after strip (was target_not_found)."""
    mod = _load_rewrite()
    root = FIXTURES
    resolved, err = mod.resolve_target(
        "01_simple_wrap.md",
        mod.strip_wikilink_wrapping("[[docs/a.md]]"),
        root,
        INDEX,
    )
    assert err is None
    assert resolved == "docs/a.md"


def test_rewrite_frontmatter_simple_wrap() -> None:
    mod = _load_rewrite()
    text = (FIXTURES / "01_simple_wrap.md").read_text(encoding="utf-8")
    from lib.common import parse_frontmatter

    fm, _, _ = parse_frontmatter(text)
    assert fm is not None
    broken: list[dict[str, str]] = []
    new_fm, count = mod.rewrite_frontmatter(
        fm, "01_simple_wrap.md", FIXTURES, INDEX, broken, text
    )
    assert count == 1
    assert new_fm.get("related_id") == "mt-2026-07-17-aaa1"
    assert broken == []
    # legacy key preserved
    assert new_fm.get("related") == "[[docs/a.md]]"


def test_rewrite_frontmatter_array_wrap() -> None:
    mod = _load_rewrite()
    text = (FIXTURES / "06_array_wrap.md").read_text(encoding="utf-8")
    from lib.common import parse_frontmatter

    fm, _, _ = parse_frontmatter(text)
    assert fm is not None
    broken: list[dict[str, str]] = []
    new_fm, count = mod.rewrite_frontmatter(
        fm, "06_array_wrap.md", FIXTURES, INDEX, broken, text
    )
    assert count == 3
    assert new_fm.get("related_ids") == [
        "mt-2026-07-17-aaa1",
        "mt-2026-07-17-bbb2",
        "nt-2026-07-17-ccc3",
    ]
    assert broken == []


def test_rewrite_frontmatter_skips_when_id_present() -> None:
    mod = _load_rewrite()
    text = (FIXTURES / "08_already_has_id.md").read_text(encoding="utf-8")
    from lib.common import parse_frontmatter

    fm, _, _ = parse_frontmatter(text)
    assert fm is not None
    broken: list[dict[str, str]] = []
    new_fm, count = mod.rewrite_frontmatter(
        fm, "08_already_has_id.md", FIXTURES, INDEX, broken, text
    )
    assert count == 0
    assert new_fm.get("related_id") == "mt-2026-07-17-aaa1"
    assert broken == []
