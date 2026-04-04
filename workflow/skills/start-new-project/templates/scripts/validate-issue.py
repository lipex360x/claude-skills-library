#!/usr/bin/env python3
"""Validate issue checkbox tags against development rules.

Data-driven validator — all rules, messages, and levels live in
validate-issue.config.json. This script is the engine; the JSON is the brain.

Usage:
    validate-issue.py <issue-number>            Validate and report
    validate-issue.py <issue-number> --verbose  Show passing checks too
    validate-issue.py --help                    Show this help
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ─── Types ────────────────────────────────────────────────


@dataclass
class Checkbox:
    tag: str
    text: str
    line: str


@dataclass
class Step:
    number: int
    title: str
    checkboxes: list[Checkbox] = field(default_factory=list)

    @property
    def tags(self) -> list[str]:
        return [cb.tag for cb in self.checkboxes]


# ─── Output ───────────────────────────────────────────────

USE_COLOR = sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


class Reporter:
    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        self.errors = 0
        self.warnings = 0

    def section(self, title: str) -> None:
        print(f"\n{_c('0;36', title)}")

    def passed(self, msg: str) -> None:
        if self.verbose:
            print(f"{_c('0;32', '  ✓')} {msg}")

    def warn(self, msg: str) -> None:
        print(f"{_c('1;33', '  ⚠')} {msg}")
        self.warnings += 1

    def fail(self, msg: str) -> None:
        print(f"{_c('0;31', '  ✗')} {msg}")
        self.errors += 1

    def emit(self, level: str, msg: str) -> None:
        match level:
            case "error":
                self.fail(msg)
            case "warn":
                self.warn(msg)
            case "off":
                self.passed(f"{msg} (suppressed)")


# ─── Config ───────────────────────────────────────────────


def load_config(script_dir: Path) -> dict:
    config_path = script_dir / "validate-issue.config.json"
    if not config_path.exists():
        print(f"{_c('0;31', '[error]')} Config not found: {config_path}")
        sys.exit(1)
    with open(config_path) as f:
        return json.load(f)


# ─── Issue fetching ───────────────────────────────────────


def fetch_issue_body(issue_number: str) -> str:
    result = subprocess.run(
        ["gh", "issue", "view", issue_number, "--json", "body", "-q", ".body"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        print(f"{_c('0;31', '[error]')} Could not fetch issue #{issue_number}")
        sys.exit(1)
    return result.stdout.strip()


# ─── Parsing ──────────────────────────────────────────────

STEP_HEADER_RE = re.compile(r"^## Step (\d+)\s*[—–-]\s*(.+)$")
CHECKBOX_RE = re.compile(r"^- \[.\] `\[([A-Z0-9]+)\]`\s*(.*)")


def parse_steps(body: str) -> list[Step]:
    steps: list[Step] = []
    current: Step | None = None

    for line in body.splitlines():
        header = STEP_HEADER_RE.match(line)
        if header:
            current = Step(number=int(header.group(1)), title=header.group(2).strip())
            steps.append(current)
            continue

        if current is None:
            continue

        cb = CHECKBOX_RE.match(line)
        if cb:
            current.checkboxes.append(
                Checkbox(tag=cb.group(1), text=cb.group(2).strip(), line=line)
            )

    return steps


# ─── Rule handlers ────────────────────────────────────────
# Each handler receives (rule_config, context) and returns violations.
# Context varies by rule scope: body-level, step-level, or checkbox-level.


def handle_body_match(rule: dict, body: str, _steps: list[Step], r: Reporter) -> None:
    if re.search(rule["pattern"], body, re.MULTILINE):
        r.passed(rule["description"])
    else:
        r.emit(rule["level"], rule["errorMessage"])


def handle_section_has_checkboxes(
    rule: dict, body: str, _steps: list[Step], r: Reporter
) -> None:
    section_name = rule["section"]
    in_section = False
    count = 0
    for line in body.splitlines():
        if line.startswith(section_name):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and re.match(r"^- \[", line):
            count += 1
    if count > 0:
        r.passed(f"{rule['description']}: {count} checkbox(es)")
    else:
        r.emit(rule["level"], rule["errorMessage"])


def handle_step_count(
    rule: dict, _body: str, steps: list[Step], r: Reporter, thresholds: dict
) -> None:
    count = len(steps)
    min_s = thresholds.get("min_steps", 2)
    max_s = thresholds.get("max_steps", 8)
    if count < min_s:
        msg = rule["errorMessage"].format(actual=count, min=min_s, max=max_s)
        r.emit(rule["level"], f"Too few steps ({count}) — minimum is {min_s}")
    elif count > max_s:
        r.emit(
            rule["level"],
            f"Too many steps ({count}) — maximum is {max_s}, split into multiple issues",
        )
    else:
        r.passed(f"Step count: {count} (within {min_s}-{max_s})")


def handle_step_numbering(
    rule: dict, _body: str, steps: list[Step], r: Reporter
) -> None:
    for i, step in enumerate(steps):
        expected = i + 1
        if step.number != expected:
            msg = rule["errorMessage"].format(expected=expected, actual=step.number)
            r.emit(rule["level"], msg)
            return
    r.passed("Step numbering: sequential")


def handle_step_title_format(
    rule: dict, body: str, _steps: list[Step], r: Reporter
) -> None:
    for line in body.splitlines():
        if re.match(r"^## Step \d+", line) and "—" not in line:
            step_n = re.search(r"\d+", line)
            num = step_n.group() if step_n else "?"
            msg = rule["errorMessage"].format(step=num)
            r.emit(rule["level"], msg)


# ─── Step-level rule handlers ─────────────────────────────


def validate_step_sizing(step: Step, rules: list[dict], r: Reporter, th: dict) -> None:
    max_cb = th.get("max_checkboxes", 8)
    rec_cb = th.get("recommended_checkboxes", 6)
    max_chars = th.get("max_checkbox_chars", 200)
    count = len(step.checkboxes)

    for rule in rules:
        match rule["type"]:
            case "step_not_empty":
                if count == 0:
                    r.emit(rule["level"], rule["errorMessage"])
                    return
            case "checkbox_count_max":
                if count > max_cb:
                    msg = rule["errorMessage"].format(count=count, max=max_cb)
                    r.emit(rule["level"], msg)
            case "checkbox_count_recommended":
                if rec_cb < count <= max_cb:
                    msg = rule["errorMessage"].format(
                        count=count, recommended=rec_cb
                    )
                    r.emit(rule["level"], msg)
            case "checkbox_text_length":
                tag_char_overrides = th.get("tag_char_overrides", {})
                for cb in step.checkboxes:
                    limit = tag_char_overrides.get(cb.tag, max_chars)
                    if len(cb.text) > limit:
                        msg = rule["errorMessage"].format(
                            max=limit, preview=cb.text[:60]
                        )
                        r.emit(rule["level"], msg)
            case "checkbox_text_not_empty":
                for cb in step.checkboxes:
                    if not cb.text:
                        msg = rule["errorMessage"].format(tag=cb.tag)
                        r.emit(rule["level"], msg)


def validate_step_tag_chains(
    step: Step, rules: list[dict], r: Reporter, tag_order: list[str]
) -> None:
    tags = step.tags
    tag_set = set(tags)

    has_frontend_ui = False

    for rule in rules:
        match rule["type"]:
            case "tag_requires":
                if rule["tag"] in tag_set and rule["requires"] not in tag_set:
                    r.emit(rule["level"], rule["errorMessage"])

            case "tag_required":
                if rule["tag"] not in tag_set:
                    r.emit(rule["level"], rule["errorMessage"])

            case "tag_must_be_last":
                if rule["tag"] in tag_set and tags and tags[-1] != rule["tag"]:
                    msg = rule["errorMessage"].format(last=tags[-1])
                    r.emit(rule["level"], msg)

            case "tag_must_be_first":
                if rule["tag"] in tag_set and tags and tags[0] != rule["tag"]:
                    msg = rule["errorMessage"].format(first=tags[0])
                    r.emit(rule["level"], msg)

            case "tag_ordering":
                order_map = {t: i for i, t in enumerate(tag_order)}
                prev_pos = -1
                for tag in tags:
                    pos = order_map.get(tag, -1)
                    if pos >= 0 and pos < prev_pos:
                        order_str = " → ".join(tag_order)
                        msg = rule["errorMessage"].format(tag=tag, order=order_str)
                        r.emit(rule["level"], msg)
                    if pos >= 0:
                        prev_pos = pos

            case "tag_recommended_with":
                when_any = rule.get("when_any", [])
                if any(t in tag_set for t in when_any) and rule["tag"] not in tag_set:
                    r.emit(rule["level"], rule["errorMessage"])

            case "ui_chain":
                ui_patterns = rule.get("ui_patterns", [])
                combined = "|".join(ui_patterns)
                for cb in step.checkboxes:
                    if cb.tag in ("GREEN", "WIRE") and re.search(
                        combined, cb.text, re.IGNORECASE
                    ):
                        has_frontend_ui = True
                        break
                if has_frontend_ui:
                    required = rule.get("required_tags", [])
                    reasons = {"E2E": "E2E tests", "PW": "visual verification", "HUMAN": "human approval"}
                    for req in required:
                        if req not in tag_set:
                            msg = rule["errorMessage"].format(
                                missing=req, reason=reasons.get(req, req)
                            )
                            r.emit(rule["level"], msg)


def validate_step_tag_semantics(
    step: Step, rules: list[dict], r: Reporter
) -> None:
    tags = step.tags
    last_red_or_green = ""

    for rule in rules:
        match rule["type"]:
            case "tag_content_match":
                for cb in step.checkboxes:
                    if cb.tag == rule["tag"] and not re.search(
                        rule["pattern"], cb.line, re.IGNORECASE
                    ):
                        r.emit(rule["level"], rule["errorMessage"])

            case "tag_content_reject":
                for cb in step.checkboxes:
                    if cb.tag == rule["tag"] and re.search(
                        rule["pattern"], cb.line, re.IGNORECASE
                    ):
                        r.emit(rule["level"], rule["errorMessage"])

            case "tag_no_consecutive":
                prev = ""
                for cb in step.checkboxes:
                    if cb.tag == rule["tag"] and prev == rule["tag"]:
                        r.emit(rule["level"], rule["errorMessage"])
                    if cb.tag in (rule["tag"], rule["separator"]):
                        prev = cb.tag

            case "tag_requires_before":
                seen_required = False
                for cb in step.checkboxes:
                    if cb.tag == rule["requires"]:
                        seen_required = True
                    if cb.tag == rule["tag"] and not seen_required:
                        r.emit(rule["level"], rule["errorMessage"])
                        break

            case "last_tag_content_match":
                matching = [cb for cb in step.checkboxes if cb.tag == rule["tag"]]
                if matching:
                    last = matching[-1]
                    if not re.search(rule["pattern"], last.line, re.IGNORECASE):
                        r.emit(rule["level"], rule["errorMessage"])

            case "no_duplicates":
                texts = [cb.text for cb in step.checkboxes]
                seen: set[str] = set()
                for t in texts:
                    if t in seen:
                        msg = rule["errorMessage"].format(text=t)
                        r.emit(rule["level"], msg)
                        break
                    seen.add(t)


# ─── Main ─────────────────────────────────────────────────


def main() -> None:
    verbose = "--verbose" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("-")]

    if not args:
        print(f"{_c('0;31', '[error]')} Usage: validate-issue.py <issue-number> [--verbose]")
        sys.exit(1)

    issue_number = args[0]
    script_dir = Path(__file__).resolve().parent
    config = load_config(script_dir)
    thresholds = config.get("thresholds", {})
    tag_order = config.get("tag_order", [])
    sections = config.get("sections", {})

    body = fetch_issue_body(issue_number)
    steps = parse_steps(body)
    r = Reporter(verbose=verbose)

    r.section(f"Validating issue #{issue_number}")

    # ── Structure rules (issue-level) ─────────────────────
    for rule in sections.get("structure", {}).get("rules", []):
        match rule["type"]:
            case "body_match":
                handle_body_match(rule, body, steps, r)
            case "section_has_checkboxes":
                handle_section_has_checkboxes(rule, body, steps, r)
            case "step_count":
                handle_step_count(rule, body, steps, r, thresholds)
            case "step_numbering":
                handle_step_numbering(rule, body, steps, r)
            case "step_title_format":
                handle_step_title_format(rule, body, steps, r)

    # ── Per-step rules ────────────────────────────────────
    sizing_rules = sections.get("sizing", {}).get("rules", [])
    chain_rules = sections.get("tag_chains", {}).get("rules", [])
    semantic_rules = sections.get("tag_semantics", {}).get("rules", [])

    for step in steps:
        r.section(f"Step {step.number} — {step.title}")
        validate_step_sizing(step, sizing_rules, r, thresholds)
        validate_step_tag_chains(step, chain_rules, r, tag_order)
        validate_step_tag_semantics(step, semantic_rules, r)

    # ── Summary ───────────────────────────────────────────
    r.section("Summary")
    print(f"  Errors:   {_c('0;31', str(r.errors))}")
    print(f"  Warnings: {_c('1;33', str(r.warnings))}")
    config_path = script_dir / "validate-issue.config.json"
    print(f"  Config:   {_c('0;36', str(config_path))}")

    if r.errors > 0:
        print(f"\n{_c('0;31', f'Validation failed with {r.errors} error(s).')}")
        sys.exit(1)
    else:
        print(f"\n{_c('0;32', 'Validation passed.')}")


if __name__ == "__main__":
    main()
