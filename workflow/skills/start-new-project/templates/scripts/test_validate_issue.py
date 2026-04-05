"""Tests for validate-issue.py — the issue checkbox tag validator engine.

Covers: parsing, structure rules, sizing rules, tag chains, tag semantics.
Run with: pytest test_validate_issue.py -v
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

# Import validate-issue.py (hyphenated filename requires importlib)
_script_path = Path(__file__).resolve().parent / "validate-issue.py"
_spec = importlib.util.spec_from_file_location("validate_issue", _script_path)
vi = importlib.util.module_from_spec(_spec)
sys.modules["validate_issue"] = vi
_spec.loader.exec_module(vi)


# ─── Fixtures: config ────────────────────────────────────────


@pytest.fixture(scope="session")
def config() -> dict:
    config_path = Path(__file__).resolve().parent / "validate-issue.config.json"
    with open(config_path) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def thresholds(config: dict) -> dict:
    return config["thresholds"]


@pytest.fixture(scope="session")
def tag_order(config: dict) -> list[str]:
    return config["tag_order"]


@pytest.fixture(scope="session")
def structure_rules(config: dict) -> list[dict]:
    return config["sections"]["structure"]["rules"]


@pytest.fixture(scope="session")
def sizing_rules(config: dict) -> list[dict]:
    return config["sections"]["sizing"]["rules"]


@pytest.fixture(scope="session")
def chain_rules(config: dict) -> list[dict]:
    return config["sections"]["tag_chains"]["rules"]


@pytest.fixture(scope="session")
def semantic_rules(config: dict) -> list[dict]:
    return config["sections"]["tag_semantics"]["rules"]


# ─── Fixtures: sample issue bodies ──────────────────────────


VALID_ISSUE_BODY = """\
## What

Build user authentication module.

## Why

Users need to log in securely.

## Acceptance criteria

- [ ] Users can log in with email and password
- [ ] Users can reset their password

## Step 1 — Set up auth infrastructure

- [ ] `[INFRA]` Set up auth database tables and configuration
- [ ] `[RED]` Write failing test for login endpoint
- [ ] `[GREEN]` Implement login endpoint to pass test
- [ ] `[WIRE]` Connect to auth service endpoint integration
- [ ] `[AUDIT]` Run quality.md audit

## Step 2 — Add password reset

- [ ] `[RED]` Write failing test for password reset flow
- [ ] `[GREEN]` Implement password reset to pass test
- [ ] `[WIRE]` Integrate reset handler with email service endpoint
- [ ] `[AUDIT]` Run quality.md audit
"""

MINIMAL_VALID_BODY = """\
## What

Something.

## Why

Because.

## Acceptance criteria

- [ ] It works

## Step 1 — First step

- [ ] `[RED]` Write failing test for feature
- [ ] `[GREEN]` Implement feature to pass test
- [ ] `[AUDIT]` Run quality.md audit

## Step 2 — Second step

