# Missing Data Management

## Diagnose Missingness

Describe missingness before choosing a method:

- Missing count and percentage for every analysis variable.
- Missingness by exposure/intervention, outcome, site, time period, demographics, disease severity, and follow-up status.
- Monotone vs intermittent missingness for longitudinal data.
- Structural missingness vs data capture failure vs loss to follow-up.

## Mechanism Framing

Use MCAR, MAR, and MNAR as assumptions, not facts.

- MCAR: missingness unrelated to observed or unobserved data.
- MAR: missingness explainable by observed data included in the imputation/weighting model.
- MNAR: missingness depends on unobserved values or unmeasured processes.

State why the chosen assumption is plausible and what sensitivity analysis challenges it.

## Strategy Selection

- Complete-case analysis: use only when missingness is limited and bias is plausibly small; compare included vs excluded participants.
- Multiple imputation: include outcome, exposure, confounders, auxiliary predictors of missingness, design variables, and transformations/interactions needed by the analysis model.
- Inverse-probability weighting: consider for dropout/loss to follow-up when observation probability can be modeled.
- Missing-indicator method: avoid as a default for confounders; justify if used for operational prediction rather than causal estimation.
- Single imputation: avoid for primary inferential analysis unless clinically deterministic and documented.

## Reporting Minimum

- Number of complete cases for each model.
- Variables imputed and method used.
- Number of imputations and convergence/diagnostics.
- Pooling method.
- Sensitivity analyses under alternative assumptions.
- Any variables not imputed and why.

## Reviewer Questions

- Does the imputation model include all variables needed to make MAR plausible?
- Were transformations handled consistently in imputation and analysis?
- Is the number of imputations adequate for the fraction of missing information?
- Are complete-case and imputed results compared?
- Is MNAR sensitivity analysis needed for key outcomes?
