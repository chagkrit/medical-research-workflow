# medical-research-workflow

Claude marketplace/local plugin and Codex skill for an audit-ready medical research workflow.

## What It Does

- Data preparation, cleaning, missing-data management, and variable coding.
- Deterministic first-pass and advanced statistical scripts.
- Statistical judgment gates for formula, coding, assumptions, convergence, confounding, and claim strength.
- Manuscript writing, reporting guideline alignment, language refinement, and journal strategy.
- Verified citation workflow with anti-hallucination rules.
- Simulated peer review, including a causal manuscript reviewer panel.

## Claude Marketplace Layout

Claude plugin installers should use:

- `.claude-plugin/marketplace.json` - marketplace repository manifest.
- `medical-research-workflow/.claude-plugin/plugin.json` - plugin metadata.
- `medical-research-workflow/.mcp.json` - optional scholarly MCP server declarations.
- `medical-research-workflow/skills/medical-research-workflow/SKILL.md` - installable Claude skill.
- `medical-research-workflow/skills/medical-research-workflow/references/` - deep workflow modules.
- `medical-research-workflow/skills/medical-research-workflow/scripts/` - deterministic analysis scripts.

## Codex Layout

The root-level `SKILL.md`, `references/`, `scripts/`, `assets/`, and `agents/` are kept for direct Codex skill use.

## Core Scripts

- `scripts/clinical_stats.py` - deterministic first-pass CSV statistics.
- `scripts/advanced_stats.py` - regression, GEE, Cox survival, imputation, propensity, and prediction workflows.

This skill is for research support, not patient-specific medical advice.
