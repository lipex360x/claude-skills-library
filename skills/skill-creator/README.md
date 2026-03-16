# Skill Creator

Create new skills, iterate on them with eval-driven feedback, and optimize their triggering descriptions — all from within Claude Code.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE.txt)

---

## Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Workflow](#workflow)
- [Scripts](#scripts)
- [Eval Viewer](#eval-viewer)
- [Agents](#agents)
- [Environment Support](#environment-support)

---

## Overview

Skill Creator guides you through the full lifecycle of a Claude skill:

1. **Draft** — capture intent, interview for edge cases, write the SKILL.md
2. **Test** — generate realistic test prompts, run them with and without the skill
3. **Review** — launch a browser-based viewer for qualitative and quantitative evaluation
4. **Iterate** — improve the skill based on user feedback and benchmark data
5. **Optimize** — fine-tune the skill description for accurate triggering
6. **Package** — bundle the skill into a distributable `.skill` file

Each stage is optional and reorderable. Jump in wherever your skill is in the process.

[Back to top](#contents)

---

## Directory Structure

```
skill-creator/
├── SKILL.md              # Skill instructions (loaded by Claude)
├── LICENSE.txt            # Apache 2.0
├── scripts/               # Automation scripts
│   ├── aggregate_benchmark.py
│   ├── generate_report.py
│   ├── improve_description.py
│   ├── package_skill.py
│   ├── quick_validate.py
│   ├── run_eval.py
│   ├── run_loop.py
│   └── utils.py
├── agents/                # Subagent instructions
│   ├── grader.md
│   ├── comparator.md
│   └── analyzer.md
├── references/            # Schemas and documentation
│   └── schemas.md
├── assets/                # HTML templates
│   └── eval_review.html
└── eval-viewer/           # Browser-based review tool
    ├── generate_review.py
    └── viewer.html
```

[Back to top](#contents)

---

## Workflow

### 1. Create or improve a skill

Tell Claude what you want the skill to do. Skill Creator handles the interview, drafts the SKILL.md, and organizes bundled resources (scripts, references, assets).

### 2. Run test cases

Claude generates 2-3 realistic test prompts and runs them in parallel — one with the skill, one without (baseline). Results go into a workspace organized by iteration.

### 3. Review results

The eval viewer opens in your browser with two tabs:

| Tab | What it shows |
|-----|---------------|
| **Outputs** | Side-by-side test case results with inline feedback |
| **Benchmark** | Pass rates, timing, token usage with mean and stddev |

### 4. Iterate

Feedback drives the next revision. Claude generalizes from specific complaints, keeps the prompt lean, and bundles repeated patterns into scripts. Each iteration gets its own directory with fresh baselines.

### 5. Optimize the description

An automated loop tests 20 trigger queries (should-trigger and should-not-trigger) against the skill description, then proposes improvements over multiple iterations. Train/test split prevents overfitting.

### 6. Package

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

Produces a `.skill` file ready for distribution.

[Back to top](#contents)

---

## Scripts

All scripts run as Python modules from the `skill-creator/` directory.

| Script | Purpose |
|--------|---------|
| `run_eval.py` | Evaluate skill triggering against a set of test queries |
| `run_loop.py` | Full description optimization loop (wraps `run_eval` + `improve_description`) |
| `improve_description.py` | Generate improved skill descriptions based on eval failures |
| `aggregate_benchmark.py` | Aggregate grading results into benchmark stats |
| `generate_report.py` | Generate markdown reports from benchmark data |
| `package_skill.py` | Bundle a skill directory into a `.skill` file |
| `quick_validate.py` | Fast validation of skill structure |

[Back to top](#contents)

---

## Eval Viewer

The eval viewer (`eval-viewer/generate_review.py`) launches an interactive HTML page for reviewing test results.

```bash
# Start the viewer server
python eval-viewer/generate_review.py <workspace>/iteration-N \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-N/benchmark.json

# For headless environments, generate a static HTML file
python eval-viewer/generate_review.py <workspace>/iteration-N \
  --skill-name "my-skill" \
  --static output.html
```

For iteration 2+, pass `--previous-workspace` to enable side-by-side comparison with the prior iteration.

[Back to top](#contents)

---

## Agents

Subagent instruction files for specialized evaluation tasks:

| Agent | Role |
|-------|------|
| `grader.md` | Evaluate assertions against skill outputs |
| `comparator.md` | Blind A/B comparison between two output versions |
| `analyzer.md` | Analyze why one version outperformed another |

These are read by Claude when spawning subagents — they are not standalone scripts.

[Back to top](#contents)

---

## Environment Support

| Environment | Parallel runs | Browser viewer | Description optimization |
|-------------|:---:|:---:|:---:|
| **Claude Code** | Yes | Yes | Yes |
| **Cowork** | Yes | Static HTML | Yes |
| **Claude.ai** | No | No | No |

> [!NOTE]
> In Claude.ai, test cases run sequentially and results are presented inline in the conversation. Description optimization requires the `claude` CLI and is unavailable.

[Back to top](#contents)
