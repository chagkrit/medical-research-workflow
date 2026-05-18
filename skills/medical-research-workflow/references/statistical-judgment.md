# Statistical Judgment Review

Use this review after drafting an analysis plan, before running `advanced_stats.py`, after model output is produced, and before manuscript interpretation. The goal is to identify issues that deterministic scripts cannot decide.

## Required Review Output

Produce a judgment table with:

- Domain: formula, coding, assumptions, convergence, confounding, missingness, interpretation.
- Finding.
- Severity: critical, major, minor, or acceptable.
- Evidence checked.
- Action required.
- Status.

Use `assets/statistical_judgment_template.md` when a reusable table is useful.

## Formula Review

Check that the model formula matches the research question and estimand:

- Outcome is correctly specified and matches its scale: continuous, binary, count, ordinal, repeated, or time-to-event.
- Exposure/intervention term matches protocol coding and contrast.
- Covariates are prespecified or clearly justified as post hoc.
- Interactions are included only when clinically/protocol justified and interpretable.
- Nonlinear relationships are handled when plausible: splines, transformations, categories, or sensitivity analysis.
- Time variables are correctly represented for survival or longitudinal models.
- Offset terms are included for rates when person-time/exposure time differs.
- Cluster/subject IDs are specified for repeated or clustered data.
- Formula syntax uses categorical markers where needed, such as `C(sex)` in statsmodels formulas.

Reviewer challenge: "How does this formula map to the estimand, and why are these terms included or excluded?"

## Coding Review

Verify variable coding before interpreting output:

- Binary outcomes use the intended event as `1`.
- Treatment/exposure direction is clear: exposed vs unexposed, intervention vs control.
- Reference categories are clinically sensible and documented.
- Ordinal variables are not treated as continuous unless justified.
- Dates, follow-up time, event indicators, and censoring are correctly coded.
- Units are consistent across sites/time.
- Missing values are true missing values, not accidental zeros or strings.
- Rare categories are handled before modeling.
- Derived variables can be reproduced from source variables.

Reviewer challenge: "Could reversed coding or an inappropriate reference level change the conclusion?"

## Assumption Review

Match diagnostics to model type:

- Linear regression: linearity, residual distribution, heteroscedasticity, influential observations.
- Logistic regression: sparse cells, separation, linearity in the logit for continuous predictors, calibration if used predictively.
- Poisson/count models: overdispersion, zero inflation, offset correctness.
- Cox models: proportional hazards, censoring assumptions, influential observations, event count per parameter.
- GEE/repeated measures: cluster size, working correlation, time ordering, missing visits/dropout.
- Propensity methods: exchangeability, positivity/overlap, covariate balance, extreme weights.
- Prediction models: calibration, discrimination, optimism, leakage, class imbalance, external validity.
- Imputation: missingness mechanism, imputation model compatibility, variables included, diagnostics, sensitivity analysis.

Reviewer challenge: "What diagnostics show that the model assumptions are acceptable or that violations were handled?"

## Convergence And Numerical Review

Treat convergence warnings as analysis findings, not console noise:

- Record all warnings from `statsmodels`, `lifelines`, and `sklearn`.
- Check non-convergence, singular matrix, complete/quasi separation, infinite estimates, huge standard errors, and implausible confidence intervals.
- Check condition number/collinearity when available.
- Confirm event-per-parameter or sample-size adequacy.
- Simplify overfit models, collapse sparse categories, penalize models, or revise the analysis plan when needed.
- Never report unstable estimates as if they were robust.

Reviewer challenge: "Were there convergence or separation problems, and how did you address them?"

## Confounding Review

Assess confounding before accepting adjusted estimates:

- Define the target causal or associational estimand.
- List known confounders based on clinical knowledge and prior evidence.
- Identify mediators, colliders, and variables affected by exposure; avoid adjusting for them unless the estimand requires it.
- Prefer a DAG or explicit causal rationale for observational studies.
- Compare unadjusted and adjusted estimates; explain meaningful changes.
- For propensity methods, require balance diagnostics after weighting/matching, not only propensity model fit.
- Consider residual confounding from unmeasured or poorly measured variables.
- Avoid causal language if exchangeability, positivity, consistency, and measurement assumptions are not defensible.

Reviewer challenge: "Why is this covariate set sufficient, and did you avoid overadjustment or collider bias?"

## Decision Rules

- If formula/coding is wrong, stop and fix before interpreting output.
- If assumptions are materially violated, run a sensitivity analysis or choose a more appropriate model.
- If convergence is unstable, do not use the estimate for manuscript claims without resolving or clearly labeling the limitation.
- If confounding control is weak, downgrade causal language and strengthen limitations.
- If uncertainty is high, report imprecision rather than forcing significance-focused language.

## Manuscript Translation

When writing Methods and Results:

- State model family, formula-level covariate set, covariance/cluster handling, missing-data handling, and software.
- Report diagnostics and sensitivity analyses that matter to credibility.
- Label adjusted, unadjusted, weighted, imputed, exploratory, and post hoc analyses.
- Keep causal claims proportional to design and assumptions.
