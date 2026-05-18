# Propensity And Balance Methods

Use this module for observational treatment/exposure comparisons, baseline imbalance, confounding control, propensity score weighting/matching, SMD diagnostics, and balance reporting.

## Method Selection

- Use covariate adjustment when the model is simple, sample size supports it, and confounding structure is clear.
- Use IPTW when estimating marginal treatment effects and overlap is adequate.
- Use matching when creating a comparable analytic cohort is more transparent than weighting.
- Use stratification/subclassification when propensity score distributions are stable and strata are interpretable.
- Use ANCOVA in randomized trials with baseline imbalance for continuous outcomes when baseline covariates are prognostic.

## Covariate Selection

Include variables associated with treatment assignment and outcome based on clinical knowledge.

Avoid:

- Mediators affected by exposure.
- Colliders.
- Instrument-like variables that predict treatment but not outcome if they worsen precision/positivity.
- Post-baseline variables unless the estimand requires them.

## Script Routing

- Use `scripts/advanced_stats.py propensity` for deterministic propensity-score estimation, IPTW calculation, and standardized mean difference diagnostics.
- Use `scripts/advanced_stats.py regression` with weights only after the script is extended to support weighted outcome models; otherwise run weighted outcome models in full statistical software and document the exact command.
- Use `statistical-judgment.md` to review positivity, exchangeability, and overadjustment before causal interpretation.

## Balance Diagnostics

Report before and after adjustment:

- SMD for each covariate.
- Thresholds: SMD < 0.1 usually acceptable; 0.1-0.2 borderline; >0.2 concerning.
- Propensity score overlap/common support.
- Extreme weights and trimming/winsorization if applied.
- Effective sample size after weighting.

## Reviewer Questions

- Were confounders selected by clinical/causal reasoning, not p values?
- Is positivity/common support adequate?
- Did weighting/matching improve balance?
- Were extreme weights handled transparently?
- Is the causal claim proportional to remaining residual confounding risk?
