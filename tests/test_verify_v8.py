"""Tests for V8 leftover path-wikilink detection."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.common import parse_frontmatter  # noqa: E402
from lib.verify_core import VerifyContext, check_v8  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


def _ctx(tmp_path: Path, files: list[Path]) -> VerifyContext:
    return VerifyContext(
        repo_root=tmp_path,
        files=files,
        id_map={},
        broken=set(),
    )


def test_v8_fails_on_unrewritten_path_wikilink_outside_fence(tmp_path: Path) -> None:
    md = tmp_path / "note.md"
    md.write_text("# x\n\nSee [[docs/other.md|other]]\n", encoding="utf-8")
    result = check_v8(_ctx(tmp_path, [md]), [md])
    assert result.status == "FAIL"
    assert result.failures


def test_v8_passes_when_only_id_wikilinks(tmp_path: Path) -> None:
    md = tmp_path / "note.md"
    md.write_text("# x\n\nSee [[pj-2026-07-17-abcd|ok]]\n", encoding="utf-8")
    result = check_v8(_ctx(tmp_path, [md]), [md])
    assert result.status == "PASS"


def test_v8_skips_path_wikilink_inside_fence(tmp_path: Path) -> None:
    md = tmp_path / "note.md"
    md.write_text(
        "# x\n\n```markdown\n[[docs/inside.md|ex]]\n```\n\n[[pj-2026-07-17-abcd|ok]]\n",
        encoding="utf-8",
    )
    result = check_v8(_ctx(tmp_path, [md]), [md])
    assert result.status == "PASS"


def test_v8_detects_wikilink_after_false_close_bug_fixed(tmp_path: Path) -> None:
    """If ```javascript wrongly closed a fence, outside wiki would be missed or mis-scoped."""
    md = tmp_path / "note.md"
    md.write_text(
        "```markdown\n"
        "example\n"
        "```javascript\n"
        "still example\n"
        "```\n"
        "\n"
        "[[docs/must-detect.md|x]]\n",
        encoding="utf-8",
    )
    result = check_v8(_ctx(tmp_path, [md]), [md])
    assert result.status == "FAIL"
    assert any("must-detect.md" in f.get("detail", "") for f in result.failures)
