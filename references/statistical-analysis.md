# Statistical Analysis

## Analysis Plan

Define before modeling:

- Primary estimand and contrast.
- Outcome type and measurement timing.
- Exposure/intervention definition.
- Confounders, mediators, colliders, and effect modifiers.
- Primary model.
- Secondary and exploratory models.
- Sensitivity analyses.
- Multiplicity approach.
- Clinically meaningful effect size.

## Deterministic Script Use

Use `scripts/clinical_stats.py` for reproducible first-pass CSV analyses when the requested scope is descriptive, Table 1, unadjusted two-group comparisons, or 2x2 effect estimates. Use `scripts/advanced_stats.py` for reproducible advanced analyses when the requested scope is multivariable regression, Cox survival analysis, GEE clustered/repeated-measures modeling, numeric iterative imputation, propensity-score IPTW/balance, or holdout prediction metrics. Read `references/deterministic-stat-scripts.md` before running either script.

Do not use bundled script output as a substitute for protocol-specific statistical judgment. A script can make analysis reproducible; it cannot decide estimands, confounder sets, causal validity, missing-data assumptions, or manuscript interpretation.

## Statistical Judgment Gate

Read `references/statistical-judgment.md` before accepting advanced model output. Complete a judgment matrix for formula validity, variable coding, assumptions, convergence/numerical stability, confounding control, missing-data implications, and interpretation strength.

Stop interpretation until critical formula, coding, convergence, or confounding findings are resolved. If unresolved issues remain, label the analysis as exploratory or sensitivity-only and downgrade manuscript claims.

## Model Selection Guide

- Continuous outcome: linear model or robust/semiparametric alternative; inspect residuals and nonlinearity.
- Binary outcome: logistic, log-binomial, Poisson with robust variance, or risk-difference model depending on estimand.
- Count outcome: Poisson, negative binomial, zero-inflated, or rate model with offset.
- Time-to-event outcome: Kaplan-Meier, Cox, flexible parametric, competing-risk methods, or restricted mean survival time.
- Repeated/clustered data: mixed-effects models, GEE, cluster-robust variance, or hierarchical models.
- Prediction modeling: separate development/validation; report calibration, discrimination, decision utility, and optimism correction.
- Observational causal analysis: justify confounder set with clinical knowledge/DAG; consider propensity scores, weighting, matching, g-methods, or target trial emulation.

For detailed method modules, read:

- `references/inferential-method-selection.md` for unadjusted test selection.
- `references/survival-analysis-practical.md` for time-to-event analysis.
- `references/diagnostic-accuracy.md` for STARD diagnostic accuracy.
- `references/propensity-balance-methods.md` for balancing and propensity methods.

## Diagnostics

Check assumptions relevant to the chosen model:

- Linearity and functional form.
- Independence and clustering.
- Distributional assumptions.
- Influential observations.
- Proportional hazards.
- Collinearity.
- Sparse data and separation.
- Overfitting and events-per-parameter concerns.
- Balance after matching/weighting.

## Reporting

Report:

- Effect estimate, confidence interval, and p value when appropriate.
- Absolute risk or mean difference when interpretable.
- Denominators for each analysis.
- Covariates included and rationale.
- Handling of missing data.
- Sensitivity and subgroup analyses clearly labeled.
- Software and packages.

## Reviewer Questions

- Does the model answer the stated estimand?
- Were assumptions tested and failures handled?
- Is confounding controlled without adjusting for mediators/colliders?
- Were formula, coding, assumptions, convergence, and confounding reviewed explicitly?
- Is multiplicity addressed for many outcomes/subgroups?
- Are claims proportional to study design and precision?
