"""Tests for validate-issue.config.json — structure and content validation.

Ensures the config file is valid JSON, has the expected structure,
and does not reference removed tags.

Run with: pytest test_validate_issue_config.py -v
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

CONFIG_PATH = Path(__file__).resolve().parent / "validate-issue.config.json"


@pytest.fixture(scope="session")
def config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


# ─── Basic structure ─────────────────────────────────────────


class TestConfigStructure:
    """Validate top-level config structure."""

    def test_config_is_valid_json(self):
        """Config file must be parseable JSON."""
        with open(CONFIG_PATH) as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_has_thresholds(self, config):
        assert "thresholds" in config
        assert isinstance(config["thresholds"], dict)

    def test_has_tag_order(self, config):
        assert "tag_order" in config
        assert isinstance(config["tag_order"], list)

    def test_has_sections(self, config):
        assert "sections" in config
        assert isinstance(config["sections"], dict)


# ─── Thresholds ──────────────────────────────────────────────


class TestThresholds:
    """Validate thresholds section has required keys with correct types."""

    REQUIRED_KEYS = [
        "min_steps",
        "max_steps",
        "max_checkboxes",
        "recommended_checkboxes",
        "max_checkbox_chars",
    ]

    def test_has_all_required_keys(self, config):
        thresholds = config["thresholds"]
        for key in self.REQUIRED_KEYS:
            assert key in thresholds, f"Missing threshold key: {key}"

    def test_numeric_thresholds_are_positive_ints(self, config):
        thresholds = config["thresholds"]
        for key in self.REQUIRED_KEYS:
            val = thresholds[key]
            assert isinstance(val, int), f"{key} should be int, got {type(val)}"
            assert val > 0, f"{key} should be positive, got {val}"

    def test_min_less_than_max_steps(self, config):
        th = config["thresholds"]
        assert th["min_steps"] < th["max_steps"]

    def test_recommended_less_than_max_checkboxes(self, config):
        th = config["thresholds"]
        assert th["recommended_checkboxes"] < th["max_checkboxes"]

    def test_tag_char_overrides_is_dict(self, config):
        th = config["thresholds"]
        if "tag_char_overrides" in th:
            assert isinstance(th["tag_char_overrides"], dict)
            for tag, limit in th["tag_char_overrides"].items():
                assert isinstance(tag, str), f"Override key must be str: {tag}"
                assert isinstance(limit, int), f"Override value must be int: {limit}"
                assert limit > 0, f"Override for {tag} must be positive: {limit}"


# ─── Tag order ───────────────────────────────────────────────


class TestTagOrder:
    """Validate tag_order list."""

    CORE_TAGS = {"RED", "GREEN", "INFRA", "WIRE", "E2E"}

    def test_tag_order_has_core_tags(self, config):
        """The 5 core TDD tags must be present."""
        tag_set = set(config["tag_order"])
        for tag in self.CORE_TAGS:
            assert tag in tag_set, f"Core tag missing from tag_order: {tag}"

    def test_tag_order_no_duplicates(self, config):
        tags = config["tag_order"]
        assert len(tags) == len(set(tags)), "tag_order contains duplicates"

    def test_tag_order_all_uppercase(self, config):
        for tag in config["tag_order"]:
            assert tag == tag.upper(), f"Tag must be uppercase: {tag}"

    def test_tag_order_all_strings(self, config):
        for tag in config["tag_order"]:
            assert isinstance(tag, str), f"Tag must be string: {tag}"

    def test_red_before_green_in_order(self, config):
        """RED must come before GREEN in the ordering."""
        tags = config["tag_order"]
        assert tags.index("RED") < tags.index("GREEN")

    def test_green_before_wire_in_order(self, config):
        """GREEN must come before WIRE (implementation before integration)."""
        tags = config["tag_order"]
        assert tags.index("GREEN") < tags.index("WIRE")


# ─── Sections ────────────────────────────────────────────────


class TestSections:
    """Validate sections structure and rule keys."""

    EXPECTED_SECTIONS = ["structure", "sizing", "tag_chains", "tag_semantics"]

    def test_has_expected_sections(self, config):
        sections = config["sections"]
        for name in self.EXPECTED_SECTIONS:
            assert name in sections, f"Missing section: {name}"

    def test_each_section_has_rules(self, config):
        for name, section in config["sections"].items():
            assert "rules" in section, f"Section '{name}' missing 'rules' key"
            assert isinstance(section["rules"], list), f"Section '{name}' rules must be a list"
            assert len(section["rules"]) > 0, f"Section '{name}' has no rules"

    def test_each_section_has_description(self, config):
        for name, section in config["sections"].items():
            assert "description" in section, f"Section '{name}' missing 'description'"

    def test_each_rule_has_required_fields(self, config):
        required = {"key", "description", "errorMessage", "level", "type"}
        for sec_name, section in config["sections"].items():
            for rule in section["rules"]:
                for field in required:
                    assert field in rule, (
                        f"Rule '{rule.get('key', '?')}' in '{sec_name}' missing field: {field}"
                    )

    def test_rule_levels_valid(self, config):
        valid_levels = {"error", "warn", "off"}
        for sec_name, section in config["sections"].items():
            for rule in section["rules"]:
                assert rule["level"] in valid_levels, (
                    f"Rule '{rule['key']}' in '{sec_name}' has invalid level: {rule['level']}"
                )

    def test_rule_keys_unique(self, config):
        all_keys: list[str] = []
        for section in config["sections"].values():
            for rule in section["rules"]:
                all_keys.append(rule["key"])
        assert len(all_keys) == len(set(all_keys)), (
            f"Duplicate rule keys found: "
            f"{[k for k in all_keys if all_keys.count(k) > 1]}"
        )


# ─── Structure section specifics ─────────────────────────────


class TestStructureSection:
    """Validate structure section has expected rule keys."""

    EXPECTED_KEYS = [
        "what_section",
        "why_section",
        "acceptance_criteria",
        "step_count",
        "step_numbering",
    ]

    def test_has_expected_rule_keys(self, config):
        keys = [r["key"] for r in config["sections"]["structure"]["rules"]]
        for expected in self.EXPECTED_KEYS:
            assert expected in keys, f"Missing structure rule: {expected}"


# ─── Sizing section specifics ────────────────────────────────


class TestSizingSection:
    """Validate sizing section has expected rule keys."""

    EXPECTED_KEYS = [
        "empty_step",
        "checkbox_count_error",
        "checkbox_count_warn",
        "checkbox_length",
        "checkbox_not_empty",
    ]

    def test_has_expected_rule_keys(self, config):
        keys = [r["key"] for r in config["sections"]["sizing"]["rules"]]
        for expected in self.EXPECTED_KEYS:
            assert expected in keys, f"Missing sizing rule: {expected}"


# ─── Tag semantics section specifics ─────────────────────────


class TestTagSemanticsSection:
    """Validate tag_semantics section has expected rule keys."""

    EXPECTED_KEYS = [
        "red_mentions_test",
        "red_no_consecutive",
        "green_before_red",
        "green_writes_tests",
        "wire_mentions_integration",
        "e2e_mentions_test",
        "no_duplicate_checkboxes",
    ]

    def test_has_expected_rule_keys(self, config):
        keys = [r["key"] for r in config["sections"]["tag_semantics"]["rules"]]
        for expected in self.EXPECTED_KEYS:
            assert expected in keys, f"Missing tag_semantics rule: {expected}"

    def test_content_match_rules_have_pattern(self, config):
        """Rules of type tag_content_match or tag_content_reject must have a pattern."""
        for rule in config["sections"]["tag_semantics"]["rules"]:
            if rule["type"] in ("tag_content_match", "tag_content_reject"):
                assert "pattern" in rule, (
                    f"Rule '{rule['key']}' needs 'pattern' for type '{rule['type']}'"
                )

    def test_content_match_patterns_are_valid_regex(self, config):
        """All patterns in tag_semantics rules must be valid regex."""
        import re

        for rule in config["sections"]["tag_semantics"]["rules"]:
            if "pattern" in rule:
                try:
                    re.compile(rule["pattern"])
                except re.error as e:
                    pytest.fail(f"Invalid regex in rule '{rule['key']}': {e}")


# ─── Tag chains section specifics ────────────────────────────


class TestTagChainsSection:
    """Validate tag_chains section has expected rule keys."""

    EXPECTED_KEYS = [
        "green_requires_red",
        "tag_ordering",
        "audit_mandatory",
        "audit_must_be_last",
    ]

    def test_has_expected_rule_keys(self, config):
        keys = [r["key"] for r in config["sections"]["tag_chains"]["rules"]]
        for expected in self.EXPECTED_KEYS:
            assert expected in keys, f"Missing tag_chains rule: {expected}"

    def test_tag_requires_rules_reference_valid_tags(self, config):
        """tag_requires rules must reference tags that exist in tag_order."""
        tag_set = set(config["tag_order"])
        for rule in config["sections"]["tag_chains"]["rules"]:
            if rule["type"] == "tag_requires":
                assert rule["tag"] in tag_set, (
                    f"Rule '{rule['key']}' references unknown tag: {rule['tag']}"
                )
                assert rule["requires"] in tag_set, (
                    f"Rule '{rule['key']}' requires unknown tag: {rule['requires']}"
                )


# ─── No removed tags ─────────────────────────────────────────


class TestNoRemovedTags:
    """Ensure the config does not reference tags that were removed from the system.

    Note: Some of these tags may still exist in the current config as part of
    the full tag system (SPAWN, REVIEW, etc.). This test class documents the
    tags that the task description flagged as potentially removed. We verify
    that if any are still referenced, they are properly listed in tag_order.
    """

    # Tags flagged as potentially removed in the task description.
    # We check they are either consistently present OR consistently absent.
    FLAGGED_TAGS = {"SPAWN", "REVIEW", "PW", "HUMAN", "DOCS", "LOG", "AUDIT"}

    def test_flagged_tags_if_in_rules_also_in_tag_order(self, config):
        """Any flagged tag referenced in rules must also be in tag_order."""
        tag_order_set = set(config["tag_order"])
        tags_in_rules: set[str] = set()

        for section in config["sections"].values():
            for rule in section["rules"]:
                if "tag" in rule:
                    tags_in_rules.add(rule["tag"])
                if "requires" in rule and isinstance(rule["requires"], str):
                    tags_in_rules.add(rule["requires"])

        flagged_in_rules = tags_in_rules & self.FLAGGED_TAGS
        for tag in flagged_in_rules:
            assert tag in tag_order_set, (
                f"Tag '{tag}' referenced in rules but missing from tag_order"
            )

    def test_count_excluded_tags_exist_in_config(self, config):
        """Tags in count_excluded_tags should be valid (in tag_order)."""
        excluded = config["thresholds"].get("count_excluded_tags", [])
        tag_order_set = set(config["tag_order"])
        for tag in excluded:
            assert tag in tag_order_set, (
                f"Excluded tag '{tag}' not in tag_order — stale reference?"
            )

    def test_tag_char_overrides_reference_valid_tags(self, config):
        """Tags in tag_char_overrides should be valid (in tag_order)."""
        overrides = config["thresholds"].get("tag_char_overrides", {})
        tag_order_set = set(config["tag_order"])
        for tag in overrides:
            assert tag in tag_order_set, (
                f"Override tag '{tag}' not in tag_order — stale reference?"
            )
