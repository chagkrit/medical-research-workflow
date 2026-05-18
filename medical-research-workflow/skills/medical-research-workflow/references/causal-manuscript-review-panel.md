# Causal Manuscript Review Panel

Use this panel when a manuscript makes causal, mechanistic, environmental exposure, survival disparity, mediation, policy, equity, or public-health translation claims.

The panel is intentionally adversarial. Its job is to identify where the manuscript's causal story, strongest statistical evidence, policy framing, equity interpretation, and missing-data strategy do not align.

## Output Format

Use this matrix:

| Reviewer | Domain | Critique | Severity | Evidence checked | Required revision | Status |
|---|---|---|---:|---|---|---|

Severity:

- `+1`: moderate concern; must clarify or temper.
- `+2`: major concern; requires substantive revision, sensitivity analysis, or reframing.
- `+3`: critical concern; current claim is not supported and risks rejection or misleading interpretation.

## Reviewer 1: Logical Systems Thinker

Focus: causality, mediation, causal chain coherence, collider/mediator/confounder separation, biological versus systems pathway.

Challenge prompts:

- Does the proposed mechanism match the statistical evidence?
- If the exposure effect disappears after adjusting for a mediator or clinical prognostic factor, is the manuscript still claiming a direct biological effect?
- Are mediators, confounders, and colliders clearly distinguished?
- Are post-exposure variables being adjusted for in a way that changes the estimand?
- Are treatment variables mediators, confounders, competing explanations, or part of the causal pathway?
- Does sequential modeling show direct effect, mediated effect, confounding, or loss of precision?

Common critique patterns:

- "The manuscript proposes a biological mechanism, but the adjusted/sequential model suggests the disparity is largely explained by `[mediator/prognostic factor]`."
- "If `[exposure]` affects `[outcome]` primarily through delayed diagnosis or advanced presentation, the causal story is a healthcare-access pathway, not direct biological aggressiveness."
- "Excluding strongly prognostic treatment variables undermines the causal framework unless the estimand explicitly excludes treatment-mediated pathways."

Required revisions:

- Redraw causal pathway or provide a DAG.
- Reframe direct biological claims as hypothesis-generating if direct evidence is weak.
- State whether the estimand is total effect, direct effect, mediated effect, or association.
- Add sensitivity analysis or mediation analysis only if the data support it.

## Reviewer 2: Framework Alignment Enforcer

Focus: claims versus strongest evidence, abstract accuracy, conclusion calibration, cherry-picking, model hierarchy.

Challenge prompts:

- Does the abstract conclusion match the most rigorous prespecified model?
- Are crude/univariable/complete-case results emphasized while adjusted/imputed/sensitivity results are weaker?
- Is statistical significance disappearing in the analysis that best handles missingness or confounding?
- Are non-significant findings described as robust?
- Are sensitivity analyses treated as primary evidence?

Common critique patterns:

- "The abstract says `[exposure]` is robustly associated with `[outcome]`, but the most rigorous adjusted/imputed model does not support that conclusion."
- "The manuscript buries the main result: after accounting for `[clinical covariates/missing data]`, the association is attenuated and non-significant."
- "Relying on a reduced complete-case sample while downplaying imputed or adjusted estimates is statistical cherry-picking."

Required revisions:

- Make the strongest/most appropriate model the interpretive anchor.
- Reframe the conclusion around supported findings.
- Move discordant sensitivity results into a transparent limitations paragraph.
- Replace "robust association" with calibrated language when evidence is inconsistent.

## Reviewer 3: Policy And Impact Strategist

Focus: policy relevance, exposure threshold validity, intervention actionability, exposure misclassification, translation.

Challenge prompts:

- Is the cutoff clinically, biologically, or policy-relevant?
- Does the threshold create extreme imbalance or dilute statistical power?
- Does the exposure definition match the causal window relevant to the outcome?
- Is exposure assigned at a geographic/time scale too crude for the claim?
- Are policy implications stronger than the exposure measurement supports?
- Does the manuscript challenge or reinforce existing standards with adequate evidence?

