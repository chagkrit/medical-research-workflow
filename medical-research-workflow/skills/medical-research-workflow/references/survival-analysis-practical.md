# Survival Analysis Practical Module

Use this module for time-to-event outcomes, Kaplan-Meier curves, log-rank tests, Cox models, landmark analyses, and survival manuscript reporting.

## Required Inputs

- Time origin: randomization, diagnosis, treatment start, admission, test date, or another prespecified anchor.
- Event definition and adjudication.
- Censoring definition and last follow-up rule.
- Follow-up time variable and unit.
- Competing events.
- Delayed entry/left truncation if applicable.
- Recurrent events if applicable.

## Analysis Routing

- Kaplan-Meier: use for descriptive survival probability over time.
- Log-rank test: use for unadjusted group comparison when hazards are plausibly proportional.
- Cox proportional hazards: use for adjusted hazard ratios when PH assumptions are defensible.
- Stratified Cox: use when a covariate violates PH but should be controlled by strata.
- Time-varying effects: consider when PH is violated and effect changes over time.
- Competing risks: use cause-specific hazard or Fine-Gray model depending on estimand.
- Restricted mean survival time: consider when PH is violated or absolute time difference is clinically clearer.

## Script Routing

- Use `scripts/advanced_stats.py survival` for Cox proportional hazards with optional strata, robust variance, and proportional hazards testing.
- Do not use the script output alone for competing risks, recurrent events, left truncation, or time-varying covariates unless the analysis has been extended and validated.

## Assumption Checks

- Proportional hazards via Schoenfeld residual tests or equivalent diagnostics.
- Log-minus-log curve plausibility where appropriate.
- Functional form of continuous covariates.
- Influential observations and sparse events.
- Event-per-parameter adequacy.
- Independent/non-informative censoring plausibility.

## Reporting

- Report number at risk over time for KM curves.
- Report median follow-up method.
- Report number of events and censored observations.
- Report HR, 95% CI, p value, and absolute survival probabilities at clinically relevant times.
- State whether HRs are adjusted or unadjusted.
- State how missing covariates were handled.

## Reviewer Questions

- Is the time origin clinically valid and identical across groups?
- Are censoring assumptions plausible?
- Was proportional hazards tested and handled?
- Are competing risks ignored when they matter?
- Are event counts sufficient for the model complexity?
