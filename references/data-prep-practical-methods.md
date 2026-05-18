# Data Preparation Practical Methods

Use this module for hands-on data profiling, cleaning, missingness decisions, imputation planning, outlier review, and variable coding before analysis.

## Data Profiling

Produce a data profile before cleaning:

- Number of rows and columns.
- Variable names, types, units, and labels.
- Missingness by variable.
- Duplicate records.
- Out-of-range values.
- Date inconsistencies.
- Continuous distributions and categorical levels.
- Candidate identifiers and linkage keys.

## Missingness Decision Guide

- <5% missing and plausibly MCAR: complete-case analysis may be acceptable; compare included vs excluded records.
- 5-20% missing and plausible MAR: consider multiple imputation or deterministic imputation for sensitivity only.
- 20-40% missing: require sensitivity analysis and careful limitations.
- MNAR concern: use pattern-mixture, delta adjustment, or explicit sensitivity analysis.
- Missing outcome/time-to-event variables: do not impute mechanically without protocol/statistician justification.

## Imputation Review

Before imputation:

- Separate structural missingness from data capture missingness.
- Include predictors of missingness and outcome in the imputation model.
- Preserve categorical/ordinal structure where possible.
- Compare distributions before and after imputation.
- Document variables imputed and number of values imputed.

## Outlier Review

Do not remove outliers automatically.

Classify:

- Data entry/unit error.
- Biologically implausible value.
- Plausible extreme clinical value.
- Influential observation needing sensitivity analysis.

Actions:

- Correct if source evidence supports correction.
- Flag if uncertain.
- Winsorize only with prespecified rationale.
- Run sensitivity analysis excluding or retaining influential observations when needed.

## Variable Coding

- Binary variables: define `1` as event/exposed when scripts require it.
- Categorical variables: document reference category.
- Ordinal variables: preserve order and avoid arbitrary numeric treatment unless justified.
- Continuous variables: keep continuous when possible; avoid unnecessary dichotomization.
- Derived variables: document exact formula and source variables.

## Reviewer Questions

- Can raw-to-analysis data transformations be reproduced?
- Were exclusions and corrections outcome-blinded?
- Were imputation and outlier decisions prespecified or sensitivity-tested?
- Are variable codings aligned with statistical formulas and manuscript interpretation?
