# Diagnostic Accuracy Module

Use this module for STARD-oriented diagnostic accuracy studies, biomarker thresholds, clinical prediction cutpoints, ROC/AUC reporting, and diagnostic test manuscripts.

## Required Inputs

- Index test definition and measurement timing.
- Reference standard definition and blinding status.
- Target condition.
- Study design: cohort, case-control, two-gate, retrospective, prospective.
- Unit of analysis: patient, lesion, image, specimen, encounter.
- Threshold handling: prespecified, optimized, multiple thresholds, or continuous score.
- Indeterminate, missing, and uninterpretable results handling.

## Core Metrics

Report with denominators:

- True positive, false positive, false negative, true negative.
- Sensitivity and specificity.
- Positive predictive value and negative predictive value.
- Positive and negative likelihood ratios.
- Diagnostic odds ratio when useful.
- AUC with confidence interval for continuous/ordinal tests.
- Calibration and clinical utility when the test is used for prediction or decision support.

## Script Routing

- Use `scripts/clinical_stats.py` for deterministic 2x2 first-pass counts and unadjusted OR/RR when the index test and reference standard are already binary.
- Use `scripts/advanced_stats.py prediction` only for first-pass holdout discrimination metrics.
- Use full statistical software or a dedicated analysis script for DeLong AUC comparisons, bootstrap confidence intervals, net benefit, clustered diagnostic designs, and multiple-reader/multiple-case studies.

## Threshold Review

- Prefer prespecified thresholds.
- If selecting an optimal cutpoint, label it as data-derived and validate it.
- Do not report a data-derived threshold as if it were externally validated.
- For multiple thresholds, avoid cherry-picking; show clinically meaningful thresholds.

## STARD Reporting

Methods must specify:

- Participant eligibility and recruitment.
- Whether sampling was consecutive, random, or convenience-based.
- Index test conduct and interpretation.
- Reference standard conduct and interpretation.
- Blinding between index test and reference standard.
- Time interval between tests.
- Handling of missing/indeterminate results.
- Statistical methods for accuracy estimates and uncertainty.

## Reviewer Questions

- Was the reference standard appropriate and applied consistently?
- Were index test readers blinded to the reference standard?
- Was spectrum bias possible?
- Were thresholds prespecified or optimized post hoc?
- Were indeterminate results excluded in a way that inflates accuracy?
- Are PPV/NPV interpreted in relation to disease prevalence?