Common critique patterns:

- "The chosen `[policy cutoff]` classifies most participants into one exposure category, weakening power and interpretability."
- "A `[geographic-unit/time-window]` exposure assignment is too blunt for individual-level survival or biological claims."
- "Policy implications are limited because cumulative, post-diagnosis, occupational, indoor, or residential-history exposure is not measured."

Required revisions:

- Justify cutoff selection and report alternative thresholds or continuous exposure sensitivity when possible.
- Reframe policy claims to match exposure measurement precision.
- Identify what policy question the data can and cannot answer.
- Add exposure-misclassification limitations.

## Reviewer 4: Equity-Critical Lens

Focus: social determinants, access to care, screening, geography, structural confounding, health inequity.

Challenge prompts:

- Could socioeconomic status, health literacy, screening, referral delay, treatment access, or geography explain the association?
- Are rural/peri-urban or disadvantaged areas overrepresented in high exposure groups?
- Does the manuscript biologicalize what may be structural healthcare inequity?
- Are unavailable equity variables acknowledged as major unmeasured confounders?
- Are policy conclusions sensitive to access-to-care bias?

Common critique patterns:

- "The manuscript attributes survival disparities to `[biological mechanism]`, but the observed pattern may reflect `[SES/access/screening/geographic]` confounding."
- "Without SES, screening history, insurance, travel time, or treatment-access variables, the causal interpretation is overextended."
- "The current framing risks mistaking structural healthcare inequity for direct exposure biology."

Required revisions:

- Add structural confounding to the causal framework.
- Temper biological mechanism claims.
- Discuss unavailable equity variables as central limitations, not minor caveats.
- Reframe implications toward screening, early diagnosis, and healthcare access when supported.

## Reviewer 5: Meta-Methodology Challenger

Focus: missing data, imputation validity, MNAR risk, complete-case bias, model fragility, convergence, robustness.

Challenge prompts:

- Are key covariates missing at rates too high for stable primary inference?
- Is MAR plausible, or is MNAR likely?
- Does complete-case significance disappear under imputation?
- Are between-imputation variance, fraction of missing information, and imputation diagnostics reported?
- Are complete-case and imputed samples clinically comparable?
- Are convergence warnings, separation, sparse events, or unstable estimates present?

Common critique patterns:

- "Imputing variables with very high missingness may add substantial uncertainty and makes definitive multivariable claims fragile."
- "The loss of significance in imputed analyses suggests the complete-case result may reflect MNAR selection bias."
- "The registry is too incomplete to definitively support the manuscript's multivariable biological question."

Required revisions:

- Report missingness by variable and exposure/outcome strata.
- Compare complete-case and imputed cohorts.
- Reframe high-missingness models as sensitivity or exploratory if appropriate.
- Add MNAR sensitivity analysis or explicitly state that the data cannot resolve the causal question.

## Integrated Synthesis

After all five reviewers, produce:

1. **Main causal verdict**: direct effect, mediated pathway, confounded association, fragile association, or unsupported claim.
2. **Strongest supported conclusion**: one sentence the manuscript can safely claim.
3. **Claims to remove or downgrade**.
4. **Analyses needed before stronger claims**.
5. **Manuscript sections requiring revision**: abstract, introduction, methods, results, discussion, limitations, figures/tables.

## Claim Calibration Examples

Overstated:

- "`[exposure]` drives `[outcome]` through `[biological mechanism]`."
- "`[exposure]` is robustly associated with poorer survival."
- "Our findings establish a clinically actionable pollution threshold."

Calibrated:

- "`[exposure]` was associated with `[outcome]` in crude analyses, but the association attenuated after adjustment for `[clinical factors]`."
- "Findings are more consistent with `[advanced presentation/access pathway]` than an independently estimated direct survival effect."
- "The data support a hypothesis that environmental exposure may mark structurally disadvantaged diagnostic pathways; direct biological mechanisms require further study."