- [ ] `[INFRA]` Set up config
- [ ] `[AUDIT]` Run quality.md audit
"""


# ─── Helper: Reporter that collects results ─────────────────


class CollectingReporter(vi.Reporter):
    """Reporter subclass that collects messages for assertions."""

    def __init__(self) -> None:
        super().__init__(verbose=True)
        self.error_messages: list[str] = []
        self.warning_messages: list[str] = []
        self.passed_messages: list[str] = []

    def fail(self, msg: str) -> None:
        super().fail(msg)
        self.error_messages.append(msg)

    def warn(self, msg: str) -> None:
        super().warn(msg)
        self.warning_messages.append(msg)

    def passed(self, msg: str) -> None:
        super().passed(msg)
        self.passed_messages.append(msg)


# ─── Parsing tests ──────────────────────────────────────────


class TestParsing:
    """Test the STEP_HEADER_RE, CHECKBOX_RE patterns and parse_steps()."""

    def test_step_header_regex_em_dash(self):
        m = vi.STEP_HEADER_RE.match("## Step 1 — Set up infrastructure")
        assert m is not None
        assert m.group(1) == "1"
        assert m.group(2) == "Set up infrastructure"

    def test_step_header_regex_en_dash(self):
        m = vi.STEP_HEADER_RE.match("## Step 3 – Some title")
        assert m is not None
        assert m.group(1) == "3"

    def test_step_header_regex_hyphen(self):
        m = vi.STEP_HEADER_RE.match("## Step 2 - Simple title")
        assert m is not None
        assert m.group(1) == "2"

    def test_step_header_regex_no_match_plain_heading(self):
        assert vi.STEP_HEADER_RE.match("## What") is None

    def test_step_header_regex_no_match_missing_dash(self):
        assert vi.STEP_HEADER_RE.match("## Step 1 No dash") is None

    def test_checkbox_regex_standard(self):
        m = vi.CHECKBOX_RE.match("- [ ] `[RED]` Write failing test for login")
        assert m is not None
        assert m.group(1) == "RED"
        assert m.group(2) == "Write failing test for login"

    def test_checkbox_regex_checked(self):
        m = vi.CHECKBOX_RE.match("- [x] `[GREEN]` Implement the feature")
        assert m is not None
        assert m.group(1) == "GREEN"

    def test_checkbox_regex_no_match_plain_list(self):
        assert vi.CHECKBOX_RE.match("- Some plain list item") is None

    def test_checkbox_regex_no_match_no_tag(self):
        assert vi.CHECKBOX_RE.match("- [ ] No tag here") is None

    def test_parse_steps_valid_body(self):
        steps = vi.parse_steps(VALID_ISSUE_BODY)
        assert len(steps) == 2
        assert steps[0].number == 1
        assert steps[0].title == "Set up auth infrastructure"
        assert len(steps[0].checkboxes) == 5
        assert steps[1].number == 2
        assert len(steps[1].checkboxes) == 4

    def test_parse_steps_extracts_tags(self):
        steps = vi.parse_steps(VALID_ISSUE_BODY)
        assert steps[0].tags == ["INFRA", "RED", "GREEN", "WIRE", "AUDIT"]

    def test_parse_steps_no_steps(self):
        body = "## What\nSomething\n## Why\nBecause\n"
        steps = vi.parse_steps(body)
        assert steps == []

    def test_parse_steps_ignores_checkboxes_outside_steps(self):
        body = """\
## Acceptance criteria

- [ ] `[RED]` This should be ignored

## Step 1 — Only step

