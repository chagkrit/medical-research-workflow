# Simulated Peer Review Modules

Run these challenges after each module. Output findings as: `module`, `concern`, `severity`, `likely reviewer wording`, `evidence needed`, `fix`, `status`.

## Data Preparation Review

- Are source data and derived data separated?
- Are inclusion/exclusion decisions reproducible?
- Are all transformations scripted or logged?
- Could linkage, duplicate handling, or unit conversion introduce bias?
- Is the cohort flow auditable?

## Cleaning Review

- Were cleaning rules defined before outcome-aware analysis?
- Are outliers handled transparently?
- Are clinically impossible values investigated rather than blindly removed?
- Are coding systems mapped correctly?
- Are site/time measurement differences considered?

## Missing Data Review

- Is missingness quantified and stratified?
- Is the chosen method justified by a plausible mechanism?
- Does the imputation/weighting model include relevant predictors?
- Are diagnostics and sensitivity analyses reported?
- Could missing outcome data change conclusions?

## Statistical Review

- Does the model match the estimand and outcome scale?
- Was a statistical judgment matrix completed for formula, coding, assumptions, convergence, and confounding?
- Are confounders chosen by causal/clinical reasoning?
- Are assumptions checked?
- Were convergence warnings, separation, sparse data, collinearity, or unstable estimates handled?
- Is multiplicity addressed?
- Are effect sizes clinically meaningful and precisely estimated?
- Are subgroup analyses credible or exploratory?

## Survival Review

- Is time origin clinically valid and identical across groups?
- Are censoring rules and follow-up definitions clear?
- Was proportional hazards assessed for Cox models?
- Are competing risks or recurrent events relevant and handled?
- Are at-risk counts, events, and censoring reported?

## Diagnostic Accuracy Review

- Is the reference standard appropriate and consistently applied?
- Were index-test readers blinded to the reference standard?
- Are sensitivity, specificity, predictive values, and likelihood ratios reported with denominators?
- Were thresholds prespecified or clearly labeled as data-derived?
- Are indeterminate and missing test results reported?

## Propensity/Balance Review

- Were covariates selected by clinical/causal reasoning?
- Is overlap/common support adequate?
- Are SMDs reported before and after weighting/matching?
- Are extreme weights handled transparently?
- Is causal language justified after residual confounding review?

## Manuscript Review

- Does the title/abstract match the design and findings?
- Are Methods reproducible?
- Are Results complete and nonselective?
- Do manuscript numbers match tables, figures, captions, and statistical outputs?
- Are figure labels, legends, axes, units, and confidence intervals publication-ready?
- Are limitations specific and consequential?
- Are conclusions proportionate?
- If the task is a full manuscript evaluation, use `references/manuscript-master-peer-review.md` for the structured core checklist and method-specific add-ons.
- If the task is manuscript development rather than evaluation only, use `references/manuscript-master-develop.md` to create a revision blueprint.
- If the task is submission targeting, use `references/journal-strategy.md` after citation/reporting/statistical checks.

## Citation Review

- Is every major claim backed by a verified source?
- Are citation identifiers present?
- Are guidelines current and official?
- Are any sources retracted, preprints, editorials, or low-quality evidence?
- Does the manuscript cite what the source actually says?
