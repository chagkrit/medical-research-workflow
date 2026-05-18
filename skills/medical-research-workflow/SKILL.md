---
name: medical-research-workflow
description: End-to-end medical research workflow for clinical, epidemiologic, biomedical, public-health, health-services, and translational research projects. Use when Codex needs to design or execute data preparation, data cleaning, missing-data management, statistical analysis, manuscript drafting, verified citation from standard databases, reporting-guideline alignment, or simulated peer review for medical research deliverables.
---

# Medical Research Workflow

## Operating Standard

Run medical research work as a reproducible, audit-ready workflow. Treat every analytic choice as something a statistician, clinician, reviewer, or editor may challenge.

Do not invent citations, effect estimates, p values, guideline requirements, database contents, or clinical claims. If a fact, citation, guideline, drug label, diagnostic criterion, or current recommendation matters, verify it from an authoritative source before using it.

Use this skill for research support, not medical care. Do not provide patient-specific diagnosis or treatment advice.

## Workflow

1. **Frame the study**
   - Define research question using PICO/PECO/PIRT as appropriate.
   - Specify study design, population, exposure/intervention, comparator, outcomes, time origin, follow-up, and estimand.
   - Identify protocol, registry, IRB/ethics constraints, data-use constraints, and target journal/reporting guideline.
   - Create an analysis decision log before touching results.

2. **Prepare data**
   - Read `references/data-prep-cleaning.md` when handling raw datasets, codebooks, dictionaries, EHR extracts, registry files, REDCap exports, claims, or lab data.
   - Read `references/data-prep-practical-methods.md` when the task needs hands-on profiling, outlier handling, variable coding, or imputation decision support.
   - Build a data inventory: source, extraction date, inclusion window, identifiers, linkage keys, units, coding systems, and provenance.
   - Preserve raw data. Work from scripted derived datasets. Record exclusions with counts and reasons.

3. **Clean data**
   - Separate factual fixes from analytic recoding.
   - Validate IDs, dates, ranges, units, duplicates, outcome definitions, medication/lab mappings, and impossible clinical sequences.
   - Produce a cleaning report that includes every rule, affected row count, and unresolved anomaly.

4. **Manage missing data**
   - Read `references/missing-data.md` before deletion, imputation, missing-indicator modeling, inverse-probability weighting, or sensitivity analysis.
   - Describe missingness by variable and key strata. Assess plausible MCAR/MAR/MNAR mechanisms.
   - Match the strategy to the estimand and design. Never default to complete-case analysis without justification.

5. **Analyze statistically**
   - Read `references/statistical-analysis.md` before modeling, hypothesis testing, survival analysis, repeated-measures analysis, propensity methods, prediction modeling, subgroup analysis, or multiplicity handling.
   - Read `references/inferential-method-selection.md` when choosing unadjusted tests or Table 1 methods.
   - Read `references/survival-analysis-practical.md` for time-to-event outcomes, Cox models, KM/log-rank, landmark analysis, or competing-risk concerns.
   - Read `references/diagnostic-accuracy.md` for ROC/AUC, sensitivity/specificity, calibration, decision curve analysis, or STARD diagnostic studies.
   - Read `references/propensity-balance-methods.md` for observational balancing, SMD, propensity scores, IPTW, matching, or ANCOVA for imbalance.
   - Use `scripts/clinical_stats.py` for deterministic first-pass CSV analysis when the task needs missingness summaries, descriptive statistics, Table 1 group comparisons, Fisher exact tests, or simple 2x2 effect estimates.
   - Use `scripts/advanced_stats.py` for deterministic advanced analyses when the task needs multivariable regression, Cox survival models, GEE clustered/repeated-measures models, numeric iterative imputation, propensity-score IPTW/balance diagnostics, or holdout prediction-model metrics.
   - Read `references/statistical-judgment.md` before interpreting advanced model output; explicitly review formula, coding, assumptions, convergence, confounding, missingness, and claim strength.
   - Predefine primary, secondary, exploratory, and sensitivity analyses.
   - Check assumptions, diagnostics, precision, clinical relevance, and robustness. Report uncertainty, not only p values.

6. **Write manuscript**
   - Read `references/manuscript-and-reporting.md` before drafting or revising.
   - Read `references/manuscript-master-router.md` when the task asks for manuscript development, peer review, language refinement, journal strategy, reviewer response, submission readiness, or end-to-end manuscript support.
   - Read `references/imrad-writing-guide.md` for section-level IMRAD drafting.
   - Read `references/reporting-guidelines-expanded.md` for design-specific checklist alignment.
   - Read `references/manuscript-consistency-qc.md` before finalizing tables, figures, captions, or results text.
   - Read `references/deep-manuscript-review.md` for high-level quality review, overclaiming checks, editor-eye review, and reviewer anticipation.
   - Use the correct reporting guideline: CONSORT, STROBE, PRISMA, TRIPOD, STARD, CARE, ARRIVE, CHEERS, RECORD, or another design-specific standard.
   - Keep Methods detailed enough to reproduce the study. Keep Results factual and separate from interpretation.