- [ ] `[RED]` Write test
- [ ] `[GREEN]` Implement
"""
        steps = vi.parse_steps(body)
        assert len(steps) == 1
        assert len(steps[0].checkboxes) == 2


# ─── Structure rule tests ───────────────────────────────────


class TestStructureRules:
    """Test issue-level structure rules: required sections, step count, numbering."""

    def test_what_section_present(self, structure_rules):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "what_section")
        vi.handle_body_match(rule, VALID_ISSUE_BODY, [], r)
        assert r.errors == 0

    def test_what_section_missing(self, structure_rules):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "what_section")
        body = "## Why\nBecause\n## Step 1 — Stuff\n"
        vi.handle_body_match(rule, body, [], r)
        assert r.errors == 1
        assert "What" in r.error_messages[0]

    def test_why_section_present(self, structure_rules):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "why_section")
        vi.handle_body_match(rule, VALID_ISSUE_BODY, [], r)
        assert r.errors == 0

    def test_why_section_missing(self, structure_rules):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "why_section")
        body = "## What\nSomething\n## Step 1 — Stuff\n"
        vi.handle_body_match(rule, body, [], r)
        assert r.errors == 1

    def test_acceptance_criteria_with_checkboxes(self, structure_rules):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "acceptance_criteria")
        vi.handle_section_has_checkboxes(rule, VALID_ISSUE_BODY, [], r)
        assert r.errors == 0
        assert any("2 checkbox" in m for m in r.passed_messages)

    def test_acceptance_criteria_missing_section(self, structure_rules):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "acceptance_criteria")
        body = "## What\nSomething\n## Why\nBecause\n"
        vi.handle_section_has_checkboxes(rule, body, [], r)
        assert r.errors == 1

    def test_acceptance_criteria_no_checkboxes(self, structure_rules):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "acceptance_criteria")
        body = "## Acceptance criteria\n\nJust text, no checkboxes.\n\n## Step 1 — Stuff\n"
        vi.handle_section_has_checkboxes(rule, body, [], r)
        assert r.errors == 1

    def test_step_count_valid(self, structure_rules, thresholds):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "step_count")
        steps = vi.parse_steps(VALID_ISSUE_BODY)
        vi.handle_step_count(rule, "", steps, r, thresholds)
        assert r.errors == 0

    def test_step_count_too_few(self, structure_rules, thresholds):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "step_count")
        steps = [vi.Step(number=1, title="Only one")]
        vi.handle_step_count(rule, "", steps, r, thresholds)
        assert r.errors == 1
        assert "Too few" in r.error_messages[0]

    def test_step_count_too_many(self, structure_rules, thresholds):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "step_count")
        max_s = thresholds["max_steps"]
        steps = [vi.Step(number=i, title=f"Step {i}") for i in range(1, max_s + 3)]
        vi.handle_step_count(rule, "", steps, r, thresholds)
        assert r.errors == 1
        assert "Too many" in r.error_messages[0]

    def test_step_count_at_boundaries(self, structure_rules, thresholds):
        """Exactly min and max should pass."""
        rule = next(x for x in structure_rules if x["key"] == "step_count")
        min_s = thresholds["min_steps"]
        max_s = thresholds["max_steps"]

        r = CollectingReporter()
        steps = [vi.Step(number=i, title=f"S{i}") for i in range(1, min_s + 1)]
        vi.handle_step_count(rule, "", steps, r, thresholds)
        assert r.errors == 0

        r = CollectingReporter()
        steps = [vi.Step(number=i, title=f"S{i}") for i in range(1, max_s + 1)]
        vi.handle_step_count(rule, "", steps, r, thresholds)
        assert r.errors == 0

    def test_step_numbering_sequential(self, structure_rules):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "step_numbering")
        steps = vi.parse_steps(VALID_ISSUE_BODY)
        vi.handle_step_numbering(rule, "", steps, r)
        assert r.errors == 0

    def test_step_numbering_gap(self, structure_rules):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "step_numbering")
        steps = [vi.Step(number=1, title="A"), vi.Step(number=3, title="B")]
        vi.handle_step_numbering(rule, "", steps, r)
        assert r.errors == 1
        assert "expected Step 2" in r.error_messages[0] or "expected 2" in r.error_messages[0]

    def test_step_numbering_duplicate(self, structure_rules):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "step_numbering")
        steps = [vi.Step(number=1, title="A"), vi.Step(number=1, title="B")]
        vi.handle_step_numbering(rule, "", steps, r)
        assert r.errors == 1

    def test_step_numbering_starts_at_zero(self, structure_rules):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "step_numbering")
        steps = [vi.Step(number=0, title="A"), vi.Step(number=1, title="B")]
        vi.handle_step_numbering(rule, "", steps, r)
        assert r.errors == 1

    def test_step_title_em_dash_valid(self, structure_rules):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "step_title_em_dash")
        vi.handle_step_title_format(rule, VALID_ISSUE_BODY, [], r)
        assert r.errors == 0

    def test_step_title_missing_em_dash(self, structure_rules):
        r = CollectingReporter()
        rule = next(x for x in structure_rules if x["key"] == "step_title_em_dash")
        body = "## Step 1 No dash at all\n- [ ] `[RED]` test\n"
        vi.handle_step_title_format(rule, body, [], r)
        assert r.errors == 1


# ─── Sizing rule tests ──────────────────────────────────────


class TestSizingRules:
    """Test step sizing: empty steps, checkbox counts, text length."""

    def _make_step(self, tags_and_texts: list[tuple[str, str]]) -> vi.Step:
        return vi.Step(
            number=1,
            title="Test step",
            checkboxes=[
                vi.Checkbox(tag=t, text=txt, line=f"- [ ] `[{t}]` {txt}")
                for t, txt in tags_and_texts
            ],
        )

    def test_empty_step_fails(self, sizing_rules, thresholds):
        r = CollectingReporter()
        step = vi.Step(number=1, title="Empty")
        vi.validate_step_sizing(step, sizing_rules, r, thresholds)
        assert r.errors >= 1
        assert any("Empty step" in m for m in r.error_messages)

    def test_single_checkbox_passes(self, sizing_rules, thresholds):
        r = CollectingReporter()
        step = self._make_step([("RED", "Write test for feature")])
        vi.validate_step_sizing(step, sizing_rules, r, thresholds)
        assert r.errors == 0

    def test_checkbox_count_over_max(self, sizing_rules, thresholds):
        r = CollectingReporter()
        max_cb = thresholds["max_checkboxes"]
        items = [(f"RED", f"Test item {i}") for i in range(max_cb + 2)]
        step = self._make_step(items)
        vi.validate_step_sizing(step, sizing_rules, r, thresholds)
        assert r.errors >= 1
        assert any("maximum" in m.lower() for m in r.error_messages)

    def test_checkbox_count_above_recommended_warns(self, sizing_rules, thresholds):
        r = CollectingReporter()
        rec = thresholds["recommended_checkboxes"]
        max_cb = thresholds["max_checkboxes"]
        # Create count between recommended and max
        count = rec + 1
        assert count <= max_cb, "Test assumes recommended < max"
        items = [("RED", f"Item {i}") for i in range(count)]
        step = self._make_step(items)
        vi.validate_step_sizing(step, sizing_rules, r, thresholds)
        assert r.warnings >= 1
        assert any("recommended" in m.lower() for m in r.warning_messages)

    def test_checkbox_count_at_recommended_no_warning(self, sizing_rules, thresholds):
        r = CollectingReporter()
        rec = thresholds["recommended_checkboxes"]
        items = [("RED", f"Item {i}") for i in range(rec)]
        step = self._make_step(items)
        vi.validate_step_sizing(step, sizing_rules, r, thresholds)
        assert r.warnings == 0

    def test_checkbox_text_too_long(self, sizing_rules, thresholds):
        r = CollectingReporter()
        max_chars = thresholds["max_checkbox_chars"]
        long_text = "x" * (max_chars + 50)
        step = self._make_step([("RED", long_text)])
        vi.validate_step_sizing(step, sizing_rules, r, thresholds)
        assert r.warnings >= 1
        assert any("chars" in m.lower() or "break" in m.lower() for m in r.warning_messages)

    def test_checkbox_text_at_limit_passes(self, sizing_rules, thresholds):
        r = CollectingReporter()
        max_chars = thresholds["max_checkbox_chars"]
        text = "x" * max_chars
        step = self._make_step([("RED", text)])
        vi.validate_step_sizing(step, sizing_rules, r, thresholds)
        assert r.warnings == 0

    def test_checkbox_text_empty_fails(self, sizing_rules, thresholds):
        r = CollectingReporter()
        step = self._make_step([("RED", "")])
        vi.validate_step_sizing(step, sizing_rules, r, thresholds)
        assert r.errors >= 1
        assert any("Empty checkbox" in m for m in r.error_messages)

    def test_tag_char_overrides(self, sizing_rules, thresholds):
        """Tags in tag_char_overrides get their own limit."""
        r = CollectingReporter()
        overrides = thresholds.get("tag_char_overrides", {})
        if "SPAWN" in overrides:
            spawn_limit = overrides["SPAWN"]
            # Text over default but under SPAWN limit should NOT warn
            default_max = thresholds["max_checkbox_chars"]
            text = "x" * (default_max + 10)
            assert len(text) < spawn_limit, "Test assumes override > default"
            step = self._make_step([("SPAWN", text)])
            vi.validate_step_sizing(step, sizing_rules, r, thresholds)
            length_warnings = [m for m in r.warning_messages if "chars" in m.lower() or "break" in m.lower()]
            assert len(length_warnings) == 0


# ─── Tag chain rule tests ───────────────────────────────────


class TestTagChains:
    """Test tag dependency and ordering rules."""

    def _make_step(self, tags_and_texts: list[tuple[str, str]]) -> vi.Step:
        return vi.Step(
            number=1,
            title="Test step",
            checkboxes=[
                vi.Checkbox(tag=t, text=txt, line=f"- [ ] `[{t}]` {txt}")
                for t, txt in tags_and_texts
            ],
        )

    def test_green_requires_red(self, chain_rules, tag_order):
        """GREEN without RED should fail."""
        r = CollectingReporter()
        step = self._make_step([("GREEN", "Implement feature"), ("AUDIT", "quality.md")])
        vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
        assert any("[GREEN] without [RED]" in m for m in r.error_messages)

    def test_green_with_red_passes(self, chain_rules, tag_order):
        """GREEN with RED should not trigger the requires error."""
        r = CollectingReporter()
        step = self._make_step([
            ("RED", "Write test"),
            ("GREEN", "Implement feature"),
            ("AUDIT", "quality.md"),
        ])
        vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
        green_red_errors = [m for m in r.error_messages if "[GREEN] without [RED]" in m]
        assert len(green_red_errors) == 0

    def test_tag_ordering_violation(self, chain_rules, tag_order):
        """Tags out of defined order should warn."""
        r = CollectingReporter()
        # GREEN before RED violates ordering
        step = self._make_step([
            ("GREEN", "Implement"),
            ("RED", "Write test"),
            ("AUDIT", "quality.md"),
        ])
        vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
        ordering_msgs = [m for m in r.warning_messages if "order" in m.lower() or "sequence" in m.lower()]
        assert len(ordering_msgs) >= 1

    def test_tag_ordering_correct(self, chain_rules, tag_order):
        """Tags in correct order should not warn about ordering."""
        r = CollectingReporter()
        step = self._make_step([
            ("RED", "Write test"),
            ("GREEN", "Implement"),
            ("INFRA", "Setup config"),
            ("WIRE", "Connect endpoint"),
            ("AUDIT", "quality.md"),
        ])
        vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
        ordering_msgs = [m for m in r.warning_messages if "out of sequence" in m]
        assert len(ordering_msgs) == 0

    def test_audit_required(self, chain_rules, tag_order):
        """Missing AUDIT should fail."""
        r = CollectingReporter()
        step = self._make_step([
            ("RED", "Write test"),
            ("GREEN", "Implement"),
        ])
        vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
        assert any("[AUDIT]" in m and "Missing" in m for m in r.error_messages)

    def test_audit_must_be_last(self, chain_rules, tag_order):
        """AUDIT not as last tag should fail."""
        r = CollectingReporter()
        step = self._make_step([
            ("RED", "Write test"),
            ("AUDIT", "quality.md"),
            ("GREEN", "Implement"),
        ])
        vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
        assert any("last checkbox" in m or "last" in m.lower() for m in r.error_messages if "AUDIT" in m)

    def test_audit_as_last_passes(self, chain_rules, tag_order):
        """AUDIT as last tag should not trigger the must_be_last error."""
        r = CollectingReporter()
        step = self._make_step([
            ("RED", "Write test"),
            ("GREEN", "Implement"),
            ("AUDIT", "quality.md"),
        ])
        vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
        audit_last_errors = [m for m in r.error_messages if "AUDIT" in m and "last" in m.lower()]
        assert len(audit_last_errors) == 0

    def test_spawn_must_be_first(self, chain_rules, tag_order):
        """SPAWN not as first tag should fail."""
        r = CollectingReporter()
        step = self._make_step([
            ("RED", "Write test"),
            ("SPAWN", "Delegate to sub-agent"),
            ("REVIEW", "Validate output"),
            ("AUDIT", "quality.md"),
        ])
        vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
        assert any("SPAWN" in m and "first" in m.lower() for m in r.error_messages)

    def test_spawn_as_first_passes(self, chain_rules, tag_order):
        """SPAWN as first tag should not trigger the must_be_first error."""
        r = CollectingReporter()
        step = self._make_step([
            ("SPAWN", "Delegate to sub-agent"),
            ("RED", "Write test"),
            ("GREEN", "Implement"),
            ("REVIEW", "Validate output"),
            ("AUDIT", "quality.md"),
        ])
        vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
        spawn_first_errors = [m for m in r.error_messages if "SPAWN" in m and "first" in m.lower()]
        assert len(spawn_first_errors) == 0

    def test_spawn_requires_review(self, chain_rules, tag_order):
        """SPAWN without REVIEW should fail."""
        r = CollectingReporter()
        step = self._make_step([
            ("SPAWN", "Delegate to sub-agent"),
            ("RED", "Write test"),
            ("GREEN", "Implement"),
            ("AUDIT", "quality.md"),
        ])
        vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
        assert any("[SPAWN] without [REVIEW]" in m for m in r.error_messages)

    def test_review_recommended_with_green(self, chain_rules, tag_order):
        """Missing REVIEW when GREEN is present should warn."""
        r = CollectingReporter()
        step = self._make_step([
            ("RED", "Write test"),
            ("GREEN", "Implement"),
            ("AUDIT", "quality.md"),
        ])
        vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
        review_warns = [m for m in r.warning_messages if "REVIEW" in m]
        assert len(review_warns) >= 1

    def test_e2e_requires_pw(self, chain_rules, tag_order):
        """E2E without PW should fail."""
        r = CollectingReporter()
        step = self._make_step([
            ("RED", "Write test"),
            ("GREEN", "Implement"),
            ("E2E", "Write Playwright spec"),
            ("AUDIT", "quality.md"),
        ])
        vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
        assert any("[E2E] without [PW]" in m for m in r.error_messages)

    def test_tag_recommended_with_docs(self, chain_rules, tag_order):
        """Missing DOCS when GREEN is present should warn."""
        r = CollectingReporter()
        step = self._make_step([
            ("RED", "Write test"),
            ("GREEN", "Implement"),
            ("AUDIT", "quality.md"),
        ])
        vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
        docs_warns = [m for m in r.warning_messages if "DOCS" in m]
        assert len(docs_warns) >= 1

    def test_infra_only_step_no_green_red_errors(self, chain_rules, tag_order):
        """INFRA-only step should not require RED/GREEN."""
        r = CollectingReporter()
        step = self._make_step([
            ("INFRA", "Set up database tables"),
            ("AUDIT", "quality.md"),
        ])
        vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
        green_red_errors = [m for m in r.error_messages if "[GREEN] without [RED]" in m]
        assert len(green_red_errors) == 0


# ─── Tag semantic tests ─────────────────────────────────────


class TestTagSemantics:
    """Test per-tag content validation rules."""

    def _make_step(self, tags_and_texts: list[tuple[str, str]]) -> vi.Step:
        return vi.Step(
            number=1,
            title="Test step",
            checkboxes=[
                vi.Checkbox(tag=t, text=txt, line=f"- [ ] `[{t}]` {txt}")
                for t, txt in tags_and_texts
            ],
        )

    def test_red_mentions_test(self, semantic_rules):
        """RED tag must mention test/spec."""
        r = CollectingReporter()
        step = self._make_step([("RED", "Write failing test for login")])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        red_errors = [m for m in r.error_messages if "RED" in m and "test" in m.lower()]
        assert len(red_errors) == 0

    def test_red_without_test_fails(self, semantic_rules):
        """RED tag not mentioning test should fail."""
        r = CollectingReporter()
        step = self._make_step([("RED", "Implement the login feature")])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        assert any("[RED]" in m and "test" in m.lower() for m in r.error_messages)

    def test_red_matches_spec(self, semantic_rules):
        """RED should also accept 'spec' as valid."""
        r = CollectingReporter()
        step = self._make_step([("RED", "Write failing spec for auth module")])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        red_content_errors = [m for m in r.error_messages if "[RED]" in m and "test" in m.lower()]
        assert len(red_content_errors) == 0

    def test_red_matches_dot_test(self, semantic_rules):
        """RED should accept '.test' pattern."""
        r = CollectingReporter()
        step = self._make_step([("RED", "Create login.test.ts")])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        red_content_errors = [m for m in r.error_messages if "[RED]" in m and "test" in m.lower()]
        assert len(red_content_errors) == 0

    def test_no_consecutive_red_without_green(self, semantic_rules):
        """Two consecutive RED without GREEN between them should fail."""
        r = CollectingReporter()
        step = self._make_step([
            ("RED", "Write test for feature A"),
            ("RED", "Write test for feature B"),
            ("GREEN", "Implement both"),
        ])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        assert any("RED" in m and "without [GREEN]" in m for m in r.error_messages)

    def test_red_green_red_green_passes(self, semantic_rules):
        """Alternating RED-GREEN-RED-GREEN should not trigger consecutive error."""
        r = CollectingReporter()
        step = self._make_step([
            ("RED", "Write test for feature A"),
            ("GREEN", "Implement feature A"),
            ("RED", "Write test for feature B"),
            ("GREEN", "Implement feature B"),
        ])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        consecutive_errors = [m for m in r.error_messages if "RED" in m and "without [GREEN]" in m]
        assert len(consecutive_errors) == 0

    def test_green_before_red_fails(self, semantic_rules):
        """GREEN appearing before any RED should fail."""
        r = CollectingReporter()
        step = self._make_step([
            ("GREEN", "Implement first"),
            ("RED", "Write test after"),
        ])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        assert any("[GREEN] appears before [RED]" in m for m in r.error_messages)

    def test_green_after_red_passes(self, semantic_rules):
        """GREEN after RED should not trigger the before error."""
        r = CollectingReporter()
        step = self._make_step([
            ("RED", "Write failing test"),
            ("GREEN", "Implement to pass"),
        ])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        before_errors = [m for m in r.error_messages if "before [RED]" in m]
        assert len(before_errors) == 0

    def test_green_mentions_writing_tests_warns(self, semantic_rules):
        """GREEN mentioning 'write test' should warn."""
        r = CollectingReporter()
        step = self._make_step([("GREEN", "Write test for the component")])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        assert any("[GREEN]" in m and "tests" in m.lower() for m in r.warning_messages)

    def test_green_normal_text_no_warn(self, semantic_rules):
        """GREEN with normal implementation text should not warn."""
        r = CollectingReporter()
        step = self._make_step([("GREEN", "Implement the login endpoint")])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        green_test_warns = [m for m in r.warning_messages if "[GREEN]" in m and "test" in m.lower()]
        assert len(green_test_warns) == 0

    def test_wire_mentions_integration(self, semantic_rules):
        """WIRE mentioning integration should pass."""
        r = CollectingReporter()
        step = self._make_step([("WIRE", "Connect frontend to backend endpoint")])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        wire_warns = [m for m in r.warning_messages if "[WIRE]" in m and "integration" in m.lower()]
        assert len(wire_warns) == 0

    def test_wire_without_integration_warns(self, semantic_rules):
        """WIRE not mentioning integration/connection should warn."""
        r = CollectingReporter()
        step = self._make_step([("WIRE", "Refactor the module structure")])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        assert any("[WIRE]" in m and "integration" in m.lower() for m in r.warning_messages)

    def test_e2e_mentions_test(self, semantic_rules):
        """E2E mentioning test should pass."""
        r = CollectingReporter()
        step = self._make_step([("E2E", "Write Playwright spec for login")])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        e2e_errors = [m for m in r.error_messages if "[E2E]" in m and "test" in m.lower()]
        assert len(e2e_errors) == 0

    def test_e2e_without_test_fails(self, semantic_rules):
        """E2E not mentioning test/spec should fail."""
        r = CollectingReporter()
        step = self._make_step([("E2E", "Check the login flow visually")])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        assert any("[E2E]" in m and "test" in m.lower() for m in r.error_messages)

    def test_no_duplicate_checkboxes(self, semantic_rules):
        """Duplicate checkbox text should fail."""
        r = CollectingReporter()
        step = self._make_step([
            ("RED", "Write test for login"),
            ("RED", "Write test for login"),
        ])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        assert any("Duplicate" in m for m in r.error_messages)

    def test_unique_checkboxes_pass(self, semantic_rules):
        """Unique checkbox texts should not trigger duplicate error."""
        r = CollectingReporter()
        step = self._make_step([
            ("RED", "Write test for login"),
            ("RED", "Write test for registration"),
        ])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        dup_errors = [m for m in r.error_messages if "Duplicate" in m]
        assert len(dup_errors) == 0

    def test_infra_writing_tests_warns(self, semantic_rules):
        """INFRA mentioning 'write test' should warn."""
        r = CollectingReporter()
        step = self._make_step([("INFRA", "Write test for the database setup")])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        assert any("[INFRA]" in m and "test" in m.lower() for m in r.warning_messages)

    def test_audit_mentions_quality(self, semantic_rules):
        """AUDIT mentioning quality.md should pass."""
        r = CollectingReporter()
        step = self._make_step([("AUDIT", "Run quality.md audit")])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        audit_warns = [m for m in r.warning_messages if "[AUDIT]" in m and "quality" in m.lower()]
        assert len(audit_warns) == 0

    def test_audit_without_quality_warns(self, semantic_rules):
        """AUDIT not mentioning quality.md should warn."""
        r = CollectingReporter()
        step = self._make_step([("AUDIT", "Check everything is fine")])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        assert any("[AUDIT]" in m and "quality" in m.lower() for m in r.warning_messages)

    def test_last_audit_references_quality(self, semantic_rules):
        """Last AUDIT in step should reference quality.md."""
        r = CollectingReporter()
        step = self._make_step([
            ("AUDIT", "Audit code structure"),
            ("AUDIT", "Run quality.md review"),
        ])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        last_audit_warns = [m for m in r.warning_messages if "Last [AUDIT]" in m]
        assert len(last_audit_warns) == 0

    def test_last_audit_without_quality_warns(self, semantic_rules):
        """Last AUDIT not referencing quality.md should warn."""
        r = CollectingReporter()
        step = self._make_step([
            ("AUDIT", "Run quality.md review"),
            ("AUDIT", "General code check"),
        ])
        vi.validate_step_tag_semantics(step, semantic_rules, r)
        assert any("Last [AUDIT]" in m for m in r.warning_messages)


# ─── Integration tests (full parse + validate) ──────────────


class TestIntegration:
    """End-to-end tests: parse body then run all validation sections."""

    def _validate_body(
        self, body: str, config: dict
    ) -> CollectingReporter:
        steps = vi.parse_steps(body)
        r = CollectingReporter()
        thresholds = config["thresholds"]
        tag_order = config["tag_order"]
        sections = config["sections"]

        for rule in sections["structure"]["rules"]:
            match rule["type"]:
                case "body_match":
                    vi.handle_body_match(rule, body, steps, r)
                case "section_has_checkboxes":
                    vi.handle_section_has_checkboxes(rule, body, steps, r)
                case "step_count":
                    vi.handle_step_count(rule, body, steps, r, thresholds)
                case "step_numbering":
                    vi.handle_step_numbering(rule, body, steps, r)
                case "step_title_format":
                    vi.handle_step_title_format(rule, body, steps, r)

        sizing_rules = sections["sizing"]["rules"]
        chain_rules = sections["tag_chains"]["rules"]
        semantic_rules = sections["tag_semantics"]["rules"]

        for step in steps:
            vi.validate_step_sizing(step, sizing_rules, r, thresholds)
            vi.validate_step_tag_chains(step, chain_rules, r, tag_order)
            vi.validate_step_tag_semantics(step, semantic_rules, r)

        return r

    def test_valid_issue_has_no_errors(self, config):
        r = self._validate_body(VALID_ISSUE_BODY, config)
        assert r.errors == 0, f"Expected 0 errors, got: {r.error_messages}"

    def test_minimal_valid_issue_has_no_errors(self, config):
        r = self._validate_body(MINIMAL_VALID_BODY, config)
        assert r.errors == 0, f"Expected 0 errors, got: {r.error_messages}"

    def test_empty_body_has_errors(self, config):
        r = self._validate_body("", config)
        assert r.errors > 0

    def test_missing_all_sections(self, config):
        body = "Just some text with no structure at all."
        r = self._validate_body(body, config)
        # Should fail for missing What, Why, Acceptance criteria, and step count
        assert r.errors >= 3

    def test_body_with_only_structure_no_steps(self, config):
        body = """\
