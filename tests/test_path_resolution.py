"""Tests for path resolution strategies in 04_rewrite_refs."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

FIXTURES = Path(__file__).parent / "fixtures" / "vault-root-path-samples"


def _load_rewrite():
    spec = importlib.util.spec_from_file_location(
        "rewrite04", ROOT / "scripts" / "migration" / "04_rewrite_refs.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _index_for_samples() -> dict[str, str]:
    return {
        "docs/target-a.md": "pj-2026-07-17-aaa1",
        "docs/source.md": "pj-2026-07-17-ccc3",
        "notes/unique-basename.md": "pj-2026-07-17-bbb2",
    }


def test_absolute_path_resolution() -> None:
    mod = _load_rewrite()
    root = FIXTURES
    index = _index_for_samples()
    resolved, err = mod.resolve_target("docs/source.md", "/docs/target-a.md", root, index)
    assert err is None
    assert resolved == "docs/target-a.md"


def test_vault_root_style_resolution() -> None:
    mod = _load_rewrite()
    root = FIXTURES
    index = _index_for_samples()
    # From docs/source.md, vault-root style docs/target-a.md must resolve
    resolved, err = mod.resolve_target("docs/source.md", "docs/target-a.md", root, index)
    assert err is None
    assert resolved == "docs/target-a.md"


def test_relative_path_resolution() -> None:
    mod = _load_rewrite()
    root = FIXTURES
    index = _index_for_samples()
    resolved, err = mod.resolve_target("docs/source.md", "./target-a.md", root, index)
    assert err is None
    assert resolved == "docs/target-a.md"


def test_basename_unique_resolution() -> None:
    mod = _load_rewrite()
    root = FIXTURES
    index = _index_for_samples()
    resolved, err = mod.resolve_target("docs/source.md", "unique-basename.md", root, index)
    assert err is None
    assert resolved == "notes/unique-basename.md"


def test_basename_ambiguous() -> None:
    mod = _load_rewrite()
    root = FIXTURES
    # two same basenames; source has no relative neighbor named dup.md
    index = {
        "docs/dup.md": "pj-2026-07-17-d001",
        "notes/dup.md": "pj-2026-07-17-d002",
        "other/source.md": "pj-2026-07-17-ccc3",
    }
    resolved, err = mod.resolve_target("other/source.md", "dup.md", root, index)
    assert resolved is None
    assert err == "ambiguous_target"


def test_priority_vault_root_over_relative_misparse() -> None:
    """Relative-only would look for docs/source/docs/target-a.md and fail."""
    mod = _load_rewrite()
    root = FIXTURES
    index = _index_for_samples()
    resolved, err = mod.resolve_target("docs/source.md", "docs/target-a.md", root, index)
    assert err is None
    assert resolved == "docs/target-a.md"
