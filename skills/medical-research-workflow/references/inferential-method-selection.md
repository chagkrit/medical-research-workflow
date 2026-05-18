# Inferential Method Selection

Use this module when choosing tests for unadjusted analysis, Table 1, secondary outcomes, or sensitivity analyses.

## Decision Rules

- Match the test to outcome scale, design, pairing, clustering, and distribution.
- Prefer effect sizes and confidence intervals over p values alone.
- Treat normality tests as aids, not mechanical decision makers; inspect sample size, skewness, outliers, and clinical scale.
- Use exact or simulation methods for sparse categorical tables.
- Avoid p-value based variable selection for primary multivariable models.

## Common Choices

Continuous independent groups:

- Approximately normal, similar variance: t-test.
- Unequal variance: Welch t-test.
- Skewed/small sample: Mann-Whitney U with distributional interpretation.
- More than two groups: ANOVA/Welch ANOVA or Kruskal-Wallis.

Paired/repeated continuous:

- Paired t-test for approximately normal paired differences.
- Wilcoxon signed-rank for non-normal paired differences.
- GEE/mixed models for repeated measures beyond two time points.

Categorical:

- Chi-square for adequate expected cell counts.
- Fisher exact for sparse 2x2 tables.
- McNemar for paired binary data.
- Logistic/Poisson models when adjustment or effect estimation is needed.

Time-to-event:

- Kaplan-Meier for survival probabilities.
- Log-rank for unadjusted comparison.
- Cox or alternative survival model for adjusted effects.

Diagnostic accuracy:

- 2x2 accuracy estimates for binary tests.
- ROC/AUC for continuous scores.
- Calibration and decision curve analysis for clinical prediction/decision tools.

## Script Routing

- Use `scripts/clinical_stats.py` for deterministic first-pass summaries, Welch t-test, chi-square, Fisher exact, and 2x2 estimates.
- Use `scripts/advanced_stats.py` for regression, GEE, Cox, imputation, propensity, and prediction workflows.
- Escalate beyond bundled scripts for exact RxC tests, DeLong AUC comparison, mixed-effects models, Fine-Gray competing risks, and formal multiple imputation pooling.

## Reviewer Questions

- Does the test match the design and data structure?
- Are paired or clustered observations mistakenly treated as independent?
- Are assumptions checked and reported?
- Are effect sizes clinically interpretable?
- Is multiplicity handled for many tests?