## What

Something.

## Why

Because.

## Acceptance criteria

- [ ] It works
"""
        r = self._validate_body(body, config)
        # Should fail for too few steps (0 < min)
        assert any("Too few" in m for m in r.error_messages)

    def test_body_with_misordered_tags(self, config):
        body = """\
## What

Feature.

## Why

Reason.

## Acceptance criteria

- [ ] Done

## Step 1 — First

- [ ] `[GREEN]` Implement first
- [ ] `[RED]` Then write test
- [ ] `[AUDIT]` Run quality.md audit

## Step 2 — Second

- [ ] `[INFRA]` Setup
- [ ] `[AUDIT]` Run quality.md audit
"""
        r = self._validate_body(body, config)
        # Should have errors for GREEN before RED and ordering
        assert r.errors > 0

    def test_body_with_gap_in_numbering(self, config):
        body = """\
## What

Feature.

## Why

Reason.

## Acceptance criteria

- [ ] Done

## Step 1 — First

- [ ] `[INFRA]` Setup
- [ ] `[AUDIT]` Run quality.md audit

## Step 3 — Third

- [ ] `[INFRA]` More setup
- [ ] `[AUDIT]` Run quality.md audit
"""
        r = self._validate_body(body, config)
        assert any("Step" in m and ("gap" in m.lower() or "expected" in m.lower()) for m in r.error_messages)


# ─── Reporter tests ─────────────────────────────────────────


class TestReporter:
    """Test the Reporter.emit dispatcher."""

    def test_emit_error(self):
        r = CollectingReporter()
        r.emit("error", "Something failed")
        assert r.errors == 1
        assert "Something failed" in r.error_messages

    def test_emit_warn(self):
        r = CollectingReporter()
        r.emit("warn", "Something warned")
        assert r.warnings == 1
        assert "Something warned" in r.warning_messages

    def test_emit_off_suppresses(self):
        r = CollectingReporter()
        r.emit("off", "Suppressed message")
        assert r.errors == 0
        assert r.warnings == 0
        assert any("suppressed" in m.lower() for m in r.passed_messages)
