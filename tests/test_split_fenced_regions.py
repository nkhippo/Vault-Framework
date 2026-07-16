"""Tests for split_fenced_regions / offset_in_code."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.common import offset_in_code, parse_frontmatter, split_fenced_regions  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


def _body(text: str) -> str:
    _, _, body = parse_frontmatter(text)
    return body


def test_simple_fence_inside_and_outside() -> None:
    text = "# Hi\n\n```\ncode\n```\n\noutside [[docs/a.md]]\n"
    regions = split_fenced_regions(text)
    # "code" line is in code
    code_pos = text.index("code")
    assert offset_in_code(regions, code_pos) is True
    out_pos = text.index("[[docs/a.md]]")
    assert offset_in_code(regions, out_pos) is False


def test_language_identifier_fence() -> None:
    text = "```yaml\nkey: 1\n```\nafter\n"
    regions = split_fenced_regions(text)
    assert offset_in_code(regions, text.index("key")) is True
    assert offset_in_code(regions, text.index("after")) is False


def test_unclosed_fence_to_eof() -> None:
    text = "before\n```\nstill code\n"
    regions = split_fenced_regions(text)
    assert offset_in_code(regions, text.index("still")) is True


def test_closing_fence_rejects_info_string() -> None:
    """```javascript must NOT close an open ```markdown fence."""
    text = FIXTURES.joinpath("false-close-fence.md").read_text(encoding="utf-8")
    regions = split_fenced_regions(text)
    # After the false-close bug, AFTER_FENCE_WIKI was wrongly outside;
    # correct behavior: still inside until a bare ``` closer — but our fixture
    # has no bare closer after javascript line, so wiki is still inside fence
    # until we hit a proper close. Looking at fixture: no close after javascript
    # content before AFTER_FENCE... Actually structure is:
    # ```markdown
    # example
    # ```javascript   <- must NOT close
    # this was wrongly...
    # ```             <- this closes markdown
    # AFTER_FENCE_WIKI
    wiki_pos = text.index("AFTER_FENCE_WIKI")
    assert offset_in_code(regions, wiki_pos) is False
    js_pos = text.index("this was wrongly")
    assert offset_in_code(regions, js_pos) is True


def test_indented_lines_are_not_code() -> None:
    text = "para\n\n    indented but not a fence\n\n[[docs/a.md]]\n"
    regions = split_fenced_regions(text)
    assert offset_in_code(regions, text.index("indented")) is False
    assert offset_in_code(regions, text.index("[[docs/a.md]]")) is False


def test_inline_code_is_not_fence() -> None:
    text = "use `[[docs/a.md]]` inline\n"
    regions = split_fenced_regions(text)
    assert offset_in_code(regions, text.index("[[docs/a.md]]")) is False


def test_thinkgrindai_obsidian_setup_wikilinks_are_inside_example_fences() -> None:
    """Investigation finding: audit's 5 wikilinks live inside ```markdown examples."""
    raw = FIXTURES.joinpath("thinkgrindai-obsidian-setup.md").read_text(encoding="utf-8")
    body = _body(raw)
    regions = split_fenced_regions(body)
    targets = [
        "[[docs/requirements-thinking.md]]",
        "[[docs/specification-thinking.md]]",
        "[[docs/cursor-instructions/cursor_instruction_thinking_v2.md]]",
        "[[ideas/REQ-001-thinking.md]]",
    ]
    for t in targets:
        pos = body.index(t)
        assert offset_in_code(regions, pos) is True, f"{t} should remain in example fence"


def test_longer_fence_requires_matching_close() -> None:
    text = "````\ncode with ``` inside\n````\nafter\n"
    regions = split_fenced_regions(text)
    assert offset_in_code(regions, text.index("code with")) is True
    assert offset_in_code(regions, text.index("after")) is False