7. **Verify citations**
   - Read `references/citation-integrity.md` before adding references.
   - Read `references/citation-search-strategy-expanded.md` when building Introduction/Discussion references or clinical evidence support.
   - Use PubMed/MEDLINE, Crossref, DOI resolver, Cochrane Library, ClinicalTrials.gov, WHO, FDA/EMA, CDC, professional society guidelines, journal pages, or other authoritative databases.
   - Require a traceable identifier for each citation when available: PMID, PMCID, DOI, trial registration number, guideline URL, or agency document ID.
   - Never cite a paper from memory unless verified during the task.

8. **Simulate peer review**
   - Read `references/peer-review-modules.md` for module-specific reviewer challenges.
   - Read `references/causal-manuscript-review-panel.md` when the manuscript contains causal, mechanistic, environmental exposure, survival disparity, mediation, policy, or equity claims.
   - Run review after each module and again on the full draft.
   - Record: concern, severity, likely reviewer wording, evidence needed, proposed fix, and whether the fix was implemented.

## Required Outputs

For substantial tasks, produce these artifacts or their concise equivalents:

- Study question and estimand summary.
- Data provenance and cleaning log.
- Missing-data table and strategy rationale.
- Statistical analysis plan with diagnostics and sensitivity analyses.
- Manuscript draft or section revision.
- Verified citation table with identifiers and source links.
- Simulated peer-review matrix by module.

## Evidence Rules

- Mark unverifiable claims as `needs verification` instead of smoothing over uncertainty.
- Distinguish protocol-defined analyses from post hoc analyses.
- Report absolute effects where possible, not only relative effects.
- Avoid causal language unless the design and assumptions support causal interpretation.
- State limitations tied to bias, confounding, measurement error, missingness, power, generalizability, and multiplicity.

## Resource Guide

- `references/data-prep-cleaning.md`: Data intake, cleaning, provenance, and audit trails.
- `references/data-prep-practical-methods.md`: Practical profiling, missingness decisions, outlier review, imputation review, and variable coding.
- `references/missing-data.md`: Missingness diagnosis, imputation, sensitivity analysis, and reporting.
- `references/statistical-analysis.md`: Model selection, assumptions, diagnostics, and reporting.
- `references/inferential-method-selection.md`: Test selection for unadjusted inference, Table 1, and sensitivity analyses.
- `references/deterministic-stat-scripts.md`: Usage and interpretation rules for bundled deterministic statistical scripts.
- `references/statistical-judgment.md`: Review checklist for formula, coding, assumptions, convergence, confounding, and interpretation.
- `references/survival-analysis-practical.md`: Survival-analysis routing, assumptions, and reporting.
- `references/diagnostic-accuracy.md`: STARD-oriented diagnostic accuracy workflow and reviewer checks.
- `references/propensity-balance-methods.md`: Propensity-score, IPTW, balance diagnostics, and confounding review.
- `references/manuscript-and-reporting.md`: Manuscript structure and reporting guideline alignment.
- `references/manuscript-master-router.md`: Mode router for manuscript develop, evaluate, language refine, journal strategy, and full-pipeline support.
- `references/manuscript-master-develop.md`: Deep manuscript development mentor workflow with revision blueprint and multi-reviewer simulation.
- `references/manuscript-master-peer-review.md`: Structured peer-review checklist with core domains and method-specific add-ons.
- `references/manuscript-language-refiner.md`: Ethical academic English refinement while preserving scientific integrity.
- `references/journal-strategy.md`: Journal fit, desk-reject risk, writing culture, and Plan A/B/C submission strategy.
- `references/imrad-writing-guide.md`: Practical IMRAD section drafting guide.
- `references/reporting-guidelines-expanded.md`: Expanded CONSORT, STROBE, STARD, and TRIPOD checklist guidance.
- `references/manuscript-consistency-qc.md`: Manuscript-table-figure consistency and publication figure QC.
- `references/deep-manuscript-review.md`: Deep quality review for gap, novelty, overclaiming, limitations, and reviewer anticipation.
- `references/citation-integrity.md`: Database-first citation workflow and anti-hallucination checks.
- `references/citation-search-strategy-expanded.md`: Expanded literature search strategy and evidence-priority routing.
- `references/peer-review-modules.md`: Reviewer challenge prompts for every module.
- `references/causal-manuscript-review-panel.md`: Five-reviewer adversarial panel for causal, mediation, policy, equity, and missing-data fragility claims.
- `scripts/clinical_stats.py`: Standard-library CSV statistics runner for missingness, Table 1, Welch t-test, chi-square/Fisher exact, and 2x2 effects.
- `scripts/advanced_stats.py`: Dependency-aware advanced statistics runner for regression, Cox survival, GEE, imputation, propensity scores, and prediction metrics.
- `assets/peer_review_matrix_template.md`: Reusable review table.
- `assets/citation_verification_table.md`: Reusable citation verification table.
- `assets/statistical_judgment_template.md`: Reusable table for statistical judgment findings.
